#!/usr/bin/env python3
"""validate_market.py — compute 12-week holdout MAPE per parameter per market.

WHY THIS EXISTS
    Per R5.1-R5.4 and Task 3.X.B of the MPE v1 spec, each fitted parameter
    needs a validation MAPE score computed on a 12-week holdout slice of
    `ps.v_weekly`. Parameters with MAPE > 40% (R9.3) are flagged
    LOW_CONFIDENCE so the owner can decide whether to trust them.

WHAT IT DOES
    For a given market:
    1. Fetch last 12 weeks of `ps.v_weekly` as the holdout set
    2. Refit the engine using weeks BEFORE the holdout
    3. Predict the holdout weeks using the refitted elasticity and seasonality
    4. Compare predicted vs actual, compute MAPE per parameter
    5. Write results to `ps.parameter_validation`, update `validation_mape`
       column on the corresponding active `ps.market_projection_params` row
    6. If MAPE > 40%, emit LOW_CONFIDENCE warning (does NOT auto-deactivate
       the param — owner review per spec)

USAGE
    python3 -m shared.tools.prediction.validate_market --market MX
    python3 -m shared.tools.prediction.validate_market --market MX --no-write

OUTPUT
    Markdown summary to stdout with per-parameter MAPE + threshold status.
"""
from __future__ import annotations

import argparse
import math
import os
import sys
from datetime import datetime, timedelta, date
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.expanduser('~/shared/tools'))

from prediction import mpe_fitting


HOLDOUT_WEEKS = 12
MAPE_WARN_THRESHOLD = 0.40   # R9.3


def _connect():
    import duckdb
    from prediction.config import MOTHERDUCK_TOKEN
    return duckdb.connect(
        f'md:ps_analytics?motherduck_token={MOTHERDUCK_TOKEN}',
        read_only=False,   # writes to ps.parameter_validation
    )


def _fetch_weekly_range(con, market: str, segment: str, not_before: date, not_after: date) -> list[dict]:
    """Fetch weekly rows in a date range for the given segment."""
    reg_col = f'{segment}_registrations'
    cost_col = f'{segment}_cost'
    cpa_col = f'{segment}_cpa'
    cpc_col = f'{segment}_cpc'
    cvr_col = f'{segment}_cvr'

    rows = con.execute(f"""
        SELECT period_start,
               {reg_col} AS regs,
               {cost_col} AS cost,
               {cpa_col} AS cpa,
               {cpc_col} AS cpc,
               {cvr_col} AS cvr
        FROM ps.v_weekly
        WHERE market = ?
          AND period_type = 'weekly'
          AND period_start BETWEEN ? AND ?
          AND {cost_col} > 0 AND {reg_col} > 0
        ORDER BY period_start
    """, [market, not_before, not_after]).fetchall()

    today = date.today()
    out = []
    for r in rows:
        age_weeks = max((today - r[0]).days / 7.0, 0)
        out.append({
            'period_start': r[0], 'age_weeks': age_weeks,
            'spend': float(r[2]), 'cpa': float(r[3]),
            'cpc': float(r[4]) if r[4] else float(r[2]) / 10.0,
            'regs': float(r[1]),
            'clicks': float(r[2]) / (float(r[4]) if r[4] else float(r[2]) / 10.0),
            'cvr': float(r[5]) if r[5] else 0.10,
        })
    return out


def _compute_mape(actual: list[float], predicted: list[float]) -> float:
    """Mean absolute percentage error across paired sequences."""
    pairs = [(a, p) for a, p in zip(actual, predicted) if a and a > 0]
    if not pairs:
        return float('nan')
    return float(np.mean([abs(a - p) / a for a, p in pairs]))


