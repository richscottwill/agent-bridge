# Implementation Plan: Skills & Powers Adoption

Each task is a discrete unit of work executable in a single session. Tasks are grouped by design phase (Phase 0 → A → B → C → D → E) plus cross-cutting validator and property-test groups. Dependencies are explicit.

**Two execution paths** (per design Phase 0 philosophy):
- **SCRAPPY-PASS** (Peter-ethos — ship, measure, iterate): Groups 0 → 1 → 2 → 3 → 30-day pilot runs → revisit this tasks.md with activation data in hand. Defers Groups 4 (routing tree), 5 (safe-creation), 7 (validators), 8 (property-based tests) until the pilot answers whether the activation habit is sticking. If activation stays near zero, the rest of the design doesn't matter — prune before building more.
- **FULL-PASS** (Mario-ethos — do it right the first time): All Groups 0 → 9, all phases implemented, all 15 properties property-tested. Longer initial build, more confidence in completeness.

Default: ask Richard which path. **Recommend SCRAPPY-PASS for first iteration** — the activation habit is the riskiest unknown. If it doesn't stick over 30 days, the routing tree, safe-creation workflow, and validator layer are premature.

Implementation language for Groups 7 (validators) and 8 (property-based tests): **Python + hypothesis**. Group 9 reporting may also be Python. Groups 0-3 are mostly procedure execution inside the agent session (filesystem reads, JSONL appends, markdown rendering) — code/no-code boundary for those groups is discussed per task.

---

## Group 0 — Bootstrap (one-shot, required for both paths)

- [x] **0.1 Confirm pass mode and check for prior adoption-system artifacts**
  - Ask Richard: SCRAPPY-PASS or FULL-PASS? Default SCRAPPY if first run.
  - Check for `~/shared/context/skills-powers/inventory.md`. If present with recent `Last updated` → ask Richard whether this is a re-run or a fresh start.
  - Check for `~/shared/context/skills-powers/activation-log.jsonl`. If present → do NOT delete; the log is append-only and survives across runs.
  - Check for any prior `~/.kiro/steering/skills-powers*.md` auto-loaded file. If present → flag as violation of anti-goal #2; do not proceed without Richard's acknowledgement.
  - _Requirements: R1.4 (location), §Anti-Goals #2_

- [x] **0.2 Create `~/shared/context/skills-powers/` directory and initialize empty artifacts**
  - `mkdir -p ~/shared/context/skills-powers/`
  - Create empty `inventory.md` with header only (`# Skills & Powers Inventory`, `Last updated: <ts>`, `Activation log: ~/shared/context/skills-powers/activation-log.jsonl`).
  - Create empty `activation-log.jsonl` (zero bytes).
  - _Requirements: R1.4, §Data Model → Inventory file, §Data Model → Activation log_

- [x] **0.3 Add single name-reference line to soul.md's Data & Context Routing table**
  - Edit `~/.kiro/steering/soul.md`. In the Data & Context Routing table, add one row:
    `| Skills/powers inventory: what's installed and what's activated | — | ~/shared/context/skills-powers/inventory.md |`
  - **Must be a name-reference only**, not `#[[file:...]]`, not inclusion mode change. Per audit R2.2 this is `name` match-type — informational, does not save the inventory from ORPHAN status.
  - Per anti-goal #2: do NOT add any new `inclusionMode: always` steering file.
  - _Requirements: R1.4, §Inventory File Spec → "Location (orphan-by-design)", §Anti-Goals #2_


---

## Group 1 — Phase 0 Activation Baseline (one-shot, required for both paths)

Runs ONCE, before Group 2's first inventory render. Produces the T0 snapshot the 30-day pilot measures against.

- [x] **1.1 Scan `~/shared/context/intake/session-log.md` for historical activations**
  - For each of the 13 installed asset names (9 skills + 4 powers), grep the session log for name occurrences plus variations (`discloseContext.*{name}`, `kiroPowers.*{name}`, plain mentions).
  - Extract per name: `first_observed` (earliest match timestamp or null), `last_observed` (most recent match timestamp or null), `approximate_count` (conservative — count only matches that look like invocations, not just mentions).
  - Skills to scan: bridge-sync, charts, coach, cr-tagging, sharepoint-sync, wbr-callouts, wiki-audit, wiki-search, wiki-write.
  - Powers to scan: aws-agentcore, flow-gen, hedy, power-builder.
  - _Requirements: R5.2, §Pilot procedure step T0, §Data Model → Activation log baseline events_

- [x] **1.2 Emit `baseline` event rows to `activation-log.jsonl`**
  - For each of the 13 installed assets, append one `{"event":"baseline","kind":"skill"|"power","name":"{n}","first_observed":"{ts|null}","last_observed":"{ts|null}","session_id":"sess-{date}-baseline","ts":"{now}"}` row.
  - Null `first_observed` / `last_observed` when the grep found no invocations. Do NOT fabricate timestamps.
  - Append-only. No truncation, no rewriting of the log file.
  - _Requirements: R5.2, R6.3, R6.4, §Data Model → Activation log, Property 12_

- [x] **1.3 Write baseline snapshot report**
  - Create `~/shared/context/skills-powers/baseline-{YYYY-MM-DD}.md` documenting T0 state: per-asset `first_observed`, `last_observed`, count, and a one-line "this is what we measured before the pilot started."
  - One-time artifact; documents what was true before any adoption-system intervention. Not re-generated.
  - _Requirements: §Pilot procedure step T0_

---

## Group 2 — Phase A Inventory Generator (required for both paths)

- [x] **2.1 Implement filesystem walker** (Python module)
  - Walk `~/.kiro/skills/*/SKILL.md` and `~/.kiro/powers/installed/*/POWER.md`.
  - Return a list of `{path, kind, raw_frontmatter_text, body_text, mtime}` records.
  - Follow symlinks at depth 1 max; record `symlinks_followed[]` for audit trail.
  - SCRAPPY-PASS note: this can be a shell one-liner for the first render. FULL-PASS: make it a Python module for Group 7 validators to reuse.
  - _Requirements: R1.1, R1.2, §Architecture Phase A_

- [x] **2.2 Implement YAML frontmatter parser** (Python module)
  - Parse frontmatter into a structured record per §Data Model → SKILL.md frontmatter and §Data Model → POWER.md frontmatter.
  - Preserve key ordering within groups per §Round-Trip File Format.
  - Do NOT silently rewrite malformed files — on parse error, return the error and leave the file unchanged (Property 7).
  - Legacy-status files (no `status` field) parse successfully; schema validation is status-gated (Property 11).
  - _Requirements: R9.1, R9.2, R9.4, Property 6, Property 7_

