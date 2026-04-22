# Dashboard Learnings Roadmap — Design

## Overview

This document is the roadmap itself. It synthesizes findings from 18 external marketing-tool GitHub repositories into a prioritized, decision-ready inventory of changes to the Kiro Dashboard and adjacent tooling. Every item is classified, evidence-traced, Five-Levels-tagged, soul-principle-checked, and effort×leverage-sized per the requirements in requirements.md.

**Reading order**: Top 10 ranked items → Connections Map → Removals → Anti-goals → Appendices.

**Sort key**: leverage × inverse-effort × L-tier-proximity. High/XS/L2 items appear first.

---

## Architecture

This is a document spec, not an implementation spec. The "architecture" is the classification framework itself:

```
  EXTERNAL PATTERN (18 repos)
         |
         v
  +------------------+
  | Classification    |
  | Engine            |
  |  IMPROVE          |  -- fits existing dashboard, L1/L2, structural, effort <= L
  |  BUILD-STANDALONE |  -- too distinct to graft, or needs team adoption
  |  REMOVE           |  -- unused / redundant / cosmetic-drift / superseded
  |  NOTE-FOR-LATER   |  -- L4+, or XL effort with no leverage jump
  +------------------+
         |
         v
  RANKED ROADMAP (this document)
         |
         v
  FOLLOW-ON SPECS (one per chosen item, created in separate sessions)
```

---

## Components and Interfaces

Not applicable — this spec produces a document, not software components.

---

## Data Models

Not applicable — no new data structures are introduced. Follow-on specs will define their own data models.

---

## Top 10 Ranked Items

### 1. `BUILD-STANDALONE` — PPC Financial Calculator + A/B Test Designer

**Sources**: claude-ads `/ads math` (CPA, ROAS, break-even, budget forecasting, LTV:CAC), claude-ads `/ads test` (hypothesis framework, statistical significance, sample size, duration calculator), anita-owens/Machine-Learning-R (A/B ANOVA with post-hoc tests), anita-owens/Marketing-Analytics-Python (correlation analysis for marketing performance)

**Internal status**: `MISSING`. No test-sizing calculator, no statistical significance checker, no CPA/ROAS calculator anywhere in the dashboard or adjacent tools. Tests tracked in `ps-testing-dashboard.xlsx` (SharePoint spreadsheet tracking test status across all markets) have no built-in math.

**Five Levels**: L2 (Drive WW Testing) — directly enables test methodology ownership. This is the single highest-fit missing tool for the active tier.

**Soul principle**: Structural over cosmetic — embeds test math into the workflow rather than requiring Richard to open a separate spreadsheet or Google "sample size calculator."

**Effort**: S (2–8h) — pure-function calculator, no external dependencies, can be a standalone HTML page or dashboard tab.

**Leverage**: High — compounds across every test Richard designs; replaces multiple manual steps with a single tool; unblocks L2 metric "every test has written status" by making test design frictionless.

**Follow-on**: `spec ps-test-calculator`

---

### 2. `IMPROVE` — WBR Health Score (composite weighted scoring)

**Sources**: ai-marketing-claude (6 dimensions × 0-10, composite 0-100), claude-ads (250+ checks, Ads Health Score 0-100, A-F grading), advertising-hub auditor (200+ checkpoints with severity scoring). Industry convergence: 3+ sources use weighted multi-dimension scoring.

**Internal status**: `HAS-IT-WEAK`. Callout reviewer rubric has 8 dimensions, 0-10, two-lens scoring — but no composite health score, no aggregate across markets/weeks. The score exists per-callout but doesn't roll up.

**Five Levels**: L1 (Sharpen Yourself) — a single WBR Health Score in Command Center (dashboard home view with Hero, Daily Blocks, Integrity Ledger, Actionable Intelligence) gives Richard an instant read on whether the week's output is improving.

**Soul principle**: Reduce decisions not options — one number replaces scanning 8 dimensions across multiple markets. The detail is still there; the default is the aggregate.

**Effort**: S (2–8h) — the scoring dimensions already exist in the callout reviewer. This is a rollup calculation + one new line in Command Center.

**Leverage**: High — compounds weekly; makes quality trend visible without opening individual callout reviews.

**Follow-on**: `spec wbr-health-score`

---

### 3. `IMPROVE` — Hard-gate rules for WBR pipeline

**Sources**: claude-ads "3x Kill Rule" (CPA >3x target = pause), budget sufficiency gates, learning phase protection; advertising-hub PPC strategist QS distribution targets, budget utilization gates. Convergence: 2+ sources enforce quality gates as hard rules, not informational flags.

