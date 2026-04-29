# MPE Dashboard — R19 Cleanup + Feature Handoff to Kiro SSH

**From:** Local Kiro (verification + spec)
**To:** Kiro SSH (ship)
**Date:** 2026-04-28
**Mockup source of truth:** `agent-bridge/context/intake/mpe-proposed-changes-mockup.html`
**Backlog tracker:** `agent-bridge/dashboards/mpe-findings.md`
**Current commit verified:** 989f62b (Chart.js swap + MX 75% target seeded + URL state live)

---

## Context for this handoff

Richard did R19 review on the feature-complete projection dashboard after the Chart.js swap and MX 75% seed landed. I did a research-grounded teardown (practitioner dashboard benchmarks — 75% of dashboards useless, 20% adoption; agentic-UX patterns — progressive disclosure, confidence visualization, action-over-report) plus a live JS probe of the rendered page:

- **15 distinct font sizes rendering** vs 6 declared in the design system (fractional px from `0.65em` and `em`-on-`<input>` overrides)
- **2,808px page height** vs 865px viewport (3.2× scroll)
- **545px dead gap** between chart and contribution panel from closed `<details>` disclosures reserving layout space
- **149px gap** from hidden feedback-bar also reserving space
- **20 always-visible regions** vs Miller's 7±2 working-memory target

The mockup HTML file has 13 proposals, each with:
- Before/after panels using real MPE design tokens
- Code snippet (CSS/HTML/JS) ready to drop in
- Acceptance criteria
- Priority badge (HIGH/MED/LOW)
- Effort estimate

Open the mockup file in a browser to see visual before/after for each proposal — it renders cleanly and is the spec.

---

## Ship order (one finding per commit, per protocol)

Single sprint, all 13 proposals. Ordered by compounding effect — structural cleanup first (whitespace + dupe kill reveal what else is off), then typography (locks the visual system), then features (built on a clean base), then deferred items last so they don't block the high-value work. Total: ~6.5h.

1. **#13 Whitespace cleanup** (HIGH, 20 min) — close the 545px dead gap below chart. Trim `details.sec-panel:not([open])` padding, hide feedback-bar gap when feedback-bar is hidden, wrap below-chart sections in a uniform-gap grid so accidental double-gaps can't happen. Acceptance: total page height drops from 2,808px to ~1,800px measured via `document.documentElement.scrollHeight`.

2. **#1 Remove Brand/NB split chip** (MED, 5 min) — duplicates Brand and NB KPI tiles directly above it. Pure delete. Acceptance: chip element no longer in DOM; Brand/NB split is readable from the KPI row.

3. **#4 Hide Saved Projections when empty** (LOW, 5 min) — trivial empty-state noise removal. Acceptance: panel renders only when `savedProjections.length > 0`.

4. **#3 Default-close Model View drawer** (MED, 10 min) — reclaims ~25% horizontal space on first load. Drawer stays fully functional; just flip the default state. Acceptance: `aside.model-view` has `hidden` attribute or collapsed class on `DOMContentLoaded`; click-to-open works; state persists in localStorage per prior pattern.

5. **#9 Fit Quality empty-state copy rewrite** (LOW, 10 min) — "Fit quality not yet measured" → "Confidence: limited history, 3 weeks of pred_regs". Acceptance: copy updates for all markets in backtest empty state.

6. **#7 Collapse VS OP2 tiles** (MED, 30 min) — merge "VS OP2 SPEND" + "VS OP2 REGS" into a single "VS OP2" tile with two sub-rows (spend + regs). Preserves both signals, removes a tile. Acceptance: single tile renders both metrics with directional arrows; KPI row count drops by 1.

7. **#2 Merge Warnings + Model Alerts** (MED, 30 min) — one alert stream instead of two parallel ones. Preserve severity chips. Acceptance: single `#alerts` panel renders both categories; Warnings and Model Alerts containers no longer both in DOM.

