<!-- DOC-0452 | duck_id: wiki-oci-playbook-rewrite -->
---
title: "OCI Rollout Playbook: From E2E to 100% in Any Market"
slug: "oci-playbook"
type: "playbook"
audience: "team"
status: "draft"
doc-type: strategy
created: "2026-03-25"
updated: "2026-04-04"
owner: "Richard Williams"
tags: ["oci", "bid-strategy", "testing", "non-brand", "paid-search", "ww"]
depends_on: []
consumed_by: ["wiki-concierge", "najp-analyst", "eu5-analyst", "abix-analyst"]
summary: "Phased playbook for rolling out OCI in any AB Paid Search market — methodology, measurement, known issues, and market considerations."
artifact-status: DRAFT
artifact-audience: amazon-internal
artifact-level: 2
update-trigger: "Quarterly as new markets go live, or when OCI measurement methodology changes"
---

# OCI Rollout Playbook: From E2E to 100% in Any Market

This playbook codifies the OCI rollout methodology that produced 35,196 incremental registrations and $16.7MM in OPS across US, UK, and DE. Use it to replicate the rollout in any new market. A teammate should be able to follow this doc end-to-end without asking the author. For the step-by-step execution reference (Google Ads navigation, monitoring checklists, troubleshooting), see the [OCI Execution Guide](~/shared/artifacts/program-details/2026-04-04-oci-execution-guide.md). For the leadership summary, see the [OCI Business Case](~/shared/artifacts/strategy/2026-04-04-oci-business-case.md).

## What OCI does and does not do

OCI sends actual Amazon Business registration data back to Google Ads. The bidding algorithm then optimizes for real conversions instead of proxy signals like clicks or page views. This improves Non-Brand CPA because the algorithm learns which queries produce registrations. In the US, NB CPA improved by roughly 50%.

OCI does not fix Brand CPA. Brand traffic converts regardless of bidding algorithm. OCI's impact is concentrated on Non-Brand, where query selection matters most. When NB CPA drops 50% via OCI, the team can absorb Brand CPA increases from competitors like Walmart. Total program CPA stays healthy. This is the structural foundation of the efficiency-over-escalation competitive strategy — Decision D1.

## How the phased rollout works

The core insight is that phased rollout with measurement at each stage eliminates risk. Never go from 0% to 100%. Always validate lift before committing more budget. AB Paid Search was the first non-retail business unit at Amazon to implement OCI. The methodology was developed through the US rollout starting July 2025. It was refined in UK (August 2025) and DE (November 2025). It is now being applied across CA, JP, and EU3.

The rollout moves through four phases. Each phase has a clear goal, a defined duration, and an exit criterion that must be met before advancing.

Phase 1 is an end-to-end pipeline test lasting two to four weeks. The goal is to confirm that registrations flow correctly from Amazon's systems to Google Ads. The team sets up the OCI conversion action, configures the data feed, triggers test registrations, and verifies they appear in Google Ads within 24 to 48 hours. Conversion counts should match Amazon's internal data within a 5% tolerance for attribution lag. If the pipeline works and there are no duplicate parameter errors, the market is ready for Phase 2. The US required two weeks of debugging as the first market. UK, DE, and the current wave each took one to two weeks.

Phase 2 allocates 25% of NB traffic to OCI bidding for four to six weeks. The remaining 75% serves as a control. Run this configuration for a minimum of four weeks to accumulate sufficient conversion data. Then compare the OCI segment against the control on registrations, CPA, and ROAS. The exit criterion is a statistically meaningful lift in registrations or CPA improvement versus the control.

Phase 3 expands to 50% of NB traffic for another four to six weeks. The goal is to confirm that lift holds at scale. Watch specifically for diminishing returns — does the lift per incremental percentage of traffic hold, or does it compress? Also check for cannibalization: is OCI stealing conversions from the control, or generating incremental ones? The exit criterion is that lift holds at 50% with no cannibalization evidence. CPA improvement should be consistent with the 25% phase.

