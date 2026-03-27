"""Unit tests for the Bayesian update algorithm in state_machine.py.

Covers:
- Belief normalization (sum to 1.0 after update)
- Epsilon floor (no belief below 0.01)
- Same category + no idle -> focused likelihood high
- Category change + short duration -> micro-interruption tolerance (0.4)
- Category change + long duration -> low focused likelihood (0.1)
- High idle -> idle likelihood dominates
- Determinism: same inputs -> same outputs
"""

from datetime import datetime, timedelta

import pytest

from attention_tracker.models import (
    ActivityEvent,
    AttentionBeliefs,
    AttentionMode,
    AttentionState,
    ClassifiedEvent,
    TrackerConfig,
)
from attention_tracker.state_machine import bayesian_update, infer_mode_with_hysteresis


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_state(
    focused: float = 0.33,
    switching: float = 0.33,
    idle: float = 0.34,
    mode: AttentionMode = AttentionMode.FOCUSED,
    category: str = "deep-work",
    focus_duration_ms: int = 0,
) -> AttentionState:
    return AttentionState(
        beliefs=AttentionBeliefs(focused=focused, switching=switching, idle=idle),
        inferred_mode=mode,
        since=datetime(2026, 1, 1, 9, 0, 0),
        current_category=category,
        focus_duration_ms=focus_duration_ms,
    )


def _make_event(
    category: str = "deep-work",
    idle_seconds: int = 0,
    duration_ms: int = 5000,
    ts: datetime | None = None,
) -> ClassifiedEvent:
    if ts is None:
        ts = datetime(2026, 1, 1, 9, 0, 5)
    return ClassifiedEvent(
        event=ActivityEvent(
            id="evt-1",
            timestamp=ts,
            app_name="code",
            window_class="Code",
            window_title="main.py — VS Code",
            idle_seconds=idle_seconds,
            duration_ms=duration_ms,
        ),
        category=category,
        productivity_score=0.9,
        rule_name="editor",
    )


CONFIG = TrackerConfig()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestBeliefNormalization:
    """After every update, beliefs must sum to 1.0 within tolerance."""

    def test_uniform_prior_same_category(self):
        state = _make_state()
        event = _make_event(category="deep-work")
        result = bayesian_update(state, event, CONFIG)
        assert abs(result.beliefs.sum() - 1.0) < 0.001

    def test_skewed_prior_category_change(self):
        state = _make_state(focused=0.8, switching=0.1, idle=0.1)
        event = _make_event(category="communication", duration_ms=20000)
        result = bayesian_update(state, event, CONFIG)
        assert abs(result.beliefs.sum() - 1.0) < 0.001

    def test_high_idle(self):
        state = _make_state(focused=0.1, switching=0.1, idle=0.8)
        event = _make_event(idle_seconds=300)
        result = bayesian_update(state, event, CONFIG)
        assert abs(result.beliefs.sum() - 1.0) < 0.001


class TestEpsilonFloor:
    """No belief should ever drop below epsilon (0.01)."""

    def test_focused_stays_above_epsilon_when_idle(self):
        """Even with strong idle evidence, focused belief >= epsilon."""
        state = _make_state(focused=0.05, switching=0.05, idle=0.90)
        event = _make_event(idle_seconds=300)
        result = bayesian_update(state, event, CONFIG)
        assert result.beliefs.focused >= CONFIG.epsilon_floor
        assert result.beliefs.switching >= CONFIG.epsilon_floor
        assert result.beliefs.idle >= CONFIG.epsilon_floor

    def test_idle_stays_above_epsilon_when_focused(self):
        """Even with strong focus evidence, idle belief >= epsilon."""
        state = _make_state(focused=0.90, switching=0.05, idle=0.05)
        event = _make_event(category="deep-work", idle_seconds=0)
        result = bayesian_update(state, event, CONFIG)
        assert result.beliefs.idle >= CONFIG.epsilon_floor


