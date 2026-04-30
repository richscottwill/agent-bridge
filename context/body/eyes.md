<!-- DOC-0222 | duck_id: organ-eyes -->






# Eyes — Perception & Awareness

*What Richard sees — market performance, competitive landscape, metric trends, test results, and what's coming. The canonical sensing layer.*

*Operating principle: Structural over cosmetic. Eyes doesn't just report numbers — it pre-interprets them so Richard walks into meetings with a position, not a spreadsheet. The predicted QA section reduces the decision of "what will they ask?" to a pre-loaded answer.*

Last updated: 2026-04-02 (loop run 17)
Sources: WBR callouts, MBR/QBR data, Google Ads, competitor monitoring, ad copy tests, W13 dashboard data, Slack ingestion (first scan)

---







## Market Health (Feb 2026)

<!-- Data: db("SELECT market, week, regs, cpa, cost, brand_regs, nb_regs, cvr FROM weekly_metrics ORDER BY market, week DESC") -->
<!-- Data: db("SELECT market, status FROM oci_status") -->
<!-- Data: db("SELECT market, competitor, impression_share, segment FROM competitors WHERE week = '2026 W13'") -->







### Market Deep Dives

**Reading this table:** Each row is one market's latest snapshot. "vs OP2" means performance against the annual operating plan. "Key Signal" is the single most important development — it always includes a cause (bid strategy change, CVR shift, competitor move, seasonal event), not just a number. When drafting callouts, lead with the Key Signal, not the raw numbers. If Key Signal mentions a person (e.g., "Lena priorities"), check roster.md for context.
  - *Example:* When reading this table:** each row is one market's lat, the expected outcome is verified by checking the result.







#### Richard's Markets (hands-on)

| Market | Period | Regs | vs OP2 | CPA | Key Signal |
|--------|--------|------|--------|-----|-----------|
| AU | W13 | 207 (-16% WoW) | — | $118 (+3%) | CVR -12% WoW (Brand -14%, NB -10%). Daily: Mon-Tue strong (53, 50) then collapsed (27, 22, 23, 8). NB CPC declining 7wks ($6.82→$4.81, -29%). NB CPA flat $187. Polaris migration mid-week may explain. Two-campaign structure proposed (3/24). Lena priorities: CPC/CPA, keyword-product mapping, Polaris. |
| MX | W13 | 354 (+9% WoW) | — | $66 (+6%) | NB regs +33% above avg. YoY: +91% regs, +37% spend. NB CPA $112 sustained from H2 2025 gains. Lorena now primary stakeholder. ie%CCP corrected to 93%. |








#### NA Markets

| Market | Period | Regs | vs OP2 | CPA | Key Signal |
|--------|--------|------|--------|-----|-----------|
| US | Feb | 32.9K | above plan | $65-77 Brand | Walmart IS 25%→55% driving Brand CPA up (was ~$40). Peak Jan: 39K (+86% YoY). Response: bid caps + NB OCI efficiency. |
| CA | Feb | +18.5% vs OP2 | +18.5% | $73 | Bulk CVR 0.82%→2.35% (+187%), Wholesale 0.75%→2.10% (+180%). OCI E2E launched 3/4, full impact Jul 2026. |







#### EU Markets

| Market | Period | Regs | vs OP2 | CPA | Key Signal |
|--------|--------|------|--------|-----|-----------|
| UK | Feb | +24% vs OP2 | +24% | — | -6% spend, still beat plan. Ad copy: +86% CTR, +31% regs. weareuncapped.com 24% IS since Dec 2023. |
| DE | Feb | -4% vs OP2 | -4% | — | NB -22% vs OP2. OCI lift W49-W51: +16-20%. |







#### APAC Markets

| Market | Period | Regs | vs OP2 | CPA | Key Signal |
|--------|--------|------|--------|-----|-----------|
| JP | Feb | — | — | — | MHLW campaign ended 1/31 (major reg driver lost). Yahoo competitors emerging: shop-pro.jp 12-15% IS. |

---







## OCI Performance

<!-- Data: db("SELECT market, status, launch_date, full_impact_date, reg_lift_pct, cpa_improvement FROM oci_status ORDER BY market") -->







### OCI Status by Market (as of 4/2)
| Market | Status | Launch/Target | Detail |
|--------|--------|---------------|--------|
| US | ✅ Live | 2025 | Baseline market. Peak Jan: 39K regs (+86% YoY). |
| UK | ✅ Live | E2E launched | Ad copy Phase 1 running: +86% CTR, +31% regs. |
| DE | ✅ Live | E2E launched | +16-20% lift (W49-W51). Data loss 3/18-3/25 — verify backfill. |
| FR | ✅ Live | 3/30 dial-up | 775 clicks confirmed 3/24 UTC. Monitor ramp. |
| IT | ✅ Live | 3/30 dial-up | 1,412 clicks. Ad copy: +15% CTR but LOW volume — needs longer window. |
| ES | ✅ Live | 3/30 dial-up | 1,168 clicks confirmed 3/24 UTC. Monitor ramp. |
| JP | ✅ Live | 3/31 dial-up | MCM-147368188 COMPLETE. Watch Yahoo competitor IS growth. |
| CA | 🟡 On track | Target 04/07 | E2E launched 3/4. Full impact expected Jul 2026. Next milestone: Apr dial-up. |
| AU | 🔴 Not started | TBD | No MCC created — blocked until MCC setup. |
| MX | 🔴 Not started | TBD | No MCC created — blocked until MCC setup. |

