"""Tests for attention_tracker.summary — Daily Summary aggregation."""

from __future__ import annotations

import json
import uuid

import pytest

from attention_tracker.database import Database
from attention_tracker.summary import (
    generate_daily_summary,
    generate_top_insight,
    store_daily_summary,
)
from attention_tracker.models import DailySummary


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DATE = "2026-03-27"


def _insert_event(
    conn,
    *,
    category: str = "deep-work",
    duration_ms: int = 60_000,
    productivity_score: float | None = 0.8,
    attention_mode: str = "FOCUSED",
    timestamp: str = "2026-03-27T10:00:00",
    app_name: str = "code",
) -> None:
    conn.execute(
        """\
INSERT INTO activity_events (
    id, timestamp, app_name, window_class, window_title,
    idle_seconds, duration_ms, category, productivity_score,
    rule_name, attention_mode, belief_focused, belief_switching, belief_idle
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            str(uuid.uuid4()),
            timestamp,
            app_name,
            "Code",
            f"{app_name} — window",
            0,
            duration_ms,
            category,
            productivity_score,
            "test-rule",
            attention_mode,
            0.8,
            0.1,
            0.1,
        ),
    )
    conn.commit()


def _insert_session(
    conn,
    *,
    start_time: str = "2026-03-27T09:00:00",
    end_time: str = "2026-03-27T10:00:00",
    category: str = "deep-work",
    total_duration_ms: int = 3_600_000,
    interruption_count: int = 0,
) -> None:
    conn.execute(
        """\
INSERT INTO focus_sessions (
    id, start_time, end_time, category,
    total_duration_ms, interruption_count, app_sequence
) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            str(uuid.uuid4()),
            start_time,
            end_time,
            category,
            total_duration_ms,
            interruption_count,
            json.dumps(["code"]),
        ),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db(tmp_path):
    db_path = str(tmp_path / "test_summary.db")
    _db = Database(db_path)
    yield _db
    _db.close()


# ---------------------------------------------------------------------------
# Empty day
# ---------------------------------------------------------------------------

class TestEmptyDay:
    def test_returns_zeroed_summary(self, db):
        summary = generate_daily_summary(db, _DATE)

        assert summary.date == _DATE
        assert summary.total_active_ms == 0
        assert summary.total_idle_ms == 0
        assert summary.focus_session_count == 0
        assert summary.avg_focus_duration_ms == 0
        assert summary.top_category == ""
        assert summary.category_breakdown == {}
        assert summary.switch_count == 0
        assert summary.productivity_score_avg == 0.0

    def test_empty_day_has_insight(self, db):
        summary = generate_daily_summary(db, _DATE)
        assert isinstance(summary.top_daily_insight, str)
        assert len(summary.top_daily_insight) > 0


# ---------------------------------------------------------------------------
# Single category day
# ---------------------------------------------------------------------------

class TestSingleCategory:
    def test_single_category_totals(self, db):
        conn = db.connection
        _insert_event(conn, category="deep-work", duration_ms=120_000, timestamp="2026-03-27T10:00:00")
        _insert_event(conn, category="deep-work", duration_ms=60_000, timestamp="2026-03-27T10:02:00")

        summary = generate_daily_summary(db, _DATE)

        assert summary.total_active_ms == 180_000
        assert summary.total_idle_ms == 0
        assert summary.top_category == "deep-work"
        assert summary.category_breakdown == {"deep-work": 180_000}
        assert summary.switch_count == 0

    def test_single_category_with_session(self, db):
        conn = db.connection
        _insert_event(conn, category="deep-work", duration_ms=60_000)
        _insert_session(conn, total_duration_ms=3_600_000)

        summary = generate_daily_summary(db, _DATE)

        assert summary.focus_session_count == 1
        assert summary.avg_focus_duration_ms == 3_600_000


# ---------------------------------------------------------------------------
# Mixed categories with NULL scores
# ---------------------------------------------------------------------------

