---
title: "Agent System Architecture: How the Body, Hooks, and Agents Work Together"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0431 | duck_id: wiki-agent-architecture -->

---
title: "Agent System Architecture: How the Body, Hooks, and Agents Work Together"
slug: "agent-architecture"
type: "guide"
doc-type: strategy
audience: "team"
status: "draft"
created: "2026-03-25"
updated: "2026-04-05"
owner: "Richard Williams"
tags: ["body-system", "agent", "hook", "steering", "tool", "mcp", "agent-bridge"]
depends_on: ["body-system-architecture"]
consumed_by: ["wiki-concierge", "karpathy", "agent-bridge-sync"]
summary: "Complete architecture guide for the body system, hook system, and agent swarm — how they connect, what each piece does, and how the whole system compounds."
artifact-status: DRAFT
artifact-audience: team
artifact-level: 5
update-trigger: "On structural changes — new agents, new hooks, new organs, architecture shifts"
---

# Agent System Architecture: How the Body, Hooks, and Agents Work Together

This doc explains the full architecture of Richard Williams' AI-assisted work system. The system comprises 11 organ files, 5 hooks, 13 custom agents organized into 3 teams, and 9 calibration loops. A new AI on a different platform should be able to read this and understand how the pieces fit together, what each component does, and how to bootstrap from cold start. A human observer should understand the design philosophy and operational flow.

## Context

This system was built iteratively starting March 2026 to augment Richard Williams' work as a Marketing Manager (L5) on Amazon Business Paid Search. It runs on Amazon's AgentSpaces platform (Kiro/Claude) but is designed for portability — every component is a plain text file that survives a platform move. The system uses a body metaphor: organs hold context, hooks trigger automation, agents execute specialized tasks, and a loop maintains everything autonomously.

The design draws from Karpathy's autoresearch (small, fast, autonomous experimentation loops that compound), Duhigg's habit loops (cue → routine → reward structures that eliminate decision fatigue), and McKeown's essentialism (subtraction before addition, routine as liberation).

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

11 organs, 23,000-word budget (hard ceiling 24,000), self-maintaining via autoresearch loop. Each organ answers its own questions without requiring cross-file reads. When an organ references another, it uses a pointer ("See Brain → D1") rather than duplicating content.

Ground truth files live separately from organs at `~/shared/context/active/` because they have different update cadences: `current.md` (live state, updated every loop run), `org-chart.md` (org structure, updated on org changes), and `rw-tracker.md` (weekly scorecard, updated every morning routine).

---

## Layer 2: Hooks & Automation

Hooks are event-driven triggers that start workflows without Richard deciding to start them. They're the cue in the habit loop — invariant triggers that eliminate the decision of "what should I do?"

### Active Hooks

| Hook | Trigger | What It Does |
|------|---------|-------------|
| Morning Routine | userTriggered (daily, one click) | Syncs Asana tasks, drafts email replies for review, refreshes to-do list with daily brief, and proposes calendar blocks |
| Run the Loop | userTriggered | Refreshes organs from email/calendar, cascades updates across the body, and optionally runs one experiment |
| Hedy Meeting Sync | userTriggered (after meetings) | Pulls Hedy meeting transcripts, analyzes communication patterns, audits contexts, and cascades updates to organs |
| Block Email Send | preToolUse (always on) | Prevents email send/reply/forward unless only recipient is Richard. Safety guard. |
| Block Calendar Invite | preToolUse (always on) | Prevents calendar events with external attendees. Safety guard. |

The first three hooks are Richard-triggered workflows that run the daily operating rhythm. The last two are always-on safety guards that prevent accidental external communication. The distinction matters: workflow hooks can be skipped on a given day, but safety hooks cannot be disabled without editing the hook config.

### The Morning Routine (Daily Driver)

The morning routine is the keystone habit. One click triggers a 4-step chain: Asana Sync, Draft Unread Replies, To-Do Refresh + Daily Brief, and Calendar Blocks. Richard's judgment is required only at step 2 (confirming draft replies) and step 4 (choosing which blocks to create). Everything else is autonomous.

### The Autoresearch Loop (Experimentation Engine)

