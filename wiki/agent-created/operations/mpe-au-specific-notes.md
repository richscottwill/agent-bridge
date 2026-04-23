# MPE Notes — AU (Australia)

**Last fitted**: 2026-04-22
**Strategy type**: `efficiency` (no ie%CCP target)
**Primary stakeholder**: Alexis
**Archetype for**: data-limited Southern Hemisphere market
**v1 status**: Phase 1.5 baseline fit (regional_fallback). Phase 3.AU.A will upgrade to SH hybrid handling per R14.9-R14.15.

## At a glance

| Parameter | Value | Notes |
|---|---|---|
| Brand CCP | (none) | AU runs efficiency strategy, no CCP |
| NB CCP | (none) | Same |
| ie%CCP target | (not applicable) | |
| ie%CCP range | (not applicable) | |
| Supported target modes | spend / regs | ie%CCP target mode hidden in UI |
| Brand spend share | 15.4% | Recency-weighted historical; between MX (11%) and US (27%) |
| Clean weeks | 29 (below 80-week threshold) | Triggers regional_fallback on elasticity + seasonality |

## Fit quality summary

| Parameter | r² | MAPE | Fallback | Notes |
|---|---:|---:|---|---|
| brand_cpa_elasticity | 0.014 | 13.6% | regional_fallback | 29 clean weeks too few |
| brand_cpc_elasticity | 0.014 | 13.9% | derived_from_cpa | Inherits weak CPA fit |
| nb_cpa_elasticity | 0.504 | 17.1% | regional_fallback | r² OK but <80 weeks triggers fallback |
| nb_cpc_elasticity | 0.504 | 10.7% | derived_from_cpa | |
| brand_seasonality_shape | — | — | regional_fallback | |
| nb_seasonality_shape | — | — | regional_fallback | |
| brand_yoy_growth | 0.000 | — | conservative_default | <104 weeks triggers LOW_CONFIDENCE_MULTI_YEAR |
| nb_yoy_growth | 0.000 | — | conservative_default | Same |
| brand_spend_share | — | — | market_specific | 15.4% |

## Regime events that shape AU

From `ps.regime_changes`:

| Date | Event | Classification | Effect on fit |
|---|---|---|---|
| 2025-06-10 | AU PS launch — no prior baseline | **Excluded** | Market-birth marker; pre-launch data doesn't exist |
| 2026-01-01 | Adobe bid strategies implemented | **Structural** | New baseline — post-Jan-2026 is the current reality |
| 2026-02-01 | Adobe strategies stabilizing | **Excluded** (merged into 2026-01-01) | Not a separate regime |
| 2026-03-26 | Polaris LP migration (reverted 2026-04-13) | **Reverted** (short-term excluded) | Weeks 13-15 of 2026 excluded from elasticity fit |

Classification locked 2026-04-22 per R14.15.

## Known quirks and caveats

### 1. AU is below the 80-week threshold

Current fit is the honest v1 baseline: elasticity + seasonality fall back to regional curves. This is **expected** per Task 0.1 audit findings — AU has 29 clean weeks of its own data.

**Phase 3.AU.A upgrade path** (per R14.9-R14.15):
- Replace regional_fallback seasonality with **SH hybrid**: use AU-real weight where AU has ≥2 usable weeks for that calendar week; otherwise use WW seasonality shifted 26 weeks
- Each weight carries a `provenance` field (`au_actual` or `nh_shifted_w{N}`) so the owner can see which weeks are real vs shifted
- Replace regional_fallback elasticity with **WW regional curve + AU level shift** (use AU's observed spend-to-regs ratio as a multiplier on WW shape)
- Set `fallback_level = 'southern_hemisphere_hybrid'` for seasonality

**Until Phase 3.AU.A**: AU projections will behave reasonably (engine falls back to regional curves) but will not reflect Southern Hemisphere seasonality inversion. WW seasonality applied as-is to AU is not Northern Hemisphere — it's a global blend — so the bias is modest but real.

### 2. Southern Hemisphere seasonality matters more than data volume

AU's summer (December-February) is Northern Hemisphere's winter. Using unshifted NH seasonality would systematically mis-forecast every AU quarter. The Phase 3.AU.A SH-hybrid handling is specifically for this.

The WW fallback currently being applied is better than pure NH (because WW is a blend) but worse than true SH-shifted. Acceptable for v1 baseline; not acceptable for demo-grade output.

### 3. No ie%CCP target mode

Per the AU MARKET_STRATEGY (efficiency type), the UI hides the ie%CCP target option for AU. The `supported_target_modes` parameter is `["spend", "regs"]`.

Any agent or script that sends `target_mode='ieccp'` for AU will get `UNSUPPORTED_TARGET_MODE` per the engine's validation.

### 4. YoY growth is zero by design

AU has <104 weeks of data, so YoY falls to `conservative_default` (flat). The engine emits `LOW_CONFIDENCE_MULTI_YEAR` on any MY1/MY2 AU projection. This is correct behavior — we genuinely can't estimate YoY with one year of data.

**Owner action**: AU multi-year projections are flat growth baselines only until AU accumulates 2 years of post-launch data (~mid 2027).

## Refit schedule

- **Next quarterly refit**: 2026-07-15. By then AU will have ~40 clean weeks — still below the 80-week threshold but enough to tighten seasonality gap-filling.
- **Phase 3.AU.A upgrade**: before demo (2026-05-16). This replaces the v1 baseline regional_fallback with SH hybrid handling.
- **2026-01-01 Adobe regime**: accept as structural. Pre-2026 data is excluded from elasticity fits; seasonality can still use it.
- **Polaris reverted weeks (2026-W13-W15)**: already excluded by the reverted-window filter in `mpe_fitting._fetch_weekly`.

## Validation sanity envelope

Given AU's data-limited state, the sanity envelope is broad:
- AU typical monthly run-rate: ~$230-260K AUD (~$150-170K USD)
- AU typical monthly regs: ~1,100
- AU typical CPA: $200-240 AUD range, reflecting efficiency strategy

Engine projections should land near these figures when spend is set to actuals-level. Wider credible intervals are expected.

## File references

- Engine: `shared/tools/prediction/mpe_engine.py`
- Parameters: `ps.market_projection_params` WHERE market = 'AU'
- Validation: `ps.parameter_validation` WHERE market = 'AU'
- Regime events: `ps.regime_changes` WHERE market = 'AU'
- Phase 3 upgrade: Task 3.AU.A in `.kiro/specs/market-projection-engine/tasks.md`

## Regime update from 2025 MBR review (added 2026-04-22)

- **No Google Bidding loss for AU** (AU launched June 2025, post-Google-Bidding-loss era).
- **Adobe bid strategies (2026-01-01, structural)** remain the current baseline.
- **AU Q1 2026 MBR performance** (from 2025 MBR doc):
  - Jan 2026: $230K AUD spend, 32K clicks, 1.1K regs, $203 AUD CPA (flat vs OP2). NB +110% MoM investment, +73% MoM regs.
  - Feb 2026: $256K AUD spend, 27K clicks, 1.1K regs, $235 AUD CPA (vs goal $226). Regs -3% MoM on +27% NB CPA.
  - Adobe bid strategies stabilizing.
- **2026-03-26 Polaris LP reverted 2026-04-13** (already flagged as reverted).
- **AU OCI tech-readiness**: BTL for 2026 per 2025 MBR. Central team timeline dependent. Projected 2027 at earliest.

The fit quality reflects AU's 29 clean weeks accurately: all elasticity parameters fall to `regional_fallback` or `conservative_default`. Task 3.AU.A upgrade to SH hybrid handling is the path forward — document when completed.
