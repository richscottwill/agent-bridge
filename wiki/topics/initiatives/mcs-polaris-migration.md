---
title: "MCS Polaris Migration — Paid Search Landing Pages"
type: initiative
status: ACTIVE
owner: Richard Williams
created: 2026-05-06
updated: 2026-05-06
hedy_topic_id: "idSAffMcAegZh6MhQNyA"
aliases:
  - "mcs"
  - "mcs-polaris"
  - "mcs-template"
  - "polaris-template-migration"
  - "mcs-coordination-ownership"
related:
  topics:
    - topics/tests/polaris-brand-lp
    - topics/markets/mx
    - topics/markets/ca
  meetings:
    - meetings/mcs-polaris-rollout
    - meetings/brandon-sync
  state_files: []
  wiki_articles: []
  protocols:
    - topics/INGEST-PROTOCOL
---
<!-- DOC-TOPIC-INITIATIVE-MCS-POLARIS -->

# MCS Polaris Migration — Paid Search Landing Pages

## Summary

Global initiative to migrate legacy paid-search landing pages (non-public, non-crawlable PADESARJAD pages) to the Polaris-branded template for brand consistency across the site. Per 2026-04-15 Canada/Polaris cross-team review (hedy:rg3S3JC10W7SuXHOyliE), Canada delivered a ~15% mobile conversion rate uplift with targeted optimizations (localized headlines, image refresh, subheadline, hamburger-menu removal). Mobile was 80–81% of non-branded traffic, so the impact was material. MX is leading the Polaris test on beauty + auto category pages (started by Carlos, now owned by Richard); results expected within ~2 weeks of 2026-04-15. Global Polaris brand-page template was targeted for team sign-off 2026-04-16, MCS implementation ~1 week after. Legacy paid-search pages are intentionally non-indexable to avoid SEO cannibalization — this posture survives the migration. Project Baloo delay (US-only, pushed 10–12 months to end of Aug 2026) freed Polaris migration to move forward.

## Links

- **Related topics**: [`topics/tests/polaris-brand-lp`](../tests/polaris-brand-lp.md), [`topics/markets/mx`](../markets/mx.md), [`topics/markets/ca`](../markets/ca.md)
- **Meeting series**: [`meetings/mcs-polaris-rollout.md`](../../meetings/mcs-polaris-rollout.md), [`meetings/brandon-sync.md`](../../meetings/brandon-sync.md)
- **Canada SSR/VR**: referenced as source of Canada optimization learnings
- **MCS lead**: Alex (Tech team)
- **PA team drivers**: Adi Thakur (Canada), Richard Williams (MX)

## Stakeholders

| Role | Name | Most recent sourced interaction |
|---|---|---|
| PS owner | Richard Williams | 2026-04-15 Canada/Polaris review (hedy:rg3S3JC10W7SuXHOyliE) |
| Manager | Brandon Munday | 2026-04-15 Canada/Polaris review (same) |
| Canada PA lead | Adi Thakur | 2026-04-15 Canada/Polaris review (same, presenter) |
| MX PS owner | Lorena Alvarez Larrea | 2026-04-15 Canada/Polaris review (same) |
| MCS tech | Alex | referenced per 2026-04-15 entry |
| MCS PM | Dwayne Palmer | 2026-04-15 Canada/Polaris review (same) |

## Simplified Timeline

#### 2026-W16 (Apr 13 – Apr 19)
- 2026-04-15 — Canada/Polaris cross-team review; Mexico confirmed as first Polaris test market; global brand template finalized next day (4/16)

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

- [ ] Richard — share MX Polaris test results (beauty + auto) once data matures — due: ~2 weeks from 2026-04-15 — source: hedy:rg3S3JC10W7SuXHOyliE
- [ ] MCS team (Alex) — finalize global Polaris brand template — due: 2026-04-16 — source: hedy:rg3S3JC10W7SuXHOyliE
- [ ] Richard + Lorena — align on paid social → paid search halo analysis in MX — source: hedy:rg3S3JC10W7SuXHOyliE
- [ ] Lorena — reach out to Vijay Kumar (Andes) on Baloo intl timeline — source: hedy:rg3S3JC10W7SuXHOyliE
- [ ] Dwayne Palmer — coordinate MCS + PA teams on Polaris migration rollout plan — source: hedy:rg3S3JC10W7SuXHOyliE

