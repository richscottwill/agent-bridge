---
title: AU NB Testing Proposal — MRO/Trades Vertical
status: DRAFT
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: AU sync feedback, keyword volume data pulled, Alexis LP confirmation
---

# AU NB Testing Proposal — MRO/Trades Vertical

---

## Hypothesis

Targeting MRO (Maintenance, Repair, Operations) and Trades keywords in AU will improve NB registration quality and CPA because these verticals have high purchase intent and natural alignment with AB's product catalog.

## Context

- AU NB regs softening: W11 -9% WoW, CPA +9%
- Bid strategies driving CPC down (-19% from W7) but traffic may be lower intent
- Lena wants weekly CPA review and keyword-to-product mapping
- MRO/Trades is a vertical where business buyers have clear, recurring purchase needs

## Proposed Keywords

| Category | Example Keywords | Expected Intent |
|----------|-----------------|-----------------|
| MRO | maintenance supplies, industrial cleaning, facility maintenance | High |
| Trades | plumbing supplies wholesale, electrical supplies business, HVAC parts | High |
| Safety | PPE business, safety equipment wholesale, work gloves bulk | High |
| Tools | power tools business, hand tools wholesale | Medium-High |

These are high-intent verticals where business buyers have recurring, predictable needs. MRO in particular is a natural fit — maintenance supplies are consumable, repeat-purchase products.

## Test Design

- Campaign: New NB campaign, AU, MRO/Trades theme
- Budget: Reallocate from underperforming generic NB keywords (not incremental spend)
- Duration: 4 weeks
- Landing page: Coordinate with Alexis — does MCS have an MRO/Trades page? If not, use general Polaris page.
- Metrics: Regs, CPA, search term quality, CVR vs general NB

## Success Criteria

| Outcome | Action |
|---------|--------|
| CPA < AU average ($140) AND regs incremental | Scale, add more MRO/Trades keywords |
| CPA comparable, regs incremental | Continue, optimize |
| CPA > $140, regs not incremental | Pause, reallocate budget back |

This is a budget-neutral test — we're reallocating from underperforming generic NB, not requesting incremental spend. The downside is limited.

## Next Steps
- [ ] Build keyword list with search volume data
- [ ] Discuss with Alexis at AU sync — LP options
- [ ] Get Lena's input on priority verticals for AU


## Sources
- AU NB regs -9% WoW, CPA +9% (W11) — source: ~/shared/context/body/eyes.md → Market Health → AU
- CPC -19% from W7 — source: ~/shared/context/body/eyes.md → Market Health → AU
- Lena wants weekly CPA review — source: ~/shared/context/active/current.md → AU Paid Search Optimization
- MRO/Trades as Engine Room task — source: ~/shared/context/body/hands.md → Engine Room tasks
- AU CPA target $140 — source: ~/shared/context/body/eyes.md → Market Health table

<!-- AGENT_CONTEXT
machine_summary: "Test proposal for AU NB expansion into MRO/Trades verticals. Budget-neutral (reallocated from underperforming generic NB). 4-week test, success = CPA < $140 with incremental regs. Requires Alexis LP confirmation and Lena input on priority verticals."
key_entities: ["AU", "MRO", "Trades", "NB keywords", "Lena", "Alexis", "CPA $140 target"]
action_verbs: ["test", "reallocate", "measure", "coordinate", "scale"]
update_triggers: ["AU sync feedback", "keyword volume data pulled", "Alexis LP confirmation", "test launch or results"]
-->
