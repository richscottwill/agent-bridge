---
title: "Workstream 2: Modern Search"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0411 | duck_id: testing-workstream-modern-search -->

---
title: "Workstream 2: Modern Search"
status: FINAL
doc-type: strategy
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-04-05
update-trigger: "EU4 ad copy results available, IT test reaches sufficient volume, AI Max test launches, new market consolidation completed"
tags: [modern-search, ad-copy, consolidation, kate-doc]
---

# Workstream 2: Modern Search

This document explains how the Paid Search team restructured campaigns and rewrote ad copy based on customer research, delivering +31% registrations and +70% CTR in the UK. It supports the Testing Approach narrative for Kate and connects directly to the OCI and Algorithmic Ads workstreams. After reading, you should understand why consolidation was necessary, what the SP study revealed, and how the team is scaling these changes worldwide.

## What problem did fragmented campaigns create?

Prior to consolidation, campaigns were split across device types and narrow keyword themes. Each campaign had its own bid strategy operating on a thin slice of data. This fragmentation starved the bidding algorithms of signal — fewer conversions per bid strategy meant slower learning and less accurate CPA optimization. When OCI launched, it needed rich data density to optimize effectively. Fragmented campaigns were the bottleneck.

The team consolidated device-specific campaigns and keyword themes across markets, starting with the US (Responsive Search Ads and device consolidation) and extending to EU5 (UK and DE Product and Vertical campaigns completed, remaining markets following as OCI rolls out). Fewer campaigns means more conversions per bid strategy, which means faster algorithm learning. This structural simplification is also a prerequisite for AI Max testing (see Workstream 5: Algorithmic Ads), which requires consolidated campaign structures to function effectively.

## What did the SP study reveal about our messaging?

The AB Sole Proprietor Experience study (August 2025) surveyed Sole Proprietors in the US and UK about what matters most when choosing suppliers. The findings exposed a fundamental mismatch between our ad copy and customer needs.

Sole Proprietors said price (31% US, 22% UK) and product quality (25% US, 33% UK) mattered most. They said ability to buy in bulk (27% US, 19% UK) mattered least. The critical finding: 50% of Sole Proprietors in both markets believed Amazon Business required bulk purchasing and was not free. Our existing ads — featuring phrases like "Online Bulk Purchasing" and "Wholesale & Bulk Prices" — reinforced both misconceptions (see Appendix: SP Study Data).

The team rewrote ad copy to address these misconceptions directly. "Online Bulk Purchasing" became "Smart Business Buying." "Online Wholesale Purchasing" became "For Businesses of All Sizes." "Purchase at Wholesale Price" became "No Minimum Order Required." We also added keyword insertion to headlines — only 6% of UK Brand ads and 23% of UK NB ads included keyword insertion previously — allowing Google to match user intent more precisely (see Appendix: Ad Copy Changes).

## What did the UK test show?

The UK AMZ Portfolio test (Phase 1, January 29 to March 2, 2026) compared 33 days of pre-period performance against 33 days of post-period performance. Despite 25% fewer impressions, the new ads drove 28% more clicks and 31% more registrations. CTR improved from 14% to 24% — a 70% increase. CVR held steady at approximately 5.2%, confirming the lift came from better-qualified clicks rather than volume inflation. Confidence: HIGH (30-day test, meaningful volume across the portfolio).

The IT test (Phase 1, February 19 to March 5, 2026) showed directionally positive CTR at +15%, but volume was too low to draw conclusions — 97% fewer clicks than control. Confidence: LOW (insufficient volume). The team needs more time before making a call on IT.

## How does this connect to competitive strategy?

As competitors increase Brand CPCs — Walmart at 37-55% impression share in the US, weareuncapped at 24% impression share in the UK — the team's response is not to escalate bids but to make ads more compelling. Higher CTR and CVR from the same or fewer impressions is a sustainable competitive advantage because it is based on customer research rather than budget.

## How are we scaling in 2026?

Keyword theme consolidation continues worldwide as part of the OCI rollout to RoW, combining campaign keyword themes to further reduce campaign count and strengthen data signals. EU4 ad copy translations are completed via GlobalLink (submission ID 2028024, delivered February 18, 2026) in IT, DE, FR, and ES, with phased rollout across all non-brand campaigns. The consolidated campaign structures also serve as the prerequisite for AI Max testing in Q2 2026.

