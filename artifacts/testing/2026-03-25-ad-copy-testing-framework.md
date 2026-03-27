---
title: Ad Copy Testing Framework
status: DRAFT
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: new market test results, phase transitions, new copy variants
---

# Ad Copy Testing Framework

---

## Background

The Sole Proprietor (SP) study (Aug 2025) revealed that 50% of SPs believed AB required bulk purchasing and was not free. Existing ad copy reinforced both misconceptions. We shifted messaging from bulk/wholesale/B2B → price, quality, selection.

## Methodology

### Phase Structure
1. Phase 1: NB 50% campaigns (High CPA) — test new copy against control
2. Phase 2: All NB campaigns
3. Phase 3: Brand Plus campaigns

### Test Design
- Duration: 30 days minimum per phase
- Split: 50/50 ad rotation (optimize for conversions OFF during test)
- Primary metric: CTR (leading indicator), Registrations (lagging)
- Secondary: CPC, CPA, impression share

### Localization
- US/UK: English originals
- EU4 (DE, FR, IT, ES): GlobalLink translations (delivered 2/18/2026)
- JP: Separate translation process
- AU/MX: English/Spanish originals

## Results to Date

| Market | Phase | Duration | CTR Lift | Reg Lift | Confidence |
|--------|-------|----------|----------|----------|------------|
| UK | 1 | Jan 29 - Mar 2 | +86% | +31% | HIGH |
| IT | 1 | Feb 19 - Mar 5 | +15% | Insufficient volume | LOW |

UK Phase 1 is HIGH confidence — the methodology works. IT is LOW confidence — volume was insufficient to draw conclusions. Next priority: launch Phase 1 in DE/FR/ES where translations are ready.

## Key Copy Changes

| Old | New | Rationale |
|-----|-----|-----------|
| "Online Bulk Purchasing" | "Smart Business Buying" | SP study: bulk = barrier |
| "Online Wholesale Purchasing" | "For Businesses of All Sizes" | SP study: wholesale = exclusionary |
| "Purchase at Wholesale Price" | "No Minimum Order Required" | SP study: 50% think bulk required |

These aren't cosmetic tweaks. The SP study showed our ads were actively deterring 50% of our target audience. The copy changes remove the two biggest barriers to signup.

## Rollout Tracker

| Market | Phase 1 | Phase 2 | Phase 3 | Notes |
|--------|---------|---------|---------|-------|
| UK | ✅ Complete | Pending | — | Strong results |
| IT | ✅ Complete | Pending | — | Low volume, directional |
| DE | Not started | — | — | Translations ready |
| FR | Not started | — | — | Translations ready |
| ES | Not started | — | — | Translations ready |
| US | Not started | — | — | Originals ready |

## Template for New Markets

When launching ad copy test in a new market:
1. Confirm translated copy is approved
2. Create test campaign (duplicate existing, swap copy)
3. Set 50/50 rotation, optimize OFF
4. Run 30 days minimum
5. Report: CTR, regs, CPA, confidence level
6. Decision: scale, extend, or revert


## Sources
- SP Study findings (50% believed bulk required, messaging priorities) — source: ~/shared/context/body/eyes.md → Ad Copy Testing → Research Foundation
- UK test results (+86% CTR, +31% regs) — source: ~/shared/context/body/eyes.md → Ad Copy Testing → Results
- IT test results (+15% CTR, low volume) — source: ~/shared/context/body/eyes.md → Ad Copy Testing → Results
- Copy changes (old→new) — source: ~/shared/context/body/eyes.md → Ad Copy Testing → What Changed
- Phase structure — source: ~/shared/context/body/eyes.md → Ad Copy Testing → Phasing
- EU4 translations delivered 2/18 — source: ~/shared/context/body/eyes.md → Ad Copy Testing → Phasing

<!-- AGENT_CONTEXT
machine_summary: "Framework for testing revised ad copy across AB PS markets, driven by SP study finding that 50% of sole proprietors believed AB required bulk purchasing. UK Phase 1 showed +86% CTR and +31% regs (HIGH confidence). IT inconclusive (LOW confidence). DE/FR/ES translations ready for Phase 1 launch."
key_entities: ["ad copy", "SP study", "sole proprietors", "UK", "IT", "DE", "FR", "ES", "CTR", "registrations", "GlobalLink"]
action_verbs: ["test", "localize", "launch", "measure", "scale"]
update_triggers: ["new market test results available", "phase transition in any market", "new copy variants created"]
-->
