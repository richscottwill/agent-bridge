---
title: Email Overlay WW Rollout Plan
status: DRAFT
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-04-04
update-trigger: Vijay tech scoping response, Adobe Ad Cloud reporting complete, market launches
---

# Email Overlay WW Rollout Plan

---

## Executive Summary

Email overlay solves a specific, measurable problem: existing Amazon Business customers who click paid search ads land on acquisition pages they cannot complete, inflating acquisition CPA and delivering a poor customer experience. The overlay identifies existing customers at the landing page level and redirects them to an engagement experience instead of the registration flow.

The US implementation is live via Adobe Target. Worldwide rollout is blocked by a single dependency: Vijay's tech scoping for international market implementation. Every non-US market is waiting on the same deliverable.

---

## The Problem

When an existing AB customer searches for a business-related term and clicks a paid search ad, they arrive at a registration page. They cannot register because they already have an account. From the customer's perspective, this is a dead end. From the program's perspective, this click counts as acquisition spend with zero conversion potential — it inflates CPA without any possibility of generating a registration.

The scale of this problem is not yet precisely measured (Adobe Ad Cloud reporting is in progress to quantify the existing-vs-new traffic split), but directional estimates suggest 15-25% of paid search clicks come from existing customers. At that rate, the CPA inflation is material: if 20% of clicks are from existing customers who can never convert, the effective CPA on convertible traffic is 25% higher than the reported blended CPA.

This is one of the few initiatives that improves both efficiency metrics and customer experience simultaneously. Existing customers get a relevant experience (product recommendations, account dashboard, category browsing). The acquisition funnel gets cleaner data (only new customers in the conversion denominator). OCI bidding gets better signals (conversions are real new customers, not noise).

---

## How the Overlay Works

### Technical Architecture

The email overlay uses Adobe Target to identify existing customers at the landing page level:

1. **Customer arrives** on an AB paid search landing page
2. **Adobe Target fires** and checks the visitor against AB's customer database
3. **If existing customer:** redirect to engagement experience (product recommendations, account dashboard, or category page)
4. **If new visitor:** show standard registration flow (no change to current experience)

The identification happens client-side via Adobe Target's visitor identification. The redirect is seamless — the customer sees the engagement page load, not a redirect notice.

### Engagement Destinations

The redirect destination matters. Sending an existing customer to a generic homepage is marginally better than a registration page, but not by much. The ideal destinations are:

| Destination Type | When to Use | Expected Impact |
|-----------------|-------------|-----------------|
| Product recommendations | Customer has purchase history | Highest engagement — personalized |
| Category page | Customer registered but never purchased | Drives first purchase (F90 alignment) |
| Account dashboard | Customer is active buyer | Lowest friction — they wanted to manage their account |
| General AB homepage | Fallback (no behavioral data) | Better than registration page, but generic |

The destination logic should be tiered: personalized > category > dashboard > homepage. Markets without personalization infrastructure start with the homepage fallback and upgrade as capabilities mature.

---

## US Implementation (Live)

The US customer redirect has been live since Q4 2025 via Adobe Target. Key details:

| Parameter | Value |
|-----------|-------|
| Platform | Adobe Target |
| Scope | All US paid search landing pages |
| Redirect destination | General engagement experience |
| Measurement | Adobe Ad Cloud segment (in progress) |
| Status | Live, monitoring |

The US implementation is the reference for WW rollout. The technical pattern (Adobe Target identification + redirect) is proven. The remaining work is replicating this pattern across international markets, which requires market-specific Adobe Target configurations and landing page implementations.

---

## WW Rollout Plan

### Market Prioritization

| Market | Priority | Status | Blocker | Target Launch |
|--------|----------|--------|---------|---------------|
| US | - | Live | None | Complete |
| UK | 1 | Pending | Tech scoping (Vijay) | Q2 2026 |
| DE | 2 | Pending | Tech scoping (Vijay) | Q2 2026 |
| CA | 3 | Pending | Tech scoping (Vijay) | Q2 2026 |
| AU | 4 | Pending | Tech scoping (Vijay) | Q2 2026 |
| MX | 5 | Pending | Tech scoping (Vijay) | Q3 2026 |
| JP | 6 | Pending | Tech scoping (Vijay) | Q3 2026 |
| FR | 7 | Pending | Tech scoping (Vijay) | Q3 2026 |
| IT | 8 | Pending | Tech scoping (Vijay) | Q3 2026 |
| ES | 9 | Pending | Tech scoping (Vijay) | Q3 2026 |

