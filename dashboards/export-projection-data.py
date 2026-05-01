#!/usr/bin/env python3
"""export-projection-data.py — Build shared/dashboards/data/projection-data.json.

WHY THIS EXISTS
    The MPE UI (projection.html, mpe_engine.js) needs fitted parameters,
    YTD actuals, seasonality shapes, YoY trends, and credible interval
    posteriors for every market and region. Instead of having the UI
    hit DuckDB directly, we snapshot everything to a single JSON file
    that the HTML loads once at page-init. This is what makes the
    "standalone-embedded" SharePoint variant work: open the HTML, see
    data, zero network calls.

WHAT IT READS
    - ps.market_projection_params_current  (fitted parameters for 10 markets)
    - ps.v_weekly                           (YTD weekly actuals, current year)
    - ps.regime_changes                     (active regime events per market)
    - ps.targets                            (OP2 / MBR targets if present)

WHAT IT WRITES
    - shared/dashboards/data/projection-data.json (target < 500 KB)
      Top-level keys:
        generated            — ISO timestamp
        methodology_version  — MPE engine version
        markets              — {MARKET: {params, ytd_weekly, regime_events, ...}}
        regions              — {NA, EU5, WW: {constituents, fallback_summary}}
        global               — {market_list, region_list, fallback_classification}

MAINTENANCE
    - Owner never runs this directly. Called via refresh-all.py + the
      mpe-refit Kiro hook.
    - If a parameter name changes in ps.market_projection_params, no
      changes here are needed — we pass through the raw value_json.
      The UI knows how to render each parameter type.

WHAT HAPPENS ON FAILURE
    - DB unreachable: script writes a "stub" JSON with fallback=True so
      the UI shows "data unavailable" banner instead of crashing
    - Partial data (e.g. AU null CCPs): preserved as nulls; UI treats
      null-CCP markets as ie%CCP-disabled
    - Oversized JSON: prints a warning at end (target <500KB)
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, date, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
OUTPUT_PATH = SCRIPT_DIR / "data" / "projection-data.json"
TARGET_SIZE_KB = 500

ALL_MARKETS = ['US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP', 'MX', 'AU']
REGIONS = {
    'NA': ['US', 'CA'],
    'EU5': ['UK', 'DE', 'FR', 'IT', 'ES'],
    'WW': ALL_MARKETS,
}


def _get_connection():
    """Return a read-only DuckDB MotherDuck connection, or None."""
    try:
        # Add shared/tools to path so prediction.config is importable
        sys.path.insert(0, os.path.expanduser('~/shared/tools'))
        import duckdb
        from prediction.config import MOTHERDUCK_TOKEN
        if not MOTHERDUCK_TOKEN:
            return None
        return duckdb.connect(
            f'md:ps_analytics?motherduck_token={MOTHERDUCK_TOKEN}',
            read_only=True,
        )
    except Exception as e:
        print(f"[export-projection-data] DB connection failed: {e}")
        return None


def _json_safe(obj):
    """Recursively convert DuckDB/datetime objects to JSON-safe values."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, float):
        # Avoid NaN/Inf in JSON
        if obj != obj or obj in (float('inf'), float('-inf')):
            return None
        return obj
    return obj


def _parse_value_json(raw):
    """ps.market_projection_params_current.value_json can be stored as str or dict."""
    if raw is None:
        return None
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return None
    return raw


def _fetch_parameters(con, market: str) -> dict:
    """Return {parameter_name: {value, fallback_level, lineage, last_refit_at, r_squared, mape}}."""
    rows = con.execute("""
        SELECT parameter_name, value_scalar, value_json, fallback_level,
               lineage, last_refit_at, validation_mape
        FROM ps.market_projection_params_current
        WHERE market = ?
    """, [market]).fetchall()

    out = {}
    for pname, vs, vj, fallback, lineage, refit_at, mape in rows:
        vj_parsed = _parse_value_json(vj)
        # Strip the heaviest fields that aren't needed client-side
        if isinstance(vj_parsed, dict):
            vj_parsed = {k: v for k, v in vj_parsed.items() if k != 'posterior_cov' or isinstance(v, list)}
        r_squared = None
        if isinstance(vj_parsed, dict) and 'r_squared' in vj_parsed:
            r_squared = vj_parsed.get('r_squared')
        out[pname] = {
            'value_scalar': vs,
            'value_json': vj_parsed,
            'fallback_level': fallback,
            'lineage': lineage,
            'last_refit_at': refit_at,
            'validation_mape': mape,
            'r_squared': r_squared,
        }
    return out


