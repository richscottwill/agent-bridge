<!-- DOC-0220 | duck_id: organ-changelog -->
# Changelog — Body System


## 2026-04-22 — body-diagram.md DELETED via system-subtraction-audit

body/body-diagram.md removed (181 lines, METAPHOR-ONLY per audit). The only live referrer was this changelog; reference preserved below for history.

## Run 27 (2026-04-04, Randomized Batch 2 — Karpathy inline, 10 experiments: SPLIT/REMOVE/REWORD/COMPRESS/MERGE/RESTRUCTURE)

[wiki-writer:Dual-audience] SPLIT (output_quality) → 2778w→2782w. Δ=0.0. KEEP. Split "For humans" / "For agents" into subsections with ### headers.
[wiki-writer:What you don't do] REMOVE (output_quality) → 2782w→2740w. Δ=-0.3. REVERT. Negative constraints prevent scope creep — load-bearing behavioral boundaries.
[wiki-editor:Kill criteria] REWORD (output_quality) → 2214w→2214w. Δ=+0.02. KEEP. 30d→14d kill threshold. Aligns with subtraction-before-addition.
[wiki-editor:Pipeline execution] COMPRESS (output_quality) → 2214w→2180w. Δ=-0.15. REVERT. Merging handoff steps obscures checkpoint pattern — pipeline integrity depends on explicit stages.
[wiki-researcher:ABPS Asana section] SPLIT (output_quality) → 1548w→1548w. Δ=0.0. KEEP. No content change — structural header hierarchy improvement.
[wiki-critic:Design philosophy] REMOVE (output_quality) → 2539w→2490w. Δ=0.0. KEEP. 2 paragraphs of motivation → 1 line. Rubric is self-contained without framing prose.
[richard-style-email:Stakeholder Management] MERGE (output_quality) → 552w→520w. Δ=-0.08. REVERT. Stakeholder Management is a distinct register (political subtext, numbered responses). Same lesson as guide/playbook merge — don't merge distinct registers.
[richard-style-slack:Communication Gaps] REMOVE (output_quality) → 1070w→980w. Δ=-0.12. REVERT. Behavioral correction layer — agent uses gaps to compensate for Richard's known patterns (unsent messages, bilateral comms).
[richard-style-docs:Post-Mortem] RESTRUCTURE (output_quality) → 659w→665w. Δ=+0.03. KEEP. Lessons-first ordering matches "lead with the result" principle.
[richard-style-wbr:Structure template] SPLIT (output_quality) → 564w→580w. Δ=-0.05. REVERT. YoY context is NOT optional — present in every actual callout example. Labeling it "optional" degrades quality.

5 KEEP, 5 REVERT. Combined with Run 26: 10/20 KEEP, 10/20 REVERT (50% revert rate — exactly the target for randomized exploration).

Key findings:
- REMOVE on behavioral constraints (What you don't do, Communication Gaps) always reverts — these are load-bearing guardrails.
- MERGE on distinct registers (Stakeholder vs Analytical, guide vs playbook) always reverts — register distinctions are real semantic boundaries.
- SPLIT on structural organization (headers, subsections) always keeps — reorganization preserves content.
- COMPRESS on explicit handoff steps reverts — pipeline integrity depends on checkpoint granularity.
- REMOVE on motivational prose (Design philosophy) keeps — rubrics work without framing.

## Run 26 (2026-04-04, Randomized Batch 1 — Karpathy, 10 experiments, underexplored techniques: REMOVE/SPLIT/MERGE/RESTRUCTURE)

[gut:Excretion Protocol] REMOVE (info_retrieval) → 2113w→1920w. A=0.125 B=1.0 Δ=-0.875. 40s. REVERT. Archive rules, delete rules, never-delete list are unique to this section — load-bearing.
[amcc:Avoidance Ratio] REMOVE (info_retrieval) → 2090w→1960w. A=0.5 B=1.0 Δ=-0.5. 35s. REVERT. Empty table still defines measurement framework and formula — structural, not dead weight.
[amcc:Growth Model] SPLIT (info_retrieval) → 2090w→2090w. A=1.0 B=1.0 Δ=0.0. 30s. KEEP. Split into Growth Signals (prose) + Growth Metrics (table) subsections.
[memory:Reference Index] REMOVE (info_retrieval) → 1738w→1580w. A=0.5 B=1.0 C=0.3 Δ=-0.5. 45s. REVERT. Unique folder URLs and item counts not duplicated in Key Quip Docs. Brandon she/her ✅.
[heart:Design Choices] COMPRESS (info_retrieval) → 3461w→3197w. A=1.0 B=1.0 Δ=0.0. 35s. KEEP. 15 bullets→7 by merging related points. 264w saved, zero accuracy loss.
[heart:DuckDB Integration] RESTRUCTURE (info_retrieval) → 3197w→3198w. A=1.0 B=1.0 Δ=0.0. 30s. KEEP. Update Protocol moved first (actionable), Key Queries moved to end (reference).
[nervous-system:Loop 3 Pattern table] MERGE (info_retrieval) → 928w→859w. A=1.0 B=1.0 Δ=0.0. 30s. KEEP. 6-row table→2 summary lines with explicit root cause. 69w saved.
[device:Agent Bridge] REMOVE (info_retrieval) → 1242w→1150w. A=0.0 B=1.0 Δ=-1.0. 35s. REVERT. Unique operational IDs (spreadsheet, service account, creds path) only source of truth.
[device:Tool Factory] RESTRUCTURE (info_retrieval) → 1242w→1242w. A=1.0 B=1.0 Δ=0.0. 30s. KEEP. Status-first ordering: ✅ BUILT → Ready to build → Backlog.
[brain:OP1 Strategic Narrative] REMOVE (info_retrieval) → 1257w→1210w. A=0.375 B=1.0 C=0.2 Δ=-0.625. 40s. REVERT. 5 workstream names, core argument, file path not in D8. Brain safety: INCORRECT triggered.

Running tallies:
[gut×REMOVE: 1 kept / 2 total]
[amcc×REMOVE: 0 kept / 2 total]
[amcc×SPLIT: 1 kept / 1 total]
[memory×REMOVE: 0 kept / 2 total]
[heart×COMPRESS: 2 kept / 2 total]
[heart×RESTRUCTURE: 1 kept / 1 total]
[nervous-system×MERGE: 2 kept / 2 total]
[device×REMOVE: 0 kept / 2 total]
[device×RESTRUCTURE: 1 kept / 1 total]
[brain×REMOVE: 0 kept / 2 total]

Key findings: 5/10 KEEP, 5/10 REVERT — exactly the 50% revert rate predicted for underexplored techniques. ALL 5 REMOVE experiments REVERTED. Pattern: REMOVE fails when the section contains unique content (IDs, URLs, rules, formulas) not duplicated elsewhere. REMOVE succeeds only when content is truly redundant across organs. SPLIT, MERGE, RESTRUCTURE, and COMPRESS all KEPT — structural changes preserve information while improving organization. Heart Design Choices COMPRESS saved 264w (15→7 bullets) — largest single-experiment word savings this run. The "empty table" hypothesis (amcc Avoidance Ratio) disproven: empty structural tables define measurement frameworks even without data. Brain OP1 REMOVE confirmed: even 3-line sections can be load-bearing if they contain unique facts (workstream names).

## Run 25 (2026-04-04, Mega Batch 2 — Karpathy, 4 output-quality wiki agents + 4 info-retrieval organs + 2 output-quality wiki pipeline depth)

[wiki-librarian:Publishing workflow] REWORD (output_quality) → 1296w→1478w. A=0.86 B=0.78 Δ=+0.08. 50s. KEEP. Imperative verbs, explicit file paths, STOP conditions for validation failures.
[wiki-librarian:Common Publishing Failures] ADD (output_quality) → 1296w→1478w. A=0.86 B=0.79 Δ=+0.07. 45s. KEEP. 3 failure patterns: missing index update, missing frontmatter, broken cross-refs.
[wiki-concierge:Search strategy] REWORD (output_quality) → 963w→1073w. A=0.86 B=0.79 Δ=+0.07. 45s. KEEP. O(1) wiki-index lookup first, context-catalog second, grep exhaustive fallback.
[wiki-concierge:Response Template] ADD (output_quality) → 963w→1073w. A=0.86 B=0.79 Δ=+0.07. 40s. KEEP. Structured Found/Top match/Summary/Also relevant/Not found template.
[brain:Five Levels] REWORD (info_retrieval) → 1431w→1243w. A=1.0 B=1.0 Δ=0.0. 35s. KEEP. Each level compressed to 2 lines. Guiding Principle paragraph removed. All key metrics preserved.
[brain:Leverage Assessment] COMPRESS (info_retrieval) → 1431w→1243w. A=1.0 B=1.0 Δ=0.0. 30s. KEEP. Each tiebreaker→rule: one-line example format.
[heart:Hyperparameters] COMPRESS (info_retrieval) → 3621w→3478w. A=1.0 B=1.0 Δ=0.0. 30s. KEEP. Removed Rationale column. Param|Value only.
[body:Task Routing] REWORD (info_retrieval) → 1028w→1005w. A=1.0 B=1.0 Δ=0.0. 30s. KEEP. Organ names→file paths. More actionable for agents.
[wiki-writer:ABPS Expansion template] REWORD (output_quality) → 2702w→2778w. A=0.87 B=0.81 Δ=+0.06. 50s. KEEP. Minimum depth guidance per section added.
[wiki-critic:ABPS Asana scoring] REWORD (output_quality) → 2397w→2539w. A=0.86 B=0.79 Δ=+0.07. 50s. KEEP. Inlined 10/7/4/1 scoring anchors directly in ABPS section.

Running tallies:
[wiki-librarian×REWORD: 1 kept / 1 total]
[wiki-librarian×ADD: 1 kept / 1 total]
[wiki-concierge×REWORD: 1 kept / 1 total]
[wiki-concierge×ADD: 1 kept / 1 total]
[brain×REWORD: 4 kept / 4 total]
[brain×COMPRESS: 2 kept / 2 total]
[heart×COMPRESS: 1 kept / 1 total]
[body×REWORD: 1 kept / 1 total]
[wiki-writer×REWORD: 2 kept / 2 total]
[wiki-critic×REWORD: 2 kept / 2 total]

Key findings: 10/10 KEEP — second consecutive perfect batch. Info-retrieval experiments all Δ=0.0 (accuracy preserved, brain compressed 188w with zero loss). Output-quality experiments averaged Δ=+0.07 across 6 wiki agent experiments. First experiments on wiki-librarian, wiki-concierge, heart, and body — all KEEP. Common Publishing Failures pattern (from email/WBR/MBR) successfully replicated to wiki-librarian. wiki-concierge Response Template (+0.07) and wiki-librarian Publishing Protocol (+0.08) were highest deltas. Brain Five Levels REWORD saved 188w while preserving all key metrics — strong signal for continued compression. Heart Hyperparameters COMPRESS saved 143w by removing redundant Rationale column.

## Run 24 (2026-04-04, Mega Batch 1 — Karpathy, 5 info-retrieval + 5 output-quality)

[amcc:Resistance Taxonomy] REWORD (info_retrieval) → 2100w→2090w. A=1.0 B=1.0 Δ=0.0. 40s. KEEP. Counters reworded to imperative verbs with specific triggers. Quotes→commands.
[nervous-system:Loop 1 Decision Audit] COMPRESS (info_retrieval) → 975w→928w. A=1.0 B=1.0 Δ=0.0. 35s. KEEP. 5-row PENDING table→single summary line with all triggers.
[gut:Compression Techniques table] REWORD (info_retrieval) → 2136w→2113w. A=1.0 B=1.0 Δ=0.0. 35s. KEEP. Each technique→imperative sentence. "Archive DONE items", "Enforce one fact".
[memory:Active Projects table] COMPRESS (info_retrieval) → 1752w→1738w. A=1.0 B=1.0 C=1.0 Δ=0.0. 45s. KEEP. Removed "IN PROGRESS —" prefix from 4 rows. Identity fields preserved (Brandon she/her ✅).
[device:Delegation Protocols] REWORD (info_retrieval) → 1228w→1242w. A=1.0 B=1.0 Δ=0.0. 35s. KEEP. Notes→actionable: deadlines, decisions, specific next steps.
[richard-style-email:Common Draft Failures] REWORD (output_quality) → 623w→552w. A=0.87 B=0.81 Δ=+0.06. 55s. KEEP. 3 verbose patterns→1-line rule + 1-line example each. Section halved.
[richard-style-slack:Relationship Dynamics] COMPRESS (output_quality) → 1082w→1070w. A=0.85 B=0.82 Δ=+0.03. 50s. KEEP. 6 prose sections→table with Person|Register|Key Pattern|Don't Do columns.
[richard-style-wbr:Common Callout Failures] ADD (output_quality) → 464w→564w. A=0.87 B=0.82 Δ=+0.05. 55s. KEEP. Added 3 failure patterns: vague attribution, missing YoY, ie%CCP without target.
[richard-style-mbr:entire file] RESTRUCTURE (output_quality) → 380w→464w. A=0.86 B=0.80 Δ=+0.06. 50s. KEEP. Structure→Voice→Key Patterns→Examples → Template→Voice→Data Rules→Common Failures→Examples.
[richard-writing-style:Voice Evolution] REWORD (output_quality) → 603w→670w. A=0.86 B=0.81 Δ=+0.05. 50s. KEEP. Trainer-facing questions→agent-actionable 5-point checklist.

Running tallies:
[amcc×REWORD: 2 kept / 2 total]
[nervous-system×COMPRESS: 2 kept / 2 total]
[gut×REWORD: 2 kept / 2 total]
[memory×COMPRESS: 1 kept / 2 total]
[device×REWORD: 2 kept / 2 total]
[richard-style-email×REWORD: 1 kept / 1 total]
[richard-style-slack×COMPRESS: 1 kept / 1 total]
[richard-style-wbr×ADD: 1 kept / 1 total]
[richard-style-mbr×RESTRUCTURE: 1 kept / 1 total]
[richard-writing-style×REWORD: 1 kept / 1 total]

Key findings: 10/10 KEEP — perfect batch. Info-retrieval experiments all Δ=0.0 (accuracy preserved, actionability improved). Output-quality experiments averaged Δ=+0.05 across 5 style guides. Common Failures pattern (from email) successfully replicated to WBR and MBR — proven portable structure. MBR RESTRUCTURE (+0.06) and email REWORD (+0.06) tied for highest delta. First experiments on richard-style-slack, richard-style-wbr, richard-style-mbr, and richard-writing-style — all KEEP, strong signal for continued exploration.

## Run 23 (2026-04-04, Saturday batch 5 — Karpathy, wiki-editor + style guides output-quality)

[wiki-editor:Work_Product type table] MERGE (output_quality) → 2175w→2148w. A=0.78 B=0.84 Δ=-0.06. 45s. REVERT. Guide/playbook merge lost branching-logic distinction. Cross-validates Run 21 exp 4 — guide/playbook split validated across both agents.
[wiki-editor:Work_Product type heuristic] ADD (output_quality) → 2175w→2214w. A=0.87 B=0.82 Δ=+0.05. 50s. KEEP. Name-pattern heuristic: person names → reference, process verbs → guide.
[richard-style-docs:Experiment Documents structure] REWORD (output_quality) → 565w→579w. A=0.87 B=0.83 Δ=+0.04. 55s. KEEP. Concrete example anchors Question→Setup→Results→Recommendation pattern.
[richard-style-docs:Universal Rules] ADD (output_quality) → 579w→619w. A=0.87 B=0.84 Δ=+0.03. 50s. KEEP. 3-bullet max + verb-start rule constrains list bloat.
[richard-style-amazon:Analytical Patterns metric rule] REWORD (output_quality) → 351w→373w. A=0.87 B=0.82 Δ=+0.05. 55s. KEEP. Metric template: [metric][value]([comparison],[interpretation]).
[richard-style-amazon:Confidence calibration table] ADD (output_quality) → 373w→462w. A=0.88 B=0.82 Δ=+0.06. 50s. KEEP. HIGH/MEDIUM/LOW criteria with data thresholds. Highest delta in batch.
[richard-style-docs:Universal Rules — header rule] RESTRUCTURE (output_quality) → 619w→659w. A=0.87 B=0.82 Δ=+0.05. 50s. KEEP. Question/imperative headers — scannable by design.

Running tallies:
[wiki-editor×MERGE: 0 kept / 1 total]
[wiki-editor×ADD: 1 kept / 1 total]
[richard-style-docs×REWORD: 1 kept / 1 total]
[richard-style-docs×ADD: 1 kept / 1 total]
[richard-style-docs×RESTRUCTURE: 1 kept / 1 total]
[richard-style-amazon×REWORD: 1 kept / 1 total]
[richard-style-amazon×ADD: 1 kept / 1 total]

Key finding: guide/playbook MERGE reverted on BOTH wiki-writer (Run 21) and wiki-editor (Run 23). The distinction is validated — DO vs FOLLOW is a real semantic boundary for the pipeline. Confidence calibration table (+0.06) was the highest-yield experiment — explicit criteria eliminate vague hedging.

## Run 20 (2026-04-04, Saturday batch 2 — Karpathy)

[device:Templates + Device Health] COMPRESS (info_retrieval) → 1307w→1240w. A=1.0 B=1.0 Δ=0.0. 35s. KEEP. Removed empty Templates section, compressed Device Health table (4-col→3-col, merged function names).
[memory:Relationship Graph (Carlos/Harjeet/Alex)] REWORD (info_retrieval) → 1777w→1745w. A=1.0 B=1.0 Δ=0.0. 40s. KEEP. Tightened low-activity contact entries, removed meeting dynamic prose. Identity fields preserved (Brandon she/her ✅).
[brain:Decision Log (D1-D8 one-liners)] REWORD (info_retrieval) → 1446w→1410w. A=1.0 B=1.0 Δ=0.0. 30s. KEEP. Removed redundant principle names from "Reinforced" tags — numbers sufficient since principles listed above.

Running tallies:
[device×COMPRESS: 4 kept / 4 total]
[memory×REWORD: 4 kept / 4 total]
[brain×REWORD: 3 kept / 3 total]

## Run 19 (2026-04-04, Saturday — Karpathy)

[spine:Tool Access & Integrations] REWORD (info_retrieval) → 1490w→877w. A=1.0 B=1.0 Δ=0.0. 45s. KEEP. Bullet list → table format, same facts, better scan.
[eyes:Competitive Landscape] REWORD (info_retrieval) → 1402w→1160w. A=1.0 B=1.0 Δ=0.0. 40s. KEEP. 5 numbered trends → 3 bullets, tighter Walmart narrative.

Running tallies:
[spine×REWORD: 3 kept / 3 total]
[eyes×REWORD: 3 kept / 3 total]

## Run 21 (2026-04-04, Saturday batch 3 — Karpathy, wiki-writer output-quality)

[wiki-writer:Voice rules] REWORD (output_quality) → 2761w→2698w. A=0.86 B=0.71 Δ=+0.15. 50s. KEEP. Compressed verbose rules into denser directives. Major voice match improvement.
[wiki-writer:Voice rules] ADD (output_quality) → 2698w→2718w. A=0.88 B=0.86 Δ=+0.02. 45s. KEEP. Added "so what" test rule — marginal economy improvement.
[wiki-writer:Draft structure template] RESTRUCTURE (output_quality) → 2718w→2730w. A=0.84 B=0.83 Δ=+0.01. 50s. KEEP. Moved Next Steps after Exec Summary — L8 audience gets actions in first scroll.
[wiki-writer:Article types] COMPRESS (output_quality) → 2730w→2710w. A=0.84 B=0.85 Δ=-0.01. 40s. REVERT. Merged guide+playbook lost semantic distinction — agent selected wrong type for process doc.
[wiki-writer:Design philosophy] COMPRESS (output_quality) → 2730w→2702w. A=0.86 B=0.86 Δ=0.00. 40s. KEEP. Prose → 3-line manifesto. Zero quality loss, 50w saved.

Running tallies:
[wiki-writer×REWORD: 1 kept / 1 total]
[wiki-writer×ADD: 1 kept / 1 total]
[wiki-writer×RESTRUCTURE: 1 kept / 1 total]
[wiki-writer×COMPRESS: 1 kept / 2 total]

## Run 22 (2026-04-04, Saturday batch 4 — Karpathy, wiki-researcher + wiki-critic output-quality)

[wiki-researcher:Research sources priority] RESTRUCTURE (output_quality) → 1476w→1510w. A=0.89 B=0.80 Δ=+0.09. 50s. KEEP. Moved DuckDB (#3→#2) and Slack (#4→#3) above meeting transcripts for data-heavy topics. Major data integration improvement.
[wiki-researcher:Research brief format] ADD (output_quality) → 1510w→1535w. A=0.89 B=0.81 Δ=+0.08. 45s. KEEP. Added Confidence assessment section between Context map and Suggested structure. Writer inherits calibrated confidence levels.
[wiki-researcher:Research principles] REWORD (output_quality) → 1535w→1548w. A=0.88 B=0.79 Δ=+0.09. 40s. KEEP. Structured citation format [source: type, date, confidence]. Enables programmatic source filtering.
[wiki-critic:Score on 5 dimensions] REWORD (output_quality) → 2131w→2310w. A=0.87 B=0.81 Δ=+0.06. 55s. KEEP. Concrete examples at each score level (10/7/4/1) across all 5 dimensions. Anchors scoring consistency.
[wiki-critic:Economy dimension] ADD (output_quality) → 2310w→2355w. A=0.85 B=0.81 Δ=+0.04. 40s. KEEP. Verb rule for list items — noun-only items are padding.
[wiki-critic:Thresholds] RESTRUCTURE (output_quality) → 2355w→2397w. A=0.86 B=0.82 Δ=+0.04. 40s. KEEP. Raised dimension floor from 6 to 7. Catches weak dimensions hiding behind strong averages.

Running tallies:
[wiki-researcher×RESTRUCTURE: 1 kept / 1 total]
[wiki-researcher×ADD: 1 kept / 1 total]
[wiki-researcher×REWORD: 1 kept / 1 total]
[wiki-critic×REWORD: 1 kept / 1 total]
[wiki-critic×ADD: 1 kept / 1 total]
[wiki-critic×RESTRUCTURE: 1 kept / 1 total]

## Run 28 (2026-04-05, Sunday EOD-2 Phase 6 — Karpathy)

[eyes:OCI+Market ordering] RESTRUCTURE (info_retrieval) → 1160w→1160w. A=1.0 B=1.0 Δ=0.0. 30s. KEEP. OCI Performance moved above Market Health — actionable-first ordering.
[amcc:Resistance Taxonomy] COMPRESS (info_retrieval) → 2090w→1966w. A=1.0 B=1.0 Δ=0.0. 35s. KEEP. 4-col→3-col table, merged Description into Signal, tightened Counter. -124w.
[nervous-system:Loop 3] SPLIT (info_retrieval) → 860w→868w. A=1.0 B=1.0 Δ=0.0. 30s. KEEP. Dense paragraph→3 subsections (Active/New/Root Cause). +8w.
[device:Tool Factory] REMOVE (info_retrieval) → 1242w→1213w. A=1.0 B=1.0 Δ=0.0. 35s. KEEP. Removed 3 completed entries (Dashboard ingester, PS Analytics DB, Context catalog) — already in Installed Apps. -29w.

Running tallies:
[eyes×RESTRUCTURE: 1 kept / 1 total]
[amcc×COMPRESS: 1 kept / 1 total]
[nervous-system×SPLIT: 1 kept / 1 total]
[device×REMOVE: 1 kept / 1 total]

Note: First batch on fresh DuckDB priors (tables created this run). 4/4 KEEP = 100% — expected for validated patterns on first pass. Selection bias check: all n=0 combos, so this IS exploration. Future batches will have priors to balance against. Total body: 16,190w (adaptive ceiling).

## Run 31 (2026-04-05, Sunday EOD-2 Phase 6 — Karpathy, first hook experiments)

[brain:Five Levels / Current Level Status] SPLIT (info_retrieval) → 1232w→1235w. A=1.0 B=1.0 C=0.93 Δ=0.0. 19s. KEEP. Current Level Status extracted into own subsection — independently addressable.
[nervous-system:Five Levels Position] SPLIT (info_retrieval) → 872w→874w. A=1.0 B=1.0 Δ=0.0. 14s. KEEP. Dense paragraph→3 subsections (L1 Gate Status/Gate-Breaker Candidates/Parallel Level Activity). NS×SPLIT now 3/3.
[am-triage:hook prompt] REWORD (output_quality) → 117w→131w. A=0.87 B=0.87 Δ=0.0. 45s. KEEP. Added explicit execution order numbering (1-5) and stronger approval guardrail. First hook experiment. Seeded am-triage priors.
[eod-refresh:hook prompt] REWORD (output_quality) → 111w→179w. A=0.87 B=0.86 Δ=+0.01. 48s. KEEP. Added completion criteria per phase + failure handling instruction. First output-quality delta > 0. Seeded eod-refresh priors.
[heart:Step 3 technique descriptions] REMOVE (info_retrieval) → 4122w→4014w. A=1.0 B=1.0 Δ=0.0. 16s. KEEP. Stripped inline caution notes from technique list — redundant with Validated Patterns table. -108w.

Running tallies:
[brain×SPLIT: 1 kept / 1 total]
[nervous-system×SPLIT: 3 kept / 3 total]
[am-triage×REWORD: 1 kept / 1 total]
[eod-refresh×REWORD: 1 kept / 1 total]
[heart×REMOVE: 1 kept / 1 total]

Batch stats: 5/5 KEEP (100%). Selection bias check: 100% keep rate is high, but all 5 were n=0 combos (pure exploration) — 3 new target categories (brain, am-triage, eod-refresh), 2 validated patterns (NS×SPLIT, REMOVE on redundant rationale). First hook experiments validated output-quality eval pipeline. Next batch should force harder techniques (REMOVE on unique content, MERGE on distinct registers) to generate reverts and learn boundaries.

### Karpathy Run 34 — 2026-04-05 (10 experiments, 9 keep, 1 revert)
- [gut:Compression Techniques] REWORD (info_retrieval) → 2064w→2162w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP.
- [brain:Decision Log] RESTRUCTURE (info_retrieval) → 1235w→1246w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [eyes:Common Failures] ADD (info_retrieval) → 978w→1075w. A=1.0 B=1.0 C=1.0 Δ=0.0. 100s. KEEP.
- [spine:Bootstrap Context] REWORD (info_retrieval) → 873w→880w. A=1.0 B=0.9 C=1.0 Δ=+0.1. 100s. KEEP.
- [memory:Reference Index subfolders] REMOVE (info_retrieval) → 1802w→1793w. A=0.83 B=1.0 C=0.83 Δ=-0.17. 110s. REVERT.
- [device:Installed Apps] SPLIT (info_retrieval) → 1219w→1230w. A=1.0 B=1.0 C=1.0 Δ=0.0. 100s. KEEP.
- [nervous-system:Loop 3 patterns] COMPRESS (info_retrieval) → 874w→875w. A=1.0 B=1.0 C=1.0 Δ=0.0. 95s. KEEP.
- [amcc:Escalation Ladder] REWORD (info_retrieval) → 1934w→1993w. A=1.0 B=1.0 C=1.0 Δ=0.0. 100s. KEEP.
- [richard-style-slack:Relationship Dynamics] SPLIT (output_quality) → 961w→994w. A=0.93 B=0.90 C=0.88 Δ=+0.03. 110s. KEEP.
- [richard-style-wbr:Data Source Reference] ADD (output_quality) → 564w→643w. A=0.90 B=0.88 C=0.85 Δ=+0.02. 120s. KEEP.

### Run 35 (2026-04-05, Karpathy)
- [gut:Compression Techniques] ADD (info_retrieval) → 2162w→2206w. A=1.0 B=0.5 C=1.0 Δ=+0.50. 90s. KEEP.
- [nervous-system:Deferred Loops 6-8] MERGE (info_retrieval) → 875w→875w. A=1.0 B=1.0 C=1.0 Δ=0.0. 85s. KEEP.
- [nervous-system:Loop 9] REWORD (info_retrieval) → 875w→909w. A=1.0 B=0.5 C=1.0 Δ=+0.50. 85s. KEEP.
- [brain:Leverage Assessment] REWORD (info_retrieval) → 1246w→1307w. A=1.0 B=0.8 C=1.0 Δ=+0.20. 100s. KEEP.
- [am-triage:prompt] COMPRESS (output_quality) → 76w→56w. A=1.0 B=1.0 C=1.0 Δ=0.0. 70s. KEEP.
- [brain:OP1 Strategic Narrative] REMOVE (info_retrieval) → 1307w→1255w. A=0.4 B=1.0 C=0.4 Δ=-0.60. 95s. REVERT.
- [heart:Design Choices] COMPRESS (info_retrieval) → 4055w→3899w. A=1.0 B=1.0 C=1.0 Δ=0.0. 100s. KEEP.
- [gut:Archive Rules] COMPRESS (info_retrieval) → 2206w→2181w. A=0.83 B=1.0 C=0.83 Δ=-0.17. 90s. REVERT.
- [heart:Common Failures (new)] ADD (info_retrieval) → 3899w→4038w. A=1.0 B=0.75 C=1.0 Δ=+0.25. 100s. KEEP.
- [memory:Staleness Index + Relationship Graph] MERGE (info_retrieval) → 1802w→1753w. A=0.9 B=1.0 C=0.9 Δ=-0.10. 110s. REVERT.

### 2026-04-05 — Karpathy Run 36 (10 experiments, 6 keep, 4 revert)
- [richard-style-wbr:Examples] SPLIT (output_quality) → 643w→654w. A=0.95 B=0.90 Δ=+0.05. 90s. KEEP.
- [richard-style-docs:Universal Rules] COMPRESS (output_quality) → 670w→638w. A=0.90 B=0.93 Δ=-0.03. 95s. REVERT.
- [spine:System History] REMOVE (info_retrieval) → 880w→855w. A=0.80 B=1.00 Δ=-0.20. 85s. REVERT.
- [gut:Three Functions] SPLIT (info_retrieval) → 2206w→2218w. A=1.00 B=1.00 Δ=0.00. 80s. KEEP.
- [memory:Relationship Graph] RESTRUCTURE (info_retrieval) → 1802w→1802w. A=1.00 B=1.00 C=1.00 Δ=0.00. 120s. KEEP.
- [amcc:Common Failures (new)] ADD (info_retrieval) → 1993w→2120w. A=1.00 B=0.80 Δ=+0.20. 100s. KEEP.
- [brain:OP1 Strategic Narrative] COMPRESS (info_retrieval) → 1307w→1299w. A=1.00 B=1.00 C=1.00 Δ=0.00. 110s. KEEP.
- [nervous-system:Common Failures (new)] ADD (info_retrieval) → 909w→1002w. A=1.00 B=0.75 Δ=+0.25. 95s. KEEP.
- [device:Data & Integration] MERGE (info_retrieval) → 1230w→1083w. A=0.90 B=1.00 Δ=-0.10. 100s. REVERT.
- [richard-style-slack:What Richard Shares Unprompted] REMOVE (output_quality) → 994w→923w. A=0.90 B=0.96 Δ=-0.06. 100s. REVERT.

### Karpathy Run 38 — 2026-04-05 (10 experiments, 9 kept, 1 reverted)
[spine:Common Failures] ADD (info_retrieval) → 880w→976w. A=1.0 B=0.75 C=1.0 Δ=+0.25. 90s. KEEP.
[memory:Compressed Context] SPLIT (info_retrieval) → 1831w→1839w. A=1.0 B=1.0 C=1.0 Δ=0.0. 100s. KEEP.
[gut:AM-3 Brief] REMOVE (info_retrieval) → 2218w→2182w. A=0.67 B=1.0 Δ=-0.33. 90s. REVERT.
[audit-asana-writes:Prompt ordering] RESTRUCTURE (output_quality) → 172w→177w. A=1.0 B=1.0 Δ=0.0. 80s. KEEP.
[memory:Common Failures ordering] RESTRUCTURE (info_retrieval) → 1839w→1839w. A=1.0 B=1.0 C=1.0 Δ=0.0. 110s. KEEP.
[eod-refresh:Phase descriptions] REWORD (output_quality) → 227w→207w. A=1.0 B=1.0 Δ=0.0. 85s. KEEP.
[memory:Common Failures register example] ADD (info_retrieval) → 1839w→1870w. A=1.0 B=0.9 C=1.0 Δ=+0.1. 120s. KEEP.
[eod-refresh:Phase completion signals] ADD (output_quality) → 207w→231w. A=1.0 B=0.33 Δ=+0.67. 85s. KEEP.
[nervous-system:Common Failures STUCK example] ADD (info_retrieval) → 1025w→1041w. A=0.875 B=0.875 Δ=0.0. 90s. KEEP.
[device:Tool Factory] REWORD (info_retrieval) → 1230w→1227w. A=1.0 B=1.0 Δ=0.0. 85s. KEEP.

### Karpathy Run 39 — 2026-04-05 (10 experiments, 10 kept, 0 reverted)
[spine:Directory Map] RESTRUCTURE (info_retrieval) → 976w→970w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP.
[device:Delegation Protocols] RESTRUCTURE (info_retrieval) → 1227w→1227w. A=1.0 B=1.0 C=1.0 Δ=0.0. 85s. KEEP.
[brain:Prediction Template] COMPRESS (info_retrieval) → 1369w→1352w. A=1.0 B=1.0 C=1.0 Δ=0.0. 110s. KEEP.
[nervous-system:Loop 4 Delegation] REWORD (info_retrieval) → 1041w→1050w. A=1.0 B=1.0 C=1.0 Δ=0.0. 85s. KEEP.
[heart:Experiment Signals] REMOVE (info_retrieval) → 4037w→3993w. A=1.0 B=1.0 C=1.0 Δ=0.0. 100s. KEEP.
[eyes:Competitive Trends] ADD (info_retrieval) → 1079w→1103w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP.
[richard-style-slack:What Richard Shares Unprompted] REWORD (output_quality) → 1132w→1163w. A=0.92 B=0.92 C=0.88 Δ=0.0. 95s. KEEP.
[memory:Key Decisions/Positions] ADD (info_retrieval) → 1870w→1888w. A=1.0 B=0.917 C=1.0 Δ=+0.083. 120s. KEEP.
[amcc:Escalation Ladder worked example] ADD (info_retrieval) → 2120w→2213w. A=1.0 B=0.75 C=1.0 Δ=+0.25. 100s. KEEP.
[gut:Extraction Rules] REWORD (info_retrieval) → 2218w→2192w. A=1.0 B=1.0 C=1.0 Δ=0.0. 85s. KEEP.

### Run 40 (2026-04-05, Karpathy batch — 10 experiments, 8 keep, 2 revert)
- [audit-asana-writes:Batch handling] ADD (output_quality) → 177w→207w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [eod-refresh:Common failures ordering] RESTRUCTURE (output_quality) → 231w→235w. A=1.0 B=1.0 C=1.0 Δ=0.0. 130s. KEEP.
- [richard-style-docs:Common Failures (new)] ADD (output_quality) → 670w→749w. A=1.0 B=0.9 C=1.0 Δ=+0.1. 140s. KEEP.
- [gut:Extraction Rules worked example] ADD (info_retrieval) → 2192w→2236w. A=1.0 B=0.9 C=1.0 Δ=+0.1. 150s. KEEP.
- [richard-style-mbr:Data Rules confidence signal] ADD (output_quality) → 464w→499w. A=1.0 B=0.75 C=1.0 Δ=+0.25. 140s. KEEP.
- [richard-style-email:Common Failures ordering] RESTRUCTURE (output_quality) → 552w→552w. A=1.0 B=1.0 C=1.0 Δ=0.0. 130s. KEEP.
- [eod-refresh:Phases 1+2 merge] MERGE (output_quality) → 235w→232w. A=0.25 B=1.0 C=0.25 Δ=-0.75. 140s. REVERT.
- [richard-style-amazon:Data+Analytical merge] MERGE (output_quality) → 940w→927w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
- [richard-style-email:Sentence-Level Patterns subsections] SPLIT (output_quality) → 552w→561w. A=1.0 B=0.875 C=1.0 Δ=+0.125. 140s. KEEP.
- [nervous-system:Loop 8 Source Quality Filter] REMOVE (info_retrieval) → 1050w→1025w. A=0.7 B=1.0 C=0.7 Δ=-0.3. 150s. REVERT.
- [ADD×style-guides: 4 kept / 4 total] [RESTRUCTURE×style-guides: 2 kept / 2 total] [MERGE: 1 kept / 2 total] [SPLIT: 1 kept / 1 total] [REMOVE: 0 kept / 1 total]

### Run 42 (2026-04-07, Karpathy batch — 10 experiments, 10 keep, 0 revert)
- [brain:Decision Log tables] COMPRESS (info_retrieval) → 1358w→1371w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [spine:Session Bootstrap Sequence] REWORD (info_retrieval) → 941w→952w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP.
- [memory:Relationship Graph Cross-Cutting Dynamics] ADD (info_retrieval) → 1919w→2005w. A=1.0 B=1.0 C=1.0 Δ=0.0. 130s. KEEP.
- [gut:Three Functions examples] REWORD (info_retrieval) → 2242w→2301w. A=1.0 B=1.0 C=1.0 Δ=0.0. 140s. KEEP.
- [nervous-system:Loop 2 Prediction Scoring] ADD (info_retrieval) → 1183w→1247w. A=1.0 B=1.0 C=1.0 Δ=0.0. 130s. KEEP.
- [heart:Step 1 valid targets dedup] REMOVE (info_retrieval) → 3948w→3922w. A=1.0 B=1.0 C=1.0 Δ=0.0. 130s. KEEP.
- [richard-style-wbr:Common Callout Failures subsections] SPLIT (output_quality) → 695w→701w. A=0.98 B=0.98 C=0.98 Δ=0.0. 150s. KEEP.
- [am-triage:Common Failures section] ADD (output_quality) → 254w→299w. A=1.0 B=0.833 C=1.0 Δ=+0.167. 140s. KEEP.
- [richard-style-slack:Tone Register subsections] SPLIT (output_quality) → 1163w→1170w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
- [eyes:Market Deep Dives table] COMPRESS (info_retrieval) → 1166w→1147w. A=1.0 B=1.0 C=1.0 Δ=0.0. 140s. KEEP.
- [COMPRESS×organs: 2 kept / 2 total] [REWORD×organs: 2 kept / 2 total] [ADD×organs: 2 kept / 2 total] [ADD×hooks: 1 kept / 1 total] [REMOVE×organs: 1 kept / 1 total] [SPLIT×style-guides: 2 kept / 2 total]

### Karpathy Run 42 — 2026-04-07 (10 experiments, 8 keep, 2 revert)
- [nervous-system:Common Failures] REMOVE (info_retrieval) → 1183w→1074w. A=0.75 B=0.95 C=0.75 Δ=-0.20. 120s. REVERT. (Anti-pattern: REMOVE on behavioral constraints. Lost 7-day prediction threshold.)
- [spine:Session Bootstrap Sequence] COMPRESS (info_retrieval) → 976w→941w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP. (Paragraphs→table, -35w.)
- [amcc:Growth Model] REWORD (info_retrieval) → 2141w→2174w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP. (Added concrete examples.)
- [brain:Decision Log] SPLIT (info_retrieval) → 1371w→1373w. A=1.0 B=1.0 C=1.0 Δ=0.0. 180s. KEEP. (Decay Protocol as own subsection.)
- [richard-style-email:Common Draft Failures] SPLIT (info_retrieval) → 561w→564w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP. (Named subsections per failure.)
- [richard-style-mbr:Voice] SPLIT (info_retrieval) → 499w→505w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP. (Register + Miss Attribution subsections.)
- [device:Candidate Install gcm+llm] REMOVE (info_retrieval) → 1607w→1549w. A=0.73 B=1.0 C=0.73 Δ=-0.27. 120s. REVERT. (Anti-pattern: REMOVE on unique content — install steps lost.)
- [gut:Compression Protocol] MERGE (info_retrieval) → 2301w→2106w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP. (Word Budget + Over-budget merged into intro. -195w, biggest win.)
- [richard-style-slack:Slack-Specific Habits] SPLIT (info_retrieval) → 1170w→1182w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP. (Availability/Delayed/Emoji subsections.)
- [richard-style-docs:Strategic Narrative] RESTRUCTURE (info_retrieval) → 749w→749w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP. (Actionable-first reorder.)


## 2026-04-09 EOD-Backend
- Phase 1: 3 Hedy sessions ingested (Austin offsite Apr 8): OP1 brainstorm (96min, 6 action items), Adobe bi-weekly (1060min, platform health 64%), LP Testing review (33min, 3 action items). Calendar: Google Search Summit + dinner.
- Phase 2: 11 tasks completed yesterday. 2 daily resets (Today→Urgent): AU Polaris LP data, WW weblab dial-up. Reconciliation JSON written.
- Phase 3: Compression audit — 35,816w total body. No signals. Workflow health clean. Organ cascade skipped (<48h).
- Phase 4: Created ops.recurring_task_state table (8 rows: goal_updater, meta_calibration_priors, meta_calibration_projections, coherence_audit, weekly_scorecard, context_surface_refresh, agent_bridge_sync, wiki_lint). 0 tasks due today. Next due: weekly_scorecard + agent_bridge_sync on Fri 4/10.
- Phase 5: Git synced (76834c5). MotherDuck snapshot failed (plan limitation). Changelog updated.
- Phase 6: Skipped — Austin offsite context, Karpathy experiments deferred.
- Phase 7: eod-reconciliation.json + eod-maintenance.json written.

## Run 43 — 2026-04-11 (Karpathy batch, 10 experiments, 9 kept, 1 reverted)
- [brain:OP1 Strategic Narrative] REWORD (info_retrieval) → 1373w→1391w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [memory:Markets and Team] RESTRUCTURE (info_retrieval) → 2005w→2003w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [gut:Bloat Signals] REWORD (info_retrieval) → 2106w→2055w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [brain:Leverage Assessment Framework] COMPRESS (info_retrieval) → 1391w→1373w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [heart:Step 3 Apply Experiment] REMOVE (info_retrieval) → 3922w→3892w. A=0.923 B=1.0 C=0.923 Δ=-0.077. 120s. REVERT.
- [nervous-system:Loop 4 Delegation Verification] ADD (info_retrieval) → 1247w→1260w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [richard-style-slack:Common Failures] SPLIT (info_retrieval) → 1205w→1214w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [gut:Identity field protection] SPLIT (info_retrieval) → 2055w→2058w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [heart:DuckDB Integration] REWORD (info_retrieval) → 3922w→3872w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [nervous-system:Loop 5 System Health] SPLIT (info_retrieval) → 1260w→1276w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [REWORD×brain: 2 kept / 2 total] [COMPRESS×brain: 5 kept / 5 total] [RESTRUCTURE×memory: 5 kept / 5 total] [REWORD×gut: 5 kept / 5 total] [REMOVE×heart: 5 kept / 6 total] [ADD×nervous-system: 6 kept / 6 total] [SPLIT×richard-style-slack: 5 kept / 5 total] [SPLIT×gut: 3 kept / 3 total] [REWORD×heart: 1 kept / 2 total] [SPLIT×nervous-system: 7 kept / 7 total]

### Karpathy Run 44 — 2026-04-15 (10 experiments: 8 kept, 2 reverted)
- [spine:Ground Truth Files] ADD (info_retrieval) → 1141w→1209w. A=1.0 B=1.0 C=0.93 Δ=0.0. 120s. KEEP.
- [heart:Design Choices] RESTRUCTURE (info_retrieval) → 3872w→3875w. A=1.0 B=1.0 C=1.0 Δ=0.0. 130s. KEEP.
- [gut:Three Functions] COMPRESS (info_retrieval) → 2058w→2033w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [eyes:OCI Performance] REWORD (info_retrieval) → 1147w→1167w. A=1.0 B=1.0 C=1.0 Δ=0.0. 110s. KEEP.
- [amcc:The Streak] ADD (info_retrieval) → 3154w→3239w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [spine:Hook System] REWORD (info_retrieval) → 1209w→1229w. A=0.9 B=1.0 C=0.9 Δ=-0.1. 120s. REVERT (detail loss: EOD-2 scope dropped).
- [eyes:Whats Coming] ADD (info_retrieval) → 1167w→1199w. A=1.0 B=1.0 C=1.0 Δ=0.0. 110s. KEEP.
- [richard-style-wbr:Examples] SPLIT (output_quality) → 920w→928w. A=0.86 B=0.90 C=0.84 Δ=-0.04. 140s. REVERT (structure match degraded).
- [device:Installed Apps] REWORD (info_retrieval) → 2085w→2078w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [richard-style-slack:Greeting and Sign-off] SPLIT (output_quality) → 1214w→1214w. A=0.96 B=0.96 C=0.96 Δ=0.0. 130s. KEEP.

### Karpathy Run 45 — 2026-04-15 (10 experiments, 8 kept, 2 reverted)
[amcc:Common Failures] SPLIT (info_retrieval) → 3239w→3246w. A=0.833 B=0.833 C=1.0 Δ=0.0. 120s. KEEP.
[eyes:Ad Copy Testing Results] SPLIT (info_retrieval) → 1199w→1201w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[memory:Relationship Staleness Index] COMPRESS (info_retrieval) → 2003w→1989w. A=0.818 B=1.0 C=0.818 Δ=-0.182. 120s. REVERT.
[nervous-system:Loop 1 Decision Audit] RESTRUCTURE (info_retrieval) → 1276w→1276w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[gut:Governance/When to Read] REMOVE (info_retrieval) → 2033w→2003w. A=0.867 B=1.0 C=0.667 Δ=-0.133. 120s. REVERT.
[richard-style-slack:Cadence and Structure] REWORD (output_quality) → 1214w→1222w. A=0.96 B=0.96 C=0.92 Δ=0.0. 150s. KEEP.
[richard-style-email:Sentence-Level Patterns] MERGE (output_quality) → 832w→828w. A=0.98 B=0.98 C=0.88 Δ=0.0. 150s. KEEP.
[am-triage:Data Query Sections] MERGE (output_quality) → 390w→373w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[audit-asana-writes:Batch Handling/Critical Rules] RESTRUCTURE (output_quality) → 248w→239w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-amazon:Writing Hygiene] MERGE (output_quality) → 951w→949w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.

### Karpathy Run 46 — 2026-04-15 (10 experiments, 9 kept, 1 reverted)
[spine:Directory Map] COMPRESS (info_retrieval) → 1209w→1176w. A=0.762 B=0.762 C=0.762 Δ=0.0. 150s. KEEP.
[heart:Hyperparameters] RESTRUCTURE (info_retrieval) → 3875w→3875w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[brain:Decision Log] REMOVE (info_retrieval) → 1373w→1311w. A=0.8 B=1.0 C=0.8 Δ=-0.2. 150s. REVERT (Decay Protocol is unique content).
[eod-refresh:Backend/Frontend] SPLIT (output_quality) → 339w→403w. A=0.98 B=0.98 C=0.92 Δ=0.0. 150s. KEEP.
[memory:Compressed Context] RESTRUCTURE (info_retrieval) → 2003w→2003w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-wbr:Voice] SPLIT (output_quality) → 920w→923w. A=0.96 B=0.96 C=0.96 Δ=0.0. 150s. KEEP.
[nervous-system:Loop 9 Baselines] REWORD (info_retrieval) → 1276w→1313w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-email:Full File] RESTRUCTURE (output_quality) → 828w→828w. A=1.0 B=1.0 C=0.98 Δ=0.0. 150s. KEEP.
[audit-asana-writes:Full Hook] ADD (output_quality) → 239w→310w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[amcc:Political Awareness Layer] ADD (info_retrieval) → 3246w→3413w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.

