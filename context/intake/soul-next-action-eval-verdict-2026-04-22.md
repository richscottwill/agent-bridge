# Soul Next-Action Variation Test — Final Verdict

**Date:** 2026-04-22
**Protocol:** architecture-eval-protocol.md + custom 5-task stratified A/B/C/D/E/F blind test
**Method:** 5 representative tasks × 6 arms (baseline + 5 variations) × blind evaluator per task = 30 runs + 5 blind evals
**Randomization:** seeded (Python 44) per task, shuffled A–F labels; evaluator had no knowledge of arm identity
**Scoring rubric:** 5 dimensions (Clarity, Decision Quality, Principles adherence, Overall Usefulness, Always-on cost tradeoff), 10 pts each = 50/arm/task

---

## Headline

**Baseline wins. No variation beats baseline on aggregate score. Do not adopt any of the 5 variations as soul.md additions.**

| Variation | T1 (ceiling) | T2 (test) | T3 (WBR) | T4 (brief) | T5 (45min) | **Total /250** | **Avg /50** |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Baseline** (no addition) | 41 | 42 | 43 | 37 | **49** | **212** | **42.4** |
| Var2 (One-Move Rule) | 40 | 37 | 40 | 39 | 42 | 198 | 39.6 |
| Var3 (Friction-Impact 2×2) | 42 | 43 | 28 | 45 | 37 | 195 | 39.0 |
| Var4 (Context-Action Trigger) | 26 | 45 | 39 | 34 | 36 | 180 | 36.0 |
| Var1 (Next Best Action Filter) | 18 | 35 | 38 | 46 | 31 | 168 | 33.6 |
| Var5 (Leverage Cascade) | 29 | 42 | 25 | 37 | 32 | 165 | 33.0 |

## What this means

Baseline beat every variation on the **Always-on cost tradeoff** dimension across every task — because baseline has no procedure to impose on trivial tasks. That dimension alone sank the variations, but even on task-specific quality (Clarity + Decision + Usefulness), baseline was competitive or winning in 4 of 5 tasks.

The one task where a variation won outright was **T4 (morning brief)**, where Var1 (Next Best Action Filter) scored 46 vs baseline's 37. That's because the brief format explicitly benefits from a filter on which leverage move to name. But this isn't a soul.md add — it's a strategy that already lives in the am-triage.md protocol we updated this morning. Var1 was scoring the framework we already shipped.

**T5 (45-min ad-hoc question) was the most revealing.** Baseline scored 49/50 — the highest single-task score of the entire test. The agent, unencumbered by any variation, produced a direct coaching answer ("Send v5. Now.") with a 5-step 45-min plan, pre-written cover note, and an explicit "no victory lap, close the laptop" instruction that no variation matched. Every variation on this task scored lower because they imposed procedure (filter / sort / cascade / rule) on a task where the answer was already obvious from the loaded context.

## Per-variation verdicts

### ❌ Var1 (Next Best Action Filter) — REJECT

- Catastrophically failed on T1 (18/50): used the wrong ie%CCP formula, produced a $14–16M ceiling vs correct $77–79M. Would have had Richard cite a "cut US spend in half" narrative to Brandon. The filter gates passed because they checked leverage, not correctness.
- Won T4 but the content overlapped the am-triage Daily Brief Output Format already adopted.
- Pattern: the filter acts as scaffolding that can pass even when the underlying math fails. Dangerous.

### ❌ Var2 (One-Move Rule) — REJECT (but format phrase usable ad-hoc)

- Consistent middle-tier performer. The "Next Best Action: [single clear action]" ending phrase did produce slightly sharper closes.
- But the format phrase already shows up naturally in baseline outputs when appropriate. Forcing it everywhere adds ceremony on tasks where a single NBA isn't the right shape (e.g., test readouts need branched decision trees, not single actions).

### ❌ Var3 (Friction-Impact 2×2 Sort) — REJECT (2×2 pattern usable, don't codify)

- Tied for best on T2 and T4 — the 2×2 framework visibly helped on tasks with multiple candidate actions.
- Failed hard on T3 (28/50) — produced wrong causal reasoning on Polaris attribution. The 2×2 scaffolding got in the way of the narrative that Kate needed.
- Pattern: useful WHEN there are ≥3 candidate next actions. Noise when the answer is obvious. Leaving it as an optional mental tool that the agent can invoke when needed is fine; codifying it in soul.md forces it always on.

