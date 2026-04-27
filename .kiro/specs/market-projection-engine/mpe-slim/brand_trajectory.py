"""
Brand Trajectory Model (v1.1 Slim)
3-stream version: Seasonal + Recent Trend + Regime
"""

def project_brand_trajectory(market: str, weeks: list, inputs) -> dict:
    """
    Projects Brand regs using blended evidence.
    Phase 1: Seasonal + Recent Trend only.
    """
    # TODO: Implement full logic
    # For now, return placeholder
    return {
        "regs": 9184,           # Placeholder for MX Y2026
        "spend": 160875,
        "contribution": {
            "seasonal": 0.40,
            "trend": 0.45,
            "regime": 0.15
        }
    }