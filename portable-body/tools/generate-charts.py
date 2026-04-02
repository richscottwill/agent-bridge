#!/usr/bin/env python3
"""
Body System Dashboard &mdash; Multi-page mini-site generator.
Outputs 5 HTML pages + shared nav. Zero dependencies beyond stdlib.

Pages:
  index.html        &mdash; Overview (scannable summary of all pages)
  growth.html       &mdash; Autonomy & Competence (how am I growing)
  willpower.html    &mdash; Willpower & Patterns (what is blocking me)
  output.html       &mdash; Weekly Output (what did I ship)
  autoresearch.html &mdash; Autoresearch Engine (how's the system)

Usage:
  python3 shared/tools/progress-charts/generate.py [--output-dir path/]
"""

import json, os, re, sys, argparse
from datetime import datetime

HOME = os.path.expanduser("~")
BODY_DIR = os.path.join(HOME, "shared", "context", "body")
ACTIVE_DIR = os.path.join(HOME, "shared", "context", "active")
CHANGELOG = os.path.join(HOME, "shared", "context", "changelog.md")
DEFAULT_OUTPUT_DIR = os.path.join(HOME, "shared", "tools", "progress-charts", "site")

# DuckDB query layer — falls back to regex if unavailable
sys.path.insert(0, os.path.expanduser('~/shared/tools/data'))
try:
    from query import db
    _DUCKDB_AVAILABLE = True
except ImportError:
    _DUCKDB_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════
# PARSERS (unchanged logic, all in one block)
# ═══════════════════════════════════════════════════════════════

def parse_gut_budgets():
    path = os.path.join(BODY_DIR, "gut.md")
    if not os.path.exists(path): return []
    with open(path) as f: text = f.read()
    return [{"organ":m.group(1).strip(),"budget":int(m.group(2)),"actual":int(m.group(3)),"utilization":int(m.group(4))}
            for m in re.finditer(r"\|\s*(\w[\w\s]*?)\s*\|\s*(\d+)w\s*\|\s*(\d+)w\s*\|\s*(\d+)%\s*\|", text)]

def _parse_changelog_regex():
    """Regex fallback: parse changelog.md for savings, runs, body totals, experiments."""
    if not os.path.exists(CHANGELOG): return {"savings":[],"runs":[],"body_totals":[],"experiments":[]}
    with open(CHANGELOG) as f: text = f.read()
    savings = [{"before":int(m.group(1).replace(",","")),"after":int(m.group(2).replace(",","")),"saved":int(m.group(1).replace(",",""))-int(m.group(2).replace(",",""))}
               for m in re.finditer(r"([\d,]{3,7})w\s*→\s*([\d,]{3,7})w", text)
               if int(m.group(1).replace(",",""))>500 and int(m.group(2).replace(",",""))>200]
    runs = [{"date":m.group(1),"run":int(m.group(2))} for m in re.finditer(r"## (2026-\d{2}-\d{2}) &mdash; Autoresearch Loop Run (\d+)", text)]
    body_totals = [int(m.group(1).replace(",","")) for m in re.finditer(r"(?:Total body|Body total|Actual body total)[:\s]*~?([\d,]{4,6})w", text, re.IGNORECASE)]
    seen = {}
    for m in re.finditer(r"CE-(\d+)\s+[^|]*?(ADOPTED|REVERTED|QUEUED|IN PROGRESS)", text, re.IGNORECASE):
        seen[int(m.group(1))] = m.group(2).upper()
    experiments = [{"id":k,"status":v} for k,v in sorted(seen.items())]
    return {"savings":savings,"runs":runs,"body_totals":body_totals,"experiments":experiments}

def parse_changelog():
    """Parse changelog data. Uses DuckDB for experiments (and savings if compression_log
    table exists), falls back to regex for everything else or on DuckDB failure."""
    # Always get runs and body_totals from regex — these are narrative/log metadata
    regex_data = _parse_changelog_regex()

    if not _DUCKDB_AVAILABLE:
        return regex_data

    result = {"savings": regex_data["savings"], "runs": regex_data["runs"],
              "body_totals": regex_data["body_totals"], "experiments": regex_data["experiments"]}

    # Experiments: try DuckDB first (experiment_id is VARCHAR like 'CE-1')
    try:
        rows = db("SELECT experiment_id, status FROM experiments ORDER BY experiment_id")
        if rows:
            exps = []
            for r in rows:
                eid = r["experiment_id"]
                # Extract numeric id from 'CE-1' format
                id_match = re.search(r"(\d+)", str(eid))
                exps.append({"id": int(id_match.group(1)) if id_match else eid,
                             "status": r["status"].upper()})
            result["experiments"] = exps
    except Exception:
        pass  # keep regex fallback

    # Savings: try DuckDB if compression_log table exists
    try:
        tables = db("SELECT table_name FROM duckdb_tables() WHERE table_name = 'compression_log'")
        if tables:
            rows = db("SELECT before_words, after_words FROM compression_log WHERE before_words > 500 AND after_words > 200 ORDER BY id")
            if rows:
                result["savings"] = [{"before": r["before_words"], "after": r["after_words"],
                                      "saved": r["before_words"] - r["after_words"]} for r in rows]
    except Exception:
        pass  # keep regex fallback

    return result

def _parse_tracker_scorecard_regex():
    """Regex fallback: parse rw-tracker.md for weekly scorecard data."""
    path = os.path.join(ACTIVE_DIR, "rw-tracker.md")
    if not os.path.exists(path): return []
    with open(path) as f: text = f.read()
    weeks = []
    for m in re.finditer(r"### Week of (\d{4}-\d{2}-\d{2}) \(W(\d+)\)", text):
        start = m.end(); nxt = text.find("### Week of", start)
        section = text[start:nxt] if nxt > 0 else text[start:start+500]
        a = re.search(r"Strategic artifacts shipped\s*\|\s*(\d+)\s*\|\s*(\d+)", section)
        t = re.search(r"Tools/automations built\s*\|\s*(\d+)\s*\|\s*(\d+)", section)
        l = re.search(r"Hours on low-leverage work\s*\|\s*<(\d+)\s*\|\s*~?(\d+)", section)
        weeks.append({"week":f"W{int(m.group(2))}","date":m.group(1),
                       "artifacts":int(a.group(2)) if a else 0,"tools":int(t.group(2)) if t else 0,
                       "low_leverage_hours":int(l.group(2)) if l else 0})
    return weeks

def parse_tracker_scorecard():
    """Parse weekly scorecard. Uses DuckDB weekly_metrics when available,
    falls back to regex parsing of rw-tracker.md."""
    if not _DUCKDB_AVAILABLE:
        return _parse_tracker_scorecard_regex()

    try:
        rows = db(
            "SELECT DISTINCT week "
            "FROM weekly_metrics "
            "ORDER BY week DESC"
        )
        if rows:
            weeks = []
            for r in rows:
                # Extract week number from format '2026 W13' -> 'W13'
                week_str = r.get("week", "")
                w_match = re.search(r"W(\d+)", week_str)
                week_label = f"W{int(w_match.group(1))}" if w_match else week_str
                weeks.append({
                    "week": week_label,
                    "date": week_str,
                    "artifacts": 0,  # not in weekly_metrics — scorecard-specific
                    "tools": 0,
                    "low_leverage_hours": 0,
                })
            # DuckDB provides the canonical week list. Overlay personal output
            # metrics (artifacts, tools, low_leverage_hours) from regex since
            # those live in rw-tracker.md, not in DuckDB.
            regex_data = _parse_tracker_scorecard_regex()
            regex_by_week = {w["week"]: w for w in regex_data}
            for w in weeks:
                if w["week"] in regex_by_week:
                    rw = regex_by_week[w["week"]]
                    w["date"] = rw["date"]
                    w["artifacts"] = rw["artifacts"]
                    w["tools"] = rw["tools"]
                    w["low_leverage_hours"] = rw["low_leverage_hours"]
            return weeks
        # Empty DuckDB result — fall back to regex
        return _parse_tracker_scorecard_regex()
    except Exception:
        return _parse_tracker_scorecard_regex()

def parse_patterns():
    path = os.path.join(BODY_DIR, "nervous-system.md")
    if not os.path.exists(path): return []
    with open(path) as f: text = f.read()
    return [{"name":m.group(1).strip(),"status":m.group(2).strip(),"weeks":m.group(3).strip(),
             "trajectory":m.group(4).strip(),"assessment":m.group(5).strip()[:120]}
            for m in re.finditer(r"\|\s*([^|]+?)\s*\|\s*(VALIDATED|ACTIVE|NEW|RESOLVED|STUCK)\s*\|\s*([^|]*?)\s*\|\s*(IMPROVING|STUCK|WORSENING|&mdash;)\s*\|\s*([^|]*?)\s*\|", text)]


def parse_amcc():
    path = os.path.join(BODY_DIR, "amcc.md")
    if not os.path.exists(path): return {"streak":0,"hard_thing":"unknown","longest":0,"resets":0,"resistance_types":[],"growth_model":[]}
    with open(path) as f: text = f.read()
    data = {"streak":0,"hard_thing":"unknown","longest":0,"resets":0,"resistance_types":[],"growth_model":[]}
    sm = re.search(r"Current streak\s*\|\s*(\d+)\s*day", text, re.IGNORECASE)
    if sm: data["streak"] = int(sm.group(1))
    lm = re.search(r"Longest streak\s*\|\s*(\d+)\s*day", text, re.IGNORECASE)
    if lm: data["longest"] = int(lm.group(1))
    rm = re.search(r"Streak resets \(total\)\s*\|\s*(\d+)", text, re.IGNORECASE)
    if rm: data["resets"] = int(rm.group(1))
    hm = re.search(r"\*\*Ship ([^*]+)\*\*", text)
    if hm: data["hard_thing"] = hm.group(1).strip()
    for m in re.finditer(r"\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*\"([^\"]+)\"", text):
        data["resistance_types"].append({"type":m.group(1).strip(),"description":m.group(2).strip()[:60],"counter":m.group(4).strip()[:80]})
    gs = text.find("Growth Model")
    if gs > 0:
        gt = text[gs:gs+1200]
        for metric in ["Current streak","Avg days to complete hard thing","Avoidance count per hard thing","Resistance types active","Interventions per session"]:
            mm = re.search(re.escape(metric)+r"\s*\|\s*([^|\n]+?)\s*\|\s*([^|\n]+?)\s*\|\s*([^|\n]+?)\s*\|", gt)
            if mm: data["growth_model"].append({"metric":metric,"current":mm.group(1).strip(),"target_30d":mm.group(2).strip(),"target_90d":mm.group(3).strip()})
    return data

