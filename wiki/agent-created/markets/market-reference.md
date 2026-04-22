---
title: "Artifact metadata"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0320 | duck_id: program-market-reference -->

---
title: "Market Reference: AB Paid Search Across 10 Markets"
slug: "market-reference"
type: "reference"
audience: "team"
status: "draft"
doc-type: reference
created: "2026-03-25"
updated: "2026-03-25"
owner: "Richard Williams"
tags: ["paid-search", "us", "ca", "jp", "uk", "de", "fr", "it", "es", "au", "mx", "ww", "oci", "cpa"]
depends_on: ["competitive-landscape", "oci-playbook"]
consumed_by: ["wiki-concierge", "abix-analyst", "najp-analyst", "eu5-analyst", "abix-callout-writer", "najp-callout-writer", "eu5-callout-writer", "callout-reviewer"]
summary: "Unified reference for all 10 AB Paid Search markets — performance, OCI status, contacts, competitors, and active initiatives in one read."
# Artifact metadata
artifact-status: DRAFT
artifact-audience: amazon-internal
artifact-level: 2
update-trigger: "Monthly after MBR data refresh, or when a market's OCI status changes"
---

# Market Reference: AB Paid Search Across 10 Markets

This doc answers "tell me everything about AB Paid Search in [market]" in one read. Any agent writing a callout, any stakeholder asking about a market, or any teammate picking up coverage should find what they need here without loading 3-4 separate files.

## Context

