# Slack Bulk Ingestion — Agent Prompt

## What this does
Pulls full channel histories from Slack and inserts them into DuckDB (`slack_messages` table) using `slack-ingest.py` to generate SQL, then executing that SQL via `mcp_duckdb_execute_query`.

## Workflow (follow exactly)

### Step 1: Pull channel history → save to temp file
For each channel, call `batch_get_conversation_history` with limit 200, then IMMEDIATELY save the raw JSON response to a temp file. Do NOT try to process the JSON in-context — it's too large.

```
Save response to: /tmp/slack-{channel_id}.json
```

Use `executeBash` with a heredoc or Python one-liner to write the JSON. Pull ONE channel at a time to avoid context overflow.

### Step 2: Run slack-ingest.py to generate SQL
```bash
python3 ~/shared/tools/slack-ingest.py <channel_id> <channel_name> /tmp/slack-<channel_id>.json > /tmp/slack-<channel_id>.sql 2>/tmp/slack-<channel_id>.err
```

The script outputs SQL INSERT statements to stdout (redirected to .sql file). Check .err for row count.

### Step 3: Execute SQL via MCP in batches
Read the .sql file, split on `;\n`, and execute each batch via `mcp_duckdb_execute_query`. Each batch is ~25 rows.

### Step 4: Clean up and paginate
Delete temp files. If the channel had `has_more: true`, use the `next_cursor` to pull the next page and repeat.

## Channel list (from slack-channel-registry.json)
| Channel ID | Name | Priority |
|---|---|---|
| C044UG8MCSZ | ab-paid-search-global | HIGH |
| C0470FHVBAR | ab-paid-search-eu | HIGH |
| C044UGEJ76Z | ab-ps_jp | HIGH |
| C065KKT53DJ | ab-paid-search-abix | HIGH |
| C06R6R19LG0 | ab-paid-search-oci | HIGH |
| C05L7H41J7M | ab-paid-search-eng | MEDIUM |

## Current state
- DuckDB: `/shared/user/tools/data/ps-analytics.duckdb`
- 304 messages currently in slack_messages (as of 2026-04-02)
- 31 people in slack_people (all names verified where available)
- Script: `~/shared/tools/slack-ingest.py`
- Pagination state: `~/shared/context/active/slack-ingest-state.md`

## Important notes
- The DuckDB MCP server holds a write lock, so the script will output SQL (not write directly)
- Pull ONE channel at a time, process it fully, then move to the next
- The script skips channel_join/leave/topic subtypes automatically
- Messages are deduped on `ts` primary key (INSERT OR REPLACE)
- After all channels, run: `SELECT channel_name, COUNT(*) FROM slack_messages GROUP BY channel_name ORDER BY msg_count DESC`
