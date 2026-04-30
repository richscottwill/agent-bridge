<!-- DOC-0389 | duck_id: protocol-duckdb-access-policy -->
# DuckDB Access Policy

**Effective: 2026-04-16. This policy supersedes all prior MotherDuck token references.**

[38;5;10m> [0m## How Python Scripts Should Get DuckDB Data[0m[0m
[0m[0m
Python scripts should never connect to MotherDuck directly. Instead, they get data through one of three approaches:[0m[0m
[0m[0m
**Option A (preferred): Read from JSON cache files.**[0m[0m
The agent queries DuckDB via MCP, writes results to local JSON files, and scripts read those files. For example, `refresh-forecast.py` reads `~/shared/data/forecast-cache.json` rather than running SQL against MotherDuck — it never needs a database connection at all.[0m[0m
[0m[0m
**Option B: Agent queries MCP, passes results to script.**[0m[0m
When a script needs fresh data that isn't cached, the agent runs the query via `execute_query` and passes the result as a file or CLI argument. For example, the agent could run `execute_query("SELECT * FROM actuals WHERE month = '2026-03'")`, save the output to `/tmp/actuals-march.json`, then call `python my_script.py --input /tmp/actuals-march.json`.[0m[0m
[0m[0m
**Option C: Script reads from a local DuckDB file.**[0m[0m
If a script truly needs SQL access (e.g., complex joins across multiple tables), it connects to a local DuckDB file (`~/shared/data/ps-cache.duckdb`) that the agent populates via MCP exports — never to MotherDuck directly.[0m[0m
[0m[0m
### Scripts That Still Connect to MotherDuck (Need Migration)[0m[0m
[0m[0m
| Script | Current Problem | Fix |[0m[0m
|---|---|---|[0m[0m
| `full_year_project.py` | Reads/writes MotherDuck directly | Agent should run queries via MCP instead |[0m[0m
| `detect_regime_changes.py` | Reads/writes MotherDuck directly | Agent should run queries via MCP instead |[0m[0m
| `wbr_pipeline.py` | Reads/writes MotherDuck directly | Agent should run queries via MCP instead |[0m[0m
| `project.py` | Reads MotherDuck directly | Agent should run queries via MCP instead |[0m[0m
| `backfill_forecasts.py` | Reads/writes MotherDuck directly | Agent should run queries via MCP instead |[0m[0m
| `project_full.py` | Reads/writes MotherDuck directly | Agent should run queries via MCP instead |[0m[0m
[0m[0m
**Migration priority:** Migrate dashboard scripts (`full_year_project.py`, `detect_regime_changes.py`, `wbr_pipeline.py`) first because they run on every `refresh-all.py` cycle. Prediction scripts like `backfill_forecasts.py` run less frequently (weekly or ad-hoc), so they can be migrated incrementally.
#### Scripts With Legacy MotherDuck Connections (to be migrated) — Details

These scripts still have direct `duckdb.connect(md:...)` calls. They work but violate this policy. Migrate as needed:

| Script | Current State | Migration Path |
|--------|--------------|----------------|
| `update-forecast-tracker.py` | Reads from MotherDuck | Already reads xlsx — remove MotherDuck fallback |
| `generate-command-center.py` | Queries MotherDuck | Already rebuilt to use MCP-populated JSON — remove legacy code |
| `refresh-body-system.py` | Queries MotherDuck with cache fallback | Already uses cache — remove MotherDuck attempt |
| `populate_forecast_tracker.py` | Writes to MotherDuck | Agent should run via MCP instead |

## Why This Matters

1. **MotherDuck token management is fragile.** Token expires, env var not set, config not found — every failure mode causes "MotherDuck unavailable" which cascades to skipped EOD phases.
2. **MCP is always available.** If the agent can chat, MCP is connected. No token management needed.
3. **Single point of truth.** MCP config manages the connection once. Scripts don't each need their own connection logic.
4. **Security.** Tokens hardcoded in Python files (prediction/config.py, project_full.py, etc.) are a credential exposure risk.


> **Example:** A typical use of this section involves reading the above rules and applying them to the current context.