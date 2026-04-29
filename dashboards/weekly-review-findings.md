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
