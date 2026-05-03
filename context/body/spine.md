<!-- DOC-0228 | duck_id: organ-spine -->

**Key consideration:** This section's content is critical for accurate operation. Cross-reference with related sections for full context.
  - *Example:* Key consideration → apply this when the situation matches the described pattern.
# Spine — Structure & Continuity

*The skeleton that holds everything together across sessions. Bootstrap sequence, directory conventions, environment rules, and the ground-truth files that define Richard's current state.*

Last updated: 2026-04-01 (Wednesday PT)

---

**Key consideration:** This section's content is critical for accurate operation. Cross-reference with related sections for full context.
## Session Bootstrap Sequence



#### **Richard Williams:** L5




#### | # |


| # | File | What |
|---|------|------|
| 1 | `body.md` | System map — organ locations |
| 2 | `spine.md` | Bootstrap, tools, dirs |
| 3 | `soul.md` | Identity, voice, routing |
| 4 | `current.md` | Live state: projects, people, actions |
| 5 | `rw-tracker.md` | Weekly scorecard, 30-day challenge |


### Continued


[38;5;10m> [0m#### **First 60 seconds[0m[0m
[0m[0m
**Checklist:** (1) Read body.md for orientation. (2) Read spine.md for IDs and tools. (3) Read soul.md for voice and routing. (4) Read current.md for live state. (5) Check amcc.md for streak and hard thing. Then load task-specific organs per body.md Task Routing table.
#### **Cold-start recovery:** MotherDuck


**Cold-start recovery:** MotherDuck → SharePoint `system-state/` → Git `agent-bridge` → filesystem rebuild. If `body/` empty, pull from `Kiro-Drive/portable-body/` first.


#### **Cold-start anti-patterns:** Don't


**Cold-start anti-patterns:** Don't skip body.md (you'll miss organ locations). Don't load all organs at once (load task-specific only). Don't assume DuckDB is local (it's on MotherDuck cloud). Don't write to organs before reading current.md (you'll overwrite live state).



## Tool Access & Integrations

### MCP Servers (16 connected)

| Access | Servers |
|--------|---------|
| Full | Hedy · DuckDB · SharePoint/OneDrive · Builder (Quip/search/Taskei/phonetool/code/pipelines) · Wiki (w.amazon.com) · Local filesystem |
| Guarded | Email/Calendar/To-Do (prichwil-only) · Slack (write: C0993SRL6FQ + self_dm only) · Asana (GID 1212732742544167 only) |
| Read-only | ARCC (security KB) · KDS · Weblab · Loop · Taskei |
| Untested | Radar · Search Marketing (AgentCore Gateway) |
| None | Google Ads · Adobe Analytics |

Full inventory + guardrails: `~/shared/context/active/mcp-tool-reference.md`










### Tool Access Troubleshooting

**Common Failures:**
1. **Slack write to wrong channel.** Only `C0993SRL6FQ` (rsw-channel) and self_dm are writable. Any other channel write will fail silently or be blocked.
2. **Asana write to wrong user.** Only GID `1212732742544167` (Richard) is writable. Writes to other users' tasks are blocked by the guard hook.
3. **DuckDB schema-unqualified queries.** Always use schema-qualified names (e.g., `asana.asana_tasks`, not `asana_tasks`). Unqualified names may resolve to wrong schema or fail.
4. **Email send to non-Richard recipient without approval.** Email guard blocks unless sole recipient is prichwil. External sends need explicit approval.

**Worked example — tool access troubleshooting:** Query fails with "table not found" → check schema qualification. `SELECT * FROM asana_tasks` fails; `SELECT * FROM asana.asana_tasks` succeeds. Slack post to #ps-team fails silently → check channel ID. Only `C0993SRL6FQ` and self_dm are writable. Asana CreateTask for a teammate fails → guard hook blocks non-Richard GIDs.

---













**Daily hook sequence:** AM-Backend (Ingest + Process) → AM-Frontend (Brief + Triage + Command Center) → (workday) → EOD (unified backend + frontend: meeting sync, system refresh, Karpathy experiments on organs + output quality). Guards (Email, Calendar, Asana) are always-on preToolUse hooks. Session Summary fires on agentStop. On-demand: WBR Callouts, SharePoint Sync, PS Audit, Agent Bridge.

| Hook | File | Type | Trigger |
|------|------|------|---------|
| AM-Backend | `am-backend.kiro.hook` | Daily AM | userTriggered |
| AM-Frontend | `am-frontend.kiro.hook` | Daily AM | userTriggered (after AM-Backend) |
| EOD | `eod.kiro.hook` | Daily EOD | userTriggered |
| Session Summary | `session-summary.kiro.hook` | Meta | agentStop |
| Guard: Email | `guard-email.kiro.hook` | Always-on | preToolUse |
| Guard: Calendar | `guard-calendar.kiro.hook` | Always-on | preToolUse |
| Guard: Asana | `guard-asana.kiro.hook` | Always-on | preToolUse |
| WBR Callouts | `wbr-callouts.kiro.hook` | On-demand | WBR prep |
| SharePoint Sync | `sharepoint-sync.kiro.hook` | On-demand | Manual |
| PS Audit | `ps-audit.kiro.hook` | On-demand | Manual |
| Agent Bridge | `agent-bridge-sync.kiro.hook` | On-demand | Manual |

Full hook details: see device.md → Installed Apps and hands.md → Hook System.

**Cold Start Recovery:** If the filesystem is empty or corrupted: (1) Query MotherDuck `md:ps_analytics` for structured data, (2) Pull `Kiro-Drive/portable-body/` from SharePoint for organ snapshots, (3) Clone `agent-bridge` from GitHub for portable body + changelog, (4) Rebuild filesystem from these three sources. Do NOT start from scratch — at least two backup layers will have current data.

---









**Example:** This section demonstrates the pattern in practice — concrete instances ground abstract rules.


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












### Durability Model

**Example:** This section demonstrates the pattern in practice — concrete instances ground abstract rules.

#### Four Layers

The system survives any single point of failure through four independent persistence layers:

| Layer | Location | What It Stores | Survives |
|-------|----------|---------------|----------|
| Filesystem | `~/shared/` (DevSpaces persistent volume) | Everything — organs, protocols, tools, data | Container restart ✅, DevSpaces rebuild ❌ |
| SharePoint | OneDrive `Kiro-Drive/` | Hook outputs, published artifacts, portable body snapshots | Container restart ✅, DevSpaces rebuild ✅, Platform migration ✅ |
| Git | `agent-bridge` GitHub repo | Portable body, sanitized context, changelog | Container restart ✅, DevSpaces rebuild ✅, Platform migration ✅ |
| MotherDuck | `md:ps_analytics` cloud DB | All structured data (Asana, signals, experiments, PS metrics) | Container restart ✅, DevSpaces rebuild ✅, Platform migration ✅ |

**Recovery priority:** MotherDuck (structured data) → SharePoint (artifacts + state) → Git (portable body) → Filesystem (rebuild from other three).




### Quick-Check Keys


**Example:** This section demonstrates the pattern in practice — concrete instances ground abstract rules.

### Common Failures


**System history:** See changelog.md for full build history (3/12 onwards: trainer, loop, To-Do, Asana bridge, Hedy, wiki team, meetings, body metaphor migration, Slack ingestion).