8. **#12 Typography consolidation (15 → 5)** (HIGH, 1h) — define 5 named tokens: `--size-hero: 64px`, `--size-h1: 24px`, `--size-h2: 20px`, `--size-body: 16px`, `--size-ui: 13px`, `--size-meta: 11px`. Grep-kill overrides for `64px`, `48px`, `28px`, `22px`, `18px`, `14px`, `0.65em`, `em`-on-inputs. Promote current 13px de-facto UI size to `--size-ui`. Acceptance: `document.querySelectorAll('*')` mapped through `getComputedStyle(el).fontSize` yields ≤6 distinct values (5 tokens + inherited).

9. **#6 CI quality label + plan-in-range flag** (HIGH, 30 min) — turns the 56%-wide MX CI from noise to signal. Label: "Confidence: wide (56% range)" or "Confidence: tight (12% range)". Flag: "OP2 plan is within range" or "OP2 plan is $X outside CI". Acceptance: both labels render on KPI row; thresholds defined in config (wide ≥ 40%, medium 20-40%, tight < 20%).

10. **#5 "Since last week" auto-summary** (HIGH, 45 min) — renders above the narrative. Auto-generated: "Brand spend ↑ 5.6% WoW; NB spend ↑ 17.4% WoW; CI widened from 42% to 56%." Pulls from existing WoW deltas + prior week's CI width. Acceptance: section renders on load with last-week comparison; empty-state handled ("First week of projection — no prior data").

11. **#10 Cross-market pulse strip** (MED, 45 min) — horizontal strip above single-market view showing spend delta + CI state per market. If data wiring not already in projection-data.json, emit BLOCKED-with-root-cause and skip to #8. Acceptance: strip renders with all 10 markets; each chip links to that market's view.

12. **#8 Action-first alerts** (HIGH, 1h) — rewrite current model alerts from report-style ("Brand CPA fit weakened") to action-style ("Trust this projection less — Brand CPA fit weakened; suggested action: rerun Pessimistic scenario"). Acceptance: every alert has a `data-action` attribute + visible action phrase; alert copy reviewed against `richard-style-docs` voice.

13. **#11 Confidence timeline sparkline** (LOW, 30 min + pipeline) — sparkline in Model View drawer showing CI width over time. Blocked on historical CI widths being persisted. If pipeline doesn't exist, emit BLOCKED-with-root-cause identifying the missing data surface and skip.

---

## Commit discipline

Per Richard's protocol, every commit needs:
- **Finding** — what user-visible behavior changed
- **Verification** — how to reproduce before/after
- **Blast radius** — which markets / screens / functions are touched

Example commit message for #13:
```
fix(dashboard): Close 545px dead gap below projection chart

Finding: closed <details> disclosures reserved 545px of vertical space
even when collapsed; feedback-bar reserved 149px when hidden. Page
rendered 2,808px tall in an 865px viewport (3.2× scroll).

Verification: cold-load /projection.html → measure
document.documentElement.scrollHeight. Before: 2,808px. After: ~1,800px
(MX Y2026, default state). Visual check: no gap between chart and
contribution panel.

Blast radius: projection.html only. All markets. No state changes. No
data changes. CSS-only.
```

One finding per commit. No batching.

---

## Verification handoff back to Local Kiro

After each commit lands, I'll:
1. Pull to latest SHA
2. Clear localStorage, cold-load `/projection.html`
3. Walk the acceptance criteria
4. Screenshot full-page + any affected region to `agent-bridge/context/intake/mpe-r19-post-{N}-{topic}.png`
5. Flag regressions; update `mpe-findings.md` with P-ID → status
6. Ping you in next turn with "clean on #X" or "regression: [description]"

If you're blocked on any proposal, use the BLOCKED-with-root-cause pattern — surface the specific blocker, not a silent skip. Forecast inflation masquerading as scope discipline is an anti-pattern we've named.

---

## Reference files Kiro SSH should read before starting

- `agent-bridge/context/intake/mpe-proposed-changes-mockup.html` — the 13 proposals with before/after + code + acceptance
- `agent-bridge/dashboards/projection.html` — current source
- `agent-bridge/dashboards/projection-app.js` — main app logic
- `agent-bridge/dashboards/projection-chart.js` — Chart.js module (already shipped)
- `agent-bridge/dashboards/projection-design-system.css` — CSS tokens (this is where #12 lands)
- `agent-bridge/dashboards/mpe-findings.md` — 48-item backlog; update status entries as you close proposals

— Local Kiro
