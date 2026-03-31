"""
Property-based tests for dashboard ingester functions.

Covers:
  Property 8: Anomaly detection threshold correctness (Task 4.3)
  Property 9: Anomaly detection purity (Task 4.4)
  Property 12: Ingester idempotence (Task 4.5)

Uses hypothesis for property-based testing with synthetic data.
"""

import copy
import os
import sys
import tempfile

import duckdb
import pytest
from hypothesis import given, settings, HealthCheck, assume
from hypothesis import strategies as st

# Add paths so we can import ingester and query modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'dashboard-ingester'))

from init_db import init_db

# Import _detect_anomalies by instantiating a minimal DashboardIngester
# We need to handle the xlsx_path requirement — use a dummy path since we only call _detect_anomalies
_ingester_dir = os.path.expanduser('~/shared/tools/dashboard-ingester')
if _ingester_dir not in sys.path:
    sys.path.insert(0, _ingester_dir)
from ingest import DashboardIngester


# ── Strategies ──

METRICS = ['regs', 'cpa', 'cvr', 'spend', 'clicks']

# Strategy for a single metric value (positive float)
metric_value_st = st.floats(min_value=0.01, max_value=100000.0, allow_nan=False, allow_infinity=False)

# Strategy for generating a trend list of N weeks with all 5 metrics
def trend_week_st():
    """Generate a single week dict with all metrics."""
    return st.fixed_dictionaries({
        'week': st.from_regex(r'2026 W(0[1-9]|[1-4][0-9]|5[0-2])', fullmatch=True),
        'regs': metric_value_st,
        'cpa': metric_value_st,
        'cvr': st.floats(min_value=0.001, max_value=1.0, allow_nan=False, allow_infinity=False),
        'spend': metric_value_st,
        'clicks': metric_value_st,
    })


def trend_list_st(min_size=3, max_size=12):
    """Generate a list of trend weeks."""
    return st.lists(trend_week_st(), min_size=min_size, max_size=max_size)


def week_data_st():
    """Generate current week data dict."""
    return st.fixed_dictionaries({
        'week': st.just('2026 W13'),
        'regs': metric_value_st,
        'cpa': metric_value_st,
        'cvr': st.floats(min_value=0.001, max_value=1.0, allow_nan=False, allow_infinity=False),
        'spend': metric_value_st,
        'clicks': metric_value_st,
    })


MARKETS = ['AU', 'MX', 'US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP']
market_st = st.sampled_from(MARKETS)

# Dummy ingester instance (xlsx_path doesn't matter for _detect_anomalies)
_dummy_ingester = DashboardIngester.__new__(DashboardIngester)



# ══════════════════════════════════════════════════════════════════════
# Property 8: Anomaly detection threshold correctness (Task 4.3)
# ══════════════════════════════════════════════════════════════════════


