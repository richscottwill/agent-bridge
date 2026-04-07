---
inclusion: fileMatch
fileMatchPattern: ["hooks/*slack*", "hooks/eod-2*"]
---

# Slack Deep Context — Backfill & Enrichment Steering

This file governs the conversation database backfill scans and enrichment processes. It is loaded by agents when they need deeper Slack context than the real-time ingestion provides.

**Who triggers these scans:** Agents, workflows, and hooks — not Richard directly. The scans exist to fill the conversation database so that agents have richer context for meeting prep, draft writing, wiki research, predicted QA, and relationship graph enrichment. Richard CAN trigger them ad-hoc, but that's the exception.

**When to run a scan:**
- **Automatically during system refresh:** If `slack-scan-state.json → backfill_scans → {scan_type}.status` is `not_started` and the conversation database has fewer than 500 rows in `slack_messages`, run DM archaeology and voice corpus as part of the first system refresh after deployment.
- **On knowledge gap detection:** If an agent needs context about a person, project, or decision and the conversation database has no relevant data, the agent should trigger the appropriate scan before proceeding.
- **During morning routine meeting prep:** If the morning routine is preparing for a meeting and `slack_people` has no record for a key participant, trigger a targeted DM scan for that contact.
- **Ad-hoc by Richard:** Richard can say "run DM archaeology" or any scan name to trigger manually. This is the fallback, not the primary path.

**Spec:** `.kiro/specs/slack-deep-context/`
**Database:** `ps-analytics.duckdb` (via DuckDB MCP `execute_query`)
**Scan state:** `~/shared/context/active/slack-scan-state.json`
**Channel registry:** `~/shared/context/active/slack-channel-registry.json`
**Guardrails:** `~/.kiro/steering/slack-guardrails.md`
**Richard's user_id:** `U040ECP305S`

**Quick query views (use via DuckDB MCP):**
- `SELECT * FROM slack_feed WHERE signal_type = 'decision' LIMIT 10` — human-readable feed with author aliases
- `SELECT * FROM slack_activity WHERE total_messages > 5` — per-person activity summary
- `SELECT * FROM slack_feed WHERE channel_name = 'ab-paid-search-global' ORDER BY ts DESC LIMIT 20` — channel history

**Python query functions (via `query.py`):**
- `slack_channel_summary()` — message counts and signal breakdown per channel
- `slack_recent(channel_name, limit, signal_type)` — recent messages with filters
- `slack_search(keyword)` — full-text search across all messages
- `slack_person(alias_or_id)` — person activity summary
- `slack_decisions(weeks)` — recent decisions
- `slack_action_items()` — unresolved action items

---

## 1. Backfill Orchestration Rules

All eleven backfill scans follow the same pattern. Do not deviate.

### Common Backfill Flow

```
1. Scan triggered (by agent, workflow, hook, or Richard)
2. Read this steering file
3. FIRST: call list_channels with channelTypes: ["public_and_private"] to get ALL channels Richard is in — do NOT rely solely on the channel registry. The registry is a subset.
4. Construct Slack MCP queries per scan instructions below
5. Paginate through ALL results — do NOT stop at first page. Follow pagination cursors to exhaustion.
6. For searches: paginate through ALL pages (page 1, 2, 3... until no more results). Slack search returns 20 results per page — a search with 100 results needs 5 pages.
7. Batch INSERT all messages to DuckDB at end of scan
8. Synthesize findings from the collected data
9. Route synthesis to target organ (or intake/ if over word budget)
10. Update slack-scan-state.json → backfill_scans with completion record
```

### Channel Scope for Backfills

**Initial backfills must be liberal.** The goal is to build a comprehensive baseline, not a filtered view.

- **Team channels (private, <20 members):** Scan ALL messages. These are the highest-signal channels.
- **Org channels (private, 20-250 members):** Scan ALL messages. These contain cross-team context.
- **Community channels (public, 250+ members):** Search only (keyword queries), don't scan full history. Too noisy for full ingestion.
- **Group DMs:** Scan ALL messages. These often contain coordination context missing from channels.
- **DMs with People Watch contacts:** Covered by DM Archaeology scan.

Richard's full channel list (from list_channels) includes ~47 channels. The channel registry tracks ~12. Backfills must use the full list, not the registry subset.

**Pagination is mandatory.** Slack search returns 20 results per page. A query returning 100 results needs pages 1-5. Never stop at page 1.

### DuckDB Write Rules

All writes use `INSERT OR REPLACE` — re-running a scan with the same data is safe (idempotent).

**Tables and columns for reference:**

`slack_messages`: ts (PK), channel_id, channel_name, thread_ts, author_id, author_alias, author_name, text_preview, full_text, is_richard, is_thread_reply, reply_count, reaction_count, richard_reacted, relevance_score, signal_type, ingested_at

`slack_threads`: thread_ts (PK), channel_id, channel_name, topic_summary, participant_aliases, message_count, decision_extracted, action_items, first_ts, last_ts, ingested_at

`slack_people`: user_id (PK), alias, display_name, first_interaction, last_interaction, total_messages, dm_messages, channel_messages, channels_shared, avg_response_time_hours, relationship_tier, ingested_at

`slack_topics`: topic + week (composite PK), channel_count, message_count, participant_count, key_participants, status, related_project, ingested_at

`decisions`: id (PK), decision_type, market, description, rationale, made_by, approved_by, approval_required, status, outcome, created_at, resolved_at

Batch all INSERTs at the end of the scan, not per-message. DuckDB handles bulk inserts in milliseconds.

### Rate Limit Handling

When the Slack API returns a rate limit response:
1. Log the event to `slack-scan-state.json → tool_invocation_log` with timestamp, tool, and "rate_limited" result
2. Pause for the duration specified in the Retry-After header (typically 30–60 seconds)
3. Resume from the last position — the batch buffer persists in your context
4. Increment `rate_limit_pauses` in the scan's backfill_scans entry
5. NEVER fail the entire scan due to rate limits — partial progress is preserved in DuckDB

### Organ Routing Rules

| Data Type | Target | Condition |
|-----------|--------|-----------|
| Relationship data (DM patterns, tone, frequency) | `memory.md` → relationship graph | Within word budget |
| Decisions (high-impact) | `brain.md` → decision log | Highest-impact only |
| Decisions (full set) | DuckDB `decisions` table | Always — complete record |
| Market/project data | `eyes.md` + `current.md` | Within word budget |
| Meeting context | Meeting series files in `~/shared/wiki/meetings/` | Per-series |
| Voice data | `~/shared/context/voice/` | New file, not an organ |
| Any overflow | `~/shared/context/intake/` | Tagged `[target: organ_name]` |

### Word Budget Compliance

