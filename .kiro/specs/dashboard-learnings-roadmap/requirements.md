# Dashboard Learnings Roadmap — Requirements

## Purpose

Produce a prioritized, decision-ready roadmap of changes to the Kiro Dashboard and its adjacent tooling, drawn from a thorough survey of 18 external marketing-tool GitHub repositories and their referenced sources. The roadmap must tell Richard, unambiguously, what to build into the dashboard, what to build as standalone tools, what to remove, and what to note for later — with enough evidence that each decision is traceable back to a specific repo pattern or internal gap.

This is a **learnings/roadmap spec**, not an implementation spec. The output (which will live in design.md) is a prioritized inventory, not shippable code. A separate session will handle build planning (tasks.md) for chosen items.

## Scope

### In scope

- The Kiro Dashboard at `~/shared/dashboards/` (Command Center, Performance, Body System, State Files, Wiki Search) plus its refresh scripts, DuckDB views, SharePoint artifacts, and hooks
- Patterns extracted from 18 external repos (see §Source Inventory below) and their linked references
- The "adjacent tools" Richard uses daily: Asana, Slack, SharePoint, Outlook, Hedy, MCP servers, wiki pipeline, WBR callout pipeline, forecast tracker, body-system agents, Excel files (.xlsx dashboards and trackers), Word documents (.docx artifacts), Google Ads platform (the ad platform where PS campaigns run)

### Out of scope

