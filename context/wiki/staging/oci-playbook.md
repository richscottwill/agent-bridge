---
title: "OCI Rollout Playbook: From E2E to 100% in Any Market"
slug: "oci-playbook"
type: "playbook"
audience: "team"
status: "draft"
created: "2026-03-25"
updated: "2026-03-25"
owner: "Richard Williams"
tags: ["oci", "bid-strategy", "testing", "non-brand", "paid-search", "ww"]
depends_on: []
consumed_by: ["wiki-concierge", "najp-analyst", "eu5-analyst", "abix-analyst"]
summary: "Step-by-step playbook for rolling out OCI in any AB Paid Search market — phased approach, measurement framework, known issues, and market-specific considerations."
# Artifact metadata
artifact-status: DRAFT
artifact-audience: amazon-internal
artifact-level: 2
update-trigger: "Quarterly as new markets go live, or when OCI measurement methodology changes"
---

# OCI Rollout Playbook: From E2E to 100% in Any Market

This playbook codifies the OCI rollout methodology that produced +35K registrations and $16.7MM+ OPS across US, UK, and DE. A teammate should be able to replicate the rollout in a new market by following this doc. No Richard required.

## Context

OCI (Offline Conversion Import) enables Google Ads to optimize bidding based on actual registration value data sent back from Amazon's systems, replacing Adobe's algorithmic bidding. AB Paid Search was the first non-retail BU to implement OCI at Amazon. The methodology was developed through US (Jul 2025), refined in UK (Aug 2025) and DE (Nov 2025), and is now being applied to CA, JP, and EU3 (Feb-Mar 2026).

The core insight: phased rollout with measurement at each stage. Never go from 0% to 100%. Always validate lift before committing more budget. This is Decision D1 — evidence over intuition, phased rollout over full migration.

## What OCI Does (and Doesn't Do)

**Does:** Sends actual registration data back to Google Ads so the bidding algorithm optimizes for real conversions, not proxy signals (clicks, page views). This improves Non-Brand CPA — in the US, by ~50% — because the algorithm learns which queries actually produce registrations.

**Doesn't:** Fix Brand CPA. Brand traffic converts regardless of bidding algorithm. OCI's impact is concentrated on Non-Brand, where the algorithm's query selection matters most.

**Why it matters at program level:** When NB CPA drops 50% via OCI, the team can absorb Brand CPA increases (from competitors like Walmart) without total program CPA degrading. This is the structural foundation of the efficiency-over-escalation competitive strategy.

## The Phased Rollout

### Phase 1: E2E Testing (2-4 weeks)

**Goal:** Confirm the data pipeline works — registrations flow from Amazon's systems to Google Ads correctly.

