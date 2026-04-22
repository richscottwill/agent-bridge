# Design Document: Skills & Powers Adoption

## Overview

This design produces one human-facing reference system and two machine-facing artifacts. The human-facing deliverables are a routing decision tree (for new-workflow intake) and a skills-powers inventory (for "what do I already have"). The machine-facing artifacts are a skill/power metadata schema extension (so files self-declare sensitivity and portability) and an append-only activation log (so staleness is computable). Everything else is working state or documentation.

**Reading order for the agent executing this adoption system**: Interplay with system-subtraction-audit → Architecture → Data Model → Routing Decision Tree → Sensitive-Data Classification Rules → Portability Tier Rules → Inventory File Spec → Candidate Identification → Adoption Habit Integration → Safe-Creation Workflow → Round-Trip File Format → Pruning Review → Anti-Goals → Design Decisions → Correctness Properties → Portability Check.

**Design stance**: This is governance, not a product. The adoption system does not deploy. It defines rules, a decision tree, a metadata schema, and a lightweight inventory + log. New skills and powers are built downstream by separate specs that consume these rules. If the rules need to change, a future spec edits this file; the rules themselves do not ship as code.

**Why so thin on "implementation"**: The 10 requirements already specify the *what*. This design specifies the *how* with the same granularity as the sibling `system-subtraction-audit/design.md` — data-model fields, decision-tree branches, and worked examples — so a different-platform agent could re-execute the governance procedures without this spec's supporting context.

### Interplay with system-subtraction-audit

