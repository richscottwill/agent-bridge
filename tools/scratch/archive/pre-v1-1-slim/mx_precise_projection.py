#!/usr/bin/env python3
"""MX 2026 Precise Week-by-Week Projection Engine."""
import math

BRAND_CCP = 97
NB_CCP = 28

# YTD 2026 actuals W2-W16 (W1 blank in source)
YTD_2026 = [
    (2, 155, 97, 1443.47, 7206.68), (3, 153, 117, 2945.94, 9875.35),
    (4, 123, 117, 3194.64, 11477.25), (5, 130, 94, 3066.45, 13705.13),
    (6, 140, 89, 3691.29, 11839.18), (7, 157, 88, 3632.99, 10362.11),
    (8, 270, 98, 4837.86, 13830.98), (9, 166, 96, 4266.32, 15466.62),
    (10, 199, 98, 4312.51, 16196.20), (11, 243, 146, 4706.24, 17755.30),
    (12, 202, 121, 4116.86, 16016.77), (13, 210, 140, 4436.56, 18783.03),
    (14, 179, 124, 3319.73, 16097.80), (15, 367, 142, 5281.81, 20162.53),
    (16, 395, 115, 6129.49, 21087.26),
]
ytd_brand = sum(r[1] for r in YTD_2026)
ytd_nb = sum(r[2] for r in YTD_2026)
ytd_brand_cost = sum(r[3] for r in YTD_2026)
ytd_nb_cost = sum(r[4] for r in YTD_2026)
ytd_cost = ytd_brand_cost + ytd_nb_cost

# 2025 weekly seasonality shape (52 weeks) — brand_share, nb_share in % of full year
Y25_SHAPE = [
    (1, 1.8875, 1.4708), (2, 1.9819, 1.9316), (3, 1.8309, 2.0379), (4, 2.1895, 1.9493),
    (5, 2.1140, 2.3215), (6, 1.5289, 1.8607), (7, 1.6044, 1.7544), (8, 1.7176, 2.1442),
    (9, 1.8686, 2.3746), (10, 1.5666, 2.2151), (11, 1.4156, 2.1797), (12, 1.0570, 2.0911),
    (13, 1.4345, 1.9316), (14, 1.5666, 1.9316), (15, 1.3968, 1.4177), (16, 1.3401, 1.7898),
    (17, 1.7176, 1.7898), (18, 1.3401, 1.3645), (19, 1.6610, 1.5063), (20, 1.6799, 2.1265),
    (21, 1.7554, 1.9316), (22, 3.0578, 2.6227), (23, 1.8686, 1.9848), (24, 1.5100, 2.3215),
    (25, 2.3028, 2.3392), (26, 1.8875, 2.7113), (27, 1.3779, 2.6404), (28, 1.5289, 2.4101),
    (29, 2.9445, 2.6404), (30, 1.8498, 2.3392), (31, 1.1891, 2.3569), (32, 1.0948, 1.9670),
    (33, 1.0948, 1.7544), (34, 1.3401, 1.9493), (35, 1.3590, 1.9670), (36, 1.3213, 1.2582),
    (37, 1.5855, 1.2405), (38, 1.1891, 1.1873), (39, 1.4156, 1.1164), (40, 1.7554, 1.1519),
    (41, 2.7180, 2.0025), (42, 2.4160, 1.9493), (43, 2.7369, 2.1088), (44, 2.6236, 2.1265),
    (45, 2.6236, 2.1265), (46, 3.4919, 2.2506), (47, 3.0200, 2.0379), (48, 2.9068, 2.2151),
    (49, 1.9630, 1.4531), (50, 2.8124, 1.2228), (51, 3.5674, 1.1873), (52, 2.7935, 1.2405),
]
FORECAST_WEEKS = [w for w in Y25_SHAPE if w[0] >= 17]
Y25_BRAND_SHARE_REM = sum(w[1] for w in FORECAST_WEEKS) / 100.0
Y25_NB_SHARE_REM = sum(w[2] for w in FORECAST_WEEKS) / 100.0

def nb_cpa_at(weekly_spend):
    return max(0.02 * weekly_spend**0.937, 1.0) if weekly_spend > 0 else 100

def brand_cpa_scale(full_year_brand):
    if full_year_brand <= 11012: return 20.0
    return 20.0 + (full_year_brand - 11012) / 4000 * 2.0