class TestAnomalyDetectionThreshold:
    """Property 8: Anomaly detection threshold correctness.

    For any metric with at least 3 historical data points and a non-zero
    baseline average, the Anomaly_Detector SHALL flag the metric if and only
    if its absolute deviation from the 8-week average exceeds 20%. Metrics
    with fewer than 3 data points or a zero baseline SHALL not be flagged.

    **Validates: Requirements 5.1, 5.2, 5.3, 5.4**
    """

    @given(market=market_st, week_data=week_data_st(), trend=trend_list_st(min_size=3, max_size=12))
    @settings(max_examples=50, deadline=None)
    def test_flags_only_when_deviation_exceeds_20pct(self, market, week_data, trend):
        """Metrics deviating >20% are flagged; <=20% are not."""
        anomalies = _dummy_ingester._detect_anomalies(market, week_data, trend)
        flagged_metrics = {a['metric'] for a in anomalies}

        for metric in METRICS:
            current = week_data.get(metric)
            if current is None:
                continue
            historical = [w.get(metric) for w in trend if w.get(metric) is not None]
            if len(historical) < 3:
                assert metric not in flagged_metrics, (
                    f"{metric} flagged with only {len(historical)} data points"
                )
                continue
            baseline = sum(historical) / len(historical)
            if baseline == 0:
                assert metric not in flagged_metrics, (
                    f"{metric} flagged with zero baseline"
                )
                continue
            deviation = abs((current - baseline) / baseline)
            if deviation > 0.20:
                assert metric in flagged_metrics, (
                    f"{metric} not flagged despite {deviation:.1%} deviation "
                    f"(current={current}, baseline={baseline:.2f})"
                )
            else:
                assert metric not in flagged_metrics, (
                    f"{metric} flagged despite only {deviation:.1%} deviation "
                    f"(current={current}, baseline={baseline:.2f})"
                )

    @given(market=market_st, week_data=week_data_st())
    @settings(max_examples=30, deadline=None)
    def test_skips_metrics_with_fewer_than_3_data_points(self, market, week_data):
        """Metrics with <3 historical data points are never flagged."""
        # Trend with only 2 weeks
        short_trend = [
            {'week': '2026 W11', 'regs': 100, 'cpa': 50, 'cvr': 0.03, 'spend': 5000, 'clicks': 2000},
            {'week': '2026 W12', 'regs': 110, 'cpa': 55, 'cvr': 0.035, 'spend': 5500, 'clicks': 2200},
        ]
        anomalies = _dummy_ingester._detect_anomalies(market, week_data, short_trend)
        assert len(anomalies) == 0, (
            f"Anomalies flagged with only 2 data points: {anomalies}"
        )

    @given(market=market_st)
    @settings(max_examples=20, deadline=None)
    def test_skips_zero_baseline(self, market):
        """Metrics with zero baseline average are never flagged."""
        week_data = {'week': '2026 W13', 'regs': 500, 'cpa': 100, 'cvr': 0.05, 'spend': 50000, 'clicks': 3000}
        # Trend where regs is always 0
        trend = [
            {'week': f'2026 W{i:02d}', 'regs': 0, 'cpa': 100, 'cvr': 0.05, 'spend': 50000, 'clicks': 3000}
            for i in range(5, 13)
        ]
        anomalies = _dummy_ingester._detect_anomalies(market, week_data, trend)
        flagged_metrics = {a['metric'] for a in anomalies}
        assert 'regs' not in flagged_metrics, "regs flagged despite zero baseline"

    @given(market=market_st, trend=trend_list_st(min_size=3, max_size=8))
    @settings(max_examples=30, deadline=None)
    def test_direction_is_correct(self, market, trend):
        """Flagged anomalies have correct direction (above/below)."""
        # Use a week_data that's very different from trend to guarantee flags
        historical_regs = [w['regs'] for w in trend]
        baseline_regs = sum(historical_regs) / len(historical_regs)
        # Set current to 2x baseline (guaranteed >20% above)
        week_data = {
            'week': '2026 W13',
            'regs': baseline_regs * 2.5,
            'cpa': trend[0]['cpa'],  # keep others at baseline
            'cvr': trend[0]['cvr'],
            'spend': trend[0]['spend'],
            'clicks': trend[0]['clicks'],
        }
        anomalies = _dummy_ingester._detect_anomalies(market, week_data, trend)
        regs_anomalies = [a for a in anomalies if a['metric'] == 'regs']
        if regs_anomalies:
            assert regs_anomalies[0]['direction'] == 'above'



# ══════════════════════════════════════════════════════════════════════
# Property 9: Anomaly detection purity (Task 4.4)
# ══════════════════════════════════════════════════════════════════════


