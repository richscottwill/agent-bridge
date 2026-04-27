"""Regional rollup validation — MPE R6.1-R6.6.

WHY THIS TEST EXISTS
    The regional projection (NA / EU5 / WW) runs each constituent market
    independently and then combines the results via sum-then-divide for
    ie%CCP. This is mathematically different from averaging per-market
    ie%CCP values (which is always wrong because CCPs vary by ≥4× across
    markets). This test locks the correct math in place so a future
    refactor can't silently regress to "average the ie%CCPs."

WHAT IT CHECKS
    1. Canonical hand-computed scenario (US + CA with controlled fits):
       regional total_regs = sum of per-market total_regs
       regional ie%CCP = regional_total_spend / Σ(market_regs × market_CCP) × 100
    2. Scale precision across MX ($97) + US ($412) + AU (null) in a
       WW-shaped rollup — no silent precision loss.
    3. Null-CCP markets (AU) correctly drop out of the ie%CCP denominator
       without corrupting the aggregation.

HOW TO RUN
    pytest shared/tools/prediction/tests/test_regional_rollup.py -v
    # or rerun at every refit via mpe-acceptance-core hook
"""

from __future__ import annotations

import math
import os
import sys

import pytest

sys.path.insert(0, os.path.expanduser('~/shared/tools'))

from prediction import mpe_engine as engine
from prediction.mpe_engine import (
    ProjectionInputs,
    project,
    REGION_CONSTITUENTS,
)


# ---------- Fixtures — deterministic parameter sets ----------

def _elast_params(a: float, b: float) -> dict:
    """Package an elasticity result as it would appear in params dict."""
    return {
        'value_json': {
            'a': a,
            'b': b,
            'r_squared': 0.80,
            'posterior_cov': [[0.001, 0.0], [0.0, 0.001]],
            'fallback_level': 'market_specific',
        },
        'fallback_level': 'market_specific',
        'lineage': 'test-fixture',
        'last_refit_at': None,
    }


def _seas_flat() -> dict:
    """52-week flat seasonality (all weights = 1.0)."""
    return {
        'value_json': {
            'weights': [1.0] * 52,
            'posteriors': [{'mean': 1.0, 'std': 0.05, 'provenance': 'fit'}] * 52,
        },
        'fallback_level': 'market_specific',
        'lineage': 'test-fixture',
        'last_refit_at': None,
    }


def _yoy_flat() -> dict:
    """Zero YoY growth — preserves point estimate for single-year test."""
    return {
        'value_json': {'mean': 0.0, 'std': 0.01, 'r_squared': 0.5},
        'fallback_level': 'market_specific',
        'lineage': 'test-fixture',
        'last_refit_at': None,
    }


def _ccp(value: float | None) -> dict:
    return {
        'value_scalar': value,
        'value_json': None,
        'fallback_level': 'market_specific',
        'lineage': 'test-fixture',
        'last_refit_at': None,
    }


def _spend_share(brand_share: float) -> dict:
    return {
        'value_json': {'brand_share': brand_share, 'nb_share': 1.0 - brand_share},
        'fallback_level': 'market_specific',
        'lineage': 'test-fixture',
        'last_refit_at': None,
    }


def _tuned_params(target_brand_cpa: float, target_nb_cpa: float,
                  brand_ccp: float | None, nb_ccp: float | None,
                  brand_share: float = 0.3,
                  supported_modes: list[str] | None = None) -> dict:
    """Build a complete market params dict with elasticities tuned so
    that at spend=$50,000 the resulting CPAs equal the target values.

    Math: CPA = exp(a) * spend^b. With b=0 the CPA is spend-invariant:
    CPA = exp(a). So a = ln(target_cpa).
    """
    a_brand = math.log(target_brand_cpa)
    a_nb = math.log(target_nb_cpa)
    return {
        'brand_cpa_elasticity': _elast_params(a_brand, 0.0),
        'nb_cpa_elasticity': _elast_params(a_nb, 0.0),
        'brand_cpc_elasticity': _elast_params(a_brand - 1.0, 0.0),   # arbitrary, unused in assertions
        'nb_cpc_elasticity': _elast_params(a_nb - 1.0, 0.0),
        'brand_seasonality_shape': _seas_flat(),
        'nb_seasonality_shape': _seas_flat(),
        'brand_yoy_growth': _yoy_flat(),
        'nb_yoy_growth': _yoy_flat(),
        'brand_ccp': _ccp(brand_ccp),
        'nb_ccp': _ccp(nb_ccp),
        'brand_spend_share': _spend_share(brand_share),
        'supported_target_modes': {
            'value_json': supported_modes or ['spend', 'ieccp', 'regs'],
            'value_scalar': None,
            'fallback_level': 'market_specific',
            'lineage': 'test-fixture',
            'last_refit_at': None,
        },
    }


