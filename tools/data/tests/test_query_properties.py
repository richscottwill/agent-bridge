"""
Property-based tests for query.py functions.

Covers:
  Property 1: Upsert correctness and idempotence (Task 2.4)
  Property 2: Write error safety (Task 2.5)
  Property 3: Convenience function equivalence to raw SQL (Task 2.6)
  Property 4: List convenience bounds and ordering (Task 2.7)
  Property 11: Read-only connection enforcement (Task 2.8)
  Property 13: Empty query returns empty result (Task 2.9)

Uses hypothesis for property-based testing against a temporary DuckDB instance.
"""

import os
import sys
import tempfile

import duckdb
import pytest
from hypothesis import given, settings, HealthCheck, assume
from hypothesis import strategies as st

# Add parent dir so we can import query and init_db
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from init_db import init_db
from query import (
    db,
    db_write,
    db_upsert,
    market_week,
    market_trend,
    market_month,
    projection,
    callout_scores,
)

# ── Shared fixtures ──

MARKETS = ["AU", "MX", "US", "CA", "UK", "DE", "FR", "IT", "ES", "JP"]


@pytest.fixture(scope="module")
def db_path():
    """Create a temporary DuckDB with full schema for the test module."""
    with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=True) as tmp:
        path = tmp.name
    init_db(path)
    yield path
    for ext in ["", ".wal"]:
        p = path + ext
        if os.path.exists(p):
            os.remove(p)


@pytest.fixture(scope="module")
def seeded_db_path():
    """Create a temporary DuckDB seeded with weekly_metrics, monthly_metrics,
    projections, and callout_scores data for convenience function tests."""
    with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=True) as tmp:
        path = tmp.name
    init_db(path)

    con = duckdb.connect(path)
    # Seed weekly_metrics: 12 weeks for AU, 5 for MX
    for i in range(1, 13):
        con.execute(
            "INSERT INTO weekly_metrics (market, week, regs, cpa, cost, clicks) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            ["AU", f"2026 W{i:02d}", 200 + i * 10, 130.0 + i, 50000.0 + i * 1000, 3000 + i * 100],
        )
    for i in range(1, 6):
        con.execute(
            "INSERT INTO weekly_metrics (market, week, regs, cpa, cost, clicks) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            ["MX", f"2026 W{i:02d}", 100 + i * 5, 80.0 + i, 20000.0 + i * 500, 1500 + i * 50],
        )

    # Seed monthly_metrics
    con.execute(
        "INSERT INTO monthly_metrics (market, month, regs, cpa, spend) "
        "VALUES ('AU', '2026 Mar', 900, 135.0, 121500.0)"
    )
    con.execute(
        "INSERT INTO monthly_metrics (market, month, regs, cpa, spend) "
        "VALUES ('MX', '2026 Mar', 450, 82.0, 36900.0)"
    )

    # Seed projections
    con.execute(
        "INSERT INTO projections (market, week, projected_regs, projected_spend) "
        "VALUES ('AU', '2026 W12', 1050, 155000.0)"
    )

    # Seed callout_scores: 10 weeks for AU
    for i in range(1, 11):
        con.execute(
            "INSERT INTO callout_scores (market, week, overall_score, headline_clarity, "
            "narrative_justification, conciseness, actionability, voice, word_count) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ["AU", f"2026 W{i:02d}", 7.0 + i * 0.1, 7.5, 7.0, 8.0, 7.5, 8.0, 110 + i],
        )

    con.close()
    yield path
    for ext in ["", ".wal"]:
        p = path + ext
        if os.path.exists(p):
            os.remove(p)


# ── Strategies ──

market_st = st.sampled_from(MARKETS)
week_num_st = st.integers(min_value=1, max_value=52)


def week_str(n):
    """Format week number as 'YYYY WNN'."""
    return f"2026 W{n:02d}"


