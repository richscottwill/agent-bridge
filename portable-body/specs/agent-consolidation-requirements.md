# Requirements Document

## Introduction

This document defines the requirements for the Agent Consolidation and State Wiring feature — consolidating 7 agent files (3 analysts + 3 writers + 1 reviewer) into 3 (1 parameterized analyst + 1 parameterized writer + 1 unchanged reviewer), externalizing market-specific knowledge into per-market context files, and wiring the Phase B agent state tables so agents build memory across sessions. The consolidated agents accept a market parameter at runtime, read `{market}-context.md` for market-specific rules, write actions and observations to DuckDB after each run, and query prior observations at the start of each run.

## Glossary

- **Market_Analyst**: The consolidated `market-analyst.md` agent that replaces `abix-analyst.md`, `najp-analyst.md`, and `eu5-analyst.md`. Accepts a market parameter and reads market-specific rules from context files at runtime.
- **Callout_Writer**: The consolidated `callout-writer.md` agent that replaces `abix-callout-writer.md`, `najp-callout-writer.md`, and `eu5-callout-writer.md`. Accepts a market parameter and reads market-specific writing rules from context files.
- **Callout_Reviewer**: The existing `callout-reviewer.md` agent, unchanged in structure but updated to write observations to DuckDB.
- **Pipeline_Hook**: The `wbr-callout-pipeline.kiro.hook` that orchestrates the sequential invocation of agents across all 10 markets.
- **Market_Context_File**: A per-market `{market}-context.md` file containing market-specific analytical rules, writing rules, and a structured `## Agent Configuration` section.
- **Agent_State_Writer**: The set of functions in `query.py` (`log_agent_action`, `log_agent_observation`, `query_prior_observations`) that provide agent memory and audit trail via DuckDB.
- **Routing_Directory**: The Agent Routing Directory table in `soul.md` that maps request triggers to agent files.

## Requirements

### Requirement 1: Parameterized Market Analyst

**User Story:** As a pipeline operator, I want a single analyst agent that accepts a market parameter, so that I maintain one agent file instead of three near-identical copies.

#### Acceptance Criteria

1. WHEN the Pipeline_Hook invokes the Market_Analyst with a valid market code and week, THE Market_Analyst SHALL read `{market}-context.md` and produce an analysis brief at `{market}-analysis-{year}-w{NN}.md`
2. WHEN the Market_Analyst processes a market where `has_yoy` is false in the Agent Configuration, THE Market_Analyst SHALL omit the YoY assessment section from the analysis brief
3. WHEN the Market_Analyst processes a market where `has_ieccp` is true in the Agent Configuration, THE Market_Analyst SHALL include ie%CCP analysis in the analysis brief
4. WHEN the Market_Analyst completes analysis for a market, THE Market_Analyst SHALL write a projection to the projections table via `db_upsert()` with key columns `[market, week]`
5. WHEN the Market_Analyst processes market X, THE Market_Analyst SHALL read only `{X}-context.md` for market-specific rules and not read any other market's context file during that run
6. THE Market_Analyst SHALL follow the same generic analysis workflow for all markets: data freshness check, structured data pull, narrative context read, analysis production, projection write, state write

### Requirement 2: Parameterized Callout Writer

**User Story:** As a pipeline operator, I want a single callout writer agent that accepts a market parameter, so that I maintain one writer file instead of three near-identical copies.

#### Acceptance Criteria

1. WHEN the Pipeline_Hook invokes the Callout_Writer with a valid market code and week, THE Callout_Writer SHALL read the analysis brief and produce a callout draft at `{market}-{year}-w{NN}.md`
2. WHEN the Callout_Writer processes a market where `has_ieccp` is true, THE Callout_Writer SHALL include ie%CCP in the callout headline
3. WHEN the Callout_Writer processes a market where `has_yoy` is false, THE Callout_Writer SHALL omit the YoY paragraph from the callout
4. WHEN the Callout_Writer processes a market where `regional_summary` is true, THE Callout_Writer SHALL produce a regional summary file in addition to the individual callout
5. THE Callout_Writer SHALL read `callout-principles.md` for universal style rules on every invocation regardless of market

### Requirement 3: Per-Market Context File Enhancement

**User Story:** As a pipeline operator, I want structured Agent Configuration sections in per-market context files, so that consolidated agents can parse market-specific rules reliably without hardcoding.

#### Acceptance Criteria

1. THE Market_Context_File for each of the 10 markets (AU, MX, US, CA, JP, UK, DE, FR, IT, ES) SHALL contain an `## Agent Configuration` section
2. THE Agent Configuration section SHALL include all required fields: `markets`, `has_yoy`, `has_ieccp`, `headline_extras`, `regional_summary`, `spend_strategy`
3. IF a Market_Context_File is missing the `## Agent Configuration` section, THEN THE Market_Analyst SHALL log an error action with `requires_human_review = true` and stop processing that market
4. WHEN a Market_Context_File is edited to change a configuration field, THE Market_Analyst SHALL reflect the updated value on the next pipeline run without any agent prompt changes

