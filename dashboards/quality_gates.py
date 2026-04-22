#!/usr/bin/env python3
"""
quality_gates.py — Hard-gate rules for the WBR callout pipeline.

Three gates run after the callout reviewer scores but before a callout is
considered "ready to publish." Each gate produces a BLOCKED or PASSED status
per market with a reason. Override requires explicit confirmation.

Gates:
  A. Forecast miss > 30% for 3+ consecutive weeks → flag for manual review
  B. CPA deviation > 2x OP2 target → require explicit override
  C. Data staleness > 24h → block publish with warning

Design reference: .kiro/specs/dashboard-learnings-roadmap/design.md Item #3
Soul principle: Protect the habit loop — the pipeline shape doesn't change;
the quality floor rises.
"""
import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

HOME = Path.home()
FORECAST_JSON = HOME / "shared/dashboards/data/forecast-data.json"
COMMAND_CENTER_JSON = HOME / "shared/dashboards/data/command-center-data.json"

# ── Gate thresholds (configurable) ────────────────────────────────────
FORECAST_MISS_PCT = 30       # Gate A: forecast miss threshold (%)
FORECAST_MISS_WEEKS = 3      # Gate A: consecutive weeks required
CPA_DEVIATION_MULTIPLIER = 2 # Gate B: CPA must be < N× OP2 target
DATA_STALENESS_HOURS = 24    # Gate C: max hours before data is stale


class GateResult:
    """Result of a single gate check."""
    BLOCKED = "BLOCKED"
    PASSED = "PASSED"

    def __init__(self, gate_id, gate_name, status, market, reason="", details=None):
        self.gate_id = gate_id
        self.gate_name = gate_name
        self.status = status
        self.market = market
        self.reason = reason
        self.details = details or {}

    def to_dict(self):
        return {
            "gate_id": self.gate_id,
            "gate_name": self.gate_name,
            "status": self.status,
            "market": self.market,
            "reason": self.reason,
            "details": self.details,
            "override_required": self.status == self.BLOCKED,
        }


# ── Gate A: Forecast miss > 30% for 3+ consecutive weeks ─────────────
def check_forecast_miss(market, forecast, current_wk,
                        miss_pct=FORECAST_MISS_PCT,
                        miss_weeks=FORECAST_MISS_WEEKS):
    """
    Check if forecast miss exceeds threshold for N consecutive weeks.

    Compares predicted_value vs actual_value from forecast data.
    A "miss" is when |actual - predicted| / predicted > miss_pct%.

    Returns GateResult.
    """
    gate_id = "A"
    gate_name = "Forecast accuracy"

    # Try DuckDB forecasts table first via forecast_tracker in the forecast JSON
    weekly_rows = forecast.get("weekly", {}).get(market, [])
    if not weekly_rows:
        return GateResult(gate_id, gate_name, GateResult.PASSED, market,
                          reason="No forecast data available — gate skipped")

    # Build list of weeks with both predicted and actual values
    weeks_with_data = []
    for row in sorted(weekly_rows, key=lambda r: r.get("wk", 0)):
        wk = row.get("wk", 0)
        if wk < 1 or wk > current_wk:
            continue
        actual_regs = row.get("regs", 0)
        pred_regs = row.get("pred_regs")
        if actual_regs and actual_regs > 0 and pred_regs and pred_regs > 0:
            error_pct = abs(actual_regs - pred_regs) / pred_regs * 100
            weeks_with_data.append({
                "wk": wk,
                "actual": actual_regs,
                "predicted": pred_regs,
                "error_pct": round(error_pct, 1),
                "is_miss": error_pct > miss_pct,
            })

    if not weeks_with_data:
        return GateResult(gate_id, gate_name, GateResult.PASSED, market,
                          reason="No weeks with both actual and predicted data")

    # Check for N consecutive misses ending at or near current week
    # Walk backward from most recent week
    consecutive_misses = 0
    miss_streak = []
    for entry in reversed(weeks_with_data):
        if entry["is_miss"]:
            consecutive_misses += 1
            miss_streak.insert(0, entry)
        else:
            break

    if consecutive_misses >= miss_weeks:
        avg_error = sum(e["error_pct"] for e in miss_streak[-miss_weeks:]) / miss_weeks
        return GateResult(
            gate_id, gate_name, GateResult.BLOCKED, market,
            reason=(
                f"Forecast miss >{miss_pct}% for {consecutive_misses} consecutive "
                f"weeks (threshold: {miss_weeks}). Average error: {avg_error:.1f}%. "
                f"Manual review required before publish."
            ),
            details={
                "consecutive_misses": consecutive_misses,
                "threshold_weeks": miss_weeks,
                "threshold_pct": miss_pct,
                "avg_error_pct": round(avg_error, 1),
                "miss_weeks": [
                    {"wk": e["wk"], "actual": e["actual"],
                     "predicted": e["predicted"], "error_pct": e["error_pct"]}
                    for e in miss_streak[-miss_weeks:]
                ],
            },
        )

    return GateResult(gate_id, gate_name, GateResult.PASSED, market,
                      reason=f"Forecast accuracy within bounds ({consecutive_misses} consecutive misses, threshold: {miss_weeks})")


