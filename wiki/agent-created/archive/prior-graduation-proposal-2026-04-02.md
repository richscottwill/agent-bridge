---
title: "Proposal: Prior Graduation Mechanism"
status: archived
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0138 | duck_id: context-prior-graduation-proposal-2026-04-02 -->

# Proposal: Prior Graduation Mechanism

**Source:** Richard + system agent, 2026-04-02 system refresh
**Route to:** Karpathy (sole authority on heart.md, gut.md, experiment protocol)
**Related:** budget-ceiling-observation.md (same session)

## The Problem

Priors accumulate in DuckDB but only influence target selection (UCB scores). The rest of the system — budgets, compression rules, maintenance behavior, organ structure — is still static text. Learning doesn't propagate into system behavior.

Example: eyes×ADD has a 100% keep rate with a positive delta (+0.25). But nothing in the system acts on that knowledge beyond "select eyes×ADD more often." The morning routine doesn't proactively look for facts to inline into Eyes. The budget doesn't adapt.

## The Constraint

Any solution must be:
- **Portable** — survives a platform move with just text files (no DuckDB dependency for behavior)
- **Not hardcoded** — no static if-then rules; derived from data
- **Self-correcting** — new evidence can override old conclusions
- **Scalable** — works at 14 experiments and at 1,400

## Directional Thinking (not a design — Karpathy owns the design)

The priors should periodically "crystallize" into portable text (likely in gut.md) as learned constraints that any agent can read without running a query. The posterior distribution determines confidence. DuckDB is the computation engine; the crystallized text is the portable policy.

Key questions for Karpathy:
1. When should crystallization happen? (cadence, confidence threshold, or event-driven?)
2. Where do learned constraints live? (gut.md section? separate file?)
3. How do crystallized constraints interact with existing static budgets? (replace them? supplement them? override them?)
4. How does the morning routine consume learned constraints during maintenance?
5. What's the minimum n before a prior is worth crystallizing?

## Evidence from Run 16

- 14 experiments, 13 kept, 1 reverted
- ADD experiments produced the only positive deltas (+0.25, +0.0625)
- brain×REMOVE reverted (Δ=-0.3) — RESOLVED decisions aren't dead weight
- aMCC went over budget and the experiment still kept — static budgets blocked by accuracy
- All compression experiments were Δ=0.0 — body was already accurate, compression saves tokens but doesn't improve
