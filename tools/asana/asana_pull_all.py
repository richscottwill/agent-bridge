#!/usr/bin/env python3
"""Pull all tasks from Asana projects via enterprise-asana-mcp, output JSON."""
import json, subprocess, sys, time, os

MCP = os.path.expanduser("~/.toolbox/bin/enterprise-asana-mcp")

PROJECTS = [
    ("1213917352480610", "ABPS AI Content"),
    ("1212762061512767", "AU"),
    ("1212775592612917", "MX"),
    ("1205997667578893", "WW Testing"),
    ("1206011235630048", "WW Acquisition"),
    ("1205997667578886", "Paid App"),
    ("1213379551525587", "ABPS AI Build"),
]

OPT = "name,due_on,start_on,completed,completed_at,assignee.gid,custom_fields.gid,custom_fields.name,custom_fields.display_value,custom_fields.enum_value.name,custom_fields.date_value,custom_fields.text_value,projects.name,projects.gid,memberships.section.name,notes,permalink_url"

CORE_FIELDS = {
    "1213608836755502": "routine_rw",
    "1212905889837829": "priority_rw",
    "1212905889837865": "importance_rw",
    "1213915851848087": "kiro_rw",
    "1213921400039514": "next_action_rw",
    "1213440376528542": "begin_date_rw",
}

ROUTINE_MAP = {
    "Sweep (Low-friction)": "Sweep",
    "Core Two (Deep Work)": "Core",
    "Engine Room (Excel and Google ads)": "Engine Room",
    "Admin (Wind-down)": "Admin",
    "Wiki": "Wiki",
}

def call_mcp(tool, args):
    req = json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call",
                       "params":{"name":tool,"arguments":args}})
    # Write to temp file to avoid shell escaping issues
    with open("/tmp/_asana_req.json","w") as f:
        f.write(req)
    try:
        p = subprocess.run(
            ["bash","-c",f"cat /tmp/_asana_req.json | timeout 90 {MCP} 2>/dev/null"],
            capture_output=True, text=True, timeout=100)
        if not p.stdout.strip():
            return None
        resp = json.loads(p.stdout.strip())
        content = resp.get("result",{}).get("content",[])
        if content:
            text = content[0].get("text","")
            try:
                return json.loads(text)
            except:
                return text
        return None
    except Exception as e:
        print(f"ERR {tool}: {e}", file=sys.stderr)
        return None

def parse_task(t, fallback_project_name, fallback_project_gid):
    gid = t.get("gid","")
    if not gid:
        return None
    assignee = t.get("assignee")
    a_gid = assignee.get("gid","") if isinstance(assignee, dict) else ""
    projects = t.get("projects",[])
    pname = projects[0].get("name","") if projects else fallback_project_name
    pgid = projects[0].get("gid","") if projects else fallback_project_gid
    memberships = t.get("memberships",[])
    section = None
    for m in memberships:
        s = m.get("section",{})
        if s and s.get("name"):
            section = s["name"]
            break
    core = {}
    flex = {}
    for cf in t.get("custom_fields",[]):
        cfgid = cf.get("gid","")
        if cfgid in CORE_FIELDS:
            col = CORE_FIELDS[cfgid]
            if col in ("routine_rw","priority_rw","importance_rw"):
                ev = cf.get("enum_value")
                if ev and isinstance(ev, dict) and ev.get("name"):
                    nm = ev["name"]
                    core[col] = ROUTINE_MAP.get(nm, nm) if col == "routine_rw" else nm
                else:
                    core[col] = None
            elif col in ("kiro_rw","next_action_rw"):
                core[col] = cf.get("text_value") or None
            elif col == "begin_date_rw":
                dv = cf.get("date_value")
                if dv and isinstance(dv, dict):
                    core[col] = dv.get("date")
                else:
                    core[col] = None
        else:
            dv = cf.get("display_value")
            if dv:
                flex[cfgid] = {"name": cf.get("name",""), "value": dv}
    return {
        "task_gid": gid, "name": t.get("name",""),
        "assignee_gid": a_gid, "project_name": pname, "project_gid": pgid,
        "section_name": section,
        "due_on": t.get("due_on"), "start_on": t.get("start_on"),
        "completed": t.get("completed", False),
        "completed_at": t.get("completed_at"),
        "routine_rw": core.get("routine_rw"),
        "priority_rw": core.get("priority_rw"),
        "importance_rw": core.get("importance_rw"),
        "kiro_rw": core.get("kiro_rw"),
        "next_action_rw": core.get("next_action_rw"),
        "begin_date_rw": core.get("begin_date_rw"),
        "flex_fields": flex if flex else None,
        "notes": (t.get("notes","") or "")[:200],
        "permalink_url": t.get("permalink_url",""),
    }

all_tasks = {}
for pgid, pname in PROJECTS:
    print(f"Pulling {pname}...", file=sys.stderr)
    result = call_mcp("asana___GetTasksFromProject", {"project_gid": pgid, "opt_fields": OPT})
    if not result:
        print(f"  FAILED", file=sys.stderr)
        continue
    items = result if isinstance(result, list) else result.get("data",[])
    if not isinstance(items, list):
        print(f"  Unexpected: {type(items)}", file=sys.stderr)
        continue
    added = 0
    for t in items:
        if t.get("completed", False):
            continue
        row = parse_task(t, pname, pgid)
        if row and row["task_gid"] not in all_tasks:
            all_tasks[row["task_gid"]] = row
            added += 1
    print(f"  +{added} incomplete (total: {len(all_tasks)})", file=sys.stderr)
    time.sleep(0.3)

# Also try SearchTasksInWorkspace for any tasks not in projects
print("Searching Richard's assignments...", file=sys.stderr)
search = call_mcp("asana___SearchTasksInWorkspace", {
    "assignee_any": "1212732742544167", "completed": "false", "sort_by": "due_date"
})
if search:
    items = search if isinstance(search, list) else search.get("data",[])
    if isinstance(items, list) and items:
        print(f"  Search found {len(items)} tasks, fetching details for new ones...", file=sys.stderr)
        new_gids = [t.get("gid","") for t in items if t.get("gid","") not in all_tasks]
        print(f"  {len(new_gids)} not yet in our set", file=sys.stderr)
        for i, tgid in enumerate(new_gids[:30]):
            detail = call_mcp("asana___GetTaskDetails", {"task_gid": tgid, "opt_fields": OPT})
            if detail:
                td = detail.get("data", detail) if isinstance(detail, dict) else detail
                if isinstance(td, dict) and not td.get("completed", False):
                    row = parse_task(td, None, None)
                    if row:
                        all_tasks[row["task_gid"]] = row
            if (i+1) % 10 == 0:
                time.sleep(0.5)
    else:
        print(f"  Search returned 0 tasks", file=sys.stderr)
else:
    print(f"  Search failed", file=sys.stderr)

print(f"\nTotal: {len(all_tasks)} unique incomplete tasks", file=sys.stderr)
json.dump(list(all_tasks.values()), sys.stdout, indent=2, default=str)
