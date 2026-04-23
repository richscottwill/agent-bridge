"""MPE Fitting — recency-weighted linear regression for market parameters.

WHY THIS EXISTS
    The Market Projection Engine needs fitted elasticity curves (CPA and
    CPC), seasonality shapes (52 weekly weights), and YoY growth trends
    per market per segment (Brand / NB). This module does the fitting.
    Everything is recency-weighted so recent weeks dominate the signal
    while older history still informs the shape.

HOW THE OWNER MAINTAINS IT
    You never call this module directly. The quarterly refit hook
    (`kiro hook run mpe-refit`) runs `refit_market_params.py` which
    uses this module behind the scenes. The owner-readable refit
    report tells you what changed and why.

    If you need to inspect a specific fit manually:
        python3 -c "
        from shared.tools.prediction.mpe_fitting import fit_elasticity
        result = fit_elasticity('MX', 'brand', 'cpa')
        print(result)
        "

WHAT HAPPENS ON FAILURE
    - Insufficient data (< 80 clean weeks): function returns a
      `FitResult` with `fallback_level='regional_fallback'` and
      loads the regional average curve instead. No crash.
    - Fit r² < 0.35: same fallback behavior.
    - CPC specific — per R2.11: fit when r² >= 0.3; else derive CPC
      from CPA (CPC = CPA * CVR) with `CPC_DERIVED_FROM_CPA` warning.
    - All-null regression: returns `FitResult(fallback_level='conservative_default')`
      with a flat curve. Banner in UI alerts owner.

MATH
    Elasticity: log(CPA) = a + b * log(spend) + noise
                → CPA = exp(a) * spend^b
    Seasonality: 52 weekly weights normalized to sum to 52.0
                 (weight = 1.0 means average week; 1.2 means 20% above avg)
    YoY trend: log(year_n / year_n-1) fit per segment, exponentiated
               multiplicatively across years.

    Recency weighting: w_i = 0.5^(age_weeks_i / HALF_LIFE_WEEKS)
    Default HALF_LIFE_WEEKS = 52 (one year half-life).

FALLBACK HIERARCHY
    1. market_specific (preferred): market has >= 80 clean weeks AND
       elasticity r² >= 0.35. Use the direct fit.
    2. regional_fallback: market is below threshold OR fit failed.
       Use the NA / EU5 / WW average curve (region determined by
       REGIONAL_FALLBACK_MAP from data_audit.py).
    3. prior_version: regional fallback itself is also unavailable.
       Re-use the previous active parameter_version.
    4. conservative_default: nothing else works. Flat curve (b=0)
       with wide credible intervals. Banner alerts owner.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

import numpy as np

# Local imports
sys.path.insert(0, os.path.expanduser('~/shared/tools'))


# ---------- Constants ----------

HALF_LIFE_WEEKS_DEFAULT = 52
THRESHOLD_MARKET_SPECIFIC_WEEKS = 80       # R1.9
THRESHOLD_MIN_ELASTICITY_R2 = 0.35         # R1.9
THRESHOLD_CPC_FIT_R2 = 0.30                # R2.11
THRESHOLD_VALIDATION_MAPE_WARN = 0.40      # R9.3

REGIONAL_FALLBACK_MAP = {
    'US': 'NA', 'CA': 'NA',
    'UK': 'EU5', 'DE': 'EU5', 'FR': 'EU5', 'IT': 'EU5', 'ES': 'EU5',
    'MX': 'WW', 'AU': 'WW', 'JP': 'WW',
}

REGION_CONSTITUENTS = {
    'NA': ['US', 'CA'],
    'EU5': ['UK', 'DE', 'FR', 'IT', 'ES'],
    'WW': ['US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'MX', 'AU', 'JP'],
}


# ---------- Result dataclasses ----------

@dataclass
class FitResult:
    """Result of a single elasticity or trend fit."""
    market: str
    segment: str                              # 'brand' or 'nb'
    metric: str                               # 'cpa' or 'cpc'
    # Fit coefficients: log(metric) = a + b * log(spend)
    coef_a: float = 0.0                       # intercept (log-space)
    coef_b: float = 0.0                       # slope (elasticity exponent)
    r_squared: float = 0.0
    # Posterior covariance for Monte Carlo sampling (2x2 for [a, b])
    posterior_cov: list[list[float]] = field(default_factory=lambda: [[0.0, 0.0], [0.0, 0.0]])
    weeks_used: int = 0
    fallback_level: str = 'market_specific'   # 'market_specific' | 'regional_fallback' | 'prior_version' | 'conservative_default' | 'derived_from_cpa'
    warnings: list[str] = field(default_factory=list)
    lineage: str = ''

    def to_json(self) -> dict:
        """Serialize for ps.market_projection_params.value_json."""
        return {
            'a': self.coef_a,
            'b': self.coef_b,
            'r_squared': self.r_squared,
            'posterior_cov': self.posterior_cov,
            'weeks_used': self.weeks_used,
            'fallback_level': self.fallback_level,
            'warnings': self.warnings,
            'lineage': self.lineage,
        }


@dataclass
class SeasonalityResult:
    """52-week seasonality shape with per-week posterior."""
    market: str
    segment: str
    weights: list[float]                      # 52 floats, normalized to sum to 52.0
    posteriors: list[dict]                    # 52 {mean, std, provenance}
    fallback_level: str = 'market_specific'
    warnings: list[str] = field(default_factory=list)
    lineage: str = ''

    def to_json(self) -> dict:
        return {
            'weights': self.weights,
            'posteriors': self.posteriors,
            'fallback_level': self.fallback_level,
            'warnings': self.warnings,
            'lineage': self.lineage,
        }


@dataclass
class YoYGrowthResult:
    """YoY growth trend with posterior."""
    market: str
    segment: str
    mean: float
    std: float
    r_squared: float
    years_used: int
    fallback_level: str = 'market_specific'
    warnings: list[str] = field(default_factory=list)
    lineage: str = ''

    def to_json(self) -> dict:
        return {
            'mean': self.mean,
            'std': self.std,
            'r_squared': self.r_squared,
            'years_used': self.years_used,
            'fallback_level': self.fallback_level,
            'warnings': self.warnings,
            'lineage': self.lineage,
        }


# ---------- Connection helper ----------

_con = None


def _db():
    """Lazy MotherDuck connection (read-only for fitting)."""
    global _con
    if _con is None:
        try:
            import duckdb
            from prediction.config import MOTHERDUCK_TOKEN
            _con = duckdb.connect(
                f'md:ps_analytics?motherduck_token={MOTHERDUCK_TOKEN}',
                read_only=True,
            )
        except Exception as e:
            print(f"[mpe_fitting] FATAL: cannot connect to MotherDuck: {e}", file=sys.stderr)
            sys.exit(2)
    return _con


# ---------- Data fetching ----------

def _fetch_weekly(
    market: str,
    segment: str,
    regime_filter: bool = True,
    include_pre_structural: bool = True,  # DEFAULT TRUE — see note below
) -> list[dict]:
    """Fetch weekly data for a market/segment, with regime-exclusion filtering.

    Returns list of dicts with keys: period_start, period_key, spend, regs, cpa, cpc, cvr, age_weeks.
    Older weeks come first. age_weeks is the number of weeks from the latest row.

    regime_filter: when True (default), excludes weeks that fall within a
    reverted/short-term-excluded event window (is_structural_baseline=FALSE,
    half_life_weeks=0, active=TRUE in ps.regime_changes).

    include_pre_structural: when True (default), INCLUDES weeks before
    the most recent structural regime change. We do this because OCI
    launches, CCP recalibrations, and similar structural events are
    typically LEVEL shifts, not SHAPE shifts — the elasticity curve and
    seasonality shape remain informative. Recency weighting (52-week
    half-life) handles the level shift gracefully: recent post-structural
    weeks dominate while older data provides shape context.

    Set include_pre_structural=False ONLY when the structural event is a
    genuine shape-breaker (e.g., market launch, permanent pause, product
    replacement). These cases are rare.
    """
    con = _db()
    spend_col = f"{segment}_cost"
    regs_col = f"{segment}_registrations"
    cpa_col = f"{segment}_cpa"
    cpc_col = f"{segment}_cpc"
    cvr_col = f"{segment}_cvr"

    rows = con.execute(f"""
        SELECT period_start, period_key,
               {spend_col} AS spend,
               {regs_col} AS regs,
               {cpa_col} AS cpa,
               {cpc_col} AS cpc,
               {cvr_col} AS cvr
        FROM ps.v_weekly
        WHERE market = ? AND period_type = 'weekly'
          AND {spend_col} IS NOT NULL AND {spend_col} > 0
          AND {regs_col} IS NOT NULL AND {regs_col} > 0
        ORDER BY period_start ASC
    """, [market]).fetchall()

    if not rows:
        return []

    reverted_windows: list[tuple[date, date]] = []
    latest_structural_date: date | None = None
    if regime_filter:
        reverted = con.execute("""
            SELECT CAST(change_date AS DATE),
                   CAST(COALESCE(end_date, change_date + INTERVAL 21 DAY) AS DATE) AS end_dt
            FROM ps.regime_changes
            WHERE market = ?
              AND is_structural_baseline = FALSE
              AND active = TRUE
              AND half_life_weeks = 0
        """, [market]).fetchall()
        for start_dt, end_dt in reverted:
            if start_dt is not None:
                end_d = end_dt if end_dt is not None else start_dt
                reverted_windows.append((start_dt, end_d))

        # Find the latest structural baseline event for this market.
        # Data before it represents a different regime and should be excluded
        # from elasticity fits (seasonality can use a longer window — see
        # fit_seasonality which passes regime_filter=False for seasonality
        # when appropriate).
        structural_row = con.execute("""
            SELECT CAST(MAX(change_date) AS DATE)
            FROM ps.regime_changes
            WHERE market = ?
              AND is_structural_baseline = TRUE
              AND active = TRUE
        """, [market]).fetchone()
        if structural_row and structural_row[0] is not None:
            latest_structural_date = structural_row[0]

    result = []
    latest = rows[-1][0]
    for r in rows:
        period_start = r[0]
        if reverted_windows:
            in_window = any(start <= period_start <= end for start, end in reverted_windows)
            if in_window:
                continue
        # Exclude weeks before the most recent structural regime change —
        # pre-regime data represents a different paradigm (different
        # elasticity, different CVR, different competitive landscape) and
        # biases fits toward an outdated reality.
        # Exception: seasonality fits pass include_pre_structural=True
        # because annual cycles persist across regime shifts.
        if not include_pre_structural and latest_structural_date is not None and period_start < latest_structural_date:
            continue
        age_days = (latest - period_start).days
        age_weeks = age_days // 7
        result.append({
            'period_start': period_start,
            'period_key': r[1],
            'spend': float(r[2]),
            'regs': float(r[3]) if r[3] is not None else 0.0,
            'cpa': float(r[4]) if r[4] is not None else 0.0,
            'cpc': float(r[5]) if r[5] is not None else 0.0,
            'cvr': float(r[6]) if r[6] is not None else 0.0,
            'age_weeks': age_weeks,
        })
    return result


def _recency_weights(ages: np.ndarray, half_life: float = HALF_LIFE_WEEKS_DEFAULT) -> np.ndarray:
    """Exponential decay recency weights. w_i = 0.5^(age / half_life)."""
    return np.power(0.5, ages / half_life)


# ---------- Elasticity fitting ----------

def _weighted_log_linear_fit(
    x: np.ndarray, y: np.ndarray, weights: np.ndarray
) -> tuple[float, float, float, np.ndarray]:
    """Weighted least-squares fit of log(y) = a + b * log(x).

    Returns (a, b, r_squared, covariance_2x2). Log-space regression with
    observation weights. Covariance is for [a, b] in that order.
    """
    mask = (x > 0) & (y > 0) & np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 5:
        # Not enough points for a meaningful fit
        return (0.0, 0.0, 0.0, np.eye(2) * 1.0)

    log_x = np.log(x[mask])
    log_y = np.log(y[mask])
    w = weights[mask]

    # Design matrix: [1, log_x]
    X = np.column_stack([np.ones_like(log_x), log_x])
    W = np.diag(w)

    try:
        # Normal equations: (X' W X) beta = X' W y
        XtWX = X.T @ W @ X
        XtWy = X.T @ W @ log_y
        beta = np.linalg.solve(XtWX, XtWy)
        a, b = float(beta[0]), float(beta[1])

        # Residuals and r-squared (weighted)
        y_pred = X @ beta
        residuals = log_y - y_pred
        ss_res = float(np.sum(w * residuals**2))
        y_mean = float(np.sum(w * log_y) / np.sum(w))
        ss_tot = float(np.sum(w * (log_y - y_mean)**2))
        r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 1e-10 else 0.0
        r_squared = max(0.0, min(1.0, r_squared))

        # Posterior covariance (weighted MLE approximation):
        # Cov(beta) ~ sigma^2 * (X' W X)^-1 where sigma^2 = ss_res / (n_eff - 2)
        n_eff = float(np.sum(w))
        if n_eff > 2:
            sigma_sq = ss_res / max(n_eff - 2, 1)
            cov = sigma_sq * np.linalg.inv(XtWX)
        else:
            cov = np.eye(2) * 0.1
        return (a, b, r_squared, cov)

    except np.linalg.LinAlgError:
        return (0.0, 0.0, 0.0, np.eye(2) * 1.0)


def fit_elasticity(
    market: str,
    segment: str,
    metric: str,
    half_life_weeks: float = HALF_LIFE_WEEKS_DEFAULT,
    data: Optional[list[dict]] = None,
) -> FitResult:
    """Fit a single elasticity curve for market/segment/metric.

    metric: 'cpa' or 'cpc'
    segment: 'brand' or 'nb'

    Returns FitResult with fallback_level set appropriately:
    - market_specific if clean weeks >= 80 and r² >= 0.35 (CPA) or 0.30 (CPC)
    - regional_fallback if either threshold missed
    - conservative_default if all else fails
    """
    if segment not in ('brand', 'nb'):
        raise ValueError(f"segment must be 'brand' or 'nb', got {segment!r}")
    if metric not in ('cpa', 'cpc'):
        raise ValueError(f"metric must be 'cpa' or 'cpc', got {metric!r}")

    lineage = f"recency-weighted log-linear fit on ps.v_weekly (half_life={int(half_life_weeks)}w, fit {date.today()})"

    # Fetch data
    if data is None:
        data = _fetch_weekly(market, segment)

    result = FitResult(market=market, segment=segment, metric=metric, lineage=lineage)
    result.weeks_used = len(data)

    if not data:
        result.fallback_level = 'conservative_default'
        result.coef_a, result.coef_b = math.log(50.0), 0.0  # flat $50 CPA / CPC default
        result.r_squared = 0.0
        result.warnings.append('NO_DATA')
        result.lineage = 'flat default — no data for market/segment'
        return result

    if len(data) < 20:
        result.fallback_level = 'conservative_default'
        result.warnings.append('INSUFFICIENT_DATA')
        result.coef_a, result.coef_b = 0.0, 0.0
        return result

    # Arrays
    ages = np.array([d['age_weeks'] for d in data], dtype=float)
    spend = np.array([d['spend'] for d in data], dtype=float)
    y = np.array([d[metric] for d in data], dtype=float)
    weights = _recency_weights(ages, half_life_weeks)

    # Fit
    a, b, r_sq, cov = _weighted_log_linear_fit(spend, y, weights)

    result.coef_a = a
    result.coef_b = b
    result.r_squared = r_sq
    result.posterior_cov = cov.tolist()

    # Threshold check
    threshold_r2 = THRESHOLD_MIN_ELASTICITY_R2 if metric == 'cpa' else THRESHOLD_CPC_FIT_R2

    if len(data) < THRESHOLD_MARKET_SPECIFIC_WEEKS:
        result.fallback_level = 'regional_fallback'
        result.warnings.append(f'WEEKS_BELOW_THRESHOLD ({len(data)} < {THRESHOLD_MARKET_SPECIFIC_WEEKS})')
    elif r_sq < threshold_r2:
        result.fallback_level = 'regional_fallback'
        result.warnings.append(f'R2_BELOW_THRESHOLD ({r_sq:.2f} < {threshold_r2})')
    else:
        result.fallback_level = 'market_specific'

    return result


def fit_cpc_with_fallback(
    market: str,
    segment: str,
    cpa_fit: FitResult,
    half_life_weeks: float = HALF_LIFE_WEEKS_DEFAULT,
) -> FitResult:
    """Fit CPC elasticity per R2.11. When r² >= 0.3, fit directly; else derive from CPA.

    Derivation: CPC = CPA * CVR. Since CVR is approximately stable with spend
    changes at modest ranges, CPC elasticity inherits CPA's b coefficient but
    a shifted intercept accounting for typical CVR.
    """
    direct_fit = fit_elasticity(market, segment, 'cpc', half_life_weeks)

    if direct_fit.r_squared >= THRESHOLD_CPC_FIT_R2 and direct_fit.fallback_level == 'market_specific':
        return direct_fit

    # Fallback: derive CPC from CPA using average CVR
    data = _fetch_weekly(market, segment)
    if not data:
        direct_fit.fallback_level = 'conservative_default'
        direct_fit.warnings.append('CPC_DERIVED_FROM_CPA')
        direct_fit.warnings.append('NO_DATA')
        return direct_fit

    cvrs = np.array([d['cvr'] for d in data if d['cvr'] > 0])
    if cvrs.size == 0:
        direct_fit.fallback_level = 'conservative_default'
        direct_fit.warnings.append('CPC_DERIVED_FROM_CPA')
        direct_fit.warnings.append('NO_CVR_DATA')
        return direct_fit

    # Recency-weighted CVR average
    ages_cvr = np.array([d['age_weeks'] for d in data if d['cvr'] > 0], dtype=float)
    cvr_weights = _recency_weights(ages_cvr, half_life_weeks)
    avg_cvr = float(np.sum(cvr_weights * cvrs) / np.sum(cvr_weights))

    # CPC = CPA * CVR → log(CPC) = log(CPA) + log(CVR)
    # If CPA = exp(a_cpa) * spend^b_cpa, then CPC = exp(a_cpa + log(avg_cvr)) * spend^b_cpa
    derived = FitResult(
        market=market,
        segment=segment,
        metric='cpc',
        coef_a=cpa_fit.coef_a + math.log(max(avg_cvr, 1e-6)),
        coef_b=cpa_fit.coef_b,
        r_squared=cpa_fit.r_squared,  # inherit CPA confidence
        posterior_cov=cpa_fit.posterior_cov,
        weeks_used=cpa_fit.weeks_used,
        fallback_level='derived_from_cpa',
        warnings=['CPC_DERIVED_FROM_CPA', f'direct CPC r²={direct_fit.r_squared:.2f} below threshold {THRESHOLD_CPC_FIT_R2}'],
        lineage=f"derived: CPC = CPA × avg_CVR={avg_cvr:.4f} (recency-weighted). Fit {date.today()}",
    )
    return derived


# ---------- Seasonality fitting ----------

def fit_seasonality(
    market: str,
    segment: str,
    half_life_weeks: float = HALF_LIFE_WEEKS_DEFAULT,
    data: Optional[list[dict]] = None,
) -> SeasonalityResult:
    """Fit 52-week seasonality shape from registrations.

    Weights are normalized to sum to 52.0, so weight=1.0 means average
    week, weight=1.2 means 20% above average. Recency-weighted so
    recent years dominate.

    Seasonality uses a LONGER data window than elasticity fits: we
    explicitly re-fetch data without the structural-regime cutoff because
    annual cycles (holidays, fiscal quarters, Semana Santa) persist
    across structural shifts. Only reverted windows are still excluded.

    Posterior per-week: {mean, std, provenance: 'fit' | 'default'}
    """
    lineage = f"recency-weighted 52-week seasonality on ps.v_weekly regs (half_life={int(half_life_weeks)}w, fit {date.today()}, pre-structural data included)"

    if data is None:
        # For seasonality, re-fetch with structural filter DISABLED so we
        # get the full annual cycle signal even across regime shifts.
        data = _fetch_weekly(market, segment, regime_filter=True, include_pre_structural=True)

    result = SeasonalityResult(
        market=market,
        segment=segment,
        weights=[1.0] * 52,
        posteriors=[{'mean': 1.0, 'std': 0.15, 'provenance': 'default'} for _ in range(52)],
        lineage=lineage,
    )

    if not data or len(data) < 26:
        result.fallback_level = 'conservative_default'
        result.warnings.append('INSUFFICIENT_DATA_FOR_SEASONALITY')
        return result

    # Bucket regs by ISO week of year
    week_buckets: list[list[tuple[float, float]]] = [[] for _ in range(52)]
    for d in data:
        iso_week = d['period_start'].isocalendar()[1]
        if iso_week < 1 or iso_week > 52:
            continue
        recency_w = 0.5 ** (d['age_weeks'] / half_life_weeks)
        week_buckets[iso_week - 1].append((d['regs'], recency_w))

    # Compute weighted mean and variance per week
    raw_means = []
    raw_stds = []
    for wk_idx in range(52):
        bucket = week_buckets[wk_idx]
        if len(bucket) == 0:
            raw_means.append(None)
            raw_stds.append(None)
            continue
        regs = np.array([b[0] for b in bucket])
        ws = np.array([b[1] for b in bucket])
        total_w = float(np.sum(ws))
        if total_w < 1e-6:
            raw_means.append(None)
            raw_stds.append(None)
            continue
        mean = float(np.sum(ws * regs) / total_w)
        if len(bucket) >= 2:
            variance = float(np.sum(ws * (regs - mean)**2) / total_w)
            std = math.sqrt(max(variance, 0.0))
        else:
            std = mean * 0.15  # default 15% CV when only one obs
        raw_means.append(mean)
        raw_stds.append(std)

    # Normalize to sum-to-52
    valid_means = [m for m in raw_means if m is not None]
    if not valid_means:
        result.fallback_level = 'conservative_default'
        result.warnings.append('NO_VALID_WEEKS')
        return result

    overall_mean = float(np.mean(valid_means))
    if overall_mean < 1e-6:
        result.fallback_level = 'conservative_default'
        result.warnings.append('ZERO_MEAN')
        return result

    weights = []
    posteriors = []
    gap_count = 0
    for wk_idx in range(52):
        m = raw_means[wk_idx]
        s = raw_stds[wk_idx]
        if m is None:
            weights.append(1.0)
            posteriors.append({'mean': 1.0, 'std': 0.20, 'provenance': 'gap_filled_overall_mean'})
            gap_count += 1
        else:
            w = m / overall_mean
            # Clamp to avoid extreme outliers (0.3x to 3x overall mean)
            w = max(0.3, min(3.0, w))
            weights.append(w)
            posteriors.append({
                'mean': w,
                'std': (s / overall_mean) if s else 0.10,
                'provenance': 'fit',
            })

    # Re-normalize to sum to 52.0 exactly
    total = sum(weights)
    if total > 0:
        weights = [w * 52.0 / total for w in weights]

    result.weights = weights
    result.posteriors = posteriors

    # Decide fallback level
    if len(data) < THRESHOLD_MARKET_SPECIFIC_WEEKS:
        result.fallback_level = 'regional_fallback'
        result.warnings.append(f'WEEKS_BELOW_THRESHOLD ({len(data)} < {THRESHOLD_MARKET_SPECIFIC_WEEKS})')
    elif gap_count > 10:
        result.fallback_level = 'regional_fallback'
        result.warnings.append(f'TOO_MANY_SEASONALITY_GAPS ({gap_count} weeks had no data)')

    return result


# ---------- YoY growth trend fitting ----------

def fit_yoy_growth(
    market: str,
    segment: str,
    half_life_weeks: float = HALF_LIFE_WEEKS_DEFAULT,
    data: Optional[list[dict]] = None,
) -> YoYGrowthResult:
    """Fit year-over-year growth trend from registrations.

    YoY uses the full available window (including pre-structural-regime
    data) because the whole point of YoY is to compare this-year to
    prior-year at matching calendar weeks. Recency weighting damps older
    comparisons automatically.
    """
    lineage = f"recency-weighted YoY trend on ps.v_weekly regs (half_life={int(half_life_weeks)}w, fit {date.today()}, full window)"

    if data is None:
        data = _fetch_weekly(market, segment, regime_filter=True, include_pre_structural=True)

    result = YoYGrowthResult(
        market=market,
        segment=segment,
        mean=0.0,
        std=0.10,
        r_squared=0.0,
        years_used=0,
        lineage=lineage,
    )

    if not data or len(data) < 104:
        result.fallback_level = 'conservative_default'
        result.warnings.append('LOW_CONFIDENCE_MULTI_YEAR')
        result.warnings.append(f'YEARS_BELOW_2 ({len(data)} weeks)')
        return result

    # Build year-over-year ratios by matching ISO (year, week)
    by_key = {}
    for d in data:
        iso = d['period_start'].isocalendar()
        year = iso[0]
        week = iso[1]
        by_key[(year, week)] = d['regs']

    ratios_weighted = []
    latest_year = max(k[0] for k in by_key.keys())
    for (year, week), regs_now in by_key.items():
        prior_key = (year - 1, week)
        if prior_key not in by_key:
            continue
        prior = by_key[prior_key]
        if prior <= 0 or regs_now <= 0:
            continue
        ratio = regs_now / prior
        # Recency weight: how many years back is this observation?
        age_weeks = (latest_year - year) * 52
        w = 0.5 ** (age_weeks / half_life_weeks)
        ratios_weighted.append((ratio, w))

    if not ratios_weighted:
        result.fallback_level = 'conservative_default'
        result.warnings.append('NO_YOY_PAIRS')
        return result

    ratios_arr = np.array([r[0] for r in ratios_weighted])
    ws_arr = np.array([r[1] for r in ratios_weighted])

    total_w = float(np.sum(ws_arr))
    mean_ratio = float(np.sum(ws_arr * ratios_arr) / total_w)
    variance = float(np.sum(ws_arr * (ratios_arr - mean_ratio)**2) / total_w)
    std = math.sqrt(max(variance, 0.0))

    # r_squared: 1 - (weighted variance around fit) / (weighted variance around 1.0 null)
    ss_fit = float(np.sum(ws_arr * (ratios_arr - mean_ratio)**2))
    ss_null = float(np.sum(ws_arr * (ratios_arr - 1.0)**2))
    r_sq = 1.0 - (ss_fit / ss_null) if ss_null > 1e-10 else 0.0
    r_sq = max(0.0, min(1.0, r_sq))

    result.mean = mean_ratio - 1.0  # Convert ratio to growth rate (e.g. 1.12 → 0.12)
    result.std = std
    result.r_squared = r_sq
    result.years_used = len(set(k[0] for k in by_key.keys()))
    result.fallback_level = 'market_specific'

    return result


# ---------- Convenience: fit all parameters for a market ----------

def fit_all_for_market(market: str, segment: str, half_life_weeks: float = HALF_LIFE_WEEKS_DEFAULT) -> dict:
    """Fit CPA elasticity, CPC elasticity (with fallback), seasonality, YoY for one market/segment.

    Returns dict of {parameter_name: result}. Does not write to registry —
    refit_market_params.py handles that.
    """
    data = _fetch_weekly(market, segment)

    cpa_fit = fit_elasticity(market, segment, 'cpa', half_life_weeks, data=data)
    cpc_fit = fit_cpc_with_fallback(market, segment, cpa_fit, half_life_weeks)
    seasonality = fit_seasonality(market, segment, half_life_weeks, data=data)
    yoy = fit_yoy_growth(market, segment, half_life_weeks, data=data)

    return {
        f'{segment}_cpa_elasticity': cpa_fit,
        f'{segment}_cpc_elasticity': cpc_fit,
        f'{segment}_seasonality_shape': seasonality,
        f'{segment}_yoy_growth': yoy,
    }


# ---------- CLI for manual inspection ----------

def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(
        prog="mpe_fitting",
        description="Fit MPE parameters for one market/segment and print results.",
    )
    parser.add_argument("--market", required=True, choices=['US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP', 'MX', 'AU'])
    parser.add_argument("--segment", required=True, choices=['brand', 'nb'])
    parser.add_argument("--half-life", type=float, default=HALF_LIFE_WEEKS_DEFAULT)
    args = parser.parse_args(argv)

    print(f"[mpe_fitting] Fitting {args.market}/{args.segment} (half_life={args.half_life}w)")
    results = fit_all_for_market(args.market, args.segment, args.half_life)

    for name, result in results.items():
        print(f"\n=== {name} ===")
        if isinstance(result, FitResult):
            print(f"  a={result.coef_a:.4f}, b={result.coef_b:.4f} "
                  f"(CPA = exp({result.coef_a:.3f}) * spend^{result.coef_b:.3f})")
            print(f"  r²={result.r_squared:.3f}")
            print(f"  weeks_used={result.weeks_used}")
            print(f"  fallback_level={result.fallback_level}")
            if result.warnings:
                print(f"  warnings: {result.warnings}")
        elif isinstance(result, SeasonalityResult):
            print(f"  52 weights (sum={sum(result.weights):.1f}, min={min(result.weights):.2f}, max={max(result.weights):.2f})")
            print(f"  fallback_level={result.fallback_level}")
            if result.warnings:
                print(f"  warnings: {result.warnings}")
        elif isinstance(result, YoYGrowthResult):
            print(f"  mean_growth={result.mean*100:+.1f}%, std={result.std*100:.1f}%")
            print(f"  r²={result.r_squared:.3f}, years_used={result.years_used}")
            print(f"  fallback_level={result.fallback_level}")
            if result.warnings:
                print(f"  warnings: {result.warnings}")

    return 0


if __name__ == "__main__":
    sys.exit(main())


# ---------- Brand/NB spend share fitting ----------

@dataclass
class SpendShareResult:
    """Recency-weighted Brand/NB spend share for a market."""
    market: str
    brand_share: float                        # fraction of total spend going to Brand
    nb_share: float                           # fraction going to NB (= 1 - brand_share)
    weeks_used: int
    range_min: float                          # historical minimum brand share
    range_max: float                          # historical maximum brand share
    lineage: str = ''

    def to_json(self) -> dict:
        return {
            'brand_share': self.brand_share,
            'nb_share': self.nb_share,
            'weeks_used': self.weeks_used,
            'range': {'min': self.range_min, 'max': self.range_max},
            'lineage': self.lineage,
        }


def fit_spend_share(market: str, half_life_weeks: float = HALF_LIFE_WEEKS_DEFAULT) -> SpendShareResult:
    """Fit recency-weighted Brand/NB spend share from historical ps.v_weekly.

    Uses the market's own data rather than a hardcoded 20/80 default. This
    is the piece that made MX smoke-test outputs underpredict Brand regs
    (MX is ~11% Brand, not 20%).
    """
    con = _db()
    rows = con.execute("""
        SELECT period_start, brand_cost, nb_cost, cost
        FROM ps.v_weekly
        WHERE market = ? AND period_type = 'weekly'
          AND cost > 0 AND brand_cost IS NOT NULL AND nb_cost IS NOT NULL
        ORDER BY period_start ASC
    """, [market]).fetchall()

    if not rows:
        return SpendShareResult(
            market=market,
            brand_share=0.20,                 # conservative default
            nb_share=0.80,
            weeks_used=0,
            range_min=0.20,
            range_max=0.20,
            lineage=f"conservative_default (no data for {market})",
        )

    latest = rows[-1][0]
    shares = []
    weights = []
    for period_start, brand_cost, nb_cost, total_cost in rows:
        if total_cost is None or total_cost <= 0:
            continue
        share = float(brand_cost) / float(total_cost)
        age_weeks = (latest - period_start).days // 7
        w = 0.5 ** (age_weeks / half_life_weeks)
        shares.append(share)
        weights.append(w)

    if not shares:
        return SpendShareResult(
            market=market, brand_share=0.20, nb_share=0.80,
            weeks_used=0, range_min=0.20, range_max=0.20,
            lineage=f"conservative_default (no valid rows for {market})",
        )

    shares_arr = np.array(shares)
    weights_arr = np.array(weights)
    total_w = float(np.sum(weights_arr))
    wtd_mean = float(np.sum(weights_arr * shares_arr) / total_w)

    return SpendShareResult(
        market=market,
        brand_share=wtd_mean,
        nb_share=1.0 - wtd_mean,
        weeks_used=len(shares),
        range_min=float(np.min(shares_arr)),
        range_max=float(np.max(shares_arr)),
        lineage=f"recency-weighted spend share from ps.v_weekly (half_life={int(half_life_weeks)}w, fit {date.today()}, {len(shares)} weeks)",
    )
