<!-- DOC-0221 | duck_id: organ-device -->
# Device — Outsourced Intelligence

*The body's phone/laptop/agent. Work that runs FOR Richard without requiring his judgment. If it needs Richard's brain, it's an organ. If it can execute autonomously, it belongs here.*

*Operating principle: Routine as liberation. Every delegation, template, and automation here exists to eliminate a decision Richard was making repeatedly. The test for a new device function: "Does this remove a recurring decision?" If yes, build it. If it just moves the decision, skip it.*

Last updated: 2026-04-13 (Forecast pipeline rebuild: _Data sheet architecture, regime changes, weighted predictions, template-based updater)

---

## The Test

Before adding anything here, ask: "Does this require Richard's judgment to produce a correct output?"
- **Yes** → It's an organ (brain, hands, etc.)
- **No** → It's a device function. Automate it, delegate it, or template it.

---

## 🤖 Installed Apps (running today)

These are live. They execute without Richard thinking.

### AM Hooks (2 sequential: backend → frontend)
- **AM-Backend** (`am-auto`) — Parallel ingestion (6 subagents: Slack, Asana Sync, Asana Activity, Email+Calendar, Loop Pages, Hedy) → sequential processing (signal routing, enrichment, portfolio scan) → SharePoint sync. ~12 min. Protocol: `am-backend-parallel.md`
- **AM-Frontend** (`am-triage`) — Interactive: daily brief, email brief, calendar blocks, enrichment execution, ABPS AI triage, portfolio alerts, command center. Reads backend state (local first, SharePoint fallback). ~10 min. Protocol: `am-frontend.md`

### EOD Hook (1 unified: backend + frontend)
- **EOD** (`eod`) — Backend: Hedy meeting ingestion, Asana reconciliation (delta sync, daily reset, recurring, completion moves, blockers), organ cascade, compression audit, workflow health, context enrichment, DuckDB snapshots, git sync, Karpathy experiments, SharePoint sync. Frontend: day summary, decisions, portfolio report, system health, experiment results, Slack DM. ~20 min. Protocol: `eod-backend.md` + `eod-frontend.md`

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
- **What it does:** 6-agent doc pipeline: editor → researcher → writer → critic → librarian + concierge. Publishes to `~/shared/wiki/`. 15 artifacts. 8/10 quality bar (critic is required gate).
- **Trigger:** On demand. Editor orchestrates. Agent files: `~/.kiro/agents/wiki-team/`

### Agent Bridge (Tool: `~/shared/tools/bridge/bridge.py`)
- **What it does:** Google Sheets/Docs async message bus + context snapshots between Kiro and Richard's personal agent swarm.

### WBR Forecast Pipeline (Tool: `~/shared/tools/wbr-pipeline.sh`)
- **What it does:** End-to-end weekly pipeline: ingest WW Dashboard xlsx → sync to MotherDuck → detect regime changes → score prior predictions → generate Bayesian weekly projections (regime-change-aware) → populate forecast_tracker (weighted predictions + actuals backfill) → update forecast xlsx (_Data sheet only) → push to SharePoint.
- **Trigger:** Weekly, after WW Dashboard xlsx is available. Manual: `bash ~/shared/tools/wbr-pipeline.sh <xlsx_path>`
- **Key scripts:**
  - `wbr-pipeline.sh` — orchestrator (8 steps)
  - `prediction/populate_forecast_tracker.py` — Bayesian projections + weighted predictions (λ=0.2 exponential decay) + actuals backfill. Monthly/quarterly/year-end derived from weekly sums.
  - `prediction/detect_regime_changes.py` — scans ps.change_log for structural changes, auto-inserts into ps.regime_changes
  - `prediction/bayesian_projector.py` — Bayesian engine with seasonal priors, regime change prior shifts, ie%CCP constraints
  - `dashboards/update-forecast-tracker.py` — writes ONLY to hidden _Data sheet in xlsx, preserving all visible sheet formatting
  - `prediction/config.py` — shared MotherDuck token + constants (single source)
- **Architecture:** Hidden `_Data` sheet holds all raw values. Visible market sheets use formulas referencing `_Data`. Script never touches visible sheets.
- **Hook:** `forecast-sharepoint-push` (fileEdited) auto-pushes xlsx to SharePoint Kiro-Drive/ + Dashboards/ after update.
- **Legacy:** `build-forecast-tracker.py.legacy` — replaced by template-based updater.

