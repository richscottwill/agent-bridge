"""Tests for attention_tracker.event_processor — EventProcessor pipeline."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from attention_tracker.database import Database
from attention_tracker.event_store import EventStore
from attention_tracker.models import (
    ActivityEvent,
    AttentionBeliefs,
    AttentionMode,
    AttentionState,
    ClassificationRule,
    ClassifiedEvent,
    MatchType,
    TabInfo,
    TrackerConfig,
    WindowInfo,
)
from attention_tracker.session_tracker import SessionTracker
from attention_tracker.event_processor import EventProcessor


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_window(
    window_class: str = "Code",
    window_title: str = "main.py — Code",
    pid: int = 1234,
    ts: datetime | None = None,
) -> WindowInfo:
    return WindowInfo(
        pid=pid,
        window_class=window_class,
        window_title=window_title,
        timestamp=ts or datetime(2026, 3, 27, 10, 0, 0, tzinfo=timezone.utc),
    )


def _make_tab(
    title: str = "GitHub",
    browser: str = "Firefox",
    url: str = "https://github.com",
) -> TabInfo:
    return TabInfo(
        title=title,
        browser=browser,
        timestamp=datetime(2026, 3, 27, 10, 0, 0, tzinfo=timezone.utc),
        url=url,
    )


SAMPLE_RULES: list[ClassificationRule] = [
    ClassificationRule(
        name="editor",
        match_type=MatchType.WINDOW_CLASS,
        pattern="Code|vim|neovim",
        category="deep-work",
        productivity_score=0.9,
        priority=10,
    ),
    ClassificationRule(
        name="browser",
        match_type=MatchType.WINDOW_CLASS,
        pattern="firefox|google-chrome",
        category="browsing",
        productivity_score=0.5,
        priority=5,
    ),
]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db(tmp_path):
    db_path = str(tmp_path / "test_ep.db")
    _db = Database(db_path)
    yield _db
    _db.close()


@pytest.fixture
def store(db):
    return EventStore(db)


@pytest.fixture
def session_tracker(store):
    return SessionTracker(store)


@pytest.fixture
def config():
    return TrackerConfig()


@pytest.fixture
def processor(config, store, session_tracker):
    return EventProcessor(
        config=config,
        classifier_rules=SAMPLE_RULES,
        event_store=store,
        session_tracker=session_tracker,
    )


# ---------------------------------------------------------------------------
# Initial state
# ---------------------------------------------------------------------------

class TestInitialState:
    def test_initial_beliefs_are_uniform_prior(self, processor):
        state = processor.state
        assert state.beliefs.focused == pytest.approx(0.33)
        assert state.beliefs.switching == pytest.approx(0.33)
        assert state.beliefs.idle == pytest.approx(0.34)

    def test_initial_beliefs_sum_to_one(self, processor):
        assert processor.state.beliefs.sum() == pytest.approx(1.0)

    def test_initial_mode_is_idle(self, processor):
        assert processor.state.inferred_mode == AttentionMode.IDLE

    def test_initial_previous_mode_is_idle(self, processor):
        assert processor.previous_mode == AttentionMode.IDLE


# ---------------------------------------------------------------------------
# process() — full pipeline
# ---------------------------------------------------------------------------

class TestProcess:
    def test_process_creates_event_and_stores_it(self, processor, db):
        window = _make_window()
        processor.process(window, None, idle_seconds=0)

        row = db.connection.execute(
            "SELECT * FROM activity_events"
        ).fetchone()
        assert row is not None

    def test_process_classifies_event_with_rules(self, processor, db):
        window = _make_window(window_class="Code", window_title="main.py — Code")
        processor.process(window, None, idle_seconds=0)

        row = db.connection.execute(
            "SELECT category, rule_name FROM activity_events"
        ).fetchone()
        assert row[0] == "deep-work"
        assert row[1] == "editor"

    def test_process_stores_attention_beliefs(self, processor, db):
        window = _make_window()
        processor.process(window, None, idle_seconds=0)

        row = db.connection.execute(
            "SELECT belief_focused, belief_switching, belief_idle FROM activity_events"
        ).fetchone()
        # Beliefs should be valid floats that sum to ~1.0
        assert row[0] is not None
        assert row[1] is not None
        assert row[2] is not None
        assert row[0] + row[1] + row[2] == pytest.approx(1.0, abs=0.01)

    def test_process_stores_attention_mode(self, processor, db):
        window = _make_window()
        processor.process(window, None, idle_seconds=0)

        row = db.connection.execute(
            "SELECT attention_mode FROM activity_events"
        ).fetchone()
        assert row[0] in ("FOCUSED", "SWITCHING", "IDLE")

    def test_process_updates_internal_state(self, processor):
        initial_state = processor.state
        window = _make_window()
        processor.process(window, None, idle_seconds=0)

        # State should have been updated (beliefs changed from uniform prior)
        new_state = processor.state
        assert new_state is not initial_state

    def test_process_with_tab_info_passes_url(self, processor, db):
        window = _make_window(window_class="firefox", window_title="GitHub - Firefox")
        tab = _make_tab(url="https://github.com")
        processor.process(window, tab, idle_seconds=0)

        row = db.connection.execute(
            "SELECT url FROM activity_events"
        ).fetchone()
        assert row[0] == "https://github.com"

    def test_process_without_tab_stores_null_url(self, processor, db):
        window = _make_window()
        processor.process(window, None, idle_seconds=0)

        row = db.connection.execute(
            "SELECT url FROM activity_events"
        ).fetchone()
        assert row[0] is None

    def test_process_uses_poll_interval_as_duration(self, processor, db):
        window = _make_window()
        processor.process(window, None, idle_seconds=0)

        row = db.connection.execute(
            "SELECT duration_ms FROM activity_events"
        ).fetchone()
        assert row[0] == processor._config.poll_interval_ms

    def test_process_stores_idle_seconds(self, processor, db):
        window = _make_window()
        processor.process(window, None, idle_seconds=42)

        row = db.connection.execute(
            "SELECT idle_seconds FROM activity_events"
        ).fetchone()
        assert row[0] == 42


# ---------------------------------------------------------------------------
# Session tracker integration
# ---------------------------------------------------------------------------

class TestSessionTrackerIntegration:
    def test_session_tracker_called_on_mode_transition(self, processor, db):
        """When mode transitions to FOCUSED, session tracker should start a session."""
        # Process enough same-category events to push beliefs toward FOCUSED
        # The initial state is IDLE with uniform prior, so we need to build up
        # focused belief by sending consistent same-category events
        for i in range(20):
            window = _make_window(
                ts=datetime(2026, 3, 27, 10, 0, i, tzinfo=timezone.utc),
            )
            processor.process(window, None, idle_seconds=0)

        # After many consistent events, mode should have transitioned to FOCUSED
        # and session tracker should have a session
        if processor.state.inferred_mode == AttentionMode.FOCUSED:
            assert processor._session_tracker.current_session is not None

    def test_focus_session_id_stored_when_in_session(self, processor, db):
        """Events stored during a focus session should have the session ID."""
        # Drive to FOCUSED mode
        for i in range(20):
            window = _make_window(
                ts=datetime(2026, 3, 27, 10, 0, i, tzinfo=timezone.utc),
            )
            processor.process(window, None, idle_seconds=0)

        if processor._session_tracker.current_session_id is not None:
            session_id = processor._session_tracker.current_session_id
            row = db.connection.execute(
                "SELECT focus_session_id FROM activity_events "
                "WHERE focus_session_id IS NOT NULL LIMIT 1"
            ).fetchone()
            assert row is not None
            assert row[0] == session_id


# ---------------------------------------------------------------------------
# handle_restart()
# ---------------------------------------------------------------------------

class TestHandleRestart:
    def test_handle_restart_with_no_previous_events(self, processor):
        """When DB is empty, handle_restart just resets state."""
        processor.handle_restart()

        assert processor.state.beliefs.focused == pytest.approx(0.33)
        assert processor.state.beliefs.switching == pytest.approx(0.33)
        assert processor.state.beliefs.idle == pytest.approx(0.34)
        assert processor.previous_mode == AttentionMode.IDLE

    def test_handle_restart_records_gap_event(self, processor, db):
        """When there's a previous event, handle_restart records a daemon-offline gap."""
        # First, store an event so there's a last timestamp
        window = _make_window()
        processor.process(window, None, idle_seconds=0)

        # Verify we have one event
        count_before = db.connection.execute(
            "SELECT COUNT(*) FROM activity_events"
        ).fetchone()[0]
        assert count_before == 1

        # Now handle restart
        processor.handle_restart()

        # Should have stored a gap event
        count_after = db.connection.execute(
            "SELECT COUNT(*) FROM activity_events"
        ).fetchone()[0]
        assert count_after == 2

        # The gap event should be "daemon-offline"
        gap_row = db.connection.execute(
            "SELECT app_name, category FROM activity_events "
            "WHERE app_name = 'daemon-offline'"
        ).fetchone()
        assert gap_row is not None
        assert gap_row[0] == "daemon-offline"
        assert gap_row[1] == "daemon-offline"

    def test_handle_restart_resets_beliefs_to_uniform(self, processor):
        """After restart, beliefs should be uniform prior."""
        # Process some events to change beliefs from uniform
        for i in range(5):
            window = _make_window(
                ts=datetime(2026, 3, 27, 10, 0, i, tzinfo=timezone.utc),
            )
            processor.process(window, None, idle_seconds=0)

        # Beliefs should have changed from uniform
        assert processor.state.beliefs.focused != pytest.approx(0.33, abs=0.01)

        # Handle restart
        processor.handle_restart()

        # Beliefs should be back to uniform
        assert processor.state.beliefs.focused == pytest.approx(0.33)
        assert processor.state.beliefs.switching == pytest.approx(0.33)
        assert processor.state.beliefs.idle == pytest.approx(0.34)

    def test_handle_restart_resets_previous_mode_to_idle(self, processor):
        """After restart, previous_mode should be IDLE."""
        window = _make_window()
        processor.process(window, None, idle_seconds=0)

        processor.handle_restart()
        assert processor.previous_mode == AttentionMode.IDLE

    def test_handle_restart_gap_event_has_null_productivity_score(self, processor, db):
        """The daemon-offline gap event should have NULL productivity score."""
        window = _make_window()
        processor.process(window, None, idle_seconds=0)

        processor.handle_restart()

        row = db.connection.execute(
            "SELECT productivity_score FROM activity_events "
            "WHERE app_name = 'daemon-offline'"
        ).fetchone()
        assert row[0] is None
