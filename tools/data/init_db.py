#!/usr/bin/env python3
"""
Initialize the PS Analytics DuckDB database.

Creates the schema for all structured data in the paid search system.
Safe to run multiple times — uses CREATE TABLE IF NOT EXISTS.

Usage:
    python3 init_db.py [--path PATH]

Default path: ~/shared/tools/data/ps-analytics.duckdb
"""

import duckdb
import argparse
import os

DEFAULT_DB_PATH = os.path.expanduser('~/shared/tools/data/ps-analytics.duckdb')


def _recreate_with_constraints(con, table_name, create_sql):
    """Recreate a table with CHECK constraints if it exists without them.

    DuckDB doesn't support ALTER TABLE ADD CONSTRAINT for CHECK constraints.
    If the table exists but lacks CHECK constraints (created before this update),
    we recreate it: backup data → drop → create with constraints → restore data.
    Skips recreation if the table already has CHECK constraints or is empty/new.
    """
    # Check if table exists
    exists = con.execute(
        f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}'"
    ).fetchone()[0]
    if not exists:
        return  # Table will be created fresh with constraints by the main CREATE

    # Check if table already has CHECK constraints
    constraints = con.execute(
        f"SELECT COUNT(*) FROM duckdb_constraints() WHERE table_name = '{table_name}' AND constraint_type = 'CHECK'"
    ).fetchone()[0]
    if constraints > 0:
        return  # Already has CHECK constraints

    # Recreate: backup → drop → create with constraints → restore
    row_count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    backup_table = f"_{table_name}_backup"
    con.execute(f"CREATE TEMPORARY TABLE {backup_table} AS SELECT * FROM {table_name}")
    con.execute(f"DROP TABLE {table_name}")
    con.execute(create_sql)
    if row_count > 0:
        con.execute(f"INSERT INTO {table_name} SELECT * FROM {backup_table}")
    con.execute(f"DROP TABLE {backup_table}")