**Internal status**: `HAS-IT-WEAK`. `ps.market_constraints` (DuckDB view containing regime-based constraints per market) has regime-based constraints, but they're informational — nothing blocks a callout from publishing if forecast miss is >30% for 3 consecutive weeks. Prediction calibration flags exist but aren't enforced.

**Five Levels**: L1 (Sharpen Yourself) — prevents publishing a callout that misrepresents performance, which directly protects artifact quality.

**Soul principle**: Protect the habit loop — the callout pipeline's cue→routine→reward stays the same, but a hard gate inside the routine catches errors before they reach the WBR. The habit shape doesn't change; the quality floor rises.

**Effort**: S (2–8h) — add 2-3 conditional checks in the callout reviewer step. If forecast miss >30% for 3+ weeks, flag for manual review. If CPA deviation >2x target, require explicit override.

**Leverage**: High — prevents compounding errors in the WBR narrative; one bad callout can mislead the entire leadership chain.

**Follow-on**: `spec callout-quality-gates`

---

### 4. `IMPROVE` — Agent Success Metrics in agent definitions

**Sources**: advertising-hub agent specs each include "Success Metrics" with quantitative targets (e.g., "200+ checkpoints evaluated", "80%+ implementation rate within 30 days").

**Internal status**: `HAS-IT-WEAK`. soul.md has Five Levels with key metrics, but individual agent definitions (market-analyst.md, callout-writer.md, etc.) don't have explicit measurable success criteria. You can't tell if an agent is performing well without reading its output manually.

**Five Levels**: L1 (Sharpen Yourself) — measurable agent metrics make it clear whether the system is improving week over week.

**Soul principle**: Structural over cosmetic — adding a "Success Metrics" section to each agent definition changes the default from "did it run?" to "did it perform?" This is a structural change to how agents are evaluated.

**Effort**: XS (<2h) — add a 3-5 line section to each of ~6 agent definition files. No code changes.

**Leverage**: Medium — noticeable friction reduction when evaluating agent quality; enables future automated agent health checks.

**Quick win**: Yes — XS effort, Medium leverage, L1 alignment.

**Follow-on**: `spec agent-success-metrics`

---

### 5. `IMPROVE` — Testing status quick-toggle in Command Center

**Sources**: babel-system one-click status cycle (Live → In Progress → Being Refreshed) on asset rows, no modal needed.

**Internal status**: `HAS-IT-WEAK`. Integrity Ledger (tabbed commitment tracker in Command Center) has status pills with click-to-cycle (not_started → in_progress → done). But tests tracked in `ps-testing-dashboard.xlsx` have NO quick-toggle — status updates require opening the SharePoint spreadsheet. The pattern exists in the dashboard but doesn't extend to tests.

**Five Levels**: L2 (Drive WW Testing) — "every test has written status" is the L2 key metric. A quick-toggle in Command Center makes status updates a 1-second action instead of a 30-second spreadsheet round-trip.

**Soul principle**: Reduce decisions not options — the status options don't change; the friction to update them drops to near-zero. Invisible over visible — the toggle writes back to the data source without Richard noticing the plumbing.

**Effort**: M (1–3 days) — needs a new "Testing" section in Command Center, data binding to `ps-testing-dashboard.xlsx` or an Asana project, and write-back logic.

**Leverage**: High — directly unblocks the L2 key metric by making test status updates trivially easy.

**Follow-on**: `spec testing-status-toggle`

---

### 6. `IMPROVE` — System Health Dashboard (MCP + Agents + Hooks) in Body System view

**Sources**: advertising-hub `mcp-servers/registry.yaml` (platform, name, repo, status, tools list); advertising-hub agent specs with quantitative Success Metrics per agent; marketing-os-starter `campaign-history.md` (what-changed log); observed internal gap — karpathy-via-subagent 4/20 failure was invisible because there's no invocation log.

**Internal status**: `HAS-IT-WEAK` (partial). Body System has a static Agent Health card (success metrics from JSON definitions) and `ops.hook_executions` / `ops.workflow_executions` capture some runtime data for backend hooks. But there is no surface showing (a) which MCP servers are alive, (b) last-invoked / invocation-count per custom agent, (c) routing-adherence rate (of messages matching soul.md triggers, % that routed to the specialist vs were handled by main), (d) invoke-status including "unreachable" for structural failures (e.g., karpathy not exposed via invokeSubAgent), or (e) hook last-run and failure trend visible at a glance.

