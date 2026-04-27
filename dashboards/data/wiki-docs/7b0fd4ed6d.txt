# MPE Notes — ES (Spain)

**Last fitted**: 2026-04-22 (v2 post-regime-audit)
**Strategy type**: `balanced` (50-65% ie%CCP range)
**Archetype for**: EU5 balanced, recent OCI

## At a glance

| Parameter | Value | Notes |
|---|---|---|
| Brand CCP | $150.00 | Column U FINAL ALIGNED |
| NB CCP | $80.03 | Column U FINAL ALIGNED |
| ie%CCP range | 50% – 65% | |
| Supported target modes | spend / ieccp / regs | |
| Brand spend share | 31.3% | |
| Clean weeks | 168 | Strong data |

## Fit quality summary

| Parameter | r² | MAPE | Fallback |
|---|---:|---:|---|
| brand_cpa_elasticity | 0.484 | 8.3% | market_specific |
| brand_cpc_elasticity | 0.617 | 5.4% | market_specific |
| nb_cpa_elasticity | 0.148 | 8.1% | regional_fallback |
| nb_cpc_elasticity | 0.148 | 7.5% | derived_from_cpa |
| brand_seasonality_shape | — | — | market_specific |
| nb_seasonality_shape | — | — | market_specific |
| brand_yoy_growth | 0.167 | — | market_specific |
| nb_yoy_growth | 0.630 | — | market_specific (strong) |
| brand_spend_share | — | — | market_specific |

## Regime events

| Date | Event | Classification | Effect |
|---|---|---|---|
| 2024-05-15 | Google Bidding loss | **Structural** | -25% reg |
| 2025-08-07 | CCP recalibration | Structural | ES Brand -5%, NB ~0% |
| 2026-03-30 | ES OCI 100% | **Structural** | New baseline (very recent) |

## Known quirks and caveats

### 1. NB CPA elasticity weak; CPC derived

ES NB CPA r²=0.148 falls to regional_fallback. Per 2025 MBR: ES NB CPC increase +12% MoM, with CPA impact from overinvestment in Generic portfolio. Per-segment fit quality improves at next refit.

### 2. NB YoY strong signal (r²=0.630)

Second-highest NB YoY among markets (after IT). Reflects ES's progressive spend discipline through 2025. Not growth per se — trending through an efficiency-tightening regime.

### 3. 2025 CCP recalibration neutral for ES

ES CCP changes were smallest in EU5 (-5% Brand, ~0% NB vs static). Fit quality benefits from this stability.

## File references

- Parameters: `ps.market_projection_params` WHERE market = 'ES'
- Regime events: `ps.regime_changes` WHERE market = 'ES'

## Regime update from 2025 MBR review (added 2026-04-22)

- **2024-05-15 Google Bidding loss (structural)**: ES lost Google bidding. OCI ramp-back to 100% on 2026-03-30.
- **2025-08-07 CCP recalibration (structural)**: ES CCP changes were the mildest in EU5 — Brand -5% ($95→$100 static), NB ~0% ($55→$55 static). This stability is why ES fit quality is cleaner than FR or IT despite similar regime density.
- **2026-03-30 OCI 100% dial-up (structural)**: Very recent. New baseline.
- **NB CPA regional_fallback (r²=0.148)**: Per 2025 MBR, ES NB CPC rose +12% MoM with CPA pressure from overinvestment in Generic portfolio. The pre-OCI NB spend discipline didn't produce a clean elasticity curve. Expect tightening at next refit.

ES is a "well-behaved regime sequence" market: structural events are clean, CCP recalibration was small, and OCI is well-bounded. Fit trust is high for Brand, correctly cautious for NB.
