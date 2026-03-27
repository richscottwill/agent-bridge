---
title: "Competitive Landscape: Who's Bidding Against Amazon Business"
slug: "competitive-landscape"
type: "reference"
audience: "org"
status: "draft"
created: "2026-03-25"
updated: "2026-03-25"
owner: "Richard Williams"
tags: ["paid-search", "brand", "non-brand", "cpc", "competitive-intel", "ww"]
depends_on: []
replaces: "competitive-intel-tracker"
consumed_by: ["wiki-concierge", "abix-analyst", "najp-analyst", "eu5-analyst", "abix-callout-writer", "najp-callout-writer", "eu5-callout-writer", "callout-reviewer"]
summary: "Full competitive picture across 10 AB Paid Search markets — who competes, their trajectory, CPC impact, and our response strategy."
# Artifact metadata
artifact-status: DRAFT
artifact-audience: amazon-internal
artifact-level: 2
update-trigger: "Monthly after MBR data refresh, or when a new competitor appears with >10% IS in any market"
---

# Competitive Landscape: Who's Bidding Against Amazon Business

This doc gives you the full competitive picture for AB Paid Search across all 10 markets. After reading it, you should be able to answer: who competes with us, how aggressive they are, what it costs us, and what we're doing about it — without asking follow-up questions.

## Context

> This doc replaces the Competitive Intelligence Tracker (previously in `reporting/`). All competitive data now lives here.

Competitive pressure on AB Paid Search has intensified since mid-2024. In 2023, most markets had 1-2 competitors. By 2026, most have 3-5. The team's strategic response is efficiency over escalation — we absorb Brand CPC increases through NB efficiency gains (primarily OCI), rather than escalating bid wars we can't win. This doc consolidates intelligence currently scattered across `eyes.md`, `research/competitor-intel.md`, and weekly callout analysis briefs into a single canonical reference.

## The Strategic Position

AB Paid Search faces a broadening competitive field, but the threat profile varies by market. The US has one dominant, sustained competitor (Walmart Business). EU markets have fragmented competition — different players in each market, none with Walmart's persistence. International markets (JP, MX, CA) have emerging but manageable threats.

Our defense is structural, not reactive:
1. OCI-powered NB efficiency absorbs Brand CPA increases at the program level
2. Bid caps on Brand prevent auction escalation
3. Ad copy optimization (evidence-based messaging from SP study) improves conversion without increasing spend
4. Campaign consolidation strengthens data signals for algorithmic bidding

This approach works because we measure holistically — total program CPA, not Brand vs NB in isolation. A $77 Brand CPA is acceptable when NB CPA has dropped 50% via OCI.

## US: Walmart Business — The Only Sustained Threat

Walmart Business is the only competitor with sustained, aggressive Brand bidding in any market. Every other competitor globally comes and goes. Walmart stays.

| Metric | Value |
|--------|-------|
| First appeared | Jul 2024 on Brand Core terms |
| IS trajectory | 25% (Jul-Sep 2024) → 35% (Oct-Nov 2024) → 37-55% (Jan-Mar 2026) |
| Peak IS | 55% in W6 2026 |
| Brand CPA impact | ~$40 avg → $65-$77 range |
| CPC impact | Brand Core CPC from ~$1.6 pre-Walmart to $2.5-$3.5 |
| Pattern | Pulls back during holidays (Thanksgiving, Christmas), ramps Jan-Mar |

**So what:** Walmart has deeper pockets for Brand terms. Escalating bids is a losing game. The team maintains IS through bid caps and offsets Brand CPA increases through NB efficiency gains via OCI. At the program level, total CPA remains healthy because NB CPA dropped ~50% with OCI. This is Decision D2 in action — efficiency over escalation.

**Confidence:** HIGH. Multiple MBR sources confirm trajectory and impact.

## EU5: Fragmented Competition by Market

EU competition is the hardest to manage because it's different in every market. No unified response works — each market requires its own monitoring and response.

