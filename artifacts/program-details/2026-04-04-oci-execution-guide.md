---
title: OCI Execution Guide
status: DRAFT
doc-type: execution
audience: amazon-internal
level: N/A
owner: Richard Williams
created: 2026-04-04
updated: 2026-04-04
update-trigger: new OCI market launches, phase transitions, troubleshooting discoveries, team questions
replaces: oci-implementation-guide, oci-methodology-knowledge-share
tags: [oci, execution, how-to, google-ads, nb, ww]
---

# OCI Execution Guide

> For the business case, validated results, and strategic rationale, see [OCI Rollout Playbook](~/shared/artifacts/testing/2026-03-25-oci-rollout-playbook.md).
> This doc is the how-to. Follow it step by step to implement OCI in any market.

---

## What OCI Is (30-Second Version)

OCI (Offline Conversion Import) sends actual Amazon Business registration data back to Google Ads so the bidding algorithm optimizes for real conversions instead of proxy signals. Before OCI, Google guessed which searches would produce registrations. With OCI, it knows.

Manual bidding does not scale across 10 markets. OCI has delivered:
- US: +24% regs, ~50% NB CPA improvement, $16.7MM OPS
- UK: +23% regs
- DE: +18% regs

The methodology is validated. The remaining markets are execution, not experimentation.

---

## What NOT to Do

Read this before touching anything in Google Ads:

1. **Do not judge OCI by week 1.** The algorithm needs 2-4 weeks to learn. CPA will spike. This is normal.
2. **Do not use OCI on Brand campaigns.** Manual bid caps are needed for competitive defense (Walmart). Brand stays manual.
3. **Do not compare raw pre/post.** Use seasonality-adjusted baselines. Raw comparisons confuse seasonal effects with OCI effects.
4. **Do not panic if CPA spikes in week 1.** It normalizes by week 3-4. If it does not normalize, see Troubleshooting below.
5. **Do not compare OCI markets to non-OCI markets directly.** AU/MX do not have OCI, so their CPA trajectory is fundamentally different.
6. **Do not set an aggressive Target CPA.** Start with the current 4-week average. You can tighten later once the algorithm has learned.

---

## Prerequisites (Before You Start)

Before launching OCI in any market, confirm all of these:

- [ ] Conversion tracking verified (Google Ads -> Tools -> Conversions)
- [ ] Minimum 30 conversions/month in the target campaign
- [ ] Baseline performance captured (4 weeks minimum)
- [ ] Brand campaigns excluded from OCI (manual bid caps stay)
- [ ] Stakeholder briefed on expected behavior (CPA may spike week 1)
- [ ] MCC structure confirmed (see MCC table below)

### MCC Structure

| MCC | ID | Markets |
|-----|-----|---------|
| Master MCC | DSAP - Amazon Business Parent MCC (873-788-1095) | All |
| NA MCC | 683-476-0964 | US, CA, MX |
| EU MCC | 549-849-5609 | UK, DE, FR, IT, ES |
| JP MCC | 852-899-4580 | JP |
| AU | Not created | N/A |

---

## Step-by-Step: E2E Launch

### Step 1: Select campaigns
- NB campaigns only (never Brand)
- Start with the highest-volume NB campaign for fastest signal
- If the market has multiple NB campaigns, pick the one with the most conversions/month

### Step 2: Change bidding strategy
- Google Ads -> Campaign -> Settings -> Bidding
- Switch from Manual CPC to "Maximize Conversions" or "Target CPA"
- If Target CPA: set to current 4-week average CPA (do not set an aggressive target)
- If Maximize Conversions: set a daily budget cap at 120% of current daily spend

### Step 3: Monitor
- **Week 1:** Daily monitoring. Check CPA, conversion volume, search terms, budget status.
- **Week 2:** Daily monitoring continues. CPA should begin stabilizing.
- **Week 3-4:** Weekly monitoring. CPA should be at or below baseline.
- **Ongoing:** Weekly CPA review, biweekly search term review.

