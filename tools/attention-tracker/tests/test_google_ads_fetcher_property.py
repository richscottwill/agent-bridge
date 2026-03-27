"""Property-based tests for multi-MCC Google Ads fetcher.

**Validates: Requirements 1.6, 1.7, 11.3, 11.4**

Property 11: Cross-MCC Account Completeness — every active account is either
in account_results or failed_accounts.
∀ account ∈ market.account_mappings: account.is_active ⟹
  (account ∈ market_google_data.account_results ∨ account ∈ market_google_data.failed_accounts)

Property 14: Partial MCC Failure Isolation — auth failure on one MCC does not
prevent fetching from other MCCs.
auth_failure(mcc_A) ∧ auth_success(mcc_B) ∧ market has accounts in both ⟹
  report includes mcc_B account data
"""

from __future__ import annotations

from dataclasses import dataclass

from hypothesis import given, settings
from hypothesis import strategies as st

from paid_search_audit.config import AccountMapping, MCCConfig, MarketConfig
from paid_search_audit.google_ads_fetcher import GoogleAdsDataFetcher


# ------------------------------------------------------------------ #
# Fake infrastructure (reuses patterns from test_google_ads_fetcher.py)
# ------------------------------------------------------------------ #

@dataclass
class FakeAccessRow:
    class _CustomerClient:
        def __init__(self, cid: str):
            self.id = cid
            self.status = "ENABLED"

    def __init__(self, account_id: str):
        self.customer_client = self._CustomerClient(account_id)


@dataclass
class FakeCampaignRow:
    class _Campaign:
        def __init__(self):
            self.id = "C1"
            self.name = "Brand"
            self.advertising_channel_type = "SEARCH"

    class _Metrics:
        def __init__(self):
            self.cost_micros = 50_000_000
            self.impressions = 1000
            self.clicks = 100
            self.conversions = 10.0
            self.conversions_value = 500.0
            self.cost_per_conversion = 5.0

    def __init__(self):
        self.campaign = self._Campaign()
        self.metrics = self._Metrics()


@dataclass
class FakeBudgetRow:
    class _Budget:
        def __init__(self):
            self.id = "B1"
            self.name = "Daily Budget"
            self.amount_micros = 100_000_000
            self.recommended_budget_estimated_change_weekly_clicks = 0

    def __init__(self):
        self.campaign_budget = self._Budget()


def _extract_account_id_from_query(query: str) -> str | None:
    import re
    match = re.search(r"customer_client\.id\s*=\s*'([^']+)'", query)
    return match.group(1) if match else None


class SuccessService:
    """Fake GA service that succeeds for all queries."""
    def search(self, customer_id: str, query: str) -> list:
        if "customer_client" in query:
            acct_id = _extract_account_id_from_query(query)
            return [FakeAccessRow(acct_id)] if acct_id else []
        if "campaign_budget" in query:
            return [FakeBudgetRow()]
        return [FakeCampaignRow()]


class SuccessClient:
    def __init__(self):
        self._service = SuccessService()

    def get_service(self, service_name: str, version: str):
        return self._service

    def login_customer_id(self) -> str:
        return "0000000000"


class AllSuccessFactory:
    def create_client(self, mcc: MCCConfig) -> SuccessClient:
        return SuccessClient()


class OneFailingMCCFactory:
    def __init__(self, failing_mcc_id: str):
        self._failing_mcc_id = failing_mcc_id

    def create_client(self, mcc: MCCConfig) -> SuccessClient:
        if mcc.mcc_id == self._failing_mcc_id:
            raise RuntimeError(f"Auth failed for MCC {mcc.mcc_id}")
        return SuccessClient()


def _fast_rate_limiter() -> "MCCRateLimiter":
    """Rate limiter with no delay for fast property tests."""
    from paid_search_audit.google_ads_fetcher import MCCRateLimiter
    return MCCRateLimiter(max_requests_per_second=1_000_000)


# ------------------------------------------------------------------ #
# Hypothesis strategies — use integer-based IDs for speed
# ------------------------------------------------------------------ #

