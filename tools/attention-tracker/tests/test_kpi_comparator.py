"""Unit tests for KPIComparator.

Validates: Requirements 8.1, 8.2, 8.3, 8.4

Tests cover:
- compare_to_targets returns findings for spend, registrations, CPA
- compute_goal_progress pacing formula
- AT_RISK flagging when pacing < 90%
- ON_TRACK when pacing >= 90%
- Kingpin Goal (MX registrations) flagged correctly
- CPA comparison (higher = worse)
- Edge cases: zero targets, day 1, None CPA
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from paid_search_audit.config import OP2Targets
from paid_search_audit.kpi_comparator import KPIComparator, KPIFinding, GoalProgress


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
def comparator() -> KPIComparator:
    return KPIComparator()


# ------------------------------------------------------------------ #
# 1. compute_goal_progress — pacing formula
# ------------------------------------------------------------------ #

class TestComputeGoalProgress:
    """Req 8.2: pacing_pct = (actual / prorated_target) × 100."""

    def test_pacing_formula(self, comparator: KPIComparator) -> None:
        progress = comparator.compute_goal_progress(
            actual=Decimal("150"),
            target=Decimal("300"),
            days_elapsed=15,
            days_total=30,
        )
        # prorated = 300 * 15/30 = 150; pacing = (150/150)*100 = 100
        assert progress.prorated_target == Decimal("150")
        assert progress.pacing_pct == Decimal("100")
        assert progress.status == "ON_TRACK"

    def test_pacing_at_50_pct(self, comparator: KPIComparator) -> None:
        progress = comparator.compute_goal_progress(
            actual=Decimal("75"),
            target=Decimal("300"),
            days_elapsed=15,
            days_total=30,
        )
        # prorated = 150; pacing = (75/150)*100 = 50
        assert progress.pacing_pct == Decimal("50")
        assert progress.status == "AT_RISK"

    def test_pacing_at_exactly_90_is_on_track(self, comparator: KPIComparator) -> None:
        """Boundary: 90% pacing should be ON_TRACK."""
        progress = comparator.compute_goal_progress(
            actual=Decimal("135"),
            target=Decimal("300"),
            days_elapsed=15,
            days_total=30,
        )
        # prorated = 150; pacing = (135/150)*100 = 90
        assert progress.pacing_pct == Decimal("90")
        assert progress.status == "ON_TRACK"

    def test_pacing_just_below_90_is_at_risk(self, comparator: KPIComparator) -> None:
        """Boundary: < 90% pacing should be AT_RISK."""
        progress = comparator.compute_goal_progress(
            actual=Decimal("134"),
            target=Decimal("300"),
            days_elapsed=15,
            days_total=30,
        )
        # prorated = 150; pacing = (134/150)*100 ≈ 89.33
        expected_prorated = Decimal("300") * Decimal("15") / Decimal("30")
        expected_pacing = (Decimal("134") / expected_prorated) * Decimal("100")
        assert progress.pacing_pct == expected_pacing
        assert progress.pacing_pct < Decimal("90")
        assert progress.status == "AT_RISK"


# ------------------------------------------------------------------ #
# 2. compute_goal_progress — edge cases
# ------------------------------------------------------------------ #

class TestGoalProgressEdgeCases:

    def test_zero_target(self, comparator: KPIComparator) -> None:
        progress = comparator.compute_goal_progress(
            actual=Decimal("100"),
            target=Decimal("0"),
            days_elapsed=15,
            days_total=30,
        )
        assert progress.pacing_pct == Decimal("0")
        assert progress.status == "AT_RISK"

    def test_zero_days_total(self, comparator: KPIComparator) -> None:
        progress = comparator.compute_goal_progress(
            actual=Decimal("100"),
            target=Decimal("300"),
            days_elapsed=0,
            days_total=0,
        )
        assert progress.pacing_pct == Decimal("0")
        assert progress.status == "AT_RISK"

    def test_day_one(self, comparator: KPIComparator) -> None:
        """Day 1 of a 31-day month."""
        progress = comparator.compute_goal_progress(
            actual=Decimal("10"),
            target=Decimal("310"),
            days_elapsed=1,
            days_total=31,
        )
        prorated = Decimal("310") * Decimal("1") / Decimal("31")
        expected_pacing = (Decimal("10") / prorated) * Decimal("100")
        assert progress.prorated_target == prorated
        assert progress.pacing_pct == expected_pacing

    def test_last_day(self, comparator: KPIComparator) -> None:
        """Last day — prorated target equals full target."""
        progress = comparator.compute_goal_progress(
            actual=Decimal("300"),
            target=Decimal("300"),
            days_elapsed=30,
            days_total=30,
        )
        assert progress.prorated_target == Decimal("300")
        assert progress.pacing_pct == Decimal("100")
        assert progress.status == "ON_TRACK"


# ------------------------------------------------------------------ #
# 3. compare_to_targets — returns findings for all metrics
# ------------------------------------------------------------------ #

class TestCompareToTargets:
    """Req 8.1: compare MTD actuals for regs, CPA, spend."""

    def test_returns_three_findings_with_cpa(self, comparator: KPIComparator) -> None:
        targets = _make_targets()
        findings = comparator.compare_to_targets(
            market_code="AU",
            actual_spend=Decimal("15000"),
            actual_regs=150,
            actual_cpa=Decimal("100"),
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        metric_names = [f.metric_name for f in findings]
        assert "spend" in metric_names
        assert "registrations" in metric_names
        assert "cpa" in metric_names
        assert len(findings) == 3

    def test_returns_two_findings_without_cpa(self, comparator: KPIComparator) -> None:
        """When actual_cpa is None, no CPA finding is produced."""
        targets = _make_targets()
        findings = comparator.compare_to_targets(
            market_code="AU",
            actual_spend=Decimal("15000"),
            actual_regs=0,
            actual_cpa=None,
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        metric_names = [f.metric_name for f in findings]
        assert "cpa" not in metric_names
        assert len(findings) == 2

    def test_all_findings_have_goal_category(self, comparator: KPIComparator) -> None:
        targets = _make_targets()
        findings = comparator.compare_to_targets(
            market_code="AU",
            actual_spend=Decimal("15000"),
            actual_regs=150,
            actual_cpa=Decimal("100"),
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        for f in findings:
            assert f.category == "GOAL"


# ------------------------------------------------------------------ #
# 4. AT_RISK flagging (Req 8.3)
# ------------------------------------------------------------------ #

class TestAtRiskFlagging:
    """Req 8.3: flag goals pacing below 90% of prorated target."""

    def test_underpacing_spend_is_at_risk(self, comparator: KPIComparator) -> None:
        targets = _make_targets(monthly_spend=Decimal("30000"))
        findings = comparator.compare_to_targets(
            market_code="AU",
            actual_spend=Decimal("5000"),  # way below prorated
            actual_regs=150,
            actual_cpa=Decimal("33.33"),
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        spend_finding = next(f for f in findings if f.metric_name == "spend")
        # prorated = 15000; pacing = (5000/15000)*100 ≈ 33.3%
        assert spend_finding.status == "AT_RISK"

    def test_on_track_spend(self, comparator: KPIComparator) -> None:
        targets = _make_targets(monthly_spend=Decimal("30000"))
        findings = comparator.compare_to_targets(
            market_code="AU",
            actual_spend=Decimal("15000"),
            actual_regs=150,
            actual_cpa=Decimal("100"),
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        spend_finding = next(f for f in findings if f.metric_name == "spend")
        assert spend_finding.status == "ON_TRACK"

    def test_underpacing_regs_is_at_risk(self, comparator: KPIComparator) -> None:
        targets = _make_targets(monthly_regs=300)
        findings = comparator.compare_to_targets(
            market_code="AU",
            actual_spend=Decimal("15000"),
            actual_regs=50,  # way below prorated 150
            actual_cpa=Decimal("300"),
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        regs_finding = next(f for f in findings if f.metric_name == "registrations")
        assert regs_finding.status == "AT_RISK"


# ------------------------------------------------------------------ #
# 5. CPA comparison — higher is worse
# ------------------------------------------------------------------ #

class TestCPAComparison:
    """CPA: AT_RISK when actual CPA > 110% of target CPA."""

    def test_cpa_on_track_at_target(self, comparator: KPIComparator) -> None:
        targets = _make_targets(target_cpa=Decimal("100"))
        findings = comparator.compare_to_targets(
            market_code="AU",
            actual_spend=Decimal("15000"),
            actual_regs=150,
            actual_cpa=Decimal("100"),
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        cpa_finding = next(f for f in findings if f.metric_name == "cpa")
        assert cpa_finding.status == "ON_TRACK"

    def test_cpa_at_risk_when_high(self, comparator: KPIComparator) -> None:
        targets = _make_targets(target_cpa=Decimal("100"))
        findings = comparator.compare_to_targets(
            market_code="AU",
            actual_spend=Decimal("15000"),
            actual_regs=150,
            actual_cpa=Decimal("120"),  # 120% of target
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        cpa_finding = next(f for f in findings if f.metric_name == "cpa")
        assert cpa_finding.status == "AT_RISK"

    def test_cpa_on_track_at_110_boundary(self, comparator: KPIComparator) -> None:
        targets = _make_targets(target_cpa=Decimal("100"))
        findings = comparator.compare_to_targets(
            market_code="AU",
            actual_spend=Decimal("15000"),
            actual_regs=150,
            actual_cpa=Decimal("110"),  # exactly 110%
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        cpa_finding = next(f for f in findings if f.metric_name == "cpa")
        assert cpa_finding.status == "ON_TRACK"

    def test_zero_target_cpa_skips_finding(self, comparator: KPIComparator) -> None:
        targets = _make_targets(target_cpa=Decimal("0"))
        findings = comparator.compare_to_targets(
            market_code="AU",
            actual_spend=Decimal("15000"),
            actual_regs=150,
            actual_cpa=Decimal("100"),
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        metric_names = [f.metric_name for f in findings]
        assert "cpa" not in metric_names


# ------------------------------------------------------------------ #
# 6. Kingpin Goal — MX registrations (Req 8.4)
# ------------------------------------------------------------------ #

class TestKingpinGoal:
    """Req 8.4: MX registrations is a Kingpin Goal."""

    def test_mx_regs_is_kingpin(self, comparator: KPIComparator) -> None:
        targets = _make_targets()
        findings = comparator.compare_to_targets(
            market_code="MX",
            actual_spend=Decimal("15000"),
            actual_regs=150,
            actual_cpa=Decimal("100"),
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        regs_finding = next(f for f in findings if f.metric_name == "registrations")
        assert regs_finding.is_kingpin_goal is True

    def test_mx_spend_is_not_kingpin(self, comparator: KPIComparator) -> None:
        targets = _make_targets()
        findings = comparator.compare_to_targets(
            market_code="MX",
            actual_spend=Decimal("15000"),
            actual_regs=150,
            actual_cpa=Decimal("100"),
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        spend_finding = next(f for f in findings if f.metric_name == "spend")
        assert spend_finding.is_kingpin_goal is False

    def test_au_regs_is_not_kingpin(self, comparator: KPIComparator) -> None:
        targets = _make_targets()
        findings = comparator.compare_to_targets(
            market_code="AU",
            actual_spend=Decimal("15000"),
            actual_regs=150,
            actual_cpa=Decimal("100"),
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        regs_finding = next(f for f in findings if f.metric_name == "registrations")
        assert regs_finding.is_kingpin_goal is False

    def test_kingpin_at_risk_is_critical(self, comparator: KPIComparator) -> None:
        """AT_RISK Kingpin Goal should be CRITICAL severity."""
        targets = _make_targets(monthly_regs=300)
        findings = comparator.compare_to_targets(
            market_code="MX",
            actual_spend=Decimal("15000"),
            actual_regs=50,  # way below prorated
            actual_cpa=Decimal("300"),
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        regs_finding = next(f for f in findings if f.metric_name == "registrations")
        assert regs_finding.is_kingpin_goal is True
        assert regs_finding.status == "AT_RISK"
        assert regs_finding.severity == "CRITICAL"

    def test_non_kingpin_at_risk_is_warning(self, comparator: KPIComparator) -> None:
        """AT_RISK non-Kingpin Goal should be WARNING severity."""
        targets = _make_targets(monthly_regs=300)
        findings = comparator.compare_to_targets(
            market_code="AU",
            actual_spend=Decimal("15000"),
            actual_regs=50,
            actual_cpa=Decimal("300"),
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        regs_finding = next(f for f in findings if f.metric_name == "registrations")
        assert regs_finding.is_kingpin_goal is False
        assert regs_finding.status == "AT_RISK"
        assert regs_finding.severity == "WARNING"

    def test_kingpin_on_track_is_info(self, comparator: KPIComparator) -> None:
        """ON_TRACK Kingpin Goal should be INFO severity."""
        targets = _make_targets(monthly_regs=300)
        findings = comparator.compare_to_targets(
            market_code="MX",
            actual_spend=Decimal("15000"),
            actual_regs=150,
            actual_cpa=Decimal("100"),
            targets=targets,
            days_elapsed=15,
            days_total=30,
        )
        regs_finding = next(f for f in findings if f.metric_name == "registrations")
        assert regs_finding.is_kingpin_goal is True
        assert regs_finding.status == "ON_TRACK"
        assert regs_finding.severity == "INFO"
