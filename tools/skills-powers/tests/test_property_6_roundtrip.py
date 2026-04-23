"""
Property 6: ROUND-TRIP

# Feature: skills-powers-adoption, Property 6: parse(serialize(parse(F))) ==
# parse(F) and body bytes preserved.

For any valid SKILL.md / POWER.md full-file text:
  - parse → serialize → parse produces the SAME frontmatter dict.
  - body bytes are preserved exactly through the roundtrip.
  - validators.roundtrip_check() reports valid=True, frontmatter_roundtrip_equal=True,
    body_byte_identical=True, file_unchanged=True.

Edge cases included:
  - legacy-only minimal frontmatter
  - current extended frontmatter with Platform_Bound + platform_bound_dependencies
  - empty body
  - unicode body
  - list-typed fields
  - nested-dict entries (platform_bound_dependencies)

Validates: Requirements 9.1, 9.2, 9.3
"""

from __future__ import annotations

import importlib
import shutil
import sys
import tempfile
from pathlib import Path

_PKG_DIR = Path(__file__).resolve().parent.parent
_TEST_DIR = Path(__file__).resolve().parent
for p in (_PKG_DIR, _TEST_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

import _strategies as gen


@pytest.fixture
def sandbox_home(monkeypatch):
    """Isolated HOME so the validator's roundtrip_check sees only our files."""
    tmp = tempfile.mkdtemp(prefix="sp_p6_roundtrip_")
    monkeypatch.setenv("HOME", tmp)
    (Path(tmp) / ".kiro" / "skills").mkdir(parents=True)
    (Path(tmp) / ".kiro" / "powers" / "installed").mkdir(parents=True)
    (Path(tmp) / "shared" / "context" / "skills-powers").mkdir(parents=True)
    import inventory
    import validators

    importlib.reload(inventory)
    importlib.reload(validators)
    yield Path(tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    importlib.reload(inventory)
    importlib.reload(validators)


def _write_skill(sandbox: Path, name: str, text: str) -> Path:
    d = sandbox / ".kiro" / "skills" / name
    d.mkdir(parents=True, exist_ok=True)
    path = d / "SKILL.md"
    path.write_text(text, encoding="utf-8")
    return path


def _write_power(sandbox: Path, name: str, text: str) -> Path:
    d = sandbox / ".kiro" / "powers" / "installed" / name
    d.mkdir(parents=True, exist_ok=True)
    path = d / "POWER.md"
    path.write_text(text, encoding="utf-8")
    return path


# ----------------------------------------------------------------------------
# Property 6 — universal roundtrip over random skills
# ----------------------------------------------------------------------------


# Validates: Requirements 9.1, 9.2, 9.3
@given(skill=gen.gen_valid_skill_file())
@settings(
    max_examples=150,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
)
def test_property_6_skill_roundtrip(sandbox_home, skill):
    """Every random valid SKILL.md roundtrips cleanly."""
    import validators as vd

    fm, body, full_text = skill
    name = fm["name"]
    path = _write_skill(sandbox_home, name, full_text)

    result = vd.roundtrip_check(path)

    assert result["valid"] is True, (
        f"roundtrip reported invalid for {name!r}: {result['violations']}"
    )
    assert result["frontmatter_roundtrip_equal"] is True, (
        f"frontmatter changed through roundtrip for {name!r}"
    )
    assert result["body_byte_identical"] is True, (
        f"body bytes changed through roundtrip for {name!r}"
    )
    assert result["file_unchanged"] is True, (
        f"validator modified file on disk for {name!r}"
    )


# Validates: Requirements 9.1, 9.2, 9.3 — powers variant.
@given(power=gen.gen_valid_power_file())
@settings(
    max_examples=150,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
)
def test_property_6_power_roundtrip(sandbox_home, power):
    """Every random valid POWER.md roundtrips cleanly."""
    import validators as vd

    fm, body, full_text = power
    name = fm["name"]
    path = _write_power(sandbox_home, name, full_text)

    result = vd.roundtrip_check(path)

    assert result["valid"] is True, (
        f"roundtrip reported invalid for power {name!r}: {result['violations']}"
    )
    assert result["frontmatter_roundtrip_equal"] is True
    assert result["body_byte_identical"] is True
    assert result["file_unchanged"] is True


# ----------------------------------------------------------------------------
# Property 6 — focused edge cases (not hypothesis-driven)
# ----------------------------------------------------------------------------


def test_property_6_empty_body(sandbox_home):
    """A file with no body content after the closing fence still roundtrips."""
    import validators as vd

    text = (
        "---\n"
        "name: empty-body\n"
        "description: d. Triggers on x.\n"
        "---\n"
    )
    path = _write_skill(sandbox_home, "empty-body", text)
    result = vd.roundtrip_check(path)
    assert result["valid"] is True
    assert result["body_byte_identical"] is True


def test_property_6_unicode_in_description(sandbox_home):
    """Unicode chars in description round-trip byte-identically through YAML."""
    import validators as vd

    text = (
        "---\n"
        "name: unicode-desc\n"
        'description: "Héllo — wörld … Triggers on unicode."\n'
        "---\n"
        "# Unicode body: café 日本語 🚀\n"
    )
    path = _write_skill(sandbox_home, "unicode-desc", text)
    result = vd.roundtrip_check(path)
    assert result["valid"] is True, result["violations"]
    assert result["frontmatter_roundtrip_equal"] is True
    assert result["body_byte_identical"] is True


def test_property_6_list_typed_field(sandbox_home):
    """A list-typed field (keywords on a power) survives roundtrip."""
    import validators as vd

    text = (
        "---\n"
        'name: "list-power"\n'
        'displayName: "List Power"\n'
        'description: "d. Triggers on x."\n'
        "keywords:\n"
        "  - one\n"
        "  - two\n"
        "  - three\n"
        'author: "Test"\n'
        "---\n"
        "# body\n"
    )
    path = _write_power(sandbox_home, "list-power", text)
    result = vd.roundtrip_check(path)
    assert result["valid"] is True, result["violations"]
    assert result["frontmatter_roundtrip_equal"] is True


def test_property_6_nested_dict_entries(sandbox_home):
    """platform_bound_dependencies is a list of dicts — must survive roundtrip."""
    import validators as vd

    text = (
        "---\n"
        "name: nested\n"
        "description: d. Triggers on x.\n"
        "status: current\n"
        "sensitive_data_class: Amazon_Internal\n"
        "portability_tier: Platform_Bound\n"
        "platform_bound_dependencies:\n"
        "  - kind: script\n"
        "    id: scripts/nested.sh\n"
        "  - kind: mcp_tool\n"
        "    id: mcp_ai_community_slack_mcp_post_message\n"
        'created_at: "2026-04-22T00:00:00+0000"\n'
        'last_validated: "2026-04-22T00:00:00+0000"\n'
        "---\n"
        "# body with nested frontmatter test\n"
    )
    path = _write_skill(sandbox_home, "nested", text)
    result = vd.roundtrip_check(path)
    assert result["valid"] is True, result["violations"]
    assert result["frontmatter_roundtrip_equal"] is True
    assert result["body_byte_identical"] is True


def test_property_6_long_body_with_platform_tokens(sandbox_home):
    """A realistic long body with Platform_Bound indicator tokens roundtrips."""
    import validators as vd

    body = (
        "# Usage\n\n"
        "Invoke via `discloseContext(name='bridge-sync')`.\n\n"
        "## Implementation\n\n"
        "Uses `mcp_ai_community_slack_mcp_post_message` and calls "
        "`scripts/sync.sh`. Reads from `ps.v_weekly` table. Hooks into "
        "`am-auto.kiro.hook`.\n"
    )
    text = (
        "---\n"
        "name: long-body\n"
        "description: d. Triggers on long.\n"
        "status: current\n"
        "sensitive_data_class: Amazon_Internal\n"
        "portability_tier: Platform_Bound\n"
        "platform_bound_dependencies:\n"
        "  - kind: script\n"
        "    id: scripts/sync.sh\n"
        'created_at: "2026-04-22T00:00:00+0000"\n'
        'last_validated: "2026-04-22T00:00:00+0000"\n'
        "---\n"
    ) + body
    path = _write_skill(sandbox_home, "long-body", text)
    result = vd.roundtrip_check(path)
    assert result["valid"] is True, result["violations"]
    assert result["body_byte_identical"] is True
