<!-- DOC-0110 | duck_id: context-2026-03-31_au-ps-w9-13-optimization -->
# AU Paid Search W9-13: Keyword-Level Optimization

Generated: 2026-03-31
Sources: Search Terms Report + Ref Tag Registrations (W9-13 Aggregated, VP WL)

## Methodology

Ref tags map 1:1 to keywords via final URL. Ref tag prefixes identify campaign type. Registration totals by campaign type (from ref tags): Brand Core ~437, Brand Phrase ~85, Food ~100, Beauty ~48, Electronics ~18, Celebrations ~10. All other campaigns = 0 regs. Within Brand, keyword-to-reg mapping inferred by click-volume correlation. Within Food/Beauty, exact keyword mapping requires final URL report.

Search terms are aggregated by their parent Keyword (keyword text + campaign + ad group = unique key). Each keyword's total spend = sum of all search terms that matched to it.

---

## SECTION 1: BRAND KEYWORDS (Registration Drivers)

### 1a. AU_Brand_Exact — ~437 regs

| Keyword | Agg. Clicks | Agg. Cost | Est. Regs | Est. CPA | Action |
|---|---|---|---|---|---|
| [amazon business] | 3,530 | $1,946 | ~220 | $8.85 | PROTECT |
| [amazon business account] | 583 | $557 | ~84 | $6.63 | PROTECT |
| [amazon business australia] | 446 | $695 | ~51 | $13.63 | PROTECT |
| [amazon business login] | 172 | $85 | ~10 | $8.50 | PROTECT |
| [amazon business account australia] | 58 | $178 | ~10 | $17.80 | MONITOR — CPA 2x core |
| [business amazon] | 59 | $18 | ~9 | $2.00 | PROTECT — efficient |
| [amazon business prime] (various exact) | ~80 | ~$100 | ~5 | ~$20 | MONITOR |
| [business prime] | 25 | $67 | ~4 | $16.75 | MONITOR |
| [amazon business sign in] | 10 | $15 | ~3 | $5.00 | OK — nav intent |
| [what is amazon business] | 25 | $219 | ~0-1 | HIGH | REDUCE — 7% of spend, informational |
| [amazon business information] | 10 | $107 | ~0 | N/A | REDUCE — pure info |
| [amazon business account vs personal] | 6 | $113 | ~0 | N/A | REDUCE — $18.89/cl |
| [is amazon business worth it] | 3 | $58 | ~0 | N/A | REDUCE — $19.33/cl |
| [amazon business cost] | 5 | $73 | ~0 | N/A | REDUCE — price shopping |
| [how does amazon business work] | 3 | $36 | ~0 | N/A | REDUCE |
| [amazon business account cost] | 5 | $34 | ~0 | N/A | REDUCE |
| [amazon business account benefits] | 5 | $39 | ~0 | N/A | REDUCE |
| [amazon business benefits] | 5 | $33 | ~0 | N/A | REDUCE |

Bloat search terms within Brand Exact (add as negatives):
- "amazon business deutschland" / "amazon business usa" — wrong country, $19-$34
- "amazon corporate services pty ltd" — legal entity, not product
- "merch by amazon australia" — wrong product

### 1b. AU_Brand_Phrase — ~85 regs

| Keyword | Est. Regs | Action |
|---|---|---|
| "amazon for business" | ~23 | PROTECT |
| "business amazon" (phrase) | ~15 | PROTECT |
| "business prime" (phrase) | ~9 | OK |
| "amazon business prime" (phrase) | ~8 | OK |
| "amazon prime business" (phrase) | ~4 | MONITOR |
| "amazon business account" (phrase) | ~3 | MONITOR |
| "amazon business portal" (phrase) | ~0-2 | CHECK |
| "amazon business information" (phrase) | ~0 | REDUCE |
| "amazon business delivery" (phrase) | ~0 | REDUCE |

Bloat search terms to negative within Brand Phrase:
- "amazon business for sale" / "for sale australia" — buying a business. 6+cl, $61
- "merch by amazon australia" — wrong product. 4cl, $50
- "amazon business ideas" — entrepreneurship. 4+cl, $29
- "how to dropship on amazon" — dropship intent
- "sell on amazon" / "selling on amazon" — seller intent
- "amazon wholesale suppliers" — supplier search, not AB signup. 31+cl, $28
- "amazon corporate services pty ltd" — legal entity. 26cl, $35+
- "ecms express amazon" — shipping tracking. 20cl, $14

---

## SECTION 2: FOOD & BEAUTY (Have Regs, Need Final URL Report)

### 2a. AU_Generic_P-V_Food — ~100 regs, need keyword-level mapping

Top-spend Food keywords (aggregated from search terms). Cannot confirm which have regs without final URL report.