### Open Items Reminder (Hook: `open-items-reminder`)
- **What it does:** On first message of a new conversation, scans session-log.md for OPEN/deferred items and surfaces them. Skips if already shown in current conversation. 3-hour cooldown.
- **Trigger:** promptSubmit (with conversation-level dedup)

### Forecast SharePoint Push (Hook: `forecast-sharepoint-push`)
- **What it does:** Auto-pushes ps-forecast-tracker.xlsx to both SharePoint locations when the file is updated locally.
- **Trigger:** fileEdited on shared/dashboards/ps-forecast-tracker.xlsx
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

### SharePoint Durability Layer (Protocol: `sharepoint-durability-sync.md`)
- **What it does:** Bidirectional sync between `~/shared/` and OneDrive `Kiro-Drive/`. Pushes AM/EOD output artifacts for cross-device access and container-death resilience. Pulls on cold start when local files are missing.
- **Push triggers:** AM-Backend Phase 5.5, EOD-Backend Phase 7.5, wiki article publish, strategic artifact ship, Friday portable body snapshot.
- **Pull triggers:** Cold start (missing local files), container restart between backend/frontend, on-demand artifact retrieval.
- **SharePoint paths:** `Kiro-Drive/system-state/` (hook outputs), `Kiro-Drive/portable-body/` (snapshots), `Kiro-Drive/meeting-briefs/` (prep docs). Published artifacts go to `Artifacts/wiki-sync/` via the separate sharepoint-sync hook.
- **NOT synced:** Organs, DuckDB, intake files, hooks, steering, audit logs.
- **Error handling:** Non-blocking. Local files are source of truth. SharePoint is durability layer, not dependency.
- **Three-layer durability:** filesystem (`~/shared/`) + SharePoint (`Kiro-Drive/`) + git (agent-bridge). Any two can fail and the system recovers.

### PS Analytics Database (DuckDB → MotherDuck Cloud)
- **What it does:** Persistent cloud analytical DB for all structured PS data and system telemetry. 8 schemas, 55 tables + 34 views.
- **Cloud DB:** `md:ps_analytics` on MotherDuck (aws-us-east-1). Persistent — survives container recycles. `USE ps_analytics` is set.
- **MCP access:** DuckDB MCP Server (`execute_query`, `list_tables`, `list_columns`). Config: `.kiro/settings/mcp.json` with MOTHERDUCK_TOKEN env var.
- **Schema layout (migrated 2026-04-06):**
  - `asana` — task management: asana_tasks, asana_task_history, asana_audit_log, daily_tracker, recurring_task_state, recurring_tasks (6 tables, 8 views)
  - `signals` — cross-channel intelligence: signal_tracker, unified_signals, slack_messages, slack_people, slack_threads, slack_topics, signal_task_log (7 tables, 8 views)
  - `karpathy` — body optimization: autoresearch_experiments, autoresearch_organ_health, autoresearch_priors, karpathy_experiment_log, experiment_outcomes, body_size_history, organ_word_counts (7 tables, 7 views)
  - `ns` — nervous system loops: ns_communication, ns_decisions, ns_delegations, ns_loop_snapshots, ns_patterns, decisions (6 tables, 2 views)
  - `ops` — system operations: hook_executions, workflow_executions, session_log, intake_metrics, data_freshness, builder_cache (6 tables, 2 views)
  - `wiki` — publishing pipeline: wiki_pipeline_runs, publication_registry (2 tables, 1 view)
  - `ps` — **Paid Search / Acquisition analytics** (WBR/MBR/QBR/annual): metrics, targets, forecasts, pacing, accounts, account_metrics, dashboard_uploads, markets, channels, change_log, competitive_signals, projections, health_alerts (13 tables, 5 views)
  - `main` — personal productivity: five_levels_weekly, l1_streak, meeting_analytics, meeting_highlights, meeting_series, relationship_activity, content_embeddings, experiments (8 tables, 1 view)
