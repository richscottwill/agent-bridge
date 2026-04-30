
# Body — System Anatomy Map


Last updated: 2026-04-04 (Karpathy Run 25 — Task Routing table: organ names→file paths)

---

| Organ | File | Function | When to read |
|-------|------|----------|-------------|
| 🔥 Soul | `~/.kiro/steering/soul.md` | Identity, values, voice, preferences | Session start. Rarely changes. |
| ❤️ Heart | `~/shared/context/body/heart.md` | Autoresearch loop protocol, experiment queue, results | Before running the loop. System health checks. |
| 🧠 Brain | `~/shared/context/body/brain.md` | Decision log, principles, Five Levels, leverage framework | Prioritizing work. Making recommendations. Predicting Richard's position. |
| 👁️ Eyes | `~/shared/context/body/eyes.md` | Market metrics, OCI performance, competitors, ad copy results, predicted QA | Preparing for meetings. Assessing market health. Building narratives. |
| ✋ Hands | `~/shared/context/body/hands.md` | Action tracker, dependencies, To-Do list IDs, hooks, integrations, tool opportunities | Executing tasks. Checking what's pending. Using integrations. |
| 🧠💬 Memory | `~/shared/context/body/memory.md` | Compressed context, relationship graph, reference links | Answering questions. Drafting communications. Relationship context. |
| 🦴 Spine | `~/shared/context/body/spine.md` | Bootstrap sequence, tool access, key IDs, directory map, ground truth file pointers | Session start. Orienting a new agent. Finding IDs. |
| 📱 Device | `~/shared/context/body/device.md` | Automation, delegation, templates, monitors, tool factory | When offloading work. When "I'll just do it myself" triggers. |
| 🧬 Nervous System | `~/shared/context/body/nervous-system.md` | Calibration, feedback loops, decision audits, prediction scoring, pattern tracking, system health | Fridays (weekly calibration). Monthly deep review. When something feels off. |
| 🔥 Anterior MCC | `~/shared/context/body/amcc.md` | Willpower engine, real-time avoidance detection, streak tracking, resistance taxonomy, escalation | Every session. When Richard drifts to comfort zone. The hard thing. |
| 🏛️ Amazon Politics | `~/shared/context/body/amazon-politics.md` | Corporate politics, promotion mechanics, PIPs, reorgs, influence tactics, leverage, polite fictions (Ethan Evans VP reference) | Career coaching. 1:1 prep. Skip-level prep. Promotion planning. Org dynamics. Stakeholder conflict. |
| 🫁 Gut | `~/shared/context/body/gut.md` | Digestion, compression, waste removal, word budgets, bloat detection | During loop cascade. When organs feel bloated. Monthly compression review. |
| 📥 Intake | `~/shared/context/intake/` | Unprocessed notes, drafts, new docs | During heart loop Phase 1. Not for direct consumption. |
| 🛠️ Tools | `~/shared/tools/` | Python utility scripts (MCP, sync, briefs). Hedy now via MCP power. | When building or running automation. |
| 📰 Wiki | `~/shared/wiki/` | Doc pipeline + context catalog. Published output → Artifacts. | When creating docs or searching for context. |
| 📦 Artifacts | `~/shared/wiki/` | Published work product (7 categories). Level 1 evidence. | When shipping or referencing finished docs. |
| 🗓️ Meetings | `~/shared/wiki/meetings/` | Meeting series notes, session summaries, stakeholder dynamics, open items. One file per series. | Meeting prep. Drafting follow-ups. Checking open items. Understanding stakeholder positions. |

---



## Task Routing (load only what you need)
---

| Task Type | Required Files | Optional |
|-----------|---------------|----------|
| Draft an email/message | `memory.md`, `soul.md`, `current.md` | `brain.md` (if strategic) |
| Prioritize work | `brain.md`, `hands.md`, `amcc.md` | `eyes.md` (deadlines) |
| Prepare for a meeting | `meetings/{series}.md`, `eyes.md` | `memory.md`, `brain.md` |
| Assess market performance | `eyes.md` | `brain.md` (decisions) |
| Build/propose a tool | `device.md`, `brain.md` | `hands.md` (what's manual) |
| Run the morning routine | ALL (see hook for load order) | — |
| Run the loop | `heart.md`, ALL organs (cascade) | — |
| Check system health | `nervous-system.md`, `gut.md` | All organs (staleness) |
| Start a new session | `spine.md`, `body.md`, `amcc.md` | Then task-specific |




## Ground Truth (separate files, different update cadences)

These stay in `~/shared/context/active/` and are NOT absorbed into organs:

| File | What it is | Updated by |
|------|-----------|------------|
| `current.md` | Live state: projects, people, meetings, pending actions | Every loop run |
| `org-chart.md` | Org structure and reporting lines | On org changes |
| `rw-tracker.md` | Weekly scorecard, To-Do sync, patterns, 30-day challenge | Every morning routine |
| `long-term-goals.md` | The Five Levels strategic arc | Monthly or on shift |
| `asana-command-center.md` | Asana command center protocol, field GIDs, capabilities | On Asana changes |
| `mcp-tool-reference.md` | MCP API docs and gotchas | On tool discovery |
