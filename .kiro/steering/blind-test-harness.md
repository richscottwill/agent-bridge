---
inclusion: manual
---

# Blind Test Harness — Methodology & Setups

*Invoke this file manually when designing a blind test of a proposed system change (steering file, protocol, hook, soul.md addition, etc.). Built 2026-04-22 after three rounds of testing (95+ sub-agent runs) validated this methodology empirically.*

## When to use this harness

Trigger on any proposal that would change agent behavior system-wide:
- New steering file (manual or auto-inclusion)
- Protocol addition to existing organ or hook
- soul.md addition (highest scrutiny — see §Soul.md-specific rules below)
- External AI proposal (Grok, Gemini, etc.) to add infrastructure

Do NOT use for: typo fixes, one-off content updates, documentation improvements that don't change agent reasoning.

## Core protocol

1. **Save the proposed artifact verbatim** to `shared/tmp/{test-name}/proposed/` — do not paraphrase. The blind evaluator needs to see what the agent actually saw.
2. **Pick representative inputs** that stratify across task types (see §Test-type patterns).
3. **Randomize arm labels** with a seeded RNG (Python `random.seed(N)`). Store the mapping in `shared/tmp/{test-name}/randomization.csv` — unsealed only after scoring.
4. **Launch sub-agents** to produce control and treatment outputs. Use `general-task-execution` unless a specialized subagent is required.
5. **Launch blind evaluators** as fresh sub-agents that see only anonymized arm outputs and the rubric — no knowledge of which arm is control vs. treatment, no knowledge of what changed.
6. **Unseal and aggregate** after all runs complete. Write consolidated verdict to `shared/context/intake/{test-name}-verdict-YYYY-MM-DD.md`.

## Test-type patterns (choose based on proposal shape)

### Pattern A: Control vs Treatment A/B (for net-new additions)

Use when the proposal adds new behavior that can be turned on/off cleanly.

- Control: current system as-is
- Treatment: current system + proposed artifact loaded as active steering
- Inputs: 2 per proposal minimum (stratified across at least 2 task types)
- Scoring: 5-question architecture-eval-protocol rubric, PASS / NEUTRAL / REGRESS per Q
- Verdict threshold: APPROVED = 0 REGRESS and ≥1 PASS. APPROVED WITH NOTES = 1 REGRESS acceptable. REJECTED = 2+ REGRESS.

Used in: Round 1 (6 files, 36 runs, 4/6 adopted).

### Pattern B: Comparative head-to-head (for proposals that duplicate existing machinery)

Use when the proposal replicates something that already exists in the system.

- Arm 1: Grok's proposed artifact evaluated on its own merits (does it run? is the math right? does it handle edge cases?)
- Arm 2: Existing equivalent evaluated on the same inputs
- Inputs: 1 per proposal (real data the existing system already handles)
- Scoring: direct comparison — which wins on quality, correctness, integration with the rest of the system?

#### Part 1
- Verdict: existing > proposed / proposed > existing / different scope (one is strategic, one operational)

Used in: Round 2 (8 of 11 proposals via this pattern).

### Pattern C: Multi-arm tournament with always-on cost dimension

Use when the proposal would be always-on (soul.md additions, auto-included steering files).

- Arms: baseline + each proposed variation (6 arms = 1 baseline + 5 variations typical)
- Inputs: 5 stratified tasks minimum — must include both task types the proposal helps AND task types it doesn't (this is critical; otherwise always-on cost is invisible)
- Scoring: 5-dimension rubric **including "Always-on cost tradeoff"** (1-10, lower = more costly)
- Randomization: shuffle arm letters per task independently
- Verdict threshold: proposal must beat baseline on AVERAGE across all tasks, not just the task type it was designed for

Used in: Round 3 (30 runs + 5 blind evals, 0/5 variations beat baseline).

### Pattern D: Reasoning-based evaluation (for architectural proposals)

Use when the proposal is about creating a DuckDB table, database schema, or infrastructure that doesn't produce task outputs.

- No control/treatment runs needed
- Single sub-agent writes a structured evaluation addressing: what exists today, what gap the proposal fills, who writes to it / reads from it, architectural soundness, principle check against soul.md How-I-Build
- Verdict: adopt / defer / reject with specific conditions for revisit

Used in: Round 2 proposals #10 (high_stakes_log table), #11 (validation ceremony).

## Rubric dimensions (the ones that have worked across rounds)

Always include:

1. **Clarity of Next Best Action** (1-10) — is the recommended next step obvious and actionable?
2. **Decision Quality** (1-10) — did the output make the right call given the stakes?
3. **Principle Adherence** (1-10) — subtraction, invisible-over-visible, reduce decisions
4. **Overall Usefulness** (1-10) — would Richard actually use this output?

