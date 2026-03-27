"""Window monitor: detects the currently active window on Linux.

Supports Wayland-native detection (swaymsg / hyprctl) as primary,
with X11 fallback (xdotool / xprop).  Auto-detects the display server
from environment variables.
"""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
from datetime import datetime, timezone
from typing import Optional

from attention_tracker.models import WindowInfo

logger = logging.getLogger(__name__)

# Sentinel returned when the active window cannot be determined.
_UNKNOWN_WINDOW = WindowInfo(
    pid=0,
    window_class="unknown",
    window_title="unknown",
    timestamp=datetime.now(timezone.utc),
)


def _make_sentinel() -> WindowInfo:
    """Return a fresh sentinel with the current timestamp."""
    return WindowInfo(
        pid=0,
        window_class="unknown",
        window_title="unknown",
        timestamp=datetime.now(timezone.utc),
    )


def _run(cmd: list[str], timeout: float = 2.0) -> Optional[str]:
    """Run a subprocess and return stripped stdout, or None on failure."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None


# ---------------------------------------------------------------------------
# X11 helpers
# ---------------------------------------------------------------------------

def _parse_xprop_pid(xprop_output: str) -> int:
    """Extract PID from xprop output containing _NET_WM_PID."""
    match = re.search(r"_NET_WM_PID.*?=\s*(\d+)", xprop_output)
    return int(match.group(1)) if match else 0


def _parse_xprop_class(xprop_output: str) -> str:
    """Extract window class from xprop WM_CLASS line.

    WM_CLASS format: WM_CLASS(STRING) = "instance", "class"
    We return the class (second value).
    """
    match = re.search(r'WM_CLASS.*?=\s*"([^"]*)",\s*"([^"]*)"', xprop_output)
    if match:
        return match.group(2)
    return "unknown"


def _parse_xprop_title(xprop_output: str) -> str:
    """Extract window title from _NET_WM_NAME in xprop output."""
    match = re.search(r'_NET_WM_NAME.*?=\s*"(.*)"', xprop_output)
    if match:
        return match.group(1)
    return "unknown"


# ---------------------------------------------------------------------------
# Wayland helpers
# ---------------------------------------------------------------------------

def _parse_swaymsg(output: str) -> Optional[WindowInfo]:
    """Parse swaymsg -t get_tree JSON to find the focused window."""
    try:
        tree = json.loads(output)
    except (json.JSONDecodeError, TypeError):
        return None

    def _find_focused(node: dict) -> Optional[dict]:
        if node.get("focused"):
            return node
        for child in node.get("nodes", []) + node.get("floating_nodes", []):
            result = _find_focused(child)
            if result:
                return result
        return None

    focused = _find_focused(tree)
    if not focused:
        return None

    return WindowInfo(
        pid=focused.get("pid", 0),
        window_class=focused.get("app_id") or focused.get("window_properties", {}).get("class", "unknown"),
        window_title=focused.get("name", "unknown"),
        timestamp=datetime.now(timezone.utc),
    )


def _parse_hyprctl(output: str) -> Optional[WindowInfo]:
    """Parse hyprctl activewindow -j JSON output."""
    try:
        data = json.loads(output)
    except (json.JSONDecodeError, TypeError):
        return None

    if not data or not isinstance(data, dict):
        return None

    return WindowInfo(
        pid=data.get("pid", 0),
        window_class=data.get("class", "unknown"),
        window_title=data.get("title", "unknown"),
        timestamp=datetime.now(timezone.utc),
    )


# ---------------------------------------------------------------------------
# Display server detection
# ---------------------------------------------------------------------------

def detect_display_server() -> str:
    """Return 'wayland' or 'x11' based on environment variables."""
    if os.environ.get("WAYLAND_DISPLAY"):
        return "wayland"
    session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
    if session_type == "wayland":
        return "wayland"
    return "x11"


# ---------------------------------------------------------------------------
# WindowMonitor
# ---------------------------------------------------------------------------

class WindowMonitor:
    """Polls the active window, deduplicating consecutive identical results."""

    def __init__(self) -> None:
        self._backend = detect_display_server()
        self._last: Optional[WindowInfo] = None
        logger.info("WindowMonitor initialised with backend=%s", self._backend)

    # -- public API ----------------------------------------------------------

    def poll(self) -> Optional[WindowInfo]:
        """Return a WindowInfo if the active window changed, else None."""
        if self._backend == "wayland":
            info = self._get_wayland_window()
        else:
            info = self._get_x11_window()

        if self._is_same(info, self._last):
            return None

        self._last = info
        return info

    # -- backend implementations ---------------------------------------------

    def _get_x11_window(self) -> WindowInfo:
        """Retrieve active window info via xdotool + xprop (X11)."""
        wid = _run(["xdotool", "getactivewindow"])
        if not wid:
            return _make_sentinel()

        xprop_out = _run(["xprop", "-id", wid, "WM_CLASS", "_NET_WM_NAME", "_NET_WM_PID"])
        if not xprop_out:
            return _make_sentinel()

        return WindowInfo(
            pid=_parse_xprop_pid(xprop_out),
            window_class=_parse_xprop_class(xprop_out),
            window_title=_parse_xprop_title(xprop_out),
            timestamp=datetime.now(timezone.utc),
        )

    def _get_wayland_window(self) -> WindowInfo:
        """Retrieve active window info on Wayland (swaymsg / hyprctl, X11 fallback)."""
        # Try swaymsg first (sway compositor)
        sway_out = _run(["swaymsg", "-t", "get_tree"])
        if sway_out:
            info = _parse_swaymsg(sway_out)
            if info:
                return info

        # Try hyprctl (Hyprland compositor)
        hypr_out = _run(["hyprctl", "activewindow", "-j"])
        if hypr_out:
            info = _parse_hyprctl(hypr_out)
            if info:
                return info

        # Fall back to xdotool via XWayland
        return self._get_x11_window()

    @property
    def last_window(self) -> Optional[WindowInfo]:
        """The most recently observed window (may be None before first poll)."""
        return self._last

    # -- deduplication -------------------------------------------------------

    @staticmethod
    def _is_same(a: WindowInfo, b: Optional[WindowInfo]) -> bool:
        """Return True if two WindowInfo represent the same window."""
        if b is None:
            return False
        return (
            a.pid == b.pid
            and a.window_class == b.window_class
            and a.window_title == b.window_title
        )
