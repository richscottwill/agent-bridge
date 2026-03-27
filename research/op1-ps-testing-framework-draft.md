# Paid Search Testing Framework: From Validated Results to Scalable Growth

This document establishes the technical foundation for OP1 by detailing the evolution of the Paid Search testing framework. Last year's tests have become this year's baseline; this approach ensures that 2026 investments are grounded in validated performance rather than speculation. By building on the cumulative effect of last year's results, the team has established a baseline that will unlock a more scalable, automated, and audience-centric acquisition engine in 2026.

Each section below covers one workstream: what we tested, what we learned, and how the validated results directly inform 2026 investment. Each initiative required cross-functional collaboration spanning Legal, Data Science, MarTech, MCS, Customer Research, and international market teams, with the PS team often serving as the connective tissue between platform capabilities and business objectives.

---

## Intelligent Management: Bidding Evolution

*Progression: Loss of Google Ads auto-bid strategy and Adobe → OCI success and expansion*

To launch OCI bidding, accurate tracking of campaign traffic and conversions was required. The Paid Search team partnered with the MarTech team to implement OCI as the first non-retail business unit at Amazon, requiring significant cross-team collaboration and operational effort. The team worked closely with Legal, the MarTech team, and the Data Science team to enable the rollout. This included defining the OCI value framework, ensuring the appropriate tracking and account structure were set up correctly, and validating the underlying data to support accurate optimization.

To ensure a disciplined rollout, the team established a phased implementation and measurement plan — beginning with E2E keyword-level testing, scaling through 25%, 50%, and 100% campaign-level application — to evaluate performance lift and guide ongoing optimization. As part of this effort, the team also analyzed the relationship between ROAS targets and CPA performance to ensure the appropriate tROAS settings were applied during the transition. The measurement framework, which compares actualized CPA against a baseline built from prior-quarter data with seasonality adjustments, has since become the standard approach for each new market rollout.

As a result, the team is seeing a +24% registration lift in the US (meeting 96% of expectations), +23% in the UK (94%), and +18% in DE (86%) through non-brand CPA improvement of -45%, -38%, and -37% respectively. In total, OCI contributed +32K registrations across the initial rollout period, translating to an estimated $16.7MM in OPS. Brand CPA improved -10% to -14% across all three markets with +1% registration lift, aligned with expectations given the lower improvement opportunity on high-intent Brand terms.

UK performance was slightly below US due to EU DMA privacy restrictions limiting the data signals available to the bidding algorithm. DE was further impacted by privacy-driven variability in OCI values and higher cost-per-clicks (+27% vs. UK), which constrained efficient volume capture at scale.

**2026: RoW Expansion.** The team is scaling OCI to CA, JP, FR, IT, ES, with tech-readiness complete in Q1 2026 and full monthly registration impact expected by July. The phased implementation and measurement framework developed in 2025 is now the standard playbook for each new market. The privacy-related learnings from DE are directly informing milestone timelines for EU4 markets — specifically, the team is building longer stabilization windows into markets with DMA-driven data restrictions.

---

## Modern Search: Fueling the Algorithm

*Progression: Fragmented, highly segmented campaigns → Device and Keyword Theme Consolidation → Fueling Machine Learning & OCI*

To align with Google's modern search best practices — leveraging automation, machine learning, and more flexible ad formats — the team implemented Responsive Search Ads (RSAs) and consolidated device-specific campaigns in the US, reducing the total number of campaigns and enabling more streamlined management. These changes are important because modern search optimization performs best with stronger data signals and simplified structures. Campaign consolidation allows the bidding algorithms to learn faster, test more creative combinations, and optimize in real time, ultimately improving efficiency and driving stronger conversion outcomes.

In EU5, the team applied a similar consolidation approach. Prior to consolidation, campaigns were fragmented across device types and narrow keyword themes, limiting the data available to each bid strategy. By consolidating device-specific campaigns and aligning keyword themes, the team provided the bidding algorithms with richer signal density, which directly supported the transition to OCI-powered bidding. The before-and-after comparison in EU5 demonstrated that consolidated structures outperformed fragmented ones in both efficiency and registration volume, even during the transition period.

Additionally, the team incorporated learnings from the AB Sole Proprietor Experience study — a primary customer research initiative conducted in August 2025 — to develop evidence-based ad copy. The study revealed that Sole Proprietors' top priorities were price, quality, and selection, and that messaging around bulk purchasing and B2B exclusivity was actively deterring registration. The team shifted ad copy accordingly, first testing in UK and IT. The UK test delivered an 86% improvement in CTR with a 31% increase in registrations compared to the original ads, validating the research-driven approach.

**2026: Consolidation and Ad Copy Scale.** As part of the OCI rollout to RoW, the team is continuing a phased consolidation approach by combining campaign keyword themes, which will further reduce campaign count and strengthen data signals for optimization, reduce operational complexity, and create a more scalable campaign structure for future growth. UK and DE Product and Vertical campaigns have already been consolidated. Translations of the research-driven ad copy have been completed for EU4 via GlobalLink, and the team is preparing phased rollout across all non-brand campaigns. This structural simplification is also a prerequisite for AI Max testing (see Algorithmic Ads section), which requires consolidated campaign structures to function effectively.