## Closed Items — Audit Trail

_None yet._

## Running Themes

_Pattern detection requires 3+ entries. Not enough signal yet._

## Log

### 2026-04-22 — Legacy template change constraints + URL flip follow-up

#### Source
hedy:dgVB26RMt6eMqak5WuHR (MCS Polaris Template Migration Update, 12 min)

Related: [topics/markets/mx](../markets/mx.md)

#### What was said / what happened
Quick working session with Dwayne Palmer walking through Richard's MCS ticket for changes on a legacy non-Polaris template (MX pages from the 4/15 workshop). Dwayne's explicit constraint: "we don't use this template anymore or you're not having any kind of support for this nonpolaris components... we won't be able to fix on this" — meaning padding/spacing/layout changes cannot be made on legacy templates. What CAN still be done: content edits (text, images, colors, section removal via content deletion, adding icons). Icons require Richard to specify which ones (naming them or screenshotting + annotating) — MCS team will replicate but won't pick content. Header image + multiple broken images in the mobile flow reported; Dwayne will investigate.

#### Decisions
- Dwayne Palmer — no layout changes on non-Polaris templates; all structural work moves to Polaris migration
- Richard — remove padding/layout requests from the ticket; replace with content + icon specs

#### Actions
- Richard — update MCS ticket with specific icon requirements (names or annotated screenshots) — due Apr 24, 2026
- Richard — remove padding and layout change requests from the ticket — completed
- Dwayne Palmer — add ticket comment documenting legacy template limitations — due Apr 24, 2026
- Dwayne Palmer — investigate and resolve broken image issues on mobile CP pages — due Apr 25, 2026

#### Notes
Reinforces the 2026-04-15 decision that iteration energy should flow to Polaris pages, not legacy. This is a clean example of what "we won't invest in the old template" looks like operationally — you can get content changes through but not structure.

---

### 2026-04-15 — Canada/Polaris cross-team review; MX confirmed as first Polaris test market

#### Source
hedy:rg3S3JC10W7SuXHOyliE (Polaris Brand LP and Canada Optimization Review)

Related: [topics/tests/polaris-brand-lp](../tests/polaris-brand-lp.md), [topics/markets/mx](../markets/mx.md), [meetings/brandon-sync](../../meetings/brandon-sync.md)

#### What was said / what happened
Adi Thakur walked the Canada team through mobile LP optimization results: ~15% mobile conversion rate improvement, with mobile traffic at 80–81% of non-branded traffic. Changes: localized Canadian headline, mobile hero image refresh, added subheadline, removed hamburger menu, repositioned layout elements. Tested in phases (2 pages changed + 3 control, then expanded). Learnings already applied across AU, MX, and EU5.

Brandon clarified why paid-search landing pages look different from MCS/Polaris public pages: "these pages are not crawlable and not part of the public site. There's no way for you to navigate to these pages unless you click on the PADESARJAD. And the reason for that is because these are very much optimized for registration, not for information... we didn't want to compete with the public page... for that space on Google because the SEO optimized public pages are going to be a lot more valuable and get indexed much better." Non-indexability stays after migration.

Brandon on Baloo impact: "Baloo has been pushed out. We don't even have a global date for that anymore. The US state has been pushed out by 12, 10, 12 months. So that's why at this point, we're moving forward with optimization of these pages and adoption Polaris." — i.e., the Baloo delay unblocks the Polaris migration.

Brandon on ownership: "Richard is kind of first in line to do with Mexico that he already has some Polaris Branded Test happening... we need to be really intentional when we switch over that the new pages that we use also highlight call to that signal to action."

Lorena raised the **paid social → branded search halo effect** in MX: "the CTR increased on branded, on branded search by a lot when we turn on again the paid social campaign." Hard attribution not possible due to ref tag loss through VAC/AVM, but directional. Brandon: "we've never seen that before so that'll be really interesting" — Mexico's smaller volume may make halo more visible than US.

