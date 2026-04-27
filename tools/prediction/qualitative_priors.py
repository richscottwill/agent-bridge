"""
qualitative_priors.py — Load + query the qualitative priors YAML catalog.

Phase 6.5.1. A thin loader around `qualitative_priors.yaml` that the engine
(or UI via its own YAML loader) can consult to turn a scenario name into
an engine-level scenario_override dict.

The YAML is the canonical catalog. Adding a scenario is yaml-only — no
Python code change. This module just reads the yaml and translates the
`trajectory_modifier` spec into the engine's native scenario_override.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

_CATALOG_CACHE: Optional[dict] = None
_CATALOG_PATH = Path(__file__).parent / "qualitative_priors.yaml"


def load_catalog(force_reload: bool = False) -> dict:
    """Load (and cache) the qualitative priors catalog from YAML.

    Returns:
        {"scenarios": [{name, description, trajectory_modifier, applicable_markets, ...}]}
    """
    global _CATALOG_CACHE
    if _CATALOG_CACHE is None or force_reload:
        if not _CATALOG_PATH.exists():
            _CATALOG_CACHE = {"scenarios": []}
        else:
            with _CATALOG_PATH.open("r") as f:
                _CATALOG_CACHE = yaml.safe_load(f) or {"scenarios": []}
    return _CATALOG_CACHE


def list_scenarios_for_market(market: str) -> list[dict]:
    """Return scenarios applicable to `market` (matches explicit market codes
    plus any scenario with `applicable_markets: ["*"]`).
    """
    cat = load_catalog()
    out = []
    for s in cat.get("scenarios", []):
        ams = s.get("applicable_markets", ["*"])
        if "*" in ams or market in ams:
            out.append(s)
    return out


def get_scenario(name: str) -> Optional[dict]:
    """Look up a scenario by name. Returns None if not found."""
    cat = load_catalog()
    for s in cat.get("scenarios", []):
        if s.get("name") == name:
            return s
    return None


def scenario_to_engine_override(scenario: dict, scenario_params: Optional[dict] = None) -> Optional[dict]:
    """Translate a YAML scenario entry into the engine's `scenario_override`
    dict format consumed by `project_brand_trajectory`.

    Supported trajectory_modifier types:
      - flat                  → None (engine default)
      - step_hold             → {half_life_weeks: None, force_confidence: 1.0}  (Bayesian-like)
      - exponential_decay     → {half_life_weeks: N, force_confidence: 1.0}
      - step_up               → user-specified onset+uplift — needs scenario_params
      - skip_regime_event     → {peak_multiplier: 1.0}  (neutralizes the regime)

    Returns None (= default engine behavior) if no effective override.
    """
    if not scenario:
        return None
    tm = scenario.get("trajectory_modifier") or {}
    t = tm.get("type")
    if t == "flat":
        return None
    if t == "step_hold":
        # Lift held at peak forever from anchor week
        return {"half_life_weeks": None, "force_confidence": 1.0}
    if t == "exponential_decay":
        hl = tm.get("half_life_weeks")
        return {"half_life_weeks": int(hl) if hl else None, "force_confidence": 1.0}
    if t == "step_up":
        # New placement landing. Engine's scenario_override doesn't natively
        # model a step-up, so callers should layer this as a multiplicative
        # factor post-projection. For v1.1 Slim we approximate by forcing
        # peak_multiplier to (1 + uplift_pct) and permanent sustain.
        params = scenario_params or {}
        uplift = params.get("uplift_pct", tm.get("uplift_pct", 0.15))
        if uplift:
            return {"peak_multiplier": 1.0 + float(uplift), "half_life_weeks": None, "force_confidence": 1.0}
        return None
    if t == "skip_regime_event":
        # Zero out regime influence — same as "No lift" chip
        return {"peak_multiplier": 1.0}
    return None


def w_qualitative_for(scenario_name: str) -> float:
    """Return the W_qualitative weight the engine should use when this
    scenario is explicitly selected.
    """
    s = get_scenario(scenario_name)
    if not s:
        return 0.05
    return float(s.get("w_qualitative_on_select", 0.20))


__all__ = [
    "load_catalog",
    "list_scenarios_for_market",
    "get_scenario",
    "scenario_to_engine_override",
    "w_qualitative_for",
]
