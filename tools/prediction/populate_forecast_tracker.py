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

# Decay rate for time-weighted predictions
# λ = 0.2: N-1 = 0.82, N-2 = 0.67, N-4 = 0.45, N-8 = 0.20, N-16 = 0.04
DECAY_LAMBDA = 0.2

def weighted_prediction(forecasts_for_target):
    """Compute time-decay-weighted average of all predictions for a target period.
    
    Args:
        forecasts_for_target: list of (forecast_date, target_week_start, predicted_value, ci_low, ci_high)
            where target_week_start is the date the target week begins
    
    Returns:
        (weighted_pred, weighted_ci_low, weighted_ci_high) or (None, None, None) if no data
    """
    if not forecasts_for_target:
        return None, None, None
    
    total_weight = 0.0
    weighted_pred = 0.0
    weighted_ci_low = 0.0
    weighted_ci_high = 0.0
    
    for forecast_date, target_start, pred, ci_lo, ci_hi in forecasts_for_target:
        if pred is None:
            continue
        # Distance in weeks between forecast date and target week start
        if target_start and forecast_date:
            days_before = (target_start - forecast_date).days
            weeks_before = max(days_before / 7.0, 0.0)
        else:
            weeks_before = 0.0
        
        weight = math.exp(-DECAY_LAMBDA * weeks_before)
        total_weight += weight
        weighted_pred += pred * weight
        if ci_lo is not None:
            weighted_ci_low += ci_lo * weight
        if ci_hi is not None:
            weighted_ci_high += ci_hi * weight
    
    if total_weight == 0:
        return None, None, None
    
    return (
        round(weighted_pred / total_weight),
        round(weighted_ci_low / total_weight) if weighted_ci_low else None,
        round(weighted_ci_high / total_weight) if weighted_ci_high else None
    )

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

    # ── Step 5a: Store current monthly/quarterly/year-end predictions as revisions in ps.forecasts ──
    print("\n=== Storing forecast revisions ===")
    import uuid
    from datetime import date as dt_date
    today = dt_date.today()
    stored = 0
    try:
        # Monthly: read current predictions from forecast_tracker, store as revision
        for market in ALL_MARKETS:
            for metric in ['registrations', 'cost']:
                rows = con.execute(f"""SELECT period_label, period_order, predicted, ci_low, ci_high 
                    FROM ps.forecast_tracker WHERE market='{market}' AND metric_name='{metric}' 
                    AND horizon='monthly' AND predicted IS NOT NULL""").fetchall()
                for r in rows:
                    period_label, period_order, pred, ci_lo, ci_hi = r
                    # Map period_label (Jan) → target_period (2026-M01)
                    mo_num = {v: k for k, v in ML.items()}.get(period_label)
                    if not mo_num:
                        continue
                    target_period = f"2026-M{mo_num:02d}"
                    # Check if we already stored a revision for this market/metric/period today
                    existing = con.execute(
                        "SELECT COUNT(*) FROM ps.forecasts WHERE market=? AND metric_name=? AND target_period=? AND forecast_date=? AND method LIKE 'bayesian%'",
                        [market, metric, target_period, today]).fetchone()[0]
                    if existing == 0:
                        con.execute(
                            "INSERT INTO ps.forecasts (forecast_id, market, channel, metric_name, forecast_date, target_period, period_type, predicted_value, confidence_low, confidence_high, method, created_at) VALUES (?, ?, 'ps', ?, ?, ?, 'monthly', ?, ?, ?, 'bayesian_populate', current_timestamp)",
                            [str(uuid.uuid4()), market, metric, today, target_period, pred, ci_lo, ci_hi])
                        stored += 1
                
                # Quarterly
                for ql, mo_nums in [('Q1',[1,2,3]),('Q2',[4,5,6]),('Q3',[7,8,9]),('Q4',[10,11,12])]:
                    qr = con.execute(f"""SELECT predicted, ci_low, ci_high FROM ps.forecast_tracker 
                        WHERE market='{market}' AND metric_name='{metric}' AND horizon='quarterly' AND period_label='{ql}'""").fetchone()
                    if qr and qr[0]:
                        target_period = f"2026-{ql}"
                        existing = con.execute(
                            "SELECT COUNT(*) FROM ps.forecasts WHERE market=? AND metric_name=? AND target_period=? AND forecast_date=? AND method LIKE 'bayesian%'",
                            [market, metric, target_period, today]).fetchone()[0]
                        if existing == 0:
                            con.execute(
                                "INSERT INTO ps.forecasts (forecast_id, market, channel, metric_name, forecast_date, target_period, period_type, predicted_value, confidence_low, confidence_high, method, created_at) VALUES (?, ?, 'ps', ?, ?, ?, 'quarterly', ?, ?, ?, 'bayesian_populate', current_timestamp)",
                                [str(uuid.uuid4()), market, metric, today, target_period, qr[0], qr[1], qr[2]])
                            stored += 1
                
                # Year-end
                yr = con.execute(f"""SELECT predicted, ci_low, ci_high FROM ps.forecast_tracker 
                    WHERE market='{market}' AND metric_name='{metric}' AND horizon='year_end' AND period_label='2026'""").fetchone()
                if yr and yr[0]:
                    existing = con.execute(
                        "SELECT COUNT(*) FROM ps.forecasts WHERE market=? AND metric_name=? AND target_period='2026-YE' AND forecast_date=? AND method LIKE 'bayesian%'",
                        [market, metric, today]).fetchone()[0]
                    if existing == 0:
                        con.execute(
                            "INSERT INTO ps.forecasts (forecast_id, market, channel, metric_name, forecast_date, target_period, period_type, predicted_value, confidence_low, confidence_high, method, created_at) VALUES (?, ?, 'ps', ?, ?, '2026-YE', 'year_end', ?, ?, ?, 'bayesian_populate', current_timestamp)",
                            [str(uuid.uuid4()), market, metric, today, yr[0], yr[1], yr[2]])
                        stored += 1
        print(f"  {stored} new forecast revisions stored")
    except Exception as e:
        print(f"  Revision storage error: {e}")
        traceback.print_exc()

    # ── Step 5b: Weighted predictions for WEEKLY, then derive higher horizons by summing ──
    print("\n=== Weighted Predictions (exponential decay λ=%.1f) ===" % DECAY_LAMBDA)
    # Weekly: time-decay-weighted average across all revisions in ps.forecasts
    # Monthly/Quarterly/Year-end: ALWAYS derived from sum of weekly predictions (reconciles by construction)
    from collections import defaultdict
    from datetime import date, timedelta
    
    w1_start = date(2025, 12, 29)
    
    wt_updated = 0
    try:
        # Step 5b-1: Apply weighted predictions to WEEKLY only
        all_fc = con.execute("""
            SELECT market, metric_name, target_period, forecast_date, predicted_value, 
                   confidence_low, confidence_high
            FROM ps.forecasts 
            WHERE target_period LIKE '2026-W%' AND method LIKE 'bayesian%'
            ORDER BY market, metric_name, target_period, forecast_date
        """).fetchall()
        
        groups = defaultdict(list)
        for row in all_fc:
            groups[(row[0], row[1], row[2])].append(row)
        
        for (market, metric, target_period), forecasts in groups.items():
            if not forecasts:
                continue
            wk = int(target_period.replace('2026-W', ''))
            tgt_start = w1_start + timedelta(weeks=wk - 1)
            fc_input = [(r[3], tgt_start, r[4], r[5], r[6]) for r in forecasts]
            w_pred, w_ci_lo, w_ci_hi = weighted_prediction(fc_input)
            if w_pred is not None:
                period_label = f'W{wk}'
                con.execute(
                    "UPDATE ps.forecast_tracker SET predicted=?, ci_low=?, ci_high=?, updated_at=current_timestamp WHERE market=? AND metric_name=? AND horizon='weekly' AND period_label=?",
                    [w_pred, w_ci_lo, w_ci_hi, market, metric, period_label])
                wt_updated += 1
        
        print(f"  {wt_updated} weekly predictions updated with weighted averages")
        
        # Step 5b-2: Derive MONTHLY from sum of weekly predictions
        MONTH_WEEKS = {1:(1,4),2:(5,8),3:(9,13),4:(14,17),5:(18,22),6:(23,26),
                       7:(27,31),8:(32,35),9:(36,39),10:(40,44),11:(45,48),12:(49,52)}
        mo_updated = 0
        for mo_num, (ws, we) in MONTH_WEEKS.items():
            mo_label = ML[mo_num]
            wk_labels = ",".join(f"'W{w}'" for w in range(ws, we + 1))
            for metric in ['registrations', 'cost']:
                con.execute(f"""UPDATE ps.forecast_tracker ft SET 
                    predicted = sub.total_pred,
                    ci_low = sub.total_lo,
                    ci_high = sub.total_hi,
                    updated_at = current_timestamp
                    FROM (SELECT market, ROUND(SUM(predicted)) as total_pred, ROUND(SUM(ci_low)) as total_lo, ROUND(SUM(ci_high)) as total_hi
                          FROM ps.forecast_tracker
                          WHERE metric_name='{metric}' AND horizon='weekly' AND period_label IN ({wk_labels}) AND predicted IS NOT NULL
                          GROUP BY market) sub
                    WHERE ft.market=sub.market AND ft.metric_name='{metric}' AND ft.horizon='monthly' AND ft.period_label='{mo_label}'""")
                mo_updated += 1
        print(f"  {mo_updated} monthly predictions derived from weekly sums")
        
        # Step 5b-3: Derive QUARTERLY from sum of monthly predictions
        QM = {'Q1':['Jan','Feb','Mar'],'Q2':['Apr','May','Jun'],'Q3':['Jul','Aug','Sep'],'Q4':['Oct','Nov','Dec']}
        for ql, mos in QM.items():
            mo_labels = ",".join(f"'{m}'" for m in mos)
            for metric in ['registrations', 'cost']:
                con.execute(f"""UPDATE ps.forecast_tracker ft SET 
                    predicted = sub.total_pred,
                    ci_low = sub.total_lo,
                    ci_high = sub.total_hi,
                    updated_at = current_timestamp
                    FROM (SELECT market, ROUND(SUM(predicted)) as total_pred, ROUND(SUM(ci_low)) as total_lo, ROUND(SUM(ci_high)) as total_hi
                          FROM ps.forecast_tracker
                          WHERE metric_name='{metric}' AND horizon='monthly' AND period_label IN ({mo_labels}) AND predicted IS NOT NULL
                          GROUP BY market) sub
                    WHERE ft.market=sub.market AND ft.metric_name='{metric}' AND ft.horizon='quarterly' AND ft.period_label='{ql}'""")
        print(f"  Quarterly predictions derived from monthly sums")
        
        # Step 5b-4: Derive YEAR-END from sum of quarterly predictions
        for metric in ['registrations', 'cost']:
            con.execute(f"""UPDATE ps.forecast_tracker ft SET 
                predicted = sub.total_pred,
                ci_low = sub.total_lo,
                ci_high = sub.total_hi,
                updated_at = current_timestamp
                FROM (SELECT market, ROUND(SUM(predicted)) as total_pred, ROUND(SUM(ci_low)) as total_lo, ROUND(SUM(ci_high)) as total_hi
                      FROM ps.forecast_tracker
                      WHERE metric_name='{metric}' AND horizon='quarterly' AND predicted IS NOT NULL
                      GROUP BY market) sub
                WHERE ft.market=sub.market AND ft.metric_name='{metric}' AND ft.horizon='year_end'""")
        print(f"  Year-end predictions derived from quarterly sums")
        
        # Verify reconciliation for AU
        wk_sum = con.execute("SELECT SUM(predicted) FROM ps.forecast_tracker WHERE market='AU' AND metric_name='registrations' AND horizon='weekly'").fetchone()[0]
        mo_sum = con.execute("SELECT SUM(predicted) FROM ps.forecast_tracker WHERE market='AU' AND metric_name='registrations' AND horizon='monthly'").fetchone()[0]
        q_sum = con.execute("SELECT SUM(predicted) FROM ps.forecast_tracker WHERE market='AU' AND metric_name='registrations' AND horizon='quarterly'").fetchone()[0]
        ye = con.execute("SELECT predicted FROM ps.forecast_tracker WHERE market='AU' AND metric_name='registrations' AND horizon='year_end'").fetchone()[0]
        print(f"  AU regs reconciliation: weekly={wk_sum}, monthly={mo_sum}, quarterly={q_sum}, year_end={ye}")
        
    except Exception as e:
        print(f"  Weighted prediction error: {e}")
        traceback.print_exc()

    # ── Step 6: Backfill actuals from ps.dive_weekly into forecast_tracker ──
    print("\n=== Backfill Actuals ===")
    # Weekly actuals: dive_weekly has the most complete pivoted data
    try:
        # Registrations
        con.execute("""UPDATE ps.forecast_tracker ft SET actual=dw.registrations, updated_at=current_timestamp
            FROM ps.dive_weekly dw
            WHERE dw.registrations IS NOT NULL
            AND ft.market=dw.market AND ft.metric_name='registrations' AND ft.horizon='weekly'
            AND ft.period_label='W' || CAST(dw.week_num AS VARCHAR)""")
        # Cost
        con.execute("""UPDATE ps.forecast_tracker ft SET actual=ROUND(dw.cost, 2), updated_at=current_timestamp
            FROM ps.dive_weekly dw
            WHERE dw.cost IS NOT NULL
            AND ft.market=dw.market AND ft.metric_name='cost' AND ft.horizon='weekly'
            AND ft.period_label='W' || CAST(dw.week_num AS VARCHAR)""")
        updated = con.execute("SELECT COUNT(*) FROM ps.forecast_tracker WHERE actual IS NOT NULL AND horizon='weekly'").fetchone()[0]
        print(f"  Weekly actuals backfilled: {updated} rows")
    except Exception as e:
        print(f"  Weekly backfill error: {e}")

    # Monthly actuals: sum weekly actuals within each month
    try:
        ML_WEEKS = {1:(1,4),2:(5,8),3:(9,13),4:(14,17),5:(18,22),6:(23,26),
                    7:(27,31),8:(32,35),9:(36,39),10:(40,44),11:(45,48),12:(49,52)}
        for mo_num, (ws, we) in ML_WEEKS.items():
            mo_label = ML[mo_num]
            wk_labels = ",".join(f"'W{w}'" for w in range(ws, we+1))
            # Only backfill if ALL weeks in the month have actuals
            for metric in ['registrations', 'cost']:
                con.execute(f"""UPDATE ps.forecast_tracker ft SET actual=sub.total, updated_at=current_timestamp
                    FROM (SELECT market, SUM(actual) as total, COUNT(actual) as cnt
                          FROM ps.forecast_tracker
                          WHERE metric_name='{metric}' AND horizon='weekly' AND period_label IN ({wk_labels})
                          GROUP BY market HAVING cnt = {we - ws + 1}) sub
                    WHERE ft.market=sub.market AND ft.metric_name='{metric}' AND ft.horizon='monthly' AND ft.period_label='{mo_label}'""")
        mo_updated = con.execute("SELECT COUNT(*) FROM ps.forecast_tracker WHERE actual IS NOT NULL AND horizon='monthly'").fetchone()[0]
        print(f"  Monthly actuals backfilled: {mo_updated} rows")
    except Exception as e:
        print(f"  Monthly backfill error: {e}")

    # Quarterly + Year-end actuals: sum from monthly
    try:
        QM = {'Q1':['Jan','Feb','Mar'],'Q2':['Apr','May','Jun'],'Q3':['Jul','Aug','Sep'],'Q4':['Oct','Nov','Dec']}
        for ql, mos in QM.items():
            mo_labels = ",".join(f"'{m}'" for m in mos)
            for metric in ['registrations', 'cost']:
                con.execute(f"""UPDATE ps.forecast_tracker ft SET actual=sub.total, updated_at=current_timestamp
                    FROM (SELECT market, SUM(actual) as total, COUNT(actual) as cnt
                          FROM ps.forecast_tracker
                          WHERE metric_name='{metric}' AND horizon='monthly' AND period_label IN ({mo_labels})
                          GROUP BY market HAVING cnt = 3) sub
                    WHERE ft.market=sub.market AND ft.metric_name='{metric}' AND ft.horizon='quarterly' AND ft.period_label='{ql}'""")
        # Year-end from quarterly
        for metric in ['registrations', 'cost']:
            con.execute(f"""UPDATE ps.forecast_tracker ft SET actual=sub.total, updated_at=current_timestamp
                FROM (SELECT market, SUM(actual) as total, COUNT(actual) as cnt
                      FROM ps.forecast_tracker
                      WHERE metric_name='{metric}' AND horizon='quarterly'
                      GROUP BY market HAVING cnt = 4) sub
                WHERE ft.market=sub.market AND ft.metric_name='{metric}' AND ft.horizon='year_end'""")
        q_updated = con.execute("SELECT COUNT(*) FROM ps.forecast_tracker WHERE actual IS NOT NULL AND horizon='quarterly'").fetchone()[0]
        print(f"  Quarterly actuals backfilled: {q_updated} rows")
    except Exception as e:
        print(f"  Quarterly backfill error: {e}")

    # Aggregate actuals (WW, EU5)
    try:
        for agg, srcs in [('WW', ALL_MARKETS), ('EU5', ['UK','DE','FR','IT','ES'])]:
            sl = ",".join(f"'{m}'" for m in srcs)
            for hz in ['weekly','monthly','quarterly','year_end']:
                con.execute(f"""UPDATE ps.forecast_tracker ft SET actual=a.total, updated_at=current_timestamp
                    FROM (SELECT period_label, metric_name, ROUND(SUM(actual)) as total
                        FROM ps.forecast_tracker WHERE market IN ({sl}) AND horizon='{hz}' AND actual IS NOT NULL
                        GROUP BY period_label, metric_name) a
                    WHERE ft.market='{agg}' AND ft.horizon='{hz}' AND ft.period_label=a.period_label AND ft.metric_name=a.metric_name""")
        print(f"  Aggregate actuals (WW, EU5) backfilled")
    except Exception as e:
        print(f"  Aggregate backfill error: {e}")

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