# ── Gate B: CPA deviation > 2× OP2 target ────────────────────────────
def check_cpa_deviation(market, forecast, current_wk, targets,
                        multiplier=CPA_DEVIATION_MULTIPLIER):
    """
    Check if current week CPA exceeds N× the OP2 target CPA.

    targets: dict with market → {cpa_target: float} or pulled from
    ps.targets / ps.market_constraints.

    Returns GateResult.
    """
    gate_id = "B"
    gate_name = "CPA deviation"

    # Get current week CPA from forecast data
    weekly_rows = forecast.get("weekly", {}).get(market, [])
    current_cpa = None
    for row in weekly_rows:
        if row.get("wk") == current_wk:
            current_cpa = row.get("cpa")
            break

    if current_cpa is None or current_cpa <= 0:
        return GateResult(gate_id, gate_name, GateResult.PASSED, market,
                          reason="No CPA data for current week — gate skipped")

    # Get OP2 target CPA
    target_cpa = targets.get(market, {}).get("cpa_target")
    if target_cpa is None or target_cpa <= 0:
        return GateResult(gate_id, gate_name, GateResult.PASSED, market,
                          reason="No OP2 CPA target available — gate skipped")

    threshold = target_cpa * multiplier
    if current_cpa > threshold:
        return GateResult(
            gate_id, gate_name, GateResult.BLOCKED, market,
            reason=(
                f"CPA ${current_cpa:.0f} exceeds {multiplier}× OP2 target "
                f"(${target_cpa:.0f} × {multiplier} = ${threshold:.0f}). "
                f"Explicit override required before publish."
            ),
            details={
                "current_cpa": round(current_cpa, 2),
                "target_cpa": round(target_cpa, 2),
                "multiplier": multiplier,
                "threshold_cpa": round(threshold, 2),
                "deviation_pct": round((current_cpa / target_cpa - 1) * 100, 1),
            },
        )

    return GateResult(gate_id, gate_name, GateResult.PASSED, market,
                      reason=f"CPA ${current_cpa:.0f} within {multiplier}× OP2 target ${target_cpa:.0f}")


