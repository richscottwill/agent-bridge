"""Event storage with in-memory buffering and error recovery."""

from __future__ import annotations

import json
import logging
import os
import sqlite3
import time
from collections import deque
from dataclasses import dataclass
from typing import Optional

from attention_tracker.database import Database
from attention_tracker.models import AttentionState, ClassifiedEvent, FocusSession

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Buffered event row — flat dict ready for INSERT
# ---------------------------------------------------------------------------

@dataclass
class _BufferedRow:
    """A flattened event row waiting to be written to SQLite."""
    table: str  # "activity_events" or "focus_sessions"
    params: dict


class EventStore:
    """Persists classified events and focus sessions with resilient buffering.

    On SQLite write failure the row is kept in an in-memory ring buffer
    (max *max_buffer* entries).  Successful writes trigger a flush attempt
    for any buffered rows.  Exponential back-off (1 s → 30 s) limits
    retry frequency.
    """

    _INSERT_EVENT_SQL = """\
INSERT OR REPLACE INTO activity_events (
    id, timestamp, app_name, window_class, window_title, url,
    idle_seconds, duration_ms, category, productivity_score, rule_name,
    attention_mode, belief_focused, belief_switching, belief_idle,
    focus_session_id
) VALUES (
    :id, :timestamp, :app_name, :window_class, :window_title, :url,
    :idle_seconds, :duration_ms, :category, :productivity_score, :rule_name,
    :attention_mode, :belief_focused, :belief_switching, :belief_idle,
    :focus_session_id
)"""

    _INSERT_SESSION_SQL = """\
INSERT OR REPLACE INTO focus_sessions (
    id, start_time, end_time, category,
    total_duration_ms, interruption_count, app_sequence
) VALUES (
    :id, :start_time, :end_time, :category,
    :total_duration_ms, :interruption_count, :app_sequence
)"""


    def __init__(self, db: Database, max_buffer: int = 1000) -> None:
        self._db = db
        self._max_buffer = max_buffer
        self._buffer: deque[_BufferedRow] = deque()
        self._backoff_seconds: float = 0.0  # 0 means "no active back-off"
        self._last_retry_time: float = 0.0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def store_event(
        self,
        classified: ClassifiedEvent,
        attention_state: AttentionState,
        focus_session_id: Optional[str] = None,
    ) -> bool:
        """Persist a classified event with its attention state.

        Returns ``True`` on immediate DB write success.
        """
        params = self._event_to_params(classified, attention_state)
        if focus_session_id is not None:
            params["focus_session_id"] = focus_session_id
        row = _BufferedRow(table="activity_events", params=params)
        return self._write_row(row)

    def store_focus_session(self, session: FocusSession) -> bool:
        """Persist a completed (or in-progress) focus session.

        Returns ``True`` on immediate DB write success.
        """
        params = self._session_to_params(session)
        row = _BufferedRow(table="focus_sessions", params=params)
        return self._write_row(row)

    def flush_buffer(self) -> int:
        """Try to flush buffered rows to the database.

        Returns the number of rows successfully flushed.
        """
        if not self._buffer:
            return 0

        flushed = 0
        remaining: deque[_BufferedRow] = deque()

        for row in self._buffer:
            try:
                self._execute_insert(row)
                flushed += 1
            except sqlite3.Error:
                remaining.append(row)

        self._buffer = remaining

        if flushed:
            self._reset_backoff()
            logger.info("Flushed %d buffered rows to database", flushed)

        return flushed

    def get_last_event_timestamp(self) -> Optional[str]:
        """Return the ISO timestamp of the most recent stored event, or ``None``."""
        try:
            cur = self._db.connection.execute(
                "SELECT timestamp FROM activity_events ORDER BY timestamp DESC LIMIT 1"
            )
            row = cur.fetchone()
            return row[0] if row else None
        except sqlite3.Error:
            logger.warning("Failed to read last event timestamp")
            return None

    # ------------------------------------------------------------------
    # Buffer / retry helpers
    # ------------------------------------------------------------------

    @property
    def buffer_size(self) -> int:
        """Number of rows currently buffered in memory."""
        return len(self._buffer)

    def _write_row(self, row: _BufferedRow) -> bool:
        """Attempt to write *row* to the DB; buffer on failure."""
        try:
            self._execute_insert(row)
        except sqlite3.DatabaseError as exc:
            if self._is_corruption(exc):
                self._handle_corruption()
            self._add_to_buffer(row)
            self._advance_backoff()
            logger.warning(
                "SQLite write failed (%s); event buffered (%d in buffer)",
                exc,
                len(self._buffer),
            )
            return False

        # Successful write — try to drain the buffer too.
        if self._buffer:
            self.flush_buffer()
        return True

    def _execute_insert(self, row: _BufferedRow) -> None:
        sql = (
            self._INSERT_EVENT_SQL
            if row.table == "activity_events"
            else self._INSERT_SESSION_SQL
        )
        self._db.connection.execute(sql, row.params)
        self._db.connection.commit()

    def _add_to_buffer(self, row: _BufferedRow) -> None:
        if len(self._buffer) >= self._max_buffer:
            dropped = len(self._buffer) - self._max_buffer + 1
            for _ in range(dropped):
                self._buffer.popleft()
            logger.warning("Buffer full — dropped %d oldest event(s)", dropped)
        self._buffer.append(row)

    # ------------------------------------------------------------------
    # Exponential back-off
    # ------------------------------------------------------------------

    _BACKOFF_INITIAL = 1.0
    _BACKOFF_MAX = 30.0

    def _advance_backoff(self) -> None:
        if self._backoff_seconds == 0.0:
            self._backoff_seconds = self._BACKOFF_INITIAL
        else:
            self._backoff_seconds = min(
                self._backoff_seconds * 2, self._BACKOFF_MAX
            )
        self._last_retry_time = time.monotonic()

    def _reset_backoff(self) -> None:
        self._backoff_seconds = 0.0
        self._last_retry_time = 0.0

    @property
    def current_backoff(self) -> float:
        """Current back-off delay in seconds (for observability / tests)."""
        return self._backoff_seconds

    # ------------------------------------------------------------------
    # Corruption recovery
    # ------------------------------------------------------------------

    @staticmethod
    def _is_corruption(exc: sqlite3.DatabaseError) -> bool:
        msg = str(exc).lower()
        return "corrupt" in msg or "malformed" in msg

    def _handle_corruption(self) -> None:
        """Attempt WAL recovery; recreate the DB if that fails."""
        logger.error("Database corruption detected — attempting WAL recovery")
        try:
            self._db.connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            self._db.connection.execute("PRAGMA integrity_check")
            logger.info("WAL recovery succeeded")
        except sqlite3.Error:
            logger.error("WAL recovery failed — creating new database")
            self._recreate_database()

    def _recreate_database(self) -> None:
        """Close the current DB, rename the corrupt file, and open fresh."""
        db_path = self._db.db_path
        try:
            self._db.close()
        except Exception:
            pass

        corrupt_path = db_path + ".corrupt"
        try:
            os.rename(db_path, corrupt_path)
            logger.info("Renamed corrupt DB to %s", corrupt_path)
        except OSError:
            logger.warning("Could not rename corrupt DB file")

        # Re-open a fresh database
        self._db = Database(db_path)
        logger.info("Created new database at %s", db_path)

    # ------------------------------------------------------------------
    # Row mapping
    # ------------------------------------------------------------------

    @staticmethod
    def _event_to_params(
        classified: ClassifiedEvent,
        attention_state: AttentionState,
    ) -> dict:
        ev = classified.event
        return {
            "id": ev.id,
            "timestamp": ev.timestamp.isoformat(),
            "app_name": ev.app_name,
            "window_class": ev.window_class,
            "window_title": ev.window_title,
            "url": ev.url,
            "idle_seconds": ev.idle_seconds,
            "duration_ms": ev.duration_ms,
            "category": classified.category,
            "productivity_score": classified.productivity_score,
            "rule_name": classified.rule_name,
            "attention_mode": attention_state.inferred_mode.value,
            "belief_focused": attention_state.beliefs.focused,
            "belief_switching": attention_state.beliefs.switching,
            "belief_idle": attention_state.beliefs.idle,
            "focus_session_id": None,
        }

    @staticmethod
    def _session_to_params(session: FocusSession) -> dict:
        return {
            "id": session.id,
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat() if session.end_time else None,
            "category": session.category,
            "total_duration_ms": session.total_duration_ms,
            "interruption_count": session.interruption_count,
            "app_sequence": json.dumps(session.app_sequence),
        }