class TestMixedCategories:
    def test_mixed_categories_breakdown(self, db):
        conn = db.connection
        _insert_event(conn, category="deep-work", duration_ms=100_000, productivity_score=0.9, timestamp="2026-03-27T10:00:00")
        _insert_event(conn, category="communication", duration_ms=50_000, productivity_score=0.3, timestamp="2026-03-27T10:02:00")
        _insert_event(conn, category="uncategorized", duration_ms=30_000, productivity_score=None, timestamp="2026-03-27T10:03:00")

        summary = generate_daily_summary(db, _DATE)

        assert summary.category_breakdown == {
            "deep-work": 100_000,
            "communication": 50_000,
            "uncategorized": 30_000,
        }
        assert summary.top_category == "deep-work"
        assert summary.switch_count == 2  # deep-work -> communication -> uncategorized

    def test_total_active_includes_null_score_events(self, db):
        conn = db.connection
        _insert_event(conn, category="deep-work", duration_ms=100_000, productivity_score=0.9, timestamp="2026-03-27T10:00:00")
        _insert_event(conn, category="uncategorized", duration_ms=50_000, productivity_score=None, timestamp="2026-03-27T10:02:00")

        summary = generate_daily_summary(db, _DATE)

        # total_active_ms includes ALL events regardless of NULL score
        assert summary.total_active_ms == 150_000

    def test_idle_events_counted_separately(self, db):
        conn = db.connection
        _insert_event(conn, category="deep-work", duration_ms=100_000, attention_mode="FOCUSED", timestamp="2026-03-27T10:00:00")
        _insert_event(conn, category="deep-work", duration_ms=60_000, attention_mode="IDLE", timestamp="2026-03-27T10:02:00")

        summary = generate_daily_summary(db, _DATE)

        assert summary.total_active_ms == 100_000
        assert summary.total_idle_ms == 60_000


# ---------------------------------------------------------------------------
# Productivity score avg excludes NULLs
# ---------------------------------------------------------------------------

class TestProductivityScoreAvg:
    def test_excludes_nulls_from_avg(self, db):
        conn = db.connection
        # score=0.9, duration=100k → weighted contribution = 90k
        _insert_event(conn, duration_ms=100_000, productivity_score=0.9, timestamp="2026-03-27T10:00:00")
        # score=0.3, duration=100k → weighted contribution = 30k
        _insert_event(conn, duration_ms=100_000, productivity_score=0.3, timestamp="2026-03-27T10:02:00")
        # score=NULL, duration=200k → excluded from avg
        _insert_event(conn, duration_ms=200_000, productivity_score=None, timestamp="2026-03-27T10:04:00")

        summary = generate_daily_summary(db, _DATE)

        # avg = (0.9*100k + 0.3*100k) / (100k + 100k) = 120k / 200k = 0.6
        assert summary.productivity_score_avg == pytest.approx(0.6)

    def test_all_null_scores_returns_zero(self, db):
        conn = db.connection
        _insert_event(conn, duration_ms=100_000, productivity_score=None, timestamp="2026-03-27T10:00:00")
        _insert_event(conn, duration_ms=50_000, productivity_score=None, timestamp="2026-03-27T10:02:00")

        summary = generate_daily_summary(db, _DATE)

        assert summary.productivity_score_avg == 0.0

    def test_single_scored_event(self, db):
        conn = db.connection
        _insert_event(conn, duration_ms=60_000, productivity_score=0.75, timestamp="2026-03-27T10:00:00")

        summary = generate_daily_summary(db, _DATE)

        assert summary.productivity_score_avg == pytest.approx(0.75)


# ---------------------------------------------------------------------------
# Top daily insight format
# ---------------------------------------------------------------------------

