# Implementation Plan: Slack Deep Context

## Overview

Configuration-driven implementation across four phases: rsw-channel command center, conversation database, historical backfill, and ongoing enrichment. All artifacts are SQL DDL, JSON config, hook prompt modifications, and steering files. No application code.

## Tasks

- [x] 1. Phase 1 — rsw-channel Command Center
  - [x] 1.1 Add `rsw_channel_behavior` config block to `shared/context/active/slack-channel-registry.json`
    - Add the `rsw_channel_behavior` object with `channel_id`, `intake_scanning`, `richard_user_id`, `system_message_markers`, and `action_patterns` as defined in design section 1c
    - _Requirements: 3.1, 3.4, 3.5_

  - [x] 1.2 Modify `rw-morning-routine.kiro.hook` to post daily brief to rsw-channel
    - Add prompt instructions after daily brief generation: compose condensed Slack version (≤300 words, mrkdwn format), post to C0993SRL6FQ via `post_message`, pin the new message
    - Include failure handling: if `post_message` fails, log error to `slack-scan-state.json → last_scan.errors` and continue
    - Include the daily brief post format template from design section 1a (top 3, calendar, status, hot topics)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [x] 1.3 Validate canvas support and implement live dashboard
    - Add prompt instructions to test `canvas_create` on C0993SRL6FQ, then `canvas_update`
    - Document result in `shared/context/active/slack-ingestion-README.md`
    - If canvas supported: implement dashboard as pinned canvas with 6 sections (Today, Streak, Markets, Hot Topics, Pending Responses, Five Levels)
    - If not supported: implement as pinned message using Slack mrkdwn, updated via `edit_message`
    - Add `dashboard` state block to `slack-scan-state.json` (`implementation`, `canvas_supported`, `message_ts`, `last_updated`)
    - _Requirements: 2.1, 2.2, 2.4, 2.5, 2.6, 21.1, 21.2, 21.3, 21.4, 21.5_

  - [x] 1.4 Add dashboard update step to both hooks
    - Add prompt instructions to end of `rw-morning-routine.kiro.hook`: after daily brief post, update live dashboard with current data from organs
    - Add prompt instructions to `run-the-loop.kiro.hook`: after Phase 1 maintenance, update live dashboard
    - Dashboard content sourced from: hands.md, calendar, amcc.md, eyes.md, brain.md, slack-scan-state.json
    - _Requirements: 2.2, 2.3, 2.6_

  - [x] 1.5 Add intake drop zone scanning to hook prompts
    - Add prompt instructions to both `rw-morning-routine.kiro.hook` and `run-the-loop.kiro.hook`: when scanning rsw-channel, check each message author_id
    - Richard's messages (U040ECP305S) that don't match system markers → create intake file at `~/shared/context/intake/rsw-intake-{YYYYMMDD-HHmm}.md`
    - Include action pattern detection (`remind me to`, `follow up with`, `todo:`, etc.) → tag with `[ACTION-RW]`
    - Include file attachment handling via `download_file_content`
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 2. Checkpoint — Verify rsw-channel command center
  - Post a test daily brief, verify dashboard appears, drop a test message and confirm intake file creation. Ask Richard if questions arise.


- [x] 3. Phase 2 — DuckDB Conversation Database
  - [x] 3.1 Add CREATE TABLE statements to `shared/tools/data/schema.sql`
    - Append the four table definitions (`slack_messages`, `slack_threads`, `slack_people`, `slack_topics`) after existing table definitions
    - Use exact DDL from design section 2a: primary keys, column types, defaults, and row count comments
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 20.2_

  - [x] 3.2 Add ingestion pipeline instructions to hook prompts
    - Modify `rw-morning-routine.kiro.hook` prompt: after existing signal extraction, batch INSERT all messages to `slack_messages`, UPSERT thread summaries to `slack_threads`, UPSERT author records to `slack_people`
    - Modify `run-the-loop.kiro.hook` prompt: same parallel write path, plus UPSERT topic clusters to `slack_topics` when hot topic detection fires
    - Specify batch write at end of cycle, upsert on primary key (`INSERT OR REPLACE`), <30 second target
    - Include people tracking logic: new author → INSERT, existing → UPDATE counts and `last_interaction`
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

  - [x] 3.3 Add `backfill_scans` and `enrichment_state` blocks to `slack-scan-state.json`
    - Add `backfill_scans` object with all 6 scan types initialized to `status: "not_started"`
    - Add `enrichment_state` object with null timestamps for each enrichment process
    - Add `dashboard` state object
    - _Requirements: 19.4_

  - [x] 3.4 Verify query interface works against new tables
    - Run CREATE TABLE statements against ps-analytics.duckdb via `execute_query`
    - Verify tables exist with `list_tables` and `list_columns`
    - Run example queries from design section 2d to confirm empty tables respond correctly
    - _Requirements: 6.1, 6.4, 6.5, 6.6, 20.1_