# Strategy for generating valid upsert data for weekly_metrics
def weekly_metrics_data_st():
    return st.fixed_dictionaries({
        "market": market_st,
        "week": week_num_st.map(lambda n: f"2099 W{n:02d}"),  # future year to avoid collisions
        "regs": st.integers(min_value=0, max_value=10000),
        "cpa": st.floats(min_value=0.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
        "cost": st.floats(min_value=0.0, max_value=1e7, allow_nan=False, allow_infinity=False),
        "clicks": st.integers(min_value=0, max_value=100000),
    })


# ══════════════════════════════════════════════════════════════════════
# Property 1: Upsert correctness and idempotence (Task 2.4)
# ══════════════════════════════════════════════════════════════════════


class TestUpsertIdempotence:
    """Property 1: Upsert correctness and idempotence.

    For any valid data dict and key columns, calling db_upsert() SHALL insert
    a new row when no matching key exists, update non-key columns when a
    matching key exists, and calling db_upsert() twice with identical data
    SHALL produce the same database state as calling it once.

    **Validates: Requirements 1.2, 1.3**
    """

    @given(data=weekly_metrics_data_st())
    @settings(
        max_examples=30,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_upsert_inserts_new_row(self, db_path, data):
        """Upserting data with no existing key inserts a new row."""
        key_cols = ["market", "week"]
        # Clean up first
        con = duckdb.connect(db_path)
        con.execute(
            "DELETE FROM weekly_metrics WHERE market = ? AND week = ?",
            [data["market"], data["week"]],
        )
        con.close()

        # Upsert
        db_upsert("weekly_metrics", data, key_cols, db_path=db_path)

        # Verify row exists
        rows = db(
            f"SELECT * FROM weekly_metrics WHERE market = '{data['market']}' AND week = '{data['week']}'",
            db_path=db_path,
        )
        assert len(rows) == 1
        assert rows[0]["regs"] == data["regs"]
        assert rows[0]["clicks"] == data["clicks"]

        # Cleanup
        con = duckdb.connect(db_path)
        con.execute(
            "DELETE FROM weekly_metrics WHERE market = ? AND week = ?",
            [data["market"], data["week"]],
        )
        con.close()

    @given(data=weekly_metrics_data_st(), new_regs=st.integers(min_value=0, max_value=10000))
    @settings(
        max_examples=30,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_upsert_updates_existing_row(self, db_path, data, new_regs):
        """Upserting with an existing key updates non-key columns."""
        key_cols = ["market", "week"]
        # Clean and insert initial
        con = duckdb.connect(db_path)
        con.execute(
            "DELETE FROM weekly_metrics WHERE market = ? AND week = ?",
            [data["market"], data["week"]],
        )
        con.close()

        db_upsert("weekly_metrics", data, key_cols, db_path=db_path)

        # Now upsert with updated regs
        updated = dict(data)
        updated["regs"] = new_regs
        db_upsert("weekly_metrics", updated, key_cols, db_path=db_path)

        # Verify only one row, with updated value
        rows = db(
            f"SELECT * FROM weekly_metrics WHERE market = '{data['market']}' AND week = '{data['week']}'",
            db_path=db_path,
        )
        assert len(rows) == 1
        assert rows[0]["regs"] == new_regs

        # Cleanup
        con = duckdb.connect(db_path)
        con.execute(
            "DELETE FROM weekly_metrics WHERE market = ? AND week = ?",
            [data["market"], data["week"]],
        )
        con.close()

    @given(data=weekly_metrics_data_st())
    @settings(
        max_examples=30,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_upsert_idempotent(self, db_path, data):
        """Calling db_upsert() twice with identical data produces same state as once."""
        key_cols = ["market", "week"]
        # Clean
        con = duckdb.connect(db_path)
        con.execute(
            "DELETE FROM weekly_metrics WHERE market = ? AND week = ?",
            [data["market"], data["week"]],
        )
        con.close()

        # Upsert once
        db_upsert("weekly_metrics", data, key_cols, db_path=db_path)
        rows_after_first = db(
            f"SELECT * FROM weekly_metrics WHERE market = '{data['market']}' AND week = '{data['week']}'",
            db_path=db_path,
        )

        # Upsert again (identical)
        db_upsert("weekly_metrics", data, key_cols, db_path=db_path)
        rows_after_second = db(
            f"SELECT * FROM weekly_metrics WHERE market = '{data['market']}' AND week = '{data['week']}'",
            db_path=db_path,
        )

        assert len(rows_after_first) == 1
        assert len(rows_after_second) == 1
        # Compare all non-timestamp columns
        for key in data:
            assert rows_after_first[0][key] == rows_after_second[0][key]

        # Cleanup
        con = duckdb.connect(db_path)
        con.execute(
            "DELETE FROM weekly_metrics WHERE market = ? AND week = ?",
            [data["market"], data["week"]],
        )
        con.close()


# ══════════════════════════════════════════════════════════════════════
# Property 2: Write error safety (Task 2.5)
# ══════════════════════════════════════════════════════════════════════


# Strategy for generating malformed SQL
malformed_sql_st = st.sampled_from([
    "INSERT INTO nonexistent_table VALUES (1)",
    "INSERT INTO weekly_metrics (market) VALUES ()",
    "UPDAET weekly_metrics SET regs = 1",
    "DELETE FORM weekly_metrics",
    "INSERT INTO weekly_metrics (bad_col_xyz) VALUES ('x')",
    "SELECT * FROM; broken",
    "INSERT INTO weekly_metrics VALUES",
])


class TestWriteErrorSafety:
    """Property 2: Write error safety.

    For any malformed SQL statement passed to db_write(), the function SHALL
    raise a descriptive error and the database state SHALL remain identical
    to its state before the call.

    **Validates: Requirement 1.5**
    """

    @given(bad_sql=malformed_sql_st)
    @settings(
        max_examples=20,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_malformed_sql_raises_and_preserves_state(self, db_path, bad_sql):
        """Malformed SQL raises an error and leaves DB unchanged."""
        # Snapshot row counts before
        con = duckdb.connect(db_path, read_only=True)
        tables = [t[0] for t in con.execute("SHOW TABLES").fetchall()]
        counts_before = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tables}
        con.close()

        # Attempt the bad write
        with pytest.raises(duckdb.Error):
            db_write(bad_sql, db_path=db_path)

        # Verify state unchanged
        con = duckdb.connect(db_path, read_only=True)
        for t in tables:
            count_after = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            assert count_after == counts_before[t], (
                f"Table '{t}' row count changed after malformed SQL: "
                f"{counts_before[t]} -> {count_after}"
            )
        # Verify all tables still exist
        tables_after = [t[0] for t in con.execute("SHOW TABLES").fetchall()]
        for t in tables:
            assert t in tables_after, f"Table '{t}' was dropped by malformed SQL"
        con.close()


# ══════════════════════════════════════════════════════════════════════
# Property 3: Convenience function equivalence to raw SQL (Task 2.6)
# ══════════════════════════════════════════════════════════════════════


class TestConvenienceFunctionEquivalence:
    """Property 3: Convenience function equivalence to raw SQL.

    For any valid market, week, month, and weeks-count inputs, each convenience
    function SHALL return data identical to the equivalent raw SQL query
    executed via db().

    **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6**
    """

    @given(market=st.sampled_from(["AU", "MX"]), week_num=st.integers(min_value=1, max_value=12))
    @settings(
        max_examples=20,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_market_week_matches_raw_sql(self, seeded_db_path, market, week_num):
        """market_week() returns same data as equivalent raw SQL."""
        week = week_str(week_num)
        convenience_result = market_week(market, week, db_path=seeded_db_path)
        raw_result = db(
            f"SELECT * FROM weekly_metrics WHERE market = '{market}' AND week = '{week}'",
            db_path=seeded_db_path,
        )

        if not raw_result:
            assert convenience_result is None
        else:
            assert convenience_result is not None
            assert convenience_result == raw_result[0]

    @given(
        market=st.sampled_from(["AU", "MX"]),
        weeks=st.integers(min_value=1, max_value=15),
    )
    @settings(
        max_examples=20,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_market_trend_matches_raw_sql(self, seeded_db_path, market, weeks):
        """market_trend() returns same data as equivalent raw SQL."""
        convenience_result = market_trend(market, weeks, db_path=seeded_db_path)
        raw_result = db(
            f"SELECT * FROM weekly_metrics WHERE market = '{market}' "
            f"ORDER BY week DESC LIMIT {int(weeks)}",
            db_path=seeded_db_path,
        )
        assert convenience_result == raw_result

    @given(market=st.sampled_from(["AU", "MX"]))
    @settings(
        max_examples=10,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_market_month_matches_raw_sql(self, seeded_db_path, market):
        """market_month() returns same data as equivalent raw SQL."""
        month = "2026 Mar"
        convenience_result = market_month(market, month, db_path=seeded_db_path)
        raw_result = db(
            f"SELECT * FROM monthly_metrics WHERE market = '{market}' AND month = '{month}'",
            db_path=seeded_db_path,
        )

        if not raw_result:
            assert convenience_result is None
        else:
            assert convenience_result == raw_result[0]

    @given(market=st.sampled_from(["AU", "MX"]))
    @settings(
        max_examples=10,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_projection_matches_raw_sql(self, seeded_db_path, market):
        """projection() returns same data as equivalent raw SQL."""
        week = "2026 W12"
        convenience_result = projection(market, week, db_path=seeded_db_path)
        raw_result = db(
            f"SELECT * FROM projections WHERE market = '{market}' AND week = '{week}'",
            db_path=seeded_db_path,
        )

        if not raw_result:
            assert convenience_result is None
        else:
            assert convenience_result == raw_result[0]

    @given(
        market=st.just("AU"),
        weeks=st.integers(min_value=1, max_value=15),
    )
    @settings(
        max_examples=15,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_callout_scores_matches_raw_sql(self, seeded_db_path, market, weeks):
        """callout_scores() returns same data as equivalent raw SQL."""
        convenience_result = callout_scores(market, weeks, db_path=seeded_db_path)
        raw_result = db(
            f"SELECT * FROM callout_scores WHERE market = '{market}' "
            f"ORDER BY week DESC LIMIT {int(weeks)}",
            db_path=seeded_db_path,
        )
        assert convenience_result == raw_result


# ══════════════════════════════════════════════════════════════════════
# Property 4: List convenience bounds and ordering (Task 2.7)
# ══════════════════════════════════════════════════════════════════════


class TestListConvenienceBoundsAndOrdering:
    """Property 4: List convenience functions are bounded, filtered, and ordered.

    For any market and positive integer N, market_trend(market, N) and
    callout_scores(market, N) SHALL return a list of length <= N, where every
    row matches the specified market, and rows are ordered by week descending.

    **Validates: Requirements 2.2, 2.5**
    """

    @given(
        market=st.sampled_from(["AU", "MX"]),
        n=st.integers(min_value=1, max_value=20),
    )
    @settings(
        max_examples=30,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_market_trend_bounded_filtered_ordered(self, seeded_db_path, market, n):
        """market_trend returns <= N rows, all for the given market, week DESC."""
        result = market_trend(market, n, db_path=seeded_db_path)

        # Bounded
        assert len(result) <= n

        # Filtered: every row is for the requested market
        for row in result:
            assert row["market"] == market

        # Ordered: weeks are descending
        weeks = [row["week"] for row in result]
        assert weeks == sorted(weeks, reverse=True), (
            f"Weeks not in DESC order: {weeks}"
        )

    @given(
        market=st.just("AU"),
        n=st.integers(min_value=1, max_value=20),
    )
    @settings(
        max_examples=30,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_callout_scores_bounded_filtered_ordered(self, seeded_db_path, market, n):
        """callout_scores returns <= N rows, all for the given market, week DESC."""
        result = callout_scores(market, n, db_path=seeded_db_path)

        # Bounded
        assert len(result) <= n

        # Filtered
        for row in result:
            assert row["market"] == market

        # Ordered
        weeks = [row["week"] for row in result]
        assert weeks == sorted(weeks, reverse=True), (
            f"Weeks not in DESC order: {weeks}"
        )


# ══════════════════════════════════════════════════════════════════════
# Property 11: Read-only connection enforcement (Task 2.8)
# ══════════════════════════════════════════════════════════════════════


# Strategy for write SQL statements
write_sql_st = st.sampled_from([
    "INSERT INTO weekly_metrics (market, week, regs) VALUES ('ZZ', '2099 W01', 1)",
    "UPDATE weekly_metrics SET regs = 9999 WHERE market = 'AU'",
    "DELETE FROM weekly_metrics WHERE market = 'AU'",
    "INSERT INTO daily_metrics (market, date) VALUES ('ZZ', '2099-01-01')",
    "UPDATE monthly_metrics SET regs = 0 WHERE market = 'AU'",
    "DELETE FROM callout_scores WHERE market = 'AU'",
    "DROP TABLE IF EXISTS weekly_metrics",
    "CREATE TABLE test_rogue (id INTEGER)",
])


class TestReadOnlyConnectionEnforcement:
    """Property 11: Read-only connection enforcement.

    For any SQL write statement (INSERT, UPDATE, DELETE) passed to db(),
    the Query_Helper SHALL raise an error and the database SHALL remain
    unchanged.

    **Validates: Requirements 12.1, 12.3**
    """

    @given(write_sql=write_sql_st)
    @settings(
        max_examples=20,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_db_rejects_write_statements(self, seeded_db_path, write_sql):
        """db() raises an error when given write SQL."""
        # Snapshot state before
        con = duckdb.connect(seeded_db_path, read_only=True)
        tables_before = sorted(t[0] for t in con.execute("SHOW TABLES").fetchall())
        counts_before = {
            t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            for t in tables_before
        }
        con.close()

        # Attempt write via read-only db()
        with pytest.raises(duckdb.Error):
            db(write_sql, db_path=seeded_db_path)

        # Verify state unchanged
        con = duckdb.connect(seeded_db_path, read_only=True)
        tables_after = sorted(t[0] for t in con.execute("SHOW TABLES").fetchall())
        assert tables_before == tables_after, "Tables changed after write attempt via db()"

        for t in tables_before:
            count_after = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            assert count_after == counts_before[t], (
                f"Table '{t}' row count changed: {counts_before[t]} -> {count_after}"
            )
        con.close()


# ══════════════════════════════════════════════════════════════════════
# Property 13: Empty query returns empty result (Task 2.9)
# ══════════════════════════════════════════════════════════════════════


# Tables that are empty in a freshly initialized DB (no seeded data)
EMPTY_TABLES = [
    "change_log",
    "anomalies",
    "competitors",
    "oci_status",
    "agent_actions",
    "agent_observations",
    "decisions",
    "task_queue",
    "experiments",
    "ingest_log",
]


@pytest.fixture()
def empty_db_path():
    """Create a fresh empty DuckDB for each test that needs a clean slate."""
    with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=True) as tmp:
        path = tmp.name
    init_db(path)
    yield path
    for ext in ["", ".wal"]:
        p = path + ext
        if os.path.exists(p):
            os.remove(p)


class TestEmptyQueryReturns:
    """Property 13: Empty query returns empty result.

    For any valid SQL SELECT query against an empty or not-yet-backfilled
    table, the Query_Helper SHALL return an empty list (not raise an error).

    **Validates: Requirement 13.4**
    """

    @given(table=st.sampled_from(EMPTY_TABLES))
    @settings(
        max_examples=20,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_select_from_empty_table_returns_empty_list(self, empty_db_path, table):
        """Querying an empty table returns [] not an error."""
        result = db(f"SELECT * FROM {table}", db_path=empty_db_path)
        assert isinstance(result, list)
        assert len(result) == 0

    @given(
        market=market_st,
        table=st.sampled_from(["weekly_metrics", "monthly_metrics", "projections", "callout_scores"]),
    )
    @settings(
        max_examples=20,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    def test_filtered_query_on_empty_table_returns_empty_list(self, empty_db_path, market, table):
        """Querying an empty table with a WHERE clause returns [] not an error."""
        result = db(
            f"SELECT * FROM {table} WHERE market = '{market}'",
            db_path=empty_db_path,
        )
        assert isinstance(result, list)
        assert len(result) == 0

    def test_convenience_functions_on_empty_db(self, empty_db_path):
        """Convenience functions return None/[] on empty tables, not errors."""
        assert market_week("AU", "2026 W01", db_path=empty_db_path) is None
        assert market_trend("AU", 8, db_path=empty_db_path) == []
        assert market_month("AU", "2026 Mar", db_path=empty_db_path) is None
        assert projection("AU", "2026 W01", db_path=empty_db_path) is None
        assert callout_scores("AU", 8, db_path=empty_db_path) == []
