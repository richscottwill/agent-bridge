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
def build_entry(market, wk, forecast, ww_data, proj_data):
    """Build one market+week callout entry."""
    callout = read_callout(market, wk)
    if not callout: return None
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

    # Prose fallback for narrative-only callouts
    prose = extract_prose_metrics(callout.get("headline","") + " " + " ".join(callout.get("context_paragraphs",[])))
    for k,v in prose.items():
        if metrics.get(k) is None and v is not None: metrics[k] = v

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

    # Merge YoY into brand/nb detail
    yoy = brief.get("yoy",{}) if brief else {}
    if brand_detail and yoy.get("brand_regs_yoy") is not None: brand_detail["regs_yoy"] = yoy["brand_regs_yoy"]
    if nb_detail and yoy.get("nb_regs_yoy") is not None: nb_detail["regs_yoy"] = yoy["nb_regs_yoy"]
    if nb_detail and yoy.get("nb_cpa_yoy") is not None: nb_detail["cpa_yoy"] = yoy["nb_cpa_yoy"]
    # Prose YoY fallback
    if brand_detail and brand_detail.get("regs_yoy") is None and prose.get("brand_regs_yoy") is not None:
        brand_detail["regs_yoy"] = prose["brand_regs_yoy"]
    if nb_detail and nb_detail.get("regs_yoy") is None and prose.get("nb_regs_yoy") is not None:
        nb_detail["regs_yoy"] = prose["nb_regs_yoy"]
    if nb_detail and nb_detail.get("cpa_yoy") is None and prose.get("nb_cpa_yoy") is not None:
        nb_detail["cpa_yoy"] = prose["nb_cpa_yoy"]

    # Compute full YoY from LY forecast data (fills gaps not covered by data briefs)
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

