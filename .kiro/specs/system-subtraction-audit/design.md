# Design Document: System Subtraction Audit

## Overview

This audit produces one human-facing deliverable (`kill-list.md`) and one machine-facing execution log (`execution.log`). Everything else — intermediate JSONs, the spec directory itself — is working state that gets cleaned up when the audit completes (per R14).

**Reading order for the agent executing this audit**: Architecture → Data Model → Classification Decision Tree → Phase Specifications → Output Format → Kill-List Review Syntax → Execution Semantics → Anti-goals.

**Design stance**: This is a procedure, not a product. Nothing about the audit lives on after execution except git history and an archived completion log. No scripts committed to `~/shared/tools/`, no dashboards, no recurring hook. If the procedure needs to run again in 6 months, a future agent re-reads this file and re-executes it.

**Why so thin elsewhere.** The 14 requirements and 17 design constraints already specify the *what*. This design specifies the *how* — the mechanical detail that was deliberately pushed out of requirements per constraint #15. Most of the length is data-model field definitions and the classification decision tree, because those are where the audit's correctness actually lives.

---

## Architecture

Five sequential phases, each producing an intermediate artifact that feeds the next. All intermediates are JSON for machine processing. The only markdown output is the kill-list and the execution log.

```
  Phase 0: PRE-FLIGHT
      |
      | checks: is there an uncompleted prior audit? (R14.3)
      | produces: proceed-or-abort decision
      v
  Phase 1: INVENTORY
      |
      | produces: inventory.json (every file with metadata)
      v
  Phase 2: REFERRER GRAPH + BROKEN REFS
      |
      | consumes: inventory.json
      | produces: referrers.json, broken_refs.json
      v
  Phase 3: DUPLICATION DETECTION
      |
      | consumes: inventory.json, referrers.json
      | produces: duplication_groups.json
      v
  Phase 4: CLASSIFICATION
      |
      | consumes: all prior artifacts
      | produces: classified.json
      v
  Phase 5: RENDER
      |
      | consumes: classified.json
      | produces: kill-list.md (human review)
      v
  --- Richard reviews, edits bulk-approval block ---
      v
  Phase 6: EXECUTION (separate session)
      |
      | consumes: kill-list.md (with approvals), classified.json
      | produces: execution.log (append-only, resumable per R9.6-7)
      v
  Phase 7: ARCHIVE (per R14)
      |
      | deletes: inventory.json, referrers.json, classified.json,
      |          duplication_groups.json, broken_refs.json
      | moves:   spec directory to wiki archive
```

Phase 0 is a safety gate for the re-run lockout rule. Phases 1-5 run in one session and produce the kill-list. Richard reviews asynchronously. Phases 6-7 run in a second session after approval.

**Why 5 generating phases + 2 execution phases** (vs. 4 or 3): the prior design folded broken-ref detection and duplication into a single referrer-graph step. Requirements 2.9, 3, and 8 are separate enough to deserve separate phases with their own artifacts — this makes partial re-runs and debugging tractable. Constraint cost: more files during the run. Benefit: any single phase can be re-run without redoing the others.

---

## Data Model

### `inventory.json` — one entry per file

```json
{
  "generated_at": "2026-04-22T01:30:00-07:00",
  "totals": {
    "body":      {"files": 15, "lines": 3496},
    "protocols": {"files": 30, "lines": 6429},
    "hooks":     {"files": 23, "lines": 0},
    "steering":  {"files": 27, "lines": 0},
    "grand_total_lines": 0
  },
  "files": [
    {
      "path":            "/home/prichwil/shared/context/body/body.md",
      "rel_path":        "~/shared/context/body/body.md",
      "layer":           "body",
      "lines":           88,
      "last_modified":   "2026-04-15T10:22:00-07:00",
      "first_heading":   "# Body — Navigation",
      "purpose_line":    "Navigation layer for the whole system...",
      "purpose_missing": false,
      "empty_shell":     false,
      "inclusion_mode":     null,
      "inclusion_mode_raw": null,
      "is_enabled":         null,
      "auto_generated_candidate": false,
      "symlink_target":  null,
      "prior_session_notes": []
    }
  ],
  "symlinks_followed": [
    {"from": "/home/prichwil/shared", "to": "/shared/user"}
  ]
}
```

**Purpose line rule** (from R1.2): extracted verbatim from the file, layer-aware:
- **Body / Protocol / Wiki-style markdown**: first H1 heading, then first non-heading paragraph. Skip code blocks and frontmatter.
- **Hook (JSON)**: value of the `description` field, then value of the `name` field if description absent.
- **Steering (markdown + frontmatter)**: value of `description` in frontmatter if present, else first H1 heading.

If nothing extractable: `purpose_line` is null and `purpose_missing` is true. Files where `first_heading` matches `/^#\s*(TODO|Placeholder|FIXME)/i` also set `purpose_missing: true` and are treated as likely empty shells (per R12.3).

**inclusion_mode** (steering only, per R13): one of `auto` (always-loaded — when raw value is `always`, `auto`, or frontmatter absent) or `conditional` (when raw value is `manual` or `fileMatch`). Unknown raw values → `inclusion_mode` is null and `needs_revisit: true` is added to the file entry.

**is_enabled** (hooks only): boolean from the JSON `enabled` field. Null for non-hook files.

**empty_shell** (per R12.1): true if (lines - frontmatter_lines) < 10.

**auto_generated_candidate**: true if git log within last 30 days shows ≥5 commits to this file from patterns suggesting automation (bot author, non-interactive commit messages, recurring timestamps). Conservatively false if uncertain.

**prior_session_notes** (per R11.4): populated by reading `~/shared/context/intake/session-log.md` and the last 90 days of `git log` for the file path. Any line mentioning the file gets a one-line note with date. Example: `["2026-04-21: hook disabled (session: Mario audit)"]`.

### `referrers.json` — directed graph

```json
{
  "generated_at": "2026-04-22T01:35:00-07:00",
  "edges": [
    {
      "from":        "~/shared/context/body/body.md",
      "to":          "~/shared/context/body/brain.md",
      "match_type":  "path",
      "line_number": 42,
      "context":     "see #[[file:~/shared/context/body/brain.md]]",
      "from_is_live": true
    }
  ],
  "by_target": {
    "~/shared/context/body/brain.md": {
      "active_path_referrers": 4,
      "latent_referrers":      1,
      "documentation_referrers": 2,
      "name_only_referrers":   0,
      "referrers_detail":      ["~/.kiro/steering/soul.md", "..."],
      "is_orphan":             false,
      "is_load_bearing":       true,
      "circular_cluster_id":   null
    }
  },
  "circular_clusters": [
    {
      "cluster_id": "cc-1",
      "members":    ["~/shared/context/body/X.md", "~/shared/context/body/Y.md"],
      "external_active_referrers": 0,
      "is_cluster_orphan": true
    }
  ]
}
```

