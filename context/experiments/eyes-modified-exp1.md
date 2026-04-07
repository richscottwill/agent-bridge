<!-- DOC-0149 | duck_id: experiment-eyes-modified-exp1 -->
# Eyes — Perception & Awareness

*What Richard sees — market performance, competitive landscape, metric trends, test results, and what's coming. The canonical sensing layer.*

*Operating principle: Structural over cosmetic. Eyes doesn't just report numbers — it pre-interprets them so Richard walks into meetings with a position, not a spreadsheet. The predicted QA section reduces the decision of "what will they ask?" to a pre-loaded answer.*

Last updated: 2026-04-01 (loop run 15)
Sources: WBR callouts, MBR/QBR data, Google Ads, competitor monitoring, ad copy tests, W13 dashboard data, Slack ingestion (first scan)

---

## Market Health (Feb 2026)

<!-- Data: db("SELECT market, week, regs, cpa, cost, brand_regs, nb_regs, cvr FROM weekly_metrics ORDER BY market, week DESC") -->
<!-- Data: db("SELECT market, status FROM oci_status") -->
<!-- Data: db("SELECT market, competitor, impression_share, segment FROM competitors WHERE week = '2026 W13'") -->

### Market Deep Dives

| Market | Period | Regs | vs OP2 | CPA | Key Signal |
|--------|--------|------|--------|-----|-----------|
| US | Jan | 39K | +30% | — | Peak OCI impact (+86% YoY) |
| US | Feb | 32.9K | above plan | $65-77 Brand | Walmart IS driving Brand CPA up (was ~$40). Response: bid caps + NB OCI efficiency. |
| UK | Feb | +24% vs OP2 | +24% | — | -6% spend, still beat plan. Ad copy test: +86% CTR, +31% regs. weareuncapped.com 24% IS since Dec 2023. |
| DE | Feb | -4% vs OP2 | -4% | — | NB -22% vs OP2. Y25 baseline unusually strong. OCI lift W49-W51: +16-20%, 74-96% to expectation. |
| CA | Feb | +18.5% vs OP2 | +18.5% | $73 | Bulk CVR 0.82%→2.35% (+187%), Wholesale 0.75%→2.10% (+180%). OCI E2E launched 3/4, full impact Jul 2026. |
| JP | Feb | — | — | — | MHLW campaign ended 1/31 (major reg driver lost). Yahoo competitors emerging: shop-pro.jp 12-15% IS. |
| AU | W13 | 207 (-16% WoW) | — | $118 (+3%) | CVR -12% WoW (Brand -14%, NB -10%). Daily: Mon-Tue strong (53, 50) then collapsed (27, 22, 23, 8). NB CPC declining 7wks ($6.82→$4.81, -29%). NB CPA flat $187. Polaris migration mid-week may explain. Two-campaign structure proposed (3/24). Lena priorities: CPC/CPA, keyword-product mapping, Polaris. |
| MX | W13 | 354 (+9% WoW) | — | $66 (+6%) | NB regs +33% above avg. YoY: +91% regs, +37% spend. NB CPA $112 sustained from H2 2025 gains. Lorena now primary stakeholder. ie%CCP corrected to 93%. |

---

## OCI Performance

<!-- Data: db("SELECT market, status, launch_date, full_impact_date, reg_lift_pct, cpa_improvement FROM oci_status ORDER BY market") -->

### MCC Structure
- Master MCC: DSAP - Amazon Business Parent MCC (873-788-1095)
- NA MCC: 683-476-0964 (US, CA, MX)
- EU MCC: 549-849-5609 (UK, DE, FR, IT, ES)
- JP MCC: 852-899-4580
- AU: Not created

### Known Issues
- Duplicate hvocijid parameters in landing page URLs across EU3 + existing markets. Causing "Duplicate query param found" errors. JP not affected. Under investigation.

---

## Competitive Landscape

<!-- Data: db("SELECT market, competitor, impression_share, cpc_impact_pct, segment, notes FROM competitors ORDER BY market, competitor") -->

### US: Walmart Business
- First appeared Jul 2024 on Brand Core terms
- IS trajectory: 25% (Jul-Sep 2024) → 35% (Oct-Nov 2024) → 37-55% (Jan-Mar 2026)
- Peak IS: 55% in W6 2026
- Brand CPA impact: ~$40 avg → $65-$77 range
- Pattern: Pulls back during holidays, ramps Jan-Mar
- Response: Bid caps + NB efficiency via OCI. Do NOT escalate auction.

### Key Trends
1. Competition broadening: 1-2 per market (2023) → 3-5 (2026)
2. Walmart is the only sustained aggressive Brand bidder in US
3. EU competition is fragmentary — different competitors per market
4. JP competition intensifying on Yahoo specifically
5. Team's defense is efficiency, not escalation

---

## Ad Copy Testing

### Research Foundation (SP Study, Aug 2025)
What SPs said matters most: Price (31% US), Product quality (25% US), Selection (21% US).
What SPs said matters least: Bulk purchasing (27% US), Store location (24% US).
Why SPs didn't sign up: Believed bulk required (50%), savings wouldn't justify costs (31%).
**Critical insight:** SPs believe AB is not free and requires bulk purchasing. Existing ads reinforced both.

