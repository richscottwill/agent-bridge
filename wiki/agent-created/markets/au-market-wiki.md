---
title: "AU Paid Search — Market Wiki"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0318 | duck_id: program-au-market-wiki -->

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

This is the canonical reference for Australia Paid Search. Use it to prep for AU syncs, understand market dynamics, and track active initiatives. It consolidates three former documents into one source of truth. Richard owns AU hands-on.

## Strategic Situation

AU sits at an inflection point. The foundational work — account build, keyword coverage, landing page migration — is largely complete. NB CPC has declined 29% over seven consecutive weeks ($6.82 to $4.81), a genuine structural improvement driven by bid strategy optimization. But that CPC gain is not translating to proportional CPA improvement: NB CPA has held flat at $187, which means conversion rate is the binding constraint, not traffic cost.

The single highest-leverage initiative for AU is OCI integration, targeted for May 2026. OCI delivered 16-20% registration lifts in DE and transformed US performance. Until OCI is live, AU is bidding without conversion signals — the equivalent of driving without a speedometer. The MCC has not been created, and Adobe (Suzane Huynh) has not committed to a firm timeline, which makes the May target aspirational rather than confirmed.

## Current Performance

February 2026 closed at approximately 1,100 registrations against a 1,110 plan — essentially flat to OP2 at roughly $140 CPA. The most recent weekly data from W13 showed 207 registrations, down 16% week-over-week, with CPA at $118 (+3%). CVR dropped 12% WoW across both Brand (-14%) and NB (-10%). The daily pattern was front-loaded: Monday and Tuesday produced 53 and 50 registrations respectively, then collapsed to 27, 22, 23, and 8 through the rest of the week. The mid-week Polaris migration likely contributed to the drop.

The headline: AU is tracking to OP2 on registrations and CPA, but the NB efficiency story is incomplete. CPC gains are not translating to CPA improvement because conversion rate is the binding constraint. Solving this requires either OCI (algorithmic bidding with conversion signals) or landing page optimization (improving the conversion funnel itself) — ideally both.


## Campaign Structure

AU runs two active campaigns. Brand operates on manual CPC with bid caps for competitive defense — this is standard across all markets and will not change with OCI. NB is the primary growth driver, also on manual CPC since OCI is not yet available. A third campaign targeting MRO and Trades verticals has been proposed as a budget-neutral test, reallocating from underperforming generic NB rather than requesting incremental spend. That proposal requires Alexis's landing page confirmation and Lena's input on priority verticals before it can proceed. See the [AU NB Testing Proposal](../testing/au-nb-mro-trades-proposal.md) for the full design.

## Active Initiatives

Polaris landing page migration is complete. Lena directed a full switch from legacy MCS pages to Polaris — no phased test, no 50/50 split. Alexis completed the keyword-to-URL mapping and the migration executed mid-March. Early data is noisy; the W13 CVR drop may be partially attributable to the migration, but the US MCS brand page template showed a 38bps conversion improvement, and Polaris is the long-term platform. The question is whether the short-term disruption masks a structural improvement that will emerge over the next two to four weeks.

The two-campaign restructure proposed on 3/24 would split the current NB campaign into product-intent and business-intent segments. The hypothesis is that keyword-product alignment will improve Quality Score and reduce wasted spend on queries that convert at fundamentally different rates. This remains in proposal stage.

OCI integration targets May 2026 via the Adobe OCI path. As noted above, the MCC has not been created and Adobe has not committed. This is the single highest-leverage initiative for AU and the gap between "target" and "confirmed" needs to close.

The AU NB MRO/Trades test is a budget-neutral experiment targeting MRO and Trades keywords by reallocating from underperforming generic NB. It requires Alexis's LP confirmation and Lena's input on priority verticals.

## The CPC Challenge

Lena flagged $6 average CPC as excessive, benchmarking against Consumer ($0.18-0.50). This is an apples-to-oranges comparison. B2B search is structurally more expensive than consumer because of lower volume, higher intent, and fewer advertisers. Shopping Ads are not available for Amazon Business — consumer Amazon uses Shopping Ads which have lower CPCs. And without OCI, AU is bidding manually, which is inherently less efficient than algorithmic bidding.

