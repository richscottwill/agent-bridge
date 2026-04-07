#!/usr/bin/env python3
"""Asana ↔ To-Do Sync Protocol — scans Auto-Comms for Asana emails, syncs to To-Do lists."""

import json
import os
import re
import subprocess
import sys
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")
MCP_BIN = os.path.expanduser("~/.toolbox/bin/aws-outlook-mcp")

def mcp_call(tool_name, arguments):
    """Call aws-outlook-mcp and return parsed Layer 3 data."""
    req_json = json.dumps({
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    })
    # Must use bash -c with echo pipe — binary doesn't work with subprocess stdin
    tmpfile = "/tmp/_mcp_req.json"
    with open(tmpfile, "w") as f:
        f.write(req_json)
    try:
        p = subprocess.run(
            ["bash", "-c", f"cat {tmpfile} | timeout 30 {MCP_BIN} 2>/dev/null"],
            capture_output=True, text=True, timeout=45
        )
        raw = p.stdout.strip()
    except Exception as e:
        print(f"  ERROR ({tool_name}): {e}", file=sys.stderr)
        return None
    if not raw:
        print(f"  Empty response from {tool_name}", file=sys.stderr)
        return None
    try:
        data = json.loads(raw)
        if "error" in data:
            print(f"  MCP ERROR ({tool_name}): {data['error']}", file=sys.stderr)
            return None
        layer2 = json.loads(data["result"]["content"][0]["text"])
        content = layer2.get("content")
        if isinstance(content, list) and content:
            return json.loads(content[0]["text"])
        elif isinstance(content, dict):
            return content
        return layer2
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"  Parse error ({tool_name}): {e}", file=sys.stderr)
        return None


# --- Constants ---
AUTO_COMMS = "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQpAAA="
LISTS = {
    "sweep":   ("🧹 Sweep",       "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESHAAA="),
    "core":    ("🎯 Core",        "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESIAAA="),
    "engine":  ("⚙️ Engine Room", "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESJAAA="),
    "admin":   ("📋 Admin",       "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESKAAA="),
    "backlog": ("📦 Backlog",     "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADWyS4nAAA="),
}

def extract_asana_id(text):
    for pat in [r'app\.asana\.com.*/0/\d+/(\d+)', r'/task/(\d+)', r'asana\.com.*?/(\d{10,})']:
        m = re.search(pat, text)
        if m: return m.group(1)
    return None

def classify(subject, body):
    t = (subject + " " + body).lower()
    for kw, typ in [("assigned","assigned"),("completed","completed"),("marked complete","completed"),
                     ("commented","commented"),("comment","commented"),("due date","due_date"),("due soon","due_date")]:
        if kw in t: return typ
    return "unknown"

def pick_list(subject, body):
    t = (subject + " " + body).lower()
    if any(w in t for w in ["reply","respond","send","forward","follow up"]): return "sweep"
    if any(w in t for w in ["framework","strategy","design","test plan","pov","artifact"]): return "core"
    if any(w in t for w in ["campaign","bid","keyword","google ads","sitelink","oci","negative"]): return "engine"
    if any(w in t for w in ["invoice","po ","budget","compliance","purchase order"]): return "admin"
    return "backlog"

def safe_get(d, *keys, default=None):
    """Safely navigate nested dicts."""
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, default)
        else:
            return default
    return d


