# MPE Notes — US (United States)

**Last fitted**: 2026-04-22
**Strategy type**: `balanced`
**Primary stakeholder**: Andrew
**Archetype for**: balanced markets with 50-65% ie%CCP range

## At a glance

| Parameter | Value | Notes |
|---|---|---|
| Brand CCP | $412.51 | Column U FINAL ALIGNED |
| NB CCP | $48.52 | Column U FINAL ALIGNED |
| ie%CCP target | (none — range-managed) | |
| ie%CCP range | 50% – 65% | Operational envelope |
| Supported target modes | spend / ieccp / regs | All three |
| Brand spend share | 27.4% | Recency-weighted historical — higher than MX (11%) as expected for a mature market |
| Clean weeks | 148 | Above 80-week threshold (per audit 2026-04-22) |

## Fit quality summary

| Parameter | r² | MAPE | Fallback | Notes |
|---|---:|---:|---|---|
| brand_cpa_elasticity | 0.850 | 9.3% | market_specific | Strong fit |
| brand_cpc_elasticity | 0.758 | 6.6% | market_specific | Strong fit |
| **nb_cpa_elasticity** | **0.054** | **35.1%** | **regional_fallback** | **See caveat below** |
| nb_cpc_elasticity | 0.054 | 7.7% | derived_from_cpa | Derived from CPA via R2.11 fallback |
| brand_seasonality_shape | — | — | market_specific | |
| nb_seasonality_shape | — | — | market_specific | |
| brand_yoy_growth | 0.277 | — | market_specific | Weak trend signal — documented below |
| nb_yoy_growth | 0.225 | — | market_specific | Weak trend signal |
| brand_spend_share | — | — | market_specific | 27.4% |

## Regime events that shape US

From `ps.regime_changes`:

| Date | Event | Classification | How the fit handles it |
|---|---|---|---|
| 2025-06-27 | OCI 25% dial-up | **Excluded** | Partial phase, superseded by 2025-09-29 100% |
| 2025-08-05 | PAM campaigns relaunch post-PD pause | **Excluded** | One-time, already absorbed |
| 2025-09-29 | US OCI Brand+NB complete (100%) | **Structural** | New baseline |
| 2025-11-12 | MCS promo page launch | **Excluded** | Small one-time |
| 2026-02-16 | PBDD promo sitelink 404 bug | **Excluded** | Fixed |
| 2026-03-16 | Promo CPC spike on music keywords | **Transient** (half-life=2) | 2-week decay applied |

## Known quirks and caveats

### 1. NB CPA elasticity is effectively non-existent (r² = 0.054)

**What it means**: NB CPA does not respond elastically to NB spend in the historical window. The fit explains 5.4% of variance — essentially no signal.

**Why it's likely**: US NB has been running at relatively stable spend levels where elasticity curves are flat. Without varied spend levels in the data, the fit can't find a meaningful slope.

**What the engine does**: Falls back to `regional_fallback` for NB CPA — uses NA regional average curve. This is the correct behavior per R1.9, but the engine doesn't yet have a populated NA regional curve because CA isn't fit yet. So the current US NB projection uses a weak direct fit until NA regional curves are in place.

**Owner action**: When projecting NB for US, expect wider credible intervals on NB regs. The Brand side of the projection is strong (r²=0.85, MAPE 9.3%). Interpret US ie%CCP carefully when NB spend moves meaningfully from the historical range.

**Refit trigger**: If a major NB spend shift happens (e.g., a strategic budget move), flag it as a regime change so the fit can use post-shift data only.

### 2. NB CPC fell to derived_from_cpa

Direct NB CPC fit r²=0.054 (below 0.30 threshold per R2.11). Engine derived CPC from CPA via `CPC = CPA × avg_CVR`. Warning `CPC_DERIVED_FROM_CPA` fires on any US NB projection.

This is not a bug — it's the R2.11 fallback path working as designed. But it means US NB CPC projections inherit the CPA's confidence (weak).

### 3. YoY growth signal is weak across both segments

Brand r²=0.28, NB r²=0.23. Neither segment shows a clean YoY trend because:
- Multiple structural regimes in 2025 (OCI, PAM relaunch, MCS promo) each shift the baseline
- Recency weighting can't fully separate regime-shift effects from organic growth

**Owner action**: Multi-year US projections should be labeled "directional" not "calibrated." VERY_WIDE_CI warning will fire on MY2.

## Refit schedule

- **Next quarterly refit**: 2026-07-15
- **NB elasticity special-attention**: if NB spend has varied by >30% from historical run-rate, attempt a fresh market-specific fit. If r² still < 0.35, keep regional_fallback and note it.
- **Annual CCP refresh**: next finance negotiation file

## Validation sanity envelope

Running `mpe_engine --scope US --period Q2 --target spend:<reasonable level>` should:
- Produce total_regs and total_spend in the historical range (US Q2 typically $3-5M spend / 8-15k regs)
- ie%CCP landing in 50-65% range
- Fire CPC_DERIVED_FROM_CPA warning for NB
- Fire DATA_LIMITED warning for NB (fallback_level=regional_fallback)

## File references

- Engine: `shared/tools/prediction/mpe_engine.py`
- Parameters: `ps.market_projection_params` WHERE market = 'US'
- Validation: `ps.parameter_validation` WHERE market = 'US'
- Regime events: `ps.regime_changes` WHERE market = 'US'

## Regime update from 2025 MBR review (added 2026-04-22)

The 2025 Paid Acq MBR/QBR document adds critical context:

- **2024-05-15 Google Bidding loss (structural, now flagged)**: US lost Google's dynamic bid optimization due to privacy concerns. This drove -25% reg decline and locked US at elevated ie%CCP (75%) through mid-2025 to compensate. OCI recovery began July 2025, with 100% rollout by September 2025.
- **2024 Q4 Walmart Business Brand competition (structural, now flagged)**: Walmart B2B began showing on >30% of "Amazon Business" branded searches. Drove Brand CPA from $44 (Y24) to $77 (Y25), +40% CPC. This is a persistent baseline shift.
- **2025-01-22 Guest test reverted 2025-02-12** (now flagged): US Guest experience PS test launched and paused — weeks 4-7 of 2025 excluded from elasticity fit.
- **2025 OCI recovery narrative**: US OCI rolled out in phases — Phase 1 8/4 (UK), test acceleration 8/25 (US Phase 2), 9/8 (US all NB), 9/29 (US NB complete). Post-9/29 is the current baseline.

The engine's US Brand CPA elasticity (r²=0.85, MAPE 9.2%) holds up well because Brand dynamics track Walmart competition (which is the dominant post-2024-Q4 signal). NB CPA elasticity falls to regional fallback because Walmart competition compresses Brand CPC — NB never responded elastically in the post-OCI window yet.

Implication for projections: US ie%CCP projections should carry a note that NB CPA elasticity is in fallback state and will tighten once we have 12+ months of post-OCI stable data.
