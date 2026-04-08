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

    return ScoringResult(
        predictions_scored=hits + misses + surprises,
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

        print(f"  Load: {total_rows} performance rows, {targets_count} target rows")
        return total_rows

    def _stage_score(self) -> ScoringResult:
        """Stage 3: Score prior predictions against new actuals."""
        return score_prior_predictions(self.con, self._current_week_key())

    def _stage_project(self, calibration_factor: float) -> list:
        """Stage 4: BayesianProjector for all 10 markets."""
        projector = BayesianProjector(self.con, calibration_factor)

        # Determine target week (next week from current)
        year, wk = self._current_week_key().split('-W')
        next_wk_num = int(wk) + 1
        if next_wk_num > 52:
            next_wk_num = 1
            year = str(int(year) + 1)
        next_wk_key = f"{year}-W{next_wk_num}"

        projections = []
        for market in ALL_MARKETS:
            try:
                proj = projector.project_market(market, next_wk_num, next_wk_key)
                projections.append(proj)
            except Exception as e:
                print(f"  WARN: projection failed for {market}: {e}")
                traceback.print_exc()

        # Write projections to ps.forecasts
        written = self._write_projections(projections, next_wk_key)
        print(f"  Project: {len(projections)} markets, {written} forecast rows written")
        return projections

    def _write_projections(self, projections: list, target_period: str) -> int:
        """Write MarketProjection list to ps.forecasts with scored=false."""
        forecast_date = datetime.now().strftime('%Y-%m-%d')
        written = 0

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
                         method, scored)
                        VALUES (?, 'ps', ?, ?, ?, 'weekly', ?, ?, ?, ?, false)
                    """, [proj.market, metric, forecast_date, target_period,
                          value, ci_l, ci_h, proj.method])
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