Phase 4 is full migration to 100% of NB traffic. Migrate the remaining traffic, decommission control campaigns, and establish new baselines. Brand campaigns remain on manual CPC with bid caps. OCI on Brand is lower-impact but worth testing in mature markets once NB is stable. Monitor weekly CPA and registration tracking for the first eight weeks post-migration. Flag any regression greater than 10% week-over-week for investigation.

The pattern across markets is consistent. The first three markets (US, UK, DE) took three to five months each from E2E to full deployment. The current wave is moving faster because the methodology is established and the MCC infrastructure exists.

## How we measure

The measurement framework is what makes this a validated rollout rather than a hope-and-pray migration.

During Phases 2 and 3, measurement uses test-versus-control comparison. For each phase, compare the OCI segment against the control on cost, registrations, ROAS, and CPA. Always report both absolute numbers and percentages. A 50% CPA improvement sounds impressive until you see it is based on ten registrations.

After Phase 4, there is no control group. Measurement shifts to seasonality-adjusted baselines. Take the same week from the prior year. Adjust for known factors like budget changes, competitor activity, and market events. Compare actualized CPA against the adjusted baseline. Report in the format "OCI lift tracking: W[X] +[Y]% ([Z]% to expectation)." The DE example from W49-W51 2025 illustrates this well. W49 showed +20% lift at 95% to expectation. W50 showed +20% at 96%. W51 showed +16% at 74%. This format tells leadership both the lift and whether it is meeting projections.

## Validated results

OCI consistently delivers 18-24% registration lift across markets of different sizes and maturities. HIGH confidence — this is backed by seven months of data across three markets.

The US produced a 24% lift with 32,047 incremental registrations and $16.7MM in OPS from July through October 2025. UK delivered a 23% lift with 2,400 incremental registrations from August through October 2025. DE produced an 18% lift with 749 incremental registrations from October through December 2025. DE provided the cleanest test-versus-control data in the portfolio.

| Market | Test Period | Reg Lift | NB CPA Improvement | Estimated OPS |
|--------|-----------|----------|-------------------|---------------|
| US | Jul-Oct 2025 | +24% (+32K regs) | ~50% | $16.7MM |
| UK | Aug-Oct 2025 | +23% (+2.4K regs) | Significant | N/A |
| DE | Oct-Dec 2025 | +18% (+749 regs) | Significant | N/A |
| **Total** | | **+35K regs** | | **$16.7MM+** |

The US result ($16.7MM OPS from 32K incremental registrations at $520 CCP) is the flagship proof point for leadership conversations. The DE data is the cleanest proof — use it for any "does OCI actually work?" conversation.

## How DE proved OCI works

The DE W44-W45 data is the strongest evidence in the portfolio. It ran a clean test-versus-control split with sufficient volume.

| Week | Segment | Cost | Regs | ROAS | CPA |
|------|---------|------|------|------|-----|
| W44 | NB Control | $44,592 | 36 | 3% | $1,239 |
| W44 | NB Test (OCI) | $64,565 | 200 | 13% | $323 |
| W44 | Difference | +45% | +456% | +333% | -74% |
| W45 | NB Control | $56,790 | 55 | 3% | $1,033 |
| W45 | NB Test (OCI) | $66,182 | 253 | 13% | $262 |
| W45 | Difference | +17% | +360% | +333% | -75% |

NB CPA dropped 74-75% in the OCI segment. The cost increase of 17-45% is more than offset by the registration increase of 360-456%. The OCI segment spent more but produced dramatically more registrations at a fraction of the cost per registration. This is the data to show anyone who questions whether OCI's lift is real or an attribution artifact.

## Market-by-market considerations

The US is the largest market and the reference implementation. OCI's impact is most visible here. Walmart Business has driven Brand CPA from roughly $40 to $65-77. That makes OCI's NB efficiency gains critical for keeping total program CPA healthy. Without OCI's NB improvement, the Brand CPA increase from competitive pressure would degrade blended program economics.

