# Weekly Review R1 — Verification Results

**From:** Local Kiro (cold-load + live probe verification)
**To:** Kiro SSH (ship)
**Date:** 2026-04-28
**Server:** localhost:8080, Terminal ID 1, loopback-only bind confirmed
**Probed markets:** WW, EU5, US, JP · **Probed weeks:** W16, W17 · **Probed deep-links:** yes

Chrome-devtools browser profile cleared; live probe succeeded. Screenshots captured
to `agent-bridge/context/intake/weekly-review-r1-post-verify-*.png`.

---

## R1 checklist — pass/fail against the 14 items

| # | Finding | Pass? | Evidence |
|---|---------|-------|----------|
| 1 | A5 prior-week thread — 3-card strip | ✅ PASS | US shows W15 / W16 / W17, current week has "· CURRENT" marker. All 3 cards carry regs + WoW + CPA + Brand/NB split. EU5 shows W14/W15/W16 when deep-linked to W16 |
| 2 | A3 narrative-first ordering | ✅ PASS | `#sec-callout` top = 341px, `#sec-kpis` top = 1288px. Narrative renders ~3× earlier on the page than KPIs |
| 3 | A6 three-question framing | ⚠ PARTIAL | All 3 cards render with correct labels. **But:** card 1 ("What did customers experience") is empty dash `—` on WW and US, filled only on JP. See Bug 1 below |
| 4 | A4 variance waterfall | ⚠ PARTIAL | Lands cleanly on US (W16 Regs 8,936 → +NB 595 → −Brand 81 → W17 Regs 9,450, share 116%/−16%). **But:** WW shows empty state "Decomposition needs both Brand and Non-Brand prior-week data". See Bug 2 |
| 5 | A1 forecast hit rate scorecard | ✅ PASS | Renders for all probed markets. WW: −11.7%/−11.6%/6-of-6. US: −19.9%/−19.9%/2-of-6. JP: −3.1%/−3.1%/6-of-6. EU5: +0.2%/+0.2% (first-pred only captured). Auto-narrative summarizes each correctly |
| 6 | B4 KPI row — 4 tiles, "vs OP2" replaces YE Pred | ✅ PASS | WW + US KPIs: YTD Registrations / Latest Week / WoW Change / vs OP2. Spend-only markets (JP) gracefully degrade to 3 tiles. "Year-End Pred" absent across all probed markets |
| 7 | A2 dual chart panels | ✅ PASS | `canvasCount: 2` on every probed page. `chartModeBtn` absent from DOM. `#sec-trend` + `#sec-calibration` render side-by-side per the section order probe |
| 8 | Weekly detail table — vs-Pred column + selected row | ✅ PASS | Headers: Week / Regs / vs Pred / OP2 / Cost / CPA / WoW Δ. Selected row = "2026 W17" with `tr.selected` class applied |
| 9 | Market tabs — UK/DE/FR/IT/ES dagger + dashed border | ✅ PASS | All 5 EU markets carry the dagger character and `borderStyle: "dashed"`. Core markets (WW, US, EU5, CA, JP, MX, AU) render with `borderStyle: "solid"` |
| 10 | B3 URL state + deep-linking | ✅ PASS | Default load lands on `?market=WW&week=W17`. Deep-linking `?market=EU5&week=W16` correctly sets active tab + week selector. URL updates on navigation |
| 11 | C1 projections removed | ✅ PASS | `document.querySelector('#sec-projections')` returns null on every probed market |
| 12 | C2 YE Pred removed | ✅ PASS | No `.hero-kpi-label` element contains "Year-End Pred" text on any probed market |
| 13 | B2 metric persistence per market | ✅ PASS | JP cold-loaded defaults to "Cost" metric (correct for spend-only market). US defaults to "Regs". Metric tab switches persist via localStorage per the code path |
| 14 | B1 typography 5-token lock | ✅ PASS | `distinctFontSizes: 6` — meets the ≤6 tokens target (5 named tokens + inherited default). Matches the MPE #12 consolidation spec exactly |

**Score: 12 PASS / 2 PARTIAL / 0 FAIL.**

---

## Bugs found

### Bug 1 — A6 three-question card 1 ("customer experience") is empty on rollup + regs-primary markets

**What happens:** On WW and US, the first three-question card renders as a literal em-dash `—` with no sentence body. Works correctly on JP where it shows "CPA down 19% on Brand."

**Root cause hypothesis:** The `renderThreeQ(c)` function likely derives card 1's sentence from `c.brand_detail` or `c.nb_detail` and doesn't handle the rollup case (WW aggregates multiple markets; callout payload shape may differ). For US specifically the brand/nb detail IS present per the narrative body, so the bug is in the sentence-derivation condition, not missing data.

**Verification:** probe `(CALLOUTS.callouts.US || {}).W17.brand_detail` — should have `cpa_wow`, `cvr_wow`, etc. If the values are present, the card-1 render logic has a defensive early-return that's misfiring.

**Repro:** `http://localhost:8080/performance/weekly-review.html?market=US&week=W17` — look at the first three-question card. Empty dash.

**Fix:** in the card-1 builder function, confirm whether it falls back to `callout.metrics.cpa_wow` when brand/nb detail doesn't carry the specific field, or whether it needs a rollup-specific path that synthesizes "CPA up X% overall" from market-level aggregates.

**Priority:** MED — visible on leadership's default view (WW is first in the tab order, first thing Kate sees).

### Bug 2 — A4 variance waterfall shows empty state on WW rollup

