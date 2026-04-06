#!/usr/bin/env python3
"""Execute enrichment tasks: pinned context updates, ABPS AI access diagnosis, event task checks."""

import json
import os
import subprocess
import sys
import time
from datetime import datetime

ASANA_MCP = os.path.expanduser("~/.toolbox/bin/enterprise-asana-mcp")
RICHARD_GID = "1212732742544167"

def asana_call(tool_name, arguments, retries=2):
    """Call enterprise-asana-mcp tool and return parsed result."""
    req = json.dumps({
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    })
    tmpfile = os.path.expanduser("~/asana_enrichment_req.json")
    with open(tmpfile, "w") as f:
        f.write(req)
    
    for attempt in range(retries + 1):
        try:
            p = subprocess.run(
                ["bash", "-c", f"cat {tmpfile} | timeout 60 {ASANA_MCP} 2>/dev/null"],
                capture_output=True, text=True, timeout=75
            )
            raw = p.stdout.strip()
            if not raw:
                if attempt < retries:
                    time.sleep(2)
                    continue
                return {"error": "empty response"}
            
            data = json.loads(raw)
            if "error" in data:
                if attempt < retries:
                    time.sleep(2)
                    continue
                return {"error": data["error"]}
            
            result = data.get("result", data)
            if isinstance(result, dict) and "content" in result:
                for c in result["content"]:
                    if c.get("type") == "text":
                        try:
                            return json.loads(c["text"])
                        except:
                            return {"raw": c["text"]}
            return result
            
        except subprocess.TimeoutExpired:
            if attempt < retries:
                time.sleep(2)
                continue
            return {"error": "timeout"}
        except json.JSONDecodeError as e:
            if attempt < retries:
                time.sleep(2)
                continue
            return {"error": f"JSON decode: {e}", "raw": raw[:500] if raw else ""}
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
                continue
            return {"error": str(e)}


