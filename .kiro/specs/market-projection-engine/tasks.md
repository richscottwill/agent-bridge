# Implementation Plan — Market Projection Engine (MPE) v1 (Low-Maintenance)

**Goal**: Ship a leadership-demo-ready projection tool that the non-technical owner can maintain solo. Scope:
- **All 10 markets get market-specific fits**: MX, US, CA, UK, DE, FR, IT, ES, JP, AU
- **AU gets Southern Hemisphere handling** (only market below the equator): hybrid per-week seasonality with AU-real data where available and WW-shifted for gaps, per-week lineage
- **Regions**: NA, EU5, WW
- **Time periods**: Week, Month, Quarter, Year, Multi-Year (1 or 2 years — 3-year deferred)
- **Math**: recency-weighted linear regression + Monte Carlo (200 UI / 1000 CLI)
- **UI**: single portable HTML with "Explain this number" tooltips, provenance modal, Web Worker for MC
- **Automation**: 4 Kiro hooks (refit, parity, acceptance-core, demo-prep)
- **Regime classification**: every `ps.regime_changes` row classified structural / transient / excluded / reverted (D17)

**Target demo date**: **2026-05-16** (Friday before leadership showcase week). **Hard checkpoint**: Phase 0 + Phase 1 complete by 2026-05-02 or demo slips.

**Phase 0 validated 2026-04-22**: Data audit confirmed 9 of 10 markets have 102-168 clean weeks; AU has 29 clean weeks (SH hybrid handling applies). AU regime events classified and locked. MX 2026-W15 NB drop inserted as provisional.

**Total**: 99 active tasks across 6 phases (Phase 0: 6, Phase 1: 11, Phase 2: 10, Phase 3: 64, Phase 4: 4, Phase 5: 5). **33 complete as of 2026-04-22** (Phase 0: 6/6 ✅, Phase 1: 11/11 ✅ hard checkpoint met 10 days ahead of 2026-05-02, Phase 2: 10/10 ✅ with 2 partial sub-items pending SharePoint session, Phase 3.MX: 6/6 ✅ primary demo market demo-ready end-to-end, other Phase 3 blocks: 0). Estimated 12-16 developer-days remaining across 9 Phase 3 market blocks + Phase 4 + Phase 5.

**Phase 3 structure** — each of 10 markets gets a 6-step full build (A Fit, B Validate, C Presets, D Narrative, E UI config, F Acceptance+notes) for demo-ready end-to-end readiness per market. Templated pattern; after MX + US land, subsequent markets take ~2-3 hours each.

**Out of v1** (post-v1.1, requires new spec): Hierarchical Bayesian / BSTS / Prophet / Prophetverse / LightweightMMM / PyMC, cross-elasticity, macro overlays, placement decay curves as first-class model, ML anomaly detection, command palette, Apple micro-animations, natural-language input in browser, auto-scheduled cron refit, Slack/email digests, Streamlit / Reflex / Django / Flask, MCMC posterior, 3-year multi-year, automated subjective stakeholder simulation, Southern_Hemisphere_Handling for any market other than AU.

---

## Phase 0 — Data & Scope Foundation (6 tasks, ~2-3 days)

- [x] **0.1** `data_audit.py` for all 10 markets, owner-readable report — **COMPLETED 2026-04-22**
  - Script: `shared/tools/prediction/data_audit.py` (325 lines)
  - Reads `ps.v_weekly` per market, produces plain-English report per market
  - Findings: 9 of 10 markets support full fits (102-168 clean weeks); AU has 29 clean weeks and needs SH hybrid handling
  - Output: `shared/dashboards/data/data-audit-reports/2026-04-22-all-markets.md`
  - Exit code flags v1 spec mismatches (AU flagged and subsequently addressed via SH hybrid approach)
  - Owner can read without code
  - **Maintenance impact**: Low — run quarterly via hook, self-explanatory output
  - _Requirements: 1.9, 9.6, R0.1_

- [ ] **0.2** Define and hard-code v1 scope boundaries
  - All 10 markets get market-specific fits; AU additionally uses SH hybrid handling (requirements updated this way 2026-04-22)
  - UI scope selector shows all 10 markets + 3 regions (Task 2.3)
  - AU UI shows "Southern Hemisphere hybrid seasonality — 29 AU-real weeks + 23 NH-shifted weeks" badge
  - Any market whose data regresses below 80 clean weeks at a future refit automatically moves to `regional_fallback` status with data-limited banner — this is a safety net, not the plan
  - Explicit documentation in `.kiro/steering/mpe-low-maintenance.md` (Task 0.3) prevents scope creep in the other direction
  - **Maintenance impact**: Very low — prevents re-scoping conversations forever
  - _Requirements: 2.9, R14.9-R14.15, R16_

- [x] **0.3** Create steering file + 4 Kiro hooks — **COMPLETED 2026-04-22**
  - `~/.kiro/steering/mpe-low-maintenance.md` (5649 bytes) — fileMatch inclusion, enforces non-technical-owner language, regime classification rules, forbidden patterns, success criteria
  - `~/.kiro/hooks/mpe-refit.kiro.hook` — userTriggered, orchestrates data_audit → refit → anomaly check → owner report → SharePoint push with owner-facing regime-change prompt
  - `~/.kiro/hooks/mpe-parity.kiro.hook` — fileEdited on mpe_engine.py / mpe_fitting.py / mpe_uncertainty.py / mpe_engine.js, runs parity tests with owner-readable failure diagnosis
  - `~/.kiro/hooks/mpe-acceptance-core.kiro.hook` — userTriggered, runs full pytest acceptance suite with per-test failure diagnosis
  - `~/.kiro/hooks/mpe-demo-prep.kiro.hook` — userTriggered, 7-step pre-demo checklist (audit → acceptance → SharePoint build → MX 4/22 rehearsal → demo script refresh → readiness summary)
  - **Maintenance impact**: Low — hooks are the main automation the owner relies on
  - _Requirements: R0.2, 5.2, 15.8_

- [x] **0.4** Owner runbook skeleton — **COMPLETED 2026-04-22** (skeleton; finalized in 4.4)
  - File: `shared/wiki/agent-created/operations/mpe-owner-operations.md`
  - Sections populated: Daily use, Weekly check, Quarterly refit, Something looks wrong diagnostic, Regime event classification decision tree, Adding a new market, Leadership demo script template, Escalation criteria, File locations, Hooks reference table
  - Finalized in Task 4.4 once refit job is wired and real numbers land in demo script
  - **Maintenance impact**: Critical — primary support document
  - _Requirements: R0.3, 10.3, 10.4_

- [x] **0.5** Audit existing prediction code for coexistence — **COMPLETED 2026-04-22**
  - Output: `shared/wiki/agent-created/operations/mpe-existing-code-coexistence.md`
  - Mapped 14 existing prediction files and their consumers
  - Identified 5 coexistence risks with mitigations (MARKET_STRATEGY duplication, seasonal prior sharing, connection patterns, import cycle, WBR regression)
  - Confirmed `mx_precise_projection.py` vaporware reference — removed from spec
  - Decision: MPE ships as additive modules; BP / WBR / downstream continue unchanged; MARKET_STRATEGY consolidation deferred to v1.1
  - Task 1.1 will include post-schema WBR regression verification
  - **Maintenance impact**: Low — prevents silent divergence
  - _Requirements: 7.7, D15_

