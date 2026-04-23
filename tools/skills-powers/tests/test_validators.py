"""
Unit tests for validators.py — Task 7.7 of the skills-powers-adoption spec.

One test (or small set) per validator, covering the specific examples called
out in design §Testing Strategy:

  - roundtrip_check            — happy path + manually-mutated counterexample.
  - format_compliance_check    — malformed YAML returns valid=False, file
                                 unchanged.
  - sensitivity_path_check     — status=legacy bypass; Amazon_Confidential in
                                 bridge-synced path errors.
  - portability_report         — Cold_Start_Safe body with mcp_* tokens → flag
                                 cold_start_safe_inconsistency=True, no
                                 rejection.
  - schema_check               — legacy minimal ok, current missing fields
                                 errors.
  - wrapper_skill_check        — single invokeSubAgent → wrapper_detected
                                 =True; multi-agent orchestration → False.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Make sibling modules importable.
_PKG_DIR = Path(__file__).resolve().parent.parent
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

import importlib

import inventory
import validators  # noqa: E402


# ----------------------------------------------------------------------------
# Sandbox fixture — isolate HOME so sensitivity_path_check sees our synthetic
# bridge-sync list instead of the real one.
# ----------------------------------------------------------------------------


@pytest.fixture
def sandbox_home(monkeypatch, tmp_path):
    """Create a fresh HOME sandbox and reload inventory + validators."""
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / ".kiro" / "skills").mkdir(parents=True)
    (tmp_path / ".kiro" / "powers" / "installed").mkdir(parents=True)
    (tmp_path / ".kiro" / "steering").mkdir(parents=True)
    (tmp_path / "shared" / "context" / "body").mkdir(parents=True)
    (tmp_path / "shared" / "context" / "protocols").mkdir(parents=True)
    importlib.reload(inventory)
    importlib.reload(validators)
    yield tmp_path
    # Restore module constants for the next test.
    importlib.reload(inventory)
    importlib.reload(validators)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------


def _write_skill(
    path: Path,
    *,
    fm: dict,
    body: str = "# Title\n\nSome content.\n",
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = inventory.serialize_frontmatter(fm, body)
    path.write_text(content, encoding="utf-8")


# ============================================================================
# 7.1 — roundtrip_check
# ============================================================================


def test_roundtrip_happy_path(tmp_path):
    p = tmp_path / "SKILL.md"
    _write_skill(
        p,
        fm={
            "name": "sample-skill",
            "description": "Does a thing. Triggers on thing, other thing.",
        },
    )
    result = validators.roundtrip_check(p)
    assert result["valid"] is True
    assert result["frontmatter_roundtrip_equal"] is True
    assert result["body_byte_identical"] is True
    assert result["file_unchanged"] is True
    assert result["violations"] == []


def test_roundtrip_missing_file(tmp_path):
    result = validators.roundtrip_check(tmp_path / "does-not-exist.md")
    assert result["valid"] is False
    assert any("file not found" in v for v in result["violations"])
    assert result["file_unchanged"] is True


def test_roundtrip_detects_unparseable_file(tmp_path):
    """A file that starts with `---` but has malformed YAML should be
    reported by roundtrip_check as a parse failure, file unchanged."""
    p = tmp_path / "SKILL.md"
    p.write_text(
        "---\nname: [unclosed\ndescription: x\n---\nbody\n", encoding="utf-8"
    )
    mtime_before = p.stat().st_mtime
    result = validators.roundtrip_check(p)
    assert result["valid"] is False
    assert result["file_unchanged"] is True
    assert p.stat().st_mtime == mtime_before


# ============================================================================
# 7.2 — format_compliance_check
# ============================================================================


def test_format_compliance_happy_legacy_skill(tmp_path):
    p = tmp_path / "SKILL.md"
    _write_skill(
        p,
        fm={
            "name": "legacy-skill",
            "description": "Legacy skill. Triggers on legacy.",
        },
    )
    result = validators.format_compliance_check(p)
    assert result["valid"] is True
    assert result["violations"] == []
    assert result["legacy_unknown_fields"] is None
    assert result["file_unchanged"] is True


def test_format_compliance_malformed_yaml_leaves_file_unchanged(tmp_path):
    p = tmp_path / "SKILL.md"
    original = "---\nname: [broken\nkey: value\n---\nbody here\n"
    p.write_text(original, encoding="utf-8")
    mtime_before = p.stat().st_mtime
    result = validators.format_compliance_check(p)
    assert result["valid"] is False
    assert any("parse failed" in v for v in result["violations"])
    assert result["file_unchanged"] is True
    # Verify byte-for-byte unchanged.
    assert p.read_text(encoding="utf-8") == original
    assert p.stat().st_mtime == mtime_before


def test_format_compliance_preserves_unknown_fields(tmp_path):
    p = tmp_path / "SKILL.md"
    _write_skill(
        p,
        fm={
            "name": "weird-skill",
            "description": "Weird skill. Triggers on weird.",
            "some_future_field": "value",
            "another_legacy_field": [1, 2, 3],
        },
    )
    result = validators.format_compliance_check(p)
    # status: legacy (default) + name + description → schema valid.
    assert result["valid"] is True
    assert result["legacy_unknown_fields"] is not None
    assert "some_future_field" in result["legacy_unknown_fields"]
    assert "another_legacy_field" in result["legacy_unknown_fields"]


def test_format_compliance_current_missing_required_fields(tmp_path):
    p = tmp_path / "SKILL.md"
    _write_skill(
        p,
        fm={
            "name": "incomplete-current",
            "description": "x. Triggers on x.",
            "status": "current",
        },
    )
    result = validators.format_compliance_check(p)
    assert result["valid"] is False
    assert any("missing required field" in v for v in result["violations"])


# ============================================================================
# 7.3 — sensitivity_path_check
# ============================================================================


def test_sensitivity_legacy_bypass(sandbox_home):
    fm = {"name": "legacy", "description": "x. Triggers on x.", "status": "legacy"}
    out_path = sandbox_home / ".kiro" / "skills" / "legacy" / "SKILL.md"
    result = validators.sensitivity_path_check(fm, out_path)
    assert result["valid"] is True
    assert result["skipped"] is True
    assert result["reason"] == "legacy asset grandfathered"


def test_sensitivity_implicit_legacy_bypass(sandbox_home):
    # No `status` field at all — treated as legacy per inventory.parse contract.
    fm = {"name": "legacy", "description": "x. Triggers on x."}
    out_path = sandbox_home / ".kiro" / "skills" / "legacy" / "SKILL.md"
    result = validators.sensitivity_path_check(fm, out_path)
    assert result["valid"] is True
    assert result["skipped"] is True


def test_sensitivity_amazon_confidential_in_kiro_skills_ok(sandbox_home):
    fm = {
        "name": "x",
        "status": "current",
        "sensitive_data_class": "Amazon_Confidential",
    }
    out_path = sandbox_home / ".kiro" / "skills" / "x" / "SKILL.md"
    result = validators.sensitivity_path_check(
        fm, out_path, agent_bridge_synced_paths=[]
    )
    assert result["valid"] is True
    assert result["sync_violation"] is False


def test_sensitivity_amazon_confidential_in_bridge_synced_errors(sandbox_home):
    fm = {
        "name": "x",
        "status": "current",
        "sensitive_data_class": "Amazon_Confidential",
    }
    synced = [sandbox_home / "shared" / "context" / "body"]
    out_path = sandbox_home / "shared" / "context" / "body" / "somewhere.md"
    result = validators.sensitivity_path_check(
        fm, out_path, agent_bridge_synced_paths=synced
    )
    assert result["valid"] is False
    assert result["sync_violation"] is True
    assert any("agent-bridge" in v for v in result["violations"])


def test_sensitivity_personal_pii_protocols_rejected(sandbox_home):
    fm = {
        "name": "x",
        "status": "current",
        "sensitive_data_class": "Personal_PII",
    }
    # protocols/ is under the synced set; plus the preference-rule is violated.
    synced = [sandbox_home / "shared" / "context" / "protocols"]
    out_path = sandbox_home / "shared" / "context" / "protocols" / "x.md"
    result = validators.sensitivity_path_check(
        fm, out_path, agent_bridge_synced_paths=synced
    )
    assert result["valid"] is False
    # Two violations: sync + prefer-body rule.
    assert result["sync_violation"] is True
    assert any("protocols" in v for v in result["violations"])


def test_sensitivity_public_allowed_anywhere(sandbox_home):
    fm = {
        "name": "x",
        "status": "current",
        "sensitive_data_class": "Public",
    }
    out_path = sandbox_home / "anywhere" / "x.md"
    result = validators.sensitivity_path_check(
        fm, out_path, agent_bridge_synced_paths=[sandbox_home / "anywhere"]
    )
    assert result["valid"] is True
    assert result["sync_violation"] is False


def test_sensitivity_default_up_when_missing(sandbox_home):
    """R3.5: for current assets, missing `sensitive_data_class` defaults to
    Amazon_Confidential and is enforced accordingly."""
    fm = {"name": "x", "status": "current"}
    out_path = sandbox_home / "random" / "place" / "SKILL.md"
    result = validators.sensitivity_path_check(
        fm, out_path, agent_bridge_synced_paths=[]
    )
    # The random/place/ directory is NOT in the Amazon_Confidential allowlist.
    assert result["sensitivity_class"] == "Amazon_Confidential"
    assert result["valid"] is False


# ============================================================================
# 7.4 — portability_report (advisory only)
# ============================================================================


def test_portability_cold_start_safe_with_mcp_tokens_flags_inconsistency(
    tmp_path,
):
    p = tmp_path / "SKILL.md"
    _write_skill(
        p,
        fm={
            "name": "x",
            "description": "x. Triggers on x.",
            "status": "current",
            "sensitive_data_class": "Public",
            "portability_tier": "Cold_Start_Safe",
            "created_at": "2026-04-22T01:00:00-07:00",
            "last_validated": "2026-04-22T01:00:00-07:00",
        },
        body=(
            "# Title\n"
            "\n"
            "Call mcp_ai_community_slack_mcp_post_message to post.\n"
            "Also uses discloseContext(name='x') and scripts/sync.sh.\n"
        ),
    )
    mtime_before = p.stat().st_mtime
    result = validators.portability_report(p)
    assert result["advisory"] is True
    assert result["declared_tier"] == "Cold_Start_Safe"
    assert result["cold_start_safe_inconsistency"] is True
    assert "mcp_tool" in result["findings"]
    assert "kiro_api" in result["findings"]
    assert "script_path" in result["findings"]
    assert result["file_unchanged"] is True
    # File must not have been touched.
    assert p.stat().st_mtime == mtime_before


def test_portability_platform_bound_cross_check(tmp_path):
    p = tmp_path / "SKILL.md"
    _write_skill(
        p,
        fm={
            "name": "x",
            "description": "x. Triggers on x.",
            "status": "current",
            "sensitive_data_class": "Amazon_Internal",
            "portability_tier": "Platform_Bound",
            "platform_bound_dependencies": [
                {"kind": "script", "id": "scripts/sync.sh"},
                {"kind": "mcp_tool", "id": "mcp_never_referenced"},
            ],
            "created_at": "2026-04-22T01:00:00-07:00",
            "last_validated": "2026-04-22T01:00:00-07:00",
        },
        body=(
            "# Title\n"
            "\n"
            "Uses scripts/sync.sh and mcp_ai_community_slack_mcp_post_message.\n"
        ),
    )
    result = validators.portability_report(p)
    assert result["advisory"] is True
    assert result["declared_tier"] == "Platform_Bound"
    # cold_start_safe_inconsistency is False (we're Platform_Bound).
    assert result["cold_start_safe_inconsistency"] is False
    cross = result["platform_bound_dependencies_cross_check"]
    # declared-but-unused includes mcp_never_referenced
    assert {"kind": "mcp_tool", "id": "mcp_never_referenced"} in cross[
        "declared_but_unused"
    ]
    # undeclared includes the slack MCP call.
    undeclared_ids = {d["id"] for d in cross["undeclared_tokens"]}
    assert any("mcp_ai_community_slack_mcp_post_message" in i for i in undeclared_ids)
    assert result["file_unchanged"] is True


def test_portability_accepts_inline_body(tmp_path):
    # body supplied explicitly; path can be anything (missing is fine if body given).
    result = validators.portability_report(
        tmp_path / "fake.md",
        body="references mcp_foo and scripts/x.sh",
    )
    assert result["advisory"] is True
    assert "mcp_tool" in result["findings"]
    assert "script_path" in result["findings"]


def test_portability_never_rejects_and_never_modifies(tmp_path):
    """Per design §Portability Tier Rules: the validator never blocks writes."""
    p = tmp_path / "SKILL.md"
    _write_skill(
        p,
        fm={
            "name": "x",
            "description": "x. Triggers on x.",
            "status": "current",
            "sensitive_data_class": "Public",
            "portability_tier": "Cold_Start_Safe",
            "created_at": "2026-04-22T01:00:00-07:00",
            "last_validated": "2026-04-22T01:00:00-07:00",
        },
        body="mcp_x mcp_y mcp_z references every platform-bound thing.\n",
    )
    original = p.read_text(encoding="utf-8")
    mtime_before = p.stat().st_mtime
    result = validators.portability_report(p)
    # Report was generated without rejecting.
    assert result["advisory"] is True
    assert result["cold_start_safe_inconsistency"] is True
    # File must be byte-identical and mtime untouched.
    assert p.read_text(encoding="utf-8") == original
    assert p.stat().st_mtime == mtime_before


# ============================================================================
# 7.5 — schema_check
# ============================================================================


def test_schema_legacy_skill_minimal_ok():
    fm = {"name": "x", "description": "x. Triggers on x."}
    result = validators.schema_check(fm, kind="skill")
    assert result["valid"] is True
    assert result["violation"] is None
    assert result["inferred_status"] == "legacy"
    assert result["status_gated"] is True


def test_schema_current_skill_missing_fields():
    fm = {
        "name": "x",
        "description": "x. Triggers on x.",
        "status": "current",
    }
    result = validators.schema_check(fm, kind="skill")
    assert result["valid"] is False
    assert result["violation"] is not None
    assert result["inferred_status"] == "current"


def test_schema_current_skill_complete():
    fm = {
        "name": "x",
        "description": "x. Triggers on x.",
        "status": "current",
        "sensitive_data_class": "Public",
        "portability_tier": "Cold_Start_Safe",
        "created_at": "2026-04-22T01:00:00-07:00",
        "last_validated": "2026-04-22T01:00:00-07:00",
    }
    result = validators.schema_check(fm, kind="skill")
    assert result["valid"] is True
    assert result["violation"] is None


def test_schema_legacy_power_minimal_ok():
    fm = {
        "name": "x",
        "displayName": "X",
        "description": "y",
        "keywords": ["a", "b"],
        "author": "me",
    }
    result = validators.schema_check(fm, kind="power")
    assert result["valid"] is True
    assert result["inferred_status"] == "legacy"


def test_schema_retired_accepts_minimal():
    fm = {
        "name": "x",
        "description": "x. Triggers on x.",
        "status": "retired",
    }
    # validate_frontmatter treats retired as minimal; but our implementation
    # only has 3 status buckets. Confirm retired is not rejected for status.
    result = validators.schema_check(fm, kind="skill")
    # Accept either valid or a content-specific violation (but NOT an unknown-
    # status violation).
    if not result["valid"]:
        assert "status" not in (result["violation"] or "") or "unknown" not in (
            result["violation"] or ""
        )


# ============================================================================
# 7.6 — wrapper_skill_check
# ============================================================================


def test_wrapper_single_invoke_is_wrapper():
    body = """# Some Skill

