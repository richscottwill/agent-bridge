# Spine — Structure & Continuity

*The skeleton that holds everything together across sessions. Bootstrap sequence, directory conventions, environment rules, and the ground-truth files that define Richard's current state.*

Last updated: 2026-03-31 (Tuesday PT)

---

## Session Bootstrap Sequence

**CRITICAL: AgentSpaces chats are deleted every 14 days.** At the start of every new session, read these files in order:

1. `~/shared/context/body/body.md` — The map of the whole system. Tells you what each organ does and where to find it.
2. `~/shared/context/body/spine.md` — This file. Bootstrap sequence, tool access, key IDs.
3. `~/.kiro/steering/soul.md` — Identity, values, voice, preferences.
4. `~/.kiro/steering/rw-trainer.md` — Coaching framework, mediocrity patterns, leverage assessment.
5. `~/shared/context/active/current.md` — Ground truth: active projects, people, meetings, pending actions.
6. `~/shared/context/active/rw-tracker.md` — Weekly scorecard, To-Do sync, patterns, 30-day challenge.

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
- **Hedy** (MCP server) — meeting transcripts, recaps, action items, speaker analysis, topics, session contexts. 18 tools via MCP. Configured as a direct MCP server in `.kiro/settings/mcp.json` (not a power). Tools are prefixed `mcp_hedy_` and available directly: `mcp_hedy_GetSessions`, `mcp_hedy_GetSessionDetails`, `mcp_hedy_GetSessionHighlights`, `mcp_hedy_GetSessionToDos`, `mcp_hedy_GetHighlights`, `mcp_hedy_GetToDos`, `mcp_hedy_GetAllTopics`, etc. No activation step needed — just call the tools. To ingest a new recording: (1) `GetSessions` with limit=1 to find the newest, (2) `GetSessionDetails` with the sessionId to get full transcript/recap/todos, (3) save to `~/shared/context/intake/` for processing.
- **Local filesystem** — ~/shared/, /workspace/

### What the AI CANNOT access:
- Slack, Asana (directly), Google Ads, Adobe Analytics, SharePoint/OneDrive