**Five Levels**: L1 (Sharpen Yourself) — system health visibility prevents wasted time debugging tool failures and surfaces shelfware agents for removal.

**Soul principle**: Invisible over visible — the health check runs automatically; Richard only sees it when something is wrong. Subtraction before addition — the dashboard's first job is surfacing agents/hooks to delete, not admiring the ones that exist.

**Effort**: M (1–3 days). Three layered deliverables:
- **Tier 1 (must have)**: `ops.agent_invocations` table + logging shim that captures every custom-agent invocation (timestamp, agent name, caller, invoke status = success/failed/unreachable/timed_out, duration). Render last-invoked + 7d/30d invocation counts per agent in Body System.
- **Tier 1 (must have)**: Hook last-run + recent-failure badges pulled from existing `ops.hook_executions` / `ops.hook_reliability`. No new logging — just surface what's already captured.
- **Tier 2 (should have)**: MCP server registry parsed from `mcp.json` configs + lightweight health-check ping. Green/yellow/red per server. Alert only on failure.
- **Tier 3 (nice to have)**: Routing-adherence metric — of chat messages matching a soul.md routing trigger (rw-trainer, karpathy, wiki-editor, etc.), % that actually routed. Requires tagging chat inputs with matched-trigger metadata; punt to a follow-on experiment if too costly.

**Leverage**: High (widened from Medium). Compounds daily — answers "is this agent earning its keep?" and "which hooks failed overnight?" in one surface. Replaces three black boxes (agent liveness, hook reliability, MCP status) with one panel.

**Adoption risk**: Do not build unless committed to one monthly review that acts on the signals (kills idle agents, fixes failing hooks). Otherwise this is decoration.

**Follow-on**: `spec system-health-dashboard` (widened from former `spec mcp-health-dashboard`).

---

### 7. `IMPROVE` — Dry-run flag for high-risk write operations

**Sources**: google-ads-mcp requires `confirm=True` for all write tools — dry-run by default.

**Internal status**: `HAS-IT-WEAK`. `/api/feedback` (POST endpoint in Command Center for submitting feedback) writes to disk immediately. Some hooks fire automatically. `state-file-constraints-sync` writes to SharePoint without confirmation. Most read operations are safe, but write operations lack a consistent safety pattern.

**Five Levels**: L1 (Sharpen Yourself) — prevents accidental writes that corrupt state files or publish unreviewed content.

**Soul principle**: Protect the habit loop — a dry-run default doesn't change the workflow shape; it adds a confirmation step that prevents the "oh no I just overwrote the state file" moment that breaks the routine.

**Effort**: S (2–8h) — add a `dry_run=True` default parameter to the 3-4 write operations that touch SharePoint or state files. Log what would happen instead of doing it.

**Leverage**: Medium — low-frequency but high-consequence protection. One bad write can cost an hour of recovery.

**Follow-on**: `spec dry-run-writes`

---

### 8. `BUILD-STANDALONE` — Framework consolidation file

**Sources**: marketing-os-starter `marketing-wisdom.md` (6 Hook Formulas, BOFU Domination, 7 Growth Playbooks — single file all agents consult), coreyhaines31/marketingskills `product-marketing-context` (foundation file read by all 35+ skills first).

**Internal status**: `HAS-IT-WEAK`. `callout-principles.md` + `callout-writer.md` + `richard-writing-style.md` + multiple style guides exist but are spread across files. Each agent loads 2-4 context files before starting work. Consolidation would reduce agent context-loading overhead.

**Five Levels**: L1 (Sharpen Yourself) — faster agent startup = faster artifact output.

**Soul principle**: Subtraction before addition — this is consolidation, not creation. Fewer files, same content. **Risk**: creating a monolith that's hard to maintain. Mitigate by keeping the consolidated file as a read-only index that references (not replaces) the source files.

**Effort**: M (1–3 days) — audit all context files agents load, create a single `ps-context-index.md` that agents read first, update agent definitions to reference it.

**Leverage**: Medium — reduces agent startup latency and context-loading errors. Not high because the current multi-file approach works, just slowly.

**Note**: Per Subtraction before addition, this should consolidate existing files, not add new content. If the consolidation creates a file larger than any individual source, reconsider.

**Follow-on**: `spec context-consolidation`

---

### 9. `REMOVE` — Command Center Scratchpad

**Internal status**: Scratchpad section in Command Center uses localStorage only — no sync, no persistence across devices, no consumer reads it back. No external source validates this pattern.

