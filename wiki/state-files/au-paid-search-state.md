---
title: "AU Paid Search — Daily State File"
status: ACTIVE
audience: amazon-internal
owner: Richard Williams
format: Amazon 1-2 Page Narrative (Flash Report)
cadence: Daily refresh
destination: OneDrive Kiro-Drive/state-files/au-paid-search-state.md
created: 2026-04-12
updated: 2026-05-01
data_through: 2026 W15 (Apr 6–12)
---
<!-- DOC-0403 | duck_id: state-file-au-ps -->

# Australia Paid Search — State of the Business

**Reporting period:** Week 15 (Apr 6–12, 2026) · **Market owner:** Richard Williams · **Primary stakeholder:** Lena Zak (L7) · **Execution partner:** Alexis Eck (L6)
**Data through:** AU W15 actuals; MX W15 actuals; WW W15 actuals.

---

## Introduction

This document provides the trailing-week operational state of the Amazon Business Australia Paid Search program. AU is Richard Williams's hands-on market, managed through Google Ads under the DSAP parent MCC. The program launched in June 2025 and operates under a CPA efficiency constraint — no ie%CCP target exists yet because CCP data is not expected until July 2026. FY26 OP2 targets $1.8M budget, 12,906 registrations, and $140 CPA. FY25 (June–December only) delivered $1.14M spend, 8,763 registrations, and $158 CPA. Lena Zak (L7) is the primary stakeholder with three stated priorities: keyword CPC/CPA investigation, keyword-to-product mapping, and Polaris migration. Alexis Eck (L6) is the collaborative execution partner. OCI has no confirmed AU timeline and no MCC has been created. Keyword-level registration data is unavailable until Q3 2026; all Non-Brand keyword analysis is directional.

## Goals

1. Achieve a blended CPA at or below $140 for FY26 (OP2 target), delivering 12,906 registrations on $1.8M budget.
2. Complete the Polaris Brand landing page migration and validate tracking integrity by April 30, 2026.
3. Prepare for OCI — MCC creation, Google Ads account configuration, and conversion signal setup (timeline TBD).
4. Establish a biweekly keyword review cadence with Alexis Eck by April 18, 2026, covering top-20 outlier keywords by CPC/CPA.
5. Pilot the two-campaign structure (product-intent vs business-intent) by May 15, 2026, with a 4-week measurement period before scaling.

## Tenets

1. **CPA efficiency is the primary constraint.** Without ie%CCP data (expected July 2026), CPA at or below $140 is the governing metric. Every spend decision must demonstrate CPA discipline.
2. **Surgical keyword optimization over broad cuts.** Brandon's guidance (3/23 sync): focus on outlier keyword analysis (top 20 by CPC/CPA), not broad keyword removal. CPC caps are a "two-way door" until OCI.
3. **Data-first stakeholder management.** Lena requires numbers. Every response to Lena must include specific data points, trend context, and actionable recommendations. Never send a qualitative-only update.
4. **Phased testing before scale.** The two-campaign structure pilot must run for 4 weeks with a defined success metric before WW consideration. No big-bang restructuring.

---

## State of the Business

AU drove 168 registrations in W15 (-1.2% WoW, -29% vs trailing 8-week average of 236) on $25,829 spend (+17.0% WoW) at a blended CPA of $153.74 (+18.4% WoW). W15 extends the registration decline streak to 7 consecutive weeks and is the lowest weekly output in the trailing 8 weeks. Spend rose while registrations fell, driving a 3-week consecutive CPA increase: $114.77 (W12) → $117.22 (W13) → $129.84 (W14) → $153.74 (W15). The Polaris URL migration tracking issue remains unresolved and is the leading candidate root cause for the sustained CVR compression.

