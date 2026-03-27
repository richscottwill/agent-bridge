import subprocess, json, sys, os

# The MCP stdio transport might need newline-terminated JSON
# Try different approaches

req = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "calendar_view",
        "arguments": {
            "start_date": "2026-03-18",
            "end_date": "2026-03-19"
        }
    }
})

# Approach 1: Use os.popen with echo pipe (mimics what worked in bash)
print("=== Approach 1: os.popen ===")
cmd = f"echo '{req}' | aws-outlook-mcp 2>/dev/null"
result = os.popen(cmd).read()
print(f"Result len: {len(result)}")
if result:
    print(f"Result[:500]: {result[:500]}")
