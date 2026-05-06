---
title: "Topic Discovery Queue"
status: ACTIVE
owner: Richard Williams
created: 2026-05-06
updated: 2026-05-06
---
<!-- DOC-TOPICS-DISCOVERY-QUEUE -->

# Topic Discovery Queue

Candidate topics that have surfaced in DuckDB (`signals.signal_tracker`, `main.project_timeline`, `signals.hedy_meetings`) with enough mentions to warrant a dedicated file, but not yet registered in `_registry.md`.

**Promotion bar**: 3+ sourced mentions over 60 days, clearly recurring.

**Discovery cadence**: AM-Backend Phase 2 (daily lightweight check) and wiki-maintenance Stage 5 (weekly full reconciliation).

**Promotion path**: `_discovery-queue.md` → create topic doc + register in `_registry.md` → remove from queue. Items not promoted within 30 days get marked deferred with reason.

## Current Queue

*(Populated by AM-Backend + wiki-maintenance discovery runs. Hand-curation welcome.)*

### 2026-05-06 initial seed from 90-day DuckDB scan

- [ ] `au-cpa-cvr` — 5 signal_tracker mentions — last seen recent — likely belongs under `topics/markets/au.md` as a sub-thread; decide whether standalone
- [ ] `deep-linking-ref-tags` — 2 mentions — cross-cutting; probably an initiative rather than a test
- [ ] `ps-data-gap` — 2 mentions — system-internal; candidate for `kiro-system` subthread rather than standalone
- [ ] `ref-tag-persistence` — 1 mention but strategic — defer
- [ ] `sparkle` — 2 mentions — event-driven, short-lived; log to `topics/markets/mx.md` rather than create dedicated doc

## Deferred (not promoting, with reason)

*(Items that surfaced but don't warrant a topic doc.)*

### 2026-05-06 initial triage

- `kiro-mentoring`, `kiro-demo-prep`, `kiro-weekly-change-aggregation` — system-internal, belongs inside `topics/initiatives/kiro-system.md`
- `netflix`, `riggle`, `gandalf`, `babel-system-oss-marketing` — external references, not recurring work threads
- `ai-workplace-surveillance`, `openai-bedrock`, `ai-tools-marketing` — industry watchlist items; belong in a separate watchlist doc, not topic logs
- `brandon-au-test-meaningless` — one-off reaction, not a topic
- `peter ocampo` — person, not topic; meeting series covers this
- `kate-india-travel`, `kate-offsite-alexis-sync` — schedule items, not topics

## Promotion Rules

1. **3+ mentions threshold** — fewer than 3 and the topic is noise. Exception: Richard can manually promote a single-mention topic when strategic.
2. **60-day window** — mentions older than 60 days don't count toward the threshold. Keeps queue fresh.
3. **No duplicate slugs** — if a candidate matches an alias of an existing registered topic, route to that topic instead.
4. **Clear type** — candidate must fit cleanly into test / market / initiative / project. If unclear, hold in queue with a note.
5. **Strategic override** — Richard can promote or defer anything; rules are defaults.
