"""Property-based tests for data model validation.

**Validates: Requirements 12.1, 12.2, 12.3**

Property 5: No Division by Zero — CPA/CTR/CVR static methods return None
when denominators are zero, and return a valid Decimal when denominators
are positive.
"""

from decimal import Decimal

from hypothesis import given, settings
from hypothesis import strategies as st

from paid_search_audit.models import NormalizedMetrics

# --- Strategies ---

# Positive decimals for spend values (non-negative, reasonable range)
decimal_spend = st.decimals(
    min_value=Decimal("0"),
    max_value=Decimal("1000000"),
    allow_nan=False,
    allow_infinity=False,
    places=2,
)

# Non-negative integers for count metrics
non_negative_int = st.integers(min_value=0, max_value=1_000_000)

# Strictly positive integers (denominators that should produce a result)
positive_int = st.integers(min_value=1, max_value=1_000_000)


class TestNoDivisionByZero:
    """Property 5: No Division by Zero.

    **Validates: Requirements 12.1, 12.2, 12.3**
    """

    # --- Zero denominator → None ---

    @given(spend=decimal_spend)
    @settings(max_examples=200)
    def test_safe_cpa_returns_none_when_conversions_zero(self, spend: Decimal) -> None:
        """Requirement 12.1: CPA returns None when conversions == 0."""
        result = NormalizedMetrics.safe_cpa(spend, 0)
        assert result is None, (
            f"safe_cpa({spend}, 0) should be None, got {result}"
        )

    @given(clicks=non_negative_int)
    @settings(max_examples=200)
    def test_safe_ctr_returns_none_when_impressions_zero(self, clicks: int) -> None:
        """Requirement 12.2: CTR returns None when impressions == 0."""
        result = NormalizedMetrics.safe_ctr(clicks, 0)
        assert result is None, (
            f"safe_ctr({clicks}, 0) should be None, got {result}"
        )

    @given(conversions=non_negative_int)
    @settings(max_examples=200)
    def test_safe_conversion_rate_returns_none_when_clicks_zero(self, conversions: int) -> None:
        """Requirement 12.3: Conversion rate returns None when clicks == 0."""
        result = NormalizedMetrics.safe_conversion_rate(conversions, 0)
        assert result is None, (
            f"safe_conversion_rate({conversions}, 0) should be None, got {result}"
        )

    # --- Positive denominator → valid Decimal ---

    @given(spend=decimal_spend, conversions=positive_int)
    @settings(max_examples=200)
    def test_safe_cpa_returns_decimal_when_conversions_positive(
        self, spend: Decimal, conversions: int
    ) -> None:
        """CPA returns a Decimal when conversions > 0."""
        result = NormalizedMetrics.safe_cpa(spend, conversions)
        assert isinstance(result, Decimal), (
            f"safe_cpa({spend}, {conversions}) should be Decimal, got {type(result)}"
        )

    @given(clicks=non_negative_int, impressions=positive_int)
    @settings(max_examples=200)
    def test_safe_ctr_returns_decimal_when_impressions_positive(
        self, clicks: int, impressions: int
    ) -> None:
        """CTR returns a Decimal when impressions > 0."""
        result = NormalizedMetrics.safe_ctr(clicks, impressions)
        assert isinstance(result, Decimal), (
            f"safe_ctr({clicks}, {impressions}) should be Decimal, got {type(result)}"
        )

    @given(conversions=non_negative_int, clicks=positive_int)
    @settings(max_examples=200)
    def test_safe_conversion_rate_returns_decimal_when_clicks_positive(
        self, conversions: int, clicks: int
    ) -> None:
        """Conversion rate returns a Decimal when clicks > 0."""
        result = NormalizedMetrics.safe_conversion_rate(conversions, clicks)
        assert isinstance(result, Decimal), (
            f"safe_conversion_rate({conversions}, {clicks}) should be Decimal, got {type(result)}"
        )
