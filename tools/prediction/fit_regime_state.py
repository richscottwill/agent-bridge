"""
Weekly regime fitter — MPE v1.1 Slim Phase 6.1.2

=============================================================================
WHAT THIS DOES (Plain English)
=============================================================================
    For every active structural regime in ps.regime_changes, fit the current
    peak multiplier and observed decay against the latest weekly data, and
    write a new row to ps.regime_fit_state.

    Runs weekly (Monday, after ps.v_weekly refreshes). Each run produces a
    snapshot that answers: "as of this week, what does the data say about
    each regime's lift and whether it's fading?"

    This keeps regime profiles fresh. Last week's "Sparkle half-life = 26
    weeks (guess)" becomes next week's "Sparkle half-life = 18 weeks (fit
    from 6 weeks of post-onset data, decaying faster than authored)."

=============================================================================
HOW IT WORKS
=============================================================================
    For each regime row in ps.regime_changes WHERE is_structural_baseline=TRUE
    AND active=TRUE:

    1. Compute pre-regime baseline: 8-week mean Brand regs immediately
       before change_date.
    2. Compute current peak: mean of the first 4-8 post-onset weeks.
       Uses as many as exist (min 2, max 8).
    3. If >= 8 post-onset weeks exist, attempt to fit observed decay:
         log(post_week_mean - pre_mean) ~ a + b × weeks_since_onset
       where b < 0 = decaying, b ≈ 0 = stable, b > 0 = still ramping.
       Convert slope to half-life: half_life_weeks = -ln(2) / b (if b < 0)
    4. Classify decay_status:
         - 'insufficient-data'     : <2 post weeks
         - 'still-peaking'         : fewer than 4 post weeks or b > 0.05
         - 'no-decay-detected'     : 4-8 post weeks, slope not statistically
                                     meaningful or ≥ 0
         - 'decaying-as-expected'  : fitted half-life within ±30% of authored
         - 'decaying-faster'       : fitted < 0.7 × authored
         - 'decaying-slower'       : fitted > 1.3 × authored
         - 'dormant'               : current_multiplier within 10% of 1.0
                                     AND post weeks >= 8
    5. Write new row to ps.regime_fit_state with fit_as_of = today.

=============================================================================
HOW IT CAN FAIL
=============================================================================
    1. Pre-regime window empty → peak_multiplier=1.0 + warning
    2. Zero post-regime weeks → 'insufficient-data' + peak=1.0
    3. MotherDuck write fails → script exits with non-zero code
    4. No active structural regimes in a market → script skips that market silently
=============================================================================
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

import numpy as np

# ---------- DB connection ----------

_con = None


def _db(read_only: bool = False):
    global _con
    if _con is None or (read_only and not _con.read_only):
        import duckdb
        from prediction.config import MOTHERDUCK_TOKEN
        _con = duckdb.connect(
            f"md:ps_analytics?motherduck_token={MOTHERDUCK_TOKEN}",
            read_only=read_only,
        )
    return _con


# ---------- Result shape ----------


@dataclass
class RegimeFit:
    regime_id: str
    market: str
    change_date: date
    authored_half_life_weeks: Optional[float]
    pre_mean: float
    current_peak: float
    peak_multiplier: float
    fitted_half_life_weeks: Optional[float]
    current_multiplier: float
    n_post_weeks: int
    decay_status: str
    confidence: float
    fit_method: str
    warnings: list[str] = field(default_factory=list)
    lineage: str = ""

    def to_row(self, fit_as_of: date) -> dict:
        return {
            "regime_id": self.regime_id,
            "market": self.market,
            "fit_as_of": fit_as_of,
            "peak_multiplier": self.peak_multiplier,
            "fitted_half_life_weeks": self.fitted_half_life_weeks,
            "current_multiplier": self.current_multiplier,
            "n_post_weeks": self.n_post_weeks,
            "decay_status": self.decay_status,
            "confidence": self.confidence,
            "authored_half_life_weeks": self.authored_half_life_weeks,
            "fit_method": self.fit_method,
            "warnings": json.dumps(self.warnings),
            "lineage": self.lineage,
        }


# ---------- Core fit ----------


def _fetch_brand_weekly(market: str, start: date, end: date) -> list[tuple[date, float]]:
    con = _db(read_only=False)
    rows = con.execute(
        """
        SELECT period_start, brand_registrations
        FROM ps.v_weekly
        WHERE market = ? AND period_type = 'weekly'
          AND period_start >= ? AND period_start < ?
          AND brand_registrations IS NOT NULL AND brand_registrations > 0
        ORDER BY period_start ASC
        """,
        [market, start, end],
    ).fetchall()
    return [(r[0], float(r[1])) for r in rows]


def fit_one_regime(
    regime_id: str,
    market: str,
    change_date: date,
    authored_half_life_weeks: Optional[float],
    fit_as_of: date,
) -> RegimeFit:
    """Fit peak multiplier + observed decay for a single regime."""
    warnings: list[str] = []

    # 1) Pre-regime baseline: 8 weeks immediately before change_date.
    pre = _fetch_brand_weekly(market, change_date - timedelta(weeks=8), change_date)
    pre_values = [v for _, v in pre]
    pre_mean = float(np.mean(pre_values)) if pre_values else 0.0
    if pre_mean <= 0:
        warnings.append("PRE_REGIME_WINDOW_EMPTY")

    # 2) Post-regime data — from onset through fit_as_of.
    post = _fetch_brand_weekly(market, change_date, fit_as_of + timedelta(weeks=1))
    n_post = len(post)

    # Insufficient-data bootstrap: no post weeks yet.
    if n_post == 0:
        return RegimeFit(
            regime_id=regime_id,
            market=market,
            change_date=change_date,
            authored_half_life_weeks=authored_half_life_weeks,
            pre_mean=pre_mean,
            current_peak=pre_mean,
            peak_multiplier=1.0,
            fitted_half_life_weeks=None,
            current_multiplier=1.0,
            n_post_weeks=0,
            decay_status="insufficient-data",
            confidence=0.0,
            fit_method="bootstrap",
            warnings=warnings + ["NO_POST_ONSET_DATA"],
            lineage=f"authored_hl={authored_half_life_weeks}; 0 post-onset weeks as of {fit_as_of}",
        )

    # 3) Peak: mean of first min(n_post, 8) weeks post-onset.
    peak_window_n = min(n_post, 8)
    peak_values = [v for _, v in post[:peak_window_n]]
    current_peak = float(np.mean(peak_values))
    raw_ratio = (current_peak / pre_mean) if pre_mean > 0 else 1.0
    peak_multiplier = max(0.1, min(10.0, raw_ratio))

    # 4) Fit observed decay when we have >= 8 post-onset weeks.
    fitted_hl: Optional[float] = None
    fit_method = "mean-ratio-8w" if n_post < 8 else "exponential-decay-fit"

    current_multiplier = peak_multiplier  # default if no decay fit

    if n_post >= 8 and pre_mean > 0 and peak_multiplier > 1.01:
        # Fit log(excess) = a + b × weeks_since_onset, where excess = post_mean - pre_mean.
        # Use rolling 4-week means to reduce noise.
        xs, ys = [], []
        window = 4
        for i in range(len(post) - window + 1):
            window_weeks = post[i : i + window]
            center_days = (window_weeks[window // 2][0] - change_date).days
            center_weeks = center_days / 7.0
            mean_val = float(np.mean([v for _, v in window_weeks]))
            excess = mean_val - pre_mean
            if excess > 0:
                xs.append(center_weeks)
                ys.append(math.log(excess))
        if len(xs) >= 3:
            x_arr = np.array(xs, dtype=float)
            y_arr = np.array(ys, dtype=float)
            try:
                # Simple OLS: [1, x] @ beta = y
                X = np.column_stack([np.ones_like(x_arr), x_arr])
                beta = np.linalg.solve(X.T @ X, X.T @ y_arr)
                slope = float(beta[1])
                # slope < 0 = decaying. half-life = -ln(2) / slope.
                if slope < -1e-4:  # meaningfully decaying
                    fitted_hl = float(-math.log(2) / slope)
                    # Sanity: clamp between 2 weeks and 520 (~10 years).
                    fitted_hl = max(2.0, min(520.0, fitted_hl))
                    # Current multiplier = 1 + (peak-1) × 0.5^(weeks_since_onset/fitted_hl)
                    weeks_since_onset = (fit_as_of - change_date).days / 7.0
                    excess_now = (peak_multiplier - 1.0) * math.pow(
                        0.5, weeks_since_onset / fitted_hl
                    )
                    current_multiplier = 1.0 + excess_now
                elif slope > 0.01:
                    # Still climbing — no decay to fit; peak from current_peak window
                    # may actually be understating. Note this as still-peaking.
                    fit_method = "mean-ratio-8w"
            except np.linalg.LinAlgError:
                warnings.append("DECAY_FIT_SINGULAR")

    # 5) Classify decay_status.
    if n_post < 2:
        decay_status = "insufficient-data"
        confidence = 0.1
    elif n_post < 4:
        decay_status = "still-peaking"
        confidence = 0.3
    elif peak_multiplier < 1.10:
        # Effect size too small to be meaningful.
        decay_status = "no-decay-detected"
        confidence = 0.4
    elif fitted_hl is None:
        # No decay slope fit (either <8 post weeks or slope not meaningfully negative).
        if n_post >= 8:
            # Current multiplier is still near peak after 8+ weeks → no decay detected.
            decay_status = "no-decay-detected"
            confidence = 0.5
        else:
            decay_status = "still-peaking"
            confidence = 0.3
    elif current_multiplier <= 1.10:
        # Regime effect has decayed back to within 10% of pre-regime baseline.
        decay_status = "dormant"
        confidence = 0.7
    elif authored_half_life_weeks is None:
        # Authored was permanent — any detected decay is "slower" (because
        # expected = infinite). Use the fit as new information.
        decay_status = "decaying-slower" if fitted_hl > 52 else "decaying-as-expected"
        confidence = 0.6
    else:
        ratio = fitted_hl / authored_half_life_weeks
        if ratio < 0.7:
            decay_status = "decaying-faster"
        elif ratio > 1.3:
            decay_status = "decaying-slower"
        else:
            decay_status = "decaying-as-expected"
        # Confidence grows with post weeks, capped at 0.85.
        confidence = min(0.85, 0.4 + 0.05 * n_post)

    lineage = (
        f"pre_mean={pre_mean:.1f} "
        f"peak={current_peak:.1f} "
        f"mult={peak_multiplier:.2f} "
        f"n_post={n_post} "
        f"fitted_hl={fitted_hl} "
        f"authored_hl={authored_half_life_weeks} "
        f"status={decay_status}"
    )

    return RegimeFit(
        regime_id=regime_id,
        market=market,
        change_date=change_date,
        authored_half_life_weeks=authored_half_life_weeks,
        pre_mean=pre_mean,
        current_peak=current_peak,
        peak_multiplier=peak_multiplier,
        fitted_half_life_weeks=fitted_hl,
        current_multiplier=current_multiplier,
        n_post_weeks=n_post,
        decay_status=decay_status,
        confidence=float(confidence),
        fit_method=fit_method,
        warnings=warnings,
        lineage=lineage,
    )


def fit_all_for_market(market: str, fit_as_of: Optional[date] = None) -> list[RegimeFit]:
    """Fit every active structural regime for a market.

    Returns list of RegimeFit objects (writes handled by caller).
    """
    if fit_as_of is None:
        fit_as_of = date.today()
    con = _db(read_only=False)
    rows = con.execute(
        """
        SELECT id, CAST(change_date AS DATE), half_life_weeks
        FROM ps.regime_changes
        WHERE market = ? AND is_structural_baseline = TRUE AND active = TRUE
        ORDER BY change_date ASC
        """,
        [market],
    ).fetchall()

    fits = []
    for regime_id, change_date, authored_hl in rows:
        if change_date is None:
            continue
        fits.append(
            fit_one_regime(
                regime_id=regime_id,
                market=market,
                change_date=change_date,
                authored_half_life_weeks=float(authored_hl) if authored_hl is not None else None,
                fit_as_of=fit_as_of,
            )
        )
    return fits


def write_fit_state(fits: list[RegimeFit], fit_as_of: date) -> int:
    """Write fits to ps.regime_fit_state. Returns number of rows written."""
    if not fits:
        return 0
    con = _db(read_only=False)
    n = 0
    for fit in fits:
        row = fit.to_row(fit_as_of)
        con.execute(
            """
            INSERT INTO ps.regime_fit_state
                (regime_id, market, fit_as_of, peak_multiplier,
                 fitted_half_life_weeks, current_multiplier, n_post_weeks,
                 decay_status, confidence, authored_half_life_weeks,
                 fit_method, warnings, lineage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                row["regime_id"],
                row["market"],
                row["fit_as_of"],
                row["peak_multiplier"],
                row["fitted_half_life_weeks"],
                row["current_multiplier"],
                row["n_post_weeks"],
                row["decay_status"],
                row["confidence"],
                row["authored_half_life_weeks"],
                row["fit_method"],
                row["warnings"],
                row["lineage"],
            ],
        )
        n += 1
    return n


