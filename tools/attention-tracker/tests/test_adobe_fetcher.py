"""Unit tests for the Adobe Analytics Data Fetcher.

Tests cover:
- Successful fetch of traffic, conversion, and registration data
- Segmentation by market and campaign type (Brand vs Non-Brand)
- Graceful failure handling — returns empty data with error flag
- fetch_all orchestration method
- Missing report suite handling

Validates: Requirements 2.1, 2.2, 2.3
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Optional

import pytest

from paid_search_audit.adobe_fetcher import (
    AdobeAnalyticsDataFetcher,
    AdobeConfig,
    AdobeFetchResult,
    ConversionData,
    RegistrationData,
    TrafficData,
)
from paid_search_audit.config import MarketConfig


# ------------------------------------------------------------------ #
# Mock HTTP client
# ------------------------------------------------------------------ #

@dataclass
class MockResponse:
    """Fake HTTP response for testing."""
    _json: Any = None
    status_code: int = 200
    _raise: bool = False

    def json(self) -> Any:
        return self._json or {}

    def raise_for_status(self) -> None:
        if self._raise:
            raise Exception("HTTP 500 Internal Server Error")


class MockHttpClient:
    """Injectable mock HTTP client."""

    def __init__(self, responses: Optional[list[MockResponse]] = None) -> None:
        self._responses = list(responses or [])
        self._call_index = 0
        self.post_calls: list[dict[str, Any]] = []
        self.get_calls: list[dict[str, Any]] = []

    def post(self, url: str, **kwargs: Any) -> MockResponse:
        self.post_calls.append({"url": url, **kwargs})
        if self._call_index < len(self._responses):
            resp = self._responses[self._call_index]
            self._call_index += 1
            return resp
        return MockResponse()

    def get(self, url: str, **kwargs: Any) -> MockResponse:
        self.get_calls.append({"url": url, **kwargs})
        return MockResponse()


# ------------------------------------------------------------------ #
# Fixtures
# ------------------------------------------------------------------ #

@pytest.fixture
def adobe_config() -> AdobeConfig:
    return AdobeConfig(
        base_url="https://analytics.adobe.io",
        company_id="test-company",
        client_id="test-client-id",
        client_secret="test-secret",
        access_token="test-token",
        global_report_suite="ab-global",
    )


@pytest.fixture
def market_config() -> MarketConfig:
    return MarketConfig(
        market_code="AU",
        adobe_report_suite="ab-au-suite",
        currency="AUD",
        timezone="Australia/Sydney",
        is_hands_on=True,
        campaign_types=["Brand", "Non-Brand"],
    )


def _traffic_response(market: str = "AU") -> dict[str, Any]:
    """Sample Adobe API response with traffic data."""
    return {
        "rows": [
            {
                "value": f"{market} - Brand - Paid Search",
                "data": [1500, 1200, 4500],
            },
            {
                "value": f"{market} - Non-Brand - Paid Search",
                "data": [3000, 2500, 9000],
            },
        ],
    }


def _conversion_response(market: str = "AU") -> dict[str, Any]:
    return {
        "rows": [
            {
                "value": f"{market} - Brand",
                "data": [50, 0.033],
            },
            {
                "value": f"{market} - Non-Brand",
                "data": [120, 0.04],
            },
        ],
    }


def _registration_response(market: str = "AU") -> dict[str, Any]:
    return {
        "rows": [
            {
                "value": f"{market} - Brand",
                "data": [50],
            },
            {
                "value": f"{market} - Non-Brand",
                "data": [120],
            },
        ],
    }


# ------------------------------------------------------------------ #
# Tests: fetch_traffic_data
# ------------------------------------------------------------------ #

class TestFetchTrafficData:
    """Tests for traffic data fetching (Requirement 2.1)."""

    def test_returns_traffic_data_segmented_by_campaign_type(
        self, adobe_config: AdobeConfig
    ) -> None:
        """Traffic data is segmented by Brand vs Non-Brand (Req 2.2)."""
        mock_http = MockHttpClient([MockResponse(_json=_traffic_response())])
        fetcher = AdobeAnalyticsDataFetcher(adobe_config, http_client=mock_http)

        result = fetcher.fetch_traffic_data(
            "ab-au-suite", ("2026-03-19", "2026-03-19"), "AU",
        )

        assert len(result) == 2
        brand = [r for r in result if r.campaign_type == "Brand"]
        non_brand = [r for r in result if r.campaign_type == "Non-Brand"]
        assert len(brand) == 1
        assert len(non_brand) == 1
        assert brand[0].visits == 1500
        assert brand[0].unique_visitors == 1200
        assert brand[0].page_views == 4500
        assert non_brand[0].visits == 3000

    def test_empty_response_returns_default_entries(
        self, adobe_config: AdobeConfig
    ) -> None:
        """Empty API response produces default entries per campaign type."""
        mock_http = MockHttpClient([MockResponse(_json={"rows": []})])
        fetcher = AdobeAnalyticsDataFetcher(adobe_config, http_client=mock_http)

        result = fetcher.fetch_traffic_data(
            "ab-au-suite", ("2026-03-19", "2026-03-19"), "AU",
        )

        assert len(result) == 2
        assert all(r.visits == 0 for r in result)

    def test_sends_correct_auth_headers(
        self, adobe_config: AdobeConfig
    ) -> None:
        """API requests include proper auth headers."""
        mock_http = MockHttpClient([MockResponse(_json={"rows": []})])
        fetcher = AdobeAnalyticsDataFetcher(adobe_config, http_client=mock_http)

        fetcher.fetch_traffic_data(
            "ab-au-suite", ("2026-03-19", "2026-03-19"), "AU",
        )

        assert len(mock_http.post_calls) == 1
        headers = mock_http.post_calls[0]["headers"]
        assert headers["Authorization"] == "Bearer test-token"
        assert headers["x-api-key"] == "test-client-id"


# ------------------------------------------------------------------ #
# Tests: fetch_conversion_data
# ------------------------------------------------------------------ #

class TestFetchConversionData:
    """Tests for conversion data fetching (Requirement 2.1)."""

    def test_returns_conversion_data_with_rates(
        self, adobe_config: AdobeConfig
    ) -> None:
        mock_http = MockHttpClient([MockResponse(_json=_conversion_response())])
        fetcher = AdobeAnalyticsDataFetcher(adobe_config, http_client=mock_http)

        result = fetcher.fetch_conversion_data(
            "ab-au-suite", ("2026-03-19", "2026-03-19"), "AU",
        )

        assert len(result) == 2
        brand = [r for r in result if r.campaign_type == "Brand"][0]
        assert brand.registrations == 50
        assert brand.conversion_rate == Decimal("0.033")


# ------------------------------------------------------------------ #
# Tests: fetch_registration_data
# ------------------------------------------------------------------ #

class TestFetchRegistrationData:
    """Tests for registration data fetching (Requirement 2.1)."""

    def test_returns_registration_counts(
        self, adobe_config: AdobeConfig
    ) -> None:
        mock_http = MockHttpClient([MockResponse(_json=_registration_response())])
        fetcher = AdobeAnalyticsDataFetcher(adobe_config, http_client=mock_http)

        result = fetcher.fetch_registration_data(
            "ab-au-suite", ("2026-03-19", "2026-03-19"), "AU",
        )

        assert len(result) == 2
        non_brand = [r for r in result if r.campaign_type == "Non-Brand"][0]
        assert non_brand.registrations == 120


# ------------------------------------------------------------------ #
# Tests: fetch_all (orchestrator entry point)
# ------------------------------------------------------------------ #

class TestFetchAll:
    """Tests for the fetch_all orchestration method (Requirement 2.3)."""

    def test_successful_fetch_returns_all_data(
        self, adobe_config: AdobeConfig, market_config: MarketConfig
    ) -> None:
        """Successful fetch populates all data lists with success=True."""
        mock_http = MockHttpClient([
            MockResponse(_json=_traffic_response()),
            MockResponse(_json=_conversion_response()),
            MockResponse(_json=_registration_response()),
        ])
        fetcher = AdobeAnalyticsDataFetcher(adobe_config, http_client=mock_http)

        result = fetcher.fetch_all(market_config, date(2026, 3, 19))

        assert result.success is True
        assert result.error is None
        assert len(result.traffic_data) == 2
        assert len(result.conversion_data) == 2
        assert len(result.registration_data) == 2

    def test_api_failure_returns_empty_with_error_flag(
        self, adobe_config: AdobeConfig, market_config: MarketConfig
    ) -> None:
        """API failure returns success=False with error message (Req 2.3)."""
        mock_http = MockHttpClient([
            MockResponse(_raise=True),
        ])
        fetcher = AdobeAnalyticsDataFetcher(adobe_config, http_client=mock_http)

        result = fetcher.fetch_all(market_config, date(2026, 3, 19))

        assert result.success is False
        assert result.error is not None
        assert "AU" in result.error
        assert result.traffic_data == []
        assert result.conversion_data == []
        assert result.registration_data == []

    def test_missing_report_suite_returns_error(
        self, adobe_config: AdobeConfig
    ) -> None:
        """Missing report suite returns error without calling API."""
        market_no_suite = MarketConfig(
            market_code="MX",
            adobe_report_suite="",
        )
        mock_http = MockHttpClient()
        fetcher = AdobeAnalyticsDataFetcher(adobe_config, http_client=mock_http)

        result = fetcher.fetch_all(market_no_suite, date(2026, 3, 19))

        assert result.success is False
        assert "No Adobe report suite" in (result.error or "")
        assert len(mock_http.post_calls) == 0

    def test_partial_failure_mid_fetch_returns_error(
        self, adobe_config: AdobeConfig, market_config: MarketConfig
    ) -> None:
        """If conversion fetch fails after traffic succeeds, whole result is error."""
        mock_http = MockHttpClient([
            MockResponse(_json=_traffic_response()),  # traffic OK
            MockResponse(_raise=True),                # conversion fails
        ])
        fetcher = AdobeAnalyticsDataFetcher(adobe_config, http_client=mock_http)

        result = fetcher.fetch_all(market_config, date(2026, 3, 19))

        assert result.success is False
        assert result.error is not None


# ------------------------------------------------------------------ #
# Tests: campaign type classification
# ------------------------------------------------------------------ #

class TestCampaignTypeClassification:
    """Tests for Brand vs Non-Brand segmentation (Requirement 2.2)."""

    def test_brand_classification(self) -> None:
        assert AdobeAnalyticsDataFetcher._classify_campaign_type("AU - Brand - PS") == "Brand"

    def test_non_brand_classification(self) -> None:
        assert AdobeAnalyticsDataFetcher._classify_campaign_type("AU - Non-Brand - PS") == "Non-Brand"

    def test_unknown_defaults_to_non_brand(self) -> None:
        assert AdobeAnalyticsDataFetcher._classify_campaign_type("AU - Generic") == "Non-Brand"
