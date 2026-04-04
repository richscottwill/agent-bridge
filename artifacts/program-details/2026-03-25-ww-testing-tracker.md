---
title: WW Testing Tracker — All Active & Planned Tests
status: DRAFT
doc-type: reference
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-04-04
update-trigger: test status changes, new tests launched, results available
---

# WW Testing Tracker

> Master tracker for every active, planned, and completed test across all 10 AB Paid Search markets. Updated when test status changes.

---

## Portfolio Health

The testing portfolio is in good shape entering Q2 2026. The team is running 10 active tests across 8 markets simultaneously, with 8 more planned. The completed tests have a strong track record: OCI validated in 3 markets with consistent 18-24% registration lift, and the CA LP optimization produced the highest CVR improvement in the program's history (+187%).

Two items need attention:
- **AI Max test design is 6 days overdue** (was due 3/28). This is the highest-priority planned test and the next OCI-scale opportunity. Needs Google sync with Mike Babich before launch.
- **Email overlay WW is blocked by a single dependency** (Vijay tech scoping). Nine markets are waiting on one deliverable.

The OCI E2E tests in EU3 and JP have progressed faster than expected — FR/IT/ES dialed up on 3/30 and JP on 3/31, moving them from E2E to 100% live. CA is the last market in the current wave, targeting 4/7.

---

## Active Tests