def _fetch_ytd_weekly(con, market: str, year: int) -> list[dict]:
    """YTD weekly actuals for current year — used for UI 'actuals to date' overlay.

    Schema reference: ps.v_weekly uses `registrations` (not `regs`) and includes
    brand_ / nb_ variants for each metric. We expose both total and
    brand/nb-split so chart can plot either granularity.
    """
    rows = con.execute("""
        SELECT period_start, registrations, cost, clicks, cpa, cpc, cvr,
               brand_registrations, brand_cost,
               nb_registrations, nb_cost,
               ieccp
        FROM ps.v_weekly
        WHERE market = ?
          AND period_type = 'weekly'
          AND YEAR(period_start) = ?
        ORDER BY period_start
    """, [market, year]).fetchall()
    out = []
    for r in rows:
        out.append({
            'period_start': r[0].isoformat() if r[0] else None,
            'regs': int(r[1]) if r[1] is not None else None,
            'cost': float(r[2]) if r[2] is not None else None,
            'clicks': int(r[3]) if r[3] is not None else None,
            'cpa': float(r[4]) if r[4] is not None else None,
            'cpc': float(r[5]) if r[5] is not None else None,
            'cvr': float(r[6]) if r[6] is not None else None,
            'brand_regs': int(r[7]) if r[7] is not None else None,
            'brand_cost': float(r[8]) if r[8] is not None else None,
            'nb_regs': int(r[9]) if r[9] is not None else None,
            'nb_cost': float(r[10]) if r[10] is not None else None,
            'ieccp': float(r[11]) if r[11] is not None else None,
        })
    return out


def _fetch_regime_events(con, market: str) -> list[dict]:
    """Active regime events only — inactive rows live in DB for audit but the UI doesn't need them."""
    rows = con.execute("""
        SELECT change_date, change_type, description, confidence,
               half_life_weeks, is_structural_baseline, end_date
        FROM ps.regime_changes
        WHERE market = ? AND active = TRUE
        ORDER BY change_date
    """, [market]).fetchall()
    out = []
    for r in rows:
        out.append({
            'change_date': r[0].isoformat() if r[0] else None,
            'change_type': r[1],
            'description': r[2],
            'confidence': float(r[3]) if r[3] is not None else None,
            'half_life_weeks': int(r[4]) if r[4] is not None else None,
            'is_structural_baseline': bool(r[5]),
            'end_date': r[6].isoformat() if r[6] else None,
        })
    return out


def _fetch_regime_fit_state(con, market: str) -> list[dict]:
    """Fetch the current weekly-fitted regime state per market (Phase 6.1.7
    pipe into the JS mirror).

    Returns the latest fit per active structural regime, with peak, decay,
    confidence, status + the authored data needed for UI display.
    """
    rows = con.execute("""
        SELECT
            fs.regime_id,
            CAST(rc.change_date AS DATE) AS change_date,
            rc.description,
            rc.expected_impact_pct,
            rc.half_life_weeks                   AS authored_hl,
            fs.peak_multiplier,
            fs.fitted_half_life_weeks,
            fs.current_multiplier,
            fs.decay_status,
            fs.confidence,
            fs.n_post_weeks,
            fs.fit_as_of,
            fs.fit_method
        FROM ps.regime_fit_state_current fs
        JOIN ps.regime_changes rc ON rc.id = fs.regime_id
        WHERE fs.market = ?
          AND rc.is_structural_baseline = TRUE
          AND rc.active = TRUE
        ORDER BY rc.change_date
    """, [market]).fetchall()
    out = []
    for (regime_id, change_date, description, expected_impact_pct,
         authored_hl, peak_mult, fitted_hl, current_mult, decay_status,
         confidence, n_post_weeks, fit_as_of, fit_method) in rows:
        out.append({
            'regime_id': regime_id,
            'change_date': change_date.isoformat() if change_date else None,
            'description': description,
            'expected_impact_pct': float(expected_impact_pct) if expected_impact_pct is not None else None,
            'authored_half_life_weeks': float(authored_hl) if authored_hl is not None else None,
            'peak_multiplier': float(peak_mult) if peak_mult is not None else 1.0,
            'fitted_half_life_weeks': float(fitted_hl) if fitted_hl is not None else None,
            'current_multiplier': float(current_mult) if current_mult is not None else 1.0,
            'decay_status': decay_status,
            'confidence': float(confidence) if confidence is not None else None,
            'n_post_weeks': int(n_post_weeks) if n_post_weeks is not None else None,
            'fit_as_of': fit_as_of.isoformat() if fit_as_of else None,
            'fit_method': fit_method,
        })
    return out


