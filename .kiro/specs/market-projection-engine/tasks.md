# Implementation Plan — Market Projection Engine (MPE) v1

**Goal**: Build a leadership-demo-ready projection tool covering all 10 markets × 3 regions × 9 KPIs × 5 time periods (W/M/Q/Y/MY) × 3 target modes, with:
- CPC elasticity (not just CPA)
- Multi-year projections (1-3 years forward)
- Recency-weighted YoY growth trends per market
- Bayesian credible intervals on every output KPI
- Anomaly detection on quarterly parameter refits
- Per-market and per-region narrative templates
- Rigorous acceptance test that simulates the MX 4/22 stakeholder pressure-test across all markets

**Target demo date**: Mid-to-late May 2026. **Minimum viable for demo**: Phases 1-2 + MX/AU/US fits + acceptance test passing for those 3 = ~32 tasks.

**Full production readiness**: All phases complete = 72 tasks.

**Sequencing**: Phase 1-2 are critical path. Phases 3-4 can run partially in parallel. Phase 5 hardens for production.

## Phase 1 — Foundation (week of 2026-04-28)

- [ ] 1. Create parameter registry schema in DuckDB
  - Write `ps.market_projection_params` table DDL with versioning columns (market, parameter_name, parameter_version, value_scalar, value_json, refit_cadence, last_refit_at, last_validated_at, validation_mape, source, fitted_on_data_range, notes, is_active)
  - Write `ps.market_projection_params_current` view
  - Write `ps.parameter_validation` table DDL
  - Write `ps.parameter_anomalies` table DDL
  - Write `ps.regional_narrative_templates` table DDL
  - Write `ps.projection_scores` table DDL
  - Write migration script `shared/tools/prediction/mpe_schema.sql`
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 5.4, 13.3, 14.3_

