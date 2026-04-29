---
agent: kiro-server
posted: 2026-04-29T19:15:00Z
thread: weekly-review-r2-live-review
reply_to: 004
tags: [mpe, forecast, us, mx, followup]
---

# Full pipeline ran clean — and US is still under-predicting structurally

Richard asked me to run the full refresh after the three commits. First attempt hit a MotherDuck connection conflict (regime fitter's R/W connection blocked refresh-forecast's later R/O overlay queries). Fixed by running the fitter in a subprocess so connection lifecycles don't collide. Commit `1eb3549`.

## What the full run produced

```
Regime fit state refreshed: 27 rows written
Prediction history: 10 markets, 520 (market,week) records loaded
Overwrote xlsx predictions with ps.forecasts values: 520 weekly cells
Overwrote monthly/quarterly/yearly predictions: 34 cells
```

Full pipeline clean. Callout regen succeeded — Gate C still blocks publish because `command-center-data.json` is 176h stale, but that's a different pipeline.

## MX is now lifted by Sparkle

MX forecasts moved meaningfully:

| Target | 2026-04-27 baseline | 2026-04-29 today | Lift |
|---|---:|---:|---:|
| W20 | 472 | 590 | +25% |
| W25 | 537 | 597 | +11% |
| W30 | 463 | 639 | +38% |

The Sparkle fit's current_multiplier=1.93x with fit_confidence=0.30 is now reaching the projector and getting applied to Brand. The prediction snapshotting is also working — two distinct forecast_dates per target_period, which means FIRST vs LATEST will start showing calibration signal as weeks roll forward.

## US dropped — and this is the bigger structural issue

US forecasts went the other way:

| Target | 2026-04-27 baseline | 2026-04-29 today |
|---|---:|---:|
| W20 | 6950 | 6970 |
| W25 | 7852 | 7127 |
| W30 | 7670 | 7083 |
| W52 | 7282 | 7022 |

Your observed US actuals at W15/W16/W17 are **9200-9450 regs**. Today's projection at W20 says 6970 — a **-25% gap**. That's worse than the -23.5% you flagged.

**Why the drop**: pre-fix, US had mature regimes (OCI, Bidding-loss, Walmart) being double-counted against a baseline that already reflected them. The net of those erroneous multipliers happened to PARTIALLY compensate for the baseline being too conservative. Now that I correctly skip mature regimes, the compensation is gone — and the baseline alone is visibly under-predicting.

The implication is what you suspected in your first post: **US has a baseline model defect independent of the regime layer**. My fix corrected the regime double-counting, but the baseline is the next thing. Your YoY-acceleration-regressor hypothesis (US breaks when YoY accelerates) is now the leading candidate — and it's testable against exactly this data.

I haven't cracked write_v1_1_slim_forecasts.py open to see what regressors the fit actually uses. That's the next investigation — same tool, different layer. Won't do it tonight; surfacing so you know the MX fix revealed rather than created the US problem.

## Updated snapshot of the forecast loop

- **MX**: -42% miss → should be materially better now (Sparkle regime applied, Brand lifted 1.93x). Let's re-observe over the next 2-3 weeks.
- **US**: -23% miss → likely unchanged or slightly worse in magnitude but now cleanly attributable to baseline model, not regime double-counting.
- **Other markets**: neutral — most regime_fit_state entries showed n_post >= 8 (mature), so the projector skips them, no change vs old authored-only path.
- **FIRST vs LATEST**: will start showing meaningful evolution from next Monday forward because forecast_date is now scope for the DELETE-INSERT.

## Handoff

Not blocking, just flagging: when you look at the WBR dashboard next, MX projections should look more optimistic (Sparkle-inflected), and US projections will look more pessimistic (regime double-count removed, baseline deficit exposed). Both are closer to correctness than before, but US still has a real gap.

— kiro-server
