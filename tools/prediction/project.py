#!/usr/bin/env python3
"""WBR Projection Engine — Brand/NB split with ie%CCP constraints.

Generates next-week, current-month, and current-quarter projections
for all 10 markets. Writes to ps.forecasts in MotherDuck.

Key design decisions:
- Brand and NB are modeled separately (different drivers)
- Brand: seasonality-heavy (YoY week-of-year patterns, events)
- NB: spend-management-heavy (ie%CCP constraint, budget pacing)
- ie%CCP > 1.0 signals NB spend pullback pressure
- Total = Brand + NB (bottom-up, not top-down)
- YoY seasonal index when 52+ weeks available
- Recent 8-week trend weighted 60%, YoY pattern 40%
- Credible intervals widen with horizon
"""

import sys, os, math, json
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional

# ── Config ──
ALL_MARKETS = ['US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP', 'AU', 'MX']

# Market strategy profiles — different markets optimize for different things
MARKET_STRATEGY = {
    # AU: Hit registration OP2 as efficiently as possible. No ie%CCP.
    'AU': {'type': 'efficiency', 'ieccp_target': None, 'ieccp_range': None,
           'notes': 'Optimize regs toward OP2 at lowest CPA. No ie%CCP tracking.'},
    # MX: Stay at 100% ie%CCP with max registrations. ie%CCP is the binding constraint.
    'MX': {'type': 'ieccp_bound', 'ieccp_target': 1.0, 'ieccp_range': (0.90, 1.10),
           'notes': 'ie%CCP=100% is the constraint. Maximize regs within that envelope.'},
    # JP: Brand-dominant. NB is negligible (~7 regs/wk). Weight Brand heavily.
    'JP': {'type': 'brand_dominant', 'ieccp_target': None, 'ieccp_range': (0.30, 0.50),
           'notes': 'Brand drives 99% of regs. NB too small to model meaningfully.'},
    # All others: balanced, 50-65% ie%CCP normal range
    'US': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
    'CA': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
    'UK': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
    'DE': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
    'FR': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
    'IT': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
    'ES': {'type': 'balanced', 'ieccp_target': None, 'ieccp_range': (0.50, 0.65)},
}


@dataclass
class SegmentForecast:
    """Forecast for one segment (Brand or NB)."""
    registrations: float
    cost: float
    cpa: float
    clicks: float
    cvr: float
    cpc: float
    ci_regs_low: float
    ci_regs_high: float
    ci_cost_low: float
    ci_cost_high: float


@dataclass
class MarketProjection:
    """Full projection for one market at one horizon."""
    market: str
    horizon: str           # 'W15', 'M04', 'Q2'
    horizon_label: str     # 'Next Week', 'April', 'Q2 2026'
    brand: SegmentForecast
    nb: SegmentForecast
    total_regs: float
    total_cost: float
    total_cpa: float
    ci_regs_low: float
    ci_regs_high: float
    ci_cost_low: float
    ci_cost_high: float
    ieccp_current: Optional[float]
    ieccp_projected: Optional[float]
    op2_spend: Optional[float]
    vs_op2_spend_pct: Optional[float]
    method: str
    notes: str



