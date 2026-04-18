---
title: "LiveRamp Program — Identity, Enhanced Match, and Audience Expansion"
slug: "liveramp-program"
doc-type: "reference"
type: "reference"
audience: "team"
status: "DRAFT"
level: "L2"
category: "research"
created: "2026-04-17"
updated: "2026-04-17"
owner: "Richard Williams"
tags: ["liveramp", "enhanced-match", "rampid", "identity-resolution", "associated-accounts", "f90", "eu-dma", "hannah-neustadt"]
depends_on: []
summary: "The full LiveRamp program — mechanics, match rate progression from 12% to projected 40%, Enhanced Match investigation, EU DMA constraints, and F90 dependency chain."
---

# LiveRamp Program

LiveRamp identity resolution is the backbone of Amazon Business's audience-based paid media. This document is the canonical LiveRamp reference for the paid search team — covering mechanics, match rate progression, the Enhanced Match investigation Brandon initiated March 30, active risks, and how the program enables F90 and engagement campaigns. It replaces three earlier documents that split the same program across primers, explainers, and test designs.

## Chronology

| Date | Milestone | Impact |
|------|-----------|--------|
| Feb 2025 | LiveRamp integration launched for US Paid Search suppression | Removed existing customers from acquisition targeting |
| 2025 | Engagement account built on LiveRamp audiences | $765K iOPS delivered in 2025 |
| 2025 | Associated Accounts partnership with ABMA | Match rate moved from 12% → 20%-30% |
| Dec 2025 – Mar 2026 | Audience size declined 5.6M → 1.2M (78% drop) | Investigation required before Enhanced Match scoping |
| Mar 30, 2026 | Brandon initiated Enhanced Match investigation | Four questions for Abdul Bishar and Adobe |
| Apr 3, 2026 | Robert Skenes confirmed PS LiveRamp segment approved | Parallel implementation with Paid Media planned |
| Apr 15, 2026 | $255K LiveRamp fee confirmed in PS ENG $1.85M budget | Fee reserved pending Enhanced Match provisioning |
| TBD | Enhanced Match provisioned | Projected match rate doubling to ~40% |

## How LiveRamp works

### The core abstraction: RampID

LiveRamp's atomic unit is the RampID, a persistent identifier that resolves to a single real-world individual across their various identities — email addresses, phone numbers, device IDs, cookie hashes. LiveRamp's value is not any single matching technique; it is the cumulative graph of identity linkages built over time across their data partners.

When we send LiveRamp a hashed customer email, LiveRamp looks up whether that hash resolves to a known RampID in their graph. If yes, the RampID returns. Downstream platforms like Google Ads receive the RampID (or a platform-specific derivation) and match it against their own known identities.

The hash-then-resolve flow means we never expose raw customer identities to LiveRamp or Google. Both parties work with hashed or tokenized values.

### Match rate math

Match rate is the percentage of customer identities LiveRamp can resolve to a RampID that the downstream platform recognizes. It is a two-sided problem. LiveRamp might recognize an identity (step one), but Google might not have a matching RampID link in its own graph (step two). The reported match rate is the intersection.

For Amazon Business, today's twenty percent match rate means that for every one hundred customer emails we send, LiveRamp and Google jointly recognize twenty. The other eighty are either unknown to LiveRamp, known to LiveRamp but unlinked to Google, or filtered by regional data policies.

### Associated account logic

Many B2B users register with a work email but have a personal Amazon consumer account with a different email. Associated account logic identifies these linked identities and sends both. This moved match rate from twelve percent to twenty percent — not by finding more customers, but by giving LiveRamp more identity signals per customer.

## Match rate progression

The match rate stepped up twice since initial integration, with one more step projected.

**Baseline: 12 percent.** The first pass sent only registered AB customer emails. LiveRamp recognized about twelve percent in Google Ads. Two-thirds of our customer base was invisible in paid media audiences.

**Current: 20-30 percent.** The second pass added associated account emails. Roughly doubled recognized identities. The 30 percent cited in some earlier documents reflects a higher-water-mark measurement; the twenty percent reflects more recent and conservative monitoring.

**Projected with Enhanced Match: 40 percent.** Enhanced Match uses LiveRamp's expanded identity graph and additional matching signals — phone numbers, device IDs, additional email variants. The forty percent projection reflects LiveRamp vendor benchmarks for advertisers who complete Enhanced Match setup. It is a planning number, not a commitment.