UK results are strong but require careful attribution. The ad copy test (+86% CTR) ran concurrently with OCI. Both initiatives contributed to the gains. Isolating OCI's specific contribution requires comparing UK OCI lift against DE, which did not have the ad copy test running simultaneously.

DE has the highest-quality test-versus-control data. Use it as the default reference for any "prove OCI works" conversation. The caveat: DE had a high Y25 baseline. This compresses year-over-year comparisons and makes the growth rate look less dramatic than it is in absolute terms.

CA launched E2E on March 4, 2026. Landing page optimization is already showing strong results — Bulk CVR +187%, Wholesale +180%. OCI will compound these gains because better conversion rates give the bidding algorithm more signal. CA is on track for 100% the week of April 7.

JP launched E2E on February 26, 2026, and reached 100% in late March 2026. JP faces a structural headwind: the MHLW campaign ended January 31, removing a significant registration driver. OCI needs to offset this loss. Yahoo competition is also intensifying.

FR launched E2E on February 26, 2026, and reached 100% in late March 2026. The competitive challenge is bruneau.fr holding 39-47% NB impression share. OCI helps NB efficiency but does not solve the impression share pressure. That requires a different competitive response.

IT launched E2E on February 26, 2026, and reached 100% in late March 2026. The primary challenge is Brand-side: Brand Core CPC is up 131% year-over-year. OCI helps NB efficiency but does not address Brand cost pressure.

ES launched E2E on February 26, 2026, and reached 100% in late March 2026. It is the smallest EU market. OCI's absolute impact will be proportionally smaller, but the efficiency improvement is still meaningful for the market's economics.

## MCC structure

All OCI markets operate under a shared MCC hierarchy. The Master MCC (DSAP — Amazon Business Parent MCC, 873-788-1095) sits at the top. The NA MCC (683-476-0964) covers US, CA, and MX. The EU MCC (549-849-5609) covers UK, DE, FR, IT, and ES. The JP MCC (852-899-4580) covers Japan. AU does not have an MCC created yet. It is planned for the Adobe OCI path through Suzane Huynh with a May 2026 target.

The MCC structure matters because OCI conversion actions are configured at the MCC level. A new market joining an existing MCC inherits the conversion tracking infrastructure. A market that needs a new MCC (like AU) requires additional setup time — plan for two to four extra weeks.

## Current rollout status

As of April 2026, eight of ten markets are at full OCI deployment or on track within the week. US, UK, and DE have been live at 100% since late 2025 and serve as the reference implementations. FR, IT, ES, and JP reached 100% in late March 2026. CA is on track for 100% the week of April 7. AU targets May 2026 via the Adobe OCI path, though the MCC has not been created and Adobe has not committed to a firm timeline. MX has no MCC and no timeline.

| Market | Status | Phase | Since |
|--------|--------|-------|-------|
| US | 100% | Live | Oct 2025 |
| UK | 100% | Live | Oct 2025 |
| DE | 100% | Live | Dec 2025 |
| FR | 100% | Live | Mar 2026 |
| IT | 100% | Live | Mar 2026 |
| ES | 100% | Live | Mar 2026 |
| JP | 100% | Live | Mar 2026 |
| CA | On track | Phase 4 | Target 4/7 |
| AU | Planned | Pre-E2E | Target May 2026 |
| MX | No timeline | Not started | — |

Seven markets are live at 100%. CA joins the week of April 7. Full monthly registration impact across all in-progress markets is projected for July 2026. The remaining gap is AU (pending Adobe MCC) and MX (no infrastructure).

## Known issues

Landing page URLs across EU3 and existing markets (US, UK, DE) are generating duplicate `hvocijid` query parameters. This causes "Duplicate query param found" errors in event processing. The potential impact is conversion tracking loss. If the duplicate parameter prevents the registration event from being matched to the click, OCI cannot optimize for that conversion. JP is not affected.

