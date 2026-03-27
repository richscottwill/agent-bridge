# Implementation Plan: Attention Tracker

## Overview

Build a local-only Linux daemon (~300 LOC Python core) that monitors the active window, classifies activity into productivity categories, and infers attention state (focused, switching, idle) using a Bayesian probabilistic model with hysteresis. Data stored in SQLite with JSON1. CLI commands integrate with Decision Journal and morning routine.

## Tasks

- [x] 1. Set up project structure and core data types
  - [x] 1.1 Create project directory structure and pyproject.toml
    - Create `attention_tracker/` package with `__init__.py`
    - Create `pyproject.toml` with Python 3.10+ requirement, dependencies: `tomli` (for 3.10 compat), `hypothesis` (dev)
    - Create `tests/` directory with `conftest.py`
    - _Requirements: 9.1, 10.1_

  - [x] 1.2 Define core data structures and enums
    - Implement `WindowInfo`, `TabInfo`, `ActivityEvent`, `ClassifiedEvent`, `ClassificationRule` dataclasses
    - Implement `AttentionBeliefs`, `AttentionState`, `AttentionMode` enum (FOCUSED, SWITCHING, IDLE)
    - Implement `TrackerConfig` with all defaults from design (poll_interval_ms=1500, idle_threshold_seconds=120, away_threshold_seconds=300, enter_threshold=0.75, maintain_threshold=0.40, epsilon_floor=0.01, micro_interruption_ms=15000)
    - Implement `FocusSession` and `DailySummary` dataclasses
    - _Requirements: 4.1, 5.4, 9.1_

- [x] 2. Implement Activity Classifier
  - [x] 2.1 Implement classification engine
    - Write `classify_event(event, rules)` that evaluates rules in descending priority order
    - First matching rule wins; unmatched events get category="uncategorized", productivity_score=None
    - Support four match types: WINDOW_CLASS, TITLE_PATTERN, URL_PATTERN, APP_NAME via regex
    - Skip invalid regex patterns with warning logged, continue evaluating remaining rules
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

  - [ ]* 2.2 Write property test: Classification Rule Priority (Property 3)
    - **Property 3: Classification Rule Priority**
    - For any set of rules sorted by priority and any event, if multiple rules match, the classifier returns the highest-priority match. If none match, returns "uncategorized" with None score.
    - **Validates: Requirements 3.1, 3.2, 3.3**

  - [ ]* 2.3 Write property test: Productivity Score Bounds (Property 4)
    - **Property 4: Productivity Score Bounds**
    - For all classified events where productivity_score is not None, the score is within [0.0, 1.0].
    - **Validates: Requirement 3.5**

  - [x] 2.4 Implement TOML rules loader
    - Load classification rules from TOML file at configured rules_path
    - Parse each rule into `ClassificationRule` with name, matchType, pattern, category, productivityScore, priority
    - Implement `validate_rules()` for the `attention-tracker rule validate` CLI command
    - _Requirements: 9.2, 9.3_

