<!-- DOC-0346 | duck_id: protocol-duckdb-schema-verification -->




# DuckDB Schema Verification Protocol

Ensures schema writes land in the correct persistent database. Run after any batch of CREATE TABLE/VIEW statements.

All DuckDB access goes through DuckDB MCP (`execute_query`). Do NOT use Python `duckdb.connect()` with MotherDuck tokens directly. The MCP server handles the connection.

---





## Why This Exists

On 4/6/2026, 10 tables from the mcp-capability-expansion spec were found missing despite being "created" in a prior session. Root cause: tables were written to a transient/shadow database rather than the persistent file. The DuckDB MCP server connects to `ps_analytics` on MotherDuck. Verification catches MCP server connection issues.





## Verification Steps

After any batch of CREATE TABLE or CREATE VIEW statements, immediately run via `execute_query`:





### Step 3: Confirm Tables Exist
```sql
SELECT table_type, COUNT(*) FROM information_schema.tables WHERE table_schema = 'main' GROUP BY table_type;
```
Expected: BASE TABLE = 46, VIEW = 39.



**Example:** This section demonstrates the pattern in practice — concrete instances ground abstract rules.




### Step 2: Confirm MCP Connection
```sql
SELECT database_name, path, type FROM duckdb_databases() WHERE database_name = 'ps_analytics';
```
If query succeeds, MCP is connected. If it fails, restart MCP server (touch .kiro/settings/mcp.json, then restart from panel).





### Step 1: Confirm Database Identity
```sql
SELECT current_database(), current_schema();
```
Expected: `ps_analytics`, `main`. If different → STOP.





**Example:** This section demonstrates the pattern in practice — concrete instances ground abstract rules.


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





## Quick Verification Query (copy-paste via execute_query)
-- Full schema check: 46 tables + 39 views expected
-- Connection check
-- Snapshot availability check
```sql
SELECT table_type, COUNT(*) AS count FROM information_schema.tables 
WHERE table_schema = 'main' GROUP BY table_type;

SELECT database_name, type FROM duckdb_databases() WHERE database_name = 'ps_analytics';

SELECT snapshot_name, created_ts FROM md_information_schema.database_snapshots
WHERE database_name = 'ps_analytics' ORDER BY created_ts DESC LIMIT 5;
```
