---
title: "Q2 2026 Initiative Status & Priorities"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0389 | duck_id: strategy-q2-initiative-status -->

---
title: Q2 2026 Initiative Status & Priorities
status: DRAFT
doc-type: strategy
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-04-04
updated: 2026-04-04
update-trigger: initiative status changes, new initiatives launched, quarterly planning
tags: q2, initiatives, status, brandon, team
---

# Q2 2026 Initiative Status & Priorities

> Single-page view of every active AB Paid Search initiative entering Q2 2026. Designed for Brandon's team management and upward reporting to Kate.

---

## Executive Summary

AB Paid Search enters Q2 2026 with strong momentum on its core initiatives but several execution gaps that need attention. OCI is the headline story: 7 of 10 markets are now at 100% (up from 3 at the start of Q1), with CA targeting April 7 for dial-up. The ad copy test produced the quarter's strongest result (+86% CTR in UK). Polaris LP rollout is mid-execution with the US weblab targeting April 6-7.

The gaps are concentrated in two areas: (1) strategic artifacts that have not shipped despite being planned (Testing Approach doc for Kate, AI Max test design, AEO POV), and (2) single-point-of-failure dependencies that are blocking multiple markets (Vijay on email overlay, finance on OP2 plan numbers for budget tooling).

Eight of ten markets are beating or matching OP2 on March projections. JP is the only market materially below plan (-14%), driven by the structural MHLW campaign ending. The team's competitive position is stable — Walmart remains the only sustained Brand threat (US), and the efficiency-over-escalation strategy is working.

---

## Initiative Scorecard

### Tier 1: In-Flight, High Impact

| Initiative | Owner | Markets | Status | Q2 Target | Risk |
|-----------|-------|---------|--------|-----------|------|
| OCI Rollout | Richard/Andrew | 10 | 7/10 at 100%. CA dial-up 4/7. AU/MX excluded. | CA at 100% by Jul. Monitor EU3 lift. | LOW — proven methodology |
| Polaris Brand LP | Stacey/Richard | 10 | US live (3/24). Weblab 4/6-7. AU migrating. | AU/MX/DE/UK live by end Q2. | MEDIUM — AEM translations are the constraint |
| Ad Copy Testing | Andrew/Richard | 10 | UK Phase 1 complete (+86% CTR). IT inconclusive. | Launch Phase 1 in DE/FR/ES/US. | LOW — translations ready |
| Testing Approach Doc | Richard | N/A | NOT STARTED (14 workdays). Brandon reviewing before Kate. | Complete and reviewed by Brandon. | HIGH — 0 progress, Level 1 gate |

### Tier 2: Planned, Pending Launch

| Initiative | Owner | Markets | Status | Q2 Target | Blocker |
|-----------|-------|---------|--------|-----------|---------|
| AI Max Test | Richard/Stacey | US | Test design 6d overdue (was due 3/28). | Launch US test Q2. | Google sync with Mike Babich needed |
| Project Baloo | TBD | US | Early access launched 3/30. Keywords delivered. | Evaluate early access data. Decision on full test. | Cost guardrails TBD |
| F90 Lifecycle | Richard | US | Legal approved. Engagement channel built. | Launch if match rate reaches 25%. | ABMA match rate (13% current, 30% target) |
| Email Overlay WW | Richard | 9 | US live. All others blocked. | Unblock tech scoping. Launch UK/DE. | Vijay tech scoping (single-point-of-failure) |

### Tier 3: Strategic / Queued

| Initiative | Owner | Status | Q2 Target | Notes |
|-----------|-------|--------|-----------|-------|
| AEO / AI Overviews POV | Richard | Queued (Level 4) | Draft POV if Level 1 gate passes | Depends on Level 1 consistency |
| Campaign Link Generator | Richard | Spec written | Build v1, convert to Sheets | Level 3 team adoption play |
| Budget Forecast Helper | Richard | Spec written, blocked | Build if OP2 numbers obtained | Blocked on finance data |
| AU NB MRO/Trades Test | Richard | Proposal stage | Launch if Alexis confirms LP | Budget-neutral, market-specific |