- [x] **2.3 Implement inventory.md rendering**
  - Render two tables: Skills (columns: Row ID, Name, Status, Triggers, Sensitivity, Portability, Last Activated, Usage) and Powers (columns: Row ID, Name, Status, Type, Sensitivity, Portability, Last Activated, Usage).
  - Row IDs: `K-S{N}` for skills (1-indexed alphabetical), `K-P{N}` for powers (same).
  - Status column is prominent and separate from Usage. Legacy rows render `—` for Sensitivity / Portability (expected absence, not validation failure). Current rows with missing required fields render **`MISSING`** in bold.
  - Append a Staleness section listing: unused (never activated), stale (activations exist but none in last 30d), candidates for next pruning review.
  - Sort: skills section by name ASC; powers section by name ASC.
  - _Requirements: R1.1, R1.2, R1.5, §Data Model → Inventory file, Property 1_

- [x] **2.4 Implement sha256 input-state hash for freshness verification**
  - Compute hash of: sorted list of (file path + frontmatter text) across all skills and powers.
  - Record the hash in the inventory's header (e.g., `Input-state-hash: sha256:abc...`).
  - On subsequent reads, recompute and compare. Mismatch → re-run Group 2 before trusting the inventory.
  - _Requirements: R1.3, Property 5_

- [x] **2.5 Implement ad-hoc refresh trigger**
  - Wire: when Richard says "refresh skills inventory" (or any phrasing matching that intent), re-run tasks 2.1 → 2.4.
  - No scheduled cron. No recurring hook. On-demand only. (Anti-goal #1, anti-goal #8.)
  - _Requirements: R1.3, §Architecture Phase A, §Anti-Goals #1_

- [x] **2.6 Render the first inventory.md**
  - Run 2.1 → 2.5 against the live filesystem. Expected output: 9 skills + 4 powers, all rows `status: legacy`, all Sensitivity/Portability `—`, all Last Activated from Group 1's baseline (many `never`).
  - Commit the rendered inventory.md. This is the T0 inventory snapshot.
  - **Anti-task:** do NOT force-classify any legacy asset at this stage. Classification happens only via touch-it-classify-it in Phase C (Group 5). See §Anti-Goals #6.
  - _Requirements: R5.2, §Schema status rules → "touch-it-classify-it migration rule"_


---

## Group 3 — Phase D Activation Logging (required for both paths; continuous once wired)

This group is the backbone of the pilot. Without 3.1 and 3.4, the 30-day activation data never materializes and Group 9 has nothing to measure.

- [x] **3.1 Implement JSONL append logic for `activated` events**
  - On every successful `discloseContext(...)` or `kiroPowers activate(...)` call during a session, append one row to `~/shared/context/skills-powers/activation-log.jsonl`:
    `{"event":"activated","kind":"skill"|"power","name":"{n}","request_summary":"{≤120 chars}","session_id":"{sess}","ts":"{ISO8601}"}`
  - Append-only. No existing rows mutated. No deletes.
  - If the file does not exist, create it (Group 0.2 already creates it empty).
  - _Requirements: R6.1, R6.3, R6.4, Property 12_

- [x] **3.2 Implement `missed-by-feedback` append on explicit Richard flag**
  - Trigger: Richard says something like "you should have used skill X" / "you missed the coach skill" / equivalent.
  - Append one row: `{"event":"missed-by-feedback","kind":"skill"|"power","name":"{n}","feedback_text":"{≤200 chars}","session_id":"{sess}","ts":"{ISO8601}"}`.
  - **Never auto-generated.** No pre-send scanner. No post-draft detector. Richard-flag only. Per §Design Decisions → "Why missed-skill detection was cut" and §Anti-Goals #10.
  - _Requirements: R6.2 (revised), §Adoption Habit Integration → "Missed-skill detection is not machine-enforced"_

- [x] **3.3 Implement `correction` event handling**
  - When a prior row is wrong, append (never mutate): `{"event":"correction","target_ts":"{erroneous row ts}","reason":"{≤200 chars}","session_id":"{sess}","ts":"{ISO8601}"}`.
  - Append-only; prior row stays in place as historical record.
  - _Requirements: §Data Model → Activation log "No updates, no deletes", Property 12_

- [x] **3.4 Implement pre-draft keyword matcher**
  - On reading a user request, before drafting the response:
    1. Parse triggers from inventory.md (skills: trigger list from `description`; powers: `keywords` array).
    2. Match request text against triggers. Match policy: ≥50% keyword overlap OR one exact trigger-phrase match.
    3. On match, call `discloseContext(name=matched_skill)` or `kiroPowers activate(powerName=matched_power)` BEFORE drafting.
    4. Task 3.1 handles the log append automatically.
  - Multiple matches: activate whichever has strongest keyword overlap; ties broken by most-recently-activated.
  - **This is the ONLY machine-enforced activation path.** No post-draft re-check. No pre-send re-scan.
  - _Requirements: R6.1, §Adoption Habit Integration → "In-turn activation via discloseContext / kiroPowers activate", Property 12_

- [x] **3.5 Checkpoint — SCRAPPY-PASS stops here and the 30-day pilot runs**
  - If SCRAPPY-PASS: verify Group 0, 1, 2, 3 are complete. Confirm `activation-log.jsonl` has 13 baseline rows from 1.2. Confirm `inventory.md` renders with all 13 assets. Confirm 3.4 is wired so subsequent sessions accrue `activated` rows automatically.
  - Start the 30-day pilot clock (T0 = date the baseline was written). Richard now works normally for 30 days.
  - At T30, run Group 9 (post-pilot review). If the pilot succeeds (≥3 activations per skill, ≥5 of 9 activated), then decide whether to do FULL-PASS for the remaining groups or leave them deferred. If the pilot fails, route survivors through Group 6 pruning before considering any new-asset creation.
  - Ensure all tests pass, ask the user if questions arise.
  - _Requirements: R5.6, §Pilot procedure_

---

## Group 4 — Phase B Routing Decision Tree (FULL-PASS only)

Implements the 8-step tree from §Routing Decision Tree. Order matters: steps 0 and 0.5 are subtraction-first; step 1 is EXTEND-EXISTING-first; only after those three gates does the tree reach mechanism-selection.

- [x] **4.1 Implement routing tree step 0 — REJECT gate**
  - Questions: frequency < 1x/month? re-explanation cost low? already captured by memory + standard prompt? one-off that won't recur?
  - Any YES → terminate REJECT with rationale "keep in head, no codification needed". Write rationale to routing-decision.json.
  - Any NO across all questions → continue to step 0.5.
  - _Requirements: R2.3, §Routing Decision Tree step 0, Property 15 (partial — step 0 rejection path)_

- [x] **4.2 Implement routing tree step 0.5 — NON-KIRO gate**
  - Checks in order: `.bashrc`, cron jobs, git hooks, OS-level shortcuts, known IDE features, known team tools.
  - For each check, look up whether the proposed workflow could already be handled by that mechanism (canonical reference case: `dashboard-server.kiro.hook` duplicating `.bashrc` auto-restart).
  - YES → terminate REJECT with rationale naming the existing mechanism (e.g., `"already handled by .bashrc auto-restart"`). Do NOT create anything inside Kiro's layers.
  - NO across all → continue to step 1.
  - _Requirements: §Routing Decision Tree step 0.5, §Design Decisions → "Why the REJECT gate checks non-Kiro mechanisms", Property 15_

- [x] **4.3 Implement routing tree step 1 — EXTEND_EXISTING gate**
  - Overlap-check against the 9 installed skills' trigger lists + 4 installed powers' keyword arrays.
  - Threshold: ≥75% keyword/trigger match OR one exact trigger-phrase match.
  - YES → terminate `EXTEND_EXISTING(asset_path)`; surface the matched asset to Richard for editing rather than creating a new asset.
  - NO → continue to step 2.
  - The `searched_mechanisms` record from this step feeds Phase C's overlap-check.json.
  - _Requirements: R2.6, R5.4, R10.1, R10.2, §Routing Decision Tree step 1, Property 10_

- [x] **4.4 Implement routing tree steps 2-7**
  - 4.4.1 Step 2: EVENT vs KEYWORD split → HOOK branch if event-triggered, continue otherwise.
  - 4.4.2 Step 3: IDENTITY / ALWAYS-APPLICABLE → STEERING branch. Scrutiny applies (every-chat tax).
  - 4.4.3 Step 4: SPECIALIST DOMAIN → SUBAGENT branch (skills orchestrating multiple subagents still OK per R10.5).
  - 4.4.4 Step 5: PERSISTENT STATE → ORGAN branch.
  - 4.4.5 Step 6: MCP-BUNDLE → POWER branch (Guided MCP vs Knowledge Base sub-type).
  - 4.4.6 Step 7: Default → SKILL branch.
  - First matching branch wins. Record terminal leaf.
  - _Requirements: R2.1, R2.5, §Routing Decision Tree steps 2-7, §Mechanism sub-trees_

- [x] **4.5 Implement routing-decision.json emission per terminal leaf**
  - On terminal leaf, emit:
    `{"timestamp":"...","workflow_description":"...","terminal_leaf":"REJECT|EXTEND_EXISTING|HOOK|STEERING|SUBAGENT|ORGAN|POWER|SKILL","rationale":"...","gates_passed":[...],"gate_that_terminated":"0|0.5|1|2|3|4|5|6|7"}`
  - Persist to session state; on CREATE-variant leaves, this feeds Phase C's overlap-check.json.
  - On REJECT / EXTEND_EXISTING leaves, persist as documentation only — no Phase C runs.
  - _Requirements: R2.3, Property 9_

- [x] **4.6 Write the routing-tree walker as a reusable procedure**
  - Not a subagent. Not a hook. A procedure the agent follows deterministically when Richard proposes a new workflow.
  - Lives as a prose procedure in the design (§Routing Decision Tree) AND as a Python function `walk_routing_tree(workflow_description, inventory) -> routing_decision_dict` for Group 7 validators and Group 8 property tests.
  - Agent reads the prose; Python function is used by validators/tests.
  - _Requirements: §Routing Decision Tree, Property 9, Property 10, Property 15_

- [ ]* 4.7 Write property tests for routing tree (hypothesis)
  - Hypothesis strategy `genWorkflowProposal`: random workflow descriptions with random trigger/event/specialist/state/MCP characteristics.
  - Assert Property 9 (ROUTING-PRECEDES-CREATE), Property 10 (EXTEND-EXISTING-PRECEDENCE), Property 15 (NON-KIRO-GATE-REJECTION) over 100+ iterations each.
  - Tag: `# Feature: skills-powers-adoption, Property 9/10/15: ...`
  - _Requirements: §Testing Strategy, Properties 9, 10, 15_


---

## Group 5 — Phase C Safe-Creation Workflow (FULL-PASS only)

Runs on two triggers: (a) Phase B terminates at CREATE-variant; (b) a `status: legacy` asset is edited for any reason (touch-it-classify-it migration).

- [x] **5.1 Implement overlap-check (Phase C.1, new assets only)** (Python module)
  - Inputs: proposed asset description / keywords / triggers, routing-decision.json from Phase B.
  - Search all 6 Kiro kinds + non-Kiro mechanisms:
    - Skills: `~/.kiro/skills/`
    - Powers: `~/.kiro/powers/installed/`
    - Subagents: `~/.kiro/agents/`
    - Hooks: `~/.kiro/hooks/`
    - Steering: `~/.kiro/steering/`
    - Organs: `~/shared/context/body/`
    - Non-Kiro: `.bashrc`, cron, git hooks, known IDE features, known team tools
  - Score each candidate: keyword/trigger overlap + cosine similarity of one-line purpose.
  - Emit `~/.kiro/skills/{name}/overlap-check.json` (or powers equivalent) with `searched_mechanisms` (all 6 kinds + `non_kiro_mechanisms_considered`), `overlap_candidates`, `decision`, `decision_rationale`, `alternatives_considered`, `reviewed_by_richard: false` (set true at 5.2).
  - Legacy reclassification: skip this task entirely — retrospective overlap-check has no decision to document.
  - _Requirements: R7.1, R7.3, R10.1, R10.3, §Phase C.1, Property 8_

- [x] **5.2 Implement Richard review gate (Phase C.2)**
  - Present to Richard: proposed SKILL.md / POWER.md content draft, declared metadata (sensitive_data_class, portability_tier, platform_bound_dependencies), overlap-check findings, portability validator report (advisory), path-allowlist check result (enforced).
  - Require explicit approval. Absence of veto is NOT approval.
  - On approval → write `reviewed_by_richard: true` and `reviewed_at: {ts}` to overlap-check.json; proceed to 5.3.
  - On edit → return to 5.1 with updated content.
  - On cancel → terminate; no files written.
  - _Requirements: R7.2, R7.3, R7.4, §Phase C.2, Property 8_

- [x] **5.3 Implement file write for new asset (Phase C.3 new-asset path)**
  - Write SKILL.md to `~/.kiro/skills/{name}/SKILL.md` or POWER.md to `~/.kiro/powers/installed/{name}/POWER.md`.
  - Frontmatter: full extended schema per §Data Model, `status: current`, `created_at: {now}`, `last_validated` set by 5.5.
  - Write overlap-check.json alongside in the same directory.
  - Round-trip serialization per §Round-Trip File Format — canonical YAML, key ordering, UTF-8, LF line endings.
  - _Requirements: R7.5, R9.1, R9.2, R9.3, §Phase C.3, Property 6_

- [x] **5.4 Implement legacy-migration path (Phase C.3 touch-it-classify-it)**
  - Trigger: any edit to a `status: legacy` asset.
  - Before writing the edit:
    1. Agent prompts Richard inline: `"This is a legacy skill. Before we save your edit, classify: sensitive_data_class? portability_tier? owner_agent?"`
    2. Richard answers → insert values, flip `status: current`, set `created_at: {stat mtime}` (or `"UNKNOWN"` if stat fails), set `last_validated: {now}`, write full extended frontmatter WITH the edit.
    3. **If Richard refuses classification** (e.g., `"I'm fixing a typo, not classifying this today"`) → accept refusal. Write the edit with minimal frontmatter preserved. Asset stays `status: legacy`. Next edit is another opportunity.
  - No forced flag-day migration. No "TODO classify" placeholder fields. Classification happens exactly on the turn Richard touches the file. Per §Anti-Goals #6 and §Design Decisions → "Why legacy / current / retired".
  - _Requirements: R5.2, R9.5, §Phase C.3 legacy-migration, Property 11_

- [x] **5.5 Implement activation-validate (Phase C.4)**
  - For new skills: call `discloseContext(name=new_name)`. On success, set `last_validated: {now}` in frontmatter.
  - For new powers: call `kiroPowers activate(powerName=new_name)`. On success, set `last_validated: {now}`.
  - On failure: annotate frontmatter with `# validation-failed: {reason}` comment. Do NOT activate the asset in any subsequent session until re-validated.
  - Same check for migrated legacy assets.
  - _Requirements: R7.6, §Phase C.4, Property 14_

- [x] **5.6 Implement inventory + log update (Phase C.5)**
  - Re-run Group 2 refresh (2.1 → 2.4) — updates inventory.md with the new/migrated row.
  - Append `{"event":"created","kind":"skill"|"power","name":"{n}","session_id":"{sess}","ts":"{now}","overlap_check_ref":"{path}"}` to activation-log.jsonl.
  - For legacy reclassification, event subtype is `classified`: `{"event":"created","subtype":"classified","kind":"...","name":"...","session_id":"...","ts":"..."}`. No overlap_check_ref (legacy path).
  - _Requirements: R7.5, R10.3, §Phase C.5, Property 12_

- [x]* 5.7 Write property tests for safe-creation (hypothesis)
  - Assert Property 8 (OVERLAP-CHECK-COMPLETENESS), Property 9 (ROUTING-PRECEDES-CREATE), Property 11 (STATUS-GATED-SCHEMA), Property 14 (ASSET-LIFECYCLE validate-before-available half).
  - Use `genFilesystemState` for inputs.
  - _Requirements: §Testing Strategy, Properties 8, 9, 11, 14_

---

## Group 6 — Phase E Pruning Review (FULL-PASS + SCRAPPY-PASS at T30)

Depends on Group 3 (activation log) and Group 2 (inventory). Runs at T30 for SCRAPPY-PASS pilot review; runs on Richard demand thereafter.

- [x] **6.1 Implement stale-set computation per Property 2**
  - Input: inventory.md + activation-log.jsonl.
  - For each installed skill/power:
    - If `status == retired` → skip (already pruned).
    - If created within last 30 days → skip (not enough measurement window).
    - If any `activated` event in last 30 days → NOT stale. **Never-prune-under-use guarantee** enforced at set construction, not at review.
    - Else → add to stale set with `{days_stale, activation_count_90d, creation_date_if_known, status}`.
  - _Requirements: R1.5, R6.5, R8.1, R8.4, §Pruning Review procedure, Property 2_

- [x] **6.2 Implement pruning review presentation**
  - Render per-asset row: `{name, status, days since last activation, activation count last 90d, creation date}`.
  - Sort: most stale first (longest gap).
  - Presentation is markdown for Richard to review interactively. No scheduled cron. No auto-approval. Absence of decision = DEFER per §Pruning Review procedure.
  - Richard marks each row: APPROVE (prune) / DEFER (keep, note reason) / PROTECT (keep permanently, note reason).
  - _Requirements: R8.1, R8.5, §Pruning Review procedure_

- [x] **6.3 Implement archive-before-delete ordering**
  - For each APPROVED row:
    1. Copy: `cp -r ~/.kiro/skills/{name}/ ~/shared/wiki/agent-created/archive/skills-powers-pruned-{YYYY-MM-DD}/{name}/` (or powers equivalent).
    2. Verify archive: list the archive directory, confirm SKILL.md / POWER.md + overlap-check.json (if present) are at destination.
    3. Only on verified archive → `rm -rf` the source directory.
    - If archive step fails → delete step does NOT run. Row is skipped, logged.
  - Atomic at the row level per Property 14.
  - _Requirements: R8.2, R8.3, §Pruning Review → "Archive-before-delete", Property 14_

- [x] **6.4 Implement `pruned` event log append and inventory update**
  - Append: `{"event":"pruned","kind":"skill"|"power","name":"{n}","archive_path":"{path}","session_id":"{sess}","ts":"{now}"}`.
  - Update inventory: mark the pruned row `status: retired` for ONE full pruning cycle, then drop on the next render.
  - _Requirements: R8.2, §Data Model → Activation log, §Pruning Review step 4, Property 12_

- [x]* 6.5 Write property tests for pruning (hypothesis)
  - Assert Property 2 (STALENESS-CORRECTNESS — never-prune-under-use) and Property 14 (ASSET-LIFECYCLE — archive-before-delete).
  - Include edge case: activation exactly 30 days ago (Property 2 generator should sample this boundary).
  - _Requirements: §Testing Strategy, Properties 2, 14_


---

## Group 7 — Validators (FULL-PASS only; cross-cutting)

Python modules called reactively by Phase C (Group 5) and ad-hoc by Richard. Never run as daemons. Per §Anti-Goals #5 and #7, validators are functions not services.

- [x] **7.1 Implement round-trip YAML parser/serializer** (Python module)
  - Parse: YAML frontmatter → structured record with preserved key ordering (groups: identity → status → classification → timestamps).
  - Serialize: structured record → canonical YAML (UTF-8, LF, 2-space indent, alphabetical within groups, block-form lists, double-quoted strings with special chars).
  - Preserve markdown body byte-identically through parse → serialize.
  - Comments in YAML attached to following key, re-emitted in same position.
  - _Requirements: R9.1, R9.2, R9.3, §Round-Trip File Format, Property 6_

- [x] **7.2 Implement format-compliance validator (non-silent rewrite)**
  - Report-and-don't-modify semantics: on malformed file, emit descriptive error (field name, expected type, actual type, line number) AND leave file unchanged on disk.
  - Unknown fields: preserve in `legacy_unknown_fields` map; do not drop.
  - Wrong types / missing required / malformed YAML: parse fails, file unchanged.
  - _Requirements: R9.4, R9.5, §Round-Trip File Format → "Error reporting", Property 7_

- [x] **7.3 Implement sensitivity path-allowlist validator**
  - Status-gated: runs for `status: current`, SKIPS for `status: legacy` (legacy assets grandfathered until next edit per Property 11).
  - For current assets with declared `sensitive_data_class = C` and output path P:
    1. Look up `allowlist(C)` per §Sensitive-Data Classification Rules.
    2. If `P ∉ allowlist(C)` → emit validation error (blocks write).
    3. For `C ∈ {Amazon_Confidential, Personal_PII}`: additionally check whether P lies under any directory currently synced to agent-bridge (read bridge-sync.md's sync list live, not cached). If yes → emit sync-violation error.
  - Blocks writes (this validator is enforced, unlike portability).
  - _Requirements: R3.2, R3.3, R3.5, R3.6, R7.4, §Sensitive-Data Classification Rules → "Path-allowlist enforcement algorithm", Property 3_

- [x] **7.4 Implement advisory portability validator (REPORT ONLY)**
  - **Does NOT reject. Does NOT modify the file. Does NOT auto-downgrade the declared tier.** Emits a report.
  - Scan body for platform-bound-indicator tokens: `mcp_[a-z_]+`, `invokeSubAgent` + subagent names from `~/.kiro/agents/`, `[a-z0-9_\-]+\.kiro\.hook`, `discloseContext`, `kiroPowers`, script paths (`scripts/`, `~/shared/tools/`, `~/shared/scripts/`), DuckDB table prefixes (`ps\.`, `signals\.`, `asana\.`, `main\.`).
  - Group findings by token kind.
  - When declared `Cold_Start_Safe` and body contains Platform_Bound tokens: emit **advisory consistency note** (not an error). Richard decides whether to rewrite the body, update the tier, or proceed as-is.
  - When declared `Platform_Bound`: cross-check `platform_bound_dependencies` list (if declared) against tokens in body — flag tokens in body not listed (informational) and items listed not found in body (informational). Cross-check is informational; `platform_bound_dependencies` is RECOMMENDED not required.
  - Report written to Phase C session state and logged as `activated` event subtype `portability_report`.
  - Per §Anti-Goals #7 and §Design Decisions → "Why the portability validator is advisory": the earlier blocking behavior was explicitly removed.
  - _Requirements: R4.3, R4.4, R4.5, §Portability Tier Rules → "Portability validator — advisory only", Property 4_

- [x] **7.5 Implement status-gated schema validator**
  - For `status: current`: require `sensitive_data_class`, `portability_tier`, `created_at`, `last_validated`; require `platform_bound_dependencies` iff `portability_tier == Platform_Bound`. Missing → validation error.
  - For `status: legacy`: SKIP all schema checks. Minimal original frontmatter (skills: `name`, `description`; powers: `name`, `displayName`, `description`, `keywords`, `author`) is sufficient. Legacy rows still appear in the inventory (Property 1 bijection).
  - For `status: retired`: accept both minimal and extended frontmatter; retired rows are historical.
  - _Requirements: R3.1, R4.2, R9.5, §Schema status rules, Property 11_

- [x] **7.6 Implement subagent-wrapper detector**
  - Analyze a proposed SKILL.md body: does it contain exactly one `invokeSubAgent` call with no other orchestration (no multi-agent pipeline, no pre/post-processing steps, no additional tool calls)?
  - Yes → emit rejection: `"wraps single subagent; subagent is the correct mechanism"`. Block the Phase C write.
  - No (multiple subagents orchestrated, or other tool calls / logic present) → pass per R10.5.
  - _Requirements: R10.4, R10.5, Property 13_

- [x]* 7.7 Write unit tests for each validator
  - Specific examples per §Testing Strategy: malformed YAML error messages; `status: legacy` bypass path; Cold_Start_Safe with Platform_Bound tokens (advisory output, file unchanged); Amazon_Confidential in bridge-synced path (error).
  - _Requirements: §Testing Strategy → "Dual testing approach"_

---

## Group 8 — Property-Based Tests (FULL-PASS only)

Python + hypothesis, minimum 100 iterations per property. Tag format: `# Feature: skills-powers-adoption, Property {N}: {property text}`. Depends on Groups 2, 3, 4, 5, 6, 7 (all mechanisms must exist before properties test them).

- [x] **8.1 Set up hypothesis harness**
  - Install `hypothesis`. Configure test settings: `max_examples=100` minimum; `deadline=None` for filesystem-touching tests.
  - One test module per property group (routing/creation/validators/lifecycle) to keep files focused.
  - _Requirements: §Testing Strategy → "Property test configuration"_

- [x] **8.2 Implement generators (hypothesis strategies)**
  - `genFilesystemState`: random directory trees with random skill/power files. Frontmatter variations (legacy vs current, valid vs malformed, all-required-fields vs missing-some). Edge cases: empty dir, single asset, 100+ assets, mixed statuses.
  - `genActivationLog`: random append-only JSONL. Random event distributions (`baseline`, `activated`, `missed-by-feedback`, `created`, `pruned`, `correction`) over random time windows. Edge cases: empty log, single event, events exactly at 30-day boundary.
  - `genWorkflowProposal`: random workflow descriptions with random trigger / event / specialist / persistent-state / MCP characteristics. Edge cases: proposal matching no existing asset, proposal matching exactly one existing asset, proposal matching multiple existing assets.
  - `genSkillBody`: random markdown bodies with varying Platform_Bound-indicator token densities (0 tokens → many tokens).
  - _Requirements: §Testing Strategy → "Property test configuration"_

- [x] **8.3 Property 1: INVENTORY-BIJECTION**
  - Tag: `# Feature: skills-powers-adoption, Property 1: For any filesystem state, inventory.md rows bijectively correspond with on-disk assets`.
  - Generator: `genFilesystemState`. Run Group 2 inventory generator. Assert: every on-disk asset appears as exactly one row; no phantom rows; `status: retired` rows tracked separately.
  - Edge cases: empty dir, single asset, 100 assets, mixed statuses.
  - _Validates: Requirements 1.1, 1.2, 1.3, 7.5_

- [x] **8.4 Property 2: STALENESS-CORRECTNESS**
  - Tag: `# Feature: skills-powers-adoption, Property 2: Stale set equals {asset : status ∈ {legacy, current} AND no activation in last 30d AND not created in last 30d}`.
  - Generator: `genActivationLog` + `genFilesystemState`. Run Group 6.1 stale-set computation. Assert set matches specification; assets activated in last 30d are NEVER in the stale set (never-prune-under-use guarantee).
  - Edge case: activation exactly 30 days ago.
  - _Validates: Requirements 1.5, 6.5, 8.1, 8.4_

- [x] **8.5 Property 3: PATH-ALLOWLIST-CORRECTNESS**
  - Tag: `# Feature: skills-powers-adoption, Property 3: Validator emits path-allowlist violation iff P ∉ allowlist(C), status-gated`.
  - Generator: random `{sensitive_data_class, output_path, status}` triples. Assert: for `status: current`, violation iff `path ∉ allowlist(class)`; for `Amazon_Confidential`/`Personal_PII`, additional sync-violation when path is under a bridge-sync directory; for `status: legacy`, validator does NOT run the allowlist check.
  - _Validates: Requirements 3.2, 3.3, 3.5, 3.6, 7.4_

- [x] **8.6 Property 4: ADVISORY-PORTABILITY-REPORT (report-only, NOT rejection)**
  - Tag: `# Feature: skills-powers-adoption, Property 4: Portability validator emits report, never rejects, never modifies file, never auto-downgrades tier`.
  - Generator: `genSkillBody` + random declared tier. Run Group 7.4. Assert (a) report is returned containing detected tokens grouped by kind; (b) input file is byte-identical after validator runs; (c) no rejection error raised regardless of declared tier — including Cold_Start_Safe with Platform_Bound tokens (the advisory consistency case).
  - **Test explicitly asserts NOT rejection**, per F1 revision.
  - _Validates: Requirements 4.3, 4.4, 4.5_

- [x] **8.7 Property 5: INVENTORY-FRESHNESS**
  - Tag: `# Feature: skills-powers-adoption, Property 5: If H_R == H_FS then R reflects current filesystem; mismatch triggers Phase A re-run`.
  - Generator: inventory render + subsequent filesystem mutation. Assert hash mismatch → agent re-runs Phase A before trusting R.
  - Scope note per F3: property is about inventory accuracy relative to FS; does NOT claim anything about inventory's own active-referrer status.
  - _Validates: Requirements 1.3, 1.4_

- [x] **8.8 Property 6: ROUND-TRIP**
  - Tag: `# Feature: skills-powers-adoption, Property 6: parse(serialize(parse(F))) == parse(F) and body bytes preserved`.
  - Generator: random valid SKILL.md / POWER.md. Run Group 7.1 parse/serialize round-trip. Assert structural equality of frontmatter + byte equality of body.
  - _Validates: Requirements 9.1, 9.2, 9.3_

- [x] **8.9 Property 7: NON-SILENT-REWRITE**
  - Tag: `# Feature: skills-powers-adoption, Property 7: Malformed file produces error AND file is unchanged on disk`.
  - Generator: random malformed files (bad YAML, wrong types, missing required for `status: current`). Assert validator errors AND `stat` before/after shows identical mtime and size.
  - _Validates: Requirement 9.4_

- [x] **8.10 Property 8: OVERLAP-CHECK-COMPLETENESS**
  - Tag: `# Feature: skills-powers-adoption, Property 8: New asset creation produces overlap-check.json with all 6 Kiro kinds + non_kiro_mechanisms_considered; proceeds only if reviewed_by_richard`.
  - Generator: random creation proposals. Run Group 5.1 + 5.2. Assert overlap-check.json contains all required fields; write at 5.3 proceeds iff `reviewed_by_richard == true`; legacy reclassification path does NOT require overlap-check.
  - _Validates: Requirements 2.6, 10.1, 10.3_

- [x] **8.11 Property 9: ROUTING-PRECEDES-CREATE**
  - Tag: `# Feature: skills-powers-adoption, Property 9: Phase C runs only if routing-decision leaf is CREATE-variant (SKILL/POWER/STEERING/HOOK/SUBAGENT/ORGAN); REJECT and EXTEND_EXISTING do not trigger Phase C`.
  - Generator: random create-trigger sequences. Assert routing-decision.json exists and leaf ∈ {SKILL, POWER, STEERING, HOOK, SUBAGENT, ORGAN} whenever Phase C runs; REJECT/EXTEND_EXISTING leaves do not trigger Phase C.
  - _Validates: Requirements 2.3, 7.1, 7.2_

- [x] **8.12 Property 10: EXTEND-EXISTING-PRECEDENCE**
  - Tag: `# Feature: skills-powers-adoption, Property 10: Tree terminates at EXTEND_EXISTING for overlap ≥75% or exact trigger-phrase match; does NOT produce new-asset leaves`.
  - Generator: `genWorkflowProposal` with varying overlap to installed assets. Assert tree terminates EXTEND_EXISTING at threshold, CREATE-variant below threshold.
  - _Validates: Requirements 5.4, 10.1, 10.2_

- [x] **8.13 Property 11: STATUS-GATED-SCHEMA**
  - Tag: `# Feature: skills-powers-adoption, Property 11: status: current requires full frontmatter; status: legacy skips schema validation; bijection holds across all statuses`.
  - Generator: `genFilesystemState` with mixed statuses. Assert: current without required fields → validation error; legacy without extended fields → validation passes; all statuses appear in inventory (bijection with Property 1).
  - Include legacy-to-current migration test: touch a legacy asset, assert Phase C.3 legacy-migration path either classifies-and-writes or accepts refusal (legacy stays legacy).
  - _Validates: Requirements 3.1, 4.2, 9.5_

- [x] **8.14 Property 12: ACTIVATION-LOGGING**
  - Tag: `# Feature: skills-powers-adoption, Property 12: Each successful discloseContext / kiroPowers activate call appends exactly one activated row; log is append-only`.
  - Generator: random activation sequences. Assert one row per activation with required fields; no row mutation; corrections append with `event: correction` referencing target_ts. Include `missed-by-feedback` generation when Richard flags a miss.
  - _Validates: Requirements 6.1, 6.3, 6.4_

- [x] **8.15 Property 13: SUBAGENT-WRAPPER-REJECTION**
  - Tag: `# Feature: skills-powers-adoption, Property 13: Skill whose only action is a single invokeSubAgent call with no orchestration → REJECT; multi-subagent orchestration → permitted`.
  - Generator: random skill bodies (single `invokeSubAgent` vs multiple subagents vs subagent + additional tool calls). Assert single-wrapper → REJECT, multi-orchestration → permitted.
  - _Validates: Requirements 10.4, 10.5_

- [x] **8.16 Property 14: ASSET-LIFECYCLE (archive-before-delete)**
  - Tag: `# Feature: skills-powers-adoption, Property 14: Activation-validate before available; archive-before-delete atomic at row level`.
  - Generator: simulated create + prune sequences. Assert: `last_validated` set only after 5.5 passes; archive operation succeeds before 6.3's delete runs; if archive fails, delete does NOT run.
  - _Validates: Requirements 7.6, 8.2, 8.3_

- [x] **8.17 Property 15: NON-KIRO-GATE-REJECTION**
  - Tag: `# Feature: skills-powers-adoption, Property 15: If non-Kiro mechanism handles W, tree terminates at step 0.5 REJECT with rationale naming the mechanism`.
  - Generator: `genWorkflowProposal` with random external-mechanism hits (.bashrc patterns, cron-like, git hook patterns). Include explicit `dashboard-server.kiro.hook` reference case. Assert step-0.5 REJECT termination; rationale field contains the external-mechanism name.
  - _Validates: Spec-internal routing decision step 0.5; prevents the dashboard-server.kiro.hook-style duplication_

- [x] **8.18 Checkpoint — Ensure all tests pass**
  - Run full pytest / hypothesis suite. Fix any failing properties. Ask Richard if questions arise.
  - _Requirements: §Testing Strategy_


---

## Group 9 — Post-pilot review (one-shot at T30; required for both paths)

Runs 30 days after Group 1 baseline. Depends on Groups 0-3 minimum. FULL-PASS additionally relies on Group 6 for pruning execution.

- [x] **9.1 Compute per-asset activation count over the 30-day window**
  - Input: `~/shared/context/skills-powers/activation-log.jsonl`.
  - For each of the 13 installed assets, count `activated` events where `ts` is within `[T0, T0+30d]`. Ignore `baseline`, `missed-by-feedback`, `created`, `pruned`, `correction` events for the activation metric (though `missed-by-feedback` entries are surfaced separately as gap signal).
  - Emit `~/shared/context/skills-powers/pilot-review-{YYYY-MM-DD}.md` with per-asset counts.
  - _Requirements: R5.5, R5.6, §Pilot metric, §Pilot procedure step T30_

- [x] **9.2 Compare against success criterion**
  - Success criterion per R5.6: **≥3 activations per skill during 30-day window AND ≥5 of 9 installed skills activated at all**.
  - Per-skill outcome:
    - ≥3 activations → **KEEP**
    - <3 activations → **PRUNE-CANDIDATE** (eligible for Phase E pruning)
  - Aggregate outcome: pilot PASSES if ≥5 of 9 skills activated at all, regardless of per-skill count; otherwise pilot FAILS.
  - Record both per-skill and aggregate outcomes in the pilot-review markdown.
  - _Requirements: R5.3, R5.6, §Pilot metric_

- [x] **9.3 Surface skills failing the criterion as Phase E pruning candidates**
  - For each PRUNE-CANDIDATE skill: add to the next Group 6 pruning review cycle's stale-set input.
  - **Anti-task:** do NOT auto-prune. Surfaced as candidates only. Richard approves/defers/protects per Group 6.2.
  - _Requirements: R5.6, R8.1, §Pilot procedure step T30_

- [x] **9.4 Present result to Richard**
  - Render: per-asset activation count, KEEP/PRUNE-CANDIDATE per skill, aggregate PASS/FAIL, `missed-by-feedback` tally, commentary on what the data shows about the adoption habit.
  - If aggregate PASS: adoption habit is working. Decide next-round direction (9.5).
  - If aggregate FAIL: adoption habit is NOT sticking. Before building any new skill or considering Phase C creation, revisit this tasks.md with the learning. See §Post-pilot decision point below.
  - _Requirements: R5.6, §Pilot procedure step T30_

- [x] **9.5 Decide next-round direction**
  - If PASS: Richard decides between three branches:
    - **EXTEND_EXISTING on survivors**: routing tree step 1 bias holds; new workflows edit existing skills.
    - **PRUNE failing skills**: run Group 6 against PRUNE-CANDIDATEs.
    - **Consider net-new creation**: ONLY if Group 4 routing terminates at CREATE_NEW AND Group 5.1 overlap-check surfaces no viable EXTEND_EXISTING. Per R5.6, net-new creation is the last resort, not the default.
  - If FAIL: see §Post-pilot decision point below — do not build new skills; revisit the design.
  - Record the decision in `pilot-review-{date}.md`.
  - _Requirements: R5.3, R5.6, §Pilot: activation of the 9 already-installed skills, §Design Decisions → "Why the pilot is the existing 9, not 3 new ones"_

---

## Dependency Graph

```
0.1 ──> 0.2 ──> 0.3
                 │
                 v
                1.1 ──> 1.2 ──> 1.3
                                 │
                                 v
                                2.1 ──> 2.2 ──> 2.3 ──> 2.4 ──> 2.5 ──> 2.6
                                                                         │
                                                                         v
                                                                        3.1 ──> 3.2 ──> 3.3 ──> 3.4 ──> 3.5 [CHECKPOINT]
                                                                                                         │
                                    ┌────────────────────────────────────────────────────────────────────┤
                                    │                                                                    │
                                    v                                                                    v
                              (SCRAPPY-PASS:                                                       (FULL-PASS:
                              30-day pilot runs;                                                     Groups 4, 5, 7, 8 in parallel;
                              at T30 → Group 9 and                                                   6 depends on 2 + 3;
                              optionally Group 6)                                                    8 depends on 2, 3, 4, 5, 6, 7)
                                    │                                                                    │
                                    │                                          4.1 → 4.2 → 4.3 → 4.4 → 4.5 → 4.6 → [4.7*]
                                    │                                                                          │
                                    │                                          5.1 → 5.2 → 5.3 → 5.4 → 5.5 → 5.6 → [5.7*]
                                    │                                                                          │
                                    │                                          7.1 → 7.2 → 7.3 → 7.4 → 7.5 → 7.6 → [7.7*]
                                    │                                                                          │
                                    │                                                6.1 → 6.2 → 6.3 → 6.4 → [6.5*]
                                    │                                                                          │
                                    │                                                8.1 → 8.2 → 8.3-8.17 → 8.18 [CHECKPOINT]
                                    │                                                                          │
                                    v                                                                          v
                                   9.1 → 9.2 → 9.3 → 9.4 → 9.5 ←──────────────────────────────────────────────┘
```

Key dependency facts:
- Group 0 is prerequisite to everything.
- Group 1 (baseline) runs before Group 3 (activation logging relies on baseline rows being present).
- Group 2 (inventory) is independent of Group 3, but Group 9 needs both.
- Groups 4, 5, 7 (routing, safe-creation, validators) are interlocked — FULL-PASS needs all three. Safe-creation invokes validators; validators consume the parsed schema defined in Group 2's parser.
- Group 6 (pruning) depends on Group 3 (log exists) and Group 2 (inventory exists).
- Group 8 (PBT) depends on Groups 2, 3, 4, 5, 6, 7 — all mechanisms must exist before properties can test them.
- Group 9 runs at T30 regardless of path. SCRAPPY-PASS reaches Group 9 via only Groups 0-3 complete; FULL-PASS reaches Group 9 with all groups complete.

---

## Task counts

- **Total top-level tasks**: 9 groups, 53 sub-tasks (0.1-0.3, 1.1-1.3, 2.1-2.6, 3.1-3.5, 4.1-4.7, 5.1-5.7, 6.1-6.5, 7.1-7.7, 8.1-8.18, 9.1-9.5).
- **Optional sub-tasks** (postfixed `*`): 4.7, 5.7, 6.5, 7.7 — write-tests tasks associated with FULL-PASS groups. Skipping them is valid for an MVP FULL-PASS; Group 8 then covers property-level guarantees without per-group unit coverage.
- **SCRAPPY-PASS minimum**: 0.1-0.3 + 1.1-1.3 + 2.1-2.6 + 3.1-3.5 + 9.1-9.5 = 22 tasks + 30-day pilot wait + Group 6 at T30 if pruning needed.
- **FULL-PASS**: all 53 sub-tasks.

---

## Post-pilot decision point (T30)

**If the pilot PASSES** (aggregate ≥5 of 9 skills activated AND ≥3 activations per activated skill):
- Adoption habit is working. Proceed per 9.5 — bias toward EXTEND_EXISTING + PRUNE; build new only when routing tree terminates at CREATE_NEW.
- FULL-PASS implementations of Groups 4, 5, 7 become justified — the routing tree and safe-creation workflow will see real traffic because Richard is reaching for skills naturally.
- Group 8 property tests are worth writing at this point.

**If the pilot FAILS** (aggregate <5 of 9 skills activated):
- **The activation habit did not stick.** Do NOT build new skills. Do NOT implement the routing tree or safe-creation workflow yet.
- Investigate: is the pre-draft keyword matcher (3.4) firing? Are trigger lists wrong? Is Richard not doing the work that would naturally pull in these skills? (Compare `missed-by-feedback` tally to the zero-activation skills.)
- **Revisit this tasks.md.** Options:
  - If keyword matcher is broken: fix 3.4, re-baseline, re-run pilot. Groups 4-8 stay deferred.
  - If trigger lists are wrong: touch-it-classify-it migration (5.4) to update legacy frontmatter; no Group 5.3 new-asset writes until activation works.
  - If workflow simply doesn't fit skills: accept that some of the 9 are METAPHOR-ONLY (per audit methodology); run Group 6 pruning to remove dead weight; consider whether the adoption-system design itself is the right answer.
- The spec's value hypothesis is **"if we make skills discoverable and auto-activated, Richard will use them."** Pilot FAIL falsifies that hypothesis for the current corpus and pulls the work back to the design level, not forward to more implementation.

---

## Anti-tasks (explicitly called out — do NOT build)

These are things a well-intentioned agent might otherwise build. They were cut in the design revision pass and must not be reintroduced at task-list time.

1. **No post-draft missed-skill detector task.** No pre-send self-check, no post-response scanner, no convention-based re-activation pass. Missed-skill data comes ONLY from Richard-flagged `missed-by-feedback` log entries (task 3.2). Per §Anti-Goals #10, §Design Decisions → "Why missed-skill detection was cut", revision finding F4.

2. **No flag-day legacy schema migration task.** There is NO task to iterate all 13 installed assets and force classification. Migration is touch-it-classify-it (task 5.4) only — triggered when Richard edits a legacy asset, with explicit escape hatch if he refuses inline classification. Per §Anti-Goals #6, §Schema status rules, revision finding F2.

3. **No "make the inventory active-scope" task.** The inventory is ORPHAN-by-design. No auto-loaded steering. No `promptSubmit` hook. No script whose only purpose is creating active-referrer evidence. Task 0.3 adds ONE name-reference line to soul.md's Data & Context Routing table (informational, per audit R2.2) and that is the full extent of discoverability intervention. Per §Anti-Goals #2, §Inventory File Spec → "Location (orphan-by-design)", revision finding F3.

4. **No blocking portability validator task.** Task 7.4 is REPORT-ONLY. It emits findings, it does not reject, it does not modify the file, it does not auto-downgrade the tier. There is no task for "block write on Cold_Start_Safe inconsistency" or "auto-downgrade tier". Per §Anti-Goals #7, §Portability Tier Rules → "Portability validator — advisory only", revision finding F1.

5. **No "build 3 new pilot skills" task.** The pilot is measurement of the 9 already-installed skills + 4 powers. Task 1.1-1.3 baselines, task 3.4 activates during the pilot, task 9.1-9.5 reviews at T30. No task for "select 3 pilot candidates from leverage formula" or "build wbr-callouts v2" or equivalent. The leverage formula is DEMOTED until activation baseline data establishes a gap EXTEND_EXISTING cannot close. Per §Design Decisions → "Why the pilot is the existing 9, not 3 new ones", §Pilot: activation of the 9 already-installed skills, revision finding F5.

6. **No recurring-service tasks.** No task to set up a scheduled cron, a periodic freshness email, a daily audit hook, a skills-review daemon, or any other always-on mechanism. Pruning is human-triggered (task 6.2). Inventory refresh is reactive (task 2.5). Activation logging is continuous BUT it is a single JSON-line append per invocation — not a service. Per §Anti-Goals #1, §Anti-Goals #5, §Anti-Goals #8.

7. **No "always-auto-loaded skills-powers.md steering" task.** Per task 0.1 check and §Anti-Goals #2, do not introduce a new steering file with `inclusionMode: always` for this spec. The adoption system is governance-by-value, not governance-by-tax.

---

## Workflow Completion

**This workflow creates the design and planning artifacts. It does NOT implement the adoption system.**

- Execution of Groups 0-9 is a separate, downstream activity performed against this task list.
- Begin execution by opening `.kiro/specs/skills-powers-adoption/tasks.md` and clicking "Start task" next to each `- [ ]` item.
- Default execution path is SCRAPPY-PASS (Groups 0 → 1 → 2 → 3 → 30-day pilot → Group 9 → optionally Group 6). FULL-PASS execution is deferred until the pilot data justifies it.

Done means: (a) the 30-day activation baseline is captured and measured, (b) pruning candidates are surfaced from data rather than intuition, (c) any new asset creation passes through the routing tree (Group 4) and safe-creation workflow (Group 5) with validators (Group 7) enforcing what the design says is enforceable. The property-test layer (Group 8) is the durability guarantee — without it, "correctness" is prose.
