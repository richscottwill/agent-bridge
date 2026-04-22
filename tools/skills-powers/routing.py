"""
Routing Decision Tree — Phase B of the skills-powers-adoption spec.

Implements the 8-step tree from design §Routing Decision Tree. First matching
branch wins. Order matters: steps 0 and 0.5 are subtraction-first gates; step 1
is EXTEND-EXISTING-first; only after those three gates does the tree reach
mechanism-selection (steps 2-7).

DESIGN STANCE

    This module walks the tree and EMITS a routing-decision.json record. It
    does NOT execute Phase C (safe-creation). Phase C is Group 5. REJECT and
    EXTEND_EXISTING leaves explicitly do NOT trigger Phase C per design
    §Routing Decision Tree and Property 9.

    Per design §Anti-Goals #3 ("Subtraction before addition is the tree's
    default"): steps 0 and 0.5 exist to terminate the tree BEFORE any
    mechanism-selection happens. Do not short-circuit them because "the caller
    already decided it's worth codifying" — the caller is often wrong, and the
    gate is the correction.

THRESHOLD NOTE (step 1)

    Design §Routing Decision Tree step 1 uses ≥75% overlap OR one exact
    trigger-phrase match for EXTEND_EXISTING termination. This is STRICTER
    than matcher.py's 0.5 threshold, which governs pre-draft activation. Both
    thresholds coexist — the matcher errs toward activating a skill on any
    plausible match (low cost, reversible), while the routing tree errs
    toward avoiding duplication only when the overlap is strong (high
    confidence, EXTEND blocks a new asset from being created).

CLI

    python3 routing.py route <workflow.json>
      Load a workflow JSON file, walk the tree, write routing-decision.json
      next to the input. Print the decision to stdout.

    python3 routing.py demo
      Exercise all 8 terminal leaves with synthetic workflows.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

# Import matcher for step 1 overlap scoring. The matcher returns scores in
# [0, 1]; step 1 uses the 0.75 threshold which is stricter than matcher's
# internal 0.5 pre-draft-activation threshold.
try:
    from matcher import match_request_to_assets
except ImportError:  # when invoked as part of a package
    from .matcher import match_request_to_assets  # type: ignore


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

EXTEND_EXISTING_THRESHOLD = 0.75  # per design §Routing Decision Tree step 1

# Valid terminal leaves per design §Routing Decision Tree.
TERMINAL_LEAVES = (
    "REJECT",
    "EXTEND_EXISTING",
    "HOOK",
    "STEERING",
    "SUBAGENT",
    "ORGAN",
    "POWER",
    "SKILL",
)


# ----------------------------------------------------------------------------
# Data classes
# ----------------------------------------------------------------------------


@dataclass
class RouteResult:
    """One terminal result from the routing tree.

    Attributes:
        leaf: one of TERMINAL_LEAVES.
        rationale: short human-readable explanation of why this leaf was chosen.
        gate: the gate number that terminated ("0", "0.5", "1", ..., "7").
        extend_target: (kind, name) tuple if leaf == "EXTEND_EXISTING", else None.
        power_subtype: "Guided MCP" or "Knowledge Base" if leaf == "POWER", else None.
    """

    leaf: str
    rationale: str
    gate: str
    extend_target: tuple[str, str] | None = None
    power_subtype: str | None = None

    def __post_init__(self) -> None:
        if self.leaf not in TERMINAL_LEAVES:
            raise ValueError(
                f"invalid terminal leaf {self.leaf!r}; expected one of {TERMINAL_LEAVES}"
            )


# ----------------------------------------------------------------------------
# Task 4.1 — Step 0: REJECT gate (subtraction before addition)
# ----------------------------------------------------------------------------


def step_0_reject_gate(workflow: dict[str, Any]) -> RouteResult | None:
    """Subtraction-before-addition gate.

    Questions, per design §Routing Decision Tree step 0:
      - frequency < 1x/month?
      - re-explanation cost low (< 5 minutes)?
      - already captured by memory + standard prompt?
      - one-off that won't recur?

    Any YES → REJECT. Any signal missing from the workflow dict → conservative
    default "no" (do NOT reject on missing data; let the caller declare intent).
    """
    reasons: list[str] = []

    freq = workflow.get("frequency_per_month")
    if freq is not None and freq < 1:
        reasons.append(f"frequency {freq:.2f}/month is below 1x/month threshold")

    cost = workflow.get("reexplanation_cost_minutes")
    if cost is not None and cost < 5:
        reasons.append(f"re-explanation cost {cost} min is below 5 min threshold")

    already = workflow.get("already_in_memory")
    if already is True:
        reasons.append("already captured by memory + standard prompt")

    one_off = workflow.get("one_off")
    if one_off is True:
        reasons.append("one-off that won't recur")

    if reasons:
        return RouteResult(
            leaf="REJECT",
            rationale=f"keep in head, no codification needed: {reasons[0]}",
            gate="0",
        )
    return None


# ----------------------------------------------------------------------------
# Task 4.2 — Step 0.5: NON-KIRO gate (external mechanism already handles it)
# ----------------------------------------------------------------------------


def step_0_5_non_kiro_gate(workflow: dict[str, Any]) -> RouteResult | None:
    """Check whether a non-Kiro mechanism already handles the workflow.

    The caller supplies `non_kiro_mechanisms_considered`: a list of dicts with
    keys {mechanism, handles_workflow, how}. For each entry where
    `handles_workflow` is truthy, the gate terminates at REJECT with a
    rationale naming the mechanism and the "how" of the coverage.

    The canonical reference case: dashboard-server.kiro.hook duplicating
    `.bashrc` auto-restart. Passing
        {"mechanism": "bashrc", "handles_workflow": True,
         "how": "auto-restart on shell init"}
    in the list would trigger REJECT here, which is the exact kill-list case
    the gate is designed to catch.
    """
    mechanisms = workflow.get("non_kiro_mechanisms_considered") or []
    if not isinstance(mechanisms, list):
        return None

    for entry in mechanisms:
        if not isinstance(entry, dict):
            continue
        if not entry.get("handles_workflow"):
            continue
        name = entry.get("mechanism", "unknown")
        how = entry.get("how", "")
        suffix = f" ({how})" if how else ""
        return RouteResult(
            leaf="REJECT",
            rationale=f"already handled by non-Kiro mechanism: {name}{suffix}",
            gate="0.5",
        )
    return None


# ----------------------------------------------------------------------------
# Task 4.3 — Step 1: EXTEND_EXISTING gate (no duplication)
# ----------------------------------------------------------------------------


def step_1_extend_existing_gate(
    workflow: dict[str, Any],
    triggers: dict[str, dict[str, list[str]]],
) -> RouteResult | None:
    """Check whether an existing asset already covers the workflow intent.

    Threshold: ≥0.75 token overlap OR exact trigger-phrase match (score 1.0)
    per design §Routing Decision Tree step 1. Stricter than matcher.py's 0.5
    pre-draft-activation threshold — both thresholds coexist because routing
    termination has higher consequences than optimistic activation.
    """
    description = workflow.get("description", "") or ""
    if not description.strip():
        return None

    matches = match_request_to_assets(description, triggers)
    # matches is sorted by score DESC, name ASC. Top entry wins if above
    # threshold.
    for kind, name, score, reason in matches:
        if score >= EXTEND_EXISTING_THRESHOLD:
            return RouteResult(
                leaf="EXTEND_EXISTING",
                rationale=(
                    f"matched existing asset '{name}' at score {score:.2f}: {reason}"
                ),
                gate="1",
                extend_target=(kind, name),
            )
    return None


# ----------------------------------------------------------------------------
# Task 4.4 — Steps 2-7: mechanism selection
# ----------------------------------------------------------------------------


def step_2_event_keyword_split(workflow: dict[str, Any]) -> RouteResult | None:
    """HOOK branch: event-triggered workflows."""
    if workflow.get("is_event_triggered"):
        return RouteResult(
            leaf="HOOK",
            rationale=(
                "event-triggered workflow (file / prompt / schedule); "
                "lives as ~/.kiro/hooks/{name}.kiro.hook"
            ),
            gate="2",
        )
    return None


def step_3_identity_always(workflow: dict[str, Any]) -> RouteResult | None:
    """STEERING branch: rules that apply to every interaction."""
    if workflow.get("applies_every_interaction"):
        return RouteResult(
            leaf="STEERING",
            rationale=(
                "applies every interaction (identity / style / environment); "
                "lives as ~/.kiro/steering/{name}.md — scrutinize every-chat tax"
            ),
            gate="3",
        )
    return None


def step_4_specialist_domain(workflow: dict[str, Any]) -> RouteResult | None:
    """SUBAGENT branch: deep specialist domain with autonomous execution."""
    if workflow.get("requires_deep_specialist_domain"):
        return RouteResult(
            leaf="SUBAGENT",
            rationale=(
                "narrow specialist domain with autonomous execution; "
                "lives as ~/.kiro/agents/{name}.json"
            ),
            gate="4",
        )
    return None


def step_5_persistent_state(workflow: dict[str, Any]) -> RouteResult | None:
    """ORGAN branch: persistent shared state."""
    if workflow.get("is_persistent_shared_state"):
        return RouteResult(
            leaf="ORGAN",
            rationale=(
                "persistent shared state (data, not behavior); "
                "lives as ~/shared/context/body/{name}.md"
            ),
            gate="5",
        )
    return None


def step_6_mcp_bundle(workflow: dict[str, Any]) -> RouteResult | None:
    """POWER branch: MCP bundle or knowledge base."""
    if workflow.get("needs_mcp_bundle_or_knowledge_base"):
        # Determine sub-type. Guided MCP requires an mcp.json bundle; Knowledge
        # Base is pure documentation loaded via kiroPowers activate.
        has_mcp = workflow.get("has_mcp_bundle", False)
        subtype = "Guided MCP" if has_mcp else "Knowledge Base"
        return RouteResult(
            leaf="POWER",
            rationale=(
                f"{subtype} power; lives as "
                "~/.kiro/powers/installed/{name}/POWER.md"
            ),
            gate="6",
            power_subtype=subtype,
        )
    return None


def step_7_default_skill(workflow: dict[str, Any]) -> RouteResult:
    """SKILL branch (default). Always terminates — this is the last gate."""
    return RouteResult(
        leaf="SKILL",
        rationale=(
            "keyword-activated workflow loaded via discloseContext; "
            "lives as ~/.kiro/skills/{name}/SKILL.md"
        ),
        gate="7",
    )


# ----------------------------------------------------------------------------
# Task 4.5 & 4.6 — Tree walker + routing-decision.json emission
# ----------------------------------------------------------------------------


def walk_routing_tree(
    workflow: dict[str, Any],
    triggers: dict[str, dict[str, list[str]]],
    *,
    gates_traversed: list[str] | None = None,
) -> RouteResult:
    """Walk the 8-step tree and return the first terminating RouteResult.

    `gates_traversed` (optional, mutated in-place if provided): appended with
    the gate identifier for every gate the tree entered (including the one
    that terminated). Useful for emitting `gates_passed` in the decision JSON.
    """
    if gates_traversed is None:
        gates_traversed = []

    # Each (gate_id, fn) pair runs in order. A truthy return terminates.
    # Note step 1 takes (workflow, triggers); the rest take (workflow,).
    gates: list[tuple[str, Callable[..., RouteResult | None]]] = [
        ("0", lambda w: step_0_reject_gate(w)),
        ("0.5", lambda w: step_0_5_non_kiro_gate(w)),
        ("1", lambda w: step_1_extend_existing_gate(w, triggers)),
        ("2", lambda w: step_2_event_keyword_split(w)),
        ("3", lambda w: step_3_identity_always(w)),
        ("4", lambda w: step_4_specialist_domain(w)),
        ("5", lambda w: step_5_persistent_state(w)),
        ("6", lambda w: step_6_mcp_bundle(w)),
    ]

    for gate_id, fn in gates:
        gates_traversed.append(gate_id)
        result = fn(workflow)
        if result is not None:
            return result

    # Step 7 is the default; always terminates.
    gates_traversed.append("7")
    return step_7_default_skill(workflow)


def _serialize_decision(
    workflow: dict[str, Any],
    result: RouteResult,
    gates_traversed: list[str],
) -> dict[str, Any]:
    """Build the routing-decision.json record."""
    record: dict[str, Any] = {
        "timestamp": datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "workflow_description": workflow.get("description", ""),
        "terminal_leaf": result.leaf,
        "rationale": result.rationale,
        # gates_passed is every gate the tree ENTERED before (and including)
        # termination. This matches design's "gates_passed" intent — an audit
        # trail of which gates were consulted.
        "gates_passed": list(gates_traversed),
        "gate_that_terminated": result.gate,
    }
    if result.extend_target is not None:
        kind, name = result.extend_target
        record["extend_target"] = f"{kind}:{name}"
    if result.power_subtype is not None:
        record["power_subtype"] = result.power_subtype
    return record


def emit_routing_decision(
    workflow: dict[str, Any],
    triggers: dict[str, dict[str, list[str]]],
    output_path: Path,
) -> dict[str, Any]:
    """Walk the tree and write routing-decision.json. Returns the record."""
    gates_traversed: list[str] = []
    result = walk_routing_tree(workflow, triggers, gates_traversed=gates_traversed)
    record = _serialize_decision(workflow, result, gates_traversed)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return record


# ----------------------------------------------------------------------------
# Task 4.6 — CLI
# ----------------------------------------------------------------------------


def _cli_route(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: python3 routing.py route <workflow.json>", file=sys.stderr)
        return 2
    workflow_path = Path(argv[2])
    if not workflow_path.is_file():
        print(f"not found: {workflow_path}", file=sys.stderr)
        return 2
    workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
    # Load triggers from the live inventory (matcher's default path).
    from matcher import extract_triggers_from_inventory

    triggers = extract_triggers_from_inventory()
    out_path = workflow_path.parent / "routing-decision.json"
    record = emit_routing_decision(workflow, triggers, out_path)
    print(f"wrote {out_path}")
    print(json.dumps(record, indent=2, ensure_ascii=False))
    return 0


def _cli_demo(argv: list[str]) -> int:
    """Exercise all 8 terminal leaves with synthetic workflows.

    One workflow per leaf. Does NOT touch the live inventory — uses synthetic
    trigger data so the demo is deterministic regardless of what's installed.
    """
    # Synthetic triggers: realistic shape, stable regardless of live inventory.
    triggers: dict[str, dict[str, list[str]]] = {
        "skill": {
            "bridge-sync": [
                "sync to git",
                "bridge sync",
                "portable body",
                "agent bridge",
            ],
            "wbr-callouts": [
                "WBR",
                "callout",
                "weekly callout",
                "market callout",
            ],
        },
        "power": {},
    }

    demos: list[tuple[str, dict[str, Any]]] = [
        # REJECT via step 0.5 (non-Kiro mechanism) — dashboard-server canonical.
        (
            "dashboard-server (REJECT-via-0.5)",
            {
                "description": "auto-restart the dashboard server when port goes down",
                "non_kiro_mechanisms_considered": [
                    {
                        "mechanism": "bashrc",
                        "handles_workflow": True,
                        "how": "auto-restart on shell init",
                    }
                ],
            },
        ),
        # REJECT via step 0 (one-off).
        (
            "typo-comparison (REJECT-via-0)",
            {
                "description": "compare three documents I opened in tabs last Tuesday",
                "one_off": True,
            },
        ),
        # EXTEND_EXISTING via step 1 (bridge-sync overlap).
        (
            "bridge-push (EXTEND_EXISTING)",
            {
                "description": "push new organs to the agent bridge",
            },
        ),
        # HOOK via step 2.
        (
            "file-watcher (HOOK)",
            {
                "description": "parse wiki candidates from any new file in ~/shared/context/intake/",
                "is_event_triggered": True,
            },
        ),
        # STEERING via step 3.
        (
            "always-use-bullets (STEERING)",
            {
                "description": "always use bullet points for multi-item responses",
                "applies_every_interaction": True,
            },
        ),
        # SUBAGENT via step 4.
        (
            "career-coach (SUBAGENT)",
            {
                "description": "deep career coaching using the full body system",
                "requires_deep_specialist_domain": True,
            },
        ),
        # ORGAN via step 5.
        (
            "op2-tracker (ORGAN)",
            {
                "description": "maintain OP2 targets per market as persistent shared state",
                "is_persistent_shared_state": True,
            },
        ),
        # POWER via step 6.
        (
            "agentcore-onboard (POWER)",
            {
                "description": "onboard Bedrock AgentCore with its own MCP tools and docs",
                "needs_mcp_bundle_or_knowledge_base": True,
                "has_mcp_bundle": True,
            },
        ),
        # SKILL via step 7 (default).
        (
            "wbr-callout-pipeline-v2 (SKILL)",
            {
                # Intentionally avoid trigger overlap with wbr-callouts so
                # step 1 doesn't fire. The prompt-level novelty here is the
                # v2 pipeline with different sub-routes.
                "description": "orchestrate a revised analyst-critic-finalizer pipeline for Q3 reviews",
            },
        ),
    ]

    print("=" * 70)
    print("ROUTING DECISION TREE — DEMO (8 terminal leaves)")
    print("=" * 70)
    for label, workflow in demos:
        gates_traversed: list[str] = []
        result = walk_routing_tree(workflow, triggers, gates_traversed=gates_traversed)
        record = _serialize_decision(workflow, result, gates_traversed)
        print(f"\n--- {label} ---")
        print(json.dumps(record, indent=2, ensure_ascii=False))
    print()
    return 0


def _cli(argv: list[str]) -> int:
    if len(argv) < 2:
        print(
            "usage: python3 routing.py route <workflow.json>\n"
            "       python3 routing.py demo",
            file=sys.stderr,
        )
        return 2
    cmd = argv[1]
    if cmd == "route":
        return _cli_route(argv)
    if cmd == "demo":
        return _cli_demo(argv)
    print(f"unknown command: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))
