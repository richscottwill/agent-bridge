<!-- DOC-0393 | duck_id: testing-2023-08-jp-app-testing-results -->
---
title: "JP App Testing Results — Apple Search Ads"
status: DRAFT
audience: amazon-internal
level: L5-L7
owner: Richard Williams
created: 2023-09-23
updated: 2026-03-25
update-trigger: "JP app marketing strategy revisited or Apple Search Ads relaunched"
tags: [experiment, japan, apple-search-ads, mobile-app, registrations]
type: reference
summary: "JP Apple Search Ads test (Aug-Sep 2023). $2,708 spend drove +189% unique impressions and +82% downloads. App regs +12% PoP vs flat market, but YoY trend suggests seasonality, not incrementality. Recommendation: conclude testing."
---

# JP App Testing Results — Apple Search Ads

## Approach

Apple Search Ads were launched on August 1st, 2023, to test performance marketing for the mobile app channel in the JP market. The primary goal was to acquire new registrants. We tested whether driving incremental traffic via Apple Search Ads to our AB mobile app page would increase registrants for the channel in JP. Market-level registrants were used as a measure of success because mobile app is currently unable to attribute registrations to marketing activity at a granular level.

## Results

From August 1–September 23 we spent $2,708 and drove 83k impressions, 759 taps, and 142 installs (0.92% tap-through rate, 19% CVR, $19 cost per download).

### Period-over-Period Comparison

JP app registrations increased 12% PoP (weeks 31-38 vs weeks 23-30), while the JP market overall was flat (-0.4%).

**So what:** The +12% app registration lift against a flat market looks promising on the surface, but the absolute numbers are small — roughly 18-20 app registrations per week, meaning the 12% lift represents approximately 2 additional registrations per week. At $2,708 total spend, the cost per incremental registration (if we attribute the full lift to marketing) would be approximately $340. More importantly, the YoY comparison undermines the incrementality claim: JP app registrations were +13% YoY during the test period, but the app channel was already trending at -19% YoY in the comparison period and -22% in the pre-test period. The improvement may reflect seasonal patterns rather than marketing impact.

### Cross-Channel Comparison

The JP app channel's registrations increased by 12% PoP, while the JP market overall was flat. YoY, JP app channel registrations increased 13%, with the overall market decreasing 13% PoP. The mobile app channel registration volume is -19% YoY in the test period, and -22% in the comparison period.

### Cross-Market Comparison

Mobile app channel registrations in JP performed better during this period than other markets: +15% JP, -11% US, +6% EU5, +4% CA. JP was the only market with app registrations from the prior year, so YoY data was unavailable for other markets to account for seasonality.

### Platform Data

| Metric | JP | US (comparison) |
| --- | --- | --- |
| Unique Impressions PoP | +189% | -2% |
| Unique Downloads PoP | +82% | -30% |

**So what:** The +189% unique impressions and +82% unique downloads in JP (vs -2% and -30% in the US during the same period) confirm that Apple Search Ads drove incremental app visibility and installs. The marketing activity clearly increased top-of-funnel metrics. The disconnect is between downloads and registrations — the funnel from app install to AB registration is where the signal breaks down.

| Platform KPI Summary | JP (Pre-test avg, Wk 23-30) | JP (Test period avg, Wk 31-38) | Change |
| --- | --- | --- | --- |
| Avg Weekly Unique Impressions | 20,580 | 59,378 | +189% |
| Avg Weekly Unique Downloads | 2,218 | 4,037 | +82% |
| Avg Weekly DLs/Impression | 0.11 | 0.09 | -20% |

## Recommendations

The recommendation is to conclude testing in JP. What we can definitively say is that Apple Search Ads drive incremental impressions and downloads of the app, but it is difficult to conclude that they drive incremental registrations given the YoY data.

**What should happen next:** The Apple Search Ads budget ($2,708 over ~8 weeks, ~$340/week) should be reallocated to channels with clearer registration attribution. If the mobile app channel develops granular attribution capabilities in the future, app marketing could be revisited with a more rigorous measurement framework. The core limitation is not the channel's potential — it's our inability to connect app installs to registrations at the campaign level.

---

## Appendix A: Registration Comparisons (Summary)

Weekly registration data for 2023 (weeks 23-38) and 2022 (weeks 23-38) across JP channels and cross-market app registrations. Full weekly breakdowns preserved below.

### 2023 PoP Summary (Weeks 31-38 vs Weeks 23-30)

