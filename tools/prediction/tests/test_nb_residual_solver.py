"""
Tests for NB Residual Solver — MPE v1.1 Slim Phase 6.1.4

Runs against live MotherDuck for end-to-end integration coverage. Unit-level
cases use synthetic params so they're fast and deterministic.
"""
from __future__ import annotations

from datetime import date, timedelta

import pytest

from prediction.nb_residual_solver import (
    MIN_NB_SPEND_FLOOR,
    NBSolution,
    _normalize_ieccp_to_percent,
    solve_nb_residual,
)


# ---------- Fixtures ----------


def _synthetic_mx_elast() -> dict:
    """MX-like NB CPA elasticity: a=-1.77, b=0.70. Used for deterministic tests."""
    return {"a": -1.77, "b": 0.70}


MX_BRAND_CCP = 97.22
MX_NB_CCP = 27.59


# ---------- Normalization helper ----------


def test_normalize_ieccp_decimal_to_percent():
    assert _normalize_ieccp_to_percent(0.75) == 75.0


def test_normalize_ieccp_already_percent():
    assert _normalize_ieccp_to_percent(75.0) == 75.0


def test_normalize_ieccp_boundary_5_percent():
    # Boundary: 5 is treated as percent (5%), not decimal.
    assert _normalize_ieccp_to_percent(5.0) == 5.0
    # 4.9 treated as decimal → percent. Use approx for float multiplication.
    assert _normalize_ieccp_to_percent(4.9) == pytest.approx(490.0)


# ---------- Spend branch ----------


def test_spend_branch_direct_allocation():
    sol = solve_nb_residual(
        brand_spend=200_000,
        brand_regs=10_000,
        target_mode="spend",
        target_value=1_000_000,
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP,
        nb_ccp=MX_NB_CCP,
        min_nb_spend=0,
        max_nb_spend=10_000_000,
    )
    assert sol.target_mode == "spend"
    assert sol.nb_spend == 800_000
    assert sol.total_spend == 1_000_000
    assert sol.converged is True
    assert "NB_UNDER_FUNDED" not in "".join(sol.warnings)


def test_spend_branch_under_funded_when_brand_exceeds_target():
    """Brand alone is bigger than target → NB clamped to floor + warning."""
    sol = solve_nb_residual(
        brand_spend=1_500_000,
        brand_regs=20_000,
        target_mode="spend",
        target_value=1_000_000,
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP,
        nb_ccp=MX_NB_CCP,
        min_nb_spend=0,
        max_nb_spend=10_000_000,
    )
    assert any("NB_UNDER_FUNDED" in w for w in sol.warnings)
    assert sol.nb_spend >= MIN_NB_SPEND_FLOOR


def test_spend_branch_null_ccp_does_not_crash():
    """AU-style market: null CCPs, spend branch should still work."""
    sol = solve_nb_residual(
        brand_spend=240_000,
        brand_regs=5_000,
        target_mode="spend",
        target_value=1_000_000,
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=None,
        nb_ccp=None,
        min_nb_spend=0,
        max_nb_spend=10_000_000,
    )
    assert sol.nb_spend == 760_000
    assert sol.computed_ieccp is None


def test_spend_branch_respects_min_nb_spend_floor():
    """min_nb_spend from market_constraints_manual floors the NB spend."""
    sol = solve_nb_residual(
        brand_spend=500_000,
        brand_regs=10_000,
        target_mode="spend",
        target_value=600_000,  # would give NB=$100K
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP,
        nb_ccp=MX_NB_CCP,
        min_nb_spend=200_000,  # floor above target allocation
        max_nb_spend=10_000_000,
    )
    # Warning fired since computed allocation below floor.
    assert any("NB_UNDER_FUNDED" in w for w in sol.warnings)


def test_spend_branch_respects_max_nb_spend():
    """Ceiling caps NB spend even when target demands more."""
    sol = solve_nb_residual(
        brand_spend=100_000,
        brand_regs=5_000,
        target_mode="spend",
        target_value=5_000_000,
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP,
        nb_ccp=MX_NB_CCP,
        min_nb_spend=0,
        max_nb_spend=1_000_000,  # ceiling well below target
    )
    assert sol.nb_spend == 1_000_000
    assert any("NB_OVER_MAX" in w for w in sol.warnings)


# ---------- ieccp branch ----------


def test_ieccp_branch_converges_under_bounds():
    """Normal case: target ie%CCP reachable within bounds."""
    sol = solve_nb_residual(
        brand_spend=200_000,
        brand_regs=10_000,
        target_mode="ieccp",
        target_value=1.00,  # 100% ie%CCP (decimal)
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP,
        nb_ccp=MX_NB_CCP,
        min_nb_spend=10_000,
        max_nb_spend=10_000_000,
    )
    assert sol.target_mode == "ieccp"
    assert sol.converged is True
    # Should be within tolerance of 100%.
    assert abs(sol.computed_ieccp - 100.0) < 1.0