## What are the risks and open questions?

The IT test volume is too low to validate the ad copy changes in that market. We need a longer test window or higher-traffic campaign set before drawing conclusions. The EU4 translations were completed by GlobalLink, but localized messaging effectiveness has not been validated — the UK results may not transfer directly to markets with different competitive dynamics and customer expectations. The team should plan for per-market validation as each rollout completes.

## Cross-functional partners

Customer Research conducted the AB Sole Proprietor Experience study (August 2025) that provided the foundation for the messaging shift. Google (Mike Babich) advised on keyword insertion recommendations and RSA best practices. GlobalLink completed the EU4 translations. The Creative team developed ad copy aligned with the "Smart Business Buying" brand messaging.

---

## Appendix

### Appendix A: SP study data

What SPs said matters most when choosing suppliers:

| Factor | US | UK |
|--------|----|----|
| Price | 31% | 22% |
| Product quality | 25% | 33% |
| Selection | 21% | 15% |

What SPs said matters least:

| Factor | US | UK |
|--------|----|----|
| Ability to buy in bulk | 27% | 19% |
| Location of store | 24% | 23% |
| Rewards program | 22% | 25% |

Why SPs without B2B accounts did not sign up:

| Reason | US | UK |
|--------|----|----|
| Believed B2B required bulk purchasing | 50% | 49% |
| Savings wouldn't justify perceived costs | 31% | 26% |
| Business wouldn't qualify | 19% | 18% |

The dominant barrier — 50% in both markets — was a misconception that the existing ad copy actively reinforced. This is not a product problem; it is a messaging problem with a clear fix.

### Appendix B: Ad copy changes

| Before | After | Rationale |
|--------|-------|-----------|
| Online Bulk Purchasing | Smart Business Buying | Updated brand messaging |
| Online Wholesale Purchasing | For Businesses of All Sizes | Addresses qualification concern |
| Purchase at Wholesale Price | No Minimum Order Required | Addresses bulk misconception |
| Wholesale & Bulk Prices | Quantity Discounts | Reframes value without bulk framing |

Every change maps directly to a specific misconception identified in the SP study. The copy shifts from wholesale/bulk framing to accessibility and value framing.

### Appendix C: UK AMZ Portfolio test results (Phase 1)

| Metric | Before (Dec 27-Jan 28) | After (Jan 29-Mar 2) | Change |
|--------|----------------------|---------------------|--------|
| Impressions | 37,388 | 28,010 | -25% |
| Clicks | 5,308 | 6,778 | +28% |
| Cost | $19,253 | $20,072 | +4% |
| Registrations | 273 | 358 | +31% |
| CTR | 14% | 24% | +70% |
| CVR | 5.10% | 5.30% | +3% |

The cost increase was marginal (+4%) while registrations grew +31%, meaning CPA improved meaningfully. The CTR jump from 14% to 24% is the headline — the research-driven messaging resonated at a measurably higher rate.

<!-- AGENT_CONTEXT
machine_summary: "Modern Search workstream: campaign consolidation (device + keyword theme) to strengthen OCI data signals, plus research-driven ad copy overhaul based on SP study (Aug 2025). SP study revealed 50% of SPs believed AB required bulk purchasing — existing ads reinforced the misconception. New copy shifted to price/quality/selection messaging. UK Phase 1 results: +70% CTR (pre/post), +31% regs with HIGH confidence (30-day test). IT: +15% CTR but LOW confidence (insufficient volume). EU4 translations completed via GlobalLink. Consolidation is prerequisite for AI Max. Competitive response: higher CTR from better messaging rather than bid escalation."
key_entities: ["SP study", "campaign consolidation", "RSA", "keyword insertion", "GlobalLink", "AI Max", "OCI"]
action_verbs: ["consolidate", "test", "translate", "scale", "rewrite"]
update_triggers: ["EU4 ad copy results available", "IT test reaches sufficient volume", "AI Max test launches", "new market consolidation completed"]
-->
