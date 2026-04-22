---
title: "Team Map & Cross-Functional Scope"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0408 | duck_id: testing-ps-team-map -->

---
title: "Team Map & Cross-Functional Scope"
slug: "kate-doc-team-map"
type: "reference"
audience: "org"
status: "draft"
created: "2026-03-25"
updated: "2026-03-25"
owner: "Richard Williams"
tags: ["team", "cross-functional", "scope", "kate-doc"]
summary: "PS team structure, individual ownership areas, and exhaustive map of PS vs. beyond-PS work."
---

# Team Map & Cross-Functional Scope

The Paid Search team operates as connective tissue between platform capabilities and business objectives. This section maps who does what, which stakeholders we serve, and the full scope of work — both within Paid Search and beyond it.

## The Team

Brandon Munday's WW Outbound Marketing team includes Paid Search, Mobile App, and Marketing Website. The Paid Search function spans seven people across three locations.

| Name | Level | Location | Primary Focus | Markets |
|------|-------|----------|---------------|---------|
| Brandon Munday | L7 | Austin | WW Head of Outbound Marketing — strategy, stakeholder management, team leadership | All |
| Stacey Gu | L6 | Seattle | OCI/Bidding strategy, US performance management, Paid Acq Testing | US, WW (OCI) |
| Dwayne Palmer | L6 | Arlington | WW Head of Marketing Website (MCS) — LP optimization, Polaris, Weblab testing | All (MCS) |
| Yun-Kang Chu | L6 | Austin | Modern Search structure, Adobe analytics, MX Paid Search | MX, US, EU5 |
| Andrew Wirtz | L5 | Seattle | Demand Gen/Algorithmic Ads, EU performance, Flash communications | EU5, US |
| Aditya Thakur | L5 | Austin | Landing Pages/UX, CA LP framework, JP testing | CA, JP |
| Richard Williams | L5 | Seattle | AU/MX hands-on management, WW testing methodology, competitive intel | AU, MX, WW |

Peter Ocampo (L6, Seattle) leads the Global AB Mobile App program — a separate function under Brandon that coordinates with PS on paid app acquisition and measurement.

## Stakeholder Interaction Map

The PS team works with at least 12 distinct stakeholder groups. The table below shows which team members are the primary interface for each.

