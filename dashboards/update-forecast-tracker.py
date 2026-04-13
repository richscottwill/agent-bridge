#!/usr/bin/env python3
"""Update ps-forecast-tracker.xlsx — writes ONLY to hidden _Data sheet.

Visible market sheets reference _Data via formulas. This script never touches
visible sheets, preserving all formatting (column widths, row heights, alignments,
freeze panes, chart positions, fonts, fills, borders).

Usage: python3 update-forecast-tracker.py
"""
import duckdb, os

TOKEN = os.environ.get('MOTHERDUCK_TOKEN',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJpY2hzY290dHdpbGxAZ21haWwuY29tIiwibWRSZWdpb24iOiJhd3MtdXMtZWFzdC0xIiwic2Vzc2lvbiI6InJpY2hzY290dHdpbGwuZ21haWwuY29tIiwicGF0IjoiVDNIYzFVQWYzT3o1bjVkLS03ckdHNlBjMlpUdVNNbFItT3RXMS1qNzVPUSIsInVzZXJJZCI6ImU2MDhlNDZiLTE4YzctNGE5Ny04M2I2LWE0N2ZhOThmNjBhYyIsImlzcyI6Im1kX3BhdCIsInJlYWRPbmx5IjpmYWxzZSwidG9rZW5UeXBlIjoicmVhZF93cml0ZSIsImlhdCI6MTc3NTQ0MzY0N30.tS0Cab3FQ8_CDZ1PqOo9z09KYHEUFHwuLVXRQrxcHig')
XLSX = os.path.expanduser('~/shared/dashboards/ps-forecast-tracker.xlsx')
MARKETS = ['US','UK','DE','FR','IT','ES','CA','JP','MX','AU']
ML = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
MONTH_WEEKS = {1:(1,4),2:(5,8),3:(9,13),4:(14,17),5:(18,22),6:(23,26),
               7:(27,31),8:(32,35),9:(36,39),10:(40,44),11:(45,48),12:(49,52)}

# _Data sheet row offsets (must match the template)
WK_START = 2      # Weekly data starts row 2 (52 rows per market)
MO_START = 524    # Monthly data starts row 524 (12 rows per market)
Q_START = 648     # Quarterly starts row 648 (4 rows per market)
YE_START = 692    # Year-end starts row 692 (1 row per market)


def run():
    from openpyxl import load_workbook
    
    print("Connecting to MotherDuck...")
    con = duckdb.connect(f'md:ps_analytics?motherduck_token={TOKEN}', read_only=True)
    
    print(f"Opening {XLSX}...")
    wb = load_workbook(XLSX)
    
    if '_Data' not in wb.sheetnames:
        print("ERROR: _Data sheet not found. Run the template builder first.")
        return
    
    ds = wb['_Data']
    
    for mi, m in enumerate(MARKETS):
        # Pull forecast_tracker
        ft = {}
        rows = con.execute(f"""SELECT horizon, period_label, metric_name, predicted, ci_low, ci_high, actual
            FROM ps.forecast_tracker WHERE market='{m}'""").fetchall()
        for r in rows:
            ft[(r[0], r[1], r[2])] = {'pred': r[3], 'ci_lo': r[4], 'ci_hi': r[5], 'actual': r[6]}
        
        # Pull performance (actuals with brand/NB split)
        perf = {}
        try:
            prows = con.execute(f"""SELECT week_num, registrations, cost, cpa, brand_registrations, nb_registrations
                FROM ps.dive_weekly WHERE market='{m}' AND registrations IS NOT NULL""").fetchall()
            for r in prows:
                perf[r[0]] = {'regs': r[1], 'cost': r[2], 'cpa': r[3], 'brand': r[4], 'nb': r[5]}
        except: pass
        
        # Pull OP2 targets
        targets = {}
        try:
            trows = con.execute(f"""SELECT period_key, target_value FROM ps.targets 
                WHERE market='{m}' AND metric_name='registrations' AND period_type='monthly'""").fetchall()
            for r in trows:
                mo = int(r[0].replace('2026-M', ''))
                targets[mo] = r[1]
        except: pass
        
        # ── Write weekly rows ──
        for wk in range(1, 53):
            row = WK_START + mi * 52 + (wk - 1)
            
            p = perf.get(wk)
            if p:
                ds.cell(row=row, column=4).value = p['regs']
                ds.cell(row=row, column=5).value = round(p['cost']) if p['cost'] else None
                ds.cell(row=row, column=6).value = round(p['cpa'], 2) if p['cpa'] else None
                ds.cell(row=row, column=11).value = p.get('brand')
                ds.cell(row=row, column=12).value = p.get('nb')
            
            ft_wk = ft.get(('weekly', f'W{wk}', 'registrations'))
            if ft_wk:
                ds.cell(row=row, column=7).value = ft_wk['pred']
                ds.cell(row=row, column=8).value = ft_wk['ci_lo']
                ds.cell(row=row, column=9).value = ft_wk['ci_hi']
                ds.cell(row=row, column=10).value = 0.7 if ft_wk['pred'] else None
            
            # OP2 weekly
            for mo_num, (ws_s, ws_e) in MONTH_WEEKS.items():
                if ws_s <= wk <= ws_e and mo_num in targets:
                    ds.cell(row=row, column=13).value = round(targets[mo_num] / (ws_e - ws_s + 1))
                    break
        
        # ── Write monthly rows ──
        for mo in range(1, 13):
            row = MO_START + mi * 12 + (mo - 1)
            mo_label = ML[mo]
            ft_mo = ft.get(('monthly', mo_label, 'registrations'))
            if ft_mo:
                ds.cell(row=row, column=4).value = ft_mo['actual']
                ds.cell(row=row, column=5).value = ft_mo['pred']
                ds.cell(row=row, column=6).value = ft_mo['ci_lo']
                ds.cell(row=row, column=7).value = ft_mo['ci_hi']
            if mo in targets:
                ds.cell(row=row, column=8).value = round(targets[mo])
        
        # ── Write quarterly rows ──
        for qi, ql in enumerate(['Q1','Q2','Q3','Q4']):
            row = Q_START + mi * 4 + qi
            ft_q = ft.get(('quarterly', ql, 'registrations'))
            if ft_q:
                ds.cell(row=row, column=4).value = ft_q['actual']
                ds.cell(row=row, column=5).value = ft_q['pred']
                ds.cell(row=row, column=6).value = ft_q['ci_lo']
                ds.cell(row=row, column=7).value = ft_q['ci_hi']
            q_months = [qi*3+1, qi*3+2, qi*3+3]
            q_op2 = sum(targets.get(m2, 0) for m2 in q_months)
            if q_op2: ds.cell(row=row, column=8).value = round(q_op2)
        
        # ── Write year-end row ──
        row = YE_START + mi
        ft_ye = ft.get(('year_end', '2026', 'registrations'))
        if ft_ye:
            ds.cell(row=row, column=2).value = ft_ye['actual']
            ds.cell(row=row, column=3).value = ft_ye['pred']
            ds.cell(row=row, column=4).value = ft_ye['ci_lo']
            ds.cell(row=row, column=5).value = ft_ye['ci_hi']
        annual_op2 = sum(targets.values())
        if annual_op2: ds.cell(row=row, column=6).value = round(annual_op2)
        
        print(f"  {m}: {len(perf)} weeks, {sum(1 for k in ft if ft[k]['pred']) } predictions")
    
    con.close()
    
    print(f"Saving {XLSX}...")
    wb.save(XLSX)
    print(f"Done: {os.path.getsize(XLSX):,} bytes")


if __name__ == '__main__':
    run()
