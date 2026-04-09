# Requirements Document

## Introduction

The WBR Pipeline Consolidation replaces scattered ad-hoc scripts (project.py, project_full.py, wbr-pipeline.sh) with a single `wbr_pipeline.py` that runs end-to-end when Richard drops a WW Dashboard xlsx. The pipeline wires the existing Bayesian engine as the sole projection engine, fixes 10 known issues (ingester schema mismatch, wrong table references in query.py, disconnected seasonal priors, missing OP2 reg targets), and produces callouts + projections + dive updates automatically. This is a consolidation and wiring job — not a greenfield build.

## Glossary

- **Pipeline**: The `wbr_pipeline.py` orchestrator that runs the 7-stage sequence: Ingest → Load → Score → Project → Callout → Dive Update → Report
- **BayesianCore**: The existing statistical inference engine at `shared/tools/prediction/core.py` with `build_prior()`, `update_posterior()`, `point_estimate()`, `credible_interval()`
- **BayesianProjector**: New adapter that bridges BayesianCore to MotherDuck data, injecting seasonal priors from `ps.seasonal_priors`
- **DashboardIngester**: The existing xlsx parser at `shared/tools/dashboard-ingester/ingest.py` that extracts daily/weekly/monthly data from WW Dashboard files
- **Calibrator**: The existing self-scoring engine at `shared/tools/prediction/calibrator.py` with `score_prediction()` and `compute_calibration()`
- **PriorState**: Dataclass representing Bayesian prior beliefs, including a `seasonality` dict field
- **PosteriorState**: Dataclass representing updated Bayesian beliefs after incorporating new evidence
- **PipelineResult**: New dataclass summarizing a full pipeline run (stages completed/failed, row counts, errors)
- **ScoringResult**: New dataclass summarizing prediction scoring outcomes (hits, misses, surprises)
- **MarketProjection**: New dataclass holding Brand + NB + Total forecasts for a single market
- **MotherDuck**: Cloud-hosted DuckDB service where `ps.performance`, `ps.seasonal_priors`, `ps.forecasts`, and `ps.targets` tables live
- **ps.performance**: Source-of-truth table with 1511 weekly + 10572 daily + 40 monthly rows of market performance data
- **ps.seasonal_priors**: Table with 520 rows (52 weeks × 10 markets) of hierarchical Bayesian seasonal adjustment factors
- **ps.forecasts**: Table storing pipeline-generated projections with scoring metadata
- **ps.targets**: Table storing OP2 budget targets (cost and registrations) per market
- **ALL_MARKETS**: The 10 supported markets: AU, MX, US, CA, JP, UK, DE, FR, IT, ES
- **ie%CCP**: Metric representing the ratio of incremental-to-existing customer conversion percentage, used as a constraint on NB projections
- **OP2**: Operating Plan 2 — the budget targets for registrations and spend per market
- **HIT**: Scoring outcome when actual value falls within the forecast credible interval
- **MISS**: Scoring outcome when actual value is outside the credible interval but error is ≤ 20%
- **SURPRISE**: Scoring outcome when forecast error exceeds 20%
- **Dive**: MotherDuck's embedded visualization component, updated via `MD_UPDATE_DIVE_CONTENT`

## Requirements

### Requirement 1: Pipeline Orchestration

**User Story:** As Richard, I want a single pipeline script that runs end-to-end when I drop a WW Dashboard xlsx, so that I don't have to manually run 3 separate scripts and wire data between them.

#### Acceptance Criteria

1. WHEN Richard provides an xlsx path to the Pipeline, THE Pipeline SHALL execute all 7 stages sequentially: Ingest, Load, Score, Project, Callout Signal, Dive Update, Report
2. WHEN the Pipeline completes, THE Pipeline SHALL return a PipelineResult containing the list of stages completed, stages failed, markets processed, row counts, and any non-fatal errors
3. WHEN a non-critical stage fails (Score, Callout Signal, Dive Update, Report), THE Pipeline SHALL log the error and continue executing subsequent stages
4. WHEN the Ingest stage fails, THE Pipeline SHALL abort and return a PipelineResult with the ingest error, since no downstream stages can proceed without parsed data
5. WHEN the Pipeline is run twice with the same xlsx file, THE Pipeline SHALL produce the same final state in MotherDuck tables due to upsert semantics throughout all write operations
6. THE Pipeline SHALL open a single MotherDuck connection and reuse it across all 7 stages
7. WHEN the Pipeline starts, THE Pipeline SHALL read the MotherDuck token from the `MOTHERDUCK_TOKEN` environment variable

