---
title: "Baloo — shop.business.amazon.com subdomain"
type: test
status: ACTIVE
owner: Richard Williams
created: 2026-05-06
updated: 2026-05-06
hedy_topic_id: "n7WMdRSB3fXXzuP3cCXJ"
aliases:
  - "baloo"
  - "baloo-phase1"
  - "baloo-deep-dive"
  - "shop.business.amazon.com"
  - "ungated AB"
related:
  topics:
    - topics/tests/polaris-brand-lp
    - topics/markets/us
  meetings:
    - meetings/brandon-sync
  state_files: []
  wiki_articles: []
  protocols:
    - topics/INGEST-PROTOCOL
---
<!-- DOC-TOPIC-TEST-BALOO -->

# Baloo — shop.business.amazon.com subdomain

## Summary

Baloo is a new ungated experience on the shop.business.amazon.com subdomain enabling AB product browsing without authentication. Primary launch channel is Paid Search. Per 2026-04-14 Brandon 1:1 (hedy:DlrGpwhm2LhxFvDpC8Rr), Brandon asked Richard to lead the following Thursday's deep dive as a group bug-finding session — "it's important for everybody to know what it is because their country level stakeholders are whatever are definitely going to ask." Per 2026-04-14 Baloo Phase 1 demo (hedy:6Zz78fIn7Qegis3Kk7xe), two material risks to Paid Search were surfaced: URL flip (subdomain context lost when clicking internal links redirecting to amazon.com) and ref tag persistence failure during registration — Richard opened a ticket with screenshots. Per 2026-04-15 Canada/Polaris review (hedy:rg3S3JC10W7SuXHOyliE), Baloo international rollout is US-only for 2026; US PZRO pushed to end of August 2026 (10–12 month delay from original). No confirmed MX or intl timeline as of 2026-04-15.

## Links

- **Related topics**: [`topics/tests/polaris-brand-lp`](polaris-brand-lp.md), [`topics/markets/us`](../markets/us.md)
- **Meeting series**: [`meetings/brandon-sync.md`](../../meetings/brandon-sync.md)
- **Key contact**: Vijay Kumar (Andes) — Baloo tech lead
- **Marketing GTL**: Mauro (Baloo GTL)
- **Ticket (ref tag persistence)**: filed 2026-04-14 by Richard (details in session)

## Stakeholders

| Role | Name | Most recent sourced interaction |
|---|---|---|
| PS owner | Richard Williams | 2026-04-14 Baloo demo (hedy:6Zz78fIn7Qegis3Kk7xe) |
| Baloo tech lead | Vijay Kumar | 2026-04-14 Baloo demo (same) |
| Baloo GTL | Mauro | 2026-04-14 Baloo demo — "Mauro is driving the Baloo GTL" |
| Manager | Brandon Munday | 2026-04-14 Brandon 1:1 (hedy:DlrGpwhm2LhxFvDpC8Rr) |
| Attendees | Arushi, Shardul, Christian, Justin, Jayne Linerishy, Alexis Eck (AU) | 2026-04-14 Baloo demo |

## Simplified Timeline

#### 2026-W16 (Apr 13 – Apr 19)
- 2026-04-14 — Brandon 1:1: Brandon asks Richard to lead Thursday deep dive
- 2026-04-14 — Baloo Phase 1 demo; Richard flags ref tag persistence issue
- 2026-04-15 — Canada/Polaris cross-team review confirms Baloo is US-only for 2026; US PZRO slipped 10-12 months

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

- [ ] VJ (Vijay Kumar) to review Richard's ref tag persistence ticket and determine if backend tracking can validate attribution loss — due: Apr 16, 2026 — source: hedy:6Zz78fIn7Qegis3Kk7xe
- [ ] Marketing to use relative URLs in all new Baloo content (ongoing) — source: hedy:6Zz78fIn7Qegis3Kk7xe
- [ ] Richard to test Baloo experience via Tampermonkey script + document findings — source: hedy:6Zz78fIn7Qegis3Kk7xe
- [ ] Lorena Alvarez to reach out to Vijay Kumar (Andes) to ask about Baloo MX/international timeline — source: hedy:rg3S3JC10W7SuXHOyliE

