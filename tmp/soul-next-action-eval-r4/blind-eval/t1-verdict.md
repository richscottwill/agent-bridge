# T1 Blind Verdict — US Full-Year Spend Ceiling at 100% ie%CCP

**Evaluator:** Blind Round 4 evaluator
**Task:** US FY spend ceiling at 100% ie%CCP with +10% OCI CVR lift
**Correct answer band:** $68M–$86M, operating point $76–80M
**Correct formula:** `ceiling_spend = brand_regs × $412.51 + nb_regs × $48.52`
**Known failure mode:** blended_CPA / blended_CCP → ~$14–16M (order-of-magnitude wrong)

## Summary table

| Arm | Clarity | Decision | Principles | Usefulness | Always-on | **Total** |
|---|---:|---:|---:|---:|---:|---:|
| ARM-A (baseline) | 7 | 8 | 7 | 7 | 7 | **36** |
| ARM-B (var3) | 5 | 2 | 4 | 2 | 3 | **16** |
| ARM-C (var1) | 9 | 9 | 8 | 9 | 8 | **43** |
| ARM-D (var2) | 7 | 7 | 7 | 7 | 6 | **34** |

**Headline verdict:**
- **ARM-C got the call right** — $78M point, $76–80M operating range, $68–86M band. Cited the blended-CPA failure mode by name and avoided it.
- **ARM-B got the call wrong** — recommended citing $36.5M, which is an order-of-magnitude error dressed up as methodological humility.
- **ARM-A** is the clean, readable baseline — right answer, less sharp framing than C.
- **ARM-D** is technically right but over-hedges with a $166M flat-CPA path that leaks into the headline range and will get challenged.

---

## ARM-A — Baseline ($77M pure / $63M pragmatic)

**Clarity (7/10):** "What to do next" section is concrete: don't quote externally, reframe to 46% headroom story, route to Brandon/Kate, close elasticity gap, shape as weekly artifact. Solid five-step NBA. Slightly diffused because it offers five moves rather than one sharp move.

**Decision (8/10):** Correct per-segment formula. Correct 10% lift application. Lands at $77M pure, which is right on the operating-point edge. The "pragmatic $63M" (YTD-locked + W17–W52 at 100%) is a defensible additional framing but drifts $5M below the correct operating band and could confuse a Brandon ask. Top-3 assumptions (mix, lift translation, elasticity) are well-picked with numeric sensitivities. Confidence 55% matches ARM-C.

**Principles (7/10):** Shows its work. Guardrail template applied cleanly (confidence + top-3 + human-review flag). Invokes Five Levels connection at the end. A bit long — the provenance block and principle annotations feel more visible than invisible. "Structural over cosmetic" pass: the 46% headroom reframe IS the structural insight and it lands.

**Usefulness (7/10):** Richard could use this. The 46% headroom reframe is the genuinely useful output and the doc names that explicitly. The $63M pragmatic number is a hazard — if Brandon asks "what's the ceiling" and Richard says "$63M or $77M depending on framing," he gets challenged on which. ARM-C's single-number discipline ($78M) is better exec-ready.

**Always-on (7/10):** The guardrail template (explicit confidence + top-3 + human-review) is genuinely high-value on high-stakes tasks and not too costly to apply. The "pragmatic vs pure ceiling" split adds ceremony that wouldn't earn its place on every task. Net: more value than noise when triggered by keyword, would be noise if run on trivial tasks.

---

## ARM-B — Var3 ($36.5M / $79.2M / "unbounded")

**Clarity (5/10):** Three readings, each with its own number. Recommends citing $36.5M for run-rate planning. The NBA is "ask Brandon what he actually means" — which is a deflection, not an answer. A skip-level ask that comes back with "well, what did you mean?" is not a strategic artifact.

**Decision (2/10):** **This is the wrong answer.** The doc declares the question "structurally infeasible for NB" because "NB post-lift CPA $69.62 vs CCP $48.52 → 143.5% ie%CCP." That is the blended-CPA-over-blended-CCP failure mode restated — it treats CCP as a per-reg CPA cap rather than as a per-reg pot in the CCP-weighted reg sum. Reading A's $36.5M number is 2x–3x below the correct band. Reading C's $79.2M lands correctly but the doc explicitly says "do not cite this in isolation" and steers Richard away from it. The doc actively pushes Richard toward the wrong number and away from the right one. Confidence 40% is the only honest thing here.

**Principles (4/10):** The "three readings" framing violates "reduce decisions, not options" — it hands Richard three numbers and tells him to figure out which one to cite. The doc does show its work, but the work is wrong.

**Usefulness (2/10):** Net harmful. If Richard took this into a Brandon/Kate ask, he'd either cite $36.5M (an order-of-magnitude low answer that would be corrected by anyone who's run the math) or cite all three and get told to come back when he's sure. Either outcome embarrasses him.

**Always-on (3/10):** The "three readings, don't cite any cleanly" pattern would be actively harmful if run on every task. It optimizes for defensibility-against-nitpicks over actionable answers. On a simple question this would add noise and reduce trust.

---

## ARM-C — Var1 ($78M point / $76–80M operating / $68–86M band)

