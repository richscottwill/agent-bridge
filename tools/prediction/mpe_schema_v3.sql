-- ====================================================================
-- MPE Schema v3 — Phase 6.2.4 parameter registry extensions
-- ====================================================================
--
-- WHY THIS EXISTS
--     v1.1 Slim introduces new Brand trajectory parameters that need
--     persistence in ps.market_projection_params for operator audit +
--     refit pipeline consumption + JSON export (JS UI). This migration
--     adds 5 new parameter keys per market and deprecates 4 v1 keys.
--
-- WHAT THIS MIGRATION ADDS (5 new params × 10 markets = 50 rows)
--     brand_seasonal_prior    — per-ISO-week multipliers from per-year-
--                               normalized fit (Phase 6.2.x refactor
--                               fixes regime distortion). JSON: {weights: [...52]}
--     brand_recent_trend      — intercept + log-slope from recent
--                               post-earliest-regime data (TREND_HALF_LIFE_WEEKS=4,
--                               TREND_FADE_HALF_LIFE_WEEKS=13). JSON: {intercept, slope_log, n_weeks_used}
--     brand_regime_multipliers — regime_id → peak multiplier summary
--                                (reads live from ps.regime_fit_state; this row
--                                is a caching snapshot). JSON: {regime_id: {peak, half_life, decay_status}}
--     brand_cpa_projected     — rolling 8-week median Brand CPA per regime segment
--                               (scalar per market or JSON per-segment if IT-style stacked regimes)
--     brand_trajectory_weights — default {seasonal: 0.40, trend: 0.40, regime: 0.15, qualitative: 0.05}
--                                per market; user overrides are scoped per-projection, not persisted
--
-- WHAT THIS MIGRATION DEPRECATES (4 × 10 = 40 rows marked inactive)
--     brand_cpa_elasticity     — superseded by brand_cpa_projected (scalar, not elasticity)
--     brand_cpc_elasticity     — same rationale
--     brand_yoy_growth         — Y-o-Y lift now lives inside the regime multiplier stream
--     brand_spend_share        — Brand/NB allocation no longer derived from share; Brand
--                                comes from trajectory, NB is residual
--
-- The deprecated rows remain in the table for audit trail — the
-- `is_active=FALSE` flag prevents them from showing in the current-view
-- query. Re-reading fit_market.py must write new v1.1 Slim rows and
-- mark the superseded rows inactive in a single transaction.
--
-- HOW TO APPLY
--     python3 -c "from prediction.mpe_engine import _db; con=_db();
--                 with open('mpe_schema_v3.sql') as f: con.execute(f.read())"
--     (needs read_only=False; use prediction.brand_trajectory._fitting_db or
--      a dedicated write connection in practice.)
-- ====================================================================

-- Safe no-op: the columns the new params use (parameter_name, value_json,
-- value_scalar, etc.) already exist in v1 schema — this migration only
-- seeds rows and flips is_active flags. No schema changes.

-- ====================================================================
-- Deprecate v1 parameters (all 10 markets)
-- ====================================================================

UPDATE ps.market_projection_params
SET is_active = FALSE,
    notes = COALESCE(notes, '') || ' [DEPRECATED 2026-04-23 in v1.1 Slim Phase 6.2.4]'
WHERE parameter_name IN (
    'brand_cpa_elasticity',
    'brand_cpc_elasticity',
    'brand_yoy_growth',
    'brand_spend_share'
)
AND is_active = TRUE;

-- Note: nb_cpa_elasticity / nb_cpc_elasticity / nb_yoy_growth / seasonality
-- are RETAINED (active=TRUE) — v1.1 Slim still uses NB CPA elasticity as
-- the closure equation for the NB residual solver.

-- ====================================================================
-- Seed v1.1 Slim parameters (placeholder rows with bootstrap lineage)
-- ====================================================================
-- Actual values populated by fit_market.py on next refit; these rows
-- exist so that _fetch_parameters has stable keys to query.

-- brand_trajectory_weights (scalar JSON per market — same defaults everywhere)
INSERT INTO ps.market_projection_params
    (market, parameter_name, parameter_version, value_json, refit_cadence,
     last_refit_at, source, fallback_level, lineage, notes, is_active)
SELECT market_list.m, 'brand_trajectory_weights', 1,
       '{"seasonal": 0.40, "trend": 0.40, "regime": 0.15, "qualitative": 0.05}',
       'quarterly', CURRENT_TIMESTAMP, 'v1.1_slim_seed', 'market_specific',
       'Default blend weights per Phase 6.2.4 seed; user overrides via regime_multiplier slider are not persisted.',
       'Seeded 2026-04-23 Phase 6.2.4', TRUE
FROM (VALUES
    ('US'), ('CA'), ('UK'), ('DE'), ('FR'),
    ('IT'), ('ES'), ('JP'), ('MX'), ('AU')
) AS market_list(m)
WHERE NOT EXISTS (
    SELECT 1 FROM ps.market_projection_params
    WHERE market = market_list.m AND parameter_name = 'brand_trajectory_weights'
);

