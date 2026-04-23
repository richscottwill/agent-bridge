-- MPE Schema — Phase 1 Task 1.1
--
-- WHY THIS EXISTS
--     The Market Projection Engine (MPE) needs its own parameter registry
--     with versioning, provenance, and fallback tracking per market per
--     parameter. This DDL creates the 6 new tables + 1 view the engine
--     depends on. All tables live in the `ps` schema alongside existing
--     ps.v_weekly, ps.performance, ps.regime_changes.
--
-- HOW THE OWNER MAINTAINS IT
--     You never edit these tables by hand. The refit hook writes to
--     ps.market_projection_params. The anomaly detector writes to
--     ps.parameter_anomalies. The UI reads from ps.market_projection_params_current.
--     If a table needs a schema change, run a new migration file
--     (mpe_schema_v2.sql). Never rewrite this one.
--
-- WHAT HAPPENS ON FAILURE
--     If a CREATE fails because the table already exists, this file uses
--     IF NOT EXISTS so rerun is idempotent. If a column needs to change,
--     use ALTER TABLE in a new migration; this file is the canonical v1.
--
-- COEXISTENCE
--     These tables are net-new. Does not touch ps.performance,
--     ps.seasonal_priors, ps.regime_changes, ps.v_weekly, ps.forecasts,
--     ps.market_constraints_manual. Existing BayesianProjector and WBR
--     pipeline are unaffected. See mpe-existing-code-coexistence.md.

-- ====================================================================
-- 1. ps.market_projection_params — versioned parameter registry
-- ====================================================================

CREATE TABLE IF NOT EXISTS ps.market_projection_params (
    market VARCHAR NOT NULL,
    parameter_name VARCHAR NOT NULL,
    parameter_version INTEGER NOT NULL,
    value_scalar DOUBLE,
    value_json JSON,
    refit_cadence VARCHAR NOT NULL,        -- 'annual' or 'quarterly'
    last_refit_at TIMESTAMP NOT NULL,
    last_validated_at TIMESTAMP,
    validation_mape DOUBLE,
    source VARCHAR NOT NULL,                -- 'finance_negotiation' | 'historical_fit' | 'manual_override' | 'regional_fallback' | 'derived_from_cpa'
    fallback_level VARCHAR NOT NULL DEFAULT 'market_specific',  -- 'market_specific' | 'regional_fallback' | 'southern_hemisphere_hybrid' | 'prior_version' | 'conservative_default'
    lineage VARCHAR,
    fitted_on_data_range VARCHAR,
    notes VARCHAR,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (market, parameter_name, parameter_version)
);

-- Current-active view: one row per (market, parameter_name) with the
-- latest active version.
CREATE OR REPLACE VIEW ps.market_projection_params_current AS
SELECT *
FROM ps.market_projection_params
WHERE is_active = TRUE
  AND parameter_version = (
      SELECT MAX(parameter_version)
      FROM ps.market_projection_params p2
      WHERE p2.market = ps.market_projection_params.market
        AND p2.parameter_name = ps.market_projection_params.parameter_name
        AND p2.is_active = TRUE
  );

-- ====================================================================
-- 2. ps.parameter_validation — per-refit validation records
-- ====================================================================

CREATE TABLE IF NOT EXISTS ps.parameter_validation (
    market VARCHAR NOT NULL,
    parameter_name VARCHAR NOT NULL,
    parameter_version INTEGER NOT NULL,
    validation_run_at TIMESTAMP NOT NULL,
    holdout_mape DOUBLE,
    validation_sample_range VARCHAR,       -- e.g. '2026-W01 to 2026-W12'
    notes VARCHAR,
    PRIMARY KEY (market, parameter_name, parameter_version, validation_run_at)
);

-- ====================================================================
-- 3. ps.parameter_anomalies — flagged anomaly candidates
-- ====================================================================