- [x] 4. Checkpoint — Verify conversation database
  - Run one ingestion cycle, query each table to verify rows inserted. Ensure `SELECT COUNT(*) FROM slack_messages` > 0 after first cycle. Ask Richard if questions arise.

- [x] 5. Phase 3 — Historical Backfill Steering
  - [x] 5.1 Create `~/.kiro/steering/slack-deep-context.md` with backfill orchestration rules
    - Write the master steering file containing: backfill scan procedures, rate limit handling protocol, organ routing rules, word budget compliance, enrichment cadence rules
    - Include the common backfill pattern: trigger → read steering → construct queries → paginate → batch INSERT → synthesize → route to organ (or intake/ if over budget) → update scan-state
    - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5, 19.1, 19.5_

  - [x] 5.2 Add DM Archaeology scan instructions to steering file
    - For each People Watch contact: `batch_get_conversation_history` on DM channel, paginate full history
    - INSERT all DM messages to `slack_messages` with `is_richard` flag, UPDATE `slack_people` with enriched DM counts and response times
    - Synthesize per-contact: communication frequency, tone patterns, topic distribution, response latency
    - Flag high-DM-volume non-People-Watch contacts as candidates in `slack-scan-state.json → people_watch_candidates`
    - Route synthesis to `memory.md` (respect word budget, overflow to `intake/`)
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7_

  - [x] 5.3 Add Voice Corpus scan instructions to steering file
    - `search` with `from:@prichwil` across 12 months, paginate all results
    - INSERT all Richard messages to `slack_messages` with `is_richard = TRUE`
    - Analyze: sentence length, punctuation, emoji patterns, formality gradient (DM vs channel vs thread), opening/closing patterns, escalation/de-escalation language
    - Compare against `richard-writing-style.md` and note differences
    - Output to `~/shared/portable-body/voice/richard-style-slack.md`
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

  - [x] 5.4 Add Decision Mining scan instructions to steering file
    - `search` for decision language patterns ("decided", "going with", "confirmed", "approved", "let's do", "final call", "we're not going to") across team channels, 12 months
    - INSERT source messages to `slack_messages` with `signal_type = 'decision'`
    - INSERT extracted decisions to existing `decisions` table with `decision_type`, `market`, `description`, `rationale`, `made_by`, `created_at`
    - Synthesize high-impact decisions for `brain.md` decision log (respect word budget)
    - Map to existing decision principles where applicable
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7_

  - [x] 5.5 Add Project Timeline scan instructions to steering file
    - `search` for project name across all channels, full lifecycle (OCI, Polaris, Baloo, F90, ad copy overhaul, Walmart response)
    - INSERT project messages to `slack_messages` with project tagged in `signal_type`
    - Produce structured timeline: milestones, drivers, decisions, blockers, resolutions, source attribution
    - Cross-reference with existing wiki drafts, flag discrepancies
    - Route to `~/shared/context/intake/` for wiki and `current.md` processing
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

  - [x] 5.6 Add Stakeholder Position Mapping scan instructions to steering file
    - `search` for messages from key stakeholders (Kate Rundell, Brandon Munday, Lena Zak, Nick Georgijev) across all channels, 6 months
    - INSERT stakeholder messages to `slack_messages`, UPDATE `slack_people` with enriched data
    - Per-stakeholder synthesis: frequent topics, concern vs satisfaction language, escalation triggers, priority shifts
    - Route to `memory.md` relationship graph + meeting series files (respect word budget, overflow to `intake/`)
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_

  - [x] 5.7 Add Pre-Meeting Context scan instructions to steering file
    - Cross-reference meeting times from calendar with Slack activity: `search` for messages within 2 hours before/after each recurring meeting, 6 months
    - INSERT meeting-adjacent messages to `slack_messages` with meeting series metadata
    - Per-meeting-series synthesis: pre-meeting prep discussions, post-meeting follow-ups, unformalised action items
    - Route to corresponding meeting series files in `~/shared/context/meetings/`
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6_

