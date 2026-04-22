"""
Skills & Powers Inventory generator — Phase A of the skills-powers-adoption spec.

Walks ~/.kiro/skills/ and ~/.kiro/powers/installed/, parses YAML frontmatter,
reads ~/shared/context/skills-powers/activation-log.jsonl, and renders
~/shared/context/skills-powers/inventory.md per the design's §Data Model →
Inventory file schema.

USAGE

    python3 inventory.py refresh

TRIGGER

    Richard says "refresh skills inventory" (or equivalent) — the agent runs
    the refresh command above. No cron. No hook. No scheduled task. Per design
    §Anti-Goals #1 (not an ongoing audit service) and §Anti-Goals #8 (no new
    auto-loaded steering or scheduled jobs).

ROUND-TRIP FILE FORMAT

    The parser/serializer pair is byte-stable: parse(serialize(parse(f))) ==
    parse(f) holds for any file this module writes. Group 8 property tests
    verify this universally. The serializer is deterministic — same input
    always produces the same bytes. UTF-8, LF line endings, 2-space indent for
    nested values.

SCOPE

    Read-only against ~/.kiro/skills/ and ~/.kiro/powers/installed/. Writes
    only to ~/shared/context/skills-powers/inventory.md. Never modifies source
    SKILL.md or POWER.md files. Legacy assets stay legacy — classification
    only happens via touch-it-classify-it in Phase C (Group 5), not here.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    import yaml  # PyYAML 6.x
except ImportError:  # pragma: no cover — environment has PyYAML per Group 0 verification
    yaml = None


# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------

HOME = Path(os.path.expanduser("~"))
SKILLS_ROOT = HOME / ".kiro" / "skills"
POWERS_ROOT = HOME / ".kiro" / "powers" / "installed"
INVENTORY_DIR = HOME / "shared" / "context" / "skills-powers"
INVENTORY_MD = INVENTORY_DIR / "inventory.md"
ACTIVATION_LOG = INVENTORY_DIR / "activation-log.jsonl"


# ----------------------------------------------------------------------------
# Canonical frontmatter key ordering (per design §Round-Trip File Format)
# ----------------------------------------------------------------------------

# Groups: identity → status → classification → timestamps.
# Within each group, keys render in the order listed. Unknown keys are appended
# at the end in alphabetical order, preserving but not promoting them.

_KEY_ORDER = [
    # identity
    "name",
    "displayName",
    "description",
    "keywords",
    "author",
    # status
    "status",
    # classification
    "sensitive_data_class",
    "portability_tier",
    "platform_bound_dependencies",
    "mcp_servers_declared",
    "owner_agent",
    # timestamps
    "created_at",
    "last_validated",
]


# ----------------------------------------------------------------------------
# Data classes
# ----------------------------------------------------------------------------


@dataclass
class AssetRecord:
    """One installed SKILL.md or POWER.md on disk."""

    path: Path
    kind: str  # "skill" | "power"
    name: str
    raw_frontmatter_text: str  # exact bytes between the two `---` fences
    body_text: str
    mtime: float
    frontmatter: dict[str, Any] = field(default_factory=dict)
    has_mcp_json: bool = False  # powers only

    @property
    def rel_path(self) -> str:
        """Path relative to HOME for stable hashing across machines."""
        try:
            return str(self.path.relative_to(HOME))
        except ValueError:
            return str(self.path)


@dataclass
class ParseSuccess:
    frontmatter: dict[str, Any]
    body: str


@dataclass
class ParseError:
    violation: str


ParseResult = ParseSuccess | ParseError


@dataclass
class WalkResult:
    assets: list[AssetRecord]
    symlinks_followed: list[str]


# ----------------------------------------------------------------------------
# Task 2.1 — Filesystem walker
# ----------------------------------------------------------------------------


def walk_installed(
    skills_root: Path = SKILLS_ROOT,
    powers_root: Path = POWERS_ROOT,
) -> WalkResult:
    """
    Enumerate ~/.kiro/skills/*/SKILL.md and ~/.kiro/powers/installed/*/POWER.md.

    Follows symlinks at depth 1 max (the immediate asset directory may be a
    symlink, but we do not recurse into symlinked subtrees). Records any
    symlinks followed for the audit trail.
    """
    assets: list[AssetRecord] = []
    symlinks_followed: list[str] = []

    # Skills
    if skills_root.is_dir():
        for entry in sorted(skills_root.iterdir()):
            if not _is_dir_depth1(entry, symlinks_followed):
                continue
            skill_md = entry / "SKILL.md"
            if not skill_md.is_file():
                continue
            rec = _read_asset(skill_md, kind="skill", name=entry.name)
            if rec is not None:
                assets.append(rec)

    # Powers
    if powers_root.is_dir():
        for entry in sorted(powers_root.iterdir()):
            if not _is_dir_depth1(entry, symlinks_followed):
                continue
            power_md = entry / "POWER.md"
            if not power_md.is_file():
                continue
            rec = _read_asset(power_md, kind="power", name=entry.name)
            if rec is not None:
                rec.has_mcp_json = (entry / "mcp.json").is_file()
                assets.append(rec)

    return WalkResult(assets=assets, symlinks_followed=symlinks_followed)


def _is_dir_depth1(entry: Path, symlinks_followed: list[str]) -> bool:
    """Accept a directory at depth 1. Symlink → follow once, record it."""
    if entry.is_symlink():
        symlinks_followed.append(str(entry))
        # Resolve only one level; if the target is a directory, accept.
        target = entry.resolve()
        return target.is_dir()
    return entry.is_dir()


def _read_asset(md_path: Path, *, kind: str, name: str) -> AssetRecord | None:
    """Read a SKILL.md / POWER.md and return an AssetRecord (no parsing yet)."""
    try:
        text = md_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    mtime = md_path.stat().st_mtime
    raw_fm, body = _split_frontmatter(text)
    rec = AssetRecord(
        path=md_path,
        kind=kind,
        name=name,
        raw_frontmatter_text=raw_fm,
        body_text=body,
        mtime=mtime,
    )
    # Populate the parsed dict now (best-effort; errors are handled by caller
    # if they care). Walk_installed returns raw text + parsed dict so downstream
    # consumers can choose which to use.
    parsed = parse_frontmatter(text)
    if isinstance(parsed, ParseSuccess):
        rec.frontmatter = parsed.frontmatter
    return rec


def _split_frontmatter(text: str) -> tuple[str, str]:
    """
    Split a markdown file into (raw_frontmatter_text, body_text).

    Frontmatter is the content between the first two `---` fences when the
    file starts with `---\n`. If there is no frontmatter, raw is "" and body
    is the entire file.
    """
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return "", text
    # Find the closing fence.
    # Normalize to LF for searching; we keep the original bytes in body though.
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        return "", text
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == "---":
            end_idx = i
            break
    if end_idx is None:
        return "", text
    raw_fm = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1 :])
    return raw_fm, body


# ----------------------------------------------------------------------------
# Task 2.2 — YAML frontmatter parser and serializer
# ----------------------------------------------------------------------------


def parse_frontmatter(text: str) -> ParseResult:
    """
    Parse a SKILL.md / POWER.md full file text into (frontmatter dict, body str).

    Returns ParseSuccess on valid input, ParseError on malformed YAML, wrong
    shape, or status-required-field violations. Does NOT modify the source
    file. Per design §Round-Trip File Format → "Error reporting", the
    violation message is descriptive: field name, expected, actual.

    Status-gated validation:
      - status: current → all current-required fields must be present.
      - status: legacy (or missing — legacy is the default for pre-spec files)
        → only minimal fields (name + description for skills; name +
        displayName + description + keywords + author for powers) required.
      - status: retired → accepted with either minimal or extended frontmatter.
    """
    raw_fm, body = _split_frontmatter(text)
    if raw_fm == "":
        return ParseError("missing frontmatter: file must begin with `---` fence")
    if yaml is None:
        return ParseError("PyYAML is not installed; cannot parse frontmatter")
    try:
        fm = yaml.safe_load(raw_fm)
    except yaml.YAMLError as e:
        return ParseError(f"malformed YAML: {e}")
    if fm is None:
        return ParseError("empty frontmatter")
    if not isinstance(fm, dict):
        return ParseError(f"frontmatter must be a mapping, got {type(fm).__name__}")
    return ParseSuccess(frontmatter=fm, body=body)


def validate_frontmatter(fm: dict[str, Any], *, kind: str) -> str | None:
    """
    Status-gated schema validation. Returns None if valid, else a descriptive
    violation string. Used by downstream validators (Group 7); not called by
    the T0 inventory render because all installed assets are legacy.
    """
    status = fm.get("status", "legacy")
    if status not in ("legacy", "current", "retired"):
        return f"status: unknown value {status!r} (expected legacy | current | retired)"
    if status == "legacy":
        if kind == "skill":
            for key in ("name", "description"):
                if key not in fm:
                    return f"legacy skill missing required field: {key}"
        else:
            for key in ("name", "displayName", "description", "keywords", "author"):
                if key not in fm:
                    return f"legacy power missing required field: {key}"
        return None
    if status == "current":
        required_common = (
            "name",
            "description",
            "sensitive_data_class",
            "portability_tier",
            "created_at",
            "last_validated",
        )
        for key in required_common:
            if key not in fm:
                return f"current {kind} missing required field: {key}"
        if kind == "power":
            for key in ("displayName", "keywords", "author"):
                if key not in fm:
                    return f"current power missing required field: {key}"
        if fm.get("portability_tier") == "Platform_Bound":
            if "platform_bound_dependencies" not in fm:
                return "Platform_Bound asset missing platform_bound_dependencies"
        sensitivity = fm.get("sensitive_data_class")
        if sensitivity not in (
            "Public",
            "Amazon_Internal",
            "Amazon_Confidential",
            "Personal_PII",
        ):
            return f"sensitive_data_class: unknown value {sensitivity!r}"
        portability = fm.get("portability_tier")
        if portability not in ("Cold_Start_Safe", "Platform_Bound"):
            return f"portability_tier: unknown value {portability!r}"
    return None


def serialize_frontmatter(fm: dict[str, Any], body: str) -> str:
    """
    Render a (frontmatter, body) pair back to disk bytes deterministically.

    Canonical form per design §Round-Trip File Format:
      - UTF-8 text, LF line endings.
      - Opening `---\\n` fence, closing `---\\n` fence.
      - Keys emitted in the canonical _KEY_ORDER; unknown keys appended in
        alphabetical order so round-trip preserves them.
      - 2-space indent for nested structures. Block-form lists.
      - Strings that contain YAML special characters are double-quoted.
      - No trailing whitespace on any line.
    """
    ordered = _order_frontmatter(fm)
    yaml_text = _dump_yaml_canonical(ordered)
    # Ensure frontmatter section ends with exactly one LF before the closing fence.
    if not yaml_text.endswith("\n"):
        yaml_text += "\n"
    # Body: preserve as-is. If body does not start with a newline and is
    # non-empty, the closing `---\n` already provides separation.
    return f"---\n{yaml_text}---\n{body}"


def _order_frontmatter(fm: dict[str, Any]) -> list[tuple[str, Any]]:
    """Return (key, value) pairs in canonical order."""
    seen: set[str] = set()
    ordered: list[tuple[str, Any]] = []
    for key in _KEY_ORDER:
        if key in fm:
            ordered.append((key, fm[key]))
            seen.add(key)
    # Unknown keys — alphabetical, preserved.
    for key in sorted(k for k in fm.keys() if k not in seen):
        ordered.append((key, fm[key]))
    return ordered


def _dump_yaml_canonical(pairs: list[tuple[str, Any]]) -> str:
    """
    Deterministic YAML emitter. Uses PyYAML with sort_keys=False and our
    ordered pairs, so key order is preserved exactly as given. Default_flow_style
    is False (block form). Indent is 2.
    """
    od = {k: v for k, v in pairs}
    text = yaml.safe_dump(
        od,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        indent=2,
        width=10_000,  # discourage line-wrapping of long descriptions
    )
    return text


# ----------------------------------------------------------------------------
# Task 2.4 — sha256 input-state hash
# ----------------------------------------------------------------------------


def compute_input_state_hash(assets: list[AssetRecord]) -> str:
    """
    sha256 over `{rel_path}\\n{raw_frontmatter_text}\\n` for every asset,
    sorted by rel_path. Matches the design's §Inventory file freshness-
    verification recipe. Stable across runs with no FS changes.
    """
    h = hashlib.sha256()
    for rec in sorted(assets, key=lambda r: r.rel_path):
        h.update(rec.rel_path.encode("utf-8"))
        h.update(b"\n")
        h.update(rec.raw_frontmatter_text.encode("utf-8"))
        h.update(b"\n")
    return f"sha256:{h.hexdigest()}"


# ----------------------------------------------------------------------------
# Activation log reading
# ----------------------------------------------------------------------------


def read_activation_log(path: Path = ACTIVATION_LOG) -> list[dict[str, Any]]:
    """Read the JSONL activation log. Returns [] if the file is missing."""
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            # Skip malformed rows rather than crash inventory render.
            continue
    return rows


def _parse_ts(s: str | None) -> datetime | None:
    """Parse an ISO 8601 timestamp or a YYYY-MM-DD date."""
    if s is None or s == "":
        return None
    # Handle offsets without colon (e.g., -0700) and with (-07:00).
    # Python 3.13 fromisoformat handles most reasonable shapes.
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        pass
    # Try date-only.
    try:
        return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        pass
    # Try with offset without colon (Python fromisoformat on older versions
    # chokes; 3.11+ generally handles this, but be defensive).
    m = re.match(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})([+-]\d{2})(\d{2})$", s)
    if m:
        fixed = f"{m.group(1)}{m.group(2)}:{m.group(3)}"
        try:
            return datetime.fromisoformat(fixed)
        except ValueError:
            return None
    return None


# ----------------------------------------------------------------------------
# Task 2.3 — inventory.md rendering
# ----------------------------------------------------------------------------


@dataclass
class _UsageInfo:
    last_activated_display: str  # "2026-04-20" | "never" | ISO timestamp
    last_activated_dt: datetime | None
    usage: str  # "used" | "stale" | "unused"
    ever_activated: bool  # has at least one "activated" event (not counting baseline)


def _usage_for(
    name: str,
    kind: str,
    log: list[dict[str, Any]],
    now: datetime,
) -> _UsageInfo:
    """
    Compute Last Activated + Usage for one asset.

      - Usage "used":    ≥1 `activated` event in last 30 days.
      - Usage "stale":   `activated` events exist but none in last 30 days.
      - Usage "unused":  no `activated` events ever (baseline rows do not count).

    Last Activated display uses the most recent `activated` event OR the
    baseline's `last_observed` as a fallback. "never" if no data at all.
    """
    thirty_days_ago = now - timedelta(days=30)
    latest_activated: datetime | None = None
    baseline_last: datetime | None = None
    has_activated = False
    has_recent_activation = False

    for row in log:
        if row.get("name") != name or row.get("kind") != kind:
            continue
        event = row.get("event")
        if event == "activated":
            has_activated = True
            ts = _parse_ts(row.get("ts"))
            if ts is not None:
                if latest_activated is None or ts > latest_activated:
                    latest_activated = ts
                # Compare using an offset-naive-safe path.
                if _is_after(ts, thirty_days_ago):
                    has_recent_activation = True
        elif event == "baseline":
            last_obs = _parse_ts(row.get("last_observed"))
            if last_obs is not None:
                if baseline_last is None or last_obs > baseline_last:
                    baseline_last = last_obs

    if has_recent_activation:
        usage = "used"
    elif has_activated:
        usage = "stale"
    else:
        usage = "unused"

    display_dt = latest_activated or baseline_last
    if display_dt is None:
        display = "never"
    else:
        display = display_dt.date().isoformat()

    return _UsageInfo(
        last_activated_display=display,
        last_activated_dt=display_dt,
        usage=usage,
        ever_activated=has_activated,
    )


def _skill_triggers(fm: dict[str, Any]) -> str:
    """Extract trigger keywords from a skill's description.

    The convention (per design §Data Model → Skill metadata) is that the
    description ends with `Triggers on {kw}, {kw}, ...`. If that pattern is
    absent, return a placeholder.
    """
    desc = fm.get("description", "") or ""
    m = re.search(r"[Tt]riggers on\s+(.+?)\.?$", desc.strip())
    if m:
        return m.group(1).strip().rstrip(".")
    return "(no trigger clause)"


def _power_type(rec: AssetRecord) -> str:
    return "Guided MCP" if rec.has_mcp_json else "Knowledge Base"


def _legacy_dash(fm: dict[str, Any], field: str) -> str:
    """
    For legacy rows, sensitivity/portability render as em-dash.
    For current rows, render the value or **MISSING** in bold if absent.
    """
    status = fm.get("status", "legacy")
    if status == "legacy":
        return "—"
    value = fm.get(field)
    if value is None or value == "":
        return "**MISSING**"
    return str(value)


def _status_of(fm: dict[str, Any]) -> str:
    return fm.get("status", "legacy")


def render_inventory(
    assets: list[AssetRecord],
    activation_log: list[dict[str, Any]],
    *,
    now: datetime | None = None,
) -> str:
    """Render the inventory.md full body per design §Data Model → Inventory file."""
    now = now or datetime.now().astimezone()
    input_hash = compute_input_state_hash(assets)

    skills = sorted([a for a in assets if a.kind == "skill"], key=lambda r: r.name)
    powers = sorted([a for a in assets if a.kind == "power"], key=lambda r: r.name)

    usage_by_key = {
        (a.kind, a.name): _usage_for(a.name, a.kind, activation_log, now)
        for a in assets
    }

    lines: list[str] = []
    lines.append("# Skills & Powers Inventory")
    lines.append("")
    lines.append(f"**Last updated**: {_iso_with_tz(now)}")
    lines.append("**Activation log**: ~/shared/context/skills-powers/activation-log.jsonl")
    lines.append(f"**Input-state-hash**: {input_hash}")
    lines.append("")

    # Skills table
    lines.append("## Skills (~/.kiro/skills/)")
    lines.append("")
    lines.append("| Row ID | Name | Status | Triggers | Sensitivity | Portability | Last Activated | Usage |")
    lines.append("|--------|------|--------|----------|-------------|-------------|----------------|-------|")
    for i, rec in enumerate(skills, start=1):
        u = usage_by_key[(rec.kind, rec.name)]
        row_id = f"K-S{i}"
        triggers = _escape_pipes(_skill_triggers(rec.frontmatter))
        lines.append(
            f"| {row_id} | {rec.name} | {_status_of(rec.frontmatter)} | {triggers} | "
            f"{_legacy_dash(rec.frontmatter, 'sensitive_data_class')} | "
            f"{_legacy_dash(rec.frontmatter, 'portability_tier')} | "
            f"{u.last_activated_display} | {u.usage} |"
        )
    lines.append("")

    # Powers table
    lines.append("## Powers (~/.kiro/powers/installed/)")
    lines.append("")
    lines.append("| Row ID | Name | Status | Type | Sensitivity | Portability | Last Activated | Usage |")
    lines.append("|--------|------|--------|------|-------------|-------------|----------------|-------|")
    for i, rec in enumerate(powers, start=1):
        u = usage_by_key[(rec.kind, rec.name)]
        row_id = f"K-P{i}"
        lines.append(
            f"| {row_id} | {rec.name} | {_status_of(rec.frontmatter)} | {_power_type(rec)} | "
            f"{_legacy_dash(rec.frontmatter, 'sensitive_data_class')} | "
            f"{_legacy_dash(rec.frontmatter, 'portability_tier')} | "
            f"{u.last_activated_display} | {u.usage} |"
        )
    lines.append("")

    # Staleness section
    lines.extend(_render_staleness_section(assets, usage_by_key, activation_log, now))

    return "\n".join(lines) + "\n"


def _render_staleness_section(
    assets: list[AssetRecord],
    usage_by_key: dict[tuple[str, str], _UsageInfo],
    activation_log: list[dict[str, Any]],
    now: datetime,
) -> list[str]:
    """Build the three-bullet Staleness block."""
    skills = sorted([a for a in assets if a.kind == "skill"], key=lambda r: r.name)
    powers = sorted([a for a in assets if a.kind == "power"], key=lambda r: r.name)
    all_assets = skills + powers

    # Row-id lookup.
    row_ids: dict[tuple[str, str], str] = {}
    for i, rec in enumerate(skills, start=1):
        row_ids[(rec.kind, rec.name)] = f"K-S{i}"
    for i, rec in enumerate(powers, start=1):
        row_ids[(rec.kind, rec.name)] = f"K-P{i}"

    unused: list[str] = []
    stale: list[str] = []
    for rec in all_assets:
        u = usage_by_key[(rec.kind, rec.name)]
        rid = row_ids[(rec.kind, rec.name)]
        if u.usage == "unused":
            unused.append(rid)
        elif u.usage == "stale":
            stale.append(rid)

    # Candidates for next pruning review: legacy + created ≥14 days ago + not activated.
    # For legacy rows the `created_at` field is absent by definition, so we use
    # the file mtime as the creation proxy (design accepts this per §Pilot
    # procedure — legacy assets predate this system's created_at tracking).
    fourteen_days_ago = now - timedelta(days=14)
    candidates: list[str] = []
    for rec in all_assets:
        status = rec.frontmatter.get("status", "legacy")
        if status != "legacy":
            continue
        u = usage_by_key[(rec.kind, rec.name)]
        if u.ever_activated:
            continue
        mtime_dt = datetime.fromtimestamp(rec.mtime).astimezone()
        if _is_after(fourteen_days_ago, mtime_dt):
            # mtime is older than 14 days ago → candidate.
            candidates.append(row_ids[(rec.kind, rec.name)])

    lines: list[str] = []
    lines.append("## Staleness")
    lines.append("")
    lines.append(f"- **Unused (never activated)**: {_joined_or_none(unused)}")
    lines.append(f"- **Stale (activations exist but none in last 30 days)**: {_joined_or_none(stale)}")
    lines.append(f"- **Candidates for next pruning review**: {_joined_or_none(candidates)}")
    return lines


def _joined_or_none(ids: list[str]) -> str:
    return ", ".join(ids) if ids else "(none)"


def _escape_pipes(s: str) -> str:
    return s.replace("|", "\\|")


def _iso_with_tz(dt: datetime) -> str:
    """Produce an ISO 8601 string with timezone, matching baseline convention."""
    # Match Group 1 style: YYYY-MM-DDTHH:MM:SS±HHMM (no colon in offset).
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


def _is_after(a: datetime, b: datetime) -> bool:
    """Compare two datetimes safely whether or not tzinfo is present."""
    if a.tzinfo is None and b.tzinfo is not None:
        a = a.replace(tzinfo=b.tzinfo)
    elif b.tzinfo is None and a.tzinfo is not None:
        b = b.replace(tzinfo=a.tzinfo)
    return a > b


# ----------------------------------------------------------------------------
# Task 2.5 — CLI refresh
# ----------------------------------------------------------------------------


def refresh() -> tuple[Path, str]:
    """Re-walk the filesystem, re-read the log, rewrite inventory.md."""
    walk = walk_installed()
    log = read_activation_log()
    md = render_inventory(walk.assets, log)
    INVENTORY_DIR.mkdir(parents=True, exist_ok=True)
    INVENTORY_MD.write_text(md, encoding="utf-8")
    return INVENTORY_MD, md


def _cli(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] not in ("refresh", "hash", "validate"):
        print(
            "usage: python3 inventory.py refresh\n"
            "       python3 inventory.py hash      # print input-state hash only\n"
            "       python3 inventory.py validate  # smoke-test parser on live assets",
            file=sys.stderr,
        )
        return 2
    cmd = argv[1]
    if cmd == "refresh":
        path, md = refresh()
        print(f"wrote {path}")
        print(f"{len(md.splitlines())} lines, {len(md)} bytes")
        return 0
    if cmd == "hash":
        walk = walk_installed()
        print(compute_input_state_hash(walk.assets))
        return 0
    if cmd == "validate":
        walk = walk_installed()
        errors = 0
        for rec in walk.assets:
            full_text = f"---\n{rec.raw_frontmatter_text}---\n{rec.body_text}"
            parsed = parse_frontmatter(full_text)
            if isinstance(parsed, ParseError):
                print(f"[PARSE-ERROR] {rec.rel_path}: {parsed.violation}")
                errors += 1
                continue
            violation = validate_frontmatter(parsed.frontmatter, kind=rec.kind)
            if violation:
                print(f"[SCHEMA-ERROR] {rec.rel_path}: {violation}")
                errors += 1
            else:
                print(f"[OK] {rec.rel_path} (status={parsed.frontmatter.get('status', 'legacy')})")
        if errors:
            print(f"\n{errors} error(s)", file=sys.stderr)
            return 1
        print(f"\n{len(walk.assets)} asset(s) OK")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))
