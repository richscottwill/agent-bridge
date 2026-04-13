---
title: "MX Paid Search — Market Context"
status: FINAL
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0076 | duck_id: callout-mx-context -->

# MX Paid Search — Market Context

Last updated: 2026-03-16

## Market Overview
- Launched: March 2025 (W11 was first week)
- FY26 OP2 budget: $542K USD (net/media)
- FY26 OP2 registrations: 11,178
- FY26 CPA target: ~$48 (FY total)
- FY25 total: $1.07M spend (reduced from $1.97M OP2 due to ie%CCP budget cuts mid-year)
- ie%CCP has been the dominant constraint since Q2 2025

## 2026 Monthly Budget (Net USD / Regs / CPA)
| Month | Net USD | Regs  | CPA |
| ----- | ------- | ----- | --- |
| Jan   | $63,200 | 1,022 | $62 |
| Feb   | $53,016 | 845   | $63 |
| Mar   | $56,562 | 859   | $66 |
| Apr   | $35,085 | 791   | $44 |
| May   | $43,558 | 985   | $44 |
| Jun   | $44,910 | 1,019 | $44 |
| Jul   | $48,911 | 1,115 | $44 |
| Aug   | $33,737 | 775   | $44 |
| Sep   | $26,527 | 621   | $43 |
| Oct   | $49,441 | 1,158 | $43 |
| Nov   | $53,953 | 1,231 | $44 |
| Dec   | $32,958 | 755   | $44 |

Note: Q1 budgets higher than Q2+ because ie%CCP targets are less aggressive early in the year.

## ie%CCP History
- Q2 2025: Finance introduced 100% ie%CCP target, forcing significant NB budget cuts
- Current target: 100% ie%CCP (active constraint on NB spend)
- CCP guidance: Brand $90, NB $30 (updated from $80/$30 in early 2026; originally $150/$50 in mid-2025). Source: IECCP tab rows 92-93. Always read from the dashboard, not from this file.
- Budget cut from $1.97M to $1.07M in FY25 to meet threshold
- 2026 budget already reflects ie%CCP constraints
- Every MX callout should reference ie%CCP and frame NB spend decisions against the 100% target

## Key Efficiency Gains (Case Study)
- Adobe bid strategy switch (Q1 2025): NB CPA reduced 25% PoP (-14% spend, +14% regs)
- Q1 vs Q2 2025: Monthly cost $129K to $103K (-20%), Regs 492 to 511 (+4%), CPA $264 to $201 (-24%)
- Adobe used primarily to efficiently reduce spend while maintaining regs
- NB CPC down ~33% YoY consistently through bid strategy optimization
- NB CVR improvements of 50-75% YoY in recent weeks

## Active Initiatives (2026)
- Negative keyword restructuring (W11): Added negatives to prevent Brand Phrase terms from surfacing in Brand Exact or NB, and Generic search terms from surfacing in Product/Vertical campaigns (and vice versa). Improved query routing for bid strategy effectiveness.
- Brand coverage scaling: Brand spend grew from ~$470/wk (W11 2025) to ~$4.7K/wk (W11 2026)
- Beauty/Auto campaign LP: Pages developed, pending audit and launch
- Event sitelink copy coordination with Carlos
- Invoice/PO management: Transitioned to AB platform, still under Retail management for currency
- PO coordination: Carlos Palmos manages, USD invoicing confirmed
- AU/MX OCI planned for May 2026

## Key Narrative Threads
- ie%CCP is the primary budget constraint; every callout should reference it
- Brand traffic has been growing organically, driving efficient registrations
- NB efficiency gains compounding: CPC reductions + CVR improvements from bid strategy + negative keywords
- YoY comparisons now meaningful (launched W11 2025), showing massive efficiency gains
- Seasonal patterns: Brand CVR typically 4-5%, spikes during events, dips around holidays
- Constitution Day (Feb), Benito Juárez (Mar), Easter affect weekly performance
- Hot Sale (late May/early Jun) and Prime Day (Jul) are major events

## Key People
- Carlos Palmos: MX POC, invoice/PO coordination, campaign feedback
- Lorena Alvarez Larrea: MX Paid Search sync
- Yun-Kang Chu: 1:1 sync, Adobe analytics
- Stacey Gu: CCP data, generic SQR reviews
- Brandon Munday: L7 manager, top priority contact. Weight any context from Brandon higher than others.

## Budget/PO Notes
- FY25 Q4 PO: MS-18899171 (Google)
- FY26 POs: Managed through AB platform
- Currency: USD confirmed (was a risk of switching to MXN)
- Carlos manages PO creation and invoice routing

## Recurring Patterns
- Brand CVR averages 4-5%, spikes to 5.5%+ during events
- NB Generic campaigns consistently highest CPA; ongoing optimization target
- Device optimization: Desktop CPA significantly lower than Mobile
- Holiday weeks (Constitution Day, Easter, etc.) cause 15-25% WoW registration dips
- Post-event weeks typically show Brand registration normalization (-20-30% WoW)


## Agent Configuration
- markets: [MX]
- has_yoy: true
- has_ieccp: true
- headline_extras: [ie%CCP]
- regional_summary: false
- spend_strategy: Maximum weekly spend keeping blended ie%CCP at or below 100%
- projection_notes: Brand follows seasonality, NB adjusted to match efficiency thresholds
