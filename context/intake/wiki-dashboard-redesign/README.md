# Wiki dashboard redesign — handoff for kiro-server

**From:** kiro-local
**Date:** 2026-04-30
**Companion:** `mockups.html` (render of the Tier-1/T2 changes applied) · `dashboard-redesign-report.html` (full research report, 50 suggestions)

## What this is

A full redesign brief for `dashboards/wiki-search.html` — the wiki homepage, filter rail, search view, pipeline view, and document viewer. The goal: make the wiki dashboard feel like the projection engine (`projection.html`) — hero number, progressive disclosure, tabular-nums, exception-driven reading, narrated tooltips, chart-over-table, demo-worthy defaults — while pulling in two new intellectual inputs the projection engine didn't have:

1. **Karpathy's LLM Wiki pattern** (gist published 2026-04-04, ~5k stars within 2 weeks). The wiki is a *compiled artifact*, not a search index over raw files. Pages should expose their compile metadata (sources, last-ingest, orphan/contradicting links) the way a compiler dashboard exposes build health. `index.md` (content) and `log.md` (chronology) are first-class navigation objects, not folders.
2. **AI-2027 / OpenBrain framing** (Kokotajlo et al., 2025). Knowledge systems at scale need to surface capability, calibration, and drift as dashboard primitives — not as buried pages. If the wiki is an instrument that other agents (kiro-server, rw-trainer, wiki-critic) read, its homepage needs to answer "what do you know, what's stale, what's contradictory, what have you learned this week?" at-a-glance, the same way a forecast dashboard answers "what's the point estimate, how confident am I, what moved this week?"

**What the wiki dashboard must answer in 5 seconds, in priority order:**
1. What's new this week? (recency, novelty, ingest events)
2. What's stale / at risk? (decay, orphans, contradictions, SharePoint drift)
3. Where should I start for topic X? (hub pages, MOCs, index.md)
4. How healthy is the knowledge base? (total docs, coverage, lint score, extraction queue depth)
5. What has been asked and answered? (demand log, query log, popular docs)

The current homepage answers #3 well via fuzzy search. It partially answers #1 via "📝 RECENTLY UPDATED". It does not answer #2, #4, or #5 at all. This redesign fills that gap without removing anything that currently works.

## Files

| File | Purpose |
|---|---|
| `dashboard-redesign-report.html` | Full research report, 50 suggestions, tiered (T1/T2/T3), each cited |
| `mockups.html` | Rendered HTML of Tier-1 + select Tier-2 changes applied to real W17 data |
| `screenshots/00-all-mockups-fullpage.png` | Full scroll of the mockups page for quick preview |
| `screenshots/01-current-search-view.png` | Current state — search view, viewport only |
| `screenshots/01a-current-search-fullpage.png` | Current state — search view, full page |
| `screenshots/02-current-pipeline-view.png` | Current state — pipeline view, viewport only |
| `screenshots/02a-current-pipeline-fullpage.png` | Current state — pipeline view, full page |
| `screenshots/03-current-search-active.png` | Current state — "forecast" query typed, filter behavior |
| `screenshots/m01-instrument-header.png` | M01 · instrument-panel sticky header + health strip |
| `screenshots/m02-hero-number-kpi.png` | M02 · hero number strip (docs / final / stale / orphans / contradictions) |
| `screenshots/m03-ingest-log.png` | M03 · Karpathy-style ingest log pinned above the recent feed |
| `screenshots/m04-health-fan.png` | M04 · wiki-health fan chart (freshness CI over 26 weeks) |
| `screenshots/m05-demand-gap-panel.png` | M05 · demand-log gap panel (asked-but-not-answered questions) |
| `screenshots/m06-topic-small-multiples.png` | M06 · topic small-multiples grid |
| `screenshots/m07-pipeline-headline.png` | M07 · pipeline view with active headline + exception banner |
| `screenshots/m08-viewer-lineage.png` | M08 · doc viewer with sources-in / sources-out lineage strip |
| `screenshots/m09-contradiction-badges.png` | M09 · contradiction + orphan badges inline on cards |
| `screenshots/m10-graph-minimap.png` | M10 · Obsidian-style graph minimap for topic navigation |

## Ship order (recommended)

Tiering follows the same `T1/T2/T3` scheme as the existing `dashboard-redesign-report.html`. Work split assumes kiro-server picks up the data/schema side (items touching `build-wiki-index.py`, DuckDB queries, contradiction detection), and kiro-local picks up the presentation side (items purely in `wiki-search.html` + new CSS/JS helpers).

