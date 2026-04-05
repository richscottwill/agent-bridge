---
title: "ie%CCP Planning & Optimization Framework"
status: FINAL
doc-type: strategy
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-03-30
updated: 2026-04-05
update-trigger: CCP revision by finance, ie%CCP target changes for any market, new market budget planning cycle, Brand volume structural shift
---

# ie%CCP Planning & Optimization Framework

This framework explains how to understand, plan around, and optimize ie%CCP — the ratio of acquisition cost to customer value — for Paid Search budget decisions. Use it to model scenarios, evaluate incremental spend, and frame recommendations for finance. Reach for this doc when you need to answer "should we spend more on NB?" or explain to finance why the team is underspending vs allocation.

## Context

ie%CCP exists because Paid Search acquisition economics are not intuitive. Brand and NB have fundamentally different cost structures, and the blended metric that finance tracks — ie%CCP — obscures the subsidy relationship between them. Every budget conversation, callout, and optimization recommendation depends on understanding this relationship. The MX FY26 cycle made this urgent: Brand grew 2.7x YoY, creating surplus that the OP2 plan never anticipated, and the team needs a shared framework for deciding how much incremental NB spend that surplus justifies.

## What ie%CCP measures

ie%CCP answers one question: how much are we paying to acquire a customer, relative to what that customer is worth? The formula is CPA divided by CCP. A result of 75% means we pay 75 cents for every dollar of customer value — efficient and sustainable. A result of 100% means breakeven, no margin for error. Lower ie%CCP means more efficient, which means better.

A 75% target is tighter (more demanding) than 100%. To move from 100% toward 75%, you either reduce CPA or increase CCP. Since CCP is set by finance, the lever is CPA.

## How Brand subsidizes NB

This is the single most important concept in ie%CCP planning. In a blended account, Brand and NB have very different efficiency profiles. Brand CPA runs $21 against $90 CCP — that is 23% ie%CCP, extremely efficient. NB CPA runs $134 against $30 CCP — that is 447% ie%CCP, deeply inefficient. Every Brand registration generates $69 of surplus ($90 CCP minus $21 CPA) that absorbs NB's $104 deficit ($134 CPA minus $30 CCP). The blended ie%CCP depends on the mix.

This is why Brand growth is the single most powerful lever for ie%CCP. More Brand registrations mean more surplus, which means more room for NB spend. Brand is the engine. NB is the passenger.

## How to read ie%CCP in a callout

When ie%CCP trends down (say 100% to 85%), the account is getting more efficient. Either Brand is growing, NB CPA is improving, or NB spend was cut. Check which one — the story matters for the recommendation.

When ie%CCP trends up (say 85% to 105%), the account is getting less efficient. Either Brand dipped, NB CPA worsened from rising CPCs, or NB spend increased into diminishing returns. Decompose the change before recommending action.

When ie%CCP sits well below target (say 50% against a 75% target), the account is underspending. There is room to invest more in NB without breaching the target. This is either a budget constraint or a missed opportunity.

## What changes the plan

The OP2 plan is built on assumptions about Brand volume, NB CPA, and CCP values. When reality diverges, the plan needs to flex.

| What changed | Direction | Effect on ie%CCP | Action |
|-------------|-----------|-----------------|--------|
| Brand regs higher than planned | Up | Improves (more surplus) | Can increase NB spend |
| Brand regs lower than planned | Down | Worsens (less surplus) | Must cut NB spend |
| NB CPA improved (lower) | Down | Improves (less deficit per NB reg) | Can add NB regs |
| NB CPA worsened (higher) | Up | Worsens (more deficit per NB reg) | Must cut NB regs or spend |
| CCP revised downward | Up | Worsens (less customer value) | Must cut spend |
| CCP revised upward | Down | Improves (more customer value) | Can increase spend |

The pattern: Brand volume and CCP revisions are the biggest ie%CCP shocks because they change the structural capacity of the account. NB CPA changes are incremental — they improve or worsen the margin on each registration but do not reshape the overall constraint. The most common real-world scenario is Brand outperforming plan, creating surplus that was not budgeted. The question becomes whether finance will fund the incremental NB spend to capture the available registrations.

## How MX FY26 illustrates the framework

This is where the framework meets reality. Finance allocated $1.8M for MX FY26. The team built an OP2 spend plan of $542K that respects the ie%CCP target. The $1.26M gap exists because NB is inefficient at 447% ie%CCP — every dollar of NB spend drags the blended ratio up, and the team can only run as much NB as Brand surplus absorbs.

Then Brand grew 2.7x YoY in Q1 (HIGH confidence — structural, not temporary). Conservative estimates for FY26 project roughly 9,375 Brand registrations generating $844K in CCP and costing $197K in spend. That surplus changes the math entirely.

