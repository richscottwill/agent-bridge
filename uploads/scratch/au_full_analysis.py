#!/usr/bin/env python3
"""AU Paid Search Weeks 9-13 — Full Analysis with correct ref tag join"""
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

# ── JOIN: Keywords to Registrations via numeric ID ──
con.execute("""
CREATE TABLE au_kw_regs AS
SELECT 
    k.keyword, k.match_type, k.campaign, k.ad_group,
    k.impressions, k.clicks, k.cost, k.kw_numeric_id,
    COALESCE(SUM(r.regs), 0) as regs,
    CASE WHEN k.clicks > 0 THEN ROUND(k.cost / k.clicks, 2) ELSE NULL END as cpc,
    CASE WHEN COALESCE(SUM(r.regs), 0) > 0 THEN ROUND(k.cost / SUM(r.regs), 2) ELSE NULL END as cost_per_reg,
    CASE WHEN k.impressions > 0 THEN ROUND(100.0 * k.clicks / k.impressions, 2) ELSE NULL END as ctr
FROM au_keywords k
LEFT JOIN au_regs r ON k.kw_numeric_id = r.reg_numeric_id
GROUP BY k.keyword, k.match_type, k.campaign, k.ad_group, k.impressions, k.clicks, k.cost, k.kw_numeric_id
""")

# ── Verify join worked ──
result = con.execute("SELECT SUM(regs) FROM au_kw_regs WHERE regs > 0").fetchone()
print(f"Total regs matched to keywords: {result[0]}")
result2 = con.execute("SELECT SUM(regs) FROM au_regs").fetchone()
print(f"Total regs in source: {result2[0]}")
result3 = con.execute("SELECT COUNT(*) FROM au_kw_regs WHERE regs > 0").fetchone()
print(f"Keywords with regs: {result3[0]}")

print("\n" + "=" * 90)
print("AU PAID SEARCH — WEEKS 9-13 FULL ANALYSIS (CORRECT REG LINKAGE)")
print("=" * 90)

# ── OVERVIEW ──
print("\n── OVERVIEW ──")
r = con.execute("""
SELECT COUNT(*), SUM(impressions), SUM(clicks), ROUND(SUM(cost),2), SUM(regs),
    ROUND(SUM(cost)/NULLIF(SUM(regs),0),2), ROUND(SUM(cost)/NULLIF(SUM(clicks),0),2),
    ROUND(100.0*SUM(clicks)/NULLIF(SUM(impressions),0),2)
FROM au_kw_regs
""").fetchone()
print(f"Keywords: {r[0]} | Impr: {r[1]:,} | Clicks: {r[2]:,} | Cost: ${r[3]:,.2f}")
print(f"Regs: {r[4]} | CPR: ${r[5]} | CPC: ${r[6]} | CTR: {r[7]}%")

# ── CAMPAIGN SUMMARY ──
print("\n── CAMPAIGN SUMMARY ──")
rows = con.execute("""
SELECT campaign, SUM(impressions) as impr, SUM(clicks) as clicks, ROUND(SUM(cost),2) as cost,
    SUM(regs) as regs, ROUND(SUM(cost)/NULLIF(SUM(clicks),0),2) as cpc,
    ROUND(SUM(cost)/NULLIF(SUM(regs),0),2) as cpr,
    ROUND(100.0*SUM(clicks)/NULLIF(SUM(impressions),0),2) as ctr
FROM au_kw_regs GROUP BY campaign ORDER BY cost DESC
""").fetchall()
print(f"{'Campaign':<35} {'Impr':>8} {'Clicks':>7} {'Cost':>10} {'Regs':>5} {'CPC':>7} {'CPR':>9} {'CTR':>6}")
for r in rows:
    cpr = f"${r[6]:,.0f}" if r[6] else "N/A"
    print(f"{r[0]:<35} {r[1]:>8,} {r[2]:>7,} ${r[3]:>9,.2f} {r[4]:>5} ${r[5]:>6} {cpr:>9} {r[7]:>5}%")

# ── TOP KEYWORDS BY REGS ──
print("\n── TOP KEYWORDS BY REGISTRATIONS ──")
rows = con.execute("""
SELECT keyword, campaign, impressions, clicks, cost, regs, cpc, cost_per_reg, ctr
FROM au_kw_regs WHERE regs > 0 ORDER BY regs DESC LIMIT 25
""").fetchall()
print(f"{'Keyword':<45} {'Campaign':<30} {'Clk':>5} {'Cost':>8} {'Reg':>4} {'CPC':>6} {'CPR':>8}")
for r in rows:
    print(f"{r[0]:<45} {r[1]:<30} {r[3]:>5,} ${r[4]:>7,.2f} {r[5]:>4} ${r[6]:>5} ${r[7]:>7,.2f}")

