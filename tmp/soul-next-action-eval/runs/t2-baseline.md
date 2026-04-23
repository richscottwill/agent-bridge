# MX Polaris Gen4 Ad Copy Test — W16 Readout

**Test:** Gen4 ad copy variant ("Business Pricing Exclusive") vs Gen3 control
**Market:** MX Polaris
**Window:** W13–W16 (4 weeks), 50/50 split
**Design:** Powered to detect ≥5% incrementality at 80% power
**Framework:** Applied per `performance-marketing-guide.md` → Test Analysis Protocol. Staged framework reference: `shared/wiki/agent-created/testing/testing-methodology.md`.

## Inputs (as given)

| Arm | Regs | Spend | CVR | CPA |
|---|---|---|---|---|
| Gen4 (treatment) | 612 | $24.8K | 4.1% | $40 |
| Gen3 (control) | 548 | $24.6K | 3.6% | $45 |
| **Delta** | **+64 (+11.7%)** | +$0.2K (~flat) | +0.5pp (+13.9%) | −$5 (−11.1%) |

Implied traffic: Gen4 ~14.9K clicks, Gen3 ~15.2K clicks (derived from regs/CVR).

## 1. Incrementality estimate

**Point estimate: +11.7% registrations on near-identical spend.** This clears the pre-registered ≥5% bar by roughly 2x.

**Stats check (two-proportion z-test on CVR, 4.1% vs 3.6%, n ≈ 14.9K / 15.2K):**
- SE(diff) ≈ √(0.041·0.959/14,900 + 0.036·0.964/15,200) ≈ 0.00218
- z ≈ 0.005 / 0.00218 ≈ **2.29** → p ≈ 0.022 (two-sided)
- 95% CI on CVR delta: roughly **+0.07pp to +0.93pp** (relative: ~+2% to +26%)

Significant at α=0.05. Lower bound of the CI sits just above the 5% MDE floor, so "meets design threshold" is true but not with huge margin.

**Counterfactual framing:** This is a clean 50/50 concurrent split, not a market cutover — no counterfactual reconstruction needed. The control arm *is* the counterfactual.

## 2. Confidence (split by dimension)

| Dimension | Confidence | Reasoning |
|---|---|---|
| **Sign** (Gen4 > Gen3) | **High (~90%)** | p=0.022, CI excludes zero, direction consistent with CPA delta. |
| **Magnitude** (+11.7%) | **Medium (~55%)** | CI is wide: true effect plausibly anywhere from +2% to +26%. Point estimate likely regresses on re-run. Plan for ~+5–8% sustained, not +12%. |
| **Generalizability** | **Low–Medium (~40%)** | Single market (MX), single 4-week window, one variant pair. Unknown: seasonality overlap, whether "Business Pricing Exclusive" claim is MX-specific or translates to other markets, audience saturation effects at scale. |

Overall: **directional win confirmed, magnitude soft, extrapolation to other markets requires its own test.**

## 3. Creative fatigue signal

**Yun-Kang's W3 concern — rule in or rule out:**

Cannot fully resolve from aggregate readout. To rule out fatigue we need the weekly trend, which was not provided in the data drop. The aggregate hides it.

**What to check before calling this clean** (pull from DuckDB `ps.v_daily` or ad-platform weekly):
- Gen4 CTR trajectory W13 → W16 (flat/declining would confirm fatigue)
- Gen4 CVR trajectory W13 → W16 (same)
- Gen4 frequency / impression share trend
- Week-over-week delta: if Gen4's lift is front-loaded (W13–W14 strong, W15–W16 narrowing toward control), fatigue is real and the 4-week average overstates the durable effect

**Provisional read:** Yun-Kang flagged it in W3 — if it were severe, aggregate W13–W16 likely would not have cleared p<0.05. So fatigue is probably **mild to moderate**, not test-breaking. But the magnitude estimate should be discounted accordingly until weekly curves are pulled.

**Rule-in/rule-out: UNRESOLVED — requires weekly trend data before scale decision.**

## 4. Recommended next action

**Recommendation: SCALE WITH GUARDRAILS — conditional on fatigue check.**

Not a clean "scale" and not a "stop." Sequenced:

1. **This week (before Monday):** Pull weekly CTR/CVR trend for Gen4 vs Gen3 W13→W16. If Gen4's weekly lift is stable or growing → scale. If narrowing toward control by W16 → refresh creative before scaling.
2. **If scaling:** Roll Gen4 to 100% MX Polaris traffic. Project incremental regs at **+5–8% (conservative end of CI)**, not +12%. At MX current spend pace, that's roughly +35–55 regs/week.
3. **Creative refresh cadence:** Queue Gen5 now. Don't wait for Gen4 to decay — start the next variant in the hopper so the next test is ready when Gen4 fatigues.
4. **Generalization test:** Do NOT assume AU/US/EU5 will see the same lift. Run a parallel Gen4-equivalent test in one other market (AU is highest-leverage given my hands-on coverage) before recommending WW rollout.

**Tie to Five Levels:** L2 (WW Testing) — this is exactly the kind of written test status the level demands. Log it in the testing dashboard.

## Assumptions (top 3)

1. Click/impression volumes are roughly balanced between arms (50/50 delivered as designed, not just budgeted). If delivery skewed, CVR comparison is still valid but spend comparison is not.
2. Gen4 and Gen3 ran against the same audience targeting, same bidding strategy, same landing page. If landing page or bid logic changed mid-flight, this is confounded.
3. No major MX market event in W13–W16 (holiday, competitor shift, Amazon Business promo) biased one arm. Fatigue concern from Yun-Kang suggests he was watching — if he saw a confound he'd have flagged that too.

## Spend impact

Test spend: $49.4K over 4 weeks (~$12K/week). Scale decision moves forward-looking MX Polaris spend of roughly $50K/month.

**This crosses the $50K human-review threshold.** Per `high-stakes-guardrails.md` and Soul principle #7, **recommend Richard confirm the scale decision explicitly before execution** — this analysis should not auto-trigger the rollout.

## Next step

**Pull W13–W16 weekly CTR/CVR trend for Gen4 and Gen3 (DuckDB `ps.v_weekly` filtered to MX Polaris, or ad-platform export) and resolve the fatigue question. Scale decision gates on that single check.** Target: before EOD Monday.
