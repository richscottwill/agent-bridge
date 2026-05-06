---
title: "<Human-readable topic name>"
type: <test | market | initiative | project>
status: <ACTIVE | PAUSED | COMPLETED | ARCHIVED>
owner: Richard Williams
created: YYYY-MM-DD
updated: YYYY-MM-DD
hedy_topic_id: ""                  # optional
aliases:
  - "alias 1"
  - "alias 2"
related:
  topics:
    - topics/markets/mx
    - topics/tests/polaris-brand-lp
  meetings:
    - meetings/brandon-sync
  state_files:
    - state-files/mx-paid-search-state
  wiki_articles:
    - agent-created/strategy/<slug>
  protocols:
    - topics/INGEST-PROTOCOL
---
<!-- DOC-TOPIC-<SLUG> -->

# <Human-readable topic name>

## Summary

<3-5 sentences describing the current state of this topic. Cite the entry dates in the Log that support each claim (e.g. "decision on X per 2026-05-05 entry"). Current posture, nearest gate, biggest unknown. Hand-authored or regenerated weekly by wiki-maintenance. Do not edit on every ingest.>

## Links

Curated set of companion docs and external references. Bidirectional with `related:` frontmatter.

- **State file**: [`<slug>-state.md`](../../state-files/<slug>-state.md) — metrics, flags, forecasts
- **Meeting series**: [`<slug>.md`](../../meetings/<slug>.md)
- **Related topics**: [`topics/markets/<slug>`](../markets/<slug>.md), [`topics/tests/<slug>`](../tests/<slug>.md)
- **Wiki article**: [`<slug>`](../../agent-created/<category>/<slug>.md)
- **Asana**: <GID or URL>
- **Quip**: <URL>
- **Weblab**: <URL>
- **Dashboard**: <path>

## Stakeholders

| Role | Name | Most recent sourced interaction |
|---|---|---|
| Primary owner | <Name> | <meeting or message — date — source ID> |
| Business stakeholder | <Name> | |
| Tech contact | <Name> | |
| Reporting line | <Name> | |

## Metrics

Current metric snapshot, cited from state file or ps.v_weekly. Authoritative source is the state file linked above.

| Metric | Current | WoW | vs OP2 | As of | Source |
|---|---|---|---|---|---|
| Registrations | | | | YYYY-WNN | `ps.v_weekly` |
| Spend | | | | | |
| CPA | | | | | |

## Simplified Timeline

Weekly rollups, newest first. One line per daily entry.

#### 2026-W19 (May 4 – May 10)
- YYYY-MM-DD — <one-line headline referencing source>

#### 2026-W18 (Apr 27 – May 3)
- YYYY-MM-DD — <one-line headline>

## Table of Contents

- [Summary](#summary)
- [Links](#links)
- [Stakeholders](#stakeholders)
- [Metrics](#metrics)
- [Simplified Timeline](#simplified-timeline)
- [Open Items](#open-items)
- [Closed Items — Audit Trail](#closed-items--audit-trail)
- [Running Themes](#running-themes)
- [Log](#log)

## Open Items

Live commitments as stated. Each item carries a source citation.

- [ ] <item as stated> — owner: <Name> — due: <date> — source: <hedy/slack/asana ID>

## Closed Items — Audit Trail

Append-only. Never deleted.

- [x] ~~<item as stated>~~ — closed YYYY-MM-DD — resolution as stated: <one-line, cite source> — log: [`### YYYY-MM-DD — entry`](#YYYY-MM-DD--entry)

## Running Themes

Patterns that cross ≥3 Log entries. Each bullet cites the entry dates it draws from.

- <Pattern> (per 2026-MM-DD, 2026-MM-DD, 2026-MM-DD entries)

## Log

Chronological, newest first. H3 entry, H4 sub-sections. Every entry carries a source. Content reflects what was actually said or happened — interpretation minimized.

### YYYY-MM-DD — <headline stating what happened>

#### Source
hedy:<session_id> | slack:<url> | asana:<gid> | email:<message-id> | wbr:<YYYY-WNN>

Related: [topics/<slug>](../<type>/<slug>.md), [meetings/<slug>](../../meetings/<slug>.md)

#### What was said / what happened
<2-5 sentences of what actually occurred. Direct quotes preferred. Attribute speakers. No interpretation. No synthesis across meetings.>

#### Decisions
- <Decision as stated, with who decided>

#### Actions
- <Owner — action as committed — due date as stated>

#### Notes
<Optional: direct quotes with speaker attribution, data cited, constraints surfaced. Mark quote vs paraphrase where ambiguous.>

---