## Closed Items — Audit Trail

_None yet._

## Running Themes

_Pattern detection requires 3+ entries. Not enough signal yet._

## Log

### 2025-11-25 — Brandon Belu UX critique: registration gets hidden 3-4 steps deep

#### Source
hedy:wM8BPUFWxU8BBqdfBNbe

Related: [meetings/brandon-sync.md](../../meetings/brandon-sync.md)

#### What was said / what happened
Working session on two threads — Baloo ("Belu") URL categorization for June rollout + current promo test post-mortem. On **Baloo UX**, Brandon shared the research doc and critiqued the user journey (quoted): "I really don't believe that it's going to be successful. With its current iteration." Core problem: the proposed flow hides the register-CTA until users see a product, add to cart, proceed to checkout — "they're going to hide that until the user like sees the product and then adds it to their car and then proceeds to check out. And then it's like, oh, surprise, you did all of this thing over the last half hour. Now you're going to have to spend half an hour registering."

Brandon also surfaced the price-shift problem (quoted): "we already have issues with our pricing because our like this example where it goes from $53 to $63... whenever you check out, it's actually like moved into your consumer side cart and they're like wait what." Users confused about which cart they're checking out from.

Richard reframed the opportunity (quoted): "the thing that seemed like the highest benefit was... we could sort of shape the CX for AB people we knew that were AB instead of like just inserting them here like this." i.e. — recognized AB customers go direct to AB shopping experience; unknown/unverified customers get the Baloo ungated experience.

Brandon agreed on the reframe: if the UX doesn't drive new registrations, the better fit is post-registration dumping into the Baloo ungated shopping experience for unverified customers who want to start building cart immediately.

Research doc weaknesses flagged: only 6 respondents (2 of 3 US respondents were over 70), "general avoidance of paid search ads" insight contradicted by Richard's actuals data.

