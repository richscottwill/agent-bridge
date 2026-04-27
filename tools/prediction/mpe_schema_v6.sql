-- ====================================================================
-- MPE Schema v6 — Deactivate JP ieccp_range (2026-04-25)
-- ====================================================================
--
-- WHY THIS EXISTS
--     Richard directed 2026-04-25: "stay away from an ie%CCP range for
--     JP". JP previously had ieccp_range = {low: 0.30, high: 0.50} but
--     no committed scalar target. Like AU, JP now has NO ie%CCP
--     commitment at all — it runs via spend-target or rollup-fallback
--     using last-4-week spend run-rate.
--
--     The deactivated row remains for audit trail.
--
-- IMPACT
--     JP projections now require target_mode = 'spend' OR participate
--     in regional rollups where the engine falls back to spend-run-rate.
--     JP's `supported_target_modes` parameter needs to be refreshed to
--     reflect this — ieccp mode is no longer supported for JP.
-- ====================================================================

UPDATE ps.market_projection_params
SET is_active = FALSE,
    notes = COALESCE(notes, '') || ' [DEACTIVATED 2026-04-25 — JP no longer uses an ie%CCP range. Per Richard: JP is run via spend-target or rollup-fallback to last-4w spend run-rate, like AU. See mpe_schema_v6.sql.]'
WHERE market = 'JP'
  AND parameter_name = 'ieccp_range'
  AND is_active = TRUE;

-- Also refresh JP's supported_target_modes to drop ieccp.
-- Previously: ['spend', 'ieccp', 'regs']. New: ['spend', 'regs'].
INSERT INTO ps.market_projection_params
    (market, parameter_name, parameter_version, value_json, refit_cadence,
     last_refit_at, source, fallback_level, lineage, notes, is_active)
SELECT 'JP', 'supported_target_modes',
       (SELECT COALESCE(MAX(parameter_version), 0) + 1 FROM ps.market_projection_params WHERE market = 'JP' AND parameter_name = 'supported_target_modes'),
       '["spend", "regs"]',
       'annual', CURRENT_TIMESTAMP, 'richard_directive_2026-04-25',
       'market_specific',
       'JP dropped ieccp mode per 2026-04-25 directive — no committed ie%CCP target.',
       'Updated 2026-04-25 Phase 6.2.x follow-on', TRUE;

-- Deactivate prior JP supported_target_modes rows.
UPDATE ps.market_projection_params
SET is_active = FALSE
WHERE market = 'JP'
  AND parameter_name = 'supported_target_modes'
  AND is_active = TRUE
  AND parameter_version < (
      SELECT MAX(parameter_version)
      FROM ps.market_projection_params
      WHERE market = 'JP' AND parameter_name = 'supported_target_modes'
  );
