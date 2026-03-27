"""Property-based tests for data store temporal correctness.

**Validates: Requirements 14.2, 14.3**

Property 8: Temporal Correctness — load_historical never returns data points
with date >= audit_date (before_date). All returned NormalizedMetrics must
have date strictly less than the before_date parameter.
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from hypothesis import given, settings
from hypothesis import strategies as st

from paid_search_audit.data_store import DataStore
from paid_search_audit.models import NormalizedMetrics

# --- Strategies ---

# Dates within a reasonable range for testing
_MIN_DATE = date(2024, 1, 1)
_MAX_DATE = date(2026, 12, 31)

reasonable_dates = st.dates(min_value=_MIN_DATE, max_value=_MAX_DATE)

market_strategy = st.sampled_from(["AU", "MX", "US", "JP", "CA"])

campaign_type_strategy = st.sampled_from(["Brand", "Non-Brand", "Competitor"])

non_negative_int = st.integers(min_value=0, max_value=100_000)

positive_int = st.integers(min_value=1, max_value=100_000)

decimal_spend = st.decimals(
    min_value=Decimal("0"),
    max_value=Decimal("100000"),
    allow_nan=False,
    allow_infinity=False,
    places=2,
)


def build_metric(metric_date: date, market: str) -> NormalizedMetrics:
    """Build a minimal NormalizedMetrics for a given date and market."""
    return NormalizedMetrics(
        date=metric_date,
        market=market,
        campaign_type="Brand",
        campaign_name="test-campaign",
        account_id="1234567890",
        mcc_id="0987654321",
        impressions=100,
        clicks=10,
        spend=Decimal("50.00"),
        spend_usd=Decimal("50.00"),
        conversions=5,
        source="GOOGLE_ADS",
    )


# Strategy: a list of dates spread around a before_date
@st.composite
def dates_around_before_date(draw):
    """Generate a before_date and a list of metric dates spread around it.

    Returns (before_date, metric_dates) where metric_dates may include
    dates before, on, and after before_date.
    """
    before_date = draw(st.dates(min_value=date(2025, 1, 15), max_value=date(2026, 6, 15)))
    # Generate offsets from -60 to +30 days relative to before_date
    offsets = draw(
        st.lists(
            st.integers(min_value=-60, max_value=30),
            min_size=1,
            max_size=20,
        )
    )
    metric_dates = [before_date + timedelta(days=d) for d in offsets]
    return before_date, metric_dates


class TestTemporalCorrectness:
    """Property 8: Temporal Correctness.

    **Validates: Requirements 14.2, 14.3**

    load_historical(market, days, before_date) must never return data points
    with date >= before_date.
    """

    @given(data=dates_around_before_date(), market=market_strategy)
    @settings(max_examples=200, deadline=None)
    def test_load_historical_returns_only_dates_before_before_date(
        self, data: tuple[date, list[date]], market: str
    ) -> None:
        """Every returned metric must have date < before_date."""
        before_date, metric_dates = data
        store = DataStore(":memory:")
        try:
            metrics = [build_metric(d, market) for d in metric_dates]
            store.store_metrics(metrics, before_date)

            result = store.load_historical(market, days=90, before_date=before_date)

            for m in result:
                assert m.date < before_date, (
                    f"load_historical returned date {m.date} which is not "
                    f"strictly before before_date {before_date}"
                )
        finally:
            store.close()

    @given(market=market_strategy, before_date=st.dates(min_value=date(2025, 3, 1), max_value=date(2026, 6, 1)))
    @settings(max_examples=200, deadline=None)
    def test_data_on_before_date_is_excluded(
        self, market: str, before_date: date
    ) -> None:
        """Data stored ON the before_date must not appear in results."""
        store = DataStore(":memory:")
        try:
            on_date_metric = build_metric(before_date, market)
            before_metric = build_metric(before_date - timedelta(days=1), market)
            # Use different campaign names so both can be stored
            on_date_metric.campaign_name = "on-date-campaign"
            before_metric.campaign_name = "before-date-campaign"

            store.store_metrics([on_date_metric, before_metric], before_date)

            result = store.load_historical(market, days=90, before_date=before_date)

            returned_dates = {m.date for m in result}
            assert before_date not in returned_dates, (
                f"load_historical returned data ON before_date {before_date}"
            )
        finally:
            store.close()

    @given(
        market=market_strategy,
        before_date=st.dates(min_value=date(2025, 3, 1), max_value=date(2026, 6, 1)),
        days_after=st.integers(min_value=1, max_value=30),
    )
    @settings(max_examples=200, deadline=None)
    def test_data_after_before_date_is_excluded(
        self, market: str, before_date: date, days_after: int
    ) -> None:
        """Data stored AFTER the before_date must not appear in results."""
        store = DataStore(":memory:")
        try:
            after_date = before_date + timedelta(days=days_after)
            after_metric = build_metric(after_date, market)
            before_metric = build_metric(before_date - timedelta(days=1), market)
            after_metric.campaign_name = "after-date-campaign"
            before_metric.campaign_name = "before-date-campaign"

            store.store_metrics([after_metric, before_metric], before_date)

            result = store.load_historical(market, days=90, before_date=before_date)

            for m in result:
                assert m.date < before_date, (
                    f"load_historical returned date {m.date} which is on or "
                    f"after before_date {before_date}"
                )
        finally:
            store.close()
