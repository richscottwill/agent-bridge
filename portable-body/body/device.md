# Device — Outsourced Intelligence

*The body's phone/laptop/agent. Work that runs FOR Richard without requiring his judgment. If it needs Richard's brain, it's an organ. If it can execute autonomously, it belongs here.*

*Operating principle: Routine as liberation. Every delegation, template, and automation here exists to eliminate a decision Richard was making repeatedly. The test for a new device function: "Does this remove a recurring decision?" If yes, build it. If it just moves the decision, skip it.*

Last updated: 2026-03-31 (Karpathy run 15 — CE-5 COMPRESS+REMOVE, 2409w→1386w)

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
- **Trigger:** userTriggered (daily). Step 2 (draft replies) and Step 4 (calendar blocks) need Richard's confirmation. Everything else autonomous.

### Autoresearch Loop (Hook: `run-the-loop`)
- **What it does:** Maintenance (refresh ground truth from email/calendar) → Cascade (update organ files) → Optionally 1 experiment
- **Trigger:** userTriggered ("run the loop")
- **Judgment required:** Phase 4 (suggestions) requires Richard's approval. Everything else is autonomous.
- **Protocol:** `~/shared/context/body/heart.md`

### Safety Guards (preToolUse hooks)
- **Block Email Send:** Prevents email_reply/send/forward unless only recipient is prichwil. Others require explicit approval.
- **Block Calendar Invite:** Prevents calendar events with external attendees. Personal blocks allowed.

### Karpathy Agent (Agent: `karpathy.md`)
- **What it does:** Loop governor + compression scientist. Sole authority on heart.md, gut.md, experiment queue.
- **Trigger:** During loop runs, on demand ("run karpathy"), weekly Fridays (metabolism report).
- **Agent file:** `~/.kiro/agents/body-system/karpathy.md`

### Eyes Chart Agent (Agent: `eyes-chart.md`)
- **What it does:** Reads body organs + market data → generates standalone HTML dashboard (Chart.js).
- **Trigger:** `update-dashboard` hook ONLY (single entry point). Read-only on all organs.
- **Tool:** `python3 ~/shared/tools/progress-charts/generate.py` · Agent: `~/shared/.kiro/agents/eyes-chart.md`

### Wiki Team (Agents: `wiki-team/`)
- **What it does:** 6-agent doc pipeline: editor → researcher → writer → critic → librarian + concierge. Publishes to `~/shared/artifacts/`. 15 artifacts. 8/10 quality bar (critic is required gate).
- **Trigger:** On demand. Editor orchestrates. Agent files: `~/.kiro/agents/wiki-team/`

### Agent Bridge (Tool: `~/shared/tools/bridge/bridge.py`)
- **What it does:** Google Sheets/Docs async message bus + context snapshots between Kiro and Richard's personal agent swarm.
- **Trigger:** `from bridge import Bridge; b = Bridge()`
- **Key IDs:** Spreadsheet `1IlM43kzxw8Vlu6aUWXUV1dr7ZIF7O7H2bD5x3kaKIHg` · Doc `1koJV8a4Ig9BBDbrtQl-w8L4-2bUrz8lGwxUxEfIgQj8` · Drive `1aeRuldkc-OL1gyR7FQ-WrvbpERPsYChZ`
- **Service Account:** `kiro-sheets-bridge@kiro-491503.iam.gserviceaccount.com` · Creds: `~/shared/credentials/kiro-491503-6b65ab0501c6.json`
- **Judgment required:** None. Autonomous reads/writes.

### Hedy Meeting Sync (Hook: `hedy-meeting-sync`)
- **What it does:** Pulls Hedy sessions, analyzes communication patterns (speaking share, hedging, filler words), flags low-visibility meetings, updates session/topic contexts, cascades to organs.
- **Trigger:** userTriggered (after meetings, or during loop Phase 1). Fully autonomous.
- **Feeds into:** Memory (relationships), Nervous System (communication patterns, Loop 7), Eyes (meeting prep)

### SharePoint Sync (Hook: `sharepoint-sync`)
- **What it does:** Wiki articles → .docx → OneDrive → SharePoint. Filters: amazon-internal, REVIEW+FINAL. Incremental via SHA-256 hashing.
- **Trigger:** userTriggered. Dry-run first, Richard confirms before live sync.
- **Tool:** `python3 ~/shared/tools/sharepoint-sync/cli.py --mode directory` · Config: `~/shared/tools/sharepoint-sync/config.yaml`
- **Local (Windows):** `c:/Users/prichwil/OneDrive - amazon.com/Artifacts/wiki-sync`

### PS Analytics Database (DuckDB)
- **What it does:** Persistent analytical DB for all structured PS data — daily/weekly/monthly metrics (10 markets, Brand/NB), IECCP, projections, callout scores, competitors, OCI status, change logs, anomalies. Auto-populated by dashboard ingester.
- **DB path:** `~/shared/data/duckdb/ps-analytics.duckdb` · Query: `~/shared/tools/data/query.py` (CLI or `from query import db, market_trend`)
- **Active tables:** daily_metrics, weekly_metrics, monthly_metrics, ieccp, projections, callout_scores, experiments, ingest_log, change_log, anomalies, competitors, oci_status. Schema-only: agent_actions, agent_observations, decisions, task_queue.
- **Agent access:** DuckDB MCP Server (`execute_query`, `list_tables`, `list_columns` via `.kiro/settings/mcp.json`). Python: `db_validate()`, `schema()`, `export_parquet()`, `db_write()`, `db_upsert()`.
- **Portability:** Single file, no server. Parquet exports at `~/shared/data/exports/`. Rebuild: `~/shared/tools/data/RECONSTRUCTION.md`.

