# Implementation Plan: Paid Search Daily Audit

## Overview

Build an automated daily audit pipeline in Python that pulls Google Ads and Adobe Analytics data across multiple MCCs, normalizes and stores it in SQLite, runs budget pacing / anomaly detection / KPI comparison engines, and generates prioritized reports in markdown, email, and JSON formats. Tasks are ordered to get a working end-to-end flow first (data pull → store → basic report), then layer in analysis engines.

## Tasks

- [x] 1. Project scaffolding and core data models
  - [x] 1.1 Create project structure and configuration
    - Create `paid_search_audit/` package with `__init__.py`
    - Create `config.py` with dataclasses for `MCCConfig`, `AccountMapping`, `MarketConfig`, `OP2Targets`, `AnomalyConfig`
    - Create `models.py` with dataclasses for `NormalizedMetrics`, `AnomalyFinding`, `PacingResult`, `MultiHorizonProjection`, `PeriodProjection`, `AuditReport`, `MarketSection`, `ActionItem`, `AuditSummary`, `WoWComparison`
    - Create a sample `config.json` with AU and MX market definitions (placeholder account IDs and MCC IDs)
    - Install dependencies: `google-ads`, `requests`, `pandas`, `sqlite3` (stdlib)
    - _Requirements: 1.1, 1.2, 1.8, 3.1_

  - [x] 1.2 Write property tests for data model validation
    - **Property 5: No Division by Zero** — CPA/CTR/CVR dataclass constructors return None when denominators are zero
    - **Validates: Requirements 12.1, 12.2, 12.3**

- [x] 2. SQLite data store and historical data layer
  - [x] 2.1 Implement the Data Store module
    - Create `data_store.py` with a `DataStore` class wrapping SQLite
    - Schema: `daily_metrics` table indexed on `(market, date)` storing all NormalizedMetrics fields
    - Implement `store_metrics(metrics: list[NormalizedMetrics], audit_date: date)`
    - Implement `load_historical(market: str, days: int, before_date: date) -> list[NormalizedMetrics]` — returns data strictly before `before_date`
    - Implement `load_period_actuals(market: str, start_date: date, end_date: date, metric: str) -> Decimal`
    - Implement DB initialization and migration
    - _Requirements: 4.1, 4.2, 4.3, 14.2, 14.3_

  - [x] 2.2 Write property tests for data store temporal correctness
    - **Property 8: Temporal Correctness** — `load_historical` never returns data points with date >= audit_date
    - **Validates: Requirements 14.2, 14.3**

  - [x] 2.3 Write unit tests for data store
    - Test store and retrieve round-trip
    - Test 30-day retrieval window
    - Test `load_period_actuals` aggregation across date ranges
    - _Requirements: 4.1, 4.2, 4.3_

- [x] 3. Checkpoint — Validate data layer
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Google Ads data fetcher with multi-MCC support
  - [x] 4.1 Implement the Google Ads Data Fetcher
    - Create `google_ads_fetcher.py` with `GoogleAdsDataFetcher` class
    - Implement `resolve_mcc_credentials(mcc: MCCConfig) -> AuthToken` using google-ads client library OAuth flow
    - Implement `validate_account_access(mcc: MCCConfig, account_id: str) -> bool`
    - Implement `fetch_account_campaigns(mcc: MCCConfig, account_id: str, date_range) -> list[CampaignData]` using GAQL queries for spend, impressions, clicks, conversions, CPA, ROAS at campaign and ad-group level
    - Implement `fetch_market_data(market: MarketConfig, date_range) -> MarketGoogleData` that groups accounts by MCC, authenticates per-MCC, iterates accounts, handles per-account failures, and tags results with `account_id` and `mcc_id`
    - Implement `get_account_budget_info(mcc: MCCConfig, account_id: str) -> list[BudgetInfo]`
    - Handle API rate limits per-MCC independently (MCC-scoped, not account-scoped)
    - Record individual account failures and continue fetching remaining accounts
    - Mark all accounts under a failed MCC as failed and continue with other MCCs
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 11.1, 11.2, 11.3, 11.4_

  - [x] 4.2 Write property tests for multi-MCC fetcher
    - **Property 11: Cross-MCC Account Completeness** — every active account is either in `account_results` or `failed_accounts`
    - **Validates: Requirements 1.6, 1.7, 11.3**
    - **Property 14: Partial MCC Failure Isolation** — auth failure on one MCC does not prevent fetching from other MCCs
    - **Validates: Requirements 1.7, 11.4**

- [x] 5. Adobe Analytics data fetcher
  - [x] 5.1 Implement the Adobe Analytics Data Fetcher
    - Create `adobe_fetcher.py` with `AdobeAnalyticsDataFetcher` class
    - Implement `fetch_traffic_data`, `fetch_conversion_data`, `fetch_registration_data`
    - Segment data by market and campaign type (Brand vs Non-Brand)
    - Handle API failures gracefully — return empty data with error flag so orchestrator can proceed with Google Ads only
    - _Requirements: 2.1, 2.2, 2.3_

