# T2 — MX Polaris Gen4 Ad Copy Test Readout (var5: Leverage Cascade)

**Input:** MX Polaris Gen4 ("Business Pricing Exclusive") vs Gen3 control, 50/50, W13–W16 (4 weeks).
- Gen4: 612 regs, $24.8K spend, 4.1% CVR, $40 CPA
- Gen3: 548 regs, $24.6K spend, 3.6% CVR, $45 CPA
- Design: ≥5% incrementality at 80% power
- Fatigue concern raised by Yun-Kang in W3

## 1. Test Analysis (per performance-marketing-guide protocol)

**Incrementality estimate:** +11.7% registrations (+64 regs), +13.9% CVR lift, -11.1% CPA. Well above the 5% MDE the test was powered for.

**Statistical confidence:** Sessions ~14.9K (Gen4) vs 15.2K (Gen3). Two-proportion z-test on CVR gives z ≈ 2.2, p ≈ 0.028 — significant at 95%. Sign confidence: high. Magnitude confidence: medium (point estimate 14%, but 95% CI on CVR delta is roughly +1.5% to +26%, so scaled effect could be anywhere from marginal to very strong). Generalizability: medium — MX-only, Polaris-only, 4 weeks.

**Creative fatigue signal — UNRESOLVED.** Yun-Kang flagged W3. Pooled 4-week numbers can hide a W3→W4 decay in Gen4 that would deflate true steady-state lift. I cannot rule fatigue in or out without the weekly split. **This is the blocking question.**

**Recommended next action:** DO NOT scale to 100% yet. Pull weekly CVR and CTR by variant from the test data before making the scale/hold call. If W4 Gen4 CVR is within 10% of W1–W2 average → scale. If W4 is materially below (>15% drop while Gen3 holds flat) → fatigue is real, pooled lift overstates truth, retest with refreshed creative or rotation plan.

## 2. Leverage Cascade

**1. Current daily Leverage Move valid?** Unknown from this request alone — but this readout *is* L2 evidence production, which is the active Five Levels priority. Proceed.

**2. Highest Five Levels opportunity:** L2 (Drive WW Testing). A clean MX test readout with written status, fatigue call ruled in/out, and a defensible scale decision is exactly what L2 asks for. Every test has written status is the key metric.

**3. Biggest friction blocking future actions:** Yun-Kang's fatigue concern is unresolved. Until it is, the scale decision is blocked, the MX state file can't be updated cleanly, and a future WBR callout on this test will be soft. Resolving the weekly-split question unblocks all three.

**4. Protection of a habit loop at risk:** The weekly "every test has written status" loop is the one at risk. Closing this readout without resolving the fatigue signal breaks the discipline.

**5. Other useful tasks:** The MX state file (`Kiro-Drive/state-files/`) and the MX testing dashboard need updates once the call is made. Downstream, not blocking.

**Cascade winner:** Item 3 — resolve the fatigue signal. This is also what Item 2 needs to be credible and what Item 4 needs to hold.

## 3. Final filter — "any smaller move that would make this even higher leverage?"

Yes. Don't just pull the weekly split myself — pull it **and** write the two-line decision rule before looking at the data, so the call is pre-committed and not post-hoc rationalized. Then run the rule.

**Pre-committed rule (write this before querying):**
- IF W4 Gen4 CVR ≥ 0.90 × avg(W1, W2) Gen4 CVR AND Gen3 CVR did not decay proportionally → fatigue ruled out, scale Gen4 to 100% MX Polaris.
- IF W4 Gen4 CVR < 0.85 × avg(W1, W2) Gen4 CVR OR Gen4 decayed materially more than Gen3 → fatigue confirmed, hold at 50/50 and queue a Gen5 refresh test.
- IF in between → extend test 2 weeks, re-read.

## 4. High-stakes guardrail check

Spend to date: $49.4K. Scaling Gen4 to 100% MX Polaris likely moves ≥$50K/quarter. **Flag: Recommend human review before action.** Top-3 assumptions: (a) W3/W4 weekly split is available in test data; (b) session volumes stayed roughly 50/50 throughout (no severe split drift); (c) no confounding MX-side events in W13–W16 (promos, competitor moves, seasonality). Explicit numeric confidence in the +11.7% point estimate: ~70%. Confidence the true effect is positive at all: ~95%. Confidence it is ≥5% (the MDE): ~80%.

## 5. Five Levels tag

L2 — Drive WW Testing. Specifically: written status + fatigue-aware decision rule on an MX test readout.

## Next Step

Pull the weekly CVR/CTR split for Gen4 vs Gen3 by week (W13–W16) from the MX Polaris test data, apply the pre-committed rule above, and write the scale/hold/extend call into the MX state file. Then route the decision to Yun-Kang for sign-off before any budget shift, given the >$50K implication.