CREATE TABLE IF NOT EXISTS ps.parameter_anomalies (
    id VARCHAR PRIMARY KEY DEFAULT uuid(),
    market VARCHAR NOT NULL,
    parameter_name VARCHAR NOT NULL,
    from_version INTEGER NOT NULL,
    to_version INTEGER NOT NULL,
    delta_pct DOUBLE,
    std_dev_distance DOUBLE,
    anomaly_category VARCHAR NOT NULL,     -- 'investigate' | 'expected-regime-change' | 'approved-by-reviewer'
    reviewer VARCHAR,
    review_notes VARCHAR,
    flagged_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- ====================================================================
-- 4. ps.regional_narrative_templates — per-region narrative templates
-- ====================================================================

CREATE TABLE IF NOT EXISTS ps.regional_narrative_templates (
    region VARCHAR PRIMARY KEY,             -- 'NA' | 'EU5' | 'WW'
    prose_template VARCHAR NOT NULL,
    mix_effect_language VARCHAR,
    so_what_framing VARCHAR,
    last_updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR
);

-- ====================================================================
-- 5. ps.projection_scores — actual vs projected scoring records
-- ====================================================================

CREATE TABLE IF NOT EXISTS ps.projection_scores (
    id VARCHAR PRIMARY KEY DEFAULT uuid(),
    saved_projection_path VARCHAR NOT NULL,
    scope VARCHAR NOT NULL,
    time_period VARCHAR NOT NULL,
    target_mode VARCHAR NOT NULL,
    metric VARCHAR NOT NULL,               -- e.g. 'total_regs', 'brand_spend', 'ieccp'
    projected_value DOUBLE,
    actual_value DOUBLE,
    error_pct DOUBLE,
    within_70pct_ci BOOLEAN,
    within_90pct_ci BOOLEAN,
    scored_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ====================================================================
-- Indices for common query patterns
-- ====================================================================

CREATE INDEX IF NOT EXISTS idx_mpe_params_market
    ON ps.market_projection_params(market);

CREATE INDEX IF NOT EXISTS idx_mpe_params_name_active
    ON ps.market_projection_params(parameter_name, is_active);

CREATE INDEX IF NOT EXISTS idx_mpe_anomalies_category
    ON ps.parameter_anomalies(anomaly_category, flagged_at);

-- ====================================================================
-- MARKET_STRATEGY seed — migrates values from bayesian_projector.py
-- This is the Task 1.1 companion seed. Values are exactly those in
-- bayesian_projector.py MARKET_STRATEGY dict as of 2026-04-22.
-- If that dict ever changes, this seed should be re-run (or deleted
-- and replaced with a v1.1 migration that has bayesian_projector.py
-- read from the registry instead).
-- ====================================================================

-- ieccp_target (scalar or null; AU, JP, US, CA, UK, DE, FR, IT, ES have null target;
-- MX is the only market with a fixed ieccp_target = 1.0 = 100%)
INSERT INTO ps.market_projection_params
    (market, parameter_name, parameter_version, value_scalar, refit_cadence,
     last_refit_at, source, fallback_level, lineage, notes, is_active)
VALUES
    ('MX', 'ieccp_target', 1, 1.0, 'annual', CURRENT_TIMESTAMP, 'finance_negotiation',
     'market_specific', 'bayesian_projector.py MARKET_STRATEGY migrated 2026-04-22',
     'MX ie%CCP target = 100% = 1.0; range 90%-110%', TRUE)
ON CONFLICT DO NOTHING;

-- ieccp_range per market
INSERT INTO ps.market_projection_params
    (market, parameter_name, parameter_version, value_json, refit_cadence,
     last_refit_at, source, fallback_level, lineage, is_active)
VALUES
    ('MX', 'ieccp_range', 1, '{"low": 0.90, "high": 1.10}', 'annual', CURRENT_TIMESTAMP,
     'finance_negotiation', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('JP', 'ieccp_range', 1, '{"low": 0.30, "high": 0.50}', 'annual', CURRENT_TIMESTAMP,
     'finance_negotiation', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('US', 'ieccp_range', 1, '{"low": 0.50, "high": 0.65}', 'annual', CURRENT_TIMESTAMP,
     'finance_negotiation', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('CA', 'ieccp_range', 1, '{"low": 0.50, "high": 0.65}', 'annual', CURRENT_TIMESTAMP,
     'finance_negotiation', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('UK', 'ieccp_range', 1, '{"low": 0.50, "high": 0.65}', 'annual', CURRENT_TIMESTAMP,
     'finance_negotiation', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('DE', 'ieccp_range', 1, '{"low": 0.50, "high": 0.65}', 'annual', CURRENT_TIMESTAMP,
     'finance_negotiation', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('FR', 'ieccp_range', 1, '{"low": 0.50, "high": 0.65}', 'annual', CURRENT_TIMESTAMP,
     'finance_negotiation', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('IT', 'ieccp_range', 1, '{"low": 0.50, "high": 0.65}', 'annual', CURRENT_TIMESTAMP,
     'finance_negotiation', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('ES', 'ieccp_range', 1, '{"low": 0.50, "high": 0.65}', 'annual', CURRENT_TIMESTAMP,
     'finance_negotiation', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE)
ON CONFLICT DO NOTHING;
-- AU has no ieccp_range (efficiency strategy) — no row

-- supported_target_modes per market
INSERT INTO ps.market_projection_params
    (market, parameter_name, parameter_version, value_json, refit_cadence,
     last_refit_at, source, fallback_level, lineage, is_active)
VALUES
    ('MX', 'supported_target_modes', 1, '["spend", "ieccp", "regs"]', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('US', 'supported_target_modes', 1, '["spend", "ieccp", "regs"]', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('CA', 'supported_target_modes', 1, '["spend", "ieccp", "regs"]', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('UK', 'supported_target_modes', 1, '["spend", "ieccp", "regs"]', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('DE', 'supported_target_modes', 1, '["spend", "ieccp", "regs"]', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('FR', 'supported_target_modes', 1, '["spend", "ieccp", "regs"]', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('IT', 'supported_target_modes', 1, '["spend", "ieccp", "regs"]', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('ES', 'supported_target_modes', 1, '["spend", "ieccp", "regs"]', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('JP', 'supported_target_modes', 1, '["spend", "ieccp", "regs"]', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('AU', 'supported_target_modes', 1, '["spend", "regs"]', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22 — AU efficiency, no ieccp', TRUE)
ON CONFLICT DO NOTHING;

-- market_strategy_type (new parameter, for narrative template selection)
INSERT INTO ps.market_projection_params
    (market, parameter_name, parameter_version, value_scalar, value_json, refit_cadence,
     last_refit_at, source, fallback_level, lineage, is_active)
VALUES
    ('AU', 'market_strategy_type', 1, NULL, '{"type": "efficiency"}', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('MX', 'market_strategy_type', 1, NULL, '{"type": "ieccp_bound"}', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('JP', 'market_strategy_type', 1, NULL, '{"type": "brand_dominant"}', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('US', 'market_strategy_type', 1, NULL, '{"type": "balanced"}', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('CA', 'market_strategy_type', 1, NULL, '{"type": "balanced"}', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('UK', 'market_strategy_type', 1, NULL, '{"type": "balanced"}', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('DE', 'market_strategy_type', 1, NULL, '{"type": "balanced"}', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('FR', 'market_strategy_type', 1, NULL, '{"type": "balanced"}', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('IT', 'market_strategy_type', 1, NULL, '{"type": "balanced"}', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE),
    ('ES', 'market_strategy_type', 1, NULL, '{"type": "balanced"}', 'annual', CURRENT_TIMESTAMP,
     'manual_override', 'market_specific', 'bayesian_projector.py MARKET_STRATEGY 2026-04-22', TRUE)
ON CONFLICT DO NOTHING;
