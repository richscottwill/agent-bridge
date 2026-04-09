#!/usr/bin/env python3
"""Backfill historical forecasts for W1-W14 2026, all 10 markets.

Generates "what would we have predicted" forecasts using BayesianProjector,
then scores them against actuals in ps.performance. Establishes a calibration
baseline for the prediction engine.

Usage:
    python3 backfill_forecasts.py
"""

import sys
import os
import traceback
from datetime import datetime, timedelta

# Ensure sibling packages are importable
sys.path.insert(0, os.path.expanduser('~/shared/tools'))
sys.path.insert(0, os.path.expanduser('~/shared/tools/prediction'))

from prediction.core import BayesianCore
from prediction.ptypes import SegmentForecast, MarketProjection

ALL_MARKETS = ['AU', 'MX', 'US', 'CA', 'JP', 'UK', 'DE', 'FR', 'IT', 'ES']

# Week period_start dates for 2026 W1-W14 (Monday of each week)
WEEK_STARTS = {
    1: '2025-12-29', 2: '2026-01-05', 3: '2026-01-12', 4: '2026-01-19',
    5: '2026-01-26', 6: '2026-02-02', 7: '2026-02-09', 8: '2026-02-16',
    9: '2026-02-23', 10: '2026-03-02', 11: '2026-03-09', 12: '2026-03-16',
    13: '2026-03-23', 14: '2026-03-30',
}


