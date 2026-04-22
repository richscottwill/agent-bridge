# Requirements Document: Dry-Run Writes

## Introduction

Add a `dry_run=True` default parameter to all write operations that touch SharePoint or local state files. Today, `/api/feedback` (POST endpoint in Command Center for submitting feedback) writes to disk immediately, `state-file-constraints-sync` writes to SharePoint without confirmation, and several hooks fire writes automatically. One misclick or one bad hook run can overwrite a state file or push stale data to SharePoint — and recovery costs an hour of manual restoration. This spec makes every write operation log what it *would* do instead of executing, unless the caller explicitly passes `confirm=True` or `--execute`.

**Origin**: `.kiro/specs/dashboard-learnings-roadmap/design.md` — Item #7 (Dry-run flag for high-risk write operations). Ranked #7 of 13 roadmap items. Classification: `IMPROVE`, effort S (2–8h), leverage Medium. Source: google-ads-mcp `confirm=True` pattern (all 29 Google Ads write tools require explicit confirmation).

**Five Levels alignment**: L1 (Sharpen Yourself) — prevents accidental writes that corrupt state files or publish unreviewed content. Directly protects the L1 key metric (consecutive weeks shipped) by eliminating the "lost an hour recovering from a bad write" failure mode.

**Soul principles**:
- Protect the habit loop — a dry-run default doesn't change the workflow shape; it adds a confirmation step that prevents the "oh no I just overwrote the state file" moment that breaks the routine. The cue (trigger the write) and reward (data persisted) stay the same; the routine gains a safety check inside it.
- Structural over cosmetic — changing the default from "write immediately" to "dry-run first" is a structural change to how writes behave. It doesn't add a new UI element or warning banner — it changes the default behavior of the operation itself.

## Glossary

- **Dry-run mode**: An execution mode where a write operation logs what it would do (target file, data to write, destination) without actually performing the write. The operation returns a preview of the intended change.
- **Confirm flag**: An explicit parameter (`confirm=True` in Python/API calls, `--execute` in CLI/hook invocations) that overrides dry-run mode and performs the actual write. Without this flag, all writes default to dry-run.
- **Write operation**: Any operation that creates, updates, or deletes data in SharePoint, local state files, or other persistent storage. Read operations are unaffected by this spec.
- **State file**: Per-market markdown file at `~/shared/context/active/` and in SharePoint `Kiro-Drive/state-files/` that captures current metrics, weekly trends, active initiatives, and open items per market.
- **/api/feedback**: POST endpoint in Command Center that writes user feedback to disk. Currently writes immediately without confirmation.
- **state-file-constraints-sync**: Hook or script that synchronizes market constraint data from DuckDB `ps.market_constraints` to SharePoint state files. Currently writes to SharePoint without confirmation.
- **SharePoint write**: Any operation using SharePoint MCP tools (`sharepoint_write_file`, `sharepoint_create_folder`, etc.) that modifies files in OneDrive `Kiro-Drive/`.
- **Dry-run log**: The structured output produced when a write operation runs in dry-run mode — includes the operation name, target path, data summary, and timestamp. Logged to console/stdout, not to a persistent store.
- **Five Levels**: Richard's sequential strategic priorities — L1 Sharpen Yourself → L2 Drive WW Testing → L3 Team Automation → L4 Zero-Click Future → L5 Agentic Orchestration
- **Soul principles**: The 6 "How I Build" principles in `soul.md` — Routine as liberation, Structural over cosmetic, Subtraction before addition, Protect the habit loop, Invisible over visible, Reduce decisions not options
- **Command Center**: Dashboard home view with Hero, Daily Blocks, Integrity Ledger, Actionable Intelligence

## Scope

### In scope

- Adding `dry_run=True` default parameter to `/api/feedback` POST handler
- Adding `dry_run=True` default parameter to `state-file-constraints-sync` hook/script
- Adding `dry_run=True` default parameter to any other hook that writes to SharePoint (identified during design audit)
- Dry-run mode implementation: log what would happen (target, data summary, operation type) instead of executing
- Confirm override mechanism: `confirm=True` parameter (API/Python) and `--execute` flag (CLI/hook) to perform actual writes
- Dry-run log format: structured, human-readable output showing the intended write operation
- Documentation of which operations are covered and how to override dry-run mode

### Out of scope