AB Paid Search operates across 10 markets under a single team (Brandon Munday's WW Outbound Marketing). Richard Williams owns AU and MX hands-on; the full team covers US, CA, JP, UK, DE, FR, IT, ES. Market context is currently scattered across `eyes.md` (market health), `callouts/{market}/` (weekly data), `org-chart.md` (contacts), and `current.md` (active projects). This doc consolidates it.

## Current Performance

For current weekly data, see the latest WW summary at `~/shared/context/active/callouts/ww/`. For monthly data, see [Eyes — Market Health](~/shared/context/body/eyes.md).

**Structural trends (updated monthly):**
- NB CPA compression via OCI is the dominant story: US -47% YoY, MX -50%, CA -46%
- Eight of ten markets beat OP2 on March projections
- JP is the only market tracking below OP2 — structural MHLW gap compounded by fiscal year-end

---

## Market Profiles

### US — Flagship Market

| Field | Value |
|-------|-------|
| Launch | Pre-2023 (mature) |
| FY26 Feb | 32.9K regs, +16% vs OP2, +68% YoY, $2.7M spend, $83 CPA |
| OCI | ✅ Live since Sep 2025 (100% NB). +24% reg lift, $16.7MM OPS. |
| Key competitor | Walmart Business (37-55% IS on Brand, driving CPA from ~$40 to $65-77) |
| Key contact | Stacey Gu (OCI/Bidding), Andrew Wirtz (DG/Algo Ads) |
| Active initiatives | Polaris Brand LP switch (completed 3/24), Weblab dial-up Apr 6-7, AI Max test design (due 3/28), F90 Lifecycle program |
| Narrative | OCI-powered growth. Jan was peak (39K regs, +86% YoY). Feb normalizing but well above plan. Brand CPA pressure from Walmart absorbed by NB efficiency. Response: bid caps on Brand, NB efficiency via OCI. |

### CA — LP Optimization + OCI Wave 2

| Field | Value |
|-------|-------|
| Launch | Pre-2023 (mature) |
| FY26 Feb | 2.8K regs, +18.5% vs OP2, +32.3% YoY, $207K spend, $73 CPA |
| OCI | 🔄 E2E launched 3/4/2026. Full impact projected Jul 2026. |
| Key competitor | Shopify.com (<10% Brand Core, +13% CPC when present) |
| Key contact | Team-wide — Stacey Gu (OCI/Bidding) handles CA OCI rollout |
| Active initiatives | OCI E2E testing, LP optimization (Bulk CVR +187%, Wholesale +180%) |
| Narrative | LP optimization producing strong results. OCI will compound these gains. Shopify is a recurring but not persistent competitor. |

### UK — Efficiency Gains Despite Spend Reduction

| Field | Value |
|-------|-------|
| Launch | Pre-2023 (mature) |
| FY26 Feb | ~5K est regs, +24% vs OP2, -6% spend vs OP2 |
| OCI | ✅ Live since Sep 2025 (100%). +23% reg lift. |
| Key competitor | weareuncapped.com (24% Brand IS since Dec 2023, +45% CPC), Temu (13% Generic NB) |
| Key contact | Andrew Wirtz (EU lead) |
| Active initiatives | Ad copy test Phase 1 complete (+86% CTR, +31% regs), Phase 2 rollout, AGL internal bidding flagged |
| Narrative | Surpassed OP2 by 24% despite spending 6% less. Ad copy test is the standout win — evidence-based messaging from SP study drove +70% CTR improvement (pre/post). weareuncapped.com is the most persistent EU competitor. |

### DE — Slight Miss, High Baseline

| Field | Value |
|-------|-------|
| Launch | Pre-2023 (mature) |
| FY26 Feb | ~4K est regs, -4% vs OP2 |
| OCI | ✅ Live since Dec 2025 (100%). +18% reg lift. |
| Key competitor | recht24-7.de (14% Brand Core, reported for store closure) |
| Key contact | Andrew Wirtz (EU lead) |
| Active initiatives | OCI lift tracking (W49-W51: +16-20% lift), ad copy translations completed |
| Narrative | Missed OP2 by 4% — NB -22% vs OP2. But Y25 was unusually strong, making the baseline hard to beat. OCI lift tracking shows consistent 16-20% improvement. DE has the cleanest test-vs-control OCI data (W44-W45). |

### FR — NB Competitive Pressure

| Field | Value |
|-------|-------|
| Launch | Pre-2023 (mature) |
| FY26 W12 | 1.2K regs, -3% WoW, $52 CPA, +14% YoY |
| OCI | 🔄 E2E launched 2/26/2026. Full impact Jul 2026. |
| Key competitor | bruneau.fr (39-47% Generic NB IS — highest NB IS of any competitor globally), mirakl.com (10% Brand Core) |
| Key contact | Andrew Wirtz (EU lead) |
| Active initiatives | OCI E2E, ad copy translations completed (GlobalLink, delivered 2/18) |
| Narrative | bruneau.fr's 39-47% NB IS is the biggest NB competitive pressure in any market. OCI will help NB efficiency but won't solve the impression share problem. FR is tracking +5% vs OP2 on March projections despite this headwind. |

### IT — CPC Inflation Challenge

| Field | Value |
|-------|-------|
| Launch | Pre-2023 (mature) |
| FY26 W12 | 1.3K regs, -12% WoW, $61 CPA, +4% YoY |
| OCI | 🔄 E2E launched 2/26/2026. Full impact Jul 2026. |
| Key competitor | Shopify/mondoffice (>10% Generic NB, -20% CVR), revolut.com (-36% CVR drop on Brand Core W10) |
| Key contact | Andrew Wirtz (EU lead) |
| Active initiatives | OCI E2E, ad copy test early stage (low volume), ad copy translations completed |
| Narrative | Brand Core CPC +131% YoY — highest in EU5. Driven by limited ad opportunities, not a single dominant competitor. revolut.com's appearance in W9-10 caused a sharp CVR drop. IT ad copy test has insufficient volume for conclusions. |

### ES — Smallest EU Market, Strong Growth

| Field | Value |
|-------|-------|
| Launch | Pre-2023 (mature) |
| FY26 W12 | 657 regs, -8% WoW, $50 CPA, +20% YoY |
| OCI | 🔄 E2E launched 2/26/2026. Full impact Jul 2026. |
| Key competitor | amazon.co.uk/AGL (<10%, +41% CPC 2/13-3/4 — internal Amazon entity) |
| Key contact | Andrew Wirtz (EU lead) |
| Active initiatives | OCI E2E, ad copy translations completed |
| Narrative | Tracking +19% vs OP2 on March projections. AGL bidding on ES Brand terms is an internal coordination issue, not a competitive one. Smallest EU market but efficient. |

### JP — MHLW Headwind + Yahoo Competition

| Field | Value |
|-------|-------|
| Launch | Pre-2023 (mature) |
| FY26 Feb | 1.6K regs, -47.5% vs OP2 |
| OCI | 🔄 E2E launched 2/26/2026. Full impact Jul 2026. |
| Key competitor | axalpha.com (10% Brand Core Google), shop-pro.jp (12-15% Yahoo Brand Core), Rakuten + moneyforward (Yahoo persistent) |
| Key contact | York Chen (back from paternity leave 3/22) |
| Active initiatives | OCI E2E, pre-post analysis framework proposed (success threshold: 45% CP improvement, rollback at 35%) |
| Narrative | The only market tracking below OP2 (-14% on March projections). MHLW campaign ended 1/31 — was a major registration driver. Competition intensifying specifically on Yahoo with multiple new entrants. OCI needs to offset the structural MHLW gap. Fiscal year-end (March) adds seasonal suppression. |

### AU — Richard's Market, Efficiency Focus

> Full detail: [AU Market Wiki](au-market-wiki.md)

| Field | Value |
|-------|-------|
| Launch | June 2025 (W24) — youngest market |
| OCI | ❌ Not in scope. No timeline. |
| Key contacts | Alexis Eck (L6, AU POC), Lena Zak (L7, Country Leader) |
| Key challenge | B2B CPC ($6 avg) vs consumer ($0.18-0.50). No Shopping Ads for AB. Lena expects data, not narratives. |

### MX — Richard's Market, ie%CCP Constrained

> Full detail: [MX Market Wiki](mx-market-wiki.md)

| Field | Value |
|-------|-------|
| Launch | March 2025 (W11) |
| OCI | ❌ Not in scope. No timeline. |
| Key contacts | Lorena Alvarez Larrea (L5, primary PS stakeholder since 3/17) |
| Key challenge | ie%CCP is the dominant budget constraint — 100% target limits NB spend. Strong growth (+68% vs OP2) but budget-capped. |

## Cross-Market Patterns

For cross-market scaling methodology, see [Cross-Market Playbook](../strategy/cross-market-playbook.md). For competitive patterns, see [Competitive Landscape](competitive-landscape).

## Decision Guide

| Situation | Action | Why |
|-----------|--------|-----|
| Need full context on a market for a callout | Read this doc's market profile + `callouts/{market}/{market}-data-brief-*.md` for latest weekly data | Profile gives structure, data brief gives current numbers |
| Stakeholder asks "how's [market] doing?" | Lead with vs OP2 and YoY, then the narrative thread | OP2 is the plan. YoY is the trend. Narrative is the "so what." |
| Market misses OP2 for 2+ consecutive months | Check: is it structural (MHLW, ie%CCP) or cyclical (seasonal, promo transition)? | Structural needs a strategy change. Cyclical needs patience. |
| New market launches PS | Use AU/MX as templates — youngest markets with documented ramp-up patterns | AU launched Jun 2025, MX launched Mar 2025. Both have context files. |

## Related

- [Eyes — Market Health](~/shared/context/body/eyes.md) — live market metrics updated each loop run
- [Competitive Landscape](competitive-landscape) — per-market competitor details
- [OCI Playbook](oci-playbook) — rollout methodology and measurement framework
- [Org Chart — International Expansion](~/shared/context/active/org-chart.md) — market-side contacts and reporting lines
- Per-market callout data: `~/shared/context/active/callouts/{market}/`

## Sources
- W12 2026 performance data — source: `shared/context/active/callouts/ww/ww-summary-2026-w12.md`
- Feb 2026 market health — source: `shared/context/body/eyes.md`, Market Health table, updated 2026-03-25
- AU market context — source: `shared/context/active/callouts/au/au-context.md`, updated 2026-03-16
- MX market context — source: `shared/context/active/callouts/mx/mx-context.md`, updated 2026-03-16
- OCI rollout status — source: `shared/context/body/eyes.md`, OCI Performance section
- Market contacts — source: `shared/context/active/org-chart.md`, International Expansion section
- Active projects per market — source: `shared/context/active/current.md`, updated 2026-03-24

<!-- AGENT_CONTEXT
machine_summary: "Structural reference for all 10 AB Paid Search markets — OCI status, key contacts, competitive context, active initiatives, and narrative thread per market. For current weekly/monthly performance data, see eyes.md or callouts/ww/. AU and MX have dedicated market wikis with deeper detail. US is flagship (OCI live, Walmart competition). JP is the only market below OP2 (MHLW structural gap)."
key_entities: ["US", "CA", "UK", "DE", "FR", "IT", "ES", "JP", "AU", "MX", "OCI", "OP2", "CPA", "NB", "Brand", "Walmart", "Lena Zak", "Alexis Eck", "Lorena Alvarez Larrea", "Andrew Wirtz"]
action_verbs: ["reference", "compare", "monitor", "callout", "assess"]
update_triggers: ["MBR data refresh (monthly)", "OCI market status change", "new market launches PS", "market contact changes"]
-->
