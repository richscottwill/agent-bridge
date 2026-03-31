# Implementation Plan: Bayesian Prediction Engine

## Overview

Build a Bayesian inference layer on top of the DuckDB data layer (from data-layer-overhaul spec) that turns historical paid search metrics into forward-looking predictions with natural-language confidence levels. The engine reads from existing DuckDB tables via query.py, maintains its own state in 5 new DuckDB tables, and exposes a Python API + CLI. Includes a self-calibration loop and an autonomy measurement tracker.

**Dependency:** This spec depends on data-layer-overhaul. Tasks assume `query.py` already has `db()`, `db_write()`, `db_upsert()`, `market_trend()`, `market_week()` and that `init_db.py` manages the DuckDB schema. Do not duplicate that work.

## Tasks

- [x] 1. Extend DuckDB schema with prediction engine tables
  - [x] 1.1 Add 5 new tables to `init_db.py`: predictions, prediction_outcomes, calibration_log, autonomy_tasks, autonomy_history
    - Add CREATE TABLE IF NOT EXISTS statements with all columns per design data models
    - Add CHECK constraints: prediction_type IN ('point','direction','probability','time_to_target','comparison'), confidence_probability BETWEEN 0 AND 1, status IN ('pending','scored','expired','cancelled'), score BETWEEN 0 AND 1, category IN ('fully_agentic','mixed','human_only'), five_levels_position BETWEEN 1 AND 5
    - Add FOREIGN KEY on prediction_outcomes.prediction_id → predictions.id
    - Add PRIMARY KEY (week, workflow) on autonomy_history
    - Add auto-increment sequences for predictions, prediction_outcomes, calibration_log, autonomy_tasks
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

  - [x] 1.2 Write property test: database constraint enforcement (Property 13)
    - Attempt inserts with invalid prediction_type, score outside [0,1], invalid category, five_levels_position outside [1,5]
    - Verify database rejects each invalid insert
    - _Requirements: 11.2, 11.3, 11.4, 11.5_

- [x] 2. Implement core data types
  - [x] 2.1 Create `~/shared/tools/prediction/types.py` with dataclasses
    - PriorState, PosteriorState, PredictionResult, PredictionScore, CalibrationReport
    - All fields per design data models section
    - _Requirements: 1.1, 2.1, 5.2, 6.1_

  - [x] 2.2 Create `~/shared/tools/prediction/__init__.py`
    - Export PredictionEngine, AutonomyTracker, and key types
    - _Requirements: 13.1_

- [x] 3. Implement BayesianCore (inference engine)
  - [x] 3.1 Create `~/shared/tools/prediction/core.py` with BayesianCore class
    - `build_prior(historical, metric)` — compute mean, variance, trend (OLS), volatility (RMSE of residuals) from historical data; return uninformative prior (variance >= 1e6) when < 3 data points; extract seasonality when >= 52 weeks
    - `update_posterior(prior, new_evidence, calibration_factor)` — Normal-Gamma conjugate update; posterior mean between prior and evidence means; posterior variance <= prior variance; blend trends 60/40 when 3+ evidence points; scale credible intervals by calibration_factor
    - `point_estimate(posterior, horizon)` — project forward by horizon weeks using trend
    - `credible_interval(posterior, level)` — compute interval at given confidence level
    - `direction_probability(posterior, threshold)` — probability next value exceeds current + threshold
    - `time_to_target(posterior, target, max_weeks)` — estimated weeks to reach target with confidence
    - All functions are pure (no side effects, no DB access)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5_

  - [x] 3.2 Write property test: prior builds from data (Property 1)
    - Generate random positive float sequences of length 3-100
    - Verify mean equals arithmetic mean, trend_slope equals OLS slope, volatility equals RMSE of residuals
    - Generate sequences of length 0-2, verify variance >= 1e6
    - _Requirements: 1.1, 1.2, 1.4, 1.5_

  - [x] 3.3 Write property test: posterior convergence (Property 2)
    - Generate random PriorState and random non-empty evidence lists
    - Verify posterior mean lies between prior mean and evidence mean
    - Verify posterior variance <= prior variance
    - _Requirements: 2.1, 2.2_

  - [x] 3.4 Write property test: calibration factor scales credible intervals (Property 3)
    - Generate random PriorState, evidence, and two calibration factors k1 < k2
    - Verify interval width with k2 >= interval width with k1
    - _Requirements: 2.3_

