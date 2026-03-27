#!/usr/bin/env python3
"""Read key new emails and check Auto-Comms folder."""
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

# Read Andrew's Testing Doc mention
print("=== ANDREW TESTING DOC MENTION ===")
raw = mcp_call("email_read", {
    "conversationId": "AAQkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAQAIGSNkSniVBLpvhqYlt3T8k=",
    "format": "text"
})
if raw:
    parsed = json.loads(raw)
    if isinstance(parsed, dict) and "content" in parsed:
        emails = parsed["content"].get("emails", [parsed["content"]])
        for e in (emails if isinstance(emails, list) else [emails]):
            print(f"From: {e.get('from','?')}")
            print(f"Subject: {e.get('subject','?')}")
            body = e.get('body','')
            print(f"Body: {body[:500]}")
    else:
        print(str(parsed)[:800])
else:
    print("No response")

# Read Sharon Prime Day email
print("\n=== SHARON PRIME DAY INTAKE ===")
raw2 = mcp_call("email_read", {
    "conversationId": "AAQkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAQAE0w6Iw/X7NDg/j+tOOH3eU=",
    "format": "text"
})
if raw2:
    parsed2 = json.loads(raw2)
    if isinstance(parsed2, dict) and "content" in parsed2:
        emails2 = parsed2["content"].get("emails", [parsed2["content"]])
        for e in (emails2 if isinstance(emails2, list) else [emails2]):
            print(f"From: {e.get('from','?')}")
            print(f"Subject: {e.get('subject','?')}")
            body = e.get('body','')
            print(f"Body: {body[:500]}")
    else:
        print(str(parsed2)[:800])
else:
    print("No response")

# Read Asana daily digest
print("\n=== ASANA DAILY DIGEST ===")
raw3 = mcp_call("email_read", {
    "conversationId": "AAQkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAQAI4hQbVPt85Gtd2i0rpsg/8=",
    "format": "text"
})
if raw3:
    parsed3 = json.loads(raw3)
    if isinstance(parsed3, dict) and "content" in parsed3:
        emails3 = parsed3["content"].get("emails", [parsed3["content"]])
        for e in (emails3 if isinstance(emails3, list) else [emails3]):
            body = e.get('body','')
            print(f"Body: {body[:600]}")
    else:
        print(str(parsed3)[:800])
else:
    print("No response")

# Check Auto-Comms folder for Asana notifications
print("\n=== AUTO-COMMS (Asana notifications) ===")
raw4 = mcp_call("email_search", {
    "query": "received:>=2026-03-17",
    "max_results": 10,
    "folderId": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQpAAA="
})
if raw4:
    parsed4 = json.loads(raw4)
    emails4 = parsed4.get("content", {}).get("emails", [])
    if emails4:
        for e in emails4:
            sender = e["senders"][0] if e.get("senders") else "?"
            print(f"  {e.get('lastDeliveryTime','?')[:16]} | {sender} | {e.get('topic','?')[:90]}")
    else:
        print("  No Asana notifications found in Auto-Comms")
else:
    print("  No response from Auto-Comms search")
