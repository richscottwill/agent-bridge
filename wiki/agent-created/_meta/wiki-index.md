---
title: "Wiki Index"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0449 | duck_id: wiki-meta-wiki-index -->

# Wiki Index

> A knowledge base for Amazon Business Paid Search. Covers operations, testing, market strategy, tools, and the agent system that manages it. Optimized for both human readers and AI agent consumption.
>
> Published articles live in `~/shared/wiki/`. This index is the discovery layer over that folder.

Last updated: 2026-04-05

---

## Articles

### Testing & Experimentation (13)

- [Testing Approach & Year Ahead](~/shared/wiki/testing/2026-03-25-testing-approach-kate.md): Kate Rundell meeting doc — 5 workstreams, testing methodology, year-ahead plan
  - slug: testing-approach-kate | status: FINAL | doc-type: strategy | audience: amazon-internal | level: 2
  - children: workstream-oci-bidding, workstream-modern-search, workstream-audiences-lifecycle, workstream-user-experience, workstream-algorithmic-ads

- [WS1: OCI Bidding](~/shared/wiki/testing/2026-03-25-workstream-oci-bidding.md): OCI bidding deep-dive — problem, test, result, scale
  - slug: workstream-oci-bidding | status: FINAL | doc-type: strategy | audience: amazon-internal | level: 2
  - parent: testing-approach-kate

- [WS2: Modern Search](~/shared/wiki/testing/2026-03-25-workstream-modern-search.md): Redirects, AEO — problem, test, result, scale
  - slug: workstream-modern-search | status: FINAL | doc-type: strategy | audience: amazon-internal | level: 2
  - parent: testing-approach-kate

- [WS3: Audiences & Lifecycle](~/shared/wiki/testing/2026-03-25-workstream-audiences-lifecycle.md): F90, engagement — problem, test, result, scale
  - slug: workstream-audiences-lifecycle | status: FINAL | doc-type: strategy | audience: amazon-internal | level: 2
  - parent: testing-approach-kate

- [WS4: User Experience](~/shared/wiki/testing/2026-03-25-workstream-user-experience.md): Landing pages, Polaris — problem, test, result, scale
  - slug: workstream-user-experience | status: FINAL | doc-type: strategy | audience: amazon-internal | level: 2
  - parent: testing-approach-kate

- [WS5: Algorithmic Ads](~/shared/wiki/testing/2026-03-25-workstream-algorithmic-ads.md): AI Max, Shopping — problem, test, result, scale
  - slug: workstream-algorithmic-ads | status: FINAL | doc-type: strategy | audience: amazon-internal | level: 2
  - parent: testing-approach-kate

- [AI Max Test Design — US](~/shared/wiki/testing/2026-03-25-ai-max-test-design.md): AI Max test design for US market
  - slug: ai-max-test-design | status: DRAFT | doc-type: strategy | audience: amazon-internal | level: 2

- [OCI Rollout Playbook](~/shared/wiki/testing/2026-03-25-oci-rollout-playbook.md): Phased OCI rollout methodology (E2E → 25% → 50% → 100%), validated results (35K regs, $16.7MM OPS), measurement framework, cross-market patterns, decision guide
  - slug: oci-rollout-playbook | status: FINAL | doc-type: strategy | audience: amazon-internal | level: 2

- [Ad Copy Testing Framework](~/shared/wiki/testing/2026-03-25-ad-copy-testing-framework.md): SP study framework for ad copy testing
  - slug: ad-copy-testing-framework | status: DRAFT | doc-type: strategy | audience: amazon-internal | level: 2

- [Email Overlay WW Rollout](~/shared/wiki/testing/2026-03-25-email-overlay-ww-rollout.md): WW rollout plan for email overlay
  - slug: email-overlay-ww-rollout | status: DRAFT | doc-type: strategy | audience: amazon-internal | level: 2

- [AU NB Testing — MRO/Trades](~/shared/wiki/testing/2026-03-25-au-nb-mro-trades-proposal.md): AU non-brand testing proposal for MRO/Trades vertical
  - slug: au-nb-mro-trades-proposal | status: DRAFT | doc-type: strategy | audience: amazon-internal | level: 2

- [Project Baloo — Shopping Ads for AB](~/shared/wiki/testing/2026-04-04-project-baloo-overview.md): Overview of Shopping Ads for AB, early access status, cost framework, and test design
  - slug: project-baloo-overview | status: DRAFT | doc-type: strategy | audience: amazon-internal | level: 2

