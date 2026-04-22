"""
Safe-Creation Workflow — Phase C of the skills-powers-adoption spec.

Implements the five-step safe-creation procedure (§Safe-Creation Workflow):

  C.1  overlap_check()                  — search 6 Kiro kinds + non-Kiro
                                          mechanisms for prior art. NEW-ASSET
                                          only; legacy reclassification skips.
  C.2  richard_review_gate()            — MANDATORY interactive gate. No
                                          auto-approval. Callback-driven so the
                                          library stays pure; agent session or
                                          CLI supplies the review UI.
  C.3  write_new_asset()                — write new SKILL.md / POWER.md with
                                          status=current + overlap-check.json
                                          evidence file. Atomic, no overwrite.
       classify_legacy_then_write()     — legacy-migration path (touch-it-
                                          classify-it). Classification is OPT
                                          via callback; refusal keeps status
                                          legacy.
  C.4  activation_validate()            — SYNTACTIC validation only. The
                                          library parses, validates schema,
                                          confirms canonical path. Tool-level
                                          activation (discloseContext /
                                          kiroPowers activate) is the AGENT's
                                          responsibility — those tools are
                                          unavailable in library code.
  C.5  post_creation_update()           — append `created` event row to
                                          activation-log.jsonl (subtype
                                          `created` or `classified`) and
                                          refresh inventory.md.

DESIGN STANCE

    This module is a LIBRARY. It does not run as a service. It does not call
    agent tools. It exposes pure-ish functions that Phase C sessions (agent
    or CLI) stitch together around an interactive review callback.

CRITICAL INVARIANTS

    1. Richard-review gate is MANDATORY. `richard_review_gate()` REQUIRES a
       `review_callback` argument; there is no default-approve path. The
       included `console_review()` helper prompts stdin and never auto-
       approves.

    2. Activation-validate is SYNTACTIC ONLY. The library verifies everything
       it can verify without agent tools: parse, schema, canonical path, and
       (for powers) mcp.json JSON validity. Full tool-level activation is the
       agent's responsibility and runs outside this module.

    3. Legacy-migration does NOT require an overlap check. Per design
       §Phase C.1, a retrospective overlap-check has no decision to document.
       `overlap_check()` raises ValueError if called on a legacy path.

    4. Atomic writes only. `classify_legacy_then_write()` writes to `{path}.tmp`
       then renames. No file is ever left half-written.

    5. No overwrite of existing assets. `write_new_asset()` raises
       FileExistsError on an existing target — accidental overwrite of an
       activated skill is a kill-list-grade failure.

    6. Write scope is strictly enforced:
         ~/.kiro/skills/{name}/         (for new skills)
         ~/.kiro/powers/installed/{n}/  (for new powers)
         ~/shared/context/skills-powers/activation-log.jsonl (log append)
         ~/shared/context/skills-powers/inventory.md         (inventory render)
       No other paths are written.
"""

from __future__ import annotations

import json
import os
import re
import string
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

# Sibling modules. When the repo is invoked as a package these would be
# relative imports; when run directly from the skills-powers/ directory the
# absolute imports work. Try both.
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
SUBAGENTS_ROOT = HOME / ".kiro" / "agents"
HOOKS_ROOT = HOME / ".kiro" / "hooks"
STEERING_ROOT = HOME / ".kiro" / "steering"
ORGANS_ROOT = HOME / "shared" / "context" / "body"

# Default non-Kiro mechanisms considered in the overlap-check record. Caller
# may override by passing non_kiro_mechanisms_considered explicitly.
DEFAULT_NON_KIRO_MECHANISMS: tuple[str, ...] = (
    ".bashrc",
    "cron",
    "git hooks",
    "IDE features",
    "team tools",
)

# Routing-decision terminal leaves that AUTHORIZE Phase C. Per Property 9
# (ROUTING-PRECEDES-CREATE), REJECT and EXTEND_EXISTING are explicitly
# excluded — Phase C must not run for those leaves.
_CREATE_VARIANT_LEAVES = frozenset(
    {"SKILL", "POWER", "STEERING", "HOOK", "SUBAGENT", "ORGAN"}
)
_NON_CREATE_LEAVES = frozenset({"REJECT", "EXTEND_EXISTING"})

# Overlap threshold: ≥0.75 triggers EXTEND_EXISTING per design §Routing
# Decision Tree step 1. Matches routing.py's threshold.
_EXTEND_EXISTING_THRESHOLD = 0.75


# ----------------------------------------------------------------------------
# Tokenization (mirrors matcher.py)
# ----------------------------------------------------------------------------

_PUNCT_STRIP = str.maketrans(
    "", "", string.punctuation.replace("-", "").replace("_", "")
)


