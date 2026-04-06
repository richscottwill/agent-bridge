#!/usr/bin/env python3
"""Full Asana → DuckDB Sync (AM-1 Full Sync)
Pulls all incomplete tasks from Richard's assignments + portfolio projects,
maps custom fields, and UPSERTs into DuckDB asana_tasks table.
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
TIMESTAMP = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# Portfolio projects to pull
PORTFOLIO_PROJECTS = {
    "1212762061512767": "AU",
    "1212775592612917": "MX",
    "1205997667578893": "WW Testing",
    "1206011235630048": "WW Acquisition",
    "1205997667578886": "Paid App",
    "1213917352480610": "ABPS AI Content",
}

# Custom field GID → column mapping
FIELD_MAP = {
    "1213608836755502": "routine_rw",
    "1212905889837829": "priority_rw",
    "1212905889837865": "importance_rw",
    "1213915851848087": "kiro_rw",
    "1213921400039514": "next_action_rw",
    "1213440376528542": "begin_date_rw",
}

# Routine enum display name → short name
ROUTINE_MAP = {
    "Sweep (Low-friction)": "Sweep",
    "Core Two (Deep Work)": "Core",
    "Engine Room (Excel and Google ads)": "Engine Room",
    "Admin (Wind-down)": "Admin",
    "Wiki": "Wiki",
}

OPT_FIELDS = "name,due_on,start_on,completed,completed_at,assignee.gid,custom_fields.gid,custom_fields.name,custom_fields.display_value,custom_fields.enum_value.name,custom_fields.date_value,custom_fields.text_value,projects.name,projects.gid,memberships.section.name,notes,permalink_url"

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
            p = subprocess.run(
                ["bash", "-c", f"cat {tmpfile} | timeout 60 {ASANA_MCP} 2>/dev/null"],
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
            
            # Parse nested content
            content = data.get("result", {}).get("content", [])
            if content and isinstance(content, list):
                text = content[0].get("text", "")
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return text
            return data.get("result")
        except Exception as e:
            print(f"  ERROR ({tool_name}, attempt {attempt+1}): {e}", file=sys.stderr)
            if attempt < retries:
                time.sleep(2)
    return None


def extract_custom_fields(task):
    """Extract custom field values from task data."""
    result = {}
    custom_fields = task.get("custom_fields", [])
    if not custom_fields:
        return result
    
    for cf in custom_fields:
        gid = cf.get("gid", "")
        if gid not in FIELD_MAP:
            continue
        
        col = FIELD_MAP[gid]
        
        if col in ("routine_rw", "priority_rw", "importance_rw"):
            # Enum field
            enum_val = cf.get("enum_value")
            if enum_val and isinstance(enum_val, dict):
                name = enum_val.get("name", "")
                if col == "routine_rw":
                    result[col] = ROUTINE_MAP.get(name, name)
                else:
                    result[col] = name
            else:
                result[col] = None
        elif col in ("kiro_rw", "next_action_rw"):
            # Text field
            result[col] = cf.get("text_value") or None
        elif col == "begin_date_rw":
            # Date field
            dv = cf.get("date_value")
            if dv and isinstance(dv, dict):
                result[col] = dv.get("date")
            elif isinstance(dv, str):
                result[col] = dv
            else:
                result[col] = None
    
    return result


def extract_task_row(task):
    """Convert an Asana task API response into a flat dict for DuckDB."""
    gid = task.get("gid", "")
    name = task.get("name", "")
    
    # Assignee
    assignee = task.get("assignee")
    assignee_gid = assignee.get("gid", "") if isinstance(assignee, dict) else (assignee or "")
    
    # Project info (first project)
    projects = task.get("projects", [])
    project_name = projects[0].get("name", "") if projects else None
    project_gid = projects[0].get("gid", "") if projects else None
    
    # Section (from memberships)
    memberships = task.get("memberships", [])
    section_name = None
    for m in memberships:
        sec = m.get("section", {})
        if sec and sec.get("name"):
            section_name = sec["name"]
            break
    
    # Custom fields
    cf = extract_custom_fields(task)
    
    return {
        "task_gid": gid,
        "name": name,
        "assignee_gid": assignee_gid,
        "project_name": project_name,
        "project_gid": project_gid,
        "section_name": section_name,
        "due_on": task.get("due_on"),
        "start_on": task.get("start_on"),
        "completed": task.get("completed", False),
        "completed_at": task.get("completed_at"),
        "routine_rw": cf.get("routine_rw"),
        "priority_rw": cf.get("priority_rw"),
        "importance_rw": cf.get("importance_rw"),
        "kiro_rw": cf.get("kiro_rw"),
        "next_action_rw": cf.get("next_action_rw"),
        "begin_date_rw": cf.get("begin_date_rw"),
    }


def step1_pull_richard_tasks():
    """Pull all incomplete tasks assigned to Richard."""
    print("=" * 60)
    print("STEP 1: Pull all incomplete tasks assigned to Richard")
    print("=" * 60)
    
    result = asana_call("asana___SearchTasksInWorkspace", {
        "assignee_any": RICHARD_GID,
        "completed": False,
        "sort_by": "due_date"
    })
    
    if not result:
        print("  ERROR: SearchTasksInWorkspace returned nothing")
        return {}
    
    # Extract task GIDs from search results
    tasks_data = result if isinstance(result, list) else result.get("data", [])
    if not isinstance(tasks_data, list):
        print(f"  Unexpected result type: {type(tasks_data)}")
        print(f"  Result preview: {str(result)[:500]}")
        return {}
    
    print(f"  Found {len(tasks_data)} tasks from search")
    
    # Get full details for each task
    all_tasks = {}
    for i, t in enumerate(tasks_data):
        tgid = t.get("gid", "")
        if not tgid:
            continue
        
        if (i + 1) % 10 == 0:
            print(f"  Fetching details... {i+1}/{len(tasks_data)}")
        
        details = asana_call("asana___GetTaskDetails", {
            "task_gid": tgid,
            "opt_fields": OPT_FIELDS
        })
        
        if details:
            task_data = details.get("data", details) if isinstance(details, dict) else details
            if isinstance(task_data, dict) and task_data.get("gid"):
                row = extract_task_row(task_data)
                all_tasks[tgid] = row
        
        # Rate limit protection
        if (i + 1) % 20 == 0:
            time.sleep(1)
    
    print(f"  Got details for {len(all_tasks)} tasks")
    return all_tasks


def step2_pull_project_tasks():
    """Pull tasks from portfolio projects."""
    print("\n" + "=" * 60)
    print("STEP 2: Pull portfolio project tasks")
    print("=" * 60)
    
    all_tasks = {}
    
    for proj_gid, proj_name in PORTFOLIO_PROJECTS.items():
        print(f"\n  Project: {proj_name} ({proj_gid})")
        
        result = asana_call("asana___GetTasksFromProject", {
            "project_gid": proj_gid,
            "opt_fields": OPT_FIELDS
        })
        
        if not result:
            print(f"    ERROR: No result for {proj_name}")
            continue
        
        tasks_data = result if isinstance(result, list) else result.get("data", [])
        if not isinstance(tasks_data, list):
            print(f"    Unexpected type: {type(tasks_data)}")
            continue
        
        count = 0
        for t in tasks_data:
            task_data = t.get("data", t) if isinstance(t, dict) else t
            if not isinstance(task_data, dict):
                continue
            
            tgid = task_data.get("gid", "")
            if not tgid:
                continue
            
            # Skip completed tasks
            if task_data.get("completed", False):
                continue
            
            if tgid not in all_tasks:
                row = extract_task_row(task_data)
                # Override project info with the project we're pulling from
                if not row["project_name"]:
                    row["project_name"] = proj_name
                    row["project_gid"] = proj_gid
                all_tasks[tgid] = row
                count += 1
        
        print(f"    Found {count} new incomplete tasks (total unique: {len(all_tasks)})")
        time.sleep(0.5)
    
    return all_tasks


def sql_escape(val):
    """Escape a value for SQL insertion."""
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    if isinstance(val, (int, float)):
        return str(val)
    # String - escape single quotes
    s = str(val).replace("'", "''")
    return f"'{s}'"


def step4_upsert_to_duckdb(all_tasks):
    """Batch UPSERT all tasks into DuckDB."""
    print("\n" + "=" * 60)
    print("STEP 4: UPSERT into DuckDB")
    print("=" * 60)
    
    task_list = list(all_tasks.values())
    batch_size = 12
    total_upserted = 0
    errors = []
    
    for batch_start in range(0, len(task_list), batch_size):
        batch = task_list[batch_start:batch_start + batch_size]
        
        values_parts = []
        for t in batch:
            vals = (
                f"({sql_escape(t['task_gid'])}, {sql_escape(t['name'])}, "
                f"{sql_escape(t['assignee_gid'])}, {sql_escape(t['project_name'])}, "
                f"{sql_escape(t['project_gid'])}, {sql_escape(t['section_name'])}, "
                f"{'CAST(' + sql_escape(t['due_on']) + ' AS DATE)' if t['due_on'] else 'NULL'}, "
                f"{'CAST(' + sql_escape(t['start_on']) + ' AS DATE)' if t['start_on'] else 'NULL'}, "
                f"{sql_escape(t['completed'])}, "
                f"{'CAST(' + sql_escape(t['completed_at']) + ' AS TIMESTAMP)' if t['completed_at'] else 'NULL'}, "
                f"{sql_escape(t['routine_rw'])}, {sql_escape(t['priority_rw'])}, "
                f"{sql_escape(t['importance_rw'])}, {sql_escape(t['kiro_rw'])}, "
                f"{sql_escape(t['next_action_rw'])}, "
                f"{'CAST(' + sql_escape(t['begin_date_rw']) + ' AS DATE)' if t['begin_date_rw'] else 'NULL'}, "
                f"CURRENT_TIMESTAMP)"
            )
            values_parts.append(vals)
        
        sql = f"""INSERT INTO asana.asana_tasks 
            (task_gid, name, assignee_gid, project_name, project_gid, section_name, 
             due_on, start_on, completed, completed_at, routine_rw, priority_rw, 
             importance_rw, kiro_rw, next_action_rw, begin_date_rw, synced_at)
        VALUES {', '.join(values_parts)}
        ON CONFLICT (task_gid) DO UPDATE SET
            name = EXCLUDED.name, assignee_gid = EXCLUDED.assignee_gid,
            project_name = EXCLUDED.project_name, project_gid = EXCLUDED.project_gid,
            section_name = EXCLUDED.section_name, due_on = EXCLUDED.due_on,
            start_on = EXCLUDED.start_on, completed = EXCLUDED.completed,
            completed_at = EXCLUDED.completed_at, routine_rw = EXCLUDED.routine_rw,
            priority_rw = EXCLUDED.priority_rw, importance_rw = EXCLUDED.importance_rw,
            kiro_rw = EXCLUDED.kiro_rw, next_action_rw = EXCLUDED.next_action_rw,
            begin_date_rw = EXCLUDED.begin_date_rw,
            deleted_at = NULL, synced_at = CURRENT_TIMESTAMP;"""
        
        # Write SQL to file and execute via DuckDB CLI or MCP
        sql_file = "/tmp/_asana_upsert.sql"
        with open(sql_file, "w") as f:
            f.write(sql)
        
        # Use duckdb MCP via the binary
        duckdb_req = json.dumps({
            "jsonrpc": "2.0", "id": 1,
            "method": "tools/call",
            "params": {"name": "execute_query", "arguments": {"sql": sql}}
        })
        
        tmpfile = "/tmp/_duckdb_req.json"
        with open(tmpfile, "w") as f:
            f.write(duckdb_req)
        
        try:
            # Use uvx to call the duckdb MCP
            p = subprocess.run(
                ["bash", "-c", f'cat {tmpfile} | timeout 30 uvx mcp-server-motherduck --db-path "md:ps_analytics" --read-write 2>/dev/null'],
                capture_output=True, text=True, timeout=45,
                env={**os.environ, "HOME": "/home/prichwil"}
            )
            if p.returncode == 0 and p.stdout.strip():
                resp = json.loads(p.stdout.strip())
                if "error" not in resp:
                    total_upserted += len(batch)
                else:
                    errors.append(f"Batch {batch_start}: {resp.get('error', {}).get('message', 'unknown')}")
            else:
                errors.append(f"Batch {batch_start}: exit={p.returncode}")
        except Exception as e:
            errors.append(f"Batch {batch_start}: {e}")
        
        print(f"  Upserted batch {batch_start//batch_size + 1} ({len(batch)} tasks, total: {total_upserted})")
    
    print(f"\n  Total upserted: {total_upserted}")
    if errors:
        print(f"  Errors: {len(errors)}")
        for e in errors:
            print(f"    ! {e}")
    
    return total_upserted, errors


def main():
    print(f"{'='*60}")
    print(f"FULL ASANA → DUCKDB SYNC — {TODAY}")
    print(f"{'='*60}\n")
    
    # Step 1: Pull Richard's tasks
    richard_tasks = step1_pull_richard_tasks()
    
    # Step 2: Pull portfolio project tasks
    project_tasks = step2_pull_project_tasks()
    
    # Step 3: Merge (deduplicate by task_gid)
    print("\n" + "=" * 60)
    print("STEP 3: Merge and deduplicate")
    print("=" * 60)
    
    all_tasks = {**project_tasks}  # Start with project tasks
    for gid, task in richard_tasks.items():
        if gid not in all_tasks:
            all_tasks[gid] = task
        else:
            # Richard's task details take priority (has assignee info)
            all_tasks[gid] = task
    
    print(f"  Richard's tasks: {len(richard_tasks)}")
    print(f"  Project tasks: {len(project_tasks)}")
    print(f"  Merged unique: {len(all_tasks)}")
    
    # Save merged tasks to JSON for DuckDB sync
    output_file = "/tmp/asana_full_sync_tasks.json"
    with open(output_file, "w") as f:
        json.dump(all_tasks, f, indent=2, default=str)
    print(f"  Saved to {output_file}")
    
    # Print summary by project
    by_project = {}
    for t in all_tasks.values():
        pn = t.get("project_name") or "No Project"
        by_project[pn] = by_project.get(pn, 0) + 1
    
    print("\n  Tasks by project:")
    for pn, count in sorted(by_project.items()):
        print(f"    {pn}: {count}")
    
    # Output all GIDs for soft-delete step
    gids_file = "/tmp/asana_synced_gids.json"
    with open(gids_file, "w") as f:
        json.dump(list(all_tasks.keys()), f)
    print(f"\n  GIDs saved to {gids_file}")
    
    return all_tasks


if __name__ == "__main__":
    all_tasks = main()
    print(f"\n\nDone. {len(all_tasks)} tasks ready for DuckDB sync.")
    print("Run DuckDB UPSERT separately via MCP.")
