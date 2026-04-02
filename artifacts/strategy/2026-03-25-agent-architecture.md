---
title: "Agent System Architecture: How the Body, Hooks, and Agents Work Together"
slug: "agent-architecture"
type: "guide"
audience: "team"
status: "draft"
created: "2026-03-25"
updated: "2026-03-25"
owner: "Richard Williams"
tags: ["body-system", "agent", "hook", "steering", "tool", "mcp", "portable-body"]
depends_on: []
consumed_by: ["wiki-concierge", "karpathy", "agent-bridge-sync"]
summary: "Complete architecture guide for the body system, hook system, and agent swarm — how they connect, what each piece does, and how the whole system compounds."
# Artifact metadata
artifact-status: DRAFT
artifact-audience: agent-only
artifact-level: 5
update-trigger: "On structural changes — new agents, new hooks, new organs, architecture shifts"
---

# Agent System Architecture: How the Body, Hooks, and Agents Work Together

This doc explains the full architecture of Richard Williams' AI-assisted work system. A new AI on a different platform should be able to read this and understand how the pieces fit together, what each component does, and how to bootstrap from cold start. A human observer should understand the design philosophy and operational flow.

## Context

This system was built iteratively starting March 2026 to augment Richard Williams' work as a Marketing Manager (L5) on Amazon Business Paid Search. It runs on Amazon's AgentSpaces platform (Kiro/Claude) but is designed for portability — every component is a plain text file that survives a platform move. The system uses a body metaphor: organs hold context, hooks trigger automation, agents execute specialized tasks, and a loop maintains everything autonomously.

The design philosophy draws from three sources:
- **Andrej Karpathy's autoresearch** — small, fast, autonomous experimentation loops that compound
- **Charles Duhigg's habit loops** — cue → routine → reward structures that eliminate decision fatigue
- **Greg McKeown's essentialism** — subtraction before addition, routine as liberation

## The Three Layers

```
┌─────────────────────────────────────────────┐
│  LAYER 3: AGENT SWARM                       │
│  Specialized agents for specific domains     │
│  (callouts, wiki, coaching, visualization)   │
├─────────────────────────────────────────────┤
│  LAYER 2: HOOKS & AUTOMATION                │
│  Event-driven triggers that start workflows  │
│  (morning routine, loop, safety guards)      │
├─────────────────────────────────────────────┤
│  LAYER 1: BODY SYSTEM (Organs)              │
│  Context files that hold current state       │
│  (brain, eyes, hands, memory, etc.)          │
└─────────────────────────────────────────────┘
```

Each layer depends on the one below it. Agents read organs to do their work. Hooks trigger agents and organ updates. Organs are the ground truth that everything else references.

---

## Layer 1: The Body System

The body is a set of 11 self-contained markdown files ("organs"), each responsible for a specific domain of Richard's work context. For the full body system architecture — organ map, design principles, data flow, and word budget system — see [Body System Architecture](~/shared/artifacts/program-details/2026-03-25-body-system-architecture.md).

**Key facts:** 11 organs, 23,000-word budget (hard ceiling 24,000), self-maintaining via autoresearch loop. Current total ~17,996 words. Each organ answers its own questions without requiring cross-file reads. When an organ references another, it uses a pointer ("See Brain → D1") rather than duplicating content.

**Ground truth files** live separately from organs at `~/shared/context/active/` because they have different update cadences:
- `current.md` — live state (projects, people, pending actions). Updated every loop run.
- `org-chart.md` — org structure. Updated on org changes.
- `rw-tracker.md` — weekly scorecard, To-Do sync, patterns. Updated every morning routine.

---

## Layer 2: Hooks & Automation

Hooks are event-driven triggers that start workflows without Richard deciding to start them. They're the cue in the habit loop — invariant triggers that eliminate the decision of "what should I do?"

### Active Hooks

