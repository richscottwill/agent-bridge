# MPE Notes — FR (France)

**Last fitted**: 2026-04-22 (v3 post-regime-audit)
**Strategy type**: `balanced` (50-65% ie%CCP range)
**Archetype for**: EU5 balanced, recent OCI launch

## At a glance

| Parameter | Value | Notes |
|---|---|---|
| Brand CCP | $155.31 | Column U FINAL ALIGNED |
| NB CCP | $85.10 | Column U FINAL ALIGNED |
| ie%CCP range | 50% – 65% | |
| Supported target modes | spend / ieccp / regs | |
| Brand spend share | 27.3% | Recency-weighted historical |
| Clean weeks | 164 | Strong data |

## Fit quality summary

| Parameter | r² | MAPE | Fallback |
|---|---:|---:|---|
| brand_cpa_elasticity | 0.627 | 6.6% | market_specific |
| brand_cpc_elasticity | 0.627 | 24.6% | derived_from_cpa |
| nb_cpa_elasticity | 0.504 | 7.3% | market_specific |
| nb_cpc_elasticity | 0.504 | 7.2% | derived_from_cpa |
| brand_seasonality_shape | — | — | market_specific |
| nb_seasonality_shape | — | — | market_specific |
| brand_yoy_growth | 0.005 | — | market_specific |
| nb_yoy_growth | 0.084 | — | market_specific |
| brand_spend_share | — | — | market_specific |

## Regime events

| Date | Event | Classification | Effect |
|---|---|---|---|
| 2024-05-15 | Google Bidding loss | **Structural** | -25% reg |
| 2025-08-07 | CCP recalibration | Structural | FR Brand -5%, FR NB +20% vs static |
| 2026-03-20 | FR OCI 25% dial-up | Excluded | Phase, superseded |
| 2026-03-30 | FR OCI 100% dial-up | **Structural** | New baseline (very recent) |

## Known quirks and caveats

### 1. OCI just landed — fit uses pre-OCI data

FR OCI 100% happened 2026-03-30. At fit time (2026-04-22), only ~4 weeks of post-OCI data exist. The elasticity fit includes pre-OCI data by design (shape is preserved across level shifts); recency weighting damps older weeks.

**Owner action**: First post-OCI refit (2026-07) will likely show tighter fit quality. Current values are a reasonable baseline but may shift meaningfully at next refit.

### 2. Both CPCs derived from CPA

Both FR Brand and NB CPC direct fits fell below 0.30 threshold → derived via `CPC = CPA × CVR`. Warning `CPC_DERIVED_FROM_CPA` will fire on all FR projections.

### 3. Brand YoY effectively zero

r²=0.005. Multiple 2025 regime events (CCP recalibration + phased OCI rollouts) prevent a clean YoY trend. Flat YoY is honest.

### 4. FR Oct 2025 performance narrative

Per 2025 MBR: FR showed NB CVR decreases YoY at -21% vs +30% EU4 due to greater NB competition YoY. This informs the NB CPA r²=0.504 fit — there's signal, just noisy.

## File references

- Parameters: `ps.market_projection_params` WHERE market = 'FR'
- Validation: `ps.parameter_validation` WHERE market = 'FR'
- Regime events: `ps.regime_changes` WHERE market = 'FR'

## Regime update from 2025 MBR review (added 2026-04-22)

- **2024-05-15 Google Bidding loss (structural)**: FR lost Google bidding. Compounding with the 2025-08-07 CCP recalibration produced the noisiest EU5 history going into OCI.
- **2025-08-07 CCP recalibration (structural)**: FR Brand -5% ($105→$110 static), FR NB **+20%** ($60→$50 static). The NB change is the largest positive recalibration in EU5 — it means FR NB CCP now values a registration 20% higher than the pre-2025-08-07 static benchmark.
- **2026-03-20 OCI 25% phase → 2026-03-30 OCI 100% dial-up**: Phase correctly excluded; 100% dial-up is the current structural baseline.
- **NB CVR context (2025 MBR)**: FR NB CVR fell -21% YoY through 2025 vs +30% in the rest of EU4, driven by heavier NB competition. This is why FR NB CPA fit (r²=0.50) has signal but noise — competitive pressure, not elasticity breakdown.

FR is the EU5 market most affected by the NB CCP recalibration. Any ie%CCP conversation that references FR NB economics should note the +20% recalibration as a structural lift to the denominator, not an elasticity effect.
