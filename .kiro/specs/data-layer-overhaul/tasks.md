# Implementation Plan: Data Layer Overhaul

## Overview

Migrate structured data from markdown to DuckDB as the canonical source of truth for numbers. Extend `query.py` with write operations and convenience functions, add new tables, update all consuming pipelines (callout, chart generator, ingester), simplify markdown files, and establish a portability layer. Phase A is the full scope; Phase B (agent state tables) gets schema only.

## Tasks

- [x] 1. Extend DuckDB schema with new tables
  - [x] 1.1 Add `change_log`, `anomalies`, `competitors`, `oci_status` tables to `init_db.py`
    - Add CREATE TABLE IF NOT EXISTS statements with all columns per design
    - Add CHECK constraints: callout_scores 0-10, competitors impression_share 0-100, anomalies deviation_pct != 0, projections projected_regs > 0
    - Add auto-increment sequences for change_log and anomalies id columns
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

  - [x] 1.2 Add Phase B agent state tables to `init_db.py` (schema only, no consumers yet)
    - Add `agent_actions`, `agent_observations`, `decisions`, `task_queue` tables per design
    - Add auto-increment sequences for all four tables
    - These tables will be empty until Phase B wires agents to write to them
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

  - [x] 1.3 Write property test for schema migration idempotence
    - **Property 5: Schema migration idempotence**
    - Run `init_db()` on a populated DB, verify existing row counts unchanged and new tables added
    - **Validates: Requirements 3.5, 13.3**

  - [x] 1.4 Write property test for CHECK constraint enforcement
    - **Property 6: CHECK constraint enforcement**
    - Attempt inserts with out-of-range values, verify rejection by DB
    - **Validates: Requirement 3.6**

