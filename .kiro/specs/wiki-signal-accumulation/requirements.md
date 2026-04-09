# Requirements Document

## Introduction

The Wiki Signal Accumulation Pipeline replaces manual wiki pipeline triggering with an autonomous signal-driven model. Content tasks in ABPS AI Content passively accumulate evidence from daily signals (Slack, email, meetings, DuckDB data changes, Asana activity) until signal density crosses a readiness threshold — then the wiki pipeline fires automatically. High-impact signals (Brandon/Kate directives, deadline-driven events) bypass accumulation and trigger immediately.

This is a wiring job — the signal sources (AM-Backend ingestion), the content tasks (ABPS AI Content project), and the wiki pipeline (editor → researcher → writer → critic → librarian) all exist. The gap is the matching, accumulation, scoring, and triggering layer between them.

## Glossary

- **Signal**: Any incoming data point from Slack, email, meetings, DuckDB, or Asana activity — already captured in `signals.unified_signals`
- **Content Task**: An ABPS AI Content project task at Pipeline_RW = Idea, representing a potential wiki article
- **Evidence**: A signal matched to a content task, stored in `wiki.content_evidence`
- **Readiness Score**: A 0-100 score computed from accumulated evidence, measuring whether a content task has enough context to justify writing
- **Threshold**: The readiness score (60) at which a content task advances from Idea to Drafting
- **Directive**: A signal from Brandon or Kate containing action language (e.g., "put together a doc on X") — bypasses accumulation
- **Signal Matcher**: Component that scores signal-to-task similarity using keyword overlap
- **Evidence Ledger**: Append-only DuckDB table (`wiki.content_evidence`) logging all matched signals
- **Readiness Scorer**: Component that computes readiness from accumulated evidence
- **Pipeline Trigger**: The mechanism that advances Pipeline_RW from Idea → Drafting when threshold is met

## Requirements

### Requirement 1: Signal-to-Content Matching

**User Story:** As the system, I want to automatically match incoming signals to existing ABPS AI Content tasks by topic, so that evidence accumulates without Richard's intervention.

#### Acceptance Criteria

1. WHEN AM-Backend processes new signals, THE Signal Matcher SHALL compare each unmatched signal against all content tasks at Pipeline_RW = Idea
2. WHEN a signal matches a content task with confidence ≥ 0.6, THE system SHALL insert a row into `wiki.content_evidence` with the task_gid, signal_id, source_type, confidence, and matched keywords
3. WHEN a signal matches a content task, THE system SHALL update `signals.unified_signals` setting `disposition = 'matched'` and `disposition_task_gid` to the matched task's GID
4. WHEN a signal does not match any content task at confidence ≥ 0.6, THE system SHALL update `signals.unified_signals` setting `disposition = 'unmatched'`
5. WHEN a signal matches multiple content tasks, THE system SHALL assign it to the highest-confidence match only
6. THE Signal Matcher SHALL use keyword extraction from signal text compared against task name, Category_RW, Series_RW, and description keywords
7. THE Signal Matcher SHALL NOT use external ML models or API calls — matching is keyword-based and runs locally

### Requirement 2: Evidence Accumulation

**User Story:** As Richard, I want content tasks to passively collect evidence from daily signals over time, so that articles are written only when there's enough substance.

#### Acceptance Criteria

1. THE `wiki.content_evidence` table SHALL be append-only — evidence rows are never deleted or modified after insertion
2. WHEN evidence is inserted, THE system SHALL record the source_type (slack, email, meeting, data, asana), source_author, a 200-char content preview, and the match confidence
3. WHEN a signal is from Brandon (brandoxy) or Kate (kataxt) and contains action language (e.g., "put together", "write up", "document", "create a doc"), THE system SHALL set `is_directive = true` on the evidence row
4. WHEN a DuckDB data change is detected that relates to a content task's topic (e.g., new market data for an AU Market Wiki task), THE system SHALL set `is_data_change = true` on the evidence row
5. THE system SHALL prevent duplicate evidence by enforcing a primary key on (task_gid, signal_id)