# ---------- Test 1: Canonical hand-computed NA rollup ----------

@pytest.mark.skip(
    reason=(
        "v1.1 Slim pivot (Phase 6.1.6, 2026-04-23): this test validates v1 "
        "top-down elasticity rollup using synthetic Brand/NB spend-share "
        "allocation. v1.1 Slim reads real Brand projections from ps.v_weekly "
        "(Brand-Anchor architecture), so the fake_load fixture's synthetic "
        "brand_spend_share and elasticity curves no longer control the output. "
        "Phase 6.1.8 rewrites this test against v1.1 Slim inputs — Brand "
        "trajectory fixtures + NB residual fixtures — then re-enables."
    )
)
def test_na_rollup_matches_hand_computed(monkeypatch):
    """US + CA with tuned fits; assert engine matches hand-computed math.

    Per-market setup (each market gets $50k spend via naive split of $100k regional target):
      US: Brand_CCP=$400, NB_CCP=$50, Brand_share=0.2, Brand_CPA=$100, NB_CPA=$25
      CA: Brand_CCP=$200, NB_CCP=$40, Brand_share=0.2, Brand_CPA=$100, NB_CPA=$25

    Per-market regs at $50k total spend, flat seasonality, zero YoY:
      US Brand regs = ($50k × 0.2) / $100 = 100
      US NB regs    = ($50k × 0.8) / $25  = 1,600
      CA Brand regs = ($50k × 0.2) / $100 = 100
      CA NB regs    = ($50k × 0.8) / $25  = 1,600

    Regional hand-compute:
      total_regs = 100 + 1,600 + 100 + 1,600 = 3,400
      total_spend = 50,000 + 50,000 = 100,000
      blended_cpa = 100,000 / 3,400 = $29.41
      ieccp_denom = 100×400 + 1600×50 + 100×200 + 1600×40
                  = 40,000 + 80,000 + 20,000 + 64,000 = 204,000
      ieccp = 100,000 / 204,000 × 100 = 49.02%
    """
    fixtures = {
        'US': _tuned_params(
            target_brand_cpa=100.0,
            target_nb_cpa=25.0,
            brand_ccp=400.0,
            nb_ccp=50.0,
            brand_share=0.2,
        ),
        'CA': _tuned_params(
            target_brand_cpa=100.0,
            target_nb_cpa=25.0,
            brand_ccp=200.0,
            nb_ccp=40.0,
            brand_share=0.2,
        ),
    }

    def fake_load(market: str) -> dict:
        if market not in fixtures:
            raise AssertionError(f"Test fixture missing market {market}")
        return fixtures[market]

    monkeypatch.setattr(engine, 'load_parameters', fake_load)
    monkeypatch.setattr(engine, 'check_parameter_readiness', lambda m, p: [])
    # Bypass historical-extrapolation DB fetch (no real DB in test context)
    monkeypatch.setattr(engine, '_db', lambda: _FakeCon())

    inputs = ProjectionInputs(
        scope='NA',
        time_period='W01',   # single-week period to keep math tractable
        target_mode='spend',
        target_value=100_000.0,
    )
    out = project(inputs)

    assert out.outcome == 'OK', f"Expected OK, got {out.outcome} with warnings {out.warnings}"

    # Per-market expectations (each gets $50k)
    # With 1-week period and 52-week flat seasonality, period_factor = 1/1 = 1,
    # but the wk_num iterates once with weight 1.0, so week_brand_spend = 50000 * 0.2 = 10000
    # week_nb_spend = 50000 * 0.8 = 40000. Brand regs = 10000/100 = 100. NB regs = 40000/25 = 1600.
    us = next(c for c in out.constituent_markets if c['market'] == 'US')
    ca = next(c for c in out.constituent_markets if c['market'] == 'CA')

    assert math.isclose(us['brand_regs'], 100.0, rel_tol=0.001), f"US Brand regs: expected 100, got {us['brand_regs']}"
    assert math.isclose(us['nb_regs'], 1600.0, rel_tol=0.001), f"US NB regs: expected 1600, got {us['nb_regs']}"
    assert math.isclose(ca['brand_regs'], 100.0, rel_tol=0.001)
    assert math.isclose(ca['nb_regs'], 1600.0, rel_tol=0.001)

    # Regional totals
    assert math.isclose(out.totals['total_regs'], 3400.0, rel_tol=0.001), \
        f"Regional total_regs: expected 3400, got {out.totals['total_regs']}"
    assert math.isclose(out.totals['total_spend'], 100_000.0, rel_tol=0.001), \
        f"Regional total_spend: expected 100000, got {out.totals['total_spend']}"
    assert math.isclose(out.totals['blended_cpa'], 100_000 / 3400, rel_tol=0.001), \
        f"Regional blended_cpa: expected 29.41, got {out.totals['blended_cpa']}"

    # Hand-computed regional ie%CCP = 100,000 / 204,000 × 100 = 49.0196...
    expected_ieccp = 100_000.0 / 204_000.0 * 100.0
    actual_ieccp = out.totals['ieccp']
    assert actual_ieccp is not None, "Regional ie%CCP should not be None"
    assert math.isclose(actual_ieccp, expected_ieccp, rel_tol=0.0001), \
        f"Regional ie%CCP: expected {expected_ieccp:.4f}, got {actual_ieccp:.4f} — diff > 0.01%"