**Four match types** (per R2.2):
- `path` — resolvable path reference (includes `#[[file:...]]`, `~/...`, `/home/...`, or any relative path with a `/` directory component) AND `from_is_live: true`.
- `latent` — resolvable path reference AND `from_is_live: false` (the referring file is a disabled hook, a manual/fileMatch steering file, or other non-firing source).
- `documentation` — resolvable path reference in a file inside `~/shared/wiki/**`, `.kiro/specs/**`, or any file named `README.md`, `CHANGELOG.md`, or matching `*-docs.md` / `*-guide.md` patterns. These are citations, not load instructions.
- `name` — bare filename mention without a resolvable path. Informational only.

**from_is_live** rule:
- Hook: `is_enabled: true` → live. Disabled → latent.
- Steering: `inclusion_mode: "auto"` → live. `"conditional"` → latent.
- Body organ / protocol / script: always live if the file itself has an active referrer path (recursive). Orphaned files with references are still live sources of references — the liveness flag only collapses when the referring file is demonstrably not firing during normal operation.

**Orphan rule** (per R2.4, R2.6): `is_orphan: true` when `active_path_referrers == 0` AND not auto-included by steering frontmatter AND not a member of a cluster with external active referrers.

**Circular cluster detection** (R2.6): build the directed graph of path references among inventory files, run Tarjan's strongly-connected-components, and any SCC of size ≥2 whose members collectively have zero external active referrers becomes a `circular_cluster`. Every member gets `is_orphan: true` set in `by_target`.

### `duplication_groups.json`

```json
{
  "groups": [
    {
      "group_id":     "dup-1",
      "shape":        "stem_variant",
      "members":      ["~/.../am-auto.md", "~/.../am-backend.md", "~/.../am-backend-parallel.md"],
      "aggregate_lines": 1264,
      "recommended_survivor": "~/.../am-backend-parallel.md",
      "survivor_rationale": "most recent (Apr 2026), referenced by disabled am-auto.kiro.hook and active eod.kiro.hook"
    },
    {
      "group_id":     "tmpl-1",
      "shape":        "template_plus_instances",
      "template":     "~/.../state-file-engine.md",
      "instances":    ["~/.../state-file-au-ps.md", "~/.../state-file-mx-ps.md", "~/.../state-file-ww-testing.md"],
      "rationale":    "engine is markedly larger (206 lines vs 53-166) and is referenced by all three instances via path"
    },
    {
      "group_id":     "ovl-1",
      "shape":        "heading_overlap",
      "members":      [...],
      "shared_heading_ratio": 0.62,
      "shared_headings": ["Phase 1 — Ingestion", "Phase 5 — Output", ...]
    }
  ]
}
```

**Shape kinds**:
- `stem_variant` — files with shared filename stem and suffix variants (`am-auto`, `am-backend`, `am-backend-parallel`). Duplication candidate → propose one survivor, delete rest.
- `heading_overlap` — files sharing >50% H1/H2 headings. Content-overlap candidate.
- `template_plus_instances` — one member markedly larger (>2x the median) AND cross-referenced by path from smaller members. Per R3.3 this is SCAFFOLDING — do NOT collapse. Template classifies KEEP, instances classify individually.

**Multi-group membership** (R3.6): if a file appears in multiple groups, assigned to the group where collapse yields largest net line reduction. Ties: most recent modification. After assignment, affected groups are re-evaluated; if a group falls below duplication threshold (`heading_overlap < 0.5` or only 1 member left), it dissolves.

### `broken_refs.json` — one entry per broken reference

```json
{
  "by_referrer": {
    "~/.kiro/steering/soul.md": [
      {
        "broken_path": "~/shared/context/body/hard-thing-selection.md",
        "line_number": 104,
        "context":     "Karpathy modifies... hard-thing-selection.md",
        "suggested_action": "update path to ~/shared/context/protocols/hard-thing-selection.md (file exists there)"
      }
    ]
  },
  "total_broken": 1
}
```

Per R8.3 — grouped by referring file, each entry names: broken path, line number, context excerpt, suggested fix (remove, update, or create).

### `classified.json` — one entry per file with recommended action

```json
{
  "files": [
    {
      "rel_path":    "~/shared/context/body/body-diagram.md",
      "layer":       "body",
      "lines":       181,
      "row_id":      "B-D1",
      "action":      "DELETE",
      "category":    "METAPHOR-ONLY",
      "confidence":  "MEDIUM",
      "rationale":   "Exists to complete anatomical framing; fails both workflow tests.",
      "evidence": {
        "active_referrers":      1,
        "latent_referrers":      0,
        "documentation_referrers": 0,
        "referrer_list":         ["~/.../body.md"],
        "duplication_group":     null,
        "circular_cluster":      null,
        "current_usage_test":    "FAILS — no workflow depends on this file; the only cost of deletion is editing body.md to remove the reference",
        "future_workflow_test":  "FAILS — no L3-L5 workflow named that requires this diagram",
        "prior_session_notes":   []
      },
      "blast_radius":       "LOW",
      "default_if_unanswered": null
    }
  ],
  "summary": {
    "delete_count":    0,
    "merge_count":     0,
    "unclear_count":   0,
    "keep_count":      0,
    "karpathy_count":  0,
    "broken_ref_count": 0,
    "estimated_lines_removed": 0,
    "per_layer": {
      "body":      {"delete": 0, "merge": 0, "unclear": 0, "keep": 0},
      "protocols": {"delete": 0, "merge": 0, "unclear": 0, "keep": 0},
      "hooks":     {"delete": 0, "merge": 0, "unclear": 0, "keep": 0},
      "steering":  {"delete": 0, "merge": 0, "unclear": 0, "keep": 0}
    }
  }
}
```

**Required fields by action**:
- `DELETE`: rationale, active-referrer count, confidence (HIGH / MEDIUM / LOW), blast_radius. At least one of: `duplication_group` (as loser), `evidence.circular_cluster`, `evidence.is_orphan`, or `category: METAPHOR-ONLY` / `EMPTY-SHELL`.
- `MERGE`: `merge_target` (rel_path), rationale, `overlap_headings`, confidence.
- `KEEP`: rationale AND one of: `current_usage` (name agent/hook that loads it) OR `future_workflow` (specific L3-L5 workflow).
- `UNCLEAR`: `question_for_richard` (specific answerable question) AND `default_if_unanswered` (action string with time horizon, default 30 days). Per R10.3, if no meaningful default exists, classifier must pick DELETE or KEEP with LOW confidence instead.
- `KARPATHY-FLAG`: `karpathy_observation` (referrer count, line count, last-modified, notable traits). No action field.

Entries missing required fields are tagged `needs_revisit: true` and surface at the top of kill-list.md in an "Incomplete classifications" section — they are NOT silently defaulted to KEEP.

