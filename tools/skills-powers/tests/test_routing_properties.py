"""
Property-based tests for routing.py — Task 4.7 of the skills-powers-adoption spec.

Three properties per design §Testing Strategy:
  - Property 9:  ROUTING-PRECEDES-CREATE
  - Property 10: EXTEND-EXISTING-PRECEDENCE
  - Property 15: NON-KIRO-GATE-REJECTION

Each property runs 100+ hypothesis iterations. Pytest + hypothesis required.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make the sibling routing.py / matcher.py importable when pytest is run from
# any working directory.
_PKG_DIR = Path(__file__).resolve().parent.parent
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

from routing import (
    EXTEND_EXISTING_THRESHOLD,
    TERMINAL_LEAVES,
    RouteResult,
    _serialize_decision,
    emit_routing_decision,
    walk_routing_tree,
)


# ----------------------------------------------------------------------------
# Fixture data: a stable, realistic trigger set used across all properties.
# Mirrors the live inventory's shape without depending on the filesystem.
# ----------------------------------------------------------------------------

FIXTURE_TRIGGERS: dict[str, dict[str, list[str]]] = {
    "skill": {
        "bridge-sync": [
            "sync to git",
            "bridge sync",
            "portable body",
            "agent bridge",
        ],
        "charts": ["chart", "dashboard", "visualize", "show dashboard"],
        "coach": [
            "coaching",
            "career",
            "1:1 prep",
            "retrospective",
            "growth",
        ],
        "wbr-callouts": [
            "WBR",
            "callout",
            "weekly callout",
            "market callout",
        ],
        "wiki-search": [
            "search wiki",
            "find doc",
            "do we have a doc on",
            "wiki lookup",
        ],
    },
    "power": {
        "flow-gen": ["flow", "tsk", "typescriptkata"],
        "power-builder": [
            "kiro power",
            "power builder",
            "build power",
            "create power",
        ],
    },
}


# All trigger phrases flattened — used by Property 10 generators to inject
# known phrases into synthetic descriptions.
_ALL_TRIGGER_PHRASES: list[tuple[str, str, str]] = [
    (kind, name, phrase)
    for kind, by_name in FIXTURE_TRIGGERS.items()
    for name, phrases in by_name.items()
    for phrase in phrases
]


# ----------------------------------------------------------------------------
# Hypothesis strategies
# ----------------------------------------------------------------------------


_FREE_TEXT = st.text(
    alphabet=st.characters(
        min_codepoint=0x20, max_codepoint=0x7E, blacklist_characters="|\\"
    ),
    min_size=0,
    max_size=120,
)


def _workflow_base() -> st.SearchStrategy[dict]:
    """A random workflow dict with random characteristics for every gate.

    All fields optional so the generator can produce workflows that flow all
    the way to step 7 (SKILL default) as well as workflows that terminate
    early at various gates.
    """
    return st.fixed_dictionaries(
        {
            "description": _FREE_TEXT,
        },
        optional={
            "frequency_per_month": st.floats(
                min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False
            ),
            "reexplanation_cost_minutes": st.floats(
                min_value=0.0, max_value=60.0, allow_nan=False, allow_infinity=False
            ),
            "already_in_memory": st.booleans(),
            "one_off": st.booleans(),
            "is_event_triggered": st.booleans(),
            "applies_every_interaction": st.booleans(),
            "requires_deep_specialist_domain": st.booleans(),
            "is_persistent_shared_state": st.booleans(),
            "needs_mcp_bundle_or_knowledge_base": st.booleans(),
            "has_mcp_bundle": st.booleans(),
            "non_kiro_mechanisms_considered": st.lists(
                st.fixed_dictionaries(
                    {
                        "mechanism": st.sampled_from(
                            [
                                "bashrc",
                                "cron",
                                "git hook",
                                "IDE feature",
                                "team tool",
                            ]
                        ),
                        "handles_workflow": st.booleans(),
                        "how": _FREE_TEXT,
                    }
                ),
                min_size=0,
                max_size=3,
            ),
        },
    )


# ----------------------------------------------------------------------------
# Property 9 — ROUTING-PRECEDES-CREATE
# ----------------------------------------------------------------------------

# Feature: skills-powers-adoption, Property 9: Phase C runs only if
# routing-decision leaf is CREATE-variant (SKILL/POWER/STEERING/HOOK/SUBAGENT/
# ORGAN); REJECT and EXTEND_EXISTING do not trigger Phase C.
@settings(max_examples=150, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(workflow=_workflow_base())
def test_property_9_routing_precedes_create(workflow: dict) -> None:
    """Every walk produces a valid RouteResult; REJECT/EXTEND do not proceed."""
    gates_traversed: list[str] = []
    result = walk_routing_tree(
        workflow, FIXTURE_TRIGGERS, gates_traversed=gates_traversed
    )

    # Basic invariants on the return.
    assert isinstance(result, RouteResult)
    assert result.leaf in TERMINAL_LEAVES
    assert result.rationale, "rationale must be non-empty"
    assert result.gate in {"0", "0.5", "1", "2", "3", "4", "5", "6", "7"}
    assert result.gate == gates_traversed[-1], (
        "terminating gate should be the last gate traversed"
    )

    # Serialize and verify the emitted record shape.
    record = _serialize_decision(workflow, result, gates_traversed)
    assert record["terminal_leaf"] == result.leaf
    assert record["gate_that_terminated"] == result.gate
    assert record["gates_passed"] == gates_traversed
    # Property 9: the record never contains a "proceed_to_phase_c" key — the
    # routing module does not execute Phase C, regardless of leaf. Phase C
    # execution is Group 5, which consumes this record separately and is
    # explicitly gated on CREATE-variant leaves.
    assert "proceed_to_phase_c" not in record

    # REJECT / EXTEND_EXISTING must NOT carry CREATE-variant metadata.
    create_variants = {"SKILL", "POWER", "STEERING", "HOOK", "SUBAGENT", "ORGAN"}
    if result.leaf == "REJECT":
        assert result.extend_target is None
        assert result.power_subtype is None
    if result.leaf == "EXTEND_EXISTING":
        # extend_target MUST be present on EXTEND_EXISTING leaves.
        assert result.extend_target is not None
        kind, name = result.extend_target
        assert kind in ("skill", "power")
        assert name  # non-empty
    if result.leaf in create_variants:
        assert result.extend_target is None


# ----------------------------------------------------------------------------
# Property 10 — EXTEND-EXISTING-PRECEDENCE
# ----------------------------------------------------------------------------


@st.composite
def _workflow_with_known_trigger(draw: st.DrawFn) -> dict:
    """Synthesize a workflow whose description contains at least one exact
    trigger phrase from FIXTURE_TRIGGERS."""
    _kind, _name, phrase = draw(st.sampled_from(_ALL_TRIGGER_PHRASES))
    # Embed the phrase inside some free-text noise. Preserve the exact phrase
    # so the matcher's word-boundary test fires.
    prefix = draw(_FREE_TEXT)
    suffix = draw(_FREE_TEXT)
    description = f"{prefix} {phrase} {suffix}".strip()
    # Ensure no gate 0 / 0.5 short-circuits — leave all those fields unset or
    # explicitly "don't trigger" so step 1 actually gets reached.
    workflow: dict = {
        "description": description,
        # Deliberately omit all step-0 and step-0.5 fields so the tree walks
        # to step 1.
    }
    # Randomize step 2-6 flags — they are AFTER step 1 in tree order, so
    # step 1's EXTEND termination must still win. This is the point of
    # the property.
    workflow["is_event_triggered"] = draw(st.booleans())
    workflow["applies_every_interaction"] = draw(st.booleans())
    workflow["requires_deep_specialist_domain"] = draw(st.booleans())
    workflow["is_persistent_shared_state"] = draw(st.booleans())
    workflow["needs_mcp_bundle_or_knowledge_base"] = draw(st.booleans())
    return workflow


# Feature: skills-powers-adoption, Property 10: Tree terminates at
# EXTEND_EXISTING for overlap >=75% or exact trigger-phrase match; does NOT
# produce new-asset leaves.
@settings(max_examples=150, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(workflow=_workflow_with_known_trigger())
def test_property_10_extend_existing_precedence(workflow: dict) -> None:
    """Any description containing ≥1 exact trigger phrase must terminate at
    EXTEND_EXISTING, regardless of downstream-gate flags."""
    result = walk_routing_tree(workflow, FIXTURE_TRIGGERS)
    assert result.leaf == "EXTEND_EXISTING", (
        f"expected EXTEND_EXISTING, got {result.leaf}; "
        f"description={workflow['description']!r}; rationale={result.rationale!r}"
    )
    assert result.gate == "1"
    assert result.extend_target is not None
    kind, name = result.extend_target
    assert kind in ("skill", "power")
    # The matched name must be one of our fixture assets.
    assert name in FIXTURE_TRIGGERS[kind]


# ----------------------------------------------------------------------------
# Property 15 — NON-KIRO-GATE-REJECTION
# ----------------------------------------------------------------------------


@st.composite
def _workflow_with_non_kiro_hit(draw: st.DrawFn) -> dict:
    """Synthesize a workflow where at least one non-Kiro mechanism entry has
    handles_workflow=True. Step 0 fields are left untouched (no one_off etc.)
    so the test cleanly isolates step 0.5 as the terminating gate."""
    n_hits = draw(st.integers(min_value=1, max_value=3))
    mechanisms = []
    for _ in range(n_hits):
        mechanisms.append(
            {
                "mechanism": draw(
                    st.sampled_from(
                        ["bashrc", "cron", "git hook", "IDE feature", "team tool"]
                    )
                ),
                "handles_workflow": True,
                "how": draw(_FREE_TEXT),
            }
        )
    # Also add some non-hit entries to test the scan behavior.
    n_misses = draw(st.integers(min_value=0, max_value=2))
    for _ in range(n_misses):
        mechanisms.append(
            {
                "mechanism": draw(
                    st.sampled_from(["cron", "IDE feature", "team tool"])
                ),
                "handles_workflow": False,
                "how": draw(_FREE_TEXT),
            }
        )
    # Shuffle order so "hits" are not always at index 0.
    idxs = draw(st.permutations(list(range(len(mechanisms)))))
    mechanisms = [mechanisms[i] for i in idxs]
    return {
        "description": draw(_FREE_TEXT),
        "non_kiro_mechanisms_considered": mechanisms,
        # Deliberately avoid step-0 triggers.
    }


# Feature: skills-powers-adoption, Property 15: If non-Kiro mechanism handles
# W, tree terminates at step 0.5 REJECT with rationale naming the mechanism.
@settings(max_examples=150, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(workflow=_workflow_with_non_kiro_hit())
def test_property_15_non_kiro_gate_rejection(workflow: dict) -> None:
    """Any non-Kiro mechanism flagged handles_workflow=True terminates at
    step 0.5 REJECT. The rationale names the mechanism."""
    result = walk_routing_tree(workflow, FIXTURE_TRIGGERS)
    assert result.leaf == "REJECT", (
        f"expected REJECT, got {result.leaf}; rationale={result.rationale!r}"
    )
    assert result.gate == "0.5"
    # The rationale must name at least one of the mechanisms that was flagged.
    flagged_names = {
        entry["mechanism"]
        for entry in workflow["non_kiro_mechanisms_considered"]
        if entry.get("handles_workflow")
    }
    assert any(name in result.rationale for name in flagged_names), (
        f"rationale {result.rationale!r} does not name any flagged mechanism "
        f"from {flagged_names}"
    )


def test_property_15_dashboard_server_canonical_case() -> None:
    """Explicit (non-randomized) dashboard-server case: the exact kill-list
    scenario the gate is designed to catch."""
    workflow = {
        "description": (
            "auto-restart the dashboard server when the port goes down"
        ),
        "non_kiro_mechanisms_considered": [
            {
                "mechanism": "bashrc",
                "handles_workflow": True,
                "how": "auto-restart on shell init",
            }
        ],
    }
    result = walk_routing_tree(workflow, FIXTURE_TRIGGERS)
    assert result.leaf == "REJECT"
    assert result.gate == "0.5"
    assert "bashrc" in result.rationale
    assert "auto-restart on shell init" in result.rationale


# ----------------------------------------------------------------------------
# Supplementary sanity test: emit_routing_decision writes a valid JSON file.
# Not a property test, but verifies the file-emission contract used by
# Group 5 (safe-creation). Keeps this test module self-contained for
# pytest's collection so Property tests and the integration check co-exist.
# ----------------------------------------------------------------------------


def test_emit_routing_decision_writes_json(tmp_path: Path) -> None:
    workflow = {
        "description": "schedule something on a cron",
        "is_event_triggered": True,
    }
    out = tmp_path / "routing-decision.json"
    record = emit_routing_decision(workflow, FIXTURE_TRIGGERS, out)
    assert out.is_file()
    assert record["terminal_leaf"] == "HOOK"
    assert record["gate_that_terminated"] == "2"
    # File on disk matches the returned record.
    import json

    on_disk = json.loads(out.read_text(encoding="utf-8"))
    assert on_disk == record


if __name__ == "__main__":
    # Allow direct invocation: python3 test_routing_properties.py
    sys.exit(pytest.main([__file__, "-v"]))