| Keyword | Agg. Clicks (est.) | Agg. Cost (est.) | Likely Converting? |
|---|---|---|---|
| "bulk buy food" | ~30-40 | ~$80-100 | LIKELY — core intent |
| "bulk foods" | ~20-30 | ~$50-70 | LIKELY |
| "bulk chocolate" | ~30-40 | ~$80-100 | UNCERTAIN — consumer product |
| [bulk chocolate] (exact) | 5 | $16 | UNCERTAIN |
| "bulk drinks" | ~25-35 | ~$60-80 | UNCERTAIN — consumer |
| "bulk herbs" | ~15-20 | ~$40-60 | POSSIBLE — B2B spice procurement |
| [easter egg bulk buy] (exact) | 9 | $42 | SEASONAL — check |
| "bulk buy easter eggs" | ~15-20 | ~$50-70 | SEASONAL |
| "wholesale foodstuffs" | ~20-30 | ~$60-80 | POSSIBLE |
| "wholesale foods" | ~15-20 | ~$40-60 | POSSIBLE |
| "commercial kitchen supplies" | ~20-30 | ~$80-100 | UNLIKELY — equipment |
| "cooking suppliers" | ~10-15 | ~$30-50 | UNLIKELY — equipment |
| "coffee machines sellers" | ~10-15 | ~$30-50 | UNLIKELY — equipment |
| "vending machine distributor" | ~15-20 | ~$30-50 | UNLIKELY — equipment |
| "bottles wholesale" | ~40-50 | ~$100-130 | UNLIKELY — packaging supplier search |
| "jars bulk" / "jars wholesale" | ~40-50 | ~$100-130 | UNLIKELY — packaging/craft |
| "wholesale chocolate" | ~10-15 | ~$40-60 | UNCERTAIN |
| "bulk cups" | ~30-40 | ~$100-130 | UNCERTAIN — could be B2B |
| "bulk take out boxes" | ~20-30 | ~$80-100 | POSSIBLE — restaurant procurement |

Key insight: "bottles wholesale", "jars bulk", "jars wholesale" collectively are likely the BIGGEST spend buckets in Food, and they're mostly candle-making, craft, and packaging searches — NOT food procurement for AB. These are likely NOT converting. Examples:
- "candle jars with lids wholesale" — candle making
- "glass honey jars wholesale australia" — small producer packaging
- "perfume bottles wholesale australia" — cosmetics packaging
- "essential oil bottles wholesale" — aromatherapy
- "diffuser bottles wholesale" — home fragrance

ACTION: Pull final URL report. Expect jars/bottles keywords to show 0 regs. If confirmed, add "candle jars", "perfume bottles", "diffuser bottles", "essential oil bottles" as negatives in Food.

### 2b. AU_Generic_P-V_Beauty — ~48 regs, need keyword-level mapping

| Keyword | Agg. Clicks (est.) | Likely Converting? |
|---|---|---|
| "professional beauty products" | ~80-100 | LIKELY — core AB intent |
| "professional salon products distributors" | ~60-80 | LIKELY |
| "cosmetics wholesaler" / "beautician wholesaler" | ~30-40 | POSSIBLE |
| "makeup suppliers" | ~20-30 | POSSIBLE |
| "false eyelashes suppliers" | ~15-20 | POSSIBLE — niche |
| "bulk skin care products" | ~30-40 | UNCERTAIN — consumer vs pro |
| "bulk bath products" | ~10-15 | UNLIKELY — consumer |
| "bulk hair care products" | ~10-15 | UNCERTAIN |
| "nail care products distributors" | ~15-20 | POSSIBLE |
| "skin care products distributors" | ~5-10 | POSSIBLE |
| "wholesale skin care products" | ~5-10 | POSSIBLE |
| "hair wholesale" | ~15-20 | UNLIKELY — hair extension consumer |
| "wholesale lamps" | ~10-15 | UNLIKELY — wrong product matching |
| "wholesale brushes" | ~5-10 | UNCERTAIN |
| "bulk waxing" | ~5-10 | POSSIBLE — salon procurement |

Key insight: "wholesale lamps" is matching in Beauty because of "candle warmer lamp wholesale", "turkish lamp kits wholesale", "wholesale table lamps" — these are home decor, not beauty. Likely 0 regs. "hair wholesale" is mostly hair extension consumer searches, not salon procurement.

ACTION: Pull final URL report. Negative "lamp", "turkish lamp" in Beauty if confirmed 0 regs.

---

## SECTION 3: ZERO-REGISTRATION CAMPAIGNS — KEYWORD BLOAT

These campaigns had 0 registrations in W9-13. Every keyword = confirmed 0 regs.
Aggregated from search terms report (keyword text + campaign + ad group).

### 3a. AU_Generic (non-PV) — 0 regs, HIGHEST SPEND zero-reg campaign

Top keywords by aggregated spend:
