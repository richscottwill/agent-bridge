#!/usr/bin/env python3
"""Step 2D.5: Sync daily_metrics from local DuckDB → ps.metrics on MotherDuck.

Aggregates daily_metrics into weekly summaries for any weeks missing from
ps.metrics. Writes to both ps.metrics (EAV) and ps.weekly_actuals (wide).

Usage:
    python3 sync_metrics.py                    # dry-run (show what would sync)
    python3 sync_metrics.py --execute          # actually write to MotherDuck
    python3 sync_metrics.py --execute --weeks 2026-W10 2026-W11  # specific weeks only

Requires: duckdb, MOTHERDUCK_TOKEN env var (or existing MotherDuck auth)
"""

import argparse
import os
import sys
from datetime import datetime

LOCAL_DB = os.path.expanduser("~/shared/data/duckdb/ps-analytics.duckdb")
MD_DB = "md:ps_analytics"

MARKETS = ["US", "CA", "UK", "DE", "FR", "IT", "ES", "JP", "AU", "MX"]

METRIC_UNITS = {
    "registrations": "count", "brand_registrations": "count", "nb_registrations": "count",
    "cost": "USD", "brand_cost": "USD", "nb_cost": "USD",
    "clicks": "count", "brand_clicks": "count", "nb_clicks": "count",
    "impressions": "count",
    "cpa": "USD", "brand_cpa": "USD", "nb_cpa": "USD",
    "cpc": "USD", "brand_cpc": "USD", "nb_cpc": "USD",
    "cvr": "ratio", "brand_cvr": "ratio", "nb_cvr": "ratio",
    "ctr": "ratio",
}


def safe_div(a, b):
    if b and b > 0:
        return a / b
    return None


def find_missing_weeks(local_con, md_con):
    """Find weeks with daily data in local DB but no weekly data in MotherDuck."""
    local_weeks = local_con.execute(
        "SELECT DISTINCT week FROM daily_metrics WHERE week LIKE '2026%' ORDER BY week"
    ).fetchall()
    local_weeks = {r[0] for r in local_weeks}

    md_weeks = md_con.execute(
        "SELECT DISTINCT period_key FROM ps.metrics WHERE period_type='weekly' AND period_key LIKE '2026%'"
    ).fetchall()
    md_weeks = {r[0] for r in md_weeks}

    # Normalize week format: local uses "2026 W10", MotherDuck uses "2026-W10"
    def normalize(w):
        return w.replace(" ", "-")

    local_normalized = {normalize(w): w for w in local_weeks}
    md_normalized = {normalize(w) for w in md_weeks}

    missing = []
    for norm_key, orig_key in sorted(local_normalized.items()):
        if norm_key not in md_normalized:
            missing.append((norm_key, orig_key))

    return missing


def aggregate_week(local_con, market, week_local_fmt):
    """Aggregate daily_metrics for a market+week into 20 weekly metrics."""
    rows = local_con.execute("""
        SELECT
            SUM(regs) as regs,
            SUM(cost) as cost,
            SUM(clicks) as clicks,
            SUM(impressions) as impressions,
            SUM(brand_regs) as brand_regs,
            SUM(brand_cost) as brand_cost,
            SUM(brand_clicks) as brand_clicks,
            SUM(brand_imp) as brand_imp,
            SUM(nb_regs) as nb_regs,
            SUM(nb_cost) as nb_cost,
            SUM(nb_clicks) as nb_clicks,
            SUM(nb_imp) as nb_imp,
            MIN(date) as week_start,
            MAX(date) as week_end,
            COUNT(*) as days
        FROM daily_metrics
        WHERE market = ? AND week = ?
    """, [market, week_local_fmt]).fetchone()

    if not rows or not rows[0]:
        return None

    regs, cost, clicks, imps = rows[0], rows[1], rows[2], rows[3]
    brand_regs, brand_cost, brand_clicks = rows[4], rows[5], rows[6]
    nb_regs, nb_cost, nb_clicks = rows[8], rows[9], rows[10]
    week_start, week_end, days = rows[12], rows[13], rows[14]

    metrics = {
        "registrations": regs,
        "cost": cost,
        "clicks": clicks,
        "impressions": imps,
        "brand_registrations": brand_regs,
        "brand_cost": brand_cost,
        "brand_clicks": brand_clicks,
        "nb_registrations": nb_regs,
        "nb_cost": nb_cost,
        "nb_clicks": nb_clicks,
        "cpa": safe_div(cost, regs),
        "cpc": safe_div(cost, clicks),
        "cvr": safe_div(regs, clicks),
        "ctr": safe_div(clicks, imps),
        "brand_cpa": safe_div(brand_cost, brand_regs),
        "brand_cpc": safe_div(brand_cost, brand_clicks),
        "brand_cvr": safe_div(brand_regs, brand_clicks),
        "nb_cpa": safe_div(nb_cost, nb_regs),
        "nb_cpc": safe_div(nb_cost, nb_clicks),
        "nb_cvr": safe_div(nb_regs, nb_clicks),
    }

    return {
        "metrics": metrics,
        "week_start": week_start,
        "week_end": week_end,
        "days": days,
    }


