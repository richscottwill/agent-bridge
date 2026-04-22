# Design Document: Skills & Powers Adoption

## Overview

This design produces one human-facing reference system and two machine-facing artifacts. The human-facing deliverables are a routing decision tree (for new-workflow intake) and a skills-powers inventory (for "what do I already have"). The machine-facing artifacts are a skill/power metadata schema extension (so files self-declare sensitivity and portability) and an append-only activation log (so staleness is computable). Everything else is working state or documentation.

**Reading order for the agent executing this adoption system**: Interplay with system-subtraction-audit → Architecture → Data Model → Routing Decision Tree → Sensitive-Data Classification Rules → Portability Tier Rules → Inventory File Spec → Pilot: activation of the 9 already-installed skills → Adoption Habit Integration → Safe-Creation Workflow → Round-Trip File Format → Pruning Review → Anti-Goals → Design Decisions → Correctness Properties → Error Handling → Testing Strategy.

**Design stance**: This is governance, not a product. The adoption system does not deploy. It defines rules, a decision tree, a metadata schema, and a lightweight inventory + log. New skills and powers are built downstream by separate specs that consume these rules. If the rules need to change, a future spec edits this file; the rules themselves do not ship as code.

**Why so thin on "implementation"**: The 10 requirements already specify the *what*. This design specifies the *how* with the same granularity as the sibling `system-subtraction-audit/design.md` — data-model fields, decision-tree branches, and worked examples — so a different-platform agent could re-execute the governance procedures without this spec's supporting context.

### Revision History

2026-04-22 — revision pass applied after stress-test against real on-disk structures (9 installed SKILL.md files + 4 installed POWER.md files + kill-list findings from system-subtraction-audit). Six findings addressed, each *subtracting* design surface:

- **F1 (BROKEN)** — portability validator becomes advisory, not blocking. A blocking regex-scan would fail every one of the 9 existing skills on day 1 (charts references `scripts/generate.sh`; wiki-write references pipeline subagents; etc.). The day-1 mass-flag is the structural-tax failure the audit exists to catch.
- **F2 (BROKEN)** — schema gains a `status` enum (`legacy` | `current` | `retired`). Zero of 13 installed assets have the new fields. Without status-gating, P5 (bijection) and P11 (schema) would contradict on day 1. Touch-it-classify-it migration, no flag day.
- **F3 (BROKEN)** — inventory is orphan-by-design. The earlier claim that it counted as an *active* referrer under audit R2.8 was wrong (R2.8 is about referrer liveness, not directory location). Nothing auto-loads the inventory; ORPHAN status is accepted deliberately. Alternatives (auto-loaded steering, promptSubmit hook, evidence-only script) each violate an audit rule or anti-goal.
- **F4 (BROKEN)** — missed-skill detector DROPPED ENTIRELY. No platform event between response draft and response send; any detector would be a convention ("remember to remember"), the exact failure skills were meant to eliminate. Property 13 is removed, the detector subsection removed, `missed` event type removed. Feedback-driven `missed-by-feedback` replaces it.
- **F5 (WEAK)** — pilot is activation of the 9 already-installed skills, not construction of 3 new ones. Corpus exists; Richard has never meaningfully invoked it. Addition before subtraction is the anti-pattern.
- **F6 (WEAK)** — routing tree gains step 0.5 (non-Kiro mechanism gate). The `dashboard-server.kiro.hook` kill-list entry (orphan hook duplicating `.bashrc`) is the canonical case the gate prevents.

Properties post-revision: 15 (Property 13 dropped, not retired-in-place; remaining properties renumbered so there are no gaps).

### Interplay with system-subtraction-audit