- [x] 4. Implement question parser
  - [x] 4.1 Create `~/shared/tools/prediction/parser.py` with parse_question()
    - Extract market code from question text (10 valid codes)
    - Extract metric from keyword matching (regs, spend, cpa, cvr, clicks, cpc + aliases)
    - Classify prediction type: direction ("up or down"), time_to_target ("how many weeks"), probability ("probability"/"chance"), comparison ("if we launch"), default to point
    - Extract horizon from "next month" (4), "next N weeks" (N), default 1
    - Accept optional context dict to override parsed values
    - Return ParsedQuestion dataclass
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

  - [x] 4.2 Write property test: question parsing determinism (Property 4)
    - Generate random question strings and context dicts
    - Call parse_question twice with identical inputs, verify identical output
    - _Requirements: 3.5_

  - [x] 4.3 Write property test: question parsing extracts known entities (Property 5)
    - Generate question strings containing exactly one market code and one metric keyword
    - Verify parse_question extracts the correct market and metric
    - Verify prediction_type is one of the 5 valid types
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 5. Implement Calibrator (self-scoring and confidence mapping)
  - [x] 5.1 Create `~/shared/tools/prediction/calibrator.py` with Calibrator class
    - `score_prediction(prediction_id, actual_value)` — compute error_pct, direction_correct, within_interval; composite score = 0.4*dir + 0.3*interval + 0.3*error_mag; upsert to prediction_outcomes; update prediction status to 'scored'; idempotent on repeated calls
    - `compute_calibration(lookback)` — query recent scored predictions; group by confidence tier; compute hit_rate vs expected_rate per tier; exclude tiers with < 5 predictions; compute confidence_adjustment clamped to [0.5, 2.0]; return CalibrationReport
    - `get_confidence_adjustment()` — return current adjustment factor
    - `confidence_to_language(probability)` — map probability to 7-level natural language scale per Requirement 7.1 thresholds
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2_

  - [x] 5.2 Write property test: scoring produces valid composite score (Property 7)
    - Create test predictions in DB, score with random actual values
    - Verify composite score in [0, 1] and matches the 0.4/0.3/0.3 formula
    - Verify prediction_outcomes row exists and prediction status is 'scored'
    - _Requirements: 5.1, 5.2, 5.3_

  - [x] 5.3 Write property test: scoring idempotence (Property 8)
    - Score the same prediction twice with identical actual_value
    - Verify identical PredictionScore returned both times
    - Verify exactly one row in prediction_outcomes (no duplicates)
    - _Requirements: 5.4_

  - [x] 5.4 Write property test: calibration self-correction with bounds (Property 9)
    - Generate sets of scored predictions with known hit rates diverging from expected rates
    - Verify confidence_adjustment moves in corrective direction
    - Verify confidence_adjustment is in [0.5, 2.0]
    - _Requirements: 6.1, 6.2, 6.3_

  - [x] 5.5 Write property test: confidence language monotonicity (Property 10)
    - Generate random pairs of probabilities p1 > p2 in [0, 1]
    - Verify confidence_to_language(p1) >= confidence_to_language(p2) in the defined ordering
    - _Requirements: 7.1, 7.2_

- [x] 6. Implement Formatter (natural language output)
  - [x] 6.1 Create `~/shared/tools/prediction/formatter.py` with Formatter class
    - `format(result, consumer)` — 'human': natural language with reasoning, confidence in plain English, no jargon; 'agent': structured dict with all numeric fields
    - `format_alert(result)` — concise one-liner for morning routine
    - `format_autonomy_report(current, trajectory, predictions)` — natural language autonomy report
    - Use Richard's voice: direct, concise, data-grounded
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

  - [x] 6.2 Write property test: no statistical jargon in human output (Property 11)
    - Generate random PredictionResult objects, format with consumer='human'
    - Verify output contains no banned terms (posterior, prior, conjugate, credible interval, p-value, distribution, variance, standard deviation, Bayesian, Normal-Gamma, hypothesis test, significance level)
    - Verify output contains confidence level text and reasoning
    - _Requirements: 8.1, 8.2_

- [x] 7. Implement ModelRegistry (per-metric model management)
  - [x] 7.1 Create `~/shared/tools/prediction/models.py` with ModelRegistry class
    - `get_model(market, metric)` — lazy creation: query historical data, build prior via BayesianCore, cache result; return cached model on subsequent calls
    - `invalidate(market, metric)` — remove matching cached models
    - `list_models()` — list active models with last-updated timestamps
    - No disk persistence — models rebuild from DuckDB on demand
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [x] 8. Implement PredictionEngine (main entry point)
  - [x] 8.1 Create `~/shared/tools/prediction/engine.py` with PredictionEngine class
    - `__init__(db_path)` — initialize ModelRegistry, Calibrator, Formatter; load calibration state
    - `predict(question, consumer, context)` — parse question via parser.py; get/build model via ModelRegistry; run inference via BayesianCore; log prediction to DuckDB; format output via Formatter; return PredictionResult
    - `predict_metric(market, metric, horizon_weeks, consumer)` — structured prediction path bypassing question parsing
    - `calibrate(week)` — score pending predictions for the given week against actuals; recompute calibration; update internal calibration_factor
    - `get_calibration_report()` — return current CalibrationReport
    - Handle graceful degradation: zero data → uncertain result; unparseable question → uncertain with suggestion; stale data → wider intervals + staleness note; cross-market asymmetry → proceed with note
    - _Requirements: 3.1, 3.6, 4.1, 4.2, 4.3, 4.4, 12.1, 12.2, 12.3, 12.4, 14.1, 14.4_

  - [x] 8.2 Write property test: prediction logging completeness (Property 6)
    - Call predict() or predict_metric() with random valid inputs against a test DB with synthetic data
    - Verify exactly one new row in predictions table with matching prediction_id and status='pending'
    - _Requirements: 4.1, 4.2_

  - [x] 8.3 Add prediction expiration logic
    - On each calibrate() call, also mark predictions as 'expired' if outcome_week is > 2 weeks past and status is still 'pending'
    - _Requirements: 5.5_