- [x] 6. Data normalizer and cross-account aggregation
  - [x] 6.1 Implement the Data Normalizer
    - Create `data_normalizer.py` with `DataNormalizer` class
    - Implement `normalize_market_google_data(raw: MarketGoogleData) -> list[NormalizedMetrics]` preserving `account_id` and `mcc_id`
    - Implement `aggregate_across_accounts(metrics: list[NormalizedMetrics]) -> list[NormalizedMetrics]` — sum spend/clicks/impressions/conversions, recompute CPA/CTR/CVR
    - Implement `detect_duplicate_campaigns(metrics: list[NormalizedMetrics]) -> list[DuplicateWarning]`
    - Implement `merge_sources(google: list, adobe: list) -> list[NormalizedMetrics]` joining on campaign/market
    - Implement `apply_currency_conversion(metrics, target_currency)` for AUD, MXN, USD, EUR, JPY, CAD, GBP → USD
    - Handle zero denominators: CPA=None when conversions=0, CTR=None when impressions=0, CVR=None when clicks=0
    - Flag data quality issues (missing fields, mismatched totals, partial account failures)
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 12.1, 12.2, 12.3_

  - [x] 6.2 Write property tests for normalizer
    - **Property 12: No Cross-MCC Double Counting** — each campaign attributed to exactly one (account_id, mcc_id) pair in aggregated output
    - **Validates: Requirements 3.2, 3.3**
    - **Property 5: No Division by Zero** — ratio metrics return None when denominators are zero
    - **Validates: Requirements 12.1, 12.2, 12.3**

- [x] 7. Audit orchestrator — end-to-end pipeline (minimal)
  - [x] 7.1 Implement the Audit Orchestrator core loop
    - Create `orchestrator.py` with `AuditOrchestrator` class
    - Implement `run_audit(config: AuditConfig, date: date) -> AuditReport` following the main orchestration algorithm
    - For each market: fetch Google Ads data (grouped by MCC), fetch Adobe data, normalize, aggregate, store, load historical
    - Handle partial failures: skip markets where all accounts fail, produce partial audits where some accounts fail
    - Collect `data_quality_notes` for all failures, partial data, and warnings
    - Wire together fetchers → normalizer → data store (analysis engines stubbed for now)
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 14.1_

  - [x] 7.2 Write property tests for orchestrator graceful degradation
    - **Property 1: Completeness** — every market with successful API calls has a MarketSection in the report
    - **Validates: Requirements 11.1, 11.2**
    - **Property 7: Graceful Degradation** — API failure for market A does not prevent market B from appearing in report
    - **Validates: Requirements 11.1, 11.4**

- [x] 8. Checkpoint — Validate end-to-end data pipeline
  - Ensure all tests pass, ask the user if questions arise. At this point the pipeline should be able to pull data from Google Ads/Adobe, normalize it, and store it in SQLite.

- [x] 9. Budget pacing engine
  - [x] 9.1 Implement the Budget Pacing Engine
    - Create `budget_pacing.py` with `BudgetPacingEngine` class
    - Implement `calculate_pacing(market, actuals, budget) -> PacingResult` with pacing_pct = (actual / prorated_target) × 100
    - Classify: ON_TRACK (85-110%), UNDERSPEND (<85%), OVERSPEND (>110%)
    - Implement `project_end_of_period` using trailing 7-day average daily spend as run rate
    - Handle projected CPA = None when projected_regs = 0
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 12.5_

  - [x] 9.2 Write property tests for budget pacing
    - **Property 2: Pacing Consistency** — pacing_pct = (actual_spend / prorated_target) × 100
    - **Validates: Requirements 5.1**

- [x] 10. Multi-horizon projection engine
  - [x] 10.1 Implement multi-horizon projections
    - Add `project_multi_horizon(market, metrics, targets, audit_date) -> MultiHorizonProjection` to `BudgetPacingEngine`
    - Compute trailing 7-day run rates for spend and registrations
    - Build monthly, quarterly, yearly `PeriodProjection` using `build_period_projection` helper
    - For QTD/YTD: load prior month actuals from DataStore when quarter/year started before current month
    - Compute vs OP2 percentages: ((projected - target) / target) × 100
    - Compute pacing percentages: (actual / prorated_target) × 100
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_

  - [x] 10.2 Write property tests for multi-horizon projections
    - **Property 15: Projection Run Rate Consistency** — all three horizons use the same trailing 7-day daily run rate
    - **Validates: Requirements 6.2**
    - **Property 16: Projection Arithmetic Integrity** — projected_spend = actual_spend + (run_rate × days_remaining)
    - **Validates: Requirements 6.3**
    - **Property 17: Period Day Accounting** — days_elapsed + days_remaining = days_total for all periods
    - **Validates: Requirements 6.7**