def _normalize(s: str) -> str:
    s = s.lower().translate(_PUNCT_STRIP)
    return re.sub(r"\s+", " ", s).strip()


def _tokenize(s: str) -> set[str]:
    s = _normalize(s)
    if not s:
        return set()
    return set(s.split(" "))


def _now_ts() -> str:
    """Match activation_log's ISO 8601 with tz-offset-no-colon format."""
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")


# ----------------------------------------------------------------------------
# Task 5.1 — overlap_check (Phase C.1)
# ----------------------------------------------------------------------------


def _read_purpose_line(path: Path) -> str:
    """
    Extract a purpose-line from an existing asset file.

    First non-empty line of the markdown body that starts with '#' → strip the
    leading hashes and return. Otherwise return the first non-empty paragraph
    after the frontmatter fence.

    Returns empty string on read failure (caller must tolerate).
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    # Strip YAML frontmatter if present.
    if text.startswith("---\n"):
        idx = text.find("\n---\n", 4)
        if idx != -1:
            text = text[idx + 5 :]
        else:
            idx = text.find("\n---", 4)
            if idx != -1:
                text = text[idx + 4 :]
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            return line.lstrip("#").strip()
        return line
    return ""


def _read_keyword_like(path: Path) -> list[str]:
    """
    Read asset-specific keyword hints.

    For SKILL.md / POWER.md we pull trigger phrases from the frontmatter via
    inventory.parse_frontmatter. For any other file kind we return [] — the
    overlap-check falls back to purpose-line tokens for those kinds.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    parsed = _inv.parse_frontmatter(text)
    if not isinstance(parsed, _inv.ParseSuccess):
        return []
    fm = parsed.frontmatter
    phrases: list[str] = []
    # Skills: description ends with "Triggers on {kw}, {kw}, ..."
    desc = fm.get("description") or ""
    m = re.search(r"[Tt]riggers on\s+(.+?)\.?$", desc.strip())
    if m:
        phrases.extend(p.strip() for p in m.group(1).split(",") if p.strip())
    # Powers: keywords array
    kw = fm.get("keywords")
    if isinstance(kw, list):
        phrases.extend(str(k).strip() for k in kw if str(k).strip())
    return phrases


def _enumerate_kiro_assets() -> dict[str, list[dict[str, Any]]]:
    """
    Walk the six Kiro mechanism sources. Each entry:
        {"name": str, "path": Path, "purpose": str, "keywords": [str, ...]}
    """

    def _collect_dir_with_child(root: Path, child_name: str) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        if not root.is_dir():
            return out
        for entry in sorted(root.iterdir()):
            if not entry.is_dir():
                continue
            target = entry / child_name
            if target.is_file():
                out.append(
                    {
                        "name": entry.name,
                        "path": target,
                        "purpose": _read_purpose_line(target),
                        "keywords": _read_keyword_like(target),
                    }
                )
        return out

    def _collect_flat_dir(
        root: Path, suffix: str | None = None
    ) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        if not root.is_dir():
            return out
        for entry in sorted(root.iterdir()):
            if not entry.is_file():
                continue
            if suffix is not None and not entry.name.endswith(suffix):
                continue
            out.append(
                {
                    "name": entry.stem,
                    "path": entry,
                    "purpose": _read_purpose_line(entry),
                    "keywords": [],
                }
            )
        return out

    return {
        "skills": _collect_dir_with_child(SKILLS_ROOT, "SKILL.md"),
        "powers": _collect_dir_with_child(POWERS_ROOT, "POWER.md"),
        "subagents": _collect_flat_dir(SUBAGENTS_ROOT, ".json"),
        "hooks": _collect_flat_dir(HOOKS_ROOT, ".kiro.hook"),
        "steering": _collect_flat_dir(STEERING_ROOT, ".md"),
        "organs": _collect_flat_dir(ORGANS_ROOT, ".md"),
    }


def _overlap_score(
    proposed_tokens: set[str], candidate_tokens: set[str]
) -> float:
    """Overlap-ratio: |intersection| / |candidate_tokens|. Returns 0 if empty."""
    if not candidate_tokens:
        return 0.0
    return len(proposed_tokens & candidate_tokens) / len(candidate_tokens)


