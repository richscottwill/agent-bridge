# Implementation Plan: WBR Pipeline Consolidation

## Overview

Consolidate scattered ad-hoc scripts into a single `wbr_pipeline.py` that runs end-to-end when Richard drops a WW Dashboard xlsx. Fix broken foundations first (query.py, ingester schema), then build the BayesianProjector adapter, wire the WBRPipeline orchestrator, add scoring/callout/dive/reporting stages, and validate with an end-to-end simulation on the actual W14 xlsx.

All code is Python. All new files go under `shared/tools/prediction/`. The pipeline reads from and writes to MotherDuck (`ps.*` tables).

## Tasks

- [ ] 1. Fix query.py table references
  - [x] 1.1 Replace `weekly_metrics` → `ps.performance` with `period_type='weekly'` filter in `market_week()` and `market_trend()`
    - `market_week()`: query `ps.performance WHERE market=M AND period_type='weekly' AND period_key=W`
    - `market_trend()`: query `ps.performance WHERE market=M AND period_type='weekly' ORDER BY period_start DESC LIMIT N`
    - _Requirements: 3.1, 3.2, 3.4_
  - [x] 1.2 Replace `monthly_metrics` → `ps.performance` with `period_type='monthly'` filter in `market_month()`
    - `market_month()`: query `ps.performance WHERE market=M AND period_type='monthly' AND period_key=month`
    - _Requirements: 3.3, 3.4_
  - [ ]* 1.3 Write unit tests for fixed query functions
    - Verify SQL strings contain `ps.performance` and correct `period_type` filters
    - Verify zero references to `weekly_metrics` or `monthly_metrics` remain in query.py
    - _Requirements: 3.4_

- [ ] 2. Fix DashboardIngester schema mismatch for OP2 targets
  - [x] 2.1 Fix the projections INSERT in `ingest.py` to align column names with actual table schema
    - Locate the `INSERT OR REPLACE INTO projections` block (~line 2100+)
    - Ensure `op2_regs` column aligns with the schema so values persist
    - _Requirements: 2.6_
  - [x] 2.2 Add OP2 registration target extraction to write both `cost` and `registrations` rows to `ps.targets`
    - After ingester parses OP2 data, write `(market, 'registrations', period_key, op2_regs, 'ww_dashboard')` to `ps.targets`
    - _Requirements: 2.5_

- [x] 3. Checkpoint — Verify foundations
  - Ensure query.py fixes and ingester schema fix are correct. Run any tests. Ask the user if questions arise.

- [ ] 4. Create data models and PipelineResult/ScoringResult dataclasses
  - [x] 4.1 Add `PipelineResult`, `ScoringResult`, and `MarketProjection` dataclasses to `shared/tools/prediction/ptypes.py`
    - `PipelineResult`: week, xlsx_path, stages_completed, stages_failed, markets_processed, rows_loaded, predictions_scored, projections_written, calibration, dive_updated, duration_seconds, errors
    - `ScoringResult`: predictions_scored, hits, misses, surprises, mean_error_pct, calibration
    - `MarketProjection`: market, brand (SegmentForecast), nb (SegmentForecast), total_regs, total_cost, ci_regs_low, ci_regs_high, vs_op2_spend_pct, method
    - Import `SegmentForecast` from `project.py` or redefine in ptypes.py
    - _Requirements: 1.2, 5.1, 6.1, 8.3_