# ── HIGH COST ZERO REGS ──
print("\n── TOP 25 HIGHEST COST KEYWORDS WITH ZERO REGS ──")
rows = con.execute("""
SELECT keyword, campaign, ad_group, impressions, clicks, cost, cpc, ctr
FROM au_kw_regs WHERE regs = 0 AND cost > 0 ORDER BY cost DESC LIMIT 25
""").fetchall()
print(f"{'Keyword':<50} {'Campaign':<30} {'Clk':>5} {'Cost':>9} {'CPC':>6} {'CTR':>5}")
for r in rows:
    print(f"{r[0]:<50} {r[1]:<30} {r[4]:>5,} ${r[5]:>8,.2f} ${r[6]:>5} {r[7]:>4}%")

# ── HIGH CPC (>$8, min 10 clicks) ──
print("\n── HIGH CPC KEYWORDS (>$8, min 10 clicks) — CPC REDUCTION CANDIDATES ──")
rows = con.execute("""
SELECT keyword, campaign, impressions, clicks, cost, regs, cpc, cost_per_reg, ctr
FROM au_kw_regs WHERE cpc > 8 AND clicks >= 10 ORDER BY cpc DESC LIMIT 20
""").fetchall()
print(f"{'Keyword':<50} {'Campaign':<25} {'Clk':>5} {'Cost':>8} {'Reg':>4} {'CPC':>7} {'CPR':>8}")
for r in rows:
    cpr = f"${r[7]:.0f}" if r[7] else "N/A"
    print(f"{r[0]:<50} {r[1]:<25} {r[3]:>5,} ${r[4]:>7,.2f} {r[5]:>4} ${r[6]:>6} {cpr:>8}")

# ── SEARCH TERMS: Negative candidates ──
print("\n── SEARCH TERM NEGATIVE CANDIDATES ──")
print("(High cost search terms on zero-reg keywords, min 3 clicks)")
rows = con.execute("""
SELECT st.search_term, st.keyword, st.campaign, st.match_type, st.clicks, st.cost,
    ROUND(st.cost/NULLIF(st.clicks,0),2) as st_cpc
FROM au_search_terms st
INNER JOIN au_kw_regs kr ON LOWER(st.keyword) = LOWER(kr.keyword) AND st.campaign = kr.campaign
WHERE kr.regs = 0 AND st.clicks >= 3 AND st.cost > 10
ORDER BY st.cost DESC LIMIT 30
""").fetchall()
print(f"{'Search Term':<42} {'Keyword':<35} {'Campaign':<25} {'Clk':>4} {'Cost':>8} {'CPC':>6}")
for r in rows:
    print(f"{r[0]:<42} {r[1]:<35} {r[2]:<25} {r[4]:>4} ${r[5]:>7,.2f} ${r[6]:>5}")

# ── CLOSE VARIANT LEAKAGE on zero-reg keywords ──
print("\n── CLOSE VARIANT LEAKAGE ON ZERO-REG KEYWORDS ──")
rows = con.execute("""
SELECT st.search_term, st.keyword, st.campaign, st.match_type, st.clicks, st.cost,
    ROUND(st.cost/NULLIF(st.clicks,0),2) as st_cpc
FROM au_search_terms st
INNER JOIN au_kw_regs kr ON LOWER(st.keyword) = LOWER(kr.keyword) AND st.campaign = kr.campaign
WHERE kr.regs = 0 
    AND (st.match_type ILIKE '%close variant%')
    AND st.clicks >= 2 AND st.cost > 5
ORDER BY st.cost DESC LIMIT 25
""").fetchall()
print(f"{'Search Term':<42} {'Keyword':<35} {'Match':<28} {'Clk':>4} {'Cost':>8}")
for r in rows:
    print(f"{r[0]:<42} {r[1]:<35} {r[3]:<28} {r[4]:>4} ${r[5]:>7,.2f}")

# ── SEARCH TERMS driving regs (on converting keywords) ──
print("\n── SEARCH TERMS ON CONVERTING KEYWORDS (top clicks) ──")
rows = con.execute("""
SELECT st.search_term, st.keyword, st.campaign, st.clicks, st.cost,
    kr.regs as kw_regs, kr.cost_per_reg as kw_cpr
FROM au_search_terms st
INNER JOIN au_kw_regs kr ON LOWER(st.keyword) = LOWER(kr.keyword) AND st.campaign = kr.campaign
WHERE kr.regs > 0
ORDER BY st.clicks DESC LIMIT 20
""").fetchall()
print(f"{'Search Term':<45} {'Keyword':<35} {'Clk':>4} {'Cost':>8} {'KW Regs':>7} {'KW CPR':>8}")
for r in rows:
    cpr = f"${r[6]:.0f}" if r[6] else "N/A"
    print(f"{r[0]:<45} {r[1]:<35} {r[3]:>4} ${r[4]:>7,.2f} {r[5]:>7} {cpr:>8}")

print("\n")
