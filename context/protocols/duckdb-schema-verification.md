# DuckDB Schema Verification Protocol

Ensures schema writes land in the correct persistent MotherDuck cloud database. Run after any batch of CREATE TABLE/VIEW statements.

---

## Why This Exists

On 4/6/2026, 10 tables from the mcp-capability-expansion spec were found missing despite being "created" in a prior session. Root cause: tables were written to a transient/shadow database rather than the persistent file. Migration to MotherDuck cloud (4/6) eliminates the local file persistence problem, but verification remains important to catch MCP server connection issues.

The DuckDB MCP server connects to `md:ps_analytics` on MotherDuck (aws-us-east-1).

## Verification Steps

After any batch of CREATE TABLE or CREATE VIEW statements, immediately run:

### Step 1: Confirm Database Identity
```sql
SELECT current_database(), current_schema();
```
Expected: `ps_analytics`, `main`. If different → STOP.

### Step 2: Confirm MotherDuck Connection
```sql
SELECT database_name, path, type FROM duckdb_databases() WHERE database_name = 'ps_analytics';
```
Expected type: `motherduck`. If type is `duckdb` → MCP server fell back to local file. Restart MCP server (touch .kiro/settings/mcp.json, then restart from panel).

### Step 3: Confirm Tables Exist
```sql
SELECT table_type, COUNT(*) FROM information_schema.tables WHERE table_schema = 'main' GROUP BY table_type;
```
Expected: BASE TABLE = 46, VIEW = 39.

### Step 4: Confirm Data Persisted (if INSERTs were run)
```sql
SELECT '[table_name]' AS tbl, COUNT(*) AS rows FROM [table_name]
UNION ALL ...
```
Row counts must match expected inserts.

## When to Run

- After any spec execution that creates DuckDB tables
- After AM-1 full sync (creates/updates asana_tasks, asana_task_history)
- After EOD-1 meeting-to-task pipeline (inserts into meeting_analytics, meeting_highlights, workflow_executions)
- After any DuckDB schema migration

## Required Tables (mcp-capability-expansion)

These 10 tables + 3 views must exist in `ps-analytics.main`:

**Tables:**
1. unified_signals
2. meeting_analytics
3. meeting_highlights
4. data_freshness
5. health_alerts
6. relationship_activity
7. competitive_signals
8. recurring_tasks
9. workflow_executions
10. publication_registry
11. builder_cache

**Views:**
1. unified_signal_queue
2. competitive_intelligence
3. workflow_reliability

## Quick Verification Query (copy-paste)
```sql
-- Full schema check: 46 tables + 39 views expected
SELECT table_type, COUNT(*) AS count FROM information_schema.tables 
WHERE table_schema = 'main' GROUP BY table_type;

-- MotherDuck connection check
SELECT database_name, type FROM duckdb_databases() WHERE database_name = 'ps_analytics';
-- Expected: type = 'motherduck'

-- Snapshot availability check
SELECT snapshot_name, created_ts FROM md_information_schema.database_snapshots
WHERE database_name = 'ps_analytics' ORDER BY created_ts DESC LIMIT 5;
```
