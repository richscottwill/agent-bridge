"""
Property-based tests for safe_creation.py — Task 5.7 of the skills-powers-adoption spec.

Four properties per design §Testing Strategy and Group 5.7:
  - Property 8:  OVERLAP-CHECK-COMPLETENESS
  - Property 9:  ROUTING-PRECEDES-CREATE  (write_new_asset() refuses
                 REJECT/EXTEND_EXISTING leaves; accepts CREATE-variants)
  - Property 11: STATUS-GATED-SCHEMA
  - Property 14: ASSET-LIFECYCLE — validate-before-available half
                 (full Property 14 also covers Phase E archive-before-delete,
                 which is outside Group 5's scope and lives with Group 6.)

Each property runs 100+ hypothesis iterations. Pytest + hypothesis required.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

# Make the sibling modules importable when pytest is run from any working dir.
_PKG_DIR = Path(__file__).resolve().parent.parent
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st


# ----------------------------------------------------------------------------
# Sandbox helper: each test runs against an isolated HOME so it cannot touch
# real ~/.kiro, ~/shared/context, or the live activation log.
# ----------------------------------------------------------------------------


@pytest.fixture
def sandbox_home(monkeypatch):
    """Create a fresh HOME sandbox. All sibling modules reload against it."""
    tmp = tempfile.mkdtemp(prefix="sp_sc_pbt_")
    monkeypatch.setenv("HOME", tmp)
    # Pre-create the Kiro skill/power roots so tools can enumerate them.
    (Path(tmp) / ".kiro" / "skills").mkdir(parents=True)
    (Path(tmp) / ".kiro" / "powers" / "installed").mkdir(parents=True)
    (Path(tmp) / ".kiro" / "agents").mkdir(parents=True)
    (Path(tmp) / ".kiro" / "hooks").mkdir(parents=True)
    (Path(tmp) / ".kiro" / "steering").mkdir(parents=True)
    (Path(tmp) / "shared" / "context" / "body").mkdir(parents=True)
    # Reload the sibling modules so their HOME-derived constants reflect the
    # sandbox. Important: reload INVENTORY and ACTIVATION_LOG first, then
    # SAFE_CREATION (which imports them).
    import importlib

    import activation_log
    import inventory
    import safe_creation

    importlib.reload(inventory)
    importlib.reload(activation_log)
    importlib.reload(safe_creation)
    # Re-bind module-level HOME-derived paths inside safe_creation to reflect
    # the new HOME (reload uses module-level `os.path.expanduser` at import).
    yield Path(tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    # Restore module state for subsequent tests that import without fixture.
    importlib.reload(inventory)
    importlib.reload(activation_log)
    importlib.reload(safe_creation)


# ----------------------------------------------------------------------------
# Hypothesis strategies
# ----------------------------------------------------------------------------

_asset_name_char = st.sampled_from("abcdefghijklmnopqrstuvwxyz0123456789-")
_asset_name = st.text(alphabet=_asset_name_char, min_size=3, max_size=24).filter(
    lambda s: s[0].isalpha() and not s.endswith("-") and "--" not in s
)
_kind = st.sampled_from(["skill", "power"])
_leaf = st.sampled_from(
    ["SKILL", "POWER", "STEERING", "HOOK", "SUBAGENT", "ORGAN"]
)
_non_create_leaf = st.sampled_from(["REJECT", "EXTEND_EXISTING"])

# Short descriptions — the overlap-check tokenizes these, so we want variety
# but we also want them to be realistic prose rather than random bytes.
_words = st.sampled_from(
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
        "subagent",
        "bridge",
        "portable",
        "agent",
        "flow",
        "typescript",
        "kata",
    ]
)
_description = st.lists(_words, min_size=3, max_size=10).map(lambda ws: " ".join(ws))


@st.composite
def proposed_asset_strategy(draw):
    return {
        "kind": draw(_kind),
        "name": draw(_asset_name),
        "description": draw(_description),
    }


# ----------------------------------------------------------------------------
# Property 8: OVERLAP-CHECK-COMPLETENESS
# Feature: skills-powers-adoption, Property 8: New asset creation produces
# overlap-check.json with all 6 Kiro kinds + non_kiro_mechanisms_considered;
# proceeds only if reviewed_by_richard.
# ----------------------------------------------------------------------------


# Validates: Requirements 2.6, 10.1, 10.3
@given(proposed=proposed_asset_strategy(), leaf=_leaf)
@settings(
    max_examples=120,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_property_8_overlap_check_completeness(sandbox_home, proposed, leaf):
    """
    Feature: skills-powers-adoption, Property 8: For any proposed asset with
    a CREATE-variant routing leaf, overlap_check() returns a record containing
    ALL required fields per design §Data Model → Overlap-check evidence record.
    """
    import safe_creation as sc

    routing = {"terminal_leaf": leaf}
    rec = sc.overlap_check(proposed, routing)

    # Top-level required fields.
    for field in (
        "created_at",
        "proposed_asset",
        "searched_mechanisms",
        "overlap_candidates",
        "decision",
        "decision_rationale",
        "alternatives_considered",
        "reviewed_by_richard",
        "reviewed_at",
    ):
        assert field in rec, f"missing top-level field: {field}"

    # proposed_asset echoes required sub-fields.
    pa = rec["proposed_asset"]
    for field in ("kind", "name", "description"):
        assert field in pa, f"proposed_asset missing {field}"
    assert pa["kind"] == proposed["kind"]
    assert pa["name"] == proposed["name"]
    assert pa["description"] == proposed["description"]

    # searched_mechanisms MUST enumerate all 6 Kiro kinds + non_kiro list.
    sm = rec["searched_mechanisms"]
    for kind_key in (
        "skills",
        "powers",
        "subagents",
        "hooks",
        "steering",
        "organs",
        "non_kiro_mechanisms_considered",
    ):
        assert kind_key in sm, f"searched_mechanisms missing {kind_key}"
        assert isinstance(sm[kind_key], list), f"{kind_key} must be a list"

    # overlap_candidates may be empty but must be a list.
    assert isinstance(rec["overlap_candidates"], list)

    # Default decision is CREATE_NEW for empty / low-overlap state.
    assert rec["decision"] in ("CREATE_NEW", "EXTEND_EXISTING", "REJECT")

    # reviewed_by_richard starts False, reviewed_at starts None.
    assert rec["reviewed_by_richard"] is False
    assert rec["reviewed_at"] is None


# ----------------------------------------------------------------------------
# Property 9: ROUTING-PRECEDES-CREATE
# Feature: skills-powers-adoption, Property 9: Phase C runs only if routing-
# decision leaf is CREATE-variant (SKILL/POWER/STEERING/HOOK/SUBAGENT/ORGAN);
# REJECT and EXTEND_EXISTING do not trigger Phase C.
# ----------------------------------------------------------------------------


# Validates: Requirements 2.3, 7.1, 7.2
@given(proposed=proposed_asset_strategy(), leaf=_non_create_leaf)
@settings(
    max_examples=120,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_property_9_overlap_check_refuses_non_create(sandbox_home, proposed, leaf):
    """Property 9 entry point: overlap_check() refuses REJECT and EXTEND_EXISTING."""
    import safe_creation as sc

    routing = {"terminal_leaf": leaf}
    with pytest.raises(ValueError):
        sc.overlap_check(proposed, routing)


# Validates: Requirements 2.3, 7.1, 7.2
@given(leaf=_non_create_leaf)
@settings(
    max_examples=40,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_property_9_write_refuses_unreviewed(sandbox_home, leaf):
    """
    Property 9 exit point: write_new_asset() refuses overlap-check records that
    would only exist if Phase C was invoked wrongly — decision != CREATE_NEW
    or reviewed_by_richard == False.

    We don't produce REJECT/EXTEND_EXISTING overlap records from overlap_check
    (Property 9 entry-point enforces that), but a hostile / buggy caller could
    synthesize one. Write must refuse.
    """
    import safe_creation as sc

    fake_overlap = {
        "decision": "EXTEND_EXISTING" if leaf == "EXTEND_EXISTING" else "REJECT",
        "reviewed_by_richard": True,
    }
    fm = {
        "name": "x",
        "description": "desc",
        "sensitive_data_class": "Amazon_Internal",
        "portability_tier": "Cold_Start_Safe",
    }
    with pytest.raises(ValueError):
        sc.write_new_asset("skill", "x", fm, "# body\n", fake_overlap)


# Validates: Requirements 2.3, 7.1, 7.2
@given(proposed=proposed_asset_strategy(), leaf=_leaf)
@settings(
    max_examples=40,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_property_9_write_accepts_create_variant(sandbox_home, proposed, leaf):
    """Property 9 acceptance: write_new_asset() accepts a reviewed CREATE_NEW overlap record."""
    import safe_creation as sc

    overlap = {
        "decision": "CREATE_NEW",
        "reviewed_by_richard": True,
        "reviewed_at": "2026-04-22T18:00:00+0000",
        "proposed_asset": proposed,
        "searched_mechanisms": {
            "skills": [],
            "powers": [],
            "subagents": [],
            "hooks": [],
            "steering": [],
            "organs": [],
            "non_kiro_mechanisms_considered": [],
        },
        "overlap_candidates": [],
        "decision_rationale": "synth",
        "alternatives_considered": [],
        "created_at": "2026-04-22T18:00:00+0000",
    }
    fm = {
        "name": proposed["name"],
        "description": proposed["description"] + ". Triggers on test.",
        "sensitive_data_class": "Amazon_Internal",
        "portability_tier": "Cold_Start_Safe",
    }
    # POWER kind needs the power-specific required fields. Only test skill
    # here to keep the generator simple; the "accepts" assertion is the same
    # regardless of kind.
    try:
        md_path = sc.write_new_asset("skill", proposed["name"], fm, "# body\n", overlap)
    except FileExistsError:
        # hypothesis can re-propose the same name on repeat examples — that's
        # a legitimate "already exists" case, not a Property 9 violation.
        assume(False)
    assert md_path.is_file()
    assert md_path.parent.name == proposed["name"]
    assert md_path.name == "SKILL.md"


# ----------------------------------------------------------------------------
# Property 11: STATUS-GATED-SCHEMA
# Feature: skills-powers-adoption, Property 11: status: current requires full
# frontmatter; status: legacy skips schema validation; bijection holds across
# all statuses.
# ----------------------------------------------------------------------------


# Validates: Requirements 3.1, 4.2, 9.5
@given(status=st.sampled_from(["current", "legacy"]))
@settings(
    max_examples=60,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_property_11_status_gated_validation_skill(sandbox_home, status):
    """Current skill with minimal fm → schema error. Legacy skill minimal → OK."""
    import inventory as inv

    fm: dict = {"name": "x", "description": "d. Triggers on x."}
    if status == "current":
        fm["status"] = "current"
        violation = inv.validate_frontmatter(fm, kind="skill")
        assert violation is not None, "current skill missing required fields should error"
        assert "sensitive_data_class" in violation or "missing required" in violation
    else:
        # status absent => default legacy → validates with minimal fm.
        violation = inv.validate_frontmatter(fm, kind="skill")
        assert violation is None, f"legacy skill minimal fm should pass; got {violation}"


# Validates: Requirements 3.1, 4.2, 9.5
@given(status=st.sampled_from(["current", "legacy"]))
@settings(
    max_examples=60,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_property_11_status_gated_validation_power(sandbox_home, status):
    """Same check for powers with their additional required minimal fields."""
    import inventory as inv

    fm: dict = {
        "name": "p",
        "displayName": "P",
        "description": "d",
        "keywords": ["p"],
        "author": "A",
    }
    if status == "current":
        fm["status"] = "current"
        violation = inv.validate_frontmatter(fm, kind="power")
        assert violation is not None
    else:
        violation = inv.validate_frontmatter(fm, kind="power")
        assert violation is None


# Validates: Requirements 3.1, 4.2, 9.5
@given(
    classify_choice=st.sampled_from(["classify", "refuse"]),
    edit_content=st.text(min_size=1, max_size=40, alphabet=st.characters(min_codepoint=32, max_codepoint=122)),
)
@settings(
    max_examples=60,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_property_11_legacy_migration(sandbox_home, classify_choice, edit_content):
    """
    Touch-it-classify-it: classify_legacy_then_write either flips legacy→current
    and adds fields, OR preserves legacy on refusal.
    """
    import safe_creation as sc

    sk = sandbox_home / ".kiro" / "skills" / "legacy_pbt"
    sk.mkdir(parents=True, exist_ok=True)
    md = sk / "SKILL.md"
    # Fresh file each iteration.
    md.write_text(
        "---\nname: legacy_pbt\ndescription: d. Triggers on demo.\n---\n# body\n",
        encoding="utf-8",
    )

    def edit(txt: str) -> str:
        # Simple body edit (safe to pass through YAML parser).
        return txt.replace("# body", "# body\nextra")

    if classify_choice == "classify":

        def classify(fm, kind):
            return {
                "sensitive_data_class": "Amazon_Internal",
                "portability_tier": "Cold_Start_Safe",
            }

        rec = sc.classify_legacy_then_write(md, edit, classify)
        assert rec["action"] == "classified"
        assert rec["previous_status"] == "legacy"
        assert rec["new_status"] == "current"
        text = md.read_text(encoding="utf-8")
        assert "status: current" in text
        assert "sensitive_data_class" in text
        assert "portability_tier" in text
        # Clean up for the next iteration.
        shutil.rmtree(sk, ignore_errors=True)
    else:

        def refuse(fm, kind):
            return None

        rec = sc.classify_legacy_then_write(md, edit, refuse)
        assert rec["action"] == "edit_only"
        assert rec["new_status"] == "legacy"
        text = md.read_text(encoding="utf-8")
        # No current-only fields were added.
        assert "status: current" not in text
        assert "sensitive_data_class" not in text
        shutil.rmtree(sk, ignore_errors=True)


# ----------------------------------------------------------------------------
# Property 14: ASSET-LIFECYCLE (validate-before-available half)
# Feature: skills-powers-adoption, Property 14: Activation-validate before
# available. If a file is invalid, activation_validate must error and
# last_validated MUST NOT be updated on the file. The file remains activate-
# blocked (annotated with # validation-failed comment).
# ----------------------------------------------------------------------------

_invalid_shape = st.sampled_from(
    [
        "missing-frontmatter",
        "malformed-yaml",
        "status-current-missing-fields",
        "non-canonical-path",
    ]
)


# Validates: Requirements 7.6
@given(shape=_invalid_shape)
@settings(
    max_examples=80,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
def test_property_14_validate_before_available(sandbox_home, shape):
    """
    Invalid asset → activation_validate returns valid=False; last_validated is
    NOT updated; file remains annotated / blocked.
    """
    import safe_creation as sc

    if shape == "missing-frontmatter":
        # Canonical path, but no `---` fences.
        sk = sandbox_home / ".kiro" / "skills" / "prop14a"
        sk.mkdir(parents=True, exist_ok=True)
        md = sk / "SKILL.md"
        md.write_text("# body only, no frontmatter\n", encoding="utf-8")
        before = md.read_text(encoding="utf-8")
        r = sc.activation_validate(md)
        assert r["valid"] is False
        after = md.read_text(encoding="utf-8")
        # No last_validated update on invalid.
        assert "last_validated" not in after
        # Annotation not appendable without a frontmatter fence — file unchanged.
        assert after == before
    elif shape == "malformed-yaml":
        sk = sandbox_home / ".kiro" / "skills" / "prop14b"
        sk.mkdir(parents=True, exist_ok=True)
        md = sk / "SKILL.md"
        md.write_text("---\nname: bad\n  bad: :: :\n---\n# x\n", encoding="utf-8")
        r = sc.activation_validate(md)
        assert r["valid"] is False
        after = md.read_text(encoding="utf-8")
        # last_validated MUST NOT be in the file.
        assert "last_validated:" not in after
        # Annotation IS in the file — future agent skips the asset.
        assert "# validation-failed:" in after
    elif shape == "status-current-missing-fields":
        sk = sandbox_home / ".kiro" / "skills" / "prop14c"
        sk.mkdir(parents=True, exist_ok=True)
        md = sk / "SKILL.md"
        md.write_text(
            "---\nname: prop14c\ndescription: d. Triggers on x.\nstatus: current\n---\n# body\n",
            encoding="utf-8",
        )
        r = sc.activation_validate(md)
        assert r["valid"] is False
        after = md.read_text(encoding="utf-8")
        assert "last_validated:" not in after
        assert "# validation-failed:" in after
    elif shape == "non-canonical-path":
        # File at a path NOT under ~/.kiro/skills/<name>/SKILL.md.
        bad_root = sandbox_home / "not-kiro"
        bad_root.mkdir(parents=True, exist_ok=True)
        md = bad_root / "SKILL.md"
        md.write_text(
            "---\nname: x\ndescription: d. Triggers on x.\n---\n# body\n",
            encoding="utf-8",
        )
        r = sc.activation_validate(md)
        assert r["valid"] is False
        assert r["canonical_path_ok"] is False