At a 100% ie%CCP target, the account can support roughly 5,676 NB registrations at $134 CPA — total spend of $959K, blended CPA of $64, ie%CCP landing around 96%. At a tighter 75% target (April onward), the account supports roughly 4,573 NB registrations but requires NB CPA to improve to $115 — total spend of $745K, blended CPA of $53, ie%CCP around 79%.

Both scenarios exceed OP2 significantly. The 100% scenario delivers 15,051 total registrations (+35% vs OP2) at $959K spend (+77%). The 75% scenario delivers 13,948 total registrations (+25% vs OP2) at $745K spend (+37%). The incremental registrations are available. The question is whether finance funds the NB spend to capture them.

The marginal economics tell the rest of the story. The first batch of incremental registrations beyond OP2 (to 75% ie%CCP) costs $143 each. The next batch (75% to 100%) costs $194 each. Diminishing returns in action — each incremental NB registration costs more than the last, and the question is never "what is the average NB CPA?" but "what is the marginal CPA of the next batch, and does that still work within ie%CCP?"

<!-- TODO: The -10% haircut on Brand estimates is stated without justification. Richard should specify why 10% vs 15% or 20%. -->

## How to apply this to callouts and recommendations

When writing a weekly callout or making an optimization recommendation, ie%CCP should frame the decision.

"Should we increase NB spend?" — check whether Brand surplus supports it, what the marginal CPA would be, and whether ie%CCP stays within target.

"Why did ie%CCP change this week?" — decompose into Brand volume, NB CPA, and mix shift. One-time events (Hot Sale, Prime Day) versus structural trends require different responses.

"How should we respond to a CCP revision?" — model the new CCP against current spend levels. When MX CCP dropped from $150/$50 to $80/$30 in early 2026, it forced the $1.97M to $1.07M budget cut in FY25. That was the single biggest ie%CCP shock in the portfolio.

"Finance is asking why we are underspending vs allocation." — the allocation is the ceiling. The ie%CCP target limits executable spend. The gap is NB spend that would breach the efficiency threshold. To close the gap, we need Brand growth, NB CPA improvement, or a looser ie%CCP target. Quantify each path.

## Quick reference

ie%CCP equals CPA divided by CCP. Lower is more efficient.

A 75% target means CPA must be at or below 75% of CCP. A 100% target means breakeven. Brand is the engine — grow it to create surplus. NB is the passenger — optimize it, then scale it. CCP is the speed limit — set by finance, not by us.

To improve ie%CCP: cut NB (fast) or grow Brand (structural). To model capacity: use the NB-per-Brand-reg ratio (see Appendix A). To evaluate incremental spend: ask about marginal CPA, not average CPA.

## Related

- [MX FY26 Budget Model](mx-fy26-budget-model)
- [WBR Callout Playbook](wbr-callout-playbook)
- [OCI Rollout Playbook](oci-rollout-playbook)

---

## Appendix A: Blended math and formula derivations

ie%CCP is a blended metric. It equals Total Spend divided by Total CCP, which is the same as blended CPA divided by blended CCP.

```
Total Spend = (Brand Regs × Brand CPA) + (NB Regs × NB CPA)
Total CCP   = (Brand Regs × Brand CCP) + (NB Regs × NB CCP)
ie%CCP      = Total Spend / Total CCP
```

At a given ie%CCP target T, you can solve for the maximum NB registrations the account can support:

```
T = (Brand × BrandCPA + NB × NB_CPA) / (Brand × BrandCCP + NB × NB_CCP)

Rearranging:
NB = Brand × (T × BrandCCP - BrandCPA) / (NB_CPA - T × NB_CCP)
```

Using current MX values (Brand CPA $21, Brand CCP $90, NB CCP $30):

| ie%CCP Target | NB CPA | NB per Brand Reg | Interpretation |
|---------------|--------|-----------------|----------------|
| 75% | $115 | 0.503 | For every 2 Brand regs, roughly 1 NB reg allowed |
| 75% | $134 | 0.417 | Worse NB CPA means fewer NB regs allowed |
| 100% | $134 | 0.663 | Looser target means more NB room |
| 100% | $115 | 0.911 | Better NB CPA plus looser target means nearly 1:1 |
| 125% | $134 | 0.960 | Overspending territory — almost 1:1 |

The ratio tells you how many NB registrations the account can afford per Brand registration at a given efficiency target.

## Appendix B: The four optimization scenarios

### When budget is constrained and the ie%CCP target is tighter

This is the hardest scenario — less money and a lower blended CPA requirement. Cut NB spend aggressively, removing the most expensive campaigns and keywords first. NB CPA improves as you cut because you are removing the expensive tail. Protect Brand at all costs. Focus NB on highest-CVR campaigns only (Invoice, Product/Vertical over Generic).

