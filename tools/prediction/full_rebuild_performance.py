#!/usr/bin/env python3
"""
Full rebuild of ps.performance from the canonical source (WW Dashboard xlsx Daily tabs).

Why: The ingester's monthly_actuals section returned MTD-schema-drifted rows
that landed as corrupted monthly rows in ps.performance (regs field holding
spend values). Quarterly and WW aggregates inherited the corruption.

Fix: Re-ingest the full daily history from the xlsx, then derive weekly,
monthly, quarterly from the daily table. This makes daily the single source
and guarantees the grains are internally consistent.

Usage:
    python3 full_rebuild_performance.py <path_to_xlsx>

Safeguards (so agents can't accidentally sum across grains):
- Canonical views: ps.v_daily, ps.v_weekly, ps.v_monthly, ps.v_quarterly
- Grain coverage view: ps.v_grain_coverage
- period_type is always a required filter; base table reads need an explicit
  period_type='x' clause.
"""

import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Set up path to reuse ingester helpers
sys.path.insert(0, os.path.expanduser('~/shared/tools/dashboard-ingester'))
sys.path.insert(0, os.path.expanduser('~/shared/tools'))

from ingest import DashboardIngester, ALL_MARKETS  # reuse the Daily tab reader


def connect_motherduck():
    import duckdb
    token = os.environ.get('MOTHERDUCK_TOKEN') or os.environ.get('motherduck_token')
    if not token:
        # Read from Kiro MCP config as fallback
        import json
        cfg_path = os.path.expanduser('~/.kiro/settings/mcp.json')
        if os.path.exists(cfg_path):
            with open(cfg_path) as f:
                cfg = json.load(f)
            duckdb_cfg = cfg.get('mcpServers', {}).get('duckdb', {})
            env = duckdb_cfg.get('env', {})
            token = env.get('motherduck_token') or env.get('MOTHERDUCK_TOKEN')
    if not token:
        # Fall back to hardcoded (same as prediction/config.py)
        from prediction.config import MOTHERDUCK_TOKEN
        token = MOTHERDUCK_TOKEN
    con = duckdb.connect(f'md:ps_analytics?motherduck_token={token}')
    return con


def iso_week_key(date_str):
    """Return ISO week key like '2026-W16' from 'YYYY-MM-DD'.

    NOTE: This is ISO (Mon-Sun) week math, which differs from the AB WW Dashboard
    which uses Sun-Sat weeks. Prefer xlsx_week_key when the daily row carries
    its own xlsx week label — it matches the dashboard's weekly aggregation.
    """
    d = datetime.strptime(date_str, '%Y-%m-%d').date()
    y, w, _ = d.isocalendar()
    return f'{y}-W{w}'


def xlsx_week_key(xlsx_week_label):
    """Normalize an xlsx week label like '2026 W16' to '2026-W16' (dashboard convention).

    The AB dashboard marks weeks as Sun-Sat and labels them e.g. '2026 W16' where
    Sun Apr 12 2026 is the start of W16. ISO calendar would put Sun Apr 12 in W15
    (Mon-Sun). Using the xlsx label preserves agreement with the dashboard's own
    Weekly tab aggregates.
    """
    if not xlsx_week_label:
        return None
    parts = xlsx_week_label.strip().split()
    if len(parts) != 2:
        return None
    return f'{parts[0]}-{parts[1]}'


def month_key(date_str):
    """Return '2026-M04' for '2026-04-14'."""
    d = datetime.strptime(date_str, '%Y-%m-%d').date()
    return f'{d.year}-M{d.month:02d}'


def quarter_key(date_str):
    """Return '2026-Q2' for '2026-04-14'."""
    d = datetime.strptime(date_str, '%Y-%m-%d').date()
    q = (d.month - 1) // 3 + 1
    return f'{d.year}-Q{q}'


def ratio(num, den):
    if num is None or den is None or den == 0:
        return None
    return num / den


PERF_COLS = (
    'market', 'period_type', 'period_key', 'period_start',
    'registrations', 'cost', 'cpa', 'clicks', 'impressions', 'cpc', 'cvr', 'ctr',
    'brand_registrations', 'brand_cost', 'brand_cpa', 'brand_clicks', 'brand_cpc', 'brand_cvr',
    'nb_registrations', 'nb_cost', 'nb_cpa', 'nb_clicks', 'nb_cpc', 'nb_cvr',
    'ieccp', 'source'
)