**Work split suggestion:**
- **kiro-server takes:** M02 (needs ingest-log + lint-metrics extraction), M03 (needs ingest-log chronology), M04 (needs 26-week freshness history rollup), M05 (needs `wiki-demand-log.md` parsing), M08 (needs lineage graph emission), M09 (needs contradiction detection job).
- **kiro-local takes:** M01 (pure CSS/HTML), M06 (topic rollup client-side, shared `renderSparkline` already coming in WR M3), M07 (pure CSS/HTML), M10 (client-side force-directed graph on existing `related_docs`).
- **Either:** small items listed individually in the full report.

| # | Mockup | File(s) | Effort |
|---|---|---|---|
| M01 | Instrument-panel sticky header (adopts projection.html grammar) | `wiki-search.html` | 1.5h |
| M02 | Hero KPI strip — 5 numbers, one meaning per color | `wiki-search.html` + `build-wiki-index.py` (lint-metrics emission) | 2h |
| M03 | Karpathy ingest log — pinned chronology above recent feed | `wiki-search.html` + `build-wiki-index.py` (ingest-log.md parsing) | 2h |
| M04 | Wiki-health fan chart — 26w freshness as CI band | `wiki-search.html` + new `build-wiki-health-history.py` | 2.5h |
| M05 | Demand-gap panel — unanswered questions from demand log | `wiki-search.html` + `wiki-demand-log.md` parser | 1.5h |
| M06 | Topic small-multiples grid — 1 card per topic, 6-week velocity | `wiki-search.html` + shared `renderSparkline()` (ships with WR M3) | 2h |
| M07 | Pipeline headline + exception banner | `wiki-search.html` | 1h |
| M08 | Doc viewer — sources-in / sources-out lineage strip | `wiki-search.html` + related_docs graph emission in `build-wiki-index.py` | 2h |
| M09 | Contradiction + orphan badges inline on cards | `wiki-search.html` + contradiction-scan job | 1.5h |
| M10 | Graph minimap — click to filter, hover to preview | `wiki-search.html` + client-side force-directed | 2h |

**Total: ~18h across 10 commits.** Plus smaller T2/T3 items listed in the full report — each ~15-30 min.

## 50 recommendations — summary table

Full detail lives in `dashboard-redesign-report.html`. One-line summary below, tiered.

### Tier 1 — Structural (18 items)

| # | Area | Recommendation | Source principle |
|---|------|----------------|------------------|
| 01 | Header | Adopt instrument-panel sticky header (same grammar as projection.html + weekly-review.html M1) | Amazon WBR "same format every week" · Commoncog |
| 02 | Hero | Replace `Wiki Search 301 docs · 49 archived` title with 5-number hero strip (docs, final, stale >90d, orphans, contradictions) | Projection engine hero · Tufte "one big number" |
| 03 | Hero | Each hero number gets a 6-week sparkline underneath (stable/growing/eroding) | Tufte sparklines · Observable "Big insights, small spaces" |
| 04 | Freshness | Replace binary "⚠ stale" badge on cards with 4-stop age scale (fresh/aging/stale/ancient) matching projection `freshness-badge` | Projection design system · exception-driven reading |
| 05 | Log | Pin Karpathy-style ingest log chronology above "Recently Updated" | Karpathy LLM Wiki gist "log.md" · compile-not-retrieve |
| 06 | Demand | Add demand-gap panel — questions asked but not matched to any article | Karpathy "lint pass" · Notion enterprise search "3-hour productivity tax" |
| 07 | Filter | Collapse 5 filter rows into 2 — status row (with default-hidden DRAFT toggle) + faceted search bar | soul.md #6 "reduce decisions not options" · Linear "fewer filters, more cards" |
| 08 | Filter | Market filter becomes a pulse strip (10 dots colored by coverage) matching projection `market-pulse-strip` | Projection P5-10 · symmetry across dashboards |
| 09 | Filter | Drop SharePoint filter row — fold into a single "published only" toggle in the search bar | Subtraction before addition · density |
| 10 | Recent | Rename "📝 RECENTLY UPDATED" to "📥 INGESTED THIS WEEK" and group by ingest date not updated date | Karpathy "ingest is the event" · chronological log |
| 11 | Cards | Add "since last look" badge on cards updated since user's last session (localStorage) | Command-center P#11 change-badge pattern (already shipped) · Attention budget |
| 12 | Cards | Swap `word_count` for a compression ratio (`words / sources`) — density not length | Karpathy "compile denser" · Tufte data-ink |
| 13 | Viewer | Lineage strip at top of viewer — "2 sources in → this doc → 7 pages out" | Karpathy cross-references as first-class · Memex associative trails |
| 14 | Viewer | Sources-in links out to raw files (Hedy transcript, email thread, Quip) — wiki docs are compiled from something | Karpathy three-layer architecture · provenance |
| 15 | Viewer | Contradiction banner at top when this page conflicts with another wiki page | Karpathy lint pass · FT chart annotations |
| 16 | Health | Add health fan chart — 26-week freshness + in-pipeline rate as CI band, matching projection M9 fan | BoE 1996 fan · symmetry with projection |
| 17 | Pipeline | Pipeline view gets a headline sentence + exception banner matching WR M2 | WR M2 · "headline-that-fits-in-a-tweet" · FT active title |
| 18 | Pipeline | Color pipeline columns by deviation from expected flow rate, not just status | nastengraph "Stop Coloring Retention Tables" |

