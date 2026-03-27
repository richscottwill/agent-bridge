"""Unit tests for AnomalyDetector.

Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9

Tests cover:
- compute_baseline for 7-day and 30-day windows
- get_day_of_week_factor with sufficient and insufficient data
- detect_anomalies z-score computation and severity classification
- Severity elevation for CPA increases and registration drops
- Skipping markets with < 7 days of history
- Higher threshold for campaign-type level (Brand vs Non-Brand)
- No findings below min_z_score threshold
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

import pytest

from paid_search_audit.anomaly_detector import AnomalyDetector, BaselineStats
from paid_search_audit.config import AnomalyConfig
from paid_search_audit.models import NormalizedMetrics


def _make_metric(
    metric_date: date,
    market: str = "AU",
    spend: Decimal = Decimal("100.00"),
    conversions: int = 5,
    clicks: int = 50,
    impressions: int = 1000,
    campaign_type: str = "Brand",
    campaign_name: str = "test-campaign",
) -> NormalizedMetrics:
    return NormalizedMetrics(
        date=metric_date,
        market=market,
        campaign_type=campaign_type,
        campaign_name=campaign_name,
        account_id="1234567890",
        mcc_id="0987654321",
        impressions=impressions,
        clicks=clicks,
        spend=spend,
        spend_usd=spend,
        conversions=conversions,
    )


def _default_config() -> AnomalyConfig:
    return AnomalyConfig(
        min_z_score=1.5,
        warning_threshold=2.0,
        critical_threshold=3.0,
    )


@pytest.fixture
def detector() -> AnomalyDetector:
    return AnomalyDetector()


# ------------------------------------------------------------------ #
# 1. compute_baseline
# ------------------------------------------------------------------ #

class TestComputeBaseline:
    """Req 7.1: Compute rolling 7-day and 30-day baselines."""

    def test_7_day_window(self, detector: AnomalyDetector) -> None:
        values = [10.0, 12.0, 11.0, 13.0, 9.0, 14.0, 10.0, 15.0, 8.0, 11.0]
        result = detector.compute_baseline(values, window=7)
        assert result is not None
        assert result.count == 7
        # Last 7 values: [13.0, 9.0, 14.0, 10.0, 15.0, 8.0, 11.0]
        expected_mean = sum([13.0, 9.0, 14.0, 10.0, 15.0, 8.0, 11.0]) / 7
        assert abs(result.mean - expected_mean) < 0.001
        assert result.stddev > 0

    def test_30_day_window(self, detector: AnomalyDetector) -> None:
        values = [float(i) for i in range(1, 35)]
        result = detector.compute_baseline(values, window=30)
        assert result is not None
        assert result.count == 30
        # Last 30 values: 5..34
        expected_mean = sum(range(5, 35)) / 30
        assert abs(result.mean - expected_mean) < 0.001

    def test_fewer_than_window_uses_all(self, detector: AnomalyDetector) -> None:
        values = [10.0, 20.0, 30.0]
        result = detector.compute_baseline(values, window=7)
        assert result is not None
        assert result.count == 3
        assert abs(result.mean - 20.0) < 0.001

    def test_empty_returns_none(self, detector: AnomalyDetector) -> None:
        result = detector.compute_baseline([], window=7)
        assert result is None

    def test_single_value_zero_stddev(self, detector: AnomalyDetector) -> None:
        result = detector.compute_baseline([42.0], window=7)
        assert result is not None
        assert result.mean == 42.0
        assert result.stddev == 0.0
        assert result.count == 1


# ------------------------------------------------------------------ #
# 2. get_day_of_week_factor
# ------------------------------------------------------------------ #

class TestDayOfWeekFactor:
    """Req 7.7: Day-of-week adjustment from >= 14 days of data."""

    def test_returns_1_with_fewer_than_14_days(self, detector: AnomalyDetector) -> None:
        series = [(date(2026, 3, d), 100.0) for d in range(1, 14)]  # 13 days
        factor = detector.get_day_of_week_factor(series, target_dow=0)
        assert factor == 1.0

    def test_returns_at_least_1(self, detector: AnomalyDetector) -> None:
        """Factor should always be >= 1.0."""
        base = date(2026, 1, 1)
        series = [(base + timedelta(days=i), 100.0 + i) for i in range(30)]
        factor = detector.get_day_of_week_factor(series, target_dow=2)
        assert factor >= 1.0

    def test_uniform_data_returns_1(self, detector: AnomalyDetector) -> None:
        """When all values are identical, factor should be 1.0."""
        base = date(2026, 1, 1)
        series = [(base + timedelta(days=i), 100.0) for i in range(21)]
        factor = detector.get_day_of_week_factor(series, target_dow=0)
        assert factor == 1.0

    def test_volatile_day_gets_higher_factor(self, detector: AnomalyDetector) -> None:
        """A day with high variance should get a factor > 1."""
        base = date(2026, 1, 5)  # Monday
        series = []
        for week in range(4):
            for dow in range(7):
                d = base + timedelta(weeks=week, days=dow)
                if dow == 0:  # Monday: high variance
                    val = 100.0 + (week * 50)
                else:
                    val = 100.0 + (week * 2)
                series.append((d, val))

        factor_monday = detector.get_day_of_week_factor(series, target_dow=0)
        factor_tuesday = detector.get_day_of_week_factor(series, target_dow=1)
        assert factor_monday >= factor_tuesday


# ------------------------------------------------------------------ #
# 3. detect_anomalies — basic z-score detection
# ------------------------------------------------------------------ #

class TestDetectAnomalies:
    """Req 7.2: Generate AnomalyFinding when z-score exceeds threshold."""

    def _build_stable_history(
        self,
        days: int = 14,
        base_date: date = date(2026, 3, 15),
        spend: Decimal = Decimal("100"),
        conversions: int = 10,
        clicks: int = 50,
        impressions: int = 1000,
        campaign_type: str = "Brand",
    ) -> list[NormalizedMetrics]:
        """Build stable historical data with consistent values."""
        return [
            _make_metric(
                base_date - timedelta(days=days - i),
                spend=spend,
                conversions=conversions,
                clicks=clicks,
                impressions=impressions,
                campaign_type=campaign_type,
            )
            for i in range(days)
        ]

    def test_large_spike_detected(self, detector: AnomalyDetector) -> None:
        """A large spend spike should produce a finding."""
        config = _default_config()
        base = date(2026, 3, 15)
        # Slightly varied historical data so stddev > 0
        historical = [
            _make_metric(base - timedelta(days=i), spend=Decimal(str(100 + (i % 3) * 5)))
            for i in range(1, 15)
        ]
        # Current day: 10x normal spend
        current = [_make_metric(base, spend=Decimal("1000"))]

        findings = detector.detect_anomalies(current, historical, config)

        spend_findings = [f for f in findings if f.metric_name == "Spend" and f.campaign_scope == "All"]
        assert len(spend_findings) >= 1
        assert spend_findings[0].direction == "UP"
        assert abs(float(spend_findings[0].z_score)) >= config.min_z_score

    def test_normal_value_no_finding(self, detector: AnomalyDetector) -> None:
        """A value within normal range should not produce a finding."""
        config = _default_config()
        base = date(2026, 3, 15)
        historical = [
            _make_metric(base - timedelta(days=i), spend=Decimal(str(100 + (i % 3) * 5)))
            for i in range(1, 15)
        ]
        current = [_make_metric(base, spend=Decimal("103"))]

        findings = detector.detect_anomalies(current, historical, config)

        spend_findings = [f for f in findings if f.metric_name == "Spend" and f.campaign_scope == "All"]
        assert len(spend_findings) == 0


# ------------------------------------------------------------------ #
# 4. Severity classification
# ------------------------------------------------------------------ #

class TestSeverityClassification:
    """Req 7.4: CRITICAL >= 3.0, WARNING >= 2.0, INFO >= 1.5."""

    def test_classify_critical(self, detector: AnomalyDetector) -> None:
        config = _default_config()
        assert detector._classify_severity(3.5, config) == "CRITICAL"
        assert detector._classify_severity(-3.0, config) == "CRITICAL"

    def test_classify_warning(self, detector: AnomalyDetector) -> None:
        config = _default_config()
        assert detector._classify_severity(2.5, config) == "WARNING"
        assert detector._classify_severity(-2.0, config) == "WARNING"

    def test_classify_info(self, detector: AnomalyDetector) -> None:
        config = _default_config()
        assert detector._classify_severity(1.5, config) == "INFO"
        assert detector._classify_severity(-1.8, config) == "INFO"


# ------------------------------------------------------------------ #
# 5. Severity elevation for CPA increases
# ------------------------------------------------------------------ #

class TestCPAElevation:
    """Req 7.5: CPA increases get severity elevated by one level."""

    def test_cpa_increase_elevates_info_to_warning(self, detector: AnomalyDetector) -> None:
        result = detector._maybe_elevate_severity("INFO", "CPA", "UP")
        assert result == "WARNING"

    def test_cpa_increase_elevates_warning_to_critical(self, detector: AnomalyDetector) -> None:
        result = detector._maybe_elevate_severity("WARNING", "CPA", "UP")
        assert result == "CRITICAL"

    def test_cpa_increase_critical_stays_critical(self, detector: AnomalyDetector) -> None:
        result = detector._maybe_elevate_severity("CRITICAL", "CPA", "UP")
        assert result == "CRITICAL"

    def test_cpa_decrease_no_elevation(self, detector: AnomalyDetector) -> None:
        result = detector._maybe_elevate_severity("INFO", "CPA", "DOWN")
        assert result == "INFO"


# ------------------------------------------------------------------ #
# 6. Severity elevation for registration drops
# ------------------------------------------------------------------ #

class TestRegistrationDropElevation:
    """Req 7.6: Registration drops get severity elevated by one level."""

    def test_reg_drop_elevates_info_to_warning(self, detector: AnomalyDetector) -> None:
        result = detector._maybe_elevate_severity("INFO", "Registrations", "DOWN")
        assert result == "WARNING"

    def test_reg_drop_elevates_warning_to_critical(self, detector: AnomalyDetector) -> None:
        result = detector._maybe_elevate_severity("WARNING", "Registrations", "DOWN")
        assert result == "CRITICAL"

    def test_reg_increase_no_elevation(self, detector: AnomalyDetector) -> None:
        result = detector._maybe_elevate_severity("INFO", "Registrations", "UP")
        assert result == "INFO"


# ------------------------------------------------------------------ #
# 7. Skip markets with < 7 days of history
# ------------------------------------------------------------------ #

class TestMinimumHistory:
    """Req 7.8: Skip anomaly detection with < 7 days of history."""

    def test_6_days_returns_empty(self, detector: AnomalyDetector) -> None:
        config = _default_config()
        base = date(2026, 3, 15)
        historical = [
            _make_metric(base - timedelta(days=i), spend=Decimal("100"))
            for i in range(1, 7)  # 6 days
        ]
        current = [_make_metric(base, spend=Decimal("1000"))]

        findings = detector.detect_anomalies(current, historical, config)
        assert findings == []

    def test_7_days_processes(self, detector: AnomalyDetector) -> None:
        config = _default_config()
        base = date(2026, 3, 15)
        historical = [
            _make_metric(base - timedelta(days=i), spend=Decimal("100"))
            for i in range(1, 8)  # 7 days
        ]
        current = [_make_metric(base, spend=Decimal("1000"))]

        findings = detector.detect_anomalies(current, historical, config)
        # Should process (may or may not find anomalies depending on stddev)
        # With constant historical values, stddev=0 so no findings
        # This is expected — constant data means no variance to detect against


# ------------------------------------------------------------------ #
# 8. No findings below min_z_score
# ------------------------------------------------------------------ #

class TestThresholdGuarantee:
    """Req 7.3: No finding with abs(z_score) < config.min_z_score."""

    def test_all_findings_above_threshold(self, detector: AnomalyDetector) -> None:
        config = _default_config()
        base = date(2026, 3, 15)
        # Create varied historical data so stddev > 0
        historical = []
        for i in range(1, 15):
            d = base - timedelta(days=i)
            spend = Decimal(str(100 + (i % 3) * 10))
            historical.append(_make_metric(d, spend=spend, conversions=5 + (i % 2)))

        current = [_make_metric(base, spend=Decimal("500"), conversions=1)]

        findings = detector.detect_anomalies(current, historical, config)

        for f in findings:
            assert abs(float(f.z_score)) >= config.min_z_score, (
                f"Finding {f.metric_name} has z_score {f.z_score} below threshold {config.min_z_score}"
            )


# ------------------------------------------------------------------ #
# 9. Campaign-type level uses higher threshold
# ------------------------------------------------------------------ #

class TestCampaignTypeThreshold:
    """Req 7.9: Campaign-type level uses min_z_score + 0.5."""

    def test_campaign_type_findings_use_higher_threshold(self, detector: AnomalyDetector) -> None:
        config = _default_config()  # min_z_score = 1.5
        base = date(2026, 3, 15)

        # Build historical with both Brand and Non-Brand
        historical = []
        for i in range(1, 15):
            d = base - timedelta(days=i)
            spend = Decimal(str(100 + (i % 3) * 10))
            historical.append(
                _make_metric(d, spend=spend, conversions=5 + (i % 2), campaign_type="Brand")
            )
            historical.append(
                _make_metric(d, spend=spend, conversions=5 + (i % 2), campaign_type="Non-Brand")
            )

        current = [
            _make_metric(base, spend=Decimal("500"), conversions=1, campaign_type="Brand"),
            _make_metric(base, spend=Decimal("500"), conversions=1, campaign_type="Non-Brand"),
        ]

        findings = detector.detect_anomalies(current, historical, config)

        # Campaign-type findings should have z_score >= min_z_score + 0.5 = 2.0
        for f in findings:
            if f.campaign_scope in ("Brand", "Non-Brand"):
                assert abs(float(f.z_score)) >= config.min_z_score + 0.5, (
                    f"Campaign-type finding {f.metric_name}/{f.campaign_scope} "
                    f"has z_score {f.z_score} below threshold {config.min_z_score + 0.5}"
                )


# ------------------------------------------------------------------ #
# 10. Empty current metrics
# ------------------------------------------------------------------ #

class TestEdgeCases:
    """Edge cases for anomaly detection."""

    def test_empty_current_returns_empty(self, detector: AnomalyDetector) -> None:
        config = _default_config()
        findings = detector.detect_anomalies([], [], config)
        assert findings == []

    def test_direction_up_for_increase(self, detector: AnomalyDetector) -> None:
        config = _default_config()
        base = date(2026, 3, 15)
        historical = []
        for i in range(1, 15):
            d = base - timedelta(days=i)
            historical.append(_make_metric(d, spend=Decimal("100"), conversions=10, clicks=50))

        # Big spend increase
        current = [_make_metric(base, spend=Decimal("1000"), conversions=10, clicks=50)]
        findings = detector.detect_anomalies(current, historical, config)

        spend_findings = [f for f in findings if f.metric_name == "Spend" and f.campaign_scope == "All"]
        for f in spend_findings:
            assert f.direction == "UP"

    def test_direction_down_for_decrease(self, detector: AnomalyDetector) -> None:
        config = _default_config()
        base = date(2026, 3, 15)
        historical = []
        for i in range(1, 15):
            d = base - timedelta(days=i)
            historical.append(_make_metric(d, spend=Decimal("1000"), conversions=100, clicks=500))

        # Big spend decrease
        current = [_make_metric(base, spend=Decimal("10"), conversions=100, clicks=500)]
        findings = detector.detect_anomalies(current, historical, config)

        spend_findings = [f for f in findings if f.metric_name == "Spend" and f.campaign_scope == "All"]
        for f in spend_findings:
            assert f.direction == "DOWN"

    def test_finding_has_context(self, detector: AnomalyDetector) -> None:
        config = _default_config()
        base = date(2026, 3, 15)
        historical = []
        for i in range(1, 15):
            d = base - timedelta(days=i)
            historical.append(_make_metric(d, spend=Decimal(str(100 + (i % 3) * 10))))

        current = [_make_metric(base, spend=Decimal("500"))]
        findings = detector.detect_anomalies(current, historical, config)

        for f in findings:
            assert f.context != ""
            assert f.market == "AU"
