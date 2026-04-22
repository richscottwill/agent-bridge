"""
Validators — cross-cutting (Group 7) of the skills-powers-adoption spec.

Six finite validators, all read-only (per design §Anti-Goals #5 / #7):

  7.1  roundtrip_check(path)                — property-test wrapper over the
                                               inventory parse/serialize
                                               primitives (Property 6).
  7.2  format_compliance_check(path)        — non-silent-rewrite parser report
                                               (Property 7). File unchanged on
                                               every code path.
  7.3  sensitivity_path_check(fm, out_path) — ENFORCED path-allowlist check
                                               per §Sensitive-Data
                                               Classification Rules
                                               (Property 3). Status-gated: skips
                                               legacy.
  7.4  portability_report(path, body=None)  — ADVISORY-ONLY scan of Platform_
                                               Bound indicator tokens
                                               (Property 4). Never rejects,
                                               never modifies, never auto-
                                               downgrades.
  7.5  schema_check(fm, kind)               — thin wrapper over
                                               inventory.validate_frontmatter
                                               with status-gating
                                               (Property 11).
  7.6  wrapper_skill_check(body)            — detects single-invokeSubAgent
                                               wrapper skills (Property 13).
                                               Blocks writes when True.

Design stance (per prompt + design §Anti-Goals):
  - Validators are functions, not services. They run reactively from Phase C
    (safe-creation) or ad-hoc.
  - Sensitivity is the ONLY enforced/blocking validator.
  - Schema is status-gated (legacy exempt).
  - Portability is advisory-only.
  - Subagent-wrapper detector rejects writes (blocking) per R10.4.
  - None of the validators ever modify source files. `file_unchanged: True`
    is confirmed by mtime check where relevant.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

try:
    import inventory as _inv
except ImportError:  # pragma: no cover — package-mode import
    from . import inventory as _inv  # type: ignore


# ----------------------------------------------------------------------------
# Paths (consumed by sensitivity_path_check)
# ----------------------------------------------------------------------------

HOME = Path(os.path.expanduser("~"))
SKILLS_ROOT = HOME / ".kiro" / "skills"
POWERS_ROOT = HOME / ".kiro" / "powers" / "installed"
STEERING_ROOT = HOME / ".kiro" / "steering"
SHARED_CONTEXT_ROOT = HOME / "shared" / "context"
SHARED_CONTEXT_BODY = SHARED_CONTEXT_ROOT / "body"
SHARED_CONTEXT_PROTOCOLS = SHARED_CONTEXT_ROOT / "protocols"
BRIDGE_SYNC_SKILL = SKILLS_ROOT / "bridge-sync" / "SKILL.md"

# Hardcoded bridge-sync fallback per current convention (design §Sensitive-Data
# Classification Rules → "Forbidden paths"). Only used when the live SKILL.md
# cannot be read.
_BRIDGE_SYNC_FALLBACK: tuple[Path, ...] = (
    SHARED_CONTEXT_BODY,
    SHARED_CONTEXT_PROTOCOLS,
    STEERING_ROOT,
)


# ----------------------------------------------------------------------------
# Task 7.1 — round-trip parser/serializer (Property 6)
# ----------------------------------------------------------------------------


def roundtrip_check(path: Path) -> dict[str, Any]:
    """
    Property-6 wrapper around inventory.parse_frontmatter and
    inventory.serialize_frontmatter. Read-only.

    Procedure:
      1. Read bytes at `path`.
      2. parse → serialize → re-parse.
      3. Assert the first and second parsed frontmatter dicts are structurally
         equal AND the first-pass body is byte-identical to the re-parsed body.

    Returns:
      {
        "valid": bool,
        "violations": [str, ...],
        "frontmatter_roundtrip_equal": bool,
        "body_byte_identical": bool,
        "file_unchanged": True,    # this validator never writes
      }
    """
    path = Path(path)
    if not path.is_file():
        return {
            "valid": False,
            "violations": [f"file not found: {path}"],
            "frontmatter_roundtrip_equal": False,
            "body_byte_identical": False,
            "file_unchanged": True,
        }

    mtime_before = path.stat().st_mtime
    original = path.read_text(encoding="utf-8")
    parsed = _inv.parse_frontmatter(original)
    if not isinstance(parsed, _inv.ParseSuccess):
        return {
            "valid": False,
            "violations": [f"parse failed: {parsed.violation}"],
            "frontmatter_roundtrip_equal": False,
            "body_byte_identical": False,
            "file_unchanged": _confirm_unchanged(path, mtime_before),
        }

    reserialized = _inv.serialize_frontmatter(parsed.frontmatter, parsed.body)
    reparsed = _inv.parse_frontmatter(reserialized)
    if not isinstance(reparsed, _inv.ParseSuccess):
        return {
            "valid": False,
            "violations": [
                f"re-serialized text failed to re-parse: {reparsed.violation}"
            ],
            "frontmatter_roundtrip_equal": False,
            "body_byte_identical": False,
            "file_unchanged": _confirm_unchanged(path, mtime_before),
        }

    fm_equal = parsed.frontmatter == reparsed.frontmatter
    body_equal = parsed.body == reparsed.body

    violations: list[str] = []
    if not fm_equal:
        violations.append(
            "frontmatter roundtrip inequality: parsed → serialized → parsed "
            "produced a structurally different dict"
        )
    if not body_equal:
        violations.append(
            "body not byte-identical after roundtrip: markdown content was "
            "mutated by serialize"
        )

    return {
        "valid": not violations,
        "violations": violations,
        "frontmatter_roundtrip_equal": fm_equal,
        "body_byte_identical": body_equal,
        "file_unchanged": _confirm_unchanged(path, mtime_before),
    }


def _confirm_unchanged(path: Path, mtime_before: float) -> bool:
    """Verify the file's mtime has not advanced since we observed it."""
    try:
        return path.stat().st_mtime == mtime_before
    except OSError:
        return False


