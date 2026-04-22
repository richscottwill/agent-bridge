# Implementation Plan: System Subtraction Audit

Each task is a discrete unit of work executable in a single session. Tasks are grouped by audit phase. Dependencies are explicit.

**Two execution paths** (per design Phase 0):
- **SCRAPPY-PASS** (Peter-ethos): Tasks 1 → 2 → 3 → 5.1 → Richard reviews → tasks.md revisited with learnings. No execution. ~30-60 min one session.
- **FULL-PASS** (Mario-ethos): All tasks 1 → 7. Two sessions (generating + executing). ~2-3 hrs agent time + Richard review time.

Default: ask Richard which path before starting. When in doubt, SCRAPPY-PASS first — the first-run data will inform whether FULL-PASS is needed.

---

## Phase 0 — Pre-Flight

- [ ] **0.1 Confirm pass mode and lockout check**
  - Ask Richard: FULL-PASS or SCRAPPY-PASS? Default SCRAPPY if first run.
  - Check for `.kiro/specs/system-subtraction-audit/kill-list.md`. If present AND no `execution.log` with `run_completed` → abort with clear message.
  - Read `~/.kiro/steering/soul.md`, compute sha256, snapshot karpathy-protected file list in `preflight.json`.
  - Write `preflight.json` with `pass_mode`, `soul_hash`, `karpathy_files[]`, `started_at`.
  - _Requirements: R5, R7, R14.3_

## Phase 1 — Inventory

- [ ] **1.1 Enumerate target files**
  - List every file in `~/shared/context/body/`, `~/shared/context/protocols/`, `~/.kiro/hooks/`, `~/.kiro/steering/`.
  - Collect per file: absolute path, rel_path (with `~`), layer, line count (`wc -l`), last_modified (`stat -c %y`).
  - Follow symlinks at depth 1 max. Record in `symlinks_followed[]`.
  - _Requirements: R1.1_

- [ ] **1.2 Extract purpose lines with layer-aware rules**
  - SCRAPPY-PASS: skip this task; set purpose_line to first heading verbatim.
  - FULL-PASS: per design data-model section — body/protocol take first H1 then first paragraph; hooks pull JSON `description`→`name`; steering pulls frontmatter `description` then first H1.
  - Flag `purpose_missing: true` if nothing extractable or matches `/TODO|Placeholder|FIXME/i`.
  - _Requirements: R1.2, R12.3_

- [ ] **1.3 Parse steering frontmatter and hook enabled state**
  - For each steering file: parse frontmatter, normalize `inclusion_mode` to `"auto"` (always/auto/absent) or `"conditional"` (manual/fileMatch) or null+`needs_revisit` for unknown values. Preserve raw.
  - For each hook: parse JSON, record `is_enabled` boolean.
  - _Requirements: R13_

- [ ] **1.4 Detect empty shells and auto-generated candidates**
  - SCRAPPY-PASS: only empty-shell (line count < 10 non-frontmatter).
  - FULL-PASS: also run `git log --oneline --since="30 days ago"` per file; flag `auto_generated_candidate: true` if ≥5 commits with non-interactive patterns.
  - _Requirements: R12.1, Design open question #4_

- [ ] **1.5 Add prior-session context notes**
  - SCRAPPY-PASS: skip.
  - FULL-PASS: grep `~/shared/context/intake/session-log.md` for each filename; pull `git log --pretty=format:'%as: %s' --since="90 days ago"` per file. Store 1-line notes in `prior_session_notes[]`.
  - _Requirements: R11.4_

- [ ] **1.6 Compute totals and write inventory.json**
  - Per-layer file count + line count, grand total.
  - Write `inventory.json` per design data model.
  - _Requirements: R1.3, R1.4_

## Phase 2 — Referrer Graph + Broken Refs

- [ ] **2.1 Build search patterns and run grep across scoped corpus**
  - Scope: `~/.kiro/**`, `~/shared/context/**`, `~/shared/wiki/**`, `~/shared/tools/**`, `~/shared/scripts/**`, `~/shared/dashboards/**`.
  - For each inventory file: grep for rel_path, absolute path, and `#[[file:...]]` form.
  - SCRAPPY-PASS: rel_path only (skip absolute path and include-form variants — accept some missed refs for speed).
  - _Requirements: R2.1, R2.8_

- [ ] **2.2 Classify each hit into match type**
  - Referring file in `~/shared/wiki/**` or `.kiro/specs/**` or matches `README.md|CHANGELOG.md|*-docs.md|*-guide.md` → `documentation`.
  - Referring file is disabled hook or conditional steering → `latent`.
  - Active referrer with path → `path`.
  - Bare filename in prose → `name`.
  - Record edges with line number and context excerpt.
  - _Requirements: R2.2, R2.3_

- [ ] **2.3 Resolve references, capture broken refs**
  - For every `path` or `latent` edge, check target exists on disk.
  - Missing target → append to `broken_refs.json` grouped by referrer, with line number, context, suggested action (remove / update to correct path / create target).
  - _Requirements: R2.9, R8_

