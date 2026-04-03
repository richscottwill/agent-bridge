# Requirements Document

## Introduction

This document defines the requirements for optimizing Richard Williams' Kiro IDE configuration. The optimization covers steering file inclusion modes, skills expansion, hook improvements, context provider usage, powers evaluation, token/context budget analysis, and documentation of Kiro limitations. This is a configuration project — no application code is written. All changes involve editing YAML front matter, creating SKILL.md files, adjusting hook event types, and restructuring inclusion modes.

## Glossary

- **Steering_File**: A markdown file in `~/.kiro/steering/` with YAML front matter that controls when and how the file's content is loaded into the Kiro context window.
- **Front_Matter**: YAML metadata block at the top of a steering file that specifies inclusion mode, name, description, and other activation parameters.
- **Inclusion_Mode**: The `inclusion` field in front matter. Valid values: `always` (every interaction), `auto` (keyword-matched), `manual` (user-requested), `fileMatch` (glob-pattern matched).
- **Auto_Inclusion**: An inclusion mode where the steering file loads when keywords in its `description` field match the user's prompt or active context.
- **Skill**: A directory under `~/.kiro/skills/` containing a SKILL.md file with name, description, and instructions. Only the name/description loads at startup; full instructions load on match.
- **Hook**: A `.kiro.hook` file that defines automated behavior triggered by specific Kiro event types (e.g., userTriggered, preToolUse, postToolUse, promptSubmit, agentStop, fileEdited).
- **Token_Budget**: The total number of tokens consumed by always-loaded and auto-loaded steering files in a given interaction's context window.
- **Context_Provider**: A `#` prefixed reference (e.g., `#url`, `#mcp`, `#spec`, `#steering`) that loads external content into the Kiro chat context.
- **Power**: A dynamic MCP tool bundle from the Kiro marketplace that loads on-demand based on conversation keywords.
- **File_Reference**: A `#[[file:relative_path]]` syntax in steering files that loads the referenced file's content when the steering file is loaded.
- **Routing_Table**: The Agent Routing Directory in soul.md that maps trigger phrases to specialized agents.
- **Guard_Hook**: A `preToolUse` hook that inspects and conditionally blocks MCP tool calls before execution.
- **Audit_Hook**: A `postToolUse` hook that logs MCP tool call results after execution.

## Requirements

### Requirement 1: Steering File Inclusion Mode Optimization

**User Story:** As a Kiro user, I want steering files to load only when relevant to my current interaction, so that I reduce wasted context tokens and keep the context window lean for non-specialized tasks.

#### Acceptance Criteria

1. THE Steering_File system SHALL have exactly two files with `inclusion: always` after optimization: soul.md and context/pilot-steering.md
2. WHEN a steering file covers fewer than 3 topic areas, THE Front_Matter migration SHALL convert the file from `inclusion: always` to `inclusion: auto` with a non-empty `name` and `description` field
3. WHEN a steering file has `inclusion: auto`, THE Front_Matter SHALL contain a `description` field with at least 3 distinct keywords that trigger activation
4. WHEN a user prompt contains keywords matching an auto-inclusion steering file's description, THE Steering_File system SHALL load that file into the context window
5. WHEN a user prompt does not contain keywords matching an auto-inclusion steering file's description, THE Steering_File system SHALL not load that file into the context window
6. THE Steering_File migration SHALL preserve the body content of every file unchanged — only the front matter is modified
7. WHEN slack-guardrails.md is converted to auto inclusion, THE Front_Matter SHALL include keywords: "Slack", "message", "DM", "channel", "post"
8. WHEN amazon-builder-production-safety.md is converted to auto inclusion, THE Front_Matter SHALL include keywords: "AWS", "production", "credential", "delete"
9. WHEN process-execution.md is converted to auto inclusion, THE Front_Matter SHALL include keywords: "background", "nohup", "server", "npm"
10. WHEN file-creation-rules.md is converted to auto inclusion, THE Front_Matter SHALL include keywords: "create file", "write file", "save"

### Requirement 2: Steering File Merging

