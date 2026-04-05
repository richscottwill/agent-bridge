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
