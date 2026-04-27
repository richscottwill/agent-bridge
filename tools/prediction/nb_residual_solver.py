"""
NB Residual Solver — MPE v1.1 Slim (Phase 6.1.4)

=============================================================================
WHAT THIS DOES (Plain English)
=============================================================================
    Given a Brand projection and a target constraint (ie%CCP, total regs,
    total spend, or OP2 efficiency), compute the NB spend that satisfies
    the constraint.

    This is the "NB is the lever" half of v1.1 Slim's architecture. Brand
    is projected independently (from its own fundamentals), then we solve
    for how much NB spend is needed to hit whatever target the user
    specified.

    Two branches ship in Phase 6.1:
      - `spend`  — direct subtraction. nb_spend = target_spend - brand_spend
      - `ieccp`  — root-finding on nb_spend such that blended ie%CCP hits target

    Two branches come in Phase 6.2:
      - `regs`          — root-finding on nb_spend such that brand_regs + nb_regs = target
      - `op2_efficient` — AU default; maximize regs under OP2 budget

=============================================================================
HOW IT WORKS
=============================================================================
    NB CPA elasticity (log-linear log(cpa) = a + b * log(spend)) is the
    closure equation — given a trial nb_spend, we compute nb_cpa and thus
    nb_regs. For ie%CCP branch:

        nb_cpa(s)      = exp(a) * s^b
        nb_regs(s)     = s / nb_cpa(s)
        total_spend    = brand_spend + s
        total_regs     = brand_regs + nb_regs(s)
        ieccp_denom    = brand_regs × brand_CCP + nb_regs(s) × nb_CCP
        computed_ieccp = total_spend / ieccp_denom

    Find s such that computed_ieccp == target_ieccp.

    Bounded search space comes from ps.market_constraints_manual (Mechanism A
    from 2026-04-23 — the retained v1 operational bounds):
        low  = min_weekly_nb_spend × open_weeks
        high = max_weekly_nb_spend × open_weeks

    Uses scipy.optimize.brentq when SciPy is available, else bisection.

    Locked-YTD floor: if the user passes `ytd_locked` with prior-period
    Brand + NB spend, we add `ytd_locked.total_nb_spend` to every computed
    nb_spend so the returned total always respects YTD actuals. Triggers
    LOCKED_YTD_CONSTRAINT_ACTIVE warning if the open-weeks solution would
    have gone below `min_weekly_nb_spend × open_weeks`.

=============================================================================
HOW IT CAN FAIL
=============================================================================
    1. Target unreachable under bounds → returns closest-feasible,
       TARGET_UNREACHABLE_UNDER_BOUNDS warning.
    2. Null CCPs (AU) on ieccp branch → UNSUPPORTED_TARGET_MODE warning,
       caller should route to spend branch instead.
    3. Zero brand projection → still solves; nb carries the whole load.
    4. Missing nb_cpa_elasticity param → NB_ELASTICITY_UNAVAILABLE, returns
       0 spend + 0 regs + warning.
    5. Search doesn't converge within max iterations → returns best attempt
       with SOLVER_NONCONVERGENCE warning.
=============================================================================
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from typing import Optional

# Reuse the existing NB CPA elasticity applier so solver math mirrors engine math.
from prediction.mpe_engine import _apply_cpa_elasticity
# ---------- Config ----------

SOLVER_MAX_ITERATIONS = 60
SOLVER_TOLERANCE_IECCP = 0.05  # percentage points on ie%CCP scale (e.g., 75.0 ± 0.05)
SOLVER_TOLERANCE_REGS = 0.005  # 0.5% relative tolerance on target_regs
MIN_NB_SPEND_FLOOR = 1_000.0   # dollars; can't go below this at any branch


# ---------- Result type ----------


@dataclass
class NBSolution:
    """Solver output: how much NB spend to hit the target, and the resulting
    NB regs, total_spend, total_regs, blended_cpa, ie%CCP.

    target_mode: the branch used
    target_value: the constraint value (same units as user passed)
    converged: True if solver hit tolerance, False if clamped by bounds
                or fell off the end of iterations
    """
    target_mode: str
    target_value: float
    nb_spend: float
    nb_regs: float
    nb_cpa: float
    brand_spend: float
    brand_regs: float
    total_spend: float
    total_regs: float
    blended_cpa: float
    computed_ieccp: Optional[float]  # percent scale (75.0 = 75%); None if CCPs missing
    converged: bool
    warnings: list[str] = field(default_factory=list)
    lineage: str = ""

    def to_json(self) -> dict:
        return {
            "target_mode": self.target_mode,
            "target_value": self.target_value,
            "nb_spend": self.nb_spend,
            "nb_regs": self.nb_regs,
            "nb_cpa": self.nb_cpa,
            "brand_spend": self.brand_spend,
            "brand_regs": self.brand_regs,
            "total_spend": self.total_spend,
            "total_regs": self.total_regs,
            "blended_cpa": self.blended_cpa,
            "computed_ieccp": self.computed_ieccp,
            "converged": self.converged,
            "warnings": self.warnings,
            "lineage": self.lineage,
        }


# ---------- Helpers ----------


def _nb_regs_from_annual_spend(
    annual_nb_spend: float,
    n_weeks: int,
    nb_cpa_elast: dict,
) -> tuple[float, float]:
    """Given an ANNUAL (or period total) NB spend and the number of weeks,
    compute annual NB regs + effective annual CPA.

    The elasticity fit `log(cpa) = a + b * log(spend)` is on WEEKLY data.
    We apply it at the per-week level (spend/n_weeks), compute per-week
    regs, then multiply back up. This matches how v1's engine applies
    elasticity in _project_market_spend_target.
    """
    if n_weeks <= 0 or annual_nb_spend <= 0:
        return 0.0, 0.0
    weekly_spend = annual_nb_spend / n_weeks
    weekly_cpa = _apply_cpa_elasticity(weekly_spend, nb_cpa_elast["a"], nb_cpa_elast["b"])
    weekly_regs = weekly_spend / weekly_cpa if weekly_cpa > 0 else 0.0
    annual_regs = weekly_regs * n_weeks
    return annual_regs, weekly_cpa


def _normalize_ieccp_to_percent(target: float) -> float:
    """User may pass 0.75 (decimal) or 75 (percent). Normalize to percent
    scale internally since _project_one_week returns ie%CCP as a percent.
    """
    return target * 100.0 if target is not None and target < 5.0 else target


def _compute_ieccp_percent(
    brand_regs: float, nb_regs: float,
    brand_spend: float, nb_spend: float,
    brand_ccp: float, nb_ccp: float,
) -> Optional[float]:
    """ie%CCP on the percent scale (75.0 = 75%). None if CCPs are missing."""
    if brand_ccp is None or nb_ccp is None:
        return None
    total_spend = brand_spend + nb_spend
    denom = brand_regs * brand_ccp + nb_regs * nb_ccp
    if denom <= 0:
        return None
    return (total_spend / denom) * 100.0


def _brent_or_bisect(
    f, low: float, high: float,
    tolerance: float, max_iterations: int,
):
    """Find x in [low, high] with f(x) ≈ 0.

    Try scipy.optimize.brentq first (faster convergence). If SciPy not
    available, fall back to bisection. Returns (x, converged) where
    converged indicates whether tolerance was hit.
    """
    try:
        from scipy.optimize import brentq
        # brentq requires sign change across the bracket. Test first.
        f_low = f(low)
        f_high = f(high)
        if f_low == 0:
            return low, True
        if f_high == 0:
            return high, True
        if f_low * f_high > 0:
            # No sign change — return whichever side is closer.
            return (low if abs(f_low) < abs(f_high) else high), False
        x = brentq(f, low, high, xtol=tolerance, maxiter=max_iterations)
        return float(x), True
    except (ImportError, ValueError):
        # Bisection fallback.
        pass

    f_low = f(low)
    for _ in range(max_iterations):
        mid = (low + high) / 2
        f_mid = f(mid)
        if abs(f_mid) < tolerance:
            return mid, True
        # Same sign as low means root is on the other side.
        if (f_low > 0) == (f_mid > 0):
            low = mid
            f_low = f_mid
        else:
            high = mid
    return (low + high) / 2, False


# ---------- Solver branches ----------


def _solve_spend_branch(
    target_spend: float,
    brand_spend: float,
    brand_regs: float,
    nb_cpa_elast: dict,
    brand_ccp: Optional[float],
    nb_ccp: Optional[float],
    min_nb_spend: float,
    max_nb_spend: Optional[float],
    ytd_nb_spend: float = 0.0,
    n_weeks: int = 52,
) -> NBSolution:
    """Direct: NB = target_spend - brand_spend - ytd_nb_spend (for open-weeks portion)."""
    warnings: list[str] = []

    # Naive direct allocation.
    nb_open_spend = target_spend - brand_spend - ytd_nb_spend
    if nb_open_spend < min_nb_spend:
        warnings.append(
            f"NB_UNDER_FUNDED: computed nb_open_spend ${nb_open_spend:,.0f} < floor ${min_nb_spend:,.0f}"
        )
        nb_open_spend = max(nb_open_spend, MIN_NB_SPEND_FLOOR)
    if max_nb_spend is not None and nb_open_spend > max_nb_spend:
        warnings.append(
            f"NB_OVER_MAX: computed nb_open_spend ${nb_open_spend:,.0f} > ceiling ${max_nb_spend:,.0f}; clamped"
        )
        nb_open_spend = max_nb_spend

    nb_total_spend = nb_open_spend + ytd_nb_spend
    # Per-week elasticity applied over n_weeks open weeks. Note: YTD is
    # included in total because we want the FULL-period elasticity response.
    nb_regs, nb_cpa = _nb_regs_from_annual_spend(nb_total_spend, n_weeks, nb_cpa_elast)

    total_spend = brand_spend + nb_total_spend
    total_regs = brand_regs + nb_regs
    blended_cpa = total_spend / total_regs if total_regs > 0 else 0.0
    ieccp = _compute_ieccp_percent(brand_regs, nb_regs, brand_spend, nb_total_spend, brand_ccp, nb_ccp)

    return NBSolution(
        target_mode="spend",
        target_value=target_spend,
        nb_spend=nb_total_spend,
        nb_regs=nb_regs,
        nb_cpa=nb_cpa,
        brand_spend=brand_spend,
        brand_regs=brand_regs,
        total_spend=total_spend,
        total_regs=total_regs,
        blended_cpa=blended_cpa,
        computed_ieccp=ieccp,
        converged=True,
        warnings=warnings,
        lineage=(
            f"spend-branch direct: target=${target_spend:,.0f} "
            f"brand=${brand_spend:,.0f} ytd_nb=${ytd_nb_spend:,.0f} "
            f"nb_open=${nb_open_spend:,.0f} n_weeks={n_weeks}"
        ),
    )


def _find_nb_spend_at_ieccp(
    target_ieccp_pct: float,
    brand_spend: float,
    brand_regs: float,
    nb_cpa_elast: dict,
    brand_ccp: float,
    nb_ccp: float,
    ytd_nb_spend: float,
    n_weeks: int,
    search_low: float = 1.0,
    search_high: float = 1e10,
) -> Optional[float]:
    """Given a target ie%CCP (percent scale), find the OPEN-weeks NB spend
    that achieves it, via bisection.

    Returns None if the target is not reachable within the search range.
    Used for computing the target-relational bounds in _solve_ieccp_branch.
    """
    def g(nb_open: float) -> float:
        nb_total = nb_open + ytd_nb_spend
        nb_regs_v, _ = _nb_regs_from_annual_spend(nb_total, n_weeks, nb_cpa_elast)
        ieccp_pct = _compute_ieccp_percent(
            brand_regs, nb_regs_v, brand_spend, nb_total, brand_ccp, nb_ccp
        )
        return (ieccp_pct if ieccp_pct is not None else 1e9) - target_ieccp_pct

    g_low = g(search_low)
    g_high = g(search_high)
    if g_low * g_high > 0:
        return None  # target outside search range
    spend, _ = _brent_or_bisect(g, search_low, search_high, 0.01, SOLVER_MAX_ITERATIONS)
    return spend


def _solve_ieccp_branch(
    target_ieccp: float,
    brand_spend: float,
    brand_regs: float,
    nb_cpa_elast: dict,
    brand_ccp: Optional[float],
    nb_ccp: Optional[float],
    min_nb_spend: float,  # kept for signature stability; unused when target-relational bounds active
    max_nb_spend: Optional[float],
    ytd_nb_spend: float = 0.0,
    n_weeks: int = 52,
    tolerance_bps: float = 500.0,
) -> NBSolution:
    """Root-finding on open-weeks NB spend to hit target ie%CCP, using
    target-relational bounds.

    Instead of a hard NB spend floor from ps.market_constraints_manual,
    we compute:
        - bound_low  = NB spend where computed ie%CCP = target + 500bps
          (less NB spend → higher ie%CCP → "upper tolerance")
        - bound_high = NB spend where computed ie%CCP = target - 500bps
          (more NB spend → lower ie%CCP → "lower tolerance")

    Note: in the NB-vs-ie%CCP relationship, MORE NB spend produces LOWER
    ie%CCP (because NB regs grow but carry a lower CCP credit; the
    denominator moves less than the numerator). So:
        low NB  → high ie%CCP
        high NB → low ie%CCP

    The 1000bps-wide band centered on target lets the solver converge on
    the real target, while rejecting solutions that would only get close
    by overshooting the tolerance either direction.

    If neither bound is reachable (elasticity can't land ie%CCP in the
    target ± 500bps window), return closest-feasible + warning.
    """
    warnings: list[str] = []

    if brand_ccp is None or nb_ccp is None:
        warnings.append("UNSUPPORTED_TARGET_MODE: ieccp branch requires both brand_ccp and nb_ccp")
        return NBSolution(
            target_mode="ieccp",
            target_value=target_ieccp,
            nb_spend=0.0,
            nb_regs=0.0,
            nb_cpa=0.0,
            brand_spend=brand_spend,
            brand_regs=brand_regs,
            total_spend=brand_spend,
            total_regs=brand_regs,
            blended_cpa=brand_spend / brand_regs if brand_regs > 0 else 0.0,
            computed_ieccp=None,
            converged=False,
            warnings=warnings,
            lineage="ieccp branch aborted: null CCPs",
        )

    target_pct = _normalize_ieccp_to_percent(target_ieccp)
    tolerance_pp = tolerance_bps / 100.0  # 500 bps = 5.0 percentage points

    # ARCHITECTURE NOTE:
    # ie%CCP is MONOTONICALLY INCREASING with NB spend (more NB → higher
    # ie%CCP) because numerator (total_spend) grows $1 per $1 of NB added,
    # while denominator grows by only (1/nb_cpa) × nb_CCP, typically <<$1.
    # So:
    #     low NB  → low  ie%CCP
    #     high NB → high ie%CCP
    #
    # The 1000bps-wide acceptable band [target-500bps, target+500bps] thus
    # maps to a spend bracket [bound_low, bound_high] where:
    #     bound_low  = NB spend where ie%CCP = target - 500bps
    #     bound_high = NB spend where ie%CCP = target + 500bps

    SEARCH_LOW_ABS = 1.0
    SEARCH_HIGH_ABS = 1e10
    if max_nb_spend is not None and max_nb_spend < SEARCH_HIGH_ABS:
        SEARCH_HIGH_ABS = max_nb_spend

    bound_low = _find_nb_spend_at_ieccp(
        target_pct - tolerance_pp,
        brand_spend, brand_regs, nb_cpa_elast,
        brand_ccp, nb_ccp, ytd_nb_spend, n_weeks,
        search_low=SEARCH_LOW_ABS, search_high=SEARCH_HIGH_ABS,
    )
    bound_high = _find_nb_spend_at_ieccp(
        target_pct + tolerance_pp,
        brand_spend, brand_regs, nb_cpa_elast,
        brand_ccp, nb_ccp, ytd_nb_spend, n_weeks,
        search_low=SEARCH_LOW_ABS, search_high=SEARCH_HIGH_ABS,
    )

    # Both bounds could be None if the elasticity curve doesn't cross the
    # target ± tolerance at all.
    if bound_low is None and bound_high is None:
        warnings.append(
            f"TARGET_UNREACHABLE_UNDER_EFFECTIVE_BOUNDS: neither target-{tolerance_bps:.0f}bps "
            f"nor target+{tolerance_bps:.0f}bps reachable by NB spend in [${SEARCH_LOW_ABS:,.0f}, "
            f"${SEARCH_HIGH_ABS:,.0f}]"
        )
        low = SEARCH_LOW_ABS
        high = SEARCH_HIGH_ABS
    elif bound_low is None:
        # Target-lower bound unreachable — target is very close to or below
        # what's achievable at minimum NB spend.
        warnings.append(
            f"TARGET_UNREACHABLE_ON_LOWER_BAND: target-{tolerance_bps:.0f}bps not reachable "
            f"even at near-zero NB spend; using $1 as lower bracket"
        )
        low = SEARCH_LOW_ABS
        high = bound_high  # type: ignore[assignment]
    elif bound_high is None:
        # Target-upper bound unreachable — even max NB doesn't reach target + tolerance.
        warnings.append(
            f"TARGET_UNREACHABLE_ON_UPPER_BAND: target+{tolerance_bps:.0f}bps not reachable "
            f"within NB spend ${SEARCH_HIGH_ABS:,.0f}; using that as upper bracket"
        )
        low = bound_low  # type: ignore[assignment]
        high = SEARCH_HIGH_ABS
    else:
        # Normal case: both bounds computed.
        low, high = bound_low, bound_high
        if low > high:
            # Can't happen under monotonic ie%CCP-vs-NB, but defend.
            low, high = high, low

    # Within the band, solve for the target precisely.
    def f(nb_open: float) -> float:
        nb_total = nb_open + ytd_nb_spend
        nb_regs_v, _ = _nb_regs_from_annual_spend(nb_total, n_weeks, nb_cpa_elast)
        ieccp_pct = _compute_ieccp_percent(
            brand_regs, nb_regs_v, brand_spend, nb_total, brand_ccp, nb_ccp
        )
        return (ieccp_pct if ieccp_pct is not None else 1e9) - target_pct

    f_low = f(low)
    f_high = f(high)

    if f_low * f_high > 0:
        # Solver shouldn't need this given the bounds construction, but defend
        # against precision issues at the band edges.
        closer_is_low = abs(f_low) < abs(f_high)
        solution_spend = low if closer_is_low else high
        converged = False
    else:
        solution_spend, converged = _brent_or_bisect(
            f, low, high, SOLVER_TOLERANCE_IECCP, SOLVER_MAX_ITERATIONS
        )
        if not converged:
            warnings.append(
                f"SOLVER_NONCONVERGENCE: {SOLVER_MAX_ITERATIONS} iterations did not hit tolerance"
            )

    nb_total = solution_spend + ytd_nb_spend
    nb_regs, nb_cpa = _nb_regs_from_annual_spend(nb_total, n_weeks, nb_cpa_elast)
    total_spend = brand_spend + nb_total
    total_regs = brand_regs + nb_regs
    blended_cpa = total_spend / total_regs if total_regs > 0 else 0.0
    ieccp = _compute_ieccp_percent(brand_regs, nb_regs, brand_spend, nb_total, brand_ccp, nb_ccp)

    # Final check: is the solution actually within the tolerance band?
    # If not, surface it as the honest answer not a fake convergence.
    if ieccp is not None and abs(ieccp - target_pct) > tolerance_pp:
        warnings.append(
            f"OUTSIDE_TOLERANCE_BAND: computed ie%CCP={ieccp:.1f}% vs "
            f"target band [{target_pct - tolerance_pp:.1f}%, {target_pct + tolerance_pp:.1f}%]"
        )

    bounds_str = (
        f"[${bound_low:,.0f} (-{tolerance_bps:.0f}bps), ${bound_high:,.0f} (+{tolerance_bps:.0f}bps)]"
        if bound_low is not None and bound_high is not None
        else f"[${low:,.0f} (fallback), ${high:,.0f} (fallback)]"
    )
    return NBSolution(
        target_mode="ieccp",
        target_value=target_ieccp,
        nb_spend=nb_total,
        nb_regs=nb_regs,
        nb_cpa=nb_cpa,
        brand_spend=brand_spend,
        brand_regs=brand_regs,
        total_spend=total_spend,
        total_regs=total_regs,
        blended_cpa=blended_cpa,
        computed_ieccp=ieccp,
        converged=converged,
        warnings=warnings,
        lineage=(
            f"ieccp target={target_pct:.1f}% (±{tolerance_bps:.0f}bps) "
            f"n_weeks={n_weeks} target-relational bounds={bounds_str} "
            f"nb_total=${nb_total:,.0f} "
            f"computed_ieccp={ieccp:.1f}%" if ieccp is not None else ""
        ),
    )


def _solve_regs_branch(
    target_regs: float,
    brand_spend: float,
    brand_regs: float,
    nb_cpa_elast: dict,
    brand_ccp: Optional[float],
    nb_ccp: Optional[float],
    min_nb_spend: float,
    max_nb_spend: Optional[float],
    ytd_nb_spend: float = 0.0,
    n_weeks: int = 52,
) -> NBSolution:
    """Root-finding on open-weeks NB spend to hit target TOTAL regs.

    target_regs = brand_regs + nb_regs(nb_spend_total)

    Solving for: the NB spend such that nb_regs(spend) = target_regs - brand_regs.

    Architecture note (Phase 6.2.1, 2026-04-23): unlike the ieccp branch,
    regs has no natural tolerance band to define lower/upper bounds —
    there's just one NB spend value that produces the target count. We
    search over [MIN_NB_SPEND_FLOOR, max_nb_spend or $1B] and return the
    closest-feasible answer when the target is unreachable (infeasible
    under elasticity curve saturation).
    """
    warnings: list[str] = []

    required_nb_regs = target_regs - brand_regs
    if required_nb_regs <= 0:
        warnings.append(
            f"REGS_TARGET_MET_BY_BRAND: target_regs={target_regs:.0f} already met by "
            f"brand_regs={brand_regs:.0f}; NB set to floor"
        )
        # Brand alone covers it — set NB to near-zero floor.
        nb_total = ytd_nb_spend + MIN_NB_SPEND_FLOOR
        nb_regs, nb_cpa = _nb_regs_from_annual_spend(nb_total, n_weeks, nb_cpa_elast)
        total_spend = brand_spend + nb_total
        total_regs = brand_regs + nb_regs
        ieccp = _compute_ieccp_percent(brand_regs, nb_regs, brand_spend, nb_total, brand_ccp, nb_ccp)
        return NBSolution(
            target_mode="regs",
            target_value=target_regs,
            nb_spend=nb_total, nb_regs=nb_regs, nb_cpa=nb_cpa,
            brand_spend=brand_spend, brand_regs=brand_regs,
            total_spend=total_spend, total_regs=total_regs,
            blended_cpa=total_spend / total_regs if total_regs > 0 else 0.0,
            computed_ieccp=ieccp, converged=True,
            warnings=warnings,
            lineage=f"regs-branch: brand covers target → nb floor",
        )

    low = MIN_NB_SPEND_FLOOR
    high = max_nb_spend if max_nb_spend is not None else 1e10

    # Does max spend even reach the target?
    regs_at_high, _ = _nb_regs_from_annual_spend(high + ytd_nb_spend, n_weeks, nb_cpa_elast)
    if regs_at_high < required_nb_regs * 0.99:
        warnings.append(
            f"TARGET_UNREACHABLE_UNDER_ELASTICITY: target_regs={target_regs:.0f} requires "
            f"nb_regs={required_nb_regs:.0f}, but max NB spend ${high:,.0f} yields only "
            f"{regs_at_high:.0f} regs; returning closest feasible"
        )
        nb_total = high + ytd_nb_spend
        nb_regs_v, nb_cpa = _nb_regs_from_annual_spend(nb_total, n_weeks, nb_cpa_elast)
        total_spend = brand_spend + nb_total
        total_regs = brand_regs + nb_regs_v
        ieccp = _compute_ieccp_percent(brand_regs, nb_regs_v, brand_spend, nb_total, brand_ccp, nb_ccp)
        return NBSolution(
            target_mode="regs", target_value=target_regs,
            nb_spend=nb_total, nb_regs=nb_regs_v, nb_cpa=nb_cpa,
            brand_spend=brand_spend, brand_regs=brand_regs,
            total_spend=total_spend, total_regs=total_regs,
            blended_cpa=total_spend / total_regs if total_regs > 0 else 0.0,
            computed_ieccp=ieccp, converged=False,
            warnings=warnings,
            lineage=f"regs-branch unreachable at max NB ${high:,.0f}",
        )

    # Root-find: f(nb_open) = nb_regs(nb_open + ytd_nb_spend) - required_nb_regs
    def f(nb_open: float) -> float:
        nb_total = nb_open + ytd_nb_spend
        regs, _ = _nb_regs_from_annual_spend(nb_total, n_weeks, nb_cpa_elast)
        return regs - required_nb_regs

    solution_spend, converged = _brent_or_bisect(f, low, high, SOLVER_TOLERANCE_REGS * required_nb_regs, SOLVER_MAX_ITERATIONS)

    nb_total = solution_spend + ytd_nb_spend
    nb_regs, nb_cpa = _nb_regs_from_annual_spend(nb_total, n_weeks, nb_cpa_elast)
    total_spend = brand_spend + nb_total
    total_regs = brand_regs + nb_regs
    blended_cpa = total_spend / total_regs if total_regs > 0 else 0.0
    ieccp = _compute_ieccp_percent(brand_regs, nb_regs, brand_spend, nb_total, brand_ccp, nb_ccp)

    return NBSolution(
        target_mode="regs",
        target_value=target_regs,
        nb_spend=nb_total, nb_regs=nb_regs, nb_cpa=nb_cpa,
        brand_spend=brand_spend, brand_regs=brand_regs,
        total_spend=total_spend, total_regs=total_regs,
        blended_cpa=blended_cpa, computed_ieccp=ieccp,
        converged=converged,
        warnings=warnings,
        lineage=f"regs-branch target={target_regs:.0f} converged={converged} nb_total=${nb_total:,.0f}",
    )


def _solve_op2_efficient_branch(
    target_regs: float,
    op2_spend_budget: float,
    brand_spend: float,
    brand_regs: float,
    nb_cpa_elast: dict,
    brand_ccp: Optional[float],
    nb_ccp: Optional[float],
    min_nb_spend: float,
    ytd_nb_spend: float = 0.0,
    n_weeks: int = 52,
) -> NBSolution:
    """AU default: hit target regs as efficiently as possible, subject to
    total_spend ≤ op2_spend_budget.

    Per Richard's rule (2026-04-23): "hit the registration goal in the most
    efficient way, but reject it if spend would be above the OP2 target."

    Logic:
      1. Solve for NB spend that hits target_regs via elasticity
      2. If resulting total_spend ≤ op2_spend_budget → return success
      3. If resulting total_spend > op2_spend_budget → emit
         OP2_BUDGET_EXCEEDED warning, return the at-budget answer
         (NB spend = budget - brand_spend) and its projected regs
    """
    warnings: list[str] = []

    # Step 1: solve for regs target via regs branch logic
    regs_sol = _solve_regs_branch(
        target_regs=target_regs,
        brand_spend=brand_spend,
        brand_regs=brand_regs,
        nb_cpa_elast=nb_cpa_elast,
        brand_ccp=brand_ccp,
        nb_ccp=nb_ccp,
        min_nb_spend=min_nb_spend,
        max_nb_spend=None,
        ytd_nb_spend=ytd_nb_spend,
        n_weeks=n_weeks,
    )

    # Step 2: does it fit within OP2 budget?
    if regs_sol.total_spend <= op2_spend_budget:
        # Success — hit target within budget.
        warnings.extend(regs_sol.warnings)
        return NBSolution(
            target_mode="op2_efficient",
            target_value=target_regs,
            nb_spend=regs_sol.nb_spend,
            nb_regs=regs_sol.nb_regs,
            nb_cpa=regs_sol.nb_cpa,
            brand_spend=brand_spend, brand_regs=brand_regs,
            total_spend=regs_sol.total_spend, total_regs=regs_sol.total_regs,
            blended_cpa=regs_sol.blended_cpa, computed_ieccp=regs_sol.computed_ieccp,
            converged=regs_sol.converged,
            warnings=warnings,
            lineage=(
                f"op2_efficient: target_regs={target_regs:.0f} hit at "
                f"total_spend=${regs_sol.total_spend:,.0f} ≤ budget=${op2_spend_budget:,.0f}"
            ),
        )

    # Step 3: target requires more spend than OP2 budget allows → clamp to budget
    nb_at_budget = max(op2_spend_budget - brand_spend, MIN_NB_SPEND_FLOOR)
    nb_total = nb_at_budget
    if nb_at_budget < ytd_nb_spend:
        # YTD already exceeds the budget — emit honest warning.
        warnings.append(
            f"OP2_BUDGET_EXCEEDED_BY_YTD: ytd_nb_spend=${ytd_nb_spend:,.0f} already exceeds "
            f"budget-minus-brand=${op2_spend_budget - brand_spend:,.0f}"
        )
        nb_total = ytd_nb_spend  # can't unspend
    nb_regs_at_budget, nb_cpa = _nb_regs_from_annual_spend(nb_total, n_weeks, nb_cpa_elast)
    total_spend = brand_spend + nb_total
    total_regs = brand_regs + nb_regs_at_budget

    regs_shortfall = target_regs - total_regs
    shortfall_pct = 100.0 * regs_shortfall / target_regs if target_regs > 0 else 0.0
    warnings.append(
        f"OP2_BUDGET_EXCEEDED: target_regs={target_regs:.0f} would require "
        f"${regs_sol.total_spend:,.0f} but budget is ${op2_spend_budget:,.0f}; "
        f"clamped to budget, projected {total_regs:.0f} regs ({shortfall_pct:.1f}% short of target)"
    )

    blended_cpa = total_spend / total_regs if total_regs > 0 else 0.0
    ieccp = _compute_ieccp_percent(brand_regs, nb_regs_at_budget, brand_spend, nb_total, brand_ccp, nb_ccp)

    return NBSolution(
        target_mode="op2_efficient",
        target_value=target_regs,
        nb_spend=nb_total, nb_regs=nb_regs_at_budget, nb_cpa=nb_cpa,
        brand_spend=brand_spend, brand_regs=brand_regs,
        total_spend=total_spend, total_regs=total_regs,
        blended_cpa=blended_cpa, computed_ieccp=ieccp,
        converged=False,
        warnings=warnings,
        lineage=(
            f"op2_efficient: budget-capped at ${op2_spend_budget:,.0f}; "
            f"shortfall {shortfall_pct:.1f}%"
        ),
    )


# ---------- Main entry point ----------


def solve_nb_residual(
    brand_spend: float,
    brand_regs: float,
    target_mode: str,
    target_value: float,
    nb_cpa_elast: dict,
    brand_ccp: Optional[float] = None,
    nb_ccp: Optional[float] = None,
    min_nb_spend: float = 0.0,
    max_nb_spend: Optional[float] = None,
    ytd_nb_spend: float = 0.0,
    n_weeks: int = 52,
) -> NBSolution:
    """Dispatch to the branch specified by target_mode.

    Args:
        brand_spend: Total projected Brand spend for the OPEN weeks
            (i.e. excludes any locked-YTD portion of Brand already spent).
        brand_regs: Total projected Brand regs for the OPEN weeks.
        target_mode: 'spend' | 'ieccp' | 'regs' | 'op2_efficient'. Phase
            6.1 supports 'spend' and 'ieccp' only; other modes emit
            UNSUPPORTED_TARGET_MODE and return a dummy NBSolution.
        target_value: Target value in native units (dollars for spend,
            decimal-or-percent for ieccp, count for regs).
        nb_cpa_elast: {'a': ..., 'b': ...} from ps.market_projection_params
            nb_cpa_elasticity parameter.
        brand_ccp: Scalar brand CCP ($ per regulated weighted registration).
            Required for ieccp branch. None for AU.
        nb_ccp: Scalar NB CCP. Required for ieccp branch. None for AU.
        min_nb_spend: Operational floor on OPEN-weeks NB spend from
            ps.market_constraints_manual.
        max_nb_spend: Operational ceiling on OPEN-weeks NB spend.
        ytd_nb_spend: NB spend already locked for YTD-weeks (only passed
            by project_with_locked_ytd; 0 for stateless calls).

    Returns NBSolution. Never raises — all errors captured as warnings.
    """
    if target_mode == "spend":
        return _solve_spend_branch(
            target_spend=target_value,
            brand_spend=brand_spend,
            brand_regs=brand_regs,
            nb_cpa_elast=nb_cpa_elast,
            brand_ccp=brand_ccp,
            nb_ccp=nb_ccp,
            min_nb_spend=min_nb_spend,
            max_nb_spend=max_nb_spend,
            ytd_nb_spend=ytd_nb_spend,
            n_weeks=n_weeks,
        )
    if target_mode == "ieccp":
        return _solve_ieccp_branch(
            target_ieccp=target_value,
            brand_spend=brand_spend,
            brand_regs=brand_regs,
            nb_cpa_elast=nb_cpa_elast,
            brand_ccp=brand_ccp,
            nb_ccp=nb_ccp,
            min_nb_spend=min_nb_spend,
            max_nb_spend=max_nb_spend,
            ytd_nb_spend=ytd_nb_spend,
            n_weeks=n_weeks,
        )
    if target_mode == "regs":
        return _solve_regs_branch(
            target_regs=target_value,
            brand_spend=brand_spend,
            brand_regs=brand_regs,
            nb_cpa_elast=nb_cpa_elast,
            brand_ccp=brand_ccp,
            nb_ccp=nb_ccp,
            min_nb_spend=min_nb_spend,
            max_nb_spend=max_nb_spend,
            ytd_nb_spend=ytd_nb_spend,
            n_weeks=n_weeks,
        )
    if target_mode == "op2_efficient":
        # op2_efficient target_value is a dict {target_regs, op2_spend_budget}.
        # Legacy callers passing target_value as a scalar are rejected with
        # an explanatory warning.
        if not isinstance(target_value, dict):
            return NBSolution(
                target_mode=target_mode, target_value=0.0,
                nb_spend=0.0, nb_regs=0.0, nb_cpa=0.0,
                brand_spend=brand_spend, brand_regs=brand_regs,
                total_spend=brand_spend, total_regs=brand_regs,
                blended_cpa=brand_spend / brand_regs if brand_regs > 0 else 0.0,
                computed_ieccp=None, converged=False,
                warnings=[
                    "OP2_EFFICIENT_REQUIRES_DICT: target_value must be "
                    "{'target_regs': N, 'op2_spend_budget': $X}, got scalar"
                ],
                lineage="op2_efficient: invalid target_value shape",
            )
        return _solve_op2_efficient_branch(
            target_regs=target_value.get("target_regs", 0),
            op2_spend_budget=target_value.get("op2_spend_budget", 0),
            brand_spend=brand_spend,
            brand_regs=brand_regs,
            nb_cpa_elast=nb_cpa_elast,
            brand_ccp=brand_ccp,
            nb_ccp=nb_ccp,
            min_nb_spend=min_nb_spend,
            ytd_nb_spend=ytd_nb_spend,
            n_weeks=n_weeks,
        )
    # Unknown mode.
    return NBSolution(
        target_mode=target_mode,
        target_value=target_value if isinstance(target_value, (int, float)) else 0.0,
        nb_spend=0.0,
        nb_regs=0.0,
        nb_cpa=0.0,
        brand_spend=brand_spend,
        brand_regs=brand_regs,
        total_spend=brand_spend,
        total_regs=brand_regs,
        blended_cpa=brand_spend / brand_regs if brand_regs > 0 else 0.0,
        computed_ieccp=None,
        converged=False,
        warnings=[f"UNKNOWN_TARGET_MODE: {target_mode!r}"],
        lineage=f"target_mode={target_mode!r} not recognized",
    )