**User Story:** As a Kiro user, I want redundant steering files merged into a single file, so that I eliminate content duplication and reduce the total number of files loaded.

#### Acceptance Criteria

1. WHEN agentspaces-core.md and devspaces-core.md have overlapping content, THE Steering_File system SHALL merge them into a single environment-rules.md file with `inclusion: auto`
2. THE merged environment-rules.md SHALL contain every unique instruction, rule, and guideline from both source files with no content loss
3. WHEN the merge is complete, THE Steering_File system SHALL remove the original agentspaces-core.md and devspaces-core.md files
4. THE merged environment-rules.md Front_Matter SHALL include a description with keywords covering both DevSpaces and AgentSpaces domains

### Requirement 3: File References in Steering Files

**User Story:** As a Kiro user, I want steering files to reference live workspace files instead of duplicating content, so that steering files stay current when referenced content changes.

#### Acceptance Criteria

1. WHEN soul.md references Key Context Files with static paths, THE Steering_File SHALL replace the static path listing with a `#[[file:~/shared/context/body/body.md]]` file reference for the navigation layer
2. WHEN asana-guardrails.md contains hardcoded GID references, THE Steering_File SHALL replace them with a `#[[file:~/shared/context/active/asana-command-center.md]]` file reference
3. WHEN rw-task-prioritization.md restates strategic priorities, THE Steering_File SHALL replace the restatement with a `#[[file:~/shared/context/body/brain.md]]` file reference

### Requirement 4: Foundational Steering File Generation

**User Story:** As a Kiro user, I want product.md and tech.md foundational steering files generated for my workspace, so that Kiro has baseline context about the workspace purpose and technology stack without loading soul.md's full content.

#### Acceptance Criteria

1. THE Steering_File system SHALL generate a product.md file describing the body system, its purpose, and the Five Levels framework
2. THE Steering_File system SHALL generate a tech.md file describing MCP servers in use, hook architecture, and agent routing
3. THE generated product.md and tech.md SHALL follow Kiro's foundational steering file format

### Requirement 5: Skills Expansion from Routing Patterns

**User Story:** As a Kiro user, I want my agent routing patterns formalized as Kiro skills, so that routing instructions load on-demand instead of consuming tokens in every interaction via soul.md.

#### Acceptance Criteria

1. WHEN an agent routing pattern from soul.md is converted to a skill, THE Skill SHALL have a directory under `~/.kiro/skills/` containing a valid SKILL.md with name, description, and instructions
2. THE Skill system SHALL create skills for these 8 routing patterns: /wbr-callouts, /wiki-write, /wiki-search, /wiki-audit, /coach, /charts, /bridge-sync, /sharepoint-sync
3. WHEN a skill is created, THE SKILL.md description keywords SHALL be a superset of the corresponding routing table trigger phrases
4. WHEN a skill includes deterministic validation or file generation, THE Skill SHALL include a scripts/ directory with the relevant script files
5. WHEN a skill references external context files, THE Skill SHALL include a references/ directory with bundled reference files
6. WHEN skills are created for routing patterns, THE Routing_Table in soul.md SHALL be trimmed to remove entries fully covered by skills, retaining only karpathy, rw-trainer, and the routing rules paragraph

### Requirement 6: Soul.md Token Optimization

**User Story:** As a Kiro user, I want soul.md trimmed to reduce its always-loaded token cost, so that the baseline context budget is smaller without losing essential identity and routing information.

#### Acceptance Criteria

1. WHEN soul.md is trimmed, THE Steering_File SHALL retain these sections: Identity, Agent Voice, How I Work, What Matters, How I Build (6 principles), Five Levels, Agent Routing Directory (trimmed), and Instructions for Any Agent
2. WHEN the Influences section is removed from soul.md, THE Steering_File system SHALL create a separate influences.md file with `inclusion: manual`
3. WHEN the My Systems section is removed from soul.md, THE Steering_File system SHALL verify that body.md navigation provides equivalent information
4. THE optimized soul.md SHALL have a token cost of approximately 3,500 tokens or less, reduced from approximately 4,500 tokens

### Requirement 7: Asana Guard Hook

