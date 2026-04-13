---
title: "Paid Search Testing Approach & Year Ahead"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0508 | duck_id: wiki-testing-approach-kate -->

---
title: "Paid Search Testing Approach & Year Ahead"
slug: "kate-doc-synthesis"
type: "playbook"
audience: "org"
status: "draft"
doc-type: strategy
created: "2026-03-25"
updated: "2026-04-05"
owner: "Richard Williams"
tags: ["testing", "strategy", "OP1", "paid-search", "kate-doc", "synthesis"]
depends_on: ["kate-doc-methodology", "kate-doc-oci", "kate-doc-modern-search", "kate-doc-audiences", "kate-doc-ux", "kate-doc-algo-ads", "kate-doc-team-map", "kate-doc-operations"]
summary: "PS testing methodology, 2025 results (+35K regs, $16.7MM OPS), and 2026 roadmap for Kate Rundell's April 16 review."
---

# Paid Search Testing Approach & Year Ahead

*Prepared for Kate Rundell — April 16, 2026*

---

In 2025, the Paid Search team's testing methodology delivered +35,196 incremental registrations and $16.7MM+ in OPS across US, UK, and DE — while building five compounding workstreams now ready to scale worldwide. The 2026 roadmap: expand OCI bidding to five additional markets (full impact by July), launch Project Baloo to unlock Shopping Ads for AB, and extend PS into lifecycle engagement through the F90 program. Every 2026 investment maps to a validated 2025 result.

This document provides the evidence base for OP1 planning — the validated 2025 results that inform where to invest in 2026 and why.

---

## How We Test

The PS team follows a four-stage methodology — hypothesis and baseline, phased rollout, matched measurement, scale or stop — applied consistently across all workstreams. A 2023 Synthetic Regional Test established that 82-92% of Non-Brand registrations are incremental (p<0.001), confirming the channel's value. When the Gated Guest experiment showed -61% registrations after four weeks, the team paused, diagnosed the failure, and pivoted to in-context registration — the results are detailed in Workstream 4 below. The full methodology is detailed in the appendix.

---

## Workstream 1: Intelligent Bidding (OCI)

The PS team partnered with MarTech, Data Science, and Legal to implement OCI as the first non-retail business unit at Amazon.

OCI delivered double-digit registration uplift in every market tested. The US saw +24% lift with 32,047 incremental registrations and $16.7MM in OPS. The UK followed at +23% and DE at +18%, totaling 35,196 incremental registrations across three markets (see Appendix: OCI Validated Results for the full market breakdown). The efficiency gains are strategically critical because they offset competitive pressure — in the US, Walmart Business has driven Brand CPA from ~$40 to $65-77, and we absorb that increase through NB efficiency gains from OCI rather than escalating bids.

**2026:** FR, IT, ES, and JP reached 100% OCI deployment in late March 2026. CA reached full deployment on April 7. Full monthly registration impact across all five expansion markets is expected by July. Privacy-related learnings from DE (DMA restrictions) are directly informing longer stabilization windows for EU4 markets.

---

## Workstream 2: Modern Search

The team consolidated device-specific campaigns and keyword themes to strengthen data signals for OCI bidding. The AB Sole Proprietor Experience study (Aug 2025) revealed that 50% of Sole Proprietors believed Amazon Business required bulk purchasing and was not free — our existing ads reinforced both misconceptions. We shifted to price, quality, selection messaging.

In the UK Phase 1 test (Jan 29 – Mar 2, 2026), the research-driven ads drove 358 registrations versus 273 in the prior period — a 31% increase despite 25% fewer impressions. CTR improved from 14% to 24%, and the test-versus-control CTR improvement was +86%. Confidence: HIGH.

**2026:** EU4 translations completed via GlobalLink. Phased rollout across all non-brand campaigns. Campaign consolidation continuing as part of OCI RoW rollout — structural prep for AI Max testing.

---

## Workstream 3: Audiences

The team extended Paid Search beyond acquisition into customer engagement, partnering with ABMA to boost Google's B2B customer match rate from 13% to 30% through Associated Accounts integration. The Engagement channel drove $765K in iOPS in 2025. During Prime Day 2025, Engagement campaigns generated $329K in OPS at 644% ROAS — a 12x improvement over the prior year.

**2026:** F90 Lifecycle Engagement — targeting recently acquired, non-purchasing customers to complete 3+ purchases. Goal: increase non-SHuMA 3+ purchase rate from 31.7% to 35.4% (+366 bps). US LiveRamp 1P positive targeting approval is on track for April. RoW expansion remains blocked pending Tumble service requirements. This extends Paid Search's role from acquisition into activation.

---

## Workstream 4: User Experience

In the previous experience, 85% of paid search customers dropped off at the MCS landing page before starting registration. The in-context registration pivot delivered +13.6K annualized incremental registrations with 100% probability (APT). In CA, mobile-first LP optimizations drove Bulk CVR from 0.82% to 2.35% (+187%).

