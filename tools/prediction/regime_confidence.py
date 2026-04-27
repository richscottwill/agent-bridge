"""
Regime confidence derivation — MPE v1.1 Slim (Phase 6.1.3b addendum)

=============================================================================
WHAT THIS DOES (Plain English)
=============================================================================
    Derives a per-regime "how much should the model trust this regime's
    lift" value (0.0-1.0) from ps.regime_fit_state.

    Before this module, the Brand trajectory had a single market-level
    `W_regime` weight (default 0.15) that the user had to pick. That's
    arbitrary. Every market was treated the same regardless of how well
    we understand its regimes.

    This module computes a confidence per regime using signals the
    weekly fitter already produces:
      - confidence (0.0-1.0)   — solver's self-reported trust
      - decay_status           — categorical tag (still-peaking, dormant, etc.)
      - n_post_weeks           — how much post-onset data fed the fit

    The Brand trajectory model then applies each regime's effective
    confidence individually. A dormant regime contributes almost nothing.
    A stable post-OCI regime contributes its full step-shift. A new,
    still-peaking regime contributes a fraction proportional to how
    confident the fit is.

=============================================================================
HOW IT WORKS
=============================================================================
    effective_confidence = fit_state.confidence × status_modifier

    status_modifier table (empirically defensible, adjust with data):
        dormant              → 0.10   # regime mostly decayed, don't double-count
        insufficient-data    → 0.20   # too early to trust
        still-peaking        → 0.60   # new regime, some uncertainty
        decaying-as-expected → 0.80   # fit aligned with authored guess
        decaying-faster      → 0.70   # model sees faster decay; trust slightly less
        decaying-slower      → 0.90   # model sees slower decay; trust slightly more
        no-decay-detected    → 1.00   # stable regime, full trust

    The global `regime_multiplier` (default 1.0) then scales everyone up
    or down. User can pass 0.5 to halve all regime contributions, or 2.0
    to aggressively weight them. Clamps final per-regime confidence to
    [0.0, 1.0].

=============================================================================
WHY THIS REMOVES HUMAN INPUT
=============================================================================
    Old UX: "pick W_regime 0.15–1.0 per projection."
    New UX: nothing to pick by default. Each regime gets its own
            data-driven confidence. A slider per regime exists for the
            rare override case, and a single multiplier slider exists for
            global "dial the whole stack" adjustments. Both default to
            auto.
=============================================================================
"""
from __future__ import annotations

from typing import Optional


# ---------- Status modifier table ----------

DECAY_STATUS_MODIFIERS: dict[str, float] = {
    "dormant": 0.10,
    "insufficient-data": 0.20,
    "still-peaking": 0.60,
    "decaying-faster": 0.70,
    "decaying-as-expected": 0.80,
    "decaying-slower": 0.90,
    "no-decay-detected": 1.00,
    # Bootstrap path: regime has no fit_state row yet. Treat cautiously.
    "no-fit-state": 0.30,
}


def effective_confidence(
    base_confidence: Optional[float],
    decay_status: Optional[str],
    regime_multiplier: float = 1.0,
) -> float:
    """Compute one regime's effective confidence for use as apply_weight input.

    Args:
        base_confidence: fit_state.confidence (0.0-1.0), None → treat as 0.3
            (bootstrap assumption, modest trust).
        decay_status: fit_state.decay_status, None → "no-fit-state".
        regime_multiplier: global dial, default 1.0. Passed through to all
            regimes; user can dial entire stack up or down.

    Returns:
        Float in [0.0, 1.0] suitable for apply_weight(raw_mult, weight).
    """
    base = float(base_confidence) if base_confidence is not None else 0.30
    modifier = DECAY_STATUS_MODIFIERS.get(decay_status or "no-fit-state", 0.30)
    raw = base * modifier * regime_multiplier
    # Clamp to [0, 1].
    return max(0.0, min(1.0, raw))


def describe_confidence(
    regime_id: str,
    change_date,
    description: Optional[str],
    base_confidence: Optional[float],
    decay_status: Optional[str],
    n_post_weeks: Optional[int],
    regime_multiplier: float = 1.0,
) -> dict:
    """Build a UI-facing dict describing a regime's confidence derivation.

    Used by the Phase 6.4 UI list-of-regimes display:

        "Polaris INTL MX — 2025-08-28 — conf 0.50 (no-decay-detected × 1.00)
         = 50% — 33 weeks of post-onset data"
    """
    eff = effective_confidence(base_confidence, decay_status, regime_multiplier)
    modifier = DECAY_STATUS_MODIFIERS.get(decay_status or "no-fit-state", 0.30)
    return {
        "regime_id": regime_id,
        "change_date": change_date.isoformat() if hasattr(change_date, "isoformat") else change_date,
        "description": (description or "")[:100],
        "base_confidence": base_confidence,
        "decay_status": decay_status,
        "status_modifier": modifier,
        "regime_multiplier": regime_multiplier,
        "effective_confidence": eff,
        "n_post_weeks": n_post_weeks,
        "explanation": (
            f"base={base_confidence or 0.30:.2f} × status_modifier={modifier:.2f} "
            f"× global_mult={regime_multiplier:.2f} = {eff:.2f}"
        ),
    }
