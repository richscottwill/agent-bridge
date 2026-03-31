#!/usr/bin/env python3
"""AU Search Terms Analysis — negative candidates + keyword-to-search-term linkage"""
import duckdb

con = duckdb.connect(':memory:')

# Re-load all tables
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

con.execute("""
CREATE TABLE au_regs AS
SELECT 
    "Ref Tag" as ref_tag,
    TRY_CAST("Regs" AS INTEGER) as regs
FROM read_csv('AU_Paid_Search_Ref_Tag_Registrations___Weeks_9_13_Aggregated__VP_WL__2026_03_31T01_37_57.csv', 
    header=true, all_varchar=true, ignore_errors=true)
WHERE "Ref Tag" IS NOT NULL
""")

# Join keywords to regs
con.execute("""
CREATE TABLE au_kw_regs AS
SELECT 
    k.*,
    regexp_extract(final_url, 'ref[_=]([^&\\s]+)', 1) as ref_tag,
    COALESCE(r.regs, 0) as regs
FROM au_keywords k
LEFT JOIN au_regs r ON LOWER(regexp_extract(k.final_url, 'ref[_=]([^&\\s]+)', 1)) = LOWER(r.ref_tag)
""")

print("=" * 80)
print("AU SEARCH TERMS ANALYSIS — WEEKS 9-13")
print("=" * 80)

# ── SEARCH TERMS: High cost, linked to keywords with 0 regs ──
# First, let's see what search terms are driving spend on zero-reg keywords
print("\n── SEARCH TERMS ON ZERO-REG KEYWORDS (by cost) ──")
print("These search terms triggered keywords that produced zero registrations.\n")
rows = con.execute("""
SELECT 
    st.search_term,
    st.keyword,
    st.campaign,
    st.ad_group,
    st.match_type,
    st.impressions,
    st.clicks,
    st.cost
FROM au_search_terms st
INNER JOIN au_kw_regs kr ON LOWER(st.keyword) = LOWER(kr.keyword) AND st.campaign = kr.campaign
WHERE kr.regs = 0 AND st.cost > 0
ORDER BY st.cost DESC
LIMIT 30
""").fetchall()
print(f"{'Search Term':<45} {'Keyword':<40} {'Campaign':<25} {'Clk':>4} {'Cost':>8} {'Match':>15}")
print("-" * 145)
for r in rows:
    print(f"{r[0]:<45} {r[1]:<40} {r[2]:<25} {r[6]:>4} ${r[7]:>7,.2f} {r[4]:>15}")

# ── SEARCH TERMS: Potential negatives (high cost, low/no relevance signals) ──
print("\n── NEGATIVE KEYWORD CANDIDATES ──")
print("Search terms with high spend, low CTR, on non-converting keywords.\n")
rows = con.execute("""
SELECT 
    st.search_term,
    st.keyword,
    st.campaign,
    st.impressions,
    st.clicks,
    st.cost,
    ROUND(100.0 * st.clicks / NULLIF(st.impressions, 0), 2) as ctr,
    ROUND(st.cost / NULLIF(st.clicks, 0), 2) as cpc
FROM au_search_terms st
INNER JOIN au_kw_regs kr ON LOWER(st.keyword) = LOWER(kr.keyword) AND st.campaign = kr.campaign
WHERE kr.regs = 0 
    AND st.clicks >= 2
    AND st.cost > 5
ORDER BY st.cost DESC
LIMIT 30
""").fetchall()
print(f"{'Search Term':<45} {'Keyword':<35} {'Campaign':<25} {'Impr':>6} {'Clk':>4} {'Cost':>8} {'CTR':>6} {'CPC':>6}")
print("-" * 140)
for r in rows:
    print(f"{r[0]:<45} {r[1]:<35} {r[2]:<25} {r[3]:>6} {r[4]:>4} ${r[5]:>7,.2f} {r[6]:>5}% ${r[7]:>5}")