**Reason**: Unused / no consumer. localStorage-only means it doesn't survive a browser clear or device switch. Richard has Asana for task capture, Slack for quick notes, and the intake folder for learnings. The Scratchpad adds a fourth capture surface with zero durability.

**Risk if removed**: None identified. No hook, script, or agent reads Scratchpad data. Verify: check `shared/dashboards/index.html` for any `localStorage.getItem('scratchpad')` calls outside the Scratchpad section itself.

**Soul principle**: Subtraction before addition — removing a zero-durability capture surface that competes with 3 durable alternatives.

**Effort**: XS (<2h). **Leverage**: Medium (reduces decision fatigue about where to capture notes).

**Follow-on**: included in `spec command-center-cleanup`

---

### 10. `REMOVE` — Legacy and duplicate forecast files

**Candidates**:
- `build-forecast-tracker.py.legacy` — legacy file, likely superseded by current `refresh-forecast.py`
- `richard-forecast-tracker.xlsx` vs `ps-forecast-tracker.xlsx` — possible duplication; verify which is consumed by `refresh-forecast.py`
- `sp-forecast-tracker-check.xlsx` — unclear purpose, may be a one-time validation artifact

**Reason**: Redundant / superseded. Multiple forecast-related files create confusion about which is the source of truth.

**Risk if removed**: Could break `refresh-forecast.py` if it references the legacy file. **Verification step**: grep `refresh-forecast.py` for all `.xlsx` and `.legacy` references before removing.

**Soul principle**: Subtraction before addition — three forecast files where one suffices is complexity drift.

**Effort**: XS (<2h). **Leverage**: Medium (eliminates "which forecast file is current?" confusion).

**Follow-on**: included in `spec command-center-cleanup`

---

### 11. `IMPROVE` — "What changed since last look?" badges

**Sources**: babel-system `lastUpdated` timestamps on every asset; marketing-os-starter `campaign-history.md` that logs what changed between sessions.

**Internal status**: `MISSING`. Every time Richard opens the dashboard, it looks the same. There's no visual diff — no "3 new items since yesterday" badge, no "forecast updated 2h ago" indicator, no "2 commitments aged past 7 days" alert. The dashboard is a snapshot, not a changelog.

**Five Levels**: L1 (Sharpen Yourself) — makes the morning glance immediately informative about what's new, rather than requiring Richard to remember yesterday's state.

**Soul principle**: Invisible over visible — the change detection runs automatically; Richard only notices when something actually changed. The dashboard looks the same when nothing changed, and subtly different when something did.

**Effort**: S (2–8h) — store a `last_seen` timestamp in localStorage, compare against `command-center-data.json` generated timestamp and item counts. Show small badge counts on sections that have new/changed items.

**Leverage**: High — compounds daily; transforms the morning glance from "scan everything" to "scan what's new."

**Follow-on**: `spec dashboard-change-badges`

---

### 12. `IMPROVE` — Data staleness indicator

**Sources**: advertising-hub MCP registry status indicators; claude-ads Context Intake that verifies data freshness before analysis.

**Internal status**: `HAS-IT-WEAK`. The dashboard shows "Updated [timestamp]" in the topbar, but it's easy to miss. If data is 18 hours stale, the dashboard looks identical to fresh data. There's no visual degradation signal.

**Five Levels**: L1 (Sharpen Yourself) — prevents acting on stale data without realizing it.

**Soul principle**: Invisible over visible — a subtle color shift on the timestamp (green = <4h, yellow = 4-12h, red = >12h) signals staleness without adding a new UI element. The timestamp is already there; the color is the only change.

**Effort**: XS (<2h) — add a CSS class toggle based on `Date.now() - generated` timestamp. Three colors, one conditional.

**Leverage**: Medium — low-frequency but prevents the "I made a decision based on yesterday's data" failure mode.

**Quick win**: Yes — XS effort, Medium leverage, L1 alignment.

**Follow-on**: `spec dashboard-staleness-indicator`

---

### 13. `IMPROVE` — Inline action links from Intelligence table

**Sources**: babel-system asset URL field (link each asset to its live page); advertising-hub Buddy orchestrator routing (click → route to specialist agent).

**Internal status**: `MISSING`. The Actionable Intelligence table shows Communicate/Delegate/Differentiate items with a dismiss button. But there's no "do it" button — no way to draft the email, create the Asana task, or open the Slack thread directly from the row. Every item requires context-switching to another tool.

