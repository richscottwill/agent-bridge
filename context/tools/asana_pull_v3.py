#!/usr/bin/env python3
"""Pull all tasks from Asana projects one at a time, merge, output JSON."""
import json, subprocess, sys, time

OPT = "name,due_on,start_on,completed,completed_at,assignee.gid,custom_fields.gid,custom_fields.name,custom_fields.display_value,custom_fields.enum_value.name,custom_fields.date_value,custom_fields.text_value,projects.name,projects.gid,memberships.section.name,notes,permalink_url"

PROJECTS = [
    ("1213917352480610", "ABPS AI Content"),
    ("1212762061512767", "AU"),
    ("1212775592612917", "MX"),
    ("1205997667578893", "WW Testing"),
    ("1206011235630048", "WW Acquisition"),
    ("1205997667578886", "Paid App"),
    ("1213379551525587", "ABPS AI Build"),
]

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

def single_mcp_call(tool, args):
    init = json.dumps({"jsonrpc":"2.0","id":0,"method":"initialize",
        "params":{"protocolVersion":"2024-11-05","capabilities":{},
                  "clientInfo":{"name":"sync","version":"1.0"}}})
    call = json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":tool,"arguments":args}})
    try:
        p = subprocess.run(["enterprise-asana-mcp"], input=init+"\n"+call+"\n",
                           capture_output=True, text=True, timeout=90)
        for line in p.stdout.strip().split("\n"):
            try:
                resp = json.loads(line)
                if resp.get("id") == 1:
                    content = resp.get("result",{}).get("content",[])
                    if content:
                        text = content[0].get("text","")
                        try:
                            return json.loads(text)
                        except:
                            return {"error": text[:300]}
            except:
                pass
    except Exception as e:
        return {"error": str(e)}
    return None

def parse_task(t, fb_pname, fb_pgid):
    gid = t.get("gid","")
    if not gid:
        return None
    assignee = t.get("assignee")
    a_gid = assignee.get("gid","") if isinstance(assignee, dict) else ""
    projects = t.get("projects",[])
    pname = projects[0].get("name","") if projects else fb_pname
    pgid = projects[0].get("gid","") if projects else fb_pgid
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
                core[col] = dv.get("date") if dv and isinstance(dv, dict) else None
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
        "flex_fields": json.dumps(flex) if flex else None,
    }

all_tasks = {}

for pgid, pname in PROJECTS:
    print(f"Pulling {pname} ({pgid})...", file=sys.stderr)
    result = single_mcp_call("asana___GetTasksFromProject", {"project_gid": pgid, "opt_fields": OPT})
    if not result:
        print(f"  NULL response", file=sys.stderr)
        continue
    if isinstance(result, dict) and "error" in result:
        print(f"  ERROR: {result['error'][:150]}", file=sys.stderr)
        continue
    items = result if isinstance(result, list) else result.get("data", [])
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
    time.sleep(1)

# Search for Richard's tasks not in any project
print(f"\nSearching Richard's assignments...", file=sys.stderr)
search = single_mcp_call("asana___SearchTasksInWorkspace", {
    "assignee_any": "1212732742544167", "completed": "false", "sort_by": "due_date"
})
if search and not (isinstance(search, dict) and "error" in search):
    items = search if isinstance(search, list) else search.get("data", [])
    if isinstance(items, list):
        new_gids = [t["gid"] for t in items if t.get("gid") and t["gid"] not in all_tasks]
        print(f"  Found {len(items)} total, {len(new_gids)} new", file=sys.stderr)
        for g in new_gids[:20]:
            detail = single_mcp_call("asana___GetTaskDetails", {"task_gid": g, "opt_fields": OPT})
            if detail and isinstance(detail, dict) and not detail.get("error"):
                td = detail.get("data", detail)
                if isinstance(td, dict) and not td.get("completed", False):
                    row = parse_task(td, None, None)
                    if row:
                        all_tasks[row["task_gid"]] = row
            time.sleep(0.5)

print(f"\nFinal total: {len(all_tasks)} unique incomplete tasks", file=sys.stderr)
by_proj = {}
for t in all_tasks.values():
    p = t.get("project_name") or "Unknown"
    by_proj[p] = by_proj.get(p, 0) + 1
for p, c in sorted(by_proj.items()):
    print(f"  {p}: {c}", file=sys.stderr)

json.dump(list(all_tasks.values()), sys.stdout, indent=2, default=str)
