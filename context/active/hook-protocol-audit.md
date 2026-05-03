<!-- DOC-0356 | duck_id: active-hook-protocol-audit -->
# Hook & Protocol Audit — System Inventory

Last updated: 2026-04-12

This document maps every hook to its protocol file, trigger type, and health status. Read this when debugging hook behavior, onboarding a new environment, or auditing system completeness.

---

## File Event Hooks

| Hook | File | Trigger | Pattern | What It Does | Version | Status |
|------|------|---------|---------|-------------|---------|--------|
| Organ Change Detector | `organ-change-detector.kiro.hook` | fileEdited | `**/shared/context/body/*.md` | Checks cross-organ coherence, gates heart.md/gut.md edits to Karpathy | 1.0.0 | ✅ Active |
| Steering Integrity | `steering-integrity-check.kiro.hook` | fileCreated | `**/.kiro/steering/*.md` | Blocks resurrection of deleted steering files, checks front matter | 1.0.0 | ✅ Active |
| WBR Pipeline Trigger | `wbr-pipeline-trigger.kiro.hook` | fileCreated | `shared/uploads/sheets/*Dashboard*.xlsx` | Auto-runs WBR pipeline when dashboard xlsx is dropped | 1 | ✅ Active |

---

## Routine Hooks (daily sequence) **Sequence:** AM-Backend → AM-Frontend → (workday) → EOD **SharePoint sync:** AM-Backend pushes to `Kiro-Drive/system-state/` in Phase 6.5. EOD pushes in Phase 7.5. Both non-blocking. Published artifacts go to `Artifacts/wiki-sync/` via the separate sharepoint-sync hook (different pipeline, same MCP server). --- | Hook | File | Display Name | Trigger | Protocol File | Version | Status | |------|------|--------------|---------|--------------|---------|--------| | AM-Backend | `am-backend.kiro.hook` | `.AM-Backend` | userTriggered | `am-backend-parallel.md` | 5.2.1 | ✅ Active | | AM-Frontend | `am-frontend.kiro.hook` | `.AM-Frontend` | userTriggered | `am-frontend.md` + `am-triage.md` | 3.0.0 | ✅ Active | | EOD | `eod.kiro.hook` | `.EOD` | userTriggered | `eod-backend.md` + `eod-frontend.md` | 7.0.0 | ✅ Active | ## Guard Hooks (always-on, preToolUse)

| Hook | File | Trigger Pattern | What It Guards | Version | Status |
|------|------|----------------|---------------|---------|--------|
| Guard: Asana | `guard-asana.kiro.hook` | `@mcp.*asana.*` | Blocks writes to tasks not assigned to Richard | 1.0.0 | ✅ Active |
| Guard: Calendar | `guard-calendar.kiro.hook` | `.*calendar_meeting.*`, `.*calendar_event.*` | Blocks events with external attendees | 2 | ✅ Active |
| Guard: Email | `guard-email.kiro.hook` | `.*email_reply.*`, `.*email_send.*`, `.*email_forward.*` | Blocks outbound email to non-Richard addresses | 4 | ✅ Active |

**Critical:** These fire on EVERY matching tool call. They are the security layer. Never disable without explicit Richard approval.

---

### Details

3. The SharePoint durability layer means key artifacts survive platform migration. Pull from `Kiro-Drive/` to bootstrap.
4. DuckDB/MotherDuck data persists independently of the workspace.
5. Git repo (`~/shared/` → agent-bridge) is the third durability layer.

**Three-layer durability:** filesystem (`~/shared/`) + SharePoint (`Kiro-Drive/`) + git (agent-bridge). Any two can fail and the system recovers.

## Session Hooks

| Hook | File | Trigger | What It Does | Version | Status |
|------|------|---------|-------------|---------|--------|
| Context Pre-Loader | `context-preloader.kiro.hook` | promptSubmit | Placeholder — delegates to auto-inclusion steering | 1.0.0 | ⚠️ No-op (echo only) |
| Session Summary | `session-summary.kiro.hook` | agentStop | Appends session log to intake/session-log.md | 1.0.0 | ✅ Active |

**Note on Context Pre-Loader:** Currently a no-op (`echo` command). Original design was for a Python router (`route.py`) that would analyze the prompt and pre-load relevant organs. This was superseded by Kiro's auto-inclusion steering files (fileMatch patterns). The hook remains as a placeholder — it doesn't hurt anything but doesn't help either. Consider removing if it adds noise to hook execution logs.

---

## Audit Hooks (postToolUse)
| Hook | File | Trigger Pattern | What It Logs | Version | Status |
|------|------|----------------|-------------|---------|--------|
| Audit: Asana Writes | `audit-asana-writes.kiro.hook` | `@mcp.*asana.*` | Logs every Asana write to JSONL + DuckDB | 1.1.0 | ✅ Active |
---
## Known Issues