**Five Levels**: L1 (Sharpen Yourself) — reduces the gap between "I see what to do" and "I'm doing it."

**Soul principle**: Reduce decisions not options — an "action" link per row that opens the right tool (Outlook for Communicate, Asana for Delegate, relevant doc for Differentiate) reduces the "where do I go to do this?" decision to zero.

**Effort**: M (1–3 days) — needs per-type action URL generation. Communicate items need an Outlook compose link or Slack deep-link. Delegate items need an Asana task creation link. Differentiate items need a link to the relevant artifact or doc.

**Leverage**: High — transforms the Intelligence table from "things to think about" to "things to do right now." Directly reduces the gap between seeing and acting.

**Follow-on**: `spec intelligence-action-links`

---

## Removals (meeting ceiling(N/3) requirement)

With 11 addition items (items 1-8, 11-13), the minimum removal count is ceiling(11/3) = 4. We have 4 removal candidates:

| # | Surface | Reason | Risk | Verification needed |
|---|---------|--------|------|-------------------|
| R1 | Command Center Scratchpad | localStorage-only, no sync, no consumer, 3 durable alternatives exist | None identified | Check index.html for scratchpad reads outside its own section |
| R2 | `build-forecast-tracker.py.legacy` | Superseded by current pipeline | Could break if referenced | Grep `refresh-forecast.py` for `.legacy` references |
| R3 | `richard-forecast-tracker.xlsx` OR `sp-forecast-tracker-check.xlsx` | Duplication / one-time artifact | Could break refresh script | Grep `refresh-forecast.py` for all `.xlsx` references |
| R4 | `karpathy-autoresearch-lab.xlsx` | Unclear if still consumed by any process | Could lose data if actively used | Check DuckDB `ops.data_freshness` for last read timestamp; check hooks for references |

**Note**: If verification shows any of R2-R4 are actively consumed, they move from REMOVE to IMPROVE (rename/consolidate) rather than being dropped from the list.

---

## Connections Map

```
PATTERN                          EXTERNAL SOURCES                    INTERNAL ANALOG                  STATUS             DECISION
-------------------------------  ----------------------------------  -------------------------------  -----------------  -------------------
Foundation context document      marketing-os-starter CLAUDE.md,     body.md / soul.md / amcc.md      HAS-IT-STRONG      Positive validation
                                 marketingskills product-marketing-
                                 context, advertising-hub agent
                                 specs, ai-marketing-claude SKILL.md,
                                 babel-system campaign JSON

Weighted multi-dimension score   ai-marketing-claude (6-dim),        Callout reviewer rubric          HAS-IT-WEAK        IMPROVE (#2)
                                 claude-ads (250+ checks),           (8-dim, no composite)
                                 advertising-hub auditor

Quality gates as hard rules      claude-ads "3x Kill Rule",          ps.market_constraints            HAS-IT-WEAK        IMPROVE (#3)
                                 advertising-hub PPC strategist      (informational only)

PPC calculator + test designer   claude-ads /ads math + /ads test,   (none)                           MISSING            BUILD-STANDALONE (#1)
                                 anita-owens ML-R, anita-owens
                                 Marketing-Analytics-Python

Status quick-toggle              babel-system one-click cycle        Integrity Ledger has it;         HAS-IT-WEAK        IMPROVE (#5)
                                                                     testing dashboard doesn't

Parallel subagent delegation     ai-marketing-claude (5 parallel),   Callout pipeline, market         HAS-IT-STRONG      Positive validation
                                 claude-ads (6+4 agents),            analyst replays, wiki pipeline
                                 marketing-os-starter (4-agent),
                                 advertising-hub (25+ agents)

Agent spec with success metrics  advertising-hub agent specs         soul.md Five Levels metrics;     HAS-IT-WEAK        IMPROVE (#4)
                                                                     individual agents lack them

Dry-run-by-default               google-ads-mcp confirm=True         Partial — some writes lack       HAS-IT-WEAK        IMPROVE (#7)
                                                                     confirmation

MCP server registry              advertising-hub registry.yaml       mcp.json exists but not          HAS-IT-WEAK        IMPROVE (#6 — widened
Agent invocation telemetry       advertising-hub agent Success       Static agent success metrics     to System Health
Hook reliability surfacing       Metrics; observed internal          exist; invocation count/        Dashboard covering
                                 karpathy-unreachable gap            last-run/routing-adherence      MCP + agents + hooks)
                                                                     not surfaced; ops.hook_
                                                                     executions not rendered

Framework consolidation          marketing-os-starter marketing-     Multiple style/context files     HAS-IT-WEAK        BUILD-STANDALONE (#8)
                                 wisdom.md, marketingskills           spread across system
                                 product-marketing-context

Context intake upfront           claude-ads "collect context first"  amcc.md check (streak +          HAS-IT-STRONG      Positive validation
                                                                     hard thing) runs first

Economic agent / budget-aware    Franklin YOPO, Smart Router         (none — intentional)             INTENTIONALLY-      NOTE-FOR-LATER
                                                                                                      OMITTED

Cross-platform attribution       advertising-hub Audience            (none — intentional)             INTENTIONALLY-      NOTE-FOR-LATER
                                 Architect, Attribution Analyst                                        OMITTED

Change-since-last-look signal    babel-system lastUpdated,           (none)                           MISSING            IMPROVE (#11)
                                 marketing-os-starter campaign-
                                 history.md

Data staleness indicator         advertising-hub MCP registry        Topbar timestamp exists but      HAS-IT-WEAK        IMPROVE (#12)
                                 status, claude-ads Context Intake   no visual degradation signal

Inline action from table         babel-system asset URL field,       Intelligence table has dismiss    MISSING            IMPROVE (#13)
                                 advertising-hub Buddy routing       but no "do it" action link
```

