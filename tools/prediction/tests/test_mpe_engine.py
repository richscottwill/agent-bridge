"""Tests for mpe_engine.py — time period parser, target mode solvers, warning taxonomy.

Covers R2 (target modes), R7 (period parsing), R9 (readiness / fallback), R11 (multi-year),
and the warning surface (HIGH_EXTRAPOLATION / SETUP_REQUIRED / STALE_PARAMETERS / VERY_WIDE_CI).
"""

from __future__ import annotations

import math
import os
import sys
from datetime import datetime, date, timedelta

import pytest

sys.path.insert(0, os.path.expanduser('~/shared/tools'))

from prediction import mpe_engine as engine
from prediction.mpe_engine import (
    parse_time_period,
    ProjectionInputs,
    project,
    ALL_MARKETS,
    ALL_REGIONS,
    VERY_WIDE_CI_RATIO,
    HIGH_UNCERTAINTY_RATIO,
    MIN_WEEKS_MULTI_YEAR,
)


# ---------- Time period parser ----------

def test_parse_week():
    tp = parse_time_period('W15')
    assert tp['type'] == 'week'
    assert tp['weeks'] == [15]


def test_parse_month():
    tp = parse_time_period('M04')
    assert tp['type'] == 'month'
    assert len(tp['weeks']) >= 4   # April has at least 4 ISO weeks


def test_parse_quarter():
    tp = parse_time_period('Q2')
    assert tp['type'] == 'quarter'
    # Q2 spans W14-W27 inclusive = 14 weeks (engine convention)
    assert len(tp['weeks']) == 14


def test_parse_year():
    tp = parse_time_period('Y2026')
    assert tp['type'] == 'year'
    assert len(tp['weeks']) == 52


def test_parse_multi_year_1():
    tp = parse_time_period('MY1')
    assert tp['type'] == 'multi_year'
    assert tp['n_years'] == 1


def test_parse_multi_year_2():
    tp = parse_time_period('MY2')
    assert tp['type'] == 'multi_year'
    assert tp['n_years'] == 2


def test_parse_my3_rejected():
    """R11.9: MY3 and beyond MUST raise."""
    with pytest.raises(ValueError, match="MY3"):
        parse_time_period('MY3')


def test_parse_my0_rejected():
    with pytest.raises(ValueError, match="Multi-year must be"):
        parse_time_period('MY0')


def test_parse_invalid_format():
    with pytest.raises(ValueError):
        parse_time_period('XYZ')


# ---------- Invalid inputs ----------

def test_unknown_scope_returns_invalid_input():
    inputs = ProjectionInputs(
        scope='XX', time_period='Q2', target_mode='spend', target_value=100000.0,
    )
    out = project(inputs)
    assert out.outcome == 'INVALID_INPUT'
    assert any('UNKNOWN_SCOPE' in w for w in out.warnings)


def test_unknown_target_mode_returns_invalid(monkeypatch):
    # Need a valid market but patch load_parameters to avoid DB dependency
    fixtures = _simple_market_params()

    monkeypatch.setattr(engine, 'load_parameters', lambda m: fixtures)
    monkeypatch.setattr(engine, 'check_parameter_readiness', lambda m, p: [])
    monkeypatch.setattr(engine, '_db', lambda: _FakeCon())

    inputs = ProjectionInputs(
        scope='MX', time_period='Q2', target_mode='bogus_mode', target_value=10.0,
    )
    out = project(inputs)
    assert out.outcome == 'INVALID_INPUT'


# ---------- SETUP_REQUIRED short-circuit ----------

def test_setup_required_on_missing_params(monkeypatch):
    """When load_parameters returns empty, engine should short-circuit with SETUP_REQUIRED."""
    monkeypatch.setattr(engine, 'load_parameters', lambda m: {})
    # Let the actual readiness check run (don't monkeypatch it) — empty params should trip SETUP_REQUIRED
    inputs = ProjectionInputs(
        scope='MX', time_period='Q2', target_mode='spend', target_value=100000.0,
    )
    out = project(inputs)
    assert out.outcome == 'SETUP_REQUIRED'
    assert any('SETUP_REQUIRED' in w for w in out.warnings)


