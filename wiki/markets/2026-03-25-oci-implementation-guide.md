<!-- DOC-0323 | duck_id: program-oci-implementation-guide -->
> **⚠️ ARCHIVED — 2026-04-04. Replaced by oci-execution-guide. Do not update this file.**

---
title: OCI Implementation Guide — Per-Market
status: archived
audience: amazon-internal
level: N/A
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: new OCI market launches, phase transitions, troubleshooting discoveries
---

# OCI Implementation Guide — Per-Market

---

> This is the hands-on execution guide. For the strategic methodology and results, see [OCI Rollout Methodology](~/shared/artifacts/testing/2026-03-25-oci-rollout-methodology.md).

## Purpose

Step-by-step guide for implementing OCI in a new market. Complements the OCI Rollout Methodology (testing/) with tactical execution details.

## Prerequisites

Before launching OCI in a market:
- [ ] Conversion tracking verified (Google Ads → Tools → Conversions)
- [ ] Minimum 30 conversions/month in the target campaign
- [ ] Baseline performance captured (4 weeks minimum)
- [ ] Brand campaigns excluded (manual bid caps stay)
- [ ] Stakeholder briefed on expected behavior (CPA may spike week 1)

## Step-by-Step: E2E Launch

### 1. Select campaigns
- NB campaigns only (never Brand)
- Start with highest-volume NB campaign for fastest signal

### 2. Change bidding strategy
- Google Ads → Campaign → Settings → Bidding
- Switch from Manual CPC to "Maximize Conversions" or "Target CPA"
- If Target CPA: set to current 4-week average CPA (don't set aggressive target)

### 3. Monitor (daily for week 1, then weekly)
- CPA: expect volatility in week 1-2, stabilization by week 3-4
- Conversion volume: should maintain or increase
- Search terms: review for quality degradation
- Budget: ensure daily budget isn't limiting (OCI needs room to bid)

### 4. Evaluate at 4 weeks
- Compare: OCI period CPA vs pre-OCI baseline (seasonality-adjusted)
- If CPA within 115%: proceed to 25% scale
- If CPA >120% for 7+ consecutive days: pause and investigate

## Scaling

Follow the phased framework in [OCI Rollout Methodology](~/shared/artifacts/testing/2026-03-25-oci-rollout-methodology.md). Gate criteria: 115% at 25%, 110% at 50%.

## Troubleshooting

| Issue | Likely Cause | Fix |
|-------|-------------|-----|
| CPA spiking week 1 | Algorithm learning | Wait. Evaluate at week 3-4. |
| CPA still high at week 4 | Target too aggressive or low volume | Raise target CPA by 10-15%. Check conversion volume. |
| Conversion tracking errors | Tag implementation | Verify Google Tag, check for duplicate tags |
| Search term quality drop | Broad match expansion | Add negative keywords, review search term report weekly |
| Budget limited | OCI bidding higher than manual | Increase daily budget or narrow targeting |
| Duplicate hvocijid in URLs | Parameter appended twice on landing pages | Under investigation (EU3 + existing markets). Do not block rollout. |
| Conversion lag | Delayed conversion attribution | Wait 72 hours before evaluating daily CPA. Use 7-day rolling average. |

## Per-Market Notes

| Market | Special Considerations |
|--------|----------------------|
| US | Complete. Reference implementation. |
| UK | Complete. weareuncapped competitor — monitor Brand IS. |
| DE | Complete. High Y25 baseline — adjust expectations. |
| CA | E2E launched 3/4. Monitor closely. |
| JP | E2E launched 2/26. MHLW headwind — lower volume. |
| FR | E2E launched 2/26. bruneau.fr NB pressure. |
| IT | E2E launched 2/26. Low volume — patience needed. |
| ES | E2E launched 2/26. AGL competitor emerging. |
| AU | Not planned. No OCI support from Google. |
| MX | Not planned. No OCI support from Google. |

US is the reference implementation. UK/DE are complete. CA/JP/EU3 are in E2E — monitor weekly. AU/MX are excluded because Google doesn't support OCI in those markets.

## Known Issues
- Duplicate hvocijid parameters in landing page URLs (EU3 + existing markets)
- JP not affected
- Under investigation — do not block rollout


## Sources
- Phased rollout steps (E2E→25%→50%→100%) — source: ~/shared/context/body/brain.md → D1: OCI Implementation Approach
- Gate criteria (115%, 110%) — source: derived from D1 methodology + operational experience
- Market status and special considerations — source: ~/shared/context/body/eyes.md → OCI Performance → Rollout Timeline
- Troubleshooting table — source: operational experience documented in eyes.md → OCI Performance
- hvocijid issue — source: ~/shared/context/body/eyes.md → OCI Performance → Known Issues
- Conversion tracking prerequisites — source: Google Ads best practices + OCI rollout experience

<!-- AGENT_CONTEXT
machine_summary: "Tactical execution guide for implementing OCI in new AB PS markets. Covers prerequisites, step-by-step E2E launch, monitoring cadence, troubleshooting, and per-market notes. Companion to oci-rollout-methodology (strategy) — this doc is the how-to."
key_entities: ["OCI", "Google Ads", "NB campaigns", "E2E launch", "Target CPA", "Maximize Conversions", "hvocijid"]
action_verbs: ["implement", "monitor", "troubleshoot", "scale", "evaluate"]
update_triggers: ["new OCI market launches", "new troubleshooting issue discovered", "phase transition in any market"]
-->
