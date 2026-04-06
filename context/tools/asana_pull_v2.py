#!/usr/bin/env python3
"""Pull all tasks from Asana via enterprise-asana-mcp with proper MCP protocol."""
import json, subprocess, sys, time

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

def mcp_batch(calls):
    """Send multiple MCP calls in one process invocation. Returns list of results."""
    init = json.dumps({"jsonrpc":"2.0","id":0,"method":"initialize",
        "params":{"protocolVersion":"2024-11-05","capabilities":{},
                  "clientInfo":{"name":"sync","version":"1.0"}}})
    lines = [init]
    for i, (tool, args) in enumerate(calls, 1):
        lines.append(json.dumps({"jsonrpc":"2.0","id":i,"method":"tools/call",
                                  "params":{"name":tool,"arguments":args}}))
    full_input = "\n".join(lines) + "\n"
    p = subprocess.run(["enterprise-asana-mcp"], input=full_input,
                       capture_output=True, text=True, timeout=120)
    results = []
    for line in p.stdout.strip().split("\n"):
        if not line.strip():
            continue
        try:
            resp = json.loads(line)
            rid = resp.get("id", -1)
            if rid == 0:
                continue  # init response
            content = resp.get("result",{}).get("content",[])
            if content:
                text = content[0].get("text","")
                try:
                    results.append(json.loads(text))
                except:
                    results.append(text)
            else:
                results.append(None)
        except:
            results.append(None)
    return results

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
        "flex_fields": flex if flex else None,
    }

# Build batch calls for all projects
calls = []
for pgid, pname in PROJECTS:
    calls.append(("asana___GetTasksFromProject", {"project_gid": pgid, "opt_fields": OPT}))

# Also search Richard's assignments
calls.append(("asana___SearchTasksInWorkspace", {
    "assignee_any": "1212732742544167", "completed": "false", "sort_by": "due_date"
}))

print(f"Sending {len(calls)} MCP calls in one batch...", file=sys.stderr)
results = mcp_batch(calls)
print(f"Got {len(results)} responses", file=sys.stderr)

all_tasks = {}

# Process project results
for i, (pgid, pname) in enumerate(PROJECTS):
    if i >= len(results) or not results[i]:
        print(f"  {pname}: FAILED", file=sys.stderr)
        continue
    data = results[i]
    items = data if isinstance(data, list) else data.get("data", [])
    if not isinstance(items, list):
        print(f"  {pname}: unexpected type {type(items)}", file=sys.stderr)
        continue
    added = 0
    for t in items:
        if t.get("completed", False):
            continue
        row = parse_task(t, pname, pgid)
        if row and row["task_gid"] not in all_tasks:
            all_tasks[row["task_gid"]] = row
            added += 1
    print(f"  {pname}: +{added} incomplete", file=sys.stderr)

# Process search results (last call)
search_idx = len(PROJECTS)
if search_idx < len(results) and results[search_idx]:
    sdata = results[search_idx]
    sitems = sdata if isinstance(sdata, list) else sdata.get("data", [])
    if isinstance(sitems, list):
        new_gids = [t.get("gid","") for t in sitems if t.get("gid","") and t.get("gid","") not in all_tasks]
        print(f"  Search: {len(sitems)} total, {len(new_gids)} new", file=sys.stderr)
        # Fetch details for new tasks in batches
        if new_gids:
            detail_calls = [("asana___GetTaskDetails", {"task_gid": g, "opt_fields": OPT}) for g in new_gids[:30]]
            detail_results = mcp_batch(detail_calls)
            for dr in detail_results:
                if dr and isinstance(dr, dict):
                    td = dr.get("data", dr)
                    if isinstance(td, dict) and not td.get("completed", False):
                        row = parse_task(td, None, None)
                        if row:
                            all_tasks[row["task_gid"]] = row

print(f"\nTotal: {len(all_tasks)} unique incomplete tasks", file=sys.stderr)

# Summary by project
by_proj = {}
for t in all_tasks.values():
    p = t.get("project_name") or "Unknown"
    by_proj[p] = by_proj.get(p, 0) + 1
for p, c in sorted(by_proj.items()):
    print(f"  {p}: {c}", file=sys.stderr)

json.dump(list(all_tasks.values()), sys.stdout, indent=2, default=str)
