"""Tests for attention_tracker.window_monitor.

All tests mock subprocess.run so they work without a display server.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from attention_tracker.window_monitor import (
    WindowMonitor,
    _make_sentinel,
    _parse_hyprctl,
    _parse_swaymsg,
    _parse_xprop_class,
    _parse_xprop_pid,
    _parse_xprop_title,
    _run,
    detect_display_server,
)


# ---------------------------------------------------------------------------
# xprop parsing
# ---------------------------------------------------------------------------

XPROP_SAMPLE = (
    'WM_CLASS(STRING) = "Navigator", "firefox"\n'
    '_NET_WM_NAME(UTF8_STRING) = "GitHub - Mozilla Firefox"\n'
    '_NET_WM_PID(CARDINAL) = 12345'
)


class TestXpropParsing:
    def test_parse_pid(self):
        assert _parse_xprop_pid(XPROP_SAMPLE) == 12345

    def test_parse_pid_missing(self):
        assert _parse_xprop_pid("WM_CLASS = something") == 0

    def test_parse_class(self):
        assert _parse_xprop_class(XPROP_SAMPLE) == "firefox"

    def test_parse_class_missing(self):
        assert _parse_xprop_class("no class here") == "unknown"

    def test_parse_title(self):
        assert _parse_xprop_title(XPROP_SAMPLE) == "GitHub - Mozilla Firefox"

    def test_parse_title_missing(self):
        assert _parse_xprop_title("no title here") == "unknown"


# ---------------------------------------------------------------------------
# Wayland parsing — swaymsg
# ---------------------------------------------------------------------------

SWAY_TREE = {
    "focused": False,
    "nodes": [
        {
            "focused": False,
            "nodes": [
                {
                    "focused": True,
                    "pid": 9999,
                    "app_id": "kitty",
                    "name": "~/code — kitty",
                    "nodes": [],
                    "floating_nodes": [],
                }
            ],
            "floating_nodes": [],
        }
    ],
    "floating_nodes": [],
}


class TestSwaymsgParsing:
    def test_parse_focused(self):
        info = _parse_swaymsg(json.dumps(SWAY_TREE))
        assert info is not None
        assert info.pid == 9999
        assert info.window_class == "kitty"
        assert info.window_title == "~/code — kitty"

    def test_parse_no_focused(self):
        tree = {"focused": False, "nodes": [], "floating_nodes": []}
        assert _parse_swaymsg(json.dumps(tree)) is None

    def test_parse_invalid_json(self):
        assert _parse_swaymsg("not json") is None

    def test_parse_none_input(self):
        assert _parse_swaymsg(None) is None

    def test_parse_window_properties_fallback(self):
        """When app_id is missing, fall back to window_properties.class (XWayland)."""
        tree = {
            "focused": True,
            "pid": 100,
            "app_id": None,
            "window_properties": {"class": "Chromium"},
            "name": "Google",
            "nodes": [],
            "floating_nodes": [],
        }
        info = _parse_swaymsg(json.dumps(tree))
        assert info is not None
        assert info.window_class == "Chromium"


# ---------------------------------------------------------------------------
# Wayland parsing — hyprctl
# ---------------------------------------------------------------------------

HYPRCTL_SAMPLE = {"pid": 5555, "class": "code", "title": "window_monitor.py — VS Code"}


class TestHyprctlParsing:
    def test_parse_active(self):
        info = _parse_hyprctl(json.dumps(HYPRCTL_SAMPLE))
        assert info is not None
        assert info.pid == 5555
        assert info.window_class == "code"
        assert info.window_title == "window_monitor.py — VS Code"

    def test_parse_empty_dict(self):
        assert _parse_hyprctl("{}") is None

    def test_parse_invalid_json(self):
        assert _parse_hyprctl("nope") is None

    def test_parse_none(self):
        assert _parse_hyprctl(None) is None


# ---------------------------------------------------------------------------
# detect_display_server
# ---------------------------------------------------------------------------

class TestDetectDisplayServer:
    def test_wayland_display_set(self):
        with patch.dict("os.environ", {"WAYLAND_DISPLAY": "wayland-0"}, clear=False):
            assert detect_display_server() == "wayland"

    def test_xdg_session_type_wayland(self):
        env = {"XDG_SESSION_TYPE": "wayland"}
        with patch.dict("os.environ", env, clear=True):
            assert detect_display_server() == "wayland"

    def test_x11_default(self):
        with patch.dict("os.environ", {}, clear=True):
            assert detect_display_server() == "x11"

    def test_xdg_session_type_x11(self):
        env = {"XDG_SESSION_TYPE": "x11"}
        with patch.dict("os.environ", env, clear=True):
            assert detect_display_server() == "x11"


# ---------------------------------------------------------------------------
# _run helper
# ---------------------------------------------------------------------------

class TestRunHelper:
    @patch("attention_tracker.window_monitor.subprocess.run")
    def test_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="  hello  ")
        assert _run(["echo", "hello"]) == "hello"

    @patch("attention_tracker.window_monitor.subprocess.run")
    def test_nonzero_exit(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stdout="")
        assert _run(["false"]) is None

    @patch("attention_tracker.window_monitor.subprocess.run", side_effect=FileNotFoundError)
    def test_missing_binary(self, mock_run):
        assert _run(["nonexistent"]) is None

    @patch("attention_tracker.window_monitor.subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 2))
    def test_timeout(self, mock_run):
        assert _run(["slow"]) is None


# ---------------------------------------------------------------------------
# _make_sentinel
# ---------------------------------------------------------------------------

class TestSentinel:
    def test_sentinel_fields(self):
        s = _make_sentinel()
        assert s.pid == 0
        assert s.window_class == "unknown"
        assert s.window_title == "unknown"
        assert isinstance(s.timestamp, datetime)


# ---------------------------------------------------------------------------
# WindowMonitor — X11 backend
# ---------------------------------------------------------------------------

def _mock_run_x11(cmd, **kwargs):
    """Simulate xdotool + xprop for a Firefox window."""
    if cmd[0] == "xdotool":
        return MagicMock(returncode=0, stdout="12345678")
    if cmd[0] == "xprop":
        return MagicMock(returncode=0, stdout=XPROP_SAMPLE)
    return MagicMock(returncode=1, stdout="")


class TestWindowMonitorX11:
    @patch("attention_tracker.window_monitor.detect_display_server", return_value="x11")
    @patch("attention_tracker.window_monitor.subprocess.run", side_effect=_mock_run_x11)
    def test_poll_returns_window_info(self, mock_run, mock_detect):
        mon = WindowMonitor()
        info = mon.poll()
        assert info is not None
        assert info.pid == 12345
        assert info.window_class == "firefox"
        assert info.window_title == "GitHub - Mozilla Firefox"

    @patch("attention_tracker.window_monitor.detect_display_server", return_value="x11")
    @patch("attention_tracker.window_monitor.subprocess.run", side_effect=_mock_run_x11)
    def test_dedup_same_window(self, mock_run, mock_detect):
        mon = WindowMonitor()
        first = mon.poll()
        assert first is not None
        second = mon.poll()
        assert second is None  # same window, deduplicated

    @patch("attention_tracker.window_monitor.detect_display_server", return_value="x11")
    @patch("attention_tracker.window_monitor.subprocess.run", return_value=MagicMock(returncode=1, stdout=""))
    def test_xdotool_failure_returns_sentinel(self, mock_run, mock_detect):
        mon = WindowMonitor()
        info = mon.poll()
        assert info is not None
        assert info.pid == 0
        assert info.window_class == "unknown"

    @patch("attention_tracker.window_monitor.detect_display_server", return_value="x11")
    @patch("attention_tracker.window_monitor.subprocess.run")
    def test_dedup_then_change(self, mock_run, mock_detect):
        """After dedup, a different window should be emitted."""
        call_count = [0]

        def side_effect(cmd, **kwargs):
            call_count[0] += 1
            if cmd[0] == "xdotool":
                return MagicMock(returncode=0, stdout="111")
            if cmd[0] == "xprop":
                # First two calls: firefox, third+: code
                if call_count[0] <= 4:  # 2 calls per poll (xdotool + xprop)
                    return MagicMock(
                        returncode=0,
                        stdout=(
                            'WM_CLASS(STRING) = "nav", "firefox"\n'
                            '_NET_WM_NAME(UTF8_STRING) = "Page"\n'
                            '_NET_WM_PID(CARDINAL) = 1'
                        ),
                    )
                return MagicMock(
                    returncode=0,
                    stdout=(
                        'WM_CLASS(STRING) = "code", "Code"\n'
                        '_NET_WM_NAME(UTF8_STRING) = "Editor"\n'
                        '_NET_WM_PID(CARDINAL) = 2'
                    ),
                )
            return MagicMock(returncode=1, stdout="")

        mock_run.side_effect = side_effect
        mon = WindowMonitor()
        first = mon.poll()
        assert first is not None
        assert first.window_class == "firefox"

        second = mon.poll()
        assert second is None  # dedup

        third = mon.poll()
        assert third is not None
        assert third.window_class == "Code"


# ---------------------------------------------------------------------------
# WindowMonitor — Wayland backend
# ---------------------------------------------------------------------------

class TestWindowMonitorWayland:
    @patch("attention_tracker.window_monitor.detect_display_server", return_value="wayland")
    @patch("attention_tracker.window_monitor.subprocess.run")
    def test_swaymsg_success(self, mock_run, mock_detect):
        mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps(SWAY_TREE))
        mon = WindowMonitor()
        info = mon.poll()
        assert info is not None
        assert info.pid == 9999
        assert info.window_class == "kitty"

    @patch("attention_tracker.window_monitor.detect_display_server", return_value="wayland")
    @patch("attention_tracker.window_monitor.subprocess.run")
    def test_hyprctl_fallback(self, mock_run, mock_detect):
        """When swaymsg fails, try hyprctl."""
        def side_effect(cmd, **kwargs):
            if cmd[0] == "swaymsg":
                return MagicMock(returncode=1, stdout="")
            if cmd[0] == "hyprctl":
                return MagicMock(returncode=0, stdout=json.dumps(HYPRCTL_SAMPLE))
            return MagicMock(returncode=1, stdout="")

        mock_run.side_effect = side_effect
        mon = WindowMonitor()
        info = mon.poll()
        assert info is not None
        assert info.pid == 5555
        assert info.window_class == "code"

    @patch("attention_tracker.window_monitor.detect_display_server", return_value="wayland")
    @patch("attention_tracker.window_monitor.subprocess.run")
    def test_xwayland_fallback(self, mock_run, mock_detect):
        """When both swaymsg and hyprctl fail, fall back to X11 via XWayland."""
        def side_effect(cmd, **kwargs):
            if cmd[0] in ("swaymsg", "hyprctl"):
                return MagicMock(returncode=1, stdout="")
            return _mock_run_x11(cmd, **kwargs)

        mock_run.side_effect = side_effect
        mon = WindowMonitor()
        info = mon.poll()
        assert info is not None
        assert info.pid == 12345
        assert info.window_class == "firefox"

    @patch("attention_tracker.window_monitor.detect_display_server", return_value="wayland")
    @patch("attention_tracker.window_monitor.subprocess.run", return_value=MagicMock(returncode=1, stdout=""))
    def test_all_fail_returns_sentinel(self, mock_run, mock_detect):
        mon = WindowMonitor()
        info = mon.poll()
        assert info is not None
        assert info.pid == 0
        assert info.window_class == "unknown"

    @patch("attention_tracker.window_monitor.detect_display_server", return_value="wayland")
    @patch("attention_tracker.window_monitor.subprocess.run")
    def test_wayland_dedup(self, mock_run, mock_detect):
        mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps(SWAY_TREE))
        mon = WindowMonitor()
        first = mon.poll()
        assert first is not None
        second = mon.poll()
        assert second is None
