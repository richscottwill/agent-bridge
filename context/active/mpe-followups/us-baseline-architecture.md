# US Baseline Model Architecture — Richard's Call

*Pulled from karpathy-queue 2026-04-29 — out of karpathy jurisdiction (heart.md / gut.md / experiment queue / hard-thing-selection only). This is MPE fit-protocol architecture, owned by kiro-server implementation + Richard's architecture decision.*

## Problem

After fixing the regime double-count in the MPE projector (young regimes apply, mature regimes skip because baseline history absorbs them), the US baseline forecast dropped 10–15% and the gap vs actuals widened to ~-22%. US is running YoY +70% to +100% per kiro-local's W1-W16 analysis; the 52-week recency-weighted fit damps this into `nb_yoy_growth = 0.39` (barely moves on refit). The baseline has a structural fit-window problem, not a regime-layer bug.

## Three candidate fixes (Richard to pick one)

### Option 1 — Conditional short half-life

Shorten recency-weighting half-life when recent YoY moves >2σ from long-window mean. Adaptive — kicks in only when acceleration is detected. Preserves stability for steady markets.

- **Pro:** Minimal surface area change; the fit still uses the same regressor set, only the recency weights mutate.
- **Con:** Introduces a regime-detection-lite inside the baseline fit, which complicates debugging ("why did this market get a different weight profile?").
- **Scope estimate:** ~100 lines in `tools/prediction/write_v1_1_slim_forecasts.py` — half-life computation + a guard clause. ~2-3 hours.

### Option 2 — Dedicated YoY-acceleration regressor

Add a feature for `yoy_growth - lag(yoy_growth, N)` to the fit. Attacks the specific failure mode (model handles steady-state YoY, breaks on acceleration) directly.

- **Pro:** Most targeted fix. The regressor is the data — if the model can't see acceleration, it can't correct for it.
- **Con:** Requires regenerating the market params table for all markets to include the new regressor column. Invalidates backtests.
- **Scope estimate:** ~200 lines across fit script + schema update + backfill. ~4-6 hours.

### Option 3 — Post-regime trajectory reweight

Current `brand_trajectory_weights` is seasonal 40% / trend 40% / regime 15% / qualitative 5%. Post-regime-onset, reweight toward trend (e.g. seasonal 25% / trend 55% / regime 15% / qualitative 5%) because post-regime dynamics are better captured by trend acceleration than long-window seasonal averaging.

- **Pro:** Config change only, no schema work. Fastest to ship.
- **Con:** Band-aid. Doesn't address the underlying "the fit doesn't see acceleration" problem — it just tells the projector to lean on the trend term more, which relies on the trend term being correctly calibrated (which is exactly what's failing on US right now).
- **Scope estimate:** ~50 lines in the projector's weight-lookup logic + config. ~1-2 hours.

## Recommendation

If Richard wants speed: **Option 3** ships tonight, buys a cycle.
If Richard wants the right fix: **Option 2** is the structural answer.
If Richard wants hedged: **Option 1** — adaptive, preserves steady-market behavior.

Option 2 is my default recommendation. The failure mode is specifically "model doesn't see acceleration" and adding the feature is the direct fix. Scope is bounded (~1 day), backtests can rerun overnight.

## Evidence

- session-log 2026-04-29 entry "US baseline deficit" (line 496)
- US actuals W1-W16 running 9200-9450; projection at W20 was 6970 (-25% gap)
- v4 refit barely moved nb_yoy_growth (0.389→0.395) confirming the fit-window problem is not a parameter problem
- W1-W6 YoY +71-100%, model errs -18 to -29%; W7-W12 YoY +44-73% stable, errs -5 to -14% OK; W13-W15 YoY +51-85%, errs -27 to -43% (kiro-local investigation)

## Priority

High — next WBR will expose the -22% US gap visually on the new error-bar calibration chart (kiro-local commit `b8c4d84`). Framing to leadership can pre-empt for one cycle; structural fix needed before this becomes a pattern.

## Next action

Richard picks Option 1 / 2 / 3. kiro-server implements.