def build_ww_entry(wk, forecast, ww_data):
    """Build WW aggregate entry."""
    if not ww_data or "_ww" not in ww_data: return None
    ww = ww_data["_ww"]
    decisions = []
    for m in MARKETS:
        fcast = get_weekly_metrics(forecast, m, wk)
        if fcast:
            decisions.append(f"{m}: {fcast['regs']:,} regs, ${fcast['cost']:,.0f} spend, ${fcast['cpa']:.0f} CPA")

    # Cross-market anomalies: compare each market's metrics against the WW average for this week
    anomalies = []
    market_data = {}
    for m in MARKETS:
        fcast = get_weekly_metrics(forecast, m, wk)
        prev = get_weekly_metrics(forecast, m, wk - 1)
        if fcast and (fcast.get("regs", 0) > 0 or fcast.get("cost", 0) > 0):
            wow_regs = None
            if prev and prev.get("regs", 0) > 0 and fcast.get("regs", 0) > 0:
                wow_regs = round((fcast["regs"] - prev["regs"]) / prev["regs"] * 100, 1)
            market_data[m] = {
                "regs": fcast.get("regs", 0),
                "spend": fcast.get("cost", 0),
                "cpa": fcast.get("cpa", 0),
                "wow_regs": wow_regs,
            }

    if market_data:
        import statistics
        # Compare WoW% across markets — flag outliers (>1.5 stdev from mean)
        wow_vals = {m: d["wow_regs"] for m, d in market_data.items() if d["wow_regs"] is not None}
        if len(wow_vals) >= 3:
            vals = list(wow_vals.values())
            mean_wow = statistics.mean(vals)
            stdev_wow = statistics.stdev(vals) if len(vals) > 1 else 0
            for m, wow in wow_vals.items():
                if stdev_wow > 0 and abs(wow - mean_wow) > 1.5 * stdev_wow:
                    direction = "above" if wow > mean_wow else "below"
                    flag = "good" if wow > mean_wow else "bad"
                    anomalies.append({
                        "metric": f"{m} WoW Regs",
                        "value": f"{wow:+.1f}%",
                        "avg_8wk": f"WW avg {mean_wow:+.1f}%",
                        "deviation": f"{wow - mean_wow:+.1f}pp",
                        "flag": flag,
                        "category": "overall",
                    })

        # Compare CPA across markets — flag outliers
        cpa_vals = {m: d["cpa"] for m, d in market_data.items() if d["cpa"] > 0}
        if len(cpa_vals) >= 3:
            vals = list(cpa_vals.values())
            mean_cpa = statistics.mean(vals)
            stdev_cpa = statistics.stdev(vals) if len(vals) > 1 else 0
            for m, cpa in cpa_vals.items():
                if stdev_cpa > 0 and abs(cpa - mean_cpa) > 1.5 * stdev_cpa:
                    flag = "bad" if cpa > mean_cpa else "good"
                    anomalies.append({
                        "metric": f"{m} CPA",
                        "value": f"${cpa:.0f}",
                        "avg_8wk": f"WW avg ${mean_cpa:.0f}",
                        "deviation": f"{(cpa - mean_cpa) / mean_cpa * 100:+.0f}%",
                        "flag": flag,
                        "category": "overall",
                    })

        # Compare regs volume — flag markets significantly above/below WW share
        regs_vals = {m: d["regs"] for m, d in market_data.items() if d["regs"] > 0}
        if len(regs_vals) >= 3:
            total = sum(regs_vals.values())
            mean_share = 100 / len(regs_vals)
            for m, regs in regs_vals.items():
                share = regs / total * 100
                # Flag if share is >2x or <0.5x the equal-share baseline
                if share > mean_share * 2:
                    anomalies.append({
                        "metric": f"{m} Volume Share",
                        "value": f"{regs:,} ({share:.0f}%)",
                        "avg_8wk": f"Equal share {mean_share:.0f}%",
                        "deviation": f"+{share - mean_share:.0f}pp",
                        "flag": "good",
                        "category": "overall",
                    })
    # WW trend from forecast
    ww_trend = {}
    ww_spend = {}
    for m in MARKETS:
        for wk_key, val in get_weekly_trend(forecast, m, wk).items():
            ww_trend[wk_key] = ww_trend.get(wk_key, 0) + (val or 0)
        for wk_key, val in get_spend_trend(forecast, m, wk).items():
            ww_spend[wk_key] = ww_spend.get(wk_key, 0) + (val or 0)
    # WW full chart data (aggregate all markets)
    ww_chart = []
    max_wk_val = forecast.get("max_week", 15)
    for w in range(1, 53):
        entry = {"wk": w, "regs": None, "spend": None, "pred_regs": None, "pred_spend": None, "ci_lo": None, "ci_hi": None, "op2_regs": None}
        for m in MARKETS:
            frow = get_weekly_metrics(forecast, m, w)
            if frow:
                is_actual = frow.get("regs", 0) > 0 or frow.get("cost", 0) > 0
                if is_actual:
                    entry["regs"] = (entry["regs"] or 0) + frow.get("regs", 0)
                    entry["spend"] = (entry["spend"] or 0) + frow.get("cost", 0)
                if frow.get("pred_regs"):
                    entry["pred_regs"] = (entry["pred_regs"] or 0) + frow["pred_regs"]
                if frow.get("op2_regs"):
                    entry["op2_regs"] = (entry["op2_regs"] or 0) + frow["op2_regs"]
        ww_chart.append(entry)
    return {
        "period": f"W{wk}",
        "headline": f"WW drove {int(ww['regs']):,} registrations ({'+' if ww['regs_wow']>0 else ''}{ww['regs_wow']:.1f}% WoW) on ${int(ww['spend']):,} spend ({'+' if ww['spend_wow']>0 else ''}{ww['spend_wow']:.1f}% WoW).",
        "metrics": {"regs":ww["regs"],"regs_wow":ww["regs_wow"],"spend":ww["spend"],"spend_wow":ww["spend_wow"]},
        "brand_detail": None, "nb_detail": None,
        "weekly_trend": ww_trend, "spend_trend": ww_spend, "chart_data": ww_chart,
        "yoy_summary": "", "pacing": {"narrative":"WW aggregate — see individual markets."},
        "projections": {}, "decisions": decisions,
        "external_factors": [{"text":c,"important":True} for c in ww_data.get("_callouts",[])],
        "anomalies": anomalies, "blocked": [],
    }

# ── Main ──────────────────────────────────────────────────────────────
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

