# Requirements Document

## Introduction

The Bayesian Prediction Engine adds a statistical inference layer on top of the DuckDB data layer (from the data-layer-overhaul spec), turning historical paid search metrics into forward-looking predictions with natural-language confidence levels. The engine serves Richard directly via chat/CLI, analyst agents for projections, the callout reviewer for predicted quality scores, the morning routine for proactive alerts, and an autonomy measurement system that tracks agentic workflow progression. Every prediction is logged, scored when outcomes arrive, and the engine self-calibrates over time.

## Glossary

- **Prediction_Engine**: The main entry point component that parses questions, routes to models, logs predictions, and returns formatted results
- **Bayesian_Core**: The statistical inference component that builds priors from historical data, updates posteriors with new evidence, and produces credible intervals
- **Model_Registry**: The component that manages one cached model per (market, metric) pair, with lazy creation and invalidation on new data
- **Calibrator**: The self-scoring component that tracks prediction accuracy by confidence tier and adjusts future confidence intervals
- **Formatter**: The component that translates PredictionResult objects into natural-language output (for humans) or structured dicts (for agents)
- **Autonomy_Tracker**: The component that categorizes task executions as fully_agentic, mixed, or human_only and tracks ratios over time
- **Prior**: A statistical belief about a metric's value before observing new evidence, computed from historical data
- **Posterior**: An updated statistical belief after incorporating new evidence into the prior
- **Credible_Interval**: A range within which the true value is expected to fall at a given confidence level
- **Calibration**: The process of checking whether X%-confidence predictions actually come true X% of the time, and adjusting future intervals accordingly
- **Confidence_Level**: A natural-language label (e.g., "likely", "uncertain") mapped from a numeric probability
- **Normal_Gamma_Model**: The conjugate Bayesian model used for updating beliefs about metric mean and variance simultaneously
- **DuckDB**: The embedded analytical database storing all structured data, accessed via query.py
- **Market**: One of the 10 paid search market codes: US, CA, UK, DE, FR, IT, ES, JP, AU, MX
- **Metric**: A measurable paid search value such as regs, spend, cpa, cvr, clicks, or cpc
- **Consumer**: The entity requesting a prediction — either 'human' (Richard, morning routine) or 'agent' (analyst, reviewer, dashboard)


## Requirements

### Requirement 1: Bayesian Prior Construction

**User Story:** As a prediction consumer, I want the engine to build statistical priors from historical data, so that predictions are grounded in actual market patterns rather than assumptions.

#### Acceptance Criteria

1. WHEN at least 3 weeks of historical data exist for a market and metric, THE Bayesian_Core SHALL compute the prior mean, variance, trend slope, and volatility from that historical data
2. WHEN fewer than 3 weeks of historical data exist for a market and metric, THE Bayesian_Core SHALL return an uninformative prior with variance greater than or equal to 1e6
3. WHEN 52 or more weeks of historical data exist, THE Bayesian_Core SHALL extract week-of-year seasonality adjustments from the data
4. THE Bayesian_Core SHALL compute trend via linear regression on the historical time series indices
5. THE Bayesian_Core SHALL compute volatility from the residuals of the trend fit

### Requirement 2: Posterior Updating

**User Story:** As a prediction consumer, I want the engine to update its beliefs when new evidence arrives, so that predictions improve over time as more data is ingested.

#### Acceptance Criteria

1. WHEN new evidence is provided to the Bayesian_Core, THE Bayesian_Core SHALL compute a posterior mean that lies between the prior mean and the evidence mean
2. WHEN new evidence is provided to the Bayesian_Core, THE Bayesian_Core SHALL compute a posterior variance that is less than or equal to the prior variance
3. WHEN a calibration factor is provided, THE Bayesian_Core SHALL scale the credible interval width by that calibration factor
4. WHEN no new evidence is provided, THE Bayesian_Core SHALL return a posterior identical to the prior with credible intervals computed from the prior volatility
5. THE Bayesian_Core SHALL blend recent trend (60% weight) with prior trend (40% weight) when at least 3 new evidence points are available

