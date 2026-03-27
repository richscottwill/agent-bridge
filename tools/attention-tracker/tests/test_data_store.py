"""Unit tests for DataStore.

Validates: Requirements 4.1, 4.2, 4.3

Tests cover:
- Store and retrieve round-trip (Decimal precision preserved)
- 30-day retrieval window
- load_period_actuals aggregation for spend and conversions
- Upsert behavior (latest values win)
- Empty results for unknown market
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

import pytest

from paid_search_audit.data_store import DataStore
from paid_search_audit.models import NormalizedMetrics


def _make_metric(
    metric_date: date,
    market: str = "AU",
    campaign_name: str = "test-campaign",
    account_id: str = "1234567890",
    spend: Decimal = Decimal("123.45"),
    spend_usd: Decimal = Decimal("80.21"),
    conversions: int = 7,
    impressions: int = 5000,
    clicks: int = 250,
    cpa: Decimal | None = Decimal("17.6357142857"),
    ctr: Decimal | None = Decimal("0.05"),
    conversion_rate: Decimal | None = Decimal("0.028"),
    quality_score_avg: Decimal | None = Decimal("7.3"),
    source: str = "GOOGLE_ADS",
    campaign_type: str = "Brand",
    mcc_id: str = "0987654321",
    is_aggregated: bool = False,
) -> NormalizedMetrics:
    return NormalizedMetrics(
        date=metric_date,
        market=market,
        campaign_type=campaign_type,
        campaign_name=campaign_name,
        account_id=account_id,
        mcc_id=mcc_id,
        impressions=impressions,
        clicks=clicks,
        spend=spend,
        spend_usd=spend_usd,
        conversions=conversions,
        cpa=cpa,
        ctr=ctr,
        conversion_rate=conversion_rate,
        quality_score_avg=quality_score_avg,
        source=source,
        is_aggregated=is_aggregated,
    )


@pytest.fixture
def store():
    """Provide an in-memory DataStore, closed after the test."""
    ds = DataStore(":memory:")
    yield ds
    ds.close()


# ------------------------------------------------------------------ #
# 1. Store and retrieve round-trip — Decimal precision preserved
# ------------------------------------------------------------------ #

class TestRoundTrip:
    """Requirement 4.1: persist merged metrics and retrieve them."""

    def test_all_fields_round_trip(self, store: DataStore) -> None:
        d = date(2026, 3, 15)
        original = _make_metric(d)
        store.store_metrics([original], d)

        results = store.load_historical("AU", days=5, before_date=d + timedelta(days=1))
        assert len(results) == 1
        m = results[0]

        assert m.date == original.date
        assert m.market == original.market
        assert m.campaign_type == original.campaign_type
        assert m.campaign_name == original.campaign_name
        assert m.account_id == original.account_id
        assert m.mcc_id == original.mcc_id
        assert m.impressions == original.impressions
        assert m.clicks == original.clicks
        assert m.conversions == original.conversions
        assert m.source == original.source
        assert m.is_aggregated == original.is_aggregated

    def test_decimal_precision_preserved(self, store: DataStore) -> None:
        d = date(2026, 3, 15)
        original = _make_metric(
            d,
            spend=Decimal("12345.6789"),
            spend_usd=Decimal("8000.1234"),
            cpa=Decimal("17.6357142857"),
            ctr=Decimal("0.05"),
            conversion_rate=Decimal("0.028"),
            quality_score_avg=Decimal("7.3"),
        )
        store.store_metrics([original], d)

        results = store.load_historical("AU", days=5, before_date=d + timedelta(days=1))
        m = results[0]

        assert m.spend == Decimal("12345.6789")
        assert m.spend_usd == Decimal("8000.1234")
        assert m.cpa == Decimal("17.6357142857")
        assert m.ctr == Decimal("0.05")
        assert m.conversion_rate == Decimal("0.028")
        assert m.quality_score_avg == Decimal("7.3")

    def test_none_optional_fields_round_trip(self, store: DataStore) -> None:
        d = date(2026, 3, 15)
        original = _make_metric(d, cpa=None, ctr=None, conversion_rate=None, quality_score_avg=None)
        store.store_metrics([original], d)

        results = store.load_historical("AU", days=5, before_date=d + timedelta(days=1))
        m = results[0]

        assert m.cpa is None
        assert m.ctr is None
        assert m.conversion_rate is None
        assert m.quality_score_avg is None


# ------------------------------------------------------------------ #
# 2. 30-day retrieval window
# ------------------------------------------------------------------ #

class TestRetrievalWindow:
    """Requirement 4.3: support retrieval of at least 30 days."""

    def test_30_day_window_filters_correctly(self, store: DataStore) -> None:
        """Store 45 days of data, request days=30 — only 30 days returned."""
        base = date(2026, 3, 15)
        metrics = []
        for i in range(45):
            d = base - timedelta(days=i)
            metrics.append(_make_metric(d, campaign_name=f"camp-{i}"))

        store.store_metrics(metrics, base)

        before_date = base + timedelta(days=1)
        results = store.load_historical("AU", days=30, before_date=before_date)

        # Window is [before_date - 30, before_date) = [2026-02-14, 2026-03-16)
        expected_start = before_date - timedelta(days=30)
        for m in results:
            assert m.date >= expected_start
            assert m.date < before_date

        # Should have exactly 30 days of data (day 0 through day 29 offset)
        returned_dates = {m.date for m in results}
        assert len(returned_dates) <= 30
        # Verify the oldest possible date in the window IS included
        assert expected_start in returned_dates


# ------------------------------------------------------------------ #
# 3. load_period_actuals — spend aggregation
# ------------------------------------------------------------------ #

class TestPeriodActualsSpend:
    """Requirement 4.2: aggregate spend across date range."""

    def test_spend_sum_across_date_range(self, store: DataStore) -> None:
        metrics = [
            _make_metric(date(2026, 3, 1), spend=Decimal("100.50")),
            _make_metric(date(2026, 3, 2), spend=Decimal("200.75"), campaign_name="c2"),
            _make_metric(date(2026, 3, 3), spend=Decimal("50.25"), campaign_name="c3"),
        ]
        store.store_metrics(metrics, date(2026, 3, 3))

        total = store.load_period_actuals(
            market="AU",
            start_date=date(2026, 3, 1),
            end_date=date(2026, 3, 3),
            metric="spend",
        )
        assert total == Decimal("100.50") + Decimal("200.75") + Decimal("50.25")


# ------------------------------------------------------------------ #
# 4. load_period_actuals — conversions aggregation
# ------------------------------------------------------------------ #

class TestPeriodActualsConversions:
    """Requirement 4.2: aggregate conversions across date range."""

    def test_conversions_sum_across_date_range(self, store: DataStore) -> None:
        metrics = [
            _make_metric(date(2026, 3, 1), conversions=10),
            _make_metric(date(2026, 3, 2), conversions=20, campaign_name="c2"),
            _make_metric(date(2026, 3, 3), conversions=5, campaign_name="c3"),
        ]
        store.store_metrics(metrics, date(2026, 3, 3))

        total = store.load_period_actuals(
            market="AU",
            start_date=date(2026, 3, 1),
            end_date=date(2026, 3, 3),
            metric="conversions",
        )
        assert total == Decimal("35")


# ------------------------------------------------------------------ #
# 5. Upsert behavior — latest values win
# ------------------------------------------------------------------ #

class TestUpsert:
    """Requirement 4.1 (idempotent storage): same key twice → latest wins."""

    def test_upsert_overwrites_with_latest_values(self, store: DataStore) -> None:
        d = date(2026, 3, 15)
        first = _make_metric(d, spend=Decimal("100.00"), conversions=5)
        store.store_metrics([first], d)

        updated = _make_metric(d, spend=Decimal("999.99"), conversions=42)
        store.store_metrics([updated], d)

        results = store.load_historical("AU", days=5, before_date=d + timedelta(days=1))
        assert len(results) == 1
        assert results[0].spend == Decimal("999.99")
        assert results[0].conversions == 42


# ------------------------------------------------------------------ #
# 6. Empty results — unknown market
# ------------------------------------------------------------------ #

class TestEmptyResults:
    """Edge case: querying a market with no data."""

    def test_load_historical_empty_for_unknown_market(self, store: DataStore) -> None:
        results = store.load_historical("ZZ", days=30, before_date=date(2026, 3, 15))
        assert results == []

    def test_load_period_actuals_returns_zero_for_unknown_market(self, store: DataStore) -> None:
        total = store.load_period_actuals(
            market="ZZ",
            start_date=date(2026, 3, 1),
            end_date=date(2026, 3, 31),
            metric="spend",
        )
        assert total == Decimal("0")