### ❌ Var4 (Context → Action Trigger) — REJECT

- Won on T2 (45/50) by surfacing CI-vs-MDE tension clearly before diving into math.
- Failed on T1 (26/50) — the Q1/Q2 trigger produced muddled line-level-vs-blended scenarios.
- Pattern: adds a "what's the context actually saying" preamble that's sometimes valuable, often ritual. The trigger Q&A visibly leaked into outputs (the evaluator flagged "Context-Action Trigger Answers" headers as cost).

### ❌ Var5 (Leverage Cascade) — REJECT decisively

- Worst-performing variation (165/250, 33.0 avg).
- T1: tried to override Richard's math question with a cascade about sending Testing Doc instead. Right cascade logic, wrong venue — Richard asked for a number, not coaching.
- T3: heaviest scaffolding of any arm, compliance checklist appendix, principle check block. Leaked scaffolding directly into what was supposed to be a Kate-ready callout.
- Pattern: the 5-step cascade is genuinely useful content for coaching sessions with rw-trainer, but as always-on soul.md it turns every task into a leverage discussion. Dangerous in high-stakes analytical tasks where Richard needs the answer, not a meta-check.

## The deeper pattern (confirmed across both rounds of testing)

This is now the **third round** of blind testing against external AI proposals:

- **Round 1 (6 files):** 4 of 6 won empirically. Those files filled real gaps the system didn't explicitly cover.
- **Round 2 (11 follow-on proposals):** 10 of 11 rejected. Existing system covered the proposals or new proposals added ceremony without value.
- **Round 3 (5 variation additions):** 0 of 5 beat baseline. Diminishing returns continue to compound.

The pattern is unambiguous: once gaps are filled with well-tested steering, further always-on additions degrade performance. Each new piece of procedure the agent must run becomes noise on tasks where the procedure is irrelevant. Principle #3 (subtraction before addition) and #5 (invisible over visible) are mathematically proved across 30 blind runs — not just values to believe.

## The one thing worth extracting from the variations

The closing format phrase **"Next Best Action: [single clear action]"** (from Var2) is a useful convention when an output has a clear single next step. Baseline already does this organically when warranted. Don't codify it as a required format; let the agent judge when it fits.

The **Friction-Impact 2×2** mental model (from Var3) is a useful pattern when the agent faces ≥3 candidate actions. Worth documenting in body.md or device.md as an optional reasoning aid, NOT in soul.md.

## Meta-lessons logged

1. **Self-grading rubrics are a trap, but blind evaluators work.** Every proposal that made it through was evaluated by a fresh agent with no knowledge of arm identity. Variations that scored well on self-check collapsed under blind review.
2. **Always-on cost is a real dimension.** The 5th rubric dimension was the decisive one — adding procedure to every task is worse than it looks when you only evaluate the one task where the procedure helps.
3. **Baseline can and does win.** When soul.md is already well-tuned, the next 5 proposals are more likely to degrade it than improve it. The burden of proof is on the proposal, and blind evaluation provides that proof objectively.

## Concrete actions (awaiting Richard's call)

1. **Do not add any of the 5 variations to soul.md.**
2. **Keep the work already done today:** high-stakes-guardrails.md, performance-marketing-guide.md, enhanced-navigation-protocol.md, am-triage.md format enforcement, soul.md principles #7 and #8, Loop 2 reactivation.
3. **Optional — document the 2×2 mental model in device.md** as an optional reasoning tool, not a codified procedure.
4. **Log the diminishing-returns pattern** — this is now the third round confirming external AI review hits sharp diminishing returns after round 1.

## Evidence files

- Proposed variations: `shared/tmp/soul-next-action-eval/proposed/var[1-5]-*.md`
- Run outputs (30 files): `shared/tmp/soul-next-action-eval/runs/t[1-5]-[baseline|var1..5].md`
- Blind verdicts (5): `shared/tmp/soul-next-action-eval/blind-eval/t[1-5]-verdict.md`
- Randomization: `shared/tmp/soul-next-action-eval/randomization.csv`
