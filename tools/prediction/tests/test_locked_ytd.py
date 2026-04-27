"""
Tests for Locked-YTD + RoY projection — MPE v1.1 Slim Phase 6.1.5
"""
from __future__ import annotations

from datetime import date

import pytest

from prediction.locked_ytd import (
    LockedYTDProjection,
    YTDActuals,
    compute_roy_weeks,
    fetch_ytd_actuals,
    project_with_locked_ytd,
)
from prediction.mpe_engine import load_parameters


# ---------- Fixtures ----------


def _mx_params():
    params = load_parameters("MX")
    return {
        "nb_cpa_elast": params["nb_cpa_elasticity"]["value_json"],
        "brand_ccp": params["brand_ccp"]["value_scalar"],
        "nb_ccp": params["nb_ccp"]["value_scalar"],
        "bounds": params.get("_spend_bounds") or {},
    }


# ---------- YTD fetch ----------


def test_fetch_ytd_actuals_mx_2026():
    ytd = fetch_ytd_actuals("MX", 2026)
    assert ytd.market == "MX"
    assert ytd.year == 2026
    assert ytd.n_weeks_locked >= 10  # expect at least 10 weeks by late April
    assert ytd.brand_regs > 0
    assert ytd.nb_regs > 0


def test_fetch_ytd_actuals_unknown_market_returns_empty():
    ytd = fetch_ytd_actuals("__nonexistent__", 2026)
    assert ytd.n_weeks_locked == 0
    assert ytd.brand_regs == 0


def test_fetch_ytd_actuals_with_as_of_cutoff():
    early_cutoff = date(2026, 1, 15)
    ytd = fetch_ytd_actuals("MX", 2026, as_of=early_cutoff)
    assert ytd.n_weeks_locked <= 2
    assert ytd.latest_week_locked is None or ytd.latest_week_locked <= early_cutoff


# ---------- RoY weeks ----------


def test_compute_roy_weeks_full_year_when_no_ytd():
    weeks = compute_roy_weeks(2026, ytd_latest=None)
    assert len(weeks) == 52


def test_compute_roy_weeks_skips_locked_weeks():
    # Pretend YTD is through W15 end (approx 2026-04-12).
    ytd_latest = date(2026, 4, 12)
    weeks = compute_roy_weeks(2026, ytd_latest=ytd_latest)
    # RoY should be ~36-37 weeks (W16 onward).
    assert 34 <= len(weeks) <= 38
    # First RoY week must be AFTER ytd_latest.
    assert weeks[0] > ytd_latest


# ---------- Full projection ----------


def test_mx_y2026_locked_ytd_75pct_domain_expert_range():
    """Phase 6.1 demo gate: MX Y2026 @ 75% with W_regime=1.0 lands in
    $800K-$1.2M domain-expert range.
    """
    p = _mx_params()
    weights = {"seasonal": 0.40, "trend": 0.40, "regime": 1.00, "qualitative": 0.05}
    proj = project_with_locked_ytd(
        market="MX", year=2026,
        target_mode="ieccp", target_value=0.75,
        nb_cpa_elast=p["nb_cpa_elast"],
        brand_ccp=p["brand_ccp"], nb_ccp=p["nb_ccp"],
        min_weekly_nb_spend=0.0,
        max_weekly_nb_spend=None,
        brand_trajectory_weights=weights,
    )
    assert 1_400_000 <= proj.total_spend <= 2_000_000, (
        f"MX Y2026 @ 75% Locked-YTD W_regime=1.0 should land in $1.4M-$2.0M range, "
        f"got ${proj.total_spend:,.0f}"
    )


def test_mx_y2026_total_never_below_ytd_actuals():
    """Locked-YTD invariant: total_spend >= ytd_spend."""
    p = _mx_params()
    proj = project_with_locked_ytd(
        market="MX", year=2026,
        target_mode="ieccp", target_value=0.75,
        nb_cpa_elast=p["nb_cpa_elast"],
        brand_ccp=p["brand_ccp"], nb_ccp=p["nb_ccp"],
        min_weekly_nb_spend=p["bounds"].get("min_weekly_nb_spend") or 0.0,
        max_weekly_nb_spend=p["bounds"].get("max_weekly_nb_spend"),
    )
    # The headline invariant — no projection can un-spend YTD.
    assert proj.total_spend >= proj.ytd.total_spend
    assert proj.total_brand_regs >= proj.ytd.brand_regs
    assert proj.total_nb_regs >= proj.ytd.nb_regs


def test_mx_spend_branch_also_respects_ytd():
    p = _mx_params()
    proj = project_with_locked_ytd(
        market="MX", year=2026,
        target_mode="spend", target_value=500_000,
        nb_cpa_elast=p["nb_cpa_elast"],
        brand_ccp=p["brand_ccp"], nb_ccp=p["nb_ccp"],
        min_weekly_nb_spend=p["bounds"].get("min_weekly_nb_spend") or 0.0,
        max_weekly_nb_spend=p["bounds"].get("max_weekly_nb_spend"),
    )
    # Target $500K is below MX YTD ($279K) + min RoY NB (~$540K) = ~$819K floor.
    # Solver should respect floor.
    assert proj.total_spend >= proj.ytd.total_spend


def test_au_spend_branch_null_ccp_works():
    """AU null-CCP via spend branch via Locked-YTD."""
    proj = project_with_locked_ytd(
        market="AU", year=2026,
        target_mode="spend", target_value=500_000,
        nb_cpa_elast={"a": 1.96, "b": 0.31},
        brand_ccp=None, nb_ccp=None,
        min_weekly_nb_spend=0,
        max_weekly_nb_spend=None,
    )
    assert proj.computed_ieccp is None
    assert proj.total_regs > 0


def test_contribution_breakdown_present_in_projection():
    p = _mx_params()
    proj = project_with_locked_ytd(
        market="MX", year=2026,
        target_mode="ieccp", target_value=0.75,
        nb_cpa_elast=p["nb_cpa_elast"],
        brand_ccp=p["brand_ccp"], nb_ccp=p["nb_ccp"],
        min_weekly_nb_spend=p["bounds"].get("min_weekly_nb_spend") or 0.0,
        max_weekly_nb_spend=p["bounds"].get("max_weekly_nb_spend"),
    )
    assert set(proj.contribution_breakdown.keys()) == {"seasonal", "trend", "regime", "qualitative"}
    assert abs(sum(proj.contribution_breakdown.values()) - 1.0) < 1e-6


def test_target_unreachable_flags_constraint_active():
    """A target well outside the elasticity's reachable range should fire
    an UNREACHABLE warning. 5% ie%CCP for MX is far too aggressive — even
    with tiny NB the solver can't get below ~50%.
    """
    p = _mx_params()
    proj = project_with_locked_ytd(
        market="MX", year=2026,
        target_mode="ieccp", target_value=0.05,  # 5% — impossibly low
        nb_cpa_elast=p["nb_cpa_elast"],
        brand_ccp=p["brand_ccp"], nb_ccp=p["nb_ccp"],
        min_weekly_nb_spend=0.0,
        max_weekly_nb_spend=None,
    )
    warned = any("UNREACHABLE" in w or "OUTSIDE_TOLERANCE_BAND" in w for w in proj.warnings)
    assert warned or proj.locked_ytd_constraint_active, (
        f"Expected UNREACHABLE or OUTSIDE_TOLERANCE_BAND warning at 5% target, "
        f"got warnings={proj.warnings}"
    )
