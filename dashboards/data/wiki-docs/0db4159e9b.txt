# MPE v1.1 Slim — 10-Market Backtest Validation Report

*Phase 6.5.2 · generated 2026-04-27 · 12-week holdout · MAPE thresholds: Brand <22%, Total <25%*

[38;5;10m> [0m## Method[0m[0m
[0m[0m
Per market: hold out the last 12 weeks of `ps.v_weekly`. Project via Frequentist baseline (last-8-week training mean, per component). Flag regime-crossings within holdout—these violate baseline assumptions and inflate MAPE.
## Per-Market Results

| Market | Brand MAPE | NB MAPE | Total Regs MAPE | Total Spend MAPE | Brand Gate | Regime in window |
| --- | --- | --- | --- | --- | --- | --- |
| MX | 30.5% | 19.5% | 27.1% | 52.0% | ✗ | 2026-03-30 — Semana Santa (Holy Week) — MX shuts down, ~35% volume suppre, 2026-04-05 — MX Sparkle campaign onset W14 2026-04-05. Brand regs stepped |
| US | 5.1% | 9.7% | 7.9% | 9.9% | ✓ | 2026-03-16 — Promo launch causing CPC spikes on music keywords |
| CA | 9.3% | 10.5% | 9.9% | 6.1% | ✓ | 2026-04-08 — CA OCI dial-up planned |
| UK | 11.2% | 10.3% | 4.6% | 24.4% | ✓ | — |
| DE | 20.0% | 25.5% | 16.8% | 27.9% | ✓ | — |
| FR | 14.4% | 17.3% | 16.0% | 26.2% | ✓ | 2026-03-30 — FR OCI 100% dial-up |
| IT | 13.3% | 18.9% | 14.1% | 14.4% | ✓ | 2026-02-18 — Italy PAM paused due to 22% tax, 2026-03-30 — IT OCI 100% dial-up |
| ES | 12.9% | 17.0% | 14.9% | 11.3% | ✓ | 2026-03-30 — ES OCI 100% dial-up |
| JP | 76.7% | 57.6% | 76.3% | 14.8% | ✗ | 2026-03-30 — JP OCI 100% dial-up |
| AU | 12.1% | 21.3% | 15.5% | 28.5% | ✓ | 2026-03-26 — Polaris LP migration — gated to open pages, CVR collapsed ~3 |

## Aggregate

- Markets with Brand MAPE < 22%: **8/10** (gate: ≥8/10)
- Markets with Total MAPE < 25%: **8/10**
- Overall acceptance: **PASS** (Phase 6.5.2 gate)

## Interpretation

The Frequentist baseline is a conservative lower bound on what the full engine delivers (adding the regime stream typically improves MAPE for markets with active structural lifts). Markets failing the gate are usually:
- **Regime-crossing in the holdout window** — a step-change occurred during the   period being predicted; the baseline can't anticipate this.
- **Small-sample markets** (AU, JP) — limited weekly history makes any 8w mean noisy.
- **Campaign-heavy markets** (MX post-Sparkle) — recent Sparkle lift (W15 step from ~200   to ~400 Brand regs) creates a discontinuity the baseline smooths away.

The production engine improves on this by: (1) applying the regime stream with decay, (2) normalizing the anchor at the latest YTD week, (3) allowing the user to select scenario chips (Bayesian / Frequentist / Mixed / No lift).
