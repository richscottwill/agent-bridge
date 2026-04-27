"""Test the qualitative priors YAML loader + engine translation (Phase 6.5.1)."""
from __future__ import annotations

from prediction.qualitative_priors import (
    load_catalog,
    list_scenarios_for_market,
    get_scenario,
    scenario_to_engine_override,
    w_qualitative_for,
)


def test_catalog_loads():
    cat = load_catalog(force_reload=True)
    assert "scenarios" in cat
    assert len(cat["scenarios"]) >= 7, f"expected ≥7 scenarios catalogued, got {len(cat['scenarios'])}"


def test_current_regime_continues_is_default():
    s = get_scenario("current_regime_continues")
    assert s is not None
    override = scenario_to_engine_override(s)
    assert override is None, "default 'current_regime_continues' should produce no override"


def test_sparkle_scenarios_mx_only():
    mx = list_scenarios_for_market("MX")
    us = list_scenarios_for_market("US")
    mx_names = {s["name"] for s in mx}
    us_names = {s["name"] for s in us}
    assert "sparkle_sustained" in mx_names
    assert "sparkle_decays_26w" in mx_names
    assert "sparkle_sustained" not in us_names
    assert "current_regime_continues" in us_names   # universal


def test_sparkle_sustained_translates_to_permanent():
    s = get_scenario("sparkle_sustained")
    o = scenario_to_engine_override(s)
    assert o["half_life_weeks"] is None
    assert o["force_confidence"] == 1.0


def test_sparkle_decays_26w_has_correct_half_life():
    s = get_scenario("sparkle_decays_26w")
    o = scenario_to_engine_override(s)
    assert o["half_life_weeks"] == 26


def test_polaris_retained_skips_regime():
    s = get_scenario("polaris_retained")
    assert s is not None
    assert "AU" in s["applicable_markets"]
    o = scenario_to_engine_override(s)
    assert o["peak_multiplier"] == 1.0


def test_w_qualitative_default_and_override():
    assert w_qualitative_for("current_regime_continues") == 0.00   # baseline
    assert w_qualitative_for("sparkle_decays_26w") == 0.20         # explicit
    assert w_qualitative_for("unknown_scenario") == 0.05           # not in catalog
