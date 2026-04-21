# Implementation Plan — Hard-Thing Selection Redesign

Companion to `amcc-patch.md` and `hard-thing-selection.md`. Describes the tables, triggers, surfaces, and first experiment needed to make the signal-driven model live.

---

## 1. Tables to create

Three new objects in `ps_analytics.main`. All DDL is reversible — a rollback drops these and reverts the amcc.md section to its pre-patch form.

### 1.1 `main.hard_thing_candidates` (snapshot history)

```sql
CREATE TABLE IF NOT EXISTS ps_analytics.main.hard_thing_candidates (
  snapshot_at                 TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  rank                        INTEGER,                -- 1..3, NULL for null-state row
  topic                       VARCHAR,
  score                       DOUBLE,
  mode                        VARCHAR,                -- 'valuable-and-avoided' | 'valuable-and-latent' | 'other' | 'null-state'
  level_num                   INTEGER,
  impact_multiplier           DOUBLE,
  channel_spread              INTEGER,
  unique_non_richard_authors  INTEGER,
  signal_count                INTEGER,
  days_since_artifact         INTEGER,
  most_recent                 TIMESTAMP,
  channels                    VARCHAR[],
  authors                     VARCHAR[],
  incumbent_since             TIMESTAMP,              -- when this topic first held this rank
  challenger_margin           DOUBLE,                 -- how much the #4 contender trailed rank-3 (for observability)
  null_state                  BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (snapshot_at, rank)
);

CREATE INDEX IF NOT EXISTS idx_hard_thing_candidates_topic ON ps_analytics.main.hard_thing_candidates (topic, snapshot_at);
CREATE INDEX IF NOT EXISTS idx_hard_thing_candidates_latest ON ps_analytics.main.hard_thing_candidates (snapshot_at DESC);
```

**Retention:** keep 90 days of snapshots for trend analysis. Older rows get pruned by the state-file-engine nightly job.

**Current view (the one the agent reads):**

```sql
CREATE OR REPLACE VIEW ps_analytics.main.hard_thing_now AS
SELECT *
FROM ps_analytics.main.hard_thing_candidates
WHERE snapshot_at = (SELECT MAX(snapshot_at) FROM ps_analytics.main.hard_thing_candidates)
ORDER BY rank NULLS LAST;
```

### 1.2 `main.hard_thing_topic_levels` (seed mapping)

See the DDL + seed inserts in `hard-thing-selection.md` §"Topic-to-level seed mapping".

### 1.3 `main.hard_thing_artifact_log` (completion detection)

See the DDL in `hard-thing-selection.md` §"Artifact detection".

---

## 2. Refresh trigger wiring

### 2.1 AM-Backend (morning)

Add to the AM-Backend protocol (`protocols/am-backend.md`), Phase 2 or 3 (after signal ingestion):

```
Step: Refresh hard-thing candidates
1. Run refresh_hard_thing_candidates() against ps_analytics.
2. Read main.hard_thing_now.
3. If rank-1 row: surface in daily brief as "The hard thing: [topic] ([mode], [N] days since artifact)."
4. If null_state: surface as "No hard thing currently — signals flat. Consider L3 tooling, delegation review, or rest."
5. If incumbent_since > 7 days: add a note "Escalation candidate for rw-trainer."
```

### 2.2 After signal write

Add to `signal-intelligence.md` Use Case 1, at the end of the reinforcement step:

```
After UPDATE/INSERT to signal_tracker and decay step, call refresh_hard_thing_candidates() with a 15-minute throttle.
```

### 2.3 Stored procedure skeleton

Implement as a Python task in the state-file-engine or as a DuckDB macro. Sketch:

