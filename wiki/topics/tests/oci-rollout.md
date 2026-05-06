---
title: "OCI Rollout"
type: test
status: ACTIVE
owner: Richard Williams
created: 2026-05-06
updated: 2026-05-06
hedy_topic_id: "tFEsxgnyO4QYp2x7TNrI"
aliases:
  - "oci"
  - "oci-rollout-canada"
  - "oci-ca-launch"
related:
  topics:
    - topics/markets/au
    - topics/markets/mx
    - topics/tests/polaris-brand-lp
  meetings:
    - meetings/weekly-paid-acq
    - meetings/brandon-sync
    - meetings/deep-dive-debate
  state_files:
    - state-files/ww-testing-state
    - state-files/au-paid-search-state
    - state-files/mx-paid-search-state
  wiki_articles: []
  protocols:
    - topics/INGEST-PROTOCOL
---
<!-- DOC-TOPIC-OCI-ROLLOUT -->

# OCI Rollout

## Summary

OCI (Offline Conversion Import) rollout is the multi-market initiative to enable Smart Bidding in Google Ads driven by actual registrations rather than directional signal. Per 2026-04-14 weekly sync (hedy:kQ0V8uBlgzL7eoAwAwVg) Canada began dial-up at 25% on 4/14, UK and Germany already in flight, Japan held for longer learning period due to low volume. Plan for OCI Flash (replacing bi-weekly format) starts 2026-05-11 with full read 2026-06-03. Model validation work preceded this — 2025-09-17 session (hedy:s4EDRCHCvDel3K3DGjSV) covered DE model output validation, 2025-09-22 (hedy:S8vUiG31J8Lmi9qlHhat) covered OCI transition performance.

## Links

- **State file**: [`ww-testing-state.md`](../../state-files/ww-testing-state.md) — Appendix I Active Test Dossier
- **Related market topics**: [`topics/markets/au`](../markets/au.md), [`topics/markets/mx`](../markets/mx.md)
- **Related tests**: [`topics/tests/polaris-brand-lp`](polaris-brand-lp.md)
- **Meeting series**: [`meetings/weekly-paid-acq`](../../meetings/weekly-paid-acq.md), [`meetings/brandon-sync`](../../meetings/brandon-sync.md)

## Stakeholders

| Role | Name | Most recent sourced interaction |
|---|---|---|
| PS owner driving rollout | Richard Williams | 2026-04-14 weekly (hedy:kQ0V8uBlgzL7eoAwAwVg) |
| Weekly team driver | Stacey Gu | 2026-04-14 weekly — confirmed CA dial-up steps |
| OCI Flash co-lead | Andrew Wirtz | 2026-04-14 weekly — confirmed May 11 start |
| Manager | Brandon Munday | recurring weekly + 1:1s |

## Metrics

| Metric | Value | As of | Source |
|---|---|---|---|
| CA dial-up | 25% → 100% target EOW | 2026-W16 | hedy:kQ0V8uBlgzL7eoAwAwVg |
| OCI Flash cadence | Weekly starting 5/11 | 2026-W20 | Andrew + Stacey alignment |
| Learning period | 4 weeks standard | — | Google recommendation |
| Markets live | CA, UK, DE | 2026-04-14 | — |
| Markets pending | JP (needs longer due to low volume) | — | — |

Authoritative weekly test data: [`ww-testing-state.md`](../../state-files/ww-testing-state.md).

## Simplified Timeline

#### 2026-W16 (Apr 13 – Apr 19)
- 2026-04-14 — Canada dial-up began at 25%, planned 100% by EOW; OCI Flash start date set to 5/11

#### 2025-W39 (Sep 22 – Sep 28)
- 2025-09-22 — OCI Transition performance review session

#### 2025-W38 (Sep 15 – Sep 21)
- 2025-09-17 — DE OCI model output validation + deployment planning

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

- [ ] CA VPN tool access for Adi to complete step 3 validation — owner: Richard (coordinating via Chantant team) — source: 2026-04-14 weekly
- [ ] Finalize OCI Flash format (no highlights/lowlights, just status) — owner: Stacey — source: 2026-04-14 weekly
- [ ] Decide whether to shorten learning period for Canada (three weeks vs standard four) — owner: Stacey + Andrew — source: 2026-04-14 weekly

## Closed Items — Audit Trail

- [x] ~~DE OCI model output validation~~ — closed 2025-09-17 — resolution: validation + deployment planning completed — log: [2025-09-17 entry](#2025-09-17--de-oci-model-output-validation--deployment-planning)

## Running Themes

- Market-maturity gate: OCI needs 1+ year market history + IAPRSTCCP availability before Smart Bidding works; this blocks AU + emerging markets (per 2026-04-14 weekly + 2026-04-28 AU handover hedy:eQUxaMZO7Kiiv903HE2e)
- OCI Flash merging with existing flash format: simpler project-status cadence with OCI performance as the top line (per 2026-04-14 weekly)
- Cross-market data sharing within same MCC reduces learning-period risk — CA/DE benefit from UK data (per 2026-04-14 weekly)

## Log

### 2026-04-14 — Canada dial-up, OCI Flash cadence set for 5/11 start

#### Source
hedy:kQ0V8uBlgzL7eoAwAwVg

Related: [meetings/weekly-paid-acq.md](../../meetings/weekly-paid-acq.md), [state-files/ww-testing-state.md](../../state-files/ww-testing-state.md)

#### What was said / what happened
58-min weekly team sync. On Canada rollout Stacey reported: "Steps one and two are done for validation. I think it needs to be done from Canada, VPN, so I'm working with Richard." Canada dial-up started at 25% on 4/14 with plan to reach 100% by EOW. Plan: four-week learning period aligning with other markets.

On OCI Flash cadence Stacey and Andrew aligned: "the week of May 11th is when we'll start our OCI Flash." Quote on format: "we're also going to keep the OCI Flash Similar, so it will be like our regular flash. We're just gonna have project updates in there, no highlights or low lights, just like this project status updates. And then at the top, it's gonna talk about the performance for OCI."

Andrew asked whether to shorten Canada's learning period to three weeks; Stacey responded: "I'd be really hesitant on Japan because it's all low and it might need even longer than four weeks. But Canada could probably also be shortened too."

Stacey noted data sharing benefit: "it already has all of the information from UK and Germany to help it be successful. So probably shortening to three weeks there would be fine."

#### Decisions
- OCI Flash starts 2026-05-11 weekly, full read target 2026-06-03
- OCI Flash merges with existing flash format (project status + OCI performance, no highlights/lowlights)
- Learning period decision for Canada deferred, Japan holds at 4+ weeks

#### Actions
- Richard — secure broader CA VPN access for Adi via Chantant team — ongoing
- Stacey — finalize OCI Flash structure — by 5/11
- Andrew — potentially shorten CA learning period if data supports — ongoing

---

### 2025-09-22 — OCI Transition Performance Review

#### Source
hedy:S8vUiG31J8Lmi9qlHhat

#### What was said / what happened
52-min session. OCI Transition performance review — context pre-dates current rollout. Full transcript in Hedy.

---

### 2025-09-17 — DE OCI model output validation & deployment planning

#### Source
hedy:s4EDRCHCvDel3K3DGjSV

#### What was said / what happened
58-min session. Germany OCI model output validation session + deployment planning. This was the model-validation predecessor to the live market rollout that began in UK/DE and is now expanding to CA. Full transcript in Hedy.

---
