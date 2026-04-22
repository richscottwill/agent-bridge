# Implementation Plan: Dashboard Learnings Roadmap

## Overview

This roadmap spec produces validation, removal, quick-win implementation, and follow-on spec creation tasks — not traditional software implementation. Tasks are grouped into four phases: validate removal candidates, implement XS/S quick wins directly, execute verified removals, and create follow-on specs for M-effort items.

All items trace back to the design.md roadmap (13 ranked items + 4 removals). Requirements references point to requirements.md acceptance criteria.

## Tasks

- [x] 1. Phase 1: Validate removal candidates
  - Verify all four REMOVE candidates are safe before executing any deletions.
  - _Requirements: 7.2, 7.3_

  - [x] 1.1 Validate R1 — Command Center Scratchpad removal safety
    - Grep `~/shared/dashboards/index.html` for all `localStorage.getItem` and `localStorage.setItem` calls referencing scratchpad data
    - Confirm no hook, script, or agent reads Scratchpad data outside its own section
    - Document findings: list any consumers found, or confirm "no consumers"
    - _Requirements: 7.2, 7.3_

  - [x] 1.2 Validate R2 — `build-forecast-tracker.py.legacy` removal safety
    - Grep `refresh-forecast.py` for any `.legacy` file references
    - Grep all Python files in `~/shared/` for `build-forecast-tracker` references
    - Check if any hook or cron references this file
    - Document findings: list any consumers found, or confirm "superseded, no references"
    - _Requirements: 7.2, 7.3_

  - [x] 1.3 Validate R3 — Duplicate forecast `.xlsx` files removal safety
    - Grep `refresh-forecast.py` for ALL `.xlsx` references — list every spreadsheet it touches
    - Identify which of `richard-forecast-tracker.xlsx`, `ps-forecast-tracker.xlsx`, `sp-forecast-tracker-check.xlsx` are actively consumed vs duplicates
    - Check DuckDB `ops.data_freshness` for last-read timestamps on each file
    - Document findings: which file is the source of truth, which are safe to remove
    - _Requirements: 7.2, 7.3_

  - [x] 1.4 Validate R4 — `karpathy-autoresearch-lab.xlsx` removal safety
    - Query DuckDB `ops.data_freshness` for any entry referencing `karpathy-autoresearch-lab`
    - Grep all hooks (`.kiro/hooks/`) for references to this file
    - Check if any agent definition or context file references it
    - Document findings: actively consumed or safe to remove
    - _Requirements: 7.2, 7.3_

- [x] 2. Checkpoint — Review validation results
  - Review all validation findings from Phase 1. If any removal candidate has active consumers, reclassify it from REMOVE to IMPROVE (rename/consolidate) per design.md guidance. Ask Richard if questions arise.

- [x] 3. Phase 2: Quick wins — XS effort items (implement directly)
  - These are XS (<2h) items that can be implemented without a separate spec.
  - _Requirements: 5.4_

  - [x] 3.1 Implement #4 — Agent Success Metrics in agent definitions
    - Read all agent definition files: `market-analyst.md`, `callout-writer.md`, `callout-reviewer.md`, and any others in `~/shared/context/`
    - Add a "Success Metrics" section (3-5 lines) to each agent definition with quantitative targets, following the advertising-hub pattern (e.g., "8/8 dimensions scored per callout", "< 2 revision cycles per article")
    - Metrics should be measurable without manual inspection — tied to existing data in DuckDB or Asana where possible
    - _Requirements: 5.1 (XS effort), 5.2 (Medium leverage), 3.1 (L1 alignment), 4.1 (Structural over cosmetic)_

  - [x] 3.2 Implement #12 — Data staleness indicator
    - In `~/shared/dashboards/index.html` (or the relevant CSS/JS file), add a CSS class toggle on the topbar timestamp element
    - Logic: compare `Date.now()` against the `generated` timestamp in `command-center-data.json`
    - Three states: green (< 4h stale), yellow (4-12h stale), red (> 12h stale)
    - Apply the color to the existing timestamp text — no new UI elements
    - _Requirements: 5.1 (XS effort), 5.2 (Medium leverage), 3.1 (L1 alignment), 4.1 (Invisible over visible)_

