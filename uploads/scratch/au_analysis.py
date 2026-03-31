#!/usr/bin/env python3
"""AU Paid Search Weeks 9-13 Analysis — Keyword + Search Term + Registration linkage"""
import duckdb

con = duckdb.connect(':memory:')

# ── 1. Load AU Keyword Report (tab-delimited, converted from UTF-16LE) ──
con.execute("""
CREATE TABLE au_keywords AS
SELECT 
    "Keyword" as keyword,
    "Match type" as match_type,
    "Campaign" as campaign,
    "Ad group" as ad_group,
    "Final URL" as final_url,
    TRY_CAST(REPLACE(REPLACE("Impr.", ',', ''), '"', '') AS INTEGER) as impressions,
    TRY_CAST(REPLACE(REPLACE("Clicks", ',', ''), '"', '') AS INTEGER) as clicks,
    TRY_CAST(REPLACE(REPLACE("Cost", ',', ''), '"', '') AS DOUBLE) as cost
FROM read_csv('kw_report_au_utf8.csv', delim='\t', header=true, all_varchar=true, ignore_errors=true)
WHERE "Keyword" IS NOT NULL AND "Keyword" != ''
""")

# ── 2. Load AU Search Terms Report (comma-delimited) ──
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

# ── 3. Load AU Registrations (comma-delimited) ──
con.execute("""
CREATE TABLE au_regs AS
SELECT 
    "Ref Tag" as ref_tag,
    TRY_CAST("Regs" AS INTEGER) as regs
FROM read_csv('AU_Paid_Search_Ref_Tag_Registrations___Weeks_9_13_Aggregated__VP_WL__2026_03_31T01_37_57.csv', 
    header=true, all_varchar=true, ignore_errors=true)
WHERE "Ref Tag" IS NOT NULL
""")

# ── 4. Extract ref_tag from keyword final URLs ──
con.execute("""
CREATE TABLE au_kw_with_ref AS
SELECT 
    k.*,
    regexp_extract(final_url, 'ref[_=]([^&\\s]+)', 1) as ref_tag
FROM au_keywords k
""")

# ── 5. Join keywords to registrations via ref_tag ──
con.execute("""
CREATE TABLE au_kw_regs AS
SELECT 
    k.keyword,
    k.match_type,
    k.campaign,
    k.ad_group,
    k.impressions,
    k.clicks,
    k.cost,
    k.ref_tag,
    COALESCE(r.regs, 0) as regs,
    CASE WHEN k.clicks > 0 THEN ROUND(k.cost / k.clicks, 2) ELSE NULL END as cpc,
    CASE WHEN COALESCE(r.regs, 0) > 0 THEN ROUND(k.cost / r.regs, 2) ELSE NULL END as cost_per_reg,
    CASE WHEN k.impressions > 0 THEN ROUND(100.0 * k.clicks / k.impressions, 2) ELSE NULL END as ctr
FROM au_kw_with_ref k
LEFT JOIN au_regs r ON LOWER(k.ref_tag) = LOWER(r.ref_tag)
""")

print("=" * 80)
print("AU PAID SEARCH — WEEKS 9-13 ANALYSIS")
print("=" * 80)

# ── OVERVIEW ──
print("\n── OVERVIEW ──")
result = con.execute("""
SELECT 
    COUNT(*) as total_keywords,
    SUM(impressions) as total_impr,
    SUM(clicks) as total_clicks,
    ROUND(SUM(cost), 2) as total_cost,
    SUM(regs) as total_regs,
    ROUND(SUM(cost) / NULLIF(SUM(regs), 0), 2) as overall_cpr,
    ROUND(SUM(cost) / NULLIF(SUM(clicks), 0), 2) as overall_cpc,
    ROUND(100.0 * SUM(clicks) / NULLIF(SUM(impressions), 0), 2) as overall_ctr
FROM au_kw_regs
""").fetchone()
print(f"Keywords: {result[0]} | Impr: {result[1]:,} | Clicks: {result[2]:,} | Cost: ${result[3]:,.2f}")
print(f"Regs: {result[4]} | CPR: ${result[5]} | CPC: ${result[6]} | CTR: {result[7]}%")

