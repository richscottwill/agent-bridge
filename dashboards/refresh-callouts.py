#!/usr/bin/env python3
"""
refresh-callouts.py — Build callout-data.json for the WBR Callout Dashboard.

Data sources (in priority order):
  1. forecast-data.json — canonical weekly metrics (regs, spend, CPA, brand, NB)
  2. shared/wiki/callouts/ — written callouts (narrative, context, analysis, change logs)
  3. shared/context/active/callouts/ — generated data briefs (Brand/NB detail, ie%CCP, YoY, anomalies)
  4. shared/context/active/callouts/projections-w*.md — Bayesian projections
  5. shared/context/active/callouts/ww-summary-*.md + shared/wiki/callouts/ww/ — WW summaries

Output: shared/dashboards/data/callout-data.json
"""
import json, os, re
from pathlib import Path
from datetime import datetime, timezone

HOME = Path.home()
FORECAST_JSON = HOME / "shared/dashboards/data/forecast-data.json"
WIKI_DIR = HOME / "shared/wiki/callouts"
ACTIVE_DIR = HOME / "shared/context/active/callouts"
OUTPUT = HOME / "shared/dashboards/data/callout-data.json"
MARKETS = ["US", "CA", "UK", "DE", "FR", "IT", "ES", "JP", "AU", "MX"]
# Derived aggregates (computed in refresh-forecast.py). Now first-class markets:
# they live in forecast['weekly'][...] and forecast['ly_weekly'][...] so build_entry
# reads them the same way as raw markets. No separate aggregation path needed here.
DERIVED_MARKETS = ["WW", "EU5"]
ALL_BUILD_MARKETS = MARKETS + DERIVED_MARKETS
# Display order (the order users see tabs). WW and EU5 appear; individual EU5
# member markets (UK/DE/FR/IT/ES) are rolled up into EU5 and not shown separately.
DISPLAY_MARKETS = ["WW", "US", "EU5", "JP", "CA", "MX", "AU"]

STAKEHOLDERS = {
    "US": {"owner": "Stacey Gu (L6)", "manager": "Brandon Munday (L7)"},
    "CA": {"owner": "Adi (L5)", "manager": "Brandon Munday (L7)"},
    "UK": {"owner": "Andrew Wirtz (L5)", "manager": "Brandon Munday (L7)"},
    "DE": {"owner": "Andrew Wirtz (L5)", "manager": "Brandon Munday (L7)"},
    "FR": {"owner": "Andrew Wirtz (L5)", "manager": "Brandon Munday (L7)"},
    "IT": {"owner": "Andrew Wirtz (L5)", "manager": "Brandon Munday (L7)"},
    "ES": {"owner": "Andrew Wirtz (L5)", "manager": "Brandon Munday (L7)"},
    "JP": {"owner": "Adi (L5)", "manager": "Brandon Munday (L7)"},
    "AU": {"owner": "Richard Williams", "primary": "Lena Zak (L7)", "partner": "Alexis Eck (L6)", "manager": "Brandon Munday (L7)"},
    "MX": {"owner": "Richard Williams", "primary": "Lorena Alvarez Larrea (L5)", "support": "Yun-Kang Chu (L6)", "manager": "Brandon Munday (L7)"},
    "WW": {"owner": "Brandon Munday (L7)", "manager": "Kate Rundell (L8)"},
    "EU5": {"owner": "Andrew Wirtz (L5)", "primary": "Yun-Kang Chu (L6)", "manager": "Brandon Munday (L7)"},
}

def pn(s):
    """Parse number from string."""
    if not s or str(s).strip() in ("", "—", "N/A"): return None
    s = str(s).strip().replace(",", "").replace("$", "").replace("%", "")
    m = re.match(r"([+-]?\d+\.?\d*)[Kk]", s)
    if m: return float(m.group(1)) * 1000
    m = re.match(r"([+-]?\d+\.?\d*)[Mm]", s)
    if m: return float(m.group(1)) * 1000000
    try: return float(s)
    except: return None

# ── Forecast data loader ──────────────────────────────────────────────
def load_forecast():
    """Load forecast-data.json as the canonical metrics source."""
    if not FORECAST_JSON.exists():
        print(f"WARNING: {FORECAST_JSON} not found — metrics will come from callout files only")
        return {}
    return json.loads(FORECAST_JSON.read_text())

def get_ly_metrics(forecast, market, wk):
    """Get last year's weekly metrics for YoY computation."""
    rows = forecast.get("ly_weekly", {}).get(market, [])
    for r in rows:
        if r.get("wk") == wk:
            return r
    return None

def get_trailing_avg(forecast, market, wk, lookback=4):
    """Get trailing N-week average metrics (excluding current week)."""
    rows = forecast.get("weekly", {}).get(market, [])
    trailing = [r for r in rows if wk - lookback <= r.get("wk", 0) < wk and (r.get("regs", 0) > 0 or r.get("cost", 0) > 0)]
    if not trailing:
        return None
    n = len(trailing)
    avg = {
        "regs": sum(r.get("regs", 0) for r in trailing) / n,
        "cost": sum(r.get("cost", 0) for r in trailing) / n,
        "brand_regs": sum(r.get("brand_regs", 0) or 0 for r in trailing) / n,
        "nb_regs": sum(r.get("nb_regs", 0) or 0 for r in trailing) / n,
        "brand_clicks": sum(r.get("brand_clicks", 0) or 0 for r in trailing) / n,
        "nb_clicks": sum(r.get("nb_clicks", 0) or 0 for r in trailing) / n,
    }
    if avg["regs"] > 0:
        avg["cpa"] = avg["cost"] / avg["regs"]
    return avg

def get_weekly_metrics(forecast, market, wk):
    """Get a week's metrics from forecast data."""
    rows = forecast.get("weekly", {}).get(market, [])
    for r in rows:
        if r.get("wk") == wk:
            return r
    return None

