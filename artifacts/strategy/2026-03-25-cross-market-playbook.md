---
title: Cross-Market Playbook — US → EU5 → RoW
status: DRAFT
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: new initiative scaling, market priority changes, Brandon direction
---

# Cross-Market Playbook — US → EU5 → RoW

---

## Purpose

Codify the repeatable process for scaling paid search initiatives from US to international markets. Every initiative should follow this playbook instead of being reinvented per market.

## The Scaling Sequence

Brandon's priority order (confirmed 3/20): AU > MX > DE > UK > JP > FR > IT > ES > CA > US-ES

## Playbook Template

### Phase 1: US Validation
- Run the test in US (largest volume, fastest signal)
- Document: hypothesis, test design, results, decision
- Create the "scaling package": what needs to change per market

### Phase 2: Tier 1 Markets (AU, UK, DE)
- Localize the scaling package (translations, currency, market-specific adjustments)
- Launch with same measurement framework
- Duration: match US test duration minimum
- Gate: results within 80% of US lift to proceed

### Phase 3: Tier 2 Markets (CA, JP, FR, IT, ES, MX)
- Apply learnings from Tier 1
- Simplified launch (fewer customizations)
- Batch where possible (EU5 together)

## Initiatives Using This Playbook

| Initiative | US Status | Tier 1 | Tier 2 | Notes |
|-----------|-----------|--------|--------|-------|
| OCI Bidding | Complete (100%) | UK/DE complete, AU not planned | CA/JP/EU3 E2E | Proven methodology |
| Ad Copy | Not started | UK complete, IT low volume | Translations ready | Phase 1 only |
| Polaris LP | US switched 3/24 | AU migrating, weblab Apr 6-7 | Per Brandon priority | AEM translations due 3/26 |
| Email Overlay | US live | Pending tech scoping | Pending | Blocked |
| AI Max | Test design due 3/28 | — | — | US first |

OCI is the most mature — it's been through the full playbook in 3 markets. Ad Copy and Polaris are mid-playbook. AI Max and Email Overlay haven't started the sequence yet.

## What Changes Per Market

| Element | Usually Changes | Usually Stays |
|---------|----------------|---------------|
| Language/copy | ✅ | |
| Currency/budget | ✅ | |
| Keywords | ✅ (local search behavior) | |
| Landing pages | ✅ (Polaris localization) | |
| Test methodology | | ✅ |
| Measurement framework | | ✅ |
| Success criteria thresholds | ✅ (adjust for market size) | |
| Campaign structure | | ✅ (mostly) |

The methodology and measurement framework are the constants. Everything else adapts. This is why the playbook works — it separates what scales from what localizes.

## Handoff Checklist (per market launch)

- [ ] Translated copy approved
- [ ] Landing page live and tested
- [ ] Campaign built in Google Ads
- [ ] Measurement baseline captured (2 weeks pre-launch)
- [ ] Market owner briefed on test parameters
- [ ] Weekly review cadence set
- [ ] Rollback criteria documented


## Sources
- Brandon priority order (AU>MX>DE>UK>JP>FR>IT>ES>CA>US-ES) — source: ~/shared/context/active/current.md → Polaris Brand LP Rollout (3/20)
- Initiative status per market — source: ~/shared/context/body/eyes.md → OCI Performance, Ad Copy Testing, Market Health
- Polaris rollout status — source: ~/shared/context/active/current.md → Active Projects → Polaris Brand LP Rollout
- Scaling methodology — source: ~/shared/context/body/brain.md → D1: OCI Implementation Approach (phased rollout principle)

<!-- AGENT_CONTEXT
machine_summary: "Repeatable playbook for scaling PS initiatives from US validation → Tier 1 (AU/UK/DE) → Tier 2 (CA/JP/FR/IT/ES/MX). Covers OCI, Ad Copy, Polaris, Email Overlay, and AI Max. Brandon's priority order: AU>MX>DE>UK>JP>FR>IT>ES>CA>US-ES."
key_entities: ["cross-market scaling", "OCI", "Ad Copy", "Polaris", "AI Max", "Email Overlay", "Brandon Munday"]
action_verbs: ["scale", "localize", "launch", "measure", "gate"]
update_triggers: ["new initiative added to playbook", "market priority order changes", "initiative completes US validation"]
-->
