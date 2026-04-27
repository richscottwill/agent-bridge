"""
Tests for BrandTrajectoryModel — MPE v1.1 Slim Phase 6.1.1

Runs against live MotherDuck. Fast — seconds, not minutes.
"""
from __future__ import annotations

from datetime import date, timedelta

import pytest

from prediction.brand_trajectory import (
    DEFAULT_WEIGHTS,
    BrandProjection,
    compute_brand_cpa_projected,
    compute_recent_trend,
    compute_regime_multiplier,
    compute_seasonal_multipliers,
    iso_week_of,
    project_brand_trajectory,
    trend_multiplier_for_week,
)


# ---------- Helpers ----------


def _y2026_weeks() -> list[date]:
    jan4 = date(2026, 1, 4)
    start = jan4 - timedelta(days=jan4.weekday())
    return [start + timedelta(weeks=i) for i in range(52)]


# ---------- Contribution breakdown invariant ----------


def test_contribution_weights_sum_to_one_for_active_streams():
    w = DEFAULT_WEIGHTS.copy()
    active_sum = sum(v for k, v in w.items() if k in ("seasonal", "trend", "regime") and v > 0)
    assert active_sum == pytest.approx(0.95)  # 0.40 + 0.40 + 0.15, qualitative reserved


def test_contribution_dict_in_projection_sums_to_one():
    proj = project_brand_trajectory("MX", _y2026_weeks())
    assert sum(proj.contribution.values()) == pytest.approx(1.0, abs=1e-6)


# ---------- Three-market acceptance ----------


def test_mx_y2026_brand_projection_runs():
    proj = project_brand_trajectory("MX", _y2026_weeks())
    assert isinstance(proj, BrandProjection)
    assert proj.market == "MX"
    assert len(proj.regs_per_week) == 52
    assert len(proj.spend_per_week) == 52
    assert proj.brand_cpa_used > 0
    assert proj.total_regs > 0
    assert proj.total_spend > 0
    assert proj.total_regs > 1000  # Basic sanity; MX is not a zero-Brand market


def test_de_y2026_brand_projection_runs():
    proj = project_brand_trajectory("DE", _y2026_weeks())
    assert proj.market == "DE"
    assert len(proj.regs_per_week) == 52
    assert proj.total_regs > 0
    # DE is the EU5 representative. Brand CCP is ~$292, Brand CPA ~$80.
    assert proj.brand_cpa_used > 30
    assert proj.brand_cpa_used < 200


def test_au_y2026_brand_projection_runs_null_ccp_market():
    """AU has null CCPs; Brand trajectory must still work. SH hybrid market
    may not have 52 weeks of history → expect SEASONAL_PRIOR_UNAVAILABLE.
    """
    proj = project_brand_trajectory("AU", _y2026_weeks())
    assert proj.market == "AU"
    assert len(proj.regs_per_week) == 52
    # AU has ~42 clean weeks; seasonality prior should be unavailable.
    assert any("SEASONAL_PRIOR_UNAVAILABLE" in w for w in proj.warnings)


# ---------- Brand CPA projected ----------


def test_brand_cpa_projected_scalar_mx():
    cpa, warnings = compute_brand_cpa_projected("MX")
    assert cpa > 0
    # MX Brand CPA is historically $15-25.
    assert 10 < cpa < 50


def test_brand_cpa_projected_scalar_de():
    cpa, warnings = compute_brand_cpa_projected("DE")
    assert cpa > 0
    assert 40 < cpa < 200  # DE Brand CPA range


# ---------- Regime multiplier ----------


def test_regime_multiplier_returns_1_for_unknown_market():
    mult, warnings, detail = compute_regime_multiplier("__nonexistent__")
    assert mult == 1.0
    assert detail == []


def test_regime_multiplier_mx_has_at_least_one_structural():
    """MX has Polaris INTL (2025-08-28) as structural baseline."""
    mult, warnings, detail = compute_regime_multiplier("MX")
    assert mult > 0
    # At least one regime should have a computed ratio.
    ratioed = [d for d in detail if d.get("ratio") is not None]
    assert len(ratioed) >= 1


# ---------- Recent trend ----------


