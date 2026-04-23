#!/usr/bin/env python3
"""MX-only projection using the same Bayesian logic as full_year_project.py.
Read-only: prints month-by-month, quarterly, and year-end forecast for MX.
Does NOT write to any table."""

import duckdb, math, os, sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.expanduser('~/shared/tools'))
from prediction.config import MOTHERDUCK_TOKEN as TOKEN

MARKET = 'MX'
STRATEGY = {'type': 'ieccp_bound', 'target': 1.0, 'range': (0.9, 1.1)}
MONTH_LBL = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
Q_MAP = {m: f'Q{(m-1)//3+1}' for m in range(1, 13)}

def ols_trend(vals):
    n = len(vals)
    if n < 3: return 0.0
    my = sum(vals)/n; mx2 = (n-1)/2.0
    ssxy = sum((i-mx2)*(v-my) for i,v in enumerate(vals))
    ssxx = sum((i-mx2)**2 for i in range(n))
    return ssxy/ssxx if ssxx > 0 else 0.0

def vol(vals):
    if len(vals) < 2: return 0.0
    m = sum(vals)/len(vals)
    return (sum((v-m)**2 for v in vals)/(len(vals)-1))**0.5

def seasonal_idx(all_data, twk, key):
    if len(all_data) < 52: return 1.0
    by_w = {}; av = []
    for w in all_data:
        v = w.get(key)
        if not v or v <= 0: continue
        try: wn = int(w['period_key'].split('W')[-1])
        except: continue
        by_w.setdefault(wn, []).append(v); av.append(v)
    if not av or twk not in by_w: return 1.0
    oa = sum(av)/len(av)
    if oa <= 0: return 1.0
    return max(0.5, min(2.0, (sum(by_w[twk])/len(by_w[twk]))/oa))

def project_seg(hist, seg, twk, wa):
    pfx = f'{seg}_'
    r8 = list(reversed(hist[:8])); ad = list(reversed(hist))
    rv = [w.get(f'{pfx}regs',0) or 0 for w in r8]
    cv = [w.get(f'{pfx}cost',0) or 0 for w in r8]
    if not rv or sum(rv)==0: return 0,0,0,0
    rs = ols_trend(rv); cs = ols_trend(cv)
    rm = sum(rv)/len(rv); cm = sum(cv)/len(cv)
    tr = rm + rs*(len(rv)-1+wa); tc = cm + cs*(len(cv)-1+wa)
    sr = seasonal_idx(ad,twk,f'{pfx}regs'); sc = seasonal_idx(ad,twk,f'{pfx}cost')
    sw = 0.4 if len(ad) >= 52 else 0.0; tw2 = 1.0 - sw
    pr = max(0, tw2*tr + sw*rm*sr); pc = max(0, tw2*tc + sw*cm*sc)
    return round(pr), round(pc,2), 1.04*vol(rv)*math.sqrt(wa), 1.04*vol(cv)*math.sqrt(wa)

def apply_ie(nr, nc, ic, isl):
    if ic is None: return nr, nc
    d = ic - STRATEGY['target']
    if abs(d) < 0.05: return nr, nc
    a = max(0.6, min(1.4, 1.0 - d*0.8))
    if isl and isl > 0.02 and a < 1.0: a *= 0.95
    return round(nr*a), round(nc*a, 2)

def wk_to_month(wk):
    mon = datetime(2026,1,5) + timedelta(weeks=wk-1)
    thu = mon + timedelta(days=3)
    return thu.month