**Row ID format** (per R4.9 — design decision): `{L}-{A}{N}` where:
- `L` = layer letter: `B` (body), `P` (protocols), `H` (hooks), `S` (steering).
- `A` = action letter: `D` (delete), `M` (merge), `U` (unclear), `K` (keep), `X` (karpathy-flag).
- `N` = sequence within that {layer, action} bucket, 1-indexed.

Example: `B-D1` = first body-layer DELETE candidate. `P-M2` = second protocol MERGE candidate. `S-K7` = seventh steering KEEP.

IDs are stable across re-renders of the same `classified.json`. If classification re-runs, IDs may shift — the kill-list header records the `classified.json` hash so mismatches surface.

### `execution.log` — append-only during Phase 6

Line-delimited JSON. One line per row attempted, plus header and footer.

```
{"event":"run_started","run_id":"exec-2026-04-22-01","kill_list_hash":"sha256:...","classified_hash":"sha256:..."}
{"event":"row_started","row_id":"B-D1","action":"DELETE","target":"~/.../body-diagram.md"}
{"event":"row_completed","row_id":"B-D1","action":"DELETE","target":"~/.../body-diagram.md","bytes_removed":6421,"timestamp":"2026-04-22T02:15:04-07:00"}
{"event":"row_skipped","row_id":"P-D3","reason":"blocked on referrer resolution","unresolved_referrers":["~/.../some-hook.hook"]}
{"event":"row_stopped","row_id":"P-M2","reason":"merge conflict between source and target","conflict_headings":["Phase 2"]}
{"event":"broken_ref_fixed","referrer":"~/.kiro/steering/soul.md","old_path":"~/.../hard-thing-selection.md","new_path":"~/.../protocols/hard-thing-selection.md"}
{"event":"run_interrupted","reason":"network_timeout","completed_count":17,"pending_count":23}
{"event":"run_resumed","run_id":"exec-2026-04-22-01","resume_from_row":"B-D18"}
{"event":"run_completed","completed_count":38,"skipped_count":2,"stopped_count":1,"broken_refs_fixed":3}
```

**Resume protocol** (per R9.6):
- On startup, check if `execution.log` exists and ends with `run_interrupted` or lacks `run_completed`.
- If so, emit `run_resumed` with the original `run_id`, read all prior `row_completed` / `row_stopped` events, build a skip-set of their `row_id` values.
- Continue from the first row in `classified.json` not in the skip-set.
- If the `kill_list_hash` or `classified_hash` mismatches (per R9.5 — stale state), STOP and require user intervention.

**Idempotence**: a second run with identical inputs and no interruption produces zero `row_started` events (all rows already in the skip-set) and emits only `run_started` + `run_completed{completed_count:0}`.

---

## Classification Decision Tree

Every file walks this tree in order. First matching branch wins. The tree order reflects R3.3 (template + instances detection BEFORE general duplication) and R5.6 (auto-included-referrer check BEFORE simple DELETE).

```
  START: file F with active_referrer_count R, layer L, inclusion context I
       |
       v
  1. Is F a karpathy-protected file?
       (heart.md, gut.md, hard-thing-selection.md, any file under
        ~/shared/context/experiments/ matching experiment queue)
       YES -> KARPATHY-FLAG, record observation, stop.
       NO -> continue.
       |
       v
  2. Is F an EMPTY-SHELL (per R12)? (lines - frontmatter < 10, or
     first-heading matches /TODO|Placeholder|FIXME/i)
       YES -> DELETE, category=EMPTY-SHELL, confidence=HIGH.
              Note blast radius if any active referrers. Stop.
       NO -> continue.
       |
       v
  3. Is F a member of a template_plus_instances duplication group?
       YES if F is the template -> category=SCAFFOLDING, continue to
            per-layer subtree (will classify KEEP unless instances
            prove the template unused).
       YES if F is an instance -> continue to per-layer subtree as
            INHABITANT, evaluated individually.
       NO -> continue.
       |
       v
  4. Is F a loser in a stem_variant or heading_overlap duplication
     group (not the designated survivor)?
       YES -> DELETE, rationale "duplicate of <survivor>", confidence=HIGH,
              impact note lists referrers that need to move to survivor.
              Stop.
       NO -> continue.
       |
       v
  5. Is F in a circular-orphan cluster (per R2.6)?
       YES -> DELETE, rationale "member of circular-orphan cluster
              cc-N with no external active referrers", confidence=HIGH.
              Stop.
       NO -> continue.
       |
       v
  6. Is F referenced by an always-auto-included steering file via
     path (per R5.6)?
       YES -> UNCLEAR with default KEEP and note "coordinated removal
              requires separate spec; this audit cannot safely delete
              in a single row". Stop.
       NO -> continue.
       |
       v
  7. Is R (active path referrers) == 0 AND F not itself auto-included
     by steering frontmatter?
       YES -> DELETE, rationale "orphaned, zero active referrers",
              confidence=HIGH (if zero across all match types) or
              MEDIUM (if latent/documentation referrers exist but
              none active). Stop.
       NO -> continue.
       |
       v
  8. Dispatch by layer:
       body     -> Body Classification Sub-tree
       protocol -> Protocol Classification Sub-tree
       hook     -> Hook Classification Sub-tree
       steering -> Steering Classification Sub-tree
       unknown  -> UNCLEAR with question "file layer not recognized",
                   default KEEP.
```

### Body Classification Sub-tree

```
  Body file B
       |
       v
  B1. Apply Current Usage Test (WORKFLOW DEPENDENCY, per R5.4):
      "If B were deleted tomorrow, what current WORKFLOW (agent run,
       hook execution, protocol step) would fail or degrade?"

      A broken reference that can be fixed by editing 1-2 lines in
      a referrer does NOT count as a workflow failure. Only a
      workflow stopping counts.

      PASSES (workflow named) -> category=INFORMATION, continue to B3.
      FAILS -> continue to B2.
       |
       v
  B2. Apply Future Workflow Test (per R5.5):
      "If B were deleted tomorrow, what specific L3-L5 agentic
       workflow would have to rebuild equivalent structure?
       Name the workflow with its L-tier prefix."

      Acceptable: "L3: team tool-adoption tracker reads this ledger"
      Not acceptable: "future agents might need this"

      PASSES -> category=SCAFFOLDING, continue to B3.
      FAILS -> category=METAPHOR-ONLY, action=DELETE, confidence=MEDIUM.
               Stop.
       |
       v
  B3. Is B load-bearing (3+ active path referrers)?
      YES -> action=KEEP, blast_radius=HIGH, note LOAD-BEARING.
      NO  -> action=KEEP, blast_radius=LOW.
      Stop.
```

### Protocol Classification Sub-tree

