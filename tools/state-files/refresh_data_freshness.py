#!/usr/bin/env python3
"""Phase 5: Bulk update data freshness for all synced tables in MotherDuck.

Called at the end of AM-Backend and EOD to record which data sources were refreshed.

Usage:
    python3 refresh_data_freshness.py --sources asana_tasks,calendar_events,emails
    python3 refresh_data_freshness.py --all      # refresh all known sources
    python3 refresh_data_freshness.py --check     # show current freshness status

Requires: duckdb, MOTHERDUCK_TOKEN env var
"""

import argparse
import os
import sys
from datetime import datetime

MD_DB = "md:ps_analytics"

KNOWN_SOURCES = {
    "asana_tasks": {"type": "duckdb_table", "cadence_hours": 12,
                    "workflows": ["am_triage", "portfolio_scan", "daily_tracker"]},
    "calendar_events": {"type": "duckdb_table", "cadence_hours": 12,
                        "workflows": ["am_triage", "daily_brief"]},
    "emails": {"type": "duckdb_table", "cadence_hours": 12,
               "workflows": ["am_triage", "signal_pipeline"]},
    "slack_messages": {"type": "duckdb_table", "cadence_hours": 12,
                       "workflows": ["am_triage", "signal_pipeline", "slack_intelligence"]},
    "signal_tracker": {"type": "duckdb_table", "cadence_hours": 12,
                       "workflows": ["signal_pipeline", "wiki_candidates"]},
    "l1_streak": {"type": "duckdb_table", "cadence_hours": 24,
                  "workflows": ["daily_tracker", "amcc"]},
    "hedy_meetings": {"type": "duckdb_table", "cadence_hours": 24,
                      "workflows": ["meeting_sync", "signal_pipeline"]},
    "ps_metrics": {"type": "motherduck_table", "cadence_hours": 168,
                   "workflows": ["state_file_generation", "callout_pipeline", "wbr_prep"]},
    "loop_pages": {"type": "duckdb_table", "cadence_hours": 12,
                   "workflows": ["loop_sync", "meeting_prep"]},
}


def main():
    parser = argparse.ArgumentParser(description="Update data freshness in MotherDuck")
    parser.add_argument("--sources", help="Comma-separated source names to refresh")
    parser.add_argument("--all", action="store_true", help="Refresh all known sources")
    parser.add_argument("--check", action="store_true", help="Show current freshness status")
    args = parser.parse_args()

    try:
        import duckdb
    except ImportError:
        print("ERROR: duckdb not installed")
        sys.exit(1)

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from md_config import connect_motherduck
    con = connect_motherduck()

    if args.check:
        print("DATA FRESHNESS STATUS:")
        print("-" * 80)
        try:
            rows = con.execute("""
                SELECT source_name, source_type, last_updated, is_stale,
                       expected_cadence_hours,
                       ROUND(EXTRACT(EPOCH FROM (NOW() - last_updated)) / 3600, 1) as hours_ago
                FROM ops.data_freshness
                ORDER BY source_name
            """).fetchall()
            for r in rows:
                status = "🔴 STALE" if r[3] else "🟢 FRESH"
                print(f"  {r[0]}: {status} (updated {r[5]}h ago, cadence {r[4]}h)")
        except Exception as e:
            print(f"  ERROR: {e}")
        con.close()
        return

    if args.all:
        sources = list(KNOWN_SOURCES.keys())
    elif args.sources:
        sources = [s.strip() for s in args.sources.split(",")]
    else:
        print("ERROR: specify --sources or --all")
        sys.exit(1)

    now = datetime.utcnow().isoformat()
    updated = 0

    for source in sources:
        config = KNOWN_SOURCES.get(source)
        if not config:
            print(f"  ⚠️  Unknown source: {source}")
            continue

        try:
            con.execute("""
                INSERT INTO ops.data_freshness
                    (source_name, source_type, expected_cadence_hours,
                     last_updated, last_checked, is_stale, downstream_workflows)
                VALUES (?, ?, ?, ?::TIMESTAMP, ?::TIMESTAMP, false, ?)
                ON CONFLICT (source_name) DO UPDATE SET
                    last_updated = EXCLUDED.last_updated,
                    last_checked = EXCLUDED.last_checked,
                    is_stale = false
            """, [source, config["type"], config["cadence_hours"],
                  now, now, config["workflows"]])
            updated += 1
            print(f"  ✅ {source}")
        except Exception as e:
            print(f"  ❌ {source}: {e}")

    print(f"\n{updated}/{len(sources)} sources refreshed.")
    con.close()


if __name__ == "__main__":
    main()
