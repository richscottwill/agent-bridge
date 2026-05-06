---
title: "Polaris Brand Landing Page Test"
type: test
status: ACTIVE
owner: Richard Williams
created: 2026-03-26
updated: 2026-05-06
hedy_topic_id: ""
aliases:
  - "polaris brand lp"
  - "brand landing page"
  - "polaris"
  - "mx-polaris-test"
  - "polaris-lp-testing"
related:
  topics:
    - topics/markets/mx
    - topics/markets/au
    - topics/initiatives/mcs-polaris-migration
  meetings:
    - meetings/brandon-sync
    - meetings/mcs-polaris-rollout
    - meetings/au-paid-search-sync
    - meetings/mx-paid-search-sync
    - meetings/weekly-paid-acq
  state_files:
    - state-files/ww-testing-state
    - state-files/mx-paid-search-state
    - state-files/au-paid-search-state
  wiki_articles: []
  protocols:
    - topics/INGEST-PROTOCOL
---
<!-- DOC-TOPIC-POLARIS-BRAND-LP -->

# Polaris Brand Landing Page Test

## Summary

Weblab test migrating brand keyword traffic to Polaris-templated brand landing pages. Launched MX on 2026-03-26, reverted 2026-04-13 after CPA regression. Per 2026-04-28 WBR W17 entry, MX results contradicted global hypothesis and WW rollout was paused. Per 2026-05-06 weekly sync entry, AMO content cache is blocking live push and Weblab dial-up is staged pending deploy. Per 2026-04-22 entry, MX W15 NB drop was provisionally flagged as a regime breakpoint in the MPE spec pending Yun-Kang investigation.

## Links

- **State file**: [`ww-testing-state.md`](../../state-files/ww-testing-state.md) — Appendix I Active Test Dossier is authoritative for test status, flags, sources
- **State files (market)**: [`mx-paid-search-state.md`](../../state-files/mx-paid-search-state.md), [`au-paid-search-state.md`](../../state-files/au-paid-search-state.md)
- **Related topics**: [`topics/markets/mx`](../markets/mx.md), [`topics/markets/au`](../markets/au.md), [`topics/initiatives/mcs-polaris-migration`](../initiatives/mcs-polaris-migration.md)
- **Meeting series**: [`meetings/mcs-polaris-rollout.md`](../../meetings/mcs-polaris-rollout.md), [`meetings/brandon-sync.md`](../../meetings/brandon-sync.md), [`meetings/weekly-paid-acq.md`](../../meetings/weekly-paid-acq.md)
- **Asana**: <TBD — parent task>
- **Weblab**: <TBD>

## Stakeholders

| Role | Name | Most recent sourced interaction |
|---|---|---|
| Primary owner | Richard Williams | 2026-05-06 team sync (hedy:qbgFqERRUQl6Eh2PcI8S) |
| Manager | Brandon Munday | 2026-04-06 1:1 (hedy — see [brandon-sync.md](../../meetings/brandon-sync.md) § 2026-04-06) |
| AU stakeholder | Lena Zak | 2026-04-06 — Brandon reported Lena had reached out to Dwayne for AU-specific changes |
| MX stakeholder | Lorena Alvarez | 2026-05-05 sync (hedy:FKZWlEQGcW5S2tv3FCav) |
| Tech contact | Dwayne Palmer's team | 2026-04-06 — Brandon said he told Dwayne to pause and align with global plan |
| Platform | MCS Polaris team | 2026-05-06 — team-sync flagged AMO cache issue (hedy:qbgFqERRUQl6Eh2PcI8S) |

## Metrics

| Metric | MX (pre-revert) | AU | WW target | As of | Source |
|---|---|---|---|---|---|
| Brand CVR delta | — | -18% | neutral-or-positive | 2026-W17 | [brandon-sync.md 2026-04-08 read](../../meetings/brandon-sync.md) |
| NB CVR delta | — | -34% | neutral-or-positive | 2026-W17 | [brandon-sync.md 2026-04-08 read](../../meetings/brandon-sync.md) |
| MX test weeks run | ~3 weeks | — | — | W11–W14 | state-files history |
| MX regime breakpoint | W15 NB drop | — | — | 2026-W15 | session-log 2026-04-22 |