PERF_SQL = f"""INSERT OR REPLACE INTO ps.performance ({', '.join(PERF_COLS)})
    VALUES ({', '.join(['?'] * len(PERF_COLS))})"""


def build_row(market, period_type, period_key, period_start, agg, source):
    """Assemble a ps.performance row tuple from an aggregated dict."""
    regs = int(agg['regs']) if agg['regs'] is not None else None
    cost = agg['cost']
    clicks = int(agg['clicks']) if agg['clicks'] is not None else None
    imps = int(agg['impressions']) if agg['impressions'] is not None else None
    b_regs = int(agg['brand_regs']) if agg['brand_regs'] is not None else None
    b_cost = agg['brand_cost']
    b_clicks = int(agg['brand_clicks']) if agg['brand_clicks'] is not None else None
    nb_regs = int(agg['nb_regs']) if agg['nb_regs'] is not None else None
    nb_cost = agg['nb_cost']
    nb_clicks = int(agg['nb_clicks']) if agg['nb_clicks'] is not None else None

    return (
        market, period_type, period_key, period_start,
        regs, cost, ratio(cost, regs), clicks, imps,
        ratio(cost, clicks), ratio(regs, clicks), ratio(clicks, imps),
        b_regs, b_cost, ratio(b_cost, b_regs), b_clicks,
        ratio(b_cost, b_clicks), ratio(b_regs, b_clicks),
        nb_regs, nb_cost, ratio(nb_cost, nb_regs), nb_clicks,
        ratio(nb_cost, nb_clicks), ratio(nb_regs, nb_clicks),
        None, source,
    )


def aggregate(days, key_fn, key_arg='date'):
    """Bucket a list of day dicts by key_fn(value); return dict keyed by bucket.

    key_arg selects which day field to pass to key_fn:
      - 'date' for calendar-derived keys (month, quarter)
      - 'week' for the xlsx week label (preserves dashboard Sun-Sat weeks)
    """
    buckets = {}
    for d in days:
        raw = d.get(key_arg)
        k = key_fn(raw)
        if k is None:
            continue
        b = buckets.setdefault(k, {
            'regs': 0, 'cost': 0.0, 'clicks': 0, 'impressions': 0,
            'brand_regs': 0, 'brand_cost': 0.0, 'brand_clicks': 0,
            'nb_regs': 0, 'nb_cost': 0.0, 'nb_clicks': 0,
            'first_date': d['date'], 'last_date': d['date'],
        })
        b['regs'] += d.get('regs', 0) or 0
        b['cost'] += d.get('cost', 0) or 0.0
        b['clicks'] += d.get('clicks', 0) or 0
        b['impressions'] += d.get('impressions', 0) or 0
        b['brand_regs'] += d.get('brand_regs', 0) or 0
        b['brand_cost'] += d.get('brand_cost', 0) or 0.0
        b['brand_clicks'] += d.get('brand_clicks', 0) or 0
        b['nb_regs'] += d.get('nb_regs', 0) or 0
        b['nb_cost'] += d.get('nb_cost', 0) or 0.0
        b['nb_clicks'] += d.get('nb_clicks', 0) or 0
        if d['date'] < b['first_date']:
            b['first_date'] = d['date']
        if d['date'] > b['last_date']:
            b['last_date'] = d['date']
    return buckets


