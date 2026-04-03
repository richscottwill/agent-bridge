# Implementation Plan: Kiro Setup Optimization

## Overview

Comprehensive audit and optimization of Richard's Kiro IDE configuration — steering file inclusion modes, skills, hooks, and context provider documentation. All tasks involve editing YAML front matter, creating/merging markdown files, writing .kiro.hook files, and creating SKILL.md directories. No application code.

## Tasks

- [x] 1. Backup and preparation
  - [x] 1.1 Create backup copies of all steering files before modification
    - Copy every file in `~/.kiro/steering/` to `~/.kiro/steering/.backup/` preserving directory structure
    - Include `context/pilot-steering.md` in the backup
    - _Requirements: 18.1, 18.2_

  - [x] 1.2 Audit current front matter on all steering files
    - Read and document the current `inclusion` mode for every steering file
    - Verify soul.md has no front matter (confirm baseline)
    - Verify which files currently have `inclusion: always`
    - _Requirements: 1.1_

- [x] 2. Steering file inclusion mode migration
  - [x] 2.1 Add explicit `inclusion: always` front matter to soul.md
    - Add YAML front matter block with `inclusion: always` to `~/.kiro/steering/soul.md`
    - Preserve all body content unchanged
    - _Requirements: 1.1, 1.6_

  - [x] 2.2 Convert slack-guardrails.md from always to auto
    - Update front matter: `inclusion: auto`, `name: "Slack Communication Guardrails"`, `description: "Rules for Slack messaging, DM posting, channel operations, ingestion cycles, audit logging"`
    - Verify description contains keywords: "Slack", "message", "DM", "channel", "post"
    - Preserve body content unchanged
    - _Requirements: 1.2, 1.3, 1.6, 1.7_

  - [x] 2.3 Convert amazon-builder-production-safety.md from always to auto
    - Update front matter: `inclusion: auto`, `name: "Production Safety"`, `description: "AWS credential safety, production resource protection, destructive action confirmation, IAM policies"`
    - Verify description contains keywords: "AWS", "production", "credential", "delete"
    - Preserve body content unchanged
    - _Requirements: 1.2, 1.3, 1.6, 1.8_

  - [x] 2.4 Convert process-execution.md from always to auto
    - Update front matter: `inclusion: auto`, `name: "Process Execution Rules"`, `description: "Background process template with nohup setsid for servers, npm commands, long-running processes"`
    - Verify description contains keywords: "background", "nohup", "server", "npm"
    - Preserve body content unchanged
    - _Requirements: 1.2, 1.3, 1.6, 1.9_

  - [x] 2.5 Convert file-creation-rules.md from always to auto
    - Update front matter: `inclusion: auto`, `name: "File Creation Rules"`, `description: "Where to create files: workspace directory, home directory, shared folder for persistence"`
    - Verify description contains keywords: "create file", "write file", "save"
    - Preserve body content unchanged
    - _Requirements: 1.2, 1.3, 1.6, 1.10_

  - [x] 2.6 Verify context/pilot-steering.md retains `inclusion: always`
    - Confirm front matter has `inclusion: always`
    - No changes to body content
    - _Requirements: 1.1_

- [x] 3. Checkpoint — Verify inclusion mode migration
  - Ensure all modified steering files have valid front matter (auto files have name + description with 3+ keywords, always files are exactly soul.md and pilot-steering.md). Ask the user if questions arise.

- [x] 4. Steering file merge: environment-rules.md
  - [x] 4.1 Merge agentspaces-core.md and devspaces-core.md into environment-rules.md
    - Read both source files and deduplicate content
    - Create `~/.kiro/steering/environment-rules.md` with front matter: `inclusion: auto`, `name: "Environment Rules"`, `description: "DevSpaces AgentSpaces container rules, workspace boundaries, Brazil build system, file operations"`
    - Merged file must contain every unique instruction from both sources
    - _Requirements: 2.1, 2.2, 2.4_

  - [x] 4.2 Remove original agentspaces-core.md and devspaces-core.md
    - Delete `~/.kiro/steering/agentspaces-core.md`
    - Delete `~/.kiro/steering/devspaces-core.md`
    - Verify backups exist in `.backup/` before deletion
    - _Requirements: 2.3_

- [x] 5. File references in steering files
  - [x] 5.1 Replace static Key Context Files paths in soul.md with file reference
    - Replace the "Key Context Files" section's static path listing with `#[[file:~/shared/context/body/body.md]]` for the navigation layer
    - Keep the section header; replace the content with the file reference
    - _Requirements: 3.1_

  - [x] 5.2 Add file reference to asana-guardrails.md for GID lookups
    - Replace hardcoded GID references with `#[[file:~/shared/context/active/asana-command-center.md]]`
    - _Requirements: 3.2_

  - [x] 5.3 Add file reference to rw-task-prioritization.md for strategic priorities
    - Replace restated Five Levels / strategic priorities with `#[[file:~/shared/context/body/brain.md]]`
    - _Requirements: 3.3_

