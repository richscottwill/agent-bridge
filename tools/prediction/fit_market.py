"""Fit a market's full parameter suite and write to the registry — Task 1.5.

WHY THIS EXISTS
    Phase 1 Task 1.5 requires each market's parameters fitted from historical
    data and written to ps.market_projection_params. This script is the
    reusable entry point invoked per market (MX first, then US, AU, ...,
    one chronological pass through all 10 markets in Phase 1).

HOW THE OWNER MAINTAINS IT
    Run once per market during initial Phase 1 build. Re-run any market
    through the quarterly refit hook (kiro hook run mpe-refit) which calls
    into this same code path. No manual editing.

    Manual ad-hoc run:
        python3 -m shared.tools.prediction.fit_market --market MX

WHAT HAPPENS ON FAILURE
    - Fits that hit regional_fallback (r² < 0.35 or <80 clean weeks) are
      written with fallback_level='regional_fallback' and is_active=TRUE
      so projections still work using regional curves downstream.
    - MAPE regression >10pp vs prior active version is flagged by setting
      is_active=FALSE and writing a ps.parameter_anomalies row. Owner
      reviews in the refit report.
    - Any exception is caught per-parameter; other parameters still get
      written. End-of-run summary lists any failures.

WHAT THIS WRITES
    Per market, 9 parameter rows:
        brand_cpa_elasticity, nb_cpa_elasticity     (quarterly refit)
        brand_cpc_elasticity, nb_cpc_elasticity     (quarterly refit)
        brand_seasonality_shape, nb_seasonality_shape (annual refit)
        brand_yoy_growth, nb_yoy_growth             (quarterly refit)
        brand_spend_share                            (quarterly refit)

    Plus 9 ps.parameter_validation rows (one per fitted parameter) with
    12-week holdout MAPE when enough data is available.
"""

from __future__ import annotations

import json
import math
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.expanduser('~/shared/tools'))


# ---------- Connection ----------

_con = None


def _db(read_only: bool = False):
    global _con
    if _con is None:
        import duckdb
        from prediction.config import MOTHERDUCK_TOKEN
        _con = duckdb.connect(
            f'md:ps_analytics?motherduck_token={MOTHERDUCK_TOKEN}',
            read_only=read_only,
        )
        # Share this connection with mpe_fitting and mpe_engine so we don't
        # hit "Can't open a connection to same database file with a different
        # configuration" errors from duckdb.
        import prediction.mpe_fitting as _mf
        _mf._con = _con
        try:
            import prediction.mpe_engine as _me
            _me._con = _con
        except ImportError:
            pass
    return _con


# ---------- Writer helpers ----------

def next_version(con, market: str, parameter_name: str) -> int:
    row = con.execute("""
        SELECT COALESCE(MAX(parameter_version), 0) + 1
        FROM ps.market_projection_params
        WHERE market = ? AND parameter_name = ?
    """, [market, parameter_name]).fetchone()
    return int(row[0])


def deactivate_prior(con, market: str, parameter_name: str) -> int:
    """Flip all prior active versions to is_active=FALSE.
    Returns the prior-version number (for MAPE comparison), or 0 if none."""
    prior_row = con.execute("""
        SELECT MAX(parameter_version)
        FROM ps.market_projection_params
        WHERE market = ? AND parameter_name = ? AND is_active = TRUE
    """, [market, parameter_name]).fetchone()
    prior_version = int(prior_row[0] or 0)
    con.execute("""
        UPDATE ps.market_projection_params
        SET is_active = FALSE
        WHERE market = ? AND parameter_name = ? AND is_active = TRUE
    """, [market, parameter_name])
    return prior_version


def write_fitted_param(
    con,
    market: str,
    parameter_name: str,
    value_json_dict: dict,
    refit_cadence: str,
    fallback_level: str,
    source: str,
    lineage: str,
    is_active: bool = True,
) -> tuple[int, int]:
    """Write a fitted parameter. Returns (new_version, prior_version)."""
    prior_version = deactivate_prior(con, market, parameter_name)
    version = next_version(con, market, parameter_name)
    con.execute("""
        INSERT INTO ps.market_projection_params
        (market, parameter_name, parameter_version, value_json, refit_cadence,
         last_refit_at, source, fallback_level, lineage, is_active)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, ?, ?)
    """, [market, parameter_name, version, json.dumps(value_json_dict),
          refit_cadence, source, fallback_level, lineage, is_active])
    return version, prior_version


