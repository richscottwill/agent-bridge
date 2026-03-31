# Requirements Document

## Introduction

This document defines the requirements for the Data Layer Overhaul — migrating structured data from markdown files to DuckDB as the canonical source of truth for numbers, while keeping markdown as the canonical source for narrative content. The overhaul extends the existing `query.py` with write operations and convenience functions, adds new DuckDB tables for data currently embedded in markdown, updates all consuming pipelines, and establishes a portability layer for platform-independent reconstruction. The design also lays the foundation for agentic autonomy through agent state tables and an approval gradient.

## Glossary

- **Query_Helper**: The `query.py` module that provides unified data access to DuckDB (`db()`, `db_df()`, `db_write()`, `db_upsert()`, and convenience functions)
- **Schema_Manager**: The `init_db.py` module that defines and migrates the DuckDB schema
- **Ingester**: The `ingest.py` dashboard ingestion script that reads xlsx files and writes structured data to DuckDB
- **Chart_Generator**: The `generate.py` script that produces the HTML dashboard from data sources
- **Portability_Layer**: The combination of `schema.sql` and `RECONSTRUCTION.md` that enables full database reconstruction on any platform
- **Anomaly_Detector**: The subsystem within the Ingester that flags metrics deviating >20% from their 8-week average
- **Callout_Pipeline**: The WBR callout workflow (analyst → writer → reviewer) that produces weekly market callouts
- **Agent_State_Tables**: The set of DuckDB tables (`agent_actions`, `agent_observations`, `decisions`, `task_queue`) that provide agent continuity and audit trail
- **Approval_Gradient**: The system that classifies agent decisions by risk level and routes them for auto-execution or human review

## Requirements

### Requirement 1: Query Helper Write Operations

**User Story:** As an agent developer, I want write operations in the query helper, so that agents can persist structured data to DuckDB without opening direct database connections.

#### Acceptance Criteria

1. WHEN an agent calls `db_write()` with a valid INSERT, UPDATE, or DELETE statement, THE Query_Helper SHALL execute the statement and return the number of rows affected
2. WHEN an agent calls `db_upsert()` with a data dict and key columns, THE Query_Helper SHALL insert a new row if no matching key exists, or update non-key columns if a matching key exists
3. WHEN `db_upsert()` is called twice with identical data, THE Query_Helper SHALL produce the same database state as calling it once (idempotent upsert)
4. WHEN `db_write()` or `db_upsert()` completes, THE Query_Helper SHALL close the database connection without leaking resources
5. IF `db_write()` receives a malformed SQL statement, THEN THE Query_Helper SHALL raise a descriptive error and leave the database unchanged

### Requirement 2: Query Helper Convenience Functions

**User Story:** As an agent developer, I want convenience functions for common query patterns, so that agents can retrieve market data with a single function call instead of writing raw SQL.

#### Acceptance Criteria

1. WHEN `market_week(market, week)` is called, THE Query_Helper SHALL return a single dict of weekly metrics for that market and week, or None if no data exists
2. WHEN `market_trend(market, weeks)` is called, THE Query_Helper SHALL return a list of up to `weeks` dicts ordered most-recent-first, containing only rows for the specified market
3. WHEN `market_month(market, month)` is called, THE Query_Helper SHALL return a single dict of monthly metrics including OP2 targets, or None if no data exists
4. WHEN `projection(market, week)` is called, THE Query_Helper SHALL return the projection dict for that market and week, or None if no data exists
5. WHEN `callout_scores(market, weeks)` is called, THE Query_Helper SHALL return a list of up to `weeks` callout score dicts for that market, ordered most-recent-first
6. THE Query_Helper convenience functions SHALL return identical data to the equivalent raw SQL query executed via `db()`

### Requirement 3: New DuckDB Tables for Structured Data Migration

**User Story:** As a system architect, I want new DuckDB tables for data currently embedded in markdown, so that structured data is queryable via SQL instead of parsed via regex.

#### Acceptance Criteria

1. THE Schema_Manager SHALL create a `change_log` table with columns for id, market, date, category, description, impact_metric, impact_value, source, and ingested_at
2. THE Schema_Manager SHALL create an `anomalies` table with columns for id, market, week, metric, value, baseline, deviation_pct, direction, flagged_at, resolved, and notes
3. THE Schema_Manager SHALL create a `competitors` table with a composite primary key of (market, competitor, week) and columns for impression_share, cpc_impact_pct, segment, notes, and ingested_at
4. THE Schema_Manager SHALL create an `oci_status` table with market as primary key and columns for status, launch_date, full_impact_date, reg_lift_pct, cpa_improvement, notes, and updated_at
5. WHEN `init_db.py` is run on a database that already contains existing tables, THE Schema_Manager SHALL add new tables without modifying or deleting existing table data
6. THE Schema_Manager SHALL enforce CHECK constraints: callout_scores between 0 and 10, competitors impression_share between 0 and 100, anomalies deviation_pct not equal to 0, projections projected_regs greater than 0

