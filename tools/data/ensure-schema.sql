-- DuckDB Schema Guard — ensure all required tables exist
-- Run at AM-1 startup or after container recycle
-- All statements use IF NOT EXISTS — safe to run repeatedly
-- Database: md:ps_analytics (MotherDuck cloud)
-- Assumes: USE ps_analytics has been called
-- Last updated: 2026-04-06 (schema migration: 8 schemas)

-- ============================================================
-- SCHEMAS
-- ============================================================
CREATE SCHEMA IF NOT EXISTS asana;
CREATE SCHEMA IF NOT EXISTS signals;
CREATE SCHEMA IF NOT EXISTS karpathy;
CREATE SCHEMA IF NOT EXISTS ns;
CREATE SCHEMA IF NOT EXISTS ops;
CREATE SCHEMA IF NOT EXISTS wiki;
CREATE SCHEMA IF NOT EXISTS ps;

-- ============================================================
-- SEQUENCES
-- ============================================================
CREATE SEQUENCE IF NOT EXISTS asana_audit_seq START 1;
CREATE SEQUENCE IF NOT EXISTS session_log_seq START 1;
CREATE SEQUENCE IF NOT EXISTS daily_tracker_seq START 1;
CREATE SEQUENCE IF NOT EXISTS karpathy_exp_seq START 1;

-- ============================================================
-- asana schema — task management & tracking
-- ============================================================

