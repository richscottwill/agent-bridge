# AU Paid Search — Handoff Guide

**Purpose:** Everything the AU team needs to independently manage the AU Paid Search program after the PS team transitions out.
**Transition date:** Week of April 13, 2026
**Hand-off call:** April 14, 2026 (may reschedule pending AU availability)
**Post-transition support:** Ad hoc calls between Lena/Brandon as needed. PS team will email AU team before implementing any WW initiatives that affect AU.

---

## 1. Program Overview

**What this is:** Amazon Business Australia runs paid search campaigns on Google Ads to drive SSR (Self-Service Registration) signups. The PS (Paid Search) team has managed this since AU launch in June 2025.

**Account structure:**
- Google Ads account sits under the DSAP parent MCC
- Two campaign types: Brand (exact/phrase match on "amazon business" terms) and Non-Brand (product/category keywords)
- Adobe Cloud (AMO) is the bid management platform — bid strategies are set there, not in Google Ads directly
- Conversion tracking flows through Google Ads native tracking (no OCI yet — see Section 8)

**Key contacts post-transition:**
- Brandon Munday (L7) — PS team lead, ad hoc escalation
- Richard Williams — PS team, available for questions during transition period
- Alexis Eck (L6) — collaborative execution partner, familiar with AU campaigns
- ABMA team — for data/attribution issues (submit SIM tickets)

---

## 2. Current Performance Snapshot (as of W15, Apr 5–11, 2026)

| Metric | W15 Actual | WoW Change | April Projection | OP2 Monthly Target (Apr) |
|---|---|---|---|---|
| Registrations | 166 | -2% | 886 | 1,071 |
| Spend (Net USD) | ~$26K | +17% | $108K | $148K |
| Blended CPA | $156 | +20% | $122 | $138 |

**What's happening right now:**
- We reverted landing pages from Polaris back to pre-Polaris versions in W15. The Polaris migration (completed mid-W13) caused a CVR collapse from ~4.0% to 2.8%. Expect CVR to recover to the 4.0% range over the next 1–2 weeks.
- Non-Brand is driving the upside: +22% regs WoW on +15% clicks and +5% CVR.
- Brand fell -21% regs on -10% clicks and -12% CVR — likely still recovering from the LP switch.
- NB CPC has been declining for 8+ weeks (down 29% from the W6 peak of ~$6.80 to $4.81 in W13). This is a positive efficiency signal.

**6-week registration decline context:** Regs peaked at 328 in W7 and fell to 166 in W15 (-49%). The primary driver was the Polaris URL migration CVR collapse, not a demand problem. With the revert, we expect recovery.

---

## 3. FY26 Budget & Targets (OP2)

### Annual Summary

| Metric | FY25 Actual (Jun–Dec) | FY26 OP2 Full Year |
|---|---|---|
| Budget (Net USD) | $1,139,602 | $1,801,927 |
| Registrations | 8,763 | 12,906 |
| Blended CPA | $158 | $140 |

### Monthly OP2 Targets

| Month | Gross USD | Net USD (Platform Spend) | Regs | CPA (Net USD) |
|---|---|---|---|---|
| Jan | $158,717 | $142,845 | 1,140 | $125 |
| Feb | $163,991 | $147,592 | 1,110 | $133 |
| Mar | $163,991 | $147,592 | 1,082 | $136 |
| Apr | $163,991 | $147,592 | 1,071 | $138 |
| May | $163,991 | $147,592 | 1,189 | $124 |
| Jun | $163,991 | $147,592 | 1,219 | $121 |
| Jul | $191,793 | $172,614 | 1,105 | $156 |
| Aug | $207,209 | $186,488 | 1,062 | $176 |
| Sep | $163,991 | $147,592 | 1,071 | $138 |
| Oct | $163,991 | $147,592 | 1,083 | $136 |
| Nov | $163,991 | $147,592 | 1,006 | $147 |
| Dec | $132,491 | $119,244 | 768 | $155 |
| **Total** | **$2,002,138** | **$1,801,927** | **12,906** | **$140** |

### YTD Actuals vs OP2

| Month | OP2 Spend | Actual Spend | OP2 Regs | Actual Regs | Actual CPA |
|---|---|---|---|---|---|
| Jan | $142,845 | ~$143K | 1,140 | ~1,100 | ~$130 |
| Feb | $147,592 | ~$159K | 1,110 | ~1,100 | ~$145 |
| Mar | $147,592 | ~$125K | 1,082 | ~1,030 | ~$121 |
| Apr (proj) | $147,592 | ~$108K | 1,071 | ~886 | ~$122 |

**Key takeaway:** CPA is running below the $140 target (good), but registration volume is running 15–20% below OP2 targets. The gap is a volume problem, not an efficiency problem.

### Budget Rules

- Monthly budgets can be adjusted based on performance trends
- **The total annual spend cannot exceed the OP2 annual budget ($2,002,138 gross / $1,801,927 net)**
- If additional budget is received (e.g., intra-channel AU transfer), **alert the Paid Search team**
- R&O (Revenue & Operations) pacing is listed monthly above. R&O suggested pacing is based on projections given limited historical data (AU launched Jun 2025)

