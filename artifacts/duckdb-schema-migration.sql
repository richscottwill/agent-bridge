-- =============================================================================
-- ps_analytics Schema Reorganization Migration
-- =============================================================================
-- Purpose: Move from flat main schema (83 objects) to 8 logical schemas
-- Database: ps_analytics (MotherDuck)
-- 
-- IMPORTANT: Run each section sequentially. Views must be dropped before
-- tables move, then recreated with qualified names.
--
-- New schema: `ps` (Paid Search / Acquisition analytics)
-- This is the serious analytics schema — built for WBR/MBR/QBR/annual
-- review cadences across all 10 markets.
-- =============================================================================

-- ---------------------------------------------------------------------------
-- PHASE 0: Create all schemas
-- ---------------------------------------------------------------------------
CREATE SCHEMA IF NOT EXISTS ps_analytics.asana;
CREATE SCHEMA IF NOT EXISTS ps_analytics.signals;
CREATE SCHEMA IF NOT EXISTS ps_analytics.karpathy;
CREATE SCHEMA IF NOT EXISTS ps_analytics.ns;
CREATE SCHEMA IF NOT EXISTS ps_analytics.ops;
CREATE SCHEMA IF NOT EXISTS ps_analytics.wiki;
CREATE SCHEMA IF NOT EXISTS ps_analytics.ps;

-- ---------------------------------------------------------------------------
-- PHASE 1: Drop all views (they reference unqualified table names)
-- We'll recreate them with qualified names in Phase 4.
-- ---------------------------------------------------------------------------
DROP VIEW IF EXISTS ps_analytics.main.asana_by_project;
DROP VIEW IF EXISTS ps_analytics.main.asana_by_routine;
DROP VIEW IF EXISTS ps_analytics.main.asana_completion_rate;
DROP VIEW IF EXISTS ps_analytics.main.asana_overdue;
DROP VIEW IF EXISTS ps_analytics.main.audit_daily_summary;
DROP VIEW IF EXISTS ps_analytics.main.autoresearch_budget_signals;
DROP VIEW IF EXISTS ps_analytics.main.autoresearch_selection_weights;
DROP VIEW IF EXISTS ps_analytics.main.communication_trend;
DROP VIEW IF EXISTS ps_analytics.main.competitive_intelligence;
DROP VIEW IF EXISTS ps_analytics.main.experiment_confirmation_rates;
DROP VIEW IF EXISTS ps_analytics.main.five_levels_heatmap;
DROP VIEW IF EXISTS ps_analytics.main.hook_reliability;
DROP VIEW IF EXISTS ps_analytics.main.karpathy_organ_stats;
DROP VIEW IF EXISTS ps_analytics.main.karpathy_run_summary;
DROP VIEW IF EXISTS ps_analytics.main.organ_size_accuracy;
DROP VIEW IF EXISTS ps_analytics.main.pattern_trajectory;
DROP VIEW IF EXISTS ps_analytics.main.prior_convergence;
DROP VIEW IF EXISTS ps_analytics.main.projection_accuracy;
DROP VIEW IF EXISTS ps_analytics.main.recurring_tasks_due;
DROP VIEW IF EXISTS ps_analytics.main.signal_decay_curve;
DROP VIEW IF EXISTS ps_analytics.main.signal_heat_map;
DROP VIEW IF EXISTS ps_analytics.main.signal_person_topics;
DROP VIEW IF EXISTS ps_analytics.main.signal_trending;
DROP VIEW IF EXISTS ps_analytics.main.signal_wiki_candidates;
DROP VIEW IF EXISTS ps_analytics.main.slack_activity;
DROP VIEW IF EXISTS ps_analytics.main.slack_feed;
DROP VIEW IF EXISTS ps_analytics.main.task_velocity;
DROP VIEW IF EXISTS ps_analytics.main.tracker_trend;
DROP VIEW IF EXISTS ps_analytics.main.unified_signal_queue;
DROP VIEW IF EXISTS ps_analytics.main.wiki_throughput;
DROP VIEW IF EXISTS ps_analytics.main.workflow_reliability;

-- ---------------------------------------------------------------------------
-- PHASE 2: Move tables to their new schemas
-- ---------------------------------------------------------------------------

-- asana schema: task management & tracking
ALTER TABLE ps_analytics.main.asana_tasks SET SCHEMA ps_analytics.asana;
ALTER TABLE ps_analytics.main.asana_task_history SET SCHEMA ps_analytics.asana;
ALTER TABLE ps_analytics.main.asana_audit_log SET SCHEMA ps_analytics.asana;
ALTER TABLE ps_analytics.main.daily_tracker SET SCHEMA ps_analytics.asana;
ALTER TABLE ps_analytics.main.recurring_tasks SET SCHEMA ps_analytics.asana;
ALTER TABLE ps_analytics.main.recurring_task_state SET SCHEMA ps_analytics.asana;

-- signals schema: cross-channel intelligence
ALTER TABLE ps_analytics.main.signal_tracker SET SCHEMA ps_analytics.signals;
ALTER TABLE ps_analytics.main.unified_signals SET SCHEMA ps_analytics.signals;
ALTER TABLE ps_analytics.main.signal_task_log SET SCHEMA ps_analytics.signals;
ALTER TABLE ps_analytics.main.slack_messages SET SCHEMA ps_analytics.signals;
ALTER TABLE ps_analytics.main.slack_people SET SCHEMA ps_analytics.signals;
ALTER TABLE ps_analytics.main.slack_threads SET SCHEMA ps_analytics.signals;
ALTER TABLE ps_analytics.main.slack_topics SET SCHEMA ps_analytics.signals;

-- karpathy schema: body system optimization
ALTER TABLE ps_analytics.main.autoresearch_experiments SET SCHEMA ps_analytics.karpathy;
ALTER TABLE ps_analytics.main.autoresearch_organ_health SET SCHEMA ps_analytics.karpathy;
ALTER TABLE ps_analytics.main.autoresearch_priors SET SCHEMA ps_analytics.karpathy;
ALTER TABLE ps_analytics.main.body_size_history SET SCHEMA ps_analytics.karpathy;
ALTER TABLE ps_analytics.main.organ_word_counts SET SCHEMA ps_analytics.karpathy;
ALTER TABLE ps_analytics.main.karpathy_experiment_log SET SCHEMA ps_analytics.karpathy;
ALTER TABLE ps_analytics.main.experiment_outcomes SET SCHEMA ps_analytics.karpathy;

-- ns schema: nervous system calibration loops
ALTER TABLE ps_analytics.main.ns_communication SET SCHEMA ps_analytics.ns;
ALTER TABLE ps_analytics.main.ns_decisions SET SCHEMA ps_analytics.ns;
ALTER TABLE ps_analytics.main.ns_delegations SET SCHEMA ps_analytics.ns;
ALTER TABLE ps_analytics.main.ns_loop_snapshots SET SCHEMA ps_analytics.ns;
ALTER TABLE ps_analytics.main.ns_patterns SET SCHEMA ps_analytics.ns;
ALTER TABLE ps_analytics.main.decisions SET SCHEMA ps_analytics.ns;

-- ops schema: system operations & reliability
ALTER TABLE ps_analytics.main.hook_executions SET SCHEMA ps_analytics.ops;
ALTER TABLE ps_analytics.main.workflow_executions SET SCHEMA ps_analytics.ops;
ALTER TABLE ps_analytics.main.session_log SET SCHEMA ps_analytics.ops;
ALTER TABLE ps_analytics.main.intake_metrics SET SCHEMA ps_analytics.ops;
ALTER TABLE ps_analytics.main.data_freshness SET SCHEMA ps_analytics.ops;
ALTER TABLE ps_analytics.main.builder_cache SET SCHEMA ps_analytics.ops;

-- wiki schema: publishing pipeline
ALTER TABLE ps_analytics.main.wiki_pipeline_runs SET SCHEMA ps_analytics.wiki;
ALTER TABLE ps_analytics.main.publication_registry SET SCHEMA ps_analytics.wiki;

-- ps schema: paid search / acquisition analytics
-- Move existing PS-domain tables
ALTER TABLE ps_analytics.main.change_log SET SCHEMA ps_analytics.ps;
ALTER TABLE ps_analytics.main.competitive_signals SET SCHEMA ps_analytics.ps;
ALTER TABLE ps_analytics.main.projections SET SCHEMA ps_analytics.ps;
ALTER TABLE ps_analytics.main.health_alerts SET SCHEMA ps_analytics.ps;

