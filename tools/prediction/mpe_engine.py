"""MPE Engine — core planning projection logic.

WHY THIS EXISTS
    This is the canonical projection engine for the Market Projection
    Engine. Given a scope (market or region), a time period, a target
    mode (spend/ieccp/regs), and optional modifiers, it produces a full
    9-KPI projection with credible intervals, warnings, and provenance.

    This engine serves planning projections with owner-defined targets.
    It coexists with bayesian_projector.py (which does live week-ahead
    forecasts for wbr_pipeline.py) — different use case, different
    entry point, no shared mutable state.

HOW THE OWNER MAINTAINS IT
    You never call this module directly in day-to-day use. The UI and
    CLI call into project() behind the scenes. The refit hook populates
    the parameter registry this engine reads from.

    If a projection looks wrong:
    1. Check the freshness banner — run the refit hook if stale
    2. Hover the KPI — "Explain this" tooltip shows the formula and lineage
    3. Read the warnings panel — HIGH_EXTRAPOLATION / DATA_LIMITED / etc
    4. Check the fallback_level in the provenance modal
    5. If none of that explains it, open this file and read the project()
       function. The math is straightforward by design.

WHAT HAPPENS ON FAILURE
    - SETUP_REQUIRED: market has no parameters → engine refuses to project
    - STALE_PARAMETERS: past refit_cadence → banner + warning but projection
      still produced (owner decides whether to trust it)
    - Infeasible target: engine returns structured INFEASIBLE response with
      binding_constraint and closest_feasible suggestion
    - HIGH_EXTRAPOLATION: spend > 1.5× historical max → Hill ceiling applied
    - REGIONAL_FALLBACK: parameter uses regional curve → DATA_LIMITED banner

MATH OUTLINE
    Per-week per-segment:
        CPA = exp(a_cpa) * spend^b_cpa
        CPC = exp(a_cpc) * spend^b_cpc   (or derived from CPA)
        regs = spend / CPA
        clicks = spend / CPC
    Weekly spend = target_spend * seasonality_weight[week] / 52
    YoY growth applied multiplicatively across years for Multi_Year
    ie%CCP = total_spend / (brand_regs * Brand_CCP + nb_regs * NB_CCP) * 100

    Target modes:
        spend: spend given, compute everything else
        ieccp: binary search spend that yields target ie%CCP
        regs: solve spend for target regs, check feasibility

    Regional rollup: independent per-market projections, sum segments,
    compute regional ie%CCP with sum-then-divide (never average CCP).
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from typing import Any, Optional

import numpy as np

sys.path.insert(0, os.path.expanduser('~/shared/tools'))


# ---------- Constants ----------

ENGINE_VERSION = "1.0.0"

ALL_MARKETS = ['US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP', 'MX', 'AU']
ALL_REGIONS = ['NA', 'EU5', 'WW']
REGION_CONSTITUENTS = {
    'NA': ['US', 'CA'],
    'EU5': ['UK', 'DE', 'FR', 'IT', 'ES'],
    'WW': ALL_MARKETS,
}

HISTORICAL_EXTRAPOLATION_MULTIPLIER = 1.5   # R2.13
HIGH_UNCERTAINTY_RATIO = 2.0                # R12.5
VERY_WIDE_CI_RATIO = 3.0                    # R11.8 (MY2)
STALE_DAYS_ANNUAL = 365
STALE_DAYS_QUARTERLY = 120
MIN_WEEKS_MULTI_YEAR = 104                  # R11.5


# ---------- Data classes ----------

@dataclass
class ProjectionInputs:
    """User-supplied inputs for a projection run."""
    scope: str                                # market code OR region code
    time_period: str                          # 'W{NN}' | 'M{MM}' | 'Q{N}' | 'Y{YYYY}' | 'MY1' | 'MY2'
    target_mode: str                          # 'spend' | 'ieccp' | 'regs'
    target_value: float
    brand_uplift_pct: float = 0.0
    nb_uplift_pct: float = 0.0
    nb_elasticity_override: Optional[dict] = None
    brand_cpa_override: Optional[float] = None
    parameter_snapshot_at: Optional[datetime] = None
    credibility_levels: tuple = (0.50, 0.70, 0.90)
    # Regional target resolution (R6.5): 'regional' or 'per_market'
    regional_target_mode: str = 'regional'


@dataclass
class WeeklyOutput:
    """One week of projection output."""
    week_num: int
    week_key: str
    brand_regs: float
    nb_regs: float
    brand_spend: float
    nb_spend: float
    brand_clicks: float
    nb_clicks: float
    brand_cpa: float
    nb_cpa: float
    blended_cpa: float
    ieccp: float | None


@dataclass
class ProjectionOutputs:
    """Full projection result."""
    scope: str
    time_period: str
    target_mode: str
    target_value: float
    outcome: str                              # 'OK' | 'INFEASIBLE' | 'SETUP_REQUIRED'
    weeks: list[WeeklyOutput] = field(default_factory=list)
    totals: dict = field(default_factory=dict)
    credible_intervals: dict = field(default_factory=dict)
    constituent_markets: list[dict] = field(default_factory=list)
    parameters_used: dict = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    fallback_level_summary: str = 'all_market_specific'
    yoy_growth_applied: dict = field(default_factory=dict)
    infeasibility_reason: dict | None = None
    methodology_version: str = ENGINE_VERSION
    generated_at: str = ''
    # v1.1 Slim additions (Phase 6.1.6):
    contribution_breakdown: dict = field(default_factory=dict)
    locked_ytd_summary: dict = field(default_factory=dict)
    regime_stack: list[dict] = field(default_factory=list)


@dataclass
class InfeasibilityResponse:
    """Structured response when a target cannot be achieved."""
    outcome: str = 'INFEASIBLE'
    binding_constraint: str = ''
    explanation: str = ''
    closest_feasible: dict = field(default_factory=dict)


# ---------- Connection ----------

_con = None


def _db():
    global _con
    if _con is None:
        import duckdb
        from prediction.config import MOTHERDUCK_TOKEN
        _con = duckdb.connect(
            f'md:ps_analytics?motherduck_token={MOTHERDUCK_TOKEN}',
            read_only=True,
        )
    return _con


# ---------- Parameter loading ----------

def load_parameters(market: str) -> dict:
    """Load all active parameters for a market from ps.market_projection_params_current.

    Returns dict keyed by parameter_name with keys: value_scalar, value_json,
    fallback_level, lineage, last_refit_at, refit_cadence. value_json is
    parsed from string if MotherDuck returned it that way.
    """
    import json as _json
    con = _db()
    rows = con.execute("""
        SELECT parameter_name, value_scalar, value_json, fallback_level,
               lineage, last_refit_at, refit_cadence, source
        FROM ps.market_projection_params_current
        WHERE market = ?
    """, [market]).fetchall()

    params = {}
    for r in rows:
        name, scalar, json_val, fallback, lineage, refit_at, cadence, source = r
        # DuckDB / MotherDuck may return JSON as string — parse if so
        if isinstance(json_val, str):
            try:
                json_val = _json.loads(json_val)
            except (ValueError, TypeError):
                pass
        params[name] = {
            'value_scalar': scalar,
            'value_json': json_val,
            'fallback_level': fallback,
            'lineage': lineage,
            'last_refit_at': refit_at,
            'refit_cadence': cadence,
            'source': source,
        }

    # Mechanism A (2026-04-23): join operational spend bounds from market_constraints_manual.
    # These are human-curated floor/ceiling on weekly per-segment spend that reflect
    # operational reality the elasticity fit cannot see (e.g. MX NB floor $15K/wk —
    # below this is policy pullback, not demand-revealed). Solver consumes these
    # to clamp its search space; weekly project loop clamps per-week spend.
    # Missing row or NULL values = no bounds (backward compatible).
    try:
        bounds_row = con.execute("""
            SELECT min_weekly_nb_spend, max_weekly_nb_spend,
                   min_weekly_brand_spend, max_weekly_brand_spend,
                   spend_bounds_rationale
            FROM ps.market_constraints_manual
            WHERE market = ?
        """, [market]).fetchone()
        if bounds_row is not None:
            min_nb, max_nb, min_brand, max_brand, rationale = bounds_row
            params['_spend_bounds'] = {
                'min_weekly_nb_spend': min_nb,
                'max_weekly_nb_spend': max_nb,
                'min_weekly_brand_spend': min_brand,
                'max_weekly_brand_spend': max_brand,
                'rationale': rationale,
            }
    except Exception:
        # market_constraints_manual may not have the new columns yet in test DBs
        pass

    return params_legacy_return_hack(params)


def params_legacy_return_hack(params: dict) -> dict:
    """Compatibility shim — identical to returning params. Exists as an anchor
    for future wrapping (e.g. read-through cache) without touching call sites."""
    return params


def required_parameter_names(market: str) -> list[str]:
    """Return the list of parameters required for a full projection.

    Phase 6.2.4 (2026-04-23): v1.1 Slim requires only nb_cpa_elasticity +
    nb_seasonality_shape + CCPs (non-AU) + supported_target_modes. The
    deprecated brand_cpa_elasticity / brand_yoy_growth / brand_spend_share
    are no longer required — Brand trajectory is computed from
    ps.v_weekly + ps.regime_fit_state directly.

    AU is special-cased: no ieccp parameters required.
    """
    base = [
        'brand_ccp' if market != 'AU' else None,
        'nb_ccp' if market != 'AU' else None,
        'nb_cpa_elasticity',
        'nb_seasonality_shape',
        'nb_yoy_growth',
        'supported_target_modes',
        # v1.1 Slim Brand params (Phase 6.2.4) — currently bootstrap placeholders,
        # real values populated by fit_market.py. Their presence (even bootstrap)
        # is required as the contract signal that v1.1 Slim is active.
        'brand_trajectory_weights',
    ]
    return [p for p in base if p is not None]


def check_parameter_readiness(market: str, params: dict) -> list[str]:
    """Check for missing or stale parameters. Returns warnings list.

    SETUP_REQUIRED if any required parameter is missing entirely.
    STALE_PARAMETERS if any parameter is past its refit_cadence.
    """
    warnings = []
    required = required_parameter_names(market)
    missing = [p for p in required if p not in params]
    if missing:
        warnings.append(f"SETUP_REQUIRED: {market} missing parameters: {missing}")
        return warnings   # short-circuit — no point checking staleness if missing

    today = datetime.now()
    for name, param in params.items():
        refit_at = param.get('last_refit_at')
        cadence = param.get('refit_cadence', 'quarterly')
        if refit_at is None:
            continue
        if isinstance(refit_at, str):
            try:
                refit_at = datetime.fromisoformat(refit_at)
            except ValueError:
                continue
        age_days = (today - refit_at).days
        max_age = STALE_DAYS_ANNUAL if cadence == 'annual' else STALE_DAYS_QUARTERLY
        if age_days > max_age:
            warnings.append(f"STALE_PARAMETERS: {name} last refit {age_days}d ago (cadence: {cadence})")
    return warnings


# ---------- Time period parsing ----------

def parse_time_period(time_period: str) -> dict:
    """Parse a time_period string. Returns dict with weeks, year span, type."""
    tp = time_period.upper().strip()

    # NOTE: check MY (multi-year) BEFORE M (month) because both start with 'M'
    if tp.startswith('MY'):
        # Multi-year MY1 or MY2 (R11.1 — MY3 forbidden)
        try:
            n = int(tp[2:])
        except ValueError:
            raise ValueError(f"Invalid multi-year period {time_period!r}")
        if n > 2:
            raise ValueError("MY3 and beyond not supported in v1 (R11.9). Use MY1 or MY2.")
        if n < 1:
            raise ValueError(f"Multi-year must be >= 1, got {n}")
        return {'type': 'multi_year', 'weeks': list(range(1, 53)), 'year_offset': 1, 'n_years': n}

    if tp.startswith('W'):
        wk = int(tp[1:])
        return {'type': 'week', 'weeks': [wk], 'year_offset': 0, 'n_years': 1}
    if tp.startswith('M'):
        # Single month e.g. M04 (April)
        mm = int(tp[1:])
        start_wk = (mm - 1) * 4 + 1
        end_wk = min(start_wk + 4, 52)
        return {'type': 'month', 'weeks': list(range(start_wk, end_wk + 1)), 'year_offset': 0, 'n_years': 1}
    if tp.startswith('Q'):
        q = int(tp[1:])
        start_wk = (q - 1) * 13 + 1
        end_wk = min(start_wk + 13, 52)
        return {'type': 'quarter', 'weeks': list(range(start_wk, end_wk + 1)), 'year_offset': 0, 'n_years': 1}
    if tp.startswith('Y'):
        return {'type': 'year', 'weeks': list(range(1, 53)), 'year_offset': 0, 'n_years': 1}

    raise ValueError(f"Unparseable time_period: {time_period!r}")


# ---------- Point projection (single parameter set → one outcome) ----------

def _apply_cpa_elasticity(spend: float, a: float, b: float) -> float:
    """CPA = exp(a) * spend^b, clamped to positive."""
    if spend <= 0:
        return 1.0
    try:
        cpa = math.exp(a) * (spend ** b)
    except (OverflowError, ValueError):
        cpa = 1e6
    return max(cpa, 0.01)


def _apply_cpc_elasticity(spend: float, a: float, b: float) -> float:
    """CPC = exp(a) * spend^b, clamped to positive."""
    if spend <= 0:
        return 0.01
    try:
        cpc = math.exp(a) * (spend ** b)
    except (OverflowError, ValueError):
        cpc = 100.0
    return max(cpc, 0.01)


def _project_one_week(
    brand_spend: float,
    nb_spend: float,
    brand_cpa_elast: dict,
    nb_cpa_elast: dict,
    brand_cpc_elast: dict,
    nb_cpc_elast: dict,
    brand_ccp: float | None,
    nb_ccp: float | None,
    week_num: int,
    week_key: str,
) -> WeeklyOutput:
    """Project a single week given per-segment spend."""
    brand_cpa = _apply_cpa_elasticity(brand_spend, brand_cpa_elast['a'], brand_cpa_elast['b'])
    nb_cpa = _apply_cpa_elasticity(nb_spend, nb_cpa_elast['a'], nb_cpa_elast['b'])
    brand_cpc = _apply_cpc_elasticity(brand_spend, brand_cpc_elast['a'], brand_cpc_elast['b'])
    nb_cpc = _apply_cpc_elasticity(nb_spend, nb_cpc_elast['a'], nb_cpc_elast['b'])

    brand_regs = brand_spend / brand_cpa if brand_cpa > 0 else 0.0
    nb_regs = nb_spend / nb_cpa if nb_cpa > 0 else 0.0
    brand_clicks = brand_spend / brand_cpc if brand_cpc > 0 else 0.0
    nb_clicks = nb_spend / nb_cpc if nb_cpc > 0 else 0.0

    total_spend = brand_spend + nb_spend
    total_regs = brand_regs + nb_regs
    blended_cpa = total_spend / total_regs if total_regs > 0 else 0.0

    # ie%CCP: only meaningful when both CCPs present
    ieccp = None
    if brand_ccp is not None and nb_ccp is not None:
        denom = brand_regs * brand_ccp + nb_regs * nb_ccp
        ieccp = (total_spend / denom * 100.0) if denom > 0 else None

    return WeeklyOutput(
        week_num=week_num,
        week_key=week_key,
        brand_regs=brand_regs,
        nb_regs=nb_regs,
        brand_spend=brand_spend,
        nb_spend=nb_spend,
        brand_clicks=brand_clicks,
        nb_clicks=nb_clicks,
        brand_cpa=brand_cpa,
        nb_cpa=nb_cpa,
        blended_cpa=blended_cpa,
        ieccp=ieccp,
    )


def _project_market_spend_target(
    total_spend: float,
    inputs: ProjectionInputs,
    params: dict,
    tp: dict,
) -> tuple[list[WeeklyOutput], dict]:
    """Project a market given total_spend distributed by seasonality."""
    market = inputs.scope

    # Extract fitted parameters
    brand_cpa_elast = params['brand_cpa_elasticity']['value_json'] or {'a': 0, 'b': 0}
    nb_cpa_elast = params['nb_cpa_elasticity']['value_json'] or {'a': 0, 'b': 0}
    brand_cpc_elast = params.get('brand_cpc_elasticity', {}).get('value_json') or brand_cpa_elast
    nb_cpc_elast = params.get('nb_cpc_elasticity', {}).get('value_json') or nb_cpa_elast
    brand_seasonality = params['brand_seasonality_shape']['value_json'] or {}
    nb_seasonality = params['nb_seasonality_shape']['value_json'] or {}
    brand_yoy = params['brand_yoy_growth']['value_json'] or {'mean': 0, 'std': 0}
    nb_yoy = params['nb_yoy_growth']['value_json'] or {'mean': 0, 'std': 0}

    brand_ccp = params.get('brand_ccp', {}).get('value_scalar')
    nb_ccp = params.get('nb_ccp', {}).get('value_scalar')

    # Apply overrides
    if inputs.brand_cpa_override is not None:
        brand_ccp = inputs.brand_cpa_override   # reuse override lane for CCP sanity test
    if inputs.nb_elasticity_override is not None:
        nb_cpa_elast = {**nb_cpa_elast, **inputs.nb_elasticity_override}

    # Extract seasonality weights (default to flat if missing)
    brand_weights = brand_seasonality.get('weights', [1.0] * 52)
    nb_weights = nb_seasonality.get('weights', [1.0] * 52)

    # Estimate historical Brand/NB spend split from fitted parameter (Task 1.5)
    # Falls back to 20/80 default only if parameter missing — engine emits a warning elsewhere
    share_param = params.get('brand_spend_share', {}).get('value_json') or {}
    brand_share = float(share_param.get('brand_share', 0.20))
    nb_share = 1.0 - brand_share

    # YoY adjustment for multi-year
    yoy_multiplier = 1.0
    yoy_applied = {'brand': 0.0, 'nb': 0.0}
    if tp['type'] == 'multi_year':
        years_forward = tp['n_years']
        brand_growth = (1.0 + (brand_yoy.get('mean', 0) or 0.0)) ** years_forward
        nb_growth = (1.0 + (nb_yoy.get('mean', 0) or 0.0)) ** years_forward
        yoy_applied['brand'] = brand_growth - 1.0
        yoy_applied['nb'] = nb_growth - 1.0
        yoy_multiplier = (brand_share * brand_growth + nb_share * nb_growth)

    weeks_out: list[WeeklyOutput] = []
    for wk_num in tp['weeks']:
        idx = (wk_num - 1) % 52
        brand_wt = brand_weights[idx] if idx < len(brand_weights) else 1.0
        nb_wt = nb_weights[idx] if idx < len(nb_weights) else 1.0

        n_weeks = max(len(tp['weeks']), 1)
        period_factor = 1.0 / n_weeks

        week_brand_spend = total_spend * brand_share * brand_wt * period_factor * (1 + inputs.brand_uplift_pct / 100.0) * yoy_multiplier
        week_nb_spend = total_spend * nb_share * nb_wt * period_factor * (1 + inputs.nb_uplift_pct / 100.0) * yoy_multiplier

        wk = _project_one_week(
            week_brand_spend, week_nb_spend,
            brand_cpa_elast, nb_cpa_elast,
            brand_cpc_elast, nb_cpc_elast,
            brand_ccp, nb_ccp,
            wk_num, f"{tp['type']}_W{wk_num:02d}",
        )
        weeks_out.append(wk)

    # Totals
    total_brand_regs = sum(w.brand_regs for w in weeks_out)
    total_nb_regs = sum(w.nb_regs for w in weeks_out)
    total_brand_spend = sum(w.brand_spend for w in weeks_out)
    total_nb_spend = sum(w.nb_spend for w in weeks_out)
    total_brand_clicks = sum(w.brand_clicks for w in weeks_out)
    total_nb_clicks = sum(w.nb_clicks for w in weeks_out)
    total_regs = total_brand_regs + total_nb_regs
    total_sp = total_brand_spend + total_nb_spend

    ieccp_total = None
    if brand_ccp is not None and nb_ccp is not None and total_regs > 0:
        denom = total_brand_regs * brand_ccp + total_nb_regs * nb_ccp
        if denom > 0:
            ieccp_total = total_sp / denom * 100.0

    totals = {
        'brand_regs': total_brand_regs,
        'nb_regs': total_nb_regs,
        'total_regs': total_regs,
        'brand_spend': total_brand_spend,
        'nb_spend': total_nb_spend,
        'total_spend': total_sp,
        'brand_clicks': total_brand_clicks,
        'nb_clicks': total_nb_clicks,
        'blended_cpa': total_sp / total_regs if total_regs > 0 else 0.0,
        'ieccp': ieccp_total,
        'yoy_growth_applied': yoy_applied,
    }
    return weeks_out, totals


# ---------- Target mode solvers ----------
#
# REMOVED in v1.1 Slim (Phase 6.1.6, 2026-04-23):
# - _solve_ieccp_target: replaced by prediction.nb_residual_solver._solve_ieccp_branch
#   with target-relational bounds (target ± 500bps) instead of hard floors.
# - _solve_regs_target: replaced by prediction.nb_residual_solver (regs branch
#   ships in Phase 6.2.1).
# - _project_market_spend_target: KEPT TEMPORARILY for Monte Carlo uncertainty
#   (see _mc_project_point below). Phase 6.2.x rewrites MC to sample Brand
#   trajectory + NB residual uncertainty instead of the top-down elasticity.
#   Marked deprecated; no new callers.
#
# The root-cause bug this fix addressed: v1's top-down solver averaged
# elasticity across regime-incompatible weeks and could silently project
# below YTD actuals, producing MX Y2026 @ 75% = $443K (vs domain-expert
# $800K-$1.2M). v1.1 Slim fixes by separating Brand (anchor) from NB
# (residual) and respecting Locked-YTD as a pre-solve partition.

# ---------- Main entry point ----------

def project(inputs: ProjectionInputs) -> ProjectionOutputs:
    """Produce a full projection for a single scope.

    Handles: markets (US, CA, UK, DE, FR, IT, ES, JP, MX, AU) and
    regions (NA, EU5, WW). Returns ProjectionOutputs with weeks,
    totals, credible_intervals (if Monte Carlo is invoked separately),
    warnings, parameters_used, and fallback_level_summary.
    """
    out = ProjectionOutputs(
        scope=inputs.scope,
        time_period=inputs.time_period,
        target_mode=inputs.target_mode,
        target_value=inputs.target_value,
        outcome='OK',
        generated_at=datetime.now().isoformat(),
    )

    # Parse time period (may raise on MY3+)
    try:
        tp = parse_time_period(inputs.time_period)
    except ValueError as e:
        out.outcome = 'INVALID_INPUT'
        out.warnings.append(f"TIME_PERIOD_INVALID: {e}")
        return out

    # Multi-year data-quality check (R11.5)
    if tp['type'] == 'multi_year' and inputs.scope in ALL_MARKETS:
        try:
            from prediction.mpe_fitting import _fetch_weekly
            data = _fetch_weekly(inputs.scope, 'brand', regime_filter=False)
            if len(data) < MIN_WEEKS_MULTI_YEAR:
                out.warnings.append(f"LOW_CONFIDENCE_MULTI_YEAR ({len(data)} weeks < {MIN_WEEKS_MULTI_YEAR})")
        except Exception:
            pass  # don't let the data check block projection

    # Route: region or market
    if inputs.scope in ALL_REGIONS:
        return _project_region(inputs, tp, out)
    if inputs.scope not in ALL_MARKETS:
        out.outcome = 'INVALID_INPUT'
        out.warnings.append(f"UNKNOWN_SCOPE: {inputs.scope}")
        return out

    # Market-level projection
    market = inputs.scope
    params = load_parameters(market)

    # Readiness check
    readiness_warnings = check_parameter_readiness(market, params)
    out.warnings.extend(readiness_warnings)
    if any(w.startswith('SETUP_REQUIRED') for w in readiness_warnings):
        out.outcome = 'SETUP_REQUIRED'
        return out

    # Validate target_mode against supported_target_modes
    supported_modes = params.get('supported_target_modes', {}).get('value_json', ['spend', 'ieccp', 'regs'])
    if inputs.target_mode not in supported_modes:
        out.outcome = 'INVALID_INPUT'
        out.warnings.append(
            f"UNSUPPORTED_TARGET_MODE: {inputs.target_mode!r} not in {supported_modes!r} for {market}"
        )
        return out

    # v1.1 Slim target solving (Phase 6.1.6): Brand-Anchor + NB-Residual.
    # For Y-periods, use Locked-YTD to respect actuals; otherwise no-YTD path.
    # The v1 _solve_ieccp_target/_solve_regs_target/_project_market_spend_target
    # functions have been removed from the primary project() path. They remain
    # in _mc_project_point for Monte Carlo uncertainty only (Phase 6.2.x will
    # rewrite MC to Brand trajectory sampling).
    from prediction.brand_trajectory import (
        project_brand_trajectory,
        list_regimes_with_confidence,
    )
    from prediction.nb_residual_solver import solve_nb_residual
    from prediction.locked_ytd import project_with_locked_ytd

    nb_cpa_elast_row = params.get('nb_cpa_elasticity', {}).get('value_json') or {'a': 0.0, 'b': 0.0}
    brand_ccp = params.get('brand_ccp', {}).get('value_scalar')
    nb_ccp = params.get('nb_ccp', {}).get('value_scalar')
    bounds = params.get('_spend_bounds') or {}
    max_weekly_nb = bounds.get('max_weekly_nb_spend')

    if tp['type'] == 'year':
        # Locked-YTD path: use the canonical production flow.
        year = int(inputs.time_period.upper().lstrip('Y'))
        lyp = project_with_locked_ytd(
            market=market,
            year=year,
            target_mode=inputs.target_mode,
            target_value=inputs.target_value,
            nb_cpa_elast=nb_cpa_elast_row,
            brand_ccp=brand_ccp,
            nb_ccp=nb_ccp,
            min_weekly_nb_spend=0.0,  # deprecated for v1.1 ieccp path; solver uses target-relational bounds
            max_weekly_nb_spend=max_weekly_nb,
            regime_multiplier=1.0,
        )
        out.warnings.extend(lyp.warnings)
        weeks = []  # per-week WeeklyOutput list shipped in Phase 6.1.7 JS-parity work
        totals = {
            'brand_regs': lyp.total_brand_regs,
            'nb_regs': lyp.total_nb_regs,
            'total_regs': lyp.total_regs,
            'brand_spend': lyp.total_brand_spend,
            'nb_spend': lyp.total_nb_spend,
            'total_spend': lyp.total_spend,
            'brand_clicks': 0.0,
            'nb_clicks': 0.0,
            'blended_cpa': lyp.blended_cpa,
            'ieccp': lyp.computed_ieccp,
            'yoy_growth_applied': {'brand': 0.0, 'nb': 0.0},
        }
        solved_spend = lyp.total_spend
        infeas = None
        out.contribution_breakdown = lyp.contribution_breakdown
        out.locked_ytd_summary = {
            'year': lyp.year,
            'n_weeks_locked': lyp.ytd.n_weeks_locked,
            'latest_week_locked': lyp.ytd.latest_week_locked.isoformat() if lyp.ytd.latest_week_locked else None,
            'ytd_brand_regs': lyp.ytd.brand_regs,
            'ytd_brand_spend': lyp.ytd.brand_spend,
            'ytd_nb_regs': lyp.ytd.nb_regs,
            'ytd_nb_spend': lyp.ytd.nb_spend,
            'roy_brand_regs': lyp.roy_brand_regs,
            'roy_brand_spend': lyp.roy_brand_spend,
            'roy_nb_regs': lyp.roy_nb_regs,
            'roy_nb_spend': lyp.roy_nb_spend,
            'constraint_active': lyp.locked_ytd_constraint_active,
        }
    else:
        # Sub-year period (W / M / Q / MY*): no Locked-YTD, just Brand + NB
        # for the target weeks.
        from datetime import date as _date, timedelta as _td
        # Build target weeks as Monday dates for current year + week numbers in tp.
        year = datetime.now().year
        if tp.get('type') == 'multi_year':
            # Multi-year: project n_years × 52 weeks forward from now.
            n_years = int(tp.get('n_years', 1))
            start = _date(year, 1, 4)
            target_weeks = [start - _td(days=start.weekday()) + _td(weeks=i) for i in range(52 * n_years)]
        else:
            jan4 = _date(year, 1, 4)
            week1_monday = jan4 - _td(days=jan4.weekday())
            target_weeks = [week1_monday + _td(weeks=w - 1) for w in tp['weeks']]

        brand_proj = project_brand_trajectory(
            market, target_weeks, regime_multiplier=1.0,
        )
        nb_sol = solve_nb_residual(
            brand_spend=brand_proj.total_spend,
            brand_regs=brand_proj.total_regs,
            target_mode=inputs.target_mode,
            target_value=inputs.target_value,
            nb_cpa_elast=nb_cpa_elast_row,
            brand_ccp=brand_ccp,
            nb_ccp=nb_ccp,
            min_nb_spend=0.0,
            max_nb_spend=(max_weekly_nb * len(target_weeks)) if max_weekly_nb else None,
            ytd_nb_spend=0.0,
            n_weeks=len(target_weeks),
        )
        out.warnings.extend(brand_proj.warnings)
        out.warnings.extend(nb_sol.warnings)
        weeks = []
        totals = {
            'brand_regs': brand_proj.total_regs,
            'nb_regs': nb_sol.nb_regs,
            'total_regs': brand_proj.total_regs + nb_sol.nb_regs,
            'brand_spend': brand_proj.total_spend,
            'nb_spend': nb_sol.nb_spend,
            'total_spend': brand_proj.total_spend + nb_sol.nb_spend,
            'brand_clicks': 0.0,
            'nb_clicks': 0.0,
            'blended_cpa': (brand_proj.total_spend + nb_sol.nb_spend) / max(brand_proj.total_regs + nb_sol.nb_regs, 1),
            'ieccp': nb_sol.computed_ieccp,
            'yoy_growth_applied': {'brand': 0.0, 'nb': 0.0},
        }
        solved_spend = totals['total_spend']
        infeas = None
        out.contribution_breakdown = brand_proj.contribution

    # Attach regime stack for downstream UI / audit.
    try:
        out.regime_stack = list_regimes_with_confidence(market)
    except Exception as e:
        out.warnings.append(f"REGIME_STACK_UNAVAILABLE: {type(e).__name__}: {e}")

    if infeas:
        out.outcome = 'INFEASIBLE'
        out.infeasibility_reason = infeas
        out.warnings.append(f"INFEASIBLE: binding_constraint={infeas['binding_constraint']}")
        return out

    # Extrapolation check (R2.13 / R9.2)
    try:
        con = _db()
        hist_max_row = con.execute("""
            SELECT MAX(cost) FROM ps.v_weekly WHERE market = ? AND period_type = 'weekly'
        """, [market]).fetchone()
        hist_max_weekly = float(hist_max_row[0] or 0)
        if hist_max_weekly > 0:
            avg_weekly_proposed = totals['total_spend'] / max(len(weeks), 1)
            if avg_weekly_proposed > HISTORICAL_EXTRAPOLATION_MULTIPLIER * hist_max_weekly:
                out.warnings.append(
                    f"HIGH_EXTRAPOLATION: avg weekly spend ${avg_weekly_proposed:,.0f} > "
                    f"{HISTORICAL_EXTRAPOLATION_MULTIPLIER}× historical max ${hist_max_weekly:,.0f}"
                )
    except Exception:
        pass

    # Regional-fallback / DATA_LIMITED check
    fallback_levels = {name: p.get('fallback_level') for name, p in params.items()}
    if any(fl in ('regional_fallback', 'southern_hemisphere_hybrid') for fl in fallback_levels.values()):
        out.warnings.append('DATA_LIMITED')
        fb_params = [n for n, fl in fallback_levels.items() if fl in ('regional_fallback', 'southern_hemisphere_hybrid')]
        out.warnings.append(f"REGIONAL_FALLBACK: {fb_params}")
        out.fallback_level_summary = 'some_regional_fallback'
    if all(fl in ('regional_fallback', 'southern_hemisphere_hybrid') for fl in fallback_levels.values() if fl is not None):
        out.fallback_level_summary = 'all_regional_fallback'

    out.weeks = weeks
    out.totals = totals
    out.yoy_growth_applied = totals.get('yoy_growth_applied', {})
    out.parameters_used = {
        name: {
            'fallback_level': p.get('fallback_level'),
            'lineage': p.get('lineage'),
            'last_refit_at': p.get('last_refit_at').isoformat() if p.get('last_refit_at') else None,
        }
        for name, p in params.items()
    }

    # Monte Carlo credible intervals (R12) + VERY_WIDE_CI check (R11.8)
    try:
        ci_dict, ci_warnings = _compute_credible_intervals(
            solved_spend=totals['total_spend'],
            inputs=inputs,
            params=params,
            tp=tp,
        )
        out.credible_intervals = ci_dict
        out.warnings.extend(ci_warnings)
    except Exception as e:
        # Never let MC failure block the projection
        out.warnings.append(f"UNCERTAINTY_UNAVAILABLE: {type(e).__name__}: {e}")

    return out


# ---------- Credible interval integration (R11.8 + R12) ----------

def _build_parameter_set(params: dict) -> dict:
    """Translate fitted `params` dict into uncertainty-module `parameter_set`.

    Each entry becomes one of four spec shapes (see mpe_uncertainty.run_monte_carlo):
    - log_linear: CPA/CPC elasticities with {a, b, posterior_cov}
    - seasonality: 52-week {weights, posteriors}
    - scalar: YoY growth {mean, std}
    - fixed: CCPs and other un-sampled scalars
    Missing or malformed params degrade gracefully to wide/flat defaults so
    the MC run completes without crashing.
    """
    out: dict = {}

    def _elast_spec(p_row: dict | None) -> dict:
        vj = (p_row or {}).get('value_json') or {}
        a = float(vj.get('a', 0.0) or 0.0)
        b = float(vj.get('b', 0.0) or 0.0)
        cov = vj.get('posterior_cov') or [[0.01, 0.0], [0.0, 0.01]]
        # Guard against malformed cov
        if not (isinstance(cov, list) and len(cov) == 2 and all(len(r) == 2 for r in cov)):
            cov = [[0.01, 0.0], [0.0, 0.01]]
        return {'type': 'log_linear', 'a': a, 'b': b, 'posterior_cov': cov}

    def _seas_spec(p_row: dict | None) -> dict:
        vj = (p_row or {}).get('value_json') or {}
        weights = vj.get('weights') or [1.0] * 52
        posteriors = vj.get('posteriors') or [{'mean': w, 'std': max(abs(w) * 0.10, 0.05)} for w in weights]
        return {'type': 'seasonality', 'weights': weights, 'posteriors': posteriors}

    def _yoy_spec(p_row: dict | None) -> dict:
        vj = (p_row or {}).get('value_json') or {}
        mean = float(vj.get('mean', 0.0) or 0.0)
        std = float(vj.get('std', 0.10) or 0.10)
        return {'type': 'scalar', 'mean': mean, 'std': std}

    out['brand_cpa_elasticity'] = _elast_spec(params.get('brand_cpa_elasticity'))
    out['nb_cpa_elasticity'] = _elast_spec(params.get('nb_cpa_elasticity'))
    out['brand_cpc_elasticity'] = _elast_spec(params.get('brand_cpc_elasticity'))
    out['nb_cpc_elasticity'] = _elast_spec(params.get('nb_cpc_elasticity'))
    out['brand_seasonality_shape'] = _seas_spec(params.get('brand_seasonality_shape'))
    out['nb_seasonality_shape'] = _seas_spec(params.get('nb_seasonality_shape'))
    out['brand_yoy_growth'] = _yoy_spec(params.get('brand_yoy_growth'))
    out['nb_yoy_growth'] = _yoy_spec(params.get('nb_yoy_growth'))

    # Fixed passthroughs — used by the projection function but not sampled
    brand_ccp = (params.get('brand_ccp') or {}).get('value_scalar')
    nb_ccp = (params.get('nb_ccp') or {}).get('value_scalar')
    out['brand_ccp'] = {'type': 'fixed', 'value': brand_ccp}
    out['nb_ccp'] = {'type': 'fixed', 'value': nb_ccp}

    share_param = (params.get('brand_spend_share') or {}).get('value_json') or {}
    out['brand_spend_share'] = {'type': 'fixed', 'value': float(share_param.get('brand_share', 0.20))}

    return out


def _mc_project_point(
    sample_params: dict,
    solved_spend: float,
    inputs: ProjectionInputs,
    tp: dict,
) -> dict:
    """One Monte Carlo sample: project the full period with sampled parameters.

    Returns the aggregate KPIs we care about for CI computation:
    total_regs, total_spend, blended_cpa, ieccp, brand_regs, nb_regs.
    """
    brand_cpa_e = sample_params['brand_cpa_elasticity']
    nb_cpa_e = sample_params['nb_cpa_elasticity']
    brand_cpc_e = sample_params['brand_cpc_elasticity']
    nb_cpc_e = sample_params['nb_cpc_elasticity']
    brand_weights = sample_params['brand_seasonality_shape']
    nb_weights = sample_params['nb_seasonality_shape']
    brand_yoy_mean = float(sample_params['brand_yoy_growth'])
    nb_yoy_mean = float(sample_params['nb_yoy_growth'])
    brand_ccp = sample_params.get('brand_ccp')
    nb_ccp = sample_params.get('nb_ccp')
    brand_share = float(sample_params.get('brand_spend_share', 0.20) or 0.20)
    nb_share = 1.0 - brand_share

    # YoY adjustment
    yoy_multiplier = 1.0
    if tp.get('type') == 'multi_year':
        n_years = int(tp.get('n_years', 1))
        brand_growth = (1.0 + brand_yoy_mean) ** n_years
        nb_growth = (1.0 + nb_yoy_mean) ** n_years
        yoy_multiplier = brand_share * brand_growth + nb_share * nb_growth

    total_brand_regs = 0.0
    total_nb_regs = 0.0
    total_brand_spend = 0.0
    total_nb_spend = 0.0
    n_weeks = max(len(tp.get('weeks', [])), 1)
    period_factor = 1.0 / n_weeks

    for wk_num in tp.get('weeks', []):
        idx = (wk_num - 1) % 52
        brand_wt = brand_weights[idx] if idx < len(brand_weights) else 1.0
        nb_wt = nb_weights[idx] if idx < len(nb_weights) else 1.0
        week_brand_spend = (
            solved_spend * brand_share * brand_wt * period_factor
            * (1 + inputs.brand_uplift_pct / 100.0) * yoy_multiplier
        )
        week_nb_spend = (
            solved_spend * nb_share * nb_wt * period_factor
            * (1 + inputs.nb_uplift_pct / 100.0) * yoy_multiplier
        )
        brand_cpa = _apply_cpa_elasticity(week_brand_spend, brand_cpa_e['a'], brand_cpa_e['b'])
        nb_cpa = _apply_cpa_elasticity(week_nb_spend, nb_cpa_e['a'], nb_cpa_e['b'])
        total_brand_regs += week_brand_spend / brand_cpa if brand_cpa > 0 else 0.0
        total_nb_regs += week_nb_spend / nb_cpa if nb_cpa > 0 else 0.0
        total_brand_spend += week_brand_spend
        total_nb_spend += week_nb_spend

    total_regs = total_brand_regs + total_nb_regs
    total_spend = total_brand_spend + total_nb_spend
    blended_cpa = total_spend / total_regs if total_regs > 0 else 0.0

    ieccp = 0.0
    if brand_ccp is not None and nb_ccp is not None and total_regs > 0:
        denom = total_brand_regs * brand_ccp + total_nb_regs * nb_ccp
        ieccp = (total_spend / denom * 100.0) if denom > 0 else 0.0

    return {
        'total_regs': total_regs,
        'total_spend': total_spend,
        'blended_cpa': blended_cpa,
        'ieccp': ieccp,
        'brand_regs': total_brand_regs,
        'nb_regs': total_nb_regs,
    }


def _compute_credible_intervals(
    solved_spend: float,
    inputs: ProjectionInputs,
    params: dict,
    tp: dict,
) -> tuple[dict, list[str]]:
    """Run Monte Carlo and return (ci_dict, ci_warnings).

    ci_dict: {metric: CredibleInterval.to_json()} for JSON-safe output.
    ci_warnings: list of warnings to append to ProjectionOutputs.warnings.
      - VERY_WIDE_CI fires on MY2 when total_regs 90% CI width > 3× central (R11.8)
      - HIGH_UNCERTAINTY is already flagged at the per-metric level in compute_ci
    """
    from prediction.mpe_uncertainty import run_monte_carlo, SAMPLES_CLI

    parameter_set = _build_parameter_set(params)

    def point_fn(sp: dict) -> dict:
        return _mc_project_point(sp, solved_spend, inputs, tp)

    ci_raw = run_monte_carlo(
        point_projection_fn=point_fn,
        parameter_set=parameter_set,
        n_samples=SAMPLES_CLI,
    )

    ci_dict = {metric: ci.to_json() for metric, ci in ci_raw.items()}
    warnings: list[str] = []

    # R11.8: VERY_WIDE_CI for MY2 projections
    is_my2 = (tp.get('type') == 'multi_year' and int(tp.get('n_years', 1)) == 2)
    if is_my2 and 'total_regs' in ci_raw:
        regs_ci = ci_raw['total_regs']
        central = abs(regs_ci.central)
        ci_90_width = regs_ci.ci_90[1] - regs_ci.ci_90[0]
        if central > 1e-6 and ci_90_width > VERY_WIDE_CI_RATIO * central:
            warnings.append(
                f"VERY_WIDE_CI: 2-year 90% CI width ({ci_90_width:,.0f}) exceeds "
                f"{VERY_WIDE_CI_RATIO:g}× central ({central:,.0f}). "
                f"RECOMMENDATION: use single-year projection only — 2-year uncertainty "
                f"is too wide to be decision-useful for this market."
            )

    return ci_dict, warnings


# ---------- Regional projection ----------

def _project_region(
    inputs: ProjectionInputs,
    tp: dict,
    out: ProjectionOutputs,
) -> ProjectionOutputs:
    """Project a region by summing per-market projections (R6.1-R6.6).

    Regional semantics (2026-04-25 clarification per Richard):
    regions are ROLLUPS of constituent markets, not drivers. Each
    constituent projects at its OWN committed target
    (ps.market_projection_params_current.ieccp_target), and the regional
    ie%CCP is computed post-hoc via sum-then-divide per R6.2.

    Target modes at region level:
      - ieccp: REJECTED (use per-market targets; regional ie%CCP is
        a rollup observation, not a driver). Returns INVALID_INPUT.
      - regs: not yet supported at region level; use per-market targets.
        Returns INVALID_INPUT for now.
      - spend: naive per-market equal split as a stopgap — constituents
        each get total/n spend. This is a "what if we allocated X total
        spend evenly" exploration mode, not a committed-target rollup.
      - op2_efficient: same as spend for now, with per-market OP2 budgets.
      - rollup (new Phase 6.2.x): DEFAULT for regions — each constituent
        runs at its own committed ieccp_target, results summed. NO
        target value needed; the regional number is a rollup observation.
    """
    region = inputs.scope
    constituents = REGION_CONSTITUENTS[region]

    # Reject region+ieccp combination — it's incorrect shape (no such
    # thing as a regional ie%CCP target). Return INVALID_INPUT with
    # the recommended alternative.
    if inputs.target_mode == 'ieccp':
        out.outcome = 'INVALID_INPUT'
        out.warnings.append(
            f"REGIONAL_IECCP_NOT_A_DRIVER: regions aggregate per-market projections; "
            f"ie%CCP for a region is a ROLLUP observation from constituents' committed "
            f"targets, not a solver input. Use target_mode='rollup' (constituents run "
            f"at their own ieccp_target rows) OR project each constituent market "
            f"separately. Constituents of {region}: {constituents}"
        )
        return out

    if inputs.target_mode == 'regs':
        out.outcome = 'INVALID_INPUT'
        out.warnings.append(
            f"REGIONAL_REGS_NOT_SUPPORTED: regional regs-target would require "
            f"cross-market allocation optimization (Phase 6.5 scope). Use "
            f"target_mode='rollup' or run each constituent market separately."
        )
        return out

    per_market_outputs: list[ProjectionOutputs] = []
    any_fallback = False
    all_fallback = True

    # Build constituent inputs based on region target mode.
    # ROLLUP mode: each constituent runs at its own committed ieccp_target.
    # SPEND mode: naive equal split (exploration mode).
    # OP2_EFFICIENT: each constituent at its own OP2 budget (not yet wired).
    for mkt in constituents:
        if inputs.target_mode == 'rollup':
            # Pull the constituent's committed ieccp_target from registry.
            # Fall back to 'spend' at a neutral value if none is set (rare).
            mkt_params = load_parameters(mkt)
            mkt_target_row = mkt_params.get('ieccp_target', {})
            mkt_target_value = mkt_target_row.get('value_scalar')
            if mkt_target_value is not None:
                mkt_mode = 'ieccp'
                mkt_value = float(mkt_target_value)
            else:
                # No committed ie%CCP target (e.g. AU null CCPs, JP uses range).
                # Fall back to a neutral projection: use last-4-week avg spend × 52.
                # This keeps the rollup meaningful without forcing a target.
                try:
                    con = _db()
                    last4 = con.execute("""
                        SELECT AVG(cost) FROM ps.v_weekly
                        WHERE market = ? AND period_type = 'weekly'
                        ORDER BY period_start DESC LIMIT 4
                    """, [mkt]).fetchone()
                    mkt_mode = 'spend'
                    mkt_value = float(last4[0] or 0) * len(tp.get('weeks', [52]))
                    if mkt_value <= 0:
                        mkt_value = 100_000  # defensive floor
                except Exception:
                    mkt_mode = 'spend'
                    mkt_value = 100_000
                out.warnings.append(
                    f"ROLLUP_FALLBACK: {mkt} has no committed ieccp_target; "
                    f"projecting at last-4w spend run-rate ${mkt_value:,.0f}"
                )
        else:
            # Legacy spend-mode naive split — exploration mode.
            mkt_mode = 'spend'
            mkt_value = inputs.target_value / len(constituents)

        mkt_inputs = ProjectionInputs(
            scope=mkt,
            time_period=inputs.time_period,
            target_mode=mkt_mode,
            target_value=mkt_value,
            brand_uplift_pct=inputs.brand_uplift_pct,
            nb_uplift_pct=inputs.nb_uplift_pct,
            regional_target_mode=inputs.regional_target_mode,
        )
        mkt_out = project(mkt_inputs)
        per_market_outputs.append(mkt_out)

        if mkt_out.fallback_level_summary != 'all_market_specific':
            any_fallback = True
        if mkt_out.fallback_level_summary != 'all_regional_fallback':
            all_fallback = False

    # Sum per-market totals (R6.1)
    total_brand_regs = sum(m.totals.get('brand_regs', 0) for m in per_market_outputs)
    total_nb_regs = sum(m.totals.get('nb_regs', 0) for m in per_market_outputs)
    total_brand_spend = sum(m.totals.get('brand_spend', 0) for m in per_market_outputs)
    total_nb_spend = sum(m.totals.get('nb_spend', 0) for m in per_market_outputs)
    total_regs = total_brand_regs + total_nb_regs
    total_spend = total_brand_spend + total_nb_spend

    # Regional ie%CCP = sum_spend / sum(regs × CCP) (R6.2) — never average CCPs (R6.3)
    ieccp_numerator_sum = 0.0
    ieccp_denominator_sum = 0.0
    for m in per_market_outputs:
        mkt_params = load_parameters(m.scope)
        brand_ccp = mkt_params.get('brand_ccp', {}).get('value_scalar')
        nb_ccp = mkt_params.get('nb_ccp', {}).get('value_scalar')
        if brand_ccp is not None and nb_ccp is not None:
            ieccp_denominator_sum += m.totals.get('brand_regs', 0) * brand_ccp
            ieccp_denominator_sum += m.totals.get('nb_regs', 0) * nb_ccp

    ieccp_total = (total_spend / ieccp_denominator_sum * 100.0) if ieccp_denominator_sum > 0 else None

    out.totals = {
        'brand_regs': total_brand_regs,
        'nb_regs': total_nb_regs,
        'total_regs': total_regs,
        'brand_spend': total_brand_spend,
        'nb_spend': total_nb_spend,
        'total_spend': total_spend,
        'blended_cpa': total_spend / total_regs if total_regs > 0 else 0.0,
        'ieccp': ieccp_total,
    }
    out.constituent_markets = [
        {
            'market': m.scope,
            'brand_regs': m.totals.get('brand_regs', 0),
            'nb_regs': m.totals.get('nb_regs', 0),
            'total_spend': m.totals.get('total_spend', 0),
            'ieccp': m.totals.get('ieccp'),
            'fallback_level_summary': m.fallback_level_summary,
            'warnings': m.warnings,
        }
        for m in per_market_outputs
    ]

    if any_fallback and not all_fallback:
        out.fallback_level_summary = 'some_regional_fallback'
    elif all_fallback:
        out.fallback_level_summary = 'all_regional_fallback'

    # Aggregate warnings (unique)
    unique_warnings = set()
    for m in per_market_outputs:
        for w in m.warnings:
            unique_warnings.add(w)
    out.warnings = sorted(unique_warnings)

    return out


# ---------- CLI ----------

def main(argv: list[str] | None = None) -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(
        prog="mpe_engine",
        description="Run a single MPE projection and emit JSON or markdown.",
    )
    parser.add_argument('--scope', required=True, help="Market (e.g. MX) or region (NA, EU5, WW)")
    parser.add_argument('--period', required=True, help="W15 | M04 | Q2 | Y2026 | MY1 | MY2")
    parser.add_argument('--target', required=True,
                        help="target_mode:value, e.g. 'spend:1000000', 'ieccp:75', 'regs:18000'")
    parser.add_argument('--format', choices=['json', 'markdown'], default='json')
    parser.add_argument('--brand-uplift', type=float, default=0.0)
    parser.add_argument('--nb-uplift', type=float, default=0.0)
    args = parser.parse_args(argv)

    if ':' not in args.target:
        print(f"[mpe_engine] ERROR: --target must be 'mode:value'", file=sys.stderr)
        return 2
    mode, val_str = args.target.split(':', 1)
    try:
        target_value = float(val_str)
    except ValueError:
        print(f"[mpe_engine] ERROR: invalid target value {val_str!r}", file=sys.stderr)
        return 2

    inputs = ProjectionInputs(
        scope=args.scope.upper(),
        time_period=args.period.upper(),
        target_mode=mode.lower(),
        target_value=target_value,
        brand_uplift_pct=args.brand_uplift,
        nb_uplift_pct=args.nb_uplift,
    )
    result = project(inputs)

    if args.format == 'json':
        # Convert to plain dict (asdict handles nested dataclasses)
        d = {
            'scope': result.scope,
            'time_period': result.time_period,
            'target_mode': result.target_mode,
            'target_value': result.target_value,
            'outcome': result.outcome,
            'totals': result.totals,
            'credible_intervals': result.credible_intervals,
            'constituent_markets': result.constituent_markets,
            'parameters_used': result.parameters_used,
            'fit_quality': _build_fit_quality_summary(result),
            'contribution_breakdown': result.contribution_breakdown,
            'regime_stack': result.regime_stack,
            'locked_ytd_summary': result.locked_ytd_summary,
            'warnings': result.warnings,
            'fallback_level_summary': result.fallback_level_summary,
            'yoy_growth_applied': result.yoy_growth_applied,
            'infeasibility_reason': result.infeasibility_reason,
            'methodology_version': result.methodology_version,
            'generated_at': result.generated_at,
            'weeks': [asdict(w) for w in result.weeks],
        }
        print(json.dumps(d, indent=2, default=str))
    else:
        print(f"# MPE Projection — {result.scope} {result.time_period}")
        print(f"**Target**: {result.target_mode}={result.target_value}")
        print(f"**Outcome**: {result.outcome}")
        print()
        print(f"## Totals")
        for k, v in result.totals.items():
            if isinstance(v, float):
                if 'spend' in k or 'cpa' in k:
                    print(f"- {k}: ${v:,.2f}")
                elif 'ieccp' in k:
                    print(f"- {k}: {v:.1f}%" if v is not None else f"- {k}: n/a")
                else:
                    print(f"- {k}: {v:,.0f}")
            else:
                print(f"- {k}: {v}")
        if result.credible_intervals:
            print()
            print(f"## Credible Intervals (50% / 80% / 90%)")
            display_metrics = ['total_regs', 'total_spend', 'blended_cpa', 'ieccp']
            for metric in display_metrics:
                ci = result.credible_intervals.get(metric)
                if not ci:
                    continue
                central = ci['central']
                lo50, hi50 = ci['ci']['50']
                lo80, hi80 = ci['ci']['80']
                lo90, hi90 = ci['ci']['90']
                if metric == 'total_spend' or metric == 'blended_cpa':
                    print(f"- {metric}: ${central:,.2f}")
                    print(f"    50% CI: ${lo50:,.2f} — ${hi50:,.2f}")
                    print(f"    80% CI: ${lo80:,.2f} — ${hi80:,.2f}")
                    print(f"    90% CI: ${lo90:,.2f} — ${hi90:,.2f}")
                elif metric == 'ieccp':
                    print(f"- {metric}: {central:.1f}%")
                    print(f"    50% CI: {lo50:.1f}% — {hi50:.1f}%")
                    print(f"    80% CI: {lo80:.1f}% — {hi80:.1f}%")
                    print(f"    90% CI: {lo90:.1f}% — {hi90:.1f}%")
                else:
                    print(f"- {metric}: {central:,.0f}")
                    print(f"    50% CI: {lo50:,.0f} — {hi50:,.0f}")
                    print(f"    80% CI: {lo80:,.0f} — {hi80:,.0f}")
                    print(f"    90% CI: {lo90:,.0f} — {hi90:,.0f}")
                if ci.get('warnings'):
                    print(f"    warnings: {', '.join(ci['warnings'])}")
        if result.warnings:
            print()
            print(f"## Warnings")
            for w in result.warnings:
                print(f"- {w}")
        if result.constituent_markets:
            print()
            print(f"## Per-Market Breakdown")
            for m in result.constituent_markets:
                ieccp_cell = f"{m['ieccp']:.1f}%" if m['ieccp'] is not None else 'n/a'
                total_regs = m['brand_regs'] + m['nb_regs']
                print(
                    f"- {m['market']}: regs={total_regs:,.0f}, "
                    f"spend=${m['total_spend']:,.0f}, "
                    f"ieccp={ieccp_cell}, "
                    f"fallback={m['fallback_level_summary']}"
                )

        # Fit quality section — surface r², fallback, n_weeks per key parameter
        # so the reader can see "how much should I trust this number?"
        fq = _build_fit_quality_summary(result)
        if fq and fq.get('per_parameter'):
            print()
            print(f"## Fit Quality")
            print(f"Overall trust: **{fq.get('overall_trust', 'unknown')}** ({fq.get('overall_trust_reason', '')})")
            print()
            print("| Parameter | r² | n weeks | Fit level | Half-life |")
            print("|---|---|---|---|---|")
            for p in fq['per_parameter']:
                r2_str = f"{p['r_squared']:.2f}" if p.get('r_squared') is not None else "—"
                nw_str = str(p.get('n_weeks', '—'))
                fb_str = p.get('fallback_level', 'unknown')
                hl_str = str(p.get('half_life_weeks', '—'))
                print(f"| {p['name']} | {r2_str} | {nw_str} | {fb_str} | {hl_str} |")
            if result.regime_stack:
                print()
                print("### Active Regimes")
                for r in result.regime_stack:
                    desc = (r.get('description') or '')[:60]
                    eff = r.get('effective_confidence', 0)
                    status = r.get('decay_status', '?')
                    n_post = r.get('n_post_weeks', '?')
                    print(f"- {r.get('change_date','?')} · {status} · {n_post}w post · confidence {eff:.2f} · {desc}")

    return 0 if result.outcome == 'OK' else 1


def _build_fit_quality_summary(result: 'ProjectionOutputs') -> dict:
    """Extract fit-quality metadata from parameters_used for UI surfacing.

    Output shape:
        {
            'overall_trust': 'high' | 'medium' | 'low',
            'overall_trust_reason': '...',
            'per_parameter': [
                {'name': 'nb_cpa_elasticity', 'r_squared': 0.41, 'n_weeks': 83,
                 'fallback_level': 'market_specific', 'half_life_weeks': None},
                ...
            ],
        }
    """
    params = result.parameters_used or {}
    per_param: list[dict] = []
    fits_r_squared: list[float] = []
    has_fallback = False
    # Focus on the parameters that actually drive v1.1 Slim projections.
    for name in ('nb_cpa_elasticity', 'brand_cpa_elasticity',
                 'brand_seasonality_shape', 'brand_yoy_growth'):
        if name not in params:
            continue
        p = params[name]
        # Pull value_json if it's been re-loaded; else parameters_used only holds meta.
        # This extracts from any nested shape.
        r2 = None
        n_weeks = None
        half_life = None
        # parameters_used contains {'fallback_level', 'lineage', 'last_refit_at'} — we need
        # to re-peek into market_projection_params_current if r² is missing.
        if 'r_squared' in p:
            r2 = p.get('r_squared')
            n_weeks = p.get('weeks_used')
        per_param.append({
            'name': name,
            'r_squared': r2,
            'n_weeks': n_weeks,
            'fallback_level': p.get('fallback_level', 'unknown'),
            'half_life_weeks': half_life,
            'lineage': p.get('lineage'),
        })
        if isinstance(r2, (int, float)):
            fits_r_squared.append(float(r2))
        if p.get('fallback_level') and p['fallback_level'] != 'market_specific':
            has_fallback = True

    # If we couldn't extract r² from parameters_used directly, re-fetch from DB.
    if not any(p.get('r_squared') is not None for p in per_param) and result.scope in ALL_MARKETS:
        try:
            import json as _json
            con = _db()
            rows = con.execute("""
                SELECT parameter_name, value_json, fallback_level
                FROM ps.market_projection_params_current
                WHERE market = ?
                  AND parameter_name IN ('nb_cpa_elasticity','brand_cpa_elasticity',
                                         'brand_seasonality_shape','brand_yoy_growth')
            """, [result.scope]).fetchall()
            lookup = {}
            for name, vj_raw, fb in rows:
                vj = _json.loads(vj_raw) if isinstance(vj_raw, str) else (vj_raw or {})
                lookup[name] = {
                    'r_squared': vj.get('r_squared'),
                    'n_weeks': vj.get('weeks_used'),
                    'fallback_level': fb,
                }
            for p in per_param:
                if p['name'] in lookup:
                    p['r_squared'] = lookup[p['name']].get('r_squared')
                    p['n_weeks'] = lookup[p['name']].get('n_weeks')
                    if p.get('fallback_level') == 'unknown':
                        p['fallback_level'] = lookup[p['name']].get('fallback_level', 'unknown')
                    if isinstance(p['r_squared'], (int, float)):
                        fits_r_squared.append(float(p['r_squared']))
                    if p['fallback_level'] and p['fallback_level'] != 'market_specific':
                        has_fallback = True
        except Exception:
            pass  # best-effort — never block the projection on fit-quality lookup

    # Classify overall trust.
    if not fits_r_squared:
        trust = 'unknown'
        reason = 'no fit quality metadata available'
    else:
        mean_r2 = sum(fits_r_squared) / len(fits_r_squared)
        if mean_r2 >= 0.45 and not has_fallback:
            trust = 'high'
            reason = f"mean r²={mean_r2:.2f} · all market-specific fits"
        elif mean_r2 >= 0.30:
            trust = 'medium'
            reason = f"mean r²={mean_r2:.2f} · {'fallback in use' if has_fallback else 'borderline r²'}"
        else:
            trust = 'low'
            reason = f"mean r²={mean_r2:.2f} · {'fallback in use' if has_fallback else 'flat-spend artifact'}"

    return {
        'overall_trust': trust,
        'overall_trust_reason': reason,
        'per_parameter': per_param,
    }


if __name__ == "__main__":
    sys.exit(main())
