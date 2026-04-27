# MPE Dashboard — Findings Backlog

Canonical status tracker for findings from Rounds 1–6 + dashboard-gap analysis.
Working document: survives context compaction, diffed in git log.

**Cadence:** one finding per commit. Step 1–7 protocol per `local-kiro-workstream-plan.md`.
Status values: `open` | `in-progress` | `done` | `verified` | `blocked` | `obsolete`

**"done"** = landed on disk + local regression green.
**"verified"** = Local Kiro pulled + walked the verification visually.

---

## Honest reconciliation: what's already on disk before we start

Several items on the incoming backlog were landed in Round 7 but not yet pushed
or verified by Local Kiro. Calling them out so status is accurate:

- `op2_pacing_divergence` alert translation — **done on disk (uncommitted)**. `CHECK_LABELS` + `translateDetail` wired in `renderMarketAnomalies` (projection-app.js:163-197).
- "Compare to baseline" disclosure button rename — **done on disk (uncommitted)**. projection.html:326.
- Scope-change state reset — **done on disk (uncommitted)**. projection-app.js scope-select handler resets `disclosures.counter` + `activeChipId` + `scenarioOverride`.
- NA rollup "rollup of US + CA" wording — **done on disk (uncommitted)**. projection-app.js:411-416.
- MY1/MY2 narrative denominator — **done on disk (uncommitted)**. mpe_narrative.js:114-115 uses `Annualized to OP2` with `/nYears`.
- Control-input focus ring — **done on disk (uncommitted)**. projection-design-system.css has `.control-input:focus-visible` override.
- abc blur handler — **done on disk (uncommitted)**. projection-app.js target-input blur listener.
- Spend upper bound — **done on disk (uncommitted)** but at $10B not $1B per Local Kiro's stricter recommendation. Revisiting in Phase 3.
- Feedback widget aria-labels + enable-on-change — **done on disk (uncommitted)**.
- Em-dash weeks leak in How modal + fit-quality strip — **done on disk (uncommitted)**.
- "Today" marker on chart — **done on disk (uncommitted)**.

These will be committed as a baseline commit labeled `mpe: R5-R7 batch (pre-backlog)`
before we start the new protocol. Every subsequent finding gets its own commit.

---

## Phase 1 — Track A (correctness)

### P1-01 · MC draws complete for every market/period combo
- **Source:** Round 1 #2, Round 3 V2, Round 5 V1
- **Status:** done (Option C — bootstrap CI)
- **Verification:** Probe on MX/US/UK/JP returns bands with plausible widths (MX 90% CI regs ±~50%, US ±~22%, UK ±~27%, JP ±~90%). CI values render in narrative as "90% plausible range: $Xlo–$Xhi spend · Rlo–Rhi regs. (Bootstrap approximation from recent-YTD residuals.)" How-modal Step 4 added with honest footnote on method limitation.
- **What landed:**
  - `V1_1_Slim.bootstrapCI(projectionOutput, ytdWeekly, alpha=0.10)` — new function in v1_1_slim.js computing per-week bands from residual sd × √(weeks_forward)
  - Wired into projection-app.js MC path, replaces the `MPE.projectWithUncertainty` call that was returning empty CIs since 2026-04-23 schema migration
  - Chart renders shaded band via `--color-ci-band-brand` fill (no longer gated on removed Uncertainty disclosure button)
  - Narrative appends CI tail line with explicit "bootstrap approximation" label
  - How-modal has a dedicated Step 4 footnote: "…not a Bayesian posterior credible interval — full posterior CIs are pending migration to the updated schema."
- **Unblocks:** P1-08 (CI in KPI tiles), P2-03 (CI bands on chart — done as side effect of this ticket).

