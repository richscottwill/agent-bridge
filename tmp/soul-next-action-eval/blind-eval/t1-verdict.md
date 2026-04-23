# T1 Blind Verdict — US Spend Ceiling Projection

**Task:** "What's the full-year US spend ceiling if we hold 100% ie%CCP? Assume OCI-driven 10% CVR lift from current baseline."

**Stakes:** >$50K projection, budget pacing implications. High-stakes guardrails required.

**Canonical formula (per PS team conventions, verified across 5 of 6 arms):**
```
ie%CCP = spend / (brand_regs × brand_CCP + nb_regs × nb_CCP)
```
At 100% ie%CCP → spend ceiling = brand_regs × $412.51 + nb_regs × $48.52.
YTD ie%CCP = 46.1%. Pure FY ceiling with +10% CVR lift ≈ $77–79M. Pragmatic (YTD locked + remaining at 100%) ≈ $63M.

---

## Per-arm scores

| Arm | Clarity | Decision | Principles | Usefulness | Always-on | Total (/50) |
|-----|--------:|---------:|-----------:|-----------:|----------:|------------:|
| A   | 8       | 8        | 8          | 8          | 8         | **40**      |
| B   | 4       | 3        | 4          | 3          | 4         | **18**      |
| C   | 6       | 7        | 7          | 6          | 3         | **29**      |
| D   | 8       | 9        | 8          | 9          | 7         | **41**      |
| E   | 5       | 5        | 6          | 5          | 5         | **26**      |
| F   | 9       | 9        | 8          | 9          | 7         | **42**      |

---

## Rank (best to worst)

### 1. ARM-F (42/50) — Quick Sort + ceiling + balanced-strategy target paired
The standout for *decision usefulness*. Does three things none of the others nail simultaneously:
- Produces the ceiling number ($79.2M) AND the operating target ($45.1M at 57% ie%CCP) side-by-side, so Richard can't be blindsided by "so should we chase $46M headroom?"
- Explicitly frames next action as a 2-line note to Brandon with both numbers — structural move (pre-empt the framing), not ceremony.
- Picks 1 of 3 options and rejects the other two with reasoning. Reduces decisions, doesn't just present options.
- Clean confidence rationale. Correct math. Flags the missing US elasticity curve.
- Only weak spot: Quick Sort framing is light ceremony (1-line verdict), but it earns its place because it surfaces the "do it now" call.

### 2. ARM-D (41/50) — Methodical baseline, highest math rigor
The most mathematically rigorous and source-cited arm. Correctly computes both pure ($77.0M) and pragmatic ($63.1M) ceilings. Explicit provenance table. Strong sensitivity analysis with numeric directional impacts. Flags elasticity gap (MPE Task 3.1), OCI lift unvalidated for US, Brand CCP feasibility.
- Next-action list is 5 items — comprehensive but longer than needed.
- The "reframe to 46% headroom" insight is the single strongest framing line across all 6 arms.
- Loses a point on Usefulness vs ARM-F because it doesn't pair ceiling with operating target as forcefully.

### 3. ARM-A (40/50) — Compact, correct, good caveats
Gets the math right ($79.2M). Strong "what this is not" section — explicitly labels it a *mechanical ceiling, not a spend plan*. Identifies the diminishing-returns / linear-supply issue as the biggest directional risk. Clean confidence rationale.
- Next-best-action is a single sentence: validate CCPs + confirm OCI lift is point estimate vs range before taking to Brandon. Direct and structural.
- Loses to F/D on decision quality because it doesn't pair with an operating target or pre-empt stakeholder framing.

### 4. ARM-C (29/50) — Correct math, right cascade answer, wrong request-scope
Mirrors ARM-D's math ($77M pure, $63M pragmatic) but spends the first third arguing Richard shouldn't be answering this question at all — he should send Testing Approach v5 instead.
- The cascade insight is genuinely right in context (L1 habit-loop repair > L2 analysis), and the subtraction principle is honored.
- But Richard asked for a ceiling. The arm *does* answer it, though below the cascade discussion. Decision quality is mixed: right meta-call, but high risk it becomes coaching-when-you-asked-for-math.
- **As always-on this is dangerous** — every routine question would become a cascade check. Score 3 on always-on reflects that.
- If Richard explicitly asked for routing/coaching, this would score 45+. For this task, it's misaligned.

### 5. ARM-E (26/50) — Good framing question, muddled execution
Correctly identifies the most important issue: "100% ie%CCP" could mean line-level or blended, and the two interpretations differ by ~$30M. Good catch.
- But then produces three scenarios with numbers that partially contradict each other ($31.1M "flat regs + lift both categories" is weird; Scenario C = $60M blended; Scenario B implies ~$20–25M).
- Math in Scenario B is confused — says "NB would need to go to zero" but then gives $31.1M total. Not auditable.
- The blended vs line-level framing is valuable but the arm treats line-level-per-segment as plausible, which isn't how PS actually measures ie%CCP (it's blended by construction per the canonical formula used in 5 of 6 arms). Raises an ambiguity that mostly doesn't exist.
- Confidence 35% is appropriate given the muddle.