def connect_md():
    """Connect to MotherDuck."""
    import duckdb
    token = os.environ.get('MOTHERDUCK_TOKEN',
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJpY2hzY290dHdpbGxAZ21haWwuY29tIiwibWRSZWdpb24iOiJhd3MtdXMtZWFzdC0xIiwic2Vzc2lvbiI6InJpY2hzY290dHdpbGwuZ21haWwuY29tIiwicGF0IjoiVDNIYzFVQWYzT3o1bjVkLS03ckdHNlBjMlpUdVNNbFItT3RXMS1qNzVPUSIsInVzZXJJZCI6ImU2MDhlNDZiLTE4YzctNGE5Ny04M2I2LWE0N2ZhOThmNjBhYyIsImlzcyI6Im1kX3BhdCIsInJlYWRPbmx5IjpmYWxzZSwidG9rZW5UeXBlIjoicmVhZF93cml0ZSIsImlhdCI6MTc3NTQ0MzY0N30.tS0Cab3FQ8_CDZ1PqOo9z09KYHEUFHwuLVXRQrxcHig')
    return duckdb.connect(f'md:ps_analytics?motherduck_token={token}')


def fetch_weekly_history(con, market, max_weeks=170):
    """Pull weekly performance data ordered by period_start DESC."""
    rows = con.execute(f"""
        SELECT period_key, period_start,
               registrations, cost, cpa, clicks, impressions, cpc, cvr, ctr,
               brand_registrations, brand_cost, brand_cpa, brand_clicks, brand_cpc, brand_cvr,
               nb_registrations, nb_cost, nb_cpa, nb_clicks, nb_cpc, nb_cvr,
               ieccp
        FROM ps.performance
        WHERE market = '{market}' AND period_type = 'weekly'
        ORDER BY period_start DESC
        LIMIT {max_weeks}
    """).fetchall()
    cols = ['period_key', 'period_start',
            'regs', 'cost', 'cpa', 'clicks', 'impressions', 'cpc', 'cvr', 'ctr',
            'brand_regs', 'brand_cost', 'brand_cpa', 'brand_clicks', 'brand_cpc', 'brand_cvr',
            'nb_regs', 'nb_cost', 'nb_cpa', 'nb_clicks', 'nb_cpc', 'nb_cvr',
            'ieccp']
    return [dict(zip(cols, r)) for r in rows]


def fetch_op2_spend(con, market, period_key):
    """Get OP2 spend target for a period."""
    rows = con.execute(f"""
        SELECT target_value FROM ps.targets
        WHERE market = '{market}' AND metric_name = 'cost' AND period_key = '{period_key}'
        LIMIT 1
    """).fetchall()
    return rows[0][0] if rows else None


def ols_trend(values):
    """Simple OLS trend slope and R² from a list of values (oldest first)."""
    n = len(values)
    if n < 3:
        return 0.0, 0.0
    mean_y = sum(values) / n
    mean_x = (n - 1) / 2.0
    ss_xy = sum((i - mean_x) * (v - mean_y) for i, v in enumerate(values))
    ss_xx = sum((i - mean_x) ** 2 for i in range(n))
    slope = ss_xy / ss_xx if ss_xx > 0 else 0.0
    predicted = [mean_y + slope * (i - mean_x) for i in range(n)]
    ss_res = sum((v - p) ** 2 for v, p in zip(values, predicted))
    ss_tot = sum((v - mean_y) ** 2 for v in values)
    r2 = max(0.0, 1.0 - ss_res / ss_tot) if ss_tot > 0 else 0.0
    return slope, r2


def seasonal_index(history, target_week_num, metric_key):
    """Compute YoY seasonal adjustment factor for a given week-of-year.
    
    Returns ratio of (avg value in target week-of-year) / (overall avg).
    Requires 52+ weeks. Returns 1.0 if insufficient data.
    """
    if len(history) < 52:
        return 1.0
    
    values_by_woy = {}
    all_vals = []
    for w in history:
        val = w.get(metric_key)
        if val is None or val <= 0:
            continue
        pk = w.get('period_key', '')
        # Extract week number from period_key like "2026-W14"
        try:
            wnum = int(pk.split('W')[-1])
        except:
            continue
        if wnum not in values_by_woy:
            values_by_woy[wnum] = []
        values_by_woy[wnum].append(val)
        all_vals.append(val)
    
    if not all_vals or target_week_num not in values_by_woy:
        return 1.0
    
    overall_avg = sum(all_vals) / len(all_vals)
    if overall_avg <= 0:
        return 1.0
    
    woy_vals = values_by_woy[target_week_num]
    woy_avg = sum(woy_vals) / len(woy_vals)
    
    # Dampen extreme seasonal factors (cap at 0.5x to 2.0x)
    ratio = woy_avg / overall_avg
    return max(0.5, min(2.0, ratio))


def volatility(values):
    """Standard deviation of values."""
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    return (sum((v - mean) ** 2 for v in values) / (len(values) - 1)) ** 0.5


def project_segment(history, segment, target_week_num, weeks_ahead=1):
    """Project a segment (brand or nb) forward.
    
    Args:
        history: list of weekly dicts, most recent first
        segment: 'brand' or 'nb'
        target_week_num: ISO week number we're projecting for
        weeks_ahead: how many weeks forward (1 for next week)
    
    Returns: SegmentForecast
    """
    prefix = f'{segment}_'
    
    # Extract segment values (reverse to oldest-first for trend calc)
    recent_8 = list(reversed(history[:8]))
    all_data = list(reversed(history))
    
    regs_vals = [w.get(f'{prefix}regs', 0) or 0 for w in recent_8]
    cost_vals = [w.get(f'{prefix}cost', 0) or 0 for w in recent_8]
    clicks_vals = [w.get(f'{prefix}clicks', 0) or 0 for w in recent_8]
    
    # CVR and CPC from recent data
    cvr_vals = [w.get(f'{prefix}cvr') for w in recent_8 if w.get(f'{prefix}cvr')]
    cpc_vals = [w.get(f'{prefix}cpc') for w in recent_8 if w.get(f'{prefix}cpc')]
    
    if not regs_vals or sum(regs_vals) == 0:
        return SegmentForecast(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    
    # ── Trend component (60% weight) ──
    regs_slope, regs_r2 = ols_trend(regs_vals)
    cost_slope, _ = ols_trend(cost_vals)
    clicks_slope, _ = ols_trend(clicks_vals)
    
    regs_mean = sum(regs_vals) / len(regs_vals)
    cost_mean = sum(cost_vals) / len(cost_vals)
    clicks_mean = sum(clicks_vals) / len(clicks_vals)
    
    # Trend-based projection
    trend_regs = regs_mean + regs_slope * (len(regs_vals) - 1 + weeks_ahead)
    trend_cost = cost_mean + cost_slope * (len(cost_vals) - 1 + weeks_ahead)
    trend_clicks = clicks_mean + clicks_slope * (len(clicks_vals) - 1 + weeks_ahead)
    
    # ── Seasonal component (40% weight when 52+ weeks available) ──
    seasonal_regs = seasonal_index(all_data, target_week_num, f'{prefix}regs')
    seasonal_cost = seasonal_index(all_data, target_week_num, f'{prefix}cost')
    
    # Blend: 60% trend + 40% seasonal-adjusted mean
    seasonal_weight = 0.4 if len(all_data) >= 52 else 0.0
    trend_weight = 1.0 - seasonal_weight
    
    proj_regs = trend_weight * trend_regs + seasonal_weight * (regs_mean * seasonal_regs)
    proj_cost = trend_weight * trend_cost + seasonal_weight * (cost_mean * seasonal_cost)
    proj_clicks = trend_weight * trend_clicks + seasonal_weight * (clicks_mean * seasonal_cost)
    
    # Floor at 0
    proj_regs = max(0, proj_regs)
    proj_cost = max(0, proj_cost)
    proj_clicks = max(0, proj_clicks)
    
    # Derived metrics
    proj_cpa = proj_cost / proj_regs if proj_regs > 0 else 0
    proj_cvr = proj_regs / proj_clicks if proj_clicks > 0 else (sum(cvr_vals) / len(cvr_vals) if cvr_vals else 0)
    proj_cpc = proj_cost / proj_clicks if proj_clicks > 0 else (sum(cpc_vals) / len(cpc_vals) if cpc_vals else 0)
    
    # ── Credible intervals ──
    regs_vol = volatility(regs_vals)
    cost_vol = volatility(cost_vals)
    # Widen with horizon: sqrt(weeks_ahead) scaling
    horizon_factor = math.sqrt(weeks_ahead)
    ci_regs = 1.04 * regs_vol * horizon_factor  # 70% CI
    ci_cost = 1.04 * cost_vol * horizon_factor
    
    return SegmentForecast(
        registrations=round(proj_regs),
        cost=round(proj_cost, 2),
        cpa=round(proj_cpa, 2),
        clicks=round(proj_clicks),
        cvr=round(proj_cvr, 4),
        cpc=round(proj_cpc, 2),
        ci_regs_low=round(max(0, proj_regs - ci_regs)),
        ci_regs_high=round(proj_regs + ci_regs),
        ci_cost_low=round(max(0, proj_cost - ci_cost), 2),
        ci_cost_high=round(proj_cost + ci_cost, 2),
    )


def apply_ieccp_constraint(nb_forecast, market, ieccp_current, ieccp_trend_slope):
    """Adjust NB forecast based on ie%CCP pressure and market strategy.
    
    Strategy-aware:
    - AU: No ie%CCP adjustment (efficiency strategy, no ie%CCP tracking)
    - MX: ie%CCP=100% is binding. Overshoot → expect spend pullback. Undershoot → room to push.
    - JP: Brand-dominant, NB too small to adjust meaningfully
    - Balanced markets (US/CA/UK/DE/FR/IT/ES): 50-65% normal range.
      Above range → mild pullback signal. Below → room to grow.
    """
    strategy = MARKET_STRATEGY.get(market, {})
    stype = strategy.get('type', 'balanced')
    
    # AU: no ie%CCP constraint
    if stype == 'efficiency' or ieccp_current is None:
        return nb_forecast
    
    # JP: NB too small to adjust
    if stype == 'brand_dominant':
        return nb_forecast
    
    ieccp_range = strategy.get('ieccp_range')
    ieccp_target = strategy.get('ieccp_target')
    
    if stype == 'ieccp_bound' and ieccp_target:
        # MX: ie%CCP = 100% is the constraint
        deviation = ieccp_current - ieccp_target
        if abs(deviation) < 0.05:
            return nb_forecast  # Within 5% of target, no adjustment
        # Overshoot: CPA > CCP, expect spend pullback
        # 10% overshoot → ~8% spend reduction (MX is more aggressive on ie%CCP)
        spend_adj = 1.0 - (deviation * 0.8)
        spend_adj = max(0.6, min(1.4, spend_adj))
    
    elif stype == 'balanced' and ieccp_range:
        # Normal markets: 50-65% range
        low, high = ieccp_range
        mid = (low + high) / 2
        if low <= ieccp_current <= high:
            return nb_forecast  # Within normal range, no adjustment
        if ieccp_current > high:
            # Above range — mild pullback signal
            overshoot = ieccp_current - high
            spend_adj = 1.0 - (overshoot * 0.3)
            spend_adj = max(0.8, spend_adj)
        else:
            # Below range — room to push spend
            undershoot = low - ieccp_current
            spend_adj = 1.0 + (undershoot * 0.2)
            spend_adj = min(1.15, spend_adj)
    else:
        return nb_forecast
    
    # If ie%CCP is trending up (slope > 0), amplify pullback
    if ieccp_trend_slope and ieccp_trend_slope > 0.02 and spend_adj < 1.0:
        spend_adj *= 0.95
    
    # Apply to NB cost and derive downstream
    adj_cost = nb_forecast.cost * spend_adj
    adj_clicks = nb_forecast.clicks * spend_adj
    adj_regs = adj_clicks * nb_forecast.cvr if nb_forecast.cvr > 0 else nb_forecast.registrations * spend_adj
    adj_cpa = adj_cost / adj_regs if adj_regs > 0 else nb_forecast.cpa
    adj_cpc = adj_cost / adj_clicks if adj_clicks > 0 else nb_forecast.cpc
    
    return SegmentForecast(
        registrations=round(adj_regs),
        cost=round(adj_cost, 2),
        cpa=round(adj_cpa, 2),
        clicks=round(adj_clicks),
        cvr=nb_forecast.cvr,
        cpc=round(adj_cpc, 2),
        ci_regs_low=round(nb_forecast.ci_regs_low * spend_adj),
        ci_regs_high=round(nb_forecast.ci_regs_high * spend_adj),
        ci_cost_low=round(nb_forecast.ci_cost_low * spend_adj, 2),
        ci_cost_high=round(nb_forecast.ci_cost_high * spend_adj, 2),
    )



def ieccp_trend(history, n=6):
    """Compute ie%CCP trend slope from last n weeks."""
    vals = [w.get('ieccp') for w in history[:n] if w.get('ieccp') is not None]
    if len(vals) < 3:
        return None
    vals.reverse()  # oldest first
    slope, _ = ols_trend(vals)
    return slope


def project_market_weekly(con, market, target_week_num, target_period_key):
    """Generate next-week projection for a market.
    
    Returns MarketProjection or None if insufficient data.
    """
    history = fetch_weekly_history(con, market)
    if len(history) < 4:
        return None
    
    strategy = MARKET_STRATEGY.get(market, {})
    stype = strategy.get('type', 'balanced')
    
    # ── Brand projection ──
    brand = project_segment(history, 'brand', target_week_num, weeks_ahead=1)
    
    # ── NB projection ──
    if stype == 'brand_dominant':
        # JP: NB is negligible, just use recent average
        recent_nb = [w.get('nb_regs', 0) or 0 for w in history[:4]]
        nb_avg = sum(recent_nb) / len(recent_nb) if recent_nb else 0
        nb = SegmentForecast(round(nb_avg), 0, 0, 0, 0, 0, 0, round(nb_avg * 1.5), 0, 0)
    else:
        nb = project_segment(history, 'nb', target_week_num, weeks_ahead=1)
    
    # ── ie%CCP constraint on NB ──
    ieccp_current = history[0].get('ieccp') if history else None
    ieccp_slope = ieccp_trend(history)
    nb = apply_ieccp_constraint(nb, market, ieccp_current, ieccp_slope)
    
    # ── Total = Brand + NB ──
    total_regs = brand.registrations + nb.registrations
    total_cost = brand.cost + nb.cost
    total_cpa = total_cost / total_regs if total_regs > 0 else 0
    
    ci_regs_low = brand.ci_regs_low + nb.ci_regs_low
    ci_regs_high = brand.ci_regs_high + nb.ci_regs_high
    ci_cost_low = brand.ci_cost_low + nb.ci_cost_low
    ci_cost_high = brand.ci_cost_high + nb.ci_cost_high
    
    # ── ie%CCP projection ──
    ieccp_projected = None
    if ieccp_current is not None and ieccp_slope is not None:
        ieccp_projected = round(ieccp_current + ieccp_slope, 3)
    
    # ── OP2 ──
    op2_spend = fetch_op2_spend(con, market, f'2026-M{datetime.now().strftime("%m")}')
    # Weekly OP2 ≈ monthly / 4.33
    weekly_op2 = op2_spend / 4.33 if op2_spend else None
    vs_op2 = round((total_cost / weekly_op2 - 1) * 100, 1) if weekly_op2 else None
    
    # ── Notes ──
    notes_parts = [f"Strategy: {stype}"]
    if ieccp_current:
        notes_parts.append(f"ie%CCP: {ieccp_current:.0%}")
    if stype == 'brand_dominant':
        notes_parts.append(f"Brand={brand.registrations}/{total_regs} regs")
    
    return MarketProjection(
        market=market,
        horizon=target_period_key,
        horizon_label='Next Week',
        brand=brand, nb=nb,
        total_regs=total_regs, total_cost=round(total_cost, 2),
        total_cpa=round(total_cpa, 2),
        ci_regs_low=ci_regs_low, ci_regs_high=ci_regs_high,
        ci_cost_low=round(ci_cost_low, 2), ci_cost_high=round(ci_cost_high, 2),
        ieccp_current=ieccp_current, ieccp_projected=ieccp_projected,
        op2_spend=weekly_op2, vs_op2_spend_pct=vs_op2,
        method='bayesian_brand_nb_split',
        notes='; '.join(notes_parts),
    )


def project_market_monthly(con, market, target_month_key, weeks_in_month=4.33):
    """Generate current-month projection by scaling weekly forecast."""
    # Get the current week number for seasonality
    now = datetime.now()
    target_wk = now.isocalendar()[1]
    
    history = fetch_weekly_history(con, market)
    if len(history) < 4:
        return None
    
    strategy = MARKET_STRATEGY.get(market, {})
    stype = strategy.get('type', 'balanced')
    
    # Project each week of the month and sum
    brand_total = SegmentForecast(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    nb_total = SegmentForecast(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    
    # Approximate: project 4 weeks forward, accumulate
    for wk_offset in range(1, 5):
        wk_num = (target_wk + wk_offset - 1) % 52 + 1
        brand_wk = project_segment(history, 'brand', wk_num, weeks_ahead=wk_offset)
        
        if stype == 'brand_dominant':
            recent_nb = [w.get('nb_regs', 0) or 0 for w in history[:4]]
            nb_avg = sum(recent_nb) / len(recent_nb) if recent_nb else 0
            nb_wk = SegmentForecast(round(nb_avg), 0, 0, 0, 0, 0, 0, round(nb_avg*1.5), 0, 0)
        else:
            nb_wk = project_segment(history, 'nb', wk_num, weeks_ahead=wk_offset)
        
        # ie%CCP constraint
        ieccp_current = history[0].get('ieccp')
        ieccp_slope = ieccp_trend(history)
        nb_wk = apply_ieccp_constraint(nb_wk, market, ieccp_current, ieccp_slope)
        
        # Accumulate
        brand_total = SegmentForecast(
            brand_total.registrations + brand_wk.registrations,
            brand_total.cost + brand_wk.cost, 0, 
            brand_total.clicks + brand_wk.clicks, 0, 0,
            brand_total.ci_regs_low + brand_wk.ci_regs_low,
            brand_total.ci_regs_high + brand_wk.ci_regs_high,
            brand_total.ci_cost_low + brand_wk.ci_cost_low,
            brand_total.ci_cost_high + brand_wk.ci_cost_high,
        )
        nb_total = SegmentForecast(
            nb_total.registrations + nb_wk.registrations,
            nb_total.cost + nb_wk.cost, 0,
            nb_total.clicks + nb_wk.clicks, 0, 0,
            nb_total.ci_regs_low + nb_wk.ci_regs_low,
            nb_total.ci_regs_high + nb_wk.ci_regs_high,
            nb_total.ci_cost_low + nb_wk.ci_cost_low,
            nb_total.ci_cost_high + nb_wk.ci_cost_high,
        )
    
    # Compute derived metrics for totals
    brand_total = SegmentForecast(
        brand_total.registrations, brand_total.cost,
        round(brand_total.cost / brand_total.registrations, 2) if brand_total.registrations > 0 else 0,
        brand_total.clicks,
        round(brand_total.registrations / brand_total.clicks, 4) if brand_total.clicks > 0 else 0,
        round(brand_total.cost / brand_total.clicks, 2) if brand_total.clicks > 0 else 0,
        brand_total.ci_regs_low, brand_total.ci_regs_high,
        brand_total.ci_cost_low, brand_total.ci_cost_high,
    )
    nb_total = SegmentForecast(
        nb_total.registrations, nb_total.cost,
        round(nb_total.cost / nb_total.registrations, 2) if nb_total.registrations > 0 else 0,
        nb_total.clicks,
        round(nb_total.registrations / nb_total.clicks, 4) if nb_total.clicks > 0 else 0,
        round(nb_total.cost / nb_total.clicks, 2) if nb_total.clicks > 0 else 0,
        nb_total.ci_regs_low, nb_total.ci_regs_high,
        nb_total.ci_cost_low, nb_total.ci_cost_high,
    )
    
    total_regs = brand_total.registrations + nb_total.registrations
    total_cost = brand_total.cost + nb_total.cost
    
    op2_spend = fetch_op2_spend(con, market, target_month_key)
    vs_op2 = round((total_cost / op2_spend - 1) * 100, 1) if op2_spend else None
    
    return MarketProjection(
        market=market, horizon=target_month_key,
        horizon_label=f'{target_month_key}',
        brand=brand_total, nb=nb_total,
        total_regs=total_regs, total_cost=round(total_cost, 2),
        total_cpa=round(total_cost / total_regs, 2) if total_regs > 0 else 0,
        ci_regs_low=brand_total.ci_regs_low + nb_total.ci_regs_low,
        ci_regs_high=brand_total.ci_regs_high + nb_total.ci_regs_high,
        ci_cost_low=round(brand_total.ci_cost_low + nb_total.ci_cost_low, 2),
        ci_cost_high=round(brand_total.ci_cost_high + nb_total.ci_cost_high, 2),
        ieccp_current=history[0].get('ieccp') if history else None,
        ieccp_projected=None,
        op2_spend=op2_spend, vs_op2_spend_pct=vs_op2,
        method='bayesian_brand_nb_split',
        notes=f"Strategy: {MARKET_STRATEGY.get(market, {}).get('type', 'balanced')}; 4-week accumulation",
    )


def project_market_quarterly(con, market, target_quarter_key, weeks_in_quarter=13):
    """Generate quarterly projection by scaling weekly forecast over 13 weeks."""
    now = datetime.now()
    target_wk = now.isocalendar()[1]
    
    history = fetch_weekly_history(con, market)
    if len(history) < 4:
        return None
    
    strategy = MARKET_STRATEGY.get(market, {})
    stype = strategy.get('type', 'balanced')
    
    total_brand_regs = 0
    total_brand_cost = 0
    total_nb_regs = 0
    total_nb_cost = 0
    total_brand_clicks = 0
    total_nb_clicks = 0
    ci_brand_low = 0
    ci_brand_high = 0
    ci_nb_low = 0
    ci_nb_high = 0
    ci_brand_cost_low = 0
    ci_brand_cost_high = 0
    ci_nb_cost_low = 0
    ci_nb_cost_high = 0
    
    for wk_offset in range(1, weeks_in_quarter + 1):
        wk_num = (target_wk + wk_offset - 1) % 52 + 1
        brand_wk = project_segment(history, 'brand', wk_num, weeks_ahead=wk_offset)
        
        if stype == 'brand_dominant':
            recent_nb = [w.get('nb_regs', 0) or 0 for w in history[:4]]
            nb_avg = sum(recent_nb) / len(recent_nb) if recent_nb else 0
            nb_wk = SegmentForecast(round(nb_avg), 0, 0, 0, 0, 0, 0, round(nb_avg*1.5), 0, 0)
        else:
            nb_wk = project_segment(history, 'nb', wk_num, weeks_ahead=wk_offset)
        
        ieccp_current = history[0].get('ieccp')
        ieccp_slope = ieccp_trend(history)
        nb_wk = apply_ieccp_constraint(nb_wk, market, ieccp_current, ieccp_slope)
        
        total_brand_regs += brand_wk.registrations
        total_brand_cost += brand_wk.cost
        total_brand_clicks += brand_wk.clicks
        total_nb_regs += nb_wk.registrations
        total_nb_cost += nb_wk.cost
        total_nb_clicks += nb_wk.clicks
        ci_brand_low += brand_wk.ci_regs_low
        ci_brand_high += brand_wk.ci_regs_high
        ci_nb_low += nb_wk.ci_regs_low
        ci_nb_high += nb_wk.ci_regs_high
        ci_brand_cost_low += brand_wk.ci_cost_low
        ci_brand_cost_high += brand_wk.ci_cost_high
        ci_nb_cost_low += nb_wk.ci_cost_low
        ci_nb_cost_high += nb_wk.ci_cost_high
    
    brand = SegmentForecast(
        total_brand_regs, round(total_brand_cost, 2),
        round(total_brand_cost / total_brand_regs, 2) if total_brand_regs > 0 else 0,
        total_brand_clicks,
        round(total_brand_regs / total_brand_clicks, 4) if total_brand_clicks > 0 else 0,
        round(total_brand_cost / total_brand_clicks, 2) if total_brand_clicks > 0 else 0,
        ci_brand_low, ci_brand_high, round(ci_brand_cost_low, 2), round(ci_brand_cost_high, 2),
    )
    nb = SegmentForecast(
        total_nb_regs, round(total_nb_cost, 2),
        round(total_nb_cost / total_nb_regs, 2) if total_nb_regs > 0 else 0,
        total_nb_clicks,
        round(total_nb_regs / total_nb_clicks, 4) if total_nb_clicks > 0 else 0,
        round(total_nb_cost / total_nb_clicks, 2) if total_nb_clicks > 0 else 0,
        ci_nb_low, ci_nb_high, round(ci_nb_cost_low, 2), round(ci_nb_cost_high, 2),
    )
    
    total_regs = total_brand_regs + total_nb_regs
    total_cost = total_brand_cost + total_nb_cost
    
    # Quarterly OP2 = sum of monthly OP2s in the quarter
    q_map = {'Q1': ['01','02','03'], 'Q2': ['04','05','06'], 'Q3': ['07','08','09'], 'Q4': ['10','11','12']}
    q_label = target_quarter_key.split('-')[-1]
    q_months = q_map.get(q_label, [])
    op2_total = 0
    for m in q_months:
        v = fetch_op2_spend(con, market, f'2026-M{m}')
        if v: op2_total += v
    op2_spend = op2_total if op2_total > 0 else None
    vs_op2 = round((total_cost / op2_spend - 1) * 100, 1) if op2_spend else None
    
    return MarketProjection(
        market=market, horizon=target_quarter_key,
        horizon_label=f'{q_label} 2026',
        brand=brand, nb=nb,
        total_regs=total_regs, total_cost=round(total_cost, 2),
        total_cpa=round(total_cost / total_regs, 2) if total_regs > 0 else 0,
        ci_regs_low=ci_brand_low + ci_nb_low,
        ci_regs_high=ci_brand_high + ci_nb_high,
        ci_cost_low=round(ci_brand_cost_low + ci_nb_cost_low, 2),
        ci_cost_high=round(ci_brand_cost_high + ci_nb_cost_high, 2),
        ieccp_current=history[0].get('ieccp') if history else None,
        ieccp_projected=None,
        op2_spend=op2_spend, vs_op2_spend_pct=vs_op2,
        method='bayesian_brand_nb_split',
        notes=f"Strategy: {stype}; {weeks_in_quarter}-week accumulation",
    )


def write_projections_to_db(con, projections):
    """Write projections to ps.forecasts with revision tracking."""
    forecast_date = datetime.now().strftime('%Y-%m-%d')
    written = 0
    
    for proj in projections:
        if proj is None:
            continue
        
        # Write total, brand, and nb as separate forecast rows
        for segment, label, regs, cost, cpa, ci_lo, ci_hi in [
            ('total', '', proj.total_regs, proj.total_cost, proj.total_cpa,
             proj.ci_regs_low, proj.ci_regs_high),
            ('brand', 'brand_', proj.brand.registrations, proj.brand.cost, proj.brand.cpa,
             proj.brand.ci_regs_low, proj.brand.ci_regs_high),
            ('nb', 'nb_', proj.nb.registrations, proj.nb.cost, proj.nb.cpa,
             proj.nb.ci_regs_low, proj.nb.ci_regs_high),
        ]:
            for metric, value, ci_l, ci_h in [
                (f'{label}registrations', regs, ci_lo, ci_hi),
                (f'{label}cost', cost, proj.ci_cost_low if segment == 'total' else None, 
                 proj.ci_cost_high if segment == 'total' else None),
                (f'{label}cpa', cpa, None, None),
            ]:
                if value is None or value == 0:
                    continue
                
                # Check for existing forecast to compute revision number
                existing = con.execute(f"""
                    SELECT MAX(revision_number) FROM ps.forecast_revisions
                    WHERE market = '{proj.market}' AND metric_name = '{metric}'
                    AND target_period = '{proj.horizon}' AND period_type = 'weekly'
                """).fetchone()
                rev_num = (existing[0] or 0) + 1 if existing and existing[0] else 1
                
                # Get prior value for drift tracking
                prior = con.execute(f"""
                    SELECT predicted_value FROM ps.forecasts
                    WHERE market = '{proj.market}' AND metric_name = '{metric}'
                    AND target_period = '{proj.horizon}'
                """).fetchone()
                prior_val = prior[0] if prior else None
                drift_abs = value - prior_val if prior_val else None
                drift_pct = round((drift_abs / prior_val) * 100, 1) if prior_val and prior_val != 0 else None
                drift_dir = 'up' if drift_abs and drift_abs > 0 else ('down' if drift_abs and drift_abs < 0 else None)
                
                # Upsert forecast
                try:
                    con.execute("DELETE FROM ps.forecasts WHERE market = ? AND metric_name = ? AND target_period = ?",
                               [proj.market, metric, proj.horizon])
                    con.execute("""INSERT INTO ps.forecasts 
                        (market, channel, metric_name, forecast_date, target_period, period_type,
                         predicted_value, confidence_low, confidence_high, method, notes)
                        VALUES (?, 'ps', ?, ?, ?, 'weekly', ?, ?, ?, ?, ?)""",
                        [proj.market, metric, forecast_date, proj.horizon,
                         value, ci_l, ci_h, proj.method, proj.notes])
                    written += 1
                except Exception as e:
                    print(f"  WARN: forecast write failed {proj.market}/{metric}/{proj.horizon}: {e}")
                
                # Write revision
                try:
                    rev_id = f"{proj.market}-{metric}-{proj.horizon}-r{rev_num}"
                    con.execute("""INSERT OR IGNORE INTO ps.forecast_revisions
                        (revision_id, market, channel, metric_name, target_period, period_type,
                         revision_number, forecast_date, predicted_value, confidence_low, confidence_high,
                         prior_predicted_value, drift_abs, drift_pct, drift_direction, reason)
                        VALUES (?, ?, 'ps', ?, ?, 'weekly', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        [rev_id, proj.market, metric, proj.horizon,
                         rev_num, forecast_date, value, ci_l, ci_h,
                         prior_val, drift_abs, drift_pct, drift_dir,
                         f"WBR W14 projection; {proj.method}"])
                except Exception as e:
                    pass  # Revision tracking is best-effort
    
    return written


def format_projection_table(projections, horizon_label):
    """Format projections as a markdown table for the callout doc."""
    lines = [f"\n### Projections — {horizon_label}\n"]
    lines.append("| Market | Regs (Brand/NB) | Spend | CPA | ie%CCP | vs OP2 Spend |")
    lines.append("|--------|----------------|-------|-----|--------|-------------|")
    
    for proj in projections:
        if proj is None:
            continue
        regs = f"{proj.total_regs:,} ({proj.brand.registrations:,}/{proj.nb.registrations:,})"
        spend = f"${proj.total_cost:,.0f}"
        cpa = f"${proj.total_cpa:,.0f}"
        ieccp = f"{proj.ieccp_current:.0%}" if proj.ieccp_current else "N/A"
        vs_op2 = f"{proj.vs_op2_spend_pct:+.1f}%" if proj.vs_op2_spend_pct is not None else "N/A"
        ci = f"[{proj.ci_regs_low:,}–{proj.ci_regs_high:,}]"
        lines.append(f"| {proj.market} | {regs} {ci} | {spend} | {cpa} | {ieccp} | {vs_op2} |")
    
    return '\n'.join(lines)


def run(current_week='2026-W14'):
    """Main entry point. Generate all projections and write to MotherDuck."""
    con = connect_md()
    
    # Parse current week to determine targets
    year, wk = current_week.split('-W')
    next_wk_num = int(wk) + 1
    next_wk_key = f"{year}-W{next_wk_num}"
    
    # Current month and quarter
    now = datetime.now()
    month_key = f"2026-M{now.strftime('%m')}"
    quarter_num = (now.month - 1) // 3 + 1
    quarter_key = f"2026-Q{quarter_num}"
    
    print(f"Projecting from {current_week}")
    print(f"  Next week: {next_wk_key} (W{next_wk_num})")
    print(f"  Month: {month_key}")
    print(f"  Quarter: {quarter_key}")
    print()
    
    weekly_projections = []
    monthly_projections = []
    quarterly_projections = []
    
    for market in ALL_MARKETS:
        strategy = MARKET_STRATEGY.get(market, {})
        print(f"{market} ({strategy.get('type', 'balanced')})...")
        
        # Weekly
        wp = project_market_weekly(con, market, next_wk_num, next_wk_key)
        weekly_projections.append(wp)
        if wp:
            print(f"  W{next_wk_num}: {wp.total_regs} regs ({wp.brand.registrations}B/{wp.nb.registrations}NB), ${wp.total_cost:,.0f}, ${wp.total_cpa:.0f} CPA")
        
        # Monthly
        mp = project_market_monthly(con, market, month_key)
        monthly_projections.append(mp)
        if mp:
            print(f"  {month_key}: {mp.total_regs} regs, ${mp.total_cost:,.0f}")
        
        # Quarterly
        qp = project_market_quarterly(con, market, quarter_key)
        quarterly_projections.append(qp)
        if qp:
            vs = f" ({qp.vs_op2_spend_pct:+.1f}% vs OP2)" if qp.vs_op2_spend_pct is not None else ""
            print(f"  {quarter_key}: {qp.total_regs} regs, ${qp.total_cost:,.0f}{vs}")
    
    # Write to MotherDuck
    print("\nWriting to MotherDuck...")
    all_projections = [p for p in weekly_projections + monthly_projections + quarterly_projections if p]
    written = write_projections_to_db(con, all_projections)
    print(f"  Wrote {written} forecast rows")
    
    # Format tables for callout doc
    weekly_table = format_projection_table(
        [p for p in weekly_projections if p], f"Next Week ({next_wk_key})")
    monthly_table = format_projection_table(
        [p for p in monthly_projections if p], f"Current Month ({month_key})")
    quarterly_table = format_projection_table(
        [p for p in quarterly_projections if p], f"Current Quarter ({quarter_key})")
    
    projection_section = f"""
---

## Projections (not part of callout word count)

{weekly_table}

{monthly_table}

{quarterly_table}

*Method: Bayesian Brand/NB split with YoY seasonality and ie%CCP constraints. CIs are 70% credible intervals.*
*Market strategies: AU=efficiency (hit OP2), MX=ie%CCP bound (100% target), JP=brand-dominant, others=balanced (50-65% ie%CCP).*
"""
    
    # Write projection section to file
    wk_label = current_week.lower().replace('2026-', '')
    proj_path = f'shared/context/active/callouts/projections-{wk_label}.md'
    with open(os.path.expanduser(f'~/{proj_path}'), 'w') as f:
        f.write(projection_section)
    print(f"\nProjection section written to ~/{proj_path}")
    
    con.close()
    return projection_section


def score_predictions(current_week):
    """Score last week's predictions against this week's actuals.
    
    Reads ps.forecasts for predictions targeting current_week,
    compares against ps.performance actuals, updates scored/error_pct/score.
    """
    con = connect_md()
    
    scored_count = 0
    for market in ALL_MARKETS:
        # Get actuals from ps.performance
        actuals = con.execute(f"""
            SELECT registrations, brand_registrations, nb_registrations, cost, cpa
            FROM ps.performance
            WHERE market = '{market}' AND period_type = 'weekly' AND period_key = '{current_week}'
        """).fetchone()
        
        if not actuals:
            continue
        
        actual_map = {
            'registrations': actuals[0],
            'brand_registrations': actuals[1],
            'nb_registrations': actuals[2],
            'cost': actuals[3],
            'cpa': actuals[4],
        }
        
        # Score each forecast for this market+week
        forecasts = con.execute(f"""
            SELECT forecast_id, metric_name, predicted_value, confidence_low, confidence_high
            FROM ps.forecasts
            WHERE market = '{market}' AND target_period = '{current_week}'
            AND (scored IS NULL OR scored = false)
        """).fetchall()
        
        for fid, metric, predicted, ci_low, ci_high in forecasts:
            actual = actual_map.get(metric)
            if actual is None or actual == 0:
                continue
            
            error = abs(predicted - actual) / actual * 100
            within_ci = (ci_low is not None and ci_high is not None 
                        and ci_low <= actual <= ci_high)
            
            if within_ci:
                score = 'HIT'
            elif error > 20:
                score = 'SURPRISE'
            else:
                score = 'MISS'
            
            try:
                con.execute("""UPDATE ps.forecasts SET 
                    actual_value = ?, error_pct = ?, scored = true, score = ?
                    WHERE market = ? AND metric_name = ? AND target_period = ?""",
                    [actual, round(error, 1), score, market, metric, current_week])
                scored_count += 1
            except Exception as e:
                print(f"  WARN: scoring failed {market}/{metric}: {e}")
    
    print(f"Scored {scored_count} predictions for {current_week}")
    con.close()
    return scored_count


def sync_to_motherduck(json_path):
    """Load ingester JSON output into ps.performance in MotherDuck.
    
    Call this after running the ingester to push data to MotherDuck.
    Handles weekly data from the JSON extract.
    """
    import json as json_mod
    con = connect_md()
    
    with open(json_path) as f:
        data = json_mod.load(f)
    
    def week_to_dates(week_str):
        parts = week_str.split()
        year = int(parts[0])
        week_num = int(parts[1].replace('W', ''))
        jan4 = datetime(year, 1, 4)
        start_of_w1 = jan4 - timedelta(days=jan4.weekday())
        monday = start_of_w1 + timedelta(weeks=week_num - 1)
        sunday = monday + timedelta(days=6)
        return monday.strftime('%Y-%m-%d'), sunday.strftime('%Y-%m-%d')
    
    def s(v):
        if v is None: return None
        try: return float(v)
        except: return None
    def si(v):
        if v is None: return None
        try: return int(v)
        except: return None
    
    INSERT_SQL = """INSERT OR REPLACE INTO ps.performance 
        (market, period_type, period_key, period_start, period_end,
         registrations, cost, cpa, clicks, impressions, cpc, cvr, ctr,
         brand_registrations, brand_cost, brand_cpa, brand_clicks, brand_cpc, brand_cvr,
         nb_registrations, nb_cost, nb_cpa, nb_clicks, nb_cpc, nb_cvr,
         ieccp, source)
        VALUES (?,?,?,?,?, ?,?,?,?,?,?,?,?, ?,?,?,?,?,?, ?,?,?,?,?,?, ?,?)"""
    
    total = 0
    for market, mdata in data.items():
        wh = mdata.get('weekly_history', [])
        rows = []
        for w in wh:
            pk = w['week'].replace(' ', '-')
            try:
                ps, pe = week_to_dates(w['week'])
            except:
                continue
            rows.append((
                market, 'weekly', pk, ps, pe,
                si(w.get('regs')), s(w.get('spend')), s(w.get('cpa')),
                si(w.get('clicks')), si(w.get('impressions')),
                s(w.get('cpc')), s(w.get('cvr')), s(w.get('ctr')),
                si(w.get('brand_regs')), s(w.get('brand_spend')), s(w.get('brand_cpa')),
                si(w.get('brand_clicks')), s(w.get('brand_cpc')), s(w.get('brand_cvr')),
                si(w.get('nb_regs')), s(w.get('nb_spend')), s(w.get('nb_cpa')),
                si(w.get('nb_clicks')), s(w.get('nb_cpc')), s(w.get('nb_cvr')),
                None, 'ww_dashboard'
            ))
        for i in range(0, len(rows), 100):
            con.executemany(INSERT_SQL, rows[i:i+100])
        total += len(rows)
        print(f"  {market}: {len(rows)} weekly rows synced")
    
    print(f"Total: {total} rows synced to ps.performance")
    con.close()
    return total


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='WBR Projection Engine')
    parser.add_argument('--week', default='2026-W14', help='Current week (e.g. 2026-W14)')
    parser.add_argument('--score', help='Score predictions for this week (e.g. 2026-W14)')
    parser.add_argument('--sync', help='Path to ingester JSON to sync to MotherDuck')
    args = parser.parse_args()
    
    if args.sync:
        sync_to_motherduck(args.sync)
    if args.score:
        score_predictions(args.score)
    run(args.week)
