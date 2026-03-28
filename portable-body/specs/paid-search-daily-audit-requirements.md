# Requirements Document

## Introduction

The Paid Search Daily Audit system automates daily health checks across Amazon Business paid search campaigns spanning AU, MX, and team-wide markets (US, EU5, JP, CA). The system pulls data from Google Ads (across multiple MCCs with independent credentials) and Adobe Analytics, detects performance anomalies, compares actuals against OP2 targets, projects end-of-period outcomes at monthly/quarterly/yearly horizons, and generates prioritized audit reports. It replaces a 45-60 minute manual daily check with a 5-minute scan of an exception-based report.

## Glossary

- **Audit_Orchestrator**: The central coordination component that triggers data fetches, runs analysis engines, and produces the final audit report
- **Google_Ads_Fetcher**: The component responsible for pulling campaign and ad-group metrics from Google Ads API across multiple MCCs
- **Adobe_Fetcher**: The component responsible for pulling traffic and conversion data from Adobe Analytics
- **Data_Normalizer**: The component that transforms raw multi-source data into a unified schema and aggregates across accounts
- **Budget_Pacing_Engine**: The component that calculates budget utilization and projects end-of-period spend against targets
- **Anomaly_Detector**: The component that identifies statistically significant deviations in key metrics using rolling baselines
- **KPI_Comparator**: The component that compares current performance against OP2 plan targets and Kingpin Goal thresholds
- **Report_Generator**: The component that produces the final audit report in markdown, email, and JSON formats
- **MCC**: Manager Client Center — a Google Ads account that manages multiple child advertising accounts, each with independent OAuth credentials
- **OP2_Targets**: Operating Plan 2 targets — the approved budget and performance targets per market for spend, registrations, and CPA
- **Kingpin_Goal**: A high-visibility organizational goal tracked at the leadership level (e.g., MX registrations)
- **Run_Rate**: The trailing 7-day average daily value used to project end-of-period outcomes
- **Z_Score**: The number of standard deviations a current value is from the rolling baseline mean
- **Pacing_Percentage**: The ratio of actual spend to prorated target spend, expressed as a percentage
- **MarketCode**: One of "AU", "MX", "US", "EU5", "JP", "CA"
- **NormalizedMetrics**: The unified data schema containing date, market, campaign type, spend, clicks, impressions, conversions, and derived ratios
- **PeriodProjection**: A projection structure containing actuals-to-date, projected end-of-period values, and comparison against OP2 targets for a given time horizon
- **Data_Store**: The local SQLite database that persists historical metrics for baseline computation and trend analysis

## Requirements

### Requirement 1: Multi-MCC Google Ads Data Fetching

**User Story:** As a paid search manager, I want the system to pull campaign data from Google Ads accounts spread across multiple MCCs with independent credentials, so that I get a complete view of each market's performance regardless of account topology.

#### Acceptance Criteria

1. WHEN the Audit_Orchestrator triggers a market audit, THE Google_Ads_Fetcher SHALL authenticate with each MCC independently using its own OAuth credentials
2. WHEN fetching data for a market, THE Google_Ads_Fetcher SHALL group accounts by MCC to minimize authentication overhead
3. WHEN fetching account data, THE Google_Ads_Fetcher SHALL retrieve spend, impressions, clicks, conversions, CPA, and ROAS at campaign and ad-group level
4. WHEN fetching account data, THE Google_Ads_Fetcher SHALL retrieve budget allocation and daily spend caps per account
5. WHEN the Google_Ads_Fetcher encounters API rate limits, THE Google_Ads_Fetcher SHALL respect per-MCC rate limits independently so that throttling on one MCC does not delay fetches from another MCC
6. WHEN an individual account fetch fails, THE Google_Ads_Fetcher SHALL record the failure and continue fetching remaining accounts in the same market
7. WHEN MCC authentication fails, THE Google_Ads_Fetcher SHALL mark all accounts under that MCC as failed and continue fetching from other MCCs
8. WHEN returning data, THE Google_Ads_Fetcher SHALL tag each result with account_id and mcc_id for traceability
9. WHEN the Audit_Orchestrator starts a market audit, THE Google_Ads_Fetcher SHALL validate that each account is accessible under its configured MCC before fetching data