## Instructions

1. Call invokeSubAgent(name="wiki-writer") with the draft.
2. Return the result.
"""
    result = validators.wrapper_skill_check(body)
    assert result["wrapper_detected"] is True
    assert result["subagent_count"] == 1
    assert result["subagent_names"] == ["wiki-writer"]
    assert result["other_tool_calls"] == []
    assert result["rejection_reason"] is not None
    assert "R10.4" in result["rejection_reason"]


def test_wrapper_multi_subagent_orchestration_not_wrapper():
    body = """# Pipeline Skill

1. invokeSubAgent(name="analyst") produces analysis.
2. invokeSubAgent(name="writer") drafts the output.
3. invokeSubAgent(name="reviewer") reviews.
"""
    result = validators.wrapper_skill_check(body)
    assert result["wrapper_detected"] is False
    assert result["subagent_count"] == 3
    assert set(result["subagent_names"]) == {"analyst", "writer", "reviewer"}
    assert result["rejection_reason"] is None


def test_wrapper_single_invoke_plus_other_tools_not_wrapper():
    body = """# Skill with orchestration

1. Call mcp_foo_bar_baz(arg=1) to fetch context.
2. Then invokeSubAgent(name="specialist") with the context.
3. Call discloseContext(name="follow-up").
"""
    result = validators.wrapper_skill_check(body)
    assert result["wrapper_detected"] is False
    assert result["subagent_count"] == 1
    # other_tool_calls captures both mcp_foo_bar_baz(...) and discloseContext(...)
    assert any("discloseContext" in t for t in result["other_tool_calls"])
    assert any("mcp_foo_bar_baz" in t for t in result["other_tool_calls"])
    assert result["rejection_reason"] is None


def test_wrapper_no_invokes_at_all_not_wrapper():
    body = """# Pure prose skill

