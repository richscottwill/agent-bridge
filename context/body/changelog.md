# Changelog — Body System

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
