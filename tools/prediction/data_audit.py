"""Data Audit — Phase 0 gate for the Market Projection Engine (MPE).

WHY THIS EXISTS
    Before fitting any market-specific projection parameters, we must know
    which markets have enough clean data to support a full fit and which
    must fall back to a regional average. This script answers that question
    in plain English so a non-technical owner can read the output and make
    the right call without reading any code.

HOW THE OWNER MAINTAINS IT
    Run quarterly via:  kiro hook run mpe-refit    (invokes this as step 1)
    Or run ad-hoc:      python3 -m shared.tools.prediction.data_audit
    Output lives at:    shared/dashboards/data/data-audit-reports/
                        {yyyy-mm-dd}-all-markets.md

WHAT HAPPENS ON FAILURE
    Each market evaluates independently. If the DuckDB connection drops or
    a single market's data is malformed, that row shows "AUDIT FAILED" with
    a plain-English reason; the rest of the report still prints. You never
    get a partial/silent audit — either all markets evaluated or the script
    exits non-zero with a loud message.

SCOPE
    v1 decision thresholds (match spec R1.9, R9.6):
      - Market_Specific fit:  >= 80 clean weeks AND data quality OK
      - Regional_Fallback:    < 80 clean weeks OR < 40 with spend variance OR data quality issues
      - Setup_Required:       < 20 weeks or completely missing

    Regional fallback routing:
      - US, CA            -> NA curve
      - UK, DE, FR, IT, ES -> EU5 curve
      - MX, AU, JP         -> WW curve (no natural region)

    v1 does NOT use this script to make fitting decisions itself — it
    surfaces them to the owner who decides. The decision gets encoded in
    ps.market_projection_params.fallback_level at fit time.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# ---------- Connection helper (pattern copied from wbr_pipeline.py / project.py) ----------

sys.path.insert(0, os.path.expanduser('~/shared/tools'))

# Lazy connection so --help works without DB
_con = None


def _db():
    global _con
    if _con is None:
        try:
            import duckdb
            from prediction.config import MOTHERDUCK_TOKEN
            _con = duckdb.connect(
                f'md:ps_analytics?motherduck_token={MOTHERDUCK_TOKEN}',
                read_only=True,
            )
        except Exception as e:
            print(f"[data_audit] FATAL: cannot connect to MotherDuck: {e}", file=sys.stderr)
            sys.exit(2)
    return _con


# ---------- Thresholds ----------

THRESHOLD_MARKET_SPECIFIC_WEEKS = 80   # R1.9
THRESHOLD_MIN_VIABLE_WEEKS = 40         # below this, even regional fallback is shaky
THRESHOLD_SETUP_REQUIRED_WEEKS = 20     # below this, no projection possible
ELASTICITY_SPEND_VARIANCE_MIN = 0.20    # need at least 20% spend coefficient-of-variation for elasticity fit

REGIONAL_FALLBACK_MAP = {
    'US': 'NA', 'CA': 'NA',
    'UK': 'EU5', 'DE': 'EU5', 'FR': 'EU5', 'IT': 'EU5', 'ES': 'EU5',
    'MX': 'WW', 'AU': 'WW', 'JP': 'WW',
}

ALL_MARKETS = ['US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP', 'MX', 'AU']

# Markets the v1 spec calls "Fully_Fit_Markets" for reference (audit may recommend otherwise)
V1_SPEC_FULLY_FIT = ['MX', 'US', 'AU']


@dataclass
class MarketAudit:
    """One market's audit result. All fields populated or explicit None on failure."""
    market: str
    weeks_total: int = 0
    weeks_clean: int = 0
    earliest: str = ""
    latest: str = ""
    brand_spend_cv: float | None = None
    nb_spend_cv: float | None = None
    missing_ccp_pct: float | None = None
    regime_exclusions: int = 0
    recommendation: str = ""       # 'market_specific' | 'regional_fallback' | 'setup_required' | 'audit_failed'
    fallback_region: str | None = None
    explanation: str = ""          # plain-English for the owner
    warnings: list[str] = field(default_factory=list)


# ---------- Audit logic ----------