The response: NB CPC has declined 29% over seven weeks through bid strategy optimization. OCI will further improve efficiency when it launches. CPC bid caps are a "two-way door" in Brandon's framing — reversible if they constrain volume. The pattern with Lena is that she drives fast, unilateral decisions (Polaris full migration, CPC scrutiny) and Brandon provides air cover. Richard's role is to own the narrative with data and not get defensive.

## Key Stakeholders

Lena Zak is the AU Country Leader (L7) based in Sydney. She is direct and data-forward, expects numbers rather than narratives, and signs off "Cheers, Lena." She challenged the $6 CPC as "outrageous" by benchmarking against Consumer rates, and has a pattern of reversing agreed decisions that Brandon has flagged. She is the hardest stakeholder — always have AU metrics loaded before any interaction.

Alexis Eck is the Senior Marketing Manager (L6) in Sydney. She is professional and collaborative, a strong execution partner who owns the MCS page mapping and defers to Lena on strategy.

Brandon Munday is Richard's manager (L7). She offered to join AU syncs, flagged Lena's decision-reversal pattern, and provided the guidance: own the narrative, lead with data, do not get defensive.

## Open Questions and Next Steps

Five questions need answers, and each has an owner. First, how much of the W13 CVR drop is attributable to Polaris migration versus seasonal softness versus promo transition? Richard needs to run the analysis using two to three more weeks of post-migration data, targeting a read by mid-April. Second, what is the realistic OCI AU timeline? The May 2026 target exists but the MCC is not created and Adobe has not committed. Richard needs to follow up with Suzane Huynh and escalate if no commitment by mid-April. Third, should CPC bid caps be implemented now as a short-term efficiency lever? This is a Brandon decision pending Richard's recommendation with supporting data. Fourth, when CCP data arrives (projected July 2026), how will ie%CCP change the optimization strategy? This is a planning question for Q3. Fifth, can the two-campaign structure be validated with historical query data before a live test? Richard needs to pull the query-level data and segment it to test the hypothesis offline.

---

## Sources
- AU performance data (Feb 2026, W13) — source: ~/shared/context/body/eyes.md → Market Health → AU
- AU budget and OP2 targets — source: ~/shared/context/active/callouts/au/au-context.md
- OCI status — source: ~/shared/context/body/eyes.md → OCI Performance
- Stakeholder dynamics — source: ~/shared/context/body/memory.md → Relationship Graph
- Lena CPC challenge and Brandon guidance — source: ~/shared/context/body/memory.md → Brandon, Lena entries
- Polaris migration decision — source: ~/shared/context/body/brain.md → D4: AU Landing Page
- NB CPC 7-week decline — source: ~/shared/context/body/eyes.md → Market Health → AU

<!-- AGENT_CONTEXT
machine_summary: "Canonical AU market reference. Merges former AU Market Wiki and AU Market Overview into one doc. Launched June 2025, Richard's primary hands-on market. $1.8M budget, 12,906 reg OP2 target, $140 CPA. Key dynamics: Lena Zak (L7) driving CPC scrutiny ($6 avg, benchmarking vs Consumer $0.18-0.50), Polaris full migration (no phased test, Lena's decision), no OCI (target May 2026). NB CPC declining 7 weeks (-29%) but NB CPA flat at $187 — CVR is the binding constraint. Open questions have owners and timelines."
key_entities: ["AU", "Lena Zak", "Alexis Eck", "Brandon Munday", "Polaris", "OCI", "CPC", "CPA", "NB", "Brand", "MRO/Trades"]
action_verbs: ["optimize", "migrate", "investigate", "propose", "report", "restructure"]
update_triggers: ["AU performance shifts >10%", "OCI AU launch or timeline change", "Lena/Alexis direction changes", "CCP data arrival", "quarterly planning"]
-->


## Related

- [OCI Program](../testing/oci-program) — AU OCI target May 2026
- [Polaris Program](polaris-program) — AU Polaris full migration complete
- [CPC Benchmark Defense Playbook](cpc-benchmark-defense-playbook) — framework for the Lena CPC response
- [AU NB MRO Trades Proposal](../testing/au-nb-mro-trades-proposal) — proposed AU category test
- [AU Keyword CPA Dashboard](../reporting/au-keyword-cpa-dashboard) — weekly review tooling
- [Paid Search Testing Approach](../testing/testing-approach-kate-v5) — testing methodology