| Channel | PoP Change |
| --- | --- |
| JP Total Regs | -0.4% |
| JP App Regs | +12.4% |
| JP Onsite | -5.0% |
| JP Paid Search | +0.3% |
| JP Free Search | +66.2% |
| JP Email | +77.4% |
| JP Telemarketing | -26.6% |

### 2022 PoP Summary (Weeks 31-38 vs Weeks 23-30, pre-test baseline)

| Channel | PoP Change |
| --- | --- |
| JP Total Regs | -13.4% |
| JP App Regs | +13.0% |
| JP Onsite | -12.4% |
| JP Paid Search | +1.8% |
| JP Free Search | +2.1% |
| JP Email | +13.6% |
| JP Telemarketing | -26.7% |

**So what:** JP app registrations showed a similar PoP pattern in both 2022 (+13.0%) and 2023 (+12.4%) during the same weeks — despite Apple Search Ads only running in 2023. This strongly suggests the +12% lift is seasonal, not marketing-driven. The app channel naturally trends upward in weeks 31-38 regardless of paid activity.

### 2023 Cross-Market App Registrations PoP

| Market | PoP Change |
| --- | --- |
| JP | +14.8% |
| US | -11.0% |
| EU5 | +5.7% |
| CA | +4.1% |

<details>
<summary>Click to expand full weekly registration tables</summary>

#### 2023 Weekly Registrations by Channel (Weeks 23-38)

| Week | JP Total | JP App | JP Onsite | JP PS | JP Free Search | JP Email | JP Telemarketing |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 23 | 3,319 | 21 | 1,071 | 466 | 134 | 402 | 1,095 |
| 24 | 3,383 | 18 | 1,043 | 525 | 158 | 424 | 1,107 |
| 25 | 3,339 | 13 | 1,034 | 546 | 178 | 289 | 1,105 |
| 26 | 3,823 | 18 | 1,230 | 629 | 229 | 298 | 1,072 |
| 27 | 3,646 | 18 | 1,436 | 571 | 196 | 257 | 964 |
| 28 | 4,515 | 26 | 2,106 | 588 | 233 | 329 | 1,032 |
| 29 | 3,370 | 19 | 1,261 | 443 | 185 | 290 | 1,027 |
| 30 | 3,405 | 12 | 1,276 | 461 | 163 | 269 | 1,092 |
| 31 | 3,152 | 18 | 1,250 | 463 | 179 | 252 | 857 |
| 32 | 2,639 | 10 | 956 | 342 | 155 | 407 | 687 |
| 33 | 2,734 | 19 | 1,019 | 363 | 170 | 574 | 482 |
| 34 | 3,346 | 17 | 1,088 | 457 | 227 | 437 | 994 |
| 35 | 3,658 | 20 | 1,226 | 525 | 293 | 634 | 827 |
| 36 | 4,653 | 20 | 1,387 | 594 | 333 | 1,264 | 887 |
| 37 | 4,558 | 27 | 1,588 | 810 | 657 | 461 | 816 |
| 38 | 3,951 | 32 | 1,425 | 687 | 439 | 509 | 684 |

#### 2022 Weekly Registrations by Channel (Weeks 23-38)

| Week | JP Total | JP App | JP Onsite | JP PS | JP Free Search | JP Email | JP Telemarketing |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 23 | 3,071 | 31 | 959 | 345 | 161 | 259 | 1,216 |
| 24 | 3,170 | 18 | 956 | 352 | 178 | 248 | 1,329 |
| 25 | 3,270 | 17 | 979 | 375 | 166 | 246 | 1,420 |
| 26 | 3,320 | 16 | 1,147 | 362 | 176 | 311 | 1,226 |
| 27 | 3,058 | 23 | 1,060 | 341 | 193 | 161 | 1,155 |
| 28 | 3,653 | 25 | 1,257 | 372 | 179 | 401 | 1,331 |
| 29 | 2,480 | 24 | 861 | 285 | 157 | 138 | 949 |
| 30 | 2,928 | 23 | 980 | 316 | 162 | 233 | 1,170 |
| 31 | 2,841 | 22 | 1,010 | 351 | 193 | 243 | 938 |
| 32 | 2,033 | 23 | 773 | 290 | 159 | 126 | 610 |
| 33 | 2,557 | 22 | 832 | 286 | 151 | 356 | 859 |
| 34 | 2,931 | 21 | 858 | 363 | 188 | 352 | 1,090 |
| 35 | 2,774 | 31 | 946 | 368 | 197 | 164 | 1,000 |
| 36 | 2,934 | 24 | 928 | 370 | 184 | 345 | 1,007 |
| 37 | 3,060 | 27 | 948 | 426 | 171 | 376 | 1,035 |
| 38 | 2,485 | 30 | 886 | 343 | 158 | 306 | 645 |

