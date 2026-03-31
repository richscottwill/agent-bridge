# Implementation Plan: Agent Consolidation and Pipeline Framework

## Overview

Consolidate 7 WBR callout agent files into 3 (parameterized analyst + parameterized writer + unchanged reviewer), wire Phase B agent state tables with 3 new `query.py` functions, update per-market context files with Agent Configuration sections, update the pipeline hook and routing directory, run the blind architecture evaluation, then clean up old files and update documentation.

## Tasks

- [x] 1. Add agent state functions to query.py
  - [x] 1.1 Implement `log_agent_action()` in `~/shared/tools/data/query.py`
    - Add function that inserts a row into `agent_actions` using `agent_actions_seq` for auto-incremented ID
    - Accept parameters: agent, action_type, market, week, description, output_summary (optional), confidence (optional), db_path (optional)
    - Return the integer ID of the new row
    - Close the database connection in a finally block
    - _Requirements: 4.1, 4.2, 4.6_

  - [x] 1.2 Implement `log_agent_observation()` in `~/shared/tools/data/query.py`
    - Add function that inserts a row into `agent_observations` using `agent_observations_seq` for auto-incremented ID
    - Accept parameters: agent, observation_type, market, week, content, severity (default 'info'), db_path (optional)
    - `acted_on` defaults to false
    - Return the integer ID of the new row
    - Close the database connection in a finally block
    - _Requirements: 5.1, 5.2, 5.3_

  - [x] 1.3 Implement `query_prior_observations()` in `~/shared/tools/data/query.py`
    - Add function that queries `agent_observations` for a given market within the last `weeks * 7` days
    - Accept parameters: market, weeks (default 4), observation_type (optional filter), db_path (optional)
    - Open a read-only connection
    - Return list of dicts ordered by `created_at` descending; empty list if no results
    - Close the database connection in a finally block
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [x] 1.4 Implement `log_architecture_eval()` in `~/shared/tools/data/query.py`
    - Add convenience wrapper that calls `log_agent_observation()` with `observation_type='architecture_eval'`
    - Accept parameters: change_name, pipeline, market, scores (dict), evaluator_notes, verdict, db_path (optional)
    - Return the observation ID
    - _Requirements: 13.7_

  - [x]* 1.5 Write property test: agent state write produces unique row with correct defaults (Property 1)
    - **Property 1: Agent state write produces unique row with correct defaults**
    - For any valid combination of agent name, action type, market, week, and description, `log_agent_action()` inserts exactly one new row with a unique auto-incremented ID
    - For any valid combination of agent, observation type, market, week, and content, `log_agent_observation()` inserts exactly one new row with `acted_on` defaulting to false
    - Use a temporary DuckDB database for isolation
    - **Validates: Requirements 4.1, 5.1, 5.2**

  - [x]* 1.6 Write property test: prior observation query returns correct filtered, ordered, time-windowed results (Property 2)
    - **Property 2: Prior observation query returns correct filtered, ordered, time-windowed results**
    - For any market and set of observations with varying timestamps and types, `query_prior_observations(market, weeks=N)` returns only observations for that market within the last `N * 7` days, ordered by `created_at` descending
    - When `observation_type` filter is provided, only matching types are returned
    - **Validates: Requirements 6.1, 6.2**

  - [x]* 1.7 Write property test: idempotent projection upsert (Property 3)
    - **Property 3: Idempotent projection upsert**
    - For any market and week, calling `db_upsert('projections', data, ['market', 'week'])` twice with the same key columns results in exactly one row, with the second call's values overwriting the first
    - **Validates: Requirements 10.1, 10.2, 10.3**

- [x] 2. Checkpoint — Verify query.py functions
  - Ensure all tests pass, ask the user if questions arise.

