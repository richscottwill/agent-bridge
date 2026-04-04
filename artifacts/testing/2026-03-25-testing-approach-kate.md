---
title: "Paid Search Testing Approach & Year Ahead"
slug: "kate-doc-synthesis"
type: "playbook"
audience: "org"
status: "draft"
doc-type: strategy
created: "2026-03-25"
updated: "2026-03-25"
owner: "Richard Williams"
tags: ["testing", "strategy", "OP1", "paid-search", "kate-doc", "synthesis"]
depends_on: ["kate-doc-methodology", "kate-doc-oci", "kate-doc-modern-search", "kate-doc-audiences", "kate-doc-ux", "kate-doc-algo-ads", "kate-doc-team-map", "kate-doc-operations"]
summary: "Complete PS testing methodology, 2025 results, 2026 roadmap, team scope, and operations for Kate Rundell's April 16 review."
---

# Paid Search Testing Approach & Year Ahead

*Prepared for Kate Rundell — April 16, 2026*

---

In 2025, the Paid Search team's testing methodology delivered +35,196 incremental registrations and $16.7MM+ in OPS across US, UK, and DE — while building five compounding workstreams now ready to scale worldwide. The 2026 roadmap: expand OCI bidding to five additional markets (full impact by July), launch Project Baloo to unlock Shopping Ads for AB, and extend PS into lifecycle engagement through the F90 program. Every 2026 investment maps to a validated 2025 result.

The team is transforming Paid Search from a keyword-driven acquisition channel into an automated, audience-centric engine — grounded in evidence rather than speculation. Each section below covers one workstream: what we tested, what we learned, and how the validated results directly inform 2026 investment. Cross-functional collaboration spanning Legal, Data Science, MarTech, MCS, ABMA, Customer Research, and international market teams was required for every initiative, with the PS team serving as the connective tissue between platform capabilities and business objectives.

---

## How We Test

The PS team follows a consistent methodology across all workstreams: identify a problem, design a controlled test, validate the result, then scale what works. The methodology has four stages:

**1. Hypothesis and Baseline.** Every test starts with a measurable claim. We establish baselines using prior-quarter data with seasonality adjustments so we can isolate the effect of the change from background noise. For channel-level incrementality, we use Synthetic Regional Testing (SyRT). Our Q2 2023 SyRT established that 82-92% of Non-Brand registrations are incremental (US NB: +16.4% lift, p<0.001), confirming the channel's value and informing budget allocation.

**2. Phased Rollout.** We do not make big-bang changes. OCI launched at the keyword level, scaled to 25%, then 50%, then 100% of campaigns. Each phase has a measurement window and a go/no-go decision. This approach was validated in the US and has become the standard playbook for every subsequent market.

**3. Measurement Framework.** We match the measurement approach to the test type: seasonality-adjusted baselines for OCI, test/control splits for ad copy, pre/post causal analysis for landing pages, Weblab (APT) for structural UX changes, and Bayesian PPR for bid modifiers. We explicitly state confidence levels — HIGH when volume and duration support conclusions, LOW when they do not.

**4. Scale or Stop.** If a test validates, we scale it. If it does not, we document the learning and move on. The Gated Guest experiment showed -61% registrations after 4 weeks — we paused it, deep-dived the data, and pivoted to in-context registration, which delivered +13.6K annualized incremental registrations with 100% probability (APT). Failures are data, not setbacks.

This methodology is not unique to Paid Search. What is distinctive is how the PS team applies it across five concurrent workstreams, 10 markets, and multiple cross-functional partnerships simultaneously.

---

## Workstream 1: Intelligent Bidding (OCI)

*Progression: Loss of Google Ads auto-bid strategy and Adobe → OCI success and expansion*

The Paid Search team partnered with MarTech to implement OCI as the first non-retail business unit at Amazon. This required defining the OCI value framework with Data Science, ensuring Legal approved the data flow, building the tracking infrastructure with MarTech, and validating the underlying data.

**Results:**

| Market | Reg Lift | NB CPA Improvement | Estimated Regs | Estimated OPS |
|--------|----------|---------------------|----------------|---------------|
| US | +24% | ~50% | +32,047 | $16.7MM |
| UK | +23% | Significant | +2,400 | — |
| DE | +18% | Significant | +749 | — |
| **Total** | | | **+35,196** | **$16.7MM+** |

OCI's efficiency gains are strategically critical because they offset competitive pressure. In the US, Walmart Business has driven Brand CPA from ~$40 to $65-77. Rather than escalating bids, we absorb the Brand CPA increase through NB efficiency gains from OCI, keeping total program CPA healthy.

**2026:** Scaling to CA, JP, FR, IT, ES with tech-readiness complete in Q1 2026 and full monthly registration impact expected by July. The privacy-related learnings from DE (DMA restrictions) are directly informing longer stabilization windows for EU4 markets.

---

## Workstream 2: Modern Search

*Progression: Fragmented campaigns → Consolidation → Research-Driven Ad Copy → Fueling ML & OCI*

The team consolidated device-specific campaigns and keyword themes to strengthen data signals for OCI bidding, and incorporated learnings from the AB Sole Proprietor Experience study (Aug 2025) to develop evidence-based ad copy.

