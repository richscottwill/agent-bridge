---
title: "OCI Rollout Playbook: From E2E to 100% in Any Market"
status: FINAL
doc-type: strategy
audience: amazon-internal
level: 2
owner: "Richard Williams"
created: 2026-03-25
updated: 2026-04-04
update-trigger: "Quarterly as new markets go live, or when OCI measurement methodology changes"
tags: ["oci", "bid-strategy", "testing", "non-brand", "paid-search", "ww"]
---

# OCI Rollout Playbook: From E2E to 100% in Any Market

This playbook codifies the OCI rollout methodology that produced 35,196 incremental registrations and $16.7MM in OPS across US, UK, and DE. Use it to replicate the rollout in any new market. A teammate should be able to follow this doc end-to-end without asking the author.

## Context

AB Paid Search was the first non-retail business unit at Amazon to implement OCI. We developed the methodology through the US rollout starting July 2025, refined it in UK (August 2025) and DE (November 2025), and are now applying it across CA, JP, and EU3. As of April 2026, seven of ten markets are at full deployment, with the methodology accelerating — the current wave moved from E2E to 100% in weeks rather than months.

OCI sends actual Amazon Business registration data back to Google Ads. The bidding algorithm then optimizes for real conversions instead of proxy signals like clicks or page views. This improves Non-Brand CPA because the algorithm learns which queries produce registrations. In the US, NB CPA improved by roughly 50%.

OCI does not fix Brand CPA. Brand traffic converts regardless of bidding algorithm. OCI's impact is concentrated on Non-Brand, where the algorithm's query selection matters most. When NB CPA drops 50% via OCI, the team can absorb Brand CPA increases from competitors like Walmart without total program CPA degrading. This is the structural foundation of the efficiency-over-escalation competitive strategy.

## The phased rollout

The core insight is that phased rollout with measurement at each stage eliminates risk. Never go from 0% to 100%. Always validate lift before committing more budget. This is Decision D1 — evidence over intuition.

### How to prove the pipeline works (Phase 1)

The first phase is an end-to-end pipeline test lasting two to four weeks. The goal is to confirm that registrations flow correctly from Amazon's systems into Google Ads. You set up the OCI conversion action, configure the data feed, and trigger test registrations. Those registrations should appear in Google Ads within 24 to 48 hours.

The key validation metric is conversion count accuracy. Counts should match Amazon's internal data within 5% tolerance for attribution lag. If the pipeline works and there are no duplicate parameter errors, the market is ready for the next phase. The US required two weeks of debugging as the first market. Every subsequent market has taken one to two weeks. One infrastructure factor affects timeline: markets joining an existing MCC inherit conversion tracking infrastructure and roll out faster, while markets requiring a new MCC (like AU) need additional setup time and cross-functional coordination.

For the step-by-step Google Ads setup, monitoring checklists, and troubleshooting procedures, see the [OCI Execution Guide](~/shared/artifacts/program-details/2026-04-04-oci-execution-guide.md).

### How to validate lift on a subset (Phase 2)

Phase 2 allocates 25% of NB traffic to OCI bidding for four to six weeks. The remaining 75% serves as a control. The goal is straightforward: prove OCI produces lift before committing more budget.

Run the split for a minimum of four weeks. This gives the algorithm enough conversion data to learn. Then compare the OCI segment against the control on registrations, CPA, and ROAS. You need a statistically meaningful lift in registrations or CPA improvement to proceed. If lift is below 10% after four weeks, extend two more weeks. If it is still below 10%, investigate data quality before moving forward.

### How to confirm lift holds at scale (Phase 3)

Phase 3 expands to 50% of NB traffic for another four to six weeks. The question changes here. You are no longer asking "does OCI work?" — you are asking "does it scale?"

Watch for two things. First, diminishing returns: does the lift per incremental percentage of traffic hold, or does it compress? Second, cannibalization: is OCI stealing conversions from the control segment, or generating incremental ones? Some compression from Phase 2 to Phase 3 is normal. Proceed to Phase 4 unless compression exceeds 50%.

### How to execute full migration (Phase 4)