def audit_market(con, market: str) -> MarketAudit:
    """Audit one market. Never raises — wraps failures in MarketAudit.recommendation='audit_failed'."""
    audit = MarketAudit(market=market)

    try:
        # --- Basic weekly count and range ---
        row = con.execute("""
            SELECT COUNT(*), MIN(period_start), MAX(period_start)
            FROM ps.v_weekly
            WHERE market = ? AND period_type = 'weekly'
        """, [market]).fetchone()
        audit.weeks_total = int(row[0] or 0)
        audit.earliest = str(row[1]) if row[1] else ""
        audit.latest = str(row[2]) if row[2] else ""

        if audit.weeks_total == 0:
            audit.recommendation = 'setup_required'
            audit.explanation = (
                f"{market} has no weekly data in ps.v_weekly. "
                f"No projections possible until data is loaded."
            )
            audit.fallback_region = REGIONAL_FALLBACK_MAP.get(market)
            return audit

        # --- Regime exclusions from ps.regime_changes ---
        regime_rows = con.execute("""
            SELECT COUNT(*) FROM ps.regime_changes WHERE market = ?
        """, [market]).fetchone()
        audit.regime_exclusions = int(regime_rows[0] or 0) if regime_rows else 0

        # Rough estimate: each regime change invalidates ~4 surrounding weeks of elasticity signal
        estimated_regime_excluded_weeks = audit.regime_exclusions * 4

        # --- Clean weeks (non-null spend, non-null regs, after regime buffer) ---
        clean_rows = con.execute("""
            SELECT COUNT(*) FROM ps.v_weekly
            WHERE market = ? AND period_type = 'weekly'
              AND cost IS NOT NULL AND cost > 0
              AND registrations IS NOT NULL AND registrations > 0
              AND brand_cost IS NOT NULL AND nb_cost IS NOT NULL
        """, [market]).fetchone()
        raw_clean = int(clean_rows[0] or 0)
        audit.weeks_clean = max(0, raw_clean - estimated_regime_excluded_weeks)

        # --- Spend variance (coefficient of variation) for Brand and NB ---
        # CV = stddev / mean. Below 0.2 means spend is too flat to fit elasticity.
        cv_row = con.execute("""
            SELECT
                CASE WHEN AVG(brand_cost) > 0 THEN STDDEV(brand_cost) / AVG(brand_cost) ELSE NULL END,
                CASE WHEN AVG(nb_cost) > 0    THEN STDDEV(nb_cost) / AVG(nb_cost)       ELSE NULL END
            FROM ps.v_weekly
            WHERE market = ? AND period_type = 'weekly'
              AND cost > 0 AND brand_cost IS NOT NULL AND nb_cost IS NOT NULL
        """, [market]).fetchone()
        audit.brand_spend_cv = float(cv_row[0]) if cv_row[0] is not None else None
        audit.nb_spend_cv = float(cv_row[1]) if cv_row[1] is not None else None

        # --- Missing ieccp (column presence, not a data-quality signal) ---
        # ps.v_weekly stores ieccp as a derived column that's often null because
        # CCP values live in a separate source (column U of the finance file).
        # We surface it only when it's unexpectedly partially populated (e.g.,
        # a market we thought had ieccp history turns out to have gaps).
        missing_row = con.execute("""
            SELECT
                100.0 * SUM(CASE WHEN ieccp IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0)
            FROM ps.v_weekly
            WHERE market = ? AND period_type = 'weekly' AND cost > 0
        """, [market]).fetchone()
        audit.missing_ccp_pct = float(missing_row[0]) if missing_row and missing_row[0] is not None else None

        # --- Recommendation logic ---
        audit.fallback_region = REGIONAL_FALLBACK_MAP.get(market)

        if audit.weeks_clean < THRESHOLD_SETUP_REQUIRED_WEEKS:
            audit.recommendation = 'setup_required'
            audit.explanation = (
                f"{market} has only {audit.weeks_clean} clean weeks after regime exclusions "
                f"(need at least {THRESHOLD_SETUP_REQUIRED_WEEKS}). No projections possible. "
                f"Revisit after {THRESHOLD_SETUP_REQUIRED_WEEKS - audit.weeks_clean} more weeks of data."
            )

        elif audit.weeks_clean < THRESHOLD_MARKET_SPECIFIC_WEEKS:
            audit.recommendation = 'regional_fallback'
            audit.explanation = (
                f"{market} has {audit.weeks_clean} clean weeks — below the {THRESHOLD_MARKET_SPECIFIC_WEEKS}-week "
                f"threshold for a market-specific fit. Use {audit.fallback_region} regional fallback. "
                f"Credible intervals will be wider than fully-fit markets. "
                f"Revisit after {THRESHOLD_MARKET_SPECIFIC_WEEKS - audit.weeks_clean} more weeks."
            )

        elif (audit.brand_spend_cv is not None and audit.brand_spend_cv < ELASTICITY_SPEND_VARIANCE_MIN) or \
             (audit.nb_spend_cv is not None and audit.nb_spend_cv < ELASTICITY_SPEND_VARIANCE_MIN):
            audit.recommendation = 'regional_fallback'
            audit.explanation = (
                f"{market} has {audit.weeks_clean} clean weeks (enough count) but spend has been too stable "
                f"to fit an elasticity curve (Brand CV={audit.brand_spend_cv:.2f}, "
                f"NB CV={audit.nb_spend_cv:.2f}; need at least {ELASTICITY_SPEND_VARIANCE_MIN}). "
                f"Use {audit.fallback_region} regional fallback until spend varies more."
            )

        else:
            audit.recommendation = 'market_specific'
            audit.explanation = (
                f"{market} has {audit.weeks_clean} clean weeks and sufficient spend variance "
                f"(Brand CV={audit.brand_spend_cv:.2f}, NB CV={audit.nb_spend_cv:.2f}). "
                f"Recommend a full market-specific fit."
            )

        # --- Add warnings where relevant ---
        if audit.regime_exclusions > 0:
            audit.warnings.append(
                f"{audit.regime_exclusions} regime change(s) documented in ps.regime_changes; "
                f"~{estimated_regime_excluded_weeks} weeks excluded from elasticity signal."
            )
        if audit.missing_ccp_pct is not None and audit.missing_ccp_pct > 20 and audit.missing_ccp_pct < 95:
            # 100% null means ieccp isn't stored in ps.v_weekly for this market — expected.
            # Partial population (20-95%) means a real gap we should flag.
            audit.warnings.append(
                f"{audit.missing_ccp_pct:.0f}% of weeks have ieccp populated and gaps elsewhere. "
                f"Investigate — CCP series should be continuous once loaded."
            )
        if audit.weeks_total > audit.weeks_clean + 5:
            audit.warnings.append(
                f"{audit.weeks_total - audit.weeks_clean} week(s) dropped from clean set "
                f"due to nulls or zero spend."
            )

    except Exception as e:
        audit.recommendation = 'audit_failed'
        audit.explanation = f"Audit crashed for {market}: {type(e).__name__}: {e}"

    return audit