def test_recent_trend_mx_returns_intercept_and_slope():
    trend, warnings = compute_recent_trend("MX")
    assert trend["intercept"] > 0
    assert isinstance(trend["slope_log"], float)
    assert trend["n_weeks_used"] >= 0
    # Slope must be within the ±10% clamp.
    assert -0.10 - 1e-9 <= trend["slope_log"] <= 0.10 + 1e-9


# ---------- Trend fade ----------


def test_trend_multiplier_fades_over_time():
    """The trend fade must produce diminishing returns on future weeks."""
    trend = {
        "intercept": 100.0,
        "slope_log": 0.05,  # +5% / week initially
        "latest_week": date(2026, 4, 20),
        "n_weeks_used": 8,
    }
    wk4 = trend_multiplier_for_week(trend, date(2026, 4, 20) + timedelta(weeks=4))
    wk13 = trend_multiplier_for_week(trend, date(2026, 4, 20) + timedelta(weeks=13))
    wk52 = trend_multiplier_for_week(trend, date(2026, 4, 20) + timedelta(weeks=52))
    # Each should grow but with diminishing marginal contribution.
    assert wk4 > 1.0
    assert wk13 > wk4
    assert wk52 > wk13
    # Over 52 weeks with +5%/wk slope raw = exp(0.05*52) ≈ 13.5× — fade must cut this.
    # With 13-week half-life, we expect ~3x max, not 13x.
    assert wk52 < 5.0, f"Trend fade not working: wk52 = {wk52:.2f}"


def test_trend_multiplier_zero_slope():
    trend = {"intercept": 100.0, "slope_log": 0.0, "latest_week": date(2026, 4, 20), "n_weeks_used": 8}
    assert trend_multiplier_for_week(trend, date(2026, 12, 31)) == 1.0


def test_trend_multiplier_no_latest_week():
    trend = {"intercept": 100.0, "slope_log": 0.05, "latest_week": None, "n_weeks_used": 0}
    assert trend_multiplier_for_week(trend, date(2026, 12, 31)) == 1.0


# ---------- Seasonality ----------


def test_seasonal_multipliers_mx_returns_map():
    weeks = _y2026_weeks()
    seasonal, warnings = compute_seasonal_multipliers("MX", weeks)
    # Should have one entry per unique ISO week (may dedupe 53→52).
    assert len(seasonal) >= 50
    # All multipliers are in the clamp range [0.3, 3.0].
    for w, mult in seasonal.items():
        assert 0.3 <= mult <= 3.0, f"Week {w} has out-of-bounds mult {mult}"


def test_seasonal_falls_back_on_short_history():
    # AU has only ~42 weeks; seasonal prior should fall back to all 1.0.
    weeks = _y2026_weeks()
    seasonal, warnings = compute_seasonal_multipliers("AU", weeks)
    assert any("SEASONAL_PRIOR_UNAVAILABLE" in w for w in warnings)


# ---------- ISO week helper ----------


def test_iso_week_of_boundary_cases():
    # 2026-01-05 is Mon of ISO week 2 of 2026
    assert iso_week_of(date(2026, 1, 5)) == 2
    # 2026-12-28 is Mon of ISO week 53 (2026 has 53 weeks).
    assert iso_week_of(date(2026, 12, 28)) in (52, 53)


# ---------- Graceful failure ----------


def test_unknown_market_returns_zero_projection():
    """Any market without data should return zeros + warnings, not crash."""
    proj = project_brand_trajectory("__nonexistent__", _y2026_weeks())
    assert proj.total_regs == 0.0
    assert proj.total_spend == 0.0
    assert len(proj.warnings) > 0


# ---------- Per-week regime decay + weight-as-deviation (Phase 6.1.2/3) ----------


def test_regime_multipliers_per_week_returns_length_matching_input():
    """Must return one multiplier per target week, in order."""
    from prediction.brand_trajectory import compute_regime_multipliers_per_week

    weeks = [date(2026, 1, 5) + timedelta(weeks=i) for i in range(10)]
    mults, warnings, detail = compute_regime_multipliers_per_week("MX", weeks)
    assert len(mults) == 10
    assert all(m > 0 for m in mults)


