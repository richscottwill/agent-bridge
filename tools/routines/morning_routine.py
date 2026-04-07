#!/usr/bin/env python3
"""Morning Routine — MCP-based Outlook + Hedy integration"""
import json, os, subprocess, sys, re
from datetime import datetime

TMPFILE = os.path.expanduser("~/shared/context/intake/_mcp_req.json")

# To-Do List IDs
LISTS = {
    "sweep": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESHAAA=",
    "core": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESIAAA=",
    "engine": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESJAAA=",
    "admin": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESKAAA=",
    "backlog": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADWyS4nAAA=",
}

AUTO_COMMS_ID = "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQpAAA="

SKIP_FOLDERS = {
    "Deleted Items", "Sync Issues", "Conflicts", "Auto-Comms", "Calendar",
    "Tasks", "Junk Email", "Sent Items", "Drafts", "Outbox",
    "Conversation History", "RSS Feeds", "Social Activity Notifications",
    "Auto", "Auto Important", "Auto-Adobe", "Auto-meeting", "Auto-Office",
    "Auto-PS", "Auto-Google", "Auto-Asana", "Auto-MS", "Auto-Quip",
    "Auto-Wiki", "Auto-Chime", "Auto-Slack", "Auto-IT", "Auto-HR",
    "Auto-Legal", "Auto-Finance", "Auto-Ops", "Auto-Data",
    "Clutter", "Notes", "Journal", "Suggested Contacts",
}

def outlook_call(tool_name, arguments):
    """Call aws-outlook-mcp with proper MCP init handshake"""
    init_req = json.dumps({
        "jsonrpc": "2.0", "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "kiro", "version": "1.0.0"}
        }
    })
    tool_req = json.dumps({
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    })
    with open(TMPFILE, "w") as f:
        f.write(init_req + "\n" + tool_req + "\n")
    
    try:
        p = subprocess.run(
            ["bash", "-c", f"cat {TMPFILE} | timeout 30 aws-outlook-mcp"],
            capture_output=True, text=True, timeout=35
        )
        if not p.stdout.strip():
            return None
        # Parse line by line - second line is the tool response
        lines = [l.strip() for l in p.stdout.strip().split("\n") if l.strip()]
        if len(lines) < 2:
            return None
        data = json.loads(lines[1])
        if "result" in data:
            text = data["result"]["content"][0]["text"]
            inner = json.loads(text)
            actual = inner["content"][0]["text"]
            try:
                return json.loads(actual)
            except:
                return actual
        return None
    except Exception as e:
        print(f"ERROR calling {tool_name}: {e}", file=sys.stderr)
        return None

def run_step(name):
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")

# ============================================================
# STEP 1: ASANA SYNC
# ============================================================
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "step1"
    
    if mode == "step1":
        run_step("STEP 1: ASANA SYNC — Scanning Auto-Comms")
        
        result = outlook_call("email_search", {
            "query": "received:>=2026-03-21",
            "max_results": 25,
            "folderId": AUTO_COMMS_ID
        })
        
        if result and isinstance(result, dict) and result.get("success"):
            emails = result.get("content", {}).get("emails", [])
            total = result.get("content", {}).get("totalResults", 0)
            print(f"\nFound {len(emails)} conversations ({total} total) in Auto-Comms since 3/21")
            
            for i, email in enumerate(emails):
                print(f"\n--- Email {i+1} ---")
                print(f"  Topic: {email.get('topic', 'N/A')}")
                print(f"  Senders: {email.get('senders', [])}")
                print(f"  Time: {email.get('lastDeliveryTime', 'N/A')}")
                print(f"  Unread: {email.get('unreadCount', 0)}")
                print(f"  ConvID: {email.get('conversationId', 'N/A')}")
                preview = email.get("preview", "")[:150]
                print(f"  Preview: {preview}")
        else:
            print(f"No results or error: {result}")
    
    elif mode == "folders":
        run_step("EMAIL FOLDERS — Finding unread")
        result = outlook_call("email_list_folders", {})
        if result and isinstance(result, dict):
            folders = result.get("content", {}).get("folders", [])
            print(f"\nTotal folders: {len(folders)}")
            print("\nFolders with unread:")
            for f in folders:
                if f.get("unreadCount", 0) > 0:
                    name = f.get("name", "?")
                    skip = "SKIP" if name in SKIP_FOLDERS else "CHECK"
                    print(f"  [{skip}] {name}: {f['unreadCount']} unread (total: {f.get('totalCount', '?')})")
                    if skip == "CHECK":
                        print(f"    ID: {f.get('id', 'N/A')}")
        else:
            print(f"Error: {result}")
    
    elif mode == "calendar":
        run_step("CALENDAR — Today's meetings")
        result = outlook_call("calendar_view", {
            "start_date": "2026-03-23",
            "end_date": "2026-03-24"
        })
        if result:
            if isinstance(result, list):
                events = result
            elif isinstance(result, dict):
                events = result.get("content", result.get("events", [result]))
            else:
                events = []
                print(f"Unexpected calendar format: {type(result)}")
            
            print(f"\nFound {len(events)} events today (Mon 3/23)")
            for e in events:
                subj = e.get("subject", "?")
                start = e.get("start", "?")
                end = e.get("end", "?")
                status = e.get("status", "?")
                org = e.get("organizer", {}).get("name", "?")
                canceled = e.get("isCanceled", False)
                resp = e.get("response", "?")
                print(f"\n  {subj}")
                print(f"    Time: {start} - {end}")
                print(f"    Status: {status} | Response: {resp} | Organizer: {org}")
                if canceled:
                    print(f"    *** CANCELED ***")
        else:
            print("No calendar data returned")
    
    elif mode == "todo":
        run_step("TO-DO LISTS — Current state")
        for name, lid in LISTS.items():
            result = outlook_call("todo_tasks", {"operation": "list", "listId": lid})
            if result and isinstance(result, dict):
                tasks = result.get("content", {}).get("tasks", [])
                active = [t for t in tasks if t.get("status") != "completed"]
                print(f"\n📋 {name.upper()} ({len(active)} active, {len(tasks)} total)")
                for t in active:
                    title = t.get("title", "?")
                    due = t.get("dueDateTime", "none")
                    imp = t.get("importance", "normal")
                    marker = "🔴" if imp == "high" else "⚪"
                    print(f"  {marker} {title} (due: {due})")
            else:
                print(f"\n📋 {name.upper()} — error fetching")