CREATE TABLE IF NOT EXISTS asana.asana_tasks (
    task_gid VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    assignee_gid VARCHAR,
    project_name VARCHAR,
    project_gid VARCHAR,
    section_name VARCHAR,
    due_on DATE,
    start_on DATE,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    deleted_at TIMESTAMP,
    routine_rw VARCHAR,
    priority_rw VARCHAR,
    importance_rw VARCHAR,
    kiro_rw VARCHAR,
    next_action_rw VARCHAR,
    begin_date_rw DATE,
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS asana.asana_task_history (
    snapshot_date DATE NOT NULL,
    task_gid VARCHAR NOT NULL,
    project_name VARCHAR,
    section_name VARCHAR,
    due_on DATE,
    completed BOOLEAN,
    priority_rw VARCHAR,
    routine_rw VARCHAR,
    PRIMARY KEY (snapshot_date, task_gid)
);

CREATE TABLE IF NOT EXISTS asana.asana_audit_log (
    id INTEGER PRIMARY KEY DEFAULT nextval('asana_audit_seq'),
    timestamp TIMESTAMP NOT NULL,
    tool VARCHAR NOT NULL,
    task_gid VARCHAR NOT NULL,
    task_name VARCHAR,
    project VARCHAR,
    pipeline_agent VARCHAR,
    pipeline_stage VARCHAR,
    fields_modified VARCHAR[],
    result VARCHAR NOT NULL,
    rule VARCHAR,
    context VARCHAR,
    notes VARCHAR
);

CREATE TABLE IF NOT EXISTS asana.daily_tracker (
    id INTEGER PRIMARY KEY DEFAULT nextval('daily_tracker_seq'),
    tracker_date DATE NOT NULL,
    completed_count INTEGER DEFAULT 0,
    carried_forward_count INTEGER DEFAULT 0,
    new_tasks_count INTEGER DEFAULT 0,
    net_delta INTEGER DEFAULT 0,
    bucket_sweep INTEGER,
    bucket_core INTEGER,
    bucket_engine INTEGER,
    bucket_admin INTEGER,
    bucket_backlog INTEGER,
    total_incomplete INTEGER,
    total_overdue INTEGER,
    l1_effort BOOLEAN DEFAULT FALSE,
    l2_effort BOOLEAN DEFAULT FALSE,
    l3_effort BOOLEAN DEFAULT FALSE,
    l4_effort BOOLEAN DEFAULT FALSE,
    l5_effort BOOLEAN DEFAULT FALSE,
    hard_thing_status VARCHAR,
    workdays_at_zero INTEGER,
    blocker_count INTEGER DEFAULT 0,
    abps_completed INTEGER DEFAULT 0,
    abps_advances INTEGER DEFAULT 0,
    portfolio_completed INTEGER DEFAULT 0,
    notes VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS asana.recurring_tasks (
    task_name VARCHAR NOT NULL,
    project_name VARCHAR NOT NULL,
    cadence VARCHAR NOT NULL,
    last_completed_date DATE,
    next_due_date DATE,
    total_instances INTEGER DEFAULT 0,
    on_time_instances INTEGER DEFAULT 0,
    compliance_rate DOUBLE DEFAULT 1.0,
    PRIMARY KEY (task_name, project_name)
);

CREATE TABLE IF NOT EXISTS asana.recurring_task_state (
    task_key VARCHAR PRIMARY KEY,
    cadence VARCHAR NOT NULL,
    last_run DATE,
    last_run_period VARCHAR,
    description VARCHAR,
    notes VARCHAR,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- signals schema — cross-channel intelligence
-- ============================================================

CREATE TABLE IF NOT EXISTS signals.signal_tracker (
    signal_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    topic VARCHAR NOT NULL,
    source_channel VARCHAR NOT NULL,
    source_author VARCHAR,
    source_id VARCHAR,
    first_seen TIMESTAMP NOT NULL,
    last_seen TIMESTAMP NOT NULL,
    signal_strength DOUBLE DEFAULT 1.0,
    reinforcement_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    decay_rate DOUBLE DEFAULT 0.1,
    content_preview VARCHAR,
    tags VARCHAR[]
);

CREATE TABLE IF NOT EXISTS signals.unified_signals (
    signal_id VARCHAR PRIMARY KEY,
    source_mcp VARCHAR NOT NULL,
    source_id VARCHAR NOT NULL,
    author VARCHAR,
    author_alias VARCHAR,
    timestamp TIMESTAMP NOT NULL,
    content_preview VARCHAR(500),
    signal_type VARCHAR NOT NULL,
    raw_priority INTEGER DEFAULT 0,
    computed_priority DOUBLE,
    cluster_id VARCHAR,
    disposition VARCHAR,
    disposition_task_gid VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS signals.signal_task_log (
    signal_source VARCHAR NOT NULL,
    signal_id VARCHAR NOT NULL,
    task_gid VARCHAR,
    action_taken VARCHAR NOT NULL,
    priority VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (signal_source, signal_id)
);

CREATE TABLE IF NOT EXISTS signals.slack_messages (
    ts VARCHAR,
    channel_id VARCHAR,
    channel_name VARCHAR,
    thread_ts VARCHAR,
    author_id VARCHAR,
    author_alias VARCHAR,
    author_name VARCHAR,
    text_preview VARCHAR,
    full_text VARCHAR,
    is_richard BOOLEAN,
    is_thread_reply BOOLEAN,
    reply_count INTEGER,
    reaction_count INTEGER,
    richard_reacted BOOLEAN,
    relevance_score INTEGER,
    signal_type VARCHAR,
    ingested_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS signals.slack_people (
    user_id VARCHAR PRIMARY KEY,
    alias VARCHAR,
    display_name VARCHAR,
    real_name VARCHAR,
    title VARCHAR,
    team VARCHAR,
    is_bot BOOLEAN DEFAULT FALSE,
    total_messages INTEGER DEFAULT 0,
    relationship_tier VARCHAR,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS signals.slack_threads (
    thread_ts VARCHAR NOT NULL,
    channel_id VARCHAR NOT NULL,
    channel_name VARCHAR,
    parent_author_id VARCHAR,
    reply_count INTEGER DEFAULT 0,
    participant_ids VARCHAR[],
    last_reply_ts VARCHAR,
    is_resolved BOOLEAN DEFAULT FALSE,
    topic VARCHAR,
    signal_type VARCHAR,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (thread_ts, channel_id)
);

CREATE TABLE IF NOT EXISTS signals.slack_topics (
    topic_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    message_ts VARCHAR NOT NULL,
    channel_id VARCHAR NOT NULL,
    topic VARCHAR NOT NULL,
    confidence DOUBLE,
    source VARCHAR DEFAULT 'extraction',
    is_actionable BOOLEAN DEFAULT FALSE,
    routed_to VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- karpathy schema — body system optimization
-- ============================================================

CREATE TABLE IF NOT EXISTS karpathy.autoresearch_experiments (
    id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL,
    run_date DATE NOT NULL,
    organ VARCHAR NOT NULL,
    section VARCHAR,
    technique VARCHAR NOT NULL,
    hypothesis VARCHAR,
    words_before INTEGER,
    words_after INTEGER,
    content_before_hash VARCHAR,
    content_after_hash VARCHAR,
    score_a DOUBLE,
    score_b DOUBLE,
    score_c DOUBLE,
    delta DOUBLE,
    result VARCHAR NOT NULL,
    revert_reason VARCHAR,
    duration_seconds INTEGER,
    model VARCHAR,
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    notes VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS karpathy.autoresearch_organ_health (
    organ VARCHAR NOT NULL,
    word_count INTEGER NOT NULL,
    accuracy_estimate DOUBLE,
    experiments_run INTEGER DEFAULT 0,
    experiments_kept INTEGER DEFAULT 0,
    last_experiment_date DATE,
    budget_signal VARCHAR,
    adaptive_budget INTEGER,
    snapshot_at TIMESTAMP NOT NULL,
    notes VARCHAR,
    PRIMARY KEY (organ, snapshot_at)
);

CREATE TABLE IF NOT EXISTS karpathy.autoresearch_priors (
    organ VARCHAR NOT NULL,
    technique VARCHAR NOT NULL,
    alpha DOUBLE NOT NULL DEFAULT 1.0,
    beta DOUBLE NOT NULL DEFAULT 1.0,
    n_experiments INTEGER DEFAULT 0,
    n_keeps INTEGER DEFAULT 0,
    n_reverts INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (organ, technique)
);

CREATE TABLE IF NOT EXISTS karpathy.body_size_history (
    measured_date DATE NOT NULL,
    organ_name VARCHAR NOT NULL,
    word_count INTEGER NOT NULL,
    add_prior_mean DOUBLE,
    compress_prior_mean DOUBLE,
    at_ceiling BOOLEAN DEFAULT FALSE,
    has_compression_signal BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (measured_date, organ_name)
);

CREATE TABLE IF NOT EXISTS karpathy.organ_word_counts (
    organ_name VARCHAR NOT NULL,
    measured_date DATE NOT NULL,
    word_count INTEGER NOT NULL,
    PRIMARY KEY (organ_name, measured_date)
);

CREATE TABLE IF NOT EXISTS karpathy.karpathy_experiment_log (
    id INTEGER PRIMARY KEY DEFAULT nextval('karpathy_exp_seq'),
    run_id INTEGER NOT NULL,
    run_date DATE NOT NULL,
    organ VARCHAR NOT NULL,
    section VARCHAR,
    operation VARCHAR NOT NULL,
    experiment_type VARCHAR,
    words_before INTEGER,
    words_after INTEGER,
    score_a DOUBLE,
    score_b DOUBLE,
    score_c DOUBLE,
    delta DOUBLE,
    duration_seconds INTEGER,
    result VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS karpathy.experiment_outcomes (
    outcome_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    experiment_id INTEGER NOT NULL,
    organ VARCHAR NOT NULL,
    technique VARCHAR NOT NULL,
    kept_date DATE NOT NULL,
    eval_date DATE,
    eval_window_days INTEGER DEFAULT 14,
    downstream_metric VARCHAR,
    baseline_score DOUBLE,
    lagged_score DOUBLE,
    delta DOUBLE,
    verdict VARCHAR,
    notes VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- ns schema — nervous system calibration loops
-- ============================================================

CREATE TABLE IF NOT EXISTS ns.ns_communication (
    week_start DATE NOT NULL,
    meeting_type VARCHAR NOT NULL,
    avg_speaking_share DOUBLE,
    avg_hedging_count DOUBLE,
    meeting_count INTEGER,
    visibility_score DOUBLE,
    coaching_signal BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (week_start, meeting_type)
);

CREATE TABLE IF NOT EXISTS ns.ns_decisions (
    decision_id VARCHAR NOT NULL PRIMARY KEY,
    decision_text VARCHAR NOT NULL,
    decision_date DATE,
    status VARCHAR NOT NULL,
    trigger_condition VARCHAR,
    trigger_date DATE,
    scored_date DATE,
    score_notes VARCHAR,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ns.ns_delegations (
    delegation_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    delegation_name VARCHAR NOT NULL,
    delegate_name VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    days_blocked INTEGER DEFAULT 0,
    first_detected DATE,
    last_checked DATE,
    notes VARCHAR,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ns.ns_loop_snapshots (
    snapshot_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    snapshot_date DATE NOT NULL,
    loop_id INTEGER NOT NULL,
    loop_name VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    metric_value DOUBLE,
    metric_name VARCHAR,
    details JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ns.ns_patterns (
    pattern_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    pattern_name VARCHAR NOT NULL,
    first_detected DATE NOT NULL,
    status VARCHAR NOT NULL,
    weeks_active INTEGER DEFAULT 1,
    gate_or_fix VARCHAR,
    escalated BOOLEAN DEFAULT FALSE,
    resolved_date DATE,
    notes VARCHAR,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ns.decisions (
    decision_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    decision_text VARCHAR NOT NULL,
    decision_date DATE NOT NULL,
    context VARCHAR,
    source VARCHAR,
    status VARCHAR DEFAULT 'PENDING',
    trigger_condition VARCHAR,
    trigger_date DATE,
    scored_date DATE,
    score VARCHAR,
    score_notes VARCHAR,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- ops schema — system operations & reliability
-- ============================================================

CREATE TABLE IF NOT EXISTS ops.hook_executions (
    execution_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    hook_name VARCHAR NOT NULL,
    execution_date DATE NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_seconds DOUBLE,
    phases_completed INTEGER DEFAULT 0,
    phases_failed INTEGER DEFAULT 0,
    asana_reads INTEGER DEFAULT 0,
    asana_writes INTEGER DEFAULT 0,
    slack_messages_sent INTEGER DEFAULT 0,
    duckdb_queries INTEGER DEFAULT 0,
    errors JSON,
    summary VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ops.workflow_executions (
    execution_id VARCHAR PRIMARY KEY,
    workflow_name VARCHAR NOT NULL,
    trigger_source VARCHAR,
    mcp_servers_involved VARCHAR[],
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status VARCHAR DEFAULT 'running',
    steps_completed INTEGER DEFAULT 0,
    steps_failed INTEGER DEFAULT 0,
    duration_seconds DOUBLE,
    error_details JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ops.session_log (
    id INTEGER PRIMARY KEY DEFAULT nextval('session_log_seq'),
    session_date DATE NOT NULL,
    topic VARCHAR NOT NULL,
    actions VARCHAR NOT NULL,
    decisions VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ops.intake_metrics (
    process_date DATE NOT NULL PRIMARY KEY,
    files_processed INTEGER DEFAULT 0,
    files_pending INTEGER DEFAULT 0,
    facts_extracted INTEGER DEFAULT 0,
    facts_routed JSON,
    duplicates_found INTEGER DEFAULT 0,
    archived INTEGER DEFAULT 0,
    processing_time_seconds INTEGER
);

CREATE TABLE IF NOT EXISTS ops.data_freshness (
    source_name VARCHAR NOT NULL,
    source_type VARCHAR NOT NULL,
    expected_cadence_hours INTEGER NOT NULL,
    last_updated TIMESTAMP,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_stale BOOLEAN DEFAULT FALSE,
    downstream_workflows VARCHAR[],
    PRIMARY KEY (source_name, source_type)
);

CREATE TABLE IF NOT EXISTS ops.builder_cache (
    cache_key VARCHAR PRIMARY KEY,
    source_tool VARCHAR NOT NULL,
    data JSON NOT NULL,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    stale_after_hours INTEGER DEFAULT 168
);

-- ============================================================
-- wiki schema — publishing pipeline
-- ============================================================

CREATE TABLE IF NOT EXISTS wiki.wiki_pipeline_runs (
    run_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    article_title VARCHAR NOT NULL,
    task_gid VARCHAR,
    stage VARCHAR NOT NULL,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    agent VARCHAR,
    critic_score DOUBLE,
    word_count INTEGER,
    revision_number INTEGER DEFAULT 1,
    notes VARCHAR
);

CREATE TABLE IF NOT EXISTS wiki.publication_registry (
    article_id VARCHAR PRIMARY KEY,
    article_title VARCHAR NOT NULL,
    local_path VARCHAR NOT NULL,
    sharepoint_url VARCHAR,
    xwiki_page_id VARCHAR,
    sharepoint_status VARCHAR DEFAULT 'pending',
    xwiki_status VARCHAR DEFAULT 'pending',
    sharepoint_last_published TIMESTAMP,
    xwiki_last_published TIMESTAMP,
    sync_status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- ps schema — Paid Search / Acquisition analytics
-- ============================================================

CREATE TABLE IF NOT EXISTS ps.markets (
    market_code     VARCHAR PRIMARY KEY,
    market_name     VARCHAR NOT NULL,
    currency_code   VARCHAR NOT NULL,
    region          VARCHAR NOT NULL,
    timezone        VARCHAR NOT NULL,
    hands_on        BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS ps.channels (
    channel_code    VARCHAR PRIMARY KEY,
    channel_name    VARCHAR NOT NULL,
    description     VARCHAR
);

CREATE TABLE IF NOT EXISTS ps.metrics (
    metric_id       VARCHAR DEFAULT uuid()::VARCHAR,
    market          VARCHAR NOT NULL,
    channel         VARCHAR NOT NULL,
    metric_name     VARCHAR NOT NULL,
    period_type     VARCHAR NOT NULL,
    period_key      VARCHAR NOT NULL,
    period_start    DATE NOT NULL,
    period_end      DATE NOT NULL,
    actual_value    DOUBLE,
    target_value    DOUBLE,
    prior_period    DOUBLE,
    prior_year      DOUBLE,
    currency_code   VARCHAR,
    unit            VARCHAR DEFAULT 'number',
    source          VARCHAR,
    notes           VARCHAR,
    updated_at      TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (market, channel, metric_name, period_type, period_key)
);

CREATE TABLE IF NOT EXISTS ps.targets (
    target_id       VARCHAR DEFAULT uuid()::VARCHAR,
    market          VARCHAR NOT NULL,
    channel         VARCHAR NOT NULL,
    metric_name     VARCHAR NOT NULL,
    fiscal_year     INTEGER NOT NULL,
    period_type     VARCHAR NOT NULL,
    period_key      VARCHAR NOT NULL,
    target_value    DOUBLE NOT NULL,
    stretch_value   DOUBLE,
    source          VARCHAR,
    approved_by     VARCHAR,
    set_date        DATE,
    notes           VARCHAR,
    PRIMARY KEY (market, channel, metric_name, period_type, period_key)
);

CREATE TABLE IF NOT EXISTS ps.forecasts (
    forecast_id     VARCHAR DEFAULT uuid()::VARCHAR,
    market          VARCHAR NOT NULL,
    channel         VARCHAR NOT NULL,
    metric_name     VARCHAR NOT NULL,
    forecast_date   DATE NOT NULL,
    target_period   VARCHAR NOT NULL,
    period_type     VARCHAR NOT NULL,
    predicted_value DOUBLE NOT NULL,
    confidence_low  DOUBLE,
    confidence_high DOUBLE,
    method          VARCHAR,
    actual_value    DOUBLE,
    error_pct       DOUBLE,
    scored          BOOLEAN DEFAULT FALSE,
    score           VARCHAR,
    notes           VARCHAR,
    lead_weeks      INT,
    prediction_run_id VARCHAR,
    created_at      TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS ps.pacing (
    pacing_id       VARCHAR DEFAULT uuid()::VARCHAR,
    market          VARCHAR NOT NULL,
    channel         VARCHAR NOT NULL,
    metric_name     VARCHAR NOT NULL,
    period_type     VARCHAR NOT NULL,
    period_key      VARCHAR NOT NULL,
    snapshot_date   DATE NOT NULL,
    days_elapsed    INTEGER NOT NULL,
    days_remaining  INTEGER NOT NULL,
    actual_to_date  DOUBLE,
    run_rate        DOUBLE,
    target_value    DOUBLE,
    pacing_pct      DOUBLE,
    status          VARCHAR,
    updated_at      TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (market, channel, metric_name, period_type, period_key, snapshot_date)
);

CREATE TABLE IF NOT EXISTS ps.accounts (
    account_id      VARCHAR NOT NULL,
    market          VARCHAR NOT NULL,
    channel         VARCHAR NOT NULL,
    platform        VARCHAR NOT NULL,
    account_name    VARCHAR,
    account_type    VARCHAR,
    status          VARCHAR DEFAULT 'active',
    monthly_budget  DOUBLE,
    currency_code   VARCHAR,
    notes           VARCHAR,
    PRIMARY KEY (account_id, platform)
);

CREATE TABLE IF NOT EXISTS ps.account_metrics (
    market          VARCHAR NOT NULL,
    account_id      VARCHAR NOT NULL,
    platform        VARCHAR NOT NULL,
    period_type     VARCHAR NOT NULL,
    period_key      VARCHAR NOT NULL,
    impressions     BIGINT,
    clicks          BIGINT,
    spend           DOUBLE,
    conversions     DOUBLE,
    revenue         DOUBLE,
    ctr             DOUBLE,
    cpc             DOUBLE,
    cpa             DOUBLE,
    cvr             DOUBLE,
    roas            DOUBLE,
    impression_share DOUBLE,
    currency_code   VARCHAR,
    updated_at      TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (market, account_id, platform, period_type, period_key)
);

CREATE TABLE IF NOT EXISTS ps.dashboard_uploads (
    upload_id       VARCHAR DEFAULT uuid()::VARCHAR,
    file_name       VARCHAR NOT NULL,
    week_ending     DATE NOT NULL,
    uploaded_at     TIMESTAMP DEFAULT current_timestamp,
    row_count       INTEGER,
    markets_found   VARCHAR[],
    channels_found  VARCHAR[],
    status          VARCHAR DEFAULT 'pending',
    error_message   VARCHAR,
    notes           VARCHAR
);

CREATE TABLE IF NOT EXISTS ps.change_log (
    id INTEGER NOT NULL,
    market VARCHAR NOT NULL,
    date DATE NOT NULL,
    category VARCHAR,
    description VARCHAR,
    impact_metric VARCHAR,
    impact_value DOUBLE,
    source VARCHAR,
    ingested_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ps.competitive_signals (
    signal_id VARCHAR PRIMARY KEY,
    competitor_name VARCHAR NOT NULL,
    market VARCHAR,
    source_type VARCHAR NOT NULL,
    source_id VARCHAR,
    content VARCHAR,
    metric_change DOUBLE,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ps.projections (
    projection_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    metric_name VARCHAR NOT NULL,
    market VARCHAR,
    projection_date DATE NOT NULL,
    target_date DATE NOT NULL,
    predicted_value DOUBLE NOT NULL,
    actual_value DOUBLE,
    confidence_low DOUBLE,
    confidence_high DOUBLE,
    method VARCHAR,
    scored BOOLEAN DEFAULT FALSE,
    score VARCHAR,
    error_pct DOUBLE,
    source VARCHAR,
    notes VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ps.health_alerts (
    alert_id VARCHAR PRIMARY KEY,
    alert_type VARCHAR NOT NULL,
    market VARCHAR,
    severity VARCHAR NOT NULL,
    message VARCHAR NOT NULL,
    context_data JSON,
    slack_context VARCHAR,
    acknowledged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- main schema — personal productivity, cross-cutting
-- ============================================================

CREATE TABLE IF NOT EXISTS main.five_levels_weekly (
    week_start DATE NOT NULL,
    level INTEGER NOT NULL,
    level_name VARCHAR NOT NULL,
    tasks_completed INTEGER DEFAULT 0,
    tasks_active INTEGER DEFAULT 0,
    hours_estimated DOUBLE DEFAULT 0,
    artifacts_shipped INTEGER DEFAULT 0,
    streak_weeks INTEGER DEFAULT 0,
    notes VARCHAR,
    PRIMARY KEY (week_start, level)
);

CREATE TABLE IF NOT EXISTS main.l1_streak (
    tracker_date DATE PRIMARY KEY,
    workdays_at_zero INTEGER NOT NULL,
    artifact_shipped BOOLEAN DEFAULT FALSE,
    artifact_name VARCHAR,
    hard_thing_task_gid VARCHAR,
    hard_thing_name VARCHAR,
    notes VARCHAR
);

CREATE TABLE IF NOT EXISTS main.meeting_analytics (
    session_id VARCHAR PRIMARY KEY,
    meeting_name VARCHAR NOT NULL,
    meeting_date DATE NOT NULL,
    duration_minutes INTEGER,
    participant_count INTEGER,
    action_item_count INTEGER,
    richard_speaking_share DOUBLE,
    hedging_count INTEGER DEFAULT 0,
    meeting_type VARCHAR,
    topics_discussed VARCHAR[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS main.meeting_highlights (
    highlight_id VARCHAR PRIMARY KEY,
    session_id VARCHAR NOT NULL,
    highlight_type VARCHAR NOT NULL,
    content TEXT NOT NULL,
    speaker VARCHAR,
    timestamp_offset INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS main.meeting_series (
    series_id VARCHAR PRIMARY KEY,
    meeting_name VARCHAR NOT NULL,
    cadence VARCHAR,
    folder VARCHAR,
    file_path VARCHAR NOT NULL,
    hedy_topic_id VARCHAR,
    attendees VARCHAR[],
    last_session_date DATE,
    open_item_count INTEGER DEFAULT 0,
    running_themes VARCHAR[],
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS main.relationship_activity (
    person_name VARCHAR NOT NULL,
    person_alias VARCHAR NOT NULL,
    week DATE NOT NULL,
    slack_interactions INTEGER DEFAULT 0,
    email_exchanges INTEGER DEFAULT 0,
    meetings_shared INTEGER DEFAULT 0,
    asana_collaborations INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0,
    interaction_trend VARCHAR,
    PRIMARY KEY (person_alias, week)
);

CREATE TABLE IF NOT EXISTS main.content_embeddings (
    embedding_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    source_type VARCHAR NOT NULL,
    source_id VARCHAR NOT NULL,
    content_preview VARCHAR,
    embedding FLOAT[384],
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS main.experiments (
    experiment_id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    experiment_name VARCHAR NOT NULL,
    hypothesis VARCHAR,
    status VARCHAR DEFAULT 'proposed',
    start_date DATE,
    end_date DATE,
    metric_name VARCHAR,
    baseline_value DOUBLE,
    result_value DOUBLE,
    outcome VARCHAR,
    notes VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
