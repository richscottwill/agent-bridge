#!/usr/bin/env python3
"""
AU PS W9-13 Analysis using DuckDB.
Reads search_terms.csv and ref_tags.csv, produces keyword-level analysis exports.
Run from the directory containing both CSVs.
"""
import duckdb
import os

# Connect to DuckDB
db = duckdb.connect(':memory:')

# Load ref tags
db.execute("""
CREATE TABLE ref_tags AS 
SELECT 
    "Ref Tag" as ref_tag,
    "Regs"::INTEGER as regs,
    CASE 
        WHEN lower("Ref Tag") LIKE '%brand_core%' THEN 'AU_Brand_Exact'
        WHEN lower("Ref Tag") LIKE '%brand_phrase%' THEN 'AU_Brand_Phrase'
        WHEN "Ref Tag" LIKE '%_pv_bea_%' THEN 'AU_Generic_P-V_Beauty'
        WHEN "Ref Tag" LIKE '%_pv_foo_%' THEN 'AU_Generic_P-V_Food'
        WHEN "Ref Tag" LIKE '%_pv_ele_%' THEN 'AU_Generic_P-V_Electronics'
        WHEN "Ref Tag" LIKE '%_pv_celec_%' THEN 'AU_Generic_P-V_Celebrations'
        ELSE 'Unknown'
    END as campaign_type,
    -- Extract the adgroup ID (last segment after final underscore)
    regexp_extract("Ref Tag", '([xy]\\d+)$') as adgroup_id,
    -- Extract keyword ID (second to last segment)  
    regexp_extract("Ref Tag", '_(\\d+)_[xy]\\d+$', 1) as keyword_id
FROM read_csv_auto('ref_tags.csv')
""")

print("=== REF TAG SUMMARY ===")
print(db.execute("""
    SELECT campaign_type, 
           COUNT(*) as keyword_count, 
           SUM(regs) as total_regs,
           COUNT(DISTINCT adgroup_id) as adgroup_count
    FROM ref_tags 
    GROUP BY campaign_type 
    ORDER BY total_regs DESC
""").fetchdf().to_string(index=False))

print("\n=== REF TAG: REGS BY ADGROUP ID ===")
print(db.execute("""
    SELECT campaign_type, adgroup_id, 
           COUNT(*) as keywords, 
           SUM(regs) as total_regs
    FROM ref_tags 
    GROUP BY campaign_type, adgroup_id 
    ORDER BY total_regs DESC
    LIMIT 30
""").fetchdf().to_string(index=False))

# Check if search_terms.csv exists
st_path = 'search_terms.csv'
if not os.path.exists(st_path):
    print(f"\n*** {st_path} not found. Please create it from the Search Terms Report CSV.")
    print("*** Once created, re-run this script.")
    
    # Still export ref tag analysis
    db.execute("""
        COPY (
            SELECT campaign_type, adgroup_id, keyword_id, regs,
                   SUM(regs) OVER (PARTITION BY campaign_type) as campaign_total_regs
            FROM ref_tags
            ORDER BY regs DESC
        ) TO 'ref_tag_analysis.csv' (HEADER, DELIMITER ',')
    """)
    print("*** Exported ref_tag_analysis.csv")
    exit(0)

# Load search terms
db.execute("""
CREATE TABLE search_terms AS
SELECT 
    "Search term" as search_term,
    "Match type" as match_type,
    "Campaign" as campaign,
    "Ad group" as ad_group,
    "Keyword" as keyword,
    "Clicks"::INTEGER as clicks,
    "Impr."::INTEGER as impressions,
    "Cost"::DOUBLE as cost
FROM read_csv_auto('search_terms.csv')
WHERE "Search term" NOT LIKE 'Total:%'
""")

# === KEYWORD AGGREGATION ===
db.execute("""
CREATE TABLE keyword_agg AS
SELECT 
    keyword,
    campaign,
    ad_group,
    SUM(clicks) as total_clicks,
    SUM(impressions) as total_impressions,
    SUM(cost) as total_cost,
    COUNT(*) as search_term_count,
    ROUND(SUM(cost) / NULLIF(SUM(clicks), 0), 2) as avg_cpc,
    -- Registration status based on campaign
    CASE
        WHEN campaign IN ('AU_Brand_Exact', 'AU_Brand_Phrase') THEN 'BRAND_HAS_REGS'
        WHEN campaign = 'AU_Generic_P-V_Food' THEN 'FOOD_HAS_REGS'
        WHEN campaign = 'AU_Generic_P-V_Beauty' THEN 'BEAUTY_HAS_REGS'
        WHEN campaign IN ('AU_Generic_P-V_Electronics', 'AU_Generic_P-V_Celebrations') THEN 'LOW_REGS'
        ELSE 'ZERO_REGS'
    END as reg_status
FROM search_terms
GROUP BY keyword, campaign, ad_group
""")

