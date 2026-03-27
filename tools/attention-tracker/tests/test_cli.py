"""Unit tests for the attention-tracker CLI.

Tests argument parsing, output formatting, and subcommand dispatch
with mocked database interactions.

Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 9.3
"""

from __future__ import annotations

import os
import sqlite3
import uuid
from datetime import date, datetime, timedelta
from unittest.mock import patch

import pytest

from attention_tracker.cli import (
    _resolve_date,
    build_parser,
    cmd_journal,
    cmd_sessions,
    cmd_status,
    cmd_today,
    cmd_unknowns,
    cmd_yesterday,
    main,
)
from attention_tracker.database import Database
from attention_tracker.models import TrackerConfig


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture()
def tmp_db(tmp_path):
    """Create a temporary database with schema and return (db, config)."""
    db_path = str(tmp_path / "test.db")
    db = Database(db_path)
    config = TrackerConfig(db_path=db_path)
    return db, config


def _insert_events(db: Database, date_str: str, count: int = 3,
                   category: str = "deep-work", score: float = 0.8) -> None:
    """Insert sample activity events for a given date."""
    conn = db.connection
    for i in range(count):
        conn.execute(
            "INSERT INTO activity_events "
            "(id, timestamp, app_name, window_class, window_title, "
            "idle_seconds, duration_ms, category, productivity_score, "
            "attention_mode, belief_focused, belief_switching, belief_idle) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                str(uuid.uuid4()),
                f"{date_str}T09:{i:02d}:00",
                "code",
                "Code",
                f"main.py - VSCode",
                0,
                600_000,  # 10 min each
                category,
                score,
                "FOCUSED",
                0.8, 0.1, 0.1,
            ),
        )
    conn.commit()


def _insert_uncategorized(db: Database, app_names: list[str]) -> None:
    """Insert uncategorized events for given app names."""
    conn = db.connection
    today = date.today().isoformat()
    for name in app_names:
        conn.execute(
            "INSERT INTO activity_events "
            "(id, timestamp, app_name, window_class, window_title, "
            "idle_seconds, duration_ms, category, attention_mode, "
            "belief_focused, belief_switching, belief_idle) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                str(uuid.uuid4()),
                f"{today}T10:00:00",
                name, name, name,
                0, 5000,
                "uncategorized",
                "SWITCHING",
                0.3, 0.5, 0.2,
            ),
        )
    conn.commit()


def _insert_sessions(db: Database, date_str: str, count: int = 2) -> None:
    """Insert sample focus sessions for a given date."""
    conn = db.connection
    for i in range(count):
        start_h = 9 + i * 2
        end_h = start_h + 1
        conn.execute(
            "INSERT INTO focus_sessions "
            "(id, start_time, end_time, category, total_duration_ms, "
            "interruption_count, app_sequence) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                str(uuid.uuid4()),
                f"{date_str}T{start_h:02d}:00:00",
                f"{date_str}T{end_h:02d}:00:00",
                "deep-work",
                3_600_000,  # 1 hour
                0,
                "[]",
            ),
        )
    conn.commit()


# ------------------------------------------------------------------
# _resolve_date
# ------------------------------------------------------------------

class TestResolveDate:
    def test_today(self):
        assert _resolve_date("today") == date.today().isoformat()

    def test_yesterday(self):
        expected = (date.today() - timedelta(days=1)).isoformat()
        assert _resolve_date("yesterday") == expected

    def test_explicit_date(self):
        assert _resolve_date("2026-01-15") == "2026-01-15"


# ------------------------------------------------------------------
# Argument parsing
# ------------------------------------------------------------------

class TestBuildParser:
    def test_today_command(self):
        parser = build_parser()
        args = parser.parse_args(["today"])
        assert args.command == "today"

    def test_yesterday_oneliner(self):
        parser = build_parser()
        args = parser.parse_args(["yesterday", "--oneliner"])
        assert args.command == "yesterday"
        assert args.oneliner is True

    def test_yesterday_default(self):
        parser = build_parser()
        args = parser.parse_args(["yesterday"])
        assert args.oneliner is False

    def test_sessions_default_date(self):
        parser = build_parser()
        args = parser.parse_args(["sessions"])
        assert args.date == "today"

    def test_sessions_custom_date(self):
        parser = build_parser()
        args = parser.parse_args(["sessions", "--date", "2026-03-15"])
        assert args.date == "2026-03-15"

    def test_rule_validate(self):
        parser = build_parser()
        args = parser.parse_args(["rule", "validate"])
        assert args.command == "rule"
        assert args.rule_command == "validate"

    def test_start_stop_status(self):
        parser = build_parser()
        for cmd in ("start", "stop", "status"):
            args = parser.parse_args([cmd])
            assert args.command == cmd


# ------------------------------------------------------------------
# cmd_today
# ------------------------------------------------------------------

class TestCmdToday:
    def test_displays_summary(self, tmp_db, capsys):
        db, config = tmp_db
        today = date.today().isoformat()
        _insert_events(db, today, count=3, category="deep-work", score=0.8)
        db.close()

        cmd_today(config)
        out = capsys.readouterr().out

        assert today in out
        assert "Active time:" in out
        assert "Focus sessions:" in out
        assert "Top category:" in out

    def test_empty_day(self, tmp_db, capsys):
        db, config = tmp_db
        db.close()

        cmd_today(config)
        out = capsys.readouterr().out

        assert "Active time:" in out
        assert "0m" in out


# ------------------------------------------------------------------
# cmd_yesterday
# ------------------------------------------------------------------

