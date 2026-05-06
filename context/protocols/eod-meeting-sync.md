<!-- DOC-0350 | duck_id: protocol-eod-meeting-sync -->

# EOD Meeting Sync Protocol

Hedy + Outlook → topic-log entries + meeting-series updates + organ updates.

**2026-05-06 migration:** This protocol used to write to `signals.hedy_meetings`, `main.meeting_analytics`, `main.meeting_highlights`, `main.meeting_series` DuckDB tables. Those tables are deprecated. Topic logs at `~/shared/wiki/topics/` are the canonical post-meeting artifact. Meeting series files at `~/shared/wiki/meetings/` continue as recurring-meeting logs. Hedy MCP remains the transcript source of truth.

---

## Context Load

- `~/shared/wiki/topics/INGEST-PROTOCOL.md` — topic log append contract
- `~/shared/wiki/topics/_registry.md` — registered topic slugs + hedy_topic_id mapping
- `~/shared/wiki/meetings/README.md` — meeting series conventions

## Pull

- Hedy MCP: `GetSessions` (today), `GetSessionDetails`, `GetSessionToDos`, `GetSessionHighlights`
- Outlook: auto-meeting folder + related email threads
- current.md, nervous-system.md, series files

## Analyze

Objective extraction only — no interpretation. Capture:
- Direct quotes where possible
- Decisions as stated (with who decided)
- Actions as committed (with owner + due date)
- Speaking share, topics discussed (on-demand via Hedy, not stored in DuckDB)
- Relationship dynamics for memory.md (noted, not quantified)

## Route to topic logs (primary write)

For each session, identify target topic docs per INGEST-PROTOCOL topic identification order:
1. `hedy_topic_id` exact match against `_registry.md`
2. slug/alias match on session title + topic names
3. related-slug match from adjacent topic docs

For each target topic doc:
- Prepend H3 Log entry with `#### Source hedy:<session_id>`, `#### What was said / what happened`, `#### Decisions`, `#### Actions`, optional `#### Notes`
- Prepend daily line to Simplified Timeline under current ISO-week H4 header
- Move resolved Open Items to Closed Items — Audit Trail (never delete)
- Update `updated:` frontmatter to today (PT)

Unregistered candidates with ≥3 mentions over 60d → append to `~/shared/wiki/topics/_discovery-queue.md`.

## Update meeting series (secondary write)

For sessions whose `meeting_name` maps to a file in `~/shared/wiki/meetings/`, update the series file:
- Prepend Latest Session entry
- Update Open Items + Running Themes per existing conventions

Meetings files remain recurring-meeting logs; topic logs are the cross-channel synthesis.

## Update Organs

- memory.md: relationship updates from meeting dynamics
- nervous-system.md: Loop 7 (meeting patterns), Loop 3 (pattern trajectory)
- current.md: people updates, new action items
- device.md: delegation updates

## Audit

Hedy: today's topics only. Flag discrepancies between transcript and routed topic-log entries. If a session was not routed to any topic doc, log reason (no match, intentional skip, etc.) in EOD summary.

## Meeting-to-Task Automation

After topic-log routing, execute `~/shared/context/protocols/meeting-to-task-pipeline.md`:

1. Walk new Log entries' `#### Actions` blocks
2. For Richard's items: dedup against Asana, CreateTask or comment
3. For others' items: append to hands.md dependencies
4. After all sessions: self_dm summary
5. Log execution to `ops.workflow_executions`

## Deprecated (do NOT perform)

- Do NOT INSERT into `signals.hedy_meetings`
- Do NOT INSERT into `main.meeting_analytics`
- Do NOT INSERT into `main.meeting_highlights`
- Do NOT UPDATE `main.meeting_series` (DuckDB table) — the meetings/*.md files remain as the meeting-series log
- Do NOT write `~/shared/context/intake/hedy-digest.md` or `~/shared/context/active/hedy-digest.md`
- Do NOT update `ops.data_freshness.hedy_meetings` row

## Report

Sessions processed, topic docs updated, files updated, flags, action items extracted, Asana tasks created/updated.

### Log Hook Execution

```sql
INSERT INTO ops.hook_executions (hook_name, execution_date, start_time, end_time, duration_seconds,
 phases_completed, asana_reads, asana_writes, slack_messages_sent, duckdb_queries, summary)
VALUES ('eod-meeting-sync', CURRENT_DATE, '[start]', '[end]', [duration],
 [phases], [reads], [writes], [slack_msgs], [queries], '[summary]');
```
