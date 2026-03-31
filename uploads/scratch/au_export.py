#!/usr/bin/env python3
"""AU Weeks 9-13 — Export formatted CSVs for all keywords, negatives, and insights"""
import duckdb
con = duckdb.connect(':memory:')

# ── LOAD ALL DATA ──
con.execute(r"""
CREATE TABLE au_keywords AS
SELECT 
    "Keyword" as keyword,
    "Match type" as match_type,
    "Campaign" as campaign,
    "Ad group" as ad_group,
    "Final URL" as final_url,
    TRY_CAST(REPLACE(REPLACE("Impr.", ',', ''), '"', '') AS INTEGER) as impressions,
    TRY_CAST(REPLACE(REPLACE("Clicks", ',', ''), '"', '') AS INTEGER) as clicks,
    TRY_CAST(REPLACE(REPLACE("Cost", ',', ''), '"', '') AS DOUBLE) as cost,
    regexp_extract("Final URL", '(\d{5,})_[xy]', 1) as kw_numeric_id
FROM read_csv('kw_report_au_utf8.csv', delim='\t', header=true, all_varchar=true, ignore_errors=true)
WHERE "Keyword" IS NOT NULL AND "Keyword" != ''
""")

con.execute(r"""
CREATE TABLE au_regs AS
SELECT 
    "Ref Tag" as ref_tag,
    TRY_CAST("Regs" AS INTEGER) as regs,
    regexp_extract("Ref Tag", '(\d{5,})_[xy]', 1) as reg_numeric_id
FROM read_csv('AU_Paid_Search_Ref_Tag_Registrations___Weeks_9_13_Aggregated__VP_WL__2026_03_31T01_37_57.csv', 
    header=true, all_varchar=true, ignore_errors=true)
WHERE "Ref Tag" IS NOT NULL
""")

con.execute("""
CREATE TABLE au_search_terms AS
SELECT 
    "Search term" as search_term,
    "Match type" as match_type,
    "Campaign" as campaign,
    "Ad group" as ad_group,
    "Keyword" as keyword,
    TRY_CAST(REPLACE(REPLACE("Clicks", ',', ''), '"', '') AS INTEGER) as clicks,
    TRY_CAST(REPLACE(REPLACE("Impr.", ',', ''), '"', '') AS INTEGER) as impressions,
    TRY_CAST(REPLACE(REPLACE("Cost", ',', ''), '"', '') AS DOUBLE) as cost
FROM read_csv('Search terms report.csv', header=true, all_varchar=true, ignore_errors=true)
WHERE "Search term" IS NOT NULL AND "Search term" != ''
""")

# ── JOIN: Keywords to Registrations ──
con.execute("""
CREATE TABLE au_kw_regs AS
SELECT 
    k.keyword, k.match_type, k.campaign, k.ad_group,
    k.impressions, k.clicks, k.cost, k.kw_numeric_id,
    COALESCE(SUM(r.regs), 0) as regs
FROM au_keywords k
LEFT JOIN au_regs r ON k.kw_numeric_id = r.reg_numeric_id
GROUP BY k.keyword, k.match_type, k.campaign, k.ad_group, k.impressions, k.clicks, k.cost, k.kw_numeric_id
""")

# ═══════════════════════════════════════════════════════════════
# FILE 1: All Keywords with KPIs
# ═══════════════════════════════════════════════════════════════
con.execute("""
COPY (
    SELECT 
        keyword as "Keyword",
        match_type as "Match Type",
        campaign as "Campaign",
        ad_group as "Ad Group",
        impressions as "Impressions",
        clicks as "Clicks",
        ROUND(cost, 2) as "Cost",
        regs as "Registrations",
        CASE WHEN clicks > 0 THEN ROUND(cost / clicks, 2) ELSE NULL END as "CPC",
        CASE WHEN regs > 0 THEN ROUND(cost / regs, 2) ELSE NULL END as "CPA",
        CASE WHEN impressions > 0 THEN ROUND(100.0 * clicks / impressions, 2) ELSE NULL END as "CTR %",
        CASE WHEN clicks > 0 THEN ROUND(100.0 * regs / clicks, 2) ELSE NULL END as "Conv Rate %"
    FROM au_kw_regs
    ORDER BY cost DESC
) TO 'au_all_keywords_w9_13.csv' (HEADER, DELIMITER ',');
""")
print("✓ au_all_keywords_w9_13.csv — All 1,016 keywords with Impressions, Clicks, Cost, Regs, CPC, CPA, CTR, Conv Rate")