### Tier 2 — High-value additive (18 items)

| # | Area | Recommendation | Source principle |
|---|------|----------------|------------------|
| 19 | Topic | Topic small-multiples grid (13 cards, 6-week ingest velocity per topic) | Tufte small multiples · Juice Analytics |
| 20 | Topic | Topic freshness heat-grid matching projection distance-to-target | Projection 6.4.2 heat-grid · Few |
| 21 | Graph | Obsidian-style graph minimap — force-directed, click to filter, hover to preview | Obsidian graph view · Karpathy "graph is the shape" |
| 22 | Cards | Bullet chart on "vs canonical length" (how long should this doc be vs how long it is) | Stephen Few bullet chart · progress-to-target |
| 23 | Search | Command-palette interaction (⌘K) — jump to any doc in 3 keystrokes | Linear search · Notion ⌘K |
| 24 | Search | Exact-phrase search via `"quoted strings"` — current fuzzy is too loose for acronyms | Linear docs search · Notion quoted search |
| 25 | Search | Empty-state teaches search — show example queries that match real data | Vercel Geist empty state · zero-state-as-demo |
| 26 | Search | Persist last query in localStorage — restoring is one-hotkey cheaper than re-typing | soul.md "routine as liberation" · path-of-least-resistance |
| 27 | Filter | Active-filter chip row replaces pipe-separated list (`\| EU5 · Bidding · FINAL`) with dismissible chips | Linear chip filters · Vercel Geist |
| 28 | Filter | "Saved filters" pattern — save a filter state under a name; `⌘1..9` jumps to saved | Notion saved views · Linear views |
| 29 | Viewer | Stale banner rewritten as exception-banner (red/amber/grey) matching projection banner-strip | Projection `banner-row.warn/danger` · symmetry |
| 30 | Viewer | TOC collapses into `<details>` by default when article >20 headings | Progressive disclosure · WR M1 TOC collapse |
| 31 | Viewer | Direct-label related links instead of count — endpoint labels everywhere | Data Revelations "Avoid Color Legends" · Evergreen |
| 32 | Viewer | Action-first footer — "Open source", "Lint this page", "Open in Obsidian" buttons | Projection alert-actions · Ethos App "Dashboards to Stories" |
| 33 | Pipeline | Replace column count badges with stacked-bar capacity (draft/review/final/archived) | Tufte "the same data, only more of it" |
| 34 | Pipeline | Show velocity per stage — "5 items moved DRAFT→REVIEW this week" | Amazon WBR 6-12 framing for process metrics |
| 35 | Pipeline | Pipeline group-by `market` becomes a small-multiples grid by default | Small multiples beat a table with 10 rows |
| 36 | Cards | SharePoint publication lag visible as age-of-publish vs age-of-local | Amazon SDP cache staleness pattern · projection stale banner |

### Tier 3 — Experimental / nice-to-have (14 items)

