---
title: WBR Callout Template & Guide
status: DRAFT
doc-type: execution
audience: amazon-internal
level: 1
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: new market added, callout format changes, dashboard ingester updates
---

# WBR Callout Template & Guide

---

## Purpose

Standardize WBR callout writing so anyone on the team can cover any market. Eliminates the "only Richard/Dwayne can write callouts" bottleneck.

## Callout Structure

Each market callout follows this format:

### [Market] — Week [X] (dates)

**Headline:** One sentence summary. Lead with the most important metric change.

**Registrations:** [X] regs, [+/-X%] vs OP2, [+/-X%] YoY. Context for the change.

**Spend & CPA:** $[X] spend, $[X] CPA. Trend vs prior week and vs target.

**Key Drivers:** What caused the change? (bid strategy, seasonal, competitive, new campaign, etc.)

**Competitive:** Notable IS changes, new competitors, CPC pressure.

**Actions:** What are we doing about it? (tests launched, bids adjusted, escalations)

## Data Sources

- WW Dashboard Excel (weekly drop from Brandon/team)
- Google Ads auction insights (competitive data)
- Dashboard ingester output: `~/shared/context/active/callouts/<market>/`

## Quip Location

[Pre-WBR Callouts](https://quip-amazon.com/MMgBAzDrlVou)

## Market-Specific Notes

| Market | Key Stakeholder | CPA Target | Special Considerations |
|--------|----------------|------------|----------------------|
| US | Brandon | $83 | Walmart Brand competition, OCI impact |
| AU | Lena/Alexis | $140 | CPC sensitivity, Polaris migration |
| MX | Lorena | N/A | Growth market, reftag tracking |
| UK | — | N/A | Ad copy test results, weareuncapped |
| DE | — | N/A | High Y25 baseline |
| CA | — | $73 | LP optimization gains |
| JP | — | N/A | MHLW headwind |

US and AU are the two markets where callouts get the most scrutiny. US because of Walmart competition and OCI impact. AU because Lena reads every number.

## Coverage Protocol

When Dwayne is OOO:
1. Richard covers PS-specific callouts
2. Use this template + dashboard ingester output
3. Post to Quip by [day/time] before Pre-WBR meeting

Dashboard ingester auto-generates draft callouts. Start there, then add narrative context and competitive color.


## Sources
- Pre-WBR Callouts Quip — source: ~/shared/context/body/spine.md → Key Quip Documents
- Market CPA targets and stakeholders — source: ~/shared/context/body/eyes.md → Market Health table
- Dashboard ingester output location — source: ~/shared/context/body/device.md → Dashboard Ingester
- Dwayne as WBR coverage partner — source: ~/shared/context/active/current.md → Key People

<!-- AGENT_CONTEXT
machine_summary: "Standardized WBR callout template and guide for AB Paid Search. Covers callout structure (headline, regs, spend/CPA, drivers, competitive, actions), data sources, market-specific notes with CPA targets, and coverage protocol when Dwayne is OOO."
key_entities: ["WBR", "Dwayne Palmer", "dashboard ingester", "Pre-WBR Callouts Quip", "US", "AU", "MX", "UK", "DE", "CA", "JP"]
action_verbs: ["write", "cover", "post", "monitor", "escalate"]
update_triggers: ["new market added", "callout format changes", "dashboard ingester updates", "CPA target changes"]
-->