The loop is inspired by Karpathy's autoresearch — 630 lines and 700+ experiments as of March 2026, with measurable accuracy improvements across all organs. It runs autonomously with no human input. It selects a target organ, applies an experiment (COMPRESS, ADD, RESTRUCTURE, REMOVE, REWORD, MERGE, or SPLIT), evaluates the result with dual blind subagent reviewers, and keeps or reverts based on accuracy thresholds.

The compressing agent never evaluates its own work. Two independent blind evaluators score questions against ground truth. Brain/Memory require 100% accuracy (wrong decisions or relationship data = real harm). Eyes/Hands require 95%. All others require 90%.

### Safety Guards

Two preToolUse hooks prevent accidental external communication. The email block prevents sends unless the only recipient is Richard. The calendar block prevents events with external attendees. These are structural interventions — they change the default from "send" to "confirm," which is more durable than a reminder to be careful.

---

## Layer 3: The Agent Swarm

Agents are specialized AI personas that handle specific domains. They read organs for context and execute within their scope. The soul.md file contains the routing directory — when a request matches an agent's domain, it gets routed there instead of handled generically.

### Agent Definition Pattern

Every agent has two files that serve different purposes:

The `.md` definition is the source of truth. It contains the agent's complete instructions: role, scope, workflow, rules, data sources, and output format. Any AI on any platform can read this file and understand what the agent does. The `.md` files live in subdirectories organized by team: `body-system/`, `wbr-callouts/`, `wiki-team/`.

The `.json` config is the environment-specific invocation layer. It makes the agent discoverable and invocable via `kiro-cli chat --agent <name>`. Each JSON config contains a condensed prompt, a `resources` field that loads the full `.md` definition at runtime, tool permissions (`read`, `write`, `shell`, `web`), and MCP server access flags. The `.json` files live at the root of `~/.kiro/agents/` because kiro-cli does not recurse into subdirectories.

This separation is deliberate. The `.md` files are portable — they survive a platform move and work with any AI that can read text. The `.json` configs are platform-specific — they encode kiro-cli's invocation format, tool categories, and MCP integration. On a different platform, you'd recreate equivalent configs in that platform's format while the `.md` definitions remain unchanged.

To recreate the invocation layer on a new platform, map these JSON fields to the platform's equivalent: `prompt` (condensed role description), `resources` (files the agent loads before executing), `tools` (capability categories — read/write/shell/web), and `includeMcpJson` (whether the agent needs access to external services like Asana, Slack, or DuckDB).

### Agent Teams

**Body System Agents (4):**

| Agent | Definition | What It Owns |
|-------|-----------|-------------|
| karpathy | `body-system/karpathy.md` | Loop governance, experiment queue, compression rules. Sole authority on heart.md and gut.md. |
| rw-trainer | `body-system/rw-trainer.md` | Career coaching, leverage assessment, Five Levels analysis. The performance coach. |
| eyes-chart | `body-system/eyes-chart.md` | Visualization specialist. Reads organs + market data, generates HTML dashboard with Chart.js. Read-only on all organs. |
| agent-bridge-sync | `body-system/agent-bridge-sync.md` | Syncs files to portable-body/, updates docs, pushes to agent-bridge GitHub repo. Friday cadence. |

Karpathy is the only agent with write access to heart.md and gut.md — a deliberate constraint that prevents other agents from modifying the experimentation protocol or compression rules. The other three agents are read-only on organs and write only to their own output domains.

**WBR Callout Pipeline (3):**

```
Market data (dashboard ingester)
  → market-analyst (produces analysis brief, one market per invocation)
    → callout-writer (produces callout draft, one market per invocation)
      → callout-reviewer (checks quality across all 10 markets)
```

| Agent | Markets | Role |
|-------|---------|------|
| market-analyst | Any (parameterized) | Analysis brief — reads market context, pulls DuckDB data, produces structured brief with projections |
| callout-writer | Any (parameterized) | Callout draft — transforms analysis brief into 100-120 word narrative prose |
| callout-reviewer | All 10 | Cross-market quality gate — scores on 5 dimensions, suggests specific edits |

Market-analyst and callout-writer are parameterized — they accept a market identifier and load market-specific rules at runtime. Adding a new market requires only a new context file, not a new agent.