# ---------- Test 2: Null-CCP handling (AU case) ----------

@pytest.mark.skip(reason="v1.1 Slim pivot (Phase 6.1.6, 2026-04-23): uses v1 fixture pattern; re-enable in 6.1.8 with v1.1 Slim fixtures.")
def test_ww_rollup_with_null_ccp_market(monkeypatch):
    """WW rollup where one market (AU) has null CCPs — ie%CCP denominator
    should correctly drop AU's contribution without crashing.
    """
    # Minimal WW: MX + US + AU with AU null
    fixtures = {
        'MX': _tuned_params(100.0, 25.0, brand_ccp=97.0, nb_ccp=27.0, brand_share=0.11),
        'US': _tuned_params(100.0, 25.0, brand_ccp=412.0, nb_ccp=48.0, brand_share=0.27),
        'CA': _tuned_params(100.0, 25.0, brand_ccp=203.0, nb_ccp=38.0, brand_share=0.30),
        'UK': _tuned_params(100.0, 25.0, brand_ccp=250.0, nb_ccp=60.0, brand_share=0.30),
        'DE': _tuned_params(100.0, 25.0, brand_ccp=291.0, nb_ccp=141.0, brand_share=0.32),
        'FR': _tuned_params(100.0, 25.0, brand_ccp=155.0, nb_ccp=85.0, brand_share=0.30),
        'IT': _tuned_params(100.0, 25.0, brand_ccp=151.0, nb_ccp=92.0, brand_share=0.37),
        'ES': _tuned_params(100.0, 25.0, brand_ccp=150.0, nb_ccp=80.0, brand_share=0.30),
        'JP': _tuned_params(100.0, 25.0, brand_ccp=224.0, nb_ccp=78.0, brand_share=0.92),
        # AU: both CCPs are None — represents the AU "efficiency strategy" market
        'AU': _tuned_params(100.0, 25.0, brand_ccp=None, nb_ccp=None, brand_share=0.30),
    }

    def fake_load(market: str) -> dict:
        return fixtures[market]

    monkeypatch.setattr(engine, 'load_parameters', fake_load)
    monkeypatch.setattr(engine, 'check_parameter_readiness', lambda m, p: [])
    monkeypatch.setattr(engine, '_db', lambda: _FakeCon())

    inputs = ProjectionInputs(
        scope='WW',
        time_period='W01',
        target_mode='spend',
        target_value=1_000_000.0,   # $100k per market (10 markets)
    )
    out = project(inputs)

    assert out.outcome == 'OK', f"Expected OK, got {out.outcome} with warnings {out.warnings}"
    assert len(out.constituent_markets) == 10, "Should have all 10 WW markets represented"

    # total_regs includes AU even though AU CCP is null
    # Each market at $100k: brand = (100k × share) / 100, nb = (100k × (1-share)) / 25
    # Sum across markets should be positive and include AU
    assert out.totals['total_regs'] > 0
    assert out.totals['total_spend'] > 0

    au = next(c for c in out.constituent_markets if c['market'] == 'AU')
    assert au['brand_regs'] > 0, "AU should still contribute regs even with null CCP"
    assert au['nb_regs'] > 0

    # Hand-compute the ie%CCP denominator (excludes AU because AU CCPs are None)
    # AU has $100k spend but contributes 0 to the ie%CCP denominator
    # All other 9 markets contribute: (brand_regs × brand_ccp) + (nb_regs × nb_ccp)
    expected_denom = 0.0
    expected_total_spend_with_ccp = 0.0
    for c in out.constituent_markets:
        m = c['market']
        f = fixtures[m]
        b_ccp = f['brand_ccp']['value_scalar']
        n_ccp = f['nb_ccp']['value_scalar']
        if b_ccp is not None and n_ccp is not None:
            expected_denom += c['brand_regs'] * b_ccp + c['nb_regs'] * n_ccp

    # Regional ie%CCP is total_spend / denom × 100 (NOTE: includes AU spend in numerator,
    # which is how the engine does it and matches the sum-then-divide convention from D16)
    expected_ieccp = out.totals['total_spend'] / expected_denom * 100.0

    actual_ieccp = out.totals['ieccp']
    assert actual_ieccp is not None
    assert math.isclose(actual_ieccp, expected_ieccp, rel_tol=0.0001), \
        f"WW ie%CCP: expected {expected_ieccp:.4f}, got {actual_ieccp:.4f}"


