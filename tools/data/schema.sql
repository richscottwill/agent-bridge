-- PS Analytics Schema Export
-- Generated: 2026-03-30T23:51:33.020095
-- Source: /home/prichwil/shared/tools/data/ps-analytics.duckdb

CREATE TABLE agent_actions(id INTEGER PRIMARY KEY, agent VARCHAR, action_type VARCHAR, market VARCHAR, "week" VARCHAR, description VARCHAR, input_summary VARCHAR, output_summary VARCHAR, confidence DOUBLE, requires_human_review BOOLEAN, reviewed_by_human BOOLEAN, human_feedback VARCHAR, created_at TIMESTAMP DEFAULT(current_timestamp));;

-- agent_actions: 0 rows as of export

CREATE TABLE agent_observations(id INTEGER PRIMARY KEY, agent VARCHAR, observation_type VARCHAR, market VARCHAR, "week" VARCHAR, "content" VARCHAR, severity VARCHAR, acted_on BOOLEAN, acted_on_by VARCHAR, created_at TIMESTAMP DEFAULT(current_timestamp));;

-- agent_observations: 0 rows as of export

CREATE TABLE anomalies(id INTEGER PRIMARY KEY, market VARCHAR NOT NULL, "week" VARCHAR NOT NULL, metric VARCHAR NOT NULL, "value" DOUBLE, baseline DOUBLE, deviation_pct DOUBLE, direction VARCHAR, flagged_at TIMESTAMP DEFAULT(current_timestamp), resolved BOOLEAN DEFAULT(CAST('f' AS BOOLEAN)), notes VARCHAR, CHECK((deviation_pct != 0)));;

-- anomalies: 0 rows as of export

CREATE TABLE callout_scores(market VARCHAR, "week" VARCHAR, overall_score DOUBLE, headline_clarity DOUBLE, narrative_justification DOUBLE, conciseness DOUBLE, actionability DOUBLE, voice DOUBLE, word_count INTEGER, reviewer_notes VARCHAR, ingested_at TIMESTAMP DEFAULT(current_timestamp), CHECK((overall_score BETWEEN 0 AND 10)), CHECK((headline_clarity BETWEEN 0 AND 10)), CHECK((narrative_justification BETWEEN 0 AND 10)), CHECK((conciseness BETWEEN 0 AND 10)), CHECK((actionability BETWEEN 0 AND 10)), CHECK((voice BETWEEN 0 AND 10)), PRIMARY KEY(market, "week"));;

-- callout_scores: 0 rows as of export

CREATE TABLE change_log(id INTEGER PRIMARY KEY, market VARCHAR NOT NULL, date DATE NOT NULL, category VARCHAR, description VARCHAR, impact_metric VARCHAR, impact_value DOUBLE, "source" VARCHAR, ingested_at TIMESTAMP DEFAULT(current_timestamp));;

-- change_log: 477 rows as of export

CREATE TABLE competitors(market VARCHAR, competitor VARCHAR, "week" VARCHAR, impression_share DOUBLE, cpc_impact_pct DOUBLE, segment VARCHAR, notes VARCHAR, ingested_at TIMESTAMP DEFAULT(current_timestamp), CHECK((impression_share BETWEEN 0 AND 100)), PRIMARY KEY(market, competitor, "week"));;

-- competitors: 14 rows as of export

CREATE TABLE daily_metrics(market VARCHAR, date DATE, "week" VARCHAR, "month" VARCHAR, "cost" DOUBLE, clicks INTEGER, impressions INTEGER, regs INTEGER, cpa DOUBLE, cpc DOUBLE, cvr DOUBLE, ctr DOUBLE, brand_cost DOUBLE, brand_clicks INTEGER, brand_imp INTEGER, brand_regs INTEGER, brand_cpa DOUBLE, brand_cpc DOUBLE, brand_cvr DOUBLE, nb_cost DOUBLE, nb_clicks INTEGER, nb_imp INTEGER, nb_regs INTEGER, nb_cpa DOUBLE, nb_cpc DOUBLE, nb_cvr DOUBLE, ingested_at TIMESTAMP DEFAULT(current_timestamp), source_file VARCHAR, PRIMARY KEY(market, date));;

