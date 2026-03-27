---
title: WW Testing Tracker — All Active & Planned Tests
status: DRAFT
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: test status changes, new tests launched, results available
---

# WW Testing Tracker

Operational complement to the Testing Approach doc. Every active and planned test across all markets, with status, owners, and results.

## Active Tests

| # | Test | Market | Status | Start | End | Owner | Result |
|---|------|--------|--------|-------|-----|-------|--------|
| 1 | OCI E2E | CA | In Progress | 3/4/26 | — | Richard | Monitoring |
| 2 | OCI E2E | JP | In Progress | 2/26/26 | — | York | Monitoring |
| 3 | OCI E2E | FR | In Progress | 2/26/26 | — | Andrew | Monitoring |
| 4 | OCI E2E | IT | In Progress | 2/26/26 | — | Andrew | Monitoring |
| 5 | OCI E2E | ES | In Progress | 2/26/26 | — | Andrew | Monitoring |
| 6 | Ad Copy Phase 1 | UK | Complete | 1/29/26 | 3/2/26 | Andrew | +86% CTR, +31% regs |
| 7 | Ad Copy Phase 1 | IT | Complete | 2/19/26 | 3/5/26 | Andrew | +15% CTR (low vol) |
| 8 | Polaris Brand LP | US | Live | 3/24/26 | — | Stacey | Switched, weblab Apr 6-7 |
| 9 | Polaris Brand LP | AU | In Progress | 3/24/26 | — | Richard | Full migration (Lena) |
| 10 | Customer Redirect | US | Live | — | — | Richard | Monitoring |

5 OCI E2E tests running simultaneously across CA/JP/EU3. Ad copy Phase 1 complete in UK (strong) and IT (inconclusive). Polaris US is live, AU migrating.

## Planned Tests

| # | Test | Market | Target Start | Owner | Blocker |
|---|------|--------|-------------|-------|---------|
| 11 | AI Max | US | Q2 2026 | Richard | Test design due 3/28 |
| 12 | Ad Copy Phase 2 | UK | TBD | Andrew | Phase 1 results reviewed |
| 13 | Ad Copy Phase 1 | DE/FR/ES | TBD | Andrew | Translations ready |
| 14 | Email Overlay WW | UK+ | TBD | Richard | Tech scoping (Vijay) |
| 15 | AU NB MRO/Trades | AU | TBD | Richard | Keyword research |
| 16 | Polaris Brand LP | MX/DE/UK/JP+ | Apr 2026+ | Per market | AEM translations |
| 17 | Project Baloo | US | Q2 2026 | TBD | Shopping Ads for AB |
| 18 | F90 Lifecycle | US | Q2 2026 | Richard | Match rate improvement |

AI Max (due 3/28) and Email Overlay (blocked by Vijay) are the two highest-priority planned tests. AU NB MRO/Trades is a market-specific opportunity, not a WW initiative.

## Completed Tests (2025-2026)

| # | Test | Market | Result | Impact | Decision |
|---|------|--------|--------|--------|----------|
| C1 | OCI Full Rollout | US | +24% regs, ~50% NB CPA | $16.7MM OPS | SCALED |
| C2 | OCI Full Rollout | UK | +23% regs | Notable | SCALED |
| C3 | OCI Full Rollout | DE | +18% regs | Notable | SCALED |
| C4 | LP Optimization | CA | Bulk +187% CVR, Wholesale +180% | Notable | SCALED |

OCI is the proven playbook. Every completed test validated the phased methodology. CA LP optimization shows the same pattern works for landing pages.

## Sources
- OCI rollout status — source: ~/shared/context/body/eyes.md → OCI Performance
- Ad copy results — source: ~/shared/context/body/eyes.md → Ad Copy Testing
- Polaris status — source: ~/shared/context/active/current.md → Polaris Brand LP Rollout
- AI Max, Baloo, F90 — source: ~/shared/context/body/eyes.md → What's Coming
- CA LP results — source: ~/shared/context/body/eyes.md → Market Health → CA

<!-- AGENT_CONTEXT
machine_summary: "Master tracker for all active, planned, and completed AB PS tests across all markets. 10 active tests (5 OCI E2E, 2 ad copy, 2 Polaris, 1 redirect), 8 planned (AI Max, ad copy expansion, email overlay, Baloo, F90), 4 completed (OCI US/UK/DE, CA LP)."
key_entities: ["OCI", "ad copy", "Polaris", "AI Max", "email overlay", "F90", "Baloo", "AU NB MRO"]
action_verbs: ["track", "launch", "monitor", "evaluate", "scale"]
update_triggers: ["test status changes", "new test launched", "test results available", "blocker resolved"]
-->