---

## What's Working

OCI is the headline: 7/10 markets at 100%, $16.7MM OPS from US alone. Ad copy testing produced the quarter's strongest non-OCI result (+86% CTR in UK). Eight of ten markets are beating or matching OP2 on March projections.

## What Needs Attention

The Testing Approach doc has not started (14 workdays at zero). AI Max test design is 6 days overdue. Email overlay has 9 markets blocked by one dependency (Vijay). JP is -14% vs OP2 with a structural MHLW gap. Each has a defined path forward — the risk is not complexity, it's execution discipline.

---

## Q2 Priorities (Recommended)

In order of leverage:

1. **Ship the Testing Approach doc.** This unlocks Level 1 graduation, Kate visibility, and team credibility. Everything else is secondary until this ships.

2. **Launch AI Max US test.** Complete the Google sync, finalize the test design, and launch. AI Max is the next OCI-scale opportunity — early testing positions the team ahead of Google's automation curve.

3. **Scale ad copy to DE/FR/ES/US.** Translations are ready. The UK result is the proof point. This is low-risk, high-reward execution.

4. **Unblock email overlay.** Escalate Vijay if needed. Nine markets waiting on one deliverable is not acceptable.

5. **Monitor OCI EU3 + JP lift.** These markets just went live. The first 4-6 weeks of data will determine whether the OCI playbook holds at scale.

---

## Key Dates

| Date | Event | Owner |
|------|-------|-------|
| Apr 6-7 | Polaris US weblab dial-up | Stacey |
| Apr 7 | CA OCI dial-up target | Richard |
| Mid-Apr | Email overlay escalation deadline | Richard/Brandon |
| Apr 16 | Kate meeting (CANCELED — doc review first) | Richard/Brandon |
| Late Apr | AI Max Google sync target | Richard/Mike Babich |
| May 2026 | AU OCI target (Adobe, unconfirmed) | Richard/Suzane |
| Q2 | F90 US launch (if match rate gate met) | Richard |

---

## Sources
- OCI status (7/10 at 100%) — source: ~/shared/context/body/eyes.md -> OCI Performance
- Ad copy UK results (+86% CTR) — source: ~/shared/context/body/eyes.md -> Ad Copy Testing
- Market performance vs OP2 — source: ~/shared/context/body/eyes.md -> Market Health
- Testing Approach doc status (14 workdays) — source: ~/shared/context/body/memory.md -> Active Projects
- AI Max overdue (6d) — source: ~/shared/context/body/eyes.md -> What's Coming
- Brandon 1:1 context (4/2) — source: ~/shared/context/body/memory.md -> Brandon Munday
- Kate meeting canceled — source: ~/shared/context/body/memory.md -> Kate Rundell
- JP MHLW headwind — source: ~/shared/context/body/eyes.md -> Market Health -> JP
- Project Baloo early access — source: ~/shared/context/body/eyes.md -> What's Coming
- Email overlay blocker — source: ~/shared/context/active/current.md -> Active Projects

<!-- AGENT_CONTEXT
machine_summary: "Q2 2026 initiative scorecard for AB Paid Search. 4 Tier 1 initiatives (OCI 7/10 markets, Polaris rollout, ad copy scaling, Testing Approach doc), 4 Tier 2 (AI Max, Baloo, F90, email overlay), 4 Tier 3 (AEO POV, tools, AU NB test). Key gaps: Testing Approach doc at 0 progress (14 workdays), AI Max 6d overdue, email overlay blocked by Vijay. 8/10 markets at or above OP2. Recommended Q2 priority order: ship Testing Approach > launch AI Max > scale ad copy > unblock email overlay > monitor OCI lift."
key_entities: ["OCI", "Polaris", "ad copy", "AI Max", "Baloo", "F90", "email overlay", "Testing Approach", "Brandon", "Kate", "Vijay"]
action_verbs: ["ship", "launch", "scale", "unblock", "monitor", "escalate"]
update_triggers: ["initiative status changes", "new initiatives launched", "quarterly planning", "Kate meeting rescheduled"]
-->
