<!-- DOC-0361 | duck_id: protocol-slack-ingest-state -->
# Slack Bulk Ingestion State

Last run: 2026-04-02

**Example:** If this section references a specific process, the concrete steps are: Last run: 2026-04-02...


## DuckDB Stats
- Total messages: 304
- Channels with data: 22
- DB path: ps-analytics.duckdb (via DuckDB MCP server)

## Channel Pagination Cursors (for resuming)

| Channel ID | Name | Messages | has_more | Next Cursor |
|---|---|---|---|---|
| C044UG8MCSZ | ab-paid-search-global | 157 | true | `bmV4dF90czoxNzcxODYzNTU5ODExOTg5` |
| C0470FHVBAR | ab-paid-search-eu | 28 | true | `bmV4dF90czoxNzcxOTY1NzkyMTg1NTQ5` |
| C044UGEJ76Z | ab-ps_jp | 25 | true | `bmV4dF90czoxNzc0NjUxNDgxNTM2NzY5` |
| C065KKT53DJ | ab-paid-search-abix | 21 | true | `bmV4dF90czoxNzc0Mzg1OTU3NzIxMzk5` |
| C06R6R19LG0 | ab-paid-search-oci | 25 | true | `bmV4dF90czoxNzczOTI4MjcyMTkzNzQ5` |
| C05L7H41J7M | ab-paid-search-eng | 16 | true | `bmV4dF90czoxNzU4MzE2MDkyODQyMTQ5` |

## Approach
- Fetch 25 messages at a time via `batch_get_conversation_history`
- Generate SQL INSERT statements manually from message text

#### Approach — Details

- Execute via `mcp_duckdb_execute_query`
- Skip: channel_join/leave/topic subtypes, empty text, image-only messages

## Key Learnings
- Slack MCP returns full JSON with blocks/files/thumbnails — very context-heavy
- 25 messages per fetch is the sweet spot (10 too slow, 50+ risks context overflow)
- Sub-agent delegation was attempted but cancelled
- The original slack-ingest.py pipeline (save JSON → run script → execute SQL) doesn't work because MCP tool responses can't be piped to files

## To Resume
- Tell the agent: "Continue Slack bulk ingestion.
- Resume [channel] from cursor [cursor].
- Approach: fetch 25 msgs → generate SQL INSERT → execute via DuckDB MCP → paginate.".