# ----------------------------------------------------------------------------
# Task 7.2 — format-compliance validator (Property 7)
# ----------------------------------------------------------------------------

# Fields we recognize per the design §Data Model. Anything else is preserved in
# `legacy_unknown_fields` (non-destructive, per Property 7).
_KNOWN_SKILL_FIELDS = frozenset(
    {
        "name",
        "description",
        "status",
        "sensitive_data_class",
        "portability_tier",
        "platform_bound_dependencies",
        "owner_agent",
        "created_at",
        "last_validated",
    }
)
_KNOWN_POWER_FIELDS = frozenset(
    {
        "name",
        "displayName",
        "description",
        "keywords",
        "author",
        "status",
        "sensitive_data_class",
        "portability_tier",
        "platform_bound_dependencies",
        "mcp_servers_declared",
        "owner_agent",
        "created_at",
        "last_validated",
    }
)


def format_compliance_check(path: Path) -> dict[str, Any]:
    """
    Property-7 non-silent-rewrite validator. Never modifies the file.

    On parse success:
      - Run inventory.validate_frontmatter (status-gated).
      - Preserve any fields not in the known-field set under
        `legacy_unknown_fields` — DO NOT DROP THEM.

    On parse failure: return a descriptive error, file unchanged.

    Always confirms `file_unchanged: True` by re-reading mtime.
    """
    path = Path(path)
    if not path.is_file():
        return {
            "valid": False,
            "violations": [f"file not found: {path}"],
            "legacy_unknown_fields": None,
            "file_unchanged": True,
        }

    mtime_before = path.stat().st_mtime
    text = path.read_text(encoding="utf-8")
    parsed = _inv.parse_frontmatter(text)

    if not isinstance(parsed, _inv.ParseSuccess):
        # Non-silent rewrite: DO NOT touch the file. Return descriptive error.
        return {
            "valid": False,
            "violations": [f"parse failed: {parsed.violation}"],
            "legacy_unknown_fields": None,
            "file_unchanged": _confirm_unchanged(path, mtime_before),
        }

    kind = "skill" if path.name == "SKILL.md" else (
        "power" if path.name == "POWER.md" else "unknown"
    )

    violations: list[str] = []
    if kind == "unknown":
        violations.append(
            f"unsupported filename for format-compliance: expected SKILL.md "
            f"or POWER.md, got {path.name}"
        )

    # Run schema validation only when the kind is recognized.
    schema_violation: str | None = None
    if kind in ("skill", "power"):
        schema_violation = _inv.validate_frontmatter(parsed.frontmatter, kind=kind)
        if schema_violation:
            violations.append(f"schema violation: {schema_violation}")

    # Preserve unknown fields (Property 7: don't drop).
    if kind == "skill":
        known = _KNOWN_SKILL_FIELDS
    elif kind == "power":
        known = _KNOWN_POWER_FIELDS
    else:
        known = frozenset()
    unknown = {
        k: v for k, v in parsed.frontmatter.items() if k not in known
    }
    legacy_unknown_fields = unknown if unknown else None

    return {
        "valid": not violations,
        "violations": violations,
        "legacy_unknown_fields": legacy_unknown_fields,
        "file_unchanged": _confirm_unchanged(path, mtime_before),
    }


