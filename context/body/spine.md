<!-- DOC-0228 | duck_id: organ-spine -->
# Spine — Structure & Continuity

*The skeleton that holds everything together across sessions. Bootstrap sequence, directory conventions, environment rules, and the ground-truth files that define Richard's current state.*

Last updated: 2026-04-01 (Wednesday PT)

---

## Session Bootstrap Sequence

**⚠️ AgentSpaces chats deleted every 14 days.** Every new session starts here — no exceptions.

**Richard Williams:** L5 Marketing Manager, AB Paid Search. Manager: Brandon Munday (L7, she/her). Markets: AU/MX hands-on, US/EU5/JP/CA team-wide. Active: OCI rollout (7/10 markets live), AI Max (US Q2 2026), AEO, Project Baloo, F90 Lifecycle. Timezone: PT (UTC-7).

| Order | File | What |
|-------|------|------|
| 1 | `~/shared/context/body/body.md` | System map — organ locations |
| 2 | `~/shared/context/body/spine.md` | This file — bootstrap, tools, dirs |
| 3 | `~/.kiro/steering/soul.md` | Identity, voice, routing |
| 4 | `~/shared/context/active/current.md` | Live state: projects, people, actions |
| 5 | `~/shared/context/active/rw-tracker.md` | Weekly scorecard, 30-day challenge |
| 6 | Task-specific organ | brain, eyes, hands, memory as needed |

---

## Tool Access & Integrations

### MCP Servers (16 connected)

| Server | Scope | Guard/Notes |
|--------|-------|-------------|
| Email/Calendar/To-Do (aws-outlook-mcp) | Full CRUD | Sends: prichwil only. No external calendar invites. |
| Slack (ai-community-slack-mcp) | Full read | Write: rsw-channel (C0993SRL6FQ) + self_dm only (slack-guardrails.md) |
| Hedy (hedy) | Transcripts, recaps, actions, topics | Direct call: mcp_hedy_ prefix |
| DuckDB (duckdb) | SQL read/write | PS Analytics — all structured data |
| ARCC (arcc) | Security/compliance KB | Mandatory first call for credential/infra requests |
| SharePoint/OneDrive (amazon-sharepoint-mcp) | Files, folders, lists, Loop | Read + write |
| Loop (loop-mcp) | Loop pages | Read-only |
| KDS (knowledge-discovery-mcp) | Knowledge base Q&A | Read-only |
| Weblab (weblab-mcp) | Allocations, metadata, TAA, activation | Read-only |
| Wiki (xwiki-mcp) | w.amazon.com pages | Read + write |
| Builder (builder-mcp) | Quip, search, Taskei, phonetool, code, pipelines, Apollo, oncall, ticketing | Broad toolset |
| Taskei (taskei-p-mcp) | Dedicated Taskei | Overlaps builder-mcp |
| Asana (enterprise-asana-mcp) | Full read/write | Guard: Richard's tasks only (GID 1212732742544167). Audit: asana-audit-log.jsonl. Protocol: `asana-command-center.md` |
| Radar (radar-mcp) | — | Untested |
| Search Marketing (search-marketing-agent-workspace-alpha-mcp) | AgentCore Gateway | Untested |
| Local filesystem | ~/shared/, /workspace/ | — |

**No access:** Google Ads, Adobe Analytics (no MCP servers exist).