| Market | Primary Competitor | IS | CPC Impact | Since | Notes |
|--------|-------------------|-----|------------|-------|-------|
| UK | weareuncapped.com | 24% Brand | +45% Brand Core CPC | Dec 2023 | Most persistent EU competitor. IS validated W10 2026. |
| UK | Temu | 13% Generic NB | +14% NB CPC | W10 2024 | NB pressure. IS validated W10 2026. |
| UK | Amazon Global Logistics UK | <10% ES Brand | +41% CPC (W8-W10 2026) | W8 2026 | Internal Amazon entity bidding on AB terms. IS validated W10 2026. |
| DE | recht24-7.de | 14% Brand Core | +3% MoM CPC | Jul 2025 | Reported for store closure — may be an Amazon Associate. IS validated W10 2026. |
| FR | bruneau.fr | 39-47% Generic NB | Significant NB pressure | W38 2025 | Highest NB IS of any EU competitor. IS validated W10 2026. |
| FR | mirakl.com | 10% Brand Core | -5% clicks, -14% CVR | W5 2026 | Marketplace platform. IS validated W10 2026. |
| IT | Shopify (mondoffice) | >10% Generic NB | -20% CVR on Generic | W43 2025 | E-commerce platform. IS validated W10 2026. |
| IT | revolut.com | <10% | -36% CVR drop on Brand Core (W10) | W9 2026 | Fintech — unusual entrant. IS validated W10 2026. |
| ES | amazon.co.uk (AGL) | <10% | +41% CPC (2/13-3/4) | W8 2026 | Internal Amazon entity. IS validated W10 2026. |

**So what:** Three patterns matter here. First, weareuncapped.com in UK is the only EU competitor approaching Walmart-level persistence (24% IS since Dec 2023). Second, bruneau.fr's 39-47% NB IS in France is the highest NB impression share of any competitor globally — it's suppressing FR NB performance. Third, internal Amazon entities (AGL in UK and ES) bidding on AB terms is a coordination problem, not a competitive one — this should be escalated internally.

**IT note:** IT Brand Core CPC is up +131% YoY — the highest in EU5. This isn't driven by a single dominant competitor but by limited ad opportunities in the Italian market combined with multiple small entrants.

## International Markets: Emerging but Manageable

| Market | Primary Competitor | IS | CPC Impact | Notes |
|--------|-------------------|-----|------------|-------|
| CA | Shopify.com | <10% Brand Core | +13% CPC when present | Recurring but not persistent. IS validated W10 2026. |
| JP | axalpha.com | 10% Brand Core (Google) | New threat | First appeared W6-W7 2026. IS validated W10 2026. |
| JP | shop-pro.jp | 12-15% Yahoo Brand Core | Strengthening | Yahoo-specific — different platform dynamics. IS validated W10 2026. |
| JP | Rakuten, moneyforward.com | Present on Yahoo | Persistent | Established Yahoo competitors. IS validated W10 2026. |
| MX | algo-mas.mx | 11-13% Brand | +20% CPC spikes | Most consistent MX competitor. IS validated W10 2026. |
| MX | Temu | Generic NB | Emerging | W23 2025. IS validated W10 2026. |

**So what:** JP competition is intensifying specifically on Yahoo, with multiple new entrants in early 2026 (axalpha, shop-pro.jp, ec-force.com). This is the market to watch — JP is already underperforming OP2 by 14% on registrations due to the MHLW campaign ending, and rising competition compounds the headwind. CA and MX competition is manageable — Shopify and algo-mas.mx are present but not dominant.

## Key Trends (2024-2026)

