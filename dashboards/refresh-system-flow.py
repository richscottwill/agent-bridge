#!/usr/bin/env python3
"""
refresh-system-flow.py — Build system-flow-data.json for System Flow page.

Mirrors refresh-body-system.py's patterns:
  - Fail-loud on missing token (BODY_REFRESH_ALLOW_STALE=1 to opt into cache fallback)
  - Token auto-resolved from env → mcp.json duckdb server
  - Provenance stamp in output JSON (data_source, token_source, generated)

Emitted shapes power the System Flow page's hero stats, freshness pills,
hook bars, and small-multiples. The Sankey topology stays hardcoded in
system-flow.html — it's a structure, not data.

Run: `python3 refresh-system-flow.py` (auto-resolves token from mcp.json)
"""
import json, os, sys
from pathlib import Path
from datetime import datetime, timezone

HOME = Path.home()
OUTPUT = HOME / "shared/dashboards/data/system-flow-data.json"

ALLOW_STALE = (
    "--allow-stale" in sys.argv
    or os.environ.get("BODY_REFRESH_ALLOW_STALE") == "1"
)


def resolve_motherduck_token():
    """env → mcp.json duckdb server. Same pattern as refresh-body-system.py."""
    tok = os.environ.get("MOTHERDUCK_TOKEN") or os.environ.get("motherduck_token")
    if tok:
        return tok, "env"
    mcp_path = HOME / ".kiro/settings/mcp.json"
    if mcp_path.exists():
        try:
            cfg = json.loads(mcp_path.read_text())
            for name, server in (cfg.get("mcpServers") or {}).items():
                if "duck" not in name.lower():
                    continue
                env = server.get("env") or {}
                tok = env.get("motherduck_token") or env.get("MOTHERDUCK_TOKEN")
                if tok:
                    return tok, f"mcp.json:{name}"
        except Exception as e:
            print(f"  Could not read mcp.json: {e}", file=sys.stderr)
    return None, None


def connect():
    """Connect or fail loud. Mirror of refresh-body-system.py query_duckdb logic."""
    try:
        import duckdb as ddb
        token, source = resolve_motherduck_token()
        if not token:
            raise RuntimeError("No MotherDuck token in env or mcp.json")
        con = ddb.connect(f"md:ps_analytics?motherduck_token={token}")
        return con, source
    except Exception as e:
        if ALLOW_STALE:
            print(f"  DuckDB unavailable: {e} (BODY_REFRESH_ALLOW_STALE=1 — cache mode)")
            return None, None
        print(
            f"\n❌ DuckDB unavailable: {e}\n"
            f"   System Flow dashboard depends on live data.\n"
            f"   Fix: export MOTHERDUCK_TOKEN=<token>, or ensure mcp.json has duckdb server.\n"
            f"   Override: BODY_REFRESH_ALLOW_STALE=1 python3 refresh-system-flow.py\n",
            file=sys.stderr,
        )
        sys.exit(2)


def q(con, sql):
    """Run a query, return list of dicts."""
    if con is None:
        return []
    result = con.execute(sql)
    cols = [d[0] for d in result.description]
    return [dict(zip(cols, row)) for row in result.fetchall()]