The study revealed that 50% of Sole Proprietors believed Amazon Business required bulk purchasing and was not free. Our existing ads reinforced both misconceptions. We shifted from bulk/wholesale/B2B messaging to price, quality, selection messaging.

**UK Results (Phase 1, Jan 29 - Mar 2, 2026):**

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Impressions | 37,388 | 28,010 | -25% |
| Clicks | 5,308 | 6,778 | +28% |
| Registrations | 273 | 358 | **+31%** |
| CTR | 14% | 24% | **+70%** |

Pre/post comparison (Dec 27-Jan 28 vs. Jan 29-Mar 2). The test-vs-control CTR improvement over the same period was +86%.

Despite 25% fewer impressions, the new ads drove 31% more registrations. Confidence: HIGH.

**2026:** EU4 translations completed via GlobalLink. Phased rollout across all non-brand campaigns. Campaign consolidation continuing as part of OCI RoW rollout — structural prep for AI Max testing.

---

## Workstream 3: Audiences

*Progression: LiveRamp Suppression → Engagement Account → Associated Accounts → F90 Lifecycle*

The team extended Paid Search beyond acquisition into customer engagement by building a dedicated Engagement account and partnering with ABMA to boost Google's B2B customer match rate from 13% to 30% through Associated Accounts integration.

The Engagement channel drove $765K in iOPS in 2025. During Prime Day 2025, Engagement campaigns generated $329K in OPS at 644% ROAS — a 12x improvement over the prior year.

**2026:** F90 Lifecycle Engagement — targeting recently acquired, non-purchasing customers to complete 3+ purchases. Goal: increase non-SHuMA 3+ purchase rate from 31.7% to 35.4% (+366 bps). Legal is reviewing audience-transmission solutions. This extends Paid Search's role from acquisition into activation.

---

## Workstream 4: User Experience

*Progression: Siloed LPs → Percolate/Guest → In-Context Registration → Polaris → Baloo*

In the previous experience, 85% of paid search customers dropped off at the MCS landing page before starting registration. After the Gated Guest experiment showed -61% registrations, the team paused, deep-dived the data, and pivoted to in-context registration — which delivered +13.6K annualized incremental registrations with 100% probability (APT). In CA, mobile-first LP optimizations drove Bulk CVR from 0.82% to 2.35% (+187%).

**2026:** Project Baloo — unauthenticated access on a dedicated subdomain allowing users to explore the AB catalog before registration. Baloo also unlocks Shopping Ads for AB. US launch Q2 2026. Additional investments: EU5 LP framework (from CA methodology), Guest auto-expiration reduction, BIOAB in-context registration, and Project Aladdin (registration + checkout merge, Q4).

---

## Workstream 5: Algorithmic Ads

*Progression: Discovery Ads → Demand Gen → DG Creative Expansion → AI Max*

Demand Gen ads drove cost-efficient traffic at $0.39 CPC vs. $2.43 for keyword campaigns (-84%). In Q4 2025, DG achieved +53% YoY traffic growth despite -35% YoY spend decrease. During Prime Day 2025, Engagement campaigns delivered 644% ROAS.

**2026:** DG Video expansion (early CPCs at $0.30, in line with image). AI Max US test planned Q2 2026 — Google's next evolution in campaign intelligence. The team is applying the same measurement discipline used for OCI: clear baselines, phased rollout, incrementality benchmarks, and guardrails against cannibalization.

---

## Challenges and Risks

DE missed OP2 by 4%, driven by a high Y25 baseline that compressed the growth rate. JP is -47.5% vs OP2 after the MHLW campaign ended on 1/31, removing a significant registration tailwind. F90 is blocked by Legal SIMs — US LiveRamp 1P positive targeting approval is on track for April, but RoW expansion is blocked pending resolution of Tumble service requirements. The OCI RoW rollout has a known technical issue: hvocijid duplicate parameters affecting EU3 and existing markets are under investigation. Each of these has a defined mitigation path, but none is resolved yet.

---

## 2026 Investment Summary

Every 2026 investment maps to a validated 2025 signal:

| Workstream | 2025 Validated Signal | 2026 Investment | Expected Impact |
|---|---|---|---|
| OCI Bidding | +24% reg uplift; ~50% NB CPA improvement; +35K regs / $16.7MM OPS | Scale to FR, IT, ES, CA, JP (Jul 2026) | Replicate double-digit reg uplift in RoW |
| Modern Search | +86% CTR / +31% regs; consolidation improved data density | WW consolidation; EU5 ad copy rollout; AI Max prep | Stronger OCI signals; campaign count reduction |
| Audiences | $765K iOPS; 30% match rate; Engagement proven | F90 Lifecycle Engagement launch | +366 bps in non-SHuMA 3+ purchase rate |
| User Experience | +13.6K annualized regs; +187% CVR (CA Bulk) | Baloo (US Q2); EU5 LP framework; Aladdin (Q4) | Shopping Ads unlock; friction-free engagement |
| Algorithmic Ads | $0.39 DG CPC; +53% YoY traffic; 644% ROAS | DG Video; AI Max US test; BSE scaling | Scalable mid-funnel at proven efficiency |

