# EOD Phase Tracker

Write ✅ next to each phase AS YOU COMPLETE IT. Do not start the Frontend until all Backend phases show ✅. If a phase is skipped, write ❌ with a reason. Read this file before presenting any EOD summary.

## Backend
- [ ] Phase 1: Meeting ingestion (Hedy + Outlook + meeting-to-task + analytics)
- [ ] Phase 2: Asana reconciliation (delta sync, daily reset, recurring, completions, blockers)
- [ ] Phase 3: Organ cascade + maintenance (compression, workflow health, communication analytics, enrichment)
- [ ] Phase 4: Recurring task state checks (goal updater, wiki lint, calibration, scorecard)
- [ ] Phase 5: Housekeeping (DuckDB snapshots, git sync, changelog, steering integrity)
- [ ] Phase 6: Experiments (Karpathy CLI — uses subagents for blind eval)
- [ ] Phase 7: Compile output (write structured JSON for EOD-Frontend)
- [ ] Phase 7.5: SharePoint durability sync (push key artifacts to OneDrive)

## Frontend
- [ ] Step 1: EOD summary
- [ ] Step 2: Decisions needed
- [ ] Step 3: Portfolio + ABPS AI summary
- [ ] Step 4: System health
- [ ] Step 5: Experiment results
- [ ] Step 6: Slack DM summary

## Rules
- Phase 7 (compile JSON) is the GATE. No frontend until JSONs exist.
- Phase 6 (Karpathy) runs every EOD. "No fresh changes" is not a valid skip reason.
- If a phase fails, log the reason and continue. Do not silently skip.
