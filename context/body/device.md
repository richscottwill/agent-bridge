# Device — Outsourced Intelligence

*The body's phone/laptop/agent. Work that runs FOR Richard without requiring his judgment. If it needs Richard's brain, it's an organ. If it can execute autonomously, it belongs here.*

*Operating principle: Routine as liberation. Every delegation, template, and automation here exists to eliminate a decision Richard was making repeatedly. The test for a new device function: "Does this remove a recurring decision?" If yes, build it. If it just moves the decision, skip it.*

Last updated: 2026-04-01 (loop run 15 — Slack Context Ingestion live)

---

## The Test

Before adding anything here, ask: "Does this require Richard's judgment to produce a correct output?"
- **Yes** → It's an organ (brain, hands, etc.)
- **No** → It's a device function. Automate it, delegate it, or template it.

---

## 🤖 Installed Apps (running today)

These are live. They execute without Richard thinking.

### AM Hooks (3 sequential, each feeds the next)
- **AM-1: Ingest** (`am-1-ingest`) — Slack scan + Asana sync + email scan. Pure data collection → intake files. ~5 min.
- **AM-2: Triage + Draft** (`am-2-triage`) — Process AM-1 intake → update hands.md, draft email replies, update amcc.md. ~5 min.
- **AM-3: Brief + Blocks** (`am-3-brief`) — Daily brief (email + Slack), dashboard update, calendar blocks, proactive drafts. ~5 min.

### EOD Hooks (2 sequential)
- **EOD-1: Meeting Sync** (`eod-1-meeting-sync`) — Hedy + Outlook + email → meetings/ series files + organ updates. ~5 min.
- **EOD-2: System Refresh** (`eod-2-system-refresh`) — Maintenance cascade + experiments (Karpathy) + dashboard + enrichments + git sync. ~10 min. Protocol: `~/shared/context/body/heart.md`

### Safety Guards (preToolUse hooks)
- **Block Email Send:** Prevents email_reply/send/forward unless only recipient is prichwil. Others require explicit approval.
- **Block Calendar Invite:** Prevents calendar events with external attendees. Personal blocks allowed.

### Karpathy Agent (Agent: `karpathy.md`)
- **What it does:** Loop governor + compression scientist + output quality experimenter. Sole authority on heart.md, gut.md, experiment queue. Experiments on both information content (organs) and output quality (style guides, market context files, callout principles, hook prompts).
- **Trigger:** During loop runs, on demand ("run karpathy"), weekly Fridays (metabolism report).
- **Agent file:** `~/.kiro/agents/body-system/karpathy.md`

### Eyes Chart Agent (Agent: `eyes-chart.md`)
- **What it does:** Reads body organs + market data → generates standalone HTML dashboard (Chart.js).
- **Trigger:** On demand (`PS Audit` hook or manual). Read-only on all organs.
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

### Hedy Meeting Sync (via EOD-1)
- **What it does:** Pulls Hedy sessions, analyzes communication patterns (speaking share, hedging, filler words), flags low-visibility meetings, updates session/topic contexts, cascades to organs.
- **Trigger:** EOD-1 hook. Fully autonomous.
- **Feeds into:** Memory (relationships), Nervous System (communication patterns, Loop 7), Eyes (meeting prep)

### Slack Context Ingestion (via AM-1)
- **What it does:** Ingests all Slack channels Richard is in (via `list_channels`) plus DMs. Section-based depth: WW Testing/AB PS = full, AB/AI = standard, Channels = light. Proactive search beyond channel list (permanent + dynamic queries). Reaction checking on tagged messages.
- **Trigger:** AM-1 hook (morning scan). Signal routing happens in EOD-2 cascade.
- **Config:** `~/shared/context/active/slack-channel-registry.json` + `~/shared/context/active/slack-scan-state.json`
- **Source of truth:** `list_channels` — adapts automatically to channel joins/leaves.
- **Guardrails:** Read-only (per slack-guardrails.md). All invocations logged to scan state. No caps — ingest everything, synthesize ruthlessly.

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

## 👥 Delegation Protocols

| Delegation | Delegate | Status | Notes |
|-----------|----------|--------|-------|
| MX Invoicing | TBD | VOID | VOID since Carlos→CPS 3/17. Decision: Lorena takes it or Richard keeps it. Decide by 4/11. |
| MX Keyword Sourcing | Lorena | IN PROGRESS | Richard keeps strategy/bids/testing. Action: send keyword guide to Lorena. |
| WBR Coverage | Dwayne | ACTIVE | Normal coverage. Richard keeps PS callouts + backup. Gap: no backup handoff template — build one. |
| OP1 Contributors | Andrew, Stacey, Yun, Adi | IN PROGRESS | Andrew active. Confirm others. Set deadline for contributor sections. |

---

## 🛠️ Tool Factory

Templates (Email, WBR Callout, Meeting Prep) queued — build when prioritized.

| # | Tool | Status |
|---|------|--------|
| 0 | **Paid Search Audit** — Gmail Apps Script auto-ingest → [Bridge_AB-Ads-Data](https://docs.google.com/spreadsheets/d/1mNnQSaQUCSHJXcrssFmvYDLqoKimWFm56UCVpeA3wjQ). Needs: schedule reports, set up script, update config.json with CIDs. | **Richard action** |
| 1 | **Dashboard ingester** | ✅ BUILT |
| 1a | **PS Analytics DB (DuckDB)** | ✅ BUILT |
| 1b | **Context catalog** | ✅ BUILT |
| 2 | **Campaign link generator** — AU/MX sitelink URL construction | Backlog |
| 3 | **Staleness detector** — auto-check file freshness. Spec: scan all organ files, flag any with `last updated` > 7 days. Compare against gut.md §4 age-based decay thresholds. Output: bloat report for AM-3 brief. | Ready to build |

Backlog proposals: WBR auto-briefing, meeting prep auto-generator, invoice routing, testing tracker, keyword analysis pipeline. Build priority (brain.md Level 3): tools teammates adopt first.

---

## 📊 Device Health

| Group | Status | Last Run |
|-------|--------|----------|
| AM Hooks (AM-1, AM-2, AM-3) | ✅ | 4/2 |
| EOD Hooks (EOD-1, EOD-2) | ✅ | 4/3, 4/2 |
| Safety Guards (Email, Calendar) | ✅ | Always |
| Agents (Karpathy, Eyes Chart, Wiki Team) | ✅ | 3/24–3/25 |
| Data Pipeline (Ingester, DuckDB, Callouts, Predictions) | ✅ | 3/30 |
| Content Tools (Bridge, Charts, Catalog, SharePoint) | ✅ | 3/25–3/27 |
| Slack Ingestion v3 | ✅ | 4/2 |
| MCP Servers (Weblab, XWiki, Builder, Taskei) | 🆕 | 4/2 |
| Attention Tracker | 🔧 | 3/30 |

---

## When to Read This File

- When Richard says "I'll just do it myself" — check if a device function exists or should be built
- When evaluating whether work is high-leverage — if it's on the device, it shouldn't be on Richard
- When the trainer flags a recurring time trap — check if a delegation protocol or tool proposal exists
- When planning system-building sessions — the Tool Factory is the backlog
