import duckdb, math
from datetime import datetime, timedelta

md_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJpY2hzY290dHdpbGxAZ21haWwuY29tIiwibWRSZWdpb24iOiJhd3MtdXMtZWFzdC0xIiwic2Vzc2lvbiI6InJpY2hzY290dHdpbGwuZ21haWwuY29tIiwicGF0IjoiVDNIYzFVQWYzT3o1bjVkLS03ckdHNlBjMlpUdVNNbFItT3RXMS1qNzVPUSIsInVzZXJJZCI6ImU2MDhlNDZiLTE4YzctNGE5Ny04M2I2LWE0N2ZhOThmNjBhYyIsImlzcyI6Im1kX3BhdCIsInJlYWRPbmx5IjpmYWxzZSwidG9rZW5UeXBlIjoicmVhZF93cml0ZSIsImlhdCI6MTc3NTQ0MzY0N30.tS0Cab3FQ8_CDZ1PqOo9z09KYHEUFHwuLVXRQrxcHig'
con = duckdb.connect(f'md:ps_analytics?motherduck_token={md_token}')

ALL_MARKETS = ['US','CA','UK','DE','FR','IT','ES','JP','AU','MX']
CURRENT_WEEK = 14

STRATEGY = {
    'AU': {'type': 'efficiency'}, 'MX': {'type': 'ieccp_bound', 'ieccp_target': 1.0, 'ieccp_range': (0.90, 1.10)},
    'JP': {'type': 'brand_dominant'},
}
for m in ['US','CA','UK','DE','FR','IT','ES']:
    STRATEGY[m] = {'type': 'balanced', 'ieccp_range': (0.50, 0.65)}

def ols_trend(values):
    n = len(values)
    if n < 3: return 0.0, sum(values)/max(n,1)
    mean_y = sum(values) / n
    mean_x = (n - 1) / 2.0
    ss_xy = sum((i - mean_x) * (v - mean_y) for i, v in enumerate(values))
    ss_xx = sum((i - mean_x) ** 2 for i in range(n))
    return (ss_xy / ss_xx if ss_xx > 0 else 0.0), mean_y

def volatility(values):
    if len(values) < 2: return 0.0
    mean = sum(values) / len(values)
    return (sum((v - mean) ** 2 for v in values) / (len(values) - 1)) ** 0.5

def week_to_month(wk):
    jan5 = datetime(2026, 1, 5)
    thu = jan5 + timedelta(weeks=wk - 1, days=3)
    return thu.month

month_ends = {1:'2026-01-31',2:'2026-02-28',3:'2026-03-31',4:'2026-04-30',5:'2026-05-31',6:'2026-06-30',
              7:'2026-07-31',8:'2026-08-31',9:'2026-09-30',10:'2026-10-31',11:'2026-11-30',12:'2026-12-31'}
month_labels = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
q_ends = {1:'2026-03-31',2:'2026-06-30',3:'2026-09-30',4:'2026-12-31'}

INS = """INSERT INTO ps.cumulative_projections 
    (projection_id, market, channel, metric_name, revision_date, horizon, 
     target_end_date, target_label, projected_cumulative, ci_low, ci_high, revision_number, reason)
    VALUES (?, ?, 'ps', ?, '2026-04-08', ?, ?, ?, ?, ?, ?, 1, ?)"""

print("Projecting W15-W52 for all markets...")

