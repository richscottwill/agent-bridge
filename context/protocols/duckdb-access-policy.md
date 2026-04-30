<!-- DOC-0389 | duck_id: protocol-duckdb-access-policy -->
# DuckDB Access Policy

**Effective: 2026-04-16. This policy supersedes all prior MotherDuck token references.**

## How Python Scripts Should Get DuckDB Data

**Option A (preferred): Read from JSON cache files.**
The agent queries DuckDB via MCP and writes results to local JSON files. Python scripts read those JSON files. This is how refresh-forecast.py and refresh-callouts.py already work — they read from xlsx/JSON, not from DuckDB directly.

**Option B: Agent queries MCP, passes results to script.**
For scripts that need live data, the agent runs the query via `execute_query`, then passes the result as a file or argument to the Python script.

**Option C: Script reads from DuckDB cache file.**
For scripts that absolutely need SQL access, use a local DuckDB file (`~/shared/data/ps-cache.duckdb`) that the agent populates via MCP exports. The script connects to the local file, not to MotherDuck.

## Scripts With Legacy MotherDuck Connections (to be migrated)

These scripts still have direct `duckdb.connect(md:...)` calls. They work but violate this policy. Migrate as needed:

| Script | Current State | Migration Path |
|--------|--------------|----------------|
| `update-forecast-tracker.py` | Reads from MotherDuck | Already reads xlsx — remove MotherDuck fallback |
| `generate-command-center.py` | Queries MotherDuck | Already rebuilt to use MCP-populated JSON — remove legacy code |
| `refresh-body-system.py` | Queries MotherDuck with cache fallback | Already uses cache — remove MotherDuck attempt |
| `populate_forecast_tracker.py` | Writes to MotherDuck | Agent should run via MCP instead |

#### Scripts With Legacy MotherDuck Connections (to be migrated) — Details

| `full_year_project.py` | Reads/writes MotherDuck | Agent should run via MCP instead |
| `detect_regime_changes.py` | Reads/writes MotherDuck | Agent should run via MCP instead |
| `wbr_pipeline.py` | Reads/writes MotherDuck | Agent should run via MCP instead |
| `project.py` | Reads MotherDuck | Agent should run via MCP instead |
| `backfill_forecasts.py` | Reads/writes MotherDuck | Agent should run via MCP instead |
| `project_full.py` | Reads/writes MotherDuck | Agent should run via MCP instead |

**Priority:** Dashboard scripts (top 3) are most urgent since they run in refresh-all.py pipeline. Prediction scripts run less frequently and can be migrated incrementally.

## Why This Matters

1. **MotherDuck token management is fragile.** Token expires, env var not set, config not found — every failure mode causes "MotherDuck unavailable" which cascades to skipped EOD phases.
2. **MCP is always available.** If the agent can chat, MCP is connected. No token management needed.
3. **Single point of truth.** MCP config manages the connection once. Scripts don't each need their own connection logic.
4. **Security.** Tokens hardcoded in Python files (prediction/config.py, project_full.py, etc.) are a credential exposure risk.


> **Example:** A typical use of this section involves reading the above rules and applying them to the current context.