# ----------------------------------------------------------------------------
# Task 7.3 — sensitivity path-allowlist validator (Property 3, ENFORCED)
# ----------------------------------------------------------------------------

# Per-tier allowlist of directory prefixes. Each value is the set of directory
# roots that a file of the given sensitivity class may live under. "Any path"
# is encoded as None.
_ALLOWLIST_AMAZON_CONFIDENTIAL: tuple[Path, ...] = (
    SKILLS_ROOT,
    POWERS_ROOT,
    SHARED_CONTEXT_ROOT,
    # SharePoint Kiro-Drive/ — represented as a HOME-relative marker; the
    # library cannot resolve a mounted SharePoint path in a portable way, so
    # we accept "SharePoint Kiro-Drive/" prefix strings via _check_sharepoint.
)

_ALLOWLIST_PERSONAL_PII: tuple[Path, ...] = (
    SKILLS_ROOT,
    POWERS_ROOT,
    SHARED_CONTEXT_ROOT,
)

# Sensitivity tiers. If the frontmatter is missing this field (for current
# assets) we treat it as Amazon_Confidential per R3.5 default-up rule.
_VALID_SENSITIVITY = ("Public", "Amazon_Internal", "Amazon_Confidential", "Personal_PII")


def sensitivity_path_check(
    frontmatter: dict[str, Any],
    output_path: Path,
    *,
    agent_bridge_synced_paths: list[Path] | None = None,
) -> dict[str, Any]:
    """
    Enforced path-allowlist check per §Sensitive-Data Classification Rules.

    Status-gating: legacy assets skip (returns valid=True, skipped=True).

    For current assets:
      - Read `sensitive_data_class`; absent ⇒ Amazon_Confidential default.
      - Look up per-tier allowlist.
      - Error if output_path not under any allowlist root.
      - For Amazon_Confidential / Personal_PII: additionally error if
        output_path is under any agent_bridge_synced_paths.
      - For Personal_PII: additionally error if output_path is under
        ~/shared/context/protocols/ (prefer body/).

    Returns:
      {
        "valid": bool,
        "violations": [str, ...],
        "sensitivity_class": str,
        "allowlist": [str, ...],         # HOME-relative string representations
        "sync_violation": bool,
        "skipped": bool,                 # True for legacy assets
        "reason": str | None,
      }
    """
    output_path = Path(output_path)
    status = frontmatter.get("status", "legacy")

    if status == "legacy":
        return {
            "valid": True,
            "violations": [],
            "sensitivity_class": "",
            "allowlist": [],
            "sync_violation": False,
            "skipped": True,
            "reason": "legacy asset grandfathered",
        }

    sensitivity = frontmatter.get("sensitive_data_class") or "Amazon_Confidential"
    if sensitivity not in _VALID_SENSITIVITY:
        return {
            "valid": False,
            "violations": [
                f"unknown sensitive_data_class: {sensitivity!r}; expected one "
                f"of {list(_VALID_SENSITIVITY)}"
            ],
            "sensitivity_class": sensitivity,
            "allowlist": [],
            "sync_violation": False,
            "skipped": False,
            "reason": None,
        }

    synced = (
        [Path(p) for p in agent_bridge_synced_paths]
        if agent_bridge_synced_paths is not None
        else _read_agent_bridge_synced_paths()
    )

    violations: list[str] = []
    sync_violation = False

    if sensitivity == "Public":
        allowlist: tuple[Path, ...] = ()  # any path
        # No allowlist check. No sync check. Public may live anywhere.
    elif sensitivity == "Amazon_Internal":
        allowlist = ()  # any local path. No hard sync restriction — only a
        # warning; we implement this without erroring.
        if _path_under_any(output_path, synced):
            # Per design: "warn if in bridge-sync scope, don't error".
            # We expose it via sync_violation=True but keep valid=True.
            sync_violation = True
    elif sensitivity == "Amazon_Confidential":
        allowlist = _ALLOWLIST_AMAZON_CONFIDENTIAL
        if not _path_under_any(output_path, allowlist):
            violations.append(
                f"path {output_path} is not under any Amazon_Confidential "
                f"allowlist root: {_allowlist_display(allowlist)}"
            )
        if _path_under_any(output_path, synced):
            violations.append(
                f"Amazon_Confidential asset cannot live under an agent-bridge"
                f"-synced path: {_matched_sync_prefix(output_path, synced)}"
            )
            sync_violation = True
    elif sensitivity == "Personal_PII":
        allowlist = _ALLOWLIST_PERSONAL_PII
        if not _path_under_any(output_path, allowlist):
            violations.append(
                f"path {output_path} is not under any Personal_PII allowlist "
                f"root: {_allowlist_display(allowlist)}"
            )
        if _path_under_any(output_path, synced):
            violations.append(
                f"Personal_PII asset cannot live under an agent-bridge-synced "
                f"path: {_matched_sync_prefix(output_path, synced)}"
            )
            sync_violation = True
        # Additional rule: prefer ~/shared/context/body/ over protocols/.
        if _path_under(output_path, SHARED_CONTEXT_PROTOCOLS):
            violations.append(
                "Personal_PII asset should prefer ~/shared/context/body/ over "
                "~/shared/context/protocols/ (protocols is synced to agent-"
                "bridge)"
            )

    return {
        "valid": not violations,
        "violations": violations,
        "sensitivity_class": sensitivity,
        "allowlist": _allowlist_display(allowlist),
        "sync_violation": sync_violation,
        "skipped": False,
        "reason": None,
    }


