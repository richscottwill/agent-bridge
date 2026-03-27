"""Event Processor: ties all components together in the processing pipeline.

Merges signals from Window Monitor, Browser Monitor, and Idle Detector,
pipes them through the Activity Classifier and Bayesian State Machine,
and stores the results to the database.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

from attention_tracker.classifier import classify_event
from attention_tracker.event_store import EventStore
from attention_tracker.models import (
    ActivityEvent,
    AttentionBeliefs,
    AttentionMode,
    AttentionState,
    ClassificationRule,
    ClassifiedEvent,
    TabInfo,
    TrackerConfig,
    WindowInfo,
)
from attention_tracker.session_tracker import SessionTracker
from attention_tracker.state_machine import bayesian_update

logger = logging.getLogger(__name__)


class EventProcessor:
    """Merge window/browser/idle signals, classify, update state, and store."""

    def __init__(
        self,
        config: TrackerConfig,
        classifier_rules: list[ClassificationRule],
        event_store: EventStore,
        session_tracker: SessionTracker,
    ) -> None:
        self._config = config
        self._rules = classifier_rules
        self._store = event_store
        self._session_tracker = session_tracker
        self._state: AttentionState = self._initial_state()
        self._previous_mode: AttentionMode = AttentionMode.IDLE

    def process(
        self, window: WindowInfo, tab: Optional[TabInfo], idle_seconds: int
    ) -> None:
        """Process one poll cycle: window info + optional tab + idle → classify → update state → store."""
        # Step 1: Create an ActivityEvent from inputs
        event = ActivityEvent(
            id=ActivityEvent.new_id(),
            timestamp=window.timestamp,
            app_name=window.window_class,
            window_class=window.window_class,
            window_title=window.window_title,
            idle_seconds=idle_seconds,
            duration_ms=self._config.poll_interval_ms,
            url=tab.url if tab else None,
        )

        # Step 2: Classify the event
        classified = classify_event(event, self._rules)

        # Step 3: Bayesian update
        new_state = bayesian_update(self._state, classified, self._config)

        # Step 4: Process session transitions
        self._session_tracker.process_transition(
            self._previous_mode,
            new_state.inferred_mode,
            new_state,
            classified,
        )

        # Step 5: Store the event (with focus_session_id if in a session)
        self._store.store_event(
            classified,
            new_state,
            focus_session_id=self._session_tracker.current_session_id,
        )

        # Update internal state
        self._previous_mode = new_state.inferred_mode
        self._state = new_state

    def handle_restart(self) -> None:
        """Handle daemon restart: check for gap, record offline event, reset beliefs."""
        last_ts = self._store.get_last_event_timestamp()

        if last_ts is not None:
            # Create a "daemon-offline" gap event
            now = datetime.now(timezone.utc)
            gap_event = ActivityEvent(
                id=ActivityEvent.new_id(),
                timestamp=now,
                app_name="daemon-offline",
                window_class="daemon-offline",
                window_title="daemon-offline",
                idle_seconds=0,
                duration_ms=0,
                url=None,
            )
            classified_gap = ClassifiedEvent(
                event=gap_event,
                category="daemon-offline",
                productivity_score=None,
                rule_name="system",
            )
            # Store with current (about-to-be-reset) state
            self._store.store_event(classified_gap, self._state)
            logger.info(
                "Recorded daemon-offline gap event since last event at %s",
                last_ts,
            )

        # Reset beliefs to uniform prior
        self._state = self._initial_state()
        self._previous_mode = AttentionMode.IDLE

    @staticmethod
    def _initial_state() -> AttentionState:
        """Return uniform-prior initial state."""
        return AttentionState(
            beliefs=AttentionBeliefs(
                focused=0.33,
                switching=0.33,
                idle=0.34,
            ),
            inferred_mode=AttentionMode.IDLE,
            since=datetime.now(timezone.utc),
            current_category="uncategorized",
            focus_duration_ms=0,
        )

    @property
    def state(self) -> AttentionState:
        """Current attention state (for observability)."""
        return self._state

    @property
    def previous_mode(self) -> AttentionMode:
        """Previous attention mode (for observability)."""
        return self._previous_mode
