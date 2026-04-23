---
title: "Head-to-head — Grok anomaly_detector.py vs MX W16 analyst workflow"
owner: Richard Williams
created: 2026-04-22
status: FINAL
---

# Grok's `anomaly_detector.py` vs the MX W16 analyst workflow

**TL;DR:** Grok's script is a toy. On the same week of MX data the existing analyst workflow surfaces 8 meaningful signals (a 3-week NB CVR decline, NB CPA at a multi-month high, NB CPC at a 12-week high, a Brand coverage-scaling anomaly, a soft Saturday, an ie%CCP cadence change, an active Slack thread, and a forecast-model miss). Grok's script surfaces 11 day-over-day spikes, every one of which is weekday/weekend cadence, zero of which are anomalies. It also doesn't run — wrong table name, wrong column model, wrong cadence.

**Verdict: existing >> Grok.** Not a tie, not different scope. Grok is strictly worse at the job the analyst workflow already does.

---

## 1. What Grok actually wrote

```python
def detect_anomalies(days_back=7):
    query = f"""
    SELECT metric, value, date,
           LAG(value) OVER (PARTITION BY metric ORDER BY date) as prev_value
    FROM ps
    WHERE date >= CURRENT_DATE - {days_back}
    """
    # Agent should run this and flag anything with >25% day-over-day change
    # Then append to daily output under "Data Snapshot"
    return "Run DuckDB query above and flag anomalies >25% change"
```

Six lines of real logic. The function returns an instruction string, not anomalies. The "implementation" is: agent, please do this yourself.

### Bugs before logic

1. **Table doesn't exist.** `FROM ps` — there is no `ps` table. The schema has `ps.v_daily`, `ps.v_weekly`, `ps.v_monthly`, `ps.v_quarterly`, `ps.forecasts`, `ps.targets`. The script would error on first execution.
2. **Wrong data model.** The query assumes long format (`metric`, `value`). Our tables are wide: `registrations`, `cost`, `nb_registrations`, `brand_registrations`, `nb_cvr`, `brand_cvr`, etc. No `metric` column exists.
3. **Weekly metrics don't have a daily cadence.** The script uses `LAG` over `ORDER BY date`. For weekly regs/spend/CPA, "yesterday's value" is meaningless. If run against `v_weekly` it would lag week N vs week N-1, which is just WoW — and the analyst already does WoW, with context.
4. **Date math is sloppy.** `CURRENT_DATE - {days_back}` interpolates an int into SQL. DuckDB accepts it but it's the kind of thing that breaks silently when `days_back` is passed as a string.
5. **No market filter.** If this ever ran, it would pool all markets together, producing nonsense LAG values (WW one row, AU the next).

### Principle check (How I Build)

- Violates **#3 Subtraction before addition** — this adds a new component that duplicates the ingester's existing anomaly detection (7-week baseline, deviation-based) with inferior logic.
- Violates **#6 Reduce decisions, not options** — an 11-flag false-positive list increases the analyst's decision load, doesn't reduce it.
- Violates **#2 Structural over cosmetic** — the output lands in the daily brief's "Data Snapshot", not in the callout or analyst brief where anomaly judgement happens. Wrong surface.

## 2. What the existing MX W16 analyst workflow surfaces

Source: `shared/wiki/callouts/mx/mx-analysis-2026-w16.md` — Flags and Anomalies sections.

**Flags (8 signals, all meaningful):**

| # | Signal | Why it matters |
|---|---|---|
| 1 | NB CPA +29% WoW to $183 | Highest since W9. The real watchpoint. Drives the "pause, don't scale NB" recommendation. |
| 2 | NB CVR -14.6% WoW (1.32% → 1.13%) | Third straight week of decline. Below the post-restructuring baseline. Possible query-mix drift / LP issue / competitor IS. |
| 3 | NB CPC $2.07 — 12-week high | Bid strategies paying more per click. Mechanical driver of the NB CPA spike. |
| 4 | Brand regs +77% above 7-week baseline | Ingester-flagged positive anomaly. Expected given coverage ramp. Noted, no action. |
| 5 | Sat Apr 18 daily regs at 31 | Below typical weekend ~41. Single-day noise so far; watch next weekend. |
| 6 | ie%CCP cadence change (monthly → quarterly) | Signal from Stacey via Kate/Fernando. Changes reporting rhythm; callout should note. |
| 7 | mx-budget-ieccp thread (strength 5.5, 2 reinforcements) | Active cross-team signal; connects to Brandon's mx-budget-transparency question. |
| 8 | ps.forecasts W16 SURPRISE | Bayesian model predicted 304 regs, actual 510. Priors need refresh. Feeds forecast pipeline. |

**Anomalies (ingester-flagged, 5):** Brand regs +77%, Brand CVR +30%, Regs +47%, Cost +26%, Blended CVR +26% — all above 7-week baseline. All positive, all consistent with Brand coverage scaling, none actionable.

**Key property:** the analyst brief **explicitly notes** that "the non-flagged NB CPA spike to $183 is the real watchpoint." The most important signal of the week is the one the ingester's baseline-based detector *missed*, and the analyst caught it via WoW reasoning + 5-week CVR trend + CPC trend + the post-restructuring baseline context. None of that context exists in Grok's script.

## 3. What Grok's script would produce on the same data

Ran the equivalent query (`ps.v_daily`, wide columns, MX filter) for W16 (2026-04-12 → 2026-04-18). Day-over-day % changes:

| Date | DoW | Regs | Regs % | Cost % | NB regs % | NB cost % | Brand regs % | Brand cost % |
|---|---|---|---|---|---|---|---|---|
| 04-12 | Sun | 51 | — | — | — | — | — | — |
| 04-13 | Mon | 89 | **+74.5** | **+25.8** | -12.5 | +11.9 | **+114.3** | **+108.5** |
| 04-14 | Tue | 77 | -13.5 | +1.9 | +21.4 | -1.3 | -20.0 | +12.0 |
| 04-15 | Wed | 74 | -3.9 | +7.4 | +17.6 | +9.6 | -10.0 | +1.2 |
| 04-16 | Thu | 99 | **+33.8** | -2.8 | +10.0 | -1.4 | **+42.6** | -7.1 |
| 04-17 | Fri | 89 | -10.1 | +22.8 | **-27.3** | -19.4 | -5.2 | **-33.7** |
| 04-18 | Sat | 31 | **-65.2** | -17.8 | **-37.5** | -18.6 | **-71.2** | -14.4 |

**Bold = Grok's >25% threshold triggers. 11 flags total.**

### What every flag actually means

- **Sun→Mon (4 flags):** Sunday is the weekest day of the week in MX paid search; Monday is a normal weekday peak. Brand especially is dominated by weekday search volume. Every Monday morning, Grok's script would scream. Every Monday morning, this would be the noise floor.
- **Wed→Thu (2 flags):** Thursday was the week's peak day (99 regs). Within normal weekly cadence.
- **Thu→Fri (2 flags):** Friday is the softest weekday. NB regs dropping Thu→Fri is normal.
- **Fri→Sat (3 flags):** Saturday is a weekend day. The -65% regs drop is the weekend cadence. Note that the analyst *did* flag Saturday's 31 regs — but framed correctly: "below typical weekend ~41, single-day noise." Grok would flag it as a -65% DoD drop, which is the weekend falling, not an anomaly.

### False positives: 11. True positives: 0.

The ingester's 7-week-baseline detector already surfaces the Brand coverage-scaling anomaly at the right grain (weekly, vs a rolling baseline, with direction context). Grok's daily-DoD detector catches none of the eight meaningful signals the analyst surfaces:

- NB CPA +29% WoW — Grok can't see this. NB CPA isn't in `v_daily` as a column (it's derived), and even if it were, DoD on daily CPA is hostage to daily reg counts hitting 10 vs 22.
- NB CVR 3-week decline — Grok's 7-day window can't see a 5-week trend.
- NB CPC at 12-week high — requires 12-week context; Grok looks back 7 days.
- Forecast model SURPRISE — Grok doesn't read `ps.forecasts`.
- Slack/Hedy signals — Grok doesn't touch `signals.signal_tracker`.
- ie%CCP cadence change — not in `v_daily` at all.

## 4. Would Grok's output "land naturally" in the daily brief Data Snapshot?

No. The Data Snapshot section surfaces yesterday's vs trend context for executional triage ("did something break overnight"). 11 DoD flags a week, 100% weekday/weekend cadence, would be:

1. **Ignored within a week.** Analysts learn to ignore boy-who-cried-wolf detectors faster than they learn to trust them.
2. **Worse than nothing.** The current Data Snapshot omission is defensible ("no news"). A Data Snapshot filled with false alarms is actively harmful — it trains the reader to skip the section.
3. **Redundant with the 7-week baseline ingester anomaly logic** which already runs and which the analyst references directly.

## 5. Signal quality scorecard

| Dimension | Existing analyst workflow | Grok's `anomaly_detector.py` |
|---|---|---|
| Runs at all | Yes | No (wrong table, wrong columns) |
| Real anomalies caught on MX W16 | 8 meaningful flags + 5 ingester anomalies | 0 |
| False positives on MX W16 | 0 (analyst frames Brand anomaly as expected) | 11 (all weekday/weekend cadence) |
| Trend context (multi-week) | Yes (5-wk CVR, 8-wk regs, 12-wk CPC) | No (7-day window only) |
| Cross-source signal integration | Yes (Slack, Hedy, ps.forecasts, signals.signal_tracker) | No |
| Right grain for weekly metrics | Yes (WoW on weekly, DoD on daily) | No (DoD on everything) |
| Correctly framed outputs | Yes ("this is expected", "this is the real watchpoint") | No (undifferentiated flag list) |
| Next-action guidance | Yes ("pull NB SQR this week") | No |

## 6. Verdict

**Existing >> Grok.** Not different scope — same scope (surface anomalies in recent MX performance data), and the existing workflow is strictly better on every dimension. Grok's script:

- Doesn't run as written.
- Even if fixed, flags weekend cadence as anomalies.
- Misses the actual story of the week (NB CVR decline + NB CPA spike + NB CPC 12-week high).
- Would degrade the Data Snapshot section, not improve it.

**Richard should not adopt.** If a daily anomaly detector is wanted, the right move is to extend the existing ingester's 7-week baseline logic to run daily on `v_daily`, with a market filter, weekday/weekend-aware baselines, and a tie-in to the analyst brief — not to replace it with Grok's DoD threshold.

### Recommendation

- **Delete** `shared/tmp/grok-eval-2/proposed/02-anomaly_detector.py` from the adoption candidate list.
- **Keep** the existing analyst → writer → reviewer callout pipeline.
- **Principle embodied:** *Subtraction before addition* (How I Build #3). The existing ingester + analyst brief already covers this surface area with higher signal quality. Adding Grok's detector doubles the surface with lower-quality output. Reject.

---

*Comparison data source: `ps.v_daily` MotherDuck, 2026-04-12 to 2026-04-18. Analyst brief: `shared/wiki/callouts/mx/mx-analysis-2026-w16.md`.*