```python
def refresh_hard_thing_candidates(conn, throttle_minutes=15):
    # 1. Check throttle — skip if last snapshot < throttle_minutes ago
    last = conn.execute("SELECT MAX(snapshot_at) FROM ps_analytics.main.hard_thing_candidates").fetchone()[0]
    if last and (datetime.now() - last).total_seconds() < throttle_minutes * 60:
        return "throttled"

    # 2. Run the scoring join (see hard-thing-selection.md §"The scoring join")
    proposed = conn.execute(SCORING_SQL).fetchdf()

    # 3. Read previous top-3 for incumbent advantage
    previous = conn.execute("SELECT rank, topic, score, incumbent_since FROM ps_analytics.main.hard_thing_now WHERE rank IS NOT NULL").fetchdf()

    # 4. Apply stickiness per hard-thing-selection.md §"Incumbent advantage"
    final = apply_stickiness(proposed, previous, margin=1.15)

    # 5. Write snapshot
    if final.empty:
        conn.execute("INSERT INTO ps_analytics.main.hard_thing_candidates (snapshot_at, mode, null_state) VALUES (CURRENT_TIMESTAMP, 'null-state', TRUE)")
    else:
        conn.executemany("INSERT INTO ps_analytics.main.hard_thing_candidates (...) VALUES (...)", final.to_records())

    return "refreshed"
```

Lives in `~/shared/hooks/hard-thing-refresh.py`. Wired via the same orchestration that runs state-file-engine.

### 2.4 Refresh on artifact detection

Separate job, runs after each detection scan (incremental, topic-scoped):

- Runs at end of AM-Backend artifact-scan phase.
- Runs at end of any EOD sync that touches Asana, wiki, or email.
- Topic-scoped refresh recomputes only the rows for that topic.

---

## 3. Where the top 3 surfaces

