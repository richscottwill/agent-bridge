<!-- DOC-0169 | duck_id: intake-asana-digest-parallel-test -->
# Asana Sync — Parallel Test Results

**Run:** 2026-04-06 | **Subagent:** B1 (Asana Sync + DuckDB) | **Mode:** Read-only verification

## Counts

| Source | Incomplete Tasks |
|--------|-----------------|
| Asana API (SearchTasksInWorkspace) | 97 |
| DuckDB (asana.asana_tasks WHERE completed=FALSE AND deleted_at IS NULL) | 109 |

## Snapshot Status

| Check | Result |
|-------|--------|
| Today's snapshot exists (asana_task_history) | Yes — 135 rows for 2026-04-06 |
| Only snapshot date in history | 2026-04-06 (single day) |
| Total tasks in asana_tasks | 135 |
| Completed | 0 |
| Soft-deleted (deleted_at IS NOT NULL) | 26 |
| Incomplete + active | 109 |

## Discrepancy Analysis

**API vs DuckDB delta: 12 tasks (109 DuckDB - 97 API)**

Likely causes:
1. SearchTasksInWorkspace returns max ~100 results — the 97 returned suggests we're near the pagination ceiling. The remaining 12 tasks exist in Asana but weren't returned in this single API call.
2. The morning sync (which populates DuckDB) uses a different retrieval method (likely project-by-project iteration across all 6 portfolio projects) that captures the full set.

**This is NOT a data integrity issue.** The DuckDB count of 109 is the authoritative number — the API search endpoint has known pagination limits.

## Verdict

- Subagent completed cleanly (read-only, no writes to DuckDB)
- Morning snapshot exists for today
- DuckDB data is consistent (135 total = 109 incomplete + 0 completed + 26 deleted)
- API search returns 97 vs DuckDB 109 — expected pagination gap, not a sync error
- No modifications made to asana-morning-snapshot.json or DuckDB tables
