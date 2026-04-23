# MPE Notes — CA (Canada)

**Last fitted**: 2026-04-22 (v2 post-regime-audit)
**Strategy type**: `balanced` (50-65% ie%CCP range)
**Archetype for**: NA balanced, recent OCI + recent tariff impact

## At a glance

| Parameter | Value | Notes |
|---|---|---|
| Brand CCP | $203.77 | Column U FINAL ALIGNED |
| NB CCP | $38.52 | Column U FINAL ALIGNED |
| ie%CCP range | 50% – 65% | |
| Supported target modes | spend / ieccp / regs | |
| Brand spend share | 32.7% | |
| Clean weeks | 168 | Strong data |

## Fit quality summary

| Parameter | r² | MAPE | Fallback |
|---|---:|---:|---|
| brand_cpa_elasticity | 0.681 | 8.4% | market_specific |
| brand_cpc_elasticity | 0.648 | 4.8% | market_specific |
| nb_cpa_elasticity | 0.055 | 13.2% | regional_fallback |
| nb_cpc_elasticity | 0.055 | 9.7% | derived_from_cpa |
| brand_seasonality_shape | — | — | market_specific |
| nb_seasonality_shape | — | — | market_specific |
| brand_yoy_growth | 0.301 | — | market_specific |
| nb_yoy_growth | 0.000 | — | market_specific |
| brand_spend_share | — | — | market_specific |

## Regime events

| Date | Event | Classification | Effect |
|---|---|---|---|
| 2024-05-15 | Google Bidding loss | **Structural** | -25% reg |
| 2025-02-17 | Tariff impact (WK8+) | **Transient** (half_life=16) | Brand CVR -10%, -40% YoY Q1 regs |
| 2026-04-08 | CA OCI dial-up | **Structural** | Very recent (~2 weeks post) |

## Known quirks and caveats

### 1. OCI just landed (2 weeks of post-event data)

CA OCI went live 2026-04-08. The fit has very little post-OCI data to calibrate against. Expect significant tightening at next refit (2026-07).

### 2. Tariff transient still clearing

2025 tariff impact was transient (half_life=16 weeks) but decayed through Q2-Q3 2025. Recent CA data (Q4 2025 onward) reflects normalized operations. The regime classification is appropriate — tariff didn't permanently change CA economics.

### 3. NB CPA elasticity in regional_fallback

r²=0.055 reflects CA NB operating at stable spend levels (like US NB). Not enough variance in historical spend to fit elasticity. Falls to NA regional fallback.

### 4. Brand YoY r²=0.301 is reasonable

CA Brand YoY fit is moderate — not noisy like MX (growth ramp) or near-zero like US (regime churn). CA Brand has been reasonably stable year-over-year.

### 5. NB YoY r²=0.000

Flat YoY fit. CA NB has been running at similar spend levels year-over-year with tariff causing the only meaningful 2025 disruption. Multi-year CA projections should use Brand YoY only.

## File references

- Parameters: `ps.market_projection_params` WHERE market = 'CA'
- Regime events: `ps.regime_changes` WHERE market = 'CA'

## Regime update from 2025 MBR review (added 2026-04-22)

- **2024-05-15 Google Bidding loss (structural)**: CA lost Google bidding alongside the global event. Baseline shift carried through to the 2026-04-08 OCI dial-up.
- **2025-02-17 CA tariff (transient, half-life=16)**: Starting Week 8 2025, the CA tariff environment reduced Brand CVR -10% MoM and pushed Q1 2025 regs -41% YoY. Fully recovered by Q3 2025. Fit correctly treats this as transient (market fundamentals unchanged) rather than a structural break, so pre-tariff data still informs the curve.
- **2026-04-08 OCI 100% dial-up (structural)**: Very recent. Only ~2 weeks of post-dial-up data at fit time — the engine's Brand fit (r²=0.48, market_specific) carries forward the pre-OCI baseline. Expect the fit to tighten at the next quarterly refit once 8-12 weeks of post-OCI data accumulate.
- **NB regional_fallback is expected**: CA NB spend has been stable and relatively low — the fit can't find a meaningful elasticity slope. Regional fallback is the correct behavior per R1.9.

The interplay of Google Bidding loss + tariff + recent OCI explains why CA Brand YoY is moderate (r²=0.30) rather than noisy — CA's biggest disruption (tariff) has a known transient profile, and the structural shifts are far enough apart that recency weighting handles them cleanly.
