#!/usr/bin/env python3
"""Populate ps.forecast_tracker with Bayesian projections for all periods.

Uses BayesianProjector (proper Bayesian engine with seasonal priors from
ps.seasonal_priors, ie%CCP constraints, calibration factors) for weekly
and monthly projections. Quarterly and year-end derived from monthly sums.

Re-runnable: updates predicted/ci columns only, preserves actuals.

Usage: python3 populate_forecast_tracker.py
"""
import sys, os, math, traceback
import duckdb

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import logging
logging.disable(logging.WARNING)  # Suppress all debug/info/warning from BayesianProjector
from prediction.bayesian_projector import BayesianProjector, ALL_MARKETS

TOKEN = os.environ.get('MOTHERDUCK_TOKEN',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJpY2hzY290dHdpbGxAZ21haWwuY29tIiwibWRSZWdpb24iOiJhd3MtdXMtZWFzdC0xIiwic2Vzc2lvbiI6InJpY2hzY290dHdpbGwuZ21haWwuY29tIiwicGF0IjoiVDNIYzFVQWYzT3o1bjVkLS03ckdHNlBjMlpUdVNNbFItT3RXMS1qNzVPUSIsInVzZXJJZCI6ImU2MDhlNDZiLTE4YzctNGE5Ny04M2I2LWE0N2ZhOThmNjBhYyIsImlzcyI6Im1kX3BhdCIsInJlYWRPbmx5IjpmYWxzZSwidG9rZW5UeXBlIjoicmVhZF93cml0ZSIsImlhdCI6MTc3NTQ0MzY0N30.tS0Cab3FQ8_CDZ1PqOo9z09KYHEUFHwuLVXRQrxcHig')
ML = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
      7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}