---

## 📋 Templates

Queued (not built): Email Templates, WBR Callout Template, Meeting Prep Template. Will be built via Tool Factory when prioritized.

---

## 👥 Delegation Protocols (apps installed on other people)

Work that Richard has offloaded or should offload to specific humans. Each protocol defines: what's delegated, to whom, what Richard still owns, and the handoff mechanism.

### MX Invoice Routing → Carlos Palmos
- **Status:** VOID — Carlos transitioned to CPS (~3/17). Richard owns MX invoicing until new delegate identified. Next step: decide whether to delegate to Lorena (send process doc + PO numbers).

### AU Day-to-Day → Harjeet (reversed)
- **Status:** REVERSED. Harjeet stepped away. Richard owns all AU PS.

### MX Keyword Sourcing → Lorena Alvarez Larrea
- **Status:** IN PROGRESS. Lorena engaging (requested strategy overview + keyword data 3/19).
- **Delegated:** Keyword opportunity identification, negative keyword management for MX. Richard keeps strategy, bid decisions, testing framework.
- **Next:** Follow up with "how to identify new keywords" guide (draft sent 3/20).

### WBR Coverage → Dwayne Palmer
- **Status:** RESTORED. Normal coverage resumed. Richard keeps PS-specific callouts + backup when Dwayne is out.
- **Gap:** No backup handoff template built. Need one for next OOO.

### OP1 Contributor Sections → Andrew, Stacey, Yun, Adi
- **Status:** IN PROGRESS. Andrew active (3/18). Others not yet confirmed. Richard keeps overall narrative + Kate presentation.
- **Gap:** No deadline set for contributor drafts.

---

## 🛠️ Tool Factory

| # | Tool | Status |
|---|------|--------|
| 0 | **Paid Search Audit** — Gmail Apps Script auto-ingest → [Bridge_AB-Ads-Data](https://docs.google.com/spreadsheets/d/1mNnQSaQUCSHJXcrssFmvYDLqoKimWFm56UCVpeA3wjQ). Needs: schedule reports, set up script, update config.json with CIDs. | **Richard action** |
| 1 | **Dashboard ingester** | ✅ BUILT |
| 1a | **PS Analytics DB (DuckDB)** | ✅ BUILT |
| 1b | **Context catalog** | ✅ BUILT |
| 2 | **Campaign link generator** — AU/MX sitelink URL construction | Backlog |
| 3 | **Staleness detector** — auto-check file freshness | Ready to build |

Backlog proposals: WBR auto-briefing, meeting prep auto-generator, invoice routing, testing tracker, keyword analysis pipeline. Build priority (brain.md Level 3): tools teammates adopt first.

---

## 📊 Device Health

Tracks installed system infrastructure only — hooks, agents, tools, and guards that run autonomously. Delegation statuses live in Delegation Protocols above. Proposed tools live in Tool Factory above.

| Function | Status | Last Run | Notes |
|----------|--------|----------|-------|
| Morning Routine | ✅ | 3/30 | Sync + drafts + brief + blocks |
| Autoresearch Loop | ✅ | 3/31 | 14 runs. Protocol: heart.md |
| Agent Bridge | ✅ | 3/27 | Google Sheets/Docs ↔ swarm |
| Dashboard Ingester | ✅ | 3/30 | All 10 markets. ie%CCP fixed 3/30 |
| Progress Charts | ✅ | 3/25 | Via `update-dashboard` hook |
| Hedy Meeting Sync | ✅ | 3/23 | Via MCP power |
| Wiki Team | ✅ | 3/25 | 6 agents. 15 artifacts. 8/10 bar |
| Context Catalog | ✅ | 3/25 | `~/shared/context/wiki/context-catalog.md` |
| Karpathy Agent | ✅ | 3/24 | Loop governor. Gates heart.md/gut.md |
| Eyes Chart Agent | ✅ | 3/25 | Read-only visualization |
| Safety: Email Block | ✅ | Always | preToolUse — prichwil-only sends |
| Safety: Calendar Block | ✅ | Always | preToolUse — no external attendees |
| SharePoint Sync | ✅ | 3/27 | Wiki → .docx → OneDrive → SharePoint |
| PS Analytics DB | ✅ | 3/30 | DuckDB. Auto-populated by ingester |
| DuckDB MCP Server | ✅ | 3/30 | Native SQL for agents via MCP |
| WBR Callout Pipeline | ✅ | 3/30 | 10-market pipeline (v2). W13 produced. Hook: `wbr-callout-pipeline` |
| Prediction Engine | ✅ | 3/30 | Bayesian forecasting. CLI: `~/shared/tools/prediction/predict.py` |
| Attention Tracker | 🔧 | 3/30 | Built, not deployed. For Richard's local Windows machine |

---

## When to Read This File

- When Richard says "I'll just do it myself" — check if a device function exists or should be built
- When evaluating whether work is high-leverage — if it's on the device, it shouldn't be on Richard
- When the trainer flags a recurring time trap — check if a delegation protocol or tool proposal exists
- When planning system-building sessions — the Tool Factory is the backlog