**User Story:** As a Kiro user, I want Asana write guardrails enforced structurally via a preToolUse hook, so that every Asana write operation is checked regardless of which hook, chat session, or skill triggered it.

#### Acceptance Criteria

1. THE Guard_Hook SHALL be a preToolUse hook that fires on all Asana MCP tool calls matching the pattern `@mcp.*asana.*`
2. WHEN an Asana read operation (Get*, Search*, List*) is detected, THE Guard_Hook SHALL grant access without restriction
3. WHEN an Asana write operation is detected on a task assigned to Richard (GID 1212732742544167), THE Guard_Hook SHALL check the whitelist and grant access or require draft-first review
4. WHEN an Asana write operation is detected on a task not assigned to Richard, THE Guard_Hook SHALL deny access
5. WHEN the Guard_Hook evaluates an operation, THE Guard_Hook SHALL log the result to asana-audit-log.jsonl

### Requirement 8: Asana Audit Hook

**User Story:** As a Kiro user, I want every Asana write operation automatically logged to an audit trail, so that I have a record of all modifications regardless of their source.

#### Acceptance Criteria

1. THE Audit_Hook SHALL be a postToolUse hook that fires on all Asana MCP tool calls matching the pattern `@mcp.*asana.*`
2. WHEN a write operation (UpdateTask, CreateTask, CreateTaskStory, SetParentForTask) completes, THE Audit_Hook SHALL append a log entry to ~/shared/context/active/asana-audit-log.jsonl
3. THE log entry SHALL contain: timestamp, tool name, task GID, fields modified, and result status
4. WHEN a read operation completes, THE Audit_Hook SHALL skip logging

### Requirement 9: Context Pre-Loader Hook

**User Story:** As a Kiro user, I want relevant context files pre-loaded before the agent processes my prompt, so that the agent has the right context without me manually specifying files.

#### Acceptance Criteria

1. THE Context_Pre-Loader SHALL be a promptSubmit hook that fires before every user prompt is processed
2. WHEN the hook fires, THE Context_Pre-Loader SHALL analyze the USER_PROMPT environment variable to determine which context files to load
3. THE Context_Pre-Loader SHALL execute as a runCommand type (not askAgent) to minimize latency

### Requirement 10: Session Summary Hook

**User Story:** As a Kiro user, I want substantive agent sessions automatically summarized and logged, so that the autoresearch loop has session data to work with.

#### Acceptance Criteria

1. THE Session_Summary hook SHALL be an agentStop hook that fires after every agent turn completes
2. WHEN a session involves tool calls, file modifications, or 3 or more conversation turns, THE Session_Summary hook SHALL append a summary to ~/shared/context/intake/session-log.md
3. THE summary SHALL contain: date, topic, key actions taken, and decisions made
4. WHEN a session consists of a single short response with no tool calls or file writes, THE Session_Summary hook SHALL skip logging

### Requirement 11: Organ Change Detector Hook

**User Story:** As a Kiro user, I want edits to body organ files automatically detected and checked for cross-organ coherence, so that organ modifications don't introduce inconsistencies.

#### Acceptance Criteria

1. THE Organ_Change_Detector SHALL be a fileEdited hook with fileGlob `**/shared/context/body/*.md`
2. WHEN an organ file is edited, THE Organ_Change_Detector SHALL check for cross-organ inconsistencies
3. WHEN heart.md or gut.md is edited, THE Organ_Change_Detector SHALL verify the edit was made by the karpathy agent
4. WHEN an organ change is detected, THE Organ_Change_Detector SHALL log the change to ~/shared/context/intake/organ-changes.md

### Requirement 12: Inline Guardrail Removal from Hooks

**User Story:** As a Kiro user, I want inline Asana guardrail text removed from individual hook prompts after the guard-asana hook is in place, so that guardrail enforcement is centralized and not duplicated across hooks.

#### Acceptance Criteria

1. WHEN the guard-asana preToolUse hook is active, THE Hook system SHALL remove inline GUARDRAILS sections from AM-1, AM-2, AM-3, and EOD-2 hook prompts
2. THE effective guardrail behavior after removal SHALL be identical to the behavior before removal — every write that was blocked remains blocked, every write that was allowed remains allowed

