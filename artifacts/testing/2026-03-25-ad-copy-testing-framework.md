---
title: Ad Copy Testing Framework
status: DRAFT
doc-type: strategy
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-04-04
update-trigger: new market test results, phase transitions, new copy variants
---

# Ad Copy Testing Framework

---

## Executive Summary

The Sole Proprietor (SP) study (August 2025) revealed that 50% of sole proprietors believed Amazon Business required bulk purchasing and was not free to join. Existing ad copy reinforced both misconceptions. The ad copy testing framework codifies the methodology for replacing misconception-reinforcing messaging with evidence-based copy across all 10 AB Paid Search markets.

UK Phase 1 results validated the approach: +86% CTR and +31% registrations over 30 days. This is Decision D3 — shift messaging from bulk/B2B framing to price, quality, and selection.

---

## Research Foundation: The SP Study

The SP study surveyed sole proprietors on what matters when choosing a business purchasing platform and why they had not signed up.

### What SPs Said Matters Most
| Factor | US Priority | Implication |
|--------|------------|-------------|
| Price | 31% | Lead with value, not volume |
| Product quality | 25% | Emphasize quality assurance |
| Selection | 21% | Highlight breadth of catalog |

### Why SPs Did Not Sign Up
| Barrier | % of SPs | Implication |
|---------|----------|-------------|
| Believed bulk purchasing required | 50% | Our ads reinforced this misconception |
| Savings would not justify costs | 31% | They think it costs money to join |

The insight is stark: our ads were telling half our audience exactly what they feared.

---

## The Messaging Shift

Every copy change maps directly to an SP study finding:

| Old Copy | New Copy | SP Study Rationale |
|----------|----------|-------------------|
| "Online Bulk Purchasing" | "Smart Business Buying" | 50% believed bulk required |
| "Online Wholesale Purchasing" | "For Businesses of All Sizes" | "Wholesale" implies exclusivity |
| "Purchase at Wholesale Price" | "No Minimum Order Required" | Directly addresses the #1 barrier |
| "B2B Marketplace" | "Business Supplies & More" | "B2B" is jargon that excludes sole proprietors |
| "Wholesale Prices" | "Great Prices on Business Essentials" | Leads with price (31% priority) |

These are not cosmetic tweaks. The SP study showed our ads were actively deterring 50% of our target audience. The copy changes remove the two biggest barriers to signup.

---

## Test Methodology

### Phase Structure

Each market follows a three-phase rollout, gated by results:

| Phase | Scope | Duration | Gate to Next Phase |
|-------|-------|----------|-------------------|
| Phase 1 | NB 50% campaigns (High CPA keywords) | 30 days minimum | CTR lift >20% AND reg lift >10% |
| Phase 2 | All NB campaigns | 30 days minimum | CPA within 110% of Phase 1 |
| Phase 3 | Brand Plus campaigns | 30 days minimum | No Brand IS degradation |

Phase 1 targets the highest-CPA NB campaigns because these have the most room for improvement and the clearest signal.

### Test Design Per Phase

| Parameter | Setting | Rationale |
|-----------|---------|-----------|
| Duration | 30 days minimum | Sufficient for learning period + steady-state measurement |
| Split | 50/50 ad rotation | Equal exposure eliminates traffic bias |
| Optimize for conversions | OFF during test | Prevents Google from biasing toward one variant prematurely |
| Primary metric | CTR (leading), Registrations (lagging) | CTR responds first; regs confirm business impact |
| Secondary metrics | CPC, CPA, impression share | Monitor for unintended side effects |
| Confidence threshold | 95% statistical significance | Standard for marketing tests |

The "optimize OFF" setting is critical. Google's default optimization will favor whichever ad gets early clicks, creating a self-fulfilling prophecy.

### Localization Protocol

| Market Group | Translation Method | Status |
|-------------|-------------------|--------|
| US, UK | English originals | Ready |
| AU | English originals (AU English) | Ready |
| DE, FR, IT, ES | GlobalLink translations (delivered 2/18/2026) | Ready |
| JP | Separate translation process (York Chen) | Pending |
| MX | Spanish originals (Richard + Lorena) | Ready |

---

## Results to Date

### UK Phase 1 (Jan 29 - Mar 2, 2026) - HIGH Confidence

| Metric | Test vs Control | Pre/Post |
|--------|----------------|----------|
| CTR | +86% | +70% |
| Clicks | +333% | +28% |
| Registrations | - | +31% |
| Impressions | - | -25% |
| Cost | +230% | - |