---

## Audiences: Utilizing B2B Reach

*Progression: LiveRamp Suppression → Engagement Account Creation → Associated Accounts Integration → F90 Lifecycle Engagement*

Paid Search teams typically function as top-of-funnel acquisition engines, accepting platform limitations and relying on provided dashboards. This team operated differently by partnering directly with lifecycle strategy owners to extend Paid Search beyond acquisition into customer engagement.

The audience strategy evolved in three phases. First, the team implemented LiveRamp suppression across US and CA campaigns in February 2025, removing current AB customers from acquisition targeting to reduce wasted spend. This established the audience infrastructure for more advanced targeting. Second, the team built a dedicated Engagement account in partnership with the Traffic & Onsite Marketing team, creating a net-new channel that bridged top-of-funnel acquisition and lifecycle strategy. The primary hurdle was Google's low B2B customer recognition rate — initially just 12-13% of our customer list could be matched to Google users. To overcome this, the team partnered with ABMA to ingest Associated Accounts (consumer-side emails linked to B2B users), a manual platform intervention that more than doubled audience reach to 30%. Third, this expanded audience capability enabled the Engagement channel to drive $765K in iOPS in 2025.

**2026: F90 Lifecycle Engagement.** With the Engagement account proven, the team is navigating Legal SIMs to launch the F90 (First 90 Days) program. F90 targets recently acquired, non-purchasing customers to complete 3+ purchases and adopt high-value actions, with the goal of increasing the percentage of non-SHuMA customers completing 3+ purchases from 31.7% to 35.4% (+366bps YoY). Legal is currently reviewing new audiences and audience-transmission solutions for use across Engagement ad types. This extends Paid Search's role from acquisition into activation — a fundamentally different operating model for the channel.

---

## User Experience: Landing Page Improvements

*Progression: Siloed Landing Pages → URL migrations → Percolate/Guest → Targeted page optimizations → Current Customer Redirects and WW push → Baloo*

In the previous experience for paid search customers coming from Google, 85% dropped off at the MCS landing page before starting registration, with an additional 60% dropping off at the registration start page. Those who completed registration had to manually re-search for the same products they found on Google. The landing page experience was the single largest source of funnel leakage.

The landing page strategy transitioned from siloed MCS pages to a standardized architecture that allows for simpler, scalable experiments. Following this migration, the team experimented with value-first engagement through "Percolate" and "Guest" flows, which allowed prospects to view product selection and pricing before encountering registration requirements. The hypothesis was that greater transparency would improve conversion. Although Percolate showed signs of success in acquisition, the Gated Guest experiment showed -61% registrations and -24% OPS after 4 weeks and was paused. The team deep-dived into setup, measurement, and CX before pivoting to the approaches below.

The team refined this baseline through integrated optimizations, partnering closely with the MCS team to optimize the end-to-end landing page experience. A key breakthrough was the in-context registration start page launched on MCS Paid Search landing pages in partnership with MCS (Q2-Q3 2025). The updated CTA wording ("Start browsing" instead of "Create a free account") captured customer email directly on the MCS page and seamlessly transitioned them to the next registration step, replacing the previous out-of-context redirect. This delivered +13.6K annualized incremental registrations with 100% probability (APT), built on learnings from two earlier experiments focused on enabling quick product engagement through guest registration.

In CA, the MCS partnership involved diagnosing mobile-specific friction points — including cropped hero images and non-localized headlines — and applying a pre/post causal analysis framework to validate impact. Phase 1 optimizations on Bulk and Wholesale pages drove significant CVR recovery: Bulk CVR improved from 0.82% to 2.35% (+186.6%) and Wholesale CVR from 0.75% to 2.10% (+180.0%), with Mobile EFID CVR gains of +88.4% and +116.5% respectively. These results validated two foundational hypotheses — localized content and mobile-first image optimization — establishing a repeatable testing framework.

Additionally, the team implemented current customer redirects and email overlay weblabs to resolve targeted friction points across global markets. By focusing on improving users' experiences after clicking ads, these efforts addressed conversion barriers that existed beyond the ad platform itself.

**2026: Baloo, EU5 Scale, and Registration Integration.** Project Baloo represents the most significant UX investment for 2026. By providing unauthenticated access for unrecognized traffic on a dedicated subdomain, Baloo allows users to explore the Amazon Business catalog and pricing prior to registration — friction-free product engagement directly from Google to AB products. This is distinct from Guest (which requires entering the registration funnel): Baloo targets customers in the product discovery phase who have not yet committed to registration. Baloo also unlocks Shopping Ads potential for AB — unlike current text ads, Shopping Ads results are unlimited, giving Amazon increased opportunity to saturate shopping results in both Paid and Free Shopping Ad slots. US launch is targeted for Q2 2026, with tech build currently in progress in partnership with CAT and MCS.