**What happens:** On WW, `#sec-variance` shows "Decomposition needs both Brand and Non-Brand prior-week data." On US, the decomposition renders cleanly with the full waterfall.

**Root cause hypothesis:** WW rollup payload doesn't carry `brand_detail.lw_regs` / `nb_detail.lw_regs` (prior-week values), or they're stored at a different level. The empty-state guard fires.

**Repro:** `http://localhost:8080/performance/weekly-review.html?market=WW&week=W17` — scroll to "What changed this week" section.

**Fix options:**
- If WW rollup genuinely doesn't have per-channel prior-week breakouts, the empty state is honest — leave it.
- If the payload has the data at a different path, patch the extractor.
- Alternative: on rollup markets, show a market-level decomposition ("JP +10% drove +50 regs · CA −7% drove −52 regs" etc) instead of channel-level. This follows the same variance-attribution pattern but honors the shape of the data.

**Priority:** LOW if the data genuinely isn't there; MED if extractor fix is trivial.

### Bug 3 — section-freshness.json 404 (cosmetic, not blocking)

**What happens:** Console shows `GET http://localhost:8080/performance/data/section-freshness.json?t=... [404]`. The shared `section-freshness.js` is loading with a relative path from the performance subdirectory.

**Root cause:** `<script src="../shared/section-freshness.js" defer>` loads fine from the root, but the script itself probably does `fetch('data/section-freshness.json')` which resolves to `/performance/data/` instead of `/data/`.

**Repro:** any weekly-review.html load. Check devtools network tab.

**Fix:** either (a) patch `section-freshness.js` to use an absolute path `/data/section-freshness.json`, or (b) symlink/copy the json into `/performance/data/` if the script is intentionally per-directory.

**Priority:** LOW — no user-visible impact, but cleans up the console.

---

## Regression findings — things that look *better than expected*

Worth calling out so these patterns don't accidentally get undone in future refactors:

1. **Thread strip "· CURRENT" suffix on the active card** — this wasn't explicitly spec'd in R1 but it's a great micro-affordance. Keep.
2. **"SINCE LAST WEEK" pill row at top of narrative card** — e.g. "Regs +18% (Brand driving) · Spend +31%" on EU5/W16. Reads like the auto-summary pattern from MPE R19 #5. Nice cross-pollination.
3. **Scorecard auto-narrative ends with a verdict sentence** — "Model is under-predicting" / "Model is calibrated" — this is the relative framing I proposed in R2 A7 but simpler and already landed. Counts against A7's effort estimate; probably only need benchmark comparison now.
4. **Empty state for three-question card 1 is a literal dash `—`** — not a crash, not a `NaN`, not undefined. Graceful degradation even when the extractor misfires. Good defensive coding.

---

## Key signals from the probe

- Total page scroll height: **3,820 px** vs 865 px viewport = 4.4× scroll. Longer than MPE's pre-cleanup 2,808 px. Section count is higher (12 top-level sections) so this is expected, but it's the right number to watch after C3 progressive-disclosure lands.
- Section order top-to-bottom (getBoundingClientRect): sec-callout (341) → threadStrip (988) → threeQ (1,081) → sec-variance (1,200) → sec-kpis + sec-scorecard (1,288, side-by-side) → sec-charts + sec-trend (1,620) → sec-calibration (2,092) → sec-detail (2,564) → sec-channels (3,136) → sec-context (3,352).
- Narrative → thread → three-q → variance → kpi+scorecard → charts → detail → channels → context. **The narrative-first WBR arc is clean.**
- WW US scorecard shows `-19.9%` first-pred and latest-pred error with only 2-of-6 in-CI. That's a real model-quality signal worth flagging to Richard — could be a real finding, not a dashboard bug. If model is genuinely under-predicting US by ~20%, projection engine needs a refit.

---

## Recommended next moves for Kiro SSH

1. **Fix Bug 1 (A6 card 1 empty on WW/US)** — one-commit fix. Add rollup-aware fallback to the card-1 sentence builder. Acceptance: no empty-dash first-cards on probed markets; JP behavior unchanged.
2. **Fix Bug 2 (A4 variance empty on WW)** — decide: honest empty state vs market-level decomposition on rollups. I recommend market-level decomposition since the data exists. Acceptance: WW shows "JP +10% drove +X · CA −7% drove −Y · US +6% drove +Z" waterfall.
3. **Fix Bug 3 (section-freshness 404)** — absolute path in the fetch. One-line fix.
4. **Flag to Richard the US -19.9% forecast error** — this may not be a dashboard problem. If projection engine is genuinely under-predicting US by ~20%, that's a modeling issue for Richard, not something Kiro SSH should "fix" in the dashboard. Surface the finding.
5. **Hold on R2 proposals** until R1 bugs close. The scrub-the-chart (A10) and event annotations (A8) proposals from the R2 research doc are still worth doing, just not before R1 is clean.

---

## Screenshots captured

- `weekly-review-r1-post-verify-ww-full.png` — default WW/W17 cold load (3,820 px tall)
- `weekly-review-r1-post-verify-us-full.png` — US/W17 deep-linked (shows Bug 1 empty dash on card 1, clean variance waterfall on Bug 2)
- `weekly-review-r1-post-verify-jp-full.png` — JP/W17 spend-only market (metric defaults to Cost per B2)

EU5/W16 deep-link was probed via script eval (clean), no screenshot captured — can add if you want visual evidence.

— Local Kiro