- [x] 11. Anomaly detection engine
  - [x] 11.1 Implement the Anomaly Detector
    - Create `anomaly_detector.py` with `AnomalyDetector` class
    - Implement `compute_baseline(historical, window) -> BaselineStats` for 7-day and 30-day rolling windows
    - Implement `get_day_of_week_factor(historical_series, target_dow) -> float` from at least 14 days of data
    - Implement `detect_anomalies(current, historical, config) -> list[AnomalyFinding]`
    - Compute z-score, apply day-of-week adjustment, classify severity (CRITICAL >= 3.0, WARNING >= 2.0, INFO >= 1.5)
    - Elevate severity for CPA increases and registration drops
    - Skip markets with < 7 days of history
    - Use higher threshold (min_z_score + 0.5) for campaign-type level (Brand vs Non-Brand)
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9_

  - [x] 11.2 Write property tests for anomaly detector
    - **Property 3: Anomaly Threshold Guarantee** — no finding with abs(z_score) < config.min_z_score
    - **Validates: Requirements 7.3**

- [x] 12. KPI comparator
  - [x] 12.1 Implement the KPI Comparator
    - Create `kpi_comparator.py` with `KPIComparator` class
    - Implement `compare_to_targets(actuals, targets) -> list[KPIFinding]`
    - Implement `compute_goal_progress(actuals, target, days_elapsed, days_total) -> GoalProgress`
    - Flag goals pacing below 90% of prorated target as at-risk
    - Include Kingpin Goal progress (MX registrations)
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [x] 13. Finding prioritization and week-over-week comparison
  - [x] 13.1 Implement priority ranking and WoW comparison
    - Create `priority_ranker.py` with `rank_findings(findings) -> list[PrioritizedFinding]`
    - Scoring: severity (CRITICAL=100, WARNING=50, INFO=10) + market weight (AU/MX=20, team-wide=5) + category weight (BUDGET=30, GOAL=25, PERFORMANCE=15) + worsening trend bonus (+15)
    - Sort descending by score, assign sequential ranks starting from 1
    - Implement `compute_wow(current_metrics, historical_metrics) -> WoWComparison`
    - Compare audit date metrics vs same day prior week for spend, clicks, conversions, CPA, CTR
    - Return None for all WoW changes when prior week data is missing
    - Handle zero/None prior period values by returning None for percentage change
    - _Requirements: 9.1, 9.2, 9.3, 13.1, 13.2, 13.3, 12.4_

  - [x] 13.2 Write property tests for priority ranking
    - **Property 4: Priority Ordering** — action_items[i].score >= action_items[j].score for all i < j
    - **Validates: Requirements 9.2**

- [x] 14. Checkpoint — Validate all analysis engines
  - Ensure all tests pass, ask the user if questions arise. At this point all analysis engines should be functional.

- [x] 15. Wire analysis engines into orchestrator
  - [x] 15.1 Complete orchestrator integration
    - Wire budget pacing, multi-horizon projections, anomaly detection, KPI comparator, priority ranker, and WoW comparison into the orchestrator's `run_audit` loop
    - Build `MarketSection` for each market with pacing, projections, anomalies, kpi_status, top_campaigns, wow_changes
    - Implement `generate_action_items(prioritized_findings) -> list[ActionItem]` — max 10 items, urgency mapping (CRITICAL/budget→TODAY, WARNING→THIS_WEEK, INFO→MONITOR), concrete suggested actions
    - Implement `compute_summary(market_sections) -> AuditSummary`
    - _Requirements: 9.1, 9.2, 9.3, 10.5, 10.6, 10.7, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_

  - [x] 15.2 Write property tests for action item generation
    - **Property 9: Action Item Bound** — report contains at most 10 action items
    - **Validates: Requirements 10.5**

- [x] 16. Report generator
  - [x] 16.1 Implement the Report Generator
    - Create `report_generator.py` with `ReportGenerator` class
    - Implement `generate_markdown(findings, date) -> str` — grouped by market, includes pacing, multi-horizon projections in WBR callout style, anomalies, KPI status, top campaigns, WoW changes
    - Implement `generate_email_brief(findings, date) -> str` — scannable morning routine format
    - Implement `generate_json(findings, date) -> dict` — structured JSON for programmatic consumption
    - Format multi-horizon projections as WBR callout lines (e.g., "[Month] is projected to end at $X spend and X registrations vs. OP2: +/-% spend, +/-% registrations")
    - Limit action items to max 10 per report
    - Assign urgency: TODAY for CRITICAL and all budget findings, THIS_WEEK for WARNING, MONITOR for INFO
    - Include concrete suggested action for each item
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7_

- [x] 17. CLI entry point and scheduling hook
  - [x] 17.1 Create CLI entry point
    - Create `cli.py` with `main()` function using argparse
    - Accept `--config`, `--date`, `--markets` (optional filter), `--output-dir` arguments
    - Load config, run audit, write markdown/JSON reports to output directory
    - Print summary to stdout
    - Wire into morning routine hook by writing report to `~/shared/audit-reports/{date}.md`
    - _Requirements: 10.1, 10.2, 10.3_

- [x] 18. Final checkpoint — End-to-end validation
  - Ensure all tests pass, ask the user if questions arise. The full pipeline should be runnable via CLI: pull data → normalize → store → analyze → generate reports.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- Implementation language: Python (google-ads client library, pandas, sqlite3, built-in JSON)
- Tasks are ordered to get a working data pipeline first (tasks 1-8), then layer analysis engines (9-14), then wire everything together (15-18)
