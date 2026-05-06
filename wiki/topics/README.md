---
title: "Topic Logs — System Overview"
status: ACTIVE
audience: amazon-internal
owner: Richard Williams
created: 2026-05-06
updated: 2026-05-06
---
<!-- DOC-TOPICS-README -->

# Topic Logs

Per-topic sourced context files for every **test**, **market**, **initiative**, and **project** that recurs in Richard's work. They complement (do not replace) state files, meeting series files, and wiki articles. Markdown is source of truth; DuckDB is a rebuildable analytical view; SharePoint is a .docx mirror.

## Core principle

Topic logs are **objective source files**. Every Log entry cites a verifiable source — hedy session ID, slack URL, email message ID, asana GID, WBR week, or quip URL. Direct quotes preferred over paraphrase. No interpretation beyond what was said. The doc should hold up as "I said this on this date per this source" in front of the stakeholder named.

Interpretive synthesis lives in `## Summary` and `## Running Themes`, and even there must cite the entry dates it draws from.

## Folder structure

```
~/shared/wiki/topics/
├── README.md                      # this file
├── TEMPLATE.md                    # canonical schema
├── INGEST-PROTOCOL.md             # how hooks/agents write to these files
├── _registry.md                   # canonical list of registered topics (machine-readable by hooks)
├── _discovery-queue.md            # candidates surfaced from DuckDB, not yet promoted
├── tests/                         # one file per test
├── markets/                       # one file per market
├── initiatives/                   # one file per long-running program
└── projects/                      # one file per bounded project with deadline
```

## Artifact map

| Artifact | Role | Shape | Authoritative for | Location |
|---|---|---|---|---|
| Topic log | Chronological sourced context, decisions, actions, cross-topic threading | Newest-first posts with Summary / Links / Stakeholders / Metrics / Timeline / Open+Closed Items / Themes / Log | "Where does this stand, what was said, when" | `~/shared/wiki/topics/<type>/<slug>.md` |
| State file | Amazon continuous-prose narrative, metrics tables, WBR-patched forecasts, flags | Amazon 1-2 page format with marker blocks | MBR/QBR narrative, dashboards, refresh-goals.py | `~/shared/wiki/state-files/<slug>-state.md` |
| Meeting series | Recurring-meeting session log | Per-session summaries, running themes | "What did we discuss last time" for recurring meetings | `~/shared/wiki/meetings/<slug>.md` |
| Wiki article | Durable how-to / framework / reference | Structured article per wiki-pipeline-rules.md | Documented pattern, methodology | `~/shared/wiki/agent-created/<category>/<slug>.md` |

Topic logs cross-reference all three others via structured frontmatter and inline links.

## File schema

Every topic file follows `TEMPLATE.md`. Required sections:

1. **Frontmatter** — title, type, status, owner, hedy_topic_id, aliases, structured `related:` (topics / meetings / state_files / wiki_articles / protocols)
2. **Summary** — 3-5 sentences citing the Log entry dates that support each claim
3. **Links** — curated companion docs (merges what was previously "Key Links" + "See also")
4. **Stakeholders** — role + name + most-recent sourced interaction
5. **Metrics** — small snapshot; authoritative source is the state file
6. **Simplified Timeline** — weekly rollups (H4 `#### YYYY-WNN (Mon D – Sun D)`), newest first, one line per daily entry
7. **Table of Contents** — static markdown anchor list
8. **Open Items** — each with owner, due date, source citation
9. **Closed Items — Audit Trail** — append-only, never deleted, each with resolution + source
10. **Running Themes** — 2-4 patterns, each citing ≥3 entry dates
11. **Log** — chronological, newest first. H3 entries, H4 sub-sections (Source, What was said / what happened, Decisions, Actions, Notes). Every entry carries a Source line and a Related: line.

## Heading conventions (SharePoint-critical)

| Markdown | Word heading | Use |
|---|---|---|
| `#` | Title | File title only |
| `##` | Heading 1 | Top-level sections |
| `###` | Heading 2 | Log entries — `### YYYY-MM-DD — headline` |
| `####` | Heading 3 | Entry sub-sections AND weekly headers in Simplified Timeline |

Never `#####` or deeper.

## Ingest protocol

See [`INGEST-PROTOCOL.md`](./INGEST-PROTOCOL.md) for the full contract. Key rules:

- Every Log entry must have a verifiable source — no source, no entry
- Direct quotes preferred; interpretation minimized
- Bidirectional cross-references — reciprocity audited by wiki-maintenance weekly
- `## Summary` and `## Running Themes` refresh weekly by wiki-maintenance, daily by AM-Backend when ≥3 new entries accumulate
- Open Items → Closed Items via move, never delete
- Slugs align across `topics/`, `state-files/`, `signals.signal_tracker.topic`, `main.project_timeline.project_name`

## Registry + discovery

- **`_registry.md`** — canonical list of every registered topic (ACTIVE / PLANNED / PAUSED / COMPLETED / ARCHIVED). Hooks read this to route signals.
- **`_discovery-queue.md`** — candidates surfaced from DuckDB (≥3 mentions, not yet registered). AM-Backend daily + wiki-maintenance weekly reconcile new candidates into the queue.

## Hook integration

Three hooks write to topic logs:

| Hook | Phase | What it does |
|---|---|---|
| `am-backend.kiro.hook` | Phase 1 (meeting ingest) | Routes today's hedy sessions + slack/email signals to matching topic docs; appends Log entries with sources; updates Simplified Timeline |
| `am-backend.kiro.hook` | Phase 2 (discovery + summary) | Reconciles `signals.signal_tracker` against `_registry.md`; appends new candidates to `_discovery-queue.md`; refreshes Summary/Running Themes on docs with ≥3 new entries |
| `wiki-maintenance.kiro.hook` | Stage 1 (enrichment) | Weekly Summary/Running Themes regeneration across all ACTIVE topic docs |
| `wiki-maintenance.kiro.hook` | Stage 5 (reconciliation) | Audits reciprocity of `related:` cross-references; promotes queue items to docs where appropriate; flags stale open items |
| `sharepoint-durability-sync.kiro.hook` | — | Mirrors .md to .docx at `Documents/Kiro-Drive/topic-logs/<type>/<slug>.docx` |

## SharePoint mirror

Canonical mirror: `Documents/Kiro-Drive/topic-logs/<type>/<slug>.docx`. Heading levels preserve. Frontmatter converts to metadata table. Inline cross-references render as hyperlinks where possible.

## What this does NOT replace

- **State files** — still authoritative for metrics, forecasts, anomaly flags. Dashboards (refresh-goals.py, state-files/*.html), WBR callouts, MBR/QBR surfaces all read state files.
- **Meeting series** — still authoritative per-recurring-meeting log.
- **Wiki articles** — still authoritative for patterns, frameworks, references.

`main.meeting_series` and `main.meeting_analytics` DuckDB tables become rebuildable derived views; they are no longer sources of truth.

## Slugs

Kebab-case, stable. Match across `topics/<type>/<slug>.md`, `signals.signal_tracker.topic` (lowercased), `main.project_timeline.project_name` (lowercased), and `state-files/<slug>-state.md` where applicable. Slug change = rename + grep update across all `related:` fields + historical references.