Priority is based on market volume and OCI status. UK and DE are highest priority because they have the largest non-US traffic volumes and are already on OCI — the overlay will compound OCI's efficiency gains by removing non-convertible clicks from the bidding signal.

### The Single-Point-of-Failure Problem

Every market except US is blocked by the same dependency: Vijay's tech scoping. This is a single-point-of-failure. The tech scoping determines:

1. Whether the US Adobe Target pattern can be replicated internationally (or if a different approach is needed)
2. Per-market implementation requirements (landing page changes, Adobe Target configuration)
3. Timeline and resource requirements

If Vijay does not respond by the escalation deadline, the path is: Richard escalates through Brandon to Vijay's management chain. The escalation is justified because 9 markets are blocked by one deliverable.

---

## Measurement Framework

### Pre-Redirect Baseline (Required Before Launch)

Before launching the overlay in any market, capture:

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| Existing customer % of clicks | Adobe Ad Cloud segment | Quantifies the CPA inflation problem |
| Blended CPA (all traffic) | Google Ads | Pre-redirect baseline for comparison |
| New-customer-only CPA | Adobe Ad Cloud segment | True acquisition CPA (the number we want to improve) |
| Existing customer bounce rate | Adobe Analytics | How many existing customers leave the registration page |

The Adobe Ad Cloud reporting segment (currently in progress) is the prerequisite for this baseline. Without it, we cannot measure the overlay's impact.

### Post-Redirect Measurement

| Metric | Expected Direction | Significance Threshold |
|--------|-------------------|----------------------|
| Acquisition CPA | Decrease (existing customers removed from denominator) | >5% improvement |
| Existing customer engagement | Increase (relevant experience vs. dead end) | Any positive engagement |
| OCI signal quality | Improve (cleaner conversion data) | Directional |
| Total paid search ROI | Improve (same spend, better outcomes for both audiences) | >3% improvement |

---

## Dependencies

| Dependency | Owner | Status | Impact if Delayed |
|-----------|-------|--------|-------------------|
| Vijay tech scoping | Vijay | Overdue | All 9 non-US markets blocked |
| Adobe Ad Cloud reporting segment | Adobe team | In progress | Cannot measure baseline or impact |
| Market-specific redirect destinations | MCS (Dwayne Palmer) | Not started | Fallback to generic homepage |
| Adobe Target international configuration | Adobe team | Pending tech scoping | Cannot implement overlay |

---

## Connection to Other Initiatives

- **OCI:** The overlay improves OCI signal quality. When existing customers are removed from the conversion funnel, OCI's bidding algorithm optimizes on cleaner data — only real new-customer conversions. This should improve NB CPA beyond the direct CPA improvement from removing non-convertible clicks.
- **F90:** The overlay creates a natural handoff to F90. Existing customers who are redirected to engagement experiences are exactly the audience F90 targets — registered but not yet purchasing. The overlay becomes the entry point for lifecycle re-engagement.
- **Polaris LP:** The overlay must be compatible with Polaris landing pages. As markets migrate to Polaris, the Adobe Target implementation needs to work on the new page templates.

---

## Sources
- US redirect live, WW pending - source: ~/shared/context/body/hands.md -> P2 Overdue Items (WW redirect)
- Vijay tech scoping blocker - source: ~/shared/context/active/current.md -> Active Projects
- Adobe Ad Cloud reporting in progress - source: ~/shared/context/body/hands.md -> Core tasks (WW redirect)
- Existing customer traffic estimates (15-25%) - source: directional estimate from US Adobe Target data
- F90 connection - source: ~/shared/context/body/brain.md -> D10: F90 Lifecycle Program
- OCI signal quality improvement - source: ~/shared/context/body/brain.md -> D1: OCI Implementation Approach

<!-- AGENT_CONTEXT
machine_summary: "WW rollout plan for email overlay that redirects existing AB customers away from acquisition pages. US is live via Adobe Target. All 9 non-US markets blocked by Vijay tech scoping (single-point-of-failure). Expected impact: lower acquisition CPA (existing customers removed from denominator), better customer experience, cleaner OCI signals. Compounds with F90 lifecycle and OCI bidding. Adobe Ad Cloud reporting segment needed for baseline measurement."
key_entities: ["email overlay", "Vijay", "Adobe Target", "Adobe Ad Cloud", "acquisition CPA", "existing customers", "OCI", "F90"]
action_verbs: ["redirect", "measure", "escalate", "implement", "rollout"]
update_triggers: ["Vijay tech scoping response", "Adobe Ad Cloud reporting complete", "market launches"]
-->