- [x] 3. Add Agent Configuration sections to per-market context files
  - [x] 3.1 Add `## Agent Configuration` section to AU context file (`~/shared/context/active/callouts/au/au-context.md`)
    - Fields: `markets: [AU]`, `has_yoy: false`, `has_ieccp: false`, `headline_extras: []`, `regional_summary: false`, `spend_strategy`, `projection_notes`
    - _Requirements: 3.1, 3.2_

  - [x] 3.2 Add `## Agent Configuration` section to MX context file (`~/shared/context/active/callouts/mx/mx-context.md`)
    - Fields: `markets: [MX]`, `has_yoy: true`, `has_ieccp: true`, `headline_extras: [ie%CCP]`, `regional_summary: false`, `spend_strategy`, `projection_notes`
    - _Requirements: 3.1, 3.2_

  - [x] 3.3 Add `## Agent Configuration` section to US context file (`~/shared/context/active/callouts/us/us-context.md`)
    - Fields: `markets: [US]`, `has_yoy: true`, `has_ieccp: false`, `headline_extras: []`, `regional_summary: false`, `spend_strategy`, `projection_notes`
    - _Requirements: 3.1, 3.2_

  - [x] 3.4 Add `## Agent Configuration` section to CA context file (`~/shared/context/active/callouts/ca/ca-context.md`)
    - Fields: `markets: [CA]`, `has_yoy: true`, `has_ieccp: false`, `headline_extras: []`, `regional_summary: false`, `spend_strategy`, `projection_notes`
    - _Requirements: 3.1, 3.2_

  - [x] 3.5 Add `## Agent Configuration` section to JP context file (`~/shared/context/active/callouts/jp/jp-context.md`)
    - Fields: `markets: [JP]`, `has_yoy: true`, `has_ieccp: false`, `headline_extras: []`, `regional_summary: false`, `spend_strategy`, `projection_notes`
    - _Requirements: 3.1, 3.2_

  - [x] 3.6 Add `## Agent Configuration` sections to EU5 context files (UK, DE, FR, IT, ES)
    - For each EU5 market context file under `~/shared/context/active/callouts/{market}/`
    - Fields: `markets: [{market}]`, `has_yoy: true`, `has_ieccp: false`, `headline_extras: []`, `regional_summary: true`, `spend_strategy`, `projection_notes`
    - Add `## Analysis Focus` section with market-specific analytical notes
    - _Requirements: 3.1, 3.2, 3.4_

- [x] 4. Create consolidated agent files
  - [x] 4.1 Create `market-analyst.md` at `~/shared/.kiro/agents/wbr-callouts/market-analyst.md`
    - Single parameterized agent that accepts `market` and `week` parameters
    - Generic analysis workflow: data freshness check → query prior observations → pull structured data → read narrative context → produce analysis → write projection → write agent state
    - Read `{market}-context.md` for market-specific rules (has_yoy, has_ieccp, headline_extras, etc.)
    - Conditionally include/exclude YoY assessment based on `has_yoy` config
    - Conditionally include ie%CCP analysis based on `has_ieccp` config
    - Include agent state write protocol: call `log_agent_action()` after analysis, call `log_agent_observation()` for anomalies, patterns, projection accuracy
    - Include `query_prior_observations()` call at run start for learned experience
    - Use `source: 'market-analyst'` uniformly in projection writes
    - Support `report_type` parameter (default 'wbr') for future MBR reuse
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 4.3, 5.4, 5.5, 9.1, 9.3, 10.1_

  - [x] 4.2 Create `callout-writer.md` at `~/shared/.kiro/agents/wbr-callouts/callout-writer.md`
    - Single parameterized agent that accepts `market` and `week` parameters
    - Read analysis brief produced by market-analyst
    - Read `{market}-context.md` for market-specific writing rules
    - Read `callout-principles.md` on every invocation
    - Conditionally include ie%CCP in headline based on `has_ieccp` config
    - Conditionally omit YoY paragraph based on `has_yoy` config
    - Conditionally produce regional summary based on `regional_summary` config
    - Include agent state write protocol: call `log_agent_action()` after writing
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 4.4, 9.2, 9.4_