Describes how to write a document without any tool invocations.
"""
    result = validators.wrapper_skill_check(body)
    assert result["wrapper_detected"] is False
    assert result["subagent_count"] == 0
    assert result["rejection_reason"] is None


def test_wrapper_non_string_body_raises():
    with pytest.raises(TypeError):
        validators.wrapper_skill_check(None)  # type: ignore[arg-type]


# ============================================================================
# Cross-cutting invariant: none of the validators modify the file they read.
# ============================================================================


def test_no_validator_modifies_the_file(tmp_path):
    p = tmp_path / "SKILL.md"
    original_fm = {
        "name": "x",
        "description": "x. Triggers on x.",
        "status": "current",
        "sensitive_data_class": "Public",
        "portability_tier": "Cold_Start_Safe",
        "created_at": "2026-04-22T01:00:00-07:00",
        "last_validated": "2026-04-22T01:00:00-07:00",
    }
    body = "# Title\n\nReferences mcp_foo.\n"
    _write_skill(p, fm=original_fm, body=body)
    original_bytes = p.read_bytes()
    mtime_before = p.stat().st_mtime

    validators.roundtrip_check(p)
    validators.format_compliance_check(p)
    validators.portability_report(p)
    # schema_check + sensitivity_path_check + wrapper_skill_check do not
    # take a path, but exercising them should still be side-effect-free.
    validators.schema_check(original_fm, kind="skill")
    validators.sensitivity_path_check(
        original_fm, p, agent_bridge_synced_paths=[]
    )
    validators.wrapper_skill_check(body)

    assert p.read_bytes() == original_bytes
    assert p.stat().st_mtime == mtime_before