### P1-02 · "At full-year pace" narrative denominator for MY1/MY2
- **Source:** Round 5 V-2
- **Status:** done on disk (R7, uncommitted)
- **Verification:** JP MY2 narrative says "Annualized to OP2, that's X% of OP2 spend" with X computed as `(annual_total_spend / 2) / op2_spend * 100`.
- **Note:** Will verify under new protocol before declaring verified.

### P1-03 · "Weeks used" em-dash placeholder in How modal + chart sub-line
- **Source:** Round 5 V-1 + V-6
- **Status:** done on disk (R7, uncommitted)
- **Verification:** "How this was calculated" modal Step 2 reads "… fit from 169 weeks of history" not "… from — weeks of history".

### P1-04 · Campaign-lift-to-baseline auto-promotion
- **Source:** Round 3 R3-4, Round 3 R3-9
- **Status:** done (UI + math)
- **Verification (UI layer, DONE):** `V1_1_Slim.listRegimesWithConfidence` emits `absorbed_into_baseline: true` on any lift with `decay_status === 'no-decay-detected'` AND `n_post_weeks >= 52`. 5/13 lifts across US/MX/UK/JP/DE correctly flagged. Narrative separates absorbed from active. Drawer pill "absorbed into baseline" with `—` instead of confidence %.
- **Verification (math layer, DONE, zero-delta):** `brand_trajectory._per_regime_weighted_contribution` now returns `1.0` for absorbed regimes. All 10 markets returned zero delta in the pre/post snapshot (guardrail ±15%: 0/10 exceeded). Zero delta is the CORRECT outcome given the 2026-04-26 anchor rework — the recent-actuals anchor already reflects absorbed-lift levels, so forward-stream contribution is a near-1.0 no-op anyway. The code change makes it symmetric with JS and self-documenting against future anchor-mechanism changes.
- **Snapshots:** `shared/dashboards/data/p1-04-preshift.json` (pre), `...postshift.json` (post). 128/128 Python tests still green. Commits: 56229df (UI), ea992c4 (pre-snap), 8cd5840 (math + post-snap).

### P1-05 · Confidence floor for projection inclusion
- **Source:** Round 2 dashboard-gap
- **Status:** open
- **Verification:** Lift #2 MX with 0.18 effective confidence is either dropped from the projection OR marked "unmodeled upside" visibly. Threshold TBD (starting point: 0.25).

### P1-06 · Solver convergence "Closest achievable" reporting
- **Source:** Round 3 R3-3
- **Status:** partial — translateWarning emits plain-English for `TARGET_UNREACHABLE_*` but doesn't always show the *closest achievable* number.
- **Verification:** When US Q2 target=65% returns 62.7% silently, banner reads "Closest achievable: 62.7% (target 65% exceeds NB spend bounds)".

### P1-07 · Regime-onset vertical rules on chart
- **Source:** Dashboard-gap #3
- **Status:** open
- **Verification:** On MX chart, a dashed purple rule at 2026-04-05 (Sparkle onset) with label "Sparkle onset" is visible.

### P1-08 · Effect-size summary with CI in KPI tiles
- **Source:** Dashboard-gap #4
- **Status:** open (blocked by P1-01)
- **Verification:** "vs OP2" tile shows point + 90% CI bracket, e.g. "+54% (90% CI: +38%/+72%)".

### P1-09 · Severity chip scope clarified
- **Source:** Round 3 R3-7
- **Status:** open
- **Verification:** Severity chip reads "Across 10 markets: 3 critical · 7 warn · 1 info" OR switches to per-market when user switches to single-market view.

