# Device — Outsourced Intelligence

*The body's phone/laptop/agent. Work that runs FOR Richard without requiring his judgment. If it needs Richard's brain, it's an organ. If it can execute autonomously, it belongs here.*

*Operating principle: Routine as liberation. Every delegation, template, and automation here exists to eliminate a decision Richard was making repeatedly. The test for a new device function: "Does this remove a recurring decision?" If yes, build it. If it just moves the decision, skip it.*

Last updated: 2026-03-26 (CE-5 applied — device compressed, run 12)

---

## The Test

Before adding anything here, ask: "Does this require Richard's judgment to produce a correct output?"
- **Yes** → It's an organ (brain, hands, etc.)
- **No** → It's a device function. Automate it, delegate it, or template it.

---

## 🤖 Installed Apps (running today)

These are live. They execute without Richard thinking.

### Morning Routine (Hook: `rw-morning-routine`)
- **What it does:** One-click daily chain: Asana Sync → Draft Unread Replies → To-Do Refresh + Daily Brief → Calendar Blocks
- **Trigger:** userTriggered (daily, one click)
- **Judgment required:** Step 2 (draft replies) presents triage table for Richard's confirmation. Step 4 (calendar blocks) asks which to create. Everything else is autonomous.
- **Includes:** Asana sync (was separate hook), task calendar blocks (was separate hook) — now consolidated into one flow.

### Autoresearch Loop (Hook: `run-the-loop`)
- **What it does:** Maintenance (refresh ground truth from email/calendar) → Cascade (update organ files) → Optionally 1 experiment
- **Trigger:** userTriggered ("run the loop")
- **Judgment required:** Phase 4 (suggestions) requires Richard's approval. Everything else is autonomous.
- **Protocol:** `~/shared/context/body/heart.md`

### Safety Guards (preToolUse hooks)
- **Block Email Send:** Prevents email_reply/send/forward unless only recipient is prichwil. Others require explicit approval.
- **Block Calendar Invite:** Prevents calendar events with external attendees. Personal blocks allowed.

### Karpathy Agent (Agent: `karpathy.md`)
- **What it does:** Governs loop evolution, compression experimentation, and system metabolism. Sole authority on changes to heart.md, gut.md compression rules, and experiment queue. No other agent modifies these files without going through Karpathy.
- **Trigger:** Invoked during loop runs (Phase 2-3), on demand ("run karpathy"), and weekly Fridays (metabolism report).
- **Judgment required:** None for compression and budget enforcement. Richard's approval required for structural loop changes (phase order, accuracy thresholds, body metaphor).
- **Agent file:** `~/shared/.kiro/agents/karpathy.md`

### Eyes Chart Agent (Agent: `eyes-chart.md`)
- **What it does:** Visualization specialist. Reads body organs (gut budgets, changelog experiments, tracker scorecard, NS patterns, aMCC streak) and market performance data (dashboard ingester JSON), generates a standalone HTML dashboard with interactive Chart.js charts.
- **Trigger:** Via `update-dashboard` hook ONLY. This hook is the single entry point for all dashboard regeneration. No other process, agent, or loop step should invoke generate.py directly.
- **Judgment required:** None. Read-only on all organs. Outputs HTML to `~/shared/tools/progress-charts/dashboard.html`.
- **Tool:** `python3 ~/shared/tools/progress-charts/generate.py`
- **Agent file:** `~/shared/.kiro/agents/eyes-chart.md`
- **Hook:** `update-dashboard` (userTriggered)

### Wiki Team (Agents: `wiki-team/`)
- **What it does:** 6-agent pipeline for doc creation: editor (orchestrator) → researcher → writer → critic → librarian + concierge (search/lookup). Publishes to `~/shared/artifacts/`. Context catalog (`~/shared/context/wiki/context-catalog.md`) enables fast source lookup for any agent.
- **Trigger:** On demand ("write a wiki article", "search the wiki", "audit the wiki"). Editor orchestrates the pipeline.
- **Judgment required:** None for pipeline execution. Richard approves final publish.
- **Agent files:** `~/.kiro/agents/wiki-team/` (6 .md agents)
- **Quality bar:** 8/10 minimum. Critic is a required gate, not optional.

