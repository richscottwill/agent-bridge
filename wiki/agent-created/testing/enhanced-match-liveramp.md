---
title: "Enhanced Match / LiveRamp — Audience Expansion for Paid Search"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0402 | duck_id: testing-enhanced-match-liveramp -->

---
title: "Enhanced Match / LiveRamp — Audience Expansion for Paid Search"
status: FINAL
doc-type: strategy
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-04-04
updated: 2026-04-05
update-trigger: Abdul Enhanced Match answers, LiveRamp EU DMA resolution, audience size investigation complete, Legal approval for Enhanced Match
---

# Enhanced Match / LiveRamp — Audience Expansion for Paid Search

This document tracks the Enhanced Match and LiveRamp audience expansion initiative for Paid Search. It covers Brandon's investigation request, the current integration state, open risks that need resolution before scoping, and connections to F90, OCI, and email overlay. After reading, the decision-maker knows what's blocked, what's next, and who owns each action.

## What's Happening

Brandon initiated an Enhanced Match investigation on 3/30, asking Richard to partner with Abdul Bishar to scope the opportunity. Robert Skenes confirmed on 4/3 that Richard's LiveRamp segment is approved and wants parallel implementation between Paid Search and Paid Media segments. Brandon is driving this personally, which means it's moving fast.

Enhanced Match is LiveRamp's capability to improve the match rate between Amazon's customer data and Google's user graph. The current integration sends customer identifiers to Google for audience targeting — suppression and engagement. Enhanced Match expands the data signals sent, potentially increasing the match rate beyond the current 30% achieved through Associated Accounts. A higher match rate means larger addressable audiences, more precise targeting, and less wasted spend on customers we can already identify through other channels.

## Brandon's Four Questions

Brandon asked Richard to get answers from Abdul or Adobe on four specific questions. First, does Enhanced Match require additional data from us, and if so, what data types and what privacy or legal review is required? Second, does it change the data sent to Google — does Adobe provide new data types, or is it just more LiveRamp IDs being matched? Third, do we need new agreements or contracts, and what are the legal implications? Fourth, are any other Amazon orgs using Enhanced Match, which would establish precedent for the legal and technical path?

These questions are unanswered as of April 4. Richard needs to reach out to Abdul and join the Adobe call. Brandon will work with Legal once the technical answers are in.

## Current State and Open Risks

The LiveRamp integration has been live for US Paid Search since February 2025. The match rate started at 13% and improved to 30% through the Associated Accounts partnership with ABMA. The integration supports both suppression (removing existing customers from acquisition campaigns) and engagement (targeting existing customers for lifecycle programs like F90).

Andrew Wirtz flagged a concerning signal on 4/2: the LiveRamp audience dropped from 5.6M to 1.2M between December 14 and March 26 — a 78% decline. If the audience shrank by that magnitude, both suppression and engagement capabilities are significantly degraded. The audience drop investigation should happen before Enhanced Match scoping, because the baseline audience size determines whether Enhanced Match is a 2x opportunity or a marginal improvement.

EU expansion is blocked by the Digital Markets Act. Brandon flagged on 3/31 that DMA restricts data sharing in EU markets, which means match rates will be "much lower than US." This is the same regulatory headwind that affected OCI's EU rollout — DE showed privacy-driven variability in OCI values and longer stabilization windows. Brandon asked Richard to get Abdul's regional availability chart showing where LiveRamp is possible per region. Clara appears to be the blocker on the EU side, with an April 7 due date referenced in the daily brief.

## Connection to Existing Initiatives

Enhanced Match connects to three active programs, and the connections determine its strategic priority. The highest-leverage connection is F90 lifecycle: the match rate is the binding constraint for F90, and if Enhanced Match pushes the rate from 30% to 40-50%, F90's addressable audience nearly doubles. The second connection is OCI bidding — Enhanced Match does not directly affect OCI, but improved audience data quality could indirectly benefit OCI's conversion signal by helping Google better distinguish existing customers from new prospects. The third connection is email overlay, which redirects existing customers away from acquisition pages. Enhanced Match improves identification of existing customers, which means the overlay catches more of them and reduces CPA inflation further.