def parse_five_levels():
    path = os.path.join(BODY_DIR, "brain.md")
    if not os.path.exists(path): return []
    with open(path) as f: text = f.read()
    levels = []
    for m in re.finditer(r"### Level (\d+):\s*([^\n]+)\n([^#]*?)(?=### Level|\Z)", text):
        num, name, block = int(m.group(1)), m.group(2).strip(), m.group(3)[:300]
        status = "ACTIVE" if "ACTIVE" in block.upper() else "NEXT" if "NEXT" in block.upper() else "QUEUED" if "QUEUED" in block.upper() else "FUTURE"
        desc_m = re.search(r"- (.+)", block)
        levels.append({"level":num,"name":name,"description":desc_m.group(1).strip()[:80] if desc_m else "","status":status})
    return levels[:5]

def parse_organ_staleness():
    organs = ["brain","eyes","hands","memory","spine","device","nervous-system","amcc","gut","heart"]
    results, today = [], datetime.now()
    for organ in organs:
        path = os.path.join(BODY_DIR, f"{organ}.md")
        if not os.path.exists(path): continue
        with open(path) as f: first = f.read(500)
        dm = re.search(r"Last updated:\s*(2026-\d{2}-\d{2})", first)
        days = (today - datetime.strptime(dm.group(1), "%Y-%m-%d")).days if dm else -1
        results.append({"organ":organ,"days_stale":days,"updated":dm.group(1) if dm else "unknown"})
    return results

def parse_experiment_queue():
    path = os.path.join(BODY_DIR, "heart.md")
    if not os.path.exists(path): return []
    with open(path) as f: text = f.read()
    return [{"id":int(m.group(1)),"name":m.group(2).strip(),"status":m.group(3) or "QUEUED"}
            for m in re.finditer(r"### CE-(\d+):\s*([^\n]+?)(?:\s*&mdash;\s*(QUEUED|IN PROGRESS|NEXT))?(?:\s*\(([^)]+)\))?\s*\n", text)]

def parse_thirty_day_challenge():
    path = os.path.join(ACTIVE_DIR, "rw-tracker.md")
    if not os.path.exists(path): return {"items":[],"completed":0,"total":0,"deadline":""}
    with open(path) as f: text = f.read()
    start = text.find("## 30-Day Challenge")
    if start < 0: return {"items":[],"completed":0,"total":0,"deadline":""}
    end = text.find("\n## ", start + 5)
    section = text[start:end] if end > 0 else text[start:start+1000]
    items = [{"text":m.group(2).strip()[:100],"done":m.group(1).strip().lower()=="x"} for m in re.finditer(r"- \[([ xX])\] (.+)", section)]
    deadline_m = re.search(r"by (\d{4}-\d{2}-\d{2})", section)
    return {"items":items,"completed":sum(1 for i in items if i["done"]),"total":len(items),"deadline":deadline_m.group(1) if deadline_m else ""}

def _stage_label(score):
    return {1:"Unconscious Incompetence",2:"Conscious Incompetence",3:"Conscious Competence",4:"Unconscious Competence"}.get(score,"Unknown")

def parse_competence_stages():
    pattern_data = parse_patterns()
    changelog_data = parse_changelog()
    savings = changelog_data.get("savings",[])
    body_totals = changelog_data.get("body_totals",[])
    s1, e1 = 3, "Morning routine built and running. Still userTriggered (not automatic)."
    s2 = 3; e2 = f"Autoresearch runs structural experiments. {len(savings)} structural changes logged." if len(savings)>3 else "Autoresearch runs structural experiments. Limited history so far."
    if len(body_totals)>=2 and body_totals[-1]<body_totals[0]: s3,e3 = 3,f"Body mass trending down ({body_totals[0]:,}w \u2192 {body_totals[-1]:,}w)."
    else: s3,e3 = 3,"Gut budgets exist. Insufficient trend data for trajectory."
    s4, e4 = 3, "Routine consolidated (3 hooks \u2192 1). Shape stable since 3/20. Contents evolve."
    improving = [p for p in pattern_data if p.get("trajectory")=="IMPROVING"]
    s5,e5 = (3,f"{len(improving)} patterns improving organically.") if improving else (2,"No patterns improving without active intervention yet.")
    s6, e6 = 2, "Morning routine pre-drafts replies. But only 1/3 templates built. Most decisions still manual."
    principles = [
        {"name":"Routine as liberation","score":s1,"evidence":e1,"stage_label":_stage_label(s1),"source":"Duhigg"},
        {"name":"Structural over cosmetic","score":s2,"evidence":e2,"stage_label":_stage_label(s2),"source":"McKeown"},
        {"name":"Subtraction before addition","score":s3,"evidence":e3,"stage_label":_stage_label(s3),"source":"McKeown"},
        {"name":"Protect the habit loop","score":s4,"evidence":e4,"stage_label":_stage_label(s4),"source":"Duhigg"},
        {"name":"Invisible over visible","score":s5,"evidence":e5,"stage_label":_stage_label(s5),"source":"Gollwitzer"},
        {"name":"Reduce decisions, not options","score":s6,"evidence":e6,"stage_label":_stage_label(s6),"source":"McKeown"},
    ]
    return {"principles":principles,"average":round(sum(p["score"] for p in principles)/len(principles),1)}

def parse_autonomy_spectrum():
    functions = []
    functions.append({"name":"Bid management & optimization (AU/MX)","category":"human","section":"Campaign Ops"})
    functions.append({"name":"Keyword research & negative keyword mgmt","category":"human","section":"Campaign Ops"})
    functions.append({"name":"Search term report review","category":"human","section":"Campaign Ops"})
    functions.append({"name":"Competitor impression share monitoring","category":"human","section":"Campaign Ops"})
    functions.append({"name":"Ad copy creation & A/B testing","category":"human","section":"Campaign Ops"})
    functions.append({"name":"Landing page coordination (Polaris)","category":"human","section":"Campaign Ops"})
    functions.append({"name":"Spend pacing & budget monitoring","category":"human","section":"Campaign Ops"})
    functions.append({"name":"Campaign structure changes","category":"human","section":"Campaign Ops"})
    functions.append({"name":"Daily anomaly flagging (spend/CPA spikes)","category":"human","section":"Campaign Ops"})
    functions.append({"name":"WBR callout writing (10 markets)","category":"agent_human","section":"Reporting"})
    functions.append({"name":"Weekly dashboard data extraction","category":"agent_human","section":"Reporting"})
    functions.append({"name":"Performance trend analysis","category":"human","section":"Reporting"})
    functions.append({"name":"Stakeholder reporting (Kate/Brandon/Lena)","category":"human","section":"Reporting"})
    functions.append({"name":"Kingpin goal updates","category":"human","section":"Reporting"})
    functions.append({"name":"MBR/QBR narrative preparation","category":"human","section":"Reporting"})
    functions.append({"name":"Test design & documentation","category":"human","section":"Strategic"})
    functions.append({"name":"OP1 narrative writing","category":"human","section":"Strategic"})
    functions.append({"name":"Cross-market playbook development","category":"human","section":"Strategic"})
    functions.append({"name":"AEO/AI Overviews POV","category":"human","section":"Strategic"})
    functions.append({"name":"OCI rollout coordination","category":"human","section":"Strategic"})
    functions.append({"name":"Invoice/PO processing (AU/MX)","category":"human","section":"Admin"})
    functions.append({"name":"Budget forecasting (R&O input)","category":"human","section":"Admin"})
    functions.append({"name":"Flash topics submission","category":"human","section":"Admin"})
    functions.append({"name":"PTO/compliance admin","category":"human","section":"Admin"})
    functions.append({"name":"Email triage & response","category":"agent_human","section":"Communication"})
    functions.append({"name":"Meeting prep (briefs, talking points)","category":"agent_human","section":"Communication"})
    functions.append({"name":"Stakeholder updates & proactive sharing","category":"human","section":"Communication"})
    functions.append({"name":"Cross-team coordination (MarTech/Legal/DS)","category":"human","section":"Communication"})
    functions.append({"name":"Meeting attendance (~10 recurring/week)","category":"human","section":"Communication"})
    path = os.path.join(BODY_DIR, "device.md")
    if os.path.exists(path):
        with open(path) as f: text = f.read()
        for m in re.finditer(r"### ([^\n]+)\n-\s*\*\*Status:\*\*\s*(IN PROGRESS|RESTORED)", text):
            functions.append({"name":m.group(1).strip(),"category":"delegated","section":"Delegated"})
    functions.append({"name":"Safety guards (email/calendar blocks)","category":"fully_agentic","section":"Agents"})
    functions.append({"name":"Hedy meeting sync & analysis","category":"fully_agentic","section":"Agents"})
    functions.append({"name":"Morning routine (sync/drafts/brief/blocks)","category":"agent_human","section":"Agents"})
    functions.append({"name":"Autoresearch loop (maintenance/experiments)","category":"agent_human","section":"Agents"})
    functions.append({"name":"Karpathy (loop governance/compression)","category":"agent_human","section":"Agents"})
    functions.append({"name":"Eyes Chart (dashboard generation)","category":"agent_human","section":"Agents"})
    functions.append({"name":"Dashboard ingester (market data)","category":"agent_human","section":"Agents"})
    functions.append({"name":"Progress charts (body system)","category":"agent_human","section":"Agents"})
    functions.append({"name":"Body organ maintenance & updates","category":"agent_human","section":"System"})
    functions.append({"name":"Context file freshness monitoring","category":"agent_human","section":"System"})
    functions.append({"name":"Agent-bridge sync","category":"agent_human","section":"System"})
    cats = {"fully_agentic":0,"agent_human":0,"human":0,"delegated":0}
    for f in functions:
        if f["category"] in cats: cats[f["category"]] += 1
    total = sum(cats.values())
    pcts = {k:round(v/max(total,1)*100) for k,v in cats.items()}
    return {"functions":functions,"summary":cats,"percentages":pcts,"total":total,
            "confidence":"medium","confidence_note":"Agents/tools from device.md (high). Campaign ops from hands.md (high). Strategic/communication estimated from role scope (medium)."}


