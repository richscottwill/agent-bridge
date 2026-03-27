---
title: OCI Methodology — Knowledge Sharing Doc
status: DRAFT
audience: amazon-internal
level: 1
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: new OCI market results, methodology changes, team questions
---

# OCI Methodology — Knowledge Sharing Doc

> This is the simplified team reference. For the full methodology, see oci-rollout-methodology. For per-market execution steps, see oci-implementation-guide.

---

## Purpose

Document the OCI rollout methodology so any team member can understand, reference, and replicate it without asking Richard. Addresses Annual Review feedback: "proactively share knowledge" and "simplify complex subjects for broader team benefit."

## What is OCI?

Optimized Conversions with Intelligence — Google's conversion-based bidding system. Instead of manual CPC bids, OCI uses machine learning to optimize bids toward a target CPA or maximize conversions within a budget.

## Why We Use It

Manual bidding doesn't scale across 10 markets. OCI has delivered:
- US: +24% regs, ~50% NB CPA improvement
- UK: +23% regs
- DE: +18% regs

## How We Roll It Out

We use a phased rollout: E2E → 25% → 50% → 100% NB. Each phase has a CPA gate (115% at 25%, 110% at 50%). Full details in [OCI Rollout Methodology](~/shared/artifacts/testing/2026-03-25-oci-rollout-methodology.md).

## What NOT to Do
- Don't judge OCI by week 1 — the algorithm needs 2-4 weeks to learn
- Don't use OCI on Brand campaigns — manual bid caps needed for Walmart defense
- Don't compare raw pre/post — use seasonality-adjusted baselines
- Don't panic if CPA spikes in week 1 — it normalizes
- Don't compare OCI markets to non-OCI markets directly — AU/MX don't have OCI, so their CPA trajectory is fundamentally different

## Current Status Across Markets

| Market | Status | Key Metric |
|--------|--------|-----------|
| US | 100% NB | +24% regs, $16.7MM OPS |
| UK | 100% NB | +23% regs |
| DE | 100% NB | +18% regs |
| CA | E2E (Mar 2026) | Monitoring |
| JP | E2E (Feb 2026) | Monitoring |
| FR/IT/ES | E2E (Feb 2026) | Monitoring |
| AU/MX | Not planned | No OCI support |

Three markets proven, five in E2E, two excluded. The methodology is validated — the remaining markets are execution, not experimentation.

## How to Check OCI Performance

1. Google Ads → Campaigns → filter NB
2. Compare: this week CPA vs 4-week trailing average
3. Check: conversion tracking status (any errors?)
4. Flag: CPA >120% of trailing average for 7+ days → investigate

## Questions?

For deeper methodology questions, see oci-rollout-methodology. For implementation troubleshooting, see oci-implementation-guide.


## Sources
- OCI definition and phased rollout — source: ~/shared/context/body/brain.md → D1: OCI Implementation Approach
- Results per market — source: ~/shared/context/body/eyes.md → OCI Performance → Impact Summary
- Market status table — source: ~/shared/context/body/eyes.md → OCI Performance → Rollout Timeline
- "Don't judge by week 1" and lessons — source: ~/shared/context/body/eyes.md → OCI Performance (operational experience)
- Brand campaigns manual (Walmart defense) — source: ~/shared/context/body/brain.md → D2: Competitive Response to Walmart
- Annual Review feedback ("proactively share knowledge") — source: ~/shared/context/body/memory.md → Brandon relationship entry (3/24)

<!-- AGENT_CONTEXT
machine_summary: "Simplified OCI methodology reference for team knowledge sharing. Explains what OCI is, the phased rollout playbook (E2E → 25% → 50% → 100%), common mistakes to avoid, and current market status. Three markets at 100%, five in E2E, two excluded."
key_entities: ["OCI", "Google Ads", "NB campaigns", "US", "UK", "DE", "CA", "JP", "EU3", "AU", "MX"]
action_verbs: ["enable", "scale", "monitor", "gate", "compare"]
update_triggers: ["new OCI market results", "methodology changes", "team questions about OCI", "OCI support added to AU/MX"]
-->
