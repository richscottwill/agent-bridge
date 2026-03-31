"""
Property 6: CHECK constraint enforcement.

Attempt inserts with out-of-range values, verify rejection by DB.
Also verify that valid values are accepted.

**Validates: Requirement 3.6**
"""

import os
import sys
import tempfile

import duckdb
import pytest
from hypothesis import given, settings, HealthCheck, assume
from hypothesis import strategies as st

# Add parent dir so we can import init_db
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from init_db import init_db


@pytest.fixture(scope="module")
def db_path():
    """Create a temporary DuckDB database with full schema for the test module."""
    with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=True) as tmp:
        path = tmp.name
    init_db(path)
    yield path
    for ext in ["", ".wal"]:
        p = path + ext
        if os.path.exists(p):
            os.remove(p)


# ── Strategies ──

# Out-of-range scores: outside [0, 10]
out_of_range_score = st.one_of(
    st.floats(min_value=-1e6, max_value=-0.001, allow_nan=False, allow_infinity=False),
    st.floats(min_value=10.001, max_value=1e6, allow_nan=False, allow_infinity=False),
)

# Valid scores: within [0, 10]
valid_score = st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False)

# Out-of-range impression share: outside [0, 100]
out_of_range_impression_share = st.one_of(
    st.floats(min_value=-1e6, max_value=-0.001, allow_nan=False, allow_infinity=False),
    st.floats(min_value=100.001, max_value=1e6, allow_nan=False, allow_infinity=False),
)

# Valid impression share: within [0, 100]
valid_impression_share = st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False)

# Invalid deviation_pct: exactly 0
zero_deviation = st.just(0.0)

# Valid deviation_pct: any non-zero float
valid_deviation = st.floats(allow_nan=False, allow_infinity=False).filter(lambda x: x != 0.0)

# Invalid projected_regs: <= 0
invalid_projected_regs = st.integers(min_value=-10000, max_value=0)

# Valid projected_regs: > 0
valid_projected_regs = st.integers(min_value=1, max_value=100000)



