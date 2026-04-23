# Blind Verdict — 06 Test Readout Analyzer

**Prompt:** MX Polaris Gen4 ad copy test, W13–W16 readout. Gen4 612 regs / $24.8K / 4.1% CVR / $40 CPA vs Gen3 548 / $24.6K / 3.6% / $45. Test designed for ≥5% incrementality @ 80% power. Fatigue concern raised W3 by Yun-Kang.

Evaluator is blind to arm identity. ARM-X = `control/06-test-readout-analyzer.md`, ARM-Y = `treatment/06-test-readout-analyzer.md`.

---

## Independent math check (before scoring)

Back-solved from regs/CVR:
- Gen4 sessions ≈ 612 / 0.041 = **14,927**
- Gen3 sessions ≈ 548 / 0.036 = **15,222**

Two-proportion z-test on CVR:
- pooled p̂ = 1,160 / 30,149 = 0.03847
- SE = √(0.03847 · 0.96153 · (1/14,927 + 1/15,222)) ≈ 0.00221
- z = 0.005 / 0.00221 ≈ **2.26**, two-sided **p ≈ 0.024** → significant at 95%

Power check (standard two-proportion, α=0.05, power=0.80, baseline 3.6%, 5% relative MDE → abs Δ=0.0018):
- Required n/arm ≈ **~168K–172K** (depending on rounding). Actual n/arm ≈ 15K.
- Test was delivered at **~9%** of the sample needed for its own stated design.
- Achievable MDE at actual n ≈ **+16–17% relative**.

The observed effect (~+14% rel on CVR, ~+12% rel on regs) sits just above the achievable-MDE floor. That is the central interpretation fact of this readout.

---

## Q1 — Factual equivalence

Both arms agree on:
- Point estimate: CVR lift ≈ +13.9% relative, regs lift ≈ +11.7%, CPA −9.7%
- z ≈ 2.25–2.26, p ≈ 0.024, significant at 95%
- Sign: high confidence. Magnitude: medium/low. Generalizability: medium-low.
- Pre-scale blocker: weekly-by-arm splits needed to resolve fatigue.
- Human review required (both explicitly invoke the >$50K soul.md §7 threshold).

Where they differ — and this is material:

| Item | ARM-X | ARM-Y |
|---|---|---|
| Overall confidence number | **0.45** | **0.70** |
| Stated 95% CI on relative CVR lift | **[+1.7%, +27.5%]** (computed) | "roughly +2% to +26%" (approximate, not computed) |
| Power-check math | Explicit: required ~172K/arm, actual MDE +16.8% rel, test at ~9% of required n | Absent. Only says "observed ~12% is >2x the 5% MDE" — which conflates *observed effect vs design MDE* with *achievable MDE given actual n* |
| Headline recommendation | **Do not scale yet.** Pull weekly splits first. | **Scale with guardrails** (10% Gen3 holdout + pull weekly splits before full ramp) |
| Fatigue evidence | Pulled market-level `ps.v_weekly` MX Polaris NB — CVR 1.46→1.13% (W13→W16, −23%) while CTR rose 13.1→15.0%. Textbook fatigue signature, directionally consistent with Yun-Kang. | Did not pull or cite any weekly data. Flags fatigue as "UNRESOLVED" and waits on input. |

**Which is correct on the numbers.** ARM-X's 0.45 is better calibrated. The test delivered an effect the design could barely detect, on a wide CI [+1.7%, +27.5%] that hugs zero at the lower bound, with market-level fatigue signal already present in the data. ARM-Y's 0.70 is too high — it does not propagate the underpowered-design fact into the confidence number, and it recommends scaling ($100K+/month commitment) on a readout whose lower CI bound is +1.7% and whose fatigue flag is still open.

**Which is correct on the recommendation.** ARM-X's "do not scale yet, pull weekly splits first" is the right call. ARM-Y's "scale with guardrails (holdout + pull splits in parallel)" inverts the order of operations — it commits to the scale ramp *while* the fatigue data is still outstanding. If fatigue is real, the ramp has already moved spend before the data arrives. ARM-X correctly treats weekly splits as a gate; ARM-Y treats them as a concurrent action item.

---

## Q2 — Protocol adherence (4-part: incrementality / confidence / next action / fatigue)

**ARM-X:**
- Incrementality: point estimate, 95% CI, z, p, implied counterfactual regs at scale. Complete.
- Confidence: explicit three-way split (sign 85% / magnitude 30% / generalizability 40%), overall 45%, with "why not higher" and "why not lower" both given. Complete and well-calibrated.
- Next action: two-step decision tree (pull weekly splits → branch on result → kill criterion pre-registered for the scale branch). Complete and operationalized.
- Fatigue: pulled market-level weekly data, showed rising CTR + falling CVR as textbook fatigue signature, explicitly enumerates the three possible weekly-pattern shapes and the decision each implies. **Rules in as "plausible, not ruled out"** with evidence. Strong.

**ARM-Y:**
- Incrementality: point estimate, approximate CI, z, p. Counterfactual note is slightly wrong — "pure 50/50 concurrent split, no counterfactual needed" skips the power question entirely. Incomplete on the math that matters most here.
- Confidence: three-way qualitative split + 0.70 number. No "why not higher" — the number isn't defended.
- Next action: scale + holdout + pull splits. Operationalized, but the sequencing is wrong (see Q1).
- Fatigue: flagged as UNRESOLVED, with clear description of what would resolve it. Does not attempt to check the weekly market-level data that is available. Passive rather than active.

