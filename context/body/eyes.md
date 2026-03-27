# Eyes — Perception & Awareness

*What Richard sees — market performance, competitive landscape, metric trends, test results, and what's coming. The canonical sensing layer.*

*Operating principle: Structural over cosmetic. Eyes doesn't just report numbers — it pre-interprets them so Richard walks into meetings with a position, not a spreadsheet. The predicted QA section reduces the decision of "what will they ask?" to a pre-loaded answer.*

Last updated: 2026-03-26 (loop run 11)
Sources: WBR callouts, MBR/QBR data, Google Ads, competitor monitoring, ad copy tests

---

## Market Health (Feb 2026)

| Market | Regs | vs OP2 | YoY | Spend | CPA | OCI Status | Key Competitor | Notes |
|--------|------|--------|-----|-------|-----|------------|----------------|-------|
| US | 32.9K | +16% | +68% | $2.7M | $83 | Live (100%) | Walmart (37-55% IS) | OCI driving NB gains; Brand CPA up to $65-77 from Walmart |
| UK | ~5K est | +24% | N/A | N/A | N/A | Live (100%) | weareuncapped (24% IS) | Surpassed OP2 despite -6% spend; ad copy test +86% CTR |
| DE | ~4K est | -4% | N/A | N/A | N/A | Live (100%) | recht24-7.de (14% IS) | Missed OP2; NB -22% vs OP2, higher Y25 baseline |
| FR | N/A | N/A | N/A | N/A | N/A | In Progress (E2E) | bruneau.fr (39-47% NB IS) | OCI E2E launched 2/26 |
| IT | N/A | N/A | N/A | N/A | N/A | In Progress (E2E) | mondoffice/Shopify | OCI E2E launched 2/26; ad copy test early stage |
| ES | N/A | N/A | N/A | N/A | N/A | In Progress (E2E) | amazon.co.uk AGL | OCI E2E launched 2/26 |
| CA | 2.8K | +18.5% | +32.3% | $207K | $73 | In Progress (E2E 3/4) | Shopify (+13% CPC) | LP optimization: Bulk CVR +187%, Wholesale +180% |
| JP | 1.6K | -47.5% | N/A | N/A | N/A | In Progress (E2E 2/26) | axalpha, shop-pro.jp | MHLW ended 1/31 — major reg driver gone |
| AU | 1.1K | -1% | N/A | $159K | ~$140 target | Not planned | None significant | Traffic decline WoW from bid strategy + seasonal transition |
| MX | 1.1K | +32% | +37% | $68K | N/A | Not planned | algo-mas.mx (11-13% IS) | Strong growth; invoice mgmt ongoing |

### Market Deep Dives

**US — Strong, OCI-powered growth.** Jan: 39K regs (+30% vs OP2, +86% YoY) — peak OCI impact. Feb: 32.9K normalizing but well above plan. Brand CPA pressure $65-77 (was ~$40 pre-Walmart). Response: bid caps on Brand, NB efficiency via OCI absorbs CPA increase at program level.

**UK — Efficiency gains despite spend reduction.** Surpassed OP2 by 24% in Feb despite -6% spend. Ad copy test (Jan 29-Mar 2): +86% CTR, +31% regs, +70% CTR pre/post. weareuncapped.com at 24% IS since Dec 2023; Amazon Global Logistics UK emerging W8-W10.

**DE — Slight miss, high baseline.** Missed OP2 by 4%; NB -22% vs OP2. Y25 was unusually strong. OCI lift tracking: W49-W51 showed +16-20% lift, 74-96% to expectation.

**CA — LP optimization paying off.** Bulk CVR: 0.82% to 2.35% (+186.6%), Wholesale CVR: 0.75% to 2.10% (+180%). OCI E2E launched 3/4, full impact projected Jul 2026.

**JP — MHLW headwind.** MHLW campaign ended 1/31 — was a major registration driver. New competitors emerging on Yahoo (shop-pro.jp 12-15% IS).

**AU — Intentional efficiency trade-off.** Traffic decline WoW attributed to bid strategy changes + Back to Biz ending. Deep dive pending. New acquisition promo: 20% off, AU$50 max. CPC $6 avg challenged by Lena (3/19).

**MX — Steady growth.** +32% vs OP2, +37% YoY. Competitor algo-mas.mx at 11-13% IS on Brand, +20% CPC spikes.

---

## OCI Performance

### Rollout Timeline
| Market | Status | Launch Date | Full Impact |
|--------|--------|-------------|-------------|
| US | Live | Jul 2025 → Sep 2025 (100% NB) | Oct 2025 |
| UK | Live | Aug 2025 → Sep 2025 (100%) | Oct 2025 |
| DE | Live | Nov 2025 → Dec 2025 (100%) | Jan 2026 |
| CA | In Progress | Mar 2026 (E2E 3/4) | Jul 2026 |
| JP | In Progress | Feb 2026 (E2E 2/26) | Jul 2026 |
| FR | In Progress | Feb 2026 (E2E 2/26) | Jul 2026 |
| IT | In Progress | Feb 2026 (E2E 2/26) | Jul 2026 |
| ES | In Progress | Feb 2026 (E2E 2/26) | Jul 2026 |
| AU | Not planned | N/A | N/A |
| MX | Not planned | N/A | N/A |