- [x] 5. Update pipeline hook
  - [x] 5.1 Update `wbr-callout-pipeline` hook to dispatch to consolidated agents
    - Phase 2 (Analysis): 10 sequential `market-analyst` invocations, one per market, passing `market` and `week` as explicit parameters
    - Phase 3 (Writing): 10 sequential `callout-writer` invocations, one per market
    - Phase 4 (Review): Unchanged — single `callout-reviewer` invocation
    - Market ordering: AU and MX first, then US, CA, JP, UK, DE, FR, IT, ES
    - Add verification step after Phase 2: check that analysis brief exists for each market before proceeding to Phase 3
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 6. Update routing directory and documentation
  - [x] 6.1 Update Agent Routing Directory in `~/.kiro/steering/soul.md`
    - Replace 3 analyst routing entries (abix-analyst, najp-analyst, eu5-analyst) with single `market-analyst` entry
    - Replace 3 writer routing entries (abix-callout-writer, najp-callout-writer, eu5-callout-writer) with single `callout-writer` entry
    - Route any "Write W__ callouts" request to `market-analyst` → `callout-writer` regardless of market
    - Preserve `callout-reviewer` routing entry unchanged
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

  - [x] 6.2 Update WBR Callout Pipeline entry in `~/shared/context/body/device.md`
    - Reference consolidated agent names (market-analyst, callout-writer)
    - Describe single-market dispatch pattern
    - Document agent state wiring (actions, observations, prior observation queries)
    - _Requirements: 12.1, 12.2_

- [x] 7. Checkpoint — Verify consolidated agents before evaluation
  - Ensure all new agent files, context file updates, hook updates, and routing changes are in place. Ask the user if questions arise.

- [x] 8. Blind architecture evaluation
  - [x] 8.1 Snapshot before: run old agents on AU, MX, and UK
    - Run `abix-analyst` on AU and MX for the latest available week, save output artifacts (analysis briefs, projections)
    - Run `eu5-analyst` on UK for the same week, save output artifacts
    - Run `abix-callout-writer` on AU and MX, save callout drafts
    - Run `eu5-callout-writer` on UK, save callout draft
    - Store all "before" artifacts in a temporary comparison directory
    - _Requirements: 13.1_

  - [x] 8.2 Run after: run consolidated agents on AU, MX, and UK
    - Run `market-analyst` with `market=AU`, `market=MX`, `market=UK` for the same week
    - Run `callout-writer` with `market=AU`, `market=MX`, `market=UK`
    - Store all "after" artifacts in the comparison directory
    - _Requirements: 13.2_

  - [x] 8.3 Spawn blind evaluator and score
    - Create a fresh evaluation prompt that receives only before/after outputs and input data
    - Evaluator has NO knowledge of what changed (no design doc, no task list, no diff)
    - Score 5 evaluation questions: factual equivalence, quality comparison, data contradiction, gap detection, decision utility
    - Each question scored as PASS, REGRESS, or NEUTRAL
    - If 2+ REGRESS: REJECTED — revert consolidation and investigate
    - If 0 REGRESS + at least 1 PASS: APPROVED
    - If 1 REGRESS: APPROVED WITH NOTES
    - Log result to `agent_observations` via `log_architecture_eval()`
    - _Requirements: 13.3, 13.4, 13.5, 13.6_

- [x] 9. Delete old agent files
  - [x] 9.1 Delete the 6 old region-specific agent files
    - Delete: `abix-analyst.md`, `najp-analyst.md`, `eu5-analyst.md`, `abix-callout-writer.md`, `najp-callout-writer.md`, `eu5-callout-writer.md` from `~/shared/.kiro/agents/wbr-callouts/`
    - Only proceed after blind evaluation is APPROVED or APPROVED WITH NOTES
    - Verify pipeline hook references only `market-analyst` and `callout-writer`
    - Verify routing directory contains no references to old agent names
    - _Requirements: 11.1, 11.2, 11.3_

- [x] 10. Final checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
  - Verify: 3 agent files remain in `wbr-callouts/` (market-analyst.md, callout-writer.md, callout-reviewer.md)
  - Verify: all 10 context files have `## Agent Configuration` sections
  - Verify: `query.py` has 4 new functions (log_agent_action, log_agent_observation, query_prior_observations, log_architecture_eval)
  - Verify: routing directory and device.md reflect consolidated architecture

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- The blind architecture evaluation (task 8) is mandatory before old agent cleanup (task 9) — this is a hard gate
- Property tests validate the query.py functions; the agent prompt files are validated by the blind evaluation
- The architecture-eval-protocol.md steering file already exists at `~/shared/.kiro/steering/architecture-eval-protocol.md` (Requirement 14 is already satisfied)
- Part 3 pipeline framework items (pipeline_registry.py, MBR pipeline, wiki state wiring) are designed but not built in this spec — they're future work