### Requirement 4: Schema Export and Portability

**User Story:** As a system operator, I want the database schema exported as plain SQL after each ingestion, so that the DuckDB database can be reconstructed on any platform from text files alone.

#### Acceptance Criteria

1. WHEN `schema_export()` is called, THE Query_Helper SHALL write a `schema.sql` file containing valid CREATE TABLE statements for every table in the database
2. WHEN `schema_export()` produces a schema.sql file, THE Portability_Layer SHALL include row count comments and a generation timestamp in the output
3. WHEN the exported `schema.sql` is executed on an empty DuckDB instance, THE Portability_Layer SHALL create all tables with the same structure as the source database
4. THE Portability_Layer SHALL include a `RECONSTRUCTION.md` file documenting which markdown files map to which tables, how to rebuild from scratch, and query patterns for common agent tasks
5. WHEN the Ingester completes a run, THE Ingester SHALL automatically invoke `schema_export()` to keep the portability layer current

### Requirement 5: Anomaly Detection

**User Story:** As a paid search analyst, I want automatic anomaly detection during data ingestion, so that significant metric deviations are flagged without manual inspection.

#### Acceptance Criteria

1. WHEN the Ingester processes a market's weekly data, THE Anomaly_Detector SHALL compare each metric (regs, cpa, cvr, spend, clicks) against the 8-week historical average
2. WHEN a metric deviates more than 20% from the 8-week average, THE Anomaly_Detector SHALL write a row to the anomalies table with the metric name, current value, baseline value, deviation percentage, and direction
3. IF a metric has fewer than 3 historical data points, THEN THE Anomaly_Detector SHALL skip anomaly detection for that metric
4. IF the baseline average for a metric is zero, THEN THE Anomaly_Detector SHALL skip anomaly detection for that metric
5. THE Anomaly_Detector SHALL not modify the input data or any other table during anomaly detection

### Requirement 6: Data Migration from Markdown to DuckDB

**User Story:** As a system operator, I want structured data migrated from markdown files to DuckDB, so that agents query SQL for numbers instead of parsing files with regex.

#### Acceptance Criteria

1. WHEN migration runs, THE Schema_Manager SHALL backfill the competitors table from eyes.md competitive landscape tables
2. WHEN migration runs, THE Schema_Manager SHALL backfill the oci_status table from eyes.md OCI performance tables
3. WHEN migration runs, THE Schema_Manager SHALL backfill the change_log table from per-market change log markdown files
4. WHEN migration completes for a data category, THE Portability_Layer SHALL verify that every structured data point from the source markdown is queryable from DuckDB
5. WHILE migration is in progress, THE Query_Helper SHALL treat DuckDB values as authoritative for any metric that exists in both DuckDB and markdown

### Requirement 7: Markdown Simplification

**User Story:** As a system architect, I want markdown files simplified to contain only narrative prose, so that the system trends toward subtraction and eliminates duplication between markdown and DuckDB.

#### Acceptance Criteria

1. WHEN migration completes for a data category, THE system SHALL remove the corresponding embedded metric tables from markdown files
2. WHEN metric tables are removed from markdown, THE system SHALL insert query hint comments referencing the equivalent DuckDB query
3. THE system SHALL preserve all narrative prose content in markdown files during simplification
4. WHEN eyes.md is simplified, THE system SHALL remove the Market Health table, OCI Performance tables, and Competitive Landscape tables, replacing each with a query hint
5. WHEN per-market data briefs are simplified, THE system SHALL remove embedded trend tables and projection tables, keeping only narrative summaries and query references

### Requirement 8: Callout Pipeline Update

**User Story:** As a callout pipeline operator, I want the pipeline to read metrics from DuckDB instead of parsing markdown data briefs, so that analysis is faster and eliminates regex fragility.

#### Acceptance Criteria