- [ ] **2.4 Detect circular-orphan clusters**
  - SCRAPPY-PASS: skip.
  - FULL-PASS: build directed graph of active path edges among inventory files; run Tarjan's SCC; SCCs of size ≥2 with zero external active referrers become `circular_cluster` entries with `is_cluster_orphan: true`.
  - _Requirements: R2.6_

- [ ] **2.5 Aggregate by_target and write graph**
  - Per file: count active/latent/documentation/name referrers; flag is_orphan, is_load_bearing (3+ active), cluster membership.
  - Write `referrers.json` and `broken_refs.json`.
  - _Requirements: R2.4, R2.5, R2.7_

## Phase 3 — Duplication Detection

- [ ] **3.1 Group by filename stem and detect template+instances**
  - Strip variant suffixes (`-v2`, `-new`, `-parallel`, `-old`, `-draft`) to get stem; groups of 2+ → candidates.
  - For each candidate group: if largest member is ≥2x median AND at least one smaller member has a path reference to largest → `template_plus_instances`. Template is SCAFFOLDING (KEEP). Instances evaluated individually. Do NOT collapse.
  - _Requirements: R3.1, R3.3_

- [ ] **3.2 Detect heading-overlap groups and designate survivors**
  - SCRAPPY-PASS: skip heading overlap; stem_variant only.
  - FULL-PASS: extract H1/H2 from first 100 lines of each non-template file; pairs with >50% overlap form `heading_overlap` groups.
  - For `stem_variant` and `heading_overlap` (but NOT `template_plus_instances`): designate survivor as most recently modified AND most active referrers (weighted equally, break ties by line count).
  - _Requirements: R3.2, R3.4, R3.5_

- [ ] **3.3 Resolve multi-group membership and write duplication_groups.json**
  - Files in 2+ groups → assign to group with largest aggregate-lines-of-losers. Re-evaluate affected groups; dissolve any that fall below threshold.
  - Write `duplication_groups.json`.
  - _Requirements: R3.6_

## Phase 4 — Classification

- [ ] **4.1 Walk classification decision tree per file**
  - For each inventory file, execute steps 1-8 of design's top-level decision tree, then the appropriate layer sub-tree.
  - Record terminating action + category + confidence + all required evidence fields.
  - Files missing required fields get `needs_revisit: true`.
  - _Requirements: R5, R6, R13, Design classification-decision-tree section_

- [ ] **4.2 Body-layer specific: apply both workflow tests and record both results**
  - For every body organ, record current_usage_test result AND future_workflow_test result even if first passes.
  - SCAFFOLDING KEEPs must name a specific L3-L5 workflow; otherwise downgrade to METAPHOR-ONLY DELETE.
  - Check R5.6 trigger: if auto-included steering path-references this organ, override to UNCLEAR with default KEEP and coordinated-removal note.
  - _Requirements: R5.4, R5.5, R5.6_

- [ ] **4.3 Generate UNCLEAR defaults and row IDs**
  - Every UNCLEAR row: specify `default_if_unanswered` (DELETE or KEEP) with time horizon (30 days default). No UNCLEAR without default — if no meaningful default exists, reclassify as DELETE or KEEP with LOW confidence.
  - Assign row IDs: sort by (layer, action) and apply `{L}-{A}{N}` format (B/P/H/S × D/M/U/K/X × 1-indexed).
  - _Requirements: R10, R4.9_

- [ ] **4.4 Flag karpathy-protected files, compute summary counts, write classified.json**
  - Karpathy files: no action, observation only (referrer count, lines, last-modified).
  - Compute per-layer and overall summary counts.
  - Hash the classified.json content for kill-list header reference.
  - _Requirements: R7, R4.6, Design data-model section_

## Phase 5 — Render

- [ ] **5.1 Write kill-list.md (SCRAPPY-PASS stops here)**
  - Header: generation timestamp, classified.json hash, unsearched-sources disclosure per R2.10.
  - Summary: per-layer table + aggregate + estimated-lines-removed-if-all-approved.
  - Bulk Approval Block (fenced code block with APPROVE/VETO/DEFER lines per design Kill-List Review Syntax).
  - Incomplete classifications section (any `needs_revisit: true`).
  - Broken references section (grouped by referrer).
  - Per-layer chunks: DELETE → MERGE → UNCLEAR → KEEP, priority-sorted within action.
  - Karpathy review section (observations, no recommendations).
  - Duplication groups summary table.
  - _Requirements: R4, R11_

- [ ] **5.2 (SCRAPPY-PASS) Report findings and stop**
  - Present summary to Richard.
  - Ask: promote to FULL-PASS for execution, or stop and revise this spec first?
  - Do NOT delete intermediate JSONs yet — they feed the next run.

## Phase 6 — Execution (FULL-PASS only, separate session after Richard reviews)