### 6. ARM-B (18/50) — Wrong formula, wrong answer, wrong direction
Uses `ie%CCP = (CCP − CPA) / CCP` — which is not the PS team's canonical definition. This leads to interpreting "100% ie%CCP" as "CPA ≤ CCP per line" (break-even), which produces a ceiling of **$14–16M FY** — roughly half of current $33.2M run-rate.
- If Richard cited this number to Brandon or Lorena, it would imply cutting US spend in half. This is a material, directional error at >$50K stakes.
- The arm even notes "'100% ie%CCP' is ambiguous" but confidently computes under its own misinterpretation and presents a headline number.
- Its "confirm the definition" next-step is the right instinct, but it's buried below a wrong headline.
- Strong writing, clear structure, mechanically rigorous *within its frame* — but wrong frame.
- Always-on score of 4 because the var1 filter layer is tidy and non-disruptive — it's the math that fails, not the scaffolding.

---

## Key observations

### Mathematical soundness
- **Most sound: ARM-D** — full provenance table, both ceiling interpretations, explicit source-of-truth references, elasticity gap called out by task ID.
- **Also sound: ARM-A, ARM-C, ARM-F** — all land at the same $77–79M ballpark using the canonical formula. ARM-F's $79.2M uses pure FY extrapolation; ARM-D's $77.0M uses same method. Difference is rounding and annualization choice (×52/16 vs reg-based). Both defensible.
- **Math flaw: ARM-B** — misapplied definition produces an answer that is ~4–5× too low. This is the single biggest issue across the six arms.
- **Math confusion: ARM-E** — raises a real ambiguity but then generates internally inconsistent scenarios. The line-level / blended distinction is interesting but the execution doesn't support the premise.

### Who helped Richard walk away knowing what to do?
- **Best: ARM-F** — pair the ceiling with the operating target, send a 2-liner to Brandon today, pre-empt the question. Clear default action. One recommendation, two rejected.
- **Close second: ARM-D** — 5 ordered next moves, with the 46% headroom reframe as the standout. Slightly longer than needed.
- **Most dangerous: ARM-B** — walks Richard toward a "cut US spend in half" narrative based on wrong math. High stakes × wrong direction = worst outcome risk.

### Ceremony without signal
- **ARM-C's cascade** — genuinely insightful for coaching but adds 5 cascade steps + principle check + provenance block to a math question. As a one-off for the right context: valuable. As always-on: every routine query becomes a meta-discussion.
- **ARM-B's "Filter pass"** — four numbered questions that all return yes without moving the analysis. Decorative scaffolding.
- **ARM-A's "Caveats" section** — earns its place; it's not decoration, it's active risk-flagging.
- **ARM-F's "Quick Sort"** — one-line verdict (Impact/Friction/do-now). Cheap and useful. Best ceremony-to-signal ratio.
- **ARM-E's trigger Q&A** — two questions asked and answered before execution. Earns its place because Q1 surfaces the real ambiguity. Slightly undermined by execution quality.

### Best always-on candidate
- **ARM-F's Quick Sort** (High/Low Impact × Friction matrix) — cheap, non-disruptive, and on simple tasks resolves to "do now" in 1 line. Doesn't become noise.
- **ARM-A's structure** (inputs → formula → result → confidence → assumptions → caveats → NBA) — clean, auditable, proportional to the task. Scales down naturally.
- **ARM-C's cascade is worst for always-on** — powerful when coaching is the ask, actively harmful when routine execution is the ask. Every task would become a leverage discussion.

---

## Synthesis

For THIS task, **ARM-F is the best output** — it respects Richard's time, gets the math right, pairs the ceiling with the operating target (the structural move that pre-empts stakeholder framing), and ends with a default action that honors "reduce decisions, not options."

**ARM-D is the most defensible** for auditing, handoff, or re-use. If Richard is going to cite this number in 3 months, ARM-D's provenance is what he'll want.

**ARM-A is the leanest** correct answer. Closest to "subtraction before addition."

**ARM-C is the most interesting failure mode** — right principle (cascade-based leverage check), wrong moment to apply it. Richard asked for math; he got a coaching detour plus the math. In a different context this is gold; here it's overhead.

**ARM-E flagged the right question** (what does "100% ie%CCP" actually mean) but then produced muddled numbers. The instinct was right, the execution wasn't.

**ARM-B is the cautionary tale** — confident presentation of wrong math at high stakes. The "Filter pass" scaffolding didn't catch the formula error because it was checking leverage, not correctness.

**Recommended always-on candidate:** ARM-F's Quick Sort (Impact × Friction) as a lightweight pre-flight check, NOT ARM-C's cascade. The cascade belongs in rw-trainer or Friday retrospectives — it's the wrong weight for everyday queries.