EU5_MARKETS = ["UK", "DE", "FR", "IT", "ES"]
# Display order: WW, US, EU5, JP, CA, MX, AU
DISPLAY_MARKETS = ["WW", "US", "EU5", "JP", "CA", "MX", "AU"]

def build_aggregate_entry(label, member_markets, wk, forecast, callouts_dict, proj_data):
    """Build an aggregate entry (EU5 or WW) by summing member market data."""
    # Aggregate metrics from forecast
    agg_regs = 0; agg_spend = 0; agg_brand = 0; agg_nb = 0
    prev_regs = 0; prev_spend = 0
    has_data = False
    for m in member_markets:
        fcast = get_weekly_metrics(forecast, m, wk)
        prev = get_weekly_metrics(forecast, m, wk - 1)
        if fcast and (fcast.get("regs", 0) > 0):
            has_data = True
            agg_regs += fcast.get("regs", 0)
            agg_spend += fcast.get("cost", 0)
            agg_brand += fcast.get("brand_regs", 0) or 0
            agg_nb += fcast.get("nb_regs", 0) or 0
        if prev and prev.get("regs", 0) > 0:
            prev_regs += prev.get("regs", 0)
            prev_spend += prev.get("cost", 0)
    if not has_data:
        return None

    regs_wow = round((agg_regs - prev_regs) / prev_regs * 100, 1) if prev_regs > 0 else None
    spend_wow = round((agg_spend - prev_spend) / prev_spend * 100, 1) if prev_spend > 0 else None
    agg_cpa = round(agg_spend / agg_regs, 2) if agg_regs > 0 else None
    cpa_wow = None
    if prev_regs > 0 and prev_spend > 0:
        prev_cpa = prev_spend / prev_regs
        cpa_wow = round((agg_cpa - prev_cpa) / prev_cpa * 100, 1) if agg_cpa else None

    metrics = {"regs": agg_regs, "spend": agg_spend, "cpa": agg_cpa,
               "regs_wow": regs_wow, "spend_wow": spend_wow, "cpa_wow": cpa_wow,
               "brand_regs": agg_brand, "nb_regs": agg_nb}

    # Aggregate brand/nb detail: regs, spend, clicks, CPA, CVR with WoW
    agg_brand_spend = 0; agg_nb_spend = 0
    agg_brand_clicks = 0; agg_nb_clicks = 0
    prev_brand = 0; prev_nb = 0
    prev_brand_spend = 0; prev_nb_spend = 0
    prev_brand_clicks = 0; prev_nb_clicks = 0
    for m in member_markets:
        fcast = get_weekly_metrics(forecast, m, wk)
        prev = get_weekly_metrics(forecast, m, wk - 1)
        # Current week: get brand/nb spend from data brief if available, else estimate from ratio
        mc = (callouts_dict.get(m, {}).get(f"W{wk}") or {})
        bd = mc.get("brand_detail") or {}
        nd = mc.get("nb_detail") or {}
        if bd.get("cpa") and bd.get("regs"):
            agg_brand_spend += bd["cpa"] * bd["regs"]
        elif fcast and fcast.get("brand_regs") and fcast.get("cost") and fcast.get("regs"):
            agg_brand_spend += fcast["cost"] * fcast["brand_regs"] / fcast["regs"]
        if nd.get("cpa") and nd.get("regs"):
            agg_nb_spend += nd["cpa"] * nd["regs"]
        elif fcast and fcast.get("nb_regs") and fcast.get("cost") and fcast.get("regs"):
            agg_nb_spend += fcast["cost"] * fcast["nb_regs"] / fcast["regs"]
        if bd.get("clicks"): agg_brand_clicks += bd["clicks"]
        if nd.get("clicks"): agg_nb_clicks += nd["clicks"]
        # Previous week
        if prev and prev.get("brand_regs"): prev_brand += prev["brand_regs"]
        if prev and prev.get("nb_regs"): prev_nb += prev["nb_regs"]
        # Prev brand/nb spend estimate
        mc_prev = (callouts_dict.get(m, {}).get(f"W{wk-1}") or {})
        bd_prev = mc_prev.get("brand_detail") or {}
        nd_prev = mc_prev.get("nb_detail") or {}
        if bd_prev.get("cpa") and bd_prev.get("regs"):
            prev_brand_spend += bd_prev["cpa"] * bd_prev["regs"]
        elif prev and prev.get("brand_regs") and prev.get("cost") and prev.get("regs"):
            prev_brand_spend += prev["cost"] * prev["brand_regs"] / prev["regs"]
        if nd_prev.get("cpa") and nd_prev.get("regs"):
            prev_nb_spend += nd_prev["cpa"] * nd_prev["regs"]
        elif prev and prev.get("nb_regs") and prev.get("cost") and prev.get("regs"):
            prev_nb_spend += prev["cost"] * prev["nb_regs"] / prev["regs"]
        if bd_prev.get("clicks"): prev_brand_clicks += bd_prev["clicks"]
        if nd_prev.get("clicks"): prev_nb_clicks += nd_prev["clicks"]

    brand_cpa = round(agg_brand_spend / agg_brand, 2) if agg_brand > 0 and agg_brand_spend > 0 else None
    nb_cpa = round(agg_nb_spend / agg_nb, 2) if agg_nb > 0 and agg_nb_spend > 0 else None
    brand_cvr = round(agg_brand / agg_brand_clicks * 100, 2) if agg_brand_clicks > 0 else None
    nb_cvr = round(agg_nb / agg_nb_clicks * 100, 2) if agg_nb_clicks > 0 else None
    prev_brand_cpa = prev_brand_spend / prev_brand if prev_brand > 0 and prev_brand_spend > 0 else None
    prev_nb_cpa = prev_nb_spend / prev_nb if prev_nb > 0 and prev_nb_spend > 0 else None

    brand_detail = {"regs": float(agg_brand)}
    if agg_brand_spend > 0: brand_detail["cost"] = round(agg_brand_spend)
    if prev_brand > 0: brand_detail["regs_wow"] = round((agg_brand - prev_brand) / prev_brand * 100, 1)
    if brand_cpa: brand_detail["cpa"] = brand_cpa
    if prev_brand_cpa and brand_cpa: brand_detail["cpa_wow"] = round((brand_cpa - prev_brand_cpa) / prev_brand_cpa * 100, 1)
    if agg_brand_spend > 0 and prev_brand_spend > 0: brand_detail["cost_wow"] = round((agg_brand_spend - prev_brand_spend) / prev_brand_spend * 100, 1)
    if agg_brand_clicks > 0: brand_detail["clicks"] = float(agg_brand_clicks)
    if prev_brand_clicks > 0 and agg_brand_clicks > 0: brand_detail["clicks_wow"] = round((agg_brand_clicks - prev_brand_clicks) / prev_brand_clicks * 100, 1)
    if brand_cvr: brand_detail["cvr"] = brand_cvr
    prev_brand_cvr = round(prev_brand / prev_brand_clicks * 100, 2) if prev_brand_clicks > 0 and prev_brand > 0 else None
    if brand_cvr and prev_brand_cvr: brand_detail["cvr_wow"] = round((brand_cvr - prev_brand_cvr) / prev_brand_cvr * 100, 1)

    nb_detail = {"regs": float(agg_nb)}
    if agg_nb_spend > 0: nb_detail["cost"] = round(agg_nb_spend)
    if prev_nb > 0: nb_detail["regs_wow"] = round((agg_nb - prev_nb) / prev_nb * 100, 1)
    if nb_cpa: nb_detail["cpa"] = nb_cpa
    if prev_nb_cpa and nb_cpa: nb_detail["cpa_wow"] = round((nb_cpa - prev_nb_cpa) / prev_nb_cpa * 100, 1)
    if agg_nb_spend > 0 and prev_nb_spend > 0: nb_detail["cost_wow"] = round((agg_nb_spend - prev_nb_spend) / prev_nb_spend * 100, 1)
    if agg_nb_clicks > 0: nb_detail["clicks"] = float(agg_nb_clicks)
    if prev_nb_clicks > 0 and agg_nb_clicks > 0: nb_detail["clicks_wow"] = round((agg_nb_clicks - prev_nb_clicks) / prev_nb_clicks * 100, 1)
    if nb_cvr: nb_detail["cvr"] = nb_cvr
    prev_nb_cvr = round(prev_nb / prev_nb_clicks * 100, 2) if prev_nb_clicks > 0 and prev_nb > 0 else None
    if nb_cvr and prev_nb_cvr: nb_detail["cvr_wow"] = round((nb_cvr - prev_nb_cvr) / prev_nb_cvr * 100, 1)
    if nb_cpa: metrics["nb_cpa"] = nb_cpa

    # Aggregate YoY: volume-weighted average of per-market YoY%
    total_with_yoy = 0; weighted_yoy = 0
    spend_yoy_num = 0; spend_yoy_den = 0
    cpa_yoy_num = 0; cpa_yoy_den = 0
    brand_yoy_num = 0; brand_yoy_den = 0
    nb_yoy_num = 0; nb_yoy_den = 0
    nb_cpa_yoy_num = 0; nb_cpa_yoy_den = 0
    for m in member_markets:
        mc = callouts_dict.get(m, {}).get(f"W{wk}")
        if not mc: continue
        mregs = mc.get("metrics", {}).get("regs", 0) or 0
        mspend = mc.get("metrics", {}).get("spend", 0) or 0
        myoy = mc.get("metrics", {}).get("regs_yoy")
        msyoy = mc.get("metrics", {}).get("spend_yoy")
        mcyoy = mc.get("metrics", {}).get("cpa_yoy")
        if myoy is not None and mregs > 0:
            total_with_yoy += mregs; weighted_yoy += mregs * myoy
        if msyoy is not None and mspend > 0:
            spend_yoy_num += mspend * msyoy; spend_yoy_den += mspend
        if mcyoy is not None and mregs > 0:
            cpa_yoy_num += mregs * mcyoy; cpa_yoy_den += mregs
        bd_m = mc.get("brand_detail") or {}
        nd_m = mc.get("nb_detail") or {}
        if bd_m.get("regs_yoy") is not None and bd_m.get("regs", 0):
            brand_yoy_num += bd_m["regs"] * bd_m["regs_yoy"]; brand_yoy_den += bd_m["regs"]
        if nd_m.get("regs_yoy") is not None and nd_m.get("regs", 0):
            nb_yoy_num += nd_m["regs"] * nd_m["regs_yoy"]; nb_yoy_den += nd_m["regs"]
        if nd_m.get("cpa_yoy") is not None and nd_m.get("regs", 0):
            nb_cpa_yoy_num += nd_m["regs"] * nd_m["cpa_yoy"]; nb_cpa_yoy_den += nd_m["regs"]
    if total_with_yoy > 0: metrics["regs_yoy"] = round(weighted_yoy / total_with_yoy, 1)
    if spend_yoy_den > 0: metrics["spend_yoy"] = round(spend_yoy_num / spend_yoy_den, 1)
    if cpa_yoy_den > 0: metrics["cpa_yoy"] = round(cpa_yoy_num / cpa_yoy_den, 1)
    if brand_yoy_den > 0: brand_detail["regs_yoy"] = round(brand_yoy_num / brand_yoy_den, 1)
    if nb_yoy_den > 0: nb_detail["regs_yoy"] = round(nb_yoy_num / nb_yoy_den, 1)
    if nb_cpa_yoy_den > 0: nb_detail["cpa_yoy"] = round(nb_cpa_yoy_num / nb_cpa_yoy_den, 1)

    # Compute aggregate YoY from LY forecast data for fields not covered by member markets
    ly_brand_regs = 0; ly_nb_regs = 0; ly_brand_cost = 0; ly_nb_cost = 0
    ly_brand_clicks = 0; ly_nb_clicks = 0
    for m in member_markets:
        ly_m = get_ly_metrics(forecast, m, wk)
        if ly_m:
            ly_brand_regs += ly_m.get("brand_regs", 0) or 0
            ly_nb_regs += ly_m.get("nb_regs", 0) or 0
            ly_brand_cost += ly_m.get("brand_cost", 0) or 0
            ly_nb_cost += ly_m.get("nb_cost", 0) or 0
            ly_brand_clicks += ly_m.get("brand_clicks", 0) or 0
            ly_nb_clicks += ly_m.get("nb_clicks", 0) or 0
    def yoy_pct(ty, ly_val):
        if ty and ly_val and ly_val > 0: return round((ty - ly_val) / ly_val * 100, 1)
        return None
    if brand_detail.get("cpa_yoy") is None and brand_cpa and ly_brand_regs > 0 and ly_brand_cost > 0:
        brand_detail["cpa_yoy"] = yoy_pct(brand_cpa, ly_brand_cost / ly_brand_regs)
    if brand_detail.get("cost_yoy") is None and agg_brand_spend > 0 and ly_brand_cost > 0:
        brand_detail["cost_yoy"] = yoy_pct(agg_brand_spend, ly_brand_cost)
    if brand_detail.get("clicks_yoy") is None and agg_brand_clicks > 0 and ly_brand_clicks > 0:
        brand_detail["clicks_yoy"] = yoy_pct(agg_brand_clicks, ly_brand_clicks)
    if brand_detail.get("cvr_yoy") is None and brand_cvr and ly_brand_regs > 0 and ly_brand_clicks > 0:
        ly_b_cvr = ly_brand_regs / ly_brand_clicks * 100
        brand_detail["cvr_yoy"] = round((brand_cvr - ly_b_cvr) / ly_b_cvr * 100, 1)
    if nb_detail.get("cost_yoy") is None and agg_nb_spend > 0 and ly_nb_cost > 0:
        nb_detail["cost_yoy"] = yoy_pct(agg_nb_spend, ly_nb_cost)
    if nb_detail.get("clicks_yoy") is None and agg_nb_clicks > 0 and ly_nb_clicks > 0:
        nb_detail["clicks_yoy"] = yoy_pct(agg_nb_clicks, ly_nb_clicks)
    if nb_detail.get("cvr_yoy") is None and nb_cvr and ly_nb_regs > 0 and ly_nb_clicks > 0:
        ly_n_cvr = ly_nb_regs / ly_nb_clicks * 100
        nb_detail["cvr_yoy"] = round((nb_cvr - ly_n_cvr) / ly_n_cvr * 100, 1)

    # ── vs 4-week average for aggregates ──
    def vsa(ty, avg_val):
        if ty and avg_val and avg_val > 0: return round((ty - avg_val) / avg_val * 100, 1)
        return None
    prev4_regs = []; prev4_spend = []; prev4_brand = []; prev4_nb = []
    prev4_brand_cost = []; prev4_nb_cost = []
    prev4_brand_clicks = []; prev4_nb_clicks = []
    for pw in range(wk - 4, wk):
        wr = 0; ws = 0; wb = 0; wn = 0; wbc = 0; wnc = 0; wbcl = 0; wncl = 0
        for m in member_markets:
            fr = get_weekly_metrics(forecast, m, pw)
            if fr and fr.get("regs", 0) > 0:
                wr += fr.get("regs", 0); ws += fr.get("cost", 0)
                wb += fr.get("brand_regs", 0) or 0; wn += fr.get("nb_regs", 0) or 0
                wbcl += fr.get("brand_clicks", 0) or 0; wncl += fr.get("nb_clicks", 0) or 0
                if fr.get("regs") and fr.get("cost"):
                    wbc += fr["cost"] * (fr.get("brand_regs", 0) or 0) / fr["regs"]
                    wnc += fr["cost"] * (fr.get("nb_regs", 0) or 0) / fr["regs"]
        if wr > 0:
            prev4_regs.append(wr); prev4_spend.append(ws)
            prev4_brand.append(wb); prev4_nb.append(wn)
            prev4_brand_cost.append(wbc); prev4_nb_cost.append(wnc)
            prev4_brand_clicks.append(wbcl); prev4_nb_clicks.append(wncl)
    if prev4_regs:
        n4 = len(prev4_regs)
        ar = sum(prev4_regs) / n4; asp = sum(prev4_spend) / n4
        metrics["regs_vs4wk"] = vsa(agg_regs, ar)
        metrics["spend_vs4wk"] = vsa(agg_spend, asp)
        if agg_cpa and ar > 0 and asp > 0: metrics["cpa_vs4wk"] = vsa(agg_cpa, asp / ar)
        ab = sum(prev4_brand) / n4; an = sum(prev4_nb) / n4
        brand_detail["regs_vs4wk"] = vsa(agg_brand, ab)
        nb_detail["regs_vs4wk"] = vsa(agg_nb, an)
        abc = sum(prev4_brand_cost) / n4; anc = sum(prev4_nb_cost) / n4
        if brand_cpa and ab > 0 and abc > 0: brand_detail["cpa_vs4wk"] = vsa(brand_cpa, abc / ab)
        if nb_cpa and an > 0 and anc > 0: nb_detail["cpa_vs4wk"] = vsa(nb_cpa, anc / an)
        # Cost vs4wk
        if agg_brand_spend > 0: brand_detail["cost_vs4wk"] = vsa(agg_brand_spend, abc)
        if agg_nb_spend > 0: nb_detail["cost_vs4wk"] = vsa(agg_nb_spend, anc)
        # Clicks vs4wk
        abcl = sum(prev4_brand_clicks) / n4; ancl = sum(prev4_nb_clicks) / n4
        if agg_brand_clicks > 0 and abcl > 0: brand_detail["clicks_vs4wk"] = vsa(agg_brand_clicks, abcl)
        if agg_nb_clicks > 0 and ancl > 0: nb_detail["clicks_vs4wk"] = vsa(agg_nb_clicks, ancl)
        # CVR vs4wk
        if brand_cvr and ab > 0 and abcl > 0:
            avg_b_cvr = ab / abcl * 100
            brand_detail["cvr_vs4wk"] = round((brand_cvr - avg_b_cvr) / avg_b_cvr * 100, 1)
        if nb_cvr and an > 0 and ancl > 0:
            avg_n_cvr = an / ancl * 100
            nb_detail["cvr_vs4wk"] = round((nb_cvr - avg_n_cvr) / avg_n_cvr * 100, 1)

    chart = []
    max_wk = forecast.get("max_week", 15)
    for w in range(1, 53):
        entry = {"wk": w, "regs": None, "spend": None, "pred_regs": None, "pred_spend": None, "ci_lo": None, "ci_hi": None, "op2_regs": None}
        for m in member_markets:
            frow = get_weekly_metrics(forecast, m, w)
            if frow:
                is_actual = frow.get("regs", 0) > 0 or frow.get("cost", 0) > 0
                if is_actual:
                    entry["regs"] = (entry["regs"] or 0) + frow.get("regs", 0)
                    entry["spend"] = (entry["spend"] or 0) + frow.get("cost", 0)
                if frow.get("pred_regs"): entry["pred_regs"] = (entry["pred_regs"] or 0) + frow["pred_regs"]
                if frow.get("pred_cost"): entry["pred_spend"] = (entry["pred_spend"] or 0) + frow["pred_cost"]
                if frow.get("ci_lo"): entry["ci_lo"] = (entry["ci_lo"] or 0) + frow["ci_lo"]
                if frow.get("ci_hi"): entry["ci_hi"] = (entry["ci_hi"] or 0) + frow["ci_hi"]
                if frow.get("op2_regs"): entry["op2_regs"] = (entry["op2_regs"] or 0) + frow["op2_regs"]
        chart.append(entry)

    # Aggregate projections
    projections = {}
    if proj_data:
        for horizon, key in [("next_week","next_week"),("month","month_end"),("quarter","quarter_end")]:
            agg_proj = {"regs":0,"spend":0,"ci_lo":0,"ci_hi":0}
            has_proj = False
            for m in member_markets:
                pd = proj_data.get(horizon,{}).get(m)
                if pd:
                    has_proj = True
                    agg_proj["regs"] += pd.get("regs") or 0
                    agg_proj["spend"] += pd.get("spend") or 0
                    if pd.get("ci_lo"): agg_proj["ci_lo"] += pd["ci_lo"]
                    if pd.get("ci_hi"): agg_proj["ci_hi"] += pd["ci_hi"]
            if has_proj:
                cpa = round(agg_proj["spend"] / agg_proj["regs"], 0) if agg_proj["regs"] > 0 else None
                projections[key] = {
                    "period": f"W{wk+1}" if horizon=="next_week" else ("Current Month" if horizon=="month" else "Q2 2026"),
                    "regs_proj": agg_proj["regs"], "spend_proj": agg_proj["spend"], "cpa_proj": cpa,
                    "ci_lo": agg_proj["ci_lo"] or None, "ci_hi": agg_proj["ci_hi"] or None,
                }

    # Try to find a callout file for the aggregate (e.g., eu5-2026-w15.md)
    callout_text = ""
    headline = f"{label} drove {agg_regs:,} registrations ({'+' if regs_wow and regs_wow>0 else ''}{regs_wow or 0:.1f}% WoW) on ${agg_spend:,.0f} spend."
    for base in [WIKI_DIR, ACTIVE_DIR]:
        cf = base / label.lower() / f"{label.lower()}-2026-w{wk}.md"
        if cf.exists():
            parsed = read_callout_raw(cf)
            if parsed:
                callout_text = parsed.get("full_body", "")
                headline = parsed.get("headline", headline)
            break

    # Per-market decisions
    decisions = []
    for m in member_markets:
        fcast = get_weekly_metrics(forecast, m, wk)
        if fcast and fcast.get("regs", 0) > 0:
            decisions.append(f"{m}: {fcast['regs']:,} regs, ${fcast['cost']:,.0f} spend, ${fcast['cpa']:.0f} CPA")

    return {
        "period": f"W{wk}",
        "headline": headline,
        "full_callout": callout_text or headline,
        "metrics": metrics,
        "brand_detail": brand_detail,
        "nb_detail": nb_detail,
        "weekly_trend": {}, "spend_trend": {},
        "chart_data": chart,
        "yoy_summary": "",
        "pacing": {"narrative": f"{label} aggregate."},
        "projections": projections,
        "decisions": decisions,
        "external_factors": [],
        "anomalies": [],
        "blocked": [],
    }