# ═══════════════════════════════════════════════════════════════
# HTML GENERATION &mdash; Shared components + per-page builders
# ═══════════════════════════════════════════════════════════════

def shared_head(title, active_page):
    """Shared <head> + nav bar for all pages."""
    pages = [("index.html","Overview"),("growth.html","Growth"),("willpower.html","Willpower"),("output.html","Output"),("autoresearch.html","Autoresearch")]
    nav = ''.join(f'<a href="{href}" class="nav-link{" active" if href==active_page else ""}">{label}</a>' for href,label in pages)
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{{--bg:#0b0e11;--surface:#131820;--surface2:#1a2230;--border:#1e2a3a;--border2:#253345;
  --text:#d0d8e0;--text2:#8899aa;--text3:#5a6a7a;--white:#f0f4f8;
  --accent:#4da8da;--accent2:#2d7eb5;--accent-dim:rgba(77,168,218,0.12);
  --green:#34d399;--red:#f87171;--amber:#fbbf24;--purple:#a78bfa}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'DM Sans',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg);color:var(--text);padding:0;min-height:100vh;-webkit-font-smoothing:antialiased}}
.page{{max-width:1200px;margin:0 auto;padding:24px 20px}}
nav{{background:var(--surface);border-bottom:1px solid var(--border);padding:0 24px;display:flex;align-items:center;gap:0;position:sticky;top:0;z-index:100;backdrop-filter:blur(12px);background:rgba(19,24,32,0.92)}}
.nav-brand{{color:var(--white);font-weight:700;font-size:.9em;padding:14px 20px 14px 0;border-right:1px solid var(--border);margin-right:4px;letter-spacing:1.5px;text-transform:uppercase}}
.nav-link{{color:var(--text2);text-decoration:none;padding:14px 18px;font-size:.8em;font-weight:500;border-bottom:2px solid transparent;transition:all .15s;letter-spacing:.3px}}
.nav-link:hover{{color:var(--text);background:rgba(77,168,218,0.06)}}
.nav-link.active{{color:var(--accent);border-bottom-color:var(--accent)}}
h1{{color:var(--white);font-size:1.35em;margin-bottom:4px;font-weight:600;letter-spacing:.2px}}
h2{{color:var(--text);font-size:.95em;margin:28px 0 12px;font-weight:600;letter-spacing:.2px}}
.sub{{color:var(--text2);font-size:.78em;margin-bottom:24px;line-height:1.5}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:16px;margin-bottom:16px}}
.grid-3{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-bottom:16px}}
.card{{background:var(--surface);border-radius:8px;padding:18px;border:1px solid var(--border)}}
.card-title{{color:var(--text2);font-size:.72em;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px;font-weight:500}}
.chart-box{{position:relative;height:280px}}
.chart-box-sm{{position:relative;height:200px}}
.stats{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px}}
.stat{{background:var(--surface);border-radius:6px;padding:12px 16px;border:1px solid var(--border);min-width:100px}}
.stat .v{{font-size:1.5em;font-weight:700;color:var(--white)}}
.stat .l{{font-size:.62em;color:var(--text3);text-transform:uppercase;letter-spacing:.8px;margin-top:2px}}
table{{width:100%;border-collapse:collapse;font-size:.82em}}
th{{text-align:left;color:var(--text3);font-weight:500;padding:8px;border-bottom:1px solid var(--border);font-size:.85em;text-transform:uppercase;letter-spacing:.5px}}
td{{padding:8px;border-bottom:1px solid var(--border)}}
.badge{{font-size:.68em;padding:3px 10px;border-radius:3px;font-weight:600;text-transform:uppercase;display:inline-block;letter-spacing:.3px}}
.b-worsening{{background:rgba(248,113,113,0.15);color:var(--red)}}.b-stuck{{background:rgba(251,191,36,0.15);color:var(--amber)}}
.b-improving{{background:rgba(52,211,153,0.15);color:var(--green)}}.b-new{{background:var(--accent-dim);color:var(--accent)}}
.b-validated{{background:rgba(167,139,250,0.15);color:var(--purple)}}.b-active{{background:var(--accent-dim);color:var(--accent)}}
.b-adopted{{background:rgba(52,211,153,0.15);color:var(--green)}}.b-reverted{{background:rgba(248,113,113,0.15);color:var(--red)}}
.b-queued{{background:rgba(90,106,122,0.15);color:var(--text2)}}
.no-data{{color:var(--text3);font-style:italic;padding:20px;text-align:center}}
.trainer{{font-size:.78em;color:var(--text3);margin-top:12px;line-height:1.5;padding:10px 0;border-top:1px solid var(--border)}}
.level-track{{margin-bottom:10px;padding:14px;background:var(--bg);border-radius:6px;border:1px solid var(--border)}}
.level-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}}
.level-name{{font-weight:600;font-size:.9em;color:var(--white)}}
.level-bar{{height:4px;background:var(--surface2);border-radius:2px;overflow:hidden;margin:6px 0}}
.level-fill{{height:100%;border-radius:2px}}
.lb{{font-size:.62em;padding:3px 10px;border-radius:3px;font-weight:600;text-transform:uppercase;letter-spacing:.5px}}
.lb-active{{background:var(--accent-dim);color:var(--accent)}}.lb-next{{background:rgba(90,106,122,0.15);color:var(--text2)}}
.lb-queued{{background:rgba(90,106,122,0.08);color:var(--text3)}}.lb-future{{background:rgba(90,106,122,0.05);color:var(--text3)}}
.comp-row{{margin-bottom:14px}}
.comp-label{{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}}
.comp-name{{font-weight:600;font-size:.85em;color:var(--text)}}
.comp-stage{{font-size:.7em;color:var(--text3)}}
.comp-track{{display:flex;height:22px;background:var(--surface2);border-radius:4px;overflow:hidden}}
.comp-stop{{flex:1;display:flex;align-items:center;justify-content:center;font-size:.58em;font-weight:600;color:rgba(255,255,255,0.1);border-right:1px solid var(--border)}}
.comp-stop:last-child{{border-right:none}}
.comp-stop.filled{{color:rgba(255,255,255,0.9)}}
.ch-item{{display:flex;align-items:flex-start;gap:10px;padding:6px 0;border-bottom:1px solid var(--border);font-size:.85em}}
.ch-box{{width:16px;height:16px;border-radius:3px;border:1.5px solid var(--border2);display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;font-size:.65em}}
.ch-done{{background:var(--accent-dim);border-color:var(--accent);color:var(--accent)}}
.ch-text{{color:var(--text)}}.ch-text.done{{color:var(--text3);text-decoration:line-through}}
.overview-card{{background:var(--surface);border-radius:8px;padding:20px;border:1px solid var(--border);text-decoration:none;display:block;transition:all .2s}}
.overview-card:hover{{border-color:var(--accent);box-shadow:0 0 20px rgba(77,168,218,0.08)}}
.oc-title{{color:var(--text2);font-weight:600;font-size:.78em;margin-bottom:8px;text-transform:uppercase;letter-spacing:.8px}}
.oc-metric{{font-size:1.8em;font-weight:700;margin:8px 0;color:var(--white)}}
.oc-sub{{color:var(--text2);font-size:.78em;line-height:1.5}}
</style></head><body>
<nav><span class="nav-brand">Body System</span>{nav}</nav>
<div class="page">'''


def shared_footer(now):
    return f'<div style="color:var(--text3);font-size:.62em;text-align:center;margin-top:48px;padding:16px;letter-spacing:.5px">GENERATED {now} &middot; STANDALONE HTML &middot; CHART.JS VIA CDN &middot; PORTABLE</div></div></body></html>'


# ═══════════════════════════════════════════════════════════════
# PAGE: Overview (index.html)
# ═══════════════════════════════════════════════════════════════

def build_overview(data, now):
    d = data
    auto = d["autonomy"]; comp = d["competence"]; amcc = d["amcc"]; ch = d["challenge"]
    budgets = d["budgets"]; cl = d["changelog"]; sc = d["scorecard"]; fl = d["five_levels"]
    ta = sum(b["actual"] for b in budgets); tb = sum(b["budget"] for b in budgets)
    adopted = sum(1 for e in cl["experiments"] if e["status"]=="ADOPTED")
    reverted = sum(1 for e in cl["experiments"] if e["status"]=="REVERTED")
    worsening = sum(1 for p in d["patterns"] if p["trajectory"]=="WORSENING")
    stuck = sum(1 for p in d["patterns"] if p["trajectory"]=="STUCK")
    zero_weeks = sum(1 for w in sc if w["artifacts"]==0)
    agent_pct = auto["percentages"].get("fully_agentic",0)+auto["percentages"].get("agent_human",0)
    human_pct = auto["percentages"].get("human",0)

    html = shared_head("Overview &mdash; Body System", "index.html")
    html += f'''