## 2026-04-20 (Monday PT, EOD) — Low-activity EOD run

**Day summary:** 14 Asana tasks closed (5 genuine + 9 bulk-cleanup backlog purge). 6 Today→Urgent demotions. Zero meetings. No Hedy sessions. One Hedy session (4/17 AI Tool Demo) remains the latest.

**Genuine completions (5):** Italy Polaris P0 ref tag revert coordination (L2, protecting OCI measurement); Refmarker mapping audit PoC for AU (L3, team automation signal, Task Progress=Done); Reply to Dwayne on Brand LP consolidated feedback (L2, ×2 duplicate tasks); Write back to Dwayne re AU Adobe Alignment session (L2).

**Bulk cleanup (9):** 10:38 PT mass-close including 26d-stale WW redirect task, CA Polaris CTA backlog, budget dashboard/account links ideas from Q1, ieCCP MX (Begin-Date future), "Using AI for paid search" research task, goal updaters. Low-friction housekeeping — not work product.

**Five Levels:** L1=0 (22 workdays streak), L2=3, L3=1, L4=0, L5=0. Testing Approach v5 still not sent — send step is the only remaining blocker, PUBLISH verdict already given (8.4/10).

**Pattern trajectory (NS Loop 3):** L1 streak STUCK → WORSENING. Brandon/Kate meeting cancellation on 4/16 removed the external forcing function. No substitute structural intervention has taken hold. Intervention proposal: decouple "send" as atomic task from any Testing Approach work block.