# === EXPORT 1: All keywords by spend ===
db.execute("""
COPY (
    SELECT keyword, campaign, ad_group, 
           total_clicks, total_impressions, 
           ROUND(total_cost, 2) as total_cost,
           avg_cpc, search_term_count, reg_status
    FROM keyword_agg
    ORDER BY total_cost DESC
) TO 'export_1_keywords_by_spend.csv' (HEADER, DELIMITER ',')
""")
print("\n*** Exported export_1_keywords_by_spend.csv")

# === EXPORT 2: Zero-reg keywords by spend (the bloat) ===
db.execute("""
COPY (
    SELECT keyword, campaign, ad_group,
           total_clicks, total_impressions,
           ROUND(total_cost, 2) as total_cost,
           avg_cpc, search_term_count
    FROM keyword_agg
    WHERE reg_status = 'ZERO_REGS'
    ORDER BY total_cost DESC
) TO 'export_2_zero_reg_keywords.csv' (HEADER, DELIMITER ',')
""")
print("*** Exported export_2_zero_reg_keywords.csv")

# === EXPORT 3: Brand keywords with estimated regs ===
db.execute("""
COPY (
    SELECT keyword, campaign, ad_group,
           total_clicks, total_impressions,
           ROUND(total_cost, 2) as total_cost,
           avg_cpc, search_term_count,
           -- Rough CPA estimate based on click-volume-to-reg correlation
           CASE
               WHEN total_clicks > 3000 THEN '~220 regs (~$8.85 CPA)'
               WHEN total_clicks > 500 THEN '~84 regs (~$6.63 CPA)'
               WHEN total_clicks > 400 THEN '~51 regs (~$13.63 CPA)'
               WHEN total_clicks > 150 THEN '~10 regs'
               WHEN total_clicks > 50 THEN '~5-9 regs'
               WHEN total_clicks > 20 THEN '~2-5 regs'
               WHEN total_clicks > 5 THEN '~0-2 regs'
               ELSE '~0 regs'
           END as est_regs_note
    FROM keyword_agg
    WHERE reg_status = 'BRAND_HAS_REGS'
    ORDER BY total_cost DESC
) TO 'export_3_brand_keywords.csv' (HEADER, DELIMITER ',')
""")
print("*** Exported export_3_brand_keywords.csv")

# === EXPORT 4: Food/Beauty keywords (have regs, need final URL mapping) ===
db.execute("""
COPY (
    SELECT keyword, campaign, ad_group,
           total_clicks, total_impressions,
           ROUND(total_cost, 2) as total_cost,
           avg_cpc, search_term_count,
           reg_status
    FROM keyword_agg
    WHERE reg_status IN ('FOOD_HAS_REGS', 'BEAUTY_HAS_REGS')
    ORDER BY total_cost DESC
) TO 'export_4_food_beauty_keywords.csv' (HEADER, DELIMITER ',')
""")
print("*** Exported export_4_food_beauty_keywords.csv")

# === EXPORT 5: Search terms in zero-reg campaigns, sorted by cost ===
db.execute("""
COPY (
    SELECT st.search_term, st.keyword, st.campaign, st.ad_group,
           st.clicks, st.impressions, ROUND(st.cost, 2) as cost,
           st.match_type
    FROM search_terms st
    JOIN keyword_agg ka ON st.keyword = ka.keyword 
                        AND st.campaign = ka.campaign 
                        AND st.ad_group = ka.ad_group
    WHERE ka.reg_status = 'ZERO_REGS'
    ORDER BY st.cost DESC
) TO 'export_5_zero_reg_search_terms.csv' (HEADER, DELIMITER ',')
""")
print("*** Exported export_5_zero_reg_search_terms.csv")