def get_full_chart_data(forecast, market):
    """Get W1-W52 chart data: actuals, predictions, CI, OP2, spend."""
    rows = forecast.get("weekly", {}).get(market, [])
    max_wk = forecast.get("max_week", 15)
    chart = []
    for r in sorted(rows, key=lambda x: x.get("wk", 0)):
        wk = r.get("wk", 0)
        if wk < 1 or wk > 52: continue
        is_actual = r.get("regs", 0) > 0 or r.get("cost", 0) > 0
        chart.append({
            "wk": wk,
            "regs": r.get("regs") if is_actual else None,
            "spend": r.get("cost") if is_actual else None,
            "pred_regs": r.get("pred_regs"),
            "pred_spend": r.get("pred_cost"),
            "ci_lo": r.get("ci_lo"),
            "ci_hi": r.get("ci_hi"),
            "op2_regs": r.get("op2_regs"),
        })
    return chart

def get_weekly_trend(forecast, market, through_wk, lookback=8):
    """Get trailing N weeks of regs (backward compat)."""
    rows = forecast.get("weekly", {}).get(market, [])
    return {f"W{r['wk']}": r.get("regs", 0) for r in rows
            if through_wk - lookback < r.get("wk", 0) <= through_wk and (r.get("regs", 0) > 0 or r.get("cost", 0) > 0)}

def get_spend_trend(forecast, market, through_wk, lookback=8):
    """Get trailing N weeks of spend (backward compat)."""
    rows = forecast.get("weekly", {}).get(market, [])
    return {f"W{r['wk']}": r.get("cost", 0) for r in rows
            if through_wk - lookback < r.get("wk", 0) <= through_wk and r.get("cost", 0) > 0}

# ── Callout file parsers ──────────────────────────────────────────────
def find_file(market, filename):
    """Find a file in active or wiki callout dirs. Prefer active (newer)."""
    mk = market.lower()
    for base in [ACTIVE_DIR, WIKI_DIR]:
        f = base / mk / filename
        if f.exists(): return f
    return None

def find_ww_file(filename):
    """Find a WW-level file."""
    for path in [ACTIVE_DIR / filename, WIKI_DIR / "ww" / filename]:
        if path.exists(): return path
    return None

def read_callout(market, wk):
    """Read the callout markdown and extract headline + full body paragraphs."""
    mk = market.lower()
    f = find_file(market, f"{mk}-2026-w{wk}.md")
    # For WW, also accept the legacy 'ww-review-2026-wN.md' filename
    if not f and market == "WW":
        f = find_file("WW", f"ww-review-2026-w{wk}.md")
    if not f: return None
    text = f.read_text()
    result = {}

    # Period from header
    m = re.search(r"#\s+\w+\s+.+?W\d+\s+\((.+?)\)", text)
    result["period"] = m.group(1).strip() if m else ""

    # Collect body paragraphs (skip frontmatter, header)
    lines = text.strip().split("\n")
    body = []
    in_fm = False
    past_header = False
    for line in lines:
        if line.strip() == "---":
            in_fm = not in_fm; continue
        if in_fm: continue
        if line.startswith("#"):
            past_header = True; continue
        if line.startswith("<!--"): continue
        if past_header and line.strip():
            body.append(line.strip())
    result["body_paragraphs"] = body

    # Headline = first paragraph
    headline = []
    for line in body:
        if not line: break
        headline.append(line)
    result["headline"] = " ".join(headline) if headline else ""

    # Weekly trend line
    tm = re.search(r"Weekly trend \(regs\):\s*(.+)", text)
    if tm:
        trend = {}
        for pair in tm.group(1).split("|"):
            pm = re.match(r"\s*(W\d+):\s*([\d,.]+[KkMm]?)", pair.strip())
            if pm: trend[pm.group(1)] = pn(pm.group(2))
        result["callout_trend"] = trend

    # Flagged anomalies
    anomalies = []
    for line in lines:
        am = re.match(r"-\s+(.+?)\s+(above|below)\s+recent avg by\s+(\d+)%", line)
        if am:
            metric, direction, pct = am.group(1).strip(), am.group(2), int(am.group(3))
            good_up = ("regs","brand regs","nb regs","cvr","brand cvr","nb cvr")
            bad_up = ("cpa","cpc","nb cpa","cost")
            flag = "good" if (direction=="above" and metric in good_up) or (direction=="below" and metric in bad_up) else \
                   "bad" if (direction=="below" and metric in good_up) or (direction=="above" and metric in bad_up) else "warn"
            anomalies.append({"metric":metric.title(),"deviation":f"{'+'if direction=='above'else'-'}{pct}%","flag":flag,"category":"brand" if "brand" in metric else ("nb" if "nb" in metric else "overall")})
    result["anomalies"] = anomalies

    # Daily
    dm = re.search(r"Daily:\s*(.+)", text)
    result["daily_raw"] = dm.group(1).strip() if dm else ""

    # Notes
    result["notes"] = [l.strip() for l in lines if l.strip().startswith("Note:")]

    # Extract context from all body paragraphs (everything after headline)
    result["context_paragraphs"] = body[len(headline):] if len(body) > len(headline) else []

    return result

