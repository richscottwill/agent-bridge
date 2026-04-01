# Production Scripts

Only production-ready scripts belong here. Debug/one-off scripts go to tools/scratch/.

| Script | Purpose | Invoked By |
|--------|---------|------------|
| asana_sync.py | Syncs Asana tasks via email bridge | Morning routine hook |
| clean_todo_titles.py | Cleans up To-Do task titles | Manual/morning routine |
| hedy-sync.py | Ingests meeting notes from Hedy | Meeting sync hook |
| hedy-meeting-prep.py | Prepares meeting briefs from Hedy data | Manual |
| morning_routine.py | Orchestrates morning routine | AM hook |
| pull_emails2.py | Pulls emails for processing | Morning routine |
| pull_todos.py | Pulls To-Do tasks | Morning routine |
| send_brief_v4.py | Sends daily brief email (latest) | Morning routine |
| update-todo.py | Updates To-Do lists | Morning routine |

## Cleaned 2026-03-31
- Removed superseded: send-brief.py, send_brief_v2.py, send_brief_v3.py, send_brief_0318.py, pull_emails.py
