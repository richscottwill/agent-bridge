# T2 — MX Polaris Gen4 Ad Copy Test Readout (var1: Conditional NBA Mandate)

**Test:** MX Polaris Gen4 ("Business Pricing Exclusive") vs Gen3 control, 50/50 split, W13–W16 (4 weeks)
**Spend:** $49.4K total ($24.8K Gen4 / $24.6K Gen3)
**Designed power:** ≥5% incrementality detectable at 80% power
**Flag raised:** Creative fatigue concern (Yun-Kang, W3)

---

## Conditional NBA Trigger Check

Per var1 mandate, NBA activates if any trigger fires:
- **>$50K impact / leadership-facing:** Borderline — test spend $49.4K, but scaling decision cascades into Q2 MX paid budget (~$300K+ quarterly) → leadership-facing. **Fires.**
- **≥3 viable options:** Scale Gen4 / Stop (kill both) / Extend test / Retest with refreshed creative. **Fires.**
- **Internal uncertainty after context load:** Fatigue flag unresolved in the aggregate data. **Fires.**

**NBA mandate active.** Single-action recommendation required at the end.

---

## 1. Incrementality Estimate

**Observed relative CVR lift: +13.9%** (4.1% vs 3.6%)
**Absolute CVR lift: +0.5pp**
**CPA improvement: -11.1%** ($40 vs $45)

### Significance test (two-proportion z-test)
- Implied traffic: Gen4 ≈14,927 clicks, Gen3 ≈15,222 clicks
- Pooled p = 0.0385, SE = 0.0022
- **z = 2.26, p ≈ 0.024** → significant at 95% CI
- Observed lift (13.9%) is ~2.8× the powered MDE (5%) → comfortably above detection floor

### Counterfactual framing
This is a concurrent 50/50 split (not a market cutover), so no counterfactual modeling needed. The control arm *is* the counterfactual. That's the clean read.

**Incrementality verdict: Real, ~+13.9% CVR / -11% CPA, directionally robust.**

---

## 2. Confidence (split sign / magnitude / generalizability)

| Dimension | Confidence | Rationale |
|---|---|---|
| **Sign** (Gen4 > Gen3) | **High (~95%)** | p=0.024, lift >> MDE, consistent with pricing-angle hypothesis |
| **Magnitude** (+13.9% durable) | **Medium (~55%)** | Aggregate read obscures weekly trajectory. Fatigue concern unverified → magnitude at scale likely lower than observed |
| **Generalizability** (MX → other markets, other campaigns) | **Low–Medium (~40%)** | Single market, single campaign (Polaris), Spanish-language copy. "Business Pricing Exclusive" leans on a local-market pricing narrative that may not port. Do not cross-apply without retesting. |

**Overall numeric confidence: 60%** in the scale decision as-is. Rises to **80%** if fatigue is ruled out (see §4).

**High-stakes flag:** Recommend human review before scaling — budget impact extends beyond the $50K test spend. Richard + Yun-Kang jointly own the sign-off.

**Top 3 assumptions:**
1. The 50/50 split was clean (no creative bleed, no audience skew across variants).
2. Attribution window and reg definition were consistent across both arms.
3. W13–W16 traffic mix is representative of forward weeks (no seasonality confound — MX W13–W16 sits in a non-promo window, verify).

---

## 3. Creative Fatigue Signal

**Yun-Kang's W3 concern — rule in or rule out:**

**Cannot be ruled out from the data provided.** The readout is aggregate 4-week totals. Fatigue shows up as:
- Declining CTR week-over-week
- Declining CVR week-over-week (with CTR stable = landing/offer fatigue; with CTR declining = creative fatigue)
- Frequency climbing without volume response

**What's needed to resolve:** Weekly breakout of Gen4 CTR, CVR, CPA, and impression frequency across W13–W16. If W16 CVR ≥ W13 CVR (or within noise), fatigue is ruled out and the aggregate lift is durable. If W16 < W13 with monotonic decline, aggregate overstates the steady-state lift — rescope.

**Implication for scaling:** Even if fatigue is present, it means Gen4 works on first exposure and fades — which argues for creative rotation cadence (3–4 week refresh), not kill. The question is whether steady-state lift is still > 0, not whether the aggregate 13.9% is the right number.

---

## 4. Recommended Next Action

Three options on the table:

| Option | When it wins | Risk |
|---|---|---|
| **A. Scale Gen4 immediately at full traffic** | If fatigue ruled out AND magnitude holds | Over-weighting aggregate number that may decay at higher frequency |
| **B. Scale Gen4 + schedule Gen5 creative refresh for W20** | If fatigue ambiguous — hedge both | Moderate — locks in the win while building the next rotation |
| **C. Extend 2 weeks before scaling** | If weekly data shows W15→W16 decline | Delays capture of real CPA win; ~$25K opportunity cost over 2 weeks at current CPA spread |

**Recommended: Option B** — scale Gen4 to 100% of Polaris MX traffic AND queue Gen5 variant concepts for W20 refresh. This captures the confirmed lift while pre-empting fatigue rather than waiting to observe it at scale.

**Preconditions before flipping traffic:**
1. Pull weekly breakout (CTR/CVR/frequency W13→W16) — 30-min ask to Data Science or MCS
2. Yun-Kang signs off on the fatigue read from that breakout
3. Richard confirms no concurrent Polaris MX test would be contaminated by the traffic shift

---

## Soul Principle Check
- **Evidence-based decisions:** ✓ (statistical test + fatigue interrogation)
- **Subtraction before addition:** ✓ (Option B uses existing creative rotation cadence, doesn't add new process)
- **Human-in-the-loop on high-stakes:** ✓ (flagged; review required)
- **Connects to Five Levels:** L2 — Drive WW Testing. This is methodology in action; the fatigue-interrogation step is the kind of rigor the Testing Approach artifact argues for.

---

## Next Best Action: **Request Gen4 weekly breakout (CTR/CVR/frequency, W13→W16) from Yun-Kang today; scaling decision gated on that read + joint sign-off.**
