#!/usr/bin/env python3
"""Sync new experiments from quip-mirror enrichment into MotherDuck ps.team_experiments."""
import duckdb, os
from datetime import datetime

TOKEN = os.environ.get('MOTHERDUCK_TOKEN',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJpY2hzY290dHdpbGxAZ21haWwuY29tIiwibWRSZWdpb24iOiJhd3MtdXMtZWFzdC0xIiwic2Vzc2lvbiI6InJpY2hzY290dHdpbGwuZ21haWwuY29tIiwicGF0IjoiVDNIYzFVQWYzT3o1bjVkLS03ckdHNlBjMlpUdVNNbFItT3RXMS1qNzVPUSIsInVzZXJJZCI6ImU2MDhlNDZiLTE4YzctNGE5Ny04M2I2LWE0N2ZhOThmNjBhYyIsImlzcyI6Im1kX3BhdCIsInJlYWRPbmx5IjpmYWxzZSwidG9rZW5UeXBlIjoicmVhZF93cml0ZSIsImlhdCI6MTc3NTQ0MzY0N30.tS0Cab3FQ8_CDZ1PqOo9z09KYHEUFHwuLVXRQrxcHig')

# Map category → channel for the Dive schema
CATEGORY_CHANNEL = {
    "incrementality": "Google+Bing",
    "ad_copy": "Google Ads",
    "bidding": "Google Ads",
    "landing_page": "Google Ads",
    "audience": "Google Ads",
    "cps": "Google DG",
    "weblab": "Weblab",
    "brand": "Google Ads",
    "secondary_language": "Google Ads",
    "nb_expansion": "Google Ads",
    "analysis": "Google Ads",
}

STATUS_MAP = {
    "completed": "Complete",
    "in_progress": "In Progress",
    "suspended": "Suspended",
}

# 25 new experiments to insert (not already in Dive)
new_experiments = [
    {
        "id": "google_causal", "name": "Google Causal Analysis — Brand Search Lift",
        "owner": "Richard", "is_richard": True, "region": "US", "channel": "Google+Bing",
        "start_date": None, "end_date": None, "status": "Complete",
        "primary_metric": "Branded search lift", "primary_result": 3.0, "primary_unit": "pct",
        "secondary_metric": "Competitor click share when absent", "secondary_result": 57.0, "secondary_unit": "pct",
        "spend": None, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Positive", "summary": "+3% branded searches where NB ads present. 57% clicks to competitors when brand ads absent.",
        "source_doc": "NQA9AAX2DOp", "test_scale": "program", "sole_owner": "Richard",
        "markets": ["US"],
    },
    {
        "id": "adcopy_uk_ph2", "name": "Ad Copy UK NB — Phase 2 Rollout",
        "owner": "Andrew", "is_richard": False, "region": "UK", "channel": "Google Ads",
        "start_date": "2026-03-06", "end_date": None, "status": "In Progress",
        "primary_metric": "CVR", "primary_result": 4.28, "primary_unit": "pct",
        "secondary_metric": None, "secondary_result": None, "secondary_unit": None,
        "spend": None, "confidence": None, "bayesian_ppr": None,
        "verdict": "Monitoring", "summary": "Phase 2 launched across all NB. Paused Poor/Average ads. CVR at 12-week high.",
        "source_doc": "KCY9AAYqWd2", "test_scale": "experiment", "sole_owner": "Andrew",
        "markets": ["UK"],
    },
    {
        "id": "rsa_rewrite", "name": "RSA Google Auto-Rewrite — US",
        "owner": "Stacey", "is_richard": False, "region": "US", "channel": "Google Ads",
        "start_date": None, "end_date": None, "status": "Complete",
        "primary_metric": "CPA", "primary_result": -5.0, "primary_unit": "pct",
        "secondary_metric": "Impressions", "secondary_result": 56.0, "secondary_unit": "pct",
        "spend": None, "confidence": "Medium", "bayesian_ppr": None,
        "verdict": "Positive", "summary": "638 RSAs rewritten. $137.68 CPA vs $145 avg. +56% impressions, +57% clicks.",
        "source_doc": "ReG9AAvZFTS", "test_scale": "experiment", "sole_owner": "Stacey",
        "markets": ["US"],
    },
    {
        "id": "amo_vs_google", "name": "AMO vs Google Smart Bidding — WW",
        "owner": "Richard", "is_richard": True, "region": "WW", "channel": "Google Ads",
        "start_date": "2022-01-01", "end_date": "2022-12-31", "status": "Complete",
        "primary_metric": "Uplift range", "primary_result": 50.0, "primary_unit": "pct",
        "secondary_metric": None, "secondary_result": None, "secondary_unit": None,
        "spend": None, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Positive", "summary": "+8% to +101% uplift across 5 portfolio sets. Google uses more signals.",
        "source_doc": "ePH9AAU0wIA", "test_scale": "program", "sole_owner": "Richard",
        "markets": ["US", "CA", "UK", "DE", "FR", "IT", "ES", "JP", "AU", "MX"],
    },
    {
        "id": "eu5_restructure", "name": "EU5 Bidding Restructure — Dec 2023",
        "owner": "Andrew", "is_richard": False, "region": "EU5", "channel": "Google Ads",
        "start_date": "2023-12-01", "end_date": "2023-12-28", "status": "Complete",
        "primary_metric": "CPA change", "primary_result": None, "primary_unit": "pct",
        "secondary_metric": None, "secondary_result": None, "secondary_unit": None,
        "spend": None, "confidence": "Medium", "bayesian_ppr": None,
        "verdict": "Mixed", "summary": "AMZ→Max Conv, Generic consolidated. DE Brand IS bidding caused CPA increase — reverted.",
        "source_doc": "dSM9AAaMwDD", "test_scale": "program", "sole_owner": "Andrew",
        "markets": ["UK", "DE", "FR", "IT", "ES"],
    },
    {
        "id": "jp_cpc_cap", "name": "JP Brand CPC Cap Reduction ($55→$10)",
        "owner": "Richard", "is_richard": True, "region": "JP", "channel": "Google Ads",
        "start_date": "2025-01-01", "end_date": "2025-02-01", "status": "Complete",
        "primary_metric": "CPA", "primary_result": -29.0, "primary_unit": "pct",
        "secondary_metric": "Regs", "secondary_result": -3.0, "secondary_unit": "pct",
        "spend": None, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Positive", "summary": "-26% CPC, -29% CPA, only -3% regs. Significant savings.",
        "source_doc": "AeG9AAmSPdu", "test_scale": "experiment", "sole_owner": "Richard",
        "markets": ["JP"],
    },
    {
        "id": "jp_manual_cpc", "name": "JP Adobe→Manual CPC — Brand_Phrase_D",
        "owner": "Richard", "is_richard": True, "region": "JP", "channel": "Google Ads",
        "start_date": "2025-02-12", "end_date": None, "status": "Complete",
        "primary_metric": "CPA", "primary_result": -40.5, "primary_unit": "pct",
        "secondary_metric": "Cost", "secondary_result": -41.0, "secondary_unit": "pct",
        "spend": None, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Positive", "summary": "Manual CPC wins: $829→$493 CPA (-37%). Adobe overbids low-volume JP Brand.",
        "source_doc": "AeG9AAmSPdu", "test_scale": "experiment", "sole_owner": "Richard",
        "markets": ["JP"],
    },
    {
        "id": "au_adobe_bid", "name": "AU Adobe Bid Strategy Transition",
        "owner": "Richard", "is_richard": True, "region": "AU", "channel": "Google Ads",
        "start_date": "2026-01-16", "end_date": None, "status": "In Progress",
        "primary_metric": None, "primary_result": None, "primary_unit": None,
        "secondary_metric": None, "secondary_result": None, "secondary_unit": None,
        "spend": None, "confidence": None, "bayesian_ppr": None,
        "verdict": "Monitoring", "summary": "Brand Plus test 1/16, full rollout 1/20. Same weekly budget pacing.",
        "source_doc": "ZZR9AAs7OfO", "test_scale": "experiment", "sole_owner": "Richard",
        "markets": ["AU"],
    },
    {
        "id": "redirect_customers", "name": "Redirect Current Customers to Shopping — US",
        "owner": "Stacey", "is_richard": False, "region": "US", "channel": "Google Ads",
        "start_date": "2025-07-01", "end_date": "2025-09-30", "status": "Complete",
        "primary_metric": "AB OPS", "primary_result": 5.0, "primary_unit": "pct",
        "secondary_metric": "AB Units Ordered", "secondary_result": 6.0, "secondary_unit": "pct",
        "spend": None, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Positive", "summary": "+5% AB OPS ($2.4M annualized), +6% Units. All NB PS ads: $30M annualized potential.",
        "source_doc": "BLP9AAhFfua", "test_scale": "program", "sole_owner": "Stacey",
        "markets": ["US"],
    },
    {
        "id": "mcs_vs_regstart", "name": "MCS LP vs Email Submit (Reg Start) — WW",
        "owner": "Richard", "is_richard": True, "region": "WW", "channel": "Google Ads",
        "start_date": "2024-01-01", "end_date": "2024-06-03", "status": "Complete",
        "primary_metric": "CVR diff", "primary_result": None, "primary_unit": "pct",
        "secondary_metric": None, "secondary_result": None, "secondary_unit": None,
        "spend": None, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Mixed", "summary": "Market-dependent. MCS wins for NB (product intent). Email wins for UK Brand. CA NB: MCS +18%.",
        "source_doc": "MQD9AAT1lD8", "test_scale": "experiment", "sole_owner": "Richard",
        "markets": ["US", "CA", "UK", "FR"],
    },
    {
        "id": "ca_cvr_mobile", "name": "CA NB Mobile CVR Recovery (Polaris)",
        "owner": "Stacey", "is_richard": False, "region": "CA", "channel": "Google Ads",
        "start_date": "2026-01-09", "end_date": "2026-02-02", "status": "Complete",
        "primary_metric": "CVR", "primary_result": 186.6, "primary_unit": "pct",
        "secondary_metric": None, "secondary_result": None, "secondary_unit": None,
        "spend": None, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Positive", "summary": "Bulk: +186.6% CVR (0.82%→2.35%). Wholesale: +180%. Mobile LP optimization critical for Polaris.",
        "source_doc": "NXb9AAss6tU", "test_scale": "experiment", "sole_owner": "Stacey",
        "markets": ["CA"],
    },
    {
        "id": "jp_callback_lp", "name": "JP Callback vs Blog Post LP",
        "owner": "Richard", "is_richard": True, "region": "JP", "channel": "Google Ads",
        "start_date": "2025-06-12", "end_date": "2025-07-30", "status": "Complete",
        "primary_metric": "CVR", "primary_result": 81.5, "primary_unit": "pct",
        "secondary_metric": "CPA", "secondary_result": -44.0, "secondary_unit": "pct",
        "spend": None, "confidence": "High", "bayesian_ppr": 0.95,
        "verdict": "Positive", "summary": "Callback wins: +81.5% CVR, -44% CPA. Blog post adds friction. 95% Bayesian confidence.",
        "source_doc": "PbI9AAI6SDn", "test_scale": "experiment", "sole_owner": "Richard",
        "markets": ["JP"],
    },
    {
        "id": "cps_eu_lead", "name": "CPS EU Lead Form Pilot",
        "owner": "Richard", "is_richard": True, "region": "EU5", "channel": "Google Ads",
        "start_date": "2023-01-01", "end_date": None, "status": "Complete",
        "primary_metric": "CPA", "primary_result": 262.0, "primary_unit": "usd",
        "secondary_metric": "MALs", "secondary_result": 1100.0, "secondary_unit": "count",
        "spend": None, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Positive", "summary": "$262 CPA, 1.1K MALs over 17mo. Only evergreen CPS success. 32x higher CVR vs SSR LPs.",
        "source_doc": "VDf9AA5JiIY", "test_scale": "pilot", "sole_owner": "Richard",
        "markets": ["UK", "DE", "FR", "IT", "ES"],
    },
    {
        "id": "cps_dg_usuk", "name": "CPS DG Display Test — US/UK",
        "owner": "Richard", "is_richard": True, "region": "US/UK", "channel": "Google DG",
        "start_date": "2025-03-20", "end_date": "2025-06-26", "status": "Complete",
        "primary_metric": "Brand lift", "primary_result": 1.51, "primary_unit": "pct",
        "secondary_metric": "HQs", "secondary_result": 0.0, "secondary_unit": "count",
        "spend": None, "confidence": "Low", "bayesian_ppr": None,
        "verdict": "Negative", "summary": "R1+R2: US +1.51% brand lift, UK +1.23%. 0 HQs both rounds. Insufficient investment.",
        "source_doc": "IUA9AAGTmnc", "test_scale": "experiment", "sole_owner": "Richard",
        "markets": ["US", "UK"],
    },
    {
        "id": "cps_dg_ssr", "name": "CPS DG SSR Results — WW",
        "owner": "Richard", "is_richard": True, "region": "WW", "channel": "Google DG",
        "start_date": "2024-10-01", "end_date": "2024-12-01", "status": "Complete",
        "primary_metric": "Search lift US", "primary_result": 78.0, "primary_unit": "pct",
        "secondary_metric": "CPC vs Text Ads", "secondary_result": -92.0, "secondary_unit": "pct",
        "spend": None, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Positive", "summary": "2.6MM clicks at 92% lower CPC. Search Lift: +78% US, +135% UK, +142% JP.",
        "source_doc": "FAZ9AAzxU6P", "test_scale": "program", "sole_owner": "Richard",
        "markets": ["US", "UK", "JP"],
    },
    {
        "id": "ca_carousel", "name": "CA Carousel on Bulk Page — Weblab",
        "owner": "Stacey", "is_richard": False, "region": "CA", "channel": "Weblab",
        "start_date": "2025-10-06", "end_date": "2025-11-14", "status": "Complete",
        "primary_metric": "Reg impact", "primary_result": -9.0, "primary_unit": "pct",
        "secondary_metric": None, "secondary_result": None, "secondary_unit": None,
        "spend": None, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Negative", "summary": "-9% reg impact. Prospects value savings messaging over product relevance. Need retail pricing API.",
        "source_doc": "dKf9AAexRbL", "test_scale": "experiment", "sole_owner": "Stacey",
        "markets": ["CA"],
    },
    {
        "id": "it_carousel", "name": "IT Carousel — Weblab (Discarded)",
        "owner": "Andrew", "is_richard": False, "region": "IT", "channel": "Weblab",
        "start_date": "2025-10-10", "end_date": "2025-11-14", "status": "Complete",
        "primary_metric": None, "primary_result": None, "primary_unit": None,
        "secondary_metric": None, "secondary_result": None, "secondary_unit": None,
        "spend": None, "confidence": None, "bayesian_ppr": None,
        "verdict": "Discarded", "summary": "EU cookie consent: only 35% allow cookies. Client-side experiments blocked in EU.",
        "source_doc": "dKf9AAexRbL", "test_scale": "experiment", "sole_owner": "Andrew",
        "markets": ["IT"],
    },
    {
        "id": "uk_mac", "name": "UK MAC Campaign Impact Analysis",
        "owner": "Andrew", "is_richard": False, "region": "UK", "channel": "Google Ads",
        "start_date": "2025-01-01", "end_date": "2026-03-04", "status": "Complete",
        "primary_metric": "Reg impact", "primary_result": -10.0, "primary_unit": "pct",
        "secondary_metric": "CPA", "secondary_result": 0.0, "secondary_unit": "pct",
        "spend": None, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Negative", "summary": "No positive impact. MAC-active: -25% imp, -9% clicks, -10% regs. CPA identical ($63).",
        "source_doc": "YEG9AAoOEiO", "test_scale": "experiment", "sole_owner": "Andrew",
        "markets": ["UK"],
    },
    {
        "id": "de_english", "name": "Secondary Language — DE English Campaigns",
        "owner": "Andrew", "is_richard": False, "region": "DE", "channel": "Google Ads",
        "start_date": "2024-07-01", "end_date": None, "status": "Complete",
        "primary_metric": "Query share", "primary_result": 11.0, "primary_unit": "pct",
        "secondary_metric": None, "secondary_result": None, "secondary_unit": None,
        "spend": None, "confidence": "Medium", "bayesian_ppr": None,
        "verdict": "Positive", "summary": "11% of DE queries are English. Captures incremental demand.",
        "source_doc": "WKS9AAlN5pT", "test_scale": "experiment", "sole_owner": "Andrew",
        "markets": ["DE"],
    },
    {
        "id": "jp_english", "name": "Secondary Language — JP English Campaigns",
        "owner": "Richard", "is_richard": True, "region": "JP", "channel": "Google Ads",
        "start_date": "2024-07-01", "end_date": None, "status": "Complete",
        "primary_metric": "CTR", "primary_result": 20.9, "primary_unit": "pct",
        "secondary_metric": "CVR", "secondary_result": -7.6, "secondary_unit": "pct",
        "spend": None, "confidence": "Medium", "bayesian_ppr": None,
        "verdict": "Mixed", "summary": "12.66% CTR (vs 10.47%) but lower CVR (1.58% vs 1.71%). Higher engagement, lower conversion.",
        "source_doc": "WKS9AAlN5pT", "test_scale": "experiment", "sole_owner": "Richard",
        "markets": ["JP"],
    },
    {
        "id": "jp_wholesale_nb", "name": "JP NB Wholesale/Bulk Keywords",
        "owner": "Richard", "is_richard": True, "region": "JP", "channel": "Google Ads",
        "start_date": "2024-01-30", "end_date": "2024-05-20", "status": "Complete",
        "primary_metric": "CPA", "primary_result": 921.0, "primary_unit": "usd",
        "secondary_metric": "Cost", "secondary_result": 22000.0, "secondary_unit": "usd",
        "spend": 22000.0, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Mixed", "summary": "$921 CPA — best JP NB result but still 10x WW avg of $85. JP NB remains challenging.",
        "source_doc": "dFZ9AA5fAz2", "test_scale": "pilot", "sole_owner": "Richard",
        "markets": ["JP"],
    },
    {
        "id": "jp_yahoo_sitelink", "name": "JP Yahoo Sitelink Extension",
        "owner": "Richard", "is_richard": True, "region": "JP", "channel": "Yahoo",
        "start_date": "2024-05-24", "end_date": None, "status": "Complete",
        "primary_metric": "Incremental regs/week", "primary_result": 6.0, "primary_unit": "count",
        "secondary_metric": None, "secondary_result": None, "secondary_unit": None,
        "spend": None, "confidence": "Medium", "bayesian_ppr": None,
        "verdict": "Positive", "summary": "+6 regs/week from sitelink addition. Simple extension, incremental volume.",
        "source_doc": "dFZ9AA5fAz2", "test_scale": "experiment", "sole_owner": "Richard",
        "markets": ["JP"],
    },
    {
        "id": "jp_mhlw", "name": "JP Post-MHLW Normalization Analysis",
        "owner": "Richard", "is_richard": True, "region": "JP", "channel": "Google Ads",
        "start_date": "2026-02-01", "end_date": "2026-02-17", "status": "Complete",
        "primary_metric": "CPA vs pre-MHLW", "primary_result": -1.3, "primary_unit": "pct",
        "secondary_metric": "CVR YoY", "secondary_result": 21.0, "secondary_unit": "pct",
        "spend": None, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Positive", "summary": "Confirmed normalization. CPA -1% vs pre-MHLW. YoY: Regs +12%, CPA -15%, CVR +21%.",
        "source_doc": "PSa9AAWBFPB", "test_scale": "experiment", "sole_owner": "Richard",
        "markets": ["JP"],
    },
    {
        "id": "primelis_brand", "name": "Primelis Cross Brand Platform — US",
        "owner": "Richard", "is_richard": True, "region": "US", "channel": "Google Ads",
        "start_date": "2025-11-03", "end_date": "2025-12-29", "status": "Complete",
        "primary_metric": None, "primary_result": None, "primary_unit": None,
        "secondary_metric": None, "secondary_result": None, "secondary_unit": None,
        "spend": 20000.0, "confidence": None, "bayesian_ppr": None,
        "verdict": "Pending", "summary": "$20K test on US Brand Core exact match (~$600K/mo). Monitors organic vs paid blended CTR.",
        "source_doc": "HNL9AA4Zse1", "test_scale": "pilot", "sole_owner": "Richard",
        "markets": ["US"],
    },
    {
        "id": "mx_category_lp", "name": "MX Category-Specific LP A/B Test",
        "owner": "Richard", "is_richard": True, "region": "MX", "channel": "Google Ads",
        "start_date": "2025-01-01", "end_date": "2025-12-31", "status": "Complete",
        "primary_metric": "CVR", "primary_result": 52.0, "primary_unit": "pct",
        "secondary_metric": None, "secondary_result": None, "secondary_unit": None,
        "spend": None, "confidence": "High", "bayesian_ppr": None,
        "verdict": "Positive", "summary": "+52% CVR with category-specific LPs. Auto/Beauty expansion followed.",
        "source_doc": "eTF9AAkPHUu", "test_scale": "experiment", "sole_owner": "Richard",
        "markets": ["MX"],
    },
]

def main():
    con = duckdb.connect(f'md:ps_analytics?motherduck_token={TOKEN}')

    inserted_exp = 0
    inserted_mkt = 0
    inserted_contrib = 0

    for exp in new_experiments:
        # Check if already exists
        exists = con.execute("SELECT COUNT(*) FROM ps.team_experiments WHERE experiment_id = ?", [exp["id"]]).fetchone()[0]
        if exists:
            print(f"  SKIP {exp['id']} (already exists)")
            continue

        con.execute("""
            INSERT INTO ps.team_experiments 
            (experiment_id, name, owner, is_richard, region, channel,
             start_date, end_date, status, primary_metric, primary_result, primary_unit,
             secondary_metric, secondary_result, secondary_unit, spend, confidence,
             bayesian_ppr, verdict, summary, source_doc, test_scale, sole_owner)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, [
            exp["id"], exp["name"], exp["owner"], exp["is_richard"], exp["region"], exp["channel"],
            exp.get("start_date"), exp.get("end_date"), exp["status"],
            exp.get("primary_metric"), exp.get("primary_result"), exp.get("primary_unit"),
            exp.get("secondary_metric"), exp.get("secondary_result"), exp.get("secondary_unit"),
            exp.get("spend"), exp.get("confidence"), exp.get("bayesian_ppr"),
            exp["verdict"], exp["summary"], exp["source_doc"],
            exp.get("test_scale"), exp.get("sole_owner"),
        ])
        inserted_exp += 1

        # Insert markets
        for mkt in exp.get("markets", []):
            con.execute("INSERT INTO ps.experiment_markets (experiment_id, market) VALUES (?, ?)", [exp["id"], mkt])
            inserted_mkt += 1

        # Insert contributor
        con.execute("INSERT INTO ps.experiment_contributors (experiment_id, person, role) VALUES (?, ?, ?)",
                     [exp["id"], exp["owner"], "owner"])
        inserted_contrib += 1

    print(f"\nInserted: {inserted_exp} experiments, {inserted_mkt} market mappings, {inserted_contrib} contributors")

    # Verify totals
    total_exp = con.execute("SELECT COUNT(*) FROM ps.team_experiments").fetchone()[0]
    total_mkt = con.execute("SELECT COUNT(*) FROM ps.experiment_markets").fetchone()[0]
    total_contrib = con.execute("SELECT COUNT(*) FROM ps.experiment_contributors").fetchone()[0]
    print(f"Totals: {total_exp} experiments, {total_mkt} market mappings, {total_contrib} contributors")

    con.close()

if __name__ == "__main__":
    main()