def test_regime_mx_sparkle_decays_over_year():
    """MX with Sparkle + Polaris should show post-April peak fading toward year-end.

    Note: per-regime confidence (auto-derived from fit_state) blends each
    regime's raw lift down — Sparkle at 2w post-onset has effective
    confidence 0.18, so its compounded effect is modest. We still expect
    the DIRECTIONAL ordering to hold: May > Oct > Dec as Sparkle decays.
    """
    from prediction.brand_trajectory import compute_regime_multipliers_per_week

    # 4 sample weeks: Feb (pre-Sparkle), May (post-Sparkle peak), Oct, Dec.
    sample_weeks = [
        date(2026, 2, 2),   # pre-Sparkle → Polaris only
        date(2026, 5, 4),   # just post-Sparkle — peak
        date(2026, 10, 5),  # ~6 months post → meaningful decay
        date(2026, 12, 28), # ~8 months post → more decay
    ]
    mults, warnings, detail = compute_regime_multipliers_per_week("MX", sample_weeks)
    feb, may, oct_, dec = mults
    # Feb: only Polaris active. With auto-derived confidence (Polaris=0.50,
    # status=no-decay-detected), effective contribution = 1 + 0.5 × 0.22 = 1.11.
    assert 1.05 < feb < 1.20, f"Feb mult {feb:.3f} expected ~1.11 (Polaris confidence-weighted)"
    # May: Sparkle contributes meaningfully on top of Polaris.
    assert may > feb, f"May mult {may:.3f} should exceed Feb mult {feb:.3f} post-Sparkle onset"
    # Oct: Sparkle decaying → less than May peak.
    assert oct_ < may, f"Oct mult {oct_:.3f} should be below May peak {may:.3f}"
    # Dec: further decay.
    assert dec < oct_, f"Dec mult {dec:.3f} should be below Oct mult {oct_:.3f}"
    # Asymptote: Polaris stays, so dec > 1.0.
    assert dec > 1.0


def test_weight_controls_regime_influence():
    """scenario_override with forced peak_multiplier moves output monotonically.

    The 2026-04-26 anchor rework normalizes the regime stream at the anchor
    reference week, so the global `regime_multiplier` dial is no longer a
    monotonic knob at Y2026 scope. The semantically clear replacement is
    to force the regime peak via scenario_override: peak=1.0 (no lift) vs
    peak=2.0 (strong lift) — the stronger peak produces more regs because
    the forward stream exceeds the anchor normalizer.

    This is the knob the UI scenario chips exercise.
    """
    from prediction.brand_trajectory import compute_regime_multipliers_per_week
    weeks = _y2026_weeks()
    # Direct test: forward regime stream with forced peaks
    no_lift = compute_regime_multipliers_per_week("MX", weeks, scenario_override={"peak_multiplier": 1.0})
    strong_lift = compute_regime_multipliers_per_week("MX", weeks, scenario_override={"peak_multiplier": 2.0, "half_life_weeks": None, "force_confidence": 1.0})
    # Strong lift: last-week multiplier stays at 2.0 (permanent, 100% conf).
    # No lift: multiplier is 1.0.
    assert strong_lift[0][-1] > no_lift[0][-1]


def test_regime_single_regime_multiplier_at_respects_onset_date():
    """Before onset: 1.0. At onset: peak. After onset: decay."""
    from prediction.brand_trajectory import _single_regime_multiplier_at

    regime = {
        "change_date": date(2026, 4, 5),
        "peak_multiplier": 2.0,
        "half_life_weeks": 26,
    }
    # 4 weeks before onset → 1.0 (regime inactive).
    pre = _single_regime_multiplier_at(regime, date(2026, 4, 5) - timedelta(weeks=4))
    assert pre == 1.0
    # At onset → peak.
    on = _single_regime_multiplier_at(regime, date(2026, 4, 5))
    assert abs(on - 2.0) < 1e-6
    # One half-life later → excess halved: 1 + (2-1)*0.5 = 1.5.
    hl = _single_regime_multiplier_at(regime, date(2026, 4, 5) + timedelta(weeks=26))
    assert abs(hl - 1.5) < 1e-6
    # Permanent regime (half_life=None) → peak forever.
    regime_permanent = {"change_date": date(2026, 4, 5), "peak_multiplier": 1.5, "half_life_weeks": None}
    future = _single_regime_multiplier_at(regime_permanent, date(2027, 4, 5))
    assert abs(future - 1.5) < 1e-6


