"""
MPE Engine v1.1 Slim — Updated Core
This is a sketch showing the key changes from v1.
"""

from typing import Dict, Any
from .brand_trajectory import project_brand_trajectory
from .nb_residual_solver import solve_nb_residual

def project(inputs) -> Dict[str, Any]:
    """
    Main projection function (v1.1 Slim version).
    Replaces the old top-down solver.
    """
    
    # === Step 1: Get Brand projection (new) ===
    brand = project_brand_trajectory(
        market=inputs.scope,
        weeks=inputs.weeks,
        inputs=inputs
    )
    
    # === Step 2: Solve for NB as residual (new) ===
    nb = solve_nb_residual(
        brand_regs=brand["regs"],
        brand_spend=brand["spend"],
        target=inputs.target,
        ytd_actuals=inputs.ytd_actuals  # NEW: Locked-YTD support
    )
    
    # === Step 3: Combine results ===
    total_spend = brand["spend"] + nb["nb_spend"]
    total_regs = brand["regs"] + nb["nb_regs"]
    
    result = {
        "total_spend": total_spend,
        "total_regs": total_regs,
        "brand_regs": brand["regs"],
        "nb_regs": nb["nb_regs"],
        "ieccp": total_spend / (brand["regs"] * 90 + nb["nb_regs"] * 30),  # placeholder CCPs
        "warnings": nb.get("warnings", []),
        "contribution": brand.get("contribution", {})
    }
    
    return result


def project_with_locked_ytd(inputs) -> Dict[str, Any]:
    """
    New v1.1 function: Respects locked YTD actuals.
    This is the highest priority improvement.
    """
    # TODO: Implement full logic
    # For now, call main project() and add warning
    result = project(inputs)
    result["warnings"].append("YTD_LOCKED: Using locked YTD + RoY projection (v1.1 Slim)")
    return result