- **CRITICAL: Always use schema-qualified names** (e.g., `asana.asana_tasks`, not just `asana_tasks`). See steering file `duckdb-schema.md` for full reference.
- **Schema guard:** `~/shared/tools/data/ensure-schema.sql` — needs update to match new schema layout.
- **Local backup:** `~/shared/tools/data/ps-analytics.duckdb` (pre-migration snapshot, not actively written to).
- **Extensions:** core_functions, icu, json, parquet, jemalloc, fts (full-text search), vss (vector similarity search), motherduck.
- **FTS index:** `signals.slack_messages` — needs rebuild after schema migration (FTS was on old main.slack_messages).
- **Portability:** MotherDuck accessible from any DuckDB client with the token. Local .duckdb file as cold backup. Parquet exports at `~/shared/data/exports/`.

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

### Built & Shipped

| # | Tool | Status |
|---|------|--------|
| 1 | **Dashboard ingester** | ✅ BUILT |
| 1a | **PS Analytics DB (DuckDB)** | ✅ BUILT |
| 1b | **Context catalog** | ✅ BUILT |

### Backlog & Candidates

| # | Tool | Status |
|---|------|--------|
| 0 | **Paid Search Audit** — Gmail Apps Script auto-ingest → Bridge_AB-Ads-Data. Needs: schedule reports, set up script, update config.json with CIDs. | **Richard action** |
| 2 | **Campaign link generator** — AU/MX sitelink URL construction | Backlog |
| 3 | **Staleness detector** — auto-check file freshness. Scan all organ files, flag any with `last updated` > 7 days. Output: bloat report for AM-3 brief. | Ready to build |
| 4 | **gcm (AI git commit)** — Shell function that pipes `git diff --cached` to an LLM for commit message generation. Requires `llm` CLI. Source: wiki/Topics/Git/add_to_zshrc.sh. | Ready to install |
| 5 | **llm CLI** — Simon Willison's general-purpose LLM CLI tool. Pipe any text to any model. Pairs with gcm. Source: https://llm.datasette.io/. | Ready to install |
| 6 | **Harlequin** — TUI for DuckDB. Browse tables, run queries interactively from terminal. Source: https://harlequin.sh. | Backlog |

Backlog proposals: WBR auto-briefing, meeting prep auto-generator, invoice routing, testing tracker, keyword analysis pipeline. Build priority (brain.md Level 3): tools teammates adopt first.

### Candidate Install: gcm + llm CLI
**Source:** wiki/Topics/Git (Karpathy/Simon Willison ecosystem)
**Install steps:**
1. `pip install llm` (or `uv tool install llm`)
2. `llm keys set openai` (or configure preferred model)
3. Add gcm function to `~/.bashrc` (source: `~/shared/wiki/Topics/Git/add_to_zshrc.sh`)
4. Test: stage a change, run `gcm`
**Status:** Ready to install. Richard action — requires API key setup.

---

## 📊 Device Health

| Group | Status | Last Run |
|-------|--------|----------|
| AM Hooks (Backend + Frontend) | ✅ | 4/4 |
| EOD Hook (Unified) | ✅ | 4/11 |
| Safety Guards (Email, Calendar, Asana) | ✅ | Always |
| Audit (Asana Writes) | ✅ | Always |
| SharePoint Durability Sync | 🆕 | 4/12 (folders created, first data push pending) |
| Agents (Karpathy, Eyes Chart, Wiki Team) | ✅ | 3/24–3/25 |
| Data Pipeline (Ingester, DuckDB, Callouts, Predictions) | ✅ | 4/13 |
| Forecast Pipeline (WBR → MotherDuck → xlsx → SharePoint) | ✅ | 4/13 |
| Regime Change Detection | ✅ | 4/13 |
| Forecast SharePoint Push Hook | ✅ | 4/13 |
| Open Items Reminder Hook | ✅ | 4/13 |
| Content Tools (Bridge, Charts, Catalog, SharePoint Wiki Sync) | ✅ | 3/25–3/27 |
| Slack Ingestion v3 | ✅ | 4/2 |
| MCP Servers (Weblab, XWiki, Builder, Taskei) | 🆕 | 4/2 |
| Attention Tracker | 🔧 | 3/30 |
| DuckDB FTS (Slack search) | ✅ | 4/5 |
| DuckDB VSS (content embeddings) | 🆕 | 4/5 (table created, empty) |
| Parquet Exports | ✅ | 4/5 |

---

## When to Read This File

- When Richard says "I'll just do it myself" — check if a device function exists or should be built
- When evaluating whether work is high-leverage — if it's on the device, it shouldn't be on Richard
- When the trainer flags a recurring time trap — check if a delegation protocol or tool proposal exists
- When planning system-building sessions — the Tool Factory is the backlog
