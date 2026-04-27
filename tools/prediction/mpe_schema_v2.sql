-- ====================================================================
-- MPE Schema v2 — Phase 6.1 v1.1 Slim additions
-- ====================================================================
--
-- WHY THIS EXISTS
--     v1.1 Slim separates AUTHORED regime facts (ps.regime_changes —
--     unchanged) from WEEKLY-FITTED regime state (ps.regime_fit_state —
--     new). Authored rows are immutable audit trail: "on 2026-04-23 we
--     recorded that Sparkle launched W14 with half-life guess 26w."
--     Fitted state updates weekly: "as of W20, Sparkle's observed decay
--     suggests half-life ~18w; peak multiplier re-estimated at 2.8×
--     from the now-longer post-onset window."
--
--     Keeping these in one table makes audit impossible. Keeping them
--     separate means you can always answer "what did the model believe
--     about this regime on date X."
--
-- HOW THE OWNER MAINTAINS IT
--     You never edit ps.regime_fit_state by hand. The weekly regime
--     fitter (shared/tools/prediction/fit_regime_state.py) writes to it
--     every Monday after ps.v_weekly refreshes. Manually-authored
--     regime rows go into ps.regime_changes as before.
--
-- WHEN TO UPDATE THIS FILE
--     Never rewrite in place. Schema changes = new migration file
--     (mpe_schema_v3.sql).
--
-- COEXISTENCE
--     ps.regime_fit_state does not modify ps.regime_changes. It
--     references regime_id as a foreign key only. Existing v1 engine
--     is unaffected. Phase 6.1.3 refactor of brand_trajectory.py will
--     prefer reading fit_state, falling back to inline compute when
--     no fit_state row exists (bootstrap path).
-- ====================================================================


-- ====================================================================
-- ps.regime_fit_state — weekly-fitted regime parameters
-- ====================================================================
-- One row per (market, regime_id, fit_as_of) combination. Append-only —
-- every weekly refit inserts a new row. Latest row per regime is the
-- current state; history is retained for audit and backtest replay.

CREATE TABLE IF NOT EXISTS ps.regime_fit_state (
    id VARCHAR PRIMARY KEY DEFAULT uuid(),
    regime_id VARCHAR NOT NULL,              -- FK to ps.regime_changes.id
    market VARCHAR NOT NULL,                 -- denormalized for fast reads
    fit_as_of DATE NOT NULL,                 -- the cutoff date — this fit used data through this week
    peak_multiplier DOUBLE NOT NULL,         -- re-fit peak, from best window available at fit_as_of
    fitted_half_life_weeks DOUBLE,           -- observed decay rate; NULL = too early to infer
    current_multiplier DOUBLE NOT NULL,      -- effective multiplier at fit_as_of (peak × decay)
    n_post_weeks INTEGER NOT NULL,           -- how many post-onset weeks fed this fit
    decay_status VARCHAR NOT NULL,           -- 'still-peaking' | 'decaying-as-expected' | 'decaying-faster' | 'decaying-slower' | 'no-decay-detected' | 'dormant' | 'insufficient-data'
    confidence DOUBLE,                       -- 0.0-1.0; how much trust to put in peak + half-life estimates
    authored_half_life_weeks DOUBLE,         -- what was authored at regime insertion time (for divergence detection)
    fit_method VARCHAR NOT NULL,             -- 'mean-ratio-8w' | 'mean-ratio-full' | 'exponential-decay-fit' | 'bootstrap'
    warnings VARCHAR,                        -- JSON array of warning codes
    fitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lineage VARCHAR,                         -- free-text provenance
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_regime_fit_regime_id
    ON ps.regime_fit_state(regime_id);
CREATE INDEX IF NOT EXISTS idx_regime_fit_market
    ON ps.regime_fit_state(market);
CREATE INDEX IF NOT EXISTS idx_regime_fit_as_of
    ON ps.regime_fit_state(fit_as_of DESC);


-- Convenience view: latest fit per regime
CREATE OR REPLACE VIEW ps.regime_fit_state_current AS
SELECT s.*
FROM ps.regime_fit_state s
WHERE s.is_active = TRUE
  AND s.fit_as_of = (
      SELECT MAX(fit_as_of)
      FROM ps.regime_fit_state s2
      WHERE s2.regime_id = s.regime_id
        AND s2.is_active = TRUE
  );