Phase 4 migrates the remaining traffic to 100% OCI. Decommission control campaigns and establish new baselines for ongoing monitoring. Brand campaigns remain on manual CPC with bid caps. OCI on Brand is lower-impact but worth testing in mature markets once NB is stable.

Monitor weekly CPA and registration tracking for the first eight weeks post-migration. Flag any regression greater than 10% week-over-week for investigation. The default posture is patience — OCI's learning period means early volatility is expected. Premature intervention is the most common mistake.

## How we measure

The measurement framework is what makes this a validated rollout rather than a hope-and-pray migration.

During Phases 2 and 3, we use test-versus-control comparison. For each phase, compare the OCI segment against the control on cost, registrations, ROAS, and CPA. Always report both absolute numbers and percentages. A 50% CPA improvement sounds impressive until you see it is based on ten registrations.

After Phase 4, there is no control group. Measurement shifts to seasonality-adjusted baselines. Take the same week from the prior year. Adjust for known factors like budget changes, competitor activity, and market events. Compare actualized CPA against the adjusted baseline. Report in the format "OCI lift tracking: W[X] +[Y]% ([Z]% to expectation)."

### Validated results

OCI consistently delivers 18-24% registration lift across markets of different sizes and maturities. The US produced a 24% lift with 32,047 incremental registrations and $16.7MM in OPS from July through October 2025. UK delivered a 23% lift with 2,400 incremental registrations from August through October 2025. DE produced an 18% lift with 749 incremental registrations from October through December 2025. DE also provided the cleanest test-versus-control data in the portfolio. The US result ($16.7MM OPS from 32K incremental registrations at $520 CCP) is the flagship proof point for leadership conversations. The DE data is the cleanest proof — use it for any "does OCI actually work?" conversation.

### DE test-versus-control reference data

The DE W44-W45 data is the strongest evidence in the portfolio. It ran a clean test-versus-control split with sufficient volume to draw conclusions with HIGH confidence.

| Week | Segment | Cost | Regs | ROAS | CPA |
|------|---------|------|------|------|-----|
| W44 | NB Control | $44,592 | 36 | 3% | $1,239 |
| W44 | NB Test (OCI) | $64,565 | 200 | 13% | $323 |
| W44 | Difference | +45% | +456% | +333% | -74% |
| W45 | NB Control | $56,790 | 55 | 3% | $1,033 |
| W45 | NB Test (OCI) | $66,182 | 253 | 13% | $262 |
| W45 | Difference | +17% | +360% | +333% | -75% |

NB CPA dropped 74-75% in the OCI segment. The cost increase of 17-45% is more than offset by the registration increase of 360-456%. The OCI segment spent more but produced dramatically more registrations at a fraction of the cost per registration.

## What the rollout taught us across markets

The ten-market rollout revealed three patterns that any new market owner should internalize before starting Phase 1.

The first pattern is that OCI's efficiency gains do not solve competitive impression share pressure. FR's bruneau.fr holds 39-47% NB impression share, which requires a separate competitive response that bidding optimization alone cannot deliver. Similarly, the US faces Walmart Business driving Brand CPA from roughly $40 to $65-77. OCI makes the NB side efficient enough to absorb that pressure, but it does not eliminate the competitive threat. Any market with a dominant NB competitor needs a parallel competitive strategy alongside OCI.

The second pattern is that OCI addresses NB efficiency but cannot offset Brand-side cost pressure. IT showed this clearly — Brand Core CPC is up 131% year-over-year, and OCI's NB focus cannot address that. The same dynamic applies in any market where Brand costs are rising independently of NB performance. OCI keeps the blended program economics healthy by improving one side of the equation, not both.

The third pattern is that concurrent initiatives complicate attribution but compound results. UK ran an ad copy test (+86% CTR) simultaneously with OCI. Both contributed to the strong results, but isolating OCI's specific contribution requires comparing UK against DE, which did not have the ad copy test running. CA is showing a similar dynamic — landing page optimization (Bulk CVR +187%, Wholesale +180%) is compounding with OCI because better conversion rates give the bidding algorithm more signal. When planning a rollout, decide upfront whether to isolate OCI or accept compounded attribution.