def _fetch_op2_targets(con, market: str, year: int) -> dict | None:
    """Fetch OP2 annual targets for the market — sum of monthly rows in
    ps.targets for the given fiscal year. Used as the default for Target
    Spend and Target Registrations in the projection UI.

    Returns None if no OP2 data is loaded for this market-year yet.
    Also returns monthly breakdown so UI can scale by selected period
    (M/Q/Y).
    """
    try:
        annual = con.execute("""
            SELECT
                SUM(CASE WHEN metric_name = 'cost'          THEN target_value END) AS cost_total,
                SUM(CASE WHEN metric_name = 'registrations' THEN target_value END) AS regs_total,
                COUNT(DISTINCT period_key)                                         AS n_months
            FROM ps.targets
            WHERE market = ?
              AND fiscal_year = ?
              AND period_type = 'monthly'
              AND metric_name IN ('cost', 'registrations')
        """, [market, year]).fetchone()
        monthly_rows = con.execute("""
            SELECT period_key,
                SUM(CASE WHEN metric_name = 'cost'          THEN target_value END) AS cost,
                SUM(CASE WHEN metric_name = 'registrations' THEN target_value END) AS regs
            FROM ps.targets
            WHERE market = ?
              AND fiscal_year = ?
              AND period_type = 'monthly'
              AND metric_name IN ('cost', 'registrations')
            GROUP BY period_key
            ORDER BY period_key
        """, [market, year]).fetchall()
    except Exception:
        return None
    if annual is None or (annual[0] is None and annual[1] is None):
        return None
    cost_total, regs_total, n_months = annual
    monthly = []
    for row in monthly_rows:
        monthly.append({
            'period_key': row[0],
            'spend': float(row[1]) if row[1] is not None else None,
            'regs':  float(row[2]) if row[2] is not None else None,
        })
    return {
        'year': year,
        'annual_spend_target': float(cost_total) if cost_total is not None else None,
        'annual_regs_target':  float(regs_total) if regs_total is not None else None,
        'n_months_present':    int(n_months) if n_months is not None else 0,
        'monthly':             monthly,
        'source':              'ps.targets (monthly sum)',
    }


def _fetch_spend_bounds(con, market: str) -> dict | None:
    """Fetch operational spend bounds from ps.market_constraints_manual (Mechanism A, 2026-04-23).

    Returns None if no row or all-null. Values are per-week dollars.
    Consumed by mpe_engine.js::solveIeccpTarget to clamp search space.
    """
    try:
        row = con.execute("""
            SELECT min_weekly_nb_spend, max_weekly_nb_spend,
                   min_weekly_brand_spend, max_weekly_brand_spend,
                   spend_bounds_rationale
            FROM ps.market_constraints_manual
            WHERE market = ?
        """, [market]).fetchone()
    except Exception:
        return None
    if row is None:
        return None
    min_nb, max_nb, min_brand, max_brand, rationale = row
    if all(v is None for v in (min_nb, max_nb, min_brand, max_brand)):
        return None
    return {
        'min_weekly_nb_spend': float(min_nb) if min_nb is not None else None,
        'max_weekly_nb_spend': float(max_nb) if max_nb is not None else None,
        'min_weekly_brand_spend': float(min_brand) if min_brand is not None else None,
        'max_weekly_brand_spend': float(max_brand) if max_brand is not None else None,
        'rationale': rationale,
    }


