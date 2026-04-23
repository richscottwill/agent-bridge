---
inclusion: manual
---

# Blind Test Methodology

*Agent-facing steering resource for running blind tests on proposed system changes. Adopted 2026-04-22, refined through 4 rounds of external-AI review (6 files + 11 follow-ons + 5 unconditional soul.md variations + 3 conditional soul.md variations = 25 proposals across ~100 sub-agent runs). Load manually when about to evaluate any system-addition proposal.*

## When to invoke this

Load this file when Richard (or another agent) asks you to evaluate any of these:

- External AI (Grok, Gemini, ChatGPT, etc.) proposes new steering files, hooks, protocols, or soul.md additions
- Internal proposal to add a new ceremony, metric, table, or always-on check
- Request to modify load-bearing files (soul.md, heart.md, gut.md, am-triage.md protocol, performance-marketing-guide.md)
- Any "should we adopt this?" decision that changes agent behavior across sessions
- Any decision where the stakes justify more than desk-review opinion

**Do not load** for trivial edits, user-requested rewrites with no behavioral change, or mechanical tool additions that don't alter reasoning.

## Core thesis (what 4 rounds proved)

**Empirical blind test > desk review > author self-assessment.** Every round where the default was "desk review" (rounds 1–3 initial critique) was wrong on at least one proposal that blind testing later confirmed should have been adopted — or rejected. The protocol below exists because the methodology is load-bearing: *the test design is what makes the verdict trustworthy*.

Four rounds also proved a secondary thesis: **external AI review hits sharp diminishing returns.** The adoption rate across rounds:

| Round | Proposals | Adopted | Rate |
|---|---:|---:|---:|
| R1 (original 6 files) | 6 | 4 | 67% |
| R2 (11 follow-ons) | 11 | 1 | 9% |
| R3 (5 unconditional soul.md variations) | 5 | 0 | 0% |
| R4 (3 conditional soul.md variations) | 3 | 0 | 0% |

The burden of proof rises each round. By round 3+, the default reasonable prior is "reject unless proposal demonstrates a genuinely novel failure mode in the current system."

## Proposal shape → test type

Pick the test type that matches the proposal's claim. Running the wrong type is the most common procedural error.

### Type A — Replacement test
*Proposal claims to replace existing machinery.*

- **Arms:** existing (as-is) vs proposed replacement
- **Test:** run both on the same real input, document outputs
- **Evaluator:** blind sub-agent compares outputs on 5-dim rubric
- **Example (R2):** excel_ingest.py vs existing dashboard-ingester/ingest.py on the same xlsx drop.
- **When to reject without testing:** if the replacement can't articulate a specific defect in the incumbent (e.g., "it's cleaner" is not a defect).

### Type B — Addition test
*Proposal claims to fill a gap the existing system doesn't cover.*

- **Arms:** control (current system, no treatment) vs treatment (current + proposed file loaded as manual-inclusion steering)
- **Test:** 1–2 representative real-world inputs per proposal
- **Randomize:** seeded Python `random.seed(N)`, shuffle X/Y labels per pair, save mapping to `randomization.csv`
- **Evaluator:** blind sub-agent, 5-dim rubric
- **Example (R1):** 6 proposed files × 2 inputs each = 12 pairs. 4 adoptions.

### Type C — Variation test
*≥3 proposals each propose an alternative implementation of the same behavior slot.*

- **Arms:** baseline + each variation = 1 + N arms
- **Test:** 5 representative tasks spanning task shapes (analytical projection, test readout, exec-facing prose, recurring routine, coaching/ad-hoc)
- **Randomize:** A–F labels shuffled per task; one evaluator per task scores all arms
- **Example (R3 and R4):** 5 and 3 variations × 5 tasks × blind evaluators.
- **Key rule:** use the same 5 tasks across rounds of the same protocol when possible — baselines are reusable and save 5 runs per round.

