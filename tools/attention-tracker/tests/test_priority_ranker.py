"""Unit tests for priority ranking and week-over-week comparison.

Validates: Requirements 9.1, 9.2, 9.3, 12.4, 13.1, 13.2, 13.3
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from typing import Optional

import pytest

from paid_search_audit.models import NormalizedMetrics, WoWComparison
from paid_search_audit.priority_ranker import (
    CATEGORY_WEIGHTS,
    HANDS_ON_MARKETS,
    MARKET_WEIGHTS_HANDS_ON,
    MARKET_WEIGHTS_TEAM_WIDE,
    SEVERITY_WEIGHTS,
    WORSENING_TREND_BONUS,
    PrioritizedFinding,
    compute_wow,
    pct_change,
    rank_findings,
)


# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #

@dataclass
class FakeFinding:
    """Minimal finding-like object for testing the ranker."""
    severity: str = "INFO"
    market: str = "AU"
    category: str = "PERFORMANCE"
    trend: Optional[str] = None


def _make_metric(
    metric_date: date,
    market: str = "AU",
    spend: Decimal = Decimal("100"),
    clicks: int = 50,
    impressions: int = 1000,
    conversions: int = 5,
    campaign_name: str = "test",
) -> NormalizedMetrics:
    return NormalizedMetrics(
        date=metric_date,
        market=market,
        campaign_type="Brand",
        campaign_name=campaign_name,
        account_id="111",
        mcc_id="222",
        impressions=impressions,
        clicks=clicks,
        spend=spend,
        spend_usd=spend,
        conversions=conversions,
    )


# ================================================================== #
# rank_findings tests
# ================================================================== #

class TestRankFindingsScoring:
    """Req 9.1: scoring = severity + market + category + trend bonus."""

    def test_critical_au_budget_worsening_max_score(self) -> None:
        f = FakeFinding(severity="CRITICAL", market="AU", category="BUDGET", trend="WORSENING")
        result = rank_findings([f])
        expected = 100 + 20 + 30 + 15  # 165
        assert result[0].score == expected

    def test_info_team_wide_performance_no_trend(self) -> None:
        f = FakeFinding(severity="INFO", market="US", category="PERFORMANCE", trend=None)
        result = rank_findings([f])
        expected = 10 + 5 + 15  # 30
        assert result[0].score == expected

    def test_warning_mx_goal(self) -> None:
        f = FakeFinding(severity="WARNING", market="MX", category="GOAL")
        result = rank_findings([f])
        expected = 50 + 20 + 25  # 95
        assert result[0].score == expected

    def test_severity_weights_match_spec(self) -> None:
        assert SEVERITY_WEIGHTS["CRITICAL"] == 100
        assert SEVERITY_WEIGHTS["WARNING"] == 50
        assert SEVERITY_WEIGHTS["INFO"] == 10

    def test_market_weights_match_spec(self) -> None:
        assert MARKET_WEIGHTS_HANDS_ON == 20
        assert MARKET_WEIGHTS_TEAM_WIDE == 5
        assert HANDS_ON_MARKETS == {"AU", "MX"}

    def test_category_weights_match_spec(self) -> None:
        assert CATEGORY_WEIGHTS["BUDGET"] == 30
        assert CATEGORY_WEIGHTS["GOAL"] == 25
        assert CATEGORY_WEIGHTS["PERFORMANCE"] == 15

    def test_worsening_trend_bonus(self) -> None:
        assert WORSENING_TREND_BONUS == 15

    def test_unknown_category_gets_zero_weight(self) -> None:
        f = FakeFinding(severity="INFO", market="US", category="UNKNOWN")
        result = rank_findings([f])
        expected = 10 + 5 + 0  # 15
        assert result[0].score == expected


class TestRankFindingsSorting:
    """Req 9.2: sort descending by score."""

    def test_descending_sort_order(self) -> None:
        high = FakeFinding(severity="CRITICAL", market="AU", category="BUDGET")
        mid = FakeFinding(severity="WARNING", market="MX", category="GOAL")
        low = FakeFinding(severity="INFO", market="US", category="PERFORMANCE")

        result = rank_findings([low, high, mid])

        assert result[0].score >= result[1].score >= result[2].score

    def test_equal_scores_preserve_insertion_order(self) -> None:
        f1 = FakeFinding(severity="WARNING", market="AU", category="PERFORMANCE")
        f2 = FakeFinding(severity="WARNING", market="MX", category="PERFORMANCE")

        result = rank_findings([f1, f2])

        # Same score — stable sort preserves order
        assert result[0].finding is f1
        assert result[1].finding is f2


class TestRankFindingsRanking:
    """Req 9.3: sequential ranks starting from 1."""

    def test_sequential_ranks(self) -> None:
        findings = [
            FakeFinding(severity="CRITICAL", market="AU"),
            FakeFinding(severity="WARNING", market="MX"),
            FakeFinding(severity="INFO", market="US"),
        ]
        result = rank_findings(findings)

        for i, pf in enumerate(result):
            assert pf.priority == i + 1

    def test_single_finding_gets_rank_1(self) -> None:
        result = rank_findings([FakeFinding()])
        assert result[0].priority == 1

    def test_empty_list_returns_empty(self) -> None:
        result = rank_findings([])
        assert result == []


# ================================================================== #
# pct_change tests  (Req 12.4)
# ================================================================== #

class TestPctChange:
    """Req 12.4: handle zero/None prior period values."""

    def test_normal_increase(self) -> None:
        result = pct_change(Decimal("120"), Decimal("100"))
        assert result == Decimal("20")

    def test_normal_decrease(self) -> None:
        result = pct_change(Decimal("80"), Decimal("100"))
        assert result == Decimal("-20")

    def test_no_change(self) -> None:
        result = pct_change(Decimal("100"), Decimal("100"))
        assert result == Decimal("0")

    def test_prior_zero_returns_none(self) -> None:
        assert pct_change(Decimal("100"), Decimal("0")) is None

    def test_prior_none_returns_none(self) -> None:
        assert pct_change(Decimal("100"), None) is None

    def test_current_none_returns_none(self) -> None:
        assert pct_change(None, Decimal("100")) is None

    def test_both_none_returns_none(self) -> None:
        assert pct_change(None, None) is None

    def test_integer_inputs(self) -> None:
        result = pct_change(150, 100)
        assert result == Decimal("50")

    def test_prior_zero_int_returns_none(self) -> None:
        assert pct_change(50, 0) is None


# ================================================================== #
# compute_wow tests  (Req 13.1, 13.2, 13.3)
# ================================================================== #

class TestComputeWoW:
    """Req 13.1, 13.2: compare audit date vs same day prior week."""

    def test_basic_wow_comparison(self) -> None:
        audit_date = date(2026, 3, 15)  # Sunday
        prior_date = audit_date - timedelta(days=7)

        current = [_make_metric(audit_date, spend=Decimal("200"), clicks=100, conversions=10)]
        historical = [_make_metric(prior_date, spend=Decimal("100"), clicks=50, conversions=5)]

        result = compute_wow(current, historical)

        assert result.spend_change_pct == Decimal("100")   # 200 vs 100 = +100%
        assert result.clicks_change_pct == Decimal("100")   # 100 vs 50 = +100%
        assert result.conversions_change_pct == Decimal("100")  # 10 vs 5 = +100%
        assert result.current is not None
        assert result.prior_week is not None

    def test_wow_with_multiple_campaigns(self) -> None:
        audit_date = date(2026, 3, 15)
        prior_date = audit_date - timedelta(days=7)

        current = [
            _make_metric(audit_date, spend=Decimal("100"), clicks=40, conversions=4, campaign_name="brand"),
            _make_metric(audit_date, spend=Decimal("150"), clicks=60, conversions=6, campaign_name="nb"),
        ]
        historical = [
            _make_metric(prior_date, spend=Decimal("200"), clicks=80, conversions=8),
        ]

        result = compute_wow(current, historical)

        # Current: spend=250, clicks=100, conversions=10
        # Prior: spend=200, clicks=80, conversions=8
        assert result.spend_change_pct == pct_change(Decimal("250"), Decimal("200"))
        assert result.clicks_change_pct == pct_change(100, 80)
        assert result.conversions_change_pct == pct_change(10, 8)

    def test_wow_cpa_comparison(self) -> None:
        audit_date = date(2026, 3, 15)
        prior_date = audit_date - timedelta(days=7)

        current = [_make_metric(audit_date, spend=Decimal("300"), conversions=10)]
        historical = [_make_metric(prior_date, spend=Decimal("200"), conversions=10)]

        result = compute_wow(current, historical)

        # CPA: current=30, prior=20 → +50%
        assert result.cpa_change_pct == pct_change(Decimal("30"), Decimal("20"))

    def test_wow_ctr_comparison(self) -> None:
        audit_date = date(2026, 3, 15)
        prior_date = audit_date - timedelta(days=7)

        current = [_make_metric(audit_date, clicks=100, impressions=1000)]
        historical = [_make_metric(prior_date, clicks=50, impressions=1000)]

        result = compute_wow(current, historical)

        # CTR: current=0.1, prior=0.05 → +100%
        current_ctr = Decimal("100") / Decimal("1000")
        prior_ctr = Decimal("50") / Decimal("1000")
        assert result.ctr_change_pct == pct_change(current_ctr, prior_ctr)


class TestComputeWoWMissingData:
    """Req 13.3: return None for all WoW changes when prior week data is missing."""

    def test_no_prior_week_data(self) -> None:
        audit_date = date(2026, 3, 15)
        current = [_make_metric(audit_date)]
        # Historical has data but NOT for the prior week date
        other_date = audit_date - timedelta(days=14)
        historical = [_make_metric(other_date)]

        result = compute_wow(current, historical)

        assert result.spend_change_pct is None
        assert result.clicks_change_pct is None
        assert result.conversions_change_pct is None
        assert result.cpa_change_pct is None
        assert result.ctr_change_pct is None
        assert result.prior_week is None

    def test_empty_historical(self) -> None:
        audit_date = date(2026, 3, 15)
        current = [_make_metric(audit_date)]

        result = compute_wow(current, [])

        assert result.spend_change_pct is None
        assert result.clicks_change_pct is None
        assert result.conversions_change_pct is None
        assert result.cpa_change_pct is None
        assert result.ctr_change_pct is None

    def test_empty_current_returns_empty_comparison(self) -> None:
        result = compute_wow([], [])
        assert result == WoWComparison()


class TestComputeWoWZeroPrior:
    """Req 12.4: zero/None prior period values → None for percentage change."""

    def test_zero_prior_spend(self) -> None:
        audit_date = date(2026, 3, 15)
        prior_date = audit_date - timedelta(days=7)

        current = [_make_metric(audit_date, spend=Decimal("100"))]
        historical = [_make_metric(prior_date, spend=Decimal("0"))]

        result = compute_wow(current, historical)
        assert result.spend_change_pct is None

    def test_zero_prior_clicks(self) -> None:
        audit_date = date(2026, 3, 15)
        prior_date = audit_date - timedelta(days=7)

        current = [_make_metric(audit_date, clicks=50)]
        historical = [_make_metric(prior_date, clicks=0)]

        result = compute_wow(current, historical)
        assert result.clicks_change_pct is None

    def test_zero_prior_conversions_cpa_is_none(self) -> None:
        """When prior conversions=0, prior CPA=None → CPA change is None."""
        audit_date = date(2026, 3, 15)
        prior_date = audit_date - timedelta(days=7)

        current = [_make_metric(audit_date, spend=Decimal("100"), conversions=5)]
        historical = [_make_metric(prior_date, spend=Decimal("100"), conversions=0)]

        result = compute_wow(current, historical)
        assert result.cpa_change_pct is None

    def test_zero_prior_impressions_ctr_is_none(self) -> None:
        """When prior impressions=0, prior CTR=None → CTR change is None."""
        audit_date = date(2026, 3, 15)
        prior_date = audit_date - timedelta(days=7)

        current = [_make_metric(audit_date, clicks=50, impressions=1000)]
        historical = [_make_metric(prior_date, clicks=50, impressions=0)]

        result = compute_wow(current, historical)
        assert result.ctr_change_pct is None
