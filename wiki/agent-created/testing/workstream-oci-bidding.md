---
title: "Workstream 1: Intelligent Bidding (OCI)"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0412 | duck_id: testing-workstream-oci-bidding -->

---
title: "Workstream 1: Intelligent Bidding (OCI)"
status: FINAL
doc-type: strategy
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-04-05
update-trigger: "EU4 market OCI results available, hvocijid investigation resolved, CA/JP E2E results, DMA policy changes"
tags: [oci, bidding, kate-doc]
---

# Workstream 1: Intelligent Bidding (OCI)

This document details how the Paid Search team implemented Offline Conversion Import (OCI) bidding as the first non-retail business unit at Amazon, delivering +35,196 incremental registrations and $16.7MM in OPS across three markets. It supports the Testing Approach narrative for Kate and provides the evidence base for the 2026 RoW expansion plan. After reading, you should understand the problem OCI solved, the validated results, and the scaling strategy.

## What problem did OCI solve?

The team lost access to Google Ads auto-bid strategy and Adobe-managed bidding in 2024, creating a gap in algorithmic optimization. Without a first-party conversion signal feeding back to Google, bid strategies relied on platform-side proxies that could not distinguish high-value registrations from low-value clicks. Non-Brand CPA was elevated, and the team had no mechanism to tell Google which conversions actually mattered to the business.

OCI closed that gap by sending Amazon's own conversion data back to Google, enabling the algorithm to optimize toward registrations rather than clicks. This was not a plug-and-play integration. It required defining the OCI value framework with Data Science (Yogesh), securing Legal approval for the data flow, building tracking infrastructure with MarTech (Joel Mallory), and validating the underlying data at each stage. The team established a phased implementation plan — E2E keyword-level testing, then 25%, 50%, and 100% campaign-level application — with go/no-go gates at each phase.

## What did the tests show?

The US launched first (July-November 2025) and delivered +24% registration lift with approximately 50% NB CPA improvement, generating +32,047 incremental registrations and $16.7MM in OPS — 96% of expectation. The UK followed (August-October 2025) with +23% registration lift and +2,400 registrations at 94% of expectation. DE launched last (October-December 2025) with +18% registration lift and +749 registrations at 86% of expectation. Across all three markets, OCI delivered +35,196 incremental registrations. Confidence: HIGH (multi-month tests, meaningful volume, consistent directional results across three markets).

Brand CPA improved -10% to -14% across all three markets with +1% registration lift, aligned with expectations given the lower improvement opportunity on high-intent Brand terms.

The DE test data illustrates the magnitude of the step-change. In the first test week, NB CPA dropped from $1,239 (control) to $323 (OCI) — a 74% reduction. In the second week, the gap widened further: $1,033 to $262, a 75% reduction. This is not incremental improvement. It is a fundamental shift in bidding efficiency (see Appendix: DE Test vs. Control Data).

## Why did UK and DE underperform the US?

UK performance was slightly below US due to EU DMA privacy restrictions limiting the data signals available to the bidding algorithm. DE was further impacted by privacy-driven variability in OCI values and higher cost-per-clicks (+27% vs. UK), which constrained efficient volume capture at scale. These learnings directly inform the EU4 rollout — we are building longer stabilization windows into markets with DMA-driven data restrictions.

## How does OCI connect to competitive strategy?

OCI's efficiency gains are strategically critical because they offset competitive pressure. In the US, Walmart Business has driven Brand CPA from approximately $40 to $65-77. Rather than escalating bids, we absorb the Brand CPA increase through NB efficiency gains from OCI, keeping total program CPA healthy. This is a sustainable competitive response because it is based on algorithmic improvement, not budget escalation.

## How are we scaling in 2026?

Five markets are in progress: CA, JP, FR, IT, and ES. Tech-readiness is complete in Q1 2026. All five launched E2E testing in February-March 2026, with full impact projected by July 2026. The phased implementation and measurement framework developed in 2025 is the standard playbook for each new market. The privacy-related learnings from DE are directly informing milestone timelines for EU4 markets, with longer stabilization windows built in.

## What are the risks and open questions?

Duplicate hvocijid parameters are appearing in landing page URLs across EU3 and existing markets, causing "Duplicate query param found" errors in event processing. JP is not affected. This is under investigation with MarTech (Joel Mallory). If unresolved, it could degrade OCI signal quality in affected markets and delay the measurement validation phase for EU4.

