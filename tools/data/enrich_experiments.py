#!/usr/bin/env python3
"""Enrich experiments table from quip-mirror testing docs."""
import duckdb
from datetime import datetime

DB = '/home/prichwil/shared/data/duckdb/ps-analytics.duckdb'

experiments = [
    # === INCREMENTALITY / MEASUREMENT ===
    {
        "experiment_id": "syrt-rct-us-nb",
        "name": "SyRT RCT: US NB Incrementality",
        "hypothesis": "US NB paid search keywords drive incremental AB registrations beyond organic",
        "start_date": "2025-03-28",
        "end_date": "2025-05-01",
        "status": "completed",
        "result": "+16.4% statistically significant lift on AB registrations. 82-92% incremental. 24.9K reg loss during test offset by Q1 overperformance.",
        "metric_before": None,
        "metric_after": 16.4,
        "effect_size": 16.4,
        "decision": "NB PS confirmed high incrementality. Continue investment.",
        "market": "US",
        "category": "incrementality",
        "quip_source": "UCa9AAcbP8I"
    },
    {
        "experiment_id": "syrt-rct-uk",
        "name": "SyRT RCT: UK Incrementality",
        "hypothesis": "UK NB paid search keywords drive incremental AB registrations",
        "start_date": "2025-06-01",
        "end_date": "2025-08-01",
        "status": "completed",
        "result": "Neither NB nor Brand significant. NB directionally positive. Tested in summer to reduce impact.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": None,
        "decision": "Inconclusive. NB directionally positive but not stat sig.",
        "market": "UK",
        "category": "incrementality",
        "quip_source": "UCa9AAcbP8I"
    },
    {
        "experiment_id": "google-causal-brand",
        "name": "Google Causal Analysis: Brand Search Lift",
        "hypothesis": "NB ads drive branded search queries",
        "start_date": None,
        "end_date": None,
        "status": "completed",
        "result": "+3% branded searches where NB ads present. 57% of clicks went to competitors when brand ads absent.",
        "metric_before": None,
        "metric_after": 3.0,
        "effect_size": 3.0,
        "decision": "Brand defense confirmed. Absence of brand ads loses 57% clicks to competitors.",
        "market": "US",
        "category": "incrementality",
        "quip_source": "NQA9AAX2DOp"
    },

    # === OCI (Offline Conversion Import) ===
    {
        "experiment_id": "oci-us-nb-rollout",
        "name": "OCI: US NB Phased Rollout",
        "hypothesis": "OCI bidding on offline conversions improves NB CPA and reg volume",
        "start_date": "2025-07-01",
        "end_date": "2025-09-01",
        "status": "completed",
        "result": "+24% reg lift. ~50% NB CPA improvement. 100% NB rolled out by Sep 2025.",
        "metric_before": None,
        "metric_after": 24.0,
        "effect_size": 24.0,
        "decision": "Full rollout. OCI is the single largest performance lever.",
        "market": "US",
        "category": "oci",
        "quip_source": "dSZ9AAZBXQy"
    },
    {
        "experiment_id": "oci-uk-rollout",
        "name": "OCI: UK Rollout",
        "hypothesis": "OCI bidding improves UK NB performance",
        "start_date": "2025-08-01",
        "end_date": "2025-09-01",
        "status": "completed",
        "result": "+23% reg lift. Significant CPA improvement. 100% by Sep 2025.",
        "metric_before": None,
        "metric_after": 23.0,
        "effect_size": 23.0,
        "decision": "Full rollout. Mature and stable.",
        "market": "UK",
        "category": "oci",
        "quip_source": "dSZ9AAZBXQy"
    },
    {
        "experiment_id": "oci-de-rollout",
        "name": "OCI: DE Rollout",
        "hypothesis": "OCI bidding improves DE NB performance",
        "start_date": "2025-11-01",
        "end_date": "2025-12-01",
        "status": "completed",
        "result": "+18% reg lift. Significant CPA improvement. 100% by Dec 2025.",
        "metric_before": None,
        "metric_after": 18.0,
        "effect_size": 18.0,
        "decision": "Full rollout. Live and stable.",
        "market": "DE",
        "category": "oci",
        "quip_source": "dSZ9AAZBXQy"
    },
    {
        "experiment_id": "oci-eu3-rollout",
        "name": "OCI: EU3 (FR/IT/ES) Rollout",
        "hypothesis": "OCI bidding improves EU3 NB performance",
        "start_date": "2026-02-01",
        "end_date": None,
        "status": "in_progress",
        "result": "E2E launched 2/26. Data exclusions applied 3/23-3/31. Full impact expected Jul 2026.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": None,
        "decision": "In progress. Monitoring ramp.",
        "market": "EU3",
        "category": "oci",
        "quip_source": "Zee9AAlSBEB"
    },
    {
        "experiment_id": "oci-ca-rollout",
        "name": "OCI: CA Rollout",
        "hypothesis": "OCI bidding improves CA NB performance",
        "start_date": "2026-03-01",
        "end_date": None,
        "status": "in_progress",
        "result": "E2E launched 3/4. ADB bidding exclusions applied. Campaign-level tracking test 3/4. Full impact expected Jul 2026.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": None,
        "decision": "In progress. Monitoring ramp.",
        "market": "CA",
        "category": "oci",
        "quip_source": "Zee9AAlSBEB"
    },
    {
        "experiment_id": "oci-jp-rollout",
        "name": "OCI: JP Rollout",
        "hypothesis": "OCI bidding improves JP NB performance",
        "start_date": "2026-02-01",
        "end_date": None,
        "status": "in_progress",
        "result": "E2E launched 2/26. Full impact expected Jul 2026.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": None,
        "decision": "In progress. Monitoring ramp.",
        "market": "JP",
        "category": "oci",
        "quip_source": "Zee9AAlSBEB"
    },

    # === AD COPY ===
    {
        "experiment_id": "ad-copy-uk-sole-prop",
        "name": "Ad Copy: UK Sole Proprietor Messaging",
        "hypothesis": "Value/price/selection messaging outperforms bulk/wholesale for sole proprietors",
        "start_date": "2025-10-01",
        "end_date": "2025-12-16",
        "status": "completed",
        "result": "UK AMZ portfolio: +86% CTR, +31% regs after update. Evidence-based from AB Sole Proprietor study.",
        "metric_before": None,
        "metric_after": 86.0,
        "effect_size": 86.0,
        "decision": "Rolled out WW. EU4 translations completed. Phase 2 launched UK 3/6.",
        "market": "UK",
        "category": "ad_copy",
        "quip_source": "KCY9AAYqWd2"
    },
    {
        "experiment_id": "ad-copy-uk-phase2",
        "name": "Ad Copy: UK NB Phase 2",
        "hypothesis": "Extending ad copy optimization across all NB campaigns improves performance",
        "start_date": "2026-03-06",
        "end_date": None,
        "status": "in_progress",
        "result": "Launched across all NB. Paused all Poor and Average performing ads.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": None,
        "decision": "Monitoring. CVR at 12-week high (4.28%).",
        "market": "UK",
        "category": "ad_copy",
        "quip_source": "KCY9AAYqWd2"
    },
    {
        "experiment_id": "rsa-google-rewrite",
        "name": "RSA: Google Auto-Rewrite Test",
        "hypothesis": "Google RSA rewrites improve ad performance",
        "start_date": None,
        "end_date": None,
        "status": "completed",
        "result": "638 RSAs rewritten. $137.68 CPA vs $145 account avg. +56% impressions, +57% clicks from RSA optimization.",
        "metric_before": 145.0,
        "metric_after": 137.68,
        "effect_size": -5.0,
        "decision": "Positive. RSA optimization drives volume at lower CPA.",
        "market": "US",
        "category": "ad_copy",
        "quip_source": "ReG9AAvZFTS"
    },

    # === BIDDING ===
    {
        "experiment_id": "amo-vs-google-bidding",
        "name": "Bidding: AMO vs Google Smart Bidding",
        "hypothesis": "Google Smart Bidding outperforms AMO due to more signals (location, time of day)",
        "start_date": "2022-01-01",
        "end_date": "2022-12-31",
        "status": "completed",
        "result": "+8% to +101% uplift across 5 portfolio sets WW. Google uses more signals.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": 50.0,
        "decision": "Google Smart Bidding preferred over AMO for most portfolios.",
        "market": "WW",
        "category": "bidding",
        "quip_source": "ePH9AAU0wIA"
    },
    {
        "experiment_id": "eu5-bidding-restructure",
        "name": "Bidding: EU5 Dec 2023 Restructure",
        "hypothesis": "Consolidating EU5 campaigns and switching Brand to IS bidding improves efficiency",
        "start_date": "2023-12-01",
        "end_date": "2023-12-28",
        "status": "completed",
        "result": "AMZ→Max Conv, GA Product/Vertical combined, Generic consolidated, RLSA merged. DE Brand CPA increased due to IS focus — reverted.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": None,
        "decision": "Mixed. IS bidding for Brand caused CPA increase in DE — reverted. Other consolidations kept.",
        "market": "EU5",
        "category": "bidding",
        "quip_source": "dSM9AAaMwDD"
    },
    {
        "experiment_id": "it-bid-modifiers",
        "name": "Bidding: IT City-Level Bid Modifiers",
        "hypothesis": "Adding bid modifiers to NB campaigns for 24 largest IT cities improves performance",
        "start_date": "2024-11-14",
        "end_date": "2024-12-12",
        "status": "completed",
        "result": "+18% Registrations, +7% CVR, +2% CPA. Bayesian PPR: 83.4% (Amazon threshold: 66%).",
        "metric_before": 5.3,
        "metric_after": 5.7,
        "effect_size": 7.0,
        "decision": "Positive. City-level modifiers drive incremental regs at marginal CPA increase.",
        "market": "IT",
        "category": "bidding",
        "quip_source": "LJb9AAugth6"
    },
    {
        "experiment_id": "jp-brand-cpc-cap",
        "name": "Bidding: JP Brand CPC Cap Reduction",
        "hypothesis": "Lowering Brand CPC cap from $55 to $10 reduces cost without significant reg loss",
        "start_date": "2025-01-01",
        "end_date": "2025-02-01",
        "status": "completed",
        "result": "-26% CPC, -29% CPA, only -3% regs.",
        "metric_before": 55.0,
        "metric_after": 10.0,
        "effect_size": -29.0,
        "decision": "Positive. Significant cost savings with minimal reg impact.",
        "market": "JP",
        "category": "bidding",
        "quip_source": "AeG9AAmSPdu"
    },
    {
        "experiment_id": "jp-adobe-to-manual",
        "name": "Bidding: JP Adobe→Manual CPC for Brand_Phrase_D",
        "hypothesis": "Manual CPC outperforms Adobe bidding for low-volume JP Brand campaigns",
        "start_date": "2025-02-12",
        "end_date": None,
        "status": "completed",
        "result": "-41% cost, -37% CPA ($829→$493).",
        "metric_before": 829.0,
        "metric_after": 493.0,
        "effect_size": -40.5,
        "decision": "Manual CPC wins for low-volume JP Brand. Adobe overbids.",
        "market": "JP",
        "category": "bidding",
        "quip_source": "AeG9AAmSPdu"
    },
    {
        "experiment_id": "au-adobe-bid-strategy",
        "name": "Bidding: AU Adobe Bid Strategy Transition",
        "hypothesis": "Adobe bid strategy improves AU performance vs manual pacing",
        "start_date": "2026-01-16",
        "end_date": None,
        "status": "in_progress",
        "result": "Brand Plus test started 1/16, full rollout 1/20. Same weekly budget pacing.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": None,
        "decision": "Monitoring. Part of AU operational maturity.",
        "market": "AU",
        "category": "bidding",
        "quip_source": "ZZR9AAs7OfO"
    },

    # === LANDING PAGES ===
    {
        "experiment_id": "polaris-brand-lp-us",
        "name": "LP: Polaris Brand LP Redesign (US)",
        "hypothesis": "Polaris redesigned Brand LP improves registration CVR",
        "start_date": "2025-07-01",
        "end_date": "2025-09-30",
        "status": "completed",
        "result": "+0.38% AB registrations (65.7% probability, 275 incremental regs annualized). +37bps reg CVR (10.03% vs 9.66%).",
        "metric_before": 9.66,
        "metric_after": 10.03,
        "effect_size": 0.38,
        "decision": "Positive but modest. Polaris LP adopted as default.",
        "market": "US",
        "category": "landing_page",
        "quip_source": "BLP9AAhFfua"
    },
    {
        "experiment_id": "redirect-current-customers",
        "name": "LP: Redirect Current Customers to Shopping",
        "hypothesis": "Redirecting existing AB customers from MCS to Shopping increases OPS",
        "start_date": "2025-07-01",
        "end_date": "2025-09-30",
        "status": "completed",
        "result": "+5% AB OPS ($2.4M annualized), +6% AB Units Ordered. If all NB /cp pages: $10.9M. All NB PS ads: $30M annualized.",
        "metric_before": None,
        "metric_after": 5.0,
        "effect_size": 5.0,
        "decision": "High impact. Scale to all NB pages.",
        "market": "US",
        "category": "landing_page",
        "quip_source": "BLP9AAhFfua"
    },
    {
        "experiment_id": "mcs-vs-regstart",
        "name": "LP: MCS LP vs Email Submit (Reg Start)",
        "hypothesis": "MCS LP with category info outperforms simple email submit for NB traffic",
        "start_date": "2024-01-01",
        "end_date": "2024-06-03",
        "status": "completed",
        "result": "US Brand: MCS +6%. CA Brand: Email +7%. CA NB: MCS +18%. UK Brand: Email +38%. FR Brand: MCS +8%. NB keywords are product-centric — MCS with category info provides better experience.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": None,
        "decision": "Market-dependent. MCS wins for NB (product intent). Email wins for UK Brand.",
        "market": "WW",
        "category": "landing_page",
        "quip_source": "MQD9AAT1lD8"
    },
    {
        "experiment_id": "ca-nb-cvr-mobile",
        "name": "LP: CA NB Mobile CVR Recovery (Polaris)",
        "hypothesis": "Mobile-specific LP optimizations recover CVR after Polaris URL migration",
        "start_date": "2026-01-09",
        "end_date": "2026-02-02",
        "status": "completed",
        "result": "Bulk: +186.6% CVR (0.82%→2.35%). Wholesale: +180% CVR (0.75%→2.10%). Phase 2: 5 additional pages updated.",
        "metric_before": 0.82,
        "metric_after": 2.35,
        "effect_size": 186.6,
        "decision": "Critical fix. Mobile LP optimization is high-leverage for Polaris migration markets.",
        "market": "CA",
        "category": "landing_page",
        "quip_source": "NXb9AAss6tU"
    },
    {
        "experiment_id": "jp-lp-callback-vs-blog",
        "name": "LP: JP Callback vs Blog Post LP",
        "hypothesis": "Blog post LP with more AB context drives higher CVR than Callback LP",
        "start_date": "2025-06-12",
        "end_date": "2025-07-30",
        "status": "completed",
        "result": "Callback wins: +81.5% CVR, -44% CPA. Only 5% Bayesian probability test would outperform. Blog format introduces friction.",
        "metric_before": 2.7,
        "metric_after": 4.9,
        "effect_size": 81.5,
        "decision": "Callback LP is superior. Blog post format adds friction without benefit.",
        "market": "JP",
        "category": "landing_page",
        "quip_source": "PbI9AAI6SDn"
    },

    # === AUDIENCES ===
    {
        "experiment_id": "liveramp-2023",
        "name": "Audiences: LiveRamp 1P Targeting",
        "hypothesis": "1st party audience targeting via LiveRamp improves PS efficiency",
        "start_date": "2023-03-01",
        "end_date": "2023-06-30",
        "status": "completed",
        "result": "AB Registrants: 14M users → 1.7M active on Google (13% match vs 30-50% expected). BCIvNext: 1.25M → 140k (11% match). Brand drove 95% cost/96% BP signups. Suspended due to US privacy law.",
        "metric_before": None,
        "metric_after": 13.0,
        "effect_size": None,
        "decision": "Suspended. Match rates too low, privacy concerns. Start simple then go granular.",
        "market": "US",
        "category": "audience",
        "quip_source": "abc9AAsI8rV"
    },

    # === CPS (Cross-Product Selling) ===
    {
        "experiment_id": "cps-eu-lead-form",
        "name": "CPS: EU Lead Form Pilot",
        "hypothesis": "Lead form approach for CPS keywords drives qualified leads",
        "start_date": "2023-01-01",
        "end_date": None,
        "status": "completed",
        "result": "$262 CPA, 1.1K MALs over 17 months. Only evergreen CPS success. EU CPS form-fill: 32x higher CVR for MQLs/SQLs vs SSR landing pages.",
        "metric_before": None,
        "metric_after": 262.0,
        "effect_size": None,
        "decision": "Only viable CPS approach. PS cannot segment CPS vs SSR audience through keyword intent.",
        "market": "EU",
        "category": "cps",
        "quip_source": "VDf9AA5JiIY"
    },
    {
        "experiment_id": "cps-dg-us-uk",
        "name": "CPS: DG Display Test (US/UK)",
        "hypothesis": "Display/DG campaigns drive CPS awareness and HQs",
        "start_date": "2025-03-20",
        "end_date": "2025-06-26",
        "status": "completed",
        "result": "R1: Limited brand lift. 0 HQs. R2: US +1.51% brand lift, UK +1.23% (age 35-44). Still 0 HQs. Search lift: +78% US, +135% UK for 'Amazon Business' searches.",
        "metric_before": None,
        "metric_after": 1.51,
        "effect_size": None,
        "decision": "Current investment insufficient. Need more granular targeting or higher budget.",
        "market": "US/UK",
        "category": "cps",
        "quip_source": "IUA9AAGTmnc"
    },
    {
        "experiment_id": "cps-dg-ssr",
        "name": "CPS: DG SSR Results (Dec 2024)",
        "hypothesis": "DG campaigns drive search lift and brand awareness for SSR",
        "start_date": "2024-10-01",
        "end_date": "2024-12-01",
        "status": "completed",
        "result": "2.6MM clicks at 92% lower CPC vs Text Ads. Brand Lift: +2% recall/consideration/purchase intent. Search Lift: +78% US, +135% UK, +142% JP.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": None,
        "decision": "DG drives search lift efficiently. $721K budget for CPS DG plan.",
        "market": "WW",
        "category": "cps",
        "quip_source": "FAZ9AAzxU6P"
    },

    # === WEBLAB / SITE TESTS ===
    {
        "experiment_id": "ca-carousel-weblab",
        "name": "Weblab: CA Carousel on Bulk Page",
        "hypothesis": "Product carousel on bulk LP improves registration CVR",
        "start_date": "2025-10-06",
        "end_date": "2025-11-14",
        "status": "completed",
        "result": "-9% registration impact. Prospects value 'savings' messaging over product relevance. Need retail pricing in API.",
        "metric_before": None,
        "metric_after": -9.0,
        "effect_size": -9.0,
        "decision": "Negative. Do not roll out. Need retail pricing API before re-running.",
        "market": "CA",
        "category": "weblab",
        "quip_source": "dKf9AAexRbL"
    },
    {
        "experiment_id": "it-carousel-weblab",
        "name": "Weblab: IT Carousel",
        "hypothesis": "Product carousel on IT LP improves registration CVR",
        "start_date": "2025-10-10",
        "end_date": "2025-11-14",
        "status": "completed",
        "result": "Discarded. EU cookie consent issues — only 35% allow cookies. Future EU tests need server-side triggering.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": None,
        "decision": "Discarded. EU cookie consent blocks client-side experiments.",
        "market": "IT",
        "category": "weblab",
        "quip_source": "dKf9AAexRbL"
    },
    {
        "experiment_id": "us-promo-bfcm",
        "name": "Weblab: US BFCM Promo Test",
        "hypothesis": "35% off promo on wholesale LP drives higher registration CVR during BFCM",
        "start_date": "2025-11-11",
        "end_date": "2025-12-14",
        "status": "completed",
        "result": "W46: -45% behind phased goal, traffic -13% lower than projected. Reg abandonment concern from H1 promo test.",
        "metric_before": None,
        "metric_after": -45.0,
        "effect_size": -45.0,
        "decision": "Underperformed. Promo messaging may cause reg abandonment.",
        "market": "US",
        "category": "weblab",
        "quip_source": "KBL9AAquAv5"
    },
    {
        "experiment_id": "guest-weblab",
        "name": "Weblab: Guest Experience (AB_MCS_GUEST_EXPERIENCE)",
        "hypothesis": "Guest ungated experience improves registration funnel",
        "start_date": "2025-10-01",
        "end_date": None,
        "status": "in_progress",
        "result": "Active weblab AB_MCS_GUEST_EXPERIENCE_1116474. Guest ungated rolled out 12/15.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": None,
        "decision": "Monitoring. Part of broader guest experience initiative.",
        "market": "US",
        "category": "weblab",
        "quip_source": "IPB9AAeNAQB"
    },

    # === UK MAC ===
    {
        "experiment_id": "uk-mac-impact",
        "name": "UK MAC Campaign Impact Analysis",
        "hypothesis": "MAC campaigns drive incremental Brand performance in UK",
        "start_date": "2025-01-01",
        "end_date": "2026-03-04",
        "status": "completed",
        "result": "No significant positive impact. MAC-active periods: -25% impressions, -9% clicks, -10% regs vs non-active. CPA identical ($63). Seasonality confirms no lift.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": 0.0,
        "decision": "No impact. MAC does not drive incremental Brand performance.",
        "market": "UK",
        "category": "brand",
        "quip_source": "YEG9AAoOEiO"
    },

    # === SECONDARY LANGUAGE ===
    {
        "experiment_id": "de-english-secondary",
        "name": "Secondary Language: DE English Campaigns",
        "hypothesis": "English-language campaigns capture untapped DE search volume",
        "start_date": "2024-07-01",
        "end_date": None,
        "status": "completed",
        "result": "11% of DE queries are English. Launched Jul 2024.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": None,
        "decision": "Launched. Captures incremental English-language demand in DE.",
        "market": "DE",
        "category": "secondary_language",
        "quip_source": "WKS9AAlN5pT"
    },
    {
        "experiment_id": "jp-english-secondary",
        "name": "Secondary Language: JP English Campaigns",
        "hypothesis": "English-language campaigns capture untapped JP search volume",
        "start_date": "2024-07-01",
        "end_date": None,
        "status": "completed",
        "result": "12.66% CTR (vs JP 10.47%), but lower CVR (1.58% vs 1.71%). Higher engagement, lower conversion.",
        "metric_before": 10.47,
        "metric_after": 12.66,
        "effect_size": 20.9,
        "decision": "Launched but lower CVR. English searchers engage more but convert less.",
        "market": "JP",
        "category": "secondary_language",
        "quip_source": "WKS9AAlN5pT"
    },

    # === JP SPECIFIC TESTS ===
    {
        "experiment_id": "jp-wholesale-bulk-nb",
        "name": "JP NB: Wholesale/Bulk Keywords",
        "hypothesis": "Wholesale/bulk keywords drive NB registrations in JP",
        "start_date": "2024-01-30",
        "end_date": "2024-05-20",
        "status": "completed",
        "result": "$921 CPA, $22k cost. Most successful JP NB campaign but still 10x WW avg of $85.",
        "metric_before": None,
        "metric_after": 921.0,
        "effect_size": None,
        "decision": "Best JP NB result but still 10x WW average. JP NB remains challenging.",
        "market": "JP",
        "category": "nb_expansion",
        "quip_source": "dFZ9AA5fAz2"
    },
    {
        "experiment_id": "jp-yahoo-sitelink",
        "name": "JP: Yahoo Sitelink Extension",
        "hypothesis": "Adding Google-style sitelinks to Yahoo drives incremental regs",
        "start_date": "2024-05-24",
        "end_date": None,
        "status": "completed",
        "result": "+6 regs/week from sitelink addition.",
        "metric_before": None,
        "metric_after": 6.0,
        "effect_size": None,
        "decision": "Positive. Simple extension drove incremental volume.",
        "market": "JP",
        "category": "ad_copy",
        "quip_source": "dFZ9AA5fAz2"
    },
    {
        "experiment_id": "jp-post-mhlw",
        "name": "JP: Post-MHLW Normalization Analysis",
        "hypothesis": "Post-MHLW performance represents normalization to baseline, not additional inefficiency",
        "start_date": "2026-02-01",
        "end_date": "2026-02-17",
        "status": "completed",
        "result": "Wk6 2026 vs Pre-MHLW: CPA -1%, CVR +6%. YoY: Regs +12%, CPA -15%, CVR +21%. Baseline aligned.",
        "metric_before": 73.8,
        "metric_after": 72.86,
        "effect_size": -1.3,
        "decision": "Confirmed normalization. JP performance back to pre-MHLW baseline.",
        "market": "JP",
        "category": "analysis",
        "quip_source": "PSa9AAWBFPB"
    },

    # === BRAND TOOLS ===
    {
        "experiment_id": "primelis-brand-core",
        "name": "Brand: Primelis Cross Brand Platform Test",
        "hypothesis": "Primelis platform reduces Brand Core costs by optimizing organic vs paid blended CTR",
        "start_date": "2025-11-03",
        "end_date": "2025-12-29",
        "status": "completed",
        "result": "$20K budget, 2-month test on US Brand Core exact match (~$600K/month spend). Monitors organic vs paid blended CTR, gradually decreases bids when organic coverage high.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": None,
        "decision": "Results pending documentation. Success criteria: cost savings without risk to clicks/regs.",
        "market": "US",
        "category": "brand",
        "quip_source": "HNL9AA4Zse1"
    },

    # === MX SPECIFIC ===
    {
        "experiment_id": "mx-lp-ab-test",
        "name": "LP: MX Category-Specific LP A/B Test",
        "hypothesis": "Category-specific landing pages outperform generic LP for MX NB traffic",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "status": "completed",
        "result": "+52% CVR with category-specific LPs. Auto/Beauty campaign expansion followed.",
        "metric_before": None,
        "metric_after": None,
        "effect_size": 52.0,
        "decision": "Positive. Category-specific LPs are high-leverage for MX.",
        "market": "MX",
        "category": "landing_page",
        "quip_source": "eTF9AAkPHUu"
    },
]