<h1>Body System</h1>
<div class="sub">A personal operating system for closing the gap between intention and execution. Built on the body metaphor: 11 organs that hold context, make decisions, track patterns, and enforce willpower. Maintained by an autoresearch loop inspired by Karpathy. This is the control panel.</div>

<p style="color:var(--text);font-size:.9em;line-height:1.7;margin-bottom:24px">
  The system was created on March 20, 2026 to solve a specific problem: Richard knows what to do but struggles to consistently do it. The Annual Review confirmed it &mdash; "Meets High Bar" overall, but the #1 growth area is visibility. Not skill. Not effort. Visibility: shipping strategic artifacts, sharing work proactively, documenting decisions so the team can reference them without asking. The body system exists to make that behavior automatic rather than effortful.
</p>

<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:32px">
  Right now, the system is {len(cl["runs"])} loop runs old. It has run {adopted + reverted} experiments with a {round(adopted/max(adopted+reverted,1)*100)}% keep rate, saving {sum(s["saved"] for s in cl["savings"]):,} words of context bloat. {agent_pct}% of Richard's work functions involve an agent in some capacity, though {human_pct}% remain fully manual. The willpower streak is at {amcc["streak"]} days. The hard thing is the Testing Approach doc for Kate's April 16 meeting. {ch["completed"]} of {ch["total"]} 30-day challenge items are complete.
</p>

<h2>Where Things Stand</h2>
<div class="grid">
  <a href="growth.html" class="overview-card">
    <div class="oc-title">Autonomy and Competence</div>
    <div class="oc-metric" style="color:var(--accent)">{agent_pct}% agent-involved</div>
    <div class="oc-sub">{auto["summary"].get("fully_agentic",0)} functions run without any human input. {auto["summary"].get("agent_human",0)} require a human trigger or approval. {auto["summary"].get("human",0)} are still fully manual &mdash; campaign ops, strategic writing, and admin. The competence model averages {comp["average"]}/4 across 6 operating principles, with two still at Stage 2 (conscious incompetence).</div>
  </a>

  <a href="willpower.html" class="overview-card">
    <div class="oc-title">Willpower and Patterns</div>
    <div class="oc-metric" style="color:{"var(--alert)" if amcc["streak"]==0 else "var(--accent)"}">{amcc["streak"]} day streak</div>
    <div class="oc-sub">The aMCC tracks the gap between knowing and doing. {len(amcc.get("resistance_types",[]))} resistance types are active &mdash; visibility avoidance is the root cause. {worsening} behavioral pattern{"s are" if worsening!=1 else " is"} worsening, {stuck} {"are" if stuck!=1 else "is"} stuck. The 30-day challenge has {ch["total"]} items due by {ch.get("deadline","TBD")}, with {ch["completed"]} complete so far.</div>
  </a>

  <a href="output.html" class="overview-card">
    <div class="oc-title">Weekly Output</div>
    <div class="oc-metric" style="color:{"var(--alert)" if zero_weeks==len(sc) and len(sc)>0 else "var(--accent)"}">{ch["completed"]}/{ch["total"]} challenge items</div>
    <div class="oc-sub">{"Zero strategic artifacts shipped across all " + str(len(sc)) + " tracked weeks. This is the #1 pattern to break &mdash; the Level 1 gate requires 4 consecutive weeks with a shipped artifact. The Testing Approach doc is the convergence point: a Level 2 artifact that proves Level 1 consistency." if zero_weeks==len(sc) and len(sc)>0 else str(len(sc))+" weeks tracked in the scorecard."} Low-leverage work (invoices, manual campaign updates, reactive deep dives) is tracked separately to make the time cost visible.</div>
  </a>

  <a href="autoresearch.html" class="overview-card">
    <div class="oc-title">Autoresearch Engine</div>
    <div class="oc-metric" style="color:var(--accent)">{ta:,}w / {tb:,}w</div>
    <div class="oc-sub">The body holds {ta:,} words of context across {len(budgets)} organs, against a {tb:,}-word budget ceiling. {adopted} experiments have been adopted, compressing {sum(s["saved"] for s in cl["savings"]):,} words while maintaining accuracy. The loop runs autonomously &mdash; Karpathy governs experiments, the gut enforces budgets, and dual blind evaluation ensures quality.</div>
  </a>
</div>

<h2>The Five Levels</h2>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:16px">
  The strategic north star. Each level funds the next &mdash; you do not graduate until the gate is met. Level 1 (consistent artifact output) is the foundation. Level 5 (full agentic orchestration) is the end state. Right now, Levels 1 and 2 are active, with Level 1 struggling. The Testing Approach doc is the artifact that bridges both: it proves Level 1 consistency while advancing Level 2 testing ownership.
</p>
<div class="card" id="levelsOverview"></div>

<h2>30-Day Challenge</h2>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:16px">
  Ten items due by {ch.get("deadline","April 13, 2026")}. A mix of strategic artifacts (Testing Approach doc, AEO POV, AI Max test design), system improvements (campaign link generator, Asana decision), and operational cleanup (invoice reduction, meeting audit, Polaris migration). {ch["completed"]}/{ch["total"]} complete. The highest-leverage items are the Testing Approach doc and AI Max test design &mdash; they feed Level 1 and Level 2 simultaneously.
</p>
<div class="card" id="challengeOverview"></div>

<script>
var fiveLevels={json.dumps(fl)};
var challenge={json.dumps(ch)};
'''
    html += '''
(function(){
  var el=document.getElementById('levelsOverview');
  var gates=['4 consecutive artifact weeks','3+ WW tests with written status','1+ tool adopted by teammate','Published POV that influenced a decision','One autonomous PS workflow'];
  var nextSteps=['Ship the Testing Approach doc outline this week.','Write status docs for OCI and ad copy test.','Finish campaign link generator. Ship to a teammate.','Publish AEO POV. Get it cited.','Convert morning routine to fully event-triggered.'];
  var fills=[35,15,0,0,0];
  var colors={ACTIVE:'#4da8da',NEXT:'#4b5563',QUEUED:'#374151',FUTURE:'#1f2230'};
  var h='';
  fiveLevels.forEach(function(lv,i){
    var c=colors[lv.status]||'#1f2230';
    var bc=lv.status==='ACTIVE'?'lb-active':lv.status==='NEXT'?'lb-next':lv.status==='QUEUED'?'lb-queued':'lb-future';
    h+='<div class="level-track"><div class="level-header"><span class="level-name">'+lv.level+'. '+lv.name+'</span>'+
      '<span style="color:var(--text3);font-size:.8em;margin-right:6px">'+fills[i]+'%</span><span class="lb '+bc+'">'+lv.status+'</span></div>'+
      '<div class="level-bar"><div class="level-fill" style="width:'+fills[i]+'%;background:'+c+'"></div></div>'+
      '<div style="font-size:.73em;color:var(--text3);margin-top:2px">Gate: '+gates[i]+'</div>';
    if(lv.status==='ACTIVE'||lv.status==='NEXT') h+='<div style="font-size:.73em;color:var(--accent);margin-top:2px">Next: '+nextSteps[i]+'</div>';
    h+='</div>';
  });
  el.innerHTML=h;
})();
(function(){
  var el=document.getElementById('challengeOverview');
  var items=challenge.items||[];
  var pct=Math.round(challenge.completed/Math.max(challenge.total,1)*100);
  var h='<div style="display:flex;justify-content:space-between;margin-bottom:6px"><span style="color:var(--text2);font-size:.85em">'+challenge.completed+'/'+challenge.total+' complete</span><span style="color:var(--white);font-weight:600">'+pct+'%</span></div>'+
    '<div style="height:4px;background:var(--surface2);border-radius:2px;margin-bottom:14px"><div style="height:100%;width:'+pct+'%;background:var(--accent);border-radius:2px"></div></div>';
  items.forEach(function(item){
    h+='<div class="ch-item"><div class="ch-box'+(item.done?' ch-done':'')+'">'+( item.done?'\\u2713':'')+'</div>'+
      '<span class="ch-text'+(item.done?' done':'')+'">'+item.text+'</span></div>';
  });
  el.innerHTML=h;
})();
</script>
'''
    html += shared_footer(now)
    return html


# ═══════════════════════════════════════════════════════════════
# PAGE: Growth (growth.html) &mdash; Autonomy & Competence
# ═══════════════════════════════════════════════════════════════

def build_growth(data, now):
    auto = data["autonomy"]; comp = data["competence"]
    human_count = auto["summary"].get("human",0)
    agent_count = auto["summary"].get("agent_human",0)
    agentic_count = auto["summary"].get("fully_agentic",0)
    html = shared_head("Growth &mdash; Body System", "growth.html")
    html += f'''
<h1>Autonomy and Competence</h1>
<div class="sub">Two dimensions of growth: how much of your work is agent-assisted (autonomy), and how automatic your operating principles have become (competence).</div>

<p style="color:var(--text);font-size:.9em;line-height:1.7;margin-bottom:16px">
  The end state is Level 5: full agentic orchestration of paid search work. Today, {auto["total"]} distinct work functions have been identified across campaign operations, reporting, strategic work, admin, communication, delegation, and system maintenance. Of those, {agentic_count} run without any human involvement, {agent_count} involve an agent but still need a human trigger or approval, and {human_count} are fully manual.
</p>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:32px">
  The biggest manual bucket is campaign operations &mdash; 9 functions including bid management, keyword research, search term review, and spend pacing. This is Level 3 territory: building tools that automate these tasks and getting teammates to adopt them. Strategic work (test design, OP1 writing, POVs) will likely stay human, but the preparation and data gathering that feeds it can be agent-assisted.
</p>