# ── CAMPAIGN-LEVEL SUMMARY ──
print("\n── CAMPAIGN-LEVEL SUMMARY (by cost) ──")
rows = con.execute("""
SELECT 
    campaign,
    SUM(impressions) as impr,
    SUM(clicks) as clicks,
    ROUND(SUM(cost), 2) as cost,
    SUM(regs) as regs,
    ROUND(SUM(cost) / NULLIF(SUM(clicks), 0), 2) as cpc,
    ROUND(SUM(cost) / NULLIF(SUM(regs), 0), 2) as cpr,
    ROUND(100.0 * SUM(clicks) / NULLIF(SUM(impressions), 0), 2) as ctr
FROM au_kw_regs
GROUP BY campaign
ORDER BY cost DESC
""").fetchall()
print(f"{'Campaign':<40} {'Impr':>8} {'Clicks':>7} {'Cost':>10} {'Regs':>5} {'CPC':>7} {'CPR':>8} {'CTR':>6}")
print("-" * 95)
for r in rows:
    cpr_str = f"${r[6]}" if r[6] else "N/A"
    print(f"{r[0]:<40} {r[1]:>8,} {r[2]:>7,} ${r[3]:>9,.2f} {r[4]:>5} ${r[5]:>6} {cpr_str:>8} {r[7]:>5}%")

# ── TOP KEYWORDS BY COST (with regs) ──
print("\n── TOP 30 KEYWORDS BY COST ──")
rows = con.execute("""
SELECT keyword, campaign, impressions, clicks, cost, regs, cpc, cost_per_reg, ctr
FROM au_kw_regs
ORDER BY cost DESC
LIMIT 30
""").fetchall()
print(f"{'Keyword':<50} {'Campaign':<30} {'Impr':>6} {'Clk':>5} {'Cost':>8} {'Reg':>4} {'CPC':>6} {'CPR':>8} {'CTR':>5}")
print("-" * 130)
for r in rows:
    cpr_str = f"${r[7]:.0f}" if r[7] else "N/A"
    print(f"{r[0]:<50} {r[1]:<30} {r[2]:>6,} {r[3]:>5,} ${r[4]:>7,.2f} {r[5]:>4} ${r[6]:>5} {cpr_str:>8} {r[8]:>4}%")

# ── HIGH COST, ZERO REGS (waste candidates) ──
print("\n── HIGH COST, ZERO REGS — OPTIMIZATION CANDIDATES ──")
rows = con.execute("""
SELECT keyword, campaign, ad_group, impressions, clicks, cost, cpc, ctr
FROM au_kw_regs
WHERE regs = 0 AND cost > 0
ORDER BY cost DESC
LIMIT 30
""").fetchall()
print(f"{'Keyword':<55} {'Campaign':<30} {'Impr':>6} {'Clk':>5} {'Cost':>8} {'CPC':>6} {'CTR':>5}")
print("-" * 120)
for r in rows:
    print(f"{r[0]:<55} {r[1]:<30} {r[3]:>6,} {r[4]:>5,} ${r[5]:>7,.2f} ${r[6]:>5} {r[7]:>4}%")

# ── BEST PERFORMERS (lowest CPR with meaningful volume) ──
print("\n── BEST PERFORMERS — LOWEST CPR (min 3 regs) ──")
rows = con.execute("""
SELECT keyword, campaign, impressions, clicks, cost, regs, cpc, cost_per_reg, ctr
FROM au_kw_regs
WHERE regs >= 3
ORDER BY cost_per_reg ASC
LIMIT 20
""").fetchall()
print(f"{'Keyword':<50} {'Campaign':<30} {'Impr':>6} {'Clk':>5} {'Cost':>8} {'Reg':>4} {'CPC':>6} {'CPR':>8} {'CTR':>5}")
print("-" * 130)
for r in rows:
    print(f"{r[0]:<50} {r[1]:<30} {r[2]:>6,} {r[3]:>5,} ${r[4]:>7,.2f} {r[5]:>4} ${r[6]:>5} ${r[7]:>7,.2f} {r[8]:>4}%")

# ── HIGH CPC KEYWORDS (CPC optimization candidates) ──
print("\n── HIGH CPC KEYWORDS (>$5 CPC, min 5 clicks) ──")
rows = con.execute("""
SELECT keyword, campaign, impressions, clicks, cost, regs, cpc, cost_per_reg, ctr
FROM au_kw_regs
WHERE cpc > 5 AND clicks >= 5
ORDER BY cpc DESC
LIMIT 20
""").fetchall()
print(f"{'Keyword':<50} {'Campaign':<30} {'Impr':>6} {'Clk':>5} {'Cost':>8} {'Reg':>4} {'CPC':>6} {'CPR':>8} {'CTR':>5}")
print("-" * 130)
for r in rows:
    cpr_str = f"${r[7]:.0f}" if r[7] else "N/A"
    print(f"{r[0]:<50} {r[1]:<30} {r[2]:>6,} {r[3]:>5,} ${r[4]:>7,.2f} {r[5]:>4} ${r[6]:>5} {cpr_str:>8} {r[8]:>4}%")

print("\n")