```
  Protocol file P (reached here means not in duplication/karpathy/shell)
       |
       v
  P1. Does any ACTIVE referrer (enabled hook or live protocol/agent)
      reference P by path?
      YES -> action=KEEP, rationale names the live referrer.
             blast_radius=HIGH if 3+ active referrers, else LOW.
             Continue to P3 for SCAFFOLDING check.
      NO  -> continue to P2.
       |
       v
  P2. Apply Protocol Future Workflow Test:
      "Is P a parameterizable pattern that a specific L3-L5
       workflow will instantiate?" (Template of a template_plus_
       instances group automatically passes if reached here.)

      PASSES -> category=SCAFFOLDING, action=KEEP, name the workflow.
      FAILS -> action=DELETE, rationale "no active referrer, no named
               future workflow", confidence=MEDIUM.
      Stop.
       |
       v
  P3. (reached from P1=YES) Is P also SCAFFOLDING for a named future
      workflow beyond its current consumer?
      YES -> note SCAFFOLDING status in rationale.
      NO  -> keep rationale as current-usage only.
      Stop.
```

### Hook Classification Sub-tree

```
  Hook file H (JSON .hook file)
       |
       v
  H1. Is `enabled` true?
      NO -> does the description contain a dated rationale for
            disablement matching /DISABLED \d{4}-\d{2}-\d{2}/?
            YES -> action=KEEP, rationale "intentionally disabled,
                   preserved for documented reason". Note the date.
            NO  -> action=UNCLEAR, question "disabled hook with no
                   dated rationale — delete or document the reason?",
                   default=DELETE after 30 days. Stop.
      YES -> continue to H2.
       |
       v
  H2. Does H fire on promptSubmit?
      YES -> continue to H3 (scrutinize — every-chat tax).
      NO  -> continue to H4.
       |
       v
  H3. Does the promptSubmit hook produce conditional output
      (skips silently when nothing to report)?
      YES -> action=KEEP, rationale notes every-chat fire + conditional.
             blast_radius annotates "runs every chat".
      NO  -> action=UNCLEAR, question "unconditional output on every
             chat — is this tax justified?", default=DELETE after 30d.
      Stop.
       |
       v
  H4. Is H a scheduled/event hook whose job duplicates another
      enabled hook?
      YES -> action=DELETE if H is less-used of the pair (fewer
             active referrers to its protocol), else H survives and
             the other becomes DELETE. Confidence=MEDIUM.
      NO  -> action=KEEP, default.
      Stop.
```

### Steering Classification Sub-tree

```
  Steering file S
       |
       v
  S1. Parse frontmatter. Determine inclusion_mode per R13:
      raw value in {"always","auto"} OR frontmatter absent -> "auto"
      raw value in {"manual","fileMatch"}                  -> "conditional"
      raw value anything else                              -> UNKNOWN
       |
       v
  S2. Is inclusion_mode UNKNOWN?
      YES -> tag needs_revisit=true, action=UNCLEAR,
             question "unknown inclusion value '<raw>' — normalize
             or update audit",  default=KEEP. Stop.
      NO  -> continue.
       |
       v
  S3. Is inclusion_mode = "auto"? (loaded every chat)
      YES -> continue to S4 (high scrutiny — taxes every chat).
      NO  -> continue to S5.
       |
       v
  S4. Does S contain rules the agent must follow in every
      interaction (identity, file-creation, environment, always-
      applicable guardrails)?
      YES -> action=KEEP, rationale "auto-loaded, universally needed".
      NO  -> action=UNCLEAR, question "auto-included but not
             universally needed — should this be conditional or
             manual?", default=KEEP (safer than silent deletion of
             a loaded file). Stop.
       |
       v
  S5. (conditional steering) Is S actively invoked by any agent,
      workflow, or fileMatch pattern that fires in practice?
      YES -> action=KEEP.
      NO  -> action=DELETE as orphan, confidence=MEDIUM (might be
             referenced by something outside our search scope —
             see R2.10 disclosure).
      Stop.
```

---

## Phase Specifications

### Phase 0: Pre-Flight (~1 min)

**Inputs**: filesystem state of spec directory, user intent.

**Procedure**:
1. Ask once (if not pre-specified by Richard): **FULL-PASS** or **SCRAPPY-PASS**?
   - FULL-PASS — run the complete spec (Phases 1-7 with all acceptance criteria). ~90 min generating + Richard review + ~30-60 min executing.
   - SCRAPPY-PASS — run a reduced Phase 1 (inventory only, no layer-aware purpose extraction, no prior-session notes) + reduced Phase 4 (orphan/duplicate detection only, skip workflow-dependency tests) + render a provisional kill-list that's 3-5 sections instead of 4 layers × 4 actions. ~30 min generating. Kill-list is reviewed but NOT executed — findings feed back into this spec and upgrade the next run.
   
   SCRAPPY-PASS is the Peter-ethos option: run something today, learn from what surfaces, decide if further rigor is needed. FULL-PASS is the Mario-ethos option: the thing is worth doing right the first time because execution is hard to reverse. Default: ask Richard. For one-shot execution against production context files, FULL-PASS is usually correct; for the first-ever run where Richard wants to see what the audit produces before committing, SCRAPPY-PASS is the bet-reducing move.

2. Check for `.kiro/specs/system-subtraction-audit/kill-list.md`. If exists, check for `execution.log`.
   - If `kill-list.md` exists AND `execution.log` does not exist OR doesn't end with `run_completed` → ABORT with message: "Uncompleted prior audit detected. Complete its execution or explicitly discard artifacts before starting a new audit (per R14.3)."
   - Otherwise → proceed.
3. Read `~/.kiro/steering/soul.md` to snapshot the karpathy-protected file list. Cache this snapshot for the whole run; per R5 any mid-run edits to soul.md are ignored.
4. Compute current `soul.md` hash and store in `preflight.json` for reference.
5. Record `pass_mode: "FULL" | "SCRAPPY"` in `preflight.json`.

**Tools**: `readFile`, `fileSearch`.

### Phase 1: Inventory (~10 min)

**Inputs**: the four target directories.

**Procedure**:
1. For each target directory, enumerate every file.
2. For each file collect: path, rel_path, layer, lines (`wc -l`), last_modified (`stat -c %y`), first_heading (regex on first 30 lines), purpose_line (layer-aware extraction — see Data Model).
3. Parse steering frontmatter into `inclusion_mode` + `inclusion_mode_raw`.
4. Parse hook JSON into `is_enabled`.
5. Detect EMPTY-SHELL: count non-frontmatter lines, set `empty_shell: true` if < 10.
6. Detect auto-generated candidates: `git log --oneline --since="30 days ago" -- <file>` — if ≥5 commits with non-interactive patterns, set `auto_generated_candidate: true`.
7. Populate `prior_session_notes` by grepping `~/shared/context/intake/session-log.md` for the filename and extracting `git log --pretty=format:'%as: %s' --since="90 days ago" -- <file>`.
8. Follow symlinks once (max depth 1); record in `symlinks_followed` array. Reject recursion.
9. Compute per-layer totals and grand total.
10. Write `inventory.json`.