### Requirement 2: Dashboard Ingestion and Data Loading

**User Story:** As Richard, I want the pipeline to parse the WW Dashboard xlsx and load data into MotherDuck correctly, so that all downstream stages operate on fresh, accurate data.

#### Acceptance Criteria

1. WHEN the Pipeline executes Stage 1 (Ingest), THE DashboardIngester SHALL parse the xlsx file and return per-market analysis results including daily, weekly, and monthly data
2. WHEN the Pipeline executes Stage 2 (Load), THE Pipeline SHALL upsert parsed weekly rows into `ps.performance` with `period_type = 'weekly'`
3. WHEN the Pipeline executes Stage 2 (Load), THE Pipeline SHALL upsert parsed daily rows into `ps.performance` with `period_type = 'daily'`
4. WHEN the Pipeline executes Stage 2 (Load), THE Pipeline SHALL upsert parsed monthly rows into `ps.performance` with `period_type = 'monthly'`
5. WHEN the DashboardIngester extracts OP2 registration targets from the xlsx, THE Pipeline SHALL write both `cost` and `registrations` rows to `ps.targets` for each market that has OP2 data
6. WHEN the DashboardIngester writes projection data, THE DashboardIngester SHALL align INSERT column names with the actual `projections` table schema so that `op2_regs` values persist correctly
7. WHEN Stage 2 completes, THE Pipeline SHALL report the total number of rows upserted to `ps.performance`

### Requirement 3: Query Layer Table Reference Fix

**User Story:** As a developer, I want query.py to read from the correct `ps.performance` table instead of the nonexistent `weekly_metrics` and `monthly_metrics` tables, so that data access functions return actual data.

#### Acceptance Criteria

1. WHEN `market_week()` is called, THE query layer SHALL query `ps.performance` with `period_type = 'weekly'` and the specified market and week filters
2. WHEN `market_trend()` is called, THE query layer SHALL query `ps.performance` with `period_type = 'weekly'`, ordered by `period_start DESC`, limited to the specified number of weeks
3. WHEN `market_month()` is called, THE query layer SHALL query `ps.performance` with `period_type = 'monthly'` and the specified market and month filters
4. THE query layer SHALL contain zero references to `weekly_metrics` or `monthly_metrics` table names after the fix is applied

### Requirement 4: Seasonal Prior Injection

**User Story:** As Richard, I want the Bayesian engine to use the 520 seasonal prior rows from `ps.seasonal_priors` when building projections, so that forecasts account for known weekly seasonality patterns.

#### Acceptance Criteria

1. WHEN the BayesianProjector builds a prior for a market, THE BayesianProjector SHALL fetch seasonal factors from `ps.seasonal_priors` for that market and metric
2. WHEN the market has fewer than 52 weeks of historical data in `ps.performance`, THE BayesianProjector SHALL populate `PriorState.seasonality` directly from `ps.seasonal_priors` factors
3. WHEN the market has 52 or more weeks of historical data, THE BayesianProjector SHALL blend data-derived seasonality with stored priors using a weighted average of 0.7 × data-derived + 0.3 × stored prior
4. WHEN `_inject_seasonality()` is called, THE BayesianProjector SHALL return a new PriorState without mutating the original PriorState input
5. IF `ps.seasonal_priors` has no rows for a market, THEN THE BayesianProjector SHALL return the prior unchanged with flat seasonality and log a warning
6. THE BayesianProjector SHALL ensure all seasonal factors in the resulting PriorState are positive floats

### Requirement 5: Bayesian Projection Engine Wiring

**User Story:** As Richard, I want the pipeline to use BayesianCore as the sole projection engine instead of ad-hoc median+IQR calculations, so that projections are statistically grounded and self-improving.

#### Acceptance Criteria

