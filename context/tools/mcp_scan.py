import subprocess, json, sys

def mcp_call(tool_name, arguments):
    req = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    })
    p = subprocess.run(
        ["aws-outlook-mcp"],
        input=req,
        capture_output=True,
        text=True,
        timeout=30
    )
    if p.stdout:
        data = json.loads(p.stdout)
        if "result" in data:
            text = data["result"]["content"][0]["text"]
            inner = json.loads(text)
            return inner["content"][0]["text"]
    return None

# 1. Calendar for today (3/18) and tomorrow (3/19)
print("=== CALENDAR (3/18 - 3/19) ===")
cal = mcp_call("calendar_view", {"start_date": "2026-03-18", "end_date": "2026-03-19"})
if cal:
    events = json.loads(cal)
    for e in events:
        s = e.get("start","")
        if "2026-03-18" in s or "2026-03-19" in s:
            print(f"  {s[11:16]}Z | {e['subject']} | Status: {e['status']} | Resp: {e['response']} | Org: {e.get('organizer',{}).get('name','?')}")

# 2. Recent emails
print("\n=== RECENT EMAILS (since 3/17) ===")
emails_raw = mcp_call("email_search", {"query": "received:>=2026-03-17", "max_results": 25})
if emails_raw:
    emails_data = json.loads(emails_raw)
    for e in emails_data["content"]["emails"]:
        sender = e["senders"][0] if e["senders"] else "?"
        print(f"  {e['lastDeliveryTime'][:16]} | {sender} | {e['topic'][:90]} | Unread: {e['unreadCount']}")

# 3. To-Do lists
print("\n=== TO-DO LISTS ===")
lists_raw = mcp_call("todo_lists", {"operation": "list"})
if lists_raw:
    lists_data = json.loads(lists_raw)
    if isinstance(lists_data, dict) and "lists" in lists_data:
        for l in lists_data["lists"]:
            print(f"  {l.get('displayName','?')} | ID: {l.get('id','')[:40]}... | Tasks: {l.get('taskCount','?')}")
    else:
        print(f"  Raw: {str(lists_data)[:500]}")