**2026:** Project Baloo — unauthenticated access on a dedicated subdomain allowing users to explore the AB catalog before registration. Baloo also unlocks Shopping Ads for AB. US launch Q2 2026. Additional investments: EU5 LP framework (from CA methodology), Guest auto-expiration reduction, BIOAB in-context registration, and Project Aladdin (registration + checkout merge, Q4).

---

## Workstream 5: Algorithmic Ads

Demand Gen ads drove cost-efficient traffic at $0.39 CPC vs. $2.43 for keyword campaigns (-84%). In Q4 2025, DG achieved +53% YoY traffic growth despite -35% YoY spend decrease. Prime Day 2025 results are detailed in Workstream 3.

**2026:** DG Video expansion (early CPCs at $0.30, in line with image). AI Max US test planned Q2 2026 — Google's next evolution in campaign intelligence. The team is applying the same measurement discipline used for OCI: clear baselines, phased rollout, incrementality benchmarks, and guardrails against cannibalization.

---

## Challenges and Risks

JP is -47.5% vs OP2 after the MHLW campaign ended on 1/31, removing a significant registration tailwind. DE missed OP2 by 4%, driven by a high Y25 baseline that compressed the growth rate. F90 US LiveRamp 1P positive targeting is on track for April approval, but RoW expansion remains blocked pending Tumble service requirements. The OCI RoW rollout has a known technical issue: hvocijid duplicate parameters affecting EU3 and existing markets are under investigation. Each of these has a defined mitigation path, but none is resolved yet.

---

## The Team

Brandon Munday's seven-person team delivers five concurrent strategic workstreams across 10 markets while maintaining 25-30 hours per week of operational work, partnering with 12+ cross-functional groups including Google, MarTech, Legal, Data Science, and ABMA. The ratio of strategic to operational capacity is the binding constraint on simultaneous initiatives. The full team roster, scope descriptions, and operational cadence are in the appendix.

---

## 2026 Investment Summary

Every 2026 investment maps to a validated 2025 signal:

| Workstream | 2025 Validated Signal | 2026 Investment | Expected Impact |
|---|---|---|---|
| OCI Bidding | US +24% reg uplift; ~50% NB CPA improvement | Scale to FR, IT, ES, CA, JP (Jul 2026) | Replicate double-digit reg uplift in RoW |
| Modern Search | +86% CTR / +31% regs; consolidation improved data density | WW consolidation; EU5 ad copy rollout; AI Max prep | Stronger OCI signals; campaign count reduction |
| Audiences | $765K iOPS; 30% match rate; Engagement proven | F90 Lifecycle Engagement launch | +366 bps in non-SHuMA 3+ purchase rate |
| User Experience | +13.6K annualized regs; +187% CVR (CA Bulk) | Baloo (US Q2); EU5 LP framework; Aladdin (Q4) | Shopping Ads unlock; friction-free engagement |
| Algorithmic Ads | $0.39 DG CPC; +53% YoY traffic; 644% ROAS | DG Video; AI Max US test; BSE scaling | Scalable mid-funnel at proven efficiency |

Every row traces a direct line from a 2025 validated result to a 2026 investment — the team is not proposing new bets, but scaling proven ones.

These workstreams compound: campaign consolidation strengthens OCI signals, OCI enables smarter bidding on the audiences the Engagement channel reaches, and Baloo creates the friction-free landing experience that AI Max's dynamic page selection requires.

The risk of not investing: OCI-eligible markets remain on deprecated Adobe bidding with no CPA improvement path, Baloo delays leave Shopping Ads unavailable for AB while competitors access them, and the Engagement infrastructure built in 2025 sits underutilized without F90 activation.

---

## Appendix

### OCI Validated Results

| Market | Reg Lift | NB CPA Improvement | Estimated Regs | Estimated OPS |
|--------|----------|---------------------|----------------|---------------|
| US | +24% | ~50% | +32,047 | $16.7MM |
| UK | +23% | Significant | +2,400 | Not yet isolated |
| DE | +18% | Significant | +749 | Not yet isolated |
| **Total** | | | **+35,196** | **$16.7MM+** |

OCI delivers double-digit registration uplift in every market tested, with the US driving the largest absolute impact at 32,047 incremental registrations and $16.7MM in OPS. UK and DE confirm the pattern holds across geographies, with the efficiency gains offsetting competitive CPA pressure in each market.

### Testing Methodology: Four-Stage Detail

**1. Hypothesis and Baseline.** Every test starts with a measurable claim. We establish baselines using prior-quarter data with seasonality adjustments so we can isolate the effect of the change from background noise. For channel-level incrementality, we use Synthetic Regional Testing (SyRT). Our Q2 2023 SyRT established that 82-92% of Non-Brand registrations are incremental (US NB: +16.4% lift, p<0.001), confirming the channel's value and informing budget allocation.

**2. Phased Rollout.** We do not make big-bang changes. OCI launched at the keyword level, scaled to 25%, then 50%, then 100% of campaigns. Each phase has a measurement window and a go/no-go decision. This approach was validated in the US and has become the standard playbook for every subsequent market.