The DMA privacy constraints that reduced DE performance to 86% of expectation will apply to FR, IT, and ES as well. The longer stabilization windows mitigate this, but we should expect EU4 markets to track closer to DE's 86% than the US's 96%.

## Cross-functional partners

MarTech (Joel Mallory) built the OCI implementation infrastructure and is investigating the hvocijid issue. Data Science (Yogesh) developed the OCI value framework and incrementality modeling. Legal approved the conversion data flow to Google. Google (Mike Babich) provides biweekly sync on OCI performance, learning phases, and account structure. Adobe (Suzane Huynh) manages the OCI reporting feed and supported the transition from Adobe bidding.

---

## Appendix

### Appendix A: Performance lift by market

| Market | Test Period | Reg Lift | NB CPA Improvement | Estimated Regs | Estimated OPS | % to Expectation |
|--------|-----------|----------|---------------------|----------------|---------------|------------------|
| US | Jul-Nov 2025 | +24% | ~50% | +32,047 | $16.7MM | 96% |
| UK | Aug-Oct 2025 | +23% | Significant | +2,400 | — | 94% |
| DE | Oct-Dec 2025 | +18% | Significant | +749 | — | 86% |
| **Total** | | | | **+35,196** | **$16.7MM+** | |

The US carried the vast majority of volume and OPS impact, which is expected given market size. UK and DE validated that OCI works in privacy-constrained EU environments, albeit at lower efficiency.

### Appendix B: DE test vs. control data (from WBR)

| Week | Segment | Cost | Regs | ROAS | CPA |
|------|---------|------|------|------|-----|
| W44 | NB Control | $44,592 | 36 | 3% | $1,239 |
| W44 | NB Test (OCI) | $64,565 | 200 | 13% | $323 |
| W44 | Difference | +45% | +456% | +333% | -74% |
| W45 | NB Control | $56,790 | 55 | 3% | $1,033 |
| W45 | NB Test (OCI) | $66,182 | 253 | 13% | $262 |
| W45 | Difference | +17% | +360% | +333% | -75% |

The control group's CPA ranged from $1,033 to $1,239 while OCI held between $262 and $323. The OCI group spent more in absolute terms but generated 4-5x the registrations, demonstrating that the algorithm efficiently allocated incremental budget toward converting queries.

### Appendix C: 2026 RoW expansion timeline

| Market | Status | Launch Date | Full Impact (Projected) |
|--------|--------|-------------|-------------------------|
| CA | In Progress | Mar 2026 (E2E 3/4) | Jul 2026 |
| JP | In Progress | Feb 2026 (E2E 2/26) | Jul 2026 |
| FR | In Progress | Feb 2026 (E2E 2/26) | Jul 2026 |
| IT | In Progress | Feb 2026 (E2E 2/26) | Jul 2026 |
| ES | In Progress | Feb 2026 (E2E 2/26) | Jul 2026 |

All five markets target full impact by July 2026. CA launched E2E testing slightly later (March 4) due to a separate tech dependency.

<!-- AGENT_CONTEXT
machine_summary: "OCI bidding workstream: first non-retail Amazon BU to implement Offline Conversion Import. US +24% reg lift, $16.7MM OPS, 96% to expectation. UK +23%, DE +18%. Total +35,196 incremental regs. DE test showed NB CPA drop from $1,239 to $323 (W44). EU DMA privacy constraints reduced DE to 86% of expectation — informs EU4 rollout with longer stabilization windows. Competitive context: OCI NB efficiency absorbs Walmart-driven Brand CPA inflation ($40→$65-77). 2026: 5 markets (CA/JP/FR/IT/ES) in E2E testing, full impact by Jul 2026. Risk: duplicate hvocijid parameters under investigation with MarTech."
key_entities: ["OCI", "MarTech", "Joel Mallory", "Yogesh", "Mike Babich", "Suzane Huynh", "DMA", "hvocijid", "Walmart Business"]
action_verbs: ["implement", "validate", "scale", "absorb", "investigate"]
update_triggers: ["EU4 market OCI results available", "hvocijid investigation resolved", "CA/JP E2E results", "DMA policy changes affecting OCI signal quality"]
-->