### Requirement 4: Agent Action Logging

**User Story:** As a system operator, I want every agent run to log its actions to DuckDB, so that I have an auditable record of what each agent did and when.

#### Acceptance Criteria

1. WHEN `log_agent_action()` is called with valid parameters, THE Agent_State_Writer SHALL insert a new row into the `agent_actions` table with an auto-incremented ID from the `agent_actions_seq` sequence
2. WHEN `log_agent_action()` completes, THE Agent_State_Writer SHALL close the database connection
3. WHEN the Market_Analyst completes a run, THE Market_Analyst SHALL call `log_agent_action()` with agent name, action type, market, week, description, output summary, and confidence
4. WHEN the Callout_Writer completes a run, THE Callout_Writer SHALL call `log_agent_action()` with agent name, action type, market, week, and description
5. WHEN the Callout_Reviewer completes a run, THE Callout_Reviewer SHALL call `log_agent_action()` with agent name, action type, and week
6. IF `log_agent_action()` fails due to a database error, THEN THE Agent_State_Writer SHALL raise the exception without blocking the calling agent's primary output

### Requirement 5: Agent Observation Logging

**User Story:** As a system architect, I want agents to record observations (anomalies, patterns, projection accuracy) to DuckDB, so that agents build learned experience across sessions.

#### Acceptance Criteria

1. WHEN `log_agent_observation()` is called with valid parameters, THE Agent_State_Writer SHALL insert a new row into the `agent_observations` table with an auto-incremented ID from the `agent_observations_seq` sequence
2. WHEN `log_agent_observation()` inserts a row, THE Agent_State_Writer SHALL set `acted_on` to false by default
3. WHEN `log_agent_observation()` completes, THE Agent_State_Writer SHALL close the database connection
4. WHEN the Market_Analyst detects a metric deviating more than 20% from the 8-week average, THE Market_Analyst SHALL call `log_agent_observation()` with observation_type `anomaly`
5. WHEN the Market_Analyst compares the prior week's projection to actual results, THE Market_Analyst SHALL call `log_agent_observation()` with observation_type `projection_accuracy`
6. WHEN the Callout_Reviewer identifies a cross-market quality pattern, THE Callout_Reviewer SHALL call `log_agent_observation()` with the relevant market and observation type

### Requirement 6: Prior Observation Querying

**User Story:** As an analyst agent, I want to query my prior observations for a market before starting analysis, so that I can incorporate learned experience into the current run.

#### Acceptance Criteria

1. WHEN `query_prior_observations()` is called with a market code and weeks parameter, THE Agent_State_Writer SHALL return observations from the last `weeks * 7` days for that market, ordered by `created_at` descending
2. WHEN `query_prior_observations()` is called with an `observation_type` filter, THE Agent_State_Writer SHALL return only observations matching that type
3. WHEN no observations exist for the specified market and time window, THE Agent_State_Writer SHALL return an empty list
4. WHEN `query_prior_observations()` executes, THE Agent_State_Writer SHALL open a read-only database connection
5. WHEN `query_prior_observations()` completes, THE Agent_State_Writer SHALL close the database connection

### Requirement 7: Pipeline Hook Update

**User Story:** As a pipeline operator, I want the pipeline hook to dispatch single-market runs to consolidated agents, so that the pipeline uses 2 agent files instead of 6 for analysis and writing.

#### Acceptance Criteria

1. WHEN the Pipeline_Hook runs Phase 2 (Analysis), THE Pipeline_Hook SHALL invoke the Market_Analyst once per market for all 10 markets sequentially
2. WHEN the Pipeline_Hook runs Phase 3 (Writing), THE Pipeline_Hook SHALL invoke the Callout_Writer once per market for all 10 markets sequentially
3. WHEN the Pipeline_Hook runs Phase 4 (Review), THE Pipeline_Hook SHALL invoke the Callout_Reviewer once for all markets
4. WHEN the Pipeline_Hook invokes the Market_Analyst, THE Pipeline_Hook SHALL pass the market code and week as explicit parameters in the invocation prompt
5. WHEN the Pipeline_Hook completes Phase 2, THE Pipeline_Hook SHALL verify that an analysis brief exists for each of the 10 markets before proceeding to Phase 3

### Requirement 8: Routing Directory Update

**User Story:** As a system operator, I want the Agent Routing Directory in soul.md to reference consolidated agents, so that routing rules are accurate and simplified.

#### Acceptance Criteria