- [Enhanced Match / LiveRamp — Audience Expansion](~/shared/wiki/testing/2026-04-04-enhanced-match-liveramp.md): LiveRamp Enhanced Match investigation, Brandon's 4 questions, EU DMA blocker, audience size drop
  - slug: enhanced-match-liveramp | status: FINAL | doc-type: strategy | audience: amazon-internal | level: 2

### Strategy & Frameworks (14)

- [Agent System Architecture](~/shared/wiki/strategy/2026-03-25-agent-architecture.md): Complete architecture guide — body system (11 organs), hooks (5 triggers), agent swarm (13 agents across 3 teams), dual-file definition pattern (.md portable + .json CLI), failure modes, portability, cold start protocol
  - slug: agent-architecture | status: DRAFT | doc-type: strategy | audience: team | level: 5 | tags: body-system, agent, hook, steering, tool, mcp, agent-bridge
  - depends_on: body-system-architecture
  - Asana project: ABPS AI - Build

- [Agentic Paid Search — Vision & Roadmap](~/shared/wiki/strategy/2026-03-25-agentic-ps-vision.md): Vision and roadmap for agentic PS
  - slug: agentic-ps-vision | status: DRAFT | audience: amazon-internal | level: 5

- [The Body System — Architecture](~/shared/wiki/strategy/2026-03-25-body-system-architecture.md): Architecture for personal AI operating systems
  - slug: body-system-architecture | status: DRAFT | audience: personal | level: 5

- [Agentic Marketing — Industry Landscape](~/shared/wiki/strategy/2026-03-25-agentic-marketing-landscape.md): Industry landscape and Amazon context for agentic marketing
  - slug: agentic-marketing-landscape | status: DRAFT | audience: personal | level: 4-5

- [AEO / AI Overviews POV](~/shared/wiki/strategy/2026-03-25-aeo-ai-overviews-pov.md): AB Paid Search POV on AI Overviews and AEO
  - slug: aeo-ai-overviews-pov | status: DRAFT | audience: amazon-internal | level: 4

- [Competitive Landscape](~/shared/wiki/strategy/2026-03-25-competitive-landscape.md): Full competitive picture across 10 markets — who competes, trajectory, CPC impact, response strategy
  - slug: competitive-landscape | status: DRAFT | doc-type: strategy | audience: amazon-internal | level: 2

- [Cross-Market Playbook](~/shared/wiki/strategy/2026-03-25-cross-market-playbook.md): US → EU5 → RoW scaling playbook
  - slug: cross-market-playbook | status: DRAFT | audience: amazon-internal | level: 2

- [F90 Lifecycle Strategy](~/shared/wiki/strategy/2026-03-25-f90-lifecycle-strategy.md): F90 lifecycle program strategy
  - slug: f90-lifecycle-strategy | status: DRAFT | audience: amazon-internal | level: 2

- [ie%CCP Planning & Optimization Framework](~/shared/wiki/strategy/2026-03-30-ieccp-planning-framework.md): How to understand, plan around, and optimize ie%CCP for budget decisions and performance analysis
  - slug: ieccp-planning-framework | status: FINAL | audience: amazon-internal | level: 2

- [Q2 2026 Initiative Status & Priorities](~/shared/wiki/strategy/2026-04-04-q2-initiative-status.md): Single-page scorecard of every active initiative entering Q2 — status, blockers, priorities
  - slug: q2-initiative-status | status: DRAFT | audience: amazon-internal | level: 2

- [OCI Impact Summary — The Business Case](~/shared/wiki/strategy/2026-04-04-oci-business-case.md): Leadership-ready summary of OCI's total business impact for Kate/Todd conversations
  - slug: oci-business-case | status: DRAFT | doc-type: strategy | audience: amazon-internal | level: 2

- [GenAI Search Traffic — What We Know](~/shared/wiki/strategy/2026-04-04-genai-search-traffic.md): GenAI engines driving ~1% of WW traffic, ACE team building Amazon MCP shopping widget, implications for PS
  - slug: genai-search-traffic | status: DRAFT | doc-type: strategy | audience: amazon-internal | level: 4

- [PS Five-Year Outlook: 2026–2030](~/shared/wiki/strategy/2026-04-05-ps-five-year-outlook.md): Five-year strategic outlook — four 2026 investment bets (AI Max, Baloo, F90, agentic tooling) grounded in OCI results, 2027 conditional on test outcomes, 2028-2030 scenario planning. Decision table with go/no-go gates and fallbacks.
  - slug: ps-five-year-outlook | status: FINAL | doc-type: strategy | audience: leadership | level: 5
  - depends_on: testing-approach-kate, agentic-ps-vision, aeo-ai-overviews-pov