def write_to_motherduck(md_con, market, period_key, agg):
    """Write aggregated metrics to ps.metrics (EAV) and ps.weekly_actuals (wide)."""
    now = datetime.utcnow().isoformat()
    metrics = agg["metrics"]
    week_start = agg["week_start"]
    week_end = agg["week_end"]

    # ps.metrics — EAV format (one row per metric)
    for metric_name, value in metrics.items():
        if value is None:
            continue
        metric_id = f"{market}-ps-{metric_name}-weekly-{period_key}"
        unit = METRIC_UNITS.get(metric_name, "")
        md_con.execute("""
            INSERT INTO ps.metrics (metric_id, market, channel, metric_name, period_type,
                period_key, period_start, period_end, actual_value, currency_code, unit, source, updated_at)
            VALUES (?, ?, 'ps', ?, 'weekly', ?, ?::DATE, ?::DATE, ?, 'USD', ?, 'sync_metrics.py', ?::TIMESTAMP)
            ON CONFLICT (metric_id) DO UPDATE SET
                actual_value = EXCLUDED.actual_value,
                updated_at = EXCLUDED.updated_at
        """, [metric_id, market, metric_name, period_key, week_start, week_end,
              value, unit, now])

    # ps.weekly_actuals — wide format (cost + registrations)
    for metric_name in ["cost", "registrations"]:
        value = metrics.get(metric_name if metric_name != "cost" else "cost")
        if metric_name == "registrations":
            value = metrics.get("registrations")
        if value is None:
            continue
        md_con.execute("""
            INSERT INTO ps.weekly_actuals (market, channel, metric_name, week_num, period_key, week_start, value, source)
            VALUES (?, 'ps', ?, ?, ?, ?, ?, 'sync_metrics.py')
            ON CONFLICT DO NOTHING
        """, [market, metric_name, int(period_key.split("-W")[1]),
              period_key, week_start, value])


def main():
    parser = argparse.ArgumentParser(description="Sync daily_metrics → ps.metrics on MotherDuck")
    parser.add_argument("--execute", action="store_true", help="Actually write (default: dry-run)")
    parser.add_argument("--weeks", nargs="*", help="Specific weeks to sync (e.g., 2026-W10 2026-W11)")
    args = parser.parse_args()

    try:
        import duckdb
    except ImportError:
        print("ERROR: duckdb not installed. pip install duckdb")
        sys.exit(1)

    if not os.path.exists(LOCAL_DB):
        print(f"ERROR: Local DB not found at {LOCAL_DB}")
        sys.exit(1)

    local_con = duckdb.connect(LOCAL_DB, read_only=True)
    
    # Use shared config for MotherDuck auth
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from md_config import connect_motherduck
    md_con = connect_motherduck()

    # Find missing weeks
    if args.weeks:
        missing = [(w, w.replace("-", " ")) for w in args.weeks]
        print(f"Syncing specified weeks: {', '.join(args.weeks)}")
    else:
        missing = find_missing_weeks(local_con, md_con)
        print(f"Found {len(missing)} weeks with daily data not yet in ps.metrics")

    if not missing:
        print("Nothing to sync.")
        local_con.close()
        md_con.close()
        return

    total_metrics = 0
    for period_key, local_fmt in missing:
        print(f"\n  {period_key}:")
        for market in MARKETS:
            agg = aggregate_week(local_con, market, local_fmt)
            if not agg:
                continue
            non_null = sum(1 for v in agg["metrics"].values() if v is not None)
            regs = agg["metrics"].get("registrations", 0)
            cost = agg["metrics"].get("cost", 0)
            print(f"    {market}: {int(regs or 0)} regs, ${int(cost or 0):,} cost, {non_null} metrics, {agg['days']}d")

            if args.execute:
                write_to_motherduck(md_con, market, period_key, agg)
                total_metrics += non_null

    if args.execute:
        # Update data freshness
        now = datetime.utcnow().isoformat()
        md_con.execute("""
            INSERT INTO ops.data_freshness (source_name, source_type, expected_cadence_hours,
                last_updated, last_checked, is_stale, downstream_workflows)
            VALUES ('ps_metrics', 'motherduck_table', 168, ?::TIMESTAMP, ?::TIMESTAMP, false,
                ARRAY['state_file_generation', 'callout_pipeline', 'wbr_prep'])
            ON CONFLICT (source_name) DO UPDATE SET
                last_updated = EXCLUDED.last_updated, last_checked = EXCLUDED.last_checked, is_stale = false
        """, [now, now])

        # Log workflow execution
        md_con.execute("""
            INSERT INTO ops.workflow_executions (workflow_name, start_time, status, notes)
            VALUES ('sync_metrics', ?::TIMESTAMP, 'completed',
                ?)
        """, [now, f"Synced {len(missing)} weeks, {total_metrics} metric rows"])

        print(f"\n✅ Synced {total_metrics} metric rows across {len(missing)} weeks to MotherDuck")
    else:
        print(f"\n🔍 DRY RUN — would sync {len(missing)} weeks. Use --execute to write.")

    local_con.close()
    md_con.close()


if __name__ == "__main__":
    main()
