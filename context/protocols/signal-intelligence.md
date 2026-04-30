<!-- DOC-0358 | duck_id: protocol-signal-intelligence -->


# Signal Intelligence Protocol

Cross-channel topic tracking with reinforcement and decay. Unifies Slack, Email, Asana, and Hedy signals into a single queryable layer in DuckDB.

---



## Core Concept

Every mention of a topic across any channel creates or reinforces a signal in `signal_tracker`. Signals strengthen when the same topic appears again (reinforcement). Signals weaken over time when the topic goes quiet (decay). The result is a live heat map of what matters right now.



### Signal Lifecycle
1. **First mention** → new row in signal_tracker (strength = 1.0)
2. **Reinforcement** → same topic appears again in any channel → strength += 0.5, reinforcement_count += 1, last_seen updated
3. **Decay** → daily decay: strength *= 0.9 (10% per day). After 14 days of silence, strength ≈ 0.23. After 30 days, strength ≈ 0.04.
4. **Deactivation** → when strength < 0.1, mark is_active = false. Signal is archived, not deleted.
5. **Reactivation** → if a deactivated topic reappears, set is_active = true, strength = 1.0, reinforcement_count += 1.



### Channel-Specific Ingestion

| Channel | Source | How Topics Are Extracted | Source ID |
|---------|--------|------------------------|-----------|
| Slack | AM-1 Slack scan | FTS match_bm25 against known topics + new topic detection from high-relevance messages | message ts |
| Email | AM-1 email triage | Subject line + body keyword extraction | conversation id |

#### Channel-Specific Ingestion — Details

| Asana | AM-2 task scan | Task name + description keywords, comment mentions | task gid |
| Hedy | EOD-1 meeting sync | Meeting transcript topic extraction, agenda items | session id |



### Topic Normalization
Topics are lowercase, hyphenated slugs: `oci-rollout`, `au-cpa-cvr`, `mx-budget-ieccp`, `polaris-brand-lp`, `liveramp-enhanced-match`, `kate-skip-level`. The agent normalizes on ingest — "OCI rollout", "OCI Rollout", "oci rollout status" all map to `oci-rollout`.

**CRITICAL: Slug consistency across channels.** Slack ingestion tends to use display names ("Brand LP Polaris Transition") while Hedy uses slugs ("polaris-lp-testing"). Both must normalize to the same canonical slug. Without this, the same topic fragments across rows and never reaches cross-channel quality thresholds. Canonical slug format: `{project-or-topic}-{subtopic}` — always lowercase, always hyphenated.

**Canonical slug registry** (add new entries as topics emerge):
| Canonical Slug | Variants to Normalize |
|---------------|----------------------|
| `polaris-brand-lp` | Brand LP Polaris Transition, polaris-lp-testing, polaris-lp-revert, brand-page-transition, brand-lp-consolidated-feedback, Polaris LP Brand Page ETA Request |
| `mx-budget-ieccp` | MX Budget Underspend, MX Budget Line, ABMA Expansion Market SIM |
| `au-cpa-cvr` | Lena MX LP Confusion, AU CPA trends, au-cpa-trends |
| `oci-rollout` | OCI CA Launch, OCI CA Launch Monday, OCI WW Launch |
| `pam-budget` | PAM Budget Availability |
| `liveramp-enhanced-match` | LiveRamp Enhanced Match, F90 Enhanced Match |
| `f90-lifecycle` | F90 Lifecycle, F90 audience |
| `deep-linking-ref-tags` | Deep Linking, Ref Tags, deep links |
| `op1-strategy` | OP1 Strategy, OP1 brainstorm |
| `ai-search-aeo` | AEO, AI Overviews, AI search, zero-click |

---



## Use Case 1: AM-1 Signal Reinforcement (replaces simple dedup)

During AM-1 Slack/Email ingestion:

1. For each new message/email, extract topic keywords.
2. FTS search existing slack_messages: `match_bm25(ts, 'topic keywords')`.
3. If BM25 score > 2.0 against an existing message → this is a reinforcement, not a new signal.
   - UPDATE signal_tracker: strength += 0.5, reinforcement_count += 1, last_seen = now.
   - Still ingest the message to slack_messages (it's new content), but flag it as `signal_type = 'reinforcement'`.
4. If no strong BM25 match → new signal.
   - INSERT into signal_tracker with strength = 1.0.
   - Ingest normally with `signal_type = 'new'`.
5. For email: same logic but without BM25 (keyword match against signal_tracker topics instead).
6. For Asana task comments: extract topic from task name + comment, match against signal_tracker.

**Decay step (run once per AM-1):**
```sql
UPDATE signal_tracker 
SET signal_strength = signal_strength * 0.9,
    last_decayed = current_timestamp
WHERE is_active = true 
  AND last_decayed < current_timestamp - INTERVAL '20 hours';

UPDATE signal_tracker SET is_active = false WHERE signal_strength < 0.1;
```

---



## Use Case 2: Instant Person-Topic Recall

Query pattern for "What did Brandon say about X?":
```sql
SELECT s.source_preview, s.source_channel, s.last_seen, s.signal_strength
FROM signal_tracker s
WHERE s.topic LIKE '%oci%' AND s.source_author = 'Brandon Munday'
ORDER BY s.last_seen DESC LIMIT 10;
```

For deeper Slack-specific search with BM25 ranking:
```sql
SELECT sm.ts, sm.channel_name, sm.text_preview,
       fts_main_slack_messages.match_bm25(sm.ts, 'Brandon OCI budget') AS score
FROM slack_messages sm
WHERE sm.author_name = 'Brandon Munday' AND score IS NOT NULL
ORDER BY score DESC LIMIT 10;
```

**Integration point:** The context-preloader hook can auto-run this when the user mentions a person + topic in their prompt. Pre-load the top 5 signal_tracker results as context.

---



## Use Case 3: WBR Callout Evidence Sourcing

During the callout pipeline analyst step:

1. Extract the callout topic (e.g., "AU CPA trends", "OCI rollout progress").
2. Query signal_tracker for that topic across all channels:
```sql
SELECT source_channel, source_author, source_preview, signal_strength, last_seen
FROM signal_tracker
WHERE topic = 'au-cpa-trends' AND is_active = true
ORDER BY signal_strength DESC LIMIT 10;
```
3. Include top results as "team conversation evidence" in the analyst brief.
4. **Trend detection:** If reinforcement_count > 5 in the last 7 days, flag as "trending topic — team is actively discussing this." This strengthens the callout's relevance.
5. **Cross-channel corroboration:** If the same topic appears in Slack + Email + Asana, it's a stronger signal than Slack-only. channel_spread >= 3 = "confirmed cross-channel trend."

---



## Use Case 4: Wiki Freshness Validation + Idea Sourcing

During the weekly wiki lint (EOD Phase 4):



### Freshness validation
For each published wiki article:
1. Extract the article's primary topic slug.
2. Query signal_tracker: how many recent mentions (last 14 days)?
3. If recent_mentions > 3 AND article.updated > 14 days ago → **stale article with active discussion**. Flag for update.
4. If recent_mentions = 0 AND article.updated > 30 days ago → topic has gone cold. Lower priority for refresh.



### Idea sourcing
Query `signal_wiki_candidates` view:
```sql
SELECT * FROM signal_wiki_candidates;
```
This returns topics with strong signals (strength >= 3.0), multi-channel spread (>= 2 channels), and multiple mentions (>= 3) that don't yet have a wiki article. These are organic wiki article candidates — the team is talking about it enough that it deserves documentation.

Output format for wiki-editor:



### Idea sourcing — Details
```
📚 WIKI SIGNAL CANDIDATES:
- [topic] — strength: [X], mentions: [N], channels: [list], authors: [list], span: [N] days
  → No matching wiki article found. Consider: [suggested article type based on topic]
```

---



## Use Case 5: Meeting Prep Auto-Context

During AM-3 meeting prep:

1. For each upcoming meeting, identify attendees.
2. Query signal_tracker for each attendee's recent topics:
```sql
SELECT topic, SUM(signal_strength) AS strength, COUNT(*) AS mentions, MAX(last_seen) AS latest
FROM signal_tracker
WHERE source_author = 'Brandon Munday' AND last_seen >= current_timestamp - INTERVAL '7 days'
GROUP BY topic ORDER BY strength DESC LIMIT 5;
```
3. Also query for topics that overlap between Richard and the attendee:
```sql
SELECT a.topic, a.signal_strength AS their_strength, b.signal_strength AS richard_strength
FROM signal_tracker a
JOIN signal_tracker b ON a.topic = b.topic
WHERE a.source_author = 'Brandon Munday' AND b.source_author = 'Richard Williams'
  AND a.last_seen >= current_timestamp - INTERVAL '7 days'
ORDER BY (a.signal_strength + b.signal_strength) DESC LIMIT 5;
```
4. Include in meeting prep brief: "Brandon's hot topics this week: [list]. Shared topics: [list]."

---



## Multi-Channel Integration

Each channel serves a different purpose but they all feed the same signal_tracker:

| Channel | What It Captures | Unique Value |
|---------|-----------------|--------------|
| Slack | Real-time discussion, decisions, reactions, @mentions | Speed — signals appear here first. Reactions indicate team agreement. Thread depth indicates importance. |
| Email | Formal requests, approvals, external comms, escalations | Authority — email signals carry more weight (people don't email casually). Cross-team signals often appear here first. |
| Asana | Task creation, status changes, comments, due dates | Commitment — a task being created means someone committed to action. Comments indicate active work. |
| Hedy | Meeting discussions, decisions, action items, speaking patterns | Depth — meeting discussions are richer than Slack messages. Decisions made in meetings often don't appear in other channels. |



### Cross-Channel Signal Weighting
When computing signal_strength for reinforcement:
- Slack mention: +0.5 (high volume, lower signal-to-noise)
- Email mention: +1.0 (lower volume, higher intent)
- Asana task/comment: +0.75 (commitment signal — someone created work)
- Hedy meeting mention: +1.0 (discussion depth, decision context)

These weights are applied during the reinforcement step in Use Case 1.



### Cross-Channel Corroboration
A topic that appears in 3+ channels is qualitatively different from one in 1 channel:
- 1 channel: noise until reinforced
- 2 channels: emerging signal
- 3+ channels: confirmed trend — auto-flag for AM-2 triage priority boost

---



## DuckDB Objects

| Object | Type | Purpose |
|--------|------|---------|
| `signal_tracker` | table | Core signal data — one row per topic × source |
| `signal_heat_map` | view | Aggregate strength by topic across all channels |
| `signal_trending` | view | Topics gaining strength in last 7 days |
| `signal_person_topics` | view | What each person talks about most |
| `signal_wiki_candidates` | view | Strong signals without matching wiki articles |

---



## Integration Points

| Hook/Protocol | How It Uses Signals |
|---------------|-------------------|
| AM-1 (am-auto) | Ingest: create/reinforce signals. Run decay step. |
| AM-2 (am-triage) | Priority boost for tasks matching trending topics. |
| AM-3 (am-auto) | Meeting prep: auto-load attendee topics. Daily brief: include trending signals. |
| Callout pipeline | Analyst step: query evidence for callout topic. |
| Wiki lint (EOD Phase 4) | Freshness validation + idea sourcing from signal_wiki_candidates. |
| Context-preloader | Auto-load signal context when user mentions a person + topic. |