- [x] 6. Checkpoint — Verify backfill steering
  - Trigger DM archaeology for one contact as smoke test. Verify `slack_messages` rows inserted, `slack_people` updated, synthesis routed correctly. Ask Richard if questions arise.


- [x] 7. Phase 4 — Ongoing Enrichment
  - [x] 7.1 Add weekly relationship graph refresh to `run-the-loop.kiro.hook`
    - Add Friday-only prompt block: query `slack_people` for 7-day interaction counts, check promotion threshold (3+ interactions for non-People-Watch), check dormancy (60+ days no interaction)
    - Update `slack_people.relationship_tier`, update `slack-scan-state.json → people_watch_candidates`
    - If changes detected: produce relationship delta summary → route to `memory.md`
    - If no changes: skip `memory.md` update
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6_

  - [x] 7.2 Add wiki pipeline candidate detection to `run-the-loop.kiro.hook`
    - Add weekly prompt block: query `slack_messages` for threads where Richard authored 200+ char messages with 3+ replies and explanatory language
    - Extract topic, explanation content, audience, thread link per candidate
    - Deduplicate against existing `wiki/demand-log.md` entries
    - Check for existing wiki article overlap, note in entry
    - Append new candidates to `~/shared/context/wiki/demand-log.md`
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5_

  - [x] 7.3 Add proactive draft detection to both hook prompts
    - Add to `rw-morning-routine.kiro.hook` and `run-the-loop.kiro.hook`: query `slack_messages` for unanswered messages directed at Richard (24+ hours old, no reaction, no reply)
    - Load `memory.md` tone notes + `richard-style-slack.md` for register
    - Load thread context from `slack_threads`
    - Post draft to rsw-channel: `[DRAFT for @{person} in #{channel}]: {draft text}`
    - Use `create_draft` when available, fall back to rsw-channel post
    - Skip messages where Richard reacted with any emoji
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5, 17.6_

  - [x] 7.4 Add monthly synthesis to `run-the-loop.kiro.hook`
    - Add first-of-month prompt block: query all 4 Slack tables for trailing 30 days
    - Produce synthesis: topic trends, new people, channel activity shifts, relationship changes
    - Route: strategic shifts → `brain.md`, relationship changes → `memory.md`, market shifts → `eyes.md`
    - Total output ≤500 words across all organ updates, respect gut.md word budgets
    - Flag 3+ week trending topics as wiki candidates in `demand-log.md`
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

  - [x] 7.5 Add quarterly stakeholder audit to `run-the-loop.kiro.hook`
    - Add QBR-aligned prompt block: query `slack_people` + `slack_messages` for per-stakeholder data, trailing 90 days
    - Per stakeholder: message volume, response time, topics, channel overlap, frequency trend
    - Compare current vs previous quarter: flag response time +50%, volume -30%
    - Calculate visibility gap metric
    - Route to `nervous-system.md` (Loop 9) and `memory.md`, respect word budgets
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_

- [x] 8. Final checkpoint — Full system verification
  - Verify all hook prompt modifications are consistent. Confirm guardrail compliance: review `tool_invocation_log` for no prohibited operations. Verify `schema.sql` matches live DuckDB. Confirm cold start behavior: enrichment queries work against DuckDB without Slack MCP. Ask Richard if questions arise.

## Notes

- This is a configuration-driven system. All tasks produce SQL DDL, JSON config, hook prompt text, or steering file content. No application code.
- Validation is manual smoke tests during hook execution, not automated test suites.
- Each task references specific requirements for traceability.
- Checkpoints ensure incremental validation between phases.
- The steering file (`~/.kiro/steering/slack-deep-context.md`) is the single source of truth for backfill and enrichment procedures.
