"""Tests for attention_tracker.browser_monitor."""

from __future__ import annotations

import pytest

from attention_tracker.browser_monitor import (
    BROWSER_SUFFIXES,
    BROWSER_WINDOW_CLASSES,
    BrowserMonitor,
    parse_browser_title,
)


# ---------------------------------------------------------------------------
# parse_browser_title — standard titles
# ---------------------------------------------------------------------------


class TestParseBrowserTitle:
    def test_firefox_standard(self):
        tab = parse_browser_title("GitHub - Mozilla Firefox")
        assert tab is not None
        assert tab.title == "GitHub"
        assert tab.browser == "Firefox"

    def test_firefox_em_dash(self):
        tab = parse_browser_title("GitHub \u2014 Mozilla Firefox")
        assert tab is not None
        assert tab.title == "GitHub"
        assert tab.browser == "Firefox"

    def test_chrome_standard(self):
        tab = parse_browser_title("Stack Overflow - Google Chrome")
        assert tab is not None
        assert tab.title == "Stack Overflow"
        assert tab.browser == "Chrome"

    def test_chromium(self):
        tab = parse_browser_title("Docs - Chromium")
        assert tab is not None
        assert tab.title == "Docs"
        assert tab.browser == "Chromium"

    def test_edge(self):
        tab = parse_browser_title("Outlook - Microsoft Edge")
        assert tab is not None
        assert tab.title == "Outlook"
        assert tab.browser == "Edge"

    def test_brave(self):
        tab = parse_browser_title("Reddit - Brave")
        assert tab is not None
        assert tab.title == "Reddit"
        assert tab.browser == "Brave"

    # -- titles with multiple separators ------------------------------------

    def test_title_with_dash_in_page_title(self):
        """The LAST separator is the browser suffix; earlier dashes are part of the page title."""
        tab = parse_browser_title("CI/CD - Build #42 - Results - Google Chrome")
        assert tab is not None
        assert tab.title == "CI/CD - Build #42 - Results"
        assert tab.browser == "Chrome"

    def test_title_with_multiple_dashes_firefox(self):
        tab = parse_browser_title("My App - Dashboard - Settings - Mozilla Firefox")
        assert tab is not None
        assert tab.title == "My App - Dashboard - Settings"
        assert tab.browser == "Firefox"

    # -- edge cases ---------------------------------------------------------

    def test_empty_string(self):
        assert parse_browser_title("") is None

    def test_whitespace_only(self):
        assert parse_browser_title("   ") is None

    def test_unknown_browser(self):
        assert parse_browser_title("Page - Unknown Browser") is None

    def test_just_browser_name(self):
        """Title that is exactly the suffix (no page title) returns None."""
        assert parse_browser_title(" - Mozilla Firefox") is None

    def test_no_separator(self):
        assert parse_browser_title("just a plain title") is None

    def test_tab_has_timestamp(self):
        tab = parse_browser_title("Page - Google Chrome")
        assert tab is not None
        assert tab.timestamp is not None

    def test_tab_url_is_none(self):
        """Title parsing cannot extract URLs — url should be None."""
        tab = parse_browser_title("Page - Google Chrome")
        assert tab is not None
        assert tab.url is None


# ---------------------------------------------------------------------------
# BrowserMonitor.is_browser
# ---------------------------------------------------------------------------


class TestIsBrowser:
    @pytest.mark.parametrize(
        "wclass",
        [
            "Navigator",
            "firefox",
            "chromium",
            "google-chrome",
            "Google-chrome",
            "Chromium-browser",
            "microsoft-edge",
            "Microsoft-edge",
            "brave-browser",
        ],
    )
    def test_known_browsers(self, wclass: str):
        mon = BrowserMonitor()
        assert mon.is_browser(wclass) is True

    @pytest.mark.parametrize(
        "wclass",
        ["code", "kitty", "Slack", "unknown", ""],
    )
    def test_non_browsers(self, wclass: str):
        mon = BrowserMonitor()
        assert mon.is_browser(wclass) is False


# ---------------------------------------------------------------------------
# BrowserMonitor.get_tab_info
# ---------------------------------------------------------------------------


class TestGetTabInfo:
    def test_browser_with_valid_title(self):
        mon = BrowserMonitor()
        tab = mon.get_tab_info("firefox", "Docs - Mozilla Firefox")
        assert tab is not None
        assert tab.title == "Docs"
        assert tab.browser == "Firefox"

    def test_non_browser_returns_none(self):
        mon = BrowserMonitor()
        assert mon.get_tab_info("code", "file.py - VS Code") is None

    def test_browser_with_unrecognised_title_returns_none(self):
        """Browser window class but title doesn't match any suffix."""
        mon = BrowserMonitor()
        assert mon.get_tab_info("firefox", "New Tab") is None

    def test_chrome_window_class(self):
        mon = BrowserMonitor()
        tab = mon.get_tab_info("google-chrome", "Gmail - Google Chrome")
        assert tab is not None
        assert tab.title == "Gmail"
        assert tab.browser == "Chrome"

    def test_edge_window_class(self):
        mon = BrowserMonitor()
        tab = mon.get_tab_info("microsoft-edge", "Teams - Microsoft Edge")
        assert tab is not None
        assert tab.title == "Teams"
        assert tab.browser == "Edge"