### Asana Bridge (workaround):
- **Create tasks**: Email x@mail.asana.com (include Richard's email)
- **Read task updates**: Check Outlook "Auto-Comms" folder
- **Read meeting context**: Check Outlook "Auto-meeting" folder (Hedy recaps + Amazon Meetings Summary)
- **Full protocol**: `~/shared/context/active/asana-sync-protocol.md`

### MCP Tool Reference:
- Full API docs: `~/shared/context/active/mcp-tool-reference.md`
- Triple-nested JSON responses, shell escaping gotchas, Python helper function

---

## Key IDs

### Microsoft To-Do Lists
| List | ID |
|------|-----|
| 🧹 Sweep | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESHAAA=` |
| 🎯 Core | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESIAAA=` |
| ⚙️ Engine Room | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESJAAA=` |
| 📋 Admin | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADUyESKAAA=` |
| 📦 Backlog | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy-SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja-dZLhI0AADWyS4nAAA=` |

### Outlook Folders
| Folder | ID |
|--------|-----|
| Auto-Comms (Asana) | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQpAAA=` |
| Auto-meeting       | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQCIgJPBFelsQrcja/dZLhI0AAC3dkeCAAA=` |
| Goal: Paid Acquisition | `AQMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1ADdkM2EwYWMALgAAAyuwPeLL9INGsaRwucS5ngYBAEas7LcSB6lEv39h0ciIq84AAAITTwAAAA==` |
| AP (Invoices) | `AAMkAGQ5NmQwNGZkLWQ0NTAtNGY4Yy1hNjhlLTY0OTU1N2QzYTBhYwAuAAAAAAArsD3iy/SDRrGkcLnEuZ4GAQDAgFdLn8NBQbObwPn0M6aUAADuhyQcAAA=` |

### Key Quip Documents
- MX Sync: https://quip-amazon.com/K9OYA9mXm7DU
- Pre-WBR Callouts: https://quip-amazon.com/MMgBAzDrlVou
- OCI Instructions: https://quip-amazon.com/Zee9AAlSBEB
- Ad Copy Updates: https://quip-amazon.com/KCY9AAYqWd2
- Testing Plan 2026: https://quip-amazon.com/EED9AAFOy4E

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
| `~/shared/tools/data/ps-analytics.duckdb` | PS Analytics database (DuckDB). All structured paid search data. | Dashboard ingester writes, all agents read+write | Query: `python3 ~/shared/tools/data/query.py "SQL"` or `from query import db`. MCP: `execute_query` tool (duckdb server). Read: `db()`, `market_trend()`, `market_week()`, `projection()`, `callout_scores()`. Write: `db_write()`, `db_upsert()`. Schema: `schema_export()` auto-runs after ingestion → `~/shared/tools/data/schema.sql`. Portability: `~/shared/tools/data/RECONSTRUCTION.md`. Data event: `~/shared/tools/data/last_ingest.json`. Parquet exports: `~/shared/tools/data/exports/`. |
| `~/shared/context/archive/` | Cold storage. | Agent | Archived artifacts, old versions |
| `~/shared/context/meetings/` | Meeting series notes. One file per recurring meeting. | Agent summarizes from Hedy | stakeholder/, team/, manager/, peer/, adhoc/ — see README.md for full map |
| `~/shared/artifacts/` | Published work product (7 categories) | Wiki team → Agent | testing/, strategy/, reporting/, tools/, communication/, program-details/, best-practices/ |
| `~/shared/research/` | Standalone research outputs. | Agent | ad-copy-results.md, competitor-intel.md, oci-performance.md, daily-brief-latest.md, data files |
| `~/shared/reference/` | Static references. | Human curates | index.md |
| `~/.kiro/steering/` | Agent behavior config. | Human edits, Agent suggests | soul.md, rw-trainer.md, writing styles, prioritization, environment rules |

---

## Ground Truth Files (stay separate — different update cadences)

| File | Location | What it is | Update cadence |
|------|----------|-----------|----------------|
| current.md | `~/shared/context/active/current.md` | Live state: projects, people, meetings, pending actions | Every loop run |
| org-chart.md | `~/shared/context/active/org-chart.md` | Org structure and reporting lines | On org changes |
| rw-tracker.md | `~/shared/context/active/rw-tracker.md` | Weekly scorecard, To-Do sync, patterns, 30-day challenge | Every morning routine |
| long-term-goals.md | `~/shared/context/active/long-term-goals.md` | The Five Levels strategic arc | Monthly or on shift |

---

## Key People (Quick Reference)
| Name | Alias | Context |
|------|-------|---------|
| Brandon Munday | brandoxy | Richard's manager (L7), Paid Acq team lead |
| Kate Rundell | kataxt | L8 Director, key stakeholder for Testing Approach doc |
| Alexis Eck | alexieck | AU market POC, MCS page mapping |
| Lena Zak | lenazak | AU stakeholder, pushes for MCS migration & performance |
| Carlos Palmos | cpalmos | MX Paid Search, invoice coordination |
| Lorena Alvarez Larrea | lorealea | MX Paid Search |
| Yun-Kang Chu | yunchu | 1:1 sync, MX PS, Adobe analytics |
| Aditya Satish Thakur | aditthk | Weekly sync, AI brainstorm partner |
| Dwayne Palmer | dtpalmer | Customer Engagement/MCS, WBR coverage |

---

## What Was Built (system history)
- 3/12: Created RW Trainer steering file, autoresearch loop (heart.md), 3 experiments
- 3/13: Excellence Tracker, Microsoft To-Do (4 workflow lists), Asana bridge, 5 more experiments. All 8 KEPT.
- 3/17: Maintenance-only loop run. Cascaded to 5 artifacts.
- 3/19: Maintenance-only loop run. Cascaded to 5 artifacts.
- 3/20: Maintenance-only loop run. Cascaded to 6 artifacts. Body metaphor migration — consolidated exp1-8 into organ files. Moved all body files to `~/shared/context/body/`.
- 3/22: Hedy API integration. Built `hedy-sync.py` (meeting transcript analysis, speaker identification, communication pattern scoring). Created `hedy-meeting-sync` hook. Updated memory.md with meeting dynamics for 7 stakeholders. Added 2 new patterns to nervous-system.md (group meeting silence, hedging language). Wired Hedy into heart.md Phase 1 maintenance and Phase 2 cascade.
- 3/23: Installed Hedy MCP power (powers/hedy/). Replaced hedy-sync.py + curl-based workflow with native MCP tools (18 tools: sessions, highlights, to-dos, topics, contexts). Updated hedy-meeting-sync hook, heart.md loop, spine.md tool access, device.md, body.md, nervous-system.md Loop 7. Script deprecated — MCP power is now the canonical Hedy integration.
- 3/23: Autoresearch loop run 8. Maintenance + cascade. Processed 3 Hedy intake files (archived). Updated current.md, hands, eyes, memory, amcc, brain, nervous-system, device. Weblab ticket confirmed submitted. MX invoice delegation marked FAILED. York Chen back from leave.
- 3/25: Wiki team built (6 agents in `~/.kiro/agents/wiki-team/`). Context catalog created (`~/shared/context/wiki/context-catalog.md`). Wiki pipeline: editor → researcher → writer → critic → librarian + concierge. 15 artifacts published to `~/shared/artifacts/`. Quality bar raised to 8/10. Agent folders reorganized (body-system/, wbr-callouts/, wiki-team/).
- 3/26: Meeting notes system built (`~/shared/context/meetings/`). 15 series files across 5 folders (stakeholder, team, manager, peer, adhoc). Each file: metadata, context, latest session summary, running themes, open items. Populated from Hedy MCP topics + memory.md. Meeting prep briefs removed from memory.md (now points to meetings/). body.md and spine.md updated with meetings folder. Agent workflow: pull Hedy transcript → agent-summarize → update series file.