### Agent Bridge (Tool: `~/shared/tools/bridge/bridge.py`)
- **What it does:** Google Sheets/Docs communication layer between Kiro (AgentSpace) and Richard's personal agent swarm. Provides async message bus, context snapshots, agent registry, and file management via Google API.
- **Trigger:** Imported by hooks/scripts. `from bridge import Bridge; b = Bridge()`
- **Surfaces:** Spreadsheet "agent bridge" (4 sheets: bus, context, registry, log) + Doc "agent bridge" (protocol + scratchpad)
- **Spreadsheet ID:** `1IlM43kzxw8Vlu6aUWXUV1dr7ZIF7O7H2bD5x3kaKIHg`
- **Doc ID:** `1koJV8a4Ig9BBDbrtQl-w8L4-2bUrz8lGwxUxEfIgQj8`
- **Drive Folder ID:** `1aeRuldkc-OL1gyR7FQ-WrvbpERPsYChZ`
- **Service Account:** `kiro-sheets-bridge@kiro-491503.iam.gserviceaccount.com`
- **Credentials:** `~/shared/credentials/kiro-491503-6b65ab0501c6.json`
- **Judgment required:** None for reads. Writes to bus/context are autonomous. New file creation in Drive folder is autonomous.
- **Portability:** Bridge files are plain text (Google Sheets/Docs). Any agent with the service account can read/write. Protocol is documented in the Google Doc itself.

### Hedy Meeting Sync (Hook: `hedy-meeting-sync`)
- **What it does:** Uses the Hedy MCP power to pull latest sessions, analyze Richard's communication patterns (speaking share, hedging, filler words, turn length), flag low-visibility meetings, audit/update Hedy session contexts and topic contexts for staleness, and cascade findings into organs.
- **Trigger:** userTriggered (after meetings, or automatically during loop Phase 1)
- **Judgment required:** None. Fully autonomous. Updates organs directly.
- **Integration:** Hedy MCP power (18 tools — GetSessions, GetSessionDetails, GetSessionHighlights, GetSessionToDos, GetAllTopics, GetTopicDetails, ListSessionContexts, UpdateSessionContext, UpdateTopic, etc.)
- **Feeds into:** Memory (relationship dynamics), Nervous System (communication patterns, Loop 7), Eyes (meeting prep — what was discussed last time)

### SharePoint Sync (Hook: `sharepoint-sync`)
- **What it does:** Converts eligible wiki articles from `~/shared/artifacts/` to .docx files and writes them to a OneDrive-synced SharePoint folder. Filters by audience (amazon-internal only) and status (configurable, default REVIEW+FINAL). Incremental sync via SHA-256 content hashing — only changed articles are re-exported. Dry-run first, then confirms with Richard before live sync.
- **Trigger:** userTriggered (one-click "Sync to SharePoint" button)
- **Judgment required:** Yes — hook runs dry-run first, shows what will be created/updated/removed, and asks Richard to confirm before executing.
- **Tool:** `python3 ~/shared/tools/sharepoint-sync/cli.py --mode directory`
- **Config:** `~/shared/tools/sharepoint-sync/config.yaml`
- **Output:** .docx files in OneDrive folder → auto-syncs to SharePoint document library
- **Local (Windows):** `c:/Users/prichwil/OneDrive - amazon.com/Artifacts/wiki-sync`
- **Portability:** Pure Python, no API keys. Config is YAML, manifest is JSON. Works on any machine with Python + OneDrive sync.

---

## 📋 Templates (pre-computed responses)

Work that's been reduced to fill-in-the-blank. Richard copy-pastes and sends.

Queued templates (not built): Email Templates, WBR Callout Template, Meeting Prep Template. Will be built via Tool Factory when prioritized.

---

## 👥 Delegation Protocols (apps installed on other people)

Work that Richard has offloaded or should offload to specific humans. Each protocol defines: what's delegated, to whom, what Richard still owns, and the handoff mechanism.

### MX Invoice Routing → Carlos Palmos
- **Status:** VOID — Carlos transitioned to CPS side of MX acquisition (~3/17). No longer owns PS invoicing.
- **What to delegate:** Monthly Google Ads invoice processing for MX. PO matching, submission, follow-up.
- **What Richard keeps:** Everything, until a new delegate is identified. Lorena is the new MX PS stakeholder but invoice routing hasn't been discussed with her yet.
- **Next step:** Decide whether to delegate MX invoicing to Lorena or keep it. If Lorena, send process doc + PO numbers.

### AU Day-to-Day (reversed)
- **Status:** REVERSED. Harjeet stepped away. Richard owns all AU PS.

### MX Keyword Sourcing → Lorena Alvarez Larrea
- **Status:** IN PROGRESS. Lorena requested MX PS strategy overview + keyword data (3/19). She's engaging.
- **What to delegate:** Ongoing keyword opportunity identification, negative keyword management for MX.
- **What Richard keeps:** Strategy, bid decisions, testing framework.
- **Handoff:** Send keyword export + strategy overview (draft sent 3/20). Follow up with a "here's how to identify new keywords" guide.

