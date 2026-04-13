---
title: "F90 Lifecycle Program Strategy"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0384 | duck_id: strategy-f90-lifecycle-strategy -->

---
title: F90 Lifecycle Program Strategy
status: DRAFT
doc-type: strategy
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-04-04
update-trigger: Legal SIM updates, match rate changes, ABMA partnership progress, first cohort results
---

# F90 Lifecycle Program Strategy

---

## Executive Summary

F90 extends Amazon Business Paid Search beyond registration into post-registration purchasing behavior. The program targets non-SHuMA customers — those who registered through paid search but have not yet made three or more purchases within 90 days of signup. The goal is to move the 3+ purchase rate from 31.7% to 35.4%, a ~12% improvement that fundamentally changes the PS team's value proposition from "we drive registrations" to "we drive registrations AND purchases."

This is Decision D10 in the brain's decision log. It builds on the Engagement channel infrastructure (D6) and positions PS as a full-funnel channel — the first time the team has owned anything beyond the registration event.

---

## The Problem

Paid search has historically been measured on one metric: registrations. A customer clicks an ad, lands on a page, and signs up. That's where PS's accountability ends. But a registration without purchasing behavior is a hollow metric — it inflates the funnel without generating OPS (Ordered Product Sales).

The data tells a specific story. Of customers acquired through paid search, 31.7% make three or more purchases within their first 90 days. The remaining 68.3% either make fewer than three purchases or none at all. These non-purchasing registrants represent a significant gap between acquisition cost and realized customer value — and that gap is what ie%CCP measures at the program level.

F90 exists to close that gap. By re-engaging non-purchasers at structured intervals (30, 60, and 90 days post-registration), the program aims to convert passive registrants into active buyers. The 35.4% target represents the minimum improvement needed to materially shift the program's unit economics.

---

## How F90 Works

The program operates in four stages:

### Stage 1: Registration Event
A customer registers via paid search. The registration event is captured in Google Ads (via OCI where available) and in Amazon's internal systems. This is the existing workflow — F90 doesn't change anything about acquisition.

### Stage 2: Identification
At day 30, 60, and 90 post-registration, F90 identifies customers who have not yet reached the 3+ purchase threshold. This identification depends on the ABMA (Amazon Business Marketing Analytics) match rate — the ability to connect a Google Ads click to an Amazon customer record.

The match rate is the critical dependency. At 13% (current state), F90 can only identify and target a small fraction of non-purchasers. At 30% (target via Associated Accounts partnership), the addressable audience triples. The match rate improvement is the single biggest lever for F90's effectiveness.

### Stage 3: Re-engagement
Identified non-purchasers receive targeted re-engagement through two channels:

1. **Paid Search (RLSA):** Remarketing Lists for Search Ads allow the team to bid differently when a known non-purchaser searches for business-related terms. The bid adjustment reflects the higher value of converting an existing registrant vs. acquiring a new one.

2. **Email:** Direct email outreach with product recommendations, category highlights, and purchase incentives. This channel requires Legal SIM approval (obtained) and depends on the match rate for audience size.

The dual-channel approach is deliberate. RLSA captures intent (the customer is actively searching), while email creates intent (the customer receives a prompt). Together, they cover both pull and push engagement.

### Stage 4: Measurement
Each cohort is tracked on three metrics:

| Metric | Definition | Baseline | Target |
|--------|-----------|----------|--------|
| 3+ purchase rate | % of cohort making 3+ purchases within 90 days | 31.7% | 35.4% |
| Time to first purchase | Median days from registration to first order | TBD | TBD |
| Incremental OPS | OPS attributable to F90 re-engagement vs. organic purchasing | $0 | TBD |

The 3+ purchase rate is the primary metric because it's the threshold where customer LTV justifies acquisition cost. One or two purchases may not cover the CPA; three or more almost certainly does.

---

## Dependencies and Current Status

### Legal (✅ Approved)
Legal SIMs for targeting existing customers with re-engagement messaging have been navigated and approved. This was the earliest blocker — without Legal clearance, the program couldn't exist. Cleared in Q4 2025.

### Engagement Channel (✅ Built)
The Engagement campaign type exists in Google Ads across relevant markets. This is the RLSA infrastructure — campaigns configured for remarketing audiences with separate bidding strategies. Built as part of Decision D6 (Engagement Channel Creation).

### ABMA Match Rate (🔄 In Progress — Primary Blocker)
The Associated Accounts partnership with ABMA is the critical path item. Current match rate: 13%. Target: 30%. The improvement comes from ABMA's ability to connect Google click IDs to Amazon customer records through associated account data.

At 13%, the addressable audience is too small for statistically meaningful results. At 30%, the program becomes viable for US launch. The match rate improvement is not a technical problem — it's a data partnership that requires ABMA to expand their matching methodology.