Authoritative weekly data: [`ww-testing-state.md`](../../state-files/ww-testing-state.md).

## Simplified Timeline

#### 2026-W19 (May 4 – May 10)
- 2026-05-06 — AMO cache blocking live content deploy, Weblab ready

#### 2026-W18 (Apr 27 – May 3)
- 2026-04-28 — WW rollout paused after MX results contradicted hypothesis

#### 2026-W17 (Apr 20 – Apr 26)
- 2026-04-22 — MX W15 NB drop flagged as provisional regime breakpoint
- 2026-04-22 — MCS Polaris template migration update (dgVB26RMt6eMqak5WuHR)

#### 2026-W16 (Apr 13 – Apr 19)
- 2026-04-16 — Polaris LP Optimization and Italy Ref Tag Issue (X9gMGQMOFP25yu51oySX)
- 2026-04-15 — Polaris Brand LP and Canada Optimization Review (rg3S3JC10W7SuXHOyliE)
- 2026-04-14 — Baloo/Mexico Testing + Polaris page alignment (Brandon 1:1)

#### 2026-W15 (Apr 6 – Apr 12)
- 2026-04-13 — MX Polaris reverted due to CPA regression
- 2026-04-08 — Adi Landing Page Optimization (pV4Rlf6vsEIa2a7WFUgz)
- 2026-04-06 — Brandon 1:1: AU Polaris conversion-rate data request, Lena intervention

#### 2026-W13 (Mar 23 – Mar 29)
- 2026-03-26 — MX Polaris launched as early test market
- 2026-03-24 — Polaris Brand LP Rollout and Weblab Planning (maKRIlUS6RdghDtTwAis)
- 2026-03-23 — AU CPC and Polaris Rollout Sync with Brandon (4veBOAWYumVzlJciaLVg)

## Table of Contents

