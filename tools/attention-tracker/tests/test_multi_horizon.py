"""Unit tests for multi-horizon projections in BudgetPacingEngine.

Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 12.5
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

import pytest

from paid_search_audit.budget_pacing import BudgetPacingEngine
from paid_search_audit.config import OP2Targets
from paid_search_audit.data_store import DataStore
from paid_search_audit.models import NormalizedMetrics


# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #

def _metric(
    metric_date: date,
    market: str = "AU",
    spend: Decimal = Decimal("100"),
    conversions: int = 5,
    campaign_name: str = "campaign-1",
) -> NormalizedMetrics:
    return NormalizedMetrics(
        date=metric_date,
        market=market,
        campaign_type="Brand",
        campaign_name=campaign_name,
        account_id="111",
        mcc_id="222",
        impressions=1000,
        clicks=50,
        spend=spend,
        spend_usd=spend,
        conversions=conversions,
    )


def _targets(
    monthly_spend: Decimal = Decimal("30000"),
    monthly_regs: int = 300,
    target_cpa: Decimal = Decimal("100"),
    quarterly_spend: Decimal = Decimal("90000"),
    quarterly_regs: int = 900,
    yearly_spend: Decimal = Decimal("360000"),
    yearly_regs: int = 3600,
    yearly_cpa: Decimal = Decimal("100"),
) -> OP2Targets:
    return OP2Targets(
        monthly_spend_target=monthly_spend,
        monthly_reg_target=monthly_regs,
        target_cpa=target_cpa,
        quarterly_spend_target=quarterly_spend,
        quarterly_reg_target=quarterly_regs,
        yearly_spend_target=yearly_spend,
        yearly_reg_target=yearly_regs,
        yearly_target_cpa=yearly_cpa,
    )


@pytest.fixture
def engine() -> BudgetPacingEngine:
    return BudgetPacingEngine()


@pytest.fixture
def store() -> DataStore:
    ds = DataStore(":memory:")
    yield ds
    ds.close()


# ------------------------------------------------------------------ #
# 1. All three horizons returned (Req 6.1)
# ------------------------------------------------------------------ #

class TestMultiHorizonStructure:
    """Req 6.1: projections for monthly, quarterly, and yearly."""

    def test_returns_all_three_horizons(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d)) for d in range(9, 16)]
        result = engine.project_multi_horizon("AU", metrics, _targets(), audit)

        assert result.market == "AU"
        assert result.audit_date == audit
        assert result.monthly is not None
        assert result.quarterly is not None
        assert result.yearly is not None

    def test_period_types(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d)) for d in range(9, 16)]
        result = engine.project_multi_horizon("AU", metrics, _targets(), audit)

        assert result.monthly.period_type == "MONTHLY"
        assert result.quarterly.period_type == "QUARTERLY"
        assert result.yearly.period_type == "YEARLY"


# ------------------------------------------------------------------ #
# 2. Same run rate across all horizons (Req 6.2)
# ------------------------------------------------------------------ #

class TestRunRateConsistency:
    """Req 6.2: same trailing 7-day run rate for all horizons."""

    def test_all_horizons_share_run_rate(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [
            _metric(date(2026, 3, d), spend=Decimal(str(d * 100)), conversions=d)
            for d in range(9, 16)
        ]
        result = engine.project_multi_horizon("AU", metrics, _targets(), audit)

        assert result.monthly.daily_spend_run_rate == result.quarterly.daily_spend_run_rate
        assert result.monthly.daily_spend_run_rate == result.yearly.daily_spend_run_rate
        assert result.monthly.daily_regs_run_rate == result.quarterly.daily_regs_run_rate
        assert result.monthly.daily_regs_run_rate == result.yearly.daily_regs_run_rate


# ------------------------------------------------------------------ #
# 3. Projected spend formula (Req 6.3)
# ------------------------------------------------------------------ #

class TestProjectedSpend:
    """Req 6.3: projected_spend = actual + run_rate × days_remaining."""

    def test_monthly_projected_spend(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d), spend=Decimal("1000")) for d in range(1, 16)]
        result = engine.project_multi_horizon("AU", metrics, _targets(), audit)

        m = result.monthly
        expected = m.actual_spend + (m.daily_spend_run_rate * Decimal(m.days_remaining))
        assert m.projected_spend == expected


# ------------------------------------------------------------------ #
# 4. Projected registrations formula (Req 6.4)
# ------------------------------------------------------------------ #

class TestProjectedRegs:
    """Req 6.4: projected_regs = actual + round(run_rate × days_remaining)."""

    def test_monthly_projected_regs(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d), conversions=10) for d in range(1, 16)]
        result = engine.project_multi_horizon("AU", metrics, _targets(), audit)

        m = result.monthly
        expected = m.actual_regs + round(m.daily_regs_run_rate * Decimal(m.days_remaining))
        assert m.projected_regs == expected


# ------------------------------------------------------------------ #
# 5. Projected CPA (Req 6.5, 12.5)
# ------------------------------------------------------------------ #

class TestProjectedCPA:
    """Req 6.5: projected_cpa = projected_spend / projected_regs."""

    def test_projected_cpa_computed(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d), spend=Decimal("1000"), conversions=10) for d in range(1, 16)]
        result = engine.project_multi_horizon("AU", metrics, _targets(), audit)

        m = result.monthly
        assert m.projected_cpa is not None
        assert m.projected_cpa == m.projected_spend / Decimal(m.projected_regs)

    def test_projected_cpa_none_when_zero_regs(self, engine: BudgetPacingEngine) -> None:
        """Req 12.5: projected CPA is None when projected_regs == 0."""
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d), spend=Decimal("1000"), conversions=0) for d in range(9, 16)]
        result = engine.project_multi_horizon("AU", metrics, _targets(), audit)

        m = result.monthly
        assert m.projected_regs == 0
        assert m.projected_cpa is None


# ------------------------------------------------------------------ #
# 6. vs OP2 percentages (Req 6.6)
# ------------------------------------------------------------------ #

class TestVsOP2:
    """Req 6.6: ((projected - target) / target) × 100."""

    def test_spend_vs_op2(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d), spend=Decimal("1000")) for d in range(1, 16)]
        targets = _targets(monthly_spend=Decimal("30000"))
        result = engine.project_multi_horizon("AU", metrics, targets, audit)

        m = result.monthly
        expected = ((m.projected_spend - Decimal("30000")) / Decimal("30000")) * Decimal("100")
        assert m.spend_vs_op2_pct == expected

    def test_regs_vs_op2(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d), conversions=10) for d in range(1, 16)]
        targets = _targets(monthly_regs=300)
        result = engine.project_multi_horizon("AU", metrics, targets, audit)

        m = result.monthly
        expected = ((Decimal(m.projected_regs) - Decimal("300")) / Decimal("300")) * Decimal("100")
        assert m.regs_vs_op2_pct == expected

    def test_zero_target_returns_zero_pct(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d)) for d in range(9, 16)]
        targets = _targets(monthly_spend=Decimal("0"), monthly_regs=0)
        result = engine.project_multi_horizon("AU", metrics, targets, audit)

        assert result.monthly.spend_vs_op2_pct == Decimal("0")
        assert result.monthly.regs_vs_op2_pct == Decimal("0")


# ------------------------------------------------------------------ #
# 7. Day accounting (Req 6.7)
# ------------------------------------------------------------------ #

class TestDayAccounting:
    """Req 6.7: days_elapsed + days_remaining = days_total."""

    def test_monthly_day_accounting(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d)) for d in range(9, 16)]
        result = engine.project_multi_horizon("AU", metrics, _targets(), audit)

        m = result.monthly
        assert m.days_elapsed + m.days_remaining == m.days_total
        assert m.days_total == 31  # March

    def test_quarterly_day_accounting(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d)) for d in range(9, 16)]
        result = engine.project_multi_horizon("AU", metrics, _targets(), audit)

        q = result.quarterly
        assert q.days_elapsed + q.days_remaining == q.days_total
        # Q1 2026: Jan(31) + Feb(28) + Mar(31) = 90
        assert q.days_total == 90

    def test_yearly_day_accounting(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d)) for d in range(9, 16)]
        result = engine.project_multi_horizon("AU", metrics, _targets(), audit)

        y = result.yearly
        assert y.days_elapsed + y.days_remaining == y.days_total
        assert y.days_total == 365  # 2026 is not a leap year


# ------------------------------------------------------------------ #
# 8. QTD loads prior months from DataStore (Req 6.8)
# ------------------------------------------------------------------ #

class TestQTDPriorMonths:
    """Req 6.8: QTD includes prior month actuals from DataStore."""

    def test_qtd_includes_prior_month_actuals(
        self, engine: BudgetPacingEngine, store: DataStore
    ) -> None:
        # Store January and February data
        jan_metrics = [_metric(date(2026, 1, d), spend=Decimal("500"), conversions=5) for d in range(1, 32)]
        feb_metrics = [_metric(date(2026, 2, d), spend=Decimal("600"), conversions=6) for d in range(1, 29)]
        store.store_metrics(jan_metrics, date(2026, 1, 31))
        store.store_metrics(feb_metrics, date(2026, 2, 28))

        # Current month metrics
        audit = date(2026, 3, 10)
        mar_metrics = [_metric(date(2026, 3, d), spend=Decimal("700"), conversions=7) for d in range(1, 11)]

        result = engine.project_multi_horizon("AU", mar_metrics, _targets(), audit, data_store=store)

        q = result.quarterly
        # QTD spend = Jan(31*500) + Feb(28*600) + Mar(10*700)
        expected_spend = Decimal("500") * 31 + Decimal("600") * 28 + Decimal("700") * 10
        assert q.actual_spend == expected_spend

        expected_regs = 5 * 31 + 6 * 28 + 7 * 10
        assert q.actual_regs == expected_regs

    def test_qtd_without_datastore_uses_current_month_only(
        self, engine: BudgetPacingEngine
    ) -> None:
        """When no DataStore is provided, QTD only has current month data."""
        audit = date(2026, 3, 10)
        metrics = [_metric(date(2026, 3, d), spend=Decimal("700"), conversions=7) for d in range(1, 11)]

        result = engine.project_multi_horizon("AU", metrics, _targets(), audit)

        q = result.quarterly
        # Only current month data
        assert q.actual_spend == Decimal("700") * 10
        assert q.actual_regs == 7 * 10


# ------------------------------------------------------------------ #
# 9. YTD from DataStore
# ------------------------------------------------------------------ #

class TestYTDFromDataStore:
    """YTD actuals loaded from DataStore when available."""

    def test_ytd_uses_datastore(
        self, engine: BudgetPacingEngine, store: DataStore
    ) -> None:
        # Store some data for Jan-Mar
        for month in range(1, 4):
            days = 31 if month in (1, 3) else 28
            ms = [_metric(date(2026, month, d), spend=Decimal("100"), conversions=2) for d in range(1, days + 1)]
            store.store_metrics(ms, date(2026, month, days))

        audit = date(2026, 3, 15)
        mar_metrics = [_metric(date(2026, 3, d), spend=Decimal("100"), conversions=2) for d in range(1, 16)]

        result = engine.project_multi_horizon("AU", mar_metrics, _targets(), audit, data_store=store)

        y = result.yearly
        # YTD = Jan(31*100) + Feb(28*100) + Mar(15*100) = 7400
        expected_spend = Decimal("100") * (31 + 28 + 15)
        assert y.actual_spend == expected_spend


# ------------------------------------------------------------------ #
# 10. Pacing percentage
# ------------------------------------------------------------------ #

class TestPacingPct:
    """Pacing = (actual / prorated_target) × 100."""

    def test_monthly_pacing(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d), spend=Decimal("1000")) for d in range(1, 16)]
        targets = _targets(monthly_spend=Decimal("31000"))
        result = engine.project_multi_horizon("AU", metrics, targets, audit)

        m = result.monthly
        prorated = Decimal("31000") * Decimal("15") / Decimal("31")
        expected = (Decimal("15000") / prorated) * Decimal("100")
        assert m.spend_pacing_pct == expected


# ------------------------------------------------------------------ #
# 11. Period labels
# ------------------------------------------------------------------ #

class TestPeriodLabels:
    """Verify human-readable period labels."""

    def test_labels(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 15)
        metrics = [_metric(date(2026, 3, d)) for d in range(9, 16)]
        result = engine.project_multi_horizon("AU", metrics, _targets(), audit)

        assert result.monthly.period_label == "March 2026"
        assert result.quarterly.period_label == "Q1 FY26"
        assert result.yearly.period_label == "FY26"


# ------------------------------------------------------------------ #
# 12. Status classification
# ------------------------------------------------------------------ #

class TestStatusClassification:
    """Status derived from spend pacing percentage."""

    def test_on_track(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 10)
        metrics = [_metric(date(2026, 3, d), spend=Decimal("1000")) for d in range(1, 11)]
        targets = _targets(monthly_spend=Decimal("31000"))
        result = engine.project_multi_horizon("AU", metrics, targets, audit)
        assert result.monthly.status == "ON_TRACK"

    def test_underspend(self, engine: BudgetPacingEngine) -> None:
        audit = date(2026, 3, 10)
        metrics = [_metric(date(2026, 3, d), spend=Decimal("200")) for d in range(1, 11)]
        targets = _targets(monthly_spend=Decimal("31000"))
        result = engine.project_multi_horizon("AU", metrics, targets, audit)
        assert result.monthly.status == "UNDERSPEND"