The pipeline originally used 6 per-region agents (abix-analyst, najp-analyst, eu5-analyst, and corresponding writers). These were consolidated in March 2026 into 2 parameterized agents that accept a market parameter and read market-specific rules from `{market}-context.md` at runtime. The consolidation eliminated code duplication while preserving market-specific behavior.

**Wiki Team (6):**

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
| wiki-editor | Editorial director. Owns roadmap, assigns work, resolves feedback. |
| wiki-researcher | Gathers source material, produces research briefs. |
| wiki-writer | Transforms research into polished articles. Dual-audience (human + agent). |
| wiki-critic | Reviews articles, runs periodic audits, detects staleness. |
| wiki-librarian | Manages wiki structure, publishes articles, maintains catalog. |
| wiki-concierge | Search/lookup interface. Tracks demand signals. |

The pipeline is sequential — each agent's output is the next agent's input. The wiki-editor is the only agent that can assign work or resolve conflicting feedback, which prevents circular revision loops. The wiki-critic enforces an 8/10 bar with dual-blind evaluation before any article publishes, which prevents low-quality docs from accumulating.

### CLI Invocation

All 13 custom agents are invocable via kiro-cli:

```bash
echo "<prompt>" | kiro-cli chat --agent <name> --no-interactive --trust-all-tools --wrap never
```

This enables hooks and skills to orchestrate multi-agent pipelines programmatically. The WBR callout skill, for example, invokes market-analyst 10 times (once per market), then callout-writer for markets above the confidence threshold, then callout-reviewer across all drafts.

Soul.md routes requests to the matching agent — career coaching goes to rw-trainer, heart.md and gut.md changes require karpathy as gatekeeper, WBR callouts flow through the three-agent pipeline, wiki work starts with wiki-editor, and visualization requests go to eyes-chart. If the request doesn't clearly match an agent's domain, it gets handled directly rather than routed.

---

## Failure Modes and Recovery

**Experiment corruption.** An experiment can corrupt an organ if the dual-blind evaluators both miss a regression. Recovery: the autoresearch loop's revert mechanism restores the pre-experiment version from the last known-good snapshot. Brain and Memory organs require 100% accuracy specifically to minimize this risk.

**Routing sprawl.** Soul.md routing becomes unwieldy beyond roughly 20 agents because the routing directory is a flat list with no hierarchy. At that scale, we'd need to introduce team-level routing — route to a team lead agent, which sub-routes to specialists.

**Word budget ceiling.** The 24,000-word ceiling on the body system is a hard constraint. When total organ content approaches the ceiling, the gut agent flags it, but the only resolution is compression or removal — there's no mechanism to expand the budget without degrading session context quality.

---

## How the System Compounds

The autoresearch loop has run 700+ experiments as of March 2026, with organ accuracy scores improving from initial baselines of 70-80% to current thresholds of 90-100% depending on the organ. The nervous system's nine calibration loops (decision audits, prediction scoring, pattern tracking, and six others) detect drift before it compounds — when a principle stops holding or a prediction misses, the system flags it for correction rather than letting the error propagate. Over time, the wiki externalizes knowledge that organs previously held, which frees word budget for higher-value context.

---

## Portability

The system is designed to survive a platform move with nothing but text files. Every component is a markdown file. No binary dependencies. No platform-specific APIs that can't be replaced.

What's portable: all organ files, all agent `.md` definitions, all steering files, research files, callout data, wiki articles. The `portable-body/` directory is the survival kit — a snapshot of the most critical files, synced weekly to the agent-bridge GitHub repo.

What's platform-specific (and replaceable): hooks (AgentSpaces JSON format, but intent documented in hooks-inventory.md), agent `.json` configs (kiro-cli format, but the `.md` definitions carry the full instructions — see Agent Definition Pattern above), MCP integrations (Hedy, Outlook, Asana — replaceable with equivalent APIs), tool access (email, calendar, task management — any platform has equivalents), and file paths (`~/shared/context/` — remap to any directory structure).