Three placements, ranked by invisibility (most preferred first, per soul.md principle #5).

### 3.1 AM daily brief (PRIMARY — invisible-structural)

The morning brief already lands in Richard's mailbox. The hard thing gets one line at the top:

```
🔨 The hard thing: polaris-brand-lp (valuable-and-avoided, 12 days since referenceable artifact).
   Brandon + Alex + Dwayne talking about it across 4 channels. No sent email, no published doc, no merged artifact on this topic from you.
```

That's it. No menu. No justification. One line.

If null state:
```
🔨 No hard thing today. Signals flat. Good day for L3 tooling or delegation cleanup.
```

### 3.2 aMCC session-start read (SECONDARY — invisible-structural)

Every agent session starts by reading amcc.md. The amcc.md "The Hard Thing" section points to `main.hard_thing_now`. The agent queries it before responding to Richard's first prompt. No UI change — the agent just has the answer loaded when Richard asks "what should I work on?"

### 3.3 Ambient during Loop 1 retrospective (OPTIONAL — visible-structural)

Weekly retrospective: "This week's top-1 hard thing history" — show how rank-1 held or shifted across the 7 days. Useful for the streak analysis and for tuning the half-life. Only read during retro, not during work.

### Not recommended

- **A dashboard page.** Adds visual surface, violates "invisible over visible." The dashboard is where dead tabs live.
- **A Slack ping on every rank change.** Notification fatigue. The incumbent margin already suppresses churn — don't undo that with pings.
- **An Asana task per candidate.** Reinstates the top-down queue the redesign is eliminating.

---

## 4. Subtractions (per soul.md principle #3)

Net change is reduction, not addition. What goes away:

| Removed | Why |
|---------|-----|
| `amcc.md → ### Current Hard Thing` table | Replaced by `main.hard_thing_now` view reference |
| `amcc.md → ### Hard Thing History` subsection | Already "removed — current-state-only principle." Redundant now. |
| Manual weekly "what's the hard thing?" decisions in 1:1 prep | System names it. Decision cost drops to zero. |
| AU CPC-style fire-drill manufacturing | Can't happen — signal density has to exist first. |
| Testing Approach / AEO POV in hard-thing slot | They're not in the top 3 under the live scoring. The redesign retires them naturally. |

What gets added:

| Added | Justification |
|-------|--------------|
| 3 tables (candidates, topic_levels, artifact_log) | Necessary to make the selection structural, not cosmetic |
| One refresh procedure | Single function replaces manual hard-thing rotation |
| One line in the AM brief | Net reduction: old brief had 3-item "hard thing options" block, new brief has 1 line |

Net: one new view reference in amcc.md, three new tables, one refresh procedure, one removed table + two removed subsections. System trends simpler.

---

## 5. Rollback

If the redesign misbehaves:

1. `DROP TABLE ps_analytics.main.hard_thing_candidates;` (and `topic_levels`, `artifact_log`).
2. Revert `body/amcc.md` to the pre-patch version from git/changelog.
3. Remove the AM-Backend refresh step.
4. Restore the manual "Current Hard Thing" table from the changelog entry.

No production data is destroyed — signal_tracker is untouched, asana_tasks is untouched, l1_streak is untouched.

---

## 6. First experiment proposal

**Experiment ID:** `amcc-halflife-v1`
**Filed against:** `ps_analytics.main.autoresearch_experiments`
**Owner:** karpathy (experiment queue owner per soul.md routing)
**Duration:** 14 days of signal data (two 7-day windows).

### Hypothesis

The default `half_life_days = 3.5` (half of the 7-day window) is the right decay rate. Lower values (2.0) will make the system twitchy and surface same-day noise as hard things. Higher values (7.0) will smooth the signal so much that yesterday's topic still dominates after a week.

### Method

Compute rank-1 and rank-3 candidates daily at three half-lives: `2.0`, `3.5`, `7.0`. Record all three in a side table `main.hard_thing_halflife_eval`. Do not change the live top-3 while the experiment runs — this is a shadow evaluation.

### Metrics

1. **Top-1 churn rate** — how often does rank 1 flip from one day to the next? Lower = more stable. Target: 1-2 flips per 7-day window.
2. **Valuable-and-avoided hit rate** — of topics that surface as rank-1, how many produce a Richard artifact within 7 days of landing there? Target: > 50%. If half-life is wrong, either nothing moves (too sticky) or everything moves (too reactive).
3. **Null-state frequency** — how often does the system return "no hard thing"? Target: 10-20% of days. Zero = system manufacturing. >50% = filters too tight.
4. **Richard's blind-selection agreement** — once per week, ask Richard "without looking, what does the team keep pushing on that you haven't shipped?" Compare to rank-1 at each half-life. Agreement rate wins.

### Decision rule

After 14 days, pick the half-life with:
- Lowest top-1 churn AND
- Highest artifact hit rate AND
- Null-state within 10-20% range.

If 3.5 wins → keep default.
If 2.0 wins → system is under-weighting recency, tighten.
If 7.0 wins → system is over-weighting memory, loosen to 5.0 and re-run.

### Second experiment (queued)

`amcc-incumbent-margin-v1` — same method, test `incumbent_margin` at `1.10`, `1.15`, `1.25`. Start after the half-life experiment closes. Measures whether 15% stickiness under-holds or over-holds the #1 slot.

### Filing

```sql
INSERT INTO ps_analytics.main.autoresearch_experiments
  (run_id, organ, section, technique, eval_type, decision, created_at)
VALUES
  ('amcc-halflife-v1', 'amcc', 'hard-thing-selection', 'exponential-decay-tuning', 'shadow-evaluation', 'pending', CURRENT_TIMESTAMP);
```

---

## 7. Sign-off checklist (for Richard)

Before promoting:

- [ ] Read `amcc-patch.md` — confirm the "The Hard Thing" section replacement preserves what you care about in the old section and removes what you rejected.
- [ ] Read `hard-thing-selection.md` — confirm the two qualification modes and the scoring math match your mental model.
- [ ] Check today's live top-3 against "what does the team keep pushing on that I haven't shipped?" — run the scoring query in this file's §1.1 view (`SELECT * FROM ps_analytics.main.hard_thing_now;` after first refresh, or the raw query from the protocol).
- [ ] Confirm the L1-L5 impact multipliers feel right, or edit the seed mapping.
- [ ] Confirm the 7-day escalation to rw-trainer is right — or tighten to 5 / loosen to 10.
- [ ] Confirm the experiment proposal is worth running, or propose a different first tuning target.

Once approved, run the promotion checklist in `README.md`.

---

## 8. Portability note (per soul.md instruction #12)

Every piece of this survives a cold-start platform migration with text files only:

- `amcc-patch.md` is a section replacement — diff-able, human-readable.
- `hard-thing-selection.md` is executable SQL — any DuckDB or Postgres can run it with trivial syntax substitutions.
- Table DDL is standard SQL.
- The refresh procedure is documented in pseudocode and can be rewritten in any language against any scheduler.
- Seed mapping is a short INSERT script — re-seedable by hand if needed.

A new agent on a different platform with only `/home/prichwil/shared/context/` checked out could reconstitute the behavior. That's the test.
