---
inclusion: auto
name: "Tech Context"
description: "MCP servers, hook architecture, Kiro configuration layers, DuckDB, Slack, Asana, Outlook, SharePoint, Hedy"
---

# Tech Context

## MCP Servers

This workspace connects to six MCP servers for external tool access:

- **Enterprise Asana** — Full read/write to Richard's Asana workspace (tasks, projects, portfolios, goals, status updates). Primary task management interface.
- **Slack** — Channel history, search, DM access, message posting, thread replies, file downloads. Primary communication and signal ingestion.
- **Outlook** — Email search, calendar view, meeting room booking, availability checks. Read-only by default.
- **DuckDB** — Local analytics database (`ps-analytics.duckdb`). Stores Slack conversation data, market metrics, decision logs.
- **SharePoint** — Document library access, file read/write, search across configured SharePoint domains.
- **Hedy Calendar** — Meeting ingestion and calendar operations (supplements Outlook calendar).

## Hook Architecture

Hooks automate recurring workflows via Kiro event triggers:

### Morning Routine (userTriggered, sequential)
- **AM-Auto** — Slack channel scan + Asana inbox + email triage + daily brief + calendar blocks.
- **AM-Triage** — Interactive task prioritization, reply drafting, To-Do list management.

### End of Day (userTriggered, sequential)
- **EOD-1: Meeting Sync** — Multi-source meeting ingestion (Hedy + Outlook) into meeting series files.
- **EOD-2: System Refresh** — Asana reconciliation, organ maintenance, experiment queue processing.

### Guards (preToolUse)
- **guard-calendar** — Calendar write protection.
- **guard-email** — Email send protection.
- **guard-asana** — Asana write guardrails (ownership check, whitelist/blacklist enforcement).

### Audit (postToolUse)
- **audit-asana-writes** — Logs every Asana write operation to audit trail.

### Automation
- **context-preloader** (promptSubmit) — Pre-loads relevant context based on user prompt keywords.
- **session-summary** (agentStop) — Writes session summary to intake after non-trivial sessions.
- **organ-change-detector** (fileEdited) — Flags cross-organ inconsistencies when body files change.

## Configuration Layers

1. **Steering files** (`~/.kiro/steering/`) — Agent behavior rules, inclusion modes (always, auto, fileMatch, manual)
2. **Skills** (`~/.kiro/skills/`) — Multi-step agent pipelines with SKILL.md instructions and optional scripts
3. **Hooks** (`~/.kiro/hooks/`) — Event-driven automation tied to Kiro lifecycle events