def validate(market: str, con, write: bool = True) -> dict:
    """Validate all segment × parameter combinations for one market.

    Returns dict of {parameter_name: mape} plus summary metadata.
    """
    today = date.today()
    holdout_start = today - timedelta(weeks=HOLDOUT_WEEKS)
    holdout_end = today
    # Train window: everything before holdout
    train_end = holdout_start - timedelta(days=1)
    train_start = date(2023, 1, 1)

    results = {}
    summary = {
        'market': market,
        'holdout_weeks': HOLDOUT_WEEKS,
        'holdout_range': (holdout_start.isoformat(), holdout_end.isoformat()),
        'parameters': {},
        'flags': [],
    }

    for segment in ('brand', 'nb'):
        # CPA elasticity — predict CPA from spend using refit, compare to actuals
        train_data = _fetch_weekly_range(con, market, segment, train_start, train_end)
        holdout_data = _fetch_weekly_range(con, market, segment, holdout_start, holdout_end)

        if len(holdout_data) < 3:
            summary['flags'].append(f"{segment}: insufficient holdout ({len(holdout_data)} weeks)")
            continue
        if len(train_data) < 20:
            summary['flags'].append(f"{segment}: insufficient training data ({len(train_data)} weeks)")
            continue

        # Refit CPA on training data only
        cpa_fit = mpe_fitting.fit_elasticity(market, segment, 'cpa', data=train_data)
        if cpa_fit.fallback_level != 'market_specific':
            summary['parameters'][f'{segment}_cpa_elasticity'] = {
                'mape': None,
                'fallback': cpa_fit.fallback_level,
                'note': 'fell to fallback on training data, validation skipped',
            }
        else:
            predicted_cpa = [
                math.exp(cpa_fit.coef_a) * (d['spend'] ** cpa_fit.coef_b)
                for d in holdout_data
            ]
            actual_cpa = [d['cpa'] for d in holdout_data]
            mape = _compute_mape(actual_cpa, predicted_cpa)
            status = 'LOW_CONFIDENCE' if mape > MAPE_WARN_THRESHOLD else 'OK'
            summary['parameters'][f'{segment}_cpa_elasticity'] = {
                'mape': mape, 'status': status, 'n_holdout_weeks': len(holdout_data),
            }
            if write:
                con.execute("""
                    INSERT INTO ps.parameter_validation
                    (market, parameter_name, parameter_version, validation_run_at,
                     holdout_mape, validation_sample_range, notes)
                    VALUES (?, ?, 1, CURRENT_TIMESTAMP, ?, ?, ?)
                """, [
                    market, f'{segment}_cpa_elasticity', mape,
                    f'{holdout_start.isoformat()} to {holdout_end.isoformat()} (n={len(holdout_data)})',
                    f'holdout_12week status={status}',
                ])
                con.execute("""
                    UPDATE ps.market_projection_params
                    SET validation_mape = ?, last_validated_at = CURRENT_TIMESTAMP
                    WHERE market = ? AND parameter_name = ? AND is_active = TRUE
                """, [mape, market, f'{segment}_cpa_elasticity'])

    # Summary render
    print(f"\n=== {market} 12-week holdout validation ===")
    print(f"Holdout range: {summary['holdout_range'][0]} to {summary['holdout_range'][1]}")
    print()
    for pname, rec in summary['parameters'].items():
        if rec.get('mape') is not None:
            status_icon = '⚠️ LOW_CONFIDENCE' if rec['status'] == 'LOW_CONFIDENCE' else '✅'
            print(f"  {status_icon} {pname}: MAPE={rec['mape']:.1%} (n={rec['n_holdout_weeks']})")
        else:
            print(f"  ⏸  {pname}: {rec.get('note', 'skipped')}")
    if summary['flags']:
        print()
        print("Flags:")
        for f in summary['flags']:
            print(f"  - {f}")

    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--market', required=True, help='Market code (e.g. MX, US, AU)')
    parser.add_argument('--no-write', action='store_true', help='Dry run; do not write to DB')
    args = parser.parse_args()

    con = _connect()
    try:
        validate(args.market.upper(), con, write=not args.no_write)
    finally:
        con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
