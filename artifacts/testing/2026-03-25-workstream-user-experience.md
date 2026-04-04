---
title: "Workstream 4: User Experience"
slug: "kate-doc-ux"
type: "playbook"
audience: "org"
status: "draft"
doc-type: strategy
created: "2026-03-25"
updated: "2026-03-25"
owner: "Richard Williams"
tags: ["ux", "landing-pages", "polaris", "baloo", "kate-doc"]
summary: "LP optimization: +13.6K annualized regs (in-context), +187% CVR (CA Bulk). Baloo unlocks Shopping Ads."
---

# Workstream 4: User Experience

*Progression: Siloed Landing Pages → URL migrations → Percolate/Guest → Targeted optimizations → Current Customer Redirects → Baloo*

## The Problem

In the previous experience for paid search customers coming from Google, 85% dropped off at the MCS landing page before starting registration, with an additional 60% dropping off at the registration start page. Those who completed registration had to manually re-search for the same products they found on Google. The landing page experience was the single largest source of funnel leakage.

## What We Did

### In-Context Registration (US, Q2-Q3 2025)

The team partnered with MCS to launch an in-context registration start page on MCS Paid Search landing pages. The updated CTA wording ("Start browsing" instead of "Create a free account") captured customer email directly on the MCS page and seamlessly transitioned them to the next registration step, replacing the previous out-of-context redirect.

**Result:** +13.6K annualized incremental registrations with 100% probability (APT).

This was built on learnings from two earlier experiments — Percolate and Gated Guest — that tested different approaches to reducing registration friction. Percolate showed signs of success in acquisition. Gated Guest showed -61% registrations and -24% OPS after 4 weeks and was paused. The team deep-dived setup, measurement, and CX before pivoting to in-context registration. The failure was the teacher.

### CA Landing Page Optimization (2025)

In CA, the MCS partnership involved diagnosing mobile-specific friction points — including cropped hero images and non-localized headlines — and applying a pre/post causal analysis framework to validate impact.

| Page | Before CVR | After CVR | Improvement |
|------|-----------|-----------|-------------|
| Bulk | 0.82% | 2.35% | +186.6% |
| Wholesale | 0.75% | 2.10% | +180.0% |
| Mobile EFID (Bulk) | — | — | +88.4% |
| Mobile EFID (Wholesale) | — | — | +116.5% |

**So what:** The CA results validated that localized content and mobile-first optimization drive material CVR improvement. The Bulk page nearly tripled its conversion rate. This framework — diagnose mobile friction, localize headlines, validate with pre/post analysis — is now the repeatable playbook being applied to EU5.

### Current Customer Redirects and Email Overlay (WW)

The team implemented current customer redirects to resolve a specific friction point: existing AB customers clicking on Google ads and landing on registration pages. By redirecting recognized customers to the buying experience instead, we eliminated wasted ad spend and improved customer experience.

Email overlay weblabs tested capturing email addresses earlier in the funnel to reduce drop-off at the registration start page.

### Polaris Brand LP Rollout (WW, 2025-2026)

Project Polaris — the end-to-end MCS redesign — launched WW in December 2025. The PS team coordinated the Brand landing page rollout across all markets:

- US: Switched to Polaris on 3/24 (Stacey)
- Weblab dial-up targeting April 6-7
- AEM translations for AU/MX/JP/CA due 3/26 (Alex VanDerStuyf)
- Brandon's priority order: AU > MX > DE > UK > JP > FR > IT > ES > CA > US-ES

MCS Flash data (Nov-Dec 2025) shows the Polaris impact: +235 bps improvement in CTR into AB registration flow in December, +635 bps YoY — driven by the WW Polaris launches coupled with OCI rollout.

## 2026: Baloo, EU5 Scale, and Registration Integration

### Project Baloo (US Q2 2026)

Baloo represents the most significant UX investment for 2026. By providing unauthenticated access for unrecognized traffic on a dedicated subdomain, Baloo allows users to explore the Amazon Business catalog and pricing prior to registration — friction-free product engagement directly from Google to AB products.

This is distinct from Guest (which requires entering the registration funnel): Baloo targets customers in the product discovery phase who have not yet committed to registration.

Baloo also unlocks Shopping Ads potential for AB. Unlike current text ads, Shopping Ads results are unlimited, giving Amazon increased opportunity to saturate shopping results in both Paid and Free Shopping Ad slots. US launch is targeted for Q2 2026, with tech build in progress in partnership with CAT and MCS.

### Additional 2026 UX Investments

| Initiative | Timeline | Expected Impact |
|-----------|----------|-----------------|
| EU5 LP framework (from CA methodology) | 2026 | Apply CA's validated playbook (regional headlines, mobile optimization, page formatting) to EU5 markets. CA Bulk CVR +187% is the benchmark. |
| Guest auto-expiration: 12 months → 3 months | Q2 2026 | Shorten the Guest window to drive conversion urgency. Current 12-month expiration lets high-intent users lapse — 3 months matches the F90 lifecycle activation window. |
| In-context registration from BIOAB placement | Q2 2026 | Auto-verified customers resume their product search post-registration instead of restarting. Extends the +13.6K in-context model to a new entry point. |
| Project Aladdin: Registration + checkout merge | Q4 2026 | Unified journey for high-intent customers — register and purchase in one flow. Eliminates the re-search friction that causes post-registration drop-off. |
| Current customer redirects WW scale | 2026 | Eliminate wasted spend on existing customers across all markets. US validated the approach; WW scale is operational execution. |
| Email overlay weblabs WW scale | 2026 | Earlier email capture in funnel reduces drop-off at registration start page. Weblab-validated approach scaling to remaining markets. |

**So what:** The 2026 UX portfolio is designed to compound. Baloo creates friction-free product engagement. Aladdin merges registration and checkout for high-intent users. Guest auto-expiration and F90 work together to convert within 90 days. Each initiative addresses a different stage of the funnel — together they reduce the 85% LP drop-off and the 60% registration start drop-off identified in the baseline.

## Cross-Functional Partners
- MCS (Dwayne Palmer, Frank Volinsky, Vijeth Shetty): LP optimization, Polaris rollout, Weblab testing
- CAT: Baloo tech build
- Alex VanDerStuyf: AEM translations for WW rollout
- Alexis Eck (AU): MCS → Polaris migration, URL mapping
- Lena Zak (AU): Confirmed full Polaris switch (3/13)
- ESI: Public pricing integration for carousel retest

<!-- AGENT_CONTEXT
machine_summary: "UX workstream addresses the 85% LP drop-off and 60% registration start drop-off. Key results: in-context registration +13.6K annualized regs (100% probability APT), CA Bulk CVR +187%, CA Wholesale CVR +180%. Gated Guest failed (-61% regs) and informed the pivot to in-context. Polaris Brand LP rolling out WW (US switched 3/24, weblab Apr 6-7). 2026: Project Baloo (US Q2, unauthenticated catalog access, unlocks Shopping Ads), EU5 LP framework from CA methodology, Project Aladdin (Q4, registration + checkout merge). Cross-functional: MCS (Dwayne Palmer), CAT (Baloo tech), Alex VanDerStuyf (AEM translations)."
key_entities: ["in-context registration", "Polaris", "Baloo", "Aladdin", "Gated Guest", "CA LP framework", "Shopping Ads", "MCS", "Weblab"]
action_verbs: ["optimize", "migrate", "redirect", "test", "scale", "unlock"]
update_triggers: ["Polaris weblab results available", "Baloo launch date confirmed", "EU5 LP framework results", "Aladdin timeline change"]
-->