JP faces a structural headwind worth noting: the MHLW campaign ended January 31, removing a significant registration driver. OCI needs to offset this loss while Yahoo competition intensifies. Not every market enters OCI from a position of growth.

## Known issues

Landing page URLs across EU3 and existing markets (US, UK, DE) are generating duplicate `hvocijid` query parameters. This causes "Duplicate query param found" errors in event processing. The potential impact is conversion tracking loss — if the duplicate parameter prevents the registration event from being matched to the click, OCI cannot optimize for that conversion. JP is not affected.

The issue is under investigation with no resolution timeline as of April 2026. The workaround is to monitor conversion match rates. Escalate to Google if the match rate drops below 90%.

## When to make which decision

| Situation | Action | Why |
|-----------|--------|-----|
| E2E test shows conversion mismatch >5% | Debug data pipeline before proceeding to Phase 2 | Bad data in means bad optimization out |
| Phase 2 shows <10% lift after 4 weeks | Extend test 2 more weeks; if still <10%, investigate data quality | Small markets may need more time for statistical significance |
| Lift compresses from Phase 2 to Phase 3 | Expected — proceed to Phase 4 unless compression >50% | Diminishing returns at scale are normal |
| Post-100% CPA regresses >10% WoW | Check seasonal factors, competitor changes, data pipeline issues — do not revert without investigation | Regression is usually external, not OCI failure |
| Stakeholder asks "does OCI work?" | Show DE W44-W45 test-versus-control data, then US $16.7MM OPS figure | DE is the cleanest proof; US is the biggest impact |

The decision guide covers the five most common situations a market owner will face during rollout.

## Related

- [OCI Execution Guide](~/shared/artifacts/program-details/2026-04-04-oci-execution-guide.md) — Follow the step-by-step Google Ads navigation, monitoring checklists, and troubleshooting procedures
- [OCI Business Case](~/shared/artifacts/strategy/2026-04-04-oci-business-case.md) — Use the $16.7MM headline and talking points when briefing Kate/Todd
- [Eyes — OCI Performance](~/shared/context/body/eyes.md) — Check live OCI status and metrics across markets
- [Brain — D1: OCI Implementation](~/shared/context/body/brain.md) — Review the decision rationale for the phased approach
- [OCI Instructions (Quip)](https://quip-amazon.com/Zee9AAlSBEB) — Set up OCI conversion actions using the technical guide
- [Competitive Landscape](~/shared/artifacts/strategy/2026-03-25-competitive-landscape.md) — Understand how OCI enables the efficiency-based competitive response

---

## Sources
- OCI rollout timeline and performance data — source: shared/research/oci-performance.md, updated 2026-03-12
- US OPS calculation ($16.7MM) — source: shared/research/oci-performance.md, US section
- DE test vs control data (W44-W45) — source: shared/research/oci-performance.md, DE section
- hvocijid issue — source: ~/shared/context/body/eyes.md, Known Issues
- Decision D1 rationale — source: ~/shared/context/body/brain.md, Decision Log
- AU OCI timeline (May 2026) — source: ~/shared/context/active/current.md, Adobe OCI Rollout project
- Market-specific considerations — source: ~/shared/context/body/eyes.md, Market Health + Market Deep Dives

<!-- AGENT_CONTEXT
machine_summary: "OCI rollout playbook for AB Paid Search. Phased approach: E2E → 25% → 50% → 100% NB traffic with measurement at each stage. Validated results: US +24% regs ($16.7MM OPS), UK +23%, DE +18%, totaling 35,196 incremental registrations. As of April 2026, 7/10 markets at 100%. Three cross-market patterns: OCI doesn't solve competitive IS pressure, doesn't offset Brand-side cost pressure, and compounds with concurrent initiatives. Known issue: duplicate hvocijid parameters in EU3+existing markets. Decision guide covers 5 common rollout scenarios."
key_entities: ["OCI", "Google Ads", "Non-Brand", "E2E testing", "hvocijid", "registration lift", "CPA improvement"]
action_verbs: ["rollout", "validate", "measure", "phase", "monitor", "escalate", "debug"]
update_triggers: ["new market goes live on OCI", "hvocijid issue resolved", "OCI measurement methodology changes", "AU/MX added to OCI scope"]
-->
