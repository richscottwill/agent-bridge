-- ====================================================================
-- MPE Schema v4 — Explicit ie%CCP targets for US, CA, EU5 markets + NA, EU5 regions
-- ====================================================================
--
-- WHY THIS EXISTS
--     Phase 6.2.x follow-on 2026-04-25: Richard directed explicit
--     ie%CCP target = 65% for the markets currently planning to that
--     ceiling (US, CA, UK, DE, FR, IT, ES) + the two regions they roll
--     into (NA, EU5).
--
--     Previously these markets had only `ieccp_range = {low: 0.50, high: 0.65}`
--     — a planning range without a committed scalar target. Engine paths
--     that needed "the target" had to derive from the range high, which
--     ambiguous when commentary said "target 65%."
--
--     MX keeps its `ieccp_target = 1.00` (different market — 100% is
--     MX's target ceiling). JP keeps its range without a scalar target
--     (no explicit commitment yet). AU never had ieccp (null by design).
--     WW has no regional target.
--
-- WHAT THIS MIGRATION ADDS
--     9 new rows in ps.market_projection_params:
--       - US, CA, UK, DE, FR, IT, ES with parameter_name='ieccp_target' = 0.65
--       - NA, EU5 with parameter_name='ieccp_target' = 0.65 (regional)
--
--     Preserves existing ieccp_range rows — those remain the planning
--     range context, ieccp_target is the committed scalar.
--
-- HOW TO APPLY
--     Same as v3 — open read_only=False connection, .execute(file.read())
-- ====================================================================

-- Set ie%CCP = 0.65 for 7 markets + 2 regions.
INSERT INTO ps.market_projection_params
    (market, parameter_name, parameter_version, value_scalar, refit_cadence,
     last_refit_at, source, fallback_level, lineage, notes, is_active)
SELECT target_list.scope, 'ieccp_target', 1, 0.65,
       'annual', CURRENT_TIMESTAMP, 'richard_directive_2026-04-25', 'market_specific',
       'Committed ie%CCP target = 65% for NA/EU5 planning. Set by Richard 2026-04-25. Previously these markets had only ieccp_range={low:0.50, high:0.65}; the 65% ceiling is now explicitly the committed target.',
       'Seeded 2026-04-25 Phase 6.2.x follow-on', TRUE
FROM (VALUES
    ('US'), ('CA'),
    ('UK'), ('DE'), ('FR'), ('IT'), ('ES'),
    ('NA'), ('EU5')
) AS target_list(scope)
WHERE NOT EXISTS (
    SELECT 1 FROM ps.market_projection_params
    WHERE market = target_list.scope AND parameter_name = 'ieccp_target'
);