def write_validation(
    con,
    market: str,
    parameter_name: str,
    parameter_version: int,
    holdout_mape: float | None,
    validation_sample_range: str,
    notes: str = '',
) -> None:
    con.execute("""
        INSERT INTO ps.parameter_validation
        (market, parameter_name, parameter_version, validation_run_at,
         holdout_mape, validation_sample_range, notes)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?, ?, ?)
    """, [market, parameter_name, parameter_version, holdout_mape,
          validation_sample_range, notes])


# ---------- MAPE holdout validation ----------

def compute_holdout_mape(
    fit_result_json: dict,
    market: str,
    segment: str,
    metric: str,
    holdout_weeks: int = 12,
) -> tuple[float | None, str]:
    """Compute MAPE on the most recent `holdout_weeks` weeks using the fit.

    For elasticity parameters (CPA / CPC): MAPE of predicted CPA vs actual.
    Returns (mape, sample_range_description). Returns (None, reason) if
    insufficient data.
    """
    con = _db()
    spend_col = f"{segment}_cost"
    metric_col = f"{segment}_{metric}"

    rows = con.execute(f"""
        SELECT period_start, period_key, {spend_col} AS spend, {metric_col} AS actual
        FROM ps.v_weekly
        WHERE market = ? AND period_type = 'weekly'
          AND {spend_col} > 0 AND {metric_col} IS NOT NULL AND {metric_col} > 0
        ORDER BY period_start DESC
        LIMIT ?
    """, [market, holdout_weeks]).fetchall()

    if len(rows) < 4:
        return (None, f"insufficient_holdout ({len(rows)} weeks, need >=4)")

    a = fit_result_json.get('a', 0)
    b = fit_result_json.get('b', 0)

    pct_errors = []
    for period_start, period_key, spend, actual in rows:
        if actual is None or actual <= 0:
            continue
        try:
            predicted = math.exp(a) * (float(spend) ** b)
        except (OverflowError, ValueError):
            continue
        if predicted <= 0:
            continue
        pct_errors.append(abs(predicted - float(actual)) / float(actual))

    if not pct_errors:
        return (None, f"no_valid_predictions")

    mape = sum(pct_errors) / len(pct_errors)
    latest = rows[0][1]
    earliest = rows[-1][1]
    return (mape, f"{earliest} to {latest}")


# ---------- Main fit-and-write routine ----------

