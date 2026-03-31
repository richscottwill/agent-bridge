#!/usr/bin/env python3
"""
Parse AU search terms report from stdin, aggregate by keyword.
Usage: python3 parse-au-search-terms.py < "Search terms report.csv"
Or: cat the CSV content and pipe it in.
"""
import csv
import sys
from collections import defaultdict

# Read from file argument or stdin
if len(sys.argv) > 1:
    f = open(sys.argv[1], 'r', encoding='utf-8-sig')
else:
    f = sys.stdin

keywords = defaultdict(lambda: {
    'clicks': 0, 'impr': 0, 'cost': 0.0,
    'campaign': '', 'ad_group': '', 'kw': '',
    'terms': []
})

reader = csv.DictReader(f)
for row in reader:
    st = row.get('Search term', '').strip()
    if st.startswith('Total:') or not st:
        continue
    kw = row.get('Keyword', '').strip()
    camp = row.get('Campaign', '').strip()
    ag = row.get('Ad group', '').strip()
    if not kw or not camp:
        continue
    
    cl = int(row.get('Clicks', '0').replace(',', ''))
    im = int(row.get('Impr.', '0').replace(',', ''))
    co = float(row.get('Cost', '0').replace(',', ''))
    
    key = f"{kw}||{camp}||{ag}"
    keywords[key]['clicks'] += cl
    keywords[key]['impr'] += im
    keywords[key]['cost'] += co
    keywords[key]['campaign'] = camp
    keywords[key]['ad_group'] = ag
    keywords[key]['kw'] = kw
    keywords[key]['terms'].append((st, cl, im, co))

if len(sys.argv) > 1:
    f.close()

# Zero-reg campaigns
zero_reg = {
    'AU_Generic', 'AU_Generic_P-V_Janitorial', 'AU_Generic_P-V_Office',
    'AU_Generic_P-V_Shops', 'AU_Generic_P-V_Apparel',
    'AU_Generic_P-V_Hospitality', 'AU_Generic_P-V_Materials',
    'AU_Generic_P-V_Safety', 'AU_Generic_P-V_Industry',
    'AU_Generic_P-V_Crafts', 'AU_Generic_P-V_Industrial',
    'AU_Generic_P-V_Pets', 'AU_Generic_P-V_Gym',
    'AU_Generic_P-V_Electronics', 'AU_Generic_P-V_Celebrations',
}

sorted_kw = sorted(keywords.items(), key=lambda x: -x[1]['cost'])

# --- SECTION A: All keywords by spend ---
print("=" * 130)
print("ALL KEYWORDS BY SPEND (top 80)")
print("=" * 130)
print(f"{'Keyword':<42} {'Campaign':<28} {'Ad Group':<32} {'Cl':>4} {'Imp':>6} {'Cost':>9} {'CPC':>7} {'Regs':>5}")
print("-" * 130)
for key, d in sorted_kw[:80]:
    cpc = d['cost']/d['clicks'] if d['clicks'] else 0
    reg = '0' if d['campaign'] in zero_reg else '?'
    if d['campaign'] in ('AU_Brand_Exact','AU_Brand_Phrase'):
        reg = 'BRAND'
    elif d['campaign'] == 'AU_Generic_P-V_Food':
        reg = 'FOOD?'
    elif d['campaign'] == 'AU_Generic_P-V_Beauty':
        reg = 'BEAU?'
    print(f"{d['kw']:<42} {d['campaign']:<28} {d['ad_group']:<32} {d['clicks']:>4} {d['impr']:>6} ${d['cost']:>7.2f} ${cpc:>5.2f} {reg:>5}")

# --- SECTION B: Zero-reg keywords by spend ---
print("\n" + "=" * 130)
print("ZERO-REGISTRATION KEYWORDS BY SPEND (top 100)")
print("Every keyword below had 0 registrations in W9-13 ref tags.")
print("=" * 130)
print(f"{'Keyword':<42} {'Campaign':<28} {'Ad Group':<32} {'Cl':>4} {'Imp':>6} {'Cost':>9} {'CPC':>7}")
print("-" * 130)
ztotal_cost = 0
ztotal_clicks = 0
zcount = 0
for key, d in sorted_kw:
    if d['campaign'] in zero_reg:
        cpc = d['cost']/d['clicks'] if d['clicks'] else 0
        if zcount < 100:
            print(f"{d['kw']:<42} {d['campaign']:<28} {d['ad_group']:<32} {d['clicks']:>4} {d['impr']:>6} ${d['cost']:>7.2f} ${cpc:>5.2f}")
        ztotal_cost += d['cost']
        ztotal_clicks += d['clicks']
        zcount += 1
print(f"\nTOTAL: {zcount} keywords, {ztotal_clicks} clicks, ${ztotal_cost:,.2f} spend — ALL with 0 registrations")

# --- SECTION C: Campaign totals ---
print("\n" + "=" * 130)
print("CAMPAIGN-LEVEL TOTALS")
print("=" * 130)
camp_totals = defaultdict(lambda: {'clicks': 0, 'impr': 0, 'cost': 0.0, 'kw_count': 0})
for key, d in keywords.items():
    c = d['campaign']
    camp_totals[c]['clicks'] += d['clicks']
    camp_totals[c]['impr'] += d['impr']
    camp_totals[c]['cost'] += d['cost']
    camp_totals[c]['kw_count'] += 1

reg_map = {
    'AU_Brand_Exact': '~400+', 'AU_Brand_Phrase': '~85',
    'AU_Generic_P-V_Food': '~100', 'AU_Generic_P-V_Beauty': '~48',
    'AU_Generic_P-V_Electronics': '~18', 'AU_Generic_P-V_Celebrations': '~10',
}
print(f"{'Campaign':<35} {'KWs':>5} {'Clicks':>7} {'Impr':>9} {'Cost':>11} {'Regs':>7} {'CPA':>8}")
print("-" * 90)
for c, t in sorted(camp_totals.items(), key=lambda x: -x[1]['cost']):
    regs = reg_map.get(c, '0')
    cpa = ''
    if regs not in ('0', '~18', '~10'):
        try:
            r = int(regs.replace('~','').replace('+',''))
            cpa = f"${t['cost']/r:.2f}"
        except:
            pass
    print(f"{c:<35} {t['kw_count']:>5} {t['clicks']:>7} {t['impr']:>9} ${t['cost']:>9,.2f} {regs:>7} {cpa:>8}")

# --- SECTION D: Top bloat search terms in zero-reg campaigns ---
print("\n" + "=" * 130)
print("TOP BLOAT SEARCH TERMS (zero-reg campaigns, sorted by cost)")
print("=" * 130)
all_zero_terms = []
for key, d in keywords.items():
    if d['campaign'] in zero_reg:
        for st, cl, im, co in d['terms']:
            all_zero_terms.append((st, cl, im, co, d['kw'], d['campaign'], d['ad_group']))

all_zero_terms.sort(key=lambda x: -x[3])
print(f"{'Search Term':<55} {'Keyword':<35} {'Campaign':<25} {'Cl':>3} {'Imp':>5} {'Cost':>8}")
print("-" * 140)
for st, cl, im, co, kw, camp, ag in all_zero_terms[:150]:
    print(f"{st:<55} {kw:<35} {camp:<25} {cl:>3} {im:>5} ${co:>6.2f}")

print("\nDone.")