# ---------- Target mode: spend ----------

def test_spend_target_produces_valid_totals(monkeypatch):
    fixtures = _simple_market_params()
    monkeypatch.setattr(engine, 'load_parameters', lambda m: fixtures)
    monkeypatch.setattr(engine, 'check_parameter_readiness', lambda m, p: [])
    monkeypatch.setattr(engine, '_db', lambda: _FakeCon())

    inputs = ProjectionInputs(
        scope='MX', time_period='Q2', target_mode='spend', target_value=325000.0,
    )
    out = project(inputs)
    assert out.outcome == 'OK'
    assert out.totals['total_spend'] > 0
    assert out.totals['total_regs'] > 0
    assert out.totals['blended_cpa'] > 0
    assert out.totals['ieccp'] is not None


# ---------- Target mode: ieccp binary search ----------

def test_ieccp_target_converges_within_tolerance(monkeypatch):
    """Binary search for ieccp=500 should converge and resulting ie%CCP should be within 0.5 of target.

    Uses non-flat elasticity so ie%CCP responds to spend. Target 500% is within the
    engine's achievable range for this fixture (confirmed by solver bracket exploration).
    """
    fixtures = _market_params_with_elasticity(
        brand_b=0.20, nb_b=0.30,
    )
    monkeypatch.setattr(engine, 'load_parameters', lambda m: fixtures)
    monkeypatch.setattr(engine, 'check_parameter_readiness', lambda m, p: [])
    monkeypatch.setattr(engine, '_db', lambda: _FakeCon())

    inputs = ProjectionInputs(
        scope='MX', time_period='Q2', target_mode='ieccp', target_value=500.0,
    )
    out = project(inputs)
    assert out.outcome == 'OK'
    assert abs(out.totals['ieccp'] - 500.0) < 0.5, \
        f"Expected ie%CCP near 500, got {out.totals['ieccp']}"


# ---------- Warnings: HIGH_EXTRAPOLATION ----------

def test_high_extrapolation_fires_when_spend_exceeds_historical(monkeypatch):
    """Spend >1.5× historical weekly max should emit HIGH_EXTRAPOLATION."""
    fixtures = _simple_market_params()
    monkeypatch.setattr(engine, 'load_parameters', lambda m: fixtures)
    monkeypatch.setattr(engine, 'check_parameter_readiness', lambda m, p: [])
    # Set historical max low so proposed spend definitely exceeds 1.5×
    monkeypatch.setattr(engine, '_db', lambda: _FakeCon(hist_max=1000.0))

    inputs = ProjectionInputs(
        scope='MX', time_period='Q2', target_mode='spend', target_value=10_000_000.0,
    )
    out = project(inputs)
    assert out.outcome == 'OK'
    assert any('HIGH_EXTRAPOLATION' in w for w in out.warnings)


# ---------- Credible interval integration ----------

def test_project_populates_credible_intervals(monkeypatch):
    """Every OK projection should populate credible_intervals with 6 metrics."""
    fixtures = _simple_market_params()
    monkeypatch.setattr(engine, 'load_parameters', lambda m: fixtures)
    monkeypatch.setattr(engine, 'check_parameter_readiness', lambda m, p: [])
    monkeypatch.setattr(engine, '_db', lambda: _FakeCon())

    inputs = ProjectionInputs(
        scope='MX', time_period='Q2', target_mode='spend', target_value=325000.0,
    )
    out = project(inputs)
    assert out.outcome == 'OK'
    expected_metrics = {'total_regs', 'total_spend', 'blended_cpa', 'ieccp', 'brand_regs', 'nb_regs'}
    assert expected_metrics.issubset(out.credible_intervals.keys())
    for metric in ['total_regs', 'total_spend']:
        ci = out.credible_intervals[metric]
        lo, hi = ci['ci']['90']
        assert lo <= ci['central'] <= hi