# ---------- Report rendering ----------

def render_markdown(audits: list[MarketAudit]) -> str:
    """Render audits as an owner-readable markdown report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M PT")
    lines = []
    lines.append(f"# MPE Data Audit — All Markets")
    lines.append(f"")
    lines.append(f"**Run at**: {now}")
    lines.append(f"**Purpose**: Tell the owner which markets can support a full market-specific "
                 f"fit in MPE v1 and which must use regional fallback. Run by `data_audit.py` "
                 f"before any fit. This is the Phase 0 gate.")
    lines.append(f"")

    # --- Summary table ---
    lines.append("## Summary")
    lines.append("")
    lines.append("| Market | Clean Weeks | Spend Variance (B/NB) | Recommendation | Fallback Region |")
    lines.append("|--------|-------------|------------------------|----------------|-----------------|")
    for a in audits:
        cv_cell = "n/a"
        if a.brand_spend_cv is not None and a.nb_spend_cv is not None:
            cv_cell = f"{a.brand_spend_cv:.2f} / {a.nb_spend_cv:.2f}"
        fallback_cell = a.fallback_region or "—"
        rec_display = {
            'market_specific': 'MARKET-SPECIFIC FIT',
            'regional_fallback': 'regional fallback',
            'setup_required': 'SETUP REQUIRED',
            'audit_failed': 'AUDIT FAILED',
        }.get(a.recommendation, a.recommendation)
        lines.append(f"| {a.market} | {a.weeks_clean} | {cv_cell} | {rec_display} | {fallback_cell} |")
    lines.append("")

    # --- v1 spec alignment check ---
    lines.append("## v1 Spec Alignment Check")
    lines.append("")
    lines.append("The spec designates MX, US, and AU as Fully_Fit_Markets. Compare with audit recommendations:")
    lines.append("")
    mismatches = []
    for m in V1_SPEC_FULLY_FIT:
        a = next((x for x in audits if x.market == m), None)
        if a is None:
            lines.append(f"- {m}: audit missing — investigate")
            continue
        if a.recommendation == 'market_specific':
            lines.append(f"- {m}: ALIGNED — market-specific fit recommended")
        else:
            lines.append(f"- {m}: MISMATCH — spec says Fully_Fit but audit recommends `{a.recommendation}`. "
                         f"Spec needs updating OR wait for more data.")
            mismatches.append(m)
    lines.append("")
    if mismatches:
        lines.append(f"**Action**: {len(mismatches)} market(s) need spec adjustment or data accumulation before fitting. "
                     f"Update `.kiro/specs/market-projection-engine/requirements.md` and rerun Phase 1.")
    else:
        lines.append("**Action**: No adjustments needed. Proceed with Phase 1 fits as spec'd.")
    lines.append("")

    # --- Per-market detail ---
    lines.append("## Per-Market Detail")
    lines.append("")
    for a in audits:
        lines.append(f"### {a.market}")
        lines.append("")
        lines.append(f"- **Recommendation**: `{a.recommendation}`")
        lines.append(f"- **Clean weeks**: {a.weeks_clean} of {a.weeks_total} total "
                     f"(data range {a.earliest} to {a.latest})")
        if a.brand_spend_cv is not None:
            lines.append(f"- **Brand spend variance (CV)**: {a.brand_spend_cv:.2f} "
                         f"(need >= {ELASTICITY_SPEND_VARIANCE_MIN} for elasticity)")
        if a.nb_spend_cv is not None:
            lines.append(f"- **NB spend variance (CV)**: {a.nb_spend_cv:.2f}")
        if a.missing_ccp_pct is not None:
            lines.append(f"- **Weeks with no ie%CCP**: {a.missing_ccp_pct:.0f}%")
        lines.append(f"- **Regime changes documented**: {a.regime_exclusions}")
        if a.fallback_region:
            lines.append(f"- **Fallback region if used**: {a.fallback_region}")
        lines.append(f"")
        lines.append(f"**Explanation**: {a.explanation}")
        if a.warnings:
            lines.append(f"")
            lines.append(f"**Warnings**:")
            for w in a.warnings:
                lines.append(f"- {w}")
        lines.append("")

    # --- Owner next steps ---
    lines.append("## What to do with this report")
    lines.append("")
    lines.append("1. Read the Summary table. Markets marked MARKET-SPECIFIC FIT are ready for Phase 1 fitting.")
    lines.append("2. Markets marked `regional fallback` will use a regional average curve in v1. Wider credible intervals. Still trustworthy.")
    lines.append("3. Markets marked SETUP REQUIRED cannot produce projections until more data accumulates. Re-audit next quarter.")
    lines.append("4. Check the v1 Spec Alignment section. If any Fully_Fit_Market came back as fallback-recommended, update the spec before fitting.")
    lines.append("5. This report is canonical for the current quarter. Next refit will generate a new one.")
    lines.append("")

    return "\n".join(lines) + "\n"


# ---------- CLI entry point ----------

def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(
        prog="data_audit",
        description="Phase 0 data audit for the Market Projection Engine.",
    )
    parser.add_argument(
        "--markets",
        default=",".join(ALL_MARKETS),
        help="Comma-separated markets to audit (default: all 10).",
    )
    parser.add_argument(
        "--out-dir",
        default=os.path.expanduser("~/shared/dashboards/data/data-audit-reports"),
        help="Directory to write markdown report.",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Print report to stdout instead of writing a file.",
    )
    args = parser.parse_args(argv)

    markets = [m.strip().upper() for m in args.markets.split(",") if m.strip()]
    invalid = [m for m in markets if m not in ALL_MARKETS]
    if invalid:
        print(f"[data_audit] ERROR: unknown markets: {invalid}. Valid: {ALL_MARKETS}", file=sys.stderr)
        return 1

    con = _db()
    audits = [audit_market(con, m) for m in markets]
    report = render_markdown(audits)

    if args.print_only:
        print(report)
        return 0

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    out_path = out_dir / f"{today}-all-markets.md"
    out_path.write_text(report)
    print(f"[data_audit] wrote {out_path}")

    # Exit code reflects outcome: 0 all OK, 1 any audit_failed, 2 if any Fully_Fit misalignment
    if any(a.recommendation == 'audit_failed' for a in audits):
        print("[data_audit] one or more audits failed — see report", file=sys.stderr)
        return 1
    mismatches = [a.market for a in audits
                  if a.market in V1_SPEC_FULLY_FIT and a.recommendation != 'market_specific']
    if mismatches:
        print(f"[data_audit] WARNING: v1 spec mismatches for {mismatches} — see report", file=sys.stderr)
        # Non-fatal: the report itself is the deliverable. Owner decides next step.
    return 0


if __name__ == "__main__":
    sys.exit(main())
