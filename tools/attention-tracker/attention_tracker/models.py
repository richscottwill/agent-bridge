"""Core data structures and enums for the Attention Tracker."""

from __future__ import annotations

import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AttentionMode(enum.Enum):
    """Discrete attention states inferred from Bayesian beliefs."""

    FOCUSED = "FOCUSED"
    SWITCHING = "SWITCHING"
    IDLE = "IDLE"


class MatchType(enum.Enum):
    """How a classification rule matches against an activity event."""

    WINDOW_CLASS = "WINDOW_CLASS"
    TITLE_PATTERN = "TITLE_PATTERN"
    URL_PATTERN = "URL_PATTERN"
    APP_NAME = "APP_NAME"


# ---------------------------------------------------------------------------
# Window / Browser primitives
# ---------------------------------------------------------------------------

@dataclass
class WindowInfo:
    """Snapshot of the currently active window."""

    pid: int
    window_class: str
    window_title: str
    timestamp: datetime


@dataclass
class TabInfo:
    """Browser tab context extracted from the active window."""

    title: str
    browser: str
    timestamp: datetime
    url: Optional[str] = None


# ---------------------------------------------------------------------------
# Activity events
# ---------------------------------------------------------------------------

@dataclass
class ActivityEvent:
    """A single activity observation from the polling loop."""

    id: str
    timestamp: datetime
    app_name: str
    window_class: str
    window_title: str
    idle_seconds: int
    duration_ms: int
    url: Optional[str] = None

    @staticmethod
    def new_id() -> str:
        """Generate a new UUID-based event id."""
        return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

@dataclass
class ClassificationRule:
    """A named rule that maps activity events to categories."""

    name: str
    match_type: MatchType
    pattern: str  # regex
    category: str
    productivity_score: float
    priority: int  # higher priority wins


@dataclass
class ClassifiedEvent:
    """An activity event after classification."""

    event: ActivityEvent
    category: str
    productivity_score: Optional[float]  # None for uncategorized
    rule_name: str


# ---------------------------------------------------------------------------
# Bayesian beliefs and attention state
# ---------------------------------------------------------------------------

@dataclass
class AttentionBeliefs:
    """Probability distribution over attention modes.

    Invariant: focused + switching + idle = 1.0 (within ±0.001).
    """

    focused: float
    switching: float
    idle: float

    def sum(self) -> float:
        """Return the sum of all beliefs."""
        return self.focused + self.switching + self.idle


@dataclass
class AttentionState:
    """Full attention state including beliefs, inferred mode, and tracking."""

    beliefs: AttentionBeliefs
    inferred_mode: AttentionMode
    since: datetime
    current_category: str
    focus_duration_ms: int


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class TrackerConfig:
    """Daemon configuration with sensible defaults from the design doc."""

    poll_interval_ms: int = 1500
    idle_threshold_seconds: int = 120
    away_threshold_seconds: int = 300
    db_path: str = "~/.local/share/attention-tracker/tracker.db"
    rules_path: str = "~/.config/attention-tracker/rules.toml"
    dashboard_port: int = 8787
    # Bayesian tuning
    enter_threshold: float = 0.75
    maintain_threshold: float = 0.40
    epsilon_floor: float = 0.01
    micro_interruption_ms: int = 15000


# ---------------------------------------------------------------------------
# Focus sessions and daily summaries
# ---------------------------------------------------------------------------

@dataclass
class FocusSession:
    """A contiguous period where inferred mode is FOCUSED."""

    id: str
    start_time: datetime
    category: str
    total_duration_ms: int = 0
    interruption_count: int = 0
    app_sequence: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = None


@dataclass
class DailySummary:
    """Aggregated attention metrics for a single calendar day."""

    date: str
    total_active_ms: int
    total_idle_ms: int
    focus_session_count: int
    avg_focus_duration_ms: int
    top_category: str
    category_breakdown: dict[str, int] = field(default_factory=dict)
    switch_count: int = 0
    productivity_score_avg: float = 0.0
    top_daily_insight: str = ""