def read_callout_raw(filepath):
    """Read a callout file and return headline + full body."""
    text = filepath.read_text()
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
    headline_parts = []
    for line in body:
        if not line: break
        headline_parts.append(line)
    return {
        "headline": " ".join(headline_parts),
        "full_body": "\n\n".join(body),
    }

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

    # Build individual market entries (all 10)
    callouts = {}
    for market in MARKETS:
        callouts[market] = {}
        for w in weeks:
            entry = build_entry(market, w, forecast, ww_summaries.get(w), proj_data.get(w))
            if entry: callouts[market][f"W{w}"] = entry

    # Build WW aggregate using same aggregation as EU5
    callouts["WW"] = {}
    for w in weeks:
        entry = build_aggregate_entry("WW", MARKETS, w, forecast, callouts, proj_data.get(w))
        if entry:
            # Enrich with WW summary callout text if available
            ww_sum = ww_summaries.get(w)
            if ww_sum and ww_sum.get("_ww"):
                ww = ww_sum["_ww"]
                entry["headline"] = f"WW drove {int(ww['regs']):,} registrations ({'+' if ww['regs_wow']>0 else ''}{ww['regs_wow']:.1f}% WoW) on ${int(ww['spend']):,} spend ({'+' if ww['spend_wow']>0 else ''}{ww['spend_wow']:.1f}% WoW)."
            if ww_sum and ww_sum.get("_callouts"):
                entry["external_factors"] = [{"text":c,"important":True} for c in ww_sum["_callouts"]]
            # Cross-market anomalies
            entry["anomalies"] = build_cross_market_anomalies(w, forecast)
            callouts["WW"][f"W{w}"] = entry

    # Build EU5 aggregate
    callouts["EU5"] = {}
    for w in weeks:
        entry = build_aggregate_entry("EU5", EU5_MARKETS, w, forecast, callouts, proj_data.get(w))
        if entry: callouts["EU5"][f"W{w}"] = entry

    # Display order: WW, US, CA, EU5, JP, AU, MX (hide individual EU5 markets)
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