class TestSameCategoryNoIdle:
    """Same category + no idle -> focused likelihood high (0.9)."""

    def test_focused_belief_increases(self):
        state = _make_state(focused=0.33, switching=0.33, idle=0.34)
        event = _make_event(category="deep-work", idle_seconds=0)
        result = bayesian_update(state, event, CONFIG)
        # Focused should dominate after same-category, no-idle evidence
        assert result.beliefs.focused > result.beliefs.switching
        assert result.beliefs.focused > result.beliefs.idle

    def test_focused_mode_inferred(self):
        state = _make_state(focused=0.5, switching=0.3, idle=0.2)
        event = _make_event(category="deep-work", idle_seconds=0)
        result = bayesian_update(state, event, CONFIG)
        assert result.inferred_mode == AttentionMode.FOCUSED


class TestMicroInterruptionTolerance:
    """Category change + short duration -> focused likelihood 0.4 (not 0.1)."""

    def test_short_detour_preserves_some_focus(self):
        """A brief category change (< micro_interruption_ms) uses 0.4 likelihood."""
        state = _make_state(focused=0.7, switching=0.2, idle=0.1, category="deep-work")
        # Short duration (5s < 15s threshold), different category
        event = _make_event(category="communication", duration_ms=5000, idle_seconds=0)
        result = bayesian_update(state, event, CONFIG)
        # Focused belief should remain meaningful (not crushed to near-zero)
        assert result.beliefs.focused > 0.15

    def test_micro_interruption_vs_sustained_switch(self):
        """Micro-interruption should leave higher focused belief than sustained switch."""
        state = _make_state(focused=0.6, switching=0.2, idle=0.2, category="deep-work")
        short_event = _make_event(category="communication", duration_ms=5000, idle_seconds=0)
        long_event = _make_event(category="communication", duration_ms=20000, idle_seconds=0)

        result_short = bayesian_update(state, short_event, CONFIG)
        result_long = bayesian_update(state, long_event, CONFIG)

        assert result_short.beliefs.focused > result_long.beliefs.focused


class TestCategoryChangeLongDuration:
    """Category change + long duration -> low focused likelihood (0.1)."""

    def test_sustained_switch_reduces_focus(self):
        state = _make_state(focused=0.6, switching=0.2, idle=0.2, category="deep-work")
        event = _make_event(category="communication", duration_ms=20000, idle_seconds=0)
        result = bayesian_update(state, event, CONFIG)
        # Switching should dominate after sustained category change
        assert result.beliefs.switching > result.beliefs.focused


class TestHighIdleDominates:
    """High idle seconds -> idle likelihood dominates."""

    def test_away_threshold_makes_idle_dominant(self):
        state = _make_state(focused=0.33, switching=0.33, idle=0.34)
        event = _make_event(idle_seconds=300)  # >= away_threshold_seconds
        result = bayesian_update(state, event, CONFIG)
        assert result.beliefs.idle > result.beliefs.focused
        assert result.beliefs.idle > result.beliefs.switching
        assert result.inferred_mode == AttentionMode.IDLE

    def test_idle_threshold_boosts_idle(self):
        state = _make_state(focused=0.33, switching=0.33, idle=0.34)
        event = _make_event(idle_seconds=120)  # == idle_threshold_seconds
        result = bayesian_update(state, event, CONFIG)
        assert result.beliefs.idle > result.beliefs.focused


class TestDeterminism:
    """Same inputs must always produce the same outputs."""

    def test_identical_runs_produce_identical_results(self):
        state = _make_state(focused=0.5, switching=0.3, idle=0.2)
        event = _make_event(category="communication", duration_ms=10000, idle_seconds=5)

        result1 = bayesian_update(state, event, CONFIG)
        result2 = bayesian_update(state, event, CONFIG)

        assert result1.beliefs.focused == result2.beliefs.focused
        assert result1.beliefs.switching == result2.beliefs.switching
        assert result1.beliefs.idle == result2.beliefs.idle
        assert result1.inferred_mode == result2.inferred_mode
        assert result1.focus_duration_ms == result2.focus_duration_ms


