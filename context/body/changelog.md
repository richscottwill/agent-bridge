<!-- DOC-0220 | duck_id: organ-changelog -->
# Changelog — Body System

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