- [x] 3. Implement Bayesian State Machine
  - [x] 3.1 Implement Bayesian update algorithm
    - Write `bayesian_update(state, event, config)` following the design pseudocode exactly
    - Compute likelihoods for focused, switching, idle based on category change, idle seconds, event duration
    - Apply micro-interruption tolerance: use focused likelihood 0.4 (not 0.1) when duration < micro_interruption_ms and category changed
    - Compute posterior = prior × likelihood, normalize to sum to 1.0
    - Apply epsilon floor (0.01) to each belief, re-normalize
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 3.2 Implement hysteresis mode inference
    - Write `infer_mode_with_hysteresis(current_mode, beliefs, config)`
    - If current mode belief >= MAINTAIN_THRESHOLD (0.40), preserve current mode
    - If current mode drops below MAINTAIN and another exceeds ENTER_THRESHOLD (0.75), transition
    - Fallback to argmax if no mode exceeds ENTER_THRESHOLD
    - Track focus duration: increment while FOCUSED, reset to 0 on mode change
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [ ]* 3.3 Write property test: Belief Invariants (Property 5)
    - **Property 5: Belief Invariants**
    - After every update: beliefs sum to 1.0 ±0.001, no belief below EPSILON (0.01).
    - **Validates: Requirements 4.1, 4.3**

  - [ ]* 3.4 Write property test: Hysteresis Correctness (Property 6)
    - **Property 6: Hysteresis Correctness**
    - If current mode belief >= MAINTAIN_THRESHOLD, mode preserved. If drops below and another exceeds ENTER_THRESHOLD, transitions. Otherwise argmax.
    - **Validates: Requirements 5.1, 5.2, 5.3**

  - [ ]* 3.5 Write property test: Hysteresis Stability (Property 7)
    - **Property 7: Hysteresis Stability Under Single Contradictory Event**
    - If current mode belief > MAINTAIN_THRESHOLD, a single contradictory event does not change the inferred mode.
    - **Validates: Requirement 5.1**

  - [ ]* 3.6 Write property test: State Machine Determinism (Property 12)
    - **Property 12: State Machine Determinism**
    - Two identical event sequences from the same initial state produce identical belief and mode sequences.
    - **Validates: Requirement 4.2**

- [x] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement Window and Browser Monitors
  - [x] 5.1 Implement Window Monitor
    - Write Wayland-native monitor using `wlr-foreign-toplevel` / `ext-foreign-toplevel-list` as primary
    - Write X11 fallback using `xdotool` / `xprop` subprocess calls
    - Auto-detect display server and select appropriate backend
    - Return sentinel WindowInfo with app_name="unknown" on display server connection loss
    - Emit only on change: deduplicate consecutive identical window polls
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

  - [ ]* 5.2 Write property test: Window Event Deduplication (Property 1)
    - **Property 1: Window Event Deduplication**
    - For any sequence of window polls, emitted events never contain two consecutive events with identical PID, window class, and window title.
    - **Validates: Requirement 1.4**

  - [x] 5.3 Implement Browser Monitor
    - Parse browser window titles to extract page title (format: "{page_title} - {browser_name}")
    - Support major browsers: Firefox, Chrome/Chromium, Edge
    - Fall back gracefully when native messaging extension is not available
    - Read only current active tab context, never browsing history
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [ ]* 5.4 Write property test: Browser Title Extraction Round-Trip (Property 2)
    - **Property 2: Browser Title Extraction Round-Trip**
    - For any browser title "{page_title} - {browser_name}", extracting page title and reconstructing produces the original page title.
    - **Validates: Requirement 2.1**

- [x] 6. Implement Data Layer (SQLite)
  - [x] 6.1 Create database schema and connection manager
    - Create SQLite database with JSON1 extension at configured db_path
    - Implement all tables: `activity_events`, `focus_sessions`, `daily_summaries`
    - Create all indexes from design (timestamp, category, attention_mode, session, start, date)
    - Verify JSON1 with `SELECT json('{}')` on connection
    - _Requirements: 6.1, 6.2_

  - [x] 6.2 Implement event storage with buffering and error recovery
    - Write `store_event()` that persists all activity event fields including beliefs and attention_mode
    - Implement in-memory buffer (max 1000 events) on SQLite write failure
    - Implement exponential backoff retry (1s → 30s max)
    - Drop oldest events when buffer full, log count of dropped events
    - Attempt WAL recovery on corruption; create new DB if recovery fails
    - _Requirements: 6.2, 6.3, 6.6, 6.7, 11.2_

  - [ ]* 6.3 Write property test: Event Storage Round-Trip (Property 8)
    - **Property 8: Event Storage Round-Trip**
    - Any valid event written to DB reads back with all fields equal to the original.
    - **Validates: Requirement 6.2**

  - [ ]* 6.4 Write property test: Temporal Ordering (Property 9)
    - **Property 9: Temporal Ordering**
    - If e1 stored before e2, then e1.timestamp <= e2.timestamp.
    - **Validates: Requirement 6.3**

  - [x] 6.5 Implement Focus Session tracking
    - Create new FocusSession on transition to FOCUSED
    - Close session (set end_time, compute total_duration_ms) on transition away from FOCUSED
    - Track interruption_count and app_sequence (JSON array)
    - Ensure all events with focus_session_id have timestamps within session range
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [ ]* 6.6 Write property test: Focus Session Integrity (Property 11)
    - **Property 11: Focus Session Integrity**
    - Every session has start_time < end_time; every event with session_id falls within [start, end]; new session on each FOCUSED transition.
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4**

  - [x] 6.7 Implement Daily Summary aggregation
    - Compute productivity_score_avg excluding NULL scores from both numerator and denominator
    - Compute total_active_ms including all events regardless of NULL score
    - Generate top_daily_insight one-liner for Decision Journal
    - Store category_breakdown as JSON object
    - _Requirements: 6.4, 6.5_

  - [ ]* 6.8 Write property test: Summary Aggregation Correctness (Property 10)
    - **Property 10: Summary Aggregation Correctness**
    - productivity_score_avg excludes NULL-scored events from both numerator and denominator; total_active_ms includes all events.
    - **Validates: Requirements 6.4, 6.5**

