---
title: "Paid Search Testing Approach: From Validated Results to Scalable Growth"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0376 | duck_id: research-testing-approach-outline -->

# Paid Search Testing Approach: From Validated Results to Scalable Growth

*Outline for Kate Rundell (L8). Brandon reviewing first. Structure: problem → test → result → scale across 5 workstreams. Strategic narrative — not a status update.*

---

## Opening: The Operating Model

- PS operates on a simple principle: don't scale what you haven't validated. Every 2026 investment maps to a 2025 test result — not a projection, not a hypothesis, a measured outcome.
- The team's role has shifted from channel execution to connective tissue between platform capabilities (Google, Adobe, LiveRamp) and business objectives (registrations, OPS, customer lifecycle). This required cross-functional partnerships with Legal, Data Science, MarTech, MCS, ABMA, and Customer Research.
- The 5 workstreams below are not independent initiatives. They compound — campaign consolidation strengthens OCI signals, OCI enables smarter bidding on the audiences the Engagement channel reaches, and Baloo creates the friction-free landing experience that AI Max's dynamic page selection requires.
- Structure of this doc: for each workstream, what problem we faced, what we tested, what we learned, and what we're investing in for 2026 based on that evidence.

---

## 1. Intelligent Bidding: OCI Implementation and Expansion

- **Problem:** Loss of Google Ads auto-bid strategy and Adobe tracking left the team without a reliable optimization signal. Bidding decisions were disconnected from actual business outcomes (registrations, OPS).
- **What we tested:** Phased OCI rollout — E2E keyword-level testing → 25% → 50% → 100% campaign application — with a measurement framework comparing actualized CPA against a seasonality-adjusted baseline. PS was the first non-retail business unit at Amazon to implement OCI, requiring significant cross-team work with MarTech, Legal, and Data Science.
- **What we learned:** US: +24% registration lift (96% of expectations), UK: +23% (94%), DE: +18% (86%). Non-brand CPA improved -45%, -38%, -37% respectively. Total: +32K incremental registrations, ~$16.7MM in OPS. DE underperformed due to EU DMA privacy restrictions limiting data signals — a learning that directly informs EU4 rollout timelines.
- **2026 investment:** Scaling OCI to CA, JP, FR, IT, ES with tech-readiness complete Q1 2026 and full monthly impact expected by July. The phased implementation and measurement framework is now the standard playbook. Privacy learnings from DE are built into longer stabilization windows for EU4 markets.

---

## 2. Modern Search: Fueling the Algorithm

- **Problem:** Fragmented, device-specific campaigns with narrow keyword themes starved the bidding algorithms of data. Low signal density meant slower learning, weaker optimization, and higher operational complexity.
- **What we tested:** Campaign consolidation (device and keyword theme) across US and EU5 to increase data density per bid strategy. Separately, the team used findings from the AB Sole Proprietor Experience study (Aug 2025) to overhaul ad copy — shifting from bulk/B2B messaging to price, quality, and selection. Tested first in UK and IT.
- **What we learned:** Consolidated structures outperformed fragmented ones in both efficiency and registration volume, even during the OCI transition. UK ad copy test: +86% CTR, +31% registrations vs. original ads. The SP study revealed that 50% of prospects believed AB required bulk purchasing and 31% believed savings wouldn't justify costs — our existing ads were reinforcing both misconceptions.
- **2026 investment:** Continuing keyword theme consolidation WW as part of OCI rollout. EU4 ad copy translations completed via GlobalLink, phased rollout across all non-brand campaigns. This structural simplification is also a prerequisite for AI Max testing — consolidated campaigns are required for the algorithm to function effectively.

---

## 3. Audiences and Lifecycle: Extending PS Beyond Acquisition

- **Problem:** PS operated as a pure top-of-funnel acquisition channel. No mechanism to suppress existing customers (wasted spend) or re-engage non-purchasing registrants (lost value). Google's B2B customer recognition rate was 12-13% — too low for meaningful audience targeting.
- **What we tested:** Three phases. (1) LiveRamp suppression across US and CA to remove current customers from acquisition targeting. (2) Dedicated Engagement account in partnership with Traffic & Onsite Marketing — a net-new channel bridging acquisition and lifecycle. (3) Associated Accounts integration with ABMA to ingest consumer-side emails linked to B2B users, more than doubling audience match rate from 13% to 30%.
- **What we learned:** The Engagement channel drove $765K in iOPS in 2025. Prime Day 2025: 80K clicks at -10% cost YoY, $329K OPS at 644% ROAS (12x improvement over prior year). The audience infrastructure — suppression, engagement, expanded match — is now operational and proven.
- **2026 investment:** F90 (First 90 Days) Lifecycle Engagement. Targets recently acquired, non-purchasing customers to complete 3+ purchases. Goal: increase non-SHuMA 3+ purchase rate from 31.7% to 35.4% (+366 bps YoY). Legal SIMs currently in review for new audiences and audience-transmission solutions. This extends PS from acquisition into activation — a fundamentally different operating model.

