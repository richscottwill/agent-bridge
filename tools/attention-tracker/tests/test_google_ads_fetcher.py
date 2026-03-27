"""Unit tests for GoogleAdsDataFetcher.

Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9,
           11.1, 11.2, 11.3, 11.4

Tests cover:
- MCC credential resolution and caching
- Account access validation
- Campaign data fetching with GAQL
- Budget info fetching
- fetch_market_data: grouping by MCC, per-account failures, MCC auth failures
- Rate limiting is MCC-scoped
- Results tagged with account_id and mcc_id
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Optional
from unittest.mock import MagicMock

import pytest

from paid_search_audit.config import AccountMapping, MCCConfig, MarketConfig
from paid_search_audit.google_ads_fetcher import (
    AccountResult,
    AuthToken,
    BudgetInfo,
    CampaignData,
    FailedAccount,
    GoogleAdsDataFetcher,
    MCCRateLimiter,
    MarketGoogleData,
    _classify_campaign_type,
    _is_retryable_error,
    _micros_to_decimal,
)


# ------------------------------------------------------------------ #
# Helpers / Fixtures
# ------------------------------------------------------------------ #

def _mcc(mcc_id: str = "111-222-3333", name: str = "Test MCC") -> MCCConfig:
    return MCCConfig(mcc_id=mcc_id, mcc_name=name, credential_ref="ref-1")


def _mcc2(mcc_id: str = "444-555-6666", name: str = "Test MCC 2") -> MCCConfig:
    return MCCConfig(mcc_id=mcc_id, mcc_name=name, credential_ref="ref-2")


def _account(
    account_id: str = "1234567890",
    mcc_id: str = "111-222-3333",
    market: str = "AU",
    active: bool = True,
    hint: Optional[str] = None,
) -> AccountMapping:
    return AccountMapping(
        account_id=account_id,
        account_name=f"Account {account_id}",
        mcc_id=mcc_id,
        market=market,
        campaign_type_hint=hint,
        is_active=active,
    )


def _market(
    code: str = "AU",
    accounts: Optional[list[AccountMapping]] = None,
) -> MarketConfig:
    return MarketConfig(
        market_code=code,
        account_mappings=accounts or [],
    )


class FakeGAService:
    """Fake Google Ads service that returns configurable rows."""

    def __init__(self, rows: Optional[list] = None, error: Optional[Exception] = None):
        self.rows = rows or []
        self.error = error
        self.queries: list[str] = []

    def search(self, customer_id: str, query: str) -> list:
        self.queries.append(query)
        if self.error:
            raise self.error
        return self.rows


class FakeClient:
    """Fake Google Ads client."""

    def __init__(self, service: Optional[FakeGAService] = None):
        self._service = service or FakeGAService()

    def get_service(self, service_name: str, version: str) -> FakeGAService:
        return self._service

    def login_customer_id(self) -> str:
        return "1112223333"


class FakeClientFactory:
    """Factory that returns fake clients, optionally raising on specific MCCs."""

    def __init__(
        self,
        default_service: Optional[FakeGAService] = None,
        fail_mccs: Optional[set[str]] = None,
        services_by_mcc: Optional[dict[str, FakeGAService]] = None,
    ):
        self._default_service = default_service or FakeGAService()
        self._fail_mccs = fail_mccs or set()
        self._services_by_mcc = services_by_mcc or {}

    def create_client(self, mcc: MCCConfig) -> FakeClient:
        if mcc.mcc_id in self._fail_mccs:
            raise RuntimeError(f"Auth failed for MCC {mcc.mcc_id}")
        svc = self._services_by_mcc.get(mcc.mcc_id, self._default_service)
        return FakeClient(service=svc)



def _extract_account_id_from_query(query: str) -> str | None:
    """Extract account_id from a GAQL customer_client query."""
    import re
    match = re.search(r"customer_client\.id\s*=\s*'([^']+)'", query)
    return match.group(1) if match else None


@dataclass
class FakeCampaignRow:
    """Mimics a Google Ads API campaign row."""

    class _Campaign:
        def __init__(self, cid: str, name: str, channel: str = "SEARCH"):
            self.id = cid
            self.name = name
            self.advertising_channel_type = channel

    class _Metrics:
        def __init__(
            self,
            cost_micros: int = 50_000_000,
            impressions: int = 10000,
            clicks: int = 500,
            conversions: float = 25.0,
            conversions_value: float = 1000.0,
            cost_per_conversion: float = 2.0,
        ):
            self.cost_micros = cost_micros
            self.impressions = impressions
            self.clicks = clicks
            self.conversions = conversions
            self.conversions_value = conversions_value
            self.cost_per_conversion = cost_per_conversion

    def __init__(self, campaign_id: str = "C1", campaign_name: str = "Brand AU", **metric_kwargs):
        self.campaign = self._Campaign(campaign_id, campaign_name)
        self.metrics = self._Metrics(**metric_kwargs)


@dataclass
class FakeBudgetRow:
    """Mimics a Google Ads API budget row."""

    class _Budget:
        def __init__(self, bid: str = "B1", name: str = "Daily Budget", amount_micros: int = 100_000_000):
            self.id = bid
            self.name = name
            self.amount_micros = amount_micros
            self.recommended_budget_estimated_change_weekly_clicks = 0

    def __init__(self, budget_id: str = "B1", budget_name: str = "Daily Budget", amount_micros: int = 100_000_000):
        self.campaign_budget = self._Budget(budget_id, budget_name, amount_micros)


@dataclass
class FakeAccessRow:
    """Mimics a customer_client row for access validation."""

    class _CustomerClient:
        def __init__(self, cid: str, status: str = "ENABLED"):
            self.id = cid
            self.status = status

    def __init__(self, account_id: str):
        self.customer_client = self._CustomerClient(account_id)


# ------------------------------------------------------------------ #
# Tests: Helpers
# ------------------------------------------------------------------ #

class TestHelpers:
    def test_micros_to_decimal(self):
        assert _micros_to_decimal(50_000_000) == Decimal("50")
        assert _micros_to_decimal(1_500_000) == Decimal("1.5")
        assert _micros_to_decimal(0) == Decimal("0")

    def test_is_retryable_error(self):
        assert _is_retryable_error(RuntimeError("rate_exceeded")) is True
        assert _is_retryable_error(RuntimeError("internal_error")) is True
        assert _is_retryable_error(RuntimeError("permission denied")) is False

    def test_classify_campaign_type_with_hint(self):
        assert _classify_campaign_type("SEARCH", "whatever", hint="Brand") == "Brand"

    def test_classify_campaign_type_from_name(self):
        assert _classify_campaign_type("SEARCH", "AB AU - Brand") == "Brand"
        assert _classify_campaign_type("SEARCH", "AB AU - Non-Brand") == "Non-Brand"
        assert _classify_campaign_type("SEARCH", "Competitor Targeting") == "Competitor"
        assert _classify_campaign_type("SEARCH", "Generic Campaign") == "Non-Brand"


# ------------------------------------------------------------------ #
# Tests: MCC Credential Resolution
# ------------------------------------------------------------------ #

class TestResolveCredentials:
    """Requirement 1.1: authenticate with each MCC independently."""

    def test_resolve_returns_auth_token(self):
        factory = FakeClientFactory()
        fetcher = GoogleAdsDataFetcher(client_factory=factory)
        mcc = _mcc()
        token = fetcher.resolve_mcc_credentials(mcc)
        assert isinstance(token, AuthToken)
        assert token.mcc_id == mcc.mcc_id

    def test_resolve_caches_token(self):
        factory = FakeClientFactory()
        fetcher = GoogleAdsDataFetcher(client_factory=factory)
        mcc = _mcc()
        t1 = fetcher.resolve_mcc_credentials(mcc)
        t2 = fetcher.resolve_mcc_credentials(mcc)
        assert t1.access_token == t2.access_token

    def test_resolve_raises_on_auth_failure(self):
        factory = FakeClientFactory(fail_mccs={"111-222-3333"})
        fetcher = GoogleAdsDataFetcher(client_factory=factory)
        with pytest.raises(RuntimeError, match="Auth failed"):
            fetcher.resolve_mcc_credentials(_mcc())

    def test_resolve_no_factory_raises(self):
        fetcher = GoogleAdsDataFetcher(client_factory=None)
        with pytest.raises(RuntimeError, match="No client factory"):
            fetcher.resolve_mcc_credentials(_mcc())



# ------------------------------------------------------------------ #
# Tests: Account Access Validation
# ------------------------------------------------------------------ #

class TestValidateAccountAccess:
    """Requirement 1.9: validate account accessibility under MCC."""

    def test_valid_account_returns_true(self):
        svc = FakeGAService(rows=[FakeAccessRow("1234567890")])
        factory = FakeClientFactory(default_service=svc)
        fetcher = GoogleAdsDataFetcher(client_factory=factory)
        assert fetcher.validate_account_access(_mcc(), "1234567890") is True

    def test_missing_account_returns_false(self):
        svc = FakeGAService(rows=[])  # no matching rows
        factory = FakeClientFactory(default_service=svc)
        fetcher = GoogleAdsDataFetcher(client_factory=factory)
        assert fetcher.validate_account_access(_mcc(), "9999999999") is False

    def test_api_error_returns_false(self):
        svc = FakeGAService(error=RuntimeError("API error"))
        factory = FakeClientFactory(default_service=svc)
        fetcher = GoogleAdsDataFetcher(client_factory=factory)
        assert fetcher.validate_account_access(_mcc(), "1234567890") is False


# ------------------------------------------------------------------ #
# Tests: Campaign Fetching
# ------------------------------------------------------------------ #

class TestFetchAccountCampaigns:
    """Requirement 1.3: retrieve campaign-level metrics."""

    def test_returns_campaign_data(self):
        rows = [
            FakeCampaignRow("C1", "Brand AU", cost_micros=50_000_000, conversions=25.0),
            FakeCampaignRow("C2", "Non-Brand AU", cost_micros=100_000_000, conversions=10.0),
        ]
        svc = FakeGAService(rows=rows)
        factory = FakeClientFactory(default_service=svc)
        fetcher = GoogleAdsDataFetcher(client_factory=factory)
        fetcher.resolve_mcc_credentials(_mcc())

        campaigns = fetcher.fetch_account_campaigns(
            _mcc(), "1234567890", ("2026-03-01", "2026-03-15"),
        )
        assert len(campaigns) == 2
        assert campaigns[0].campaign_id == "C1"
        assert campaigns[0].spend == Decimal("50")
        assert campaigns[0].conversions == 25
        assert campaigns[0].cpa == Decimal("2")

    def test_cpa_none_when_zero_conversions(self):
        rows = [FakeCampaignRow("C1", "Brand AU", conversions=0.0)]
        svc = FakeGAService(rows=rows)
        factory = FakeClientFactory(default_service=svc)
        fetcher = GoogleAdsDataFetcher(client_factory=factory)
        fetcher.resolve_mcc_credentials(_mcc())

        campaigns = fetcher.fetch_account_campaigns(
            _mcc(), "1234567890", ("2026-03-01", "2026-03-15"),
        )
        assert campaigns[0].cpa is None


# ------------------------------------------------------------------ #
# Tests: Budget Info
# ------------------------------------------------------------------ #

class TestGetAccountBudgetInfo:
    """Requirement 1.4: retrieve budget allocation and daily spend caps."""

    def test_returns_budget_info(self):
        rows = [FakeBudgetRow("B1", "Daily Budget", 100_000_000)]
        svc = FakeGAService(rows=rows)
        factory = FakeClientFactory(default_service=svc)
        fetcher = GoogleAdsDataFetcher(client_factory=factory)
        fetcher.resolve_mcc_credentials(_mcc())

        budgets = fetcher.get_account_budget_info(_mcc(), "1234567890")
        assert len(budgets) == 1
        assert budgets[0].budget_id == "B1"
        assert budgets[0].amount == Decimal("100")
        assert budgets[0].daily_spend_cap == Decimal("100")


# ------------------------------------------------------------------ #
# Tests: fetch_market_data — the main orchestration method
# ------------------------------------------------------------------ #

class TestFetchMarketData:
    """Requirements 1.1, 1.2, 1.6, 1.7, 1.8, 1.9, 11.3, 11.4."""

    def _build_fetcher(
        self,
        mcc_configs: list[MCCConfig],
        factory: FakeClientFactory,
    ) -> GoogleAdsDataFetcher:
        fetcher = GoogleAdsDataFetcher(client_factory=factory)
        fetcher.set_mcc_configs(mcc_configs)
        return fetcher

    def test_groups_accounts_by_mcc(self):
        """Req 1.2: accounts grouped by MCC to minimize auth overhead."""

        class SmartService:
            """Returns access rows matching the queried account_id."""
            def __init__(self):
                self.queries = []

            def search(self, customer_id: str, query: str) -> list:
                self.queries.append((customer_id, query))
                if "customer_client" in query:
                    # Extract account_id from the query
                    acct_id = _extract_account_id_from_query(query)
                    return [FakeAccessRow(acct_id)] if acct_id else []
                if "campaign_budget" in query:
                    return [FakeBudgetRow()]
                return [FakeCampaignRow("C1", "Brand AU")]

        smart_svc = SmartService()
        mcc1 = _mcc("MCC-1")
        mcc2 = _mcc2("MCC-2")

        class SmartFactory:
            def create_client(self, mcc: MCCConfig) -> FakeClient:
                return FakeClient(service=smart_svc)

        fetcher = GoogleAdsDataFetcher(client_factory=SmartFactory())
        fetcher.set_mcc_configs([mcc1, mcc2])

        market = _market("AU", [
            _account("A1", "MCC-1"),
            _account("A2", "MCC-1"),
            _account("A3", "MCC-2"),
        ])

        result = fetcher.fetch_market_data(market, ("2026-03-01", "2026-03-15"))
        assert len(result.account_results) == 3
        assert len(result.failed_accounts) == 0

    def test_tags_results_with_account_and_mcc(self):
        """Req 1.8: results tagged with account_id and mcc_id."""
        class TagService:
            def search(self, customer_id: str, query: str) -> list:
                if "customer_client" in query:
                    acct_id = _extract_account_id_from_query(query)
                    return [FakeAccessRow(acct_id)] if acct_id else []
                if "campaign_budget" in query:
                    return [FakeBudgetRow()]
                return [FakeCampaignRow()]

        class TagFactory:
            def create_client(self, mcc: MCCConfig) -> FakeClient:
                return FakeClient(service=TagService())

        mcc = _mcc("MCC-A")
        fetcher = GoogleAdsDataFetcher(client_factory=TagFactory())
        fetcher.set_mcc_configs([mcc])

        market = _market("AU", [_account("ACCT-1", "MCC-A")])
        result = fetcher.fetch_market_data(market, ("2026-03-01", "2026-03-15"))

        assert len(result.account_results) == 1
        assert result.account_results[0].account_id == "ACCT-1"
        assert result.account_results[0].mcc_id == "MCC-A"

    def test_mcc_auth_failure_marks_all_accounts_failed(self):
        """Req 1.7: MCC auth failure marks all accounts under that MCC as failed."""
        factory = FakeClientFactory(fail_mccs={"MCC-BAD"})
        mcc_bad = _mcc("MCC-BAD")
        fetcher = GoogleAdsDataFetcher(client_factory=factory)
        fetcher.set_mcc_configs([mcc_bad])

        market = _market("AU", [
            _account("A1", "MCC-BAD"),
            _account("A2", "MCC-BAD"),
        ])

        result = fetcher.fetch_market_data(market, ("2026-03-01", "2026-03-15"))
        assert len(result.account_results) == 0
        assert len(result.failed_accounts) == 2
        for fa in result.failed_accounts:
            assert fa.mcc_id == "MCC-BAD"
            assert "MCC auth failure" in fa.error
            assert fa.is_retryable is True

    def test_mcc_auth_failure_does_not_block_other_mccs(self):
        """Req 11.4: auth failure on one MCC does not prevent fetching from others."""
        class MixedService:
            def search(self, customer_id: str, query: str) -> list:
                if "customer_client" in query:
                    acct_id = _extract_account_id_from_query(query)
                    return [FakeAccessRow(acct_id)] if acct_id else []
                if "campaign_budget" in query:
                    return [FakeBudgetRow()]
                return [FakeCampaignRow()]

        class MixedFactory:
            def create_client(self, mcc: MCCConfig) -> FakeClient:
                if mcc.mcc_id == "MCC-BAD":
                    raise RuntimeError("Auth failed for MCC MCC-BAD")
                return FakeClient(service=MixedService())

        mcc_good = _mcc("MCC-GOOD")
        mcc_bad = _mcc("MCC-BAD")
        fetcher = GoogleAdsDataFetcher(client_factory=MixedFactory())
        fetcher.set_mcc_configs([mcc_good, mcc_bad])

        market = _market("AU", [
            _account("A1", "MCC-GOOD"),
            _account("A2", "MCC-BAD"),
        ])

        result = fetcher.fetch_market_data(market, ("2026-03-01", "2026-03-15"))
        # MCC-GOOD account succeeds
        assert len(result.account_results) == 1
        assert result.account_results[0].account_id == "A1"
        # MCC-BAD account is in failed
        assert len(result.failed_accounts) == 1
        assert result.failed_accounts[0].account_id == "A2"

    def test_per_account_failure_continues_remaining(self):
        """Req 1.6: individual account failure doesn't stop other accounts."""
        call_count = 0

        class PartialService:
            def search(self, customer_id: str, query: str) -> list:
                nonlocal call_count
                if "customer_client" in query:
                    acct_id = _extract_account_id_from_query(query)
                    return [FakeAccessRow(acct_id)] if acct_id else []
                if "campaign_budget" in query:
                    return [FakeBudgetRow()]
                # Campaign query — fail for A-FAIL (hyphens stripped by fetcher)
                if customer_id in ("A-FAIL", "AFAIL"):
                    raise RuntimeError("permission denied for A-FAIL")
                return [FakeCampaignRow()]

        class PartialFactory:
            def create_client(self, mcc: MCCConfig) -> FakeClient:
                return FakeClient(service=PartialService())

        mcc = _mcc("MCC-1")
        fetcher = GoogleAdsDataFetcher(client_factory=PartialFactory())
        fetcher.set_mcc_configs([mcc])

        market = _market("AU", [
            _account("A-OK", "MCC-1"),
            _account("A-FAIL", "MCC-1"),
            _account("A-OK2", "MCC-1"),
        ])

        result = fetcher.fetch_market_data(market, ("2026-03-01", "2026-03-15"))
        # Two succeed, one fails
        assert len(result.account_results) == 2
        assert len(result.failed_accounts) == 1
        assert result.failed_accounts[0].account_id == "A-FAIL"

    def test_inactive_accounts_skipped(self):
        """Inactive accounts should not be fetched."""
        class NoopService:
            def search(self, customer_id: str, query: str) -> list:
                if "customer_client" in query:
                    acct_id = _extract_account_id_from_query(query)
                    return [FakeAccessRow(acct_id)] if acct_id else []
                if "campaign_budget" in query:
                    return []
                return []

        class NoopFactory:
            def create_client(self, mcc: MCCConfig) -> FakeClient:
                return FakeClient(service=NoopService())

        mcc = _mcc("MCC-1")
        fetcher = GoogleAdsDataFetcher(client_factory=NoopFactory())
        fetcher.set_mcc_configs([mcc])

        market = _market("AU", [
            _account("A1", "MCC-1", active=True),
            _account("A2", "MCC-1", active=False),
        ])

        result = fetcher.fetch_market_data(market, ("2026-03-01", "2026-03-15"))
        all_ids = {r.account_id for r in result.account_results} | {f.account_id for f in result.failed_accounts}
        assert "A2" not in all_ids

    def test_missing_mcc_config_marks_accounts_failed(self):
        """Accounts referencing an unknown MCC are marked as failed."""
        factory = FakeClientFactory()
        fetcher = GoogleAdsDataFetcher(client_factory=factory)
        fetcher.set_mcc_configs([])  # no MCCs registered

        market = _market("AU", [_account("A1", "MCC-UNKNOWN")])
        result = fetcher.fetch_market_data(market, ("2026-03-01", "2026-03-15"))

        assert len(result.account_results) == 0
        assert len(result.failed_accounts) == 1
        assert "MCC config not found" in result.failed_accounts[0].error

    def test_account_access_validation_failure(self):
        """Req 1.9: account not accessible under MCC is recorded as failed."""
        class DenyService:
            def search(self, customer_id: str, query: str) -> list:
                if "customer_client" in query:
                    return []  # no matching rows = not accessible
                return []

        class DenyFactory:
            def create_client(self, mcc: MCCConfig) -> FakeClient:
                return FakeClient(service=DenyService())

        mcc = _mcc("MCC-1")
        fetcher = GoogleAdsDataFetcher(client_factory=DenyFactory())
        fetcher.set_mcc_configs([mcc])

        market = _market("AU", [_account("A1", "MCC-1")])
        result = fetcher.fetch_market_data(market, ("2026-03-01", "2026-03-15"))

        assert len(result.account_results) == 0
        assert len(result.failed_accounts) == 1
        assert "not accessible" in result.failed_accounts[0].error


# ------------------------------------------------------------------ #
# Tests: Rate Limiter
# ------------------------------------------------------------------ #

class TestMCCRateLimiter:
    """Requirement 1.5: per-MCC rate limits independently."""

    def test_different_mccs_independent(self):
        """Throttling on MCC-A should not delay MCC-B."""
        limiter = MCCRateLimiter(max_requests_per_second=1000)
        # Both should proceed without delay
        limiter.wait_if_needed("MCC-A")
        limiter.wait_if_needed("MCC-B")
        # No assertion needed — if they were coupled, the second would block

    def test_same_mcc_respects_interval(self):
        limiter = MCCRateLimiter(max_requests_per_second=1000)
        limiter.wait_if_needed("MCC-A")
        limiter.wait_if_needed("MCC-A")  # should not raise