- [x] 6. fileMatch inclusion for hook-specific steering
  - [x] 6.1 Convert rw-task-prioritization.md to fileMatch inclusion
    - Update front matter: `inclusion: fileMatch`, `fileMatch: ["hooks/am-*", "hooks/eod-*"]`
    - _Requirements: 17.1_

  - [x] 6.2 Convert slack-deep-context.md to fileMatch inclusion
    - Update front matter: `inclusion: fileMatch`, `fileMatch: ["hooks/*slack*", "hooks/eod-2*"]`
    - _Requirements: 17.2_

  - [x] 6.3 Convert slack-knowledge-search.md to fileMatch inclusion
    - Update front matter: `inclusion: fileMatch`, `fileMatch: ["hooks/*slack*"]`
    - _Requirements: 17.3_

- [x] 7. Soul.md token optimization
  - [x] 7.1 Move Influences section from soul.md to separate influences.md
    - Extract the "Influences (how I think)" section from soul.md
    - Create `~/.kiro/steering/influences.md` with `inclusion: manual`
    - Remove the section from soul.md
    - _Requirements: 6.2_

  - [x] 7.2 Remove My Systems section from soul.md
    - Verify `~/shared/context/body/body.md` provides equivalent navigation
    - Remove the "My Systems" section from soul.md
    - _Requirements: 6.3_

  - [x] 7.3 Trim Agent Routing Directory in soul.md
    - Remove routing entries now covered by skills (market-analyst, callout-reviewer, agent-bridge-sync, eyes-chart, wiki-editor, wiki-concierge, wiki-critic)
    - Retain: karpathy, rw-trainer, and the routing rules paragraph
    - _Requirements: 5.6, 6.1_

- [x] 8. Checkpoint — Verify steering optimization
  - Ensure soul.md retains Identity, Agent Voice, How I Work, What Matters, How I Build, Five Levels, trimmed Routing Directory, and Instructions for Any Agent. Verify environment-rules.md contains all unique content from both source files. Ask the user if questions arise.

- [x] 9. Foundational steering file generation
  - [x] 9.1 Generate product.md foundational steering file
    - Create `~/.kiro/steering/product.md` describing the body system, its purpose, and the Five Levels framework
    - Follow Kiro's foundational steering file format
    - _Requirements: 4.1, 4.3_

  - [x] 9.2 Generate tech.md foundational steering file
    - Create `~/.kiro/steering/tech.md` describing MCP servers in use (Asana, Slack, Outlook, DuckDB, Hedy, Calendar), hook architecture, and agent routing
    - Follow Kiro's foundational steering file format
    - _Requirements: 4.2, 4.3_

- [x] 10. Skills expansion
  - [x] 10.1 Create /wbr-callouts skill
    - Create `~/.kiro/skills/wbr-callouts/SKILL.md` with name, description (keywords: "WBR", "callout", "weekly callout"), and full pipeline instructions (ingest → analyst → writer → blind review → correction)
    - Create `~/.kiro/skills/wbr-callouts/scripts/validate-callout.sh` for word count compliance
    - Create `~/.kiro/skills/wbr-callouts/references/callout-principles.md`
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [x] 10.2 Create /wiki-write skill
    - Create `~/.kiro/skills/wiki-write/SKILL.md` with name, description (keywords: "write wiki", "document", "wiki article"), and pipeline instructions (editor → researcher → writer → critic → librarian)
    - _Requirements: 5.1, 5.2, 5.3_

  - [x] 10.3 Create /wiki-search skill
    - Create `~/.kiro/skills/wiki-search/SKILL.md` with name, description (keywords: "search wiki", "find doc", "do we have"), and concierge instructions
    - _Requirements: 5.1, 5.2, 5.3_

  - [x] 10.4 Create /wiki-audit skill
    - Create `~/.kiro/skills/wiki-audit/SKILL.md` with name, description (keywords: "audit wiki", "stale docs"), and critic instructions
    - _Requirements: 5.1, 5.2, 5.3_

  - [x] 10.5 Create /coach skill
    - Create `~/.kiro/skills/coach/SKILL.md` with name, description (keywords: "coaching", "career", "1:1 prep", "retrospective", "growth"), and rw-trainer instructions
    - _Requirements: 5.1, 5.2, 5.3_

  - [x] 10.6 Create /charts skill
    - Create `~/.kiro/skills/charts/SKILL.md` with name, description (keywords: "chart", "dashboard", "visualize"), and eyes-chart instructions
    - Create `~/.kiro/skills/charts/scripts/generate.sh` wrapping `python3 ~/shared/tools/progress-charts/generate.py`
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 10.7 Create /bridge-sync skill
    - Create `~/.kiro/skills/bridge-sync/SKILL.md` with name, description (keywords: "sync to git", "bridge sync", "portable body"), and sync instructions
    - Create `~/.kiro/skills/bridge-sync/scripts/sync.sh` for git operations
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 10.8 Create /sharepoint-sync skill
    - Create `~/.kiro/skills/sharepoint-sync/SKILL.md` with name, description (keywords: "sync to SharePoint", "SharePoint"), and sync instructions
    - Create `~/.kiro/skills/sharepoint-sync/scripts/sync.sh` wrapping cli.py
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [x] 11. Checkpoint — Verify skills and soul.md trimming
  - Ensure all 8 skill directories exist with valid SKILL.md files. Verify soul.md routing table retains only karpathy, rw-trainer, and routing rules. Ask the user if questions arise.