1. WHEN the analyst agent runs for a market, THE Callout_Pipeline SHALL retrieve weekly metrics via `market_trend()` and `market_week()` instead of parsing data brief markdown tables
2. WHEN the analyst agent produces a projection, THE Callout_Pipeline SHALL write the projection to the projections table via `db_upsert()`
3. WHEN the reviewer agent scores callouts, THE Callout_Pipeline SHALL write scores to the callout_scores table via `db_upsert()`
4. WHEN the reviewer agent compares against historical scores, THE Callout_Pipeline SHALL retrieve score history via `callout_scores()` convenience function
5. THE Callout_Pipeline SHALL continue reading narrative context (callout-principles.md, per-market context files) from markdown files

### Requirement 9: Chart Generator Update

**User Story:** As a dashboard consumer, I want the chart generator to read structured data from DuckDB, so that dashboard generation eliminates regex parsing of organ files for metrics.

#### Acceptance Criteria

1. WHEN generating market performance charts, THE Chart_Generator SHALL query weekly_metrics and monthly_metrics tables via the Query_Helper instead of regex-parsing organ files
2. WHEN generating experiment charts, THE Chart_Generator SHALL query the experiments table via the Query_Helper instead of regex-parsing changelog.md
3. THE Chart_Generator SHALL continue reading narrative organ data (amcc streak, patterns, budgets, competence stages, staleness, autonomy spectrum) from markdown files via existing parsers
4. WHEN the Chart_Generator completes, THE Chart_Generator SHALL produce the same 5-page HTML dashboard structure as the current implementation

### Requirement 10: Ingester Enhancement

**User Story:** As a data pipeline operator, I want the ingester to detect anomalies, export schema, and produce slimmer data briefs, so that ingestion is a complete data pipeline step.

#### Acceptance Criteria

1. WHEN the Ingester processes weekly data for a market, THE Ingester SHALL invoke the Anomaly_Detector and write flagged anomalies to the anomalies table
2. WHEN the Ingester completes a full run, THE Ingester SHALL invoke `schema_export()` to update the portability layer
3. WHEN the Ingester generates data briefs, THE Ingester SHALL produce narrative-only briefs with query hint references instead of embedding raw metric tables
4. THE Ingester SHALL continue using upsert semantics on primary keys so that re-running on the same xlsx produces the same database state

### Requirement 11: Agent State Tables

**User Story:** As a system architect, I want agent state tables in DuckDB, so that agents have continuity between sessions and their actions are auditable via SQL.

#### Acceptance Criteria

1. THE Schema_Manager SHALL create an `agent_actions` table with columns for id, agent, action_type, market, week, description, input_summary, output_summary, confidence, requires_human_review, reviewed_by_human, human_feedback, and created_at
2. THE Schema_Manager SHALL create an `agent_observations` table with columns for id, agent, observation_type, market, week, content, severity, acted_on, acted_on_by, and created_at
3. THE Schema_Manager SHALL create a `decisions` table with columns for id, decision_type, market, description, rationale, made_by, approved_by, approval_required, status, outcome, created_at, and resolved_at
4. THE Schema_Manager SHALL create a `task_queue` table with columns for id, task_type, market, description, priority, assigned_to, status, created_by, created_at, completed_at, and result
5. WHEN an agent performs an action, THE Query_Helper SHALL support writing the action to the agent_actions table via `db_write()` or `db_upsert()`

### Requirement 12: Connection Safety

**User Story:** As a system operator, I want read-only connections as the default for all agent queries, so that agents cannot accidentally mutate data through query functions.

#### Acceptance Criteria

1. WHEN `db()` or `db_df()` is called, THE Query_Helper SHALL open a read-only database connection
2. WHEN `db_write()` or `db_upsert()` is called, THE Query_Helper SHALL open a read-write database connection
3. IF an agent passes a write statement (INSERT, UPDATE, DELETE) to `db()`, THEN THE Query_Helper SHALL raise an error from the read-only connection without modifying the database
4. WHEN any query or write operation completes (successfully or with error), THE Query_Helper SHALL close the database connection

### Requirement 13: Error Handling and Recovery

**User Story:** As a system operator, I want clear error handling for database operations, so that failures are diagnosable and recoverable without data loss.

#### Acceptance Criteria

1. IF the DuckDB file does not exist when `db()` is called, THEN THE Query_Helper SHALL raise an error message indicating the file path and instructing to run `init_db.py`
2. IF the Ingester crashes mid-write, THEN THE Ingester SHALL rely on DuckDB ACID transactions to roll back partial writes, leaving the database in its pre-ingestion state
3. IF `init_db.py` is run on a database with an older schema, THEN THE Schema_Manager SHALL add missing tables without affecting existing table data or rows
4. IF an agent queries DuckDB for data that has not been backfilled yet, THEN THE Query_Helper SHALL return an empty result set (not an error)
