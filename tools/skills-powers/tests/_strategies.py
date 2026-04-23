"""
Shared hypothesis strategies for Group 8 property-based tests.

Consolidated generators used across the NEW property tests (Properties 1, 3,
5, 6, 7, 12). Existing per-module strategies in test_routing_properties.py,
test_pruning_properties.py, and test_safe_creation_properties.py are left in
place — the minimal-refactor stance is per Group 8.2 spec.

Strategies here:

  gen_asset_name         — lowercase-dash-only directory-safe names.
  gen_skill_frontmatter  — frontmatter dicts (legacy or current) that round-
                           trip cleanly through inventory.parse/serialize.
  gen_power_frontmatter  — same shape for powers.
  gen_skill_body         — markdown bodies with variable Platform_Bound-
                           indicator token density (Property 4 + 6 + 7).
  gen_valid_skill_file   — (frontmatter, body) → well-formed SKILL.md text.
  gen_valid_power_file   — same for POWER.md.
  gen_malformed_skill_file — intentionally broken content for Property 7.
  gen_filesystem_state   — list of (kind, name, frontmatter, body) for
                           Property 1 + 5. Caller materializes to disk.
  gen_activation_log     — list of activation-log row dicts for Property 12.
  gen_sensitivity_tuple  — (sensitive_data_class, status, output_path_kind)
                           for Property 3.

Every strategy is deterministic given a seed. None of them touch the real
filesystem — materialization is the caller's job.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from hypothesis import strategies as st


# ----------------------------------------------------------------------------
# Asset names
# ----------------------------------------------------------------------------

_name_char = st.sampled_from("abcdefghijklmnopqrstuvwxyz0123456789-")

gen_asset_name = st.text(alphabet=_name_char, min_size=3, max_size=24).filter(
    lambda s: s[0].isalpha() and not s.endswith("-") and "--" not in s
)


# ----------------------------------------------------------------------------
# Sensitivity / portability enums
# ----------------------------------------------------------------------------

_SENSITIVITY_CLASSES = (
    "Public",
    "Amazon_Internal",
    "Amazon_Confidential",
    "Personal_PII",
)
_PORTABILITY_TIERS = ("Cold_Start_Safe", "Platform_Bound")
_STATUSES = ("legacy", "current")  # retired excluded from generators


gen_sensitivity = st.sampled_from(_SENSITIVITY_CLASSES)
gen_portability = st.sampled_from(_PORTABILITY_TIERS)
gen_status = st.sampled_from(_STATUSES)


# ----------------------------------------------------------------------------
# Trigger-phrase words & descriptions
# ----------------------------------------------------------------------------

_trigger_word = st.sampled_from(
    [
        "sync",
        "push",
        "pull",
        "build",
        "deploy",
        "review",
        "audit",
        "analyze",
        "callout",
        "market",
        "weekly",
        "chart",
        "dashboard",
        "wiki",
        "document",
        "coach",
        "growth",
        "career",
        "retrospective",
        "hook",
        "skill",
        "power",
        "bridge",
        "portable",
        "agent",
        "flow",
        "kata",
    ]
)


@st.composite
def _trigger_list_text(draw):
    """Produce 'Triggers on w1, w2, w3' style clause."""
    words = draw(st.lists(_trigger_word, min_size=1, max_size=5, unique=True))
    return "Triggers on " + ", ".join(words) + "."


@st.composite
def gen_description(draw):
    """Short prose ending in the triggers clause (skills-style)."""
    head = " ".join(draw(st.lists(_trigger_word, min_size=2, max_size=4)))
    # Capitalize first letter for aesthetics only; parser doesn't care.
    head = head[0].upper() + head[1:] if head else "Do stuff"
    tail = draw(_trigger_list_text())
    return f"{head}. {tail}"


# ----------------------------------------------------------------------------
# Frontmatter generators
# ----------------------------------------------------------------------------


def _fixed_iso_ts(offset_minutes: int = 0) -> str:
    base = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    dt = base + timedelta(minutes=offset_minutes)
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


@st.composite
def gen_skill_frontmatter(draw, *, force_status: str | None = None):
    """
    A frontmatter dict for a SKILL.md, with enough fields to round-trip.

    If status is "current" the full extended schema is populated. Legacy
    skills get minimal {name, description} only.

    We deliberately avoid characters that are YAML-problematic (colons in
    unquoted strings, leading dashes, tab indents) because we want the
    frontmatter to round-trip cleanly. Property 7 (malformed-file) uses a
    different generator.
    """
    status = force_status or draw(gen_status)
    name = draw(gen_asset_name)
    description = draw(gen_description())
    fm: dict[str, Any] = {
        "name": name,
        "description": description,
    }
    if status == "current":
        sensitivity = draw(gen_sensitivity)
        portability = draw(gen_portability)
        fm["status"] = "current"
        fm["sensitive_data_class"] = sensitivity
        fm["portability_tier"] = portability
        fm["created_at"] = _fixed_iso_ts(draw(st.integers(min_value=0, max_value=9_000)))
        fm["last_validated"] = _fixed_iso_ts(
            draw(st.integers(min_value=0, max_value=9_000))
        )
        if portability == "Platform_Bound":
            fm["platform_bound_dependencies"] = [
                {"kind": "script", "id": f"scripts/{name}.sh"}
            ]
    return fm


@st.composite
def gen_power_frontmatter(draw, *, force_status: str | None = None):
    """Same shape for POWER.md. Powers have additional minimal-required fields."""
    status = force_status or draw(gen_status)
    name = draw(gen_asset_name)
    fm: dict[str, Any] = {
        "name": name,
        "displayName": name.replace("-", " ").title(),
        "description": draw(gen_description()),
        "keywords": draw(st.lists(_trigger_word, min_size=1, max_size=5, unique=True)),
        "author": "Test",
    }
    if status == "current":
        fm["status"] = "current"
        fm["sensitive_data_class"] = draw(gen_sensitivity)
        fm["portability_tier"] = draw(gen_portability)
        fm["created_at"] = _fixed_iso_ts(draw(st.integers(min_value=0, max_value=9_000)))
        fm["last_validated"] = _fixed_iso_ts(
            draw(st.integers(min_value=0, max_value=9_000))
        )
    return fm


# ----------------------------------------------------------------------------
# Body generators
# ----------------------------------------------------------------------------

# Platform_Bound indicator tokens per design §Portability Tier Rules. We'll
# produce bodies with varying density so Property 6 (roundtrip) and Property
# 7 (non-silent-rewrite) both exercise realistic content shapes.

_platform_bound_tokens = st.sampled_from(
    [
        "mcp_ai_community_slack_mcp_post_message",
        "mcp_duckdb_execute_query",
        "discloseContext(name='bridge-sync')",
        "kiroPowers activate(powerName='flow-gen')",
        "scripts/sync.sh",
        "~/shared/tools/some-tool.py",
        "am-auto.kiro.hook",
        "ps.v_weekly",
        "signals.trending",
    ]
)

_prose_word = st.sampled_from(
    [
        "This",
        "skill",
        "does",
        "things",
        "for",
        "the",
        "user",
        "when",
        "triggered",
        "properly",
        "handles",
        "failures",
        "safely",
        "logs",
        "activity",
        "review",
        "output",
    ]
)


@st.composite
def gen_skill_body(draw, *, token_density: float | None = None):
    """
    Markdown body with a tunable density of platform-bound indicator tokens.

    token_density ∈ [0, 1] — if None, randomly drawn per example.

    Produces short prose with section headers, plain paragraphs, and some
    token references. Output is UTF-8 safe with no YAML-confusing content.
    """
    if token_density is None:
        token_density = draw(st.floats(min_value=0.0, max_value=1.0))
    paragraphs: list[str] = []
    n_sections = draw(st.integers(min_value=1, max_value=3))
    for i in range(n_sections):
        heading = "# Section " + str(i + 1) if i == 0 else "## Section " + str(i + 1)
        words = draw(st.lists(_prose_word, min_size=3, max_size=12))
        # Inject tokens based on density.
        if draw(st.floats(min_value=0.0, max_value=1.0)) < token_density:
            words.append(draw(_platform_bound_tokens))
        paragraphs.append(heading + "\n\n" + " ".join(words) + ".")
    return "\n\n".join(paragraphs) + "\n"


# ----------------------------------------------------------------------------
# Full file generators
# ----------------------------------------------------------------------------


def _render_frontmatter(fm: dict[str, Any]) -> str:
    """
    Minimal deterministic YAML emitter for test fixtures.

    We avoid PyYAML here to keep the generator zero-dependency-on-parser so a
    malformed-content generator can't accidentally emit malformed YAML that
    PyYAML massages into validity. The inventory parser still parses these.
    """
    lines: list[str] = []
    for key, value in fm.items():
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            elif all(isinstance(v, str) for v in value):
                lines.append(f"{key}:")
                for v in value:
                    lines.append(f"  - {_yaml_quote(v)}")
            else:
                # list of dicts (e.g., platform_bound_dependencies)
                lines.append(f"{key}:")
                for entry in value:
                    if isinstance(entry, dict):
                        keys = list(entry.keys())
                        if keys:
                            first_k = keys[0]
                            lines.append(f"  - {first_k}: {_yaml_quote(entry[first_k])}")
                            for k in keys[1:]:
                                lines.append(f"    {k}: {_yaml_quote(entry[k])}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif value is None:
            lines.append(f"{key}: null")
        else:
            lines.append(f"{key}: {_yaml_quote(value)}")
    return "\n".join(lines) + "\n"


def _yaml_quote(value: Any) -> str:
    """Double-quote YAML-unfriendly strings; pass-through simple scalars."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    needs_quote = any(ch in s for ch in (":", "#", "\"", "'", "\n")) or s.strip() != s
    if needs_quote:
        escaped = s.replace("\\", "\\\\").replace("\"", "\\\"")
        return f"\"{escaped}\""
    return s


