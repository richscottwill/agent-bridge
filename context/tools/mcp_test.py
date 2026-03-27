import subprocess, json, sys

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

# Try with explicit stdin close via communicate
p = subprocess.Popen(
    ["aws-outlook-mcp"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
stdout, stderr = p.communicate(input=req, timeout=30)
print(f"STDOUT len: {len(stdout)}")
print(f"STDERR len: {len(stderr)}")
if stdout:
    print(f"STDOUT[:1000]: {stdout[:1000]}")
if stderr:
    print(f"STDERR[:500]: {stderr[:500]}")