| Hook | Trigger | What It Does |
|------|---------|-------------|
| Morning Routine (`rw-morning-routine`) | userTriggered (daily, one click) | Asana Sync → Draft Unread Replies → To-Do Refresh + Daily Brief → Calendar Blocks |
| Run the Loop (`run-the-loop`) | userTriggered ("run the loop") | Maintenance (refresh from email/calendar) → Cascade (update organs) → Optionally 1 experiment |
| Hedy Meeting Sync (`hedy-meeting-sync`) | userTriggered (after meetings) | Pull Hedy sessions → analyze communication patterns → audit contexts → cascade to organs |
| Block Email Send | preToolUse (always on) | Prevents email send/reply/forward unless only recipient is Richard. Safety guard. |
| Block Calendar Invite | preToolUse (always on) | Prevents calendar events with external attendees. Safety guard. |

### The Morning Routine (Daily Driver)

The morning routine is the keystone habit. One click triggers a 4-step chain:

1. **Asana Sync** — Pull task updates from Asana via email bridge (Outlook "Auto-Comms" folder)
2. **Draft Unread Replies** — Scan inbox, draft replies for routine emails, present triage table for Richard's confirmation
3. **To-Do Refresh + Daily Brief** — Sync Microsoft To-Do lists, generate daily brief with priorities, calendar, and gut check
4. **Calendar Blocks** — Propose time blocks for deep work based on calendar gaps

Richard's judgment is required only at Step 2 (confirming draft replies) and Step 4 (choosing which blocks to create). Everything else is autonomous.

### The Autoresearch Loop (Experimentation Engine)

The loop is inspired by Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) — 630 lines, 700 experiments, measurable results. It runs autonomously with no human input.

**What it does:** Selects a target organ, applies an experiment (COMPRESS, ADD, RESTRUCTURE, REMOVE, REWORD, MERGE, or SPLIT), evaluates the result with dual blind subagent reviewers, and keeps or reverts based on accuracy thresholds.

**Evaluation protocol:** The compressing agent never evaluates its own work. Two independent blind evaluators score 5 questions (3 standard + 2 adversarial). Both must score ≥4/5 to keep. This is the PR review for every experiment.

**Accuracy thresholds:** Brain/Memory require 100% (wrong decisions or relationship data = real harm). Eyes/Hands require 95%. All others require 90%.

**9 completed runs** as of 3/25/2026. 8 of those runs included experiments (all kept — 100% keep rate). Run 9 was a maintenance-only run (organ refresh, no experiment). 4 compression experiments adopted across those 8, saving 2,827 words (29% across 4 organs).

### Safety Guards

Two preToolUse hooks prevent accidental external communication:
- **Email block:** No sends unless the only recipient is Richard (prichwil). External sends require explicit approval.
- **Calendar block:** No events with external attendees. Personal blocks are allowed.

These are structural interventions — they change the default from "send" to "confirm," which is more durable than a reminder to be careful.

---

## Layer 3: The Agent Swarm

Agents are specialized AI personas that handle specific domains. They read organs for context and execute within their scope. The soul.md file contains the routing directory — when a request matches an agent's domain, it gets routed there instead of handled generically.

### Agent Teams

**Body System Agents:**

| Agent | File | What It Owns |
|-------|------|-------------|
| Karpathy | `agents/body-system/karpathy.md` | Loop governance, experiment queue, compression rules. Sole authority on heart.md and gut.md. No other agent modifies these files. |
| RW Trainer | `agents/body-system/rw-trainer.md` | Career coaching, leverage assessment, Five Levels analysis. The performance coach. |
| Eyes Chart | `agents/body-system/eyes-chart.md` | Visualization specialist. Reads organs + market data, generates HTML dashboard with Chart.js. Read-only on all organs. |
| Agent Bridge Sync | `agents/body-system/agent-bridge-sync.md` | Syncs files to portable-body/, updates docs, pushes to agent-bridge GitHub repo. Friday cadence. |

**WBR Callout Pipeline:**

```
Market data (dashboard ingester)
  → Analyst agent (produces analysis brief)
    → Writer agent (produces callout draft)
      → Reviewer agent (checks quality across all markets)
```

| Agent | Markets | Role |
|-------|---------|------|
| ABIX Analyst | AU, MX | Analysis brief |
| ABIX Callout Writer | AU, MX | Callout draft |
| NAJP Analyst | US, CA, JP | Analysis brief |
| NAJP Callout Writer | US, CA, JP | Callout draft |
| EU5 Analyst | UK, DE, FR, IT, ES | Analysis brief |
| EU5 Callout Writer | UK, DE, FR, IT, ES | Callout draft |
| Callout Reviewer | All markets | Cross-market quality check |

