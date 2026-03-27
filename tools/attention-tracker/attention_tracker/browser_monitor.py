"""Browser monitor: extracts tab context from browser window titles.

Window title parsing is the PRIMARY approach — it works across all browsers,
Snaps, and Flatpaks without extension installation.  Native messaging
extensions are an optional enhancement for richer URL data.

Never reads browsing history — only the current active tab context.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

from attention_tracker.models import TabInfo

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Known browser window classes (used by is_browser)
# ---------------------------------------------------------------------------

BROWSER_WINDOW_CLASSES: set[str] = {
    "Navigator",          # Firefox (WM_CLASS instance)
    "firefox",
    "chromium",
    "google-chrome",
    "Google-chrome",
    "Chromium-browser",
    "microsoft-edge",
    "Microsoft-edge",
    "brave-browser",
}

# ---------------------------------------------------------------------------
# Known browser title suffixes → browser display name
# ---------------------------------------------------------------------------

BROWSER_SUFFIXES: dict[str, str] = {
    " - Mozilla Firefox": "Firefox",
    " \u2014 Mozilla Firefox": "Firefox",   # em-dash variant
    " - Google Chrome": "Chrome",
    " - Chromium": "Chromium",
    " - Microsoft Edge": "Edge",
    " - Brave": "Brave",
}


# ---------------------------------------------------------------------------
# Title parser
# ---------------------------------------------------------------------------

def parse_browser_title(window_title: str) -> Optional[TabInfo]:
    """Extract page title and browser name from a browser window title.

    Browser window titles typically follow the pattern:
        "{page_title} - {browser_name}"
    or with an em-dash:
        "{page_title} — {browser_name}"

    When the page title itself contains " - ", we match the LAST occurrence
    by checking known suffixes (which always appear at the end).

    Returns None if the title doesn't match any known browser suffix.
    """
    if not window_title or not window_title.strip():
        return None

    for suffix, browser_name in BROWSER_SUFFIXES.items():
        if window_title.endswith(suffix):
            page_title = window_title[: -len(suffix)]
            # Guard against empty page titles (title was just the browser name)
            if not page_title:
                return None
            return TabInfo(
                title=page_title,
                browser=browser_name,
                timestamp=datetime.now(timezone.utc),
            )

    return None


# ---------------------------------------------------------------------------
# BrowserMonitor
# ---------------------------------------------------------------------------

class BrowserMonitor:
    """Monitors browser windows and extracts tab context.

    Uses window title parsing as the primary approach.  Native messaging
    extension support is an optional enhancement (not implemented here).
    """

    def get_tab_info(
        self, window_class: str, window_title: str
    ) -> Optional[TabInfo]:
        """Return TabInfo if *window_class* belongs to a browser, else None.

        Combines ``is_browser`` check with title parsing so callers get a
        single call that either returns rich tab context or None.
        """
        if not self.is_browser(window_class):
            return None

        tab = parse_browser_title(window_title)
        if tab is not None:
            return tab

        # Browser window but title didn't match any known suffix.
        # Fall back gracefully — return basic info from the raw title.
        logger.debug(
            "Browser window class %r but title didn't match known suffix: %r",
            window_class,
            window_title,
        )
        return None

    @staticmethod
    def is_browser(window_class: str) -> bool:
        """Return True if *window_class* belongs to a known browser."""
        return window_class in BROWSER_WINDOW_CLASSES