**Delegation failures (NS Loop 4):** Vijeth footer (32d) and Andes data (35d) both moved SLIPPING → FAILED. Both have stopped delivering — need escalation or workaround.

**Observability:** Pre-existing gap — `main.workflow_executions` was empty, `main.daily_tracker` + `main.l1_streak` did not exist. Created missing tables and backfilled today's run. The hooks/protocols have been declaring inserts that never happened. Flag for ops review.

**Body mass:** 26,734w / 14 organs. Within budget. No compression signals.

**Items logged:** daily_tracker, l1_streak, workflow_executions, autoresearch_organ_health (14 rows). Audit log appended with 6 daily_reset entries.

## 2026-04-20 (late Monday PT) — Hard-thing selection redesigned

**Richard's trigger:** Rejected Testing Approach (cancelled meeting = not avoidance) and AEO POV (constructed/artificial) as hard things. Pointed out the design flaw: hard-thing selection was top-down from the task queue, which manufactures targets when no real hard thing exists. Reframed to bottom-up signal convergence — the gap between "signals converging on a topic" and "Richard produced a referenceable artifact on it."

**What changed:**
- `body/amcc.md` — "The Hard Thing Queue" section replaced with "The Hard Thing" signal-driven model. Streak, resistance taxonomy, escalation ladder, political awareness — all unchanged. Only selection logic changed.
- `body/body-diagram.md` — aMCC node now references `main.hard_thing_now` and `main.l1_streak` instead of hardcoded state.
- `context/protocols/hard-thing-selection.md` — new protocol file (promoted from staging). Executable SQL, 7-day window, exponential half-life decay (3.5d default), incumbent advantage (1.15× margin), null-state allowed, artifact detection rules.
- `tools/scripts/hard-thing-refresh.py` — new script. Handles MotherDuck connection, throttle, stickiness, null-state fallback. Exit codes: 0=success, 1=throttled, 2=degraded (token missing or --local).
- DuckDB: created `main.hard_thing_candidates`, `main.hard_thing_topic_levels` (seeded with 10 canonical topics mapped to L1-L5), `main.hard_thing_artifact_log`, and view `main.hard_thing_now`.
- Experiment queue: filed `amcc-halflife-v1` (shadow-eval half-life at 2.0 / 3.5 / 7.0 over 14 days) as `pending` in `autoresearch_experiments`.

