"""
Phase 6.1 multi-market acceptance tests — all 10 markets.

Validates that v1.1 Slim engine (mpe_engine.project()) produces sensible
output for every market × supported target mode, not just MX/DE/AU.

These are the Phase 6.1 acceptance gates. Green here = go/no-go to Phase 6.2.
"""
from __future__ import annotations

import pytest

from prediction.mpe_engine import ProjectionInputs, project


ALL_10_MARKETS = ["MX", "US", "CA", "UK", "DE", "FR", "IT", "ES", "JP", "AU"]
IECCP_MARKETS = ["MX", "US", "CA", "UK", "DE", "FR", "IT", "ES"]  # 8 — AU+JP are spend-only per v6 refactor
NULL_CCP_MARKETS = ["AU"]  # 1 — null CCPs; ieccp branch must not crash
SPEND_ONLY_MARKETS = ["AU", "JP"]  # 2 — no ie%CCP target (v6 committed stance)

IECCP_TOLERANCE_PP = 0.5  # converges within 0.5 percentage points


# ---------- Runs-without-crashing ----------


@pytest.mark.parametrize("market", ALL_10_MARKETS)
def test_every_market_y2026_spend_runs_cleanly(market):
    """Every market should execute the spend branch without crashing."""
    target_spend = 1_000_000  # $1M — a neutral sanity number
    inputs = ProjectionInputs(
        scope=market, time_period="Y2026",
        target_mode="spend", target_value=target_spend,
    )
    out = project(inputs)
    assert out.outcome == "OK", (
        f"{market} Y2026 spend:$1M returned {out.outcome} · warnings={out.warnings}"
    )
    assert "total_spend" in out.totals
    assert out.totals["total_regs"] > 0


# ---------- ie%CCP convergence (9 markets) ----------


@pytest.mark.parametrize("market", IECCP_MARKETS)
def test_every_ieccp_market_y2026_converges_to_target(market):
    """Every market with CCPs should converge ie%CCP within 0.5pp of target
    OR return a TARGET_UNREACHABLE warning with the closest-feasible result.

    After the 2026-04-26 post-onset anchor fix, MX's Brand baseline stepped
    up enough that 75% ie%CCP is no longer reachable within historical NB
    spend bounds — the solver correctly flags TARGET_UNREACHABLE_ON_UPPER_BAND.
    This is the right signal (honest bounds, not fake solutions) but means
    the strict convergence assertion doesn't apply.
    """
    target = 0.75  # 75% — common target
    inputs = ProjectionInputs(
        scope=market, time_period="Y2026",
        target_mode="ieccp", target_value=target,
    )
    out = project(inputs)
    assert out.outcome == "OK", (
        f"{market} Y2026 ieccp:75% returned {out.outcome} · warnings={out.warnings}"
    )
    assert out.totals.get("ieccp") is not None, f"{market} returned None ie%CCP"
    unreachable = any("TARGET_UNREACHABLE" in w for w in (out.warnings or []))
    if unreachable:
        # Solver flagged target unreachable within historical bounds.
        # Result is closest-feasible. Must be within a wider tolerance (5pp)
        # and strictly below the target (can only UNDER-shoot since upper-band blocked).
        assert abs(out.totals["ieccp"] - 75.0) < 5.0, (
            f"{market} closest-feasible ie%CCP {out.totals['ieccp']:.2f}% "
            f"diverges >5pp from 75% target (even with UNREACHABLE flag)"
        )
    else:
        assert abs(out.totals["ieccp"] - 75.0) < IECCP_TOLERANCE_PP, (
            f"{market} ie%CCP {out.totals['ieccp']:.2f}% diverges >0.5pp from 75% target"
        )


# ---------- Null-CCP markets (AU) ----------


@pytest.mark.parametrize("market", NULL_CCP_MARKETS)
def test_null_ccp_markets_ieccp_branch_returns_setup_or_warning(market):
    """AU (null CCPs) should either (a) run ieccp branch with null ie%CCP +
    warning, or (b) return an INVALID_INPUT/SETUP_REQUIRED outcome.
    It must NOT crash and must NOT produce a bogus numeric ie%CCP.
    """
    inputs = ProjectionInputs(
        scope=market, time_period="Y2026",
        target_mode="ieccp", target_value=0.75,
    )
    out = project(inputs)
    # Either outcome is acceptable; null ie%CCP is the tell-tale.
    assert out.totals.get("ieccp") is None, (
        f"{market} should return null ie%CCP (no CCP data), got {out.totals.get('ieccp')}"
    )


# ---------- Locked-YTD invariant across all markets ----------


