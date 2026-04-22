"""
Pruning Review — Phase E of the skills-powers-adoption spec.

Implements the four-step pruning procedure (§Pruning Review):

  6.1  compute_stale_set()   — stale-set computation with never-prune-under-
                               use guarantee (Property 2). Excludes retired,
                               recently-created, and recently-activated
                               assets. Pure function over assets + log.

  6.2  render_pruning_review() — render a markdown review file Richard edits
                               interactively, one block per stale asset
                               with APPROVE / DEFER / PROTECT checkboxes.
                               Absence of decision = DEFER.

  6.3  execute_prune()       — archive-before-delete (Property 14). For
                               each APPROVE decision: atomic copytree to
                               the archive directory, verify archive
                               contents, ONLY THEN rmtree the source. If
                               archive/verify fails, delete does NOT run.
                               dry_run=True simulates without fs mutation.

  6.4  post_prune_update()   — append `pruned` events to activation-log.jsonl
                               and refresh inventory.md. Retired rows drop
                               from inventory on next Phase A refresh because
                               their source directory is gone — no special
                               retired-row handling needed.

DESIGN STANCE

    Human-triggered only. No cron, no scheduled runner, no hook. Trigger is
    Richard saying "run skills pruning review" (or equivalent). Per design
    §Pruning Review § Trigger and §Anti-Goals #1.

CRITICAL INVARIANTS

    1. Never-prune-under-use: any asset with ≥1 `activated` event in last 30
       days is NEVER in the stale set, regardless of any other factor.
       Enforced at set construction (Property 2), not at Richard-review time.

    2. Archive-before-delete: every pruned asset is archived to
       ~/shared/wiki/agent-created/archive/skills-powers-pruned-{YYYY-MM-DD}/
       {name}/ BEFORE its source is deleted. If archive fails, delete does
       NOT run. Property 14.

    3. Scoped writes: archival destination is strictly under
       ~/shared/wiki/agent-created/archive/skills-powers-pruned-{date}/.
       No writes outside that scope.

    4. Source mutation never happens during archival: we use shutil.copytree,
       not shutil.move. The source is deleted only after the archive is
       verified.
"""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# Sibling modules. Support both direct execution (absolute imports) and
# package-mode (relative imports) following the existing safe_creation pattern.
try:
    import inventory as _inv
    import activation_log as _log
except ImportError:  # pragma: no cover — package-mode import
    from . import inventory as _inv  # type: ignore
    from . import activation_log as _log  # type: ignore


# ----------------------------------------------------------------------------
# Paths — write-scope allowlist
# ----------------------------------------------------------------------------

HOME = Path(os.path.expanduser("~"))
SKILLS_ROOT = HOME / ".kiro" / "skills"
POWERS_ROOT = HOME / ".kiro" / "powers" / "installed"
ARCHIVE_ROOT = HOME / "shared" / "wiki" / "agent-created" / "archive"
REVIEW_DIR = HOME / "shared" / "context" / "skills-powers"


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

_DEFAULT_HORIZON_DAYS = 30
_DEFAULT_LEGACY_GRACE_DAYS = 30
_ACTIVATION_COUNT_WINDOW_DAYS = 90


# ----------------------------------------------------------------------------
# Data classes
# ----------------------------------------------------------------------------


@dataclass
class StaleCandidate:
    """One row surfaced to Richard for prune-review."""

    row_id: str  # "1", "2", ... — sequential after most-stale-first sort
    name: str
    kind: str  # "skill" | "power"
    status: str  # "legacy" | "current"  (retired is excluded upstream)
    days_since_last_activation: int | None  # None → never activated
    activation_count_last_90d: int
    creation_date_iso_or_unknown: str  # "YYYY-MM-DD" | "UNKNOWN"
    reason: str  # human-readable reason stale

    def to_dict(self) -> dict[str, Any]:
        return {
            "row_id": self.row_id,
            "name": self.name,
            "kind": self.kind,
            "status": self.status,
            "days_since_last_activation": self.days_since_last_activation,
            "activation_count_last_90d": self.activation_count_last_90d,
            "creation_date_iso_or_unknown": self.creation_date_iso_or_unknown,
            "reason": self.reason,
        }


@dataclass
class PruneDecision:
    """Richard's verdict on a single stale asset."""

    name: str
    kind: str  # "skill" | "power"
    action: str  # "APPROVE" | "DEFER" | "PROTECT"
    rationale: str = ""