What to check each day/week:
| Check | Where | What to Look For |
|-------|-------|-----------------|
| CPA | Google Ads -> Campaigns -> filter NB | Compare this week vs 4-week trailing average |
| Conversion volume | Google Ads -> Campaigns -> Conversions column | Should maintain or increase vs baseline |
| Search terms | Google Ads -> Keywords -> Search Terms | Quality degradation (irrelevant queries) |
| Budget | Google Ads -> Campaigns -> Budget column | "Limited by budget" warning = OCI needs more room |
| Conversion tracking | Google Ads -> Tools -> Conversions | Any errors or status warnings |

### Step 4: Evaluate at 4 weeks
- Compare: OCI period CPA vs pre-OCI baseline (seasonality-adjusted)
- If CPA within 115% of baseline: proceed to 25% scale (Phase 2)
- If CPA between 115-120%: extend test 2 more weeks
- If CPA >120% for 7+ consecutive days: pause and investigate (see Troubleshooting)

---

## Scaling: Phase 2 through Phase 4

| Phase | Traffic | Duration | Gate to Next Phase |
|-------|---------|----------|-------------------|
| Phase 2 | 25% of NB spend | 2-4 weeks | CPA within 115% of baseline |
| Phase 3 | 50% of NB spend | 2-4 weeks | CPA within 110% of baseline |
| Phase 4 | 100% NB | Ongoing | Weekly CPA review, monthly deep dive |

At each phase:
1. Expand OCI to the next traffic percentage
2. Monitor for the specified duration
3. Check CPA against the gate threshold
4. If gate passes: proceed to next phase
5. If gate fails: hold at current phase, investigate, adjust

After Phase 4 (100% NB):
- Brand campaigns remain on manual CPC with bid caps
- Establish new baselines for ongoing monitoring
- Begin Brand campaign evaluation (OCI on Brand is lower-impact but worth testing in mature markets)

---

## Troubleshooting

| Issue | Likely Cause | Fix |
|-------|-------------|-----|
| CPA spiking week 1 | Algorithm learning | Wait. Evaluate at week 3-4. Do not intervene. |
| CPA still high at week 4 | Target too aggressive or low volume | Raise target CPA by 10-15%. Check conversion volume (need 30+/month). |
| Conversion tracking errors | Tag implementation | Verify Google Tag. Check for duplicate tags. Confirm conversion action is active. |
| Search term quality drop | Broad match expansion | Add negative keywords. Review search term report weekly. |
| Budget limited | OCI bidding higher than manual | Increase daily budget or narrow targeting. OCI needs room to bid. |
| Duplicate hvocijid in URLs | Parameter appended twice on landing pages | Known issue (EU3 + existing markets). JP not affected. Under investigation. Do not block rollout. |
| Conversion lag | Delayed conversion attribution | Wait 72 hours before evaluating daily CPA. Use 7-day rolling average instead of daily. |
| CPA volatile after week 4 | Seasonal factors or competitive shifts | Check: is the volatility OCI-specific or market-wide? Compare Brand CPA trend. If Brand is also volatile, it is market-level, not OCI. |

---

## Per-Market Notes

| Market | Status | Special Considerations |
|--------|--------|----------------------|
| US | 100% live | Reference implementation. Peak Jan: 39K regs (+86% YoY). |
| UK | 100% live | weareuncapped competitor (24% Brand IS) -- monitor Brand IS weekly. |
| DE | 100% live | High Y25 baseline -- adjust YoY expectations. Cleanest test-vs-control data (W44-W45). |
| FR | 100% live | bruneau.fr at 39-47% NB IS -- OCI helps efficiency but does not solve impression share pressure. |
| IT | 100% live | Brand Core CPC +131% YoY -- IT challenge is Brand-side, not NB. Low volume -- patience needed. |
| ES | 100% live | AGL (internal Amazon entity) bidding on ES Brand -- coordination issue, not competitive. |
| JP | 100% live | MHLW campaign ended 1/31 -- major reg driver lost. Yahoo competition intensifying. |
| CA | On track (4/7) | E2E launched 3/4. LP optimization already showing strong results (Bulk CVR +187%). |
| AU | Not started | Target May 2026 via Adobe OCI path (Suzane Huynh). MCC not created. |
| MX | Not started | No MCC. No timeline. |