def run_sync():
    res = {"emails_scanned": 0, "new": [], "updated": [], "skipped": [], "issues": []}

    # Step 1: Search Auto-Comms for recent Asana emails
    print("Step 1: Scanning Auto-Comms...")
    data = mcp_call("email_search", {
        "query": "from:asana received:>=2026-03-18",
        "max_results": 25,
        "folderId": AUTO_COMMS
    })
    if not data:
        res["issues"].append("Could not search Auto-Comms")
        return res

    emails = safe_get(data, "content", "emails", default=[]) or data.get("emails", [])
    res["emails_scanned"] = len(emails)
    print(f"  Found {len(emails)} email(s)")
    if not emails:
        return res

    # Step 2: Index existing To-Do tasks by Asana ID
    print("\nStep 2: Indexing To-Do tasks...")
    existing = {}  # asana_id -> {key, tid, title, body}
    for key, (name, lid) in LISTS.items():
        td = mcp_call("todo_tasks", {"operation": "list", "listId": lid})
        tasks = safe_get(td, "content", "tasks", default=[]) or td.get("tasks", []) if td else []
        print(f"  {name}: {len(tasks)} tasks")
        for t in tasks:
            body = t.get("body", "") or ""
            m = re.search(r'ASANA:\s*(\d+)', body)
            if m:
                existing[m.group(1)] = {"key": key, "tid": t.get("id"), "title": t.get("title",""), "body": body}
    print(f"  {len(existing)} tasks with Asana IDs")

    # Step 3: Process each email
    print("\nStep 3: Processing...")
    for i, em in enumerate(emails):
        cid = em.get("conversationId", "")
        subj = em.get("topic", "") or ""
        preview = em.get("preview", "")
        print(f"\n  [{i+1}/{len(emails)}] {subj[:70]}")

        # Read full email
        rd = mcp_call("email_read", {"conversationId": cid, "format": "text"})
        body = ""
        if rd:
            em_list = safe_get(rd, "content", "emails", default=[]) or rd.get("emails", [])
            if em_list:
                body = em_list[0].get("body", "") or ""
        if not body:
            body = preview

        aid = extract_asana_id(body) or extract_asana_id(preview)
        if not aid:
            print(f"    SKIP: no task ID")
            res["skipped"].append(subj[:80])
            continue

        ntype = classify(subj, body)
        print(f"    Asana:{aid} type:{ntype}")

        if aid in existing:
            # Update existing
            match = existing[aid]
            lname = LISTS[match["key"]][0]
            print(f"    MATCH in {lname}: {match['title'][:50]}")

            entry = f"[{TODAY}] {ntype}"
            if ntype == "completed":
                entry += " — complete in Asana (close in To-Do if done)"

            old = match["body"]
            if "--- SYNC LOG ---" in old:
                new_body = re.sub(r'(LAST_SYNCED:)', f'{entry}\n\\1', old)
                new_body = re.sub(r'LAST_SYNCED:.*', f'LAST_SYNCED: {TODAY}', new_body)
            else:
                new_body = old + f"\n\n--- SYNC LOG ---\n{entry}\nLAST_SYNCED: {TODAY}"

            r = mcp_call("todo_tasks", {
                "operation": "update",
                "listId": LISTS[match["key"]][1],
                "taskId": match["tid"],
                "body": new_body
            })
            if r:
                print(f"    UPDATED")
                res["updated"].append({"title": match["title"], "list": lname, "type": ntype, "aid": aid})
            else:
                print(f"    UPDATE FAILED")
                res["issues"].append(f"Update failed: {match['title'][:40]}")
        else:
            # Create new
            tgt = pick_list(subj, body)
            lname = LISTS[tgt][0]
            print(f"    NEW → {lname}")

            tname = subj
            for pfx in ["You've been assigned a task: ", "New task: ", "You've been assigned "]:
                tname = tname.replace(pfx, "")
            tname = tname.strip()[:250]

            tbody = (
                f"STATUS: New from Asana (synced {TODAY})\nASANA: {aid}\n\n"
                f"WHAT TO DO:\n{tname}\n\n"
                f"KEY DETAILS:\n- Source: Asana ({ntype})\n- Due: Unknown\n\n"
                f"WHY IT MATTERS:\nNeeds triage\n\n"
                f"--- SYNC LOG ---\n[{TODAY}] Created from Asana notification\nLAST_SYNCED: {TODAY}"
            )

            r = mcp_call("todo_tasks", {
                "operation": "create",
                "listId": LISTS[tgt][1],
                "title": tname,
                "body": tbody
            })
            if r:
                print(f"    CREATED")
                res["new"].append({"title": tname[:80], "list": lname, "aid": aid})
            else:
                print(f"    CREATE FAILED")
                res["issues"].append(f"Create failed: {tname[:40]}")

    return res


if __name__ == "__main__":
    print(f"=== Asana ↔ To-Do Sync — {TODAY} ===\n")
    r = run_sync()

    print(f"\n{'='*50}")
    print(f"SYNC COMPLETE — {TODAY}")
    print(f"{'='*50}")
    print(f"Emails scanned: {r['emails_scanned']}")
    print(f"New tasks created: {len(r['new'])}")
    for t in r["new"]:
        print(f"  + [{t['list']}] {t['title']}")
    print(f"Tasks updated: {len(r['updated'])}")
    for t in r["updated"]:
        print(f"  ~ [{t['list']}] {t['title']} ({t['type']})")
    print(f"Skipped: {len(r['skipped'])}")
    for s in r["skipped"]:
        print(f"  - {s}")
    if r["issues"]:
        print(f"Issues: {len(r['issues'])}")
        for x in r["issues"]:
            print(f"  ! {x}")

    with open(os.path.expanduser("~/shared/context/intake/_sync_results.json"), "w") as f:
        json.dump(r, f, indent=2)
