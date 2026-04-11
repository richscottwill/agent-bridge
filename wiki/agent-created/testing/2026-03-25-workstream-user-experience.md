<!-- DOC-0413 | duck_id: testing-workstream-user-experience -->
---
title: "Workstream 4: User Experience"
status: FINAL
doc-type: strategy
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-04-05
update-trigger: "Polaris weblab results available, Baloo launch date confirmed, EU5 LP framework results, Aladdin timeline change, Guest auto-expiration weblab results"
tags: [ux, landing-pages, polaris, baloo, kate-doc]
---

# Workstream 4: User Experience

This document explains how the Paid Search team reduced funnel leakage at the landing page and registration stages, delivering +13.6K annualized incremental registrations in the US and +187% CVR improvement in CA. It provides the evidence base for the 2026 UX portfolio including Project Baloo and Project Aladdin. After reading, you should understand the baseline problem, the validated solutions, and how the 2026 investments compound across the funnel.

## How bad was the baseline?

In the previous experience, 85% of paid search customers dropped off at the MCS landing page before starting registration. Of those who made it to the registration start page, an additional 60% dropped off there. Customers who completed registration lost their product context entirely — they had to re-search for the same products they found on Google, creating a post-registration drop-off point with no measured recovery rate. The landing page experience was the single largest source of funnel leakage — and the team had no direct control over it without cross-functional partnership.

## What did in-context registration deliver?

The team partnered with MCS (Dwayne Palmer, Frank Volinsky, Vijeth Shetty) to launch an in-context registration start page on MCS Paid Search landing pages in the US (Q2-Q3 2025). The updated CTA wording — "Start browsing" instead of "Create a free account" — captured customer email directly on the MCS page and seamlessly transitioned them to the next registration step, replacing the previous out-of-context redirect. The result: +13.6K annualized incremental registrations with 100% probability (APT). Confidence: HIGH (APT-validated, sustained over multiple months).

This was built on learnings from two earlier experiments. Percolate showed signs of success in acquisition. Gated Guest showed -61% registrations and -24% OPS after 4 weeks and was paused. The team deep-dived setup, measurement, and CX before pivoting to in-context registration. The Gated Guest failure directly informed the design of the in-context approach — specifically, that reducing friction needed to happen within the existing page flow rather than through a separate gating mechanism.

## What did the CA landing page work show?

In CA, the MCS partnership involved diagnosing mobile-specific friction points — including cropped hero images and non-localized headlines — and applying a pre/post causal analysis framework to validate impact. The Bulk page CVR improved from 0.82% to 2.35% (+187%), and the Wholesale page improved from 0.75% to 2.10% (+180%). Mobile-specific improvements were also significant: +88% for Mobile EFID Bulk and +117% for Mobile EFID Wholesale (see Appendix: CA Test Results).

The CA results validated that localized content and mobile-first optimization drive material CVR improvement. This framework — diagnose mobile friction, localize headlines, validate with pre/post analysis — is now the repeatable playbook being applied to EU5.

## How is Polaris changing the brand landing page experience?

Project Polaris — the end-to-end MCS redesign — launched worldwide in December 2025. The PS team coordinated the Brand landing page rollout across all markets, with the US switching on March 24 and weblab dial-up targeting April 6-7. AEM translations are rolling out market-by-market, with AU and MX prioritized first. Early MCS Flash data shows +235 bps improvement in CTR into the AB registration flow in December, +635 bps YoY. This improvement reflects the combined effect of worldwide Polaris launches coupled with OCI rollout — the two workstreams compound.

## What does the 2026 UX portfolio look like?

The 2026 investments are designed to address different stages of the funnel, and they compound when deployed together. If resources constrain the portfolio, Baloo and in-context BIOAB are the highest-leverage investments — Baloo unlocks Shopping Ads (a step-change in channel capability) and BIOAB extends the proven in-context approach to a new placement.

Project Baloo (US Q2 2026) is the most significant UX investment. By providing unauthenticated access for unrecognized traffic on a dedicated subdomain, Baloo allows users to explore the Amazon Business catalog and pricing prior to registration. This is distinct from Guest, which requires entering the registration funnel. Baloo targets customers in the product discovery phase who have not yet committed to registration.

Baloo also unlocks Shopping Ads potential for AB — and this is a step-change in channel capability. Unlike current text ads, Shopping Ads results are unlimited, giving Amazon increased opportunity to saturate shopping results in both Paid and Free Shopping Ad slots. The current text-ad-only constraint caps AB's share of the search results page, and Shopping Ads removes that cap. The tech build is in progress with CAT and MCS.

Project Aladdin (Q4 2026) merges registration and checkout into a unified journey for high-intent customers, eliminating the re-search friction that causes post-registration drop-off. Guest auto-expiration is shortening from 12 months to 3 months (Q2 2026) to drive conversion urgency — the current 12-month window lets high-intent users lapse, and the 3-month window aligns with the F90 lifecycle activation window from Workstream 3. In-context registration is extending to the BIOAB placement (Q2 2026), where auto-verified customers resume their product search post-registration. Current customer redirects are scaling worldwide to eliminate wasted spend on existing customers across all markets. Email overlay weblabs are scaling worldwide to capture emails earlier in the funnel, reducing drop-off at the registration start page.

## What are the risks and open questions?

Baloo's Q2 2026 timeline depends on the CAT and MCS tech build completing on schedule. The Shopping Ads unlock is contingent on Baloo launching — without unauthenticated catalog access, Shopping Ads cannot function for AB. The Polaris weblab results (April 6-7 dial-up) will determine whether the registration flow improvements hold at full traffic. The EU5 LP framework assumes the CA methodology transfers to markets with different mobile usage patterns and competitive dynamics — per-market validation is needed.

---

## Appendix: CA landing page test results

| Page | Before CVR | After CVR | Improvement |
|------|-----------|-----------|-------------|
| Bulk | 0.82% | 2.35% | +186.6% |
| Wholesale | 0.75% | 2.10% | +180.0% |
| Mobile EFID (Bulk) | — | — | +88.4% |
| Mobile EFID (Wholesale) | — | — | +116.5% |

Mobile improvements addressed a disproportionate share of traffic given CA's mobile-dominant browsing patterns — the percentage gains understate the absolute volume impact.

<!-- AGENT_CONTEXT
machine_summary: "UX workstream addresses 85% LP drop-off and 60% registration start drop-off. Key results: in-context registration +13.6K annualized regs (100% probability APT, HIGH confidence), CA Bulk CVR +187%, CA Wholesale CVR +180%. Gated Guest failed (-61% regs) and informed pivot to in-context. Polaris Brand LP rolling out WW (US switched 3/24, weblab Apr 6-7, +235 bps CTR in Dec 2025). 2026: Project Baloo (US Q2, unauthenticated catalog access, unlocks Shopping Ads), EU5 LP framework from CA methodology, Project Aladdin (Q4, registration + checkout merge), Guest auto-expiration 12mo→3mo aligns with F90. Prioritization: Baloo and in-context BIOAB are highest-leverage if resources constrain. Risks: Baloo depends on CAT/MCS tech build, Polaris weblab results pending."
key_entities: ["in-context registration", "Polaris", "Baloo", "Aladdin", "Gated Guest", "CA LP framework", "Shopping Ads", "MCS", "Weblab", "F90", "BIOAB"]
action_verbs: ["optimize", "migrate", "redirect", "test", "scale", "unlock"]
update_triggers: ["Polaris weblab results available", "Baloo launch date confirmed", "EU5 LP framework results", "Aladdin timeline change", "Guest auto-expiration weblab results"]
-->
