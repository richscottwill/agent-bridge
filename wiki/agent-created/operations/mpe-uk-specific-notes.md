# MPE Notes — UK (United Kingdom)

**Last fitted**: 2026-04-22
**Strategy type**: `balanced` (50-65% ie%CCP range)
**Archetype for**: EU5 mature market with completed OCI transition

## At a glance

| Parameter | Value | Notes |
| Brand CCP | $250.00 | Column U FINAL ALIGNED (round value from finance) |
| ie%CCP range | 50% – 65% | |
| Supported target modes | spend / ieccp / regs | |
| Brand spend share | 35.9% | Highest Brand share fit so far |
| Clean weeks | 160 | |

## Fit quality summary

| Parameter | r² | MAPE | Fallback | Notes |
|---|---:|---:|---|---|
| brand_cpa_elasticity | 0.697 | 6.0% | market_specific | Strong |
| brand_cpc_elasticity | 0.425 | 5.8% | market_specific | Acceptable |
| **nb_cpa_elasticity** | **0.169** | **36.6%** | **regional_fallback** | Below r² threshold |
| nb_cpc_elasticity | 0.311 | 6.9% | market_specific | Just above 0.30 threshold |
| brand_seasonality_shape | — | — | market_specific | |
| nb_seasonality_shape | — | — | market_specific | |
| brand_yoy_growth | 0.037 | — | market_specific | Essentially no YoY signal |
| nb_yoy_growth | 0.201 | — | market_specific | Weak |
| brand_spend_share | — | — | market_specific | 35.9% |

## Regime events

| Date | Event | Classification | Effect on fit |
|---|---|---|---|
| 2025-06-27 | OCI 25% dial-up | **Excluded** | Phase, superseded |
| 2025-07-01 | OCI 100% dial-up | **Structural** | New baseline |
| 2025-10-01 | OCI transitioned to standard | **Excluded** | Documentation note only |

## Known quirks and caveats

### 1. NB CPA elasticity fell to regional_fallback

r²=0.169 well below 0.35 threshold. UK NB spend-to-CPA relationship has been too variable to fit cleanly. Engine falls back to EU5 regional average (once EU5 constituent markets are fit and the regional curve can be computed).

**Owner action**: UK NB projections carry wider credible intervals. Interpret ie%CCP carefully when NB spend moves meaningfully.

### 2. Brand-heavy spend mix

At 35.9% Brand share, UK is the most Brand-heavy market fit so far. This tracks with UK's strategic positioning.

### 3. Brand YoY effectively zero

r²=0.037 means Brand YoY fit has almost no explanatory power. Multiple 2025 regime events (OCI 25% → 100% → transition) churn through the fit window. Flat YoY is the honest stance.

### 4. NB CPC direct fit is marginal

r²=0.311 — just above the 0.30 threshold. One more noisy quarter could trigger derived_from_cpa fallback. Monitor.

## Refit schedule

- **Next quarterly refit**: 2026-07-15
- Monitor NB CPA r² (currently 0.169, in regional_fallback)
- Monitor NB CPC r² (currently 0.311, marginal)

## File references

- Parameters: `ps.market_projection_params` WHERE market = 'UK'
- Validation: `ps.parameter_validation` WHERE market = 'UK'
- Regime events: `ps.regime_changes` WHERE market = 'UK'

## Regime update from 2025 MBR review (added 2026-04-22)

- **2024-05-15 Google Bidding loss (structural)**: UK lost Google bidding. UK ie%CCP elevated to 89% in 2024 (vs 63% in 2025) to compensate for loss.
- **2025-07-01 OCI 100% (structural)**: UK OCI launched, with -60% CPA improvement vs Control. ie%CCP pulled back to historical norms.
- **UK OCI performance (Wk 37 2025 action item)**: +455 reg since testing, +138 Wk37 alone. "Not easily visible in YoY comparisons since UK iECCP was 89% in 2024 vs 63% in 2025."
- **UK Brand competition**: heavier competition than most EU markets, with NB CVR declines -53% UK YoY vs EU4 -18% YoY (Aug 2025 period).

The fit quality for UK reflects this: Brand CPA elasticity r²=0.697 (strong), but NB CPA r²=0.169 (regional fallback) because UK NB has been operating at stable spend levels where elasticity signal is flat.
