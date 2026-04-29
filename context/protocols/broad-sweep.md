<!-- DOC-0413 | duck_id: protocol-broad-sweep -->
# Broad Sweep Protocol — weekly deep-scan

**Purpose:** Once per week, do an exhaustive pull across email, Slack, Loop, Hedy, SharePoint — including distros, channels, and folders that the daily AM Brief skips — and surface anything that matters but wasn't flagged during the week.

**Why separate from AM Brief:** AM is tuned for speed and narrow priority (Brandon/Kate/Todd senders, known-priority channels). Sweep is tuned for coverage. It assumes nothing about sender or channel priority — it ingests broadly, classifies against `topic-watchlist.md`, and produces a "what you might have missed this week" digest.

**Cadence:** weekly. Richard picks the day — not prescribed here. The hook is on-demand or scheduled by user config, not auto-fired.

---

## Execution

### Phase 0: Determine scan window

1. Read `ops.sync_watermarks` for table `broad_sweep_last_run`.
2. Scan window = `[last_run, CURRENT_TIMESTAMP]`. If no previous run, default to last 7 days.
3. If window > 14 days, cap at 14 (longer and the volume gets unmanageable — Richard can run two passes).


**Constraint:** All identifiers, thresholds, and rules in this section are load-bearing. Modifications require re-validation.

### Phase 1: Broad ingestion

This is the expensive part — everything the AM scan filters out.

#### Email (full sweep)
- `email_search` across **all folders** (inbox, sent, archive, deleted, custom folders) with `startDate = scan_start`, `endDate = now`.
- No sender filter. No subject filter. Ingest everything.
- For each email:
  - Check if already in `signals.emails` by `conversation_id`. If yes, skip.
  - If no, insert with full body (not just preview).
- Special attention: emails where `to` or `cc` or `bcc` contain distros (`*@amazon.com` that match `*-announcement@`, `*-interest@`, `*-product-mgrs@`, `ab-*@`, `*-flash@`, etc.). These are the BCC-distro blind spot.

#### Slack (full sweep)
- `list_channels(channelTypes=['public_and_private', 'dm', 'group_dm'])` — ALL channels Richard is a member of, not just unread.
- Filter to sections whose `scan_in` array in `~/shared/data/state/slack-channel-registry.json` (v3.1+) contains `broad_sweep` — this is nearly all sections by default. Excluded sections (if any) are logged in the digest header so Richard can reconsider exclusions.
- For each channel: `batch_get_conversation_history` with `oldest = scan_start`.
- Ingest everything. No relevance filter. Skip channels explicitly excluded in `slack-channel-registry.json` (e.g., noisy bot channels).
- Include thread replies for all parent messages with `reply_count > 0` within the window.

#### Loop (full sweep)
- Query `docs.loop_pages` for all tracked pages.
- For each page: `sharepoint_read_loop` — even if `last_ingested` is recent. We want a current snapshot, not cached.
- Diff against prior content to detect meaningful changes (not just timestamp bumps).

#### Hedy (full sweep)
- `GetSessions(after=scan_start, limit=100)` — all meetings in the window.
- For each: `GetSessionDetails` + `GetSessionToDos` + `GetSessionHighlights`.
- Insert/update `signals.hedy_meetings`. Ingest full recap, not just the preview.

#### SharePoint drift check
- `sharepoint_list_files` for `Kiro-Drive/state-files/`, `Documents/Artifacts/`, `Dashboards/`.
- For each file: compare `LastModified` against local equivalent in `~/shared/wiki/` or `~/shared/context/active/`.
- Flag drift (local newer than SharePoint = unpushed, SharePoint newer than local = changes from another device).

### Phase 2: Classification against topic-watchlist

Run the Topic Sentry scan logic (see `topic-sentry.md` Phase 1) but over the full sweep window instead of 24h. This surfaces every topic-watchlist hit across the week — including sources that AM missed because of sender filter, channel priority, or folder coverage.

#### Phase 2: Classification against topic-watchlist (continued)


Write hits to `~/shared/context/active/broad-sweep-topic-hits.json` for feeding into the digest and for Topic Sentry's promotion/demotion proposals.

### Phase 3: Gap analysis — what AM missed

This is the Sweep's core value. Produce a per-channel diff.

#### Computation

| Term | Definition |
|------|-----------|
| AM-covered | Sources that appeared in any email-triage.md / slack-digest.md / hedy-digest.md during the week |
| Sweep-found | Sources ingested in Phase 1 |
| **Gap** | Sweep-found − AM-covered |

#### Classification (priority order)

| Priority | Category | Signal | Example |
|----------|----------|--------|---------|
| High | Topic-watchlist hit | Matched watchlist keyword AM never saw | ABMX-style distro miss → digest top |
| Medium | Sender-escalation | Non-priority sender became relevant | VP you haven't interacted with |
| Medium | High-reply/reaction Slack | Significant engagement in non-AM channels | 20+ replies in #ab-product-mgrs |
| Medium | Loop changes on high-traffic pages | Edits to key docs | Brandon 1:1, MBR doc, test-readout doc |
| Low | Everything else | No specific signal | Summarized in aggregate |

### Phase 4: Topic promotion/demotion proposals

Based on 7-day hit counts against `topic-watchlist.md`:

- Topics with 0 hits in 30 days → propose demotion to `monitoring` or `sunset`.
- `monitoring` topics with 5+ hits in 7 days → propose promotion to P3.
- P3 topics with 15+ hits in 7 days → propose promotion to P2.
- New emerging topics (FTS clusters appearing in `signals.signal_tracker` that aren't in watchlist AND have strength > 5) → propose adding.

Write proposals to `~/shared/context/intake/topic-sentry-proposals.md`. Do not auto-execute.

### Phase 5: Write `broad-sweep.md` digest

**Location:** `~/shared/context/active/broad-sweep-YYYY-WNN.md` (weekly rolling).

**Required sections (in order):**
1. Header with scan window dates + ingestion summary line: `_Ingested: X emails, Y Slack messages across Z channels, W Loop pages, V Hedy meetings. New vs AM: N sources._`
2. What you might have missed — topic-watchlist hits, non-priority senders, Slack channels outside daily rotation, Loop page changes
3. SharePoint drift — local newer (unpushed) vs SharePoint newer (pulled from another device)
4. Topic watchlist proposals — PROMOTE/DEMOTE/ADD with reasons
5. Weekly aggregate counters — email volume (WoW%), Slack messages (WoW%), Loop page updates, meetings attended, top 5 topic-watchlist hits

**Format reference (template):**

```markdown
# Broad Sweep — Week NN of YYYY (scan window YYYY-MM-DD to YYYY-MM-DD)

_Ingested: X emails, Y Slack messages across Z channels, W Loop pages, V Hedy meetings. New vs AM: N sources._

## What you might have missed

### Topic-watchlist hits that AM didn't surface
- [YYYY-MM-DD email] <sender> → <subject> — matched <topic-name> — <one-line why>
- [YYYY-MM-DD slack #<channel>] <author>: <one-line> — matched <topic-name>

### Non-priority senders worth noting
- <sender>: sent <N> emails in window; relevant because <reason>

### Slack channels outside daily rotation
- #<channel> (M messages, K replies this week): <summary of notable discussion>

### Loop page changes
- <page_title>: changed on YYYY-MM-DD by <author>. Key diff: <delta>.

## SharePoint drift
- <file>: local newer (unpushed since YYYY-MM-DD)
- <file>: SharePoint newer (pulled changes from another device, review)

## Topic watchlist proposals
- PROMOTE `monitoring/<topic-name>` → P3 (hit 6 times this week, was 0 last 30 days). Reason: <signal>.
- DEMOTE `P3/<topic-name>` → monitoring (0 hits in 30 days). Reason: stale.
- ADD new topic `<slug>`: <keywords>. Seen as emerging cluster in signal_tracker (strength 7.2, 4 sources).

_Review and apply in `~/shared/context/body/topic-watchlist.md` — proposals do not self-execute._

## Weekly aggregate counters
---
- Loop page updates: <N>
- Slack messages: <N> (WoW ±X%)
- Email volume: <N> (week-over-week ±X%)
- Top 5 topic-watchlist hits: <list>
- Meetings attended: <N>


_Next sweep due: YYYY-MM-DD_
```

### Phase 6: SharePoint durability

Push the weekly sweep to `AB-Paid-Acq-Ops/agent-state/broad-sweep-YYYY-WNN.md` (SharePoint personal OneDrive). This is the canonical agent-state home as of the 2026-04-28 folder restructure — do NOT use the deprecated `Kiro-Drive/` path.

### Phase 7: Update ops.sync_watermarks

```sql
UPDATE ops.sync_watermarks
SET last_run_at = CURRENT_TIMESTAMP,
    sources_ingested = '<json of counts>'

#### Phase 7: Update ops.sync_watermarks — Details

WHERE source = 'broad_sweep_last_run';
```

If the row doesn't exist, insert it.

---


**Constraint:** All identifiers, thresholds, and rules in this section are load-bearing. Modifications require re-validation.

## Contract with AM-Backend and Topic Sentry

- **Broad Sweep reads the same DuckDB tables AM-Backend writes to.** It doesn't re-architect ingestion — it does a *longer window* pull using the same MCP tools and writes to the same tables (dedup on conversation_id / ts / session_id).
- **Broad Sweep doesn't replace AM.** AM still runs daily for priority-sender filtering and calendar. Sweep runs weekly for coverage.
- **Topic Sentry's daily output is a subset of what Sweep finds.** Sweep catches the same topics over a longer window + non-topic gaps (senders, channels, drift).

**Worked example:** Monday AM-Backend ingests 3 emails from Brandon (priority sender) and 12 Slack messages from #au-ps (priority channel). It writes to `signals.emails` and `signals.slack_messages`. Friday Broad Sweep runs — it pulls the same tables plus 47 emails from non-priority senders and 200+ Slack messages from 15 channels AM skips. It writes to the same `signals.*` tables (dedup prevents duplicates on the 3 Brandon emails). Gap analysis: 8 of the 47 non-priority emails matched topic-watchlist keywords AM never saw.

---

## Guardrails & Failure Modes

**Resilience:**
- MCP server down (Slack auth, SharePoint Midway, etc.): skip that channel, flag in digest header, continue. Never abort on single-channel failure.
- Sweep skipped >14 days: cap window at 14 days, include "coverage gap" note in digest.
- No new sources in window: still produce digest with "no new sources" + watermark bump (visible confirmation sweep ran).

**Anti-patterns:**
- **Don't re-run AM.** Sweep is *additive*, not a replacement. If it produces the same priority-sender digest, it's failing its purpose.
- **Don't auto-apply watchlist changes.** Proposals are suggestions. Richard edits `topic-watchlist.md` by hand to confirm.
- **Don't silently drop sources.** Excluded channels go in digest header so Richard can reconsider.
- **Don't expand to daily cadence.** If AM/Sentry aren't catching enough, tune those — not Sweep.