def overlap_check(
    proposed: dict[str, Any],
    routing_decision: dict[str, Any],
    *,
    non_kiro_mechanisms_considered: list[str] | None = None,
) -> dict[str, Any]:
    """
    Phase C.1 overlap-check. Produces the `overlap-check.json` evidence record
    per design §Data Model → Overlap-check evidence record.

    Args:
        proposed: dict with `kind` ("skill"|"power"|"steering"|"hook"|
            "subagent"|"organ"), `name`, and `description`.
        routing_decision: the Phase B routing-decision record. MUST have a
            CREATE-variant `terminal_leaf`; REJECT and EXTEND_EXISTING raise
            ValueError per Property 9. Also used to detect legacy path.
        non_kiro_mechanisms_considered: optional list of external-mechanism
            strings to record as considered. Defaults to the library's
            canonical list (`.bashrc`, cron, git hooks, IDE features, team
            tools).

    Returns the full record as a dict. Does NOT write the record to disk —
    that happens in `write_new_asset()` so the record's `reviewed_by_richard`
    bit can be flipped by Phase C.2 first.

    Raises:
        ValueError if called on a legacy-reclassification path (per design
            §Phase C.1: retrospective overlap-check has no decision to
            document).
        ValueError if the routing_decision's terminal_leaf is REJECT or
            EXTEND_EXISTING (per Property 9).
    """
    # Legacy-migration guard. Caller signals legacy path either by setting
    # proposed["is_legacy_migration"] = True or by passing a routing_decision
    # that explicitly flags legacy. Either way we refuse.
    if proposed.get("is_legacy_migration"):
        raise ValueError(
            "overlap_check is not valid for legacy-migration paths; "
            "retrospective overlap-check has no decision to document "
            "(design §Phase C.1)"
        )
    if routing_decision.get("is_legacy_migration"):
        raise ValueError(
            "overlap_check is not valid for legacy-migration paths; "
            "retrospective overlap-check has no decision to document "
            "(design §Phase C.1)"
        )

    # Routing-precedes-create guard (Property 9).
    leaf = routing_decision.get("terminal_leaf")
    if leaf in _NON_CREATE_LEAVES:
        raise ValueError(
            f"overlap_check refuses: routing_decision.terminal_leaf "
            f"is {leaf!r}; Phase C may not run for REJECT or "
            f"EXTEND_EXISTING leaves (design §Property 9)"
        )
    if leaf is not None and leaf not in _CREATE_VARIANT_LEAVES:
        raise ValueError(
            f"overlap_check refuses: unknown terminal_leaf {leaf!r}; "
            f"expected one of {sorted(_CREATE_VARIANT_LEAVES)}"
        )

    # Shape validation on `proposed`.
    for field in ("kind", "name", "description"):
        if field not in proposed:
            raise ValueError(f"proposed missing required field: {field}")

    non_kiro = list(
        non_kiro_mechanisms_considered
        if non_kiro_mechanisms_considered is not None
        else DEFAULT_NON_KIRO_MECHANISMS
    )

    kiro = _enumerate_kiro_assets()
    proposed_tokens = _tokenize(str(proposed["description"]))

    candidates: list[dict[str, Any]] = []
    top_score = 0.0
    for kind_plural, assets in kiro.items():
        for a in assets:
            # Build candidate tokens from its purpose-line + keywords.
            tok_src = " ".join([a["purpose"], *a["keywords"]]).strip()
            cand_tokens = _tokenize(tok_src)
            score = _overlap_score(proposed_tokens, cand_tokens)
            if score <= 0.0:
                continue
            try:
                asset_path_repr = f"~/{a['path'].relative_to(HOME)}"
            except ValueError:
                asset_path_repr = str(a["path"])
            candidates.append(
                {
                    "asset_path": asset_path_repr,
                    "kind": kind_plural[:-1],  # strip pluralizing 's'
                    "name": a["name"],
                    "overlap_type": "functional",
                    "overlap_score": round(score, 4),
                    "rationale": (
                        f"token overlap with candidate purpose/keywords: "
                        f"score {score:.2f}"
                    ),
                }
            )
            if score > top_score:
                top_score = score

    candidates.sort(key=lambda c: (-c["overlap_score"], c["asset_path"]))

    if top_score >= _EXTEND_EXISTING_THRESHOLD:
        decision = "EXTEND_EXISTING"
        decision_rationale = (
            f"Top overlap candidate scored {top_score:.2f} (≥ "
            f"{_EXTEND_EXISTING_THRESHOLD}); edit the existing asset rather "
            f"than create a new one (design §Routing Decision Tree step 1)."
        )
    else:
        decision = "CREATE_NEW"
        decision_rationale = (
            f"No existing asset scored ≥ {_EXTEND_EXISTING_THRESHOLD} "
            f"overlap (max {top_score:.2f}); safe-creation proceeds."
        )

    # `searched_mechanisms` must enumerate all 6 Kiro kinds + non-Kiro list,
    # per design §Data Model → Overlap-check evidence record and Property 8.
    searched = {
        "skills": [a["name"] for a in kiro["skills"]],
        "powers": [a["name"] for a in kiro["powers"]],
        "subagents": [a["name"] for a in kiro["subagents"]],
        "hooks": [a["name"] for a in kiro["hooks"]],
        "steering": [a["name"] for a in kiro["steering"]],
        "organs": [a["name"] for a in kiro["organs"]],
        "non_kiro_mechanisms_considered": non_kiro,
    }

    record: dict[str, Any] = {
        "created_at": _now_ts(),
        "proposed_asset": {
            "kind": proposed["kind"],
            "name": proposed["name"],
            "description": proposed["description"],
        },
        "searched_mechanisms": searched,
        "overlap_candidates": candidates,
        "decision": decision,
        "decision_rationale": decision_rationale,
        "alternatives_considered": proposed.get("alternatives_considered", []),
        "reviewed_by_richard": False,
        "reviewed_at": None,
    }
    return record



