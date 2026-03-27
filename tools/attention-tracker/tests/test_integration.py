"""Integration smoke test — full pipeline end-to-end.

Validates the complete chain:
  WindowInfo → EventProcessor → Classifier → StateMachine → EventStore → Database → CLI query

This is a simple wiring test, not an exhaustive property test.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from attention_tracker.cli import main as cli_main
from attention_tracker.database import Database
from attention_tracker.event_processor import EventProcessor
from attention_tracker.event_store import EventStore
from attention_tracker.models import (
    AttentionMode,
    ClassificationRule,
    MatchType,
    TrackerConfig,
    WindowInfo,
)
from attention_tracker.session_tracker import SessionTracker


# ------------------------------------------------------------------
# Shared helpers
# ------------------------------------------------------------------

RULES = [
    ClassificationRule(
        name="editor",
        match_type=MatchType.WINDOW_CLASS,
        pattern="Code|vim",
        category="deep-work",
        productivity_score=0.9,
        priority=10,
    ),
    ClassificationRule(
        name="chat",
        match_type=MatchType.WINDOW_CLASS,
        pattern="Slack|slack",
        category="communication",
        productivity_score=0.3,
        priority=5,
    ),
]


def _window(cls: str, title: str, ts: datetime) -> WindowInfo:
    return WindowInfo(pid=1000, window_class=cls, window_title=title, timestamp=ts)


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture()
def integration_env(tmp_path):
    """Set up a temp database, EventProcessor, and TrackerConfig wired together."""
    db_path = str(tmp_path / "integration.db")
    config = TrackerConfig(db_path=db_path)
    db = Database(db_path)
    store = EventStore(db)
    session_tracker = SessionTracker(store)
    processor = EventProcessor(
        config=config,
        classifier_rules=RULES,
        event_store=store,
        session_tracker=session_tracker,
    )
    yield db, config, processor
    db.close()


# ------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------

class TestFullPipeline:
    """Push mock WindowInfo events through the full pipeline and verify DB + CLI."""

    def test_events_stored_with_correct_fields(self, integration_env):
        db, config, processor = integration_env
        now = datetime(2026, 3, 27, 10, 0, 0, tzinfo=timezone.utc)

        # Process a few events
        processor.process(_window("Code", "main.py — Code", now), None, 0)
        processor.process(
            _window("Code", "utils.py — Code", now + timedelta(seconds=2)),
            None, 0,
        )
        processor.process(
            _window("Slack", "general — Slack", now + timedelta(seconds=4)),
            None, 0,
        )

        rows = db.connection.execute(
            "SELECT app_name, category, productivity_score, attention_mode, "
            "belief_focused, belief_switching, belief_idle "
            "FROM activity_events ORDER BY timestamp"
        ).fetchall()

        assert len(rows) == 3

        # First two events: editor → deep-work
        assert rows[0][0] == "Code"
        assert rows[0][1] == "deep-work"
        assert rows[0][2] == pytest.approx(0.9)
        assert rows[0][3] in ("FOCUSED", "SWITCHING", "IDLE")

        # Third event: Slack → communication
        assert rows[2][0] == "Slack"
        assert rows[2][1] == "communication"
        assert rows[2][2] == pytest.approx(0.3)

        # Beliefs should sum to ~1.0 for every row
        for row in rows:
            assert row[4] + row[5] + row[6] == pytest.approx(1.0, abs=0.01)

    def test_cli_today_reads_pipeline_data(self, integration_env, capsys):
        db, config, processor = integration_env
        today = datetime.now(timezone.utc).replace(
            hour=10, minute=0, second=0, microsecond=0
        )

        # Push events with today's date
        for i in range(5):
            processor.process(
                _window("Code", f"file{i}.py — Code", today + timedelta(seconds=i * 2)),
                None, 0,
            )

        # Run CLI `today` against the same DB
        with patch("attention_tracker.cli.TrackerConfig", return_value=config):
            rc = cli_main(["today"])

        assert rc == 0
        out = capsys.readouterr().out
        assert "Active time:" in out
        assert "Top category:" in out

    def test_cli_journal_produces_insight(self, integration_env, capsys):
        db, config, processor = integration_env
        today = datetime.now(timezone.utc).replace(
            hour=10, minute=0, second=0, microsecond=0
        )

        for i in range(3):
            processor.process(
                _window("Code", f"f{i}.py — Code", today + timedelta(seconds=i * 2)),
                None, 0,
            )

        with patch("attention_tracker.cli.TrackerConfig", return_value=config):
            rc = cli_main(["journal"])

        assert rc == 0
        out = capsys.readouterr().out.strip()
        # Insight should be a non-empty one-liner
        assert len(out) > 0
        assert "\n" not in out

    def test_cli_yesterday_oneliner(self, integration_env, capsys):
        db, config, processor = integration_env
        yesterday = (
            datetime.now(timezone.utc) - timedelta(days=1)
        ).replace(hour=10, minute=0, second=0, microsecond=0)

        for i in range(3):
            processor.process(
                _window("Code", f"f{i}.py — Code", yesterday + timedelta(seconds=i * 2)),
                None, 0,
            )

        with patch("attention_tracker.cli.TrackerConfig", return_value=config):
            rc = cli_main(["yesterday", "--oneliner"])

        assert rc == 0
        out = capsys.readouterr().out.strip()
        lines = out.split("\n")
        assert len(lines) == 1
        assert "Yesterday:" in lines[0]
