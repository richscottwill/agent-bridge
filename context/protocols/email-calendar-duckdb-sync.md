<!-- DOC-0347 | duck_id: protocol-email-calendar-duckdb-sync -->
# Email + Calendar → DuckDB Sync Protocol

Canonical sync procedure for keeping DuckDB `signals.emails` and `main.calendar_events` populated from Outlook MCP. Runs as part of AM-Backend Subagent C.

Database: `ps_analytics` (via DuckDB MCP). Always use schema-qualified names.

---

## Step 1 — Pull Emails (All Folders, Date-Bounded)

### Step 1A — Determine scan window

Query `ops.data_freshness` for the last successful email sync date:

```sql
SELECT last_updated::DATE AS last_scan_date
FROM ps_analytics.ops.data_freshness
WHERE source_name = 'emails';
```

- If a row exists: `startDate` = that date (YYYY-MM-DD). This **includes** the last-scanned day to catch late-arriving emails.
- If no row exists (first run): `startDate` = today minus 3 days as a safe bootstrap window.
- `endDate` = today (YYYY-MM-DD).

### Step 1B — Search all folders

```
email_search(query="*", startDate="{startDate}", endDate="{endDate}", limit=250)
```

This searches across **all folders** (inbox, sent, custom folders, subfolders, newly created folders) and returns emails within the date window. Each result includes: conversationId, topic (subject), senders, lastDeliveryTime, preview, hasAttachments, folder.

**Why `email_search` instead of `email_inbox`:** `email_inbox` only returns inbox emails. `email_search` with a date range covers every folder — including custom rules-based folders and any folder created after this protocol was written.

**Why include the last-scanned day:** Emails can arrive late (server-side rules, delayed delivery, calendar invites updating). Re-scanning the overlap day with UPSERT ensures nothing is missed. The ON CONFLICT clause makes this idempotent.

**Pagination:** If 250 results are returned (limit hit), increment `offset` by 250 and repeat until fewer than 250 results come back. In practice, a 1-3 day window rarely exceeds 250.

### Sender Priority Classification

| Priority | Condition |
|----------|-----------|
| high | Sender contains: Brandon, Kate, Todd, Lena, Lorena, Alexis, Andrew, Stacey, Yun, Adi |
| medium | Sender contains: Kiran, Vijeth, Alex, Dwayne, Caroline, Frank, Suzane |
| low | All others (automated, newsletters, system notifications) |

### Action Classification

| action_needed | Condition |
|---------------|-----------|
| respond | Email is a direct question to Richard, or a request for input/data/file |
| review | Email contains information Richard should read (FYI, update, report) |
| none | Automated notification, newsletter, system alert, or already-handled |

### Step 2 — INSERT into signals.emails

For each email from Step 1, execute:

```sql
INSERT INTO signals.emails (
    email_id, conversation_id, subject, sender_name, sender_alias,
    received_at, is_read, priority, action_needed, content_preview,
    has_attachments, folder, synced_at
) VALUES (
    '{generate_unique_id}',          -- e.g. 'em_' + short hash of conversationId
    '{conversationId}',
    '{topic}',
    '{senders[0]}',                  -- first sender name
    NULL,                            -- alias not available from inbox API
    '{lastDeliveryTime}'::TIMESTAMP,
    {unreadCount == 0},              -- true if unreadCount is 0
    '{priority}',                    -- from classification above
    '{action_needed}',               -- from classification above
    '{preview first 200 chars}',
    {hasAttachments},
    '{folder}',                      -- actual folder from email_search result (no longer hardcoded to inbox)
    NOW()
)
ON CONFLICT (email_id) DO UPDATE SET
    is_read = EXCLUDED.is_read,
    priority = EXCLUDED.priority,
    action_needed = EXCLUDED.action_needed,
    synced_at = NOW();
```

**email_id generation:** Use `'em_' || LEFT(MD5(conversationId), 12)` or a deterministic short ID derived from the conversationId. This ensures idempotent re-runs don't create duplicates.

**CRITICAL:** Do NOT skip this step. The DuckDB write is the primary deliverable of this subagent — the file output (email-triage.md) is secondary.

---

## Step 3 — Pull Today's Calendar