- [ ] 5. Build BayesianProjector adapter
  - [x] 5.1 Create `shared/tools/prediction/bayesian_projector.py` with `BayesianProjector` class
    - `__init__(self, con, calibration_factor)`: store MotherDuck connection and calibration factor
    - `_fetch_history(self, market)`: SELECT from `ps.performance WHERE market=M AND period_type='weekly'` (up to 170 weeks)
    - `_fetch_seasonal_priors(self, market)`: SELECT from `ps.seasonal_priors WHERE market=M`, return `{week_num: factor}`
    - _Requirements: 5.2, 4.1_
  - [x] 5.2 Implement `_inject_seasonality(self, prior, seasonal)` method
    - If `prior.seasonality` is empty (< 52 weeks data): use stored priors directly
    - If `prior.seasonality` has entries (≥ 52 weeks): blend `0.7 * data_derived + 0.3 * stored_prior`
    - Return NEW PriorState — do not mutate original
    - Ensure all resulting seasonal factors are positive floats (> 0.0)
    - _Requirements: 4.2, 4.3, 4.4, 4.5, 4.6_
  - [ ]* 5.3 Write property test for seasonal prior injection — Property 5: Seasonal prior injection correctness
    - **Property 5: Seasonal prior injection correctness**
    - Generate random histories of varying length + seasonal priors, verify blending formula
    - **Validates: Requirements 4.2, 4.3**
  - [ ]* 5.4 Write property test for seasonal injection immutability — Property 6: Seasonal injection immutability
    - **Property 6: Seasonal injection immutability**
    - Generate random PriorState + seasonal dict, verify original unchanged after call
    - **Validates: Requirement 4.4**
  - [ ]* 5.5 Write property test for seasonal factor positivity — Property 7: Seasonal factor positivity invariant
    - **Property 7: Seasonal factor positivity invariant**
    - Generate random seasonal factors, verify all results > 0.0
    - **Validates: Requirement 4.6**
  - [x] 5.6 Implement `project_market(self, market, target_week_num, target_period_key)` method
    - Call `BayesianCore.build_prior()` with historical data
    - Inject seasonality via `_inject_seasonality()`
    - Call `BayesianCore.update_posterior()` with last 4 weeks + calibration_factor
    - Apply seasonal adjustment to point estimate and CI
    - Project Brand + NB segments separately
    - Apply ie%CCP constraint for NB (market-specific)
    - Fetch OP2 targets from `ps.targets`, compute `vs_op2_spend_pct`
    - Return `MarketProjection`
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_
  - [ ]* 5.7 Write property test for point estimate within CI — Property 8: Point estimate within credible interval
    - **Property 8: Point estimate within credible interval**
    - Generate random valid PosteriorStates, verify `point_estimate` within `credible_interval(level=0.7)`
    - **Validates: Requirement 5.4**
  - [ ]* 5.8 Write property test for ie%CCP constraint — Property 9: ie%CCP constraint enforcement
    - **Property 9: ie%CCP constraint enforcement**
    - Generate random NB projections + ie%CCP bounds, verify NB regs capped
    - **Validates: Requirement 5.5**

- [ ] 6. Checkpoint — Verify BayesianProjector
  - Ensure BayesianProjector builds, injects seasonality, and produces MarketProjection. Run any tests. Ask the user if questions arise.

- [ ] 7. Build prediction scoring logic
  - [x] 7.1 Implement `score_prior_predictions(con, current_week)` function in `shared/tools/prediction/wbr_pipeline.py` (or a scoring module)
    - For each market: fetch actuals from `ps.performance`, fetch unscored forecasts from `ps.forecasts`
    - Compute `error_pct = abs(predicted - actual) / actual * 100`
    - Classify: HIT (actual within CI), SURPRISE (error > 20%), MISS (otherwise)
    - UPDATE `ps.forecasts SET actual_value, error_pct, scored=true, score`
    - Call `Calibrator.compute_calibration()` and return `ScoringResult`
    - If no actuals exist, return empty ScoringResult without error
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_
  - [ ]* 7.2 Write property test for scoring classification — Property 10: Scoring classification exhaustiveness and exclusivity
    - **Property 10: Scoring classification exhaustiveness and exclusivity**
    - Generate random forecast+actual pairs, verify exactly one of HIT/MISS/SURPRISE assigned
    - **Validates: Requirements 6.2, 6.3, 6.4, 6.5**
  - [ ]* 7.3 Write property test for scoring closure — Property 11: Scoring closure
    - **Property 11: Scoring closure**
    - Generate random unscored forecasts + actuals, verify all scored after function completes
    - **Validates: Requirement 6.6**