class TestFocusDurationTracking:
    """Focus duration increments while FOCUSED, resets otherwise."""

    def test_focus_duration_increments(self):
        state = _make_state(
            focused=0.8, switching=0.1, idle=0.1,
            mode=AttentionMode.FOCUSED,
            focus_duration_ms=30000,
        )
        event = _make_event(category="deep-work", duration_ms=5000, idle_seconds=0)
        result = bayesian_update(state, event, CONFIG)
        if result.inferred_mode == AttentionMode.FOCUSED:
            assert result.focus_duration_ms == 35000

    def test_focus_duration_resets_on_mode_change(self):
        state = _make_state(
            focused=0.2, switching=0.6, idle=0.2,
            mode=AttentionMode.FOCUSED,
            focus_duration_ms=60000,
            category="deep-work",
        )
        # Strong switching evidence
        event = _make_event(category="communication", duration_ms=20000, idle_seconds=0)
        result = bayesian_update(state, event, CONFIG)
        if result.inferred_mode != AttentionMode.FOCUSED:
            assert result.focus_duration_ms == 0


class TestSinceTimestamp:
    """The 'since' field updates only when mode changes."""

    def test_since_unchanged_when_mode_stays(self):
        original_since = datetime(2026, 1, 1, 9, 0, 0)
        state = _make_state(focused=0.8, switching=0.1, idle=0.1)
        state.since = original_since
        event = _make_event(category="deep-work", idle_seconds=0)
        result = bayesian_update(state, event, CONFIG)
        if result.inferred_mode == state.inferred_mode:
            assert result.since == original_since

    def test_since_updates_when_mode_changes(self):
        state = _make_state(
            focused=0.2, switching=0.6, idle=0.2,
            mode=AttentionMode.FOCUSED,
            category="deep-work",
        )
        event_ts = datetime(2026, 1, 1, 9, 5, 0)
        event = _make_event(category="communication", duration_ms=20000, ts=event_ts)
        result = bayesian_update(state, event, CONFIG)
        if result.inferred_mode != AttentionMode.FOCUSED:
            assert result.since == event_ts


# ---------------------------------------------------------------------------
# Hysteresis Mode Inference Tests (Task 3.2)
# ---------------------------------------------------------------------------

class TestHysteresisCurrentModePreserved:
    """Req 5.1: Current mode preserved when belief >= MAINTAIN_THRESHOLD (0.40)."""

    def test_focused_maintained_at_threshold(self):
        """Exactly at MAINTAIN_THRESHOLD (0.40) — mode should be preserved."""
        beliefs = AttentionBeliefs(focused=0.40, switching=0.35, idle=0.25)
        result = infer_mode_with_hysteresis(AttentionMode.FOCUSED, beliefs, CONFIG)
        assert result == AttentionMode.FOCUSED

    def test_focused_maintained_above_threshold(self):
        beliefs = AttentionBeliefs(focused=0.50, switching=0.30, idle=0.20)
        result = infer_mode_with_hysteresis(AttentionMode.FOCUSED, beliefs, CONFIG)
        assert result == AttentionMode.FOCUSED

    def test_switching_maintained_at_threshold(self):
        beliefs = AttentionBeliefs(focused=0.35, switching=0.40, idle=0.25)
        result = infer_mode_with_hysteresis(AttentionMode.SWITCHING, beliefs, CONFIG)
        assert result == AttentionMode.SWITCHING

    def test_idle_maintained_above_threshold(self):
        beliefs = AttentionBeliefs(focused=0.20, switching=0.20, idle=0.60)
        result = infer_mode_with_hysteresis(AttentionMode.IDLE, beliefs, CONFIG)
        assert result == AttentionMode.IDLE

    def test_focused_maintained_even_when_not_argmax(self):
        """Current mode preserved even if another mode has higher belief,
        as long as current >= MAINTAIN_THRESHOLD."""
        beliefs = AttentionBeliefs(focused=0.40, switching=0.45, idle=0.15)
        result = infer_mode_with_hysteresis(AttentionMode.FOCUSED, beliefs, CONFIG)
        assert result == AttentionMode.FOCUSED


