---
title: "RefTag Taxonomy System — Replacing Feature Registry"
type: initiative
status: ACTIVE
owner: Christine (AB Marketing)
created: 2026-05-06
updated: 2026-05-06
aliases:
  - "reftag-taxonomy"
  - "refmarker-taxonomy"
  - "feature-registry-replacement"
related:
  topics:
    - topics/markets/mx
    - topics/markets/au
    - topics/tests/baloo-shop-subdomain
    - topics/initiatives/mcs-polaris-migration
  meetings: []
  state_files: []
  wiki_articles: []
  protocols:
    - topics/INGEST-PROTOCOL
---
<!-- DOC-TOPIC-INITIATIVE-REFTAG-TAXONOMY -->

# RefTag Taxonomy System — Replacing Feature Registry

## Summary

Cross-functional initiative owned by Christine (AB Marketing) to build a centralized RefTag taxonomy replacing Feature Registry, which is deprecating in Q2 2026. Per 2026-04-27 workshop (hedy:m85ITBLjL9iJ4Nlxz2Nr), the system will define RefTag structure, ownership model, and data tables for attribution across acquisition/engagement/on-site/off-site/email/push/field/pipeline channels. Key constraints: 64-character RefTag limit forces prioritization of embedded attributes vs. joined-from-data-table attributes. Edge cases flagged by Richard and peers: ref tag loss on Baloo registration flow (see [baloo-shop-subdomain.md § 2026-04-14](../tests/baloo-shop-subdomain.md)), verification/R&O/AIT teams only parsing regex (not full tag) from Feed-on-Street flows, MCS-only fixed pattern for free traffic, product-led sends (spend analysis emails, detail-page promo clicks, Galileo/Newton placements) as ambiguous attribution boundary between product and marketing.

## Links

- **Owner**: Christine (AB Marketing); channel owners + data team (ABMA) co-contributors
- **Deprecation target**: Feature Registry, Q2 2026

## Stakeholders

| Role | Name | Most recent sourced interaction |
|---|---|---|
| Workshop owner | Christine | 2026-04-27 RefTag Taxonomy Workshop (hedy:m85ITBLjL9iJ4Nlxz2Nr) |
| PS paid-search reps | Richard Williams, Adi Thakur, Andrew Wirtz, Stacey Gu | 2026-04-27 same |
| MCS rep | Joanne | 2026-04-27 same |
| F90/LiveRamp | Abdul | referenced |
| Partner rep | Anna (MX GLEDA bank partnership) | 2026-04-27 same |
| Feed-on-street rep | Harsha | 2026-04-27 same — raised regex-parsing gap |

## Simplified Timeline

#### 2026-W17 (Apr 20 – Apr 26)
- 2026-04-27 — All-hands taxonomy workshop. Channels, program/campaign types, attributes captured. Feed-on-street regex gap and MCS fixed pattern surfaced.

## Table of Contents

