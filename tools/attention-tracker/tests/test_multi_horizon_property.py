"""Property-based tests for multi-horizon projections.

**Validates: Requirements 6.2, 6.3, 6.7**

Property 15: Projection Run Rate Consistency — all three horizons use the same
             trailing 7-day daily run rate for both spend and registrations.

Property 16: Projection Arithmetic Integrity — projected_spend = actual_spend +
             (daily_spend_run_rate × days_remaining) for every horizon.

Property 17: Period Day Accounting — days_elapsed + days_remaining = days_total
             for all period projections.
"""

from __future__ import annotations

import calendar
from datetime import date, timedelta
from decimal import Decimal

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from paid_search_audit.budget_pacing import BudgetPacingEngine
from paid_search_audit.config import OP2Targets
from paid_search_audit.models import NormalizedMetrics

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

audit_date_strategy = st.dates(min_value=date(2024, 1, 8), max_value=date(2027, 12, 31))

market_strategy = st.sampled_from(["AU", "MX", "US", "JP", "CA", "DE"])

daily_spend_strategy = st.decimals(
    min_value=Decimal("0"),
    max_value=Decimal("50000"),
    allow_nan=False,
    allow_infinity=False,
    places=2,
)

daily_conversions_strategy = st.integers(min_value=0, max_value=500)

target_spend_strategy = st.decimals(
    min_value=Decimal("0"),
    max_value=Decimal("10000000"),
    allow_nan=False,
    allow_infinity=False,
    places=2,
)

target_regs_strategy = st.integers(min_value=0, max_value=100000)


def _build_metric(
    metric_date: date,
    market: str,
    spend: Decimal,
    conversions: int,
) -> NormalizedMetrics:
    """Build a minimal NormalizedMetrics row."""
    return NormalizedMetrics(
        date=metric_date,
        market=market,
        campaign_type="Brand",
        campaign_name="test-campaign",
        account_id="1234567890",
        mcc_id="0987654321",
        impressions=1000,
        clicks=50,
        spend=spend,
        spend_usd=spend,
        conversions=conversions,
        source="GOOGLE_ADS",
    )


@st.composite
def multi_horizon_scenario(draw):
    """Generate a scenario with at least 7 days of trailing metrics.

    Returns (audit_date, metrics, targets, market).
    Metrics cover the trailing 7 days up to and including audit_date,
    plus any earlier days in the current month so MTD actuals are realistic.
    """
    audit_date = draw(audit_date_strategy)
    market = draw(market_strategy)

    # Ensure audit_date is at least day 1 (always true) and we have room
    # for 7 trailing days.  The date strategy min is Jan 8 2024 so this holds.
    assume(audit_date >= date(2024, 1, 8))

    # Generate daily spend/conversions for each day from month-start to audit_date
    month_start = audit_date.replace(day=1)
    num_days = (audit_date - month_start).days + 1

    daily_spends = draw(
        st.lists(daily_spend_strategy, min_size=num_days, max_size=num_days)
    )
    daily_convs = draw(
        st.lists(daily_conversions_strategy, min_size=num_days, max_size=num_days)
    )

    metrics: list[NormalizedMetrics] = []
    for i in range(num_days):
        d = month_start + timedelta(days=i)
        metrics.append(_build_metric(d, market, daily_spends[i], daily_convs[i]))

    # Also add metrics for trailing days before month-start (if needed for
    # the 7-day window).  E.g. if audit_date is March 3, we need March 1-3
    # plus a few days from February.
    window_start = audit_date - timedelta(days=6)
    if window_start < month_start:
        extra_start = window_start
        extra_end = month_start - timedelta(days=1)
        extra_days = (extra_end - extra_start).days + 1
        extra_spends = draw(
            st.lists(daily_spend_strategy, min_size=extra_days, max_size=extra_days)
        )
        extra_convs = draw(
            st.lists(daily_conversions_strategy, min_size=extra_days, max_size=extra_days)
        )
        for i in range(extra_days):
            d = extra_start + timedelta(days=i)
            metrics.append(_build_metric(d, market, extra_spends[i], extra_convs[i]))

    # Targets
    monthly_spend = draw(target_spend_strategy)
    monthly_regs = draw(target_regs_strategy)
    quarterly_spend = draw(target_spend_strategy)
    quarterly_regs = draw(target_regs_strategy)
    yearly_spend = draw(target_spend_strategy)
    yearly_regs = draw(target_regs_strategy)
    target_cpa = draw(
        st.decimals(
            min_value=Decimal("0.01"),
            max_value=Decimal("10000"),
            allow_nan=False,
            allow_infinity=False,
            places=2,
        )
    )

    targets = OP2Targets(
        monthly_spend_target=monthly_spend,
        monthly_reg_target=monthly_regs,
        target_cpa=target_cpa,
        quarterly_spend_target=quarterly_spend,
        quarterly_reg_target=quarterly_regs,
        yearly_spend_target=yearly_spend,
        yearly_reg_target=yearly_regs,
        yearly_target_cpa=target_cpa,
    )

    return audit_date, metrics, targets, market


