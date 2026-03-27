# aws-outlook-mcp — Tool Reference

Last updated: 2026-03-20
Source: Reverse-engineered from working scripts in ~/shared/context/intake/

## How to Call (CLI / Python)

The `aws-outlook-mcp` binary speaks JSON-RPC 2.0 over stdin/stdout. Every call follows this pattern:

### Request Format
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "<tool_name>",
    "arguments": { ... }
  }
}
```

### Response Format (triple-nested JSON)
```
Layer 1: {"result": {"content": [{"type": "text", "text": "<layer2>"}]}, "jsonrpc": "2.0", "id": 1}
Layer 2: {"content": [{"type": "text", "text": "<layer3>"}]}
Layer 3: The actual data (JSON string — parse again)
```

### Invocation Methods

**Method 1: echo pipe (simple requests, no special chars in body)**
```bash
echo '<json_request>' | timeout 15 aws-outlook-mcp 2>/dev/null
```

**Method 2: cat pipe (complex requests with HTML/special chars)**
```bash
# Write request to temp file first
cat /path/to/request.json | timeout 15 aws-outlook-mcp 2>/dev/null
```

**Method 3: subprocess.run (Python)**
```python
p = subprocess.run(
    ["aws-outlook-mcp"],
    input=req_json_string,
    capture_output=True,
    text=True,
    timeout=30
)
```

### Python Helper Function (proven working)
```python
import json, os

def mcp_call(tool_name, arguments):
    req = json.dumps({
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    })
    # Write to temp file to avoid shell escaping issues
    tmpfile = os.path.expanduser("~/shared/context/intake/_mcp_req.json")
    with open(tmpfile, "w") as f:
        f.write(req)
    cmd = f"cat {tmpfile} | timeout 15 aws-outlook-mcp 2>/dev/null"
    result = os.popen(cmd).read().strip()
    if not result:
        return None
    data = json.loads(result)
    if "result" in data:
        text = data["result"]["content"][0]["text"]
        inner = json.loads(text)
        return inner["content"][0]["text"]
    return None
