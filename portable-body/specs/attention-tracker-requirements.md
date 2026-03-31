# Requirements Document

## Introduction

Attention Tracker is a local-only Linux daemon that monitors the active window, classifies activity into productivity categories, and infers attention state (focused, switching, idle) using a Bayesian probabilistic model. All data stays on-disk in SQLite. The system surfaces attention patterns through CLI commands that integrate with the Decision Journal and morning routine. This serves Level 1 (Sharpen Yourself) by making attention patterns evidence-based.

## Glossary

- **Tracker_Daemon**: The background process that polls the active window, classifies events, updates Bayesian beliefs, and writes to the database
- **Window_Monitor**: Component that retrieves the currently active window's PID, class, and title from the display server
- **Browser_Monitor**: Component that extracts tab context (title, optional URL) from browser windows via title parsing
- **Activity_Classifier**: Component that maps activity events to categories and productivity scores using priority-sorted regex rules
- **Bayesian_State_Machine**: Component that maintains a probability distribution over attention modes (FOCUSED, SWITCHING, IDLE) and updates it via Bayesian inference on each event
- **Hysteresis_Function**: Sub-component of the Bayesian State Machine that prevents rapid mode oscillation by requiring higher thresholds to enter a mode than to maintain it
- **Query_Engine**: Component that reads from the SQLite database to serve CLI and dashboard queries
- **CLI_Tool**: Command-line interface for querying summaries, managing the daemon, and piping insights to external systems
- **Classification_Rule**: A named regex pattern with match type, category, productivity score, and priority used by the Activity Classifier
- **Attention_Beliefs**: A probability triple (focused, switching, idle) that sums to 1.0, representing the system's confidence in each attention mode
- **Attention_Mode**: One of FOCUSED, SWITCHING, or IDLE — the inferred discrete state derived from beliefs with hysteresis
- **Focus_Session**: A contiguous period where the inferred mode is FOCUSED, tracked with start/end times, interruption count, and app sequence
- **Daily_Summary**: An aggregated record for one calendar day containing active/idle time, focus session count, category breakdown, and a top daily insight
- **ENTER_THRESHOLD**: The belief probability (0.75) a mode must exceed to become the new inferred mode
- **MAINTAIN_THRESHOLD**: The belief probability (0.40) below which the current mode loses its hysteresis hold
- **EPSILON**: The minimum belief floor (0.01) applied to prevent any mode's probability from collapsing to zero
- **Productivity_Score**: A float in [0.0, 1.0] assigned by a classification rule, or NULL for uncategorized events

## Requirements

### Requirement 1: Window Monitoring

**User Story:** As a user, I want the daemon to detect which window is currently active, so that my activity can be tracked without manual input.

#### Acceptance Criteria

1. WHEN the Tracker_Daemon polls the display server, THE Window_Monitor SHALL return the active window's PID, window class, window title, and timestamp
2. WHILE the desktop session uses Wayland, THE Window_Monitor SHALL use Wayland protocols (wlr-foreign-toplevel or ext-foreign-toplevel-list) as the primary method
3. WHILE the desktop session uses X11 or XWayland, THE Window_Monitor SHALL fall back to X11 tools (xdotool/xprop) for window detection
4. WHEN two consecutive polls return identical window information, THE Window_Monitor SHALL emit only one event to avoid duplicate records
5. IF the display server connection is lost, THEN THE Window_Monitor SHALL return a sentinel WindowInfo with app_name set to "unknown" and continue polling

### Requirement 2: Browser Monitoring

**User Story:** As a user, I want the tracker to understand what I'm doing in the browser beyond just "browser is open," so that browser time is classified meaningfully.

#### Acceptance Criteria

1. WHEN the active window belongs to a browser, THE Browser_Monitor SHALL extract the page title from the window title string
2. WHERE the native messaging extension is installed, THE Browser_Monitor SHALL capture the full URL of the active tab
3. WHEN the native messaging extension is not available, THE Browser_Monitor SHALL rely on window title parsing without error
4. THE Browser_Monitor SHALL read only the current active tab context and SHALL NOT access browsing history

### Requirement 3: Activity Classification

**User Story:** As a user, I want my activity automatically categorized (e.g., deep-work, communication, uncategorized), so that I can see where my time goes without manual tagging.

#### Acceptance Criteria