-- brand_cpa_projected — populated by next fit_market.py run; seed with
-- zero-scalar placeholder to reserve the slot.
INSERT INTO ps.market_projection_params
    (market, parameter_name, parameter_version, value_scalar, refit_cadence,
     last_refit_at, source, fallback_level, lineage, notes, is_active)
SELECT market_list.m, 'brand_cpa_projected', 1,
       0.0,
       'weekly', CURRENT_TIMESTAMP, 'v1.1_slim_seed', 'bootstrap',
       'Placeholder — will be populated by next fit_market.py run with rolling 8-week median Brand CPA. Current projections still read from ps.v_weekly directly via compute_brand_cpa_projected().',
       'Seeded 2026-04-23 Phase 6.2.4', TRUE
FROM (VALUES
    ('US'), ('CA'), ('UK'), ('DE'), ('FR'),
    ('IT'), ('ES'), ('JP'), ('MX'), ('AU')
) AS market_list(m)
WHERE NOT EXISTS (
    SELECT 1 FROM ps.market_projection_params
    WHERE market = market_list.m AND parameter_name = 'brand_cpa_projected'
);

-- brand_seasonal_prior, brand_recent_trend, brand_regime_multipliers —
-- these three are placeholder-only; fit_market.py populates value_json.
-- We seed null value_json with bootstrap lineage so the keys exist.
-- Rationale: brand_trajectory.py currently computes these on-the-fly
-- from ps.v_weekly + ps.regime_fit_state. Persisting them is an
-- optimization + audit feature, not a correctness requirement.

INSERT INTO ps.market_projection_params
    (market, parameter_name, parameter_version, value_json, refit_cadence,
     last_refit_at, source, fallback_level, lineage, notes, is_active)
SELECT market_list.m, 'brand_seasonal_prior', 1,
       '{"weights": [], "yoy_cv": [], "n_years_used": 0, "fit_method": "per-year-normalized"}',
       'annual', CURRENT_TIMESTAMP, 'v1.1_slim_seed', 'bootstrap',
       'Placeholder — compute_seasonal_multipliers() in brand_trajectory.py reads live from ps.v_weekly. Next fit_market.py run persists snapshot here for export pipeline + audit.',
       'Seeded 2026-04-23 Phase 6.2.4 (per-year-normalized method, replaces v1 flat-average seasonality)', TRUE
FROM (VALUES
    ('US'), ('CA'), ('UK'), ('DE'), ('FR'),
    ('IT'), ('ES'), ('JP'), ('MX'), ('AU')
) AS market_list(m)
WHERE NOT EXISTS (
    SELECT 1 FROM ps.market_projection_params
    WHERE market = market_list.m AND parameter_name = 'brand_seasonal_prior'
);

INSERT INTO ps.market_projection_params
    (market, parameter_name, parameter_version, value_json, refit_cadence,
     last_refit_at, source, fallback_level, lineage, notes, is_active)
SELECT market_list.m, 'brand_recent_trend', 1,
       '{"intercept": 0.0, "slope_log": 0.0, "n_weeks_used": 0, "latest_week": null}',
       'weekly', CURRENT_TIMESTAMP, 'v1.1_slim_seed', 'bootstrap',
       'Placeholder — compute_recent_trend() in brand_trajectory.py reads live. Next fit_market.py run persists snapshot.',
       'Seeded 2026-04-23 Phase 6.2.4', TRUE
FROM (VALUES
    ('US'), ('CA'), ('UK'), ('DE'), ('FR'),
    ('IT'), ('ES'), ('JP'), ('MX'), ('AU')
) AS market_list(m)
WHERE NOT EXISTS (
    SELECT 1 FROM ps.market_projection_params
    WHERE market = market_list.m AND parameter_name = 'brand_recent_trend'
);

INSERT INTO ps.market_projection_params
    (market, parameter_name, parameter_version, value_json, refit_cadence,
     last_refit_at, source, fallback_level, lineage, notes, is_active)
SELECT market_list.m, 'brand_regime_multipliers', 1,
       '{"regimes": [], "n_active": 0, "source_table": "ps.regime_fit_state_current"}',
       'weekly', CURRENT_TIMESTAMP, 'v1.1_slim_seed', 'bootstrap',
       'Placeholder — brand_trajectory.py reads directly from ps.regime_fit_state_current. This row is a caching hint.',
       'Seeded 2026-04-23 Phase 6.2.4', TRUE
FROM (VALUES
    ('US'), ('CA'), ('UK'), ('DE'), ('FR'),
    ('IT'), ('ES'), ('JP'), ('MX'), ('AU')
) AS market_list(m)
WHERE NOT EXISTS (
    SELECT 1 FROM ps.market_projection_params
    WHERE market = market_list.m AND parameter_name = 'brand_regime_multipliers'
);