On April 17, Alex VanDerStuyf (MCS) confirmed that Italy's Polaris `/cp/ps-brand` page (launched April 1) routed Italian signup traffic to the AU domain via an incorrect ref tag — a P0 production bug that was detected on April 16 during the Polaris LP sync. Legacy Italy template was restored April 16; the Polaris Italy variant is now parked in AEM as `it/cp/ps-brand-new`. This is an Italy-to-AU routing issue, not an AU page issue, but it is an additional indicator that the Polaris template rollout has introduced ref tag regressions that require systematic verification before AU's tracking can be treated as clean.

**Input metrics (controllable levers):**

| Input Metric | W15 Value | WoW Δ | Trend |
|---|---|---|---|
| Total spend | $25,829 | +17.0% | Reversed W14 decline; highest since W11 |
| Brand CVR | 6.08% | -10.6% | Below 8-week avg of 7.46% |
| NB CVR | 1.99% | +6.4% | 27% below 8-week average of 2.74% |
| NB CPC | $4.77 | -0.8% | 15% below 8-week average of $5.61 |
| Max-clicks bid strategy | Live 4/17 | — | Carried forward from Friday handover; Monday check pending |

**Output metrics (lagging results):**

| Output Metric | W15 Value | WoW Δ | vs OP2 Run Rate |
|---|---|---|---|
| Total registrations | 168 | -1.2% | 32% below 248/wk needed for 12,906 FY26 |
| Brand registrations | 77 | -19.8% | Lowest in trailing 8 weeks |
| NB registrations | 91 | +23.0% | Recovered from W14 low of 74 |
| Blended CPA | $153.74 | +18.4% | $13.74 above $140 OP2 target |
| Brand CPA | $52.59 | +17.5% | Above $35–$45 stability band |
| NB CPA | $239.34 | -0.4% | Roughly flat vs W14 |
| Brand spend | $4,049 | -5.7% | Continuing spend discipline |
| NB spend | $21,780 | +22.5% | NB absorbed the spend increase |

The W15 pattern differs from W14: Brand and NB moved in opposite directions. Brand registrations dropped -19.8% on -5.7% spend — a CVR problem (6.08% vs 7.15% W14). NB registrations rose +23.0% on +22.5% spend — volume recovery on nearly flat CPA. The NB CPC decline streak held at $4.77, confirming Brandon's surgical-not-broad keyword approach continues to suppress cost per click without eroding CPA because CVR also softened.

**April MTD (through W15):** 168 registrations and $25,829 spend against OP2 month targets of 1,071 regs and $147,592 spend — 15.7% pacing on registrations and 17.5% pacing on cost at 19% of the month elapsed. Week 1 of April captured only one week of data; April pacing will be reassessed at W16.

<!-- WBR-OWNED:prediction-scoring START -->
<!-- WBR-OWNED:prediction-scoring END -->

<!-- WBR-OWNED:forecast START -->
**W16 forecast (Bayesian seasonal brand/NB split, forecast date 2026-04-15):** 207 registrations (CI 188–288), $26,396 spend, $115 CPA. The forecast assumes a post-Easter recovery pattern consistent with April 2025, with brand CVR recovering toward the 8-week average of 7.46%. If actual W16 registrations fall below the CI low of 188, the Polaris tracking hypothesis upgrades from candidate root cause to confirmed driver.
<!-- WBR-OWNED:forecast END -->

No YoY comparison is available — AU launched in June 2025. The earliest YoY data will be available in June 2026.

## Flags

<!-- AM-OWNED:trailing-week-flags START -->
4 anomalies detected (>20% deviation from 8-week average):

| Metric | W15 Value | 8-Week Avg | Deviation | Implication |
|---|---|---|---|---|
| Registrations | 168 | 236 | -29% | 7-week decline streak confirmed |
| Brand registrations | 77 | 104 | -26% | Brand-side contribution weakening |
| NB CVR | 1.99% | 2.74% | -27% | 5th consecutive week below baseline 2.5%–3.5% |
| Brand CPA | $52.59 | $45.88 | +15% | Above $35–$45 stability band |