class TestHysteresisTransition:
    """Req 5.2: Mode transitions when current drops below MAINTAIN
    and another exceeds ENTER_THRESHOLD (0.75)."""

    def test_transition_to_focused(self):
        beliefs = AttentionBeliefs(focused=0.80, switching=0.10, idle=0.10)
        result = infer_mode_with_hysteresis(AttentionMode.SWITCHING, beliefs, CONFIG)
        assert result == AttentionMode.FOCUSED

    def test_transition_to_idle(self):
        beliefs = AttentionBeliefs(focused=0.10, switching=0.10, idle=0.80)
        result = infer_mode_with_hysteresis(AttentionMode.FOCUSED, beliefs, CONFIG)
        assert result == AttentionMode.IDLE

    def test_transition_to_switching(self):
        beliefs = AttentionBeliefs(focused=0.10, switching=0.80, idle=0.10)
        result = infer_mode_with_hysteresis(AttentionMode.IDLE, beliefs, CONFIG)
        assert result == AttentionMode.SWITCHING

    def test_no_transition_when_current_above_maintain(self):
        """Even if another mode exceeds ENTER, current stays if >= MAINTAIN."""
        beliefs = AttentionBeliefs(focused=0.40, switching=0.10, idle=0.50)
        result = infer_mode_with_hysteresis(AttentionMode.FOCUSED, beliefs, CONFIG)
        assert result == AttentionMode.FOCUSED


class TestHysteresisArgmaxFallback:
    """Req 5.3: Argmax fallback when no mode exceeds ENTER_THRESHOLD."""

    def test_argmax_when_no_mode_exceeds_enter(self):
        """Current below MAINTAIN, no mode above ENTER — pick highest."""
        beliefs = AttentionBeliefs(focused=0.50, switching=0.30, idle=0.20)
        result = infer_mode_with_hysteresis(AttentionMode.IDLE, beliefs, CONFIG)
        assert result == AttentionMode.FOCUSED

    def test_argmax_picks_switching(self):
        beliefs = AttentionBeliefs(focused=0.20, switching=0.50, idle=0.30)
        result = infer_mode_with_hysteresis(AttentionMode.FOCUSED, beliefs, CONFIG)
        assert result == AttentionMode.SWITCHING

    def test_argmax_picks_idle(self):
        beliefs = AttentionBeliefs(focused=0.20, switching=0.10, idle=0.70)
        result = infer_mode_with_hysteresis(AttentionMode.FOCUSED, beliefs, CONFIG)
        assert result == AttentionMode.IDLE


class TestHysteresisThresholdInvariant:
    """Req 5.4: ENTER_THRESHOLD > MAINTAIN_THRESHOLD invariant."""

    def test_default_config_invariant(self):
        assert CONFIG.enter_threshold > CONFIG.maintain_threshold

    def test_enter_is_075_maintain_is_040(self):
        assert CONFIG.enter_threshold == 0.75
        assert CONFIG.maintain_threshold == 0.40


class TestHysteresisStabilityUnderContradiction:
    """Req 5.1: Single contradictory event doesn't flip mode
    when current belief is strong."""

    def test_focused_survives_single_category_change(self):
        """Start strongly focused, send one switching-evidence event.
        Mode should remain FOCUSED due to hysteresis."""
        state = _make_state(
            focused=0.80, switching=0.10, idle=0.10,
            mode=AttentionMode.FOCUSED,
            category="deep-work",
        )
        # One contradictory event: category change, long duration
        event = _make_event(category="communication", duration_ms=20000, idle_seconds=0)
        result = bayesian_update(state, event, CONFIG)
        assert result.inferred_mode == AttentionMode.FOCUSED

    def test_idle_survives_single_active_event(self):
        """Start strongly idle, send one active event.
        Mode should remain IDLE due to hysteresis."""
        state = _make_state(
            focused=0.05, switching=0.05, idle=0.90,
            mode=AttentionMode.IDLE,
            category="deep-work",
        )
        event = _make_event(category="deep-work", idle_seconds=0, duration_ms=5000)
        result = bayesian_update(state, event, CONFIG)
        assert result.inferred_mode == AttentionMode.IDLE