This spec is the positive-construction complement to `system-subtraction-audit`. The audit applies *subtraction-before-addition* (soul.md #3) to the existing system. This adoption system applies the same principle to every *new* workflow Richard would otherwise bolt on. Specifically:

1. **Every mechanism this spec introduces passes the audit's own classification tests.** The audit's `Current Usage Test` and `Future Workflow Test` (requirements R5.4-5.5 of the audit) apply here too. Each component in the Architecture section declares its `Workflow dependency:` and `Future workflow:` labels. Components that fail both tests are METAPHOR-ONLY and are cut. See §Design Decisions → "What we almost added and cut".

2. **We reuse the audit's artifact patterns, not parallel ones.**
   - Row IDs for inventory rows: `K-{kind}{N}` where `kind` ∈ {S (skill), P (power)} and `N` is 1-indexed within kind. Matches the audit's `{L}-{A}{N}` grammar.
   - Format split: one human-facing markdown (`inventory.md`) + one machine-facing JSONL (`activation-log.jsonl`) + transient JSON intermediates during creation (`overlap-check.json`). Same convention as the audit's `kill-list.md` + `execution.log` + intermediate JSONs.
   - Archive pattern: any retired skill/power file moves to `~/shared/wiki/agent-created/archive/skills-powers-pruned-{YYYY-MM-DD}/` before deletion, same shape as the audit's spec-archive path.

3. **Search scope and referrer classification are respected.** The audit treats `.kiro/specs/**` as `documentation` referrers, not load-bearing. For the inventory and routing-framework doc to count as *active* referrers that save skills/powers from ORPHAN status in future audits, they must live **outside** `.kiro/specs/`. Both live at `~/shared/context/skills-powers/` (active scope per audit R2.8). The `.kiro/specs/skills-powers-adoption/` directory is the authoring scratchpad and gets archived when the initial build-out is complete.

4. **No auto-loaded steering.** The audit's R5.6 warns: any always-loaded steering that path-references a candidate file becomes UNCLEAR with default KEEP — which means a bad-taste steering file can permanently save orphan content. This adoption system deliberately does **not** create a `.kiro/steering/skills-powers.md` auto-loaded layer. The inventory is consulted on-demand by the agent's natural lookup flow (when the agent is about to draft a skill or hit a keyword-match opportunity), never via steering frontmatter.

5. **This spec is the extension-first answer to the audit's open question #7** ("restructure surviving files as extension-loaded modules per the pi / OpenClaw architecture pattern"). Skills via `discloseContext` and Powers via `kiroPowers activate` are already that pattern — extension-loaded, keyword-gated, on-demand. The adoption system's job is to route *new* workflows to this extension-loaded mechanism by default rather than adding more always-loaded steering or more hook surface.

6. **The routing tree has an explicit reject-for-subtraction branch before any mechanism-selection branches.** The first question the tree asks is not "skill or power?" — it is "should this workflow be codified at all?" If the workflow is one-off, low-leverage, or already covered by memory + a simple prompt, the tree terminates at REJECT. This applies soul.md #3 (subtraction before addition) inside the design of the adoption system itself.

---

## Architecture

The adoption system is an ongoing **governance loop**, not a one-time audit. Five phases run on different cadences: inventory refresh is reactive (triggered by create/prune events), routing intake is reactive (triggered by Richard proposing a new workflow), safe-creation is reactive (triggered by routing deciding CREATE), activation logging is continuous (every skill/power invocation writes one line), and pruning review is human-triggered (Richard invokes it monthly or ad-hoc).

```
  Phase A: INVENTORY REFRESH (reactive — on create / prune / install / uninstall)
      |
      | inputs: filesystem state of ~/.kiro/skills/, ~/.kiro/powers/installed/
      |         activation-log.jsonl
      | produces: inventory.md (updated in-session)
      v

  Phase B: NEW-WORKFLOW INTAKE (reactive — on Richard proposing a new workflow)
      |
      | inputs: Richard's workflow description
      | procedure: walk Routing Decision Tree
      | produces: routing-decision.json (transient, one per intake)
      |           → terminal leaf: REJECT | SKILL | POWER | STEERING | HOOK | SUBAGENT | ORGAN | EXTEND-EXISTING
      v

  Phase C: SAFE-CREATION (reactive — only if Phase B terminates at CREATE-new)
      |
      | inputs: routing-decision.json
      | procedure:
      |   C1. overlap-check against existing mechanisms
      |   C2. Richard review of proposed content + declared metadata
      |   C3. write file
      |   C4. activation-validate (call discloseContext / kiroPowers activate)
      |   C5. update inventory.md + append creation entry to activation-log.jsonl
      | produces: new SKILL.md or POWER.md
      |           overlap-check.json (archived with the new asset as evidence)
      v

  Phase D: ACTIVATION LOGGING (continuous — every activation during a session)
      |
      | inputs: any discloseContext or kiroPowers activate call
      | procedure: append one line to activation-log.jsonl
      | produces: activation-log.jsonl (append-only, survives sessions)
      v

  Phase E: PRUNING REVIEW (human-triggered — Richard invokes monthly or ad-hoc)
      |
      | inputs: inventory.md, activation-log.jsonl
      | procedure:
      |   E1. compute stale set (not activated in 30d)
      |   E2. present list to Richard
      |   E3. on approval: archive → delete → update inventory
      | produces: updated inventory.md
      |           archive at ~/shared/wiki/agent-created/archive/skills-powers-pruned-{date}/
```

**Why these five and not more**: an earlier sketch had a sixth phase for "periodic keyword-match audit" — walk every response and flag missed-skill opportunities. That phase was cut. The missed-skill note is part of Phase D (emitted inline during a response, not in a batch pass) and the keyword-match logic lives in the skill description itself (§Adoption Habit Integration). A separate batch phase would be a dashboard-shaped mechanism that fails both of the audit's workflow tests.

**Why it's five phases and not one "always-on adoption service"**: the audit's anti-goal #1 ("not an ongoing audit service") applies here. A recurring hook that checks for stale skills every day would itself be new surface area. Richard invokes pruning when the inventory feels bloated; the activation log captures data continuously because logging one line is cheap; everything else is reactive to Richard's intent.

---

## Data Model

### Skill metadata extension — SKILL.md frontmatter

Existing frontmatter (per `~/.kiro/skills/bridge-sync/SKILL.md`):

```yaml
---
name: bridge-sync
description: "Sync files to shared/context/... Triggers on sync to git, bridge sync, portable body, agent bridge."
---
```

Extended frontmatter required by this adoption system:

```yaml
---
name: bridge-sync
description: "Sync files to shared/context/... Triggers on sync to git, bridge sync, portable body, agent bridge."
sensitive_data_class: Amazon_Internal     # one of: Public | Amazon_Internal | Amazon_Confidential | Personal_PII
portability_tier: Platform_Bound          # one of: Cold_Start_Safe | Platform_Bound
platform_bound_dependencies:              # required iff portability_tier == Platform_Bound, else omitted
  - kind: script                          # one of: mcp_tool | subagent | hook | script | duckdb_table
    id: "scripts/sync.sh"
  - kind: mcp_tool
    id: "mcp_ai_community_slack_mcp_post_message"
owner_agent: bridge-sync                  # which agent/subagent should be consulted on edits; null if none
created_at: "2026-04-22T01:00:00-07:00"   # ISO 8601 with TZ; set once, never mutated
last_validated: "2026-04-22T01:00:00-07:00"  # updated whenever activation-validate passes
---
```

**Field definitions**:
- `name` (string, required, existing): unique identifier, matches directory name.
- `description` (string, required, existing): one-line purpose that ends with `Triggers on {keyword}, {keyword}, ...`. The trigger list is what the agent keyword-matches against; the adoption system's keyword-activation heuristic parses the last sentence for comma-separated triggers.
- `sensitive_data_class` (enum, required): see §Sensitive-Data Classification Rules. If missing, validator errors; treated as `Amazon_Confidential` when the file is read for routing decisions (R3.5 default).
- `portability_tier` (enum, required): `Cold_Start_Safe` or `Platform_Bound`. See §Portability Tier Rules.
- `platform_bound_dependencies` (list, conditionally required): required iff `portability_tier == Platform_Bound`. Each entry has `{kind, id}` where `kind` is one of the enumerated kinds. Informational — not resolved at runtime, but parsed by the portability validator to confirm the file's internal consistency.
- `owner_agent` (string, nullable): if this skill's logic is owned by a specialist agent (e.g., `wiki-writer`, `rw-trainer`, `karpathy`), name them. Null when no specialist owns the skill.
- `created_at` (ISO 8601 datetime with TZ, required): immutable. Written by Phase C safe-creation.
- `last_validated` (ISO 8601 datetime with TZ, required): updated by Phase C.4 (activation-validate) and by any explicit re-validation. Stale `last_validated` (> 90 days) is a signal for the portability validator to re-check but not itself a pruning trigger.

### Power metadata extension — POWER.md frontmatter

Existing frontmatter (per `~/.kiro/powers/installed/power-builder/POWER.md`):

```yaml
---
name: "power-builder"
displayName: "Power Builder"
description: "..."
keywords: ["kiro power", "power builder", "build power", ...]
author: "Kiro Team"
---
```

Extended frontmatter required by this adoption system:

```yaml
---
name: "power-builder"
displayName: "Power Builder"
description: "..."
keywords: ["kiro power", "power builder", ...]
author: "Kiro Team"
sensitive_data_class: Public              # same enum as skills
portability_tier: Cold_Start_Safe         # same enum as skills
platform_bound_dependencies: []           # required iff Platform_Bound
mcp_servers_declared:                     # mirrors mcp.json — redundant but keeps POWER.md self-describing
  - "power-builder"
created_at: "2026-01-15T00:00:00-08:00"
last_validated: "2026-04-22T01:00:00-07:00"
---
```

**New fields**: `sensitive_data_class`, `portability_tier`, `platform_bound_dependencies`, `mcp_servers_declared`, `created_at`, `last_validated`. Same semantics as the skill fields.

**Note on `keywords`**: powers already declare `keywords` in frontmatter — the adoption system's keyword-activation heuristic uses this list directly for powers (same way it parses the trigger list from skill descriptions). Powers do not need an additional trigger field.

### Inventory file — `~/shared/context/skills-powers/inventory.md`

**Location**: `~/shared/context/skills-powers/inventory.md`. This is inside the audit's active-scope (R2.8 of the audit) so any path-reference from the inventory to a skill or power counts as an active referrer and saves it from ORPHAN status in a future audit.

**Shape**: single markdown file, one table per kind, sorted by kind then by name.

```markdown
# Skills & Powers Inventory

**Last updated**: 2026-04-22T01:00:00-07:00
**Activation log**: ~/shared/context/skills-powers/activation-log.jsonl

## Skills (~/.kiro/skills/)

| Row ID | Name | Triggers | Sensitivity | Portability | Last Activated | Status |
|--------|------|----------|-------------|-------------|----------------|--------|
| K-S1 | bridge-sync | sync to git, bridge sync, portable body, agent bridge | Amazon_Internal | Platform_Bound | 2026-04-20 | used |
| K-S2 | charts | chart, dashboard, visualize, show dashboard | Amazon_Internal | Platform_Bound | 2026-04-18 | used |
| ... | ... | ... | ... | ... | ... | ... |

## Powers (~/.kiro/powers/installed/)

| Row ID | Name | Type | Sensitivity | Portability | Last Activated | Status |
|--------|------|------|-------------|-------------|----------------|--------|
| K-P1 | power-builder | Knowledge Base | Public | Cold_Start_Safe | never | unused |
| K-P2 | aws-agentcore | Guided MCP | Public | Platform_Bound | 2026-04-10 | used |
| ... | ... | ... | ... | ... | ... | ... |

## Staleness

- **Unused (never activated)**: K-P1, K-S5
- **Stale (no activation in 30+ days)**: K-S7
- **Candidates for next pruning review**: K-P1 (installed 2025-12, never activated; >14d dormant per R6.5)
```

**Columns**:
- `Row ID`: `K-S{N}` for skills, `K-P{N}` for powers, 1-indexed within kind. Stable within a given inventory rendering; may shift on re-render. The inventory header includes the sha256 of the rendering's input state so shifts are detectable.
- `Name`: from frontmatter.
- `Triggers` (skills) / `Type` (powers): trigger keywords for skills; `Guided MCP` or `Knowledge Base` for powers (derived from presence of `mcp.json`).
- `Sensitivity`, `Portability`: from frontmatter. Missing → renders as `MISSING` in bold.
- `Last Activated`: most recent timestamp in activation-log.jsonl for this name; `never` if no entries.
- `Status`: one of `used` (≥1 activation in last 30d), `unused` (never activated), `stale` (activations exist but none in last 30d).

**Sort order**: skills section sorted by name ASC; powers section sorted by name ASC; Staleness section groups by status.

**How updated**:
- Phase A refreshes the inventory after every Phase C safe-creation, Phase E pruning action, or manual install/uninstall Richard performs.
- Richard can trigger an ad-hoc refresh by asking the agent to "refresh skills inventory" — the agent walks ~/.kiro/skills/ and ~/.kiro/powers/installed/ and rewrites the file.
- The inventory is never silently regenerated on a schedule. Anti-goal.

**Freshness verification**: on read, the agent computes the sha256 of the current filesystem state (concatenated file paths + frontmatter) and compares against the inventory's recorded input-state hash. Mismatch → agent re-runs Phase A before trusting the inventory.

### Activation log — `~/shared/context/skills-powers/activation-log.jsonl`

Line-delimited JSON, append-only. Same shape as the audit's `execution.log`. Survives sessions. Portable: no dependency on DuckDB or Kiro-specific infrastructure.

```
{"event":"activated","kind":"skill","name":"bridge-sync","request_summary":"sync body to agent-bridge","session_id":"sess-2026-04-22-01","ts":"2026-04-22T01:05:00-07:00"}
{"event":"activated","kind":"power","name":"aws-agentcore","request_summary":"deploy bedrock agent","session_id":"sess-2026-04-22-01","ts":"2026-04-22T01:10:00-07:00"}
{"event":"created","kind":"skill","name":"wbr-callouts","session_id":"sess-2026-04-22-01","ts":"2026-04-22T01:20:00-07:00","overlap_check_ref":"~/.kiro/skills/wbr-callouts/overlap-check.json"}
{"event":"missed","kind":"skill","name":"wiki-search","request_summary":"find docs on testing approach","reason":"keyword match not activated before response draft","session_id":"sess-2026-04-22-02","ts":"2026-04-22T02:15:00-07:00"}
{"event":"pruned","kind":"skill","name":"obsolete-skill","archive_path":"~/shared/wiki/agent-created/archive/skills-powers-pruned-2026-05-15/obsolete-skill/","session_id":"sess-2026-05-15-01","ts":"2026-05-15T03:00:00-07:00"}
```

**Event types**:
- `activated`: a skill or power was successfully invoked via `discloseContext` or `kiroPowers activate`.
- `created`: a new skill or power was written to disk and passed Phase C activation-validate.
- `missed`: the missed-skill detector flagged a gap — a response was drafted where a skill's keywords matched the request but the skill was never activated. Logged so the adoption habit is measurable.
- `pruned`: the skill or power was archived and deleted per Phase E.

**Required fields**: `event`, `kind`, `name`, `session_id`, `ts`. Event-specific fields:
- `activated`, `missed`: `request_summary` (short free-text, ≤120 chars).
- `created`: `overlap_check_ref` (path to the archived overlap-check evidence).
- `missed`: `reason` (short free-text explaining why the detector flagged it).
- `pruned`: `archive_path` (where the file was moved before deletion).

**No updates, no deletes**: this file is append-only. If an entry is wrong, a subsequent correction entry is appended with `event: "correction"` and a reference to the erroneous entry's timestamp. Same idempotence guarantee as the audit's `execution.log`.

### Overlap-check evidence record — per-creation JSON

Captured once per safe-creation in Phase C.1, archived alongside the new asset as `~/.kiro/skills/{name}/overlap-check.json` (or `~/.kiro/powers/installed/{name}/overlap-check.json`).

```json
{
  "created_at": "2026-04-22T01:20:00-07:00",
  "proposed_asset": {
    "kind": "skill",
    "name": "wbr-callouts",
    "description": "Full WBR callout pipeline for weekly business review. Covers all 10 markets..."
  },
  "searched_mechanisms": {
    "skills": ["bridge-sync", "charts", "coach", "cr-tagging", "sharepoint-sync", "wiki-audit", "wiki-search", "wiki-write"],
    "powers": ["power-builder", "aws-agentcore", "flow-gen"],
    "subagents": ["rw-trainer", "karpathy", "callout-analyst", "callout-writer", "callout-reviewer", "wiki-writer", "wiki-researcher", "wiki-editor", "wiki-critic", "wiki-librarian", "wiki-concierge"],
    "hooks": ["wbr-callouts.kiro.hook", "am-auto.kiro.hook", "eod.kiro.hook", "..."],
    "steering": ["soul.md", "richard-writing-style.md", "callout-principles.md", "..."],
    "organs": ["body.md", "brain.md", "memory.md", "..."]
  },
  "overlap_candidates": [
    {
      "asset_path": "~/.kiro/hooks/wbr-callouts.kiro.hook",
      "overlap_type": "functional",
      "overlap_score": 0.75,
      "rationale": "Existing hook already fires on WBR prompt. Proposed skill would orchestrate the analyst-writer-reviewer pipeline but the hook just triggers it."
    },
    {
      "asset_path": "~/.kiro/agents/callout-writer.json",
      "overlap_type": "functional",
      "overlap_score": 0.45,
      "rationale": "Writer subagent is called by the pipeline; skill is an orchestrator, not a wrapper."
    }
  ],
  "decision": "CREATE_NEW",
  "decision_rationale": "The existing wbr-callouts.kiro.hook is an event trigger; the proposed skill is a keyword-activated orchestrator for a multi-market pipeline that the hook does not cover (hook only fires on one specific prompt pattern). The three callout subagents are orchestrated by this skill — the skill's legitimate value-add per R10.5 is the sequencing.",
  "alternatives_considered": [
    {"option": "extend wbr-callouts.kiro.hook", "rejected_because": "hook event trigger is narrow; skill needs keyword match across more prompt shapes"},
    {"option": "no skill, keep ad-hoc", "rejected_because": "pipeline is invoked weekly × 10 markets = 40+ activations/quarter; leverage ranking places it top-5"}
  ],
  "reviewed_by_richard": true,
  "reviewed_at": "2026-04-22T01:18:00-07:00"
}
```

**Purpose**: NO-ORPHAN-CREATION property evidence. Every new skill or power carries its own justification forever. If a future audit asks "why does this skill exist alongside that subagent?", the overlap-check answers it without requiring Richard's memory.

**Required fields**: `created_at`, `proposed_asset.{kind,name,description}`, `searched_mechanisms` (all 6 kinds present as lists), `overlap_candidates` (possibly empty), `decision` (one of `CREATE_NEW`, `EXTEND_EXISTING`, `REJECT`), `decision_rationale`, `alternatives_considered`, `reviewed_by_richard` (must be `true` for CREATE_NEW to proceed), `reviewed_at`.

**Lifetime**: archived with the new asset, persists as long as the skill/power exists. On Phase E prune, the overlap-check.json is archived alongside the SKILL.md/POWER.md in the dated archive directory.

---

## Routing Decision Tree

Every proposed workflow walks this tree in order. First matching branch wins. The tree's first question is deliberately *should this exist at all?* — applying soul.md #3 (subtraction before addition) inside the design of the adoption system itself.

Workflow dependency: Phase B intake. Future workflow: L3-L5 agentic orchestration will consume the same tree when autonomous agents propose encoding their own repeated subtasks.

```
  START: workflow W with description D, trigger T, frequency F, data sensitivity S,
         sharability H (cross-team? team-only? personal?)
       |
       v
  0. REJECT gate (subtraction before addition)
     Does W happen < 1x/month AND the cost of re-explaining it each time is low?
     OR is W already captured by memory + a standard prompt?
     OR is W a one-off that won't recur?
       YES -> terminate: REJECT, rationale "keep in head, no codification needed".
              Do NOT create anything.
       NO  -> continue.
       |
       v
  1. EXTEND-EXISTING gate (no duplication)
     Does any existing skill, power, subagent, hook, steering, or organ
     already cover W's intent ≥ 75%?
       YES -> terminate: EXTEND_EXISTING(asset_path).
              Record overlap in overlap-check.json; edit the existing
              asset rather than create a new one.
       NO  -> continue.
       |
       v
  2. EVENT vs KEYWORD split
     Is W triggered by an IDE / filesystem / scheduled EVENT (file save,
     prompt submit, time)?
       YES -> branch to mechanism=HOOK. go to H-branch below.
       NO  -> continue (trigger is keyword-based or manual).
       |
       v
  3. IDENTITY / ALWAYS-APPLICABLE gate (avoid steering bloat)
     Does W define a rule the agent must follow in EVERY interaction
     (identity, writing style, environment guardrails)?
       YES -> branch to mechanism=STEERING (auto-include). go to S-branch.
             Scrutiny applies — steering is an every-chat tax.
       NO  -> continue.
       |
       v
  4. SPECIALIST DOMAIN gate (subagent territory)
     Does W require deep specialist knowledge + autonomous execution,
     AND is the specialist domain narrow (career coaching, wiki writing,
     callout review)?
       YES -> branch to mechanism=SUBAGENT. go to A-branch.
              Note: skills that orchestrate multiple subagents are OK (R10.5).
       NO  -> continue.
       |
       v
  5. PERSISTENT STATE gate (organ territory)
     Is W about reading or maintaining shared persistent state
     (relationship graph, tool inventory, OP2 targets)?
       YES -> branch to mechanism=ORGAN. go to O-branch.
       NO  -> continue.
       |
       v
  6. MCP-BUNDLE gate (power territory)
     Does W require a specific MCP server OR a curated knowledge base
     that an agent needs to activate on-demand across many sessions?
       YES -> branch to mechanism=POWER. go to P-branch.
       NO  -> continue.
       |
       v
  7. Default: SKILL
     W is a keyword-activated workflow that loads specialist instructions
     into context on-demand, NOT requiring an MCP bundle or a subagent
     handoff, NOT always-applicable.
       -> terminate: mechanism=SKILL. go to K-branch.
```

### Mechanism sub-trees (terminal branches)

**REJECT-branch**:
- Terminate. Do not create any file. Record rationale in the routing-decision record for future reference ("we considered codifying W but rejected per subtraction-before-addition").

**EXTEND-branch**:
- Identify the existing asset path.
- Open it for edit.
- Append the new instruction as an additive section; do not rewrite existing logic.
- Record in overlap-check.json (still required — evidence of the decision).

**H-branch (HOOK)**:
- Event type is one of: `fileEdited`, `fileCreated`, `fileDeleted`, `userTriggered`, `promptSubmit`, `agentStop`, `preToolUse`, `postToolUse`, `preTaskExecution`, `postTaskExecution`.
- Scrutinize `promptSubmit` hooks (every-chat tax per audit H3). Unconditional output → reject or require conditional-output pattern.
- Hook JSON goes to `~/.kiro/hooks/{name}.kiro.hook`.

**S-branch (STEERING)**:
- Inclusion mode: `always` ONLY if the rule truly applies every chat. Otherwise `manual` or `fileMatch` (conditional).
- Steering goes to `~/.kiro/steering/{name}.md`.
- Forbidden: do not create an always-auto-loaded steering file that path-references a candidate-deletion target (audit R5.6 compatibility).

**A-branch (SUBAGENT)**:
- Subagent JSON goes to `~/.kiro/agents/{name}.json`.
- Applies domain-specific system prompt and tool allowlist.

**O-branch (ORGAN)**:
- Markdown organ goes to `~/shared/context/body/{name}.md` or a sub-layer.
- Organs carry state; they are the data, not the behavior.

**P-branch (POWER)**:
- Two sub-types:
  - *Guided MCP*: includes `mcp.json` — adds tools to the session via MCP. Use when the workflow requires tools not already in Kiro's core.
  - *Knowledge Base*: POWER.md + optional steering files — pure documentation loaded via `kiroPowers activate`.
- Power goes to `~/.kiro/powers/installed/{name}/POWER.md`.

**K-branch (SKILL)**:
- SKILL.md goes to `~/.kiro/skills/{name}/SKILL.md`.
- Frontmatter includes trigger list embedded in description ("Triggers on {kw1}, {kw2}, ...").
- Activated via `discloseContext` when the agent keyword-matches the request.

### Worked examples (one per terminal leaf — R2.5)

**Example 1 — REJECT**: Richard asks, "Should we codify the workflow I did last Tuesday where I opened three tabs and compared three documents?"
- Tree: step 0 asks "does this happen < 1x/month, or is it a one-off?" → one-off. **Terminate: REJECT.**
- Rationale: encoding a one-off three-tab comparison workflow adds surface without recurring payoff. Keep in head.

**Example 2 — EXTEND-EXISTING**: Richard asks, "I want a workflow that pushes new body organs to the agent-bridge repo."
- Tree: step 1 finds `bridge-sync` skill (K-S1) with description covering "Sync files to shared/context/ directory, push to agent-bridge". Overlap > 75%. **Terminate: EXTEND_EXISTING(bridge-sync).**
- Rationale: already exists. Edit bridge-sync to cover any newly-named organs if needed; do not create a parallel skill.

**Example 3 — HOOK**: Richard asks, "I want something that fires when a file in ~/shared/context/intake/ is created and parses it for wiki candidates."
- Tree: step 2 sees `fileCreated` event trigger. **Terminate: HOOK.**
- Rationale: event-triggered, not keyword-triggered. Lives in `~/.kiro/hooks/intake-parse.kiro.hook`.

**Example 4 — STEERING**: Richard asks, "I want the agent to always use bullet points for multi-item responses."
- Tree: step 3 identifies identity/always-applicable rule. **Terminate: STEERING (auto-include).**
- Rationale: every-chat rule about response shape. Belongs in soul.md or a style steering file. Note: this already exists; example is illustrative for the decision tree.

**Example 5 — SUBAGENT**: Richard asks, "I want a specialist agent that does deep career coaching using the full body system."
- Tree: step 4 identifies specialist domain (career coaching) requiring deep context + autonomous execution. **Terminate: SUBAGENT.**
- Rationale: narrow domain, deep specialist, requires its own tool allowlist. Lives as `rw-trainer` subagent (already exists; example is illustrative).

**Example 6 — ORGAN**: Richard asks, "I want a single place to track OP2 targets per market that the agent can read during callout writing."
- Tree: step 5 identifies persistent shared state. **Terminate: ORGAN.** (Actually: already covered by `ps.targets` DuckDB table + `ps-performance-schema.md` reference doc, so would likely hit EXTEND-EXISTING at step 1; example is illustrative of the ORGAN leaf.)

**Example 7 — POWER**: Richard asks, "I want to onboard Bedrock AgentCore with its own tools and docs."
- Tree: step 6 identifies MCP-bundle need. **Terminate: POWER (Guided MCP).**
- Rationale: includes `mcp.json` with agentcore-mcp-server. Lives as `aws-agentcore` power (already installed; example is illustrative).

**Example 8 — SKILL**: Richard asks, "When I say 'write a WBR callout', I want the full analyst-writer-reviewer pipeline to fire."
- Tree: steps 0-6 all pass through. Step 7 default: SKILL. **Terminate: SKILL.**
- Rationale: keyword-activated ("write a WBR callout", "WBR", "callout"), orchestrates multiple subagents in sequence (the callout pipeline), no MCP bundle needed, not every-chat. Lives as `wbr-callouts` skill.

---

## Sensitive-Data Classification Rules

Four tiers. Each tier has a concrete source-of-truth and a concrete path-allowlist. The validator enforces the allowlist at creation time and any time a skill/power is edited.

Workflow dependency: Phase C safe-creation uses these rules to validate the declared class. Future workflow: L5 autonomous agents that propose new skills on their own must classify before the create step will proceed.

### Tier definitions

**Public** — already published externally or intended for public consumption.
- Sources: wiki articles under `~/shared/wiki/agent-created/` published to w.amazon.com or external; public AWS/Kiro documentation; open-source references; power-builder content.
- Examples: power-builder POWER.md, aws-agentcore POWER.md, flow-gen POWER.md (all already installed as Public).
- Path allowlist for files declared Public: any path, including `~/.kiro/skills/`, `~/.kiro/powers/installed/`, `~/shared/wiki/**`, and anything synced to the agent-bridge repo.

**Amazon_Internal** — non-confidential Amazon information used in routine work.
- Sources: internal Amazon processes, tool guides, generic workflow patterns that happen to involve Amazon tools (Asana, DuckDB, Outlook MCP).
- Examples: bridge-sync (syncs files but contains no Amazon-confidential content itself), charts (visualization patterns), wiki-audit (generic audit procedure).
- Path allowlist: any path on the user's local/SSH machines. **May NOT be synced to agent-bridge if the body content it touches is higher-sensitivity** — classification is about what the skill *handles*, not where the skill itself lives. Re-check at sync time by looking at each file's declared class.

**Amazon_Confidential** — business-sensitive Amazon data.
- Sources: PS performance metrics (regs, spend, CPA from `ps.v_weekly`, `ps.v_daily`), forecasts, OP2 targets, pre-publication strategic artifacts, internal stakeholder reviews, competitive intelligence, pre-launch test results.
- Examples: any skill that reads/writes state files under `Kiro-Drive/state-files/`, forecasting skills, Testing Approach drafts before publication.
- Path allowlist: `~/.kiro/skills/`, `~/.kiro/powers/installed/`, `~/shared/context/` (local only), SharePoint `Kiro-Drive/` (authenticated). **Forbidden paths**: anything synced to the agent-bridge GitHub repo. Check bridge-sync.md's sync list at create time; the current sync targets are `~/shared/context/body/`, `~/shared/context/protocols/`, `~/.kiro/steering/` — skills declared Amazon_Confidential must not live in those paths if the paths sync to agent-bridge.
- Note: `~/.kiro/skills/` itself is not currently synced to agent-bridge, so Amazon_Confidential skills may live there. If bridge-sync.md's sync list ever expands to include skills, the adoption system's validator re-checks.

**Personal_PII** — identifying information for Amazon employees, external colleagues, or stakeholders.
- Sources: names / emails / aliases of people (memory.md relationship graph, amazon-politics.md stakeholder maps, 1:1 meeting notes, performance feedback, compensation discussions, HR content).
- Examples: coach skill (touches 1:1 prep, relationship dynamics); any skill that reads memory.md or amazon-politics.md.
- Path allowlist: `~/.kiro/skills/`, `~/.kiro/powers/installed/`, `~/shared/context/` (local only), SharePoint `Kiro-Drive/personal-body/`. **Forbidden paths**: agent-bridge repo, any path in a GitHub repo, any path with external sync. Personal_PII skills effectively never leave the local machine. Even among `~/shared/context/`, Personal_PII skills should prefer `~/shared/context/body/` (not synced) over `~/shared/context/protocols/` (synced to agent-bridge per bridge-sync.md).
- If unsure whether a name/alias is Personal_PII: it is. Default up, not down.

### Default handling when missing (R3.5)

If a skill or power has no declared `sensitive_data_class`, the validator treats it as `Amazon_Confidential` for all path-allowlist checks. The validator also flags the skill as `needs_classification: true` in a re-validation queue so Richard can declare explicitly. Missing class is a warning, not an outright error — legacy skills created before this spec won't have the field and must be classified during first contact.

### Path-allowlist enforcement algorithm

Given a skill S with declared sensitivity C and an output-write path P:
1. Look up allowlist(C) from the table above.
2. Check P ⊆ allowlist(C). If not, emit validation error.
3. For declared-class Amazon_Confidential and Personal_PII, additionally check: does P lie inside any directory currently synced to agent-bridge (per bridge-sync.md's sync list)? If yes, emit sync-violation error.
4. The sync list is read at validation time, not cached. If bridge-sync.md's sync targets change, the next validator run catches any newly-illegal paths.

---

## Portability Tier Rules

Two tiers. The difference is whether a new AI on a different platform can understand and execute the skill/power using only the file text + other Cold_Start_Safe files.

Workflow dependency: Phase C safe-creation applies these rules. Future workflow: L5 platform-migration scenarios depend on Cold_Start_Safe skills surviving the move intact; Platform_Bound skills migrate but will need platform-specific rewriting of their declared dependencies.

### Cold_Start_Safe indicators (what makes a skill portable)

A skill is Cold_Start_Safe when **all** of the following hold:
- Instructions describe workflow *intent* in plain language ("sync body files to the remote repo and run a verification step"), not tool-specific procedure ("call `mcp_ai_community_slack_mcp_post_message` with channel_id=...").
- No direct references to Kiro-specific tool names (`discloseContext`, `invokeSubAgent`, `kiroPowers`).
- No direct references to specific MCP tool function names (`mcp_*`).
- No direct references to specific subagent names (`rw-trainer`, `karpathy`, `wiki-writer`).
- No direct references to specific hook IDs (`am-auto.kiro.hook`, `eod.kiro.hook`).
- No direct references to specific DuckDB tables unless the reference includes enough context for a new agent to understand what the table contains (table schema described, not just table name).
- No hard-coded file paths that only exist in this environment (unless the path represents a portable convention, like `~/shared/context/body/`).

### Platform_Bound indicators (what makes a skill non-portable)

A skill is Platform_Bound when **any** of the following hold:
- Body contains MCP tool function names (`mcp_ai_community_slack_mcp_search`, `mcp_hedy_GetSessionDetails`, etc.).
- Body contains subagent names (`invokeSubAgent(name="rw-trainer")`).
- Body contains hook IDs (`am-auto.kiro.hook`).
- Body specifies DuckDB table names without schema context (`SELECT * FROM asana.asana_tasks` with no explanation of what `asana_tasks` is).
- Body hard-codes paths outside the portable convention.

### Consistency check (R4.5 / PORTABILITY-CONSISTENCY property)

The portability validator runs these checks:
1. Parse the skill body.
2. Scan for Platform_Bound indicator tokens:
   - Regex `mcp_[a-z_]+` for MCP tool names.
   - Regex `invokeSubAgent\(.*name=['"]([a-z\-]+)['"]` for subagent references.
   - Regex `[a-z\-]+\.kiro\.hook` for hook IDs.
   - Regex `kiroPowers\s*\(` or `discloseContext\s*\(` for Kiro API names.
3. If declared `Cold_Start_Safe` AND any token found → validator flags `portability_inconsistency: true` and lists the offending tokens. Skill must either:
   - Be downgraded to `Platform_Bound` and the tokens documented in `platform_bound_dependencies`, OR
   - Be rewritten to remove the tokens.
4. If declared `Platform_Bound`, validator verifies `platform_bound_dependencies` is non-empty and each declared dependency appears in the body (soft check; warning, not error, since some dependencies are declared at the semantic level not the syntactic level).

### Examples

**Cold_Start_Safe skill** (hypothetical): "Format a WBR callout from weekly metrics. Input: market, registrations, spend, CPA, previous-week deltas, and an OP2 target. Output: three paragraphs in the Amazon 1-2-3 style (what happened, why it happened, what we're doing). Check the numbers sum correctly before finalizing."
- Portable: any agent on any platform can execute with text input.

**Platform_Bound skill** (bridge-sync, actual): "Run `scripts/sync.sh` to commit and push changes to the agent-bridge GitHub repository."
- Platform-bound: references a specific script at a specific path. Declared dependencies list `{kind: script, id: "scripts/sync.sh"}`.

---

## Inventory File Spec

### Location (audit-referrer-aware)

`~/shared/context/skills-powers/inventory.md`.

**Why this path**:
- `~/shared/context/` is inside the audit's active-referrer scope (R2.8 of audit). Any path-reference from the inventory to a skill/power counts as an active referrer, saving the skill/power from ORPHAN classification in a future audit.
- Not inside `.kiro/specs/**` (which the audit classifies as `documentation` and does not count as active).
- Not inside `.kiro/steering/` (which would auto-load the file every chat — the anti-pattern we are explicitly avoiding per Interlock point 4).

Workflow dependency: Phase A inventory refresh writes this file. Every Phase B / C / E phase reads it to orient. Future workflow: L5 autonomous skill-proposal agents read this file before proposing new skills to avoid duplicates.

### Format

Markdown with three sections: Skills table, Powers table, Staleness summary. See §Data Model → Inventory for the column layout.

### How updated

Three update paths:
1. **Phase C auto-update**: whenever a new skill or power is created and passes activation-validate, the inventory is re-rendered in the same session.
2. **Phase E auto-update**: whenever a skill or power is pruned, the inventory is re-rendered.
3. **Richard-triggered refresh**: Richard can ask "refresh skills inventory" and the agent re-walks the filesystem + re-reads the activation log and rewrites the file. Used when Richard manually installed/uninstalled a power or skill outside the adoption-system flow.

### Freshness verification

The inventory header records a sha256 of its input state:
```
**Input state hash**: sha256:abc123...
```

The hash is computed over: concatenation of `{filepath}\n{frontmatter-yaml}\n` for every SKILL.md and POWER.md, sorted by filepath. On read, the agent re-computes the hash against the current filesystem. Mismatch → agent runs Phase A before trusting the inventory's content.

No freshness hook, no scheduled refresh. Verification is on-demand by the consumer (another agent or a Phase B/C/E flow), matching the audit's principle of no recurring automation.

---

## Candidate Workflow Identification Method

Workflow dependency: one-shot initial identification, then reactive during Phase B as Richard proposes new workflows. Future workflow: L3 team-adoption workflows will use the same leverage-ranking formula to decide which team workflows are worth codifying.

### Source scan

Four input sources per R5.1:
1. **`~/shared/context/body/body.md`** — system map. Look for workflows named in the navigation layer that are currently handled manually each session.
2. **`~/shared/context/body/device.md`** — installed apps and tools. Look for tool-use patterns that recur (e.g., "every time I open Outlook I do X").
3. **Hook inventory** (`~/.kiro/hooks/*.kiro.hook`). Already-codified event-triggered workflows — if a hook covers it, the adoption system does NOT recommend a new skill (R5.4).
4. **Subagent inventory** (`~/.kiro/agents/*.json`). Already-codified specialist domains — if a subagent covers it, the adoption system does NOT recommend a new skill (R5.4).

Additional sources: `~/shared/context/intake/session-log.md` (recent session activity — what has Richard been repeatedly asking for?), DuckDB `main.project_timeline` (recurring activity signals).

### Leverage ranking formula

Per Richard's brain.md leverage framework:
- **Recurrence**: how often does the workflow happen? `R = activations_per_month` (estimated).
- **Explanation cost**: how expensive is re-explaining the workflow each time? `C = rough_minutes_to_re-explain`.
- **Artifact level**: which L1-L5 level does it produce? `L ∈ {1, 2, 3, 4, 5}` (higher = more strategic).
- **Leverage score**: `score = R × C × L`.

Higher score = higher priority for codification. Scores are ordinal only — they exist to sort, not to be trusted in absolute terms.

### Pilot cap (R5.6)

Top 3 candidates by leverage score get the pilot. Not top 10. Not all candidates. Three. Rationale in §Design Decisions.

### Candidate record shape

Each candidate is one row in a ranked list:

```json
{
  "rank": 1,
  "workflow_description": "Write a WBR callout pipeline end-to-end across 10 markets",
  "proposed_mechanism": "SKILL",
  "proposed_sensitivity": "Amazon_Confidential",
  "proposed_portability": "Platform_Bound",
  "proposed_trigger": "WBR, callout, weekly callout, market callout",
  "existing_asset_overlap": [{"path": "~/.kiro/hooks/wbr-callouts.kiro.hook", "overlap_type": "functional", "rationale": "hook fires on prompt; skill orchestrates pipeline"}],
  "duplicates_existing": false,
  "leverage_score": 4 * 30 * 3,
  "pilot": true
}
```

The ranked list goes in the initial build-out spec (downstream of this design). The list is NOT part of this adoption system's durable artifacts — it's a one-shot work product that seeds the pilot skills. After the pilot skills are built, the ranked list is archived.

---

## Adoption Habit Integration

R6.1-R6.2 require two behaviors: (1) activate a matching skill before responding, and (2) flag a missed opportunity after responding when a skill was not activated but should have been.

Workflow dependency: Phase D runs continuously during any chat session where skills are installed. Future workflow: L3 team-tooling adoption tracker consumes the `missed` events to compute adoption rate per skill per teammate.

### Keyword-activation heuristic (pre-response, R6.1)

Procedure the agent follows on every user request before drafting a response:

1. Parse the user request into a set of meaningful tokens (lowercase, strip punctuation, keep multi-word phrases).
2. For each installed skill S, parse S's frontmatter `description` and extract the trigger list (everything after "Triggers on " as comma-separated phrases).
3. For each installed power P, read the `keywords` frontmatter field (list of strings).
4. Compute `match(request, skill) = (|request_tokens ∩ trigger_tokens| ≥ 1)`. Simple substring / phrase match.
5. If any skill or power matches → call `discloseContext({name: skill.name})` or `kiroPowers({action: "activate", powerName: power.name})` before drafting the response.
6. Append one `{"event": "activated", ...}` line to activation-log.jsonl for each activation.

The match is conservative: one token / phrase match is enough. False positives (activating a skill that didn't end up being needed) cost a few KB of context. False negatives (missing a skill that should have fired) cost Richard re-explaining the workflow — the exact failure mode this adoption system exists to prevent.

### Missed-skill detection (post-draft, R6.2)

Procedure the agent follows after drafting a response but before sending:

1. Extract the response draft's content tokens (same normalization as request tokens).
2. For each installed skill S that was NOT activated in this response, recompute `match(draft, S)`.
3. If any non-activated skill matches the draft's content → append a "missed skill" note to the response: *"Note: I drafted this without activating the `{skill.name}` skill, which may have been relevant. Tell me if you'd like me to redo with the skill loaded."*
4. Append one `{"event": "missed", ...}` line to activation-log.jsonl.

The missed note is user-visible. It is the feedback loop that makes adoption measurable: if Richard sees the same missed skill flagged repeatedly across sessions, it means the keyword-match heuristic is under-matching that skill's trigger words and the trigger list needs expansion.

### Why keyword-match and not semantic-match

Simplicity and portability. Keyword matching works on any platform with any LLM. Semantic matching would require an embedding model, which introduces a platform dependency. Keyword matching errs toward over-activation (which is cheap) rather than over-missing (which is expensive).

---

## Safe-Creation Workflow

Workflow dependency: Phase C safe-creation procedure, invoked only when Phase B routing terminates at CREATE_NEW for SKILL / POWER. Future workflow: L5 autonomous agents proposing skills-of-their-own will follow the same steps.

Five sub-steps. Each is gated; a failure at any step stops the creation and leaves the filesystem in its pre-creation state.

### Step 1: Overlap check (R10.1-R10.2)

1. Enumerate existing assets:
   - Skills: `~/.kiro/skills/*/SKILL.md`
   - Powers: `~/.kiro/powers/installed/*/POWER.md`
   - Subagents: `~/.kiro/agents/*.json`
   - Hooks: `~/.kiro/hooks/*.kiro.hook`
   - Steering: `~/.kiro/steering/*.md`
   - Organs: `~/shared/context/body/*.md`
2. Extract each existing asset's description or first paragraph.
3. Compute overlap between the proposed asset's description and each existing description:
   - Keyword overlap (trigger tokens shared)
   - Semantic overlap (this is where a richer check matters — for the first version, use keyword overlap only; upgrade to semantic check later if false negatives accumulate).
4. For any existing asset with overlap ≥ 0.5 (keyword ratio), record in `overlap_candidates`.
5. Write overlap-check.json per the schema in §Data Model.

If ≥1 candidate has overlap ≥ 0.75 → default decision is `EXTEND_EXISTING`. Richard can override to `CREATE_NEW` with rationale. If all candidates < 0.5 → default decision is `CREATE_NEW` with no candidates listed.

### Step 2: Richard review gate (R7.2-R7.3)

Before any file write, present Richard with:
- The proposed SKILL.md or POWER.md full content.
- Declared `sensitive_data_class` + path-allowlist implications.
- Declared `portability_tier` + any flagged `platform_bound_dependencies`.
- Trigger keywords (for skills) or keywords field (for powers).
- The overlap-check.json summary (who was considered, why this asset is still new).

Richard replies: APPROVE, REVISE (with feedback), or REJECT. On APPROVE, set `reviewed_by_richard: true` and `reviewed_at` in the overlap-check.json. On REVISE, loop back to draft. On REJECT, terminate and do not write.

Per R7.4: if `sensitive_data_class ∈ {Amazon_Confidential, Personal_PII}`, Richard is additionally asked to confirm the declared write paths are not synced to agent-bridge. The validator has already checked this, but the human confirmation is the second fence.

### Step 3: File write

Write SKILL.md or POWER.md at the canonical path:
- Skill: `~/.kiro/skills/{name}/SKILL.md`
- Power: `~/.kiro/powers/installed/{name}/POWER.md` (plus optional `~/.kiro/powers/installed/{name}/mcp.json`)

Write the overlap-check.json alongside: `~/.kiro/skills/{name}/overlap-check.json`.

Set `created_at` and initial `last_validated` to the current ISO 8601 timestamp.

### Step 4: Activation validation (R7.6)

Actually call the activation tool against the new file:
- For a new skill: `discloseContext({name: new_skill_name})`. Success = tool returns without error.
- For a new power: `kiroPowers({action: "activate", powerName: new_power_name})`. Success = tool returns the power's overview / toolsByServer without error.

On failure, log the error and **delete the partially-created file**. The creation is NOT complete until activation succeeds.

On success, update `last_validated` timestamp to the current time.

### Step 5: Inventory + log update (R7.5)

1. Append a `{"event": "created", "kind": ..., "name": ..., "overlap_check_ref": ..., ...}` line to activation-log.jsonl.
2. Run Phase A inventory refresh, which re-renders inventory.md with the new row.

The creation is complete when all five steps have succeeded. Partial failure at any step: the filesystem is rolled back (no orphan files, no orphan log entries).

---

## Round-Trip File Format Property

Per R9 — file format is round-trip safe: parse → serialize → parse yields an equivalent AST.

Workflow dependency: any agent that reads and re-writes a SKILL.md or POWER.md (e.g., a future batch-edit for metadata migration) depends on round-trip correctness. Future workflow: L5 autonomous agents that edit their own skills need round-trip safety to avoid silent corruption.

### Grammar (YAML-subset for frontmatter + markdown body)

A SKILL.md or POWER.md has the structure:

```
FILE       := FRONTMATTER BODY
FRONTMATTER := "---\n" YAML_SUBSET "---\n"
YAML_SUBSET := KEY_VALUE ("\n" KEY_VALUE)*
KEY_VALUE  := KEY ":" (SCALAR | LIST | OBJECT)
KEY        := [a-z_][a-z0-9_]*
SCALAR     := (QUOTED_STRING | UNQUOTED_STRING | NUMBER | BOOLEAN | NULL | ISO8601_DATETIME)
LIST       := "\n" ("  - " SCALAR)+
OBJECT     := "\n" ("  " KEY ":" SCALAR)+
BODY       := <arbitrary markdown content, including code blocks, tables, etc.>
```

**Restrictions on the YAML subset** (for portability — a parser in any language can implement it):
- No anchors / aliases / tags.
- No multi-document streams.
- Scalar strings use double-quotes for any value containing `:`, `#`, or starting with `{`, `[`, `!`, `&`, `*`, or a digit.
- Lists use `-` indented by 2 spaces.
- Nested objects indent by 2 spaces.
- Date-time values are ISO 8601 with explicit timezone (never naive).

**Required frontmatter keys** (validator enforces presence):
- Skill: `name`, `description`, `sensitive_data_class`, `portability_tier`, `created_at`, `last_validated`.
- Power: `name`, `displayName`, `description`, `keywords`, `author`, `sensitive_data_class`, `portability_tier`, `created_at`, `last_validated`.
- Conditionally required: `platform_bound_dependencies` iff `portability_tier == Platform_Bound`. `mcp_servers_declared` iff the power bundles an `mcp.json`.

### Parse function behavior

`parse(file_contents: string) -> ParseResult`:
- `ParseResult = Success(frontmatter: object, body: string) | Error(violation: string)`.
- Reads everything between two `---` markers as YAML frontmatter; everything after the second marker is body.
- On invalid YAML: return `Error("invalid YAML at line N: <message>")`.
- On missing required key: return `Error("missing required key: <key>")`.
- On unknown-value-for-enum (sensitive_data_class not in the four tiers, portability_tier not in two tiers): return `Error("invalid enum value: <key>=<value>, expected one of <allowed>")`.
- On inconsistency (Cold_Start_Safe body contains Platform_Bound tokens, or Platform_Bound with empty platform_bound_dependencies): return `Error("portability inconsistency: <description>")`.

Error-on-malformed is the requirement. The parser NEVER silently rewrites.

### Serialize function behavior

`serialize(frontmatter: object, body: string) -> string`:
- Emits `---\n` marker.
- Emits each key in a canonical order (the order listed in §Data Model — name first, then description, then metadata fields, then timestamps). Canonical order makes the serialize function deterministic (same input → same output byte-for-byte).
- Quoting rule: strings containing `:` or starting with a reserved YAML character are double-quoted; others are unquoted. This is the only normalization.
- Emits `---\n` closing marker.
- Appends body verbatim.

### Round-trip property (tested in §Correctness Properties)

For any file that the parser accepts as valid, the round-trip property is:

```
parse(serialize(parse(f))) == parse(f)
```

This is an *AST* equality check, not a byte equality. Two valid files with different cosmetic whitespace parse to the same AST; their second serialization produces canonical form; re-parsing yields the same AST. Byte-equality is not required.

For files the parser rejects (`Error` variant), the property does not apply — error messages are not expected to round-trip.

---

## Pruning Review Design

Workflow dependency: Phase E runs on Richard's manual invocation. Future workflow: L3 team-adoption pruning will follow the same procedure applied to team-shared skills when team skill sharing is implemented.

### Cadence

**Human-triggered, not scheduled.** Monthly is the suggested cadence (matching soul.md's existing quarterly/monthly review rhythms) but the scheduler does not exist. Richard invokes the review when he feels the skill inventory is bloated, or when the inventory's Staleness section shows ≥3 stale skills.

No hook, no cron, no scheduled agent. This directly matches the audit's anti-goal #1 and the Interplay point 4 / audit R5.6.

### Procedure

1. **Compute stale set**: for each skill/power in the inventory, compute last activation from activation-log.jsonl. If last activation is > 30 days ago OR there is no activation record AND `created_at` is > 14 days ago (R6.5 threshold for never-activated), the skill is *stale*.
2. **Present to Richard**: the agent lists stale skills with columns: name, last_activated, days_stale, sensitivity, portability, recommendation (default DELETE).
3. **Richard decides per row**: APPROVE, KEEP (with rationale — skill kept despite stale, rationale recorded in inventory notes), or DEFER (re-check next cycle).
4. **For each APPROVE row**:
   - **Archive**: copy the entire skill directory (SKILL.md + overlap-check.json + any auxiliary files) to `~/shared/wiki/agent-created/archive/skills-powers-pruned-{YYYY-MM-DD}/{name}/`.
   - **Verify archive exists**: stat check. If archive write failed, STOP — do not delete.
   - **Delete**: remove the original directory from `~/.kiro/skills/{name}/` or `~/.kiro/powers/installed/{name}/`.
   - **Append to log**: `{"event": "pruned", "kind": ..., "name": ..., "archive_path": ..., ...}`.
5. **Refresh inventory**: Phase A re-renders inventory.md.
6. **Commit**: git commit the archive + deletions with message `prune: skills-powers review {date}`.

### Archive path

`~/shared/wiki/agent-created/archive/skills-powers-pruned-{YYYY-MM-DD}/`

Same parent directory as the audit's spec-archive path (`~/shared/wiki/agent-created/archive/system-subtraction-audit-{date}/`). Consistent archive convention across both specs means a single `ls` in `archive/` shows every governance action in chronological order.

### Archive-before-delete ordering (R8.3, ARCHIVE-BEFORE-DELETE property)

The order is always: **archive write → verify → delete**. Never the reverse. On any failure in the write or verify step, the delete does not proceed. This is the same guarantee as the audit's MERGE stops-on-conflict behavior — no step proceeds when a prerequisite failed.

---

## Anti-Goals (explicit)

1. **Not a recurring hook or dashboard.** Matches audit anti-goals #1, #3, #4. No scheduled refresh, no inventory dashboard UI, no daily stale-skill summary email. Every refresh and review is reactive / human-triggered.

2. **Not a new always-loaded steering file.** No `.kiro/steering/skills-powers.md` that auto-loads rules on every chat. The inventory is consulted on-demand by the agent's lookup flow. Per audit R5.6, adding auto-loaded steering that path-references candidate skills would make them UNCLEAR in future audits — exactly the coupling we avoid.

3. **Not a duplicate of the subtraction audit.** The audit is a one-shot cleanup of existing surface. This spec is the positive governance loop for new workflows going forward. Different phase-cadence, different outputs. This spec references the audit's patterns and artifact shapes so they interoperate, but it doesn't re-audit.

4. **Not a wrapper-skill generator** (R10.4). Skills whose only function is to invoke a single existing subagent are rejected at creation. The subagent is the correct mechanism; a skill around it is surface area with no payoff. The NO-WRAPPER-SKILL property catches this.

5. **Not an extraction system** for hook-content-into-skills. Hooks that fire on events are better as hooks. The adoption system does not recommend "let's take this hook's logic and put it in a skill" as a default. Event-triggered workflows stay in hooks per the routing tree's step 2.

6. **Not autonomous skill creation.** No agent creates skills on its own. Every new skill/power walks through Phase C including Richard's review gate. The REVIEW-GATE-SCHEMA property encodes this: no file write without a review record.

7. **Not a tooling project.** No scripts committed to `~/shared/tools/`. The routing tree, classification rules, and file-format grammar are all described in this design doc and consumed by the agent reading it. If the agent needs to validate a skill file, it reads §Round-Trip File Format and applies the grammar. No compiled validator, no shared library.

8. **Not a platform-portability solution on its own.** The adoption system defines the portability tier and enforces consistency, but actually making a platform move work is the job of bridge-sync + a future migration spec. The adoption system ensures skills *can* be migrated; it doesn't perform the migration.

9. **Not a complexity product.** Same as the audit's anti-goal #9. The adoption system's own artifacts (inventory.md, activation-log.jsonl) are durable but cheap: two files, both append-only-or-rewritable-from-filesystem-state. The overlap-check.json records are archived with the skills they justify. No sprawling scaffolding.

---

## Design Decisions and Rationale

### Why inventory lives in `~/shared/context/skills-powers/` not `.kiro/specs/skills-powers-adoption/`

Per the audit's R2.8 scope + R2.3 / R2.4 documentation-referrer classification. `.kiro/specs/**` is documentation in the audit's graph — references from there are `documentation` type and do NOT save a skill from ORPHAN status. For the inventory's path-reference to each skill to count as an *active* referrer (and save real skills from being flagged as orphans in a future audit), the inventory must live in an active scope path. `~/shared/context/` is active scope. That's why the inventory lives there.

### Why no auto-loaded steering for the adoption system

Per audit R5.6. Any always-loaded steering that path-references candidate-deletion files becomes UNCLEAR-default-KEEP in the audit's classification. If I created a `.kiro/steering/skills-adoption.md` auto-loaded file that listed every skill by path, every skill would become UNCLEAR-default-KEEP in future audits. The coupling is wrong. Instead, skills are referenced from inventory.md (in active scope, so they count as referrers) but not via auto-loaded steering.

### Why pilot capped at 3 (R5.6)

soul.md #3 (subtraction before addition) + soul.md #6 (reduce decisions, not options). Proposing 10 candidate skills at once forces Richard to decide among 10 things. Proposing the top 3 gives him one obvious next step, with the rest queued for later cycles. The cost of waiting is low (the other 7 candidates accumulate in the pipeline); the benefit is Richard actually ships the pilot instead of stalling on choice overload.

### Why activation-log is JSONL not DuckDB

Portability. The sibling audit's `execution.log` is also JSONL for the same reason. A DuckDB table would require the DuckDB MCP to be live during logging — a cold-start / platform-move scenario would lose the log. JSONL in `~/shared/context/` survives a platform move intact and is parseable with any language's standard library.

### Why the routing tree has a REJECT branch first

Applying soul.md #3 inside the design of the adoption system itself. If the first question is "skill or power?" rather than "should this exist?", the tree defaults to *something*. Defaulting to something creates surface area by default. Defaulting to REJECT forces justification. Subtraction-before-addition as a tree topology, not just as a rationale.

### Why keyword-match and not semantic-match for activation

Simplicity + portability. Keyword match runs on any platform with any LLM. Semantic match would require an embedding model, introducing a platform dependency. False positives (over-activating) are cheap; false negatives (missing activations) are the exact failure mode this adoption system exists to prevent. Err toward over-activation.

### Why Amazon_Confidential defaults when sensitivity is missing (R3.5)

Fail-safe default. The alternative (treating missing as Public) would let legacy skills silently get synced to agent-bridge on first edit. Defaulting up means the validator blocks a sync that would have been wrong, and Richard classifies explicitly.

### Why the overlap-check.json is archived forever (not just during creation)

Evidence of the creation decision survives as long as the skill does. If a future audit asks "why does `wbr-callouts` skill exist when `callout-writer` subagent also exists?", the overlap-check.json is the answer. This is the same pattern as the audit's `kill-list.md` being archived — decisions are documents, not just transient state.

### Why activation-validate happens after Richard's review, not before

Richard's review gates the *intent* of the skill (is this the right skill, right sensitivity, right scope). Activation-validate checks the *mechanics* (does the file parse, does the tool accept it). Checking mechanics before Richard approves is wasted effort if Richard rejects. Intent-first, mechanics-second.

### What we almost added and cut

Three candidate mechanisms were drafted and cut because they failed the audit's workflow tests:

- **Recurring "stale skill" digest hook**: would fire weekly and post stale skills to Slack. Cut — violates audit anti-goal #1 (not an ongoing service); the inventory's Staleness section already surfaces this, and pruning is human-triggered.
- **Skills-powers dashboard HTML**: would render the inventory as an interactive dashboard. Cut — violates audit anti-goal #3 (flat markdown preferred); nothing the dashboard would show isn't already in inventory.md.
- **Auto-loaded `.kiro/steering/skill-index.md`**: would list every skill on every chat so the agent always "remembers". Cut — violates Interplay point 4 / audit R5.6; the keyword-match heuristic achieves the same outcome without the every-chat tax.

### Why this spec carries the same Mario-and-Peter fingerprints as the audit

Same two-philosophy design. Mario-rigor for the rules (sensitivity tiers, portability grammar, round-trip property) because getting these wrong corrupts skill files silently. Peter-scrappiness for the pilot (cap at 3, human-triggered review, on-demand inventory refresh) because skill creation is iterative and the first pilot is never the final set. The long-term structural target matches the audit's open question #7: skills-and-powers *are* the extension-first pattern. The adoption system is the governance that gets us there.

---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

PBT is appropriate for this feature because the core governance behaviors are pure functions over structured inputs: parse/serialize for file format, route(workflow) → mechanism for the decision tree, validator(skill) → errors for metadata checks, stale-detector(log, clock) → flagged-set for pruning. Each has a wide input space where random generation reveals edge cases (whitespace, unicode, empty lists, boundary timestamps). The AWS-like integration concerns (does bridge-sync actually push to GitHub) are out of scope — those are covered by bridge-sync.md's own integration tests, not this spec.

### Property 1: Round-trip file format

*For any* valid SKILL.md or POWER.md file accepted by the parser, parse(serialize(parse(file))) yields a parsed AST equal to parse(file).

**Validates: Requirements 9.3**

### Property 2: Error-on-malformed file

*For any* malformed SKILL.md or POWER.md file (invalid YAML, missing required key, invalid enum value, or portability inconsistency), the parser returns a descriptive Error record and does NOT silently rewrite the file or return a partial AST.

**Validates: Requirements 9.4, 9.5**

### Property 3: Sensitivity path consistency

*For any* skill or power S with declared `sensitive_data_class ∈ {Amazon_Confidential, Personal_PII}`, all of S's output write paths lie inside the allowlist for that sensitivity class, AND none of those paths lie inside any directory currently synced to the agent-bridge repository. *For any* S with missing sensitivity class, validation treats S as Amazon_Confidential and enforces the same restriction.

**Validates: Requirements 3.1, 3.2, 3.3, 3.5, 3.6, 7.4**

### Property 4: Portability consistency

*For any* skill or power S with declared `portability_tier == Cold_Start_Safe`, S's body does not contain Platform_Bound indicator tokens (MCP tool function names matching `mcp_[a-z_]+`, subagent invocation patterns matching `invokeSubAgent\(.*name=...`, hook IDs matching `[a-z\-]+\.kiro\.hook`, or Kiro-API names like `discloseContext` / `kiroPowers`). *For any* S with `portability_tier == Platform_Bound`, the `platform_bound_dependencies` frontmatter list is non-empty.

**Validates: Requirements 4.4, 4.5**

### Property 5: Inventory freshness (bijection)

*For any* filesystem state of `~/.kiro/skills/` and `~/.kiro/powers/installed/` and *for any* sequence of create / prune / manual-install / manual-uninstall operations applied to that state, after each operation there is a bijection between (a) the set of SKILL.md + POWER.md files on disk and (b) the set of rows in inventory.md — every file has exactly one row and every row corresponds to exactly one file.

**Validates: Requirements 1.1, 1.2, 1.3, 7.5, 8.2**

### Property 6: Stale detection

*For any* activation-log.jsonl state and *for any* clock time T and threshold D (in days), the stale-detector returns exactly the set of skills and powers where (no activation event within [T-D, T]) OR (no activation events at all AND created_at < T-14days). The detector is deterministic: same inputs → same output set.

**Validates: Requirements 1.5, 6.5, 8.1, 8.4**

### Property 7: Routing totality

*For any* well-formed workflow descriptor D (contains description, trigger-type, frequency-estimate, sensitivity, sharability), the routing function route(D) returns exactly one of the terminal values {REJECT, EXTEND_EXISTING, HOOK, STEERING, SUBAGENT, ORGAN, POWER, SKILL} paired with a non-empty rationale string. The function is deterministic and total: no input yields undefined output.

**Validates: Requirements 2.1, 2.3, 2.4**

### Property 8: Overlap surfacing

*For any* proposed workflow W and *for any* existing-mechanism-set M, if any asset m ∈ M has description-keyword-overlap with W ≥ 0.5, the overlap-check record produced by Phase C.1 lists m in `overlap_candidates` with its overlap score, rationale, and overlap_type.

**Validates: Requirements 2.6, 10.1, 10.2**

### Property 9: No-orphan-creation

*For any* new skill or power file written to disk by the adoption system, there exists an accompanying overlap-check.json in the same directory with `reviewed_by_richard == true` and a `decision` value of either `CREATE_NEW` or `EXTEND_EXISTING`, and the timestamp on the overlap-check.json is strictly earlier than the file's created_at. Put differently: no SKILL.md or POWER.md is ever created without pre-existing evidence of the creation decision.

**Validates: Requirements 7.1, 7.2, 10.3**

### Property 10: No-wrapper-skill

*For any* proposed skill S whose body consists solely of a single `invokeSubAgent` call with one subagent name and no additional orchestration, the wrapper-detector rejects S with the reason "wrapper skill — use the subagent directly (R10.4)". *For any* proposed skill S whose body orchestrates ≥2 distinct subagent calls or ≥2 distinct MCP tool calls in a documented sequence, the detector accepts S (R10.5).

**Validates: Requirements 10.4, 10.5**

### Property 11: Review-gate schema

*For any* validated skill or power file (newly created or existing), the required metadata fields for its kind are all present: `name`, `description`, `sensitive_data_class`, `portability_tier`, `created_at`, `last_validated` for skills; plus `displayName`, `keywords`, `author` for powers; plus `platform_bound_dependencies` (non-empty) iff `portability_tier == Platform_Bound`.

**Validates: Requirements 7.3, 9.5**

### Property 12: Logging invariant

*For any* single activation call (successful `discloseContext` or `kiroPowers activate`), exactly one line is appended to activation-log.jsonl. That line is valid JSON and contains all required fields: `event`, `kind`, `name`, `session_id`, `ts`. For `activated` and `missed` events, `request_summary` is also present. For `created` events, `overlap_check_ref` is present. For `pruned` events, `archive_path` is present.

**Validates: Requirements 6.3, 6.4**

### Property 13: Keyword activation

*For any* user request R containing tokens that match any installed skill's trigger list OR any installed power's keywords, either (a) the matching skill/power is activated (entry appears in activation-log.jsonl with event=activated and session_id == current session) before the response is drafted, OR (b) a missed-skill note appears in the response AND a corresponding `missed` entry appears in activation-log.jsonl.

**Validates: Requirements 6.1, 6.2**

### Property 14: Archive before delete

*For any* skill or power S approved for pruning in Phase E, the archive write at `~/shared/wiki/agent-created/archive/skills-powers-pruned-{date}/{name}/` completes and the archive file exists on disk **before** the original file at `~/.kiro/skills/{name}/` or `~/.kiro/powers/installed/{name}/` is deleted. If the archive write fails, the delete does not proceed.

**Validates: Requirements 8.3**

---

## Testing Strategy

Dual approach matching the sibling audit's pattern:

- **Unit tests**: specific examples, edge cases, error conditions. Focus on:
  - Individual decision-tree branches with specific workflow inputs (each of the 8 worked examples in §Routing Decision Tree becomes a unit test).
  - Specific malformed-file examples for parse error messages (empty file, frontmatter without closing `---`, missing required keys one at a time, each invalid enum value).
  - Integration between safe-creation phases (Step 1 → Step 2 → Step 3 → Step 4 → Step 5 under a happy-path example).
- **Property tests**: universal properties across all inputs. Configuration:
  - Library: pick a property-based testing library for the target language (the implementing spec downstream selects; likely `fast-check` for TypeScript or `hypothesis` for Python). Do NOT implement PBT from scratch.
  - Minimum 100 iterations per property test.
  - Tag each test with a comment referencing the design property. Tag format: `// Feature: skills-powers-adoption, Property {number}: {property_text}`.
  - Each Correctness Property above maps to exactly ONE property-based test; property reflection already consolidated the redundant ones.

### Per-property implementation notes

- **Property 1 (round-trip)**: generator produces valid frontmatter objects (random from the allowed enums, random ISO 8601 timestamps, random body strings including unicode / whitespace / code fences). Serialize → parse → compare ASTs.
- **Property 2 (error on malformed)**: generator produces intentionally malformed files — corrupted YAML, missing keys, invalid enum values. Assert parser returns `Error` with a descriptive message; assert no partial AST is returned.
- **Property 3 (sensitivity)**: generator produces (skill body, declared sensitivity, declared output paths, current agent-bridge sync list). Validate assertion: declared output paths ⊆ allowlist(sensitivity) AND if sensitivity ∈ restricted-set, output paths ∩ sync list == ∅.
- **Property 4 (portability)**: generator produces skill bodies with planted Platform_Bound tokens at varying densities. Assert the validator flags inconsistency iff `declared == Cold_Start_Safe` and any token present.
- **Property 5 (inventory bijection)**: generator produces a sequence of create/prune/install/uninstall operations. After each op, run inventory-render and assert bijection with filesystem.
- **Property 6 (stale)**: generator produces random activation logs + random clock times + random thresholds. Compare detector output to oracle (explicit set-comprehension over the log).
- **Property 7 (routing)**: generator produces well-formed workflow descriptors across the input space. Assert route() returns a terminal + non-empty rationale; assert determinism (run twice, equal output).
- **Property 8 (overlap)**: generator produces (proposed description, existing-mechanism-set with planted overlaps at varied ratios). Assert overlap_check surfaces any existing asset with overlap ≥ 0.5.
- **Property 9 (no orphan)**: simulate create calls; assert for each written file, overlap-check.json exists, is reviewed, and predates created_at.
- **Property 10 (no wrapper)**: generator produces skill body templates varying the count of distinct tool/subagent invocations. Assert wrapper_detector rejects count==1 (single subagent) and accepts count≥2.
- **Property 11 (schema)**: generator produces skill/power frontmatter with random subsets of fields present. Assert validator pass iff all required fields present.
- **Property 12 (logging)**: generator produces sequences of activation calls; assert log length and per-entry schema after each.
- **Property 13 (keyword)**: generator produces (request-text, skill-set with trigger lists). Assert either activation happens pre-draft OR missed note appears post-draft.
- **Property 14 (archive-before-delete)**: generator produces prune approvals; assert filesystem ordering — archive file exists before original deletion.

### What is NOT tested by PBT

- Actual GitHub push behavior of bridge-sync — integration boundary, covered by bridge-sync's own tests.
- Actual DuckDB query responses — integration boundary.
- Visual rendering of inventory.md — rendering is mechanical markdown serialization, covered by Property 5.
- Richard's actual approve/reject decisions in Phase C — human in the loop, not a function.

---

## Portability Check

A new AI on a different platform reads this design. Can it re-execute the governance procedures?

- **Phase A (inventory refresh)** needs: filesystem listing, file reading, YAML parse, markdown write. Standard tools.
- **Phase B (routing)** needs: read a workflow description, walk the decision tree, emit a routing-decision record. Pure logic, no tool dependencies.
- **Phase C (safe-creation)** needs:
  - Overlap check: search across filesystem paths — standard.
  - Richard review: human-in-the-loop, same on any platform.
  - File write: standard.
  - Activation-validate: `discloseContext` and `kiroPowers activate` are Kiro-specific. On a different platform, this step is replaced by the platform's equivalent skill/capability activation mechanism. The adoption system as described is abstract enough — "call the activation mechanism, assert success" — to migrate.
  - Inventory + log update: standard.
- **Phase D (activation logging)** needs: append to a JSONL file. Standard.
- **Phase E (pruning)** needs: human review, archive-then-delete, same on any platform.

The YAML-subset grammar for SKILL.md and POWER.md is explicit. The routing tree is deterministic. The classification rules have concrete path-allowlists. The worked examples are concrete enough for a different-platform agent to verify its understanding against.

Kiro-specific tool names (`discloseContext`, `kiroPowers`) appear in Property 13's text but are called out as "the platform's equivalent activation mechanism" — the property itself is platform-agnostic (keyword-match request → activation happens). Confirmed portable.