### Requirement 2: Adobe Analytics Data Fetching

**User Story:** As a paid search manager, I want the system to pull traffic and conversion data from Adobe Analytics, so that I can cross-reference Google Ads performance with site-level registration and traffic metrics.

#### Acceptance Criteria

1. WHEN the Audit_Orchestrator triggers a market audit, THE Adobe_Fetcher SHALL pull registration counts, traffic volume, and conversion rates from Adobe Analytics
2. WHEN fetching Adobe data, THE Adobe_Fetcher SHALL segment data by market and campaign type (Brand vs Non-Brand)
3. IF the Adobe Analytics API is unreachable or returns incomplete data, THEN THE Audit_Orchestrator SHALL proceed with Google Ads data only and flag Adobe-dependent metrics as unavailable

### Requirement 3: Data Normalization and Cross-Account Aggregation

**User Story:** As a paid search manager, I want raw data from multiple Google Ads accounts and Adobe Analytics merged into a single unified view per market, so that I can see market-level performance without manually combining data from different accounts and MCCs.

#### Acceptance Criteria

1. WHEN normalizing Google Ads data, THE Data_Normalizer SHALL map raw fields to the NormalizedMetrics schema while preserving account_id and mcc_id as metadata
2. WHEN aggregating across accounts within a market, THE Data_Normalizer SHALL sum spend, clicks, impressions, and conversions, and recompute derived ratios (CPA, CTR, conversion rate)
3. WHEN the same campaign name exists in multiple accounts within a market, THE Data_Normalizer SHALL detect the potential duplicate and generate a warning
4. WHEN merging Google Ads and Adobe data, THE Data_Normalizer SHALL join data on campaign and market dimensions
5. WHEN metrics involve different currencies, THE Data_Normalizer SHALL apply currency conversion to a common currency (USD) for cross-market comparison
6. IF data quality issues are detected (missing fields, mismatched totals, partial account failures), THEN THE Data_Normalizer SHALL flag the issues in data quality notes

### Requirement 4: Historical Data Storage

**User Story:** As a paid search manager, I want daily metrics stored locally so that the system can compute rolling baselines and detect trends over time without re-fetching from APIs.

#### Acceptance Criteria

1. WHEN a market audit completes data normalization, THE Data_Store SHALL persist the merged metrics for the audit date
2. WHEN the Anomaly_Detector or Budget_Pacing_Engine requests historical data, THE Data_Store SHALL return metrics indexed by market and date
3. THE Data_Store SHALL support retrieval of at least 30 days of historical data per market for baseline computation

### Requirement 5: Budget Pacing

**User Story:** As a paid search manager, I want to know whether each market is on track to hit its monthly spend target, so that I can intervene early on underspend or overspend situations.

#### Acceptance Criteria

1. WHEN calculating budget pacing, THE Budget_Pacing_Engine SHALL compute pacing percentage as actual spend divided by prorated target spend (target × days_elapsed / days_in_month) × 100
2. WHEN pacing percentage is between 85% and 110% inclusive, THE Budget_Pacing_Engine SHALL classify the market as ON_TRACK
3. WHEN pacing percentage is below 85%, THE Budget_Pacing_Engine SHALL classify the market as UNDERSPEND
4. WHEN pacing percentage is above 110%, THE Budget_Pacing_Engine SHALL classify the market as OVERSPEND
5. WHEN projecting end-of-month spend, THE Budget_Pacing_Engine SHALL use the trailing 7-day average daily spend as the run rate


### Requirement 6: Multi-Horizon Projections

**User Story:** As a paid search manager, I want monthly, quarterly, and yearly projections using the same trailing 7-day run rate methodology used in WBR callouts, so that I can assess performance trajectory at every planning horizon.

#### Acceptance Criteria

