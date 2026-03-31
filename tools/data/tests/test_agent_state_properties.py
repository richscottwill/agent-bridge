"""
Property-based tests for agent state functions in query.py.

Covers:
  Property 1: Agent state write produces unique row with correct defaults (Task 1.5)
  Property 2: Prior observation query returns correct filtered, ordered, time-windowed results (Task 1.6)
  Property 3: Idempotent projection upsert (Task 1.7)

Uses hypothesis for property-based testing against temporary DuckDB instances.
"""

import os
import sys
import tempfile
import json

import duckdb
import pytest
from hypothesis import given, settings, HealthCheck, assume
from hypothesis import strategies as st

# Add parent dir so we can import query and init_db
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from init_db import init_db
from query import (
    db,
    db_upsert,
    log_agent_action,
    log_agent_observation,
    query_prior_observations,
    log_architecture_eval,
)

# ── Shared strategies ──

MARKETS = ["AU", "MX", "US", "CA", "UK", "DE", "FR", "IT", "ES", "JP"]
AGENTS = ["market-analyst", "callout-writer", "callout-reviewer"]
ACTION_TYPES = ["analysis", "projection", "callout_write", "review", "score"]
OBSERVATION_TYPES = ["anomaly", "pattern", "projection_accuracy",
                     "narrative_thread", "data_quality", "competitive"]
SEVERITIES = ["info", "warning", "critical"]

market_st = st.sampled_from(MARKETS)
agent_st = st.sampled_from(AGENTS)
action_type_st = st.sampled_from(ACTION_TYPES)
obs_type_st = st.sampled_from(OBSERVATION_TYPES)
severity_st = st.sampled_from(SEVERITIES)
week_st = st.from_regex(r"2026 W(0[1-9]|[1-4][0-9]|5[0-3])", fullmatch=True)
description_st = st.text(min_size=1, max_size=200,
                         alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")))
confidence_st = st.one_of(st.none(), st.floats(min_value=0.0, max_value=1.0,
                                                allow_nan=False))


# ── Fixtures ──

@pytest.fixture()
def tmp_db():
    """Create a fresh temporary DuckDB for each test."""
    with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=True) as tmp:
        path = tmp.name
    init_db(path)
    yield path
    for ext in ["", ".wal"]:
        p = path + ext
        if os.path.exists(p):
            os.remove(p)


def _fresh_db():
    """Create a fresh temporary DuckDB (non-fixture, for use inside hypothesis)."""
    path = tempfile.mktemp(suffix=".duckdb")
    init_db(path)
    return path


def _cleanup_db(path):
    """Remove a temporary DuckDB and its WAL file."""
    for ext in ["", ".wal"]:
        p = path + ext
        if os.path.exists(p):
            os.remove(p)


# ══════════════════════════════════════════════════════════════
# Property 1: Agent state write produces unique row with correct defaults
# **Validates: Requirements 4.1, 5.1, 5.2**
# ══════════════════════════════════════════════════════════════