---

## 4. How to Monitor Performance

### Weekly Performance Doc

**Primary tracker:** [AU PS Weekly Performance (Quip)](https://quip-amazon.com/84SxAbCaICKb/AU-PS-Weekly-Performance)
- Contains OP2 targets, WoW trends (registrations, spend), MTD pacing vs OP2
- Callout context and notes on changes in targets, bid strategies, focus areas
- AU team is now responsible for updating this weekly

**Reporting spreadsheet:** [AU-Paid-Search.xlsx (SharePoint)](https://amazon-my.sharepoint.com/:x:/p/prichwil/IQBD-gb5zK5xS4tVlz4m6wDyAW5afOGDAhKnxs0fPCKmc48?e=aYyd6G)

### How to Pull Registration Data

**Option A — GenBI:**
- Use GenBI for self-service reporting on campaign/registration data
- Campaign-level data can be pulled weekly
- For issues with GenBI, reach out to ABMA

**Option B — Hubble Query:**
Use this query to pull AU registrations by channel:

```sql
SELECT
  nva.account_verified_date,
  nva.feature_name,
  CASE WHEN CAA.business_tier_new IN ('SSR', 'SMB') THEN CAA.business_tier_new ELSE 'CPS' END as Business_classification,
  'AU' AS Market_Country,
  count(distinct nva.business_account_id)
FROM abbd_sandbox_mktg.ab_acq_channel_attr nva
LEFT JOIN abbd_sandbox_mktg.ab_business_accts_agg_metrics CAA
  ON nva.BUSINESS_ACCOUNT_ID = CAA.BUSINESS_ACCOUNT_ID
  AND nva.marketplace_id = caa.marketplace_id
WHERE nva.is_abuse = 0
  AND nva.overall_status IN ('VERIFIED_POSITIVE','WHITELISTED')
  AND nva.channel = 'Paid Search'
  AND nva.marketplace_id = 111172
  AND nva.account_verified_date BETWEEN '20260101' AND '20261231'
GROUP BY 1,2,3,4
ORDER BY 1
```

**Option C — Adobe Exports:**
Adobe Cloud can be configured to send automated reports via email:
- Campaign-level, ad group-level, or keyword-level views
- Different time lookback windows (daily, weekly, monthly)
- Can be set up to email a distribution list on a recurring schedule
- Advanced option: If you have an Excel template, Adobe can insert raw campaign-level data daily and email it to you

### Performance Splits Available

- Performance by time period and search segment (including ref) via GenBI
- Registrations by campaign via GenBI or Hubble
- Keyword-level registration data is **not available until Q3 2026** — all NB keyword analysis is directional until then

---

## 5. Optimization Playbook

### Goals
Drive maximum volume of registrations within efficiency/budget constraints. The primary metric is blended CPA at or below $140 (OP2 target).

**Important context:** There is no ie%CCP target for AU yet. CCP data is not expected until July 2026. Until then, CPA is the only governing efficiency metric.

### What Levers to Pull

**Brand campaigns:**
- Brand is efficient ($38–$45 CPA range) and driven primarily by organic search demand
- Brand traffic is volatile — it correlates with promotions, holidays, and seasonal events
- Don't cut Brand budget to save money; it's already efficient. Focus optimization energy on NB.

**Non-Brand campaigns:**
- NB is where the CPA challenge lives ($180–$240 CPA range)
- NB CPC has been declining for 8 weeks (good) but CVR has been declining too (bad — Polaris-related, now reverted)
- Optimization approach per Brandon's guidance: **Focus on the top 20 outlier keywords by CPC/CPA, not broad keyword removal.** CPC caps are a "two-way door" — reversible.
- Negative keywords have been added across campaigns to improve bid strategy effectiveness
- Bid strategies are managed in Adobe Cloud, not Google Ads directly

### Testing Approach

- **Recommended testing period:** End of September 2026 (allows enough data to accumulate post-OCI)
- **Two-campaign structure pilot:** Product-intent keywords vs. business-intent keywords — approved for phased testing with a 4-week measurement period before scaling
- **Landing page testing:** Polaris pages were reverted due to CVR issues. Any future LP testing should be monitored closely for CVR impact. Consider testing EN pages first (including UK/AU), then non-EN since those need localization.

### Keyword Management

- A keyword file was shared covering W12–W13: [au_all_keywords_w12_13.xlsx](https://amazon-my.sharepoint.com/:x:/p/prichwil/IQDxRiZuasDMQrVU-sPoN8clATgDB48relsUg_rxoQd4pFA?e=l8g5Yi)
  - Tab 1: Keywords with higher than $100 CPA
  - Tab 2: Raw keyword performance
  - Search queries show what people searched; keywords show what the queries matched to
- Feedback on search queries helps determine fit for the business
- Separate generic vs. product keywords (don't mix them)
- Perishables and alcohol: keywords paused and negatives added — we should not be bidding on these terms

---

## 6. Billing & Financial Operations

### R&O (Revenue & Operations)
- **AU team owns R&O starting April 2026** (March R&O concluded April 9)
- Subscribe to ab-marketing-budget@ for communications
- When completing R&O, use the **SSR tracker file**
- Only update the **AU row** within the "SSR Acquisition Paid Search" section (cells R100–R112)
- R&O sample from Q1 is available in the tracker file for reference

### ASP & PO
- Owned by AU team — no change from current process

### Google Ads PO
- AU team updates when new POs are created (Stella owns PO creation)
- The current PO covers all of 2026 — a new PO will not be needed until 2027

---

## 7. Rules & Guardrails

### Access
- **Do not remove Paid Search team Google Ads access.** The PS team needs continued access for WW initiative coordination and troubleshooting support.

### Reporting & Documentation
- AU team is responsible for performance updates in xBRs and docs
- Use GenBI for reporting data
- For data issues, reach out to ABMA (submit SIM ticket)

### Ref Tag Naming Convention
All registrations are attributed based on ref tag naming. **Registrations will only be attributed if the naming convention is followed.**

**Current structure:**
- Brand: ref tag contains `pd_sl_au_brand`
- Non-Brand: ref tag contains `pd_sl_au` but does NOT contain `brand`

**Creating new ref tags:**
- New refs can be created using the current format above
- **Any ref tag updates must be aligned with the PS team** — misnamed refs will break attribution

### Paid Search Flash
- Subscribe to the PS Flash for WW updates
- Can submit a SIM ticket for help/questions

### WW Initiatives
- **Events:** AU PS to work with AU team for creation of sitelinks. These are typically localized anyway — AU team can handle directly.
- **Landing Page / MCS Updates:** PS team will alert AU once WW NB updates are complete. AU team can utilize pages as they see fit.

---

## 8. Upcoming: OCI (Online Conversion Integration)

**What it is:** OCI connects Google Ads conversion tracking to Amazon's internal conversion data, improving bid strategy optimization. Markets with OCI see 18–24% registration uplift (US +24%, UK +23%, DE +18%).

**AU OCI status:** No confirmed timeline. **No MCC has been created yet.** MCC creation requires 2–3 weeks of lead time for Google Ads account setup and conversion signal configuration once kicked off.

**Action needed:** MCC creation and an AU OCI timeline decision are both open. At AU's current ~170 regs/week baseline, a 20% OCI uplift would add ~34 regs/week (~1,768 annualized, worth ~$230K at $130 CPA).

**AU team action:** Coordinate with PS team on MCC creation timing.

---

## 9. Landing Pages

**Current state:** Polaris landing pages were tested in W13 and caused a significant CVR drop (from ~4.0% to 2.8%). Pages have been reverted to pre-Polaris versions as of W15.

**Key pages:**
- Registration page: https://www.amazon.com.au/business/register/org/landing
- MRO/Industrial LP: https://business.amazon.com/en/cp/lpa-mro-industrial (used for NB email overlay test)

**Landing page testing guidance:**
- Any LP changes carry risk to registration performance — monitor CVR closely after any change
- Start with a smaller percentage of traffic in test, increase as confident
- Consider the full funnel (ad → LP → registration → verification), not just the LP in isolation
- If building new pages, start with EN (including UK/AU) then localize

---

## 10. Process: New Country Launches & Ongoing Oversight

### New Country Launches
- PS team provides account copy for localization as needed

### Ongoing Oversight
- PS team will alert AU for WW issues (rare)
- No regular cadence required — ad hoc as needed

---

## 11. Key Reference Documents

| Document | What It Contains | Link |
|---|---|---|
| AU PS Weekly Performance | WoW performance, callouts, notes | [Quip](https://quip-amazon.com/84SxAbCaICKb/AU-PS-Weekly-Performance) |
| AU PS Launch Doc | Original launch planning | [Quip](https://quip-amazon.com/JMZ9AAput1I) |
| 2026 AU Testing | Test tracker | [Quip](https://quip-amazon.com/IAJ9AAZJsDL) |
| AU Events Calendar | Planned events | [Quip](https://quip-amazon.com/GkMhANNFpn7z) |
| AU Market Guide H1 2026 | Google team market insights | [PDF in Quip](https://quip-amazon.com/-/blob/ZZR9AAs7OfO/Becr7zzFycBTLz0G0O4ukA) |
| Y26 OP2 Forecast | Registration forecast model | [SharePoint](https://amazonaus-my.sharepoint.com/:x:/r/personal/gompesm_amazon_com/_layouts/15/doc2.aspx?sourcedoc=%7B0042920A-2D17-43C3-B967-F05C6F340D72%7D) |
| AU Holidays | Public holidays calendar | [publicholidays.com.au](https://publicholidays.com.au/#2025-public-holidays) |

---

## 12. Internal Next Steps (PS Team — Pre-Handoff)

- [x] Brandon to email Lena re: handoff call timing (4/13)
- [x] Brandon to confirm with Kate first (4/13)
- [ ] Richard to prepare this documentation (4/14)
- [ ] Richard to add YTD Actuals/R&O column to budget table (see Section 3)
- [ ] Confirm OCI MCC creation timeline with AU team
- [ ] Schedule first biweekly keyword review with Alexis (target: week of Apr 14)
