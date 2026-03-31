# Eyes — Perception & Awareness

*What Richard sees — market performance, competitive landscape, metric trends, test results, and what's coming. The canonical sensing layer.*

*Operating principle: Structural over cosmetic. Eyes doesn't just report numbers — it pre-interprets them so Richard walks into meetings with a position, not a spreadsheet. The predicted QA section reduces the decision of "what will they ask?" to a pre-loaded answer.*

Last updated: 2026-03-31 (loop run 14)
Sources: WBR callouts, MBR/QBR data, Google Ads, competitor monitoring, ad copy tests, W13 dashboard data

---

## Market Health (Feb 2026)

<!-- Data: db("SELECT market, week, regs, cpa, cost, brand_regs, nb_regs, cvr FROM weekly_metrics ORDER BY market, week DESC") -->
<!-- Data: db("SELECT market, status FROM oci_status") -->
<!-- Data: db("SELECT market, competitor, impression_share, segment FROM competitors WHERE week = '2026 W13'") -->

### Market Deep Dives

**US — Strong, OCI-powered growth.** Jan: 39K regs (+30% vs OP2, +86% YoY) — peak OCI impact. Feb: 32.9K normalizing but well above plan. Brand CPA pressure $65-77 (was ~$40 pre-Walmart). Response: bid caps on Brand, NB efficiency via OCI absorbs CPA increase at program level.

**UK — Efficiency gains despite spend reduction.** Surpassed OP2 by 24% in Feb despite -6% spend. Ad copy test (Jan 29-Mar 2): +86% CTR, +31% regs, +70% CTR pre/post. weareuncapped.com at 24% IS since Dec 2023; Amazon Global Logistics UK emerging W8-W10.

**DE — Slight miss, high baseline.** Missed OP2 by 4%; NB -22% vs OP2. Y25 was unusually strong. OCI lift tracking: W49-W51 showed +16-20% lift, 74-96% to expectation.

**CA — LP optimization paying off.** Bulk CVR: 0.82% to 2.35% (+186.6%), Wholesale CVR: 0.75% to 2.10% (+180%). OCI E2E launched 3/4, full impact projected Jul 2026.

**JP — MHLW headwind.** MHLW campaign ended 1/31 — was a major registration driver. New competitors emerging on Yahoo (shop-pro.jp 12-15% IS).

**AU — Polaris migration + CVR compression.** W13: 207 regs (-16% WoW), $24K spend (-13%), CPA $118 (+3%). CVR compressed -12% WoW (Brand -14%, NB -10%). Mon-Tue strong (53, 50 regs) before Wed-Sat collapsed (27, 22, 23, 8). NB CPC declining 7 consecutive weeks ($6.82 W6 → $4.81 W13, -29%). NB CPA flat at $187. Polaris URL migration completing mid-week may explain daily pattern. Two-campaign structure proposed (3/24). Lena's 3 priorities: keyword CPC/CPA, keyword-to-product mapping, Polaris migration.

**MX — Steady growth, NB surge.** W13: 354 regs (+9% WoW), $23K spend (+15%), CPA $66 (+6%). NB regs +33% above recent avg. YoY: +91% regs, +37% spend. NB CPA $112 sustained from H2 2025 efficiency gains. Lorena now primary PS stakeholder. ie%CCP corrected to 93% (ingester bug fixed — was reading CPA as ie%CCP).

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

Based on calendar patterns, email threads, active projects as of 3/31/26 Tuesday PT.

**Q1: "What do I need for the Frank Volinsky sync at 11:30?"**
Frank wants to confirm requirements for MCS-3004 (WW PS Brand Polaris Redesign weblab). Bring: market priority list (AU > MX > DE > UK > JP > FR > IT > ES > CA > US-ES per Brandon), current Polaris page URLs per market, weblab parameters (traffic split, duration, success metrics), do-no-harm criteria (minimal localization, follow US template). Alex's page creation task status. Weblab dial-up still targeting April 6-7.

**Q2: "What should I bring to the Brandon 1:1 at 2pm?"**
10 workdays at zero on Testing Approach doc. Brandon's #1 feedback: visibility. But also: Baloo keyword data delivered ✅, W13 callouts produced for all 10 markets, prediction engine built, data layer overhauled, callout pipeline consolidated. Massive Level 3/5 output. The question is whether Brandon sees this as progress or as avoidance of Level 1. Also: Polaris weblab sync outcome from 11:30am, Lorena still unanswered (6 days), Memorial Day feedback due today.

**Q3: "What's the AU sync prep for 4:30pm?"**
W13 AU data: 207 regs (-15.5% WoW), $24K spend (-12.9%), CPA $118 (+3%). Regs below recent avg by 21%. NB regs down 25%. CPC down 21%. Polaris migration completing. Two-campaign structure proposal (product-intent vs business-intent) from 3/24. Lena's 3 priorities: keyword CPC/CPA investigation, keyword-to-product mapping, Polaris migration. Rolling 4-week CPA dashboard still not started.

**Q4: "Did Richard make progress on the Testing Approach doc?"**
No. 10 workdays. W13 was zero. Monday 3/30 had open blocks — Richard delivered Baloo keywords and followed up on ABMA-11245 instead. The pattern is consistent: Richard does valuable execution and system-building work but avoids the strategic artifact. The aMCC is at maximum alert.

**Q5: "What happened with the system builds over the weekend?"**
Prediction engine (Bayesian, 9 modules, 10 test files), data layer overhaul (query.py expansion, agent state functions, DuckDB MCP, 6 PBT test files, migration scripts), WBR callout pipeline consolidation (3 parameterized agents, W13 callouts for all 10 markets), attention tracker (full app, 34 test files), ie%CCP ingester bug fix, change log ingestion (477 rows). Massive Level 3/5 output.

Last updated: 2026-03-31 (Tuesday PT)

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
- OCI ROW: CA/JP/EU3 E2E launched, full impact Jul 2026
- AI Max: US test planned Q2 2026, no test design written yet (3d overdue — was due 3/28)
- Project Baloo: Early access launched 3/30. Keywords delivered. Shopping Ads for AB.
- AEO/Zero-click: Educational session attended 3/10, POV queued (Level 4)
- Polaris Brand LP WW rollout: Frank Volinsky sync TODAY 11:30am PT to confirm requirements. Weblab dial-up targeting April 6-7.