---

## 4. User Experience: Landing Page and Conversion Optimization

- **Problem:** 85% of paid search traffic dropped off at the MCS landing page before starting registration. An additional 60% dropped at registration start. Customers who completed registration had to manually re-search for products they'd already found on Google. The landing page was the single largest source of funnel leakage.
- **What we tested:** Migrated from siloed MCS pages to a standardized architecture. Tested "Percolate" and "Guest" flows (value-first engagement before registration). Guest showed -61% registrations and was paused. Pivoted to in-context registration on MCS pages — updated CTA from "Create a free account" to "Start browsing," capturing email directly on the landing page. In CA, diagnosed mobile-specific friction (cropped hero images, non-localized headlines) and applied pre/post causal analysis.
- **What we learned:** In-context registration: +13.6K annualized incremental registrations at 100% probability (APT). CA: Bulk CVR +186.6% (0.82% → 2.35%), Wholesale CVR +180.0% (0.75% → 2.10%). The Guest failure taught us that transparency alone doesn't convert — the registration moment needs to be embedded in the product experience, not gated before it.
- **2026 investment:** Project Baloo (US Q2) — unauthenticated product access on a dedicated subdomain, friction-free engagement from Google to AB catalog. Unlocks Shopping Ads for AB (unlimited results vs. current text ad constraints). EU5 LP framework rollout using CA's validated methodology. Additional: Guest auto-expiration reduction (12mo → 3mo), in-context registration from BIOAB placement, and Project Aladdin (Q4) merging registration and checkout into a unified journey.

---

## 5. Algorithmic Ads: Demand Gen and Incremental Growth

- **Problem:** PS was entirely keyword-dependent — no visual ad formats, no mid-funnel presence, no mechanism to reach customers outside of active search behavior. The channel had no answer for demand generation or brand awareness at scale.
- **What we tested:** Launched Discovery Ads (2023), iterated through Google's transition to Demand Gen. Incorporated LiveRamp targeting for existing customer audiences. Tested DG image placements for Business Essentials. Expanded DG investment in Q4 2025 with a focus on CPC efficiency.
- **What we learned:** DG CPC: $0.39 vs. $2.43 for keyword campaigns in the Engagement account. Q4 2025: +53% YoY traffic growth despite -35% YoY spend decrease, CPC improved -58% YoY. Prime Day: 644% ROAS. BSE: 52K visitors in first year at $0.30 CPC. Visual ad formats are a proven, scalable, cost-efficient channel for qualified traffic.
- **2026 investment:** DG Video expansion (early testing shows video CPCs matching image at $0.30). AI Max US test — Google's next evolution in campaign intelligence (expanded keyword matching, dynamic LP selection, enhanced audience signals). Applying the same measurement discipline as OCI: clear baselines, phased rollout, incrementality benchmarks before scaling. Collaboration with other Amazon teams and Google vendors to ensure AI Max doesn't cannibalize existing PS performance.

---

## Closing: The Compound Effect

- These workstreams are not a portfolio of independent projects. They are a compound system — each validated result creates the conditions for the next test to succeed.
- Campaign consolidation (Modern Search) strengthens the data signals that OCI (Bidding) needs to optimize. OCI enables smarter bidding on the audiences that the Engagement channel (Audiences) reaches. Baloo (UX) creates the friction-free landing experience that AI Max's (Algorithmic Ads) dynamic page selection requires.
- The team is transforming Paid Search from a keyword-driven acquisition channel into an automated, audience-centric engine — grounded not in speculation, but in the cumulative evidence of the past year's validated results.
- 2026 is not a pivot. It's the natural next step of a testing methodology that has been compounding since 2024.

---

## Appendix: 2026 Investment Summary

- Summary table mapping each workstream: 2025 validated signal → 2026 investment → expected impact
- Cross-functional partner acknowledgments (MarTech, Legal, Data Science, MCS, ABMA, Customer Research, international market teams)
- Measurement framework overview (phased rollout methodology, baseline construction, confidence levels)

---

*Draft outline. Next step: Brandon review, then fill sections with full narrative.*