### Paid Search Operations / Program Details (8)

- [AB Paid Search Program Wiki](~/shared/wiki/markets/2026-03-25-ab-paid-search-wiki.md): Master program wiki for AB Paid Search
  - slug: ab-paid-search-wiki | status: DRAFT | doc-type: reference | audience: amazon-internal | level: N/A

- [AU Paid Search — Market Wiki](~/shared/wiki/markets/2026-04-04-au-market-wiki.md): Canonical AU reference — performance, initiatives, stakeholders, open questions
  - slug: au-market-wiki | status: FINAL | doc-type: reference | audience: amazon-internal | level: N/A | tags: market-wiki, au
  - replaces: au-market-wiki (old), au-market-overview, au-paid-search-market-overview

- [MX Paid Search — Market Wiki](~/shared/wiki/markets/2026-03-25-mx-market-wiki.md): Canonical MX reference — includes Lorena onboarding context (formerly separate handoff guide)
  - slug: mx-market-wiki | status: DRAFT | doc-type: reference | audience: amazon-internal | level: N/A | tags: market-wiki, mx
  - replaces: mx-market-wiki (old), mx-ps-handoff-guide

- [OCI Execution Guide](~/shared/wiki/markets/2026-04-04-oci-execution-guide.md): Step-by-step OCI implementation — prerequisites, E2E launch, scaling, troubleshooting
  - slug: oci-execution-guide | status: FINAL | doc-type: execution | audience: amazon-internal | level: N/A
  - replaces: oci-implementation-guide, oci-methodology-knowledge-share

- [WW Testing Tracker](~/shared/wiki/markets/2026-03-25-ww-testing-tracker.md): All active, planned, and completed tests across markets with portfolio health narrative
  - slug: ww-testing-tracker | status: DRAFT | doc-type: reference | audience: amazon-internal | level: 2

- [Team Capacity & Workload Distribution](~/shared/wiki/markets/2026-04-04-team-workload-distribution.md): Who is doing what across 10 markets — coverage gaps, overload risks, delegation opportunities
  - slug: team-workload-distribution | status: DRAFT | doc-type: reference | audience: amazon-internal | level: N/A | tags: team, capacity, brandon

- [Polaris WW Rollout — Status & Decision Log](~/shared/wiki/markets/2026-04-04-polaris-rollout-status.md): Single source of truth for Polaris Brand LP rollout across all markets
  - slug: polaris-rollout-status | status: DRAFT | doc-type: reference | audience: amazon-internal | level: 2 | tags: polaris, rollout, ww
  - replaces: polaris-rollout-timeline

- [Market Reference](~/shared/wiki/markets/2026-03-25-market-reference.md): All 10 markets in one read — performance, OCI status, contacts, competitors
  - slug: market-reference | status: DRAFT | doc-type: reference | audience: amazon-internal | level: 2

### Reporting (2)

- [AU Keyword CPA Dashboard](~/shared/wiki/reporting/2026-03-25-au-keyword-cpa-dashboard.md): AU keyword CPA dashboard design
  - slug: au-keyword-cpa-dashboard | status: DRAFT | audience: amazon-internal | level: 1

- [WBR Callout Template & Guide](~/shared/wiki/reporting/2026-03-25-wbr-callout-guide.md): WBR callout template and guide
  - slug: wbr-callout-guide | status: DRAFT | audience: amazon-internal | level: 1

### Tools & Automation (2)

- [Campaign Link Generator Spec](~/shared/wiki/operations/2026-03-25-campaign-link-generator-spec.md): Tool spec for campaign link generator
  - slug: campaign-link-generator-spec | status: DRAFT | audience: amazon-internal | level: 3

- [Budget Forecast Helper Spec](~/shared/wiki/operations/2026-03-25-budget-forecast-helper-spec.md): Tool spec for budget forecast helper
  - slug: budget-forecast-helper-spec | status: DRAFT | audience: amazon-internal | level: 3

### Communication (1)

- [Stakeholder Communication Guide](~/shared/wiki/operations/2026-03-25-stakeholder-comms-guide.md): How to talk to each audience — templates, tiers, proactive triggers
  - slug: stakeholder-comms-guide | status: DRAFT | doc-type: execution | audience: personal | level: 1

_Archived: Polaris Rollout Timeline (superseded by polaris-rollout-status), MX PS Handoff Guide (merged into mx-market-wiki), OCI Methodology Knowledge Share (merged into oci-execution-guide)_

### Best Practices (3)