**Recommended action:** Do not treat the W15 regression as proof of structural decline without first validating Polaris tracking. Brand CVR is the highest-signal metric to monitor post-tracking-fix because Brand CVR is the least-dependent on market demand fluctuation. If Brand CVR returns to 7.0%+ within 7 days of tracking validation, the decline is resolvable; if it does not, structural keyword or LP investigation is required.

**Cost of inaction (null case):** If the Polaris URL migration tracking is not validated within the next 7 days, 3 consecutive weeks of CVR data will remain ambiguous — the team cannot distinguish genuine demand softness from a tracking artifact. At the current W15 run rate of 168 registrations per week, AU would deliver approximately 8,736 FY26 registrations — 32% below the 12,906 OP2 target and $600K below the $1.8M budget plan. Separately, OCI has no confirmed AU timeline and no MCC has been created. Every quarter without OCI forgoes the 18–24% registration uplift observed in comparable OCI markets (US +24%, UK +23%, DE +18%). At AU's current 168 regs/week baseline, a 20% OCI uplift would add approximately 34 registrations per week — 1,768 annualized registrations worth approximately $271K at $153 CPA.
<!-- AM-OWNED:trailing-week-flags END -->

<!-- WBR-OWNED:signal-flags START -->
<!-- WBR-OWNED:signal-flags END -->

---

## Lessons Learned

Three operational insights from the trailing four-week window (W12–W15) inform the immediate tactical posture:

1. **The Polaris URL migration remains the most likely cause of the CVR collapse, and April 16 Polaris LP optimization sync reinforced this hypothesis with an Italy ref tag regression as corroborating evidence.** W15 Brand CVR at 6.08% is the lowest in the trailing 8 weeks and -18% below the 8-week average of 7.46%. The April 16 meeting revealed that Italy's Polaris LP overwrote the market's ref tag, routing Italian signup traffic to the AU domain — a confirmed production failure. AU's own Polaris LP has not been subjected to the same ref tag audit. Until the audit is complete, Brand CVR degradation cannot be attributed to any specific driver. Validation is not optional — it is the precondition for every other AU optimization.

2. **NB CPC's 8-week decline streak (from $6.53 in W8 to $4.77 in W15, -27% total) continues to hold, but NB CPA is locked at elevated levels because NB CVR remains 27% below the 8-week average.** NB CPA in W15 is $239.34, nearly identical to W14's $240.26, and still 43% above the $140 OP2 blended target. The CPC decline has delivered the efficiency Brandon requested on March 23, but CVR recovery is the gating factor for translating CPC gains into CPA improvement. If NB CVR recovers to the baseline range of 2.5%–3.5%, NB CPA mechanically drops to $170–$200 at current CPC levels.

3. **The W15 NB registration rebound from 74 to 91 on similar CPC suggests demand is not the structural issue.** NB clicks volume rose in W15, NB CVR recovered modestly from 1.87% to 1.99%, and NB registrations grew +23.0% WoW. This pattern indicates that the NB funnel can absorb additional traffic productively when CVR cooperates. The Brand-side weakness (CVR -10.6% WoW, registrations -19.8% WoW) is a distinct problem — one that aligns with the Polaris LP migration timing. Treating AU's decline as a unified story is incorrect; the Brand and NB dynamics are now diverging and require separate diagnostics.

---

## Strategic Priorities

**Next 24–48 hours:**

| Priority | Action | Owner | Deadline | Goal Link |
|---|---|---|---|---|
| 1 | Audit AU Polaris `/cp/ps-brand` page for ref tag integrity — apply the Italy-detection method from April 16 Polaris sync | Richard + Alex VanDerStuyf | Apr 22 | Goal 2, Tenet 1 |
| 2 | Check AU account post-4/17 max-clicks bid strategy switch — validate W16 CPC/CVR trajectory | Richard | Apr 20 | Goal 1 |
| 3 | Respond to Lena — AU LP URL analysis + CPA methodology (draft written Apr 3, 17 days overdue) | Richard | Apr 21 | Tenet 3 |
| 4 | Complete refmarker mapping audit PoC — AU (Brandon assigned, 10 days overdue) | Richard | Apr 22 | Goal 2 |
| 5 | Initiate OCI MCC creation for AU — required for any future launch | Richard + Brandon | Apr 22 | Goal 3 |
| 6 | AU meetings agenda for Tuesday 4:30pm PT sync with Lena/Alexis | Richard | Apr 21 | Tenet 3 |