## Enhanced Match investigation

Brandon initiated the Enhanced Match investigation on March 30, 2026 with four specific questions for Abdul Bishar and the Adobe team:

1. **Does Enhanced Match require additional data from us?** If so, what data types, and what privacy or legal review is required?
2. **Does it change the data sent to Google?** Does Adobe provide new data types, or is it just more LiveRamp IDs being matched?
3. **Do we need new agreements or contracts?** What are the legal implications?
4. **Are any other Amazon orgs using Enhanced Match?** Precedent would establish the legal and technical path.

These questions were unanswered as of April 4. Richard to reach out to Abdul and join the Adobe call. Brandon to work with Legal once technical answers are in.

### Provisioning

Richard owns the LiveRamp relationship with Hannah Neustadt (Customer Success Director). Provisioning requires legal review, technical integration, and data feed modifications on LiveRamp's side. Brandon's April 15 framing: "we will only use the fee once Enhanced Match gets set up — probably slow." No confirmed timeline.

The $255K LiveRamp fee is reserved in the 2026 PS ENG budget of $1.85M total. Yun confirmed no budget release until Enhanced Match is operational.

## Why match rate matters

Every audience-based campaign is capped by the match rate.

A **suppression campaign** that excludes current AB customers from acquisition targeting only suppresses the twelve to twenty percent LiveRamp can match. The remaining eighty percent appear to Google as unrecognized prospects, and we pay CPC to re-acquire them.

The **Engagement account** delivered $765K in iOPS in 2025 against a twenty percent match ceiling. Enhanced Match doubling that audience should proportionally expand the impact.

**F90 activation campaigns** face the same ceiling. The F90 audience of recently-acquired non-purchasers is small in absolute terms; a twenty percent match rate makes it constrained in Google. Enhanced Match is the primary unblocker for F90 at scale. See [F90 Program](f90-program).

## Active risks

### Audience size decline

Andrew Wirtz flagged on April 2 that the LiveRamp audience dropped from 5.6M to 1.2M between December 14 and March 26 — a 78 percent decline. If the audience shrank by that magnitude, both suppression and engagement capabilities are significantly degraded.

The audience drop investigation should happen **before** Enhanced Match scoping, because the baseline audience size determines whether Enhanced Match is a 2x opportunity or a marginal improvement. Two possibilities: a data pipeline issue (fix first) or a legal/consent change (scope on the smaller baseline).

### EU DMA constraints

European Union Digital Markets Act restrictions materially reduce match rate for EU markets. DMA limits the data signals that can pass between large platforms. For AB, this shows up in UK and DE OCI performance — UK OCI delivers a 23 percent registration lift versus US at 24 percent, partly because UK has less signal density post-DMA. DE sits at 18 percent for similar reasons plus higher CPC environment.

Brandon flagged on March 31 that DMA will keep EU match rates "much lower than US." Richard to get Abdul's regional availability chart showing where LiveRamp is possible per region. Clara appears to be the blocker on the EU side, with an April 7 due date referenced in the daily brief.

EU expansion markets should plan for longer stabilization windows due to DMA constraints. See [Paid Search Testing Approach](../testing/testing-approach-kate-v5) for the phased implementation approach that accounts for this.

## Cross-program connections

Enhanced Match connects to three active programs, and the connections determine strategic priority.

**F90 lifecycle.** Highest-leverage connection. Match rate is the binding constraint for F90. Enhanced Match pushing the rate from 20-30 percent to 40-50 percent would nearly double F90's addressable audience.

**OCI bidding.** Indirect connection. Enhanced Match does not directly affect OCI, but improved audience data quality could indirectly benefit OCI's conversion signal by helping Google better distinguish existing customers from new prospects.

**Email overlay.** Direct connection. The overlay redirects existing customers away from acquisition pages. Enhanced Match improves identification of existing customers, which means the overlay catches more of them and reduces CPA inflation further.

## What Enhanced Match does not do

Enhanced Match does not change attribution mechanics. It does not create new ad formats. It does not replace OCI or Adobe. It does not grant visibility into AI search placements. It is a specific upgrade to identity matching, not a general capability expansion. Treat it as a tool that unlocks existing capabilities at higher scale, not a new capability.

## Amazon Ads identity — distinction