The CA landing page testing framework is being applied to EU5 markets, using the validated methodology of regional-specific headlines, mobile optimization, and page formatting improvements. Current customer redirects and email overlay weblabs are being scaled to WW markets.

Additional 2026 UX investments include: reducing Guest auto-expiration from 12 months to 3 months (Q2 2026) to drive conversion urgency based on current conversion patterns; in-context registration from the onsite Buy-it-on-AB (BIOAB) placement (Q2 2026), allowing automatically verified customers to resume their action post-registration; and integrating registration with checkout via Project Aladdin (Q4 2026) — merging the traditional two separate journeys of registration and checkout into a unified experience for high-intent customers.

---

## Algorithmic Ads: Demand Gen and Incremental Growth

*Progression: Google Discovery Ads Launch → Google's Transition to Demand Gen → 2026 DG Creative & Audience Expansion → 2026 AI Max Testing (US)*

The PS team proactively tested new Google campaign types beyond traditional keyword campaigns, launching Discovery Ads in 2023. While initial registrations were limited, the team continued iterating mid-funnel strategies by leveraging Demand Gen ads to drive traffic. In 2024, the team incorporated LiveRamp targeting capabilities to reach existing customer audiences in the US, improving audience precision for engagement campaigns.

Demand Gen ads drove cost-efficient traffic — $0.39 CPC in 2025 compared to $2.43 for keyword campaigns in the Engagement account — leading the team to further expand the tactic and increase investment. In Q4 2025, the team strategically focused on DG campaigns, achieving +53% YoY traffic growth despite a -35% YoY decrease in Q4 spend by improving CPC -58% YoY. During Prime Day 2025, the Engagement campaigns drove 80K clicks at -10% cost YoY, generating $329K in OPS at a 644% ROAS, a 12x improvement over the prior year. The team also launched Business Essentials through DG image placements, delivering 52K visitors in the first year at a $0.30 CPC. These efforts established visual ad formats as a scalable and cost-efficient channel for driving qualified traffic.

**2026: Video Expansion and AI Max.** With Demand Gen images now a proven channel, the team is turning attention to video assets within the Demand Gen ad type. Early testing shows video CPCs in line with image asset CPCs ($0.30 for both), indicating strong efficiency potential. BSE video launched in January 2026, with the strategy replicating the proven DG image approach while optimizing through short video creative and increased image variations.

The team also plans to test Google's AI Max feature, beginning with a US-market test in 2026. AI Max represents Google's next evolution in campaign intelligence — expanding keyword matching, dynamically selecting landing page experiences, and unlocking enhanced audience signals. The team is approaching this test in collaboration with other Amazon teams as well as Google vendors, establishing clear measurement guardrails, defining incrementality benchmarks, and working to ensure AI Max's expanded reach does not cannibalize existing Paid Search performance. This test applies the same measurement discipline used for OCI: clear baselines, phased rollout, and incrementality benchmarks established before scaling. If the US test validates efficiency and incremental growth, the learnings will inform a broader rollout strategy WW.

---

## 2026 Summary

Every 2026 investment maps to a validated 2025 signal. The table below summarizes the through-line from results to forward commitment.

| Workstream | 2025 Validated Signal | 2026 Investment | Expected Impact |
|---|---|---|---|
| OCI Bidding | +18-24% reg uplift; -37% to -45% NB CPA; +32K regs / $16.7MM OPS | Scale to FR, IT, ES, CA, JP (July 2026) | Replicate double-digit reg uplift in RoW |
| Modern Search | +86% CTR / +31% regs (research-driven copy); consolidation improved data density | Keyword theme consolidation WW; EU5 ad copy rollout; structural prep for AI Max | Further campaign count reduction; stronger OCI signals |
| Audiences | $765K iOPS; 30% match rate (from 13%); Engagement channel proven | F90 Lifecycle Engagement launch | +366 bps in non-SHuMA 3+ purchase rate |
| User Experience | +13.6K annualized regs (in-context); +186% CVR (CA Bulk); 85% LP drop-off identified and addressed | Project Baloo (US Q2); EU5 LP framework rollout; Aladdin (Q4) | Friction-free product engagement; Shopping Ads unlock |
| Algorithmic Ads | $0.39 DG CPC vs. $2.43 keyword; +53% YoY traffic; 644% ROAS (Prime Day) | DG Video expansion; AI Max US test; BSE scaling | Scalable mid-funnel at proven efficiency |

Collectively, these workstreams compound: campaign consolidation strengthens OCI signals, OCI enables smarter bidding on the audiences the Engagement channel reaches, and Baloo creates the friction-free landing experience that AI Max's dynamic page selection requires. The team is transforming Paid Search from a keyword-driven acquisition channel into an automated, audience-centric engine that drives incremental growth at scale — grounded not in speculation, but in the cumulative evidence of the past year's validated results.