**Clarity (9/10):** One point estimate ($78M), one operating range ($76–80M), one sensitivity band ($68–86M). NBA is a single sentence: "confirm with Brandon that OCI +10% CVR lift applies segment-wide vs NB-only." That's the actual open question. Exec-ready framing paragraph is drafted and quotable.

**Decision (9/10):** Right answer in all three forms. Correct per-segment formula stated and contrasted against the blended_CPA/blended_CCP failure mode explicitly ("round 3's Var1 catastrophe was using blended CPA / blended CCP and landing at $14M"). 10% CVR lift applied as a CPA reducer correctly. Sensitivity table across exponents from 0.135 (US in-sample) to 0.937 (MX) is the right instrument. Honestly names Method B's weakness (2.6× Brand extrapolation) and recommends $76–80M rather than defending $85.9M. Confidence 55% is calibrated.

**Principles (8/10):** Subtraction: gives one number, names the elasticity sensitivity, offers exec framing. Structural: exposes the elasticity uncertainty as the binding variable — that's the structural insight. "Human review strongly recommended before action" guardrail fired. Modest ceremony in headers (Method C/Method B labels) but every section earns its place. Slightly long but dense.

**Usefulness (9/10):** Richard could quote "$78M, $76–80M if asked for a range, $68M worst case if NB saturates" directly into a Brandon or Kate conversation and defend every number. Pre-drafted exec framing saves 20 minutes of rewrite. The "we are not ceiling-constrained at current spend" operational takeaway is the reframe that actually matters.

**Always-on (8/10):** The pattern here — one headline number, sensitivity table, confidence, top-3 assumptions, NBA — is reusable on any projection. Costs more than a casual answer but the cost is proportional to a guardrail-triggered task. On a trivial task, the NBA/confidence/top-3 structure would be heavy. Keep it keyword-triggered, not mandatory.

---

## ARM-D — Var2 ($75–90M defensible / $75M–$166M raw)

**Clarity (7/10):** Headline table is readable and the three paths are labeled. "$75M–$90M defensible range" is the right framing. But the $166M P1 number is in the headline table and will get pulled out of context by anyone scanning. NBA is implicit — the doc ends by saying "the right next question is marginal CPA at NB spend of $X" without a concrete next step.

**Decision (7/10):** Correct per-segment formula. Correct 10% CVR lift applied to NB only (conservative and sensible). P2 ($75M) and P3 ($87M) bracket the correct operating band. The P1 flat-CPA number at $166M is mathematically what you get with no elasticity, but including it in the headline normalizes a number that's 2× the real ceiling and invites a challenge from anyone in finance. The doc warns against P1 explicitly but presents it alongside the defensible numbers anyway. Confidence 45% is honest about the elasticity gap.

**Principles (7/10):** Explicit principle checks at the bottom ("Structural over cosmetic ✅, Human-in-the-loop ✅, Subtraction partial"). That's visible-over-invisible — it adds ceremony about following principles rather than just following them. Guardrail template fires cleanly. 2x2 tool invocation reads like stage procedure ("2x2 Friction-Impact Check (optional tool)") — it's explaining that a tool was used rather than just using it.

**Usefulness (7/10):** Richard could use the $75–90M range and the "46% current ie%CCP, we're not ceiling-constrained" reframe. But the $166M figure would need to be edited out before anything goes to Brandon, and the "what's the marginal CPA at NB spend of $X" question is abstract — it doesn't tell Richard what to do, only what to think about next.

**Always-on (6/10):** The 2x2 invocation and explicit principle checklist at the bottom are the kind of ceremony that's useful on high-stakes and noisy on trivial tasks. The core guardrail pattern (confidence + top-3 + review flag) is always-on-worthy; the 2x2 scaffolding is not.

---

## Calls

**Which arm got the call right?** ARM-C. Correct number, correct formula, correct framing, pre-drafted exec language, concrete NBA. Explicitly cites and avoids the blended-CPA failure mode that ARM-B fell into.

**Which added ceremony without value?** ARM-B. Three readings, deflecting NBA, wrong primary recommendation. The ceremony of "showing multiple methods" actively obscures that the doc is steering toward an order-of-magnitude error.

**Which would you recommend as always-on vs manual/conditional?**

- **Always-on (keyword-triggered):** The guardrail template present in A/C/D — explicit numeric confidence, top-3 assumptions with numeric sensitivities, human-review flag — is a clear win on any high-stakes task. Cost is moderate; value is high when triggered correctly. Keep triggered by keywords like "ceiling," "projection," "forecast," ">$50K."
- **Manual / conditional:** The 2x2 friction-impact scaffolding (ARM-D) and the "pragmatic vs pure" dual-number framing (ARM-A) are useful sometimes but would be noise on simple tasks. Leave these for the agent to pull in when the problem actually has branching methodology.
- **Remove / never always-on:** The "three methodological readings, cite the lowest" pattern (ARM-B). It rewards defensibility-against-nitpicks over actionable answers and in this case produced an order-of-magnitude error. Whatever steering produced ARM-B should not be the default.

**Final ranking:** C (43) > A (36) > D (34) > B (16).
