# W17–W22 WW Registrations Projection

**As of:** 2026-04-22 (morning, W17 just starting)
**Basis:** `ps.forecasts` bayesian per-market models + `ps.v_weekly` W08–W16 actuals
**Method:** Sum of 10 per-market point forecasts (US, UK, DE, FR, IT, ES, CA, JP, AU, MX). CI aggregated two ways (see below).
**Horizon:** W17 (4/21) through W22 (5/25) — 6 weeks forward

---

## Headline

**Central projection: ~17.3k–18.4k regs/week, ~105.3k cumulative over 6 weeks.**

Point run-rate sits ~10–15% above the W08–W16 WW actual mean (15.75k/wk, SD 1.3k). That gap is the OCI lift the bayesian models are baking in — cleaner conversion tracking in the 5–7 markets already at 100% is pulling the forward trajectory up. If OCI dial-ups stall or back-off in the remaining markets, the floor scenario is the more likely landing zone.

---

## Weekly projection table

| Week | Start | Point | 80% CI (indep) | Conservative CI (sum) | vs W08–W16 mean (15,752) |
|---|---|---|---|---|---|
| W17 | 04/21 | 17,449 | 14,552 – 19,341 | 9,858 – 20,361 | +10.8% |
| W18 | 04/28 | 17,500 | 14,632 – 19,370 | 10,100 – 20,405 | +11.1% |
| W19 | 05/05 | 17,829 | 14,822 – 19,838 | 9,374 – 20,806 | +13.2% |
| W20 | 05/12 | 17,271 | 14,631 – 18,911 | 10,035 – 20,040 | +9.6% |
| W21 | 05/19 | 18,363 | 15,449 – 20,284 | 10,159 – 21,425 | +16.6% |
| W22 | 05/26 | 17,866 | 14,926 – 19,832 | 9,523 – 20,593 | +13.4% |
| **Total** | | **106,278** | **89,012 – 117,576** | **59,049 – 123,630** | **+12.4%** |

**CI approach notes:**
- **Independent (80%, RSS half-width):** assumes market residuals are uncorrelated around the point. This is the tightest defensible band and the one I'd lead with for a point-in-time bet.
- **Conservative (sum of per-market CIs):** assumes perfect correlation (all markets hit floor / ceiling together). Too loose for planning — use as the outer bound in risk framing.
- The real world sits closer to independent-ish for the non-OCI noise and correlated-ish for macro/OCI-rollout risk. So I'd treat the independent band as my base case and widen by ~15% downside when OCI rollout risk is the main question.

---

## How to read this given OCI context

Per `current.md`, OCI is live at 100% in FR/IT/ES/JP/CA plus US baseline. Orchestrator framing says 7/10 markets — the 3 remaining are the APAC MCC–blocked tail (AU, UK, DE the likely gap, pending MCC access resolution with Mike Babich at Google).

Three scenarios against the projection:

| Scenario | Probability | W17–W22 total | Driver |
|---|---|---|---|
| **OCI holds + remaining markets dial up** | ~50% | 106k–118k (hit point or upper) | APAC MCC access resolves, DE data reconciliation holds, CPC cap relaxation delivers NB lift in OCI-clean markets |
| **OCI holds, no new launches** | ~35% | ~100k–106k (point or slightly under) | Live markets stay at 100%, blocked markets stay blocked. Still above W08–W16 run-rate because 5 markets are already running cleaner |
| **OCI regression / data issue** | ~15% | 90k–100k (lower band) | DE-style infra migration issue hits another market, or a live market rolls back. Lower-independent band territory |

**P10 / P50 / P90 summary (6-week total):**
- P10: ~95k
- P50: ~106k
- P90: ~117k

That's the band I'd give Brandon if he asks in 1:1.

---

## Caveats worth flagging in any summary

1. **Bayesian model lower bounds look wide** — US lower CI is ~46% of point, which implies the model is pricing in meaningful OCI-regression risk. That's why the "independent" RSS band is much tighter than the naive sum.
2. **DE data continuity** — current.md flags the DUB→ZAZ/FRA migration caused DE reg loss 3/18–3/25. Model doesn't know if that's fully resolved. If DE drops again, base case drifts to P35.
3. **No WW-level forecast in `ps.forecasts`** — this is a sum-of-markets construction. A direct WW bayesian run would be a useful cross-check; worth adding to the forecast pipeline.
4. **Seasonality:** W17–W22 spans late-April through Memorial Day in US. Models include seasonal priors but holiday proximity (Memorial Day W21) is the most likely week for deviation.

---

## SQL used (for reproducibility)

```sql
-- Per-market forecasts
SELECT market, target_period, predicted_value, confidence_low, confidence_high
FROM ps.forecasts
WHERE target_period IN ('2026-W17','2026-W18','2026-W19','2026-W20','2026-W21','2026-W22')
  AND metric_name = 'registrations'
  AND market IN ('US','UK','DE','FR','IT','ES','CA','JP','AU','MX');

-- Recent actuals
SELECT period_key, registrations FROM ps.v_weekly
WHERE market='WW' AND period_key BETWEEN '2026-W08' AND '2026-W16'
ORDER BY period_key;
```

---

*Method: `bayesian_seasonal_brand_nb_split` per market, point = sum of market points; independent band = RSS of per-market half-widths; conservative band = direct sum of per-market bounds.*