- [x] 2. Enhance query.py with write operations and convenience functions
  - [x] 2.1 Add `db_write()` and `db_upsert()` to `query.py`
    - `db_write(sql, params, db_path)` — opens read-write connection, executes INSERT/UPDATE/DELETE, returns rows affected, closes connection
    - `db_upsert(table, data, key_cols, db_path)` — builds INSERT ... ON CONFLICT DO UPDATE SET, executes via read-write connection
    - Ensure `db()` and `db_df()` remain read-only (already use `read_only=True`)
    - Add error handling: descriptive error on malformed SQL, connection always closed (try/finally)
    - Add DB-not-found check: if .duckdb file missing, raise error pointing to `init_db.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 12.1, 12.2, 12.3, 12.4, 13.1_

  - [x] 2.2 Add convenience query functions to `query.py`
    - `market_week(market, week)` — single dict or None from weekly_metrics
    - `market_trend(market, weeks=8)` — list of up to N dicts, most-recent-first
    - `market_month(market, month)` — single dict or None from monthly_metrics
    - `projection(market, week)` — single dict or None from projections
    - `callout_scores(market, weeks=8)` — list of up to N score dicts, most-recent-first
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

  - [x] 2.3 Add `schema_export()` to `query.py`
    - Export all CREATE TABLE statements + row count comments + timestamp to `~/shared/tools/data/schema.sql`
    - Use `duckdb_tables()` system function to extract DDL
    - _Requirements: 4.1, 4.2, 4.3_

  - [x] 2.4 Write property test for upsert idempotence
    - **Property 1: Upsert correctness and idempotence**
    - Using hypothesis, generate random data dicts, verify insert-on-new, update-on-existing, double-upsert produces same state
    - **Validates: Requirements 1.2, 1.3**

  - [x] 2.5 Write property test for write error safety
    - **Property 2: Write error safety**
    - Pass malformed SQL to `db_write()`, verify error raised and DB state unchanged
    - **Validates: Requirement 1.5**

  - [x] 2.6 Write property test for convenience function equivalence
    - **Property 3: Convenience function equivalence to raw SQL**
    - For each convenience function, verify output matches equivalent raw `db()` SQL query
    - **Validates: Requirements 2.1-2.6**

  - [x] 2.7 Write property test for list convenience bounds and ordering
    - **Property 4: List convenience functions are bounded, filtered, and ordered**
    - Verify `market_trend(m, N)` returns ≤ N rows, all for market m, ordered week DESC
    - **Validates: Requirements 2.2, 2.5**

  - [x] 2.8 Write property test for read-only connection enforcement
    - **Property 11: Read-only connection enforcement**
    - Pass INSERT/UPDATE/DELETE to `db()`, verify error raised and DB unchanged
    - **Validates: Requirements 12.1, 12.3**

  - [x] 2.9 Write property test for empty query returns
    - **Property 13: Empty query returns empty result**
    - Query empty/non-backfilled tables via `db()`, verify empty list returned (not error)
    - **Validates: Requirement 13.4**

- [x] 3. Checkpoint — Verify schema and query layer
  - Run `init_db.py` on the existing database, confirm new tables created without affecting existing data
  - Test each convenience function against live data in ps-analytics.duckdb
  - Test `db_write()` and `db_upsert()` with sample inserts to new tables
  - Verify `schema_export()` produces valid schema.sql
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Update dashboard ingester with anomaly detection and schema export
  - [x] 4.1 Add `_detect_anomalies()` method to `DashboardIngester` in `ingest.py`
    - Compare each metric (regs, cpa, cvr, spend, clicks) against 8-week average from `market_trend()`
    - Flag metrics deviating >20% from baseline
    - Skip metrics with <3 historical data points or zero baseline
    - Write flagged anomalies to `anomalies` table via `db_upsert()`
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [x] 4.2 Wire anomaly detection and schema export into ingester pipeline
    - Call `_detect_anomalies()` after processing each market's weekly data
    - Call `schema_export()` at end of full ingestion run
    - Import convenience functions from `query.py` (add `sys.path` or relative import)
    - Maintain upsert semantics on all existing writes (idempotent re-runs)
    - _Requirements: 10.1, 10.2, 10.4_

  - [x] 4.3 Write property test for anomaly detection threshold
    - **Property 8: Anomaly detection threshold correctness**
    - Generate synthetic week_data and trend lists, verify >20% flagged, ≤20% not flagged, <3 data points skipped, zero baseline skipped
    - **Validates: Requirements 5.1-5.4**

  - [x] 4.4 Write property test for anomaly detection purity
    - **Property 9: Anomaly detection purity**
    - Verify `_detect_anomalies()` does not modify input data or other tables
    - **Validates: Requirement 5.5**

  - [x] 4.5 Write property test for ingester idempotence
    - **Property 12: Ingester idempotence**
    - Run ingester twice on same test data, verify identical DB state
    - **Validates: Requirement 10.4**

- [x] 5. Update callout pipeline to read from DuckDB
  - [x] 5.1 Update analyst agent data access patterns
    - Modify analyst agents (`abix-analyst`, `najp-analyst`, `eu5-analyst`) to import and use `market_trend()`, `market_week()`, `projection()` from `query.py` instead of parsing data brief markdown tables
    - Analyst agents write projections to `projections` table via `db_upsert()` instead of appending to markdown
    - Agents continue reading narrative context (callout-principles.md, per-market context files) from markdown
    - _Requirements: 8.1, 8.2, 8.5_

  - [x] 5.2 Update callout reviewer to write scores to DuckDB
    - Modify `callout-reviewer` agent to write quality scores to `callout_scores` table via `db_upsert()`
    - Reviewer reads historical scores via `callout_scores()` convenience function for trend comparison
    - _Requirements: 8.3, 8.4_

- [x] 6. Update chart generator to query DuckDB
  - [x] 6.1 Replace regex-based metric parsers in `generate.py` with DuckDB queries
    - Replace `parse_tracker_scorecard()` market performance data with `db("SELECT ... FROM weekly_metrics ...")`
    - Replace `parse_changelog()` experiment extraction with `db("SELECT * FROM experiments ...")`
    - Replace `parse_changelog()` savings data with DuckDB query if compression_log table exists, else keep as-is
    - Keep all narrative parsers unchanged: `parse_gut_budgets()`, `parse_patterns()`, `parse_amcc()`, `parse_five_levels()`, `parse_organ_staleness()`, `parse_autonomy_spectrum()`, `parse_competence_stages()`
    - Import `db` from `query.py`
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [x] 7. Checkpoint — Verify pipeline updates
  - Run callout pipeline on a test market, confirm analyst reads from DuckDB and writes projection
  - Run callout reviewer, confirm scores written to callout_scores table
  - Run chart generator, confirm HTML dashboard renders with DuckDB-sourced data
  - Verify ingester anomaly detection flags expected deviations
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Data migration from markdown to DuckDB
  - [x] 8.1 Write migration script to backfill `competitors` table from `eyes.md`
    - Parse competitive landscape tables from eyes.md
    - Write rows to `competitors` table via `db_upsert()`
    - Verify all structured data points are queryable post-migration
    - _Requirements: 6.1, 6.4_

  - [x] 8.2 Write migration script to backfill `oci_status` table from `eyes.md`
    - Parse OCI performance tables from eyes.md
    - Write rows to `oci_status` table via `db_upsert()`
    - _Requirements: 6.2, 6.4_

  - [x] 8.3 Write migration script to backfill `change_log` table from per-market change log files
    - Parse structured entries (date, category, description, impact) from change log markdown files
    - Write rows to `change_log` table via `db_upsert()`
    - Keep narrative entries in markdown (the "why" stays, the "what" moves)
    - _Requirements: 6.3, 6.4, 6.5_

  - [x] 8.4 Write property test for migration completeness
    - **Property 14: Migration completeness**
    - For each migrated data point from source markdown, verify a SQL query returns it from DuckDB
    - **Validates: Requirement 6.4**

- [x] 9. Simplify markdown files
  - [x] 9.1 Simplify `eyes.md` — remove metric tables, add query hints
    - Remove Market Health table, replace with query hint: `db("SELECT market, ... FROM weekly_metrics ...")`
    - Remove OCI Performance tables, replace with query hint referencing `oci_status` table
    - Remove Competitive Landscape tables, replace with query hint referencing `competitors` table
    - Preserve all narrative prose content unchanged
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [x] 9.2 Simplify per-market data briefs — remove embedded tables
    - Remove embedded trend tables and projection tables from data brief markdown files
    - Add query hint references (e.g., `market_trend('AU')`, `projection('AU', '2026 W13')`)
    - Keep narrative summaries and context notes intact
    - _Requirements: 7.1, 7.2, 7.3, 7.5_

  - [x] 9.3 Update ingester to generate slim data briefs
    - Modify `_write_to_duckdb()` / brief generation in `ingest.py` to produce narrative-only briefs
    - Briefs contain: narrative summary, query hints, and only context notes not in DuckDB
    - No embedded metric tables in generated briefs
    - _Requirements: 10.3_

  - [x] 9.4 Write property test for narrative preservation
    - **Property 10: Narrative preservation during markdown simplification**
    - Verify prose word count after simplification ≥ prose word count before (minus small epsilon for table-to-hint replacement)
    - **Validates: Requirement 7.3**

- [x] 10. Create portability layer
  - [x] 10.1 Create `RECONSTRUCTION.md` at `~/shared/tools/data/RECONSTRUCTION.md`
    - Document which markdown files map to which DuckDB tables
    - Document rebuild-from-scratch procedure: `init_db.py` → `ingest.py` → manual backfill for competitors/oci/change_log
    - Document query patterns for common agent tasks (market trend, projection, anomaly check, score history)
    - Document the schema.sql auto-export mechanism
    - _Requirements: 4.4_

  - [x] 10.2 Write property test for schema export round-trip
    - **Property 7: Schema export round-trip**
    - Export schema via `schema_export()`, execute on empty DuckDB, verify all tables created with same structure
    - **Validates: Requirements 4.1, 4.3**

- [x] 11. Wire everything together and update system documentation
  - [x] 11.1 Update `device.md` PS Analytics Database section
    - Update table list to include new tables (change_log, anomalies, competitors, oci_status, agent state tables)
    - Note that `query.py` now supports write operations (`db_write`, `db_upsert`) and convenience functions
    - Reference `RECONSTRUCTION.md` for portability documentation
    - _Requirements: 4.4, 11.5_

  - [x] 11.2 Update `spine.md` tool access section
    - Add write operation examples: `from query import db_upsert, market_trend`
    - Note schema export and portability layer
    - _Requirements: 4.4_

- [x] 12. Final checkpoint — Full system validation
  - Run `init_db.py` — verify all 12 tables exist (8 original + 4 new Phase A tables; 4 Phase B agent state tables present but empty)
  - Run `schema_export()` — verify schema.sql is valid and complete
  - Query each new table — verify backfilled data is accessible
  - Run ingester on latest xlsx — verify anomaly detection, schema export, slim briefs
  - Run callout pipeline — verify DuckDB reads and writes
  - Run chart generator — verify HTML dashboard renders correctly
  - Verify simplified markdown files retain all narrative prose
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests use the `hypothesis` library (Python) per design spec
- Checkpoints ensure incremental validation at natural break points
- Phase A (tasks 1-12) is the full scope of this overhaul
- Phase B agent state tables get schema only (task 1.2) — consumers are future work
- Phases C (approval gradient) and D (continuous operations) are future work, not included in this plan
- All code changes are Python, targeting existing files in `~/shared/tools/data/`, `~/shared/tools/dashboard-ingester/`, `~/shared/tools/progress-charts/`, and `~/.kiro/agents/wbr-callouts/`