- [Google Ads Campaign Structure Standards](~/shared/wiki/operations/2026-03-25-google-ads-campaign-structure.md): Campaign structure standards for AB PS
  - slug: google-ads-campaign-structure | status: DRAFT | audience: amazon-internal | level: N/A

- [Landing Page Testing Playbook](~/shared/wiki/operations/2026-03-25-landing-page-testing-playbook.md): LP testing playbook
  - slug: landing-page-testing-playbook | status: DRAFT | audience: amazon-internal | level: N/A

- [Invoice & PO Process Guide](~/shared/wiki/operations/2026-03-25-invoice-po-process-guide.md): Invoice and PO process guide for AB PS
  - slug: invoice-po-process-guide | status: DRAFT | audience: amazon-internal | level: N/A

### System Documentation (0)

_No system documentation articles published yet. System docs currently live in body organs and steering files._

---

## Summary

| Category | Count | Artifact Folder |
|----------|-------|-----------------|
| Testing & Experimentation | 13 | `testing/` |
| Strategy & Frameworks | 13 | `strategy/` |
| Program Details / PS Ops | 8 | `program-details/` |
| Reporting | 2 | `reporting/` |
| Tools & Automation | 2 | `tools/` |
| Communication | 1 | `communication/` |
| Best Practices | 3 | `best-practices/` |
| System Documentation | 0 | _(none yet)_ |
| **Total** | **42** | |

Status: 30 DRAFT | 0 REVIEW | 11 FINAL
Audience: 33 amazon-internal | 2 personal | 0 agent-only

Doc-type breakdown: ~18 strategy | ~10 execution | ~10 reference

---

## Categories