Before writing to ANY organ:
1. Check `gut.md` word budget table for the target organ
2. If the organ is at or over budget, route to `~/shared/context/intake/` instead
3. Tag overflow files with `[target: organ_name]` so the next compression cycle picks them up
4. Raw data ALWAYS goes to DuckDB regardless of organ budget — the database is the complete record

### Attribution

All backfill outputs include an attribution tag:
```
[Slack Backfill: {scan_type}, {date_range}, {date}]
```
Example: `[Slack Backfill: DM archaeology, full history, 2026-04-05]`

### Progress Tracking

After each scan completes, update `slack-scan-state.json → backfill_scans → {scan_type}`:
```json
{
  "status": "completed",
  "triggered": "ISO timestamp when Richard triggered",
  "completed": "ISO timestamp when scan finished",
  "messages_ingested": 0,
  "rate_limit_pauses": 0,
  "synthesis_routed_to": "target organ or intake/"
}
```
While running, set `status: "in_progress"`. If interrupted, the in_progress status tells you to resume on next trigger.

### Audit Logging

Log every Slack MCP tool invocation to `slack-scan-state.json → tool_invocation_log`:
```json
{
  "timestamp": "ISO",
  "tool": "tool_name",
  "query": "search query or channel ID",
  "rationale": "Backfill: {scan_type}",
  "result": "success — N matches" or "rate_limited" or "error — description"
}
```


---

## 2. DM Archaeology

**Trigger:** Agent detects empty/sparse relationship data in slack_people for People Watch contacts, OR system refresh finds backfill_scans.dm_archaeology.status == "not_started", OR Richard says "run DM archaeology"
**Requirements:** 7.1–7.7

### Procedure

1. Load People Watch contacts from `slack-channel-registry.json → people_watch` (always_high_relevance + boosted lists)

2. For each People Watch contact:
   a. Call `list_channels` with `channelTypes: ["dm"]` — find the DM channel for this contact
   b. Call `batch_get_conversation_history` on the DM channel
   c. Paginate to full history — follow `next_cursor` until exhausted
   d. For each message, record:
      - `is_richard = TRUE` if `author_id == U040ECP305S`, else `FALSE`
      - `channel_name` = DM with {contact alias}
      - `signal_type` = NULL (backfill — not scored)

3. Batch `INSERT OR REPLACE INTO slack_messages` all collected DM messages

4. For each contact, `INSERT OR REPLACE INTO slack_people`:
   - `dm_messages` = count of DM messages
   - `avg_response_time_hours` = average time between Richard's message and contact's reply (and vice versa)
   - `first_interaction` = earliest message date
   - `last_interaction` = most recent message date
   - `total_messages` = update with DM count added to existing channel count
   - `relationship_tier` = sync from People Watch status

5. Scan for non-People-Watch contacts with high DM volume:
   - After processing People Watch DMs, check `list_channels` DM results for other contacts
   - Any contact with 20+ DM messages who is NOT in People Watch → add to `slack-scan-state.json → people_watch_candidates`

### Synthesis (per contact)

For each People Watch contact, synthesize:
- **Communication frequency:** How often do they DM? Daily, weekly, sporadic?
- **Tone patterns:** Formal vs casual, emoji usage, opener patterns ("Hey", "Hi", none), closer patterns ("Thanks,", "Cheers,", none)
- **Topic distribution:** What do they DM about? (projects, quick questions, escalations, social)
- **Response latency:** Average response time in hours — both directions

### Routing

- Route per-contact synthesis to `memory.md` relationship graph entries
- Enrich existing entries with DM-specific tone notes and topic patterns
- Check `gut.md` word budget for memory.md before writing — overflow to `~/shared/context/intake/` tagged `[target: memory.md]`
- Attribution: `[Slack Backfill: DM archaeology, full history, {today's date}]`

### Scan State Update

```json
{
  "dm_archaeology": {
    "status": "completed",
    "triggered": "...",
    "completed": "...",
    "contacts_scanned": 15,
    "messages_ingested": 4200,
    "rate_limit_pauses": 0,
    "synthesis_routed_to": "memory.md"
  }
}
```


---

## 3. Voice Corpus