- [x] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement Event Processor and Daemon Loop
  - [x] 8.1 Implement Event Processor
    - Merge signals from Window Monitor, Browser Monitor, and Idle Detector
    - Pipe merged ActivityEvent through Activity Classifier then Bayesian State Machine
    - Store resulting event + beliefs + inferred mode to database
    - Handle daemon restart: read last event timestamp from DB, record "daemon-offline" gap event, reset beliefs to uniform prior (0.33, 0.33, 0.34)
    - _Requirements: 4.6, 11.1, 11.3, 11.4_

  - [x] 8.2 Implement daemon main loop and systemd integration
    - Implement polling loop at configured poll_interval_ms
    - Create systemd service unit file (`attention-tracker.service`) with Restart=on-failure
    - Implement graceful shutdown on SIGTERM/SIGINT
    - Ensure zero network operations in all code paths
    - _Requirements: 8.6, 10.1, 10.2, 10.3, 11.3_

- [x] 9. Implement CLI Tool
  - [x] 9.1 Implement query engine and CLI commands
    - `attention-tracker today` — display current day summary (active time, focus sessions, top category)
    - `attention-tracker yesterday --oneliner` — single-line summary for morning routine
    - `attention-tracker journal` — generate daily summary if needed, output top_daily_insight
    - `attention-tracker sessions --date today` — list focus sessions with start, end, duration, category
    - `attention-tracker unknowns` — list uncategorized app names
    - `attention-tracker start | stop | status` — daemon management
    - `attention-tracker rule validate` — check rules for valid regex
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 9.3_

  - [ ]* 9.2 Write unit tests for CLI commands
    - Test `today` output format and content
    - Test `yesterday --oneliner` produces single-line output
    - Test `journal` generates summary and outputs insight
    - Test `unknowns` lists only uncategorized apps
    - Test `sessions` date filtering
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 10. Integration wiring and end-to-end validation
  - [x] 10.1 Wire all components together
    - Connect Window Monitor → Event Processor → Classifier → State Machine → DB pipeline
    - Wire CLI query engine to SQLite database
    - Wire Decision Journal hook (`attention-tracker journal >> ~/shared/context/intake/attention-insight.md`)
    - Wire morning routine hook (`attention-tracker yesterday --oneliner`)
    - _Requirements: 8.1, 8.2, 8.3_

  - [ ]* 10.2 Write integration tests
    - Simulate window switches end-to-end, verify events + beliefs in DB
    - Test crash recovery: verify beliefs reset to uniform prior, gap recorded as daemon-offline
    - Test CLI round-trip: collect data → query → verify output matches DB
    - _Requirements: 4.6, 6.2, 8.1, 11.3, 11.4_

- [x] 11. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests use the Hypothesis library and validate the 12 correctness properties from the design
- Implementation language: Python 3.10+
- All data local-only, zero network dependencies