---

## How to Check OCI Performance (Quick Reference)

For any market on OCI, this is the weekly check:

1. Google Ads -> Campaigns -> filter NB campaigns
2. Compare: this week CPA vs 4-week trailing average
3. Check: conversion tracking status (any errors or warnings?)
4. Check: search term report for quality (any irrelevant queries?)
5. Flag: CPA >120% of trailing average for 7+ days -> investigate using Troubleshooting table
6. Report: include OCI status in weekly market review

---

## Current Market Status (as of April 2026)

| Market | Status | Key Date |
|--------|--------|----------|
| US | 100% live | Since Sep 2025 |
| UK | 100% live | Since Sep 2025 |
| DE | 100% live | Since Dec 2025 |
| FR | 100% live | Dialed up 3/30 |
| IT | 100% live | Dialed up 3/30 |
| ES | 100% live | Dialed up 3/30 |
| JP | 100% live | Dialed up 3/31 |
| CA | On track | Target 4/7 |
| AU | Not started | Target May 2026 |
| MX | Not started | TBD |

---

## Related Docs

- [OCI Rollout Playbook](~/shared/artifacts/testing/2026-03-25-oci-rollout-playbook.md) -- Strategy doc: business case, validated results, competitive context, measurement framework
- [OCI Business Case](~/shared/artifacts/strategy/2026-04-04-oci-business-case.md) -- Leadership summary: $16.7MM headline, talking points for Kate/Todd
- [OCI Instructions (Quip)](https://quip-amazon.com/Zee9AAlSBEB) -- Technical setup guide (original Quip doc)

---

## Sources
- Phased rollout steps (E2E->25%->50%->100%) -- source: ~/shared/context/body/brain.md -> D1: OCI Implementation Approach
- Gate criteria (115%, 110%) -- source: derived from D1 methodology + operational experience
- Market status -- source: ~/shared/context/body/eyes.md -> OCI Performance
- Troubleshooting table -- source: operational experience documented in eyes.md -> OCI Performance
- hvocijid issue -- source: ~/shared/context/body/eyes.md -> OCI Performance -> Known Issues
- MCC structure -- source: ~/shared/context/body/eyes.md -> OCI Performance -> MCC Structure
- "What NOT to do" lessons -- source: operational experience across US/UK/DE rollouts
- Annual Review feedback ("proactively share knowledge") -- source: ~/shared/context/body/memory.md -> Brandon relationship entry

<!-- AGENT_CONTEXT
machine_summary: "Consolidated OCI execution guide for AB Paid Search. Merges the former OCI Implementation Guide and OCI Methodology Knowledge Share into one doc. Covers: what OCI is (30-sec version), what NOT to do (6 rules), prerequisites checklist, step-by-step E2E launch, scaling phases with gate criteria, troubleshooting table (8 issues), per-market notes (10 markets), and quick reference for weekly OCI checks. 7/10 markets at 100%, CA targeting 4/7, AU May 2026, MX TBD."
key_entities: ["OCI", "Google Ads", "NB campaigns", "E2E launch", "Target CPA", "Maximize Conversions", "hvocijid", "MCC"]
action_verbs: ["implement", "monitor", "troubleshoot", "scale", "evaluate", "check"]
update_triggers: ["new OCI market launches", "new troubleshooting issue discovered", "phase transition in any market", "team questions about OCI"]
-->
