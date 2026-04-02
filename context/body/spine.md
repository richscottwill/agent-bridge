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

### What the AI CAN access:
- **Email** (Outlook) — read, search, send, reply, forward, folders
- **Calendar** (Outlook) — view, create, update meetings
- **Microsoft To-Do** — full CRUD on tasks and lists
- **Slack** (ai-community-slack-mcp) — full read access. Channel ingestion driven by `list_channels` (Richard's sidebar sections determine depth). Proactive search beyond channel list. Reaction checking. DM scanning. Write restricted to rsw-channel and self_dm per slack-guardrails.md. Config: `~/shared/context/active/slack-channel-registry.json`.
- **Hedy** (MCP server) — meeting transcripts, recaps, action items, speaker analysis, topics, session contexts. 18 tools via MCP. Configured as a direct MCP server in `.kiro/settings/mcp.json` (not a power). Tools are prefixed `mcp_hedy_` and available directly: `mcp_hedy_GetSessions`, `mcp_hedy_GetSessionDetails`, `mcp_hedy_GetSessionHighlights`, `mcp_hedy_GetSessionToDos`, `mcp_hedy_GetHighlights`, `mcp_hedy_GetToDos`, `mcp_hedy_GetAllTopics`, etc. No activation step needed — just call the tools. To ingest a new recording: (1) `GetSessions` with limit=1 to find the newest, (2) `GetSessionDetails` with the sessionId to get full transcript/recap/todos, (3) save to `~/shared/context/intake/` for processing.
- **Local filesystem** — ~/shared/, /workspace/

### What the AI CANNOT access:
- Asana (directly), Google Ads, Adobe Analytics, SharePoint/OneDrive

### Asana Bridge:
See hands.md → Asana Bridge for full protocol. Short version: email x@mail.asana.com to create tasks, read Auto-Comms folder for updates.

### MCP Tool Reference:
- Full API docs: `~/shared/context/active/mcp-tool-reference.md`
- Triple-nested JSON responses, shell escaping gotchas, Python helper function

---

## Key IDs

See hands.md → Task List Structure for Microsoft To-Do list IDs.
See hands.md → Key Outlook Folders for Outlook folder IDs.
See memory.md → Reference Index for Quip document links.

---

## Hook System

| # | Hook | Trigger | When to Run |
|---|------|---------|-------------|
| 1 | 1 · AM: Morning Routine | userTriggered | Morning — reads fresh organs → Asana sync → drafts → brief → calendar blocks |
| 2 | 2 · EOD: Meeting Sync | userTriggered | End of day — ingest today's meetings into series files |
| 3 | 3 · EOD: System Refresh | userTriggered | End of day, after Meeting Sync — cascade into organs, then git push to personal repo |
| 4 | Guard: Email | preToolUse | Always on |
| 5 | Guard: Calendar | preToolUse | Always on |
| 6 | On-Demand: PS Audit | userTriggered | When reviewing campaign data |
| 7 | On-Demand: Dashboard | userTriggered | When you want visuals |

**Daily sequence: AM (1), then EOD (2 → 3 → git push).** Meeting Sync feeds System Refresh feeds git sync feeds tomorrow's Morning Routine. Guards are automatic. On-Demand hooks run when needed.

---

## Directory Map

| Directory | Role | Owner | Contents |
|-----------|------|-------|----------|
| `~/shared/context/body/` | Body organs + device | Agent (maintained), Human (validated) | body.md, brain.md, eyes.md, hands.md, memory.md, spine.md, heart.md, device.md |
| `~/shared/context/active/` | Ground truth. Live state. | Agent + Human | current.md, org-chart.md, rw-tracker.md, long-term-goals.md, session-bootstrap.md, asana-sync-protocol.md, mcp-tool-reference.md |
| `~/shared/context/intake/` | Inbox. Unprocessed material. | Human drops, Agent processes | Drafts, raw notes, new docs |
| `~/shared/context/wiki/` | Doc pipeline + context catalog | Wiki team agents | context-catalog.md, wiki-index.md, staging/, research/, reviews/ |
| `~/shared/context/tools/` | Utility scripts. | Agent builds | Python scripts for MCP, sync, briefs |
| `~/shared/data/duckdb/ps-analytics.duckdb` | PS Analytics database (DuckDB). All structured paid search data. | Dashboard ingester writes, all agents read+write | Query: `python3 ~/shared/tools/data/query.py "SQL"` or `from query import db`. MCP: `execute_query` tool (duckdb server). Read: `db()`, `market_trend()`, `market_week()`, `projection()`, `callout_scores()`. Write: `db_write()`, `db_upsert()`. Schema: `schema_export()` auto-runs after ingestion → `~/shared/tools/data/schema.sql`. Portability: `~/shared/tools/data/RECONSTRUCTION.md`. Data event: `~/shared/tools/data/last_ingest.json`. Parquet exports: `~/shared/data/exports/`. |
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

## Key People

See memory.md → Relationship Graph for the full people directory with tone notes and draft style guidance.

---

## System History

See changelog.md for full build history (3/12 onwards: trainer, loop, To-Do, Asana bridge, Hedy, wiki team, meetings, body metaphor migration, Slack ingestion).
