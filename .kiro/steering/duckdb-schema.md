---
inclusion: auto
---

# DuckDB Schema Reference (ps_analytics on MotherDuck)

As of 2026-04-06, ps_analytics uses 8 schemas. **Never write unqualified table names.** Always use `schema.table` format (e.g., `asana.asana_tasks`, not just `asana_tasks`). The database context is already set to `ps_analytics` via `USE ps_analytics`.

## Schema Map

| Schema | Purpose | Key tables |
|--------|---------|------------|
| `asana` | Task management, daily tracker, recurring tasks, audit trail | asana_tasks, asana_task_history, audit_log, daily_tracker, recurring_task_state, recurring_tasks |
| `signals` | Cross-channel intelligence (Slack, email, unified signals) | signal_tracker, unified_signals, slack_messages, slack_people, slack_threads, slack_topics, signal_task_log, emails |
| `karpathy` | Body system optimization, autoresearch experiments | autoresearch_experiments, autoresearch_organ_health, autoresearch_priors, karpathy_experiment_log, experiment_outcomes, body_size_history, organ_word_counts |
| `ns` | Nervous system calibration loops | ns_communication, ns_decisions, ns_delegations, ns_loop_snapshots, ns_patterns, decisions |
| `ops` | System operations, hook/workflow reliability | hook_executions, workflow_executions, session_log, intake_metrics, data_freshness, builder_cache |
| `wiki` | Publishing pipeline | wiki_pipeline_runs, publication_registry |
| `ps` | **Paid Search / Acquisition analytics** — WBR, MBR, QBR, annual | metrics, targets, forecasts, pacing, accounts, account_metrics, dashboard_uploads, markets, channels, change_log, competitive_signals, projections, health_alerts |
| `main` | Personal productivity, cross-cutting, calendar | five_levels_weekly, l1_streak, meeting_analytics, meeting_highlights, meeting_series, relationship_activity, content_embeddings, experiments, calendar_events |

## Query Rules

### DuckDB-First Principle
**DEFAULT: Query DuckDB for all operational data.** DuckDB is synced during AM-Backend (full sync) and EOD-2 (delta sync). Between syncs, DuckDB is the authoritative read source.

**When to query DuckDB (default):**
- Asana tasks, overdue, buckets, history → `asana.asana_tasks`, `asana.overdue`, etc.
- Slack messages, signals, topics → `signals.slack_messages`, `signals.signal_tracker`, etc.
- Email triage, unanswered → `signals.emails`, `signals.emails_actionable`
- Calendar today/week → `main.calendar_today`, `main.calendar_week`
- Audit trail → `asana.audit_log`, `asana.recent_audit`
- Meeting data → `main.meeting_analytics`, `main.meeting_highlights`
- Market metrics → `ps.metrics`, `ps.wbr_weekly`, etc.

**When to query live MCP sources (exceptions):**
- During AM-Backend sync (writing TO DuckDB — must read from source)
- During EOD-2 delta sync (same)
- When Richard explicitly asks for "live" or "current" data from a specific source
- When performing a write operation (Asana UpdateTask, email send, Slack post — always hit the live API)
- When DuckDB data is known stale (sync failed, first run of day before AM-Backend) — agent should auto-refresh from live MCP AND update DuckDB inline

**Staleness indicator:** Each synced table has a `synced_at` column. If `MAX(synced_at) < CURRENT_TIMESTAMP - INTERVAL '12 hours'`, the data is stale. **Auto-refresh rule:** When the agent detects stale data, it should immediately query the live MCP source, use the fresh data for the current task, AND update the DuckDB table with the new data so subsequent queries are fresh. Don't just flag staleness — fix it inline.

### Schema Rules
1. Always prefix table names with schema: `SELECT * FROM asana.asana_tasks`
2. Cross-schema joins use schema prefixes: `SELECT ... FROM signals.signal_tracker s JOIN asana.asana_tasks a ON ...`
3. Views live in the same schema as their base tables. Use `asana.overdue` not `main.asana_overdue`.
4. The `ps` schema is the analytics backbone. All market/channel/period data lives there.
5. `ps.metrics` is the core fact table — one row per market × channel × metric × period.
6. `ps.markets` and `ps.channels` are reference dimensions — join on market_code and channel_code.

## Key Views by Schema

- `asana.overdue`, `asana.by_project`, `asana.velocity`, `asana.tracker_trend`, `asana.recurring_due`, `asana.recent_audit`
- `signals.trending`, `signals.queue`, `signals.slack_feed`, `signals.heat_map`, `signals.emails_actionable`, `signals.emails_unanswered`
- `karpathy.organ_stats`, `karpathy.run_summary`, `karpathy.budget_signals`, `karpathy.prior_convergence`
- `ns.pattern_trajectory`, `ns.communication_trend`
- `ops.hook_reliability`, `ops.workflow_reliability`
- `wiki.throughput`
- `ps.wbr_weekly`, `ps.variance`, `ps.forecast_accuracy`, `ps.competitive_intelligence`
- `main.five_levels_heatmap`, `main.calendar_today`, `main.calendar_week`

## Migration Note

This schema layout replaced a flat 83-object `main` schema on 2026-04-06. If you encounter old queries referencing `main.asana_tasks` or `main.signal_tracker`, update them to use the correct schema prefix.
