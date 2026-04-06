#!/usr/bin/env python3
"""AM-2 Triage Writes — Execute approved proposals from morning triage.
Proposal 1: Create PAM budget reply task
Proposal 2: Near-due escalation (3 tasks)
Proposal 3: Overdue Kiro_RW batch (18 tasks)
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime

ASANA_MCP = os.path.expanduser("~/.toolbox/bin/enterprise-asana-mcp")
RICHARD_GID = "1212732742544167"
TODAY = datetime.now().strftime("%Y-%m-%d")
TODAY_SHORT = f"{datetime.now().month}/{datetime.now().day}"
TIMESTAMP = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
AUDIT_LOG = os.path.expanduser("~/shared/context/active/asana-audit-log.jsonl")

# GIDs
ROUTINE_SWEEP = "1213608836755503"
PRIORITY_TODAY = "1212905889837830"
PRIORITY_NOT_URGENT = "1212905889837833"
FIELD_ROUTINE = "1213608836755502"
FIELD_PRIORITY = "1212905889837829"
FIELD_KIRO = "1213915851848087"
FIELD_NEXT_ACTION = "1213921400039514"

def asana_call(tool_name, arguments, retries=2):
    """Call enterprise-asana-mcp tool and return parsed result."""
    req = json.dumps({
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    })
    tmpfile = "/tmp/_asana_req.json"
    with open(tmpfile, "w") as f:
        f.write(req)
    for attempt in range(retries + 1):
        try:
            # Use echo pipe — the MCP binary needs bash pipe for stdin
            escaped_req = req.replace("'", "'\\''")
            p = subprocess.run(
                ["bash", "-c", f"echo '{escaped_req}' | timeout 60 {ASANA_MCP}"],
                capture_output=True, text=True, timeout=75
            )
            raw = p.stdout.strip()
            if not raw:
                if attempt < retries:
                    time.sleep(2)
                    continue
                return None
            data = json.loads(raw)
            if "error" in data:
                print(f"  MCP ERROR ({tool_name}): {data['error']}", file=sys.stderr)
                if attempt < retries:
                    time.sleep(2)
                    continue
                return None
            content = data.get("result", {}).get("content", [])
            if content and isinstance(content, list):
                text = content[0].get("text", "")
                try:
                    parsed = json.loads(text)
                    # Asana responses wrap in {"data": {...}}
                    if isinstance(parsed, dict) and "data" in parsed:
                        return parsed["data"]
                    return parsed
                except json.JSONDecodeError:
                    return text
            return data.get("result")
        except Exception as e:
            print(f"  ERROR ({tool_name}, attempt {attempt+1}): {e}", file=sys.stderr)
            if attempt < retries:
                time.sleep(2)
    return None

def audit_log(tool, task_gid, task_name, fields_modified, result, project="My_Tasks", notes=""):
    entry = {
        "timestamp": TIMESTAMP,
        "tool": tool,
        "task_gid": task_gid,
        "task_name": task_name,
        "project": project,
        "fields_modified": fields_modified,
        "result": result,
        "notes": notes
    }
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"  AUDIT: {tool} on {task_name} → {result}")


def proposal_1_create_pam_task():
    """Create PAM budget reply task."""
    print("\n=== PROPOSAL 1: Create PAM Budget Reply Task ===")
    result = asana_call("asana___CreateTask", {
        "name": "Reply to Brandon — PAM budget needs assessment",
        "assignee": RICHARD_GID,
        "due_on": TODAY,
        "workspace": "8442528107068",
        "custom_fields": {
            FIELD_ROUTINE: ROUTINE_SWEEP,
            FIELD_PRIORITY: PRIORITY_TODAY,
            FIELD_KIRO: f"{TODAY_SHORT}: Brandon asked about extra PAM $. Reply today.",
            FIELD_NEXT_ACTION: "Check PAM US spend pacing and reply in ab-paid-search-app"
        }
    })
    if result and isinstance(result, dict) and result.get("gid"):
        gid = result["gid"]
        print(f"  ✅ Created task GID: {gid}")
        audit_log("CreateTask", gid, "Reply to Brandon — PAM budget needs assessment",
                  ["name", "assignee", "due_on", "custom_fields.Routine_RW", "custom_fields.Priority_RW",
                   "custom_fields.Kiro_RW", "custom_fields.Next_Action"],
                  "success", notes="From Slack signal: Brandon PAM budget @mention")
        return gid
    else:
        print(f"  ❌ Failed to create task: {result}")
        audit_log("CreateTask", "unknown", "Reply to Brandon — PAM budget needs assessment",
                  ["name"], "failure", notes="Creation failed")
        return None


def proposal_2_near_due_escalation():
    """Escalate 3 near-due tasks to Today priority."""
    print("\n=== PROPOSAL 2: Near-Due Escalation (3 tasks) ===")
    tasks = [
        ("1213764961716427", "WW weblab dial-up (Richard)", "WW Testing"),
        ("1213917832711157", "Verify MX/AU net pacing against OP2 numbers", "My_Tasks"),
        ("1213917639154050", "AU meetings - Agenda", "AU"),
    ]
    for gid, name, project in tasks:
        # First verify assignee
        details = asana_call("asana___GetTaskDetails", {
            "task_gid": gid,
            "opt_fields": "assignee.gid,custom_fields.gid,custom_fields.display_value"
        })
        if not details or not isinstance(details, dict):
            print(f"  ⚠️ Could not read {name} — skipping")
            audit_log("UpdateTask", gid, name, ["custom_fields.Priority_RW"], "failure",
                      project=project, notes="Could not read task details")
            continue
        
        assignee_gid = details.get("assignee", {}).get("gid", "")
        if assignee_gid != RICHARD_GID:
            print(f"  ⛔ BLOCKED: {name} not assigned to Richard (assignee: {assignee_gid})")
            audit_log("UpdateTask", gid, name, ["custom_fields.Priority_RW"], "blocked",
                      project=project, notes=f"Assignee {assignee_gid} != Richard")
            continue
        
        result = asana_call("asana___UpdateTask", {
            "task_gid": gid,
            "custom_fields": {
                FIELD_PRIORITY: PRIORITY_TODAY,
                FIELD_KIRO: f"{TODAY_SHORT}: Near-due. Priority escalated.",
            }
        })
        if result:
            print(f"  ✅ Escalated: {name}")
            audit_log("UpdateTask", gid, name,
                      ["custom_fields.Priority_RW", "custom_fields.Kiro_RW"],
                      "success", project=project, notes="Near-due escalation (auto)")
        else:
            print(f"  ❌ Failed: {name}")
            audit_log("UpdateTask", gid, name, ["custom_fields.Priority_RW"], "failure",
                      project=project, notes="Near-due escalation failed")


def proposal_3_overdue_kiro_batch():
    """Update Kiro_RW on overdue tasks with overdue flagging."""
    print("\n=== PROPOSAL 3: Overdue Kiro_RW Batch ===")
    from datetime import date
    today = date.today()
    
    overdue_tasks = [
        ("1212808474749819", "Raise rest of year PO for PAM US", "2026-03-01", "Paid_App"),
        ("1213230198995937", "WW redirect - Adobe Ad Cloud reporting", "2026-03-09", "My_Tasks"),
        ("1213560614815911", "PAM R&O", "2026-03-10", "My_Tasks"),
        ("1213720297606981", "Flash topics due today", "2026-03-17", "My_Tasks"),
        ("1213730974261148", "Make changes to AU/MX/PAM for the week", "2026-03-18", "My_Tasks"),
        ("1213072707685834", "MX Automotive page", "2026-03-20", "MX"),
        ("1213637505601024", "R&O for MX/AU", "2026-03-23", "My_Tasks"),
        ("1213637505601028", "MX/AU confirm budgets", "2026-03-25", "My_Tasks"),
        ("1213839064321460", "Weekly Reporting - Global WBR sheet", "2026-03-30", "My_Tasks"),
        ("1213828814410247", "Mondays - Write into EU SSR Acq Asana", "2026-03-30", "My_Tasks"),
        ("1213341921686564", "Testing Document for Kate", "2026-04-01", "WW_Testing"),
        ("1213530917597503", "Monthly - Confirm actual budgets", "2026-04-01", "Paid_App"),
        ("1213917888972148", "Reply to Stacey — CA exclusion from Polaris 4/7", "2026-04-03", "My_Tasks"),
        ("1213917967984980", "Respond to Lena — AU LP URL analysis + CPA", "2026-04-03", "AU"),
        ("1213546434830000", "ie%CCP calc - insert MX spend/regs before 9th", "2026-04-03", "My_Tasks"),
        ("1213923128960832", "Prime Day Creative Phase 4 inputs — Smartsheets", "2026-04-03", "My_Tasks"),
    ]
    
    success_count = 0
    fail_count = 0
    blocked_count = 0
    
    for gid, name, due_str, project in overdue_tasks:
        due_date = date.fromisoformat(due_str)
        days_overdue = (today - due_date).days
        
        # Verify assignee first
        details = asana_call("asana___GetTaskDetails", {
            "task_gid": gid,
            "opt_fields": "assignee.gid"
        })
        if not details or not isinstance(details, dict):
            print(f"  ⚠️ Could not read {name} — skipping")
            fail_count += 1
            continue
        
        assignee_gid = details.get("assignee", {}).get("gid", "")
        if assignee_gid != RICHARD_GID:
            print(f"  ⛔ BLOCKED: {name} (assignee: {assignee_gid})")
            audit_log("UpdateTask", gid, name, ["custom_fields.Kiro_RW"], "blocked",
                      project=project, notes=f"Assignee {assignee_gid} != Richard")
            blocked_count += 1
            continue
        
        kiro_text = f"{TODAY_SHORT}: Overdue {days_overdue}d. Extend or close."
        next_action = "Decide: extend due date, reduce scope, or complete"
        
        result = asana_call("asana___UpdateTask", {
            "task_gid": gid,
            "custom_fields": {
                FIELD_KIRO: kiro_text,
                FIELD_NEXT_ACTION: next_action,
            }
        })
        if result:
            print(f"  ✅ {name}: {kiro_text}")
            audit_log("UpdateTask", gid, name,
                      ["custom_fields.Kiro_RW", "custom_fields.Next_Action"],
                      "success", project=project, notes=f"Overdue {days_overdue}d flagging")
            success_count += 1
        else:
            print(f"  ❌ Failed: {name}")
            audit_log("UpdateTask", gid, name, ["custom_fields.Kiro_RW"], "failure",
                      project=project, notes="Overdue flagging failed")
            fail_count += 1
    
    print(f"\n  Summary: {success_count} updated, {fail_count} failed, {blocked_count} blocked")


if __name__ == "__main__":
    print(f"AM-2 Triage Writes — {TODAY}")
    print(f"Audit log: {AUDIT_LOG}")
    
    proposal_1_create_pam_task()
    proposal_2_near_due_escalation()
    proposal_3_overdue_kiro_batch()
    
    print("\n=== ALL PROPOSALS EXECUTED ===")
