"""
mpe_anomaly.py — Phase 4.1 — anomaly detection for v1.1 Slim refit cycles.

Compares current fit-quality and regime-confidence against prior quarterly
state and flags drops that warrant owner review. Runs as part of the
`mpe-refit` hook after `fit_market.py` + `fit_regime_state.py`.

Not a deep ML anomaly detector (that's v1.2+). Just the 80/20 rule checks:

1. **Fit-quality drop** — brand_cpa_elasticity.r_squared dropped > 0.10
   absolute from prior quarter.
2. **Regime confidence decay** — an active regime's confidence dropped
   below 0.20 (effectively dormant but still listed).
3. **OP2 pacing divergence** — projected annual total vs OP2 target
   diverged > 15%.
4. **YTD vs projection step** — latest YTD week's brand_regs differs
   from the next projected week's brand_regs by more than 3× (the
   "MX W15 cliff" diagnostic).

Each anomaly record:
    { market, check, severity, detail, remediation }

Usage:
    python3 -m prediction.mpe_anomaly
    python3 -m prediction.mpe_anomaly --market MX
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Optional


MARKETS = ["MX", "US", "CA", "UK", "DE", "FR", "IT", "ES", "JP", "AU"]

FIT_R2_DROP_THRESHOLD = 0.10       # absolute r² drop to flag
REGIME_CONFIDENCE_MIN = 0.20        # regime below this is effectively dormant
OP2_DIVERGENCE_PCT = 0.15           # 15% annual pacing gap
YTD_PROJECTION_STEP_RATIO = 3.0     # last YTD vs next projection ratio


@dataclass
class Anomaly:
    market: str
    check: str
    severity: str   # 'info', 'warn', 'error'
    detail: str
    remediation: str


def _con():
    import duckdb
    from prediction.config import MOTHERDUCK_TOKEN
    return duckdb.connect(f"md:ps_analytics?motherduck_token={MOTHERDUCK_TOKEN}")


def check_fit_quality(con, market: str) -> list[Anomaly]:
    """Look up brand_cpa_elasticity r² in current fit vs the prior version."""
    out = []
    try:
        # r² lives inside value_json for elasticity params
        rows = con.execute("""
            SELECT value_json, last_refit_at
            FROM ps.market_projection_params
            WHERE market = ? AND parameter_name = 'brand_cpa_elasticity'
            ORDER BY last_refit_at DESC
            LIMIT 2
        """, [market]).fetchall()
        if len(rows) < 2:
            return out
        import json
        def _r2(js):
            if js is None:
                return None
            if isinstance(js, dict):
                return js.get("r_squared")
            try:
                return json.loads(js).get("r_squared")
            except Exception:
                return None
        curr_r2 = _r2(rows[0][0])
        prev_r2 = _r2(rows[1][0])
        if curr_r2 is None or prev_r2 is None:
            return out
        drop = float(prev_r2) - float(curr_r2)
        if drop > FIT_R2_DROP_THRESHOLD:
            out.append(Anomaly(
                market=market,
                check="fit_r2_drop",
                severity="warn",
                detail=f"brand_cpa_elasticity r² fell {drop:.2f} (from {prev_r2:.2f} to {curr_r2:.2f})",
                remediation="Investigate data-quality drift in ps.v_weekly; check for recent regime onset not yet in ps.regime_changes.",
            ))
    except Exception as e:
        out.append(Anomaly(market=market, check="fit_r2_drop", severity="info",
                          detail=f"check skipped: {e}", remediation=""))
    return out


def check_regime_confidence(con, market: str) -> list[Anomaly]:
    out = []
    try:
        rows = con.execute("""
            SELECT rc.description, fs.confidence, fs.decay_status
            FROM ps.regime_fit_state_current fs
            JOIN ps.regime_changes rc ON rc.id = fs.regime_id
            WHERE fs.market = ? AND rc.is_structural_baseline = TRUE AND rc.active = TRUE
        """, [market]).fetchall()
        for desc, conf, status in rows:
            if conf is None:
                continue
            if float(conf) < REGIME_CONFIDENCE_MIN:
                out.append(Anomaly(
                    market=market,
                    check="regime_low_confidence",
                    severity="info",
                    detail=f"'{(desc or '')[:40]}' confidence={float(conf):.2f} (status={status})",
                    remediation="Regime approaching dormant. Verify post-onset data still supports the lift.",
                ))
    except Exception as e:
        out.append(Anomaly(market=market, check="regime_low_confidence", severity="info",
                          detail=f"check skipped: {e}", remediation=""))
    return out


def check_op2_pacing(con, market: str) -> list[Anomaly]:
    """Compare annual v1.1 Slim forecast total to OP2 target."""
    out = []
    try:
        # OP2 annual
        op2 = con.execute("""
            SELECT SUM(target_value) FROM ps.targets
            WHERE market = ? AND fiscal_year = 2026
              AND metric_name = 'registrations' AND period_type = 'monthly'
        """, [market]).fetchone()
        if not op2 or not op2[0]:
            return out
        op2_annual = float(op2[0])

        # v1.1 Slim annual total
        slim = con.execute("""
            SELECT SUM(predicted_value) FROM ps.forecasts
            WHERE market = ? AND method = 'v1_1_slim'
              AND metric_name = 'registrations'
              AND target_period LIKE '2026-W%'
              AND (scored IS NULL OR scored = false)
        """, [market]).fetchone()
        if not slim or not slim[0]:
            return out
        slim_annual = float(slim[0])

        gap = (slim_annual - op2_annual) / op2_annual
        if abs(gap) > OP2_DIVERGENCE_PCT:
            sev = "error" if abs(gap) > 0.30 else "warn"
            out.append(Anomaly(
                market=market,
                check="op2_pacing_divergence",
                severity=sev,
                detail=f"v1.1 Slim annual regs={slim_annual:,.0f} vs OP2={op2_annual:,.0f} (gap {gap:+.1%})",
                remediation="Compare with user expectations. If real → revisit regime fit or anchor window.",
            ))
    except Exception as e:
        out.append(Anomaly(market=market, check="op2_pacing_divergence", severity="info",
                          detail=f"check skipped: {e}", remediation=""))
    return out


def check_ytd_projection_step(con, market: str) -> list[Anomaly]:
    out = []
    try:
        # Last YTD Brand regs
        ytd = con.execute("""
            SELECT brand_registrations FROM ps.v_weekly
            WHERE market = ? AND period_type='weekly'
              AND YEAR(period_start) = 2026
            ORDER BY period_start DESC LIMIT 1
        """, [market]).fetchone()
        if not ytd or not ytd[0]:
            return out
        last_ytd_brand = float(ytd[0])

        # First projected Brand regs
        proj = con.execute("""
            SELECT predicted_value FROM ps.forecasts
            WHERE market = ? AND method = 'v1_1_slim'
              AND metric_name = 'brand_registrations'
              AND target_period LIKE '2026-W%'
              AND (scored IS NULL OR scored = false)
            ORDER BY target_period ASC LIMIT 1
        """, [market]).fetchone()
        if not proj or not proj[0]:
            return out
        first_proj_brand = float(proj[0])

        if last_ytd_brand <= 0 or first_proj_brand <= 0:
            return out
        ratio = max(last_ytd_brand, first_proj_brand) / min(last_ytd_brand, first_proj_brand)
        if ratio > YTD_PROJECTION_STEP_RATIO:
            out.append(Anomaly(
                market=market,
                check="ytd_projection_step",
                severity="warn",
                detail=f"last YTD Brand={last_ytd_brand:.0f} vs first projection={first_proj_brand:.0f} (ratio {ratio:.1f}×)",
                remediation="Anchor may be stale. Check brand_trajectory.py anchor window; confirm regime onset correctly modeled.",
            ))
    except Exception as e:
        out.append(Anomaly(market=market, check="ytd_projection_step", severity="info",
                          detail=f"check skipped: {e}", remediation=""))
    return out


def run(markets: Optional[list[str]] = None) -> list[Anomaly]:
    con = _con()
    markets = markets or MARKETS
    all_anomalies = []
    for m in markets:
        all_anomalies.extend(check_fit_quality(con, m))
        all_anomalies.extend(check_regime_confidence(con, m))
        all_anomalies.extend(check_op2_pacing(con, m))
        all_anomalies.extend(check_ytd_projection_step(con, m))
    return all_anomalies


def run_as_json(markets: Optional[list[str]] = None) -> dict:
    """Return anomalies keyed by market for UI consumption."""
    anomalies = run(markets)
    by_market: dict[str, list[dict]] = {}
    for a in anomalies:
        by_market.setdefault(a.market, []).append({
            "check": a.check,
            "severity": a.severity,
            "detail": a.detail,
            "remediation": a.remediation,
        })
    return {
        "markets": by_market,
        "summary": {
            "total": len(anomalies),
            "error": sum(1 for a in anomalies if a.severity == "error"),
            "warn": sum(1 for a in anomalies if a.severity == "warn"),
            "info": sum(1 for a in anomalies if a.severity == "info"),
        },
    }


def format_report(anomalies: list[Anomaly]) -> str:
    if not anomalies:
        return "No anomalies detected. All 10 markets passing fit-quality + regime-confidence + OP2-pacing + YTD-step checks."
    by_sev = {"error": [], "warn": [], "info": []}
    for a in anomalies:
        by_sev[a.severity].append(a)
    lines = [f"# MPE Anomaly Report", ""]
    for sev in ("error", "warn", "info"):
        rows = by_sev[sev]
        if not rows:
            continue
        lines.append(f"## {sev.upper()} ({len(rows)})")
        lines.append("")
        for a in rows:
            lines.append(f"- **{a.market} · {a.check}** — {a.detail}")
            if a.remediation:
                lines.append(f"  - _Remediation_: {a.remediation}")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", default=None)
    args = ap.parse_args()
    markets = [args.market] if args.market else None
    anomalies = run(markets)
    print(format_report(anomalies))


if __name__ == "__main__":
    main()