@dataclass
class PruneResult:
    """Outcome of one execute_prune() iteration."""

    name: str
    kind: str
    action: str  # echo PruneDecision.action
    success: bool
    dry_run: bool = False
    archive_path: str | None = None  # HOME-relative on success
    note: str = ""
    reason: str | None = None  # failure reason if success=False

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "kind": self.kind,
            "action": self.action,
            "success": self.success,
            "dry_run": self.dry_run,
            "archive_path": self.archive_path,
            "note": self.note,
            "reason": self.reason,
        }


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------


def _now() -> datetime:
    """Return a timezone-aware `now` tied to the local offset."""
    return datetime.now().astimezone()


def _ensure_aware(dt: datetime, reference: datetime) -> datetime:
    """
    Coerce `dt` to be timezone-aware by borrowing `reference`'s tzinfo when
    needed. All comparisons in this module are done against a timezone-aware
    `now` so we can safely mix ISO 8601 rows (which carry offsets) with
    file mtime datetimes (which don't).
    """
    if dt.tzinfo is None and reference.tzinfo is not None:
        return dt.replace(tzinfo=reference.tzinfo)
    return dt


def _parse_ts(s: str | None) -> datetime | None:
    """Permissive ISO 8601 parser — delegates to inventory._parse_ts semantics.

    We duplicate the small helper here rather than import the private symbol
    so this module is self-contained. Same shape of inputs supported.
    """
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        pass
    # Offset without colon, e.g. "2026-04-22T09:08:53-0700"
    import re

    m = re.match(
        r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})([+-]\d{2})(\d{2})$", s
    )
    if m:
        fixed = f"{m.group(1)}{m.group(2)}:{m.group(3)}"
        try:
            return datetime.fromisoformat(fixed)
        except ValueError:
            return None
    # Date-only fallback.
    try:
        return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _asset_source_dir(name: str, kind: str) -> Path:
    """Return the live source directory for an asset — not the archive path."""
    if kind == "skill":
        return SKILLS_ROOT / name
    if kind == "power":
        return POWERS_ROOT / name
    raise ValueError(f"kind must be 'skill' or 'power', got {kind!r}")


def _asset_md_path(name: str, kind: str) -> Path:
    """Return the canonical md path for an asset."""
    src = _asset_source_dir(name, kind)
    return src / ("SKILL.md" if kind == "skill" else "POWER.md")


def _archive_dir_for(name: str, kind: str, now: datetime) -> Path:
    """Archive directory per design §Pruning Review step 4.

    ~/shared/wiki/agent-created/archive/skills-powers-pruned-{YYYY-MM-DD}/{name}/
    """
    date_str = now.strftime("%Y-%m-%d")
    parent = ARCHIVE_ROOT / f"skills-powers-pruned-{date_str}"
    return parent / name


def _home_relative(p: Path) -> str:
    """Render a Path as HOME-relative when possible, else absolute."""
    try:
        return f"~/{p.relative_to(HOME)}"
    except ValueError:
        return str(p)


# ----------------------------------------------------------------------------
# Task 6.1 — compute_stale_set (Property 2)
# ----------------------------------------------------------------------------


def _creation_dt_for(rec: _inv.AssetRecord, now: datetime) -> tuple[datetime | None, str]:
    """
    Derive an asset's creation datetime and its display form.

    For status=current: use frontmatter.created_at. "UNKNOWN" strings are
    treated as missing (no datetime, no creation-based filtering).

    For status=legacy (or missing status): use file mtime as the creation
    proxy. Design accepts this fallback per §Pilot procedure — legacy
    assets predate the `created_at` field's existence.

    Returns (datetime | None, display_string). Display is YYYY-MM-DD or
    "UNKNOWN".
    """
    status = rec.frontmatter.get("status", "legacy")
    if status == "current":
        raw = rec.frontmatter.get("created_at")
        if isinstance(raw, str) and raw and raw != "UNKNOWN":
            dt = _parse_ts(raw)
            if dt is not None:
                dt = _ensure_aware(dt, now)
                return dt, dt.date().isoformat()
            return None, "UNKNOWN"
        return None, "UNKNOWN"
    # legacy / retired / missing — use mtime
    try:
        mtime_dt = datetime.fromtimestamp(rec.mtime).astimezone()
        return mtime_dt, mtime_dt.date().isoformat()
    except (OSError, OverflowError, ValueError):
        return None, "UNKNOWN"