Lorena on Baloo MX inclusion asked: Brandon confirmed "all of the development across 2026 is all US focused... I haven't seen any international timeline." Told Lorena to reach out to Vijay Kumar (Andes) for future updates. Lorena's angle: "use Mexico as a playground before the U.S. Just because it minimizes the risk."

Lorena asked about process for MX-side changes: Brandon: "this goes through the MCS team. So, Adi, I think that you had submitted a SIM and then worked with the MCS team in particular, it was Alex." Richard already opened an MCS ticket emulating Canada's changes on the older MX template, but the long-term iteration should be on Polaris pages.

#### Decisions
- Brandon — paid search pages migrate to Polaris globally; legacy PADESARJAD pages deprecated
- Brandon — MX serves as the first Polaris test market; its results inform the global rollout
- Brandon — Canada's optimization playbook (localized headline, image refresh, subheadline, remove hamburger menu) is the reference pattern for all markets
- Acknowledged — paid social → branded search halo in MX monitored directionally despite attribution gap

#### Actions
- Richard — share MX Polaris test results (beauty + auto) when data matures — due ~2 weeks
- MCS team (Alex) — finalize global Polaris brand template — due Apr 16
- Richard — submit MCS tickets for any additional MX optimizations leveraging Canada learnings — ongoing
- Lorena + Richard — connect on paid social × paid search halo — soon
- Lorena — reach out to Vijay Kumar (Andes) re: Baloo intl — no due date
- Dwayne Palmer — coordinate MCS + PA rollout plan — by 2026-04-23

#### Notes
Direct cite of the Canada uplift: "around 15% improvement in mobile conversion rates" — Adi Thakur. Brandon on Canada → other markets: "the learnings that we had for the Canadian market, we already tried implementing those and successfully implemented them in a lot of the markets across the AP Australia, Mexico and other European nations as well."

Strategic connection: this feeds directly into [polaris-brand-lp.md](../tests/polaris-brand-lp.md) — Brandon is sequencing MX → WW on Polaris brand template, with MX test on beauty + auto as the first leading indicator.

---


### 2026-03-24 — Polaris Brand LP rollout + Weblab dial-up planning

#### Source
hedy:maKRIlUS6RdghDtTwAis (Polaris Brand LP Rollout and Weblab Planning, 30 min) + hedy:4veBOAWYumVzlJciaLVg (AU CPC + Polaris sync, 34 min)

Related: [topics/tests/polaris-brand-lp](../tests/polaris-brand-lp.md), [topics/markets/au](../markets/au.md)

#### What was said / what happened
Dwayne confirmed status: EU5 + non-EU (ex-Japan) pages all validated and ready. JP pending translation (ETA 3/26); JP legacy had an intake form (unique among markets) — team decision: **launch without form**, test, add back if data requires.

Header implementation is via Adobe Target as a temporary workaround — hiding AEM's default big header behind a minimal one. Permanent fix requires Alex to build a new AEM template + experience fragment dedicated to paid-search pages. Timeline: end of week or early next.

Personalization component on CP pages (beauty, auto) contains async CTAs + ASINs tech-owned. Richard needed to test logged-in vs. logged-out experience.

**Weblab dial-up target: 2026-04-06 or 04-07**, pending all pages finalized by 3/26 + header fix shipped. Dwayne owns Weblab config.

AU side (hedy:4veBOAWYumVzlJciaLVg): Richard to migrate MCC→Polaris on 3/24. Brandon's push: testing plan needs go-live dates (Lena wants timeline visibility).

#### Decisions
- JP launches without form (measurable-test approach)
- Adobe Target header is temporary; dedicated AEM template is the permanent path
- Weblab dial-up targeted 2026-04-06/07
- Richard owns logged-in-vs-logged-out personalization testing

#### Actions
- Alex — build AEM template + experience fragment for paid-search pages — EOW
- Richard — test personalization component for logged-out experience — by 3/28
- Dwayne — finalize Weblab configuration — by 4/5
- Stacey — verify JP page post-translation — by 3/27