**Rollout: 7/10 live (70%).** Next: CA (Apr). AU/MX: TBD.







### Known Issues
- Duplicate hvocijid parameters in landing page URLs across EU3 + existing markets. Causing "Duplicate query param found" errors. JP not affected. Under investigation.







### MCC Structure
- Master MCC: DSAP - Amazon Business Parent MCC (873-788-1095)
- NA MCC: 683-476-0964 (US, CA, MX)
- EU MCC: 549-849-5609 (UK, DE, FR, IT, ES)
- JP MCC: 852-899-4580
- AU: Not created

**Worked example — reading OCI status for meeting prep:** CA shows 🟡 On track with E2E launched 3/4 and full impact Jul 2026. In a WBR, lead with "CA OCI on track for Apr dial-up, full impact expected Jul 2026" — the status emoji + target date is the callout, the detail row provides the backup if asked.

---







## Competitive Landscape

<!-- Data: db("SELECT market, competitor, impression_share, cpc_impact_pct, segment, notes FROM competitors ORDER BY market, competitor") -->







### Defense Posture & Trends
- **Posture: efficiency over escalation.** Do NOT escalate auctions.
- Market-wide: 1-2 competitors/market (2023) → 3-5 (2026).
- EU: fragmentary — different competitors per market. JP: intensifying on Yahoo.







### US: Walmart Business
Brand Core since Jul 2024. IS: 25%→55% (peak W6 2026). Brand CPA impact: ~$40→$65-77. Seasonal: ramps Jan-Mar, pulls back holidays. Response: bid caps + NB OCI efficiency. Only sustained US Brand bidder.







### JP: Yahoo Competitors
shop-pro.jp emerging with 12-15% IS. Intensifying since MHLW campaign ended 1/31 (major reg driver lost). Monitor for further IS growth.

**Worked example:** Walmart IS surged to 55% in W6 2026. Instead of increasing Brand bids to reclaim IS, we held bid caps and shifted budget to NB OCI (where Walmart doesn't compete). Result: Brand CPA stabilized at $65-77 without auction escalation, NB efficiency improved via OCI.

---







## Ad Copy Testing







### Research Foundation (SP Study, Aug 2025)
SPs said matters most: Price (31% US), Product quality (25%), Selection (21%).
SPs said matters least: Bulk purchasing (27%), Store location (24%).
Why SPs didn't sign up: Believed bulk required (50%), savings wouldn't justify costs (31%).
**Key insight:** SPs believe AB requires bulk purchasing and isn't free. Existing ads reinforced both.

*Example:* When this applies, the expected outcome is verified by checking the result.
### Messaging Shift
Bulk/wholesale/B2B → price, quality, selection:
- "Online Bulk Purchasing" → "Smart Business Buying"
- "Online Wholesale Purchasing" → "For Businesses of All Sizes"
- "Purchase at Wholesale Price" → "No Minimum Order Required"







### Results







#### UK AMZ Portfolio (Phase 1, Jan 29 - Mar 2, 2026)
- Test vs Control: +86% CTR, +333% clicks, +230% cost
- Pre/Post: +70% CTR, +28% clicks, +31% regs despite -25% impressions
- Confidence: HIGH (30-day test, meaningful volume)







#### IT (Phase 1, Feb 19 - Mar 5, 2026)
- +15% CTR directionally, but volume too low (-97% clicks vs control)
- Confidence: LOW (insufficient volume)







### Phasing
- Phase 1: NB 50% campaigns (High CPA) — in progress
- Phase 2: All NB
- Phase 3: Brand Plus
- EU4 translations completed via GlobalLink (delivered 2/18/2026)

---




## Pipeline, Outlook & Predicted Questions

_Predicted questions cleared at EOD 4/3. Regenerated each AM-2 from calendar + active threads + Slack signals._

*Example:* When this applies, the expected outcome is verified by checking the result.
### Data Pipeline

| Component | Detail |
|-----------|--------|
| **Ingestion** | Richard drops xlsx → `~/shared/tools/dashboard-ingester/ingest.py <path>` |
| **Outputs** | Per-market callout drafts (`~/shared/wiki/callouts/<market>/`), WW summary, JSON extract |
| **Feeds** | WBR callouts, MBR narratives, QBR trends, daily Google Ads checks (MX, AU, Paid App) |
| **Current data** | WW Dashboard Y25 Final (baseline), Y26 W13 (processed 3/30), Change Log CSVs (477 rows to DuckDB) |







### What's Coming

| Initiative | Status | Detail |
|-----------|--------|--------|
| AI Max | ⚠️ Test design 6d overdue (3/28) | US Q2 2026. No design written. L2. |
| Project Baloo | 🟢 Early access 3/30 | Shopping Ads for AB. Keywords delivered. L2. |
| AEO/Zero-click | 📋 POV queued | Educational session 3/10. L4. |
| Polaris Brand LP | 🟢 No action | WW rollout dial-up targeting Apr 6-7. |
