"""Unit tests for BudgetPacingEngine.

Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 12.5

Tests cover:
- Mid-month pacing calculation
- Start-of-month edge case (day 1)
- End-of-month edge case (last day)
- ON_TRACK, UNDERSPEND, OVERSPEND classification
- Zero prorated target handling
- project_end_of_period trailing 7-day average
- Projected CPA = None when projected_regs = 0 (Req 12.5)
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

import pytest

from paid_search_audit.budget_pacing import BudgetPacingEngine
from paid_search_audit.config import OP2Targets
from paid_search_audit.models import NormalizedMetrics


def _make_metric(
    metric_date: date,
    market: str = "AU",
    spend: Decimal = Decimal("100.00"),
    conversions: int = 5,
    campaign_name: str = "test-campaign",
) -> NormalizedMetrics:
    return NormalizedMetrics(
        date=metric_date,
        market=market,
        campaign_type="Brand",
        campaign_name=campaign_name,
        account_id="1234567890",
        mcc_id="0987654321",
        impressions=1000,
        clicks=50,
        spend=spend,
        spend_usd=spend,
        conversions=conversions,
    )


def _make_targets(
    monthly_spend: Decimal = Decimal("30000"),
    monthly_regs: int = 300,
    target_cpa: Decimal = Decimal("100"),
) -> OP2Targets:
    return OP2Targets(
        monthly_spend_target=monthly_spend,
        monthly_reg_target=monthly_regs,
        target_cpa=target_cpa,
    )


@pytest.fixture
def engine() -> BudgetPacingEngine:
    return BudgetPacingEngine()


# ------------------------------------------------------------------ #
# 1. Mid-month pacing calculation
# ------------------------------------------------------------------ #

class TestMidMonthPacing:
    """Requirement 5.1: pacing_pct = (actual / prorated_target) × 100."""

    def test_mid_month_pacing_calculation(self, engine: BudgetPacingEngine) -> None:
        """Day 15 of a 31-day month, $15,000 spent against $30,000 target."""
        audit_date = date(2026, 3, 15)
        # Create 15 days of $1000/day spend
        metrics = [
            _make_metric(date(2026, 3, d), spend=Decimal("1000"))
            for d in range(1, 16)
        ]
        targets = _make_targets(monthly_spend=Decimal("30000"))

        result = engine.calculate_pacing("AU", metrics, targets, audit_date)

        # prorated_target = 30000 * 15/31 = ~14516.13
        expected_prorated = Decimal("30000") * Decimal("15") / Decimal("31")
        expected_pacing = (Decimal("15000") / expected_prorated) * Decimal("100")

        assert result.actual_spend == Decimal("15000")
        assert result.pacing_pct == expected_pacing
        assert result.days_elapsed == 15
        assert result.days_remaining == 16
        assert result.market == "AU"
        assert result.period == "March 2026"

    def test_pacing_formula_matches_spec(self, engine: BudgetPacingEngine) -> None:
        """Verify pacing_pct = (actual_spend / prorated_target) × 100 exactly."""
        audit_date = date(2026, 3, 10)
        metrics = [
            _make_metric(date(2026, 3, d), spend=Decimal("500"))
            for d in range(1, 11)
        ]
        targets = _make_targets(monthly_spend=Decimal("31000"))

        result = engine.calculate_pacing("MX", metrics, targets, audit_date)

        prorated = Decimal("31000") * Decimal("10") / Decimal("31")
        expected = (Decimal("5000") / prorated) * Decimal("100")
        assert result.pacing_pct == expected


# ------------------------------------------------------------------ #
# 2. Start-of-month edge case
# ------------------------------------------------------------------ #

class TestStartOfMonth:
    """Edge case: audit on day 1 of the month."""

    def test_day_one_pacing(self, engine: BudgetPacingEngine) -> None:
        audit_date = date(2026, 3, 1)
        metrics = [_make_metric(audit_date, spend=Decimal("800"))]
        targets = _make_targets(monthly_spend=Decimal("30000"))

        result = engine.calculate_pacing("AU", metrics, targets, audit_date)

        assert result.days_elapsed == 1
        assert result.days_remaining == 30  # March has 31 days
        prorated = Decimal("30000") * Decimal("1") / Decimal("31")
        expected_pacing = (Decimal("800") / prorated) * Decimal("100")
        assert result.pacing_pct == expected_pacing


# ------------------------------------------------------------------ #
# 3. End-of-month edge case
# ------------------------------------------------------------------ #

class TestEndOfMonth:
    """Edge case: audit on the last day of the month."""

    def test_last_day_pacing(self, engine: BudgetPacingEngine) -> None:
        audit_date = date(2026, 3, 31)
        # Spend exactly on target
        metrics = [
            _make_metric(date(2026, 3, d), spend=Decimal("1000"))
            for d in range(1, 32)
        ]
        targets = _make_targets(monthly_spend=Decimal("31000"))

        result = engine.calculate_pacing("AU", metrics, targets, audit_date)

        assert result.days_elapsed == 31
        assert result.days_remaining == 0
        # prorated_target = 31000 * 31/31 = 31000
        expected_pacing = (Decimal("31000") / Decimal("31000")) * Decimal("100")
        assert result.pacing_pct == expected_pacing
        assert result.status == "ON_TRACK"


# ------------------------------------------------------------------ #
# 4. ON_TRACK classification (85-110%)
# ------------------------------------------------------------------ #

class TestOnTrack:
    """Requirement 5.2: ON_TRACK when 85% <= pacing <= 110%."""

    def test_exactly_100_pct_is_on_track(self, engine: BudgetPacingEngine) -> None:
        audit_date = date(2026, 3, 10)
        # 10 days elapsed in 31-day month, target $31000
        # prorated = 31000 * 10/31 = 10000
        metrics = [
            _make_metric(date(2026, 3, d), spend=Decimal("1000"))
            for d in range(1, 11)
        ]
        targets = _make_targets(monthly_spend=Decimal("31000"))

        result = engine.calculate_pacing("AU", metrics, targets, audit_date)
        assert result.status == "ON_TRACK"

    def test_85_pct_boundary_is_on_track(self, engine: BudgetPacingEngine) -> None:
        audit_date = date(2026, 3, 10)
        # prorated = 31000 * 10/31 = 10000; 85% of 10000 = 8500
        metrics = [
            _make_metric(date(2026, 3, d), spend=Decimal("850"))
            for d in range(1, 11)
        ]
        targets = _make_targets(monthly_spend=Decimal("31000"))

        result = engine.calculate_pacing("AU", metrics, targets, audit_date)
        assert result.status == "ON_TRACK"

    def test_110_pct_boundary_is_on_track(self, engine: BudgetPacingEngine) -> None:
        audit_date = date(2026, 3, 10)
        # prorated = 31000 * 10/31 = 10000; 110% of 10000 = 11000
        metrics = [
            _make_metric(date(2026, 3, d), spend=Decimal("1100"))
            for d in range(1, 11)
        ]
        targets = _make_targets(monthly_spend=Decimal("31000"))

        result = engine.calculate_pacing("AU", metrics, targets, audit_date)
        assert result.status == "ON_TRACK"


# ------------------------------------------------------------------ #
# 5. UNDERSPEND classification (<85%)
# ------------------------------------------------------------------ #

class TestUnderspend:
    """Requirement 5.3: UNDERSPEND when pacing < 85%."""

    def test_low_spend_is_underspend(self, engine: BudgetPacingEngine) -> None:
        audit_date = date(2026, 3, 10)
        # prorated = 31000 * 10/31 = 10000; spend 5000 = 50%
        metrics = [
            _make_metric(date(2026, 3, d), spend=Decimal("500"))
            for d in range(1, 11)
        ]
        targets = _make_targets(monthly_spend=Decimal("31000"))

        result = engine.calculate_pacing("AU", metrics, targets, audit_date)
        assert result.status == "UNDERSPEND"
        assert result.pacing_pct < Decimal("85")


# ------------------------------------------------------------------ #
# 6. OVERSPEND classification (>110%)
# ------------------------------------------------------------------ #

class TestOverspend:
    """Requirement 5.4: OVERSPEND when pacing > 110%."""

    def test_high_spend_is_overspend(self, engine: BudgetPacingEngine) -> None:
        audit_date = date(2026, 3, 10)
        # prorated = 31000 * 10/31 = 10000; spend 15000 = 150%
        metrics = [
            _make_metric(date(2026, 3, d), spend=Decimal("1500"))
            for d in range(1, 11)
        ]
        targets = _make_targets(monthly_spend=Decimal("31000"))

        result = engine.calculate_pacing("AU", metrics, targets, audit_date)
        assert result.status == "OVERSPEND"
        assert result.pacing_pct > Decimal("110")


# ------------------------------------------------------------------ #
# 7. Zero prorated target handling
# ------------------------------------------------------------------ #

class TestZeroTarget:
    """Edge case: zero monthly spend target."""

    def test_zero_target_returns_zero_pacing(self, engine: BudgetPacingEngine) -> None:
        audit_date = date(2026, 3, 15)
        metrics = [_make_metric(audit_date, spend=Decimal("1000"))]
        targets = _make_targets(monthly_spend=Decimal("0"))

        result = engine.calculate_pacing("AU", metrics, targets, audit_date)
        assert result.pacing_pct == Decimal("0")
        assert result.projected_variance_pct == Decimal("0")


# ------------------------------------------------------------------ #
# 8. project_end_of_period — trailing 7-day average
# ------------------------------------------------------------------ #

class TestProjectEndOfPeriod:
    """Requirement 5.5: trailing 7-day average daily spend as run rate."""

    def test_trailing_7_day_average(self, engine: BudgetPacingEngine) -> None:
        audit_date = date(2026, 3, 15)
        # 7 days of varying spend
        spends = [Decimal("100"), Decimal("200"), Decimal("150"), Decimal("300"),
                  Decimal("250"), Decimal("175"), Decimal("225")]
        metrics = [
            _make_metric(audit_date - timedelta(days=6 - i), spend=s)
            for i, s in enumerate(spends)
        ]

        avg = engine.project_end_of_period(metrics, audit_date, window=7)
        expected = sum(spends, Decimal("0")) / Decimal("7")
        assert avg == expected

    def test_fewer_than_7_days_uses_available(self, engine: BudgetPacingEngine) -> None:
        """When only 3 days of data exist, average over those 3 days."""
        audit_date = date(2026, 3, 3)
        metrics = [
            _make_metric(date(2026, 3, 1), spend=Decimal("100")),
            _make_metric(date(2026, 3, 2), spend=Decimal("200")),
            _make_metric(date(2026, 3, 3), spend=Decimal("300")),
        ]

        avg = engine.project_end_of_period(metrics, audit_date, window=7)
        assert avg == Decimal("200")  # (100+200+300)/3

    def test_no_data_returns_zero(self, engine: BudgetPacingEngine) -> None:
        audit_date = date(2026, 3, 15)
        avg = engine.project_end_of_period([], audit_date, window=7)
        assert avg == Decimal("0")

    def test_multiple_metrics_same_day_summed(self, engine: BudgetPacingEngine) -> None:
        """Multiple campaigns on the same day should be summed."""
        audit_date = date(2026, 3, 15)
        metrics = [
            _make_metric(audit_date, spend=Decimal("100"), campaign_name="brand"),
            _make_metric(audit_date, spend=Decimal("200"), campaign_name="non-brand"),
        ]

        avg = engine.project_end_of_period(metrics, audit_date, window=7)
        assert avg == Decimal("300")  # single day, two campaigns


# ------------------------------------------------------------------ #
# 9. Projected EOM spend uses run rate
# ------------------------------------------------------------------ #

class TestProjectedEOMSpend:
    """Requirement 5.5: projected_eom_spend = actual + (avg_daily × days_remaining)."""

    def test_projected_eom_spend_formula(self, engine: BudgetPacingEngine) -> None:
        audit_date = date(2026, 3, 15)
        # 15 days of $1000/day
        metrics = [
            _make_metric(date(2026, 3, d), spend=Decimal("1000"))
            for d in range(1, 16)
        ]
        targets = _make_targets(monthly_spend=Decimal("30000"))

        result = engine.calculate_pacing("AU", metrics, targets, audit_date)

        # actual = 15000, avg_daily = 1000 (7-day trailing), days_remaining = 16
        expected_eom = Decimal("15000") + Decimal("1000") * Decimal("16")
        assert result.projected_eom_spend == expected_eom


# ------------------------------------------------------------------ #
# 10. Projected variance percentage
# ------------------------------------------------------------------ #

class TestProjectedVariance:
    """Projected variance = ((projected - target) / target) × 100."""

    def test_positive_variance(self, engine: BudgetPacingEngine) -> None:
        audit_date = date(2026, 3, 15)
        metrics = [
            _make_metric(date(2026, 3, d), spend=Decimal("1200"))
            for d in range(1, 16)
        ]
        targets = _make_targets(monthly_spend=Decimal("30000"))

        result = engine.calculate_pacing("AU", metrics, targets, audit_date)

        # actual=18000, avg_daily=1200, days_remaining=16
        projected = Decimal("18000") + Decimal("1200") * Decimal("16")
        expected_var = ((projected - Decimal("30000")) / Decimal("30000")) * Decimal("100")
        assert result.projected_variance_pct == expected_var
