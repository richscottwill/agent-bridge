"""SQLite database schema and connection manager for the Attention Tracker."""

from __future__ import annotations

import os
import sqlite3


_SCHEMA_SQL = """\
CREATE TABLE IF NOT EXISTS activity_events (
  id TEXT PRIMARY KEY,
  timestamp TEXT NOT NULL,
  app_name TEXT NOT NULL,
  window_class TEXT,
  window_title TEXT,
  url TEXT,
  idle_seconds INTEGER,
  duration_ms INTEGER,
  category TEXT,
  productivity_score REAL,
  rule_name TEXT,
  attention_mode TEXT,
  belief_focused REAL,
  belief_switching REAL,
  belief_idle REAL,
  focus_session_id TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS focus_sessions (
  id TEXT PRIMARY KEY,
  start_time TEXT NOT NULL,
  end_time TEXT,
  category TEXT NOT NULL,
  total_duration_ms INTEGER,
  interruption_count INTEGER,
  app_sequence TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS daily_summaries (
  date TEXT PRIMARY KEY,
  total_active_ms INTEGER,
  total_idle_ms INTEGER,
  focus_session_count INTEGER,
  avg_focus_duration_ms INTEGER,
  top_category TEXT,
  category_breakdown TEXT,
  switch_count INTEGER,
  productivity_score_avg REAL,
  top_daily_insight TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_events_timestamp ON activity_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_category ON activity_events(category);
CREATE INDEX IF NOT EXISTS idx_events_attention_mode ON activity_events(attention_mode);
CREATE INDEX IF NOT EXISTS idx_events_session ON activity_events(focus_session_id);
CREATE INDEX IF NOT EXISTS idx_sessions_start ON focus_sessions(start_time);
CREATE INDEX IF NOT EXISTS idx_summaries_date ON daily_summaries(date);
"""


class Database:
    """SQLite database manager for the Attention Tracker.

    Opens (or creates) the database at *db_path*, enables WAL mode,
    verifies the JSON1 extension is available, and creates all tables
    and indexes on first use.

    Supports the context-manager protocol::

        with Database(path) as db:
            ...
    """

    def __init__(self, db_path: str) -> None:
        self.db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._verify_json1()
        self._create_tables()

    # -- context manager ------------------------------------------------

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        self.close()

    # -- public ---------------------------------------------------------

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        if self._conn:
            self._conn.close()
            self._conn = None  # type: ignore[assignment]

    @property
    def connection(self) -> sqlite3.Connection:
        """Return the raw SQLite connection."""
        return self._conn

    # -- private --------------------------------------------------------

    def _verify_json1(self) -> None:
        """Raise RuntimeError if the JSON1 extension is not available."""
        try:
            self._conn.execute("SELECT json('{}')").fetchone()
        except sqlite3.OperationalError as exc:
            raise RuntimeError(
                "SQLite JSON1 extension is required but not available"
            ) from exc

    def _create_tables(self) -> None:
        """Create all tables and indexes if they don't already exist."""
        self._conn.executescript(_SCHEMA_SQL)
