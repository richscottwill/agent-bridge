# EOD Phase Tracker

Write ✅ next to each phase AS YOU COMPLETE IT. Write ❌ REASON next to any skipped phase. Read this file before presenting any EOD summary.

## Backend
- [ ] Phase 1: Meeting ingestion (Hedy + Outlook + meeting-to-task + analytics)
- [ ] Phase 2: Asana reconciliation (delta sync, daily reset, recurring, completions, blockers)
- [ ] Phase 3: Organ cascade + maintenance (compression, workflow health, communication analytics, enrichment)
- [ ] Phase 4: Recurring task state checks (goal updater, wiki lint, calibration, scorecard)
- [ ] Phase 5: Housekeeping (DuckDB via MCP, git sync, changelog, steering integrity)
- [ ] Phase 6: Experiments (Karpathy CLI — uses subagents for blind eval)
- [ ] Phase 7: Compile output (write structured JSON for EOD-Frontend)
- [ ] Phase 7.5: SharePoint durability sync (push key artifacts to OneDrive)

## Frontend
- [ ] Step 0: HARD GATE — verify all 3 JSONs exist with today's date (eod-reconciliation.json, eod-maintenance.json, eod-experiments.json). If ANY missing → go back and complete the backend phase. Do NOT proceed.
- [ ] Step 0.5: SKIP CHECK — if any backend phase shows ❌, the FIRST LINE of the EOD summary must be: "⚠️ INCOMPLETE RUN — Phases [X] skipped: [reasons]". This goes BEFORE the task table.
- [ ] Step 1: EOD summary
- [ ] Step 2: Decisions needed
- [ ] Step 3: Portfolio + ABPS AI summary
- [ ] Step 4: System health
- [ ] Step 5: Experiment results
- [ ] Step 6: Slack DM summary

## Enforcement Rules
- Phase 7 (compile JSON) is the GATE. No frontend until JSONs exist with today's date.
- Phase 6 (Karpathy) runs every EOD. "No fresh changes" is not a valid skip reason.
- "Context budget" is not a valid skip reason. If context is tight, use subagents for individual phases.
- "MotherDuck unavailable" is not a valid skip reason. All DuckDB access goes through DuckDB MCP — if MCP is connected, DuckDB is available.
- If a phase genuinely fails (tool error, MCP down), log the specific error and write a skip JSON: `{"generated": "YYYY-MM-DD", "status": "skipped", "reason": "[error]"}`.
- Silent skipping is forbidden. Every skip must be visible in the frontend summary's first line.