- [x] 9. Implement AutonomyTracker
  - [x] 9.1 Create `~/shared/tools/prediction/autonomy.py` with AutonomyTracker class
    - `log_task(workflow, category, details, agent)` — insert row into autonomy_tasks; validate category is one of 'fully_agentic', 'mixed', 'human_only'; return task ID
    - `get_ratios(period)` — query autonomy_tasks for the period; compute pct_fully_agentic, pct_mixed, pct_human_only; return dict
    - `get_workflow_trajectory(workflow)` — return historical category distribution from autonomy_history
    - `predict_transition(workflow, target_category)` — use BayesianCore to predict when workflow reaches target; return PredictionResult
    - `five_levels_position()` — map current autonomy state to Richard's Five Levels framework (1-5)
    - `compute_autonomy_snapshot(week)` — compute and insert weekly snapshot into autonomy_history
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

  - [x] 9.2 Write property test: autonomy ratios sum to 100% (Property 12)
    - Generate random sets of autonomy tasks with random categories
    - Call get_ratios(), verify pct_fully_agentic + pct_mixed + pct_human_only == 100% (within 0.1% tolerance)
    - _Requirements: 10.2_

- [x] 10. Implement CLI entry point
  - [x] 10.1 Create `~/shared/tools/prediction/predict.py` CLI
    - Positional argument: natural-language question → calls engine.predict()
    - `--market`, `--metric`, `--horizon` flags → calls engine.predict_metric()
    - `--calibrate` flag → calls engine.calibrate() and prints report
    - `--autonomy` flag → prints current autonomy ratios
    - `--log-task WORKFLOW --category CATEGORY` → calls tracker.log_task()
    - Print formatted output to stdout
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6_

- [x] 11. Integration and end-to-end testing
  - [x] 11.1 Write integration test: full prediction → calibration cycle
    - Initialize test DuckDB with synthetic weekly_metrics (10 markets × 20 weeks)
    - Call predict() for each prediction type (point, direction, probability, time_to_target, comparison)
    - Verify predictions logged to predictions table
    - Insert "actual" values for predicted weeks
    - Call calibrate(), verify predictions scored and outcomes logged
    - Call compute_calibration(), verify calibration report is reasonable
    - Make new predictions, verify confidence_adjustment affects interval width
    - _Requirements: 4.1, 5.1, 5.3, 6.1, 14.4_

  - [x] 11.2 Write integration test: autonomy tracking cycle
    - Log tasks across multiple workflows with varying categories
    - Compute ratios, verify sums
    - Compute weekly snapshot, verify autonomy_history row
    - Call predict_transition, verify PredictionResult returned
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

  - [x] 11.3 Write integration test: CLI produces same results as Python API
    - Run predict.py with a question, capture stdout
    - Run engine.predict() with same question, compare formatted output
    - _Requirements: 13.1, 13.2_

- [ ] 12. Blind architecture evaluation
  - [ ] 12.1 Snapshot before: run analyst agents WITHOUT prediction engine on AU, MX, and US
    - Run the current callout pipeline for AU, MX, and US for the latest available week
    - Save the analysis briefs and callout drafts as "before" artifacts
    - These represent the baseline output quality without Bayesian predictions
    - _Requirements: (architecture-eval-protocol)_

  - [ ] 12.2 Run after: run analyst agents WITH prediction engine on AU, MX, and US
    - Enable the prediction engine integration in the analyst agent prompt
    - Run the callout pipeline for the same markets and week
    - Save the analysis briefs and callout drafts as "after" artifacts
    - _Requirements: (architecture-eval-protocol)_

  - [ ] 12.3 Spawn blind evaluator and score
    - Create a fresh evaluation prompt that receives only before/after outputs and input data
    - Evaluator has NO knowledge of the prediction engine — it just sees two sets of analysis briefs and callouts
    - Score 5 evaluation questions: factual equivalence, quality comparison, data contradiction, gap detection, decision utility
    - Each question scored as PASS, REGRESS, or NEUTRAL
    - If 2+ REGRESS: REJECTED — disable prediction engine integration and investigate
    - Log result to `agent_observations` via `log_architecture_eval()`
    - _Requirements: (architecture-eval-protocol)_