<h2>Work Classification</h2>
<div class="grid">
  <div class="card"><div class="card-title">Autonomy Spectrum</div><div class="chart-box"><canvas id="autoChart"></canvas></div></div>
  <div class="card"><div class="card-title">Breakdown by Category</div><div id="autoTable"></div>
    <div style="font-size:.72em;color:var(--text3);margin-top:8px;line-height:1.5">
      <b style="color:var(--accent)">Fully Agentic</b> Zero touch &middot; <b style="color:rgba(77,168,218,0.7)">Agent + Human</b> Agent works, human triggers &middot; <b style="color:var(--text2)">Delegated</b> Another human &middot; <b style="color:var(--text3)">Human</b> Manual
    </div>
    <div style="font-size:.58em;color:var(--text3);margin-top:4px;font-style:italic">{auto["confidence_note"]}</div>
  </div>
</div>

<h2>Full Inventory</h2>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:12px">
  Every function Richard performs, classified by who or what does it. The color dot indicates autonomy level. This inventory was built from device.md (tools and agents), hands.md (tasks and recurring work), current.md (active projects), and standard paid search marketing manager responsibilities.
</p>
<div class="card" id="autoBySection"></div>

<h2>Competence Stages</h2>
<p style="color:var(--text);font-size:.9em;line-height:1.7;margin-bottom:16px">
  Six operating principles drawn from Duhigg (habit loops), McKeown (essentialism), and Gollwitzer (implementation intentions). Each is scored on a 4-stage competence model: from unconscious incompetence (Stage 1, not even aware of the gap) through conscious competence (Stage 3, can do it but requires effort) to unconscious competence (Stage 4, automatic behavior).
</p>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:16px">
  The current average is {comp["average"]}/4. Four principles are at Stage 3 &mdash; the system actively checks alignment and the behavior happens with effort. Two are at Stage 2: "Invisible over visible" (system improvements are still noticeable rather than seamless) and "Reduce decisions, not options" (most templates are unbuilt, so decisions that could be pre-loaded still require active thought). The goal is Stage 4 across all six &mdash; when the checking becomes unnecessary because the behavior is automatic.
</p>
<div class="card">
  <div style="display:flex;justify-content:space-between;font-size:.7em;color:var(--text3);margin-bottom:10px">
    <span>Stage 1: Unconscious Incompetence</span>
    <span>Stage 2: Conscious Incompetence</span>
    <span>Stage 3: Conscious Competence</span>
    <span>Stage 4: Unconscious Competence</span>
  </div>
  <div id="compDisplay"></div>
</div>

<script>
var autonomy={json.dumps(data["autonomy"])};
var competence={json.dumps(data["competence"])};
var C={{accent:'#4da8da',accent60:'rgba(77,168,218,0.6)',accent30:'rgba(77,168,218,0.3)',accent12:'rgba(77,168,218,0.12)',neutral:'#8899aa',neutral30:'rgba(136,153,170,0.3)',alert:'#f87171',white:'#f0f4f8'}};
Chart.defaults.color='#8899aa';
Chart.defaults.plugins.tooltip.titleColor='#fff';
Chart.defaults.plugins.tooltip.bodyColor='#ccc';
</script>
'''
    html += f'''
<h2>Autonomy Spectrum &mdash; {data["autonomy"]["total"]} Work Functions Classified</h2>
<div class="grid">
  <div class="card"><div class="card-title">Work Classification</div><div class="chart-box"><canvas id="autoChart"></canvas></div></div>
  <div class="card"><div class="card-title">Breakdown by Category</div><div id="autoTable"></div>
    <div style="font-size:.72em;color:#888;margin-top:8px;line-height:1.5">
      <b style="color:var(--accent)">Fully Agentic</b> Zero touch &middot; <b style="color:var(--accent)">Agent + Human</b> Agent works, human triggers &middot; <b style="color:var(--text2)">Delegated</b> Another human &middot; <b style="color:var(--text3)">Human</b> Manual
    </div>
    <div style="font-size:.6em;color:#666;margin-top:4px;font-style:italic">{data["autonomy"]["confidence_note"]}</div>
  </div>
</div>
<div class="trainer">58% of your work is still fully manual. Campaign ops (9 functions) is the biggest bucket &mdash; that is Level 3 territory. Strategic work stays human, but prep can be agent-assisted. Every function that moves from red to blue is a step toward Level 5.</div>

<h2>Autonomy by Work Area</h2>
<div class="card" id="autoBySection"></div>

<h2>Competence Stages &mdash; Average {data["competence"]["average"]}/4</h2>
<div class="card">
  <div style="display:flex;justify-content:space-between;font-size:.7em;color:#888;margin-bottom:10px">
    <span style="color:#fca5a5">Stage 1: Unconscious Incompetence</span>
    <span style="color:#fcd34d">Stage 2: Conscious Incompetence</span>
    <span style="color:#93c5fd">Stage 3: Conscious Competence</span>
    <span style="color:#86efac">Stage 4: Unconscious Competence </span>
  </div>
  <div id="compDisplay"></div>
</div>
<div class="trainer">Two principles at Stage 2: "Invisible over visible" and "Reduce decisions." Building more templates and making the morning routine event-triggered would move both forward. Stage 4 is when the system checks become unnecessary &mdash; the behavior just happens.</div>

<script>
var autonomy={json.dumps(data["autonomy"])};
var competence={json.dumps(data["competence"])};
'''
    html += '''
// Doughnut with numerical labels
(function(){
  var s=autonomy.summary||{};
  var labels=['Fully Agentic','Agent + Human','Delegated','Human'];
  var data=[s.fully_agentic||0,s.agent_human||0,s.delegated||0,s.human||0];
  var colors=[C.accent,'#4da8da99',C.neutral,C.neutral30];
  new Chart(document.getElementById('autoChart'),{type:'doughnut',
    data:{labels:labels,datasets:[{data:data,backgroundColor:colors,borderColor:'#1a1d27',borderWidth:3}]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'bottom',labels:{color:'#888',font:{size:11},padding:12,
        generateLabels:function(chart){var ds=chart.data.datasets[0];var total=ds.data.reduce(function(a,b){return a+b},0);
          return chart.data.labels.map(function(label,i){return {text:label+' ('+ds.data[i]+', '+Math.round(ds.data[i]/total*100)+'%)',fillStyle:ds.backgroundColor[i],strokeStyle:ds.backgroundColor[i],fontColor:'#ccc',hidden:false,index:i}})}}},
        tooltip:{callbacks:{label:function(c){var total=c.dataset.data.reduce(function(a,b){return a+b},0);return c.label+': '+c.raw+' of '+total}}}}}});
  // Table
  var el=document.getElementById('autoTable');
  var cats=[{l:'Fully Agentic',k:'fully_agentic',c:C.accent},{l:'Agent + Human',k:'agent_human',c:'#4da8da99'},{l:'Delegated',k:'delegated',c:C.neutral},{l:'Human',k:'human',c:C.neutral30}];
  var total=autonomy.total||1;var funcs=autonomy.functions||[];
  var h='<table><tr><th>Category</th><th style="text-align:center">#</th><th>Examples</th></tr>';
  cats.forEach(function(cat){
    var count=s[cat.k]||0;var examples=funcs.filter(function(f){return f.category===cat.k}).map(function(f){return f.name}).slice(0,3).join(', ');
    h+='<tr><td style="color:'+cat.c+';font-weight:600;white-space:nowrap">'+cat.l+'</td><td style="text-align:center">'+count+'</td><td style="color:#888;font-size:.78em">'+examples+'</td></tr>';
  });
  el.innerHTML=h+'</table>';
})();
// By section
(function(){
  var el=document.getElementById('autoBySection');
  var funcs=autonomy.functions||[];
  var sections={};
  funcs.forEach(function(f){if(!sections[f.section])sections[f.section]=[];sections[f.section].push(f)});
  var catColors={fully_agentic:C.accent,agent_human:'#4da8da99',delegated:C.neutral,human:C.neutral30};
  var h='<table><tr><th>Area</th><th>Function</th><th>Status</th></tr>';
  Object.keys(sections).sort().forEach(function(sec){
    sections[sec].forEach(function(f,i){
      var c=catColors[f.category]||'#888';
      h+='<tr><td style="color:#888;font-size:.8em">'+(i===0?sec:'')+'</td><td>'+f.name+'</td>'+
        '<td><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:'+c+'"></span></td></tr>';
    });
  });
  el.innerHTML=h+'</table>';
})();
// Competence bars
(function(){
  var p=competence.principles||[];
  var el=document.getElementById('compDisplay');
  var stageFull=['Unconscious Incompetence','Conscious Incompetence','Conscious Competence','Unconscious Competence'];
  var stageColors=['rgba(136,153,170,0.2)','rgba(136,153,170,0.35)','rgba(77,168,218,0.4)','rgba(77,168,218,0.7)'];
  var h='';
  p.forEach(function(pr){
    h+='<div class="comp-row"><div class="comp-label"><span class="comp-name">'+pr.name+' <span style="color:#888;font-size:.8em;font-weight:400">('+pr.source+')</span></span>'+
      '<span class="comp-stage">Stage '+pr.score+'</span></div><div class="comp-track">';
    for(var i=0;i<4;i++){var filled=i<pr.score;h+='<div class="comp-stop'+(filled?' filled':'')+'" style="'+(filled?'background:'+stageColors[i]:'')+'"></div>';}
    h+='</div><div style="font-size:.73em;color:#888;margin-top:2px">'+pr.evidence+'</div></div>';
  });
  h+='<div style="margin-top:10px;padding:8px 12px;background:#12141c;border-radius:6px;display:flex;justify-content:space-between"><span style="font-size:.85em;color:#888">Average</span><span style="font-size:1.1em;font-weight:700;color:#fff">'+competence.average+' / 4</span></div>';
  el.innerHTML=h;
})();
</script>
'''
    html += shared_footer(now)
    return html


# ═══════════════════════════════════════════════════════════════
# PAGE: Willpower (willpower.html) &mdash; aMCC + Patterns
# ═══════════════════════════════════════════════════════════════

def build_willpower(data, now):
    amcc = data["amcc"]; patterns = data["patterns"]; ch = data["challenge"]
    worsening = sum(1 for p in patterns if p["trajectory"]=="WORSENING")
    stuck_count = sum(1 for p in patterns if p["trajectory"]=="STUCK")
    html = shared_head("Willpower &mdash; Body System", "willpower.html")
    html += f'''
