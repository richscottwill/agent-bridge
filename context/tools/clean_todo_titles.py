#!/usr/bin/env python3
"""Remove emojis from To-Do task titles and replace with plain text markers."""
import json, os

SWEEP_ID = "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESHAAA="
CORE_ID = "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESIAAA="
ENGINE_ID = "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESJAAA="
ADMIN_ID = "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESKAAA="
BACKLOG_ID = "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADWyS4nAAA="

# Emoji to text mapping
REPLACEMENTS = {
    "\U0001f534 ": "[OVERDUE] ",   # red circle
    "\U0001f7e1 ": "[THIS WEEK] ", # yellow circle
    "\U0001f7e2 ": "[BACKLOG] ",   # green circle
    "\U0001f9f9 ": "[CLEANUP] ",   # broom
    "\U0001f534": "[OVERDUE]",     # red circle (no trailing space)
    "\U0001f7e1": "[THIS WEEK]",   # yellow circle (no trailing space)
    "\U0001f7e2": "[BACKLOG]",     # green circle (no trailing space)
    "\U0001f9f9": "[CLEANUP]",     # broom (no trailing space)
    "\u2014": " - ",               # em dash
    "\u2013": " - ",               # en dash
    "\u2192": "->",                # right arrow
    "\u2190": "<-",                # left arrow
    "\u2705": "[done]",            # check mark
    "\u26A0\uFE0F": "[!]",        # warning sign with variation
    "\u26A0": "[!]",              # warning sign
    "\u2022": "-",                 # bullet
    "\u201c": '"',                 # left curly quote
    "\u201d": '"',                 # right curly quote
    "\u2018": "'",                 # left single curly quote
    "\u2019": "'",                 # right single curly quote
    "\u00ed": "i",                 # accented i (clinica)
    "\u00e9": "e",                 # accented e (esteticas)
}

def mcp_call(tool_name, arguments):
    req = json.dumps({
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    })
    # Write to temp file to avoid shell escaping issues with body content
    tmpfile = os.path.expanduser("~/shared/context/intake/_mcp_req.json")
    with open(tmpfile, "w") as f:
        f.write(req)
    # Use cat pipe which avoids shell interpretation of content
    cmd = f"cat {tmpfile} | timeout 15 aws-outlook-mcp 2>/dev/null"
    result = os.popen(cmd).read().strip()
    if not result:
        # Fallback: try echo pipe for simple requests
        safe = req.replace("'", "'\\''")
        cmd2 = f"echo '{safe}' | timeout 15 aws-outlook-mcp 2>/dev/null"
        result = os.popen(cmd2).read().strip()
    if not result:
        return None
    data = json.loads(result)
    if "result" in data:
        text = data["result"]["content"][0]["text"]
        inner = json.loads(text)
        if "content" in inner and isinstance(inner["content"], list):
            return inner["content"][0]["text"]
        elif "content" in inner and isinstance(inner["content"], dict):
            return json.dumps(inner["content"])
        else:
            return json.dumps(inner)
    if "error" in data:
        return json.dumps({"success": False, "error": str(data["error"])})
    return None

def clean_title(title):
    new_title = title
    for old, new in REPLACEMENTS.items():
        new_title = new_title.replace(old, new)
    return new_title

def process_list(list_name, list_id):
    print(f"\n=== {list_name} ===")
    raw = mcp_call("todo_tasks", {"operation": "list", "listId": list_id})
    if not raw:
        print("  No response")
        return
    parsed = json.loads(raw)
    tasks = parsed.get("content", {}).get("tasks", [])
    
    for task in tasks:
        old_title = task["title"]
        old_body = task.get("body", "") or ""
        new_title = clean_title(old_title)
        new_body = clean_title(old_body)
        
        title_changed = old_title != new_title
        body_changed = old_body != new_body
        
        if not title_changed and not body_changed:
            print(f"  SKIP (no change): {old_title[:60]}")
            continue
        
        task_id = task["id"]
        changes = []
        if title_changed:
            changes.append("title")
        if body_changed:
            changes.append("body")
        print(f"  UPDATE ({', '.join(changes)}): {old_title[:60]}")
        
        update_args = {
            "operation": "update",
            "listId": list_id,
            "taskId": task_id,
        }
        if title_changed:
            update_args["title"] = new_title
        if body_changed:
            update_args["body"] = new_body
        
        result = mcp_call("todo_tasks", update_args)
        if result:
            r = json.loads(result)
            if r.get("success"):
                print(f"      OK")
            else:
                print(f"      FAIL: {str(r)[:100]}")
        else:
            print(f"      NO RESPONSE")

# Process remaining lists (Sweep, Core, Engine Room already done)
for name, lid in [
    ("Admin", ADMIN_ID),
    ("Backlog", BACKLOG_ID),
]:
    process_list(name, lid)

print("\nDone.")