### Requirement 3: Prediction Request Handling

**User Story:** As Richard, I want to ask natural-language questions about market metrics and get predictions back, so that I can make informed decisions without writing SQL or understanding statistics.

#### Acceptance Criteria

1. WHEN a natural-language question is submitted, THE Prediction_Engine SHALL parse the question to extract market, metric, prediction type, and horizon
2. WHEN a question contains a valid market code (US, CA, UK, DE, FR, IT, ES, JP, AU, MX), THE Prediction_Engine SHALL identify that market from the question text
3. WHEN a question contains metric keywords (regs, spend, cpa, cvr, clicks, cpc), THE Prediction_Engine SHALL identify the target metric
4. THE Prediction_Engine SHALL classify each question into exactly one prediction type: point, direction, probability, time_to_target, or comparison
5. WHEN the same question and context are submitted multiple times, THE Prediction_Engine SHALL produce the same parsed result each time (deterministic parsing)
6. WHEN a question cannot be parsed into a known pattern, THE Prediction_Engine SHALL return a result with confidence_level 'uncertain' and suggest rephrasing or using the structured API

### Requirement 4: Prediction Logging and Tracking

**User Story:** As a system operator, I want every prediction logged to DuckDB, so that the engine can score predictions against actuals and track accuracy over time.

#### Acceptance Criteria

1. WHEN a prediction is generated, THE Prediction_Engine SHALL insert exactly one row into the predictions table with the question, market, metric, prediction type, point estimate, bounds, confidence level, confidence probability, direction, horizon, outcome week, reasoning, consumer, and status set to 'pending'
2. WHEN a prediction is logged, THE Prediction_Engine SHALL assign a unique integer id to the prediction and include it in the returned PredictionResult
3. THE Prediction_Engine SHALL store predictions with valid prediction_type values: 'point', 'direction', 'probability', 'time_to_target', or 'comparison'
4. THE Prediction_Engine SHALL store confidence_probability as a value between 0 and 1 inclusive

### Requirement 5: Prediction Scoring

**User Story:** As a system operator, I want predictions scored against actual outcomes when data arrives, so that the engine can measure and improve its accuracy.

#### Acceptance Criteria

1. WHEN actual data arrives for a predicted outcome week, THE Calibrator SHALL score each pending prediction for that week by computing error percentage, direction correctness, and interval coverage
2. WHEN a prediction is scored, THE Calibrator SHALL compute a composite score as: 0.4 × direction_score + 0.3 × interval_score + 0.3 × error_magnitude_score, where each component is between 0 and 1
3. WHEN a prediction is scored, THE Calibrator SHALL insert a row into prediction_outcomes and update the prediction status to 'scored'
4. WHEN score_prediction is called twice with the same prediction_id and actual_value, THE Calibrator SHALL produce the same PredictionScore and database state (idempotent upsert)
5. WHEN a prediction remains in 'pending' status for more than 2 weeks past its outcome_week, THE Prediction_Engine SHALL mark the prediction status as 'expired'


### Requirement 6: Self-Calibration

**User Story:** As a system operator, I want the engine to automatically detect when it is overconfident or underconfident and adjust future predictions accordingly, so that confidence levels become trustworthy over time.

#### Acceptance Criteria

1. WHEN compute_calibration is called, THE Calibrator SHALL compare the actual hit rate for each confidence tier against the expected rate across the most recent scored predictions (up to lookback count)
2. WHEN the actual hit rate for a confidence tier differs from the expected rate by more than 15 percentage points, THE Calibrator SHALL compute a confidence_adjustment factor that moves in the corrective direction (greater than 1.0 if overconfident, less than 1.0 if underconfident)
3. THE Calibrator SHALL clamp the confidence_adjustment factor to the range [0.5, 2.0]
4. WHEN no scored predictions exist, THE Calibrator SHALL return a neutral CalibrationReport with confidence_adjustment equal to 1.0
5. THE Calibrator SHALL exclude confidence tiers with fewer than 5 scored predictions from the calibration error computation