**Industry convergence signals** (3+ independent sources):
- Foundation context document (5+ sources) → HAS-IT-STRONG ✓
- Weighted multi-dimension scoring (3+ sources) → HAS-IT-WEAK → IMPROVE
- Parallel subagent delegation (4+ sources) → HAS-IT-STRONG ✓

---

## Anti-goals

1. **No cross-platform ad management.** advertising-hub's Audience Architect and Attribution Analyst handle Google/Meta/LinkedIn cross-platform orchestration. PS operates within Google Ads. Cross-platform attribution is MCS territory, not PS. (Pattern 13: INTENTIONALLY-OMITTED)

2. **No autonomous paid transactions.** Franklin's YOPO pay-per-outcome model and Smart Router (per-task model routing by cost/quality ratio) are real innovations, but PS doesn't run autonomous paid transactions. The Smart Router concept is interesting for L5 (Agentic Orchestration) but not actionable at L1/L2. (Pattern 12: INTENTIONALLY-OMITTED)

3. **No wholesale repo forks.** The mandate is pattern-extraction, not code-lift. babel-system's campaign framework, marketing-os-starter's agent pipeline, and advertising-hub's 25-agent architecture are instructive but not transplantable. Each finding must be adapted to PS's existing shape.

4. **No newsletter/email/AR marketing tools.** Tier C repos (listmonk, CampaignGenerator, webar, MapCampaigner, ai-ad-campaign-manager) are wrong-surface for PS work. PS doesn't own email marketing, AR experiences, or generic ad campaign management outside Google Ads.

5. **No L4/L5 tooling that pulls focus from L1/L2.** Agentic orchestration (L5) and zero-click futures (L4) are queued, not active. Any finding that requires L4/L5 infrastructure without also advancing L1/L2 is deferred. This includes: autonomous workflow execution, multi-model routing, and self-healing agent pipelines.

6. **No cosmetic dashboard changes.** Section reordering, new color schemes, emoji additions, and layout tweaks are rejected unless they embody a soul principle. The callout dashboard doesn't need to look different — it needs to work better structurally.

7. **No tools requiring teammate adoption without named adoption plan.** L3 (Team Automation) items that assume teammates will adopt a tool without naming the specific person, their current tool, and the migration friction are deferred. Building tools nobody uses is worse than building nothing.

---

## Error Handling

Not applicable — this spec produces a document, not software. Follow-on specs will define error handling for their respective implementations.

---

## Testing Strategy

**PBT applicability assessment**: Property-based testing does not apply to this feature. This spec produces a prioritized document (the roadmap), not executable code with input/output behavior. There are no pure functions, parsers, serializers, or algorithms to validate with universal properties.

**Validation approach for this roadmap**:
- **Manual review**: Richard reviews each item against the 9 requirements for completeness
- **Traceability check**: Every item must trace to at least one source repo + file/section
- **Ratio verification**: Removals count ≥ ceiling(additions/3) — currently 4 ≥ ceiling(11/3) = 4 ✓
- **Five Levels alignment**: No item tagged above L2 appears in the top 10 without explicit justification
- **Soul principle audit**: Every IMPROVE/BUILD-STANDALONE item has at least one principle citation