def log_audit(tool, task_gid, task_name, fields_modified, result, notes=""):
    """Append to audit log."""
    entry = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": tool,
        "task_gid": task_gid,
        "task_name": task_name,
        "project": "My_Tasks",
        "fields_modified": fields_modified,
        "result": result,
        "notes": notes
    }
    audit_path = os.path.expanduser("~/shared/context/active/asana-audit-log.jsonl")
    with open(audit_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

# ============================================================
# TASK 1: Enrich 4 pinned context tasks with next_action_rw
# ============================================================
print("=" * 60)
print("TASK 1: Enriching pinned context tasks with next_action_rw")
print("=" * 60)

pinned_tasks = [
    {
        "gid": "1213917747384849",
        "name": "📌 AU Market Context (Agent-Maintained)",
        "value": "No action — agent-maintained reference doc, refreshed weekly in EOD-2"
    },
    {
        "gid": "1213917747438931",
        "name": "📌 AU Market Context (Kiro)",
        "value": "No action — pinned context doc, refreshed weekly in EOD-2"
    },
    {
        "gid": "1213917639688517",
        "name": "📌 MX Market Context (Kiro)",
        "value": "No action — pinned context doc, refreshed weekly in EOD-2"
    },
    {
        "gid": "1213917771155873",
        "name": "📌 Paid App Project Context (Kiro)",
        "value": "No action — pinned context doc, refreshed weekly in EOD-2"
    },
]

NEXT_ACTION_FIELD_GID = "1213921400039514"

for task in pinned_tasks:
    print(f"\n  Updating: {task['name']} ({task['gid']})")
    print(f"    Setting next_action_rw = \"{task['value']}\"")
    
    result = asana_call("asana___UpdateTask", {
        "task_gid": task["gid"],
        "custom_fields": json.dumps({NEXT_ACTION_FIELD_GID: task["value"]})
    })
    
    if result and not result.get("error"):
        print(f"    ✅ SUCCESS")
        log_audit("UpdateTask", task["gid"], task["name"], 
                  ["custom_fields.Next-action_RW"], "success",
                  f"Set next_action_rw for pinned context task")
    else:
        err = result.get("error", "unknown") if result else "no response"
        print(f"    ❌ FAILED: {err}")
        log_audit("UpdateTask", task["gid"], task["name"],
                  ["custom_fields.Next-action_RW"], "failure",
                  f"Failed: {err}")
    
    time.sleep(0.5)


# ============================================================
# TASK 2: Diagnose ABPS AI Content & Build access
# ============================================================
print("\n" + "=" * 60)
print("TASK 2: Diagnosing ABPS AI project access")
print("=" * 60)

for project_name, project_gid in [("ABPS AI Content", "1213917352480610"), ("ABPS AI Build", "1213379551525587")]:
    print(f"\n--- {project_name} (GID: {project_gid}) ---")
    
    # Test 1: GetTasksFromProject
    print(f"  Test 1: GetTasksFromProject...")
    r1 = asana_call("asana___GetTasksFromProject", {
        "project_gid": project_gid,
        "opt_fields": "name,completed,assignee.gid"
    })
    if r1 and not r1.get("error"):
        data = r1.get("data", r1)
        if isinstance(data, list):
            print(f"    ✅ SUCCESS — returned {len(data)} tasks")
            for t in data[:3]:
                asg = t.get("assignee", {})
                asg_gid = asg.get("gid", "none") if asg else "unassigned"
                print(f"      - {t.get('name', '?')} (assignee: {asg_gid})")
        else:
            print(f"    ⚠️ Unexpected format: {str(r1)[:300]}")
    else:
        err = r1.get("error", "unknown") if r1 else "no response"
        raw = r1.get("raw", "") if r1 else ""
        print(f"    ❌ FAILED: {err}")
        if raw:
            print(f"    Raw: {raw[:300]}")
    
    time.sleep(0.5)
    
    # Test 2: GetProjectDetails
    print(f"  Test 2: GetProjectDetails...")
    r2 = asana_call("asana___GetProjectDetails", {
        "project_gid": project_gid
    })
    if r2 and not r2.get("error"):
        data = r2.get("data", r2)
        if isinstance(data, dict):
            owner = data.get("owner", {})
            owner_gid = owner.get("gid", "?") if owner else "none"
            print(f"    ✅ SUCCESS — name: {data.get('name', '?')}, owner: {owner_gid}")
        else:
            print(f"    ⚠️ Unexpected format: {str(r2)[:300]}")
    else:
        err = r2.get("error", "unknown") if r2 else "no response"
        raw = r2.get("raw", "") if r2 else ""
        print(f"    ❌ FAILED: {err}")
        if raw:
            print(f"    Raw: {raw[:300]}")
    
    time.sleep(0.5)
    
    # Test 3: SearchTasksInWorkspace
    print(f"  Test 3: SearchTasksInWorkspace(projects_any)...")
    r3 = asana_call("asana___SearchTasksInWorkspace", {
        "projects_any": project_gid,
        "completed": False
    })
    if r3 and not r3.get("error"):
        data = r3.get("data", r3)
        if isinstance(data, list):
            print(f"    ✅ SUCCESS — returned {len(data)} tasks")
        else:
            print(f"    ⚠️ Unexpected format: {str(r3)[:300]}")
    else:
        err = r3.get("error", "unknown") if r3 else "no response"
        raw = r3.get("raw", "") if r3 else ""
        print(f"    ❌ FAILED: {err}")
        if raw:
            print(f"    Raw: {raw[:300]}")
    
    time.sleep(0.5)


# ============================================================
# TASK 3: Check Paid App event task assignees
# ============================================================
print("\n" + "=" * 60)
print("TASK 3: Checking Paid App event task assignees")
print("=" * 60)

event_tasks = [
    {"gid": "1206497728159526", "name": "Paid App - Prime Day Event"},
    {"gid": "1206497728159532", "name": "Paid App - Back to School"},
    {"gid": "1206497728159528", "name": "Paid App - PBBD Event"},
    {"gid": "1206497731655624", "name": "Paid App - Black Friday/Cyber Monday"},
    {"gid": "1206497731655622", "name": "Paid App - Business Gift Guide"},
]

unassigned_tasks = []
richard_tasks = []

for task in event_tasks:
    print(f"\n  Checking: {task['name']} ({task['gid']})")
    
    result = asana_call("asana___GetTaskDetails", {
        "task_gid": task["gid"],
        "opt_fields": "name,assignee.gid,assignee.name,due_on,memberships.section.name"
    })
    
    if result and not result.get("error"):
        data = result.get("data", result)
        assignee = data.get("assignee")
        due = data.get("due_on", "no due date")
        section = "unknown"
        memberships = data.get("memberships", [])
        if memberships:
            section = memberships[0].get("section", {}).get("name", "unknown")
        
        if assignee and assignee.get("gid") == RICHARD_GID:
            print(f"    ✅ Assigned to Richard | due: {due} | section: {section}")
            richard_tasks.append(task)
        elif assignee:
            aname = assignee.get("name", assignee.get("gid"))
            print(f"    ⚠️ Assigned to {aname} | due: {due} | section: {section}")
            unassigned_tasks.append(task)
        else:
            print(f"    🚫 UNASSIGNED | due: {due} | section: {section}")
            unassigned_tasks.append(task)
    else:
        err = result.get("error", "unknown") if result else "no response"
        print(f"    ❌ Failed to fetch: {err}")
    
    time.sleep(0.5)

print(f"\n  SUMMARY:")
print(f"    Richard-assigned: {len(richard_tasks)}")
print(f"    Unassigned/other: {len(unassigned_tasks)}")
if unassigned_tasks:
    print(f"    ⛔ GUARD BLOCKS enrichment on {len(unassigned_tasks)} tasks.")
    print(f"    RECOMMENDATION: Richard should assign these to himself first.")
    for t in unassigned_tasks:
        print(f"      - {t['name']} ({t['gid']})")

print("\n✅ All Asana operations complete.")
