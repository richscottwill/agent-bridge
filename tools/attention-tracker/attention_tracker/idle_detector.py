"""Idle time detection via xprintidle or fallback.

Detects user idle time (seconds since last keyboard/mouse input).
Primary: ``xprintidle`` command (common on Linux X11/XWayland).
Fallback: returns 0 if the command is unavailable.
"""

from __future__ import annotations

import logging
import subprocess

logger = logging.getLogger(__name__)


class IdleDetector:
    """Detect user idle time via xprintidle command with graceful fallback."""

    def __init__(self) -> None:
        self._available: bool | None = None  # lazy probe

    def get_idle_seconds(self) -> int:
        """Return seconds since last user input.

        Uses ``xprintidle`` which reports idle time in milliseconds.
        Returns 0 if the tool is unavailable or fails.
        """
        if self._available is False:
            return 0

        try:
            result = subprocess.run(
                ["xprintidle"],
                capture_output=True,
                text=True,
                timeout=2.0,
            )
            if result.returncode != 0:
                if self._available is None:
                    logger.info("xprintidle not available; idle detection disabled")
                    self._available = False
                return 0

            self._available = True
            idle_ms = int(result.stdout.strip())
            return idle_ms // 1000

        except FileNotFoundError:
            if self._available is None:
                logger.info("xprintidle not found; idle detection disabled")
            self._available = False
            return 0
        except (subprocess.TimeoutExpired, ValueError, OSError) as exc:
            logger.debug("xprintidle failed: %s", exc)
            return 0
