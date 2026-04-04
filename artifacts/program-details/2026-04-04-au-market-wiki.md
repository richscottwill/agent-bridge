---
title: AU Paid Search — Market Wiki
status: DRAFT
doc-type: reference
audience: amazon-internal
level: N/A
owner: Richard Williams
created: 2026-04-04
updated: 2026-04-04
update-trigger: AU performance shifts >10%, OCI AU launch, stakeholder direction changes, quarterly planning
tags: [market-wiki, au, overview]
replaces: au-market-wiki, au-market-overview, au-paid-search-market-overview
---

# AU Paid Search — Market Wiki

> Canonical reference for Australia. One doc, one source of truth.

---

## Overview

Australia is the newest market in the AB Paid Search portfolio, launched in June 2025 (W24). Richard owns AU hands-on. It operates on a $1.8M net annual budget with an OP2 target of 12,906 registrations at a $140 CPA. FY25 was a partial year ($1.14M spend, 8,763 regs, $158 CPA across seven months), so every trend line is still being established.

The market sits at an inflection point. The foundational work — account build, keyword coverage, landing page migration — is largely complete. The next phase is efficiency: reducing CPA through smarter bidding, tighter keyword-product alignment, and OCI integration. AU does not yet have OCI support (target: May 2026), which means it is running without the conversion signal infrastructure that drives 16-20% registration lifts in other markets.

---

## Current Performance

February 2026 closed at approximately 1,100 registrations against a 1,110 plan — essentially flat to OP2 at roughly $140 CPA.

The most recent weekly data (W13): 207 registrations, down 16% WoW, CPA $118 (+3%). CVR dropped 12% WoW across both Brand (-14%) and NB (-10%). Daily pattern: Mon-Tue strong (53, 50 regs) then collapsed (27, 22, 23, 8) — mid-week Polaris migration likely contributed.

NB CPC has been declining for seven consecutive weeks ($6.82 to $4.81, -29%), a genuine structural improvement. NB CPA has held flat at $187 — CPC gains are not yet translating to proportional CPA improvement, suggesting conversion rate is the binding constraint, not traffic cost.

| Metric | Value | vs OP2 | Notes |
|--------|-------|--------|-------|
| Registrations (Feb) | 1.1K | -1% | Slight miss, within margin |
| Spend (Feb) | $159K | — | — |
| CPA (Feb) | ~$140 | Target | Lena's benchmark |
| NB CPC (W13) | $4.81 | — | Down from $6.82 (7-week decline) |
| NB CPA (W13) | $187 | — | Flat despite CPC improvement |

---

## Campaign Structure

| Campaign | Type | Status | Bidding | Notes |
|----------|------|--------|---------|-------|
| AU Brand | Brand | Active | Manual CPC, bid caps | Competitive defense |
| AU NB | Non-Brand | Active | Manual CPC (no OCI) | Primary growth driver |
| AU Category | Category | Proposed | TBD | MRO/Trades vertical (see AU NB Testing Proposal) |

---

## Active Initiatives

### Polaris Landing Page Migration
Lena directed a full switch from legacy MCS pages to Polaris — no phased test, no 50/50 split. Alexis completed the keyword-to-URL mapping, migration executed mid-March. Early data is noisy (W13 CVR drop may be partially attributable). The US MCS brand page template showed a 38bps conversion improvement, and Polaris is the long-term platform.

### Two-Campaign Restructure (Proposed 3/24)
Split current NB campaign into product-intent and business-intent segments. Hypothesis: keyword-product alignment will improve Quality Score and reduce wasted spend on queries that convert at fundamentally different rates. Still in proposal stage.

### OCI Integration (Target: May 2026)
MCC has not been created. Adobe-side discussion (Suzane Huynh) happened 3/19 without firm commitment. OCI delivered +16-20% registration lift in DE and transformed US performance — this is the single highest-leverage initiative for AU. Until OCI is live, AU is bidding without conversion signals.

### AU NB MRO/Trades Test
Budget-neutral test targeting MRO and Trades keywords. Reallocating from underperforming generic NB, not incremental spend. Requires Alexis LP confirmation and Lena input on priority verticals. See [AU NB Testing Proposal](~/shared/artifacts/testing/2026-03-25-au-nb-mro-trades-proposal.md).

---

## Key Stakeholders

