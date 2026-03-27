"""Property-based tests for the Data Normalizer.

**Validates: Requirements 3.2, 3.3, 12.1, 12.2, 12.3**

Property 12: No Cross-MCC Double Counting — each campaign attributed to
exactly one (account_id, mcc_id) pair in aggregated output.
∀ campaign_name ∈ aggregated: count(campaign_name) == 1
∧ total_spend(aggregated) == total_spend(input)

Property 5: No Division by Zero — ratio metrics return None when
denominators are zero, through the full normalize and aggregate pipeline.
conversions == 0 ⟹ CPA is None
impressions == 0 ⟹ CTR is None
clicks == 0 ⟹ conversion_rate is None
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from hypothesis import given, settings
from hypothesis import strategies as st

from paid_search_audit.data_normalizer import DataNormalizer
from paid_search_audit.google_ads_fetcher import (
    AccountResult,
    CampaignData,
    MarketGoogleData,
)
from paid_search_audit.models import NormalizedMetrics


# ------------------------------------------------------------------ #
# Hypothesis strategies
# ------------------------------------------------------------------ #

non_neg_int = st.integers(min_value=0, max_value=100_000)
pos_spend = st.decimals(
    min_value=Decimal("0"), max_value=Decimal("100000"),
    allow_nan=False, allow_infinity=False, places=2,
)
campaign_names = st.sampled_from(["Brand-AU", "NonBrand-AU", "Competitor-AU", "Brand-MX"])
campaign_types = st.sampled_from(["Brand", "Non-Brand", "Competitor"])


@st.composite
def normalized_metrics_list(draw):
    """Generate a list of NormalizedMetrics with various account/mcc combos.

    Same campaign_name may appear under different (account_id, mcc_id) pairs
    to exercise the aggregation dedup logic.
    """
    num_mccs = draw(st.integers(min_value=1, max_value=3))
    mcc_ids = [f"MCC-{i}" for i in range(num_mccs)]

    metrics: list[NormalizedMetrics] = []
    for mcc_id in mcc_ids:
        num_accounts = draw(st.integers(min_value=1, max_value=2))
        for acct_idx in range(num_accounts):
            account_id = f"{mcc_id}-A{acct_idx}"
            num_campaigns = draw(st.integers(min_value=1, max_value=3))
            for _ in range(num_campaigns):
                cname = draw(campaign_names)
                ctype = draw(campaign_types)
                spend = draw(pos_spend)
                clicks = draw(non_neg_int)
                impressions = draw(non_neg_int)
                conversions = draw(non_neg_int)

                nm = NormalizedMetrics(
                    date=date(2026, 3, 15),
                    market="AU",
                    campaign_type=ctype,
                    campaign_name=cname,
                    account_id=account_id,
                    mcc_id=mcc_id,
                    impressions=impressions,
                    clicks=clicks,
                    spend=spend,
                    spend_usd=spend,
                    conversions=conversions,
                    cpa=NormalizedMetrics.safe_cpa(spend, conversions),
                    ctr=NormalizedMetrics.safe_ctr(clicks, impressions),
                    conversion_rate=NormalizedMetrics.safe_conversion_rate(
                        conversions, clicks,
                    ),
                    source="GOOGLE_ADS",
                    is_aggregated=False,
                )
                metrics.append(nm)

    return metrics



@st.composite
def market_google_data_with_zero_denominators(draw):
    """Generate MarketGoogleData where some campaigns have zero denominators.

    Ensures we exercise the normalize path with zero conversions,
    impressions, and clicks.
    """
    num_accounts = draw(st.integers(min_value=1, max_value=3))
    account_results: list[AccountResult] = []

    for acct_idx in range(num_accounts):
        account_id = f"A{acct_idx}"
        mcc_id = f"MCC-{acct_idx % 2}"
        num_campaigns = draw(st.integers(min_value=1, max_value=3))
        campaigns: list[CampaignData] = []

        for camp_idx in range(num_campaigns):
            # Draw values, but force at least some zeros
            zero_choice = draw(st.sampled_from([
                "zero_conversions", "zero_impressions", "zero_clicks", "all_zero", "none_zero",
            ]))

            spend = draw(pos_spend)
            if zero_choice == "zero_conversions":
                impressions = draw(st.integers(min_value=1, max_value=10000))
                clicks = draw(st.integers(min_value=1, max_value=impressions))
                conversions = 0
            elif zero_choice == "zero_impressions":
                impressions = 0
                clicks = 0  # can't have clicks without impressions
                conversions = 0
            elif zero_choice == "zero_clicks":
                impressions = draw(st.integers(min_value=1, max_value=10000))
                clicks = 0
                conversions = 0
            elif zero_choice == "all_zero":
                impressions = 0
                clicks = 0
                conversions = 0
            else:  # none_zero
                impressions = draw(st.integers(min_value=1, max_value=10000))
                clicks = draw(st.integers(min_value=1, max_value=impressions))
                conversions = draw(st.integers(min_value=1, max_value=clicks))

            campaigns.append(CampaignData(
                campaign_id=f"C{acct_idx}-{camp_idx}",
                campaign_name=draw(campaign_names),
                campaign_type=draw(campaign_types),
                spend=spend,
                impressions=impressions,
                clicks=clicks,
                conversions=conversions,
            ))

        account_results.append(AccountResult(
            account_id=account_id,
            mcc_id=mcc_id,
            campaigns=campaigns,
        ))

    return MarketGoogleData(
        market="AU",
        account_results=account_results,
        failed_accounts=[],
    )


# ------------------------------------------------------------------ #
# Property 12: No Cross-MCC Double Counting
# ------------------------------------------------------------------ #

class TestNoCrossMCCDoubleCounting:
    """Property 12: No Cross-MCC Double Counting.

    **Validates: Requirements 3.2, 3.3**

    After aggregate_across_accounts, each unique (date, market,
    campaign_type, campaign_name) tuple appears exactly once.
    Total spend in aggregated output equals sum of input spend.
    """

    @given(metrics=normalized_metrics_list())
    @settings(max_examples=100, deadline=None)
    def test_each_campaign_appears_once_after_aggregation(
        self, metrics: list[NormalizedMetrics],
    ) -> None:
        """Each (date, market, campaign_type, campaign_name) key appears
        exactly once in aggregated output."""
        normalizer = DataNormalizer(audit_date=date(2026, 3, 15))
        aggregated = normalizer.aggregate_across_accounts(metrics)

        seen_keys: set[tuple] = set()
        for m in aggregated:
            key = (m.date, m.market, m.campaign_type, m.campaign_name)
            assert key not in seen_keys, (
                f"Duplicate key {key} in aggregated output — "
                f"double-counting detected"
            )
            seen_keys.add(key)

    @given(metrics=normalized_metrics_list())
    @settings(max_examples=100, deadline=None)
    def test_total_spend_preserved_after_aggregation(
        self, metrics: list[NormalizedMetrics],
    ) -> None:
        """Total spend in aggregated output equals sum of input spend
        (no data lost or duplicated)."""
        normalizer = DataNormalizer(audit_date=date(2026, 3, 15))
        aggregated = normalizer.aggregate_across_accounts(metrics)

        input_spend = sum((m.spend for m in metrics), Decimal("0"))
        output_spend = sum((m.spend for m in aggregated), Decimal("0"))

        assert input_spend == output_spend, (
            f"Spend mismatch: input={input_spend}, output={output_spend}. "
            f"Data was lost or duplicated during aggregation."
        )

    @given(metrics=normalized_metrics_list())
    @settings(max_examples=100, deadline=None)
    def test_total_clicks_preserved_after_aggregation(
        self, metrics: list[NormalizedMetrics],
    ) -> None:
        """Total clicks preserved through aggregation."""
        normalizer = DataNormalizer(audit_date=date(2026, 3, 15))
        aggregated = normalizer.aggregate_across_accounts(metrics)

        input_clicks = sum(m.clicks for m in metrics)
        output_clicks = sum(m.clicks for m in aggregated)

        assert input_clicks == output_clicks, (
            f"Clicks mismatch: input={input_clicks}, output={output_clicks}"
        )

    @given(metrics=normalized_metrics_list())
    @settings(max_examples=100, deadline=None)
    def test_total_conversions_preserved_after_aggregation(
        self, metrics: list[NormalizedMetrics],
    ) -> None:
        """Total conversions preserved through aggregation."""
        normalizer = DataNormalizer(audit_date=date(2026, 3, 15))
        aggregated = normalizer.aggregate_across_accounts(metrics)

        input_conv = sum(m.conversions for m in metrics)
        output_conv = sum(m.conversions for m in aggregated)

        assert input_conv == output_conv, (
            f"Conversions mismatch: input={input_conv}, output={output_conv}"
        )


# ------------------------------------------------------------------ #
# Property 5: No Division by Zero (through normalizer pipeline)
# ------------------------------------------------------------------ #

class TestNoDivisionByZeroNormalizer:
    """Property 5: No Division by Zero — through the normalizer pipeline.

    **Validates: Requirements 12.1, 12.2, 12.3**

    When campaigns have zero conversions/impressions/clicks, the
    normalize and aggregate pipeline must produce None for the
    corresponding ratio metrics, never raise an exception.
    """

    @given(raw=market_google_data_with_zero_denominators())
    @settings(max_examples=100, deadline=None)
    def test_normalize_zero_conversions_yields_none_cpa(
        self, raw: MarketGoogleData,
    ) -> None:
        """CPA is None for every normalized metric where conversions == 0."""
        normalizer = DataNormalizer(audit_date=date(2026, 3, 15))
        normalized = normalizer.normalize_market_google_data(raw)

        for m in normalized:
            if m.conversions == 0:
                assert m.cpa is None, (
                    f"CPA should be None when conversions=0, "
                    f"got {m.cpa} for campaign '{m.campaign_name}'"
                )

    @given(raw=market_google_data_with_zero_denominators())
    @settings(max_examples=100, deadline=None)
    def test_normalize_zero_impressions_yields_none_ctr(
        self, raw: MarketGoogleData,
    ) -> None:
        """CTR is None for every normalized metric where impressions == 0."""
        normalizer = DataNormalizer(audit_date=date(2026, 3, 15))
        normalized = normalizer.normalize_market_google_data(raw)

        for m in normalized:
            if m.impressions == 0:
                assert m.ctr is None, (
                    f"CTR should be None when impressions=0, "
                    f"got {m.ctr} for campaign '{m.campaign_name}'"
                )

    @given(raw=market_google_data_with_zero_denominators())
    @settings(max_examples=100, deadline=None)
    def test_normalize_zero_clicks_yields_none_cvr(
        self, raw: MarketGoogleData,
    ) -> None:
        """Conversion rate is None for every normalized metric where clicks == 0."""
        normalizer = DataNormalizer(audit_date=date(2026, 3, 15))
        normalized = normalizer.normalize_market_google_data(raw)

        for m in normalized:
            if m.clicks == 0:
                assert m.conversion_rate is None, (
                    f"conversion_rate should be None when clicks=0, "
                    f"got {m.conversion_rate} for campaign '{m.campaign_name}'"
                )

    @given(raw=market_google_data_with_zero_denominators())
    @settings(max_examples=100, deadline=None)
    def test_aggregate_zero_denominators_yields_none_ratios(
        self, raw: MarketGoogleData,
    ) -> None:
        """After normalize + aggregate, zero-denominator ratios are still None."""
        normalizer = DataNormalizer(audit_date=date(2026, 3, 15))
        normalized = normalizer.normalize_market_google_data(raw)
        aggregated = normalizer.aggregate_across_accounts(normalized)

        for m in aggregated:
            if m.conversions == 0:
                assert m.cpa is None, (
                    f"Aggregated CPA should be None when conversions=0, "
                    f"got {m.cpa} for '{m.campaign_name}'"
                )
            if m.impressions == 0:
                assert m.ctr is None, (
                    f"Aggregated CTR should be None when impressions=0, "
                    f"got {m.ctr} for '{m.campaign_name}'"
                )
            if m.clicks == 0:
                assert m.conversion_rate is None, (
                    f"Aggregated conversion_rate should be None when clicks=0, "
                    f"got {m.conversion_rate} for '{m.campaign_name}'"
                )