# ═══════════════════════════════════════════════════════════════
# FILE 2: Campaign + Ad Group Summary
# ═══════════════════════════════════════════════════════════════
con.execute("""
COPY (
    SELECT 
        campaign as "Campaign",
        ad_group as "Ad Group",
        SUM(impressions) as "Impressions",
        SUM(clicks) as "Clicks",
        ROUND(SUM(cost), 2) as "Cost",
        SUM(regs) as "Registrations",
        ROUND(SUM(cost) / NULLIF(SUM(clicks), 0), 2) as "CPC",
        ROUND(SUM(cost) / NULLIF(SUM(regs), 0), 2) as "CPA",
        ROUND(100.0 * SUM(clicks) / NULLIF(SUM(impressions), 0), 2) as "CTR %",
        ROUND(100.0 * SUM(regs) / NULLIF(SUM(clicks), 0), 2) as "Conv Rate %"
    FROM au_kw_regs
    GROUP BY campaign, ad_group
    ORDER BY SUM(cost) DESC
) TO 'au_campaign_adgroup_summary_w9_13.csv' (HEADER, DELIMITER ',');
""")
print("✓ au_campaign_adgroup_summary_w9_13.csv — Campaign + Ad Group rollup with KPIs")

# ═══════════════════════════════════════════════════════════════
# FILE 3: Suggested Negatives
# ═══════════════════════════════════════════════════════════════
con.execute("""
COPY (
    SELECT 
        st.search_term as "Suggested Negative",
        st.keyword as "Triggered Keyword",
        st.campaign as "Campaign",
        st.ad_group as "Ad Group",
        st.match_type as "How It Matched",
        st.impressions as "Impressions",
        st.clicks as "Clicks",
        ROUND(st.cost, 2) as "Cost",
        ROUND(st.cost / NULLIF(st.clicks, 0), 2) as "CPC",
        kr.regs as "Keyword Regs",
        CASE 
            WHEN st.match_type ILIKE '%close variant%' AND kr.regs = 0 THEN 'Close variant leakage on zero-reg keyword'
            WHEN kr.regs = 0 AND st.cost > 30 THEN 'High spend on zero-reg keyword'
            WHEN kr.regs = 0 AND st.clicks >= 5 THEN 'Multiple clicks, zero-reg keyword'
            WHEN st.search_term ILIKE '%dropship%' THEN 'Dropshipping intent — wrong audience'
            WHEN st.search_term ILIKE '%alibaba%' OR st.search_term ILIKE '%merkandi%' THEN 'Competitor intent'
            WHEN st.search_term ILIKE '%business card%' THEN 'Consumer product search, not B2B procurement'
            WHEN st.search_term ILIKE '%is amazon business%' OR st.search_term ILIKE '%what is amazon%' THEN 'Informational query, not registration intent'
            ELSE 'Review — low relevance signal'
        END as "Reason"
    FROM au_search_terms st
    INNER JOIN au_kw_regs kr ON LOWER(st.keyword) = LOWER(kr.keyword) AND st.campaign = kr.campaign
    WHERE kr.regs = 0 
        AND st.clicks >= 2
        AND st.cost > 5
    ORDER BY st.cost DESC
) TO 'au_suggested_negatives_w9_13.csv' (HEADER, DELIMITER ',');
""")
neg_count = con.execute("""
SELECT COUNT(*) FROM au_search_terms st
INNER JOIN au_kw_regs kr ON LOWER(st.keyword) = LOWER(kr.keyword) AND st.campaign = kr.campaign
WHERE kr.regs = 0 AND st.clicks >= 2 AND st.cost > 5
""").fetchone()[0]
print(f"✓ au_suggested_negatives_w9_13.csv — {neg_count} search terms to consider as negatives (with reason codes)")