@st.composite
def gen_valid_skill_file(draw, *, force_status: str | None = None):
    """Return (frontmatter_dict, body, full_text) for a valid SKILL.md."""
    fm = draw(gen_skill_frontmatter(force_status=force_status))
    body = draw(gen_skill_body())
    full = "---\n" + _render_frontmatter(fm) + "---\n" + body
    return fm, body, full


@st.composite
def gen_valid_power_file(draw, *, force_status: str | None = None):
    """Return (frontmatter_dict, body, full_text) for a valid POWER.md."""
    fm = draw(gen_power_frontmatter(force_status=force_status))
    body = draw(gen_skill_body())
    full = "---\n" + _render_frontmatter(fm) + "---\n" + body
    return fm, body, full


# ----------------------------------------------------------------------------
# Malformed-file generator (Property 7)
# ----------------------------------------------------------------------------

_malformed_shape = st.sampled_from(
    [
        "missing-frontmatter",
        "unclosed-fence",
        "malformed-yaml-colons",
        "tab-indented-yaml",
        "frontmatter-is-list",
        "frontmatter-is-scalar",
        "current-missing-required",
        "bad-unclosed-quote",
    ]
)


@st.composite
def gen_malformed_skill_file(draw):
    """
    Produce a (shape, text) pair where text will fail parsing OR fail
    validation. Property 7 asserts the validator reports the error and leaves
    the file bytes unchanged.
    """
    shape = draw(_malformed_shape)
    if shape == "missing-frontmatter":
        text = "# body only, no frontmatter\n\nprose here\n"
    elif shape == "unclosed-fence":
        text = "---\nname: broken\ndescription: d. Triggers on x.\n# body never closed\n"
    elif shape == "malformed-yaml-colons":
        text = "---\nname: broken\n  bad: :: :\n---\n# body\n"
    elif shape == "tab-indented-yaml":
        # YAML forbids tabs as indentation. PyYAML rejects.
        text = "---\nname: broken\nnested:\n\tsubkey: value\n---\n# body\n"
    elif shape == "frontmatter-is-list":
        text = "---\n- one\n- two\n---\n# body\n"
    elif shape == "frontmatter-is-scalar":
        text = "---\njust a string\n---\n# body\n"
    elif shape == "current-missing-required":
        name = draw(gen_asset_name)
        text = (
            "---\n"
            f"name: {name}\n"
            f"description: d. Triggers on {name}.\n"
            "status: current\n"
            "---\n# body\n"
        )
    elif shape == "bad-unclosed-quote":
        text = (
            '---\n'
            'name: broken\n'
            'description: "unclosed quote\n'
            '---\n# body\n'
        )
    else:  # pragma: no cover
        raise ValueError(f"unknown malformed shape: {shape}")
    return shape, text