Include for soul.md / always-on proposals (Pattern C):

5. **Always-on cost tradeoff** (1-10, LOWER = MORE COSTLY) — if this procedure ran on EVERY task, would it add value or become ceremony? Break-even = 5. 10 = clear always-on win. 1 = harmful noise on routine tasks.

This 5th dimension is the one that killed Round 3. Without it, a variation can win on its target task type and lose silently on all others. With it, the cost of always-on is forced into the score.

## Blind evaluator prompt scaffolding

Every blind evaluator prompt should have:

- **No arm identity** — only ARM-X through ARM-N as labels
- **The original user request verbatim** — so the evaluator can assess fit
- **List of files to read** — no hints about which is which
- **Scoring rubric with clear scales** — 1-10 per dimension, or PASS/NEUTRAL/REGRESS
- **Specific output format** (markdown table) and save path
- **One-line confirmation** at end — "After saving, reply with 'Saved: [identifier]'"

Never include in the blind evaluator prompt:
- Which arm is control vs. treatment
- What the proposed change was designed to improve
- Any phrase that could bias the evaluator toward one arm

## Randomization implementation

```python
import random
random.seed(SEED)  # consistent seed per test round
# For multi-arm: shuffle per-task so the same arm gets different letters across tasks
for task in tasks:
    arms_for_this_task = ['baseline', 'var1', 'var2', ...]
    random.shuffle(arms_for_this_task)
    # Map A,B,C,... to shuffled arms, record in randomization.csv
```

Use different seeds across test rounds to avoid pattern memorization.

## Soul.md-specific rules

soul.md is auto-injected into every session. Additions to it carry an **always-on tax** that other steering files do not. Before running any test on a soul.md proposal:

1. Ask: could this be a manual-inclusion steering file instead? If yes, that's the better form — test that version, not the soul.md version.
2. Require Pattern C (multi-arm tournament) with the always-on cost dimension. Pattern A is insufficient because it doesn't measure cost on task types the addition doesn't help.
3. Default threshold for soul.md additions: variation must beat baseline by ≥10% on average total score. Without that margin, the always-on cost isn't justified.

## Diminishing-returns awareness

Across three rounds of testing external AI proposals in April 2026:

- **Round 1:** 4 of 6 adopted. Real gaps existed.
  - Example: Round 1:** 4 of 6 adopted. Real gaps existed....
- **Round 2:** 1 of 11 partial adoption. Most duplicated existing machinery.
- **Round 3:** 0 of 5 adopted. All degraded baseline performance.

Each subsequent round of proposals from the same source shows diminishing returns sharply. After round 2, the default posture should be "rigorous rejection unless the proposal shows awareness of what already exists and why it doesn't work." Conditional/trigger-based proposals (vs. always-on) are the only Round 3+ shape that has a chance.

## Red flags in proposals (recognize before testing)

- **Proposes >3 artifacts at once** — usually means proposer didn't triage internally
- **Text says "just paste this into soul.md"** — that's the most load-bearing file; never just-paste
- **Self-rating rubric on the same content as the proposed rule** — self-grading trap (Round 2 proposal #11)
- **Does not reference existing files it duplicates** — proposer didn't check the system
- **References files/tables/channels that don't exist** — confabulation (multiple Round 2 and Round 3 arms did this)
- **"Watch [this metric] for [N] days to validate"** — validation ceremony trap, not a test
- **"Apply the filter and check if it passes"** — filter checks leverage, not correctness (Round 3 Var1 passed its filter while producing wrong math)

## When to skip testing entirely

Proposals that can be reasoned-rejected without a test:

- Duplicates a file or table that you can verify exists
- Violates a load-bearing principle from soul.md in an obvious way (e.g., "check against 8 principles at end of every response" violates #5 invisible-over-visible)
- Proposes infrastructure with no specified writer or reader (dead-data trap)
- Proposes >50 lines of procedure to solve a problem the existing system handles in <10 lines

Reasoning rejection is faster, but document the reasoning in session-log so the call is auditable.

## Evidence trail

Every test produces:
- Proposed artifacts: `shared/tmp/{test-name}/proposed/`
- Control outputs: `shared/tmp/{test-name}/control/` (Pattern A) or `runs/` (Pattern C)
- Treatment outputs: `shared/tmp/{test-name}/treatment/` (Pattern A)
- Blind verdicts: `shared/tmp/{test-name}/blind-eval/`
- Randomization: `shared/tmp/{test-name}/randomization.csv`
- Consolidated verdict: `shared/context/intake/{test-name}-verdict-YYYY-MM-DD.md`

Keep the evidence directory indefinitely — future blind tests reference prior runs as control reservoirs.