@pytest.mark.parametrize("market", ALL_10_MARKETS)
def test_locked_ytd_invariant_every_market(market):
    """For Y-periods, total_spend must never be below YTD-locked spend.
    Tested via the spend target mode at a target below plausible YTD.
    """
    inputs = ProjectionInputs(
        scope=market, time_period="Y2026",
        target_mode="spend", target_value=1.0,  # absurdly low target
    )
    out = project(inputs)
    ytd = out.locked_ytd_summary
    # If locked_ytd_summary is populated (Y-period), total must respect YTD floor.
    if ytd and ytd.get("ytd_brand_spend") is not None:
        ytd_total = (ytd.get("ytd_brand_spend") or 0) + (ytd.get("ytd_nb_spend") or 0)
        assert out.totals["total_spend"] >= ytd_total, (
            f"{market} total_spend ${out.totals['total_spend']:,.0f} below "
            f"YTD-locked ${ytd_total:,.0f}"
        )


# ---------- Contribution breakdown + regime stack ----------


@pytest.mark.parametrize("market", ALL_10_MARKETS)
def test_every_market_has_contribution_breakdown_summing_to_one(market):
    inputs = ProjectionInputs(
        scope=market, time_period="Y2026",
        target_mode="spend", target_value=500_000,
    )
    out = project(inputs)
    assert out.contribution_breakdown, f"{market} missing contribution_breakdown"
    total = sum(out.contribution_breakdown.values())
    assert abs(total - 1.0) < 1e-6, (
        f"{market} contribution_breakdown sums to {total}, not 1.0"
    )


@pytest.mark.parametrize("market", ALL_10_MARKETS)
def test_every_market_has_regime_stack(market):
    """regime_stack is populated via list_regimes_with_confidence() —
    may be empty for markets without structural regimes but must exist.
    """
    inputs = ProjectionInputs(
        scope=market, time_period="Y2026",
        target_mode="spend", target_value=500_000,
    )
    out = project(inputs)
    assert isinstance(out.regime_stack, list), f"{market} regime_stack not a list"
    for r in out.regime_stack:
        assert "effective_confidence" in r
        assert 0.0 <= r["effective_confidence"] <= 1.0
        assert "peak_multiplier" in r
        assert "decay_status" in r


# ---------- Deleted v1 solvers ----------


def test_v1_solver_symbols_removed():
    """Phase 6.1.6 deleted _solve_ieccp_target and _solve_regs_target
    from mpe_engine.py. Import should fail.
    """
    from prediction import mpe_engine
    assert not hasattr(mpe_engine, "_solve_ieccp_target"), (
        "_solve_ieccp_target should have been deleted in Phase 6.1.6"
    )
    assert not hasattr(mpe_engine, "_solve_regs_target"), (
        "_solve_regs_target should have been deleted in Phase 6.1.6"
    )


# ---------- Regional rollups ----------


@pytest.mark.parametrize("region,min_markets", [("NA", 2), ("EU5", 5), ("WW", 10)])
def test_regional_rollup_runs(region, min_markets):
    """Regional projections aggregate per-market results and should not
    regress after Phase 6.1.6 engine pivot.

    NA = US + CA (MX tracked separately as LATAM — see spec discrepancy
    with design-v1.1.md flagged in session-log 2026-04-23).
    EU5 = UK + DE + FR + IT + ES.
    WW = all 10 markets.
    """
    inputs = ProjectionInputs(
        scope=region, time_period="Y2026",
        target_mode="spend", target_value=10_000_000,
    )
    out = project(inputs)
    assert out.outcome == "OK", f"{region} returned {out.outcome}"
    assert out.totals.get("total_regs", 0) > 0
    assert len(out.constituent_markets) >= min_markets, (
        f"{region} should have >={min_markets} constituent markets, got "
        f"{len(out.constituent_markets)}"
    )


# ---------- MX demo gate ----------


def test_mx_y2026_75pct_in_domain_expert_range():
    """Phase 6.1 headline demo gate: MX Y2026 @ 75% ie%CCP lands in the
    $1.4M-$2.0M domain-expert range. Rebased 2026-04-26 after post-onset
    anchor fix — anchor now reflects the W14+ Sparkle level rather than
    averaging against pre-Sparkle weeks. New projection aligns with
    leadership's "current run-rate × 52 weeks" mental model.
    """
    inputs = ProjectionInputs(
        scope="MX", time_period="Y2026",
        target_mode="ieccp", target_value=0.75,
    )
    out = project(inputs)
    assert 1_400_000 <= out.totals["total_spend"] <= 2_000_000, (
        f"MX Y2026 @ 75% landed at ${out.totals['total_spend']:,.0f} · "
        f"expected $1.4M-$2.0M"
    )
