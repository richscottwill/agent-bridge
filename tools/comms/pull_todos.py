#!/usr/bin/env python3
"""Pull all tasks from the 5 active To-Do lists via MCP."""
import subprocess, json, os

LISTS = {
    "Sweep": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESHAAA=",
    "Core": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESIAAA=",
    "Engine Room": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESJAAA=",
    "Admin": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESKAAA=",
    "Backlog": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADWyS4nAAA=",
}

def mcp_call(tool_name, arguments):
    req = json.dumps({
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    })
    cmd = f"echo '{req}' | timeout 15 aws-outlook-mcp 2>/dev/null"
    result = os.popen(cmd).read().strip()
    if not result:
        return None
    data = json.loads(result)
    if "result" in data:
        text = data["result"]["content"][0]["text"]
        inner = json.loads(text)
        return inner["content"][0]["text"]
    return None

all_tasks = {}
for name, list_id in LISTS.items():
    raw = mcp_call("todo_tasks", {"operation": "list", "listId": list_id})
    if raw:
        parsed = json.loads(raw)
        tasks = parsed.get("content", {}).get("tasks", [])
        all_tasks[name] = tasks
        print(f"\n=== {name} ({len(tasks)} tasks) ===")
        for t in tasks:
            status = t.get("status", "?")
            imp = t.get("importance", "?")
            due = t.get("dueDateTime", "none")
            title = t.get("title", "?")
            print(f"  [{status}] {imp} | Due: {due} | {title}")
    else:
        all_tasks[name] = []
        print(f"\n=== {name} (0 tasks - no response) ===")

# Save structured output
outpath = os.path.expanduser("~/shared/context/intake/todo_snapshot.json")
with open(outpath, "w") as f:
    json.dump(all_tasks, f, indent=2)
print(f"\nSaved to {outpath}")