1. **context-preloader.kiro.hook** — is a no-op. Either remove it or implement the Python router it was designed for.
2. **ps-audit.kiro.hook** — references a Python CLI (`paid_search_audit.cli`) that may not exist in the current workspace. Needs verification.
3. **eod-meeting-sync.md** — and **eod-system-refresh.md** may be orphaned — the unified EOD hook now references eod-backend.md and eod-frontend.md directly.
4. **SharePoint sync** — in the sharepoint-sync.kiro.hook (on-demand wiki sync) is separate from the durability sync in AM/EOD. They serve different purposes but share the same MCP server.

---

*Example:* When this applies, the expected outcome is verified by checking the result.
## Protocol File Inventory

| Protocol | File | Used By | Purpose |
|----------|------|---------|---------|
| am-auto.md | `protocols/am-auto.md` | AM-Backend hook | Sequential processing phases after parallel ingestion |
| am-backend-parallel.md | `protocols/am-backend-parallel.md` | AM-Backend hook | Parallel subagent ingestion architecture |
| am-frontend.md | `protocols/am-frontend.md` | AM-Frontend hook | Interactive brief + triage + command center |
| am-triage.md | `protocols/am-triage.md` | AM-Frontend hook | Detailed triage logic (enrichment, ABPS AI, portfolio) |
| eod-backend.md | `protocols/eod-backend.md` | EOD hook | 7.5-phase autonomous backend |
| eod-frontend.md | `protocols/eod-frontend.md` | EOD hook | Interactive summary + decisions |
| eod-meeting-sync.md | `protocols/eod-meeting-sync.md` | (legacy) | Older meeting sync protocol — may be superseded by eod-backend Phase 1 |
| eod-system-refresh.md | `protocols/eod-system-refresh.md` | (legacy) | Older system refresh — may be superseded by eod-backend Phases 2-5 |
| sharepoint-durability-sync.md | `protocols/sharepoint-durability-sync.md` | AM + EOD hooks | Bidirectional SharePoint sync (push artifacts, pull on cold start) |
| asana-duckdb-sync.md | `protocols/asana-duckdb-sync.md` | AM + EOD hooks | Asana ↔ DuckDB delta sync |
| meeting-to-task-pipeline.md | `protocols/meeting-to-task-pipeline.md` | EOD Phase 1 | Extract action items from Hedy → Asana tasks |
| signal-to-task-pipeline.md | `protocols/signal-to-task-pipeline.md` | AM Phase 2 | Route Slack/email signals → Asana tasks |
| signal-intelligence.md | `protocols/signal-intelligence.md` | AM Phase 1 | Topic extraction, reinforcement detection, trending |
| slack-conversation-intelligence.md | `protocols/slack-conversation-intelligence.md` | AM Phase 1 | Acronym detection, KDS enrichment |
| communication-analytics.md | `protocols/communication-analytics.md` | EOD Phase 3 (Friday) | Weekly meeting speaking share + hedging trends |
| context-enrichment.md | `protocols/context-enrichment.md` | EOD Phase 3 | KDS/ARCC queries for active project context |
| email-calendar-duckdb-sync.md | `protocols/email-calendar-duckdb-sync.md` | AM Subagent C | Email + calendar → DuckDB sync |
| loop-page-sync.md | `protocols/loop-page-sync.md` | AM Subagent D | Loop page refresh → DuckDB |
| duckdb-schema-verification.md | `protocols/duckdb-schema-verification.md` | AM Phase 1 | Verify MotherDuck connection + schema |
| workflow-observability.md | `protocols/workflow-observability.md` | EOD Phase 3 | Query workflow reliability metrics |

---

## Legacy Protocols (may need cleanup)

| File | Status | Notes |
|------|--------|-------|
| eod-meeting-sync.md | Possibly superseded | EOD backend Phase 1 now handles meeting ingestion directly. Check if this is still referenced. |
| eod-system-refresh.md | Possibly superseded | EOD backend Phases 2-5 now handle reconciliation + maintenance. Check if this is still referenced. |

---

## Portability Notes

If migrating to a new platform:
1. Hook JSON files are Kiro-specific — they'd need to be translated to the new platform's automation format.
2. Protocol markdown files are platform-agnostic — any AI can read and execute them.

## On-Demand Hooks (userTriggered)

| Hook | File | What It Does | Version | Status |
|------|------|-------------|---------|--------|
| WBR Callouts | `wbr-callouts.kiro.hook` | Full 10-market callout pipeline (analyst → writer → reviewer) | 2 | ✅ Active |
| SharePoint Sync | `sharepoint-sync.kiro.hook` | Wiki-to-SharePoint sync via CLI | 1 | ✅ Active |
| Agent Bridge Sync | `agent-bridge-sync.kiro.hook` | Git push + email snapshot to personal email | 1 | ✅ Active |
| PS Audit | `ps-audit.kiro.hook` | Paid search audit pipeline via Python CLI | 1 | ⚠️ Untested (CLI may not exist) |

---
