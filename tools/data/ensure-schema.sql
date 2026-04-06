-- DuckDB Schema Guard — ensure all required tables exist
-- Run at AM-1 startup or after container recycle
-- All statements use IF NOT EXISTS — safe to run repeatedly
-- Database: md:ps_analytics (MotherDuck cloud)
-- Last updated: 2026-04-06

-- ============================================================
-- SEQUENCES
-- ============================================================
CREATE SEQUENCE IF NOT EXISTS asana_audit_seq START 1;
CREATE SEQUENCE IF NOT EXISTS session_log_seq START 1;
CREATE SEQUENCE IF NOT EXISTS daily_tracker_seq START 1;
CREATE SEQUENCE IF NOT EXISTS karpathy_exp_seq START 1;

-- ============================================================
-- CORE SIGNAL & COMMUNICATION TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS signal_task_log (
    signal_source VARCHAR NOT NULL,
    signal_id VARCHAR NOT NULL,
    task_gid VARCHAR,
    action_taken VARCHAR NOT NULL,
    priority VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (signal_source, signal_id)
);

CREATE TABLE IF NOT EXISTS unified_signals (
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

CREATE TABLE IF NOT EXISTS competitive_signals (
    signal_id VARCHAR PRIMARY KEY,
    competitor_name VARCHAR NOT NULL,
    market VARCHAR,
    source_type VARCHAR NOT NULL,
    source_id VARCHAR,
    content VARCHAR,
    metric_change DOUBLE,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- MEETING & COMMUNICATION TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS meeting_analytics (
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

CREATE TABLE IF NOT EXISTS meeting_highlights (
    highlight_id VARCHAR PRIMARY KEY,
    session_id VARCHAR NOT NULL,
    highlight_type VARCHAR NOT NULL,
    content TEXT NOT NULL,
    speaker VARCHAR,
    timestamp_offset INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS meeting_series (
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


-- ============================================================
-- ASANA STATE TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS asana_tasks (
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

CREATE TABLE IF NOT EXISTS asana_task_history (
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

CREATE TABLE IF NOT EXISTS asana_audit_log (
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

-- ============================================================
-- MONITORING & HEALTH TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS data_freshness (
    source_name VARCHAR NOT NULL,
    source_type VARCHAR NOT NULL,
    expected_cadence_hours INTEGER NOT NULL,
    last_updated TIMESTAMP,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_stale BOOLEAN DEFAULT FALSE,
    downstream_workflows VARCHAR[],
    PRIMARY KEY (source_name, source_type)
);

CREATE TABLE IF NOT EXISTS health_alerts (
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

CREATE TABLE IF NOT EXISTS workflow_executions (
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

CREATE TABLE IF NOT EXISTS hook_executions (
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

-- ============================================================
-- PROJECTIONS & FORECASTING
-- ============================================================

CREATE TABLE IF NOT EXISTS projections (
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

-- ============================================================
-- EXPERIMENT & RESEARCH TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS experiment_outcomes (
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

CREATE TABLE IF NOT EXISTS karpathy_experiment_log (
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

-- ============================================================
-- NERVOUS SYSTEM TIME SERIES
-- ============================================================

CREATE TABLE IF NOT EXISTS ns_loop_snapshots (
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

CREATE TABLE IF NOT EXISTS ns_patterns (
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

CREATE TABLE IF NOT EXISTS ns_delegations (
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

CREATE TABLE IF NOT EXISTS ns_decisions (
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

CREATE TABLE IF NOT EXISTS ns_communication (
    week_start DATE NOT NULL,
    meeting_type VARCHAR NOT NULL,
    avg_speaking_share DOUBLE,
    avg_hedging_count DOUBLE,
    meeting_count INTEGER,
    visibility_score DOUBLE,
    coaching_signal BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (week_start, meeting_type)
);

-- ============================================================
-- FIVE LEVELS & TRACKING
-- ============================================================

CREATE TABLE IF NOT EXISTS five_levels_weekly (
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

CREATE TABLE IF NOT EXISTS l1_streak (
    tracker_date DATE PRIMARY KEY,
    workdays_at_zero INTEGER NOT NULL,
    artifact_shipped BOOLEAN DEFAULT FALSE,
    artifact_name VARCHAR,
    hard_thing_task_gid VARCHAR,
    hard_thing_name VARCHAR,
    notes VARCHAR
);

CREATE TABLE IF NOT EXISTS daily_tracker (
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

CREATE TABLE IF NOT EXISTS session_log (
    id INTEGER PRIMARY KEY DEFAULT nextval('session_log_seq'),
    session_date DATE NOT NULL,
    topic VARCHAR NOT NULL,
    actions VARCHAR NOT NULL,
    decisions VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- BODY HEALTH & COMPRESSION
-- ============================================================

CREATE TABLE IF NOT EXISTS body_size_history (
    measured_date DATE NOT NULL,
    organ_name VARCHAR NOT NULL,
    word_count INTEGER NOT NULL,
    add_prior_mean DOUBLE,
    compress_prior_mean DOUBLE,
    at_ceiling BOOLEAN DEFAULT FALSE,
    has_compression_signal BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (measured_date, organ_name)
);

CREATE TABLE IF NOT EXISTS organ_word_counts (
    organ_name VARCHAR NOT NULL,
    measured_date DATE NOT NULL,
    word_count INTEGER NOT NULL,
    PRIMARY KEY (organ_name, measured_date)
);

CREATE TABLE IF NOT EXISTS intake_metrics (
    process_date DATE NOT NULL PRIMARY KEY,
    files_processed INTEGER DEFAULT 0,
    files_pending INTEGER DEFAULT 0,
    facts_extracted INTEGER DEFAULT 0,
    facts_routed JSON,
    duplicates_found INTEGER DEFAULT 0,
    archived INTEGER DEFAULT 0,
    processing_time_seconds INTEGER
);

-- ============================================================
-- KNOWLEDGE & PUBLISHING
-- ============================================================

CREATE TABLE IF NOT EXISTS publication_registry (
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

CREATE TABLE IF NOT EXISTS wiki_pipeline_runs (
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

CREATE TABLE IF NOT EXISTS builder_cache (
    cache_key VARCHAR PRIMARY KEY,
    source_tool VARCHAR NOT NULL,
    data JSON NOT NULL,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    stale_after_hours INTEGER DEFAULT 168
);

-- ============================================================
-- RELATIONSHIP & RECURRING
-- ============================================================

CREATE TABLE IF NOT EXISTS relationship_activity (
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

CREATE TABLE IF NOT EXISTS recurring_tasks (
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

CREATE TABLE IF NOT EXISTS recurring_task_state (
    task_key VARCHAR PRIMARY KEY,
    cadence VARCHAR NOT NULL,
    last_run DATE,
    last_run_period VARCHAR,
    description VARCHAR,
    notes VARCHAR,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
