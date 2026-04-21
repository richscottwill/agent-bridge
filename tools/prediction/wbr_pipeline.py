#!/usr/bin/env python3
"""WBR Pipeline — consolidated end-to-end orchestrator.

Replaces project.py, project_full.py, and wbr-pipeline.sh with a single
script that runs 7 stages: Ingest → Load → Score → Project → Callout →
Dive Update → Report.

Usage:
    python3 wbr_pipeline.py <xlsx_path> [--week 2026-W15]
"""

import sys
import os
import json
import time
import traceback
from datetime import datetime
from pathlib import Path

# Ensure sibling packages are importable
sys.path.insert(0, os.path.expanduser('~/shared/tools'))
sys.path.insert(0, os.path.expanduser('~/shared/tools/dashboard-ingester'))
sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))

from prediction.ptypes import (
    PipelineResult, ScoringResult, MarketProjection, SegmentForecast,
)
from prediction.bayesian_projector import BayesianProjector, ALL_MARKETS

DIVE_ID = '68b308c1-97be-4c72-81ae-517318500de9'
DIVE_JSX_PATH = os.path.expanduser('~/shared/tools/dashboard-ingester/dive-v3.jsx')


# ── Scoring ────────────────────────────────────────────────────────────────

def score_prior_predictions(con, current_week: str) -> ScoringResult:
    """Score prior predictions against new actuals.

    For each market: fetch actuals from ps.performance, fetch unscored
    forecasts from ps.forecasts, compute error, classify HIT/MISS/SURPRISE,
    and UPDATE ps.forecasts.
    """
    hits = 0
    misses = 0
    surprises = 0
    error_pcts = []

    for market in ALL_MARKETS:
        # Get actuals
        actuals_row = con.execute(f"""
            SELECT registrations, brand_registrations, nb_registrations, cost, cpa
            FROM ps.performance
            WHERE market = '{market}' AND period_type = 'weekly'
            AND period_key = '{current_week}'
        """).fetchone()

        if not actuals_row:
            continue

        actual_map = {
            'registrations': actuals_row[0],
            'brand_registrations': actuals_row[1],
            'nb_registrations': actuals_row[2],
            'cost': actuals_row[3],
            'cpa': actuals_row[4],
        }

        # Get unscored forecasts targeting this week
        forecasts = con.execute(f"""
            SELECT market, metric_name, predicted_value,
                   confidence_low, confidence_high
            FROM ps.forecasts
            WHERE market = '{market}' AND target_period = '{current_week}'
            AND (scored IS NULL OR scored = false)
        """).fetchall()

        for mkt, metric, predicted, ci_low, ci_high in forecasts:
            actual = actual_map.get(metric)
            if actual is None or actual == 0:
                continue

            predicted = float(predicted) if predicted else 0
            actual = float(actual)
            error_pct = abs(predicted - actual) / actual * 100

            within_ci = (
                ci_low is not None and ci_high is not None
                and float(ci_low) <= actual <= float(ci_high)
            )

            if within_ci:
                score = 'HIT'
                hits += 1
            elif error_pct > 20:
                score = 'SURPRISE'
                surprises += 1
            else:
                score = 'MISS'
                misses += 1

            error_pcts.append(error_pct)

            try:
                con.execute("""
                    UPDATE ps.forecasts SET
                        actual_value = ?, error_pct = ?, scored = true, score = ?
                    WHERE market = ? AND metric_name = ? AND target_period = ?
                """, [actual, round(error_pct, 1), score, market, metric, current_week])
            except Exception as e:
                print(f"  WARN: scoring update failed {market}/{metric}: {e}")

    mean_error = sum(error_pcts) / len(error_pcts) if error_pcts else 0.0

    # Compute calibration factor (simple: if we're consistently over/under)
    calibration = 1.0
    if error_pcts:
        # Use mean error to adjust: high error → widen intervals
        if mean_error > 15:
            calibration = 1.0 + (mean_error - 15) / 100
        calibration = max(0.5, min(2.0, calibration))

    # ── Gap 2 + Gap 4: Persist calibration + CI width adjustment per market ──
    total_scored = hits + misses + surprises
    if total_scored > 0:
        hit_rate = hits / total_scored
    else:
        hit_rate = 0.0

    # Gap 4: Compute CI width adjustment from hit rate
    ci_width_adj = 1.0
    if total_scored > 0:
        if hit_rate < 0.60:
            # CIs too narrow → widen
            ci_width_adj = 1.0 + (0.70 - hit_rate) * 2
        elif hit_rate > 0.85 and mean_error > 15:
            # CIs too wide → narrow
            ci_width_adj = max(0.7, 1.0 - (hit_rate - 0.85))
        # else: ci_width_adj stays 1.0

    # Persist per-market calibration state
    cal_upsert_rows = []
    for market in ALL_MARKETS:
        # Compute per-market stats from scored forecasts (rolling last 20)
        try:
            market_stats = con.execute(f"""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN score = 'HIT' THEN 1 ELSE 0 END) as hits,
                    AVG(error_pct) as avg_err
                FROM (
                    SELECT score, error_pct
                    FROM ps.forecasts
                    WHERE market = '{market}' AND scored = true
                    AND metric_name = 'registrations'
                    ORDER BY forecast_date DESC
                    LIMIT 20
                )
            """).fetchone()

            if market_stats and market_stats[0] and market_stats[0] > 0:
                m_total = int(market_stats[0])
                m_hits = int(market_stats[1] or 0)
                m_hit_rate = m_hits / m_total
                m_avg_err = float(market_stats[2] or 0)

                # Per-market CI width adjustment
                m_ci_adj = 1.0
                if m_hit_rate < 0.60:
                    m_ci_adj = 1.0 + (0.70 - m_hit_rate) * 2
                elif m_hit_rate > 0.85 and m_avg_err > 15:
                    m_ci_adj = max(0.7, 1.0 - (m_hit_rate - 0.85))

                # Per-market calibration factor from rolling error
                m_cal = 1.0
                if m_avg_err > 15:
                    m_cal = 1.0 + (m_avg_err - 15) / 100
                m_cal = max(0.5, min(2.0, m_cal))

                cal_upsert_rows.append((market, round(m_cal, 4), round(m_ci_adj, 4),
                                        current_week, m_total, round(m_hit_rate, 4), round(m_avg_err, 2)))
        except Exception as e:
            print(f"  WARN: calibration stats query failed for {market}: {e}")

    if cal_upsert_rows:
        try:
            con.executemany("""
                INSERT OR REPLACE INTO ps.calibration_state
                (market, metric_name, calibration_factor, ci_width_adjustment,
                 last_scored_week, total_scored, hit_rate, mean_error_pct, updated_at)
                VALUES (?, 'registrations', ?, ?, ?, ?, ?, ?, NOW())
            """, cal_upsert_rows)
        except Exception as e:
            print(f"  WARN: calibration_state batch upsert failed: {e}")

    return ScoringResult(
        predictions_scored=total_scored,
        hits=hits,
        misses=misses,
        surprises=surprises,
        mean_error_pct=round(mean_error, 1),
        calibration=calibration,
    )