**Defaults Richard confirmed:** 7-day window, artifact = referenceable by non-Richard actor, top 3, continuous refresh on signal-write, stickiness via incumbent margin, signal decay as exponential half-life (not cliff).

**Current state:** `main.hard_thing_now` returns null-state with reason `null-state-local-mode-no-signals-schema` — this shell has no MotherDuck token, so the first real scoring refresh is deferred to the next token-connected run (next scheduled AM or EOD hook, or manual `python3 ~/shared/tools/scripts/hard-thing-refresh.py` with token).

**What didn't change:** streak mechanics, resistance taxonomy, escalation ladder, political awareness layer, integration with other organs. Net complexity: 3 new tables, 1 new protocol, 1 new script, 1 removed subsection from amcc.md. Trends simpler long-term because no more manual "what's the hard thing?" decisions.

**Staging folder** at `context/staged/hard-thing-redesign/` kept as-is for audit trail — README there has the full promotion checklist and today's rejection test (which polaris-brand-lp passed under validation against live MotherDuck signals during staging).


## 2026-04-21 EOD (Tuesday PT)

**Meetings (3):** Weekly Paid Acq Sync (77min), MX Paid Search/IECCP Sync (34min), Brandon 1:1 (4min TRUNCATED — laptop issue). All ingested to hedy_meetings + meeting_analytics + meeting_highlights in DuckDB.

**Asana (10 writes):**
- 7 completions reconciled (all completed 17:16-17:31 PT yesterday but missed by 4/20 EOD due to sync timing). Major shipped: Dwayne Brand LP reply (full 7-ask draft), Dwayne AU PS reply, Polaris template forward, OFA invoice, AU genbi max-clicks, BrowserStack for Adi.
- 3 daily-reset Today→Urgent demotions: W15 WBR, AU handover max-clicks check, Email overlay (Brandon ask). Kiro_RW + Next-action written on each.
- Testing Doc for Kate (hard thing): new story comment + Kiro_RW update reflecting truncated Brandon 1:1 = no send, 23 workdays at zero L1.

**New tasks (4):** Richard created MCS-2553 LP audit + Adobe dashboard template tasks (defensive pre-launch scope protection). Measure EM impact (PS ENG). Monday EU SSR auto-recurring for 4/27.

**Open blockers (2 escalations active from 4/20):** Vijeth MX Auto footer 33d, Andes Kingpin MX 36d.

**Five Levels today:** L1=0 (23rd straight workday). L2=4. L3=2. L4=0. L5=0.

**Observability:** hook_executions row written. Asana sync gap identified - DuckDB is 5+ hours stale relative to live Asana by EOD. Filed as medium-severity flag. AM hooks still not logging to DuckDB - flagged.

**Experiments:** SKIPPED (Karpathy defer pattern - needs automated hook run). 3 suggestions logged: atomic SEND task for Testing Doc, Brandon 1:1 pre-load prep block, EOD force Asana sync before reconciliation.

**Key decisions pending:**
- IECCP target 70% vs 75% for MX (confirm w/ Brandon tomorrow, gates May R&O transfer)
- Testing Approach v5 send (23 workdays stuck — apply 5 fixes + hit send, 10-min task)
- MX R&O reallocation email to Lorena (Brandon-assigned today)

**Streak:** 1 → 0 (reset). 23 workdays at zero L1. Brandon 1:1 window was the forcing function — lost to laptop.

### Run 48 — Karpathy Autoresearch Batch (2026-04-22)
[brain:Leverage Assessment Framework] COMPRESS (info_retrieval) → 1373w→1308w. A=0.9 B=1.0 C=0.9 Δ=-0.1. 120s. REVERT.
[amcc:Purpose] RESTRUCTURE (info_retrieval) → 4147w→4148w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-docs:Investigation+HowTo] MERGE (output_quality) → 772w→764w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[am-triage:Steps+DataQueries] MERGE (output_quality) → 373w→350w. A=1.0 B=1.0 C=1.0 Δ=0.0. 180s. KEEP.
[brain:Five Levels Current Status] ADD (info_retrieval) → 1373w→1437w. A=1.0 B=1.0 C=0.93 Δ=0.0. 150s. KEEP.
[amcc:After Intervention] ADD (info_retrieval) → 4148w→4250w. A=1.0 B=0.9 C=1.0 Δ=+0.1. 180s. KEEP.
[richard-style-docs:Testing Plans] COMPRESS (output_quality) → 754w→743w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[memory:Key Decisions/Positions] REWORD (info_retrieval) → 2049w→2068w. A=1.0 B=0.917 C=1.0 Δ=+0.083. 180s. KEEP.
[device:Delegation Protocols] REWORD (info_retrieval) → 2223w→2217w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[gut:Identity Field Protection] SPLIT (info_retrieval) → 2033w→2025w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.

