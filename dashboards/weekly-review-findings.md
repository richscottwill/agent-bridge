# Weekly Review — Findings Backlog

Canonical status tracker for the weekly-review R1 sprint (Local Kiro review,
2026-04-28). Mirrors the `mpe-findings.md` pattern for the projection engine.

**Cadence:** one finding per commit. Status values: `open` | `in-progress` |
`done` | `verified` | `blocked` | `obsolete`.

**"done"** = landed on disk + regression green.
**"verified"** = Local Kiro pulled + walked the verification visually.

**Source bundles:**
- `~/shared/context/intake/weekly-review-r1-handoff-prompt.md` — 12 proposals (A1-A6, B1-B4, C1-C2) framing weekly-review as "the forecast grading rubric for the projection engine"
- `~/shared/context/intake/wbr-proposed-changes-mockup.html` — 13 proposals (correctness + duplication + density + UX)

Both bundles audited against live code + data before execution. 19 reconciled
findings shipped in 17 commits (WR-B3 verified-already-done, no commit).

---

## Sprint summary — shipped 2026-04-28

| # | Finding | Status | Commit |
|---|---|---|---|
| WR-C1 | safeWoW helper (symmetric WoW thresholds + 0-prior guard) | done | `efd9082` |
| WR-C2 | Two-timestamp collapse (single header freshness) | done | `edfea36` |
| WR-C3 | Callout headline de-duplication | done | `760e193` |
| WR-C4 | Regs/Pred column → vs-Pred delta | done | `6d5f486` |
| WR-C5 | Remove Projections sub-panel | done | `7c42d2e` |
| WR-C6 | KPI cleanup — drop YE Pred + add OP2 Pacing | done | `bac7382` |
| WR-C7 | EU5 member-market union (UK/DE/FR/IT/ES) | done | `b634b05` |
| WR-B1 | Metric controls as segmented control | done | `27f586f` |
| WR-B2 | Typography token sweep | done | `4d842d0` |
| WR-B3 | Now-line on default chart | done (already present in canon-chart.js) | n/a |
| WR-P1 | URL state + explicit latest-week default | done | `2de9a5c` |
| WR-P2 | Metric-tab persists per market | done | `0273fac` |
| WR-D1 | Forecast Hit Rate scorecard | done | `268cece` |
| WR-D2 | Calibration first-class panel + axis toggle | done | `97a8ca2` |
| WR-D3 | Callout narrative goes first | done | `982f523` |
| WR-D4 | Since-last-week auto-summary | done | `15ee67a` |
| WR-D5 | Three-question WBR framing | done | `f1dc7d2` |
| WR-D6 | Variance decomposition waterfall | done | `bb213f6` |
| WR-D7 | Prior-week thread strip | done | `a2ea608` |

Findings doc seeded in `c057d9f` (reconciliation + backlog).

---

## Reconciliation with live code (2026-04-28 audit)

Before executing I ran a live audit — Local Kiro's claims need grounding, per
the logged discipline "audit bundled specs against live code before executing."

**Verified claims:**
- `predictions_history` exists in `forecast-data.json` for all 12 markets incl. EU5 — A1 scorecard has its data.
- `brand_detail.lw_regs` + `nb_detail.lw_regs` exist in `callout-data.json` — A4 variance decomposition CAN derive WoW deltas.
- `metrics.regs_wow / spend_wow / cpa_wow` exist — since-last-week summary has fields.
- Line 762 weekly-review.html `wow > 0 ? 'good' : wow < -5 ? 'bad' : 'warn'` — wbr-#1 asymmetry bug was real.
- Line 446 `chartModeBtn` — wbr-#9 toggle was real; became moot after r1-A2 (toggle removed in favor of two panels).
- Line 786 `Year-End Pred` tile — real; r1-C2 + wbr-#6 agreed it should go.
- Line 512 market filter used intersection — wbr-#4 EU5 gap was real. Callout markets = 7, forecast markets = 12.
- `predictions_history[market][wk]` has richer shape than the spec assumed: `first_pred`, `latest_pred`, `actual`, `first_ci_lo/hi`, `latest_ci_lo/hi`, `error_pct`, `score` (HIT/MISS) — A1 is well-fed.

**Partial/conditional claims:**
- `callout.projections` is **empty `{}`** for current weeks (W17/W16) on all markets. Populated only on W15 and earlier. **WR-D5 qPacing and WR-C6 OP2 Pacing** have empty-state fallbacks on current weeks until the next refresh-callouts.py run populates them. Not a blocker — empty states shipped as part of the spec.