1. WHEN projecting end-of-period outcomes, THE Budget_Pacing_Engine SHALL compute projections for monthly, quarterly, and yearly horizons
2. THE Budget_Pacing_Engine SHALL use the same trailing 7-day daily run rate for all three projection horizons
3. WHEN computing projected spend, THE Budget_Pacing_Engine SHALL calculate projected_spend as actual_spend + (daily_spend_run_rate × days_remaining)
4. WHEN computing projected registrations, THE Budget_Pacing_Engine SHALL calculate projected_regs as actual_regs + (daily_regs_run_rate × days_remaining)
5. WHEN computing projected CPA, THE Budget_Pacing_Engine SHALL calculate projected_cpa as projected_spend / projected_regs when projected_regs is greater than zero
6. WHEN computing vs OP2 percentages, THE Budget_Pacing_Engine SHALL calculate ((projected - target) / target) × 100 for both spend and registrations
7. THE Budget_Pacing_Engine SHALL ensure days_elapsed + days_remaining equals days_total for every period projection
8. WHEN computing quarterly projections and the quarter started before the current month, THE Budget_Pacing_Engine SHALL include actuals from prior months loaded from the Data_Store

### Requirement 7: Anomaly Detection

**User Story:** As a paid search manager, I want the system to automatically detect statistically significant deviations in key metrics, so that I am alerted to performance changes that need investigation.

#### Acceptance Criteria

1. WHEN detecting anomalies, THE Anomaly_Detector SHALL compute rolling 7-day and 30-day baselines for each monitored metric (CPA, Registrations, Spend, CTR, ConversionRate, Clicks)
2. WHEN a metric's z-score (adjusted for day-of-week) exceeds the configured minimum threshold, THE Anomaly_Detector SHALL generate an AnomalyFinding
3. THE Anomaly_Detector SHALL never include a finding with abs(z_score) below the configured min_z_score threshold
4. WHEN classifying severity, THE Anomaly_Detector SHALL assign CRITICAL when abs(z_score) >= critical_threshold (default 3.0), WARNING when abs(z_score) >= warning_threshold (default 2.0), and INFO when abs(z_score) >= min_z_score (default 1.5)
5. WHEN classifying CPA increases, THE Anomaly_Detector SHALL elevate severity by one level compared to other metrics
6. WHEN classifying registration drops, THE Anomaly_Detector SHALL elevate severity by one level compared to other metrics
7. WHEN adjusting for day-of-week patterns, THE Anomaly_Detector SHALL compute a day-of-week factor from at least 14 days of historical data and divide the raw z-score by this factor
8. WHEN a market has fewer than 7 days of historical data, THE Anomaly_Detector SHALL skip anomaly detection for that market
9. WHEN detecting anomalies at campaign-type level (Brand vs Non-Brand), THE Anomaly_Detector SHALL use a higher z-score threshold (min_z_score + 0.5) to reduce noise

### Requirement 8: KPI Comparison Against OP2 Targets

**User Story:** As a paid search manager, I want current performance compared against OP2 plan targets, so that I can see which markets and goals are at risk of missing plan.

#### Acceptance Criteria

1. WHEN comparing KPIs, THE KPI_Comparator SHALL load OP2 targets per market for registrations, CPA, and spend
2. WHEN computing goal progress, THE KPI_Comparator SHALL compare MTD actuals against prorated monthly targets
3. WHEN a goal is pacing below 90% of its prorated target, THE KPI_Comparator SHALL flag the goal as at-risk
4. WHEN tracking Kingpin Goals (e.g., MX registrations), THE KPI_Comparator SHALL include Kingpin Goal progress in the KPI findings


### Requirement 9: Finding Prioritization

**User Story:** As a paid search manager, I want findings ranked by priority so that I focus on the most impactful issues first during my morning scan.

#### Acceptance Criteria

1. WHEN ranking findings, THE Audit_Orchestrator SHALL assign a priority score based on severity (CRITICAL=100, WARNING=50, INFO=10), market weight (AU/MX hands-on=20, team-wide=5), category weight (BUDGET=30, GOAL=25, PERFORMANCE=15), and worsening trend bonus (+15)
2. WHEN findings are ranked, THE Audit_Orchestrator SHALL sort findings in descending order by priority score
3. WHEN assigning priority ranks, THE Audit_Orchestrator SHALL assign sequential ranks starting from 1 (highest priority)

### Requirement 10: Report Generation

**User Story:** As a paid search manager, I want the audit output in markdown, email, and JSON formats, so that I can scan it in my morning routine, receive it via email, and feed it into other tools.

#### Acceptance Criteria

