"""Tests for attention_tracker.session_tracker — Focus Session lifecycle."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta

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
from attention_tracker.session_tracker import SessionTracker


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_event(
    app_name: str = "code",
    category: str = "deep-work",
    ts: datetime | None = None,
    duration_ms: int = 1500,
) -> ClassifiedEvent:
    ts = ts or datetime(2026, 3, 27, 10, 0, 0)
    return ClassifiedEvent(
        event=ActivityEvent(
            id=str(uuid.uuid4()),
            timestamp=ts,
            app_name=app_name,
            window_class="Code",
            window_title=f"{app_name} — window",
            idle_seconds=0,
            duration_ms=duration_ms,
            url=None,
        ),
        category=category,
        productivity_score=0.9,
        rule_name="test-rule",
    )


def _make_state(
    mode: AttentionMode = AttentionMode.FOCUSED,
    focus_duration_ms: int = 30000,
) -> AttentionState:
    return AttentionState(
        beliefs=AttentionBeliefs(focused=0.80, switching=0.10, idle=0.10),
        inferred_mode=mode,
        since=datetime(2026, 3, 27, 9, 55, 0),
        current_category="deep-work",
        focus_duration_ms=focus_duration_ms,
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db(tmp_path):
    db_path = str(tmp_path / "test_session.db")
    _db = Database(db_path)
    yield _db
    _db.close()


@pytest.fixture
def store(db):
    return EventStore(db)


@pytest.fixture
def tracker(store):
    return SessionTracker(store)


# ---------------------------------------------------------------------------
# Session starts on transition to FOCUSED
# ---------------------------------------------------------------------------

class TestSessionStart:
    def test_creates_session_on_transition_to_focused(self, tracker):
        event = _make_event(ts=datetime(2026, 3, 27, 10, 0, 0))
        result = tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.FOCUSED,
            _make_state(), event,
        )

        assert result is None  # no completed session returned
        assert tracker.current_session is not None
        assert tracker.current_session.start_time == datetime(2026, 3, 27, 10, 0, 0)
        assert tracker.current_session.category == "deep-work"
        assert tracker.current_session.app_sequence == ["code"]

    def test_creates_session_from_idle_to_focused(self, tracker):
        event = _make_event(app_name="vim", category="deep-work")
        tracker.process_transition(
            AttentionMode.IDLE, AttentionMode.FOCUSED,
            _make_state(), event,
        )

        assert tracker.current_session is not None
        assert tracker.current_session.app_sequence == ["vim"]

    def test_session_has_uuid_id(self, tracker):
        event = _make_event()
        tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.FOCUSED,
            _make_state(), event,
        )

        # Should be a valid UUID
        uuid.UUID(tracker.current_session.id)

    def test_session_starts_with_zero_interruptions(self, tracker):
        event = _make_event()
        tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.FOCUSED,
            _make_state(), event,
        )

        assert tracker.current_session.interruption_count == 0


# ---------------------------------------------------------------------------
# Session closes on transition away from FOCUSED
# ---------------------------------------------------------------------------

class TestSessionClose:
    def test_closes_session_on_transition_away(self, tracker):
        start_ts = datetime(2026, 3, 27, 10, 0, 0)
        end_ts = datetime(2026, 3, 27, 10, 30, 0)

        # Start session
        tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.FOCUSED,
            _make_state(), _make_event(ts=start_ts),
        )

        # Close session
        completed = tracker.process_transition(
            AttentionMode.FOCUSED, AttentionMode.SWITCHING,
            _make_state(mode=AttentionMode.SWITCHING), _make_event(ts=end_ts),
        )

        assert completed is not None
        assert completed.start_time == start_ts
        assert completed.end_time == end_ts
        assert completed.total_duration_ms == 30 * 60 * 1000  # 30 minutes

    def test_current_session_is_none_after_close(self, tracker):
        tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.FOCUSED,
            _make_state(), _make_event(ts=datetime(2026, 3, 27, 10, 0, 0)),
        )
        tracker.process_transition(
            AttentionMode.FOCUSED, AttentionMode.IDLE,
            _make_state(mode=AttentionMode.IDLE),
            _make_event(ts=datetime(2026, 3, 27, 10, 15, 0)),
        )

        assert tracker.current_session is None
        assert tracker.current_session_id is None

    def test_closed_session_persisted_to_store(self, tracker, db):
        start_ts = datetime(2026, 3, 27, 10, 0, 0)
        end_ts = datetime(2026, 3, 27, 10, 45, 0)

        tracker.process_transition(
            AttentionMode.IDLE, AttentionMode.FOCUSED,
            _make_state(), _make_event(ts=start_ts),
        )
        completed = tracker.process_transition(
            AttentionMode.FOCUSED, AttentionMode.SWITCHING,
            _make_state(mode=AttentionMode.SWITCHING), _make_event(ts=end_ts),
        )

        # Verify it was written to the database
        db.connection.row_factory = None
        row = db.connection.execute(
            "SELECT * FROM focus_sessions WHERE id = ?", (completed.id,)
        ).fetchone()
        assert row is not None

    def test_start_time_strictly_less_than_end_time(self, tracker):
        start_ts = datetime(2026, 3, 27, 10, 0, 0)
        end_ts = datetime(2026, 3, 27, 10, 0, 1)

        tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.FOCUSED,
            _make_state(), _make_event(ts=start_ts),
        )
        completed = tracker.process_transition(
            AttentionMode.FOCUSED, AttentionMode.IDLE,
            _make_state(mode=AttentionMode.IDLE), _make_event(ts=end_ts),
        )

        assert completed.start_time < completed.end_time


# ---------------------------------------------------------------------------
# App sequence tracking (deduped)
# ---------------------------------------------------------------------------

class TestAppSequence:
    def test_deduplicates_consecutive_same_app(self, tracker):
        tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.FOCUSED,
            _make_state(), _make_event(app_name="code", ts=datetime(2026, 3, 27, 10, 0, 0)),
        )

        # Same app again — should NOT be added
        tracker.process_transition(
            AttentionMode.FOCUSED, AttentionMode.FOCUSED,
            _make_state(), _make_event(app_name="code", ts=datetime(2026, 3, 27, 10, 0, 2)),
        )

        assert tracker.current_session.app_sequence == ["code"]

    def test_adds_different_app_to_sequence(self, tracker):
        tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.FOCUSED,
            _make_state(), _make_event(app_name="code", ts=datetime(2026, 3, 27, 10, 0, 0)),
        )

        tracker.process_transition(
            AttentionMode.FOCUSED, AttentionMode.FOCUSED,
            _make_state(), _make_event(app_name="terminal", ts=datetime(2026, 3, 27, 10, 0, 2)),
        )

        tracker.process_transition(
            AttentionMode.FOCUSED, AttentionMode.FOCUSED,
            _make_state(), _make_event(app_name="code", ts=datetime(2026, 3, 27, 10, 0, 4)),
        )

        assert tracker.current_session.app_sequence == ["code", "terminal", "code"]


# ---------------------------------------------------------------------------
# current_session_id property
# ---------------------------------------------------------------------------

class TestCurrentSessionId:
    def test_returns_id_during_focus(self, tracker):
        tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.FOCUSED,
            _make_state(), _make_event(),
        )

        assert tracker.current_session_id is not None
        assert tracker.current_session_id == tracker.current_session.id

    def test_returns_none_when_not_focused(self, tracker):
        assert tracker.current_session_id is None

    def test_returns_none_after_session_closes(self, tracker):
        tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.FOCUSED,
            _make_state(), _make_event(ts=datetime(2026, 3, 27, 10, 0, 0)),
        )
        tracker.process_transition(
            AttentionMode.FOCUSED, AttentionMode.IDLE,
            _make_state(mode=AttentionMode.IDLE),
            _make_event(ts=datetime(2026, 3, 27, 10, 5, 0)),
        )

        assert tracker.current_session_id is None


# ---------------------------------------------------------------------------
# No session for non-FOCUSED transitions
# ---------------------------------------------------------------------------

class TestNonFocusedTransitions:
    def test_no_session_for_switching_to_idle(self, tracker):
        result = tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.IDLE,
            _make_state(mode=AttentionMode.IDLE), _make_event(),
        )

        assert result is None
        assert tracker.current_session is None

    def test_no_session_for_idle_to_switching(self, tracker):
        result = tracker.process_transition(
            AttentionMode.IDLE, AttentionMode.SWITCHING,
            _make_state(mode=AttentionMode.SWITCHING), _make_event(),
        )

        assert result is None
        assert tracker.current_session is None

    def test_no_session_for_switching_to_switching(self, tracker):
        result = tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.SWITCHING,
            _make_state(mode=AttentionMode.SWITCHING), _make_event(),
        )

        assert result is None
        assert tracker.current_session is None


# ---------------------------------------------------------------------------
# Interruption tracking
# ---------------------------------------------------------------------------

class TestInterruptionTracking:
    def test_increments_interruption_on_focus_duration_reset(self, tracker):
        tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.FOCUSED,
            _make_state(), _make_event(ts=datetime(2026, 3, 27, 10, 0, 0)),
        )

        # Simulate focus_duration_ms resetting to 0 while still FOCUSED
        tracker.process_transition(
            AttentionMode.FOCUSED, AttentionMode.FOCUSED,
            _make_state(focus_duration_ms=0),
            _make_event(ts=datetime(2026, 3, 27, 10, 1, 0)),
        )

        assert tracker.current_session.interruption_count == 1

    def test_no_interruption_when_focus_duration_positive(self, tracker):
        tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.FOCUSED,
            _make_state(), _make_event(ts=datetime(2026, 3, 27, 10, 0, 0)),
        )

        tracker.process_transition(
            AttentionMode.FOCUSED, AttentionMode.FOCUSED,
            _make_state(focus_duration_ms=5000),
            _make_event(ts=datetime(2026, 3, 27, 10, 1, 0)),
        )

        assert tracker.current_session.interruption_count == 0

    def test_multiple_interruptions_accumulate(self, tracker):
        tracker.process_transition(
            AttentionMode.SWITCHING, AttentionMode.FOCUSED,
            _make_state(), _make_event(ts=datetime(2026, 3, 27, 10, 0, 0)),
        )

        for i in range(3):
            tracker.process_transition(
                AttentionMode.FOCUSED, AttentionMode.FOCUSED,
                _make_state(focus_duration_ms=0),
                _make_event(ts=datetime(2026, 3, 27, 10, i + 1, 0)),
            )

        assert tracker.current_session.interruption_count == 3