@st.composite
def market_with_multiple_mccs(draw):
    """Generate a MarketConfig with 2-4 MCCs, each owning 1-3 active accounts."""
    num_mccs = draw(st.integers(min_value=2, max_value=4))
    mcc_ids = [f"MCC-{i}" for i in range(num_mccs)]

    mcc_configs = [
        MCCConfig(mcc_id=mid, mcc_name=f"Name-{mid}", credential_ref="ref")
        for mid in mcc_ids
    ]

    accounts: list[AccountMapping] = []
    active_ids: set[str] = set()
    acct_counter = 0

    for mid in mcc_ids:
        n = draw(st.integers(min_value=1, max_value=3))
        for _ in range(n):
            aid = f"A{acct_counter}"
            acct_counter += 1
            active_ids.add(aid)
            accounts.append(AccountMapping(
                account_id=aid, account_name=aid,
                mcc_id=mid, market="AU", is_active=True,
            ))

    market = MarketConfig(market_code="AU", account_mappings=accounts)
    return market, mcc_configs, active_ids


@st.composite
def market_with_mixed_active_inactive(draw):
    """Generate a MarketConfig with a mix of active and inactive accounts."""
    num_mccs = draw(st.integers(min_value=1, max_value=3))
    mcc_ids = [f"MCC-{i}" for i in range(num_mccs)]

    mcc_configs = [
        MCCConfig(mcc_id=mid, mcc_name=f"Name-{mid}", credential_ref="ref")
        for mid in mcc_ids
    ]

    # Pre-draw total accounts and their active flags in bulk
    total_accounts = draw(st.integers(min_value=num_mccs, max_value=num_mccs * 3))
    active_flags = draw(st.lists(
        st.booleans(), min_size=total_accounts, max_size=total_accounts,
    ))

    accounts: list[AccountMapping] = []
    active_ids: set[str] = set()

    for i in range(total_accounts):
        mid = mcc_ids[i % num_mccs]
        aid = f"A{i}"
        is_active = active_flags[i]
        if is_active:
            active_ids.add(aid)
        accounts.append(AccountMapping(
            account_id=aid, account_name=aid,
            mcc_id=mid, market="AU", is_active=is_active,
        ))

    market = MarketConfig(market_code="AU", account_mappings=accounts)
    return market, mcc_configs, active_ids


@st.composite
def market_with_one_failing_mcc(draw):
    """Generate a MarketConfig where exactly one MCC will fail auth."""
    num_mccs = draw(st.integers(min_value=2, max_value=4))
    mcc_ids = [f"MCC-{i}" for i in range(num_mccs)]
    failing_idx = draw(st.integers(min_value=0, max_value=num_mccs - 1))
    failing_mcc_id = mcc_ids[failing_idx]

    mcc_configs = [
        MCCConfig(mcc_id=mid, mcc_name=f"Name-{mid}", credential_ref="ref")
        for mid in mcc_ids
    ]

    accounts: list[AccountMapping] = []
    good_ids: set[str] = set()
    all_ids: set[str] = set()
    acct_counter = 0

    for mid in mcc_ids:
        n = draw(st.integers(min_value=1, max_value=3))
        for _ in range(n):
            aid = f"A{acct_counter}"
            acct_counter += 1
            all_ids.add(aid)
            if mid != failing_mcc_id:
                good_ids.add(aid)
            accounts.append(AccountMapping(
                account_id=aid, account_name=aid,
                mcc_id=mid, market="AU", is_active=True,
            ))

    market = MarketConfig(market_code="AU", account_mappings=accounts)
    return market, mcc_configs, failing_mcc_id, good_ids, all_ids


# ------------------------------------------------------------------ #
# Property 11: Cross-MCC Account Completeness
# ------------------------------------------------------------------ #

class TestCrossMCCAccountCompleteness:
    """Property 11: Cross-MCC Account Completeness.

    **Validates: Requirements 1.6, 1.7, 11.3**

    For every active account in the market config, the account_id appears
    in EITHER account_results OR failed_accounts. The union covers all
    active accounts.
    """

    @given(data=market_with_multiple_mccs())
    @settings(max_examples=50, deadline=None)
    def test_all_active_accounts_accounted_for(
        self,
        data: tuple[MarketConfig, list[MCCConfig], set[str]],
    ) -> None:
        """Every active account appears in account_results or failed_accounts."""
        market, mcc_configs, active_ids = data

        fetcher = GoogleAdsDataFetcher(
            client_factory=AllSuccessFactory(),
            rate_limiter=_fast_rate_limiter(),
        )
        fetcher.set_mcc_configs(mcc_configs)

        result = fetcher.fetch_market_data(market, ("2026-03-01", "2026-03-15"))

        covered = {r.account_id for r in result.account_results} | {
            f.account_id for f in result.failed_accounts
        }

        for acct_id in active_ids:
            assert acct_id in covered, (
                f"Active account {acct_id} missing from both "
                f"account_results and failed_accounts"
            )

    @given(data=market_with_mixed_active_inactive())
    @settings(max_examples=50, deadline=None)
    def test_active_covered_inactive_excluded(
        self,
        data: tuple[MarketConfig, list[MCCConfig], set[str]],
    ) -> None:
        """Active accounts are covered; inactive accounts are excluded."""
        market, mcc_configs, active_ids = data

        fetcher = GoogleAdsDataFetcher(
            client_factory=AllSuccessFactory(),
            rate_limiter=_fast_rate_limiter(),
        )
        fetcher.set_mcc_configs(mcc_configs)

        result = fetcher.fetch_market_data(market, ("2026-03-01", "2026-03-15"))

        covered = {r.account_id for r in result.account_results} | {
            f.account_id for f in result.failed_accounts
        }

        for acct_id in active_ids:
            assert acct_id in covered, (
                f"Active account {acct_id} missing from results"
            )

        inactive_ids = {a.account_id for a in market.account_mappings} - active_ids
        for acct_id in inactive_ids:
            assert acct_id not in covered, (
                f"Inactive account {acct_id} should not appear in results"
            )


