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
    brand_ / nb_ variants for each metric.
    """
    rows = con.execute("""
        SELECT period_start, registrations, cost, clicks, cpa, cpc, cvr,
               brand_registrations, nb_registrations, ieccp
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
            'nb_regs': int(r[8]) if r[8] is not None else None,
            'ieccp': float(r[9]) if r[9] is not None else None,
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
            spend_bounds = _fetch_spend_bounds(con, market)

            fallback_summary = _market_fallback_summary(params)
            market_entry = {
                'parameters': _json_safe(params),
                'ytd_weekly': ytd,
                'regime_events': regimes,
                'fallback_summary': fallback_summary,
                'clean_weeks_count': len(ytd),
            }
            if spend_bounds is not None:
                market_entry['_spend_bounds'] = spend_bounds
            out['markets'][market] = market_entry
            bounds_label = ' bounds=on' if spend_bounds else ''
            print(f"[{market}] {len(params)} params, {len(ytd)} YTD weeks, {len(regimes)} active regimes, fallback={fallback_summary}{bounds_label}")
        except Exception as e:
            print(f"[{market}] ERROR: {type(e).__name__}: {e}")
            out['markets'][market] = {
                'error': f"{type(e).__name__}: {e}",
                'fallback_summary': 'error',
            }

    # Regional summaries
    out['regions'] = _region_summary(REGIONS, out['markets'])

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