# ── SEARCH TERMS: Close variant / broad match leakage ──
print("\n── CLOSE VARIANT / BROAD MATCH LEAKAGE ──")
print("Search terms that matched via close variant or broad — potential intent mismatch.\n")
rows = con.execute("""
SELECT 
    st.search_term,
    st.keyword,
    st.match_type,
    st.campaign,
    st.clicks,
    st.cost,
    ROUND(st.cost / NULLIF(st.clicks, 0), 2) as cpc
FROM au_search_terms st
WHERE (st.match_type ILIKE '%close variant%' OR st.match_type ILIKE '%broad%')
    AND st.clicks >= 2
ORDER BY st.cost DESC
LIMIT 25
""").fetchall()
print(f"{'Search Term':<45} {'Keyword':<35} {'Match Type':<30} {'Clk':>4} {'Cost':>8} {'CPC':>6}")
print("-" * 135)
for r in rows:
    print(f"{r[0]:<45} {r[1]:<35} {r[2]:<30} {r[4]:>4} ${r[5]:>7,.2f} ${r[6]:>5}")

# ── SEARCH TERMS: Good performers (high clicks, on converting keywords) ──
print("\n── HIGH-VALUE SEARCH TERMS (on converting keywords) ──")
print("Search terms driving clicks on keywords that DO produce registrations.\n")
rows = con.execute("""
SELECT 
    st.search_term,
    st.keyword,
    st.campaign,
    st.clicks,
    st.cost,
    kr.regs as kw_regs,
    ROUND(kr.cost / NULLIF(kr.regs, 0), 2) as kw_cpr
FROM au_search_terms st
INNER JOIN au_kw_regs kr ON LOWER(st.keyword) = LOWER(kr.keyword) AND st.campaign = kr.campaign
WHERE kr.regs > 0
ORDER BY st.clicks DESC
LIMIT 25
""").fetchall()
print(f"{'Search Term':<45} {'Keyword':<35} {'Campaign':<25} {'Clk':>4} {'Cost':>8} {'KW Regs':>8} {'KW CPR':>8}")
print("-" * 140)
for r in rows:
    print(f"{r[0]:<45} {r[1]:<35} {r[2]:<25} {r[3]:>4} ${r[4]:>7,.2f} {r[5]:>8} ${r[6]:>7,.2f}")

# ── AD GROUP LEVEL: Efficiency ──
print("\n── AD GROUP EFFICIENCY (min $10 spend) ──")
rows = con.execute("""
SELECT 
    campaign,
    ad_group,
    SUM(impressions) as impr,
    SUM(clicks) as clicks,
    ROUND(SUM(cost), 2) as cost,
    SUM(regs) as regs,
    ROUND(SUM(cost) / NULLIF(SUM(clicks), 0), 2) as cpc,
    ROUND(SUM(cost) / NULLIF(SUM(regs), 0), 2) as cpr
FROM au_kw_regs
GROUP BY campaign, ad_group
HAVING SUM(cost) >= 10
ORDER BY cost DESC
LIMIT 30
""").fetchall()
print(f"{'Campaign':<30} {'Ad Group':<35} {'Impr':>7} {'Clk':>5} {'Cost':>9} {'Reg':>4} {'CPC':>6} {'CPR':>8}")
print("-" * 110)
for r in rows:
    cpr_str = f"${r[7]:.0f}" if r[7] else "N/A"
    print(f"{r[0]:<30} {r[1]:<35} {r[2]:>7,} {r[3]:>5,} ${r[4]:>8,.2f} {r[5]:>4} ${r[6]:>5} {cpr_str:>8}")

# ── REGISTRATION DISTRIBUTION ──
print("\n── REGISTRATION DISTRIBUTION BY REF TAG (top 20) ──")
rows = con.execute("""
SELECT ref_tag, regs FROM au_regs ORDER BY regs DESC LIMIT 20
""").fetchall()
print(f"{'Ref Tag':<60} {'Regs':>6}")
print("-" * 68)
for r in rows:
    print(f"{r[0]:<60} {r[1]:>6}")

# ── UNMATCHED REF TAGS (regs with no keyword match) ──
print("\n── UNMATCHED REF TAGS (regs exist but no keyword URL match) ──")
rows = con.execute("""
SELECT r.ref_tag, r.regs
FROM au_regs r
LEFT JOIN (
    SELECT DISTINCT LOWER(regexp_extract(final_url, 'ref[_=]([^&\\s]+)', 1)) as ref_tag
    FROM au_keywords
) k ON LOWER(r.ref_tag) = k.ref_tag
WHERE k.ref_tag IS NULL
ORDER BY r.regs DESC
LIMIT 15
""").fetchall()
if rows:
    print(f"{'Ref Tag':<60} {'Regs':>6}")
    print("-" * 68)
    for r in rows:
        print(f"{r[0]:<60} {r[1]:>6}")
else:
    print("All ref tags matched to keywords.")

print("\n")
