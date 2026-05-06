-- Hedy Table Teardown Script
-- Created: 2026-05-06
-- EXECUTED: 2026-05-06 06:00 UTC (Richard overrode 6-gate discipline, ran teardown + backfill same session)
-- Purpose: Archive + drop the 4 deprecated Hedy-only DuckDB tables after the topic-log pipeline proves stable.
--
-- STATUS: COMPLETED. Archive tables live in hedy_archive.* (56/16/29/15 rows). Originals dropped.
-- Freshness: hedy_meetings row removed, topic_logs row added.
--
-- This script:
--   1. CREATEs a one-shot backup schema `hedy_archive`
--   2. COPIES all 4 Hedy-only tables into the archive with _archived_at timestamp
--   3. DROPs the original tables
--   4. Updates ops.data_freshness to remove the hedy_meetings row
--
-- The archive preserves the historical data so any future agent that wants to rebuild a
-- derived view (meeting_analytics replacement) can do so from the archive without reconnecting
-- to Hedy MCP.

-- Step 1: Create archive schema
CREATE SCHEMA IF NOT EXISTS hedy_archive;

-- Step 2: Archive tables with timestamp
CREATE TABLE IF NOT EXISTS hedy_archive.hedy_meetings AS
SELECT *, CURRENT_TIMESTAMP AS _archived_at
FROM signals.hedy_meetings;

CREATE TABLE IF NOT EXISTS hedy_archive.meeting_analytics AS
SELECT *, CURRENT_TIMESTAMP AS _archived_at
FROM main.meeting_analytics;

CREATE TABLE IF NOT EXISTS hedy_archive.meeting_highlights AS
SELECT *, CURRENT_TIMESTAMP AS _archived_at
FROM main.meeting_highlights;

CREATE TABLE IF NOT EXISTS hedy_archive.meeting_series AS
SELECT *, CURRENT_TIMESTAMP AS _archived_at
FROM main.meeting_series;

-- Verification: row counts should match pre-drop
SELECT 'signals.hedy_meetings' AS source, COUNT(*) AS rows FROM signals.hedy_meetings
UNION ALL SELECT 'hedy_archive.hedy_meetings', COUNT(*) FROM hedy_archive.hedy_meetings
UNION ALL SELECT 'main.meeting_analytics', COUNT(*) FROM main.meeting_analytics
UNION ALL SELECT 'hedy_archive.meeting_analytics', COUNT(*) FROM hedy_archive.meeting_analytics
UNION ALL SELECT 'main.meeting_highlights', COUNT(*) FROM main.meeting_highlights
UNION ALL SELECT 'hedy_archive.meeting_highlights', COUNT(*) FROM hedy_archive.meeting_highlights
UNION ALL SELECT 'main.meeting_series', COUNT(*) FROM main.meeting_series
UNION ALL SELECT 'hedy_archive.meeting_series', COUNT(*) FROM hedy_archive.meeting_series;

-- Step 3: Drop originals (EXECUTED 2026-05-06)
DROP TABLE IF EXISTS signals.hedy_meetings;
DROP TABLE IF EXISTS main.meeting_analytics;
DROP TABLE IF EXISTS main.meeting_highlights;
DROP TABLE IF EXISTS main.meeting_series;

-- Step 4: Update freshness tracker (EXECUTED 2026-05-06)
DELETE FROM ops.data_freshness WHERE source_name = 'hedy_meetings';
INSERT INTO ops.data_freshness (source_name, source_type, expected_cadence_hours, last_updated, last_checked, is_stale, downstream_workflows)
SELECT 'topic_logs', 'file_count', 24, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE, ['topic-sentry', 'wbr-callouts', 'broad-sweep']
WHERE NOT EXISTS (SELECT 1 FROM ops.data_freshness WHERE source_name = 'topic_logs');

-- Post-teardown recovery path:
-- If we ever need the meeting_series table back (for a dashboard or agent that wasn't caught),
-- rebuild from topic-log files:
--   CREATE TABLE main.meeting_series AS
--     SELECT <fields> FROM <topic_log_scan>
-- Or restore from archive:
--   CREATE TABLE main.meeting_series AS
--     SELECT * EXCLUDE(_archived_at) FROM hedy_archive.meeting_series;
