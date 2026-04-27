-- MPE v1.1 Slim — Schema v7 (Phase 6.5.3)
-- Adds ps.projection_feedback for capturing human judgment at projection time.

CREATE TABLE IF NOT EXISTS ps.projection_feedback (
    id VARCHAR PRIMARY KEY DEFAULT uuid(),
    projection_id VARCHAR NOT NULL,    -- FK to ps.forecasts (or a UI-generated uuid if not persisted)
    user_id VARCHAR NOT NULL,          -- Amazon alias
    verdict VARCHAR NOT NULL,          -- too_high | too_low | missing_context | looks_right
    magnitude_pct FLOAT,               -- optional % for too_high/too_low
    freetext VARCHAR,                  -- required for missing_context, optional otherwise
    scope VARCHAR NOT NULL,            -- market or region code
    time_period VARCHAR NOT NULL,      -- W17 | M04 | Q2 | Y2026 | MY1 etc.
    target_mode VARCHAR NOT NULL,      -- spend | ieccp | regs | rollup
    target_value FLOAT NOT NULL,
    scenario_chip VARCHAR,             -- mixed | frequentist | bayesian | no-lift (Phase 6.4.5)
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,            -- null until "missing_context" text reviewed for catalog
    resulted_in_qualitative_prior BOOLEAN DEFAULT FALSE,
    notes VARCHAR                      -- triage notes appended during review (Phase 6.5.4)
);

-- Quick-lookup indexes (DuckDB uses these as sort pruning hints)
CREATE INDEX IF NOT EXISTS idx_projection_feedback_submitted_at ON ps.projection_feedback (submitted_at DESC);
CREATE INDEX IF NOT EXISTS idx_projection_feedback_verdict ON ps.projection_feedback (verdict);
CREATE INDEX IF NOT EXISTS idx_projection_feedback_scope ON ps.projection_feedback (scope);