<h1>Willpower and Patterns</h1>
<div class="sub">The gap between knowing and doing. The aMCC (anterior midcingulate cortex) grows when you do hard things you do not want to do, and atrophies when you choose comfort.</div>

<p style="color:var(--text);font-size:.9em;line-height:1.7;margin-bottom:16px">
  The streak measures consecutive days where Richard chose the hard thing over the comfortable thing. Right now it is at {amcc["streak"]} days, with {amcc["resets"]} total resets since tracking began on March 20. {len(amcc.get("resistance_types",[]))} distinct resistance types have been identified, each with a specific counter-reframe the system uses during live sessions.
</p>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:24px">
  The nervous system tracks behavioral patterns over time. {worsening} pattern{"s are" if worsening!=1 else " is"} currently worsening, {stuck_count} {"are" if stuck_count!=1 else "is"} stuck. When a pattern is stuck for 3+ weeks, the intervention is wrong. The system proposes structural fixes (changing defaults, building tools, removing friction) rather than relying on willpower.
</p>

<div class="stats">
  <div class="stat"><div class="v" style="color:{"var(--alert)" if amcc["streak"]==0 else "var(--accent)"}">{amcc["streak"]}</div><div class="l">Streak Days</div></div>
  <div class="stat"><div class="v">{amcc["longest"]}</div><div class="l">Longest</div></div>
  <div class="stat"><div class="v">{amcc["resets"]}</div><div class="l">Resets</div></div>
  <div class="stat"><div class="v">{len(amcc.get("resistance_types",[]))}</div><div class="l">Resistance Types</div></div>
  <div class="stat"><div class="v">{worsening}</div><div class="l">Worsening</div></div>
  <div class="stat"><div class="v">{stuck_count}</div><div class="l">Stuck</div></div>
</div>

<div class="card" style="margin-bottom:16px;padding:24px;text-align:center">
  <div style="font-size:.72em;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">The Hard Thing</div>
  <div style="font-size:1.1em;color:var(--accent);font-weight:500">{amcc.get("hard_thing","No hard thing set")}</div>
  <div style="font-size:.78em;color:var(--text3);margin-top:10px;max-width:600px;margin-left:auto;margin-right:auto">At any given time there is one hard thing. Not three. Not a prioritized list. One. The aMCC fires when you are about to choose the comfortable thing over this.</div>
</div>

<h2>30-Day Challenge</h2>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:12px">
  {ch["total"]} items due by {ch.get("deadline","TBD")}. A mix of strategic artifacts, system improvements, and operational cleanup. {ch["completed"]}/{ch["total"]} complete. The highest-leverage items are the Testing Approach doc and AI Max test design &mdash; they feed Level 1 and Level 2 simultaneously.
</p>
<div class="card" id="challengeList"></div>

<h2>Growth Model &mdash; Current vs Targets</h2>
<div class="grid">
  <div class="card" id="growthTable"></div>
  <div class="card"><div class="card-title">Resistance Taxonomy</div><div id="resistanceTable"></div>
    <div style="font-size:.72em;color:#888;margin-top:6px">Each resistance type has a counter &mdash; a reframe that makes the hard choice easier. The aMCC uses these during live sessions when avoidance is detected.</div>
  </div>
</div>

<h2>Pattern Trajectories</h2>
<div style="font-size:.72em;color:var(--text3);margin-bottom:8px">
  Each pattern is scored on a -2 to +1 scale. The bar shows direction: left is worsening, right is improving. Weeks shows how long the pattern has been tracked.
</div>
<div class="card" id="patternTable"></div>
<div class="trainer" id="patternTrainer"></div>

<script>
var amcc={json.dumps(amcc)};
var patterns={json.dumps(patterns)};
var challenge={json.dumps(ch)};
'''
    html += '''
// Challenge
(function(){
  var el=document.getElementById('challengeList');
  var items=challenge.items||[];
  var pct=Math.round(challenge.completed/Math.max(challenge.total,1)*100);
  var h='<div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-size:.85em;color:#888">Progress</span><span style="font-weight:700;color:#fff">'+pct+'%</span></div>'+
    '<div style="height:6px;background:#1f2230;border-radius:3px;margin-bottom:12px"><div style="height:100%;width:'+pct+'%;background:var(--accent);border-radius:3px"></div></div>';
  items.forEach(function(item){
    h+='<div class="ch-item"><div class="ch-box'+(item.done?' ch-done':'')+'">'+( item.done?'\\u2713':'')+'</div><span class="ch-text'+(item.done?' done':'')+'">'+item.text+'</span></div>';
  });
  el.innerHTML=h;
})();
// Growth
(function(){
  var el=document.getElementById('growthTable');
  var gm=amcc.growth_model||[];
  if(!gm.length){el.innerHTML='<div class="no-data">No data</div>';return;}
  var h='<div class="card-title">Growth Metrics</div><table><tr><th>Metric</th><th>Current</th><th>30d Target</th><th>90d Target</th></tr>';
  gm.forEach(function(r){h+='<tr><td>'+r.metric+'</td><td style="color:#fff;font-weight:600">'+r.current+'</td><td style="color:#888">'+r.target_30d+'</td><td style="color:#666">'+r.target_90d+'</td></tr>';});
  el.innerHTML=h+'</table><div style="font-size:.72em;color:#888;margin-top:6px">The aMCC grows with sustained effort and atrophies with avoidance. Stage 4 (unconscious competence) is when these metrics hit their 90d targets and stay there.</div>';
})();
// Resistance
(function(){
  var el=document.getElementById('resistanceTable');
  var rt=amcc.resistance_types||[];
  if(!rt.length){el.innerHTML='<div class="no-data">No data</div>';return;}
  var h='<table><tr><th>Type</th><th>Counter</th></tr>';
  rt.forEach(function(r){h+='<tr><td style="font-weight:600;font-size:.85em">'+r.type+'</td><td style="color:#888;font-size:.82em">'+r.counter+'</td></tr>';});
  el.innerHTML=h+'</table>';
})();
// Patterns &mdash; numeric scale with directional bars
(function(){
  var el=document.getElementById('patternTable');
  if(!patterns.length){el.innerHTML='<div class="no-data">No patterns</div>';return;}
  var scores={'WORSENING':-2,'STUCK':-1,'NEW':0,'ACTIVE':0,'IMPROVING':1,'VALIDATED':1};
  var h='<table><tr><th>Pattern</th><th style="text-align:center;width:60px">Weeks</th><th style="text-align:center;width:180px">Trend</th><th>Assessment</th></tr>';
  patterns.forEach(function(p){
    var traj=p.trajectory!=='\\u2014'?p.trajectory:p.status;
    var score=scores[traj]!==undefined?scores[traj]:0;
    // Build centered directional bar
    var barLeft='',barRight='';
    if(score<0){
      var w=Math.abs(score)*40;
      barLeft='<div style="position:absolute;right:50%;height:100%;width:'+w+'px;background:rgba(248,113,113,0.4);border-radius:2px 0 0 2px"></div>';
    } else if(score>0){
      var w=score*40;
      barRight='<div style="position:absolute;left:50%;height:100%;width:'+w+'px;background:rgba(77,168,218,0.5);border-radius:0 2px 2px 0"></div>';
    }
    var scoreColor=score<0?'#f87171':score>0?'var(--accent)':'var(--text3)';
    h+='<tr><td style="font-weight:500">'+p.name+'</td>'+
      '<td style="text-align:center;color:var(--text3)">'+p.weeks+'</td>'+
      '<td><div style="position:relative;height:16px;background:var(--surface2);border-radius:2px;overflow:hidden">'+
        '<div style="position:absolute;left:50%;top:0;bottom:0;width:1px;background:var(--border2)"></div>'+
        barLeft+barRight+
      '</div><div style="text-align:center;font-size:.65em;color:'+scoreColor+';margin-top:2px">'+
        (score>0?'+':'')+score+
      '</div></td>'+
      '<td style="color:var(--text2);font-size:.8em">'+(p.assessment||'\\u2014')+'</td></tr>';
  });
  el.innerHTML=h+'</table>';
  var w=patterns.filter(function(p){return p.trajectory==='WORSENING'});
  var s=patterns.filter(function(p){return p.trajectory==='STUCK'});
  var note='';
  if(w.length) note+=w.length+' pattern(s) at -2 (worsening). These need structural intervention, not more willpower. ';
  if(s.length>1) note+=s.length+' pattern(s) at -1 (stuck). Same approach for 3+ weeks without movement means the approach is wrong.';
  if(!note) note='All patterns at 0 or above. Stable.';
  document.getElementById('patternTrainer').textContent=note;
})();
</script>
'''
    html += shared_footer(now)
    return html


# ═══════════════════════════════════════════════════════════════
# PAGE: Output (output.html) &mdash; Weekly Scorecard + Low-leverage
# ═══════════════════════════════════════════════════════════════

def build_output(data, now):
    sc = data["scorecard"]; fl = data["five_levels"]
    total_artifacts = sum(w["artifacts"] for w in sc)
    total_tools = sum(w["tools"] for w in sc)
    total_low_lev = sum(w["low_leverage_hours"] for w in sc)
    zero_weeks = sum(1 for w in sc if w["artifacts"]==0)
    html = shared_head("Output &mdash; Body System", "output.html")
    html += f'''
