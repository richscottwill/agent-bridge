"""Tests for attention_tracker.database — schema, connection, and JSON1."""

import sqlite3

import pytest

from attention_tracker.database import Database


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

EXPECTED_TABLES = {"activity_events", "focus_sessions", "daily_summaries"}

EXPECTED_COLUMNS = {
    "activity_events": [
        "id", "timestamp", "app_name", "window_class", "window_title",
        "url", "idle_seconds", "duration_ms", "category",
        "productivity_score", "rule_name", "attention_mode",
        "belief_focused", "belief_switching", "belief_idle",
        "focus_session_id", "created_at",
    ],
    "focus_sessions": [
        "id", "start_time", "end_time", "category",
        "total_duration_ms", "interruption_count", "app_sequence",
        "created_at",
    ],
    "daily_summaries": [
        "date", "total_active_ms", "total_idle_ms",
        "focus_session_count", "avg_focus_duration_ms", "top_category",
        "category_breakdown", "switch_count", "productivity_score_avg",
        "top_daily_insight", "created_at",
    ],
}

EXPECTED_INDEXES = {
    "idx_events_timestamp",
    "idx_events_category",
    "idx_events_attention_mode",
    "idx_events_session",
    "idx_sessions_start",
    "idx_summaries_date",
}


def _table_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()
    return {r[0] for r in rows}


def _column_names(conn: sqlite3.Connection, table: str) -> list[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return [r[1] for r in rows]


def _index_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()
    return {r[0] for r in rows}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestDatabaseCreation:
    """Database file, tables, columns, and indexes are created correctly."""

    def test_creates_database_file(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        db = Database(db_path)
        assert (tmp_path / "test.db").exists()
        db.close()

    def test_creates_all_tables(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        with Database(db_path) as db:
            tables = _table_names(db.connection)
        assert tables == EXPECTED_TABLES

    def test_activity_events_columns(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        with Database(db_path) as db:
            cols = _column_names(db.connection, "activity_events")
        assert cols == EXPECTED_COLUMNS["activity_events"]

    def test_focus_sessions_columns(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        with Database(db_path) as db:
            cols = _column_names(db.connection, "focus_sessions")
        assert cols == EXPECTED_COLUMNS["focus_sessions"]

    def test_daily_summaries_columns(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        with Database(db_path) as db:
            cols = _column_names(db.connection, "daily_summaries")
        assert cols == EXPECTED_COLUMNS["daily_summaries"]

    def test_creates_all_indexes(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        with Database(db_path) as db:
            indexes = _index_names(db.connection)
        assert EXPECTED_INDEXES.issubset(indexes)


class TestJSON1:
    """JSON1 extension verification."""

    def test_json1_available(self, tmp_path):
        """Database opens successfully when JSON1 is present (default CPython)."""
        db_path = str(tmp_path / "test.db")
        with Database(db_path) as db:
            result = db.connection.execute("SELECT json('{}')").fetchone()
        assert result[0] == "{}"


class TestWALMode:
    """WAL journal mode is enabled."""

    def test_wal_mode_enabled(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        with Database(db_path) as db:
            mode = db.connection.execute("PRAGMA journal_mode").fetchone()[0]
        assert mode == "wal"


class TestContextManager:
    """Context manager protocol works correctly."""

    def test_context_manager_returns_database(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        with Database(db_path) as db:
            assert isinstance(db, Database)

    def test_connection_closed_after_exit(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        with Database(db_path) as db:
            conn = db.connection
        # After exiting, the connection object should be None
        assert db._conn is None


class TestExpandUser:
    """Tilde paths are expanded correctly."""

    def test_expands_tilde_in_path(self, tmp_path, monkeypatch):
        # Point ~ to tmp_path so we don't touch the real home dir
        monkeypatch.setenv("HOME", str(tmp_path))
        db = Database("~/subdir/test.db")
        assert db.db_path == str(tmp_path / "subdir" / "test.db")
        assert (tmp_path / "subdir" / "test.db").exists()
        db.close()


class TestIdempotentCreation:
    """Opening the same database twice doesn't fail or duplicate tables."""

    def test_open_twice_is_safe(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        db1 = Database(db_path)
        db1.close()
        db2 = Database(db_path)
        tables = _table_names(db2.connection)
        assert tables == EXPECTED_TABLES
        db2.close()