# ═══════════════════════════════════════════════════════════════
# FILE 4: CPC Reduction Candidates
# ═══════════════════════════════════════════════════════════════
con.execute("""
COPY (
    SELECT 
        keyword as "Keyword",
        match_type as "Match Type",
        campaign as "Campaign",
        ad_group as "Ad Group",
        impressions as "Impressions",
        clicks as "Clicks",
        ROUND(cost, 2) as "Cost",
        regs as "Registrations",
        ROUND(cost / NULLIF(clicks, 0), 2) as "CPC",
        ROUND(cost / NULLIF(regs, 0), 2) as "CPA",
        CASE 
            WHEN regs = 0 AND cost > 500 THEN 'HIGH PRIORITY — $500+ spend, zero regs'
            WHEN regs = 0 AND cost > 100 THEN 'MEDIUM — $100+ spend, zero regs'
            WHEN regs > 0 AND ROUND(cost / regs, 2) > 200 THEN 'CPA above $200 — reduce CPC'
            WHEN ROUND(cost / NULLIF(clicks, 0), 2) > 10 THEN 'CPC above $10 — bid too high'
            ELSE 'Review'
        END as "Action"
    FROM au_kw_regs
    WHERE (regs = 0 AND cost > 100) 
       OR (regs > 0 AND ROUND(cost / regs, 2) > 200)
       OR (ROUND(cost / NULLIF(clicks, 0), 2) > 10 AND clicks >= 5)
    ORDER BY cost DESC
) TO 'au_cpc_reduction_candidates_w9_13.csv' (HEADER, DELIMITER ',');
""")
cpc_count = con.execute("""
SELECT COUNT(*) FROM au_kw_regs
WHERE (regs = 0 AND cost > 100) 
   OR (regs > 0 AND ROUND(cost / regs, 2) > 200)
   OR (ROUND(cost / NULLIF(clicks, 0), 2) > 10 AND clicks >= 5)
""").fetchone()[0]
print(f"✓ au_cpc_reduction_candidates_w9_13.csv — {cpc_count} keywords flagged for CPC reduction (with action codes)")

# ═══════════════════════════════════════════════════════════════
# FILE 5: Top Performers (keywords worth protecting/scaling)
# ═══════════════════════════════════════════════════════════════
con.execute("""
COPY (
    SELECT 
        keyword as "Keyword",
        match_type as "Match Type",
        campaign as "Campaign",
        ad_group as "Ad Group",
        impressions as "Impressions",
        clicks as "Clicks",
        ROUND(cost, 2) as "Cost",
        regs as "Registrations",
        ROUND(cost / NULLIF(clicks, 0), 2) as "CPC",
        ROUND(cost / NULLIF(regs, 0), 2) as "CPA",
        ROUND(100.0 * clicks / NULLIF(impressions, 0), 2) as "CTR %",
        ROUND(100.0 * regs / NULLIF(clicks, 0), 2) as "Conv Rate %"
    FROM au_kw_regs
    WHERE regs > 0
    ORDER BY regs DESC, cost ASC
) TO 'au_top_performers_w9_13.csv' (HEADER, DELIMITER ',');
""")
perf_count = con.execute("SELECT COUNT(*) FROM au_kw_regs WHERE regs > 0").fetchone()[0]
print(f"✓ au_top_performers_w9_13.csv — {perf_count} converting keywords ranked by regs then efficiency")

# ═══════════════════════════════════════════════════════════════
# FILE 6: Search Terms with Keyword Linkage
# ═══════════════════════════════════════════════════════════════
con.execute("""
COPY (
    SELECT 
        st.search_term as "Search Term",
        st.keyword as "Keyword",
        st.match_type as "Match Type",
        st.campaign as "Campaign",
        st.ad_group as "Ad Group",
        st.impressions as "Impressions",
        st.clicks as "Clicks",
        ROUND(st.cost, 2) as "Cost",
        ROUND(st.cost / NULLIF(st.clicks, 0), 2) as "CPC",
        kr.regs as "Keyword Regs",
        ROUND(kr.cost / NULLIF(kr.regs, 0), 2) as "Keyword CPA",
        CASE WHEN kr.regs > 0 THEN 'Converting KW' ELSE 'Zero-Reg KW' END as "Keyword Status"
    FROM au_search_terms st
    LEFT JOIN au_kw_regs kr ON LOWER(st.keyword) = LOWER(kr.keyword) AND st.campaign = kr.campaign
    ORDER BY st.cost DESC
) TO 'au_search_terms_linked_w9_13.csv' (HEADER, DELIMITER ',');
""")
st_count = con.execute("SELECT COUNT(*) FROM au_search_terms").fetchone()[0]
print(f"✓ au_search_terms_linked_w9_13.csv — {st_count} search terms with keyword reg linkage and status")

print("\n── All files written to workspace root (~/). ──")