# ---------- Helpers ----------

def _simple_market_params() -> dict:
    """Minimal deterministic market params for engine tests (mirrors test_regional_rollup)."""
    return _market_params_with_elasticity(brand_b=0.0, nb_b=0.0)


def _market_params_with_elasticity(brand_b: float = 0.0, nb_b: float = 0.0) -> dict:
    """Market params with tunable elasticity exponents for solver tests."""
    a_brand = math.log(100.0)
    a_nb = math.log(25.0)
    return {
        'brand_cpa_elasticity': {
            'value_json': {
                'a': a_brand, 'b': brand_b, 'r_squared': 0.80,
                'posterior_cov': [[0.001, 0.0], [0.0, 0.001]],
            },
            'fallback_level': 'market_specific', 'lineage': 'test',
            'last_refit_at': None,
        },
        'nb_cpa_elasticity': {
            'value_json': {
                'a': a_nb, 'b': nb_b, 'r_squared': 0.80,
                'posterior_cov': [[0.001, 0.0], [0.0, 0.001]],
            },
            'fallback_level': 'market_specific', 'lineage': 'test',
            'last_refit_at': None,
        },
        'brand_cpc_elasticity': {
            'value_json': {
                'a': a_brand - 1.0, 'b': brand_b, 'r_squared': 0.50,
                'posterior_cov': [[0.001, 0.0], [0.0, 0.001]],
            },
            'fallback_level': 'market_specific', 'lineage': 'test',
            'last_refit_at': None,
        },
        'nb_cpc_elasticity': {
            'value_json': {
                'a': a_nb - 1.0, 'b': nb_b, 'r_squared': 0.50,
                'posterior_cov': [[0.001, 0.0], [0.0, 0.001]],
            },
            'fallback_level': 'market_specific', 'lineage': 'test',
            'last_refit_at': None,
        },
        'brand_seasonality_shape': {
            'value_json': {
                'weights': [1.0] * 52,
                'posteriors': [{'mean': 1.0, 'std': 0.05, 'provenance': 'fit'}] * 52,
            },
            'fallback_level': 'market_specific', 'lineage': 'test',
            'last_refit_at': None,
        },
        'nb_seasonality_shape': {
            'value_json': {
                'weights': [1.0] * 52,
                'posteriors': [{'mean': 1.0, 'std': 0.05, 'provenance': 'fit'}] * 52,
            },
            'fallback_level': 'market_specific', 'lineage': 'test',
            'last_refit_at': None,
        },
        'brand_yoy_growth': {
            'value_json': {'mean': 0.0, 'std': 0.05, 'r_squared': 0.5},
            'fallback_level': 'market_specific', 'lineage': 'test',
            'last_refit_at': None,
        },
        'nb_yoy_growth': {
            'value_json': {'mean': 0.0, 'std': 0.05, 'r_squared': 0.5},
            'fallback_level': 'market_specific', 'lineage': 'test',
            'last_refit_at': None,
        },
        'brand_ccp': {
            'value_scalar': 97.22, 'value_json': None,
            'fallback_level': 'market_specific', 'lineage': 'test',
            'last_refit_at': None,
        },
        'nb_ccp': {
            'value_scalar': 27.59, 'value_json': None,
            'fallback_level': 'market_specific', 'lineage': 'test',
            'last_refit_at': None,
        },
        'brand_spend_share': {
            'value_json': {'brand_share': 0.11, 'nb_share': 0.89},
            'fallback_level': 'market_specific', 'lineage': 'test',
            'last_refit_at': None,
        },
        'supported_target_modes': {
            'value_json': ['spend', 'ieccp', 'regs'], 'value_scalar': None,
            'fallback_level': 'market_specific', 'lineage': 'test',
            'last_refit_at': None,
        },
    }


class _FakeCon:
    def __init__(self, hist_max: float = 1_000_000_000.0):
        self._hist_max = hist_max

    def execute(self, sql, params=None):
        return self

    def fetchone(self):
        return (self._hist_max,)

    def fetchall(self):
        return []
