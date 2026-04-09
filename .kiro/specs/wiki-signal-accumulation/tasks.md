# Implementation Plan: Wiki Signal Accumulation Pipeline

## Overview

Wire signal accumulation into the existing AM-Backend → AM-Frontend → wiki pipeline chain. Build the matching, evidence, scoring, and triggering layers. All code is Python. New tables go in DuckDB `wiki` schema. Pipeline execution uses existing kiro-cli wiki agents.

## Tasks

- [ ] 1. Create DuckDB schema and tables
  - [ ] 1.1 Create `wiki` schema and `wiki.content_evidence` table
    - Evidence ledger: task_gid, signal_id, source_type, source_author, source_preview, confidence, matched_keywords, is_directive, is_data_change, created_at
    - Primary key on (task_gid, signal_id)
    - _Requirements: 2.1, 2.5_
  - [ ] 1.2 Create `wiki.content_tasks` table
    - Mirror of ABPS AI Content tasks: task_gid, name, pipeline_stage, category, audience, series, frequency, levels, keywords, evidence_count, readiness_score, last_evidence_at, last_published_at, synced_at
    - `last_published_at` tracks when the task last reached Published — used for frequency-based re-accumulation
    - _Requirements: 5.1, 10.1_
  - [ ] 1.3 Create `wiki.pipeline_triggers` table
    - Trigger log: trigger_id, task_gid, trigger_type, readiness_score, evidence_count, source_diversity, trigger_signal_id, triggered_at
    - _Requirements: 4.3, 9.2_
  - [ ] 1.4 Create or update `signals.wiki_candidates` view
    - Rank Idea-stage tasks by readiness_score descending, join with evidence counts and source diversity
    - _Requirements: 9.1_

- [ ] 2. Checkpoint — Verify schema
  - Ensure all tables and views exist in DuckDB. Query each to confirm structure.

- [ ] 3. Build content task sync
  - [ ] 3.1 Create `shared/tools/wiki/content_sync.py` with `sync_content_tasks(con)` function
    - Pull all ABPS AI Content tasks from Asana (GetTasksFromProject with opt_fields for custom fields)
    - Extract keywords from task names and descriptions (stopword removal, lowercase, dedupe)
    - Upsert to `wiki.content_tasks` with pipeline_stage from Pipeline_RW, category from Category_RW, etc.
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 4. Build signal matcher
  - [ ] 4.1 Create `shared/tools/wiki/signal_matcher.py` with `SignalMatcher` class
    - `__init__`: load content tasks from `wiki.content_tasks`
    - `match(signal)`: extract keywords from signal text, compare against task keywords/name/category/series
    - Weighted scoring: name match (0.4), category match (0.3), keyword overlap (0.3)
    - Return MatchResult if confidence >= 0.6, else None
    - _Requirements: 1.1, 1.5, 1.6, 1.7_
  - [ ] 4.2 Implement directive detection in matcher
    - Check if signal author is Brandon (brandoxy) or Kate (kataxt)
    - Check for action language patterns: "put together", "write up", "document", "create a doc", "need a one-pager", etc.
    - Set is_directive=true on evidence when both conditions met
    - _Requirements: 2.3_
  - [ ] 4.3 Implement `match_signals_to_content(con)` orchestrator function
    - Query `signals.unified_signals WHERE disposition IS NULL`
    - For each signal, call matcher.match()
    - Insert matched evidence to `wiki.content_evidence`
    - Update signal disposition in `signals.unified_signals`
    - _Requirements: 1.2, 1.3, 1.4_

- [ ] 5. Checkpoint — Verify matching
  - Run matcher against existing signals in DuckDB. Verify evidence rows created, dispositions updated.

- [ ] 6. Build readiness scorer
  - [ ] 6.1 Create `shared/tools/wiki/readiness_scorer.py` with `ReadinessScorer` class
    - `compute_readiness(task_gid, evidence, task_metadata)` → ReadinessScore
    - Five components: signal_count (0-25, confidence-weighted), source_diversity (0-25), recency (0-20), author_weight (0-15), data_availability (0-15)
    - Signal count uses confidence-weighted formula: `min(25, sum(confidence) * 5)` — not raw count
    - Directive bypass: any is_directive=true → score=100
    - Recency decay: signals >30d old get reduced recency contribution
    - For recurring tasks: only count evidence with `created_at > last_published_at`
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 10.3_
  - [ ] 6.2 Implement `score_all_tasks(con)` function
    - Query evidence grouped by task_gid
    - Compute readiness for each task with evidence
    - Update `wiki.content_tasks` with readiness_score and evidence_count
    - Return list of tasks that crossed threshold
    - _Requirements: 3.1, 6.4_

