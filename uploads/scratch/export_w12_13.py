#!/usr/bin/env python3
"""AU + MX Paid Search Weeks 12-13 — Full export with KPIs, CPA, negatives, insights"""
import duckdb, os

def run_market(con, market, kw_file, st_file, reg_file, reg_col_tag, reg_col_regs, kw_skip_rows, kw_has_status, ref_join_mode):
    """
    ref_join_mode:
      'numeric_id'  = AU style (extract numeric ID with _x/_y suffix from both sides)
      'keyword_id'  = MX style (use Keyword ID column, extract first numeric ID from reg ref tag)
    """
    prefix = market.lower()
    
    # ── KEYWORDS ──
    # MX has Keyword ID column, AU does not
    kw_id_col = ', "Keyword ID" as keyword_id' if ref_join_mode == 'keyword_id' else ''
    
    if kw_has_status:
        kw_sql = f"""
        CREATE OR REPLACE TABLE keywords AS
        SELECT 
            "Keyword" as keyword,
            "Match type" as match_type,
            "Campaign" as campaign,
            "Ad group" as ad_group,
            "Final URL" as final_url,
            TRY_CAST(REPLACE(REPLACE("Impr.", ',', ''), '"', '') AS INTEGER) as impressions,
            TRY_CAST(REPLACE(REPLACE("Clicks", ',', ''), '"', '') AS INTEGER) as clicks,
            TRY_CAST(REPLACE(REPLACE("Cost", ',', ''), '"', '') AS DOUBLE) as cost
            {kw_id_col}
        FROM read_csv('{kw_file}', header=true, skip={kw_skip_rows}, all_varchar=true, ignore_errors=true)
        WHERE "Keyword" IS NOT NULL AND "Keyword" != '' 
            AND "Keyword status" NOT LIKE 'Total%'
            AND "Keyword" NOT LIKE 'Total%'
        """
    else:
        kw_sql = f"""
        CREATE OR REPLACE TABLE keywords AS
        SELECT 
            "Keyword" as keyword,
            "Match type" as match_type,
            "Campaign" as campaign,
            "Ad group" as ad_group,
            "Final URL" as final_url,
            TRY_CAST(REPLACE(REPLACE("Impr.", ',', ''), '"', '') AS INTEGER) as impressions,
            TRY_CAST(REPLACE(REPLACE("Clicks", ',', ''), '"', '') AS INTEGER) as clicks,
            TRY_CAST(REPLACE(REPLACE("Cost", ',', ''), '"', '') AS DOUBLE) as cost
            {kw_id_col}
        FROM read_csv('{kw_file}', header=true, skip={kw_skip_rows}, all_varchar=true, ignore_errors=true)
        WHERE "Keyword" IS NOT NULL AND "Keyword" != ''
        """
    con.execute(kw_sql)
    
    # Filter out total rows that slipped through
    con.execute("""DELETE FROM keywords WHERE campaign IS NULL OR campaign = '' OR campaign LIKE 'Total%'""")
    
    # ── SEARCH TERMS ──
    con.execute(f"""
    CREATE OR REPLACE TABLE search_terms AS
    SELECT 
        "Search term" as search_term,
        "Match type" as match_type,
        "Campaign" as campaign,
        "Ad group" as ad_group,
        "Keyword" as keyword,
        TRY_CAST(REPLACE(REPLACE("Clicks", ',', ''), '"', '') AS INTEGER) as clicks,
        TRY_CAST(REPLACE(REPLACE("Impr.", ',', ''), '"', '') AS INTEGER) as impressions,
        TRY_CAST(REPLACE(REPLACE("Cost", ',', ''), '"', '') AS DOUBLE) as cost
    FROM read_csv('{st_file}', header=true, skip={kw_skip_rows}, all_varchar=true, ignore_errors=true)
    WHERE "Search term" IS NOT NULL AND "Search term" != ''
        AND "Search term" NOT LIKE 'Total%'
    """)
    
    # ── REGISTRATIONS ──
    con.execute(f"""
    CREATE OR REPLACE TABLE regs AS
    SELECT 
        "{reg_col_tag}" as ref_tag,
        TRY_CAST("{reg_col_regs}" AS INTEGER) as regs
    FROM read_csv('{reg_file}', header=true, all_varchar=true, ignore_errors=true)
    WHERE "{reg_col_tag}" IS NOT NULL
    """)
    
    # ── JOIN LOGIC ──
    if ref_join_mode == 'numeric_id':
        # AU: extract numeric ID (before _x or _y suffix) from both keyword URL and reg ref tag
        con.execute(r"""
        CREATE OR REPLACE TABLE kw_regs AS
        SELECT 
            k.keyword, k.match_type, k.campaign, k.ad_group,
            k.impressions, k.clicks, k.cost,
            COALESCE(SUM(r.regs), 0) as regs
        FROM keywords k
        LEFT JOIN regs r 
            ON regexp_extract(k.final_url, '(\d{5,})_[xy]', 1) = regexp_extract(r.ref_tag, '(\d{5,})_[xy]', 1)
            AND regexp_extract(k.final_url, '(\d{5,})_[xy]', 1) IS NOT NULL
            AND regexp_extract(k.final_url, '(\d{5,})_[xy]', 1) != ''
        GROUP BY k.keyword, k.match_type, k.campaign, k.ad_group, k.impressions, k.clicks, k.cost
        """)
    elif ref_join_mode == 'keyword_id':
        # MX: use Keyword ID column, extract first long numeric ID from reg ref tag
        con.execute(r"""
        CREATE OR REPLACE TABLE regs_with_id AS
        SELECT ref_tag, regs,
            regexp_extract(ref_tag, 'pd_sl_\w+_(\d{5,})', 1) as reg_numeric_id
        FROM regs
        WHERE regexp_extract(ref_tag, 'pd_sl_\w+_(\d{5,})', 1) IS NOT NULL
            AND regexp_extract(ref_tag, 'pd_sl_\w+_(\d{5,})', 1) != ''
        """)
        con.execute("""
        CREATE OR REPLACE TABLE kw_regs AS
        SELECT 
            k.keyword, k.match_type, k.campaign, k.ad_group,
            k.impressions, k.clicks, k.cost,
            COALESCE(SUM(r.regs), 0) as regs
        FROM keywords k
        LEFT JOIN regs_with_id r ON k.keyword_id = r.reg_numeric_id
        GROUP BY k.keyword, k.match_type, k.campaign, k.ad_group, k.impressions, k.clicks, k.cost
        """)
    
    # Verify
    matched = con.execute("SELECT SUM(regs) FROM kw_regs WHERE regs > 0").fetchone()[0] or 0
    total = con.execute("SELECT SUM(regs) FROM regs").fetchone()[0] or 0
    kw_count = con.execute("SELECT COUNT(*) FROM kw_regs").fetchone()[0]
    converting = con.execute("SELECT COUNT(*) FROM kw_regs WHERE regs > 0").fetchone()[0]
    print(f"\n{'='*70}")
    print(f"  {market} — Weeks 12-13 | {kw_count} keywords | {matched}/{total} regs matched | {converting} converting KWs")
    print(f"{'='*70}")

    # ═══ FILE 1: All Keywords ═══
    out1 = f"{prefix}_all_keywords_w12_13.csv"
    con.execute(f"""
    COPY (
        SELECT 
            keyword as "Keyword", match_type as "Match Type", campaign as "Campaign", ad_group as "Ad Group",
            impressions as "Impressions", clicks as "Clicks", ROUND(cost, 2) as "Cost",
            regs as "Registrations",
            CASE WHEN clicks > 0 THEN ROUND(cost / clicks, 2) ELSE NULL END as "CPC",
            CASE WHEN regs > 0 THEN ROUND(cost / regs, 2) ELSE NULL END as "CPA",
            CASE WHEN impressions > 0 THEN ROUND(100.0 * clicks / impressions, 2) ELSE NULL END as "CTR %",
            CASE WHEN clicks > 0 THEN ROUND(100.0 * regs / clicks, 2) ELSE NULL END as "Conv Rate %"
        FROM kw_regs ORDER BY cost DESC
    ) TO '{out1}' (HEADER, DELIMITER ',');
    """)
    print(f"  ✓ {out1}")

    # ═══ FILE 2: Campaign + Ad Group Summary ═══
    out2 = f"{prefix}_campaign_adgroup_summary_w12_13.csv"
    con.execute(f"""
    COPY (
        SELECT 
            campaign as "Campaign", ad_group as "Ad Group",
            SUM(impressions) as "Impressions", SUM(clicks) as "Clicks",
            ROUND(SUM(cost), 2) as "Cost", SUM(regs) as "Registrations",
            ROUND(SUM(cost)/NULLIF(SUM(clicks),0), 2) as "CPC",
            ROUND(SUM(cost)/NULLIF(SUM(regs),0), 2) as "CPA",
            ROUND(100.0*SUM(clicks)/NULLIF(SUM(impressions),0), 2) as "CTR %",
            ROUND(100.0*SUM(regs)/NULLIF(SUM(clicks),0), 2) as "Conv Rate %"
        FROM kw_regs GROUP BY campaign, ad_group ORDER BY SUM(cost) DESC
    ) TO '{out2}' (HEADER, DELIMITER ',');
    """)
    print(f"  ✓ {out2}")

    # ═══ FILE 3: Suggested Negatives ═══
    out3 = f"{prefix}_suggested_negatives_w12_13.csv"
    con.execute(f"""
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
                WHEN st.search_term ILIKE '%dropship%' THEN 'Dropshipping intent'
                WHEN st.search_term ILIKE '%alibaba%' OR st.search_term ILIKE '%merkandi%' OR st.search_term ILIKE '%temu%' THEN 'Competitor intent'
                WHEN st.search_term ILIKE '%business card%' THEN 'Consumer product search'
                WHEN st.search_term ILIKE '%is amazon business%' OR st.search_term ILIKE '%what is amazon%' THEN 'Informational query'
                ELSE 'Review — zero-reg keyword spend'
            END as "Reason"
        FROM search_terms st
        INNER JOIN kw_regs kr ON LOWER(st.keyword) = LOWER(kr.keyword) AND st.campaign = kr.campaign
        WHERE kr.regs = 0 AND st.clicks >= 2 AND st.cost > 3
        ORDER BY st.cost DESC
    ) TO '{out3}' (HEADER, DELIMITER ',');
    """)
    neg_count = con.execute("""
    SELECT COUNT(*) FROM search_terms st
    INNER JOIN kw_regs kr ON LOWER(st.keyword) = LOWER(kr.keyword) AND st.campaign = kr.campaign
    WHERE kr.regs = 0 AND st.clicks >= 2 AND st.cost > 3
    """).fetchone()[0]
    print(f"  ✓ {out3} ({neg_count} candidates)")

    # ═══ FILE 4: CPC Reduction Candidates ═══
    out4 = f"{prefix}_cpc_reduction_candidates_w12_13.csv"
    con.execute(f"""
    COPY (
        SELECT 
            keyword as "Keyword", match_type as "Match Type", campaign as "Campaign", ad_group as "Ad Group",
            impressions as "Impressions", clicks as "Clicks", ROUND(cost, 2) as "Cost",
            regs as "Registrations",
            ROUND(cost / NULLIF(clicks, 0), 2) as "CPC",
            ROUND(cost / NULLIF(regs, 0), 2) as "CPA",
            CASE 
                WHEN regs = 0 AND cost > 500 THEN 'HIGH — $500+ spend, zero regs'
                WHEN regs = 0 AND cost > 100 THEN 'MEDIUM — $100+ spend, zero regs'
                WHEN regs > 0 AND ROUND(cost / regs, 2) > 200 THEN 'CPA above $200'
                WHEN ROUND(cost / NULLIF(clicks, 0), 2) > 10 THEN 'CPC above $10'
                ELSE 'Review'
            END as "Action"
        FROM kw_regs
        WHERE (regs = 0 AND cost > 100) 
           OR (regs > 0 AND ROUND(cost / regs, 2) > 200)
           OR (ROUND(cost / NULLIF(clicks, 0), 2) > 10 AND clicks >= 5)
        ORDER BY cost DESC
    ) TO '{out4}' (HEADER, DELIMITER ',');
    """)
    cpc_count = con.execute("""
    SELECT COUNT(*) FROM kw_regs
    WHERE (regs = 0 AND cost > 100) OR (regs > 0 AND ROUND(cost / regs, 2) > 200)
       OR (ROUND(cost / NULLIF(clicks, 0), 2) > 10 AND clicks >= 5)
    """).fetchone()[0]
    print(f"  ✓ {out4} ({cpc_count} keywords)")

    # ═══ FILE 5: Top Performers ═══
    out5 = f"{prefix}_top_performers_w12_13.csv"
    con.execute(f"""
    COPY (
        SELECT 
            keyword as "Keyword", match_type as "Match Type", campaign as "Campaign", ad_group as "Ad Group",
            impressions as "Impressions", clicks as "Clicks", ROUND(cost, 2) as "Cost",
            regs as "Registrations",
            ROUND(cost / NULLIF(clicks, 0), 2) as "CPC",
            ROUND(cost / NULLIF(regs, 0), 2) as "CPA",
            ROUND(100.0 * clicks / NULLIF(impressions, 0), 2) as "CTR %",
            ROUND(100.0 * regs / NULLIF(clicks, 0), 2) as "Conv Rate %"
        FROM kw_regs WHERE regs > 0 ORDER BY regs DESC, cost ASC
    ) TO '{out5}' (HEADER, DELIMITER ',');
    """)
    perf_count = con.execute("SELECT COUNT(*) FROM kw_regs WHERE regs > 0").fetchone()[0]
    print(f"  ✓ {out5} ({perf_count} converting keywords)")

    # ═══ FILE 6: Search Terms Linked ═══
    out6 = f"{prefix}_search_terms_linked_w12_13.csv"
    con.execute(f"""
    COPY (
        SELECT 
            st.search_term as "Search Term", st.keyword as "Keyword", st.match_type as "Match Type",
            st.campaign as "Campaign", st.ad_group as "Ad Group",
            st.impressions as "Impressions", st.clicks as "Clicks", ROUND(st.cost, 2) as "Cost",
            ROUND(st.cost / NULLIF(st.clicks, 0), 2) as "CPC",
            kr.regs as "Keyword Regs",
            ROUND(kr.cost / NULLIF(kr.regs, 0), 2) as "Keyword CPA",
            CASE WHEN kr.regs > 0 THEN 'Converting KW' ELSE 'Zero-Reg KW' END as "Keyword Status"
        FROM search_terms st
        LEFT JOIN kw_regs kr ON LOWER(st.keyword) = LOWER(kr.keyword) AND st.campaign = kr.campaign
        ORDER BY st.cost DESC
    ) TO '{out6}' (HEADER, DELIMITER ',');
    """)
    st_count = con.execute("SELECT COUNT(*) FROM search_terms").fetchone()[0]
    print(f"  ✓ {out6} ({st_count} search terms)")


# ── MAIN ──
con = duckdb.connect(':memory:')

# AU
run_market(con, "AU",
    kw_file="Search keyword report (11).csv",
    st_file="Search terms report (3).csv",
    reg_file="AU_Paid_Search_Registrations_by_Ref_Tag___Weeks_12_13_2026_2026_03_31T03_41_08.csv",
    reg_col_tag="ref_tag", reg_col_regs="total_regs",
    kw_skip_rows=2, kw_has_status=True,
    ref_join_mode='numeric_id'
)

# MX
run_market(con, "MX",
    kw_file="Search keyword report (12).csv",
    st_file="Search terms report (2).csv",
    reg_file="MX_Paid_Search_Registrations_by_Ref_Tag___Weeks_12_13_2026_2026_03_31T03_42_45.csv",
    reg_col_tag="ref_tag", reg_col_regs="total_regs",
    kw_skip_rows=2, kw_has_status=True,
    ref_join_mode='keyword_id'
)

print("\n── All files written to ~/  ──")