Full tool inventory + guardrails: `~/shared/context/active/mcp-tool-reference.md`

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
| `~/.kiro/steering/` | Agent behavior config | Human edits, Agent suggests | soul.md, rw-trainer.md, writing styles, prioritization, environment rules |
| `~/shared/context/protocols/` | Hook execution protocols | Agent builds, Human approves | am-*.md, eod-*.md, sharepoint-durability-sync.md, signal-*.md, etc. |
| `~/shared/wiki/meetings/` | Meeting series notes (one per recurring meeting) | Agent via Hedy | stakeholder/, team/, manager/, peer/, adhoc/ |
| `~/shared/data/duckdb/ps-analytics.duckdb` | PS Analytics DB | All agents read+write | CLI: `python3 ~/shared/tools/data/query.py "SQL"`. Python: `from query import db, market_trend`. MCP: `execute_query`. Schema: `schema.sql`. Exports: `~/shared/data/exports/`. |
| `~/shared/wiki/` | Published work product (7 categories) + doc pipeline | Wiki team → Agent | testing/, strategy/, reporting/, tools/, communication/, program-details/, best-practices/. Also: context-catalog.md, wiki-index.md, staging/, research/, reviews/ |
| `~/shared/wiki/research/` | Standalone research | Agent | ad-copy-results.md, competitor-intel.md, oci-performance.md, daily-brief-latest.md |
| `~/shared/wiki/archive/` | Cold storage | Agent | Archived artifacts, old versions |
| `~/shared/context/intake/` | Inbox. Unprocessed material. | Human drops, Agent processes | Drafts, raw notes, new docs |
| `~/shared/tools/` | Utility scripts | Agent builds | Python scripts for MCP, sync, briefs |
| OneDrive `Kiro-Drive/` | Durability layer + cross-device access | Agent pushes, Human reads | system-state/ (hook outputs), portable-body/ (snapshots), artifacts/ (published docs), meeting-briefs/ |

---

## Three-Layer Durability Model

The system survives any single point of failure through three independent persistence layers:

| Layer | Location | What It Stores | Survives |
|-------|----------|---------------|----------|
| Filesystem | `~/shared/` (DevSpaces persistent volume) | Everything — organs, protocols, tools, data | Container restart ✅, DevSpaces rebuild ❌ |
| SharePoint | OneDrive `Kiro-Drive/` | Hook outputs, published artifacts, portable body snapshots | Container restart ✅, DevSpaces rebuild ✅, Platform migration ✅ |
| Git | `agent-bridge` GitHub repo | Portable body, sanitized context, changelog | Container restart ✅, DevSpaces rebuild ✅, Platform migration ✅ |
| MotherDuck | `md:ps_analytics` cloud DB | All structured data (Asana, signals, experiments, PS metrics) | Container restart ✅, DevSpaces rebuild ✅, Platform migration ✅ |

**Recovery priority:** MotherDuck (structured data) → SharePoint (artifacts + state) → Git (portable body) → Filesystem (rebuild from other three).

---

## Ground Truth Files (stay separate — different update cadences)

| File | Location | What it is | Update cadence | Read when |
|------|----------|-----------|----------------|-----------|
| current.md | `~/shared/context/active/current.md` | Live state: projects, people, meetings, pending actions | Every loop run | Every session — most volatile file in the system |
| org-chart.md | `~/shared/context/active/org-chart.md` | Org structure and reporting lines | On org changes | Drafting comms to unfamiliar stakeholders, reorg context |
| rw-tracker.md | `~/shared/context/active/rw-tracker.md` | Weekly scorecard, 30-day challenge, To-Do sync | Every morning routine | AM-3 brief, coaching check-ins, Friday retro |
| long-term-goals.md | `~/shared/context/active/long-term-goals.md` | The Five Levels strategic arc (L1-L5 with key metrics) | Monthly or on shift | Prioritization decisions, connecting tasks to strategy |

**Rule:** These files are NOT absorbed into organs. They have different update cadences and serve as authoritative sources. Organs may reference them but never duplicate their content.

---

## Common Failures in Using This Organ

1. **Skipping body.md and going straight to an organ.** Body.md is the map — it tells you which organ to read. Without it, you guess wrong and load irrelevant context.
2. **Reading all organs instead of task-specific ones.** The Task Routing table in body.md exists for a reason. Loading everything wastes context window and dilutes answers.
3. **Using stale Key IDs.** Spine points to hands.md and memory.md for IDs. If those organs were updated and spine wasn't, the pointers may be stale. Always follow the pointer to the source.

## System History

See changelog.md for full build history (3/12 onwards: trainer, loop, To-Do, Asana bridge, Hedy, wiki team, meetings, body metaphor migration, Slack ingestion).