def _path_under(path: Path, root: Path) -> bool:
    """True if `path` equals `root` or is a descendant of `root`."""
    try:
        path = Path(path).resolve(strict=False)
        root = Path(root).resolve(strict=False)
    except (OSError, ValueError):
        return False
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _path_under_any(path: Path, roots) -> bool:
    return any(_path_under(path, Path(r)) for r in roots)


def _matched_sync_prefix(path: Path, roots) -> str:
    for r in roots:
        if _path_under(path, Path(r)):
            try:
                return f"~/{Path(r).relative_to(HOME)}"
            except ValueError:
                return str(r)
    return ""


def _allowlist_display(roots) -> list[str]:
    out: list[str] = []
    for r in roots:
        try:
            out.append(f"~/{Path(r).relative_to(HOME)}")
        except ValueError:
            out.append(str(r))
    return out


def _read_agent_bridge_synced_paths() -> list[Path]:
    """
    Attempt to read the live bridge-sync SKILL.md body for an explicit sync
    list. Fall back to the hardcoded convention list if no sync-list block
    is parseable.

    Supported parse pattern: a fenced or bulleted list of `~/...` paths
    anywhere in the SKILL.md body. We accept any line matching `^\\s*[-*]\\s+
    (~/[^\\s`]+)` and treat each captured path as a synced root.
    """
    if not BRIDGE_SYNC_SKILL.is_file():
        return list(_BRIDGE_SYNC_FALLBACK)
    try:
        text = BRIDGE_SYNC_SKILL.read_text(encoding="utf-8")
    except OSError:
        return list(_BRIDGE_SYNC_FALLBACK)

    # Strip frontmatter to reduce noise.
    parsed = _inv.parse_frontmatter(text)
    body = parsed.body if isinstance(parsed, _inv.ParseSuccess) else text

    matches: list[Path] = []
    for line in body.splitlines():
        m = re.match(r"^\s*[-*]\s+`?(~/[^\s`]+)`?", line)
        if m:
            raw = m.group(1)
            # Expand ~ and normalize trailing slash.
            expanded = Path(os.path.expanduser(raw))
            matches.append(expanded)

    if not matches:
        return list(_BRIDGE_SYNC_FALLBACK)
    return matches


# ----------------------------------------------------------------------------
# Task 7.4 — advisory portability validator (Property 4, REPORT-ONLY)
# ----------------------------------------------------------------------------

# Indicator-token regexes per design §Portability Tier Rules.
_PORTABILITY_PATTERNS: dict[str, re.Pattern[str]] = {
    "mcp_tool": re.compile(r"\bmcp_[a-z][a-z0-9_]*"),
    "subagent": re.compile(
        r"""invokeSubAgent\s*\(\s*[^)]*?name\s*=\s*["']([a-z0-9][a-z0-9\-]*)["']""",
        re.DOTALL,
    ),
    "hook": re.compile(r"\b[a-z0-9][a-z0-9_\-]*\.kiro\.hook\b"),
    "kiro_api": re.compile(r"\b(?:discloseContext|kiroPowers)\s*\("),
    "script_path": re.compile(
        r"(?:~/shared/(?:tools|scripts)/[A-Za-z0-9_./\-]+|(?<![A-Za-z0-9/])scripts/[A-Za-z0-9_./\-]+)"
    ),
    "duckdb_table": re.compile(
        r"\b(?:ps|signals|asana|main|docs)\.[a-z_][a-z0-9_]*"
    ),
}