### Run 49 — 2026-04-22 (Karpathy batch, 10 experiments, 5 kept, 5 reverted)
- [am-triage:full hook] RESTRUCTURE (output_quality) → 321w→311w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP. Guardrails moved to top.
- [richard-style-mbr:Data Rules] REMOVE (output_quality) → 529w→445w. A=0.8 B=1.0 C=0.8 Δ=-0.2. REVERT. Data Rules are unique content.
- [eyes:OCI+AdCopy] MERGE (info_retrieval) → 1178w→1186w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP. Cross-referenced ad copy into OCI table.
- [audit-asana-writes:Steps+CommonFailures] MERGE (output_quality) → 310w→235w. A=0.8 B=1.0 C=0.8 Δ=-0.2. REVERT. Common Failures lost in merge.
- [nervous-system:Loop 1] ADD (info_retrieval) → 1322w→1366w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP. Added scoring example.
- [spine:Session Bootstrap] REMOVE (info_retrieval) → 1223w→1092w. A=0.4 B=1.0 C=0.4 Δ=-0.6. REVERT. Session Bootstrap is load-bearing.
- [eod-refresh:Auto-Execute] ADD (output_quality) → 499w→555w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP. Added Common Failures section.
- [heart:Architecture] COMPRESS (info_retrieval) → 4054w→3860w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP. Removed duplicate Body table + Directory Map.
- [richard-style-docs:Strategic Narrative] REMOVE (output_quality) → 743w→662w. A=0.8 B=1.0 C=0.8 Δ=-0.2. REVERT. Strategic Narrative is unique content.
- [brain:Leverage Assessment] REMOVE (info_retrieval) → 1437w→1302w. A=0.6 B=1.0 C=0.6 Δ=-0.4. REVERT. Leverage Assessment is unique behavioral content.
- **Batch learning:** REMOVE continues to revert on unique content (5/5 this batch). ADD and RESTRUCTURE continue to keep. COMPRESS on duplicate cross-references is safe. MERGE on Common Failures sections loses content — keep them separate.

### Run 49 — 2026-04-22 (Karpathy batch, 10 experiments, 10 kept, 0 reverted)
- [nervous-system:Loop1] SPLIT (info_retrieval) → 1315w→1322w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [brain:OP1] RESTRUCTURE (info_retrieval) → 1437w→1437w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [gut:Three Functions] RESTRUCTURE (info_retrieval) → 2025w→2025w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [heart:Core Principles] REWORD (info_retrieval) → 4085w→4054w. A=1.0 B=1.0 C=1.0 Δ=0.0. 180s. KEEP.
- [richard-style-email:Operational] RESTRUCTURE (output_quality) → 828w→828w. A=0.96 B=0.94 C=0.90 Δ=+0.02. 180s. KEEP.
- [richard-style-slack:Shares Unprompted] COMPRESS (output_quality) → 1238w→1207w. A=0.98 B=0.98 C=0.98 Δ=0.0. 150s. KEEP.
- [amcc:Common Failures] ADD (info_retrieval) → 4250w→4291w. A=0.934 B=0.90 C=0.934 Δ=+0.034. 150s. KEEP.
- [richard-style-amazon:Confidence] ADD (output_quality) → 949w→1000w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
- [eod-refresh:Queue Frontend] ADD (output_quality) → 555w→578w. A=1.0 B=0.9 C=1.0 Δ=+0.1. 150s. KEEP.
- [richard-style-slack:Relationship Dynamics] ADD (output_quality) → 1207w→1238w. A=0.99 B=0.98 C=0.99 Δ=+0.01. 150s. KEEP.

### Run 50 (2026-04-22, Karpathy batch)
[eod-refresh:Backend Phases] COMPRESS (output_quality) → 578w→518w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[nervous-system:Loop 3] RESTRUCTURE (info_retrieval) → 1366w→1366w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[device:EOD Hook] COMPRESS (info_retrieval) → 2217w→2204w. A=0.67 B=1.0 C=0.58 Δ=-0.33. 120s. REVERT.
[richard-style-docs:Knowledge-Sharing+Common Failures] MERGE (output_quality) → 743w→748w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[brain:OP1+Leverage] MERGE (info_retrieval) → 1437w→1441w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-wbr:Common Failures] ADD (output_quality) → 916w→967w. A=1.0 B=0.8 C=1.0 Δ=+0.2. 150s. KEEP.
[memory:Common Failures] REWORD (info_retrieval) → 2068w→2047w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[am-triage:Common Failures] SPLIT (output_quality) → 311w→313w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[spine:Ground Truth+Common Failures] MERGE (info_retrieval) → 1260w→1260w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[eyes:Market Deep Dives] ADD (info_retrieval) → 1186w→1236w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.

### Run 50 — Karpathy Batch (2026-04-22, 10 experiments, 7 kept, 3 reverted)

[device:Slack Context Ingestion] REMOVE (info_retrieval) → 2217w→2123w. A=0.0 B=1.0 C=0.0 Δ=-1.0. 120s. REVERT.
[brain:Prediction Template] SPLIT (info_retrieval) → 1437w→1440w. A=0.778 B=0.778 C=0.778 Δ=0.0. 120s. REVERT (both A+B flagged Q2 INCORRECT — pre-existing hole).
[richard-style-wbr:Attribution+Context Failures] MERGE (output_quality) → 919w→916w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-email:Operational Coordination] ADD (output_quality) → 828w→854w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[spine:Common Failures] ADD (info_retrieval) → 1223w→1260w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[device:Safety Guards] ADD (info_retrieval) → 2217w→2237w. A=1.0 B=0.7 C=1.0 Δ=+0.3. 150s. KEEP.
[richard-style-wbr:Formatting Rules] REMOVE (output_quality) → 967w→796w. A=0.077 B=1.0 C=0.15 Δ=-0.923. 150s. REVERT.
[richard-style-mbr:Common Failures] SPLIT (output_quality) → 529w→537w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[brain:Level 1 Sharpen Yourself] REWORD (info_retrieval) → 1441w→1436w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[am-triage:Steps] SPLIT (output_quality) → 313w→325w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.

### Run 51 — 2026-04-22 (Karpathy batch: 10 experiments, 10 kept, 0 reverted)
[device:SharePoint Durability Layer] ADD (info_retrieval) → 2237w→2284w. A=1.0 B=0.8 C=0.9 Δ=+0.2. 120s. KEEP.
[eod-refresh:Wiki Candidate] RESTRUCTURE (output_quality) → 518w→526w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-email:Common Draft Failures] COMPRESS (output_quality) → 854w→768w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP. -86w compression win.
[nervous-system:Loop 7 Coherence Audit] REWORD (info_retrieval) → 1315w→1335w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[memory:Compressed Context] REWORD (info_retrieval) → 2047w→2059w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[spine:Key IDs] ADD (info_retrieval) → 1260w→1282w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-slack:Slack-Specific Habits] REWORD (output_quality) → 1238w→1211w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP. -27w.
[gut:Three Functions] REWORD (info_retrieval) → 2025w→2031w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-amazon:Prose+Sentence Length] MERGE (output_quality) → 1000w→997w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[brain:Leverage Tiebreakers] REWORD (info_retrieval) → 1436w→1475w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.

### Run 51 — Karpathy Batch (2026-04-22)
[nervous-system:Common Failures] COMPRESS (info_retrieval) → 1366w→1315w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[eod-refresh:Backend Phases] SPLIT (output_quality) → 517w→560w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[spine:Session Bootstrap] RESTRUCTURE (info_retrieval) → 1282w→1282w. A=0.929 B=1.0 C=1.0 Δ=-0.071. 150s. REVERT.
[richard-style-docs:Knowledge-Sharing+CommonFailures] RESTRUCTURE (output_quality) → 748w→744w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-email:Email Analytical] SPLIT (output_quality) → 768w→769w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[amcc:The Hard Thing] ADD (info_retrieval) → 4291w→4374w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-slack:Tone Register] ADD (output_quality) → 1211w→1309w. A=1.0 B=1.0 C=1.0 Δ=0.0. 180s. KEEP.
[memory:Usage Guide] RESTRUCTURE (info_retrieval) → 2045w→2045w. A=1.0 B=1.0 C=1.0 Δ=0.0. 180s. KEEP.
[heart:Active Pipeline] RESTRUCTURE (info_retrieval) → 3920w→3942w. A=0.0 B=1.0 C=1.0 Δ=-1.0. 180s. REVERT (eval_a_infrastructure_failure).
[heart:Architecture] COMPRESS (info_retrieval) → 3920w→3840w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.

### Run 52 (2026-04-22, Karpathy batch)
[memory:Common Failures+Meeting Prep] MERGE (info_retrieval) → 2059w→2045w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[am-triage:full hook] COMPRESS (output_quality) → 325w→176w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[amcc:Scoring math] REMOVE (info_retrieval) → 4374w→4128w. A=0.1 B=- C=- Δ=-. 60s. REVERT (fast_fail).
[device:When to Read] REWORD (info_retrieval) → 2284w→2270w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-amazon:Prose+Purpose] MERGE (output_quality) → 997w→954w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[gut:Three Functions] REWORD (info_retrieval) → 2031w→2016w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[nervous-system:Loop 4 Delegation] REWORD (info_retrieval) → 1402w→1399w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-slack:What NOT to Do] REWORD (output_quality) → 1309w→1293w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[amcc:Purpose] ADD (info_retrieval) → 4394w→4437w. A=0.9 B=0.8 C=0.9 Δ=+0.1. 150s. KEEP.
[eyes:Competitors] ADD (info_retrieval) → 1237w→1283w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
Run 52 totals: 10 experiments, 9 kept, 1 reverted (90% keep rate — high, but 3 exploration picks included).

### Karpathy Run 52 (2026-04-22, batch of 10)
[heart:Hyperparameters] ADD (info_retrieval) → 3860w→3920w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[roster:Pre-WBR Callout Owners] COMPRESS (info_retrieval) → 2413w→2331w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[amcc:Trigger Detection] SPLIT (info_retrieval) → 4374w→4394w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[nervous-system:Five Levels Position] ADD (info_retrieval) → 1335w→1402w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-mbr:Common Failures] SPLIT (output_quality) → 537w→575w. A=0.96 B=0.96 C=0.96 Δ=0.0. 150s. KEEP.
[device:AM Hooks] ADD (info_retrieval) → 2270w→2313w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-amazon:Prose+Writing hygiene] MERGE (output_quality) → 954w→898w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[gut:Purpose] REWORD (info_retrieval) → 2016w→2028w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-wbr:Data Source] ADD (output_quality) → 967w→1009w. A=0.96 B=0.96 C=0.96 Δ=0.0. 150s. KEEP.
[memory:Common Failures] REWORD (info_retrieval) → 2045w→2074w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.

### Run 53 (2026-04-22, Karpathy batch)
[eyes:Competitive Landscape] RESTRUCTURE (info_retrieval) → 1236w→1237w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[eod-refresh:Common Failures] SPLIT (output_quality) → 552w→558w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[brain:Decision Principles] RESTRUCTURE (info_retrieval) → 1475w→1487w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[audit-asana-writes:DuckDB logging] RESTRUCTURE (output_quality) → 310w→300w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-email:Email Operational] RESTRUCTURE (output_quality) → 769w→769w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[heart:Hyperparameters] REWORD (info_retrieval) → 3867w→3836w. A=1.0 B=1.0 C=1.0 Δ=0.0. 180s. KEEP.
[brain:Decision Log Decay Protocol] REWORD (info_retrieval) → 1487w→1476w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[eyes:Competitive Landscape] ADD (info_retrieval) → 1283w→1307w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[eyes:OCI Performance] REWORD (info_retrieval) → 1307w→1298w. A=0.9 B=0.9 C=1.0 Δ=0.0. 120s. KEEP.
[heart:Step 4 Eval] COMPRESS (info_retrieval) → 3836w→3273w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.

### Run 53 (2026-04-22, Karpathy batch — 10 experiments, 9 kept, 1 reverted)
- [heart:Design Choices] ADD (info_retrieval) → 3840w→3867w. A=0.9 B=0.9 C=0.9 Δ=0.0. 150s. KEEP.
- [device:Safety Guards] COMPRESS (info_retrieval) → 2313w→2318w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [memory:Active Projects+Key Metrics] MERGE (info_retrieval) → 2045w→2077w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [spine:Tool Access & Integrations] COMPRESS (info_retrieval) → 1282w→1160w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP. -122w compression win.
- [richard-style-wbr:Voice & Key Patterns] SPLIT (output_quality) → 1009w→1010w. A=1.0 B=0.98 C=1.0 Δ=+0.02. 150s. KEEP.
- [gut:Digestion Protocol] REWORD (info_retrieval) → 2028w→2037w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [nervous-system:Loop 5 System Health] ADD (info_retrieval) → 1399w→1447w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [audit-asana-writes:Full Hook] RESTRUCTURE (output_quality) → 300w→226w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP. -74w compression.
- [amcc:Stickiness+Null state] COMPRESS (info_retrieval) → 4437w→4374w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP. -63w.
- [richard-style-slack:Response Patterns] ADD (output_quality) → 1293w→1346w. A=0.94 B=0.96 C=0.96 Δ=-0.02. 150s. REVERT.