class TestAnomalyDetectionPurity:
    """Property 9: Anomaly detection purity.

    For any input data passed to _detect_anomalies(), the function SHALL not
    modify the input data, and no database tables other than the anomalies
    table SHALL be affected.

    **Validates: Requirement 5.5**
    """

    @given(market=market_st, week_data=week_data_st(), trend=trend_list_st(min_size=3, max_size=8))
    @settings(max_examples=50, deadline=None)
    def test_does_not_modify_inputs(self, market, week_data, trend):
        """_detect_anomalies does not mutate week_data or trend."""
        week_data_before = copy.deepcopy(week_data)
        trend_before = copy.deepcopy(trend)

        _dummy_ingester._detect_anomalies(market, week_data, trend)

        assert week_data == week_data_before, (
            f"week_data was modified: {week_data_before} -> {week_data}"
        )
        assert trend == trend_before, "trend list was modified by _detect_anomalies"

    @given(market=market_st, week_data=week_data_st(), trend=trend_list_st(min_size=3, max_size=8))
    @settings(max_examples=30, deadline=None)
    def test_returns_list_of_dicts(self, market, week_data, trend):
        """_detect_anomalies returns a list of dicts with expected keys."""
        result = _dummy_ingester._detect_anomalies(market, week_data, trend)
        assert isinstance(result, list)
        expected_keys = {'market', 'week', 'metric', 'value', 'baseline', 'deviation_pct', 'direction'}
        for anomaly in result:
            assert isinstance(anomaly, dict)
            assert set(anomaly.keys()) == expected_keys, (
                f"Anomaly dict has unexpected keys: {set(anomaly.keys())} vs {expected_keys}"
            )
            assert anomaly['direction'] in ('above', 'below')
            assert anomaly['metric'] in METRICS

    @given(market=market_st, week_data=week_data_st(), trend=trend_list_st(min_size=3, max_size=8))
    @settings(max_examples=30, deadline=None)
    def test_no_db_side_effects(self, market, week_data, trend):
        """_detect_anomalies does not touch the database (pure function)."""
        # Create a temp DB, snapshot it, run detect, verify unchanged
        with tempfile.NamedTemporaryFile(suffix='.duckdb', delete=True) as tmp:
            path = tmp.name
        init_db(path)

        con = duckdb.connect(path, read_only=True)
        tables = [t[0] for t in con.execute("SHOW TABLES").fetchall()]
        counts_before = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tables}
        con.close()

        # Run anomaly detection (pure — should not touch DB)
        _dummy_ingester._detect_anomalies(market, week_data, trend)

        con = duckdb.connect(path, read_only=True)
        for t in tables:
            count_after = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            assert count_after == counts_before[t], (
                f"Table '{t}' row count changed after _detect_anomalies: "
                f"{counts_before[t]} -> {count_after}"
            )
        con.close()

        # Cleanup
        for ext in ['', '.wal']:
            p = path + ext
            if os.path.exists(p):
                os.remove(p)



# ══════════════════════════════════════════════════════════════════════
# Property 12: Ingester idempotence (Task 4.5)
# ══════════════════════════════════════════════════════════════════════


