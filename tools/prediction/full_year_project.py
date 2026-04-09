#!/usr/bin/env python3
"""Full-year projection: 52 weeks × 10 markets + WW + EU5.
Writes to ps.cumulative_projections in MotherDuck.
Weeks sum to months, months sum to quarters, quarters sum to year-end."""

import duckdb, math, os
from datetime import datetime, timedelta

TOKEN = os.environ.get('MOTHERDUCK_TOKEN',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJpY2hzY290dHdpbGxAZ21haWwuY29tIiwibWRSZWdpb24iOiJhd3MtdXMtZWFzdC0xIiwic2Vzc2lvbiI6InJpY2hzY290dHdpbGwuZ21haWwuY29tIiwicGF0IjoiVDNIYzFVQWYzT3o1bjVkLS03ckdHNlBjMlpUdVNNbFItT3RXMS1qNzVPUSIsInVzZXJJZCI6ImU2MDhlNDZiLTE4YzctNGE5Ny04M2I2LWE0N2ZhOThmNjBhYyIsImlzcyI6Im1kX3BhdCIsInJlYWRPbmx5IjpmYWxzZSwidG9rZW5UeXBlIjoicmVhZF93cml0ZSIsImlhdCI6MTc3NTQ0MzY0N30.tS0Cab3FQ8_CDZ1PqOo9z09KYHEUFHwuLVXRQrxcHig')

ALL_MARKETS = ['US','CA','UK','DE','FR','IT','ES','JP','AU','MX']
STRATEGY = {
    'AU': {'type':'efficiency'}, 'MX': {'type':'ieccp_bound','target':1.0,'range':(0.9,1.1)},
    'JP': {'type':'brand_dominant'},
}
for m in ['US','CA','UK','DE','FR','IT','ES']:
    STRATEGY[m] = {'type':'balanced','range':(0.5,0.65)}

MONTH_END = {i: f'2026-{i:02d}-{[31,28,31,30,31,30,31,31,30,31,30,31][i-1]}' for i in range(1,13)}
MONTH_LBL = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
Q_MAP = {m: f'Q{(m-1)//3+1}' for m in range(1,13)}
Q_END = {'Q1':'2026-03-31','Q2':'2026-06-30','Q3':'2026-09-30','Q4':'2026-12-31'}

def ols_trend(vals):
    n=len(vals)
    if n<3: return 0.0
    my=sum(vals)/n; mx2=(n-1)/2.0
    ssxy=sum((i-mx2)*(v-my) for i,v in enumerate(vals))
    ssxx=sum((i-mx2)**2 for i in range(n))
    return ssxy/ssxx if ssxx>0 else 0.0

def vol(vals):
    if len(vals)<2: return 0.0
    m=sum(vals)/len(vals)
    return (sum((v-m)**2 for v in vals)/(len(vals)-1))**0.5

def seasonal_idx(all_data, twk, key):
    if len(all_data)<52: return 1.0
    by_w={}; av=[]
    for w in all_data:
        v=w.get(key); 
        if not v or v<=0: continue
        try: wn=int(w['period_key'].split('W')[-1])
        except: continue
        by_w.setdefault(wn,[]).append(v); av.append(v)
    if not av or twk not in by_w: return 1.0
    oa=sum(av)/len(av)
    if oa<=0: return 1.0
    return max(0.5,min(2.0,(sum(by_w[twk])/len(by_w[twk]))/oa))


def project_seg(hist, seg, twk, wa):
    pfx=f'{seg}_'
    r8=list(reversed(hist[:8])); ad=list(reversed(hist))
    rv=[w.get(f'{pfx}regs',0) or 0 for w in r8]
    cv=[w.get(f'{pfx}cost',0) or 0 for w in r8]
    if not rv or sum(rv)==0: return 0,0,0,0
    rs,_=ols_trend(rv),0; cs=ols_trend(cv)
    rm=sum(rv)/len(rv); cm=sum(cv)/len(cv)
    tr=rm+rs*(len(rv)-1+wa); tc=cm+cs*(len(cv)-1+wa)
    sr=seasonal_idx(ad,twk,f'{pfx}regs'); sc=seasonal_idx(ad,twk,f'{pfx}cost')
    sw=0.4 if len(ad)>=52 else 0.0; tw2=1.0-sw
    pr=max(0,tw2*tr+sw*rm*sr); pc=max(0,tw2*tc+sw*cm*sc)
    return round(pr),round(pc,2),1.04*vol(rv)*math.sqrt(wa),1.04*vol(cv)*math.sqrt(wa)

def apply_ie(mkt,nr,nc,ic,isl):
    s=STRATEGY.get(mkt,{})
    if s.get('type') in ('efficiency','brand_dominant') or ic is None: return nr,nc
    if s['type']=='ieccp_bound':
        d=ic-s.get('target',1.0)
        if abs(d)<0.05: return nr,nc
        a=max(0.6,min(1.4,1.0-d*0.8))
    elif s['type']=='balanced':
        rng=s.get('range',(0.5,0.65))
        if rng[0]<=ic<=rng[1]: return nr,nc
        a=max(0.8,1.0-(ic-rng[1])*0.3) if ic>rng[1] else min(1.15,1.0+(rng[0]-ic)*0.2)
    else: return nr,nc
    if isl and isl>0.02 and a<1.0: a*=0.95
    return round(nr*a),round(nc*a,2)

def wk_to_month(wk):
    mon=datetime(2026,1,5)+timedelta(weeks=wk-1)
    thu=mon+timedelta(days=3)
    return thu.month

def wk_end(wk):
    mon=datetime(2026,1,5)+timedelta(weeks=wk-1)
    return (mon+timedelta(days=6)).strftime('%Y-%m-%d')

def run():
    con=duckdb.connect(f'md:ps_analytics?motherduck_token={TOKEN}')
    con.execute("DELETE FROM ps.cumulative_projections")
    print("Cleared cumulative_projections")

    for market in ALL_MARKETS:
        con2=duckdb.connect(f'md:ps_analytics?motherduck_token={TOKEN}')
        rows=con2.execute(f"""SELECT period_key,period_start,
            registrations as regs,cost,cpa,brand_registrations as brand_regs,brand_cost,brand_cpa,
            nb_registrations as nb_regs,nb_cost,nb_cpa,ieccp
            FROM ps.performance WHERE market='{market}' AND period_type='weekly' ORDER BY period_start DESC""").fetchall()
        cols=['period_key','period_start','regs','cost','cpa','brand_regs','brand_cost','brand_cpa','nb_regs','nb_cost','nb_cpa','ieccp']
        hist=[dict(zip(cols,r)) for r in rows]
        if len(hist)<4:
            print(f"  {market}: skip ({len(hist)} weeks)")
            con2.close(); continue

        stype=STRATEGY.get(market,{}).get('type','balanced')
        ic=hist[0].get('ieccp')
        iv=[w.get('ieccp') for w in hist[:6] if w.get('ieccp') is not None]
        isl=ols_trend(list(reversed(iv))) if len(iv)>=3 else None

        abw={}
        for w in hist:
            try: wn=int(w['period_key'].split('W')[-1]); abw[wn]=w
            except: pass

        # Project 52 weeks
        wk_data={}  # wk -> (regs, cost, ci_r, ci_c, is_actual)
        for wk in range(1,53):
            if wk in abw:
                aw=abw[wk]
                wk_data[wk]=(aw.get('regs') or 0, aw.get('cost') or 0, 0, 0, True)
            else:
                wa=max(1,wk-max(abw.keys()) if abw else wk)
                br,bc,brc,bcc=project_seg(hist,'brand',wk,wa)
                if stype=='brand_dominant':
                    rnb=[w.get('nb_regs',0) or 0 for w in hist[:4]]
                    nr=round(sum(rnb)/len(rnb)) if rnb else 0; nc=0; nrc=nr*0.5; ncc=0
                else:
                    nr,nc,nrc,ncc=project_seg(hist,'nb',wk,wa)
                    nr,nc=apply_ie(market,nr,nc,ic,isl)
                wk_data[wk]=(br+nr,bc+nc,brc+nrc,bcc+ncc,False)

        # Accumulate into months
        mo_r={m:0 for m in range(1,13)}; mo_c={m:0 for m in range(1,13)}
        mo_cir={m:0 for m in range(1,13)}; mo_cic={m:0 for m in range(1,13)}
        for wk in range(1,53):
            r,c,cr,cc,ia=wk_data[wk]
            mo=wk_to_month(wk)
            mo_r[mo]+=r; mo_c[mo]+=c
            mo_cir[mo]+=cr if not ia else 0
            mo_cic[mo]+=cc if not ia else 0

        # ── Insert weekly ──
        batch=[]
        for wk in range(1,53):
            r,c,cr,cc,ia=wk_data[wk]
            wl=f"W{wk}"; we=wk_end(wk)
            for mn,v,ci in [('registrations',r,cr),('cost',c,cc)]:
                batch.append((f"{market}-{mn}-{wl}-r1",market,'ps',mn,'2026-04-08','weekly',
                    we,wl,round(v),round(max(0,v-ci)),round(v+ci),1,
                    'actual' if ia else 'bayesian_brand_nb_split'))
        for i in range(0,len(batch),50):
            con2.executemany("""INSERT INTO ps.cumulative_projections 
                (projection_id,market,channel,metric_name,revision_date,horizon,
                 target_end_date,target_label,projected_cumulative,ci_low,ci_high,revision_number,reason)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",batch[i:i+50])

        # ── Insert monthly cumulative ──
        cum_r=0; cum_c=0; cum_cil_r=0; cum_cih_r=0
        for mo in range(1,13):
            cum_r+=mo_r[mo]; cum_c+=mo_c[mo]
            cum_cil_r+=max(0,mo_r[mo]-mo_cir[mo]); cum_cih_r+=mo_r[mo]+mo_cir[mo]
            for mn,v,cl,ch in [
                ('registrations',cum_r,cum_cil_r,cum_cih_r),
                ('cost',round(cum_c,2),round(max(0,cum_c-mo_cic[mo]),2),round(cum_c+mo_cic[mo],2))]:
                con2.execute("""INSERT INTO ps.cumulative_projections 
                    (projection_id,market,channel,metric_name,revision_date,horizon,
                     target_end_date,target_label,projected_cumulative,ci_low,ci_high,revision_number,reason)
                    VALUES(?,?,'ps',?,'2026-04-08','monthly',?,?,?,?,?,1,'bayesian_brand_nb_split')""",
                    [f"{market}-{mn}-m{mo:02d}-r1",market,mn,MONTH_END[mo],MONTH_LBL[mo],round(v),round(cl),round(ch)])
            if mo_r[mo]>0:
                mcpa=mo_c[mo]/mo_r[mo]
                con2.execute("""INSERT INTO ps.cumulative_projections 
                    (projection_id,market,channel,metric_name,revision_date,horizon,
                     target_end_date,target_label,projected_cumulative,ci_low,ci_high,revision_number,reason)
                    VALUES(?,?,'ps','cpa','2026-04-08','monthly',?,?,?,?,?,1,'bayesian_brand_nb_split')""",
                    [f"{market}-cpa-m{mo:02d}-r1",market,MONTH_END[mo],MONTH_LBL[mo],round(mcpa,2),round(mcpa*0.9,2),round(mcpa*1.1,2)])

        # ── Insert quarterly ──
        for ql,qe in Q_END.items():
            qms=[m for m in range(1,13) if Q_MAP[m]==ql]
            qr=sum(mo_r[m] for m in qms); qc=sum(mo_c[m] for m in qms)
            qcir=sum(mo_cir[m] for m in qms); qcic=sum(mo_cic[m] for m in qms)
            for mn,v,cl,ch in [
                ('registrations',qr,max(0,qr-qcir),qr+qcir),
                ('cost',round(qc,2),round(max(0,qc-qcic),2),round(qc+qcic,2))]:
                con2.execute("""INSERT INTO ps.cumulative_projections 
                    (projection_id,market,channel,metric_name,revision_date,horizon,
                     target_end_date,target_label,projected_cumulative,ci_low,ci_high,revision_number,reason)
                    VALUES(?,?,'ps',?,'2026-04-08','quarterly',?,?,?,?,?,1,'bayesian_brand_nb_split')""",
                    [f"{market}-{mn}-{ql}-r1",market,mn,qe,ql,round(v),round(cl),round(ch)])
            if qr>0:
                qcpa=qc/qr
                con2.execute("""INSERT INTO ps.cumulative_projections 
                    (projection_id,market,channel,metric_name,revision_date,horizon,
                     target_end_date,target_label,projected_cumulative,ci_low,ci_high,revision_number,reason)
                    VALUES(?,?,'ps','cpa','2026-04-08','quarterly',?,?,?,?,?,1,'bayesian_brand_nb_split')""",
                    [f"{market}-cpa-{ql}-r1",market,qe,ql,round(qcpa,2),round(qcpa*0.9,2),round(qcpa*1.1,2)])

        # ── Year-end ──
        yer=cum_r; yec=cum_c
        for mn,v,cl,ch in [
            ('registrations',yer,cum_cil_r,cum_cih_r),
            ('cost',round(yec,2),round(max(0,yec-sum(mo_cic[m] for m in range(1,13))),2),round(yec+sum(mo_cic[m] for m in range(1,13)),2))]:
            con2.execute("""INSERT INTO ps.cumulative_projections 
                (projection_id,market,channel,metric_name,revision_date,horizon,
                 target_end_date,target_label,projected_cumulative,ci_low,ci_high,revision_number,reason)
                VALUES(?,?,'ps',?,'2026-04-08','year_end','2026-12-31','2026 YE',?,?,?,1,'bayesian_brand_nb_split')""",
                [f"{market}-{mn}-YE-r1",market,mn,round(v),round(cl),round(ch)])
        if yer>0:
            yecpa=yec/yer
            con2.execute("""INSERT INTO ps.cumulative_projections 
                (projection_id,market,channel,metric_name,revision_date,horizon,
                 target_end_date,target_label,projected_cumulative,ci_low,ci_high,revision_number,reason)
                VALUES(?,?,'ps','cpa','2026-04-08','year_end','2026-12-31','2026 YE',?,?,?,1,'bayesian_brand_nb_split')""",
                [f"{market}-cpa-YE-r1",market,round(yecpa,2),round(yecpa*0.85,2),round(yecpa*1.15,2)])

        # Verify
        cnt=con2.execute(f"SELECT COUNT(*) FROM ps.cumulative_projections WHERE market='{market}'").fetchone()[0]
        print(f"  {market} ({stype}): {yer:,} regs YE, ${yec:,.0f} cost, {cnt} rows")
        con2.close()

    # ── WW + EU5 aggregates ──
    print("Building aggregates...")
    con3=duckdb.connect(f'md:ps_analytics?motherduck_token={TOKEN}')
    for agg,srcs in [('WW',ALL_MARKETS),('EU5',['UK','DE','FR','IT','ES'])]:
        for metric in ['registrations','cost']:
            for hz in ['weekly','monthly','quarterly','year_end']:
                rows=con3.execute(f"""SELECT target_label,target_end_date,
                    SUM(projected_cumulative),SUM(ci_low),SUM(ci_high)
                    FROM ps.cumulative_projections
                    WHERE market IN ({','.join(f"'{m}'" for m in srcs)})
                    AND metric_name='{metric}' AND horizon='{hz}'
                    GROUP BY target_label,target_end_date ORDER BY target_end_date""").fetchall()
                batch2=[]
                for lb,ed,pj,cl,ch in rows:
                    batch2.append((f"{agg}-{metric}-{lb}-r1",agg,'ps',metric,'2026-04-08',hz,ed,lb,round(pj),round(cl),round(ch),1,'aggregate'))
                if batch2:
                    for i in range(0,len(batch2),50):
                        con3.executemany("""INSERT INTO ps.cumulative_projections 
                            (projection_id,market,channel,metric_name,revision_date,horizon,
                             target_end_date,target_label,projected_cumulative,ci_low,ci_high,revision_number,reason)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",batch2[i:i+50])

    # Verify totals
    print("\nConsistency:")
    for mkt in ALL_MARKETS+['WW','EU5']:
        ws=con3.execute(f"SELECT SUM(projected_cumulative) FROM ps.cumulative_projections WHERE market='{mkt}' AND metric_name='registrations' AND horizon='weekly'").fetchone()[0] or 0
        qs=con3.execute(f"SELECT SUM(projected_cumulative) FROM ps.cumulative_projections WHERE market='{mkt}' AND metric_name='registrations' AND horizon='quarterly'").fetchone()[0] or 0
        ye=con3.execute(f"SELECT projected_cumulative FROM ps.cumulative_projections WHERE market='{mkt}' AND metric_name='registrations' AND horizon='year_end'").fetchone()
        ye=ye[0] if ye else 0
        ok="✅" if abs(ws-ye)<5 and abs(qs-ye)<5 else "❌"
        print(f"  {mkt}: wks={ws:,.0f} qtr={qs:,.0f} YE={ye:,.0f} {ok}")

    total=con3.execute("SELECT COUNT(*) FROM ps.cumulative_projections").fetchone()[0]
    print(f"\nTotal: {total} rows")
    con3.close()

if __name__=='__main__':
    run()
