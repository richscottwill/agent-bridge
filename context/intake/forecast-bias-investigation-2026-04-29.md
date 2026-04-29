# Forecast Bias Investigation — 2026-04-29

**Context:** R2 dashboard live-probe flagged US forecast error at -23.5%, first=latest (no recalibration). Investigation expanded to all markets.

**Investigator:** kiro-local
**Source data:** `agent-bridge/dashboards/data/forecast-data.json` (`predictions_history` key)
**Probe script:** `agent-bridge/tmp/forecast-probe.py`

---

## Headline findings

1. **The pipeline is not recalibrating predictions for most markets.** 9 of 12 markets have `first_pred == latest_pred` for every historical week, with `n_preds = 1`. That includes US. The dashboard's "FIRST-PRED ERROR vs LATEST-PRED ERROR" widget is therefore showing identical numbers because there is nothing to compare — the pipeline emits one prediction per week and never revisits it. **This is a pipeline defect, not a model defect.** Markets where first≠latest has been observed: WW, MX, AU.

2. **MX is in worse shape than US.** Mean first-pred error -42.4%, 1 of 6 in CI band, 100% negative bias (every week under-predicted). MX is one of Richard's hands-on markets. If the WW callout composes in MX bullets, this is leaking into leadership views.

3. **US error pattern is periodic, not a simple level shift.** Errors go high (W1-W5), low (W7-W12), high again (W13-W15). The pattern tracks YoY growth rate: model is too conservative whenever YoY accelerates. W15 actual was +85% YoY; first-pred was -42.6% low.

4. **Market-level bias is bimodal — under-predicting markets (US, MX, UK, WW) sit alongside over-predicting markets (FR, ES, AU, IT, DE, EU5 roughly calibrated).** This rules out a single "global miscalibration" explanation. Different markets need different treatment.

---

## Per-market bias (last 6 weeks of actuals, regs)

| Market | Mean err | StDev | Neg-bias | In-CI | Recalibrating? |
|--------|---------:|------:|--------:|------:|---------------|
| US  | **-23.5%** | 12.3 | 100% | 2/6 | No |
| MX  | **-42.4%** | 14.4 | 100% | 1/6 | Yes (but still badly under) |
| WW  | -13.2% | 6.2  | 100% | 6/6 | Yes |
| UK  | -9.9%  | 14.9 | 83%  | 6/6 | No |
| JP  | -3.6%  | 8.4  | 50%  | 6/6 | No |
| CA  | -2.2%  | 5.6  | 67%  | 5/6 | No |
| EU5 | +1.9%  | 5.4  | 50%  | 6/6 | No |
| IT  | +5.7%  | 19.8 | 33%  | 5/6 | No |
| DE  | +6.4%  | 34.3 | 33%  | 4/6 | No |
| FR  | +10.8% | 11.5 | 17%  | 6/6 | No |
| ES  | +12.5% | 14.8 | 17%  | 5/6 | No |
| AU  | +21.1% | 42.2 | 33%  | 3/6 | Yes |

Error sign convention: **negative = under-predicting** (model below actual). Opposite of `forecast-data.json` stored `error_pct` which uses the reverse convention; stored values are positive when pred < actual.

---

## US week-by-week (regs)