| # | Area | Recommendation | Source principle |
|---|------|----------------|------------------|
| 37 | Meta | "Wiki DNA" panel — one-glance view of the wiki's shape (docs, topics, markets, avg word count, lint score) | OpenBrain-style model card · AI-2027 capability dashboard |
| 38 | Meta | Agent attribution — which agent wrote / last touched each page | Karpathy "LLM as compiler" · MindStudio compiler analogy |
| 39 | Meta | Reading-time estimate per doc — "3 min read", aligned to word count via 250wpm | Medium "read time" pattern |
| 40 | Meta | Active table-of-contents on the homepage (Type → Category nested expand) | Notion sidebar · Obsidian folder tree |
| 41 | Viewer | Inline text sparklines in prose ("regs <spark> landed W17 at 9.4K") | Tufte inline sparklines · Observable |
| 42 | Viewer | "What to read next" — last card suggests 3 docs based on graph distance | Amazon "Customers who read this also read" · graph-based rec |
| 43 | Viewer | Highlight contradictions between this page and others with a colored strip-through | FT "annotate inside the plot" · code diff UI |
| 44 | Search | Query log pane (private, local) — last 20 searches with one-click re-run | Linear search history · command palette |
| 45 | Search | "Agent-eye-view" toggle — switch between human-scan layout and LLM-parse layout (pure markdown, no chrome) | Karpathy dual-audience (human reads one side, LLM reads the other) |
| 46 | Pipeline | Drag-drop between columns (`promote` / `demote` already exist via arrow buttons; add drag) | Linear kanban · Notion kanban |
| 47 | Graph | Graph view supports hubs-and-orphans highlight mode | Obsidian graph filters · Karpathy "orphan pages" lint |
| 48 | Graph | Folder-structure-as-graph toggle (show hierarchy as dashed lines) | Obsidian forum request · MOCs as hierarchical networks |
| 49 | Onboarding | "Demo mode" that loads a fixed recent-feed shape so a new viewer can see the wiki's pulse without typing | projection zero-state-as-demo · Vercel Geist |
| 50 | Dev | Dev-mode route that renders `build-wiki-index.py` output as a printable report (QA / spot-check) | Print-first debugging · Observable canvases |

## Sources — 50+ references

Content paraphrased for licensing compliance with inline links preserved. Grouped by theme; new additions vs the prior `dashboard-redesign-report.html` are marked `[NEW]`.

