"""Tests for attention_tracker.event_store — storage, buffering, and recovery."""

from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime
from unittest.mock import patch

import pytest

from attention_tracker.database import Database
from attention_tracker.event_store import EventStore
from attention_tracker.models import (
    ActivityEvent,
    AttentionBeliefs,
    AttentionMode,
    AttentionState,
    ClassifiedEvent,
    FocusSession,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_classified(
    category: str = "deep-work",
    score: float = 0.9,
    ts: datetime | None = None,
    event_id: str | None = None,
) -> ClassifiedEvent:
    ts = ts or datetime(2026, 3, 27, 10, 0, 0)
    return ClassifiedEvent(
        event=ActivityEvent(
            id=event_id or str(uuid.uuid4()),
            timestamp=ts,
            app_name="code",
            window_class="Code",
            window_title="main.py — VS Code",
            idle_seconds=0,
            duration_ms=1500,
            url=None,
        ),
        category=category,
        productivity_score=score,
        rule_name="vscode-rule",
    )


def _make_attention_state() -> AttentionState:
    return AttentionState(
        beliefs=AttentionBeliefs(focused=0.80, switching=0.10, idle=0.10),
        inferred_mode=AttentionMode.FOCUSED,
        since=datetime(2026, 3, 27, 9, 55, 0),
        current_category="deep-work",
        focus_duration_ms=30000,
    )


def _make_focus_session() -> FocusSession:
    return FocusSession(
        id=str(uuid.uuid4()),
        start_time=datetime(2026, 3, 27, 9, 0, 0),
        category="deep-work",
        total_duration_ms=3600000,
        interruption_count=2,
        app_sequence=["code", "terminal", "code"],
        end_time=datetime(2026, 3, 27, 10, 0, 0),
    )


def _read_event(conn: sqlite3.Connection, event_id: str) -> sqlite3.Row | None:
    conn.row_factory = sqlite3.Row
    return conn.execute(
        "SELECT * FROM activity_events WHERE id = ?", (event_id,)
    ).fetchone()


def _read_session(conn: sqlite3.Connection, session_id: str) -> sqlite3.Row | None:
    conn.row_factory = sqlite3.Row
    return conn.execute(
        "SELECT * FROM focus_sessions WHERE id = ?", (session_id,)
    ).fetchone()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db(tmp_path):
    """Fresh in-memory-like Database backed by a temp file."""
    db_path = str(tmp_path / "test.db")
    _db = Database(db_path)
    yield _db
    _db.close()


@pytest.fixture
def store(db):
    return EventStore(db)


# ---------------------------------------------------------------------------
# Successful event storage and retrieval
# ---------------------------------------------------------------------------

class TestStoreEvent:
    def test_stores_event_successfully(self, store, db):
        classified = _make_classified(event_id="evt-1")
        state = _make_attention_state()

        result = store.store_event(classified, state)

        assert result is True
        row = _read_event(db.connection, "evt-1")
        assert row is not None
        assert row["app_name"] == "code"
        assert row["category"] == "deep-work"
        assert row["productivity_score"] == 0.9
        assert row["attention_mode"] == "FOCUSED"
        assert row["belief_focused"] == pytest.approx(0.80)
        assert row["belief_switching"] == pytest.approx(0.10)
        assert row["belief_idle"] == pytest.approx(0.10)
        assert row["window_class"] == "Code"
        assert row["window_title"] == "main.py — VS Code"
        assert row["idle_seconds"] == 0
        assert row["duration_ms"] == 1500
        assert row["rule_name"] == "vscode-rule"
        assert row["focus_session_id"] is None

    def test_stores_event_with_none_score(self, store, db):
        classified = _make_classified(
            category="uncategorized", score=None, event_id="evt-none"
        )
        state = _make_attention_state()

        store.store_event(classified, state)

        row = _read_event(db.connection, "evt-none")
        assert row["productivity_score"] is None
        assert row["category"] == "uncategorized"

    def test_returns_true_on_success(self, store):
        assert store.store_event(_make_classified(), _make_attention_state()) is True


# ---------------------------------------------------------------------------
# Buffer fills on write failure
# ---------------------------------------------------------------------------

class TestBufferOnFailure:
    def test_buffers_event_on_write_failure(self, store, db):
        # Close the connection to force write failures
        db.connection.close()

        classified = _make_classified(event_id="evt-fail")
        state = _make_attention_state()

        result = store.store_event(classified, state)

        assert result is False
        assert store.buffer_size == 1

    def test_returns_false_on_failure(self, store, db):
        db.connection.close()
        result = store.store_event(_make_classified(), _make_attention_state())
        assert result is False

    def test_backoff_increases_on_repeated_failures(self, store, db):
        db.connection.close()

        store.store_event(_make_classified(), _make_attention_state())
        assert store.current_backoff == 1.0

        store.store_event(_make_classified(), _make_attention_state())
        assert store.current_backoff == 2.0

        store.store_event(_make_classified(), _make_attention_state())
        assert store.current_backoff == 4.0

    def test_backoff_caps_at_30_seconds(self, store, db):
        db.connection.close()

        # Drive backoff past 30s: 1, 2, 4, 8, 16, 32→30
        for _ in range(6):
            store.store_event(_make_classified(), _make_attention_state())

        assert store.current_backoff == 30.0


# ---------------------------------------------------------------------------
# Buffer drops oldest when full
# ---------------------------------------------------------------------------

class TestBufferDropsOldest:
    def test_drops_oldest_when_buffer_full(self, db):
        db.connection.close()
        store = EventStore(db, max_buffer=5)

        # Fill the buffer with 5 events
        for i in range(5):
            store.store_event(
                _make_classified(event_id=f"evt-{i}"), _make_attention_state()
            )
        assert store.buffer_size == 5

        # Adding one more should drop the oldest
        store.store_event(
            _make_classified(event_id="evt-new"), _make_attention_state()
        )
        assert store.buffer_size == 5

        # The buffer should contain evt-1 through evt-4 and evt-new
        # (evt-0 was dropped)
        ids = [row.params["id"] for row in store._buffer]
        assert "evt-0" not in ids
        assert "evt-new" in ids


# ---------------------------------------------------------------------------
# Flush empties buffer on recovery
# ---------------------------------------------------------------------------

class TestFlushBuffer:
    def test_flush_writes_buffered_events(self, tmp_path):
        db_path = str(tmp_path / "flush.db")
        db = Database(db_path)
        store = EventStore(db)

        # Simulate failure by closing, buffering, then reopening
        original_conn = db.connection
        db._conn = sqlite3.connect(":memory:")  # broken — no tables

        classified = _make_classified(event_id="evt-buffered")
        state = _make_attention_state()
        store.store_event(classified, state)
        assert store.buffer_size == 1

        # Restore the real connection
        db._conn = original_conn

        flushed = store.flush_buffer()
        assert flushed == 1
        assert store.buffer_size == 0

        row = _read_event(db.connection, "evt-buffered")
        assert row is not None
        assert row["app_name"] == "code"
        db.close()

    def test_flush_returns_zero_when_empty(self, store):
        assert store.flush_buffer() == 0

    def test_successful_write_triggers_flush(self, tmp_path):
        db_path = str(tmp_path / "autoflush.db")
        db = Database(db_path)
        store = EventStore(db)

        # Buffer an event by breaking the connection temporarily
        original_conn = db.connection
        db._conn = sqlite3.connect(":memory:")

        store.store_event(
            _make_classified(event_id="evt-buf"), _make_attention_state()
        )
        assert store.buffer_size == 1

        # Restore and write a new event — should auto-flush the buffer
        db._conn = original_conn
        store.store_event(
            _make_classified(event_id="evt-new"), _make_attention_state()
        )

        assert store.buffer_size == 0
        assert _read_event(db.connection, "evt-buf") is not None
        assert _read_event(db.connection, "evt-new") is not None
        db.close()


# ---------------------------------------------------------------------------
# get_last_event_timestamp
# ---------------------------------------------------------------------------

class TestGetLastEventTimestamp:
    def test_returns_none_when_empty(self, store):
        assert store.get_last_event_timestamp() is None

    def test_returns_latest_timestamp(self, store):
        ts1 = datetime(2026, 3, 27, 9, 0, 0)
        ts2 = datetime(2026, 3, 27, 10, 0, 0)

        store.store_event(_make_classified(ts=ts1, event_id="e1"), _make_attention_state())
        store.store_event(_make_classified(ts=ts2, event_id="e2"), _make_attention_state())

        result = store.get_last_event_timestamp()
        assert result == ts2.isoformat()

    def test_returns_none_on_db_error(self, store, db):
        db.connection.close()
        assert store.get_last_event_timestamp() is None


# ---------------------------------------------------------------------------
# Focus session storage
# ---------------------------------------------------------------------------

class TestStoreFocusSession:
    def test_stores_session_successfully(self, store, db):
        session = _make_focus_session()

        result = store.store_focus_session(session)

        assert result is True
        row = _read_session(db.connection, session.id)
        assert row is not None
        assert row["category"] == "deep-work"
        assert row["total_duration_ms"] == 3600000
        assert row["interruption_count"] == 2
        assert row["app_sequence"] == '["code", "terminal", "code"]'

    def test_stores_session_without_end_time(self, store, db):
        session = FocusSession(
            id="sess-open",
            start_time=datetime(2026, 3, 27, 9, 0, 0),
            category="deep-work",
        )

        store.store_focus_session(session)

        row = _read_session(db.connection, "sess-open")
        assert row is not None
        assert row["end_time"] is None

    def test_buffers_session_on_failure(self, store, db):
        db.connection.close()
        session = _make_focus_session()

        result = store.store_focus_session(session)

        assert result is False
        assert store.buffer_size == 1