Cold start protocol: a new AI reads `portable-body/README.md` → `body/body.md` → `body/spine.md` → `soul.md`. Within 2-3 hours, it should be operational. To recreate the agent invocation layer, read each `.md` definition and create equivalent configs in the new platform's format.

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
│   ├── *.json          # CLI-invocable configs (13 custom + platform agents)
│   ├── body-system/    # .md definitions: karpathy, rw-trainer, eyes-chart, agent-bridge-sync
│   ├── wbr-callouts/   # .md definitions: market-analyst, callout-writer, callout-reviewer
│   └── wiki-team/      # .md definitions: editor, researcher, writer, critic, librarian, concierge
├── hooks/              # Event-driven automation (morning routine, guards, audit)
├── skills/             # Multi-agent pipeline definitions (wbr-callouts, coach, etc.)
└── settings/           # MCP server config
```

## Decision Guide

| Situation | Action | Why |
|-----------|--------|-----|
| New AI, cold start | See cold start protocol in Portability section above. | Bootstrap sequence gets you operational in 2-3 hours. |
| Need to add a new agent | Write `.md` definition in appropriate subfolder, create `.json` config at root (see Agent Definition Pattern above), add routing rule to soul.md. | `.md` is the portable spec; `.json` makes it CLI-invocable. |
| Need to add a new organ | Check gut.md word budget first. Justify why existing organs can't absorb the content. | Subtraction before addition. The body should trend simpler. |
| Need to add a new hook | Document in device.md. Ensure it has a clear trigger and doesn't duplicate existing hooks. | Hooks are structural interventions. Each one should eliminate a recurring decision. |
| System feels bloated | Run gut.md bloat detection. Check word budgets. Run compression experiment. | The gut is the only organ whose job is removal. |
| Platform migration | Copy all `.md` files. Recreate `.json` configs in new platform's format (see Agent Definition Pattern above). Remap file paths. Replace MCP integrations with equivalents. | The `.md` files ARE the system. The `.json` configs are the environment adapter. |

## Sources

- Describes the body system architecture, organ map, and operating principles — source: `shared/context/body/body.md`
- Documents the loop protocol and experiment results — source: `shared/context/body/heart.md`
- Defines the hook system and installed apps — source: `shared/context/body/device.md`
- Contains all agent definitions organized by team — source: `~/.kiro/agents/` directory (body-system/, wbr-callouts/, wiki-team/)
- Specifies agent JSON configs, validated and tested 2026-04-05 — source: `~/.kiro/agents/*.json`
- Enforces word budgets and bloat detection — source: `shared/context/body/gut.md`
- Runs 9 calibration loops for system self-correction — source: `shared/context/body/nervous-system.md`
- Routes requests to the matching agent — source: `~/.kiro/steering/soul.md`
- Defines the session bootstrap sequence — source: `shared/context/body/spine.md`
- Explains portability as a continuous design constraint — source: `shared/context/body/heart.md`
- Records the agent consolidation from 6 per-region to 2 parameterized — source: `~/.kiro/specs/agent-consolidation/`, completed March 2026

<!-- AGENT_CONTEXT
machine_summary: "Complete architecture guide for Richard Williams' AI work system. Three layers: (1) Body System — 11 organ files holding current state within a 23,000-word budget, (2) Hooks — 5 event-driven triggers including morning routine (daily keystone habit), autoresearch loop (autonomous experimentation with 700+ experiments as of March 2026), and safety guards, (3) Agent Swarm — 13 custom agents across body-system (4), WBR callouts (3, parameterized for all 10 markets), and wiki team (6, pipeline: editor → researcher → writer → critic → librarian). All agents use a dual-file pattern: .md definitions (portable, source of truth) + .json configs (platform-specific CLI invocation). System compounds via autoresearch (organ accuracy 90-100%), nervous system (9 calibration loops), and wiki externalization. Designed for portability — all plain text, cold start in 2-3 hours."
key_entities: ["body system", "organs", "hooks", "agents", "autoresearch loop", "morning routine", "Karpathy", "gut", "word budget", "agent-bridge", "soul.md", "spine.md", "nervous system", "kiro-cli", "json config", "md definition", "market-analyst", "callout-writer"]
action_verbs: ["bootstrap", "route", "experiment", "compress", "calibrate", "cascade", "externalize", "invoke"]
update_triggers: ["new agent added", "new hook added", "new organ added", "architecture structural change", "platform migration", "agent definition pattern change"]
-->