### Requirement 13: Context Provider Recommendations

**User Story:** As a Kiro user, I want documented recommendations for using Kiro context providers, so that I can load external content into chat more efficiently.

#### Acceptance Criteria

1. THE documentation SHALL recommend `#url` for pulling Quip documents and wiki pages into chat context
2. THE documentation SHALL recommend `#mcp` for inspecting available MCP tools and their parameters
3. THE documentation SHALL recommend `#spec` for loading active spec context into chat
4. THE documentation SHALL recommend `#steering` for referencing steering files during meta-work

### Requirement 14: Powers Evaluation

**User Story:** As a Kiro user, I want an assessment of marketplace powers against my current MCP setup, so that I know which powers would add value and which are redundant.

#### Acceptance Criteria

1. THE evaluation SHALL document that powers for Asana, Slack, DuckDB, and Calendar/Email are redundant with existing direct MCP connections
2. THE evaluation SHALL identify GitHub and Documentation powers as medium-value candidates for future evaluation
3. THE evaluation SHALL recommend monitoring the marketplace for powers offering capabilities beyond current MCP servers

### Requirement 15: Token Budget Reduction

**User Story:** As a Kiro user, I want the total always-loaded token cost reduced, so that more of the context window is available for actual work content.

#### Acceptance Criteria

1. THE optimized configuration SHALL reduce always-loaded tokens from approximately 8,000 to approximately 5,300 tokens
2. THE total token savings SHALL be approximately 3,500-3,700 tokens per typical non-specialized interaction when combined with soul.md trimming
3. WHEN auto-loaded files activate for a specialized interaction, THE Token_Budget SHALL add only the relevant files' tokens (not the full previous always-loaded set)

### Requirement 16: Kiro Limitations Documentation

**User Story:** As a Kiro user, I want Kiro's current limitations documented, so that I avoid wasted effort on unsupported capabilities and have workarounds for each limitation.

#### Acceptance Criteria

1. THE documentation SHALL list these unsupported capabilities: cross-workspace steering sync, hook chaining, conditional hook execution, hook scheduling/cron, steering file inheritance, dynamic inclusion mode, skill chaining, hook access to previous hook output, multi-model routing per hook, and steering file versioning
2. THE documentation SHALL provide a workaround for each listed limitation
3. THE documentation SHALL identify custom subagents as a significant Phase 2 opportunity for isolated agent context windows

### Requirement 17: fileMatch Inclusion for Hook-Specific Steering

**User Story:** As a Kiro user, I want hook-specific steering files to load automatically when their associated hooks are active, so that relevant context is available without manual loading.

#### Acceptance Criteria

1. WHEN rw-task-prioritization.md is converted to fileMatch inclusion, THE Front_Matter SHALL specify fileMatch patterns: `hooks/am-*` and `hooks/eod-*`
2. WHEN slack-deep-context.md is converted to fileMatch inclusion, THE Front_Matter SHALL specify fileMatch patterns: `hooks/*slack*` and `hooks/eod-2*`
3. WHEN slack-knowledge-search.md is converted to fileMatch inclusion, THE Front_Matter SHALL specify fileMatch pattern: `hooks/*slack*`
4. WHEN the active file matches a fileMatch pattern, THE Steering_File system SHALL load the corresponding steering file
5. WHEN the active file does not match any fileMatch pattern, THE Steering_File system SHALL not load the fileMatch steering file

### Requirement 18: Rollback Safety

**User Story:** As a Kiro user, I want all optimization changes to be reversible, so that I can revert any change that causes issues without data loss.

#### Acceptance Criteria

1. THE optimization process SHALL create backup copies of all steering files before modifying their front matter
2. THE optimization process SHALL retain original agentspaces-core.md and devspaces-core.md files until the merged environment-rules.md is verified
3. IF a skill is deleted, THEN THE Routing_Table in soul.md SHALL still contain the fallback routing entry for that agent pattern
4. IF a new hook causes issues, THEN THE Hook system SHALL allow deletion of the hook without affecting existing hooks or steering files
