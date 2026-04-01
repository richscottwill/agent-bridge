# Implementation Plan: Slack Context Ingestion

## Overview

Add Slack as a read-only context source for the Body system. Implementation is entirely configuration-driven: JSON config files, markdown steering rules, and modifications to existing hook prompts. No application code, no new hooks, no new agents.

Tasks are ordered by dependency: config files → steering rules → hook modifications → documentation.

## Tasks

- [ ] 1. Create Channel Registry configuration file
  - [x] 1.1 Create `~/shared/context/active/slack-channel-registry.json` with full schema
    - Include `version`, `last_updated`, `updated_by`, `tiers` definitions
    - Populate `channels` array with initial Tier 1 entries (rsw-channel C0993SRL6FQ with organ targets hands/current)
    - Populate `community_channels` array with all 6 knowledge search channels (agentspaces-interest, amazon-builder-genai-power-users, cps-ai-win-share-learn, bedrock-agentcore-interest, abma-genbi-analytics-interest, andes-workbench-interest) with IDs, member counts, and topics
    - Populate `people_watch` section: `always_high_relevance` (Brandon Munday), `boosted` list (Alexis Eck, Lena Zak, Lorena Alvarez Larrea, Yun-Kang Chu, Aditya Satish Thakur, Dwayne Palmer, Kate Rundell), `candidate_tracking` with threshold
    - Set `default_tier_for_new_channels` to 3
    - _Requirements: 1.1, 1.4, 1.5, 1.6, 3.1, 3.3, 3.5, 13.1, 15.2_

  - [x] 1.2 Validate Channel Registry is portable and human-readable
    - Ensure JSON is well-formatted with descriptive `notes` fields on each entry
    - Verify a new AI on a different platform could read and understand the file without MCP access
    - _Requirements: 1.6, 13.1_

- [x] 2. Create Scan State initial file
  - [x] 2.1 Create `~/shared/context/active/slack-scan-state.json` with empty initial state
    - Include `version`, `last_scan` (null/empty for cold start), empty `channels` object, empty `dm_conversations` object
    - Include `hot_topics` with empty `active` and `cooled` arrays
    - Include `volume_tracking` with `week_start` set to current Monday, zeroed `words_by_organ` for current/hands/memory/eyes/brain
    - Include empty `discovered_channels`, `people_watch_candidates`, and `tool_invocation_log` arrays
    - _Requirements: 8.1, 8.4, 8.5, 11.1, 12.5, 13.2, 14.4_

- [x] 3. Checkpoint — Verify config files
  - Ensure both JSON files are valid JSON and parseable
  - Verify file locations match the design (`~/shared/context/active/`)
  - Ask the user if questions arise

- [x] 4. Create Knowledge Search steering file
  - [x] 4.1 Create `~/.kiro/steering/slack-knowledge-search.md` with manual inclusion frontmatter
    - Add `---\ninclusion: manual\n---` frontmatter
    - Write "When to Search" section: triggers for MCP servers, CLI tools, Kiro features, AgentSpaces, Bedrock, Amazon internal tooling questions, and explicit user requests
    - Write "How to Search" section: use `search` tool, filter by community channels from registry, prefer last 90 days, prefer threads with replies, retrieve full thread replies via `batch_get_thread_replies`
    - Write "How to Present Results" section: include attribution (author, channel, timestamp, thread link), present as supplementary evidence, let Richard verify
    - Write "What NOT to Do" section: no writing to organs, no digest production, no scan state modification, no reporting failed searches, no searching community channels during scheduled scans
    - Write "Community Channels" section referencing `slack-channel-registry.json → community_channels`
    - _Requirements: 15.1, 15.3, 15.4, 15.5, 15.6, 15.7, 15.8_

- [ ] 5. Update Slack Guardrails steering file
  - [x] 5.1 Update `~/.kiro/steering/slack-guardrails.md` to add ingester-specific guardrails
    - Add an "Ingester Read Operations" section listing all allowed read tools: `search`, `batch_get_conversation_history`, `batch_get_thread_replies`, `batch_get_channel_info`, `batch_get_user_info`, `reaction_tool`, `download_file_content`, `list_channels`
    - Add explicit prohibition of `post_message`, `open_conversation`, `add_channel_members`, `create_channel` during ingestion cycles
    - Add note that `self_dm` is permitted for ingestion status summaries to Richard
    - Add note that all tool invocations during ingestion must be logged to `slack-scan-state.json → tool_invocation_log`
    - Preserve all existing guardrail content — this is additive only
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [x] 6. Checkpoint — Verify steering files
  - Ensure `slack-knowledge-search.md` has correct `inclusion: manual` frontmatter
  - Ensure `slack-guardrails.md` retains all existing rules and new ingester rules are additive
  - Ask the user if questions arise