**Blocked items:**
- OCI MCC: Not created. Cannot begin Google Ads account setup or conversion signal configuration until MCC exists. Blocks any AU OCI launch.
- Keyword-level registration data: Unavailable until Q3 2026. All NB keyword analysis remains directional. Blocks precise keyword-to-registration attribution.
- ie%CCP target: CCP data not expected until July 2026. AU operates on CPA constraint only until then.
- Polaris ref tag audit: AU page not yet validated after Italy regression discovered April 16. Blocks attribution confidence for all W14–W15 data.

**Stakeholder actions required:**
- Lena: Biweekly keyword review cadence and two-campaign structure pilot scope confirmation still pending from March discussion.
- Alexis: Friday handover (switched to max-clicks 4/17) confirmed; AU account check today.
- Brandon: Approve OCI MCC creation request for AU. Forward Polaris template change-requests email to Dwayne (pending from 4/17 DM request).
- Alex VanDerStuyf (MCS): Extend Italy ref tag audit methodology to AU Polaris page.
- MarTech: Validate Polaris conversion tag implementation post-migration.

---

## Appendix A: Weekly Trend (W8–W15)

| Week | Regs | Brand | NB | Spend | CPA | NB CPA | NB CVR | NB CPC |
|---|---|---|---|---|---|---|---|---|
| W8 | 256 | 94 | 162 | $37,196 | $145.30 | $198.13 | 3.29% | $6.53 |
| W9 | 256 | 121 | 135 | $36,408 | $142.22 | $223.68 | 2.84% | $6.36 |
| W10 | 251 | 111 | 140 | $31,589 | $125.85 | $189.14 | 3.08% | $5.83 |
| W11 | 241 | 108 | 133 | $30,999 | $128.63 | $198.41 | 2.79% | $5.53 |
| W12 | 244 | 119 | 125 | $28,005 | $114.77 | $188.51 | 2.85% | $5.37 |
| W13 | 208 | 98 | 110 | $24,381 | $117.22 | $184.99 | 2.60% | $4.81 |
| W14 | 170 | 96 | 74 | $22,074 | $129.84 | $240.26 | 1.87% | $4.50 |
| W15 | 168 | 77 | 91 | $25,829 | $153.74 | $239.34 | 1.99% | $4.77 |

**7-week decline streak:** W8 (256) → W9 (256) → W10 (251) → W11 (241) → W12 (244) → W13 (208) → W14 (170) → W15 (168). Cumulative decline: -34% from W8. NB CPC 8-week decline: $6.53 → $4.77, -27% cumulative.

## Appendix B: YoY Comparison

No YoY data available. AU Paid Search launched June 2025. First YoY comparison will be available June 2026.

## Appendix C: April 2026 Monthly Projection

| Metric | MTD (Apr 1–12) | OP2 Month Target | MTD Pacing | W16 Forecast |
|---|---|---|---|---|
| Registrations | 168 | 1,071 | 15.7% at 19% elapsed | 207 (CI 188–288) |
| Spend | $25,829 | $147,592 | 17.5% at 19% elapsed | $26,396 |
| CPA | $153.74 | $138 | +11% above target | $115 (forecast) |

MTD data reflects only W15 (Apr 6–12). Pacing will be reassessed at W16. The W16 forecast assumes a post-Easter recovery pattern consistent with April 2025.

## Appendix D: FY26 Plan Summary

| Metric | FY25 Actual (Jun–Dec) | FY26 OP2 | Run Rate (W15) |
|---|---|---|---|
| Total spend | $1.14M | $1.8M | $1.34M annualized |
| Total registrations | 8,763 | 12,906 | 8,736 annualized |
| Blended CPA | $158 | $140 | $154 |