all_weekly = {}
for market in ALL_MARKETS:
    rows = con.execute(f"""
        SELECT period_key, registrations, brand_registrations, nb_registrations,
               cost, brand_cost, nb_cost, ieccp
        FROM ps.performance WHERE market = '{market}' AND period_type = 'weekly' ORDER BY period_start
    """).fetchall()
    if not rows: continue
    
    history = []
    for pk, regs, bregs, nbregs, cost, bcost, nbcost, ieccp in rows:
        try: wn = int(pk.split('W')[-1])
        except: continue
        history.append({'wk':wn, 'brand_regs':bregs or 0, 'nb_regs':nbregs or 0,
                       'brand_cost':bcost or 0, 'nb_cost':nbcost or 0, 'regs':regs or 0, 'cost':cost or 0, 'ieccp':ieccp})
    
    recent = history[-8:]
    has_season = len(history) >= 52
    strat = STRATEGY.get(market, {})
    stype = strat.get('type', 'balanced')
    
    # Seasonal indices by week-of-year
    woy_data = {}
    for h in history:
        woy = h['wk'] % 52 or 52
        if woy not in woy_data: woy_data[woy] = {'br':[], 'nr':[], 'bc':[], 'nc':[]}
        if h['brand_regs'] > 0: woy_data[woy]['br'].append(h['brand_regs'])
        if h['nb_regs'] > 0: woy_data[woy]['nr'].append(h['nb_regs'])
        if h['brand_cost'] > 0: woy_data[woy]['bc'].append(h['brand_cost'])
        if h['nb_cost'] > 0: woy_data[woy]['nc'].append(h['nb_cost'])
    
    all_br = [h['brand_regs'] for h in history if h['brand_regs'] > 0]
    all_nr = [h['nb_regs'] for h in history if h['nb_regs'] > 0]
    avg_br = sum(all_br)/len(all_br) if all_br else 1
    avg_nr = sum(all_nr)/len(all_nr) if all_nr else 1
    avg_bc = sum(h['brand_cost'] for h in history if h['brand_cost']>0) / max(len([h for h in history if h['brand_cost']>0]),1)
    avg_nc = sum(h['nb_cost'] for h in history if h['nb_cost']>0) / max(len([h for h in history if h['nb_cost']>0]),1)
    
    br_slope, br_mean = ols_trend([h['brand_regs'] for h in recent])
    nr_slope, nr_mean = ols_trend([h['nb_regs'] for h in recent])
    bc_slope, bc_mean = ols_trend([h['brand_cost'] for h in recent])
    nc_slope, nc_mean = ols_trend([h['nb_cost'] for h in recent])
    br_vol = volatility([h['brand_regs'] for h in recent])
    nr_vol = volatility([h['nb_regs'] for h in recent])
    bc_vol = volatility([h['brand_cost'] for h in recent])
    nc_vol = volatility([h['nb_cost'] for h in recent])
    
    # ie%CCP NB adjustment
    ieccp_current = history[-1].get('ieccp')
    nb_adj = 1.0
    if ieccp_current and stype == 'ieccp_bound':
        dev = ieccp_current - strat.get('ieccp_target', 1.0)
        if abs(dev) > 0.05: nb_adj = max(0.6, min(1.4, 1.0 - dev * 0.8))
    elif ieccp_current and stype == 'balanced':
        rng = strat.get('ieccp_range', (0.5, 0.65))
        if ieccp_current > rng[1]: nb_adj = max(0.8, 1.0 - (ieccp_current - rng[1]) * 0.3)
    
    weekly_regs = {}
    weekly_cost = {}
    for wk in range(CURRENT_WEEK + 1, 53):
        wa = wk - CURRENT_WEEK
        woy = wk % 52 or 52
        
        t_br = max(0, br_mean + br_slope * (len(recent)-1+wa))
        t_bc = max(0, bc_mean + bc_slope * (len(recent)-1+wa))
        if has_season and woy in woy_data and woy_data[woy]['br']:
            si_br = (sum(woy_data[woy]['br'])/len(woy_data[woy]['br'])) / avg_br if avg_br > 0 else 1
            si_bc = (sum(woy_data[woy]['bc'])/len(woy_data[woy]['bc'])) / avg_bc if avg_bc > 0 else 1
            si_br = max(0.5, min(2.0, si_br))
            si_bc = max(0.5, min(2.0, si_bc))
            p_br = 0.6*t_br + 0.4*(br_mean*si_br)
            p_bc = 0.6*t_bc + 0.4*(bc_mean*si_bc)
        else:
            p_br = t_br; p_bc = t_bc
        
        if stype == 'brand_dominant':
            p_nr = max(0, nr_mean); p_nc = max(0, nc_mean)
        else:
            t_nr = max(0, nr_mean + nr_slope * (len(recent)-1+wa))
            t_nc = max(0, nc_mean + nc_slope * (len(recent)-1+wa))
            if has_season and woy in woy_data and woy_data[woy]['nr']:
                si_nr = (sum(woy_data[woy]['nr'])/len(woy_data[woy]['nr'])) / avg_nr if avg_nr > 0 else 1
                si_nc = (sum(woy_data[woy]['nc'])/len(woy_data[woy]['nc'])) / avg_nc if avg_nc > 0 else 1
                si_nr = max(0.5, min(2.0, si_nr)); si_nc = max(0.5, min(2.0, si_nc))
                p_nr = 0.6*t_nr + 0.4*(nr_mean*si_nr)
                p_nc = 0.6*t_nc + 0.4*(nc_mean*si_nc)
            else:
                p_nr = t_nr; p_nc = t_nc
            p_nr = max(0, p_nr * nb_adj); p_nc = max(0, p_nc * nb_adj)
        
        tr = max(1, round(p_br + p_nr))
        tc = round(p_bc + p_nc, 2)
        hf = math.sqrt(wa)
        rci = 1.04 * (br_vol + nr_vol) * hf
        cci = 1.04 * (bc_vol + nc_vol) * hf
        weekly_regs[wk] = (tr, max(0, round(tr - rci)), round(tr + rci))
        weekly_cost[wk] = (round(tc,2), max(0, round(tc-cci,2)), round(tc+cci,2))
    
    all_weekly[market] = {'registrations': weekly_regs, 'cost': weekly_cost}
    yr = sum(h['regs'] for h in history) + sum(v[0] for v in weekly_regs.values())
    print(f"  {market}: YE regs={yr:,}, nb_adj={nb_adj:.2f}")

