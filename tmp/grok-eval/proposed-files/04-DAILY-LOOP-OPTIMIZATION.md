# Daily Loop Optimization (AM / EOD Hooks — April 2026)

Goal: Make the existing AM-1 / AM-2 / AM-3 and EOD hooks even tighter and more autonomous.

## Recommended Hook Enhancements (propose to Richard)
- **AM-1 (Ingest)**: Auto-process any new files in `uploads/` into DuckDB + generate 3-bullet delta summary.
- **AM-2 (Triage)**: Cross-reference `current.md` + `rw-tracker.md` + latest DuckDB signals → surface only items that move the Five Levels.
- **AM-3 (Brief)**: Output in consistent format: Priorities | Leverage Move | Friction to Remove | Data Snapshot | Open Questions for Richard.
- **EOD-2 (System Refresh)**: Run the new Self-Discovery Query + propose 1 system improvement if friction was detected.

## New "Master Morning Command"
Create a single Kiro command / hook:
**"Run Full Morning Routine"**
This should chain AM-1 → AM-2 → AM-3 and output the brief + updated dashboards + any Slack/Outlook digest.

## High-Leverage Addition
Add a lightweight "Prediction Scoring" hook (nervous-system.md) that scores yesterday's projections vs actuals and surfaces bias patterns for the agent to learn from.