**Bundle overlaps resolved:**
- r1-B4 (OP2 pacing tile) + wbr-#6 (replace passive OP2 Target with vs-OP2 delta) + r1-C2 (remove YE Pred) → one commit (WR-C6) replacing YE Pred with a directional OP2 pacing tile.
- r1-A2 (calibration first-class) + wbr-#10 (reduce calibration line count) → one commit (WR-D2) promoting calibration AND defaulting to regs-only axis inside the new panel.
- r1-B1 (typography lock, rides MPE P5-12) + wbr-#12 (token sweep on local overrides) → one commit (WR-B2) sweeping the .pred-lbl / .wr-proj-* / .wr-list local overrides to tokens.
- wbr-#9 (chart mode toggle state) became moot after r1-A2 landed — dropped.

---

## Order of work (shipped)

1. ✅ WR-C1 safeWoW
2. ✅ WR-C2 timestamp collapse
3. ✅ WR-C3 headline de-dup
4. ✅ WR-C4 Regs/Pred column → vs-Pred delta
5. ✅ WR-C5 remove Projections sub-panel
6. ✅ WR-C6 KPI tile cleanup (YE Pred + OP2 Target → OP2 Pacing)
7. ✅ WR-C7 EU5 member-market union
8. ✅ WR-B1 controls row rebalance
9. ✅ WR-B2 typography token sweep
10. ✅ WR-B3 now-line on default chart (already-done verification)
11. ✅ WR-P1 URL state + latest-week default
12. ✅ WR-P2 metric-tab persist per market
13. ✅ WR-D1 Forecast Hit Rate scorecard
14. ✅ WR-D2 calibration first-class + axis toggle
15. ✅ WR-D3 narrative first
16. ✅ WR-D4 since-last-week summary
17. ✅ WR-D5 three-question framing
18. ✅ WR-D6 variance decomposition
19. ✅ WR-D7 prior-week thread

**Sprint closed** — 19 / 19 shipped.

## Known follow-ups (out of sprint scope)

- **canon-chart.js light-theme polish:** the tracker/calibration render path still has hardcoded dark-theme axis tick colors (`#666` / `#1f222b`) and `color: '#4ade80'` on the nowLine label. Contrast is adequate on the light background but not polished. Low priority; pick up in a dedicated chart-polish commit.
- **Current-week projections populate:** WR-C6 OP2 Pacing and WR-D5 qPacing will remain in their weekly-fallback form on W17/W16 until `refresh-callouts.py` runs and populates `callout.projections.month_end.vs_op2_spend` for the current weeks. Pipeline concern, not code.

---

## R2 proposals (Local Kiro, 2026-04-28) — forecasting-platform research pass

Second-round ideas grounded in research on Good Judgment Open, Polymarket,
Metaculus, and Robinhood Advanced Charts. Source file:
`~/shared/context/intake/weekly-review-r2-handoff-prompt.md` (pasted into
the 2026-04-28 session; not yet in repo).

All R2 items are `open-R2` — research-grounded proposals awaiting Richard's
go-ahead. Not shipped. Data-dependency audit done against live payloads;
gating notes flag items that need pipeline work before shipping.

### WR-A7 · Relative forecast error (benchmark against naive baseline)
- **Source:** R2 (GJO Brier-relative pattern)
- **Priority:** MED · **Effort:** 45 min · **Depends on:** WR-D1
- **Data:** forecast-data.json weekly actuals + predictions_history — sufficient.
- **Status:** open-R2

### WR-A8 · Event annotations on trend chart
- **Source:** R2 (Polymarket context-overlay critique)
- **Priority:** HIGH · **Effort:** 1h (+ pipeline work for structured events)
- **Data audit:** `callout.external_factors` is list of `{text, important}` objects (5 items for US/W17). **Prose only — no structured `{week, label, kind}` triples.** Pinning to specific weeks would require either parsing week references out of prose (fragile) or extending `refresh-callouts.py` to emit structured events. **Gated on callout-pipeline schema extension.**
- **Status:** open-R2 (partially gated)

### WR-A9 · Forecast aging visualization (prediction trajectory per week)
- **Source:** R2 (GJO daily-Brier pattern)
- **Priority:** LOW · **Effort:** 2h + backend
- **Data audit:** `predictions_history[market][wk].regs.n_preds = 1` for all current rows; `first_date == latest_date`. **The week-by-week forecast evolution Local Kiro proposed isn't supported today.** Needs `predictions_history[market][wk]` to become an array of `{date, pred}` snapshots or a separate `prediction_snapshots` table. **Gated on forecast pipeline extension — correctly flagged by Local Kiro.**
- **Status:** open-R2 (gated — schema work required)