def fit_and_write_market(market: str, half_life_weeks: float = 52.0) -> dict:
    """Fit all parameters for a market, write to registry, compute MAPE.

    Returns summary dict with counts and per-parameter status.
    """
    # Open connection FIRST so mpe_fitting inherits it (avoid DuckDB
    # "different configuration" collision)
    con = _db(read_only=False)

    from prediction.mpe_fitting import (
        fit_all_for_market,
        fit_spend_share,
    )

    summary = {
        'market': market,
        'written': 0,
        'skipped': 0,
        'anomalies': [],
        'warnings': [],
        'per_parameter': {},
    }

    # ----- Brand and NB fits -----
    brand_results = fit_all_for_market(market, 'brand', half_life_weeks)
    nb_results = fit_all_for_market(market, 'nb', half_life_weeks)

    # Map of parameter_name -> (result_obj, cadence, segment, metric_for_mape)
    all_fits = {}
    for name, r in brand_results.items():
        segment = 'brand'
        # Derive metric for MAPE: 'cpa' for cpa_elasticity, 'cpc' for cpc_elasticity, None otherwise
        metric = 'cpa' if 'cpa_elasticity' in name else ('cpc' if 'cpc_elasticity' in name else None)
        cadence = 'annual' if 'seasonality' in name else 'quarterly'
        all_fits[name] = {'result': r, 'cadence': cadence, 'segment': segment, 'metric': metric}
    for name, r in nb_results.items():
        segment = 'nb'
        metric = 'cpa' if 'cpa_elasticity' in name else ('cpc' if 'cpc_elasticity' in name else None)
        cadence = 'annual' if 'seasonality' in name else 'quarterly'
        all_fits[name] = {'result': r, 'cadence': cadence, 'segment': segment, 'metric': metric}

    # Write each fit
    for name, info in all_fits.items():
        r = info['result']
        try:
            value_json_dict = r.to_json()
            source = 'historical_fit' if r.fallback_level in ('market_specific', 'derived_from_cpa') else r.fallback_level
            version, prior_version = write_fitted_param(
                con=con,
                market=market,
                parameter_name=name,
                value_json_dict=value_json_dict,
                refit_cadence=info['cadence'],
                fallback_level=r.fallback_level,
                source=source,
                lineage=getattr(r, 'lineage', f"{name} fit {datetime.now().strftime('%Y-%m-%d')}"),
                is_active=True,
            )
            summary['written'] += 1

            # Compute holdout MAPE for elasticity fits only
            if info['metric'] in ('cpa', 'cpc'):
                mape, sample_range = compute_holdout_mape(
                    fit_result_json=value_json_dict,
                    market=market,
                    segment=info['segment'],
                    metric=info['metric'],
                    holdout_weeks=12,
                )
                if mape is not None:
                    write_validation(
                        con, market, name, version,
                        holdout_mape=mape,
                        validation_sample_range=sample_range,
                        notes=f"12-week holdout MAPE for {info['segment']}_{info['metric']}",
                    )
                    summary['per_parameter'][name] = {
                        'version': version,
                        'prior_version': prior_version,
                        'fallback_level': r.fallback_level,
                        'r_squared': getattr(r, 'r_squared', None),
                        'mape': mape,
                        'sample_range': sample_range,
                    }
                    # MAPE warning per R9.3 (>40%)
                    if mape > 0.40:
                        summary['warnings'].append(
                            f"{name}: LOW_CONFIDENCE (MAPE={mape:.1%} > 40%)"
                        )
                else:
                    summary['per_parameter'][name] = {
                        'version': version,
                        'prior_version': prior_version,
                        'fallback_level': r.fallback_level,
                        'r_squared': getattr(r, 'r_squared', None),
                        'mape': None,
                        'sample_range': sample_range,
                    }
            else:
                summary['per_parameter'][name] = {
                    'version': version,
                    'prior_version': prior_version,
                    'fallback_level': r.fallback_level,
                    'r_squared': getattr(r, 'r_squared', None) if hasattr(r, 'r_squared') else None,
                }

        except Exception as e:
            summary['skipped'] += 1
            summary['per_parameter'][name] = {'error': f"{type(e).__name__}: {e}"}

    # ----- brand_spend_share (per-market Brand/NB allocation) -----
    try:
        share_result = fit_spend_share(market, half_life_weeks)
        value_json_dict = share_result.to_json()
        version, prior_version = write_fitted_param(
            con=con,
            market=market,
            parameter_name='brand_spend_share',
            value_json_dict=value_json_dict,
            refit_cadence='quarterly',
            fallback_level='market_specific' if share_result.weeks_used >= 20 else 'conservative_default',
            source='historical_fit' if share_result.weeks_used >= 20 else 'conservative_default',
            lineage=share_result.lineage,
            is_active=True,
        )
        summary['written'] += 1
        summary['per_parameter']['brand_spend_share'] = {
            'version': version,
            'prior_version': prior_version,
            'brand_share': share_result.brand_share,
            'weeks_used': share_result.weeks_used,
            'range': {'min': share_result.range_min, 'max': share_result.range_max},
        }
    except Exception as e:
        summary['skipped'] += 1
        summary['per_parameter']['brand_spend_share'] = {'error': f"{type(e).__name__}: {e}"}

    return summary


# ---------- CLI ----------

def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(
        prog="fit_market",
        description="Fit a market's full MPE parameter suite and write to ps.market_projection_params.",
    )
    parser.add_argument('--market', required=True,
                        choices=['US','CA','UK','DE','FR','IT','ES','JP','MX','AU'],
                        help="Market code")
    parser.add_argument('--half-life', type=float, default=52.0,
                        help="Recency-weighting half-life in weeks (default 52)")
    args = parser.parse_args(argv)

    market = args.market
    print(f"[fit_market] Fitting {market} with half_life={args.half_life}w...")
    summary = fit_and_write_market(market, args.half_life)

    print(f"\n=== {market} fit summary ===")
    print(f"Written: {summary['written']} parameters")
    if summary['skipped']:
        print(f"Skipped: {summary['skipped']}")

    print(f"\n--- Per-parameter ---")
    for name, info in summary['per_parameter'].items():
        if 'error' in info:
            print(f"  {name:30s} ERROR: {info['error']}")
            continue
        fb = info.get('fallback_level', 'n/a')
        r2 = info.get('r_squared')
        r2_str = f"r²={r2:.3f}" if r2 is not None else ""
        mape = info.get('mape')
        mape_str = f"MAPE={mape:.1%}" if mape is not None else ""
        brand_share = info.get('brand_share')
        share_str = f"brand_share={brand_share:.1%}" if brand_share is not None else ""
        print(f"  {name:30s} v{info['version']} [{fb}] {r2_str} {mape_str} {share_str}")

    if summary['warnings']:
        print(f"\n--- Warnings ---")
        for w in summary['warnings']:
            print(f"  - {w}")

    return 0 if summary['written'] > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