def read_data_brief(market, wk):
    """Read data brief for Brand/NB detail, ie%CCP, YoY, anomalies."""
    mk = market.lower()
    f = find_file(market, f"{mk}-data-brief-2026-w{wk}.md")
    if not f: return {}
    text = f.read_text()
    result = {}

    # ie%CCP
    ie = re.search(r"This week:\s*(\d+)%", text)
    if ie: result["ie_ccp"] = int(ie.group(1))
    ie_lw = re.search(r"Last week:\s*(\d+)%", text)
    if ie_lw: result["ie_ccp_lw"] = int(ie_lw.group(1))

    # Brand/NB detail with WoW
    def parse_channel(name):
        pattern = rf"{name}:\s*\n\s+Regs:\s*(\d+)\s+vs\s+(\d+)\s+LW\s+\(([+-]?\d+)%\)\s*\n\s+CVR:\s*([\d.]+)%\s+vs\s+([\d.]+)%\s+\(([+-]?\d+)%\)\s*\n\s+Clicks:\s*([\d,]+)\s+vs\s+([\d,]+)\s+\(([+-]?\d+)%\)\s*\n\s+CPA:\s*\$([\d.]+)\s+vs\s+\$([\d.]+)\s+\(([+-]?\d+)%\)"
        m = re.search(pattern, text)
        if not m: return None
        return {
            "regs": pn(m.group(1)), "lw_regs": pn(m.group(2)), "regs_wow": float(m.group(3)),
            "cvr": pn(m.group(4)), "lw_cvr": pn(m.group(5)), "cvr_wow": float(m.group(6)),
            "clicks": pn(m.group(7)), "lw_clicks": pn(m.group(8)), "clicks_wow": float(m.group(9)),
            "cpa": pn(m.group(10)), "lw_cpa": pn(m.group(11)), "cpa_wow": float(m.group(12)),
        }
    result["brand_detail"] = parse_channel("Brand")
    result["nb_detail"] = parse_channel("Non-Brand")

    # Primary driver
    drv = re.search(r"Primary driver:\s*(.+)", text)
    if drv: result["primary_driver"] = drv.group(1).strip()

    # YoY
    yoy = {}
    yoy_sec = re.search(r"## YoY comparison\n((?:- .+\n)+)", text)
    if yoy_sec:
        for line in yoy_sec.group(1).strip().split("\n"):
            line = line.strip("- ").strip()
            rm = re.search(r"\(?([+-]?\d+)%\)?", line)
            if "Brand regs" in line and rm: yoy["brand_regs_yoy"] = float(rm.group(1))
            elif "NB regs" in line and rm: yoy["nb_regs_yoy"] = float(rm.group(1))
            elif "NB CPA" in line and rm: yoy["nb_cpa_yoy"] = float(rm.group(1))
            elif line.startswith("Regs:") and rm: yoy["regs_yoy"] = float(rm.group(1))
            elif line.startswith("Spend:") and rm: yoy["spend_yoy"] = float(rm.group(1))
            elif "WoW pattern" in line: yoy["wow_pattern"] = line
        yoy["raw_lines"] = [l.strip("- ").strip() for l in yoy_sec.group(1).strip().split("\n")]
    result["yoy"] = yoy

    # Anomalies with values
    anomalies = []
    anom_sec = re.search(r"## Anomalies.*?\n((?:- .+\n)+)", text)
    if anom_sec:
        for line in anom_sec.group(1).strip().split("\n"):
            am = re.match(r"-\s+(.+?):\s+(above|below)\s+avg by\s+(\d+)%\s+\(current:\s*([\d.]+),\s*avg:\s*([\d.]+)\)", line)
            if am:
                metric, direction, pct = am.group(1).strip(), am.group(2), int(am.group(3))
                good_up = ("regs","brand regs","nb regs","cvr","brand cvr","nb cvr")
                bad_up = ("cpa","cpc","nb cpa","cost")
                flag = "good" if (direction=="above" and metric in good_up) or (direction=="below" and metric in bad_up) else \
                       "bad" if (direction=="below" and metric in good_up) or (direction=="above" and metric in bad_up) else "warn"
                anomalies.append({
                    "metric":metric.title(),
                    "value":am.group(4),
                    "avg_8wk":am.group(5),
                    "deviation":f"{'+'if direction=='above'else'-'}{pct}%",
                    "flag":flag,
                    "category": "brand" if "brand" in metric else ("nb" if "nb" in metric else "overall"),
                })
    result["anomalies"] = anomalies

    # Streaks
    streaks = []
    ss = re.search(r"## Detected streaks\n((?:- .+\n)+)", text)
    if ss:
        streaks = [l.strip("- ").strip() for l in ss.group(1).strip().split("\n")]
    result["streaks"] = streaks

    # Monthly projection
    proj = {}
    mp = re.search(r"Simple linear projection.*?:\s*\$?([\d,.]+[KkMm]?)\s+spend,\s*([\d,.]+[KkMm]?)\s+regs,\s*\$?([\d,.]+)\s+CPA", text)
    if mp:
        proj["proj_spend"] = pn(mp.group(1)); proj["proj_regs"] = pn(mp.group(2)); proj["proj_cpa"] = pn(mp.group(3))
    mo = re.search(r"Month:\s*(\d{4}\s+\w+)", text)
    if mo: proj["month"] = mo.group(1).strip()
    pace = re.search(r"MTD vs OP2 pace:\s*([+-]?\d+)%\s+regs,\s*([+-]?\d+)%\s+spend", text)
    if pace: proj["vs_op2_regs"] = float(pace.group(1)); proj["vs_op2_spend"] = float(pace.group(2))
    mtd = re.search(r"MTD actuals:.*?(\d[\d,.]*[KkMm]?)\s+regs", text)
    if mtd: proj["mtd_regs"] = pn(mtd.group(1))
    op2 = re.search(r"OP2 targets:.*?([\d,.]+[KkMm]?)\s+regs", text)
    if op2: proj["op2_regs"] = pn(op2.group(1))
    result["monthly_proj"] = proj

    return result