Timeline: ABMA has committed to the partnership but has not provided a firm delivery date. Richard's estimate: Q2 2026 for the match rate to reach 25-30%.

### F90 Targeting (⏳ Pending Match Rate)
The actual targeting logic — identifying non-purchasers at 30/60/90 days and building RLSA audiences — cannot be implemented until the match rate reaches a viable threshold. This is a hard dependency, not a soft one.

### Data Science Partnership (🔄 In Progress)
Data Science is providing customer segmentation for targeting. The segmentation model will identify which non-purchasers are most likely to convert with re-engagement (high-propensity) vs. those who registered with no purchase intent (low-propensity). Targeting high-propensity non-purchasers first maximizes the program's early results and builds the case for expansion.

---

## Cross-Functional Partners

| Team | Role | Contact | Status |
|------|------|---------|--------|
| ABMA | Associated Accounts, match rate improvement | — | Active partnership, match rate improvement in progress |
| Legal | SIM approval for targeting existing customers | — | ✅ Approved |
| Data Science | Customer segmentation, LTV modeling, propensity scoring | — | Active, segmentation model in development |
| MCS | Lifecycle page destinations (where redirected customers land) | Dwayne Palmer | Pending — need to define engagement landing pages |
| Adobe | Audience segment creation, Ad Cloud reporting | Suzane Huynh | Pending — depends on match rate milestone |

---

## Strategic Context

F90 sits at the intersection of Level 2 (structured testing with clear measurement), Decision D6 (Engagement channel infrastructure), and Decision D10 (extending PS beyond registration). If F90 works, PS becomes a full-funnel channel — registration is the top, F90 is the middle, and the team's value is measured by how many people sign up AND buy.

---

## Launch Plan

| Phase | Scope | Timeline | Gate |
|-------|-------|----------|------|
| Phase 1 | US only, high-propensity non-purchasers | Q2 2026 (pending match rate) | Match rate ≥25% |
| Phase 2 | US expanded to all non-purchasers | Q3 2026 | Phase 1 shows ≥2pp improvement in 3+ purchase rate |
| Phase 3 | UK, DE (OCI markets with match rate support) | Q4 2026 | Phase 2 validated |

US first because it has the largest volume, the most mature OCI infrastructure, and the strongest ABMA partnership. UK and DE follow because they're the next-largest OCI markets. Markets without OCI (AU, MX) are excluded from the initial rollout — F90 depends on conversion signal infrastructure that those markets don't have.

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Match rate stays below 25% | MEDIUM | HIGH — program can't launch | Escalate through Brandon to ABMA leadership. Explore alternative matching methods. |
| Non-purchasers don't respond to re-engagement | LOW | MEDIUM — program underperforms | Data Science propensity model filters for high-likelihood converters. Start with best audience. |
| Email channel cannibalization | LOW | LOW — measurement isolates channels | Run RLSA and email as separate test cells initially to measure incremental lift per channel. |
| Legal SIM scope changes | LOW | HIGH — program paused | SIMs already approved. Monitor for policy changes. |

---

## Sources
- F90 target: non-SHuMA 31.7% → 35.4% — source: ~/shared/context/body/brain.md → D10: F90 Lifecycle Program
- Legal SIMs navigated — source: ~/shared/context/body/brain.md → D10
- ABMA partnership, match rate 13% → 30% — source: ~/shared/context/body/brain.md → D6: Engagement Channel Creation
- Engagement channel created — source: ~/shared/context/body/brain.md → D6
- Cross-functional partners — source: ~/shared/context/body/brain.md → Decision Principle #5
- ie%CCP framework and customer value — source: ~/shared/artifacts/strategy/2026-03-30-ieccp-planning-framework.md
- RLSA campaign structure — source: ~/shared/artifacts/best-practices/2026-03-25-google-ads-campaign-structure.md → Engagement campaigns
- Level 2 testing methodology — source: ~/shared/context/body/brain.md → Five Levels → Level 2

<!-- AGENT_CONTEXT
machine_summary: "Strategy for F90 lifecycle program extending PS beyond registration into post-reg purchasing. Target: improve non-SHuMA 3+ purchase rate from 31.7% to 35.4% within 90 days. Depends on ABMA match rate improvement (13%→30%). Legal approved. Engagement channel built. US launch Q2 2026 pending match rate gate. Dual-channel approach: RLSA + email. Data Science providing propensity scoring. If successful, transforms PS from acquisition-only to full-funnel channel."
key_entities: ["F90", "lifecycle", "non-SHuMA", "ABMA", "match rate", "RLSA", "Engagement channel", "Data Science", "Legal SIM", "OPS"]
action_verbs: ["target", "re-engage", "measure", "segment", "launch", "scale"]
update_triggers: ["ABMA match rate reaches 25%", "F90 targeting launches", "Legal SIM changes", "first cohort results available", "Data Science segmentation model delivered"]
-->