class TestProperty1AgentStateWrite:
    """Property 1: Agent state write produces unique row with correct defaults.

    For any valid combination of agent name, action type, market, week, and
    description, log_agent_action() inserts exactly one new row with a unique
    auto-incremented ID. For any valid combination of agent, observation type,
    market, week, and content, log_agent_observation() inserts exactly one new
    row with acted_on defaulting to false.
    """

    @given(
        agent=agent_st,
        action_type=action_type_st,
        market=market_st,
        week=week_st,
        description=description_st,
        confidence=confidence_st,
    )
    @settings(max_examples=30, deadline=None)
    def test_log_agent_action_unique_row(self, agent, action_type,
                                          market, week, description, confidence):
        """log_agent_action inserts exactly one row with a unique ID."""
        tmp = _fresh_db()
        try:
            action_id = log_agent_action(
                agent=agent, action_type=action_type, market=market,
                week=week, description=description, confidence=confidence,
                db_path=tmp,
            )

            count = db(
                "SELECT COUNT(*) as n FROM agent_actions", db_path=tmp
            )[0]["n"]

            assert count == 1, "Should insert exactly one row"
            assert isinstance(action_id, int), "Should return an integer ID"

            row = db(
                f"SELECT * FROM agent_actions WHERE id = {action_id}", db_path=tmp
            )
            assert len(row) == 1
            assert row[0]["agent"] == agent
            assert row[0]["action_type"] == action_type
            assert row[0]["market"] == market
            assert row[0]["week"] == week
        finally:
            _cleanup_db(tmp)

    @given(
        agent=agent_st,
        obs_type=obs_type_st,
        market=market_st,
        week=week_st,
        content=description_st,
        severity=severity_st,
    )
    @settings(max_examples=30, deadline=None)
    def test_log_agent_observation_unique_row_with_defaults(
        self, agent, obs_type, market, week, content, severity
    ):
        """log_agent_observation inserts exactly one row with acted_on=false."""
        tmp = _fresh_db()
        try:
            obs_id = log_agent_observation(
                agent=agent, observation_type=obs_type, market=market,
                week=week, content=content, severity=severity, db_path=tmp,
            )

            count = db(
                "SELECT COUNT(*) as n FROM agent_observations", db_path=tmp
            )[0]["n"]

            assert count == 1, "Should insert exactly one row"
            assert isinstance(obs_id, int), "Should return an integer ID"

            row = db(
                f"SELECT * FROM agent_observations WHERE id = {obs_id}", db_path=tmp
            )
            assert len(row) == 1
            assert row[0]["agent"] == agent
            assert row[0]["observation_type"] == obs_type
            assert row[0]["acted_on"] == False, "acted_on should default to false"
            assert row[0]["severity"] == severity
        finally:
            _cleanup_db(tmp)

    @given(n=st.integers(min_value=2, max_value=10))
    @settings(max_examples=5, deadline=None)
    def test_multiple_actions_get_unique_ids(self, n):
        """N consecutive log_agent_action calls produce N distinct IDs."""
        tmp = _fresh_db()
        try:
            ids = []
            for i in range(n):
                aid = log_agent_action(
                    agent="market-analyst", action_type="analysis",
                    market="AU", week="2026 W13",
                    description=f"Action {i}", db_path=tmp,
                )
                ids.append(aid)
            assert len(set(ids)) == n, f"Expected {n} unique IDs, got {len(set(ids))}"
        finally:
            _cleanup_db(tmp)


# ══════════════════════════════════════════════════════════════
# Property 2: Prior observation query returns correct filtered, ordered,
#             time-windowed results
# **Validates: Requirements 6.1, 6.2**
# ══════════════════════════════════════════════════════════════

class TestProperty2PriorObservationQuery:
    """Property 2: Prior observation query returns correct filtered, ordered,
    time-windowed results.

    For any market and set of observations with varying timestamps and types,
    query_prior_observations(market, weeks=N) returns only observations for
    that market within the last N*7 days, ordered by created_at descending.
    When observation_type filter is provided, only matching types are returned.
    """

    @given(
        target_market=market_st,
        other_market=market_st,
        obs_type=obs_type_st,
        n_target=st.integers(min_value=1, max_value=5),
        n_other=st.integers(min_value=0, max_value=3),
    )
    @settings(max_examples=20, deadline=None)
    def test_market_filter(self, target_market, other_market,
                           obs_type, n_target, n_other):
        """Only observations for the requested market are returned."""
        assume(target_market != other_market)
        tmp = _fresh_db()
        try:
            for i in range(n_target):
                log_agent_observation(
                    agent="market-analyst", observation_type=obs_type,
                    market=target_market, week="2026 W13",
                    content=f"Target obs {i}", db_path=tmp,
                )
            for i in range(n_other):
                log_agent_observation(
                    agent="market-analyst", observation_type=obs_type,
                    market=other_market, week="2026 W13",
                    content=f"Other obs {i}", db_path=tmp,
                )

            results = query_prior_observations(target_market, weeks=4, db_path=tmp)
            assert len(results) == n_target
            for r in results:
                assert r["market"] == target_market
        finally:
            _cleanup_db(tmp)

    @given(
        market=market_st,
        target_type=obs_type_st,
        other_type=obs_type_st,
    )
    @settings(max_examples=20, deadline=None)
    def test_observation_type_filter(self, market, target_type, other_type):
        """When observation_type filter is provided, only matching types returned."""
        assume(target_type != other_type)
        tmp = _fresh_db()
        try:
            log_agent_observation(
                agent="market-analyst", observation_type=target_type,
                market=market, week="2026 W13",
                content="Target type obs", db_path=tmp,
            )
            log_agent_observation(
                agent="market-analyst", observation_type=other_type,
                market=market, week="2026 W13",
                content="Other type obs", db_path=tmp,
            )

            results = query_prior_observations(
                market, weeks=4, observation_type=target_type, db_path=tmp
            )
            assert len(results) == 1
            assert results[0]["observation_type"] == target_type
        finally:
            _cleanup_db(tmp)

    @given(market=market_st)
    @settings(max_examples=10, deadline=None)
    def test_ordering_descending(self, market):
        """Results are ordered by created_at descending (most recent first)."""
        tmp = _fresh_db()
        try:
            for i in range(3):
                log_agent_observation(
                    agent="market-analyst", observation_type="pattern",
                    market=market, week="2026 W13",
                    content=f"Obs {i}", db_path=tmp,
                )

            results = query_prior_observations(market, weeks=4, db_path=tmp)
            assert len(results) == 3
            for i in range(len(results) - 1):
                assert results[i]["created_at"] >= results[i + 1]["created_at"]
        finally:
            _cleanup_db(tmp)

    def test_empty_result_for_no_observations(self, tmp_db):
        """Returns empty list when no observations exist."""
        results = query_prior_observations("AU", weeks=4, db_path=tmp_db)
        assert results == []

    def test_time_window_excludes_old_observations(self, tmp_db):
        """Observations older than the time window are excluded."""
        # Insert an observation with a backdated created_at
        con = duckdb.connect(tmp_db)
        try:
            next_id = con.execute(
                "SELECT nextval('agent_observations_seq')"
            ).fetchone()[0]
            con.execute("""
                INSERT INTO agent_observations
                    (id, agent, observation_type, market, week, content,
                     severity, acted_on, created_at)
                VALUES (?, 'market-analyst', 'anomaly', 'AU', '2026 W01',
                        'Old observation', 'info', false,
                        current_timestamp - INTERVAL '60' DAY)
            """, [next_id])
        finally:
            con.close()

        # Insert a recent one
        log_agent_observation(
            agent="market-analyst", observation_type="anomaly",
            market="AU", week="2026 W13",
            content="Recent observation", db_path=tmp_db,
        )

        results = query_prior_observations("AU", weeks=4, db_path=tmp_db)
        assert len(results) == 1
        assert results[0]["content"] == "Recent observation"