def read_ww_summary(wk):
    """Parse WW summary table."""
    f = find_ww_file(f"ww-summary-2026-w{wk}.md")
    if not f: return None
    text = f.read_text()
    result = {}
    # Parse table rows
    for row in re.findall(r"\|\s*(\w+)\s*\|\s*([\d,.]+[KkMm]?)\s*\|\s*([+-]?[\d.]+)%\s*\|\s*\$?([\d,.]+[KkMm]?)\s*\|\s*([+-]?[\d.]+)%\s*\|\s*\$?([\d,.]+)\s*\|\s*([+-]?[\d.]+)%\s*\|\s*([+-]?[\d.]+%|N/A)\s*\|\s*([\d,.]+[KkMm]?)\s*\|\s*([+-]?[\d.]+)%\s*\|", text):
        m = row[0].strip()
        if m in ("Market","**WW**","WW"): continue
        result[m] = {"regs_yoy": pn(row[7].replace("%","")) if row[7]!="N/A" else None, "proj_regs": pn(row[8]), "vs_op2": pn(row[9])}
    # WW totals
    ww = re.search(r"\|\s*\*\*WW\*\*\s*\|\s*\*\*([\d,.]+[KkMm]?)\*\*\s*\|\s*\*\*([+-]?[\d.]+)%\*\*\s*\|\s*\*\*\$?([\d,.]+[KkMm]?)\*\*\s*\|\s*\*\*([+-]?[\d.]+)%\*\*", text)
    if ww: result["_ww"] = {"regs":pn(ww.group(1)),"regs_wow":pn(ww.group(2)),"spend":pn(ww.group(3)),"spend_wow":pn(ww.group(4))}
    # Key callouts
    result["_callouts"] = [l[2:].strip() for l in text.split("\n") if l.startswith("- Biggest")]
    # Anomalies
    anoms = {}
    asec = text.split("## Anomalies")
    if len(asec)>1:
        for line in asec[1].strip().split("\n"):
            am = re.match(r"-\s+(\w+):\s+(.+?)\s+(above|below)\s+recent avg by\s+(\d+)%", line)
            if am:
                mkt = am.group(1)
                if mkt not in anoms: anoms[mkt] = []
                metric, direction, pct = am.group(2).strip(), am.group(3), int(am.group(4))
                good_up = ("regs","brand regs","nb regs","cvr","brand cvr","nb cvr")
                flag = "good" if (direction=="above" and metric.lower() in good_up) or (direction=="below" and metric.lower() in ("cpa","cpc","cost")) else \
                       "bad" if (direction=="below" and metric.lower() in good_up) or (direction=="above" and metric.lower() in ("cpa","cpc","cost")) else "warn"
                anoms[mkt].append({"metric":metric.title(),"deviation":f"{'+'if direction=='above'else'-'}{pct}%","flag":flag})
    result["_anoms"] = anoms
    return result

def read_projections(wk):
    """Parse Bayesian projections file."""
    f = find_ww_file(f"projections-w{wk}.md")
    if not f: return None
    text = f.read_text()
    result = {"next_week":{},"month":{},"quarter":{}}
    sections = {
        "next_week": r"### Projections — Next Week[^\n]*\n+\|[^\n]+\n\|[-| ]+\n((?:\|[^\n]+\n)+)",
        "month": r"### Projections — Current Month[^\n]*\n+\|[^\n]+\n\|[-| ]+\n((?:\|[^\n]+\n)+)",
        "quarter": r"### Projections — Current Quarter[^\n]*\n+\|[^\n]+\n\|[-| ]+\n((?:\|[^\n]+\n)+)",
    }
    for key, pattern in sections.items():
        m = re.search(pattern, text)
        if not m: continue
        for row in m.group(1).strip().split("\n"):
            cols = [c.strip() for c in row.split("|") if c.strip()]
            if len(cols) >= 6:
                market = cols[0]
                rm = re.match(r"([\d,.]+[KkMm]?)\s*\((\d[\d,.]*)/(\d[\d,.]*)\)\s*\[([\d,.]+[KkMm]?)[\u2013–-]([\d,.]+[KkMm]?)\]", cols[1])
                if rm:
                    result[key][market] = {
                        "regs":pn(rm.group(1)),"brand_regs":pn(rm.group(2)),"nb_regs":pn(rm.group(3)),
                        "ci_lo":pn(rm.group(4)),"ci_hi":pn(rm.group(5)),
                        "spend":pn(cols[2].replace("$","")), "cpa":pn(cols[3].replace("$","")),
                        "vs_op2_spend":pn(cols[5].replace("%",""))
                    }
    return result

# ── Prose metric extraction (for narrative-only callouts like W11) ────
def extract_prose_metrics(text):
    """Extract metrics from narrative callout text when no data brief exists."""
    pm = {}
    m = re.search(r"drove\s+([\d,.]+[KkMm]?)\s+registrations?\s+\(([+-]?\d+)%\s*WoW\)", text)
    if m: pm["regs"] = pn(m.group(1)); pm["regs_wow"] = float(m.group(2))
    m = re.search(r"([+-]?\d+)%\s+spend\s+WoW", text)
    if m: pm["spend_wow"] = float(m.group(1))
    m = re.search(r"CPA\s+(?:came in at|decreased to|increased to)\s+\$(\d+)\s+\(([+-]?\d+)%\s*WoW\)", text)
    if m: pm["cpa"] = float(m.group(1)); pm["cpa_wow"] = float(m.group(2))
    m = re.search(r"(\d+)%\s*ie%CCP", text)
    if m: pm["ie_ccp"] = int(m.group(1))
    # Brand/NB WoW from prose: "Brand (+26%) and NB (+48%)"
    m = re.search(r"Brand\s+\(([+-]?\d+)%\)\s+and\s+NB\s+\(([+-]?\d+)%\)", text)
    if m: pm["brand_regs_wow"] = float(m.group(1)); pm["nb_regs_wow"] = float(m.group(2))
    # CVR WoW: "(+29% Brand, +40% NB)"
    m = re.search(r"CVR\s+increases?\s+on\s+both\s+sides\s+\(([+-]?\d+)%\s*Brand,\s*([+-]?\d+)%\s*NB\)", text)
    if m: pm["brand_cvr_wow"] = float(m.group(1)); pm["nb_cvr_wow"] = float(m.group(2))
    # YoY: "spent -21% with +101% registrations"
    m = re.search(r"YoY\s+we\s+spent\s+([+-]?\d+)%\s+with\s+([+-]?\d+)%\s+registrations", text)
    if m: pm["spend_yoy"] = float(m.group(1)); pm["regs_yoy"] = float(m.group(2))
    # NB CPA YoY: "NB CPA improved -47% YoY ($121 vs $228)"
    m = re.search(r"NB CPA\s+improved\s+([+-]?\d+)%\s+YoY\s+\(\$(\d+)\s+vs\s+\$(\d+)\)", text)
    if m: pm["nb_cpa_yoy"] = float(m.group(1)); pm["nb_cpa"] = float(m.group(2))
    # Brand regs YoY from prose
    m = re.search(r"Brand\s+(?:regs|registrations)\s+([+-]?\d+)%\s+YoY", text)
    if m: pm["brand_regs_yoy"] = float(m.group(1))
    # NB regs YoY
    m = re.search(r"([+-]?\d+)%\s+registrations\s+despite", text)
    if m: pm["nb_regs_yoy"] = float(m.group(1))
    return pm

