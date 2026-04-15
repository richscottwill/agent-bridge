#!/usr/bin/env python3
"""
Refresh forecast-data.json from ps-forecast-tracker.xlsx on SharePoint.

Usage:
  1. Drop updated xlsx into shared/dashboards/ (or let this script pull from SharePoint)
  2. Run: python3 refresh-forecast.py
  3. Dashboard at localhost:8080/forecast-tracker.html auto-loads fresh data.

Source: OneDrive > Kiro-Drive/ps-forecast-tracker.xlsx (_Data sheet)
"""
import json, os, sys
from datetime import datetime, timezone

try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl not installed. Run: pip install openpyxl")
    sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "ps-forecast-tracker.xlsx")
JSON_PATH = os.path.join(SCRIPT_DIR, "data", "forecast-data.json")

# Also check /tmp in case SharePoint MCP just downloaded it
FALLBACK_PATH = "/tmp/ps-forecast-tracker.xlsx"

def find_xlsx():
    if os.path.exists(XLSX_PATH):
        return XLSX_PATH
    if os.path.exists(FALLBACK_PATH):
        return FALLBACK_PATH
    print(f"ERROR: Cannot find {XLSX_PATH} or {FALLBACK_PATH}")
    print("Download from SharePoint first, or copy the file to shared/dashboards/")
    sys.exit(1)