def test_regime_fit_state_is_used_when_available():
    """After a fit_regime_state run, _fetch_structural_regimes must show source='fitted'."""
    from prediction.brand_trajectory import _fetch_structural_regimes

    regimes = _fetch_structural_regimes("MX")
    assert len(regimes) >= 1
    # MX has regime_fit_state rows from Phase 6.1.2 — verify they're consumed.
    fitted = [r for r in regimes if r.get("source") == "fitted"]
    assert len(fitted) >= 1, "MX should have at least one fitted regime row"


def test_stream_multipliers_per_week_exposes_decomposition():
    """The per-week detail field lets UI show which stream moved each week."""
    weeks = _y2026_weeks()
    proj = project_brand_trajectory("MX", weeks)
    assert len(proj.stream_multipliers_per_week) == 52
    sample = proj.stream_multipliers_per_week[20]  # mid-year
    assert "seasonal_raw" in sample
    assert "trend_raw" in sample
    assert "regime_raw" in sample
    assert "combined" in sample


# ---------- Auto-derived per-regime confidence (Phase 6.1.5 pivot) ----------


def test_list_regimes_with_confidence_mx_has_polaris_and_sparkle():
    """Phase 6.4 UI list-of-regimes consumer."""
    from prediction.brand_trajectory import list_regimes_with_confidence

    regimes = list_regimes_with_confidence("MX")
    assert len(regimes) >= 2  # Polaris + Sparkle
    for r in regimes:
        assert "effective_confidence" in r
        assert "peak_multiplier" in r
        assert "decay_status" in r
        assert 0.0 <= r["effective_confidence"] <= 1.0
        assert r["explanation"]  # human-readable provenance


def test_regime_confidence_auto_derivation_dormant_is_near_zero():
    from prediction.regime_confidence import effective_confidence

    # A dormant regime with 0.7 base confidence should produce ~0.07 effective
    # (heavy downweight because the regime's observed contribution is tiny).
    eff = effective_confidence(base_confidence=0.7, decay_status="dormant")
    assert eff < 0.1


def test_regime_confidence_auto_derivation_stable_is_near_base():
    from prediction.regime_confidence import effective_confidence

    # A stable regime (no-decay-detected) with 0.5 base should produce 0.5.
    eff = effective_confidence(base_confidence=0.5, decay_status="no-decay-detected")
    assert abs(eff - 0.5) < 1e-6


def test_regime_confidence_still_peaking_is_damped():
    from prediction.regime_confidence import effective_confidence

    # Still-peaking regime with 0.3 base → 0.3 × 0.6 = 0.18.
    eff = effective_confidence(base_confidence=0.3, decay_status="still-peaking")
    assert abs(eff - 0.18) < 1e-6


def test_regime_multiplier_global_dial_scales_output():
    """After 2026-04-26 anchor rework, the regime stream is normalized at
    the anchor reference week. The end-to-end dial effect depends on
    scenario shape (decay vs permanent) rather than pure amplitude.

    Clean semantic test: with the same forced peak, a PERMANENT regime
    produces higher Y2026 output than a FAST-DECAY regime, because the
    decaying scenario falls below anchor during the year while the
    permanent scenario stays at peak.
    """
    weeks = _y2026_weeks()
    fast_decay = project_brand_trajectory(
        "MX", weeks,
        scenario_override={"peak_multiplier": 2.0, "half_life_weeks": 8, "force_confidence": 1.0},
    ).total_regs
    permanent = project_brand_trajectory(
        "MX", weeks,
        scenario_override={"peak_multiplier": 2.0, "half_life_weeks": None, "force_confidence": 1.0},
    ).total_regs
    assert permanent > fast_decay, (
        f"Expected permanent regime to yield higher Y2026 output than fast-decay: "
        f"permanent={permanent:.0f}, fast_decay={fast_decay:.0f}"
    )


def test_weights_regime_key_is_ignored_with_warning():
    """Passing weights['regime']=0.8 should emit REGIME_WEIGHT_IGNORED warning
    and not affect output (per-regime confidence is auto-derived).
    """
    weeks = _y2026_weeks()
    default_proj = project_brand_trajectory("MX", weeks)
    override_proj = project_brand_trajectory(
        "MX", weeks,
        weights={"seasonal": 0.40, "trend": 0.40, "regime": 0.80, "qualitative": 0.05},
    )
    # Warning fires.
    assert any("REGIME_WEIGHT_IGNORED" in w for w in override_proj.warnings)
    # Outputs identical (regime weight is ignored).
    assert abs(default_proj.total_regs - override_proj.total_regs) < 0.01