- [x] 12. New hooks
  - [x] 12.1 Create guard-asana.kiro.hook (preToolUse)
    - Create `~/.kiro/hooks/guard-asana.kiro.hook` as a preToolUse hook on `@mcp.*asana.*`
    - Prompt: classify read vs write, check assignee GID for writes, enforce whitelist, log to asana-audit-log.jsonl
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [x] 12.2 Create audit-asana-writes.kiro.hook (postToolUse)
    - Create `~/.kiro/hooks/audit-asana-writes.kiro.hook` as a postToolUse hook on `@mcp.*asana.*`
    - Prompt: log write operations (UpdateTask, CreateTask, CreateTaskStory, SetParentForTask) to `~/shared/context/active/asana-audit-log.jsonl` with timestamp, tool, task_gid, fields_modified, result. Skip reads.
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

  - [x] 12.3 Create context-preloader.kiro.hook (promptSubmit)
    - Create `~/.kiro/hooks/context-preloader.kiro.hook` as a promptSubmit hook with runCommand type
    - Command: `echo "$USER_PROMPT" | python3 ~/shared/tools/context-router/route.py`
    - _Requirements: 9.1, 9.2, 9.3_

  - [x] 12.4 Create session-summary.kiro.hook (agentStop)
    - Create `~/.kiro/hooks/session-summary.kiro.hook` as an agentStop hook
    - Prompt: write 2-3 line summary to `~/shared/context/intake/session-log.md` only when session involved tool calls, file modifications, or 3+ turns. Skip trivial sessions.
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

  - [x] 12.5 Create organ-change-detector.kiro.hook (fileEdited)
    - Create `~/.kiro/hooks/organ-change-detector.kiro.hook` as a fileEdited hook with fileGlob `**/shared/context/body/*.md`
    - Prompt: check cross-organ inconsistencies, verify heart.md/gut.md edits are by karpathy, log to `~/shared/context/intake/organ-changes.md`
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [x] 13. Remove inline guardrails from existing hooks
  - [x] 13.1 Remove inline GUARDRAILS sections from AM-1, AM-2, AM-3, and EOD-2 hooks
    - Read each hook file and remove the GUARDRAILS: section from the prompt text
    - The guard-asana.kiro.hook now handles this structurally
    - Verify no other guardrail logic is lost
    - _Requirements: 12.1, 12.2_

- [x] 14. Checkpoint — Verify hooks
  - Ensure all 5 new hooks exist with correct event types and valid JSON structure. Verify inline guardrails are removed from AM/EOD hooks. Ask the user if questions arise.

- [x] 15. Documentation
  - [x] 15.1 Create context-provider-recommendations.md
    - Create `~/.kiro/steering/context/context-provider-recommendations.md` with `inclusion: manual`
    - Document recommendations for `#url` (Quip docs), `#mcp` (tool discovery), `#spec` (spec loading), `#steering` (meta-work)
    - _Requirements: 13.1, 13.2, 13.3, 13.4_

  - [x] 15.2 Create powers-evaluation.md
    - Create `~/.kiro/steering/context/powers-evaluation.md` with `inclusion: manual`
    - Document: Asana/Slack/DuckDB/Calendar powers are redundant with direct MCP; GitHub and Documentation powers are medium-value candidates; recommend monitoring marketplace
    - _Requirements: 14.1, 14.2, 14.3_

  - [x] 15.3 Create kiro-limitations.md
    - Create `~/.kiro/steering/context/kiro-limitations.md` with `inclusion: manual`
    - List all unsupported capabilities with workarounds: cross-workspace sync, hook chaining, conditional hooks, scheduling, inheritance, dynamic inclusion, skill chaining, hook output sharing, multi-model routing, steering versioning
    - Flag custom subagents as Phase 2 opportunity
    - _Requirements: 16.1, 16.2, 16.3_

- [x] 16. Final checkpoint — Full verification
  - Verify: exactly 2 always-loaded files (soul.md, pilot-steering.md). All auto files have name + description with 3+ keywords. environment-rules.md contains all content from both source files. 8 skills exist. 5 new hooks exist. Inline guardrails removed. Documentation files created. Backups intact. Ask the user if questions arise.

## Notes

- All tasks edit real files at real paths in `~/.kiro/` and `~/shared/context/`
- Backups in task 1.1 enable rollback per Requirement 18
- Tasks are sequenced so each builds on the previous — steering modes first, then merges, then skills (which depend on knowing what routing entries to trim), then hooks, then cleanup
- Checkpoints at tasks 3, 8, 11, 14, and 16 ensure incremental validation
- No application code is written — this is entirely configuration editing