| WK | Actual | First-pred | Latest-pred | Err% (pred vs actual) | YoY actual | Score |
|----|-------:|-----------:|------------:|-------:|---------:|-------|
| 1  | 8,111  | 6,612 | 6,612 | -18.5% | +14.7% | MISS |
| 2  | 9,071  | 6,934 | 6,934 | -23.6% | +88.7% | SURPRISE |
| 3  | 9,145  | 6,494 | 6,494 | -29.0% | +83.5% | SURPRISE |
| 4  | 8,527  | 6,370 | 6,370 | -25.3% | +71.7% | HIT |
| 5  | 8,841  | 6,967 | 6,967 | -21.2% | +100.0% | SURPRISE |
| 6  | 8,862  | 7,403 | 7,403 | -16.5% | +89.9% | HIT |
| 7  | 7,738  | 6,795 | 6,795 | -12.2% | +67.1% | HIT |
| 8  | 7,949  | 7,449 | 7,449 | -6.3%  | +55.0% | HIT |
| 9  | 8,017  | 7,306 | 7,306 | -8.9%  | +55.0% | HIT |
| 10 | 7,543  | 7,142 | 7,142 | -5.3%  | +44.6% | HIT |
| 11 | 8,292  | 7,107 | 7,107 | -14.3% | +71.6% | HIT |
| 12 | 8,151  | 7,207 | 7,207 | -11.6% | +72.7% | HIT |
| 13 | 8,670  | 5,948 | 5,948 | -31.4% | +75.9% | SURPRISE |
| 14 | 7,611  | 5,557 | 5,557 | -27.0% | +51.0% | SURPRISE |
| 15 | 9,236  | 5,300 | 5,300 | -42.6% | +85.3% | SURPRISE |
| 16 | 9,109  | 7,804 | 7,804 | -14.3% | +92.4% | MISS |

**Pattern:** Errors correlate with YoY acceleration. Mid-quarter lull (W7-W12, YoY ~+55% to +70%) = model OK. Acceleration periods (W1-W6, W13-W15 with YoY 70-100%) = model breaks.

---

## What the dashboard actually showed

The dashboard says (on US/W17):
- First-pred error: -23.5%
- Latest-pred error: -23.5%
- In-CI: 2/6 (33% vs 80% target)

All correct per the data. The data is just telling us two things at once:
1. The model is badly under-predicting US (genuinely -23.5% on average)
2. "Latest" is identical to "first" because the pipeline doesn't recalibrate

---

## Suggested fixes — prioritized

### Immediate (this week)
1. **Find and fix the MX forecast.** -42.4% error with 1/6 in CI is broken. If this is the same model family as US but worse, there's a common defect. Before a Kate-facing WBR, MX numbers need either a fix or a footnote disclaiming the forecast.
2. **Audit the recalibration pipeline.** 9/12 markets never recalibrate. Either:
   - the recalibration job isn't running for those markets, or
   - it runs but doesn't write back to `predictions_history`, or
   - the schema's `latest_*` fields were added but never wired up.
3. **Add a dashboard note when first==latest** — the current "FIRST vs LATEST" widget implies two numbers were produced and compared. When they're identical by pipeline defect, the widget is misleading.

### Near-term (next 1-2 weeks)
4. **Add YoY-acceleration as a model input.** The US pattern shows the model handles steady-state YoY but breaks on acceleration. Even a simple lagged YoY regressor should cut US error roughly in half.
5. **Different models per region.** Current one-size-fits-all produces bimodal bias (US/MX under-predict by 20-40%, FR/ES/AU over-predict by 10-20%). At minimum, separate North America / Europe / APAC / LATAM.
6. **Confidence intervals need widening for volatile markets** — DE stdev is 34%, AU stdev is 42%. A narrow CI on these markets means the "in-CI rate" looks bad even when bias is OK.

### Longer-term (Sprint 3+)
7. **Prediction snapshotting (WR-A9).** Solves the "first == latest" problem structurally — every time the model runs, write a snapshot to an archive table rather than overwriting. Enables real calibration tracking.
8. **US-specific refit** — the W13-W16 degradation is worth digging into. Was there a spend pattern shift, a new campaign launch, or a seasonal regressor missed?

---

## Environment note

I pulled this from `forecast-data.json` (the JSON the dashboard fetches). The source-of-truth for fitting lives upstream — likely in `dashboards/refresh-forecast.py` or the Harmony app. To investigate the fit process itself (what regressors, what training window, what recalibration schedule), kiro-server with DuckDB/pipeline access is the better-positioned agent.

My scope from here: I can do more JSON-level analysis, compare to OneDrive spend data if useful, and prep the leadership-facing framing. For the actual pipeline fix, handoff to kiro-server.