**Follow-on spec testing**: Each follow-on spec (e.g., `spec ps-test-calculator`, `spec wbr-health-score`) will define its own testing strategy appropriate to its implementation. The PPC calculator, for example, would be an excellent candidate for property-based testing (pure functions with clear input/output behavior).

---

## Appendix A: NOTE-FOR-LATER Items (grouped thematically)

### Agent Architecture
- **Economic agent / budget-aware execution** (Franklin Smart Router): Per-task model routing by cost/quality ratio. Interesting for L5 but PS doesn't run autonomous paid transactions. Source: Franklin YOPO model. L5 tag. DEFER.
- **Cross-platform audience/attribution** (advertising-hub Audience Architect): First-party data activation across platforms, incrementality testing, media mix modeling. PS operates within Google Ads. Source: advertising-hub. L5 tag. DEFER.

### Content & Frameworks
- **Hormozi content frameworks** (Marketing-Swarm-Template): 10 platform-specific content agents with Hormozi frameworks, `agents.yaml` variable placeholder pattern. Interesting template but PS content is WBR narratives and test designs, not social media posts. Source: Marketing-Swarm-Template. L3 tag. DEFER — would need team adoption.
- **BigQuery → ad platform data sync** (marketing-data-sync): Apache Beam/Dataflow pipeline for audience onboarding. PS uses DuckDB + SharePoint, not BigQuery. Source: DP6/marketing-data-sync. L4 tag. DEFER.

### Scoring & Analytics
- **Industry detection from account signals** (claude-ads): Automatically detect advertiser industry from account data to contextualize recommendations. PS works within a known vertical (Amazon Business Paid Search on Google Ads). Source: claude-ads. L3 tag. DEFER — low value in single-vertical context.
- **Correlation analysis for marketing performance** (anita-owens Marketing-Analytics-Python): Automated correlation detection between marketing variables. Interesting for forecast improvement but requires statistical infrastructure. Source: anita-owens/Marketing-Analytics-Python. L3 tag. DEFER.

---

## Appendix B: Positive Validations (things Kiro already does well)

These patterns appear in multiple external sources AND are already strong in the Kiro system. No action needed — they confirm the current architecture is sound.

1. **Foundation context document** (5+ sources): body.md / soul.md / amcc.md is a stronger implementation than any single external source. marketing-os-starter's CLAUDE.md is the closest analog but lacks the organ-based navigation and streak tracking.

2. **Parallel subagent delegation** (4+ sources): Callout pipeline (analyst → writer → reviewer), market-analyst replays (6 parallel), wiki pipeline (editor → researcher → writer → critic → librarian) — already doing this well. advertising-hub's 25-agent architecture is larger but not better-structured.

3. **Context intake upfront** (2+ sources): amcc.md check (streak + hard thing) before any work begins is more disciplined than claude-ads' "collect context first" pattern, which is optional.

---

## Appendix C: Full Item Metadata

| # | Category | Title | Sources | Internal Status | Five Levels | Soul Principle | Effort | Leverage | Follow-on Spec |
|---|----------|-------|---------|----------------|-------------|---------------|--------|----------|---------------|
| 1 | BUILD-STANDALONE | PPC Calculator + Test Designer | claude-ads, anita-owens (2 repos) | MISSING | L2 | Structural over cosmetic | S | High | ps-test-calculator |
| 2 | IMPROVE | WBR Health Score | ai-marketing-claude, claude-ads, advertising-hub | HAS-IT-WEAK | L1 | Reduce decisions not options | S | High | wbr-health-score |
| 3 | IMPROVE | Hard-gate rules for WBR pipeline | claude-ads, advertising-hub | HAS-IT-WEAK | L1 | Protect the habit loop | S | High | callout-quality-gates |
| 4 | IMPROVE | Agent Success Metrics | advertising-hub | HAS-IT-WEAK | L1 | Structural over cosmetic | XS | Medium | agent-success-metrics |
| 5 | IMPROVE | Testing status quick-toggle | babel-system | HAS-IT-WEAK | L2 | Reduce decisions not options | M | High | testing-status-toggle |
| 6 | IMPROVE | System Health Dashboard (MCP + Agents + Hooks) | advertising-hub, observed-internal | HAS-IT-WEAK | L1 | Invisible over visible | M | High | system-health-dashboard |
| 7 | IMPROVE | Dry-run flag for writes | google-ads-mcp | HAS-IT-WEAK | L1 | Protect the habit loop | S | Medium | dry-run-writes |
| 8 | BUILD-STANDALONE | Framework consolidation file | marketing-os-starter, marketingskills | HAS-IT-WEAK | L1 | Subtraction before addition | M | Medium | context-consolidation |
| R1 | REMOVE | Command Center Scratchpad | (no external validation) | Unused | L1 | Subtraction before addition | XS | Medium | command-center-cleanup |
| R2 | REMOVE | build-forecast-tracker.py.legacy | INTERNAL | Superseded | L1 | Subtraction before addition | XS | Medium | command-center-cleanup |
| R3 | REMOVE | Duplicate forecast xlsx files | INTERNAL | Redundant | L1 | Subtraction before addition | XS | Medium | command-center-cleanup |
| R4 | REMOVE | karpathy-autoresearch-lab.xlsx | INTERNAL | Unclear consumption | L1 | Subtraction before addition | XS | Low | command-center-cleanup |
| 11 | IMPROVE | Change-since-last-look badges | babel-system, marketing-os-starter | MISSING | L1 | Invisible over visible | S | High | dashboard-change-badges |
| 12 | IMPROVE | Data staleness indicator | advertising-hub, claude-ads | HAS-IT-WEAK | L1 | Invisible over visible | XS | Medium | dashboard-staleness-indicator |
| 13 | IMPROVE | Inline action links from Intelligence | babel-system, advertising-hub | MISSING | L1 | Reduce decisions not options | M | High | intelligence-action-links |