1. WHEN an activity event is received, THE Activity_Classifier SHALL evaluate classification rules in descending priority order and apply the first matching rule
2. WHEN multiple classification rules match an event, THE Activity_Classifier SHALL use the rule with the highest priority value
3. WHEN no classification rule matches an event, THE Activity_Classifier SHALL assign category "uncategorized" and productivity_score NULL
4. THE Activity_Classifier SHALL support four match types: WINDOW_CLASS, TITLE_PATTERN, URL_PATTERN, and APP_NAME
5. FOR ALL classified events where productivity_score is not NULL, THE Activity_Classifier SHALL assign a productivity_score within the range [0.0, 1.0]
6. IF a classification rule contains an invalid regex pattern, THEN THE Activity_Classifier SHALL skip that rule with a warning logged and continue evaluating remaining rules

### Requirement 4: Bayesian Attention State Machine

**User Story:** As a user, I want the system to infer whether I'm focused, switching, or idle using probabilistic reasoning, so that brief interruptions don't destroy my focus tracking.

#### Acceptance Criteria

1. THE Bayesian_State_Machine SHALL maintain Attention_Beliefs as a probability triple (focused, switching, idle) that sums to 1.0 within a tolerance of ±0.001
2. WHEN a classified event is received, THE Bayesian_State_Machine SHALL compute likelihoods for each mode based on category change, idle seconds, and event duration, then update beliefs using Bayes' rule (posterior = prior × likelihood, normalized)
3. THE Bayesian_State_Machine SHALL apply an EPSILON floor of 0.01 to each belief after every update and re-normalize, preventing any mode's probability from collapsing to zero
4. WHEN the event duration is less than the micro_interruption_ms threshold (default 15000ms) and the category changed, THE Bayesian_State_Machine SHALL use a focused likelihood of 0.4 instead of 0.1 to tolerate brief interruptions
5. WHEN idle_seconds exceeds the idle_threshold_seconds (default 120), THE Bayesian_State_Machine SHALL assign a focused likelihood near zero (0.01) and an idle likelihood of at least 0.9
6. IF the Tracker_Daemon restarts after a crash, THEN THE Bayesian_State_Machine SHALL reset beliefs to a uniform prior (0.33, 0.33, 0.34)

### Requirement 5: Hysteresis Mode Inference

**User Story:** As a user, I want the inferred attention mode to be stable and not flip-flop on every event, so that my focus sessions reflect reality.

#### Acceptance Criteria

1. WHILE the current mode's belief is at or above MAINTAIN_THRESHOLD (0.40), THE Hysteresis_Function SHALL preserve the current Attention_Mode regardless of other modes' beliefs
2. WHEN the current mode's belief drops below MAINTAIN_THRESHOLD and another mode's belief exceeds ENTER_THRESHOLD (0.75), THE Hysteresis_Function SHALL transition to that new mode
3. WHEN the current mode's belief drops below MAINTAIN_THRESHOLD and no mode exceeds ENTER_THRESHOLD, THE Hysteresis_Function SHALL select the mode with the highest belief (argmax)
4. THE Hysteresis_Function SHALL require ENTER_THRESHOLD to be strictly greater than MAINTAIN_THRESHOLD

### Requirement 6: Data Storage

**User Story:** As a user, I want all my attention data stored locally in a reliable database, so that I own my data and can query it flexibly.

#### Acceptance Criteria

1. THE Tracker_Daemon SHALL store all activity events, focus sessions, and daily summaries in a local SQLite database with the JSON1 extension enabled
2. WHEN storing an activity event, THE Tracker_Daemon SHALL persist timestamp, app_name, window_class, window_title, url, idle_seconds, duration_ms, category, productivity_score, rule_name, attention_mode, belief_focused, belief_switching, belief_idle, and focus_session_id
3. FOR ALL stored events, THE Tracker_Daemon SHALL maintain temporal ordering: if event e1 was stored before event e2, then e1.timestamp is less than or equal to e2.timestamp
4. WHEN computing productivity_score_avg in a daily summary, THE Query_Engine SHALL exclude events with NULL productivity_score from both the numerator and denominator
5. WHEN computing total_active_ms in a daily summary, THE Query_Engine SHALL include durations from all events regardless of whether productivity_score is NULL
6. IF a SQLite write fails, THEN THE Tracker_Daemon SHALL buffer events in memory (max 1000) and retry with exponential backoff from 1 second to 30 seconds maximum
7. IF the in-memory buffer reaches capacity, THEN THE Tracker_Daemon SHALL drop the oldest events and log the count of dropped events