def _market_fallback_summary(params: dict) -> str:
    """Summarize the fallback mix for UI banner."""
    levels = {p.get('fallback_level') for p in params.values() if p.get('fallback_level')}
    if not levels:
        return 'no_parameters'
    if levels == {'market_specific'}:
        return 'all_market_specific'
    if 'regional_fallback' in levels or 'conservative_default' in levels:
        if 'market_specific' in levels:
            return 'some_regional_fallback'
        return 'all_regional_fallback'
    if levels == {'market_specific', 'derived_from_cpa'}:
        return 'market_specific_with_cpc_derived'
    return 'mixed'


def _region_summary(regions: dict, market_data: dict) -> dict:
    """Build the regional summary block for UI freshness/fallback banner."""
    out = {}
    for region, constituents in regions.items():
        summaries = [
            market_data.get(m, {}).get('fallback_summary', 'no_parameters')
            for m in constituents
        ]
        out[region] = {
            'constituents': constituents,
            'per_market_fallback': dict(zip(constituents, summaries)),
            'banner': _build_region_banner(constituents, summaries),
        }
    return out


def _build_region_banner(constituents: list[str], summaries: list[str]) -> str:
    """One-line banner. Example: 'MX US AU market-specific | CA UK DE FR IT ES JP regional fallback'."""
    market_specific = [m for m, s in zip(constituents, summaries) if s == 'all_market_specific' or s == 'market_specific_with_cpc_derived']
    some_fallback = [m for m, s in zip(constituents, summaries) if s == 'some_regional_fallback']
    all_fallback = [m for m, s in zip(constituents, summaries) if s == 'all_regional_fallback']
    parts = []
    if market_specific:
        parts.append(f"{' '.join(market_specific)} market-specific")
    if some_fallback:
        parts.append(f"{' '.join(some_fallback)} mixed fallback")
    if all_fallback:
        parts.append(f"{' '.join(all_fallback)} regional fallback")
    return ' | '.join(parts) or 'no data'


def _write_stub(reason: str) -> int:
    """Emit a minimal JSON when DB is unreachable — UI should show 'data unavailable' banner."""
    stub = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'methodology_version': '1.0.0',
        'fallback': True,
        'reason': reason,
        'markets': {},
        'regions': {},
        'global': {
            'market_list': ALL_MARKETS,
            'region_list': list(REGIONS.keys()),
        },
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(stub, indent=2))
    print(f"[export-projection-data] Wrote stub due to: {reason}")
    return 1


