# EOD Meeting Sync Protocol

Hedy + Outlook + email → meetings/ series files + organ updates.

---

## Context Load
meetings/README.md for protocol.

## Pull
- Hedy: GetSessions (today), details, todos.
- Outlook: Auto-meeting folder.
- Email threads related to meetings.
- current.md, nervous-system.md, series files.

## Analyze
- Speaking share
- Hedging language
- Strategic contributions
- Action items
- Relationship dynamics

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

## Meeting-to-Task Automation

After processing each Hedy session, execute the meeting-to-task pipeline:

**Read and execute ~/shared/context/protocols/meeting-to-task-pipeline.md**

For each session:
1. Extract all action items (todos, highlights marked as action)
2. For each item assigned to Richard:
   a. Search Asana for duplicates: SearchTasksInWorkspace(text="[key phrases]", assignee_any="1212732742544167", completed=false)
   b. If duplicate (2+ phrase overlap): AddComment on existing task with meeting reference
   c. If new: CreateTask with meeting context, derived due date, appropriate project
3. For items assigned to others: append to hands.md dependencies
4. Insert session data into DuckDB meeting_analytics table
5. Insert highlights into DuckDB meeting_highlights table
6. After ALL sessions: self_dm summary of tasks created, updated, and dependencies logged
7. Log pipeline execution to workflow_executions in DuckDB

## Report
Sessions processed, files updated, flags, action items extracted, Asana tasks created/updated.

### Log Hook Execution
```sql
INSERT INTO hook_executions (hook_name, execution_date, start_time, end_time, duration_seconds,
    phases_completed, asana_reads, asana_writes, slack_messages_sent, duckdb_queries, summary)
VALUES ('eod-meeting-sync', CURRENT_DATE, '[start]', '[end]', [duration],
    [phases], [reads], [writes], [slack_msgs], [queries], '[summary]');
```