At the W15 run rate, AU would deliver approximately 8,736 registrations on $1.34M spend at $154 CPA — 32% below the OP2 registration target and $13 above the CPA target. The volume gap has widened versus the W14 snapshot (from -31% to -32%). OCI (projected +18–24% uplift) and Polaris tracking validation remain the two highest-leverage interventions to close the volume gap.

## Appendix E: Change Log (2026 YTD)

| Date | Change | Owner |
|---|---|---|
| 1/12 | Adjusted bid strategies across Brand and NB campaigns | Richard |
| 1/20 | Increased Brand max CPC targets | Richard |
| 1/27 | Added negative keywords to NB campaigns | Richard |
| 2/3 | Transitioned NB to portfolio bid strategy | Richard |
| 2/10 | Adjusted NB budget allocation (-10%) | Richard |
| 2/17 | Added negative keywords (Brand Exact routing) | Richard |
| 2/24 | Increased Brand Phrase budget +15% | Richard |
| 3/1 | Polaris Brand LP migration initiated | Richard |
| 3/5 | Completed mid-week Polaris URL migration | Richard |
| 3/5 | Applied CPC caps to top-20 NB outlier keywords | Richard |
| 4/16 | Italy Polaris ref tag regression detected (routed IT traffic to AU domain); AU page integrity check opened | MCS + Richard |
| 4/17 | Switched AU to max-clicks bid strategy; handover from Alexis | Richard + Alexis |

## Appendix F: Variance Bridge — Data Source Reconciliation

AU currently operates without OCI (Online Conversion Integration). All conversion data flows through Google Ads native tracking. No variance bridge between advertising platform and internal ERP is required at this time. When OCI launches for AU, this section will document the expected 5–15% discrepancy between Ordered Product Sales and Shipped Product Sales, and the reconciliation methodology.

**Known data limitations:**
- ie%CCP: Not available. CCP data expected July 2026. AU operates on CPA constraint only.
- Keyword-level registrations: Unavailable until Q3 2026. All NB keyword analysis is directional.
- YoY comparison: Not available until June 2026 (AU launched June 2025).
- Polaris tracking integrity: Unvalidated post-migration. W13 daily pattern suggests potential tracking disruption.

---

## Appendix H: Placeholder Schema for Automated Refresh

This schema defines the contract between the Kiro agent swarm (LLM output) and the DOCX template (deterministic patching). The agent generates a JSON payload mapping these keys to generated strings. A patching script replaces the placeholders in the Word XML without touching surrounding formatting.

| Placeholder Tag | Section | Data Source | Update Cadence |
|---|---|---|---|
| `{{REPORTING_PERIOD}}` | Header | Calendar + dashboard week | Weekly |
| `{{INTRO_PARAGRAPH}}` | Introduction | Semi-static; update on stakeholder/structural changes | Monthly |
| `{{SOTB_PARAGRAPH_1}}` | State of Business — headline | Weekly metrics JSON | Weekly |
| `{{SOTB_INPUT_TABLE}}` | State of Business — input metrics | Weekly metrics JSON | Weekly |
| `{{SOTB_OUTPUT_TABLE}}` | State of Business — output metrics | Weekly metrics JSON | Weekly |
| `{{SOTB_ANALYSIS}}` | State of Business — narrative bridge | LLM synthesis of input→output causation | Weekly |
| `{{SOTB_ANOMALY_FLAG}}` | State of Business — anomaly detection | Anomaly engine (>20% deviation from 8wk avg) | Weekly |
| `{{SOTB_NULL_CASE}}` | State of Business — cost of inaction | CPA model + OCI readiness constraints | Weekly |
| `{{SOTB_FLAGS}}` | State of Business — conditional flags | Anomaly engine; only present during anomalous weeks | Conditional |
| `{{LESSONS_1}}` | Lessons Learned — insight 1 | LLM synthesis of trailing 3-week window | Weekly |
| `{{LESSONS_2}}` | Lessons Learned — insight 2 | LLM synthesis | Weekly |
| `{{LESSONS_3}}` | Lessons Learned — insight 3 | LLM synthesis | Weekly |
| `{{PRIORITIES_TABLE}}` | Strategic Priorities — action table | Asana tasks + overdue items + calendar | Daily |
| `{{BLOCKED_ITEMS}}` | Strategic Priorities — blockers | Asana blocked tasks | Daily |
| `{{STAKEHOLDER_ACTIONS}}` | Strategic Priorities — external deps | Memory.md relationship graph + Asana | Daily |
| `{{APPENDIX_A_TREND}}` | Appendix A — weekly trend table | DuckDB weekly_metrics | Weekly |
| `{{APPENDIX_C_PROJECTION}}` | Appendix C — monthly projection | Analyst projection model | Weekly |
| `{{APPENDIX_E_CHANGELOG}}` | Appendix E — change log | DuckDB change_log table | On change |