- [x] 4. Phase 2 continued: Quick wins — S effort items (implement directly)
  - These are S (2-8h) items. Implement directly with concrete sub-tasks.
  - _Requirements: 5.4_

  - [x] 4.1 Implement #2 — WBR Health Score composite
    - Read the callout reviewer rubric to identify the 8 scoring dimensions and their current 0-10 scale
    - Create a rollup calculation: weighted average across dimensions, producing a single 0-100 composite score
    - Add the composite score as a new field in the callout review output (the data that feeds Command Center)
    - Display the WBR Health Score in Command Center's Hero or top section — one number, one trend arrow (up/down/flat vs last week)
    - Store weekly scores in DuckDB or the callout data pipeline so trends are queryable
    - _Requirements: 5.1 (S effort), 5.2 (High leverage), 3.1 (L1 alignment), 4.1 (Reduce decisions not options)_

  - [x] 4.2 Implement #3 — Hard-gate rules for WBR pipeline
    - Identify the callout reviewer step in the pipeline where quality checks should be enforced
    - Add 2-3 conditional hard gates: (a) if forecast miss > 30% for 3+ consecutive weeks, flag for manual review; (b) if CPA deviation > 2x target, require explicit override; (c) if data staleness > 24h, block publish with warning
    - Gates should block the callout from proceeding to publish — not just warn. Override requires explicit confirmation.
    - Update `ps.market_constraints` DuckDB view if needed to support the gate thresholds
    - _Requirements: 5.1 (S effort), 5.2 (High leverage), 3.1 (L1 alignment), 4.1 (Protect the habit loop)_

  - [x] 4.3 Implement #11 — Change-since-last-look badges
    - Store a `last_seen` timestamp in localStorage keyed to the dashboard session
    - On dashboard load, compare `last_seen` against `command-center-data.json` generated timestamp and item counts per section
    - Show small badge counts on section headers: "3 new" on Actionable Intelligence, "1 updated" on Integrity Ledger, etc.
    - Badges should be subtle (small pill, muted color) — visible only when something changed, invisible when nothing did
    - Update `last_seen` after the user has viewed the dashboard for > 5 seconds (not on immediate load)
    - _Requirements: 5.1 (S effort), 5.2 (High leverage), 3.1 (L1 alignment), 4.1 (Invisible over visible)_

  - [x] 4.4 Implement #1 — PPC Calculator + A/B Test Designer (standalone tool)
    - Create a standalone HTML page (or new dashboard tab) at `~/shared/dashboards/ps-test-calculator.html`
    - **PPC Calculator section**: CPA calculator, ROAS calculator, break-even analysis, budget forecasting, LTV:CAC ratio — pure functions, no external API calls
    - **A/B Test Designer section**: sample size calculator (given baseline conversion rate, minimum detectable effect, significance level, power), test duration estimator (given daily traffic), statistical significance checker (given control/variant results)
    - Use the existing `canon-chart.js` for any visualizations to maintain dashboard consistency
    - Link from Command Center or add as a dashboard tab
    - _Requirements: 5.1 (S effort), 5.2 (High leverage), 3.1 (L2 alignment), 4.1 (Structural over cosmetic)_

- [x] 5. Checkpoint — Verify quick wins
  - Ensure all quick-win implementations work correctly. Test the staleness indicator with stale/fresh data. Verify agent success metrics are present in all agent files. Confirm WBR Health Score calculates correctly. Ask Richard if questions arise.

- [x] 6. Phase 3: Execute verified removals
  - Only proceed with removals that passed Phase 1 validation. Skip any that were reclassified.
  - _Requirements: 7.1, 7.2, 7.3_

  - [x] 6.1 Execute R1 — Remove Command Center Scratchpad (if validated safe)
    - Remove the Scratchpad section from `~/shared/dashboards/index.html`
    - Remove associated CSS and JavaScript for the Scratchpad component
    - Clean up any localStorage keys used by Scratchpad
    - Verify dashboard loads correctly without the Scratchpad section
    - _Requirements: 7.2 (Subtraction before addition), 1.3 (REMOVE justification)_

  - [x] 6.2 Execute R2 — Remove `build-forecast-tracker.py.legacy` (if validated safe)
    - Delete the `.legacy` file
    - Verify `refresh-forecast.py` still runs correctly
    - _Requirements: 7.2, 1.3_

  - [x] 6.3 Execute R3 — Remove duplicate forecast `.xlsx` files (if validated safe)
    - Delete the identified duplicate(s) — keep only the source-of-truth file consumed by `refresh-forecast.py`
    - Update any references if needed
    - Verify forecast refresh pipeline still works
    - _Requirements: 7.2, 1.3_

  - [x] 6.4 Execute R4 — Remove `karpathy-autoresearch-lab.xlsx` (if validated safe)
    - Delete the file
    - Verify no hooks or agents break
    - _Requirements: 7.2, 1.3_

- [x] 7. Checkpoint — Verify removals
  - Confirm all executed removals haven't broken any pipelines, hooks, or dashboard functionality. Run a full dashboard load test. Ask Richard if questions arise.