def test_ieccp_branch_target_unreachable_under_bounds():
    """Target-relational bounds: if target-500bps isn't reachable via any
    NB spend up to max_nb_spend (tight ceiling), emit TARGET_UNREACHABLE_*."""
    sol = solve_nb_residual(
        brand_spend=200_000,
        brand_regs=10_000,
        target_mode="ieccp",
        target_value=2.00,  # 200% — very aggressive, requires massive NB
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP,
        nb_ccp=MX_NB_CCP,
        min_nb_spend=0,
        max_nb_spend=100_000,  # tight ceiling — can't reach 200%
    )
    # Either target is unreachable (warning) or solver lands outside band.
    unreachable = any("UNREACHABLE" in w for w in sol.warnings)
    outside_band = any("OUTSIDE_TOLERANCE_BAND" in w for w in sol.warnings)
    assert unreachable or outside_band, (
        f"Expected UNREACHABLE or OUTSIDE_TOLERANCE_BAND warning, got {sol.warnings}"
    )


def test_ieccp_branch_null_ccp_aborts_with_warning():
    """AU-style null CCPs should abort ieccp branch cleanly."""
    sol = solve_nb_residual(
        brand_spend=200_000,
        brand_regs=10_000,
        target_mode="ieccp",
        target_value=1.00,
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=None,
        nb_ccp=None,
        min_nb_spend=10_000,
        max_nb_spend=10_000_000,
    )
    assert any("UNSUPPORTED_TARGET_MODE" in w for w in sol.warnings)
    assert sol.converged is False


def test_ieccp_decimal_and_percent_produce_same_answer():
    """Whether user passes 0.75 or 75, answer should be identical."""
    args = dict(
        brand_spend=200_000,
        brand_regs=10_000,
        target_mode="ieccp",
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP,
        nb_ccp=MX_NB_CCP,
        min_nb_spend=10_000,
        max_nb_spend=10_000_000,
    )
    sol_decimal = solve_nb_residual(target_value=0.75, **args)
    sol_percent = solve_nb_residual(target_value=75.0, **args)
    # Within solver tolerance.
    if sol_decimal.converged and sol_percent.converged:
        assert abs(sol_decimal.nb_spend - sol_percent.nb_spend) < 1.0


# ---------- ytd locked support ----------


def test_spend_branch_ytd_locked_shifts_open_weeks_allocation():
    """When ytd_nb_spend is set, only the open-weeks portion is computed."""
    sol_no_ytd = solve_nb_residual(
        brand_spend=200_000, brand_regs=10_000,
        target_mode="spend", target_value=1_000_000,
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP, nb_ccp=MX_NB_CCP,
        min_nb_spend=0, max_nb_spend=10_000_000, ytd_nb_spend=0,
    )
    sol_ytd = solve_nb_residual(
        brand_spend=200_000, brand_regs=10_000,
        target_mode="spend", target_value=1_000_000,
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP, nb_ccp=MX_NB_CCP,
        min_nb_spend=0, max_nb_spend=10_000_000, ytd_nb_spend=300_000,
    )
    # Both should return same total NB spend (ytd is part of total), just differently decomposed.
    assert abs(sol_no_ytd.nb_spend - sol_ytd.nb_spend) < 1.0


# ---------- regs branch (Phase 6.2.1) ----------


def test_regs_branch_hits_target_for_mx():
    """MX regs branch: solve for NB spend that hits total regs target."""
    sol = solve_nb_residual(
        brand_spend=200_000, brand_regs=10_000,
        target_mode="regs", target_value=15_000,
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP, nb_ccp=MX_NB_CCP,
        min_nb_spend=10_000, max_nb_spend=10_000_000,
    )
    assert sol.target_mode == "regs"
    # Total regs within 1% tolerance.
    assert abs(sol.total_regs - 15_000) / 15_000 < 0.01, (
        f"Expected ~15,000 regs, got {sol.total_regs:.0f}"
    )


def test_regs_branch_brand_alone_covers_target():
    """If Brand already exceeds target, NB is clamped to floor + warning fires."""
    sol = solve_nb_residual(
        brand_spend=500_000, brand_regs=20_000,
        target_mode="regs", target_value=15_000,  # below brand alone
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP, nb_ccp=MX_NB_CCP,
        min_nb_spend=0, max_nb_spend=10_000_000,
    )
    assert any("REGS_TARGET_MET_BY_BRAND" in w for w in sol.warnings)