class TestCmdYesterday:
    def test_full_output(self, tmp_db, capsys):
        db, config = tmp_db
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        _insert_events(db, yesterday, count=2, category="communication")
        db.close()

        cmd_yesterday(config, oneliner=False)
        out = capsys.readouterr().out

        assert yesterday in out
        assert "Active time:" in out

    def test_oneliner_single_line(self, tmp_db, capsys):
        db, config = tmp_db
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        _insert_events(db, yesterday, count=2, category="deep-work")
        db.close()

        cmd_yesterday(config, oneliner=True)
        out = capsys.readouterr().out

        lines = out.strip().split("\n")
        assert len(lines) == 1
        assert "Yesterday:" in lines[0]
        assert "deep session" in lines[0]
        assert "context switch" in lines[0]


# ------------------------------------------------------------------
# cmd_journal
# ------------------------------------------------------------------

class TestCmdJournal:
    def test_generates_insight(self, tmp_db, capsys):
        db, config = tmp_db
        today = date.today().isoformat()
        _insert_events(db, today, count=2, category="deep-work", score=0.9)
        db.close()

        cmd_journal(config)
        out = capsys.readouterr().out.strip()

        # Should contain the insight format from generate_top_insight
        assert "focused on" in out
        assert "deep session" in out or "context switch" in out

    def test_returns_cached_insight(self, tmp_db, capsys):
        db, config = tmp_db
        today = date.today().isoformat()
        # Pre-insert a summary with insight
        db.connection.execute(
            "INSERT INTO daily_summaries (date, total_active_ms, total_idle_ms, "
            "focus_session_count, avg_focus_duration_ms, top_category, "
            "category_breakdown, switch_count, productivity_score_avg, "
            "top_daily_insight) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (today, 3600000, 0, 2, 1800000, "deep-work", "{}", 5, 0.85,
             "Cached insight text"),
        )
        db.connection.commit()
        db.close()

        cmd_journal(config)
        out = capsys.readouterr().out.strip()
        assert out == "Cached insight text"


# ------------------------------------------------------------------
# cmd_sessions
# ------------------------------------------------------------------

class TestCmdSessions:
    def test_lists_sessions(self, tmp_db, capsys):
        db, config = tmp_db
        today = date.today().isoformat()
        _insert_sessions(db, today, count=2)
        db.close()

        cmd_sessions(config, date_str="today")
        out = capsys.readouterr().out

        assert "Start" in out
        assert "Duration" in out
        assert "deep-work" in out
        assert "1h" in out  # 1 hour sessions

    def test_no_sessions(self, tmp_db, capsys):
        db, config = tmp_db
        db.close()

        cmd_sessions(config, date_str="today")
        out = capsys.readouterr().out
        assert "No focus sessions" in out

    def test_explicit_date(self, tmp_db, capsys):
        db, config = tmp_db
        _insert_sessions(db, "2026-03-15", count=1)
        db.close()

        cmd_sessions(config, date_str="2026-03-15")
        out = capsys.readouterr().out
        assert "deep-work" in out


# ------------------------------------------------------------------
# cmd_unknowns
# ------------------------------------------------------------------

class TestCmdUnknowns:
    def test_lists_uncategorized(self, tmp_db, capsys):
        db, config = tmp_db
        _insert_uncategorized(db, ["slack", "zoom", "mystery-app"])
        db.close()

        cmd_unknowns(config)
        out = capsys.readouterr().out

        assert "Uncategorized apps:" in out
        assert "mystery-app" in out
        assert "slack" in out
        assert "zoom" in out

    def test_no_unknowns(self, tmp_db, capsys):
        db, config = tmp_db
        db.close()

        cmd_unknowns(config)
        out = capsys.readouterr().out
        assert "No uncategorized apps found." in out

    def test_deduplicates(self, tmp_db, capsys):
        db, config = tmp_db
        # Insert same app name twice
        _insert_uncategorized(db, ["slack", "slack"])
        db.close()

        cmd_unknowns(config)
        out = capsys.readouterr().out
        assert out.count("slack") == 1  # DISTINCT


# ------------------------------------------------------------------
# cmd_status (no PID file)
# ------------------------------------------------------------------

class TestCmdStatus:
    def test_not_running(self, tmp_path, capsys, monkeypatch):
        fake_pid = str(tmp_path / "nonexistent.pid")
        monkeypatch.setattr("attention_tracker.cli.PID_FILE", fake_pid)

        cmd_status()
        out = capsys.readouterr().out
        assert "not running" in out


# ------------------------------------------------------------------
# main() integration
# ------------------------------------------------------------------

class TestMain:
    def test_no_command_shows_help(self, capsys):
        rc = main([])
        assert rc == 0

    def test_today_via_main(self, tmp_db, capsys):
        db, config = tmp_db
        today = date.today().isoformat()
        _insert_events(db, today)
        db.close()

        with patch("attention_tracker.cli.TrackerConfig", return_value=config):
            rc = main(["today"])
        assert rc == 0
        assert "Active time:" in capsys.readouterr().out

    def test_yesterday_oneliner_via_main(self, tmp_db, capsys):
        db, config = tmp_db
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        _insert_events(db, yesterday)
        db.close()

        with patch("attention_tracker.cli.TrackerConfig", return_value=config):
            rc = main(["yesterday", "--oneliner"])
        assert rc == 0
        out = capsys.readouterr().out
        lines = out.strip().split("\n")
        assert len(lines) == 1
        assert "Yesterday:" in lines[0]

    def test_unknowns_via_main(self, tmp_db, capsys):
        db, config = tmp_db
        _insert_uncategorized(db, ["unknown-app"])
        db.close()

        with patch("attention_tracker.cli.TrackerConfig", return_value=config):
            rc = main(["unknowns"])
        assert rc == 0
        assert "unknown-app" in capsys.readouterr().out
