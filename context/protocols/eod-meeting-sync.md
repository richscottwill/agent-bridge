<!-- DOC-0350 | duck_id: protocol-eod-meeting-sync -->


# EOD Meeting Sync Protocol Hedy + Outlook + email → meetings/ series files + organ updates. ## Details

---



## Context Load
meetings/README.md for protocol.



## Pull
- Hedy: GetSessions (today), details, todos.
- Outlook: Auto-meeting folder.; Email threads related to meetings.
- current.md, nervous-system.md, series files.



## Analyze - Speaking share - Hedging language - Strategic contributions - Action items - Relationship dynamics 


## Update meetings/
For each session:
- ONE Latest Session entry
- Open Items section
- Running Themes section



## Update Organs
- memory.md: relationship updates from meeting dynamics
- nervous-system.md: Loop 7 (meeting patterns), Loop 3 (pattern trajectory)
- current.md: people updates, new action items
- device.md: delegation updates


## Audit
Hedy: today's topics only. Flag discrepancies.



[38;5;10m> [0m## Meeting-to-Task Automation[0m[0m
[0m[0m
After each Hedy session, execute **~/shared/context/protocols/meeting-to-task-pipeline.md**:[0m[0m
[0m[0m
1. Extract all action items (todos, action-marked highlights)[0m[0m
2. For Richard's items:[0m[0m
  a. Search Asana for duplicates: SearchTasksInWorkspace(text="[key phrases]", assignee_any="1212732742544167", completed=false)[0m[0m
  b. Duplicate found: AddComment with meeting reference[0m[0m
  c. New: CreateTask with meeting context, derived due date, appropriate project[0m[0m
3. Others' items: append to hands.md dependencies[0m[0m
4. Insert session data into DuckDB meeting_analytics; highlights into meeting_highlights[0m[0m
5. After all sessions: self_dm summary of tasks created, updated, and dependencies logged[0m[0m
6. Log execution to workflow_executions in DuckDB[0m[0m
[0m[0m
## Report[0m[0m
[0m[0m
Sessions processed, files updated, flags, action items extracted, Asana tasks created/updated.
### Log Hook Execution
```sql
INSERT INTO hook_executions (hook_name, execution_date, start_time, end_time, duration_seconds,
 phases_completed, asana_reads, asana_writes, slack_messages_sent, duckdb_queries, summary)
VALUES ('eod-meeting-sync', CURRENT_DATE, '[start]', '[end]', [duration],
 [phases], [reads], [writes], [slack_msgs], [queries], '[summary]');
```
