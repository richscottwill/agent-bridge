<!-- DOC-0412 | duck_id: protocol-topic-sentry -->
# Topic Sentry Protocol — daily topic-driven scan

**Purpose:** Every morning, scan the last 24h of emails + Slack + Loop + Hedy + Asana for content matching topics in `~/shared/context/body/topic-watchlist.md`, regardless of sender. Produce `~/shared/context/active/topic-sentry.md` as a dedicated digest.

**Why separate from AM Brief:** AM Brief classifies by sender priority (Brandon/Kate/Todd = HIGH). That mis-prioritizes *structural* signals — BCC distros, feature launches, cross-team announcements — where sender isn't the point. Topic Sentry closes that gap by scanning for subject matter instead.

**Cadence:** daily, after AM-Backend completes so DuckDB is fresh. Runs in the orchestrator (no subagent fan-out needed — all reads, no MCP writes beyond the output file).

---

## Execution

### Phase 0: Load watchlist

1. Read `~/shared/context/body/topic-watchlist.md`.
2. Parse each `### <topic-name>` block into a struct:
   - `name`, `status`, `priority` (P1/P2/P3/monitoring/sunset)
   - `keywords` (list of phrases — quoted phrases are exact-match, unquoted are case-insensitive token match)
   - `senders` (optional list)
   - `channels` (subset of {email, slack, loop, hedy, asana, all})
   - `why`, `review_date`
3. Skip `sunset` topics. Log any topic whose review_date has passed — include in the output's "Review needed" footer.

### Phase 1: Scan each channel

For each non-sunset topic, query DuckDB for matches in the last 24 hours:

#### Email (`signals.emails`)
```sql
SELECT received_at, sender_email, subject, preview, conversation_id
FROM signals.emails
WHERE received_at >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
  AND (
    -- any keyword match against subject OR preview
    <keyword_predicate>
    OR sender_email = ANY(<senders_array>)
  )
```

Build `<keyword_predicate>` from the topic's keywords. Quoted phrases use `ILIKE '%<phrase>%'`. Unquoted tokens use `ILIKE '%<token>%'`. Join with `OR`.

#### Slack (`signals.slack_messages`)

First, filter to channels whose section has `"topic_sentry"` in its `scan_in` array (per `~/shared/data/state/slack-channel-registry.json` v3.1+). This excludes `Channels` (sweep-only) by default.

```sql
SELECT ts, channel_name, author, text, reply_count

#### Phase 1: Scan each channel — Details

FROM signals.slack_messages
WHERE ingested_at >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
  AND channel_section IN (<sections_scan_in_topic_sentry>)
  AND <keyword_predicate>
```

#### Hedy (`signals.hedy_meetings`)
```sql
SELECT meeting_ts, topic_name, attendees, recap_preview
FROM signals.hedy_meetings
WHERE ingested_at >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
  AND <keyword_predicate>
```

#### Loop (`docs.loop_pages`)
```sql
SELECT page_title, last_modified, content_preview, url
FROM docs.loop_pages
WHERE last_ingested >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
  AND <keyword_predicate>
```

#### Asana (`asana.asana_tasks` — optional)
Only scan if a topic explicitly lists `asana` in channels. Match against name + notes + recent story text (if stored).

### Phase 2: Dedup and rank

- A single source (email thread, Slack ts, Hedy session, Loop page) can match multiple topics. Include it under each matching topic; don't dedup across topics.
- Within a topic, dedup by source id (conversation_id for email, ts for Slack, etc.).
- Rank within topic by recency (most recent first).

### Phase 3: Write `topic-sentry.md`

Format:

```markdown
# Topic Sentry — YYYY-MM-DD

#### Phase 3: Write `topic-sentry.md` — Details


_Scan window: last 24 hours. Watchlist: N active topics. Hits: M sources across K topics._

**Five Levels coverage (by hit count):** L1: X hits · L2: X hits · L3: X hits · L4: X hits · L5: X hits · operational: X hits
_If any Level has 0 hits for 7+ consecutive days, note it: "⚠️ No L4 hits in 7 days — Zero-Click Future radar quiet."_

## P1 — must surface

### <topic-name> (N hits)
_Why: <one-line why from watchlist>_

- [HH:MM email] <sender> — <subject> — [<one-line preview>] ([open](link-if-available))
- [HH:MM slack #<channel>] <author>: <one-line preview> ([open](link))
- [HH:MM hedy] <meeting_topic> — <recap_preview>
- [HH:MM loop] <page_title> — <content_preview>

### <topic-name> (0 hits)
_no activity in 24h_

## P2 — worth knowing

<same structure>

## P3 — background radar

<same structure>

## Monitoring

<same structure, typically low/no hits>

---

## Review needed

- <topic-name>: review_date YYYY-MM-DD has passed (N days ago). Confirm still worth watching.

## Operating notes

- Topics with 0 hits in 30 consecutive days: proposed for demotion to `monitoring` or sunset. Logged to `~/shared/context/intake/topic-sentry-proposals.md` for Richard review.
- Topics hitting >5 times in 7 days on P3: proposed for promotion to P2.
- Proposals never self-execute — they're suggestions for the weekly Broad Sweep review.
```

### Phase 4: Write to SharePoint (durability)

Push `topic-sentry.md` to `Kiro-Drive/system-state/topic-sentry-YYYY-MM-DD.md` for cross-device access. Non-blocking — if SharePoint fails, log warning and continue.

### Phase 5: Output consumed by AM-Frontend
- Surfaces up to 5 P1 topics with hits >= 1 in the brief
- Flags `⚠️ Topic Sentry: stale or missing` if the file is >24h old or absent
- Line 2 `_Scan window: ... Watchlist: N active topics. Hits: M sources across K topics._`
- H3 section headers with pattern `### <topic-slug> (N hits)` — N parsed as int, 0 means no activity
- Parses the header (total hits, topic count, Five Levels coverage)
- Line 3 bold `**Five Levels coverage (by hit count):** L1: X · L2: X · L3: X · L4: X · L5: X · operational: X`
- First bullet under each H3 (used as one-line summary in brief)

Topic Sentry produces `~/shared/context/active/topic-sentry.md`. AM-Frontend (hook #1 `.AM-Frontend: Brief + Triage + Command Center`) reads this file during Step 1 Brief — see `am-frontend.md` § Topic Radar Section. The frontend:


This is the structural closure of the loop — without AM-Frontend consuming the file, Sentry produces unread output. The Brief's Topic Radar section renders:

```
🎯 TOPIC SENTRY — M sources across K topics (last 24h)
Five Levels: L1:x · L2:x · L3:x · L4:x · L5:x · operational:x
P1 topics with hits today:
• [topic-slug] (N hits): <first bullet one-line summary>
...
Full digest: ~/shared/context/active/topic-sentry.md
```

**Header keys AM-Frontend parses** (keep these stable across Sentry refactors):

Breaking any of these patterns requires a matching update to `am-frontend.md` § Topic Radar Section.

---

3. Flag stale sources in the output header: `⚠️ Stale: email (last sync 18h ago), slack (last sync 6h ago)`
- `docs.loop_pages` populated by Subagent D
2. Proceed with the sources that are fresh
- `signals.hedy_meetings` populated by Subagent E
---
1. Log which data sources are stale (from `ops.data_freshness`)
- `signals.emails` populated by Subagent C
- `signals.slack_messages` populated by Subagent A

Topic Sentry runs AFTER AM-Backend because it depends on:

If any of those failed this morning, Topic Sentry should:

This means Topic Sentry is NOT a replacement for AM ingestion — it's a layer on top. If ingestion is degraded, Sentry coverage is degraded too. Honest about it.


## Failure handling
- If `topic-watchlist.md` is missing or unparseable: log error, fall back to writing an empty `topic-sentry.md` with a header telling Richard to fix the watchlist.
- If all DuckDB queries fail: log error, write minimal output saying "DuckDB unreachable."
- Never silently produce an empty digest. The output file should always exist with a clear status, so Richard can distinguish "no hits today" from "scanner broke."
---
## Tuning knobs

- **Scan window:** default 24h. Adjustable in the hook trigger if Richard wants a catch-up run (e.g., after a long weekend set to 72h).
- **Keyword matching:** ILIKE-based substring match. If false positives spike, move to tokenized match against a stopword-filtered FTS column.
- **Max hits per topic:** 10 in the digest. More than that collapses to `N hits total — top 10 shown, see DuckDB for rest`.