1. WHEN the Pipeline executes Stage 4 (Project), THE BayesianProjector SHALL produce a MarketProjection for each of the 10 markets in ALL_MARKETS
2. WHEN projecting for a market, THE BayesianProjector SHALL call `BayesianCore.build_prior()` with historical data from `ps.performance`
3. WHEN projecting for a market, THE BayesianProjector SHALL call `BayesianCore.update_posterior()` with the most recent 4 weeks of evidence and the current calibration factor
4. FOR ALL projections, THE BayesianProjector SHALL ensure the point estimate falls within the 70% credible interval bounds (`ci_regs_low ≤ total_regs ≤ ci_regs_high`)
5. WHEN a market has an ie%CCP constraint defined in market strategy, THE BayesianProjector SHALL cap NB registration projections by the ie%CCP bound
6. WHEN OP2 targets exist in `ps.targets` for a market, THE MarketProjection SHALL include `vs_op2_spend_pct` comparing projected cost to the OP2 cost target
7. WHEN Stage 4 completes, THE Pipeline SHALL write all MarketProjection results to `ps.forecasts` with `scored = false`
8. THE Pipeline SHALL not reference `project.py` or `project_full.py` for projection logic

### Requirement 6: Prediction Scoring

**User Story:** As Richard, I want the pipeline to automatically score last week's predictions against this week's actuals, so that the engine self-calibrates and I can track forecast accuracy.

#### Acceptance Criteria

1. WHEN the Pipeline executes Stage 3 (Score), THE Pipeline SHALL identify all unscored forecasts in `ps.forecasts` where `target_period` matches the current week
2. WHEN actuals exist in `ps.performance` for the current week and market, THE Pipeline SHALL compute `error_pct = abs(predicted_value - actual_value) / actual_value × 100`
3. WHEN the actual value falls within the forecast credible interval, THE Pipeline SHALL assign a score of 'HIT'
4. WHEN the forecast error exceeds 20%, THE Pipeline SHALL assign a score of 'SURPRISE'
5. WHEN the actual value is outside the credible interval and error is 20% or less, THE Pipeline SHALL assign a score of 'MISS'
6. WHEN scoring completes, THE Pipeline SHALL mark all scored forecasts with `scored = true` in `ps.forecasts`
7. WHEN scoring completes, THE Pipeline SHALL invoke `Calibrator.compute_calibration()` and pass the resulting calibration factor to Stage 4 (Project)
8. IF no actuals exist for the current week, THEN THE Pipeline SHALL score zero predictions and return an empty ScoringResult without error

### Requirement 7: Callout Signal and Dive Update

**User Story:** As Richard, I want the pipeline to automatically signal the callout skill and update the dive dashboard after projections are written, so that Brandon gets callouts and the dive stays current without manual intervention.

#### Acceptance Criteria

1. WHEN the Pipeline executes Stage 5 (Callout Signal), THE Pipeline SHALL write a signal file containing the current week and list of markets with completed projections
2. WHEN the Pipeline executes Stage 6 (Dive Update), THE Pipeline SHALL call `MD_UPDATE_DIVE_CONTENT` with the configured dive ID and the dive-v3.jsx component
3. IF the dive update fails, THEN THE Pipeline SHALL set `PipelineResult.dive_updated` to false and log the error without aborting the pipeline

### Requirement 8: Pipeline Reporting

**User Story:** As Richard, I want a clear summary report after each pipeline run, so that I can quickly see what happened — how many markets were projected, how many predictions were scored, and whether anything failed.

#### Acceptance Criteria

1. WHEN the Pipeline executes Stage 7 (Report), THE Pipeline SHALL print a summary including: week processed, number of markets projected, number of predictions scored, dive update status, and any errors
2. WHEN stages have failed, THE Pipeline SHALL list each failed stage and its error in the report
3. THE Pipeline SHALL record the total duration in seconds in `PipelineResult.duration_seconds`

### Requirement 9: End-to-End Validation via Simulation

**User Story:** As Richard, I want to validate the consolidated pipeline by running it against the actual W14 xlsx file (`shared/uploads/sheets/AB SEM WW Dashboard_Y26 W14 vEU5.xlsx`), so that I can confirm it produces correct results before trusting it for weekly use.

#### Acceptance Criteria

1. WHEN the Pipeline is run against the W14 xlsx file with `week_override='2026-W14'`, THE Pipeline SHALL complete all 7 stages without fatal errors
2. WHEN the simulation run completes, THE Pipeline SHALL have written rows to `ps.performance` for all 10 markets
3. WHEN the simulation run completes, THE Pipeline SHALL have written projection rows to `ps.forecasts` for all 10 markets
4. WHEN the simulation run completes, THE Pipeline SHALL have written OP2 registration targets to `ps.targets` for markets that have OP2 data in the W14 xlsx
5. WHEN the simulation run completes, THE PipelineResult SHALL report zero fatal errors in `stages_failed` (non-fatal warnings are acceptable)
