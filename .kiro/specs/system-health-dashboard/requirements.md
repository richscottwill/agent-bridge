# Requirements Document: System Health Dashboard

## Introduction

Widen the existing Agent Health card in the Body System dashboard view into a unified "System Health" panel covering three subsystems: custom agents (with runtime invocation telemetry), hooks (reliability surfacing from existing data), and MCP servers (registry + health-check). Today, agent liveness is a black box — the karpathy-via-subagent 4/20 failure was invisible because there's no invocation log. Hook failures are captured in `ops.hook_executions` and `ops.hook_reliability` (DuckDB tables tracking hook run history and reliability metrics) but never rendered. MCP server status is unknowable without manually testing each server. This spec replaces three black boxes with one panel.

**Origin**: `.kiro/specs/dashboard-learnings-roadmap/design.md` — Item #6 (System Health Dashboard, MCP + Agents + Hooks). Ranked #6 of 13 roadmap items. Classification: `IMPROVE` (widened from former `spec mcp-health-dashboard`), effort M (1–3 days), leverage High.

**Five Levels alignment**: L1 (Sharpen Yourself) — system health visibility prevents wasted time debugging tool failures and surfaces shelfware agents for removal. Directly supports the L1 key metric (consecutive weeks shipped) by reducing time lost to invisible infrastructure failures.

**Soul principles**:
- Invisible over visible — the health check runs automatically; Richard only sees it when something is wrong. Silent when healthy, loud when broken.
- Subtraction before addition — the panel's first job is surfacing agents, hooks, and servers to *delete*, not admiring the ones that exist. Every subsection includes an "idle too long" flag that surfaces removal candidates.

**Adoption gate**: This panel ships only if paired with a monthly review cadence that acts on the signals (kill idle agents, fix failing hooks, remove dead MCP servers). Without that commitment, the panel is decoration — and decoration violates Structural over cosmetic.

## Glossary

- **Body System**: Dashboard view at `~/shared/dashboards/index.html` showing system internals — agent definitions, hook status, data freshness, and organ health
- **Agent Health card**: Existing static card in Body System that displays agent success metrics from JSON definition files. This spec widens it into the "System Health" panel.
- **System Health panel**: The new unified panel replacing Agent Health, with three subsections: Agents, Hooks, MCP Servers
- **ops.agent_invocations**: New DuckDB table (created by this spec) recording every custom-agent invocation with status, duration, and cost estimate
- **ops.hook_executions**: Existing DuckDB table capturing hook run history (hook name, start/end time, status, error details)
- **ops.hook_reliability**: Existing DuckDB view computing reliability metrics per hook (success rate, avg duration, recent failures)
- **Logging shim**: A lightweight wrapper around agent invocation calls that records telemetry to `ops.agent_invocations` without changing the invocation interface
- **invokeSubAgent**: The Kiro tool used to delegate tasks to custom agents (e.g., `rw-trainer`, `karpathy`, `wiki-editor`)
- **mcp.json**: Configuration files defining MCP server connections — exists at `~/.kiro/settings/mcp.json` (global) and workspace-level `mcp.json`
- **Health-check ping**: A lightweight probe sent to each MCP server to verify it responds. Not a functional test — just "are you alive?"
- **Routing adherence**: The percentage of chat inputs matching a soul.md routing trigger that actually routed to the specialist agent vs were handled by the main agent
- **Idle flag**: A visual indicator on an agent, hook, or MCP server that hasn't been invoked/run/pinged within a configurable threshold, surfacing it as a removal candidate
- **Five Levels**: Richard's sequential strategic priorities — L1 Sharpen Yourself → L2 Drive WW Testing → L3 Team Automation → L4 Zero-Click Future → L5 Agentic Orchestration
- **Soul principles**: The 6 "How I Build" principles in `soul.md` — Routine as liberation, Structural over cosmetic, Subtraction before addition, Protect the habit loop, Invisible over visible, Reduce decisions not options
- **Command Center**: Dashboard home view with Hero, Daily Blocks, Integrity Ledger, Actionable Intelligence
- **DuckDB**: The analytical database (`ps_analytics` on MotherDuck) storing operational, performance, and system data

