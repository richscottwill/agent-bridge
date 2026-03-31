# Production Scripts

Only production-ready scripts belong here. Debug/one-off scripts go to tools/scratch/.

| Script | Purpose | Invoked By |
|--------|---------|------------|
| asana_sync.py | Syncs Asana tasks via email bridge | Morning routine hook |
| clean_todo_titles.py | Cleans up To-Do task titles | Manual/morning routine |
| hedy-sync.py | Ingests meeting notes from Hedy | Meeting sync hook |
| hedy-meeting-prep.py | Prepares meeting briefs from Hedy data | Manual |
| morning_routine.py | Orchestrates morning routine | AM hook |
| pull_emails.py | Pulls emails for processing | Morning routine |
| pull_emails2.py | Updated email pull variant | Morning routine |
| pull_todos.py | Pulls To-Do tasks | Morning routine |
| send-brief.py | Sends daily brief email | Morning routine |
| send_brief_v2.py | Daily brief v2 | Morning routine |
| send_brief_v3.py | Daily brief v3 | Morning routine |
| send_brief_v4.py | Daily brief v4 (latest) | Morning routine |
| send_brief_0318.py | Daily brief snapshot 03-18 | Archive candidate |
| update-todo.py | Updates To-Do lists | Morning routine |