### WBR Coverage → Dwayne Palmer (restored)
- **Status:** RESTORED. Dwayne back from OOO. Normal coverage resumes.
- **What Richard keeps:** PS-specific callouts when asked. Backup coverage when Dwayne is out.
- **Gap:** No backup process was created during the 2/23-3/6 coverage. Build a template so next time it's a 10-minute handoff, not a multi-day absorption.

### OP1 Contributor Sections → Andrew, Stacey, Yun, Adi
- **Status:** IN PROGRESS. Andrew active in Loop doc (3/18). Others not yet confirmed.
- **What Richard keeps:** Overall narrative, integration across sections, Kate presentation.
- **What's delegated:** Each contributor writes their workstream section (problem→test→result→scale).
- **Gap:** No deadline set for contributor drafts. Need to send a "sections due by [date]" message.

---

## 🛠️ Tool Factory

| # | Tool | Status |
|---|------|--------|
| 0 | **Paid Search Audit — Sheets Bridge setup** — Schedule Google Ads reports (AU, MX) to richscottwill@gmail.com → set up Gmail Apps Script auto-ingest (`paid_search_audit/gmail_auto_ingest.js`) at script.google.com → parses CSV attachments → writes to [Bridge_AB-Ads-Data](https://docs.google.com/spreadsheets/d/1mNnQSaQUCSHJXcrssFmvYDLqoKimWFm56UCVpeA3wjQ) AU/MX tabs → update `config.json` with real account CIDs/MCC IDs. Then audit runs end-to-end. | **Richard action needed** |
| 1 | **Dashboard ingester** — manual weekly data extraction → automated | ✅ BUILT |
| 1b | **Context catalog** — universal source index for all agents | ✅ BUILT |
| 2 | **Campaign link generator** — manual promo URL construction for AU/MX sitelinks | Backlog |
| 3 | **Staleness detector** — auto-check file freshness, prevent context drift | Ready to build |

Additional proposals in backlog: WBR auto-briefing agent, Meeting prep auto-generator, Invoice routing workflow, Testing tracker, Keyword analysis pipeline.

### Build Priority Rule
From brain.md (Level 3): "Give your team leverage through automation." The first tool adopted by a teammate is the milestone. Prioritize tools that others can use, not just Richard.

---

## 📊 Device Health

Tracks installed system infrastructure only — hooks, agents, tools, and guards that run autonomously. Delegation statuses live in Delegation Protocols above. Proposed tools live in Tool Factory above.

| Function | Status | Last Run | Notes |
|----------|--------|----------|-------|
| Morning Routine | ✅ Active | 3/24 | One-click: sync + drafts + brief + blocks |
| Autoresearch Loop | ✅ Active | 3/27 | 13 runs completed |
| Agent Bridge | ✅ Active | 3/27 | Google Sheets/Docs bridge to personal swarm. `~/shared/tools/bridge/bridge.py` |
| Dashboard Ingester | ✅ Active | 3/23 | `python3 shared/tools/dashboard-ingester/ingest.py <xlsx>` — all 10 markets |
| Progress Charts | ✅ Active | 3/25 | Via `update-dashboard` hook only — single entry point for HTML dashboard |
| Hedy Meeting Sync | ✅ Active | 3/23 | Via MCP power — no script needed |
| Wiki Team | ✅ Active | 3/25 | 6-agent pipeline. 15 artifacts published. 8/10 quality bar. |
| Context Catalog | ✅ Active | 3/25 | Universal source index. `~/shared/context/wiki/context-catalog.md` |
| Karpathy Agent | ✅ Active | 3/24 | Loop governor + compression scientist. Gates all heart.md/gut.md changes. |
| Eyes Chart Agent | ✅ Active | 3/25 | Visualization specialist. Read-only. Invokes progress-charts tool. |
| Safety: Email Block | ✅ Active | Always on | preToolUse guard |
| Safety: Calendar Block | ✅ Active | Always on | preToolUse guard |
| SharePoint Sync | ✅ Active | 3/27 | Wiki → .docx → OneDrive → SharePoint. Hook: `sharepoint-sync` |

---

## When to Read This File

- When Richard says "I'll just do it myself" — check if a device function exists or should be built
- When evaluating whether work is high-leverage — if it's on the device, it shouldn't be on Richard
- When the trainer flags a recurring time trap — check if a delegation protocol or tool proposal exists
- When planning system-building sessions — the Tool Factory is the backlog
