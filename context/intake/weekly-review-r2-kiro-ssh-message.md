# Weekly Review R2 — Handoff Message to Kiro SSH

**Copy everything below the line and paste into Kiro SSH chat. Don't edit — the repo refs are precise.**

---

R2 consolidated spec is ready. Congrats on closing the R1 sprint — 19/19 shipped with the full reconciliation + follow-up discipline documented in `weekly-review-findings.md`. That doc is the cleanest tracker in the repo right now and I lifted several gating notes from it (A8 structured events, A9 prediction snapshots, B6 period-state flag) into the R2 spec.

**What's new on this pull:**
- `context/intake/weekly-review-r2-consolidated-mockup.html` — 23-finding mockup covering R1 live-probe bugs, a deep nitpick sweep, 4 structural moves, and the 6 R2 research ideas you already surfaced in the findings doc
- `context/intake/weekly-review-r2-consolidated-preview.png` — rendered preview
- `context/intake/weekly-review-r1-verification-results.md` — my live-probe results from when the chrome-devtools lock cleared on my side (12 pass / 2 partial / 0 fail across WW/US/EU5/JP)
- 8 MPE R19 artifacts in `context/intake/` that were never committed during the MPE sprint, landed now for durability

**How the R2 mockup relates to your R1 findings doc:**

Your doc already has the 8 R2 proposals (A7, A8, A9, A10, A11, B5, B6, C3) — I'm not duplicating those. What the R2 mockup adds is **17 findings your doc doesn't have**, split into 3 buckets:

1. **Live-probe bugs (3):** surfaced from my cold-load verification across WW/US/EU5/JP:
   - **Finding #1 — Three-Q cards 1+2 render as literal `—` on WW rollup** (US, JP render correctly; WR-D5 extractor needs a rollup-aware branch)
   - **Finding #2 — Variance waterfall shows "Decomposition needs both Brand and Non-Brand prior-week data" on WW** (WR-D6 needs a rollup path — market-level decomposition works since `callout.market_breakdown[].regs_wow` is populated)
   - **Finding #3 — `section-freshness.json` 404 on every load** (cosmetic, path resolution in the shared script fetches `/performance/data/` instead of `/data/`)

2. **Nit polish (10):** from a deep-probe pass looking for MPE-level quality parity:
   - `.sec-panel` computed `padding: 0px` (content sits flush against card edges, MPE panels have `20px 24px`)
   - 152px dead gap between sec-scorecard and sec-trend (grid row height stretching — `align-items: start` fixes it)
   - TOC link order doesn't match rendered page order (TOC lists Scorecard-KPIs-Trend-Detail-Callout-Channels-Context but rendered order is Callout-Variance-KPIs-Scorecard-Charts-Detail-Channels-Context)
   - Narrative card uses H3 for body prose, not a section title (screen readers hear "US drove 9.4K registrations..." as an H3 heading)
   - H2 level skipped entirely — page jumps H1 → H3 with 0 H2s
   - Zero semantic landmarks (no `header`, `main`, `nav`, `aside`)
   - Canvases missing `aria-label` + `role="img"`
   - Week selector `<select>` has no accessible label
   - Thread strip lacks `role="group"` + aria-label
   - Calibration H3 swallows the Regs/Spend/Both axis toggle (toggle is nested inside the H3, not adjacent)

3. **Structural moves (4):**
   - Page is 3,820px tall (4.4× scroll) — apply progressive disclosure to secondary panels (weekly detail, channel detail, context+drivers+stakeholders) to land ~1,800px on cold load
   - Scorecard + KPIs side-by-side instead of stacked (eliminates the 152px gap, matches how Kate reads "where are we / how good is the forecast" in one glance)
   - Brand/NB channel cards show empty rows on WW rollup — hide or replace with per-market breakdown table
   - Weekly detail table has `max-height: 520px; overflow: auto` creating a scroll-within-scroll trap (pair with progressive disclosure — wrap in `<details>` and let it flow inline when open)

Every finding in the mockup has: probe evidence (verbatim JSON from my chrome-devtools-mcp calls), before/after visual, code snippet, and acceptance criterion with a verification script.

**Suggested ship order — 3 sprints:**

- **Sprint 1 (2.5h, 7 commits):** Findings 1-6 + 14. Closes all 3 live bugs + 4 HIGH-priority polish items + progressive disclosure. Kills the leadership-demo risk (empty dashes on Kate's default WW view).
- **Sprint 2 (2h, 10 commits):** Findings 7-13 + 15-17. Remaining polish + structure for MPE a11y parity.
- **Sprint 3 (6.5h, 6 commits):** The 6 R2 research ideas from your findings doc — use your ship order (A10 → A8 → C3 → A7 → A11 → B5, with B6/A9 holding for pipeline work).

**Seed these 17 new findings into `weekly-review-findings.md` under a new "R2 consolidated (Local Kiro, 2026-04-29)" section** so the tracker stays the single source of truth. IDs: WR-B1-1 through WR-B1-3 (bugs), WR-P3 through WR-P12 (polish), WR-S1 through WR-S4 (structural). Adjust IDs to match your convention.

**Commit discipline:** one finding per commit, Finding / Verification / Blast radius format, same as the R1 sprint. After each commit flip status in `weekly-review-findings.md`. I'll cold-load, walk acceptance criteria, screenshot, and post back "clean on #X" or "regression: [description]."

Example commit message for Finding #1:

```
fix(weekly-review): Make three-question extractor rollup-aware

Finding: on ?market=WW&week=W17, cards 1 and 2 of the three-question framing
render as literal em-dash. US and JP render correctly. Bug is rollup-specific
— WR-D5 renderThreeQ extracts from callout.brand_detail and callout.nb_detail
which don't exist on WW rollup payload.

Verification: cold-load /performance/weekly-review.html?market=WW&week=W17.
Before: [...document.querySelectorAll('.wr-q-body')].map(e=>e.textContent)
returns ['—', '—', 'Latest week +19.2% vs weekly OP2. Pacing ahead.']. After:
all three cards populate with rollup-synthesized sentences from
callout.market_breakdown (top gainer, top decliner, total market count).

Blast radius: weekly-review.html only. WW / EU5 / NA rollup markets changed.
Per-country markets (US/CA/UK/DE/FR/IT/ES/JP/MX/AU) path unchanged.
```

**Reference bundle in this commit:**
- `context/intake/weekly-review-r2-consolidated-mockup.html` — the spec (23 findings, inline SVG/CSS mocks, zero external asset deps)
- `context/intake/weekly-review-r2-consolidated-preview.png` — rendered preview
- `context/intake/weekly-review-r1-verification-results.md` — cold-load probe results across 4 markets

**Chrome-devtools lock on my side is clear** now — your findings doc note about pending live-probe verification is resolved. Full live-probe results shipped in `weekly-review-r1-verification-results.md`.

Ping me when Sprint 1's first commit lands and I'll start verification.

— Local Kiro
