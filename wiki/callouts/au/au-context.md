---
title: "AU Paid Search — Market Context"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0009 | duck_id: callout-au-context -->

# AU Paid Search — Market Context

Last updated: 2026-03-16

## Market Overview
- Launched: June 2025 (W24, 6/10/25)
- FY26 OP2 budget: $1.8M USD (net/media), $2.0M gross
- FY26 OP2 registrations: 12,906
- FY26 CPA target: $140
- No YoY comparisons available yet (market too new)
- FY25 total: $1.14M spend, 8,763 regs, $158 CPA (June–Dec only)
- Current objective: maximize registrations while improving CPA. No ie%CCP target yet — CCP data expected July 2026, at which point an ie%CCP target will likely be introduced. Until then, CPA efficiency is the primary constraint.

## 2026 Monthly Budget (Net USD / Regs / CPA)
| Month | Net USD  | Regs  | CPA  |
| ----- | -------- | ----- | ---- |
| Jan   | $142,845 | 1,140 | $125 |
| Feb   | $147,592 | 1,110 | $133 |
| Mar   | $147,592 | 1,082 | $136 |
| Apr   | $147,592 | 1,071 | $138 |
| May   | $147,592 | 1,189 | $124 |
| Jun   | $147,592 | 1,219 | $121 |
| Jul   | $172,614 | 1,105 | $156 |
| Aug   | $186,488 | 1,062 | $176 |
| Sep   | $147,592 | 1,071 | $138 |
| Oct   | $147,592 | 1,083 | $136 |
| Nov   | $147,592 | 1,006 | $147 |
| Dec   | $119,244 | 768   | $155 |

Adjusted budget rebalanced to flat $140 CPA across months.

## Active Testing (2026)
- Phase 1: Adobe bid strategies (in progress, Q1 target). Expecting 5-15% CPA improvement.
- Phase 2: Additional Adobe signals (Registration Start page visits). Q3 start.
- Landing page optimization: Brand LP testing after bid strategies stabilize. MCS brand page template showed 38bps improvement in US.
- Event support: MCS page banners during local events.
- Image extensions: Implemented Aug 2025, need localized AU images.
- Negative keyword cleanup: Ongoing. Perishables/alcohol paused.
- Account structure improvements: Limiting search query paths for bid strategy effectiveness.
- Demand Gen campaigns: Planned, leveraging US learnings ($0.29 CPC vs $2.97 keyword).

## Key Narrative Threads
- Back to Biz to Evergreen promo transition causing registration softness (W8-W11)
- Bid strategy transition from Google click-based to Adobe conversion-based (started W3)
- NB bid strategies showing efficiency gains: CPC down 15% from W7 to W10
- Brand traffic volatile due to holidays, events, and market maturity
- New acquisition promo live: "20% off first order, up to AU$50" — monitoring W12+ impact
- Landing page test pending: MCS vs Polaris (50/50 split or full switch, awaiting Lena confirmation)
- AU/MX OCI planned for May 2026

## Key People
- Alexis Eck: AU market POC, owns MCS page mapping
- Lena Zak: AU stakeholder, pushes for MCS migration and performance data
- Harsha Mudradi: AU sync attendee
- Melissa O'Leary: Budget coordination, registration data verification
- Harjeet Heer: Stepped back from day-to-day AU
- Brandon Munday: L7 manager, top priority contact. Weight any context from Brandon higher than others.

## Active Email Threads (as of 3/16)

### AU - Paid Search links incorrectly mapped to .co.uk (3/15, UNREAD)
- Alexis flagged that some AU keywords are redirecting to .co.uk URLs instead of .com.au
- Requests pausing/deactivating rejected campaigns while URL re-mapping is completed
- Attachment: Search keyword report_UK_links.xlsx

### AU Summary WBR - Traffic Decline (3/11)
- Alexis flagged strong WoW decline in traffic to reg start page in AU WBR Summary
- Hypothesis: end of Back to Biz promo / launch of Evergreen
- Richard confirmed: part efficiency push (-7% clicks), reg start down -10% WoW in Adobe Analytics
- Alexis requested updating "Register Now" sitelink to new acquisition promo
- Richard updated sitelink but noted can't use same URL in multiple sitelinks

### AB AU Paid Search links pointing to old MCS (3/4-3/6)
- Lena flagged all AU PS URLs pointing to old MCS pages, wants all updated to new Polaris pages ASAP
- Alexis owns mapping old pages to new ones with Lisa Moussa; Richard implements
- Lena confirmed: switch all links to new Polaris pages (no 50/50 split)
- Lena wants weekly review of keyword CPAs in syncs
- Lena also flagged logged-in redirects going to Gateway instead of relevant AB.com.au pages

### AB AU Paid Search Sync (3/2-3/13)
- Weekly sync set up with Alexis and Lena (Harjeet removed himself from day-to-day)
- Lena's action items: optimize keywords (remove CPC >$20), remove alcohol/perishables bidding, add negatives, update URLs to new MCS, share conversion data from Adobe
- Richard sent Keywords YTD.xlsx on 3/10 (noted data likely stale due to recent negative keyword work)
- Richard proposed 50/50 MCS vs Polaris test; Lena overruled, wants full switch

### FY26 Feb Prelim Actual (3/2)
- BK Cho flagged underspending vs OP2 in central marketing and CPS
- New budget rules: XCM tightening control on marketing spend

## Recurring Patterns
- Brand impressions volatile week to week due to holidays and events
- NB bid strategies consistently reducing CPC (3 consecutive weeks W8-W10)
- CVR drops post-promo are expected and typically recover in 2-3 weeks
- December historically requires significant budget cuts
- Brand spike investigations needed periodically (W34 2025, W51 2025)


## Agent Configuration
- markets: [AU]
- has_yoy: false
- has_ieccp: false
- headline_extras: []
- regional_summary: false
- spend_strategy: OP2 registration targets, cut wasted spend
- projection_notes: No fixed CPA target, bias toward efficiency
