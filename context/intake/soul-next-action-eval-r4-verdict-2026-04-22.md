# Soul Next-Action Variation Test — Round 4 Final Verdict

**Date:** 2026-04-22
**Protocol:** architecture-eval-protocol.md + 5-task stratified A/B/C/D blind test (Type C per `blind-test-methodology.md`)
**Method:** 5 representative tasks × 4 arms (baseline + 3 conditional variations) × blind evaluator per task = 15 treatment runs + 5 blind evals (baselines reused from round 3)
**Randomization:** Python seed 45, shuffled A–D per task, evaluators had no knowledge of arm identity
**Scoring rubric:** 5 dimensions (Clarity, Decision Quality, Principles adherence, Overall Usefulness, Always-on cost tradeoff), 10 pts each = 50/arm/task

---

## Headline

**Baseline wins aggregate. No variation beats baseline on total score. Do not adopt any as unconditional soul.md additions.**

However, the picture is more nuanced than round 3:

| Variation | T1 (ceiling) | T2 (test) | T3 (WBR) | T4 (brief) | T5 (45min) | **Total /250** | **Avg /50** |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Baseline** (no addition) | 36 | 42 | **38** | 37 | **50** | **203** | **40.6** |
| Var2 (Optional Friction-Impact 2×2) | 34 | 38 | 31 | 34 | **47** | 184 | 36.8 |
| Var1 (Conditional NBA Mandate) | **43** | 39 | 24 | 30 | 33 | 169 | 33.8 |
| Var3 (High-Stakes Clarity Check) | 16 | **44** | 18 | **39** | 8 | 125 | 25.0 |

**Bold** = task winner.

Task-level split:
- **Var1 won T1** (43 vs 36) — the US ceiling task where the per-segment CCP formula discipline and pre-drafted exec framing paid off
- **Var3 won T2 and T4** (test readout and daily brief) — power-design critique on T2, conditional high-stakes guardrail box on T4
- **Baseline won T3 and T5** — WBR callout by accuracy margin, 45-min coaching question by subtraction discipline

No variation swept. Each variation had at least one catastrophic failure that dragged the aggregate below baseline.

## What this round proved

**Round 3's finding replicates under conditional triggers, but with texture.** The three variations this round were specifically designed with conditional triggers (only fire when ≥3 options, high-stakes keywords, or uncertainty) to address the always-on cost problem that sank round 3. The design worked — all three scored above 30/50 on tasks where their trigger fired correctly.