The pipeline is sequential: analyst → writer → reviewer. Don't skip steps.

**Wiki Team:**

```
wiki-editor (orchestrator — assigns work, resolves feedback)
  ├── wiki-researcher (gathers source material)
  │     └── wiki-writer (drafts article to staging)
  │           └── wiki-critic (reviews, scores, flags issues)
  │                 └── wiki-librarian (publishes to wiki, manages structure)
  └── wiki-concierge (search/lookup — can be invoked directly)
```

| Agent | Role |
|-------|------|
| Wiki Editor | Editorial director. Owns roadmap, assigns work, resolves feedback. |
| Wiki Researcher | Gathers source material, produces research briefs. |
| Wiki Writer | Transforms research into polished articles. Dual-audience (human + agent). |
| Wiki Critic | Reviews articles, runs periodic audits, detects staleness. |
| Wiki Librarian | Manages wiki structure, publishes articles, maintains catalog. |
| Wiki Concierge | Search/lookup interface. Tracks demand signals. |

### Routing Rules

The soul.md routing directory maps triggers to agents:

| Trigger Pattern | Route To |
|----------------|----------|
| Career coaching, growth planning, pattern stuck 3+ times | rw-trainer |
| heart.md, gut.md, experiment queue changes | karpathy (gatekeeper) |
| "Write W__ callouts" for AU/MX | abix-analyst → abix-callout-writer |
| "Write W__ callouts" for US/CA/JP | najp-analyst → najp-callout-writer |
| "Write W__ callouts" for EU5 | eu5-analyst → eu5-callout-writer |
| Wiki content creation | wiki-editor (orchestrates the rest) |
| Wiki search/lookup | wiki-concierge (direct) |
| Dashboard/visualization | eyes-chart |
| Agent-bridge sync | agent-bridge-sync |

**Key rule:** If the request clearly falls in one agent's domain, route to that agent. Don't try to handle it yourself. If unsure, handle it — only route when the match is clear.

---

## How the System Compounds

The system is designed to get better over time without getting bigger. Three compounding mechanisms:

### 1. The Autoresearch Loop
Every experiment either improves an organ's usefulness-per-token or gets reverted. Over time, organs answer more questions more accurately in fewer words. 9 runs, 8 experiments, 100% keep rate, 2,827 words saved.

### 2. The Nervous System
Nine calibration loops evaluate whether the system is working. Decision audits check if principles hold. Prediction scoring measures forecasting accuracy. Pattern tracking detects stuck behaviors. The system self-corrects.

### 3. The Wiki
Knowledge that's useful beyond the agent system gets externalized as wiki articles. Organs are for agents. The wiki is for humans AND agents. Over time, the wiki becomes the canonical reference and organs can point to it instead of holding the content themselves.

---

## Portability

The system is designed to survive a platform move with nothing but text files. Every component is a markdown file. No binary dependencies. No platform-specific APIs that can't be replaced.

**What's portable:**
- All organ files (plain markdown)
- All agent definitions (plain markdown)
- All steering files (plain markdown)
- Research files, callout data, wiki articles
- The `portable-body/` directory is the survival kit — a snapshot of the most critical files

**What's platform-specific (and replaceable):**
- Hooks (AgentSpaces-specific, but the logic is documented in device.md)
- MCP integrations (Hedy, Outlook — replaceable with equivalent APIs)
- Tool access (email, calendar, To-Do — any platform has equivalents)
- File paths (`~/shared/context/` — remap to any directory structure)

**Cold start protocol:** A new AI reads `portable-body/README.md` → `body/body.md` → `body/spine.md` → `soul.md`. Within 2-3 hours, it should be operational. CE-7 (queued experiment) will validate this claim.

## Directory Structure

