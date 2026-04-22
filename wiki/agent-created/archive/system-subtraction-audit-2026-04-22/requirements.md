# Requirements Document: System Subtraction Audit

## Introduction

Audit the Kiro context/body/protocol/hook system for accumulated complexity and produce a reviewed kill list. The system has grown to 195 context markdown files, 30 protocol files (6,429 lines), 23 hooks, 15 body organs (3,496 lines), and 27 steering files. Much of this is justified individually and none of it in aggregate — classic agent-generated complexity where every addition seemed reasonable at the time. This spec delivers findings and a kill list. It does NOT delete anything. Richard makes the final call file by file.

**Origin**: Session 2026-04-21 self-audit against Mario's pi/terminal-bench thesis ("enterprise-grade complexity within two weeks with just two humans and 10 agents"). The audit found two specific categories of drift worth reviewing: (1) the body-metaphor layer (body.md, body-diagram.md, nervous-system.md, amcc.md, gut.md, heart.md as agent-owned artifacts) which justifies its own existence more than it serves Richard, and (2) the 30-file protocol layer which has known duplication (am-auto, am-backend, am-backend-parallel are three variants of one workflow).

**Soul principle alignment**: Subtraction before addition (principle #3) is named in soul.md but has never been applied systematically. Invisible over visible (principle #5) — a smaller system is invisibly better every interaction. This audit is the first deliberate application of principle #3.

**Five Levels alignment**: L1 (Sharpen Yourself). Every file the agent must consult before doing useful work is a tax on L1 output. A smaller system ships faster.

**Non-goal**: This is NOT a rewrite, not a reorganization, not a new metaphor. The output is a categorized list of candidate files to delete, merge, or keep, with one-line justifications Richard can veto or approve.

**Future-looking constraint (added 2026-04-21)**: The audit must respect Richard's L3→L5 trajectory — team automation, zero-click future, agentic orchestration — where workflows eventually run without human intervention. The body metaphor was a transition scaffold that helped reason about agents having persistent state, shared context, and coordination layers. Pure subtraction risks killing scaffolding that future agentic work will need to rebuild. The audit therefore distinguishes three categories beyond DELETE/MERGE/KEEP:

- **SCAFFOLDING**: Container/schema files whose shape future agentic workflows will need (e.g., a state-file pattern, a protocol template, a coordination ledger). Light current usage is acceptable if the shape is right. Default action: KEEP with a one-line "future use" justification naming the specific L3-L5 workflow that will inhabit it.
- **INHABITANT**: Content living inside scaffolding (e.g., a specific market's state, a specific protocol's current parameters). Evaluated on current usage. Unused inhabitants are DELETE candidates even if the scaffolding stays.
- **METAPHOR-ONLY**: Files whose only reason for existing is to complete the anatomical framing (body-diagram.md, body.md-as-navigation-layer, nervous-system.md as a concept). Default action: DELETE. The metaphor was a transition tool, not a permanent structure. Future agents will reference data and schemas, not anatomy.

This is Mario's point applied with discipline: cut today's slop, keep tomorrow's scaffolding. The test is not "does Richard use this today?" but "does this file contain information, a schema, or a pattern that a working system — now or in 18 months — would need to rebuild if deleted?"

## Glossary

- **Body metaphor**: The anatomical organization in `~/shared/context/body/` — body.md (navigation), brain.md, heart.md, gut.md, amcc.md, memory.md, spine.md, device.md, hands.md, eyes.md, nervous-system.md, body-diagram.md, roster.md, changelog.md, amazon-politics.md (15 files, 3,496 lines total).
- **Protocol layer**: The files in `~/shared/context/protocols/` — 30 markdown files totaling 6,429 lines, covering morning backend (am-auto, am-backend, am-backend-parallel), asana sync, signal routing, state file engines, slack ingestion, hedy sync, and more.
- **Agent-owned artifact**: A file the agent is expected to read AND modify as part of its operating loop — e.g., amcc.md (streak tracking), gut.md and heart.md (owned by karpathy agent), hard-thing-selection (scoring math).
- **Reference organ**: A file the agent reads but never modifies — e.g., memory.md (relationship graph), device.md (tool inventory), roster.md (people index).
- **Kill list**: The output of this audit — a file at `.kiro/specs/system-subtraction-audit/kill-list.md` with each candidate file tagged DELETE, MERGE (into what), or KEEP (why). Richard reviews and approves or vetoes each line.
- **Structural vs cosmetic** (from soul.md #2): Structural changes alter defaults, friction, or pre-loaded content. Cosmetic changes rename, reorder, or add emojis. This audit is structural by definition — it removes pre-loaded content.
- **Scaffolding**: A file whose value comes from its shape (schema, pattern, template) rather than its current content. A state-file template that each market instantiates is scaffolding. The metaphor of "body" is not scaffolding — it's a frame that doesn't produce downstream structure.
- **Inhabitant**: A file whose value comes from its current content (a specific market's performance data, a specific protocol's current parameters, a specific meeting's minutes). Inhabitants can become stale; scaffolding generally doesn't.
- **Future-inhabited**: A scaffolding file lightly used today because the agentic workflows that will inhabit it haven't been built yet. Legitimate KEEP candidate *if* the future workflow can be named; otherwise speculative and subject to DELETE.
- **Path referrer**: A file that references the target via a resolvable path — includes `#[[file:...]]`, absolute paths starting with `~/` or `/home/`, or relative paths with a directory component (`protocols/foo.md`). Bare filenames in prose do NOT count as path referrers.
- **Name mention**: A file that mentions the target's filename in prose without a resolvable path (e.g., "see brain.md" with no directory). Informational, not load-bearing.
- **Latent referrer**: A path referrer inside a disabled hook, a manual-only steering file that's rarely invoked, or another file that does not fire during normal operation. The reference exists but dead-weights the count.
- **Documentation referrer**: A path referrer inside a wiki article, spec document, README, or other descriptive file. The reference is a citation (naming the file for discussion), not a load instruction. Does not save a file from ORPHAN status.
- **Active referrer**: A path referrer inside a live execution path — enabled hook, auto-included steering, file that's loaded by the agent during any normal session. Excludes latent and documentation referrers.
- **Circular-orphan cluster**: A set of files that only path-reference each other, with no active path referrer from outside the set. Treated as collectively orphaned; no member can save another by mutual reference.
- **Workflow dependency**: A file whose deletion causes a workflow (agent run, hook execution, protocol step) to fail or degrade. Distinct from a reference dependency, which only requires editing the referrer to remove the mention.
- **Broken reference**: A path referrer pointing to a file that does not exist on disk. These are bugs already present in the system and are surfaced by the audit as a separate class (not DELETE candidates — the file is already gone; the referrer needs to be fixed).
- **Duplication group**: A set of files with a shared filename stem and variant suffixes (`am-auto.md`, `am-backend.md`, `am-backend-parallel.md`) OR >50% H1/H2 heading overlap. Requires a surviving member designated before the group can be partially deleted.
- **Template + instances**: A special duplication-group shape where one member (typically markedly larger and cross-referenced by the others) is a parameterizable pattern (the template) and the smaller members are concrete instantiations (the instances). The template is SCAFFOLDING; instances are INHABITANTs evaluated independently. Templates are NOT collapsed into their instances nor vice versa.
- **Empty shell**: A file with fewer than 10 lines of non-frontmatter content. Default DELETE — stub with no content earns nothing.
- **Approval signal**: An explicit marker on a kill-list row indicating Richard accepts the recommended action. Absence of a veto is NOT an approval signal. Execution only applies rows with an explicit APPROVE tag.

## Scope

### In scope

- Full inventory of the 4 layers under review: body organs (15), protocols (30), hooks (23), steering files (27). Each file listed with path, line count, last-modified date, and known consumers (agents, hooks, or protocols that reference it).
- Classification of each file into one of: KEEP (justified), MERGE (content should fold into another file), DELETE (no longer earns its place), UNCLEAR (needs Richard's call).
- Duplication detection: identify file groups that do the same job (e.g., am-auto + am-backend + am-backend-parallel; the three state-file protocols; the multiple WBR hooks). Template + instances groups are detected and protected from collapse.
- Orphan detection: files no active agent, hook, or protocol references.
- Referrer analysis across an expanded scope: `~/.kiro/**`, `~/shared/context/**`, `~/shared/wiki/**`, `~/shared/tools/**`, `~/shared/scripts/**`, `~/shared/dashboards/**`. Scripts that import or read context files are first-class referrers — a file referenced only by a live script is NOT orphaned.
- Broken reference detection: any path referrer in any scanned file that points to a non-existent target is surfaced as a separate class of finding. These are bugs already in the system, not audit candidates.
- Latent vs active referrer distinction: referrers inside disabled hooks or manual-only steering files are tagged LATENT and do NOT save a file from ORPHAN classification on their own.
- Empty-shell detection: files with fewer than 10 lines of non-frontmatter content are flagged for default DELETE.
- Output: a single kill-list.md at the spec directory, one row per file, with the candidate action, approval semantics, and a one-line rationale Richard can approve, veto, or defer.

### Out of scope

- Any actual deletion. The audit produces findings; Richard makes the call; execution is a separate session.
- Changes to steering files' auto-inclusion rules (those are governed by frontmatter, not the scope of this audit — we can identify candidates but don't touch the auto-inclusion mechanism here).
- Rewriting or restructuring retained files — if a file stays, it stays as-is.
- Merging the body metaphor into a new metaphor. If the body layer is partially killed, what remains keeps its current names. No rename churn.
- The DuckDB schema, wiki files, tools/scripts, or dashboards — those are the "work system" (per the 2026-04-21 audit) and are out of scope. This audit only covers the "agent-soul system" layers.
- Hard-thing-selection protocol, karpathy's experiment queue, heart.md, gut.md content edits — per soul.md routing rules, only karpathy modifies those. This audit can FLAG them for review but cannot recommend deletion without karpathy's input.

## Requirements

### Requirement 1: Inventory

**User Story**: As Richard, I want a flat inventory of every file in the 4 target layers so I can see the surface area in one place, not navigate nested trees to discover it.

#### Acceptance Criteria

1. WHEN the inventory is produced, THEN it SHALL list every file in `~/shared/context/body/`, `~/shared/context/protocols/`, `~/.kiro/hooks/`, and `~/.kiro/steering/` with columns: path, lines, last_modified, category (body/protocol/hook/steering).
2. WHEN a file is listed, THEN the entry SHALL include a one-line purpose drawn from the file's first heading or first paragraph — not a summary generated by the agent, the file's own stated purpose.
3. WHEN the inventory is produced, THEN it SHALL be sorted by category, then by line count descending, so the largest files in each layer surface first (those are the highest-cost candidates).
4. WHEN the inventory is produced, THEN the total line count per layer and across all layers SHALL be reported at the top — so Richard sees the aggregate tax, not just individual files.

### Requirement 2: Referrer Graph

**User Story**: As Richard deciding what to cut, I want to know who actually references each file so I can judge whether removing it breaks something or is genuinely unused.

#### Acceptance Criteria

1. WHEN the referrer graph is produced, THEN each file in the inventory SHALL have a `referenced_by` list showing every other file (steering, agent definition, hook, protocol, body organ, or script) that references it via a resolvable path.
2. WHEN the referrer graph is produced, THEN it SHALL distinguish four match types: `path` (resolvable path reference in a live-execution file, load-bearing), `name` (bare filename in prose, informational), `latent` (path reference inside a disabled hook or a manual-only steering file, dead weight during normal operation), and `documentation` (path reference inside a wiki article, spec, README, or other descriptive file — a citation, not a load instruction).
3. WHEN a path reference appears inside the audit's own spec directory (`.kiro/specs/system-subtraction-audit/`) OR inside any other `.kiro/specs/**` file, THEN it SHALL be classified as `documentation` — specs cite paths descriptively and must not inflate referrer counts.
4. WHEN a file has zero ACTIVE path referrers AND is not auto-included by steering frontmatter, THEN it SHALL be flagged ORPHAN — strongest candidate for deletion. Latent, name-only, and documentation referrers do NOT save a file from ORPHAN status on their own.
5. WHEN a file is referenced only by other files that are themselves DELETE candidates, THEN it SHALL be flagged SECONDARY — its referrers die first, then it becomes orphaned.
6. WHEN a set of files only path-references each other (circular cluster) AND no file outside the set actively references any member, THEN the entire set SHALL be flagged CIRCULAR-ORPHAN and treated as orphaned en bloc. A cycle of references among candidates for deletion does NOT save any member from ORPHAN status.
7. WHEN a file is referenced by 3+ active path referrers, THEN it SHALL be flagged LOAD-BEARING — deleting it requires updating all referrers, raising the cost of removal.
8. WHEN the referrer search is scoped, THEN it SHALL include `~/.kiro/**`, `~/shared/context/**`, `~/shared/wiki/**`, `~/shared/tools/**`, `~/shared/scripts/**`, and `~/shared/dashboards/**`. A file referenced only by a script in `~/shared/tools/` is NOT orphaned.
9. WHEN a path referrer points to a file that does not exist on disk, THEN it SHALL be recorded as a BROKEN REFERENCE — surfaced in a separate section of the kill-list as a pre-existing bug, not as an audit candidate.
10. WHEN the audit completes, THEN the kill-list SHALL explicitly disclose reference sources NOT searched — specifically DuckDB rows, Asana task descriptions, Slack messages, and Outlook email bodies. These sources MAY contain references that the audit cannot see. Files referenced only by these external sources will appear orphaned; Richard calibrates confidence accordingly.

### Requirement 3: Duplication Detection

**User Story**: As Richard looking at protocols I know are redundant (am-auto vs am-backend vs am-backend-parallel), I want the audit to call out the duplication groups explicitly so I don't have to find them myself — AND I want it to recognize when a group is actually a template-plus-instances pattern that should NOT be collapsed.

#### Acceptance Criteria

1. WHEN files have overlapping names (same stem, different suffix like `-v2`, `-parallel`, `-new`), THEN they SHALL be grouped as a DUPLICATION CANDIDATE with a note "pick one, kill the others".
2. WHEN files share >50% of their section headings (measured by markdown H1/H2 overlap), THEN they SHALL be grouped as CONTENT OVERLAP with a note identifying the shared headings.
3. WHEN a duplication group contains one file that is markedly larger AND is cross-referenced by the smaller files (via path referrers), THEN the group SHALL be reclassified as TEMPLATE + INSTANCES. The large file is SCAFFOLDING (KEEP). The smaller files are INHABITANTs evaluated individually on current usage. This group is NOT collapsed.
4. WHEN the protocol layer has known duplication groups (am-backend variants, state-file variants, slack-history-backfill + slack-conversation-intelligence overlap), THEN the audit SHALL list them explicitly with a recommendation for which single file should survive — UNLESS they meet the template + instances pattern above.
5. WHEN duplication is detected, THEN the output SHALL include the aggregate line count of the duplicate group — so Richard sees "killing 2 of these 3 files saves 800 lines" rather than making him compute it.
6. WHEN a file belongs to multiple overlapping groups, THEN it SHALL be assigned to the group where collapse produces the largest net line reduction. Ties broken by most recent modification date.

### Requirement 4: Kill List Output

**User Story**: As Richard reviewing the audit, I want a single file with one line per candidate so I can go row by row and say yes/no/defer without context-switching — AND I want clear approval semantics so the execution session cannot misread my intent.

#### Acceptance Criteria

1. WHEN the kill list is produced, THEN it SHALL be a single file at `.kiro/specs/system-subtraction-audit/kill-list.md` with one row per file in the inventory, sorted first by recommended action (DELETE first, then MERGE, then UNCLEAR, then KEEP) and secondarily by confidence within action (highest-confidence DELETEs first — orphans and obvious duplicates).
2. WHEN a row is DELETE, THEN it SHALL include a one-line rationale, the active-referrer count, an impact note, and a confidence indicator (HIGH for orphan/duplicate, MEDIUM for METAPHOR-ONLY, LOW when edge cases apply).
3. WHEN a row is MERGE, THEN it SHALL name the target file the content should fold into — no MERGE without a target.
4. WHEN a row is UNCLEAR, THEN it SHALL state the specific question Richard needs to answer AND a default action if the question goes unanswered within 30 days. UNCLEAR without a default is not a valid classification.
5. WHEN a row is KEEP, THEN it SHALL include a brief justification — why this file earns its place despite the subtraction bias. KEEP is the action that requires justification in this audit, not DELETE.
6. WHEN the kill list is produced, THEN the top of the file SHALL contain summary counts: total files reviewed, DELETE count, MERGE count, UNCLEAR count, KEEP count, BROKEN REFERENCE count, KARPATHY-FLAG count, and estimated total lines removed if all DELETE/MERGE candidates are approved.
7. WHEN the kill list is produced, THEN it SHALL support unambiguous bulk approval — Richard can mark groups of rows as approved, vetoed, or deferred without editing each row individually. The execution session MUST only act on explicitly approved rows; absence of veto is NOT approval. The exact syntax is a design decision.
8. WHEN the kill list is produced, THEN it SHALL be chunked visually by layer (body / protocols / hooks / steering) so Richard can review one layer per sitting if preferred.
9. WHEN the kill list is produced, THEN each row SHALL have a stable identifier so bulk-approval references are unambiguous. The exact identifier format is a design decision.

### Requirement 5: Body Metaphor Evaluation

**User Story**: As Richard questioning whether the body metaphor earns its place, I want the audit to evaluate each body organ against three questions: does it contain information I use today, does it provide scaffolding future agentic workflows will inhabit, or does it exist only to complete the anatomy?

#### Acceptance Criteria

1. WHEN each body organ is evaluated, THEN it SHALL be classified as one of:
   - INFORMATION: Contains facts currently used (memory.md relationship graph, device.md tool inventory, roster.md people index, amazon-politics.md stakeholder map).
   - SCAFFOLDING: Provides a shape future agentic workflows will need — name the specific L3-L5 workflow (e.g., changelog.md as an audit trail pattern future autonomous agents will need).
   - METAPHOR-ONLY: Exists to complete the anatomical frame (body-diagram.md, body.md's role as navigation layer, nervous-system.md as concept). Default DELETE.
2. WHEN an organ is METAPHOR-ONLY, THEN it SHALL default to DELETE. The anatomical frame was a transition tool; agentic workflows of the future reference data and schemas, not body parts.
3. WHEN an organ is INFORMATION or SCAFFOLDING, THEN KEEP is the default action with its current filename — no rename churn. "Cleaner names" is a cosmetic change (soul.md #2) and fails the structural bar.
4. WHEN the body layer is evaluated, THEN the audit SHALL apply two tests using WORKFLOW DEPENDENCY (not reference dependency):
   - Current Usage Test: "If this file were deleted tomorrow, what current *workflow* (not reference) would fail or degrade?" A broken reference that can be fixed by editing 1-2 lines in the referrer FAILS this test. Only a workflow that stops producing output PASSES.
   - Future Workflow Test: "If this file were deleted tomorrow, what specific L3-L5 agentic workflow would have to rebuild equivalent structure? Name the workflow."
   A file that fails both tests is METAPHOR-ONLY regardless of its name.
5. WHEN the body organ evaluation is complete, THEN the audit SHALL explicitly name — for each retained organ — the specific L3-L5 workflow it supports. Vague "future agents might need this" is not sufficient. If no concrete workflow can be named, the file fails the SCAFFOLDING test.
6. WHEN an always-auto-included steering file references a candidate DELETE organ (e.g., soul.md `#[[file:...]]` reference to body.md), THEN the organ SHALL NOT be a simple-row DELETE. It SHALL be classified UNCLEAR with default action KEEP and a note: "Coordinated removal requires a separate spec — this audit cannot safely delete a file referenced from always-auto-loaded steering in a single row." Richard can elevate to a follow-on spec if he wants the coordinated removal.

### Requirement 6: Protocol Consolidation Targets

**User Story**: As Richard knowing the protocol layer has obvious consolidation opportunities (three morning-backend files, three state-file files), I want the audit to name specific merges, not just flag duplication generally.

#### Acceptance Criteria

1. WHEN the protocol layer is evaluated, THEN the audit SHALL explicitly propose a consolidation for the am-backend family (pick one of am-auto.md, am-backend.md, am-backend-parallel.md; delete the other two).
2. WHEN the state-file protocols are evaluated, THEN the audit SHALL propose either merging the three market variants (state-file-au-ps.md, state-file-mx-ps.md, state-file-ww-testing.md) into one parameterized protocol, OR flag that per-market variants are load-bearing and should stay — with the rationale for either call.
3. WHEN the slack protocols are evaluated, THEN the audit SHALL assess whether slack-conversation-intelligence.md, slack-history-backfill.md, slack-deep-context.md (steering), and slack-knowledge-search.md (steering) have genuine separate jobs or are a consolidation candidate.
4. WHEN the audit proposes a protocol consolidation, THEN it SHALL identify every hook and agent that references the candidates — so Richard knows the blast radius of the merge before approving.

### Requirement 7: Karpathy-Protected Files

**User Story**: As Richard, I respect the routing rule that only karpathy modifies heart.md, gut.md, the experiment queue, and the hard-thing-selection protocol. I want this audit to respect that boundary — flag them, don't recommend action.

#### Acceptance Criteria

1. WHEN a karpathy-protected file is encountered (heart.md, gut.md, experiment queue files, hard-thing-selection.md), THEN it SHALL be classified KARPATHY-FLAG with no recommended action.
2. WHEN karpathy-protected files are flagged, THEN the kill list SHALL include a separate section "For karpathy review" listing them with the audit's observations AND their active-referrer count, line count, and last-modified date — so Richard has full context when routing to karpathy.
3. WHEN the audit completes, THEN Richard is free to route those flags to karpathy in a separate session — this audit doesn't presume authority over that scope.

### Requirement 8: Broken Reference Detection

**User Story**: As Richard cleaning up the system, I want to know which references in the system already point nowhere so I can fix them — the audit surfaces latent breakage that wasn't caused by this cleanup.

#### Acceptance Criteria

1. WHEN the referrer graph is built, THEN every path referrer SHALL be resolved against the filesystem. Any reference pointing to a non-existent target SHALL be recorded as a BROKEN REFERENCE.
2. WHEN broken references are recorded, THEN they SHALL be grouped by the referring file — so Richard sees "soul.md contains 2 broken references" rather than scattered rows.
3. WHEN the kill-list is produced, THEN it SHALL include a "Broken references to fix" section listing each broken reference with: referring file, broken path, line number if available, and a suggested action (remove the reference, update to a correct path, or create the target).
4. WHEN broken references are surfaced, THEN they SHALL NOT be treated as DELETE candidates — the file is already gone. The fix is editing the referrer.

### Requirement 9: Execution Safety

**User Story**: As Richard approving deletions, I want guarantees that the execution session cannot silently break the system or lose content — approvals must be explicit, execution must be ordered safely, MERGE must preserve unique content, and interrupted runs must be resumable without re-doing completed work.

#### Acceptance Criteria

1. WHEN the execution session reads the approved kill-list, THEN it SHALL only act on rows with an explicit APPROVE signal. Absence of veto is NOT approval.
2. WHEN multiple deletions are approved, THEN execution SHALL proceed in dependency order: files with zero path referrers first (leaves), files with referrers last (load-bearing). If a load-bearing file is approved for deletion, every referrer MUST be either also approved for deletion OR explicitly approved for in-place edit (removing the reference) in the same execution session.
3. WHEN a load-bearing DELETE is approved but one or more referrers are still UNCLEAR or un-approved, THEN execution SHALL SKIP that DELETE, log it as "blocked on referrer resolution," and continue with other rows. The blocked row remains in the kill-list for the next cycle.
4. WHEN a MERGE is executed, THEN the execution session SHALL perform an atomic sequence: (a) read source, (b) identify content in source that is not present in target, (c) append non-duplicate content to target in a clearly-marked section, (d) delete source. If step (b) finds conflicting content between source and target, execution STOPS for that row and flags it for manual review.
5. WHEN execution encounters a row whose referrers are no longer a matching state (e.g., a new referrer appeared after the kill-list was generated, or a referrer was deleted by another process), THEN that row SHALL be skipped and logged for the next audit cycle rather than executed against stale assumptions.
6. WHEN the execution session is interrupted (network failure, agent timeout, manual cancel, or system restart), THEN a subsequent resume SHALL skip rows already completed (recorded in the execution log) and continue with remaining approved rows. Execution is idempotent: re-running against an unchanged kill-list produces zero additional changes.
7. WHEN execution completes OR is interrupted, THEN it SHALL write a running completion log at `.kiro/specs/system-subtraction-audit/execution.log` recording every file deleted, every file merged (with content-fold summary), every row skipped (with reason), every broken-reference fix applied, and the status of each row (COMPLETED / SKIPPED / BLOCKED / PENDING). The log is append-only within a run and is the source of truth for resume.

### Requirement 10: UNCLEAR Default Actions

**User Story**: As Richard, I don't want the kill-list to create permanent purgatory — every UNCLEAR row must have an exit path even if I never answer the question.

#### Acceptance Criteria

1. WHEN a row is classified UNCLEAR, THEN it SHALL include a DEFAULT-IF-UNANSWERED action — either DELETE (if the risk of keeping is higher) or KEEP (if the risk of deleting is higher) — with a time horizon (default: 30 days).
2. WHEN the execution session runs more than the UNCLEAR time horizon after kill-list generation, THEN rows still tagged UNCLEAR SHALL be acted on per their default action and logged as "auto-resolved UNCLEAR."
3. WHEN no meaningful default can be named for an UNCLEAR row, THEN the classifier SHALL NOT use UNCLEAR — the file should be classified DELETE or KEEP with LOW confidence instead.

### Requirement 11: Review Ergonomics

**User Story**: As Richard reviewing 95+ rows, I want the kill-list structured so I can review it in reasonable time without losing focus — chunked by layer, priority-sorted within chunks, and summary metrics visible at the top.

#### Acceptance Criteria

1. WHEN the kill-list is produced, THEN it SHALL be chunked into four visible sections by layer (body / protocols / hooks / steering) so Richard can review one sitting per layer if preferred.
2. WHEN rows within a section are sorted, THEN HIGH-confidence DELETEs (orphans, obvious duplicates) SHALL appear first within the DELETE subsection — easy wins surface first.
3. WHEN the kill-list summary appears at the top, THEN it SHALL include per-layer sub-totals (e.g., "body layer: 3 DELETE, 2 MERGE, 1 UNCLEAR, 9 KEEP"), a quantified impact ("approving all DELETE + MERGE removes ~2,400 lines, 32% of current surface"), and the bulk-approval block template.
4. WHEN rows reference prior-session context (e.g., am-auto.kiro.hook already disabled 2026-04-21), THEN the row SHALL note that context so Richard doesn't re-litigate decisions he already made. The source of this context is the inventory phase's read of `~/shared/context/intake/session-log.md` and any git log entries within the last 90 days touching the target file.

### Requirement 12: Empty-Shell and Stub Detection

**User Story**: As Richard cleaning up accumulated skeletons, I want files that were created but never populated with real content to surface as default DELETE — stubs don't earn their place.

#### Acceptance Criteria

1. WHEN a file has fewer than 10 lines of non-frontmatter content, THEN it SHALL be flagged EMPTY-SHELL with default action DELETE.
2. WHEN an EMPTY-SHELL file has active referrers, THEN the row SHALL note that those referrers need updating — the empty file is still blast-radius-aware.
3. WHEN a file's first heading is a placeholder (e.g., `# TODO`, `# Placeholder`, `# FIXME`), THEN the purpose-extraction SHALL mark purpose_missing and classification SHALL treat it as likely EMPTY-SHELL pending content check.

### Requirement 13: Steering Inclusion-Value Handling

**User Story**: As Richard knowing the steering layer has several inclusion modes (always, auto, manual, fileMatch, and some files with no frontmatter at all), I want the audit to handle each explicitly so classifications aren't quietly wrong.

#### Acceptance Criteria

1. WHEN a steering file's frontmatter is parsed, THEN the audit SHALL recognize these inclusion values as "loaded every chat": `always`, `auto`, or absent frontmatter. Each of these SHALL be normalized to a single `inclusion_mode: "auto"` in the data model.
2. WHEN a steering file's frontmatter specifies `manual` or `fileMatch`, THEN the audit SHALL recognize these as "conditionally loaded" and normalize to `inclusion_mode: "conditional"` in the data model, with the original value preserved in `inclusion_mode_raw`.
3. WHEN a steering file has an unknown inclusion value (anything not in the enumerated list), THEN the classifier SHALL tag the file `needs_revisit: true` rather than guess.
4. WHEN a steering file is auto-loaded (`inclusion_mode: "auto"`) AND contains rules the agent must follow in every interaction, THEN it SHALL be classified KEEP.
5. WHEN a steering file is auto-loaded BUT its rules are only relevant in specific contexts, THEN it SHALL be classified UNCLEAR with the question "auto-included but not universally needed — should this be conditional or manual?" with default KEEP if unanswered.

### Requirement 14: Post-Audit Artifact Hygiene

**User Story**: As Richard applying the Subtraction Before Addition principle to this audit itself, I don't want the audit's own artifacts (intermediate JSONs, spec directory, kill-list) to accumulate as new complexity after the audit is executed.

#### Acceptance Criteria

1. WHEN the execution session completes successfully (all approved rows applied or safely skipped), THEN the intermediate working artifacts (`inventory.json`, `referrers.json`, `classified.json`, `duplication_groups.json`, `broken_refs.json`) SHALL be deleted.
2. WHEN the execution session completes, THEN the spec directory (`.kiro/specs/system-subtraction-audit/`) SHALL be archived — moved to `~/shared/wiki/agent-created/archive/system-subtraction-audit-YYYY-MM-DD/` — with the completion log preserved as the record of what was done.
3. WHEN a new audit cycle begins in the future, THEN it SHALL detect whether a prior uncompleted audit exists (prior `kill-list.md` present, prior `execution.log` not marked complete). If yes, the new audit SHALL NOT proceed until the prior audit is either completed or its artifacts explicitly discarded by Richard. Overlapping audits are not permitted.
4. WHEN the audit is archived, THEN the durable artifact of value is git history plus the archived completion log — not the live spec directory. requirements.md and design.md serve their purpose during the audit and then become part of the archive.

## Design Constraints

1. **No deletion this spec**. This audit produces findings only. Execution is a separate session after Richard approves the kill list row by row.
2. **No new metaphors, no rewrites, no rename churn**. Files either survive with their current names or get deleted. If a MERGE is proposed, the target is an existing file; the merged content absorbs into the target's structure.
3. **Subtraction-biased, not future-blind**. Default action on a marginal file is DELETE. KEEP must be justified. Acceptable KEEP justifications: (a) currently used by Richard or an active agent, (b) SCAFFOLDING for a *named* L3-L5 workflow. "Might be useful later" without a concrete workflow is not sufficient.
4. **Evidence over opinion**. A DELETE recommendation needs a concrete rationale (orphaned, duplicate, metaphor-only). A KEEP-for-scaffolding recommendation needs a named future workflow. "I think this feels bloated" and "I think we might need this" both fail the bar.
5. **Blast-radius aware**. Every DELETE/MERGE candidate lists its active referrers. Richard sees the cost of removal before approving it.
6. **Single output file**. The kill list is one markdown file, flat table-like format, sortable by eye. Not a multi-file spec with its own navigation layer — that would be the recursion Mario's warning about.
7. **Portability**. A new AI on a different platform reading kill-list.md should understand what each row means and how to execute an approved DELETE without needing access to this spec's supporting documents.
8. **Scaffolding survives lean usage**. A file that's lightly used today but has the right shape for future agentic workflows is a KEEP — not "maybe we'll need it" but "the L3 tool-adoption workflow will write to this ledger" or "the L5 autonomous market-update workflow will read this schema." The future workflow must be nameable.
9. **Metaphor is a transition tool**. The body/brain/heart/gut framing helped build the system. It is not a permanent structure. Files whose only justification is completing the anatomy fail the audit. Files that happen to live inside the metaphor but contain information or scaffolding keep their current names and stay.
10. **Workflow dependency trumps reference dependency**. A file earns KEEP by supporting a workflow, not by being referenced. If the only cost of deletion is editing 1-2 lines in a referrer, the file does not pass the Current Usage Test. Reference counts determine blast radius, not merit.
11. **Explicit approval, never implicit**. The execution session reads APPROVE tags and the bulk-approval block. It does not infer approval from silence. A half-reviewed kill-list is a non-executable kill-list.
12. **Safe execution order**. Leaves before load-bearing files. Referrer updates before referent deletes. MERGE preserves unique content or stops. The audit is allowed to cause no harm it would not catch in review.
13. **Time-boxed UNCLEAR**. Every UNCLEAR row has a default. The kill-list cannot decay into permanent purgatory.
14. **Broken references are surfaced, not audited**. The audit finds pre-existing broken references as a side-effect and reports them, but does not add them to the DELETE/MERGE/KEEP classification — the file is already gone; the fix is editing the referrer.
15. **Implementation details stay in design.md**. Requirements specify what the system must do; design.md specifies how. Concrete syntaxes (bulk-approval format, row identifier scheme, regex patterns, data-model field names) belong in design, not here.
16. **Resumable, idempotent execution**. Execution state is tracked per row. Interrupted runs resume without re-doing completed work. Re-running against an unchanged kill-list produces zero additional changes.
17. **Audit artifacts do not become new complexity**. After execution completes, intermediate files are deleted, the spec directory is archived, and only git history plus the completion log survive as durable record.