def init_db(db_path=None):
    if db_path is None:
        db_path = DEFAULT_DB_PATH

    con = duckdb.connect(db_path)

    # ── Daily metrics: one row per market per day ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS daily_metrics (
            market VARCHAR NOT NULL,
            date DATE NOT NULL,
            week VARCHAR,
            month VARCHAR,
            -- Totals
            cost DOUBLE,
            clicks INTEGER,
            impressions INTEGER,
            regs INTEGER,
            cpa DOUBLE,
            cpc DOUBLE,
            cvr DOUBLE,
            ctr DOUBLE,
            -- Brand
            brand_cost DOUBLE,
            brand_clicks INTEGER,
            brand_imp INTEGER,
            brand_regs INTEGER,
            brand_cpa DOUBLE,
            brand_cpc DOUBLE,
            brand_cvr DOUBLE,
            -- Non-Brand
            nb_cost DOUBLE,
            nb_clicks INTEGER,
            nb_imp INTEGER,
            nb_regs INTEGER,
            nb_cpa DOUBLE,
            nb_cpc DOUBLE,
            nb_cvr DOUBLE,
            -- Metadata
            ingested_at TIMESTAMP DEFAULT current_timestamp,
            source_file VARCHAR,
            PRIMARY KEY (market, date)
        )
    """)

    # ── Weekly metrics: one row per market per week ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS weekly_metrics (
            market VARCHAR NOT NULL,
            week VARCHAR NOT NULL,
            date_range VARCHAR,
            num_days INTEGER,
            -- Totals
            cost DOUBLE,
            clicks INTEGER,
            impressions INTEGER,
            regs INTEGER,
            cpa DOUBLE,
            cpc DOUBLE,
            cvr DOUBLE,
            ctr DOUBLE,
            -- Brand
            brand_cost DOUBLE,
            brand_clicks INTEGER,
            brand_imp INTEGER,
            brand_regs INTEGER,
            brand_cpa DOUBLE,
            brand_cpc DOUBLE,
            brand_cvr DOUBLE,
            -- Non-Brand
            nb_cost DOUBLE,
            nb_clicks INTEGER,
            nb_imp INTEGER,
            nb_regs INTEGER,
            nb_cpa DOUBLE,
            nb_cpc DOUBLE,
            nb_cvr DOUBLE,
            -- Metadata
            ingested_at TIMESTAMP DEFAULT current_timestamp,
            source_file VARCHAR,
            PRIMARY KEY (market, week)
        )
    """)

    # ── Monthly metrics: one row per market per month ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS monthly_metrics (
            market VARCHAR NOT NULL,
            month VARCHAR NOT NULL,
            -- Actuals (totals)
            spend DOUBLE,
            regs INTEGER,
            cpa DOUBLE,
            clicks INTEGER,
            impressions INTEGER,
            cpc DOUBLE,
            cvr DOUBLE,
            ctr DOUBLE,
            -- Actuals (Brand)
            brand_spend DOUBLE,
            brand_regs INTEGER,
            brand_cpa DOUBLE,
            brand_clicks INTEGER,
            brand_impressions INTEGER,
            -- Actuals (NB)
            nb_spend DOUBLE,
            nb_regs INTEGER,
            nb_cpa DOUBLE,
            nb_clicks INTEGER,
            nb_impressions INTEGER,
            -- OP2 targets
            spend_op2 DOUBLE,
            regs_op2 INTEGER,
            cpa_op2 DOUBLE,
            clicks_op2 INTEGER,
            impressions_op2 INTEGER,
            -- Metadata
            ingested_at TIMESTAMP DEFAULT current_timestamp,
            source_file VARCHAR,
            PRIMARY KEY (market, month)
        )
    """)

    # ── IECCP: one row per market per week ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS ieccp (
            market VARCHAR NOT NULL,
            week VARCHAR NOT NULL,
            value DOUBLE,
            ingested_at TIMESTAMP DEFAULT current_timestamp,
            PRIMARY KEY (market, week)
        )
    """)

    # ── Projections: one row per market per week ──
    PROJECTIONS_SQL = """
        CREATE TABLE IF NOT EXISTS projections (
            market VARCHAR NOT NULL,
            week VARCHAR NOT NULL,
            month VARCHAR,
            days_elapsed INTEGER,
            total_days INTEGER,
            projected_regs INTEGER CHECK (projected_regs > 0),
            projected_spend DOUBLE,
            projected_cpa DOUBLE,
            actual_regs INTEGER,
            actual_spend DOUBLE,
            actual_cpa DOUBLE,
            op2_regs INTEGER,
            op2_spend DOUBLE,
            vs_op2_regs_pct DOUBLE,
            vs_op2_spend_pct DOUBLE,
            error_pct DOUBLE,
            rationale TEXT,
            source VARCHAR,
            ingested_at TIMESTAMP DEFAULT current_timestamp,
            PRIMARY KEY (market, week)
        )
    """
    _recreate_with_constraints(con, 'projections', PROJECTIONS_SQL)
    con.execute(PROJECTIONS_SQL)

    # ── Callout scores: one row per market per week ──
    CALLOUT_SCORES_SQL = """
        CREATE TABLE IF NOT EXISTS callout_scores (
            market VARCHAR NOT NULL,
            week VARCHAR NOT NULL,
            overall_score DOUBLE CHECK (overall_score BETWEEN 0 AND 10),
            headline_clarity DOUBLE CHECK (headline_clarity BETWEEN 0 AND 10),
            narrative_justification DOUBLE CHECK (narrative_justification BETWEEN 0 AND 10),
            conciseness DOUBLE CHECK (conciseness BETWEEN 0 AND 10),
            actionability DOUBLE CHECK (actionability BETWEEN 0 AND 10),
            voice DOUBLE CHECK (voice BETWEEN 0 AND 10),
            word_count INTEGER,
            reviewer_notes TEXT,
            ingested_at TIMESTAMP DEFAULT current_timestamp,
            PRIMARY KEY (market, week)
        )
    """
    _recreate_with_constraints(con, 'callout_scores', CALLOUT_SCORES_SQL)
    con.execute(CALLOUT_SCORES_SQL)

    # ── Experiment results: one row per experiment ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            experiment_id VARCHAR NOT NULL,
            name VARCHAR,
            hypothesis TEXT,
            start_date DATE,
            end_date DATE,
            status VARCHAR,
            result TEXT,
            metric_before DOUBLE,
            metric_after DOUBLE,
            effect_size DOUBLE,
            decision VARCHAR,
            ingested_at TIMESTAMP DEFAULT current_timestamp,
            PRIMARY KEY (experiment_id)
        )
    """)

    # ── Ingest log: tracks what files were processed ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS ingest_log (
            id INTEGER PRIMARY KEY,
            source_file VARCHAR,
            ingested_at TIMESTAMP DEFAULT current_timestamp,
            markets_processed VARCHAR,
            target_week VARCHAR,
            rows_daily INTEGER,
            rows_weekly INTEGER,
            rows_monthly INTEGER,
            duration_seconds DOUBLE
        )
    """)
    # Auto-increment for ingest_log
    con.execute("""
        CREATE SEQUENCE IF NOT EXISTS ingest_log_seq START 1
    """)

    # ── Change log: replaces per-market {market}-change-log.md structured entries ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS change_log (
            id INTEGER PRIMARY KEY,
            market VARCHAR NOT NULL,
            date DATE NOT NULL,
            category VARCHAR,
            description TEXT,
            impact_metric VARCHAR,
            impact_value DOUBLE,
            source VARCHAR,
            ingested_at TIMESTAMP DEFAULT current_timestamp
        )
    """)
    con.execute("""
        CREATE SEQUENCE IF NOT EXISTS change_log_seq START 1
    """)

    # ── Anomalies: replaces flagged anomalies in supplementary sections ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS anomalies (
            id INTEGER PRIMARY KEY,
            market VARCHAR NOT NULL,
            week VARCHAR NOT NULL,
            metric VARCHAR NOT NULL,
            value DOUBLE,
            baseline DOUBLE,
            deviation_pct DOUBLE CHECK (deviation_pct != 0),
            direction VARCHAR,
            flagged_at TIMESTAMP DEFAULT current_timestamp,
            resolved BOOLEAN DEFAULT false,
            notes TEXT
        )
    """)
    con.execute("""
        CREATE SEQUENCE IF NOT EXISTS anomalies_seq START 1
    """)

    # ── Competitor intel: replaces eyes.md competitive landscape tables ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS competitors (
            market VARCHAR NOT NULL,
            competitor VARCHAR NOT NULL,
            week VARCHAR NOT NULL,
            impression_share DOUBLE CHECK (impression_share BETWEEN 0 AND 100),
            cpc_impact_pct DOUBLE,
            segment VARCHAR,
            notes TEXT,
            ingested_at TIMESTAMP DEFAULT current_timestamp,
            PRIMARY KEY (market, competitor, week)
        )
    """)

    # ── OCI rollout status: replaces eyes.md OCI tables ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS oci_status (
            market VARCHAR NOT NULL PRIMARY KEY,
            status VARCHAR,
            launch_date DATE,
            full_impact_date DATE,
            reg_lift_pct DOUBLE,
            cpa_improvement TEXT,
            notes TEXT,
            updated_at TIMESTAMP DEFAULT current_timestamp
        )
    """)

    # ══════════════════════════════════════════════════════════════
    # Phase B: Agent state tables (schema only — no consumers yet)
    # ══════════════════════════════════════════════════════════════

    # ── Agent actions: audit trail for every agent action ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS agent_actions (
            id INTEGER PRIMARY KEY,
            agent VARCHAR,
            action_type VARCHAR,
            market VARCHAR,
            week VARCHAR,
            description TEXT,
            input_summary TEXT,
            output_summary TEXT,
            confidence DOUBLE,
            requires_human_review BOOLEAN,
            reviewed_by_human BOOLEAN,
            human_feedback TEXT,
            created_at TIMESTAMP DEFAULT current_timestamp
        )
    """)
    con.execute("""
        CREATE SEQUENCE IF NOT EXISTS agent_actions_seq START 1
    """)

    # ── Agent observations: what agents notice during analysis ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS agent_observations (
            id INTEGER PRIMARY KEY,
            agent VARCHAR,
            observation_type VARCHAR,
            market VARCHAR,
            week VARCHAR,
            content TEXT,
            severity VARCHAR,
            acted_on BOOLEAN,
            acted_on_by VARCHAR,
            created_at TIMESTAMP DEFAULT current_timestamp
        )
    """)
    con.execute("""
        CREATE SEQUENCE IF NOT EXISTS agent_observations_seq START 1
    """)

    # ── Decisions: tracks decisions requiring approval or review ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY,
            decision_type VARCHAR,
            market VARCHAR,
            description TEXT,
            rationale TEXT,
            made_by VARCHAR,
            approved_by VARCHAR,
            approval_required BOOLEAN,
            status VARCHAR,
            outcome TEXT,
            created_at TIMESTAMP DEFAULT current_timestamp,
            resolved_at TIMESTAMP
        )
    """)
    con.execute("""
        CREATE SEQUENCE IF NOT EXISTS decisions_seq START 1
    """)

    # ── Task queue: agent work items with priority and status ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS task_queue (
            id INTEGER PRIMARY KEY,
            task_type VARCHAR,
            market VARCHAR,
            description TEXT,
            priority INTEGER,
            assigned_to VARCHAR,
            status VARCHAR,
            created_by VARCHAR,
            created_at TIMESTAMP DEFAULT current_timestamp,
            completed_at TIMESTAMP,
            result TEXT
        )
    """)
    con.execute("""
        CREATE SEQUENCE IF NOT EXISTS task_queue_seq START 1
    """)

    # ══════════════════════════════════════════════════════════════
    # Prediction Engine tables
    # ══════════════════════════════════════════════════════════════

    # ── Predictions: every prediction logged ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY,
            question TEXT,
            market VARCHAR,
            metric VARCHAR,
            prediction_type VARCHAR CHECK (prediction_type IN ('point','direction','probability','time_to_target','comparison')),
            point_estimate DOUBLE,
            lower_bound DOUBLE,
            upper_bound DOUBLE,
            confidence_level VARCHAR,
            confidence_probability DOUBLE CHECK (confidence_probability BETWEEN 0 AND 1),
            direction VARCHAR,
            horizon_weeks INTEGER,
            outcome_week VARCHAR,
            reasoning TEXT,
            consumer VARCHAR,
            status VARCHAR DEFAULT 'pending' CHECK (status IN ('pending','scored','expired','cancelled')),
            created_at TIMESTAMP DEFAULT current_timestamp
        )
    """)
    con.execute("CREATE SEQUENCE IF NOT EXISTS predictions_seq START 1")

    # ── Prediction outcomes: scored predictions ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS prediction_outcomes (
            id INTEGER PRIMARY KEY,
            prediction_id INTEGER NOT NULL,
            actual_value DOUBLE,
            predicted_value DOUBLE,
            error_pct DOUBLE,
            direction_correct BOOLEAN,
            within_interval BOOLEAN,
            score DOUBLE CHECK (score BETWEEN 0 AND 1),
            scored_at TIMESTAMP DEFAULT current_timestamp
        )
    """)
    con.execute("CREATE SEQUENCE IF NOT EXISTS prediction_outcomes_seq START 1")

    # ── Calibration log: periodic calibration snapshots ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS calibration_log (
            id INTEGER PRIMARY KEY,
            period VARCHAR,
            total_predictions INTEGER,
            total_scored INTEGER,
            mean_error_pct DOUBLE,
            direction_accuracy DOUBLE,
            interval_coverage DOUBLE,
            calibration_score DOUBLE,
            confidence_adjustment DOUBLE,
            tier_breakdown TEXT,
            computed_at TIMESTAMP DEFAULT current_timestamp
        )
    """)
    con.execute("CREATE SEQUENCE IF NOT EXISTS calibration_log_seq START 1")

    # ── Autonomy tasks: individual task executions ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS autonomy_tasks (
            id INTEGER PRIMARY KEY,
            workflow VARCHAR NOT NULL,
            category VARCHAR NOT NULL CHECK (category IN ('fully_agentic','mixed','human_only')),
            details TEXT,
            agent VARCHAR,
            quality_score DOUBLE,
            logged_at TIMESTAMP DEFAULT current_timestamp
        )
    """)
    con.execute("CREATE SEQUENCE IF NOT EXISTS autonomy_tasks_seq START 1")

    # ── Autonomy history: weekly snapshots of autonomy ratios ──
    con.execute("""
        CREATE TABLE IF NOT EXISTS autonomy_history (
            week VARCHAR NOT NULL,
            workflow VARCHAR NOT NULL,
            total_tasks INTEGER,
            pct_fully_agentic DOUBLE,
            pct_mixed DOUBLE,
            pct_human_only DOUBLE,
            avg_quality_score DOUBLE,
            five_levels_position INTEGER CHECK (five_levels_position BETWEEN 1 AND 5),
            computed_at TIMESTAMP DEFAULT current_timestamp,
            PRIMARY KEY (week, workflow)
        )
    """)

    con.close()
    print(f"Database initialized at {db_path}")
    # Show table summary
    con = duckdb.connect(db_path)
    tables = con.execute("SHOW TABLES").fetchall()
    for t in tables:
        count = con.execute(f"SELECT COUNT(*) FROM {t[0]}").fetchone()[0]
        print(f"  {t[0]}: {count} rows")
    con.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initialize PS Analytics DuckDB')
    parser.add_argument('--path', default=DEFAULT_DB_PATH, help='Database file path')
    args = parser.parse_args()
    init_db(args.path)