```
~/shared/
├── context/
│   ├── body/           # 11 organ files + device
│   ├── active/         # Ground truth (current.md, org-chart.md, rw-tracker.md)
│   │   └── callouts/   # Per-market WBR callout data (10 markets + ww)
│   ├── intake/         # Inbox for unprocessed material
│   ├── archive/        # Cold storage
│   ├── tools/          # Utility scripts
│   └── wiki/           # Wiki articles, staging, research, roadmap
├── research/           # Standalone research outputs
├── reference/          # Static references
└── artifacts/          # Strategic work product (Level 1 evidence)

~/.kiro/
├── steering/           # Agent behavior config (soul.md, writing styles, trainer)
├── agents/
│   ├── body-system/    # Karpathy, trainer, eyes-chart, agent-bridge-sync
│   ├── wbr-callouts/   # Analyst, writer, reviewer agents (3 pipelines)
│   └── wiki-team/      # Editor, researcher, writer, critic, librarian, concierge
└── settings/           # MCP server config, hooks
```

## Decision Guide

| Situation | Action | Why |
|-----------|--------|-----|
| New AI, cold start | Read portable-body/README.md → body.md → spine.md → soul.md | Bootstrap sequence gets you operational in 2-3 hours |
| Need to add a new organ | Check gut.md word budget first. Justify why existing organs can't absorb the content. | Subtraction before addition. The body should trend simpler. |
| Need to add a new agent | Define in `~/.kiro/agents/` with clear scope. Add routing rule to soul.md. | Agents must have clear domain boundaries. Overlap causes confusion. |
| Need to add a new hook | Document in device.md. Ensure it has a clear trigger and doesn't duplicate existing hooks. | Hooks are structural interventions. Each one should eliminate a recurring decision. |
| System feels bloated | Run gut.md bloat detection. Check word budgets. Run compression experiment. | The gut is the only organ whose job is removal. |
| Platform migration | Copy all markdown files. Remap file paths. Replace MCP integrations with equivalents. | Everything is plain text. The system is the files, not the platform. |

## Related

- [Body Map](~/shared/context/body/body.md) — navigation layer for the whole system
- [Heart — Loop Protocol](~/shared/context/body/heart.md) — autoresearch experiment methodology
- [Spine — Bootstrap](~/shared/context/body/spine.md) — session startup sequence and tool access
- [Device — Installed Apps](~/shared/context/body/device.md) — hooks, agents, templates, delegation
- [Gut — Compression](~/shared/context/body/gut.md) — word budgets and bloat detection
- [Soul — Identity](~/.kiro/steering/soul.md) — agent routing directory and operating principles

## Sources
- Body system architecture — source: `shared/context/body/body.md`, organ map and operating principles
- Loop protocol and experiment results — source: `shared/context/body/heart.md`, run protocol and experiment queue
- Hook system — source: `shared/context/body/device.md`, Installed Apps section
- Agent definitions — source: `~/.kiro/agents/` directory (body-system/, wbr-callouts/, wiki-team/)
- Word budgets — source: `shared/context/body/gut.md`, Word Budget Enforcement table
- Calibration loops — source: `shared/context/body/nervous-system.md`, 9 loops
- Routing directory — source: `~/.kiro/steering/soul.md`, Agent Routing Directory
- Bootstrap sequence — source: `shared/context/body/spine.md`, Session Bootstrap Sequence
- Portability design — source: `shared/context/body/heart.md`, Design Choices (portability as continuous constraint)

<!-- AGENT_CONTEXT
machine_summary: "Complete architecture guide for Richard Williams' AI work system. Three layers: (1) Body System — 11 organ files holding current state within a 23,000-word budget (see Body System Architecture for full detail), (2) Hooks — 5 event-driven triggers including morning routine (daily keystone habit) and autoresearch loop (autonomous experimentation, 9 runs, 8 experiments, 100% keep rate), (3) Agent Swarm — 18+ specialized agents across body-system, WBR callouts (3 market pipelines), and wiki team (6 agents, pipeline: editor → researcher → writer → critic → librarian). System compounds via autoresearch, nervous system (9 calibration loops), and wiki externalization. Designed for portability — all plain text, cold start in 2-3 hours."
key_entities: ["body system", "organs", "hooks", "agents", "autoresearch loop", "morning routine", "Karpathy", "gut", "word budget", "portable-body", "soul.md", "spine.md", "nervous system"]
action_verbs: ["bootstrap", "route", "experiment", "compress", "calibrate", "cascade", "externalize"]
update_triggers: ["new agent added", "new hook added", "new organ added", "architecture structural change", "platform migration"]
-->