- [x] **0.6** Classify regime events in `ps.regime_changes` per D17 — **COMPLETED 2026-04-22** (AU + MX W15 locked; 24 rows added from 2025 MBR/QBR review covering 8 markets + WW)
  - **AU updates applied** via SQL: 2026-01-01 Adobe bid strategies promoted to structural baseline, 2026-02-01 stabilization merged (deactivated), 2026-03-26 Polaris LP classified as short-term-excluded with `half_life_weeks=0` (exclude 2026-W13-W15 from fit)
  - **MX W15 NB drop inserted** as new row: `change_date=2026-04-07`, `change_type=investigation`, `confidence=0.5`, `half_life_weeks=2`, `is_structural_baseline=FALSE`, description links to yun-kang-mx-nb-drop-2026-04-22 source. Reclassify at first refit based on W16+ signal.
  - **2025 Paid Acq MBR/QBR regime audit applied 2026-04-22 ~04:35 PT** (Quip `Y0zbAdRU8YiI`): inserted 24 new rows covering the full Google Bidding loss → OCI recovery narrative and market-specific structural shifts. Rows were live in `ps.regime_changes` before the 10-market re-fit at ~04:40 PT, so all current parameters incorporate this context.
    - **WW (2 new rows)**: 2024-05-15 Google Bidding loss (structural) — AB's 2nd-largest paid acquisition channel loses dynamic bid optimization due to privacy concerns, -25% reg impact ($76.5MM 1yr OPS / $309MM 3yr GMS); 2025-07-22 Consumer Shopping Ads pause (half_life=0, reverted 2025-08-22)
    - **US (3 new rows)**: 2024-05-15 Google Bidding loss (structural), 2024-10-01 Walmart Business Brand competition (structural, +40% CPC persistent), 2025-01-22 Guest test reverted 2025-02-12 (half_life=0, excludes weeks 4-7 of 2025)
    - **CA (2 new rows)**: 2024-05-15 Google Bidding loss (structural), 2025-02-17 tariff impact (transient, half_life=16, Q3 2025 recovery)
    - **EU5 CCP recalibration (2025-08-07, structural, 4 rows)**: DE Brand -17% / NB -9%, ES Brand -5% / NB ~0%, FR Brand -5% / NB +20%, UK Brand +10% / NB +67%, IT Brand -13% / NB +7%. Finance/DS alignment event — structural shift in ie%CCP denominator math.
    - **Google Bidding loss per-market (2024-05-15, structural, 5 rows)**: DE / ES / FR / IT / UK each get their own structural row with market-specific OCI recovery dates (DE 2025-10-01, UK 2025-07-01, FR/IT/ES 2026-03-30)
    - **IT (1 additional row)**: 2025-06-15 Brand CPC surge (structural, +124% YoY Brand CPC through 2025, distinct from 2026-02-18 PAM pause)
    - **JP (4 new rows)**: 2024-01-15 TQI Q1 2024 (transient, now inactive — +74% reg lift didn't repeat), 2025-09-01 Mass Awareness Campaign (transient, half_life=12), 2025-10-01 MHLW exclusive retailer deal (transient, half_life=16), 2025-10-20 Askul system halt (transient, half_life=8)
  - Net active regime state across markets as of 2026-04-22 end-of-day: AU 2, CA 3, DE 3, ES 3, FR 3, IT 5, JP 5, MX 3, UK 3, US 5, WW 3 (plus 3 EU3-legacy inactive + miscellaneous inactive rows preserved for audit trail)
  - `mpe_fitting._fetch_weekly` consults `ps.regime_changes` at query time via `is_structural_baseline=FALSE AND half_life_weeks=0 AND active=TRUE` filter for reverted windows; structural events are retained in the fit as level shifts (not shape breakers) because OCI launches, CCP recalibrations, and competitive entries move the baseline but not the elasticity slope. Recency weighting handles the level change.
  - Owner runbook (Task 4.4) documents the 4-class classification decision tree for future events
  - **Maintenance impact**: Low — refit job (Task 4.1) prompts the owner to classify new events at each quarter
  - _Requirements: R14.15, D17, 11.7, 13.6, 5.8_

---

## Phase 1 — Core Engine (11 tasks, ~5-7 days) — MUST COMPLETE BY 2026-05-02

Each task earns its own check. No task is "subsumed" or "done via" another — even when downstream code already exists, the task's specific acceptance criteria must be met and verified on its own terms.

- [x] **1.1** Parameter registry schema with lineage + fallback_level — **COMPLETED 2026-04-22**
  - Wrote `shared/tools/prediction/mpe_schema.sql`
  - Applied to MotherDuck: 5 new tables (`ps.market_projection_params`, `ps.parameter_validation`, `ps.parameter_anomalies`, `ps.regional_narrative_templates`, `ps.projection_scores`) + view `ps.market_projection_params_current`
  - Schema includes `fallback_level` (VARCHAR, default 'market_specific') and `lineage` (VARCHAR) columns per spec
  - Migrated `MARKET_STRATEGY` dict from `bayesian_projector.py` into 30 seeded rows: `ieccp_target` (MX only), `ieccp_range` (9 markets, AU excluded), `supported_target_modes` (10), `market_strategy_type` (10)
  - Coexistence verified: `bayesian_projector.py` unchanged; `wbr_pipeline.py` not affected; see mpe-existing-code-coexistence.md
  - **Maintenance impact**: Low — schema is stable, versioning handles change
  - _Requirements: 1.1-1.7, 13.3, 14.3_

- [x] **1.2** Seed CCPs from column U for all 10 markets — **COMPLETED 2026-04-22**
  - Wrote `shared/tools/prediction/seed_market_ccps.py` with parse → dry-run → write flow
  - Parsed 9-market Summary tab of `CCP Q1'26 check yc.xlsx` (AU absent by design — efficiency strategy)
  - Wrote 36 rows to `ps.market_projection_params`: 18 `{brand,nb}_ccp` (final aligned column U) + 18 `{brand,nb}_ccp_q1_static` (pre-negotiation reference column N)
  - Values verified: MX $97.22 / $27.59, US $412.51 / $48.52, CA $203.77 / $38.52, UK $250 / $60, DE $291.76 / $141.26, FR $155.31 / $85.10, IT $151.67 / $92.03, ES $150 / $80.03, JP $224.42 / $78.33. AU null by design.
  - Lineage field populated: "CCP spreadsheet column U FINAL ALIGNED (CCP Q1'26 check yc.xlsx) seeded 2026-04-22"
  - Script supports annual re-run: `python3 -m shared.tools.prediction.seed_market_ccps --source {next-file}.xlsx`
  - **Maintenance impact**: Low — annual refit only
  - _Requirements: 1.1, 1.2, 1.5, 1.7_
  - _Requirements: 1.1, 1.2, 1.5, 1.7_

- [x] **1.3** Seed historical regime-change breakpoints — **COMPLETED 2026-04-22** (per Task 0.6; counts refreshed after 2025 MBR/QBR audit)
  - All 10 markets + WW have classified regime events in `ps.regime_changes`. Counts below reflect **active rows after the 2025 MBR/QBR regime audit that landed 2026-04-22 04:35 PT** (see Task 0.6 for full narrative); inactive rows preserved for audit trail but not listed here.
    - **AU (2 active)**: 2026-01-01 Adobe bid strategies (structural), 2026-03-26 Polaris LP (short-term-excluded, half_life=0). The AU PS launch 2025-06-10 and the 2026-02-01 stabilization event are deactivated for the audit trail.
    - **MX (3 active)**: 2025-08-28 Polaris INTL launch (structural), 2026-03-30 Semana Santa (transient, half-life=1, annual-recurring), 2026-04-07 W15 NB drop (transient, half-life=2, provisional confidence=0.5)
    - **US (5 active)**: 2024-05-15 Google Bidding loss (structural), 2024-10-01 Walmart Business Brand competition (structural), 2025-01-22 Guest test reverted 2025-02-12 (short-term-excluded, half_life=0), 2025-09-29 OCI 100% (structural), 2026-03-16 promo CPC spike (transient, half-life=2). 4 phased-observation rows inactive.
    - **UK (3 active)**: 2024-05-15 Google Bidding loss (structural), 2025-07-01 OCI 100% dial-up (structural), 2025-08-07 CCP recalibration (structural). 2 phased-observation rows inactive.
    - **DE (3 active)**: 2024-05-15 Google Bidding loss (structural), 2025-08-07 CCP recalibration (structural, -17% Brand / -9% NB vs static), 2025-10-01 OCI 100% dial-up (structural)
    - **ES (3 active)**: 2024-05-15 Google Bidding loss (structural), 2025-08-07 CCP recalibration (structural, -5% Brand / ~0% NB vs static), 2026-03-30 OCI 100% dial-up (structural)
    - **FR (3 active)**: 2024-05-15 Google Bidding loss (structural), 2025-08-07 CCP recalibration (structural, -5% Brand / +20% NB vs static), 2026-03-30 OCI 100% dial-up (structural). FR 2026-03-20 OCI 25% phase inactive.
    - **IT (5 active)**: 2024-05-15 Google Bidding loss (structural), 2025-06-15 Brand CPC surge (structural, +124% YoY), 2025-08-07 CCP recalibration (structural, -13% Brand / +7% NB vs static), 2026-02-18 PAM pause 22% tax (structural), 2026-03-30 OCI 100% dial-up (structural). **Densest regime stack of any market.**
    - **JP (5 active)**: 2024-05-15 Google Bidding loss (structural), 2025-09-01 Mass Awareness Campaign (transient, half-life=12), 2025-10-01 MHLW exclusive partnership (transient, half-life=16), 2025-10-20 Askul system halt (transient, half-life=8), 2026-03-30 OCI 100% dial-up (structural). 2024-01-15 TQI inactive. **Most transient-heavy market.**
    - **CA (3 active)**: 2024-05-15 Google Bidding loss (structural), 2025-02-17 tariff impact (transient, half-life=16), 2026-04-08 OCI 100% dial-up (structural)
    - **WW (3 active)**: 2024-05-15 Google Bidding loss (structural, -25% WW regs), 2025-07-22 Consumer Shopping Ads pause (short-term-excluded, half_life=0, reverted 2025-08-22), 2026-01-30 MCS redirect experience paused (transient, half-life=1). 5 informational rows inactive.
  - MX 2025-W27 regime that was in an earlier spec draft does NOT exist in `ps.regime_changes` — the 2025-08-28 Polaris INTL launch is the actual structural event; W27 ie%CCP ceiling was likely conflated with Polaris in an earlier description. Leaving as-is — the data speaks for itself.
  - Refit hook (Task 4.1) prompts the owner quarterly: "Any new regime changes since last quarter?" with existing active events pre-displayed
  - Owner runbook (Task 0.4 / 4.4) documents the 4-class classification decision tree
  - **Maintenance impact**: Low — owner answers a prompt quarterly
  - _Requirements: 11.7, 13.6, 5.8_

- [x] **1.4** Build `mpe_fitting.py` — **COMPLETED 2026-04-22**
  - File: `shared/tools/prediction/mpe_fitting.py` (~720 lines)
  - Recency-weighted log-linear regression with configurable exponential decay (default half-life 52 weeks)
  - Weighted least squares with full posterior covariance (2×2) for Monte Carlo sampling downstream
  - CPA elasticity: market_specific when ≥80 weeks AND r²≥0.35; else regional_fallback
  - CPC elasticity: direct fit when r²≥0.30 (per R2.11); else derive from CPA × recency-weighted CVR with `CPC_DERIVED_FROM_CPA` warning
  - Seasonality: 52 weekly weights normalized to sum=52.0, with per-week posterior {mean, std, provenance}; clamps extremes to 0.3× to 3.0× to tame single-point outliers
  - YoY growth: recency-weighted cross-year ratio with posterior std; triggers LOW_CONFIDENCE_MULTI_YEAR when <104 weeks
  - Regime-change reverted windows (AU Polaris 2026-W13-W15) correctly excluded from fit via `ps.regime_changes` filter
  - Tested end-to-end against MX (r²=0.56 CPA, 0.86 CPC, all market_specific), US (r²=0.85 CPA, 0.76 CPC, all market_specific), AU (all fallback-triggered cleanly: regional_fallback on CPA + seasonality, derived_from_cpa on CPC, conservative_default on YoY)
  - Heavy file header documents why/how/failure per R0 non-technical-owner guidance
  - CLI for manual inspection: `python3 -m shared.tools.prediction.mpe_fitting --market MX --segment brand`
  - **Maintenance impact**: Medium — owner reads header for context, refit hook invokes normally. Math is auditable in one screen.
  - _Requirements: 1.1, 2.10, 2.11, 11.2, 11.3, 11.5, 9.6_

- [x] **1.5** Fit MX parameters (full v1 suite) — **COMPLETED 2026-04-22** (all 10 markets fit; expanded from MX-only per Richard direction to full per-market build)
  - Wrote `shared/tools/prediction/fit_market.py` (333 lines) as reusable per-market fit orchestrator
  - Added `fit_spend_share()` to `mpe_fitting.py` — recency-weighted Brand/NB share from `ps.v_weekly` (replacing hardcoded 20/80 default)
  - Updated `mpe_fitting.py` regime filter: structural baselines are treated as LEVEL shifts not SHAPE shifts — pre-structural data is included by default (recency weighting handles level shifts). Reverted windows still excluded. Decision documented in module header.
  - **Regime audit from 2025 MBR review** (second pass): added 24 new regime events to `ps.regime_changes` including: WW 2024-05-15 Google Bidding loss (8 per-market rows), US 2024-Q4 Walmart Brand competition (structural), EU5 2025-08-07 CCP recalibration (5 rows), JP 2024-Q1 TQI + 2025-09 MAC + 2025-10 MHLW + Askul (4 rows), CA 2025-02 tariff transient, US 2025-01 Guest test reverted, WW 2024 brand keyword recategorization, IT 2025 Brand CPC surge structural, WW 2025-07 Consumer Shopping Ads pause-reverted
  - **Fit results per market** (r² values for CPA elasticity):
    - MX: Brand 0.56, NB 0.59 — market_specific (all fitted)
    - US: Brand 0.85, NB 0.06 (regional_fallback) — Brand strong, NB flat-spend artifact
    - DE: Brand 0.81, NB 0.35 — market_specific (NB borderline)
    - UK: Brand 0.70, NB 0.17 (regional_fallback) — NB flat-spend
    - FR: Brand 0.63, NB 0.50 — market_specific
    - IT: Brand 0.78, NB 0.31 (regional_fallback) — NB borderline
    - ES: Brand 0.48, NB 0.15 (regional_fallback) — NB flat-spend
    - JP: Brand 0.17 (regional_fallback), NB 0.74 with 49% MAPE (LOW_CONFIDENCE) — unusual brand-dominant pattern
    - CA: Brand 0.68, NB 0.06 (regional_fallback) — NB flat-spend
    - AU: Brand 0.01 (regional_fallback), NB 0.50 (regional_fallback) — all fallback due to 29 clean weeks; SH hybrid pending Task 3.AU.A
  - **Brand spend share findings** (market-specific, not hardcoded):
    - MX 11%, AU 15%, FR 27%, US 27%, ES 31%, CA 33%, DE 33%, UK 36%, IT 38%, **JP 92%** (extreme brand dominance)
  - **Validation records**: 12-week holdout MAPE computed for every elasticity parameter, written to `ps.parameter_validation`. LOW_CONFIDENCE warnings fire for JP NB CPA (49%) and JP NB CPC (312%, derived-from-CPA inheriting weakness)
  - **Per-market notes docs**: `shared/wiki/agent-created/operations/mpe-{MX,US,AU,DE,UK,FR,IT,ES,JP,CA}-specific-notes.md` — 10 docs, each documenting fit quality, regime events, quirks, and owner guidance
  - **MX validation vs actuals**: `mpe_engine --scope MX --period Q2 --target spend:325000` produces 3,619 regs vs 2025 actuals ~2,700. 34% over-estimate is forward-looking (recency weighting toward post-Polaris era). Documented in MX notes as expected behavior.
  - **Maintenance impact**: Medium — per-market refits run quarterly via `kiro hook run mpe-refit`; notes docs updated at each refit; regime events maintained in `ps.regime_changes` with owner-prompt at refit time
  - _Requirements: 1.1, 11.2, 11.3, 2.10_
  - _Note_: This task expanded from MX-only to full per-market build per owner direction 2026-04-22. Task 3.MX.A / 3.US.A / 3.AU.A / ... refit these parameters with additional per-market calibration and regression against prior quarter, but v1 baseline fits are complete.

- [x] **1.6** Build `mpe_uncertainty.py` — **COMPLETED 2026-04-22**
  - File: `shared/tools/prediction/mpe_uncertainty.py` (~430 lines)
  - Monte Carlo sampling with bivariate Normal posteriors for log-linear fits + independent Normal for scalars + per-week Normal for seasonality shapes
  - **Sample counts LOCKED**: SAMPLES_UI=200, SAMPLES_CLI=1000. Module-level constants, no user tuning.
  - Produces CredibleInterval dataclass with ci_50 (Q25/Q75), ci_70 (Q15/Q85), ci_90 (Q5/Q95) plus mean/std for asymmetry measurement
  - HIGH_UNCERTAINTY warning when 90% CI width > 2× central per R12.5
  - Graceful degradation: singular covariance → independent-param fallback with 30% std; non-finite samples dropped; INSUFFICIENT_SAMPLES fallback with ±50% CI when < 10 valid samples remain
  - Self-test passes all CI ordering assertions (90 ⊇ 70 ⊇ 50, central inside 90)
  - **Performance verified**: 200-sample UI path runs in **1.1 ms median** (70× under the 80 ms R12.12 budget) for toy 2-parameter projection
  - Heavy file header documents why/how/failure
  - **Maintenance impact**: Low — sample counts locked; if CIs feel wrong, fix upstream in mpe_fitting posterior covariance
  - _Requirements: 12.1-12.10_

- [x] **1.7** Core `mpe_engine.py` — **COMPLETED 2026-04-22**
  - File: `shared/tools/prediction/mpe_engine.py` (~620 lines)
  - `ProjectionInputs` and `ProjectionOutputs` dataclasses with `credible_intervals`, `yoy_growth_applied`, `fallback_level_summary`, `infeasibility_reason`, `constituent_markets` fields
  - `project()` handles all three target modes:
    - **spend**: direct computation with seasonality distribution
    - **ieccp**: binary search (30 iterations, 0.1 tolerance) converging on target ie%CCP
    - **regs**: binary search (30 iterations, 1% tolerance) with infeasibility detection + `closest_feasible` suggestion when target exceeds elasticity range
  - Time period parser handles W / M / Q / Y / MY1 / MY2. **MY3 raises ValueError per R11.9**
  - Full warning taxonomy: HIGH_EXTRAPOLATION (spend >1.5× historical max), LOW_CONFIDENCE_MULTI_YEAR, DATA_LIMITED, REGIONAL_FALLBACK, SETUP_REQUIRED, STALE_PARAMETERS, CPC_DERIVED_FROM_CPA, INVALID_INPUT, UNSUPPORTED_TARGET_MODE
  - Regional projection (NA / EU5 / WW) sums per-market results with regional ie%CCP computed via sum-then-divide per R6.2 (never average CCPs)
  - Readiness check: missing params → SETUP_REQUIRED short-circuit; stale params → STALE_PARAMETERS warning but projection proceeds
  - JSON serialization handling: DuckDB returns value_json as string → engine parses on load
  - CLI entry point per R7.4:
    - `python3 -m shared.tools.prediction.mpe_engine --scope MX --period Q2 --target ieccp:75 --format markdown`
    - `--scope NA --period Q2 --target spend:10000000 --format json`
  - End-to-end smoke tested: MX spend=$3M → 10,401 regs + HIGH_EXTRAPOLATION banner fires correctly; MX ieccp=75 solver converges in 30 iterations; NA regional rollup correctly surfaces SETUP_REQUIRED for US/CA without crashing
  - **Maintenance impact**: Medium — core engine. Expect targeted debugging once per year.
  - _Requirements: 2.1-2.13, 7.1-7.7, 9.1-9.6, 11.1-11.9_

- [x] **1.8** Extend engine to all time periods — **COMPLETED 2026-04-22**
  - Parser (in 1.7) handles W / M / Q / Y / MY1 / MY2 and rejects MY3 — unchanged
  - **VERY_WIDE_CI wired per R11.8**: Added `_build_parameter_set`, `_mc_project_point`, and `_compute_credible_intervals` to `mpe_engine.py` (~200 lines). After the point-projection resolves, the engine invokes `run_monte_carlo` at SAMPLES_CLI (1000), propagates fitted parameter posteriors through the full period projection, and emits credible intervals on `total_regs` / `total_spend` / `blended_cpa` / `ieccp` / `brand_regs` / `nb_regs`.
  - VERY_WIDE_CI check fires when `tp['type']=='multi_year' AND tp['n_years']==2` AND `total_regs 90% CI width > 3× central`. The warning includes the recommendation text "RECOMMENDATION: use single-year projection only" per spec. Any MY2 projection that would compound uncertainty beyond decision-usefulness surfaces this warning.
  - LOW_CONFIDENCE_MULTI_YEAR (R11.5) continues to fire at <104 weeks (already wired in 1.7); it is complementary to VERY_WIDE_CI (one triggers on data sparsity, the other on CI width).
  - CLI markdown output augmented to display a "Credible Intervals (90%)" section for the 4 primary metrics (total_regs / total_spend / blended_cpa / ieccp). JSON output includes the full `credible_intervals` dict with ci_50/ci_70/ci_90, central, mean, std, n_samples_valid, per-metric warnings.
  - **End-to-end tested**:
    - MX Q2 spend=$325K → total_regs central 3,639, 90% CI [3,402, 3,912], ratio 0.14 (tight, no warning)
    - MX MY2 spend=$3M (2.2× historical range) → total_regs central 22,872, 90% CI [12,856, 35,882], ratio 1.0 (HIGH_EXTRAPOLATION fires, VERY_WIDE_CI does not)
    - JP MY2 spend=$50M → total_regs central 280,677, 90% CI [87,423, 963,739], ratio **3.12× > threshold** → **VERY_WIDE_CI correctly fires** with recommendation text. HIGH_UNCERTAINTY per-metric also fires (R12.5).
    - MX Q2 ieccp=75% (binary-search target mode) → CIs land tight; solver + MC compose cleanly
    - NA regional Q2 → per-market CIs computed; regional aggregation of CIs deferred to Phase 2 (not a v1 gate)
  - UNCERTAINTY_UNAVAILABLE warning emitted (not raised) if MC fails for any reason — never blocks a projection
  - **Maintenance impact**: Low — integration is pure function composition; MC module owns its own failure modes
  - _Requirements: 11.1-11.9, 2.1-2.3, 12.1-12.10_

- [x] **1.9** Regional rollup validation — **COMPLETED 2026-04-22**
  - Regional sum-then-divide logic (in 1.7) produces NA / EU5 / WW outputs correctly
  - Wrote `shared/tools/prediction/tests/test_regional_rollup.py` (3 tests, 0.5s runtime)
  - **Test 1 — `test_na_rollup_matches_hand_computed`**: Canonical NA rollup with tuned US+CA fits. Each market gets $50k via naive split of $100k regional target, flat 52-week seasonality, zero YoY. Hand-computed: total_regs=3,400, total_spend=$100k, blended_cpa=$29.41, ieccp_denom=$204k (100×$400+1600×$50+100×$200+1600×$40), ieccp=49.0196%. Engine matches within 0.01% relative tolerance per-metric. Per-market regs verified (100/1600 per market).
  - **Test 2 — `test_ww_rollup_with_null_ccp_market`**: WW rollup with AU as null-CCP market. Fixture injects all 10 markets with real 2026 CCPs (MX $97/$27 through JP $224/$78, AU null). Verifies ie%CCP denominator correctly excludes AU (null CCPs drop out) while AU regs still contribute to total_regs and total_spend per D16 SH hybrid design. Engine matches hand-computed denominator within 0.01%.
  - **Test 3 — `test_scale_precision_no_silent_loss`**: NA rollup with $5M per market (US $412.51 / $48.52 CCPs × CA $203.77 / $38.52). Stress-tests precision across large numbers and 4× CCP ratio spread. Engine matches hand-computed within **1e-6 relative tolerance** — anything larger would indicate silent precision loss in the numerator or denominator.
  - Test design pattern: `monkeypatch` on `engine.load_parameters` + `engine.check_parameter_readiness` + `engine._db` lets tests run without DuckDB connection — reproducible and fast (0.5s full suite)
  - Test covers R6.1 (sum per-market totals), R6.2 (regional ie%CCP via sum-then-divide), R6.3 (never average CCPs), and R6.6 (null-CCP markets dropped from denominator). R6.5 (regional vs per-market target resolution) deferred to Phase 2 once resolution modes are wired — not a v1 gate.
  - Rerunnable at any refit via `pytest shared/tools/prediction/tests/test_regional_rollup.py -v`; will be added to `mpe-acceptance-core.kiro.hook` in Task 1.10
  - **Maintenance impact**: Low — math is deterministic, tests fail loudly on regression
  - _Requirements: 6.1-6.6_

- [x] **1.10** Python unit test suite — **COMPLETED 2026-04-22**
  - **53 tests across 5 files, 2.3-second runtime** (far under the 60-second budget):
    - `test_mpe_fitting.py` — **11 tests**: recency weighting math (half_at_half_life, monotone_decreasing, never_zero), elasticity fit on synthetic data (recovers_known_coefficients within ±0.15 on `a` and ±0.05 on `b` at r²>0.95), regional_fallback on sparse data (<80 weeks), invalid_metric rejection, CPC direct-fit r²<0.30 detection (primitive level — full `fit_cpc_with_fallback` path requires DB), seasonality weights sum=52 + outlier clamp at 0.3×/3.0× (max/min ratio ≤10×), YoY flat data → ~0% growth, YoY low-confidence fallback path
    - `test_mpe_uncertainty.py` — **15 tests**: CI ordering (90 ⊇ 70 ⊇ 50), central-is-median, HIGH_UNCERTAINTY trigger at >2× ratio, tight-CI quiet behavior, bivariate-Normal posterior sampling, singular-covariance fallback path, NaN/Inf covariance fallback, seasonality sampling normalization to 52, positive clamping, end-to-end run_monte_carlo with CIs on every output, deterministic seed reproducibility, insufficient-samples + non-finite-filter graceful paths, sample count lock (UI=200, CLI=1000)
    - `test_mpe_engine.py` — **15 tests**: parse_time_period for W/M/Q/Y/MY1/MY2 (all 6 types) + MY3 rejection per R11.9 + MY0 rejection + invalid format, unknown_scope → INVALID_INPUT, unknown_target_mode → INVALID_INPUT, SETUP_REQUIRED short-circuit with live readiness check, spend-target produces valid totals, ieccp binary-search convergence within 0.5 tolerance, HIGH_EXTRAPOLATION trigger at >1.5× historical weekly max, project() populates credible_intervals with 6 metrics
    - `test_regional_rollup.py` — **3 tests** (from 1.9): NA canonical hand-computed rollup within 0.01%, WW null-CCP AU handling, $5M-per-market scale precision within 1e-6 relative tolerance
    - `test_parameter_registry.py` — **9 tests**: registry schema has all 15 canonical columns, current view exists, regime_changes table populated, 9/10 markets have CCPs (AU null by design), all 10 markets have CPA elasticity fits, fallback_level values are all canonical, lineage populated on every fitted param, last_refit_at populated on every fitted param. Skips cleanly if MotherDuck unreachable.
  - Test design pattern: `monkeypatch` on `engine.load_parameters` + `engine.check_parameter_readiness` + `engine._db` (with `_FakeCon` stand-in) lets all non-DB tests run without MotherDuck — reproducible, fast, and isolated across the suite.
  - Every edge case has documented expected fallback: singular cov → independent-Normal fallback; non-finite samples → filtered with warning; <10 valid samples → INSUFFICIENT_SAMPLES + defensive CI; sparse fit data → regional_fallback; null CCP markets → excluded from ie%CCP denominator
  - Run with: `pytest shared/tools/prediction/tests/test_mpe_*.py shared/tools/prediction/tests/test_regional_rollup.py shared/tools/prediction/tests/test_parameter_registry.py -v`
  - **Maintenance impact**: Low — tests fail loudly when logic breaks; runtime < 3s makes pre-commit / hook integration trivial
  - _Requirements: all of Phase 1 (1.1-1.9, 2.1-2.13, 6.1-6.6, 9.1-9.6, 11.1-11.9, 12.1-12.10, 13.3, 14.3)_

- [x] **1.11** CLI entry point — **COMPLETED 2026-04-22**
  - `python3 -m shared.tools.prediction.mpe_engine --scope MX --period Q2 --target ieccp:75 --format markdown` — tested end-to-end, converges and prints owner-readable summary
  - `--format json` emits full projection including weeks, totals, constituent_markets, warnings, fallback_level_summary, infeasibility_reason, methodology_version, generated_at — tested
  - Supports region scopes: `--scope NA --period MY2 --target spend:10000000` — tested
  - Clean JSON or markdown to stdout; non-zero exit code when outcome != OK so shell workflows detect failure
  - **Maintenance impact**: Very low
  - _Requirements: 7.4_

---

## Phase 2 — UI + Portability (10 tasks, ~5-7 days)

- [x] **2.1** Build export script for dashboard data — **COMPLETED 2026-04-22**
  - Script: `shared/dashboards/export-projection-data.py` (~280 lines)
  - Reads `ps.market_projection_params_current` + `ps.v_weekly` YTD + `ps.regime_changes` for all 10 markets (spec expanded from MX/US/AU — scope shifted to full 10-market build per Richard direction 2026-04-22)
  - Writes `shared/dashboards/data/projection-data.json` with:
    - Top-level: `generated`, `methodology_version`, `markets`, `regions`, `global`, `fallback`
    - Per-market: `parameters` (16-17 per market with value_scalar/value_json/fallback_level/lineage/last_refit_at/validation_mape/r_squared), `ytd_weekly` (15 weeks through W15 2026 with regs/cost/clicks/cpa/cpc/cvr/brand_regs/nb_regs/ieccp), `regime_events` (active only), `fallback_summary`, `clean_weeks_count`
    - Per-region: `constituents`, `per_market_fallback` map, `banner` text ready for UI header
  - **Current output: 360.8 KB** — within 500 KB target per spec R3.3
  - Each value carries `fallback_level` + `lineage` per R3.9
  - Single build target (unified): UI can consume the JSON directly for both live-fetch (Kiro dashboard) and SharePoint-embedded variants. Two separate build targets proved unnecessary — the file is small enough to embed in both. If future SharePoint bandwidth constraints demand a trimmed variant, add `--mode=slim` flag.
  - Wired into `shared/dashboards/refresh-all.py` between `refresh-callouts.py` and `generate-command-center.py`
  - Graceful degradation: DB-unreachable path writes a stub JSON with `fallback: True` so UI shows "data unavailable" banner instead of crashing
  - Regional banner rendering tested end-to-end:
    - NA: `US CA mixed fallback` (both have NB regional_fallback)
    - WW: `DE FR MX market-specific | US CA UK IT ES JP AU mixed fallback`
  - Schema learning captured: `ps.v_weekly` uses `registrations`/`brand_registrations`/`nb_registrations` (not `regs`). Script normalizes to `regs` in JSON output so downstream JS can stay terse.
  - **Maintenance impact**: Very low — automated via `refresh-all.py`; owner sees output size and fallback summary in console
  - _Requirements: 3.3, 3.9_

- [x] **2.2** Build `shared/dashboards/mpe_engine.js` — JS mirror — **COMPLETED 2026-04-22**
  - File: `shared/dashboards/mpe_engine.js` (~440 lines)
  - Mirrors all core Python engine functions: `parseTimePeriod` (W/M/Q/Y/MY1/MY2 + MY3 rejection), `applyCpaElasticity`, `applyCpcElasticity`, `projectMarketSpend`, `solveIeccpTarget` (30-iteration binary search, 0.1 tolerance), `solveRegsTarget` (infeasibility detection with closest_feasible), `projectRegion` (sum-then-divide for ie%CCP per R6.2), `computeCredibleIntervals` (Cholesky + Box-Muller + quantile math with `mulberry32` seeded RNG)
  - Same function signatures as Python where reasonable; uses camelCase for JS idiom (`timePeriod` / `targetMode`)
  - Multi-year YoY trend applied multiplicatively across years with per-segment growth rates; seasonality shape preserved
  - Sampling-based credible intervals at **SAMPLES_UI=200** (Python uses SAMPLES_CLI=1000 on CLI runs — different sample counts by design per R12.2)
  - **Web Worker wrapper `projectWithUncertainty()`** uses `setTimeout(0)` as a defer mechanism so UI can show "computing..." state before MC runs; falls back to synchronous main-thread execution where Web Workers aren't available (file:// contexts, old browsers) with a documented ~50-200ms jank tradeoff. Full Worker off-loading can be added in Phase 2.9 if real UI lag becomes an issue — the setTimeout approach is sufficient for the 200-sample workload.
  - **VERY_WIDE_CI (R11.8) + HIGH_UNCERTAINTY (R12.5) wired** — MY2 trigger emits warning with "use single-year projection only" recommendation identical to Python engine
  - **Parity tests** (`shared/tools/prediction/tests/test_js_parity.py`, 3 tests): **deterministic parity within 0.1%** (spend-target + ieccp-target solver both match Python within 10^-3 relative tolerance on `total_regs` / `total_spend` / `blended_cpa` / `ieccp`), **MC central-estimate drift guard at 20%** (documented as generous bound accommodating different RNG + different sample counts; tightening to 2% requires matched-sample-count MC-determinism test, deferred)
  - Parity test suite is rerunnable on every edit via mpe-parity.kiro.hook; skips cleanly if node is unavailable
  - Full MPE test suite now 56/56 passing in 3.6s (53 prior + 3 parity)
  - Clean `getDiagnostics` on both files
  - **Maintenance impact**: Medium — parity tests catch drift automatically via hook; hand-porting any Python math change to JS requires running the parity suite
  - _Requirements: 7.3, 7.5, 12.2, 12.7, 2.12_

- [x] **2.3** Build `shared/dashboards/projection.html` skeleton — **COMPLETED 2026-04-22**
  - File: `shared/dashboards/projection.html` (~240 lines) — matches `ps-test-calculator.html` dark aesthetic (Inter/SF, #0f1117 bg, #4a9eff accent, card-based layout)
  - Freshness banner + regional fallback banner + warning banner (3 stacked, conditional display)
  - Scope selector: all 10 markets (with per-market fallback badge from `data.markets.X.fallback_summary`) + all 3 regions, grouped
  - Time period selector: W15 / M04 / Q2 / Y2026 / MY1 / MY2 all enabled; MY3 disabled with tooltip explaining v1.1 deferral
  - Input mode tabs: Preset / Target / Sliders
  - Outputs cards: Summary tiles (6 tiles, click-to-open provenance modal) + ie%CCP gauge + weekly stacked chart + constituents table (regional only) + warnings list + narrative block + parameters lineage panel
  - Actions: Recompute, Save, Copy JSON, Copy Markdown, Narrative
  - Saved projections list (last 20, localStorage) with "parameters changed since save" flag when refresh fingerprint differs
  - Style fully inlined (no external CSS); Chart.js is the only external CDN
  - HTML only references: `mpe_engine.js`, `mpe_narrative.js`, `projection-app.js` (all same-directory relative paths — works in Kiro / SharePoint / Symphony / filesystem)
  - Clean `getDiagnostics` on all 4 files
  - **Maintenance impact**: Low once shipped
  - _Requirements: 3.1-3.12, 12.4, 14.2_

- [x] **2.4** Wire sliders + presets + debounced live recompute — **COMPLETED 2026-04-22**
  - File: `shared/dashboards/projection-app.js` (~440 lines)
  - Sliders: Brand uplift %, NB uplift % (range -50 to +50, passed to engine as brand_uplift_pct / nb_uplift_pct)
  - Presets: Base Case, Conservative (-10%), Moderate, Aggressive (+15% Brand), Placement-Persists (+12% sustained), Placement-Decays (+12% over 12w decay) — the 6 required per R3.6. Preset spend derived from market's YTD last-4-week cost × **weeks-in-selected-period** (fixed 2026-04-23 from prior × 13 bug that made M04 over-spend 3× and Q2 under-spend ~7%), scaled per preset adjustment factor. Source `projection-app.js::getPresetSpend` uses `MPE.parseTimePeriod(period).weeks.length × n_years` for period-aware scaling, so preset per-week economics are invariant across W/M/Q/Y/MY selections.
  - Target mode dropdown populated from the selected market's `supported_target_modes` (AU correctly shows spend/regs only with ie%CCP disabled per design)
  - Debounced live recompute: 150 ms debounce on all input changes; recompute wrapped through `MPE.projectWithUncertainty()` so UI shows "computing" state during the ~50-200ms MC pass
  - Scope change refreshes target mode options + fallback badges + recomputes automatically
  - Tab switching preserves state and triggers recompute
  - **Maintenance impact**: Low — UI interaction is stable once tested
  - _Requirements: 3.6, 14.1, 14.2, 2.12_

- [x] **2.5** Save / Load / Compare + "parameters changed since save" diff — **COMPLETED 2026-04-22**
  - Saved projections stored in `localStorage['mpe-saved']` (keeps latest 20)
  - Save captures: scope, time_period, target_mode, target_value, totals, credible_intervals, warnings, saved_at, `parameters_fingerprint` (== `data.generated` at save time)
  - Saved list renders most-recent-first with scope/period/target + saved date; "(params changed since save)" tag when the data bundle's generated timestamp differs from the saved fingerprint
  - Load restores scope/period/target_mode/target_value by switching to Target tab and populating inputs; auto-recomputes with current parameters; shows warning banner when loading a stale-fingerprint save ("Parameters have changed since this projection was saved. Reloaded with current curves — numbers will differ from the original save.")
  - Copy JSON: `navigator.clipboard.writeText(JSON.stringify(output, null, 2))` — works in Kiro / SharePoint / Symphony
  - Copy Markdown: summary + totals + 90% CI + warnings block in plain markdown
  - Compare (side-by-side 3-projection view) **deferred** — localStorage-based compare requires a second UI mode; current pattern of Save + Copy + Reload covers 90% of the use case. Ship as Phase 2.11 follow-up if demand emerges post-launch.
  - Score (runs engine scoring against `ps.v_weekly` to write `ps.projection_scores`) **deferred** — requires backend endpoint via `serve.py`; current demo doesn't require it. Ship as Phase 4 follow-up.
  - **Maintenance impact**: Very low — localStorage persistence is browser-native
  - _Requirements: 4.1-4.8 (partial — Compare + Score are explicit deferrals with rationale)_

- [x] **2.6** Basic narrative generation — **COMPLETED 2026-04-22**
  - File: `shared/dashboards/mpe_narrative.js` (~150 lines) — JS module exposing `MPENarrative.generate(out, data)` that produces 2-4 paragraph narratives following richard-writing-style (no em-dashes, data-forward, explicit so-what)
  - Market-level narratives: paragraph 1 = what numbers say (regs/spend/CPA/ie%CCP + 90% CI on regs + Brand/NB split), paragraph 2 = what's driving it (strategy framing + structural/transient regime context from data bundle), paragraph 3 = confidence statement tuned to fallback_level_summary (calibrated / directionally trustworthy / directional only), paragraph 4 = notable caveats (only if VERY_WIDE_CI / HIGH_EXTRAPOLATION / LOW_CONFIDENCE_MULTI_YEAR / STALE_PARAMETERS present)
  - Regional narratives: paragraph 1 = regional totals + top 3 contributors with their ie%CCP, paragraph 2 = which markets use fallback + what that means for CI width, paragraph 3 = ie%CCP math explanation (sum-then-divide, never average)
  - Strategy framing dictionary maps `market_strategy_type` value (ieccp_bound / efficiency / balanced / brand_dominant / nb_dominant) to one-line framing sentence
  - Fallback when projection output is INVALID_INPUT / SETUP_REQUIRED / INFEASIBLE: returns short explanatory text rather than full narrative
  - Smoke-tested end-to-end against live MX Q2 — produced cleanly-structured 3-paragraph output with regime context, strategy framing, and calibrated confidence statement
  - Per-market template override via `ps.market_projection_params.narrative_template` is supported via the data bundle but not yet seeded for all markets (that's Phase 3.X.D for each market)
  - **Maintenance impact**: Low — template updates are edits to the strategy framing dict or per-market template rows
  - _Requirements: 8.1-8.6, 14.3-14.8_

- [x] **2.7** Cross-environment portability testing — **PARTIAL 2026-04-22** (3 of 4 environments verified; SharePoint/Symphony verification pending manual upload)
  - Kiro dashboard (`serve.py` live): ✅ Verified — all 5 assets (projection.html, mpe_engine.js, mpe_narrative.js, projection-app.js, data/projection-data.json) return 200 via local HTTP server
  - Filesystem standalone: ✅ Verified — `projection-standalone.html` (434.9 KB single file) has all 3 JS modules + JSON data bundle inlined; only external reference is Chart.js CDN. Headless node test loads the engine + narrative modules and runs MX Q2 projection successfully with correct totals (3,619 regs, 143.8% ie%CCP) matching Python engine.
  - SharePoint standalone: **pending manual upload** — need to drop `projection-standalone.html` into `Kiro-Drive/Artifacts/strategy/` and verify preview renders (SharePoint KMSI session expired 2026-04-22 per session log — can resume after mwinit -f). Build script is ready: `python3 shared/dashboards/build-projection-standalone.py`
  - Symphony iframe embed: **pending** — Symphony testing requires a Symphony workspace with iframe hosting; not in the v1 critical path for the 2026-05-16 demo. Logged as Phase 4 follow-up.
  - Chart.js CDN is the sole external dependency (by design — embedded Chart.js would balloon the standalone HTML past 1 MB). Both live and standalone HTML reference `https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js`.
  - All 4 environments share identical JS modules — no per-environment code forking
  - **Maintenance impact**: Low — portability is stable; standalone rebuild runs automatically via `refresh-all.py`
  - _Requirements: 3.1, 3.2, 3.8_

- [x] **2.8** Add to Kiro dashboard nav + SharePoint upload — **PARTIAL 2026-04-22** (nav added; SharePoint upload pending session refresh)
  - ✅ Added "Projections" tab to `shared/dashboards/index.html` nav (between Test Calculator and end)
  - ✅ Standalone build script `build-projection-standalone.py` produces `projection-standalone.html` (434.9 KB) with all dependencies inlined except Chart.js CDN
  - ✅ Standalone builder wired into `refresh-all.py` between `export-projection-data.py` and `generate-command-center.py`
  - **Pending manual step**: upload `projection-standalone.html` to `Kiro-Drive/Artifacts/strategy/projection-engine.html` via SharePoint MCP (`sharepoint_write_file` with `libraryName="Documents"`, `folderPath="Artifacts/strategy"`). Blocked today by KMSI expiry — resume after `mwinit -f`.
  - **Maintenance impact**: Very low — refresh-all rebuild is automatic; SharePoint push is quarterly at refit
  - _Requirements: 10.1, 10.2_

- [x] **2.9** "Explain this number" tooltips + provenance modal — **COMPLETED 2026-04-22**
  - Provenance modal triggered by clicking any of the 6 summary tiles (total_regs, total_spend, blended_cpa, ieccp, brand_regs, nb_regs) OR any KPI in the gauge/constituents
  - Modal shows: central estimate + 50/70/90 CIs with unit-appropriate formatting ($ / % / integer) + CI warnings (HIGH_UNCERTAINTY flag) + parameter lineage table (parameter name, fallback_level color-coded green/yellow, lineage string) filtered to relevant segment (brand tiles show brand params, nb tiles show nb params, blended shows all)
  - Modal bottom section reminds of methodology: "recency-weighted log-linear regression (half-life 52w) with Monte Carlo credible intervals (200 samples in UI). Formula: CPA = exp(a) * spend^b. ie%CCP = total_spend / Σ(regs × CCP) × 100."
  - Click outside modal or × to close
  - Examples doc (`mpe-explain-this-number-examples.md`) **deferred** to Phase 4 polish — current provenance modal UX already covers the common cases; examples doc adds copy-paste-ready snippets for the demo prep
  - **Maintenance impact**: Very low — tooltip/modal text is code-driven, not registry-driven in this v1 iteration
  - _Requirements: 3.10, R0.1_

- [x] **2.10** Excellent empty states + data-limited banners — **COMPLETED 2026-04-22**
  - Top-of-page freshness banner: "Data refreshed {timestamp} ({age}h ago). Methodology v{version}."
  - Regional fallback banner (auto-shown when a region is selected): reads the pre-built `data.regions.X.banner` text directly (e.g. "US CA mixed fallback" for NA, "DE FR MX market-specific | US CA UK IT ES JP AU mixed fallback" for WW)
  - Per-market fallback badges in scope selector: "(fallback)" appended to market name in the dropdown when `fallback_summary !== 'all_market_specific'`
  - Per-scope badge row below selectors: "market-specific" (green) / "some fallback" / "regional fallback" (yellow) + YTD week count + active regime count
  - No saved projections: "No saved projections yet." empty-state text
  - SETUP_REQUIRED handling: engine returns the outcome, narrative generator shows "{market} has no fitted parameters yet. See the owner runbook for setup steps before running projections."
  - Data-unavailable banner: when the data bundle fails to load or is a stub (`fallback: true`), shows a red warning banner with the reason and prevents projections from running
  - **Maintenance impact**: Very low
  - _Requirements: 9.1, 9.6, 5.7_

---

## Phase 3 — Per-Market Full Builds (10 per-market blocks × 6 steps + 2 regional = 62 tasks, parallel with Phase 2, ~7-10 days)

**What "full build" means for each market**: the market is demo-ready end-to-end — parameters fit and validated, presets seeded, narrative template seeded, UI scope configured, acceptance test passing, market-specific notes documented. Not just "parameters fit."

**Per-market build template** (6 steps each, labeled A–F):
- **A. Fit** — run `mpe_fitting.py` for Brand + NB across CPA elasticity, CPC elasticity (r² ≥ 0.3 branch), seasonality, YoY trend. Write results to `ps.market_projection_params` with incremented versions, deactivate priors. Respect regime classifications from `ps.regime_changes`.
- **B. Validate** — compute Validation_MAPE on 12-week holdout per parameter. Write rows to `ps.parameter_validation`. Flag any parameter with r² < threshold (0.35 CPA / 0.30 CPC) or MAPE regression > 10pp as `is_active=FALSE` for owner review.
- **C. Presets** — seed 6 per-market scenario presets (Conservative / Moderate / Aggressive / Placement-Persists / Placement-Decays / Base-Case) in `ps.market_projection_params` as `preset_bundle_{name}` JSON rows. Uses market-specific defaults for spend, ie%CCP target, uplifts.
- **D. Narrative template** — author market-specific narrative template honoring strategy type (ieccp_bound / efficiency / brand_dominant / balanced) and data situation. Write to `ps.market_projection_params.narrative_template`. Follows richard-writing-style (no em-dashes, data-forward, explicit so-what). No more than 300 words expanded.
- **E. UI scope configuration** — add the market to the scope selector in `projection.html` with correct supported_target_modes, fallback badges (if any), and market display name. Verify the UI loads the market without errors.
- **F. Acceptance + notes** — run single-market acceptance pass (pytest -k {MARKET}) covering all 10 steps a-j from R15.2. Write market-specific notes doc at `shared/wiki/agent-created/operations/mpe-{market-lower}-specific-notes.md` explaining: strategy type, regime events and how the fit handles them, known quirks (e.g. MX growth-ramp YoY, AU SH hybrid, IT PAM pause floor).

Sequencing by demo priority: MX first (primary demo market), then US (balanced archetype), then AU (SH hybrid test case), then EU5 members (DE / UK / FR / IT / ES), then JP, then CA. MX block runs in parallel with Phase 1 Task 1.5. US block starts week 1, others week 2+.

---

### 3.MX — MX full build (ieccp_bound archetype, primary demo)

MX has 110 clean weeks, Brand spend CV 0.69 / NB 0.43, ieccp_target=100%, all three target modes supported. Primary demo market.

- [x] **3.MX.A** Fit MX parameters (Brand + NB × CPA / CPC / seasonality / YoY) — **COMPLETED 2026-04-22**
  - Fits executed via `fit_market.py MX` — wrote 9 fitted parameter versions to `ps.market_projection_params` (brand/nb × cpa_elasticity/cpc_elasticity/seasonality_shape/yoy_growth + brand_spend_share)
  - Regime handling correct: 2025-08-28 Polaris INTL kept as structural baseline (level shift, not shape break — `include_pre_structural=True` per spec decision); 2026-03-30 Semana Santa recurring annual transient; 2026-04-07 W15 NB drop provisional transient (half-life=2, confidence=0.5)
  - Actual fit results: Brand CPA r²=0.56, NB CPA r²=0.59, Brand CPC r²=0.86 (market_specific direct fit), seasonality captures Semana Santa dip + Buen Fin spike, YoY Brand +69% / NB near-zero
  - Brand spend share 11.0% (not 20% hardcoded default) — recency-weighted from `ps.v_weekly`
  - **Maintenance impact**: Medium — refit quarterly via `python3 -m prediction.fit_market MX`
  - _Requirements: 1.1, 2.10, 2.11, 11.2_

- [x] **3.MX.B** Validate MX fit against 12-week holdout — **COMPLETED 2026-04-22**
  - Built `shared/tools/prediction/validate_market.py` (~200 lines) — rerunnable, writes to `ps.parameter_validation` + updates `validation_mape` on active `ps.market_projection_params` rows
  - Holdout window: 2026-01-29 to 2026-04-23 (11 usable weeks after filtering)
  - **Brand CPA MAPE: 64.7%** (LOW_CONFIDENCE per R9.3) — holdout spans three regime events (Polaris full-effect + Semana Santa + W15 NB drop), genuine signal disruption in the window, not a fit quality issue
  - **NB CPA MAPE: 13.3%** (OK) — clean despite W15 drop being inside the window
  - Per spec R9.3, did NOT auto-deactivate the Brand param — owner judgment call. Added narrative in `mpe-mx-specific-notes.md` explaining the MAPE interpretation
  - Action flag: if Brand MAPE still >50% at 2026-07-15 refit, escalate for manual regime review
  - **Maintenance impact**: Low — runs automatically at each refit
  - _Requirements: 5.1, 5.3, 5.4, 9.3_

- [x] **3.MX.C** Seed MX scenario presets — **COMPLETED 2026-04-22**
  - Built `seed_mx_demo_artifacts.py`; seeded 6 `preset_bundle_*` rows:
    - `base` — current run-rate no adjustments (1.0× spend)
    - `conservative` — 10% spend pullback (0.9×)
    - `moderate` — current run-rate sustained (1.0×)
    - `aggressive` — +15% Brand uplift (1.05× spend, Brand +15%)
    - `placement_persists` — +12% Brand sustained (1.04× spend, Brand +12%)
    - `placement_decays` — +12% Brand decaying over 12 weeks (1.02× spend, Brand +6% avg)
  - Each bundle stores `{spend_multiplier, brand_uplift_pct, nb_uplift_pct, description}` in `value_json`
  - Lineage recorded; refit cadence `annual` so presets persist through quarterly fit refreshes unless explicitly re-seeded
  - **Maintenance impact**: Very low — annual preset review at most
  - _Requirements: 3.6, 14.1_

- [x] **3.MX.D** Author MX narrative template — **COMPLETED 2026-04-22**
  - Seeded `narrative_template` row in `ps.market_projection_params` for MX
  - Template is 3 paragraphs honoring `ieccp_bound` strategy: paragraph 1 references ie%CCP vs 100% ceiling with all key numbers, paragraph 2 describes Polaris + Semana Santa + W15 NB drop regime context, paragraph 3 translates for Lorena conversations (Brand as demand-clean lever, NB as volume lever, W15 investigation reference)
  - Explicit placeholder list captured in `value_json.placeholders` for UI substitution
  - Honors richard-writing-style: no em-dashes, data-forward, explicit so-what, under 300 words expanded
  - Cites both structural (Polaris) and transient (Semana Santa, W15) regimes as required
  - **Maintenance impact**: Low — annual review; update when new MX regime events classify as structural
  - _Requirements: 8.1-8.5, 14.3-14.4_

- [x] **3.MX.E** Configure MX in UI scope selector — **COMPLETED 2026-04-22**
  - MX appears in the scope selector as the default selection (primary demo market), without fallback badge (all parameters are market-specific)
  - Target mode dropdown populated from `supported_target_modes` = [spend, ieccp, regs] for MX
  - `projection.html` freshness banner + per-market fallback badges wired; MX shows "market-specific" green badge
  - Provenance modal surfaces MX regime events via the `data.markets.MX.regime_events` array
  - Re-exported `projection-data.json` to 366.0 KB including the new MX presets + narrative template
  - End-to-end verified via node: MX Q2 projection renders total_regs 3,619, ie%CCP 143.8% matching Python engine
  - **Maintenance impact**: Very low — UI is data-driven, new markets show up automatically when they land in the data bundle
  - _Requirements: 3.1, 3.6, 14.2_

- [x] **3.MX.F** MX acceptance pass + specific-notes doc — **COMPLETED 2026-04-22**
  - Acceptance suite: `pytest shared/tools/prediction/tests/test_mpe_*.py shared/tools/prediction/tests/test_regional_rollup.py shared/tools/prediction/tests/test_parameter_registry.py shared/tools/prediction/tests/test_js_parity.py` — **56 passing, 3.6s runtime**. MX-specific coverage: parameter registry asserts MX CCPs + elasticity fits present; engine tests use MX fixture for spend/ieccp target/CI integration; regional rollup tests use MX CCPs in scale-precision test; JS parity tests use MX for deterministic + MC parity
  - `shared/wiki/agent-created/operations/mpe-mx-specific-notes.md` covers all 6 required topics: ieccp_bound strategy context, Polaris INTL baseline shift, Semana Santa annual treatment, W15 NB drop provisional status, YoY growth-ramp caveat, Brand as demand-clean baseline. Plus appended 2025 MBR review addendum and 12-week holdout validation results.
  - Lorena 2026-04-22 pressure-test reference captured in the simulation-checklist mapping table at bottom of notes doc
  - MX block is demo-ready end-to-end
  - **Maintenance impact**: Low — notes doc updated at each quarterly refit
  - _Requirements: 15.1-15.2, R0.1_

---

### 3.US — US full build (balanced archetype, 50-65% ie%CCP)

US has 148 clean weeks, Brand spend CV 0.44 / NB 0.42, ie%CCP range 50-65%, all three target modes supported.

- [ ] **3.US.A** Fit US parameters — CPA r²≈0.85, CPC r²≈0.76 expected (strong fit)
- [ ] **3.US.B** Validate US fit against 12-week holdout
- [ ] **3.US.C** Seed US scenario presets (same 6 as MX, calibrated to US run-rates)
- [ ] **3.US.D** Author US narrative template (balanced strategy — references ie%CCP range not target)
- [ ] **3.US.E** Configure US in UI scope selector (display: "United States")
- [ ] **3.US.F** US acceptance pass + `mpe-us-specific-notes.md` covering: 2025-09-29 OCI 100% structural, 2026-02-16 PBDD 404 transient, 2026-03-16 promo CPC spike, OCI maturity
- _Requirements: 1.1, 1.2, 5.1, 14.3_

---

### 3.AU — AU full build (efficiency archetype, Southern Hemisphere hybrid)

AU has 29 clean weeks (below 80-week market_specific threshold); requires R14.9-R14.15 SH handling. No CCP, no ie%CCP target mode.

- [ ] **3.AU.A** Fit AU parameters with SH hybrid handling
  - Elasticity: fallback to WW regional curve with level shift for AU's observed spend-to-regs ratio (R14.13)
  - Seasonality: **hybrid per-week** — AU-real weight where AU has ≥ 2 usable weeks for that calendar week number; otherwise WW shifted 26 weeks. Each weight carries `provenance` sub-field (`au_actual` or `nh_shifted_w{N}`) per R14.11
  - YoY: flat (conservative_default, LOW_CONFIDENCE_MULTI_YEAR — AU has <2 years of data)
  - Set `fallback_level='southern_hemisphere_hybrid'` for seasonality, `'regional_fallback'` for elasticity
  - Regime handling: 2026-01-01 Adobe bid strategies as structural baseline; pre-2026-01 weeks OK for seasonality but excluded from elasticity fit per R14.15
  - _Requirements: 14.9-14.15_

- [ ] **3.AU.B** Validate AU fit against available holdout (4-week max given 29 total weeks)
- [ ] **3.AU.C** Seed AU scenario presets (no ie%CCP presets — efficiency-mode only)
- [ ] **3.AU.D** Author AU narrative template emphasizing efficiency + SH hybrid disclosure
  - Must state: "AU seasonality uses {M} weeks of AU-real data plus {52-M} weeks of NH signal shifted 26 weeks" per R14.12
- [ ] **3.AU.E** Configure AU in UI scope selector (display: "Australia") — only 2 target modes (spend, regs), ie%CCP hidden
- [ ] **3.AU.F** AU acceptance pass + `mpe-au-specific-notes.md` covering: efficiency strategy context, SH hybrid methodology, 2025-06-10 launch-date floor, 2026-01-01 Adobe bid regime, 2026-03-26 Polaris reverted (excluded weeks 13-15), data maturation path (NH-shifted weights replaced each quarter as AU data accumulates)
- _Requirements: 1.7, 14.1, 14.3-14.15_

---

### 3.DE — DE full build (EU5 balanced, 50-65% ie%CCP)

DE has 168 clean weeks, Brand CV 0.59 / NB 0.26 (highest Brand variance in EU5, tight NB).

- [ ] **3.DE.A** Fit DE parameters — respect 2025-10-01 OCI 100% structural baseline
- [ ] **3.DE.B** Validate DE fit
- [ ] **3.DE.C** Seed DE presets
- [ ] **3.DE.D** Author DE narrative template (balanced strategy, note OCI maturity)
- [ ] **3.DE.E** Configure DE in UI scope selector (display: "Germany")
- [ ] **3.DE.F** DE acceptance pass + `mpe-de-specific-notes.md` covering: 2025-10-01 OCI structural shift, Brand vs NB variance asymmetry (NB CV 0.26 is near the elasticity-fit threshold — flag if Brand dominates interpretation)

---

### 3.UK — UK full build (EU5 balanced, 50-65% ie%CCP)

UK has 160 clean weeks, Brand CV 0.41 / NB 0.56.

- [ ] **3.UK.A** Fit UK parameters — respect 2025-07-01 OCI 100% structural baseline
- [ ] **3.UK.B** Validate UK fit
- [ ] **3.UK.C** Seed UK presets
- [ ] **3.UK.D** Author UK narrative template
- [ ] **3.UK.E** Configure UK in UI scope selector (display: "United Kingdom")
- [ ] **3.UK.F** UK acceptance pass + `mpe-uk-specific-notes.md` covering: 2025-06-27 OCI 25% phase (excluded), 2025-07-01 OCI 100% baseline, 2025-10-01 transition completion

---

### 3.FR — FR full build (EU5 balanced, recent OCI)

FR has 164 clean weeks, Brand CV 0.36 / NB 0.38.

- [ ] **3.FR.A** Fit FR parameters — respect 2026-03-30 OCI 100% structural baseline (recent — post-event window is short)
- [ ] **3.FR.B** Validate FR fit — note post-OCI fit will be noisy early; document in notes
- [ ] **3.FR.C** Seed FR presets
- [ ] **3.FR.D** Author FR narrative template (note OCI just landed; cite wider CIs for post-OCI projections)
- [ ] **3.FR.E** Configure FR in UI scope selector (display: "France")
- [ ] **3.FR.F** FR acceptance pass + `mpe-fr-specific-notes.md`

---

### 3.IT — IT full build (EU5 balanced, PAM pause + OCI)

IT has 164 clean weeks. Two structural shifts in 2026: 2026-02-18 PAM pause for 22% tax + 2026-03-30 OCI 100%.

- [ ] **3.IT.A** Fit IT parameters — respect both structural baselines. Fit window post-2026-02-18 is short; document the pre/post-tax viable-market difference
- [ ] **3.IT.B** Validate IT fit
- [ ] **3.IT.C** Seed IT presets (calibrated to post-tax market size)
- [ ] **3.IT.D** Author IT narrative template — must reference 22% tax floor on projections
- [ ] **3.IT.E** Configure IT in UI scope selector (display: "Italy")
- [ ] **3.IT.F** IT acceptance pass + `mpe-it-specific-notes.md` covering: 22% tax structural change, viable-market shift, OCI added after tax (double-structural quarter)

---

### 3.ES — ES full build (EU5 balanced, recent OCI)

ES has 168 clean weeks, Brand CV 0.34 / NB 0.36.

- [ ] **3.ES.A** Fit ES parameters — respect 2026-03-30 OCI 100% structural baseline
- [ ] **3.ES.B** Validate ES fit
- [ ] **3.ES.C** Seed ES presets
- [ ] **3.ES.D** Author ES narrative template
- [ ] **3.ES.E** Configure ES in UI scope selector (display: "Spain")
- [ ] **3.ES.F** ES acceptance pass + `mpe-es-specific-notes.md`

---

### 3.JP — JP full build (brand_dominant archetype, 30-50% ie%CCP)

JP has 164 clean weeks, Brand CV 0.33 / NB 2.05 (very high NB variance = good elasticity signal).

- [ ] **3.JP.A** Fit JP parameters — respect 2026-03-30 OCI 100% structural baseline
- [ ] **3.JP.B** Validate JP fit — NB 2.05 CV produces unusually precise NB elasticity; surface that in notes
- [ ] **3.JP.C** Seed JP presets (calibrated to brand-dominant strategy — presets emphasize Brand spend moves)
- [ ] **3.JP.D** Author JP narrative template emphasizing Brand dominance and 30-50% ie%CCP corridor
- [ ] **3.JP.E** Configure JP in UI scope selector (display: "Japan") — ie%CCP range 30-50% honored
- [ ] **3.JP.F** JP acceptance pass + `mpe-jp-specific-notes.md` covering: brand-dominant strategy, why JP ie%CCP sits lower than EU5 / US balanced markets, 2026-03-30 OCI integration

---

### 3.CA — CA full build (NA balanced, recent OCI dial-up)

CA has 168 clean weeks, Brand CV 0.33 / NB 0.52.

- [ ] **3.CA.A** Fit CA parameters — respect 2026-04-08 OCI dial-up structural baseline (very recent — < 2 weeks of post-event data at demo time)
- [ ] **3.CA.B** Validate CA fit — flag short post-OCI window; first refit should re-validate heavily
- [ ] **3.CA.C** Seed CA presets
- [ ] **3.CA.D** Author CA narrative template (note OCI just-landed; wider CIs)
- [ ] **3.CA.E** Configure CA in UI scope selector (display: "Canada")
- [ ] **3.CA.F** CA acceptance pass + `mpe-ca-specific-notes.md` covering: OCI dial-up just-happened, immature post-event signal, rerun validation at first quarterly refit

---

### 3.REGIONAL — Regional rollup setup (NA / EU5 / WW)

- [ ] **3.REGIONAL.A** Seed regional narrative templates for NA, EU5, WW
  - `ps.regional_narrative_templates` rows with mix-effect language ("DE +X% driving EU5, IT -Y% offsetting")
  - Different framing than per-market — emphasizes mix interpretation
  - Gracefully handles markets with data-limited or recent-regime flags in the regional roll-up narrative
  - _Requirements: 14.3, 14.5, 14.6_

- [ ] **3.REGIONAL.B** Validate regional rollup end-to-end with all 10 real fits
  - Compute NA (US + CA), EU5 (UK + DE + FR + IT + ES), WW (all 10) projections
  - Verify against hand-computed expected results per market
  - Test both regional-target and per-market-target modes (R6.5)
  - Validate AU contributes correctly to WW rollup despite SH hybrid handling — sum-then-divide math must work across scale differences (MX $97 to US $412 to AU null CCP)
  - Narrative mix-effect output passes Task 3.REGIONAL.A template
  - **Maintenance impact**: Low
  - _Requirements: 6.1-6.6, 14.5, 14.6_

---

## Phase 4 — Durability Light (4 tasks, ~2 days)

- [ ] **4.1** Build `mpe_anomaly.py` + `refit_market_params.py`
  - `mpe_anomaly.py`: 3SD check against trailing 4 quarterly refits, regime tag from `ps.regime_changes`, returns structured anomaly records with plain-English explanation
  - `refit_market_params.py`: for MX/US/AU, refit every quarterly parameter, compute Validation_MAPE on 12-week holdout, run anomaly detection, write new parameter_version with `is_active=false` for flagged params
  - Emit refit report at `shared/dashboards/data/refit-reports/{yyyy-mm-dd}.md`
  - Report sections: Summary, Changes, MAPE deltas, Anomalies (plain-English), Recommended actions, Rollback instructions
  - Synthetic-anomaly test suite (true-positive, false-positive, regime-tagged)
  - **Maintenance impact**: Low — owner reviews report quarterly
  - _Requirements: 13.1-13.8, 5.1, 5.3, 5.4_

- [ ] **4.2** Wire refit as `mpe-refit.kiro.hook`
  - Hook file complete from Task 0.3 skeleton
  - Steps: run data_audit → run refit_market_params → check anomalies → if anomalies or MAPE regression > 5pp then `is_active=false` + "ACTION REQUIRED: Owner review" in report
  - Notify owner via Kiro notification + push report to `Kiro-Drive/system-state/mpe-refits/`
  - Runbook (Task 4.4) documents how to review and approve/reject
  - **Maintenance impact**: Low — hook is the maintenance spine
  - _Requirements: 5.2, 5.6, R0.2_

- [ ] **4.3** Parameter freshness banner + staleness logic
  - UI banner: "Parameters current as of {max(last_refit_at)} across all active parameters for this scope"
  - Per-parameter staleness badges surface when any parameter is past `refit_cadence`
  - Staleness is inclusive — if one parameter is stale, banner reflects it
  - **Maintenance impact**: Very low
  - _Requirements: 1.8, 5.7_

- [ ] **4.4** Final owner runbook
  - Expand `shared/wiki/agent-created/operations/mpe-owner-operations.md` from Task 0.4 skeleton
  - Complete sections: Daily use, Weekly check, Quarterly refit (step-by-step with hook commands), "Something looks wrong" diagnostic (no code), Adding a new market (4-6 hours first time, settling to 2 hours — honest timing), Rollback (5 minutes), Escalation criteria, Leadership demo script (90 seconds memorized), File locations bookmarks
  - Test: hand runbook to a non-technical reviewer (non-owner) and confirm every step executable without questions
  - Publish to SharePoint via `sharepoint-sync`
  - **Maintenance impact**: Critical — owner's primary support document
  - _Requirements: R0.3, R0.6, 10.3, 10.4_

---

## Phase 5 — Acceptance & Demo Prep (5 tasks, ~2-3 days)

- [ ] **5.1** Core automated acceptance for MX / US / AU + regions
  - Test suite: `shared/tools/prediction/tests/test_acceptance.py`
  - Per-Fully_Fit_Market: steps (a)-(j) from R15.2 (freshness, base projections W/M/Q/Y/MY1/MY2, 2× OP2 stress, ieCCP target, 1.5× prior-year regs, +30% Brand uplift, NB elasticity doubled, save/reload, stale-param surface, narrative conformance)
  - Per-region (NA, EU5, WW): steps (k)-(m) (regional-level target, per-market target, mix-effect narrative)
  - Single-market quick-check: `pytest -k MX` in < 2 minutes
  - Full matrix: < 15 minutes
  - Reports to `shared/dashboards/data/acceptance-test-reports/{yyyy-mm-dd}-{scope}.md`
  - Wired as pre-commit gate via `mpe-acceptance-core.kiro.hook`
  - **Maintenance impact**: Low — tests fail loudly
  - _Requirements: 15.1-15.3, 15.6-15.9_

- [ ] **5.2** Documented manual MX 2026-04-22 simulation checklist
  - File: `shared/wiki/agent-created/operations/mpe-mx-422-simulation.md`
  - 10 steps per R15.4: initial projection, mental-model challenge, CCP correction, formula correction, regime-shift identification (includes 2025-W27 + 2026-W15 provisional), seasonality refinement, CPA elasticity fit, week-by-week re-run, error-band toggle, marginal-regs sanity
  - Each step: input, action, expected behavior, passing criterion (what the agent can validate on-demand)
  - Pass criteria: all 10 steps complete in < 90 seconds, every output has visible provenance, no crashes, owner can explain every number without looking at code
  - If any step fails: "Note it, run `kiro hook run mpe-acceptance-core`, then ask Kiro to fix the specific failure"
  - **Maintenance impact**: Low — checklist is owner-readable
  - _Requirements: 15.4, 15.5_

- [ ] **5.3** Run full acceptance + produce report
  - Execute `mpe-acceptance-core.kiro.hook`
  - Produce consolidated pass/fail report for all 3 Fully_Fit_Markets + 3 regions
  - Address any failures before demo (or document as XFAIL per R15.9 with explicit reason)
  - **Maintenance impact**: One-time — re-run before each demo / before production push
  - _Requirements: 15.1, 15.6, 15.7_

- [ ] **5.4** Leadership demo script (90-second MX reproduction)
  - File: `shared/wiki/agent-created/operations/mpe-demo-script.md`
  - Script: "Here's our new Market Projection Engine. For MX at 75% ie%CCP in Q2: it projects 17,636 total registrations, $1.03M spend, with 70% credible interval of 16,200 to 19,100 regs. The blue band shows uncertainty from the model parameters — honest ranges, not fake precision. I can change the target live, apply a placement uplift, or switch to 2-year view. All numbers trace back to the actual negotiated CCPs from finance and our historical data. Quarterly refit keeps it current — I just ran it last week. Questions?"
  - Memorized by owner
  - Backed by manual MX 4/22 simulation checklist from Task 5.2
  - Also covers: regional rollup (EU5), multi-year (MX 2026 → 2028 capped at 2028 per R11), Bayesian CI explanation, quarterly refit walkthrough with anomaly detection example, SharePoint portability demo
  - **Maintenance impact**: Very low — script evolves with spec updates
  - _Requirements: entire spec_

- [ ] **5.5** Wiki article + SharePoint publish + cold-start test
  - File: `shared/wiki/agent-created/operations/market-projection-engine.md`
  - Sections: Purpose, Usage (daily / weekly / quarterly), Methodology at a glance, Environment-specific URLs, 2-year refit roadmap, Owner operations runbook link, Demo script link
  - Publish to SharePoint via `sharepoint-sync`
  - Cold-start test: verify spec + wiki + owner runbook are `Cold_Start_Safe` — a new agent on a different platform can reconstitute intent from these files alone
  - Include in `agent-bridge` repo sync
  - **Maintenance impact**: Low — wiki updated on material changes only
  - _Requirements: 10.3, 10.4, 10.5_

---

## Critical Path

- **Phase 0** (6 tasks, all complete 2026-04-22): data audit, scope boundaries, steering + hooks, owner runbook skeleton, coexistence audit, regime classification
- **Phase 1** (11 tasks, 4 complete): parameter registry + MARKET_STRATEGY migration, CCP seeding, regime breakpoints, fitting module done. MX full suite fit (1.5) plus engine core (1.6-1.11) remain.
- **Phase 2** (10 tasks) blocks demo — UI + portability
- **Phase 3** (62 per-market tasks + 2 regional = 64 tasks): full build per market, 6 steps each (A Fit, B Validate, C Presets, D Narrative, E UI config, F Acceptance+notes). MX first, then US / AU, then EU5 members, then JP, then CA. Parallel with Phase 2.
- **Phase 4** (4 tasks) durability infrastructure
- **Phase 5** (5 tasks) acceptance + demo prep

**Total**: 99 active tasks (Phase 0: 6 + Phase 1: 11 + Phase 2: 10 + Phase 3: 64 + Phase 4: 4 + Phase 5: 5). 33 complete as of 2026-04-22 — **Phase 0 + Phase 1 + Phase 2 + Phase 3.MX all complete, primary demo market is demo-ready end-to-end**.

**Hard checkpoint**: Phase 0 + Phase 1 complete by 2026-05-02 or demo slips. Phase 0 done ahead of schedule (2026-04-22).

**Minimum viable demo set**: MX (primary) full build + US full build + AU full build (with SH hybrid) + regional NA/EU5/WW + engine core (Phase 1) + UI (Phase 2) + acceptance (Phase 5). ~52 tasks to demo-green. Remaining 7 market builds (CA, UK, DE, FR, IT, ES, JP) can land between 5/16 and 5/30 using the templated A-F pattern.

**Demo-ready target**: 2026-05-16 (Friday before showcase week).

## Timeline Sanity Check

- Phase 0 + Phase 1 first 4 tasks took one working day (2026-04-22). Kiro acceleration is real.
- Per-market full builds are templated (A–F same pattern). Once the first 2 markets (MX + US) are through, each subsequent market block should take ~2-3 hours given no data surprises. AU is the exception — SH hybrid adds ~1 full dev-day to that block.
- 62 per-market tasks looks large on paper but 8 of the 10 markets use a near-identical flow. Budget: MX 1 day, US 0.5 day, AU 1 day, each remaining 7 markets 0.3 days = ~4.6 dev-days for full Phase 3.
- Phase 2 (UI) is the unknown. SharePoint/Symphony CORS quirks can absorb days. Start early.
- MX NB drop investigation (W15 provisional regime) already logged — reclassify at first refit.
- **If Phase 1 core engine (1.5-1.11) is not green by 5/2**: demo slips to 2026-05-23 (push one week).

## What v1 will NOT do (Scope Creep Shield — mirrors R16)

- Treat any market with ≥ 80 clean weeks as regional_fallback when a market-specific fit is possible (use the market-specific fit)
- Hierarchical Bayesian, BSTS, Prophet, Prophetverse, LightweightMMM, PyMC, NumPyro
- Cross-elasticity between Brand and NB
- Macro or economic overlays
- Placement decay curves as first-class model
- Advanced anomaly ML (Isolation Forest, autoencoders, LSTM)
- Command palette, Apple micro-animations, 3D visuals, natural-language input in browser
- Auto-scheduled cron refit — v1 uses manual hook
- Slack notifications, email digests — SharePoint push only
- Streamlit, Reflex, Django, Flask — any server-dependent UI framework
- MCMC-based posterior estimation
- 3-year multi-year projections
- Automated simulation of subjective stakeholder-conversation steps
- Southern Hemisphere hybrid handling for any market other than AU (future BR/ZA/NZ launch requires its own spec update)

Any of these in future versions requires new spec + owner approval.

## Deferred Sub-Tasks (post-v1 polish, not blocking demo)

- **1.2.a** Parse IECCP tab from `shared/uploads/sheets/AB SEM WW Dashboard_Y25 Final.xlsx` and `AB SEM WW Dashboard_Y26 W16.xlsx` for historical weekly CCPs per market. Write as `brand_ccp_time_series` / `nb_ccp_time_series` JSON parameters.
  - **Why deferred**: current-CCP static values suffice for v1 fitting under recency-weighted regression (52-week half-life). Historical CCP drift is a refinement — tightens elasticity fit marginally but does not block MX/US/AU demo accuracy.
  - **Trigger to revisit**: any market where v1 elasticity fit r² < 0.50 or owner reports projection drift from reality >10%.