The issue is under investigation with no resolution timeline as of April 2026. The workaround is to monitor conversion match rates. Escalate to Google if the match rate drops below 90%.

## When to make which decision

| Situation | Action | Why |
|-----------|--------|-----|
| E2E test shows conversion mismatch >5% | Debug data pipeline before proceeding to Phase 2 | Bad data in means bad optimization out |
| Phase 2 shows <10% lift after 4 weeks | Extend test 2 more weeks; if still <10%, investigate data quality | Small markets may need more time for statistical significance |
| Lift compresses from Phase 2 to Phase 3 | Expected — proceed to Phase 4 unless compression >50% | Diminishing returns at scale are normal |
| Post-100% CPA regresses >10% WoW | Check seasonal factors, competitor changes, data pipeline issues — do not revert without investigation | Regression is usually external, not OCI failure |
| Stakeholder asks "does OCI work?" | Show DE W44-W45 test-versus-control data, then US $16.7MM OPS figure | DE is the cleanest proof; US is the biggest impact |

The decision guide covers the five most common situations a market owner will face during rollout. The default posture is patience. OCI's learning period means early volatility is expected. Premature intervention is the most common mistake.

## Related

- [OCI Execution Guide](~/shared/artifacts/program-details/2026-04-04-oci-execution-guide.md) — Step-by-step how-to: Google Ads navigation, monitoring, troubleshooting
- [OCI Business Case](~/shared/artifacts/strategy/2026-04-04-oci-business-case.md) — Leadership summary: $16.7MM headline, talking points for Kate/Todd
- [Eyes — OCI Performance](~/shared/context/body/eyes.md) — Live OCI status and metrics
- [Brain — D1: OCI Implementation](~/shared/context/body/brain.md) — Decision rationale for phased approach
- [OCI Instructions (Quip)](https://quip-amazon.com/Zee9AAlSBEB) — Technical setup guide
- [Competitive Landscape](~/shared/artifacts/strategy/2026-03-25-competitive-landscape.md) — How OCI enables the efficiency-based competitive response

---

## Sources
- OCI rollout timeline and performance data — source: shared/research/oci-performance.md, updated 2026-03-12
- US OPS calculation ($16.7MM) — source: shared/research/oci-performance.md, US section
- DE test vs control data (W44-W45) — source: shared/research/oci-performance.md, DE section
- MCC structure — source: ~/shared/context/body/eyes.md, OCI Performance section
- hvocijid issue — source: ~/shared/context/body/eyes.md, Known Issues
- Decision D1 rationale — source: ~/shared/context/body/brain.md, Decision Log
- AU OCI timeline (May 2026) — source: ~/shared/context/active/current.md, Adobe OCI Rollout project
- Market-specific considerations — source: ~/shared/context/body/eyes.md, Market Health + Market Deep Dives
- Market status updated April 2026 — FR/IT/ES/JP at 100% since late March, CA on track 4/7

<!-- AGENT_CONTEXT
machine_summary: "OCI rollout playbook for AB Paid Search. Phased approach: E2E → 25% → 50% → 100% NB traffic with measurement at each stage. Validated results: US +24% regs ($16.7MM OPS), UK +23%, DE +18%, totaling 35,196 incremental registrations. As of April 2026, 7 markets live at 100% (US, UK, DE, FR, IT, ES, JP), CA on track 4/7, AU May 2026, MX TBD. Known issue: duplicate hvocijid parameters in EU3+existing markets. Decision guide covers 5 common rollout scenarios."
key_entities: ["OCI", "Google Ads", "Non-Brand", "E2E testing", "hvocijid", "MCC", "Adobe", "registration lift", "CPA improvement"]
action_verbs: ["rollout", "validate", "measure", "phase", "monitor", "escalate", "debug"]
update_triggers: ["new market goes live on OCI", "hvocijid issue resolved", "OCI measurement methodology changes", "AU/MX added to OCI scope", "CA reaches 100%"]
-->