### Requirement 7: Confidence Language Mapping

**User Story:** As Richard, I want predictions expressed in natural language like "likely" or "uncertain" instead of numbers, so that I can quickly understand the engine's confidence without interpreting probabilities.

#### Acceptance Criteria

1. THE Calibrator SHALL map probabilities to confidence levels using these thresholds: greater than 0.85 maps to 'very_likely', 0.70-0.85 maps to 'likely', 0.55-0.70 maps to 'leaning_toward', 0.45-0.55 maps to 'uncertain', 0.30-0.45 maps to 'leaning_against', 0.15-0.30 maps to 'unlikely', less than 0.15 maps to 'very_unlikely'
2. WHEN two probabilities p1 and p2 satisfy p1 > p2, THE Calibrator SHALL map p1 to a confidence level equal to or higher than the level for p2 in the ordering: very_unlikely < unlikely < leaning_against < uncertain < leaning_toward < likely < very_likely

### Requirement 8: Natural Language Formatting

**User Story:** As Richard, I want prediction output that sounds like a human analyst wrote it, so that I can consume predictions without encountering statistical jargon.

#### Acceptance Criteria

1. WHEN a prediction is formatted for consumer type 'human', THE Formatter SHALL produce natural-language output that includes the prediction, reasoning based on recent data patterns, and the confidence level in plain English
2. WHEN a prediction is formatted for consumer type 'human', THE Formatter SHALL NOT include any of these statistical terms: "posterior", "prior", "conjugate", "credible interval", "p-value", "distribution", "variance", "standard deviation", "Bayesian", "Normal-Gamma", "hypothesis test", "significance level"
3. WHEN a prediction is formatted for consumer type 'agent', THE Formatter SHALL return a structured dict containing point_estimate, lower_bound, upper_bound, confidence_level, confidence_probability, direction, and reasoning
4. WHEN format_alert is called, THE Formatter SHALL produce a concise one-liner suitable for morning routine integration

### Requirement 9: Model Registry Management

**User Story:** As a system operator, I want models cached per market-metric pair and automatically invalidated when new data arrives, so that predictions use fresh data without manual intervention.

#### Acceptance Criteria

1. WHEN a model is requested for a market-metric pair that has not been built, THE Model_Registry SHALL create the model by querying historical data from DuckDB and building a prior via the Bayesian_Core
2. WHEN a model for a market-metric pair already exists in cache, THE Model_Registry SHALL return the cached model without rebuilding
3. WHEN invalidate is called for a specific market or metric, THE Model_Registry SHALL remove matching cached models so they are rebuilt on next request
4. THE Model_Registry SHALL NOT persist model state to disk — models are rebuilt from DuckDB data on demand to maintain portability

### Requirement 10: Autonomy Tracking

**User Story:** As Richard, I want to track what percentage of my marketing manager workflows are fully agentic vs. mixed vs. human-only, so that I can measure progress toward Level 5 (Agentic Orchestration).

#### Acceptance Criteria

1. WHEN a task is logged via the Autonomy_Tracker, THE Autonomy_Tracker SHALL insert a row into autonomy_tasks with workflow name, category ('fully_agentic', 'mixed', or 'human_only'), optional details, optional agent name, and optional quality score
2. WHEN get_ratios is called, THE Autonomy_Tracker SHALL compute the percentage of tasks in each category for the requested period, and the three percentages SHALL sum to 100% within floating-point tolerance of 0.1%
3. WHEN a weekly autonomy snapshot is computed, THE Autonomy_Tracker SHALL insert a row into autonomy_history with the workflow, total tasks, percentage breakdowns, average quality score, and five_levels_position (1-5)
4. WHEN predict_transition is called for a workflow, THE Autonomy_Tracker SHALL use the Bayesian_Core to predict when the workflow will reach the target autonomy category based on historical trajectory