- [Summary](#summary)
- [Links](#links)
- [Stakeholders](#stakeholders)
- [Simplified Timeline](#simplified-timeline)
- [Open Items](#open-items)
- [Closed Items — Audit Trail](#closed-items--audit-trail)
- [Running Themes](#running-themes)
- [Log](#log)

## Open Items

- [ ] Christine — compile all Figma/Zoom-chat inputs into unified RefTag taxonomy draft — target 2026-05-04 — source: hedy:m85ITBLjL9iJ4Nlxz2Nr
- [ ] ABMA/Data team — build source-of-truth tables as interim Feature Registry replacement — ongoing Q2 2026 — source: same
- [ ] Verification/R&O/AIT teams — review RefTag capture process (regex vs. full tag) for Feed-on-Street flows — follow-up TBD — source: same
- [ ] Richard + ABMA — define RefTag onboarding path for new campaigns — target 2026-05-11 — source: same

## Closed Items — Audit Trail

_None yet._

## Running Themes

- RefTag persistence through registration flow is a recurring paid-search attribution risk (flagged 2026-04-14 Baloo demo, 2026-04-27 workshop)
- MCS operates on a fixed, blocked-at-CMS pattern distinct from other channels — the taxonomy must accommodate this rather than enforce uniformity

## Log

### 2026-04-27 — Cross-functional RefTag taxonomy workshop

#### Source
hedy:m85ITBLjL9iJ4Nlxz2Nr (AB Marketing RefTag Taxonomy Workshop, 115 min)

Related: [topics/tests/baloo-shop-subdomain](../tests/baloo-shop-subdomain.md), [meetings/google-adobe-sync](../../meetings/google-adobe-sync.md)

#### What was said / what happened
Christine led a multi-team workshop to build a unified RefTag taxonomy replacing the soon-deprecated Feature Registry (Q2 2026 cutoff). Rationale: last QBR exposed the "Wack-a-Mole" problem of manual Ref Tag management per Transit + other channels. Long-term ambition is an MI-style registry with numerical routing through finance; short-term, ABMA will build source-of-truth data tables.

Inputs captured on Figma (then re-transcribed via Zoom chat + Richard transcribing for access-blocked users): channels (acquisition, engagement, onsite, offsite, email, push, field, pipeline), program types, campaign types, attributes (time-based, geographic, audience, technical).

**Key constraint:** 64-char RefTag limit. Forces priority: embed high-frequency attributes in the tag, join low-frequency attributes via data tables.

**Key edge cases raised:**
- **Pipeline (Emily):** whether LD campaigns should be a separate bucket or nested under acquisition/engagement. Consensus: nest.
- **Feed on the Street (Harsha):** verification, R&O, and AIT teams only parse regex patterns — not the full RefTag — during registration. This means the unique tag isn't persisted downstream to payment/AMO models. Paid-search attribution risk mirror.
- **MCS (Joanne):** MCS uses a fixed RefTag pattern for free traffic, blocked in the CMS if deviated. Other channels route via A.com logic so no cross-chan complexity. MCS is exception, not template.
- **MX partnerships (Anna):** GLEDA bank partnership sends email/WhatsApp; partner channels need to be added as a program type. Marketing retains tag-structure control despite partner-owned sends.
- **Product-led sends (Alex, Robert):** spend-analysis transactional email contains marketing content; detail-page promo widget clicks are triggered by marketing but shown via product channel. Ambiguous attribution boundary.
- **Geographic (Stacey):** Italy (IT) vs. InfoTech (INFTCH) prefix collision. Decision: use "IT" for Italy, "INFTCH" for InfoTech.

**Audience granularity decision:** SSR / CPS / admin vs. non-admin etc. should be stored in data tables and joined; only top-level audience bucket embedded in RefTag due to char limit.

**Ownership model:** goal is to minimize manual Ref Tag entry. ABMA provides the source-of-truth tables; marketers follow the standardized pattern. New campaign onboarding path TBD.

**Richard's role:** actively transcribed inputs from access-blocked Zoom participants into the Figma board (Clara, Harsha, Nourash). Didn't surface a major paid-search-specific issue beyond the existing F90 and Baloo ref-tag persistence concerns.

#### Decisions
- Christine — pipeline is not a separate bucket; nest under acquisition or engagement
- Christine — on-site + paid media as aggregate rollup channels for reporting
- Christine — "IT" for Italy, "INFTCH" for InfoTech (resolves historical data confusion)
- Christine — full RefTag capture required in Feed-on-Street registration flow (follow-up meeting with Verification/R&O/AIT required)

#### Actions
- Christine — compile unified RefTag taxonomy draft — by 2026-05-04
- ABMA/Data team — build source-of-truth tables — ongoing Q2
- Christine + Richard + ABMA — define new-campaign onboarding path — by 2026-05-11
- Christine — schedule follow-up with Verification/R&O/AIT on full-RefTag capture — no firm date

#### Notes
This is infrastructure-layer for attribution. If the Feature Registry → data-table transition happens cleanly, the ref-tag persistence gap Richard flagged on Baloo (hedy:6Zz78fIn7Qegis3Kk7xe) can be solved as part of this roll-up rather than as a one-off fix. Worth Richard staying close to this initiative through OP1 draft — one-page taxonomy cheat sheet and the cross-channel halo discussion for MX would benefit from alignment with the new tables.

---