## Scope

### In scope

- **Tier 1 (must have)**: `ops.agent_invocations` DuckDB table + logging shim for custom-agent invocations + agent telemetry display in Body System
- **Tier 1 (must have)**: Hook reliability surfacing from existing `ops.hook_executions` / `ops.hook_reliability` data in Body System
- **Tier 2 (should have)**: MCP server registry parsed from `mcp.json` configs + health-check ping + status display
- **Tier 3 (optional, punt if costly)**: Routing adherence metric for soul.md trigger keywords
- Unified "System Health" panel in Body System replacing the current Agent Health card
- "Idle too long" flags per subsection surfacing removal candidates

### Out of scope

- Modifying the agent invocation interface itself — the shim wraps existing calls, it doesn't change how agents are invoked
- Creating new hooks or modifying hook behavior — this spec only *surfaces* existing hook data
- Replacing MCP servers or changing MCP configuration — this spec only *monitors* server health
- Real-time streaming dashboards or WebSocket connections — the panel refreshes on dashboard load like all other sections
- Multi-user access or team-wide visibility — Richard is the sole user
- Automated remediation (auto-restarting failed MCP servers, auto-disabling broken hooks) — the panel surfaces signals for human decision
- Mobile or responsive layout — the dashboard is desktop-only
- Tier 3 routing adherence if implementation cost exceeds 1 day of additional work (punt to a separate experiment spec)

## Requirements

### Requirement 1: Agent Invocation Telemetry Table

**User Story**: As Richard, I want every custom-agent invocation recorded in a queryable table, so I can see which agents are actually being used, which are failing, and which are shelfware.

#### Acceptance Criteria

1. WHEN the system is set up, THEN a DuckDB table `ops.agent_invocations` SHALL exist with columns: `invocation_id` (UUID, primary key), `agent_name` (text), `caller` (text — the agent or user that triggered the invocation), `invoke_status` (text, constrained to `success`, `failed`, `unreachable`, `timed_out`), `duration_seconds` (numeric), `error_message` (text, nullable), `invoked_at` (timestamp), `token_cost_estimate` (numeric, nullable)
2. WHEN a custom agent is invoked via `invokeSubAgent`, THEN the logging shim SHALL record one row in `ops.agent_invocations` with the invocation outcome
3. WHEN a custom agent is invoked via `kiro-cli chat --agent X`, THEN the logging shim SHALL record one row in `ops.agent_invocations` with the invocation outcome
4. WHEN an agent invocation fails or times out, THEN the `error_message` column SHALL capture the error detail (truncated to 500 characters if longer)
5. WHEN an agent is structurally unreachable (e.g., not exposed via `invokeSubAgent`, missing definition file), THEN the `invoke_status` SHALL be `unreachable` — distinct from `failed` (which means the agent was reached but errored)
6. WHEN the logging shim records an invocation, THEN it SHALL NOT add more than 200ms of latency to the invocation call — logging is fire-and-forget, not blocking

### Requirement 2: Agent Telemetry Display

**User Story**: As Richard opening Body System, I want to see at a glance which agents are active, which are failing, and which haven't been invoked in weeks — so I can decide what to fix and what to kill.

#### Acceptance Criteria