### What Changed
Shifted from bulk/wholesale/B2B messaging → price, quality, selection messaging.
- "Online Bulk Purchasing" → "Smart Business Buying"
- "Online Wholesale Purchasing" → "For Businesses of All Sizes"
- "Purchase at Wholesale Price" → "No Minimum Order Required"

### Results
**UK AMZ Portfolio (Phase 1, Jan 29 - Mar 2, 2026):**
- Test vs Control: +86% CTR, +333% clicks, +230% cost
- Pre/Post: +70% CTR, +28% clicks, +31% regs despite -25% impressions
- Confidence: HIGH (30-day test, meaningful volume)

**IT (Phase 1, Feb 19 - Mar 5, 2026):**
- +15% CTR directionally, but volume too low (-97% clicks vs control)
- Confidence: LOW (insufficient volume)

### Phasing
- Phase 1: NB 50% campaigns (High CPA) — in progress
- Phase 2: All NB
- Phase 3: Brand Plus
- EU4 translations completed via GlobalLink (delivered 2/18/2026)

---

## Predicted Questions (next session)

Based on calendar patterns, email threads, active projects, Slack signals as of 4/1/26 Wednesday PT.

**Q1: "What should I bring to the Adi sync at noon?"**
Adi confirmed JP Google account for OCI preflight (all ref tags unique, search ads only). Follow up on AI ad-copy workflow progress (JP translation rules, D-Pel vs AI decision matrix). Check if Adi has updates on the "process-snap" sync Richard was supposed to schedule. Also: Stacey's JP ref tag question in Slack — Adi may have context.

**Q2: "What's happening with OCI JP launch?"**
Major milestone: FR/IT/ES dialed to 100%, JP at 100%. CA on track for 04/07. First QBR goal of 2026 achieved (Kiran Pantham celebrated in OCI channel). Mukesh created MCM-147368188 for JP tracking template. Brandon confirmed Day7 MCM steps. Brandon deferred JP ref tag taxonomy update to post-launch — will discuss with Deepika Thursday. Richard is in the JP channel thread about ref tag changes.

**Q3: "What does Lena want from the AU weekly update?"**
Lena replied to Richard's AU PS Weekly Update (4/1) with 3 questions: (1) data dump with landing page URLs showing where traffic goes, (2) how many clicks redirect because customer is already logged in, (3) are we overstating CPAs due to repeat visitors. These are sharp analytical questions — Lena is digging into whether the CPA picture is worse than it looks or better. Richard needs to investigate Google Ads landing page report and potentially coordinate with analytics for logged-in redirect data.

**Q4: "Did Richard make progress on the Testing Approach doc?"**
No. 11 workdays. W14 day 2. Kate meeting is 11 business days away. Yesterday Richard sent the AU weekly update (good — proactive communication, addresses visibility gap) and moved meetings around for the offsite. But the doc remains untouched. The AU update is Level 2 work. The Testing Approach doc is Level 1 gate.

**Q5: "What's the Baloo noindex situation?"**
Slack signal (baloo-search-and-mcs, 3/31): meta tag noindex requirement not implemented on Baloo pages. Not impacting SEO while behind VPN, but flagged as a launch blocker. 6 replies in thread — actively being discussed. Richard should monitor but this is a tech team issue, not PS.

Last updated: 2026-04-01 (Wednesday PT)

---

## Data Pipeline
- WW Dashboard Y25 Final (full year baseline) — in intake
- WW Dashboard Y26 W13 (current week) — PROCESSED 3/30 via dashboard ingester + callout pipeline
- Change Log CSVs (EU5, MX/AU, NA/JP) — INGESTED 3/30 (477 rows to DuckDB)
- Weekly cadence: Richard drops new week's xlsx → run `python3 shared/tools/dashboard-ingester/ingest.py <path>` → callouts + JSON + WW summary auto-generated
- Ingester location: `~/shared/tools/dashboard-ingester/ingest.py`
- Output: per-market callout drafts in `~/shared/context/active/callouts/<market>/`, WW summary, JSON data extract
- Feeds: WBR callouts, MBR narratives, QBR trends, daily Google Ads checks (MX, AU, Paid App)

## What's Coming
- OCI ROW: FR/IT/ES/JP dialed up to 100% (3/31 Slack). CA on track for 04/07. JP tracking template MCM (MCM-147368188) in progress. JP ref tag taxonomy update deferred to post-launch (Brandon decision). First QBR goal of 2026 achieved.
- AI Max: US test planned Q2 2026, no test design written yet (3d overdue — was due 3/28)
- Project Baloo: Early access launched 3/30. Keywords delivered. Shopping Ads for AB.
- AEO/Zero-click: Educational session attended 3/10, POV queued (Level 4)
- Polaris Brand LP WW rollout: Frank Volinsky CANCELLED sync (3/31) — got requirements from Alex. No action needed. Weblab dial-up still targeting April 6-7.