1. **Competition is broadening, not just deepening.** Markets went from 1-2 competitors (2023) to 3-5 (2026). This is a structural shift, not a temporary spike.
2. **Walmart is unique.** No other competitor globally has sustained aggressive Brand bidding for 18+ months. All others cycle in and out.
3. **EU competition is fragmentary.** Different competitors per market makes a unified response impossible. Each market needs its own monitoring cadence.
4. **JP competition is intensifying on Yahoo specifically.** Google competition in JP is minimal; Yahoo is where the battle is.
5. **The team's defense is efficiency, not escalation.** OCI, campaign consolidation, ad copy optimization, and LP improvements allow the team to absorb CPC increases without proportional budget increases.
6. **Internal Amazon entities are bidding on AB terms.** AGL in UK and ES is an internal coordination issue that should be escalated, not competed against.

## Decision Guide

| Situation | Action | Why |
|-----------|--------|-----|
| New competitor appears with >10% IS on Brand | Monitor for 4 weeks. If persistent, add to this doc and adjust bid caps. | Most competitors cycle out within 4-6 weeks. Don't react to noise. |
| Existing competitor IS increases >5% WoW | Flag in WBR callout. Check if CPA impact is material at program level. | IS changes matter only if they move program-level CPA. |
| Brand CPA spikes >20% WoW | Check competitor IS first. If competitor-driven, hold bid caps and let NB efficiency absorb. | Escalating bids rewards the competitor's strategy. |
| Internal Amazon entity bidding on AB terms | Escalate to Brandon/Kate. This is a coordination problem. | Don't compete with ourselves. |
| Competitor appears on NB terms | Less urgent — NB competition is normal. Monitor CVR impact. | NB competition affects volume, not brand equity. |

## Update Cadence

- **Weekly:** Check auction insights for IS changes >5% in any market. Update the relevant row.
- **Monthly:** Full competitive review across all markets after MBR data refresh.
- **Ad hoc:** When WBR data shows unexpected CPC/CPA spikes, investigate and update.
- **Quarterly:** Review whether any competitor has exited (>8 weeks absent) and archive their row.

## Related

- [Eyes — Competitive Landscape](~/shared/context/body/eyes.md) — live competitive data updated each loop run
- [Competitor Intel Research](~/shared/research/competitor-intel.md) — raw competitive data from WBR callouts
- [Brain — D2: Competitive Response](~/shared/context/body/brain.md) — the decision rationale for efficiency over escalation
- [OCI Rollout Playbook](oci-playbook) — how OCI enables the efficiency-based competitive response

## Sources
- Competitive IS and CPC data — source: `shared/research/competitor-intel.md`, WBR callouts W27 2024 - W10 2026
- Walmart trajectory and Brand CPA impact — source: `shared/context/body/eyes.md`, Competitive Landscape section, updated 2026-03-25
- Strategic response (efficiency over escalation) — source: `shared/context/body/brain.md`, Decision D2
- EU5 per-market competitor data — source: `shared/research/competitor-intel.md`, EU5 section
- IT CPC YoY — source: `shared/research/competitor-intel.md`, IT section
- JP Yahoo competition — source: `shared/context/body/eyes.md`, International Competitors table

<!-- AGENT_CONTEXT
machine_summary: "AB Paid Search faces broadening competition across 10 markets. Walmart Business is the only sustained aggressive Brand bidder (37-55% IS in US since Jul 2024, driving Brand CPA from $40 to $65-77). EU5 has fragmented competition (different per market, weareuncapped.com most persistent at 24% UK Brand IS). JP competition intensifying on Yahoo. Team defense is efficiency over escalation — OCI-powered NB gains absorb Brand CPA increases at program level."
key_entities: ["Walmart Business", "weareuncapped.com", "bruneau.fr", "algo-mas.mx", "shop-pro.jp", "axalpha.com", "Temu", "Amazon Global Logistics", "OCI", "Brand CPA"]
action_verbs: ["monitor", "escalate", "absorb", "flag", "hold-bid-caps"]
update_triggers: ["new competitor >10% IS in any market", "MBR data refresh (monthly)", "Walmart IS change >5%", "new internal Amazon entity bidding on AB terms"]
-->
