"""
Phase 6.2.6 stable output fixture generator.

Runs the v1.1 Slim engine across all 10 markets + 3 regions × default target
modes and writes a JSON fixture. The regression test (test_v1_1_slim_phase6_2.py)
re-runs this and compares output to the fixture within ±1% tolerance.

Re-run when the engine intentionally changes to regenerate the baseline.
"""
from __future__ import annotations

import json
from pathlib import Path

from prediction.mpe_engine import ProjectionInputs, project


MARKET_TARGETS = {
    # Phase 6.2.x follow-on (2026-04-25): committed ie%CCP targets per
    # ps.market_projection_params_current. Richard set NA/EU5 markets +
    # NA/EU5 regions to 0.65. MX stays at 1.00. JP and AU have NO
    # committed ie%CCP target (JP deactivated 2026-04-25 per v6
    # migration; AU has null CCPs by design). Both use spend branch.
    "MX": ("ieccp", 1.00),
    "US": ("ieccp", 0.65),
    "CA": ("ieccp", 0.65),
    "UK": ("ieccp", 0.65),
    "DE": ("ieccp", 0.65),
    "FR": ("ieccp", 0.65),
    "IT": ("ieccp", 0.65),
    "ES": ("ieccp", 0.65),
    "JP": ("spend", 5_000_000),
    "AU": ("spend", 500_000),
}

REGION_TARGETS = {
    # Phase 6.2.x follow-on (2026-04-25): regions are ROLLUPS of
    # constituent markets, not drivers. target_mode='rollup' runs each
    # constituent at its own committed ieccp_target from the registry,
    # then sum-then-divides the regional ie%CCP per R6.2. No target
    # value — the region's number is what its children produce.
    "NA": ("rollup", 0),
    "EU5": ("rollup", 0),
    "WW": ("rollup", 0),
}


def main() -> int:
    fixture = {
        "generated": None,  # filled by json dump
        "period": "Y2026",
        "per_market": {},
        "per_region": {},
    }

    from datetime import datetime
    fixture["generated"] = datetime.now().isoformat()

    for market, (mode, value) in MARKET_TARGETS.items():
        inputs = ProjectionInputs(
            scope=market, time_period="Y2026",
            target_mode=mode, target_value=value,
        )
        out = project(inputs)
        fixture["per_market"][market] = {
            "outcome": out.outcome,
            "target_mode": mode,
            "target_value": value,
            "total_regs": round(out.totals.get("total_regs", 0), 2),
            "total_spend": round(out.totals.get("total_spend", 0), 2),
            "brand_regs": round(out.totals.get("brand_regs", 0), 2),
            "nb_regs": round(out.totals.get("nb_regs", 0), 2),
            "blended_cpa": round(out.totals.get("blended_cpa", 0), 2),
            "ieccp": round(out.totals["ieccp"], 2) if out.totals.get("ieccp") is not None else None,
            "warnings_count": len(out.warnings),
            "n_regimes": len(out.regime_stack) if out.regime_stack else 0,
        }
        print(f"[{market}] spend ${fixture['per_market'][market]['total_spend']:,.0f}")

    for region, (mode, value) in REGION_TARGETS.items():
        inputs = ProjectionInputs(
            scope=region, time_period="Y2026",
            target_mode=mode, target_value=value,
        )
        out = project(inputs)
        fixture["per_region"][region] = {
            "outcome": out.outcome,
            "target_mode": mode,
            "target_value": value,
            "total_regs": round(out.totals.get("total_regs", 0), 2),
            "total_spend": round(out.totals.get("total_spend", 0), 2),
            "ieccp": round(out.totals["ieccp"], 2) if out.totals.get("ieccp") is not None else None,
            "n_constituent_markets": len(out.constituent_markets),
        }
        print(f"[{region}] spend ${fixture['per_region'][region]['total_spend']:,.0f}")

    out_path = Path(__file__).resolve().parent / "phase6_2_stable_output.json"
    out_path.write_text(json.dumps(fixture, indent=2))
    print(f"\nWrote {out_path}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
