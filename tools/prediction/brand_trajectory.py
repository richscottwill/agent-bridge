"""
Brand Trajectory Model — MPE v1.1 Slim (Phase 6.1.1)

=============================================================================
WHAT THIS DOES (Plain English)
=============================================================================
    Projects Brand registrations and Brand spend for a market over a list of
    weeks, using three independent evidence streams blended with explicit
    weights. This is the "Brand-Anchor" half of v1.1 Slim's architecture.

    Unlike v1, Brand is projected INDEPENDENTLY of any target (ie%CCP, regs,
    spend). The Brand trajectory is what it is — trend, seasonality, and
    regime-level shifts are all properties of Brand itself. The NB-Residual
    solver (nb_residual_solver.py) takes the Brand projection as given and
    moves NB spend to hit the target.

    Every projection returns a `contribution_breakdown` dict that lets the
    owner see WHICH evidence stream drove the answer — "Brand W22 = 1,038
    regs: 40% seasonal, 40% trend, 15% regime." This makes the model
    auditable rather than opaque.

=============================================================================
HOW IT WORKS
=============================================================================
    Three evidence streams combine multiplicatively with named weights:

    brand_regs[w] = annual_baseline
                  × seasonal_multiplier[w]   × W_seasonal   (default 0.40)
                  × recent_trend_multiplier  × W_trend      (default 0.40)
                  × regime_multiplier        × W_regime     (default 0.15)

    Weights sum to 0.95 in Phase 6.1 — the remaining 0.05 is reserved for
    the qualitative-priors stream that ships in Phase 6.5. Reserving the
    slot now means Phase 6.5 is a drop-in addition, not a weight re-balance.

    The multiplicative blend is applied as a log-space weighted sum:
        log(mult[w]) = W_s·log(s[w]) + W_t·log(t) + W_r·log(r)
    so each stream scales the others rather than adding-then-clipping.

    Brand CPA is a scalar per regime segment (rolling 8-week median of
    actuals). Not an elasticity curve — Brand CPA has never shown meaningful
    responsiveness to Brand spend in the ranges we operate in.

=============================================================================
HOW IT CAN FAIL (and what happens)
=============================================================================
    1. Missing seasonality data (<52 weeks of history)
       → Falls back to flat seasonal=1.0, emits SEASONAL_PRIOR_UNAVAILABLE
          warning in the BrandProjection.
    2. No recent trend (<4 weeks since latest regime event)
       → Falls back to trend=1.0 (no slope), emits TREND_INSUFFICIENT_DATA.
    3. No structural regime rows in ps.regime_changes
       → regime multiplier defaults to 1.0 (neutral).
    4. Null-CCP market (AU)
       → Fully supported. Brand projection is independent of CCPs.
    5. Market not in ps.v_weekly or 0 Brand weeks available
       → Returns BrandProjection with regs=0, spend=0, warning=NO_DATA.
          Caller (mpe_engine) surfaces this as SETUP_REQUIRED.
=============================================================================
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

import numpy as np

# Reuse fitting module's DB connection + data-fetcher to keep a single
# read path. This also means regime filtering rules are centralized there.
from prediction.mpe_fitting import _db as _fitting_db
from prediction.mpe_fitting import _fetch_weekly, _recency_weights

# ---------- Defaults ----------

DEFAULT_WEIGHTS = {
    "seasonal": 0.40,
    "trend": 0.40,
    "regime": 0.15,
    "qualitative": 0.05,  # reserved for Phase 6.5; read but not applied in 6.1
}

# Half-life for recency weighting of trend fit. Tighter than seasonality
# (which uses 52w half-life) because trend tracks the CURRENT regime.
TREND_HALF_LIFE_WEEKS = 4

# Minimum weeks post-latest-structural-regime before we will fit a trend.
# Below this, slope is noisy and we return intercept-only with a warning.
TREND_MIN_WEEKS = 4
# Max weeks of history used for trend fit (cap so trend stays recent).
TREND_MAX_WEEKS = 16

# Recent-actuals anchor window — last N weeks of YTD data feed the anchor.
# 2026-04-26 rework: anchor now reflects WHERE WE ARE (with all regime lifts
# already baked in), not a pre-regime baseline. Regime stream describes
# forward evolution relative to today, not a correction from an old level.
# 8 weeks picked to balance: long enough to average out single-week noise,
# short enough that active-campaign lifts (like Sparkle W14→W17 at MX) are
# reflected rather than diluted.
ANCHOR_RECENT_WEEKS = 8

# Weeks after which the fitted trend fades to 50% of its initial effect.
# Prevents naive extrapolation of a 16-week ramp out to +51x annual growth.
# Empirically: Sparkle-era MX had a 16w ramp that decays inside 26w; setting
# TREND_FADE_HALF_LIFE at the same scale means the trend is still the
# dominant "where are we now" signal but doesn't obliterate seasonality.
TREND_FADE_HALF_LIFE_WEEKS = 13

# Minimum history for seasonality fit — 1 full year needed to form a shape.
SEASONALITY_MIN_WEEKS = 52

# Brand CPA rolling median window (weeks).
BRAND_CPA_MEDIAN_WEEKS = 8


# ---------- Result type ----------


@dataclass
class BrandProjection:
    """Per-week Brand regs + per-week Brand spend, with contribution breakdown.

    weeks: list of period_start dates in order
    regs_per_week: same length as `weeks`
    spend_per_week: same length as `weeks`
    brand_cpa_used: the scalar CPA used to compute spend from regs
    contribution: weight-normalized dict {'seasonal': 0.40, 'trend': 0.40, ...}
    stream_multipliers_per_week: optional debug detail per week per stream
    warnings: list of string codes
    lineage: free-text description of fit sources (for UI provenance)
    """
    market: str
    weeks: list[date]
    regs_per_week: list[float]
    spend_per_week: list[float]
    brand_cpa_used: float
    contribution: dict[str, float]
    stream_multipliers_per_week: list[dict[str, float]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    lineage: str = ""

    @property
    def total_regs(self) -> float:
        return float(sum(self.regs_per_week))

    @property
    def total_spend(self) -> float:
        return float(sum(self.spend_per_week))

    def to_json(self) -> dict:
        return {
            "market": self.market,
            "weeks": [w.isoformat() for w in self.weeks],
            "regs_per_week": self.regs_per_week,
            "spend_per_week": self.spend_per_week,
            "brand_cpa_used": self.brand_cpa_used,
            "contribution": self.contribution,
            "total_regs": self.total_regs,
            "total_spend": self.total_spend,
            "warnings": self.warnings,
            "lineage": self.lineage,
        }


# ---------- Seasonality stream ----------


def compute_seasonal_multipliers(market: str, target_weeks: list[date]) -> tuple[dict[int, float], list[str]]:
    """Return {iso_week: multiplier} for target weeks + any warnings.

    Multiplier is relative to the market's annual mean Brand regs — so a
    seasonal=1.10 means "this ISO week typically runs 10% above annual mean."

    Architecture (updated 2026-04-23 Phase 6.2.x per-year normalization fix):
      1. Group Brand history by ISO year.
      2. For each year, compute year-level mean and express each week as
         multiplier vs that year's mean (NOT the all-years mean).
      3. Average the per-year multipliers across years.

    This removes regime-level-shift contamination. Previously a Sparkle
    year with 4× Brand volume would push W15's aggregate multiplier up
    by ~1 SD even though W15 seasonality in normal years is flat. Now
    Sparkle 2026's W15 is expressed as 1.7× of Sparkle's own 2026 mean
    (which might actually be low-normal for Sparkle year) before
    averaging with pre-Sparkle years.

    Clamps multipliers to [0.3, 3.0]. Flags high-CV weeks (YoY instability
    >50%) via SEASONAL_WEEK_UNSTABLE warnings — caller can decide whether
    to downweight or report honestly.
    """
    warnings: list[str] = []
    rows = _fetch_weekly(market, "brand", regime_filter=True, include_pre_structural=True)
    if len(rows) < SEASONALITY_MIN_WEEKS:
        warnings.append(f"SEASONAL_PRIOR_UNAVAILABLE ({len(rows)} weeks < {SEASONALITY_MIN_WEEKS})")
        return {iso_week_of(w): 1.0 for w in target_weeks}, warnings

    # Group by (iso_year, iso_week). iso_year handles the year-boundary edge
    # case where W52/W53 of year N vs W1 of year N+1 sit near Dec 31 / Jan 1.
    from collections import defaultdict
    by_year_week: dict[int, dict[int, float]] = defaultdict(dict)
    for r in rows:
        iso_year, iso_w, _ = r["period_start"].isocalendar()
        if iso_w == 53:
            iso_w = 52
        # If W52 already populated for this year (e.g. a partial W53), skip.
        if iso_w in by_year_week[iso_year]:
            # Average with existing (handles rare W53 collapse).
            by_year_week[iso_year][iso_w] = (by_year_week[iso_year][iso_w] + r["regs"]) / 2
        else:
            by_year_week[iso_year][iso_w] = r["regs"]

    # Compute per-year mean; skip years with too few weeks to be meaningful.
    MIN_WEEKS_PER_YEAR = 26  # half a year — noise below this
    per_year_mults: dict[int, dict[int, float]] = {}
    for year, week_map in by_year_week.items():
        if len(week_map) < MIN_WEEKS_PER_YEAR:
            continue
        year_mean = float(np.mean(list(week_map.values())))
        if year_mean <= 0:
            continue
        per_year_mults[year] = {
            w: max(0.3, min(3.0, v / year_mean)) for w, v in week_map.items()
        }

    if not per_year_mults:
        warnings.append("SEASONAL_PRIOR_UNAVAILABLE (no year with >= 26 weeks)")
        return {iso_week_of(w): 1.0 for w in target_weeks}, warnings

    # Average per-year multipliers across years.
    week_mults: dict[int, float] = {}
    week_yoy_cv: dict[int, float] = {}
    import statistics
    for iso_w in range(1, 53):
        values = [m[iso_w] for m in per_year_mults.values() if iso_w in m]
        if not values:
            continue
        week_mults[iso_w] = float(np.mean(values))
        if len(values) >= 2:
            mean_v = week_mults[iso_w]
            stdev_v = statistics.stdev(values) if len(values) > 1 else 0.0
            cv = stdev_v / mean_v if mean_v > 0 else 0.0
            week_yoy_cv[iso_w] = cv
            if cv > 0.50:
                warnings.append(
                    f"SEASONAL_WEEK_UNSTABLE: W{iso_w:02d} YoY CV {cv*100:.0f}% "
                    f"(n={len(values)} years, per-year mults {values})"
                )

    # For any target week with no historical data, default to 1.0.
    result: dict[int, float] = {}
    for w in target_weeks:
        iso_w = iso_week_of(w)
        if iso_w == 53:
            iso_w = 52
        result[iso_week_of(w)] = week_mults.get(iso_w, 1.0)

    return result, warnings


def iso_week_of(d: date) -> int:
    """Return 1-53 ISO week number for a date."""
    return d.isocalendar()[1]


# ---------- Recent trend stream ----------


def compute_recent_trend(market: str) -> tuple[dict, list[str]]:
    """Fit intercept + slope to recent Brand regs in log space.

    2026-04-26 rework (anchor semantics): intercept is now RECENT actuals
    (last ANCHOR_RECENT_WEEKS weeks of clean YTD data), NOT a pre-regime
    baseline. This means:

    - anchor × 1.0 = where we are TODAY (with all active regimes baked in)
    - regime stream describes forward EVOLUTION (how the lift decays or
      persists from this week onward, relative to today)

    Previously: intercept was "pre-first-regime 8-week mean" and the regime
    stream had to LIFT from that stale level. Problem: when fit confidence
    was low (e.g. Sparkle 0.18 effective), the 1.87× peak only applied as
    1.16× at the current-week projection — producing a visible cliff when
    actuals were ~400 regs but the model said ~130.

    New semantics: anchor IS the observed recent level. Regime stream only
    describes future deviation (decay toward baseline, persistence at peak,
    etc.), not correction from a pre-regime level.

    Returns a dict with:
        'intercept': recent-actuals mean (ANCHOR_RECENT_WEEKS weeks, clean YTD)
        'intercept_source': 'recent_actuals' | 'pre_regime_fallback' | 'full_history_fallback'
        'slope_log': weekly log-linear growth rate, fit on post-regime data
        'n_weeks_used': how many weeks fed the slope fit
        'latest_week': date of most recent week used

    Plus warnings list.

    Slope is log-space so a slope of 0.01 = ~1%/wk compounding growth.
    """
    warnings: list[str] = []
    con = _fitting_db()

    # Identify earliest structural regime for slope-fit window (not anchor).
    earliest_struct = con.execute("""
        SELECT CAST(MIN(change_date) AS DATE)
        FROM ps.regime_changes
        WHERE market = ? AND is_structural_baseline = TRUE AND active = TRUE
    """, [market]).fetchone()
    cutoff_date = earliest_struct[0] if earliest_struct and earliest_struct[0] else None

    # Full history (regime_filter still excludes reverted windows).
    all_rows = _fetch_weekly(market, "brand", regime_filter=True, include_pre_structural=True)

    # Post-earliest-regime rows — trend SLOPE fit still operates on post-regime data.
    if cutoff_date is not None:
        recent = [r for r in all_rows if r["period_start"] >= cutoff_date]
    else:
        recent = all_rows[-TREND_MAX_WEEKS:] if len(all_rows) >= TREND_MIN_WEEKS else all_rows
    if len(recent) > TREND_MAX_WEEKS:
        recent = recent[-TREND_MAX_WEEKS:]

    # ANCHOR (intercept): recent-actuals mean from last ANCHOR_RECENT_WEEKS
    # weeks of clean YTD data. This is the Bayesian-natural level: observed
    # data speaks louder than old priors. The anchor implicitly contains
    # whatever regime lifts are currently active — we don't subtract them
    # out anymore.
    #
    # 2026-04-26 fix: if the LATEST structural regime started recently,
    # clip the window to post-onset weeks only. Otherwise the anchor
    # averages pre-regime and post-regime together and dilutes the current
    # campaign lift (the "MX W15–W17 cliff" symptom — Sparkle stepped
    # Brand from 200 → 400 at W14, but averaging W8–W15 produced ~250).
    latest_struct = con.execute("""
        SELECT CAST(MAX(change_date) AS DATE)
        FROM ps.regime_changes
        WHERE market = ? AND is_structural_baseline = TRUE AND active = TRUE
    """, [market]).fetchone()
    latest_onset = latest_struct[0] if latest_struct and latest_struct[0] else None

    # Start with the standard last-N-week window
    anchor_window = all_rows[-ANCHOR_RECENT_WEEKS:] if len(all_rows) >= ANCHOR_RECENT_WEEKS else all_rows

    anchor_clip_note = None
    if latest_onset is not None:
        post_onset = [r for r in all_rows if r["period_start"] >= latest_onset]
        # Clip if the latest onset is RECENT (falls within the default anchor window)
        # AND we have at least 2 post-onset weeks. 2 weeks is noisy but far better
        # than averaging 6 pre-onset weeks at the wrong level.
        ANCHOR_POST_ONSET_MIN = 2
        window_oldest = anchor_window[0]["period_start"] if anchor_window else None
        onset_is_recent = window_oldest is None or latest_onset >= window_oldest
        if onset_is_recent and len(post_onset) >= ANCHOR_POST_ONSET_MIN and len(post_onset) < len(anchor_window):
            anchor_window = post_onset
            anchor_clip_note = (
                f"ANCHOR_CLIPPED_POST_REGIME (latest onset {latest_onset}, "
                f"{len(post_onset)} post-onset weeks in window)"
            )
            warnings.append(anchor_clip_note)

    anchor_regs = [r["regs"] for r in anchor_window if r["regs"] > 0]
    if anchor_regs:
        intercept = float(np.mean(anchor_regs))
        intercept_source = "recent_actuals_post_regime" if anchor_clip_note else "recent_actuals"
    elif cutoff_date is not None:
        # Fallback: pre-regime window (old behavior) if recent window is empty/zero
        pre_rows = [r for r in all_rows if r["period_start"] < cutoff_date]
        pre_window = pre_rows[-ANCHOR_RECENT_WEEKS:] if len(pre_rows) >= ANCHOR_RECENT_WEEKS else pre_rows
        if pre_window:
            intercept = float(np.mean([r["regs"] for r in pre_window]))
            intercept_source = "pre_regime_fallback"
            warnings.append("ANCHOR_FELL_BACK_TO_PRE_REGIME (recent window was empty)")
        else:
            intercept = float(np.mean([r["regs"] for r in all_rows])) if all_rows else 0.0
            intercept_source = "full_history_fallback"
            warnings.append("ANCHOR_FELL_BACK_TO_FULL_HISTORY")
    else:
        intercept = float(np.mean([r["regs"] for r in all_rows])) if all_rows else 0.0
        intercept_source = "full_history_fallback"

    if len(recent) < TREND_MIN_WEEKS:
        warnings.append(f"TREND_INSUFFICIENT_DATA ({len(recent)} weeks < {TREND_MIN_WEEKS})")
        return {
            "intercept": intercept,
            "intercept_source": intercept_source,
            "slope_log": 0.0,
            "n_weeks_used": len(recent),
            "latest_week": recent[-1]["period_start"] if recent else (all_rows[-1]["period_start"] if all_rows else None),
        }, warnings

    # Weighted log-linear fit: log(regs) = a + b × week_index
    regs = np.array([r["regs"] for r in recent])
    ages = np.array([r["age_weeks"] for r in recent])
    # Age is "weeks from latest" — we want week_index increasing with time.
    week_idx = ages.max() - ages
    weights = _recency_weights(ages, half_life=TREND_HALF_LIFE_WEEKS)

    mask = (regs > 0) & np.isfinite(regs)
    if mask.sum() < TREND_MIN_WEEKS:
        warnings.append("TREND_INSUFFICIENT_DATA (non-zero mask)")
        return {
            "intercept": intercept,
            "intercept_source": intercept_source,
            "slope_log": 0.0,
            "n_weeks_used": len(recent),
            "latest_week": recent[-1]["period_start"],
        }, warnings

    log_regs = np.log(regs[mask])
    x = week_idx[mask].astype(float)
    w = weights[mask]
    # Weighted OLS on [1, week_idx] vs log_regs.
    X = np.column_stack([np.ones_like(x), x])
    W = np.diag(w)
    try:
        beta = np.linalg.solve(X.T @ W @ X, X.T @ W @ log_regs)
        slope_log = float(beta[1])
    except np.linalg.LinAlgError:
        warnings.append("TREND_SLOPE_UNSTABLE")
        slope_log = 0.0

    # Sanity clamp: weekly growth outside ±10% is suspicious.
    if abs(slope_log) > 0.10:
        warnings.append(f"TREND_SLOPE_CLAMPED (raw={slope_log:+.3f}, clamped to ±0.10)")
        slope_log = max(-0.10, min(0.10, slope_log))

    return {
        "intercept": intercept,
        "intercept_source": intercept_source,
        "slope_log": slope_log,
        "n_weeks_used": len(recent),
        "latest_week": recent[-1]["period_start"],
    }, warnings


def trend_multiplier_for_week(trend: dict, target_week: date) -> float:
    """Apply the trend slope forward from `latest_week` to `target_week`, with
    exponential fade so the trend's influence decays instead of compounding
    unchecked.

    Fade formula: effective_slope = slope × 0.5^(weeks_ahead / HALF_LIFE).
    The trend is the LOCAL direction of travel — it says nothing about what
    happens 6+ months forward. Fading it keeps seasonality + regime as the
    dominant long-horizon signals.
    """
    if trend.get("latest_week") is None or trend.get("slope_log", 0.0) == 0.0:
        return 1.0
    weeks_ahead = (target_week - trend["latest_week"]).days / 7.0
    if weeks_ahead <= 0:
        return 1.0

    slope = trend["slope_log"]
    # Integrate slope × 0.5^(t/H) from 0 to weeks_ahead.
    # Closed form: (slope × H / ln 2) × (1 - 0.5^(weeks_ahead/H))
    H = TREND_FADE_HALF_LIFE_WEEKS
    fade_integral = (slope * H / math.log(2)) * (1.0 - math.pow(0.5, weeks_ahead / H))
    return float(math.exp(fade_integral))


# ---------- Regime stream ----------


def _fetch_structural_regimes(market: str) -> list[dict]:
    """Load active structural baseline rows with their peak multipliers and
    decay profiles.

    Data flow:
      1. Prefer ps.regime_fit_state_current (weekly-fitted peak + decay).
      2. Fall back to inline before/after compute from ps.v_weekly when a
         regime has no fit_state row yet (bootstrap path).

    This three-layer separation — authored facts in ps.regime_changes,
    fitted state in ps.regime_fit_state, consumed here — lets the weekly
    refit hook (fit_regime_state.py) update peak/decay as data accumulates
    without mutating the authored rows.

    For each row:
        peak_multiplier = from fit_state.peak_multiplier (or inline fallback)
        half_life_weeks = fit_state.fitted_half_life_weeks IF sufficiently
            confident; else fall back to authored half_life_weeks

    Returns [{regime_id, change_date, peak_multiplier, half_life_weeks,
              description, warnings, decay_status, source}], ordered by
    change_date.
    """
    con = _fitting_db()
    # Left-join authored regime rows against the latest fit_state row so
    # we see both even when fit_state hasn't been populated yet.
    rows = con.execute("""
        SELECT
            rc.id,
            CAST(rc.change_date AS DATE) AS change_date,
            rc.description,
            rc.expected_impact_pct,
            rc.half_life_weeks                   AS authored_hl,
            fs.peak_multiplier                   AS fitted_peak,
            fs.fitted_half_life_weeks            AS fitted_hl,
            fs.current_multiplier                AS fitted_current,
            fs.decay_status                      AS decay_status,
            fs.confidence                        AS fit_confidence,
            fs.n_post_weeks                      AS n_post_weeks
        FROM ps.regime_changes rc
        LEFT JOIN ps.regime_fit_state_current fs ON fs.regime_id = rc.id
        WHERE rc.market = ? AND rc.is_structural_baseline = TRUE AND rc.active = TRUE
        ORDER BY rc.change_date ASC
    """, [market]).fetchall()

    result: list[dict] = []
    for (
        regime_id, change_date, description, expected_impact_pct,
        authored_hl, fitted_peak, fitted_hl, fitted_current,
        decay_status, fit_confidence, n_post_weeks,
    ) in rows:
        if change_date is None:
            continue
        row_warnings: list[str] = []
        source = "fitted" if fitted_peak is not None else "inline-bootstrap"

        # Peak multiplier: prefer fitted, fall back to inline before/after.
        if fitted_peak is not None:
            peak = float(fitted_peak)
            b_mean = float("nan")  # fit_state doesn't retain these; only for lineage
            a_mean = float("nan")
            raw_ratio = peak
        else:
            before = con.execute("""
                SELECT AVG(brand_registrations)
                FROM ps.v_weekly
                WHERE market = ? AND period_type = 'weekly'
                  AND period_start < ? AND period_start >= ?
                  AND brand_registrations IS NOT NULL AND brand_registrations > 0
            """, [market, change_date, change_date - timedelta(weeks=8)]).fetchone()
            after = con.execute("""
                SELECT AVG(brand_registrations)
                FROM ps.v_weekly
                WHERE market = ? AND period_type = 'weekly'
                  AND period_start >= ? AND period_start < ?
                  AND brand_registrations IS NOT NULL AND brand_registrations > 0
            """, [market, change_date, change_date + timedelta(weeks=8)]).fetchone()

            b_mean = float(before[0]) if before and before[0] is not None else 0.0
            a_mean = float(after[0]) if after and after[0] is not None else 0.0
            if b_mean > 0 and a_mean > 0:
                raw_ratio = a_mean / b_mean
                peak = max(0.1, min(10.0, raw_ratio))
            else:
                peak = 1.0
                raw_ratio = None
                row_warnings.append(
                    f"REGIME_PEAK_UNAVAILABLE ({regime_id} @ {change_date}: b_mean={b_mean:.1f}, a_mean={a_mean:.1f})"
                )

        # Half-life: prefer fitted (if meaningful decay observed) else
        # fall back to authored. Confidence gate prevents low-data fits
        # from overriding the authored guess.
        effective_hl: Optional[float] = None
        if fitted_hl is not None and (fit_confidence or 0.0) >= 0.5:
            effective_hl = float(fitted_hl)
        elif authored_hl is not None and authored_hl > 0:
            effective_hl = float(authored_hl)
        else:
            effective_hl = None  # None = permanent (no decay applied)

        result.append({
            "regime_id": regime_id,
            "change_date": change_date,
            "description": description or "",
            "peak_multiplier": peak,
            "raw_ratio": raw_ratio,
            "before_mean": b_mean,
            "after_mean": a_mean,
            "half_life_weeks": effective_hl,
            "authored_half_life_weeks": float(authored_hl) if authored_hl is not None else None,
            "fitted_half_life_weeks": float(fitted_hl) if fitted_hl is not None else None,
            "fit_confidence": float(fit_confidence) if fit_confidence is not None else None,
            "decay_status": decay_status or "no-fit-state",
            "n_post_weeks": int(n_post_weeks) if n_post_weeks is not None else None,
            "expected_impact_pct": expected_impact_pct,
            "source": source,
            "warnings": row_warnings,
        })

    return result


def _single_regime_multiplier_at(regime: dict, target_week: date) -> float:
    """Multiplier contribution from ONE regime at ONE projection week.

    Before onset: 1.0 (regime hasn't activated yet — project as if it doesn't exist)
    At/after onset:
        - If half_life_weeks is None or 0: peak_multiplier forever (permanent)
        - Otherwise: 1 + (peak - 1) × 0.5^(weeks_since_onset / half_life)
          → at onset, = peak
          → at half_life_weeks after, excess over 1 is halved
          → at ∞, approaches 1.0 (regime effect fully decayed)
    """
    weeks_since_onset = (target_week - regime["change_date"]).days / 7.0
    if weeks_since_onset < 0:
        return 1.0  # regime hasn't started yet at this projection week

    peak = regime["peak_multiplier"]
    half_life = regime.get("half_life_weeks")

    if half_life is None or half_life <= 0:
        return peak  # permanent regime — full multiplier forever after onset

    # Exponential decay of the *excess* over 1.0 (so effect fades to neutral,
    # not to zero).
    excess = peak - 1.0
    decayed_excess = excess * math.pow(0.5, weeks_since_onset / half_life)
    return 1.0 + decayed_excess


# Round 7 P1-04 math-side: lifts with no-decay-detected AND >=52 weeks of
# post-onset data are treated as structural baseline — their "lift" has
# persisted for >=1 year without decay, meaning the system has drifted INTO
# that level as its new baseline. Continuing to count them as a transient
# lift on top of the pre-regime anchor is double-counting. UI-side flag
# absorbed_into_baseline has been live since 2026-04-27; math-side parity
# landed in this commit after pre/post snapshot + delta review.
_ABSORBED_INTO_BASELINE_MIN_POST_WEEKS = 52


def _is_absorbed_into_baseline(regime: dict) -> bool:
    """Return True if the regime should be treated as part of the baseline
    rather than a transient lift on top of it."""
    n_post = regime.get("n_post_weeks")
    status = regime.get("decay_status")
    if status != "no-decay-detected":
        return False
    if n_post is None:
        return False
    return int(n_post) >= _ABSORBED_INTO_BASELINE_MIN_POST_WEEKS


def _per_regime_weighted_contribution(regime: dict, target_week: date, regime_multiplier: float = 1.0) -> float:
    """Apply a regime's effective confidence to its raw multiplier at the
    given week, returning the weighted factor that will compound into the
    Brand trajectory.

    Effective confidence is derived from fit_state (base confidence ×
    decay-status modifier × global multiplier). No single global
    regime-weight dial — each regime carries its own trust based on data.

    Formula (same shape as apply_weight elsewhere in the file):
        weighted = 1 + effective_confidence × (raw_mult - 1)

    For a dormant regime with near-zero effective confidence, weighted ≈ 1.0
    and the regime contributes nothing.

    For a stable, high-confidence regime, weighted ≈ raw_mult and the full
    step-shift lands in the output.

    Absorbed-into-baseline regimes (no-decay-detected AND n_post >= 52w)
    return 1.0 — they contribute nothing MULTIPLICATIVELY because they've
    drifted into the baseline. The Brand trajectory anchor already reflects
    their level. Counting them again would double-count.
    """
    from prediction.regime_confidence import effective_confidence

    if _is_absorbed_into_baseline(regime):
        return 1.0

    raw = _single_regime_multiplier_at(regime, target_week)
    eff = effective_confidence(
        regime.get("fit_confidence"),
        regime.get("decay_status"),
        regime_multiplier=regime_multiplier,
    )
    return 1.0 + eff * (raw - 1.0)


def compute_regime_multipliers_per_week(
    market: str, target_weeks: list[date], regime_multiplier: float = 1.0,
    scenario_override: Optional[dict] = None,
) -> tuple[list[float], list[str], list[dict]]:
    """Return (per-week net multipliers, warnings, per-regime detail).

    For each target week, compound the multiplier from every active
    structural regime — each regime contributes its own onset+decay profile
    AND its own auto-derived confidence (from fit_state), and effects
    multiply.

    Args:
        market: market code
        target_weeks: ISO-week start dates to project
        regime_multiplier: global dial over all per-regime confidences,
            default 1.0 (trust the auto-derivation). User can dial to 0.5
            to halve all regime contributions, 2.0 to double, etc.
        scenario_override: optional per-regime parameter override, applied
            to ALL active regimes for this projection. Supported keys:
            - 'half_life_weeks': int | None (None = permanent, no decay)
            - 'peak_multiplier': float (e.g. 1.0 to zero out the lift)
            - 'force_confidence': float in [0,1] (override fit confidence)
            The UI uses these to implement scenario chips like "current lift
            persists" (half_life_weeks=None) or "no lift" (peak=1.0).

    The compound formula per week:
        regime_mult[w] = product over active regimes of (
            1 + effective_confidence[r] × (raw_multiplier[r, w] - 1)
        )

    A dormant or data-sparse regime with low effective confidence contributes
    ~1.0 (neutral). A stable, well-fitted regime contributes near its full
    raw multiplier.
    """
    warnings: list[str] = []
    regimes = _fetch_structural_regimes(market)
    for r in regimes:
        warnings.extend(r["warnings"])

    if not regimes:
        return [1.0] * len(target_weeks), warnings, []

    # Apply scenario overrides (non-destructive — shallow copy each regime dict).
    # The strip_anchor_lift flag is handled in project_brand_trajectory, not here.
    if scenario_override:
        overridden = []
        for r in regimes:
            rc = dict(r)
            if "half_life_weeks" in scenario_override:
                rc["half_life_weeks"] = scenario_override["half_life_weeks"]
            if "peak_multiplier" in scenario_override:
                rc["peak_multiplier"] = scenario_override["peak_multiplier"]
            if "force_confidence" in scenario_override:
                rc["fit_confidence"] = scenario_override["force_confidence"]
            overridden.append(rc)
        regimes = overridden

    per_week: list[float] = []
    for wk in target_weeks:
        compound = 1.0
        for r in regimes:
            compound *= _per_regime_weighted_contribution(r, wk, regime_multiplier)
        per_week.append(compound)

    return per_week, warnings, regimes


# --- Backward-compatible wrapper for test/inspection code ---
def compute_regime_multiplier(market: str) -> tuple[float, list[str], list[dict]]:
    """Legacy scalar-multiplier accessor.

    Returns the steady-state multiplier — i.e. each regime's contribution
    assuming it's fully active. For regimes with finite half-life, this is
    an upper-bound overestimate of the long-run contribution (decay makes
    the actual contribution approach 1.0).

    Retained for:
      - existing test_brand_trajectory.py tests asserting on this shape
      - CLI debug inspection
      - any external caller that needs "what does the engine think this
        market's baseline lift is right now"

    New code should use compute_regime_multipliers_per_week() which
    accounts for decay.
    """
    regimes = _fetch_structural_regimes(market)
    warnings: list[str] = []
    for r in regimes:
        warnings.extend(r["warnings"])

    if not regimes:
        return 1.0, warnings, []

    # Compound at the onset week of the latest regime — "peak of current state"
    latest_onset = max(r["change_date"] for r in regimes)
    net = 1.0
    for r in regimes:
        net *= _single_regime_multiplier_at(r, latest_onset)

    # Build legacy-shape detail list.
    detail = [
        {
            "regime_id": r["regime_id"],
            "change_date": r["change_date"].isoformat(),
            "description": r["description"],
            "before_mean": r["before_mean"],
            "after_mean": r["after_mean"],
            "ratio": r["raw_ratio"],
            "ratio_clamped": r["peak_multiplier"],
            "half_life_weeks": r["half_life_weeks"],
            "expected_impact_pct": r["expected_impact_pct"],
        }
        for r in regimes
    ]
    return net, warnings, detail


# ---------- Brand CPA stream (not a stream, a scalar) ----------


def compute_brand_cpa_projected(market: str) -> tuple[float, list[str]]:
    """Rolling 8-week median of Brand CPA from ps.v_weekly.

    Scalar, not elasticity. Brand CPA has shown ~no responsiveness to Brand
    spend in our operating ranges (MX stayed $15–$25 across 5× spend change).
    """
    warnings: list[str] = []
    con = _fitting_db()
    rows = con.execute("""
        SELECT brand_cpa
        FROM ps.v_weekly
        WHERE market = ? AND period_type = 'weekly'
          AND brand_cpa IS NOT NULL AND brand_cpa > 0
        ORDER BY period_start DESC
        LIMIT ?
    """, [market, BRAND_CPA_MEDIAN_WEEKS]).fetchall()

    if not rows:
        warnings.append("BRAND_CPA_UNAVAILABLE (0 weeks)")
        return 0.0, warnings

    if len(rows) < BRAND_CPA_MEDIAN_WEEKS:
        warnings.append(f"BRAND_CPA_LOW_CONFIDENCE ({len(rows)} weeks < {BRAND_CPA_MEDIAN_WEEKS})")

    values = [float(r[0]) for r in rows if r[0] is not None]
    return float(np.median(values)) if values else 0.0, warnings


# ---------- Main entry point ----------


def project_brand_trajectory(
    market: str,
    target_weeks: list[date],
    weights: Optional[dict[str, float]] = None,
    regime_multiplier: float = 1.0,
    scenario_override: Optional[dict] = None,
) -> BrandProjection:
    """Produce a Brand regs + Brand spend projection for target_weeks.

    Args:
        market: market code (MX, US, DE, AU, ...)
        target_weeks: list of ISO week start dates (Monday) to project
        weights: optional override of {seasonal, trend, regime, qualitative}.
            For v1.1 Slim (Phase 6.1.5 architecture), `regime` is no longer
            a single global weight — each regime carries its own
            auto-derived confidence from ps.regime_fit_state. Passing a
            `regime` key here is IGNORED; use `regime_multiplier` instead
            for global override.
        regime_multiplier: global dial over auto-derived per-regime
            confidences, default 1.0 (trust the fit). User can dial to
            0.5 to halve all regime contributions, 2.0 to double.
        scenario_override: optional per-regime parameter override applied
            to all active regimes. Supported keys:
                half_life_weeks: None | int (None = permanent)
                peak_multiplier: float
                force_confidence: float in [0,1]
            Used by UI scenario chips to model "lift persists" vs "faster
            decay" vs "no lift".

    Returns BrandProjection. Never raises — any failure is captured as a
    warning and a defensible fallback value is used.
    """
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    warnings: list[str] = []
    if weights is not None and "regime" in weights and abs(weights.get("regime", 0.15) - 0.15) > 1e-6:
        warnings.append(
            "REGIME_WEIGHT_IGNORED: per-regime confidence is auto-derived from "
            "ps.regime_fit_state; use regime_multiplier=X instead of weights['regime']"
        )

    # 1) Fetch streams.
    seasonal, s_warn = compute_seasonal_multipliers(market, target_weeks)
    warnings.extend(s_warn)

    trend, t_warn = compute_recent_trend(market)
    warnings.extend(t_warn)

    regime_mults_per_week, r_warn, regime_detail = compute_regime_multipliers_per_week(
        market, target_weeks, regime_multiplier=regime_multiplier,
        scenario_override=scenario_override,
    )
    warnings.extend(r_warn)

    brand_cpa, cpa_warn = compute_brand_cpa_projected(market)
    warnings.extend(cpa_warn)

    # 2) Anchor (annual baseline): use trend intercept as the per-week anchor.
    # 2026-04-26 rework: intercept now reflects RECENT actuals (last
    # ANCHOR_RECENT_WEEKS weeks) which already have active regime lifts
    # baked in. To prevent double-counting when the forward regime stream
    # multiplies on top, we normalize the regime stream by its value at the
    # ANCHOR REFERENCE WEEK (the latest actuals week the anchor averaged).
    #
    # Net effect:  regime_mult_normalized[w] = regime_mult[w] / regime_mult_at_anchor
    #
    # This means:
    #   - at the anchor reference week, regime_mult_normalized ≈ 1.0 (no double-count)
    #   - if regime decays forward, normalized multiplier drops below 1.0
    #   - if regime intensifies, normalized multiplier climbs above 1.0
    #
    # If there are no active regimes (normalized = 1.0 everywhere), the old
    # and new behaviors are identical. If anchor_source is pre_regime_fallback
    # (recent window was empty), we skip the normalization because the anchor
    # doesn't have regime lifts baked in and we need the stream to lift.
    anchor = float(trend.get("intercept", 0.0))
    anchor_ref_week = trend.get("latest_week", None)
    intercept_source = trend.get("intercept_source", "recent_actuals")

    if anchor <= 0:
        warnings.append("BRAND_ANCHOR_ZERO (projecting zero Brand)")
        return BrandProjection(
            market=market,
            weeks=target_weeks,
            regs_per_week=[0.0] * len(target_weeks),
            spend_per_week=[0.0] * len(target_weeks),
            brand_cpa_used=brand_cpa,
            contribution=_normalize_contribution(w),
            warnings=warnings,
            lineage=_lineage_string(seasonal, trend, regime_detail),
        )

    # Compute regime multiplier at anchor reference week to normalize the stream.
    # Only applied when anchor came from recent_actuals — for fallback sources,
    # the anchor is regime-neutral (no lift baked in) and the stream should lift.
    if intercept_source in ("recent_actuals", "recent_actuals_post_regime") and anchor_ref_week is not None:
        anchor_week_mults, _, _ = compute_regime_multipliers_per_week(
            market, [anchor_ref_week], regime_multiplier=regime_multiplier,
            scenario_override=scenario_override,
        )
        regime_mult_at_anchor = anchor_week_mults[0] if anchor_week_mults else 1.0
        if regime_mult_at_anchor > 0:
            regime_mults_per_week = [m / regime_mult_at_anchor for m in regime_mults_per_week]

        # "Strip anchor lift" scenario: divide anchor itself by the BASELINE
        # regime multiplier (i.e. before any scenario_override). This removes
        # the implicit lift that the recent-actuals anchor has baked in,
        # producing a hypothetical "what would this market do without the
        # current campaign effects" projection.
        #
        # Only triggered when scenario_override has strip_anchor_lift=True.
        # Without this flag, the default behavior keeps the anchor at its
        # recent-actuals level (which is correct for the mixed/frequentist/
        # bayesian scenarios — only "no lift" wants to strip it).
        if scenario_override and scenario_override.get("strip_anchor_lift"):
            baseline_week_mults, _, _ = compute_regime_multipliers_per_week(
                market, [anchor_ref_week], regime_multiplier=1.0,
                scenario_override=None,   # use raw fit_state, no override
            )
            baseline_mult_at_anchor = baseline_week_mults[0] if baseline_week_mults else 1.0
            if baseline_mult_at_anchor > 0:
                anchor = anchor / baseline_mult_at_anchor
                warnings.append(
                    f"ANCHOR_LIFT_STRIPPED: divided by baseline regime_mult={baseline_mult_at_anchor:.3f} "
                    f"to expose pre-lift hypothetical baseline"
                )
    # else: anchor is pre_regime_fallback — use stream directly to lift from old level

    # 3) Compose per week.
    #
    # Architecture: regime multiplier is a LEVEL SHIFT (the "where is the
    # baseline right now"), seasonality is a SHAPE on top of the current
    # level, and trend is a LOCAL DRIFT on top of the level.
    #
    #     brand_regs[w] = anchor × regime_mult[w] × apply_weight(seasonal[w], W_s)
    #                            × apply_weight(trend[w], W_t)
    #
    # Regime stream is applied directly (not via apply_weight) because its
    # confidence is ALREADY baked into the per-week multiplier via the
    # per-regime auto-derivation (see compute_regime_multipliers_per_week).
    # A dormant regime with ~0 confidence already contributes ~1.0 (neutral)
    # per week — no separate global W_regime dial needed.
    #
    # Seasonal and trend keep their W_s / W_t knobs because those streams
    # don't have per-item confidence metadata (seasonality is an annual
    # shape, trend is a slope — neither has an analog of fit_state.confidence).

    def _apply_weight(value: float, weight: float) -> float:
        """Apply weight as 'fraction of deviation from 1.0 to carry forward'."""
        return 1.0 + weight * (value - 1.0)

    w_seasonal = w.get("seasonal", 0.0)
    w_trend = w.get("trend", 0.0)

    regs_per_week: list[float] = []
    stream_mults_per_week: list[dict[str, float]] = []

    for idx, wk in enumerate(target_weeks):
        s_raw = seasonal.get(iso_week_of(wk), 1.0)
        t_raw = trend_multiplier_for_week(trend, wk)
        r_applied = regime_mults_per_week[idx]  # already confidence-weighted

        s_applied = _apply_weight(s_raw, w_seasonal)
        t_applied = _apply_weight(t_raw, w_trend)

        combined_mult = s_applied * t_applied * r_applied
        regs_this_week = max(0.0, anchor * combined_mult)
        regs_per_week.append(regs_this_week)
        stream_mults_per_week.append({
            "seasonal_raw": s_raw,
            "seasonal_applied": s_applied,
            "trend_raw": t_raw,
            "trend_applied": t_applied,
            "regime_raw": r_applied,      # already confidence-weighted
            "regime_applied": r_applied,  # no separate weighting step
            "combined": combined_mult,
        })

    # 4) Brand spend = regs × Brand CPA (scalar).
    spend_per_week = [r * brand_cpa for r in regs_per_week]

    return BrandProjection(
        market=market,
        weeks=target_weeks,
        regs_per_week=regs_per_week,
        spend_per_week=spend_per_week,
        brand_cpa_used=brand_cpa,
        contribution=_normalize_contribution(w),
        stream_multipliers_per_week=stream_mults_per_week,
        warnings=warnings,
        lineage=_lineage_string(seasonal, trend, regime_detail),
    )


def _normalize_contribution(weights: dict[str, float]) -> dict[str, float]:
    """Return {stream: fraction} for display — only streams with nonzero weight."""
    total = sum(v for v in weights.values() if v > 0)
    if total <= 0:
        return {k: 0.0 for k in weights}
    return {k: (v / total) for k, v in weights.items()}


def _lineage_string(seasonal: dict, trend: dict, regime_detail: list[dict]) -> str:
    """Build a human-readable provenance string for UI display."""
    n_regimes = len(regime_detail) if regime_detail else 0
    fitted = sum(1 for r in regime_detail if r.get("source") == "fitted") if regime_detail else 0
    parts = [
        f"seasonal: {len(seasonal)} weeks",
        f"trend: {trend.get('n_weeks_used', 0)}w slope={trend.get('slope_log', 0.0):+.3f}/wk",
        f"regimes: {n_regimes} ({fitted} fitted, {n_regimes - fitted} bootstrap)",
    ]
    return " · ".join(parts)


# ---------- CLI for manual inspection (Phase 6.1.1 smoke test) ----------


def main(argv: list[str] | None = None) -> int:
    """Run Brand trajectory for one market over a period; print summary.

    Example:
        python3 -m prediction.brand_trajectory --market MX --period Y2026
    """
    import argparse
    import json

    p = argparse.ArgumentParser(description="Brand trajectory inspector")
    p.add_argument("--market", required=True)
    p.add_argument("--period", default="Y2026", help="Y2026, Q2, M05, W17-W20, ...")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = p.parse_args(argv)

    # Build list of Monday dates for the period. For Phase 6.1.1 we just
    # do the annual case — full period parsing lives in mpe_engine.
    if not args.period.startswith("Y"):
        print(f"Phase 6.1.1 CLI supports Y-periods only (got {args.period!r})", file=sys.stderr)
        return 2
    year = int(args.period[1:])
    from datetime import date as _date
    # Use ISO week 1 Monday as start.
    jan4 = _date(year, 1, 4)
    start = jan4 - timedelta(days=jan4.weekday())
    weeks = [start + timedelta(weeks=i) for i in range(52)]

    proj = project_brand_trajectory(args.market, weeks)

    if args.format == "json":
        print(json.dumps(proj.to_json(), indent=2, default=str))
        return 0

    print(f"# Brand Trajectory — {args.market} {args.period}")
    print()
    print(f"Weeks projected: {len(proj.weeks)}")
    print(f"Brand regs total: {proj.total_regs:,.0f}")
    print(f"Brand spend total: ${proj.total_spend:,.0f}")
    print(f"Brand CPA used: ${proj.brand_cpa_used:.2f}")
    print()
    print("Contribution:")
    for stream, frac in proj.contribution.items():
        print(f"  {stream}: {frac*100:.0f}%")
    print()
    print(f"Lineage: {proj.lineage}")
    if proj.warnings:
        print()
        print("Warnings:")
        for w in proj.warnings:
            print(f"  - {w}")
    # Monthly breakdown for quick scan.
    print()
    print("Monthly breakdown:")
    from collections import defaultdict
    monthly = defaultdict(lambda: {"regs": 0.0, "spend": 0.0})
    for wk, regs, spend in zip(proj.weeks, proj.regs_per_week, proj.spend_per_week):
        key = wk.strftime("%Y-%m")
        monthly[key]["regs"] += regs
        monthly[key]["spend"] += spend
    for mo in sorted(monthly.keys()):
        m = monthly[mo]
        print(f"  {mo}: {m['regs']:>8,.0f} regs · ${m['spend']:>12,.0f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())


def list_regimes_with_confidence(market: str, regime_multiplier: float = 1.0) -> list[dict]:
    """Return a UI-ready list of a market's active structural regimes with
    their auto-derived confidences.

    Phase 6.4 UI consumes this to render:

        Regime stack for MX:
          ○ Polaris INTL MX (2025-08-28)
              raw peak 1.22× · no-decay-detected · 33w post-onset
              auto confidence: 50% [============= .........]
          ○ MX Sparkle campaign onset W14 2026-04-05 (2026-04-05)
              raw peak 1.87× · still-peaking · 2w post-onset
              auto confidence: 18% [===. .................. ]

    Each row has both the raw fit data (peak, half-life, status) and the
    derived effective confidence. The UI slider lets users override a single
    regime's confidence if they disagree with the auto-derived value.
    """
    from prediction.regime_confidence import describe_confidence

    regimes = _fetch_structural_regimes(market)
    return [
        describe_confidence(
            regime_id=r["regime_id"],
            change_date=r["change_date"],
            description=r["description"],
            base_confidence=r.get("fit_confidence"),
            decay_status=r.get("decay_status"),
            n_post_weeks=r.get("n_post_weeks"),
            regime_multiplier=regime_multiplier,
        )
        | {
            "peak_multiplier": r["peak_multiplier"],
            "half_life_weeks": r.get("half_life_weeks"),
            "source": r.get("source", "fitted"),
        }
        for r in regimes
    ]