-- daily_metrics: 10502 rows as of export

CREATE TABLE decisions(id INTEGER PRIMARY KEY, decision_type VARCHAR, market VARCHAR, description VARCHAR, rationale VARCHAR, made_by VARCHAR, approved_by VARCHAR, approval_required BOOLEAN, status VARCHAR, outcome VARCHAR, created_at TIMESTAMP DEFAULT(current_timestamp), resolved_at TIMESTAMP);;

-- decisions: 0 rows as of export

CREATE TABLE experiments(experiment_id VARCHAR, "name" VARCHAR, hypothesis VARCHAR, start_date DATE, end_date DATE, status VARCHAR, result VARCHAR, metric_before DOUBLE, metric_after DOUBLE, effect_size DOUBLE, decision VARCHAR, ingested_at TIMESTAMP DEFAULT(current_timestamp), PRIMARY KEY(experiment_id));;

-- experiments: 0 rows as of export

CREATE TABLE ieccp(market VARCHAR, "week" VARCHAR, "value" DOUBLE, ingested_at TIMESTAMP DEFAULT(current_timestamp), PRIMARY KEY(market, "week"));;

-- ieccp: 9 rows as of export

CREATE TABLE ingest_log(id INTEGER PRIMARY KEY, source_file VARCHAR, ingested_at TIMESTAMP DEFAULT(current_timestamp), markets_processed VARCHAR, target_week VARCHAR, rows_daily INTEGER, rows_weekly INTEGER, rows_monthly INTEGER, duration_seconds DOUBLE);;

-- ingest_log: 1 rows as of export

CREATE TABLE monthly_metrics(market VARCHAR, "month" VARCHAR, spend DOUBLE, regs INTEGER, cpa DOUBLE, clicks INTEGER, impressions INTEGER, cpc DOUBLE, cvr DOUBLE, ctr DOUBLE, brand_spend DOUBLE, brand_regs INTEGER, brand_cpa DOUBLE, brand_clicks INTEGER, brand_impressions INTEGER, nb_spend DOUBLE, nb_regs INTEGER, nb_cpa DOUBLE, nb_clicks INTEGER, nb_impressions INTEGER, spend_op2 DOUBLE, regs_op2 INTEGER, cpa_op2 DOUBLE, clicks_op2 INTEGER, impressions_op2 INTEGER, ingested_at TIMESTAMP DEFAULT(current_timestamp), source_file VARCHAR, PRIMARY KEY(market, "month"));;

-- monthly_metrics: 66 rows as of export

CREATE TABLE oci_status(market VARCHAR PRIMARY KEY, status VARCHAR, launch_date DATE, full_impact_date DATE, reg_lift_pct DOUBLE, cpa_improvement VARCHAR, notes VARCHAR, updated_at TIMESTAMP DEFAULT(current_timestamp));;

-- oci_status: 10 rows as of export

CREATE TABLE projections(market VARCHAR, "week" VARCHAR, "month" VARCHAR, days_elapsed INTEGER, total_days INTEGER, projected_regs INTEGER, projected_spend DOUBLE, projected_cpa DOUBLE, actual_regs INTEGER, actual_spend DOUBLE, actual_cpa DOUBLE, op2_regs INTEGER, op2_spend DOUBLE, vs_op2_regs_pct DOUBLE, vs_op2_spend_pct DOUBLE, error_pct DOUBLE, rationale VARCHAR, "source" VARCHAR, ingested_at TIMESTAMP DEFAULT(current_timestamp), CHECK((projected_regs > 0)), PRIMARY KEY(market, "week"));;

-- projections: 10 rows as of export