| # | Test | Market | Status | Start | End | Owner | Result |
|---|------|--------|--------|-------|-----|-------|--------|
| 1 | OCI | CA | E2E, dial-up 4/7 | 3/4/26 | — | Richard | On track |
| 2 | OCI | JP | 100% live | 2/26/26 | 3/31 dial-up | York | Monitoring lift |
| 3 | OCI | FR | 100% live | 2/26/26 | 3/30 dial-up | Andrew | Monitoring lift |
| 4 | OCI | IT | 100% live | 2/26/26 | 3/30 dial-up | Andrew | Monitoring lift |
| 5 | OCI | ES | 100% live | 2/26/26 | 3/30 dial-up | Andrew | Monitoring lift |
| 6 | Ad Copy Phase 1 | UK | Complete | 1/29/26 | 3/2/26 | Andrew | +86% CTR, +31% regs (HIGH) |
| 7 | Ad Copy Phase 1 | IT | Complete | 2/19/26 | 3/5/26 | Andrew | +15% CTR (LOW — insufficient volume) |
| 8 | Polaris Brand LP | US | Live | 3/24/26 | — | Stacey | Switched, weblab Apr 6-7 |
| 9 | Polaris Brand LP | AU | In Progress | 3/24/26 | — | Richard | Full migration (Lena's decision, no 50/50) |
| 10 | Customer Redirect | US | Live | — | — | Richard | Monitoring |

---

## Planned Tests

| # | Test | Market | Target Start | Owner | Blocker | Priority |
|---|------|--------|-------------|-------|---------|----------|
| 11 | AI Max | US | Q2 2026 | Richard | Test design overdue (was 3/28). Google sync needed. | HIGH |
| 12 | Ad Copy Phase 2 | UK | TBD | Andrew | Phase 1 results reviewed | MEDIUM |
| 13 | Ad Copy Phase 1 | DE/FR/ES | TBD | Andrew | Translations ready, awaiting launch | HIGH |
| 14 | Email Overlay WW | UK+ | TBD | Richard | Vijay tech scoping (single-point-of-failure) | HIGH |
| 15 | AU NB MRO/Trades | AU | TBD | Richard | Keyword research + Alexis LP confirmation | MEDIUM |
| 16 | Polaris Brand LP | MX/DE/UK/JP+ | Apr 2026+ | Per market | AEM translations + EU5 ops ticket | MEDIUM |
| 17 | Project Baloo | US | Q2 2026 | TBD | Cost guardrails + product feed setup | HIGH |
| 18 | F90 Lifecycle | US | Q2 2026 | Richard | ABMA match rate (13% current, 25% gate) | MEDIUM |

### What's Blocked and Why

| Blocker | Tests Affected | Owner | Escalation Path |
|---------|---------------|-------|-----------------|
| Vijay tech scoping | Email Overlay (9 markets) | Vijay | Richard -> Brandon if no response by mid-April |
| Google sync (Mike Babich) | AI Max test design | Richard | Schedule in first 2 weeks of Q2 |
| ABMA match rate | F90 Lifecycle | ABMA team | No escalation path yet — partnership in progress |
| EU5 AEM ops ticket | Polaris FR/IT/ES | Andrew | Andrew -> Brandon if not resolved by mid-April |
| Cost guardrails | Project Baloo | Richard/Vijay | 1:1 with Vijay (3/26) started the discussion |

---

## Completed Tests (2025-2026)

| # | Test | Market | Period | Result | Impact | Decision |
|---|------|--------|--------|--------|--------|----------|
| C1 | OCI Full Rollout | US | Jul-Oct 2025 | +24% regs, ~50% NB CPA | $16.7MM OPS | SCALED to 100% |
| C2 | OCI Full Rollout | UK | Aug-Oct 2025 | +23% regs | Notable | SCALED to 100% |
| C3 | OCI Full Rollout | DE | Oct-Dec 2025 | +18% regs | Notable | SCALED to 100% |
| C4 | LP Optimization | CA | 2025 | Bulk +187% CVR, Wholesale +180% | Notable | SCALED — framework applied to EU5 |
| C5 | In-Context Registration | US | Q2-Q3 2025 | +13.6K annualized regs | 100% probability (APT) | SCALED WW |
| C6 | Gated Guest | US | 2025 | -61% regs, -24% OPS | Negative | STOPPED — informed in-context pivot |

Every completed test either validated and scaled, or failed and informed the next test. The Gated Guest failure directly led to the in-context registration success (+13.6K regs). This is the methodology working as designed.

---

## Test Pipeline by Workstream

| Workstream | Active | Planned | Completed | Next Milestone |
|-----------|--------|---------|-----------|----------------|
| OCI Bidding | 1 (CA) | 0 | 3 (US/UK/DE) + 4 just went live (FR/IT/ES/JP) | CA dial-up 4/7 |
| Ad Copy | 0 | 3 (UK Phase 2, DE/FR/ES Phase 1) | 2 (UK Phase 1, IT Phase 1) | Launch DE/FR/ES Phase 1 |
| Polaris LP | 2 (US weblab, AU migration) | 1 (MX/DE/UK/JP+) | 0 | US weblab Apr 6-7 |
| Email Overlay | 1 (US live) | 1 (WW rollout) | 0 | Unblock Vijay |
| AI Max | 0 | 1 (US) | 0 | Complete test design |
| Baloo | 0 | 1 (US) | 0 | Finalize cost guardrails |
| F90 Lifecycle | 0 | 1 (US) | 0 | Match rate gate (25%) |
| AU NB | 0 | 1 (MRO/Trades) | 0 | Alexis LP confirmation |

---

## Sources
- OCI rollout status (7/10 at 100%) — source: ~/shared/context/body/eyes.md -> OCI Performance
- Ad copy results — source: ~/shared/context/body/eyes.md -> Ad Copy Testing
- Polaris status — source: ~/shared/context/active/current.md -> Polaris Brand LP Rollout
- AI Max, Baloo, F90 — source: ~/shared/context/body/eyes.md -> What's Coming
- CA LP results — source: ~/shared/context/body/eyes.md -> Market Health -> CA
- In-context registration and Gated Guest — source: ~/shared/artifacts/testing/2026-03-25-workstream-user-experience.md
- Blocker analysis — source: ~/shared/context/body/hands.md -> P2 Overdue Items

<!-- AGENT_CONTEXT
machine_summary: "Master tracker for all AB PS tests. 10 active (1 OCI E2E in CA, 4 OCI just went live in FR/IT/ES/JP, 2 ad copy complete, 2 Polaris, 1 redirect), 8 planned (AI Max HIGH priority but overdue, email overlay blocked by Vijay, ad copy DE/FR/ES ready, Baloo, F90, AU NB, Polaris WW), 6 completed (OCI US/UK/DE, CA LP, in-context reg, Gated Guest stopped). Portfolio health: strong track record, two blockers need attention (AI Max overdue, email overlay stuck)."
key_entities: ["OCI", "ad copy", "Polaris", "AI Max", "email overlay", "F90", "Baloo", "AU NB MRO", "Vijay", "Mike Babich"]
action_verbs: ["track", "launch", "monitor", "evaluate", "scale", "unblock"]
update_triggers: ["test status changes", "new test launched", "test results available", "blocker resolved"]
-->