### Requirement 3: Readiness Scoring

**User Story:** As the system, I want to compute a readiness score for each content task based on its accumulated evidence, so that the pipeline triggers at the right time — not too early, not too late.

#### Acceptance Criteria

1. THE Readiness Scorer SHALL compute a score on a 0-100 scale with five components: signal count (0-25, confidence-weighted), source diversity (0-25), recency (0-20), author weight (0-15), and data availability (0-15)
2. WHEN a content task has evidence with `is_directive = true`, THE Readiness Scorer SHALL return a score of 100 regardless of other evidence
3. THE readiness threshold for triggering the pipeline SHALL be 60
4. THE Readiness Scorer SHALL apply recency decay — signals older than 30 days contribute reduced recency points
5. THE Readiness Scorer SHALL weight signals from Brandon and Kate higher than signals from other authors (15 points for any Brandon/Kate signal vs 0 for others)
6. THE Readiness Scorer SHALL award data availability points when DuckDB contains relevant data for the content task's topic (e.g., ps.performance data for a market wiki)
7. THE signal count component SHALL use confidence-weighted counting: `min(25, sum(confidence) * 5)` — higher-confidence matches contribute more than lower-confidence matches

### Requirement 4: Pipeline Triggering

**User Story:** As the system, I want content tasks to automatically advance from Idea to Drafting when their readiness score crosses the threshold, so that the wiki pipeline fires without Richard's prompting.

#### Acceptance Criteria

1. WHEN a content task's readiness score reaches or exceeds 60, THE system SHALL update the task's Pipeline_RW from Idea to Drafting in Asana
2. WHEN a content task is triggered, THE system SHALL update Kiro_RW with trigger context: date, score, evidence count, source diversity, and the triggering signal
3. WHEN a content task is triggered, THE system SHALL insert a row into `wiki.pipeline_triggers` recording the trigger type, score, and evidence summary
4. WHEN a content task is already at Pipeline_RW = Drafting or later, THE system SHALL NOT re-trigger it (idempotent)
5. WHEN a directive signal is detected, THE system SHALL trigger the pipeline immediately without waiting for the next scoring cycle
6. THE system SHALL append an audit log entry to `asana-audit-log.jsonl` for every Pipeline_RW change

### Requirement 5: Content Task Sync

**User Story:** As the system, I want ABPS AI Content tasks mirrored to DuckDB for efficient querying during signal matching, so that the matcher doesn't need to call the Asana API for every signal.

#### Acceptance Criteria

1. THE system SHALL maintain a `wiki.content_tasks` table in DuckDB mirroring all ABPS AI Content tasks with their metadata (name, pipeline_stage, category, audience, series, frequency, levels, keywords)
2. THE system SHALL sync content tasks from Asana to DuckDB during AM-Backend, before signal matching runs
3. WHEN a content task's Pipeline_RW changes in Asana, THE sync SHALL update `wiki.content_tasks.pipeline_stage` accordingly
4. THE sync SHALL extract keywords from task names and descriptions for use by the Signal Matcher

### Requirement 6: AM-Backend Integration

**User Story:** As the system, I want signal accumulation to run as part of the existing AM-Backend routine, so that it happens automatically every morning without a separate trigger.

#### Acceptance Criteria

1. THE signal accumulation phase SHALL run during AM-Backend, after signal ingestion (Slack, email, Asana) and before brief generation
2. THE AM-Backend SHALL sync content tasks to DuckDB before running the signal matcher
3. THE AM-Backend SHALL process all signals with `disposition IS NULL` in `signals.unified_signals`
4. THE AM-Backend SHALL compute readiness scores for all content tasks that have new evidence since the last scoring run
5. THE AM-Backend SHALL write trigger results to the pre-computed state files for AM-Frontend consumption