- [ ] 8. Build WBRPipeline orchestrator
  - [x] 8.1 Create `shared/tools/prediction/wbr_pipeline.py` with `WBRPipeline` class
    - `__init__(self, xlsx_path, week_override=None)`: validate xlsx exists, read `MOTHERDUCK_TOKEN` from env
    - `run(self) -> PipelineResult`: execute all 7 stages sequentially, track timing
    - Open single MotherDuck connection, reuse across all stages
    - _Requirements: 1.1, 1.6, 1.7_
  - [x] 8.2 Implement `_stage_ingest(self)` and `_stage_load(self, results)`
    - Stage 1: call `DashboardIngester(xlsx_path).run()`, return results
    - Stage 2: upsert weekly/daily/monthly rows to `ps.performance`, write OP2 targets to `ps.targets`
    - Report total rows upserted
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.7_
  - [x] 8.3 Implement `_stage_score(self)` wiring
    - Call `score_prior_predictions(con, current_week)` from task 7.1
    - Pass calibration factor to Stage 4
    - _Requirements: 6.1, 6.7_
  - [x] 8.4 Implement `_stage_project(self, calibration_factor)`
    - Instantiate `BayesianProjector(con, calibration_factor)`
    - Loop ALL_MARKETS, call `project_market()` for each
    - Write all MarketProjections to `ps.forecasts` with `scored=false`
    - _Requirements: 5.1, 5.7, 5.8_
  - [ ]* 8.5 Write property test for new forecasts written unscored — Property 12: New forecasts written unscored
    - **Property 12: New forecasts written unscored**
    - Verify all newly inserted forecast rows have `scored = false`
    - **Validates: Requirement 5.7**
  - [x] 8.6 Implement fail-forward error handling
    - If Ingest fails → abort (return PipelineResult with error)
    - If any other stage fails → log error, continue to next stage
    - Track stages_completed and stages_failed in PipelineResult
    - _Requirements: 1.3, 1.4_
  - [ ]* 8.7 Write property test for fail-forward resilience — Property 1: Pipeline fail-forward resilience
    - **Property 1: Pipeline fail-forward resilience**
    - Inject random stage failures, verify subsequent stages still execute
    - **Validates: Requirement 1.3**

- [ ] 9. Checkpoint — Verify core pipeline stages
  - Ensure WBRPipeline runs stages 1-4 with fail-forward handling. Run any tests. Ask the user if questions arise.

- [ ] 10. Build callout signal, dive update, and reporting stages
  - [x] 10.1 Implement `_stage_callout_signal(self)` — write signal file for callout skill
    - Write JSON signal file with current week and list of markets with completed projections
    - _Requirements: 7.1_
  - [x] 10.2 Implement `_stage_dive_update(self)` — call `MD_UPDATE_DIVE_CONTENT`
    - Execute `CALL MD_UPDATE_DIVE_CONTENT(dive_id, jsx)` with dive ID `68b308c1-97be-4c72-81ae-517318500de9`
    - Set `result.dive_updated = True` on success, `False` on failure
    - _Requirements: 7.2, 7.3_
  - [x] 10.3 Implement `_stage_report(self, result)` — print summary and record duration
    - Print: week, markets projected, predictions scored, dive status, errors
    - Record `duration_seconds` in PipelineResult
    - _Requirements: 8.1, 8.2, 8.3_
  - [x] 10.4 Add CLI entry point (`if __name__ == '__main__'`) to `wbr_pipeline.py`
    - Accept `xlsx_path` as positional arg, `--week` as optional override
    - Print final report to stdout
    - _Requirements: 1.1_

- [ ] 11. Checkpoint — Full pipeline wired
  - Ensure all 7 stages are wired and the CLI entry point works. Run any tests. Ask the user if questions arise.

- [ ] 12. End-to-end simulation run on W14 xlsx
  - [x] 12.1 Run `WBRPipeline('shared/uploads/sheets/AB SEM WW Dashboard_Y26 W14  vEU5.xlsx', week_override='2026-W14').run()` and validate results
    - Verify all 7 stages complete without fatal errors
    - Verify `ps.performance` has rows for all 10 markets
    - Verify `ps.forecasts` has projection rows for all 10 markets
    - Verify `ps.targets` has OP2 registration targets for markets with OP2 data
    - Verify `PipelineResult.stages_failed` is empty (non-fatal warnings acceptable)
    - Print full PipelineResult summary for Richard to review
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 13. Final checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- The final task (12) is the end-to-end simulation Richard explicitly requested — it validates the whole pipeline against real data
- All new code is Python, targeting the existing `shared/tools/prediction/` directory
- The pipeline replaces `project.py`, `project_full.py`, and `wbr-pipeline.sh` — those files are not deleted but are superseded
