<!-- DOC-0410 | duck_id: testing-workstream-audiences-lifecycle -->
---
title: "Workstream 3: Audiences and Lifecycle"
status: FINAL
doc-type: strategy
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-04-05
update-trigger: "F90 Legal SIM resolved, LiveRamp 1P approval status change, Engagement channel quarterly performance update, Tumble service requirements resolved"
tags: [audiences, engagement, f90, kate-doc]
---

# Workstream 3: Audiences and Lifecycle

This document explains how the Paid Search team extended its role from top-of-funnel acquisition into customer lifecycle engagement, delivering $765K in iOPS through a dedicated Engagement channel in 2025. It supports the Testing Approach narrative for Kate and provides the evidence base for the 2026 F90 lifecycle program. After reading, you should understand the three-phase audience strategy, the cross-functional work that made it possible, and the legal and technical dependencies for the next phase.

## Why did Paid Search need an audience strategy?

Paid Search teams typically function as acquisition engines — they target unknown prospects, accept platform limitations, and rely on provided dashboards. This team operated differently. The opportunity was clear: if we could identify which Google users were already Amazon Business customers, we could stop spending acquisition budget on them and start spending engagement budget to drive repeat purchasing. The problem was that Google could only match 13% of our customer list to its user base, making precision targeting nearly impossible.

## How did we build the audience infrastructure?

The team built this capability in three phases. Phase 1 (February 2025) implemented LiveRamp suppression across US and CA campaigns, removing current AB customers from acquisition targeting to reduce wasted spend. This was the plumbing — the foundational audience infrastructure that made everything else possible.

Phase 2 tackled the match rate problem. The team partnered with ABMA (Naresh, Nishchhal) to ingest Associated Accounts — consumer-side emails linked to B2B users — into the Google audience. This was not a Google feature or a platform toggle. It was a manual data integration that required cross-team coordination between PS, ABMA, and MarTech (Joel Mallory). Google match rate jumped from 13% to 30%, more than doubling the addressable audience for engagement campaigns.

Phase 3 built a dedicated Engagement account in partnership with Traffic and Onsite Marketing (Daron Manso), creating a net-new channel that bridged acquisition and lifecycle strategy. With the expanded audience from Phase 2, this channel had the reach to operate at meaningful scale. The core insight across all three phases: platform limitations are problems to solve, not constraints to accept — and that mindset is what enabled the ABMA partnership and the match rate breakthrough.

## What did the Engagement channel deliver?

The Engagement channel drove $765K in iOPS in 2025 (source: Paid Acquisition Flash, Andrew Wirtz). Prime Day 2025 confirmed the channel operates at scale — 80K clicks at -10% cost YoY, $329K OPS at 644% ROAS.

The Engagement account also enabled the Business Essentials launch through Demand Gen placements (see Workstream 5: Algorithmic Ads for DG performance data).

## What is the 2026 F90 plan?

With the Engagement account proven, the team is navigating Legal SIMs to launch the F90 (First 90 Days) program. F90 targets recently acquired, non-purchasing customers to complete 3+ purchases and adopt high-value actions. The goal is to increase the percentage of non-SHuMA customers completing 3+ purchases from 31.7% to 35.4% (+366 bps YoY). The 90-day window aligns with the proposed Guest auto-expiration change from 12 months to 3 months (see Workstream 4: User Experience), creating a coordinated conversion urgency window across both programs.

If LiveRamp 1P approval comes through by end of April, US F90 launches in May. If it slips, the launch delays. Regional expansion is blocked on Tumble with no resolution date. Legal (Matt Rich, Joyce Glancy, Alyssa Stout) is reviewing new audiences and audience-transmission solutions for use across Engagement ad types, and Brand and Paid Media (Abdul Bishar) is coordinating LiveRamp 1P targeting.

If successful, F90 establishes Paid Search as a lifecycle partner, not just a top-of-funnel engine. This is a fundamentally different operating model for the channel — and it connects directly to SSR Activation's (Saajan Chowhan) broader lifecycle strategy.

## What are the risks and open questions?

The Legal SIM timeline is the primary dependency. If LiveRamp 1P positive targeting approval slips past April 2026, the US F90 launch delays accordingly. Regional expansion beyond the US is blocked on Tumble service requirements with no current resolution date. The 31.7% to 35.4% target (+366 bps) assumes the Engagement channel can influence purchasing behavior at sufficient scale — this is directionally supported by the 2025 iOPS results but has not been validated for the specific F90 cohort.

## Cross-functional partners

ABMA (Naresh, Nishchhal) enabled the Associated Accounts ingestion that doubled the Google match rate. Traffic and Onsite Marketing (Daron Manso) co-developed the Engagement account strategy. Legal (Matt Rich, Joyce Glancy, Alyssa Stout) is managing the F90 audience SIMs and LiveRamp data usage approvals. MarTech (Joel Mallory) built the LiveRamp infrastructure and audience transmission. SSR Activation (Saajan Chowhan) owns the F90 lifecycle strategy and promo coordination. Brand and Paid Media (Abdul Bishar) is coordinating LiveRamp 1P targeting.

<!-- AGENT_CONTEXT
machine_summary: "Audiences workstream extended PS beyond acquisition into lifecycle engagement through three phases: LiveRamp suppression (Feb 2025), ABMA Associated Accounts integration (match rate 13% → 30%), and dedicated Engagement account ($765K iOPS 2025, Prime Day 644% ROAS, 12x YoY). 2026: F90 Lifecycle program targeting non-purchasing customers for 3+ purchases within 90 days (31.7% → 35.4%, +366 bps). Legal SIMs in progress — LiveRamp 1P approval on track for US by end of April 2026, regional expansion blocked on Tumble service requirements."
key_entities: ["LiveRamp", "ABMA", "Associated Accounts", "Engagement account", "F90", "Demand Gen", "Prime Day", "iOPS", "Tumble"]
action_verbs: ["suppress", "ingest", "target", "engage", "activate"]
update_triggers: ["F90 Legal SIM resolved", "LiveRamp 1P approval status change", "Engagement channel quarterly performance update", "Tumble service requirements resolved"]
-->
