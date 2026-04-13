"""BayesianProjector — bridges BayesianCore to MotherDuck data.

Fetches historical performance and seasonal priors from MotherDuck,
injects seasonality into BayesianCore priors, applies market-specific
ie%CCP constraints, and produces MarketProjection dataclasses.

Enhanced with monthly data awareness: cross-validates weekly seasonal
priors against monthly patterns and computes MTD pacing vs OP2 targets.
"""

import sys
import os
import math
import logging

from .core import BayesianCore
from .ptypes import (
    PriorState, PosteriorState, SegmentForecast, MarketProjection,
)

logger = logging.getLogger(__name__)

ALL_MARKETS = ['AU', 'MX', 'US', 'CA', 'JP', 'UK', 'DE', 'FR', 'IT', 'ES']

# Market strategy profiles
MARKET_STRATEGY = {
    'AU': {'type': 'efficiency', 'ieccp_target': None, 'ieccp_range': None},
    'MX': {'type': 'ieccp_bound', 'ieccp_target': 1.0, 'ieccp_range': (0.90, 1.10)},
    'JP': {'type': 'brand_dominant', 'ieccp_target': None, 'ieccp_range': (0.30, 0.50)},
    'US': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
    'CA': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
    'UK': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
    'DE': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
    'FR': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
    'IT': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
    'ES': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
}