- Read operations — only write operations are affected
- DuckDB writes — DuckDB is an analytical store, not a state/artifact store; writes there are low-risk and high-frequency (logging, telemetry). Adding dry-run to DuckDB inserts would create friction without proportional safety benefit.
- Asana writes — Asana has its own undo/history; the risk profile is different from file overwrites
- Slack or Outlook message sends — these are communication actions, not data persistence; they have their own confirmation flows
- Automated rollback or versioning of state files (that's a separate concern — this spec prevents bad writes, not recovers from them)
- UI changes to Command Center — dry-run is a backend/API behavior change, not a dashboard feature
- Multi-user access control or permission gating — Richard is the sole user

## Requirements

### Requirement 1: Dry-Run Default for Write Operations

**User Story**: As Richard, I want all write operations that touch SharePoint or state files to default to dry-run mode, so I never accidentally overwrite important data without seeing what would change first.

#### Acceptance Criteria

1. WHEN `/api/feedback` POST is called without a `confirm` parameter, THEN the operation SHALL run in dry-run mode — logging the intended write without executing it
2. WHEN `state-file-constraints-sync` runs without an `--execute` flag, THEN the operation SHALL run in dry-run mode — logging what would be written to SharePoint without executing the write
3. WHEN any hook that writes to SharePoint fires without an explicit confirm/execute parameter, THEN the operation SHALL run in dry-run mode
4. WHEN a write operation runs in dry-run mode, THEN it SHALL return/log a structured preview showing: operation name, target path (file or SharePoint location), data summary (first 200 characters or key fields), and timestamp
5. WHEN a write operation runs in dry-run mode, THEN it SHALL NOT modify any file, SharePoint document, or persistent state — the operation is purely informational

### Requirement 2: Explicit Confirm Override

**User Story**: As Richard, I want to explicitly confirm a write when I'm ready, so the dry-run default doesn't block me — it just makes me opt in to the write.

#### Acceptance Criteria

1. WHEN `/api/feedback` POST is called with `confirm=True` (or equivalent parameter), THEN the operation SHALL execute the actual write as it does today — no dry-run, no preview
2. WHEN `state-file-constraints-sync` is invoked with `--execute` flag, THEN the operation SHALL execute the actual write to SharePoint
3. WHEN a hook is invoked with the confirm/execute parameter, THEN the operation SHALL execute the actual write
4. WHEN a confirmed write executes successfully, THEN the operation SHALL log the same structured output as dry-run mode, plus a confirmation indicator (e.g., `[EXECUTED]` vs `[DRY-RUN]`)
5. WHEN a confirmed write fails, THEN the operation SHALL return the error without having partially written — writes should be atomic where possible

### Requirement 3: Dry-Run Log Output

**User Story**: As Richard reviewing a dry-run result, I want a clear, structured log of what would have happened, so I can decide whether to confirm the write or abort.

#### Acceptance Criteria

1. WHEN a dry-run log entry is produced, THEN it SHALL include: operation name (e.g., `feedback_write`, `constraints_sync`), target path, data summary, timestamp, and a `[DRY-RUN]` label
2. WHEN a dry-run log entry includes a data summary, THEN the summary SHALL show enough context to understand the change (key fields, first 200 characters of content, or diff against current state) without dumping the entire payload
3. WHEN multiple write operations run in dry-run mode in a single session (e.g., a hook that writes to 3 state files), THEN each write SHALL produce its own log entry — not a single combined entry
4. WHEN dry-run logs are produced, THEN they SHALL be written to stdout/console — not to a persistent log file or DuckDB table (keep it simple; persistent logging is a separate concern)

### Requirement 4: Affected Operations Audit

**User Story**: As Richard, I want to know exactly which operations are covered by dry-run mode, so I'm not surprised when a write I expected to be safe actually executes.

#### Acceptance Criteria

1. WHEN the dry-run system is implemented, THEN the design SHALL include a complete inventory of all write operations that touch SharePoint or state files, with each operation marked as: covered (dry-run applied), excluded (with reason), or deferred (to be covered in a future iteration)
2. WHEN the inventory is produced, THEN it SHALL cover at minimum: `/api/feedback` POST, `state-file-constraints-sync`, and any hook in `.kiro/hooks/` that calls SharePoint write MCP tools
3. WHEN a new write operation is added to the system in the future, THEN the dry-run pattern SHALL be documented clearly enough that the developer knows to apply it — the design should include a "how to add dry-run to a new operation" section
4. WHEN an operation is excluded from dry-run coverage, THEN the exclusion reason SHALL be documented (e.g., "DuckDB inserts are high-frequency telemetry writes with no recovery cost")

### Requirement 5: Backward Compatibility

**User Story**: As Richard, I want the dry-run default to not break any existing automation that relies on writes executing immediately — the transition should be safe.

#### Acceptance Criteria

1. WHEN dry-run mode is enabled by default, THEN any existing automation (hooks, scripts, scheduled tasks) that currently writes without a confirm parameter SHALL switch to dry-run mode — this is intentional and expected, not a bug
2. WHEN existing automation needs to continue writing without manual confirmation, THEN the automation SHALL be updated to pass `confirm=True` or `--execute` — the migration is explicit, not implicit
3. WHEN the dry-run system is deployed, THEN a migration checklist SHALL be provided listing every automation that needs the confirm/execute flag added, so nothing silently stops working
4. WHEN an automation runs in dry-run mode unexpectedly (because it wasn't updated), THEN the dry-run log output SHALL make it obvious that the write was skipped — the failure mode is "nothing happened and you can see why," not "nothing happened silently"

## Design Constraints

1. **No new infrastructure**: Dry-run mode must be implementable within existing Python scripts, hook definitions, and API handlers. No new services, databases, or queues.
2. **Single-user assumption**: Richard is the sole user. No multi-user concurrency or permission model needed.
3. **Minimal code change per operation**: Adding dry-run to an operation should require wrapping the write call in a conditional — not restructuring the entire operation. The pattern should be copy-pasteable across operations.
4. **No UI changes**: Dry-run is a backend behavior. The dashboard doesn't need a "dry-run toggle" or "confirm write" button. Confirmation happens at the API/CLI level.
5. **Reversible deployment**: If dry-run mode causes unexpected friction, it should be removable by changing the default parameter back to `False` — no architectural changes needed to revert.
6. **Subtraction check**: This spec adds a parameter to existing operations — it doesn't add new operations, new UI elements, or new data stores. The net complexity increase is minimal: one conditional check per write operation.