1. WHEN the Routing_Directory is updated, THE Routing_Directory SHALL replace the three analyst routing entries (`abix-analyst`, `najp-analyst`, `eu5-analyst`) with a single `market-analyst` entry
2. WHEN the Routing_Directory is updated, THE Routing_Directory SHALL replace the three writer routing entries (`abix-callout-writer`, `najp-callout-writer`, `eu5-callout-writer`) with a single `callout-writer` entry
3. THE Routing_Directory SHALL route any "Write W__ callouts" request to `market-analyst` followed by `callout-writer` regardless of which market is specified
4. THE Routing_Directory SHALL preserve the `callout-reviewer` routing entry unchanged

### Requirement 9: Output Backward Compatibility

**User Story:** As a callout consumer, I want the consolidated agents to produce output files with identical structure and paths as the old agents, so that downstream consumers see no change.

#### Acceptance Criteria

1. THE Market_Analyst SHALL produce analysis brief files at the same paths as the region-specific analysts: `{market}-analysis-{year}-w{NN}.md`
2. THE Callout_Writer SHALL produce callout draft files at the same paths as the region-specific writers: `{market}-{year}-w{NN}.md`
3. THE Market_Analyst SHALL produce analysis briefs with the same section structure (registration drivers, trend context, YoY assessment, monthly projection, flags) as the region-specific analysts
4. THE Callout_Writer SHALL produce callouts with the same structure (headline, WoW paragraph, YoY paragraph, Note, supplementary section) as the region-specific writers

### Requirement 10: Idempotent Projection Writes

**User Story:** As a system operator, I want projection writes to be idempotent on market+week, so that re-running the analyst for the same market and week updates the existing projection instead of creating duplicates.

#### Acceptance Criteria

1. WHEN the Market_Analyst writes a projection via `db_upsert()` with key columns `[market, week]`, THE Query_Helper SHALL update the existing row if a row with the same market and week exists
2. WHEN the Market_Analyst writes a projection for a market+week combination that does not exist, THE Query_Helper SHALL insert a new row
3. WHEN the Market_Analyst is run twice for the same market and week, THE projections table SHALL contain exactly one row for that market+week combination

### Requirement 11: Old Agent File Cleanup

**User Story:** As a system maintainer, I want the old region-specific agent files deleted after consolidation is verified, so that the codebase trends toward subtraction.

#### Acceptance Criteria

1. WHEN consolidation is verified working for all 10 markets, THE system SHALL delete the 6 old agent files: `abix-analyst.md`, `najp-analyst.md`, `eu5-analyst.md`, `abix-callout-writer.md`, `najp-callout-writer.md`, `eu5-callout-writer.md`
2. WHEN old agent files are deleted, THE Pipeline_Hook SHALL reference only `market-analyst` and `callout-writer`
3. WHEN old agent files are deleted, THE Routing_Directory SHALL contain no references to the old agent names

### Requirement 12: Documentation Update

**User Story:** As a system operator, I want device.md updated to reflect the consolidated pipeline, so that documentation matches the actual system state.

#### Acceptance Criteria

1. WHEN consolidation is complete, THE system SHALL update the WBR Callout Pipeline entry in `device.md` to reference the consolidated agent names and the single-market dispatch pattern
2. THE documentation SHALL describe the agent state wiring (actions, observations, prior observation queries) as part of the pipeline description

### Requirement 13: Blind Architecture Evaluation

**User Story:** As a system architect, I want every architecture change validated by a blind evaluator that doesn't know what changed, so that I have objective evidence that the change improved or maintained output quality.

#### Acceptance Criteria

1. BEFORE the consolidated agents replace the old agents, THE system SHALL run the old agents on AU, MX, and UK for the latest available week and save the output artifacts
2. AFTER the consolidated agents are implemented, THE system SHALL run the new agents on the same markets and week and save the output artifacts
3. THE system SHALL spawn a blind evaluator agent that receives only the before/after outputs and input data, with no knowledge of what changed
4. THE blind evaluator SHALL score 5 evaluation questions (factual equivalence, quality comparison, data contradiction, gap detection, decision utility) as PASS, REGRESS, or NEUTRAL
5. IF the blind evaluator scores 2 or more REGRESS, THE system SHALL revert the consolidation and investigate
6. THE evaluation result SHALL be logged to `agent_observations` with `observation_type = 'architecture_eval'`
7. THE `log_architecture_eval()` function SHALL be added to `query.py` as a convenience wrapper for logging evaluation results

### Requirement 14: Reusable Evaluation Protocol

**User Story:** As a system architect, I want the blind evaluation protocol documented as a reusable steering file, so that all future architecture changes follow the same rigor.

#### Acceptance Criteria

1. THE system SHALL create a steering file at `shared/.kiro/steering/architecture-eval-protocol.md` documenting the full protocol
2. THE steering file SHALL specify when the protocol is required and when it is not
3. THE steering file SHALL be referenced in the design doc's Testing Strategy section