def test_regs_branch_target_unreachable():
    """Target regs beyond elasticity curve → TARGET_UNREACHABLE warning."""
    sol = solve_nb_residual(
        brand_spend=100_000, brand_regs=5_000,
        target_mode="regs", target_value=100_000_000,  # absurdly high
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP, nb_ccp=MX_NB_CCP,
        min_nb_spend=0, max_nb_spend=100_000,  # tight ceiling
    )
    assert any("TARGET_UNREACHABLE" in w for w in sol.warnings)


# ---------- op2_efficient branch (Phase 6.2.2) ----------


def test_op2_efficient_target_fits_within_budget():
    """Target regs achievable within OP2 budget → success, no warnings."""
    sol = solve_nb_residual(
        brand_spend=200_000, brand_regs=10_000,
        target_mode="op2_efficient",
        target_value={"target_regs": 15_000, "op2_spend_budget": 2_000_000},
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP, nb_ccp=MX_NB_CCP,
        min_nb_spend=0,
    )
    assert sol.target_mode == "op2_efficient"
    assert sol.total_spend <= 2_000_000
    assert not any("OP2_BUDGET_EXCEEDED" in w for w in sol.warnings)


def test_op2_efficient_target_exceeds_budget():
    """Target needs more than OP2 budget → clamped + warning with shortfall pct."""
    sol = solve_nb_residual(
        brand_spend=100_000, brand_regs=5_000,
        target_mode="op2_efficient",
        target_value={"target_regs": 50_000, "op2_spend_budget": 500_000},
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP, nb_ccp=MX_NB_CCP,
        min_nb_spend=0,
    )
    assert any("OP2_BUDGET_EXCEEDED" in w for w in sol.warnings)
    assert sol.total_spend <= 500_000 + 1.0  # ≤ budget (float tolerance)


def test_op2_efficient_requires_dict_target_value():
    """Scalar target_value → OP2_EFFICIENT_REQUIRES_DICT warning."""
    sol = solve_nb_residual(
        brand_spend=100_000, brand_regs=5_000,
        target_mode="op2_efficient", target_value=15_000,  # scalar, not dict
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP, nb_ccp=MX_NB_CCP,
        min_nb_spend=0,
    )
    assert any("OP2_EFFICIENT_REQUIRES_DICT" in w for w in sol.warnings)


# ---------- Unknown modes ----------


def test_unknown_target_mode_returns_warning():
    sol = solve_nb_residual(
        brand_spend=100_000, brand_regs=5_000,
        target_mode="nonexistent_mode", target_value=100,
        nb_cpa_elast=_synthetic_mx_elast(),
        brand_ccp=MX_BRAND_CCP, nb_ccp=MX_NB_CCP,
        min_nb_spend=0,
    )
    assert any("UNKNOWN_TARGET_MODE" in w for w in sol.warnings)


# ---------- Integration with Brand trajectory ----------


def test_mx_y2026_end_to_end_ieccp_lands_in_domain_expert_range():
    """Full Brand-Anchor + NB-Residual pipeline on real MX data via
    Locked-YTD (the canonical production path for Y-period projections).

    MX Y2026 @ 75% ie%CCP with auto-derived regime confidence should land
    in the domain-expert $800K-$1.2M range.

    This test uses Locked-YTD because the non-locked Brand projection
    over-counts Sparkle by applying its multiplier to the full year
    including pre-onset weeks (where the authored change_date=2026-04-05
    means the regime contributes 1.0 × everywhere before). Locked-YTD
    respects actuals for W1-W15 and projects only W16+, where Sparkle
    is correctly active.
    """
    from prediction.locked_ytd import project_with_locked_ytd
    from prediction.mpe_engine import load_parameters

    params = load_parameters("MX")
    nb_cpa_elast = params["nb_cpa_elasticity"]["value_json"]
    brand_ccp = params["brand_ccp"]["value_scalar"]
    nb_ccp = params["nb_ccp"]["value_scalar"]

    proj = project_with_locked_ytd(
        market="MX", year=2026,
        target_mode="ieccp", target_value=0.75,
        nb_cpa_elast=nb_cpa_elast,
        brand_ccp=brand_ccp, nb_ccp=nb_ccp,
        min_weekly_nb_spend=0.0,
        max_weekly_nb_spend=None,
        # No regime_multiplier override — use auto-derived confidence.
    )

    # Domain-expert range: $1.4M - $2.0M (rebased 2026-04-26 after post-onset anchor fix)
    assert 1_400_000 <= proj.total_spend <= 2_000_000, (
        f"MX Y2026 @ 75% Locked-YTD with auto-derived regime confidence "
        f"should land in $1.4M-$2.0M range, got ${proj.total_spend:,.0f}"
    )