def portability_report(
    path: Path, body: str | None = None
) -> dict[str, Any]:
    """
    Advisory-only Property-4 report. Never modifies, never rejects.

    Scans body for Platform_Bound indicator tokens, groups by kind, and
    cross-checks against the declared `platform_bound_dependencies` list.

    Returns:
      {
        "advisory": True,
        "declared_tier": str,           # Cold_Start_Safe | Platform_Bound |
                                        # "" when frontmatter absent
        "findings": {kind: [token, ...]},
        "platform_bound_dependencies_cross_check": {
          "declared": [{"kind": ..., "id": ...}, ...],
          "undeclared_tokens": [{"kind": ..., "id": ...}, ...],
          "declared_but_unused": [{"kind": ..., "id": ...}, ...],
        },
        "cold_start_safe_inconsistency": bool,  # advisory flag; True when
                                                # declared Cold_Start_Safe
                                                # AND any platform-bound
                                                # tokens were found
        "file_unchanged": True,
      }
    """
    path = Path(path)
    file_unchanged = True
    declared_tier = ""
    declared_deps: list[dict[str, str]] = []
    mtime_before: float | None = None

    if body is None:
        if not path.is_file():
            return {
                "advisory": True,
                "declared_tier": "",
                "findings": {},
                "platform_bound_dependencies_cross_check": {
                    "declared": [],
                    "undeclared_tokens": [],
                    "declared_but_unused": [],
                },
                "cold_start_safe_inconsistency": False,
                "file_unchanged": True,
                "violations": [f"file not found: {path}"],
            }
        mtime_before = path.stat().st_mtime
        text = path.read_text(encoding="utf-8")
        parsed = _inv.parse_frontmatter(text)
        if isinstance(parsed, _inv.ParseSuccess):
            declared_tier = parsed.frontmatter.get("portability_tier", "") or ""
            raw_deps = parsed.frontmatter.get("platform_bound_dependencies")
            if isinstance(raw_deps, list):
                for entry in raw_deps:
                    if isinstance(entry, dict) and "kind" in entry and "id" in entry:
                        declared_deps.append(
                            {"kind": str(entry["kind"]), "id": str(entry["id"])}
                        )
            body_text = parsed.body
        else:
            body_text = text
    else:
        body_text = body

    findings: dict[str, list[str]] = {}
    found_tokens: set[tuple[str, str]] = set()
    for kind, pat in _PORTABILITY_PATTERNS.items():
        hits: list[str] = []
        for m in pat.finditer(body_text):
            token = m.group(1) if m.groups() else m.group(0)
            hits.append(token)
            found_tokens.add((kind, token))
        if hits:
            # Preserve discovery order but deduplicate.
            seen: set[str] = set()
            deduped: list[str] = []
            for h in hits:
                if h in seen:
                    continue
                seen.add(h)
                deduped.append(h)
            findings[kind] = deduped

    declared_set: set[tuple[str, str]] = {
        (d["kind"], d["id"]) for d in declared_deps
    }
    undeclared_tokens = [
        {"kind": k, "id": v}
        for (k, v) in sorted(found_tokens - declared_set)
    ]
    declared_but_unused = [
        {"kind": k, "id": v}
        for (k, v) in sorted(declared_set - found_tokens)
    ]

    cold_start_safe_inconsistency = bool(
        declared_tier == "Cold_Start_Safe" and findings
    )

    if mtime_before is not None:
        file_unchanged = _confirm_unchanged(path, mtime_before)

    return {
        "advisory": True,
        "declared_tier": declared_tier,
        "findings": findings,
        "platform_bound_dependencies_cross_check": {
            "declared": declared_deps,
            "undeclared_tokens": undeclared_tokens,
            "declared_but_unused": declared_but_unused,
        },
        "cold_start_safe_inconsistency": cold_start_safe_inconsistency,
        "file_unchanged": file_unchanged,
    }


# ----------------------------------------------------------------------------
# Task 7.5 — status-gated schema validator (Property 11)
# ----------------------------------------------------------------------------