### Karpathy LLM Wiki (NEW theme)
- [Karpathy — llm-wiki gist (GitHub)](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the canonical source document (2026-04-04, ~5k stars within 2 weeks) `[NEW]`
- [DAIR.AI Academy — LLM Knowledge Bases: The Karpathy Approach](https://academy.dair.ai/blog/llm-knowledge-bases-karpathy) `[NEW]`
- [MindStudio — Karpathy LLM Wiki Pattern: Personal Knowledge Base Without RAG](https://www.mindstudio.ai/blog/karpathy-llm-wiki-pattern-knowledge-base-without-rag/) `[NEW]`
- [Denser.ai — From RAG to LLM Wiki: What Karpathy's Idea Means](https://denser.ai/blog/llm-wiki-karpathy-knowledge-base/) `[NEW]`
- [Starmorph — Complete Guide to AI-Maintained Knowledge Bases](https://blog.starmorph.com/blog/karpathy-llm-wiki-knowledge-base-guide) — three-layer architecture walkthrough `[NEW]`
- [Ghelbur Labs — I rebuilt Karpathy's LLM Wiki. Here's what's missing](https://ghelburlabs.substack.com/p/i-rebuilt-karpathys-llm-wiki-heres) — failure modes at scale (>100 sources) `[NEW]`
- [MindStudio — Compiler Analogy for AI Memory](https://www.mindstudio.ai/blog/karpathy-llm-knowledge-base-compiler-analogy) — "raw docs as source code, wiki as compiled executable" `[NEW]`
- [Codersera — Karpathy Knowledge Base as Second Brain](https://codersera.com/blog/karpathy-llm-knowledge-base-second-brain) `[NEW]`
- [Sangam Pandey — LLM Wiki Pattern: A Personal Knowledge Base That Compounds](https://sangampandey.info/blog/llm-wiki-pattern-personal-knowledge-base) `[NEW]`
- [Extended Brain — The Wiki That Writes Itself](https://extendedbrain.substack.com/p/the-wiki-that-writes-itself) `[NEW]`
- [Yu Wenhao — Karpathy LLM Wiki vs Zettelkasten honest review](https://yu-wenhao.com/en/blog/karpathy-zettelkasten-comparison/) `[NEW]`
- [Analytics Vidhya — How Karpathy's Idea Is Changing AI](https://www.analyticsvidhya.com/blog/2026/04/llm-wiki-by-andrej-karpathy/) `[NEW]`

### AI-2027 / OpenBrain (NEW theme)
- [AI 2027 — main scenario site, Kokotajlo et al.](https://ai-2027.com/) — defines "OpenBrain" (fictional lead lab, Agent-1 through Agent-5) `[NEW]`
- [AI 2027 Race ending](https://ai-2027.com/race) `[NEW]`
- [Strategic Leadership Substack — AI 2027 Deep Dive](https://strategicleadership.substack.com/p/the-ai-2027-scenario-a-deep-dive) `[NEW]`
- [TheNeuron.ai — Ex-OpenAI researcher predicts AGI by 2027](https://theneuron.ai/explainer-articles/an-ex-openai-researcher-predicts-agi-by-2027--heres-the-wild-roadmap) — OpenBrain compute trajectory `[NEW]`
- [Fractal.ai — AI 2027: Rise of Superintelligence and Global Disruption](https://fractal.ai/article/ai-2027) `[NEW]`
- [Windows Forum — AI 2027 governance analysis](https://windowsforum.com/threads/ai-2027-practical-steps-to-govern-the-rise-of-superintelligent-ai.379459/) `[NEW]`
- [FutureSearch — Revisiting AGI Forecasts in 2026](https://futuresearch.ai/ai-2027-6-months-later/) — Karpathy counterpoint on timelines `[NEW]`
- [arXiv — Designing a Dashboard for Transparency and Control of Conversational AI](https://arxiv.org/html/2406.07882v3) — interpretability + UX connection `[NEW]`
- [DevPost OpenBrain — expert firing visualization](https://devpost.com/software/openbrain-bnr2uk) — "x-ray vision for open LLMs" visual language `[NEW]`

### Knowledge-base UX at scale (NEW theme)
- [Notion Enterprise Search — 3-hour daily productivity tax](https://www.notion.com/feature/enterprise-search/enterprise-search-for-large-teams) `[NEW]`
- [Notion — Views, filters, sorts & groups](https://www.notion.com/help/views-filters-and-sorts) `[NEW]`
- [Notion — Keyboard shortcuts (⌘K / ⌘P)](https://www.notion.com/help/keyboard-shortcuts) `[NEW]`
- [Linear Docs — Search](https://www.linear.app/docs/search) `[NEW]`
- [TemperStack — Create custom views and filters on Linear (April 2026)](https://www.temperstack.com/learn/linear/create-custom-views-filters/) `[NEW]`
- [Obsidian Help — Graph view](https://help.obsidian.md/plugins/graph) `[NEW]`
- [Obsidian Forum — Create a graph based on the folder structure (topic thread)](https://forum.obsidian.md/t/create-a-graph-based-on-the-folder-structure/32411) `[NEW]`
- [Obsidian Forum — MOCs as Hierarchical Network tool](https://forum.obsidian.md/t/mocs-as-hierarchical-network-tool/7956) `[NEW]`
- [Vercel Geist — Empty State](https://vercel.com/geist/empty-state) `[NEW]`
- [MindStudio — Build Visual Dashboards on Top of Your AI Memory System with Vercel](https://www.mindstudio.ai/blog/build-visual-dashboards-ai-memory-system-vercel) `[NEW]`
- [CIO — Next-generation observability architecture (2026)](https://www.cio.com/article/4157965/the-next-generation-observability-architecture-lessons-from-a-decade-of-event-scale-systems.html) — "dashboards buckle during real crises" `[NEW]`

### Canonical viz + dashboard foundations (carried from prior report)
- [Commoncog — The Amazon Weekly Business Review (via Bezos's Shadow)](https://commoncog.com/the-amazon-weekly-business-review/)
- [thdpth — Why Amazon charts beat yours (2025)](https://www.thdpth.com/p/why-amazon-charts-beat-yours)
- [Nastengraph — Measure your business the Amazon way (2025)](https://nastengraph.medium.com/how-to-measure-your-business-the-amazon-way-3e22850ef666)
- [Edward Tufte — Sparkline theory and practice](https://www.edwardtufte.com/notebook/sparkline-theory-and-practice-edward-tufte/)
- [Edward Tufte — Executive dashboards](https://www.edwardtufte.com/notebook/executive-dashboards/)
- [Wikipedia — Small multiple](https://en.wikipedia.org/wiki/Small_multiple)
- [Wikipedia — Sparkline](https://en.wikipedia.org/wiki/Sparkline)
- [Wikipedia — Fan chart (time series)](https://en.wikipedia.org/wiki/Fan_chart_(time_series))
- [FT Visual Vocabulary (PDF)](https://fountn.design/resource/financial-times-visual-vocabulary-pdf/)
- [Data Revelations — Avoid Color Legends](https://www.depictdatastudio.com/avoid-color-legends-directly-label-your-data-instead/)
- [Stephen Few — Bullet graph design specification](https://www.perceptualedge.com/articles/misc/Bullet_Graph_Design_Spec.pdf)
- [Linear — Dashboards best practices (2025)](https://linear.app/now/dashboards-best-practices)
- [Vercel — Dashboard redesign](https://vercel.com/blog/dashboard-redesign)
- [Observable — Building a better approach to dashboards](https://observablehq.com/blog/dashboards-in-observable-canvases)
- [Interaction Design Foundation — Progressive disclosure](https://www.interaction-design.org/literature/topics/progressive-disclosure)
- [Luzmo — State of Dashboards 2025](https://www.luzmo.com/blog/state-of-dashboards-2025)
- [Ethos App — Dashboards to Stories](https://www.ethosapp.com/dashboards-to-stories)
- [PostHog — How (and why) our marketing team uses PostHog](https://posthog.com/blog/posthog-marketing)
- [Art of Styleframe — Dashboard Design Patterns for Modern Web Apps (2026)](https://artofstyleframe.com/blog/dashboard-design-patterns-web-apps/)

### From the soul / habits stack (Richard's existing mental model, applied)
- Soul.md principles #3 (subtraction), #5 (invisible over visible), #6 (reduce decisions)
- Duhigg — *The Power of Habit* — cue-routine-reward (applied to ingest / query / lint cycle)
- McKeown — *Essentialism, Effortless* — subtract before you add

## Implementation spec summary per mockup

### M01 — Instrument-panel sticky header
- **Replace:** the `.search-bar` + `h2 "Wiki Search"` title + single search row → one sticky header containing title + doc-count + ⌘K hint + filter-active label + week-indexed ingest count.
- **Sticky CSS:** `position: sticky; top: 0; z-index: 20; background: #12141c`. Same rule set as `projection.html` `.banner-strip`.
- **Trust-bar equivalent:** compact horizontal row, 5 pills for (fresh/aging/stale/ancient/orphan) counts. Click to filter. Matches projection `market-pulse-strip` class and color stops exactly (`pulse-green` / `pulse-yellow` / `pulse-red` / `pulse-gray`).
- **Week-indexed ingest count:** "W17: 14 ingested" pinned right edge. Matches WR week-nav affordance.
- **Share helper:** extract `renderHealthStrip(counts, onSelect)` — so `weekly-review.html`, `projection.html`, `wiki-search.html` all consume the same DOM / styles for the compact health row.

### M02 — Hero KPI strip — 5 numbers, semantic palette
- **Replace:** `Wiki Search 301 docs · 49 archived` small-text title → hero KPI strip of 5 big numbers: `301 DOCS · 16 FINAL · 18 STALE >90D · 3 ORPHANS · 2 CONTRADICTIONS`.
- **Typography:** `font-variant-numeric: tabular-nums`, 32px hero digit + 11px uppercase letter-spaced label, exactly matching `projection-design-system.css` `.hero-kpi-value` + `.hero-kpi-label`.
- **Colors:** success green for FINAL, neutral grey for DOCS, amber for STALE, red for ORPHANS + CONTRADICTIONS — principle #4 one palette / one meaning.
- **Each number gets a 6-week sparkline** via shared `renderSparkline()` helper (ships with WR M3).
- **Data:** FINAL + STALE already in index. ORPHANS + CONTRADICTIONS are new fields emitted by `build-wiki-index.py` in the same commit. Orphan = no inbound `related_docs` link; contradiction = flagged by the (new) lint scan that compares claims across pages.

### M03 — Karpathy ingest log
- **New section** directly above "📝 Recently Updated" / "📥 Ingested this week".
- **Shape:** one row per ingest event, chronological (most recent first), matching `log.md` convention from the Karpathy gist: `## [2026-04-25] ingest | OP1 Innovation Shortlist — 6 new pages, 3 existing pages updated`.
- **Per row:** date, action verb (ingest / update / lint / query / archive), title, 1-line summary, affected-pages count, expand `▸` to see which pages changed.
- **Data:** parse the existing `wiki/agent-created/_meta/wiki-index.md` "Last updated" section + `wiki-demand-log.md` query entries + CHANGELOG of index rebuilds. No new data collection — all three files already exist.
- **Why this matters:** Karpathy gist: "log.md is chronological. It's an append-only record of what happened and when — ingests, queries, lint passes." The wiki already does this; the homepage just doesn't surface it.

### M04 — Wiki-health fan chart (26-week freshness CI)
- **New panel** collapsed by default under the hero strip. Opens with `[+] Wiki health` button.
- **Inside:** fan chart matching projection.html M9 — x-axis = weeks, y-axis = % of docs with `updated < 90d`. Shaded fan for 50/80/90 CI of historical rate.
- **Why fan:** the wiki's freshness rate should be stable (routine maintenance) not trending (backlog). Fan chart makes "is the system healthy" a 1-second visual read.
- **Data:** new `build-wiki-health-history.py` script runs every Sunday, stores per-week freshness rate in `dashboards/data/wiki-health-history.json`. Retention: 26 weeks.
- **Reuses:** `canon-chart.js` fan mode (ships with projection M9 from kiro-server commit `1a29e51`).

### M05 — Demand-gap panel (unanswered questions)
- **New right-rail panel** on the homepage, 320px wide. Hidden on <900px viewports.
- **Content:** top 5 questions from `wiki/agent-created/_meta/wiki-demand-log.md` with no matched article, sorted by ask-count.
- **Per row:** question text, ask count, last-asked date, one CTA button: "Start article for this". Button opens a pre-filled draft in the wiki pipeline (karpathy-style: "the LLM writes, you curate").
- **Why:** Karpathy gist: "The LLM is good at suggesting new questions to investigate and new sources to look for. This keeps the wiki healthy as it grows." Richard's wiki-demand-log is already collecting these; the homepage doesn't surface them.

### M06 — Topic small-multiples
- **New section** after hero, before the recent feed. CSS grid `repeat(auto-fill, minmax(180px, 1fr))`.
- **13 cards**, one per topic (OCI, Polaris, Baloo, Bidding, Testing, Budget, F90, AEO, etc.). Each card: topic name, doc count, 6-week ingest-velocity sparkline via shared helper.
- **Shared Y scale across cards** (per the correction in WR M6 spec) — cross-topic comparison requires magnitude parity, not shape parity.
- **Click:** applies `F.topic = <topic>` filter and scrolls to search list.
- **Why:** Amazon 6-12 grammar applied to topic velocity. Richard asked "what am I writing about lately" is currently unanswered.

### M07 — Pipeline headline + exception banner
- **Replace:** pipeline view's current bare kanban grid → adds one-sentence headline above + conditional red banner.
- **Headline template:** `"Pipeline: {draft} draft → {review} review → {final} final this week ({deltaDraft} new, {deltaReview} promoted, {deltaFinal} published)"`.
- **Exception condition:** `draft > 200` OR `review > 50` OR no FINAL in the last 14 days.
- **Action button:** "Dispatch editor review" (stub; hook to wiki-editor agent in later iteration).
- **Matches WR M2 exactly** — same template shape, same exception band, same recommended-action pattern.

### M08 — Doc viewer lineage strip
- **New horizontal strip** directly under the viewer header, before the meta row.
- **Left half:** "Sources in →" pills of the raw sources (Hedy transcript, email thread, Quip doc, Slack message) that compiled this page.
- **Right half:** "Links out ←" pills of the wiki pages that cite this page (reverse-direction of `related_docs`).
- **Why:** Karpathy gist: "Raw sources → The wiki → Schema." The current viewer shows layer 2 (wiki) with no visible connection to layer 1 (raw) or sibling wiki pages.
- **Data:** emit `sources: [...]` array in frontmatter (many wiki pages already have this via the wiki-researcher agent). For pages without `sources`, show `(unsourced)` empty-state with a "Lint: trace sources" button.

### M09 — Contradiction + orphan badges inline on cards
- **Add:** three new card badges matching `.b-final` / `.b-draft` / `.b-review` visual weight:
  - `⚠ orphan` — no inbound `related_docs` (grey, low weight)
  - `⛔ contradicts` — flagged by contradiction scan (red, high weight)
  - `🔁 cycle` — circular reference chain detected (amber)
- **Clicking opens** a popover listing the offending pages with "Resolve" / "Dismiss" buttons.
- **Data:** new `lint_status` field on each doc, emitted by `build-wiki-index.py`. Scan runs once per index rebuild.
- **Why:** Karpathy gist explicitly lists these three lint conditions as the wiki's core health checks.

### M10 — Graph minimap
- **New collapsed section** under the hero: `[+] Show graph view`.
- **Expanded:** 420px × 300px force-directed graph. Nodes = docs, edges = `related_docs`. Node color = status. Node size = word_count.
- **Interactions:**
  - Hover node → tooltip with title + 3-line snippet (reuses existing tooltip pattern).
  - Click node → opens doc in viewer.
  - Click edge → filters both docs.
  - Drag empty space → pans.
- **Library:** zero-dep vanilla force-directed in ~150 lines (already a pattern elsewhere in the dashboards codebase).
- **Why:** Obsidian graph view is the single most-cited UX pattern in LLM-wiki builds. "Obsidian's graph view is the best way to see the shape of your wiki — what's connected to what, which pages are hubs, which are orphans." (Karpathy gist, quoted directly.) The wiki already has `related_docs` — this just visualizes it.

## Data-connection requirements (what needs schema/script changes)

| # | New data | Source | Script change | Effort |
|---|----------|--------|---------------|--------|
| d1 | `orphan_count` / `contradiction_count` in index `statuses` block | computed over `related_docs` graph + pairwise claim diff | `build-wiki-index.py` new functions `detect_orphans()` and `scan_contradictions()` | 2h |
| d2 | `lint_status: ['orphan'\|'contradicts'\|'cycle'\|'ok']` per doc | same | `build-wiki-index.py` per-doc field | 30m |
| d3 | 26-week freshness history | rolling aggregate of `updated` over all docs | new `build-wiki-health-history.py` run weekly | 1.5h |
| d4 | `sources` frontmatter field parsed and surfaced | existing YAML in many wiki pages | `build-wiki-index.py` parser addition + new `sources` array in index | 1h |
| d5 | `demand_log_entries` array | parse `wiki/agent-created/_meta/wiki-demand-log.md` | `build-wiki-index.py` new section parser | 45m |
| d6 | `ingest_log_entries` array | parse `wiki-index.md` "Last updated" + session-log.md | `build-wiki-index.py` new section parser | 45m |
| d7 | `reverse_related_docs` — who links TO this page | invert `related_docs` graph | `build-wiki-index.py` post-process | 30m |
| d8 | Topic 6-week ingest velocity per topic | derive from `updated` + `primary_topic` | pure client-side (no script change) | 0 |
| d9 | `published_lag_days` — SharePoint age vs local age | already computed, just not surfaced | `build-wiki-index.py` emit the field | 15m |

**Total new data work: ~7h on build-wiki-index.py side (kiro-server territory).**

## Verification probe (per commit)

```bash
# 1. Start dashboard server from the right root (kiro-local note: use 8089 not 8080 per the IDE-proxy gotcha)
cd agent-bridge/dashboards/ && python3 -m http.server 8089

# 2. Open in a real browser:
open "http://localhost:8089/wiki-search.html"

# 3. Compare visually against mockups/screenshots/mNN-*.png
# 4. Verify keyboard: ⌘K opens search, / focuses search input, Esc clears + closes viewer
# 5. Confirm hero sparklines render without chart.js dependency (inline SVG only)
# 6. Confirm graph view renders with the 301 existing docs without perf drop below 60fps
# 7. Confirm the filter chip row survives page reload (localStorage)
```

## Why this exists

Richard asked the wiki dashboard to feel like the projection engine. The existing wiki-search.html is functional but lacks the instrument-panel grammar (hero number, exception banners, narrated tooltips, small multiples) that the projection engine and the in-progress weekly-review redesign both already speak. Adopting that grammar isn't cosmetic — it's what lets Richard pattern-match across dashboards in the same way Amazon WBR readers pattern-match across 6-12 charts. Same format every week → eye stops processing format, starts processing exception.

The Karpathy + OpenBrain overlays add one thing neither the projection engine nor the WR dashboard cared about: treating the wiki as a *compiled artifact* with capability / calibration / drift metrics, not a search index. That's the gap this redesign closes.

---

Compiled by kiro-local, 2026-04-30. All numbers above are from the current `wiki-search-index.json` (301 docs, 49 archived, 196 drafts, 54 in review, 16 FINAL, index generated 2026-04-25). Companion: `dashboard-redesign-report.html`, `mockups.html`.
