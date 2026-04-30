# MPE Notes — DE (Germany)

**Last fitted**: 2026-04-22
**Strategy type**: `balanced` (50-65% ie%CCP range)
**Archetype for**: EU5 mature market with recent OCI structural shift

## At a glance

| Parameter | Value | Notes |
|---|---|---|
| Brand CCP | $291.76 | Column U FINAL ALIGNED |
| NB CCP | $141.26 | Highest NB CCP in EU5 |
| ie%CCP range | 50% – 65% | |
| Supported target modes | spend / ieccp / regs | |
| Brand spend share | 32.8% | Brand-heavy mix relative to EU5 peers |
| Clean weeks | 168 | Strong data set |

## Fit quality summary

| Parameter | r² | MAPE | Fallback | Notes |
|---|---:|---:|---|---|
| brand_cpa_elasticity | 0.805 | 12.8% | market_specific | Strong |
| brand_cpc_elasticity | 0.831 | 7.6% | market_specific | Strong |
| nb_cpa_elasticity | 0.352 | 12.8% | market_specific | Marginal (just above 0.35 threshold) |
| nb_cpc_elasticity | 0.352 | 21.3% | derived_from_cpa | Direct CPC fit fell below 0.30 |
| brand_seasonality_shape | — | — | market_specific | |
| nb_seasonality_shape | — | — | market_specific | |
| brand_yoy_growth | 0.445 | — | market_specific | Best YoY fit among markets so far |
| nb_yoy_growth | 0.050 | — | market_specific | Weak NB YoY signal |
| brand_spend_share | — | — | market_specific | 32.8% |

[38;5;10m> [0m## Regime events[0m[0m
[0m[0m
| Date | Event | Classification | Effect on fit |[0m[0m
|---|---|---|---|[0m[0m
| 2025-10-01 | DE OCI 100% complete | **Structural** | New baseline |
## Known quirks and caveats

### 1. Brand-heavy mix

DE runs a 32.8% Brand spend share — highest among markets fit so far (MX 11%, US 27.4%, AU 15.4%). DE PS operates with stronger brand investment relative to NB.

**Implication**: Brand moves affect DE ie%CCP more than they do in NB-heavy markets like MX. A 10% Brand uplift shifts DE ie%CCP meaningfully.

### 2. NB CPA elasticity sits at the threshold

r²=0.352 is just above the 0.35 market_specific threshold. One more noisy quarter could push it to regional_fallback. Monitor at next refit.

### 3. NB CPC fell to derived_from_cpa

Direct NB CPC fit r² below 0.30. Engine derived from CPA via R2.11. Warning `CPC_DERIVED_FROM_CPA` fires on DE NB projections.

### 4. DE has the best YoY signal so far

Brand YoY r²=0.445. Interpretation: DE has genuine Brand growth trend visible in the recency-weighted fit. Still treat multi-year projections with care — 0.445 is moderate, not strong.

## Refit schedule

- **Next quarterly refit**: 2026-07-15
- Monitor NB CPA r² (currently 0.352 — close to threshold)
- Monitor NB CPC direct fit (currently below 0.30 threshold, using derived)

## File references

- Parameters: `ps.market_projection_params` WHERE market = 'DE'
- Validation: `ps.parameter_validation` WHERE market = 'DE'
- Regime events: `ps.regime_changes` WHERE market = 'DE'

## Regime update from 2025 MBR review (added 2026-04-22)

- **2024-05-15 Google Bidding loss (structural)**: DE lost Google bidding along with the rest of WW. OCI tech-readiness was delayed from original 9/29 to 10/10 due to DMA (EU) legal requirements.
- **2025-10-01 OCI 100% dial-up (structural)**: DE OCI went live with Google learning period. Full performance visible by Dec 2025.
- **2025 CCP recalibration (2025-08-07, structural)**: Y25 New CCP vs Static: DE Brand -17% ($200>$240 static), DE NB -9% ($105>$115 static). The column U CCPs in the registry ($291.76 Brand / $141.26 NB) are the authoritative 2026 values.
- **2026-01-16 DE location targeting removed accidentally by Andrew** — impacted 1 Saturday with 39% of spend going to incorrect locations. $9K overbudget. One-off noise, does not require regime flag.
- **2026-03-18 SSR reg attribution change** (from change_log): SSR reg in DE incorrectly attributed to Direct channel starting 3/18. Investigate if this affects Brand/NB split calculations.

Fit quality remains strong post-update. DE's 32.8% Brand spend share and strong elasticity fits (Brand r²=0.805, NB r²=0.352) are defensible.