# ── Assembly ──────────────────────────────────────────────────────────
DERIVED_MARKETS_SET = {"WW", "EU5"}

def build_entry(market, wk, forecast, ww_data, proj_data):
    """Build one market+week callout entry."""
    callout = read_callout(market, wk)
    if not callout:
        # For derived markets (WW/EU5), fall back to a quantitative-only skeleton
        # when no narrative callout file exists. We still render the chart + KPIs
        # because forecast['weekly'][market] is populated by refresh-forecast.py.
        if market in DERIVED_MARKETS_SET and get_weekly_metrics(forecast, market, wk):
            callout = {
                "period": f"W{wk}",
                "headline": "",
                "body_paragraphs": [],
                "context_paragraphs": [],
                "anomalies": [],
                "daily_raw": "",
                "notes": [],
                "callout_trend": {},
            }
        else:
            return None
    brief = read_data_brief(market, wk)
    fcast = get_weekly_metrics(forecast, market, wk)

    # ── Metrics: forecast is canonical, brief fills gaps ──
    metrics = {}
    if fcast:
        metrics["regs"] = fcast.get("regs")
        metrics["spend"] = fcast.get("cost")
        metrics["cpa"] = fcast.get("cpa")
        metrics["brand_regs"] = fcast.get("brand_regs")
        metrics["nb_regs"] = fcast.get("nb_regs")
    # WoW/YoY from brief or WW summary
    bm = brief.get("metrics", {}) if brief else {}
    for k in ["regs_wow","spend_wow","cpa_wow","nb_cpa","nb_cvr","ie_ccp","regs_yoy"]:
        if bm.get(k) is not None: metrics[k] = bm[k]
    if brief.get("ie_ccp") is not None: metrics["ie_ccp"] = brief["ie_ccp"]
    if brief.get("yoy",{}).get("regs_yoy") is not None: metrics["regs_yoy"] = brief["yoy"]["regs_yoy"]
    if brief.get("yoy",{}).get("spend_yoy") is not None: metrics["spend_yoy"] = brief["yoy"]["spend_yoy"]
    if brief.get("yoy",{}).get("nb_cpa_yoy") is not None: metrics["cpa_yoy"] = brief["yoy"]["nb_cpa_yoy"]  # overall CPA YoY approximated from NB CPA YoY
    # WW summary YoY fallback
    if ww_data and market in ww_data and metrics.get("regs_yoy") is None:
        yoy = ww_data[market].get("regs_yoy")
        if yoy is not None: metrics["regs_yoy"] = yoy

    # Extract prose metrics (used as a LAST-resort fallback later — after LY math).
    # We compute it here so later brand/nb detail construction can use non-YoY fields
    # (e.g. prose CVR_wow) when forecast-derived values are absent.
    prose = extract_prose_metrics(callout.get("headline","") + " " + " ".join(callout.get("context_paragraphs",[])))

    # ── Brand/NB detail ──
    brand_detail = brief.get("brand_detail") if brief else None
    nb_detail = brief.get("nb_detail") if brief else None
    # Build from forecast + prose if no brief
    if not brand_detail and fcast and fcast.get("brand_regs"):
        brand_detail = {"regs": fcast["brand_regs"]}
        if prose.get("brand_regs_wow") is not None: brand_detail["regs_wow"] = prose["brand_regs_wow"]
        if prose.get("brand_cvr_wow") is not None: brand_detail["cvr_wow"] = prose["brand_cvr_wow"]
    if not nb_detail and fcast and fcast.get("nb_regs"):
        nb_detail = {"regs": fcast["nb_regs"]}
        if prose.get("nb_regs_wow") is not None: nb_detail["regs_wow"] = prose["nb_regs_wow"]
        if prose.get("nb_cvr_wow") is not None: nb_detail["cvr_wow"] = prose["nb_cvr_wow"]
        if prose.get("nb_cpa") is not None: nb_detail["cpa"] = prose["nb_cpa"]

    # Merge YoY into brand/nb detail (from data brief first — authoritative)
    yoy = brief.get("yoy",{}) if brief else {}
    if brand_detail and yoy.get("brand_regs_yoy") is not None: brand_detail["regs_yoy"] = yoy["brand_regs_yoy"]
    if nb_detail and yoy.get("nb_regs_yoy") is not None: nb_detail["regs_yoy"] = yoy["nb_regs_yoy"]
    if nb_detail and yoy.get("nb_cpa_yoy") is not None: nb_detail["cpa_yoy"] = yoy["nb_cpa_yoy"]

    # Compute full YoY from LY forecast data (ground truth — runs BEFORE prose fallback
    # so narrative claims in callout prose can't override the actual LY math).
    ly = get_ly_metrics(forecast, market, wk)
    if ly and fcast:
        def yoy_pct(ty, ly_val):
            if ty and ly_val and ly_val > 0: return round((ty - ly_val) / ly_val * 100, 1)
            return None
        # Overall metrics YoY
        if metrics.get("regs_yoy") is None: metrics["regs_yoy"] = yoy_pct(fcast.get("regs"), ly.get("regs"))
        if metrics.get("spend_yoy") is None: metrics["spend_yoy"] = yoy_pct(fcast.get("cost"), ly.get("cost"))
        if metrics.get("cpa_yoy") is None and fcast.get("cpa") and ly.get("cpa"):
            metrics["cpa_yoy"] = yoy_pct(fcast["cpa"], ly["cpa"])
        # Brand detail YoY
        if brand_detail:
            if brand_detail.get("regs_yoy") is None: brand_detail["regs_yoy"] = yoy_pct(brand_detail.get("regs"), ly.get("brand_regs"))
            if brand_detail.get("cpa_yoy") is None and brand_detail.get("cpa") and ly.get("brand_cpa"):
                brand_detail["cpa_yoy"] = yoy_pct(brand_detail["cpa"], ly["brand_cpa"])
            if brand_detail.get("clicks") and ly.get("brand_clicks"):
                brand_detail["clicks_yoy"] = yoy_pct(brand_detail["clicks"], ly["brand_clicks"])
            # CVR YoY: compute from regs/clicks
            if brand_detail.get("cvr") and ly.get("brand_regs") and ly.get("brand_clicks") and ly["brand_clicks"] > 0:
                ly_brand_cvr = ly["brand_regs"] / ly["brand_clicks"] * 100
                brand_detail["cvr_yoy"] = round((brand_detail["cvr"] - ly_brand_cvr) / ly_brand_cvr * 100, 1)
        # NB detail YoY
        if nb_detail:
            if nb_detail.get("regs_yoy") is None: nb_detail["regs_yoy"] = yoy_pct(nb_detail.get("regs"), ly.get("nb_regs"))
            if nb_detail.get("cpa_yoy") is None and nb_detail.get("cpa") and ly.get("nb_cpa"):
                nb_detail["cpa_yoy"] = yoy_pct(nb_detail["cpa"], ly["nb_cpa"])
            if nb_detail.get("clicks") and ly.get("nb_clicks"):
                nb_detail["clicks_yoy"] = yoy_pct(nb_detail["clicks"], ly["nb_clicks"])
            # CVR YoY
            if nb_detail.get("cvr") and ly.get("nb_regs") and ly.get("nb_clicks") and ly["nb_clicks"] > 0:
                ly_nb_cvr = ly["nb_regs"] / ly["nb_clicks"] * 100
                nb_detail["cvr_yoy"] = round((nb_detail["cvr"] - ly_nb_cvr) / ly_nb_cvr * 100, 1)

    # Prose fallback — ONLY fills gaps that LY data and briefs couldn't answer.
    # (Runs after LY so incorrect narrative claims don't override ground truth.)
    for k,v in prose.items():
        if metrics.get(k) is None and v is not None: metrics[k] = v
    if brand_detail and brand_detail.get("regs_yoy") is None and prose.get("brand_regs_yoy") is not None:
        brand_detail["regs_yoy"] = prose["brand_regs_yoy"]
    if nb_detail and nb_detail.get("regs_yoy") is None and prose.get("nb_regs_yoy") is not None:
        nb_detail["regs_yoy"] = prose["nb_regs_yoy"]
    if nb_detail and nb_detail.get("cpa_yoy") is None and prose.get("nb_cpa_yoy") is not None:
        nb_detail["cpa_yoy"] = prose["nb_cpa_yoy"]

    # ── vs 4-week average + fill remaining WoW/YoY gaps for Cost/CVR/Clicks ──
    avg4 = get_trailing_avg(forecast, market, wk, 4)
    if avg4 and fcast:
        def vsa(ty, avg_val):
            if ty and avg_val and avg_val > 0: return round((ty - avg_val) / avg_val * 100, 1)
            return None
        metrics["regs_vs4wk"] = vsa(fcast.get("regs"), avg4.get("regs"))
        metrics["spend_vs4wk"] = vsa(fcast.get("cost"), avg4.get("cost"))
        if fcast.get("cpa") and avg4.get("cpa"):
            metrics["cpa_vs4wk"] = vsa(fcast["cpa"], avg4["cpa"])

        trailing = [r for r in forecast.get("weekly", {}).get(market, [])
                   if wk - 4 <= r.get("wk", 0) < wk and (r.get("regs", 0) > 0)]
        n = len(trailing) if trailing else 1

        for detail, prefix in [(brand_detail, "brand"), (nb_detail, "nb")]:
            if not detail or not trailing: continue
            avg_ch_regs = sum(r.get(f"{prefix}_regs", 0) or 0 for r in trailing) / n
            avg_ch_cost = sum(r.get("cost", 0) * (r.get(f"{prefix}_regs", 0) or 0) / max(r.get("regs", 1), 1) for r in trailing) / n

            # Regs vs4wk
            detail["regs_vs4wk"] = vsa(detail.get("regs"), avg_ch_regs)
            # CPA vs4wk
            if detail.get("cpa") and avg_ch_regs > 0 and avg_ch_cost > 0:
                detail["cpa_vs4wk"] = vsa(detail["cpa"], avg_ch_cost / avg_ch_regs)
            # Cost: compute TY cost, LW cost, LY cost, avg cost
            ty_cost = detail.get("cpa", 0) * detail.get("regs", 0) if detail.get("cpa") and detail.get("regs") else None
            if ty_cost:
                detail["cost"] = round(ty_cost)
                # Cost WoW
                lw_cost = detail.get("lw_cpa", 0) * detail.get("lw_regs", 0) if detail.get("lw_cpa") and detail.get("lw_regs") else None
                if lw_cost and lw_cost > 0:
                    detail["cost_wow"] = round((ty_cost - lw_cost) / lw_cost * 100, 1)
                # Cost vs4wk
                detail["cost_vs4wk"] = vsa(ty_cost, avg_ch_cost)
            # Cost YoY from LY data
            ly_m = get_ly_metrics(forecast, market, wk)
            if ly_m and ty_cost:
                ly_ch_cost = ly_m.get(f"{prefix}_cost", 0)
                if ly_ch_cost and ly_ch_cost > 0:
                    detail["cost_yoy"] = round((ty_cost - ly_ch_cost) / ly_ch_cost * 100, 1)
            # Clicks vs4wk from trailing click data
            if detail.get("clicks") and avg4.get(f"{prefix}_clicks") and avg4[f"{prefix}_clicks"] > 0:
                detail["clicks_vs4wk"] = vsa(detail["clicks"], avg4[f"{prefix}_clicks"])
            # CVR vs4wk: compute from trailing regs/clicks
            if detail.get("cvr") and avg_ch_regs > 0 and avg4.get(f"{prefix}_clicks") and avg4[f"{prefix}_clicks"] > 0:
                avg_cvr = avg_ch_regs / avg4[f"{prefix}_clicks"] * 100
                detail["cvr_vs4wk"] = round((detail["cvr"] - avg_cvr) / avg_cvr * 100, 1)

    # ── Trends from forecast (canonical) ──
    weekly_trend = get_weekly_trend(forecast, market, wk)
    spend_trend = get_spend_trend(forecast, market, wk)
    chart_data = get_full_chart_data(forecast, market)
    # Fallback to callout trend if forecast empty
    if not weekly_trend and callout.get("callout_trend"):
        weekly_trend = callout["callout_trend"]

    # ── Anomalies: prefer brief (has values), fall back to callout ──
    anomalies = brief.get("anomalies",[]) if brief else []
    if not anomalies: anomalies = callout.get("anomalies",[])
    if not anomalies and ww_data: anomalies = ww_data.get("_anoms",{}).get(market,[])

    # ── External factors / context ──
    external = []
    for n in callout.get("notes",[]):
        external.append({"text": n.replace("Note: ",""), "important": True})
    if callout.get("daily_raw"):
        external.append({"text": "Daily: " + callout["daily_raw"], "important": False})
    if brief and brief.get("streaks"):
        for s in brief["streaks"]: external.append({"text": s, "important": True})
    if metrics.get("ie_ccp") and metrics["ie_ccp"] > 100:
        external.append({"text": f"ie%CCP at {metrics['ie_ccp']}% — above 100% target", "important": True})
    if brief and brief.get("primary_driver"):
        external.append({"text": "Primary driver: " + brief["primary_driver"], "important": False})
    if yoy.get("wow_pattern"):
        external.append({"text": yoy["wow_pattern"], "important": False})
    # Context paragraphs from the callout (everything after headline)
    for para in callout.get("context_paragraphs",[]):
        if para not in [e.get("text","") for e in external]:
            external.append({"text": para, "important": False})

    # ── Decisions / drivers ──
    decisions = []
    if brief and brief.get("primary_driver"):
        decisions.append("Primary driver: " + brief["primary_driver"])
    if brand_detail and brand_detail.get("regs") and brand_detail.get("cpa"):
        decisions.append(f"Brand: {int(brand_detail['regs'])} regs, CPA ${brand_detail['cpa']:.0f}")
    if nb_detail and nb_detail.get("regs") and nb_detail.get("cpa"):
        decisions.append(f"NB: {int(nb_detail['regs'])} regs, CPA ${nb_detail['cpa']:.0f}")

    # ── Projections ──
    projections = {}
    if proj_data:
        for horizon, key in [("next_week","next_week"),("month","month_end"),("quarter","quarter_end")]:
            pd = proj_data.get(horizon,{}).get(market)
            if pd:
                mp = brief.get("monthly_proj",{}) if brief else {}
                projections[key] = {
                    "period": f"W{wk+1}" if horizon=="next_week" else (mp.get("month","") if horizon=="month" else "Q2 2026"),
                    "regs_proj":pd.get("regs"),"spend_proj":pd.get("spend"),"cpa_proj":pd.get("cpa"),
                    "ci_lo":pd.get("ci_lo"),"ci_hi":pd.get("ci_hi"),"vs_op2_spend":pd.get("vs_op2_spend"),
                }

    # ── Pacing ──
    pacing = {}
    if brief and brief.get("monthly_proj",{}).get("proj_regs"):
        mp = brief["monthly_proj"]
        pacing["narrative"] = f"{mp.get('month','')} projection: {int(mp['proj_regs']):,} regs, ${int(mp.get('proj_spend',0)):,} spend, ${mp.get('proj_cpa',0):.0f} CPA."
        if mp.get("vs_op2_regs") is not None:
            pacing["narrative"] += f" vs OP2: {'+' if mp['vs_op2_regs']>0 else ''}{mp['vs_op2_regs']:.0f}% regs."
        pacing["mtd_regs"] = mp.get("mtd_regs")
        pacing["op2_regs"] = mp.get("op2_regs")

    # ── YoY summary ──
    yoy_summary = ""
    if yoy.get("raw_lines"): yoy_summary = " | ".join(yoy["raw_lines"])
    elif metrics.get("regs_yoy") is not None: yoy_summary = f"Regs {'+' if metrics['regs_yoy']>0 else ''}{metrics['regs_yoy']:.1f}% YoY"
    else: yoy_summary = "No YoY data available."

    return {
        "period": callout.get("period",""),
        "headline": callout.get("headline",""),
        "full_callout": "\n\n".join(callout.get("body_paragraphs",[])),
        "metrics": metrics,
        "brand_detail": brand_detail,
        "nb_detail": nb_detail,
        "weekly_trend": weekly_trend,
        "spend_trend": spend_trend,
        "chart_data": chart_data,
        "yoy_summary": yoy_summary,
        "pacing": pacing,
        "projections": projections,
        "decisions": decisions,
        "external_factors": external,
        "anomalies": anomalies,
        "blocked": [],
    }

