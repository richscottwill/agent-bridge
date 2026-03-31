---
inclusion: manual
---

# Architecture Evaluation Protocol

Every architecture change that modifies how agents access data, produce output, or coordinate must be validated by a blind evaluator that has no knowledge of the change. The agent that made the change cannot evaluate its own work.

This is the same principle as the dual blind eval in the autoresearch loop (heart.md), applied to system architecture instead of organ compression.

## When to run

- Agent consolidation or restructuring
- New pipeline creation
- Changes to agent data access patterns (e.g., markdown → DuckDB)
- Changes to agent prompt structure that affect output format
- Any change where "did this make things better or worse?" is a meaningful question

NOT required for: pure infrastructure additions (new query.py function), documentation updates, bug fixes that don't change output.

## Protocol

1. **Snapshot before**: Run the pipeline on a representative input. Save output artifacts.
2. **Apply the change**: Implement the architecture modification.
3. **Run after**: Same pipeline, same input, new architecture. Save output artifacts.
4. **Spawn blind evaluator**: Fresh agent with NO knowledge of what changed. Receives only the before/after outputs and the input data. Does NOT receive the design doc, task list, diff, or any description of the change.
5. **Evaluate**: 5 questions per pipeline:
   - Q1: Factual equivalence (same numbers, conclusions, projections)
   - Q2: Quality comparison (narrative clarity, analytical depth)
   - Q3: Data contradiction check (does "after" contradict input data?)
   - Q4: Gap detection (sections missing, metrics omitted, context lost?)
   - Q5: Decision utility (which output would you use to make a business decision?)
6. **Score**: PASS / REGRESS / NEUTRAL per question
   - APPROVED: 0 REGRESS, at least 1 PASS
   - APPROVED WITH NOTES: 1 REGRESS acknowledged as acceptable tradeoff
   - REJECTED: 2+ REGRESS
7. **Log**: Write to `agent_observations` with `observation_type = 'architecture_eval'`

## Key rules

- The evaluator is blind to the change. It sees outputs, not process.
- Run on at least 3 representative inputs that exercise different code paths.
- If REJECTED, the change is reverted. No exceptions.
- The evaluation result is permanent — it lives in DuckDB as an audit trail.
- This protocol is itself subject to the autoresearch loop's governance. Karpathy can propose experiments on the protocol, but the protocol must be followed until changed.
