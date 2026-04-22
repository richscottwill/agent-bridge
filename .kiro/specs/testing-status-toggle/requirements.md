# Requirements Document: Testing Status Toggle

## Introduction

Add a "Testing" section to the Command Center dashboard with quick-toggle status pills for all active tests across markets. Currently, test status lives in `ps-testing-dashboard.xlsx` (a SharePoint spreadsheet tracking test status across all markets), requiring a 30-second round-trip to open, find the row, update the cell, and save. This spec reduces that to a 1-second click in Command Center — the same pattern the Integrity Ledger already uses for commitment tracking, extended to the testing domain.

**Origin**: `.kiro/specs/dashboard-learnings-roadmap/design.md` — Item #5 (Testing status quick-toggle in Command Center). Ranked #5 of 13 roadmap items. Classification: `IMPROVE`, effort M (1–3 days), leverage High.

**Five Levels alignment**: L2 (Drive WW Testing) — "every test has written status" is the L2 key metric. A quick-toggle in Command Center makes status updates a 1-second action instead of a 30-second spreadsheet round-trip. This directly unblocks the L2 key metric by making test status updates trivially easy.

**Soul principle**: Reduce decisions not options — the status options don't change; the friction to update them drops to near-zero. Invisible over visible — the toggle writes back to the data source without Richard noticing the plumbing.

## Glossary

- **Command Center**: Dashboard home view at `~/shared/dashboards/index.html` with Hero, Daily Blocks, Integrity Ledger, Actionable Intelligence, and other sections
- **Testing Section**: The new section this spec adds to Command Center, displaying active tests grouped by market with quick-toggle status pills
- **Status Pill**: A clickable UI element showing the current status of a test as a colored label. Clicking cycles to the next status in the sequence.
- **Status Cycle**: The fixed sequence of test statuses: `not_started` → `designed` → `launched` → `analyzing` → `complete`
- **ps-testing-dashboard.xlsx**: SharePoint spreadsheet (OneDrive `Kiro-Drive/ps-testing-dashboard.xlsx`) tracking test status, hypothesis, design, launch date, and results across all markets
- **Write-back**: The mechanism by which a status toggle in the dashboard persists the change to the authoritative data source (SharePoint xlsx or Asana project), not just to localStorage
- **Integrity Ledger**: Existing Command Center section with click-to-cycle status pills for commitments — the UX pattern this spec extends to tests
- **Data Source**: Either `ps-testing-dashboard.xlsx` on SharePoint or an Asana project — the authoritative store for test status. The design phase will determine which is primary.
- **Five Levels**: Richard's sequential strategic priorities — L1 Sharpen Yourself → L2 Drive WW Testing → L3 Team Automation → L4 Zero-Click Future → L5 Agentic Orchestration
- **Soul principles**: The 6 "How I Build" principles in `soul.md` — Routine as liberation, Structural over cosmetic, Subtraction before addition, Protect the habit loop, Invisible over visible, Reduce decisions not options

## Scope

### In scope

- New "Testing" section in Command Center displaying all active tests with status pills
- Data binding to read test data from `ps-testing-dashboard.xlsx` (SharePoint) or an Asana project
- Write-back logic so clicking a status pill persists the change to the data source
- One-click status cycle: `not_started` → `designed` → `launched` → `analyzing` → `complete`
- Per-market grouping of tests within the Testing section
- Visual consistency with existing Integrity Ledger status pill pattern
- Integration with the existing Command Center layout and refresh pipeline

### Out of scope

- Creating new tests from the dashboard (test creation stays in the spreadsheet or Asana)
- Editing test metadata (hypothesis, design details, launch date, results) — only status toggles
- Historical test status tracking or audit log (the data source handles history)
- Notifications or alerts when a test status changes
- Multi-user concurrent editing conflict resolution (Richard is the sole user)
- Replacing `ps-testing-dashboard.xlsx` — the spreadsheet remains the source of truth; the dashboard is a faster interface to it
- Mobile or responsive layout — the dashboard is desktop-only

## Requirements

### Requirement 1: Testing Section Display

**User Story**: As Richard opening Command Center, I want to see all active tests with their current status at a glance, so I don't have to open the SharePoint spreadsheet to know where things stand.

#### Acceptance Criteria

1. WHEN Command Center loads, THEN a "Testing" section SHALL appear showing all tests whose status is not `complete`
2. WHEN tests are displayed, THEN each test SHALL show: test name, market, and current status as a colored pill
3. WHEN tests are displayed, THEN they SHALL be grouped by market (e.g., AU, MX, US, JP, etc.) with a market header per group
4. WHEN a market has zero active tests, THEN that market group SHALL NOT appear in the Testing section
5. WHEN the Testing section has zero active tests across all markets, THEN it SHALL display a single line: "No active tests" rather than an empty section

### Requirement 2: Status Pill Quick-Toggle

**User Story**: As Richard reviewing test status, I want to click a status pill to advance it to the next stage, so updating status is a 1-second action instead of a 30-second spreadsheet round-trip.

#### Acceptance Criteria

