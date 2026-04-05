# Eyes — Perception & Awareness

*What Richard sees — market performance, competitive landscape, metric trends, test results, and what's coming. The canonical sensing layer.*

*Operating principle: Structural over cosmetic. Eyes doesn't just report numbers — it pre-interprets them so Richard walks into meetings with a position, not a spreadsheet. The predicted QA section reduces the decision of "what will they ask?" to a pre-loaded answer.*

Last updated: 2026-04-05 (Karpathy Run 28 — OCI Performance moved above Market Health, actionable-first)
Sources: WBR callouts, MBR/QBR data, Google Ads, competitor monitoring, ad copy tests, W13 dashboard data, Slack ingestion (first scan)

---

## OCI Performance

<!-- Data: db("SELECT market, status, launch_date, full_impact_date, reg_lift_pct, cpa_improvement FROM oci_status ORDER BY market") -->

### OCI Status by Market (as of 4/2)
| Market | Status | Key Date | Notes |
|--------|--------|----------|-------|
| US | 100% live | Launched 2025 | Baseline. Peak Jan: 39K regs (+86% YoY). |
| UK | 100% live | E2E launched | Tracking lift. |
| DE | 100% live | E2E launched | W49-W51: +16-20% lift. Data loss 3/18-3/25 (DUB→ZAZ migration). |
| FR | 100% live | Dialed up 3/30 | Confirmed 775 click events 3/24 UTC. |
| IT | 100% live | Dialed up 3/30 | Confirmed 1,412 click events 3/24 UTC. |
| ES | 100% live | Dialed up 3/30 | Confirmed 1,168 click events 3/24 UTC. |
| JP | 100% live | Dialed up 3/31 | MCM-147368188 COMPLETE — tracking template implemented, feed enabled. Ref tag taxonomy deferred post-launch. |
| CA | On track | Target 04/07 | E2E launched 3/4. Full impact projected Jul 2026. |
| AU | Not started | Target May 2026 | MCC not created. Discussed with Suzane (Adobe) 3/19. |
| MX | Not started | TBD | No MCC. |

### MCC Structure
- Master MCC: DSAP - Amazon Business Parent MCC (873-788-1095)
- NA MCC: 683-476-0964 (US, CA, MX)
- EU MCC: 549-849-5609 (UK, DE, FR, IT, ES)
- JP MCC: 852-899-4580
- AU: Not created

### Known Issues
- Duplicate hvocijid parameters in landing page URLs across EU3 + existing markets. Causing "Duplicate query param found" errors. JP not affected. Under investigation.

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

## Competitive Landscape

<!-- Data: db("SELECT market, competitor, impression_share, cpc_impact_pct, segment, notes FROM competitors ORDER BY market, competitor") -->

### US: Walmart Business
Brand Core since Jul 2024. IS: 25%→55% (peak W6 2026). Brand CPA impact: ~$40→$65-77. Seasonal: ramps Jan-Mar, pulls back holidays. Response: bid caps + NB OCI efficiency. Do NOT escalate auction.

### Trends
- Market-wide: 1-2 competitors/market (2023) → 3-5 (2026). Walmart only sustained US Brand bidder.
- EU: fragmentary — different competitors per market. JP: intensifying on Yahoo.
- Defense posture: efficiency over escalation.

---

## Ad Copy Testing

### SP Study (Aug 2025) — Messaging Foundation
SPs value: Price (31%), Quality (25%), Selection (21%). SPs reject: Bulk (27%), Location (24%).
Signup barriers: Believed bulk required (50%), savings wouldn't justify (31%).
**Key insight:** SPs think AB requires bulk and isn't free — old ads reinforced both misconceptions.

### Messaging Shift: Bulk/B2B → Price/Quality/Selection
| Old Copy | New Copy |
|----------|----------|
| Online Bulk Purchasing | Smart Business Buying |
| Online Wholesale Purchasing | For Businesses of All Sizes |
| Purchase at Wholesale Price | No Minimum Order Required |

### Results
| Market | Period | CTR | Regs | Confidence |
|--------|--------|-----|------|------------|
| UK (AMZ Portfolio) | Jan 29–Mar 2 | +86% (test vs ctrl), +70% (pre/post) | +31% despite -25% impr | HIGH |
| IT | Feb 19–Mar 5 | +15% directional | -97% clicks (low vol) | LOW |

### Phasing
Phase 1: NB 50% (High CPA) — in progress. Phase 2: All NB. Phase 3: Brand Plus.
EU4 translations via GlobalLink (delivered 2/18/2026).

---

## Predicted Questions

_Cleared at EOD 4/3. Regenerated each AM-2 from calendar + active threads + Slack signals._

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
- AI Max: US test planned Q2 2026, no test design written yet (6d overdue — was due 3/28)
- Project Baloo: Early access launched 3/30. Keywords delivered. Shopping Ads for AB.
- AEO/Zero-click: Educational session attended 3/10, POV queued (Level 4)
- Polaris Brand LP WW rollout: Weblab dial-up targeting April 6-7. Frank got requirements from Alex — no action needed.