def run():
    con = duckdb.connect(f'md:ps_analytics?motherduck_token={TOKEN}')

    # Clear predictions only (preserve actuals)
    con.execute("UPDATE ps.forecast_tracker SET predicted=NULL, ci_low=NULL, ci_high=NULL, updated_at=current_timestamp")
    print("Cleared predictions\n")

    # Get calibration factor
    cal = 1.0
    try:
        row = con.execute("SELECT AVG(calibration_factor) FROM ps.calibration_state WHERE total_scored >= 3").fetchone()
        if row and row[0]: cal = float(row[0])
    except: pass
    print(f"Calibration factor: {cal:.3f}")

    projector = BayesianProjector(con, calibration_factor=cal)

    # ── Step 1: Weekly projections (W1-W52) per market ──
    print("\n=== Weekly ===")
    for market in ALL_MARKETS:
        ok = 0
        for wk in range(1, 53):
            try:
                p = projector.project_market(market, wk, f"2026-W{wk:02d}")
                if p and p.total_regs is not None:
                    # Registrations
                    con.execute("UPDATE ps.forecast_tracker SET predicted=?, ci_low=?, ci_high=?, updated_at=current_timestamp WHERE market=? AND metric_name='registrations' AND horizon='weekly' AND period_label=?",
                        [round(p.total_regs), round(p.ci_regs_low), round(p.ci_regs_high), market, f'W{wk}'])
                    # Cost
                    ci_cost_lo = round(p.total_cost * 0.85, 2)
                    ci_cost_hi = round(p.total_cost * 1.15, 2)
                    con.execute("UPDATE ps.forecast_tracker SET predicted=?, ci_low=?, ci_high=?, updated_at=current_timestamp WHERE market=? AND metric_name='cost' AND horizon='weekly' AND period_label=?",
                        [round(p.total_cost, 2), ci_cost_lo, ci_cost_hi, market, f'W{wk}'])
                    ok += 1
            except Exception as e:
                if wk == 1: print(f"  {market} W{wk}: {e}")
        print(f"  {market}: {ok}/52 weeks")

    # ── Step 2: Monthly projections (M01-M12) per market ──
    print("\n=== Monthly ===")
    for market in ALL_MARKETS:
        ok = 0
        for mo in range(1, 13):
            try:
                p = projector.project_market_monthly(market, f"2026-M{mo:02d}")
                if p and p.total_regs is not None:
                    con.execute("UPDATE ps.forecast_tracker SET predicted=?, ci_low=?, ci_high=?, updated_at=current_timestamp WHERE market=? AND metric_name='registrations' AND horizon='monthly' AND period_label=?",
                        [round(p.total_regs), round(p.ci_regs_low), round(p.ci_regs_high), market, ML[mo]])
                    ci_cost_lo = round(p.total_cost * 0.85, 2)
                    ci_cost_hi = round(p.total_cost * 1.15, 2)
                    con.execute("UPDATE ps.forecast_tracker SET predicted=?, ci_low=?, ci_high=?, updated_at=current_timestamp WHERE market=? AND metric_name='cost' AND horizon='monthly' AND period_label=?",
                        [round(p.total_cost, 2), ci_cost_lo, ci_cost_hi, market, ML[mo]])
                    ok += 1
            except Exception as e:
                if mo == 1: print(f"  {market} M{mo}: {e}")
        print(f"  {market}: {ok}/12 months")

    # ── Step 3: Quarterly (sum of monthly predictions) ──
    print("\n=== Quarterly ===")
    QM = {'Q1':['Jan','Feb','Mar'],'Q2':['Apr','May','Jun'],'Q3':['Jul','Aug','Sep'],'Q4':['Oct','Nov','Dec']}
    for market in ALL_MARKETS:
        for ql, mos in QM.items():
            for metric in ['registrations', 'cost']:
                row = con.execute(
                    "SELECT SUM(predicted), ROUND(SQRT(SUM(POWER(GREATEST(ci_high-predicted,1),2)))), ROUND(SQRT(SUM(POWER(GREATEST(predicted-ci_low,1),2)))) FROM ps.forecast_tracker WHERE market=? AND metric_name=? AND horizon='monthly' AND period_label IN (?,?,?)",
                    [market, metric, mos[0], mos[1], mos[2]]).fetchone()
                if row[0] is not None:
                    pred = round(row[0])
                    ci_hi_width = row[1] or 0
                    ci_lo_width = row[2] or 0
                    con.execute("UPDATE ps.forecast_tracker SET predicted=?, ci_low=?, ci_high=?, updated_at=current_timestamp WHERE market=? AND metric_name=? AND horizon='quarterly' AND period_label=?",
                        [pred, round(max(0, pred - ci_lo_width)), round(pred + ci_hi_width), market, metric, ql])
        print(f"  {market}: Q1-Q4")

    # ── Step 4: Year-end (sum of quarterly) ──
    print("\n=== Year-End ===")
    for market in ALL_MARKETS:
        for metric in ['registrations', 'cost']:
            row = con.execute(
                "SELECT SUM(predicted), ROUND(SQRT(SUM(POWER(GREATEST(ci_high-predicted,1),2)))), ROUND(SQRT(SUM(POWER(GREATEST(predicted-ci_low,1),2)))) FROM ps.forecast_tracker WHERE market=? AND metric_name=? AND horizon='quarterly'",
                [market, metric]).fetchone()
            if row[0] is not None:
                pred = round(row[0])
                ci_hi_w = row[1] or 0
                ci_lo_w = row[2] or 0
                con.execute("UPDATE ps.forecast_tracker SET predicted=?, ci_low=?, ci_high=?, updated_at=current_timestamp WHERE market=? AND metric_name=? AND horizon='year_end' AND period_label='2026'",
                    [pred, round(max(0, pred - ci_lo_w)), round(pred + ci_hi_w), market, metric])
        print(f"  {market}: 2026 YE")

    # ── Step 5: Aggregates (WW, EU5) ──
    print("\n=== Aggregates ===")
    for agg, srcs in [('WW', ALL_MARKETS), ('EU5', ['UK','DE','FR','IT','ES'])]:
        sl = ",".join(f"'{m}'" for m in srcs)
        for hz in ['weekly','monthly','quarterly','year_end']:
            con.execute(f"""UPDATE ps.forecast_tracker ft SET predicted=a.p, ci_low=a.cl, ci_high=a.ch, updated_at=current_timestamp
                FROM (SELECT period_label, metric_name, ROUND(SUM(predicted)) p, ROUND(SUM(ci_low)) cl, ROUND(SUM(ci_high)) ch
                    FROM ps.forecast_tracker WHERE market IN ({sl}) AND horizon='{hz}' GROUP BY period_label, metric_name) a
                WHERE ft.market='{agg}' AND ft.horizon='{hz}' AND ft.period_label=a.period_label AND ft.metric_name=a.metric_name""")
        print(f"  {agg}")

    # ── Verify ──
    miss = con.execute("SELECT COUNT(*) FROM ps.forecast_tracker WHERE predicted IS NULL").fetchone()[0]
    tot = con.execute("SELECT COUNT(*) FROM ps.forecast_tracker").fetchone()[0]
    print(f"\nDone: {tot} rows, {miss} missing predictions")
    for m in ['AU','MX','US','WW']:
        ye = con.execute(f"SELECT predicted, ci_low, ci_high FROM ps.forecast_tracker WHERE market='{m}' AND metric_name='registrations' AND horizon='year_end'").fetchone()
        if ye: print(f"  {m} YE: {ye[0]:,.0f} [{ye[1]:,.0f}-{ye[2]:,.0f}]")
        w15 = con.execute(f"SELECT predicted, ci_low, ci_high FROM ps.forecast_tracker WHERE market='{m}' AND metric_name='registrations' AND horizon='weekly' AND period_label='W15'").fetchone()
        if w15: print(f"  {m} W15: {w15[0]:,.0f} [{w15[1]:,.0f}-{w15[2]:,.0f}]")
    con.close()

if __name__ == '__main__':
    run()
