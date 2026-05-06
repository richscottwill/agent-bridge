---
title: "AU Paid Search Sync"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-05-06
---
<!-- DOC-0199 | duck_id: meeting-au-paid-search-sync -->

# AU Paid Search Sync

## Metadata
- Cadence: Weekly
- Attendees: Richard Williams, Alexis Eck (L6, Sydney), Lena Zak (L7, AU Country Leader, Sydney), Harsha Mudradi
- Hedy Topic: AU (ID: N6kHmgM0rOdDdah7iNNf)
- Hedy Sessions: 4
- Outlook Series: AB AU Paid Search Sync

## Context
Richard owns all AU paid search optimization and stakeholder communication. Lena is the hardest stakeholder to satisfy — she's data-demanding, expects numbers not narratives, and has escalated to leadership (challenged $6 avg CPC vs consumer benchmarks). Alexis is collaborative and a strong execution partner who defers to Lena on strategic direction. AU launched June 2025. No Shopping Ads available for AB. OCI has no confirmed AU timeline. Weekly CPA target ~$140.

Key dynamic: Richard must always have AU metrics loaded before any Lena interaction. Lead with data, be clear about timelines. Alexis is the day-to-day partner; Lena sets direction.

## Latest Session
### 2026-05-05 — AU Paid Search Handover to Megan / ABix (81 min) — FINAL HANDOVER
Source: hedy:j7nQYyfUFwwAbzM6LGZv

