<!-- DOC-0002 | duck_id: audit-blind-evaluator-tests -->
# Blind Evaluator Test Suite

Give a fresh agent ONLY ~/shared/DIRECTORY-MAP.md and these prompts. No other context.
Target: >98% accuracy (49/50+ correct).

## Prompts and Expected Answers

| # | Prompt | Expected Answer |
|---|--------|----------------|
| 1 | Where do I drop a new CSV I downloaded? | uploads/sheets/ |
| 2 | Where is the experiment queue? | context/body/heart.md |
| 3 | Where are AU callouts for week 13? | context/active/callouts/au/au-2026-w13.md |
| 4 | Where do debug scripts go? | tools/scratch/ |
| 5 | Where is the DuckDB database? | data/duckdb/ps-analytics.duckdb |
| 6 | Where do I find the weekly ship log? | artifacts/weekly-ships/ |
| 7 | Where is the test methodology framework? | artifacts/testing/templates/ |
| 8 | Where do agent-generated CSV exports go? | data/exports/ |
| 9 | Where is the org chart? | context/active/org-chart.md |
| 10 | Where do I put a tool I'm building for the team? | tools/team/ |
| 11 | Where are meeting notes for my manager 1:1? | context/meetings/manager/ |
| 12 | Where is the AEO research? | research/aeo/ |
| 13 | Where do autonomous workflow configs go? | tools/autonomous/configs/ |
| 14 | Where is the morning routine script? | context/tools/morning_routine.py |
| 15 | Where do processed data files go after DuckDB ingestion? | data/processed/ |
| 16 | Where is the system navigation map? | context/body/body.md |
| 17 | Where do change log CSVs go? | uploads/changelogs/ |
| 18 | Where is the relationship graph? | context/body/memory.md |
| 19 | Where do I find the callout writing principles? | context/active/callouts/callout-principles.md |
| 20 | Where is the bootstrap sequence? | context/body/spine.md |
| 21 | Where do wiki articles live? | context/wiki/ |
| 22 | Where is the decision log? | context/body/brain.md |
| 23 | Where do I put a PDF document? | uploads/docs/ |
| 24 | Where is the Asana sync protocol? | context/active/asana-sync-protocol.md |
| 25 | Where do per-market data files go for AU? | data/markets/au/ |
| 26 | Where is the willpower/streak tracker? | context/body/amcc.md |
| 27 | Where do completed test results go? | artifacts/testing/completed/ |
| 28 | Where is the portable body? | portable-body/ |
| 29 | Where do I find agent configs? | .kiro/agents/ |
| 30 | Where are hook configs? | .kiro/hooks/ |
| 31 | Where is the directory map? | DIRECTORY-MAP.md |
| 32 | Where do steering files live? | .kiro/steering/ |
| 33 | Where is the current active state? | context/active/current.md |
| 34 | Where do raw unprocessed data files go? | data/raw/ |
| 35 | Where is the system changelog? | context/changelog.md |
| 36 | Where do archived context files go? | context/archive/context/ |
| 37 | Where is the Hedy meeting sync script? | context/tools/hedy-sync.py |
| 38 | Where do test-specific data files go? | data/testing/ |
| 39 | Where is the ad copy research? | research/ad-copy-results.md |
| 40 | Where do reusable frameworks go? | artifacts/frameworks/ |
| 41 | Where is the task tracker? | context/active/rw-tracker.md |
| 42 | Where do MX callouts live? | context/active/callouts/mx/ |
| 43 | Where is the automation impact research? | research/automation-impact/ |
| 44 | Where do team tool docs go? | tools/team/docs/ |
| 45 | Where is the system audit output? | audit-reports/ |
| 46 | Where do ephemeral agent outputs go? | uploads/scratch/ |
| 47 | Where is the market metrics data? | context/body/eyes.md |
| 48 | Where do active test designs go? | artifacts/testing/active/ |
| 49 | Where is the long-term goals doc? | context/active/long-term-goals.md |
| 50 | Where do credentials live? | credentials/ (PROTECTED) |

## Adversarial Prompts

| # | Prompt | Expected Answer | Confusion Point |
|---|--------|----------------|-----------------|
| 51 | I have a CSV — uploads/sheets or data/raw? | uploads/sheets/ (human drop zone) | uploads = human, data/raw = pipeline |
| 52 | Where do I put a one-off analysis script? | tools/scratch/ | Not context/tools/ |
| 53 | Where is the experiment queue vs experiment results? | heart.md (queue) vs artifacts/testing/ (results) | Two different things |
| 54 | Where do archived research files go? | context/archive/research/ | Not research/ |
| 55 | Where is the DuckDB schema? | tools/data/schema.sql | Still in tools/data/ (pipeline code) |