def _activation_stats(
    name: str,
    kind: str,
    activation_log: list[dict[str, Any]],
    now: datetime,
) -> tuple[datetime | None, int]:
    """
    Return (last_activated_dt, activation_count_last_90d).

    Only `activated` events count. `baseline`, `missed-by-feedback`,
    `created`, `pruned`, `correction` events are explicitly excluded
    per Group 6.1 spec and Property 2 semantics.
    """
    last_activated: datetime | None = None
    count_90d = 0
    window_start = now - timedelta(days=_ACTIVATION_COUNT_WINDOW_DAYS)

    for row in activation_log:
        if row.get("event") != "activated":
            continue
        if row.get("name") != name or row.get("kind") != kind:
            continue
        ts = _parse_ts(row.get("ts"))
        if ts is None:
            continue
        ts = _ensure_aware(ts, now)
        if last_activated is None or ts > last_activated:
            last_activated = ts
        if ts >= window_start:
            count_90d += 1
    return last_activated, count_90d


def compute_stale_set(
    assets: list[_inv.AssetRecord],
    activation_log: list[dict[str, Any]],
    *,
    now: datetime | None = None,
    horizon_days: int = _DEFAULT_HORIZON_DAYS,
    legacy_grace_days: int = _DEFAULT_LEGACY_GRACE_DAYS,
) -> list[StaleCandidate]:
    """
    Compute the stale set per design §Pruning Review procedure step 1 and
    Property 2 (STALENESS-CORRECTNESS).

    An asset is EXCLUDED from the stale set when any of:
      - status == "retired": already pruned.
      - Created within last `legacy_grace_days` (default 30): not enough
        measurement window yet. Strict inequality at the boundary:
        creation EXACTLY `legacy_grace_days` days ago is IN-window —
        i.e., NOT excluded (see "Boundary" note below).
      - Any `activated` event within last `horizon_days` (default 30):
        never-prune-under-use guarantee. Strict inequality: an activation
        exactly `horizon_days` days ago is OUT of window — i.e., does NOT
        save from staleness (see "Boundary" note below).

    Boundary convention: "within last N days" means `now - dt < timedelta(N)`.
    Equivalently, dt is in-window iff `dt > now - N days`. At exactly the
    boundary, dt is OUT of window.

    Stale-set members are returned as StaleCandidate records with:
      {name, kind, status, days_since_last_activation,
       activation_count_last_90d, creation_date_iso_or_unknown, row_id, reason}

    Sorted most-stale-first (longest gap at top). `row_id` is assigned
    sequentially after the sort for stable presentation. Assets never
    activated sort to the top (days_since = ∞ conceptually).
    """
    now = now.astimezone() if now is not None else _now()
    horizon_cutoff = now - timedelta(days=horizon_days)
    grace_cutoff = now - timedelta(days=legacy_grace_days)

    raw: list[StaleCandidate] = []

    for rec in assets:
        status = rec.frontmatter.get("status", "legacy")

        # Filter 1: retired assets are excluded.
        if status == "retired":
            continue
        # Only legacy and current can be in the stale set.
        if status not in ("legacy", "current"):
            # Unknown statuses are excluded conservatively (do not prune
            # something we don't understand).
            continue

        # Filter 2: recent creation → not enough measurement window.
        creation_dt, creation_display = _creation_dt_for(rec, now)
        if creation_dt is not None and creation_dt > grace_cutoff:
            continue

        # Filter 3: never-prune-under-use. Any activation in last
        # horizon_days excludes the asset from the stale set.
        last_activated, count_90d = _activation_stats(
            rec.name, rec.kind, activation_log, now
        )
        if last_activated is not None and last_activated > horizon_cutoff:
            continue

        # Reason classification per spec.
        if last_activated is None:
            # Never activated; asset exists at least legacy_grace_days old
            # (guaranteed by Filter 2 above for assets with known creation
            # dates; unknown-creation legacy assets fall through to this
            # branch too — we treat unknown as "has existed long enough").
            days_since: int | None = None
            reason = "never activated (created \u2265{}d ago)".format(legacy_grace_days)
        else:
            days_since = (now - last_activated).days
            if status == "legacy":
                reason = "stale + legacy candidate"
            else:
                reason = "no activation in {}d".format(horizon_days)

        raw.append(
            StaleCandidate(
                row_id="",  # assigned after sort
                name=rec.name,
                kind=rec.kind,
                status=status,
                days_since_last_activation=days_since,
                activation_count_last_90d=count_90d,
                creation_date_iso_or_unknown=creation_display,
                reason=reason,
            )
        )

    # Sort: most stale first. Never-activated sorts highest (infinite gap);
    # among activated, larger days_since sorts higher. Tie-break on kind
    # then name for determinism.
    def _sort_key(c: StaleCandidate) -> tuple:
        # Never-activated → (0, ...) sorts before (1, ...).
        # Within never-activated, order by kind then name.
        # Within activated, order by -days_since (largest first).
        if c.days_since_last_activation is None:
            return (0, c.kind, c.name)
        return (1, -c.days_since_last_activation, c.kind, c.name)

    raw.sort(key=_sort_key)

    # Assign sequential row ids after sort.
    for i, cand in enumerate(raw, start=1):
        cand.row_id = str(i)

    return raw