### Requirement 7: Focus Session Tracking

**User Story:** As a user, I want to see my focus sessions as distinct blocks with start/end times and interruption counts, so that I can understand my deep work patterns.

#### Acceptance Criteria

1. WHEN the Attention_Mode transitions to FOCUSED, THE Tracker_Daemon SHALL create a new Focus_Session with the current timestamp as start_time
2. WHEN the Attention_Mode transitions away from FOCUSED, THE Tracker_Daemon SHALL close the current Focus_Session by setting end_time to the current timestamp and computing total_duration_ms
3. FOR ALL focus sessions, THE Tracker_Daemon SHALL ensure start_time is strictly less than end_time
4. FOR ALL events with a focus_session_id, THE Tracker_Daemon SHALL ensure the event timestamp falls within the session's [start_time, end_time] range
5. WHEN the Attention_Mode is FOCUSED and the focus duration resets to zero, THE Tracker_Daemon SHALL increment the interruption_count on the current Focus_Session

### Requirement 8: CLI and Integration

**User Story:** As a user, I want CLI commands that surface attention insights and pipe them into my Decision Journal and morning routine, so that the data becomes actionable without opening a separate dashboard.

#### Acceptance Criteria

1. WHEN the user runs `attention-tracker today`, THE CLI_Tool SHALL display the current day's summary including total active time, focus session count, and top category
2. WHEN the user runs `attention-tracker yesterday --oneliner`, THE CLI_Tool SHALL output a single-line summary of the previous day's attention pattern suitable for the morning routine
3. WHEN the user runs `attention-tracker journal`, THE CLI_Tool SHALL generate the daily summary if not already materialized and output the top_daily_insight as a single sentence
4. WHEN the user runs `attention-tracker sessions --date today`, THE CLI_Tool SHALL list all focus sessions for the specified date with start time, end time, duration, and category
5. WHEN the user runs `attention-tracker unknowns`, THE CLI_Tool SHALL list all uncategorized app names observed, so the user can create classification rules for them
6. WHEN the user runs `attention-tracker start`, THE CLI_Tool SHALL start the Tracker_Daemon; `stop` SHALL stop it; `status` SHALL report whether the daemon is running

### Requirement 9: Configuration

**User Story:** As a user, I want to configure polling intervals, thresholds, and classification rules via files, so that I can tune the tracker to my workflow.

#### Acceptance Criteria

1. THE Tracker_Daemon SHALL load configuration from a TrackerConfig structure with sensible defaults: poll_interval_ms=1500, idle_threshold_seconds=120, away_threshold_seconds=300, enter_threshold=0.75, maintain_threshold=0.40, epsilon_floor=0.01, micro_interruption_ms=15000
2. THE Activity_Classifier SHALL load classification rules from a TOML file at the configured rules_path (default ~/.config/attention-tracker/rules.toml)
3. WHEN the user runs `attention-tracker rule validate`, THE CLI_Tool SHALL check all rules for valid regex patterns and report any errors before the daemon loads them

### Requirement 10: Data Locality and Privacy

**User Story:** As a user, I want absolute certainty that none of my attention data leaves my machine, so that I can track sensitive work without privacy concerns.

#### Acceptance Criteria

1. THE Tracker_Daemon SHALL perform zero network operations — all reads and writes target local filesystem paths only
2. THE Tracker_Daemon SHALL store the database at a local path (default ~/.local/share/attention-tracker/tracker.db) with no replication or sync to external services
3. THE Tracker_Daemon SHALL NOT include any telemetry, analytics, or crash reporting that transmits data over a network

### Requirement 11: Error Recovery

**User Story:** As a user, I want the daemon to handle failures gracefully and recover automatically, so that tracking continues even when things go wrong.

#### Acceptance Criteria

1. IF the display server connection is lost, THEN THE Tracker_Daemon SHALL record events with app_name "unknown" and resume normal tracking when the connection is restored
2. IF the SQLite database becomes corrupted, THEN THE Tracker_Daemon SHALL attempt WAL recovery; if recovery fails, THE Tracker_Daemon SHALL create a new database and log the incident
3. IF the Tracker_Daemon process crashes, THEN systemd SHALL restart it via Restart=on-failure, and THE Tracker_Daemon SHALL record the gap as a "daemon-offline" event on restart
4. WHEN the Tracker_Daemon restarts, THE Tracker_Daemon SHALL read the last event timestamp from the database to identify the offline gap