**Quick wins** (XS/S effort + High leverage + L1/L2): Items 1, 2, 3, 4, 11, 12

---

## Glossary

- **Kiro Dashboard**: Richard's single-page web dashboard at `~/shared/dashboards/index.html` with 5 views (Command Center, Performance, Body System, State Files, Wiki Search)
- **Command Center**: Dashboard home view with Hero (highest-leverage item), Daily Blocks (4-column WIP-capped task view), Integrity Ledger (tabbed commitment tracker), Actionable Intelligence (3-type table: Communicate/Delegate/Differentiate), Scratchpad (tabbed notes)
- **Five Levels**: Richard's sequential strategic priorities — L1 Sharpen Yourself → L2 Drive WW Testing → L3 Team Automation → L4 Zero-Click Future → L5 Agentic Orchestration. Each funds the next; don't skip ahead.
- **Soul principles**: The 6 "How I Build" principles in `soul.md` — Routine as liberation, Structural over cosmetic, Subtraction before addition, Protect the habit loop, Invisible over visible, Reduce decisions not options
- **Callout**: A short narrative (100-120 words) summarizing a market's weekly performance for the WBR, produced by the callout pipeline (analyst → writer → reviewer)
- **State file**: Per-market markdown file at `~/shared/context/active/` and in SharePoint `Kiro-Drive/state-files/` that captures current metrics + active initiatives per market
- **Canon-chart**: Shared JavaScript chart component (`canon-chart.js`) used by both the callout dashboard and forecast tracker for consistent visualization
- **Integrity Ledger**: Tabbed section in Command Center that tracks commitments (tasks, promises, deliverables) with status pills (not_started / in_progress / done)
- **Body System**: Dashboard tab showing the "body" metaphor — organs (brain, spine, amcc, etc.) representing different system components and their health
- **WBR**: Weekly Business Review — the recurring leadership meeting where market performance is presented via callouts
- **Convergence signal**: A pattern appearing in 3+ independent external sources, suggesting it's industry practice rather than one person's preference
- **ps.market_constraints**: DuckDB view containing regime-based constraints per market (e.g., budget floors, CPA ceilings) used by the forecast and callout systems
- **ps-testing-dashboard.xlsx**: SharePoint spreadsheet tracking test status (hypothesis, design, launch date, results) across all markets
- **rw-tracker**: Richard Williams tracker — a hook-generated summary of daily progress, streaks, and blockers pushed to SharePoint for cross-device access
- **MCP server**: Model Context Protocol server — a tool integration that exposes external services (Slack, Asana, SharePoint, Outlook, etc.) to the AI agent via a standardized interface
- **Adjacent tools**: Tools Richard uses daily but that aren't the dashboard itself — Asana, Slack, SharePoint, Outlook, Hedy, MCP servers, wiki pipeline, WBR callout pipeline, forecast tracker, Excel files (`.xlsx` dashboards and trackers), Word documents (`.docx` published artifacts), Google Ads platform (the ad platform where PS campaigns run)