# ── Cross-market analysis ────────────────────────────────────────────
def build_cross_market_anomalies(wk, forecast):
    """Compare markets against each other for the same week."""
    anomalies = []
    market_data = {}
    for m in MARKETS:
        fcast = get_weekly_metrics(forecast, m, wk)
        prev = get_weekly_metrics(forecast, m, wk - 1)
        if fcast and (fcast.get("regs", 0) > 0 or fcast.get("cost", 0) > 0):
            wow_regs = None
            if prev and prev.get("regs", 0) > 0 and fcast.get("regs", 0) > 0:
                wow_regs = round((fcast["regs"] - prev["regs"]) / prev["regs"] * 100, 1)
            market_data[m] = {"regs": fcast.get("regs", 0), "spend": fcast.get("cost", 0), "cpa": fcast.get("cpa", 0), "wow_regs": wow_regs}
    if not market_data:
        return anomalies
    import statistics
    wow_vals = {m: d["wow_regs"] for m, d in market_data.items() if d["wow_regs"] is not None}
    if len(wow_vals) >= 3:
        vals = list(wow_vals.values())
        mean_wow = statistics.mean(vals)
        stdev_wow = statistics.stdev(vals) if len(vals) > 1 else 0
        for m, wow in wow_vals.items():
            if stdev_wow > 0 and abs(wow - mean_wow) > 1.5 * stdev_wow:
                flag = "good" if wow > mean_wow else "bad"
                anomalies.append({"metric": f"{m} WoW Regs", "value": f"{wow:+.1f}%", "avg_8wk": f"WW avg {mean_wow:+.1f}%", "deviation": f"{wow - mean_wow:+.1f}pp", "flag": flag, "category": "overall"})
    cpa_vals = {m: d["cpa"] for m, d in market_data.items() if d["cpa"] > 0}
    if len(cpa_vals) >= 3:
        vals = list(cpa_vals.values())
        mean_cpa = statistics.mean(vals)
        stdev_cpa = statistics.stdev(vals) if len(vals) > 1 else 0
        for m, cpa in cpa_vals.items():
            if stdev_cpa > 0 and abs(cpa - mean_cpa) > 1.5 * stdev_cpa:
                flag = "bad" if cpa > mean_cpa else "good"
                anomalies.append({"metric": f"{m} CPA", "value": f"${cpa:.0f}", "avg_8wk": f"WW avg ${mean_cpa:.0f}", "deviation": f"{(cpa - mean_cpa) / mean_cpa * 100:+.0f}%", "flag": flag, "category": "overall"})
    return anomalies

