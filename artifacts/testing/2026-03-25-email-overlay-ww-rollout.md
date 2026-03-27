---
title: Email Overlay WW Rollout Plan
status: DRAFT
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: Vijay tech scoping response, Adobe Ad Cloud reporting complete, market launches
---

# Email Overlay WW Rollout Plan

Due: 3/27/2026 | Blocker: Tech scoping (Vijay)

---

## Overview

Email overlay targets existing AB customers who land on acquisition pages via paid search. Today, when an existing customer clicks a paid search ad, they see the standard registration flow — which they can't complete because they already have an account. This inflates acquisition CPA (they count as a click but never convert) and gives the customer a poor experience.

With the overlay, existing customers are identified and redirected to an engagement experience (e.g., product recommendations, account dashboard) instead of the registration page. The expected impact: acquisition CPA improves because existing-customer traffic is removed from the conversion denominator, and existing customers get a relevant experience instead of a dead end.

## Why This Matters

Existing customers hitting acquisition pages inflate our CPA because they don't convert (they're already registered). Redirecting them improves acquisition CPA and gives existing customers a better experience. This is one of the few initiatives that improves both efficiency metrics and customer experience simultaneously.

## Current State

- US: Customer redirect live via Adobe Target
- WW: Rollout pending tech scoping
- Adobe Ad Cloud reporting: In progress (needed to measure existing vs new traffic split)

## Rollout Plan

| Market | Status | Blocker | Target |
|--------|--------|---------|--------|
| US | Live | None | Complete |
| UK | Pending | Tech scoping | Q2 2026 |
| DE | Pending | Tech scoping | Q2 2026 |
| CA | Pending | Tech scoping | Q2 2026 |
| AU | Pending | Tech scoping | Q2 2026 |
| MX | Pending | Tech scoping | Q3 2026 |
| JP | Pending | Tech scoping | Q3 2026 |
| FR/IT/ES | Pending | Tech scoping | Q3 2026 |

Every market except US is blocked by the same thing: Vijay's tech scoping. This is a single-point-of-failure. If Vijay doesn't respond by 3/27, escalate through Brandon.

## Measurement

- Pre-redirect: % of paid search traffic from existing customers (baseline)
- Post-redirect: CPA improvement on acquisition campaigns (existing customer traffic removed)
- Engagement: redirect destination conversion rate

## Dependencies
- Adobe Target implementation per market
- Adobe Ad Cloud reporting segment (in progress — WW redirect task)
- Market-specific redirect destination pages

## Open Items
- [ ] Vijay tech scoping response (escalate if no response by 3/27)
- [ ] Adobe Ad Cloud metric/segment for existing vs new traffic
- [ ] Redirect destination pages per market


## Sources
- US redirect live, WW pending — source: ~/shared/context/body/hands.md → P2 Overdue Items (WW redirect)
- Vijay tech scoping blocker — source: ~/shared/context/active/current.md → Active Projects
- Adobe Ad Cloud reporting in progress — source: ~/shared/context/body/hands.md → Core tasks (WW redirect)
- Due date 3/27 — source: ~/shared/context/active/rw-tracker.md → Backlog

<!-- AGENT_CONTEXT
machine_summary: "WW rollout plan for email overlay that redirects existing AB customers away from acquisition pages. US is live; all other markets blocked by Vijay's tech scoping (single-point-of-failure). Expected impact: lower acquisition CPA and better existing-customer experience."
key_entities: ["email overlay", "Vijay", "Adobe Target", "Adobe Ad Cloud", "acquisition CPA", "existing customers"]
action_verbs: ["redirect", "measure", "escalate", "implement", "rollout"]
update_triggers: ["Vijay tech scoping response", "Adobe Ad Cloud reporting complete", "market launches", "3/27 escalation deadline"]
-->