def _snapshot_and_fetch_confidence_history(con, market: str, current_year: int) -> list[dict]:
    """Snapshot today's CI width for `market` and return the last 16 snapshots.

    Research report #P5-11 consumer. Storage: local DuckDB file at
    dashboards/data/confidence-history.duckdb (NOT ps_analytics — that's
    read-only from the export-side connection). Idempotent per
    (market, snapshot_date) via UNIQUE constraint. Safe to run repeatedly.

    Computation: run the engine at the default Y{current_year} @ 75% ieccp
    scenario, extract credible_intervals.total_regs.ci['90'], compute
    ci_width_pct = (hi - lo) / central * 100. Skip markets where the engine
    can't produce a CI.

    Return shape: list of {week, ci_width_pct} entries, oldest-first, up to
    16. Empty list on any failure — UI renders the "collecting data" state.
    """
    from datetime import date as _date
    try:
        from prediction.mpe_engine import ProjectionInputs, project as _project
        import duckdb as _duckdb
    except ImportError:
        return []

    from pathlib import Path as _Path
    history_path = _Path(__file__).parent / 'data' / 'confidence-history.duckdb'
    history_path.parent.mkdir(parents=True, exist_ok=True)

    snapshot_date = _date.today().isoformat()
    week_key = f'{current_year}-W{_date.today().isocalendar().week:02d}'

    try:
        hcon = _duckdb.connect(str(history_path))
        hcon.execute(
            """CREATE TABLE IF NOT EXISTS forecast_uncertainty_history (
                 market VARCHAR NOT NULL,
                 snapshot_date DATE NOT NULL,
                 week_key VARCHAR NOT NULL,
                 ci_width_pct DOUBLE,
                 ci_lo_regs DOUBLE,
                 ci_hi_regs DOUBLE,
                 central_regs DOUBLE,
                 method VARCHAR DEFAULT 'bootstrap_90',
                 engine_version VARCHAR,
                 PRIMARY KEY (market, snapshot_date)
               )"""
        )
    except Exception as e:
        print(f"[{market}] confidence_history table init failed: {type(e).__name__}: {e}")
        return []

    # Compute current-week CI. Default scenario so week-over-week snapshots
    # are comparable without scenario noise.
    try:
        inp = ProjectionInputs(
            scope=market,
            time_period=f'Y{current_year}',
            target_mode='ieccp',
            target_value=0.75,
        )
        result = _project(inp)
        ci_blob = result.credible_intervals.get('total_regs') if result.credible_intervals else None
        ci_90 = (ci_blob.get('ci') or {}).get('90') if isinstance(ci_blob, dict) else None
        central = (ci_blob or {}).get('central') if isinstance(ci_blob, dict) else None
        if ci_90 and central and central > 0:
            ci_lo, ci_hi = ci_90[0], ci_90[1]
            width_pct = (ci_hi - ci_lo) / central * 100.0
            hcon.execute(
                """INSERT OR REPLACE INTO forecast_uncertainty_history
                   (market, snapshot_date, week_key, ci_width_pct,
                    ci_lo_regs, ci_hi_regs, central_regs, method, engine_version)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (market, snapshot_date, week_key, round(width_pct, 2),
                 round(ci_lo, 1), round(ci_hi, 1), round(central, 1),
                 'bootstrap_90', result.methodology_version or ''),
            )
    except Exception as e:
        print(f"[{market}] confidence_history snapshot skipped: {type(e).__name__}: {e}")

    try:
        rows = hcon.execute(
            """SELECT week_key, ci_width_pct
               FROM forecast_uncertainty_history
               WHERE market = ?
               ORDER BY snapshot_date DESC
               LIMIT 16""",
            (market,),
        ).fetchall()
        hcon.close()
        return [{'week': r[0], 'ci_width_pct': float(r[1])} for r in reversed(rows)]
    except Exception:
        try:
            hcon.close()
        except Exception:
            pass
        return []


def main() -> int:
    con = _get_connection()
    if con is None:
        return _write_stub("MotherDuck connection unavailable (check motherduck_token env var)")

    current_year = date.today().year

    out = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'methodology_version': '1.0.0',
        'fallback': False,
        'markets': {},
        'regions': {},
        'global': {
            'market_list': ALL_MARKETS,
            'region_list': list(REGIONS.keys()),
            'current_year': current_year,
        },
    }

    # Collect market data
    for market in ALL_MARKETS:
        try:
            params = _fetch_parameters(con, market)
            ytd = _fetch_ytd_weekly(con, market, current_year)
            regimes = _fetch_regime_events(con, market)
            regime_fit_state = _fetch_regime_fit_state(con, market)
            spend_bounds = _fetch_spend_bounds(con, market)
            op2_targets = _fetch_op2_targets(con, market, current_year)

            # Pre-compute Brand trajectory for common scenarios so JS can display
            # without re-fitting. Phase 6.1.7 parity: JS reads these arrays.
            brand_trajectory_y2026 = None
            try:
                from prediction.brand_trajectory import project_brand_trajectory
                from datetime import timedelta as _td
                jan4 = date(current_year, 1, 4)
                start = jan4 - _td(days=jan4.weekday())
                weeks = [start + _td(weeks=i) for i in range(52)]
                bt = project_brand_trajectory(market, weeks)
                brand_trajectory_y2026 = {
                    'weeks': [w.isoformat() for w in bt.weeks],
                    'regs_per_week': [round(r, 2) for r in bt.regs_per_week],
                    'spend_per_week': [round(s, 2) for s in bt.spend_per_week],
                    'brand_cpa_used': round(bt.brand_cpa_used, 2),
                    'total_regs': round(bt.total_regs, 2),
                    'total_spend': round(bt.total_spend, 2),
                    'contribution': bt.contribution,
                    'warnings': bt.warnings,
                    'lineage': bt.lineage,
                }
            except Exception as e:
                print(f"[{market}] brand_trajectory skipped: {type(e).__name__}: {e}")

            fallback_summary = _market_fallback_summary(params)

            # Research report #P5-11 (mpe-findings): confidence_history sparkline
            # in the Model View drawer. Snapshot current-week bootstrap CI width
            # into ps.forecast_uncertainty_history on each export run (idempotent
            # per market/date via PRIMARY KEY), then read back the last 16 rows.
            # First run emits 1 row per market; weekly runs grow the history.
            confidence_history = _snapshot_and_fetch_confidence_history(con, market, current_year)

            market_entry = {
                'parameters': _json_safe(params),
                'ytd_weekly': ytd,
                'regime_events': regimes,
                'regime_fit_state': regime_fit_state,
                'brand_trajectory_y2026': brand_trajectory_y2026,
                'fallback_summary': fallback_summary,
                'clean_weeks_count': len(ytd),
                'op2_targets': op2_targets,
                'confidence_history': confidence_history,
            }
            if spend_bounds is not None:
                market_entry['_spend_bounds'] = spend_bounds
            out['markets'][market] = market_entry
            bounds_label = ' bounds=on' if spend_bounds else ''
            bt_label = ' bt=y2026' if brand_trajectory_y2026 else ''
            op2_label = ' op2=on' if op2_targets else ''
            print(f"[{market}] {len(params)} params, {len(ytd)} YTD weeks, "
                  f"{len(regimes)} regimes ({len(regime_fit_state)} fit-state), "
                  f"fallback={fallback_summary}{bounds_label}{bt_label}{op2_label}")
        except Exception as e:
            print(f"[{market}] ERROR: {type(e).__name__}: {e}")
            out['markets'][market] = {
                'error': f"{type(e).__name__}: {e}",
                'fallback_summary': 'error',
            }

    # Regional summaries
    out['regions'] = _region_summary(REGIONS, out['markets'])

    # Anomalies (Phase 4.1 + Phase 6.5.3) — inline so UI can surface per-market
    # without a second fetch. Uses the already-open export connection to avoid
    # DuckDB's "same database different configuration" conflict with a second conn.
    try:
        from prediction.mpe_anomaly import (
            check_fit_quality, check_regime_confidence,
            check_op2_pacing, check_ytd_projection_step, Anomaly,
        )
        anomalies = []
        for m in out['markets'].keys():
            anomalies.extend(check_fit_quality(con, m))
            anomalies.extend(check_regime_confidence(con, m))
            anomalies.extend(check_op2_pacing(con, m))
            anomalies.extend(check_ytd_projection_step(con, m))
        by_market: dict[str, list[dict]] = {}
        for a in anomalies:
            by_market.setdefault(a.market, []).append({
                'check': a.check, 'severity': a.severity,
                'detail': a.detail, 'remediation': a.remediation,
            })
        out['anomalies'] = {
            'markets': by_market,
            'summary': {
                'total': len(anomalies),
                'error': sum(1 for a in anomalies if a.severity == 'error'),
                'warn':  sum(1 for a in anomalies if a.severity == 'warn'),
                'info':  sum(1 for a in anomalies if a.severity == 'info'),
            },
        }
        print(f"  anomalies: {out['anomalies']['summary']}")
    except Exception as e:
        out['anomalies'] = {'markets': {}, 'summary': {}, 'error': f'{type(e).__name__}: {e}'}
        print(f"  WARNING: anomaly scan failed: {e}")

    # Write
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(out, indent=2, default=str)
    OUTPUT_PATH.write_text(payload)

    size_kb = len(payload.encode('utf-8')) / 1024.0
    print(f"\n[export-projection-data] Wrote {OUTPUT_PATH} ({size_kb:.1f} KB)")
    if size_kb > TARGET_SIZE_KB:
        print(f"  WARNING: exceeds {TARGET_SIZE_KB}KB target — consider compacting seasonality or YTD weeks")

    try:
        con.close()
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