def main():
    print("=" * 50)
    print("System Flow Data Refresh")
    print("=" * 50)
    con, token_source = connect()
    data_source = "live" if con else "cache"

    # ── Source volumes (last 7 days) ──
    print("\n[1/5] Source volumes...")
    slack = q(con, """
        SELECT COUNT(DISTINCT channel_name) AS channels,
               COUNT(*) AS msgs_7d
        FROM signals.slack_messages
        WHERE TO_TIMESTAMP(CAST(ts AS DOUBLE)) >= CURRENT_TIMESTAMP - INTERVAL '7 days'
    """)
    emails = q(con, """
        SELECT COUNT(*) AS emails_7d
        FROM signals.emails
        WHERE CAST(received_at AS TIMESTAMP) >= CURRENT_TIMESTAMP - INTERVAL '7 days'
    """)
    asana = q(con, """
        SELECT COUNT(*) AS open_tasks FROM asana.asana_tasks WHERE completed = false
    """)
    hedy = q(con, """
        SELECT COUNT(*) AS meetings_30d,
               COUNT(DISTINCT meeting_name) AS series
        FROM signals.hedy_meetings
        WHERE meeting_date >= CURRENT_DATE - INTERVAL '30 days'
    """)
    cal = q(con, """
        SELECT COUNT(*) AS events_7d FROM main.calendar_events
        WHERE start_time >= CURRENT_TIMESTAMP - INTERVAL '7 days'
          AND start_time <= CURRENT_TIMESTAMP + INTERVAL '0 days'
    """) if con else []
    # Fallback: calendar_events schema varies — skip silently if it errors
    if not cal:
        try:
            cal = q(con, """
                SELECT COUNT(*) AS events_7d FROM main.calendar_today
            """)
        except Exception:
            cal = [{"events_7d": 0}]

    schemas = q(con, """
        SELECT table_schema, COUNT(*) AS n
        FROM information_schema.tables
        WHERE table_schema NOT LIKE '%_information_schema'
          AND table_schema NOT LIKE '%_pg_catalog'
          AND table_schema NOT LIKE 'pg_%'
          AND table_schema NOT LIKE 'fts_%'
        GROUP BY 1 ORDER BY n DESC
    """)
    total_tables = sum(s["n"] for s in schemas)

    print(f"  Slack: {slack[0]['channels'] if slack else 0} channels, {slack[0]['msgs_7d'] if slack else 0} msgs/7d")
    print(f"  Email: {emails[0]['emails_7d'] if emails else 0}/7d")
    print(f"  Asana: {asana[0]['open_tasks'] if asana else 0} open")
    print(f"  Hedy: {hedy[0]['meetings_30d'] if hedy else 0} meetings/30d")
    print(f"  Tables: {total_tables} across {len(schemas)} schemas")

    # ── Ingest freshness ──
    print("\n[2/5] Ingest freshness...")
    freshness = q(con, """
        SELECT source_name,
               last_updated::VARCHAR AS last_updated,
               DATE_DIFF('hour', last_updated, CURRENT_TIMESTAMP) AS hours_stale
        FROM ops.data_freshness
        WHERE last_updated IS NOT NULL
          AND source_name IN ('slack_messages', 'emails', 'asana_tasks',
                              'hedy_meetings', 'loop_pages', 'calendar_events',
                              'signal_tracker')
        ORDER BY source_name
    """)
    print(f"  {len(freshness)} source freshness rows")

    # ── Hook reliability (for small-multiples bar chart) ──
    print("\n[3/5] Hook reliability...")
    hooks = q(con, """
        SELECT hook_name, total_runs, total_failures, avg_duration_s,
               last_run::VARCHAR AS last_run,
               DATE_DIFF('day', last_run, CURRENT_DATE) AS days_since_last
        FROM ops.hook_reliability
        ORDER BY total_runs DESC NULLS LAST
        LIMIT 10
    """)
    total_hook_runs = sum(h.get("total_runs") or 0 for h in hooks)
    total_hook_fails = sum(h.get("total_failures") or 0 for h in hooks)
    print(f"  {len(hooks)} hooks, {total_hook_runs} total runs, {total_hook_fails} failures")

    # ── Workflow reliability ──
    print("\n[4/5] Workflow reliability...")
    workflows = q(con, """
        SELECT workflow_name, total_runs, successes,
               success_rate, avg_duration_s,
               DATE_DIFF('day', last_run, CURRENT_DATE) AS days_since_last
        FROM ops.workflow_reliability
        ORDER BY total_runs DESC NULLS LAST
        LIMIT 10
    """)
    print(f"  {len(workflows)} workflows")

    # ── Assemble ──
    print("\n[5/5] Assembling JSON...")
    output = {
        "generated": datetime.now(tz=timezone.utc).isoformat(),
        "data_source": data_source,
        "token_source": token_source or "none",
        "sources": {
            "slack": {
                "channels": slack[0]["channels"] if slack else 0,
                "msgs_7d": slack[0]["msgs_7d"] if slack else 0,
            },
            "emails_7d": emails[0]["emails_7d"] if emails else 0,
            "asana_open": asana[0]["open_tasks"] if asana else 0,
            "hedy_30d": hedy[0]["meetings_30d"] if hedy else 0,
            "hedy_series": hedy[0]["series"] if hedy else 0,
            "calendar_7d": cal[0]["events_7d"] if cal else 0,
            "motherduck_tables": total_tables,
            "motherduck_schemas": len(schemas),
            "schema_breakdown": [
                {"name": s["table_schema"], "n": s["n"]}
                for s in schemas[:10]
            ],
        },
        "freshness": freshness,
        "hooks": [
            {
                "name": h["hook_name"],
                "runs": h.get("total_runs") or 0,
                "failures": h.get("total_failures") or 0,
                "avg_duration_s": h.get("avg_duration_s"),
                "days_since_last": h.get("days_since_last"),
                "last_run": h.get("last_run"),
            }
            for h in hooks
        ],
        "workflows": [
            {
                "name": w["workflow_name"],
                "runs": w.get("total_runs") or 0,
                "successes": w.get("successes") or 0,
                "success_rate": w.get("success_rate"),
                "avg_duration_s": w.get("avg_duration_s"),
                "days_since_last": w.get("days_since_last"),
            }
            for w in workflows
        ],
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nWritten: {OUTPUT}")
    print(f"Source: {data_source} · token: {token_source or 'none'}")


if __name__ == "__main__":
    main()
