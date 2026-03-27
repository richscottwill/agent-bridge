"""Property-based tests for anomaly detector.

**Validates: Requirements 7.3**

Property 3: Anomaly Threshold Guarantee — no finding with abs(z_score) < config.min_z_score.
Also verifies that campaign-type findings (Brand/Non-Brand) respect the higher
threshold of min_z_score + 0.5.
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from typing import Optional

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from paid_search_audit.anomaly_detector import AnomalyDetector
from paid_search_audit.config import AnomalyConfig
from paid_search_audit.models import NormalizedMetrics

# --- Strategies ---

# Positive metric values
positive_int = st.integers(min_value=1, max_value=100_000)
positive_spend = st.decimals(
    min_value=Decimal("0.01"),
    max_value=Decimal("100000"),
    allow_nan=False,
    allow_infinity=False,
    places=2,
)

market_strategy = st.sampled_from(["AU", "MX", "US", "JP", "CA", "DE"])
campaign_type_strategy = st.sampled_from(["Brand", "Non-Brand"])


def _build_metric(
    metric_date: date,
    market: str,
    spend: Decimal,
    clicks: int,
    conversions: int,
    impressions: int,
    campaign_type: str = "Brand",
) -> NormalizedMetrics:
    return NormalizedMetrics(
        date=metric_date,
        market=market,
        campaign_type=campaign_type,
        campaign_name="test-campaign",
        account_id="1234567890",
        mcc_id="0987654321",
        impressions=impressions,
        clicks=clicks,
        spend=spend,
        spend_usd=spend,
        conversions=conversions,
        source="GOOGLE_ADS",
    )


@st.composite
def anomaly_config_strategy(draw):
    """Generate a random AnomalyConfig with valid thresholds.

    Ensures min_z_score < warning_threshold < critical_threshold.
    """
    min_z = draw(st.floats(min_value=0.5, max_value=3.0, allow_nan=False, allow_infinity=False))
    warning_offset = draw(st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    critical_offset = draw(st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))

    return AnomalyConfig(
        min_z_score=min_z,
        warning_threshold=min_z + warning_offset,
        critical_threshold=min_z + warning_offset + critical_offset,
    )


@st.composite
def historical_metrics_strategy(draw):
    """Generate 14-30 days of historical metrics with varying values.

    Includes both Brand and Non-Brand campaign types to exercise
    campaign-type level detection.
    """
    market = draw(market_strategy)
    num_days = draw(st.integers(min_value=14, max_value=30))
    base_date = date(2026, 3, 20)

    metrics: list[NormalizedMetrics] = []
    for i in range(num_days):
        d = base_date - timedelta(days=num_days - i)
        for ctype in ["Brand", "Non-Brand"]:
            spend = draw(positive_spend)
            clicks = draw(st.integers(min_value=1, max_value=10_000))
            conversions = draw(st.integers(min_value=0, max_value=clicks))
            impressions = draw(st.integers(min_value=clicks, max_value=100_000))
            metrics.append(_build_metric(d, market, spend, clicks, conversions, impressions, ctype))

    return metrics, market, base_date


@st.composite
def current_day_metrics_strategy(draw, market: str, audit_date: date):
    """Generate current day metrics for both campaign types."""
    metrics: list[NormalizedMetrics] = []
    for ctype in ["Brand", "Non-Brand"]:
        spend = draw(positive_spend)
        clicks = draw(st.integers(min_value=1, max_value=10_000))
        conversions = draw(st.integers(min_value=0, max_value=clicks))
        impressions = draw(st.integers(min_value=clicks, max_value=100_000))
        metrics.append(_build_metric(audit_date, market, spend, clicks, conversions, impressions, ctype))
    return metrics


@st.composite
def full_anomaly_scenario(draw):
    """Generate a complete anomaly detection scenario.

    Returns (current_metrics, historical_metrics, config).
    """
    historical, market, base_date = draw(historical_metrics_strategy())
    current = draw(current_day_metrics_strategy(market, base_date))
    config = draw(anomaly_config_strategy())
    return current, historical, config


class TestAnomalyThresholdGuarantee:
    """Property 3: Anomaly Threshold Guarantee.

    **Validates: Requirements 7.3**

    No finding shall have abs(z_score) < config.min_z_score.
    Campaign-type findings (Brand/Non-Brand) shall have
    abs(z_score) >= config.min_z_score + 0.5.
    """

    @given(scenario=full_anomaly_scenario())
    @settings(max_examples=200, deadline=None)
    def test_no_finding_below_min_z_score(self, scenario):
        """Every finding must have abs(z_score) >= config.min_z_score."""
        current, historical, config = scenario
        detector = AnomalyDetector()

        findings = detector.detect_anomalies(current, historical, config)

        for f in findings:
            assert abs(float(f.z_score)) >= config.min_z_score, (
                f"Finding {f.metric_name} (scope={f.campaign_scope}) has "
                f"abs(z_score)={abs(float(f.z_score)):.4f} < min_z_score={config.min_z_score}"
            )

    @given(scenario=full_anomaly_scenario())
    @settings(max_examples=200, deadline=None)
    def test_campaign_type_findings_use_higher_threshold(self, scenario):
        """Campaign-type findings (Brand/Non-Brand) must have abs(z_score) >= min_z_score + 0.5."""
        current, historical, config = scenario
        detector = AnomalyDetector()

        findings = detector.detect_anomalies(current, historical, config)

        for f in findings:
            if f.campaign_scope in ("Brand", "Non-Brand"):
                assert abs(float(f.z_score)) >= config.min_z_score + 0.5, (
                    f"Campaign-type finding {f.metric_name} (scope={f.campaign_scope}) has "
                    f"abs(z_score)={abs(float(f.z_score)):.4f} < "
                    f"min_z_score + 0.5={config.min_z_score + 0.5}"
                )