# ---------------------------------------------------------------------------
# Property 15: Projection Run Rate Consistency
# ---------------------------------------------------------------------------

class TestProjectionRunRateConsistency:
    """Property 15: Projection Run Rate Consistency.

    **Validates: Requirements 6.2**

    All three horizons (monthly, quarterly, yearly) must use the same
    trailing 7-day daily run rate for both spend and registrations.
    """

    @given(scenario=multi_horizon_scenario())
    @settings(max_examples=200, deadline=None)
    def test_spend_run_rate_same_across_horizons(
        self, scenario: tuple[date, list[NormalizedMetrics], OP2Targets, str]
    ) -> None:
        """daily_spend_run_rate must be identical for monthly, quarterly, yearly."""
        audit_date, metrics, targets, market = scenario
        engine = BudgetPacingEngine()

        result = engine.project_multi_horizon(market, metrics, targets, audit_date)

        m = result.monthly
        q = result.quarterly
        y = result.yearly

        assert m.daily_spend_run_rate == q.daily_spend_run_rate, (
            f"Monthly spend run rate ({m.daily_spend_run_rate}) != "
            f"Quarterly ({q.daily_spend_run_rate})"
        )
        assert m.daily_spend_run_rate == y.daily_spend_run_rate, (
            f"Monthly spend run rate ({m.daily_spend_run_rate}) != "
            f"Yearly ({y.daily_spend_run_rate})"
        )

    @given(scenario=multi_horizon_scenario())
    @settings(max_examples=200, deadline=None)
    def test_regs_run_rate_same_across_horizons(
        self, scenario: tuple[date, list[NormalizedMetrics], OP2Targets, str]
    ) -> None:
        """daily_regs_run_rate must be identical for monthly, quarterly, yearly."""
        audit_date, metrics, targets, market = scenario
        engine = BudgetPacingEngine()

        result = engine.project_multi_horizon(market, metrics, targets, audit_date)

        m = result.monthly
        q = result.quarterly
        y = result.yearly

        assert m.daily_regs_run_rate == q.daily_regs_run_rate, (
            f"Monthly regs run rate ({m.daily_regs_run_rate}) != "
            f"Quarterly ({q.daily_regs_run_rate})"
        )
        assert m.daily_regs_run_rate == y.daily_regs_run_rate, (
            f"Monthly regs run rate ({m.daily_regs_run_rate}) != "
            f"Yearly ({y.daily_regs_run_rate})"
        )


# ---------------------------------------------------------------------------
# Property 16: Projection Arithmetic Integrity
# ---------------------------------------------------------------------------