```
calendar_view(start_date="{today MM-DD-YYYY}", view="day")
```

This returns events with: meetingId, subject, start, end, location, organizer.name, isCanceled, isRecurring, isAllDay, response, status, categories.

### Step 4 — UPSERT into main.calendar_events

For each calendar event from Step 3:

```sql
INSERT INTO main.calendar_events (
    event_id, subject, start_time, end_time, location,
    organizer_name, is_all_day, is_recurring, is_canceled,
    response, status, synced_at
) VALUES (
    '{generate_event_id}',           -- e.g. 'cal_' + LEFT(MD5(meetingId), 12)
    '{subject}',
    '{start}'::TIMESTAMP,
    '{end}'::TIMESTAMP,
    '{location}',
    '{organizer.name}',
    {isAllDay},
    {isRecurring},
    {isCanceled},
    '{response}',
    '{status}',
    NOW()
)
ON CONFLICT (event_id) DO UPDATE SET
    subject = EXCLUDED.subject,
    start_time = EXCLUDED.start_time,
    end_time = EXCLUDED.end_time,
    location = EXCLUDED.location,
    is_canceled = EXCLUDED.is_canceled,
    response = EXCLUDED.response,
    status = EXCLUDED.status,
    synced_at = NOW();
```

**event_id generation:** Use `'cal_' || LEFT(MD5(meetingId), 12)` for deterministic dedup.

**CRITICAL:** Do NOT skip this step. Calendar data in DuckDB powers the daily Dive dashboard and AM brief.

---

## Step 5 — Update Data Freshness

After both writes complete:

```sql
UPDATE ops.data_freshness
SET last_updated = NOW(), last_checked = NOW(), is_stale = false
WHERE source_name IN ('emails', 'calendar_events');
```

If the rows don't exist yet (first run), INSERT them:

```sql
INSERT INTO ops.data_freshness (source_name, source_type, expected_cadence_hours, last_updated, last_checked, is_stale, downstream_workflows)
VALUES
    ('emails', 'duckdb_table', 12, NOW(), NOW(), false, ARRAY['am_brief', 'signal_routing']),
    ('calendar_events', 'duckdb_table', 12, NOW(), NOW(), false, ARRAY['am_brief', 'daily_tracker'])
ON CONFLICT DO NOTHING;
```

---

## Step 6 — Write email-triage.md (file output)

After DuckDB writes succeed, write the human-readable digest:

```
~/shared/context/intake/email-triage.md
```

Format:
```markdown
# Email Triage — {date}

## High Priority (respond)
- **{subject}** from {sender} ({days_old}d ago) — {preview}

## Medium Priority (review)
- **{subject}** from {sender} ({days_old}d ago) — {preview}

## Low / No Action
- {subject} from {sender} — {disposition}

---
Synced: {timestamp} | {total} emails processed | {high_count} high / {medium_count} medium / {low_count} low
```

---

## Error Handling

- **Outlook MCP failure:** Log error to `~/shared/context/intake/email-sync-error-{date}.md`. Write empty email-triage.md with error note. Do NOT skip calendar sync if email fails (and vice versa).
- **DuckDB write failure:** Log the specific SQL error. Retry once. If still failing, write the file output anyway and flag: "⚠️ DuckDB write failed for {table}. Data is in email-triage.md only."
- **Empty inbox:** Valid state. Write 0 rows to DuckDB. Write email-triage.md with "No emails in scan window."
- **ops.data_freshness missing:** First run. Use startDate = today minus 3 days. The INSERT ON CONFLICT in Step 5 handles bootstrapping the row.
- **Calendar API failure:** Log error. Email sync should still complete independently.

---

## Execution Order (mandatory)

1. Query ops.data_freshness for last scan date (DuckDB)
2. Pull emails across all folders since last scan date (Outlook MCP — `email_search`)
3. **Write emails to DuckDB** ← this is the step that was being skipped
4. Pull calendar (Outlook MCP)
5. **Write calendar to DuckDB** ← this is the step that was being skipped
6. Update data freshness (DuckDB)
7. Write email-triage.md (file)

DuckDB writes come BEFORE file output. If DuckDB fails, the file output still happens as fallback. But DuckDB is the primary target.
