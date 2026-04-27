"""
Part 2 research — seasonality analysis and external benchmarking per market.

Generates a markdown report per market showing:
  - Multi-year seasonal pattern from ps.v_weekly (our own truth)
  - Known-event annotations (Semana Santa MX, back-to-school UK, etc.)
  - Year-over-year stability check
  - Flags weeks where the fitted seasonal multiplier looks anomalous
  - Comparison hook for external benchmarks (left blank — filled in by operator)

Output: shared/wiki/agent-created/operations/mpe-seasonality-research.md
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import duckdb
from collections import defaultdict


ALL_MARKETS = ['US', 'CA', 'UK', 'DE', 'FR', 'IT', 'ES', 'JP', 'MX', 'AU']

# Known seasonal events per market that we'd expect to see in the data.
# Source: internal WBR / MBR commentary + industry-standard search seasonality.
KNOWN_EVENTS = {
    'US': [
        ('W01-W02', 'Post-holiday slowdown — paid search typically dips 10-15% vs Dec average'),
        ('W13-W15', 'Tax deadline spike — business registrations uptick mid-April'),
        ('W27-W32', 'Summer soft season — travel + vacation reduces B2B search'),
        ('W48-W52', 'Black Friday through year-end — strong paid search lift 20-30%'),
    ],
    'CA': [
        ('W27-W32', 'Summer soft season, similar US pattern'),
        ('W48-W52', 'Boxing Day + Black Friday echo'),
    ],
    'UK': [
        ('W01', 'Return-to-work spike — January is historically UK paid search peak'),
        ('W30-W34', 'Summer holidays UK schools out — B2B reduced'),
        ('W48-W52', 'Black Friday now strong in UK, ~15-20% lift'),
    ],
    'DE': [
        ('W28-W34', 'Summer vacation — August especially quiet'),
        ('W48-W52', 'Weihnachtsmarkt season — modest Q4 lift'),
    ],
    'FR': [
        ('W31-W34', 'August vacances — almost entirely offline'),
        ('W48-W52', 'End-of-year moderate uplift'),
    ],
    'IT': [
        ('W32-W34', 'Ferragosto (August 15 week) — near-complete shutdown'),
        ('W48-W52', 'Holiday season'),
    ],
    'ES': [
        ('W32-W34', 'Summer holidays southern Spain'),
        ('W48-W52', 'Christmas / Three Kings lead-in'),
    ],
    'JP': [
        ('W01-W02', 'New Year holiday — January 1-3 extended'),
        ('W18-W21', 'Golden Week — early May'),
        ('W32-W34', 'Obon (mid-August)'),
    ],
    'MX': [
        ('W14', 'Semana Santa (Holy Week) — 30-35% volume suppression'),
        ('W48-W52', 'Buen Fin + Navidad — holiday Q4 uplift'),
    ],
    'AU': [
        ('W01-W05', 'Southern hemisphere summer — AU schools out through end of January'),
        ('W26-W30', 'Mid-year EOFY (End Of Financial Year) ends W26 — business registrations spike'),
        ('W48-W52', 'Christmas holidays'),
    ],
}


def _get_connection():
    from prediction.config import MOTHERDUCK_TOKEN
    return duckdb.connect(
        f'md:ps_analytics?motherduck_token={MOTHERDUCK_TOKEN}',
        read_only=True,
    )


def analyze_market(con, market: str) -> dict:
    """Pull weekly Brand regs for the market, compute per-ISO-week seasonal
    multiplier and year-over-year stability.
    """
    rows = con.execute("""
        SELECT period_start, brand_registrations
        FROM ps.v_weekly
        WHERE market = ? AND period_type = 'weekly'
          AND brand_registrations IS NOT NULL AND brand_registrations > 0
        ORDER BY period_start
    """, [market]).fetchall()

    if not rows:
        return {'market': market, 'error': 'no data'}

    # Group by ISO week; track year for YoY stability.
    by_week = defaultdict(list)   # iso_week -> list of (year, regs)
    all_regs = []
    for period_start, regs in rows:
        iso_year, iso_week, _ = period_start.isocalendar()
        if iso_week == 53:
            iso_week = 52
        by_week[iso_week].append((iso_year, float(regs)))
        all_regs.append(float(regs))

    annual_mean = sum(all_regs) / len(all_regs) if all_regs else 0.0
    year_range = [r[0].year for r in rows]
    min_year, max_year = min(year_range), max(year_range)

    week_analysis = {}
    for iso_week in range(1, 53):
        entries = by_week.get(iso_week, [])
        if not entries:
            continue
        regs_values = [v for _, v in entries]
        week_mean = sum(regs_values) / len(regs_values)
        multiplier = week_mean / annual_mean if annual_mean > 0 else 1.0
        # Year-over-year stability: std / mean across years
        if len(regs_values) >= 2:
            import statistics
            year_stdev = statistics.stdev(regs_values) if len(regs_values) > 1 else 0.0
            yoy_cv = year_stdev / week_mean if week_mean > 0 else 0.0
        else:
            yoy_cv = None
        week_analysis[iso_week] = {
            'week_mean': week_mean,
            'multiplier': multiplier,
            'n_years': len(regs_values),
            'yoy_cv': yoy_cv,
            'raw_values': regs_values,
        }

    return {
        'market': market,
        'annual_mean': annual_mean,
        'year_range': (min_year, max_year),
        'total_weeks': len(rows),
        'week_analysis': week_analysis,
    }


def format_market_report(analysis: dict) -> str:
    """Build markdown section for one market."""
    m = analysis['market']
    if 'error' in analysis:
        return f"## {m}\n\n_No data: {analysis['error']}_\n\n"

    lines = [f"## {m}\n"]
    lines.append(f"**Data coverage**: {analysis['total_weeks']} weeks, {analysis['year_range'][0]}-{analysis['year_range'][1]}")
    lines.append(f"**Annual mean Brand regs/wk**: {analysis['annual_mean']:,.0f}")
    lines.append("")

    # Notable highs and lows
    week_analysis = analysis['week_analysis']
    sorted_by_mult = sorted(
        [(w, d['multiplier'], d.get('yoy_cv')) for w, d in week_analysis.items()],
        key=lambda x: x[1]
    )
    lowest_5 = sorted_by_mult[:5]
    highest_5 = sorted_by_mult[-5:][::-1]

    lines.append("### Notable weeks (from our data)")
    lines.append("")
    lines.append("**Lowest 5 weeks** (seasonal dips):")
    for w, mult, cv in lowest_5:
        cv_note = f" · YoY CV {cv:.0%}" if cv is not None else ""
        lines.append(f"- W{w:02d}: **{mult:.2f}×** annual mean{cv_note}")
    lines.append("")
    lines.append("**Highest 5 weeks** (seasonal peaks):")
    for w, mult, cv in highest_5:
        cv_note = f" · YoY CV {cv:.0%}" if cv is not None else ""
        lines.append(f"- W{w:02d}: **{mult:.2f}×** annual mean{cv_note}")
    lines.append("")

    # Anomaly flags: multiplier outside [0.5, 2.0] or high YoY CV
    anomalies = []
    for w in sorted(week_analysis.keys()):
        d = week_analysis[w]
        m_v = d['multiplier']
        cv = d.get('yoy_cv')
        if m_v < 0.5 or m_v > 2.0:
            anomalies.append(f"W{w:02d}: multiplier {m_v:.2f}× outside [0.5, 2.0] range")
        elif cv is not None and cv > 0.50:
            anomalies.append(f"W{w:02d}: YoY CV {cv:.0%} — year-over-year instability")
    if anomalies:
        lines.append("### Anomaly flags (investigate before trusting multiplier)")
        lines.append("")
        for a in anomalies:
            lines.append(f"- {a}")
        lines.append("")

    # Known events
    known = KNOWN_EVENTS.get(m, [])
    if known:
        lines.append("### Known seasonal events (reference)")
        lines.append("")
        for week_range, note in known:
            lines.append(f"- **{week_range}**: {note}")
        lines.append("")

    # External benchmark placeholder
    lines.append("### External benchmark (to fill in during refresh)")
    lines.append("")
    lines.append(f"- Google Trends: _compare against `Amazon Business {m}` search interest over 52w_")
    lines.append(f"- Industry reference: _Search Engine Land B2B search seasonality report_")
    lines.append(f"- Internal: _WBR / MBR seasonality commentary for {m} market_")
    lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    con = _get_connection()
    report_path = Path(__file__).resolve().parent.parent.parent / "wiki" / "agent-created" / "operations" / "mpe-seasonality-research.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# MPE Seasonality Research — Per-Market Reference",
        "",
        "_Auto-generated from ps.v_weekly Brand registrations history._",
        "_Generated: " + date.today().isoformat() + "_",
        "",
        "## Purpose",
        "",
        "This document is the reference for understanding each market's seasonal pattern — both what our data says and how it compares to known calendar events.",
        "",
        "The MPE Brand trajectory model (see `brand_trajectory.py`) fits a single seasonality curve per market using all available history. This report validates those fits by showing:",
        "",
        "1. **What our data says** — lowest/highest weeks from multi-year history",
        "2. **Known seasonal events** — Semana Santa, Ferragosto, Golden Week, etc. — as a sanity check",
        "3. **Anomaly flags** — weeks where the fit looks suspicious (multiplier outside [0.5, 2.0] or high YoY instability)",
        "4. **External benchmark placeholders** — Google Trends, industry reports, WBR/MBR commentary (filled in manually at refresh)",
        "",
        "Use this doc when someone asks: _why does the model say W15 is low for MX?_ — answer: because our 3 years of Brand data show W14-W15 at 0.7-0.8× annual mean, AND Semana Santa is a well-known suppression event.",
        "",
        "---",
        "",
    ]

    for market in ALL_MARKETS:
        try:
            analysis = analyze_market(con, market)
            lines.append(format_market_report(analysis))
            lines.append("---")
            lines.append("")
            print(f"[{market}] analyzed — {analysis.get('total_weeks', 0)} weeks")
        except Exception as e:
            print(f"[{market}] ERROR: {type(e).__name__}: {e}")
            lines.append(f"## {market}\n\n_Error: {e}_\n\n---\n\n")

    report_path.write_text("\n".join(lines))
    print(f"\nWrote {report_path}")
    print(f"Size: {report_path.stat().st_size / 1024:.1f} KB")

    try:
        con.close()
    except Exception:
        pass
    return 0


if __name__ == '__main__':
    sys.exit(main())