class TestProjectionArithmeticIntegrity:
    """Property 16: Projection Arithmetic Integrity.

    **Validates: Requirements 6.3**

    For each horizon: projected_spend = actual_spend + (daily_spend_run_rate × days_remaining).
    """

    @given(scenario=multi_horizon_scenario())
    @settings(max_examples=200, deadline=None)
    def test_monthly_projected_spend_formula(
        self, scenario: tuple[date, list[NormalizedMetrics], OP2Targets, str]
    ) -> None:
        audit_date, metrics, targets, market = scenario
        engine = BudgetPacingEngine()
        result = engine.project_multi_horizon(market, metrics, targets, audit_date)

        m = result.monthly
        expected = m.actual_spend + (m.daily_spend_run_rate * Decimal(m.days_remaining))
        assert m.projected_spend == expected, (
            f"Monthly: {m.projected_spend} != {m.actual_spend} + "
            f"({m.daily_spend_run_rate} × {m.days_remaining}) = {expected}"
        )

    @given(scenario=multi_horizon_scenario())
    @settings(max_examples=200, deadline=None)
    def test_quarterly_projected_spend_formula(
        self, scenario: tuple[date, list[NormalizedMetrics], OP2Targets, str]
    ) -> None:
        audit_date, metrics, targets, market = scenario
        engine = BudgetPacingEngine()
        result = engine.project_multi_horizon(market, metrics, targets, audit_date)

        q = result.quarterly
        expected = q.actual_spend + (q.daily_spend_run_rate * Decimal(q.days_remaining))
        assert q.projected_spend == expected, (
            f"Quarterly: {q.projected_spend} != {q.actual_spend} + "
            f"({q.daily_spend_run_rate} × {q.days_remaining}) = {expected}"
        )

    @given(scenario=multi_horizon_scenario())
    @settings(max_examples=200, deadline=None)
    def test_yearly_projected_spend_formula(
        self, scenario: tuple[date, list[NormalizedMetrics], OP2Targets, str]
    ) -> None:
        audit_date, metrics, targets, market = scenario
        engine = BudgetPacingEngine()
        result = engine.project_multi_horizon(market, metrics, targets, audit_date)

        y = result.yearly
        expected = y.actual_spend + (y.daily_spend_run_rate * Decimal(y.days_remaining))
        assert y.projected_spend == expected, (
            f"Yearly: {y.projected_spend} != {y.actual_spend} + "
            f"({y.daily_spend_run_rate} × {y.days_remaining}) = {expected}"
        )


# ---------------------------------------------------------------------------
# Property 17: Period Day Accounting
# ---------------------------------------------------------------------------

class TestPeriodDayAccounting:
    """Property 17: Period Day Accounting.

    **Validates: Requirements 6.7**

    For every period projection: days_elapsed + days_remaining = days_total.
    """

    @given(scenario=multi_horizon_scenario())
    @settings(max_examples=200, deadline=None)
    def test_monthly_day_accounting(
        self, scenario: tuple[date, list[NormalizedMetrics], OP2Targets, str]
    ) -> None:
        audit_date, metrics, targets, market = scenario
        engine = BudgetPacingEngine()
        result = engine.project_multi_horizon(market, metrics, targets, audit_date)

        m = result.monthly
        assert m.days_elapsed + m.days_remaining == m.days_total, (
            f"Monthly: {m.days_elapsed} + {m.days_remaining} != {m.days_total} "
            f"(audit_date={audit_date})"
        )

    @given(scenario=multi_horizon_scenario())
    @settings(max_examples=200, deadline=None)
    def test_quarterly_day_accounting(
        self, scenario: tuple[date, list[NormalizedMetrics], OP2Targets, str]
    ) -> None:
        audit_date, metrics, targets, market = scenario
        engine = BudgetPacingEngine()
        result = engine.project_multi_horizon(market, metrics, targets, audit_date)

        q = result.quarterly
        assert q.days_elapsed + q.days_remaining == q.days_total, (
            f"Quarterly: {q.days_elapsed} + {q.days_remaining} != {q.days_total} "
            f"(audit_date={audit_date})"
        )

    @given(scenario=multi_horizon_scenario())
    @settings(max_examples=200, deadline=None)
    def test_yearly_day_accounting(
        self, scenario: tuple[date, list[NormalizedMetrics], OP2Targets, str]
    ) -> None:
        audit_date, metrics, targets, market = scenario
        engine = BudgetPacingEngine()
        result = engine.project_multi_horizon(market, metrics, targets, audit_date)

        y = result.yearly
        assert y.days_elapsed + y.days_remaining == y.days_total, (
            f"Yearly: {y.days_elapsed} + {y.days_remaining} != {y.days_total} "
            f"(audit_date={audit_date})"
        )