- [Summary](#summary)
- [Links](#links)
- [Stakeholders](#stakeholders)
- [Metrics](#metrics)
- [Simplified Timeline](#simplified-timeline)
- [Open Items](#open-items)
- [Closed Items — Audit Trail](#closed-items--audit-trail)
- [Running Themes](#running-themes)
- [Log](#log)

## Open Items

- [ ] AMO cache fix — owner: MCS platform — source: 2026-05-06 team sync (hedy:qbgFqERRUQl6Eh2PcI8S)
- [ ] Secondary QA once brand LPs push live — owner: Richard — source: 2026-05-06 team sync
- [ ] Investigate MX W15 NB drop root cause — owner: Yun-Kang — source: session-log 2026-04-22
- [ ] Refresh WW rollout sequencing decision post-AMO-fix — owner: Richard + Brandon — source: 2026-04-28 WBR W17 context

## Closed Items — Audit Trail

- [x] ~~MX Polaris early-market launch~~ — closed 2026-03-26 — resolution: MX selected and launched (source: state-files history) — log: [2026-03-26 entry](#2026-03-26--mx-polaris-launched)
- [x] ~~MX CPA regression threshold decision~~ — closed 2026-04-13 — resolution: CPA exceeded revert threshold, test reverted (source: state-files history) — log: [2026-04-13 entry](#2026-04-13--mx-polaris-reverted)

## Running Themes

- Platform-side push reliability is the constraint: AMO cache block (2026-05-06 entry) follows the Italy ref tag issue pattern from earlier rollouts — technical push gaps keep blocking tests that are otherwise "ready"
- MX as test market surfaces contradictory signal: MX revert (2026-04-13) + MX W15 NB drop (2026-04-22) + MX results contradicted hypothesis (2026-04-28) — three entries where MX data diverged from WW expectation
- Data-led posture in response to stakeholder pressure: Brandon's 2026-04-06 pushback on Lena's direct request to Dwayne — "we want to be data-led"

## Log

### 2025-11-19 — Canada Polaris ref-marker override catch (Adi 1:1)

#### Source
hedy:UlQUG8kl9BA5Ws23hCzM

Related: [meetings/adi-sync.md](../../meetings/adi-sync.md)

#### What was said / what happened
During first post-leave 1:1, Adi reported on Canada Polaris URL swap work (Stacey-led, Alex-tracked). Adi caught specific pattern: some new Polaris pages had ref-markers that **overrode the CPS ref-marker on navigation links** — caught and fixed via authoring toggle. Reusable learning — same pattern likely recurs on future Polaris migrations in other markets.

Richard's context (quoted): "because those call to actions are where most of the people are gonna register and if it's like being overwritten then that's not good... that's like where whoever created that page there's the this check mark that you can do where you can add, you can overwrite with a new ref marker instead of just keeping whatever the ref marker is from when people click the add."

Root cause: page-authoring default allows ref-marker override when it should preserve the CPS ref-marker. Fix: authoring toggle on each new Polaris page. Richard and Adi both uncertain why this setting exists vs being the default preserve-behavior.

#### Decisions
- Checklist for future Polaris migrations: verify authoring toggle set correctly for ref-marker preservation on every new page

#### Actions
- Adi: continue cross-checking remaining Canada Polaris pages for ref-marker override
- Richard: flag pattern to MCS team for future rollouts (MX, other EU markets)

#### Notes
This catch foreshadowed the 4/16 Italy ref-tag-override crisis (B2B MCS CP PS Brain → misrouted to Australia domain). Pattern was visible on Canada Polaris migration 5 months earlier. Worth auditing: do all completed Polaris migrations have the preserve-toggle enabled? Candidate for wiki-maintenance to grep state-files for this pattern.

---

### 2026-05-06 — AMO cache blocking live push, Weblab ready

#### Source
hedy:qbgFqERRUQl6Eh2PcI8S

Related: [meetings/weekly-paid-acq.md](../../meetings/weekly-paid-acq.md), [meetings/mcs-polaris-rollout.md](../../meetings/mcs-polaris-rollout.md), [state-files/ww-testing-state.md](../../state-files/ww-testing-state.md)

#### What was said / what happened
In the paid acquisition weekly team sync, Richard reported on Polaris testing during the testing update. Quote from transcript: "there was some kind of cash issue on AM. So when they did actually make the updates, they weren't being reflected live. So that's something that's holding us back. And we should hear from that team today or tomorrow on the phone and the Weblab is ready. It's basically ready to go live. It just needs the updates from the website." Brandon confirmed updates were needed from the brand landing pages. Richard said he had already gone through the landing pages with the team, updates are in place, but the content isn't being pushed live to the page. Weblab is gated on the content deploy.

#### Decisions
- None formal this session

#### Actions
- Richard — monitor AMO cache fix and run secondary QA immediately on push — this week (stated during the sync)
- Team — perform secondary QA after Richard's first pass once live

---

### 2026-04-16 — 10 Polaris LP optimization suggestions + Italy ref-tag crisis

#### Source
hedy:X9gMGQMOFP25yu51oySX

Related: [topics/markets/mx](../markets/mx.md), [topics/markets/au](../markets/au.md), [meetings/mcs-polaris-rollout.md](../../meetings/mcs-polaris-rollout.md), [state-files/ww-testing-state.md](../../state-files/ww-testing-state.md)

#### What was said / what happened
60-min LP testing session with Richard leading + Brandon, Dwayne, Adi, Stacey. Richard presented **10 optimization suggestions** based on 2026-W15 Weblab feedback consolidation:

1. **Remove outbound links** (Explore Category button — tied to percolate component, needs dev to decouple)
2. **Minimal header** (already evergreen)
3. **Reduce white space** (esp. mobile widths)
4. **Replace percolate widget with benefit cards** (Yun-Kang + Andrew proposed for Germany)
5. **Localized country in subheadline** — "From Sole Props to Enterprise, sign up for Amazon Business Canada" pattern (test in CA + EU5)
6. **Remove "What do I need to register" FAQ** — replace with "All you need is a work email"
7. **Add "Is Amazon Business free?" FAQ**
8. **Add "What are the pricing benefits?" FAQ**
9. **Add closing CTA + tagline at bottom** (currently no persistent CTA below fold)
10. **Update hero image + monitor CVR post-change** (Enidobi alert at campaign/ad-group level)

Richard shared early US data: "6% increase in conversion with the current set of that we have for the US brand page" based on 20 days pre/post Polaris rollout (March 24).

**Critical Italy finding — Stacey:** Italy brand pages went live on Polaris template prematurely. Ref tag is being overwritten. Quote: "right now all of our Italy brand is MCS Polaris page. And our ref tag got override when people click on the creative free account. You'll go to B2B MCS, CP, PS, Brain." Effectively: Italy registrations misrouting to Australia domain = not tracked, not verified. Must revert to old MCS template ASAP.

#### Decisions
- Benefit cards replace percolate widget globally
- Outbound links removed from template
- Subheadline standardized with country localization + business-size inclusivity
- FAQ section streamlined (remove scary reg requirement, add free + pricing benefits)
- Closing CTA added to all pages
- Italy rollout reverted to old MCS template (critical tracking restoration)

#### Actions
- Richard — coordinate with Alex (Andes) to revert Italy Polaris page — ASAP
- Richard — update/create SIM for corrected template — before Weblab setup
- Team — Weblab setup in US/DE/FR — target 4/20
- Richard — propose Enidobi alert at campaign/ad-group level for CVR monitoring — 4/18

---

### 2026-04-28 — Mexico results contradicted hypothesis, WW paused

#### Source
hedy:DlrGpwhm2LhxFvDpC8Rr | wbr:2026-W17

Related: [topics/markets/mx](../markets/mx.md), [state-files/ww-testing-state.md](../../state-files/ww-testing-state.md), [state-files/mx-paid-search-state.md](../../state-files/mx-paid-search-state.md)

#### What was said / what happened
Per W17 WBR callout and the Brandon/testing sync: MX Polaris-branded LP weblab showed negative CPA impact rather than expected lift. WW rollout was paused.

#### Decisions
- WW rollout is not automatic on MX-positive result; requires positive-or-neutral confirmation before rollout resumes

---

### 2026-04-22 — MX W15 NB drop flagged as provisional regime breakpoint

#### Source
session-log:2026-04-22 | hedy:kQ0V8uBlgzL7eoAwAwVg

Related: [topics/markets/mx](../markets/mx.md), [state-files/mx-paid-search-state.md](../../state-files/mx-paid-search-state.md)

#### What was said / what happened
Per session-log: MX non-brand registrations dropped at W15. The Market Projection Engine spec was updated to flag W15 as a provisional regime breakpoint, pending Yun-Kang investigation into root cause (Polaris-caused, Sparkle-adjacent, or unrelated).

#### Actions
- Yun-Kang — investigate W15 NB drop root cause — open as of session-log entry
- Richard — hold MPE codification decision until investigation resolves — open as of session-log entry

---

### 2026-04-13 — MX Polaris reverted

#### Source
state-files history | [ww-testing-state.md Appendix I](../../state-files/ww-testing-state.md)

Related: [topics/markets/mx](../markets/mx.md)

#### What was said / what happened
MX Polaris brand LP test reverted. Per state-files history: CPA regression exceeded revert threshold.

---

### 2026-03-26 — MX Polaris launched

#### Source
state-files history

Related: [topics/markets/mx](../markets/mx.md), [meetings/mcs-polaris-rollout.md](../../meetings/mcs-polaris-rollout.md)

#### What was said / what happened
MX selected as early test market for Polaris brand LP migration, ahead of WW rollout. Launch date per state-files history.

---