-- main schema: keeps these (personal productivity, cross-cutting)
-- five_levels_weekly, l1_streak, meeting_analytics, meeting_highlights,
-- meeting_series, relationship_activity, content_embeddings, experiments
-- These stay in main — they don't belong to any single domain.

-- ---------------------------------------------------------------------------
-- PHASE 3: Build the PS analytics data model
-- ---------------------------------------------------------------------------
-- This is the new stuff. Purpose-built for paid search analytics across
-- WBR (weekly), MBR (monthly), QBR (quarterly), and annual cadences.
--
-- Design principles:
--   - market is ALWAYS a column (AU, MX, US, CA, JP, UK, DE, FR, IT, ES)
--   - channel separates paid_search, paid_app, acquisition, engagement
--   - period_type + period_key enable cadence-agnostic queries
--   - all monetary values in local currency with currency_code column
--   - targets and actuals live in the same table for easy variance calc
-- ---------------------------------------------------------------------------

-- 3a. Market reference dimension
CREATE TABLE IF NOT EXISTS ps_analytics.ps.markets (
    market_code     VARCHAR PRIMARY KEY,  -- AU, MX, US, CA, JP, UK, DE, FR, IT, ES
    market_name     VARCHAR NOT NULL,
    currency_code   VARCHAR NOT NULL,     -- AUD, MXN, USD, CAD, JPY, GBP, EUR, EUR, EUR, EUR
    region          VARCHAR NOT NULL,     -- APAC, LATAM, NA, NA, APAC, EU, EU, EU, EU, EU
    timezone        VARCHAR NOT NULL,     -- Australia/Sydney, America/Mexico_City, etc.
    hands_on        BOOLEAN DEFAULT FALSE -- TRUE for AU, MX (Richard's direct markets)
);

COMMENT ON TABLE ps_analytics.ps.markets IS
'Reference dimension for all 10 AB Paid Search markets. Currency, region, timezone, and ownership flag. Join key for all ps schema tables.';

INSERT INTO ps_analytics.ps.markets VALUES
    ('AU', 'Australia',      'AUD', 'APAC',  'Australia/Sydney',        TRUE),
    ('MX', 'Mexico',         'MXN', 'LATAM', 'America/Mexico_City',    TRUE),
    ('US', 'United States',  'USD', 'NA',    'America/Los_Angeles',    FALSE),
    ('CA', 'Canada',         'CAD', 'NA',    'America/Toronto',        FALSE),
    ('JP', 'Japan',          'JPY', 'APAC',  'Asia/Tokyo',             FALSE),
    ('UK', 'United Kingdom', 'GBP', 'EU',    'Europe/London',          FALSE),
    ('DE', 'Germany',        'EUR', 'EU',    'Europe/Berlin',          FALSE),
    ('FR', 'France',         'EUR', 'EU',    'Europe/Paris',           FALSE),
    ('IT', 'Italy',          'EUR', 'EU',    'Europe/Rome',            FALSE),
    ('ES', 'Spain',          'EUR', 'EU',    'Europe/Madrid',          FALSE);

-- 3b. Channel reference dimension
CREATE TABLE IF NOT EXISTS ps_analytics.ps.channels (
    channel_code    VARCHAR PRIMARY KEY,  -- ps, pa, acq, eng
    channel_name    VARCHAR NOT NULL,
    description     VARCHAR
);

COMMENT ON TABLE ps_analytics.ps.channels IS
'Reference dimension for acquisition/engagement channels. ps=Paid Search, pa=Paid App, acq=Acquisition (organic+paid), eng=Engagement (retention/reactivation).';

INSERT INTO ps_analytics.ps.channels VALUES
    ('ps',  'Paid Search',  'SEM/PPC campaigns on Google, Bing, Yahoo JP'),
    ('pa',  'Paid App',     'App install campaigns (Apple Search Ads, Google UAC)'),
    ('acq', 'Acquisition',  'All new customer acquisition (paid + organic)'),
    ('eng', 'Engagement',   'Retention, reactivation, lifecycle campaigns');

-- 3c. Metrics — the core fact table
-- One row per market × channel × metric × period.
-- Covers WBR (weekly), MBR (monthly), QBR (quarterly), annual.
CREATE TABLE IF NOT EXISTS ps_analytics.ps.metrics (
    metric_id       VARCHAR DEFAULT uuid()::VARCHAR,
    market          VARCHAR NOT NULL,     -- FK to markets
    channel         VARCHAR NOT NULL,     -- FK to channels
    metric_name     VARCHAR NOT NULL,     -- e.g. 'spend', 'registrations', 'cpa', 'roas', 'impressions', 'clicks', 'cvr'
    period_type     VARCHAR NOT NULL,     -- 'weekly', 'monthly', 'quarterly', 'annual'
    period_key      VARCHAR NOT NULL,     -- '2026-W14', '2026-03', '2026-Q1', '2026'
    period_start    DATE NOT NULL,        -- first day of period
    period_end      DATE NOT NULL,        -- last day of period
    actual_value    DOUBLE,               -- NULL if period hasn't closed
    target_value    DOUBLE,               -- NULL if no target set
    prior_period    DOUBLE,               -- same metric, previous period (for WoW, MoM, QoQ, YoY)
    prior_year      DOUBLE,               -- same metric, same period last year
    currency_code   VARCHAR,              -- local currency for monetary metrics, NULL for ratios
    unit            VARCHAR DEFAULT 'number', -- 'currency', 'percent', 'ratio', 'number'
    source          VARCHAR,              -- 'google_ads', 'bing', 'manual', 'api', 'sheets'
    notes           VARCHAR,
    updated_at      TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (market, channel, metric_name, period_type, period_key)
);

COMMENT ON TABLE ps_analytics.ps.metrics IS
'Core fact table for all paid search/acquisition/engagement metrics. One row per market × channel × metric × period. Supports WBR (weekly), MBR (monthly), QBR (quarterly), and annual cadences. Actuals and targets in the same row for easy variance calculation. Prior period and prior year columns enable trend analysis without self-joins.';

-- 3d. Targets — annual/quarterly goals that cascade down
-- Separate from metrics because targets are set top-down and don't change weekly.
CREATE TABLE IF NOT EXISTS ps_analytics.ps.targets (
    target_id       VARCHAR DEFAULT uuid()::VARCHAR,
    market          VARCHAR NOT NULL,
    channel         VARCHAR NOT NULL,
    metric_name     VARCHAR NOT NULL,     -- matches metrics.metric_name
    fiscal_year     INTEGER NOT NULL,     -- 2026
    period_type     VARCHAR NOT NULL,     -- 'annual', 'quarterly', 'monthly'
    period_key      VARCHAR NOT NULL,     -- '2026', '2026-Q1', '2026-03'
    target_value    DOUBLE NOT NULL,
    stretch_value   DOUBLE,               -- aspirational target (if different)
    source          VARCHAR,              -- 'op1', 'op2', 'qbr_reforecast', 'manual'
    approved_by     VARCHAR,              -- who signed off
    set_date        DATE,                 -- when target was set/revised
    notes           VARCHAR,
    PRIMARY KEY (market, channel, metric_name, period_type, period_key)
);

COMMENT ON TABLE ps_analytics.ps.targets IS
'Goal/target table for annual planning (OP1/OP2), QBR reforecasts, and monthly breakdowns. Cascades: annual → quarterly → monthly. Stretch targets optional. Source tracks whether target came from OP1, QBR reforecast, or manual override.';

-- 3e. Forecasts — forward-looking projections with confidence intervals
-- Replaces the generic projections table for PS-specific forecasting.
CREATE TABLE IF NOT EXISTS ps_analytics.ps.forecasts (
    forecast_id     VARCHAR DEFAULT uuid()::VARCHAR,
    market          VARCHAR NOT NULL,
    channel         VARCHAR NOT NULL,
    metric_name     VARCHAR NOT NULL,
    forecast_date   DATE NOT NULL,        -- when the forecast was made
    target_period   VARCHAR NOT NULL,     -- period being forecasted: '2026-W15', '2026-Q2', etc.
    period_type     VARCHAR NOT NULL,     -- 'weekly', 'monthly', 'quarterly', 'annual'
    predicted_value DOUBLE NOT NULL,
    confidence_low  DOUBLE,
    confidence_high DOUBLE,
    method          VARCHAR,              -- 'linear_trend', 'bayesian', 'manual', 'pace_based'
    actual_value    DOUBLE,               -- filled in after period closes
    error_pct       DOUBLE,               -- (actual - predicted) / actual * 100
    scored          BOOLEAN DEFAULT FALSE,
    score           VARCHAR,              -- 'HIT', 'MISS', 'SURPRISE'
    notes           VARCHAR,
    created_at      TIMESTAMP DEFAULT current_timestamp
);

COMMENT ON TABLE ps_analytics.ps.forecasts IS
'Forward-looking projections for PS metrics with confidence intervals. Scored after period closes. Replaces generic projections table for PS-domain forecasting. Supports pace-based (WTD/MTD extrapolation), trend, and Bayesian methods.';

-- 3f. Campaign changes — enriched version of change_log
-- Keeps the existing data but adds structure for analysis.
-- (change_log already moved to ps schema in Phase 2)

-- 3g. Pacing — intra-period tracking for WBR prep
CREATE TABLE IF NOT EXISTS ps_analytics.ps.pacing (
    pacing_id       VARCHAR DEFAULT uuid()::VARCHAR,
    market          VARCHAR NOT NULL,
    channel         VARCHAR NOT NULL,
    metric_name     VARCHAR NOT NULL,
    period_type     VARCHAR NOT NULL,     -- typically 'weekly' or 'monthly'
    period_key      VARCHAR NOT NULL,     -- '2026-W14', '2026-03'
    snapshot_date   DATE NOT NULL,        -- when this pacing snapshot was taken
    days_elapsed    INTEGER NOT NULL,     -- days into the period
    days_remaining  INTEGER NOT NULL,
    actual_to_date  DOUBLE,               -- spend/regs/etc. so far this period
    run_rate        DOUBLE,               -- actual_to_date / days_elapsed * total_days
    target_value    DOUBLE,               -- period target for comparison
    pacing_pct      DOUBLE,               -- actual_to_date / (target * days_elapsed/total_days) * 100
    status          VARCHAR,              -- 'on_pace', 'ahead', 'behind', 'at_risk'
    updated_at      TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (market, channel, metric_name, period_type, period_key, snapshot_date)
);

COMMENT ON TABLE ps_analytics.ps.pacing IS
'Intra-period pacing snapshots for WBR/MBR prep. Tracks actual-to-date vs target run rate. Status flags (on_pace/ahead/behind/at_risk) drive callout generation. One row per market × channel × metric × period × snapshot date.';

-- 3h. Account-level data — for market-specific deep dives
CREATE TABLE IF NOT EXISTS ps_analytics.ps.accounts (
    account_id      VARCHAR NOT NULL,     -- Google/Bing account ID
    market          VARCHAR NOT NULL,
    channel         VARCHAR NOT NULL,
    platform        VARCHAR NOT NULL,     -- 'google_ads', 'bing_ads', 'apple_search_ads', 'yahoo_jp'
    account_name    VARCHAR,
    account_type    VARCHAR,              -- 'brand', 'non_brand', 'competitor', 'dsa', 'pmax', 'shopping'
    status          VARCHAR DEFAULT 'active', -- 'active', 'paused', 'removed'
    monthly_budget  DOUBLE,
    currency_code   VARCHAR,
    notes           VARCHAR,
    PRIMARY KEY (account_id, platform)
);

COMMENT ON TABLE ps_analytics.ps.accounts IS
'Account-level reference data for all ad platforms across markets. Maps account IDs to market, channel, platform, and campaign type. Budget column enables spend vs budget analysis.';

-- 3i. Account metrics — granular performance by account
CREATE TABLE IF NOT EXISTS ps_analytics.ps.account_metrics (
    market          VARCHAR NOT NULL,
    account_id      VARCHAR NOT NULL,
    platform        VARCHAR NOT NULL,
    period_type     VARCHAR NOT NULL,
    period_key      VARCHAR NOT NULL,
    impressions     BIGINT,
    clicks          BIGINT,
    spend           DOUBLE,
    conversions     DOUBLE,              -- registrations, installs, etc.
    revenue         DOUBLE,              -- attributed revenue if available
    ctr             DOUBLE,              -- clicks / impressions
    cpc             DOUBLE,              -- spend / clicks
    cpa             DOUBLE,              -- spend / conversions
    cvr             DOUBLE,              -- conversions / clicks
    roas            DOUBLE,              -- revenue / spend
    impression_share DOUBLE,             -- for competitive analysis
    currency_code   VARCHAR,
    updated_at      TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (market, account_id, platform, period_type, period_key)
);

COMMENT ON TABLE ps_analytics.ps.account_metrics IS
'Account-level performance metrics. Granular data that rolls up into ps.metrics. Enables account-level deep dives, budget allocation analysis, and impression share tracking for competitive intelligence.';

-- ---------------------------------------------------------------------------
-- PHASE 4: Recreate all views with fully qualified table names
-- ---------------------------------------------------------------------------

-- === asana schema views ===
CREATE VIEW ps_analytics.asana.by_project AS
SELECT project_name, count(*) AS total,
       count(*) FILTER (WHERE NOT completed) AS incomplete,
       count(*) FILTER (WHERE completed) AS completed_count,
       count(*) FILTER (WHERE due_on < CURRENT_DATE AND NOT completed) AS overdue
FROM ps_analytics.asana.asana_tasks WHERE deleted_at IS NULL
GROUP BY project_name;

CREATE VIEW ps_analytics.asana.by_routine AS
SELECT routine_rw, count(*) AS task_count
FROM ps_analytics.asana.asana_tasks
WHERE NOT completed AND deleted_at IS NULL
GROUP BY routine_rw;

CREATE VIEW ps_analytics.asana.completion_rate AS
SELECT snapshot_date,
       count(*) FILTER (WHERE completed) AS completed,
       count(*) AS total,
       round(count(*) FILTER (WHERE completed) * 100.0 / nullif(count(*), 0), 1) AS completion_pct
FROM ps_analytics.asana.asana_task_history
WHERE snapshot_date >= CURRENT_DATE - 30
GROUP BY snapshot_date ORDER BY snapshot_date;

CREATE VIEW ps_analytics.asana.overdue AS
SELECT task_gid, name, project_name, due_on, routine_rw, priority_rw,
       datediff('day', due_on, CURRENT_DATE) AS days_overdue
FROM ps_analytics.asana.asana_tasks
WHERE due_on < CURRENT_DATE AND NOT completed AND deleted_at IS NULL
ORDER BY days_overdue DESC;

CREATE VIEW ps_analytics.asana.audit_daily_summary AS
SELECT CAST(timestamp AS DATE) AS audit_date,
       count(*) AS total_writes,
       count(*) FILTER (WHERE tool = 'CreateTask') AS tasks_created,
       count(*) FILTER (WHERE tool = 'UpdateTask') AS tasks_updated,
       count(*) FILTER (WHERE result = 'blocked') AS blocked,
       count(DISTINCT task_gid) AS unique_tasks
FROM ps_analytics.asana.asana_audit_log
GROUP BY CAST(timestamp AS DATE) ORDER BY audit_date DESC;

CREATE VIEW ps_analytics.asana.velocity AS
SELECT snapshot_date, routine_rw AS bucket,
       count(*) FILTER (WHERE completed) AS completed,
       count(*) FILTER (WHERE NOT completed) AS incomplete,
       count(*) FILTER (WHERE NOT completed AND due_on < snapshot_date) AS overdue
FROM ps_analytics.asana.asana_task_history
GROUP BY snapshot_date, routine_rw ORDER BY snapshot_date DESC, routine_rw;

CREATE VIEW ps_analytics.asana.tracker_trend AS
SELECT tracker_date, completed_count, total_overdue, workdays_at_zero,
       total_incomplete, blocker_count,
       lag(total_overdue) OVER (ORDER BY tracker_date) AS prev_overdue,
       total_overdue - lag(total_overdue) OVER (ORDER BY tracker_date) AS overdue_delta
FROM ps_analytics.asana.daily_tracker ORDER BY tracker_date DESC;

CREATE VIEW ps_analytics.asana.recurring_due AS
SELECT task_key, cadence, last_run, last_run_period, description,
       CASE WHEN cadence = 'weekly' THEN 'W' || date_part('week', CURRENT_DATE)
            WHEN cadence = 'monthly' THEN strftime(CURRENT_DATE, '%Y-%m')
            WHEN cadence = 'quarterly' THEN strftime(CURRENT_DATE, '%Y') || '-Q' || CAST(ceil(date_part('month', CURRENT_DATE) / 3.0) AS INTEGER)
       END AS current_period,
       CASE WHEN last_run_period != CASE
            WHEN cadence = 'weekly' THEN strftime(CURRENT_DATE, '%G') || '-W' || lpad(CAST(date_part('week', CURRENT_DATE) AS VARCHAR), 2, '0')
            WHEN cadence = 'monthly' THEN strftime(CURRENT_DATE, '%Y-%m')
            WHEN cadence = 'quarterly' THEN strftime(CURRENT_DATE, '%Y') || '-Q' || CAST(ceil(date_part('month', CURRENT_DATE) / 3.0) AS INTEGER)
       END THEN TRUE ELSE FALSE END AS is_due
FROM ps_analytics.asana.recurring_task_state;

-- === signals schema views ===
CREATE VIEW ps_analytics.signals.decay_curve AS
SELECT topic, signal_strength, first_seen, last_seen,
       datediff('day', last_seen, CURRENT_DATE) AS days_since_last_seen,
       reinforcement_count, source_channel,
       CASE WHEN signal_strength > 2.0 THEN 'STRONG'
            WHEN signal_strength > 1.0 THEN 'ACTIVE'
            WHEN signal_strength > 0.5 THEN 'FADING'
            ELSE 'DYING' END AS strength_category
FROM ps_analytics.signals.signal_tracker WHERE is_active ORDER BY signal_strength DESC;

CREATE VIEW ps_analytics.signals.heat_map AS
SELECT topic, sum(signal_strength) AS total_strength, count(*) AS total_mentions,
       count(DISTINCT source_channel) AS channel_spread,
       max(last_seen) AS most_recent, min(first_seen) AS first_detected,
       round(date_part('EPOCH', max(last_seen) - min(first_seen)) / 86400, 1) AS span_days,
       sum(reinforcement_count) AS total_reinforcements,
       list(DISTINCT source_channel) AS channels, list(DISTINCT source_author) AS authors
FROM ps_analytics.signals.signal_tracker WHERE is_active GROUP BY topic ORDER BY total_strength DESC;

CREATE VIEW ps_analytics.signals.person_topics AS
SELECT source_author, topic, count(*) AS mentions, sum(signal_strength) AS total_strength,
       max(last_seen) AS most_recent
FROM ps_analytics.signals.signal_tracker
WHERE is_active AND source_author IS NOT NULL
GROUP BY source_author, topic ORDER BY source_author, total_strength DESC;

CREATE VIEW ps_analytics.signals.trending AS
SELECT topic, sum(signal_strength) AS total_strength,
       count(*) FILTER (WHERE last_seen >= current_timestamp - INTERVAL '7 days') AS recent_mentions,
       count(*) FILTER (WHERE last_seen >= current_timestamp - INTERVAL '24 hours') AS today_mentions,
       count(DISTINCT source_channel) AS channel_spread,
       sum(reinforcement_count) AS total_reinforcements,
       list(DISTINCT source_channel) AS channels
FROM ps_analytics.signals.signal_tracker WHERE is_active GROUP BY topic
HAVING count(*) FILTER (WHERE last_seen >= current_timestamp - INTERVAL '7 days') >= 2
ORDER BY recent_mentions DESC, total_strength DESC;

CREATE VIEW ps_analytics.signals.wiki_candidates AS
SELECT topic, sum(signal_strength) AS total_strength, count(*) AS total_mentions,
       count(DISTINCT source_channel) AS channel_spread,
       count(DISTINCT source_author) AS unique_authors,
       min(first_seen) AS first_detected, max(last_seen) AS most_recent,
       round(date_part('EPOCH', max(last_seen) - min(first_seen)) / 86400, 1) AS span_days
FROM ps_analytics.signals.signal_tracker WHERE is_active GROUP BY topic
HAVING sum(signal_strength) >= 3.0 AND count(DISTINCT source_channel) >= 2 AND count(*) >= 3
ORDER BY total_strength DESC;

CREATE VIEW ps_analytics.signals.slack_activity AS
SELECT sp.alias AS author, sp.display_name AS name, sp.total_messages, sp.relationship_tier,
       count(DISTINCT sm.channel_name) AS channels_active,
       sum(CASE WHEN sm.signal_type = 'action-item' THEN 1 ELSE 0 END) AS action_items,
       sum(CASE WHEN sm.signal_type = 'decision' THEN 1 ELSE 0 END) AS decisions,
       max(sm.ts) AS last_message_ts
FROM ps_analytics.signals.slack_people sp
LEFT JOIN ps_analytics.signals.slack_messages sm ON sp.user_id = sm.author_id
GROUP BY sp.alias, sp.display_name, sp.total_messages, sp.relationship_tier
ORDER BY sp.total_messages DESC;

CREATE VIEW ps_analytics.signals.slack_feed AS
SELECT sm.ts, sm.channel_name,
       COALESCE(sp.alias, sm.author_id) AS author,
       COALESCE(sp.display_name, '') AS author_name,
       sm.text_preview, sm.signal_type, sm.is_richard, sm.reply_count,
       sm.reaction_count, sm.richard_reacted, sm.is_thread_reply, sm.ingested_at
FROM ps_analytics.signals.slack_messages sm
LEFT JOIN ps_analytics.signals.slack_people sp ON sm.author_id = sp.user_id
ORDER BY sm.ts DESC;

CREATE VIEW ps_analytics.signals.queue AS
SELECT *, CASE WHEN signal_type = 'blocker' THEN 5
               WHEN signal_type = 'request' THEN 4
               WHEN signal_type = 'decision' THEN 3
               WHEN signal_type = 'action_item' THEN 2
               WHEN signal_type = 'fyi' THEN 1 END AS type_weight,
       computed_priority
FROM ps_analytics.signals.unified_signals
WHERE disposition IS NULL ORDER BY computed_priority DESC, timestamp DESC;

-- === karpathy schema views ===
CREATE VIEW ps_analytics.karpathy.budget_signals AS
SELECT p.organ, p.technique,
       CAST(p.alpha AS FLOAT) / (p.alpha + p.beta) AS posterior_mean,
       sqrt(CAST(p.alpha AS FLOAT) * p.beta / ((p.alpha + p.beta) * (p.alpha + p.beta) * ((p.alpha + p.beta) + 1))) AS posterior_std,
       p.n_experiments, p.n_keeps, p.n_reverts,
       CASE WHEN p.technique = 'ADD' AND p.n_experiments > 5 AND CAST(p.alpha AS FLOAT) / (p.alpha + p.beta) < 0.3 THEN 'AT_CEILING'
            WHEN p.technique = 'COMPRESS' AND p.n_experiments > 5 AND CAST(p.alpha AS FLOAT) / (p.alpha + p.beta) > 0.7 THEN 'ROOM_TO_SHRINK'
            ELSE 'EXPLORING' END AS budget_signal
FROM ps_analytics.karpathy.autoresearch_priors p
WHERE p.technique IN ('ADD', 'COMPRESS') ORDER BY p.organ, p.technique;

CREATE VIEW ps_analytics.karpathy.selection_weights AS
SELECT organ, technique, alpha, beta,
       alpha / (alpha + beta) AS posterior_mean,
       n_experiments, n_keeps, n_reverts,
       sqrt(alpha * beta / (power(alpha + beta, 2) * (alpha + beta + 1))) AS posterior_std,
       alpha / (alpha + beta) + sqrt(alpha * beta / (power(alpha + beta, 2) * (alpha + beta + 1))) AS ucb_score
FROM ps_analytics.karpathy.autoresearch_priors ORDER BY ucb_score DESC;

CREATE VIEW ps_analytics.karpathy.organ_stats AS
SELECT organ, count(*) AS total,
       count(*) FILTER (WHERE result = 'KEEP') AS kept,
       round(count(*) FILTER (WHERE result = 'KEEP') * 100.0 / count(*), 0) AS keep_rate_pct,
       round(avg(CASE WHEN result = 'KEEP' THEN delta END), 3) AS avg_kept_delta
FROM ps_analytics.karpathy.karpathy_experiment_log GROUP BY organ ORDER BY total DESC;

CREATE VIEW ps_analytics.karpathy.run_summary AS
SELECT run_id, run_date, count(*) AS total_experiments,
       count(*) FILTER (WHERE result = 'KEEP') AS kept,
       count(*) FILTER (WHERE result = 'REVERT') AS reverted,
       round(count(*) FILTER (WHERE result = 'KEEP') * 100.0 / count(*), 0) AS keep_rate_pct,
       round(avg(delta), 3) AS avg_delta,
       sum(duration_seconds) AS total_duration_s
FROM ps_analytics.karpathy.karpathy_experiment_log
GROUP BY run_id, run_date ORDER BY run_date DESC, run_id DESC;

CREATE VIEW ps_analytics.karpathy.size_accuracy AS
SELECT oh.organ, oh.word_count, oh.accuracy_estimate,
       CAST(oh.snapshot_at AS DATE) AS measured_date,
       p_add.alpha / (p_add.alpha + p_add.beta) AS add_posterior, p_add.n_experiments AS add_n,
       p_comp.alpha / (p_comp.alpha + p_comp.beta) AS compress_posterior, p_comp.n_experiments AS compress_n,
       CASE WHEN p_add.alpha / (p_add.alpha + p_add.beta) < 0.3 AND p_add.n_experiments >= 5 THEN 'AT_CEILING'
            WHEN p_comp.alpha / (p_comp.alpha + p_comp.beta) > 0.7 AND p_comp.n_experiments >= 5 THEN 'SHOULD_COMPRESS'
            ELSE 'HEALTHY' END AS size_signal
FROM ps_analytics.karpathy.autoresearch_organ_health oh
LEFT JOIN ps_analytics.karpathy.autoresearch_priors p_add ON oh.organ = p_add.organ AND p_add.technique = 'ADD'
LEFT JOIN ps_analytics.karpathy.autoresearch_priors p_comp ON oh.organ = p_comp.organ AND p_comp.technique = 'COMPRESS'
ORDER BY oh.organ, oh.snapshot_at;

CREATE VIEW ps_analytics.karpathy.confirmation_rates AS
SELECT organ, technique, count(*) AS total_evaluated,
       count(*) FILTER (WHERE verdict = 'CONFIRMED') AS confirmed,
       count(*) FILTER (WHERE verdict = 'NEUTRAL') AS neutral,
       count(*) FILTER (WHERE verdict = 'REGRESSED') AS regressed,
       round(count(*) FILTER (WHERE verdict = 'CONFIRMED') * 100.0 / nullif(count(*), 0), 1) AS confirmation_rate_pct,
       round(avg(delta), 3) AS avg_lagged_delta
FROM ps_analytics.karpathy.experiment_outcomes GROUP BY organ, technique;

CREATE VIEW ps_analytics.karpathy.prior_convergence AS
SELECT organ, technique, alpha, beta, n_experiments,
       round(alpha / (alpha + beta), 3) AS posterior_mean,
       round(1.0 / (12.0 * (alpha + beta + 1) * (alpha + beta) * (alpha + beta)), 4) AS posterior_variance,
       CASE WHEN technique IN ('ADD', 'add') AND alpha / (alpha + beta) < 0.3 AND n_experiments >= 5 THEN 'AT_CEILING'
            WHEN technique IN ('COMPRESS', 'compress') AND alpha / (alpha + beta) > 0.7 AND n_experiments >= 5 THEN 'COMPRESS_SIGNAL'
            WHEN n_experiments < 5 THEN 'INSUFFICIENT_DATA'
            ELSE 'NORMAL' END AS budget_signal,
       last_updated
FROM ps_analytics.karpathy.autoresearch_priors ORDER BY organ, technique;

-- === ns schema views ===
CREATE VIEW ps_analytics.ns.communication_trend AS
SELECT week_start, meeting_type, avg_speaking_share, avg_hedging_count, meeting_count,
       lag(avg_speaking_share) OVER (PARTITION BY meeting_type ORDER BY week_start) AS prev_week_share,
       avg_speaking_share - lag(avg_speaking_share) OVER (PARTITION BY meeting_type ORDER BY week_start) AS share_delta,
       coaching_signal
FROM ps_analytics.ns.ns_communication ORDER BY meeting_type, week_start DESC;

CREATE VIEW ps_analytics.ns.pattern_trajectory AS
SELECT pattern_name, status, weeks_active, first_detected,
       CASE WHEN status = 'STUCK' AND weeks_active >= 3 THEN 'NEEDS_STRUCTURAL_FIX'
            WHEN status = 'WORSENING' THEN 'ESCALATE'
            WHEN status = 'IMPROVING' THEN 'MONITOR'
            WHEN status = 'RESOLVED' THEN 'ARCHIVE' END AS action_needed,
       gate_or_fix, escalated, resolved_date
FROM ps_analytics.ns.ns_patterns WHERE status != 'RESOLVED' ORDER BY weeks_active DESC;

-- === ops schema views ===
CREATE VIEW ps_analytics.ops.hook_reliability AS
SELECT hook_name, count(*) AS total_runs,
       round(avg(duration_seconds), 1) AS avg_duration_s,
       max(duration_seconds) AS max_duration_s,
       sum(phases_failed) AS total_failures,
       sum(asana_writes) AS total_asana_writes,
       max(execution_date) AS last_run
FROM ps_analytics.ops.hook_executions WHERE execution_date >= CURRENT_DATE - 30
GROUP BY hook_name;

CREATE VIEW ps_analytics.ops.workflow_reliability AS
SELECT workflow_name, count(*) AS total_runs,
       count(*) FILTER (WHERE status = 'completed') AS successes,
       round(count(*) FILTER (WHERE status = 'completed') * 100.0 / nullif(count(*), 0), 1) AS success_rate,
       round(avg(duration_seconds), 1) AS avg_duration_s,
       max(start_time) AS last_run
FROM ps_analytics.ops.workflow_executions
WHERE start_time > current_timestamp - INTERVAL '7 days'
GROUP BY workflow_name;

-- === wiki schema views ===
CREATE VIEW ps_analytics.wiki.throughput AS
SELECT CAST(date_trunc('week', started_at) AS DATE) AS week,
       count(DISTINCT article_title) AS articles_touched,
       count(*) FILTER (WHERE stage = 'publish') AS published,
       count(*) FILTER (WHERE stage = 'review') AS reviewed,
       round(avg(critic_score) FILTER (WHERE critic_score IS NOT NULL), 2) AS avg_critic_score,
       round(avg(word_count) FILTER (WHERE word_count IS NOT NULL), 0) AS avg_word_count
FROM ps_analytics.wiki.wiki_pipeline_runs
GROUP BY date_trunc('week', started_at) ORDER BY week DESC;

-- === main schema views (cross-cutting) ===
CREATE VIEW ps_analytics.main.five_levels_heatmap AS
SELECT week_start,
       max(CASE WHEN level = 1 THEN tasks_completed END) AS l1_completed,
       max(CASE WHEN level = 1 THEN streak_weeks END) AS l1_streak,
       max(CASE WHEN level = 2 THEN tasks_completed END) AS l2_completed,
       max(CASE WHEN level = 3 THEN tasks_completed END) AS l3_completed,
       max(CASE WHEN level = 4 THEN tasks_completed END) AS l4_completed,
       max(CASE WHEN level = 5 THEN tasks_completed END) AS l5_completed,
       sum(artifacts_shipped) AS total_artifacts
FROM ps_analytics.main.five_levels_weekly GROUP BY week_start ORDER BY week_start DESC;

-- === ps schema views — the analytics layer ===
CREATE VIEW ps_analytics.ps.competitive_intelligence AS
SELECT competitor_name, market, 
       count(*) FILTER (WHERE source_type = 'slack_mention') AS slack_mentions_7d,
       count(*) FILTER (WHERE source_type = 'impression_share') AS share_changes,
       count(*) FILTER (WHERE source_type = 'kds_finding') AS kds_findings,
       max(detected_at) AS last_signal
FROM ps_analytics.ps.competitive_signals
WHERE detected_at > current_timestamp - INTERVAL '7 days'
GROUP BY competitor_name, market;

CREATE VIEW ps_analytics.ps.forecast_accuracy AS
SELECT metric_name, market, method,
       count(*) AS total_forecasts,
       count(*) FILTER (WHERE scored) AS scored_count,
       count(*) FILTER (WHERE score = 'HIT') AS hits,
       count(*) FILTER (WHERE score = 'MISS') AS misses,
       count(*) FILTER (WHERE score = 'SURPRISE') AS surprises,
       round(count(*) FILTER (WHERE score = 'HIT') * 100.0 / nullif(count(*) FILTER (WHERE scored), 0), 1) AS hit_rate_pct,
       round(avg(abs(error_pct)) FILTER (WHERE scored), 1) AS avg_abs_error_pct
FROM ps_analytics.ps.forecasts GROUP BY metric_name, market, method;

-- WBR-ready: weekly variance view
CREATE VIEW ps_analytics.ps.weekly_variance AS
SELECT m.market, m.channel, m.metric_name, m.period_key,
       m.actual_value, m.target_value, m.prior_period, m.prior_year,
       round((m.actual_value - m.target_value) / nullif(m.target_value, 0) * 100, 1) AS vs_target_pct,
       round((m.actual_value - m.prior_period) / nullif(m.prior_period, 0) * 100, 1) AS wow_pct,
       round((m.actual_value - m.prior_year) / nullif(m.prior_year, 0) * 100, 1) AS yoy_pct,
       mk.region, mk.hands_on
FROM ps_analytics.ps.metrics m
JOIN ps_analytics.ps.markets mk ON m.market = mk.market_code
WHERE m.period_type = 'weekly'
ORDER BY m.period_key DESC, mk.region, m.market;

-- MBR-ready: monthly rollup with target attainment
CREATE VIEW ps_analytics.ps.monthly_attainment AS
SELECT m.market, m.channel, m.metric_name, m.period_key,
       m.actual_value, 
       t.target_value AS monthly_target,
       t.stretch_value AS stretch_target,
       round(m.actual_value / nullif(t.target_value, 0) * 100, 1) AS attainment_pct,
       round(m.actual_value / nullif(t.stretch_value, 0) * 100, 1) AS stretch_attainment_pct,
       m.prior_period, m.prior_year,
       round((m.actual_value - m.prior_period) / nullif(m.prior_period, 0) * 100, 1) AS mom_pct,
       round((m.actual_value - m.prior_year) / nullif(m.prior_year, 0) * 100, 1) AS yoy_pct
FROM ps_analytics.ps.metrics m
LEFT JOIN ps_analytics.ps.targets t 
    ON m.market = t.market AND m.channel = t.channel 
    AND m.metric_name = t.metric_name AND t.period_type = 'monthly' 
    AND m.period_key = t.period_key
WHERE m.period_type = 'monthly'
ORDER BY m.period_key DESC, m.market;

-- QBR-ready: quarterly with annual pace
CREATE VIEW ps_analytics.ps.quarterly_review AS
SELECT m.market, m.channel, m.metric_name, m.period_key,
       m.actual_value,
       t_q.target_value AS quarterly_target,
       t_a.target_value AS annual_target,
       round(m.actual_value / nullif(t_q.target_value, 0) * 100, 1) AS q_attainment_pct,
       -- Annualized pace: actual * 4 / annual target (rough, assumes even quarters)
       round(m.actual_value * 4 / nullif(t_a.target_value, 0) * 100, 1) AS annual_pace_pct,
       m.prior_year,
       round((m.actual_value - m.prior_year) / nullif(m.prior_year, 0) * 100, 1) AS yoy_pct
FROM ps_analytics.ps.metrics m
LEFT JOIN ps_analytics.ps.targets t_q 
    ON m.market = t_q.market AND m.channel = t_q.channel 
    AND m.metric_name = t_q.metric_name AND t_q.period_type = 'quarterly' 
    AND m.period_key = t_q.period_key
LEFT JOIN ps_analytics.ps.targets t_a 
    ON m.market = t_a.market AND m.channel = t_a.channel 
    AND m.metric_name = t_a.metric_name AND t_a.period_type = 'annual'
    AND t_a.fiscal_year = CAST(left(m.period_key, 4) AS INTEGER)
WHERE m.period_type = 'quarterly'
ORDER BY m.period_key DESC, m.market;

-- Pacing status for current open periods
CREATE VIEW ps_analytics.ps.current_pacing AS
SELECT p.market, p.channel, p.metric_name, p.period_type, p.period_key,
       p.actual_to_date, p.run_rate, p.target_value, p.pacing_pct, p.status,
       p.days_elapsed, p.days_remaining, p.snapshot_date,
       mk.region, mk.hands_on
FROM ps_analytics.ps.pacing p
JOIN ps_analytics.ps.markets mk ON p.market = mk.market_code
WHERE p.snapshot_date = (SELECT max(snapshot_date) FROM ps_analytics.ps.pacing)
ORDER BY p.status DESC, mk.region, p.market;

-- Account-level rollup by market
CREATE VIEW ps_analytics.ps.account_performance AS
SELECT am.market, a.account_name, a.account_type, a.platform,
       am.period_type, am.period_key,
       am.spend, am.conversions, am.cpa, am.roas, am.impression_share,
       a.monthly_budget,
       round(am.spend / nullif(a.monthly_budget, 0) * 100, 1) AS budget_utilization_pct
FROM ps_analytics.ps.account_metrics am
JOIN ps_analytics.ps.accounts a ON am.account_id = a.account_id AND am.platform = a.platform
ORDER BY am.period_key DESC, am.market, am.spend DESC;

-- 3j. Dashboard uploads — lineage for weekly WW dashboard ingestion
CREATE TABLE IF NOT EXISTS ps_analytics.ps.dashboard_uploads (
    upload_id       VARCHAR DEFAULT uuid()::VARCHAR,
    file_name       VARCHAR NOT NULL,
    week_ending     DATE NOT NULL,
    uploaded_at     TIMESTAMP DEFAULT current_timestamp,
    row_count       INTEGER,
    markets_found   VARCHAR[],
    channels_found  VARCHAR[],
    status          VARCHAR DEFAULT 'pending', -- 'pending', 'processed', 'error'
    error_message   VARCHAR,
    notes           VARCHAR
);

COMMENT ON TABLE ps_analytics.ps.dashboard_uploads IS
'Lineage tracker for weekly WW dashboard file uploads. Each row = one file ingestion. Rows in ps.metrics and ps.account_metrics trace back to an upload_id here. Status tracks processing pipeline state.';

-- === karpathy schema views ===
CREATE VIEW ps_analytics.karpathy.budget_signals AS
SELECT p.organ, p.technique,
       CAST(p.alpha AS FLOAT) / (p.alpha + p.beta) AS posterior_mean,
       sqrt(CAST(p.alpha AS FLOAT) * p.beta / ((p.alpha + p.beta) * (p.alpha + p.beta) * ((p.alpha + p.beta) + 1))) AS posterior_std,
       p.n_experiments, p.n_keeps, p.n_reverts,
       CASE WHEN p.technique = 'ADD' AND p.n_experiments > 5 AND CAST(p.alpha AS FLOAT) / (p.alpha + p.beta) < 0.3 THEN 'AT_CEILING'
            WHEN p.technique = 'COMPRESS' AND p.n_experiments > 5 AND CAST(p.alpha AS FLOAT) / (p.alpha + p.beta) > 0.7 THEN 'ROOM_TO_SHRINK'
            ELSE 'EXPLORING' END AS budget_signal
FROM ps_analytics.karpathy.autoresearch_priors p
WHERE p.technique IN ('ADD', 'COMPRESS')
ORDER BY p.organ, p.technique;

CREATE VIEW ps_analytics.karpathy.selection_weights AS
SELECT organ, technique, alpha, beta,
       alpha / (alpha + beta) AS posterior_mean,
       n_experiments, n_keeps, n_reverts,
       sqrt(alpha * beta / (power(alpha + beta, 2) * (alpha + beta + 1))) AS posterior_std,
       alpha / (alpha + beta) + sqrt(alpha * beta / (power(alpha + beta, 2) * (alpha + beta + 1))) AS ucb_score
FROM ps_analytics.karpathy.autoresearch_priors ORDER BY ucb_score DESC;

CREATE VIEW ps_analytics.karpathy.organ_stats AS
SELECT organ, count(*) AS total,
       count(*) FILTER (WHERE result = 'KEEP') AS kept,
       round(count(*) FILTER (WHERE result = 'KEEP') * 100.0 / count(*), 0) AS keep_rate_pct,
       round(avg(CASE WHEN result = 'KEEP' THEN delta END), 3) AS avg_kept_delta
FROM ps_analytics.karpathy.karpathy_experiment_log GROUP BY organ ORDER BY total DESC;

CREATE VIEW ps_analytics.karpathy.run_summary AS
SELECT run_id, run_date, count(*) AS total_experiments,
       count(*) FILTER (WHERE result = 'KEEP') AS kept,
       count(*) FILTER (WHERE result = 'REVERT') AS reverted,
       round(count(*) FILTER (WHERE result = 'KEEP') * 100.0 / count(*), 0) AS keep_rate_pct,
       round(avg(delta), 3) AS avg_delta,
       sum(duration_seconds) AS total_duration_s
FROM ps_analytics.karpathy.karpathy_experiment_log
GROUP BY run_id, run_date ORDER BY run_date DESC, run_id DESC;

CREATE VIEW ps_analytics.karpathy.organ_size_accuracy AS
SELECT oh.organ, oh.word_count, oh.accuracy_estimate,
       CAST(oh.snapshot_at AS DATE) AS measured_date,
       p_add.alpha / (p_add.alpha + p_add.beta) AS add_posterior, p_add.n_experiments AS add_n,
       p_comp.alpha / (p_comp.alpha + p_comp.beta) AS compress_posterior, p_comp.n_experiments AS compress_n,
       CASE WHEN p_add.alpha / (p_add.alpha + p_add.beta) < 0.3 AND p_add.n_experiments >= 5 THEN 'AT_CEILING'
            WHEN p_comp.alpha / (p_comp.alpha + p_comp.beta) > 0.7 AND p_comp.n_experiments >= 5 THEN 'SHOULD_COMPRESS'
            ELSE 'HEALTHY' END AS size_signal
FROM ps_analytics.karpathy.autoresearch_organ_health oh
LEFT JOIN ps_analytics.karpathy.autoresearch_priors p_add ON oh.organ = p_add.organ AND p_add.technique = 'ADD'
LEFT JOIN ps_analytics.karpathy.autoresearch_priors p_comp ON oh.organ = p_comp.organ AND p_comp.technique = 'COMPRESS'
ORDER BY oh.organ, oh.snapshot_at;

CREATE VIEW ps_analytics.karpathy.prior_convergence AS
SELECT organ, technique, alpha, beta, n_experiments,
       round(alpha / (alpha + beta), 3) AS posterior_mean,
       round(1.0 / (12.0 * (alpha + beta + 1) * (alpha + beta) * (alpha + beta)), 4) AS posterior_variance,
       CASE WHEN technique IN ('ADD', 'add') AND alpha / (alpha + beta) < 0.3 AND n_experiments >= 5 THEN 'AT_CEILING'
            WHEN technique IN ('COMPRESS', 'compress') AND alpha / (alpha + beta) > 0.7 AND n_experiments >= 5 THEN 'COMPRESS_SIGNAL'
            WHEN n_experiments < 5 THEN 'INSUFFICIENT_DATA'
            ELSE 'NORMAL' END AS budget_signal,
       last_updated
FROM ps_analytics.karpathy.autoresearch_priors ORDER BY organ, technique;

CREATE VIEW ps_analytics.karpathy.confirmation_rates AS
SELECT organ, technique, count(*) AS total_evaluated,
       count(*) FILTER (WHERE verdict = 'CONFIRMED') AS confirmed,
       count(*) FILTER (WHERE verdict = 'NEUTRAL') AS neutral,
       count(*) FILTER (WHERE verdict = 'REGRESSED') AS regressed,
       round(count(*) FILTER (WHERE verdict = 'CONFIRMED') * 100.0 / nullif(count(*), 0), 1) AS confirmation_rate_pct,
       round(avg(delta), 3) AS avg_lagged_delta
FROM ps_analytics.karpathy.experiment_outcomes GROUP BY organ, technique;

-- === ns schema views ===
CREATE VIEW ps_analytics.ns.communication_trend AS
SELECT week_start, meeting_type, avg_speaking_share, avg_hedging_count, meeting_count,
       lag(avg_speaking_share) OVER (PARTITION BY meeting_type ORDER BY week_start) AS prev_week_share,
       avg_speaking_share - lag(avg_speaking_share) OVER (PARTITION BY meeting_type ORDER BY week_start) AS share_delta,
       coaching_signal
FROM ps_analytics.ns.ns_communication ORDER BY meeting_type, week_start DESC;

CREATE VIEW ps_analytics.ns.pattern_trajectory AS
SELECT pattern_name, status, weeks_active, first_detected,
       CASE WHEN status = 'STUCK' AND weeks_active >= 3 THEN 'NEEDS_STRUCTURAL_FIX'
            WHEN status = 'WORSENING' THEN 'ESCALATE'
            WHEN status = 'IMPROVING' THEN 'MONITOR'
            WHEN status = 'RESOLVED' THEN 'ARCHIVE' END AS action_needed,
       gate_or_fix, escalated, resolved_date
FROM ps_analytics.ns.ns_patterns WHERE status != 'RESOLVED' ORDER BY weeks_active DESC;

-- === ops schema views ===
CREATE VIEW ps_analytics.ops.hook_reliability AS
SELECT hook_name, count(*) AS total_runs,
       round(avg(duration_seconds), 1) AS avg_duration_s,
       max(duration_seconds) AS max_duration_s,
       sum(phases_failed) AS total_failures,
       sum(asana_writes) AS total_asana_writes,
       max(execution_date) AS last_run
FROM ps_analytics.ops.hook_executions
WHERE execution_date >= CURRENT_DATE - 30 GROUP BY hook_name;

CREATE VIEW ps_analytics.ops.workflow_reliability AS
SELECT workflow_name, count(*) AS total_runs,
       count(*) FILTER (WHERE status = 'completed') AS successes,
       round(count(*) FILTER (WHERE status = 'completed') * 100.0 / nullif(count(*), 0), 1) AS success_rate,
       round(avg(duration_seconds), 1) AS avg_duration_s,
       max(start_time) AS last_run
FROM ps_analytics.ops.workflow_executions
WHERE start_time > current_timestamp - INTERVAL '7 days' GROUP BY workflow_name;

-- === wiki schema views ===
CREATE VIEW ps_analytics.wiki.throughput AS
SELECT CAST(date_trunc('week', started_at) AS DATE) AS week,
       count(DISTINCT article_title) AS articles_touched,
       count(*) FILTER (WHERE stage = 'publish') AS published,
       count(*) FILTER (WHERE stage = 'review') AS reviewed,
       round(avg(critic_score) FILTER (WHERE critic_score IS NOT NULL), 2) AS avg_critic_score,
       round(avg(word_count) FILTER (WHERE word_count IS NOT NULL), 0) AS avg_word_count
FROM ps_analytics.wiki.wiki_pipeline_runs
GROUP BY date_trunc('week', started_at) ORDER BY week DESC;

-- === ps schema views ===
CREATE VIEW ps_analytics.ps.competitive_intelligence AS
SELECT competitor_name, market, 
       count(*) FILTER (WHERE source_type = 'slack_mention') AS slack_mentions_7d,
       count(*) FILTER (WHERE source_type = 'impression_share') AS share_changes,
       count(*) FILTER (WHERE source_type = 'kds_finding') AS kds_findings,
       max(detected_at) AS last_signal
FROM ps_analytics.ps.competitive_signals
WHERE detected_at > current_timestamp - INTERVAL '7 days'
GROUP BY competitor_name, market;

CREATE VIEW ps_analytics.ps.forecast_accuracy AS
SELECT metric_name, market, method, count(*) AS total_forecasts,
       count(*) FILTER (WHERE scored) AS scored_count,
       count(*) FILTER (WHERE score = 'HIT') AS hits,
       count(*) FILTER (WHERE score = 'MISS') AS misses,
       count(*) FILTER (WHERE score = 'SURPRISE') AS surprises,
       round(count(*) FILTER (WHERE score = 'HIT') * 100.0 / nullif(count(*) FILTER (WHERE scored), 0), 1) AS hit_rate_pct,
       round(avg(abs(error_pct)) FILTER (WHERE scored), 1) AS avg_abs_error_pct
FROM ps_analytics.ps.forecasts GROUP BY metric_name, market, method;

-- Keep the legacy projection_accuracy view pointing at the old projections table (now in ps)
CREATE VIEW ps_analytics.ps.projection_accuracy AS
SELECT metric_name, market, method, count(*) AS total_projections,
       count(*) FILTER (WHERE scored) AS scored_count,
       count(*) FILTER (WHERE score = 'HIT') AS hits,
       count(*) FILTER (WHERE score = 'MISS') AS misses,
       count(*) FILTER (WHERE score = 'SURPRISE') AS surprises,
       round(count(*) FILTER (WHERE score = 'HIT') * 100.0 / nullif(count(*) FILTER (WHERE scored), 0), 1) AS hit_rate_pct,
       round(avg(abs(error_pct)) FILTER (WHERE scored), 1) AS avg_abs_error_pct
FROM ps_analytics.ps.projections GROUP BY metric_name, market, method;

-- Variance analysis: actuals vs targets vs prior period
CREATE VIEW ps_analytics.ps.variance AS
SELECT m.market, m.channel, m.metric_name, m.period_type, m.period_key,
       m.actual_value, m.target_value, m.prior_period, m.prior_year,
       CASE WHEN m.target_value IS NOT NULL AND m.target_value != 0
            THEN round((m.actual_value - m.target_value) / m.target_value * 100, 1) END AS vs_target_pct,
       CASE WHEN m.prior_period IS NOT NULL AND m.prior_period != 0
            THEN round((m.actual_value - m.prior_period) / m.prior_period * 100, 1) END AS vs_prior_pct,
       CASE WHEN m.prior_year IS NOT NULL AND m.prior_year != 0
            THEN round((m.actual_value - m.prior_year) / m.prior_year * 100, 1) END AS yoy_pct,
       m.currency_code, m.unit
FROM ps_analytics.ps.metrics m
WHERE m.actual_value IS NOT NULL;

-- WBR-ready weekly summary
CREATE VIEW ps_analytics.ps.wbr_weekly AS
SELECT m.market, m.channel, m.metric_name,
       m.period_key AS week, m.actual_value, m.target_value,
       m.prior_period AS prev_week, m.prior_year AS same_week_ly,
       CASE WHEN m.prior_period IS NOT NULL AND m.prior_period != 0
            THEN round((m.actual_value - m.prior_period) / m.prior_period * 100, 1) END AS wow_pct,
       CASE WHEN m.prior_year IS NOT NULL AND m.prior_year != 0
            THEN round((m.actual_value - m.prior_year) / m.prior_year * 100, 1) END AS yoy_pct,
       p.pacing_pct, p.status AS pacing_status
FROM ps_analytics.ps.metrics m
LEFT JOIN ps_analytics.ps.pacing p
    ON m.market = p.market AND m.channel = p.channel
    AND m.metric_name = p.metric_name AND m.period_key = p.period_key
    AND p.snapshot_date = (SELECT max(snapshot_date) FROM ps_analytics.ps.pacing p2
                           WHERE p2.market = p.market AND p2.period_key = p.period_key)
WHERE m.period_type = 'weekly';

-- === main schema views (cross-cutting) ===
CREATE VIEW ps_analytics.main.five_levels_heatmap AS
SELECT week_start,
       max(CASE WHEN level = 1 THEN tasks_completed END) AS l1_completed,
       max(CASE WHEN level = 1 THEN streak_weeks END) AS l1_streak,
       max(CASE WHEN level = 2 THEN tasks_completed END) AS l2_completed,
       max(CASE WHEN level = 3 THEN tasks_completed END) AS l3_completed,
       max(CASE WHEN level = 4 THEN tasks_completed END) AS l4_completed,
       max(CASE WHEN level = 5 THEN tasks_completed END) AS l5_completed,
       sum(artifacts_shipped) AS total_artifacts
FROM ps_analytics.main.five_levels_weekly GROUP BY week_start ORDER BY week_start DESC;

-- ---------------------------------------------------------------------------
-- PHASE 5: Rebuild FTS index for slack_messages (now in signals schema)
-- ---------------------------------------------------------------------------
-- The fts_main_slack_messages schema was auto-generated by DuckDB's FTS extension.
-- After moving slack_messages to signals schema, the old index is orphaned.
-- Drop it and recreate pointing at the new location.

DROP SCHEMA IF EXISTS ps_analytics.fts_main_slack_messages CASCADE;

-- Recreate FTS index on the new location
-- (Run after confirming slack_messages moved successfully)
-- PRAGMA create_fts_index('ps_analytics.signals.slack_messages', 'rowid', 'text_preview', 'channel_name');

-- ---------------------------------------------------------------------------
-- PHASE 6: Add comments to all ps schema tables
-- ---------------------------------------------------------------------------
COMMENT ON TABLE ps_analytics.ps.markets IS
'Reference dimension for all 10 AB Paid Search markets. Currency, region, timezone, and ownership flag. Join key for all ps schema tables.';

COMMENT ON TABLE ps_analytics.ps.channels IS
'Reference dimension for acquisition/engagement channels. ps=Paid Search, pa=Paid App, acq=Acquisition (organic+paid), eng=Engagement (retention/reactivation).';

COMMENT ON TABLE ps_analytics.ps.metrics IS
'Core fact table for all paid search/acquisition/engagement metrics. One row per market × channel × metric × period. Supports WBR (weekly), MBR (monthly), QBR (quarterly), and annual cadences. Actuals and targets in the same row for easy variance calculation.';

COMMENT ON TABLE ps_analytics.ps.targets IS
'Goal/target table for annual planning (OP1/OP2), QBR reforecasts, and monthly breakdowns. Source tracks whether target came from OP1, QBR reforecast, or manual override.';

COMMENT ON TABLE ps_analytics.ps.forecasts IS
'Forward-looking projections for PS metrics with confidence intervals. Scored after period closes. Supersedes generic projections table.';

COMMENT ON TABLE ps_analytics.ps.pacing IS
'Intra-period pacing snapshots for WBR/MBR prep. Tracks actual-to-date vs target run rate. Status flags drive callout generation.';

COMMENT ON TABLE ps_analytics.ps.accounts IS
'Account-level reference data for all ad platforms across markets. Maps account IDs to market, channel, platform, and campaign type.';

COMMENT ON TABLE ps_analytics.ps.account_metrics IS
'Account-level performance metrics. Granular data that rolls up into ps.metrics. Enables account-level deep dives and impression share tracking.';

COMMENT ON TABLE ps_analytics.ps.dashboard_uploads IS
'Lineage tracker for weekly WW dashboard file uploads. Each row = one file ingestion. Rows in ps.metrics trace back here via upload context.';

-- ---------------------------------------------------------------------------
-- PHASE 7: Verification queries
-- ---------------------------------------------------------------------------
-- Run these after migration to confirm everything landed correctly.

-- Check table counts per schema
SELECT schema_name, count(*) AS object_count, 
       count(*) FILTER (WHERE table_type = 'BASE TABLE') AS tables,
       count(*) FILTER (WHERE table_type = 'VIEW') AS views
FROM information_schema.tables 
WHERE table_catalog = 'ps_analytics'
GROUP BY schema_name ORDER BY schema_name;

-- Check main is lean (should be ~8 tables + 1 view)
SELECT table_name, table_type 
FROM information_schema.tables 
WHERE table_catalog = 'ps_analytics' AND table_schema = 'main'
ORDER BY table_type, table_name;

-- Check ps schema has all expected objects
SELECT table_name, table_type 
FROM information_schema.tables 
WHERE table_catalog = 'ps_analytics' AND table_schema = 'ps'
ORDER BY table_type, table_name;

-- Smoke test: ps.variance view should return without errors
SELECT * FROM ps_analytics.ps.variance LIMIT 5;

-- Smoke test: asana views still work
SELECT * FROM ps_analytics.asana.by_project LIMIT 5;
SELECT * FROM ps_analytics.asana.overdue LIMIT 5;

-- Smoke test: signals views still work  
SELECT * FROM ps_analytics.signals.trending LIMIT 5;
