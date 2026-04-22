# Follow-On Work — From system-subtraction-audit (2026-04-22)

This audit produced a kill-list and executed ~650 lines of deletions. The bigger-leverage findings are items this audit did NOT cover, flagged here for future spec work.

## High-priority follow-ons

### 1. Broken Reference Cleanup Spec
**Finding**: 300 broken path references detected across the search scope — references pointing to files that don't exist on disk. These are pre-existing bugs, not caused by this audit. Most concentrate in a few degenerate docs (old spec files, historical logs, wiki drafts) that never got updated when real files moved.

**Artifact**: `broken-references-preserved.json` in this archive contains the full list grouped by referrer.

**Scope for follow-on**: Triage the 300 into three buckets — (a) referrer should be deleted, (b) referrer path should be updated, (c) reference is in historical log and safe to leave. Likely 80% are category (c) and the first two combined are <60 live fixes.

### 2. Hook Layer Classifier Bug
**Finding**: The audit's orphan detection failed for hooks because hook files don't path-reference each other — they fire via IDE events (promptSubmit, fileEdited, agentStop). Liveness for hooks is determined by `enabled: true` (or absent) + `when:` trigger validity, not by referrer count.

**Scope for follow-on**: Before the next subtraction audit, fix `classify.py` decision tree to use layer-specialized liveness tests. Hooks: check `enabled` field and `when.type`. Add a "hook fires in practice" test by checking for recent execution evidence (log lines, file changes matching the hook's trigger pattern).

### 3. Coordinated Removal of Body-Metaphor Files
**Finding**: body.md, brain.md, spine.md, amcc.md, body-diagram.md (deleted in this run) are the anatomical navigation layer. body-diagram was safely removed. The other four have 5-6 live load-bearing references each (soul.md auto-include, rw-trainer agent dependency, dashboard pipelines). They can't be single-row deleted without breaking things.

**Scope for follow-on**: Separate coordinated-removal spec per the Mario-Peter dichotomy — transition toward Peter-ethos extension-first architecture where these files become plug-ins (loaded on demand by agents that need them) rather than always-auto-included steering. Migration path:
- Extract soul.md's body-file `#[[file:...]]` references into an agent-specific loader
- Update rw-trainer to read amcc content via direct file read rather than via soul.md chain
- Update dashboards to query DuckDB views (which already exist: `main.hard_thing_now`, `main.l1_streak`, `asana.daily_tracker`) instead of parsing body files
- Then the body files become conditional / manual-inclusion and can be safely shrunk or removed

### 4. Extension-First Refactor (Long-term)
**Finding**: The survivors of this audit are still a monolith. The long-term structural answer (Peter Steinberger's OpenClaw ethos, Mario's pi ethos) is to restructure surviving files as plug-ins loaded on-demand, not always-loaded steering.

**Scope for follow-on**: Major refactor spec. Move toward a minimal steering core + extension API + on-demand loading. Targets:
- Richard-writing-style family (6 files, ~400 lines, all manual-inclusion already) → could be a single extension loaded when any writing task starts
- Guard hooks (guard-asana, guard-calendar, guard-email) → could be a single security extension
- Body organs → extensions loaded per-workflow (callout agent loads memory.md + amcc.md; wiki agent loads memory.md + brain.md; etc.)
- Protocols → pure extension content, never auto-included

This is the target state. Not this spec's job. But it's the work that retires the need for recurring subtraction audits.

## Lower-priority follow-ons

### 5. Duplication Detector Refinement
The heuristic incorrectly flagged eod-backend.md and eod-frontend.md as duplicates (they're two halves of one workflow), and missed state-file-engine.md as a template (stem differed). Before the next audit, refine:
- Filename stem detection to include semantic pairs (backend/frontend, client/server, reader/writer)
- Template detection to also check for filename patterns, not just size-ratio heuristics

### 6. Referrer Source Bucketing
Active-referrer counts were misleading without bucketing by source-directory. 111 of amcc.md's 124 "active" referrers turned out to be in `shared/context/active/` historical logs, not live dependencies. Next audit should bucket referrers by source before computing load-bearing status:
- Live: body, protocols, steering, hooks, agents, tools, scripts
- Historical: active/, intake/, experiments/ (sometimes), dashboards/data/
- Documentation: wiki/, specs/

### 7. Kill-List Review Ergonomics
The generated kill-list was 768 lines. Richard reviewed it section-by-section which worked, but if the next audit finds 100+ DELETE candidates, the linear review will break down. Consider a two-pass review in the next iteration:
- Pass 1: high-confidence orphans (no input needed, auto-approve)
- Pass 2: medium-confidence + UNCLEAR (Richard reviews)

## Artifacts in this archive

- `requirements.md` — 266 lines, 14 requirements, 17 design constraints
- `design.md` — 1042 lines, 5 phases + data model + classification tree + execution semantics
- `tasks.md` — 238 lines, phase-grouped runbook with SCRAPPY/FULL paths
- `kill-list.md` — 768 lines, final review document with Richard's approvals
- `execution.log` — append-only JSON log of what actually got deleted
- `broken-references-preserved.json` — 300 broken refs grouped by referrer, for follow-on #1
- `follow-on.md` — this file

## Total impact

- 9 files deleted (~650 lines, ~4.7% of audited surface)
- 1 file updated (body/changelog.md — deletion note for body-diagram.md)
- 2 git commits: deletion commit + archive commit
- Wiki candidate written for the dreaming/consolidation pipeline

The numeric impact is smaller than the learnings. The real value was surfacing 4 follow-on work items, proving the classifier had layer-specialization gaps, and demonstrating that the Mario-Peter dichotomy lives in every spec tradeoff (rigor vs iteration, waterfall vs scrappy).

Next time we're about to audit again: the extension-first refactor (follow-on #4) should be considered first. If we successfully move to on-demand loading, we won't need another subtraction audit.
