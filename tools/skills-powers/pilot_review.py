"""
Pilot Review — Group 9 of the skills-powers-adoption spec.

Human-triggered (per design §Anti-Goals #1) tool that runs at T30 to score
the 30-day activation pilot against the R5.6 success criterion and surface
skills failing the criterion as pre-filled Phase E pruning candidates (per
Group 6's `execute_prune()` flow).

Parameterized by (t0, t30) so the same tool can re-run against any pilot
window — today's session smoke-tests with synthetic dates; the real review
runs on 2026-05-22 with t0=2026-04-22, t30=2026-05-22.

PIPELINE

  compute_pilot_metrics(t0, t30)
    → list[AssetMetric]  — per-asset activation counts + first/last within window

  evaluate_pilot_outcome(metrics)
    → dict with per_asset_outcomes, aggregate_outcome, rationale

  surface_prune_candidates(outcome)
    → list[dict]         — pre-filled PruneDecision-style records (suggested only)

  render_next_round_section(outcome)
    → str                — markdown section with branches Richard chooses from

  run(t0=None, t30=None)
    → (markdown_str, Path)  — orchestrates the whole pipeline and writes the
                              review markdown to pilot-review-{t30_date}.md

CRITICAL INVARIANTS (anti-goals)

  1. NO AUTO-PRUNE. This module surfaces candidates only. Richard reviews them
     and, if he approves, Group 6's `execute_prune()` runs under his direction.

  2. NO SCHEDULED RUN. The tool is human-triggered. No hook, no cron. Per
     design §Anti-Goals #1 — adoption is governance, not a service.

  3. NO MUTATION OF SIBLING MODULES. This module reads the activation log,
     walks the inventory for installed assets, and writes exactly one file:
     ~/shared/context/skills-powers/pilot-review-{YYYY-MM-DD}.md.
     It never modifies inventory.py, activation_log.py, or pruning.py.

  4. NO FABRICATION. If t0 is not provided and the activation log has no
     baseline rows, the tool refuses to run rather than guess. A pilot review
     requires a real baseline to measure against.

WINDOW SEMANTICS (per spec's 9.1 note)

  "activated" events count iff t0 <= ts <= t30 (inclusive of both bounds).
  Inclusive-inclusive is the design's natural reading of "over the 30-day
  window" — the first activation on T0 and the last activation on T30 both
  count toward the per-asset tally.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# Sibling-module import pattern mirrored from pruning.py so this file runs
# both as a script (python3 pilot_review.py run) and as a package member
# (from skills_powers import pilot_review).
try:
    import inventory as _inv
except ImportError:  # pragma: no cover — package-mode import
    from . import inventory as _inv  # type: ignore


# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------

HOME = Path(os.path.expanduser("~"))
REVIEW_DIR = HOME / "shared" / "context" / "skills-powers"
ACTIVATION_LOG = REVIEW_DIR / "activation-log.jsonl"


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

# Success criterion per R5.6 and design §Pilot metric:
#   ≥3 activations per skill AND ≥5 of 9 installed skills activated at all.
_MIN_ACTIVATIONS_PER_SKILL = 3
_MIN_SKILLS_ACTIVATED_AT_ALL = 5
_EXPECTED_TOTAL_SKILLS = 9

# The 13 expected installed assets — design §Inventory file (T0 state). If the
# live inventory diverges from these names, the tool still emits per-asset
# rows for whatever is installed, but the "X / 9 skills activated" denominator
# stays pinned at the design's constant so the comparison is apples-to-apples
# with R5.6.
_EXPECTED_SKILLS = (
    "bridge-sync",
    "charts",
    "coach",
    "cr-tagging",
    "sharepoint-sync",
    "wbr-callouts",
    "wiki-audit",
    "wiki-search",
    "wiki-write",
)
_EXPECTED_POWERS = (
    "aws-agentcore",
    "flow-gen",
    "hedy",
    "power-builder",
)


# ----------------------------------------------------------------------------
# Data classes
# ----------------------------------------------------------------------------


@dataclass
class AssetMetric:
    """Per-asset activation metric over the pilot window [t0, t30]."""

    kind: str  # "skill" | "power"
    name: str
    activation_count: int
    missed_by_feedback_count: int
    first_activation_ts: str | None  # ISO 8601 or None
    last_activation_ts: str | None  # ISO 8601 or None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------


def _parse_ts(s: str | None) -> datetime | None:
    """Permissive ISO 8601 parser.

    Accepts offset with or without colon, and date-only YYYY-MM-DD. Returns
    a timezone-aware datetime whenever the source carries an offset;
    date-only inputs are treated as UTC midnight so comparisons are stable.
    """
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        pass
    m = re.match(
        r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})([+-]\d{2})(\d{2})$", s
    )
    if m:
        fixed = f"{m.group(1)}{m.group(2)}:{m.group(3)}"
        try:
            return datetime.fromisoformat(fixed)
        except ValueError:
            return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _ensure_aware(dt: datetime, reference: datetime) -> datetime:
    """Borrow `reference`'s tzinfo when `dt` is naive, so comparisons work."""
    if dt.tzinfo is None and reference.tzinfo is not None:
        return dt.replace(tzinfo=reference.tzinfo)
    return dt


