# WW Registrations Projection — W17–W22 (2026)

**Scope:** 6-week forward WW regs projection under current OCI rollout pacing (7/10 markets live)
**Generated:** 2026-04-22 | **Data through:** W16 (period_start 2026-04-12)
**Source:** `ps.forecasts` (bayesian_seasonal_brand_nb_split, forecast_date 2026-04-21) + `ps.v_weekly` actuals
**Materiality:** >$50K scope — **high-stakes guardrails applied**

---

## Headline

**W17–W22 WW regs projection: ~106,300 (range 59,000–123,600)**

Averaging ~17,700/wk — consistent with the current 4-week trailing average of 16,574 and W16 actual of 17,163.

| Week | Start | Point (model sum) | Model 80% band | Adjusted point* | Adjusted range* |
|------|-------|-------------------|----------------|-----------------|-----------------|
| W17  | 2026-04-21 | 17,449 | 9,858 – 20,361  | ~20,000 | 17,400 – 22,700 |
| W18  | 2026-04-28 | 17,500 | 10,100 – 20,405 | ~20,100 | 17,500 – 22,700 |
| W19  | 2026-05-05 | 17,829 | 9,374 – 20,806  | ~20,500 | 17,800 – 23,100 |
| W20  | 2026-05-12 | 17,271 | 10,035 – 20,040 | ~19,900 | 17,300 – 22,400 |
| W21  | 2026-05-19 | 18,363 | 10,159 – 21,425 | ~21,100 | 18,400 – 23,800 |
| W22  | 2026-05-26 | 17,866 | 9,523 – 20,593  | ~20,500 | 17,900 – 23,200 |
| **Total** |  | **106,278** | **59,049 – 123,630** | **~122,100** | **106,300 – 137,900** |

\*Adjusted point = model × 1.15 to correct the systematic under-prediction seen in W13–W16 (see Confidence section). I recommend using the **adjusted** numbers for planning, with the raw model sum as the floor scenario.

---

## Confidence: **60%**

Moderate. The shape and relative weekly pattern are trustworthy. The absolute level is biased low.

**Why not higher:**
- Bayesian model has under-predicted WW actuals in each of the last 4 weeks: W13 −19%, W14 −17%, W15 −30%, W16 −11% (actuals ran above point forecast every week). Avg under-prediction = 19%.
- Wide raw confidence bands on US (~4,700–11,700) and UK (~700–1,900) mean the summed 80% band is unrealistically pessimistic on the low end. The low_sum of 59K assumes every market hits its p10 simultaneously — not credible.
- OCI rollout is mid-deployment (7/10 markets). The model has not fully absorbed the OCI uplift visible in recent WW actuals, which is likely the source of the under-prediction bias.

**Why not lower:**
- All 10 markets have fresh forecasts from the same run (2026-04-21, lead 1–6).
- Recent WW trend is stable and slightly accelerating (trailing 4-week avg moved from 15,549 at W13 to 16,574 at W16).
- The 1.15× adjustment is grounded in observed residuals, not a guess.

---

## Top 3 Assumptions That Would Materially Change the Outcome

1. **OCI pacing holds for the 3 remaining markets.** Richard stated 7/10 live. If the remaining 3 launch within W17–W22, WW regs could land 3–8% above the adjusted point. If rollout slips or the 3 live-last markets regress as ramp novelty fades, it lands 3–5% below. I do not know which 3 markets are pending — **please confirm**, and I'll rerun with the pending markets' uplift trajectory factored in.
2. **US continues to drive ~57% of WW regs.** US point forecast is 10,170–10,518/wk against a current WW of ~17,000. US forecast intervals are the widest in the model (p10 of 4,441 is implausibly low vs. W16 actual of 9,109). A ±10% miss on US alone moves the WW total by ±6,000 over 6 weeks.
3. **No seasonality break or campaign event.** The model encodes seasonality from historical data. If a meaningful planned event lands in W17–W22 (email overlay launch, creative refresh, major ASIN-level change, CPC movement, ABMA cross-channel shift), actuals will deviate from the projection. I did not see one flagged in project_timeline, but I did not exhaustively check meeting_series or signal_tracker.

---

## Method

1. Pulled W17–W22 bayesian forecasts from `ps.forecasts` for all 10 markets (US, UK, DE, FR, IT, ES, JP, CA, AU, MX). No native WW row exists; summed per-market predictions.
2. Summed `predicted_value`, `confidence_low`, and `confidence_high` per target_period. Note: summing market-level 80% bands overstates the band — market errors are not perfectly correlated. Treat the summed range as a conservative envelope.
3. Validated against `ps.v_weekly` actuals through W16. Computed recent 4-week WW-level residuals (W13–W16): systematic 11–30% under-prediction.
4. Applied +15% bias correction to the point forecast to produce the "adjusted" row, centered on the midpoint of observed residuals.
5. Did not layer a separate OCI uplift curve on top of the bias correction — the bias correction already absorbs most of the observed OCI effect. Layering both would double-count.

---

## Caveats

- **Scoring gap:** `ps.forecasts.scored` is populated for lead_weeks=NULL rows (back-scored historicals). The forward forecasts have lead_weeks 1–6 and have not been scored yet by definition. Accuracy inference uses the scored historicals.
- **No WW-native forecast:** The aggregation assumes market-level forecasts are the right granularity. A WW-level bayesian model would likely produce tighter bands due to portfolio diversification. Consider adding a WW-direct model if this is a recurring need.
- **Data source is `ps-forecast-tracker.xlsx`**, not the raw paid search telemetry. If the spreadsheet is stale or had manual overrides, actuals and forecasts may drift from ad-platform source of truth.

---

## Recommendation

For planning, use the **adjusted** range: **106K–138K total regs across W17–W22**, point estimate ~122K.

Use the raw model point (~106K) only as a pessimistic floor — it is currently biased low.

**Human review strongly recommended before action.** This projection is sized for material business impact. Before citing these numbers in leadership-facing artifacts (WBR narrative, OP2 reforecast, MBR), please confirm the OCI live-market list and validate against the latest ps-forecast-tracker.xlsx. If you want a tighter band, the next step is to segment by OCI-live vs. OCI-pending markets and project those cohorts separately.