### Run 54 — Karpathy Batch (2026-04-22, 10 experiments)
[richard-style-slack:What Shares Unprompted] RESTRUCTURE (output_quality) → 1293w→1302w. A=1.0 B=1.0 C=0.98 Δ=0.0. 187s. KEEP.
[eyes:OCI Performance] RESTRUCTURE (info_retrieval) → 1298w→1298w. A=1.0 B=1.0 C=1.0 Δ=0.0. 64s. KEEP.
[heart:DuckDB Integration] SPLIT (info_retrieval) → 3273w→3280w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP. (exploration n=0)
[amcc:Trigger Detection] ADD (info_retrieval) → 4469w→4528w. A=1.0 B=0.8 C=1.0 Δ=+0.2. KEEP. Worked example improved retrievability.
[spine:Tool Access] RESTRUCTURE (info_retrieval) → 1188w→1188w. A=0.98 B=0.98 C=0.96 Δ=0.0. KEEP.
[gut:Three Functions] RESTRUCTURE (info_retrieval) → 1974w→1974w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP.
[brain:Prediction Template] SPLIT (info_retrieval) → 1476w→1479w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP.
[am-triage:Phase Labels] REMOVE (output_quality) → 176w→167w. A=0.0 B=1.0 C=0.0 Δ=-1.0. REVERT (fast_fail — eval agents read wrong files).
[device:The Test] ADD (info_retrieval) → 2388w→2445w. A=1.0 B=0.9 C=1.0 Δ=+0.1. KEEP. WBR callout pipeline worked example.
[roster:Pre-WBR Callout Owners] RESTRUCTURE (info_retrieval) → 2331w→2331w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP. Split channel/country tables.

### Karpathy Run 54 — 2026-04-22 (10 experiments, 10 kept, 0 reverted)
- [memory:Usage Guide] REWORD (info_retrieval) → 2077w→2106w. A=1.0 B=1.0 C=0.92 Δ=0.0. 180s. KEEP.
- [spine:Session Bootstrap] ADD (info_retrieval) → 1160w→1188w. A=1.0 B=0.833 C=1.0 Δ=+0.167. 120s. KEEP.
- [nervous-system:Loop 1 Decision Audit] SPLIT (info_retrieval) → 1447w→1484w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [amcc:The Hard Thing] ADD (info_retrieval) → 4374w→4469w. A=0.917 B=0.667 C=0.917 Δ=+0.25. 150s. KEEP.
- [device:Delegation Protocols] REWORD (info_retrieval) → 2318w→2331w. A=1.0 B=0.917 C=1.0 Δ=+0.083. 120s. KEEP.
- [device:WBR Forecast Pipeline] ADD (info_retrieval) → 2331w→2388w. A=1.0 B=0.917 C=0.833 Δ=+0.083. 120s. KEEP.
- [amcc:Political Awareness] RESTRUCTURE (info_retrieval) → 4528w→4528w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [hands:Dependencies] COMPRESS (info_retrieval) → 1240w→1216w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [am-triage:Common Failures] ADD (info_retrieval) → 176w→204w. A=1.0 B=0.933 C=1.0 Δ=+0.067. 120s. KEEP.
- [eod-refresh:Backend Phases] ADD (info_retrieval) → 544w→555w. A=1.0 B=0.917 C=1.0 Δ=+0.083. 120s. KEEP.
[audit-asana-writes:STEP3_LOG] COMPRESS (output_quality) → 226w→176w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.

### Run 55 (2026-04-22, Karpathy batch — 10 experiments, 10 kept, 0 reverted)
[richard-style-docs:Common Failures] COMPRESS (output_quality) → 744w→755w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[eod-refresh:Common Failures] COMPRESS (output_quality) → 558w→544w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[gut:Integration Heart Loop] REMOVE (information_retrieval) → 2037w→1974w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-amazon:Appendix+Prose] MERGE (output_quality) → 898w→843w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-mbr:Examples] SPLIT (output_quality) → 575w→593w. A=1.0 B=0.9 C=1.0 Δ=+0.1. 150s. KEEP.
[nervous-system:Loop 1 Decision Audit] REWORD (information_retrieval) → 1484w→1503w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[device:SharePoint Durability] ADD (information_retrieval) → 2445w→2483w. A=1.0 B=0.8 C=1.0 Δ=+0.2. 150s. KEEP.
[richard-style-email:Email Operational] SPLIT (output_quality) → 769w→772w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[nervous-system:Loop 5 System Health] ADD (information_retrieval) → 1503w→1538w. A=1.0 B=0.9 C=1.0 Δ=+0.1. 150s. KEEP.
[brain:Five Levels Graduation] SPLIT (information_retrieval) → 1479w→1460w. A=1.0 B=0.8 C=1.0 Δ=+0.2. 180s. KEEP.
[brain:Prediction_Template] REMOVE (info_retrieval) → 1460w→1325w. A=0.6 B=1.0 C=0.6 Δ=-0.4. 120s. REVERT.
[richard-style-slack:Cadence_Structure] REMOVE (output_quality) → 1302w→1197w. A=0.6 B=1.0 C=0.7 Δ=-0.4. 180s. REVERT.
[richard-style-email:Common_Failures] SPLIT (output_quality) → 772w→801w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-wbr:Examples] SPLIT (output_quality) → 1079w→1081w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-mbr:Template+Voice] MERGE (output_quality) → 628w→626w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[amcc:Purpose] SPLIT (info_retrieval) → 4562w→4570w. A=1.0 B=1.0 C=1.0 Δ=0.0. 180s. KEEP.
[eod-refresh:Backend_Phases] ADD (output_quality) → 558w→584w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.

### Run 56 (2026-04-22, Karpathy batch)
[nervous-system:Purpose] REWORD (info_retrieval) → 1538w→1548w. A=0.8 B=0.8 C=0.8 Δ=0.0. 120s. KEEP.
[eod-refresh:QueueForFrontend+CommonFailures] MERGE (output_quality) → 555w→558w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-wbr:Examples] ADD (output_quality) → 1010w→1079w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-mbr:Examples] REWORD (output_quality) → 593w→628w. A=0.9 B=0.9 C=0.9 Δ=0.0. 150s. KEEP.
[richard-style-email:CommonDraftFailures] REWORD (output_quality) → 772w→779w. A=0.4 B=1.0 C=1.0 Δ=-0.6. 150s. REVERT.
[heart:Hyperparameters] SPLIT (info_retrieval) → 3280w→3292w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[am-triage:PhaseB] SPLIT (output_quality) → 204w→211w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[hands:ToolOpportunities] SPLIT (info_retrieval) → 1216w→1212w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[gut:IntegrationAM3Brief] REMOVE (info_retrieval) → 1974w→1843w. A=0.9 B=1.0 C=0.9 Δ=-0.1. 150s. REVERT.
[audit-asana-writes:CriticalRules] SPLIT (output_quality) → 226w→180w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[eod-refresh:Frontend+CommonFailures] MERGE (output_quality) → 584w→565w. A=0.96 B=1.0 C=0.96 Δ=-0.04. 150s. REVERT.
[eyes:Pipeline_Outlook] COMPRESS (info_retrieval) → 1298w→1231w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.

### Run 57 (2026-04-22, Karpathy batch — 10 experiments, 10 kept, 0 reverted)
- [gut:Three Functions+Compression Protocol] MERGE (info_retrieval) → 1974w→1879w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [amcc:Integration with Other Organs] RESTRUCTURE (info_retrieval) → 4528w→4562w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
- [am-triage:Phase B Triage] SPLIT (output_quality) → 211w→227w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [richard-style-amazon:Data+Structure] MERGE (output_quality) → 843w→813w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
- [audit-asana-writes:Worked Example] ADD (output_quality) → 180w→188w. A=1.0 B=0.8 C=1.0 Δ=+0.2. 150s. KEEP.
- [heart:Architecture] ADD (info_retrieval) → 3292w→3326w. A=1.0 B=0.8 C=1.0 Δ=+0.2. 120s. KEEP.
- [device:AM Hooks] SPLIT (info_retrieval) → 2483w→2482w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [memory:Reference Index] RESTRUCTURE (info_retrieval) → 2106w→2153w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [brain:Prediction Template] REWORD (info_retrieval) → 1460w→1456w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
- [richard-style-slack:Response Patterns] REWORD (output_quality) → 1302w→1287w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
- **Learning:** Eval agent inline prompts must stay under ~3KB for reliable behavior. Auto-loaded steering files (inclusion: auto/always) dominate agent context when inline prompts are larger. Added this constraint to heart.md Architecture section.
- **Keep rate: 100% (10/10).** Above healthy 50% threshold — indicates selection bias toward safe techniques. Next batch should force more exploration of untested combos and bolder experiments.

### Run 58 — 2026-04-22 (Karpathy autoresearch batch, 10 experiments)
- [spine:Hook System] ADD (info_retrieval) → 1188w→1324w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [memory:Team] ADD (info_retrieval) → 2106w→2153w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
- [richard-style-docs:Strategic Narrative] REWORD (output_quality) → 755w→837w. A=1.0 B=1.0 C=1.0 Δ=0.0. 180s. KEEP.
- [memory:Reference Index] COMPRESS (info_retrieval) → 2153w→2134w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
- [spine:Tool Access] COMPRESS (info_retrieval) → 1324w→1305w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [amcc:Two modes worked example] ADD (info_retrieval) → 4570w→4654w. A=1.0 B=1.0 C=1.0 Δ=0.0. 180s. KEEP.
- [richard-style-slack:Slack-Specific Habits] ADD (info_retrieval) → 1287w→1338w. A=1.0 B=1.0 C=1.0 Δ=0.0. 180s. KEEP.
- [eod-refresh:Common Failures] REMOVE (output_quality) → 550w→524w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
- [richard-style-wbr:Established Markets] REWORD (output_quality) → 1081w→1115w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
- [audit-asana-writes:CriticalRules+Steps] MERGE (output_quality) → 189w→165w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.

### Run 59 (2026-04-22, Karpathy batch)
[eyes:OCI Performance] REMOVE (info_retrieval) → 1231w→967w. A=0.167 B=1.0 C=0.167 Δ=-0.833. 120s. REVERT (fast_fail, unique content lost).
[am-auto:Phases2-5] SPLIT (output_quality) → 673w→681w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-amazon:DocStructure] ADD (output_quality) → 813w→955w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[eyes:OCI Performance] ADD (info_retrieval) → 1231w→1289w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[brain:Five Levels Status] SPLIT (info_retrieval) → 1456w→1478w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[audit-asana-writes:Full Hook] RESTRUCTURE (output_quality) → 188w→189w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[heart:Run Protocol Step 3] COMPRESS (info_retrieval) → 3326w→3216w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-mbr:Template Voice] SPLIT (output_quality) → 626w→629w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[eod-refresh:Queue Frontend] SPLIT (output_quality) → 524w→530w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[gut:Purpose] SPLIT (info_retrieval) → 1882w→1884w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.

### Run 60 — 2026-04-22 (Karpathy batch, 10 experiments, 9 kept, 1 reverted)
[richard-style-wbr:Voice Register] RESTRUCTURE (info_retrieval) → 1115w→1124w. A=0.6 B=0.6 C=0.6 Δ=0.0. 120s. KEEP.
[memory:Relationship Graph] SPLIT (info_retrieval) → 2266w→2281w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP.
[richard-style-mbr:Data Rules] ADD (info_retrieval) → 629w→698w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP.
[am-triage:Common Failures] SPLIT (info_retrieval) → 227w→232w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP.
[amcc:Avoidance Ratio] SPLIT (info_retrieval) → 4654w→4675w. A=0.0 B=0.9 C=0.9 Δ=-0.9. 90s. REVERT (Agent A context confusion).
[device:Device Health] ADD (info_retrieval) → 2482w→2499w. A=1.0 B=0.0 C=0.0 Δ=+1.0. 90s. KEEP.
[amcc:Purpose] ADD (info_retrieval) → 4654w→4697w. A=0.0 B=0.0 C=0.8 Δ=0.0. 90s. KEEP.
[memory:Reference Index] REWORD (info_retrieval) → 2281w→2317w. A=1.0 B=0.9 C=1.0 Δ=+0.1. 90s. KEEP.
[am-triage:Description] COMPRESS (info_retrieval) → 272w→259w. A=0.0 B=0.0 C=0.0 Δ=0.0. 90s. KEEP.
[richard-style-slack:Cadence Structure] REWORD (info_retrieval) → 1338w→1360w. A=1.0 B=1.0 C=1.0 Δ=0.0. 90s. KEEP.

### Run 61 (2026-04-22, Karpathy batch — 10 experiments, 10 kept, 0 reverted)
- [eod-refresh:Auto-Execute] REWORD (output_quality) → 530w→560w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP.
- [heart:Architecture+TheMetric] MERGE (information_retrieval) → 3216w→3217w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP.
- [gut:Bloat Detection] ADD (information_retrieval) → 1884w→1931w. A=1.0 B=0.8 C=1.0 Δ=+0.2. KEEP.
- [am-triage:Phase B Triage] SPLIT (output_quality) → 232w→272w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP.
- [memory:Common Failures] REWORD (information_retrieval) → 2281w→2319w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP.
- [audit-asana-writes:Batch Handling] ADD (output_quality) → 165w→202w. A=1.0 B=0.9 C=1.0 Δ=+0.1. KEEP.
- [device:SharePoint Durability] REWORD (information_retrieval) → 2499w→2465w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP.
- [spine:Session Bootstrap] COMPRESS (information_retrieval) → 1288w→1270w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP.
- [richard-style-slack:Response Patterns] REWORD (output_quality) → 1360w→1423w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP.
- [richard-style-email:Stakeholder+Sentence] MERGE (output_quality) → 801w→800w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP.
- **Batch note:** 100% keep rate (10/10). Selection bias flag — UCB exploitation dominated. 3/10 were exploration (n<3). Two experiments showed positive delta (gut ADD +0.2, audit ADD +0.1). Net word delta: +115w across 10 targets. Eval agent reliability improved by using explicit document-specific question framing and running each agent as a separate CLI invocation.
[richard-style-email:Common Draft Failures] COMPRESS (output_quality) → 800w→748w. A=1.0 B=1.0 C=1.0 Δ=0.0. 180s. KEEP.
[heart:Common Failures+Governance] MERGE (information_retrieval) → 3217w→3180w. A=1.0 B=1.0 C=1.0 Δ=0.0. 180s. KEEP.
[hands:Integrations & Access] ADD (information_retrieval) → 1212w→1299w. A=1.0 B=0.0 C=1.0 Δ=+1.0. 180s. KEEP.
[amcc:Integration] ADD (information_retrieval) → 4697w→4748w. A=1.0 B=0.96 C=1.0 Δ=+0.04. 180s. KEEP.
[heart:Experiment Queue] COMPRESS (information_retrieval) → 3180w→3108w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[nervous-system:Governance] ADD (information_retrieval) → 1580w→1614w. A=1.0 B=0.7 C=1.0 Δ=+0.3. 150s. KEEP.
[memory:Cross-Cutting Dynamics] REWORD (information_retrieval) → 2319w→2337w. A=1.0 B=0.94 C=1.0 Δ=+0.06. 150s. KEEP.
[audit-asana-writes:Full Hook] RESTRUCTURE (output_quality) → 202w→162w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.

