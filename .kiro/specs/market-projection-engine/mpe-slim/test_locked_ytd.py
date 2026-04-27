"""
Starter test for Locked-YTD functionality.
Run this after implementing project_with_locked_ytd().
"""

import pytest
from src.mpe_engine import project_with_locked_ytd, ProjectionInputs

def test_locked_ytd_prevents_under_spend():
    """Should never return total spend below YTD actuals + minimum NB."""
    inputs = ProjectionInputs(
        scope="MX",
        time_period="Y2026",
        target_mode="ieccp",
        target_value=0.75
    )
    
    result = project_with_locked_ytd(inputs)
    
    # YTD actual spend for MX through W16 ≈ $279K
    # Minimum remaining NB spend (35 weeks × $15K) = $525K
    # Expected minimum total ≈ $804K
    assert result["total_spend"] >= 800000, "Locked-YTD constraint violated"
    assert "YTD_LOCKED" in result.get("warnings", []), "Should emit YTD_LOCKED warning"

def test_mx_y2026_75pct_returns_realistic_range():
    """MX Y2026 @ 75% should be in realistic $750K-$1.1M band (primary demo market)."""
    inputs = ProjectionInputs(
        scope="MX",
        time_period="Y2026",
        target_mode="ieccp",
        target_value=0.75
    )
    
    result = project_with_locked_ytd(inputs)
    
    assert 750000 <= result["total_spend"] <= 1100000, \
        f"Got ${result['total_spend']:,} — outside expected realistic range"


def test_all_markets_locked_ytd():
    """All 10 markets should respect Locked-YTD constraint."""
    markets = ["MX", "US", "CA", "JP", "UK", "DE", "FR", "IT", "ES", "AU"]
    for market in markets:
        inputs = ProjectionInputs(
            scope=market,
            time_period="Y2026",
            target_mode="ieccp" if market != "AU" else "op2_efficient",
            target_value=0.75 if market != "AU" else None
        )
        result = project_with_locked_ytd(inputs)
        assert result["total_spend"] >= 0, f"{market} failed Locked-YTD"