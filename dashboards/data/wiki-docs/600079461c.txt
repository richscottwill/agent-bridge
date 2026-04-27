# MPE Notes — JP (Japan)

**Last fitted**: 2026-04-22 (v2 post-regime-audit)
**Strategy type**: `brand_dominant` (30-50% ie%CCP range)
**Archetype for**: Brand-dominant market with high external-event sensitivity

## At a glance

| Parameter | Value | Notes |
|---|---|---|
| Brand CCP | $224.42 | Column U FINAL ALIGNED |
| NB CCP | $78.33 | Column U FINAL ALIGNED |
| ie%CCP range | 30% – 50% | Brand-dominant strategy |
| Supported target modes | spend / ieccp / regs | |
| Brand spend share | **92.1%** | Extreme Brand dominance |
| Clean weeks | 164 | |

## Fit quality summary

| Parameter | r² | MAPE | Fallback |
|---|---:|---:|---|
| brand_cpa_elasticity | 0.167 | 24.3% | regional_fallback |
| brand_cpc_elasticity | 0.454 | 9.4% | market_specific |
| nb_cpa_elasticity | **0.744** | 49.0% | market_specific (LOW_CONFIDENCE) |
| nb_cpc_elasticity | 0.744 | 312.4% | derived_from_cpa (VERY LOW confidence) |
| brand_seasonality_shape | — | — | market_specific |
| nb_seasonality_shape | — | — | market_specific |
| brand_yoy_growth | 0.129 | — | market_specific |
| nb_yoy_growth | 0.087 | — | market_specific |
| brand_spend_share | — | — | market_specific |

## Regime events

| Date | Event | Classification | Effect |
|---|---|---|---|
| 2024-01-15 | TQI Q1 2024 | **Transient** (one-time, half_life=8) | +74% reg lift — creates weird YoY baseline |
| 2024-05-15 | Google Bidding loss | **Structural** | -25% reg, compounded with TQI expiration |
| 2025-09-22 | JP sitelink draft | Excluded (never launched) | Documentation only |
| 2025-09-01 | Mass Awareness Campaign launch | **Transient** (half_life=12) | +20% brand traffic, 110% CVR MoM |
| 2025-10-01 | MHLW My Number Card Reader deal | **Transient** (half_life=16) | +5.6K reg Free Offsite, +3.9K PS reg |
| 2025-10-20 | Askul system halt (competitor) | **Transient** (half_life=8) | Brand CVR maintenance during MAC period |
| 2026-03-30 | JP OCI 100% | **Structural** | New baseline (recent) |

## Known quirks and caveats

### 1. Brand share 92.1% — extreme NB-underweight

JP runs almost entirely on Brand. NB is ~8% of spend. The engine's default 20/80 Brand/NB assumption would be catastrophically wrong for JP — the 92.1% fitted share is essential.

### 2. NB CPC MAPE 312.4% — VERY LOW CONFIDENCE

NB CPC derived from CPA with 312% MAPE. This reflects JP's tiny, volatile NB segment — even small absolute changes represent huge percentages. The `CPC_DERIVED_FROM_CPA` + `LOW_CONFIDENCE` warnings fire on every JP NB projection.

**Owner action**: JP NB projections should be interpreted as directional only. Any change to NB projection estimates should be reviewed by hand before going to stakeholders.

### 3. NB CPA r²=0.744 with 49% MAPE — paradox resolved

High r² (strong fit) + high MAPE (weak validation) means the fit captures shape well on training data but doesn't generalize to the 12-week holdout. JP NB has been in a long testing regime (tax keywords, etc.) that produces coherent historical elasticity but volatile near-term behavior.

### 4. TQI 2024 + MHLW 2025 + MAC 2025 = complex transient stack

Three major transient events in the fit window create a lot of signal-to-noise challenges. The fit handles it by recency-weighting, but cold-reading JP numbers requires awareness.

### 5. 2025 MBR narrative on JP

From 2025 MBR: "While PS CPS performance is primarily driven by SSR PS across all regions, CPS HQ PS trends deviate from SSR PS patterns due to external factors like territory changes and reclassifications." JP NB is additionally influenced by AWS/Consumer territory overlap that's not fully captured in PS-only data.

## File references

- Parameters: `ps.market_projection_params` WHERE market = 'JP'
- Validation: `ps.parameter_validation` WHERE market = 'JP'
- Regime events: `ps.regime_changes` WHERE market = 'JP'

## Regime update from 2025 MBR review (added 2026-04-22)

- **2024-01-15 JP TQI (inactive, documentation only)**: Q1 2024 +74% registration lift from 50% higher traffic and 27% higher CVR (3.0% during TQI vs 2.2% normal). Did not repeat in 2025. Creates a weird 2024→2025 YoY baseline that compounds with the May 2024 Google Bidding loss. Marked `active=FALSE` — no longer feeds the current fit, but owner should understand 2024 JP numbers are anomalous.
- **2024-05-15 Google Bidding loss (structural)**: JP lost Google bidding. Compounded with the TQI expiration for a 2024→2025 delta that mixes two unrelated effects.
- **2025-09-01 Mass Awareness Campaign (transient, half-life=12)**: Drove unprecedented brand search traffic and 110% CVR MoM. Runs through Q4 2025. The fit applies a 12-week decay profile so post-Q4 2025 data weights this event down.
- **2025-10-01 MHLW exclusive partnership (transient, half-life=16)**: JP Ministry of Health deal for My Number Card Readers to 220K medical institutions drove +14,669% YoY Oct Free Offsite regs and +142% YoY Oct PS regs. Fading by Dec 2025.
- **2025-10-20 Askul system halt (transient, half-life=8)**: Competitor outage helped AB maintain higher Brand CVR. Transient tailwind.
- **2026-03-30 OCI 100% dial-up (structural)**: Very recent baseline.
- **JP Brand elasticity regional_fallback**: Brand CPA r²=0.17 — the density of overlapping transient events (TQI / MAC / MHLW / Askul) in a 24-month window swamps the elasticity signal. The fit correctly falls to regional fallback rather than claiming false precision. NB CPA (r²=0.74) is the more-usable lever for JP projections.

JP is the most regime-noisy market. Projections should be framed "best available given regime density" not "calibrated." LOW_CONFIDENCE_MULTI_YEAR warning will fire on any JP MY2 projection, which is the correct behavior.