- [ ] 2. Seed CCPs from canonical sources (CCP Q1'26 check file column U + WW dashboard IECCP tab for history)
  - Parse `shared/uploads/sheets/CCP Q1'26 check yc.xlsx` Summary tab, **Column U ("FINAL ALIGNED")** for post-negotiation 2026 Q1 CCPs per market per segment
  - Canonical negotiated values (from column U): US Brand $412.51 / NB $48.52, CA Brand $203.77 / NB $38.52, UK Brand $250.00 / NB $60.00, DE Brand $291.76 / NB $141.26, FR Brand $155.31 / NB $85.10, IT Brand $151.67 / NB $92.03, ES Brand $150.00 / NB $80.03, JP Brand $224.42 / NB $78.33, MX Brand $97.22 / NB $27.59
  - AU has no CCP (efficiency strategy) — set ccp fields to null, supported_target_modes excludes 'ieccp'
  - WW/EU5/NA CCPs derived at query time from constituent markets (no direct seed)
  - Parse `shared/uploads/sheets/AB SEM WW Dashboard_Y25 Final.xlsx` IECCP tab for historical weekly CCPs per market
  - Parse `shared/uploads/sheets/AB SEM WW Dashboard_Y26 W16.xlsx` IECCP tab for 2026 weekly CCPs
  - Write `seed_market_ccps.py` script to write per-market brand_ccp, nb_ccp, brand_ccp_time_series, nb_ccp_time_series to registry
  - Also seed column N ("Q1 Static CCP") as `brand_ccp_q1_static` / `nb_ccp_q1_static` for historical reference and transition-period calculations
  - _Requirements: 1.1, 1.2, 1.5_

- [ ] 3. Seed historical regime-change breakpoints
  - Insert MX H1/H2 2025 regime change (no ie%CCP → 100% ie%CCP ceiling at W27) in ps.regime_changes
  - Research and insert any other known historical breakpoints per market (campaign strategy changes, CCP renegotiations, placement launches) — pulls from project_timeline
  - _Requirements: 11.7, 13.6_

- [ ] 4. Build recency-weighted fitting module `mpe_fitting.py`
  - Exponential decay weighting with configurable half-life (default 52 weeks)
  - Log-linear regression for elasticity curves (CPA and CPC) with posterior estimation
  - Weekly seasonality fitting (normalized weights, with posterior per week)
  - YoY growth trend fitting (per-market per-segment)
  - Writes r_squared and posterior parameters to value_json
  - _Requirements: 1.1, 11.2, 11.3, 11.5_

- [ ] 5. Fit MX parameters (full suite, v1 seed)
  - Brand CPA elasticity, NB CPA elasticity (leverages existing curve from mx_precise_projection.py, extended with recency weighting)
  - Brand CPC elasticity, NB CPC elasticity (new for v1)
  - Brand seasonality shape, NB seasonality shape
  - Brand YoY growth, NB YoY growth (fit from 2024-2026 data)
  - baselines and CPC values
  - ieccp_target=100, ieccp_range={low:90, high:110}
  - supported_target_modes=['spend','ieccp','regs']
  - _Requirements: 1.1, 11.2, 11.3_

- [ ] 6. Build Bayesian uncertainty module `mpe_uncertainty.py`
  - Monte Carlo sampling over parameter posteriors (default 1000 samples)
  - Propagate samples through engine to get distribution of each output KPI
  - Compute 50%, 70%, 90% credible intervals
  - HIGH_UNCERTAINTY warning when 90% interval > 2× central
  - _Requirements: 12.1, 12.2, 12.3, 12.5, 12.6, 12.8_

- [ ] 7. Build Python engine core `shared/tools/prediction/mpe_engine.py`
  - Implement `ProjectionInputs` and `ProjectionOutputs` dataclasses (with credible_intervals, yoy_growth_applied fields)
  - Implement `project()` for single-market, Year target_period, Spend_Target mode
  - Wire up parameter loading from ps.market_projection_params_current
  - Integrate with mpe_uncertainty for credible interval output
  - Produce weekly + totals output conforming to schema
  - _Requirements: 2.1, 2.2, 2.4, 7.1, 12.1, 12.2, 12.3_

- [ ] 8. Extend engine to ieCCP_Target and Regs_Target modes
  - Binary search solver for ieCCP_Target
  - Feasibility-aware Regs_Target solver
  - _Requirements: 2.5, 2.6, 2.8_

- [ ] 9. Extend engine to Week, Month, Quarter, Year, Multi_Year time_periods
  - Parse `W{NN}`, `M{MM}`, `Q{N}`, `Y{YYYY}`, `MY{N}` inputs
  - Multi_Year applies YoY_Growth_Trend multiplicatively across years
  - Emit LOW_CONFIDENCE_MULTI_YEAR if market has < 104 weeks of data
  - VERY_WIDE_CI warning when 3-year 90% interval > 3× central
  - _Requirements: 2.1, 2.3, 11.1, 11.4, 11.6, 11.8_

- [ ] 10. Add regional rollup support (NA, EU5, WW)
  - Per-market projection then sum segments
  - Regional-level vs per-market-level target mode options
  - Validate sum-then-divide CCP math against hand-computed expected values
  - _Requirements: 6.1-6.5_

- [ ] 11. Implement feasibility check and warning emission
  - feasibility_check() returns structured reasons for infeasibility
  - Binding constraint identification
  - Full warning taxonomy: HIGH_EXTRAPOLATION, LOW_CONFIDENCE, SEASONALITY_DOMINATED, HIGH_UNCERTAINTY, LOW_CONFIDENCE_MULTI_YEAR, VERY_WIDE_CI, STALE_PARAMETERS, SETUP_REQUIRED
  - _Requirements: 2.8, 9.1-9.5, 11.6, 12.5_

- [ ] 12. Python unit test suite for engine core
  - 50+ tests covering each target_mode, each market archetype (ie%CCP-bound, efficiency, balanced, brand-dominant), edge cases
  - Tests for regional rollup math
  - Tests for feasibility and warning emission
  - Tests for multi-year projections and YoY growth application
  - _Requirements: 2, 6, 9, 11_

- [ ] 13. Build CLI entry point
  - `python3 -m shared.tools.prediction.mpe_engine --market MX --period 2026-Q2 --target ieCCP:75 --format json`
  - `python3 -m shared.tools.prediction.mpe_engine --region EU5 --period MY2 --target spend:5000000 --format markdown`
  - _Requirements: 7.4_

## Phase 2 — UI, Portability, and Persistence (week of 2026-05-05)

- [ ] 14. Build export script for dashboard data
  - `shared/dashboards/export-projection-data.py` reads ps.market_projection_params_current + ps.v_weekly YTD
  - Writes `shared/dashboards/data/projection-data.json` with parameters, YTD actuals, seasonality shapes, YoY trends, posteriors
  - Two build targets: live-fetch variant + standalone-embedded variant
  - Wired into refresh-all.py
  - _Requirements: 3.3, 3.9_

- [ ] 15. Build `shared/dashboards/mpe_engine.js` — JS port of Python engine
  - Mirror math for all target_modes and time_periods
  - Same function signatures as Python (project, feasibilityCheck, narrative)
  - Multi-year YoY trend application
  - Sampling-based credible intervals (wider tolerance vs Python due to JS randomness)
  - _Requirements: 7.3, 7.5, 12.2_

- [ ] 16. Build JS/Python parity test suite
  - 30 canonical test cases in `shared/tools/prediction/tests/parity_cases.json` (including multi-year, regional, credible intervals)
  - Python runs via mpe_engine.py
  - JS runs via playwright/puppeteer headless
  - Assert outputs match within 0.1% for deterministic outputs, 2% for Monte Carlo CI outputs
  - _Requirements: 7.3, 7.5_

- [ ] 17. Build `shared/dashboards/projection.html` structure
  - Header with freshness banner + data-range banner
  - Scope selector (10 markets + NA/EU5/WW rollups), Time_Period (W/M/Q/Y/MY), Input mode tabs (Preset/Sliders/Target)
  - supported_target_modes honored (hide ie%CCP for AU, etc.)
  - Outputs: summary card, ie%CCP gauge, regs/spend line chart with credible interval band, Brand-vs-NB stacked chart, constituent-markets table, warnings panel
  - Actions panel (Save, Copy JSON, Copy markdown, Generate narrative, Score)
  - Saved projections list
  - Style inlined, matches ps-test-calculator.html
  - Chart.js via CDN
  - _Requirements: 3.1, 3.2, 3.6, 3.7, 12.4, 14.2_

- [ ] 18. Embed Methodology_Manifest in HTML
  - Full formula list including multi-year, CPC elasticity, Bayesian CI formulas
  - Output schema with credible intervals
  - Updated automatically by export-projection-data.py
  - _Requirements: 3.4, 7.5, 7.6_

- [ ] 19. Wire sliders, presets, target modes to JS engine
  - Sliders: Brand regs, Brand/NB CPA, Brand/NB CPC, Brand/NB elasticity exponents, placement uplift %, YoY growth override, target ie%CCP, total spend
  - Presets: "Conservative", "Moderate", "Aggressive", "Placement-Persists", "Placement-Decays", "Base-Case", loaded from per-market parameter defaults
  - Target modes: ieccp/spend/regs with dropdown constrained to supported_target_modes for selected scope
  - Slider locking logic
  - Live recompute on input change (debounced)
  - _Requirements: 3.6, 14.1, 14.2_

- [ ] 20. Implement Save/Load/Compare/Score actions
  - Save: POST /api/save-projection writes JSON file
  - Load: GET /api/list-projections + /api/load-projection
  - Copy JSON: clipboard action for SharePoint/Symphony
  - Compare: side-by-side view up to 3 projections
  - Score: runs engine scoring against ps.v_weekly, writes ps.projection_scores
  - _Requirements: 4.1-4.4, 4.6, 4.8_

- [ ] 21. Implement narrative generation with per-market + per-region templates
  - Per-market templates in ps.market_projection_params
  - Per-region templates in ps.regional_narrative_templates
  - Narrative module respects supported_target_modes (AU narrative doesn't mention ie%CCP)
  - Follows richard-writing-style (no em-dashes, data-forward, so-what)
  - Surfaces mix effects for regional output
  - _Requirements: 8.1-8.5, 14.3-14.8_

- [ ] 22. Cross-environment portability testing
  - Kiro dashboard (serve.py live), SharePoint (upload + render + interact), Symphony (iframe embed), standalone file (no external calls)
  - Fix CORS / cache / path issues per environment
  - _Requirements: 3.1, 3.2, 3.8_

- [ ] 23. Add to Kiro dashboard nav
  - Update `shared/dashboards/index.html` with "Projections" tab
  - _Requirements: 10.1_

## Phase 3 — Per-Market Fits (parallel with Phase 2, weeks of 2026-05-05 to 2026-05-19)

Each market-fit task includes: Brand+NB CPA elasticity, Brand+NB CPC elasticity, seasonality shapes, YoY growth trends, baselines, CPCs, narrative template, supported_target_modes, regime_change_breakpoints where known. All fitted with recency-weighted regression.

- [ ] 24. Fit AU parameters (efficiency-strategy market, no ie%CCP)
  - supported_target_modes=['spend', 'regs'] (no ieccp)
  - AU-specific narrative template emphasizing efficiency
  - _Requirements: 1.7, 5.1, 14.1, 14.3, 14.4_

- [ ] 25. Fit US parameters (balanced market, 50-65% ie%CCP)
  - CCPs from file column U: Brand $412.51, NB $48.52
  - _Requirements: 1.1, 1.2, 5.1_

- [ ] 26. Fit CA parameters (balanced market)
  - CCPs from file column U: Brand $203.77, NB $38.52
  - _Requirements: 1.1, 1.2, 5.1_

- [ ] 27. Fit UK parameters
  - CCPs from file column U: Brand $250.00, NB $60.00
  - _Requirements: 1.1, 1.2, 5.1_

- [ ] 28. Fit DE parameters
  - CCPs from file column U: Brand $291.76, NB $141.26
  - _Requirements: 1.1, 1.2, 5.1_

- [ ] 29. Fit FR parameters
  - CCPs from file column U: Brand $155.31, NB $85.10
  - _Requirements: 1.1, 1.2, 5.1_

- [ ] 30. Fit IT parameters
  - CCPs from file column U: Brand $151.67, NB $92.03
  - _Requirements: 1.1, 1.2, 5.1_

- [ ] 31. Fit ES parameters
  - CCPs from file column U: Brand $150.00, NB $80.03
  - _Requirements: 1.1, 1.2, 5.1_

- [ ] 32. Fit JP parameters (brand-dominant market, 30-50% ie%CCP)
  - CCPs from file column U: Brand $224.42, NB $78.33
  - NB elasticity may fall back to regional-fallback if insufficient NB history
  - JP-specific narrative template emphasizing Brand dominance
  - _Requirements: 1.1, 1.2, 1.7, 5.1, 14.3_

- [ ] 33. Seed per-region narrative templates (NA, EU5, WW)
  - Explicitly surface mix effects (e.g., "DE +X% driving EU5, IT -Y% offsetting")
  - Different strategic framing vs per-market
  - _Requirements: 14.3, 14.5, 14.6_

- [ ] 34. Validate regional rollup math with real parameters end-to-end
  - Compute NA, EU5, WW projections
  - Verify against hand-computed expected results per market
  - Test both regional-target and per-market-target modes
  - _Requirements: 6.1-6.5_

## Phase 4 — Durability, Anomaly Detection, and Refit Job (week of 2026-05-19)

- [ ] 35. Build anomaly detection module `mpe_anomaly.py`
  - Compares new parameter_version against trailing distribution
  - Flags parameters > 3 SD from trailing mean
  - Returns structured anomaly records with explanation
  - Respects regime_change_breakpoints (expected-anomaly classification)
  - Test suite with synthetic anomalies (both true-positive and false-positive)
  - _Requirements: 13.1-13.7_

- [ ] 36. Build `refit_market_params.py` job
  - For each market, refit quarterly parameters (CPA elasticity, CPC elasticity, CPCs, baselines, YoY growth)
  - Compute Validation_MAPE on 12-week holdout
  - Run anomaly detection on new parameter values
  - Write new parameter_version with is_active=false for anomaly-flagged parameters
  - Emit refit report at `shared/dashboards/data/refit-reports/{yyyy-mm-dd}.md` including anomalies section
  - _Requirements: 5.1-5.4, 13.1, 13.4_

- [ ] 37. Wire refit job as scheduled hook
  - Create `~/.kiro/hooks/mpe-quarterly-refit.kiro.hook` (manual trigger for v1)
  - _Requirements: 5.2, 5.6_

- [ ] 38. Write annual refit runbook
  - `shared/wiki/agent-created/operations/mpe-annual-refit-runbook.md`
  - Covers CCP refresh from finance, seasonality re-baselining, ie%CCP target reconfirmation, regime-change review
  - _Requirements: 5.5_

- [ ] 39. Build parameter freshness warnings in UI
  - "Parameters current as of {max(last_refit_at)}" banner
  - Per-parameter staleness badges on relevant cards
  - _Requirements: 1.6, 5.7_

## Phase 5 — Rigorous Acceptance Test (week of 2026-05-19)

- [ ] 40. Build acceptance test suite structure `tests/test_acceptance.py`
  - Per-market test functions for all 10 markets
  - Per-region test functions for NA, EU5, WW
  - Single-market quick-check mode (`pytest -k MX`) in < 2 min
  - Full matrix run in < 15 min
  - Output structured reports to `shared/dashboards/data/acceptance-test-reports/`
  - _Requirements: 15.1, 15.6, 15.7_

- [ ] 41. Implement acceptance test steps a-j (from Requirement 15.2) for each market
  - (a) Parameter freshness check
  - (b) Base projections W/M/Q/Y/MY with no errors
  - (c) 2× OP2 budget stress test → HIGH_EXTRAPOLATION + HIGH_UNCERTAINTY
  - (d) ie%CCP target at market's configured level → sanity envelope check
  - (e) 1.5× prior-year regs → converge or structured infeasibility
  - (f) Brand +30% uplift → proportional Brand regs increase
  - (g) NB CPA elasticity double-slope override → NB spend adjustment
  - (h) Save/reload exact match
  - (i) Stale-parameter surface test
  - (j) Narrative output conformance
  - _Requirements: 15.2_

- [ ] 42. Implement regional acceptance test steps k-m
  - (k) Regional-level target → sum-then-divide validation
  - (l) Per-market target → sum of independent solutions
  - (m) Regional narrative mix-effect surfacing
  - _Requirements: 15.3_

- [ ] 43. Implement MX back-and-forth simulation (and DE equivalent)
  - Scripted iterative refinement matching the MX 2026-04-22 session:
    - Initial projection
    - Mental-model challenge (why is this higher than $X?)
    - CCP correction (test the swapped-CCP case)
    - Formula correction (blended vs reg-weighted)
    - Regime-shift identification
    - Seasonality refinement
    - CPA elasticity fit
    - Week-by-week re-run
    - Symmetric vs asymmetric error bands
    - Marginal-regs sanity check
    - Final recommendation
  - Assert each step either updates output consistently or produces documented "cannot improve" response
  - _Requirements: 15.4, 15.5_

- [ ] 44. Wire acceptance test as pre-commit gate
  - For changes touching mpe_engine.py, mpe_engine.js, or ps.market_projection_params schema
  - _Requirements: 15.8_

- [ ] 45. XFAIL handling for data-limited markets
  - Markets with < 104 weeks of data can mark multi-year tests XFAIL
  - Reasons recorded in registry
  - _Requirements: 15.9_

- [ ] 46. Document acceptance test suite in runbook
  - Quarterly review process for test suite itself
  - How new conversation patterns get added
  - _Requirements: 15.10_

## Phase 6 — Deployment and Showcase (week of 2026-05-26)

- [ ] 47. Publish to SharePoint
  - Build standalone variant with parameters embedded
  - Upload to `Kiro-Drive/Artifacts/strategy/projection-engine.html`
  - Upload companion JSON if live-fetch variant
  - Test SharePoint rendering + interactivity
  - _Requirements: 10.2, 10.4_

- [ ] 48. Publish to Symphony (if applicable)
  - Embed via iframe
  - Validate functionality
  - _Requirements: 10.2_

- [ ] 49. Write wiki article
  - `shared/wiki/agent-created/operations/market-projection-engine.md`
  - Purpose, usage, methodology at a glance, environment-specific URLs, 2-year refit roadmap
  - Published via sharepoint-sync
  - _Requirements: 10.3, 10.4_

- [ ] 50. Cold-start portability check
  - Verify spec + wiki are Cold_Start_Safe
  - Included in agent-bridge sync
  - _Requirements: 10.5_

- [ ] 51. Leadership demo prep
  - 15-minute demo script covering:
    - MX scenario (4/22 pressure-test reproduced in 90 seconds via UI)
    - Regional rollup (EU5 projection)
    - Multi-year projection (2026 → 2028 MX for OP1 preview)
    - Bayesian credible intervals explanation
    - Quarterly refit walkthrough with anomaly detection example
    - SharePoint/Symphony portability demo
  - Handout: one-page wiki article summary
  - _Requirements: entire spec_

## Out of v1 (post-launch roadmap)

- Natural-language input in browser (Kiro chat covers this for now)
- Auto-scheduled cron refit (manual trigger for v1)
- Slack notification when refit anomalies fire
- MCMC-based posterior estimation (Monte Carlo sampling from fit-derived posteriors is v1)
- Cross-channel projection (integrating paid social, display, etc.)

---

## Critical path

**Phase 1** (13 tasks) blocks everything.
**Phase 2** (10 tasks) blocks demo.
**Phase 3** (11 tasks) runs parallel with Phase 2. Minimum for demo = MX+AU+US+JP + regional templates.
**Phase 4** (5 tasks) anomaly + refit system.
**Phase 5** (7 tasks) acceptance test.
**Phase 6** (5 tasks) deployment.

**Minimum viable demo**: Phase 1 + Phase 2 + Tasks 24, 25, 32, 33, 34 (AU+US+JP fits + regional templates + regional validation) + acceptance test for those 3 markets + 47 (SharePoint publish) + 51 (demo prep) = **32 tasks**.

**Full production**: all 51 tasks = **51 tasks** (roughly doubled from original 37 with the scope expansions).

**Demo-ready target**: 2026-05-16 (Friday before leadership showcase week).