def connect():
    """Open MotherDuck connection."""
    import duckdb
    token = os.environ.get('MOTHERDUCK_TOKEN',
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJpY2hzY290dHdpbGxAZ21haWwuY29tIiwibWRSZWdpb24iOiJhd3MtdXMtZWFzdC0xIiwic2Vzc2lvbiI6InJpY2hzY290dHdpbGwuZ21haWwuY29tIiwicGF0IjoiVDNIYzFVQWYzT3o1bjVkLS03ckdHNlBjMlpUdVNNbFItT3RXMS1qNzVPUSIsInVzZXJJZCI6ImU2MDhlNDZiLTE4YzctNGE5Ny04M2I2LWE0N2ZhOThmNjBhYyIsImlzcyI6Im1kX3BhdCIsInJlYWRPbmx5IjpmYWxzZSwidG9rZW5UeXBlIjoicmVhZF93cml0ZSIsImlhdCI6MTc3NTQ0MzY0N30.tS0Cab3FQ8_CDZ1PqOo9z09KYHEUFHwuLVXRQrxcHig')
    return duckdb.connect(f'md:ps_analytics?motherduck_token={token}')


def fetch_all_weekly_history(con, market):
    """Fetch ALL weekly history for a market, ordered by period_start ASC."""
    rows = con.execute(f"""
        SELECT period_key, period_start,
               registrations, cost, cpa, clicks, impressions, cpc, cvr, ctr,
               brand_registrations, brand_cost, brand_cpa, brand_clicks, brand_cpc, brand_cvr,
               nb_registrations, nb_cost, nb_cpa, nb_clicks, nb_cpc, nb_cvr,
               ieccp
        FROM ps.performance
        WHERE market = '{market}' AND period_type = 'weekly'
        ORDER BY period_start ASC
    """).fetchall()
    cols = [
        'period_key', 'period_start',
        'regs', 'cost', 'cpa', 'clicks', 'impressions', 'cpc', 'cvr', 'ctr',
        'brand_regs', 'brand_cost', 'brand_cpa', 'brand_clicks', 'brand_cpc', 'brand_cvr',
        'nb_regs', 'nb_cost', 'nb_cpa', 'nb_clicks', 'nb_cpc', 'nb_cvr',
        'ieccp',
    ]
    return [dict(zip(cols, r)) for r in rows]


def week_num_from_key(pk):
    """Extract week number from period_key like '2026-W5' or '2025-W52'."""
    try:
        return int(pk.split('-W')[1])
    except (IndexError, ValueError):
        return 0


def project_from_history(core, history_slice, segment_prefix, seasonal_adj):
    """Project a segment (brand_ or nb_) from a pre-sliced history list.

    history_slice: list of dicts, most recent FIRST (reversed from ASC order).
    """
    metric_key = f'{segment_prefix}regs'
    hist_for_core = [{'value': float(w.get(metric_key, 0) or 0)} for w in reversed(history_slice)]

    if not hist_for_core or all(h['value'] == 0 for h in hist_for_core):
        return SegmentForecast(regs=0, cost=0, cpa=0, clicks=0)

    prior = core.build_prior(hist_for_core, 'value')
    # Use last 4 weeks as recent evidence
    recent = [{'value': float(w.get(metric_key, 0) or 0)} for w in history_slice[:4]]
    posterior = core.update_posterior(prior, recent, 1.0)

    base_regs = core.point_estimate(posterior, horizon=1)
    adj_regs = max(0, base_regs * seasonal_adj)

    # Cost: recent avg CPA ratio
    recent_costs = [float(w.get(f'{segment_prefix}cost', 0) or 0) for w in history_slice[:8]]
    recent_regs = [float(w.get(metric_key, 0) or 0) for w in history_slice[:8]]
    total_cost = sum(recent_costs)
    total_regs = sum(recent_regs)
    avg_cpa = total_cost / total_regs if total_regs > 0 else 0
    adj_cost = adj_regs * avg_cpa

    adj_cpa = adj_cost / adj_regs if adj_regs > 0 else 0

    return SegmentForecast(
        regs=round(adj_regs),
        cost=round(adj_cost, 2),
        cpa=round(adj_cpa, 2),
        clicks=0,
    )



def backfill_weekly(con, core):
    """Generate weekly backfill forecasts for W1-W14 2026, all markets."""
    print("\n=== WEEKLY BACKFILL: W1-W14 2026 ===\n")
    written = 0
    skipped = 0

    for market in ALL_MARKETS:
        all_history = fetch_all_weekly_history(con, market)
        if len(all_history) < 5:
            print(f"  {market}: insufficient history ({len(all_history)} weeks), skipping")
            continue

        # Fetch seasonal priors
        seasonal_rows = con.execute(f"""
            SELECT week_of_year, seasonal_index FROM ps.seasonal_priors
            WHERE market = '{market}'
        """).fetchall()
        seasonal = {int(r[0]): float(r[1]) for r in seasonal_rows}

        # Build index: find where 2026 weeks start in the sorted history
        # all_history is ASC by period_start
        week_index = {}
        for i, w in enumerate(all_history):
            week_index[w['period_key']] = i

        for target_wk in range(1, 15):
            target_pk = f"2026-W{target_wk}"

            # Check if forecast already exists
            existing = con.execute(f"""
                SELECT COUNT(*) FROM ps.forecasts
                WHERE market = '{market}' AND target_period = '{target_pk}'
                AND method = 'bayesian_backfill'
            """).fetchone()
            if existing and existing[0] > 0:
                skipped += 4
                continue

            # Slice history: only weeks BEFORE the target week
            target_idx = week_index.get(target_pk)
            if target_idx is None:
                continue

            # Everything before target_idx, reversed so most recent first
            history_before = list(reversed(all_history[:target_idx]))

            if len(history_before) < 3:
                continue

            # Seasonal adjustment
            seasonal_adj = seasonal.get(target_wk % 52, 1.0) if seasonal else 1.0

            # Project brand + nb
            brand = project_from_history(core, history_before, 'brand_', seasonal_adj)
            nb = project_from_history(core, history_before, 'nb_', seasonal_adj)

            total_regs = brand.regs + nb.regs
            total_cost = brand.cost + nb.cost

            if total_regs == 0:
                continue

            # CI from total regs posterior
            hist_for_ci = [{'value': float(w.get('regs', 0) or 0)} for w in reversed(history_before)]
            prior = core.build_prior(hist_for_ci, 'value')
            recent = [{'value': float(w.get('regs', 0) or 0)} for w in history_before[:4]]
            posterior = core.update_posterior(prior, recent, 1.0)
            ci_low, ci_high = core.credible_interval(posterior, level=0.7)
            ci_low = max(0, ci_low * seasonal_adj)
            ci_high = ci_high * seasonal_adj

            # forecast_date = Monday of the PRIOR week (simulating when we'd predict)
            if target_wk == 1:
                forecast_date = '2025-12-22'  # Week before W1
            else:
                prior_wk_start = WEEK_STARTS.get(target_wk - 1, WEEK_STARTS.get(target_wk))
                forecast_date = prior_wk_start

            # Write 4 metric rows
            metrics = [
                ('registrations', total_regs, ci_low, ci_high),
                ('cost', total_cost, None, None),
                ('brand_regs', brand.regs, None, None),
                ('nb_regs', nb.regs, None, None),
            ]

            for metric_name, value, cl, ch in metrics:
                if value is None or value == 0:
                    continue
                try:
                    con.execute("""
                        INSERT INTO ps.forecasts
                        (market, channel, metric_name, forecast_date, target_period,
                         period_type, predicted_value, confidence_low, confidence_high,
                         method, scored)
                        VALUES (?, 'ps', ?, ?, ?, 'weekly', ?, ?, ?, 'bayesian_backfill', false)
                    """, [market, metric_name, forecast_date, target_pk,
                          value, cl, ch])
                    written += 1
                except Exception as e:
                    print(f"  WARN: insert failed {market}/{metric_name}/{target_pk}: {e}")

        print(f"  {market}: backfill complete")

    print(f"\nWeekly backfill: {written} rows written, {skipped} skipped (already exist)")
    return written



def backfill_monthly(con, core):
    """Generate monthly backfill forecasts for M01-M04 2026, all markets.

    Strategy: use weekly history to project monthly totals.
    - M01: use all weeks before Jan (i.e. 2025 data), project ~4.3 weeks of Jan
    - M02: use weeks through Jan, project Feb
    - M03: use weeks through Feb, project Mar
    - M04: use weeks through Mar, project Apr (partial)
    """
    print("\n=== MONTHLY BACKFILL: M01-M04 2026 ===\n")
    written = 0

    # Map months to the last week of the prior month (what we'd know at prediction time)
    # and the weeks that belong to each month
    month_config = {
        'M01': {'forecast_date': '2025-12-22', 'weeks_in_month': 5,
                'cutoff_before': '2026-01-01'},
        'M02': {'forecast_date': '2026-01-26', 'weeks_in_month': 4,
                'cutoff_before': '2026-02-01'},
        'M03': {'forecast_date': '2026-02-23', 'weeks_in_month': 4,
                'cutoff_before': '2026-03-01'},
        'M04': {'forecast_date': '2026-03-30', 'weeks_in_month': 5,
                'cutoff_before': '2026-04-01'},
    }

    for market in ALL_MARKETS:
        all_history = fetch_all_weekly_history(con, market)
        if len(all_history) < 5:
            continue

        for month_key, cfg in month_config.items():
            target_pk = f"2026-{month_key}"

            # Check existing
            existing = con.execute(f"""
                SELECT COUNT(*) FROM ps.forecasts
                WHERE market = '{market}' AND target_period = '{target_pk}'
                AND method = 'bayesian_backfill'
            """).fetchone()
            if existing and existing[0] > 0:
                continue

            # Slice history to only weeks before the cutoff date
            cutoff = cfg['cutoff_before']
            history_before = [w for w in all_history if str(w['period_start']) < cutoff]
            history_before = list(reversed(history_before))  # most recent first

            if len(history_before) < 3:
                continue

            # Project one week, then multiply by weeks_in_month
            weeks_mult = cfg['weeks_in_month']

            brand_wk = project_from_history(core, history_before, 'brand_', 1.0)
            nb_wk = project_from_history(core, history_before, 'nb_', 1.0)

            total_regs = (brand_wk.regs + nb_wk.regs) * weeks_mult
            total_cost = (brand_wk.cost + nb_wk.cost) * weeks_mult
            brand_regs = brand_wk.regs * weeks_mult
            nb_regs = nb_wk.regs * weeks_mult

            if total_regs == 0:
                continue

            metrics = [
                ('registrations', total_regs, None, None),
                ('cost', total_cost, None, None),
                ('brand_regs', brand_regs, None, None),
                ('nb_regs', nb_regs, None, None),
            ]

            for metric_name, value, cl, ch in metrics:
                if value is None or value == 0:
                    continue
                try:
                    con.execute("""
                        INSERT INTO ps.forecasts
                        (market, channel, metric_name, forecast_date, target_period,
                         period_type, predicted_value, confidence_low, confidence_high,
                         method, scored)
                        VALUES (?, 'ps', ?, ?, ?, 'monthly', ?, ?, ?, 'bayesian_backfill', false)
                    """, [market, metric_name, cfg['forecast_date'], target_pk,
                          value, cl, ch])
                    written += 1
                except Exception as e:
                    print(f"  WARN: monthly insert failed {market}/{metric_name}/{target_pk}: {e}")

        print(f"  {market}: monthly backfill complete")

    print(f"\nMonthly backfill: {written} rows written")
    return written


def backfill_quarterly(con, core):
    """Generate quarterly backfill forecasts for Q1 and Q2 2026."""
    print("\n=== QUARTERLY BACKFILL: Q1-Q2 2026 ===\n")
    written = 0

    quarter_config = {
        'Q1': {'forecast_date': '2025-12-22', 'weeks_in_quarter': 13,
               'cutoff_before': '2026-01-01'},
        'Q2': {'forecast_date': '2026-03-30', 'weeks_in_quarter': 13,
               'cutoff_before': '2026-04-01'},
    }

    for market in ALL_MARKETS:
        all_history = fetch_all_weekly_history(con, market)
        if len(all_history) < 5:
            continue

        for q_key, cfg in quarter_config.items():
            target_pk = f"2026-{q_key}"

            existing = con.execute(f"""
                SELECT COUNT(*) FROM ps.forecasts
                WHERE market = '{market}' AND target_period = '{target_pk}'
                AND method = 'bayesian_backfill'
            """).fetchone()
            if existing and existing[0] > 0:
                continue

            cutoff = cfg['cutoff_before']
            history_before = [w for w in all_history if str(w['period_start']) < cutoff]
            history_before = list(reversed(history_before))

            if len(history_before) < 3:
                continue

            weeks_mult = cfg['weeks_in_quarter']

            brand_wk = project_from_history(core, history_before, 'brand_', 1.0)
            nb_wk = project_from_history(core, history_before, 'nb_', 1.0)

            total_regs = (brand_wk.regs + nb_wk.regs) * weeks_mult
            total_cost = (brand_wk.cost + nb_wk.cost) * weeks_mult
            brand_regs = brand_wk.regs * weeks_mult
            nb_regs = nb_wk.regs * weeks_mult

            if total_regs == 0:
                continue

            metrics = [
                ('registrations', total_regs, None, None),
                ('cost', total_cost, None, None),
                ('brand_regs', brand_regs, None, None),
                ('nb_regs', nb_regs, None, None),
            ]

            for metric_name, value, cl, ch in metrics:
                if value is None or value == 0:
                    continue
                try:
                    con.execute("""
                        INSERT INTO ps.forecasts
                        (market, channel, metric_name, forecast_date, target_period,
                         period_type, predicted_value, confidence_low, confidence_high,
                         method, scored)
                        VALUES (?, 'ps', ?, ?, ?, 'quarterly', ?, ?, ?, 'bayesian_backfill', false)
                    """, [market, metric_name, cfg['forecast_date'], target_pk,
                          value, cl, ch])
                    written += 1
                except Exception as e:
                    print(f"  WARN: quarterly insert failed {market}/{metric_name}/{target_pk}: {e}")

        print(f"  {market}: quarterly backfill complete")

    print(f"\nQuarterly backfill: {written} rows written")
    return written



def score_all_backfill(con):
    """Score ALL backfill forecasts in batch using SQL joins.

    Much faster than row-by-row updates — builds a scoring table in memory
    then applies it in one UPDATE per period type.
    """
    print("\n=== SCORING ALL BACKFILL FORECASTS ===\n")

    # --- Weekly scoring ---
    # Build a temp table of actuals mapped to forecast metric names
    con.execute("""
        CREATE OR REPLACE TEMP TABLE weekly_actuals AS
        SELECT market, period_key,
            'registrations' as metric_name, registrations as actual_value
        FROM ps.performance WHERE period_type = 'weekly'
            AND period_key LIKE '2026-W%' AND registrations IS NOT NULL AND registrations > 0
        UNION ALL
        SELECT market, period_key,
            'cost', cost
        FROM ps.performance WHERE period_type = 'weekly'
            AND period_key LIKE '2026-W%' AND cost IS NOT NULL AND cost > 0
        UNION ALL
        SELECT market, period_key,
            'brand_regs', brand_registrations
        FROM ps.performance WHERE period_type = 'weekly'
            AND period_key LIKE '2026-W%' AND brand_registrations IS NOT NULL AND brand_registrations > 0
        UNION ALL
        SELECT market, period_key,
            'nb_regs', nb_registrations
        FROM ps.performance WHERE period_type = 'weekly'
            AND period_key LIKE '2026-W%' AND nb_registrations IS NOT NULL AND nb_registrations > 0
    """)

    # Compute scores in a temp table
    con.execute("""
        CREATE OR REPLACE TEMP TABLE weekly_scores AS
        SELECT
            f.market, f.metric_name, f.target_period,
            a.actual_value,
            ROUND(ABS(f.predicted_value - a.actual_value) / a.actual_value * 100, 1) as error_pct,
            CASE
                WHEN f.confidence_low IS NOT NULL AND f.confidence_high IS NOT NULL
                     AND a.actual_value >= f.confidence_low AND a.actual_value <= f.confidence_high
                THEN 'HIT'
                WHEN ABS(f.predicted_value - a.actual_value) / a.actual_value * 100 > 20
                THEN 'SURPRISE'
                ELSE 'MISS'
            END as score
        FROM ps.forecasts f
        JOIN weekly_actuals a
            ON f.market = a.market
            AND f.target_period = a.period_key
            AND f.metric_name = a.metric_name
        WHERE f.method = 'bayesian_backfill'
            AND f.period_type = 'weekly'
            AND (f.scored IS NULL OR f.scored = false)
    """)

    weekly_count = con.execute("SELECT COUNT(*) FROM weekly_scores").fetchone()[0]
    print(f"  Weekly: {weekly_count} forecasts to score")

    # Apply scores
    con.execute("""
        UPDATE ps.forecasts f SET
            actual_value = s.actual_value,
            error_pct = s.error_pct,
            scored = true,
            score = s.score
        FROM weekly_scores s
        WHERE f.market = s.market
            AND f.metric_name = s.metric_name
            AND f.target_period = s.target_period
            AND f.method = 'bayesian_backfill'
    """)
    print(f"  Weekly scoring complete: {weekly_count} scored")

    # --- Monthly scoring ---
    con.execute("""
        CREATE OR REPLACE TEMP TABLE monthly_actuals AS
        SELECT market, period_key,
            'registrations' as metric_name, registrations as actual_value
        FROM ps.performance WHERE period_type = 'monthly'
            AND period_key IN ('2026-M01','2026-M02','2026-M03','2026-M04')
            AND registrations IS NOT NULL AND registrations > 0
        UNION ALL
        SELECT market, period_key,
            'cost', cost
        FROM ps.performance WHERE period_type = 'monthly'
            AND period_key IN ('2026-M01','2026-M02','2026-M03','2026-M04')
            AND cost IS NOT NULL AND cost > 0
        UNION ALL
        SELECT market, period_key,
            'brand_regs', brand_registrations
        FROM ps.performance WHERE period_type = 'monthly'
            AND period_key IN ('2026-M01','2026-M02','2026-M03','2026-M04')
            AND brand_registrations IS NOT NULL AND brand_registrations > 0
        UNION ALL
        SELECT market, period_key,
            'nb_regs', nb_registrations
        FROM ps.performance WHERE period_type = 'monthly'
            AND period_key IN ('2026-M01','2026-M02','2026-M03','2026-M04')
            AND nb_registrations IS NOT NULL AND nb_registrations > 0
    """)

    con.execute("""
        CREATE OR REPLACE TEMP TABLE monthly_scores AS
        SELECT
            f.market, f.metric_name, f.target_period,
            a.actual_value,
            ROUND(ABS(f.predicted_value - a.actual_value) / a.actual_value * 100, 1) as error_pct,
            CASE
                WHEN ABS(f.predicted_value - a.actual_value) / a.actual_value * 100 <= 10 THEN 'HIT'
                WHEN ABS(f.predicted_value - a.actual_value) / a.actual_value * 100 > 20 THEN 'SURPRISE'
                ELSE 'MISS'
            END as score
        FROM ps.forecasts f
        JOIN monthly_actuals a
            ON f.market = a.market
            AND f.target_period = a.period_key
            AND f.metric_name = a.metric_name
        WHERE f.method = 'bayesian_backfill'
            AND f.period_type = 'monthly'
            AND (f.scored IS NULL OR f.scored = false)
    """)

    monthly_count = con.execute("SELECT COUNT(*) FROM monthly_scores").fetchone()[0]

    con.execute("""
        UPDATE ps.forecasts f SET
            actual_value = s.actual_value,
            error_pct = s.error_pct,
            scored = true,
            score = s.score
        FROM monthly_scores s
        WHERE f.market = s.market
            AND f.metric_name = s.metric_name
            AND f.target_period = s.target_period
            AND f.method = 'bayesian_backfill'
    """)
    print(f"  Monthly scoring complete: {monthly_count} scored")

    # --- Quarterly scoring ---
    # Build Q1 actuals from sum of M01-M03, Q2 from M04-M06
    con.execute("""
        CREATE OR REPLACE TEMP TABLE quarterly_actuals AS
        SELECT market, '2026-Q1' as period_key, metric_name, SUM(actual_value) as actual_value
        FROM monthly_actuals
        WHERE period_key IN ('2026-M01','2026-M02','2026-M03')
        GROUP BY market, metric_name
        HAVING SUM(actual_value) > 0
        UNION ALL
        SELECT market, '2026-Q2' as period_key, metric_name, SUM(actual_value) as actual_value
        FROM monthly_actuals
        WHERE period_key IN ('2026-M04','2026-M05','2026-M06')
        GROUP BY market, metric_name
        HAVING SUM(actual_value) > 0
    """)

    con.execute("""
        CREATE OR REPLACE TEMP TABLE quarterly_scores AS
        SELECT
            f.market, f.metric_name, f.target_period,
            a.actual_value,
            ROUND(ABS(f.predicted_value - a.actual_value) / a.actual_value * 100, 1) as error_pct,
            CASE
                WHEN ABS(f.predicted_value - a.actual_value) / a.actual_value * 100 <= 10 THEN 'HIT'
                WHEN ABS(f.predicted_value - a.actual_value) / a.actual_value * 100 > 20 THEN 'SURPRISE'
                ELSE 'MISS'
            END as score
        FROM ps.forecasts f
        JOIN quarterly_actuals a
            ON f.market = a.market
            AND f.target_period = a.period_key
            AND f.metric_name = a.metric_name
        WHERE f.method = 'bayesian_backfill'
            AND f.period_type = 'quarterly'
            AND (f.scored IS NULL OR f.scored = false)
    """)

    quarterly_count = con.execute("SELECT COUNT(*) FROM quarterly_scores").fetchone()[0]

    con.execute("""
        UPDATE ps.forecasts f SET
            actual_value = s.actual_value,
            error_pct = s.error_pct,
            scored = true,
            score = s.score
        FROM quarterly_scores s
        WHERE f.market = s.market
            AND f.metric_name = s.metric_name
            AND f.target_period = s.target_period
            AND f.method = 'bayesian_backfill'
    """)
    print(f"  Quarterly scoring complete: {quarterly_count} scored")

    total_scored = weekly_count + monthly_count + quarterly_count
    print(f"\nTotal scored: {total_scored}")
    return total_scored



def print_summary(con):
    """Print calibration summary: hit rate per market, overall stats."""
    print("\n" + "=" * 70)
    print("BACKFILL CALIBRATION SUMMARY")
    print("=" * 70)

    # Overall stats
    totals = con.execute("""
        SELECT COUNT(*) as total,
               SUM(CASE WHEN scored = true THEN 1 ELSE 0 END) as scored,
               SUM(CASE WHEN score = 'HIT' THEN 1 ELSE 0 END) as hits,
               SUM(CASE WHEN score = 'MISS' THEN 1 ELSE 0 END) as misses,
               SUM(CASE WHEN score = 'SURPRISE' THEN 1 ELSE 0 END) as surprises,
               ROUND(AVG(CASE WHEN scored = true THEN error_pct END), 1) as avg_error
        FROM ps.forecasts
        WHERE method = 'bayesian_backfill'
    """).fetchone()

    total, scored, hits, misses, surprises, avg_error = totals
    hit_rate = round(hits * 100.0 / scored, 1) if scored > 0 else 0

    print(f"\n  Total forecasts:  {total}")
    print(f"  Scored:           {scored}")
    print(f"  Hits:             {hits}")
    print(f"  Misses:           {misses}")
    print(f"  Surprises:        {surprises}")
    print(f"  Avg error %:      {avg_error}%")
    print(f"  Overall hit rate: {hit_rate}%")

    # Per-market breakdown (weekly only for cleaner view)
    print(f"\n{'Market':<8} {'Scored':>7} {'Hits':>6} {'Miss':>6} {'Surp':>6} {'Err%':>7} {'HitRate':>8}")
    print("-" * 55)

    market_rows = con.execute("""
        SELECT market,
               COUNT(*) as scored,
               SUM(CASE WHEN score = 'HIT' THEN 1 ELSE 0 END) as hits,
               SUM(CASE WHEN score = 'MISS' THEN 1 ELSE 0 END) as misses,
               SUM(CASE WHEN score = 'SURPRISE' THEN 1 ELSE 0 END) as surprises,
               ROUND(AVG(error_pct), 1) as avg_error
        FROM ps.forecasts
        WHERE method = 'bayesian_backfill' AND scored = true
        AND period_type = 'weekly'
        GROUP BY market
        ORDER BY market
    """).fetchall()

    for mkt, sc, h, m, s, err in market_rows:
        hr = round(h * 100.0 / sc, 1) if sc > 0 else 0
        print(f"  {mkt:<6} {sc:>7} {h:>6} {m:>6} {s:>6} {err:>6}% {hr:>7}%")

    # Per-metric breakdown
    print(f"\n{'Metric':<16} {'Scored':>7} {'Hits':>6} {'Miss':>6} {'Surp':>6} {'Err%':>7} {'HitRate':>8}")
    print("-" * 63)

    metric_rows = con.execute("""
        SELECT metric_name,
               COUNT(*) as scored,
               SUM(CASE WHEN score = 'HIT' THEN 1 ELSE 0 END) as hits,
               SUM(CASE WHEN score = 'MISS' THEN 1 ELSE 0 END) as misses,
               SUM(CASE WHEN score = 'SURPRISE' THEN 1 ELSE 0 END) as surprises,
               ROUND(AVG(error_pct), 1) as avg_error
        FROM ps.forecasts
        WHERE method = 'bayesian_backfill' AND scored = true
        AND period_type = 'weekly'
        GROUP BY metric_name
        ORDER BY metric_name
    """).fetchall()

    for met, sc, h, m, s, err in metric_rows:
        hr = round(h * 100.0 / sc, 1) if sc > 0 else 0
        print(f"  {met:<14} {sc:>7} {h:>6} {m:>6} {s:>6} {err:>6}% {hr:>7}%")

    # Legend
    print(f"\n{'─' * 70}")
    print("LEGEND")
    print(f"{'─' * 70}")
    print("  Scored   = Number of forecasts that had actuals to compare against")
    print("  Hits     = Actual value fell WITHIN the 70% credible interval (CI)")
    print("  Miss     = Actual was OUTSIDE the CI, but error was 20% or less")
    print("  Surp     = Actual was OUTSIDE the CI AND error exceeded 20%")
    print("  Err%     = Average |predicted - actual| / actual * 100 across scored forecasts")
    print("  HitRate  = Hits / Scored * 100 (% of predictions where actual was within CI)")
    print()
    print("  How CI works: BayesianCore computes a 70% credible interval around the")
    print("  point estimate. A 'HIT' means the engine's uncertainty range was well-")
    print("  calibrated. A high HitRate with low Err% = good. High HitRate with high")
    print("  Err% = CIs are too wide (engine is uncertain but technically correct).")
    print()
    print("  Note: cost/brand_regs/nb_regs lack CIs (only total regs has CI), so")
    print("  they can only score HIT via the error threshold, not interval coverage.")
    print(f"{'─' * 70}")
    print("=" * 70)


def main():
    print("Connecting to MotherDuck...")
    con = connect()
    core = BayesianCore()

    try:
        # Phase 1: Generate weekly backfill
        weekly_written = backfill_weekly(con, core)

        # Phase 2: Generate monthly backfill
        monthly_written = backfill_monthly(con, core)

        # Phase 3: Generate quarterly backfill
        quarterly_written = backfill_quarterly(con, core)

        # Phase 4: Score everything (batch SQL — much faster)
        total_scored = score_all_backfill(con)

        # Phase 5: Summary
        print_summary(con)

        print(f"\nDone. {weekly_written + monthly_written + quarterly_written} total forecasts written, "
              f"{total_scored} scored.")

    except Exception as e:
        print(f"\nFATAL: {e}")
        traceback.print_exc()
    finally:
        con.close()


if __name__ == '__main__':
    main()
