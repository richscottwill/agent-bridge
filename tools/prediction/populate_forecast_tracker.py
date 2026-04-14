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
from prediction.config import MOTHERDUCK_TOKEN as TOKEN, ML

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

    # Steps 2-4 REMOVED (2026-04-13): Monthly/quarterly/year-end projections are now
    # derived from weekly sums in step 5b. Independent Bayesian monthly/quarterly projections
    # were producing values that didn't reconcile with weekly sums. Weekly is the source of truth.

    # ── Step 5: Aggregates (WW, EU5) — applied AFTER step 5b derives higher horizons ──
    # (Moved to after 5b so aggregates use the derived values)

    # Step 5a REMOVED (2026-04-13): Was storing derived monthly/quarterly/year-end sums
    # as independent forecast revisions in ps.forecasts — polluted revision history.
    # Weekly revisions in ps.forecasts are the only source of truth.
    # Monthly/quarterly/year-end can always be reconstructed by summing weekly.

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
        
        # Step 5b-2: Derive MONTHLY from weekly: actuals for completed weeks + predictions for future
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
                    FROM (SELECT market, 
                          ROUND(SUM(COALESCE(actual, predicted))) as total_pred,
                          ROUND(SUM(COALESCE(actual, ci_low))) as total_lo,
                          ROUND(SUM(COALESCE(actual, ci_high))) as total_hi
                          FROM ps.forecast_tracker
                          WHERE metric_name='{metric}' AND horizon='weekly' AND period_label IN ({wk_labels}) AND predicted IS NOT NULL
                          GROUP BY market) sub
                    WHERE ft.market=sub.market AND ft.metric_name='{metric}' AND ft.horizon='monthly' AND ft.period_label='{mo_label}'""")
                mo_updated += 1
        print(f"  {mo_updated} monthly projections derived (actuals + predictions)")
        
        # Step 5b-3: Derive QUARTERLY from monthly: actuals for completed months + predictions for future
        QM = {'Q1':['Jan','Feb','Mar'],'Q2':['Apr','May','Jun'],'Q3':['Jul','Aug','Sep'],'Q4':['Oct','Nov','Dec']}
        for ql, mos in QM.items():
            mo_labels = ",".join(f"'{m}'" for m in mos)
            for metric in ['registrations', 'cost']:
                con.execute(f"""UPDATE ps.forecast_tracker ft SET 
                    predicted = sub.total_pred,
                    ci_low = sub.total_lo,
                    ci_high = sub.total_hi,
                    updated_at = current_timestamp
                    FROM (SELECT market, 
                          ROUND(SUM(COALESCE(actual, predicted))) as total_pred,
                          ROUND(SUM(COALESCE(actual, ci_low))) as total_lo,
                          ROUND(SUM(COALESCE(actual, ci_high))) as total_hi
                          FROM ps.forecast_tracker
                          WHERE metric_name='{metric}' AND horizon='monthly' AND period_label IN ({mo_labels}) AND predicted IS NOT NULL
                          GROUP BY market) sub
                    WHERE ft.market=sub.market AND ft.metric_name='{metric}' AND ft.horizon='quarterly' AND ft.period_label='{ql}'""")
        print(f"  Quarterly projections derived (actuals + predictions)")
        
        # Step 5b-4: Derive YEAR-END from quarterly: actuals for completed quarters + predictions for future
        for metric in ['registrations', 'cost']:
            con.execute(f"""UPDATE ps.forecast_tracker ft SET 
                predicted = sub.total_pred,
                ci_low = sub.total_lo,
                ci_high = sub.total_hi,
                updated_at = current_timestamp
                FROM (SELECT market, 
                      ROUND(SUM(COALESCE(actual, predicted))) as total_pred,
                      ROUND(SUM(COALESCE(actual, ci_low))) as total_lo,
                      ROUND(SUM(COALESCE(actual, ci_high))) as total_hi
                      FROM ps.forecast_tracker
                      WHERE metric_name='{metric}' AND horizon='quarterly' AND predicted IS NOT NULL
                      GROUP BY market) sub
                WHERE ft.market=sub.market AND ft.metric_name='{metric}' AND ft.horizon='year_end'""")
        print(f"  Year-end projections derived (actuals + predictions)")
        
        # Verify reconciliation for AU
        wk_sum = con.execute("SELECT SUM(predicted) FROM ps.forecast_tracker WHERE market='AU' AND metric_name='registrations' AND horizon='weekly'").fetchone()[0]
        mo_sum = con.execute("SELECT SUM(predicted) FROM ps.forecast_tracker WHERE market='AU' AND metric_name='registrations' AND horizon='monthly'").fetchone()[0]
        q_sum = con.execute("SELECT SUM(predicted) FROM ps.forecast_tracker WHERE market='AU' AND metric_name='registrations' AND horizon='quarterly'").fetchone()[0]
        ye = con.execute("SELECT predicted FROM ps.forecast_tracker WHERE market='AU' AND metric_name='registrations' AND horizon='year_end'").fetchone()[0]
        print(f"  AU regs reconciliation: weekly={wk_sum}, monthly={mo_sum}, quarterly={q_sum}, year_end={ye}")
        
    except Exception as e:
        print(f"  Weighted prediction error: {e}")
        traceback.print_exc()

    # ── Step 5c: Aggregates (WW, EU5) — AFTER derivation so they use correct values ──
    print("\n=== Aggregates ===")
    for agg, srcs in [('WW', ALL_MARKETS), ('EU5', ['UK','DE','FR','IT','ES'])]:
        sl = ",".join(f"'{m}'" for m in srcs)
        for hz in ['weekly','monthly','quarterly','year_end']:
            con.execute(f"""UPDATE ps.forecast_tracker ft SET predicted=a.p, ci_low=a.cl, ci_high=a.ch, updated_at=current_timestamp
                FROM (SELECT period_label, metric_name, ROUND(SUM(predicted)) p, ROUND(SUM(ci_low)) cl, ROUND(SUM(ci_high)) ch
                    FROM ps.forecast_tracker WHERE market IN ({sl}) AND horizon='{hz}' GROUP BY period_label, metric_name) a
                WHERE ft.market='{agg}' AND ft.horizon='{hz}' AND ft.period_label=a.period_label AND ft.metric_name=a.metric_name""")
        print(f"  {agg}")

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

    # ── Reconciliation Checks ──
    # These describe what should be true about the data. Violations are warnings,
    # not hard stops — but they mean something is probably wrong.
    print("\n=== Reconciliation Checks ===")
    warnings = []

    # 1. A month's projection should never be less than the actuals already recorded
    #    for its completed weeks. If April has 2 weeks of actuals totaling 16,000,
    #    the April projection better be at least 16,000.
    try:
        rows = con.execute("""
            SELECT w.market, w.metric_name, m.period_label as month,
                ROUND(SUM(w.actual)) as ytd_actuals_in_month,
                m.predicted as month_projection
            FROM ps.forecast_tracker w
            JOIN ps.forecast_tracker m 
                ON w.market = m.market AND w.metric_name = m.metric_name
            WHERE w.horizon = 'weekly' AND w.actual IS NOT NULL
            AND m.horizon = 'monthly' AND m.predicted IS NOT NULL
            AND (
                (m.period_label = 'Jan' AND w.period_label IN ('W1','W2','W3','W4'))
                OR (m.period_label = 'Feb' AND w.period_label IN ('W5','W6','W7','W8'))
                OR (m.period_label = 'Mar' AND w.period_label IN ('W9','W10','W11','W12','W13'))
                OR (m.period_label = 'Apr' AND w.period_label IN ('W14','W15','W16','W17'))
                OR (m.period_label = 'May' AND w.period_label IN ('W18','W19','W20','W21','W22'))
                OR (m.period_label = 'Jun' AND w.period_label IN ('W23','W24','W25','W26'))
            )
            GROUP BY w.market, w.metric_name, m.period_label, m.predicted
            HAVING SUM(w.actual) > m.predicted * 1.001
        """).fetchall()
        for r in rows:
            msg = f"  ⚠ {r[0]} {r[2]} {r[1]}: month projection ({r[4]:,.0f}) is less than actuals already in ({r[3]:,.0f})"
            warnings.append(msg)
            print(msg)
    except Exception as e:
        print(f"  Check 1 error: {e}")

    # 2. Year-end projection should be at least as large as YTD actuals.
    #    If we've already recorded 125K US regs through W15, the year-end
    #    number can't be 100K.
    try:
        rows = con.execute("""
            SELECT w.market, w.metric_name,
                ROUND(SUM(w.actual)) as ytd_actuals,
                ye.predicted as ye_projection
            FROM ps.forecast_tracker w
            JOIN ps.forecast_tracker ye
                ON w.market = ye.market AND w.metric_name = ye.metric_name
            WHERE w.horizon = 'weekly' AND w.actual IS NOT NULL
            AND ye.horizon = 'year_end' AND ye.predicted IS NOT NULL
            GROUP BY w.market, w.metric_name, ye.predicted
            HAVING SUM(w.actual) > ye.predicted
        """).fetchall()
        for r in rows:
            msg = f"  ⚠ {r[0]} year-end {r[1]}: projection ({r[3]:,.0f}) is less than YTD actuals ({r[2]:,.0f})"
            warnings.append(msg)
            print(msg)
    except Exception as e:
        print(f"  Check 2 error: {e}")

    # 3. Weekly predictions for weeks that have actuals should be close to those actuals.
    #    A prediction that's off by more than 50% from the actual for a completed week
    #    suggests the model didn't incorporate the data properly.
    try:
        rows = con.execute("""
            SELECT market, period_label, metric_name, predicted, actual,
                ROUND(ABS(actual - predicted) / NULLIF(predicted, 0) * 100, 1) as abs_err_pct
            FROM ps.forecast_tracker
            WHERE horizon = 'weekly' AND actual IS NOT NULL AND predicted IS NOT NULL
            AND ABS(actual - predicted) / NULLIF(predicted, 0) > 0.5
            AND metric_name = 'registrations'
            ORDER BY ABS(actual - predicted) / NULLIF(predicted, 0) DESC
            LIMIT 10
        """).fetchall()
        if rows:
            print(f"  ℹ {len(rows)} weekly predictions are >50% off from actuals (top misses):")
            for r in rows:
                print(f"    {r[0]} {r[1]}: predicted {r[3]:,.0f}, actual {r[4]:,.0f} ({r[5]:+.0f}%)")
    except Exception as e:
        print(f"  Check 3 error: {e}")

    # 4. Monthly projections should add up to quarterly projections.
    #    If Jan+Feb+Mar projections sum to 30K but Q1 says 25K, something broke
    #    in the derivation chain.
    try:
        QM = {'Q1':['Jan','Feb','Mar'],'Q2':['Apr','May','Jun'],'Q3':['Jul','Aug','Sep'],'Q4':['Oct','Nov','Dec']}
        for ql, mos in QM.items():
            mo_labels = ",".join(f"'{m}'" for m in mos)
            rows = con.execute(f"""
                SELECT m.market, m.metric_name,
                    ROUND(SUM(m.predicted)) as mo_sum,
                    q.predicted as q_pred
                FROM ps.forecast_tracker m
                JOIN ps.forecast_tracker q
                    ON m.market = q.market AND m.metric_name = q.metric_name
                WHERE m.horizon = 'monthly' AND m.period_label IN ({mo_labels}) AND m.predicted IS NOT NULL
                AND q.horizon = 'quarterly' AND q.period_label = '{ql}' AND q.predicted IS NOT NULL
                GROUP BY m.market, m.metric_name, q.predicted
                HAVING ABS(SUM(m.predicted) - q.predicted) > 5
            """).fetchall()
            for r in rows:
                msg = f"  ⚠ {r[0]} {ql} {r[1]}: monthly sum ({r[2]:,.0f}) ≠ quarterly ({r[3]:,.0f})"
                warnings.append(msg)
                print(msg)
    except Exception as e:
        print(f"  Check 4 error: {e}")

    # 5. Aggregate markets (WW, EU5) should equal the sum of their components.
    #    If US+UK+...+AU year-end regs sum to 800K but WW says 750K, the
    #    aggregation step didn't run or ran in the wrong order.
    try:
        for agg, srcs in [('WW', ALL_MARKETS), ('EU5', ['UK','DE','FR','IT','ES'])]:
            sl = ",".join(f"'{m}'" for m in srcs)
            rows = con.execute(f"""
                SELECT a.metric_name, a.horizon,
                    a.predicted as agg_pred,
                    ROUND(SUM(c.predicted)) as component_sum
                FROM ps.forecast_tracker a
                JOIN ps.forecast_tracker c
                    ON a.metric_name = c.metric_name AND a.horizon = c.horizon AND a.period_label = c.period_label
                WHERE a.market = '{agg}' AND c.market IN ({sl})
                AND a.predicted IS NOT NULL AND c.predicted IS NOT NULL
                AND a.horizon = 'year_end'
                GROUP BY a.metric_name, a.horizon, a.predicted
                HAVING ABS(SUM(c.predicted) - a.predicted) > 10
            """).fetchall()
            for r in rows:
                msg = f"  ⚠ {agg} {r[1]} {r[0]}: aggregate ({r[2]:,.0f}) ≠ component sum ({r[3]:,.0f})"
                warnings.append(msg)
                print(msg)
    except Exception as e:
        print(f"  Check 5 error: {e}")

    if not warnings:
        print("  ✓ All checks passed")
    else:
        print(f"\n  {len(warnings)} warning(s) found — review before publishing")

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