CREATE TABLE task_queue(id INTEGER PRIMARY KEY, task_type VARCHAR, market VARCHAR, description VARCHAR, priority INTEGER, assigned_to VARCHAR, status VARCHAR, created_by VARCHAR, created_at TIMESTAMP DEFAULT(current_timestamp), completed_at TIMESTAMP, result VARCHAR);;

-- task_queue: 0 rows as of export

CREATE TABLE weekly_metrics(market VARCHAR, "week" VARCHAR, date_range VARCHAR, num_days INTEGER, "cost" DOUBLE, clicks INTEGER, impressions INTEGER, regs INTEGER, cpa DOUBLE, cpc DOUBLE, cvr DOUBLE, ctr DOUBLE, brand_cost DOUBLE, brand_clicks INTEGER, brand_imp INTEGER, brand_regs INTEGER, brand_cpa DOUBLE, brand_cpc DOUBLE, brand_cvr DOUBLE, nb_cost DOUBLE, nb_clicks INTEGER, nb_imp INTEGER, nb_regs INTEGER, nb_cpa DOUBLE, nb_cpc DOUBLE, nb_cvr DOUBLE, ingested_at TIMESTAMP DEFAULT(current_timestamp), source_file VARCHAR, PRIMARY KEY(market, "week"));;

-- weekly_metrics: 510 rows as of export


-- ============================================================
-- Slack Deep Context: Conversation Database
-- Added: 2026-04-01
-- Spec: .kiro/specs/slack-deep-context/
-- ============================================================

CREATE TABLE slack_messages(
    ts VARCHAR PRIMARY KEY,
    channel_id VARCHAR NOT NULL,
    channel_name VARCHAR,
    thread_ts VARCHAR,
    author_id VARCHAR NOT NULL,
    author_alias VARCHAR,
    author_name VARCHAR,
    text_preview VARCHAR,
    full_text VARCHAR,
    is_richard BOOLEAN DEFAULT(CAST('f' AS BOOLEAN)),
    is_thread_reply BOOLEAN DEFAULT(CAST('f' AS BOOLEAN)),
    reply_count INTEGER DEFAULT(0),
    reaction_count INTEGER DEFAULT(0),
    richard_reacted BOOLEAN DEFAULT(CAST('f' AS BOOLEAN)),
    relevance_score INTEGER,
    signal_type VARCHAR,
    ingested_at TIMESTAMP DEFAULT(current_timestamp));;

-- slack_messages: 0 rows as of schema creation

CREATE TABLE slack_threads(
    thread_ts VARCHAR PRIMARY KEY,
    channel_id VARCHAR NOT NULL,
    channel_name VARCHAR,
    topic_summary VARCHAR,
    participant_aliases VARCHAR,
    message_count INTEGER,
    decision_extracted VARCHAR,
    action_items VARCHAR,
    first_ts TIMESTAMP,
    last_ts TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT(current_timestamp));;

-- slack_threads: 0 rows as of schema creation

CREATE TABLE slack_people(
    user_id VARCHAR PRIMARY KEY,
    alias VARCHAR,
    display_name VARCHAR,
    first_interaction DATE,
    last_interaction DATE,
    total_messages INTEGER DEFAULT(0),
    dm_messages INTEGER DEFAULT(0),
    channel_messages INTEGER DEFAULT(0),
    channels_shared INTEGER DEFAULT(0),
    avg_response_time_hours DOUBLE,
    relationship_tier VARCHAR,
    ingested_at TIMESTAMP DEFAULT(current_timestamp));;

-- slack_people: 0 rows as of schema creation

CREATE TABLE slack_topics(
    topic VARCHAR,
    "week" VARCHAR,
    channel_count INTEGER,
    message_count INTEGER,
    participant_count INTEGER,
    key_participants VARCHAR,
    status VARCHAR DEFAULT('active'),
    related_project VARCHAR,
    ingested_at TIMESTAMP DEFAULT(current_timestamp),
    PRIMARY KEY(topic, "week"));;

-- slack_topics: 0 rows as of schema creation
