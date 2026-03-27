#!/usr/bin/env python3
"""Read Sharon Prime Day email and MS Advertising paused."""
import json, os

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

# Sharon Prime Day
print("=== SHARON PRIME DAY ===")
raw = mcp_call("email_read", {
    "conversationId": "AAQkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAQAE0w6Iw/X7NDg/j+tOOH3eU=",
    "format": "text"
})
if raw:
    parsed = json.loads(raw)
    # Try to get all emails in conversation
    content = parsed.get("content", {})
    emails = content.get("emails", [])
    if emails:
        for e in emails:
            print(f"From: {e.get('from',{}).get('name','?') if isinstance(e.get('from'), dict) else e.get('from','?')}")
            print(f"Subject: {e.get('subject','?')}")
            body = e.get('body','')
            print(f"Body[:600]: {body[:600]}")
            print("---")
    else:
        print(str(parsed)[:1000])

# MS Advertising paused (just one to check)
print("\n=== MS ADVERTISING PAUSED ===")
raw2 = mcp_call("email_search", {
    "query": "from:Microsoft Advertising received:>=2026-03-17",
    "max_results": 3
})
if raw2:
    parsed2 = json.loads(raw2)
    emails2 = parsed2.get("content", {}).get("emails", [])
    for e in emails2[:1]:
        print(f"Topic: {e.get('topic','?')}")
        print(f"Preview: {e.get('preview','?')[:300]}")