# ---------- Test 3: Scale precision across MX/US/AU mix ----------

@pytest.mark.skip(reason="v1.1 Slim pivot (Phase 6.1.6, 2026-04-23): uses v1 fixture pattern; re-enable in 6.1.8 with v1.1 Slim fixtures.")
def test_scale_precision_no_silent_loss(monkeypatch):
    """Very different CCP scales (MX $97, US $412) with 10k+ regs each market —
    assert precision preserved in ie%CCP numerator and denominator.
    """
    fixtures = {
        'US': _tuned_params(50.0, 30.0, brand_ccp=412.51, nb_ccp=48.52, brand_share=0.274),
        'CA': _tuned_params(50.0, 30.0, brand_ccp=203.77, nb_ccp=38.52, brand_share=0.30),
    }

    def fake_load(market: str) -> dict:
        return fixtures[market]

    monkeypatch.setattr(engine, 'load_parameters', fake_load)
    monkeypatch.setattr(engine, 'check_parameter_readiness', lambda m, p: [])
    monkeypatch.setattr(engine, '_db', lambda: _FakeCon())

    inputs = ProjectionInputs(
        scope='NA',
        time_period='W01',
        target_mode='spend',
        target_value=10_000_000.0,   # $5M each — large numbers to stress precision
    )
    out = project(inputs)
    assert out.outcome == 'OK'

    # Manually compute expected from constituent markets to check regional math
    exp_total_regs = sum(c['brand_regs'] + c['nb_regs'] for c in out.constituent_markets)
    exp_total_spend = sum(c['total_spend'] for c in out.constituent_markets)

    exp_denom = 0.0
    for c in out.constituent_markets:
        f = fixtures[c['market']]
        exp_denom += c['brand_regs'] * f['brand_ccp']['value_scalar']
        exp_denom += c['nb_regs'] * f['nb_ccp']['value_scalar']

    exp_ieccp = exp_total_spend / exp_denom * 100.0

    # Match within 1e-6 relative tolerance — any larger is a precision bug
    assert math.isclose(out.totals['total_regs'], exp_total_regs, rel_tol=1e-6)
    assert math.isclose(out.totals['total_spend'], exp_total_spend, rel_tol=1e-6)
    assert math.isclose(out.totals['ieccp'], exp_ieccp, rel_tol=1e-6), \
        f"Scale precision loss: expected {exp_ieccp:.8f}, got {out.totals['ieccp']:.8f}"


# ---------- Test helpers ----------

class _FakeCon:
    """Stand-in for DuckDB connection — short-circuits _db-using extrapolation check."""
    def execute(self, sql, params=None):
        return self

    def fetchone(self):
        # historical max weekly spend — return a big number so HIGH_EXTRAPOLATION
        # doesn't fire in the test (we care about the math, not the warning)
        return (1_000_000_000.0,)

    def fetchall(self):
        return []