- [x] 8. Phase 4: Create follow-on specs for M-effort items
  - These items are too large to implement directly. Create a Kiro spec for each so they can be planned and executed in dedicated sessions.
  - _Requirements: 5.5_

  - [x] 8.1 Create follow-on spec: `spec testing-status-toggle` (Item #5)
    - Create `.kiro/specs/testing-status-toggle/` with requirements.md covering:
    - New "Testing" section in Command Center with quick-toggle status pills
    - Data binding to `ps-testing-dashboard.xlsx` or Asana project for test status
    - Write-back logic so toggle updates persist to the data source
    - One-click status cycle: not_started → designed → launched → analyzing → complete
    - _Requirements: 5.5, 3.1 (L2 alignment)_

  - [x] 8.2 Create follow-on spec: `spec system-health-dashboard` (Item #6 — widened)
    - Create `.kiro/specs/system-health-dashboard/` with requirements.md covering:
    - **Tier 1 — Agent runtime telemetry (must have)**: Create `ops.agent_invocations` DuckDB table (columns: invocation_id, agent_name, caller, invoke_status in {success, failed, unreachable, timed_out}, duration_seconds, error_message, invoked_at, token_cost_estimate). Add logging shim that records every custom-agent invocation — covers both `invokeSubAgent` calls and `kiro-cli chat --agent X` sessions. Render last-invoked timestamp, 7d/30d invocation counts, and failure counts per agent in Body System view.
    - **Tier 1 — Hook reliability surfacing (must have)**: Render existing `ops.hook_executions` and `ops.hook_reliability` data in Body System — no new logging required, just display last_run + recent_failures + avg_duration per hook. Flag any hook with failures in last 7d or last_run > 72h.
    - **Tier 2 — MCP server registry (should have)**: Parse `~/.kiro/settings/mcp.json` + workspace `mcp.json` configs to build a server list. Add lightweight health-check ping per server. Green (responsive), yellow (slow), red (failed) per server. Alert only on failure — silent when healthy.
    - **Tier 3 — Routing adherence (optional, punt if costly)**: Of chat inputs matching a soul.md routing trigger keyword set, measure % that actually routed to the specialist vs were handled by the main agent. Requires tagging chat inputs or wrapping the routing decision with logging. Scope as a separate experiment if implementation cost is unclear.
    - **Surface**: single panel in Body System view (existing Agent Health card widens to "System Health"). Subsections: Agents (with invocation telemetry), Hooks (reliability), MCP Servers (status). One "idle too long" flag per subsection surfaces removal candidates (Subtraction before addition).
    - **Adoption gate**: ship only if paired with a monthly review cadence that acts on signals (kill idle agents, fix failing hooks). Otherwise the panel is decoration.
    - _Requirements: 5.5, 3.1 (L1 alignment), 4.1 (Invisible over visible; Subtraction before addition)_

  - [x] 8.3 Create follow-on spec: `spec dry-run-writes` (Item #7)
    - Create `.kiro/specs/dry-run-writes/` with requirements.md covering:
    - Add `dry_run=True` default parameter to write operations touching SharePoint or state files
    - Affected operations: `/api/feedback` POST, `state-file-constraints-sync`, any hook that writes to SharePoint
    - Dry-run mode logs what would happen instead of executing
    - Explicit `confirm=True` or `--execute` flag required to perform actual writes
    - _Requirements: 5.5, 3.1 (L1 alignment)_

  - [x] 8.4 Create follow-on spec: `spec context-consolidation` (Item #8)
    - Create `.kiro/specs/context-consolidation/` with requirements.md covering:
    - Audit all context files agents currently load at startup
    - Create a single `ps-context-index.md` that agents read first — an index that references (not replaces) source files
    - Update agent definitions to reference the consolidated index
    - Constraint: consolidated file must NOT be larger than any individual source file (per Subtraction before addition)
    - _Requirements: 5.5, 3.1 (L1 alignment), 4.1 (Subtraction before addition)_

  - [x] 8.5 Create follow-on spec: `spec intelligence-action-links` (Item #13)
    - Create `.kiro/specs/intelligence-action-links/` with requirements.md covering:
    - Per-type action URL generation for Actionable Intelligence table rows
    - Communicate items → Outlook compose link or Slack deep-link
    - Delegate items → Asana task creation link (pre-filled with context)
    - Differentiate items → link to relevant artifact or doc in SharePoint
    - One "action" button per row that opens the right tool
    - _Requirements: 5.5, 3.1 (L1 alignment), 4.1 (Reduce decisions not options)_

- [x] 9. Final checkpoint — Roadmap execution complete
  - All 4 removal candidates validated. All XS/S quick wins implemented. All verified removals executed. All M-effort follow-on specs created. Review the full roadmap coverage against design.md Appendix C metadata table to confirm nothing was missed. Ask Richard if questions arise.

## Notes

- Phase 1 (validation) must complete before Phase 3 (removals) — never delete without verification
- Quick wins (Phase 2) can proceed in parallel with validation since they're additions, not removals
- Items 4 and 12 are XS and should take < 2 hours each
- Items 1, 2, 3, 11 are S and should take 2-8 hours each
- Items 5, 6, 7, 8, 13 are M (1-3 days) and get follow-on specs instead of direct implementation
- If any removal candidate turns out to have active consumers, reclassify to IMPROVE per design.md guidance
- All follow-on specs should follow the requirements-first workflow and reference this roadmap as their origin