# ----------------------------------------------------------------------------
# Filesystem state generator (Property 1, 5)
# ----------------------------------------------------------------------------


@st.composite
def gen_filesystem_state(draw, *, min_size: int = 0, max_size: int = 20):
    """
    A list of asset tuples describing a filesystem to materialize:
        [(kind, name, frontmatter, body), ...]

    Names are unique within each kind. Mix of legacy + current statuses.
    """
    n = draw(st.integers(min_value=min_size, max_value=max_size))
    if n == 0:
        return []
    assets: list[tuple[str, str, dict[str, Any], str]] = []
    used_skill_names: set[str] = set()
    used_power_names: set[str] = set()
    for _ in range(n):
        kind = draw(st.sampled_from(["skill", "power"]))
        if kind == "skill":
            name = draw(gen_asset_name)
            if name in used_skill_names:
                continue
            used_skill_names.add(name)
            fm, body, _ = draw(gen_valid_skill_file())
            fm["name"] = name  # align directory name
            assets.append((kind, name, fm, body))
        else:
            name = draw(gen_asset_name)
            if name in used_power_names:
                continue
            used_power_names.add(name)
            fm, body, _ = draw(gen_valid_power_file())
            fm["name"] = name
            assets.append((kind, name, fm, body))
    return assets


# ----------------------------------------------------------------------------
# Activation log generator (Property 12)
# ----------------------------------------------------------------------------