1. WHEN Richard clicks a status pill, THEN the status SHALL advance to the next value in the cycle: `not_started` → `designed` → `launched` → `analyzing` → `complete`
2. WHEN the status is `complete` and Richard clicks the pill, THEN the status SHALL NOT cycle back to `not_started` — `complete` is a terminal state (the test disappears from active view on next refresh)
3. WHEN a status pill is clicked, THEN the pill color and label SHALL update immediately in the UI (optimistic update) before the write-back completes
4. WHEN a status pill is clicked, THEN the pill SHALL show a brief visual confirmation (e.g., subtle flash or checkmark) indicating the click was registered
5. WHEN the status cycle is displayed, THEN each status SHALL have a distinct color: `not_started` (gray), `designed` (blue), `launched` (yellow), `analyzing` (orange), `complete` (green)

### Requirement 3: Data Binding — Read

**User Story**: As Richard, I want the Testing section to pull live test data from the authoritative source, so the dashboard always reflects the real state of my tests.

#### Acceptance Criteria

1. WHEN Command Center refreshes, THEN the Testing section SHALL read test data from the configured data source (`ps-testing-dashboard.xlsx` on SharePoint or an Asana project)
2. WHEN reading from the data source, THEN the system SHALL extract at minimum: test name, market, and current status per test
3. WHEN the data source is unreachable (network error, auth failure), THEN the Testing section SHALL display the last successfully loaded data with a staleness indicator (e.g., "Data from 2h ago")
4. WHEN the data source contains a status value not in the defined cycle, THEN the system SHALL display it as-is with a neutral color and log a warning — it SHALL NOT crash or hide the test

### Requirement 4: Write-Back — Persist Status Changes

**User Story**: As Richard, I want my status toggle clicks to persist to the data source, so the change is real — not just a localStorage illusion that disappears when I close the browser.

#### Acceptance Criteria

1. WHEN a status pill is clicked, THEN the system SHALL write the new status back to the authoritative data source (SharePoint xlsx or Asana project)
2. WHEN the write-back succeeds, THEN the system SHALL NOT show any additional confirmation beyond the immediate UI update (invisible over visible — success is silent)
3. WHEN the write-back fails, THEN the system SHALL show a non-blocking error indicator on the affected pill (e.g., red outline or retry icon) and revert the optimistic UI update
4. WHEN the write-back fails, THEN the system SHALL queue the failed update for automatic retry on the next refresh cycle
5. WHEN multiple status changes are made in rapid succession, THEN the system SHALL batch or serialize writes to avoid race conditions with the data source

### Requirement 5: Per-Market Test Grouping

**User Story**: As Richard managing tests across AU, MX, and other markets, I want tests grouped by market so I can quickly scan the status of a specific market's testing program.

#### Acceptance Criteria

1. WHEN tests are displayed, THEN they SHALL be grouped under market headers sorted alphabetically (AU, CA, DE, ES, FR, IT, JP, MX, UK, US)
2. WHEN a market header is displayed, THEN it SHALL show the market code and a count of active tests (e.g., "AU (3)")
3. WHEN tests within a market are displayed, THEN they SHALL be sorted by status in cycle order (`not_started` first, `analyzing` last) so the least-progressed tests are most visible

### Requirement 6: Integration with Command Center Layout

**User Story**: As Richard, I want the Testing section to feel like a native part of Command Center, not a bolted-on afterthought, so the dashboard remains a single coherent surface.

#### Acceptance Criteria

1. WHEN the Testing section is rendered, THEN it SHALL use the same CSS framework, font sizes, spacing, and color palette as existing Command Center sections (Hero, Daily Blocks, Integrity Ledger, Actionable Intelligence)
2. WHEN the Testing section is positioned, THEN it SHALL appear after the Integrity Ledger and before Actionable Intelligence — logically grouping commitment tracking (Ledger) with test tracking (Testing) before action items (Intelligence)
3. WHEN the dashboard data refresh runs (via `command-center-data.json` regeneration), THEN the Testing section data SHALL be included in the same refresh cycle — no separate refresh button or manual trigger
4. WHEN the Testing section is added, THEN it SHALL NOT increase the initial dashboard load time by more than 500ms (the SharePoint read can be async/deferred)

## Design Constraints

1. **No new infrastructure**: The Testing section must work within the existing dashboard architecture — HTML/CSS/JS in `~/shared/dashboards/`, data via `command-center-data.json` or direct SharePoint/Asana API calls, no new backend services.
2. **Single-user assumption**: Richard is the sole user. No multi-user concurrency, no auth beyond existing SharePoint/Asana credentials.
3. **Existing pattern reuse**: The status pill UX must match the Integrity Ledger's existing click-to-cycle pattern. Don't invent a new interaction model.
4. **Data source flexibility**: The design must support either `ps-testing-dashboard.xlsx` (SharePoint) or an Asana project as the data source. The design phase will determine which is primary, but the requirements accommodate both.
5. **Subtraction check**: Adding the Testing section is justified because it replaces a higher-friction workflow (opening SharePoint → finding the spreadsheet → locating the row → editing the cell → saving). If the friction reduction doesn't materialize in practice, the section should be removable without breaking anything else.
