#!/usr/bin/env python3
"""Asana Full Sync Runner — pulls tasks via enterprise-asana-mcp and outputs JSON."""
import json, subprocess, sys, time, os

MCP = os.path.expanduser("~/.toolbox/bin/enterprise-asana-mcp")
RICHARD_GID = "1212732742544167"

PROJECTS = {
    "1213917352480610": "ABPS AI Content",
    "1212762061512767": "AU",
    "1212775592612917": "MX",
    "1205997667578893": "WW Testing",
    "1206011235630048": "WW Acquisition",
    "1205997667578886": "Paid App",
    "1213379551525587": "ABPS AI Build",
}

OPT_FIELDS = "name,due_on,start_on,completed,completed_at,assignee.gid,custom_fields.gid,custom_fields.name,custom_fields.display_value,custom_fields.enum_value.name,custom_fields.date_value,custom_fields.text_value,projects.name,projects.gid,memberships.section.name,notes,permalink_url"

FIELD_MAP = {
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

def mcp_call(tool_name, arguments):
    req = json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":tool_name,"arguments":arguments}})
    # Escape single quotes in req for shell
    req_escaped = req.replace("'", "'\\''")
    try:
        p = subprocess.run(
            ["bash", "-c", f"echo '{req_escaped}' | timeout 60 {MCP} 2>/dev/null"],
            capture_output=True, text=True, timeout=75
        )
        if p.returncode != 0 or not p.stdout.strip():
            return None
        resp = json.loads(p.stdout.strip())
        if "error" in resp:
            print(f"  MCP error ({tool_name}): {resp['error']}", file=sys.stderr)
            return None
        content = resp.get("result", {}).get("content", [])
        if content and isinstance(content, list):
            text = content[0].get("text", "")
            try:
                return json.loads(text)
            except:
                return text
        return resp.get("result")
    except Exception as e:
        print(f"  Exception ({tool_name}): {e}", file=sys.stderr)
        return None

def extract_fields(task):
    """Extract custom fields and flex_fields from task."""
    core = {}
    flex = {}
    for cf in task.get("custom_fields", []):
        gid = cf.get("gid", "")
        if gid in FIELD_MAP:
            col = FIELD_MAP[gid]
            if col in ("routine_rw", "priority_rw", "importance_rw"):
                ev = cf.get("enum_value")
                if ev and isinstance(ev, dict):
                    name = ev.get("name", "")
                    core[col] = ROUTINE_MAP.get(name, name) if col == "routine_rw" else name
                else:
                    core[col] = None
            elif col in ("kiro_rw", "next_action_rw"):
                core[col] = cf.get("text_value") or None
            elif col == "begin_date_rw":
                dv = cf.get("date_value")
                if dv and isinstance(dv, dict):
                    core[col] = dv.get("date")
                elif isinstance(dv, str):
                    core[col] = dv
                else:
                    core[col] = None
        else:
            # Flex field
            dv = cf.get("display_value")
            if dv:
                flex[gid] = {"name": cf.get("name", ""), "value": dv}
    return core, flex

def task_to_row(task):
    gid = task.get("gid", "")
    assignee = task.get("assignee")
    assignee_gid = assignee.get("gid", "") if isinstance(assignee, dict) else ""
    projects = task.get("projects", [])
    project_name = projects[0].get("name", "") if projects else None
    project_gid = projects[0].get("gid", "") if projects else None
    memberships = task.get("memberships", [])
    section_name = None
    for m in memberships:
        sec = m.get("section", {})
        if sec and sec.get("name"):
            section_name = sec["name"]
            break
    core, flex = extract_fields(task)
    return {
        "task_gid": gid,
        "name": task.get("name", ""),
        "assignee_gid": assignee_gid,
        "project_name": project_name,
        "project_gid": project_gid,
        "section_name": section_name,
        "due_on": task.get("due_on"),
        "start_on": task.get("start_on"),
        "completed": task.get("completed", False),
        "completed_at": task.get("completed_at"),
        "routine_rw": core.get("routine_rw"),
        "priority_rw": core.get("priority_rw"),
        "importance_rw": core.get("importance_rw"),
        "kiro_rw": core.get("kiro_rw"),
        "next_action_rw": core.get("next_action_rw"),
        "begin_date_rw": core.get("begin_date_rw"),
        "flex_fields": flex if flex else None,
    }

# STEP 1: Search Richard's incomplete tasks
print("STEP 1: SearchTasksInWorkspace...", file=sys.stderr)
search_result = mcp_call("asana___SearchTasksInWorkspace", {
    "assignee_any": RICHARD_GID,
    "completed": False,
    "sort_by": "due_date",
    "opt_fields": OPT_FIELDS
})

all_tasks = {}
if search_result:
    tasks_data = search_result if isinstance(search_result, list) else search_result.get("data", [])
    if isinstance(tasks_data, list):
        print(f"  Search returned {len(tasks_data)} tasks", file=sys.stderr)
        for t in tasks_data:
            tgid = t.get("gid", "")
            if tgid and not t.get("completed", False):
                all_tasks[tgid] = task_to_row(t)
    else:
        print(f"  Unexpected search result type: {type(tasks_data)}", file=sys.stderr)
        print(f"  Preview: {str(search_result)[:500]}", file=sys.stderr)
else:
    print("  Search returned nothing", file=sys.stderr)

print(f"  Step 1 total: {len(all_tasks)} tasks", file=sys.stderr)

# STEP 2: Pull from each project
print("\nSTEP 2: Pull portfolio projects...", file=sys.stderr)
for proj_gid, proj_name in PROJECTS.items():
    print(f"  Project: {proj_name}...", file=sys.stderr)
    result = mcp_call("asana___GetTasksFromProject", {
        "project_gid": proj_gid,
        "opt_fields": OPT_FIELDS
    })
    if not result:
        print(f"    No result", file=sys.stderr)
        continue
    tasks_data = result if isinstance(result, list) else result.get("data", [])
    if not isinstance(tasks_data, list):
        print(f"    Unexpected type: {type(tasks_data)}", file=sys.stderr)
        continue
    count = 0
    for t in tasks_data:
        td = t.get("data", t) if isinstance(t, dict) else t
        if not isinstance(td, dict):
            continue
        tgid = td.get("gid", "")
        if not tgid or td.get("completed", False):
            continue
        if tgid not in all_tasks:
            row = task_to_row(td)
            if not row["project_name"]:
                row["project_name"] = proj_name
                row["project_gid"] = proj_gid
            all_tasks[tgid] = row
            count += 1
        else:
            # Update project info if missing
            if not all_tasks[tgid]["project_name"]:
                all_tasks[tgid]["project_name"] = proj_name
                all_tasks[tgid]["project_gid"] = proj_gid
    print(f"    +{count} new (total: {len(all_tasks)})", file=sys.stderr)
    time.sleep(0.3)

print(f"\nTotal unique tasks: {len(all_tasks)}", file=sys.stderr)

# Output as JSON to stdout
json.dump(all_tasks, sys.stdout, indent=2, default=str)