def project_year(brand_full, spend_target=None, ieccp_target=None):
    def run(spend):
        brand_rem = max(0, brand_full - ytd_brand)
        b_wts = {w: s / (Y25_BRAND_SHARE_REM * 100) for w, s, _ in FORECAST_WEEKS}
        n_wts = {w: s / (Y25_NB_SHARE_REM * 100) for w, s, _ in FORECAST_WEEKS}
        bcpa = brand_cpa_scale(brand_full)
        total_brand_cost = brand_full * bcpa
        nb_full_cost = spend - total_brand_cost
        nb_rem_cost = nb_full_cost - ytd_nb_cost
        if nb_rem_cost < 0: return None
        wk_rows = []
        for wk, bs, ns in FORECAST_WEEKS:
            bw = brand_rem * b_wts[wk]
            bc = bw * bcpa
            nc = nb_rem_cost * n_wts[wk]
            ncpa = nb_cpa_at(nc)
            nw = nc / ncpa if ncpa > 0 else 0
            wk_rows.append(dict(wk=wk, brand_regs=bw, brand_cost=bc, nb_cost=nc, nb_cpa=ncpa, nb_regs=nw))
        fy_b = ytd_brand + sum(r['brand_regs'] for r in wk_rows)
        fy_n = ytd_nb + sum(r['nb_regs'] for r in wk_rows)
        fy_bc = ytd_brand_cost + sum(r['brand_cost'] for r in wk_rows)
        fy_nc = ytd_nb_cost + sum(r['nb_cost'] for r in wk_rows)
        fy_cost = fy_bc + fy_nc
        fy_regs = fy_b + fy_n
        denom = fy_b * BRAND_CCP + fy_n * NB_CCP
        ieccp = fy_cost / denom * 100
        return dict(spend=spend, fy_brand=fy_b, fy_nb=fy_n, fy_regs=fy_regs,
                    fy_brand_cost=fy_bc, fy_nb_cost=fy_nc, fy_cost=fy_cost,
                    cpa=fy_cost/fy_regs, ieccp=ieccp, weekly=wk_rows, bcpa=bcpa)
    if spend_target:
        return run(spend_target)
    if ieccp_target:
        lo, hi = ytd_cost + 50_000, 3_000_000
        best = None
        for _ in range(80):
            mid = (lo + hi) / 2
            r = run(mid)
            if r is None:
                lo = mid + 1000; continue
            if abs(r['ieccp'] - ieccp_target) < 0.05:
                return r
            if r['ieccp'] < ieccp_target: lo = mid
            else: hi = mid
            best = r
        return best

scenarios = {'CONSERVATIVE': 11012, 'MODERATE': 12664, 'AGGRESSIVE': 14316}

print("="*100)
print("MX 2026 PRECISE WEEK-BY-WEEK — YTD W2-W16 actuals locked + W17-W52 projected")
print("="*100)
print(f"YTD: Brand {ytd_brand:,}, NB {ytd_nb:,}, Total {ytd_brand+ytd_nb:,} regs, Cost ${ytd_cost:,.0f}")
print(f"YTD ie%CCP: {ytd_cost/(ytd_brand*BRAND_CCP + ytd_nb*NB_CCP)*100:.1f}%")
print(f"NB CPA curve: $0.02 × weekly_spend^0.937   |   Brand CPA: $20 base + scale adjust")
print()
print(f"Remaining (W17-W52): 36 weeks, covers {Y25_BRAND_SHARE_REM*100:.1f}% of Brand, {Y25_NB_SHARE_REM*100:.1f}% of NB per 2025 shape")
print()

for title, kwargs in [("SCENARIO 1: SPEND = $1.3M", {"spend_target": 1_300_000}),
                     ("SCENARIO 2: TARGET 100% ie%CCP", {"ieccp_target": 100}),
                     ("SCENARIO 3: TARGET 75% ie%CCP", {"ieccp_target": 75})]:
    print("-"*100)
    print(title)
    print("-"*100)
    for label, brand in scenarios.items():
        r = project_year(brand, **kwargs)
        if r:
            nb_rem_spend = r['fy_nb_cost'] - ytd_nb_cost
            avg_wk_nb = nb_rem_spend / 36
            avg_ncpa = nb_cpa_at(avg_wk_nb)
            print(f"  {label:12}  Brand {r['fy_brand']:>7,.0f} @ ${r['bcpa']:.2f}   "
                  f"NB {r['fy_nb']:>6,.0f} (avg ${avg_ncpa:.0f} CPA @ ${avg_wk_nb:,.0f}/wk)   "
                  f"Total {r['fy_regs']:>7,.0f}   ${r['fy_cost']:>9,.0f}   "
                  f"CPA ${r['cpa']:.2f}   ie%CCP {r['ieccp']:.1f}%")
    print()

# Weekly detail for MODERATE @ 1.3M
print("="*100)
print("WEEKLY DETAIL — MODERATE (Brand 12,664) @ $1.3M total")
print("="*100)
r = project_year(12664, spend_target=1_300_000)
print(f"{'Wk':<4} {'Brand':>7} {'BrandCost':>10} {'NBCost':>9} {'NBCPA':>7} {'NBRegs':>8} {'Total':>7}")
# W17-W19 (near-term), W30-W34 (summer), W46-W52 (holiday peak)
sample_wks = [17, 18, 19, 20, 25, 30, 34, 36, 41, 46, 50, 52]
for row in r['weekly']:
    if row['wk'] in sample_wks:
        tot = row['brand_regs'] + row['nb_regs']
        print(f"W{row['wk']:<3}  {row['brand_regs']:>6.0f}  ${row['brand_cost']:>8,.0f}  ${row['nb_cost']:>7,.0f}  ${row['nb_cpa']:>5.0f}  {row['nb_regs']:>8.0f}  {tot:>7.0f}")
print()
print(f"Summary MODERATE @ $1.3M:")
print(f"  Full year: {r['fy_regs']:,.0f} regs / ${r['fy_cost']:,.0f} / CPA ${r['cpa']:.2f} / ie%CCP {r['ieccp']:.1f}%")