# ══════════════════════════════════════════════════════════════
# Property 3: Idempotent projection upsert
# **Validates: Requirements 10.1, 10.2, 10.3**
# ══════════════════════════════════════════════════════════════

class TestProperty3IdempotentProjectionUpsert:
    """Property 3: Idempotent projection upsert.

    For any market and week, calling db_upsert('projections', data,
    ['market', 'week']) twice with the same key columns results in exactly
    one row, with the second call's values overwriting the first.
    """

    @given(
        market=market_st,
        week=week_st,
        regs_1=st.integers(min_value=1, max_value=10000),
        regs_2=st.integers(min_value=1, max_value=10000),
        spend_1=st.floats(min_value=0.01, max_value=1000000.0,
                          allow_nan=False, allow_infinity=False),
        spend_2=st.floats(min_value=0.01, max_value=1000000.0,
                          allow_nan=False, allow_infinity=False),
    )
    @settings(max_examples=30, deadline=None)
    def test_upsert_twice_produces_one_row(self, market, week,
                                            regs_1, regs_2, spend_1, spend_2):
        """Two upserts with same market+week produce exactly one row with second values."""
        tmp = _fresh_db()
        try:
            data_1 = {
                "market": market,
                "week": week,
                "projected_regs": regs_1,
                "projected_spend": spend_1,
                "source": "market-analyst",
            }
            data_2 = {
                "market": market,
                "week": week,
                "projected_regs": regs_2,
                "projected_spend": spend_2,
                "source": "market-analyst",
            }

            db_upsert("projections", data_1, ["market", "week"], db_path=tmp)
            db_upsert("projections", data_2, ["market", "week"], db_path=tmp)

            rows = db(
                f"SELECT * FROM projections WHERE market = '{market}' AND week = '{week}'",
                db_path=tmp,
            )
            assert len(rows) == 1, f"Expected 1 row, got {len(rows)}"
            assert rows[0]["projected_regs"] == regs_2, "Second upsert should overwrite"
            assert rows[0]["projected_spend"] == pytest.approx(spend_2), "Second upsert should overwrite"
        finally:
            _cleanup_db(tmp)

    @given(
        market=market_st,
        week=week_st,
        regs=st.integers(min_value=1, max_value=10000),
    )
    @settings(max_examples=15, deadline=None)
    def test_single_upsert_inserts_new_row(self, market, week, regs):
        """A single upsert for a new market+week creates exactly one row."""
        tmp = _fresh_db()
        try:
            data = {
                "market": market,
                "week": week,
                "projected_regs": regs,
                "source": "market-analyst",
            }
            db_upsert("projections", data, ["market", "week"], db_path=tmp)

            rows = db(
                f"SELECT * FROM projections WHERE market = '{market}' AND week = '{week}'",
                db_path=tmp,
            )
            assert len(rows) == 1
            assert rows[0]["projected_regs"] == regs
        finally:
            _cleanup_db(tmp)
