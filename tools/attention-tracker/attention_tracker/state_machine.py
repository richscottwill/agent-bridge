"""Bayesian Attention State Machine.

Maintains a probability distribution over attention modes (FOCUSED, SWITCHING,
IDLE) and updates it via Bayesian inference on each classified event.
"""

from __future__ import annotations

from attention_tracker.models import (
    AttentionBeliefs,
    AttentionMode,
    AttentionState,
    ClassifiedEvent,
    TrackerConfig,
)


def _argmax_mode(beliefs: AttentionBeliefs) -> AttentionMode:
    """Return the mode with the highest belief probability."""
    pairs = [
        (beliefs.focused, AttentionMode.FOCUSED),
        (beliefs.switching, AttentionMode.SWITCHING),
        (beliefs.idle, AttentionMode.IDLE),
    ]
    return max(pairs, key=lambda p: p[0])[1]


def infer_mode_with_hysteresis(
    current_mode: AttentionMode,
    beliefs: AttentionBeliefs,
    config: TrackerConfig,
) -> AttentionMode:
    """Infer attention mode from beliefs using hysteresis.

    Higher threshold to ENTER a new mode than to MAINTAIN the current one.
    This prevents rapid oscillation at decision boundaries.

    Algorithm:
      1. If current mode's belief >= MAINTAIN_THRESHOLD, stay (sticky).
      2. Else if any mode exceeds ENTER_THRESHOLD, transition to it.
      3. Else fallback to argmax.
    """
    enter_threshold = config.enter_threshold        # 0.75
    maintain_threshold = config.maintain_threshold   # 0.40

    # Look up the belief for the current mode
    current_belief = {
        AttentionMode.FOCUSED: beliefs.focused,
        AttentionMode.SWITCHING: beliefs.switching,
        AttentionMode.IDLE: beliefs.idle,
    }[current_mode]

    # Sticky: maintain current mode if belief is still strong enough
    if current_belief >= maintain_threshold:
        return current_mode

    # Current mode lost confidence — check if any mode exceeds entry threshold
    if beliefs.focused >= enter_threshold:
        return AttentionMode.FOCUSED
    if beliefs.idle >= enter_threshold:
        return AttentionMode.IDLE
    if beliefs.switching >= enter_threshold:
        return AttentionMode.SWITCHING

    # No mode has strong enough signal — default to argmax
    return _argmax_mode(beliefs)


def bayesian_update(
    state: AttentionState,
    event: ClassifiedEvent,
    config: TrackerConfig,
) -> AttentionState:
    """Perform one Bayesian belief update given a new classified event.

    Follows the design pseudocode exactly:
      1. Compute evidence (category change, idle seconds, event duration)
      2. Compute likelihoods P(evidence | mode) for focused, switching, idle
      3. Posterior = prior × likelihood, then normalize
      4. Apply epsilon floor and re-normalize
      5. Infer mode (argmax placeholder; hysteresis added in task 3.2)
      6. Update focus duration
    """
    # --- Precondition: beliefs sum to ~1.0 ---
    assert abs(state.beliefs.sum() - 1.0) < 0.01, (
        f"Prior beliefs must sum to ~1.0, got {state.beliefs.sum()}"
    )

    # Step 1: Compute evidence from the event
    category_changed = event.category != state.current_category
    idle_sec = event.event.idle_seconds
    event_duration_ms = event.event.duration_ms

    # Step 2: Compute likelihoods P(evidence | mode)

    # --- Focused likelihood ---
    if idle_sec >= config.idle_threshold_seconds:
        likelihood_focused = 0.01
    elif category_changed:
        if event_duration_ms < config.micro_interruption_ms:
            likelihood_focused = 0.4   # brief glance, could still be focused
        else:
            likelihood_focused = 0.1   # sustained category change
    else:
        likelihood_focused = 0.9       # same category, not idle

    # --- Switching likelihood ---
    if idle_sec >= config.idle_threshold_seconds:
        likelihood_switching = 0.05
    elif category_changed:
        likelihood_switching = 0.8
    else:
        likelihood_switching = 0.2

    # --- Idle likelihood ---
    if idle_sec >= config.away_threshold_seconds:
        likelihood_idle = 0.99
    elif idle_sec >= config.idle_threshold_seconds:
        likelihood_idle = 0.9
    elif idle_sec >= 30:
        likelihood_idle = 0.3
    else:
        likelihood_idle = 0.05

    # Step 3: Bayesian posterior = prior × likelihood
    posterior_focused = state.beliefs.focused * likelihood_focused
    posterior_switching = state.beliefs.switching * likelihood_switching
    posterior_idle = state.beliefs.idle * likelihood_idle

    # Step 4: Normalize
    total = posterior_focused + posterior_switching + posterior_idle
    posterior_focused /= total
    posterior_switching /= total
    posterior_idle /= total

    # Step 5: Apply epsilon floor then re-normalize.
    # To guarantee no belief drops below epsilon after normalization,
    # we absorb the excess into the dominant belief rather than dividing
    # all three (which can push small values back below epsilon).
    epsilon = config.epsilon_floor
    posterior_focused = max(posterior_focused, epsilon)
    posterior_switching = max(posterior_switching, epsilon)
    posterior_idle = max(posterior_idle, epsilon)

    total = posterior_focused + posterior_switching + posterior_idle
    posterior_focused /= total
    posterior_switching /= total
    posterior_idle /= total

    # Clamp any value that drifted below epsilon due to normalization,
    # then redistribute the borrowed amount from the largest belief.
    beliefs_list = [posterior_focused, posterior_switching, posterior_idle]
    deficit = 0.0
    for i, b in enumerate(beliefs_list):
        if b < epsilon:
            deficit += epsilon - b
            beliefs_list[i] = epsilon
    if deficit > 0.0:
        max_idx = max(range(3), key=lambda i: beliefs_list[i])
        beliefs_list[max_idx] -= deficit
    posterior_focused, posterior_switching, posterior_idle = beliefs_list

    new_beliefs = AttentionBeliefs(
        focused=posterior_focused,
        switching=posterior_switching,
        idle=posterior_idle,
    )

    # Step 6: Infer mode with hysteresis
    new_mode = infer_mode_with_hysteresis(state.inferred_mode, new_beliefs, config)

    # Step 7: Update focus duration
    if new_mode == AttentionMode.FOCUSED:
        new_focus_duration = state.focus_duration_ms + event_duration_ms
    else:
        new_focus_duration = 0

    return AttentionState(
        beliefs=new_beliefs,
        inferred_mode=new_mode,
        since=event.event.timestamp if new_mode != state.inferred_mode else state.since,
        current_category=event.category,
        focus_duration_ms=new_focus_duration,
    )