class TestTopDailyInsight:
    def test_insight_contains_key_elements(self, db):
        conn = db.connection
        _insert_event(conn, category="deep-work", duration_ms=192 * 60_000, timestamp="2026-03-27T10:00:00")
        _insert_session(conn, total_duration_ms=3_600_000)

        summary = generate_daily_summary(db, _DATE)

        assert "deep-work" in summary.top_daily_insight
        assert "1 deep session" in summary.top_daily_insight

    def test_insight_uses_human_readable_time(self, db):
        conn = db.connection
        # 3h12m = 192 minutes = 11_520_000 ms
        _insert_event(conn, category="deep-work", duration_ms=11_520_000, timestamp="2026-03-27T10:00:00")

        summary = generate_daily_summary(db, _DATE)

        assert "3h12m" in summary.top_daily_insight

    def test_insight_pluralizes_sessions(self, db):
        conn = db.connection
        _insert_event(conn, category="deep-work", duration_ms=60_000, timestamp="2026-03-27T10:00:00")
        _insert_session(conn, start_time="2026-03-27T09:00:00", end_time="2026-03-27T10:00:00")
        _insert_session(conn, start_time="2026-03-27T14:00:00", end_time="2026-03-27T15:00:00")

        summary = generate_daily_summary(db, _DATE)

        assert "2 deep sessions" in summary.top_daily_insight

    def test_generate_top_insight_standalone(self):
        summary = DailySummary(
            date=_DATE,
            total_active_ms=11_520_000,  # 3h12m
            total_idle_ms=0,
            focus_session_count=2,
            avg_focus_duration_ms=5_760_000,
            top_category="deep-work",
            switch_count=14,
        )
        insight = generate_top_insight(summary)

        assert "3h12m" in insight
        assert "deep-work" in insight
        assert "2 deep sessions" in insight
        assert "14 context switches" in insight


# ---------------------------------------------------------------------------
# Store and retrieve round-trip
# ---------------------------------------------------------------------------

class TestStoreRoundTrip:
    def test_store_and_retrieve(self, db):
        summary = DailySummary(
            date=_DATE,
            total_active_ms=180_000,
            total_idle_ms=60_000,
            focus_session_count=2,
            avg_focus_duration_ms=90_000,
            top_category="deep-work",
            category_breakdown={"deep-work": 120_000, "communication": 60_000},
            switch_count=5,
            productivity_score_avg=0.72,
            top_daily_insight="3h focused on deep-work, 2 deep sessions, 5 context switches",
        )

        result = store_daily_summary(db, summary)
        assert result is True

        # Read back
        row = db.connection.execute(
            "SELECT * FROM daily_summaries WHERE date = ?", (_DATE,)
        ).fetchone()
        col_names = [desc[0] for desc in db.connection.execute(
            "SELECT * FROM daily_summaries LIMIT 0"
        ).description]
        stored = dict(zip(col_names, row))

        assert stored["date"] == _DATE
        assert stored["total_active_ms"] == 180_000
        assert stored["total_idle_ms"] == 60_000
        assert stored["focus_session_count"] == 2
        assert stored["avg_focus_duration_ms"] == 90_000
        assert stored["top_category"] == "deep-work"
        assert json.loads(stored["category_breakdown"]) == {
            "deep-work": 120_000,
            "communication": 60_000,
        }
        assert stored["switch_count"] == 5
        assert stored["productivity_score_avg"] == pytest.approx(0.72)
        assert stored["top_daily_insight"] == summary.top_daily_insight

    def test_store_replaces_existing(self, db):
        s1 = DailySummary(date=_DATE, total_active_ms=100, total_idle_ms=0,
                          focus_session_count=0, avg_focus_duration_ms=0,
                          top_category="a")
        s2 = DailySummary(date=_DATE, total_active_ms=200, total_idle_ms=0,
                          focus_session_count=0, avg_focus_duration_ms=0,
                          top_category="b")

        store_daily_summary(db, s1)
        store_daily_summary(db, s2)

        row = db.connection.execute(
            "SELECT total_active_ms, top_category FROM daily_summaries WHERE date = ?",
            (_DATE,),
        ).fetchone()
        assert row[0] == 200
        assert row[1] == "b"