#### 2023 Cross-Market App Registrations (Weeks 23-38)

| Week | CA App | JP App | US App | EU5 App |
| --- | --- | --- | --- | --- |
| 23 | 26 | 21 | 380 | 491 |
| 24 | 23 | 18 | 358 | 483 |
| 25 | 13 | 13 | 350 | 453 |
| 26 | 25 | 18 | 397 | 452 |
| 27 | 22 | 17 | 527 | 595 |
| 28 | 29 | 25 | 464 | 545 |
| 29 | 31 | 18 | 396 | 519 |
| 30 | 26 | 12 | 402 | 449 |
| 31 | 24 | 18 | 339 | 493 |
| 32 | 27 | 10 | 367 | 489 |
| 33 | 19 | 19 | 432 | 450 |
| 34 | 28 | 17 | 386 | 457 |
| 35 | 30 | 20 | 349 | 481 |
| 36 | 23 | 20 | 322 | 647 |
| 37 | 22 | 27 | 358 | 606 |
| 38 | 30 | 32 | 360 | 592 |

</details>

## Appendix B: Platform KPIs

Weekly platform data for unique impressions, downloads, and efficiency ratios across JP, US, and CA.

<details>
<summary>Click to expand full weekly platform KPI tables</summary>

#### Unique Impressions by Market (Weekly)

| Date | CA Unique Imps | JP Unique Imps | US Unique Imps |
| --- | --- | --- | --- |
| 7/3/2023 | 9,379 | 22,670 | 102,684 |
| 7/10/2023 | 11,077 | 24,928 | 117,673 |
| 7/17/2023 | 8,717 | 18,079 | 99,564 |
| 7/24/2023 | 8,603 | 16,644 | 104,775 |
| 7/31/2023 | 8,829 | 40,022 | 106,555 |
| 8/7/2023 | 9,569 | 69,258 | 105,867 |
| 8/14/2023 | 8,882 | 54,511 | 104,210 |
| 8/21/2023 | 8,513 | 73,721 | 99,784 |
| **PoP** | **-5.25%** | **+188.52%** | **-1.95%** |

#### Downloads by Market (Weekly)

| Date | CA Downloads | JP Downloads | US Downloads |
| --- | --- | --- | --- |
| 7/3/2023 | 1,710 | 1,793 | 26,778 |
| 7/10/2023 | 1,660 | 2,146 | 30,241 |
| 7/17/2023 | 1,371 | 2,532 | 18,068 |
| 7/24/2023 | 1,193 | 2,401 | 81,096 |
| 7/31/2023 | 1,058 | 11,793 | 37,183 |
| 8/7/2023 | 1,172 | 1,520 | 28,145 |
| 8/14/2023 | 1,125 | 1,396 | 15,214 |
| 8/21/2023 | 1,049 | 1,437 | 28,291 |
| **PoP** | **-25.78%** | **+81.99%** | **-30.32%** |

</details>

<!-- AGENT_CONTEXT
machine_summary: "JP Apple Search Ads test (Aug-Sep 2023). $2,708 spend drove +189% unique impressions and +82% downloads in JP (vs -2% and -30% in US). App registrations +12% PoP vs flat market, but 2022 showed identical +13% seasonal pattern without paid activity. Recommendation: conclude testing — marketing drives downloads but cannot demonstrate incremental registrations due to attribution limitations."
key_entities: ["Apple Search Ads", "JP mobile app", "AB registrations", "app installs"]
action_verbs: ["test", "measure", "compare", "conclude"]
depends_on: ["2023-01-jp-nb-experiment-google"]
update_triggers: ["JP app marketing strategy revisited", "Mobile app attribution capabilities improved", "Apple Search Ads relaunched in JP"]
key_facts: ["$2,708 total spend over 8 weeks", "+189% unique impressions PoP in JP", "+82% unique downloads PoP in JP", "+12% app registrations PoP (but +13% in 2022 without ads)", "~18-20 app registrations per week (small absolute numbers)", "Recommendation: conclude testing"]
-->