def run():
    con = duckdb.connect(f'md:ps_analytics?motherduck_token={TOKEN}')
    rows = con.execute(f"""SELECT period_key, period_start,
        registrations AS regs, cost, cpa,
        brand_registrations AS brand_regs, brand_cost, brand_cpa,
        nb_registrations AS nb_regs, nb_cost, nb_cpa, ieccp
        FROM ps.performance WHERE market='{MARKET}' AND period_type='weekly'
        ORDER BY period_start DESC""").fetchall()
    cols = ['period_key','period_start','regs','cost','cpa','brand_regs','brand_cost','brand_cpa','nb_regs','nb_cost','nb_cpa','ieccp']
    hist = [dict(zip(cols, r)) for r in rows]

    print(f"=== MX Full-Year 2026 Projection — Bayesian Brand/NB Split ===")
    print(f"History weeks:      {len(hist)}")
    print(f"Latest actual week: {hist[0]['period_key']} ({hist[0]['period_start']})")
    print(f"Latest ie%CCP:      {hist[0].get('ieccp')}")
    print()

    ic = hist[0].get('ieccp')
    iv = [w.get('ieccp') for w in hist[:6] if w.get('ieccp') is not None]
    isl = ols_trend(list(reversed(iv))) if len(iv) >= 3 else None

    # Only use 2026 weeks as actuals; older weeks are history for the trend model
    abw = {}
    for w in hist:
        pk = w['period_key']
        if not pk.startswith('2026'): continue
        try: wn = int(pk.split('W')[-1]); abw[wn] = w
        except: pass

    wk_data = {}
    for wk in range(1, 53):
        if wk in abw:
            aw = abw[wk]
            wk_data[wk] = (aw.get('regs') or 0, aw.get('cost') or 0, 0, 0, True)
        else:
            wa = max(1, wk - max(abw.keys()) if abw else wk)
            br, bc, brc, bcc = project_seg(hist, 'brand', wk, wa)
            nr, nc, nrc, ncc = project_seg(hist, 'nb', wk, wa)
            nr, nc = apply_ie(nr, nc, ic, isl)
            wk_data[wk] = (br + nr, bc + nc, brc + nrc, bcc + ncc, False)

    mo_r = {m:0 for m in range(1,13)}; mo_c = {m:0 for m in range(1,13)}
    mo_cir = {m:0 for m in range(1,13)}; mo_cic = {m:0 for m in range(1,13)}
    mo_ar = {m:0 for m in range(1,13)}; mo_ac = {m:0 for m in range(1,13)}
    for wk in range(1,53):
        r, c, cr, cc, ia = wk_data[wk]
        mo = wk_to_month(wk)
        mo_r[mo] += r; mo_c[mo] += c
        if not ia: mo_cir[mo] += cr; mo_cic[mo] += cc
        else: mo_ar[mo] += r; mo_ac[mo] += c

    print(f"{'Mo':<4} {'Regs':>7} {'Cost':>11} {'CostLow':>11} {'CostHi':>11} {'RegsLow':>8} {'RegsHi':>8} {'CPA':>7}  {'Src':<8}")
    for mo in range(1, 13):
        v = mo_r[mo]; c = mo_c[mo]
        cl = max(0, v - mo_cir[mo]); ch = v + mo_cir[mo]
        costlow = max(0, c - mo_cic[mo]); costhi = c + mo_cic[mo]
        cpa = c/v if v > 0 else 0
        src = 'actual' if mo_cir[mo] == 0 and mo_r[mo] > 0 else 'fcast'
        print(f"{MONTH_LBL[mo]:<4} {v:>7.0f} ${c:>10,.0f} ${costlow:>10,.0f} ${costhi:>10,.0f} {cl:>8.0f} {ch:>8.0f} ${cpa:>6.2f}  {src}")

    print()
    for ql in ['Q1','Q2','Q3','Q4']:
        qms = [m for m in range(1,13) if Q_MAP[m]==ql]
        qr = sum(mo_r[m] for m in qms); qc = sum(mo_c[m] for m in qms)
        qcir = sum(mo_cir[m] for m in qms); qcic = sum(mo_cic[m] for m in qms)
        qcpa = qc/qr if qr > 0 else 0
        print(f"{ql:<4} {qr:>7.0f} ${qc:>10,.0f} ${max(0,qc-qcic):>10,.0f} ${qc+qcic:>10,.0f} {max(0,qr-qcir):>8.0f} {qr+qcir:>8.0f} ${qcpa:>6.2f}")

    ye_r = sum(mo_r.values()); ye_c = sum(mo_c.values())
    ye_cir = sum(mo_cir.values()); ye_cic = sum(mo_cic.values())
    ye_cpa = ye_c/ye_r if ye_r > 0 else 0
    print()
    print(f"{'YE':<4} {ye_r:>7,.0f} ${ye_c:>10,.0f} ${max(0,ye_c-ye_cic):>10,.0f} ${ye_c+ye_cic:>10,.0f} {max(0,ye_r-ye_cir):>8.0f} {ye_r+ye_cir:>8.0f} ${ye_cpa:>6.2f}")

    ytd_r = sum(mo_ar.values()); ytd_c = sum(mo_ac.values())
    ytd_cpa = ytd_c/ytd_r if ytd_r > 0 else 0
    roy_r = ye_r - ytd_r; roy_c = ye_c - ytd_c
    print()
    print(f"YTD actuals:   {ytd_r:,.0f} regs, ${ytd_c:,.0f}, CPA ${ytd_cpa:.2f}")
    print(f"RoY projected: {roy_r:,.0f} regs, ${roy_c:,.0f}")
    print()
    OP2 = 1735313
    print(f"OP2 (Yun April R&O):         ${OP2:,} USD gross")
    print(f"Dashboard year-end forecast: ${ye_c:,.0f} (CI ${max(0,ye_c-ye_cic):,.0f} to ${ye_c+ye_cic:,.0f})")
    print(f"OP2 minus forecast midpoint: ${OP2-ye_c:,.0f}")
    print(f"OP2 minus forecast high:     ${OP2-(ye_c+ye_cic):,.0f}  <- conservative transfer")
    print(f"OP2 minus forecast low:      ${OP2-max(0,ye_c-ye_cic):,.0f}  <- aggressive transfer")

if __name__ == '__main__':
    run()