# Now load into cumulative_projections
print("\nLoading cumulative_projections...")

for market in ALL_MARKETS:
    mw = all_weekly.get(market, {})
    if not mw: continue
    
    act_rows = con.execute(f"""
        SELECT period_key, registrations, cost FROM ps.performance
        WHERE market = '{market}' AND period_type = 'weekly' AND period_key LIKE '2026%'
        ORDER BY period_start
    """).fetchall()
    act_by_wk = {}
    for pk, regs, cost in act_rows:
        try:
            wn = int(pk.split('W')[-1])
            act_by_wk[wn] = {'regs': regs or 0, 'cost': cost or 0}
        except: pass
    
    for metric in ['registrations', 'cost']:
        wk_data = mw.get(metric, {})
        full_year = {}
        for wk in range(1, 53):
            if wk in act_by_wk:
                v = act_by_wk[wk]['regs'] if metric == 'registrations' else act_by_wk[wk]['cost']
                full_year[wk] = (v, v, v)
            elif wk in wk_data:
                full_year[wk] = wk_data[wk]
        
        # Weekly (future only)
        for wk in range(CURRENT_WEEK+1, 53):
            if wk not in wk_data: continue
            v, cl, ch = wk_data[wk]
            con.execute(INS, [f"{market}-{metric}-W{wk}-r1", market, metric, 'weekly',
                             f"2026-W{wk}", f"W{wk}", v, cl, ch, 'bayesian_brand_nb_split'])
        
        # Monthly cumulative
        run = 0; run_l = 0; run_h = 0
        for mn in range(1, 13):
            mt = 0; ml = 0; mh = 0; has = False
            for wk in range(1, 53):
                if week_to_month(wk) == mn and wk in full_year:
                    v, cl, ch = full_year[wk]
                    mt += v; ml += cl; mh += ch; has = True
            if not has: continue
            run += mt; run_l += ml; run_h += mh
            con.execute(INS, [f"{market}-{metric}-m{mn:02d}-r1", market, metric, 'monthly',
                             month_ends[mn], month_labels[mn], round(run), round(run_l), round(run_h), 'bayesian_brand_nb_split'])
        
        # Quarterly
        for qi in range(1, 5):
            qt = 0; ql = 0; qh = 0; has = False
            for wk in range(1, 53):
                m = week_to_month(wk)
                qn = (m-1)//3 + 1
                if qn == qi and wk in full_year:
                    v, cl, ch = full_year[wk]
                    qt += v; ql += cl; qh += ch; has = True
            if not has: continue
            con.execute(INS, [f"{market}-{metric}-Q{qi}-r1", market, metric, 'quarterly',
                             q_ends[qi], f"Q{qi}", round(qt), round(ql), round(qh), 'bayesian_brand_nb_split'])
        
        # Year-end
        ye = sum(v[0] for v in full_year.values())
        ye_l = sum(v[1] for v in full_year.values())
        ye_h = sum(v[2] for v in full_year.values())
        con.execute(INS, [f"{market}-{metric}-YE-r1", market, metric, 'year_end',
                         '2026-12-31', '2026 YE', round(ye), round(ye_l), round(ye_h), 'bayesian_brand_nb_split'])
    
    # CPA (derived)
    for hz in ['monthly', 'quarterly', 'year_end']:
        cr = con.execute(f"SELECT target_label, target_end_date, projected_cumulative, ci_low, ci_high FROM ps.cumulative_projections WHERE market='{market}' AND metric_name='cost' AND horizon='{hz}'").fetchall()
        rr = con.execute(f"SELECT target_label, projected_cumulative, ci_low, ci_high FROM ps.cumulative_projections WHERE market='{market}' AND metric_name='registrations' AND horizon='{hz}'").fetchall()
        rm = {r[0]: (r[1], r[2], r[3]) for r in rr}
        for label, ed, cv, ccl, cch in cr:
            rd = rm.get(label)
            if rd and rd[0] > 0:
                cpa = round(cv/rd[0], 2)
                cpa_l = round(ccl/rd[2], 2) if rd[2] > 0 else round(cpa*0.9, 2)
                cpa_h = round(cch/rd[1], 2) if rd[1] > 0 else round(cpa*1.1, 2)
                con.execute(INS, [f"{market}-cpa-{label}-r1", market, 'cpa', hz, ed, label, cpa, cpa_l, cpa_h, 'derived'])