- [ ] 7. Build pipeline trigger
  - [ ] 7.1 Create `shared/tools/wiki/pipeline_trigger.py` with `trigger_pipeline(con, task_gid, score)` function
    - Verify task is at Pipeline_RW = Idea (idempotent — skip if already Drafting+)
    - Update Asana: Pipeline_RW → Drafting, Kiro_RW with trigger context
    - Insert row to `wiki.pipeline_triggers`
    - Append audit log entry
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.6_
  - [ ] 7.2 Implement immediate directive trigger path
    - When directive detected during matching, call trigger_pipeline() immediately
    - Set trigger_type='directive' in pipeline_triggers
    - _Requirements: 4.5_

- [ ] 8. Checkpoint — Verify scoring and triggering
  - Manually insert test evidence rows, run scorer, verify threshold detection and Asana Pipeline_RW update.

- [ ] 9. Wire into AM-Backend
  - [ ] 9.1 Add signal accumulation phase to AM-Backend protocol
    - After signal ingestion, before brief generation
    - Sequence: sync_content_tasks() → match_signals_to_content() → score_all_tasks() → trigger if threshold met
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  - [ ] 9.2 Write accumulation results to pre-computed state file
    - Output to `am-content-readiness.json`: per-task readiness scores, triggered tasks, near-threshold tasks
    - _Requirements: 6.5_

- [ ] 10. Wire into AM-Frontend
  - [ ] 10.1 Add Content Pipeline section to daily brief
    - Read `am-content-readiness.json`
    - Display: task name, score/threshold, evidence count, source diversity, most recent signal
    - Flag triggered tasks with ✅, near-threshold with ⚠️
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 11. Wire wiki pipeline execution
  - [ ] 11.1 Implement frequency-based re-accumulation reset
    - During AM-Backend, before signal matching: check `wiki.content_tasks` for Published tasks where `now() - last_published_at > frequency_interval`
    - Reset Pipeline_RW to Idea in Asana, reset readiness_score to 0 in DuckDB
    - Skip One-time tasks (they stay Published forever)
    - _Requirements: 10.1, 10.2, 10.4, 10.5_
  - [ ] 11.2 Implement pipeline execution orchestration in AM-Backend
    - After accumulation/scoring, before brief generation
    - Query `wiki.content_tasks WHERE pipeline_stage = 'Drafting'` ordered by readiness_score DESC
    - Process at most 1 task per AM cycle
    - Invoke wiki agents via kiro-cli in sequence: editor → researcher → writer → critic (Eval A) → critic (Eval B) → librarian (if both pass)
    - Each agent reads `wiki.content_evidence` for the task to get accumulated context
    - Track pipeline stage in Asana Pipeline_RW and Kiro_RW after each agent completes
    - On agent failure: log error, leave task at current stage, retry next AM cycle (max 2 retries)
    - On publish: set `last_published_at` in `wiki.content_tasks`, update Pipeline_RW to Published
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9_
  - [ ] 11.3 Implement pipeline queue visibility
    - If multiple tasks are at Drafting, write queue order to `am-content-readiness.json`
    - Daily brief shows: "Pipeline queue: [task1] (processing), [task2] (queued), [task3] (queued)"
    - _Requirements: 8.7_

- [ ] 12. Checkpoint — End-to-end validation
  - Create a test content task in ABPS AI Content at Idea stage
  - Inject 5 test signals from 3 sources into unified_signals
  - Run full AM-Backend cycle
  - Verify: evidence accumulated, readiness scored, threshold crossed, Pipeline_RW advanced to Drafting
  - Verify: daily brief shows Content Pipeline section with correct data

- [ ] 13. Final checkpoint
  - Ensure all tables populated, matching working, scoring calibrated, triggers firing. Ask Richard if questions arise.

## Notes

- Tasks marked with `*` would be optional property-based tests (none in this spec — keeping it lean)
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- The signal matcher is intentionally simple (keyword-based) — can be upgraded to semantic similarity later if matching quality is poor
- The readiness threshold (60) and component weights are initial values — calibrate after 2-4 weeks of data
- Wiki pipeline execution (task 11) depends on kiro-cli agent infrastructure working reliably
- All new code goes under `shared/tools/wiki/`