- [ ] **6.1 Parse bulk-approval block and build approved-set**
  - Read kill-list.md, locate bulk-approval block by fenced-code-block marker under `## Bulk Approval Block`.
  - Parse APPROVE/VETO/DEFER lines. Expand ranges. Apply precedence: DEFER > VETO > APPROVE.
  - Also scan row headers for inline APPROVED tags.
  - Absence of veto is NOT approval.
  - _Requirements: R9.1_

- [ ] **6.2 Verify state freshness and hash match**
  - Check classified.json hash matches kill-list header.
  - Re-read current filesystem state; compare to inventory.json. If any approved row's target has changed since kill-list generation → skip that row, log with reason.
  - _Requirements: R9.5_

- [ ] **6.3 Topologically sort approved DELETE set by referrer dependency**
  - Build directed graph of active path refs among approved DELETE rows.
  - Kahn's algorithm: leaves first, load-bearing last.
  - Load-bearing DELETE with any unresolved UNCLEAR/un-approved referrer → skip, log as "blocked on referrer resolution."
  - _Requirements: R9.2, R9.3_

- [ ] **6.4 Execute row-by-row with append-only log**
  - Emit `run_started` with kill-list and classified hashes.
  - Per row: `row_started` → action (DELETE / MERGE / referrer-update) → `row_completed` or `row_skipped` or `row_stopped`.
  - MERGE: atomic sequence per design Execution Semantics section. On conflict between source and target sections, STOP that row.
  - Referrer updates paired with load-bearing DELETEs happen in the same session, before the DELETE.
  - Apply broken-reference fixes unless Richard vetoed them.
  - On interruption: emit `run_interrupted`. On resume: read log, build skip-set, continue. Hash mismatch on resume → STOP.
  - _Requirements: R9.4, R9.5, R9.6, R9.7_

- [ ] **6.5 Emit run_completed with totals**
  - completed_count, skipped_count, stopped_count, broken_refs_fixed.
  - Git commit all changes with message including audit date and summary.

## Phase 7 — Archive

- [ ] **7.1 Delete intermediate JSONs**
  - Remove `preflight.json`, `inventory.json`, `referrers.json`, `broken_refs.json`, `duplication_groups.json`, `classified.json`.
  - _Requirements: R14.1_

- [ ] **7.2 Append audit learning to wiki-candidates.md**
  - One-line entry per design open question #6: `[YYYY-MM-DDTHH:MM audit-complete] signal: <biggest finding> | source: system-subtraction-audit | proposed: <slug>`.
  - Example: `x% surface reduction, N metaphor-only deleted, N scaffolding preserved for L3-L5`.
  - _Requirements: R14 + design open question #6_

- [ ] **7.3 Archive spec directory**
  - Move `.kiro/specs/system-subtraction-audit/` → `~/shared/wiki/agent-created/archive/system-subtraction-audit-{YYYY-MM-DD}/`.
  - Archive contains: requirements.md, design.md, tasks.md, kill-list.md, execution.log.
  - Git commit the move with message `audit: system-subtraction-audit completed {date}`.
  - _Requirements: R14.2, R14.4_

- [ ] **7.4 Add follow-on recommendation to archive**
  - Append a single file `follow-on.md` to the archive listing the named follow-on spec from design open question #7: "restructure surviving files as extension-loaded modules per pi / OpenClaw architecture pattern."
  - This is the Peter-ethos target state — not a task for this audit, just a breadcrumb for when the user returns.

---

## Dependency Summary

```
0.1 ──> 1.1 ──> 1.2 ──> 1.3 ──> 1.4 ──> 1.5 ──> 1.6
                                                 │
                                                 v
                                                2.1 ──> 2.2 ──> 2.3 ──> 2.4 ──> 2.5
                                                                                 │
                                                                                 v
                                                                                3.1 ──> 3.2 ──> 3.3
                                                                                                 │
                                                                                                 v
                                                                                                4.1 ──> 4.2 ──> 4.3 ──> 4.4
                                                                                                                         │
                                                                                                                         v
                                                                                                                        5.1 ──> [SCRAPPY stops: 5.2]
                                                                                                                                 │
                                                                                                                                 │ (Richard reviews, FULL-PASS continues)
                                                                                                                                 v
                                                                                                                                6.1 ──> 6.2 ──> 6.3 ──> 6.4 ──> 6.5
                                                                                                                                                                 │
                                                                                                                                                                 v
                                                                                                                                                                7.1 ──> 7.2 ──> 7.3 ──> 7.4
```

## Post-Execution

The audit is complete when Phase 7 tasks are done. What remains:

- git history captures every file deletion and every referrer edit.
- The archive at `wiki/agent-created/archive/system-subtraction-audit-{date}/` is the decision record.
- `wiki-candidates.md` has the one-line learning signal for the dreaming pipeline to process.
- `follow-on.md` in the archive names the extension-first restructure as the next structural step (not a task for this audit).

No live spec directory. No recurring hook. No dashboard. Done means done.