### Impact Summary
| Market | Test Period | Reg Lift | CPA Improvement | Estimated OPS |
|--------|-----------|----------|-----------------|---------------|
| US | Jul-Oct 2025 | +24% (+32K regs) | ~50% NB CPA | $16.7MM |
| UK | Aug-Oct 2025 | +23% (+2.4K regs) | Significant | N/A |
| DE | Oct-Dec 2025 | +18% (+749 regs) | Significant | N/A |
| **Total** | | **+35K regs** | | **$16.7MM+** |

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

### US: Walmart Business
- First appeared Jul 2024 on Brand Core terms
- IS trajectory: 25% (Jul-Sep 2024) → 35% (Oct-Nov 2024) → 37-55% (Jan-Mar 2026)
- Peak IS: 55% in W6 2026
- Brand CPA impact: ~$40 avg → $65-$77 range
- Pattern: Pulls back during holidays, ramps Jan-Mar
- Response: Bid caps + NB efficiency via OCI. Do NOT escalate auction.

### EU5 Competitors
| Market | Competitor | IS | Impact |
|--------|-----------|-----|--------|
| UK | weareuncapped.com | 24% Brand | +45% Brand Core CPC. Persistent since Dec 2023. |
| UK | Temu | 13% Generic NB | +14% NB CPC |
| UK | Amazon Global Logistics UK | <10% ES Brand | +41% CPC (W8-W10 2026) |
| DE | recht24-7.de | 14% Brand Core | +3% MoM CPC; reported for store closure |
| FR | bruneau.fr | 39-47% Generic NB | Significant NB pressure |
| FR | mirakl.com | 10% Brand Core | -5% clicks, -14% CVR |
| IT | Shopify (mondoffice) | >10% Generic NB | -20% CVR on Generic |
| IT | revolut.com | <10% | -36% CVR drop on Brand Core (W10) |
| ES | amazon.co.uk (AGL) | <10% | +41% CPC (2/13-3/4) |

### International Competitors
| Market | Competitor | IS | Notes |
|--------|-----------|-----|-------|
| CA | Shopify.com | <10% Brand Core | Recurring, +13% CPC |
| JP | axalpha.com | 10% Brand Core Google | New threat |
| JP | shop-pro.jp | 12-15% Yahoo Brand Core | Strengthening |
| MX | algo-mas.mx | 11-13% Brand | +20% CPC spikes |

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

Based on calendar patterns, email threads, active projects as of 3/26/26 Thursday evening PT.

**Q1: "What's on my plate tomorrow?"**
LIGHT meeting day Friday. Update Kingpin (7am PT, 30 min — recurring). Biweekly AB Onsite Events Stakeholder (8:30am PT, 30 min — Caroline Miller, tentative). Otherwise open. AI Max test design due 3/28 (Saturday — effectively due Friday). Testing Approach doc outline still not started — 7 workdays since hard thing was set. Flash content due (AU status update, UK/CA decision). Baloo keyword cost data due Monday.

**Q2: "What happened with OCI APAC?"**
Mike Babich (Google) sent 3 follow-up questions at 11pm 3/26: (1) loop him into case 6-7924000040915 email thread, (2) confirm if new user access resolved the issue, (3) status of appeal for first user. Brandon needs to respond. Still unresolved — JP OCI launch delayed.

**Q3: "What came out of the R&O Flash review?"**
US highlight renamed to "Modern Search Structure" (combines campaign + portfolio consolidation). CA moved from highlight to status update (tariff-driven). AU moved from lowlight to announcements. WhatsApp simplified. Video strategy: Andrew to specify "unlocking new placements." DE tech issue under investigation (EAAAAA project). App resourcing: Peter to escalate to Kate/Todd. Brandon called out late submissions.

**Q4: "What does Lorena need?"**
Two open requests: (1) Q2 expected spend for MX PO submission (3/25 email — needs response), (2) keyword performance data + negative keyword strategy (3/19 email — still pending). She also added beauty LP inputs. Lorena is actively engaging — good sign for delegation.

**Q5: "What's the Baloo early access status?"**
Vijay briefed Richard 3/26. 50 stakeholders get Tampermonkey script. Direct URL (shop.business.amazon.com) for routine testing, Google search restricted to 5-6 leadership demo clicks. Richard owes keyword cost data + "don't use Google" blurb by Monday 3/30. Vijay will tag Richard in Baloo SIM. Kate attended prior demo — positive.

Last updated: 2026-03-26 (Thursday evening PT)

---

## Data Pipeline
- WW Dashboard Y25 Final (full year baseline) — in intake
- WW Dashboard Y26 W12 (current week) — PROCESSED 3/23 via dashboard ingester
- WW Dashboard Y26 W11 (prior week) — in intake
- Weekly cadence: Richard drops new week's xlsx → run `python3 shared/tools/dashboard-ingester/ingest.py <path>` → callouts + JSON + WW summary auto-generated
- Ingester location: `~/shared/tools/dashboard-ingester/ingest.py`
- Output: per-market callout drafts in `~/shared/context/active/callouts/<market>/`, WW summary, JSON data extract
- Feeds: WBR callouts, MBR narratives, QBR trends, daily Google Ads checks (MX, AU, Paid App)

## What's Coming
- OCI ROW: CA/JP/EU3 E2E launched, full impact Jul 2026
- AI Max: US test planned Q2 2026, no test design written yet (due 3/28)
- Project Baloo: US Q2 launch, unlocks Shopping Ads for AB
- AEO/Zero-click: Educational session attended 3/10, POV due today
- Polaris Brand LP WW rollout: Brandon set priority order (3/20), translations due 3/26