### Type D — Reasoning-only verdict
*Proposal is architectural and execution-testing is impractical (new table schema, passive log format, meta-ceremony, something that doesn't produce testable output in a single run).*

- **Skip execution.** No A/B is possible.
- **Evaluator:** fresh sub-agent with no knowledge of author, reads proposal + relevant existing system state, applies principle check (soul.md principles 1–8), outputs ADOPT/DEFER/REJECT with reasoning.
- **Example (R2):** high_stakes_log table (DEFER — view over table), guardrail-usage-log (REJECT — duplicate state), validation ceremony (REJECT — self-grading trap).
- **Key rule:** Type D does NOT exempt the proposal from the burden of proof. If reasoning-only review can't articulate the problem the proposal solves, reject.

## Task selection for Type B and C

Bad task selection ruins the test. The tasks must span the agent's actual work shapes, not just the one shape the proposal is good at.

For soul.md / protocol additions, the 5-task set that's worked across R3 and R4:

| # | Task shape | Why included | Stakes | Round 3 baseline | Round 4 baseline |
|---|---|---|---:|---:|---:|
| T1 | Analytical projection (market ceiling, forecast with math) | Tests decision quality + formula discipline | High | 41/50 | 36/50 |
| T2 | Test readout with launch/kill recommendation | Tests stats rigor + actionable next step | Medium | 42/50 | 42/50 |
| T3 | Exec-facing prose (WBR callout for Kate) | Tests Amazon-writing discipline + accuracy | Med-high | 43/50 | 38/50 |
| T4 | Recurring routine (daily brief) | Tests always-on cost at daily cadence | Low per-instance, high frequency | 37/50 | 37/50 |
| T5 | Coaching/ad-hoc direct question | Tests subtraction discipline (answer ≠ framework) | Variable | **49/50** | **50/50** |

The T5 ceiling score (49–50) is the important one: a well-tuned system on a coaching question should answer in the first line with no scaffolding. Any variation that drags T5 below 45 is imposing ceremony that the task specifically rewards avoiding.

**Reuse baselines across rounds when task definitions are stable.** R4 reused R3 baselines; saved 5 runs.

## Standard 5-dimension rubric (Type B and C)

Score each arm 1–10 per dimension:

1. **Clarity of Next Best Action** — Was the next step obvious and actionable?
2. **Decision Quality** — Did the output prioritize correctly given the stakes? Got the math/data right? Right judgment call on extrapolation, confidence, risk?
3. **Adherence to Richard's principles** — Subtraction before addition, structural over cosmetic, invisible over visible, reduce decisions, protect the habit loop. Did the output show procedure or just produce the answer?
4. **Overall Usefulness for THIS TASK** — Would Richard actually use this output in the real context it simulates?
5. **META — Always-on cost tradeoff** — If the decision procedure this arm produces were ALWAYS ON for every task (not just this one), would it add value or become noise? 10 = clear always-on win. 5 = break-even. 1 = harmful noise on simple/routine tasks.

**Dimension 5 is the decisive one for always-on additions.** Every round since R3 has confirmed this. If a proposal scores <7 on dimension 5 across the task set, it doesn't go into always-on steering. At best it becomes a manual-inclusion steering file, a documented optional tool in `device.md`, or a protocol addition in a topical file.

**Sanity thresholds:**
- Totals ≥40/50 on a task = the arm is credible on that task
- Any task score ≤20/50 is typically a "catastrophic failure" — inspect for wrong ground truth, invented triggers, or fabricated data (see failure modes below)
- Baseline totals of 200+/250 across 5 tasks set a high floor; most variations won't clear it

## Randomization protocol (Type B and C)

Positional bias is real. If arm A is always "baseline" and D is always "treatment," evaluators learn the pattern. Shuffle per pair/task:

```python
import random, csv
random.seed(N)                        # monotonic integer per round (42, 43, 44, 45...)
arms = ['baseline', 'var1', 'var2', ...]
tasks = ['t1', 't2', 't3', 't4', 't5']
out = [['task'] + list('ABCDEF'[:len(arms)])]
for t in tasks:
    shuffled = arms.copy()
    random.shuffle(shuffled)
    out.append([t] + shuffled)
with open('shared/tmp/[eval-dir]/randomization.csv','w',newline='') as f:
    csv.writer(f).writerows(out)
```

Save the mapping. **Unseal only after all blind evaluators have written verdicts.** Evaluators must receive only the letter labels (A, B, C, D), never "baseline" or "treatment."

## Evaluator briefing templates

Fresh sub-agent, no context from your main thread. The briefing is load-bearing.

### Generic Type B/C template

```
You are a BLIND evaluator. You have NO knowledge of what produced each output.

The original request was: "[EXACT USER PROMPT]"

**Context you need to score correctly:**
- [Stakes: low/medium/high, who's the audience]
- [Correct answer or answer band if known — but frame as "expected" not "ground truth"]
- [Known failure modes to watch for if relevant]
- [Anything that makes the task non-obvious]

**Arms to evaluate. Labels shuffled per task — anonymous.**
- ARM-A: `shared/tmp/[eval-dir]/runs/[task]-[letter-A-arm].md`
- ARM-B: `shared/tmp/[eval-dir]/runs/[task]-[letter-B-arm].md`
- ARM-C: ...
- ARM-D: ...

**Read all files. Score each arm 1-10 on 5 dimensions:**
1. Clarity of Next Best Action
2. Decision Quality
3. Adherence to Richard's principles (subtraction, invisible-over-visible, reduce-decisions)
4. Overall Usefulness for THIS TASK
5. META — Always-on cost tradeoff (value vs noise if this procedure ran on every task)

Per-arm total out of 50. Then note:
- Which arm got the call right?
- Which added ceremony without value?
- Which would you recommend always-on vs manual/conditional?

**Write verdict to:** `shared/tmp/[eval-dir]/blind-eval/[task]-verdict.md`

Format: summary table (Arm | Clarity | Decision | Principles | Usefulness | Always-on | Total) + per-arm commentary. Be direct and evidence-based.

**DO NOT read any files outside the N arm files above and your own verdict output.** DO NOT peek at prior verdict files from earlier rounds. Be blind.
```

### Type D (reasoning-only) template

```
You are a blind reviewer for a system-change proposal. You have NO knowledge of the author or prior verdicts.

**The proposal:** [paste full text or link to file in shared/tmp/]

**The existing system state it would modify:** [paste relevant existing file content]

**Apply these principle checks:**
1. Subtraction — does this add without removing something that would otherwise serve the purpose?
2. Structural over cosmetic — does this change a default, friction, or pre-loaded content? Or does it just rename/reorder?
3. Invisible over visible — would the intervention be felt as "things just work better"? Or as visible novelty likely to decay?
4. Reduce decisions, not options — does this remove decision fatigue or add a new decision?
5. Self-grading trap — does this proposal include a validation mechanism that would be scored by the same author? If yes, that's a red flag.

**Also answer:**
- What specific defect in the existing system does this solve? (If none articulable, reject.)
- What's the cost of being wrong about adopting this? (If it could degrade sensitive outputs, raise the bar.)
- Is this a "tool we already have, relabeled"? (Check soul.md, body.md, device.md, existing steering files.)

**Verdict:** ADOPT / ADOPT WITH MODIFICATION / DEFER / REJECT, with explicit reasoning.

**Write verdict to:** `shared/tmp/[eval-dir]/type-d-verdict.md`
```

## Failure modes to watch for

Numbered across all 4 rounds. These are patterns that blind testing specifically exposed. Use them as checks when reviewing a proposal or its outputs.

### 1. Self-grading rubrics are a trap
*Round 2, "Validation Test Ceremony."* If the agent produces the output AND grades it against a rubric written by the same author (or derived from the proposal's own language), the rubric IS the answer key and the validation is tautological. **Always use fresh evaluator sub-agents with no knowledge of arm identity.**

### 2. Scaffolding passes when math fails
*Round 3 Var1/T1 (cited $14M ceiling via blended-CPA/blended-CCP error) and Round 4 Var1/T3 (fabricated Italy→AU Polaris narrative).* A filter, sort, or checklist can pass all procedural gates while the underlying analysis is wrong. **Always include Decision Quality on real data in the rubric, not just procedural compliance.** If the arm cites the correct formula but applies it to fabricated inputs, the rubric should catch that as a low score on Decision Quality.

### 3. Procedure that must fire will invent triggers
*Round 4 Var3/T5.* A proposal that says "this activates on high-stakes keywords" will, given a low-stakes task, find something to reinterpret as high-stakes rather than sit out. On T5 (coaching question, send Testing Doc v5 now), Var3 invented an MX-forecast high-stakes trigger and told Richard NOT to send v5 — catastrophic 8/50. **Every proposed procedure needs a legible off-ramp the agent will actually use (see failure mode 4).**

### 4. No explicit-decline path = procedure always fires
*Round 4 Var2 demonstrated the fix.* Var2's outputs included lines like "2x2 usage: Not used (reduce decisions, not options)" — a one-line acknowledgment that the tool was considered and declined. This single design property separated Var2 (184/250) from Var3 (125/250). **When reviewing a proposal, check: does it include a mechanism for the agent to recognize inapplicability and say so briefly?** If not, expect always-on ceremony.

### 5. Tool-wrapping can degrade quality
*Round 2, "Test Readout Analyzer."* Turning a capability the agent already has into a "tool" call can force procedural simulation over actual reasoning — the agent performs the tool's steps instead of thinking. **A proposed tool must demonstrably outperform the agent's natural reasoning on the task, not just structure it.**

### 6. "Redundant with existing steering" is insufficient as rejection reason
*Round 1 verdict — desk review was wrong on 4 of 6 files.* Making behavior explicit at inference time changes attention allocation even when content is nominally covered. The treatment arm with a focused task-specific file can beat the control arm even when the control has "the same information somewhere in loaded context." **If the desk review argument is "this is already covered," run the blind test anyway — it's cheap and often wrong.**

### 7. Task-level wins do not equal adoption
*Round 4 Var3: won T2 (44/50) and T4 (39/50), catastrophic on T5 (8/50), aggregate 125/250.* A proposal that wins 2 of 5 tasks but fails disastrously on 1 is net-negative for always-on use. **Aggregate scores across the task spread matter more than cherry-picked wins.** A task winner can justify manual-inclusion or a conditional protocol addition, but not always-on adoption.

### 8. External-AI review has a half-life
*Rounds 1–4 adoption rate: 67% → 9% → 0% → 0%.* Once the gaps a reviewer identifies have been filled, further proposals from the same source will mostly re-propose existing machinery or add ceremony. **By round 3+, the default prior should be "reject unless proposal demonstrates a novel failure mode in the current system."** Don't run the full protocol on round 5+ of the same external source without a specific reason.

## What adoption-worthy looks like (what R1's 4 winners had in common)

The R1 adoptees (enhanced-navigation-protocol, performance-marketing-guide, high-stakes-guardrails, soul.md principles #7 and #8) shared these properties:

1. **Specific failure mode in the existing system.** Each proposal could name a concrete task shape where the current system underperformed (navigation: context hunting wasted turns; performance-marketing: routine structure drifted without a task-specific template; guardrails: high-stakes outputs lacked explicit confidence/review-flag discipline; principles #7–#8: procedural checks were happening inconsistently).
2. **Task-specific or conditional activation.** None proposed an always-on behavior change for all task shapes. Manual inclusion, fileMatch patterns, or keyword triggers scoped the load.
3. **Structural content, not cosmetic.** They added defaults, pre-loaded templates, or explicit friction-reduction — not renamings or reorderings.
4. **Blind-testable against specific inputs.** Each could be instantiated as "run the agent on this real task with and without the file." Proposals that couldn't be instantiated this way (Type D) had lower adoption rates even when they passed reasoning-only review.

If a proposal doesn't match at least 3 of these 4, the prior tilts toward reject.

## Directory and file conventions

Use these consistently so the protocol is auditable and reusable:

```
shared/tmp/[slug]-[round-N]/
  proposed/
    [id]-[short-name].md          # one file per proposal
  runs/
    [task]-[arm].md               # Type B: control/treatment; Type C: baseline/varN
  blind-eval/
    [task]-verdict.md             # one verdict per task, written by blind evaluator
  randomization.csv               # seeded shuffle mapping, unsealed after evals
shared/context/intake/
  [topic]-verdict-[date].md       # final aggregated verdict with adoption list
```

Naming:
- Eval dir slug: `soul-next-action-eval-r4`, not `test-r4` or `experiment-april-22`
- Rounds: always `-r[N]`, monotonic integer
- Seeds: monotonic (42, 43, 44, 45...), so re-running is deterministic

## Running the test: agent's procedural checklist

When you are asked to run a blind test, work this sequence top to bottom:

1. **Classify the proposal.** Which test type (A/B/C/D)? If you can't decide, read the proposal's claim — does it replace, add, compete with alternatives, or describe architecture?
2. **Check the skip conditions.** Is this round 3+ of the same external source? Does the proposal match adoption-worthy properties? If both are "no," consider reasoning-only Type D rejection instead of full test.
3. **Design the task set** (for Type B/C). Reuse existing task definitions when possible. Span analytical, exec-prose, recurring routine, and coaching shapes.
4. **Create the eval directory** with the convention above.
5. **Launch treatment runs as top-level sub-agent calls.** Nested invokeSubAgent from a sub-agent can hit `z14.registerSubAgentExecution is not a function` — always run arms as top-level calls from the main thread.
6. **Generate randomization.csv** with a monotonic seed. Save it. Do not peek.
7. **Launch blind evaluators in parallel** — one sub-agent per task. Brief each evaluator with the generic template. Include stakes context and correct-answer bands where known, but frame as "expected" not "ground truth" so evaluators can still score sharply on rigor.
8. **Collect verdict files.** Check each wrote to the expected path.
9. **Unseal randomization.** Map blind scores (A–D) back to arm names using the CSV.
10. **Aggregate scores** — totals per variation across all tasks. Flag any single task score ≤20 as a catastrophic-failure candidate.
11. **Write the final verdict** at `shared/context/intake/[topic]-verdict-[date].md` using the round 3/4 verdict shape:
    - Headline (N of M adopted, aggregate scores table)
    - Task-level split analysis (who won what, by how much)
    - Per-proposal verdicts with rationale (adopt/reject + reason tied to dimension scores)
    - Pattern observations (which failure modes fired, what generalizable lessons emerged)
    - Concrete adoption list with file paths
    - Meta-lessons for future rounds
    - Evidence file index
12. **Log to session-log.md** with a 2–3 line summary including file writes and decisions.
13. **Append wiki-candidates.md** if a novel pattern emerged worth documenting elsewhere.
14. **Execute adoptions** as a separate action, not in the same turn as the verdict write — keeps the audit trail clean.

## When to stop testing

External AI review hits sharp diminishing returns. Rules of thumb:

- **R1:** run the full protocol. Real gaps may exist.
- **R2:** run it but expect a ~10% hit rate; most proposals will duplicate existing or add ceremony.
- **R3:** reject by default unless proposal is conditional/trigger-based. Burden of proof is on the proposal.
- **R4+:** strongly recommend closing the thread. Marginal return is near zero. If Richard insists on running R4+, scope it to the smallest defensible set and do reasoning-only (Type D) for proposals that can't articulate a specific novel failure mode.
- **R5+ from the same external source:** the thread is closed. If the user wants to test new proposals, suggest routing the effort to a different class of test (e.g., testing whether an existing adopted file should be *removed*, which has been under-tested).

## Closing thread note

As of 2026-04-22, the external-AI-review thread (Grok proposals against the soul.md / steering file system) is officially closed by default. Four rounds, 25 proposals, 5 adoptions (all in round 1). Any future proposals from this source require the proposal author to first articulate, in writing, what specific failure mode in the current system they've observed. Desk review is sufficient to reject without that articulation.

This closure does NOT apply to:
- Internal proposals (Richard or karpathy or rw-trainer) — those go through the standard protocol
- New external sources (different reviewer, different frame) — treat as R1 for that source
- Subtraction proposals (removing an existing adopted file) — under-tested; worth running

## Evidence files from the four rounds

- R1 verdict (6 files, 4 adopted): adoption list visible in `.kiro/steering/` — enhanced-navigation-protocol.md, performance-marketing-guide.md, high-stakes-guardrails.md, soul.md updates
- R2 verdict: `shared/context/intake/grok-eval-verdict-round2-2026-04-22.md`
- R3 verdict (5 variations, 0 adopted): `shared/context/intake/soul-next-action-eval-verdict-2026-04-22.md`
- R4 verdict (3 conditional variations, 0 adopted): `shared/context/intake/soul-next-action-eval-r4-verdict-2026-04-22.md`
- R1–R4 run evidence: `shared/tmp/soul-next-action-eval*/` and related directories