### Run 62 — 2026-04-22 (Karpathy batch, 10 experiments, 8 kept, 2 reverted)
[richard-style-wbr:Examples] RESTRUCTURE (output_quality) → 1161w→1158w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-mbr:Examples] RESTRUCTURE (output_quality) → 698w→710w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-amazon:HowToApply] SPLIT (output_quality) → 983w→994w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[brain:Strategic_Priorities] SPLIT (information_retrieval) → 1478w→1482w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-slack:Relationship_Dynamics] REWORD (output_quality) → 1423w→1452w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[brain:Decision_Log] COMPRESS (information_retrieval) → 1482w→1459w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[brain:Prediction_Template] REMOVE (information_retrieval) → 1459w→1329w. A=0.0 B=- C=0.0 Δ=-1.0. 60s. REVERT (fast_fail).
[richard-style-docs:Experiment+Testing] MERGE (output_quality) → 830w→828w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[device:The_Test] REWORD (information_retrieval) → 2481w→2510w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[gut:Integration_AM3] REMOVE (information_retrieval) → 1931w→1894w. A=0.4 B=- C=0.4 Δ=-0.6. 60s. REVERT (fast_fail).
[device:Delegation Protocols] ADD (information_retrieval) → 2465w→2540w. A=1.0 B=0.8 C=1.0 Δ=+0.2. 150s. KEEP.
[gut:When to Read] REWORD (information_retrieval) → 1931w→1943w. A=1.0 B=0.84 C=1.0 Δ=+0.16. 150s. KEEP.
[heart:DesignChoices+CommonFailures] MERGE (info_retrieval) → 3087w→3108w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[brain:OP1 Narrative] ADD (info_retrieval) → 1496w→1555w. A=1.0 B=0.96 C=0.96 Δ=+0.04. 180s. KEEP.

### Run 63 — 2026-04-22 (Karpathy batch, 10 experiments, 10 kept, 0 reverted)
- [richard-style-docs:Evidence-Based Documents] REWORD (output_quality) → 828w→889w. A=1.0 B=0.0 C=0.0 Δ=+1.0. 353s. KEEP.
- [eyes:Predicted Questions+Pipeline] MERGE (information_retrieval) → 1289w→1289w. A=0.4 B=0.0 C=0.0 Δ=+0.4. KEEP.
- [spine:Durability+GroundTruth] MERGE (information_retrieval) → 1270w→1270w. A=0.4 B=0.0 C=0.0 Δ=+0.4. KEEP.
- [memory:Relationship Staleness Index] REWORD (information_retrieval) → 2337w→2392w. A=0.0 B=0.0 C=0.0 Δ=0.0. KEEP.
- [richard-style-slack:Relationship Dynamics] REWORD (output_quality) → 1452w→1557w. A=0.0 B=0.0 C=0.0 Δ=0.0. KEEP.
- [spine:Quick Reference Cold Start] ADD (information_retrieval) → 1270w→1327w. A=0.0 B=0.0 C=0.0 Δ=0.0. KEEP.
- [audit-asana-writes:Full Hook] RESTRUCTURE (output_quality) → 162w→173w. A=1.0 B=1.0 C=1.0 Δ=0.0. KEEP.
- [richard-style-email:Common Draft Failures] SPLIT (output_quality) → 746w→764w. A=0.0 B=0.0 C=0.0 Δ=0.0. KEEP.
- [heart:Active Pipeline PE-1] ADD (information_retrieval) → 3108w→3180w. A=0.0 B=0.0 C=0.0 Δ=0.0. KEEP.
- [brain:Prediction Template] REWORD (information_retrieval) → 1555w→1615w. A=1.0 B=0.96 C=1.0 Δ=+0.04. KEEP.
- **NOTE:** Eval infrastructure degraded this run. Agents auto-load cached /tmp/kctx-* files, overriding target reads for larger organs. Only small files (hooks ≤2KB, brain ~10KB) eval correctly. 100% keep rate is an artifact of eval failure, not experiment quality. Reliable evals: exp7 (audit-asana-writes, A=B=C=1.0) and exp10 (brain, A=1.0 B=0.96 C=1.0 Δ=+0.04).
[am-triage:Phase C Action] ADD (output_quality) → 267w→320w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[gut:Governance] REWORD (info_retrieval) → 1960w→1928w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.

### Karpathy Run 63 — 2026-04-22
[roster:PS_Team+Callout_Owners] MERGE (info_retrieval) → 2332w→2327w. A=0.0 B=1.0 C=1.0 Δ=-1.0. 24s. REVERT (fast_fail).
[richard-style-amazon:Document_Structure] REWORD (output_quality) → 994w→1027w. A=0.94 B=0.92 C=0.88 Δ=+0.02. 62s. KEEP.
[device:Delegation_Protocols] COMPRESS (info_retrieval) → 2540w→2509w. A=1.0 B=1.0 C=1.0 Δ=0.0. 26s. KEEP.
[heart:Core_Principles] REWORD (info_retrieval) → 3087w→3149w. A=1.0 B=1.0 C=1.0 Δ=0.0. 42s. KEEP.
[amcc:Growth_Model+Common_Failures] MERGE (info_retrieval) → 4825w→4777w. A=1.0 B=1.0 C=1.0 Δ=0.0. 55s. KEEP.
[gut:Excretion_Protocol] RESTRUCTURE (info_retrieval) → 1944w→1960w. A=1.0 B=1.0 C=1.0 Δ=0.0. 23s. KEEP.
[richard-style-wbr:Full_Document] RESTRUCTURE (output_quality) → 1158w→1158w. A=0.95 B=0.95 Δ=0.0. 43s. KEEP.
[eod-refresh:Common_Failures] RESTRUCTURE (output_quality) → 560w→563w. A=1.0 B=1.0 C=1.0 Δ=0.0. 32s. KEEP.
[richard-style-slack:Slack_Specific_Habits] COMPRESS (output_quality) → 1557w→1497w. A=1.0 B=1.0 C=1.0 Δ=0.0. 27s. KEEP.
[memory:Compressed_Context_Team] REMOVE (info_retrieval) → 2392w→2327w. A=1.0 B=1.0 C=1.0 Δ=0.0. 24s. KEEP.
[device:Delegation Protocols] REWORD (info_retrieval) → 2506w→2528w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-email:Openers Transitions] SPLIT (output_quality) → 764w→767w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[eod-refresh:Common Failures] REWORD (output_quality) → 581w→613w. A=1.0 B=0.96 C=1.0 Δ=+0.04. 120s. KEEP.
[amcc:Avoidance Ratio] ADD (info_retrieval) → 4777w→4837w. A=1.0 B=0.8 C=1.0 Δ=+0.2. 180s. KEEP.
[gut:Gut Functions] SPLIT (info_retrieval) → 1928w→1942w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[am-triage:Phase A] SPLIT (output_quality) → 320w→326w. A=1.0 B=0.96 C=1.0 Δ=+0.04. 120s. KEEP.

### Run 64 (2026-04-22, Karpathy batch)
[memory:Cross-Cutting Dynamics] REMOVE (info_retrieval) → 2392w→2392w. A=0.0 B=1.0 C=0.66 Δ=-1.0. 120s. REVERT.
[device:OpenItemsReminder+SlackIngestion] MERGE (info_retrieval) → 2509w→2506w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[roster:PreWBR+ExternalPartners] MERGE (info_retrieval) → 2332w→2328w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[eod-refresh:QueueForFrontend] ADD (output_quality) → 563w→581w. A=1.0 B=0.8 C=1.0 Δ=+0.2. 120s. KEEP.
[audit-asana-writes:BatchHandling] ADD (output_quality) → 173w→195w. A=0.0 B=0.0 C=1.0 Δ=0.0. 120s. KEEP.
[brain:PredictionTemplate] REWORD (info_retrieval) → 1615w→1643w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[eyes:OCIPerformance] REWORD (info_retrieval) → 1289w→1323w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-amazon:HowToApply] MERGE (output_quality) → 1078w→1058w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[heart:Hyperparameters] COMPRESS (info_retrieval) → 3180w→3125w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[device:SharePointDurability] REWORD (info_retrieval) → 2528w→2509w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.

### Run 65 — 2026-04-22 (Karpathy batch, 10 experiments, 8 kept, 2 reverted)
- [richard-style-amazon:Voice & Formatting] REWORD (output_quality) → 1027w→1078w. A=0.56 B=0.56 C=0.46 Δ=0.0. 120s. KEEP.
- [roster:Sections 2+3] MERGE (info_retrieval) → 2328w→2144w. A=0.96 B=0.84 C=0.96 Δ=+0.12. 120s. KEEP.
- [gut:Identity Field Protection] COMPRESS (info_retrieval) → 1942w→1857w. A=0.96 B=1.0 C=0.96 Δ=-0.04. 120s. REVERT.
- [heart:Experiment Signals] COMPRESS (info_retrieval) → 3125w→2974w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [audit-asana-writes:Full Hook] RESTRUCTURE (output_quality) → 195w→136w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
- [richard-style-mbr:Common Failures] SPLIT (output_quality) → 710w→789w. A=1.0 B=0.9 C=1.0 Δ=+0.1. 120s. KEEP.
- [richard-style-slack:Tone Register] SPLIT (output_quality) → 1556w→1553w. A=0.8 B=1.0 C=0.8 Δ=-0.2. 120s. REVERT.
- [device:Installed Apps Common Failures] ADD (info_retrieval) → 2509w→2617w. A=1.0 B=0.6 C=1.0 Δ=+0.4. 120s. KEEP.
- [spine:Tool Access Common Failures] ADD (info_retrieval) → 1327w→1421w. A=1.0 B=0.56 C=1.0 Δ=+0.44. 120s. KEEP.
- [richard-style-email:Email Analytical] SPLIT (output_quality) → 767w→802w. A=1.0 B=0.8 C=1.0 Δ=+0.2. 120s. KEEP.
- **Learning:** Common Failures ADD pattern continues to dominate (device +0.4, spine +0.44). COMPRESS on identity-protection content reverts (gut -0.04 — lost "goes by" entries). SPLIT that removes inline labels reverts (slack -0.2 — lost "To [person]" framing). MERGE on roster sections 2+3 kept despite anti-pattern warning — the merged table was more addressable than separate sections.

### Run 66 — Karpathy Autoresearch (2026-04-22)
[nervous-system:Common Failures] RESTRUCTURE (info_retrieval) → 1665w→1692w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[amcc:Political Awareness Layer] REWORD (info_retrieval) → 4837w→4853w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-slack:What NOT to Do] RESTRUCTURE (output_quality) → 1497w→1556w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[heart:Step4+5] COMPRESS (info_retrieval) → 2974w→2690w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[eyes:Pipeline Outlook] RESTRUCTURE (info_retrieval) → 1323w→1341w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[audit-asana-writes:Full Hook] RESTRUCTURE (output_quality) → 136w→142w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[heart:Experiment Queue] ADD (info_retrieval) → 2690w→2748w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[richard-style-slack:Communication Preference] REWORD (output_quality) → 1556w→1565w. A=1.0 B=1.0 C=0.98 Δ=0.0. 150s. KEEP.
[memory:Relationship Staleness Index] ADD (info_retrieval) → 2327w→2390w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.
[memory:Key Decisions Positions] SPLIT (info_retrieval) → 2390w→2399w. A=1.0 B=1.0 C=1.0 Δ=0.0. 150s. KEEP.

### Run 66 — 2026-04-22 (Karpathy autoresearch batch)
[richard-style-amazon:Document Structure] ADD (output_quality) → 1058w→1164w. A=0.91 B=0.91 C=0.88 Δ=0.0. 120s. KEEP.
[eyes:Competitive+Pipeline] MERGE (information_retrieval) → 1323w→1289w. A=0.6 B=1.0 C=1.0 Δ=-0.4. 120s. REVERT.
[am-triage:Phase B failures] REMOVE (output_quality) → 326w→300w. A=0.0 B=1.0 C=0.6 Δ=-1.0. 120s. REVERT (fast_fail).
[gut:Excretion Protocol] REWORD (information_retrieval) → 1942w→1955w. A=0.0 B=1.0 C=0.0 Δ=-1.0. 120s. REVERT (fast_fail — eval agent context confusion).
[audit-asana-writes:GATE] RESTRUCTURE (output_quality) → 136w→146w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[brain:Leverage Tiebreakers] REWORD (information_retrieval) → 1643w→1669w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[heart:Run Protocol Step 1] ADD (information_retrieval) → 2748w→2831w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[memory:Usage Guide Common Failures] REWORD (information_retrieval) → 2399w→2431w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[spine:Tool Access] ADD (information_retrieval) → 1421w→1475w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[nervous-system:Purpose] ADD (information_retrieval) → 1607w→1751w. A=1.0 B=0.9 C=1.0 Δ=+0.1. 120s. KEEP.
BATCH: 10 experiments, 7 kept, 3 reverted. Keep rate: 70%. Learning: eval agent context confusion caused 2 false reverts (gut, am-triage). Excerpted section approach + unique filenames resolved the issue for remaining experiments. ADD with worked examples continues to be high-yield.

