"""Tests for the parameter registry schema — ps.market_projection_params_current view.

These tests hit MotherDuck in read-only mode to verify the live registry invariants.
If MotherDuck is unreachable, tests skip cleanly rather than failing.

Covers R1.1-R1.7 (registry shape), R13.3 (lineage), R14.3 (versioning).
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.expanduser('~/shared/tools'))


def _get_connection():
    """Return a read-only DuckDB connection to MotherDuck, or None if unavailable."""
    try:
        import duckdb
        from prediction.config import MOTHERDUCK_TOKEN
        if not MOTHERDUCK_TOKEN:
            return None
        return duckdb.connect(
            f'md:ps_analytics?motherduck_token={MOTHERDUCK_TOKEN}',
            read_only=True,
        )
    except Exception:
        return None


@pytest.fixture(scope='module')
def con():
    c = _get_connection()
    if c is None:
        pytest.skip("MotherDuck connection unavailable — skipping registry tests")
    yield c
    try:
        c.close()
    except Exception:
        pass


# ---------- Schema shape ----------

def test_registry_has_required_columns(con):
    """ps.market_projection_params must expose the 15 canonical columns."""
    cols = {
        r[0] for r in con.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema='ps' AND table_name='market_projection_params'"
        ).fetchall()
    }
    required = {
        'market', 'parameter_name', 'parameter_version',
        'value_scalar', 'value_json',
        'refit_cadence', 'last_refit_at', 'last_validated_at',
        'validation_mape', 'source',
        'fallback_level', 'lineage', 'fitted_on_data_range',
        'notes', 'is_active',
    }
    assert required.issubset(cols), f"Missing columns: {required - cols}"


def test_current_view_exists(con):
    """ps.market_projection_params_current must be a view over latest-active rows."""
    result = con.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema='ps' AND table_name='market_projection_params_current'"
    ).fetchone()
    assert result is not None


def test_regime_changes_table_exists(con):
    """ps.regime_changes is the source of truth for regime filtering."""
    result = con.execute(
        "SELECT COUNT(*) FROM ps.regime_changes WHERE active = TRUE"
    ).fetchone()
    assert result[0] > 0


# ---------- Registry content invariants ----------

def test_all_active_markets_have_ccps(con):
    """9 of 10 markets should have brand_ccp + nb_ccp seeded (AU null by design)."""
    rows = con.execute("""
        SELECT market, parameter_name, value_scalar
        FROM ps.market_projection_params_current
        WHERE parameter_name IN ('brand_ccp', 'nb_ccp')
    """).fetchall()
    markets_with_ccp = {r[0] for r in rows if r[2] is not None}
    expected = {'MX', 'US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP'}
    assert expected.issubset(markets_with_ccp), \
        f"Missing CCPs for: {expected - markets_with_ccp}"


def test_all_markets_have_elasticity_fits(con):
    """All 10 markets should have brand+nb CPA elasticity fits."""
    rows = con.execute("""
        SELECT market
        FROM ps.market_projection_params_current
        WHERE parameter_name IN ('brand_cpa_elasticity', 'nb_cpa_elasticity')
        GROUP BY market
        HAVING COUNT(DISTINCT parameter_name) = 2
    """).fetchall()
    markets = {r[0] for r in rows}
    expected = {'MX', 'US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP', 'AU'}
    assert expected.issubset(markets), \
        f"Missing elasticity fits for: {expected - markets}"


def test_fallback_level_values_are_canonical(con):
    """Only known fallback_level values should appear in the registry."""
    rows = con.execute("""
        SELECT DISTINCT fallback_level
        FROM ps.market_projection_params_current
        WHERE fallback_level IS NOT NULL
    """).fetchall()
    values = {r[0] for r in rows}
    canonical = {
        'market_specific', 'regional_fallback', 'derived_from_cpa',
        'conservative_default', 'southern_hemisphere_hybrid',
        'prior_version',
    }
    unknown = values - canonical
    assert not unknown, f"Non-canonical fallback_level values found: {unknown}"


def test_lineage_populated_on_fitted_params(con):
    """Every fitted elasticity/seasonality/yoy param should have lineage."""
    rows = con.execute("""
        SELECT market, parameter_name, lineage
        FROM ps.market_projection_params_current
        WHERE parameter_name IN (
            'brand_cpa_elasticity', 'nb_cpa_elasticity',
            'brand_seasonality_shape', 'nb_seasonality_shape',
            'brand_yoy_growth', 'nb_yoy_growth'
        )
    """).fetchall()
    missing_lineage = [(m, p) for m, p, ln in rows if not ln]
    assert not missing_lineage, f"Params missing lineage: {missing_lineage}"


def test_last_refit_at_populated(con):
    """Every active parameter row should carry a last_refit_at timestamp."""
    count = con.execute("""
        SELECT COUNT(*) FROM ps.market_projection_params_current
        WHERE last_refit_at IS NULL
          AND parameter_name NOT IN ('ieccp_target', 'ieccp_range',
                                      'supported_target_modes', 'market_strategy_type',
                                      'brand_ccp_q1_static', 'nb_ccp_q1_static')
    """).fetchone()
    assert count[0] == 0, f"{count[0]} fitted params are missing last_refit_at"