MX H2 2025 is the real example. Budget was cut from $1.97M to $1.07M, ie%CCP target set at 100%. NB spend dropped roughly 60% from H1 to H2. NB registrations dropped roughly 40%. But NB CPA improved from $264 to $201 (minus 24%) because the remaining spend concentrated in efficient campaigns.

### When budget is constrained but the ie%CCP target is looser

Easier than the first scenario. Less total spend, but more of it can go to NB because the ie%CCP ceiling is higher. Allocate more of the fixed budget to NB. Accept higher NB CPA on marginal registrations. The risk: if you push NB too hard within the budget, CPA rises and you may still breach the looser target.

### When budget is unconstrained and the ie%CCP target is tighter

The growth scenario. Budget is not the constraint — efficiency is. Grow Brand first (highest leverage). Improve NB efficiency before scaling — negative keyword optimization, bid strategy tuning, CVR improvements. Scale NB only after efficiency gains are locked in. The sequence matters: improve efficiency, lock in gains, then scale.

MX Q1 2026 illustrates this. Brand grew 2.7x YoY organically, creating massive CCP surplus. NB spend increased to fill the surplus, but NB CPA stayed at $134 because bid strategies were chasing volume. ie%CCP landed at roughly 98% — right at the 100% target. If NB CPA had been improved first (via negative keywords, which happened in W11), the same Brand surplus could have funded even more NB registrations.

### When budget is unconstrained and the ie%CCP target is looser

The maximum-volume scenario. Rare in practice, useful as a ceiling estimate. Scale NB aggressively, accept diminishing returns, expand into lower-CVR campaigns. Use this scenario for "what is the maximum registrations we could drive?" analysis. The risk: CPA spirals as each incremental NB registration costs more.

## Appendix C: The marginal CPA curve

Not all NB registrations cost the same. The first NB registrations are cheap (high-intent keywords, Invoice campaigns). As you scale, you push into lower-CVR, higher-CPC territory.

The core 50% of NB spend runs roughly $100-110 CPA with a marginal cost around $100 per registration. The mid tier (next 30%) runs $120-130 CPA with marginal cost around $150. The tail (last 20%) runs $140-160 CPA with marginal cost above $190.

This is why cutting NB spend improves CPA disproportionately — you remove the expensive tail first. And why scaling NB spend worsens CPA disproportionately — you add expensive marginal registrations. When evaluating whether to increase NB spend, the question is always marginal CPA, not average CPA.

## Appendix D: Levers ranked by impact

Brand registration volume is the highest-leverage input. Every Brand registration at $21 CPA against $90 CCP generates $69 of surplus. That surplus funds NB spend. An additional 100 Brand registrations per month creates $6,900 of surplus — room for roughly 50-65 more NB registrations at current CPA. Brand growth is mostly organic, driven by brand awareness, market maturity, events, and paid social spillover. The PS team's job is to capture the demand through Brand coverage, Brand Phrase campaigns, and sitelink optimization during events. The biggest Brand moves come from outside PS: paid social campaigns, events (Hot Sale, Prime Day), and market maturity.

NB CPA is the second-highest lever. Lowering NB CPA from $134 to $115 reduces the deficit per registration from $104 to $85 — an 18% improvement that compounds across every NB registration. The levers within NB CPA include bid strategy optimization, negative keyword management, campaign structure consolidation, device optimization, and landing page improvements. A $20 NB CPA improvement across 500 NB registrations per month saves $10K per month — room for roughly 75 more NB registrations.

NB spend level is the most direct lever but has diminishing returns. More spend means higher CPA on marginal registrations. Pull this lever after Brand and NB CPA are optimized.

CCP values are not in our control. CCP is set by finance based on projected 3-year OPS. MX CCP went from $150/$50 (mid-2025) to $80/$30 (early 2026) to $90/$30 (current). Each downward revision tightened the constraint. We cannot control CCP, but we need to monitor it and model scenarios for potential revisions.

<!-- AGENT_CONTEXT
machine_summary: "Decision framework for ie%CCP (CPA/CCP ratio) in Paid Search budget planning. Main body covers the subsidy model (Brand at 23% ie%CCP subsidizes NB at 447%), how to read and decompose ie%CCP changes in callouts, and the MX FY26 case study showing 25-35% upside vs OP2 depending on ie%CCP target. Appendices carry formula derivations, four optimization scenarios, marginal CPA curve, and lever rankings."
key_entities: ["ie%CCP", "CPA", "CCP", "Brand", "NB", "MX", "OP2", "marginal CPA", "budget planning", "finance"]
action_verbs: ["model", "decompose", "evaluate", "calculate", "forecast", "optimize"]
update_triggers: ["CCP revision by finance", "ie%CCP target changes for any market", "new market budget planning cycle", "Brand volume structural shift"]
-->