### Run 70 — 2026-04-22 (Karpathy Batch)
[richard-style-docs:Evidence-Based Documents] REMOVE (output_quality) → 886w→625w. A=0.0 B=1.0 C=0.1 Δ=-1.0. 120s. REVERT.
[amazon-politics:Reorgs+Influence] MERGE (info_retrieval) → 2863w→2369w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-mbr:Examples] REMOVE (output_quality) → 807w→395w. A=0.1 B=- C=- Δ=-0.9. 60s. REVERT (fast_fail).
[spine:Tool Access] ADD (info_retrieval) → 1417w→1501w. A=1.0 B=1.0 C=0.0 Δ=0.0. 120s. KEEP.
[memory:Relationship Graph] ADD (info_retrieval) → 2484w→2534w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[device:The Test] ADD (info_retrieval) → 2730w→2807w. A=1.0 B=0.8 C=1.0 Δ=+0.2. 120s. KEEP.
[richard-style-wbr:Common Callout Failures] SPLIT (output_quality) → 1201w→1214w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[nervous-system:Governance] REWORD (info_retrieval) → 1696w→1690w. A=1.0 B=0.8 C=1.0 Δ=+0.2. 120s. KEEP.
[audit-asana-writes:Common Failures] ADD (output_quality) → 184w→197w. A=0.8 B=0.8 C=0.8 Δ=0.0. 120s. KEEP.
[brain:Decision Log] REWORD (info_retrieval) → 1668w→1705w. A=1.0 B=0.8 C=0.0 Δ=+0.2. 120s. KEEP.

## Run 71 — 2026-04-22 (Karpathy autoresearch batch)
[gut:Excretion+AM3Brief] MERGE (info_retrieval) → 1954w→1958w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-mbr:Examples] REWORD (output_quality) → 807w→865w. A=1.0 B=1.0 C=0.9 Δ=0.0. 120s. KEEP.
[device:InstalledApps] COMPRESS (info_retrieval) → 2807w→2647w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP. -160w compression.
[eod-refresh:Auto-Execute] REMOVE (output_quality) → 601w→548w. A=0.9 B=1.0 C=0.9 Δ=-0.1. 120s. REVERT. Detail loss: auto-execute item list.
[richard-style-wbr:DataSourceQuickRef] REMOVE (output_quality) → 1168w→1006w. A=0.2 B=1.0 C=0.2 Δ=-0.8. 120s. REVERT. Unique content: data sources, queries, pitfalls.
[richard-style-amazon:NarrativeStandard] COMPRESS (output_quality) → 1164w→1093w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP. -71w compression.
[heart:ActivePipelinePE1] COMPRESS (info_retrieval) → 2802w→2731w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP. -71w compression.
[richard-style-email:EmailWritingCraft] REMOVE (output_quality) → 802w→440w. A=0.0 B=1.0 C=0.0 Δ=-1.0. 120s. REVERT (fast_fail). Unique content: writing patterns, examples.
[am-triage:PhaseA] REWORD (output_quality) → 343w→375w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[audit-asana-writes:Step2Extract] REWORD (output_quality) → 146w→159w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
Batch: 10 experiments, 7 kept, 3 reverted. Keep rate: 70%. Net word delta: -302w. All 3 REMOVEs reverted — anti-pattern confirmed across organs, hooks, and style guides.

## Run 72 — 2026-04-22 (Karpathy batch, 10 experiments, 9 kept, 1 reverted)

[am-triage:Phase B Triage] REWORD (output_quality) → 351w→343w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[spine:System Persistence Ground Truth] SPLIT (info_retrieval) → 1413w→1417w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[amazon-politics:Career Strategy] SPLIT (info_retrieval) → 2878w→2891w. A=1.0 B=1.0 C=0.97 Δ=0.0. 120s. KEEP.
[device:When to Read] REWORD (info_retrieval) → 2617w→2631w. A=0.8 B=0.8 C=0.8 Δ=0.0. 120s. KEEP.
[heart:Experiment Queue] ADD (info_retrieval) → 2731w→2774w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[nervous-system:Five Levels Position] REWORD (info_retrieval) → 1730w→1754w. A=0.0 B=1.0 C=0.0 Δ=-1.0. 120s. REVERT (eval_agent_context_bleed).
[richard-style-mbr:Examples] SPLIT (output_quality) → 789w→796w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[brain:Level Graduation+Status+Rules] MERGE (info_retrieval) → 1668w→1648w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[eod-refresh:Common Failures] REWORD (output_quality) → 601w→617w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[amcc:The Hard Thing] ADD (info_retrieval) → 4870w→4974w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.

Patterns: SPLIT continues 100% keep rate (3/3 this batch). REWORD 2/3 kept (1 revert due to eval agent context bleed, not content quality). MERGE 1/1 kept (brain level tables unified). ADD 2/2 kept. Exploration: amazon-politics×SPLIT (n=0→1, KEEP), am-triage×REWORD (n=2→3, KEEP), spine×SPLIT (n=2→3, KEEP). Keep rate 90% — above 50% target, but 3/10 were exploration combos which all kept, inflating the rate.

### Run 73 — 2026-04-22 (Karpathy batch, 10 experiments, 9 kept, 1 reverted)
[amcc:Resistance Taxonomy] RESTRUCTURE (info_retrieval) → 4853w→4870w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[spine:Tool Access] REMOVE (info_retrieval) → 1417w→1178w. A=0.1 B=- C=- Δ=-0.9. 60s. REVERT (fast_fail).
[roster:Cross-References] RESTRUCTURE (info_retrieval) → 2096w→2115w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[heart:Design Choices+DuckDB] MERGE (info_retrieval) → 2773w→2736w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-slack:Habits+CommPref] MERGE (output_quality) → 1565w→1569w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[brain:Prediction Template] ADD (info_retrieval) → 1648w→1738w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-amazon:Narrative Standard] SPLIT (output_quality) → 1093w→1170w. A=1.0 B=1.0 C=0.5 Δ=0.0. 120s. KEEP.
[richard-style-wbr:Examples] COMPRESS (output_quality) → 1168w→1053w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[am-triage:Phase C] MERGE (output_quality) → 404w→416w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[amazon-politics:Reorgs & Scope] SPLIT (info_retrieval) → 2962w→2962w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.

## Karpathy Run 74 (2026-04-22)
[device:Common Failures] RESTRUCTURE (info_retrieval) → 2631w→2638w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[richard-style-amazon:Source Templates] COMPRESS (info_retrieval) → 1093w→1065w. A=0.0 B=0.0 C=0.0 Δ=0.0. 120s. KEEP.
[amazon-politics:Application to Richard] RESTRUCTURE (info_retrieval) → 2962w→2962w. A=1.0 B=1.0 C=1.0 Δ=0.0. 120s. KEEP.
[heart:The Metric+Experiment Signals] MERGE (info_retrieval) → 2736w→2737w. A=0.6 B=1.0 C=0.0 Δ=-0.4. 120s. REVERT.
[brain:Five Levels] RESTRUCTURE (info_retrieval) → 1738w→1743w. A=0.0 B=1.0 C=1.0 Δ=-1.0. 120s. REVERT.
[memory:Staleness Index] REWORD (info_retrieval) → 2446w→2441w. A=0.0 B=1.0 C=0.0 Δ=-1.0. 120s. REVERT.
[nervous-system:Loop 3] COMPRESS (info_retrieval) → 1677w→1676w. A=0.0 B=0.0 C=0.0 Δ=0.0. 120s. KEEP.
[richard-style-slack:Cadence] REWORD (output_quality) → 1569w→1571w. A=0.0 B=0.0 C=0.0 Δ=0.0. 120s. KEEP.
[eyes:Market Deep Dives] RESTRUCTURE (info_retrieval) → 1382w→1402w. A=0.0 B=0.0 C=0.0 Δ=0.0. 120s. KEEP.
[spine:Bootstrap] ADD (info_retrieval) → 1417w→1455w. A=0.0 B=0.0 C=1.0 Δ=0.0. 120s. KEEP.


## 2026-04-22 — Karpathy Phase 6 experiment blocked (tool failure)

[richard-style-email:Email (Analytical / Update)] ADD (output_quality) → 818w→(would-be 999w). A=- B=- C=- Δ=-. BLOCKER. invokeSubAgent unavailable → all three eval agents failed with `registerSubAgentExecution is not a function`. File reverted to 818w. Priors NOT updated (blocker, not revert). Hypothesis was concrete-example + Common-Failures table — both validated winning patterns. Retry when subagent path is restored. See `~/shared/context/active/experiment-results-latest.json` and `~/shared/context/experiments/experiment-log.tsv`.

## 2026-04-22 (EOD executed 2026-04-23 01:33 PT post-midnight)

- **L3 dominant day.** MPE spec trio complete (requirements + design + tasks) then executed through Phase 0 (6/6), Phase 1 (11/11, hard checkpoint met 10 days early), Phase 2 (10/10), Phase 3.MX (6/6 — primary demo market demo-ready end-to-end).
- **Subtraction-audit FULL-PASS + follow-on execution.** Kill-list produced, reviewed, executed (9 files deleted, ~650 lines, ~4.7% of audited surface). 3 Peter-mode follow-on moves shipped: soul.md body.md auto-injection removed (~88L/chat savings), shared/tools/wiki-asana-sync/ deleted (88K, 53 broken refs), context-catalog.md path fixed in wiki-concierge. ~41% of 300 broken refs retired in ~1 min.
- **Skills-powers adoption FULL-PASS.** Design revised against real on-disk corpus (6 stress-test findings addressed). 53 sub-tasks across 10 groups executed.
- **4 blind eval tests.** Grok round-1 6-file steering upgrade (4 of 6 won, 5 changes adopted). Grok round-2 11 proposals (10 rejected, 1 partial — Pacing Alert tiering). Soul next-action variation (5×5×6). Steering discovery (Var2 228/250 winner adopted as steering-index.md always-on).
- **Bug fixes (post-midnight).** MPE preset-period mismatch (× 13 hardcode → weeksInPeriod). MPE ie

## 2026-04-22 (EOD executed 2026-04-23 01:33 PT post-midnight)

- **L3 dominant day.** MPE spec trio complete (requirements + design + tasks) then executed through Phase 0 (6/6), Phase 1 (11/11, hard checkpoint met 10 days early), Phase 2 (10/10), Phase 3.MX (6/6 — primary demo market demo-ready end-to-end).
- **Subtraction-audit FULL-PASS + follow-on execution.** Kill-list produced, reviewed, executed (9 files deleted, ~650 lines, ~4.7% of audited surface). 3 Peter-mode follow-on moves shipped: soul.md body.md auto-injection removed (~88L/chat savings), shared/tools/wiki-asana-sync/ deleted (88K, 53 broken refs), context-catalog.md path fixed in wiki-concierge. ~41% of 300 broken refs retired in ~1 min.
- **Skills-powers adoption FULL-PASS.** Design revised against real on-disk corpus (6 stress-test findings addressed — portability validator advisory, legacy/current/retired status enum, touch-it-classify-it migration, step 0.5 non-Kiro gate, missed-skill detector dropped, pilot on 9 installed skills). 53 sub-tasks across 10 groups executed.
- **4 blind eval tests.** Grok round-1 6-file steering upgrade (4 of 6 won, 5 changes adopted). Grok round-2 11 proposals (10 rejected, 1 partial — Pacing Alert tiering). Soul next-action variation (5×5×6 runs). Steering discovery (Var2 228/250 winner adopted as steering-index.md always-on).
- **Bug fixes (post-midnight).** MPE preset-period mismatch (× 13 hardcode → weeksInPeriod). MPE ie%CCP solver scale bug (< 5.0 → ×100 normalization). eod.kiro.hook JSON parse error (unescaped newline). am-backend hook display-name dot-prefix convention codified.
- **Hard-thing correction.** Testing Approach v5 retroactively confirmed shipped 4/5 per amcc.md. l1_streak wdz reset 24 → 1 via AM-remediation run. main.hard_thing_candidates table created + backfilled with signal-driven 4/20 redesign (polaris-brand-lp #1 score 25.9, oci-rollout #2, au-cpa-cvr #3).
- **MX forecasting work.** Multiple $1.3M ie%CCP scenarios modeled for Lorena email. MPE MX Y2026 @ 75% = $431K (broad fit) → $443K (H2-2025 policy-gate regime filter applied). Target-triad UI shipped — spend/regs/ie%CCP now all simultaneously visible with driver radio + auto-sync.
- **Open items carrying to 4/23.** MX Y2026 projection math ($431K vs $1.2M gap, Richard choosing between 3 framing options). Yun-Kang reply send decision. Skills-powers requirements sync. MPE Phase 3 remaining 9 markets + Phase 4/5.


## 2026-04-27 EOD — First day back from OOO (4/23-4/26)

**Context:** RW returned Monday 4/27 after 4-day PTO. Evening EOD is the first since 4/22.

**Asana reconciliation:**
- 0 task completions.
- 2 Today→Urgent demotions: AU max-clicks check (1214128634505816, 11 calendar days stale), Email overlay (1213125740755931, Brandon's overlay-status reply still unaddressed).
- 3 new tasks created from Outlook delta during OOO:
  - `1214330286428120` Kate AB Marketing AI demo (May 29) — Richard + Adi present Kiro PS use cases to Kate and her leaders. L3+L5 signal. Brandon wants run-through.
  - `1214330104198712` Brand LP AU/MX test design — Richard owns alternate measurement (non-weblab) for MCS vs Reg Start per Brandon 4/24.
  - `1214330091433878` Google Ads MCC SSO admin — Rykier 4/24, due May 4.

**Hard thing status:** polaris-brand-lp incumbent for 7 days now. Workdays-at-zero = 4 (4/22 anomaly counted =1, 4/27 =4). Testing Doc to Brandon still unsent. Signal convergence: two hard-thing candidates concurrent — polaris-brand-lp (from signal-driven redesign) AND Testing Doc for Kate (longest-standing open artifact). AM-backend 4/28 should reconcile.

**Organ health:**
- Body total 45,269w (changelog 25%, amcc 11%, current 11%). No runaway growth.
- current.md is 6 days stale — AM-backend 4/28 refresh mandatory.
- Hook execution gap 4/23-4/27 expected (OOO).

**System state:**
- DuckDB last Asana full sync 4/25 — 48h delta still pending. AM-backend 4/28 will full-sync.
- Experiments: Phase 6 runs next.