- [Testing & Experimentation](#testing--experimentation-11): Test designs, methodologies, experiment frameworks
- [Strategy & Frameworks](#strategy--frameworks-6): POVs, playbooks, strategic narratives
- [Paid Search Operations / Program Details](#paid-search-operations--program-details-6): Day-to-day PS docs, market wikis, account details
- [Reporting](#reporting-3): Dashboards, analysis docs, performance summaries
- [Tools & Automation](#tools--automation-2): Tool specs, automation docs
- [Communication](#communication-3): Stakeholder docs, handoff guides
- [Best Practices](#best-practices-3): Operational standards, how-tos
- [System Documentation](#system-documentation-0): Body system, agent architecture, hooks

## Dependency Graph

```
testing-approach-kate (PARENT)
  ├── workstream-oci-bidding ──────→ oci-rollout-playbook (strategy), oci-execution-guide (execution)
  ├── workstream-modern-search ───→ aeo-ai-overviews-pov, email-overlay-ww-rollout
  ├── workstream-audiences ───────→ f90-lifecycle-strategy
  ├── workstream-user-experience ─→ polaris-rollout-status, landing-page-testing-playbook, au-market-wiki
  └── workstream-algorithmic-ads ─→ ai-max-test-design, project-baloo-overview

oci-rollout-playbook (STRATEGY) ←→ oci-execution-guide (EXECUTION)
  └── oci-business-case (LEADERSHIP SUMMARY)

agentic-ps-vision (STANDALONE)
  └── body-system-architecture, agentic-marketing-landscape

cross-market-playbook (STANDALONE)
  └── references all workstream docs + market wikis

ww-testing-tracker (STANDALONE)
  └── references all testing/ docs

q2-initiative-status (STANDALONE)
  └── references all active initiatives
```

## Distribution Model

Local wiki (`~/shared/wiki/`) is the working branch. SharePoint is production.

- **DRAFT** → article exists locally, still being written or revised
- **REVIEW** → article is ready for Richard to review for SharePoint publish
- **FINAL** → article has been human-approved and published to SharePoint

Publishing to SharePoint is a deliberate, human-approved action — like a git push to main. The agent pipeline (editor → researcher → writer → critic → librarian) produces DRAFT and can promote to REVIEW. Only Richard promotes to FINAL and triggers the SharePoint publish.

Distribution endpoints (MCP servers installed, target sites TBD):
- `amazon-sharepoint-mcp` — SharePoint. Primary target for amazon-internal audience articles.
- `xwiki-mcp` — XWiki. Optional alternative endpoint. May be preferred depending on team adoption and tooling.

Target site and library for each endpoint will be configured when the first article is ready to publish.

Publishing workflow (future — Level 3):
1. Librarian marks article as REVIEW when quality checks pass
2. Richard reviews the article and approves
3. Agent publishes to SharePoint via MCP, updates status to FINAL
4. Local copy remains source of truth; SharePoint is the read-only distribution copy

Until the target site is configured, all articles remain local. No auto-publish, ever.

---

## Update Log

| Date | Article | Change |
|------|---------|--------|
| 2026-04-05 | agent-architecture | Published revision (v2). Updated: consolidated WBR agents (6→2 parameterized), added Agent Definition Pattern section (.md/.json dual-file), added Failure Modes, updated routing/portability/directory. Eval A R2: 8.6/10 PUBLISH, Eval B R2: 8.2/10 with post-review fixes. Added to wiki-index (was previously unindexed). Asana: ABPS AI - Build. |
| 2026-04-05 | workstream-oci-bidding | Published as FINAL (v2). Critic Eval A: 8.6/10 — PUBLISH direct. Status DRAFT → FINAL. Replaced artifact in testing/. |
| 2026-04-05 | workstream-modern-search | Published as FINAL (v2). Critic Eval A: 8.6/10 — PUBLISH direct. Status DRAFT → FINAL. Replaced artifact in testing/. |
| 2026-04-05 | workstream-audiences-lifecycle | Published as FINAL (v3). Critic Eval A: 8.4/10 → revised per Economy feedback (cross-WS duplication, trimmed learning section). Status DRAFT → FINAL. Replaced artifact in testing/. |
| 2026-04-05 | workstream-user-experience | Published as FINAL (v3). Critic Eval A: 8.0/10 → revised per Economy feedback (split Baloo paragraph, cut summary sentence, reframed baseline). Status DRAFT → FINAL. Replaced artifact in testing/. |
| 2026-04-05 | workstream-algorithmic-ads | Published as FINAL (v3). Critic Eval A: 7.8/10 → revised per Accuracy+Economy feedback (trimmed Prime Day duplication, flagged AI Max status, cut Discovery Ads history, merged DG expansion). Status DRAFT → FINAL. Replaced artifact in testing/. |
| 2026-04-05 | testing-approach-kate | Published as FINAL (v5 rewrite). Critic Eval A: 8.4/10, Eval B: 8.2/10. Status DRAFT → FINAL. Frontmatter normalized (audience→amazon-internal, added level/update-trigger). Replaced artifact in testing/. |
| 2026-04-04 | oci-rollout-playbook | Published as FINAL (v2 rewrite). Critic Eval A: 8.4/10. Status DRAFT → FINAL. Replaced artifact in testing/. |
| 2026-04-04 | (wiki-wide) | Introduced doc-type system (strategy/execution/reference). Consolidated 3 OCI docs into 2 (Playbook + Execution Guide). Merged AU Market Wiki + AU Market Overview into one canonical doc. Merged MX Handoff Guide into MX Market Wiki. Archived Polaris Timeline (superseded by Polaris Rollout Status). Added narrative to WW Testing Tracker. Total: 42 → 38 articles (4 archived via consolidation). |
| 2026-04-04 | oci-execution-guide | New article — merged OCI Implementation Guide + OCI Methodology Knowledge Share |
| 2026-04-04 | au-market-wiki | Rewritten — merged AU Market Wiki + AU Market Overview into one canonical doc |
| 2026-04-04 | mx-market-wiki | Updated — merged MX PS Handoff Guide content into market wiki |
| 2026-04-04 | ww-testing-tracker | Rewritten — added portfolio health narrative, blocker analysis, pipeline by workstream |
| 2026-04-04 | q2-initiative-status | New article — Q2 initiative scorecard for Brandon's team management |
| 2026-04-04 | oci-business-case | New article — Leadership-ready OCI impact summary for Kate/Todd |
| 2026-04-04 | team-workload-distribution | New article — Team capacity analysis, coverage gaps, delegation opportunities |
| 2026-04-04 | polaris-rollout-status | New article — Polaris WW rollout single source of truth (replaces polaris-rollout-timeline) |
| 2026-04-04 | project-baloo-overview | New article — Shopping Ads for AB overview, early access, test design |
| 2026-04-04 | f90-lifecycle-strategy | Expanded from ~500 to ~1500 words |
| 2026-04-04 | ad-copy-testing-framework | Expanded from ~600 to ~1500 words |
| 2026-04-04 | email-overlay-ww-rollout | Expanded from ~600 to ~1500 words |
| 2026-04-04 | ai-max-test-design | Expanded from ~600 to ~1500 words |
| 2026-04-04 | campaign-link-generator-spec | Expanded from ~500 to ~1200 words |
| 2026-04-04 | budget-forecast-helper-spec | Expanded from ~400 to ~1200 words |
| 2026-04-03 | au-paid-search-market-overview | New article (now archived — merged into au-market-wiki) |
| 2026-03-25 | (all 34 artifacts) | Initial catalog — existing artifacts indexed into wiki system |