- Formal handover of AU Paid Search ownership from Richard → Megan (ABix), effective immediately. Attendees: Richard, Megan (ABix), Lena Zak (joined late), Brandon Munday, Yoon (late).
- Ownership framing: WW team retains platform permissions (Google Ads, Adobe) because Adobe can't be scoped to a single market. Megan takes on WBR/MBR/QBR, weekly Quip + change log, and R&O from the April R&O forward (~10 days out from handover).
- Data escalation protocol: Monday AM reg-data delays are common; open ABMA sim when data is stale. Worldwide syncs happen Monday morning US time — if global, WW team opens the sim; for AU-only delays, Megan must escalate.
- Reporting setup walked through: Excel sheet (daily → weekly/monthly auto-populate), GenBI for investigation, Hubble queries for accurate cost+registration stitching. Brandon's framing: "GenBI has all the correct data, but it's very difficult to get it to match up because the day that you pay for a click is not necessarily the day or week that it registers."
- Change log discipline emphasized: "we stress the importance of our change logs... this helps to pinpoint what change might have occurred that could have prompted the change in registration." Richard to paste historical entries into handover Quip.
- Budget / FX: AB Finance has finalized FX rate for the year; Megan to subscribe to AB-Marketing-Finance budget email ALS (separate from AB Marketing Access). Brandon confirmed USD OP2 numbers in the R&O file are final. Tax (10%) adds to platform-displayed spend when invoice lands.
- IECCP deferred 12+ months pending data-science roadmap; Brandon noted "even after it's set up, like Canada had IECCP in year four... we weren't even really utilizing it to pin down to like, efficiency at like 50%" — emerging markets take longer than one year.
- Adobe access: no market-scoped permissioning available. Richard to set up Adobe AdCloud reporting exports (weekly start cadence). Adobe Analytics access for page-level / bounce-rate data routes through Dwayne Palmer's team.
- RefTag structure: immutable. Megan can create new ref tags for new keywords but must follow the established structure (e.g., `PDSL-AU-BRAND_<keyword-id>-<ad-group>`). Shared negatives managed centrally.
- Bid strategy: reverted to Max Clicks from Adobe bidding (Adobe bidding test showed negligible impact). Richard confirmed moving forward no more @efrontier.com email appearing in change history.
- Ad copy and keyword-level tracking: AU tracks signups at keyword level via ref tags (not ad level) — Lena asked about using this for deeper cohort analysis; Richard confirmed post-registration personalization is not currently leveraged (that's a Baloo-era goal).
- Baloo rollout: US-only for 2026, PZRO end of August 2026, worldwide 2027+. Megan to be updated as development progresses.
- Site links: low CTR (~0.2%), primarily for ad real-estate visibility.
- Flash communications: Brandon noted ABix marketers (including Megan's team) may not be on the AB Paid Search Flash email distribution — Richard to paste the AB-Marketing-Access alias and verify Megan is added.
- FX rate: Lena confirmed AU finance had been using 0.62 but AB Finance's updated FX rate supersedes (QBR numbers need refresh as a result).
- Decisions: AU PS ownership formally transfers effective now; WW retains platform permissions; IECCP deferred 12+ months; bid strategy stays on Max Clicks.
- Action items:
  - Richard: set up Adobe AdCloud reporting exports (weekly start) — this week
  - Megan: take over R&O May forward (~10 days for April R&O)
  - Megan: submit ticket to Dwayne for Adobe Analytics access — near-term
  - Megan: subscribe to AB-Marketing-Finance budget email ALS — near-term
  - Richard: paste change log historical entries + RefTag structure example in handover Quip — post-call
  - Richard: confirm Megan is on AB Paid Search Flash distribution — post-call

## Previous Session
### 2026-04-28 — AU Paid Search Handover + Performance Review (32 min) — PRE-HANDOVER
Source: hedy:eQUxaMZO7Kiiv903HE2e

- Pre-handover biweekly with Richard, Brandon, Alexis Eck, Megan (incoming ABix owner), Lena. First intro for Megan before the 5/5 formal handoff.
- Brandon framed scope: "Next week is going to be the formal handoff... Richard's creating some documentation on what that looks like. He'll share that with you next week." Post-handoff: "Richard will not be managing actively, I would be completely led by your team. Like we are here for questions we have a sim intake as well."
- Performance: Richard reported AU down to ~$107 CPA (prior week was ~$155). Non-brand slower to recover than brand after budget adjustments.
- Polaris LP test post-mortem: Richard explained AU test was reverted after ~30% conv-rate decline immediately post-switch. After revert, reg volume recovered to flat vs pre-switch. Brandon: "this is a kind of one of those trade-offs between bias for action and insistence on the highest standard."
- Market maturity benchmarking: Brandon said AU brand CPA is "comparable to the other EU markets, especially like the smaller EU3 markets... same rate historically seen whenever we're launching Market. I mean, it can take like three years before we would call it mature."
- Automation limits: "a lot of the automation that we have, it's based on IAPRSTCCP, which is not available for Australia because it's not over a year old... in terms of our typical efficiency mechanisms and how we optimized for that, the tools that we use, we just can't with emerging markets."
- Megan asked about automation for OP1; Brandon: WW outbound handles global paid search; items live in OP2 2026 / MIRTEK / marketing intake.
- Decisions: Post-handoff AU PS management shifts fully to Megan/ABix; legacy AU LPs stay live until new Polaris-branded + conversion-optimized pages are A/B testable via Weblab; manual batch optimization continues until emerging-market automation is available.
- Action items:
  - Richard: grant Google Ads access to attendees post-call — today
  - Richard: include aggregated data views in handover doc — by next week
  - Richard: include Polaris LP test post-mortem in handover doc — by next week
  - Megan: lead AU paid search management starting next week

## Previous Session
### 2026-03-24 — AU Paid Search Performance and MCS Migration (34 min)
- Improved efficiency this week: lower spend but stable registration volume — positive ROI movement
- All non-selling keyword categories (perishables, alcohol) paused and added as negatives — contributing to CPA improvement
- MCS → Polaris migration completing today/tomorrow
- Two-campaign structure proposed: product-intent vs business-intent keywords. Alexis agreed — "I think this is a really good idea. It's a solid idea."
- Biweekly keyword review cadence agreed — Richard: "My intuition is every two weeks... over time there's going to be diminishing returns"
- Alexis offered to help with keyword-level analysis: "Don't hesitate to use me. I'm really happy to help you on that."
- Strategy question raised: should targeting focus on product intent (what businesses buy) or business intent (search terms implying business ownership like "business cards")? Current structure mixes both — separation would improve bid strategy optimization.
- Alexis: "I'm not sure if it's the expectation for us in the country to define it or for you guys within the central team to provide it to us." — Richard acknowledged it's both, with product-intent as the near-term focus and business-intent as future expansion.
- Tracking concern: new MCS pages with multiple navigation points could dilute registration conversion. Current MCS-driven registrations are low (1-2/week) — easy to detect changes post-migration.
- Ref tag tracking should persist unless overridden. Main risk is user drift from increased navigation options.
- MCS page replication from MX model discussed — Alexis: "We would be eager to try and replicate the Mexico custom pages." Richard: needs strategic justification (e.g., paper product test) to prioritize with MCS team. Global urgency > market-specific asks.
- Alexis: "If you're having this conversation with the MCS team and you need support from us to prioritize, feel free to include us in the loop."
- Decisions: Two-campaign structure pilot approved. Biweekly keyword review cadence. Rolling 4-week CPA view for trend analysis. MCS migration proceeds with close monitoring.
- Action items:
  - Richard: compile rolling 4-week keyword CPA dashboard (due ~4/2)
  - Richard: verify tracking integrity on new Polaris LP pages with MCS team
  - Richard: finalize negative keyword list for non-selling categories
  - Richard: establish biweekly keyword review cadence

## Running Themes
- AU CPC defense: B2B inherently higher than consumer; building data narrative for Lena
- Polaris migration: full switch confirmed, tracking integrity validation in progress
- Keyword optimization: surgical approach (outlier analysis) over broad cuts
- Two-campaign structure: product-intent vs business-intent — pilot approved
- OCI timeline: no confirmed AU date — will help with bidding and attribution when launched
- Lena's 3 priorities: keyword CPC/CPA investigation, keyword-to-product mapping, Polaris migration
- MCS page replication: MX model as template, needs global urgency justification
- Alexis as collaborative partner: "don't hesitate to use me"

## Open Items
- [ ] Rolling 4-week keyword CPA dashboard (due ~4/2)
- [ ] Verify tracking integrity on Polaris LP pages post-migration
- [ ] Finalize negative keyword list (alcohol, perishables, etc.)
- [ ] Pilot business-intent vs product-intent campaign structure
- [ ] Assess feasibility of replicating MX custom MCS pages for AU (needs strategic justification)
- [ ] Coordinate with MCS team on tracking/attribution post-migration
- [ ] Establish biweekly keyword review cadence


## Previous Session
### 2026-03-24 — AU Paid Search Performance & MCS Migration (34 min)
Source: hedy:11P8Yl6nS9cou3yMnAFY

- Alexis Eck weekly sync. AU showing improved efficiency week: lower spend, stable reg volume, across both brand + non-brand.
- Keyword optimization: paused + negatived perishables/alcohol. Richard to compile 4-week rolling CPA dashboard in Excel.
- Strategy debate: product-intent vs business-intent targeting (e.g. "business cards" = business-intent). Agreement to pilot 2-campaign split with separate budgets + KPIs.
- MCS migration proceeding, but tracking risk flagged: multiple redirection points on new Polaris pages could dilute registration conversion. RETCA tracking should persist via ref tags unless overridden.
- MX-style custom MCS pages: Alexis wants to replicate for AU. Richard's advice: MCS team prioritizes worldwide, not market-specific — justify via strategic initiative (Sydney paper test, brand pages) not OP1.
- Alexis: "it's a two-way door as well" — comfortable proceeding with MCS migration + monitoring closely.

## Previous Session
### 2025-11-24 — AU Handoff Deep-Dive: Budget Process + Melissa Relationship + Backfill + Data Feeds (45 min)
Source: hedy:b8A72gLr82FE4mj0Z7vV

- Yun-Kang deep-handoff to Richard as Richard assumes AU lead post-leave. Adi previously covering.
- **AU budget**: Nov net $171K USD (includes 10% VAT buffer); Dec dropped to $65K net due to earlier-year over-spend needing recovery. Melissa pre-warned about Dec pull-back performance impact.
- **Invoice process**: AU central finance requires monthly invoice download from MCC + email to specific finance alias within 2 business days of month start. Yun covers Nov; Richard onward — calendar reminder essential.
- **AU stakeholder framing (Nina context)**: Nina (AU country leader) previously ran retail paid search, now leads AB paid. Yun-Kang flagged (quoted): "she was like, 'Okay, maybe we can be the exception' [on OCI expansion timeline], but we have a close relationship with retail." Retail-era expectation mismatch drives her friction with central marketing.
- **Brand lift expectations — explicit push-back**: Melissa expects ~10% brand lift from Paid Media launch (per Kate positioning). Yun-Kang's directive (quoted): "for our experience in all the markets, there's no huge brand lift. You cannot assume, 'Oh, I will see 10% lift.'" Richard not to commit to lift numbers. UK analysis (no lift seen) cited as proof.
- **Landing-page test post-mortem (Oct)**: Nina-requested business-savings landing page test for existing-customer targeting. User experience was broken: sign-in button tiny, create-account text tiny, tracking non-functional. Shut down after 2 weeks. Caused huge non-brand reg drop visible in Oct weekly callouts.
- **Bidding strategy**: Max Clicks holds through year-end to establish baseline. AMO CPA testing deferred to Jan/Feb; daily-spend-target AMO likely similar or worse than Max Clicks per Yun-Kang's read.
- **Registration backfill investigation** (W33+ stuck-in-bracket pattern): ABMA investigating, backfill may not have run yet. Richard to monitor dashboard week-over-week.
- **AU data feed mechanics**: Refresh2 feed has all since-launch data (use for full history). EFID1 feed just added AU last month, actively monitored by ABMA. Numbers match across both within ~1%. Yun-Kang's rule: use Refresh2 for historical; EFID1 for current-month monitoring. Don't change anything on existing setup.
- **Melissa communication pattern**: highly engaged, active in weekly Quip + Slack. Richard should reply same-day when possible; morning-of-next-day acceptable for non-urgent. Melissa pulled in from retail — high expectations on responsiveness.
- **Site link cleanup** (Richard's side): pulled all AU + worldwide site link URLs. Some invoice-related pages (business.amazon.com/TVA, Fattura, etc.) need CP-version confirmation. Richard to email Alex for CP-equivalent pages.
- **Handoff timing**: Richard owns AU weekly callout starting next week (first run due by Mon 5pm PT to give Melissa WBR-ready context by her Wed local time). Team OneNote approach: Richard drafts + Yun can review.
- Decisions: Max Clicks baseline held to year-end. Refresh2/EFID1 dual-feed setup preserved. Richard owns AU callout + budget + invoicing from next week.
- Action items:
  - Richard: email Alex for CP-equivalent invoice landing pages (TVA, Fattura, UK Prime Business tool, IT/FR equivalents) — today
  - Richard: first AU callout next Mon by 5pm PT
  - Richard: monthly invoice process starting Dec 2 (AU central finance email)
  - Richard: compare W-over-W dashboard for backfill evidence; flag to ABMA if no movement
  - Yun: add Richard to Melissa 3-week recurring call + intro next Monday
  - Yun: handle Nov invoice as final step before full handoff

Source: hedy:sUfWyLSkhOM30LykIHPI

- First AU sync with Lena Zak as the direct PS stakeholder after Melissa's departure. Data delayed from tech team — performance discussion went strategic instead.
- Lena's ask (quoted): "what I would really really love is a table that tells me our total clicks across brand and everything. And then total sign ups and the CPA that we had that week and the running CPA for the month and for the quarter and for the year today." Rationale: she manages a multi-channel budget and needs CPA comparable across channels.
- Lena framed the core decision question: "what I'm going to do is optimize for where I'm going to get the most efficient acquisition."
- Richard's cohort framing (quoted): AU comparable to MX/CA but "they're definitely very different case studies." Canada brand CPC up ~18% YoY consistently. MX had to cut spend 2nd half of year to hit ICCP — was essentially flat Year 1 vs Year 2.
- Lena pushed against ICCP as near-term optimization target (quoted): "I would sort of worry less about the eye of the sense ACP because we don't have that right now. We're not optimizing to that."
- Lena's strategic asks:
  - (1) A year-long plan of testing + CPA optimization initiatives, including QBR-ready output.
  - (2) Calendar integration with AU market events (end of fiscal year May-June, summer-to-work-back transition).
  - (3) Vertical targeting on "tradies" (tradespeople) — largest individual employment sector in AU with good on-site selection match.
  - (4) Sydney paper product test — Lena quoted the cultural nuance: "our paper is priced so high that they prefer to go in store to buy paper at a more competitive price than buy it on Amazon." Wants localized Sydney-specific campaign with competitive paper ASIN.
  - (5) Business Essentials ASIN list integration — Lena's selection PM building a curated list, wants paid search to drive traffic to a new business-essentials landing page.
  - (6) Quarterly Google review — wants AB's central Google team to run quarterly AU B2B insights the way the local Google Australia team did last year.
  - (7) Keyword/search-term insights shared upstream (quoted): "to use that to then change the way that we message more broadly."
- Lena pushed back on Richard's ASIN-driven vertical identification (quoted): "because we're so new and we have such strange shopping patterns right now... one order will come in, it'll blow all of our data out of proportion. You're going to struggle to really identify the key sort of essence just based on what's actually happening." Her preferred alternative: follow the Business Essentials PM's curated list rather than mining ASIN data for verticals.
- Ewan (Alexis's support) proposed splitting traffic within Google ads for paper test + developing a dedicated paper landing page with AU team.
- Lena explored whether PS team should be added to AU MBRs for better context visibility — defer decision to let team think about timezone tradeoffs.
- Decisions: Standardized performance table (week / month / quarter / year CPA) to become the recurring format. Quarterly AB Google review to be scheduled. Sydney paper test approved for scoping.
- Action items:
  - Richard: develop weekly performance table with brand/non-brand split, clicks, signups, CPA across week/month/quarter/year
  - Richard: scope Sydney paper test (keyword volume, ad copy, landing page coordination with AU team)
  - Richard: set up quarterly AU strategy review with Google AB team
  - Lena/Alexis: introduce Richard to Amy (selection PM) for AU Business Essentials ASIN list integration
  - Lena: kick off email thread for Sydney paper product test scoping