| Name | Role | Communication Style | Key Context |
|------|------|-------------------|-------------|
| Lena Zak | Country Leader (L7), Sydney | Direct, data-forward. Expects numbers, not narratives. Signs "Cheers, Lena" | Challenged $6 CPC as "outrageous" (benchmarking vs Consumer $0.18-0.50). Pattern of reversing agreed decisions (Brandon flagged). Hardest stakeholder — always have AU metrics loaded. |
| Alexis Eck | Sr. Mktg Mgr (L6), Sydney | Professional, collaborative. Signs "Thanks, Alexis" | Strong execution partner. Owns MCS page mapping. Defers to Lena on strategy. |
| Harsha Mudradi | Sr. PM, Search (L6) | Professional | AU sync attendee. Prime International. Stepped back from day-to-day. |
| Brandon Munday | Richard's manager (L7) | Supportive | Offered to join AU syncs. Flagged Lena's decision-reversal pattern. Guidance: own the narrative, lead with data, don't get defensive. |

---

## The CPC Challenge

Lena flagged $6 avg CPC as excessive, benchmarking against Consumer ($0.18-0.50). This is an apples-to-oranges comparison:

- B2B search is structurally more expensive than consumer (lower volume, higher intent, fewer advertisers)
- Shopping Ads are not available for AB — consumer Amazon uses Shopping Ads which have lower CPCs
- No OCI means AU is bidding manually, which is inherently less efficient than algorithmic bidding

The response: NB CPC has declined 29% over 7 weeks ($6.82 to $4.81) through bid strategy optimization. OCI (May 2026) will further improve efficiency. CPC bid caps are a "two-way door" (Brandon's framing) — reversible if they constrain volume.

---

## Competitors

No competitors in AU currently. This is unusual — most markets have 3-5 competitors by 2026. AU's isolation may be due to market size and maturity.

---

## Recurring Meetings

- AB AU Paid Search Sync: weekly (Alexis, Lena, Harsha, Richard)
- Prep: load AU data from eyes.md, have CPA trend ready, surface AU-related Asana tasks

---

## Key Decisions

| Decision | Made By | Date | Rationale |
|----------|---------|------|-----------|
| Full Polaris migration (no 50/50 split) | Lena Zak | 3/13 | Lena overrode phased test recommendation |
| CPC bid caps as "two-way door" | Brandon | 3/23 | Short-term efficiency lever while waiting for OCI |
| Brandon offered to join AU syncs | Brandon | 3/23 | Support Richard in managing Lena's expectations |
| Two-campaign structure (product vs business intent) | Richard (proposed) | 3/24 | Improve keyword-product alignment |

---

## Open Questions

1. How much of the W13 CVR drop is attributable to Polaris migration vs. seasonal softness vs. promo transition?
2. What is the realistic OCI AU timeline? May 2026 target, but MCC not created and Adobe has not committed.
3. Should CPC bid caps be implemented now as a short-term lever?
4. When CCP data arrives (projected July 2026), how will ie%CCP change the optimization strategy?
5. Can the two-campaign structure be validated with historical query data before live test?

---

## Sources
- AU performance data (Feb 2026, W13) — source: ~/shared/context/body/eyes.md -> Market Health -> AU
- AU budget and OP2 targets — source: ~/shared/context/active/callouts/au/au-context.md
- OCI status — source: ~/shared/context/body/eyes.md -> OCI Performance
- Stakeholder dynamics — source: ~/shared/context/body/memory.md -> Relationship Graph
- Lena CPC challenge and Brandon guidance — source: ~/shared/context/body/memory.md -> Brandon, Lena entries
- Polaris migration decision — source: ~/shared/context/body/brain.md -> D4: AU Landing Page
- NB CPC 7-week decline — source: ~/shared/context/body/eyes.md -> Market Health -> AU
- Campaign structure — source: ~/shared/context/body/hands.md -> Recurring Execution Work

<!-- AGENT_CONTEXT
machine_summary: "Canonical AU market reference. Merges former AU Market Wiki and AU Market Overview into one doc. Launched June 2025, Richard's primary hands-on market. $1.8M budget, 12,906 reg OP2 target, $140 CPA. Key dynamics: Lena Zak (L7) driving CPC scrutiny ($6 avg, benchmarking vs Consumer $0.18-0.50), Polaris full migration (no phased test, Lena's decision), no OCI (target May 2026). NB CPC declining 7 weeks (-29%) but NB CPA flat at $187 — CVR is the binding constraint. No competitors. Open questions on OCI timeline, CPC bid caps, and two-campaign restructure."
key_entities: ["AU", "Lena Zak", "Alexis Eck", "Brandon Munday", "Polaris", "OCI", "CPC", "CPA", "NB", "Brand", "MRO/Trades", "Harsha Mudradi"]
action_verbs: ["optimize", "migrate", "investigate", "propose", "report", "restructure"]
update_triggers: ["AU performance shifts >10%", "OCI AU launch or timeline change", "Lena/Alexis direction changes", "CCP data arrival", "quarterly planning"]
-->