class BayesianProjector:
    """Bridges BayesianCore to MotherDuck data with seasonal prior injection."""

    def __init__(self, con, calibration_factor: float = 1.0):
        self.con = con
        self.calibration_factor = calibration_factor
        self.core = BayesianCore()
        self._priors_updated = set()  # Gap 1: track which markets had priors updated this instance

    # ── Data fetching ──────────────────────────────────────────────────

    def _fetch_history(self, market: str) -> list:
        """Pull weekly performance from ps.performance, up to 170 weeks."""
        rows = self.con.execute(f"""
            SELECT period_key, period_start,
                   registrations, cost, cpa, clicks, impressions, cpc, cvr, ctr,
                   brand_registrations, brand_cost, brand_cpa, brand_clicks, brand_cpc, brand_cvr,
                   nb_registrations, nb_cost, nb_cpa, nb_clicks, nb_cpc, nb_cvr,
                   ieccp
            FROM ps.performance
            WHERE market = '{market}' AND period_type = 'weekly'
            ORDER BY period_start DESC
            LIMIT 170
        """).fetchall()
        cols = [
            'period_key', 'period_start',
            'regs', 'cost', 'cpa', 'clicks', 'impressions', 'cpc', 'cvr', 'ctr',
            'brand_regs', 'brand_cost', 'brand_cpa', 'brand_clicks', 'brand_cpc', 'brand_cvr',
            'nb_regs', 'nb_cost', 'nb_cpa', 'nb_clicks', 'nb_cpc', 'nb_cvr',
            'ieccp',
        ]
        return [dict(zip(cols, r)) for r in rows]

    def _fetch_seasonal_priors(self, market: str) -> dict:
        """Pull seasonal factors from ps.seasonal_priors. Returns {week_num: factor}.
        
        TODO (deferred 2026-04-13): Incorporate 2025 YoY data into seasonal priors.
        The 2025 WW Dashboard (AB SEM WW Dashboard_Y25 Final.xlsx) has weekly data per market
        going back to 2022. This should be ingested into ps.seasonal_priors to give the model
        real seasonal patterns instead of single-year estimates. HIGH PRIORITY for next WBR run.
        See session-log.md [2026-04-13] consolidated open items.
        """
        rows = self.con.execute(f"""
            SELECT week_of_year, seasonal_index
            FROM ps.seasonal_priors
            WHERE market = '{market}'
        """).fetchall()
        return {int(r[0]): float(r[1]) for r in rows}

    def _update_seasonal_priors(self, market: str) -> bool:
        """Gap 1: Auto-update seasonal priors from accumulated weekly data.

        Only updates if:
        - Market has 52+ weeks of data
        - Market hasn't been updated this instance (class-level cache)
        - Last update was >7 days ago (or never)

        Returns True if priors were updated, False otherwise.
        """
        if market in self._priors_updated:
            return False

        # Check if last update was >7 days ago
        try:
            last_update = self.con.execute(f"""
                SELECT MAX(updated_at) FROM ps.seasonal_priors
                WHERE market = '{market}' AND source = 'auto_update'
            """).fetchone()
            if last_update and last_update[0]:
                from datetime import datetime, timedelta
                last_ts = last_update[0]
                if hasattr(last_ts, 'timestamp'):
                    if (datetime.now() - last_ts).days < 7:
                        self._priors_updated.add(market)
                        return False
        except Exception:
            pass  # If check fails, proceed with update

        # Fetch all weekly history for this market
        rows = self.con.execute(f"""
            SELECT period_key, period_start, registrations
            FROM ps.performance
            WHERE market = '{market}' AND period_type = 'weekly'
            AND registrations IS NOT NULL AND registrations > 0
            ORDER BY period_start ASC
        """).fetchall()

        if len(rows) < 52:
            self._priors_updated.add(market)
            return False

        # Compute seasonal factors: for each week_of_year, mean(regs) / overall_mean
        from collections import defaultdict
        week_buckets = defaultdict(list)
        all_regs = []

        for pk, ps_date, regs in rows:
            reg_val = float(regs)
            all_regs.append(reg_val)
            # Extract week of year from period_key (e.g. '2026-W14' → 14)
            try:
                woy = int(str(pk).split('-W')[1])
            except (IndexError, ValueError):
                # Fallback: use position mod 52
                woy = len(all_regs) % 52
                if woy == 0:
                    woy = 52
            week_buckets[woy].append(reg_val)

        overall_mean = sum(all_regs) / len(all_regs) if all_regs else 1.0
        if overall_mean <= 0:
            self._priors_updated.add(market)
            return False

        # Fetch existing stored priors
        existing = self._fetch_seasonal_priors(market)

        # Compute new data-derived factors and blend with existing — batch upsert
        upsert_rows = []
        for woy in range(1, 53):
            bucket = week_buckets.get(woy, [])
            if not bucket:
                continue

            data_factor = (sum(bucket) / len(bucket)) / overall_mean
            existing_factor = existing.get(woy, 1.0)

            # Blend: 0.8 * data-derived + 0.2 * existing (heavier on data now)
            blended = 0.8 * data_factor + 0.2 * existing_factor

            # Confidence based on sample size
            confidence = min(0.95, 0.5 + len(bucket) * 0.1)
            notes = f"n={len(bucket)}, data={data_factor:.3f}, prior={existing_factor:.3f}"
            upsert_rows.append((market, woy, round(blended, 4), round(confidence, 2), notes))

        if upsert_rows:
            try:
                self.con.executemany("""
                    INSERT OR REPLACE INTO ps.seasonal_priors
                    (market, week_of_year, seasonal_index, confidence, source, notes, updated_at)
                    VALUES (?, ?, ?, ?, 'auto_update', ?, NOW())
                """, upsert_rows)
            except Exception as e:
                logger.warning(f"{market}: batch seasonal prior upsert failed: {e}")

        self._priors_updated.add(market)
        return True

    def _fetch_ieccp(self, market: str) -> float | None:
        """Get latest ie%CCP from ps.performance for this market."""
        rows = self.con.execute(f"""
            SELECT ieccp FROM ps.performance
            WHERE market = '{market}' AND period_type = 'weekly' AND ieccp IS NOT NULL
            ORDER BY period_start DESC LIMIT 1
        """).fetchall()
        return float(rows[0][0]) if rows and rows[0][0] is not None else None

    # ── Monthly data methods ───────────────────────────────────────────

    def _fetch_monthly_history(self, market: str) -> list:
        """Read monthly actuals from ps.performance for both 2025 and 2026."""
        rows = self.con.execute(f"""
            SELECT period_key, period_start,
                   registrations, cost, cpa,
                   brand_registrations, brand_cost, brand_cpa,
                   nb_registrations, nb_cost, nb_cpa
            FROM ps.performance
            WHERE market = '{market}' AND period_type = 'monthly'
            ORDER BY period_start ASC
        """).fetchall()
        cols = [
            'period_key', 'period_start',
            'regs', 'cost', 'cpa',
            'brand_regs', 'brand_cost', 'brand_cpa',
            'nb_regs', 'nb_cost', 'nb_cpa',
        ]
        return [dict(zip(cols, r)) for r in rows]

    def _fetch_monthly_targets(self, market: str) -> dict:
        """Read OP2 targets from ps.targets for registrations, cost, and cpa.

        Returns {period_key: {'registrations': val, 'cost': val, 'cpa': val}}.
        """
        rows = self.con.execute(f"""
            SELECT period_key, metric_name, target_value
            FROM ps.targets
            WHERE market = '{market}'
            ORDER BY period_key
        """).fetchall()
        targets = {}
        for pk, metric, val in rows:
            if pk not in targets:
                targets[pk] = {}
            targets[pk][metric] = float(val) if val else None
        return targets

    def _compute_monthly_pacing(self, market: str, target_week_key: str) -> dict:
        """Compute MTD pacing: cumulative weekly actuals vs monthly OP2 target.

        Returns dict with mtd_regs, mtd_cost, monthly_op2_regs, monthly_op2_cost,
        pacing_regs_pct, pacing_cost_pct. Empty dict if insufficient data.
        """
        # Derive current month from the target week's period_start
        # target_week_key like '2026-W15' — get the latest week's period_start
        try:
            week_rows = self.con.execute(f"""
                SELECT period_start FROM ps.performance
                WHERE market = '{market}' AND period_type = 'weekly'
                ORDER BY period_start DESC LIMIT 1
            """).fetchall()
            if not week_rows:
                return {}
            latest_start = week_rows[0][0]
            # Extract year and month
            if hasattr(latest_start, 'year'):
                year = latest_start.year
                month = latest_start.month
            else:
                # String date
                parts = str(latest_start).split('-')
                year = int(parts[0])
                month = int(parts[1])
        except Exception:
            return {}

        month_key = f"{year}-M{month:02d}"

        # Get MTD weekly actuals for this month
        try:
            mtd = self.con.execute(f"""
                SELECT SUM(registrations) as mtd_regs, SUM(cost) as mtd_cost
                FROM ps.performance
                WHERE market = '{market}' AND period_type = 'weekly'
                AND EXTRACT(YEAR FROM period_start) = {year}
                AND EXTRACT(MONTH FROM period_start) = {month}
            """).fetchone()
        except Exception:
            return {}

        if not mtd or (mtd[0] is None and mtd[1] is None):
            return {}

        mtd_regs = float(mtd[0]) if mtd[0] else 0
        mtd_cost = float(mtd[1]) if mtd[1] else 0

        # Get OP2 targets for this month
        targets = self._fetch_monthly_targets(market)
        month_targets = targets.get(month_key, {})
        op2_regs = month_targets.get('registrations')
        op2_cost = month_targets.get('cost')

        pacing_regs = round(mtd_regs * 100.0 / op2_regs, 1) if op2_regs else None
        pacing_cost = round(mtd_cost * 100.0 / op2_cost, 1) if op2_cost else None

        return {
            'mtd_regs': mtd_regs,
            'mtd_cost': mtd_cost,
            'monthly_op2_regs': op2_regs,
            'monthly_op2_cost': op2_cost,
            'pacing_regs_pct': pacing_regs,
            'pacing_cost_pct': pacing_cost,
        }

    def _cross_validate_seasonal_priors(self, market: str,
                                         weekly_seasonality: dict) -> None:
        """Soft check: compare weekly seasonal priors against monthly patterns.

        If 12+ months of monthly data exist, compute monthly seasonal factors
        and log warnings when weekly priors disagree by >30%.
        """
        monthly = self._fetch_monthly_history(market)
        if len(monthly) < 12:
            return

        # Compute monthly seasonal factors from regs
        monthly_regs = []
        for m in monthly:
            r = m.get('regs')
            if r and r > 0:
                monthly_regs.append((m['period_key'], float(r)))

        if len(monthly_regs) < 12:
            return

        avg_monthly = sum(v for _, v in monthly_regs) / len(monthly_regs)
        if avg_monthly <= 0:
            return

        # Build month-level seasonal factors
        monthly_factors = {}
        for pk, val in monthly_regs:
            # period_key like '2025-M06' → month 6
            try:
                month_num = int(pk.split('-M')[1])
                monthly_factors[month_num] = val / avg_monthly
            except (IndexError, ValueError):
                continue

        if not monthly_factors or not weekly_seasonality:
            return

        # Map weekly seasonal keys to approximate months
        # Week 1-4 → Jan, 5-8 → Feb, etc.
        for week_key, weekly_factor in weekly_seasonality.items():
            approx_month = (week_key // 4) + 1
            approx_month = min(12, max(1, approx_month))
            monthly_factor = monthly_factors.get(approx_month)
            if monthly_factor is None:
                continue

            # Check for >30% disagreement
            if monthly_factor > 0:
                ratio = weekly_factor / monthly_factor
                if abs(ratio - 1.0) > 0.30:
                    logger.warning(
                        f"{market} W{week_key}: weekly seasonal={weekly_factor:.2f} "
                        f"vs monthly M{approx_month:02d}={monthly_factor:.2f} "
                        f"(ratio={ratio:.2f}, >30% disagreement)"
                    )

    # ── Seasonality injection ──────────────────────────────────────────

    def _inject_seasonality(self, prior: PriorState, seasonal: dict) -> PriorState:
        """Merge ps.seasonal_priors into PriorState.seasonality.

        - If prior.seasonality is empty (< 52 weeks data): use stored priors directly.
        - If prior.seasonality has entries (>= 52 weeks): blend 0.7*data + 0.3*stored.
        - Returns NEW PriorState — does not mutate original.
        - All resulting factors are positive (> 0.0).
        """
        if not seasonal:
            # No stored priors — return copy unchanged
            return PriorState(
                mean=prior.mean, variance=prior.variance,
                n_observations=prior.n_observations,
                trend_slope=prior.trend_slope,
                trend_confidence=prior.trend_confidence,
                seasonality=dict(prior.seasonality),
                volatility=prior.volatility,
            )

        new_seasonality = {}

        if not prior.seasonality:
            # < 52 weeks: use stored priors directly
            for wn, factor in seasonal.items():
                key = wn % 52
                new_seasonality[key] = max(0.001, float(factor))
        else:
            # >= 52 weeks: blend data-derived with stored
            all_keys = set(prior.seasonality.keys()) | {wn % 52 for wn in seasonal.keys()}
            for key in all_keys:
                data_val = prior.seasonality.get(key, 1.0)
                stored_val = seasonal.get(key, seasonal.get(key + 52, 1.0))
                blended = 0.7 * data_val + 0.3 * stored_val
                new_seasonality[key] = max(0.001, blended)

        return PriorState(
            mean=prior.mean, variance=prior.variance,
            n_observations=prior.n_observations,
            trend_slope=prior.trend_slope,
            trend_confidence=prior.trend_confidence,
            seasonality=new_seasonality,
            volatility=prior.volatility,
        )

    # ── ie%CCP constraint ──────────────────────────────────────────────

    def _apply_ieccp_constraint(self, nb_forecast: SegmentForecast,
                                 market: str, ieccp: float | None) -> SegmentForecast:
        """Cap NB projections by ie%CCP bounds per market strategy."""
        strategy = MARKET_STRATEGY.get(market, {})
        stype = strategy.get('type', 'balanced')

        if stype == 'efficiency' or ieccp is None:
            return nb_forecast
        if stype == 'brand_dominant':
            return nb_forecast

        ieccp_range = strategy.get('ieccp_range')
        ieccp_target = strategy.get('ieccp_target')
        spend_adj = 1.0

        if stype == 'ieccp_bound' and ieccp_target:
            deviation = ieccp - ieccp_target
            if abs(deviation) < 0.05:
                return nb_forecast
            spend_adj = 1.0 - (deviation * 0.8)
            spend_adj = max(0.6, min(1.4, spend_adj))
        elif stype == 'balanced' and ieccp_range:
            low, high = ieccp_range
            if low <= ieccp <= high:
                return nb_forecast
            if ieccp > high:
                overshoot = ieccp - high
                spend_adj = max(0.8, 1.0 - overshoot * 0.3)
            else:
                undershoot = low - ieccp
                spend_adj = min(1.15, 1.0 + undershoot * 0.2)
        else:
            return nb_forecast

        adj_cost = nb_forecast.cost * spend_adj
        adj_clicks = nb_forecast.clicks * spend_adj
        adj_regs = nb_forecast.regs * spend_adj
        adj_cpa = adj_cost / adj_regs if adj_regs > 0 else nb_forecast.cpa

        return SegmentForecast(
            regs=round(adj_regs),
            cost=round(adj_cost, 2),
            cpa=round(adj_cpa, 2),
            clicks=round(adj_clicks),
        )

    # ── Segment projection helper ──────────────────────────────────────

    def _project_segment(self, history: list, segment: str,
                         target_week_num: int, seasonal_adj: float) -> SegmentForecast:
        """Project a single segment (brand or nb) using BayesianCore."""
        prefix = f'{segment}_'
        metric_key = f'{prefix}regs'

        # Build history dicts for BayesianCore (it expects list of dicts with metric key)
        hist_for_core = [{'value': float(w.get(metric_key, 0) or 0)} for w in reversed(history)]
        if not hist_for_core or all(h['value'] == 0 for h in hist_for_core):
            return SegmentForecast(regs=0, cost=0, cpa=0, clicks=0)

        prior = self.core.build_prior(hist_for_core, 'value')
        recent_evidence = [{'value': float(w.get(metric_key, 0) or 0)} for w in history[:4]]
        posterior = self.core.update_posterior(prior, recent_evidence, self.calibration_factor)

        base_regs = self.core.point_estimate(posterior, horizon=1)
        adj_regs = max(0, base_regs * seasonal_adj)

        # Cost projection: use recent average cost-per-reg ratio
        recent_costs = [float(w.get(f'{prefix}cost', 0) or 0) for w in history[:8]]
        recent_regs = [float(w.get(metric_key, 0) or 0) for w in history[:8]]
        total_cost = sum(recent_costs)
        total_regs_hist = sum(recent_regs)
        avg_cpa = total_cost / total_regs_hist if total_regs_hist > 0 else 0
        adj_cost = adj_regs * avg_cpa

        # Clicks
        recent_clicks = [float(w.get(f'{prefix}clicks', 0) or 0) for w in history[:8]]
        avg_clicks = sum(recent_clicks) / len(recent_clicks) if recent_clicks else 0
        adj_clicks = avg_clicks * seasonal_adj

        adj_cpa = adj_cost / adj_regs if adj_regs > 0 else 0

        return SegmentForecast(
            regs=round(adj_regs),
            cost=round(adj_cost, 2),
            cpa=round(adj_cpa, 2),
            clicks=round(adj_clicks),
        )

    # ── Gap 3: Monthly + Quarterly Bayesian models ───────────────────

    def project_market_monthly(self, market: str, target_month_key: str) -> MarketProjection | None:
        """Gap 3: Proper monthly Bayesian projection using monthly history.

        Args:
            market: Market code (e.g. 'AU')
            target_month_key: e.g. '2026-M04'

        Returns MarketProjection with period_type context, or None if insufficient data.
        """
        monthly = self._fetch_monthly_history(market)
        if len(monthly) < 6:
            # Not enough monthly data — fall back to None (caller can skip)
            return None

        # Build prior from monthly regs directly
        hist_for_core = [{'value': float(m.get('regs', 0) or 0)} for m in monthly if m.get('regs')]
        if len(hist_for_core) < 3:
            return None

        prior = self.core.build_prior(hist_for_core, 'value')

        # Monthly seasonal adjustment: derive from monthly data itself
        monthly_regs = [float(m.get('regs', 0) or 0) for m in monthly if m.get('regs')]
        overall_mean = sum(monthly_regs) / len(monthly_regs) if monthly_regs else 1.0

        # Group by month number for seasonal pattern
        from collections import defaultdict
        month_buckets = defaultdict(list)
        for m in monthly:
            pk = m.get('period_key', '')
            regs = m.get('regs')
            if not regs or not pk:
                continue
            try:
                month_num = int(pk.split('-M')[1])
                month_buckets[month_num].append(float(regs))
            except (IndexError, ValueError):
                continue

        # Target month number
        try:
            target_month_num = int(target_month_key.split('-M')[1])
        except (IndexError, ValueError):
            target_month_num = 1

        seasonal_adj = 1.0
        if overall_mean > 0 and target_month_num in month_buckets:
            bucket = month_buckets[target_month_num]
            seasonal_adj = (sum(bucket) / len(bucket)) / overall_mean

        # Update posterior with recent months
        recent = hist_for_core[-3:] if len(hist_for_core) >= 3 else hist_for_core
        posterior = self.core.update_posterior(prior, recent, self.calibration_factor)

        base_regs = self.core.point_estimate(posterior, horizon=1)
        adj_regs = max(0, base_regs * seasonal_adj)

        # Cost projection from monthly data
        monthly_costs = [float(m.get('cost', 0) or 0) for m in monthly if m.get('cost')]
        monthly_regs_vals = [float(m.get('regs', 0) or 0) for m in monthly if m.get('regs')]
        avg_cpa = (sum(monthly_costs) / sum(monthly_regs_vals)) if sum(monthly_regs_vals) > 0 else 0
        adj_cost = adj_regs * avg_cpa

        # CI
        ci_low, ci_high = self.core.credible_interval(posterior, level=0.7)
        ci_regs_low = max(0, ci_low * seasonal_adj)
        ci_regs_high = ci_high * seasonal_adj

        # OP2 comparison
        vs_op2_spend_pct = None
        try:
            targets = self._fetch_monthly_targets(market)
            month_targets = targets.get(target_month_key, {})
            op2_cost = month_targets.get('cost')
            if op2_cost and op2_cost > 0:
                vs_op2_spend_pct = round((adj_cost / op2_cost - 1) * 100, 1)
        except Exception:
            pass

        brand = SegmentForecast(regs=round(adj_regs * 0.5), cost=round(adj_cost * 0.5, 2), cpa=round(avg_cpa, 2), clicks=0)
        nb = SegmentForecast(regs=round(adj_regs * 0.5), cost=round(adj_cost * 0.5, 2), cpa=round(avg_cpa, 2), clicks=0)

        return MarketProjection(
            market=market,
            brand=brand,
            nb=nb,
            total_regs=round(adj_regs),
            total_cost=round(adj_cost, 2),
            ci_regs_low=round(ci_regs_low),
            ci_regs_high=round(ci_regs_high),
            vs_op2_spend_pct=vs_op2_spend_pct,
            method='bayesian_monthly',
            week=target_month_key,
        )

    def project_market_quarterly(self, market: str, target_quarter_key: str) -> MarketProjection | None:
        """Gap 3: Quarterly projection by summing 3 monthly projections.

        Args:
            market: Market code
            target_quarter_key: e.g. '2026-Q2'

        Returns MarketProjection or None if monthly projections unavailable.
        """
        try:
            year = int(target_quarter_key.split('-Q')[0])
            quarter = int(target_quarter_key.split('-Q')[1])
        except (IndexError, ValueError):
            return None

        # Months in this quarter
        start_month = (quarter - 1) * 3 + 1
        month_keys = [f"{year}-M{m:02d}" for m in range(start_month, start_month + 3)]

        # Sum monthly projections
        total_regs = 0
        total_cost = 0
        ci_low_sum = 0
        ci_high_sum = 0
        months_projected = 0

        for mk in month_keys:
            mp = self.project_market_monthly(market, mk)
            if mp:
                total_regs += mp.total_regs
                total_cost += mp.total_cost
                ci_low_sum += mp.ci_regs_low
                ci_high_sum += mp.ci_regs_high
                months_projected += 1

        if months_projected == 0:
            return None

        # OP2 quarterly target (sum of 3 monthly targets)
        vs_op2_spend_pct = None
        try:
            targets = self._fetch_monthly_targets(market)
            q_op2_cost = 0
            for mk in month_keys:
                mt = targets.get(mk, {})
                c = mt.get('cost')
                if c:
                    q_op2_cost += c
            if q_op2_cost > 0:
                vs_op2_spend_pct = round((total_cost / q_op2_cost - 1) * 100, 1)
        except Exception:
            pass

        avg_cpa = total_cost / total_regs if total_regs > 0 else 0
        brand = SegmentForecast(regs=round(total_regs * 0.5), cost=round(total_cost * 0.5, 2), cpa=round(avg_cpa, 2), clicks=0)
        nb = SegmentForecast(regs=round(total_regs * 0.5), cost=round(total_cost * 0.5, 2), cpa=round(avg_cpa, 2), clicks=0)

        return MarketProjection(
            market=market,
            brand=brand,
            nb=nb,
            total_regs=round(total_regs),
            total_cost=round(total_cost, 2),
            ci_regs_low=round(ci_low_sum),
            ci_regs_high=round(ci_high_sum),
            vs_op2_spend_pct=vs_op2_spend_pct,
            method='bayesian_quarterly',
            week=target_quarter_key,
        )

    # ── Main projection method ─────────────────────────────────────────

    def project_market(self, market: str, target_week_num: int,
                       target_period_key: str) -> MarketProjection:
        """Full projection for one market: Brand + NB + Total."""
        history = self._fetch_history(market)
        if len(history) < 3:
            # Insufficient data — return zero projection
            zero_seg = SegmentForecast(regs=0, cost=0, cpa=0, clicks=0)
            return MarketProjection(
                market=market, brand=zero_seg, nb=zero_seg,
                total_regs=0, total_cost=0, ci_regs_low=0, ci_regs_high=0,
                vs_op2_spend_pct=None, method='insufficient_data',
                week=target_period_key,
            )

        # Build prior from total regs for CI computation
        hist_for_core = [{'value': float(w.get('regs', 0) or 0)} for w in reversed(history)]
        raw_prior = self.core.build_prior(hist_for_core, 'value')

        # Fetch and inject seasonal priors
        seasonal = self._fetch_seasonal_priors(market)
        adjusted_prior = self._inject_seasonality(raw_prior, seasonal)

        # Update posterior with last 4 weeks
        recent_evidence = [{'value': float(w.get('regs', 0) or 0)} for w in history[:4]]
        posterior = self.core.update_posterior(adjusted_prior, recent_evidence, self.calibration_factor)

        # Seasonal adjustment factor for target week
        seasonal_adj = adjusted_prior.seasonality.get(target_week_num % 52, 1.0)

        # Project Brand + NB segments
        strategy = MARKET_STRATEGY.get(market, {})
        stype = strategy.get('type', 'balanced')

        brand = self._project_segment(history, 'brand', target_week_num, seasonal_adj)

        if stype == 'brand_dominant':
            # JP: NB too small to model, use recent average
            recent_nb = [float(w.get('nb_regs', 0) or 0) for w in history[:4]]
            nb_avg = sum(recent_nb) / len(recent_nb) if recent_nb else 0
            nb = SegmentForecast(regs=round(nb_avg), cost=0, cpa=0, clicks=0)
        else:
            nb = self._project_segment(history, 'nb', target_week_num, seasonal_adj)

        # Apply ie%CCP constraint
        ieccp = self._fetch_ieccp(market)
        nb = self._apply_ieccp_constraint(nb, market, ieccp)

        # Totals
        total_regs = brand.regs + nb.regs
        total_cost = brand.cost + nb.cost

        # Apply regime change prior shifts from ps.regime_changes
        try:
            regime_rows = self.con.execute(f"""
                SELECT change_type, expected_impact_pct, confidence, change_date
                FROM ps.regime_changes
                WHERE market = '{market}' AND metric_affected = 'registrations' AND active = TRUE
                ORDER BY change_date
            """).fetchall()
            for rr in regime_rows:
                change_type, impact_pct, conf, change_date = rr
                # Only apply if the target week is AFTER the regime change
                # Convert target_period_key (2026-W15) to approximate date
                from datetime import date, timedelta
                w1_start = date(2025, 12, 29)
                target_date = w1_start + timedelta(weeks=target_week_num - 1)
                if target_date >= change_date:
                    # Scale impact by confidence: full confidence = full impact
                    adj = 1.0 + (impact_pct * conf)
                    total_regs = max(0, round(total_regs * adj))
                    total_cost = max(0, round(total_cost * adj, 2))
                    # Also adjust brand/nb proportionally
                    brand = SegmentForecast(
                        regs=max(0, round(brand.regs * adj)),
                        cost=max(0, round(brand.cost * adj, 2)),
                        cpa=brand.cpa, clicks=brand.clicks)
                    nb = SegmentForecast(
                        regs=max(0, round(nb.regs * adj)),
                        cost=max(0, round(nb.cost * adj, 2)),
                        cpa=nb.cpa, clicks=nb.clicks)
        except Exception:
            pass  # No regime_changes table or query error — proceed without

        # CI from posterior (adjusted by seasonality)
        ci_low, ci_high = self.core.credible_interval(posterior, level=0.7)
        ci_regs_low = max(0, ci_low * seasonal_adj)
        ci_regs_high = ci_high * seasonal_adj

        # Gap 4: Apply CI width adjustment from ps.calibration_state
        try:
            ci_adj_row = self.con.execute(f"""
                SELECT ci_width_adjustment FROM ps.calibration_state
                WHERE market = '{market}' AND metric_name = 'registrations'
            """).fetchone()
            if ci_adj_row and ci_adj_row[0] is not None:
                ci_width_adj = float(ci_adj_row[0])
                if ci_width_adj != 1.0:
                    ci_regs_low = total_regs - (total_regs - ci_regs_low) * ci_width_adj
                    ci_regs_high = total_regs + (ci_regs_high - total_regs) * ci_width_adj
                    ci_regs_low = max(0, ci_regs_low)
        except Exception:
            pass  # No calibration state yet — use raw CI

        # Ensure point estimate is within CI (widen if needed)
        if total_regs < ci_regs_low:
            ci_regs_low = total_regs * 0.85
        if total_regs > ci_regs_high:
            ci_regs_high = total_regs * 1.15

        # OP2 comparison
        vs_op2_spend_pct = None
        try:
            op2_rows = self.con.execute(f"""
                SELECT target_value FROM ps.targets
                WHERE market = '{market}' AND metric_name = 'cost'
                ORDER BY period_key DESC LIMIT 1
            """).fetchall()
            if op2_rows and op2_rows[0][0]:
                weekly_op2 = float(op2_rows[0][0]) / 4.33
                if weekly_op2 > 0:
                    vs_op2_spend_pct = round((total_cost / weekly_op2 - 1) * 100, 1)
        except Exception:
            pass

        # Monthly pacing context
        pacing = {}
        try:
            pacing = self._compute_monthly_pacing(market, target_period_key)
        except Exception as e:
            logger.debug(f"{market}: monthly pacing failed: {e}")

        # Cross-validate weekly seasonal priors against monthly patterns
        try:
            self._cross_validate_seasonal_priors(market, adjusted_prior.seasonality)
        except Exception as e:
            logger.debug(f"{market}: seasonal cross-validation failed: {e}")

        return MarketProjection(
            market=market,
            brand=brand,
            nb=nb,
            total_regs=total_regs,
            total_cost=round(total_cost, 2),
            ci_regs_low=round(ci_regs_low),
            ci_regs_high=round(ci_regs_high),
            vs_op2_spend_pct=vs_op2_spend_pct,
            method='bayesian_seasonal_brand_nb_split',
            week=target_period_key,
            **pacing,
        )