#### Decisions
- Brandon's read: current Baloo design unlikely to drive registration lift without a persistent-register-CTA banner
- Better use case is post-registration for unverified customers (Richard's reframe)

#### Actions
- Brandon: re-raise persistent register-CTA banner with Baloo team (already raised previously)
- Richard: categorize brand vs non-brand URLs for Baloo rollout testing (deferred to Adi; deadline end of day 4th)

#### Notes
This session pre-dates the 4/14 Phase 1 demo where Richard flagged the ref-tag persistence issue. The UX critique captured here is Brandon's independent read before the formal demo — consistent with Richard's later flagging that internal navigation can overwrite ref tags on the Baloo subdomain.

---

### 2026-04-02 — Baloo early access cost discussion

#### Source
hedy:mUHxP0XagLnHhnBFjf4D (Baloo Early Access and Cost Impact Review, 18 min)

Related: [topics/initiatives/op1-2026](../initiatives/op1-2026.md)

#### What was said / what happened
Stacey Gu walked Richard through the Baloo early access plan: 50 stakeholders installing the Tampermonkey script to enable shop.business.amazon.com + all Weblabs, testing hands-on. Paid search is the primary launch channel. Brandon flagged at MBR that internal Google-search clicks would inflate ad costs. Richard provided the cost basis: **$4.43 average CPC for non-brand**, range $2-$9. 5-10 clicks per week per stakeholder × 50 = meaningful spend burn. Decision: restrict stakeholders to direct-link access (shop.business.amazon.com) for routine testing; only 5-6 Google-search clicks permitted, reserved for leadership demos. Richard to supply the cost data as a warning note in the enablement comms.

#### Decisions
- Stacey — early access limited to 50 stakeholders via Tampermonkey script
- Google-search testing restricted to 5-6 leadership demo clicks; everyone else uses direct link

#### Actions
- Richard — supply CPC cost data + keyword list for early-access warning comms — by 2026-03-30
- Stacey — launch early access EOD Monday 2026-03-30, tag Richard in internal Baloo SIM

---

### 2026-04-15 — Baloo international rollout confirmed as US-only for 2026

#### Source
hedy:rg3S3JC10W7SuXHOyliE (Polaris Brand LP and Canada Optimization Review)

Related: [topics/tests/polaris-brand-lp](polaris-brand-lp.md), [topics/markets/mx](../markets/mx.md)

#### What was said / what happened
Lorena asked who could confirm Mexico is included in the Baloo rollout strategy. Brandon's direct answer: "all of the development across 2026 is all US focused. Like I said, Baloo got pushed out like 10, 12 months. It was supposed to be launched last year and now it's not going to be till end of August for the PZRO. And then they're going to open it up to other channels in the US within this year as well. So I haven't seen any international timeline." Brandon committed to sharing Vijay Kumar's (Andes) alias for Lorena to ping directly. Lorena said she'd pitched using Mexico as a playground before US because "it minimizes the risk and basically you can learn a lot of things."

#### Decisions
- Brandon — Baloo remains US-only for 2026; Mexico/intl are not on the current roadmap

#### Actions
- Lorena — reach out to Vijay Kumar (Andes) re: Baloo intl timeline — no firm due date

---

### 2026-04-14 — Baloo Phase 1 demo; ref tag persistence issue surfaced

#### Source
hedy:6Zz78fIn7Qegis3Kk7xe (Baloo Project Phase 1 Demo and Feedback)

Related: [meetings/brandon-sync](../../meetings/brandon-sync.md), [topics/tests/polaris-brand-lp](polaris-brand-lp.md)

#### What was said / what happened
Vijay Kumar walked through Phase 1 of Baloo (shop.business.amazon.com subdomain): AB nav un-gated for unauthenticated users, onboarding business page for unauthenticated customers (static widgets, full campaigns launching end of April), cart-to-auth flow, new AP/Auth page. Unauthenticated users can see marketing content + business pricing (gated by merchant opt-in guardrail — if merchant opts out, B2C pricing shows instead). Gated features (e.g., business analytics requiring CID) prompt sign-in.

Major technical risk identified: **URL flip**. VJ/Vijay explained customers clicking internal links (Business Essentials, Tech Supply) get redirected from shop.business.amazon.com to amazon.com, losing Baloo subdomain context. Root causes: absolute URLs + short URLs in marketing content. Mitigation: marketing must use relative URLs going forward.

Richard raised a second critical issue: **ref tag persistence**. Quote: "I noticed that our Ref Tags were getting overwritten as you go through to the registration. I didn't see it as like the original Ref Tag or the Ref Tag that was like within the URL string when you're going into the red start... If someone's clicking around away from the product page, then they're probably going to get overwritten. And so attribution would just not [work]." Richard submitted a ticket with screenshots. Vijay committed VJ would review.

#### Decisions
- Vijay Kumar — Baloo campaigns use dedicated widget group separate from CID-personalized AB campaigns
- Vijay Kumar — relative URLs mandatory for all new Baloo content
- Vijay Kumar — ref tag persistence is P0; requires immediate investigation

#### Actions
- VJ — review Richard's ref tag ticket, determine if backend tracking validates data loss — due Apr 16, 2026
- Marketing — use relative URLs in all new Baloo content — ongoing
- Vijay Kumar — document URL flip scenarios — due Apr 16, 2026
- Mauro — finalize Baloo GTL roadmap — due Apr 20, 2026
- All stakeholders — submit Baloo feedback via ticketing — due Apr 18, 2026
- Richard — test Baloo experience via Tampermonkey script, document findings — ongoing

#### Notes
Richard's ref tag observation ties directly to Brandon's MBR concern about paid-search attribution integrity. Loss of ref tags during registration would distort ROI reporting for any Baloo-bound paid search traffic. This is the first concrete attribution risk flagged on Baloo. Worth tracking in the state file if/when MX or other markets come online.

---