def quarter_start(q_key):
    """'2026-Q2' → '2026-04-01'."""
    year, q = q_key.split('-Q')
    start_month = (int(q) - 1) * 3 + 1
    return f'{year}-{start_month:02d}-01'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('xlsx_path', help='Path to WW Dashboard xlsx')
    parser.add_argument('--dry-run', action='store_true', help='Print summary, do not write')
    args = parser.parse_args()

    if not os.path.exists(args.xlsx_path):
        print(f'ERROR: xlsx not found: {args.xlsx_path}')
        sys.exit(1)

    print(f'Reading {args.xlsx_path}...')
    analyzer = DashboardIngester(args.xlsx_path)

    source = os.path.basename(args.xlsx_path)

    # Per-market daily data — read the full Daily tab for each market
    all_days_per_market = {}
    for market in ALL_MARKETS:
        days = analyzer._read_daily_tab(market)
        # Filter out rows with no registrations or cost (empty/future)
        days = [d for d in days if d.get('regs', 0) > 0 or d.get('cost', 0) > 0]
        all_days_per_market[market] = days
        if days:
            print(f'  {market}: {len(days)} days ({days[0]["date"]} → {days[-1]["date"]})')
        else:
            print(f'  {market}: 0 days (no data)')

    total_daily_rows = sum(len(v) for v in all_days_per_market.values())
    print(f'\nTotal daily rows to write: {total_daily_rows}')

    if args.dry_run:
        print('Dry run — stopping before DB write.')
        return

    # Connect to MotherDuck
    print('\nConnecting to MotherDuck...')
    con = connect_motherduck()

    # Wipe all ps.performance rows. A clean rebuild.
    print('Wiping ps.performance (full rebuild)...')
    con.execute('DELETE FROM ps.performance')
    con.commit()

    daily_written = 0
    weekly_written = 0
    monthly_written = 0
    quarterly_written = 0

    # Collect all rows as tuples, then bulk-insert via executemany for MotherDuck speed
    daily_rows = []
    weekly_rows = []
    monthly_rows = []
    quarterly_rows = []

    # ── Daily + weekly + monthly + quarterly per market ──
    for market in ALL_MARKETS:
        days = all_days_per_market[market]
        if not days:
            continue

        # Daily rows
        for d in days:
            agg = {
                'regs': d.get('regs', 0),
                'cost': d.get('cost', 0.0),
                'clicks': d.get('clicks', 0),
                'impressions': d.get('impressions', 0),
                'brand_regs': d.get('brand_regs', 0),
                'brand_cost': d.get('brand_cost', 0.0),
                'brand_clicks': d.get('brand_clicks', 0),
                'nb_regs': d.get('nb_regs', 0),
                'nb_cost': d.get('nb_cost', 0.0),
                'nb_clicks': d.get('nb_clicks', 0),
            }
            daily_rows.append(build_row(market, 'daily', d['date'], d['date'], agg, source))

        # Weekly rows — aggregate daily by xlsx week label (dashboard's Sun-Sat convention)
        weekly_buckets = aggregate(days, xlsx_week_key, key_arg='week')
        for wk_key, b in weekly_buckets.items():
            weekly_rows.append(build_row(market, 'weekly', wk_key, b['first_date'], b, source))

        # Monthly rows — aggregate daily by calendar month
        monthly_buckets = aggregate(days, month_key, key_arg='date')
        for m_key, b in monthly_buckets.items():
            year, m = m_key.split('-M')
            month_start = f'{year}-{int(m):02d}-01'
            monthly_rows.append(build_row(market, 'monthly', m_key, month_start, b, source))

        # Quarterly rows — aggregate daily by calendar quarter
        quarterly_buckets = aggregate(days, quarter_key, key_arg='date')
        for q_key, b in quarterly_buckets.items():
            quarterly_rows.append(build_row(market, 'quarterly', q_key, quarter_start(q_key), b, source))

    # Bulk insert all rows using DuckDB's native DataFrame loader (much faster than
    # parameterized executemany which does one round-trip per row to MotherDuck)
    print(f'\nBulk-inserting: {len(daily_rows)} daily, {len(weekly_rows)} weekly, {len(monthly_rows)} monthly, {len(quarterly_rows)} quarterly...')
    import pandas as pd
    col_names = list(PERF_COLS)

    def bulk_insert(rows, grain_label):
        if not rows:
            return 0
        df = pd.DataFrame(rows, columns=col_names)
        # Register as temp view and INSERT via SELECT — MotherDuck handles this in one round-trip
        # Explicitly list columns to avoid column-count mismatch with period_end/updated_at etc.
        con.register('_tmp_rows', df)
        col_list = ', '.join(col_names)
        con.execute(f"INSERT OR REPLACE INTO ps.performance ({col_list}) SELECT {col_list} FROM _tmp_rows")
        con.unregister('_tmp_rows')
        print(f'  {grain_label}: {len(rows)} rows inserted')
        return len(rows)

    daily_written = bulk_insert(daily_rows, 'Daily')
    weekly_written = bulk_insert(weekly_rows, 'Weekly')
    monthly_written = bulk_insert(monthly_rows, 'Monthly')
    quarterly_written = bulk_insert(quarterly_rows, 'Quarterly')
    con.commit()

    print(f'\nPer-market writes: {daily_written} daily, {weekly_written} weekly, {monthly_written} monthly, {quarterly_written} quarterly')

    # ── WW aggregate at every grain ──
    # Sum the 10 markets at matching (period_type, period_key) and insert as
    # market='WW'. Same grain-filter discipline so cross-grain summing is
    # impossible via ps.v_{grain} views.
    print('Building WW aggregate at every grain...')
    ww_inserted = 0
    for grain in ('daily', 'weekly', 'monthly', 'quarterly'):
        n = con.execute(f"""
            INSERT OR REPLACE INTO ps.performance
            (market, period_type, period_key, period_start,
             registrations, cost, cpa, clicks, impressions, cpc, cvr, ctr,
             brand_registrations, brand_cost, brand_cpa, brand_clicks, brand_cpc, brand_cvr,
             nb_registrations, nb_cost, nb_cpa, nb_clicks, nb_cpc, nb_cvr,
             ieccp, source)
            SELECT
                'WW' AS market,
                period_type, period_key, MIN(period_start) AS period_start,
                SUM(registrations), SUM(cost),
                CASE WHEN SUM(registrations) > 0 THEN SUM(cost) / SUM(registrations) END,
                SUM(clicks), SUM(impressions),
                CASE WHEN SUM(clicks) > 0 THEN SUM(cost) / SUM(clicks) END,
                CASE WHEN SUM(clicks) > 0 THEN CAST(SUM(registrations) AS DOUBLE) / SUM(clicks) END,
                CASE WHEN SUM(impressions) > 0 THEN CAST(SUM(clicks) AS DOUBLE) / SUM(impressions) END,
                SUM(brand_registrations), SUM(brand_cost),
                CASE WHEN SUM(brand_registrations) > 0 THEN SUM(brand_cost) / SUM(brand_registrations) END,
                SUM(brand_clicks),
                CASE WHEN SUM(brand_clicks) > 0 THEN SUM(brand_cost) / SUM(brand_clicks) END,
                CASE WHEN SUM(brand_clicks) > 0 THEN CAST(SUM(brand_registrations) AS DOUBLE) / SUM(brand_clicks) END,
                SUM(nb_registrations), SUM(nb_cost),
                CASE WHEN SUM(nb_registrations) > 0 THEN SUM(nb_cost) / SUM(nb_registrations) END,
                SUM(nb_clicks),
                CASE WHEN SUM(nb_clicks) > 0 THEN SUM(nb_cost) / SUM(nb_clicks) END,
                CASE WHEN SUM(nb_clicks) > 0 THEN CAST(SUM(nb_registrations) AS DOUBLE) / SUM(nb_clicks) END,
                NULL, 'ww_rollup'
            FROM ps.performance
            WHERE period_type = '{grain}' AND market IN ({','.join([f"'{m}'" for m in ALL_MARKETS])})
            GROUP BY period_type, period_key
        """).fetchone()
        count = con.execute(f"SELECT COUNT(*) FROM ps.performance WHERE market='WW' AND period_type='{grain}'").fetchone()[0]
        ww_inserted += count
        print(f'  WW {grain}: {count} rows')

    # ── Refresh canonical views ──
    print('\nRefreshing views...')
    for grain in ('daily', 'weekly', 'monthly', 'quarterly'):
        con.execute(f"""
            CREATE OR REPLACE VIEW ps.v_{grain} AS
            SELECT * FROM ps.performance WHERE period_type = '{grain}'
        """)
    con.execute("""
        CREATE OR REPLACE VIEW ps.v_grain_coverage AS
        SELECT market, period_type,
               COUNT(*) AS rows,
               MIN(period_key) AS first_key,
               MAX(period_key) AS last_key,
               MIN(period_start) AS first_date,
               MAX(period_start) AS last_date
        FROM ps.performance
        GROUP BY market, period_type
        ORDER BY market, period_type
    """)
    print('  ps.v_daily, ps.v_weekly, ps.v_monthly, ps.v_quarterly, ps.v_grain_coverage')

    total = daily_written + weekly_written + monthly_written + quarterly_written + ww_inserted
    print(f'\nDone. Total rows written: {total}')
    print(f'  Per-market: {daily_written}d + {weekly_written}w + {monthly_written}m + {quarterly_written}q')
    print(f'  WW aggregate: {ww_inserted}')

    con.close()


if __name__ == '__main__':
    main()
