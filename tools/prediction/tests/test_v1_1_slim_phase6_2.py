"""
Phase 6.2.6 regression test — 10 markets + 3 regions stable output fixture.

Compares current engine output to the baseline fixture within ±1% tolerance.
When this fails:
  - If the engine changed intentionally: regenerate the fixture
    (`python3 prediction/tests/fixtures/phase6_2_stable_output_generator.py`)
  - If you didn't mean to change anything: something drifted; investigate.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from prediction.mpe_engine import ProjectionInputs, project


FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "phase6_2_stable_output.json"

TOLERANCE_PCT = 0.01  # 1%


@pytest.fixture(scope="module")
def baseline():
    if not FIXTURE_PATH.exists():
        pytest.skip(f"Fixture not found at {FIXTURE_PATH}; generate with the fixture generator")
    return json.loads(FIXTURE_PATH.read_text())


@pytest.mark.parametrize("market", ["MX", "US", "CA", "UK", "DE", "FR", "IT", "ES", "JP", "AU"])
def test_market_stable_output_within_1pct(market, baseline):
    """Each of 10 markets produces output within 1% of the baseline fixture."""
    expected = baseline["per_market"][market]
    target_mode = expected["target_mode"]
    target_value = expected["target_value"]

    inputs = ProjectionInputs(
        scope=market, time_period="Y2026",
        target_mode=target_mode, target_value=target_value,
    )
    out = project(inputs)
    assert out.outcome == expected["outcome"], (
        f"{market} outcome: expected {expected['outcome']}, got {out.outcome} · "
        f"warnings={out.warnings[:3]}"
    )

    def _close(actual, expected_val, label):
        if expected_val is None:
            assert actual is None, f"{market} {label}: expected None, got {actual}"
            return
        if expected_val == 0:
            assert abs(actual) < 1, f"{market} {label}: expected 0, got {actual}"
            return
        delta = abs(actual - expected_val) / abs(expected_val)
        assert delta < TOLERANCE_PCT, (
            f"{market} {label}: actual={actual:.2f} vs expected={expected_val:.2f} "
            f"(delta={delta*100:.2f}% exceeds {TOLERANCE_PCT*100:.0f}%)"
        )

    _close(out.totals.get("total_regs", 0), expected["total_regs"], "total_regs")
    _close(out.totals.get("total_spend", 0), expected["total_spend"], "total_spend")
    _close(out.totals.get("brand_regs", 0), expected["brand_regs"], "brand_regs")
    _close(out.totals.get("nb_regs", 0), expected["nb_regs"], "nb_regs")
    if expected.get("ieccp") is not None:
        _close(out.totals.get("ieccp"), expected["ieccp"], "ieccp")


@pytest.mark.parametrize("region", ["NA", "EU5", "WW"])
def test_region_stable_output_within_1pct(region, baseline):
    """Each of 3 regions produces output within 1% of the baseline fixture."""
    expected = baseline["per_region"][region]
    target_mode = expected["target_mode"]
    target_value = expected["target_value"]

    inputs = ProjectionInputs(
        scope=region, time_period="Y2026",
        target_mode=target_mode, target_value=target_value,
    )
    out = project(inputs)
    assert out.outcome == expected["outcome"]

    def _close(actual, expected_val, label):
        if expected_val == 0:
            assert abs(actual) < 1, f"{region} {label}: expected 0, got {actual}"
            return
        delta = abs(actual - expected_val) / abs(expected_val)
        assert delta < TOLERANCE_PCT, (
            f"{region} {label}: actual={actual:.2f} vs expected={expected_val:.2f} "
            f"(delta={delta*100:.2f}%)"
        )

    _close(out.totals.get("total_regs", 0), expected["total_regs"], "total_regs")
    _close(out.totals.get("total_spend", 0), expected["total_spend"], "total_spend")
    assert len(out.constituent_markets) == expected["n_constituent_markets"], (
        f"{region} constituent_markets count: expected {expected['n_constituent_markets']}, "
        f"got {len(out.constituent_markets)}"
    )
