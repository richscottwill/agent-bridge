"""Property-based tests for budget pacing.

**Validates: Requirements 5.1**

Property 2: Pacing Consistency — pacing_pct = (actual_spend / prorated_target) × 100
where prorated_target = monthly_target × (days_elapsed / days_in_month).

Also verifies:
- days_elapsed + days_remaining == days_in_month
- Status classification matches pacing_pct thresholds
"""

from __future__ import annotations

import calendar
from datetime import date
from decimal import Decimal

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from paid_search_audit.budget_pacing import BudgetPacingEngine
from paid_search_audit.config import OP2Targets
from paid_search_audit.models import NormalizedMetrics

# --- Strategies ---

# Audit dates spanning a wide range of months
audit_date_strategy = st.dates(min_value=date(2024, 1, 1), max_value=date(2027, 12, 31))

# Positive monthly spend targets (avoid zero — tested separately)
monthly_target_strategy = st.decimals(
    min_value=Decimal("0.01"),
    max_value=Decimal("10000000"),
    allow_nan=False,
    allow_infinity=False,
    places=2,
)

# Daily spend amounts (non-negative)
daily_spend_strategy = st.decimals(
    min_value=Decimal("0"),
    max_value=Decimal("100000"),
    allow_nan=False,
    allow_infinity=False,
    places=2,
)

market_strategy = st.sampled_from(["AU", "MX", "US", "JP", "CA", "DE"])


def _build_metric(metric_date: date, market: str, spend: Decimal) -> NormalizedMetrics:
    """Build a minimal NormalizedMetrics for a given date, market, and spend."""
    return NormalizedMetrics(
        date=metric_date,
        market=market,
        campaign_type="Brand",
        campaign_name="test-campaign",
        account_id="1234567890",
        mcc_id="0987654321",
        impressions=100,
        clicks=10,
        spend=spend,
        spend_usd=spend,
        conversions=1,
        source="GOOGLE_ADS",
    )


@st.composite
def pacing_scenario(draw):
    """Generate a complete pacing scenario: audit_date, daily spends, and monthly target.

    Returns (audit_date, metrics, targets, market) where metrics contains
    one NormalizedMetrics per day from month start through audit_date.
    """
    audit_date = draw(audit_date_strategy)
    market = draw(market_strategy)
    monthly_target = draw(monthly_target_strategy)

    days_in_month = calendar.monthrange(audit_date.year, audit_date.month)[1]
    days_elapsed = audit_date.day  # day 1 through audit_date.day

    # Generate one spend amount per elapsed day
    daily_spends = draw(
        st.lists(
            daily_spend_strategy,
            min_size=days_elapsed,
            max_size=days_elapsed,
        )
    )

    metrics = [
        _build_metric(
            date(audit_date.year, audit_date.month, day_num + 1),
            market,
            daily_spends[day_num],
        )
        for day_num in range(days_elapsed)
    ]

    targets = OP2Targets(
        monthly_spend_target=monthly_target,
        monthly_reg_target=100,
        target_cpa=Decimal("50"),
    )

    return audit_date, metrics, targets, market


class TestPacingConsistency:
    """Property 2: Pacing Consistency.

    **Validates: Requirements 5.1**

    pacing_pct = (actual_spend / prorated_target) × 100
    where prorated_target = monthly_target × (days_elapsed / days_in_month)
    """

    @given(scenario=pacing_scenario())
    @settings(max_examples=200, deadline=None)
    def test_pacing_pct_equals_formula(
        self, scenario: tuple[date, list[NormalizedMetrics], OP2Targets, str]
    ) -> None:
        """pacing_pct must equal (actual_spend / prorated_target) × 100."""
        audit_date, metrics, targets, market = scenario
        engine = BudgetPacingEngine()

        result = engine.calculate_pacing(market, metrics, targets, audit_date)

        days_in_month = calendar.monthrange(audit_date.year, audit_date.month)[1]
        days_elapsed = audit_date.day

        actual_spend = sum((m.spend for m in metrics), Decimal("0"))
        prorated_target = (
            targets.monthly_spend_target * Decimal(days_elapsed) / Decimal(days_in_month)
        )

        if prorated_target == 0:
            assert result.pacing_pct == Decimal("0"), (
                f"Expected pacing_pct=0 when prorated_target=0, got {result.pacing_pct}"
            )
        else:
            expected_pacing = (actual_spend / prorated_target) * Decimal("100")
            assert result.pacing_pct == expected_pacing, (
                f"pacing_pct mismatch: got {result.pacing_pct}, "
                f"expected {expected_pacing} "
                f"(actual_spend={actual_spend}, prorated_target={prorated_target})"
            )

    @given(scenario=pacing_scenario())
    @settings(max_examples=200, deadline=None)
    def test_days_elapsed_plus_remaining_equals_days_in_month(
        self, scenario: tuple[date, list[NormalizedMetrics], OP2Targets, str]
    ) -> None:
        """days_elapsed + days_remaining must equal days_in_month."""
        audit_date, metrics, targets, market = scenario
        engine = BudgetPacingEngine()

        result = engine.calculate_pacing(market, metrics, targets, audit_date)

        days_in_month = calendar.monthrange(audit_date.year, audit_date.month)[1]
        assert result.days_elapsed + result.days_remaining == days_in_month, (
            f"Day accounting mismatch: {result.days_elapsed} + {result.days_remaining} "
            f"!= {days_in_month} for {audit_date}"
        )

    @given(scenario=pacing_scenario())
    @settings(max_examples=200, deadline=None)
    def test_status_matches_pacing_thresholds(
        self, scenario: tuple[date, list[NormalizedMetrics], OP2Targets, str]
    ) -> None:
        """Status classification must match pacing_pct thresholds:
        UNDERSPEND < 85%, ON_TRACK 85-110%, OVERSPEND > 110%.
        """
        audit_date, metrics, targets, market = scenario
        engine = BudgetPacingEngine()

        result = engine.calculate_pacing(market, metrics, targets, audit_date)

        if result.pacing_pct < Decimal("85"):
            assert result.status == "UNDERSPEND", (
                f"Expected UNDERSPEND for pacing_pct={result.pacing_pct}, "
                f"got {result.status}"
            )
        elif result.pacing_pct > Decimal("110"):
            assert result.status == "OVERSPEND", (
                f"Expected OVERSPEND for pacing_pct={result.pacing_pct}, "
                f"got {result.status}"
            )
        else:
            assert result.status == "ON_TRACK", (
                f"Expected ON_TRACK for pacing_pct={result.pacing_pct}, "
                f"got {result.status}"
            )