### P1-10 · Numbers-drift between reloads
- **Source:** Round 3 R3-5
- **Status:** done
- **Root-cause probe (2026-04-27):** Grep confirms NO localStorage persistence of scope/period/driver/target in projection-app.js. `rngSeed: 42` is hardcoded. The drift was NOT a non-deterministic seed bug. It was the `projection-data.json` bundle regenerating between loads (every time `export-projection-data.py` or the WBR pipeline runs, Y2026 re-fits with a week's more YTD data). Local Kiro's initial hypothesis matched: data is genuinely refreshing.
- **Fix (shipped):** Added prominent `Refreshed Xh ago` indicator inside the hero market badge (12px/500 in subtle gray, cursor:help on hover). Tooltip reads: "Last refresh: Apr 27 2:39 AM. Projections update when YTD actuals refresh, typically every Monday. If yesterday's number differs from today's, the underlying data has advanced — the model is not non-deterministic." Existing 12px `header-freshness` top-right line retained for redundancy. No math changes.
- **Verification:** Cold-load shows the badge with human-readable timestamp. Tooltip surfaces the full refresh datetime and explains the drift. A Kate-grade test: if she compares a screenshot from Monday ($1.32M) to one on Tuesday ($1.88M), she sees two different "Refreshed" values and understands why the numbers differ.

### P1-11 · abc input blur handler
- **Source:** Round 5 V-3
- **Status:** done on disk (R7, uncommitted)
- **Verification:** Type `abc` into target-input, tab out, see "Enter a number." error.

### P1-12 · Console uncaught promise errors
- **Source:** Round 5 V-7
- **Status:** open
- **Verification:** Fresh page load on localhost:8080 with DevTools open shows zero uncaught promise rejections in console.

---

## Phase 2 — Track B (missing capabilities)

### P2-01 · Chart hover tooltips
- **Source:** Round 1 C-5, Round 2 R4-10
- **Status:** open
- **Verification:** Hover over week-14 dot on MX chart, popup shows "Week 14 · Actuals: 287 · Projected: 310 · Δ +23".
- **Next:** Demo-critical. First after correctness phase.

### P2-02 · Chart x-axis period-scoping
- **Source:** Round 3 R4-12
- **Status:** open
- **Verification:** Select period=W17 → chart x-domain covers roughly 4 weeks around week 17. Select MY2 → x-domain covers ~104 weeks.

### P2-03 · CI shaded bands on chart (blocked by P1-01)
- **Source:** Dashboard-gap #1
- **Status:** blocked by P1-01
- **Verification:** Shaded band using `--color-ci-band-brand` wraps the projected Brand line from YTD-latest forward.

### P2-04 · 3-panel component decomposition (Prophet-style)
- **Source:** Dashboard-gap #2
- **Status:** open
- **Verification:** Below main chart: 3 stacked plots labeled "Trend", "Seasonality", "Campaign lifts" each showing that stream's per-week contribution.

### P2-05 · Backtest panel
- **Source:** Dashboard-gap #5 + #6
- **Status:** open
- **Verification:** A panel shows last 8 weeks of actuals overlaid with 8-weeks-ago projection + MAPE % + coverage %.

### P2-06 · Week-over-week delta on KPI tiles
- **Source:** Round 1 K-8
- **Status:** open
- **Verification:** Each hero KPI has a small "+3.2% vs last week" subline in green/red.

### P2-07 · Clickable chart legend
- **Source:** Round 4 C-10
- **Status:** open
- **Verification:** Click "Projected Non-Brand" in legend → that line toggles invisible/visible.

### P2-08 · Line end-labels
- **Source:** Round 4 C-11
- **Status:** open
- **Verification:** Right edge of each projected line has a text annotation with the series name + last value.

### P2-09 · Today marker correctness across all markets
- **Source:** R5 shipped; needs verification
- **Status:** done on disk (R7, uncommitted); needs cross-market verification
- **Verification:** On all 10 markets + 3 regions, the "↓ Today" marker lands exactly at `ytd_latest` and reads "Today".

### P2-10 · URL-based state sharing
- **Source:** Round 4 R4-28
- **Status:** open
- **Verification:** Open `localhost:8080/projection.html?scope=UK&period=Y2026&driver=ieccp&target=65` → loads UK Y2026 @ 65%. Change any control → URL updates.

### P2-11 · CSV export
- **Source:** Dashboard-gap #9
- **Status:** open
- **Verification:** Click Export → browser downloads `MX-Y2026-projection.csv` with columns `date,projected_brand,projected_nb,projected_total,lower_90,upper_90,actual`.

### P2-12 · Saved projection load/delete/compare
- **Source:** Round 4 R4-16
- **Status:** open
- **Verification:** Each saved item has Load/Delete buttons; Load restores full state; Compare overlays on current chart.

### P2-13 · Brand/NB stacked bar visual
- **Source:** Round 1 K-7
- **Status:** open
- **Verification:** In place of separate Brand Regs + NB Regs tiles, one horizontal bar split 37/63 with labels.

### P2-14 · Directional color/arrow on OP2 comparisons
- **Source:** Round 1 K-3
- **Status:** open
- **Verification:** vs OP2 Spend at 137% shows red down-arrow; vs OP2 Regs at 137% shows green up-arrow.

### P2-15 · Spend on separate axis or chart
- **Source:** Round 1 C-2
- **Status:** open
- **Verification:** Spend no longer scaled onto the regs y-axis. Either dual y-axis with labeled "Spend ($)" right axis, or small spend sparkline below.

### P2-16 · Y-axis auto-scale tightening
- **Source:** Round 1 C-3
- **Status:** open
- **Verification:** Every market's y-axis max is within 15% of its visible peak (currently 30–60% headroom).

### P2-17 · Shared y-scale toggle for all-10 grid
- **Source:** Round 2
- **Status:** open
- **Verification:** On the "All 10 markets" view, a toggle switches between per-market y-scale and shared y-scale.

### P2-18 · Distance-to-target view fix
- **Source:** Round 2
- **Status:** open
- **Verification:** Heatgrid shows meaningful distances (distance to OP2 or unconstrained projection) rather than 0pp for solver-back-fit markets.

---

## Phase 3 — Track C (polish, a11y, naming)

### P3-01 · Alert translation render wire-up
- **Source:** Round 6 V6-3
- **Status:** done on disk (R7, uncommitted)
- **Verification:** MX alerts panel shows "Warning Projection diverges from OP2 plan — annual regs=17,235 vs OP2=11,178 (gap +54.2%)" not "[WARN] op2_pacing_divergence —".

### P3-02 · "Baseline only" deduplication
- **Source:** Round 6 V6-2
- **Status:** partial — disclosure button renamed to "Compare to baseline" in R7. Scenario chip still "Baseline only".
- **Verification:** No two controls share the name "Baseline only". Each one's label clearly indicates its effect.

### P3-03 · Scenario chip definition tooltips
- **Source:** Round 6 V6-5
- **Status:** partial — native `title` attr works, but no styled tooltip.
- **Verification:** Hover over "Pessimistic" scenario chip → styled tooltip within 200ms shows "Recent actuals extrapolated forward. No assumed uplift from active campaigns."

### P3-04 · Disclosure button state reset on market switch
- **Source:** Round 6 V6-4
- **Status:** done on disk (R7, uncommitted)
- **Verification:** Activate "Compare to baseline" on UK, switch to MX → button is de-activated and MX shows Planned scenario numbers.

### P3-05 · Control-input focus ring
- **Source:** Round 6 V6-1
- **Status:** done on disk (R7, uncommitted)
- **Verification:** Tab through market dropdown, period, driver, target-input, slider → each shows a 2px brand-blue outline.

### P3-06 · NA rollup subtitle wording
- **Source:** Round 5 V-5
- **Status:** done on disk (R7, uncommitted)
- **Verification:** Market badge on NA reads "NA · Year 2026 · rollup of US + CA" not "… rollup target".

### P3-07 · Contribution bar "Qualitative" relabel
- **Source:** Round 1 L-5
- **Status:** open
- **Verification:** Fourth contribution segment reads "Judgment" or "Manual adjustment" not "Qualitative".

### P3-08 · Plural handling in narrative
- **Source:** Round 6
- **Status:** open
- **Verification:** Narrative generator emits "1 transient regime event" not "1 transient regime event(s)" and "2 events" correctly.

### P3-09 · Raw numbers formatted everywhere (grep pass)
- **Source:** Multiple rounds
- **Status:** partial — NB residual string + saved projection label still have raw numbers in some paths.
- **Verification:** Grep of codebase for `\$\{[^}]*(target|spend|regs)[^}]*\}` without an `fmt` wrapper returns zero hits.

### P3-10 · Spend upper bound cap
- **Source:** Round 5 V-4 / Round 6
- **Status:** partial — tightened to $10B in R7. Local Kiro asks for $1B.
- **Verification:** Entering `$2B` in Target Value spend mode shows "Spend target exceeds $1B — likely a typo."

### P3-11 · Time format on saved projections
- **Source:** Round 5 V-?
- **Status:** open
- **Verification:** Saved items show "4/26/2026 14:23" not "4/26/2026".

### P3-12 · aria-label coverage
- **Source:** Round 4 R4-23
- **Status:** partial — feedback inputs labeled in R7. Scope/period/driver selects still need aria-labels.
- **Verification:** Every `button`, `select`, `input` has an `aria-label` or is wrapped in a `<label for="…">`.

### P3-13 · Landmark elements
- **Source:** Round 4 R4-21
- **Status:** open
- **Verification:** Page has `<main>`, `<aside>` for drawer, `<nav role="toolbar">` for controls row. Screen reader can navigate by landmark.

### P3-14 · Heading hierarchy
- **Source:** Round 4 R4-22
- **Status:** open
- **Verification:** No heading level skip. H1 → H2 → H3, not H1 → H3.

### P3-15 · Remove [WARN]/[ERROR] bracket notation
- **Source:** Round 4 R4-26
- **Status:** done on disk (R7, uncommitted)
- **Verification:** Alerts panel shows "Warning" / "Error" pill badges, no brackets.

### P3-16 · Recompute button decision
- **Source:** Round 4 R4-18
- **Status:** open
- **Verification:** Button either removed entirely OR re-fetches `projection-data.json` when clicked (visible via network tab).

### P3-17 · Scenario chip meaning (decide chip vs annotation)
- **Source:** Round 4 R4-19
- **Status:** open
- **Verification:** Either chips are clearly labeled interactive with hover tooltips (P3-03 covers), or they're restyled as annotations if that's the intent.

### P3-18 · Feedback widget radio enables inputs
- **Source:** Round 2 R4-20
- **Status:** done on disk (R7, uncommitted — HTML `disabled` removed + JS radio handler)
- **Verification:** Click "Too high" radio → magnitude + freetext + submit are enabled.

### P3-19 · Reset-to-defaults button
- **Source:** Round 4 R4-29
- **Status:** open
- **Verification:** A "Reset" button somewhere in the controls row → clicking restores MX Y2026 @ 75% efficiency (default state) and clears scenarioOverride.

---

## Phase 4 — Deferred refactors + AB.com branding

Executes LAST, after Phases 1-3 are stable. One commit per finding. Each
commit gets a visual regression pass from Local Kiro before next commit.

**Critical do-NOT rules (common traps flagged by Local Kiro):**
- **DO NOT migrate chart encoding colors** (`--color-nb` #FF9900, `--color-brand-line` #0066CC, `--color-actuals` #4A4A4A). Chart encoding is a data-ink concern; it is NOT UI chrome. The Non-Brand orange is close to AB.com's Smile orange and moving it creates visual collision. Leave chart colors untouched.
- **DO NOT pillify generic buttons.** The `.btn-primary` class with Smile-orange pill is for EXACTLY ONE button per view. If applied to `button { ... }` or all `.disclosure-btn`, it turns Save + Model details + Baseline + Recompute all into orange pills — three mistakes at once: (1) visual noise, (2) Smile orange bleeding away from its "primary action" semantic, (3) potential collision with the chart's NB orange when chart + orange-pill are both onscreen.
- **DO NOT bundle Amazon Ember .woff files into the repo.** That is a licensing violation and will fail internal review. Options in order: corp CDN URL (check AB.com network tab), sanctioned internal source, fallback to OS-installed `'Amazon Ember'` via font-family stack. If font source can't be resolved in 30 min of investigation, mark P4-03 blocked.
- **DO NOT migrate palette + type scale in one commit.** Failure modes become unattributable. Palette first (P4-01), CTA pill scoped (P4-04), then type scale (P4-02).

### P4-01 · Palette token migration to AB.com colors
- **Status:** planned (blocked until Phases 1-3 done)
- **Verification:** After pull + clear localStorage, page background reads warm cream `#F5F3EF`, panel bg stays `#FFFFFF`, primary body text reads `#161D26`, brand blue is `#2162A1`. DevTools computed-style on `.page-frame` shows `background-color: rgb(245, 243, 239)`.
- **Tokens to change:**
  - `--color-neutral-bg: #FFFFFF` → `#F5F3EF`
  - `--color-panel-bg: #FAFAFA` → `#FFFFFF`
  - `--color-text-body: #1A1A1A` → `#161D26`
  - `--color-text-hero: #0A0A0A` → `#0F1111`
  - `--color-brand: #0066CC` → `#2162A1`
  - `--color-panel-border: #E0E0E0` → `#E5E5E5` or `#6E6E78` (depends on weight — test both)
- **Tokens NOT to change:** `--color-nb`, `--color-brand-line`, `--color-actuals`, `--color-regime`, `--color-seasonal`, `--color-trend`, `--color-qualitative`, `--color-counterfactual`, `--color-ci-band-*`, `--color-target`, `--color-locked-ytd`, `--color-success`, `--color-warning`, `--color-danger`.
- **Risk:** White-on-colored chips may fail contrast against warm-cream background. Run WCAG AA spot-check on severity chip, feedback bar, active scenario chip after the swap.
- **Scope:** single commit on `projection-design-system.css` only. Screenshots before/after on all 10 markets + 3 regions.

### P4-02 · Type scale migration (body → 18px, 4-token scale)
- **Status:** planned (blocked until P4-03 lands so Ember is loaded)
- **Verification:** DevTools shows body elements at 18px (up from 12/13/14/16 mix). H1 at 48px, H2 at 24px, captions at 13px. No inline `style="font-size:10px"` or `11px` or similar in the rendered DOM.
- **Scale:**
  - `--size-display: 48px` (hero number, keep existing — AB.com's 84px is too big for a dense tool)
  - `--size-title: 24px` (section titles, market badge name)
  - `--size-body: 14px` → `18px` (all body, table cells, labels)
  - `--size-meta: 12px` → `13px` (captions, footnotes only)
- **Scope:** multiple commits, one per region — header, KPI strip, chart area, sidebar drawer, feedback panel, alerts panel, narrative, controls row. Screenshot after each region.
- **Risk:** 18px body expands every panel height. Dashboard currently fits on 900px tall viewport. Measure before/after. Don't shrink back to 14/16 — adjust panel padding if overflow.

### P4-03 · Ember font source compliance verification
- **Status:** planned, parallel to P4-01 but must resolve before P4-02
- **Verification:** DevTools Network panel on cold-load shows Ember .woff files loading with HTTP 200 from an Amazon-approved source (internal CDN or corp domain). No `.woff` files committed in the repo.
- **Investigation path:**
  1. Inspect business.amazon.com Network tab — find the amz-ember-reg.woff request URL. If it's on an Amazon corp domain (a2z.com, amazon.dev, awsapps.com), that's the sanctioned source; reference it directly in our CSS via `@font-face src: url(...)`.
  2. If step 1 doesn't yield a reusable URL, ask AB design team for sanctioned source.
  3. Fall back: rely on OS-installed Ember via `font-family: 'Amazon Ember', -apple-system, BlinkMacSystemFont, sans-serif`. Acceptable for corp-machine audience (Kate + Brandon + Todd are all on corp Macs). Loses display quality on non-corp devices.
- **If blocked:** mark blocked, proceed with fallback font stack. P4-02 can still ship.
- **Commit includes:** the decision + rationale in commit message.

### P4-04 · Primary CTA styled as AB Smile-orange pill (SCOPED TO ONE BUTTON)
- **Status:** planned
- **Verification:** Exactly ONE button per view has the pill styling. Other buttons unchanged. Smile orange `#F55600` does NOT appear anywhere in the chart or on the severity chip or feedback bar. Computed style on the designated button: `background-color: rgb(245, 86, 0); color: white; border-radius: 160px`.
- **Component:**
  ```css
  .btn-primary {
    background: #F55600;
    color: #FFFFFF;
    border: none;
    border-radius: 160px;
    padding: 12px 20px;
    font-size: 18px;
    font-weight: 600;
  }
  .btn-primary:hover { background: #D94A00; }
  ```
- **Application rule:** Single-market view → `#btn-recompute` gets `.btn-primary`. Detail views / Export view → the Export button gets it (after P2-11 lands). No other button gets pilled.
- **Anti-pattern guards:**
  - Grep the codebase after the commit: `grep -n "btn-primary" *.html *.js` should return ≤ 3 hits (one HTML class, one JS reference if any, one CSS definition). More than that suggests blanket application.
  - Visually verify: look at the full page screenshot — if you see more than one orange pill, you over-applied.
- **Why this matters:** The playbook explicitly flags pillifying as a trap. Smile orange's job is to mark the single next-action. Any other button-orange dilutes that semantic AND risks visual collision with the chart's NB orange when both are onscreen at the same zoom level.

### P4-05 · Full matrix regression test (10 markets × 6 periods × 3 drivers = 180 combos)
- **Status:** planned, sanity gate after P4-01 through P4-04
- **Verification:** Automated screenshot pass; grid saved to `context/intake/phase4-regression/<market>-<period>-<driver>.png`. Human review: any combo that breaks contrast, overflows the viewport, or renders with fallback Arial instead of Ember gets flagged and fixed before moving to P4-02.
- **Tooling:** Reuse or extend existing `shared/tools/prediction/run_market_simulation.py` pattern. May need a Puppeteer/Playwright script in `shared/dashboards/tools/` or a Python+Selenium wrapper.

---

## Phase 4 sequencing (why this order)

1. **P4-01 palette** — biggest visual shift, single variable surface, failure is obvious and localized. Commit + Local Kiro verify.
2. **P4-04 CTA pill** — scoped component addition, doesn't touch existing styles. Safe after palette lands.
3. **P4-03 Ember source** — must resolve before P4-02 activates the stack. Runs in parallel with P4-04.
4. **P4-02 type scale** — largest diff, highest regression risk. Isolate after visual moves stabilized.
5. **P4-05 regression matrix** — sanity gate.

Rationale: isolating failure modes. If palette and type scale ship together and something breaks, can't tell whether it's from color or type. Separating them keeps failures attributable.

---

## Prior Phase 4 items (palette + type-scale consolidation) — consolidated into P4-01/P4-02

The earlier "Phase 4 palette consolidation 41→14 tokens" and "type scale 13→4" items are subsumed by P4-01 and P4-02 above. The AB.com branding makes the consolidation more specific (actual target values, not just "fewer tokens"), which is a win — the consolidation wasn't scoped to target values before.

---

## Order of work

Execute top-to-bottom within each phase. When a finding is blocked, mark the
reason in-place and move to the next. Never silently skip.

**Current next-up:** P1-01 (MC draws). Blocks P1-08 + P2-03.