<h1>Weekly Output</h1>
<div class="sub">What you shipped, what you built, and where your time went. This is the evidence layer for the Five Levels.</div>

<p style="color:var(--text);font-size:.9em;line-height:1.7;margin-bottom:16px">
  The standard is simple: every week, at least one strategic artifact. Every month, at least one tool or automation. Every quarter, at least one initiative that changes how the team operates. These map directly to the Five Levels &mdash; artifacts prove Level 1 consistency, tools advance Level 3 adoption, and initiatives build toward Level 5 orchestration.
</p>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:24px">
  Across {len(sc)} tracked weeks: {total_artifacts} artifacts shipped, {total_tools} tools built, ~{total_low_lev} hours spent on low-leverage work. {"Every tracked week has zero artifacts &mdash; this is the #1 pattern to break. The Annual Review confirmed it: visibility is the gap, and artifacts are how you close it. The Testing Approach doc for Kate is the convergence point." if zero_weeks==len(sc) and len(sc)>0 else "Tracking in progress."} Low-leverage work includes invoice/PO coordination, manual campaign link updates, reactive deep dives, meetings without clear output, and manual budget spreadsheets. Each hour there is an hour not spent on the hard thing.
</p>

<h2>Weekly Scorecard</h2>
<div class="card"><div class="chart-box"><canvas id="scChart"></canvas></div>
  <div style="font-size:.75em;color:var(--text3);margin-top:8px;line-height:1.5">
    <b style="color:var(--accent)">Artifacts</b> Strategic docs, frameworks, test designs, POVs published that week. Target: 1/week. This is the Level 1 gate metric. &middot;
    <b style="color:rgba(77,168,218,0.7)">Tools</b> Automations or tools completed and usable by Richard or teammates. Target: 1/month. Level 3 gate metric. &middot;
    <b style="color:var(--text2)">Low-Leverage Hours</b> Time on work that does not advance the Five Levels. Target: under 5 hours/week.
  </div>
</div>

<h2>Five Levels</h2>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:12px">
  Sequential. Each level funds the next. You can do work at multiple levels simultaneously, but you do not graduate until the gate is met. The aMCC tracks Level 1 progress via the streak. The nervous system tracks all levels via calibration loops.
</p>
<div class="card" id="levelsDisplay"></div>

<h2>Low-Leverage Patterns</h2>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:12px">
  Recurring time traps identified by the trainer. Each has been observed for multiple weeks. The fix column shows the structural intervention &mdash; not "try harder" but "change the default." The signal column is what the trainer says when this pattern appears.
</p>
<div class="card" id="lowLevTable"></div>

<script>
var scorecard={json.dumps(sc)};
var fiveLevels={json.dumps(fl)};
var C={{accent:'#4da8da',accent60:'rgba(77,168,218,0.6)',accent30:'rgba(77,168,218,0.3)',neutral:'#8899aa',alert:'#f87171',white:'#f0f4f8'}};
Chart.defaults.color='#8899aa';
var cDef={{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{labels:{{color:'#888',font:{{size:11}}}}}}}},scales:{{x:{{ticks:{{color:'#666'}},grid:{{color:'#1f2230'}}}},y:{{ticks:{{color:'#666'}},grid:{{color:'#1f2230'}}}}}}}};
if(scorecard.length){{
  new Chart(document.getElementById('scChart'),{{type:'bar',data:{{labels:scorecard.map(function(w){{return w.week}}),datasets:[
    {{label:'Artifacts',data:scorecard.map(function(w){{return w.artifacts}}),backgroundColor:C.purple,borderRadius:4}},
    {{label:'Tools',data:scorecard.map(function(w){{return w.tools}}),backgroundColor:C.cyan,borderRadius:4}},
    {{label:'Low-Lev Hrs',data:scorecard.map(function(w){{return w.low_leverage_hours}}),backgroundColor:C.amber,borderRadius:4}}
  ]}},options:cDef}});
}}
'''
    html += '''
// Levels
(function(){
  var el=document.getElementById('levelsDisplay');
  var gates=['4 consecutive artifact weeks','3+ WW tests with written status','1+ tool adopted by teammate','Published POV that influenced a decision','One autonomous PS workflow'];
  var nextSteps=['Ship the Testing Approach doc outline this week.','Write status docs for OCI + ad copy test.','Finish campaign link generator. Ship to a teammate.','Publish AEO POV. Get it cited.','Convert morning routine to fully event-triggered.'];
  var fills=[35,15,0,0,0];
  var colors={ACTIVE:'#4da8da',NEXT:'#4b5563',QUEUED:'#374151',FUTURE:'#1f2230'};
  var h='';
  fiveLevels.forEach(function(lv,i){
    var c=colors[lv.status]||'#1f2230';
    var bc=lv.status==='ACTIVE'?'lb-active':lv.status==='NEXT'?'lb-next':lv.status==='QUEUED'?'lb-queued':'lb-future';
    h+='<div class="level-track"><div class="level-header"><span class="level-name">'+lv.level+'. '+lv.name+'</span>'+
      '<span style="color:#888;font-size:.8em;margin-right:6px">'+fills[i]+'%</span><span class="lb '+bc+'">'+lv.status+'</span></div>'+
      '<div class="level-bar"><div class="level-fill" style="width:'+fills[i]+'%;background:'+c+'"></div></div>'+
      '<div style="font-size:.73em;color:#666;margin-top:2px">'+lv.description+'</div>'+
      '<div style="font-size:.73em;color:#888;margin-top:1px;font-style:italic">Gate: '+gates[i]+'</div>';
    if(lv.status==='ACTIVE'||lv.status==='NEXT') h+='<div style="font-size:.73em;color:var(--accent);margin-top:2px">'+nextSteps[i]+'</div>';
    h+='</div>';
  });
  el.innerHTML=h;
})();
// Low-leverage
(function(){
  var el=document.getElementById('lowLevTable');
  var traps=[
    {name:'Invoice/PO coordination',weeks:'4+',fix:'Delegate + process doc',signal:'$0 career value'},
    {name:'Manual campaign link updates',weeks:'3',fix:'Build generator tool',signal:'Automate or template'},
    {name:'Reactive deep dives',weeks:'2',fix:'Self-service dashboard',signal:'Do once, then automate'},
    {name:'Meetings without clear output',weeks:'3+',fix:'Audit + decline or prep',signal:"What is your deliverable?"},
    {name:'Manual budget spreadsheets',weeks:'recurring',fix:'Timebox or build helper',signal:'Cap at 30 min'},
    {name:'Admin backlog not clearing',weeks:'3',fix:'Batch and timebox (40 min)',signal:'PAM PO is 24 days overdue'}
  ];
  var h='<table><tr><th>Time Trap</th><th style="text-align:center">Weeks</th><th>Fix</th><th>Signal</th></tr>';
  traps.forEach(function(t){
    h+='<tr><td style="font-weight:500">'+t.name+'</td><td style="color:#888;text-align:center">'+t.weeks+'</td><td style="color:#888;font-size:.82em">'+t.fix+'</td><td style="color:#666;font-size:.78em;font-style:italic">'+t.signal+'</td></tr>';
  });
  el.innerHTML=h+'</table>';
})();
</script>
'''
    html += shared_footer(now)
    return html


# ═══════════════════════════════════════════════════════════════
# PAGE: Autoresearch (autoresearch.html)
# ═══════════════════════════════════════════════════════════════

def build_autoresearch(data, now):
    budgets = data["budgets"]; cl = data["changelog"]; staleness = data["staleness"]; eq = data["exp_queue"]
    ta = sum(b["actual"] for b in budgets); tb = sum(b["budget"] for b in budgets)
    adopted = sum(1 for e in cl["experiments"] if e["status"]=="ADOPTED")
    reverted = sum(1 for e in cl["experiments"] if e["status"]=="REVERTED")
    total_saved = sum(s["saved"] for s in cl["savings"])
    stale_count = sum(1 for s in staleness if s["days_stale"]>3)
    over_budget = sum(1 for b in budgets if b["utilization"]>100)
    budget_note = "All organs are currently within budget." if over_budget==0 else f"{over_budget} organ(s) over budget; compression experiments are queued."
    util_pct = round(ta/max(tb,1)*100)
    html = shared_head("Autoresearch &mdash; Body System", "autoresearch.html")
    html += f'''
<h1>Autoresearch Engine</h1>
<div class="sub">How the body system maintains itself. Inspired by Karpathy&#39;s autoresearch: 630 lines, 700 experiments, measurable results. Small, fast, autonomous, compounding.</div>

<p style="color:var(--text);font-size:.9em;line-height:1.7;margin-bottom:16px">
  The body is an 11-organ system that holds context, makes decisions, tracks patterns, and enforces willpower. Each organ is a self-contained markdown file with a word budget enforced by the gut. The autoresearch loop runs experiments on these organs autonomously &mdash; snapshot the current state, apply a modification (compress, add, restructure, remove, reword, merge, or split), evaluate with two independent blind subagents, and keep or revert based on accuracy and completeness scores.
</p>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:16px">
  The primary metric is usefulness per token: does the organ answer the questions it is supposed to answer, accurately and self-containedly, without requiring additional file reads? Word count is a constraint (ceiling), not an objective. An organ at 95% of budget that answers everything correctly is fine. An organ at 50% that misses questions needs content added, not celebrated for being small.
</p>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:24px">
  After {len(cl["runs"])} loop runs, the system has run {adopted + reverted} experiments with a {round(adopted/max(adopted+reverted,1)*100)}% keep rate. {total_saved:,} words have been saved through compression while maintaining accuracy thresholds (100% for Brain and Memory, 95% for Eyes and Hands, 90% for all others). The body currently holds {ta:,} words against a {tb:,}-word ceiling, leaving {tb-ta:,} words of headroom for future content.
</p>