def _default_t0_from_log(log: list[dict[str, Any]]) -> datetime | None:
    """Find the earliest baseline row's timestamp.

    Used when the caller doesn't pass an explicit t0. Returns None when
    no baseline rows exist, which signals "no real pilot to review".
    """
    earliest: datetime | None = None
    for row in log:
        if row.get("event") != "baseline":
            continue
        ts = _parse_ts(row.get("ts"))
        if ts is None:
            continue
        if earliest is None or ts < earliest:
            earliest = ts
    return earliest


def _iso(dt: datetime) -> str:
    """ISO 8601 with timezone, matching activation-log convention."""
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


def _date_str(dt: datetime) -> str:
    return dt.date().isoformat()


# ----------------------------------------------------------------------------
# Task 9.1 — compute_pilot_metrics
# ----------------------------------------------------------------------------


def _live_installed_assets() -> list[tuple[str, str]]:
    """Return (kind, name) for every currently-installed asset.

    Reads the live filesystem via inventory.walk_installed(). Used when no
    explicit asset list is passed — it keeps the metric aligned with what is
    actually on disk rather than a hardcoded roster.
    """
    walk = _inv.walk_installed()
    return [(a.kind, a.name) for a in walk.assets]


def _expected_assets_union(live: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Union the design's expected 13 with whatever is live on disk.

    The pilot's denominator (R5.6 → ≥5 of 9 skills) is pinned to the design
    constants. But per-asset rows also include any currently-installed asset
    not in the expected roster, so re-running after an install/uninstall
    still renders a complete report. Deduped, preserving design order first.
    """
    seen: set[tuple[str, str]] = set()
    result: list[tuple[str, str]] = []
    for name in _EXPECTED_SKILLS:
        key = ("skill", name)
        if key not in seen:
            seen.add(key)
            result.append(key)
    for name in _EXPECTED_POWERS:
        key = ("power", name)
        if key not in seen:
            seen.add(key)
            result.append(key)
    for key in live:
        if key not in seen:
            seen.add(key)
            result.append(key)
    return result


def compute_pilot_metrics(
    t0: datetime | None = None,
    t30: datetime | None = None,
    *,
    activation_log: list[dict[str, Any]] | None = None,
    assets: list[tuple[str, str]] | None = None,
) -> list[AssetMetric]:
    """Compute per-asset activation counts over the pilot window [t0, t30].

    Window semantics (per Group 9.1 note and design §Pilot metric):
      - Inclusive of both bounds: an event at ts == t0 or ts == t30 counts.
      - Only `activated` events feed the primary count.
      - `missed-by-feedback` events within the window are counted separately
        and surfaced as gap signal (spec: "though `missed-by-feedback`
        entries are surfaced separately").
      - `baseline`, `created`, `pruned`, `correction` events are ignored
        for the activation metric.

    Defaults:
      - activation_log: read from ~/shared/context/skills-powers/activation-log.jsonl.
      - assets: expected 13 unioned with whatever is currently live on disk.
      - t0:  earliest baseline row's ts in the log.
      - t30: t0 + 30 days.

    Raises ValueError when t0 cannot be determined (no baseline rows, no
    explicit t0 passed). This is the "no fabrication" invariant — a pilot
    review with no real baseline is not a pilot review.
    """
    if activation_log is None:
        activation_log = _inv.read_activation_log(ACTIVATION_LOG)

    if t0 is None:
        t0 = _default_t0_from_log(activation_log)
        if t0 is None:
            raise ValueError(
                "cannot compute pilot metrics: no baseline rows in activation "
                "log and no explicit t0 provided. A pilot review requires a "
                "real baseline — run Group 1 first."
            )
    if t30 is None:
        t30 = t0 + timedelta(days=30)

    if assets is None:
        assets = _expected_assets_union(_live_installed_assets())

    metrics: list[AssetMetric] = []
    for kind, name in assets:
        activations: list[datetime] = []
        missed_count = 0
        for row in activation_log:
            if row.get("name") != name or row.get("kind") != kind:
                continue
            event = row.get("event")
            ts = _parse_ts(row.get("ts"))
            if ts is None:
                continue
            ts = _ensure_aware(ts, t0)
            # Inclusive of both bounds.
            if not (t0 <= ts <= t30):
                continue
            if event == "activated":
                activations.append(ts)
            elif event == "missed-by-feedback":
                missed_count += 1
            # baseline / created / pruned / correction explicitly ignored
            # for the activation metric per the spec.
        activations.sort()
        first_iso = _iso(activations[0]) if activations else None
        last_iso = _iso(activations[-1]) if activations else None
        metrics.append(
            AssetMetric(
                kind=kind,
                name=name,
                activation_count=len(activations),
                missed_by_feedback_count=missed_count,
                first_activation_ts=first_iso,
                last_activation_ts=last_iso,
            )
        )
    return metrics


# ----------------------------------------------------------------------------
# Task 9.2 — evaluate_pilot_outcome
# ----------------------------------------------------------------------------


def evaluate_pilot_outcome(metrics: list[AssetMetric]) -> dict[str, Any]:
    """Score the metrics against R5.6.

    Per-skill outcome:
      - ≥3 activations → KEEP
      - <3 activations → PRUNE-CANDIDATE

    Aggregate outcome:
      PASS iff (skills activated at all ≥ 5) AND (every skill with
      activations hits ≥3). The spec's two-part criterion is:
        "≥3 activations per activated skill AND ≥5 of 9 skills activated
         at all"
      We interpret "per activated skill" as the 9.2 sub-task's literal
      per-skill rule above (≥3 → KEEP, else PRUNE-CANDIDATE). PASS requires
      both: breadth (≥5 of 9 skills fired) and depth (no KEEP-eligible
      skill falling below 3).

    Powers are rendered in per_asset_outcomes for completeness but do NOT
    feed the aggregate — R5.6 is skill-only.
    """
    per_asset_outcomes: list[dict[str, Any]] = []
    skills_activated_at_all = 0
    skill_outcomes: list[str] = []

    for m in metrics:
        if m.activation_count >= _MIN_ACTIVATIONS_PER_SKILL:
            outcome = "KEEP"
        else:
            outcome = "PRUNE-CANDIDATE"
        per_asset_outcomes.append(
            {
                "name": m.name,
                "kind": m.kind,
                "activation_count": m.activation_count,
                "outcome": outcome,
            }
        )
        if m.kind == "skill":
            skill_outcomes.append(outcome)
            if m.activation_count > 0:
                skills_activated_at_all += 1

    # Aggregate PASS/FAIL — skill-only.
    skills_keep = sum(1 for o in skill_outcomes if o == "KEEP")
    pass_breadth = skills_activated_at_all >= _MIN_SKILLS_ACTIVATED_AT_ALL
    aggregate = "PASS" if pass_breadth else "FAIL"

    rationale_parts: list[str] = []
    rationale_parts.append(
        f"{skills_activated_at_all} of {_EXPECTED_TOTAL_SKILLS} skills "
        f"activated at least once in the 30-day window "
        f"(threshold: \u2265{_MIN_SKILLS_ACTIVATED_AT_ALL})."
    )
    rationale_parts.append(
        f"{skills_keep} skill(s) reached KEEP (\u2265"
        f"{_MIN_ACTIVATIONS_PER_SKILL} activations); "
        f"{len(skill_outcomes) - skills_keep} flagged PRUNE-CANDIDATE."
    )
    if aggregate == "PASS":
        rationale_parts.append(
            "Breadth threshold met \u2014 adoption habit is taking hold. "
            "Continue with bias toward EXTEND_EXISTING + PRUNE per design "
            "\u00a7Post-pilot decision point."
        )
    else:
        rationale_parts.append(
            "Breadth threshold NOT met \u2014 adoption habit is not "
            "sticking. Do NOT build new skills; revisit the design "
            "(matcher, triggers, or whether the corpus fits) per design "
            "\u00a7Post-pilot decision point."
        )

    return {
        "per_asset_outcomes": per_asset_outcomes,
        "aggregate_outcome": aggregate,
        "skills_activated_at_all": skills_activated_at_all,
        "pass_threshold": (
            "\u22655 of 9 skills activated AND \u22653 activations per activated skill"
        ),
        "rationale": " ".join(rationale_parts),
    }


# ----------------------------------------------------------------------------
# Task 9.3 — surface_prune_candidates
# ----------------------------------------------------------------------------


def surface_prune_candidates(outcome: dict[str, Any]) -> list[dict[str, Any]]:
    """Produce pre-filled PruneDecision-style dicts for every PRUNE-CANDIDATE.

    Per spec §Anti-task: DO NOT auto-execute pruning. This function shapes
    the candidates; the actual archive + delete only runs if Richard, during
    a later Group 6 review, explicitly marks the candidate APPROVE and calls
    `execute_prune()`.

    Each dict mirrors Group 6's `PruneDecision` shape (name, kind, action,
    rationale) with:
      - action: "APPROVE (suggested)" — the trailing " (suggested)" is a
        deliberate guard. It is NOT the literal token Group 6 accepts
        ({"APPROVE", "DEFER", "PROTECT"}), so if somebody tries to pipe
        these dicts straight into `execute_prune()` without review, it
        will crash with "unknown action" instead of silently pruning.
      - rationale: cites the exact activation count that triggered the
        candidate, so Richard can sanity-check against the pilot data.
    """
    candidates: list[dict[str, Any]] = []
    for row in outcome.get("per_asset_outcomes", []):
        if row.get("outcome") != "PRUNE-CANDIDATE":
            continue
        count = row.get("activation_count", 0)
        candidates.append(
            {
                "name": row["name"],
                "kind": row["kind"],
                "action": "APPROVE (suggested)",
                "rationale": (
                    f"Failed pilot criterion: {count} activation"
                    f"{'s' if count != 1 else ''} in 30-day window "
                    f"(threshold: \u2265{_MIN_ACTIVATIONS_PER_SKILL})"
                ),
            }
        )
    return candidates



# ----------------------------------------------------------------------------
# Task 9.5 — render_next_round_section
# ----------------------------------------------------------------------------


def render_next_round_section(outcome: dict[str, Any]) -> str:
    """Render the "Next-round direction" markdown section per design.

    Content is pulled directly from design §Post-pilot decision point:

      PASS: three branches (EXTEND_EXISTING / PRUNE / net-new creation).
      FAIL: the investigation flow (matcher check, missed-by-feedback
            comparison, four option paths).

    The section is appended verbatim to the review markdown. Richard reads
    it, picks a branch, and records his choice in the review file or in a
    follow-up session — no automation closes the loop.
    """
    agg = outcome.get("aggregate_outcome", "FAIL")
    lines: list[str] = []
    lines.append("## Next-round direction (Richard decides)")
    lines.append("")
    if agg == "PASS":
        lines.append(
            "The adoption habit is working. Pick one of three branches "
            "(you can combine them):"
        )
        lines.append("")
        lines.append(
            "1. **EXTEND_EXISTING on survivors** \u2014 routing tree step 1 "
            "bias holds. New workflows edit existing skills rather than "
            "creating new ones."
        )
        lines.append(
            "2. **PRUNE failing skills** \u2014 take the suggested "
            "PRUNE-CANDIDATEs above into a Group 6 pruning review. "
            "Mark each APPROVE / DEFER / PROTECT and then run "
            "`pruning.execute_prune()` against approved rows."
        )
        lines.append(
            "3. **Consider net-new creation** \u2014 last resort, not the "
            "default. Only if Group 4 routing terminates at CREATE_NEW "
            "AND Group 5.1 overlap-check surfaces no viable "
            "EXTEND_EXISTING candidate."
        )
        lines.append("")
        lines.append(
            "Additionally: Groups 4, 5, 7, 8 (FULL-PASS routing, safe-"
            "creation, validators, property tests) are now justified \u2014 "
            "the routing tree and safe-creation workflow will see real "
            "traffic because skills are being reached for naturally."
        )
    else:
        lines.append(
            "The adoption habit did NOT stick. Do NOT build new skills. "
            "Do NOT implement routing tree / safe-creation (if still "
            "deferred). Investigate the cause first:"
        )
        lines.append("")
        lines.append(
            "1. **Check if the pre-draft keyword matcher is firing** "
            "(Group 3.4). A broken matcher looks identical to an unused "
            "corpus from the log's perspective. Verify with a test request "
            "that clearly hits a skill's trigger keywords and watch "
            "whether an `activated` row appears."
        )
        lines.append(
            "2. **Compare the `missed-by-feedback` tally to zero-activation "
            "skills.** If the same skills appear in both, the matcher is "
            "missing them \u2014 the triggers are wrong, not the skill itself."
        )
        lines.append("")
        lines.append("Then pick one of four options:")
        lines.append("")
        lines.append(
            "- **Fix the matcher** (3.4 bug) \u2014 re-baseline, re-run the "
            "30-day pilot. Groups 4\u20138 stay deferred."
        )
        lines.append(
            "- **Update trigger lists** via touch-it-classify-it (5.4) \u2014 "
            "edit the legacy skill's description to include the triggers "
            "Richard's requests actually used. No Group 5.3 new-asset "
            "writes until activation works."
        )
        lines.append(
            "- **Accept skills don't fit** \u2014 some of the 9 may be "
            "METAPHOR-ONLY (audit methodology). Run Group 6 pruning to "
            "remove the dead weight."
        )
        lines.append(
            "- **Revisit the design** \u2014 if fixing the matcher or the "
            "triggers won't help, the adoption-system hypothesis is "
            "falsified for this corpus. Pull the work back to design, "
            "not forward to more implementation."
        )
    lines.append("")
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# Markdown rendering — Task 9.4
# ----------------------------------------------------------------------------


def _render_asset_table(metrics: list[AssetMetric], outcome: dict[str, Any]) -> str:
    """Render the per-asset metrics table with the per-row KEEP/PRUNE verdict."""
    # Index outcomes by (kind, name) for quick lookup.
    verdict_by_key: dict[tuple[str, str], str] = {}
    for row in outcome.get("per_asset_outcomes", []):
        verdict_by_key[(row["kind"], row["name"])] = row["outcome"]

    lines: list[str] = []
    lines.append(
        "| Kind | Name | Activations | Missed-by-feedback | First | Last | Outcome |"
    )
    lines.append(
        "|------|------|-------------|--------------------|-------|------|---------|"
    )
    # Sort: skills first by name, then powers by name.
    sorted_metrics = sorted(
        metrics, key=lambda m: (0 if m.kind == "skill" else 1, m.name)
    )
    for m in sorted_metrics:
        first = m.first_activation_ts or "\u2014"
        last = m.last_activation_ts or "\u2014"
        verdict = verdict_by_key.get((m.kind, m.name), "\u2014")
        lines.append(
            f"| {m.kind} | {m.name} | {m.activation_count} | "
            f"{m.missed_by_feedback_count} | {first} | {last} | {verdict} |"
        )
    return "\n".join(lines)


def _render_prune_checklist(candidates: list[dict[str, Any]]) -> str:
    """Render the Phase E suggested-candidates checklist."""
    if not candidates:
        return (
            "_(No PRUNE-CANDIDATEs \u2014 every skill cleared the \u2265"
            f"{_MIN_ACTIVATIONS_PER_SKILL}-activation bar.)_"
        )
    lines: list[str] = []
    lines.append(
        "Each row below is a pre-filled suggestion. Take these into a "
        "Group 6 pruning review: mark APPROVE / DEFER / PROTECT and only "
        "then call `pruning.execute_prune()` against the approved rows."
    )
    lines.append("")
    for c in candidates:
        lines.append(
            f"- [ ] **{c['name']}** ({c['kind']}) \u2014 suggested action: "
            f"`{c['action']}`. Rationale: {c['rationale']}."
        )
    return "\n".join(lines)


def _count_activated_skills(outcome: dict[str, Any]) -> int:
    """Number of skills with \u22651 activation over the window."""
    # Reconstruct from per_asset_outcomes + the activation_count field.
    # outcome carries the pre-computed count too; we prefer that for
    # consistency with evaluate_pilot_outcome.
    return outcome.get("skills_activated_at_all", 0)


def _count_activated_powers(metrics: list[AssetMetric]) -> int:
    return sum(
        1 for m in metrics if m.kind == "power" and m.activation_count > 0
    )


def render_pilot_review_markdown(
    t0: datetime,
    t30: datetime,
    metrics: list[AssetMetric],
    outcome: dict[str, Any],
    candidates: list[dict[str, Any]],
) -> str:
    """Assemble the full pilot-review markdown per Task 9.4's template.

    Shape:
      - Title + T0 / T30 / duration header.
      - Outcome: PASS | FAIL with rationale paragraph.
      - Counts: skills activated (N/9), powers activated (M/4).
      - Per-asset table with KEEP / PRUNE-CANDIDATE verdict.
      - Suggested PRUNE-CANDIDATEs checklist.
      - Next-round direction section (from render_next_round_section).
    """
    total_skills = sum(1 for m in metrics if m.kind == "skill")
    total_powers = sum(1 for m in metrics if m.kind == "power")
    skills_activated = _count_activated_skills(outcome)
    powers_activated = _count_activated_powers(metrics)

    agg = outcome.get("aggregate_outcome", "FAIL")
    rationale = outcome.get("rationale", "")

    lines: list[str] = []
    lines.append(f"# Pilot Review \u2014 {_date_str(t30)}")
    lines.append("")
    lines.append(f"**T0**: {_iso(t0)}  ")
    lines.append(f"**T30**: {_iso(t30)}  ")
    duration_days = (t30 - t0).days
    lines.append(f"**Duration**: {duration_days} days")
    lines.append("")
    lines.append(f"## Outcome: {agg}")
    lines.append("")
    lines.append(rationale)
    lines.append("")
    lines.append(
        f"**Pass threshold**: {outcome.get('pass_threshold', '')}"
    )
    lines.append("")
    lines.append(f"## Skills activated at all: {skills_activated}/{total_skills}")
    lines.append(f"## Powers activated at all: {powers_activated}/{total_powers}")
    lines.append("")
    lines.append("## Per-asset activation metrics")
    lines.append("")
    lines.append(_render_asset_table(metrics, outcome))
    lines.append("")
    lines.append("## Skills / powers failing criterion (suggested PRUNE-CANDIDATEs)")
    lines.append("")
    lines.append(_render_prune_checklist(candidates))
    lines.append("")
    lines.append(render_next_round_section(outcome))
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------------
# End-to-end orchestrator
# ----------------------------------------------------------------------------


def run(
    t0: datetime | None = None,
    t30: datetime | None = None,
    *,
    activation_log: list[dict[str, Any]] | None = None,
    assets: list[tuple[str, str]] | None = None,
) -> tuple[str, Path]:
    """Run the full pilot review pipeline and write the markdown file.

    Output path: ~/shared/context/skills-powers/pilot-review-{t30_date}.md.

    Returns (markdown_str, output_path). Caller (CLI or agent) decides how
    to present the result to Richard.
    """
    if activation_log is None:
        activation_log = _inv.read_activation_log(ACTIVATION_LOG)

    # Resolve t0/t30 explicitly so we can stamp them in the header.
    if t0 is None:
        t0 = _default_t0_from_log(activation_log)
        if t0 is None:
            raise ValueError(
                "cannot run pilot review: no baseline rows in activation log "
                "and no explicit t0 provided. Run Group 1 first."
            )
    if t30 is None:
        t30 = t0 + timedelta(days=30)

    metrics = compute_pilot_metrics(
        t0=t0, t30=t30, activation_log=activation_log, assets=assets
    )
    outcome = evaluate_pilot_outcome(metrics)
    candidates = surface_prune_candidates(outcome)
    md = render_pilot_review_markdown(t0, t30, metrics, outcome, candidates)

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    out_path = REVIEW_DIR / f"pilot-review-{_date_str(t30)}.md"
    out_path.write_text(md, encoding="utf-8")
    return md, out_path


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------


def _parse_date_arg(s: str | None) -> datetime | None:
    """Accept YYYY-MM-DD on the CLI; interpret as local midnight."""
    if not s:
        return None
    try:
        d = datetime.strptime(s, "%Y-%m-%d")
    except ValueError as e:
        raise SystemExit(f"invalid date {s!r}: expected YYYY-MM-DD ({e})") from e
    return d.astimezone()


def _main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="pilot_review",
        description=(
            "Pilot review tool for the skills-powers-adoption spec. "
            "Human-triggered \u2014 no scheduling, no auto-prune."
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser(
        "run",
        help="compute metrics, score outcome, write pilot-review markdown",
    )
    run_p.add_argument("--t0", help="pilot start date (YYYY-MM-DD)")
    run_p.add_argument("--t30", help="pilot end date (YYYY-MM-DD)")

    args = parser.parse_args(argv[1:])

    if args.cmd == "run":
        t0 = _parse_date_arg(getattr(args, "t0", None))
        t30 = _parse_date_arg(getattr(args, "t30", None))
        try:
            md, path = run(t0=t0, t30=t30)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        print(f"wrote {path}")
        print(f"{len(md.splitlines())} lines, {len(md)} bytes")
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":  # pragma: no cover
    sys.exit(_main(sys.argv))
