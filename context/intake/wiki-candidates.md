# Wiki Candidates Queue

Append-only log of wiki article candidates and enrichment opportunities observed by hooks during their normal runs. Hooks observe — they do not analyze, classify, or draft. The wiki-editor consumes this file during the weekly `wiki-maintenance` manual hook run and proposes action.

## Format

One line per candidate. Loose format — hooks don't judge quality or priority. That's the editor's job.

```
[YYYY-MM-DDTHH:MM hook-name] signal: <one-line observation> | source: <where it came from> | proposed: <article slug or "enrich: existing-slug">
```

## Rules for contributing hooks

- One line per candidate. Do not expand.
- Timestamp in PT (use `TZ=America/Los_Angeles date +%Y-%m-%dT%H:%M`).
- Hook name = your hook's short name (am-auto, eod, session-summary, wbr-callouts).
- `signal:` — what you observed in one sentence.
- `source:` — DuckDB table, file path, Slack thread ID, meeting session ID.
- `proposed:` — either a new article slug OR `enrich: <existing-slug>` if the signal updates an existing doc.
- If unsure whether something is wiki-worthy, err on the side of appending. Noise is cheaper than misses.
- Do not deduplicate against existing entries. The consumer handles dedup.

## Rules for consuming hook (wiki-maintenance)

- Read this file during the manual wiki-maintenance run.
- Dedupe by signal text similarity + proposed slug.
- Group related signals (multiple hooks flagged the same topic = stronger signal).
- Propose top 3-5 items to `_meta/review-queue.md` for Richard's review.
- Archive processed entries by moving them to `archive/wiki-candidates-YYYY-WNN.md`.
- Do not draft articles from this file. Only propose.

## Kill condition

**2026-06-01.** If this queue accumulates >100 unprocessed entries AND wiki-editor hasn't promoted any to review-queue.md, the contribution pattern is noise — delete the file, revert the hook contributions, and go back to manual article creation. Keep-or-kill on 6/1.

---

## Candidates


<!-- Hooks append below this line -->
<!-- Last archive: 2026-W16 second pass (2026-04-17 19:00 PT). Prior entries moved to archive/wiki-candidates-2026-W16.md. -->
<!-- Last archive: 2026-W18 (2026-05-01). 362 entries moved to archive/wiki-candidates-2026-W18.md. -->
[2026-05-02T03:40 session-summary] signal: Agent-level consent checking — when one agent hands off scope that conflicts with a prior directive from the principal (Richard), implicit "approved by me" layering is insufficient for high-regression-risk actions; the receiving agent should decline and ask for explicit override rather than aggregate authority upward. | source: this-session | proposed: enrich: inter-agent-directive-pattern