# WW + EU5 aggregates
print("Building WW and EU5...")
for agg, srcs in [('WW', ALL_MARKETS), ('EU5', ['UK','DE','FR','IT','ES'])]:
    for metric in ['registrations', 'cost']:
        for hz in ['monthly', 'quarterly', 'year_end', 'weekly']:
            rows = con.execute(f"""SELECT target_label, target_end_date, SUM(projected_cumulative), SUM(ci_low), SUM(ci_high)
                FROM ps.cumulative_projections WHERE market IN ({','.join(f"'{m}'" for m in srcs)})
                AND metric_name='{metric}' AND horizon='{hz}' GROUP BY target_label, target_end_date ORDER BY target_end_date""").fetchall()
            for label, ed, p, cl, ch in rows:
                con.execute(INS, [f"{agg}-{metric}-{label}-r1", agg, metric, hz, ed, label, round(p), round(cl), round(ch), 'aggregate'])
    for hz in ['monthly', 'quarterly', 'year_end']:
        cr = con.execute(f"SELECT target_label, target_end_date, projected_cumulative FROM ps.cumulative_projections WHERE market='{agg}' AND metric_name='cost' AND horizon='{hz}'").fetchall()
        rr = con.execute(f"SELECT target_label, projected_cumulative FROM ps.cumulative_projections WHERE market='{agg}' AND metric_name='registrations' AND horizon='{hz}'").fetchall()
        rm = {r[0]: r[1] for r in rr}
        for label, ed, cv in cr:
            rv = rm.get(label)
            if rv and rv > 0:
                cpa = round(cv/rv, 2)
                con.execute(INS, [f"{agg}-cpa-{label}-r1", agg, 'cpa', hz, ed, label, cpa, round(cpa*0.9,2), round(cpa*1.1,2), 'aggregate'])

# Consistency check
print("\nConsistency (regs: Dec cum = YE = sum Q1-Q4):")
for market in ALL_MARKETS + ['WW', 'EU5']:
    ye = con.execute(f"SELECT projected_cumulative FROM ps.cumulative_projections WHERE market='{market}' AND metric_name='registrations' AND horizon='year_end'").fetchone()
    dec = con.execute(f"SELECT projected_cumulative FROM ps.cumulative_projections WHERE market='{market}' AND metric_name='registrations' AND horizon='monthly' AND target_label='Dec'").fetchone()
    qs = con.execute(f"SELECT SUM(projected_cumulative) FROM ps.cumulative_projections WHERE market='{market}' AND metric_name='registrations' AND horizon='quarterly'").fetchone()
    ye_v = ye[0] if ye else 0; dec_v = dec[0] if dec else 0; q_v = qs[0] if qs else 0
    ok = "✅" if abs(ye_v - dec_v) < 2 and abs(ye_v - q_v) < 2 else "❌"
    print(f"  {market}: YE={ye_v:,.0f} Dec={dec_v:,.0f} Qsum={q_v:,.0f} {ok}")

total = con.execute("SELECT COUNT(*) FROM ps.cumulative_projections").fetchone()
print(f"\nTotal: {total[0]} rows")
con.close()
print("Done.")
