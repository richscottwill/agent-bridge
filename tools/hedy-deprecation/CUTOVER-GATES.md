# Hedy Deprecation — Cutover Gates

Created 2026-05-06. Must all be green before running `teardown-hedy-tables.sql`.

## Gate 1: Topic-log pipeline has run ≥2 successful cycles

- [ ] EOD Phase 1 has run twice with the new v7.2.0 hook writing to topic logs
- [ ] AM-Backend Subagent E has run twice with the new v5.3.0 hook routing to topic logs
- [ ] No errors in `ops.hook_executions` rows for those runs

Check with:
```sql
SELECT hook_name, execution_date, start_time, end_time, summary
FROM ops.hook_executions
WHERE hook_name IN ('eod-meeting-sync', 'am-backend')
  AND execution_date >= CURRENT_DATE - 2
ORDER BY start_time DESC;
```

## Gate 2: Topic logs show recent Hedy-sourced entries

- [ ] At least 5 topic log `.md` files under `~/shared/wiki/topics/` have Log entries citing `hedy:<session_id>` from the last 72 hours
- [ ] Entries include direct quotes and decisions per the sourcing bar

Check with:
```bash
grep -rlE "hedy:[A-Za-z0-9]+" ~/shared/wiki/topics/*/*.md | wc -l
```

## Gate 3: Consumers of deprecated tables all migrated

- [ ] `wbr-callouts.kiro.hook` — no longer queries `main.meeting_series` (patched 2026-05-06)
- [ ] `topic-sentry.kiro.hook` — no longer queries `signals.hedy_meetings` (patched 2026-05-06)
- [ ] `broad-sweep.kiro.hook` — reads Hedy coverage from topic-log files (patched 2026-05-06)
- [ ] `refresh-system-flow.py` — counts topic-log files instead (patched 2026-05-06)
- [ ] `refresh_data_freshness.py` — `hedy_meetings` marked deprecated, `topic_logs` added (patched 2026-05-06)
- [ ] `context-enrichment.md` Step 2.5A — deprecation banner in place (patched 2026-05-06)
- [ ] `communication-analytics.md` — deprecation banner in place (patched 2026-05-06)
- [ ] `meeting-to-task-pipeline.md` Steps 6+7 — marked DEPRECATED (patched 2026-05-06)
- [ ] `state-file-engine.md` — no direct references to deprecated tables (verified 2026-05-06, clean)

## Gate 4: Archive written, verified

- [ ] Run Step 1+2 of `teardown-hedy-tables.sql` (CREATE SCHEMA, COPY with archive timestamp)
- [ ] Row counts verified — archive matches original for all 4 tables
- [ ] Archive schema `hedy_archive` visible in `SELECT * FROM information_schema.schemata`

## Gate 5: One-week soak

- [ ] Topic logs have been the only Hedy consumer for ≥7 days
- [ ] No dashboard or hook has surfaced errors referencing deprecated tables
- [ ] WBR callout Monday ran cleanly without `meeting_series` — verify cross-channel signal flags still populate from topic-log scan

## Gate 6: Final sign-off

- [ ] Richard explicit go-ahead to run Step 3+4 (DROP tables + update freshness)
- [ ] Rollback path documented: restore from `hedy_archive.*` tables if any consumer breaks

## Cutover sequence

Only after all 6 gates green:

1. Run archive step: `Step 1+2` of teardown SQL
2. Verify row counts match
3. Uncomment Step 3 (DROP TABLE x 4)
4. Uncomment Step 4 (freshness update)
5. Run the full script
6. Watch next EOD + AM cycle for errors
7. If clean: log completion in session-log.md, archive `_discovery-queue.md` first-seed entries older than 30d
8. If issues: roll back via `CREATE TABLE <original> AS SELECT * EXCLUDE(_archived_at) FROM hedy_archive.<original>`
