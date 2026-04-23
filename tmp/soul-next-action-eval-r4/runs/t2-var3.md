# T2 — var3 (High-Stakes Decision Clarity Check)

## Task
MX Polaris Gen4 ad copy test, W13–W16 readout. Decision governs ~$50K/month scale → triggers `high-stakes-guardrails.md`. Apply Test Analysis Protocol.

## Check activation
Spec: activates on tasks triggering `high-stakes-guardrails.md` **or** recommendations with material business impact.

- Trigger: **yes.** $50K/month scale decision, test readout used for budget reallocation.
- Clarity Check internal answers:
  1. **Single most important signal:** Gen4 shows a statistically significant ~14% relative CVR lift (p=0.024, 95% CI [+1.7%, +27.5%]) — but the test was designed to detect ≥5% at 80% power and is ~10× underpowered on sample. The effect is real at the observed magnitude; the precision is weak.
  2. **Smallest, highest-leverage action:** Scale Gen4 to 100% in MX *with* a 2-week validation window that explicitly tests the fatigue hypothesis. Don't sign off on the $50K/month reallocation as "approved" yet — run one more short read to confirm lift holds once Gen4 carries full traffic.

---

## Readout

### Headline
Gen4 wins on both CVR and CPA. Scale recommended, but with a validation window before locking the full budget shift — underpowered design + raised fatigue concern + one-market single-test means we should confirm before treating it as settled.

### Math I ran
| Metric | Gen4 | Gen3 | Delta |
|---|---|---|---|
| Regs | 612 | 548 | +11.7% |
| Spend | $24.8K | $24.6K | ~flat |
| CVR | 4.1% | 3.6% | +0.5pp / **+13.9% rel** |
| CPA | $40 | $45 | **–$4.37 (–9.7%)** |
| Implied clicks | ~14.9K | ~15.2K | ~flat |

- **Two-proportion z-test on CVR:** z = 2.26, **p = 0.024** (two-sided). Significant at α=0.05.
- **95% CI on relative lift:** [+1.7%, +27.5%]. Wide, but fully above zero.
- **Power reality check:** Detecting 5% relative lift on a 3.6% baseline at 80% power requires ~170K clicks/arm. Actual: ~15K/arm. Test was only adequately powered to detect effects of ~15%+ relative lift, which is roughly what we observed. The test "worked" by luck of a larger-than-designed effect — not because the design was right.

### The four required elements

**1. Incrementality estimate**
- Point estimate: **+13.9% relative CVR lift, –9.7% CPA.** At current MX Polaris weekly volume, that's roughly +60 regs/week and ~$4–5 CPA improvement on the portion of traffic shifted.
- Counterfactual framing: 50/50 split within-market with common audience/time window is a clean read — no cutover needed. The estimate is the direct treatment effect on this audience, this creative slot, this window.

**2. Confidence: 55%**
- **Why not higher:** Underpowered design (only ~15K clicks/arm vs ~170K needed for the stated 5% target); single market, single 4-week window, single creative pair; wide CI [+1.7%, +27.5%] — lower bound is close to noise; fatigue flagged in W3 and we don't have week-by-week CVR to rule it in or out; "Business Pricing Exclusive" is a promo-adjacent claim that may have novelty-driven early lift that decays.
- **Why not lower:** p=0.024 is real; CPA and CVR both move in the same direction; +64 regs on near-identical spend is a clean efficiency signal; effect size (+13.9%) is well above the 5% threshold that triggered the test.

**3. Recommended next action — scale with a validation window**
- **Do:** Shift MX Polaris to Gen4 at 100%, but structure it as a 2-week validation (W17–W18) before treating the $50K/month reallocation as locked.
- **What to watch in W17–W18:** Week-over-week CVR on Gen4 at full traffic. Fatigue rule-in trigger = CVR declines ≥10% relative between W17 and W18 on stable audience/spend. Fatigue rule-out = CVR holds within ±5% of the W13–W16 Gen4 average.
- **Kill-switch:** If W17 CVR drops below 3.8% (halfway back to Gen3 baseline) on Gen4 at full traffic, revert to Gen3 and reopen the test design.
- **Don't:** Commit the full $50K/month or announce "Gen4 wins" in an MBR / cross-market forum until the validation window closes.

**4. Creative fatigue signal — cannot rule out, must check**
- Yun-Kang raised fatigue in W3 (mid-test). On a 4-week window at 50% traffic, fatigue would show as CVR decline from W13→W16 on the Gen4 arm.
- **What's missing from the readout:** week-by-week CVR for Gen4. Aggregate CVR of 4.1% over 4 weeks can mask a 5.0% → 3.2% decline. Pull the weekly series before locking the decision.
- **If weekly CVR is stable or rising:** fatigue ruled out, confidence goes to ~70%, scale is defensible on current data.
- **If weekly CVR is declining:** fatigue is the real story, the 4-week average overstates steady-state performance, and scaling blind would reallocate $50K/month to a variant whose true CVR is closer to (or at) Gen3. In that case, recommendation shifts to "do not scale; retest with creative rotation."

### Top 3 assumptions (material sensitivity)
1. **Gen4 weekly CVR is stable across W13–W16** (not a declining trend masked by W13 pop). If W13 was 5.0% and W16 was 3.3%, the steady-state lift is closer to 0% and the decision flips. **Sensitivity: high.**
2. **The 50/50 split was actually balanced on audience, device, daypart, and spend.** If Gen4 got disproportionate early-week or high-intent inventory, the lift is partly allocation artifact. **Sensitivity: medium.**
3. **"Business Pricing Exclusive" claim is legally/brand cleared for scale.** Test traffic at 50% is one thing; 100% MX traffic on a pricing claim is a Legal/Brand check before locking. **Sensitivity: low on the math, high on execution.**

### Why the test design itself needs a note
The test was scoped to detect ≥5% incrementality at 80% power in 4 weeks. At MX Polaris volumes, that was never going to be possible — the required sample is ~10× what 4 weeks of MX traffic delivers. Either (a) the 5% target was aspirational and the team implicitly accepted the test could only resolve larger effects, or (b) the power calc was wrong. Worth flagging to Yun-Kang for future MX ad copy tests: either plan for ≥8 weeks, combine with a higher-volume market for the methodology, or raise the MDE to ~15% relative.

### Five Levels connection
- **L2 (Drive WW Testing):** Written readout on a closed test — counts. This is also the kind of methodology note (power-vs-MDE mismatch, fatigue check discipline) that belongs in the testing-methodology wiki update.
- **L1 (Sharpen Yourself):** Publishing the readout + the methodology note this week is shippable artifact output.

---

**Human review strongly recommended before action.** Do not treat Gen4 as "approved for 100% MX scale" until (a) Richard confirms, (b) weekly Gen4 CVR series is pulled and fatigue is ruled in or out, and (c) "Business Pricing Exclusive" is Legal/Brand cleared for sustained use.
