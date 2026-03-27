"""Focus Session tracking for the Attention Tracker.

Creates, updates, and closes FocusSession objects based on attention mode
transitions. Persists completed sessions via EventStore.
"""

from __future__ import annotations

from typing import Optional
from uuid import uuid4

from attention_tracker.event_store import EventStore
from attention_tracker.models import (
    AttentionMode,
    AttentionState,
    ClassifiedEvent,
    FocusSession,
)


class SessionTracker:
    """Track focus sessions based on attention mode transitions.

    A new session starts when the mode transitions *to* FOCUSED.
    The session closes when the mode transitions *away* from FOCUSED.
    While staying FOCUSED, the session's app_sequence is updated (deduped).
    """

    def __init__(self, event_store: EventStore) -> None:
        self._store = event_store
        self._current_session: Optional[FocusSession] = None

    def process_transition(
        self,
        previous_mode: AttentionMode,
        current_mode: AttentionMode,
        current_state: AttentionState,
        event: ClassifiedEvent,
    ) -> Optional[FocusSession]:
        """Process a mode transition. Returns a completed FocusSession if one just ended."""
        was_focused = previous_mode == AttentionMode.FOCUSED
        now_focused = current_mode == AttentionMode.FOCUSED

        # Case 1: Entering FOCUSED from a non-FOCUSED mode → start new session
        if not was_focused and now_focused:
            self._start_session(event)
            return None

        # Case 2: Leaving FOCUSED → close session, persist, return it
        if was_focused and not now_focused:
            return self._close_session(event)

        # Case 3: Staying FOCUSED → update session (app sequence, interruptions)
        if was_focused and now_focused:
            self._update_session(event, current_state)
            return None

        # Case 4: Non-FOCUSED → Non-FOCUSED — nothing to do
        return None

    @property
    def current_session(self) -> Optional[FocusSession]:
        """The active focus session, or None if not currently focused."""
        return self._current_session

    @property
    def current_session_id(self) -> Optional[str]:
        """Returns the current session ID for tagging events, or None."""
        if self._current_session is not None:
            return self._current_session.id
        return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _start_session(self, event: ClassifiedEvent) -> None:
        """Create a new FocusSession from the triggering event."""
        self._current_session = FocusSession(
            id=str(uuid4()),
            start_time=event.event.timestamp,
            category=event.category,
            total_duration_ms=0,
            interruption_count=0,
            app_sequence=[event.event.app_name],
        )

    def _close_session(self, event: ClassifiedEvent) -> Optional[FocusSession]:
        """Close the current session, persist it, and return it."""
        session = self._current_session
        if session is None:
            return None

        session.end_time = event.event.timestamp
        delta = session.end_time - session.start_time
        session.total_duration_ms = int(delta.total_seconds() * 1000)

        self._store.store_focus_session(session)
        self._current_session = None
        return session

    def _update_session(
        self, event: ClassifiedEvent, current_state: AttentionState
    ) -> None:
        """Update the running session while still FOCUSED."""
        if self._current_session is None:
            return

        # Deduplicated app sequence: only add if different from last entry
        app_name = event.event.app_name
        if (
            not self._current_session.app_sequence
            or self._current_session.app_sequence[-1] != app_name
        ):
            self._current_session.app_sequence.append(app_name)

        # Track interruptions: focus_duration_ms resetting to 0 while still
        # FOCUSED means the state machine detected a brief interruption.
        if current_state.focus_duration_ms == 0:
            self._current_session.interruption_count += 1