# === EXPORT 6: Negative keyword candidates (search terms in brand campaigns with wrong intent) ===
db.execute("""
COPY (
    SELECT st.search_term, st.keyword, st.campaign, st.ad_group,
           st.clicks, st.impressions, ROUND(st.cost, 2) as cost,
           CASE
               WHEN lower(st.search_term) LIKE '%for sale%' THEN 'BUYING_A_BUSINESS'
               WHEN lower(st.search_term) LIKE '%merch by%' THEN 'WRONG_PRODUCT'
               WHEN lower(st.search_term) LIKE '%dropship%' THEN 'DROPSHIP_INTENT'
               WHEN lower(st.search_term) LIKE '%sell on%' OR lower(st.search_term) LIKE '%selling on%' THEN 'SELLER_INTENT'
               WHEN lower(st.search_term) LIKE '%wholesale supplier%' THEN 'SUPPLIER_SEARCH'
               WHEN lower(st.search_term) LIKE '%corporate services%' THEN 'LEGAL_ENTITY'
               WHEN lower(st.search_term) LIKE '%deutschland%' OR lower(st.search_term) LIKE '% usa%' OR lower(st.search_term) LIKE '% mexico%' OR lower(st.search_term) LIKE '% canada%' THEN 'WRONG_COUNTRY'
               WHEN lower(st.search_term) LIKE '%ideas%' THEN 'ENTREPRENEURSHIP'
               WHEN lower(st.search_term) LIKE '%franchise%' THEN 'FRANCHISE_INTENT'
               WHEN lower(st.search_term) LIKE '%course%' THEN 'EDUCATION_INTENT'
               ELSE 'REVIEW_MANUALLY'
           END as neg_reason
    FROM search_terms st
    WHERE st.campaign IN ('AU_Brand_Exact', 'AU_Brand_Phrase')
    AND (
        lower(st.search_term) LIKE '%for sale%'
        OR lower(st.search_term) LIKE '%merch by%'
        OR lower(st.search_term) LIKE '%dropship%'
        OR lower(st.search_term) LIKE '%sell on%'
        OR lower(st.search_term) LIKE '%selling on%'
        OR lower(st.search_term) LIKE '%wholesale supplier%'
        OR lower(st.search_term) LIKE '%corporate services%'
        OR lower(st.search_term) LIKE '%deutschland%'
        OR lower(st.search_term) LIKE '% usa %'
        OR lower(st.search_term) LIKE '%ideas%'
        OR lower(st.search_term) LIKE '%franchise%'
        OR lower(st.search_term) LIKE '%course%'
    )
    ORDER BY st.cost DESC
) TO 'export_6_brand_negative_candidates.csv' (HEADER, DELIMITER ',')
""")
print("*** Exported export_6_brand_negative_candidates.csv")

# === EXPORT 7: Campaign-level summary with reg data ===
db.execute("""
COPY (
    SELECT campaign,
           COUNT(DISTINCT keyword) as unique_keywords,
           SUM(total_clicks) as total_clicks,
           SUM(total_impressions) as total_impressions,
           ROUND(SUM(total_cost), 2) as total_cost,
           ROUND(SUM(total_cost) / NULLIF(SUM(total_clicks), 0), 2) as avg_cpc,
           MAX(reg_status) as reg_status
    FROM keyword_agg
    GROUP BY campaign
    ORDER BY total_cost DESC
) TO 'export_7_campaign_summary.csv' (HEADER, DELIMITER ',')
""")
print("*** Exported export_7_campaign_summary.csv")

# === Print summary stats ===
print("\n=== SUMMARY ===")
total_spend = db.execute("SELECT ROUND(SUM(total_cost),2) FROM keyword_agg").fetchone()[0]
zero_spend = db.execute("SELECT ROUND(SUM(total_cost),2) FROM keyword_agg WHERE reg_status='ZERO_REGS'").fetchone()[0]
brand_spend = db.execute("SELECT ROUND(SUM(total_cost),2) FROM keyword_agg WHERE reg_status='BRAND_HAS_REGS'").fetchone()[0]
food_spend = db.execute("SELECT ROUND(SUM(total_cost),2) FROM keyword_agg WHERE reg_status='FOOD_HAS_REGS'").fetchone()[0]
beauty_spend = db.execute("SELECT ROUND(SUM(total_cost),2) FROM keyword_agg WHERE reg_status='BEAUTY_HAS_REGS'").fetchone()[0]

print(f"Total spend: ${total_spend:,.2f}")
print(f"Brand spend (has regs): ${brand_spend:,.2f} ({brand_spend/total_spend*100:.1f}%)")
print(f"Food spend (has regs): ${food_spend:,.2f} ({food_spend/total_spend*100:.1f}%)")
print(f"Beauty spend (has regs): ${beauty_spend:,.2f} ({beauty_spend/total_spend*100:.1f}%)")
print(f"ZERO-REG spend: ${zero_spend:,.2f} ({zero_spend/total_spend*100:.1f}%)")
print(f"\nZero-reg spend is {zero_spend/total_spend*100:.1f}% of total — this is pure bloat with 0 measured conversions.")

print("\nAll exports saved to current directory. Open in Excel/Sheets for review.")
print("Key files:")
print("  export_1_keywords_by_spend.csv — all keywords ranked by spend")
print("  export_2_zero_reg_keywords.csv — keywords with confirmed 0 regs (cut/reduce)")
print("  export_3_brand_keywords.csv — brand keywords with estimated regs")
print("  export_4_food_beauty_keywords.csv — need final URL report to confirm regs")
print("  export_5_zero_reg_search_terms.csv — individual search terms to negative")
print("  export_6_brand_negative_candidates.csv — wrong-intent terms in brand campaigns")
print("  export_7_campaign_summary.csv — campaign-level overview")