# ── Gate C: Data staleness > 24h ─────────────────────────────────────
def check_data_staleness(market, staleness_hours=DATA_STALENESS_HOURS):
    """
    Check if the underlying data is stale (> N hours since last refresh).

    Checks:
    1. forecast-data.json generated timestamp
    2. command-center-data.json generated timestamp

    Returns GateResult.
    """
    gate_id = "C"
    gate_name = "Data freshness"

    now = datetime.now(tz=timezone.utc)
    stale_sources = []
    freshest_age_hours = 0

    for source_path, source_name in [
        (FORECAST_JSON, "forecast-data.json"),
        (COMMAND_CENTER_JSON, "command-center-data.json"),
    ]:
        if not source_path.exists():
            stale_sources.append({
                "source": source_name,
                "reason": "File not found",
                "age_hours": None,
            })
            continue

        try:
            data = json.loads(source_path.read_text())
            generated = data.get("generated")
            if not generated:
                # Fall back to file modification time
                mtime = datetime.fromtimestamp(
                    source_path.stat().st_mtime, tz=timezone.utc
                )
                age = now - mtime
            else:
                gen_dt = datetime.fromisoformat(generated)
                if gen_dt.tzinfo is None:
                    gen_dt = gen_dt.replace(tzinfo=timezone.utc)
                age = now - gen_dt

            age_hours = age.total_seconds() / 3600
            freshest_age_hours = max(freshest_age_hours, age_hours)

            if age_hours > staleness_hours:
                stale_sources.append({
                    "source": source_name,
                    "reason": f"Last updated {age_hours:.1f}h ago (threshold: {staleness_hours}h)",
                    "age_hours": round(age_hours, 1),
                })
        except (json.JSONDecodeError, OSError) as e:
            stale_sources.append({
                "source": source_name,
                "reason": f"Error reading file: {e}",
                "age_hours": None,
            })

    if stale_sources:
        reasons = "; ".join(
            f"{s['source']}: {s['reason']}" for s in stale_sources
        )
        return GateResult(
            gate_id, gate_name, GateResult.BLOCKED, market,
            reason=(
                f"Data staleness exceeds {staleness_hours}h threshold. "
                f"Stale sources: {reasons}. "
                f"Publish blocked — refresh data before proceeding."
            ),
            details={
                "threshold_hours": staleness_hours,
                "stale_sources": stale_sources,
                "max_age_hours": round(freshest_age_hours, 1),
            },
        )

    return GateResult(gate_id, gate_name, GateResult.PASSED, market,
                      reason=f"All data sources fresh (max age: {freshest_age_hours:.1f}h, threshold: {staleness_hours}h)")


# ── Orchestrator: run all gates for a market ──────────────────────────
def run_quality_gates(market, forecast, current_wk, targets):
    """
    Run all 3 quality gates for a single market.

    Args:
        market: Market code (e.g., "US", "AU", "MX")
        forecast: Loaded forecast-data.json dict
        current_wk: Current week number (int)
        targets: Dict of market → {cpa_target: float}

    Returns:
        list of GateResult dicts. If any gate is BLOCKED, the callout
        should not proceed to publish without explicit override.
    """
    results = [
        check_forecast_miss(market, forecast, current_wk),
        check_cpa_deviation(market, forecast, current_wk, targets),
        check_data_staleness(market),
    ]
    return [r.to_dict() for r in results]


def get_blocked_gates(gate_results):
    """Return only the BLOCKED gates from a list of gate results."""
    return [g for g in gate_results if g["status"] == GateResult.BLOCKED]


def is_publish_blocked(gate_results):
    """Return True if any gate is BLOCKED."""
    return any(g["status"] == GateResult.BLOCKED for g in gate_results)


def format_gate_summary(gate_results, market):
    """Format a human-readable summary of gate results for a market."""
    blocked = get_blocked_gates(gate_results)
    if not blocked:
        return f"✅ {market}: All quality gates PASSED — ready to publish."

    lines = [f"🚫 {market}: PUBLISH BLOCKED — {len(blocked)} gate(s) failed:"]
    for g in blocked:
        lines.append(f"  Gate {g['gate_id']} ({g['gate_name']}): {g['reason']}")
    lines.append("  → Override requires explicit confirmation.")
    return "\n".join(lines)


# ── Load OP2 targets from DuckDB or market_constraints ────────────────
def load_op2_targets_from_forecast(forecast):
    """
    Extract OP2 CPA targets from the forecast data structure.

    Falls back to computing CPA from monthly OP2 cost/regs if available
    in the market_constraints view data.
    """
    targets = {}
    # The forecast JSON doesn't directly contain OP2 targets, but
    # market_constraints has month_op2_cpa. We'll build targets from
    # what's available in the forecast structure.
    #
    # For now, return empty — the caller should provide targets from
    # DuckDB or the market_constraints view.
    return targets


def load_op2_targets_from_constraints(constraints_data):
    """
    Build targets dict from ps.market_constraints query results.

    constraints_data: list of dicts with keys: market, month_op2_cpa
    """
    targets = {}
    for row in constraints_data:
        market = row.get("market")
        cpa = row.get("month_op2_cpa")
        if market and cpa and cpa > 0:
            targets[market] = {"cpa_target": cpa}
    return targets