### JSON Output Contract

```json
{
  "REPORTING_PERIOD": "Week 15 (Apr 5–11, 2026)",
  "SOTB_PARAGRAPH_1": "AU drove 185 registrations...",
  "SOTB_INPUT_TABLE": "[markdown table string]",
  "SOTB_OUTPUT_TABLE": "[markdown table string]",
  "SOTB_ANALYSIS": "The W15 registration change was...",
  "SOTB_ANOMALY_FLAG": "NB CVR at 37% below trailing average.",
  "SOTB_NULL_CASE": "If Polaris tracking is not validated...",
  "SOTB_FLAGS": "[conditional — only present if anomalies detected]",
  "LESSONS_1": "First insight...",
  "LESSONS_2": "Second insight...",
  "LESSONS_3": "Third insight...",
  "PRIORITIES_TABLE": "[markdown table string]",
  "BLOCKED_ITEMS": "[markdown list]",
  "STAKEHOLDER_ACTIONS": "[markdown list]"
}
```

Static sections (Goals, Tenets, Appendix B/D) are NOT in the JSON — they persist unchanged in the template until manually revised.

---

## Appendix G: Source Links

All source documents referenced in or feeding this state file. Links open in browser.

### Kiro-Drive (OneDrive)

| Document | Purpose | Link |
|---|---|---|
| ps-forecast-tracker.xlsx | WW PS forecast model, budget scenarios | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Kiro-Drive/ps-forecast-tracker.xlsx?web=1) |
| ps-testing-dashboard.xlsx | Active test tracker across all markets | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Kiro-Drive/ps-testing-dashboard.xlsx?web=1) |
| command-center.xlsx | Operational command center — tasks, status, owners | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Kiro-Drive/command-center.xlsx?web=1) |

### Artifacts — AU Callouts & Analysis (OneDrive)

| Document | Period | Link |
|---|---|---|
| au-2026-w14.docx | W14 callout | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Artifacts/markets/abix/au/au-2026-w14.docx?web=1) |
| au-2026-w13.docx | W13 callout | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Artifacts/markets/abix/au/au-2026-w13.docx?web=1) |
| au-2026-w12.docx | W12 callout | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Artifacts/markets/abix/au/au-2026-w12.docx?web=1) |
| au-2026-w11.docx | W11 callout | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Artifacts/markets/abix/au/au-2026-w11.docx?web=1) |
| au-analysis-2026-w13.docx | W13 deep analysis | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Artifacts/markets/abix/au/au-analysis-2026-w13.docx?web=1) |
| au-analysis-2026-w12.docx | W12 deep analysis | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Artifacts/markets/abix/au/au-analysis-2026-w12.docx?web=1) |
| au-data-brief-2026-w14.docx | W14 data brief | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Artifacts/markets/abix/au/au-data-brief-2026-w14.docx?web=1) |
| au-data-brief-2026-w13.docx | W13 data brief | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Artifacts/markets/abix/au/au-data-brief-2026-w13.docx?web=1) |
| au-data-brief-2026-w12.docx | W12 data brief | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Artifacts/markets/abix/au/au-data-brief-2026-w12.docx?web=1) |
| au-change-log.docx | 2026 YTD change log | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Artifacts/markets/abix/au/au-change-log.docx?web=1) |
| au-context.docx | AU market context doc | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Artifacts/markets/abix/au/au-context.docx?web=1) |
| au-projections.docx | Monthly projections tracker | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Artifacts/markets/abix/au/au-projections.docx?web=1) |