def main():
    path = find_xlsx()
    print(f"Reading: {path}")
    wb = openpyxl.load_workbook(path, data_only=True)

    if "_Data" not in wb.sheetnames:
        print("ERROR: _Data sheet not found. Available sheets:", wb.sheetnames)
        sys.exit(1)

    ws = wb["_Data"]
    # Parse header row
    headers = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
    col = {h: i for i, h in enumerate(headers)}

    required = ["Market", "Week", "Wk#", "Actual_Regs", "Actual_Cost", "Actual_CPA"]
    for r in required:
        if r not in col:
            print(f"ERROR: Missing column '{r}'. Found: {headers}")
            sys.exit(1)

    # Parse all data rows into weekly, monthly, quarterly buckets
    weekly = {}
    monthly = {}
    quarterly = {}
    markets_set = set()
    max_wk = 0

    MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    QUARTERS = ['Q1','Q2','Q3','Q4']

    for row in ws.iter_rows(min_row=2, values_only=True):
        market = row[col["Market"]]
        if not market:
            continue

        wk_raw = row[col["Wk#"]]
        week_label = str(row[col["Week"]] or "")
        regs = row[col["Actual_Regs"]]
        cost = row[col["Actual_Cost"]]
        cpa = row[col["Actual_CPA"]]

        # Skip header-like rows
        if regs is not None and isinstance(regs, str) and not regs.replace('.','').replace('-','').isdigit():
            continue

        # Check for prediction data
        pred_regs_val = row[col.get("Pred_Regs", -1)] if "Pred_Regs" in col else None
        ci_lo_val = row[col.get("CI_Lo", -1)] if "CI_Lo" in col else None
        op2_val = row[col.get("OP2_Regs", -1)] if "OP2_Regs" in col else None

        # Skip rows with no actuals AND no predictions
        has_actuals = regs is not None or cost is not None
        has_predictions = pred_regs_val is not None or op2_val is not None
        if not has_actuals and not has_predictions:
            continue

        markets_set.add(market)

        def safe_int(v):
            try: return int(v) if v is not None else None
            except (ValueError, TypeError): return None

        def safe_float(v):
            try: return round(float(v), 2) if v is not None else None
            except (ValueError, TypeError): return None

        # Route to monthly bucket
        if week_label in MONTHS:
            if market not in monthly:
                monthly[market] = []
            monthly[market].append({
                "period": week_label,
                "actual_regs": safe_int(regs),
                "actual_cost": safe_float(cost),
                "actual_cpa": safe_float(cpa),
                "pred_regs": safe_int(pred_regs_val),
                "ci_lo": safe_int(ci_lo_val),
            })
            continue

        # Route to quarterly bucket
        if week_label in QUARTERS:
            if market not in quarterly:
                quarterly[market] = []
            quarterly[market].append({
                "period": week_label,
                "actual_regs": safe_int(regs),
                "actual_cost": safe_float(cost),
                "actual_cpa": safe_float(cpa),
                "pred_regs": safe_int(pred_regs_val),
                "ci_lo": safe_int(ci_lo_val),
            })
            continue

        # Skip other summary rows (YTD, Total, etc.)
        if week_label and any(x in week_label for x in ['YTD','Total']):
            continue

        try:
            wk = int(wk_raw) if wk_raw is not None else 0
        except (ValueError, TypeError):
            wk = 0

        # Skip summary/total rows (Excel date serials or wk > 52)
        if wk > 52 or wk < 1:
            continue

        if wk > max_wk and (regs is not None or cost is not None):
            max_wk = wk

        if market not in weekly:
            weekly[market] = []

        entry = {
            "wk": wk,
            "week": f"2026 {week_label}" if week_label and not week_label.startswith("2026") else (week_label or f"W{wk}"),
            "regs": safe_int(regs) or 0,
            "cost": round(float(cost), 0) if cost else 0,
            "cpa": safe_float(cpa) or 0,
        }

        # Add prediction data if available
        pred_regs = row[col.get("Pred_Regs", -1)] if "Pred_Regs" in col else None
        ci_lo = row[col.get("CI_Lo", -1)] if "CI_Lo" in col else None
        ci_hi = row[col.get("CI_Hi", -1)] if "CI_Hi" in col else None
        op2 = row[col.get("OP2_Regs", -1)] if "OP2_Regs" in col else None
        brand = row[col.get("Brand_Regs", -1)] if "Brand_Regs" in col else None
        nb = row[col.get("NB_Regs", -1)] if "NB_Regs" in col else None

        if pred_regs is not None:
            entry["pred_regs"] = int(pred_regs)
        if ci_lo is not None:
            entry["ci_lo"] = int(ci_lo)
        if ci_hi is not None:
            entry["ci_hi"] = int(ci_hi)
        if op2 is not None:
            entry["op2_regs"] = int(op2)
        if brand is not None:
            entry["brand_regs"] = int(brand)
        if nb is not None:
            entry["nb_regs"] = int(nb)

        weekly[market].append(entry)

    # Sort each market by week number
    for m in weekly:
        weekly[m].sort(key=lambda x: x["wk"])

    # Note: TY click enrichment happens after _Daily_Data loading below

    # Derive predicted spend/CPA for future weeks using trailing 4-week avg CPA
    for m in weekly:
        rows = weekly[m]
        # Collect actual CPAs for trailing average
        actual_cpas = [r["cpa"] for r in rows if r["cpa"] > 0 and r["regs"] > 0]
        if not actual_cpas:
            continue
        # Use last 4 weeks' CPA as baseline for predictions
        trailing_cpa = round(sum(actual_cpas[-4:]) / len(actual_cpas[-4:]), 2)

        for r in rows:
            has_actual = r["regs"] > 0 or r["cost"] > 0
            pred_regs = r.get("pred_regs")
            op2_regs = r.get("op2_regs")

            if not has_actual and pred_regs:
                r["pred_cost"] = round(pred_regs * trailing_cpa, 0)
                r["pred_cpa"] = trailing_cpa
            if op2_regs:
                r["op2_cost"] = round(op2_regs * trailing_cpa, 0)
                r["op2_cpa"] = trailing_cpa

        # Store trailing CPA for reference
        weekly[m] = rows  # already sorted

    markets = sorted(markets_set)

    # Week-to-month mapping (approximate: W1-4=Jan, W5-8=Feb, W9-13=Mar, W14-17=Apr, etc.)
    # More precise: use week_start dates if available, else approximate
    WEEK_TO_MONTH = {}
    for w in range(1, 53):
        if w <= 4: WEEK_TO_MONTH[w] = 'Jan'
        elif w <= 8: WEEK_TO_MONTH[w] = 'Feb'
        elif w <= 13: WEEK_TO_MONTH[w] = 'Mar'
        elif w <= 17: WEEK_TO_MONTH[w] = 'Apr'
        elif w <= 21: WEEK_TO_MONTH[w] = 'May'
        elif w <= 26: WEEK_TO_MONTH[w] = 'Jun'
        elif w <= 30: WEEK_TO_MONTH[w] = 'Jul'
        elif w <= 34: WEEK_TO_MONTH[w] = 'Aug'
        elif w <= 39: WEEK_TO_MONTH[w] = 'Sep'
        elif w <= 43: WEEK_TO_MONTH[w] = 'Oct'
        elif w <= 47: WEEK_TO_MONTH[w] = 'Nov'
        else: WEEK_TO_MONTH[w] = 'Dec'

    MONTH_TO_Q = {'Jan':'Q1','Feb':'Q1','Mar':'Q1','Apr':'Q2','May':'Q2','Jun':'Q2',
                  'Jul':'Q3','Aug':'Q3','Sep':'Q3','Oct':'Q4','Nov':'Q4','Dec':'Q4'}

    # Enrich monthly/quarterly with cost+CPA aggregated from weekly data
    for m in markets:
        weeks = weekly.get(m, [])
        # Aggregate weekly cost by month
        month_cost = {}
        month_regs_actual = {}
        for w in weeks:
            mo = WEEK_TO_MONTH.get(w['wk'])
            if not mo:
                continue
            if mo not in month_cost:
                month_cost[mo] = 0
                month_regs_actual[mo] = 0
            if w['cost'] > 0:
                month_cost[mo] += w['cost']
            if w['regs'] > 0:
                month_regs_actual[mo] += w['regs']

        # Update monthly entries with aggregated cost/CPA
        for entry in monthly.get(m, []):
            mo = entry['period']
            if mo in month_cost and month_cost[mo] > 0:
                entry['actual_cost'] = round(month_cost[mo], 0)
                if month_regs_actual.get(mo, 0) > 0:
                    entry['actual_cpa'] = round(month_cost[mo] / month_regs_actual[mo], 2)
                else:
                    entry['actual_cpa'] = None
            else:
                entry['actual_cost'] = None
                entry['actual_cpa'] = None

        # Aggregate quarterly cost from monthly
        for entry in quarterly.get(m, []):
            q = entry['period']
            q_months = [mo for mo, qq in MONTH_TO_Q.items() if qq == q]
            q_cost = sum(month_cost.get(mo, 0) for mo in q_months)
            q_regs = sum(month_regs_actual.get(mo, 0) for mo in q_months)
            if q_cost > 0:
                entry['actual_cost'] = round(q_cost, 0)
                entry['actual_cpa'] = round(q_cost / q_regs, 2) if q_regs > 0 else None
            else:
                entry['actual_cost'] = None
                entry['actual_cpa'] = None

    # Build year-end projections by summing monthly predictions
    yearly = {}
    for m in markets:
        m_months = monthly.get(m, [])
        m_weeks = weekly.get(m, [])
        if m_months:
            total_actual = sum(r["actual_regs"] or 0 for r in m_months if r["actual_regs"])
            total_pred = sum(r["pred_regs"] or 0 for r in m_months if r["pred_regs"])
            total_cost = sum(r["actual_cost"] or 0 for r in m_months if r["actual_cost"])
            yearly[m] = {
                "actual_regs_ytd": total_actual,
                "pred_regs_annual": total_pred,
                "actual_cost_ytd": round(total_cost, 0) if total_cost else None,
                "actual_cpa_ytd": round(total_cost / total_actual, 2) if total_actual and total_cost else None,
                "months_with_actuals": sum(1 for r in m_months if r["actual_regs"]),
            }

    # Determine last data date from the highest week with actuals
    # W15 of 2026 starts 2026-04-07, ends 2026-04-13
    # Approximate: week_start = 2025-12-29 + (wk-1)*7, week_end = week_start + 6
    from datetime import timedelta
    w1_start = datetime(2025, 12, 29)  # 2026 W1 starts Dec 29 2025
    last_data_end = w1_start + timedelta(days=(max_wk - 1) * 7 + 6)
    last_data_date = last_data_end.strftime("%Y-%m-%d")

    # ── Load daily data from _Daily_Data sheet (2025+2026) ──
    ly_weekly = {}
    daily_agg = {}
    if "_Daily_Data" in wb.sheetnames:
        ws_dd = wb["_Daily_Data"]
        dd_headers = [c.value for c in next(ws_dd.iter_rows(min_row=1, max_row=1))]
        dd_col = {h: i for i, h in enumerate(dd_headers)}
        from collections import defaultdict
        daily_agg = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        for row in ws_dd.iter_rows(min_row=2, values_only=True):
            m = row[dd_col.get("Market", 0)]
            yr = row[dd_col.get("Year", 2)]
            wk = row[dd_col.get("Week", 4)]
            channel = row[dd_col.get("Channel", 6)]
            if not m or not wk: continue
            try: wk = int(wk)
            except: continue
            yr_val = None
            try: yr_val = int(yr)
            except: continue
            ch = str(channel or "Total").strip()
            for field in ["Cost","Clicks","Impressions","Regs"]:
                idx = dd_col.get(field)
                if idx is not None and row[idx] is not None:
                    try:
                        val = float(row[idx])
                        if yr_val == 2025:
                            if ch == "Total":
                                daily_agg[m][wk][field.lower()] += val
                            elif ch == "Brand":
                                daily_agg[m][wk]["brand_" + field.lower()] += val
                            elif ch == "Non-Brand":
                                daily_agg[m][wk]["nb_" + field.lower()] += val
                        elif yr_val == 2026:
                            # Store TY clicks for enriching weekly data
                            if field == "Clicks":
                                if ch == "Brand":
                                    daily_agg[m].setdefault(-wk, {})["ty_brand_clicks"] = daily_agg[m].get(-wk, {}).get("ty_brand_clicks", 0) + val
                                elif ch == "Non-Brand":
                                    daily_agg[m].setdefault(-wk, {})["ty_nb_clicks"] = daily_agg[m].get(-wk, {}).get("ty_nb_clicks", 0) + val
                    except: pass
        for m in daily_agg:
            ly_weekly[m] = []
            for wk in sorted(daily_agg[m].keys()):
                d = daily_agg[m][wk]
                regs = d.get("regs", 0)
                cost = d.get("cost", 0)
                ly_weekly[m].append({
                    "wk": wk,
                    "regs": int(regs) if regs else 0,
                    "cost": round(cost, 0) if cost else 0,
                    "cpa": round(cost / regs, 2) if regs > 0 else 0,
                    "clicks": int(d.get("clicks", 0)),
                    "brand_regs": int(d.get("brand_regs", 0)),
                    "nb_regs": int(d.get("nb_regs", 0)),
                    "brand_cost": round(d.get("brand_cost", 0), 0),
                    "nb_cost": round(d.get("nb_cost", 0), 0),
                    "brand_clicks": int(d.get("brand_clicks", 0)),
                    "nb_clicks": int(d.get("nb_clicks", 0)),
                    "brand_cpa": round(d.get("brand_cost", 0) / d.get("brand_regs", 1), 2) if d.get("brand_regs", 0) > 0 else 0,
                    "nb_cpa": round(d.get("nb_cost", 0) / d.get("nb_regs", 1), 2) if d.get("nb_regs", 0) > 0 else 0,
                })
        print(f"LY data: {len(ly_weekly)} markets, {sum(len(v) for v in ly_weekly.values())} weekly rows")
    elif "_LY_Data" in wb.sheetnames:
        # Backward compat with old sheet name
        ws_ly = wb["_LY_Data"]
        ly_headers = [c.value for c in next(ws_ly.iter_rows(min_row=1, max_row=1))]
        ly_col = {h: i for i, h in enumerate(ly_headers)}
        from collections import defaultdict
        ly_daily = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        for row in ws_ly.iter_rows(min_row=2, values_only=True):
            m = row[ly_col.get("Market", 0)]
            wk = row[ly_col.get("Week", 2)]
            if not m or not wk: continue
            try: wk = int(wk)
            except: continue
            for field in ["Cost","Clicks","Impressions","Regs","Brand_Cost","Brand_Clicks","Brand_Imp","Brand_Regs","NB_Cost","NB_Clicks","NB_Imp","NB_Regs"]:
                idx = ly_col.get(field)
                if idx is not None and row[idx] is not None:
                    try: ly_daily[m][wk][field.lower()] += float(row[idx])
                    except: pass
        for m in ly_daily:
            ly_weekly[m] = []
            for wk in sorted(ly_daily[m].keys()):
                d = ly_daily[m][wk]
                regs = d.get("regs", 0)
                cost = d.get("cost", 0)
                ly_weekly[m].append({
                    "wk": wk, "regs": int(regs), "cost": round(cost, 0),
                    "cpa": round(cost / regs, 2) if regs > 0 else 0,
                    "brand_regs": int(d.get("brand_regs", 0)), "nb_regs": int(d.get("nb_regs", 0)),
                    "brand_cost": round(d.get("brand_cost", 0), 0), "nb_cost": round(d.get("nb_cost", 0), 0),
                    "brand_clicks": int(d.get("brand_clicks", 0)), "nb_clicks": int(d.get("nb_clicks", 0)),
                    "brand_cpa": round(d.get("brand_cost", 0) / d.get("brand_regs", 1), 2) if d.get("brand_regs", 0) > 0 else 0,
                    "nb_cpa": round(d.get("nb_cost", 0) / d.get("nb_regs", 1), 2) if d.get("nb_regs", 0) > 0 else 0,
                })
        print(f"LY data (legacy): {len(ly_weekly)} markets, {sum(len(v) for v in ly_weekly.values())} weekly rows")
    else:
        print("No _Daily_Data or _LY_Data sheet — run extract-ly-data.py first")

    # Enrich weekly entries with TY click data from _Daily_Data
    if daily_agg:
        for m in weekly:
            for entry in weekly[m]:
                wk_num = entry["wk"]
                ty_data = daily_agg.get(m, {}).get(-wk_num, {})
                if ty_data.get("ty_brand_clicks"):
                    entry["brand_clicks"] = int(ty_data["ty_brand_clicks"])
                if ty_data.get("ty_nb_clicks"):
                    entry["nb_clicks"] = int(ty_data["ty_nb_clicks"])

    output = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_data_date": last_data_date,
        "source": "ps-forecast-tracker.xlsx (SharePoint)",
        "max_week": max_wk,
        "weekly": weekly,
        "ly_weekly": ly_weekly,
        "monthly": monthly,
        "quarterly": quarterly,
        "yearly": yearly,
        "markets": markets,
    }

    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    with open(JSON_PATH, "w") as f:
        json.dump(output, f, indent=2)

    total_rows = sum(len(v) for v in weekly.values())
    total_monthly = sum(len(v) for v in monthly.values())
    total_quarterly = sum(len(v) for v in quarterly.values())
    print(f"Done: {len(markets)} markets, {total_rows} weekly + {total_monthly} monthly + {total_quarterly} quarterly rows, through W{max_wk}")
    print(f"Written: {JSON_PATH}")

if __name__ == "__main__":
    main()