**Tools**: `listDirectory`, `executeBash` (`wc -l`, `stat`, `git log`), `readFile`, `grepSearch`.

**Failure mode**: empty directory → record `"files": []` for that layer. Stat failure on single file → log and continue; don't abort phase.

### Phase 2: Referrer Graph + Broken Refs (~15 min)

**Inputs**: `inventory.json`.

**Procedure**:
1. For each file F in inventory, build a search pattern for its rel_path, its absolute path, and its `#[[file:...]]` form.
2. Run `grepSearch` across the scoped corpus (R2.8): `~/.kiro/**`, `~/shared/context/**`, `~/shared/wiki/**`, `~/shared/tools/**`, `~/shared/scripts/**`, `~/shared/dashboards/**`.
3. For each hit, determine `match_type`:
   - Referring file is inside `~/shared/wiki/**`, `.kiro/specs/**`, or matches `README.md|CHANGELOG.md|*-docs.md|*-guide.md` → `documentation`.
   - Referring file is a disabled hook (`is_enabled: false`) or conditional steering (`inclusion_mode: "conditional"`) → `latent`.
   - Resolvable path, from a live file → `path` (active).
   - Otherwise if bare filename without path context → `name`.
4. Resolve every path reference against the filesystem. If the target doesn't exist, record in `broken_refs.json` with referrer, line number, context, and suggested_action (heuristics: if filename exists elsewhere, suggest path update; else suggest remove-or-create).
5. Build `by_target` aggregation with counts per match type.
6. Detect circular clusters: build directed graph of active path references among inventory files. Run SCC (Tarjan's or Kosaraju's). For each SCC of size ≥2, check if any member has an active path referrer from OUTSIDE the SCC. If no → tag all members with `circular_cluster_id` and set `is_cluster_orphan: true`.
7. Write `referrers.json` and `broken_refs.json`.

**Tools**: `grepSearch`, `fileSearch`, `executeBash` (filesystem resolution).

**Efficiency**: ~95 inventory files × ~3 search variants = ~285 grep runs. Use basename-filtering to scope each search.

### Phase 3: Duplication Detection (~10 min)

**Inputs**: `inventory.json`, `referrers.json`.

**Procedure**:
1. Group files by filename stem (everything before the last `.` minus known variant suffixes: `-v2`, `-new`, `-parallel`, `-old`, `-draft`). Groups of 2+ are `stem_variant` candidates.
2. For each stem_variant group, check for template_plus_instances shape: find the largest member (by lines). If largest is ≥2x the median of the group AND at least one smaller member has a path referrer to the largest → promote to `template_plus_instances` shape.
3. For remaining candidates, extract H1/H2 headings from first 100 lines of each file. Compute pairwise heading-overlap ratio = |shared| / max(|h_a|, |h_b|). Pairs with ratio >0.5 form `heading_overlap` groups.
4. For stem_variant and heading_overlap groups (but NOT template_plus_instances): designate a survivor using the rule in R3: most recently modified AND most active referrers (weighted equally, break ties with lines).
5. Multi-group resolution: if a file is in 2+ groups, assign to the group where `(aggregate_lines_of_losers)` is largest (= most savings). Re-evaluate affected groups after assignment; if any drops below threshold, dissolve.
6. Write `duplication_groups.json`.

**Tools**: `readFile`, `executeBash`.

### Phase 4: Classification (~20 min)

**Inputs**: `inventory.json`, `referrers.json`, `duplication_groups.json`, `preflight.json`.

**Procedure**:
1. For each file, walk the Classification Decision Tree. Record terminating node as action + category + confidence.
2. Build classified entry with ALL required fields per Data Model. Entries missing required fields get `needs_revisit: true`.
3. Body layer: record both current-usage-test and future-workflow-test results on every body organ, even if first test passed (per R5.4).
4. Karpathy files: skip action, record observation with referrer counts.
5. Assign row_id: sort by (layer, action, sequence) and apply the `{L}-{A}{N}` scheme.
6. Compute summary counts per layer and overall.
7. Hash `classified.json` (sha256) for the kill-list header.
8. Write `classified.json`.

**Tools**: `readFile` (verify workflow claims against file content), `grepSearch` (verify live-referrer claims).

**The discipline gate**: if the classifier cannot name a specific L3-L5 workflow or active referrer for a KEEP, the required field is null and `needs_revisit: true`. No silent hedging.

### Phase 5: Render (~10 min)

**Inputs**: `classified.json`, `broken_refs.json`.

**Procedure**: write `kill-list.md` per the Output Format section. Include: summary header, bulk-approval block template, per-layer chunks with rows sorted by action then confidence, broken-references section, karpathy section, duplication-group summary table, incomplete-classifications section (if any).

**Tools**: `fsWrite`.

### Phase 6: Execution (separate session, ~30-60 min)