# ----------------------------------------------------------------------------
# Task 6.2 — render_pruning_review
# ----------------------------------------------------------------------------


def _days_since_display(n: int | None) -> str:
    if n is None:
        return "never activated"
    return f"{n}"


def render_pruning_review(
    stale: list[StaleCandidate],
    *,
    now: datetime | None = None,
) -> tuple[str, Path]:
    """
    Render the pruning review markdown for Richard to edit.

    Output shape per design §Pruning Review procedure step 2:
      - Header: title + timestamp + total-stale-count summary.
      - One block per stale asset with APPROVE / DEFER / PROTECT checkboxes
        and a rationale line. Blocks are already sorted most-stale-first by
        compute_stale_set().
      - Footer with syntax hint: absence of decision = DEFER.

    Writes to:
      ~/shared/context/skills-powers/pruning-review-{YYYY-MM-DD}.md

    Returns (rendered_markdown, path_written).
    """
    now = now.astimezone() if now is not None else _now()
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    out_path = REVIEW_DIR / f"pruning-review-{now.strftime('%Y-%m-%d')}.md"

    lines: list[str] = []
    lines.append("# Pruning Review \u2014 skills-powers-adoption")
    lines.append("")
    lines.append(f"**Generated**: {now.strftime('%Y-%m-%dT%H:%M:%S%z')}")
    lines.append(f"**Stale candidates**: {len(stale)}")
    lines.append("")

    if not stale:
        lines.append(
            "(No stale assets. All installed skills/powers have been "
            "activated within the last 30 days, were created within the "
            "grace window, or are already retired.)"
        )
        lines.append("")
    else:
        lines.append(
            "Sort order is most-stale-first. Fill in the action checkbox "
            "for each asset you reviewed."
        )
        lines.append("")
        for cand in stale:
            lines.append(
                f"### {cand.row_id}. {cand.name} ({cand.kind}, {cand.status})"
            )
            lines.append(
                f"- Days since last activation: "
                f"{_days_since_display(cand.days_since_last_activation)}"
            )
            lines.append(
                f"- Activations in last 90d: {cand.activation_count_last_90d}"
            )
            lines.append(
                f"- Creation date: {cand.creation_date_iso_or_unknown}"
            )
            lines.append(f"- Reason stale: {cand.reason}")
            lines.append(
                "- Action: [ ] APPROVE / [ ] DEFER / [ ] PROTECT"
            )
            lines.append(
                "- Rationale (required for DEFER/PROTECT, optional for "
                "APPROVE): _____________"
            )
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Syntax")
    lines.append("")
    lines.append(
        "- Fill in the action checkbox for each asset you reviewed."
    )
    lines.append(
        "- Absence of decision = DEFER (keep until next cycle)."
    )
    lines.append("- APPROVE means prune. PROTECT means never prune (permanent carveout).")
    lines.append(
        "- DEFER and PROTECT require a rationale; APPROVE rationale is optional."
    )
    lines.append("")

    md = "\n".join(lines) + "\n"
    out_path.write_text(md, encoding="utf-8")
    return md, out_path