This spec is the positive-construction complement to `system-subtraction-audit`. The audit applies *subtraction-before-addition* (soul.md #3) to the existing system. This adoption system applies the same principle to every *new* workflow Richard would otherwise bolt on. Specifically:

1. **Every mechanism this spec introduces passes the audit's own classification tests.** The audit's `Current Usage Test` and `Future Workflow Test` (requirements R5.4-5.5 of the audit) apply here too. Each component in the Architecture section declares its `Workflow dependency:` and `Future workflow:` labels. Components that fail both tests are METAPHOR-ONLY and are cut. See §Design Decisions → "What we almost added and cut".

2. **We reuse the audit's artifact patterns, not parallel ones.**
   - Row IDs for inventory rows: `K-{kind}{N}` where `kind` ∈ {S (skill), P (power)} and `N` is 1-indexed within kind. Matches the audit's `{L}-{A}{N}` grammar.
   - Format split: one human-facing markdown (`inventory.md`) + one machine-facing JSONL (`activation-log.jsonl`) + transient JSON intermediates during creation (`overlap-check.json`). Same convention as the audit's `kill-list.md` + `execution.log` + intermediate JSONs.
   - Archive pattern: any retired skill/power file moves to `~/shared/wiki/agent-created/archive/skills-powers-pruned-{YYYY-MM-DD}/` before deletion, same shape as the audit's spec-archive path.

3. **Search scope and referrer classification are respected — skills and powers are ORPHAN-by-design.** The audit treats `.kiro/specs/**` as `documentation` referrers, not load-bearing. **Skills and powers will appear as ORPHAN in future audits because the activation mechanism (`discloseContext`, `kiroPowers activate`) is not a path referrer.** This is structurally correct — extension-loaded modules *should* look orphan in a dependency graph. The adoption system's inventory + activation-log are the governance layer that saves them from DELETE classification in any future audit. Earlier drafts claimed that placing the inventory at `~/shared/context/skills-powers/` its path-references to each skill would count as *active* referrers per audit R2.8. That claim was wrong: R2.8 is about *referrer liveness* (does anything actively load this file), not about directory location. The inventory itself also registers as ORPHAN in the audit graph — nothing auto-loads it — and we accept that deliberately rather than manufacture liveness via auto-loaded steering (which would trigger audit R5.6 UNCLEAR coupling) or a `promptSubmit` hook (the exact recurring-service pattern the audit's anti-goal #1 forbids). See §Inventory File Spec → "Location (orphan-by-design)" and §Anti-Goals #10.

4. **No auto-loaded steering.** The audit's R5.6 warns: any always-loaded steering that path-references a candidate file becomes UNCLEAR with default KEEP — which means a bad-taste steering file can permanently save orphan content. This adoption system deliberately does **not** create a `.kiro/steering/skills-powers.md` auto-loaded layer. The inventory is consulted on-demand by the agent's natural lookup flow (when the agent is about to draft a skill or hit a keyword-match opportunity), never via steering frontmatter.

5. **This spec is the extension-first answer to the audit's open question #7** ("restructure surviving files as extension-loaded modules per the pi / OpenClaw architecture pattern"). Skills via `discloseContext` and Powers via `kiroPowers activate` are already that pattern — extension-loaded, keyword-gated, on-demand. The adoption system's job is to route *new* workflows to this extension-loaded mechanism by default rather than adding more always-loaded steering or more hook surface.

6. **The routing tree has an explicit reject-for-subtraction branch and a non-Kiro-mechanism gate before any Kiro mechanism-selection branches.** The first question the tree asks is not "skill or power?" — it is "should this workflow be codified at all?" If the workflow is one-off, low-leverage, or already covered by memory + a simple prompt, the tree terminates at REJECT. The second question is "does an existing non-Kiro mechanism (shell alias, .bashrc, cron, git hook, IDE feature) already handle this?" — if yes, REJECT rather than build a Kiro duplicate. This applies soul.md #3 (subtraction before addition) inside the design of the adoption system itself. The kill-list's `dashboard-server.kiro.hook` DELETE candidate — a hook that duplicated .bashrc auto-restart logic — is the reference case this gate is designed to prevent.

---

## Architecture

The adoption system is an ongoing **governance loop**, not a one-time audit. Six phases run on different cadences: a one-shot activation-baseline scan captures starting-line usage of the 13 installed assets (Phase 0); inventory refresh is reactive (triggered by create/prune events); routing intake is reactive (triggered by Richard proposing a new workflow); safe-creation is reactive (triggered by routing deciding CREATE); activation logging is continuous (every skill/power invocation writes one line); and pruning review is human-triggered (Richard invokes it monthly or ad-hoc).

```
  Phase 0: ACTIVATION BASELINE (one-shot — runs before Phase A the first time)
      |
      | inputs: ~/shared/context/intake/session-log.md (historical sessions)
      |         filesystem state of ~/.kiro/skills/, ~/.kiro/powers/installed/
      | procedure: scan session log for invocation patterns per skill/power name
      | produces: seed rows in activation-log.jsonl with event="baseline"
      |           per-asset "first observed activation" and "most recent activation"
      v

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

  Phase C: SAFE-CREATION (reactive — only if Phase B terminates at CREATE-new, OR when a legacy asset is edited)
      |
      | inputs: routing-decision.json (new asset) OR existing legacy asset being edited
      | procedure:
      |   C1. overlap-check against existing mechanisms (new assets only)
      |   C2. Richard review of proposed content + declared metadata
      |   C3. write file (new asset) OR classify-then-write (legacy asset)
      |   C4. activation-validate (call discloseContext / kiroPowers activate)
      |   C5. update inventory.md + append creation/classification entry to activation-log.jsonl
      | produces: new SKILL.md or POWER.md, OR reclassified legacy asset with extended frontmatter
      |           overlap-check.json (new assets only; archived with the asset as evidence)
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

**Why these six and not more**: an earlier sketch had a seventh phase for "periodic keyword-match audit" — walk every drafted response and flag missed-skill opportunities. That phase is cut. No post-draft / pre-send event exists in the platform, so any implementation would be a convention the agent is asked to remember to execute — exactly the "remember to remember" failure mode that skills were designed to eliminate. Missed-skill detection is not machine-enforced; gap data comes from Richard flagging after the fact, logged as `missed-by-feedback` (see §Adoption Habit Integration, §Design Decisions → "Why missed-skill detection was cut", §Anti-Goals #10).

**Why it's six phases and not one "always-on adoption service"**: the audit's anti-goal #1 ("not an ongoing audit service") applies here. A recurring hook that checks for stale skills every day would itself be new surface area. Richard invokes pruning when the inventory feels bloated; the activation log captures data continuously because logging one line is cheap; everything else is reactive to Richard's intent. Phase 0 is one-shot and never runs again — once the baseline is in the log it's historical.

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

Extended frontmatter required by this adoption system **for `status: current` assets** (new skills created after this spec, or legacy skills reclassified at next edit):

```yaml
---
name: bridge-sync
description: "Sync files to shared/context/... Triggers on sync to git, bridge sync, portable body, agent bridge."
status: current                           # one of: legacy | current | retired
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
- `status` (enum, required for current/retired; implicit for legacy): `legacy` | `current` | `retired`. See §Schema status rules below.
- `sensitive_data_class` (enum, required for `status: current`): see §Sensitive-Data Classification Rules. Not required for `status: legacy`.
- `portability_tier` (enum, required for `status: current`): `Cold_Start_Safe` or `Platform_Bound`. See §Portability Tier Rules. Not required for `status: legacy`.
- `platform_bound_dependencies` (list, conditionally required for current): required iff `portability_tier == Platform_Bound`. Each entry has `{kind, id}` where `kind` is one of the enumerated kinds. Informational — not resolved at runtime, but parsed by the portability validator to confirm the file's internal consistency.
- `owner_agent` (string, nullable, optional for current): if this skill's logic is owned by a specialist agent (e.g., `wiki-writer`, `rw-trainer`, `karpathy`), name them. Null when no specialist owns the skill.
- `created_at` (ISO 8601 datetime with TZ, required for current): immutable. Written by Phase C safe-creation. Unknown for legacy assets until reclassification — left blank on legacy rows.
- `last_validated` (ISO 8601 datetime with TZ, required for current): updated by Phase C.4 (activation-validate) and by any explicit re-validation. Stale `last_validated` (> 90 days) is a signal for the portability validator to re-check but not itself a pruning trigger.

### Schema status rules (legacy / current / retired)

Three statuses:

- **`legacy`** — SKILL.md or POWER.md exists on disk with the original, minimal frontmatter only (skills: `{name, description}`; powers: `{name, displayName, description, keywords, author}`). No `sensitive_data_class`, `portability_tier`, `created_at`, or `last_validated` required. **Inventoried, activatable, exempt from schema validation** until the file is next edited. All 9 installed skills and 4 installed powers are `legacy` as of this spec's first run.
- **`current`** — SKILL.md or POWER.md has the full extended frontmatter above. New assets created via Phase C are born `current`. Legacy assets become `current` when they are next edited for any reason (see migration rule below).
- **`retired`** — asset has been pruned via Phase E. Archived to `~/shared/wiki/agent-created/archive/skills-powers-pruned-{date}/{name}/`. Not present on disk at `~/.kiro/skills/` or `~/.kiro/powers/installed/`. Retained in the inventory's historical section for one full pruning cycle then dropped.

**Touch-it-classify-it migration rule**: when a legacy skill or power is edited for any reason (bug fix, trigger-list update, description tweak), the edit is not saved to disk until the extended fields have been added and the asset's status flipped to `current`. Richard reviews the classification inline with the edit. There is no forced flag-day migration of all 13 assets at once — the subtraction audit has taught us that forced flag-day migrations produce abandoned fields. Classification happens naturally on the turn Richard touches the file.

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

Extended frontmatter required by this adoption system **for `status: current` powers**:

```yaml
---
name: "power-builder"
displayName: "Power Builder"
description: "..."
keywords: ["kiro power", "power builder", ...]
author: "Kiro Team"
status: current
sensitive_data_class: Public              # same enum as skills
portability_tier: Cold_Start_Safe         # same enum as skills
platform_bound_dependencies: []           # required iff Platform_Bound
mcp_servers_declared:                     # mirrors mcp.json — redundant but keeps POWER.md self-describing
  - "power-builder"
created_at: "2026-01-15T00:00:00-08:00"
last_validated: "2026-04-22T01:00:00-07:00"
---
```

**New fields**: `status`, `sensitive_data_class`, `portability_tier`, `platform_bound_dependencies`, `mcp_servers_declared`, `created_at`, `last_validated`. Same semantics as the skill fields. Same legacy/current/retired semantics apply — all 4 installed powers are `legacy` until their next edit.

**Note on `keywords`**: powers already declare `keywords` in frontmatter — the adoption system's keyword-activation heuristic uses this list directly for powers (same way it parses the trigger list from skill descriptions). Powers do not need an additional trigger field.


### Inventory file — `~/shared/context/skills-powers/inventory.md`

**Location**: `~/shared/context/skills-powers/inventory.md`. This is inside the `~/shared/context/` tree — a stable location that survives sessions and platform moves — but it is **orphan-by-design in the audit's referrer graph**. See §Inventory File Spec → "Location (orphan-by-design)" for the rationale.

**Shape**: single markdown file, one table per kind, sorted by kind then by name. The `Status` column is prominent so Richard can see at a glance which assets are legacy (unclassified), current (classified), and retired.

```markdown
# Skills & Powers Inventory

**Last updated**: 2026-04-22T01:00:00-07:00
**Activation log**: ~/shared/context/skills-powers/activation-log.jsonl

## Skills (~/.kiro/skills/)

| Row ID | Name | Status | Triggers | Sensitivity | Portability | Last Activated | Usage |
|--------|------|--------|----------|-------------|-------------|----------------|-------|
| K-S1 | bridge-sync | legacy | sync to git, bridge sync, portable body, agent bridge | — | — | 2026-04-20 | used |
| K-S2 | charts | legacy | chart, dashboard, visualize, show dashboard | — | — | 2026-04-18 | used |
| K-S3 | coach | legacy | coaching, career, 1:1 prep, retrospective, growth, annual review | — | — | never | unused |
| K-S4 | cr-tagging | legacy | (invoke-on-CR; no keyword triggers) | — | — | never | unused |
| K-S5 | sharepoint-sync | legacy | sync to SharePoint, SharePoint sync, upload to SharePoint | — | — | never | unused |
| K-S6 | wbr-callouts | legacy | WBR, callout, weekly callout, market callout | — | — | never | unused |
| K-S7 | wiki-audit | legacy | audit wiki, stale docs, which docs are stale, wiki quality | — | — | never | unused |
| K-S8 | wiki-search | legacy | search wiki, find doc, do we have a doc on, wiki lookup | — | — | never | unused |
| K-S9 | wiki-write | legacy | write wiki, document, wiki article, what should we document | — | — | never | unused |

## Powers (~/.kiro/powers/installed/)

| Row ID | Name | Status | Type | Sensitivity | Portability | Last Activated | Usage |
|--------|------|--------|------|-------------|-------------|----------------|-------|
| K-P1 | aws-agentcore | legacy | Guided MCP | — | — | never | unused |
| K-P2 | flow-gen | legacy | Knowledge Base | — | — | never | unused |
| K-P3 | hedy | legacy | Guided MCP | — | — | never | unused |
| K-P4 | power-builder | legacy | Knowledge Base | — | — | never | unused |

## Staleness

- **Unused (never activated)**: K-S3, K-S4, K-S5, K-S6, K-S7, K-S8, K-S9, K-P1, K-P2, K-P3, K-P4
- **Stale (activations exist but none in last 30 days)**: (none observed at baseline)
- **Candidates for next pruning review**: surfaced at 30-day threshold; no action taken at baseline
```

**Columns**:
- `Row ID`: `K-S{N}` for skills, `K-P{N}` for powers, 1-indexed within kind. Stable within a given inventory rendering; may shift on re-render. The inventory header includes the sha256 of the rendering's input state so shifts are detectable.
- `Name`: from frontmatter.
- `Status`: one of `legacy`, `current`, `retired`. For legacy rows, Sensitivity and Portability render as em-dash (`—`) rather than `MISSING`, because the missing fields are expected for legacy assets, not a validation failure.
- `Triggers` (skills) / `Type` (powers): trigger keywords for skills; `Guided MCP` or `Knowledge Base` for powers (derived from presence of `mcp.json`).
- `Sensitivity`, `Portability`: from frontmatter. For `status: current` rows, required; missing → renders as **`MISSING`** in bold. For `status: legacy` rows, rendered as `—`.
- `Last Activated`: most recent timestamp in activation-log.jsonl for this name; `never` if no entries.
- `Usage`: one of `used` (≥1 activation in last 30d), `unused` (never activated), `stale` (activations exist but none in last 30d).

**Sort order**: skills section sorted by name ASC; powers section sorted by name ASC; Staleness section groups by status.

**How updated**:
- Phase A refreshes the inventory after every Phase C safe-creation or classification, Phase E pruning action, or manual install/uninstall Richard performs.
- Richard can trigger an ad-hoc refresh by asking the agent to "refresh skills inventory" — the agent walks ~/.kiro/skills/ and ~/.kiro/powers/installed/ and rewrites the file.
- The inventory is never silently regenerated on a schedule. Anti-goal.

**Freshness verification**: on read, the agent computes the sha256 of the current filesystem state (concatenated file paths + frontmatter) and compares against the inventory's recorded input-state hash. Mismatch → agent re-runs Phase A before trusting the inventory.

### Activation log — `~/shared/context/skills-powers/activation-log.jsonl`

Line-delimited JSON, append-only. Same shape as the audit's `execution.log`. Survives sessions. Portable: no dependency on DuckDB or Kiro-specific infrastructure.

```
{"event":"baseline","kind":"skill","name":"bridge-sync","first_observed":"2026-03-14T...","last_observed":"2026-04-20T...","session_id":"sess-2026-04-22-baseline","ts":"2026-04-22T00:59:00-07:00"}
{"event":"activated","kind":"skill","name":"bridge-sync","request_summary":"sync body to agent-bridge","session_id":"sess-2026-04-22-01","ts":"2026-04-22T01:05:00-07:00"}
{"event":"activated","kind":"power","name":"aws-agentcore","request_summary":"deploy bedrock agent","session_id":"sess-2026-04-22-01","ts":"2026-04-22T01:10:00-07:00"}
{"event":"created","kind":"skill","name":"some-new-skill","session_id":"sess-2026-04-22-01","ts":"2026-04-22T01:20:00-07:00","overlap_check_ref":"~/.kiro/skills/some-new-skill/overlap-check.json"}
{"event":"pruned","kind":"skill","name":"obsolete-skill","archive_path":"~/shared/wiki/agent-created/archive/skills-powers-pruned-2026-05-15/obsolete-skill/","session_id":"sess-2026-05-15-01","ts":"2026-05-15T03:00:00-07:00"}
```

**Event types**:
- `baseline`: one row per installed asset, written by Phase 0. Records `first_observed` and `last_observed` from historical session-log scan. Replaced by subsequent `activated` events; purely informational.
- `activated`: a skill or power was successfully invoked via `discloseContext` or `kiroPowers activate`. The pre-draft activation path (agent checks inventory on reading a user request, calls `discloseContext` or `kiroPowers activate` before responding when a keyword matches) is the sole source of `activated` events.
- `created`: a new skill or power was written to disk and passed Phase C activation-validate. Also used when a legacy asset is reclassified to `current` via touch-it-classify-it — event subtype is `classified` in that case.
- `pruned`: the skill or power was archived and deleted per Phase E.
- `missed-by-feedback`: Richard told the agent after the fact that it should have activated a skill/power but did not. **This is the only gap-data event.** It is never auto-generated — it is appended only when Richard explicitly flags a miss during or after a session. The row records the skill/power name, Richard's free-text feedback (≤200 chars), and the session id and timestamp. There is no automated pre-send detection — see §Adoption Habit Integration and §Design Decisions → "Why missed-skill detection was cut".
- `correction`: errata for a prior row. Appended (not mutated) with a reference to the erroneous entry's timestamp.

**Required fields**: `event`, `kind`, `name`, `session_id`, `ts`. Event-specific fields:
- `baseline`: `first_observed`, `last_observed` (both optional — null if no historical activation).
- `activated`: `request_summary` (short free-text, ≤120 chars).
- `created`: `overlap_check_ref` (path to the archived overlap-check evidence).
- `pruned`: `archive_path` (where the file was moved before deletion).
- `missed-by-feedback`: `feedback_text` (Richard's free-text reason, ≤200 chars). No automatic detection; only present when Richard explicitly flags the miss.

**No updates, no deletes**: this file is append-only. If an entry is wrong, a subsequent correction entry is appended with `event: "correction"` and a reference to the erroneous entry's timestamp. Same idempotence guarantee as the audit's `execution.log`.

### Overlap-check evidence record — per-creation JSON

Captured once per safe-creation in Phase C.1, archived alongside the new asset as `~/.kiro/skills/{name}/overlap-check.json` (or `~/.kiro/powers/installed/{name}/overlap-check.json`). Only applies to **new** assets — not to legacy reclassification. Legacy assets already exist; the overlap-check would be retrospective and has no decision to document.

```json
{
  "created_at": "2026-04-22T01:20:00-07:00",
  "proposed_asset": {
    "kind": "skill",
    "name": "some-new-skill",
    "description": "..."
  },
  "searched_mechanisms": {
    "skills": ["bridge-sync", "charts", "coach", "cr-tagging", "sharepoint-sync", "wbr-callouts", "wiki-audit", "wiki-search", "wiki-write"],
    "powers": ["aws-agentcore", "flow-gen", "hedy", "power-builder"],
    "subagents": ["rw-trainer", "karpathy", "wiki-writer", "wiki-researcher", "wiki-editor", "wiki-critic", "wiki-librarian", "wiki-concierge", "callout-analyst", "callout-writer", "callout-reviewer", "..."],
    "hooks": ["am-auto.kiro.hook", "eod.kiro.hook", "..."],
    "steering": ["soul.md", "richard-writing-style.md", "callout-principles.md", "..."],
    "organs": ["body.md", "brain.md", "memory.md", "..."],
    "non_kiro_mechanisms_considered": ["bashrc", "cron", "git hooks", "IDE features"]
  },
  "overlap_candidates": [
    {
      "asset_path": "~/.kiro/hooks/some-existing-hook.kiro.hook",
      "overlap_type": "functional",
      "overlap_score": 0.55,
      "rationale": "Partial overlap on trigger; proposed skill is keyword-activated rather than event-triggered."
    }
  ],
  "decision": "CREATE_NEW",
  "decision_rationale": "...",
  "alternatives_considered": [
    {"option": "extend existing hook", "rejected_because": "..."},
    {"option": "no skill, keep ad-hoc", "rejected_because": "..."}
  ],
  "reviewed_by_richard": true,
  "reviewed_at": "2026-04-22T01:18:00-07:00"
}
```

**Purpose**: NO-ORPHAN-CREATION property evidence. Every new skill or power carries its own justification forever. If a future audit asks "why does this skill exist alongside that subagent?", the overlap-check answers it without requiring Richard's memory.

**Required fields**: `created_at`, `proposed_asset.{kind,name,description}`, `searched_mechanisms` (all 6 Kiro kinds present as lists, plus `non_kiro_mechanisms_considered` per revision 6), `overlap_candidates` (possibly empty), `decision` (one of `CREATE_NEW`, `EXTEND_EXISTING`, `REJECT`), `decision_rationale`, `alternatives_considered`, `reviewed_by_richard` (must be `true` for CREATE_NEW to proceed), `reviewed_at`.

**Lifetime**: archived with the new asset, persists as long as the skill/power exists. On Phase E prune, the overlap-check.json is archived alongside the SKILL.md/POWER.md in the dated archive directory.

---

## Routing Decision Tree

Every proposed workflow walks this tree in order. First matching branch wins. The tree's first two questions are deliberately *should this exist at all?* and *does something outside Kiro already handle it?* — applying soul.md #3 (subtraction before addition) inside the design of the adoption system itself.

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
  0.5. NON-KIRO GATE (external mechanism already handles it)
       Does an existing non-Kiro mechanism already handle W? (shell alias,
       .bashrc, cron, git hook, OS-level shortcut, IDE feature, team tool)
         YES -> terminate: REJECT, rationale names the existing mechanism
                (e.g., "already handled by .bashrc auto-restart").
                Do NOT create anything inside Kiro's layers.
         NO  -> continue to step 1.
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
- Terminate. Do not create any file. Record rationale in the routing-decision record for future reference ("we considered codifying W but rejected per subtraction-before-addition" OR "we considered codifying W but rejected because non-Kiro mechanism X already handles it").

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

**Example 0 — REJECT via non-Kiro mechanism (step 0.5)**: Richard asks, "I want a hook that auto-restarts the dashboard server when the port goes down."
- Tree: step 0 passes — the workflow is high-frequency (dashboards crash occasionally) and has non-trivial re-explanation cost. Step 0.5 catches it: `.bashrc` already runs the dashboard server on shell init. **Terminate: REJECT**, rationale "covered by non-Kiro mechanism; codifying as Kiro surface would be duplication across tool boundaries".
- **Reference case**: this is the exact case the audit caught with `dashboard-server.kiro.hook` on the kill-list — an orphan hook, 11 lines, duplicated by `.bashrc`. Without step 0.5, the workflow would have passed into mechanism-selection and landed on HOOK. With step 0.5, it terminates early. This is the instinct-to-reach-for-Kiro-when-the-OS-already-does-it case the gate is designed to catch.

**Example 1 — REJECT (step 0)**: Richard asks, "Should we codify the workflow I did last Tuesday where I opened three tabs and compared three documents?"
- Tree: step 0 asks "does this happen < 1x/month, or is it a one-off?" → one-off. **Terminate: REJECT.**
- Rationale: encoding a one-off three-tab comparison workflow adds surface without recurring payoff. Keep in head.

**Example 2 — EXTEND-EXISTING**: Richard asks, "I want a workflow that pushes new body organs to the agent-bridge repo."
- Tree: step 0 passes. Step 0.5 passes (no non-Kiro mechanism handles this). Step 1 finds `bridge-sync` skill (K-S1) with description covering "Sync files to shared/context/ directory, push to agent-bridge". Overlap > 75%. **Terminate: EXTEND_EXISTING(bridge-sync).**
- Rationale: already exists. Edit bridge-sync to cover any newly-named organs if needed; do not create a parallel skill.

**Example 3 — HOOK**: Richard asks, "I want something that fires when a file in ~/shared/context/intake/ is created and parses it for wiki candidates."
- Tree: steps 0 / 0.5 / 1 pass. Step 2 sees `fileCreated` event trigger. **Terminate: HOOK.**
- Rationale: event-triggered, not keyword-triggered. Lives in `~/.kiro/hooks/intake-parse.kiro.hook`.

**Example 4 — STEERING**: Richard asks, "I want the agent to always use bullet points for multi-item responses."
- Tree: steps 0 / 0.5 / 1 / 2 pass. Step 3 identifies identity/always-applicable rule. **Terminate: STEERING (auto-include).**
- Rationale: every-chat rule about response shape. Belongs in soul.md or a style steering file. Note: this already exists; example is illustrative for the decision tree.

**Example 5 — SUBAGENT**: Richard asks, "I want a specialist agent that does deep career coaching using the full body system."
- Tree: steps 0 / 0.5 / 1 / 2 / 3 pass. Step 4 identifies specialist domain (career coaching) requiring deep context + autonomous execution. **Terminate: SUBAGENT.**
- Rationale: narrow domain, deep specialist, requires its own tool allowlist. Lives as `rw-trainer` subagent (already exists; example is illustrative).

**Example 6 — ORGAN**: Richard asks, "I want a single place to track OP2 targets per market that the agent can read during callout writing."
- Tree: steps 0 / 0.5 pass. Step 1 hits: already covered by `ps.targets` DuckDB table + `ps-performance-schema.md` reference doc, so would hit EXTEND-EXISTING. (Had there been no existing coverage, step 5 would identify persistent shared state → ORGAN. Example is illustrative of the ORGAN leaf.)

**Example 7 — POWER**: Richard asks, "I want to onboard Bedrock AgentCore with its own tools and docs."
- Tree: steps 0 / 0.5 / 1 / 2 / 3 / 4 / 5 pass. Step 6 identifies MCP-bundle need. **Terminate: POWER (Guided MCP).**
- Rationale: includes `mcp.json` with agentcore-mcp-server. Lives as `aws-agentcore` power (already installed; example is illustrative).

**Example 8 — SKILL**: Richard asks, "When I say 'write a WBR callout', I want the full analyst-writer-reviewer pipeline to fire."
- Tree: steps 0 through 6 all pass through. **Terminate: SKILL.**
- Rationale: keyword-activated ("write a WBR callout", "WBR", "callout"), orchestrates multiple subagents in sequence (the callout pipeline), no MCP bundle needed, not every-chat. Lives as `wbr-callouts` skill (already installed).

---

## Sensitive-Data Classification Rules

Four tiers. Each tier has a concrete source-of-truth and a concrete path-allowlist. The validator enforces the allowlist at creation time and any time a `status: current` skill/power is edited. **Legacy assets are exempt** until they are reclassified via touch-it-classify-it.

Workflow dependency: Phase C safe-creation uses these rules to validate the declared class. Future workflow: L5 autonomous agents that propose new skills on their own must classify before the create step will proceed.

### Tier definitions

**Public** — already published externally or intended for public consumption.
- Sources: wiki articles under `~/shared/wiki/agent-created/` published to w.amazon.com or external; public AWS/Kiro documentation; open-source references; power-builder content.
- Examples (once classified): power-builder POWER.md, aws-agentcore POWER.md, flow-gen POWER.md.
- Path allowlist for files declared Public: any path, including `~/.kiro/skills/`, `~/.kiro/powers/installed/`, `~/shared/wiki/**`, and anything synced to the agent-bridge repo.

**Amazon_Internal** — non-confidential Amazon information used in routine work.
- Sources: internal Amazon processes, tool guides, generic workflow patterns that happen to involve Amazon tools (Asana, DuckDB, Outlook MCP).
- Examples (once classified): bridge-sync (syncs files but contains no Amazon-confidential content itself), charts (visualization patterns), wiki-audit (generic audit procedure).
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

For `status: current` assets, if `sensitive_data_class` is absent the validator errors. For `status: legacy` assets the field is not required and the validator does not error — the asset is treated as `Amazon_Confidential` for path-allowlist checks at any edit boundary, and the classification will be set explicitly during touch-it-classify-it.

### Path-allowlist enforcement algorithm

Given a `status: current` skill S with declared sensitivity C and an output-write path P:
1. Look up allowlist(C) from the table above.
2. Check P ⊆ allowlist(C). If not, emit validation error.
3. For declared-class Amazon_Confidential and Personal_PII, additionally check: does P lie inside any directory currently synced to agent-bridge (per bridge-sync.md's sync list)? If yes, emit sync-violation error.
4. The sync list is read at validation time, not cached. If bridge-sync.md's sync targets change, the next validator run catches any newly-illegal paths.

For `status: legacy` skills, steps 1-4 are not run — legacy skills are grandfathered. The path-allowlist check runs on the first edit (when the asset becomes `current`).



---

## Portability Tier Rules

Two tiers. **The portability validator is advisory — it emits findings, it does not reject or rewrite skills.** This is a deliberate reframe from an earlier draft that treated portability as a blocking gate. On the real on-disk corpus of 9 skills and 4 powers, every existing asset references at least one `mcp_*` tool, a `.kiro.hook`, a `discloseContext` call, a subagent, or a script — which means a blocking validator would force-downgrade every legacy asset on first run or require a `platform_bound_dependencies` list nobody will maintain. That is exactly the "novel structural tax the audit would turn around and delete" failure mode. Portability is a *declaration of intent* and a *source of honesty in the file itself*, not a gate.

Workflow dependency: Phase C safe-creation uses these rules to classify the declared tier for `status: current` assets and to emit advisory findings. Future workflow: cold-start recovery onto a platform without Kiro's MCP servers — the tier declaration tells a recovering agent which files it can trust cold.

### Tier definitions

**Cold_Start_Safe** — the file's intent is expressible in plain text. A new agent on a different platform can read the file and understand what it's supposed to do using only the file text plus other `Cold_Start_Safe` files in the agent-bridge repo.
- Positive markers: the SKILL.md / POWER.md body describes the *goal* and the *procedure* in prose. If it names specific mechanisms, it names them with fallbacks ("use Slack MCP if available; otherwise describe what would be posted").
- Negative markers (would indicate `Platform_Bound`): hard-coded references to `mcp_*` tool names, specific `.kiro.hook` IDs, specific subagent names, script paths, DuckDB table names.
- Examples (aspirational — no legacy skills currently classify as Cold_Start_Safe): a `wiki-write` skill that describes *how to write a wiki article* in prose, without naming the wiki-writer subagent, could be Cold_Start_Safe. A `charts` skill that describes the *kind of dashboard* and the inputs, without naming the dashboard-server script, could be Cold_Start_Safe.

**Platform_Bound** — the file depends on platform-specific mechanisms to function. A recovering agent on a different platform would need to either re-implement the dependencies or rewrite the skill.
- All 9 existing skills fall here on inspection: `bridge-sync` depends on `scripts/sync.sh` and `mcp_ai_community_slack_mcp_post_message`; `charts` depends on a dashboard-server script; `coach` depends on the `rw-trainer` subagent; `wbr-callouts` depends on the analyst → writer → reviewer subagent pipeline; etc.
- **`platform_bound_dependencies` is RECOMMENDED, not required.** An asset declared Platform_Bound MAY enumerate its platform-specific dependencies. Omission is not a validation error — it's advisory information that helps a future cold-start attempt but its absence does not block anything. When present, the validator parses it and cross-checks consistency with the file body (see validator rules below).

### Portability validator — advisory only

The portability validator runs at Phase C for `status: current` assets and can be invoked ad-hoc for any asset. It **emits a report**, not a pass/fail verdict.

Validator procedure for an asset F with declared tier T:

1. Scan F's body for platform-bound-indicator tokens:
   - `mcp_[a-z_]+` (MCP tool names)
   - `invokeSubAgent` and subagent names from `~/.kiro/agents/`
   - `[a-z0-9_\-]+\.kiro\.hook` (hook IDs)
   - `discloseContext`, `kiroPowers`
   - Script paths under `scripts/`, `~/shared/tools/`, `~/shared/scripts/`
   - DuckDB table references (`ps\.`, `signals\.`, `asana\.`, `main\.`)
2. Collect all matches into a findings list.
3. Emit the findings as **informational output**, grouped by category:
   - "Declared `Cold_Start_Safe` — findings: {list of tokens detected}. Author review: are these references essential, or can they be paraphrased?" (advisory only — no rejection)
   - "Declared `Platform_Bound` — findings: {list of tokens detected}. `platform_bound_dependencies` list: {declared list}. Cross-check: {tokens in body NOT listed, tokens listed NOT in body}." (advisory only — cross-check is informational)
4. **The validator never modifies F. The validator never blocks writes. The validator's only output is a report.**

The report is written to Phase C's session state and surfaced to Richard during Phase C.2 review. Richard decides whether to rewrite the file, update the declared tier, or proceed as-is. The output is also logged as an `activated` event subtype `portability_report` in activation-log.jsonl when the validator runs.

### Consistency report (replaces blocking check from earlier draft)

For an asset declared `Cold_Start_Safe` where the body contains Platform_Bound-indicator tokens, the validator emits a consistency note: "Declared Cold_Start_Safe but body references {token}. Consider rewriting the reference to be platform-agnostic, or downgrading tier to Platform_Bound." **This is advisory. The asset is saved either way.** Contrast with the earlier-draft behavior which would have rejected or auto-downgraded; that earlier behavior was the structural tax F1 was designed to remove.

### Why advisory, not enforcing

Three reasons:

1. **Real-world compatibility**: the 13 installed assets contain Platform_Bound tokens by necessity. A blocking validator would force every legacy asset to either carry a `platform_bound_dependencies` list nobody will maintain or downgrade to Platform_Bound with stub documentation. Either outcome is what the subtraction audit would catch and delete in the next cycle.
2. **Cold-start recovery is aspirational**: Cold_Start_Safe is aspirational documentation that describes a portability goal. Turning it into a pass/fail check would flip the meaning from "I am trying to make this portable" to "my code didn't compile", which is a category mismatch.
3. **Trust the author**: Richard or whoever writes a skill is the one who knows whether a reference is essential or accidental. The validator surfaces *what* references exist; the human decides *whether they matter*.


---

## Inventory File Spec

The inventory is a single markdown file at `~/shared/context/skills-powers/inventory.md`. It is a **reference document**, not an active load-bearing file.

Workflow dependency: Phase A (inventory refresh) writes this file; Phase E (pruning review) reads it; Richard reads it on demand. Future workflow: cold-start recovery onto a new platform reads the inventory as its first step to understand what skills/powers exist.

### Location (orphan-by-design)

**Path**: `~/shared/context/skills-powers/inventory.md`.

**Why this path, and why it's orphan-by-design in the audit's referrer graph**:

The inventory is a reference document, not a live-execution file. Its path-references to skills count as `documentation` referrers in the audit's classification, NOT `path` (active). This matters because of a second, stronger fact: **skills and powers themselves are ORPHAN-classified by default in any future audit**, unless something else actively references them (a hook fires the skill, an agent reads the power's MCP, a script imports a skill's helper). The inventory does not save them. This is the design: skills/powers are extension-loaded by construction, and extension-loaded files register as orphan in a referrer-graph analysis because nothing loads them in the active path — their activation tool (`discloseContext`, `kiroPowers`) is not a path-reference.

An earlier draft of this section claimed that placing the inventory inside `~/shared/context/skills-powers/` would make its path-references to each skill count as *active referrers* under audit R2.8. That claim was wrong. The audit's "active" definition (R2.8 + R2.2) is about **referrer liveness**, not directory location. Nothing auto-loads `~/shared/context/skills-powers/inventory.md`. In the audit's graph, the inventory is ORPHAN — and so are the skills and powers it lists.

**We accept this orphan status deliberately**. The alternatives are worse:

- **Auto-loaded steering referencing the inventory**: triggers audit R5.6 UNCLEAR coupling (always-auto-included referrer → candidate file), soft-preserving the inventory forever. Also taxes every chat.
- **A `promptSubmit` hook that loads the inventory every turn**: the exact recurring-service pattern anti-goal #1 forbids.
- **A script in `~/shared/tools/` that touches the inventory**: a script that exists only to create active-referrer evidence is itself kill-list material.

The correct answer: accept ORPHAN status; keep the inventory (and the skills it lists) alive by value to Richard and future agents reading it on demand; let the adoption system's governance layer (inventory + activation log) serve as the documentary justification the audit's R5 would otherwise apply to an unreferenced file. Kept discoverable (see below) but governed by usefulness, not auto-load.

**What makes the inventory discoverable despite being orphan**:

A single **name-reference line** is added to soul.md's Data & Context Routing table. Per audit R2.2, a bare filename is `name` match-type — informational, not active. Does NOT save the inventory from ORPHAN status, but makes it discoverable to an agent parsing soul.md naturally.

Proposed soul.md addition (name-reference only, no `#[[file:...]]`, no auto-include):
```
| Skills/powers inventory: what's installed and what's activated | — | ~/shared/context/skills-powers/inventory.md |
```

Richard can also find it by asking any agent "where's the skills inventory?".

### Shape and schema

See §Data Model → "Inventory file" for the full table schema.



---

## Pilot: activation of the 9 already-installed skills

**The skills corpus already exists.** `bridge-sync`, `charts`, `coach`, `cr-tagging`, `sharepoint-sync`, `wbr-callouts`, `wiki-audit`, `wiki-search`, `wiki-write` are the pilot. The adoption system's pilot measure is not *ship N new skills* — it is **achieve sustained activation of the installed 9 over a 30-day window**. Rationale: the actual adoption gap is *activation of what exists*, not *design of what to build next*. See §Design Decisions → "Why the pilot is the existing 9, not 3 new ones".

Workflow dependency: Phase 0 activation-baseline + Phase D activation-logging produce the activation metric that determines whether the adoption habit is working. Future workflow: once activation baseline is re-established and shown to trend upward, the leverage formula (below, demoted) becomes relevant for deciding *additional* candidates.

### Pilot metric

The pilot runs for 30 days starting at Phase 0 execution.

**Success criterion**: the activation log shows ≥3 activations per skill across the 30-day window, with at least 5 of the 9 skills activated at all. Skills that fail the threshold become **Phase E pruning candidates, not replacements-to-build**.

The metric is asymmetric: a low-activation skill is presumed redundant (either covered by another mechanism, or its workflow doesn't recur often enough to justify codification). The burden of proof is on the skill to show it's used, not on the agent to prove it's unused.

### Pilot procedure

1. **T0 (day 0)**: run Phase 0. Scan `~/shared/context/intake/session-log.md` for historical activations per skill/power name. Emit `baseline` rows in activation-log.jsonl. Snapshot the inventory showing current activation state.
2. **T0-T30 (days 0-30)**: normal operation. Activation log accrues `activated` events via Phase D as skills/powers are invoked by the pre-draft activation path (agent checks the inventory on reading the request and activates on keyword match before responding). Richard is not asked to remember to invoke skills. If the activation habit is working, the log grows.
3. **T30 (day 30)**: compare per-asset activation counts against the success criterion. Skills meeting it stay. Skills failing it move into the next Phase E pruning review as archival candidates.

### What the pilot produces and does not produce

Produces: 30 days of activation data in activation-log.jsonl; a re-rendered inventory showing per-asset usage at T30 vs. T0; a per-skill decision at T30 (keep if criterion met, prune if not).

Does NOT produce:
- **Any new skills or powers.** No new skill is created during the pilot window unless Phase B routing explicitly terminates at CREATE_NEW AND the overlap-check surfaces no viable EXTEND_EXISTING on the existing 9.
- **A new inventory ranking.** Leverage formula is demoted to a future-rounds tool.
- **Any automated intervention.** Missed-skill detection is out of scope per F4. Missed skills surface via `missed-by-feedback` entries (Richard flagging), not an auto-detector.

### Why 30 days and not shorter

Activation is low-frequency. Coach-pipeline triggers are monthly. SharePoint sync is weekly. WBR callouts are weekly. A 7-day window doesn't capture the full activation cycle. A 30-day window matches the pruning cadence (R8.5) and gives each low-frequency skill at least one natural opportunity.

### Phase B step 1 — check existing skills first (elevated)

Phase B of the architecture — the routing decision tree — already includes an EXTEND-EXISTING gate at step 1. During and after the pilot, this gate's standard is strict:

- Before walking the rest of the decision tree for any new-workflow proposal, the agent MUST check whether any of the 9 installed skills' trigger lists or any of the 4 installed powers' keyword lists matches the proposed workflow description. Match threshold: 50% keyword overlap OR one exact trigger phrase match.
- A match → terminate at EXTEND_EXISTING(asset) with the matched asset surfaced to Richard for edit rather than create.
- No match → continue to step 2 (event vs. keyword split).

This is not a new step — it's a stricter standard for an existing step. The earlier draft treated EXTEND-EXISTING as one gate among many; this revision treats it as the first-priority gate. Rationale: the on-disk corpus of 13 assets is underutilized; routing should bias toward surfacing existing coverage before creating more.

### The leverage formula (demoted — reserved for future rounds)

The earlier draft included a leverage-ranking formula for new-skill candidates:

> `leverage_score = (frequency_per_month × reexplanation_cost_in_minutes × cross_team_usability) / one_time_creation_cost_in_minutes`

This formula is **preserved as a reference for future rounds** — specifically, rounds after the pilot concludes and Richard has 30+ days of activation data indicating a real activation gap not addressable by extend-existing. Until then, the formula is not in active use. It is here rather than deleted because:

1. It encodes a reasonable mental model (recurring × reexplanation ÷ creation).
2. Deleting it would lose the reasoning and require re-deriving it later.
3. Keeping it disarmed (demoted) is cheaper than keeping it armed (where every new proposal runs the formula even though addition is off the table).

**When the formula becomes active**: only after Phase 0's 30-day measurement concludes AND Richard explicitly decides the activation gap justifies new-skill creation AND a specific workflow has passed through the Routing Decision Tree's steps 0, 0.5, and 1 without terminating. At that point, the formula ranks the surviving candidates.

**When the formula is NOT active**: during the pilot period, and during any later period where EXTEND-EXISTING terminates a proposal. The formula does not decide whether to create; it only ranks between already-decided create candidates.

### Candidate list source (reference data — future rounds only)

For the eventual future rounds when the formula becomes active, candidate sources per R5.1 are:
- body.md system map
- device.md installed apps / tools inventory
- existing hook inventory (`~/.kiro/hooks/*.kiro.hook`)
- existing subagent inventory (`~/.kiro/agents/*.json`)

Candidates drawn from these sources are evaluated against the Routing Decision Tree. The tree's step 1 EXTEND-EXISTING gate catches most of them; the formula ranks whatever survives. The R5.6 cap of "no more than three candidates to pilot adoption" becomes relevant only after the initial pilot on existing assets has established a baseline.



---

## Adoption Habit Integration

The goal is that skills surface naturally when Richard's request matches their triggers.

Workflow dependency: Phase D activation logging; Phase E pruning review. Future workflow: L5 autonomous agents that invoke skills on their own during multi-turn tasks rely on the same trigger-matching logic.

### In-turn activation via discloseContext / kiroPowers activate

On reading a user request, the agent checks the inventory's trigger lists (skills) and keyword lists (powers). If the request text matches any installed skill's trigger keywords or any installed power's `keywords` array, the agent activates the matching asset before producing the substantive response:

- For skills: call `discloseContext(name=matched_skill_name)`.
- For powers: call `kiroPowers activate(powerName=matched_power)`.

The activation writes one row to `activation-log.jsonl` with `event: "activated"`, the matched name, a short `request_summary`, the session id, and the timestamp. If multiple skills/powers match, the agent activates whichever has the strongest keyword overlap; ties are broken by most-recently-activated.

This is the *only* machine-enforced activation path. No post-draft loop. No pre-send re-check. Adherence is not enforced — it is observable by activation-log growth. The logged counts are the measurement; Richard and any downstream agent can read `activation-log.jsonl` to see whether the adoption habit is working.

### Missed-skill detection is not machine-enforced

Missed-skill detection is not machine-enforced. Gap data comes from Richard flagging "you should have used skill X" after the fact — at which point the agent appends a `{"event": "missed-by-feedback", ...}` entry to the activation log. Attempting to build a pre-send auto-detector violates anti-goal #1 (no recurring automation layered on top) and reintroduces the exact "remember to remember" failure mode skills were designed to eliminate. See §Design Decisions → "Why missed-skill detection was cut" for the full reasoning.

### R6 requirement mapping after the revision

| Requirement | Status | Implementation |
|---|---|---|
| R6.1 (auto-activate on keyword match) | implemented | `discloseContext` / `kiroPowers activate` in-turn before response, on reading the request |
| R6.2 (note missed skills) | reinterpreted | Manual flagging by Richard → `missed-by-feedback` event. No automatic post-draft detector — this is a deliberate anti-goal (see §Anti-Goals #10). R6.2 should be rewritten in requirements.md to remove the agent-side auto-note obligation; see the requirements-adjustment summary at the end of this revision. |
| R6.3 (durable activation log) | implemented | `activation-log.jsonl` appended in Phase D |
| R6.4 (log fields) | implemented | name, request_summary, session_id, ts (see Data Model) |
| R6.5 (periodic review of unused skills) | implemented | Phase E pruning review reads activation log at 30-day cadence |



---

## Safe-Creation Workflow

Phase C of the architecture. Runs on two triggers: (a) a new asset created from a Routing Decision Tree terminating at SKILL, POWER, STEERING, HOOK, SUBAGENT, or ORGAN; (b) a `status: legacy` asset being edited for any reason (touch-it-classify-it migration).

Workflow dependency: writes new and migrated assets; produces overlap-check.json for new assets; updates inventory.md and activation-log.jsonl. Future workflow: any L3-L5 workflow that proposes creating a new skill runs through the same steps.

### Phase C.1 — Overlap check (new assets only)

Applies to new assets. For legacy reclassification, overlap-check is skipped — the asset already exists; a retrospective overlap check has no decision to document.

Procedure:

1. Parse the proposed asset's description / keywords / trigger list.
2. Search each of the 6 Kiro kinds + non-Kiro mechanisms:
   - Skills: all files under `~/.kiro/skills/`
   - Powers: all files under `~/.kiro/powers/installed/`
   - Subagents: all files under `~/.kiro/agents/`
   - Hooks: all files under `~/.kiro/hooks/`
   - Steering: all files under `~/.kiro/steering/`
   - Organs: all files under `~/shared/context/body/`
   - Non-Kiro mechanisms: `.bashrc`, cron jobs, git hooks, known IDE features, known team tools
3. For each candidate, score overlap by keyword/trigger match and purpose-line semantic match (cosine similarity of the one-line purpose).
4. If max overlap ≥ 75% → recommend EXTEND_EXISTING (asset_path) to Richard. If Richard confirms, terminate safe-creation and redirect to editing the existing asset.
5. If max overlap in 50%-75% range → surface as overlap_candidate in the evidence record; Richard reviews alongside the proposed creation.
6. Write `overlap-check.json` with the full evidence record (see Data Model).

### Phase C.2 — Richard review

The agent presents:

- Proposed asset content (SKILL.md / POWER.md / etc. draft)
- Declared metadata: sensitive_data_class, portability_tier, platform_bound_dependencies (if any)
- Overlap-check findings (candidates, decision rationale)
- Portability validator report (advisory, see §Portability Tier Rules)
- Sensitive-data path-allowlist check result (enforced, see §Sensitive-Data Classification Rules)

Richard explicitly approves, edits, or cancels. `reviewed_by_richard: true` is written to the overlap-check record only on explicit approval. Absence of veto is not approval.

### Phase C.3 — Write (new asset) OR classify-then-write (legacy migration)

**New asset path**: write the file to `~/.kiro/skills/{name}/SKILL.md` or `~/.kiro/powers/installed/{name}/POWER.md` with full extended frontmatter. Status is born `current`.

**Legacy migration path (touch-it-classify-it)**: the triggering edit (bug fix, description tweak, whatever Richard came to the file to do) is staged in memory but NOT yet written. Before the write:

1. Agent prompts Richard with the classification questions: "This is a legacy skill. Before we save your edit, classify: sensitive_data_class? portability_tier? owner_agent?"
2. Richard answers. Values are inserted into the frontmatter.
3. `status` flips from implicit `legacy` to explicit `current`.
4. `created_at` is set to the original file's `stat -c %y` mtime (preserving historical creation date) or to "UNKNOWN" if stat fails.
5. `last_validated` is set to the current timestamp.
6. THE EDIT IS NOW WRITTEN with full extended frontmatter.

This is the critical migration trigger: no forced batch-day, no abandoned "TODO classify" placeholder fields, no flag day. Classification happens exactly when Richard is already in the file, so the marginal cost is one prompt and three answers.

**If Richard refuses to classify** (e.g., "I'm fixing a typo, not classifying this today"), the agent accepts the refusal and writes the edit WITHOUT migrating the asset's status. The asset remains `legacy`. The next edit is another classification opportunity. This is a deliberate escape hatch — demanding classification on every edit would be the flag-day failure mode with extra steps.

### Phase C.4 — Activation validate

For new skills: call `discloseContext(name=new_name)` and verify no error. For new powers: call `kiroPowers activate(powerName=new_name)` and verify documentation returns. For migrated legacy assets: same activation check.

On success, `last_validated` is set to the current timestamp and written back to the frontmatter.

On failure, the asset is marked with a validation-failure comment in the frontmatter (`# validation-failed: <reason>`), Richard is notified, and the asset is NOT activated in any session until re-validated.

### Phase C.5 — Inventory update + activation log

The inventory.md is regenerated (Phase A reactive refresh). For new assets, a `created` event is appended to activation-log.jsonl. For legacy reclassification, a `created` event with subtype `classified` is appended.



---

## Round-Trip File Format

Per R9, the SKILL.md and POWER.md file formats must survive parse → edit → re-serialize without corruption.

Workflow dependency: Phase C writes files; any future agent-driven edit reads and re-writes them. Future workflow: cold-start recovery parses and re-serializes skills on a different platform — the round-trip guarantee is what makes this portable.

### Canonical SKILL.md format

```
---
<YAML frontmatter — key ordering preserved alphabetically within required/optional groups>
---

<markdown body — unchanged by parse/serialize>
```

YAML rules:
- UTF-8 encoding, LF line endings.
- 2-space indentation for nested values.
- Strings with embedded colons, quotes, or leading/trailing whitespace are double-quoted.
- Lists use block form (one item per line with `- ` prefix) for lists of 2+ items; inline `[...]` only for empty lists.
- Key order within a group is alphabetical. Groups are (in serialize order): identity (`name`, `description`), status (`status`), classification (`sensitive_data_class`, `portability_tier`, `platform_bound_dependencies`, `owner_agent`), timestamps (`created_at`, `last_validated`).

### Canonical POWER.md format

Same rules as SKILL.md plus:
- Keys `displayName`, `keywords`, `author` preserved in the identity group.
- `mcp_servers_declared` appears in the classification group.

### Round-trip property

For any SKILL.md or POWER.md file F that passes validation:
- `parse(F) → structured-representation S`
- `serialize(S) → F'`
- `parse(F') → S'`
- Then `S == S'` (structural equality) AND the markdown body of F and F' are byte-identical.

Key ordering within groups is enforced during serialize so that re-serialization is deterministic. Comments in the YAML are preserved as adjacent metadata (attached to the next key) and re-emitted in the same position.

### Error reporting (non-silent rewrites per R9.4)

If a file does not match the canonical format at parse time:
- **Unknown fields**: flagged but preserved in a `legacy_unknown_fields` map; not dropped.
- **Wrong types**: parse fails with a descriptive error identifying the field, expected type, and actual type. The file is NOT modified.
- **Missing required fields for `status: current`**: parse succeeds, validation fails with a list of missing fields. The file is NOT modified.
- **Malformed YAML**: parse fails with the YAML library's error message and line number. The file is NOT modified.

The adoption system NEVER silently rewrites a file. Any rewrite is explicit, reviewed by Richard (Phase C.2), and leaves a trace in the activation log (`created` event with subtype `format_migration` if the rewrite was for format normalization).

### Validator output

Per R9.5, the validator reports for any skill/power file:
- Is it format-compliant? (YAML parses, required fields for declared status present, field types correct)
- Is the declared metadata complete for its status? (for `status: current`: all required fields present with non-null values)
- Are there advisory portability findings? (see §Portability Tier Rules)
- Is the output-path-allowlist consistent with the declared sensitive_data_class? (see §Sensitive-Data Classification Rules)

The validator emits a report, not a verdict. Format-compliance failures block writes. Advisory findings do not.



---

## Pruning Review

Phase E of the architecture. Human-triggered, monthly or ad-hoc. Implements R8.

Workflow dependency: reads inventory.md and activation-log.jsonl; writes archive directory; updates inventory.md. Future workflow: the same pruning procedure applies to any adoption system Richard builds on top of skills/powers in future rounds.

### Trigger

Richard invokes pruning by saying "run skills pruning review" or equivalent. Phase E never runs automatically. This is deliberate — automated pruning would itself be a new recurring surface (audit anti-goal #1).

### Procedure

1. **Compute stale set**: for each installed skill/power, check last `activated` event timestamp in activation-log.jsonl. If no activation in last 30 days AND the asset is `status: legacy` OR `status: current`, add to stale candidate list. Exclude `status: retired` (already pruned) and skills/powers created in the last 30 days (not enough time to measure).
2. **Present to Richard**: render the stale list with per-asset {name, status, days since last activation, activation count in last 90 days, creation date if known}. Sorted by "most stale first" (longest gap).
3. **Richard reviews each row**: APPROVE (prune), DEFER (keep until next cycle, note reason), or PROTECT (keep permanently, note reason). Absence of decision = DEFER.
4. **On APPROVE**:
   - Archive: `cp -r ~/.kiro/skills/{name}/ ~/shared/wiki/agent-created/archive/skills-powers-pruned-{YYYY-MM-DD}/{name}/` (or `powers/installed` for powers).
   - Delete: `rm -rf ~/.kiro/skills/{name}/` (or powers equivalent).
   - Log: append `pruned` event to activation-log.jsonl with archive_path.
   - Inventory: mark the row `status: retired` for one full cycle, then drop.
5. **On DEFER / PROTECT**: record the decision in the pruning-review session transcript. No file operations.

### Never-prune-under-use guarantee

Per R8.4: if an asset has any `activated` event in the last 30 days, it is NOT in the stale set, regardless of status. This is enforced at set construction, not at Richard-review time.

### Archive-before-delete

Per R8.3: every pruned asset is archived before deletion. Archive path includes the date of the pruning review for traceability. The overlap-check.json evidence (if present) is archived alongside the asset — so a future audit asking "why was this pruned?" can trace back to both the creation rationale and the pruning rationale.

### Cadence

Per R8.5: Richard sets his own cadence. Default: monthly, invoked on Fridays after the retrospective. Pruning is a decision ritual, not a scheduled task.



---

## Anti-Goals

Explicit list of things this spec is NOT, and things a well-intentioned agent might otherwise build that would violate the spec's governance stance. Each entry names what's forbidden and why.

1. **Not an ongoing adoption service**. There is no daemon, no always-on hook, no scheduled job that audits skills on Richard's behalf. Activation logging is continuous because it's a single JSON-line append per invocation; pruning is human-triggered. A "monthly automated pruning mail" would add always-on surface for a task Richard can run when he wants.

2. **Not a replacement for `.kiro/steering/soul.md`**. This spec does not install its own auto-loaded steering. The inventory is discoverable through a name-reference in soul.md's Data & Context Routing table; nothing more. If a future agent suggests adding `inclusionMode: always` to any file in `~/shared/context/skills-powers/`, reject.

3. **Not a build tool for new skills**. This spec governs adoption; it does not produce skills. Building a new skill is a downstream activity gated by the Routing Decision Tree. The spec produces the rules; separate specs produce the assets.

4. **Not a duplicate of the subtraction audit**. The audit applies subtraction to existing files; this spec applies the same tests to proposed additions. They share methodology and artifacts but do not overlap scope.

5. **Not an always-on validator daemon**. Phase C validation runs reactively on create/migrate. No pre-commit hook, no scheduled validator sweep, no continuous integration check. The validator is a function the agent calls when it's doing something; it doesn't loop.

6. **Not a flag-day schema migration**. Legacy assets migrate on touch, one at a time, when Richard is already editing them. No forced day-zero migration of all 13 assets. The earlier draft's "every skill must have these fields" check is replaced by `status: legacy` exemption.

7. **Not a blocking portability gate**. The portability validator emits findings, not verdicts. No skill or power is rejected, downgraded, or rewritten based on portability tokens detected in its body. The validator reports; the human decides.

8. **Not a recurring-service pattern**. No hook creates, audits, or modifies skills automatically. The only continuously-running component is activation logging, which is one JSON-line append and doesn't involve any reasoning.

9. **Not a candidate-generation machine**. The pilot is measurement of existing assets, not enumeration of new ones. The leverage formula is demoted until activation baseline is established.

10. **Not a post-draft behavioral convention**. Activation habit is structurally enforced (keyword match → `discloseContext` call before response) or it isn't enforced. A post-draft pre-send self-check is not enforcement — it's a convention the agent is supposed to remember, which is the same failure mode skills were supposed to eliminate. Missed-skill detection is not machine-enforced in this spec; gap data comes from Richard flagging after the fact (`missed-by-feedback` events). If the platform later provides a true pre-response-send event, a detector can be scoped in a future spec; until then, this anti-goal stands.



---

## Design Decisions and Rationale

The reasoning behind structural choices that aren't obvious from the rules themselves. Each entry names the decision, the alternatives considered, and why the chosen path wins.

### Why the routing tree rejects before it routes

Steps 0 and 0.5 of the Routing Decision Tree ask "should this exist at all?" and "is this already handled outside Kiro?" before any Kiro-mechanism branching. The earlier draft's tree started at "event vs. keyword?" — a mechanism-selection question. That ordering is wrong: it assumes the workflow belongs inside Kiro before asking whether it needs to be codified at all. The new tree applies subtraction before addition to itself — the first question is always "don't add", then "not in Kiro", then mechanism selection. The `dashboard-server.kiro.hook` kill-list entry (a hook that duplicated `.bashrc`) is the reference case step 0.5 is designed to prevent.

### Why the REJECT gate checks non-Kiro mechanisms

The audit's DELETE of `dashboard-server.kiro.hook` (orphan, 11 lines, duplicated by `.bashrc`) is the canonical case. Richard's tools live across shell, native apps, Amazon's ecosystem, and Kiro. Kiro-only duplication of a solved workflow is the subtle failure mode — step 0.5 closes it. Without the gate, a workflow that's already solved by `.bashrc`, cron, git hooks, or a team tool could still pass into Kiro-mechanism selection and land on HOOK or SUBAGENT. The gate names the class of failure ("duplication across tool boundaries") and terminates before any Kiro surface is added.

### Why orphan-by-design for the inventory

The inventory lives at `~/shared/context/skills-powers/inventory.md` and is intentionally ORPHAN in the audit's referrer graph. An earlier draft claimed that placing the file inside `~/shared/context/` made its path-references to skills count as *active referrers*. That claim was wrong — the audit's liveness definition is about referrer load, not directory location. Making the inventory live-by-steering would trigger audit R5.6 UNCLEAR coupling (always-auto-included referrer to candidate file, soft-preserving the inventory forever). Making it live-by-hook would violate anti-goal #1. Making it live-by-script would create a script whose only purpose is generating active-referrer evidence — itself a kill-list candidate. The correct tradeoff is: accept ORPHAN status, keep the inventory alive by value rather than by load-path, and make it discoverable through a single name-reference line in soul.md's Data & Context Routing table (informational per R2.2, does not save from ORPHAN but does make the file findable).

### Why the portability validator is advisory

The earlier draft's portability validator enforced a blocking check: a skill declared `Cold_Start_Safe` with a Platform_Bound token in its body would be rejected or auto-downgraded. Against the real on-disk corpus of 9 skills + 4 powers, every existing asset contains at least one `mcp_*` tool name, `discloseContext` call, subagent reference, or script path. The enforcing validator would mass-flag the entire corpus on first run, forcing either (a) 9+4 `platform_bound_dependencies` lists nobody will maintain or (b) 9+4 forced-downgrades with no semantic change. Either is the novel structural tax the audit itself would catch and delete in the next cycle. The advisory validator produces honest information (here are the tokens in the body) and leaves the judgement to the human (are those essential or accidental).

### Why legacy / current / retired (and the touch-it-classify-it migration)

The earlier draft required every SKILL.md / POWER.md to have `sensitive_data_class`, `portability_tier`, `created_at`, `last_validated`. On day-zero of this spec's first run, zero of the 13 installed assets have any of these fields. The earlier draft's inventory-bijection property (every file on disk appears in inventory) conflicted with its schema-validation property (every row has required fields) — on the real corpus one of the two properties had to fail. The `legacy` status resolves the conflict: legacy rows appear in the inventory (bijection preserved) but are exempt from schema validation (schema stays strict for `current`). Migration happens on touch, not on a flag day — because the subtraction audit has shown that flag-day migrations produce abandoned fields that live in the system forever as legacy sludge.

### Why missed-skill detection was cut

An earlier draft included a post-draft pre-send missed-skill detector that walked the drafted response, keyword-matched against installed skills, and emitted a `missed` event. That mechanism is cut entirely — not retired-in-place, not deferred-with-hook.

Why:

1. **No platform event exists between response draft and response send.** Anything at that moment would be a convention — instructions the agent is supposed to remember to follow.
2. **A convention-based self-check is the exact failure mode skills were meant to eliminate.** "Remember to check for missed skills after drafting" has the same shape as "remember that the coach skill exists" — the thing skills are supposed to replace.
3. **Gap data is cheap without a detector.** Richard flags a miss; a `missed-by-feedback` row is appended. Slower than a theoretical auto-detector but 100% accurate and free when no miss is noticed.
4. **Pre-draft activation is the enforced path and is sufficient.** Agent checks the inventory on reading the request, activates on keyword match before responding. If that check runs, misses are rare by construction; if it doesn't, a post-draft detector would just be a second convention failing at the same thing.

If a real pre-response-send event appears in the platform later, a detector can be re-scoped in a future spec. Until then, anti-goal #10 stands.

### Why the pilot is the existing 9, not 3 new ones

The earlier draft's R5.6 ("no more than three candidates to pilot adoption") framed the pilot as building 3 new skills. Reality: 9 skills and 4 powers are already installed, never meaningfully invoked. Building 3 more while the installed 9 are at or near zero activation amplifies the gap — cumulative installed count goes to 12, activation rate doesn't move, next cycle the audit catches another generation of orphans.

**9 pilots with 0 activation is a larger signal than 3 pilots with unknown activation.** Pilot = 30-day activation measurement against the 9 installed skills, strict criterion (≥3 activations per skill, ≥5 of 9 activated at all). Skills failing the criterion are Phase E pruning candidates on day 31. The activation mechanism and the subtraction mechanism point at the same corpus, reinforcing each other rather than adding surface.

Addition before subtraction is the anti-pattern; subtraction before addition is the rule (soul.md #3). The leverage-ranking formula is preserved for future rounds but disarmed until Phase 0 baseline data indicates a real gap extend-existing cannot close.

### What we almost added and cut (audit-style self-application)

Applied to this spec's own mechanisms, the audit's Current Usage Test and Future Workflow Test:

- **A dedicated `skills-powers.md` auto-loaded steering file**: FAILS both tests. No current workflow needs it that soul.md's routing table can't handle. No future L3-L5 workflow needs the steering mechanism specifically. METAPHOR-ONLY → CUT.
- **A scheduled "freshness email" summarizing inventory weekly**: FAILS both tests. Current freshness is on-demand; future autonomous agents are more likely to query the inventory directly than consume a summary email. METAPHOR-ONLY → CUT.
- **A DuckDB schema for activation logs**: FAILS the Future Workflow Test for cold-start scenarios. A new agent on a different platform cannot read DuckDB. JSONL is portable; DuckDB is Platform_Bound. The line-delimited JSON format is preserved. DuckDB materialization is optional downstream and not in scope here.
- **The post-draft missed-skill detector**: FAILS the Current Usage Test (no platform event exists) and is the exact failure mode skills were meant to eliminate. CUT (see above).
- **The blocking portability validator**: FAILS the Current Usage Test against the real corpus. CUT in favor of advisory (see above).
- **The leverage-ranking formula as a gate**: FAILS the Current Usage Test (the gate always passes because Richard only proposes workflows he already thinks are worth codifying). DEMOTED (not cut — the reasoning is preserved for future rounds when activation baseline makes the gate meaningful).



---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

These properties govern the adoption system's machine-facing behaviors (validator, inventory generator, activation logger, overlap checker, routing tree). Governance rules that are documentation-only (tier definitions, path allowlists as written text) are not property-tested — they are specified in §Sensitive-Data Classification Rules and §Portability Tier Rules.

Properties 4, 5, 11 were revised during the 2026-04-22 revision pass per findings F1, F3, F2. Property 13 from the earlier draft (post-draft pre-send missed-skill detector) was dropped entirely per finding F4 — remaining properties have been renumbered so there are no gaps. Property 15 (NON-KIRO-GATE-REJECTION) was added per finding F6. There are 15 properties in the revised design.

### Property 1: INVENTORY-BIJECTION

*For any* filesystem state containing skills under `~/.kiro/skills/` and powers under `~/.kiro/powers/installed/`, the inventory.md's rows bijectively correspond with the on-disk assets — every asset appears as exactly one row with its correct name, status, triggers/keywords, and the columns described in §Data Model → Inventory file. No phantom rows, no missing rows. `status: retired` rows are an exception: they appear for one pruning cycle after deletion to document the transition, then drop.

**Validates: Requirements 1.1, 1.2, 1.3, 7.5**

### Property 2: STALENESS-CORRECTNESS

*For any* activation-log.jsonl L and inventory I, the stale set S(I, L) computed by Phase E equals `{ asset ∈ I : status ∈ {legacy, current} AND no `activated` event for asset.name in L within the last 30 days AND asset not created within the last 30 days }`. An asset with at least one activation in the last 30 days is NEVER in the stale set.

**Validates: Requirements 1.5, 6.5, 8.1, 8.4**

### Property 3: PATH-ALLOWLIST-CORRECTNESS

*For any* `status: current` skill or power S with declared `sensitive_data_class = C` and proposed output-write path P, the validator emits a path-allowlist violation iff P ∉ allowlist(C), per the four-tier table in §Sensitive-Data Classification Rules. For declared C ∈ {Amazon_Confidential, Personal_PII}, the validator additionally emits a sync-violation iff P lies inside a directory currently synced to agent-bridge. For `status: legacy` skills, the validator does NOT run the path-allowlist check (legacy assets are grandfathered until their next edit).

**Validates: Requirements 3.2, 3.3, 3.5, 3.6, 7.4**

### Property 4 (REVISED per finding F1): ADVISORY-PORTABILITY-REPORT

*For any* skill or power S with declared `portability_tier`, the portability validator MAY emit findings listing Platform_Bound-indicator tokens detected in S's body. The validator does NOT reject, rewrite, or auto-downgrade S based on these findings — the report is purely informational. For any S declared `Platform_Bound`, the `platform_bound_dependencies` list MAY be populated; omission is NOT an error and does NOT prevent the asset from passing validation. When the list is populated, the validator MAY emit a cross-check report comparing declared dependencies to tokens detected in the body; mismatches are informational findings, not errors.

**Validates: Requirements 4.3, 4.4, 4.5** (reinterpreted — tier declaration is advisory self-documentation, not an enforced gate; see per-property test note in §Testing Strategy)

### Property 5: INVENTORY-FRESHNESS (with scope note per finding F3)

*For any* inventory.md rendering R with recorded input-state hash H_R, and for the current filesystem state with computed hash H_FS, if `H_R == H_FS` then R reflects the current filesystem. If `H_R ≠ H_FS`, the agent re-runs Phase A before trusting R.

**Scope note**: this property concerns the inventory's *accuracy relative to the filesystem*. It does NOT make claims about the inventory's own active-referrer status in the audit graph. Per finding F3, the inventory is orphan-by-design in the audit — no active load-path makes it "live" in the audit's sense, and that is deliberate. The inventory's accuracy is a property of its contents; the inventory's referrer status is an independent fact about the audit's scoring, and out of scope for this property.

**Validates: Requirements 1.3, 1.4**

### Property 6: ROUND-TRIP

*For any* valid SKILL.md or POWER.md file F, `parse(serialize(parse(F))) == parse(F)` (structural equality), and the markdown body of `serialize(parse(F))` is byte-identical to the body of F.

**Validates: Requirements 9.1, 9.2, 9.3**

### Property 7: NON-SILENT-REWRITE

*For any* SKILL.md or POWER.md file F that does not match the canonical format (unknown required field types, missing required fields for `status: current`, malformed YAML), the validator emits a descriptive error identifying the violation AND the file F is NOT modified on disk.

**Validates: Requirement 9.4**

### Property 8: OVERLAP-CHECK-COMPLETENESS

*For any* new skill or power creation C (Phase C.1 execution), the overlap-check.json artifact produced contains `searched_mechanisms` enumerating all 6 Kiro kinds (skills, powers, subagents, hooks, steering, organs) plus `non_kiro_mechanisms_considered` as a list. Creation of C proceeds to Phase C.3 (write) only if `reviewed_by_richard == true`. Legacy-asset reclassification does NOT require an overlap check.

**Validates: Requirements 2.6, 10.1, 10.3**

### Property 9: ROUTING-PRECEDES-CREATE

*For any* Phase C safe-creation for a new asset, the routing-decision.json evidence from Phase B exists and its terminal leaf is one of {SKILL, POWER, STEERING, HOOK, SUBAGENT, ORGAN} (not REJECT and not EXTEND_EXISTING). If the routing-decision leaf is REJECT or EXTEND_EXISTING, Phase C does NOT run.

**Validates: Requirements 2.3, 7.1, 7.2**

### Property 10: EXTEND-EXISTING-PRECEDENCE

*For any* proposed new workflow W evaluated by the Routing Decision Tree, if any installed skill's trigger list or installed power's keywords list overlaps W's description by ≥75% (or contains an exact trigger-phrase match), the tree terminates at EXTEND_EXISTING(matched_asset) and does NOT produce a new SKILL, POWER, STEERING, HOOK, SUBAGENT, or ORGAN leaf.

**Validates: Requirements 5.4, 10.1, 10.2** (elevated per finding F5 — the existing-first check is now the default gate, not a tie-breaker)

### Property 11 (REVISED per finding F2): STATUS-GATED-SCHEMA

*For any* skill or power S with `status: current`, all required metadata fields (`sensitive_data_class`, `portability_tier`, `platform_bound_dependencies` iff `portability_tier == Platform_Bound`, `created_at`, `last_validated`) are present and typed correctly per §Data Model. *For any* S with `status: legacy`, schema validation is SKIPPED — the minimal original frontmatter (`name`, `description` for skills; `name`, `displayName`, `description`, `keywords`, `author` for powers) is sufficient. When a `status: legacy` S is next written (any edit that reaches disk), the writing path (Phase C.3 legacy-migration) MUST classify S to `status: current` before the edit completes, UNLESS Richard explicitly refuses inline classification — in which case S remains `status: legacy` and the edit is written with the minimal frontmatter preserved. The bijection from Property 1 applies to all statuses equally — legacy rows are inventoried without schema enforcement.

**Validates: Requirement 3.1, 4.2, 9.5** (reinterpreted — schema enforcement is status-gated, not universal)

### Property 12: ACTIVATION-LOGGING

*For any* successful `discloseContext` or `kiroPowers activate` call during an agent session, exactly one row is appended to `activation-log.jsonl` with `event: "activated"`, the correct skill/power name, a `request_summary` (≤120 chars), the session id, and the timestamp. The log is append-only: no existing rows are mutated or deleted. Corrections are appended with `event: "correction"` referencing the erroneous row's timestamp.

**Validates: Requirements 6.1, 6.3, 6.4**

### Property 13: SUBAGENT-WRAPPER-REJECTION

*For any* proposed new skill S whose only action is a single `invokeSubAgent` call to an existing subagent with no additional orchestration (no multi-agent pipeline, no pre-/post-processing, no additional tool calls), the Routing Decision Tree MUST reject S (terminate at REJECT with rationale "wraps single subagent; subagent is the correct mechanism"). Skills that orchestrate multiple subagents or multiple MCP tools in sequence ARE permitted.

**Validates: Requirements 10.4, 10.5**

### Property 14: ASSET-LIFECYCLE

*For any* new asset creation C (Phase C), activation-validate (Phase C.4) must succeed before `last_validated` is set and the asset becomes available in sessions. *For any* pruning action P (Phase E) approved by Richard, the archive operation (copy to `~/shared/wiki/agent-created/archive/skills-powers-pruned-{date}/`) must succeed before the delete operation runs. Archive-before-delete is atomic at the row level: if archive fails, delete does not run.

**Validates: Requirements 7.6, 8.2, 8.3**

### Property 15: NON-KIRO-GATE-REJECTION

*For any* workflow W evaluated by the Routing Decision Tree, if an existing non-Kiro mechanism (shell alias, `.bashrc`, cron, git hook, OS-level shortcut, IDE feature, team tool) already handles W or could handle W with trivial effort, the tree terminates at REJECT at step 0.5 with a rationale naming the existing mechanism. The tree does NOT continue to Kiro-mechanism-selection branches for W.

**Validates: Spec-internal routing decision step 0.5; prevents the `dashboard-server.kiro.hook`-style duplication that the subtraction audit catches after the fact.**



---

## Error Handling

Governance errors are handled by surfacing them to Richard, not by automated recovery. Three categories:

**Validator errors (blocking, non-destructive)**:
- Malformed YAML in SKILL.md / POWER.md: parse fails with descriptive error; file is not modified; Richard is told what line failed.
- Missing required fields for `status: current`: validation fails with a list of missing fields; the file stays in its previous state; Richard decides whether to add the fields or revert.
- Path-allowlist violation (Phase C): creation blocks; Richard is told which class / path pair violates and can either adjust the path, re-declare the class, or cancel.

**Advisory findings (non-blocking)**:
- Portability report: emitted, logged, surfaced. No action taken.
- Overlap candidates in the 50%-75% band: surfaced for Richard's review; he decides.

**Race conditions and stale state**:
- Inventory freshness-hash mismatch: agent re-runs Phase A before trusting the inventory.
- Activation-log append concurrency: the file is append-only; parallel appends are serialized via filesystem-level line locking or accepted as benign (event order may interleave but no row is lost).
- Phase C create fails mid-sequence (e.g., write succeeds but activation-validate fails): the file remains on disk with `# validation-failed` comment in the frontmatter; Richard sees the failure and can re-run or delete.

**User-refusal paths (escape hatches)**:
- Legacy asset edit with classification refused (§Phase C.3): the edit is written without migration; asset remains `legacy`. No error, just a logged refusal.
- Pruning review DEFER / PROTECT: recorded in the session transcript; no further action.



---

## Testing Strategy

The testing approach combines unit tests for specific behaviors, property-based tests for universal correctness, and smoke tests for one-time configuration. Property-based testing is appropriate for this spec because most properties are over pure functions (inventory generator, YAML round-trip, stale-set computation, validator report generation, path-allowlist check, routing tree walk) or over filesystem states that can be simulated with temporary directories.

### Dual testing approach

- **Unit tests**: specific examples (wbr-callouts skill generates specific triggers; bridge-sync skill declares Platform_Bound), edge cases (empty description, missing frontmatter, legacy-to-current transition), error conditions (malformed YAML, path-allowlist violation).
- **Property tests**: universal properties (Properties 1-15 above) over randomly generated filesystem states, activation logs, and workflow proposals.
- **Smoke tests**: one-time configuration checks (inventory path exists; routing tree documentation file present; 4 sensitivity tiers and 2 portability tiers defined in the spec).

### Property test configuration

- Minimum 100 iterations per property test.
- Each property test tagged with a comment referencing the design property:
  - Format: `// Feature: skills-powers-adoption, Property {number}: {property_text}`
- Properties 1-15 map to 15 property-based tests (or fewer, where properties collapse into a single broader test).
- Generators:
  - `genFilesystemState` — produces random directory trees with random skill/power files (frontmatter variations, legacy vs current, valid vs malformed).
  - `genActivationLog` — produces append-only JSONL sequences with random event distributions over random time windows.
  - `genWorkflowProposal` — produces random workflow descriptions with random trigger / event / specialist / persistent-state / MCP characteristics.
  - `genSkillBody` — produces random markdown bodies with varying Platform_Bound-indicator token densities.

### Property-test notes per property

- **Property 1 (INVENTORY-BIJECTION)**: generate random filesystem state; run inventory generator; assert bijection. Include edge cases: empty directory, single asset, 100 assets, mixed statuses.
- **Property 2 (STALENESS-CORRECTNESS)**: generate random activation log; run stale-set computation; assert set matches specification. Include edge case: activation exactly 30 days ago.
- **Property 3 (PATH-ALLOWLIST-CORRECTNESS)**: generate random {class, path} pairs; assert validator emits violation iff path outside allowlist. Also assert legacy assets are never rejected by this check.
- **Property 4 (ADVISORY-PORTABILITY-REPORT)**: per F1, the test asserts the validator is a **report-emitting function, not a rejecter**. Generate random skill bodies; assert (a) report is returned containing the detected tokens, (b) the input file is unchanged, (c) no rejection error is raised regardless of declared tier. The test explicitly does NOT assert that Cold_Start_Safe files with Platform_Bound tokens are rejected — that was the earlier-draft behavior removed in revision.
- **Property 5 (INVENTORY-FRESHNESS)**: generate inventory render + subsequent filesystem changes; assert hash mismatch triggers re-render.
- **Property 6 (ROUND-TRIP)**: generate random valid SKILL.md / POWER.md content; assert parse/serialize round-trip produces byte-identical body and structurally-equal frontmatter.
- **Property 7 (NON-SILENT-REWRITE)**: generate random malformed files; assert validator errors AND disk state is unchanged.
- **Property 8 (OVERLAP-CHECK-COMPLETENESS)**: generate random creation proposals; assert overlap-check.json is produced with all required fields.
- **Property 9 (ROUTING-PRECEDES-CREATE)**: generate random create-trigger sequences; assert routing-decision.json exists and its leaf is CREATE-variant whenever Phase C runs.
- **Property 10 (EXTEND-EXISTING-PRECEDENCE)**: generate proposals with varying degrees of overlap to installed assets; assert tree terminates at EXTEND_EXISTING for overlap ≥75%.
- **Property 11 (STATUS-GATED-SCHEMA)**: generate assets with varying status and frontmatter completeness; assert validation behavior matches specification. Include legacy-to-current migration case.
- **Property 12 (ACTIVATION-LOGGING)**: generate random activation sequences; assert exactly one log row per activation, with required fields, append-only. Include `missed-by-feedback` row generation when Richard flags a miss.
- **Property 13 (SUBAGENT-WRAPPER-REJECTION)**: generate proposals; assert single-subagent-wrapper proposals are rejected and multi-agent orchestrations are permitted.
- **Property 14 (ASSET-LIFECYCLE)**: simulate create + prune sequences; assert archive-before-delete and validate-before-available.
- **Property 15 (NON-KIRO-GATE-REJECTION)**: generate workflow proposals with random external-mechanism hits; assert step-0.5 REJECT termination. Include the `dashboard-server.kiro.hook` reference case as an explicit example.

### Library choice

Use a property-based testing library appropriate to the implementation language. If the adoption system's governance tooling is implemented in Python, use `hypothesis`. If in TypeScript, use `fast-check`. If in Rust, use `proptest`. The choice is downstream of this spec — this spec specifies the properties, not the implementation.

### What is NOT property-tested

- Documentation content (tier definitions, path allowlists as prose): specified in §Sensitive-Data Classification Rules and §Portability Tier Rules; verified by human review.
- Richard's manual pruning decisions: not a code path.
- Richard's manual missed-skill flagging: not automated; the `missed-by-feedback` event insertion IS property-tested as part of Property 12 (given a manual flag, the event row appears with the correct fields), but the decision to flag is not.
- Cold-start recovery on a different platform: aspirational; cannot be property-tested without a second platform. The advisory portability validator's report content IS property-tested.