**Steps:**
1. Set up OCI conversion action in Google Ads (see [OCI Instructions Quip](https://quip-amazon.com/Zee9AAlSBEB) for technical setup)
2. Configure the data feed: Amazon registration events → Google Ads offline conversion import
3. Run E2E test: trigger test registrations, verify they appear in Google Ads within 24-48 hours
4. Validate: conversion counts in Google Ads match Amazon's internal registration data (±5% tolerance for attribution lag)
5. Check for known issues (see Known Issues section below)

**Exit criteria:** Data pipeline confirmed working. Conversion counts match within tolerance. No duplicate parameter errors.

**Duration by market:**
- US: 2 weeks (first market, more debugging)
- UK/DE: 1-2 weeks (process established)
- CA/JP/EU3: 1-2 weeks (current wave, launched Feb-Mar 2026)

### Phase 2: 25% NB Traffic (4-6 weeks)

**Goal:** Validate OCI lift on a subset of Non-Brand traffic before committing more budget.

**Steps:**
1. Split NB campaigns: 25% of NB traffic uses OCI bidding, 75% remains on existing bidding (Adobe or Google click-based)
2. Run for minimum 4 weeks to accumulate sufficient conversion data
3. Measure: compare OCI segment vs control on registrations, CPA, ROAS
4. Build the measurement framework (see Measurement section below)

**Exit criteria:** OCI segment shows statistically meaningful lift in registrations and/or CPA improvement vs control. Minimum 4 weeks of data.

### Phase 3: 50% NB Traffic (4-6 weeks)

**Goal:** Confirm lift holds at scale before full migration.

**Steps:**
1. Expand OCI to 50% of NB traffic
2. Monitor for 4 weeks
3. Watch for diminishing returns — does the lift per incremental % of traffic hold, or does it compress?
4. Check for cannibalization: is OCI stealing conversions from the control segment, or generating incremental ones?

**Exit criteria:** Lift holds at 50%. No evidence of cannibalization. CPA improvement is consistent with 25% phase.

### Phase 4: 100% NB (ongoing)

**Goal:** Full migration. OCI becomes the default NB bidding strategy.

**Steps:**
1. Migrate remaining NB traffic to OCI
2. Decommission control campaigns
3. Establish new baselines for ongoing performance monitoring
4. Begin Brand campaign evaluation (OCI on Brand is lower-impact but worth testing)

**Post-migration monitoring:** Weekly CPA and registration tracking for first 8 weeks. Flag any regression >10% WoW for investigation.

## Measurement Framework

The measurement framework is what makes this a validated rollout, not a hope-and-pray migration.

### Test vs Control (During Phases 2-3)

| Metric | OCI (Test) | Control | Difference |
|--------|-----------|---------|------------|
| Cost | $ | $ | % |
| Registrations | # | # | % |
| ROAS | % | % | pp |
| CPA | $ | $ | % |

**Always report both absolute numbers AND percentages.** A 50% CPA improvement sounds great until you see it's based on 10 registrations.

### Seasonality-Adjusted Baseline (Post Phase 4)

Once at 100%, there's no control group. Use seasonality-adjusted baselines:
1. Take the same week from the prior year (if available)
2. Adjust for known factors: budget changes, competitor activity, market events
3. Compare actualized CPA vs adjusted baseline
4. Report as "OCI lift tracking: W[X] +[Y]% ([Z]% to expectation)"

**DE example (W49-W51 2025):** W49 +20% (95% to expectation), W50 +20% (96%), W51 +16% (74%). This format tells leadership both the lift AND whether it's meeting projections.

### Validated Results by Market

| Market | Test Period | Reg Lift | NB CPA Improvement | Estimated OPS |
|--------|-----------|----------|-------------------|---------------|
| US | Jul-Oct 2025 | +24% (+32K regs) | ~50% | $16.7MM |
| UK | Aug-Oct 2025 | +23% (+2.4K regs) | Significant | N/A |
| DE | Oct-Dec 2025 | +18% (+749 regs) | Significant | N/A |
| **Total** | | **+35K regs** | | **$16.7MM+** |

**So what:** OCI consistently delivers 18-24% registration lift across markets of different sizes and maturities. The US result ($16.7MM OPS from 32K incremental regs at $520 CCP) is the flagship proof point for leadership conversations.

### DE Test vs Control Data (Reference)

| Week | Segment | Cost | Regs | ROAS | CPA |
|------|---------|------|------|------|-----|
| W44 | NB Control | $44,592 | 36 | 3% | $1,239 |
| W44 | NB Test (OCI) | $64,565 | 200 | 13% | $323 |
| W44 | Difference | +45% | +456% | +333% | -74% |
| W45 | NB Control | $56,790 | 55 | 3% | $1,033 |
| W45 | NB Test (OCI) | $66,182 | 253 | 13% | $262 |
| W45 | Difference | +17% | +360% | +333% | -75% |

**So what:** The DE data is the cleanest test-vs-control comparison we have. NB CPA dropped 74-75% in the OCI segment. The cost increase (+17-45%) is more than offset by the registration increase (+360-456%). This is the data to show anyone who asks "does OCI actually work?"

## MCC Structure

All OCI markets operate under a shared MCC hierarchy:

| MCC | ID | Markets |
|-----|-----|---------|
| Master (Parent) | DSAP - Amazon Business Parent MCC (873-788-1095) | All |
| NA | 683-476-0964 | US, CA, MX |
| EU | 549-849-5609 | UK, DE, FR, IT, ES |
| JP | 852-899-4580 | JP |
| AU | Not created | N/A (not in OCI scope) |

## Rollout Status (as of March 2026)

| Market | Status | Launch Date | Full Impact |
|--------|--------|-------------|-------------|
| US | ✅ Live (100%) | Jul 2025 → Sep 2025 | Oct 2025 |
| UK | ✅ Live (100%) | Aug 2025 → Sep 2025 | Oct 2025 |
| DE | ✅ Live (100%) | Nov 2025 → Dec 2025 | Jan 2026 |
| CA | 🔄 In Progress | E2E launched 3/4/2026 | Jul 2026 (projected) |
| JP | 🔄 In Progress | E2E launched 2/26/2026 | Jul 2026 (projected) |
| FR | 🔄 In Progress | E2E launched 2/26/2026 | Jul 2026 (projected) |
| IT | 🔄 In Progress | E2E launched 2/26/2026 | Jul 2026 (projected) |
| ES | 🔄 In Progress | E2E launched 2/26/2026 | Jul 2026 (projected) |
| AU | ❌ Not planned | N/A | N/A |
| MX | ❌ Not planned | N/A | N/A |

**AU/MX exclusion:** Neither market is in OCI scope. AU is planned for Adobe OCI integration via Suzane Huynh (May 2026 timeline discussed 3/19). MX has no OCI timeline.

## Known Issues

### Duplicate hvocijid Parameters
**What:** Landing page URLs across EU3 and existing markets (US, UK, DE) are generating duplicate `hvocijid` query parameters. This causes "Duplicate query param found" errors in event processing.

**Impact:** Potential conversion tracking loss — if the duplicate parameter prevents the registration event from being matched to the click, OCI can't optimize for that conversion.

**Affected markets:** US, UK, DE, FR, IT, ES. JP is NOT affected.

**Status:** Under investigation. No resolution timeline as of 3/25/2026.

**Workaround:** Monitor conversion match rates. If match rate drops below 90%, escalate to Google.

## Market-Specific Considerations

| Market | Consideration |
|--------|--------------|
| US | Largest market. OCI impact most visible here. Walmart Brand competition means OCI's NB efficiency is critical for program-level CPA health. |
| UK | Strong OCI results compounded by ad copy test (+86% CTR). Attribute gains carefully — OCI and ad copy are concurrent. |
| DE | Highest-quality test-vs-control data. Use DE data for any "prove OCI works" conversation. Higher Y25 baseline makes YoY comparisons less dramatic. |
| CA | LP optimization already showing strong results (Bulk CVR +187%, Wholesale +180%). OCI will compound these gains. |
| JP | MHLW campaign ended 1/31 — major registration driver gone. OCI needs to offset this structural headwind. Yahoo competition intensifying. |
| FR | bruneau.fr at 39-47% NB IS. OCI will help NB efficiency but won't solve the competitive pressure on NB impressions. |
| IT | Brand Core CPC +131% YoY. OCI helps NB but IT's challenge is Brand-side. |
| ES | Smallest EU market. OCI impact will be proportionally smaller but still meaningful for efficiency. |

## Decision Guide

| Situation | Action | Why |
|-----------|--------|-----|
| E2E test shows conversion mismatch >5% | Debug data pipeline before proceeding to Phase 2 | Bad data in = bad optimization out |
| Phase 2 shows <10% lift after 4 weeks | Extend test 2 more weeks. If still <10%, investigate data quality. | Small markets may need more time for statistical significance. |
| Lift compresses from Phase 2 to Phase 3 | Expected. Proceed to Phase 4 unless compression >50%. | Diminishing returns at scale are normal. |
| Post-100% CPA regresses >10% WoW | Check for: seasonal factors, competitor changes, data pipeline issues. Don't revert without investigation. | Regression is usually external, not OCI failure. |
| Stakeholder asks "does OCI work?" | Show DE W44-W45 test vs control data. Then US $16.7MM OPS figure. | DE is the cleanest proof. US is the biggest impact. |

## Related

- [Eyes — OCI Performance](~/shared/context/body/eyes.md) — live OCI status and metrics
- [OCI Performance Research](~/shared/research/oci-performance.md) — detailed rollout data
- [Brain — D1: OCI Implementation](~/shared/context/body/brain.md) — decision rationale for phased approach
- [OCI Instructions (Quip)](https://quip-amazon.com/Zee9AAlSBEB) — technical setup guide
- [Competitive Landscape](competitive-landscape) — how OCI enables the efficiency-based competitive response

## Sources
- OCI rollout timeline and performance data — source: `shared/research/oci-performance.md`, updated 2026-03-12
- US OPS calculation ($16.7MM) — source: `shared/research/oci-performance.md`, US section
- DE test vs control data (W44-W45) — source: `shared/research/oci-performance.md`, DE section
- MCC structure — source: `shared/context/body/eyes.md`, OCI Performance section
- hvocijid issue — source: `shared/context/body/eyes.md`, Known Issues
- Decision D1 rationale — source: `shared/context/body/brain.md`, Decision Log
- AU OCI timeline (May 2026) — source: `shared/context/active/current.md`, Adobe OCI Rollout project
- Market-specific considerations — source: `shared/context/body/eyes.md`, Market Health + Market Deep Dives

<!-- AGENT_CONTEXT
machine_summary: "OCI (Offline Conversion Import) rollout playbook for AB Paid Search. Phased approach: E2E → 25% → 50% → 100% NB traffic with measurement at each stage. Validated results: US +24% regs ($16.7MM OPS), UK +23%, DE +18%. Currently rolling out to CA/JP/EU3 (E2E launched Feb-Mar 2026, full impact Jul 2026). Known issue: duplicate hvocijid parameters in EU3+existing markets. AU/MX not in scope."
key_entities: ["OCI", "Google Ads", "Non-Brand", "E2E testing", "hvocijid", "MCC", "Adobe", "registration lift", "CPA improvement"]
action_verbs: ["rollout", "validate", "measure", "phase", "monitor", "escalate", "debug"]
update_triggers: ["new market goes live on OCI", "hvocijid issue resolved", "OCI measurement methodology changes", "AU/MX added to OCI scope"]
-->