# ── Pipeline ───────────────────────────────────────────────────────────────

class WBRPipeline:
    """Consolidated WBR pipeline. One file, one entry point, one run."""

    def __init__(self, xlsx_path: str, week_override: str = None):
        self.xlsx_path = xlsx_path
        self.week_override = week_override
        self.con = None
        self.prediction_run_id = f"run-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        if not os.path.exists(xlsx_path):
            raise FileNotFoundError(f"xlsx not found: {xlsx_path}")

    def _connect(self):
        """Open single MotherDuck connection."""
        import duckdb
        token = os.environ.get('MOTHERDUCK_TOKEN',
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJpY2hzY290dHdpbGxAZ21haWwuY29tIiwibWRSZWdpb24iOiJhd3MtdXMtZWFzdC0xIiwic2Vzc2lvbiI6InJpY2hzY290dHdpbGwuZ21haWwuY29tIiwicGF0IjoiVDNIYzFVQWYzT3o1bjVkLS03ckdHNlBjMlpUdVNNbFItT3RXMS1qNzVPUSIsInVzZXJJZCI6ImU2MDhlNDZiLTE4YzctNGE5Ny04M2I2LWE0N2ZhOThmNjBhYyIsImlzcyI6Im1kX3BhdCIsInJlYWRPbmx5IjpmYWxzZSwidG9rZW5UeXBlIjoicmVhZF93cml0ZSIsImlhdCI6MTc3NTQ0MzY0N30.tS0Cab3FQ8_CDZ1PqOo9z09KYHEUFHwuLVXRQrxcHig')
        if not token:
            raise EnvironmentError("MOTHERDUCK_TOKEN not set")
        self.con = duckdb.connect(f'md:ps_analytics?motherduck_token={token}')

    def _ensure_schema(self):
        """Create pipeline_runs table and source-of-truth views if missing."""
        # pipeline_runs — audit log for every run
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS ps.pipeline_runs (
                run_id VARCHAR,
                week VARCHAR,
                xlsx_path VARCHAR,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                stages_completed VARCHAR,
                stages_failed VARCHAR,
                markets_processed VARCHAR,
                rows_loaded INTEGER,
                projections_written INTEGER,
                predictions_scored INTEGER,
                errors VARCHAR
            )
        """)

        # calibration_state — persistent calibration across runs (Gap 2 + Gap 4)
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS ps.calibration_state (
                market VARCHAR,
                metric_name VARCHAR,
                calibration_factor DOUBLE,
                ci_width_adjustment DOUBLE,
                last_scored_week VARCHAR,
                total_scored INTEGER,
                hit_rate DOUBLE,
                mean_error_pct DOUBLE,
                updated_at TIMESTAMP,
                PRIMARY KEY (market, metric_name)
            )
        """)

        # PE-1 Phase 1: Add lead_weeks and prediction_run_id to ps.forecasts
        # (idempotent — ALTER TABLE ADD COLUMN IF NOT EXISTS)
        try:
            self.con.execute("ALTER TABLE ps.forecasts ADD COLUMN IF NOT EXISTS lead_weeks INT")
            self.con.execute("ALTER TABLE ps.forecasts ADD COLUMN IF NOT EXISTS prediction_run_id VARCHAR")
        except Exception:
            pass  # Column already exists or DB doesn't support IF NOT EXISTS

        # latest_forecasts — most recent unscored forecast per market+metric
        self.con.execute("""
            CREATE OR REPLACE VIEW ps.latest_forecasts AS
            SELECT market, metric_name, target_period, predicted_value,
                   confidence_low, confidence_high, method, forecast_date
            FROM ps.forecasts
            WHERE scored IS NULL OR scored = false
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY market, metric_name
                ORDER BY forecast_date DESC
            ) = 1
        """)

        # forecast_accuracy — scored forecasts with hit/miss/surprise rates
        self.con.execute("""
            CREATE OR REPLACE VIEW ps.forecast_accuracy AS
            SELECT market, metric_name,
                   COUNT(*) AS total_scored,
                   SUM(CASE WHEN score = 'HIT' THEN 1 ELSE 0 END) AS hits,
                   SUM(CASE WHEN score = 'MISS' THEN 1 ELSE 0 END) AS misses,
                   SUM(CASE WHEN score = 'SURPRISE' THEN 1 ELSE 0 END) AS surprises,
                   ROUND(AVG(error_pct), 1) AS avg_error_pct,
                   ROUND(SUM(CASE WHEN score = 'HIT' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS hit_rate_pct
            FROM ps.forecasts
            WHERE scored = true
            GROUP BY market, metric_name
        """)

        # market_status — latest actuals + forecast + OP2 per market
        self.con.execute("""
            CREATE OR REPLACE VIEW ps.market_status AS
            SELECT
                p.market,
                p.period_key AS latest_week,
                p.registrations AS actual_regs,
                p.cost AS actual_cost,
                p.cpa AS actual_cpa,
                f.predicted_value AS forecast_regs,
                f.confidence_low AS forecast_ci_low,
                f.confidence_high AS forecast_ci_high,
                t.target_value AS op2_cost_target
            FROM ps.performance p
            LEFT JOIN ps.forecasts f
                ON p.market = f.market
                AND p.period_key = f.target_period
                AND f.metric_name = 'registrations'
            LEFT JOIN ps.targets t
                ON p.market = t.market
                AND t.metric_name = 'cost'
            WHERE p.period_type = 'weekly'
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY p.market
                ORDER BY p.period_start DESC
            ) = 1
        """)

    # ── Stage implementations ──────────────────────────────────────────

    def _stage_ingest(self):
        """Stage 1: Run DashboardIngester, return (results, monthly_actuals, monthly_budgets)."""
        from ingest import DashboardIngester

        ingester = DashboardIngester(self.xlsx_path)

        # Convert week format: '2026-W14' → '2026 W14' for ingester
        target_week = None
        if self.week_override:
            target_week = self.week_override.replace('-', ' ')

        results = ingester.run(target_week=target_week)
        if results is None:
            raise RuntimeError("DashboardIngester returned None — could not parse xlsx")

        # Read monthly data separately (ingester attaches to results but also returns standalone)
        monthly_actuals = ingester._read_monthly_actuals()
        monthly_budgets = ingester._read_monthly_budget()

        return results, monthly_actuals, monthly_budgets

    def _stage_load(self, results: dict, monthly_actuals: dict,
                    monthly_budgets: dict) -> int:
        """Stage 2: Upsert to ps.performance + ps.targets. Returns row count."""
        from datetime import timedelta
        source_file = os.path.basename(self.xlsx_path)
        total_rows = 0

        def week_to_dates(week_str):
            """Convert '2026 W14' to (start_date, end_date) strings."""
            parts = week_str.split()
            year = int(parts[0])
            week_num = int(parts[1].replace('W', ''))
            jan4 = datetime(year, 1, 4)
            start_of_w1 = jan4 - timedelta(days=jan4.weekday())
            monday = start_of_w1 + timedelta(weeks=week_num - 1)
            sunday = monday + timedelta(days=6)
            return monday.strftime('%Y-%m-%d'), sunday.strftime('%Y-%m-%d')

        def s(v):
            if v is None:
                return None
            try:
                return float(v)
            except (ValueError, TypeError):
                return None

        def si(v):
            if v is None:
                return None
            try:
                return int(float(v))
            except (ValueError, TypeError):
                return None

        PERF_SQL = """INSERT OR REPLACE INTO ps.performance
            (market, period_type, period_key, period_start,
             registrations, cost, cpa, clicks, impressions, cpc, cvr, ctr,
             brand_registrations, brand_cost, brand_cpa, brand_clicks, brand_cpc, brand_cvr,
             nb_registrations, nb_cost, nb_cpa, nb_clicks, nb_cpc, nb_cvr,
             ieccp, source)
            VALUES (?,?,?,?, ?,?,?,?,?,?,?,?, ?,?,?,?,?,?, ?,?,?,?,?,?, ?,?)"""

        for market, analysis in results.items():
            if not isinstance(analysis, dict) or 'error' in analysis:
                continue

            # Weekly rows from weekly_history
            weekly_history = analysis.get('weekly_history', [])
            for w in weekly_history:
                pk = w['week'].replace(' ', '-')
                try:
                    ps_date, _ = week_to_dates(w['week'])
                except Exception:
                    continue
                try:
                    self.con.execute(PERF_SQL, [
                        market, 'weekly', pk, ps_date,
                        si(w.get('regs')), s(w.get('spend')), s(w.get('cpa')),
                        si(w.get('clicks')), si(w.get('impressions')),
                        s(w.get('cpc')), s(w.get('cvr')), s(w.get('ctr')),
                        si(w.get('brand_regs')), s(w.get('brand_spend')), s(w.get('brand_cpa')),
                        si(w.get('brand_clicks')), s(w.get('brand_cpc')), s(w.get('brand_cvr')),
                        si(w.get('nb_regs')), s(w.get('nb_spend')), s(w.get('nb_cpa')),
                        si(w.get('nb_clicks')), s(w.get('nb_cpc')), s(w.get('nb_cvr')),
                        None, source_file,
                    ])
                    total_rows += 1
                except Exception as e:
                    print(f"  WARN: weekly insert failed {market}/{pk}: {e}")

        # Monthly actuals → ps.performance
        for market in ALL_MARKETS:
            actuals = monthly_actuals.get(market, {})
            for month_label, m in actuals.items():
                if not m or (m.get('spend', 0) == 0 and m.get('regs', 0) == 0):
                    continue
                # month_label like '2026 Jan' → period_key '2026-M01'
                month_map = {
                    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
                }
                parts = month_label.split()
                if len(parts) == 2:
                    pk = f"{parts[0]}-M{month_map.get(parts[1], '00')}"
                    ps_date = f"{parts[0]}-{month_map.get(parts[1], '01')}-01"
                else:
                    continue
                try:
                    self.con.execute(PERF_SQL, [
                        market, 'monthly', pk, ps_date,
                        si(m.get('regs')), s(m.get('spend')), s(m.get('cpa')),
                        si(m.get('clicks')), si(m.get('impressions')),
                        s(m.get('cpc')), s(m.get('cvr')), s(m.get('ctr')),
                        si(m.get('brand_regs')), s(m.get('brand_spend')), s(m.get('brand_cpa')),
                        si(m.get('brand_clicks')), s(m.get('brand_cpc')), s(m.get('brand_cvr')),
                        si(m.get('nb_regs')), s(m.get('nb_spend')), s(m.get('nb_cpa')),
                        si(m.get('nb_clicks')), s(m.get('nb_cpc')), s(m.get('nb_cvr')),
                        None, source_file,
                    ])
                    total_rows += 1
                except Exception as e:
                    print(f"  WARN: monthly insert failed {market}/{pk}: {e}")

        # Daily actuals → ps.performance (period_type='daily', period_key='YYYY-MM-DD')
        # Source: ingester analysis['daily_patterns']['daily'] contains 7 verified
        # day dicts per market for the target week. This is the authoritative per-day
        # actuals from the xlsx Daily tab. Also iterate the same write for the prior
        # week's daily rows when available (14-day backfill window for corrections).
        daily_count = 0
        for market, analysis in results.items():
            if not isinstance(analysis, dict) or 'error' in analysis:
                continue
            dp = analysis.get('daily_patterns') or {}
            days = dp.get('daily') or []
            for day in days:
                iso_date = day.get('date')
                if not iso_date:
                    continue
                # Derive ratios from totals so Brand/NB/blended CPA/CVR/CPC are present
                regs = si(day.get('regs')); cost = s(day.get('cost'))
                clicks = si(day.get('clicks')); imps = si(day.get('impressions'))
                b_regs = si(day.get('brand_regs')); b_cost = s(day.get('brand_cost'))
                b_clicks = si(day.get('brand_clicks'))
                nb_regs = si(day.get('nb_regs')); nb_cost = s(day.get('nb_cost'))
                nb_clicks = si(day.get('nb_clicks'))

                def safe_ratio(num, den):
                    if num is None or den is None or den == 0:
                        return None
                    return num / den

                cpa = safe_ratio(cost, regs)
                cpc = safe_ratio(cost, clicks)
                cvr = safe_ratio(regs, clicks)
                ctr = safe_ratio(clicks, imps)
                b_cpa = safe_ratio(b_cost, b_regs)
                b_cpc = safe_ratio(b_cost, b_clicks)
                b_cvr = safe_ratio(b_regs, b_clicks)
                nb_cpa = safe_ratio(nb_cost, nb_regs)
                nb_cpc = safe_ratio(nb_cost, nb_clicks)
                nb_cvr = safe_ratio(nb_regs, nb_clicks)

                try:
                    self.con.execute(PERF_SQL, [
                        market, 'daily', iso_date, iso_date,
                        regs, cost, cpa, clicks, imps, cpc, cvr, ctr,
                        b_regs, b_cost, b_cpa, b_clicks, b_cpc, b_cvr,
                        nb_regs, nb_cost, nb_cpa, nb_clicks, nb_cpc, nb_cvr,
                        None, source_file,
                    ])
                    daily_count += 1
                    total_rows += 1
                except Exception as e:
                    print(f"  WARN: daily insert failed {market}/{iso_date}: {e}")

        # Quarterly rollup → ps.performance (period_type='quarterly', period_key='YYYY-Qn')
        # Computed from monthly rows (3 months per quarter) so the math is internally
        # consistent and doesn't double-count with weekly boundaries crossing quarters.
        quarter_count = 0
        QUARTER_MONTHS = {
            'Q1': ['01', '02', '03'],
            'Q2': ['04', '05', '06'],
            'Q3': ['07', '08', '09'],
            'Q4': ['10', '11', '12'],
        }
        for market in ALL_MARKETS:
            for quarter, months in QUARTER_MONTHS.items():
                year = datetime.now().strftime('%Y')
                month_pks = [f"{year}-M{m}" for m in months]
                try:
                    rows = self.con.execute(f"""
                        SELECT
                            SUM(registrations), SUM(cost), SUM(clicks), SUM(impressions),
                            SUM(brand_registrations), SUM(brand_cost), SUM(brand_clicks),
                            SUM(nb_registrations), SUM(nb_cost), SUM(nb_clicks),
                            COUNT(*) AS months_present
                        FROM ps.performance
                        WHERE market = ? AND period_type = 'monthly'
                          AND period_key IN ({','.join(['?'] * len(month_pks))})
                    """, [market] + month_pks).fetchone()
                except Exception as e:
                    print(f"  WARN: quarterly read failed {market}/{quarter}: {e}")
                    continue
                if not rows or not rows[0] or rows[-1] == 0:
                    continue  # skip quarters with no monthly data
                q_regs, q_cost, q_clicks, q_imps, q_b_regs, q_b_cost, q_b_clicks, q_nb_regs, q_nb_cost, q_nb_clicks, months_present = rows
                q_pk = f"{year}-{quarter}"
                q_start = f"{year}-{months[0]}-01"

                def qr(num, den):
                    return (num / den) if (num is not None and den and den != 0) else None

                q_cpa = qr(q_cost, q_regs); q_cpc = qr(q_cost, q_clicks)
                q_cvr = qr(q_regs, q_clicks); q_ctr = qr(q_clicks, q_imps)
                q_b_cpa = qr(q_b_cost, q_b_regs); q_b_cpc = qr(q_b_cost, q_b_clicks)
                q_b_cvr = qr(q_b_regs, q_b_clicks)
                q_nb_cpa = qr(q_nb_cost, q_nb_regs); q_nb_cpc = qr(q_nb_cost, q_nb_clicks)
                q_nb_cvr = qr(q_nb_regs, q_nb_clicks)

                try:
                    self.con.execute(PERF_SQL, [
                        market, 'quarterly', q_pk, q_start,
                        si(q_regs), s(q_cost), q_cpa, si(q_clicks), si(q_imps),
                        q_cpc, q_cvr, q_ctr,
                        si(q_b_regs), s(q_b_cost), q_b_cpa, si(q_b_clicks), q_b_cpc, q_b_cvr,
                        si(q_nb_regs), s(q_nb_cost), q_nb_cpa, si(q_nb_clicks), q_nb_cpc, q_nb_cvr,
                        None, source_file,
                    ])
                    quarter_count += 1
                    total_rows += 1
                except Exception as e:
                    print(f"  WARN: quarterly insert failed {market}/{q_pk}: {e}")

        # WW aggregate → ps.performance (market='WW' at every period_type)
        # Computed as SUM of the 10 markets at the matching grain — this is the
        # "10-market total" rollup. Grain filter (period_type=) prevents any
        # accidental cross-grain summing. WW rows use the same period_type/period_key
        # as their constituent market rows.
        ww_count = 0
        try:
            # Delete existing WW rows to avoid stale aggregates
            self.con.execute("DELETE FROM ps.performance WHERE market = 'WW'")
            # Re-aggregate from all 10 markets at every grain
            self.con.execute(f"""
                INSERT INTO ps.performance
                (market, period_type, period_key, period_start,
                 registrations, cost, cpa, clicks, impressions, cpc, cvr, ctr,
                 brand_registrations, brand_cost, brand_cpa, brand_clicks, brand_cpc, brand_cvr,
                 nb_registrations, nb_cost, nb_cpa, nb_clicks, nb_cpc, nb_cvr,
                 ieccp, source)
                SELECT
                    'WW' AS market,
                    period_type, period_key, MIN(period_start) AS period_start,
                    SUM(registrations), SUM(cost),
                    CASE WHEN SUM(registrations) > 0 THEN SUM(cost) / SUM(registrations) END AS cpa,
                    SUM(clicks), SUM(impressions),
                    CASE WHEN SUM(clicks) > 0 THEN SUM(cost) / SUM(clicks) END AS cpc,
                    CASE WHEN SUM(clicks) > 0 THEN CAST(SUM(registrations) AS DOUBLE) / SUM(clicks) END AS cvr,
                    CASE WHEN SUM(impressions) > 0 THEN CAST(SUM(clicks) AS DOUBLE) / SUM(impressions) END AS ctr,
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
                    NULL, '{source_file}'
                FROM ps.performance
                WHERE market IN ({','.join([f"'{m}'" for m in ALL_MARKETS])})
                GROUP BY period_type, period_key
            """)
            ww_row = self.con.execute("SELECT COUNT(*) FROM ps.performance WHERE market = 'WW'").fetchone()
            ww_count = ww_row[0] if ww_row else 0
            total_rows += ww_count
        except Exception as e:
            print(f"  WARN: WW aggregate build failed: {e}")

        # Refresh canonical read views (idempotent) — one per grain so callers
        # can't accidentally sum across grains. Also rebuild the guardrail view.
        try:
            for grain in ('daily', 'weekly', 'monthly', 'quarterly'):
                self.con.execute(f"""
                    CREATE OR REPLACE VIEW ps.v_{grain} AS
                    SELECT * FROM ps.performance WHERE period_type = '{grain}'
                """)
            self.con.execute("""
                CREATE OR REPLACE VIEW ps.v_grain_coverage AS
                SELECT market, period_type, COUNT(*) AS rows,
                       MIN(period_key) AS first_key, MAX(period_key) AS last_key
                FROM ps.performance
                GROUP BY market, period_type
                ORDER BY market, period_type
            """)
            print(f"  Views refreshed: ps.v_daily, ps.v_weekly, ps.v_monthly, ps.v_quarterly, ps.v_grain_coverage")
        except Exception as e:
            print(f"  WARN: view refresh failed: {e}")

        print(f"  Load: {total_rows} performance rows ({daily_count} daily, {quarter_count} quarterly, {ww_count} WW)")

        # OP2 targets → ps.targets
        targets_count = 0
        month_to_pk = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
        }

        TARGETS_SQL = """
            INSERT OR REPLACE INTO ps.targets
            (market, channel, metric_name, fiscal_year, period_type,
             period_key, target_value, source)
            VALUES (?, 'ps', ?, 2026, 'monthly', ?, ?, 'ww_dashboard')
        """

        for market in ALL_MARKETS:
            budget = monthly_budgets.get(market, {})
            spend_op2 = budget.get('spend_op2', {})
            regs_op2 = budget.get('regs_op2', {})
            cpa_op2 = budget.get('cpa_op2', {})
            if not isinstance(spend_op2, dict):
                spend_op2 = {}
            if not isinstance(regs_op2, dict):
                regs_op2 = {}
            if not isinstance(cpa_op2, dict):
                cpa_op2 = {}
            all_months = set(list(spend_op2.keys()) + list(regs_op2.keys()) + list(cpa_op2.keys()))
            for month_key in all_months:
                # Convert '2026 Jan' → '2026-M01'
                parts = month_key.split()
                if len(parts) == 2:
                    pk = f"{parts[0]}-M{month_to_pk.get(parts[1], '00')}"
                else:
                    continue

                cost_val = spend_op2.get(month_key)
                if cost_val and float(cost_val) > 0:
                    try:
                        self.con.execute(TARGETS_SQL,
                            [market, 'cost', pk, float(cost_val)])
                        targets_count += 1
                    except Exception as e:
                        print(f"  WARN: cost target insert failed {market}/{pk}: {e}")
                regs_val = regs_op2.get(month_key)
                if regs_val and float(regs_val) > 0:
                    try:
                        self.con.execute(TARGETS_SQL,
                            [market, 'registrations', pk, float(regs_val)])
                        targets_count += 1
                    except Exception as e:
                        print(f"  WARN: regs target insert failed {market}/{pk}: {e}")
                cpa_val = cpa_op2.get(month_key)
                if cpa_val and float(cpa_val) > 0:
                    try:
                        self.con.execute(TARGETS_SQL,
                            [market, 'cpa', pk, float(cpa_val)])
                        targets_count += 1
                    except Exception as e:
                        print(f"  WARN: cpa target insert failed {market}/{pk}: {e}")

        print(f"  Load: {targets_count} target rows")
        return total_rows

    def _stage_score(self) -> ScoringResult:
        """Stage 3: Score prior predictions against new actuals."""
        return score_prior_predictions(self.con, self._current_week_key())

    def _stage_update_priors(self) -> int:
        """Stage 3.5: Auto-update seasonal priors for markets with 52+ weeks (Gap 1).

        Inserted between Score and Project so priors are fresh before projections.
        Returns count of markets updated.
        """
        projector = BayesianProjector(self.con, 1.0)
        updated = 0
        for market in ALL_MARKETS:
            try:
                if projector._update_seasonal_priors(market):
                    updated += 1
            except Exception as e:
                print(f"  WARN: seasonal prior update failed for {market}: {e}")
        return updated

    def _stage_project(self, calibration_factor: float) -> list:
        """Stage 4: BayesianProjector for all 10 markets across W+1..W52.

        Generates forward-looking predictions for every future week of the
        current year, not just W+1. This is what lets the chart show a
        prediction trajectory all the way through end-of-year rather than
        flat-lining at W+1. Each run overwrites prior unscored predictions
        (see _write_projections' DELETE clause) so predictions stay fresh
        week over week; scored predictions for past weeks are preserved.
        """
        # Gap 2: Read persisted calibration from ps.calibration_state if available
        # Fall back to the scoring result or 1.0
        persisted_cal = calibration_factor
        try:
            cal_row = self.con.execute("""
                SELECT AVG(calibration_factor) as avg_cal
                FROM ps.calibration_state
                WHERE metric_name = 'registrations' AND total_scored >= 3
            """).fetchone()
            if cal_row and cal_row[0] is not None:
                persisted_cal = float(cal_row[0])
                print(f"  Using persisted calibration factor: {persisted_cal:.3f} (from ps.calibration_state)")
            else:
                print(f"  No persisted calibration — using scoring result: {calibration_factor:.3f}")
        except Exception:
            print(f"  Calibration state read failed — using scoring result: {calibration_factor:.3f}")

        projector = BayesianProjector(self.con, persisted_cal)

        # Determine current week, then project every remaining week of the year.
        year_str, wk_str = self._current_week_key().split('-W')
        current_wk = int(wk_str)
        year_int = int(year_str)

        # Build the forward week schedule: W+1 through W52 of the current year.
        # We stop at W52 rather than rolling into next year so a single run
        # writes a bounded, predictable number of rows per market.
        forward_weeks = []
        for wk_num in range(current_wk + 1, 53):
            forward_weeks.append((year_int, wk_num, f"{year_int}-W{wk_num}"))

        # The "primary" projection — W+1 — drives the callout signal and
        # any downstream code that reads the latest projection list. Keep it
        # at index 0 of the returned projections so consumers don't change.
        primary_projections = []
        total_weekly_written = 0
        total_weekly_skipped = 0

        for i, (yr, wk_num, wk_key) in enumerate(forward_weeks):
            week_projections = []
            for market in ALL_MARKETS:
                try:
                    proj = projector.project_market(market, wk_num, wk_key)
                    week_projections.append(proj)
                except Exception as e:
                    if i == 0:
                        # Only log failures loudly for W+1; deeper-out weeks
                        # legitimately fail more often (missing priors, etc.)
                        print(f"  WARN: projection failed for {market} {wk_key}: {e}")
                        traceback.print_exc()
                    total_weekly_skipped += 1

            written = self._write_projections(week_projections, wk_key)
            total_weekly_written += written

            if i == 0:
                primary_projections = week_projections

        print(f"  Weekly: {len(forward_weeks)} future weeks × {len(ALL_MARKETS)} markets → "
              f"{total_weekly_written} forecast rows written "
              f"({total_weekly_skipped} projections skipped)")

        # ── Gap 3: Monthly + Quarterly projections ──
        # Derive current month and quarter from the first forward week (W+1).
        try:
            from datetime import timedelta
            if forward_weeks:
                _yr, next_wk_num, _ = forward_weeks[0]
            else:
                next_wk_num = current_wk + 1
            jan4 = datetime(year_int, 1, 4)
            start_of_w1 = jan4 - timedelta(days=jan4.weekday())
            target_date = start_of_w1 + timedelta(weeks=next_wk_num - 1)
            current_month = target_date.month
            current_quarter = (current_month - 1) // 3 + 1
            month_key = f"{year_int}-M{current_month:02d}"
            quarter_key = f"{year_int}-Q{current_quarter}"

            monthly_projections = []
            quarterly_projections = []
            for market in ALL_MARKETS:
                try:
                    mp = projector.project_market_monthly(market, month_key)
                    if mp:
                        monthly_projections.append(mp)
                except Exception as e:
                    print(f"  WARN: monthly projection failed for {market}: {e}")

                try:
                    qp = projector.project_market_quarterly(market, quarter_key)
                    if qp:
                        quarterly_projections.append(qp)
                except Exception as e:
                    print(f"  WARN: quarterly projection failed for {market}: {e}")

            # Write monthly + quarterly to ps.forecasts
            m_written = self._write_projections(monthly_projections, month_key, period_type='monthly')
            q_written = self._write_projections(quarterly_projections, quarter_key, period_type='quarterly')
            total_weekly_written += m_written + q_written
            print(f"  Monthly: {len(monthly_projections)} markets, Quarterly: {len(quarterly_projections)} markets")
        except Exception as e:
            print(f"  WARN: monthly/quarterly projections failed: {e}")
            traceback.print_exc()

        print(f"  Project: {len(primary_projections)} markets (W+1), "
              f"{total_weekly_written} total forecast rows written")
        return primary_projections

    def _write_projections(self, projections: list, target_period: str,
                           period_type: str = 'weekly') -> int:
        """Write MarketProjection list to ps.forecasts with scored=false."""
        forecast_date = datetime.now().strftime('%Y-%m-%d')
        written = 0

        # Compute lead_weeks: distance from current week to target_period
        current_wk_key = self._current_week_key()
        lead_weeks = None
        if period_type == 'weekly' and '-W' in target_period and '-W' in current_wk_key:
            try:
                cur_yr, cur_wk = current_wk_key.split('-W')
                tgt_yr, tgt_wk = target_period.split('-W')
                lead_weeks = (int(tgt_yr) - int(cur_yr)) * 52 + int(tgt_wk) - int(cur_wk)
            except (ValueError, IndexError):
                lead_weeks = None
        elif period_type == 'monthly' and '-M' in target_period and '-W' in current_wk_key:
            try:
                cur_yr, cur_wk = current_wk_key.split('-W')
                tgt_yr, tgt_m = target_period.split('-M')
                # Approximate: month midpoint week ≈ (month-1)*4.33 + 2
                tgt_approx_wk = int((int(tgt_m) - 1) * 4.33 + 2)
                lead_weeks = (int(tgt_yr) - int(cur_yr)) * 52 + tgt_approx_wk - int(cur_wk)
            except (ValueError, IndexError):
                lead_weeks = None
        elif period_type == 'quarterly' and '-Q' in target_period and '-W' in current_wk_key:
            try:
                cur_yr, cur_wk = current_wk_key.split('-W')
                tgt_yr, tgt_q = target_period.split('-Q')
                # Approximate: quarter midpoint week ≈ (quarter-1)*13 + 7
                tgt_approx_wk = int((int(tgt_q) - 1) * 13 + 7)
                lead_weeks = (int(tgt_yr) - int(cur_yr)) * 52 + tgt_approx_wk - int(cur_wk)
            except (ValueError, IndexError):
                lead_weeks = None

        for proj in projections:
            if proj is None or proj.total_regs == 0:
                continue

            # Write total, brand, nb as separate rows
            rows_to_write = [
                ('registrations', proj.total_regs, proj.ci_regs_low, proj.ci_regs_high),
                ('cost', proj.total_cost, None, None),
                ('brand_registrations', proj.brand.regs, None, None),
                ('nb_registrations', proj.nb.regs, None, None),
            ]

            for metric, value, ci_l, ci_h in rows_to_write:
                if value is None or value == 0:
                    continue
                try:
                    # Delete existing unscored forecast for same market+metric+period
                    self.con.execute("""
                        DELETE FROM ps.forecasts
                        WHERE market = ? AND metric_name = ? AND target_period = ?
                        AND (scored IS NULL OR scored = false)
                    """, [proj.market, metric, target_period])

                    self.con.execute("""
                        INSERT INTO ps.forecasts
                        (market, channel, metric_name, forecast_date, target_period,
                         period_type, predicted_value, confidence_low, confidence_high,
                         method, scored, lead_weeks, prediction_run_id)
                        VALUES (?, 'ps', ?, ?, ?, ?, ?, ?, ?, ?, false, ?, ?)
                    """, [proj.market, metric, forecast_date, target_period,
                          period_type, value, ci_l, ci_h, proj.method,
                          lead_weeks, self.prediction_run_id])
                    written += 1
                except Exception as e:
                    print(f"  WARN: forecast write failed {proj.market}/{metric}: {e}")

            # Write revision for tracking
            try:
                existing = self.con.execute(f"""
                    SELECT MAX(revision_number) FROM ps.forecast_revisions
                    WHERE market = '{proj.market}' AND metric_name = 'registrations'
                    AND target_period = '{target_period}'
                """).fetchone()
                rev_num = (existing[0] or 0) + 1 if existing and existing[0] else 1
                rev_id = f"{proj.market}-registrations-{target_period}-r{rev_num}"

                self.con.execute("""
                    INSERT OR IGNORE INTO ps.forecast_revisions
                    (revision_id, market, channel, metric_name, target_period,
                     period_type, revision_number, forecast_date, predicted_value,
                     confidence_low, confidence_high, reason)
                    VALUES (?, ?, 'ps', 'registrations', ?, 'weekly', ?, ?, ?, ?, ?, ?)
                """, [rev_id, proj.market, target_period, rev_num,
                      forecast_date, proj.total_regs, proj.ci_regs_low,
                      proj.ci_regs_high, f"WBR pipeline; {proj.method}"])
            except Exception:
                pass  # Revision tracking is best-effort

        return written

    def _stage_callout_signal(self, projections: list) -> None:
        """Stage 5: Write JSON signal file for callout skill trigger."""
        signal = {
            'week': self._current_week_key(),
            'timestamp': datetime.now().isoformat(),
            'markets': [p.market for p in projections if p and p.total_regs > 0],
            'source': 'wbr_pipeline',
        }
        signal_dir = os.path.expanduser('~/shared/tools/prediction')
        signal_path = os.path.join(signal_dir, 'callout-signal.json')
        with open(signal_path, 'w') as f:
            json.dump(signal, f, indent=2)
        print(f"  Callout signal: {signal_path}")

    def _stage_dive_update(self) -> bool:
        """Stage 6: Update MotherDuck dive via MD_UPDATE_DIVE_CONTENT."""
        if not os.path.exists(DIVE_JSX_PATH):
            print(f"  WARN: dive JSX not found at {DIVE_JSX_PATH}")
            return False

        with open(DIVE_JSX_PATH, 'r') as f:
            jsx_content = f.read()

        try:
            self.con.execute(
                "CALL MD_UPDATE_DIVE_CONTENT("
                "required_resources := []::STRUCT(url VARCHAR, alias VARCHAR)[], "
                "api_version := 1, "
                "description := 'WBR Pipeline Dashboard', "
                "content := ?, "
                "id := ?)",
                [jsx_content, DIVE_ID],
            )
            print(f"  Dive updated: {DIVE_ID}")
            return True
        except Exception as e:
            print(f"  WARN: dive update failed: {e}")
            return False

    def _stage_report(self, result: PipelineResult) -> str:
        """Stage 7: Print summary and record duration."""
        result.duration_seconds = round(time.time() - self._start_time, 1)

        lines = [
            f"\n{'='*60}",
            f"WBR Pipeline — {result.week}",
            f"{'='*60}",
            f"  xlsx:        {os.path.basename(result.xlsx_path)}",
            f"  markets:     {', '.join(result.markets_processed) if result.markets_processed else 'none'}",
            f"  rows loaded: {result.rows_loaded}",
            f"  scored:      {result.predictions_scored} predictions",
            f"  projected:   {result.projections_written} forecast rows",
            f"  calibration: {result.calibration:.2f}",
            f"  dive:        {'✓' if result.dive_updated else '✗'}",
            f"  stages OK:   {', '.join(result.stages_completed)}",
        ]
        if result.stages_failed:
            lines.append(f"  stages FAIL: {', '.join(result.stages_failed)}")
        if result.errors:
            lines.append(f"  errors:")
            for err in result.errors:
                lines.append(f"    - {err[:200]}")
        lines.append(f"  duration:    {result.duration_seconds}s")
        lines.append(f"{'='*60}\n")

        report = '\n'.join(lines)
        print(report)
        return report

    # ── Helpers ─────────────────────────────────────────────────────────

    def _current_week_key(self) -> str:
        """Return the current week key in ISO format (e.g. '2026-W14')."""
        if self.week_override:
            return self.week_override
        # Fallback: current ISO week
        now = datetime.now()
        return f"{now.year}-W{now.isocalendar()[1]:02d}"

    def _log_run(self, result: PipelineResult):
        """Write run metadata to ps.pipeline_runs for auditability."""
        try:
            run_id = f"run-{result.week}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.con.execute("""
                INSERT INTO ps.pipeline_runs
                (run_id, week, xlsx_path, started_at, completed_at,
                 stages_completed, stages_failed, markets_processed,
                 rows_loaded, projections_written, predictions_scored, errors)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                run_id, result.week, result.xlsx_path,
                datetime.fromtimestamp(self._start_time).isoformat(),
                datetime.now().isoformat(),
                ','.join(result.stages_completed),
                ','.join(result.stages_failed),
                ','.join(result.markets_processed),
                result.rows_loaded, result.projections_written,
                result.predictions_scored,
                '; '.join(result.errors) if result.errors else None,
            ])
        except Exception as e:
            print(f"  WARN: pipeline_runs log failed: {e}")

    # ── Main orchestrator ──────────────────────────────────────────────

    def run(self) -> PipelineResult:
        """Execute all 7 stages sequentially. Fail-forward on non-critical stages."""
        self._start_time = time.time()
        result = PipelineResult(
            week=self._current_week_key() if self.week_override else '',
            xlsx_path=self.xlsx_path,
        )

        # Connect to MotherDuck
        try:
            self._connect()
            self._ensure_schema()
        except Exception as e:
            result.errors.append(f"Connection failed: {e}")
            result.stages_failed.append('connect')
            return result

        # If week not set yet, it will be set after ingest
        if self.week_override:
            result.week = self.week_override

        projections = []

        # ── Stage 1: Ingest (CRITICAL — abort on failure) ──
        try:
            print("Stage 1: Ingest...")
            ingest_results, monthly_actuals, monthly_budgets = self._stage_ingest()
            result.markets_processed = [m for m in ingest_results.keys()
                                         if isinstance(ingest_results.get(m), dict)
                                         and 'error' not in ingest_results[m]]
            result.stages_completed.append('ingest')
            print(f"  Ingest: {len(result.markets_processed)} markets parsed")
        except Exception as e:
            result.stages_failed.append('ingest')
            result.errors.append(f"Ingest: {e}")
            print(f"  FATAL: Ingest failed — {e}")
            traceback.print_exc()
            self._stage_report(result)
            if self.con:
                self._log_run(result)
                self.con.close()
            return result

        # ── Stage 2: Load ──
        try:
            print("Stage 2: Load to MotherDuck...")
            result.rows_loaded = self._stage_load(
                ingest_results, monthly_actuals, monthly_budgets)
            result.stages_completed.append('load')
        except Exception as e:
            result.stages_failed.append('load')
            result.errors.append(f"Load: {e}")
            print(f"  ERROR: Load failed — {e}")
            traceback.print_exc()

        # ── Stage 3: Score ──
        try:
            print("Stage 3: Score prior predictions...")
            scoring = self._stage_score()
            result.predictions_scored = scoring.predictions_scored
            result.calibration = scoring.calibration
            result.stages_completed.append('score')
            print(f"  Score: {scoring.predictions_scored} scored "
                  f"({scoring.hits}H/{scoring.misses}M/{scoring.surprises}S), "
                  f"calibration={scoring.calibration:.2f}")
        except Exception as e:
            result.stages_failed.append('score')
            result.errors.append(f"Score: {e}")
            result.calibration = 1.0
            print(f"  ERROR: Score failed — {e}")
            traceback.print_exc()

        # ── Stage 3.5: Update Seasonal Priors (Gap 1) ──
        try:
            print("Stage 3.5: Update seasonal priors...")
            priors_updated = self._stage_update_priors()
            result.stages_completed.append('update_priors')
            print(f"  Priors: {priors_updated} markets updated")
        except Exception as e:
            result.stages_failed.append('update_priors')
            result.errors.append(f"Update priors: {e}")
            print(f"  ERROR: Prior update failed — {e}")
            traceback.print_exc()

        # ── Stage 4: Project ──
        try:
            print("Stage 4: Project all markets...")
            projections = self._stage_project(result.calibration)
            result.projections_written = sum(
                1 for p in projections if p and p.total_regs > 0)
            result.stages_completed.append('project')
        except Exception as e:
            result.stages_failed.append('project')
            result.errors.append(f"Project: {e}")
            print(f"  ERROR: Project failed — {e}")
            traceback.print_exc()

        # ── Stage 5: Callout Signal ──
        try:
            print("Stage 5: Callout signal...")
            self._stage_callout_signal(projections)
            result.stages_completed.append('callout_signal')
        except Exception as e:
            result.stages_failed.append('callout_signal')
            result.errors.append(f"Callout: {e}")
            print(f"  ERROR: Callout signal failed — {e}")

        # ── Stage 6: Dive Update ──
        try:
            print("Stage 6: Dive update...")
            result.dive_updated = self._stage_dive_update()
            result.stages_completed.append('dive_update')
        except Exception as e:
            result.stages_failed.append('dive_update')
            result.errors.append(f"Dive: {e}")
            result.dive_updated = False
            print(f"  ERROR: Dive update failed — {e}")

        # ── Stage 7: Report ──
        try:
            print("Stage 7: Report...")
            self._stage_report(result)
            result.stages_completed.append('report')
        except Exception as e:
            result.stages_failed.append('report')
            result.errors.append(f"Report: {e}")

        # Log run to ps.pipeline_runs
        self._log_run(result)

        # Close connection
        if self.con:
            self.con.close()

        return result


# ── CLI entry point ────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='WBR Pipeline — consolidated orchestrator')
    parser.add_argument('xlsx_path', help='Path to WW Dashboard xlsx file')
    parser.add_argument('--week', default=None, help='Week override (e.g. 2026-W14)')
    args = parser.parse_args()

    result = WBRPipeline(args.xlsx_path, week_override=args.week).run()