# ----------------------------------------------------------------------------
# Task 6.3 — execute_prune (Property 14 — archive-before-delete)
# ----------------------------------------------------------------------------


def _verify_archive(archive_dir: Path, kind: str, src_had_overlap: bool) -> tuple[bool, str]:
    """
    Verify the archive directory contains the expected files.

    Requires the canonical md file (SKILL.md / POWER.md) to be present.
    If the source had overlap-check.json, it must also be present in the
    archive.
    """
    if not archive_dir.is_dir():
        return False, f"archive dir missing after copytree: {archive_dir}"
    expected_md = "SKILL.md" if kind == "skill" else "POWER.md"
    md_path = archive_dir / expected_md
    if not md_path.is_file():
        return False, f"archive missing {expected_md}"
    if src_had_overlap:
        oc = archive_dir / "overlap-check.json"
        if not oc.is_file():
            return False, "archive missing overlap-check.json (was present in source)"
    return True, "verified"


def _execute_one(decision: PruneDecision, *, dry_run: bool, now: datetime) -> PruneResult:
    """Execute one decision. APPROVE → archive + delete; DEFER/PROTECT → no-op."""
    action = decision.action
    if action not in ("APPROVE", "DEFER", "PROTECT"):
        return PruneResult(
            name=decision.name,
            kind=decision.kind,
            action=action,
            success=False,
            dry_run=dry_run,
            reason=f"unknown action: {action!r}",
        )

    if action in ("DEFER", "PROTECT"):
        return PruneResult(
            name=decision.name,
            kind=decision.kind,
            action=action,
            success=True,
            dry_run=dry_run,
            note="no file operations",
        )

    # APPROVE path.
    try:
        src = _asset_source_dir(decision.name, decision.kind)
    except ValueError as e:
        return PruneResult(
            name=decision.name,
            kind=decision.kind,
            action=action,
            success=False,
            dry_run=dry_run,
            reason=str(e),
        )

    archive_dir = _archive_dir_for(decision.name, decision.kind, now)
    archive_dir_display = _home_relative(archive_dir)

    if not src.exists():
        return PruneResult(
            name=decision.name,
            kind=decision.kind,
            action=action,
            success=False,
            dry_run=dry_run,
            reason=f"source directory not found: {_home_relative(src)}",
        )

    src_had_overlap = (src / "overlap-check.json").is_file()

    if dry_run:
        # Simulate — do not touch the filesystem.
        return PruneResult(
            name=decision.name,
            kind=decision.kind,
            action=action,
            success=True,
            dry_run=True,
            archive_path=archive_dir_display,
            note="dry run: no filesystem mutation",
        )

    # Real execution.
    # Ensure the archive parent exists. copytree will create archive_dir itself
    # and will fail if archive_dir already exists (loud failure on collision).
    archive_dir.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copytree(src, archive_dir)
    except Exception as e:  # FileExistsError, OSError, PermissionError, etc.
        return PruneResult(
            name=decision.name,
            kind=decision.kind,
            action=action,
            success=False,
            dry_run=False,
            reason=f"archive failed; source preserved: {e}",
        )

    # Verify archive before deleting source.
    verified, verify_msg = _verify_archive(
        archive_dir, decision.kind, src_had_overlap
    )
    if not verified:
        return PruneResult(
            name=decision.name,
            kind=decision.kind,
            action=action,
            success=False,
            dry_run=False,
            reason=f"archive verify failed; source preserved: {verify_msg}",
        )

    # Only now delete the source.
    try:
        shutil.rmtree(src)
    except Exception as e:
        # Archive succeeded but delete failed. We report failure; the source
        # still exists, the archive also exists. The caller can retry delete.
        return PruneResult(
            name=decision.name,
            kind=decision.kind,
            action=action,
            success=False,
            dry_run=False,
            archive_path=archive_dir_display,
            reason=f"source delete failed after archive: {e}",
        )

    return PruneResult(
        name=decision.name,
        kind=decision.kind,
        action=action,
        success=True,
        dry_run=False,
        archive_path=archive_dir_display,
        note="archived and deleted",
    )