```

---

## Tools

### 1. email_search
Search emails, optionally within a specific folder.

**Arguments:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | yes | Outlook search query (KQL syntax) |
| max_results | int | no | Max emails to return (default varies) |
| folderId | string | no | Outlook folder ID to search within |

**Example — search inbox:**
```json
{"name": "email_search", "arguments": {
  "query": "received:>=2026-03-17",
  "max_results": 25
}}
```

**Example — search Auto-Comms folder:**
```json
{"name": "email_search", "arguments": {
  "query": "received:>=2026-03-17",
  "max_results": 10,
  "folderId": "AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQpAAA="
}}
```

**Example — search by sender:**
```json
{"name": "email_search", "arguments": {
  "query": "from:Microsoft Advertising received:>=2026-03-17",
  "max_results": 3
}}
```

**Response (Layer 3):**
```json
{
  "success": true,
  "content": {
    "message": "Found 25 emails (showing 0 to 25 of 122 total results).",
    "emails": [
      {
        "conversationId": "AAQk...",
        "topic": "Subject line",
        "senders": ["Sender Name"],
        "lastDeliveryTime": "2026-03-18T15:09:55+00:00",
        "preview": "First ~200 chars of body...",
        "unreadCount": 1,
        "items": []
      }
    ],
    "totalResults": 122,
    "offset": 0,
    "limit": 25
  }
}
```

---

### 2. email_read
Read full email conversation by conversationId.

**Arguments:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| conversationId | string | yes | From email_search results |
| format | string | no | "text" or "html" (default: text) |

**Example:**
```json
{"name": "email_read", "arguments": {
  "conversationId": "AAQkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAQAIGSNkSniVBLpvhqYlt3T8k=",
  "format": "text"
}}
```

**Response (Layer 3):**
```json
{
  "content": {
    "emails": [
      {
        "from": {"name": "Sender Name", "email": "sender@amazon.com"},
        "subject": "Subject line",
        "body": "Full email body text..."
      }
    ]
  }
}
```

---

### 3. email_send
Send an email.

**Arguments:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| to | string[] | yes | Array of recipient email addresses |
| subject | string | yes | Email subject |
| body | string | yes | Email body (HTML supported) |

**Example:**
```json
{"name": "email_send", "arguments": {
  "to": ["prichwil@amazon.com"],
  "subject": "Daily Brief — March 20, 2026",
  "body": "<html><body><h1>Brief</h1><p>Content here</p></body></html>"
}}
```

**Note:** For HTML bodies with special characters, use the cat-pipe method (write request to temp file first) to avoid shell escaping issues.

---

### 4. email_reply
Reply to an email conversation.

**Arguments:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| conversationId | string | yes | Conversation to reply to |
| body | string | yes | Reply body |
| replyAll | boolean | no | Reply to all recipients |

*(Inferred from autoApprove list — not yet used in scripts)*

---

### 5. email_draft
Create a draft email.

**Arguments:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| to | string[] | yes | Recipients |
| subject | string | yes | Subject |
| body | string | yes | Body |

*(Inferred from autoApprove list — not yet used in scripts)*

---

### 6. email_inbox
List inbox emails.

*(Inferred from autoApprove list — no usage examples found)*

---

### 7. email_folders / email_list_folders
List email folders.

*(Inferred from autoApprove list — no usage examples found)*

---

### 8. calendar_view
Get calendar events for a date range.

**Arguments:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| start_date | string | yes | Start date (YYYY-MM-DD) |
| end_date | string | yes | End date (YYYY-MM-DD) |

**Example:**
```json
{"name": "calendar_view", "arguments": {
  "start_date": "2026-03-18",
  "end_date": "2026-03-19"
}}
```

**Response (Layer 3) — array of events:**
```json
[
  {
    "meetingId": "AAkALg...",
    "meetingChangeKey": "DwAA...",
    "subject": "Meeting Name",
    "start": "2026-03-18T16:00:00Z",
    "end": "2026-03-18T17:00:00Z",
    "location": "zoom/chime URL or room",
    "status": "Busy|Free|Tentative",
    "categories": [],
    "organizer": {"name": "Name", "email": "alias@amazon.com"},
    "isCanceled": false,
    "isRecurring": true,
    "isAllDay": false,
    "response": "Accept|Organizer|NoResponseReceived"
  }
]
```

---

### 9. calendar_search
Search calendar events.

*(Inferred from autoApprove list — no usage examples found)*

---

### 10. calendar_meeting
Create, read, update, or delete calendar meetings.

**Arguments:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| operation | string | yes | "create", "read", "update", or "delete" |
| subject | string | yes (create) | Meeting subject |
| start | string | yes (create) | Start time (ISO 8601, UTC) |
| end | string | yes (create) | End time (ISO 8601, UTC) |
| body | string | no | Meeting body/description |
| showAs | string | no | "busy", "free", "tentative" |
| reminderMinutes | int | no | Reminder before meeting |

**Example — create a focus block:**
```json
{"name": "calendar_meeting", "arguments": {
  "operation": "create",
  "subject": "Focus: Task Name",
  "start": "2026-03-23T21:30:00Z",
  "end": "2026-03-23T23:00:00Z",
  "body": "Task context and instructions",
  "showAs": "busy",
  "reminderMinutes": 15
}}
```

**Response:**
```json
{"success": true, "content": {"message": "Meeting created successfully", "meetingId": "AAkALg...", "changeKey": "DwAA...", "subject": "...", "start": "...", "end": "...", "location": ""}}
```

---

### 11. todo_lists
List all To-Do lists.

**Arguments:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| operation | string | yes | "list" |

**Example:**
```json
{"name": "todo_lists", "arguments": {"operation": "list"}}
```

**Response (Layer 3):**
```json
{
  "lists": [
    {
      "displayName": "🧹 Sweep",
      "id": "AAMk...",
      "taskCount": 5
    }
  ]
}
```

---

### 12. todo_tasks
Full CRUD on To-Do tasks.

#### List tasks in a list
```json
{"name": "todo_tasks", "arguments": {
  "operation": "list",
  "listId": "AAMk..."
}}
```

**Response (Layer 3):**
```json
{
  "content": {
    "tasks": [
      {
        "id": "AAMk...",
        "title": "Task title",
        "status": "notStarted|completed",
        "importance": "normal|high",
        "dueDateTime": "2026-03-20" or "none",
        "body": "Task body content..."
      }
    ]
  }
}
```

#### Create a task
```json
{"name": "todo_tasks", "arguments": {
  "operation": "create",
  "listId": "AAMk...",
  "title": "New task title",
  "body": "Task body with details",
  "dueDateTime": "2026-03-25",
  "importance": "high"
}}
```

#### Update a task
```json
{"name": "todo_tasks", "arguments": {
  "operation": "update",
  "listId": "AAMk...",
  "taskId": "AAMk...",
  "title": "Updated title",
  "body": "Updated body"
}}
```

**Response:**
```json
{"success": true, ...}
```

---

## Key IDs

### Outlook Folders
| Folder | ID |
|--------|-----|
| Auto-Comms (Asana) | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQpAAA=` |
| Auto-meeting       | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja/dZLhI0AAC3dkeCAAA=` |
| Goal: Paid Acquisition | `AQMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1ADdkM2EwYWMALgAAAyuwPeLL9INGsaRwucS5ngYBAEas7LcSB6lEv39h0ciIq84AAAITTwAAAA==` |
| AP (Invoices) | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQcAAA=` |

### To-Do Lists
| List | ID |
|------|-----|
| 🧹 Sweep | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESHAAA=` |
| 🎯 Core | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESIAAA=` |
| ⚙️ Engine Room | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESJAAA=` |
| 📋 Admin | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESKAAA=` |
| 📦 Backlog | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADWyS4nAAA=` |

## Known Gotchas

1. **Triple-nested JSON**: Response is JSON → JSON string → JSON string → actual data. Must parse 3 times.
2. **Shell escaping**: HTML bodies with quotes/special chars break `echo` pipe. Use cat-pipe method (write to temp file, then `cat file | aws-outlook-mcp`).
3. **Timeout**: Always use `timeout 15` or `timeout=30` — the binary can hang if the API is slow.
4. **Folder IDs**: The Auto-Comms folder ID uses `/` in the base64 (not `-`). The To-Do list IDs use `-` instead of `/`. Both are valid — they're different Microsoft Graph resources.
5. **Unicode in titles**: Microsoft To-Do stores emoji in task titles. Some render as boxes in terminal. The `clean_todo_titles.py` script handles replacement.
6. **No streaming**: The binary processes one request per invocation and exits. No persistent connection.
