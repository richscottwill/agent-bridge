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
[2026-04-17T19:14 session-summary] signal: When an agent is asked to "complete all action items" after proposing them, that phrase is a blanket confirmation covering all reversible in-context work — don't re-ask per-item; execute all and report what happened. Direct application of the newly-documented "act on reversible in-context work" operating norm. | source: this-session | proposed: enrich: agent-architecture
[2026-04-17T19:20 session-summary] signal: SharePoint Artifacts/ layout has two market-scoped folders (markets/ with country subfolders, wiki-sync/ created 4/17 with empty country subfolders) — the split between "canonical wiki article" (long-lived reference) and "market-partitioned sync output" (callouts/state-files/briefs) isn't documented anywhere; needs a folder-taxonomy rule before both grow. | source: this-session | proposed: enrich: 04-kiro-sharepoint-protocol
[2026-04-17T19:25 session-summary] signal: SharePoint has two overlapping layers accumulated by history — Artifacts/wiki-sync/ (sharepoint-sync hook's auto-mirror of ~/shared/wiki/**, populated since 4/12) and Artifacts/{testing,strategy,markets,operations,reporting,research,_meta}/ (older manually-curated article .docx, which is what the dashboard's published/unpublished flag reads); picking one as canonical and deprecating the other is a pending call. | source: this-session | proposed: enrich: 04-kiro-sharepoint-protocol

[2026-04-17T19:50 eod] signal: ABPS AI Content Asana project deprecated 4/17 — wiki articles + SharePoint Artifacts/ are now sole source of truth for published content | source: shared/context/body/soul.md (data-routing table updated) | proposed: enrich: wiki-pipeline-architecture
[2026-04-17T19:50 eod] signal: AI Tool Demo workflow (master prompt + multi-file upload + Markdown output) is a reusable pattern — team committed to SharePoint prompt repo + Gandalf template evaluation | source: hedy:IvUNtHCncikQcZvODFj1 | proposed: ai-tool-wbr-callout-workflow (already drafted today 15:02 — promote from DRAFT)