Brandon announced on 4/3 a new protocol for ABMA-related SIMs — submit at Sev 2.5 with Vijay Kumar (vkumarmp) as watcher for any registration-related issues, including LiveRamp integration problems.

## Next Steps

Richard needs to reach out to Abdul Bishar with Brandon's four questions — this is urgent because Brandon is waiting. Richard also needs to get Abdul's regional availability chart for LiveRamp per region and investigate the 5.6M-to-1.2M audience drop to determine whether it is a LiveRamp legal change or a data pipeline issue. Once the technical answers are in, Brandon will work with Legal on agreements and contracts. Robert Skenes will coordinate segment naming and parallel implementation between PS and Paid Media.

---

## Appendix A: Decision Guide

| Situation | Action |
|-----------|--------|
| Abdul confirms Enhanced Match needs new data types | Escalate to Legal immediately — do not wait for Brandon to initiate |
| Abdul confirms no new data needed (just better matching) | Fast-track: Legal review is lighter, implementation can parallel with Paid Media |
| Audience drop (5.6M→1.2M) is a data pipeline issue | Fix the pipeline first — Enhanced Match on a degraded audience is low-value |
| Audience drop is a legal/consent change | Scope Enhanced Match assuming the smaller audience is the new baseline |
| EU DMA blocks LiveRamp entirely | Focus Enhanced Match on US only, document EU as future opportunity |

This table is for Richard and Brandon. The branching logic depends on two unknowns: what Abdul says about data requirements, and what caused the audience drop. Both answers are needed before the path forward is clear.

## Appendix B: Sources

- Brandon's 4 questions on Enhanced Match — source: Slack DM brandoxy→prichwil, 3/30/2026
- Robert Skenes LiveRamp coordination — source: Slack group DM rskenes/prichwil/arbishar/brandoxy, 4/3/2026
- Brandon EU LiveRamp blocked — source: Slack DM brandoxy→prichwil, 3/31/2026
- LiveRamp audience drop 5.6M→1.2M — source: Slack DM awirtz→prichwil, 4/2/2026
- ABMA SIM escalation protocol — source: Slack ab-paid-search-global, brandoxy, 4/3/2026
- Current match rate (13%→30%) — source: ~/shared/context/body/brain.md → D6: Engagement Channel Creation
- F90 connection — source: ~/shared/artifacts/strategy/2026-03-25-f90-lifecycle-strategy.md
- DMA impact on OCI — source: ~/shared/artifacts/testing/2026-03-25-workstream-oci-bidding.md → DE variance

<!-- AGENT_CONTEXT
machine_summary: "Enhanced Match / LiveRamp audience expansion initiative for Paid Search. Brandon driving investigation (3/30) with 4 specific questions for Abdul/Adobe. Robert Skenes confirmed PS LiveRamp segment approved, wants parallel implementation with Paid Media. EU expansion blocked by DMA. LiveRamp audience dropped 78% (5.6M→1.2M, Dec-Mar) — needs investigation before scoping. Connects to F90 (match rate is binding constraint), OCI (cleaner conversion signals), and email overlay (better existing customer identification). Decision guide in Appendix A covers five scenarios. New ABMA SIM escalation protocol: Sev 2.5 + Vijay Kumar as watcher."
key_entities: ["Enhanced Match", "LiveRamp", "Abdul Bishar", "Robert Skenes", "Brandon Munday", "ABMA", "DMA", "F90", "Clara", "Andrew Wirtz", "Vijay Kumar"]
action_verbs: ["investigate", "scope", "coordinate", "escalate", "implement"]
update_triggers: ["Abdul answers Brandon's 4 questions", "LiveRamp EU DMA resolution", "audience size investigation complete", "Legal approval for Enhanced Match"]
decision_guide: "Appendix A: 5 scenarios — new data needed (escalate Legal), no new data (fast-track), audience drop is pipeline (fix first), audience drop is legal (scope on smaller baseline), EU blocked (US-only focus)"
-->