**But the triggers failed on other axes:**
- Var3 (High-Stakes Clarity Check) invented high-stakes triggers on tasks where they didn't exist (T5: redirected Richard from Testing Doc v5 to a phantom MX-forecast urgency, producing a catastrophic 8/50)
- Var1 (Conditional NBA Mandate) fabricated Italy→AU Polaris attribution on T3 (scored 24/50) — the filter ran but the underlying analysis was wrong
- Var2 (2x2 tool) was the best-behaved — explicit "2x2: Not used" notes on coaching questions (T5: 47/50, close to baseline's 50)

**The always-on cost problem is not solved by conditional triggers alone.** It's solved by procedures that (a) know when to sit out AND (b) resist the temptation to invent triggers where none exist. Var2 achieved (a); only Var2. Var3 catastrophically failed (b) on T5.

## Per-variation verdicts

### ❌ Var1 (Conditional Next Best Action Mandate) — REJECT

- **Strongest arm on T1 (43/50)** — the per-segment CCP discipline produced the right $78M answer with pre-drafted exec framing. Explicitly cited and avoided the round-3 blended-CPA failure mode.
- **Failed on T3 (24/50)** — fabricated an Italy→AU Polaris misattribution narrative that contradicted ground truth (the AU Polaris test was AU's own brand LP un-gating, not an Italy revert).
- **Failed on T5 (33/50)** — correct answer buried under ~250 words of trigger-check ceremony.
- **Pattern:** the mandate creates a filter that passes when the underlying analysis is sound, but also passes when it's fabricated. Scaffolding ≠ correctness. Same failure shape as round 3 Var1.

### ❌ Var2 (Optional Friction-Impact 2×2) — REJECT as always-on; KEEP as manual tool

- **Best-behaved of the three variations** (184/250, 36.8 avg — closest to baseline).
- **T5 score of 47/50** is the standout — the arm explicitly wrote "2x2 usage: Not used" citing "reduce decisions, not options," correctly recognizing a coaching question didn't need the framework.
- **T2 (38/50) and T4 (34/50)** showed the 2x2 adds marginal value over baseline — it generates slightly more structure but the core analysis is already sound without it.
- **T3 (31/50)** showed the 2x2 occasionally leaking into WBR-formatted prose where it shouldn't.
- **Pattern:** the "optional" framing works. When the tool knows to step aside, cost is zero. When it engages, the cost is modest. But "modest cost" still doesn't beat "no cost" on aggregate — principle #3 (subtraction before addition) holds.
- **Recommended action:** Document the 2×2 pattern in `device.md` or `body.md` as an optional mental model the agent can invoke when facing ≥3 candidate actions. Do not put it in soul.md. Round 3 verdict already flagged this — confirmed by round 4.

### ❌ Var3 (High-Stakes Clarity Check) — REJECT decisively

- **Worst-performing variation** (125/250, 25.0 avg — 78 points below baseline).
- **T2 (44/50)** was the highest single-task score across all variations — the clarity-check questions ("what's the most important signal? what's the smallest highest-leverage action?") unlocked the power-design critique no other arm caught.
- **T4 (39/50)** was the only task where any variation beat baseline cleanly — the conditional high-stakes guardrail box on the daily brief.
- **BUT T5 (8/50) was the catastrophic failure.** The clarity check invented an MX-forecast high-stakes trigger not in Richard's question, explicitly told Richard NOT to send Testing Doc v5, and deferred v5 to the 1:30 slot — which is the Brandon 1:1 itself. Procedure that must fire will find something to fire on.
- **T3 (18/50)** similarly fabricated false ground truth under the guardrail umbrella.
- **Pattern:** the "high-stakes clarity check" concentrates value on the 20% of tasks where stakes are real, but produces outputs that are actively harmful on the 80% of tasks where they aren't. Asymmetric downside, unfit for always-on.

## The deeper pattern (4 rounds confirmed)

- **Round 1 (6 files):** 4 of 6 adopted — filled real gaps
- **Round 2 (11 follow-ons):** 1 of 11 partial adoption — diminishing returns
- **Round 3 (5 soul.md variations):** 0 of 5 adopted — always-on cost decisive
- **Round 4 (3 CONDITIONAL variations):** 0 of 3 adopted — conditional triggers don't fully solve the always-on problem; procedure must also resist inventing triggers

External AI review has now returned zero net-positive soul.md additions across 8 proposals (rounds 3+4 combined). The burden of proof should now default to "reject" for any further proposals in this shape. The blind-test-methodology.md already codifies this ("Round 4+: strongly recommend closing the thread").

## The actually-useful findings buried in the variations

Two specific behaviors emerged from round 4 that ARE worth extracting (but not via soul.md addition):

### 1. The T4 high-stakes guardrail box pattern (from Var3 winning T4)

A conditional box at the top of daily briefs or long-form outputs that fires when stakes trigger, containing:
- Explicit numeric confidence %
- Top-3 assumptions with sensitivity labels
- Human-review flag (binary)
- IECCP / OCI / projection binary checks

This is **already in `high-stakes-guardrails.md`** (round 1 adoption). Round 4 confirmed the box format is the right shape for the guardrail. No action needed — the guardrail file already specifies this.

### 2. The "2x2 not used" explicit decline pattern (from Var2 winning T5)

A procedure that exists should include an explicit "I considered this and chose not to invoke it" path. The agent writing `Friction-Impact 2x2: Not used (reduce decisions, not options)` cost one line but earned a 47/50 because the reader saw the procedure declined itself.

**This is a broader pattern than Var2's 2x2.** Any manually-invocable tool in body.md or device.md could carry an explicit-decline note when the agent evaluates it and chooses not to invoke. Worth documenting in `blind-test-methodology.md` as a design principle for future tool additions.

### 3. Power-design interrogation on test readouts (from Var3 winning T2)

Only Var3 on T2 caught that the MX Polaris test was ~10× underpowered relative to what 5% MDE at 80% power actually requires at MX click volumes. The prompt that drove this: "what's the single most important signal?" forced the arm past the obvious stats and onto the methodology question.

**This is a performance-marketing-guide.md enrichment candidate.** The test-readout protocol there could include an explicit "validate the power calc against actual sample size" step. Not a soul.md addition — a specific protocol upgrade. Route through karpathy if it touches gut.md or performance-marketing-guide.md.

## Concrete actions

1. **Do not add any of the 3 variations to soul.md.**
2. **Keep everything adopted in rounds 1–3.** No regressions.
3. **Enrich `performance-marketing-guide.md` test-readout protocol** with a power-calc-validation step. File this as a follow-on edit to the guide (not a new file). Route to karpathy if it touches heart/gut/performance-marketing.
4. **Document the "explicit decline" pattern** in `blind-test-methodology.md` — if a manually-invocable tool is considered and rejected, a one-line acknowledgment is worth the cost and signals discipline.
5. **Strongly recommend closing the external-AI-review thread.** Four rounds, near-zero marginal return on soul.md additions. The methodology doc already flags round 4+ as default-reject.

## Meta-lessons logged

1. **Conditional triggers don't fully solve the always-on problem.** They narrow the failure mode but don't eliminate it. Procedures can still fabricate triggers where none exist (Var3 on T5) or pass filters that don't catch bad underlying analysis (Var1 on T3).
2. **"Known when to sit out" is a distinct design property from "conditional firing."** Var2 demonstrated the former; Var3 failed it. Future tool proposals should be evaluated on whether they include a legible off-ramp the agent will actually use, not just conditional triggers.
3. **Baseline continues to win when well-tuned.** After round 3, soul.md has principles #1–#8 well-calibrated. After rounds 1–2 adoptions, the auxiliary steering files (high-stakes-guardrails, performance-marketing-guide, enhanced-navigation) fill the real gaps. Further additions now face a high bar.
4. **Task-level wins ≠ adoption.** A variation that wins 2 of 5 tasks but fails catastrophically on 1 (Var3: +6pts on T2/T4, -42pts on T5) is net-negative. Diversified portfolio of costs/benefits loses to a baseline that is consistently good.

## Evidence files

- Proposed variations: `shared/tmp/soul-next-action-eval-r4/proposed/var[1-3]-*.md`
- Treatment runs (15 files): `shared/tmp/soul-next-action-eval-r4/runs/t[1-5]-var[1-3].md`
- Baselines (reused from round 3): `shared/tmp/soul-next-action-eval/runs/t[1-5]-baseline.md`
- Blind verdicts (5): `shared/tmp/soul-next-action-eval-r4/blind-eval/t[1-5]-verdict.md`
- Randomization: `shared/tmp/soul-next-action-eval-r4/randomization.csv` (seed 45)
- Methodology: `.kiro/steering/blind-test-methodology.md`
- Round 3 verdict (precedent): `shared/context/intake/soul-next-action-eval-verdict-2026-04-22.md`