| Stakeholder | Primary PS Contact | Interaction Cadence | Key Topics | Key Outcome |
|-------------|-------------------|---------------------|------------|-------------|
| Google (Mike Babich) | Brandon, Stacey, Richard | Biweekly sync | OCI, AI Max, account structure, ad copy | OCI implementation (first non-retail BU at Amazon), AI Max test planning |
| Adobe (Suzane Huynh, Jen Vitiello) | Yun, Richard | Biweekly sync | OCI reporting, Ad Cloud analytics, WW redirects | OCI reporting feed integration, AU OCI timeline TBD |
| MCS (Dwayne's team) | Dwayne, Adi, Richard | Continuous | LP optimization, Polaris, Weblab, in-context reg | In-context registration +13.6K regs, Polaris WW rollout |
| MarTech (Joel Mallory) | Stacey, Yun | As needed | OCI infrastructure, tracking, LiveRamp | OCI technical implementation across 8 markets |
| Legal | Brandon | As needed | F90 audiences, LiveRamp data usage, audience SIMs | F90 audience approval in progress (US by end of April) |
| Data Science (Yogesh) | Stacey | As needed | OCI value framework, incrementality modeling | OCI measurement framework adopted as rollout standard |
| ABMA (Naresh, Nishchhal) | Stacey, Richard | As needed | Associated Accounts, audience match rates | Match rate 13% → 30%, enabling $765K iOPS Engagement channel |
| AU (Lena Zak, Alexis Eck) | Richard | Weekly sync | AU PS strategy, CPC optimization, Polaris migration | Full Polaris migration, keyword CPA optimization framework |
| MX (Lorena Alvarez Larrea) | Richard, Yun | Biweekly sync | MX campaign management, keyword strategy | +68% vs OP2 (Mar projection), LP optimization |
| CPS (Kevin Townsend) | Adi | As needed | LP coordination, CPS-heavy markets (JP) | JP testing methodology, cross-channel LP alignment |
| SSR Activation (Saajan Chowhan) | Richard | Weekly OHs | F90 lifecycle, promo strategy | F90 program design, promo coordination |
| Creative (Raven Smith) | Andrew | As needed | DG video assets, BSE creative, ad copy | DG video launch, BSE 52K visitors, ad copy creative |
| Brand & Paid Media (Robert Skenes) | Brandon | Monthly flash | LiveRamp 1P, ADSP coordination, measurement | LiveRamp 1P targeting coordination for F90 |

**So what:** Every strategic initiative in this document required at least one cross-functional partnership that the PS team initiated or drove. OCI required MarTech and Google. The Engagement channel required ABMA. Ad copy required Customer Research. Landing pages required MCS. The "Key Outcome" column shows this is not coordination overhead — it is how the team delivers results.

## What We Do for Paid Search

This is the core function — the work that directly drives registrations and OPS through search engine advertising.

| Category | Activities | Owner(s) |
|----------|-----------|----------|
| **Campaign Management** | Google Ads management across 10 markets (US, UK, DE, FR, IT, ES, CA, JP, AU, MX). Keyword strategy (Brand, NB, Product, Vertical). Bid strategy management (tROAS, manual CPC, bid caps). Campaign structure optimization. | Stacey (US), Andrew (EU5), Yun (MX, Modern Search), Richard (AU, MX), Adi (CA, JP) |
| **OCI Bidding** | Implementation, phased rollout, measurement framework, market-by-market optimization. First non-retail BU at Amazon to implement OCI. | Stacey (lead), Richard (measurement), all (market execution) |
| **Testing & Measurement** | Test design, hypothesis development, measurement frameworks (SyRT, pre/post, Weblab/APT, Bayesian PPR). Confidence assessment. Scale-or-stop decisions. | Richard (methodology), all (execution) |
| **Ad Copy Optimization** | Research-driven messaging (SP study), test/control splits, phased rollout, WW translations. | Yun (Modern Search), Richard (testing), Andrew (EU5) |
| **Competitive Monitoring** | Auction insights review, IS tracking, CPC trend analysis, competitor response strategy. | Richard (analysis), Andrew (EU5 monitoring) |
| **Budget & Pacing** | Budget management, R&O input, spend pacing, budget confirmations across markets. | Andrew (EU5), Richard (AU, MX), Stacey (US) |
| **Invoicing & POs** | Google Ads invoicing for AU and MX, PO matching, OFA approvals, finance coordination. | Richard (AU, MX) |
| **Reporting** | WBR callouts, MBR narratives, QBR trends, Paid Acquisition Flash (bimonthly). | Andrew (Flash author), Richard (WBR coverage), all (market callouts) |
| **Microsoft Advertising** | Account management, triage (10x paused account emails in W12). | Richard |

## What We Also Do Beyond Paid Search

This is the work that extends the team's impact beyond the search engine advertising channel — cross-functional partnerships, lifecycle strategy, and platform innovation.

| Category | Activities | Partners |
|----------|-----------|----------|
| **Engagement Channel** | Demand Gen campaigns, LiveRamp audience targeting, Business Essentials traffic, Prime Day/BFCM event campaigns. Bridges acquisition and lifecycle. | ABMA, Traffic & Onsite Marketing, Creative |
| **F90 Lifecycle Program** | Designing PS-driven activation for non-purchasing customers within 90 days of registration. Extends PS into post-acquisition. | Legal, SSR Activation, ABMA |
| **Mobile App Acquisition** | Apple Search Ads (US, DE, IT, ES), Google App campaigns. Paid app program expansion. | Peter Ocampo (Mobile App) |
| **Landing Page Strategy** | Polaris Brand LP rollout, Baloo (unauthenticated access), in-context registration, current customer redirects, email overlay. | MCS (Dwayne), CAT, Alex VanDerStuyf (AEM) |
| **Cross-Team Measurement** | SyRT incrementality testing, OCI as measurement framework adopted by other teams, COSMOS/MMR coordination. | Data Science, ABMA, Brand & Paid Media |
| **Adobe Analytics** | AMO access, bi-weekly Adobe sync, OCI reporting feed, WW redirect reporting. | Adobe (Suzane Huynh), Yun |
| **International Market Consulting** | AU CPC benchmarking (Lena challenge), MX keyword strategy, JP testing methodology. PS provides SEM expertise to market teams. | Lena Zak (AU), Lorena (MX), Nick Georgijev |
| **Event Strategy** | BSE, Prime Day, BFCM — PS + DG campaigns coordinated with broader marketing events. | Caroline Miller (Events), Creative |
| **AI/Automation Exploration** | AI Max testing, AEO/zero-click research, Jasper AI pilot evaluation. | Google, Hydra/Retail PS |
| **WBR Coverage** | Covering MCS WBR callouts when Dwayne is out. Pre-WBR Customer Engagement meeting participation. | Dwayne Palmer, Kristine Weber |

## Scope Summary

The PS team manages campaigns across 10 markets, coordinates with 13 stakeholder groups, and operates across both acquisition and engagement. The cross-functional work is not optional overhead — it is how every strategic initiative in this document was delivered.

<!-- AGENT_CONTEXT
machine_summary: "PS team structure: 7 people across 3 locations under Brandon Munday (L7). Covers 10 markets (US, UK, DE, FR, IT, ES, CA, JP, AU, MX) plus Mobile App (Peter Ocampo). 13 stakeholder groups with documented outcomes: Google (OCI implementation), MCS (in-context reg +13.6K regs), ABMA (match rate 13%→30%), MarTech (OCI infrastructure). Core PS work: campaign management, OCI bidding, testing, ad copy, competitive monitoring, budget/pacing, invoicing, reporting. Beyond-PS work: Engagement channel, F90 lifecycle, Mobile App, LP strategy, cross-team measurement, Adobe analytics, international consulting, event strategy, AI/automation."
key_entities: ["Brandon Munday", "Stacey Gu", "Dwayne Palmer", "Yun-Kang Chu", "Andrew Wirtz", "Aditya Thakur", "Richard Williams", "Peter Ocampo"]
action_verbs: ["manage", "coordinate", "test", "report", "optimize", "partner"]
update_triggers: ["team roster change", "new stakeholder relationship", "scope expansion or contraction", "new workstream added"]
-->