# ------------------------------------------------------------------ #
# Property 14: Partial MCC Failure Isolation
# ------------------------------------------------------------------ #

class TestPartialMCCFailureIsolation:
    """Property 14: Partial MCC Failure Isolation.

    **Validates: Requirements 1.7, 11.4**

    Auth failure on one MCC does not prevent fetching from other MCCs.
    Accounts under successful MCCs still appear in account_results.
    """

    @given(data=market_with_one_failing_mcc())
    @settings(max_examples=50, deadline=None)
    def test_good_mcc_accounts_still_fetched(
        self,
        data: tuple[MarketConfig, list[MCCConfig], str, set[str], set[str]],
    ) -> None:
        """Accounts under non-failing MCCs appear in account_results."""
        market, mcc_configs, failing_mcc_id, good_ids, all_ids = data

        fetcher = GoogleAdsDataFetcher(
            client_factory=OneFailingMCCFactory(failing_mcc_id),
            rate_limiter=_fast_rate_limiter(),
        )
        fetcher.set_mcc_configs(mcc_configs)

        result = fetcher.fetch_market_data(market, ("2026-03-01", "2026-03-15"))

        result_ids = {r.account_id for r in result.account_results}

        for acct_id in good_ids:
            assert acct_id in result_ids, (
                f"Account {acct_id} under a healthy MCC was not fetched. "
                f"Failing MCC {failing_mcc_id} should not block other MCCs."
            )

    @given(data=market_with_one_failing_mcc())
    @settings(max_examples=50, deadline=None)
    def test_failed_mcc_accounts_in_failed_list(
        self,
        data: tuple[MarketConfig, list[MCCConfig], str, set[str], set[str]],
    ) -> None:
        """Accounts under the failing MCC appear in failed_accounts."""
        market, mcc_configs, failing_mcc_id, good_ids, all_ids = data

        fetcher = GoogleAdsDataFetcher(
            client_factory=OneFailingMCCFactory(failing_mcc_id),
            rate_limiter=_fast_rate_limiter(),
        )
        fetcher.set_mcc_configs(mcc_configs)

        result = fetcher.fetch_market_data(market, ("2026-03-01", "2026-03-15"))

        failed_ids = {f.account_id for f in result.failed_accounts}
        bad_ids = all_ids - good_ids

        for acct_id in bad_ids:
            assert acct_id in failed_ids, (
                f"Account {acct_id} under failing MCC {failing_mcc_id} "
                f"should be in failed_accounts"
            )

    @given(data=market_with_one_failing_mcc())
    @settings(max_examples=50, deadline=None)
    def test_completeness_holds_with_partial_failure(
        self,
        data: tuple[MarketConfig, list[MCCConfig], str, set[str], set[str]],
    ) -> None:
        """Even with a failing MCC, every active account is accounted for
        (Property 11 still holds under partial failure)."""
        market, mcc_configs, failing_mcc_id, good_ids, all_ids = data

        fetcher = GoogleAdsDataFetcher(
            client_factory=OneFailingMCCFactory(failing_mcc_id),
            rate_limiter=_fast_rate_limiter(),
        )
        fetcher.set_mcc_configs(mcc_configs)

        result = fetcher.fetch_market_data(market, ("2026-03-01", "2026-03-15"))

        covered = {r.account_id for r in result.account_results} | {
            f.account_id for f in result.failed_accounts
        }

        for acct_id in all_ids:
            assert acct_id in covered, (
                f"Active account {acct_id} missing from both "
                f"account_results and failed_accounts under partial failure"
            )