The UK result is the proof point. +86% CTR in a test-vs-control design over 30 days is not noise. The pre/post data adds context: registrations increased 31% despite a 25% drop in impressions, meaning the new copy converted at a dramatically higher rate per impression.

The cost increase (+230% test vs control) reflects higher click volume, not higher CPC. More people clicked because the ad was more relevant. CPA improved because more of those clicks converted.

### IT Phase 1 (Feb 19 - Mar 5, 2026) - LOW Confidence

| Metric | Result | Notes |
|--------|--------|-------|
| CTR | +15% directional | Volume too low for significance |
| Clicks | -97% vs control | Insufficient sample |
| Confidence | LOW | Cannot draw conclusions |

IT result is directionally positive but statistically meaningless. Decision: Do not extend IT Phase 1. Move to DE/FR/ES where volume is higher.

---

## Rollout Tracker

| Market | Phase 1 | Phase 2 | Phase 3 | Priority | Notes |
|--------|---------|---------|---------|----------|-------|
| UK | Complete (+86% CTR) | Pending | - | Done | Strong results |
| IT | Complete (inconclusive) | - | - | Low | Volume insufficient |
| DE | Not started | - | - | HIGH | Translations ready, highest EU volume after UK |
| FR | Not started | - | - | HIGH | Translations ready |
| ES | Not started | - | - | MEDIUM | Translations ready |
| US | Not started | - | - | HIGH | English originals ready, largest market |
| AU | Not started | - | - | MEDIUM | English originals ready |
| MX | Not started | - | - | MEDIUM | Spanish originals ready |
| JP | Not started | - | - | LOW | Translations pending |
| CA | Not started | - | - | LOW | English originals ready |

---

## Template for New Market Launch

1. Confirm translated copy is approved and messaging intent is preserved
2. Duplicate existing NB High CPA campaign, replace all ad copy with new variants
3. Set ad rotation to "Do not optimize" (50/50 equal rotation) - non-negotiable during test
4. Capture 2 weeks of pre-test performance baseline (CTR, CPC, CPA, regs)
5. Run 30 days minimum - do not evaluate before 30 days
6. Report: CTR lift, reg lift, CPA impact, confidence level (HIGH/MEDIUM/LOW)
7. Decision: Scale (Phase 2), extend (more data needed), or revert (negative result)

---

## Connection to Other Initiatives

- **OCI:** New copy + OCI bidding compound. Better ads attract higher-intent clicks, and OCI optimizes bids for those clicks. UK's +86% CTR result occurred on OCI-enabled campaigns.
- **Polaris LP:** New ad copy should align with Polaris landing page messaging. If the ad says "No Minimum Order Required" but the LP says "Bulk Purchasing," the disconnect hurts CVR.
- **Competitive response:** Better ad copy improves Quality Score, which improves ad rank without increasing bids. Structural competitive advantage through relevance, not spend.

---

## Sources
- SP Study findings (50% believed bulk required) - source: ~/shared/context/body/eyes.md -> Ad Copy Testing -> Research Foundation
- UK test results (+86% CTR, +31% regs) - source: ~/shared/context/body/eyes.md -> Ad Copy Testing -> Results
- IT test results (+15% CTR, low volume) - source: ~/shared/context/body/eyes.md -> Ad Copy Testing -> Results
- Copy changes (old to new) - source: ~/shared/context/body/eyes.md -> Ad Copy Testing -> What Changed
- Phase structure - source: ~/shared/context/body/eyes.md -> Ad Copy Testing -> Phasing
- EU4 translations delivered 2/18 - source: ~/shared/context/body/eyes.md -> Ad Copy Testing -> Phasing
- Decision D3 rationale - source: ~/shared/context/body/brain.md -> D3: Ad Copy Overhaul
- OCI interaction - source: ~/shared/context/body/eyes.md -> OCI Performance

<!-- AGENT_CONTEXT
machine_summary: "Framework for testing revised ad copy across AB PS markets, driven by SP study finding that 50% of sole proprietors believed AB required bulk purchasing. Messaging shift: bulk/wholesale/B2B to price/quality/selection. UK Phase 1: +86% CTR, +31% regs (HIGH confidence). IT inconclusive. DE/FR/ES/US translations ready. Three-phase rollout per market. Compounds with OCI and Polaris."
key_entities: ["ad copy", "SP study", "sole proprietors", "UK", "IT", "DE", "FR", "ES", "US", "CTR", "registrations", "GlobalLink", "OCI", "Polaris"]
action_verbs: ["test", "localize", "launch", "measure", "scale", "revert"]
update_triggers: ["new market test results available", "phase transition in any market", "new copy variants created"]
-->
