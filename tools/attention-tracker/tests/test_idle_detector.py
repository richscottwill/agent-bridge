"""Tests for the IdleDetector class."""

from unittest.mock import patch, MagicMock
import subprocess

import pytest

from attention_tracker.idle_detector import IdleDetector


class TestIdleDetector:
    """Unit tests for IdleDetector.get_idle_seconds()."""

    def test_returns_seconds_from_xprintidle(self):
        """xprintidle reports milliseconds; we return seconds."""
        detector = IdleDetector()
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "5000\n"

        with patch("attention_tracker.idle_detector.subprocess.run", return_value=mock_result):
            assert detector.get_idle_seconds() == 5

    def test_returns_zero_when_xprintidle_not_found(self):
        """Graceful fallback when xprintidle is not installed."""
        detector = IdleDetector()

        with patch(
            "attention_tracker.idle_detector.subprocess.run",
            side_effect=FileNotFoundError,
        ):
            assert detector.get_idle_seconds() == 0

    def test_returns_zero_on_nonzero_exit(self):
        """Non-zero exit code (e.g., no display) returns 0."""
        detector = IdleDetector()
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""

        with patch("attention_tracker.idle_detector.subprocess.run", return_value=mock_result):
            assert detector.get_idle_seconds() == 0

    def test_returns_zero_on_timeout(self):
        """Timeout returns 0 without crashing."""
        detector = IdleDetector()

        with patch(
            "attention_tracker.idle_detector.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="xprintidle", timeout=2.0),
        ):
            assert detector.get_idle_seconds() == 0

    def test_caches_unavailability(self):
        """After first failure, subsequent calls skip the subprocess entirely."""
        detector = IdleDetector()

        with patch(
            "attention_tracker.idle_detector.subprocess.run",
            side_effect=FileNotFoundError,
        ) as mock_run:
            detector.get_idle_seconds()
            detector.get_idle_seconds()
            # Only called once — second call short-circuits
            assert mock_run.call_count == 1

    def test_truncates_to_whole_seconds(self):
        """Milliseconds below 1000 round down to 0."""
        detector = IdleDetector()
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "999\n"

        with patch("attention_tracker.idle_detector.subprocess.run", return_value=mock_result):
            assert detector.get_idle_seconds() == 0

    def test_large_idle_value(self):
        """Large idle values convert correctly."""
        detector = IdleDetector()
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "360000\n"  # 6 minutes

        with patch("attention_tracker.idle_detector.subprocess.run", return_value=mock_result):
            assert detector.get_idle_seconds() == 360
