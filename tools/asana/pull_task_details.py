#!/usr/bin/env python3
"""Pull full details for all Richard's tasks + portfolio project tasks."""
import json, os, subprocess, sys, time, shlex

ASANA_MCP = os.path.expanduser("~/.toolbox/bin/enterprise-asana-mcp")
OPT_FIELDS = "name,due_on,start_on,completed,completed_at,assignee.gid,custom_fields.gid,custom_fields.name,custom_fields.display_value,custom_fields.enum_value.name,custom_fields.date_value,custom_fields.text_value,projects.name,projects.gid,memberships.section.name,notes,permalink_url"

ROUTINE_MAP = {
    "Sweep (Low-friction)": "Sweep",
    "Core Two (Deep Work)": "Core",
    "Engine Room (Excel and Google ads)": "Engine Room",
    "Admin (Wind-down)": "Admin",
    "Wiki": "Wiki",
}

FIELD_MAP = {
    "1213608836755502": "routine_rw",
    "1212905889837829": "priority_rw",
    "1212905889837865": "importance_rw",
    "1213915851848087": "kiro_rw",
    "1213921400039514": "next_action_rw",
    "1213440376528542": "begin_date_rw",
}

PORTFOLIO_PROJECTS = {
    "1212762061512767": "AU",
    "1212775592612917": "MX",
    "1205997667578893": "WW Testing",
    "1206011235630048": "WW Acquisition",
    "1205997667578886": "Paid App",
    "1213917352480610": "ABPS AI Content",
}

def asana_call(tool_name, arguments):
    req = json.dumps({
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    })
    for attempt in range(3):
        try:
            p = subprocess.run(
                ["bash", "-c", f"echo {shlex.quote(req)} | timeout 60 {ASANA_MCP} 2>/dev/null"],
                capture_output=True, text=True, timeout=75
            )
            raw = p.stdout.strip()
            if not raw:
                time.sleep(2)
                continue
            d = json.loads(raw)
            if d.get("result", {}).get("isError"):
                err = d["result"]["content"][0]["text"]
                print(f"  API ERROR: {err[:200]}", file=sys.stderr)
                if "429" in err or "rate" in err.lower():
                    time.sleep(30)
                else:
                    time.sleep(2)
                continue
            content = d["result"]["content"][0]["text"]
            parsed = json.loads(content)
            if "APIOutput" in parsed:
                return parsed["APIOutput"].get("Response", {}).get("data", parsed["APIOutput"])
            return parsed.get("data", parsed)
        except Exception as e:
            print(f"  Exception ({tool_name}, attempt {attempt}): {e}", file=sys.stderr)
            time.sleep(2)
    return None

def extract_fields(task):
    result = {}
    for cf in task.get("custom_fields", []):
        gid = cf.get("gid", "")
        if gid not in FIELD_MAP:
            continue
        col = FIELD_MAP[gid]
        if col in ("routine_rw", "priority_rw", "importance_rw"):
            ev = cf.get("enum_value")
            if ev and isinstance(ev, dict):
                name = ev.get("name", "")
                result[col] = ROUTINE_MAP.get(name, name) if col == "routine_rw" else name
            else:
                result[col] = None
        elif col in ("kiro_rw", "next_action_rw"):
            result[col] = cf.get("text_value") or None
        elif col == "begin_date_rw":
            dv = cf.get("date_value")
            if dv and isinstance(dv, dict):
                result[col] = dv.get("date")
            else:
                result[col] = None
    return result

def task_to_row(task):
    gid = task.get("gid", "")
    assignee = task.get("assignee")
    agid = assignee.get("gid", "") if isinstance(assignee, dict) else ""
    projects = task.get("projects", [])
    pname = projects[0].get("name", "") if projects else None
    pgid = projects[0].get("gid", "") if projects else None
    memberships = task.get("memberships", [])
    sname = None
    for m in memberships:
        s = m.get("section", {})
        if s and s.get("name"):
            sname = s["name"]
            break
    cf = extract_fields(task)
    return {
        "task_gid": gid, "name": task.get("name", ""),
        "assignee_gid": agid, "project_name": pname, "project_gid": pgid,
        "section_name": sname, "due_on": task.get("due_on"),
        "start_on": task.get("start_on"), "completed": task.get("completed", False),
        "completed_at": task.get("completed_at"),
        "routine_rw": cf.get("routine_rw"), "priority_rw": cf.get("priority_rw"),
        "importance_rw": cf.get("importance_rw"), "kiro_rw": cf.get("kiro_rw"),
        "next_action_rw": cf.get("next_action_rw"), "begin_date_rw": cf.get("begin_date_rw"),
    }

# STEP 1: Get all Richard's task GIDs
print("STEP 1: Search Richard's incomplete tasks...")
search_result = asana_call("asana___SearchTasksInWorkspace", {
    "assignee_any": "1212732742544167", "completed": "false", "sort_by": "due_date"
})
richard_gids = []
if isinstance(search_result, list):
    richard_gids = [t["gid"] for t in search_result if t.get("gid")]
print(f"  Found {len(richard_gids)} task GIDs")

# STEP 2: Get details for each
print("\nSTEP 2: Fetch task details...")
all_tasks = {}
errors = []
for i, gid in enumerate(richard_gids):
    if (i+1) % 10 == 0:
        print(f"  Progress: {i+1}/{len(richard_gids)}")
    details = asana_call("asana___GetTaskDetails", {"task_gid": gid, "opt_fields": OPT_FIELDS})
    if details and isinstance(details, dict) and details.get("gid"):
        all_tasks[gid] = task_to_row(details)
    else:
        errors.append(gid)
    if (i+1) % 15 == 0:
        time.sleep(1)

print(f"  Got details for {len(all_tasks)} tasks, {len(errors)} errors")

# STEP 3: Pull portfolio project tasks
print("\nSTEP 3: Pull portfolio project tasks...")
for pgid, pname in PORTFOLIO_PROJECTS.items():
    print(f"  {pname}...")
    result = asana_call("asana___GetTasksFromProject", {"project_gid": pgid, "opt_fields": OPT_FIELDS})
    if not result:
        print(f"    ERROR: no result")
        continue
    tasks = result if isinstance(result, list) else []
    new_count = 0
    for t in tasks:
        if not isinstance(t, dict) or not t.get("gid"):
            continue
        if t.get("completed", False):
            continue
        tgid = t["gid"]
        if tgid not in all_tasks:
            all_tasks[tgid] = task_to_row(t)
            new_count += 1
    print(f"    {new_count} new tasks (total: {len(all_tasks)})")
    time.sleep(0.5)

# Save results
output = os.path.expanduser("~/shared/tools/_sync_tasks.json")
with open(output, "w") as f:
    json.dump(all_tasks, f, indent=2, default=str)

# Summary
by_project = {}
for t in all_tasks.values():
    pn = t.get("project_name") or "No Project"
    by_project[pn] = by_project.get(pn, 0) + 1

print(f"\n{'='*50}")
print(f"TOTAL: {len(all_tasks)} unique tasks")
print(f"By project:")
for pn, c in sorted(by_project.items()):
    print(f"  {pn}: {c}")
print(f"Errors: {len(errors)}")
if errors:
    print(f"  Failed GIDs: {errors[:10]}")
print(f"Saved to {output}")