_EVENT_KINDS = ("activated", "missed-by-feedback", "correction", "created", "pruned")


@st.composite
def gen_log_event_call(draw):
    """
    Produce one (event_kind, kwargs) tuple describing a logger function call.
    Caller invokes the matching append_* function.

    Returns one of:
        ("activated", {kind, name, request_summary})
        ("missed_by_feedback", {kind, name, feedback_text})
        ("correction", {target_ts, reason})
        ("created", {kind, name, subtype, overlap_check_ref})
        ("pruned", {kind, name, archive_path})
    """
    event = draw(st.sampled_from(_EVENT_KINDS))
    kind = draw(st.sampled_from(["skill", "power"]))
    name = draw(gen_asset_name)
    if event == "activated":
        return (
            "activated",
            {
                "kind": kind,
                "name": name,
                "request_summary": draw(
                    st.text(min_size=0, max_size=100, alphabet=st.characters(
                        min_codepoint=32, max_codepoint=126
                    ))
                ),
            },
        )
    if event == "missed-by-feedback":
        return (
            "missed_by_feedback",
            {
                "kind": kind,
                "name": name,
                "feedback_text": draw(
                    st.text(min_size=1, max_size=150, alphabet=st.characters(
                        min_codepoint=32, max_codepoint=126
                    ))
                ),
            },
        )
    if event == "correction":
        return (
            "correction",
            {
                "target_ts": _fixed_iso_ts(draw(st.integers(min_value=0, max_value=1000))),
                "reason": draw(
                    st.text(min_size=1, max_size=150, alphabet=st.characters(
                        min_codepoint=32, max_codepoint=126
                    ))
                ),
            },
        )
    if event == "created":
        subtype = draw(st.sampled_from(["created", "classified"]))
        overlap_ref = None if subtype == "classified" else f"~/.kiro/{kind}s/{name}/overlap-check.json"
        return (
            "created",
            {
                "kind": kind,
                "name": name,
                "subtype": subtype,
                "overlap_check_ref": overlap_ref,
            },
        )
    # pruned
    return (
        "pruned",
        {
            "kind": kind,
            "name": name,
            "archive_path": f"~/shared/wiki/agent-created/archive/skills-powers-pruned-2026-04-22/{name}/",
        },
    )


gen_log_event_sequence = st.lists(gen_log_event_call(), min_size=0, max_size=20)


# ----------------------------------------------------------------------------
# Sensitivity / path generators (Property 3)
# ----------------------------------------------------------------------------


@st.composite
def gen_path_kind(draw):
    """
    A symbolic path kind that the test materializes to an absolute path
    against the sandbox HOME.

    Returns one of:
      "skills", "powers", "context-body", "context-protocols",
      "steering", "agent-bridge-synced", "outside-home", "tmp",
    """
    return draw(
        st.sampled_from(
            [
                "skills",
                "powers",
                "context-body",
                "context-protocols",
                "steering",
                "agent-bridge-synced",
                "outside-home",
                "tmp",
            ]
        )
    )


@st.composite
def gen_sensitivity_tuple(draw):
    """
    (sensitivity_class, status, path_kind) tuple for Property 3.
    path_kind is a symbolic key the test resolves against the sandbox HOME.
    """
    return (draw(gen_sensitivity), draw(gen_status), draw(gen_path_kind()))