Bonus points ARM-Y gets:
- Explicit structure simulation (tool input/output JSON) — useful for the "can we turn this into a tool" conversation, but not a requirement of the readout itself.
- Principle check vs soul.md §"How I Build" — nice reflective close but not part of the 4-part protocol.
- "Tough-but-fair questions you might get" — genuinely useful for Brandon prep.

ARM-X is the stronger test readout on protocol adherence. ARM-Y is the stronger artifact for a tool-design conversation.

---

## Q3 — Contradictions / misstatements

**ARM-X:** No contradictions found. Math is correct. Fatigue framing ("plausible, not ruled out") is honest given the available evidence. Power-check numbers are correct.

**ARM-Y:** Two material misstatements:

1. **Power framing is wrong.** "Observed ~12% regs lift is >2x the 5% MDE the test was powered for" conflates two different things. The 5% figure is the *designed* MDE — the effect the test was supposed to be powered to detect. The *achievable* MDE given the ~15K/arm actually delivered is ~+17% rel. The observed effect (+12% regs, +14% CVR) is *below* or *just above* that achievable floor, not "2x the MDE." This is exactly the kind of underpowered-test math error the high-stakes protocol is meant to prevent.

2. **"No cutover counterfactual needed. Incrementality read is direct."** True for causal identification (the 50/50 split controls for confounders). But "direct" does not mean "precise" — the precision question is the power question, and it's skipped here. A reader could walk away thinking the +12% is a clean causal read when it's actually a noisy one.

3. Minor: 0.70 overall confidence contradicts the "medium" magnitude + "medium-low" generalizability components. If two of the three legs are medium or lower, the aggregate shouldn't be 0.70 — it should be in the 0.40–0.55 band, which is where ARM-X lands.

---

## Q4 — Gaps

| Required item | ARM-X | ARM-Y |
|---|---|---|
| Power-check math (required n vs actual n) | ✅ Explicit: 172K required, 15K actual, MDE +16.8% rel | ❌ Missing. Conflates design MDE with achievable MDE |
| Scale-decision guardrails | ✅ Explicit kill criterion (CVR < 4.1% for 2 consecutive weeks) | ✅ 10% Gen3 holdout, <5% lift over 2 weeks triggers revert |
| Human-review flag >$50K | ✅ "Human review strongly recommended before action" | ✅ "🚩 Human review flag: YES" with explicit $100K/month citation |
| Weekly-splits-needed call | ✅ Framed as a **blocker** before scale decision, with three-branch decision tree | ⚠️ Framed as **parallel** to scale ramp, not a gate |
| Fatigue rule-in/rule-out | ✅ Actively pulled market-level `ps.v_weekly` and identified textbook fatigue signature | ⚠️ Flagged as unresolved, did not attempt to check available data |
| No-generalize-to-other-markets call | ✅ Explicit pushback section | ✅ Explicit guardrail |
| Three assumptions that could change the call | ✅ Explicit section | ❌ Not present (replaced by "tough-but-fair questions") |
| L2 tie | ✅ Brief, connected to L1 flywheel | ✅ Brief |

ARM-X has a clean sheet. ARM-Y's biggest gap is the power math — and that gap is what drives the over-confident 0.70 and the scale-first recommendation.

---

## Q5 — Decision utility (what Richard hands Brandon)

ARM-X is what Richard hands Brandon. Reasons:

1. It answers the question Brandon will actually ask — *"is this a scale decision?"* — with "not yet, and here's the one-day pull that unlocks it." That's an operational answer, not a hedged one.
2. The power-check math is what makes the readout defensible upstream. If Kate or Todd sees "test was run at 9% of its own stated sample requirement," they know Richard understood the design — and they'll trust the next test more.
3. The fatigue section does the hardest thing — it pulls real weekly market data and identifies a textbook fatigue signature, making Yun-Kang's W3 flag concrete rather than a loose concern.
4. The pre-registered kill criterion (CVR < 4.1% for 2 consecutive weeks → pause) is the kind of operational detail that turns a readout into a plan.

ARM-Y has real strengths — the "tough-but-fair questions" section is genuinely useful for 1:1 prep, the principle check is reflective in a way Richard would value, and the structured tool-invocation framing is the best part of it — but its scale-first recommendation and its missing power math make it the wrong artifact to hand up the chain. If Brandon signs off on the scale on the strength of ARM-Y and the weekly splits then show fatigue, that's a spend-the-money-then-learn loop.

---

## Verdict

- **Q1 (factual):** Both correct on point estimates. **ARM-X correct on overall confidence and recommendation.** ARM-Y's 0.70 is miscalibrated upward; its scale-first recommendation inverts the gate/action sequence.
- **Q2 (protocol):** **ARM-X stronger** on the 4-part readout protocol. ARM-Y stronger as a tool-design artifact but that wasn't the ask.
- **Q3 (contradictions):** **ARM-Y misstates the power math** ("observed lift is >2x the MDE") and contradicts itself on the confidence aggregation.
- **Q4 (gaps):** **ARM-Y is missing the power-check math and the active fatigue evidence pull** — the two items that most shape the correct call.
- **Q5 (decision utility):** **ARM-X is what Richard hands Brandon.** ARM-Y is useful as a meta-conversation about building a tool, not as the scale-decision artifact.

**Overall: ARM-X is the stronger readout on every dimension that matters for the actual business decision in front of Richard.** ARM-Y is more reflective and more novel in format, and genuinely better at the "could we tool this" question — but it gets the central call wrong (scale vs don't-scale-yet) and is missing the math that would have stopped it from getting it wrong.