class TestCalloutScoresCheckConstraints:
    """CHECK constraints on callout_scores: all score columns BETWEEN 0 AND 10.

    **Validates: Requirement 3.6**
    """

    SCORE_COLUMNS = [
        "overall_score",
        "headline_clarity",
        "narrative_justification",
        "conciseness",
        "actionability",
        "voice",
    ]

    @given(bad_score=out_of_range_score, col_idx=st.integers(min_value=0, max_value=5))
    @settings(max_examples=30, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_rejects_out_of_range_scores(self, db_path, bad_score, col_idx):
        """Inserting a score outside [0, 10] must raise a constraint error."""
        col = self.SCORE_COLUMNS[col_idx]
        con = duckdb.connect(db_path)
        try:
            with pytest.raises(duckdb.ConstraintException):
                con.execute(
                    f"INSERT INTO callout_scores (market, week, {col}) "
                    f"VALUES ('AU', '2026 W99', ?)",
                    [bad_score],
                )
        finally:
            # Clean up any rows that might have been inserted
            con.execute("DELETE FROM callout_scores WHERE week = '2026 W99'")
            con.close()

    @given(score=valid_score)
    @settings(max_examples=15, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_accepts_valid_scores(self, db_path, score):
        """Inserting a score within [0, 10] must succeed."""
        con = duckdb.connect(db_path)
        try:
            con.execute(
                "DELETE FROM callout_scores WHERE market = 'ZZ' AND week = '2026 W98'"
            )
            con.execute(
                "INSERT INTO callout_scores (market, week, overall_score, headline_clarity, "
                "narrative_justification, conciseness, actionability, voice) "
                "VALUES ('ZZ', '2026 W98', ?, ?, ?, ?, ?, ?)",
                [score, score, score, score, score, score],
            )
            row = con.execute(
                "SELECT overall_score FROM callout_scores WHERE market = 'ZZ' AND week = '2026 W98'"
            ).fetchone()
            assert row is not None
        finally:
            con.execute("DELETE FROM callout_scores WHERE market = 'ZZ'")
            con.close()


class TestCompetitorsCheckConstraints:
    """CHECK constraint on competitors: impression_share BETWEEN 0 AND 100.

    **Validates: Requirement 3.6**
    """

    @given(bad_share=out_of_range_impression_share)
    @settings(max_examples=30, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_rejects_out_of_range_impression_share(self, db_path, bad_share):
        """Inserting impression_share outside [0, 100] must raise a constraint error."""
        con = duckdb.connect(db_path)
        try:
            with pytest.raises(duckdb.ConstraintException):
                con.execute(
                    "INSERT INTO competitors (market, competitor, week, impression_share) "
                    "VALUES ('AU', 'TestComp', '2026 W99', ?)",
                    [bad_share],
                )
        finally:
            con.execute("DELETE FROM competitors WHERE week = '2026 W99'")
            con.close()

    @given(share=valid_impression_share)
    @settings(max_examples=15, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_accepts_valid_impression_share(self, db_path, share):
        """Inserting impression_share within [0, 100] must succeed."""
        con = duckdb.connect(db_path)
        try:
            con.execute("DELETE FROM competitors WHERE market = 'ZZ' AND competitor = 'Valid' AND week = '2026 W98'")
            con.execute(
                "INSERT INTO competitors (market, competitor, week, impression_share) "
                "VALUES ('ZZ', 'Valid', '2026 W98', ?)",
                [share],
            )
            row = con.execute(
                "SELECT impression_share FROM competitors WHERE market = 'ZZ' AND competitor = 'Valid'"
            ).fetchone()
            assert row is not None
        finally:
            con.execute("DELETE FROM competitors WHERE market = 'ZZ'")
            con.close()


class TestAnomaliesCheckConstraints:
    """CHECK constraint on anomalies: deviation_pct != 0.

    **Validates: Requirement 3.6**
    """

    @given(data=st.data())
    @settings(max_examples=15, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_rejects_zero_deviation_pct(self, db_path, data):
        """Inserting deviation_pct = 0 must raise a constraint error."""
        con = duckdb.connect(db_path)
        try:
            with pytest.raises(duckdb.ConstraintException):
                con.execute(
                    "INSERT INTO anomalies (id, market, week, metric, value, baseline, deviation_pct, direction) "
                    "VALUES (99999, 'AU', '2026 W99', 'regs', 100, 100, 0.0, 'above')"
                )
        finally:
            con.execute("DELETE FROM anomalies WHERE id = 99999")
            con.close()

    @given(dev=valid_deviation)
    @settings(max_examples=15, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_accepts_nonzero_deviation_pct(self, db_path, dev):
        """Inserting a non-zero deviation_pct must succeed."""
        con = duckdb.connect(db_path)
        try:
            con.execute("DELETE FROM anomalies WHERE id = 99998")
            con.execute(
                "INSERT INTO anomalies (id, market, week, metric, value, baseline, deviation_pct, direction) "
                "VALUES (99998, 'AU', '2026 W98', 'regs', 300, 200, ?, 'above')",
                [dev],
            )
            row = con.execute("SELECT deviation_pct FROM anomalies WHERE id = 99998").fetchone()
            assert row is not None
        finally:
            con.execute("DELETE FROM anomalies WHERE id = 99998")
            con.close()


class TestProjectionsCheckConstraints:
    """CHECK constraint on projections: projected_regs > 0.

    **Validates: Requirement 3.6**
    """

    @given(bad_regs=invalid_projected_regs)
    @settings(max_examples=30, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_rejects_non_positive_projected_regs(self, db_path, bad_regs):
        """Inserting projected_regs <= 0 must raise a constraint error."""
        con = duckdb.connect(db_path)
        try:
            with pytest.raises(duckdb.ConstraintException):
                con.execute(
                    "INSERT INTO projections (market, week, projected_regs) "
                    "VALUES ('ZZ', '2026 W99', ?)",
                    [bad_regs],
                )
        finally:
            con.execute("DELETE FROM projections WHERE market = 'ZZ' AND week = '2026 W99'")
            con.close()

    @given(good_regs=valid_projected_regs)
    @settings(max_examples=15, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_accepts_positive_projected_regs(self, db_path, good_regs):
        """Inserting projected_regs > 0 must succeed."""
        con = duckdb.connect(db_path)
        try:
            con.execute("DELETE FROM projections WHERE market = 'ZZ' AND week = '2026 W98'")
            con.execute(
                "INSERT INTO projections (market, week, projected_regs) "
                "VALUES ('ZZ', '2026 W98', ?)",
                [good_regs],
            )
            row = con.execute(
                "SELECT projected_regs FROM projections WHERE market = 'ZZ' AND week = '2026 W98'"
            ).fetchone()
            assert row is not None and row[0] == good_regs
        finally:
            con.execute("DELETE FROM projections WHERE market = 'ZZ'")
            con.close()