**Trigger:** Agent needs Slack-specific voice data for drafting (richard-style-slack.md doesn't exist), OR system refresh finds backfill_scans.voice_corpus.status == "not_started", OR Richard says "run voice corpus scan"
**Requirements:** 8.1–8.6

### Procedure

1. `search` with query `from:@prichwil` — paginate all results across 12 months
   - Use `after:` date modifier set to 12 months ago
   - Follow pagination until all results retrieved

2. For each message:
   - `INSERT OR REPLACE INTO slack_messages` with `is_richard = TRUE`
   - Capture `channel_name` and `thread_ts` to categorize by context (DM vs channel vs thread reply)

3. Categorize all Richard messages by context:
   - **DM messages:** channel is a DM conversation
   - **Channel messages:** top-level messages in public/private channels
   - **Thread replies:** messages where `is_thread_reply = TRUE`

### Analysis

Analyze the full corpus for:

- **Sentence length distribution:** Average words per message by context (DM, channel, thread)
- **Punctuation habits:** Period usage, exclamation marks, question marks, ellipsis, em dashes
- **Emoji frequency and patterns:** Which emoji, how often, in what contexts (reactions vs inline)
- **Formality gradient:**
  - DMs: most casual (fragments, no greeting, rapid-fire)
  - Channels: moderate (complete sentences, occasional greeting)
  - Threads: varies by audience and topic
- **Opening patterns:** "Hey", "Hi", "Hi!", none (just starts talking), @mention
- **Closing patterns:** "Thanks,", "Thank you,", "Thanks!", none, emoji-only
- **Escalation language:** Words/phrases Richard uses when raising urgency
- **De-escalation language:** Words/phrases Richard uses when calming things down

### Comparison

Compare findings against `~/.kiro/steering/richard-writing-style.md`:
- Note where Slack voice differs from email voice (likely: shorter sentences, more emoji, less formal closings, stream-of-consciousness pacing)
- Note where they align (likely: direct tone, data-first approach, parenthetical asides)

### Output

Write analysis to `~/shared/context/voice/richard-style-slack.md`

Structure the file by:
1. Context sections: DM, Channel, Thread
2. Within each context: formality level, typical patterns, example phrases
3. Comparison notes vs email register
4. Escalation/de-escalation vocabulary

This file is NOT an organ — it lives in portable-body and is loaded by agents drafting Slack messages.

### Routing

- Output file: `~/shared/context/voice/richard-style-slack.md`
- Attribution: `[Slack Backfill: voice corpus, 12 months, {today's date}]`
- No organ write needed — this is a standalone reference file


---

## 4. Decision Mining

**Trigger:** Agent needs historical decision context and DuckDB decisions table has < 10 rows, OR system refresh finds backfill_scans.decision_mining.status == "not_started", OR Richard says "run decision mining"
**Requirements:** 9.1–9.7

### Procedure

1. `search` for each decision language pattern across team channels, 12 months:
   - `"decided" after:{12 months ago}`
   - `"going with" after:{12 months ago}`
   - `"confirmed" after:{12 months ago}`
   - `"approved" after:{12 months ago}`
   - `"let's do" after:{12 months ago}`
   - `"final call" after:{12 months ago}`
   - `"we're not going to" after:{12 months ago}`
   - Scope to team channels from `slack-channel-registry.json` (AB PS, WW Testing sections) — exclude community/general channels to reduce noise
   - Paginate each query to completion

2. Deduplicate results — the same message may match multiple patterns

3. For each decision message:
   - `INSERT OR REPLACE INTO slack_messages` with `signal_type = 'decision'`
   - If the message is in a thread, pull thread context via `batch_get_thread_replies` to understand the full decision discussion

4. Extract structured decisions and `INSERT OR REPLACE INTO decisions`:
   - `decision_type`: budget, strategy, launch, process, personnel, tool
   - `market`: AU, MX, US, EU5, JP, CA, WW, or NULL if not market-specific
   - `description`: one-sentence summary of what was decided
   - `rationale`: why — extracted from thread context
   - `made_by`: alias of the person who made/announced the decision
   - `created_at`: timestamp of the decision message
   - `status`: 'active' (default for historical decisions)

### Synthesis

- Identify high-impact decisions: multi-market scope OR made by L7+ stakeholders (brandoxy, kataxt, theimes, lenazak)
- For high-impact decisions, produce a summary for `brain.md` decision log
- Map each decision to existing `brain.md` decision principles where applicable:
  - "Holistic measurement over segmented Brand/NB goals"
  - "Efficiency over escalation as competitive response"
  - "Evidence-based phased rollouts (OCI playbook)"
  - Note which principle each decision reinforces or qualifies

### Routing

- High-impact decision summaries → `brain.md` decision log (respect word budget — only highest-impact)
- Full decision set → DuckDB `decisions` table (always — complete record)
- If `brain.md` is at word budget capacity → overflow to `~/shared/context/intake/` tagged `[target: brain.md]`
- Attribution: `[Slack Backfill: decision mining, 12 months, {today's date}]`


---

## 5. Project Timeline Reconstruction

**Trigger:** Agent needs project history for wiki article or OP1 narrative and slack_messages has no rows with signal_type = 'project:{name}', OR Richard says "reconstruct timeline for [project name]"
**Requirements:** 10.1–10.6

### Known Projects

| Project | Search Terms | Expected Channels |
|---------|-------------|-------------------|
| OCI | `OCI`, `"optimized click identifier"` | ab-paid-search-oci, ab-paid-search-global, ab-ps_jp |
| Polaris | `Polaris`, `"brand LP"`, `"landing page"` | ab-paid-search-global, mcs-ps-redirect-expansion |
| Baloo | `Baloo` | baloo-search-and-mcs |
| F90 | `F90` | ab-ps_partnership-accounts |
| Ad copy overhaul | `"ad copy"`, `"ad creative"`, `"ad text"` | ab-paid-search-global, ab-paid-search-eu |
| Walmart response | `Walmart`, `"competitive response"` | ab-paid-search-global, ab-outbound-marketing |

### Procedure

1. `search` for the project name (and alternate terms) across all channels, full lifecycle
   - No date restriction — search the full history to capture project inception through current state
   - Paginate all results

2. `INSERT OR REPLACE INTO slack_messages` with `signal_type = 'project:{project_name}'`
   - Example: `signal_type = 'project:OCI'`

3. For threads with 3+ messages about the project, pull full thread via `batch_get_thread_replies`

4. Construct structured timeline from the collected messages:

### Timeline Output Format

```markdown
# {Project Name} — Slack Timeline Reconstruction

[Slack Backfill: project timeline, {project}, full lifecycle, {today's date}]

## Key Milestones
| Date | Milestone | Driven By | Channel | Source |
|------|-----------|-----------|---------|--------|
| 2025-10-15 | OCI pilot launched in CA | staceygu | ab-paid-search-oci | ts:1729000000 |
| ... | ... | ... | ... | ... |

## Decisions
- {date}: {decision} — made by {person} in #{channel}

## Blockers & Resolutions
- {date}: BLOCKER — {description}. RESOLVED {date}: {resolution}

## Discrepancies vs Existing Docs
- {description of discrepancy between Slack timeline and existing wiki/artifact}
```

5. Cross-reference with existing wiki article drafts in `~/shared/wiki/` and `~/shared/wiki/` — flag any discrepancies between the reconstructed timeline and documented history

### Routing

- Route timeline document to `~/shared/context/intake/` for processing into wiki articles and `current.md`
- Tag: `[target: current.md, wiki]`
- Attribution: `[Slack Backfill: project timeline, {project}, full lifecycle, {today's date}]`


---

## 6. Stakeholder Position Mapping

**Trigger:** Agent preparing meeting prep or predicted QA and slack_people has no enriched data for key stakeholders, OR system refresh finds backfill_scans.stakeholder_positions.status == "not_started", OR Richard says "run stakeholder position mapping"
**Requirements:** 11.1–11.6

### Key Stakeholders

| Name | Alias | Slack User ID | Role | Search Query |
|------|-------|---------------|------|-------------|
| Kate Rundell | kataxt | UNRESOLVED_kataxt | L8 Director, skip-level | `from:@kataxt` |
| Brandon Munday | brandoxy | U03H47TS508 | L7 Manager | `from:@brandoxy` |
| Lena Zak | lenazak | — | L7 AU Country Leader | `from:@lenazak` |
| Nick Georgijev | — | — | Leadership | `from:@nickgeor` or name search |

### Procedure

1. For each stakeholder, `search` with `from:@{alias}` across all channels, 6 months:
   - Use `after:` date modifier set to 6 months ago
   - Paginate all results
   - These searches go across ALL channels — not just Richard's — to capture stakeholder activity in channels Richard may not be in

2. `INSERT OR REPLACE INTO slack_messages` for all stakeholder messages
   - Set `author_alias` and `author_name` from search results

3. `INSERT OR REPLACE INTO slack_people` for each stakeholder:
   - Update `total_messages`, `channel_messages`, `last_interaction`
   - Update `channels_shared` — count channels where both Richard and this stakeholder appear

4. For threads where the stakeholder made decisions or escalated, pull full thread context via `batch_get_thread_replies`

### Per-Stakeholder Synthesis

For each stakeholder, produce:

- **Topics raised most frequently:** What do they talk about? Rank by message count.
- **Language when concerned vs satisfied:**
  - Concerned: what words/phrases signal worry? (e.g., "I'm not seeing...", "when can we expect...", "this needs to...")
  - Satisfied: what words/phrases signal approval? (e.g., "great work", "this is exactly...", "love this")
- **Escalation triggers:** What topics or situations cause them to escalate? Include specific examples with source attribution (channel, date, quote).
- **Priority shifts over time:** How have their focus areas changed over the 6-month window? (e.g., Kate shifted from X to Y in month 3)
- **Specific examples:** For each pattern identified, include at least one concrete example with channel name, date, and a brief quote.

### Routing

- Route per-stakeholder synthesis to `memory.md` relationship graph entries — enrich existing entries
- Route meeting-relevant findings to corresponding meeting series files:
  - Kate findings → `meetings/team/` files where Kate appears
  - Brandon findings → `meetings/manager/brandon-sync.md`
  - Lena findings → `meetings/stakeholder/au-paid-search-sync.md`
- Check `gut.md` word budget for `memory.md` before writing — overflow to `~/shared/context/intake/` tagged `[target: memory.md]`
- Attribution: `[Slack Backfill: stakeholder positions, 6 months, {today's date}]`


---

## 7. Pre-Meeting Context

**Trigger:** Agent preparing meeting prep and meeting series file has no Slack context section, OR system refresh finds backfill_scans.pre_meeting_context.status == "not_started", OR Richard says "run pre-meeting context scan"
**Requirements:** 12.1–12.6

### Meeting Series

| Meeting | File | Key Participants | Typical Day/Time |
|---------|------|-----------------|-----------------|
| AU Paid Search Sync | `meetings/stakeholder/au-paid-search-sync.md` | Lena Zak, Alexis Eck | Weekly |
| MX Paid Search Sync | `meetings/stakeholder/mx-paid-search-sync.md` | Lorena Alvarez Larrea | Weekly |
| Brandon 1:1 | `meetings/manager/brandon-sync.md` | Brandon Munday | Weekly |
| Adi sync | `meetings/peer/adi-sync.md` | Adi Thakur | Weekly |
| Andrew sync | `meetings/peer/andrew-sync.md` | Andrew Wirtz | Weekly |
| Yun sync | `meetings/peer/yun-sync.md` | Yun-Kang Chu | Weekly |
| Deep Dive & Debate | `meetings/team/deep-dive-debate.md` | Full team | Weekly |
| Weekly Paid Acq | `meetings/team/weekly-paid-acq.md` | Full team | Weekly |
| Pre-WBR Customer Engagement | `meetings/team/pre-wbr-customer-engagement.md` | Full team + stakeholders | Weekly |

### Procedure

1. Get Richard's recurring meeting times from calendar:
   - Use `calendar_view` or `calendar_search` to identify recurring meeting times for each series above
   - Record day-of-week and time for each meeting over the past 6 months

2. For each meeting occurrence over 6 months:
   a. Calculate the 2-hour window before and after the meeting time
   b. `search` for messages from key participants in that window:
      - `from:@{participant_alias} after:{2h before meeting} before:{2h after meeting}`
      - Also search for the meeting topic keywords in team channels during the same window
   c. Paginate results

3. `INSERT OR REPLACE INTO slack_messages` for all meeting-adjacent messages
   - Set `signal_type = 'meeting:{series_name}'`
   - Example: `signal_type = 'meeting:au-paid-search-sync'`

4. For threads started within the meeting window, pull full context via `batch_get_thread_replies`

### Per-Meeting-Series Synthesis

For each meeting series, produce:

- **Pre-meeting prep discussions:** What topics come up in Slack in the 2 hours before the meeting? Are participants aligning on agenda items, sharing data, or flagging concerns?
- **Post-meeting follow-ups:** What gets discussed in Slack after the meeting? Action items, clarifications, side conversations that continue the meeting's topics.
- **Unformalised action items:** Action items discussed in Slack before/after the meeting that never made it into meeting notes or task trackers. These are the dropped balls.
- **Patterns:** Does a particular participant consistently raise topics before the meeting that don't get addressed? Does post-meeting Slack activity suggest the meeting isn't resolving issues?

### Routing

- Route per-series synthesis to the corresponding meeting series file in `~/shared/wiki/meetings/`
- Each series file gets a new section: `## Slack Context (Backfill)` with the synthesis
- Check file size before writing — meeting files don't have formal word budgets but keep synthesis concise (200–400 words per series)
- If a meeting file would become unwieldy, route overflow to `~/shared/context/intake/` tagged `[target: meetings/{series_file}]`
- Attribution: `[Slack Backfill: pre-meeting context, 6 months, {today's date}]`


---

## 8. People Discovery — Shadow Network

**Trigger:** Agent detects visibility gaps (e.g., someone references Richard's work in a channel he's not in), OR system refresh finds backfill_scans.people_discovery.status == "not_started", OR Richard says "run people discovery" or "run shadow network scan"
**Requirements:** Idea #8 from slack-deep-context-ideas.md

### What This Finds

People and channels that discuss Richard or his work when he's not in the room. Public channels only — Slack search API won't return results from private channels Richard isn't a member of.

### Procedure

1. `search` with query `prichwil` across ALL of Slack, 6 months:
   - Use `after:` date modifier set to 6 months ago
   - Paginate ALL pages (not just page 1) — follow pagination until exhausted
   - This searches public channels Richard may NOT be a member of — that's the point

2. `search` with query `@prichwil` (direct mentions) across ALL of Slack, 6 months:
   - Same pagination, same date range
   - Captures @mentions specifically vs keyword matches

3. `search` with query `"Richard Williams"` across ALL of Slack, 6 months:
   - Catches full-name references that don't use the alias
   - Paginate all pages

4. Deduplicate results from all three queries

4. For each message:
   - `INSERT OR REPLACE INTO slack_messages` with `signal_type = 'shadow_mention'`
   - Record `channel_id`, `channel_name`, `author_id`, `author_alias`

5. Categorize results:
   - **Known channels:** Channels Richard is already a member of (cross-reference with `list_channels` results or channel registry)
   - **Unknown channels:** Channels Richard is NOT a member of — these are the shadow network signals
   - **Known people:** Authors already in People Watch or slack_people
   - **Unknown people:** Authors not in the relationship graph — potential new contacts

6. For unknown channels with 3+ mentions, call `batch_get_channel_info` to get channel name, member count, purpose

7. `INSERT OR REPLACE INTO slack_people` for any new authors discovered:
   - Set `relationship_tier = 'candidate'`
   - Set `total_messages` from the mention count

### Synthesis

Produce three outputs:

**A. Shadow Channels** — Channels where Richard's work is discussed but he has no presence:
- Channel name, member count, purpose
- How many times Richard/his work was mentioned
- Who's doing the mentioning (are they stakeholders? peers? unknown?)
- Recommendation: join, monitor via proactive search, or ignore

**B. Shadow People** — People who reference Richard but aren't in the relationship graph:
- Alias, name, role (if discoverable from Slack profile)
- How often they mention Richard, in which channels
- Whether they're in channels with Richard's stakeholders
- Recommendation: add to People Watch, note for awareness, or ignore

**C. Visibility Map** — Where is Richard visible vs invisible?
- Channels where Richard is active AND mentioned (strong visibility)
- Channels where Richard is a member but rarely mentioned (weak visibility)
- Channels where Richard is mentioned but not a member (blind spot)
- Channels where Richard's stakeholders are active but Richard is absent (strategic gap)

### Routing

- Shadow Channels list → `~/shared/context/intake/` tagged `[target: current.md, channel-registry]`
- Shadow People list → `slack-scan-state.json → people_watch_candidates` (append, don't overwrite)
- Visibility Map → `~/shared/context/intake/` tagged `[target: nervous-system.md]` (feeds Loop 9 visibility tracking)
- High-priority findings (channels where Kate/Brandon discuss Richard's work) → flag in intake with `[URGENT]`
- Attribution: `[Slack Backfill: people discovery, 6 months, {today's date}]`

### Scan State Update

```json
{
  "people_discovery": {
    "status": "completed",
    "triggered": "...",
    "completed": "...",
    "total_mentions_found": 0,
    "unknown_channels_discovered": 0,
    "unknown_people_discovered": 0,
    "messages_ingested": 0,
    "rate_limit_pauses": 0,
    "synthesis_routed_to": "intake/"
  }
}
```

### Limitations

- **Public channels only.** Private channels Richard isn't a member of won't appear in search results. The shadow network is incomplete by design.
- **Keyword matching.** Searching for "prichwil" may miss references to "Richard" or "Richard Williams" without the alias. Consider adding name-based searches if initial results are sparse.
- **One-time baseline.** After the initial scan, the daily proactive search handles ongoing mention detection. This scan establishes the historical baseline.


---

## 9. Tribal Knowledge Extraction (Wiki Demand Signals)

**Trigger:** Agent needs to prioritize wiki articles by actual demand, OR system refresh finds backfill_scans.tribal_knowledge.status == "not_started", OR Richard says "run tribal knowledge extraction"
**Requirements:** Idea #12 from slack-deep-context-ideas.md

### What This Finds

Questions people ask repeatedly in Slack that reveal gaps in team documentation. This is demand-side signal — what the team doesn't know — as opposed to Task 7.2's supply-side signal (what Richard has already explained).

### Question Patterns

Search for these patterns across team channels, 12 months:
- `"does anyone know"`
- `"how do we"`
- `"where is the"`
- `"what's the process for"`
- `"who owns"`
- `"where can I find"`
- `"is there a doc"`
- `"has anyone done"`
- `"what's the status of"`
- `"how does X work"`

### Procedure

1. For each question pattern, `search` across team channels (from `slack-channel-registry.json` — AB PS, WW Testing sections), 12 months:
   - Use `after:` date modifier set to 12 months ago
   - Scope to team channels to reduce noise from community/general channels
   - Paginate each query to completion

2. Deduplicate results — same message may match multiple patterns

3. For each question message:
   - `INSERT OR REPLACE INTO slack_messages` with `signal_type = 'question'`
   - If the message is in a thread, pull thread context via `batch_get_thread_replies` to check:
     - Was the question answered? By whom?
     - Was the answer a link to a doc (already documented) or an ad-hoc explanation (not documented)?

4. Classify each question:
   - **Topic:** What subject area? (process, tool, data, person/ownership, status)
   - **Answered:** Yes/no. If yes, by whom?
   - **Answer type:** Doc link (documented), ad-hoc explanation (not documented), no answer (gap)
   - **Asker:** Who asked? (role context — is this a new hire, a peer, a stakeholder?)
   - **Recurrence:** Has this same question (or close variant) been asked before?

5. Cluster questions by topic. Recurring questions about the same topic = high-demand wiki candidate.

### Synthesis

Produce a ranked demand list:

```markdown
# Tribal Knowledge Demand Signals

[Slack Backfill: tribal knowledge, 12 months, {today's date}]

## High Demand (3+ occurrences, no existing doc)
| Topic | Times Asked | Askers | Typical Answerer (SME) | Existing Doc? |
|-------|------------|--------|----------------------|---------------|
| OCI ref tag setup process | 5 | aditthk, awirtz, staceygu | prichwil | No |
| ... | ... | ... | ... | ... |

## Medium Demand (2 occurrences or 1 unanswered)
| Topic | Times Asked | Askers | Typical Answerer (SME) | Existing Doc? |
|-------|------------|--------|----------------------|---------------|
| ... | ... | ... | ... | ... |

## Low Demand (1 occurrence, answered)
(List only — no table needed)

## SME Map
| Person | Topics They Answer | Frequency |
|--------|-------------------|-----------|
| prichwil | OCI setup, testing methodology, AU market | 12 |
| brandoxy | Budget process, partnership accounts | 8 |
| ... | ... | ... |
```

### Routing

- Full demand list → append to `~/shared/wiki/demand-log.md`
- Deduplicate against existing entries in demand-log.md before appending
- Cross-reference with existing wiki article drafts in `~/shared/wiki/` — if a draft already covers a high-demand topic, note it as "draft exists, prioritize completion"
- SME map → `~/shared/context/intake/` tagged `[target: memory.md]` (enriches relationship graph with expertise data)
- Attribution: `[Slack Backfill: tribal knowledge, 12 months, {today's date}]`

### Scan State Update

```json
{
  "tribal_knowledge": {
    "status": "completed",
    "triggered": "...",
    "completed": "...",
    "questions_found": 0,
    "topics_clustered": 0,
    "high_demand_topics": 0,
    "messages_ingested": 0,
    "rate_limit_pauses": 0,
    "synthesis_routed_to": "wiki/demand-log.md"
  }
}
```

### Monthly Refresh

Unlike other backfill scans that are one-time, tribal knowledge extraction should re-run monthly as part of the monthly synthesis (enrichment process in `eod-2-system-refresh.kiro.hook`).

**Monthly procedure (lighter than initial backfill):**
1. Query `slack_messages WHERE signal_type = 'question' AND ingested_at > {30 days ago}` — check what's already captured from daily ingestion
2. `search` for question patterns with `after:{30 days ago}` — catch any questions the daily ingestion missed (it doesn't specifically look for question patterns)
3. Cluster new questions with existing demand-log entries
4. Update demand counts and recurrence data in `demand-log.md`
5. Flag any new high-demand topics (3+ occurrences in 30 days) to wiki-editor for prioritization
6. Update `enrichment_state.last_tribal_knowledge_refresh` in `slack-scan-state.json`


---

## 10. Sentiment & Escalation Patterns

**Trigger:** Agent preparing predicted QA or meeting prep and needs stress/escalation context, OR system refresh finds backfill_scans.sentiment_patterns.status == "not_started", OR Richard says "run sentiment scan" or "run escalation patterns"
**Requirements:** Idea #13 from slack-deep-context-ideas.md

### What This Finds

Longitudinal emotional tone patterns in team channels — when does language shift from neutral to urgent, what topics trigger escalation, and what seasonal patterns exist (WBR weeks, QBR prep, OP planning). Builds a "stress forecast" model the system can use for predicted QA and meeting prep.

### Procedure

1. `search` for escalation language patterns across team channels, 12 months:
   - Urgency markers: `"ASAP"`, `"urgent"`, `"need this today"`, `"escalating"`, `"blocker"`, `"critical"`, `"can't wait"`
   - Frustration markers: `"still waiting"`, `"no update"`, `"this was due"`, `"dropped the ball"`, `"why hasn't"`, `"I asked for this"`
   - Positive markers (for contrast): `"great work"`, `"well done"`, `"love this"`, `"exactly what"`, `"ahead of schedule"`, `"smooth launch"`
   - Scope to team channels from `slack-channel-registry.json` (AB PS, WW Testing sections)
   - Use `after:` date modifier set to 12 months ago
   - Paginate each query to completion

2. Deduplicate results across pattern queries

3. For each message:
   - `INSERT OR REPLACE INTO slack_messages` with `signal_type = 'escalation'` (urgency/frustration) or `signal_type = 'positive'` (positive markers)
   - Record `channel_id`, `channel_name`, `author_id`, `author_alias`, `ts`

4. For escalation messages in threads, pull full thread via `batch_get_thread_replies` to capture:
   - What triggered the escalation (the preceding messages)
   - How it was resolved (the following messages)
   - Who de-escalated and what language they used

### Analysis

**Per-stakeholder escalation profile** (key stakeholders: Kate, Brandon, Lena, Nick):
- What topics trigger their escalation language?
- What's their escalation vocabulary? (Some people say "urgent", others say "I'm concerned about...")
- Average time from escalation to resolution
- Who do they escalate TO? (Does Kate escalate to Brandon? Does Brandon escalate to Richard?)
- What de-escalates them? (Data? A plan? Acknowledgment? A timeline?)

**Seasonal stress mapping:**
- Plot escalation message density by week across 12 months
- Identify recurring stress peaks — correlate with:
  - WBR weeks (weekly, but some weeks are worse — month-end, quarter-end)
  - QBR prep periods (2-3 weeks before QBR)
  - OP planning cycles (OP1 in spring, OP2 in fall)
  - Launch windows (OCI rollouts, Polaris migrations)
  - Month-end / quarter-end reporting pressure
- Identify calm periods — what makes a low-stress week?

**Topic-stress correlation:**
- Which topics consistently appear alongside escalation language?
- Which topics appear alongside positive language?
- Are there topics that started positive and turned negative (or vice versa)?

### Synthesis

Produce two outputs:

**A. Stakeholder Escalation Profiles** (per key stakeholder):
```markdown
### {Name} — Escalation Profile
- Triggers: {topics/situations that cause escalation}
- Vocabulary: {their specific escalation phrases}
- Escalation path: {who they escalate to}
- De-escalation: {what calms them — data, plan, acknowledgment, timeline}
- Response time expectation: {how fast they expect a response when escalating}
- Examples: {2-3 concrete examples with date, channel, brief quote}
```

**B. Stress Calendar** (seasonal pattern map):
```markdown
### Stress Calendar — Trailing 12 Months
| Period | Stress Level | Primary Drivers | Key Stakeholders Affected |
|--------|-------------|-----------------|--------------------------|
| WBR weeks (Mon-Tue) | High | Callout deadlines, metric scrutiny | Lena, Brandon |
| QBR prep (2w before) | Very High | Data compilation, narrative drafts | Kate, Brandon |
| OP1 (Apr-May) | High | Goal setting, resource allocation | Kate, Brandon |
| Month-end | Moderate | Reporting, metric reconciliation | Lena |
| Post-launch (1w after) | Moderate-High | Bug reports, performance monitoring | varies |
| Mid-month, no launches | Low | Steady-state operations | — |
```

### Routing

- Stakeholder Escalation Profiles → `~/shared/context/intake/` tagged `[target: memory.md]` (enriches relationship graph with escalation data)
- Stress Calendar → `~/shared/context/intake/` tagged `[target: eyes.md]` (feeds predicted QA stress forecasting)
- If Stakeholder Position Mapping (scan #6) has already run, MERGE escalation profiles with existing stakeholder data rather than creating duplicates
- Attribution: `[Slack Backfill: sentiment patterns, 12 months, {today's date}]`

### Integration with Predicted QA

After this scan completes, eyes.md predicted QA can incorporate stress context:
- If current week matches a high-stress period from the Stress Calendar, boost predicted QA urgency
- If a meeting is with a stakeholder whose escalation triggers match current hot topics, flag in meeting prep
- This is a passive enrichment — no new process, just richer context for existing predicted QA generation

### Scan State Update

```json
{
  "sentiment_patterns": {
    "status": "completed",
    "triggered": "...",
    "completed": "...",
    "escalation_messages_found": 0,
    "positive_messages_found": 0,
    "stakeholders_profiled": 0,
    "stress_periods_identified": 0,
    "messages_ingested": 0,
    "rate_limit_pauses": 0,
    "synthesis_routed_to": "intake/"
  }
}
```

### Limitations

- **Tone is subjective.** Keyword matching for escalation language is a proxy, not a sentiment model. "ASAP" from Kate might be routine; "ASAP" from Brandon might be genuine urgency. The stakeholder profiles help calibrate, but it's imperfect.
- **Seasonal patterns need 12+ months.** With only 12 months of data, you get one data point per seasonal event (one OP1, one OP2, etc.). Patterns are suggestive, not statistically validated. Confidence improves over time as the conversation database accumulates more data.
- **No real-time stress detection.** This is a historical backfill. Real-time escalation detection is handled by the daily ingestion's +20 escalation scoring. This scan provides the baseline context that makes real-time detection more useful.


---

## 11. Slack-Sourced Change Log Entries

**Trigger:** Agent preparing WBR callouts and change_log has gaps between CSV exports, OR system refresh finds backfill_scans.change_log_backfill.status == "not_started", OR Richard says "run change log backfill"
**Requirements:** Idea #16 from slack-deep-context-ideas.md

### What This Finds

Status changes and launches announced in Slack that never made it to the CSV-sourced change_log. These are the "we just launched X" and "dialed up Y to 100%" messages that happen between periodic data exports. Filling these gaps directly improves WBR callout accuracy.

### Change Language Patterns

Search for these patterns across team channels, 12 months:
- Launch language: `"launched"`, `"went live"`, `"is live"`, `"now live"`, `"go live"`, `"rolled out"`, `"rollout complete"`
- Dial/ramp language: `"dialed up"`, `"dialed down"`, `"ramped to"`, `"increased to"`, `"decreased to"`, `"set to"`, `"budget to"`
- Migration language: `"migrated"`, `"switched to"`, `"moved to"`, `"transitioned"`, `"cutover"`
- Test language: `"weblab"`, `"A/B"`, `"test started"`, `"test ended"`, `"results show"`, `"lift of"`
- Pause/stop language: `"paused"`, `"stopped"`, `"turned off"`, `"disabled"`, `"sunset"`

### Procedure

1. For each change language pattern, `search` across ALL channels Richard is in (from `list_channels` — not just the registry subset), 12 months:
   - Use `after:` date modifier set to 12 months ago
   - Include team channels, org channels, and group DMs. Exclude community channels (250+ members) to reduce noise.
   - Paginate EVERY query through ALL pages — Slack returns 20 results per page, follow pagination to exhaustion
   - For private channels: search within each channel individually if broad search returns 0 (Slack search with `in:#channel` works for private channels the user is in)

2. Deduplicate results — same message may match multiple patterns

3. For each change message:
   - `INSERT OR REPLACE INTO slack_messages` with `signal_type = 'change'`
   - If the message is in a thread, pull thread context via `batch_get_thread_replies` to get:
     - What specifically changed (the details often come in replies)
     - Which market was affected
     - What metric was impacted
     - Who made the change

4. Extract structured change_log entries from each message. For each change detected:

   **Field mapping:**
   | change_log column | Extraction logic |
   |-------------------|-----------------|
   | `id` | Auto-increment: `SELECT MAX(id) + 1 FROM change_log` as starting point, increment per entry |
   | `market` | Extract from message context: channel name (ab-ps_jp → JP), explicit market mention (AU, MX, US, etc.), or 'WW' if multi-market |
   | `date` | Date of the Slack message (not ingestion date) |
   | `category` | Classify: 'launch', 'budget_change', 'test_start', 'test_end', 'migration', 'pause', 'config_change' |
   | `description` | One-sentence summary of what changed, extracted from message + thread context |
   | `impact_metric` | If mentioned: CPC, CPA, regs, spend, impressions, clicks, CTR, CVR. NULL if not stated. |
   | `impact_value` | Numeric value if stated (e.g., "CPA dropped 15%" → -15.0). NULL if not stated. |
   | `source` | Always `'slack'` — distinguishes from CSV-sourced entries (`'csv'`) |

5. Before INSERT, deduplicate against existing change_log entries:
   - Check for same market + same date + similar description (fuzzy match)
   - If a CSV-sourced entry already covers this change, skip the Slack-sourced entry
   - If the Slack message adds detail the CSV entry lacks, note it but don't create a duplicate

6. Batch `INSERT INTO change_log` all new entries

### Quality Rules

- **Only concrete changes.** "We should launch next week" is NOT a change log entry. "Launched today" IS.
- **Market must be identifiable.** If the message doesn't specify or imply a market, skip it. Don't guess.
- **One entry per change.** A thread discussing a launch gets one change_log row, not one per message.
- **Prefer specificity.** "Dialed up JP OCI to 100% of traffic" is better than "made changes to JP."
- **impact_metric and impact_value are optional.** Many Slack announcements don't include metrics. That's fine — the description alone is valuable for callout context.

### Synthesis

After all entries are inserted, produce a summary:

```markdown
# Change Log Backfill — Slack Sources

[Slack Backfill: change log, 12 months, {today's date}]

## New Entries Added: {count}
## Duplicates Skipped: {count} (already in CSV-sourced data)

### By Market
| Market | Entries Added | Date Range |
|--------|-------------|------------|
| AU | 12 | 2025-06 to 2026-03 |
| JP | 8 | 2025-09 to 2026-04 |
| ... | ... | ... |

### By Category
| Category | Count |
|----------|-------|
| launch | 15 |
| budget_change | 22 |
| test_start | 8 |
| ... | ... |

### Gap Periods Filled
Months where CSV exports had 0 entries but Slack had changes:
- {month}: {count} entries added
```

### Routing

- All entries → DuckDB `change_log` table directly (this is the primary output)
- Summary → `~/shared/context/intake/` tagged `[target: eyes.md]` (callout pipeline awareness)
- No organ writes needed — the change_log table IS the destination, and the callout pipeline reads it directly
- Attribution: `[Slack Backfill: change log, 12 months, {today's date}]`

### Ongoing Capture

After the initial backfill, the daily ingestion should also write change_log entries when it detects status-change signals. Add to the signal routing logic:
- When `signal_type = 'status-change'` is extracted during daily ingestion, ALSO `INSERT INTO change_log` with `source = 'slack'`
- This keeps the change_log current between CSV exports without requiring another backfill

### Scan State Update

```json
{
  "change_log_backfill": {
    "status": "completed",
    "triggered": "...",
    "completed": "...",
    "messages_scanned": 0,
    "entries_added": 0,
    "duplicates_skipped": 0,
    "markets_covered": [],
    "messages_ingested": 0,
    "rate_limit_pauses": 0,
    "synthesis_routed_to": "change_log table + intake/"
  }
}
```


---

## 12. Experiment Backfill from Slack

**Trigger:** Agent preparing testing methodology artifacts and experiments table has 0 rows, OR system refresh finds backfill_scans.experiment_backfill.status == "not_started", OR Richard says "run experiment backfill"
**Requirements:** Idea #17 from slack-deep-context-ideas.md

### What This Finds

Full experiment lifecycles discussed in Slack — from hypothesis through launch, results, and decision. Unlike Change Log Backfill (scan #11) which captures the *event* ("test started"), this scan captures the *structured experiment record* (hypothesis, variants, duration, results, decision). Populates the DuckDB `experiments` table (currently 0 rows).

### Relationship to Change Log Backfill

These two scans share search patterns but produce different outputs:
- Change Log Backfill → `change_log` table rows (what happened, when)
- Experiment Backfill → `experiments` table rows (full test lifecycle)

If both scans run, they can share the same Slack search results. Run Change Log Backfill first — its `slack_messages` rows with `signal_type = 'change'` are a starting point for experiment extraction.

### Experiment Language Patterns

Search for these patterns across team channels, 12 months:
- Test identity: `"weblab"`, `"A/B test"`, `"experiment"`, `"test plan"`, `"control vs"`, `"variant"`
- Test lifecycle: `"test started"`, `"test launched"`, `"test ended"`, `"test concluded"`, `"test paused"`, `"extending the test"`
- Results language: `"results show"`, `"lift of"`, `"statistically significant"`, `"no significant"`, `"confidence"`, `"p-value"`, `"conversion rate"`, `"incremental"`
- Decision language: `"scaling"`, `"rolling out"`, `"reverting"`, `"keeping the control"`, `"going with variant"`

### Procedure

1. Check if Change Log Backfill has already run:
   - If yes: query `slack_messages WHERE signal_type = 'change' AND full_text ILIKE '%weblab%' OR full_text ILIKE '%test%' OR full_text ILIKE '%A/B%'` — use these as a starting point, supplement with additional searches below
   - If no: run full searches from scratch

2. For each experiment language pattern, `search` across team channels (from `slack-channel-registry.json` — AB PS, WW Testing, OCI sections), 12 months:
   - Use `after:` date modifier set to 12 months ago
   - Scope to team channels
   - Paginate each query to completion

3. Deduplicate results across pattern queries and against existing `slack_messages` rows

4. For each experiment-related message:
   - `INSERT OR REPLACE INTO slack_messages` with `signal_type = 'experiment'`
   - Pull full thread context via `batch_get_thread_replies` — experiment discussions often span multiple messages in a thread

5. **Lifecycle stitching** — the hard part. Group messages into experiment lifecycles:
   a. Identify unique experiments by name/identifier (weblab ID, test name, project + "test")
   b. For each experiment, find:
      - **Start signal:** "test started", "weblab launched", "experiment live"
      - **Progress signals:** "extending", "paused", "resumed", mid-test data shares
      - **End signal:** "test ended", "results show", "concluded"
      - **Decision signal:** "scaling", "reverting", "going with" (may also appear in Decision Mining results)
   c. These signals may be in different threads, different channels, weeks apart. Use the experiment name/ID as the stitching key.
   d. If lifecycle is incomplete (e.g., start found but no end), still create the record with `status = 'unknown'` and NULL fields for missing data

6. For each stitched experiment, extract a structured record:

   **Field mapping to `experiments` table:**
   | Column | Extraction logic |
   |--------|-----------------|
   | `experiment_id` | Weblab ID if available, otherwise generate: `slack-{market}-{YYYYMM}-{seq}` |
   | `name` | Descriptive name from Slack context (e.g., "JP OCI ref tag A/B test") |
   | `hypothesis` | If stated in thread: extract verbatim. If not stated: infer from context and mark `[inferred]`. If unknowable: NULL. |
   | `start_date` | Date of earliest "test started" message. NULL if not found. |
   | `end_date` | Date of "test ended" / "results" message. NULL if test still running or end not found. |
   | `status` | 'completed' (has results), 'active' (started, no end), 'cancelled' (explicitly stopped), 'unknown' (incomplete data) |
   | `result` | One-sentence summary of outcome. NULL if no results shared. |
   | `metric_before` | Numeric baseline if stated. NULL if not. |
   | `metric_after` | Numeric result if stated. NULL if not. |
   | `effect_size` | Percentage lift/decline if stated (e.g., +12.0 for 12% lift). NULL if not. |
   | `decision` | What was decided: 'scaled', 'reverted', 'extended', 'pending', NULL |

7. Batch `INSERT OR REPLACE INTO experiments` all extracted records

### Quality Rules

- **Prefer explicit over inferred.** If the hypothesis isn't stated in Slack, mark it `[inferred]` so it's clear this is agent interpretation, not team documentation.
- **One row per experiment.** Multiple threads about the same test → one experiments row. Use the experiment name/ID to deduplicate.
- **Don't fabricate metrics.** If "results show positive lift" but no number is given, set `effect_size = NULL` and put "positive lift, magnitude not stated" in `result`.
- **Incomplete records are valuable.** An experiment with only a start_date and name is still better than 0 rows. The table can be enriched later.
- **Cross-reference with Decision Mining.** If scan #4 found a decision that maps to an experiment ("going with variant B for JP OCI"), link them: set the experiment's `decision` field accordingly.

### Synthesis

After all entries are inserted, produce a summary:

```markdown
# Experiment Backfill — Slack Sources

[Slack Backfill: experiment backfill, 12 months, {today's date}]

## Experiments Found: {count}
## Complete Records (all fields populated): {count}
## Partial Records (missing hypothesis, results, or decision): {count}

### By Market
| Market | Experiments | Completed | Active | Unknown |
|--------|------------|-----------|--------|---------|
| AU | 4 | 3 | 0 | 1 |
| JP | 3 | 1 | 2 | 0 |
| WW | 2 | 1 | 0 | 1 |
| ... | ... | ... | ... | ... |

### By Status
| Status | Count |
|--------|-------|
| completed | 8 |
| active | 3 |
| unknown | 4 |

### Notable Findings
- Experiments with results but no documented decision: {list}
- Experiments started 3+ months ago with no end signal: {list}
- Tests where hypothesis was never stated: {list}
```

### Routing

- All experiment records → DuckDB `experiments` table directly (primary output)
- Summary → `~/shared/context/intake/` tagged `[target: brain.md, eyes.md]`
- Experiments with `status = 'active'` and `start_date` > 60 days ago → flag in intake as `[STALE-TEST]` for Richard's attention
- Experiments with results but no decision → flag in intake as `[DECISION-NEEDED]`
- Attribution: `[Slack Backfill: experiment backfill, 12 months, {today's date}]`

### Ongoing Capture

After the initial backfill, the daily ingestion should also create/update experiment records when it detects test-related signals:
- When `signal_type = 'status-change'` contains test/weblab language during daily ingestion, check if an `experiments` row exists for that test
- If yes: update `status`, `end_date`, `result`, `effect_size`, `decision` as new data arrives
- If no: create a new row with available fields, `status = 'active'`
- This keeps the experiments table current without requiring another backfill

### Scan State Update

```json
{
  "experiment_backfill": {
    "status": "completed",
    "triggered": "...",
    "completed": "...",
    "messages_scanned": 0,
    "experiments_found": 0,
    "complete_records": 0,
    "partial_records": 0,
    "messages_ingested": 0,
    "rate_limit_pauses": 0,
    "synthesis_routed_to": "experiments table + intake/"
  }
}
```

### Limitations

- **Lifecycle stitching is imperfect.** Slack threads rarely contain the full experiment lifecycle in one place. A "test started" message in March and a "results show" message in April in a different thread require the agent to infer they're the same experiment. The experiment name/ID is the stitching key, but not all tests are named consistently.
- **Hypothesis is often unstated.** Teams frequently run tests without documenting the hypothesis in Slack. The `[inferred]` tag makes this visible, but many records will have NULL or inferred hypotheses.
- **Metrics are sparse.** Detailed results (metric_before, metric_after, effect_size) are often shared in spreadsheets or dashboards, not Slack. Expect many NULL metric fields. The description and decision fields carry more value from Slack sources.