1. WHEN the System Health panel loads, THEN the Agents subsection SHALL display one row per known agent (from agent definition files + any agent appearing in `ops.agent_invocations`)
2. WHEN an agent row is displayed, THEN it SHALL show: agent name, last-invoked timestamp (or "Never" if no invocations), 7-day invocation count, 30-day invocation count, and failure count in the last 7 days
3. WHEN an agent has zero invocations in the last 30 days, THEN it SHALL be flagged with an "idle" indicator (e.g., gray badge or muted row) surfacing it as a removal candidate
4. WHEN an agent has any failures in the last 7 days, THEN the failure count SHALL be displayed in red/warning color
5. WHEN an agent has `unreachable` status in its most recent invocation, THEN it SHALL be flagged with a distinct "unreachable" indicator — this is a structural problem, not a transient failure
6. WHEN agent rows are displayed, THEN they SHALL be sorted by last-invoked timestamp descending (most recently used first), with never-invoked agents at the bottom

### Requirement 3: Hook Reliability Surfacing

**User Story**: As Richard, I want to see which hooks ran recently, which failed, and which are stale — using data that's already being captured — so I don't have to query DuckDB manually to know if my automation is healthy.

#### Acceptance Criteria

1. WHEN the System Health panel loads, THEN the Hooks subsection SHALL display one row per hook found in `ops.hook_executions`
2. WHEN a hook row is displayed, THEN it SHALL show: hook name, last_run timestamp, recent_failures count (last 7 days), and avg_duration (from `ops.hook_reliability`)
3. WHEN a hook has any failures in the last 7 days, THEN it SHALL be flagged with a warning indicator (e.g., orange/red badge with failure count)
4. WHEN a hook's last_run is more than 72 hours ago, THEN it SHALL be flagged with a "stale" indicator — the hook may be broken or no longer triggering
5. WHEN a hook has both recent failures AND stale last_run, THEN both flags SHALL appear — they are independent signals
6. WHEN hook data is displayed, THEN it SHALL require NO new logging — this requirement surfaces existing `ops.hook_executions` and `ops.hook_reliability` data only

### Requirement 4: MCP Server Registry and Health Check

**User Story**: As Richard, I want to see which MCP servers are configured, whether they're responding, and which ones are down — so I don't discover a broken server mid-task when I need it.

#### Acceptance Criteria

1. WHEN the System Health panel loads, THEN the MCP Servers subsection SHALL display one row per server parsed from `~/.kiro/settings/mcp.json` and workspace-level `mcp.json` configs
2. WHEN an MCP server row is displayed, THEN it SHALL show: server name, source config file (global vs workspace), and health status indicator
3. WHEN a health-check ping succeeds within a reasonable response time, THEN the server status SHALL be green (responsive)
4. WHEN a health-check ping succeeds but response time exceeds a configurable threshold (default: 5 seconds), THEN the server status SHALL be yellow (slow)
5. WHEN a health-check ping fails (connection refused, timeout, error), THEN the server status SHALL be red (failed) with the error reason displayed
6. WHEN all MCP servers are green, THEN the MCP Servers subsection SHALL be visually quiet — no alerts, no attention-grabbing elements (Invisible over visible: silent when healthy)
7. WHEN any MCP server is red, THEN the subsection header SHALL show an alert count (e.g., "MCP Servers (1 down)") to draw attention without requiring Richard to scan every row

### Requirement 5: Routing Adherence Metric (Tier 3 — Optional)

**User Story**: As Richard, I want to know what percentage of my chat inputs that match a routing trigger actually routed to the specialist agent — so I can tell if the routing system is working or if the main agent is swallowing requests it should delegate.

#### Acceptance Criteria

1. WHEN routing adherence is implemented, THEN the system SHALL maintain a set of routing trigger keywords derived from soul.md's Agent Routing Directory (e.g., "coaching", "career", "1:1 prep", "retrospective" → rw-trainer; "heart.md", "gut.md", "experiment queue" → karpathy)
2. WHEN a chat input matches one or more routing triggers, THEN the system SHALL log whether the input was routed to the specialist or handled by the main agent
3. WHEN the System Health panel loads, THEN the routing adherence metric SHALL display: total trigger-matched inputs (7d), % that routed correctly, and a list of the most common "missed routes" (trigger matched but not routed)
4. WHEN routing adherence cannot be implemented without wrapping the routing decision with logging that adds complexity disproportionate to the value, THEN this requirement SHALL be deferred to a separate experiment spec — it is explicitly optional
5. WHEN routing adherence is deferred, THEN the System Health panel SHALL still function fully with Tiers 1 and 2 — Tier 3 is additive, not a dependency