### Quip Documents

| Document | Purpose | Link |
|---|---|---|
| 2026 AU Testing | AU testing tracker | [Open](https://quip-amazon.com/IAJ9AAZJsDL) |
| AU PS Launch | AU PS launch planning | [Open](https://quip-amazon.com/JMZ9AAput1I) |
| AU PS Weekly Performance | Weekly performance tracker | [Open](https://quip-amazon.com/ZZR9AAs7OfO) |
| Pre-WBR Callouts | WBR callout working doc | [Open](https://quip-amazon.com/MMgBAzDrlVou) |

### SharePoint Team Sites

| Document | Purpose | Link |
|---|---|---|
| AB AU MBR January 2026 | AU Monthly Business Review (Lena) | [Open](https://amazon.sharepoint.com/sites/ABIX/Shared%20Documents/ABAU/AB%20AU%20MBR/AB%20AU%20MBR%20January%202026.pdf) |
| AB AU WBR Deck W10 | AU Weekly Business Review W10 | [Open](https://amazon.sharepoint.com/sites/ABIX/Shared%20Documents/ABAU/AB%20AU%20WBR/AB%20AU%20WBR%20Deck(WK-10-2026).docx) |
| AB AU Q4 2025 QBR | AU Quarterly Business Review Q4 2025 | [Open](https://amazon.sharepoint.com/sites/ABIX/Shared%20Documents/ABAU/AB%20AU%20QBR/AB_AU_Q42025_QBR.docx) |
| AB AU Q3 2025 QBR | AU Quarterly Business Review Q3 2025 | [Open](https://amazon.sharepoint.com/sites/ABIX/Shared%20Documents/ABAU/AB%20AU%20QBR/AB_AU_Q32025_QBR.docx) |
| AB AU Marketing Strategy | AU Marketing offsite strategy | [Open](https://amazon.sharepoint.com/sites/ABIX/Shared%20Documents/ABAU/GTM/Marketing%20GTM/AB_AU_MarOffsite_Marketing_v6.docx) |
| AB EE Marketing Framework | Emerging Expansion marketing collaboration | [Open](https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/Downloads/AB%20Emerging%20Expansion%20(EE)%20Marketing%20Collaboration%20Framework-1-19.docx) |

---

*This document is designed for daily automated refresh via the Kiro agent swarm. Sections marked with placeholder tags in the DOCX template version are populated by the LLM output JSON and patched into the Word file via deterministic XML injection. The narrative sections above represent the current human-authored baseline that the agent will maintain and update as new weekly data arrives.*

*Template location: OneDrive Kiro-Drive/state-files/au-paid-search-state.md*

---

## Recent signal

### 2026-05-01 — weekly enrichment

- AU Paid Search is transitioning from Richard Williams to Megan Oshry's team. Brandon confirmed the move in Hedy on 4/29, and the AU Transition doc has completed its feedback cycle (Brandon asked Richard to review his comments on 5/1). Alexis Eck is leaving the AU role; Richard is setting up new PTR access for the incoming team.
- Brandon raised a pointed concern about the transition's measurability: the test of "dedicated person vs. time split 5 ways" lacks a clean counterfactual, and he has escalated this framing issue to Kate.
- Megan's team is ramping up on AU data access. Megan asked for the Google Ads conversion data pipeline and the registration query. Richard confirmed AU uses database registration data (not Google Ads platform conversions), consistent with the data limitations documented in Appendix F.
- The AU Transition doc feedback loop is now closed on Brandon's side. Richard's review is the remaining open action before the transition plan finalizes.