<div class="stats">
  <div class="stat"><div class="v">{ta:,}w</div><div class="l">Body Mass</div></div>
  <div class="stat"><div class="v">{tb:,}w</div><div class="l">Ceiling</div></div>
  <div class="stat"><div class="v">{round(ta/max(tb,1)*100)}%</div><div class="l">Utilization</div></div>
  <div class="stat"><div class="v">{over_budget}</div><div class="l">Over Budget</div></div>
  <div class="stat"><div class="v">{len(cl["runs"])}</div><div class="l">Loop Runs</div></div>
  <div class="stat"><div class="v">{adopted}/{adopted+reverted}</div><div class="l">Kept / Total</div></div>
  <div class="stat"><div class="v">{round(adopted/max(adopted+reverted,1)*100)}%</div><div class="l">Keep Rate</div></div>
  <div class="stat"><div class="v">{total_saved:,}w</div><div class="l">Words Saved</div></div>
<h2>Organ Word Budgets</h2>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:12px">
  {budget_note} The total body budget is {tb:,}w with a hard ceiling of 24,000 words. Current utilization is {util_pct} percent.
</p>
<div class="grid">
  <div class="card"><div class="chart-box"><canvas id="budgetChart"></canvas></div></div>
  <div class="card"><div class="card-title">Budget Details</div><div id="budgetTable"></div></div>
</div>

<h2>Experiment History</h2>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:12px">
  Every experiment follows the same protocol: select a target organ, snapshot it, apply a technique, evaluate with dual blind subagents (one with full system context, one generic), and keep or revert. The compressing agent never evaluates its own work. {adopted} experiments have been adopted so far. {"The perfect keep rate suggests the experiments could be more aggressive &mdash; pushing closer to accuracy thresholds rather than staying safe." if reverted==0 and adopted>0 else ""} {len(eq)} experiments are queued for future runs.
</p>
<div class="grid">
  <div class="card"><div class="card-title">Word Savings per Experiment</div><div class="chart-box"><canvas id="savingsChart"></canvas></div></div>
  <div class="card">
    <div class="card-title">Experiment Log</div><div id="expTable"></div>
    <div class="card-title" style="margin-top:16px">Queue</div><div id="queueTable"></div>
  </div>
</div>

<h2>Organ Freshness</h2>
<p style="color:var(--text2);font-size:.85em;line-height:1.7;margin-bottom:12px">
  {"All organs have been updated within the last 3 days." if stale_count==0 else str(stale_count)+" organ(s) are more than 3 days stale and should be refreshed in the next loop run."} The staleness threshold is 7 days &mdash; any section older than that gets flagged in the daily brief. The morning routine handles maintenance; the autoresearch loop handles experiments.
</p>
<div class="card"><div class="chart-box-sm"><canvas id="stalenessChart"></canvas></div></div>

<script>
var budgets={json.dumps(budgets)};
var changelog={json.dumps(cl)};
var staleness={json.dumps(staleness)};

var expQueue={json.dumps(eq)};
var C={{accent:'#4da8da',accent60:'rgba(77,168,218,0.6)',accent30:'rgba(77,168,218,0.3)',accent12:'rgba(77,168,218,0.12)',neutral:'#8899aa',neutral30:'rgba(136,153,170,0.3)',alert:'#f87171',white:'#f0f4f8'}};
Chart.defaults.color='#8899aa';
var cDef={{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{labels:{{color:'#888',font:{{size:11}}}}}}}},scales:{{x:{{ticks:{{color:'#666'}},grid:{{color:'#1f2230'}}}},y:{{ticks:{{color:'#666'}},grid:{{color:'#1f2230'}}}}}}}};
'''
    html += '''
// Budget chart
if(budgets.length){
  new Chart(document.getElementById('budgetChart'),{type:'bar',
    data:{labels:budgets.map(function(b){return b.organ}),datasets:[
      {label:'Actual',data:budgets.map(function(b){return b.actual}),backgroundColor:budgets.map(function(b){return b.utilization>100?C.alert:C.accent}),borderRadius:4},
      {label:'Budget',data:budgets.map(function(b){return b.budget}),backgroundColor:'rgba(255,255,255,0.06)',borderRadius:4}
    ]},options:{...cDef,indexAxis:'y',plugins:{...cDef.plugins,tooltip:{callbacks:{label:function(c){return c.dataset.label+': '+c.raw.toLocaleString()+'w'}}}}}});
}
// Budget table
(function(){
  var el=document.getElementById('budgetTable');
  var h='<table><tr><th>Organ</th><th style="text-align:right">Actual</th><th style="text-align:right">Budget</th><th style="text-align:right">%</th></tr>';
  budgets.forEach(function(b){
    var color=b.utilization>100?C.alert:b.utilization>90?C.neutral:C.neutral;
    h+='<tr><td>'+b.organ+'</td><td style="text-align:right">'+b.actual.toLocaleString()+'w</td><td style="text-align:right;color:#666">'+b.budget.toLocaleString()+'w</td><td style="text-align:right;color:'+color+';font-weight:600">'+b.utilization+'%</td></tr>';
  });
  var ta=budgets.reduce(function(s,b){return s+b.actual},0);
  var tb=budgets.reduce(function(s,b){return s+b.budget},0);
  h+='<tr style="border-top:2px solid #2a2d37"><td style="font-weight:700">Total</td><td style="text-align:right;font-weight:700">'+ta.toLocaleString()+'w</td><td style="text-align:right;color:#666">'+tb.toLocaleString()+'w</td><td style="text-align:right;font-weight:700">'+Math.round(ta/tb*100)+'%</td></tr>';
  el.innerHTML=h+'</table>';
})();
// Savings
(function(){
  var s=changelog.savings||[];
  if(!s.length){document.getElementById('savingsChart').parentElement.innerHTML='<div class="no-data">No savings yet</div>';return;}
  new Chart(document.getElementById('savingsChart'),{type:'bar',
    data:{labels:s.map(function(_,i){return 'Exp '+(i+1)}),datasets:[
      {label:'Before',data:s.map(function(x){return x.before}),backgroundColor:'rgba(255,255,255,0.06)',borderRadius:4},
      {label:'After',data:s.map(function(x){return x.after}),backgroundColor:C.accent,borderRadius:4}
    ]},options:{...cDef,plugins:{...cDef.plugins,tooltip:{callbacks:{label:function(c){return c.dataset.label+': '+c.raw.toLocaleString()+'w'}}}}}});
})();
// Exp table
(function(){
  var el=document.getElementById('expTable');
  var exps=changelog.experiments||[];
  if(!exps.length){el.innerHTML='<div class="no-data">No experiments</div>';return;}
  var bc={ADOPTED:'b-adopted',REVERTED:'b-reverted',QUEUED:'b-queued'};
  var h='<table><tr><th>CE</th><th>Status</th></tr>';
  exps.forEach(function(e){h+='<tr><td>CE-'+e.id+'</td><td><span class="badge '+(bc[e.status]||'b-queued')+'">'+e.status+'</span></td></tr>';});
  el.innerHTML=h+'</table>';
})();
// Queue
(function(){
  var el=document.getElementById('queueTable');
  if(!expQueue.length){el.innerHTML='<div class="no-data">Queue empty</div>';return;}
  var h='<table><tr><th>CE</th><th>Name</th></tr>';
  expQueue.forEach(function(e){h+='<tr><td>CE-'+e.id+'</td><td style="font-size:.85em">'+e.name+'</td></tr>';});
  el.innerHTML=h+'</table>';
})();
// Staleness
(function(){
  if(!staleness.length)return;
  var colors=staleness.map(function(s){return s.days_stale<=1?C.accent:s.days_stale<=3?C.neutral:C.alert});
  new Chart(document.getElementById('stalenessChart'),{type:'bar',
    data:{labels:staleness.map(function(s){return s.organ}),datasets:[
      {label:'Days',data:staleness.map(function(s){return Math.max(s.days_stale,0)}),backgroundColor:colors,borderRadius:4}
    ]},options:{...cDef,indexAxis:'y',scales:{...cDef.scales,x:{...cDef.scales.x,max:Math.max.apply(null,staleness.map(function(s){return s.days_stale}))+2}},
      plugins:{...cDef.plugins,legend:{display:false},tooltip:{callbacks:{label:function(c){return 'Updated: '+staleness[c.dataIndex].updated}}}}}});
})();
</script>
'''
    html += shared_footer(now)
    return html


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Generate body system dashboard mini-site")
    parser.add_argument("--output-dir", "-o", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    print("Parsing data sources...")
    data = {
        "budgets": parse_gut_budgets(),
        "changelog": parse_changelog(),
        "scorecard": parse_tracker_scorecard(),
        "patterns": parse_patterns(),
        "amcc": parse_amcc(),
        "five_levels": parse_five_levels(),
        "staleness": parse_organ_staleness(),
        "exp_queue": parse_experiment_queue(),
        "challenge": parse_thirty_day_challenge(),
        "autonomy": parse_autonomy_spectrum(),
        "competence": parse_competence_stages(),
    }
    for k, v in data.items():
        if isinstance(v, list): print(f"  {k}: {len(v)} items")
        elif isinstance(v, dict) and "total" in v: print(f"  {k}: {v['total']} items")
        elif isinstance(v, dict): print(f"  {k}: {len(v)} keys")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    os.makedirs(args.output_dir, exist_ok=True)

    pages = {
        "index.html": build_overview(data, now),
        "growth.html": build_growth(data, now),
        "willpower.html": build_willpower(data, now),
        "output.html": build_output(data, now),
        "autoresearch.html": build_autoresearch(data, now),
    }

    for filename, html in pages.items():
        path = os.path.join(args.output_dir, filename)
        with open(path, "w") as f:
            f.write(html)
        print(f"  {filename}: {len(html):,} bytes")

    print(f"\nSite generated: {args.output_dir}/")
    print(f"Open {args.output_dir}/index.html to start.")


if __name__ == "__main__":
    main()