# ----------------------------------------------------------------------------
# Task 5.2 — richard_review_gate (Phase C.2)
# ----------------------------------------------------------------------------


def console_review(summary: dict[str, Any]) -> dict[str, Any]:
    """
    Default stdin-based review callback for CLI / ad-hoc sessions.

    Prints the review summary to stdout, reads a yes/no response from stdin,
    and returns an approval record. **NEVER auto-approves** — a missing answer
    or an unrecognized response counts as rejection. Per design §Phase C.2:
    "Absence of veto is not approval."

    Caller supplies this to `richard_review_gate(review_callback=...)` when
    they want a stdin-driven interactive review. For agent sessions, the
    caller should supply their own callback that surfaces the summary via
    the agent's interactive-input channel.
    """
    print("=" * 72, file=sys.stderr)
    print("Phase C.2 — Richard review gate", file=sys.stderr)
    print("=" * 72, file=sys.stderr)
    print(json.dumps(summary, indent=2, ensure_ascii=False), file=sys.stderr)
    print("-" * 72, file=sys.stderr)
    print("Approve this proposal? [yes/no] ", end="", file=sys.stderr, flush=True)
    try:
        answer = input().strip().lower()
    except EOFError:
        answer = ""
    approved = answer in ("yes", "y")
    return {
        "approved": approved,
        "reviewed_at": _now_ts(),
        "edits": None,
    }