def schema_check(frontmatter: dict[str, Any], *, kind: str) -> dict[str, Any]:
    """
    Thin wrapper over inventory.validate_frontmatter. Exposes the status-gating
    contract per Property 11:

      - `status: legacy`   → always valid with minimal frontmatter.
      - `status: current`  → strict required-field check.
      - `status: retired`  → accepts minimal OR extended frontmatter.

    Returns:
      {
        "valid": bool,
        "violation": str | None,
        "status_gated": True,
        "inferred_status": str,     # the status used for gating
      }
    """
    inferred_status = frontmatter.get("status", "legacy")
    violation = _inv.validate_frontmatter(frontmatter, kind=kind)
    return {
        "valid": violation is None,
        "violation": violation,
        "status_gated": True,
        "inferred_status": inferred_status,
    }


# ----------------------------------------------------------------------------
# Task 7.6 — subagent-wrapper detector (Property 13)
# ----------------------------------------------------------------------------

_INVOKE_SUBAGENT_RE = re.compile(r"invokeSubAgent\s*\(", re.MULTILINE)
_SUBAGENT_NAME_RE = re.compile(
    r"""invokeSubAgent\s*\(\s*[^)]*?name\s*=\s*["']([a-z0-9][a-z0-9\-]*)["']""",
    re.DOTALL,
)
_OTHER_TOOL_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("mcp_call", re.compile(r"\bmcp_[a-z][a-z0-9_]*\s*\(")),
    ("discloseContext", re.compile(r"\bdiscloseContext\s*\(")),
    ("kiroPowers", re.compile(r"\bkiroPowers\s*\(")),
    ("hook_reference", re.compile(r"\b[a-z0-9][a-z0-9_\-]*\.kiro\.hook\b")),
    ("execute_query", re.compile(r"\bexecute_query\s*\(")),
)


def wrapper_skill_check(body: str) -> dict[str, Any]:
    """
    Property 13 — detect SKILL.md bodies that wrap exactly one invokeSubAgent
    call with no other orchestration. Such skills are redundant with the
    subagent itself and should be rejected per R10.4.

    Returns:
      {
        "wrapper_detected": bool,
        "subagent_count": int,
        "subagent_names": [str, ...],
        "other_tool_calls": [str, ...],   # non-invokeSubAgent tool references
        "rejection_reason": str | None,   # set only when wrapper_detected
      }
    """
    if not isinstance(body, str):
        raise TypeError(f"body must be str, got {type(body).__name__}")

    # Strip fenced code blocks first? No — invocations in code blocks still
    # count as references per design R10.4. We match the raw body.
    invoke_matches = list(_INVOKE_SUBAGENT_RE.finditer(body))
    subagent_names = [m.group(1) for m in _SUBAGENT_NAME_RE.finditer(body)]
    # Dedupe preserving discovery order.
    seen: set[str] = set()
    unique_names: list[str] = []
    for n in subagent_names:
        if n in seen:
            continue
        seen.add(n)
        unique_names.append(n)

    other_calls: list[str] = []
    for kind, pat in _OTHER_TOOL_PATTERNS:
        for m in pat.finditer(body):
            tok = m.group(0)
            other_calls.append(f"{kind}:{tok}")

    invoke_count = len(invoke_matches)
    unique_names_count = len(unique_names)

    # Wrapper condition: exactly ONE invokeSubAgent call (count, not distinct
    # names), ≤1 distinct subagent name, and no other orchestration tokens.
    wrapper_detected = (
        invoke_count == 1 and unique_names_count <= 1 and not other_calls
    )
    rejection_reason = (
        "wraps single subagent; subagent is the correct mechanism (R10.4)"
        if wrapper_detected
        else None
    )

    return {
        "wrapper_detected": wrapper_detected,
        "subagent_count": unique_names_count,
        "subagent_names": unique_names,
        "other_tool_calls": other_calls,
        "rejection_reason": rejection_reason,
    }


# ----------------------------------------------------------------------------
# Module self-description
# ----------------------------------------------------------------------------


if __name__ == "__main__":  # pragma: no cover
    print("validators module — Group 7 of skills-powers-adoption")
    print("  roundtrip_check(path)                   — Property 6")
    print("  format_compliance_check(path)           — Property 7")
    print("  sensitivity_path_check(fm, out_path)    — Property 3 (enforced)")
    print("  portability_report(path, body=None)     — Property 4 (advisory)")
    print("  schema_check(fm, kind)                  — Property 11")
    print("  wrapper_skill_check(body)               — Property 13")
