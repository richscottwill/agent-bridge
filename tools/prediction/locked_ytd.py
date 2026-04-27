"""
Locked-YTD + Remaining-of-Year (RoY) Projection — MPE v1.1 Slim (Phase 6.1.5)

=============================================================================
WHAT THIS DOES (Plain English)
=============================================================================
    For Y-periods (annual projections), splits the projection into:
      - LOCKED weeks: already-completed weeks in ps.v_weekly. We DON'T
        project these. We use the actual numbers.
      - OPEN weeks: remaining-of-year weeks. We project these via the new
        Brand-Anchor + NB-Residual pipeline.

    The core rule: a projection NEVER returns a total spend below the
    already-committed YTD. You can't un-spend what's already spent.

    This was the root cause of the v1 $443K bug on MX Y2026 @ 75%: the
    top-down solver freely moved spend below YTD actuals because it
    treated all 52 weeks as solver variables. Locked-YTD makes the
    past weeks physics, not optimization space.

=============================================================================
HOW IT WORKS
=============================================================================
    1. Fetch ps.v_weekly for market × year up to data cutoff.
    2. Sum YTD actuals: brand_spend, brand_regs, nb_spend, nb_regs per
       locked weeks.
    3. Compute open_weeks = [data_cutoff_week + 1, 52].
    4. Project Brand trajectory over open_weeks via brand_trajectory.
    5. Solve NB residual over open_weeks, passing ytd_nb_spend so the
       solver can return total (YTD + open) NB spend that hits the target.
    6. Combine YTD actuals + open-weeks projection into ProjectionOutputs.

    Warning taxonomy:
      - LOCKED_YTD_CONSTRAINT_ACTIVE: floor forced the solver away from
        a lower-spend answer.
      - YTD_NO_DATA_AVAILABLE: the market has no ps.v_weekly rows for
        this year; falls back to full-year projection.
      - YTD_PARTIAL: some weeks missing; we lock whatever exists and
        project the rest.

=============================================================================
HOW IT CAN FAIL
=============================================================================
    1. Non-Y period (W, M, Q) → short-circuits, returns regular project()
       result with LOCKED_YTD_NOT_APPLIED warning.
    2. Year entirely in future → no locked data, LOCKED_YTD_NOT_APPLIED.
    3. Year entirely in past → all weeks locked, no projection; returns
       pure actuals.
=============================================================================
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

from prediction.brand_trajectory import project_brand_trajectory
from prediction.nb_residual_solver import solve_nb_residual


# ---------- Result types ----------


@dataclass
class YTDActuals:
    """Sum of locked YTD weeks for a market."""
    market: str
    year: int
    weeks: list[date] = field(default_factory=list)
    brand_regs: float = 0.0
    brand_spend: float = 0.0
    nb_regs: float = 0.0
    nb_spend: float = 0.0
    n_weeks_locked: int = 0
    latest_week_locked: Optional[date] = None

    @property
    def total_regs(self) -> float:
        return self.brand_regs + self.nb_regs

    @property
    def total_spend(self) -> float:
        return self.brand_spend + self.nb_spend


@dataclass
class LockedYTDProjection:
    """Full combined YTD + RoY projection."""
    market: str
    year: int
    target_mode: str
    target_value: float

    # YTD
    ytd: YTDActuals

    # RoY (projected)
    roy_brand_regs: float
    roy_brand_spend: float
    roy_nb_regs: float
    roy_nb_spend: float
    roy_weeks: list[date]

    # Combined
    total_brand_regs: float
    total_brand_spend: float
    total_nb_regs: float
    total_nb_spend: float
    total_regs: float
    total_spend: float
    blended_cpa: float
    computed_ieccp: Optional[float]

    # Provenance
    contribution_breakdown: dict[str, float] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    locked_ytd_constraint_active: bool = False
    lineage: str = ""

    def to_json(self) -> dict:
        return {
            "market": self.market,
            "year": self.year,
            "target_mode": self.target_mode,
            "target_value": self.target_value,
            "ytd": {
                "n_weeks_locked": self.ytd.n_weeks_locked,
                "latest_week": self.ytd.latest_week_locked.isoformat() if self.ytd.latest_week_locked else None,
                "brand_regs": self.ytd.brand_regs,
                "brand_spend": self.ytd.brand_spend,
                "nb_regs": self.ytd.nb_regs,
                "nb_spend": self.ytd.nb_spend,
                "total_regs": self.ytd.total_regs,
                "total_spend": self.ytd.total_spend,
            },
            "roy": {
                "brand_regs": self.roy_brand_regs,
                "brand_spend": self.roy_brand_spend,
                "nb_regs": self.roy_nb_regs,
                "nb_spend": self.roy_nb_spend,
                "n_weeks": len(self.roy_weeks),
            },
            "totals": {
                "brand_regs": self.total_brand_regs,
                "brand_spend": self.total_brand_spend,
                "nb_regs": self.total_nb_regs,
                "nb_spend": self.total_nb_spend,
                "total_regs": self.total_regs,
                "total_spend": self.total_spend,
                "blended_cpa": self.blended_cpa,
                "computed_ieccp": self.computed_ieccp,
            },
            "contribution_breakdown": self.contribution_breakdown,
            "locked_ytd_constraint_active": self.locked_ytd_constraint_active,
            "warnings": self.warnings,
            "lineage": self.lineage,
        }


# ---------- YTD actuals fetch ----------


def fetch_ytd_actuals(market: str, year: int, as_of: Optional[date] = None) -> YTDActuals:
    """Sum weekly actuals from ps.v_weekly for market × year.

    If as_of is given, cut off at that date (useful for historical replay).
    Otherwise cuts off at the most recent complete week in the data.
    """
    from prediction.brand_trajectory import _fitting_db

    con = _fitting_db()
    # One row per available week; sum in Python so we can also track
    # the weeks list for later joining with RoY.
    rows = con.execute(
        """
        SELECT period_start,
               COALESCE(brand_registrations, 0) AS brand_regs,
               COALESCE(brand_cost, 0) AS brand_spend,
               COALESCE(nb_registrations, 0) AS nb_regs,
               COALESCE(nb_cost, 0) AS nb_spend
        FROM ps.v_weekly
        WHERE market = ? AND period_type = 'weekly'
          AND EXTRACT(YEAR FROM period_start) = ?
        ORDER BY period_start ASC
        """,
        [market, year],
    ).fetchall()

    ytd = YTDActuals(market=market, year=year)
    for period_start, b_regs, b_spend, n_regs, n_spend in rows:
        if as_of is not None and period_start > as_of:
            break
        ytd.weeks.append(period_start)
        ytd.brand_regs += float(b_regs)
        ytd.brand_spend += float(b_spend)
        ytd.nb_regs += float(n_regs)
        ytd.nb_spend += float(n_spend)
        ytd.n_weeks_locked += 1
        ytd.latest_week_locked = period_start

    return ytd


def compute_roy_weeks(year: int, ytd_latest: Optional[date]) -> list[date]:
    """Return list of Monday dates for remaining-of-year weeks."""
    # ISO week 1 Monday of the year.
    jan4 = date(year, 1, 4)
    week1_monday = jan4 - timedelta(days=jan4.weekday())

    # First open week = week after ytd_latest (or week 1 if nothing locked).
    if ytd_latest is None:
        first_open_monday = week1_monday
    else:
        first_open_monday = ytd_latest + timedelta(weeks=1)

    # Build weeks through year-end (52 weeks total in most years).
    all_weeks = [week1_monday + timedelta(weeks=i) for i in range(52)]
    return [w for w in all_weeks if w >= first_open_monday]


# ---------- Main entry point ----------


def project_with_locked_ytd(
    market: str,
    year: int,
    target_mode: str,
    target_value: float,
    nb_cpa_elast: dict,
    brand_ccp: Optional[float],
    nb_ccp: Optional[float],
    min_weekly_nb_spend: float = 0.0,
    max_weekly_nb_spend: Optional[float] = None,
    brand_trajectory_weights: Optional[dict] = None,
    regime_multiplier: float = 1.0,
    as_of: Optional[date] = None,
) -> LockedYTDProjection:
    """Full YTD + RoY projection with locked-YTD constraint.

    Args:
        market: market code
        year: target year (e.g., 2026)
        target_mode: 'spend' | 'ieccp' | 'regs' | 'op2_efficient'
        target_value: constraint value
        nb_cpa_elast: {'a': ..., 'b': ...} from ps.market_projection_params
        brand_ccp, nb_ccp: scalar CCPs (None for AU)
        min_weekly_nb_spend, max_weekly_nb_spend: ops bounds per week
        brand_trajectory_weights: optional override
        as_of: historical replay cutoff date (default: today)

    Returns LockedYTDProjection. Never raises.
    """
    warnings: list[str] = []

    # 1) Fetch YTD actuals.
    ytd = fetch_ytd_actuals(market, year, as_of=as_of)
    if ytd.n_weeks_locked == 0:
        warnings.append("YTD_NO_DATA_AVAILABLE (falling back to pure RoY projection for full year)")

    # 2) Compute RoY weeks.
    roy_weeks = compute_roy_weeks(year, ytd.latest_week_locked)
    n_roy = len(roy_weeks)

    if n_roy == 0:
        # Year entirely in past — all weeks locked, no projection needed.
        return LockedYTDProjection(
            market=market, year=year,
            target_mode=target_mode, target_value=target_value,
            ytd=ytd,
            roy_brand_regs=0.0, roy_brand_spend=0.0,
            roy_nb_regs=0.0, roy_nb_spend=0.0, roy_weeks=[],
            total_brand_regs=ytd.brand_regs,
            total_brand_spend=ytd.brand_spend,
            total_nb_regs=ytd.nb_regs,
            total_nb_spend=ytd.nb_spend,
            total_regs=ytd.total_regs,
            total_spend=ytd.total_spend,
            blended_cpa=(ytd.total_spend / ytd.total_regs) if ytd.total_regs > 0 else 0.0,
            computed_ieccp=_ieccp_percent(
                ytd.brand_regs, ytd.nb_regs,
                ytd.brand_spend, ytd.nb_spend,
                brand_ccp, nb_ccp,
            ),
            warnings=warnings + ["YEAR_FULLY_LOCKED (all weeks in past)"],
            lineage=f"YTD-only: {ytd.n_weeks_locked} weeks, no open weeks",
        )

    # 3) Brand trajectory for RoY weeks only.
    brand_proj = project_brand_trajectory(
        market, roy_weeks, weights=brand_trajectory_weights,
        regime_multiplier=regime_multiplier,
    )

    # Full-year Brand totals for the solver (YTD actuals + RoY projection).
    # The solver targets FULL-YEAR ie%CCP, so brand_spend/brand_regs passed
    # in must be full-year, not RoY-only.
    brand_total_spend = ytd.brand_spend + brand_proj.total_spend
    brand_total_regs = ytd.brand_regs + brand_proj.total_regs

    # Solve NB residual for RoY portion. As of Phase 6.1.5 pivot (2026-04-23):
    # ieccp branch uses target-relational bounds (target ± 500bps) internally
    # instead of operational floors, so we pass 0/None here for the hard bounds.
    # The spend branch still uses max_nb_spend if provided as a sanity ceiling.
    min_nb_total = 0.0  # no hard floor; ieccp branch computes its own from target
    max_nb_total = (max_weekly_nb_spend * n_roy) if max_weekly_nb_spend else None

    nb_sol = solve_nb_residual(
        brand_spend=brand_total_spend,
        brand_regs=brand_total_regs,
        target_mode=target_mode,
        target_value=target_value,
        nb_cpa_elast=nb_cpa_elast,
        brand_ccp=brand_ccp,
        nb_ccp=nb_ccp,
        min_nb_spend=min_nb_total,
        max_nb_spend=max_nb_total,
        ytd_nb_spend=ytd.nb_spend,
        n_weeks=52,  # full-year elasticity application; nb_total spans the full year
    )
    warnings.extend(brand_proj.warnings)
    warnings.extend(nb_sol.warnings)

    # nb_sol.nb_spend is TOTAL (YTD + RoY) NB per solve_nb_residual contract.
    # RoY NB spend is the portion ABOVE ytd.nb_spend.
    nb_roy_spend = max(0.0, nb_sol.nb_spend - ytd.nb_spend)
    total_nb_regs_full = nb_sol.nb_regs  # full-year NB regs from solver
    nb_roy_regs = max(0.0, total_nb_regs_full - ytd.nb_regs)

    # 5) Assemble totals. Solver used full-year Brand + full-year NB inputs,
    # so nb_sol.total_spend and nb_sol.total_regs are already full-year totals.
    total_brand_spend = brand_total_spend
    total_brand_regs = brand_total_regs
    total_nb_spend = nb_sol.nb_spend
    total_spend = total_brand_spend + total_nb_spend
    total_regs = total_brand_regs + total_nb_regs_full
    blended_cpa = total_spend / total_regs if total_regs > 0 else 0.0
    ieccp = _ieccp_percent(
        total_brand_regs, total_nb_regs_full,
        total_brand_spend, total_nb_spend,
        brand_ccp, nb_ccp,
    )

    # Check whether the bounds forced the solver off its preferred answer.
    # Signals: any solver warning about unreachability, tolerance band
    # overshoot, or under-funded NB (target below achievable floor).
    constraint_active = any(
        kw in "".join(warnings)
        for kw in ("TARGET_UNREACHABLE", "OUTSIDE_TOLERANCE_BAND", "NB_UNDER_FUNDED")
    )

    return LockedYTDProjection(
        market=market, year=year,
        target_mode=target_mode, target_value=target_value,
        ytd=ytd,
        roy_brand_regs=brand_proj.total_regs,
        roy_brand_spend=brand_proj.total_spend,
        roy_nb_regs=nb_roy_regs,
        roy_nb_spend=nb_roy_spend,
        roy_weeks=roy_weeks,
        total_brand_regs=total_brand_regs,
        total_brand_spend=total_brand_spend,
        total_nb_regs=total_nb_regs_full,
        total_nb_spend=total_nb_spend,
        total_regs=total_regs,
        total_spend=total_spend,
        blended_cpa=blended_cpa,
        computed_ieccp=ieccp,
        contribution_breakdown=brand_proj.contribution,
        warnings=warnings,
        locked_ytd_constraint_active=constraint_active,
        lineage=(
            f"YTD: {ytd.n_weeks_locked}w locked through {ytd.latest_week_locked} "
            f"({ytd.total_regs:,.0f} regs, ${ytd.total_spend:,.0f}); "
            f"RoY: {n_roy}w projected via {brand_proj.lineage}"
        ),
    )


def _ieccp_percent(brand_regs, nb_regs, brand_spend, nb_spend, brand_ccp, nb_ccp):
    """ie%CCP on percent scale, None if CCPs missing."""
    if brand_ccp is None or nb_ccp is None:
        return None
    total = brand_spend + nb_spend
    denom = brand_regs * brand_ccp + nb_regs * nb_ccp
    if denom <= 0:
        return None
    return (total / denom) * 100.0


# ---------- CLI ----------


def main(argv: Optional[list[str]] = None) -> int:
    import argparse
    from prediction.mpe_engine import load_parameters

    p = argparse.ArgumentParser(description="Locked-YTD + RoY projection (Phase 6.1.5)")
    p.add_argument("--market", required=True)
    p.add_argument("--year", type=int, default=2026)
    p.add_argument("--target-mode", default="ieccp")
    p.add_argument("--target-value", type=float, default=0.75)
    p.add_argument(
        "--regime-multiplier", type=float, default=1.0,
        help="Global dial over auto-derived per-regime confidences (default 1.0)."
    )
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = p.parse_args(argv)

    params = load_parameters(args.market)
    nb_cpa_elast = params.get("nb_cpa_elasticity", {}).get("value_json")
    if not nb_cpa_elast:
        print(f"No nb_cpa_elasticity for {args.market}", file=sys.stderr)
        return 2
    brand_ccp = params.get("brand_ccp", {}).get("value_scalar")
    nb_ccp = params.get("nb_ccp", {}).get("value_scalar")
    bounds = params.get("_spend_bounds") or {}

    weights = {
        "seasonal": 0.40, "trend": 0.40, "regime": 0.15, "qualitative": 0.05,
    }

    proj = project_with_locked_ytd(
        market=args.market, year=args.year,
        target_mode=args.target_mode, target_value=args.target_value,
        nb_cpa_elast=nb_cpa_elast,
        brand_ccp=brand_ccp, nb_ccp=nb_ccp,
        min_weekly_nb_spend=bounds.get("min_weekly_nb_spend") or 0.0,
        max_weekly_nb_spend=bounds.get("max_weekly_nb_spend"),
        brand_trajectory_weights=weights,
        regime_multiplier=args.regime_multiplier,
    )

    if args.format == "json":
        import json
        print(json.dumps(proj.to_json(), indent=2, default=str))
        return 0

    print(f"# Locked-YTD + RoY — {proj.market} Y{proj.year}")
    print(f"Target: {proj.target_mode}:{proj.target_value}")
    print(f"Brand weights: {weights}")
    print()
    print(f"## YTD ({proj.ytd.n_weeks_locked} weeks locked through {proj.ytd.latest_week_locked})")
    print(f"  Brand: {proj.ytd.brand_regs:,.0f} regs, ${proj.ytd.brand_spend:,.0f}")
    print(f"  NB:    {proj.ytd.nb_regs:,.0f} regs, ${proj.ytd.nb_spend:,.0f}")
    print(f"  Total: {proj.ytd.total_regs:,.0f} regs, ${proj.ytd.total_spend:,.0f}")
    print()
    print(f"## RoY ({len(proj.roy_weeks)} weeks projected)")
    print(f"  Brand: {proj.roy_brand_regs:,.0f} regs, ${proj.roy_brand_spend:,.0f}")
    print(f"  NB:    {proj.roy_nb_regs:,.0f} regs, ${proj.roy_nb_spend:,.0f}")
    print()
    print(f"## Total (YTD + RoY)")
    print(f"  Brand: {proj.total_brand_regs:,.0f} regs, ${proj.total_brand_spend:,.0f}")
    print(f"  NB:    {proj.total_nb_regs:,.0f} regs, ${proj.total_nb_spend:,.0f}")
    print(f"  Total: {proj.total_regs:,.0f} regs, ${proj.total_spend:,.0f}")
    print(f"  Blended CPA: ${proj.blended_cpa:.2f}")
    if proj.computed_ieccp is not None:
        print(f"  ie%CCP: {proj.computed_ieccp:.1f}%")
    print()
    print(f"Contribution: {proj.contribution_breakdown}")
    print(f"Locked-YTD constraint active: {proj.locked_ytd_constraint_active}")
    print(f"Lineage: {proj.lineage}")
    if proj.warnings:
        print()
        print("Warnings:")
        for w in proj.warnings:
            print(f"  - {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
