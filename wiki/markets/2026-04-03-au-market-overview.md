<!-- DOC-0317 | duck_id: program-au-market-overview -->
> **⚠️ ARCHIVED — 2026-04-04. Replaced by au-market-wiki. Do not update this file.**

---
title: AU Paid Search — Market Overview
status: archived
audience: amazon-internal
level: N/A
owner: Richard Williams
created: 2026-04-03
updated: 2026-04-03
update-trigger: AU performance shifts >10%, OCI AU launch, stakeholder direction changes, quarterly planning
tags: market-wiki, au, overview
---

# AU Paid Search — Market Overview

---

## Overview

Australia is the newest market in the AB Paid Search portfolio, launched in June 2025 (W24). It operates on a $1.8M net annual budget with an OP2 target of 12,906 registrations at a $140 CPA. Unlike the more mature US and EU markets, AU has no year-over-year comparisons yet — FY25 was a partial year ($1.14M spend, 8,763 regs, $158 CPA across seven months), so every trend line is still being established.

The market sits at an inflection point. The foundational work — account build, keyword coverage, landing page migration — is largely complete. The next phase is efficiency: reducing CPA through smarter bidding, tighter keyword-product alignment, and OCI integration. AU does not yet have OCI support (target: May 2026), which means it's running without the conversion signal infrastructure that drives 16-20% registration lifts in markets like DE and the +86% YoY peak in US. That gap defines much of the current performance ceiling.

## Current Performance

February 2026 closed at approximately 1,100 registrations against a 1,110 plan — essentially flat to OP2 at roughly $140 CPA. The miss is marginal, but the trajectory underneath it matters more than the topline.

The most recent weekly data (W13) tells a sharper story: 207 registrations, down 16% week-over-week, with CPA climbing to $118 (+3%). CVR dropped 12% WoW across both Brand (-14%) and Non-Brand (-10%). The daily pattern was telling — Monday and Tuesday delivered 53 and 50 registrations respectively, then volume collapsed to 27, 22, 23, and 8 through the rest of the week. The mid-week Polaris migration likely contributed to that falloff, though we're still isolating the signal.

On the efficiency side, NB CPC has been declining for seven consecutive weeks ($6.82 → $4.81, a 29% reduction), which is a genuine structural improvement. NB CPA, however, has held flat at $187 — the CPC gains aren't yet translating to proportional CPA improvement, which suggests conversion rate is the binding constraint, not traffic cost.

## Active Initiatives

Three workstreams are running in parallel, each addressing a different layer of the performance stack:

The Polaris landing page migration is the most visible. Lena Zak (AU Country Leader) directed a full switch from legacy MCS pages to Polaris — no phased test, no 50/50 split. Alexis Eck completed the keyword-to-URL mapping, and the migration executed mid-March. Early data is noisy (the W13 CVR drop may be partially attributable), but the structural bet is sound: the US MCS brand page template showed a 38bps conversion improvement, and Polaris is the long-term platform.

The two-campaign restructure (proposed 3/24) would split the current Non-Brand campaign into product-intent and business-intent segments. The hypothesis is that keyword-product alignment will improve Quality Score and reduce wasted spend on queries that convert at fundamentally different rates. This is still in proposal stage.

OCI integration is targeted for May 2026 but has not started — the MCC has not been created, and the Adobe-side discussion (with Suzane) happened on 3/19 without a firm commitment. Given that OCI delivered +16-20% registration lift in DE and transformed US performance, this is the single highest-leverage initiative for AU. Until OCI is live, AU is bidding without conversion signals — the equivalent of driving with the dashboard lights off.

## Key Stakeholders

Lena Zak (L7, Sydney) is the AU Country Leader and the primary decision-maker. She is direct, data-driven, and sets the pace for AU syncs. Lena challenged the $6 average CPC as excessive (benchmarking against Consumer at $0.18-0.50), which is an apples-to-oranges comparison — B2B search is structurally more expensive, and Shopping Ads are not available for AB — but her scrutiny reflects real pressure from AU leadership to demonstrate efficiency. Expect weekly CPA reviews and pointed questions on keyword-level performance.

Alexis Eck (L6, Sydney) is the execution partner. She owns the MCS page mapping, coordinates with the local team, and runs the weekly sync logistics. Professional, collaborative, and reliable — Alexis defers to Lena on strategic calls but drives implementation.

Brandon Munday (L7, Richard's manager) has offered to join AU syncs if needed and has explicitly flagged Lena's pattern of reversing previously agreed decisions (e.g., overruling the 50/50 LP test in favor of a full switch). Brandon's guidance: own the narrative, lead with data, don't get defensive.

## Open Questions

1. How much of the W13 CVR drop is attributable to the Polaris migration vs. seasonal softness vs. the Back-to-Biz → Evergreen promo transition?
2. What is the realistic OCI AU timeline? May 2026 is the target, but MCC creation hasn't started and Adobe hasn't committed resources.
3. Should we implement CPC bid caps as a short-term efficiency lever while waiting for OCI? Brandon framed this as a "two-way door" — reversible if it constrains volume.
4. When CCP data arrives (projected July 2026), how will an ie%CCP target change the optimization strategy? The current CPA-only constraint may shift.
5. Can the two-campaign structure proposal be validated with historical query-level data before implementation, or does it require a live test?

---

## Sources
- AU performance data (Feb 2026, W13) — source: ~/shared/context/body/eyes.md → Market Health → AU
- AU budget and OP2 targets — source: ~/shared/context/active/callouts/au/au-context.md
- OCI status and market rollout — source: ~/shared/context/body/eyes.md → OCI Performance
- Stakeholder dynamics — source: ~/shared/context/body/memory.md → Relationship Graph
- Lena CPC challenge and Brandon guidance — source: ~/shared/context/body/memory.md → Brandon Munday, Lena Zak entries
- Polaris migration decision — source: ~/shared/context/active/callouts/au/au-context.md → Active Email Threads

<!-- AGENT_CONTEXT
machine_summary: "Strategic market overview for AU Paid Search. Covers current state (1.1K regs, ~$140 CPA, no OCI), active initiatives (Polaris migration, two-campaign restructure, OCI May 2026 target), stakeholder dynamics (Lena Zak driving CPC scrutiny, Alexis Eck executing), and five open questions. Written as a reference doc for any team member."
key_entities: ["AU", "Lena Zak", "Alexis Eck", "Brandon Munday", "Polaris", "OCI", "CPC", "CPA", "NB", "Brand", "MCS"]
action_verbs: ["migrate", "restructure", "integrate", "optimize", "validate"]
update_triggers: ["AU performance shifts >10%", "OCI AU launch or timeline change", "Lena/Alexis direction changes", "CCP data arrival", "quarterly planning"]
-->
