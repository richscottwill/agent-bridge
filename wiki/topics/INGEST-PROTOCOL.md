---
title: "Topic Log Ingest Protocol"
type: protocol
status: ACTIVE
owner: Richard Williams
created: 2026-05-06
updated: 2026-05-06
---
<!-- DOC-PROTO-TOPIC-LOG-INGEST -->

# Topic Log Ingest Protocol

How hooks and agents write to topic-log markdown files under `~/shared/wiki/topics/`.

## Core principle — sourcing bar

**Topic logs are objective source files. Only capture things that were actually said and that can point to the exact meeting, message, ticket, or artifact where it happened.**

Every Log entry must carry a verifiable `Source` line (hedy session ID, slack URL, email message ID, asana GID, WBR week, or quip doc URL). If no source exists, the entry does not belong in the Log.

Interpretation is minimized:
- Direct quotes preferred over paraphrase
- Decisions phrased as what was decided, not why
- Actions stated as the owner committed to them, with due dates as stated
- Running Themes and Summary may synthesize across entries — but must name which entries they draw from
- Do NOT infer intent, motivation, or feelings from a session unless the speaker stated them

A topic log entry should be defensible in a 1:1 with the stakeholder named. "I said this on May 5 per hedy:<id>" must hold up.

## When to invoke

Every time an agent or hook observes substantive new signal on an existing or new topic:

- Hedy session ingest (EOD Phase 1, AM-Backend Phase 1)
- Slack thread with a decision, owner, or date
- Email with a commitment or stakeholder change
- Asana task status change worth narrative context
- WBR callout with a decision or flagged signal
- Any manual session where Richard directs "log this to [topic]"

Substantive bar: if the entry wouldn't hold up as "something that actually happened with a specific attribution," don't write it.

## Topic identification

Order of precedence to route a signal to the right doc(s):

1. **Hedy topic ID match** — if the signal is a Hedy session and `hedy_topic_id` matches a frontmatter value in any topic doc, route there.
2. **Slug match on aliases + title** — keyword match against the slug, title, and `aliases:` list of every topic doc.
3. **DuckDB signal-tracker cross-check** — if the signal maps to a `signals.signal_tracker.topic` value that already has a registered topic doc (see `topics/_registry.md`), route there.
4. **Related slug match** — if primary topic has `related:` pointing to other docs and the signal text mentions those slugs, cross-post.
5. **No match** — create a new doc only if the signal clearly represents a new recurring topic (see topic discovery below). Otherwise log to session-log.md.

Multi-topic posts: the same signal can be written to multiple docs. Do it — duplication is the right answer when a signal spans topics.

## Topic discovery (hook-run)

AM-Backend and wiki-maintenance hooks run a topic-discovery pass that reconciles `signals.signal_tracker`, `main.project_timeline`, and `signals.hedy_meetings` against the topic registry.

Discovery query (run by AM-Backend Phase 2 and wiki-maintenance Stage 5):

```sql
WITH registered AS (
  SELECT slug FROM <topics-registry manifest>  -- parsed from topics/_registry.md
), candidates AS (
  SELECT LOWER(topic) AS slug, COUNT(*) AS mentions, MAX(last_seen) AS last_seen
  FROM signals.signal_tracker
  WHERE is_active AND LOWER(topic) NOT IN (SELECT slug FROM registered)
  GROUP BY 1 HAVING COUNT(*) >= 3
  UNION ALL
  SELECT LOWER(project_name) AS slug, COUNT(*) AS mentions, MAX(event_date) AS last_seen
  FROM main.project_timeline
  WHERE event_date > CURRENT_DATE - INTERVAL '60 days'
    AND LOWER(project_name) NOT IN (SELECT slug FROM registered)
  GROUP BY 1 HAVING COUNT(*) >= 3
)
SELECT slug, SUM(mentions) AS total_mentions, MAX(last_seen) AS last_seen
FROM candidates GROUP BY slug ORDER BY total_mentions DESC LIMIT 20;
```

For each candidate with ≥3 mentions, append one line to `~/shared/wiki/topics/_discovery-queue.md` with format:

```
- [ ] <slug> — <mention count> mentions — last seen <date> — sources: <channels>
```

Richard or a subsequent hook run promotes queue items to real topic docs (see Creating a new topic). Queue items not promoted within 30 days are demoted with reason.

## Cross-reference discovery (required on every write)

Every topic doc carries structured cross-references. Agents maintain them on every ingest and every edit.

### On doc creation

When creating a new topic doc, populate the `related:` frontmatter by scanning:

1. **Existing topic docs**: for each other file under `~/shared/wiki/topics/`, check if the new doc's slug/aliases appear in that file's title, aliases, or Log entries. If yes, add to new doc's `related.topics`, AND add new doc's slug to the other file's `related.topics` (bidirectional).
2. **State files**: check `~/shared/wiki/state-files/*-state.md`. If any state file's content discusses the new topic's slug or aliases, add to `related.state_files`.
3. **Meeting series**: check `~/shared/wiki/meetings/*.md`. If any meeting series discusses the new topic, add to `related.meetings`.
4. **Agent-created wiki articles**: grep `~/shared/wiki/agent-created/**/*.md` for slug/alias mentions. If any, add to `related.wiki_articles`.
5. **Protocols**: only add `related.protocols` when the doc directly describes how to operate a system component.

### On ingest (adding a new Log entry)

Each new Log entry should include a `Related:` line under `#### Source` citing any other topic docs, state files, meetings, or wiki articles that the entry references or that would benefit from cross-linking. Inline markdown links preferred over bare paths.

If an entry establishes a new recurring connection (e.g., a meeting repeatedly discusses a test), promote the connection: add the other doc to the frontmatter `related:` list on both sides.

### Reciprocity rule

Cross-references are bidirectional. If `topics/tests/polaris-brand-lp.md` lists `topics/markets/mx.md` under `related.topics`, then `topics/markets/mx.md` must list `topics/tests/polaris-brand-lp.md` under `related.topics`. wiki-maintenance's weekly audit flags reciprocity gaps.

### When NOT to cross-reference

- Don't add a reference just because a word overlaps
- Don't add references to archived or deprecated docs unless historically necessary
- Don't force a cross-link if the relationship is one-way (a wiki article may reference the topic doc without the topic doc backlinking every article)

## Append contract

For each topic doc the signal touches:

1. Read current file.
2. Verify source exists (hedy session, slack URL, email msg-id, asana GID). If not, do not write the Log entry.
3. Identify cross-references this entry introduces.
4. Under `## Log`, prepend a new entry. Format:

```markdown
### YYYY-MM-DD — <one-line headline — a statement of what happened, not an interpretation>

#### Source
hedy:<session_id> | slack:<url> | asana:<gid> | email:<message-id> | wbr:<YYYY-WNN>

Related: [topics/<slug>](<path>), [meetings/<slug>](<path>), [state-files/<slug>](<path>)

#### What was said / what happened
<2-5 sentences of exactly what was said or what occurred. Use direct quotes where possible. Attribute named speakers. No interpretation, no synthesis across meetings. Cross-reference inline where a specific doc is relevant.>

#### Decisions
- <Decision as stated, with who decided — no rationale unless the rationale was stated>

#### Actions
- <Owner — action text as committed — due date as stated>

#### Notes
<Optional: direct quotes, data points cited, constraints surfaced. Label as quote vs. paraphrase where uncertain.>

---
```

5. Under `## Simplified Timeline`, prepend one line under the current `#### YYYY-WNN (Mon D – Sun D)` week header, OR create a new week header if this is the first entry of the week. One line per entry, format: `- YYYY-MM-DD — <one-line headline>`.
6. If the entry opens a new commitment or open question, add an item to `## Open Items`.
7. If the entry resolves an open item, move that item to `## Closed Items — Audit Trail` with format `- [x] ~~<item text>~~ — closed YYYY-MM-DD — resolution: <one-line resolution citing the log entry> — log: [link to entry]`. Never delete closed items.
8. If the entry introduces a new cross-reference not yet in `related:`, update frontmatter and apply the reciprocity rule to the target doc.
9. Update `updated:` frontmatter field to today (PT).
10. Do NOT touch `## Summary`, `## Running Themes`, or the Table of Contents on a per-ingest basis. Those are refreshed by the Summary Refresh cadence below.

## Heading level discipline

Required for SharePoint .docx conversion fidelity (Heading 1/2/3 mapping in Word navigation pane).

| Markdown | Word | Use |
|---|---|---|
| `#` | Title | File title only, one per file |
| `##` | Heading 1 | Top-level sections |
| `###` | Heading 2 | Log entries — one per post |
| `####` | Heading 3 | Entry sub-sections (Source, What was said, Decisions, Actions, Notes) AND weekly headers inside Simplified Timeline |

Never use `#####` or deeper in a topic doc. If an entry needs that structure, split it into multiple entries or move content to a linked artifact.

## Summary Refresh cadence

`## Summary` and `## Running Themes` refresh on the longer cadence. Three triggers:

1. **Weekly, by wiki-maintenance.kiro.hook** — for every topic doc where `updated:` moved since last Monday, regenerate Summary from the last 5 Log entries. Running Themes updated if a pattern has emerged across 3+ entries, each citing the entry date it draws from.
2. **Daily, by am-backend.kiro.hook Phase 2** — after ingesting today's signals, if a topic doc accumulated ≥3 new entries since the last Summary refresh, force a refresh.
3. **On-demand by sharepoint-durability-sync.kiro.hook** — when a doc's Summary-refresh debt is ≥3, force a refresh before the SharePoint mirror push.

Summary rewrite rule: keep to 3-5 sentences. Describe current state, nearest gate or decision, biggest unknown. Synthesize from Log entries, cite the entry dates that support each claim.

## Open Items discipline

- Add item when a decision or action opens without resolution in the same entry
- Move item to `## Closed Items — Audit Trail` when a later Log entry resolves it (write the resolution into that entry's Context, link back to the original open from the closed entry)
- Never delete closed items — the audit trail is the point
- If an item has been open for 21+ days without a Log entry touching it, flag in the next Summary refresh as "stale open item"

## Coexistence with state files

Topic docs do NOT replace state files. Two artifacts, different roles:

| Artifact | Role | Update cadence | Consumers |
|---|---|---|---|
| `state-files/<slug>-state.md` | Amazon continuous-prose narrative, metrics tables, WBR-patched forecasts, flags, appendices | AM daily + WBR Monday + EOD | dashboards, MBR/QBR prep, refresh-goals.py |
| `topics/<type>/<slug>.md` | Chronological sourced context log, decisions, actions, cross-topic threading | On-signal append, Summary weekly | 1:1 prep, retrospectives, "where does this stand" questions |

Every topic doc with a matching state file lists it in `related.state_files`, and every state file gets a corresponding topic doc listed in its narrative. State files remain the authoritative metric/forecast artifact; topic docs are the authoritative sourced context/decision/action artifact.

## Slug discipline

Slugs must be kebab-case, stable, and match the filename (without `.md`). Slugs align across:
- `topics/<type>/<slug>.md`
- DuckDB `signals.signal_tracker.topic` (lowercased)
- DuckDB `main.project_timeline.project_name` (lowercased)
- `state-files/<slug>-state.md` (where applicable)

A slug change requires a rename + grep-update across all `related:` fields + historical session-log references + signal_tracker normalization.

## Creating a new topic

Trigger: a candidate surfaces from `_discovery-queue.md` (3+ mentions, not yet registered), OR Richard directs creation manually, OR the first signal that doesn't match any existing topic but clearly names a recurring thread.

1. Copy `~/shared/wiki/topics/TEMPLATE.md` to `~/shared/wiki/topics/<type>/<slug>.md`
2. Fill frontmatter (title, type, status ACTIVE, owner, created=today, updated=today, aliases)
3. Run the cross-reference discovery (§Cross-reference discovery → On doc creation) to populate `related:` and add reciprocal backlinks
4. Register the slug in `~/shared/wiki/topics/_registry.md` with type + canonical slug + aliases
5. Write the first Summary as one factual sentence citing a source — will be refreshed next Monday
6. Log the first entry with full source attribution
7. Append one line to `~/shared/context/intake/wiki-candidates.md` so wiki-maintenance picks it up for indexing
8. Remove the candidate from `_discovery-queue.md` if applicable

## SharePoint mirror

`sharepoint-durability-sync.kiro.hook` converts each topic doc to .docx and mirrors to `Documents/Kiro-Drive/topic-logs/<type>/<slug>.docx`. Heading levels preserve. Frontmatter is converted to a metadata table at the top of the .docx. Cross-references remain as hyperlinks where possible.

## Deprecating a topic

When status flips to COMPLETED or ARCHIVED:

- Final Log entry summarizes outcome with source attribution and links to what supersedes it (if anything)
- Summary rewritten in past tense
- Frontmatter `status:` updated
- Doc remains in place (no moves); wiki-index.md marks it archived
- `related:` references from other docs remain (history matters)
- Registry entry in `_registry.md` updated to reflect ARCHIVED state

## Anti-patterns to avoid

- Writing a Log entry without a verifiable source — violates core principle
- Paraphrasing when a direct quote is available
- Inferring intent, motivation, or feelings not explicitly stated
- Writing a Log entry that duplicates the exact text of an ingested Hedy recap — synthesize minimally, but keep attribution exact
- Adding `#####` depth instead of splitting entries
- Updating `## Summary` on every ingest
- Creating a new topic doc for every one-off project mention — only create when the thread is clearly recurring with ≥3 sourced mentions
- Deleting Log entries or Closed Items
- One-way cross-references
- Adding a cross-reference on weak keyword overlap