# ---------- CLI ----------


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Weekly regime state fitter for MPE v1.1")
    p.add_argument("--market", help="Fit only this market (default: all 10)")
    p.add_argument("--all-markets", action="store_true", help="Fit every market")
    p.add_argument("--fit-as-of", help="Date cutoff YYYY-MM-DD (default today)")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute fits and print summary, don't write to DB",
    )
    args = p.parse_args(argv)

    if args.fit_as_of:
        from datetime import datetime as _dt

        fit_as_of = _dt.strptime(args.fit_as_of, "%Y-%m-%d").date()
    else:
        fit_as_of = date.today()

    if args.all_markets:
        markets = ["MX", "US", "CA", "UK", "DE", "FR", "IT", "ES", "JP", "AU"]
    elif args.market:
        markets = [args.market]
    else:
        print("Specify --market X or --all-markets", file=sys.stderr)
        return 2

    total_written = 0
    for m in markets:
        fits = fit_all_for_market(m, fit_as_of)
        print(f"\n=== {m} — {len(fits)} active structural regimes, fit_as_of={fit_as_of} ===")
        for f in fits:
            print(
                f"  {f.change_date} [{f.regime_id[:8]}…] "
                f"peak={f.peak_multiplier:.2f}× "
                f"current={f.current_multiplier:.2f}× "
                f"fitted_hl={f.fitted_half_life_weeks if f.fitted_half_life_weeks is None else f'{f.fitted_half_life_weeks:.1f}w'} "
                f"(authored={f.authored_half_life_weeks}) "
                f"status={f.decay_status} n_post={f.n_post_weeks} conf={f.confidence:.2f}"
            )
            if f.warnings:
                for w in f.warnings:
                    print(f"      W: {w}")
        if not args.dry_run and fits:
            n = write_fit_state(fits, fit_as_of)
            total_written += n
            print(f"  Wrote {n} rows to ps.regime_fit_state")
        elif args.dry_run:
            print("  DRY RUN — not writing")

    print(f"\nTotal fit rows written: {total_written}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