### Requirement 6: Unified System Health Panel Layout

**User Story**: As Richard, I want agents, hooks, and MCP servers in one panel — not three separate cards — so I can assess system health in one glance instead of scanning the entire Body System view.

#### Acceptance Criteria

1. WHEN the System Health panel is rendered, THEN it SHALL replace the existing Agent Health card in Body System — not appear alongside it (Subtraction before addition: one panel replaces one card, net zero UI elements)
2. WHEN the System Health panel is rendered, THEN it SHALL contain three collapsible subsections: "Agents" (invocation telemetry), "Hooks" (reliability), "MCP Servers" (status)
3. WHEN all subsections are healthy (no failures, no stale hooks, no down servers, no idle agents), THEN the panel SHALL display a compact summary (e.g., "All systems healthy — 6 agents, 12 hooks, 4 MCP servers") without expanding subsection details
4. WHEN any subsection has an issue (failure, staleness, downtime, idle flag), THEN that subsection SHALL auto-expand to show the problem rows — healthy subsections remain collapsed
5. WHEN the panel is rendered, THEN it SHALL use the same CSS framework, font sizes, spacing, and color palette as existing Body System cards
6. WHEN each subsection is displayed, THEN it SHALL include an "idle too long" summary line showing the count of agents/hooks/servers flagged as idle or stale — surfacing removal candidates per Subtraction before addition

### Requirement 7: Adoption Gate

**User Story**: As Richard, I don't want to build a monitoring panel that becomes decoration — I want the spec to enforce that the panel is paired with a review cadence that acts on the signals.

#### Acceptance Criteria

1. WHEN the System Health panel is shipped, THEN it SHALL be paired with a documented monthly review cadence (e.g., first Monday of each month) that reviews idle agents, failing hooks, and down MCP servers
2. WHEN the monthly review cadence is defined, THEN it SHALL specify concrete actions: kill agents with zero invocations in 60 days, investigate hooks with >3 failures in 30 days, remove MCP server configs that have been red for >14 days
3. WHEN the monthly review has not been performed within 45 days, THEN the System Health panel header SHALL display a "Review overdue" indicator — the panel holds itself accountable
4. WHEN the adoption gate is not met (no review cadence committed), THEN the panel SHALL NOT be shipped — building monitoring without acting on it violates Structural over cosmetic

## Design Constraints

1. **No new infrastructure**: The System Health panel must work within the existing dashboard architecture — HTML/CSS/JS in `~/shared/dashboards/`, data via DuckDB queries and `mcp.json` file parsing, no new backend services.
2. **Single-user assumption**: Richard is the sole user. No multi-user concurrency, no auth beyond existing credentials.
3. **Existing pattern reuse**: The panel layout must match existing Body System cards. The logging shim must integrate with existing invocation patterns without requiring callers to change their code.
4. **Tiered delivery**: Tier 1 (agent telemetry + hook surfacing) is the minimum viable delivery. Tier 2 (MCP registry) ships if time permits. Tier 3 (routing adherence) ships only if implementation cost is clearly low — otherwise it becomes a separate experiment spec.
5. **Non-blocking logging**: The agent invocation logging shim must not degrade agent invocation performance. Fire-and-forget writes to DuckDB, not synchronous inserts in the invocation path.
6. **Subtraction check**: The panel replaces the existing Agent Health card (net zero UI additions). If the panel doesn't surface actionable signals within the first month of use, it should be removable without breaking anything else.
7. **Data freshness**: Hook and agent data refresh on dashboard load. MCP health-check pings run on dashboard load (not continuously). Staleness thresholds are configurable.
