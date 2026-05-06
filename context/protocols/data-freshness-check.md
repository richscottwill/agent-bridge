---
title: "Data Freshness Check Protocol"
type: protocol
status: ACTIVE
owner: Richard Williams
created: 2026-05-06
updated: 2026-05-06
---

# Data Freshness Check Protocol

Called by `data-freshness-warning.kiro.hook` on every promptSubmit. Prevents agents from producing stale-as-fresh outputs by surfacing when upstream DuckDB sources are behind their expected cadence.

## Gate

Check if you've already surfaced freshness warnings in this conversation. If yes, skip silently. Otherwise run the check below.

## Query

Run silent DuckDB query:

```sql
SELECT
  source_name,
  source_type,
  expected_cadence_hours,
  DATE_DIFF('hour', last_updated, CURRENT_TIMESTAMP) AS hours_since_update,
  ROUND(DATE_DIFF('hour', last_updated, CURRENT_TIMESTAMP) / expected_cadence_hours::FLOAT, 1) AS staleness_multiple,
  downstream_workflows
FROM ops.data_freshness
WHERE last_updated IS NOT NULL
  AND DATE_DIFF('hour', last_updated, CURRENT_TIMESTAMP) > expected_cadence_hours * 1.5
  AND source_type LIKE 'duckdb%'
ORDER BY staleness_multiple DESC
```

The `1.5x cadence` threshold is a "materially stale" bar — ignores sources that are just slightly behind schedule, surfaces sources that are meaningfully delayed.

## Output format

If the query returns 0 rows: skip silently.

If 1-3 stale sources: prepend one-liner to response:

```
⚠️ Stale sources: slack_messages (49h / 36h cadence, 1.4x), loop_pages (74h / 12h, 6.2x), emails (49h / 12h, 4.1x) — downstream workflows may produce stale-as-fresh outputs. Check context/active/ for last AM-Backend run.
```

If 4+ stale sources: prepend compact summary:

```
⚠️ Multiple sources stale (N of M DuckDB tables) — AM-Backend likely hasn't run today. Affected workflows: [deduped list of downstream_workflows]. Confirm last run before producing outputs labeled as current.
```

## Non-blocking

Background check only. Do NOT delay Richard's actual request. If DuckDB is unreachable or query errors, skip silently rather than surfacing the error.

## Why 1.5x cadence not 1.0x

A source updated exactly at its cadence boundary is fine — it's expected to be "due for refresh soon." Only flag when meaningfully overdue. The `is_stale` boolean in the table uses a stricter 1.0x threshold, which is fine for dashboard-level alerting but too noisy for per-turn warnings.

## Rationale for existence

The pattern this prevents: AM-Backend fails or runs degraded, DuckDB tables don't get refreshed, but the agent produces outputs (daily brief, callouts, analyses) labeled as "fresh as of today" built on yesterday's or older data. This has hit the system multiple times:
- 2026-05-04: cross-channel WoW data gap (ingester didn't extract the channel tab)
- 2026-05-05: degraded-auth AM run labeled outputs as current when signal_tracker was 25+ hours old
- Multiple 401/cookie-expiry scenarios where MCP ingest silently skipped sources

The freshness warning inverts this: agent is told upfront "your upstream data is N hours past cadence" before generating outputs.