### Requirement 7: AM-Frontend Integration

**User Story:** As Richard, I want to see content task readiness in my daily brief, so that I know which articles are approaching the trigger threshold and can manually intervene if needed.

#### Acceptance Criteria

1. THE daily brief SHALL include a Content Pipeline section showing each Idea-stage task's readiness score, evidence count, source diversity, and distance to threshold
2. WHEN a content task was triggered during the current AM cycle, THE brief SHALL flag it with a ✅ TRIGGERED indicator
3. WHEN a content task is within 10 points of the threshold, THE brief SHALL flag it as "near threshold"
4. THE brief SHALL list the most recent signal matched to each content task for context

### Requirement 8: Wiki Pipeline Execution

**User Story:** As the system, I want triggered content tasks to flow through the full wiki pipeline (editor → researcher → writer → critic → librarian) automatically, so that articles are produced without manual orchestration.

#### Acceptance Criteria

1. WHEN a content task reaches Pipeline_RW = Drafting, THE wiki-editor SHALL be invoked to define the article outline and assign research topics
2. THE wiki-editor SHALL read the task's accumulated evidence from `wiki.content_evidence` to inform the outline
3. THE wiki pipeline SHALL follow the existing execution order: editor → researcher → writer → critic (dual blind eval) → librarian
4. THE wiki pipeline SHALL respect all existing pipeline rules (dual blind eval, 8/10 bar, appendix-heavy structure, no trainer voice, max 2 revision cycles)
5. WHEN the pipeline completes (Published or max revisions exceeded), THE system SHALL update Pipeline_RW accordingly and log the outcome
6. THE system SHALL process at most 1 content task through the full wiki pipeline per AM cycle to avoid context window exhaustion
7. WHEN multiple tasks are triggered simultaneously, THE system SHALL queue them by readiness score (highest first) and process one per cycle
8. WHEN a wiki agent invocation fails (kiro-cli error, timeout, SSE failure), THE system SHALL retry on the next AM cycle, up to 2 retries before flagging to Richard
9. THE orchestrating agent (AM-Backend) SHALL invoke wiki agents via kiro-cli in sequence: editor → researcher → writer → critic (2 separate evals) → librarian

### Requirement 9: Observability and Calibration

**User Story:** As Richard, I want to see how well the signal matching and readiness scoring are working, so that I can tune thresholds and matching quality over time.

#### Acceptance Criteria

1. THE system SHALL populate `signals.wiki_candidates` view with topics that have accumulated evidence but haven't triggered yet, ranked by readiness score
2. THE `wiki.pipeline_triggers` table SHALL record every trigger event with the trigger type, score, evidence count, and source diversity for post-hoc analysis
3. THE system SHALL log match confidence distributions to enable threshold tuning (e.g., if most matches are at 0.55-0.65, the 0.6 threshold may need adjustment)

### Requirement 10: Frequency-Based Re-Accumulation

**User Story:** As Richard, I want Monthly and Quarterly content tasks to automatically re-enter the accumulation cycle after being published, so that living documents get refreshed when enough new context accumulates — without me prompting for it.

#### Acceptance Criteria

1. WHEN a content task with Frequency_RW = Monthly reaches Pipeline_RW = Published, THE system SHALL record `last_published_at` in `wiki.content_tasks`
2. WHEN `now() - last_published_at` exceeds the frequency interval (7d for Weekly, 30d for Monthly, 90d for Quarterly), THE system SHALL reset the task's Pipeline_RW to Idea and readiness_score to 0
3. WHEN a recurring task re-enters Idea, THE Readiness Scorer SHALL only count evidence with `created_at > last_published_at` — prior-cycle evidence is excluded from scoring but retained in the ledger for audit
4. WHEN a content task has Frequency_RW = One-time, THE system SHALL NOT reset Pipeline_RW after publishing — the task stays at Published permanently
5. THE frequency reset check SHALL run during AM-Backend, before the signal matching phase