**3. Measurement Framework.** We match the measurement approach to the test type: seasonality-adjusted baselines for OCI, test/control splits for ad copy, pre/post causal analysis for landing pages, Weblab (APT) for structural UX changes, and Bayesian PPR for bid modifiers. We explicitly state confidence levels — HIGH when volume and duration support conclusions, LOW when they do not.

**4. Scale or Stop.** If a test validates, we scale it. If it does not, we document the learning and move on. The Gated Guest experiment showed -61% registrations after 4 weeks — we paused it, deep-dived the data, and pivoted to in-context registration, which delivered +13.6K annualized incremental registrations with 100% probability (APT).

This methodology is not unique to Paid Search. What is distinctive is how the PS team applies it across five concurrent workstreams, 10 markets, and multiple cross-functional partnerships simultaneously.

### Team Roster

| Name | Level | Primary Focus |
|------|-------|---------------|
| Brandon Munday | L7 | WW Head — strategy, stakeholder management |
| Stacey Gu | L6 | OCI/Bidding, US performance |
| Dwayne Palmer | L6 | WW Marketing Website (MCS) |
| Yun-Kang Chu | L6 | Modern Search, Adobe, MX |
| Andrew Wirtz | L5 | DG/Algorithmic Ads, EU5 |
| Aditya Thakur | L5 | Landing Pages/UX, CA, JP |
| Richard Williams | L5 | AU/MX, WW testing, competitive intel |

### What we do within Paid Search

The core function is Google Ads campaign management across 10 markets, which includes OCI bidding implementation, keyword and bid strategy, ad copy testing, campaign consolidation, and competitive monitoring. The team also owns budget management, invoice and PO coordination, and performance reporting across WBR, MBR, QBR, and Flash cadences.

### What we also do beyond Paid Search

The team's scope extends into Engagement channel management through Demand Gen and LiveRamp audiences, F90 lifecycle program design, Mobile App acquisition, and landing page UX strategy including Polaris and Baloo. We also drive cross-team measurement advocacy (SyRT, OCI framework), Adobe analytics coordination, international market consulting for AU and MX, event strategy, and AI/automation exploration.

### Operational Backbone

The strategic work runs on a consistent operational foundation. The team monitors campaigns daily across 10 markets — spend pacing, CPA checks, bid strategy health, disapproved ads, and keyword alerts. Weekly cadence includes WBR callout preparation, market-specific performance reviews, the team's Deep Dive & Debate sync, and stakeholder syncs for AU and MX. Biweekly, the team runs Google performance syncs, Adobe analytics syncs, and MX coordination. Monthly work covers budget management through R&O, invoice and PO coordination, Kingpin Goal updates, MBR narratives, competitive monitoring, and Flash contributions.

This operational discipline is what enables the team to run five concurrent strategic workstreams across 10 markets. The strategic work gets the headlines. The operational work makes the strategic work possible. Both are delivered by the same seven-person team.

### Supporting Data

Full supporting data tables, competitive intelligence, market performance, cross-team contact lists, and source documents are available in the companion appendix document.

<!-- AGENT_CONTEXT
machine_summary: "Flagship synthesis doc for Kate Rundell (Apr 16, 2026). V5 revision — applied appendix-heavy structure rule: moved OCI results table from Workstream 1 main body to Appendix: OCI Validated Results, replaced with prose embedding headline numbers. Investment Summary table retained in main body as decision artifact (exception per rule). PS team testing methodology across 5 workstreams: OCI Bidding (+35,196 regs, $16.7MM+ OPS, scaling to 5 RoW markets by Jul 2026), Modern Search (+86% CTR test-vs-control, +31% regs), Audiences ($765K iOPS, F90 lifecycle launch), User Experience (+13.6K annualized regs, Project Baloo US Q2), Algorithmic Ads ($0.39 DG CPC, AI Max US test Q2). Core argument: every 2026 investment maps to a validated 2025 result. Workstreams compound. 7-person team, 10 markets, 12+ cross-functional partners."
key_entities: ["Kate Rundell", "OCI", "Baloo", "F90", "AI Max", "SyRT", "Demand Gen", "Polaris", "Walmart", "LiveRamp", "ABMA", "MarTech"]
action_verbs: ["validate", "scale", "compound", "invest", "test"]
word_count_target: 1300
appendix_companion: true
depends_on: ["kate-doc-methodology", "kate-doc-oci", "kate-doc-modern-search", "kate-doc-audiences", "kate-doc-ux", "kate-doc-algo-ads", "kate-doc-team-map", "kate-doc-operations", "kate-doc-appendix"]
consumed_by: ["Kate Rundell Apr 16 review", "OP1 planning", "OP2 planning", "Todd Heimes PS investment decision"]
update_triggers: ["OCI RoW market status change", "Baloo launch date confirmed", "F90 Legal approval", "AI Max test results", "any workstream data update"]
-->