- Building any of the recommended items (that's what separate spec work per chosen item will cover)
- Replacing existing tools (Asana, SharePoint, DuckDB) with repo alternatives — the mandate is learn-and-adapt, not rip-and-replace
- General-purpose marketing tooling unrelated to PS work (e.g., newsletter managers, AR marketing, WYSIWYG email editors)
- Recommendations Richard has already rejected in prior sessions (e.g., replacing Asana with a web UI, wholesale fork of babel-system)

## Source Inventory

All 18 repos have been read at README level or deeper. Deep-dive coverage per tier:

**Tier A — Deep crawl** (README + internal skill/agent files + referenced external tools):
1. `desireem-seb/babel-system` — open-source campaign builder, JSON storage, Anthropic-grounded content gen, status quick-toggle, asset tagging
2. `zubair-trabzada/ai-marketing-claude` — 15 `/market` commands, 5 parallel subagents, 6-dimension weighted scoring (0-10 per dimension, composite 0-100)
3. `AgriciDaniel/claude-ads` — 250+ ad audit checks, Quality Gates as hard rules, Context Intake upfront, `/ads math` PPC calculator, `/ads test` A/B test designer, industry detection from account signals
4. `itallstartedwithaidea/advertising-hub` — 14 platforms, 25+ agents (paid-media/cross-platform/orchestrator), shared core package (auth/models/rate-limiting/errors), MCP registry.yaml, agent spec template with measurable Success Metrics
5. `ericosiu/marketing-os-starter` — 4-agent team (Orchestrator/Researcher/Strategist/Copywriter), JSON schema handoffs, persistent memory (4 files that compound), `marketing-wisdom.md` (6 Hook Formulas, BOFU Domination, 7 Growth Playbooks, 3-Segment Activation, Price Ladder, Revenue-First measurement)
6. `coreyhaines31/marketingskills` (referenced by Eric Siu) — 35+ skills with cross-reference graph, `product-marketing-context` as foundation file read by all others first
7. `itallstartedwithaidea/google-ads-mcp` (referenced) — 29 Google Ads tools, dry-run-by-default safety pattern for writes (`confirm=True` required)
8. `irinabuht12-oss/google-meta-ads-ga4-mcp` — 250+ MCP tools across Google/Meta/GA4, OAuth 2.1 + PKCE, cross-platform ROAS comparison

**Tier B — README + one internal file**:
9. `The-Swarm-Corporation/Marketing-Swarm-Template` — 10 platform-specific content agents with Hormozi frameworks, `agents.yaml` variable placeholder pattern
10. `BlockRunAI/Franklin` — economic-agent category, YOPO pay-per-outcome, Smart Router classifier over 55+ models by quality-to-cost ratio
11. `DP6/marketing-data-sync` — BigQuery → ad platform onboarding pipeline (Apache Beam/Dataflow), Google Spreadsheet config layer
12. `anita-owens/Machine-Learning-R` — marketing campaign ML (logistic regression, decision trees, A/B ANOVA with post-hoc tests)
13. `anita-owens/Marketing-Analytics-Python` — correlation analysis for marketing performance, synthetic data simulation

**Tier C — README only** (confirmed wrong-surface, documented with reasoning):
14. `knadh/listmonk` — newsletter manager (wrong surface — PS doesn't own email marketing)
15. `leonma333/CampaignGenerator` — Angular/Firebase WYSIWYG email editor (wrong surface)
16. `aribairfan-indoverseai/ai-ad-campaign-manager` — generic AI ad mgr (duplicates existing capability without PS-specific value)
17. `walidabazo/webar` — AR marketing (wrong surface)
18. `hotosm/MapCampaigner` — OSM field data collection (wrong surface)

**Curated lists** (tool catalog scan, not deep crawl):
- `marketingtoolslist/awesome-marketing` — 200+ tools across 12 categories
- `paulbradish/awesome-digital-marketing` — 300+ tools across 35 categories (55KB README)

## Requirements

### Requirement 1: Four-category classification

**User story**: As Richard reviewing the roadmap, I want every item categorized cleanly so I can decide at a glance what to ship, what to build standalone, what to remove, and what to park.

**Acceptance criteria**:
1. WHEN the roadmap lists a finding THEN it SHALL be tagged as one of: `IMPROVE` (change to existing Kiro Dashboard/tool), `BUILD-STANDALONE` (new tool separate from the dashboard), `REMOVE` (subtraction from existing Kiro surface), or `NOTE-FOR-LATER` (pattern worth recording, not acting on)
2. WHEN a finding could fit more than one category THEN the roadmap SHALL pick the single best fit and explain the tradeoff in a one-line note (no dual-tagging)
3. WHEN a finding is tagged `REMOVE` THEN it SHALL include explicit justification — what gets removed and what measurable decision fatigue / complexity it eliminates (per soul principle Subtraction before addition)

### Requirement 2: Evidence tracing

**User story**: As Richard evaluating a roadmap item, I want to see where the idea came from so I can decide if the source is credible and if the pattern actually applies to PS work.

**Acceptance criteria**:
1. WHEN the roadmap lists a finding THEN it SHALL cite at least one specific source (repo + file path or section name, or adjacent-tool surface by name)
2. WHEN a finding claims a pattern appears across multiple sources THEN the roadmap SHALL name at least two sources and quote or paraphrase the common pattern
3. WHEN a finding is purely Richard-originated (not from the 18 repos) THEN it SHALL be tagged `INTERNAL` with the originating session or file
4. WHEN a finding is a pattern with no matching source THEN it SHALL NOT be included (prevents cargo-culting from imagination)
5. WHEN a curated-list repo (awesome-marketing, awesome-digital-marketing) is cited THEN it SHALL be supporting evidence only — never the sole source for a finding

### Requirement 3: Five Levels alignment

**User story**: As Richard deciding whether to act on a finding, I want to know which of the Five Levels it advances so I don't invest in something off-strategy.

**Acceptance criteria**:
1. WHEN the roadmap lists a finding THEN it SHALL tag exactly one primary Five Levels tier: L1 (Sharpen Yourself), L2 (Drive WW Testing), L3 (Team Automation), L4 (Zero-Click Future), L5 (Agentic Orchestration)
2. WHEN a finding advances a tier ranked above the current active tier (L2) AND does not also advance L1/L2 THEN the roadmap SHALL mark it `DEFER` and explain why it's not blocking current work (per the sequential-levels rule)
3. WHEN a finding is L1 or L2 THEN it SHALL be eligible for current-cycle action; higher tiers default to `NOTE-FOR-LATER` unless the roadmap explicitly argues otherwise
4. WHEN a finding is L3 (Team Automation) AND would require teammate adoption THEN the roadmap SHALL include an adoption-risk score (Low / Medium / High) with one-sentence rationale naming the specific teammates and their current tool

### Requirement 4: Soul-principle self-audit

**User story**: As Richard, I want the roadmap to self-audit against the 6 principles in soul.md so cosmetic changes and decision-multiplying additions don't sneak through.

**Acceptance criteria**:
1. WHEN the roadmap lists an `IMPROVE` or `BUILD-STANDALONE` finding THEN it SHALL be labeled against at least one of the 6 soul principles with format `{principle name}: {one-sentence justification}` — Routine as liberation / Structural over cosmetic / Subtraction before addition / Protect the habit loop / Invisible over visible / Reduce decisions not options
2. WHEN a finding violates a principle THEN the roadmap SHALL flag the violation explicitly and either justify the tradeoff or reclassify as `NOTE-FOR-LATER`
3. WHEN a finding embodies a principle well THEN the roadmap SHOULD call that out as bonus-signal

### Requirement 5: Effort × leverage sizing with follow-on spec

**User story**: As Richard sequencing work, I want a consistent sizing model so I can compare items apples-to-apples and know what spec to create next.

**Acceptance criteria**:
1. WHEN the roadmap lists an `IMPROVE` or `BUILD-STANDALONE` finding THEN it SHALL include an effort estimate from the set: `XS` (<2h), `S` (2–8h), `M` (1–3 days), `L` (1–2 weeks), `XL` (>2 weeks)
2. WHEN the roadmap lists an `IMPROVE` or `BUILD-STANDALONE` finding THEN it SHALL include a leverage score from the set: `High` (compounds / replaces multiple existing steps / unblocks a Five-Level jump), `Medium` (noticeable friction reduction), `Low` (small quality-of-life)
3. WHEN a finding is `XL` effort AND `Low` leverage THEN it SHALL be rejected or reclassified as `NOTE-FOR-LATER`
4. WHEN a finding is `XS`/`S` effort AND `High` leverage THEN it SHALL be flagged as a "quick win" candidate for the next execution cycle
5. WHEN a finding is `IMPROVE` or `BUILD-STANDALONE` THEN it SHALL name the follow-on spec it would require (e.g., "Follow-on: spec ps-testing-asset-repo") so the roadmap is actionable, not just informational

### Requirement 6: Connections map with internal-status tagging

**User story**: As Richard, I asked specifically to "find connections" between the repos and my existing tooling; I don't want another flat listicle. I also want to see where we're already strong vs where we're weak.

**Acceptance criteria**:
1. WHEN the roadmap is delivered THEN it SHALL include a separate Connections Map section showing, for each major pattern identified, the shape: `{external source(s)} → {internal dashboard/tool surface it maps to} → {decision: IMPROVE / BUILD-STANDALONE / REMOVE / NOTE-FOR-LATER}`
2. WHEN a pattern appears in 3+ external sources AND has an existing internal analog THEN it SHALL be flagged as "industry convergence" — convergence is a tiebreaker for priority, not a trump card; internal fit still dominates
3. WHEN an external source contains a pattern that the Kiro Dashboard already does well THEN the roadmap SHALL record that as positive validation (not a build item)
4. WHEN the Kiro Dashboard has a tool or section that appears in zero external sources AND has no documented user need THEN the roadmap SHALL flag it as a `REMOVE` candidate pending Richard's review
5. WHEN the roadmap identifies a pattern THEN it SHALL tag whether Kiro currently: `HAS-IT-STRONG` (fully implemented, better than most sources), `HAS-IT-WEAK` (implemented but could be improved — candidate for `IMPROVE`), `MISSING` (not present — candidate for `BUILD-STANDALONE` or `IMPROVE`), or `INTENTIONALLY-OMITTED` (not present for a good reason — worth documenting with reasoning)
6. WHEN a pattern touches multiple internal surfaces (e.g., a scoring system could apply to callouts AND forecasts AND tests) THEN the roadmap SHALL list it once with a "targets" field naming all applicable surfaces — not duplicated per surface

### Requirement 7: Removals discipline

**User story**: As Richard living the Subtraction before addition principle, I want the roadmap to not just propose adding — I want it to force-surface what could be dropped.

**Acceptance criteria**:
1. WHEN the roadmap proposes N new `IMPROVE` or `BUILD-STANDALONE` items THEN it SHALL also surface at least ceiling(N/3) `REMOVE` candidates (at a minimum — more is better)
2. WHEN a `REMOVE` candidate is proposed THEN it SHALL specify the surface (file path, dashboard section, script, hook, or table), the reason (unused / redundant / cosmetic-drift / superseded), and the risk if removed (e.g., "breaks hook X" or "no known consumer")
3. WHEN a `REMOVE` candidate cannot be verified as unused via existing data THEN the roadmap SHALL list the specific verification step needed (e.g., "check Asana project usage in last 30 days via `asana.asana_task_history`") rather than assuming safe-to-cut
4. WHEN the roadmap cannot find enough `REMOVE` candidates to meet the ratio THEN it SHALL explicitly state that fact with a one-line explanation rather than padding the list

### Requirement 8: Anti-goals

**User story**: As Richard, I want to see what the roadmap is NOT trying to do, so scope creep doesn't dilute the work.

**Acceptance criteria**:
1. WHEN the roadmap is delivered THEN it SHALL include an "Anti-goals" section stating at least five things the roadmap deliberately does not pursue
2. WHEN a source repo contains an impressive capability that doesn't fit PS work THEN it SHALL appear in Anti-goals with the reason (e.g., "Franklin's USDC wallet is real but PS does not run autonomous paid transactions")
3. WHEN a repo in Tier C appears THEN it SHALL be explicitly named in Anti-goals with its wrong-surface reason
4. WHEN the roadmap identifies a shiny-object risk (pattern that would feel productive but doesn't advance the Five Levels) THEN it SHALL be named in Anti-goals

### Requirement 9: Output format — portable and bounded

**User story**: As Richard reading this (and as a future AI on a different platform), I want a document I can read in one sitting, decide from, and understand cold without Kiro-specific context.

**Acceptance criteria**:
1. WHEN the roadmap is delivered THEN the design.md SHALL be no longer than ~3,000 words body text (appendices and connections map may extend beyond)
2. WHEN more than 20 `IMPROVE`/`BUILD-STANDALONE` candidates are identified THEN the roadmap SHALL rank them and present the top 10 inline, with the remainder in an appendix
3. WHEN more than 10 `NOTE-FOR-LATER` items are identified THEN they SHALL be grouped thematically in an appendix, not individually enumerated inline
4. WHEN the roadmap would benefit from a visual THEN a plain-text ASCII diagram SHALL suffice — no external image dependencies
5. WHEN the roadmap references a Kiro-specific surface (DuckDB table, hook name, Python script, SharePoint folder) THEN it SHALL describe the surface's purpose in one sentence on first reference
6. WHEN the roadmap cites a Five Levels tier THEN it SHALL briefly restate the tier name at first mention (e.g., "L2 Drive WW Testing")
7. WHEN the roadmap relies on internal vocabulary (callout, state file, canon-chart, rw-tracker) THEN it SHALL include a short glossary entry at end of document
8. WHEN the roadmap references a soul principle THEN it SHALL cite the principle by name (not by number alone)

## Decision Rules (how items move between categories)

These rules apply when the design phase classifies findings:

- **→ IMPROVE**: Pattern fits the existing dashboard shape, fits L1/L2, structural change (not cosmetic), effort ≤ L, leverage ≥ Medium
- **→ BUILD-STANDALONE**: Pattern is too distinct from the dashboard to graft on; OR needs team adoption where Richard's dashboard is personal-only; OR fits L3+ where current dashboard is L1/L2 focused
- **→ REMOVE**: Surface has unused / redundant / cosmetic-only properties; risk is low or verifiable; no known consumer
- **→ NOTE-FOR-LATER**: Pattern fits L4+ (Zero-Click Future, Agentic Orchestration) and Richard is not yet at that tier; OR pattern is valid but effort is `XL` with no corresponding leverage jump
- **Cosmetic-only gate**: Any finding whose primary benefit is cosmetic (new colors, new emojis, section reordering) SHALL be rejected or reclassified as `NOTE-FOR-LATER` unless it embodies a soul principle
- **Sort order**: Items SHALL be ranked by `(leverage × inverse-effort × L-tier-proximity)` — High/XS/L2 items first, Low/XL/L5 items last

## Anti-goals (preliminary — to be finalized in design)

1. Do not propose replacing Asana, SharePoint, DuckDB, or Slack with any repo alternative — these are infrastructure, not candidates
2. Do not propose wholesale forking of any repo — the mandate is pattern-extraction, not code-lift
3. Do not propose changes whose primary benefit is cosmetic unless they embody a soul principle
4. Do not propose L4/L5 tooling that would pull focus from L1/L2 (Sharpen Yourself is struggling, Drive WW Testing is active — these come first)
5. Do not propose tools that assume teammate adoption without naming the specific teammates, their current tool, and the migration friction

## Glossary (for portability)

- **Kiro Dashboard**: Richard's single-page web dashboard at `~/shared/dashboards/index.html` with 5 views (Command Center, Performance, Body System, State Files, Wiki Search)
- **Command Center**: Dashboard home view with Hero (highest-leverage item), Daily Blocks (4-column WIP-capped task view), Integrity Ledger (tabbed commitment tracker), Actionable Intelligence (3-type table: Communicate/Delegate/Differentiate), Scratchpad (tabbed notes)
- **Five Levels**: Richard's sequential strategic priorities — L1 Sharpen Yourself → L2 Drive WW Testing → L3 Team Automation → L4 Zero-Click Future → L5 Agentic Orchestration. Each funds the next; don't skip ahead.
- **Soul principles**: The 6 "How I Build" principles in `soul.md` — Routine as liberation, Structural over cosmetic, Subtraction before addition, Protect the habit loop, Invisible over visible, Reduce decisions not options
- **Adjacent tools**: Tools Richard uses daily but that aren't the dashboard itself — Asana (task management), Slack (communication), SharePoint (document durability), Outlook (email/calendar), Hedy (meeting transcription), MCP servers (tool integrations), wiki pipeline (article creation), WBR callout pipeline (weekly business review narratives), forecast tracker (prediction vs actuals), Excel files (`.xlsx` dashboards like ps-forecast-tracker, ps-testing-dashboard, command-center), Word documents (`.docx` published artifacts in SharePoint Artifacts/), Google Ads platform (the ad platform where PS campaigns run)
- **Convergence signal**: A pattern appearing in 3+ independent external sources, suggesting it's industry practice rather than one person's preference
- **State file**: Per-market markdown file at `~/shared/context/active/` and in SharePoint `Kiro-Drive/state-files/` that captures current metrics + active initiatives per market
- **Canon-chart**: Shared JavaScript chart component (`canon-chart.js`) used by both the callout dashboard and forecast tracker for consistent visualization
- **Callout**: A short narrative (100-120 words) summarizing a market's weekly performance for the WBR, produced by the callout pipeline (analyst → writer → reviewer)
