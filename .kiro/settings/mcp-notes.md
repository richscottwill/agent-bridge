# MCP Server Notes: Hedy & DuckDB

## Hedy (Meeting Intelligence)

**What it is:** Hedy is an AI meeting coach that records, transcribes, and analyzes meetings. The MCP server gives agents access to session transcripts, highlights, to-dos, and topics.

**Server type:** Remote OAuth server (not an AIM package)
**URL:** `https://api.hedy.bot/mcp`
**Transport:** Uses `mcp-remote` npm bridge to convert remote OAuth into local stdio
**Auth:** OAuth via browser — first connection opens a browser window to sign in with your Hedy account
**Requires:** Hedy Pro subscription, Node.js (for npx/mcp-remote)

**Available tools (18 total):**
- `GetSessions` / `GetSessionDetails` — list and read meeting sessions with full transcripts
- `GetSessionHighlights` / `GetHighlights` / `GetHighlightDetails` — key moments captured during meetings
- `GetSessionToDos` / `GetToDos` — action items extracted from meetings
- `GetAllTopics` / `GetTopicDetails` / `GetTopicSessions` — organized conversation themes
- `CreateTopic` / `UpdateTopic` / `DeleteTopic` — manage topic organization
- `ListSessionContexts` / `GetSessionContext` / `CreateSessionContext` / `UpdateSessionContext` / `DeleteSessionContext` — background info Hedy uses during analysis

**Re-authorization:** If the OAuth token expires, reconnect from the MCP Server panel — it will re-trigger the browser auth flow.

**Headless environments (AgentSpaces/DevSpaces):** OAuth requires a browser. Either authorize on local machine first and copy `~/.mcp-auth/` cache, or use the older API key approach with a Bearer token from Hedy settings.

**Docs:**
- Setup: https://help.hedy.bot/en/articles/12465594-connect-hedy-with-ai-assistants-using-mcp
- Product: https://www.hedy.ai

---

## DuckDB (via MotherDuck MCP)

**What it is:** An in-process SQL database. The MCP server lets agents run SQL queries, browse schemas, and interact with MotherDuck cloud databases. This is the ONLY way to access DuckDB — do NOT use Python `duckdb.connect()` with MotherDuck tokens directly.

**Server type:** Local Python package via uvx (not an AIM package)
**Package:** `mcp-server-motherduck` on PyPI
**Requires:** Python 3.10+, uvx/uv

**Current config:** Connected to `ps_analytics` on MotherDuck cloud. Read-write enabled.

**POLICY (as of 2026-04-16):** All DuckDB access goes through DuckDB MCP (`execute_query`). Python scripts that need DuckDB data should either:
1. Read from local JSON cache files that the agent populates via MCP, OR
2. Be invoked by the agent which queries MCP and passes results as arguments.
Do NOT use `duckdb.connect()` with `motherduck_token` in Python scripts. The MCP server handles authentication and connection management.

**Key flags:**
- `--db-path md:` — connects to MotherDuck cloud (current config)
- `--read-write` — enables write operations
- `--motherduck-token TOKEN` — handled by MCP config, not by scripts
- `--allow-switch-databases` — lets the agent switch between databases at runtime

**Available tools:**
- `execute_query` — run any SQL query (this is the primary interface)
- `list_databases` — show attached databases
- `list_tables` — show tables/views with comments
- `list_columns` — show column types and comments for a table

### Connecting to MotherDuck (cloud)

MotherDuck is the cloud-hosted version of DuckDB. It goes through the same MCP server — you just change the connection args:

```json
"duckdb": {
  "command": "uvx",
  "args": [
    "mcp-server-motherduck",
    "--db-path", "md:",
    "--motherduck-token", "YOUR_TOKEN_HERE",
    "--read-write"
  ]
}
```

- `md:` tells DuckDB to connect to MotherDuck instead of a local file
- The token comes from your MotherDuck account at https://app.motherduck.com
- Once connected, you can query both local and cloud databases, read S3/GCS Parquet files directly, and use MotherDuck's shared databases
- There is no separate "MotherDuck MCP server" — it's all `mcp-server-motherduck`, just with different connection flags

**Docs:**
- GitHub: https://github.com/motherduckdb/mcp-server-motherduck
- PyPI: https://pypi.org/project/mcp-server-motherduck/
- Blog: https://motherduck.com/blog/faster-data-pipelines-with-mcp-duckdb-ai/
- MotherDuck: https://motherduck.com