Amazon Ads has its own identity resolution system that overlaps with LiveRamp's in some ways. For AB paid search on Google, LiveRamp is the primary identity layer. For AB on Amazon-owned surfaces (on-site, email, push), Amazon's internal identity system handles resolution natively. The paid search team does not need to worry about Amazon Ads identity for Google campaigns, but should understand that when Amazon Ads teams discuss "audiences," they typically mean something different from LiveRamp audiences.

## Compliance

LiveRamp operations must comply with regional data regulations. EU DMA is the most restrictive, followed by California CCPA. Legal review is required before any new audience type is activated. Hannah Neustadt coordinates the legal review process on LiveRamp's side.

Brandon announced on April 3 a new protocol for ABMA-related SIMs: submit at Sev 2.5 with Vijay Kumar (vkumarmp) as watcher for any registration-related issues, including LiveRamp integration problems.

## Decision guide

| Situation | Action |
|-----------|--------|
| Abdul confirms Enhanced Match needs new data types | Escalate to Legal immediately — do not wait for Brandon to initiate |
| Abdul confirms no new data needed (just better matching) | Fast-track: Legal review is lighter, implementation can parallel with Paid Media |
| Audience drop (5.6M→1.2M) is a data pipeline issue | Fix the pipeline first — Enhanced Match on a degraded audience is low-value |
| Audience drop is a legal/consent change | Scope Enhanced Match assuming the smaller audience is the new baseline |
| EU DMA blocks LiveRamp entirely | Focus Enhanced Match on US only, document EU as future opportunity |

## Next Steps

1. Reach out to Abdul Bishar with Brandon's four questions — urgent, Brandon is waiting.
2. Investigate the 5.6M → 1.2M audience drop to determine whether it is a LiveRamp legal change or a data pipeline issue.
3. Push Hannah Neustadt for Enhanced Match provisioning timeline by April 24.
4. Get Abdul's regional LiveRamp availability chart.
5. Document F90 audience size projections at 20 percent versus 40 percent match for OP1 planning.

## Sources

- Brandon's four Enhanced Match questions — Slack DM brandoxy→prichwil, 2026-03-30
- Robert Skenes LiveRamp coordination — Slack group DM rskenes/prichwil/arbishar/brandoxy, 2026-04-03
- Brandon EU LiveRamp blocked — Slack DM brandoxy→prichwil, 2026-03-31
- LiveRamp audience drop 5.6M→1.2M — Slack DM awirtz→prichwil, 2026-04-02
- ABMA SIM escalation protocol — Slack ab-paid-search-global, brandoxy, 2026-04-03
- Current match rate (13% → 30%) — `~/shared/context/body/brain.md` → D6: Engagement Channel Creation
- F90 connection — [F90 Program](f90-program)
- DMA impact on OCI — [OCI Program](oci-program) → DE variance
- $255K fee in PS ENG budget — Slack ABIX, 2026-04-15

## Related

- [F90 Program](../strategy/f90-program)
- [OP1 2027 Innovation Shortlist](../strategy/op1-2027-innovation-shortlist)
- [Paid Search Testing Approach](../testing/testing-approach-kate-v5)
- [Paid App Attribution Debate](../testing/paid-app-attribution-debate)

<!-- AGENT_CONTEXT
machine_summary: "Canonical LiveRamp program reference. Chronology Feb 2025 (integration) → 2025 (Engagement $765K iOPS) → Associated Accounts (12% → 20-30%) → Dec 2025-Mar 2026 audience drop (5.6M → 1.2M, 78%) → Mar 30 2026 Enhanced Match investigation. Brandon's 4 questions for Abdul. $255K fee reserved. EU DMA constrains. F90 binding constraint."
key_entities: ["LiveRamp", "Enhanced Match", "RampID", "Hannah Neustadt", "Abdul Bishar", "Robert Skenes", "Brandon Munday", "Associated Accounts", "ABMA", "EU DMA", "F90", "audience drop"]
action_verbs: ["resolve", "match", "suppress", "target", "scope"]
update_triggers: ["Abdul answers Brandon's 4 questions", "audience size investigation resolved", "Enhanced Match provisioned", "DMA regulation change", "LiveRamp contract renewal", "match rate measurement updated"]
decision_guide: "5 scenarios: new data needed (escalate Legal), no new data (fast-track), audience drop is pipeline (fix first), audience drop is legal (scope on smaller baseline), EU blocked (US-only focus)"
-->