### WR-A10 · Scrub-the-chart interaction (cross-page lens)
- **Source:** R2 (Robinhood Advanced Charts)
- **Priority:** HIGH · **Effort:** 2h · **Depends on:** WR-D2, WR-D3, WR-D5
- **Approach:** hovering a chart week swaps KPI row / three-question cards / variance table / callout headline to that week's values. Release → return to selected week. Structural unlock — page becomes an interactive lens instead of a static view. Highest demo value per Local Kiro.
- **Data:** all callout weeks present in CALLOUTS.callouts[market]; no backend work needed.
- **Status:** open-R2

### WR-A11 · Specialized layouts per market archetype
- **Source:** R2 (Polymarket specialized-interface critique)
- **Priority:** MED · **Effort:** 1.5h · **Depends on:** WR-D1, WR-C6
- **Approach:** JP/AU show spend-discipline scorecard (YTD spend vs OP2 spend, CPC trends) instead of regs forecast hit rate. Three market archetypes: regs-and-efficiency (US/EU5/CA/MX), spend-only (JP/AU), rollups (WW/EU5).
- **Status:** open-R2

### WR-B5 · Cross-market accuracy leaderboard strip
- **Source:** R2 (GJO challenge-style leaderboard)
- **Priority:** MED · **Effort:** 1h · **Depends on:** WR-D1
- **Data audit:** predictions_history covers all 12 markets — **fully implementable now.**
- **Approach:** compact horizontal strip above market tabs showing each market's 6-week in-CI rate. Green ≥80%, red ≤50%. Answers "can I trust this market's projection?" in one glance for Kate.
- **Status:** open-R2 (ready to ship)

### WR-B6 · Period-state background tint on callout card
- **Source:** R2 (Robinhood color-state semantics)
- **Priority:** LOW · **Effort:** 20 min + pipeline
- **Data audit:** `callout.period` is plain text range ('Apr 19–25') — **no structured state flag.** Q-close / holiday / refit / normal distinction would need pipeline to emit something like `period_state: 'q_close' | 'holiday' | 'refit' | 'normal'`. **Gated on pipeline.**
- **Status:** open-R2 (gated)

### WR-C3 · Progressive disclosure — collapse secondary panels by default
- **Source:** R2 (Polymarket mobile-first principle)
- **Priority:** MED · **Effort:** 30 min · **Depends on:** R1 verified clean
- **Approach:** wrap Brand+NB cards behind "Channel detail" disclosure, wrap Context+Drivers+Stakeholders behind "Context" disclosure. Cold-load shows thread → narrative → 3Q → KPIs → 2 charts → variance only — the full WBR arc on one screen.
- **Status:** open-R2

### R2 recommended ship order (from Local Kiro)
1. WR-A10 scrub-the-chart (HIGH, 2h) — structural unlock
2. WR-A8 event annotations (HIGH, 1h + pipeline for structured events)
3. WR-C3 progressive disclosure (MED, 30 min)
4. WR-A7 relative error (MED, 45 min)
5. WR-A11 specialized layouts (MED, 1.5h)
6. WR-B5 accuracy leaderboard (MED, 1h — ready-to-ship, ungated)
7. WR-B6 period-state tint (LOW, 20 min + pipeline)
8. WR-A9 forecast aging (LOW, 2h + schema work — gated)

**Ready-to-ship without backend work (priority order):**
A10 → A7 → C3 → A11 → B5 → none-of-the-three-gated

**Gated on pipeline work:** A8 (structured events), A9 (prediction snapshots), B6 (period state flag).

---

## R1 verification probe (2026-04-28)

Static structural analysis written to
`~/shared/context/intake/weekly-review-r1-live-probe.txt`. 19/19 R1 findings
pass static checks (1 verification-only for WR-B3 confirmed in canon-chart.js).
Live browser probe pending — Local Kiro's chrome-devtools-mcp lock on
Richard's Windows side, not clearable from DevSpaces. Static analysis covers
15 of 19 checklist items directly; the other 4 (scrollHeight, viewport,
`getBoundingClientRect` positions, distinct computed font-sizes) need a real
browser.

**One follow-up commit triggered by probe:** `2e14a8d` WR-B2 follow-through
swapped the last literal `24px` (`.wr-score-value` from WR-D1 scorecard)
to `var(--size-section)`. Zero literal-px font-sizes remain in
weekly-review.html.