- [x] 7. Modify Morning Routine hook to add Slack scanning
  - [x] 7.1 Add Slack scan substep to the CONTEXT LOAD section of `.kiro/hooks/rw-morning-routine.kiro.hook`
    - Insert after the existing context load items (after amcc.md) and before Step 1 (Asana Sync)
    - Add instructions to: load `slack-channel-registry.json`, load `slack-scan-state.json`, scan Tier 1 channels for messages since last morning routine timestamp, scan Tier 2 channels if interval elapsed, scan DM conversations with People Watch contacts, run Relevance Filter, produce `slack-digest-{timestamp}.md` in `intake/` if signals found, update `slack-scan-state.json`
    - Add error handling: on rate limit or API failure, log to scan state and continue with other data sources
    - Add cold start behavior: if scan state file doesn't exist, scan only last 24 hours
    - This must NOT be a new numbered step — it is an invisible substep within context load
    - _Requirements: 6.1, 6.6, 7.4, 8.1, 8.2, 8.4_

  - [x] 7.2 Add Slack Overnight section to the STEP 3 daily brief in `.kiro/hooks/rw-morning-routine.kiro.hook`
    - In PHASE 2 (DAILY BRIEF), add instructions to include a "SLACK OVERNIGHT" section if a Slack digest was produced during context load
    - Position between HEADS UP and TODAY sections in the brief section order
    - Include top 5 signals by relevance score, capped at 150 words
    - If signals contain `[ACTION-RW]` items, add them to the To-Do refresh in Phase 1
    - If no relevant Slack activity: omit the section entirely (silence = nothing happened)
    - Add design system details: same card-based dark navy layout, section header "SLACK OVERNIGHT" (10px uppercase, #4a5a78), each signal as one row with type icon + summary + source channel in secondary text, `[ACTION-RW]` items highlighted in amber (#d4880f)
    - _Requirements: 6.2, 6.3, 6.4, 6.5_

  - [x] 7.3 Add Relevance Filter instructions to the morning routine hook
    - Include the scoring model inline or by reference: direct mention (+100), manager messages (+100), People Watch boosted (+30), active project keyword (+25), keyword trigger (+20), Tier 1 channel (+15), decision language (+20), action assignment (+25), deadline language (+15), escalation language (+20), hot topic cluster (+15), thread >5 replies (+10)
    - Set relevance threshold at 25 points — messages below 25 are discarded
    - Include signal extraction rules: 6 signal types (decision, action-item, status-change, escalation, mention, topic-update) with trigger patterns
    - Include signal fields: type, source channel, thread_ts, author, timestamp, content summary (1-2 sentences), target organ, relevance score, action flag
    - Include digest format: hard cap 500 words, `[ACTION-RW]` prefix for Richard's action items, no digest if zero signals, plain markdown
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.2, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 14.1, 14.2_

- [x] 8. Modify System Refresh hook to add Slack ingestion
  - [x] 8.1 Add Slack ingestion substep to Phase 1 (Maintenance) of `.kiro/hooks/run-the-loop.kiro.hook`
    - Insert after "Refresh ground truth from email/calendar" and before "Process intake/"
    - Add instructions to: load `slack-channel-registry.json` and `slack-scan-state.json`, scan all Tier 1 channels (messages since last scan timestamp), scan Tier 2 channels if interval elapsed, scan DM conversations with People Watch contacts, run Relevance Filter and extract Signals, produce `slack-digest-{timestamp}.md` in `intake/` if signals found, update `slack-scan-state.json` including tool invocation log for audit
    - Add error handling: on rate limit or API error, log error and continue with other data sources
    - Add note that the Slack digest in `intake/` gets processed by the existing "Process intake/ using gut.md Digestion Protocol" substep
    - This must NOT be a new phase — it is a substep within existing Phase 1
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [x] 8.2 Add Slack signal routing instructions to Phase 2 (Cascade) of `.kiro/hooks/run-the-loop.kiro.hook`
    - Add organ routing rules: decision → brain.md + current.md, action-item → hands.md + current.md, status-change → current.md + eyes.md, escalation → current.md + hands.md, mention → current.md, topic-update → current.md + brain.md, relationship info → memory.md, market metrics → eyes.md
    - Add constraint: no new organ files created — all Slack signals absorbed into existing organs
    - Add constraint: before writing to an organ, check word budget in gut.md; compress or defer if at capacity
    - Add instruction: after routing all signals from a digest, delete the processed digest from `intake/`
    - Add source attribution rule: every Slack-sourced fact written to an organ includes `[Slack: #channel, author, date]` tag
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 14.3_

  - [x] 8.3 Add volume control and hot topic detection instructions to the system refresh hook
    - Add weekly cumulative tracking: update `volume_tracking` in scan state after each organ write
    - Add 20% ceiling rule: if cumulative Slack-sourced words for an organ exceed 20% of its word budget in a week, reduce scan frequency for channels feeding that organ
    - Add hot topic detection: when same topic appears in signals from 3+ channels within 24 hours, flag as hot topic in scan state and digest
    - Add hot topic cooling: if no new signals for 48 hours, move to `cooled` and stop boosting relevance
    - Add People Watch derivation: re-derive from memory.md during Phase 2 cascade, update `people_watch` in channel registry
    - Add new person detection: track unique Slack users in conversations with Richard, flag candidates at 3+ interactions in 7 days
    - Add DM monitoring: scan Richard's DM conversations with People Watch contacts, extract signals with same relevance filter, respect read-only guardrails
    - _Requirements: 3.5, 3.6, 10.1, 10.2, 10.3, 10.4, 10.5, 11.1, 11.2, 11.3, 11.4, 11.5, 14.4, 14.5_

- [x] 9. Checkpoint — Verify hook modifications
  - Ensure both hook files are valid JSON after modifications
  - Verify no new numbered steps or phases were added — Slack is a substep within existing phases
  - Verify morning routine hook still has all 4 original steps (5 on Fridays) intact
  - Verify system refresh hook still has all 6 original phases intact
  - Ask the user if questions arise

- [x] 10. Create README documentation
  - [x] 10.1 Create `~/shared/context/active/slack-ingestion-README.md`
    - Document the ingester's purpose: read-only Slack context source for the Body system
    - Document all configuration files and their locations: channel registry, scan state, knowledge search steering, slack guardrails
    - Document the scan logic: tiered scanning, relevance filter scoring model with all factors and thresholds, signal extraction types and trigger patterns
    - Document organ routing rules table: which signal types route to which organs
    - Document the digest format: 500 word cap, `[ACTION-RW]` prefix, transient lifecycle (intake → process → delete)
    - Document volume control: per-cycle cap, per-organ budget check, weekly cumulative tracking with 20% ceiling
    - Document hot topic detection and cooling logic
    - Document People Watch derivation from memory.md and new person candidate tracking
    - Document DM monitoring scope and read-only constraint
    - Document Knowledge Search: on-demand only, community channels, independent from scheduled scans
    - Document cold start behavior: scan last 24 hours only, no organ fails without Slack data
    - Document error handling: rate limits, MCP unavailability, malformed data fallbacks
    - Document guardrail compliance: read-only operations only, all invocations logged for audit
    - Ensure the README is self-contained — a new AI on a different platform can understand the full system from this file alone
    - _Requirements: 13.4, 13.5_

- [x] 11. Final checkpoint — Verify all files
  - Ensure all 7 implementation files exist and are consistent with each other:
    1. `~/shared/context/active/slack-channel-registry.json` (config)
    2. `~/shared/context/active/slack-scan-state.json` (initial state)
    3. `~/.kiro/steering/slack-knowledge-search.md` (steering)
    4. `~/.kiro/steering/slack-guardrails.md` (updated steering)
    5. `.kiro/hooks/rw-morning-routine.kiro.hook` (modified hook)
    6. `.kiro/hooks/run-the-loop.kiro.hook` (modified hook)
    7. `~/shared/context/active/slack-ingestion-README.md` (documentation)
  - Verify cross-references: channel IDs, file paths, organ names are consistent across all files
  - Verify no new hooks, agents, or organ files were created
  - Ensure all 15 requirements have coverage across the task list
  - Ask the user if questions arise

## Notes

- All implementation is configuration-driven: JSON, markdown, and hook prompt modifications. No application code.
- No new hooks, agents, or organ files. Slack scanning is a data source within existing hooks.
- Tasks are ordered by dependency: config files (1-2) → steering rules (4-5) → hook modifications (7-8) → documentation (10).
- Checkpoints (3, 6, 9, 11) ensure incremental validation at each layer.
- The design document contains full schemas, scoring models, and routing tables that the implementing agent should reference directly during execution.