# Insert into DuckDB
con = duckdb.connect(DB)

# Clear existing data
con.execute("DELETE FROM experiments")

inserted = 0
for exp in experiments:
    con.execute("""
        INSERT INTO experiments (experiment_id, name, hypothesis, start_date, end_date, 
                                 status, result, metric_before, metric_after, effect_size, 
                                 decision, market, category, quip_source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        exp["experiment_id"], exp["name"], exp["hypothesis"],
        exp.get("start_date"), exp.get("end_date"),
        exp["status"], exp["result"],
        exp.get("metric_before"), exp.get("metric_after"), exp.get("effect_size"),
        exp["decision"],
        exp.get("market"), exp.get("category"), exp.get("quip_source")
    ])
    inserted += 1

print(f"Inserted {inserted} experiments")

# Verify
count = con.execute("SELECT COUNT(*) FROM experiments").fetchone()[0]
print(f"Total rows in experiments: {count}")

# Summary by category
print("\nBy category:")
rows = con.execute("SELECT category, COUNT(*) FROM experiments GROUP BY category ORDER BY COUNT(*) DESC").fetchall()
for r in rows:
    print(f"  {r[0]}: {r[1]}")

# Summary by status
print("\nBy status:")
rows = con.execute("SELECT status, COUNT(*) FROM experiments GROUP BY status ORDER BY COUNT(*) DESC").fetchall()
for r in rows:
    print(f"  {r[0]}: {r[1]}")

# Summary by market
print("\nBy market:")
rows = con.execute("SELECT market, COUNT(*) FROM experiments GROUP BY market ORDER BY COUNT(*) DESC").fetchall()
for r in rows:
    print(f"  {r[0]}: {r[1]}")

con.close()
print("\nDone.")
