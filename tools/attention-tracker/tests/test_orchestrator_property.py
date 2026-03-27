"""Property-based tests for orchestrator graceful degradation.

**Validates: Requirements 11.1, 11.2, 11.4**

Property 1: Completeness — every market with successful API calls
(at least one account_result) has a MarketSection in the report and
appears in markets_audited.

Property 7: Graceful Degradation — API failure for market A does not
prevent market B from appearing in the report.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional, Tuple

from hypothesis import given, settings
from hypothesis import strategies as st

from paid_search_audit.adobe_fetcher import AdobeAnalyticsDataFetcher, AdobeFetchResult
from paid_search_audit.config import (
    AccountMapping,
    AuditConfig,
    MCCConfig,
    MarketConfig,
)
from paid_search_audit.data_store import DataStore
from paid_search_audit.google_ads_fetcher import (
    AccountResult,
    CampaignData,
    FailedAccount,
    GoogleAdsDataFetcher,
    MarketGoogleData,
)
from paid_search_audit.orchestrator import AuditOrchestrator

AUDIT_DATE = date(2026, 3, 15)
MARKET_CODES = ["AU", "MX", "US", "UK", "DE"]


# ------------------------------------------------------------------ #
# Fake fetchers (reuse patterns from test_orchestrator.py)
# ------------------------------------------------------------------ #

class FakeGoogleFetcher(GoogleAdsDataFetcher):
    """Google fetcher returning pre-configured data per market code."""

    def __init__(
        self,
        market_data: Optional[dict[str, MarketGoogleData]] = None,
        raise_for: Optional[set[str]] = None,
    ) -> None:
        super().__init__(client_factory=None, rate_limiter=None)
        self._market_data = market_data or {}
        self._raise_for = raise_for or set()

    def fetch_market_data(
        self, market: MarketConfig, date_range: Tuple[str, str]
    ) -> MarketGoogleData:
        if market.market_code in self._raise_for:
            raise RuntimeError(f"API down for {market.market_code}")
        return self._market_data.get(
            market.market_code,
            MarketGoogleData(market=market.market_code),
        )


class FakeAdobeFetcher(AdobeAnalyticsDataFetcher):
    """Adobe fetcher that always succeeds."""

    def __init__(self) -> None:
        super().__init__(adobe_config=None, http_client=None)

    def fetch_all(self, market_config: MarketConfig, audit_date: date) -> AdobeFetchResult:
        return AdobeFetchResult(success=True, error=None)


# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #

def _campaign(name: str = "Campaign A") -> CampaignData:
    return CampaignData(
        campaign_id="c-1",
        campaign_name=name,
        campaign_type="Brand",
        spend=Decimal("100"),
        impressions=1000,
        clicks=50,
        conversions=5,
    )


def _success_data(market: str) -> MarketGoogleData:
    """MarketGoogleData with one successful account."""
    return MarketGoogleData(
        market=market,
        account_results=[
            AccountResult(
                account_id=f"acc-{market}",
                mcc_id="111-222-3333",
                campaigns=[_campaign()],
            )
        ],
        failed_accounts=[],
    )


def _all_failed_data(market: str) -> MarketGoogleData:
    """MarketGoogleData where all accounts failed."""
    return MarketGoogleData(
        market=market,
        account_results=[],
        failed_accounts=[
            FailedAccount(
                account_id=f"acc-{market}",
                mcc_id="111-222-3333",
                error="timeout",
            )
        ],
    )


def _mcc() -> MCCConfig:
    return MCCConfig(mcc_id="111-222-3333", mcc_name="Test MCC", credential_ref="ref")


def _market(code: str) -> MarketConfig:
    return MarketConfig(
        market_code=code,
        account_mappings=[
            AccountMapping(
                account_id=f"acc-{code}",
                account_name=f"Account {code}",
                mcc_id="111-222-3333",
                market=code,
            )
        ],
        currency="USD",
    )


# ------------------------------------------------------------------ #
# Hypothesis strategies
# ------------------------------------------------------------------ #

@st.composite
def random_market_configs(draw):
    """Generate 1-5 markets, each randomly succeeding or failing.

    Returns (market_configs, google_data_map, raise_for_set,
             expected_success_codes).
    - google_data_map: markets that succeed get _success_data
    - raise_for_set: markets that raise an API exception
    - For markets that "all accounts fail", google_data_map has
      _all_failed_data (no exception, but empty account_results).
    - expected_success_codes: markets that should appear in the report
    """
    num_markets = draw(st.integers(min_value=1, max_value=5))
    codes = MARKET_CODES[:num_markets]

    # Each market gets one of three states:
    #   "success"      -> has account_results
    #   "all_failed"   -> MarketGoogleData with empty account_results
    #   "api_exception" -> fetch_market_data raises
    states = draw(
        st.lists(
            st.sampled_from(["success", "all_failed", "api_exception"]),
            min_size=num_markets,
            max_size=num_markets,
        )
    )

    google_data: dict[str, MarketGoogleData] = {}
    raise_for: set[str] = set()
    expected_success: list[str] = []

    for code, state in zip(codes, states):
        if state == "success":
            google_data[code] = _success_data(code)
            expected_success.append(code)
        elif state == "all_failed":
            google_data[code] = _all_failed_data(code)
            # Not expected in report — all accounts failed
        else:  # api_exception
            raise_for.add(code)
            # Not expected in report — API exception

    market_configs = [_market(c) for c in codes]
    return market_configs, google_data, raise_for, expected_success


@st.composite
def mixed_success_failure_configs(draw):
    """Generate configs where at least one market succeeds and at least one fails.

    Returns (market_configs, google_data_map, raise_for_set,
             success_codes, failure_codes).
    """
    num_markets = draw(st.integers(min_value=2, max_value=5))
    codes = MARKET_CODES[:num_markets]

    # Ensure at least one success and one failure
    success_count = draw(st.integers(min_value=1, max_value=num_markets - 1))
    shuffled = draw(st.permutations(codes))

    success_codes = list(shuffled[:success_count])
    failure_codes = list(shuffled[success_count:])

    google_data: dict[str, MarketGoogleData] = {}
    raise_for: set[str] = set()

    for code in success_codes:
        google_data[code] = _success_data(code)

    # Failures are either api_exception or all_failed
    failure_types = draw(
        st.lists(
            st.sampled_from(["all_failed", "api_exception"]),
            min_size=len(failure_codes),
            max_size=len(failure_codes),
        )
    )
    for code, ftype in zip(failure_codes, failure_types):
        if ftype == "api_exception":
            raise_for.add(code)
        else:
            google_data[code] = _all_failed_data(code)

    market_configs = [_market(c) for c in codes]
    return market_configs, google_data, raise_for, success_codes, failure_codes


# ------------------------------------------------------------------ #
# Property 1: Completeness
# ------------------------------------------------------------------ #

class TestCompletenessProperty:
    """Property 1: Completeness.

    **Validates: Requirements 11.1, 11.2**

    Every market with at least one successful account_result has a
    MarketSection in the report and appears in markets_audited.
    """

    @given(data=random_market_configs())
    @settings(max_examples=50, deadline=None)
    def test_successful_markets_appear_in_report(self, data):
        """Every market with successful API calls appears in the report."""
        market_configs, google_data, raise_for, expected_success = data

        config = AuditConfig(
            markets=market_configs,
            mcc_configs=[_mcc()],
        )
        orch = AuditOrchestrator(
            google_fetcher=FakeGoogleFetcher(
                market_data=google_data, raise_for=raise_for
            ),
            adobe_fetcher=FakeAdobeFetcher(),
            data_store=DataStore(":memory:"),
        )

        report = orch.run_audit(config, AUDIT_DATE)

        section_markets = {s.market for s in report.market_sections}

        for code in expected_success:
            assert code in report.markets_audited, (
                f"Market {code} had successful API calls but is missing "
                f"from markets_audited"
            )
            assert code in section_markets, (
                f"Market {code} had successful API calls but has no "
                f"MarketSection in the report"
            )

    @given(data=random_market_configs())
    @settings(max_examples=50, deadline=None)
    def test_failed_markets_excluded_from_report(self, data):
        """Markets where all accounts failed or API raised do NOT appear."""
        market_configs, google_data, raise_for, expected_success = data

        config = AuditConfig(
            markets=market_configs,
            mcc_configs=[_mcc()],
        )
        orch = AuditOrchestrator(
            google_fetcher=FakeGoogleFetcher(
                market_data=google_data, raise_for=raise_for
            ),
            adobe_fetcher=FakeAdobeFetcher(),
            data_store=DataStore(":memory:"),
        )

        report = orch.run_audit(config, AUDIT_DATE)

        all_codes = {m.market_code for m in market_configs}
        failed_codes = all_codes - set(expected_success)

        for code in failed_codes:
            assert code not in report.markets_audited, (
                f"Market {code} failed but still appears in markets_audited"
            )


# ------------------------------------------------------------------ #
# Property 7: Graceful Degradation
# ------------------------------------------------------------------ #

class TestGracefulDegradationProperty:
    """Property 7: Graceful Degradation.

    **Validates: Requirements 11.1, 11.4**

    API failure for market A does not prevent market B from appearing
    in the report. Successful markets are always present regardless of
    which other markets failed.
    """

    @given(data=mixed_success_failure_configs())
    @settings(max_examples=50, deadline=None)
    def test_successful_markets_unaffected_by_failures(self, data):
        """Successful markets appear in report regardless of other failures."""
        market_configs, google_data, raise_for, success_codes, failure_codes = data

        config = AuditConfig(
            markets=market_configs,
            mcc_configs=[_mcc()],
        )
        orch = AuditOrchestrator(
            google_fetcher=FakeGoogleFetcher(
                market_data=google_data, raise_for=raise_for
            ),
            adobe_fetcher=FakeAdobeFetcher(),
            data_store=DataStore(":memory:"),
        )

        report = orch.run_audit(config, AUDIT_DATE)

        section_markets = {s.market for s in report.market_sections}

        for code in success_codes:
            assert code in report.markets_audited, (
                f"Market {code} succeeded but is missing from "
                f"markets_audited. Failed markets: {failure_codes}"
            )
            assert code in section_markets, (
                f"Market {code} succeeded but has no MarketSection. "
                f"Failed markets: {failure_codes}"
            )

    @given(data=mixed_success_failure_configs())
    @settings(max_examples=50, deadline=None)
    def test_failed_markets_do_not_appear(self, data):
        """Failed markets are excluded from the report."""
        market_configs, google_data, raise_for, success_codes, failure_codes = data

        config = AuditConfig(
            markets=market_configs,
            mcc_configs=[_mcc()],
        )
        orch = AuditOrchestrator(
            google_fetcher=FakeGoogleFetcher(
                market_data=google_data, raise_for=raise_for
            ),
            adobe_fetcher=FakeAdobeFetcher(),
            data_store=DataStore(":memory:"),
        )

        report = orch.run_audit(config, AUDIT_DATE)

        for code in failure_codes:
            assert code not in report.markets_audited, (
                f"Market {code} failed but still appears in markets_audited"
            )
