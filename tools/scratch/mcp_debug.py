import subprocess, json, sys

def mcp_call_raw(tool_name, arguments):
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
    return p.stdout, p.stderr

# Debug calendar
print("=== CALENDAR RAW ===")
out, err = mcp_call_raw("calendar_view", {"start_date": "2026-03-18", "end_date": "2026-03-19"})
if out:
    data = json.loads(out)
    # Print structure
    content = data.get("result", {}).get("content", [])
    if content:
        text = content[0].get("text", "")
        # Try parsing as JSON
        try:
            inner = json.loads(text)
            print(f"Type of inner: {type(inner)}")
            if isinstance(inner, dict):
                print(f"Keys: {list(inner.keys())}")
                if "content" in inner:
                    print(f"Inner content type: {type(inner['content'])}")
                    if isinstance(inner['content'], list):
                        for item in inner['content']:
                            print(f"  Item type: {type(item)}, keys: {list(item.keys()) if isinstance(item, dict) else 'N/A'}")
                            if isinstance(item, dict) and 'text' in item:
                                print(f"  Text[:200]: {item['text'][:200]}")
                else:
                    print(f"Full inner[:500]: {json.dumps(inner)[:500]}")
            elif isinstance(inner, list):
                print(f"List len: {len(inner)}")
                if inner:
                    print(f"First item[:200]: {json.dumps(inner[0])[:200]}")
            else:
                print(f"Raw[:500]: {str(inner)[:500]}")
        except json.JSONDecodeError:
            print(f"Not JSON. Raw text[:500]: {text[:500]}")
    else:
        print("No content in result")
if err:
    print(f"STDERR: {err[:200]}")

# Debug todo_lists
print("\n=== TODO LISTS RAW ===")
out2, err2 = mcp_call_raw("todo_lists", {"operation": "list"})
if out2:
    data2 = json.loads(out2)
    content2 = data2.get("result", {}).get("content", [])
    if content2:
        text2 = content2[0].get("text", "")
        try:
            inner2 = json.loads(text2)
            print(f"Type: {type(inner2)}, Keys: {list(inner2.keys()) if isinstance(inner2, dict) else 'N/A'}")
            print(f"Content[:500]: {json.dumps(inner2)[:500]}")
        except:
            print(f"Raw[:500]: {text2[:500]}")
if err2:
    print(f"STDERR: {err2[:200]}")