These workstreams compound: campaign consolidation strengthens OCI signals, OCI enables smarter bidding on the audiences the Engagement channel reaches, and Baloo creates the friction-free landing experience that AI Max's dynamic page selection requires.

The risk of not investing: OCI-eligible markets remain on deprecated Adobe bidding with no CPA improvement path, Baloo delays leave Shopping Ads unavailable for AB while competitors access them, and the Engagement infrastructure built in 2025 sits underutilized without F90 activation.

These investments directly support the PS team's OP2 registration and OPS commitments — the validated 2025 results provide the evidence base for the 2026 plan.

---

## The Team

Brandon Munday's WW Outbound Marketing team spans seven people across Paid Search, plus Mobile App and Marketing Website functions.

| Name | Level | Primary Focus |
|------|-------|---------------|
| Brandon Munday | L7 | WW Head — strategy, stakeholder management |
| Stacey Gu | L6 | OCI/Bidding, US performance |
| Dwayne Palmer | L6 | WW Marketing Website (MCS) |
| Yun-Kang Chu | L6 | Modern Search, Adobe, MX |
| Andrew Wirtz | L5 | DG/Algorithmic Ads, EU5 |
| Aditya Thakur | L5 | Landing Pages/UX, CA, JP |
| Richard Williams | L5 | AU/MX, WW testing, competitive intel |

The team works with 12+ cross-functional stakeholder groups: Google, Adobe, MCS, MarTech, Legal, Data Science, ABMA, International Expansion (AU, MX), CPS, SSR Activation, Creative, and Brand & Paid Media. Every strategic initiative in this document was enabled by a cross-functional partnership that the PS team initiated or drove.

### What We Do Within Paid Search
Google Ads campaign management across 10 markets. OCI bidding implementation. Keyword and bid strategy. Ad copy testing. Campaign consolidation. Competitive monitoring. Budget management. Invoice/PO coordination. Performance reporting (WBR, MBR, QBR, Flash).

### What We Also Do Beyond Paid Search
Engagement channel (DG, LiveRamp audiences). F90 lifecycle program design. Mobile App acquisition. Landing page UX strategy (Polaris, Baloo). Cross-team measurement advocacy (SyRT, OCI framework). Adobe analytics coordination. International market consulting. Event strategy. AI/automation exploration.

---

## Operational Backbone

The strategic work runs on a consistent operational foundation:

- **Daily:** Campaign monitoring across 10 markets — spend pacing, CPA checks, bid strategy health, disapproved ads, keyword alerts.
- **Weekly:** WBR callout preparation, market-specific performance reviews, team sync (Deep Dive & Debate), stakeholder syncs (AU, MX).
- **Biweekly:** Google performance sync, Adobe analytics sync, MX sync.
- **Monthly:** Budget management (R&O), invoice/PO coordination, Kingpin Goal updates, MBR narratives, competitive monitoring, Flash contributions.

This operational discipline is what enables the team to run five concurrent strategic workstreams across 10 markets. The strategic work gets the headlines. The operational work makes the strategic work possible. Both are delivered by the same seven-person team, which spends approximately 25-30 hours per week on operational work — monitoring, reporting, budget management, and stakeholder coordination across 10 markets. The remaining capacity funds the five strategic workstreams.

---

## Appendix

Full supporting data tables, competitive intelligence, market performance, cross-team contact lists, and source documents are available in the companion appendix document.

<!-- AGENT_CONTEXT
machine_summary: "Flagship synthesis doc for Kate Rundell (Apr 16, 2026). PS team testing methodology across 5 workstreams: OCI Bidding (+35,196 regs, $16.7MM+ OPS, scaling to 5 RoW markets by Jul 2026), Modern Search (+86% CTR test-vs-control, +31% regs from research-driven ad copy), Audiences ($765K iOPS, match rate 13% to 30%, F90 lifecycle launch), User Experience (+13.6K annualized regs from in-context, Project Baloo US Q2), Algorithmic Ads ($0.39 DG CPC, AI Max US test Q2). Core argument: every 2026 investment maps to a validated 2025 result. Workstreams compound -- consolidation feeds OCI, OCI feeds audience bidding, Baloo feeds AI Max. 7-person team, 10 markets, 12+ cross-functional partners."
key_entities: ["Kate Rundell", "OCI", "Baloo", "F90", "AI Max", "SyRT", "Demand Gen", "Polaris", "Walmart", "LiveRamp", "ABMA", "MarTech"]
action_verbs: ["validate", "scale", "compound", "invest", "test"]
depends_on: ["kate-doc-methodology", "kate-doc-oci", "kate-doc-modern-search", "kate-doc-audiences", "kate-doc-ux", "kate-doc-algo-ads", "kate-doc-team-map", "kate-doc-operations", "kate-doc-appendix"]
consumed_by: ["Kate Rundell Apr 16 review", "OP2 planning", "Todd Heimes PS investment decision"]
update_triggers: ["OCI RoW market status change", "Baloo launch date confirmed", "F90 Legal approval", "AI Max test results", "any workstream data update"]
-->