def execute_prune(
    decisions: list[PruneDecision],
    *,
    dry_run: bool = False,
    now: datetime | None = None,
) -> list[PruneResult]:
    """
    Execute Richard's prune decisions per design §Pruning Review step 4.

    For each APPROVE decision:
      1. Resolve source dir (~/.kiro/skills/{name}/ or
         ~/.kiro/powers/installed/{name}/).
      2. Compute archive dir
         (~/shared/wiki/agent-created/archive/skills-powers-pruned-{date}/{n}/).
      3. Atomic copy via shutil.copytree (fails loudly if destination exists).
      4. Verify archive: SKILL.md/POWER.md + (if source had it) overlap-check.json
         exist at destination.
      5. ONLY THEN rmtree the source.

    If archive or verify fails → delete does NOT run; PruneResult.success=False
    and the source directory is preserved.

    DEFER and PROTECT actions: no-op, success=True, note="no file operations".

    dry_run=True simulates all steps without any filesystem mutation. Used by
    property tests to exercise the control flow without touching disk.
    """
    now = now.astimezone() if now is not None else _now()
    return [_execute_one(d, dry_run=dry_run, now=now) for d in decisions]


# ----------------------------------------------------------------------------
# Task 6.4 — post_prune_update
# ----------------------------------------------------------------------------


def post_prune_update(
    results: list[PruneResult],
    *,
    session_id: str | None = None,
) -> None:
    """
    Finalize Phase E: log `pruned` events for every successful APPROVE
    result and refresh inventory.md.

    Per design §Pruning Review step 4:
      - Append `pruned` event row per design §Data Model shape.
      - Re-render inventory.md. Retired rows drop from inventory on the
        next Phase A refresh BECAUSE the source file is gone — once rmtree
        has removed ~/.kiro/skills/{name}/, the walker simply no longer
        enumerates that name. No special "retired-row survives one cycle"
        logic is needed in the inventory module; absence from the live
        filesystem is the drop signal.

    dry-run PruneResults are skipped (they did not mutate the log or the
    filesystem, so neither should this call). DEFER and PROTECT results
    are also skipped — they are "no file operations" by design.

    Args:
        results: output of execute_prune(...).
        session_id: optional label propagated to the log append; defaults to
            sess-YYYY-MM-DD-HHMMSS via activation_log's helper.
    """
    any_pruned = False
    for r in results:
        if r.dry_run:
            continue
        if r.action != "APPROVE":
            continue
        if not r.success:
            continue
        if r.archive_path is None:
            # Defensive: successful APPROVE without a path shouldn't happen.
            continue
        _log.append_pruned_event(
            kind=r.kind,  # type: ignore[arg-type]
            name=r.name,
            archive_path=r.archive_path,
            session_id=session_id,
        )
        any_pruned = True

    # Refresh inventory regardless of whether any rows changed — a stale
    # inventory for a minute is worse than a free re-render.
    _inv.refresh()

    _ = any_pruned  # reserved for future return-value wiring if needed.


# ----------------------------------------------------------------------------
# End-to-end convenience wrapper (human-triggered)
# ----------------------------------------------------------------------------


def generate_review() -> tuple[list[StaleCandidate], str, Path]:
    """
    Convenience: walk the live filesystem, read the live activation log,
    compute the stale set, and render the review markdown.

    The agent calls this when Richard says "run skills pruning review".
    The agent then displays `review_md` to Richard and, after Richard edits
    the checkboxes, parses the decisions and calls `execute_prune()` +
    `post_prune_update()`.

    Returns (stale_candidates, rendered_markdown, review_md_path).
    """
    walk = _inv.walk_installed()
    log = _inv.read_activation_log()
    stale = compute_stale_set(walk.assets, log)
    md, path = render_pruning_review(stale)
    return stale, md, path


# ----------------------------------------------------------------------------
# Module-level self-description
# ----------------------------------------------------------------------------


if __name__ == "__main__":  # pragma: no cover
    print("pruning module \u2014 Phase E of skills-powers-adoption")
    print("  compute_stale_set(assets, activation_log, *, now=None,")
    print("                    horizon_days=30, legacy_grace_days=30)")
    print("  render_pruning_review(stale, *, now=None)")
    print("  execute_prune(decisions, *, dry_run=False, now=None)")
    print("  post_prune_update(results, *, session_id=None)")
    print("  generate_review()  \u2014 live-FS + log convenience wrapper")
    print(f"  ARCHIVE_ROOT = {ARCHIVE_ROOT}")
    print(f"  REVIEW_DIR   = {REVIEW_DIR}")