### Requirement 11: DuckDB Schema Extension

**User Story:** As a system operator, I want the prediction engine's tables defined in init_db.py alongside existing tables, so that the schema is centrally managed and portable.

#### Acceptance Criteria

1. THE Prediction_Engine SHALL define five new tables in init_db.py: predictions, prediction_outcomes, calibration_log, autonomy_tasks, and autonomy_history
2. THE predictions table SHALL enforce: prediction_type IN ('point','direction','probability','time_to_target','comparison'), confidence_probability BETWEEN 0 AND 1, status IN ('pending','scored','expired','cancelled')
3. THE prediction_outcomes table SHALL enforce: score BETWEEN 0 AND 1, and prediction_id references predictions(id)
4. THE autonomy_tasks table SHALL enforce: category IN ('fully_agentic','mixed','human_only')
5. THE autonomy_history table SHALL enforce: five_levels_position BETWEEN 1 AND 5, with PRIMARY KEY (week, workflow)

### Requirement 12: Graceful Degradation

**User Story:** As a prediction consumer, I want the engine to handle edge cases gracefully instead of crashing, so that predictions are always available even with incomplete data.

#### Acceptance Criteria

1. WHEN a prediction is requested for a market-metric pair with zero historical data, THE Prediction_Engine SHALL return a PredictionResult with confidence_level 'uncertain' and reasoning that explains insufficient data
2. IF the DuckDB database file is missing or corrupted, THEN THE Prediction_Engine SHALL raise a PredictionEngineError with clear recovery instructions referencing init_db.py and ingest.py
3. WHEN no data has been ingested for 3 or more weeks, THE Prediction_Engine SHALL widen prediction intervals and include a staleness note in the reasoning
4. WHEN a cross-market comparison is requested and the reference markets have significantly different data availability, THE Prediction_Engine SHALL proceed with the prediction and note the asymmetry in the reasoning

### Requirement 13: CLI and Python API

**User Story:** As Richard, I want to access predictions via both a command-line tool and a Python API, so that I can get predictions interactively or integrate them into automated workflows.

#### Acceptance Criteria

1. THE Prediction_Engine SHALL expose a Python API via `predict(question, consumer, context)` and `predict_metric(market, metric, horizon_weeks, consumer)` methods
2. THE Prediction_Engine SHALL expose a CLI at `~/shared/tools/prediction/predict.py` that accepts a natural-language question as a positional argument
3. WHEN the CLI is invoked with `--market`, `--metric`, and `--horizon` flags, THE Prediction_Engine SHALL use the structured predict_metric path instead of question parsing
4. WHEN the CLI is invoked with `--calibrate`, THE Prediction_Engine SHALL run calibration and print the calibration report
5. WHEN the CLI is invoked with `--autonomy`, THE Prediction_Engine SHALL print the current autonomy ratios report
6. WHEN the CLI is invoked with `--log-task` and `--category`, THE Autonomy_Tracker SHALL log the task and confirm

### Requirement 14: Consumer Integration

**User Story:** As a system architect, I want the prediction engine to integrate cleanly with existing consumers (analyst agents, callout reviewer, morning routine, dashboard), so that predictions flow into existing workflows without disruption.

#### Acceptance Criteria

1. WHEN an analyst agent calls predict_metric with consumer='agent', THE Prediction_Engine SHALL return a PredictionResult dataclass with numeric fields suitable for programmatic use
2. WHEN the morning routine requests predictions, THE Formatter SHALL produce alert strings that are concise one-liners with the market, direction, and confidence
3. WHEN the dashboard queries predictions, THE Prediction_Engine SHALL ensure prediction data is accessible via standard SQL queries against the predictions table
4. WHEN the dashboard ingester completes a weekly ingestion, THE Prediction_Engine SHALL trigger calibration to score pending predictions against the newly arrived actuals