# ── Main ──────────────────────────────────────────────────────────────
def main():
    forecast = load_forecast()

    # Discover all weeks
    weeks = set()
    for base in [ACTIVE_DIR, WIKI_DIR]:
        if not base.exists(): continue
        for mdir in base.iterdir():
            if mdir.is_dir() and mdir.name in [m.lower() for m in MARKETS]:
                for f in mdir.glob("*-2026-w*.md"):
                    if "data-brief" not in f.name and "analysis" not in f.name and "change-log" not in f.name and "context" not in f.name and "projection" not in f.name:
                        wm = re.search(r"w(\d+)", f.name)
                        if wm: weeks.add(int(wm.group(1)))
        # Also check eu5 directory
        eu5_dir = base / "eu5"
        if eu5_dir.exists():
            for f in eu5_dir.glob("eu5-2026-w*.md"):
                wm = re.search(r"w(\d+)", f.name)
                if wm: weeks.add(int(wm.group(1)))
        ww = base / "ww" if (base / "ww").exists() else base
        for f in ww.glob("ww-summary-2026-w*.md"):
            wm = re.search(r"w(\d+)", f.name)
            if wm: weeks.add(int(wm.group(1)))
    weeks = sorted(weeks, reverse=True)
    print(f"Found weeks: {weeks}")

    # Load WW summaries and projections
    ww_summaries = {}
    proj_data = {}
    for w in weeks:
        ww = read_ww_summary(w)
        if ww: ww_summaries[w] = ww
        pd = read_projections(w)
        if pd: proj_data[w] = pd

    # Build all market entries (raw + derived) via the unified build_entry path.
    # WW and EU5 read their pre-aggregated rows from forecast['weekly'][market]
    # which are populated by refresh-forecast.py.
    callouts = {}
    for market in ALL_BUILD_MARKETS:
        callouts[market] = {}
        for w in weeks:
            entry = build_entry(market, w, forecast, ww_summaries.get(w), proj_data.get(w))
            if entry:
                callouts[market][f"W{w}"] = entry

    # Post-enrich WW with cross-market anomalies and the WW summary narrative.
    # (Cross-market comparison still iterates the 10 raw markets, not WW itself.)
    for w in weeks:
        wkey = f"W{w}"
        if wkey not in callouts.get("WW", {}):
            continue
        entry = callouts["WW"][wkey]
        ww_sum = ww_summaries.get(w)
        if ww_sum and ww_sum.get("_callouts"):
            entry["external_factors"] = [{"text": c, "important": True} for c in ww_sum["_callouts"]]
        # Cross-market anomalies override the standard per-market anomaly list for WW
        cm_anoms = build_cross_market_anomalies(w, forecast)
        if cm_anoms:
            entry["anomalies"] = cm_anoms
        # Per-market decision breakdown (unique to WW)
        decisions = []
        for m in MARKETS:
            fcast = get_weekly_metrics(forecast, m, w)
            if fcast and fcast.get("regs", 0) > 0:
                decisions.append(f"{m}: {fcast['regs']:,} regs, ${fcast['cost']:,.0f} spend, ${fcast['cpa']:.0f} CPA")
        if decisions:
            entry["decisions"] = decisions

    # Post-enrich EU5 with per-market decision breakdown.
    for w in weeks:
        wkey = f"W{w}"
        if wkey not in callouts.get("EU5", {}):
            continue
        entry = callouts["EU5"][wkey]
        decisions = []
        for m in ["UK", "DE", "FR", "IT", "ES"]:
            fcast = get_weekly_metrics(forecast, m, w)
            if fcast and fcast.get("regs", 0) > 0:
                decisions.append(f"{m}: {fcast['regs']:,} regs, ${fcast['cost']:,.0f} spend, ${fcast['cpa']:.0f} CPA")
        if decisions:
            entry["decisions"] = decisions

    # Display order: WW, US, EU5, JP, CA, MX, AU (hide individual EU5 markets)
    display_markets = [m for m in DISPLAY_MARKETS if callouts.get(m)]

    output = {
        "generated": datetime.now(tz=timezone.utc).isoformat(),
        "max_wk": forecast.get("max_week", 15),
        "markets": display_markets,
        "weeks": [f"W{w}" for w in weeks],
        "stakeholders": STAKEHOLDERS,
        "callouts": callouts,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2, default=str))
    total = sum(len(v) for v in callouts.values() if isinstance(v, dict))
    print(f"Written {OUTPUT}")
    print(f"Markets: {len(display_markets)}, Weeks: {len(weeks)}, Entries: {total}")

if __name__ == "__main__":
    main()