1. WHEN generating a report, THE Report_Generator SHALL produce a markdown report grouped by market with pacing, projections, anomalies, KPI status, top campaigns, and week-over-week changes
2. WHEN generating a report, THE Report_Generator SHALL produce an email-ready brief for the morning routine
3. WHEN generating a report, THE Report_Generator SHALL produce a JSON output for programmatic consumption
4. WHEN generating market sections, THE Report_Generator SHALL include multi-horizon projections formatted in WBR callout style (e.g., "[Month] is projected to end at $X spend and X registrations vs. OP2: +/-% spend, +/-% registrations")
5. THE Report_Generator SHALL limit action items to at most 10 per report to prevent information overload
6. WHEN generating action items, THE Report_Generator SHALL assign urgency as TODAY for CRITICAL findings and all budget-related findings, THIS_WEEK for WARNING findings, and MONITOR for INFO findings
7. WHEN generating action items, THE Report_Generator SHALL include a concrete suggested action for each item

### Requirement 11: Graceful Degradation

**User Story:** As a paid search manager, I want the audit to produce results for every market it can reach, even when some APIs or accounts fail, so that a single failure does not block my entire morning audit.

#### Acceptance Criteria

1. WHEN an API failure occurs for one market, THE Audit_Orchestrator SHALL continue auditing all other configured markets
2. WHEN all accounts in a market fail, THE Audit_Orchestrator SHALL skip that market and record the failure in data quality notes
3. WHEN some but not all accounts in a market fail, THE Audit_Orchestrator SHALL produce a partial audit for that market with a PARTIAL_DATA flag and list which accounts are missing
4. WHEN MCC authentication fails for one MCC but other MCCs for the same market succeed, THE Audit_Orchestrator SHALL include data from the successful MCCs and note the failed MCC in data quality notes
5. IF currency conversion rates are unavailable, THEN THE Audit_Orchestrator SHALL use the last known exchange rate with a staleness warning, or a hardcoded fallback rate if no rate has ever been fetched
6. WHEN the most recent available data is older than the audit date, THE Audit_Orchestrator SHALL run the audit on the most recent data and include a DATA_LAG warning with the number of hours/days of lag

### Requirement 12: Ratio Metric Safety

**User Story:** As a paid search manager, I want the system to handle zero-value denominators gracefully, so that division-by-zero errors never crash the audit or produce misleading metrics.

#### Acceptance Criteria

1. WHEN computing CPA and conversions equals zero, THE Data_Normalizer SHALL return NULL for CPA
2. WHEN computing CTR and impressions equals zero, THE Data_Normalizer SHALL return NULL for CTR
3. WHEN computing conversion rate and clicks equals zero, THE Data_Normalizer SHALL return NULL for conversion rate
4. WHEN computing week-over-week percentage change and the prior period value is zero or NULL, THE Audit_Orchestrator SHALL return NULL for the percentage change
5. WHEN computing projected CPA and projected registrations equals zero, THE Budget_Pacing_Engine SHALL return NULL for projected CPA

### Requirement 13: Week-over-Week Comparison

**User Story:** As a paid search manager, I want to see how today's metrics compare to the same day last week, so that I can quickly spot directional changes in performance.

#### Acceptance Criteria

1. WHEN computing week-over-week comparison, THE Audit_Orchestrator SHALL compare the audit date's aggregated metrics against the same day of the prior week
2. WHEN computing WoW changes, THE Audit_Orchestrator SHALL calculate percentage change for spend, clicks, conversions, CPA, and CTR
3. WHEN prior week data is missing for the comparison day, THE Audit_Orchestrator SHALL return NULL for all WoW percentage changes

### Requirement 14: Audit Idempotency and Temporal Correctness

**User Story:** As a paid search manager, I want the audit to produce consistent results when re-run for the same date, and I want baselines computed only from data before the audit date, so that results are reproducible and unbiased.

#### Acceptance Criteria

1. WHEN the same audit is run multiple times for the same date with unchanged underlying data, THE Audit_Orchestrator SHALL produce identical results
2. WHEN computing historical baselines, THE Anomaly_Detector SHALL use only data points with dates strictly before the audit date
3. THE Audit_Orchestrator SHALL not include the audit date's data in baseline computations for anomaly detection