**Inputs**: `kill-list.md` (with Richard's edits), `classified.json`.

**Procedure**:
1. Parse kill-list bulk-approval block and per-row overrides. Build approved-set.
2. Emit `run_started` with hashes of kill-list and classified.json.
3. Topologically sort approved-set by referrer dependency: leaves (zero path referrers) first, load-bearing files last.
4. For each row in order:
   - If already in skip-set from prior resume → skip silently.
   - If row is load-bearing DELETE with any UNCLEAR/un-approved referrer → emit `row_skipped{reason:"blocked on referrer resolution"}`.
   - If row is MERGE → atomic sequence per R9.4. On conflict, emit `row_stopped`.
   - If row is DELETE → emit `row_started`, delete file, emit `row_completed`.
   - If row updates a referrer (part of coordinated load-bearing deletion) → edit the referrer to remove the reference, emit `row_completed`.
5. Apply broken-reference fixes per the `suggested_action` in broken_refs.json (unless Richard vetoed them in the kill-list).
6. Emit `run_completed` with totals.

**Resumption**: if `execution.log` ends with `run_interrupted` or abruptly, restart from first row not in skip-set (per Data Model resume protocol).

**Tools**: `deleteFile`, `strReplace` / `fsWrite` (for referrer updates and merges), `executeBash` (git diff / commit).

### Phase 7: Archive (after Phase 6 completes, ~2 min)

**Inputs**: spec directory state.

**Procedure** (per R14):
1. Verify `execution.log` ends with `run_completed`.
2. Delete intermediate JSONs: `preflight.json`, `inventory.json`, `referrers.json`, `broken_refs.json`, `duplication_groups.json`, `classified.json`.
3. Move spec directory: `mv .kiro/specs/system-subtraction-audit ~/shared/wiki/agent-created/archive/system-subtraction-audit-{YYYY-MM-DD}/` — where the date is the execution date.
4. The archive contains: `requirements.md` (final), `design.md` (final), `kill-list.md` (with Richard's approvals intact), `execution.log` (the completion record). That's the durable record.
5. Commit the archive move + all file deletions in a single git commit with message `audit: system-subtraction-audit completed {date}`.

**Tools**: `deleteFile`, `executeBash` (`mv`, `git commit`).

---

## Output Format: `kill-list.md`

```markdown
# Kill List — System Subtraction Audit

**Generated**: 2026-04-22T02:00:00-07:00
**classified.json hash**: sha256:abc123...
**Files reviewed**: 95 across 4 layers
**Unsearched reference sources** (per R2.10): DuckDB rows, Asana task descriptions, Slack messages, Outlook emails. A file referenced only by these sources will appear orphaned in this audit.

## Summary

**Per-layer**:
| Layer     | Files | DELETE | MERGE | UNCLEAR | KEEP | KARPATHY |
|-----------|-------|--------|-------|---------|------|----------|
| body      | 15    | 3      | 0     | 2       | 7    | 3        |
| protocols | 30    | 8      | 2     | 3       | 16   | 1        |
| hooks     | 23    | 2      | 0     | 1       | 20   | 0        |
| steering  | 27    | 0      | 0     | 2       | 25   | 0        |

**Aggregate**:
- DELETE: 13 files (~1,840 lines)
- MERGE:  2 files (~380 lines absorbed)
- UNCLEAR: 8 files (defaults applied after 30 days)
- KEEP: 68 files
- KARPATHY-FLAG: 4 (for karpathy review, no recommendation)
- BROKEN REFS: 3 (fix separately)

**If all DELETE + MERGE approved**: ~2,220 lines removed, ~23% of current surface.

---

## Bulk Approval Block

Edit this block to approve, veto, or defer rows in bulk. The executor only acts on rows with an explicit APPROVE entry here or an inline APPROVED tag on the row.

Syntax:
- `APPROVE: B-D1, B-D3, P-D1-P-D5, H-D1`  (individual IDs or ranges)
- `VETO: P-D3`  (block specific rows even if ranged-approved above)
- `DEFER: U1, U3`  (explicitly carry to next cycle — suppresses default-if-unanswered countdown)

Absence of a row from this block is NOT approval. Unapproved rows are skipped.

```text
APPROVE:
VETO:
DEFER:
```

---

## How to use this file

1. Read top-to-bottom. Each row is one file with a recommended action.
2. To approve rows, add their IDs to the `APPROVE:` line in the block above.
3. To block a specific row inside an approved range, add its ID to `VETO:`.
4. To punt on an UNCLEAR (suppress its default-if-unanswered), add its ID to `DEFER:`.
5. Rows you don't address remain in the kill-list for the next cycle.
6. The executor reads this file and parses the block. It never infers approval from absence of veto.

---

## Incomplete classifications

*(empty unless some file had required-fields missing — these must be resolved before execution)*

---

## Broken references to fix (not audit candidates)

### ~/.kiro/steering/soul.md
- Line 104: references `~/shared/context/body/hard-thing-selection.md` — file doesn't exist at this path.
  - Suggested: update to `~/shared/context/protocols/hard-thing-selection.md` (file exists there, 404 lines).

---

## Body layer (15 files)

### DELETE — body layer

#### B-D1. `~/shared/context/body/body-diagram.md`  [181 lines, METAPHOR-ONLY, MEDIUM confidence]
- **Rationale**: Exists to complete anatomical framing; fails both workflow tests.
- **Active referrers**: 1 (body.md)
- **Current usage test**: FAILS — no workflow depends on this file; only body.md references it for self-documentation.
- **Future workflow test**: FAILS — no L3-L5 workflow named.
- **Blast radius**: LOW — only body.md needs a 1-line edit to remove the reference.

*(... each DELETE row follows this format ...)*

### MERGE — body layer

*(empty or MERGE rows if any)*

### UNCLEAR — body layer

#### B-U1. `~/shared/context/body/body.md`  [88 lines, LOAD-BEARING via soul.md auto-include]
- **Question**: body.md's role is navigation (metaphor-only) but soul.md auto-loads it. Approve coordinated removal via separate spec, or keep as-is?
- **Default if unanswered (30 days)**: KEEP — per R5.6, coordinated removal requires a separate spec; this audit cannot safely delete single-row.
- **Prior session notes**: 2026-04-21 Mario/pi audit flagged body metaphor as transition-tool not permanent structure.

### KEEP — body layer

#### B-K1. `~/shared/context/body/memory.md`  [246 lines, INFORMATION]
- **Rationale**: Relationship graph used in every drafted communication per soul.md #6.
- **Current usage**: 4 agents load by path (callout-writer, callout-reviewer, coach, wiki-writer).
- **Future workflow**: L3 contact-routing workflow will inhabit the same graph.

*(... etc ...)*

---

## Protocols layer (30 files)

*(same structure: DELETE → MERGE → UNCLEAR → KEEP sub-sections, priority-sorted within each)*

---

## Hooks layer (23 files)

*(same)*

---

## Steering layer (27 files)

*(same)*

---

## For karpathy review (4 files, no recommendation)

- `~/shared/context/body/heart.md` — 312 lines, 2 active path referrers, last modified 2026-04-18. Observation: referenced from soul.md routing table.
- `~/shared/context/body/gut.md` — 181 lines, 1 active path referrer, last modified 2026-04-17.
- `~/shared/context/protocols/hard-thing-selection.md` — 404 lines, 0 active path referrers, last modified 2026-03-24. Observation: large protocol with no active consumer — may have been superseded or not yet wired up.
- `~/shared/context/experiments/experiment-log.tsv` — *(if present)* the karpathy experiment queue.

---

## Duplication groups

| ID    | Shape                    | Members | Total lines | Survivor | Net loss | Row IDs |
|-------|--------------------------|---------|-------------|----------|----------|---------|
| dup-1 | stem_variant             | am-auto.md, am-backend.md, am-backend-parallel.md | 1,264 | am-backend-parallel.md | ~656 lines | P-D1, P-D2 |
| tmpl-1 | template_plus_instances | state-file-engine.md (tmpl), state-file-au-ps.md, state-file-mx-ps.md, state-file-ww-testing.md | 479 | NOT COLLAPSED — all KEEP | 0 | — |
| ovl-1 | heading_overlap          | slack-conversation-intelligence.md, slack-history-backfill.md | 339 | *TBD during classification* | TBD | P-D3? |
```

**Format discipline**: plain-text markdown, readable in `less`. No YAML in the output, no embedded JSON. Richard edits the Bulk Approval block with a text editor. The executor parses the block with a strict regex (documented in Phase 6).

---

## Kill-List Review Syntax

This section specifies the exact syntax the executor parses. Richard reads this ONCE at the top of kill-list.md; the executor enforces it.

### Bulk Approval Block Grammar

Block delimited by a fenced code block tagged `text` immediately after the `## Bulk Approval Block` heading. Inside the block:

```
APPROVE: <id-or-range>[, <id-or-range>]*
VETO:    <id>[, <id>]*
DEFER:   <id>[, <id>]*
```

Each line is optional. Empty values (just `APPROVE:`) mean no approvals.

**Range syntax**: `B-D1-B-D5` means `B-D1, B-D2, B-D3, B-D4, B-D5` (inclusive, same {layer, action} bucket). Ranges across different buckets are invalid and parsed as literal strings → no match → effective no-op.

**Precedence**: VETO overrides APPROVE. DEFER overrides both (a deferred row is never executed this cycle).

**Row ID format**: `{L}-{A}{N}` where:
- `L` ∈ {B, P, H, S} (body / protocol / hook / steering)
- `A` ∈ {D, M, U, K, X} (delete / merge / unclear / keep / karpathy)
- `N` = 1-indexed sequence number within that bucket.

IDs are stable for a given `classified.json` hash. The kill-list header includes this hash. If Richard edits `classified.json` or re-runs classification, IDs may shift — the executor detects hash mismatch and stops.

### Inline Approval Fallback

If Richard prefers row-by-row editing, he can add `APPROVED` to the end of a row's header line:

```
#### B-D1. `~/.../body-diagram.md`  [181 lines, METAPHOR-ONLY, MEDIUM confidence]  APPROVED
```

The executor accepts this as equivalent to listing `B-D1` under `APPROVE:` in the block. Useful for one-off approvals without touching the block.

### Parser Behavior

- Unrecognized tokens in the bulk block → logged, ignored. Not an error.
- Row ID referencing a non-existent row → logged, skipped.
- A row appearing in both APPROVE and VETO → VETO wins.
- A row appearing in both APPROVE and DEFER → DEFER wins.

---

## Execution Semantics

Per R9 + R16 — these are the executor's guarantees:

1. **Explicit approval only** (R9.1). Executor reads the bulk block + inline APPROVED tags. Silence is never approval.
2. **Dependency order** (R9.2). Topological sort over active path-referrer graph: leaves first. Load-bearing DELETE approved alongside its referrer's edits → both happen in the same execution session.
3. **Load-bearing with unresolved referrer** (R9.3). DELETE row is skipped (logged as blocked), not force-executed.
4. **Atomic MERGE** (R9.4). Read source → diff against target → append unique content under a clearly-marked `## Absorbed from {source}` heading → delete source. On content conflict (same heading with different body), STOP that row and flag manual review. Don't guess.
5. **State freshness check** (R9.5). Before acting on a row, re-read target file and referrers. If a new active referrer appeared since classification (someone else edited the system), skip and log for next cycle.
6. **Resumability** (R9.6, R16). Execution log is append-only line-JSON. On restart: read log, build skip-set of `row_completed` and `row_stopped` IDs, resume from first unprocessed. Hash check prevents resuming against a modified kill-list.
7. **Idempotence**. Re-running against an unchanged kill-list with a complete log is a no-op: `run_started` + `run_completed{completed_count: 0}`.

### Merge Content Preservation Detail

Per R9.4 step (b) — "identify content in source that is not present in target":

1. Parse both files into sections by H1/H2 headings.
2. For each section in source:
   - If target has a section with the same heading and matching body (normalized whitespace) → skip (already present).
   - If target has a section with the same heading but DIFFERENT body → CONFLICT. Stop this row.
   - If target has no such section → queue for append.
3. Append queued sections to target under a clearly-marked divider:
   ```
   ---
   ## Absorbed from {source_rel_path} on {date}
   
   {queued sections verbatim}
   ```
4. Delete source.

Content outside sections (top-of-file preamble) is appended in a separate `## Preamble from {source}` section rather than merged into target's preamble (avoids mangling).

### Dependency-Ordered Deletion Detail

Per R9.2 — topological sort:

1. Build directed graph of active path-referrers among APPROVED DELETE rows.
2. Kahn's algorithm: repeatedly find a row with zero unprocessed referrers among the APPROVED set, emit it, remove from graph.
3. If a cycle remains (impossible if circular-orphan cluster detection worked, but defensive), stop and flag. Circular clusters approved for deletion are handled by deleting all members in a single sweep, since no outside referrer depends on any of them.
4. For each emitted row, if it has referrers that are themselves approved-for-edit (referrer updates), apply those edits first, then delete the target.

---

## Design Decisions and Rationale

### Why 5 generating phases + 2 execution phases (vs. 4-phase original)

Prior design combined broken-ref detection and duplication into the referrer phase. R2.9, R3, and R8 are orthogonal concerns that deserve separate phases — broken-ref detection is independent of duplication grouping, and a failure in one shouldn't block the other. Cost: more JSON files during a run. Benefit: partial re-runs are tractable.

### Why JSON intermediate + markdown final + JSON log

Three artifact kinds, three purposes:
- **JSON intermediates** (inventory/referrers/duplication/classified): procedures consume them. Machine-processable, sortable, joinable.
- **Markdown kill-list**: Richard consumes it. Linear, editable, readable in `less` or any text editor.
- **JSON log** (execution.log): append-only, line-delimited, resume-safe. Not read by humans during normal operation.

Mixing formats in the wrong place is the anti-pattern Mario called out. Each format serves its consumer.

### Why row IDs use `{L}-{A}{N}` format

Alternatives considered:
- Sequential integers (1, 2, 3): no indication of layer or action; Richard can't tell at a glance what `Row 42` means.
- Hash IDs (`B-d1a8`): stable across re-runs but unreadable.
- Filename-based: too long and breaks when files are renamed.

`B-D1` is unambiguous, stable for a given classification, short enough for range syntax (`B-D1-B-D5`), and readable. Layer letters match the four-section chunking in the kill-list so Richard's eye tracks naturally.

### Why the decision tree checks template_plus_instances before regular duplication

The prior design had duplication as step 2 and scaffolding as part of the body sub-tree. That meant `state-file-au-ps.md` would get DELETEd as a duplicate of `state-file-engine.md` before the template rule could protect the instances. Swapping the order costs nothing and preserves scaffolding.

### Why auto-included-steering-referrer → UNCLEAR (not DELETE)

Per R5.6 — the cost of deleting a file referenced from always-loaded steering isn't just "edit 1 line in soul.md." soul.md is the agent identity file. Edits there require care, testing, and potentially coordinated changes to every agent that loads it. That's bigger than a kill-list row. The UNCLEAR classification with KEEP default forces Richard to elevate to a separate coordinated-removal spec if he wants to proceed. This is the discipline that keeps the audit from causing self-inflicted identity damage.

### Why the executor never infers approval from silence

Per R9.1 + constraint #11. The failure mode from implicit approval is catastrophic: Richard reviews 60 of 95 rows, gets interrupted, the executor runs the "approved" rows (= everything he didn't veto) and deletes 35 files he never saw. Explicit APPROVE is the only safe default. Cost: Richard must actively approve every row he wants deleted. Benefit: no file dies without his sign-off.

### Why merges stop on content conflict

Per R9.4 — if the source and target have sections with the same heading but different bodies, that's a *semantic* conflict. The executor can't know which version is canonical. Stopping and flagging is the safe option. Automated resolution here is the kind of agent-guessing that Mario's critique is entirely about.

### Why archive to `shared/wiki/agent-created/archive/` not just delete

Per R14 — the audit's artifacts are history. Deleting them loses the record of what was decided and why. Archiving them to wiki/archive/ preserves the kill-list (with Richard's approvals intact) and the execution log as a durable decision record. Git history captures file deletions; the archive captures reasoning. Future audits can look back at prior kill-lists to see what was kept, what was cut, and whether any kept-for-scaffolding files eventually earned their keep.

### Why the design carries both Mario and Peter's fingerprints

This design was written under the influence of two philosophies: Mario's (cut the slop, rigor before execution, read the critical code) and Peter Steinberger's (iterate in small steps, extensions over forks, the first version is never the final one). They disagree on how much spec-up-front is healthy. They agree on the things that matter more: taste, saying no, system design, humans as the bottleneck.

The audit is deliberately Mario-shaped because it's a one-shot cleanup with hard-to-reverse deletions — that's the situation where rigor pays. But Phase 0 now offers SCRAPPY-PASS as a Peter-option, because even a rigorous design should let the operator choose a lower-commitment first run if they want to learn before committing. Open question #7 names the Peter follow-on: the long-term structural answer is extension-first, not recurring audits.

See `.kiro/steering/mario-peter-dichotomy.md` (manual-include) for the full framework on when to apply which ethos.

### Why no recurring hook or dashboard

Per constraint #17 + Mario's critique applied recursively. If this audit becomes a scheduled job, it accumulates its own artifacts every run. Every kill-list becomes complexity. The right cadence is human-triggered: Richard runs it when the system feels bloated, executes the result, archives it, forgets about it until the next bloat. One-shot procedure, every time.

The Peter-ethos counterpoint is also load-bearing here: recurring audits are a *symptom* of the real problem, which is that the surviving files are always-loaded instead of extension-loaded. A system where context loads on-demand doesn't need periodic cleanup. That's the target state. This audit is the transition.

---

## Anti-goals (explicit)

1. **Not an ongoing audit service**. One-shot procedure. No recurring hook, no scheduled job, no dashboard view. If re-run: manual invocation, archive prior, start fresh.
2. **Not a refactor**. Surviving files keep their current names, structure, content, and frontmatter. Only deletions and targeted merges.
3. **Not a tooling project**. No scripts committed to `~/shared/tools/`. The procedure is the design doc; the agent re-reads it and executes.
4. **Not a dashboard**. Flat markdown, readable in a terminal. No HTML, no charts, no visualization.
5. **Not karpathy's job**. Karpathy-protected files are flagged-only, routed separately.
6. **Not a rename exercise**. Surviving files keep names. Cosmetic changes fail constraint #2.
7. **Not a DuckDB-aware audit**. References inside DuckDB rows, Asana task descriptions, Slack messages, and Outlook emails are out of search scope (R2.10). Richard is told this explicitly so a file referenced only by those sources appearing orphaned doesn't cause surprise deletions.
8. **Not autonomous**. Every DELETE requires explicit human approval. No file dies because Richard was silent.
9. **Not a complexity product**. The audit's own artifacts are transient. Only git history + archived kill-list + archived execution log survive.

---

## Open Implementation Questions

These surfaced during design and need either Richard's call or a small experiment:

1. **Karpathy experiment queue location**. soul.md routes heart.md / gut.md / hard-thing-selection.md to karpathy. What's the "experiment queue" exactly — a single file, a directory? The experiments/ directory under `~/shared/context/` contains TSV logs and *-modified-*.md files. Are any of those in karpathy's scope? Proposed default: treat the entire `~/shared/context/experiments/` directory as karpathy-flagged if it contains files matching `*-modified-*.md` or `experiment-log.*`.

2. **Steering scope**. R1.1 lists the 4 target directories. Does `.kiro/settings/` (containing `mcp.json`) count as part of the audit? Proposed default: no — mcp.json is configuration, not a text file with referrer relationships. Out of scope.

3. **Heading-overlap threshold**. R3.2 says 50%. Should this be tunable? Proposed default: hardcode 0.5 for the first audit run; tune later if the first pass produces weird groupings.

4. **Auto-generated detection heuristic**. The 5-commits-in-30-days rule is arbitrary. Is this good enough for changelog.md (which may be partially automated)? Proposed default: flag `auto_generated_candidate: true` and let Richard decide in review; no automatic KEEP.

5. **Conflict resolution vocabulary for MERGE**. R9.4 says "conflicting content." What qualifies? Proposed default: whitespace-normalized body comparison per section. Identical after whitespace normalization → not a conflict. Different → conflict. Same heading, same body except whitespace → merge skips the section.

6. **Dreaming integration**. Peter Steinberger's "dreaming" concept (session-log reconciliation into durable memory, drop irrelevant, elevate recurring) is structurally the same pattern as Richard's existing `session-log.md` → `wiki-candidates.md` → published wiki pipeline. This audit's `execution.log` archive should become an input to that pipeline — the completion record is a learning artifact, not a closed record. Proposed default: the Phase 7 archive step includes a one-line append to `wiki-candidates.md` naming the audit's biggest finding (e.g., "x% surface reduction, n metaphor-only files deleted, n scaffolding files preserved for L3-L5") so the learning compounds into the wiki over time. Richard to confirm or adjust scope.

7. **Extension-first long-term target**. The audit produces a kill-list. What survives is still a monolith. The long-term structural answer (Peter's ethos) is to refactor survivors into extensions that get loaded on-demand rather than always-loaded. This is out of scope for this audit — but calling it out so the archived completion log includes a recommendation for the follow-on spec: "restructure surviving files as extension-loaded modules per the pi / OpenClaw architecture pattern." Not a task for this audit; a named follow-on for when it completes.

These questions don't block the design — they're documented for the Phase 4 classification session to resolve with Richard's input if they arise.

---

## Portability Check (per constraint #7)

A new AI on a different platform reads this design file. Can it execute the audit?

- Phase 1 needs `listDirectory`, `wc -l`, `stat`, `git log`, `readFile` — standard tools, available on any Linux shell.
- Phase 2 needs file-content regex search (ripgrep or equivalent) — available.
- Phase 3 needs basic string parsing — available.
- Phase 4 is pure classification over JSON — no special tools.
- Phase 5 is markdown write — standard.
- Phase 6 needs `deleteFile`, file edit tools, `git commit` — standard.
- Phase 7 needs `mv` and `git commit` — standard.

No Kiro-specific tools (hooks, MCP servers, subagents) are required. The JSON schemas are explicit. The decision tree is deterministic given inputs. Row ID format is documented. The kill-list review syntax is specified as a grammar.

A different-platform agent reading this file could re-execute the audit against the same system and produce equivalent output. That's the portability bar.
