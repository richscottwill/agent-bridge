---
title: Enhanced Match / LiveRamp — Audience Expansion for Paid Search
status: DRAFT
doc-type: strategy
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-04-04
updated: 2026-04-04
update-trigger: Abdul Enhanced Match answers, LiveRamp EU DMA resolution, audience size changes, Legal approval status
tags: [liveramp, enhanced-match, audience, abma, abdul, legal, dma]
---

# Enhanced Match / LiveRamp — Audience Expansion for Paid Search

---

## What's Happening

Brandon initiated an Enhanced Match investigation on 3/30, asking Richard to partner with Abdul Bishar (Brand & Paid Media) to scope the opportunity. Robert Skenes confirmed on 4/3 that Richard's LiveRamp segment is approved and wants parallel implementation between Paid Search and Paid Media segments. This is moving fast — Brandon is driving it personally.

Enhanced Match is LiveRamp's capability to improve the match rate between Amazon's customer data and Google's user graph. The current LiveRamp integration sends customer identifiers to Google for audience targeting (suppression, engagement). Enhanced Match expands the data signals sent, potentially increasing the match rate beyond the current 30% achieved through Associated Accounts.

The opportunity is significant: a higher match rate means larger addressable audiences for both suppression (removing existing customers from acquisition campaigns) and engagement (targeting existing customers for lifecycle programs like F90). Every percentage point of match rate improvement translates to more precise targeting and less wasted spend.

---

## Brandon's Four Questions (3/30)

Brandon asked Richard to get answers from Abdul or Adobe on these specific questions:

1. **Does Enhanced Match require additional data from us?** If so, what data types and what's the privacy/legal review required?
2. **Does it change the data sent to Google?** Does Adobe provide new data types, or is it just more LiveRamp IDs being matched?
3. **Do we need new agreements or contracts?** Legal implications for data sharing.
4. **Are any other Amazon orgs using it?** Precedent within Amazon for the legal and technical path.

These questions are unanswered as of 4/4. Richard needs to reach out to Abdul and/or join the Adobe call to get answers. Brandon said she'll work with Legal once the technical answers are in.

---

## Current State

The LiveRamp integration has been live for US Paid Search since February 2025 (LiveRamp suppression, then Engagement account). The current architecture:

- Amazon customer data → LiveRamp → Google Ads audience lists
- Match rate: started at 13%, improved to 30% via Associated Accounts (ABMA partnership)
- Used for: suppression (removing existing customers from acquisition targeting) and engagement (F90 lifecycle targeting)

A concerning signal from Andrew Wirtz (4/2): the LiveRamp audience dropped from 5.6M to 1.2M between December 14 and March 26, 2026. Andrew asked if this was related to LiveRamp legal changes during that period. This audience size drop needs investigation — if the audience shrank by 78%, the suppression and engagement capabilities are significantly degraded.

---

## EU Expansion — Blocked by DMA

Brandon flagged (3/31) that EU LiveRamp expansion is blocked. The Digital Markets Act (DMA) restricts data sharing in EU markets, which means match rates will be "much lower than US." Brandon asked Richard to get Abdul's regional availability chart (which shows where LiveRamp is possible per region) and scope the potential impact given DMA constraints.

This is the same DMA issue that affected OCI's EU rollout — the DE privacy-driven variability in OCI values and the longer stabilization windows for EU4 markets. LiveRamp EU faces the same regulatory headwind.

The EU team wants to launch LiveRamp, but the path is unclear. Clara (referenced in daily brief 4/1) appears to be the blocker — "Enhanced Match / LiveRamp EU — due Apr 7, blocked across Amazon."

---

## Connection to Existing Initiatives

Enhanced Match connects to three active programs:

**F90 Lifecycle:** The match rate is the binding constraint for F90. At 30%, F90 can target a meaningful audience. If Enhanced Match pushes the rate to 40-50%, F90's addressable audience nearly doubles. This is the highest-leverage connection.

**OCI Bidding:** Enhanced Match doesn't directly affect OCI, but the audience data quality improvement could indirectly benefit OCI's conversion signal — if Google can better identify which users are existing customers vs. new prospects, the bidding algorithm gets cleaner data.

**Email Overlay:** The email overlay redirects existing customers away from acquisition pages. Enhanced Match improves the identification of existing customers, which means the overlay catches more of them — reducing CPA inflation further.

---

## ABMA SIM Escalation Protocol (New)

Brandon announced on 4/3 a new protocol for ABMA-related SIMs: submit all SIMs requiring ABMA on-call support at Sev 2.5 severity, and include Vijay Kumar (vkumarmp) as a watcher if the SIM is related to registration. This was driven by "slow reaction times from ABMA on-call." The protocol is documented in the Paid Acq SIM doc.

This is relevant to Enhanced Match because any technical issues with the LiveRamp integration will require ABMA on-call support. The new escalation protocol ensures faster response.

---

## Next Steps

1. Richard: Reach out to Abdul Bishar with Brandon's 4 questions (URGENT — Brandon is waiting)
2. Richard: Get Abdul's regional availability chart for LiveRamp per region
3. Richard: Investigate the 5.6M → 1.2M audience drop (Dec-Mar) — is this LiveRamp legal changes or a data issue?
4. Brandon: Work with Legal once technical answers are in
5. Robert Skenes: Coordinate segment naming and parallel implementation between PS and Paid Media

---

## Sources
- Brandon's 4 questions on Enhanced Match — source: Slack DM brandoxy→prichwil, 3/30/2026 (ab-ps_partnership-accounts channel)
- Robert Skenes LiveRamp coordination — source: Slack group DM rskenes/prichwil/arbishar/brandoxy, 4/3/2026
- Brandon EU LiveRamp blocked — source: Slack DM brandoxy→prichwil, 3/31/2026
- LiveRamp audience drop 5.6M→1.2M — source: Slack DM awirtz→prichwil, 4/2/2026
- ABMA SIM escalation protocol — source: Slack ab-paid-search-global, brandoxy, 4/3/2026
- Current match rate (13%→30%) — source: ~/shared/context/body/brain.md → D6: Engagement Channel Creation
- F90 connection — source: ~/shared/artifacts/strategy/2026-03-25-f90-lifecycle-strategy.md
- DMA impact on OCI — source: ~/shared/artifacts/testing/2026-03-25-workstream-oci-bidding.md → DE variance

<!-- AGENT_CONTEXT
machine_summary: "New initiative: Enhanced Match / LiveRamp audience expansion for Paid Search. Brandon driving investigation (3/30) with 4 specific questions for Abdul/Adobe. Robert Skenes confirmed PS LiveRamp segment approved, wants parallel implementation with Paid Media. EU expansion blocked by DMA. LiveRamp audience dropped 78% (5.6M→1.2M, Dec-Mar) — needs investigation. Connects to F90 (match rate is binding constraint), OCI (cleaner conversion signals), and email overlay (better existing customer identification). New ABMA SIM escalation protocol: Sev 2.5 + Vijay Kumar as watcher."
key_entities: ["Enhanced Match", "LiveRamp", "Abdul Bishar", "Robert Skenes", "Brandon Munday", "ABMA", "DMA", "F90", "Clara"]
action_verbs: ["investigate", "scope", "coordinate", "escalate", "implement"]
update_triggers: ["Abdul answers Brandon's 4 questions", "LiveRamp EU DMA resolution", "audience size investigation complete", "Legal approval for Enhanced Match"]
-->
