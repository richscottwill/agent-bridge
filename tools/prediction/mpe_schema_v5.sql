-- ====================================================================
-- MPE Schema v5 — Remove regional ie%CCP target scalars (2026-04-25)
-- ====================================================================
--
-- WHY THIS EXISTS
--     Yesterday's v4 migration seeded NA and EU5 with
--     `ieccp_target = 0.65` scalar rows. Richard corrected the shape:
--     regional targets are ROLLUPS of constituent markets' projections,
--     not solver constraints that drive per-market NB allocation.
--     Markets have their own committed targets (US/CA/UK/DE/FR/IT/ES
--     = 0.65, MX = 1.00, JP range 0.30-0.50, AU none); a region's
--     realized ie%CCP is what its children produce, summed-then-divided
--     per R6.2.
--
--     Having a regional `ieccp_target` scalar was misleading because
--     the engine would either (a) ignore it and leave callers confused
--     or (b) incorrectly apply it by overwriting per-market targets.
--     Cleanest fix: deactivate the regional target rows, keep the
--     per-market rows (which were correctly seeded in v4).
--
-- WHAT THIS MIGRATION DOES
--     Marks ieccp_target rows for NA and EU5 as is_active=FALSE.
--     The per-market rows (US, CA, UK, DE, FR, IT, ES) added in v4
--     remain active — those are correct.
-- ====================================================================

UPDATE ps.market_projection_params
SET is_active = FALSE,
    notes = COALESCE(notes, '') || ' [DEACTIVATED 2026-04-25 — regional targets are rollups of constituents, not solver constraints. Per-market ieccp_target rows remain active. See mpe_schema_v5.sql for rationale.]'
WHERE parameter_name = 'ieccp_target'
  AND market IN ('NA', 'EU5')
  AND is_active = TRUE;