def richard_review_gate(
    proposal: dict[str, Any],
    overlap_result: dict[str, Any],
    portability_report: dict[str, Any],
    sensitivity_check: dict[str, Any],
    review_callback: Callable[[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    """
    Phase C.2 interactive gate. MANDATORY — no default-approve path.

    Args:
        proposal: the draft asset {kind, name, frontmatter, body}.
        overlap_result: the dict returned by `overlap_check()`.
        portability_report: advisory report from the portability validator
            (report-only per design §Portability Tier Rules). Caller may pass
            {} if not yet implemented — the gate surfaces it verbatim.
        sensitivity_check: enforced path-allowlist check result from the
            sensitivity validator. MUST contain a `valid` boolean; rejection
            on `valid == False` is handled here before the review.
        review_callback: mandatory callable. Takes a summary dict, returns
            `{approved: bool, reviewed_at: str, edits: dict|None}`.

    Returns a record:
        {
          "approved": bool,
          "reviewed_at": str,
          "edits": dict|None,           # if caller requested edits
          "overlap_result": dict,       # mutated in-place on approval:
                                        # reviewed_by_richard=True, reviewed_at
          "rejection_reason": str|None, # set if approved=False
        }
    """
    if review_callback is None:
        raise ValueError(
            "review_callback is MANDATORY; Phase C.2 has no default-approve "
            "path (design §Phase C.2: absence of veto is not approval)"
        )

    # Hard-stop on an enforced sensitivity failure BEFORE surfacing for review.
    # Sensitivity is the enforced validator per design §Phase C.2.
    if sensitivity_check.get("valid") is False:
        return {
            "approved": False,
            "reviewed_at": _now_ts(),
            "edits": None,
            "overlap_result": overlap_result,
            "rejection_reason": (
                f"sensitivity validator blocked proposal: "
                f"{sensitivity_check.get('violations', [])}"
            ),
        }

    summary = {
        "proposal": proposal,
        "overlap_summary": {
            "decision": overlap_result.get("decision"),
            "decision_rationale": overlap_result.get("decision_rationale"),
            "top_candidates": overlap_result.get("overlap_candidates", [])[:5],
        },
        "declared_metadata": {
            "sensitive_data_class": proposal.get("frontmatter", {}).get(
                "sensitive_data_class"
            ),
            "portability_tier": proposal.get("frontmatter", {}).get(
                "portability_tier"
            ),
            "platform_bound_dependencies": proposal.get("frontmatter", {}).get(
                "platform_bound_dependencies"
            ),
        },
        "portability_report": portability_report,
        "sensitivity_check": sensitivity_check,
    }

    decision = review_callback(summary)
    if not isinstance(decision, dict):
        raise TypeError(
            f"review_callback must return a dict, got {type(decision).__name__}"
        )
    approved = bool(decision.get("approved", False))
    reviewed_at = decision.get("reviewed_at") or _now_ts()
    edits = decision.get("edits")

    if approved:
        overlap_result["reviewed_by_richard"] = True
        overlap_result["reviewed_at"] = reviewed_at

    return {
        "approved": approved,
        "reviewed_at": reviewed_at,
        "edits": edits,
        "overlap_result": overlap_result,
        "rejection_reason": None if approved else "richard rejected",
    }


# ----------------------------------------------------------------------------
# Task 5.3 — write_new_asset (Phase C.3 new-asset path)
# ----------------------------------------------------------------------------


def _target_dir_for(kind: str, name: str) -> tuple[Path, Path]:
    """
    Resolve (asset_dir, canonical_md_path) for a new asset. Raises on invalid
    kind — this module only writes SKILL.md and POWER.md. The Phase C
    mechanism-selection branches for steering/hook/subagent/organ are outside
    this module's scope; their write routines live in whichever module
    implements those mechanisms.
    """
    if kind == "skill":
        asset_dir = SKILLS_ROOT / name
        return asset_dir, asset_dir / "SKILL.md"
    if kind == "power":
        asset_dir = POWERS_ROOT / name
        return asset_dir, asset_dir / "POWER.md"
    raise ValueError(
        f"write_new_asset supports kind in ('skill', 'power'); got {kind!r}. "
        f"Other mechanisms (steering/hook/subagent/organ) are written by "
        f"their respective modules."
    )


def _atomic_write(path: Path, text: str) -> None:
    """
    Write `text` to `path` via a tmp-and-rename atomic pattern.

    Guarantees: `path` is either the prior contents (unchanged on I/O error)
    or the new contents — never a half-written file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def write_new_asset(
    kind: str,
    name: str,
    frontmatter: dict[str, Any],
    body: str,
    overlap_check_record: dict[str, Any],
) -> Path:
    """
    Phase C.3 new-asset write path.

    Writes `~/.kiro/skills/{name}/SKILL.md` (or POWER.md for powers) with
    the supplied frontmatter + body, plus the overlap-check evidence file
    `~/.kiro/skills/{name}/overlap-check.json`.

    Per design §Phase C.3 & Property 9:
      - The overlap_check_record's `decision` must be CREATE_NEW. An
        EXTEND_EXISTING decision means this function should not have been
        called (caller should have routed to the existing asset instead).
      - `reviewed_by_richard` must be True. Writes are blocked otherwise.

    Per design §Data Model → Skill metadata extension:
      - `status: current`, `created_at: {now}`, `last_validated: {now}` are
        set here. If the caller pre-populated these fields with CONFLICTING
        values (e.g., `status: legacy`), raise ValueError — the caller is
        signaling the wrong path.

    Returns the Path to the written SKILL.md / POWER.md.

    Raises:
        FileExistsError — target md file already exists. Never overwrite.
        ValueError      — overlap-check didn't approve CREATE_NEW, Richard
                          hasn't reviewed, or frontmatter conflicts with
                          status=current.
    """
    if overlap_check_record.get("decision") != "CREATE_NEW":
        raise ValueError(
            f"write_new_asset requires overlap_check.decision == 'CREATE_NEW'; "
            f"got {overlap_check_record.get('decision')!r}"
        )
    if not overlap_check_record.get("reviewed_by_richard"):
        raise ValueError(
            "write_new_asset requires overlap_check.reviewed_by_richard == "
            "True; Phase C.2 has not approved this proposal"
        )

    _, md_path = _target_dir_for(kind, name)
    if md_path.exists():
        raise FileExistsError(
            f"refusing to overwrite existing {md_path}; new-asset writes "
            f"are never destructive (design §Phase C.3)"
        )

    # Build the final frontmatter dict — inject timestamps + status, reject
    # conflicts. We copy to avoid mutating the caller's dict.
    fm: dict[str, Any] = dict(frontmatter)
    now = _now_ts()

    declared_status = fm.get("status")
    if declared_status is not None and declared_status != "current":
        raise ValueError(
            f"new-asset write refuses frontmatter with status={declared_status!r}; "
            f"Phase C.3 new-asset writes produce status=current only "
            f"(design §Schema status rules)"
        )
    fm["status"] = "current"

    for ts_field in ("created_at", "last_validated"):
        existing = fm.get(ts_field)
        if existing not in (None, "", now):
            raise ValueError(
                f"new-asset write refuses conflicting {ts_field}={existing!r}; "
                f"Phase C.3 sets these fields to the current time. Remove or "
                f"align the caller-provided value."
            )
        fm[ts_field] = now

    # Name coherence: frontmatter.name should match directory name.
    if fm.get("name") is not None and fm["name"] != name:
        raise ValueError(
            f"frontmatter.name ({fm['name']!r}) does not match requested "
            f"asset name ({name!r})"
        )
    fm.setdefault("name", name)

    # Render canonical YAML + body via inventory's round-trip serializer.
    serialized = _inv.serialize_frontmatter(fm, body)
    _atomic_write(md_path, serialized)

    # Evidence file alongside the asset.
    overlap_path = md_path.parent / "overlap-check.json"
    _atomic_write(
        overlap_path,
        json.dumps(overlap_check_record, indent=2, ensure_ascii=False) + "\n",
    )

    return md_path


# ----------------------------------------------------------------------------
# Task 5.4 — classify_legacy_then_write (Phase C.3 touch-it-classify-it)
# ----------------------------------------------------------------------------


def _infer_kind_from_path(path: Path) -> str:
    name = path.name
    if name == "SKILL.md":
        return "skill"
    if name == "POWER.md":
        return "power"
    raise ValueError(
        f"classify_legacy_then_write only supports SKILL.md / POWER.md; "
        f"got {path}"
    )


def classify_legacy_then_write(
    path: Path,
    edit_function: Callable[[str], str],
    classification_callback: Callable[[dict[str, Any], str], dict[str, Any] | None],
) -> dict[str, Any]:
    """
    Phase C.3 legacy-migration path (touch-it-classify-it).

    Flow:
      a. parse existing file
      b. compute edited text via edit_function(current_text)
      c. re-parse edited text to ensure YAML still valid
      d. call classification_callback(frontmatter, kind)
      e. if callback returned a classification dict → insert fields, flip
         status to current, set created_at from file mtime (or "UNKNOWN" on
         stat failure), set last_validated=now, re-serialize, atomic write
      f. if callback returned None → accept refusal. Write edited text,
         preserving minimal frontmatter. Status stays legacy.

    Returns a record with:
        {
          "path": str,                  # ~/.kiro/...
          "action": "classified" | "edit_only",
          "previous_status": str,       # usually "legacy"
          "new_status": str,            # "current" or unchanged
          "mtime_before": float,
          "mtime_after": float,
        }

    Raises:
        FileNotFoundError if `path` does not exist.
        ValueError if the existing file or the edit result produces invalid
            frontmatter.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"classify_legacy_then_write: {path} not found")

    kind = _infer_kind_from_path(path)

    try:
        mtime_before = path.stat().st_mtime
    except OSError:
        mtime_before = 0.0

    current_text = path.read_text(encoding="utf-8")
    parsed_current = _inv.parse_frontmatter(current_text)
    if not isinstance(parsed_current, _inv.ParseSuccess):
        raise ValueError(
            f"existing file has invalid frontmatter; refusing to edit: "
            f"{parsed_current.violation}"
        )
    previous_status = parsed_current.frontmatter.get("status", "legacy")

    # Apply caller's edit.
    new_text = edit_function(current_text)
    if not isinstance(new_text, str):
        raise TypeError(
            f"edit_function must return str, got {type(new_text).__name__}"
        )
    parsed_edit = _inv.parse_frontmatter(new_text)
    if not isinstance(parsed_edit, _inv.ParseSuccess):
        raise ValueError(
            f"edit produced invalid frontmatter; refusing to write: "
            f"{parsed_edit.violation}"
        )

    # Ask the caller whether to classify.
    classification = classification_callback(parsed_edit.frontmatter, kind)

    if classification is None:
        # Refusal: write the edit as-is, preserve legacy status.
        _atomic_write(path, new_text)
        try:
            mtime_after = path.stat().st_mtime
        except OSError:
            mtime_after = mtime_before
        return {
            "path": str(path),
            "action": "edit_only",
            "previous_status": previous_status,
            "new_status": parsed_edit.frontmatter.get("status", "legacy"),
            "mtime_before": mtime_before,
            "mtime_after": mtime_after,
        }

    if not isinstance(classification, dict):
        raise TypeError(
            f"classification_callback must return dict or None, got "
            f"{type(classification).__name__}"
        )

    # Apply classification: inject fields, flip status → current.
    fm = dict(parsed_edit.frontmatter)
    for field in (
        "sensitive_data_class",
        "portability_tier",
        "platform_bound_dependencies",
        "owner_agent",
    ):
        if field in classification:
            fm[field] = classification[field]
    fm["status"] = "current"

    # created_at from file mtime — preserve historical creation date — or
    # "UNKNOWN" on stat failure per design §Phase C.3.
    try:
        created_at_dt = datetime.fromtimestamp(mtime_before).astimezone()
        fm["created_at"] = created_at_dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    except (OSError, OverflowError, ValueError):
        fm["created_at"] = "UNKNOWN"

    fm["last_validated"] = _now_ts()

    serialized = _inv.serialize_frontmatter(fm, parsed_edit.body)
    _atomic_write(path, serialized)

    try:
        mtime_after = path.stat().st_mtime
    except OSError:
        mtime_after = mtime_before

    return {
        "path": str(path),
        "action": "classified",
        "previous_status": previous_status,
        "new_status": "current",
        "mtime_before": mtime_before,
        "mtime_after": mtime_after,
    }



# ----------------------------------------------------------------------------
# Task 5.5 — activation_validate (Phase C.4 — SYNTACTIC ONLY)
# ----------------------------------------------------------------------------


def _is_canonical_path(path: Path) -> tuple[bool, str]:
    """Return (ok, canonical_root) describing whether path is at a canonical location."""
    try:
        rel_skills = path.relative_to(SKILLS_ROOT)
        # Must be {name}/SKILL.md — depth 2.
        parts = rel_skills.parts
        if len(parts) == 2 and parts[1] == "SKILL.md":
            return True, "~/.kiro/skills/"
        return False, "~/.kiro/skills/"
    except ValueError:
        pass
    try:
        rel_powers = path.relative_to(POWERS_ROOT)
        parts = rel_powers.parts
        if len(parts) == 2 and parts[1] == "POWER.md":
            return True, "~/.kiro/powers/installed/"
        return False, "~/.kiro/powers/installed/"
    except ValueError:
        pass
    return False, "none"


def _annotate_validation_failure(path: Path, reason: str) -> None:
    """
    Append a `# validation-failed: <reason>` comment line inside the file's
    frontmatter, just before the closing `---` fence. Best-effort: if we
    can't locate the fence cleanly, do nothing (the error is already in the
    returned record).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        return
    # Find the closing fence.
    close_idx: int | None = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == "---":
            close_idx = i
            break
    if close_idx is None:
        return
    annotation = f"# validation-failed: {reason}\n"
    # Avoid duplicating identical annotations.
    if any(
        line.rstrip("\r\n").startswith("# validation-failed:")
        for line in lines[1:close_idx]
    ):
        return
    new_lines = lines[:close_idx] + [annotation] + lines[close_idx:]
    _atomic_write(path, "".join(new_lines))


def activation_validate(path: Path) -> dict[str, Any]:
    """
    Phase C.4 — SYNTACTIC VALIDATION ONLY.

    **Documented gap**: full tool-level activation (calling discloseContext /
    kiroPowers activate) is the AGENT's responsibility and runs outside this
    module. discloseContext and kiroPowers are agent-level tools — they are
    not callable from a Python library. This function performs every check
    the library CAN perform:

      1. Parse file with inventory.parse_frontmatter — detect malformed YAML.
      2. Run inventory.validate_frontmatter — schema check for the declared
         status (current or legacy).
      3. Confirm the file sits at a canonical path (~/.kiro/skills/{name}/
         SKILL.md or ~/.kiro/powers/installed/{name}/POWER.md).
      4. For powers, verify mcp.json is JSON-parseable if present (not its
         semantic shape — the library can't resolve MCP servers).

    On success: update `last_validated: {now}` in the file's frontmatter
    (parse → update → serialize → atomic write) and return valid=True.

    On failure: annotate the frontmatter with a `# validation-failed: <reason>`
    comment (appended before the closing fence) so the agent's subsequent
    activation sweep can skip the asset. Returns valid=False with the list
    of violations.

    Returns:
        {
          "valid": bool,
          "level": "syntactic",   # always — no tool-level check here
          "path": str,
          "violations": [str, ...],
          "canonical_path_ok": bool,
        }
    """
    path = Path(path)
    violations: list[str] = []

    if not path.is_file():
        return {
            "valid": False,
            "level": "syntactic",
            "path": str(path),
            "violations": [f"file not found: {path}"],
            "canonical_path_ok": False,
        }

    # Canonical path check.
    canon_ok, canon_root = _is_canonical_path(path)
    if not canon_ok:
        violations.append(
            f"non-canonical path: expected {canon_root}<name>/SKILL.md or "
            f"...POWER.md, got {path}"
        )

    # Parse + schema.
    text = path.read_text(encoding="utf-8")
    parsed = _inv.parse_frontmatter(text)
    if not isinstance(parsed, _inv.ParseSuccess):
        violations.append(f"frontmatter parse failed: {parsed.violation}")
        _annotate_validation_failure(path, parsed.violation)
        return {
            "valid": False,
            "level": "syntactic",
            "path": str(path),
            "violations": violations,
            "canonical_path_ok": canon_ok,
        }

    kind = "skill" if path.name == "SKILL.md" else "power"
    schema_violation = _inv.validate_frontmatter(parsed.frontmatter, kind=kind)
    if schema_violation:
        violations.append(f"schema violation: {schema_violation}")

    # Powers: optional mcp.json JSON-validity check.
    if kind == "power":
        mcp_path = path.parent / "mcp.json"
        if mcp_path.is_file():
            try:
                json.loads(mcp_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as e:
                violations.append(f"mcp.json invalid JSON: {e}")

    if violations:
        reason = violations[0]
        _annotate_validation_failure(path, reason)
        return {
            "valid": False,
            "level": "syntactic",
            "path": str(path),
            "violations": violations,
            "canonical_path_ok": canon_ok,
        }

    # Valid — update last_validated and re-write.
    fm = dict(parsed.frontmatter)
    fm["last_validated"] = _now_ts()
    serialized = _inv.serialize_frontmatter(fm, parsed.body)
    _atomic_write(path, serialized)
    return {
        "valid": True,
        "level": "syntactic",
        "path": str(path),
        "violations": [],
        "canonical_path_ok": canon_ok,
    }


# ----------------------------------------------------------------------------
# Task 5.6 — post_creation_update (Phase C.5)
# ----------------------------------------------------------------------------


def post_creation_update(
    kind: str,
    name: str,
    overlap_check_path: Path | None,
    subtype: str = "created",
    session_id: str | None = None,
) -> None:
    """
    Phase C.5 post-creation update. Appends a `created` event row to the
    activation log and refreshes the inventory.

    Args:
        kind: "skill" or "power".
        name: asset name (also directory name).
        overlap_check_path: Path to the overlap-check.json evidence file.
            Required for subtype="created", MUST be None for subtype
            ="classified" (legacy migration has no overlap check per design
            §Phase C.1).
        subtype: "created" (new asset) or "classified" (legacy migration).
        session_id: passed through to activation_log.append_created_event.

    Side effects:
        - Appends one `created` row to activation-log.jsonl via
          activation_log.append_created_event.
        - Refreshes ~/shared/context/skills-powers/inventory.md via
          inventory.refresh().
    """
    if kind not in ("skill", "power"):
        raise ValueError(f"kind must be 'skill' or 'power', got {kind!r}")
    if subtype not in ("created", "classified"):
        raise ValueError(
            f"subtype must be 'created' or 'classified', got {subtype!r}"
        )

    if subtype == "classified":
        # Enforced by activation_log.append_created_event too, but fail fast.
        if overlap_check_path is not None:
            raise ValueError(
                "subtype='classified' (legacy migration) MUST have "
                "overlap_check_path=None per design §Phase C.1"
            )
        ref_str: str | None = None
    else:
        if overlap_check_path is None:
            # New-asset writes produce an overlap-check.json alongside the
            # asset; passing None here is likely a caller bug, not a design
            # escape hatch. Warn-via-exception.
            raise ValueError(
                "subtype='created' requires overlap_check_path; the "
                "evidence file is written alongside the asset by "
                "write_new_asset()"
            )
        # Render as a HOME-relative string if possible.
        try:
            ref_str = f"~/{Path(overlap_check_path).relative_to(HOME)}"
        except ValueError:
            ref_str = str(overlap_check_path)

    _log.append_created_event(
        kind=kind,  # type: ignore[arg-type]
        name=name,
        subtype=subtype,
        overlap_check_ref=ref_str,
        session_id=session_id,
    )

    # Refresh inventory.md so the new/migrated row surfaces immediately.
    _inv.refresh()


# ----------------------------------------------------------------------------
# Module-level self-description (no side effects)
# ----------------------------------------------------------------------------


if __name__ == "__main__":  # pragma: no cover
    print("safe_creation module — Phase C of skills-powers-adoption")
    print("  overlap_check(proposed, routing_decision)")
    print("  richard_review_gate(proposal, overlap_result, ")
    print("                      portability_report, sensitivity_check,")
    print("                      review_callback)")
    print("  console_review(summary)  — stdin-backed default callback")
    print("  write_new_asset(kind, name, frontmatter, body, overlap_check_record)")
    print("  classify_legacy_then_write(path, edit_function, classification_callback)")
    print("  activation_validate(path)  — SYNTACTIC ONLY; see docstring")
    print("  post_creation_update(kind, name, overlap_check_path, subtype='created')")