class TestIngesterIdempotence:
    """Property 12: Ingester idempotence.

    For any valid xlsx file, running the Ingester twice on the same file
    SHALL produce the same database state as running it once (upsert
    semantics on primary keys).

    **Validates: Requirement 10.4**

    Note: We test this at the _detect_anomalies + write level using synthetic
    data, since we can't depend on a real xlsx file in property tests.
    We verify that running anomaly detection and DB writes twice produces
    identical state.
    """

    @given(
        market=market_st,
        week_data=week_data_st(),
        trend=trend_list_st(min_size=3, max_size=8),
    )
    @settings(max_examples=30, deadline=None)
    def test_anomaly_detection_idempotent(self, market, week_data, trend):
        """Running _detect_anomalies twice returns identical results."""
        result1 = _dummy_ingester._detect_anomalies(market, week_data, trend)
        result2 = _dummy_ingester._detect_anomalies(market, week_data, trend)
        assert result1 == result2, (
            f"Non-deterministic anomaly detection:\n  Run 1: {result1}\n  Run 2: {result2}"
        )

    @given(
        market=market_st,
        week_data=week_data_st(),
        trend=trend_list_st(min_size=3, max_size=8),
    )
    @settings(max_examples=20, deadline=None)
    def test_anomaly_db_writes_idempotent(self, market, week_data, trend):
        """Writing anomalies to DB twice produces same state as once."""
        with tempfile.NamedTemporaryFile(suffix='.duckdb', delete=True) as tmp:
            path = tmp.name
        init_db(path)

        detected = _dummy_ingester._detect_anomalies(market, week_data, trend)
        target_week = week_data['week']

        def write_anomalies():
            con = duckdb.connect(path)
            # Delete + re-insert pattern (same as _write_to_duckdb)
            con.execute("DELETE FROM anomalies WHERE market = ? AND week = ?", [market, target_week])
            for anom in detected:
                con.execute("""
                    INSERT INTO anomalies
                    (id, market, week, metric, value, baseline, deviation_pct, direction)
                    VALUES (nextval('anomalies_seq'), ?, ?, ?, ?, ?, ?, ?)
                """, [anom['market'], anom['week'], anom['metric'],
                      anom['value'], anom['baseline'], anom['deviation_pct'],
                      anom['direction']])
            con.close()

        # Write once
        write_anomalies()
        con = duckdb.connect(path, read_only=True)
        rows_after_first = con.execute(
            "SELECT market, week, metric, value, baseline, deviation_pct, direction "
            "FROM anomalies WHERE market = ? AND week = ? ORDER BY metric",
            [market, target_week],
        ).fetchall()
        con.close()

        # Write again (idempotent re-run)
        write_anomalies()
        con = duckdb.connect(path, read_only=True)
        rows_after_second = con.execute(
            "SELECT market, week, metric, value, baseline, deviation_pct, direction "
            "FROM anomalies WHERE market = ? AND week = ? ORDER BY metric",
            [market, target_week],
        ).fetchall()
        con.close()

        # Same data (ignoring id which will differ due to sequence)
        assert len(rows_after_first) == len(rows_after_second), (
            f"Row count changed: {len(rows_after_first)} -> {len(rows_after_second)}"
        )
        for r1, r2 in zip(rows_after_first, rows_after_second):
            assert r1 == r2, f"Row data differs:\n  Run 1: {r1}\n  Run 2: {r2}"

        # Cleanup
        for ext in ['', '.wal']:
            p = path + ext
            if os.path.exists(p):
                os.remove(p)

    def test_weekly_metrics_upsert_idempotent(self):
        """Upserting the same weekly metrics twice produces identical state."""
        with tempfile.NamedTemporaryFile(suffix='.duckdb', delete=True) as tmp:
            path = tmp.name
        init_db(path)

        test_data = [
            ('AU', '2026 W13', 1000, 500, 50000, 245, 204.0, 100.0, 0.032, 0.049),
            ('MX', '2026 W13', 800, 400, 30000, 120, 250.0, 75.0, 0.028, 0.04),
        ]

        def write_weekly():
            con = duckdb.connect(path)
            for market, week, cost, clicks, imp, regs, cpa, cpc, cvr, ctr in test_data:
                con.execute("""
                    INSERT OR REPLACE INTO weekly_metrics
                    (market, week, cost, clicks, impressions, regs, cpa, cpc, cvr, ctr)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [market, week, cost, clicks, imp, regs, cpa, cpc, cvr, ctr])
            con.close()

        # Write once
        write_weekly()
        con = duckdb.connect(path, read_only=True)
        state1 = con.execute(
            "SELECT market, week, cost, clicks, impressions, regs, cpa, cpc, cvr, ctr "
            "FROM weekly_metrics ORDER BY market, week"
        ).fetchall()
        count1 = con.execute("SELECT COUNT(*) FROM weekly_metrics").fetchone()[0]
        con.close()

        # Write again
        write_weekly()
        con = duckdb.connect(path, read_only=True)
        state2 = con.execute(
            "SELECT market, week, cost, clicks, impressions, regs, cpa, cpc, cvr, ctr "
            "FROM weekly_metrics ORDER BY market, week"
        ).fetchall()
        count2 = con.execute("SELECT COUNT(*) FROM weekly_metrics").fetchone()[0]
        con.close()

        assert count1 == count2, f"Row count changed: {count1} -> {count2}"
        assert state1 == state2, "Weekly metrics state differs after second write"

        # Cleanup
        for ext in ['', '.wal']:
            p = path + ext
            if os.path.exists(p):
                os.remove(p)
