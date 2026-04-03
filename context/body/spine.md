# Spine — Structure & Continuity

*The skeleton that holds everything together across sessions. Bootstrap sequence, directory conventions, environment rules, and the ground-truth files that define Richard's current state.*

Last updated: 2026-04-01 (Wednesday PT)

---

## Session Bootstrap Sequence

**CRITICAL: AgentSpaces chats are deleted every 14 days.** At the start of every new session, read these files in order:

1. `~/shared/context/body/body.md` — The map of the whole system. Tells you what each organ does and where to find it.
2. `~/shared/context/body/spine.md` — This file. Bootstrap sequence, tool access, directory map.
3. `~/.kiro/steering/soul.md` — Identity, values, voice, preferences, agent routing.
4. `~/shared/context/active/current.md` — Ground truth: active projects, people, meetings, pending actions.
5. `~/shared/context/active/rw-tracker.md` — Weekly scorecard, 30-day challenge.

Then read the organ you need for the task at hand (brain, eyes, hands, memory).

---

## Richard's Role & Markets
- Amazon Business, Paid Search (WW Outbound Marketing under Brandon Munday L7)
- Owns: AU (Australia), MX (Mexico) hands-on; US/EU5/JP/CA team-wide
- Key focus: OCI bidding rollout, AI Max testing, Answer Engine Optimization, Project Baloo, F90 Lifecycle
- Timezone: PT (UTC-7). System clock shows UTC — adjust accordingly.

---

## Tool Access & Integrations

### What the AI CAN access (16 MCP servers):
- **Email, Calendar, To-Do** (aws-outlook-mcp) — full CRUD. Guarded: sends restricted to prichwil, no external calendar invites.
- **Slack** (ai-community-slack-mcp) — full read. Write restricted to rsw-channel (C0993SRL6FQ) and self_dm per slack-guardrails.md.
- **Hedy** (hedy) — meeting transcripts, recaps, action items, topics. Call tools directly (mcp_hedy_ prefix).
- **DuckDB** (duckdb) — PS Analytics database. SQL read/write. All structured PS data.
- **ARCC** (arcc) — security/compliance knowledge base. Mandatory first call for credential/infra requests.
- **SharePoint/OneDrive** (amazon-sharepoint-mcp) — files, folders, lists, Loop pages. Read + write.
- **Loop** (loop-mcp) — Microsoft Loop page reader. Read-only.
- **KDS** (knowledge-discovery-mcp) — knowledge base Q&A. Read-only.
- **Weblab** (weblab-mcp) — experiment data: allocations, metadata, TAA alarms, activation history. Read-only.
- **Wiki** (xwiki-mcp) — w.amazon.com wiki pages. Read + write.
- **Builder** (builder-mcp) — Quip docs, internal search, Taskei tickets, phonetool, code search, pipelines, Apollo, oncall, ticketing. Massive toolset.
- **Taskei** (taskei-p-mcp) — dedicated Taskei integration. May overlap with builder-mcp.
- **Asana** (enterprise-asana-mcp) — full read/write. SearchTasksInWorkspace, GetTaskDetails, UpdateTask, CreateTask, CreateTaskStory, GetTaskStories, GetGoal, SetParentForTask, etc. Guarded: only modify Richard's tasks (GID 1212732742544167). Audit all writes to asana-audit-log.jsonl. Command center protocol: `~/shared/context/active/asana-command-center.md`.
- **Radar** (radar-mcp) — untested.
- **Search Marketing** (search-marketing-agent-workspace-alpha-mcp) — AgentCore Gateway for PS tools. Untested.
- **Local filesystem** — ~/shared/, /workspace/

### What the AI CANNOT access:
- Google Ads (no MCP server exists)
- Adobe Analytics (no MCP server exists)

### MCP Tool Reference:
- Full inventory with all tools, guardrails, and usage patterns: `~/shared/context/active/mcp-tool-reference.md`

---

## Key IDs

See hands.md → Task List Structure for Microsoft To-Do list IDs.
See hands.md → Key Outlook Folders for Outlook folder IDs.
See memory.md → Reference Index for Quip document links.

---

## Hook System

**Daily sequence:** AM-1 (Ingest) → AM-2 (Triage) → AM-3 (Brief), then EOD-1 (Meeting Sync) → EOD-2 (System Refresh + Karpathy experiments on organs + output quality). Guards (Email, Calendar) are always-on preToolUse hooks. On-demand: WBR Callouts, SharePoint Sync, PS Audit, Agent Bridge.

Full hook details: see device.md → Installed Apps and hands.md → Hook System.

---

## Directory Map

| Directory | Role | Owner | Contents |
|-----------|------|-------|----------|
| `~/shared/context/body/` | Body organs + device | Agent (maintained), Human (validated) | body.md, brain.md, eyes.md, hands.md, memory.md, spine.md, heart.md, device.md |
| `~/shared/context/active/` | Ground truth. Live state. | Agent + Human | current.md, org-chart.md, rw-tracker.md, long-term-goals.md, asana-command-center.md, mcp-tool-reference.md |
| `~/shared/context/intake/` | Inbox. Unprocessed material. | Human drops, Agent processes | Drafts, raw notes, new docs |
| `~/shared/context/wiki/` | Doc pipeline + context catalog | Wiki team agents | context-catalog.md, wiki-index.md, staging/, research/, reviews/ |
| `~/shared/context/tools/` | Utility scripts. | Agent builds | Python scripts for MCP, sync, briefs |
| `~/shared/data/duckdb/ps-analytics.duckdb` | PS Analytics database (DuckDB) | Dashboard ingester writes, all agents read+write | CLI: `python3 ~/shared/tools/data/query.py "SQL"`. Python: `from query import db, market_trend`. MCP: `execute_query`. Schema: `~/shared/tools/data/schema.sql`. Portability: `RECONSTRUCTION.md`. Exports: `~/shared/data/exports/`. |
| `~/shared/context/archive/` | Cold storage. | Agent | Archived artifacts, old versions |
| `~/shared/context/meetings/` | Meeting series notes. One file per recurring meeting. | Agent summarizes from Hedy | stakeholder/, team/, manager/, peer/, adhoc/ — see README.md for full map |
| `~/shared/artifacts/` | Published work product (7 categories) | Wiki team → Agent | testing/, strategy/, reporting/, tools/, communication/, program-details/, best-practices/ |
| `~/shared/research/` | Standalone research outputs. | Agent | ad-copy-results.md, competitor-intel.md, oci-performance.md, daily-brief-latest.md, data files |
| `~/shared/artifacts/` | Static references. | Human curates | index.md |
| `~/.kiro/steering/` | Agent behavior config. | Human edits, Agent suggests | soul.md, rw-trainer.md, writing styles, prioritization, environment rules |

---

## Ground Truth Files (stay separate — different update cadences)

| File | Location | What it is | Update cadence |
|------|----------|-----------|----------------|
| current.md | `~/shared/context/active/current.md` | Live state: projects, people, meetings, pending actions | Every loop run |
| org-chart.md | `~/shared/context/active/org-chart.md` | Org structure and reporting lines | On org changes |
| rw-tracker.md | `~/shared/context/active/rw-tracker.md` | Weekly scorecard, 30-day challenge | Every morning routine |
| long-term-goals.md | `~/shared/context/active/long-term-goals.md` | The Five Levels strategic arc | Monthly or on shift |

---

## System History

See changelog.md for full build history (3/12 onwards: trainer, loop, To-Do, Asana bridge, Hedy, wiki team, meetings, body metaphor migration, Slack ingestion).
