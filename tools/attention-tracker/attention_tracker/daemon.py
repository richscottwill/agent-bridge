"""Attention Tracker daemon — main polling loop with graceful shutdown.

Ties together Window Monitor, Browser Monitor, Idle Detector,
Event Processor, and the SQLite database.  Designed to run under
systemd (``attention-tracker.service``) or standalone.

Zero network operations in all code paths.
"""

from __future__ import annotations

import logging
import signal
import sys
import time
from types import FrameType
from typing import Optional

from attention_tracker.browser_monitor import BrowserMonitor
from attention_tracker.database import Database
from attention_tracker.event_processor import EventProcessor
from attention_tracker.event_store import EventStore
from attention_tracker.idle_detector import IdleDetector
from attention_tracker.models import TrackerConfig
from attention_tracker.rules_loader import load_rules
from attention_tracker.session_tracker import SessionTracker
from attention_tracker.window_monitor import WindowMonitor

logger = logging.getLogger(__name__)


class TrackerDaemon:
    """Main daemon that polls the active window and processes events."""

    def __init__(self, config: TrackerConfig) -> None:
        self._config = config
        self._running = False

        # Components initialised in start() so __init__ stays lightweight
        self._db: Optional[Database] = None
        self._window_monitor: Optional[WindowMonitor] = None
        self._browser_monitor: Optional[BrowserMonitor] = None
        self._idle_detector: Optional[IdleDetector] = None
        self._event_store: Optional[EventStore] = None
        self._session_tracker: Optional[SessionTracker] = None
        self._event_processor: Optional[EventProcessor] = None

        # Track previous idle state for detecting significant changes
        self._last_idle_seconds: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Start the daemon: initialise components, handle restart, enter polling loop."""
        logger.info("Attention Tracker daemon starting")

        self._setup_signal_handlers()
        self._init_components()

        # Handle restart gap detection
        assert self._event_processor is not None
        self._event_processor.handle_restart()

        logger.info(
            "Entering polling loop (interval=%d ms)",
            self._config.poll_interval_ms,
        )
        self._running = True

        try:
            self._run_loop()
        finally:
            self._shutdown()

    def stop(self) -> None:
        """Signal the daemon to stop gracefully."""
        logger.info("Stop requested")
        self._running = False

    # ------------------------------------------------------------------
    # Polling loop
    # ------------------------------------------------------------------

    def _run_loop(self) -> None:
        """Main polling loop — runs until ``_running`` is set to False."""
        sleep_seconds = self._config.poll_interval_ms / 1000.0

        while self._running:
            try:
                self._poll_once()
            except Exception:
                logger.exception("Error during poll cycle")

            time.sleep(sleep_seconds)

    def _poll_once(self) -> None:
        """Execute one poll cycle."""
        assert self._window_monitor is not None
        assert self._browser_monitor is not None
        assert self._idle_detector is not None
        assert self._event_processor is not None

        idle_seconds = self._idle_detector.get_idle_seconds()
        window = self._window_monitor.poll()

        if window is not None:
            # Window changed — always process
            tab = self._browser_monitor.get_tab_info(
                window.window_class, window.window_title
            )
            self._event_processor.process(window, tab, idle_seconds)
            self._last_idle_seconds = idle_seconds

        elif self._idle_state_changed_significantly(idle_seconds):
            # Window unchanged but idle state shifted — re-process with last known window
            last_window = self._window_monitor.last_window
            if last_window is not None:
                tab = self._browser_monitor.get_tab_info(
                    last_window.window_class, last_window.window_title
                )
                self._event_processor.process(last_window, tab, idle_seconds)
                self._last_idle_seconds = idle_seconds

    def _idle_state_changed_significantly(self, idle_seconds: int) -> bool:
        """Return True if idle state crossed a meaningful threshold."""
        prev = self._last_idle_seconds
        idle_thresh = self._config.idle_threshold_seconds
        away_thresh = self._config.away_threshold_seconds

        # Crossed idle threshold in either direction
        if (prev < idle_thresh) != (idle_seconds < idle_thresh):
            return True
        # Crossed away threshold in either direction
        if (prev < away_thresh) != (idle_seconds < away_thresh):
            return True
        return False

    # ------------------------------------------------------------------
    # Signal handling
    # ------------------------------------------------------------------

    def _setup_signal_handlers(self) -> None:
        """Register SIGTERM/SIGINT handlers for graceful shutdown."""
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

    def _handle_signal(self, signum: int, frame: Optional[FrameType]) -> None:
        """Handle termination signals."""
        sig_name = signal.Signals(signum).name
        logger.info("Received %s — shutting down", sig_name)
        self._running = False

    # ------------------------------------------------------------------
    # Initialisation / teardown
    # ------------------------------------------------------------------

    def _init_components(self) -> None:
        """Create and wire all daemon components."""
        # Load classification rules (graceful if file missing)
        rules = self._load_rules()

        # Database
        self._db = Database(self._config.db_path)

        # Monitors
        self._window_monitor = WindowMonitor()
        self._browser_monitor = BrowserMonitor()
        self._idle_detector = IdleDetector()

        # Storage + session tracking
        self._event_store = EventStore(self._db)
        self._session_tracker = SessionTracker(self._event_store)

        # Event processor (ties everything together)
        self._event_processor = EventProcessor(
            config=self._config,
            classifier_rules=rules,
            event_store=self._event_store,
            session_tracker=self._session_tracker,
        )

        logger.info("All components initialised")

    def _load_rules(self) -> list:
        """Load classification rules from the configured path."""
        import os

        rules_path = os.path.expanduser(self._config.rules_path)
        try:
            rules = load_rules(rules_path)
            logger.info("Loaded %d classification rules from %s", len(rules), rules_path)
            return rules
        except FileNotFoundError:
            logger.warning(
                "Rules file not found at %s — running with no rules", rules_path
            )
            return []

    def _shutdown(self) -> None:
        """Clean up resources on exit."""
        logger.info("Shutting down daemon")
        if self._db is not None:
            try:
                self._db.close()
                logger.info("Database closed")
            except Exception:
                logger.exception("Error closing database")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point for ``python -m attention_tracker.daemon``."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    config = TrackerConfig()
    daemon = TrackerDaemon(config)

    try:
        daemon.start()
    except KeyboardInterrupt:
        pass

    logger.info("Daemon exited")


if __name__ == "__main__":
    main()
