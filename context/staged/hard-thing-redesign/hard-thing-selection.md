<!-- DOC-STAGED | duck_id: protocol-hard-thing-selection -->
# Hard Thing Selection Protocol

Signal-driven bottom-up selection for the aMCC's single hard thing. Replaces the task-queue top-down model. Produces `ps_analytics.main.hard_thing_candidates` with the top 3 candidates and incumbent advantage for stickiness.

**Status:** Staged for Richard's review. Do not run against production until approved. See `~/shared/context/staged/hard-thing-redesign/README.md`.

---

## Core concept

The hard thing is the gap between where signals are converging and where Richard has produced referenceable output. A topic qualifies under one of two modes:

- **Valuable-and-avoided:** high cross-channel signal density + zero referenceable artifact.
- **Valuable-and-latent:** signal density building + no one has named it as a priority yet.

The scoring function ranks all candidate topics. The top 3 are surfaced. The #1 slot is the hard thing. Stickiness prevents the list from flipping on daily noise.

---

## Parameters

All tunable. Defaults are the starting math from Richard's 2026-04-20 decision. Tuning lives in the autoresearch experiment queue.

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `window_days` | 7 | Rolling window for signals. Beyond this the frame crystallizes. Decay continues but weight is negligible. |
| `half_life_days` | 3.5 | Exponential decay half-life. At day 7 a signal is ~25% of original weight. |
| `incumbent_margin` | 1.15 | Challenger must score > incumbent × 1.15 to displace at rank 3. |
| `min_score` | 2.0 | Floor for a topic to qualify at all. Below this = null state. |
| `min_channel_spread` | 2 | Minimum distinct channels (of slack/email/hedy/asana). Single-channel chatter doesn't qualify. |
| `min_unique_authors` | 2 | At least 2 distinct non-Richard authors. Filters out Richard-only topics. |
| `stuck_days` | 7 | If `incumbent_since > stuck_days` without an artifact, escalate to rw-trainer. |

---

## Scoring function

```
signal_weight(t) = base_weight × 0.5 ^ (age_days / half_life_days)
topic_score      = Σ signal_weight across channels
                   × impact_multiplier
                   ÷ (1 + action_recency_penalty)
```

**`base_weight`** — per-signal weight from the channel that raised it (already set by the signal-intelligence protocol):
- Slack: 0.5
- Email: 1.0
- Asana task/comment: 0.75
- Hedy meeting: 1.0

These are inherited from `signals.signal_tracker` — do not re-weight here.

**`impact_multiplier`** — Five Levels mapping. Topics get classified against `brain.md → Strategic Priorities`:

| Level | Multiplier | Examples of topics that map here |
|-------|-----------|----------------------------------|
| L1 Sharpen Yourself | 1.0 | Personal artifact habits, weekly shipping discipline |
| L2 Drive WW Testing | 1.25 | Testing Approach, test design, OCI rollout, market test status |
| L3 Team Automation | 1.5 | Tools teammates adopt, callout pipeline, Slack digest |
| L4 Zero-Click Future | 1.75 | AEO/AI Overviews POV, brand LP strategy, zero-click narrative |
| L5 Agentic Orchestration | 2.0 | Agent swarm workflows, autonomous PS operations |

Default multiplier for unclassified topics: 1.25 (L2). Classification is stored alongside the candidate; the agent re-evaluates on major topic re-naming.

**`action_recency_penalty`** — inverse of days since Richard's last referenceable artifact on this topic, clamped to [0, 14]. It's `14 - days_since_artifact` with a floor of 0. Purpose: suppress a topic Richard just shipped on so it drops off the top 3.

- Shipped today (0 days ago) → penalty 14, score divides by 15
- Shipped 7 days ago → penalty 7, score divides by 8
- Shipped 14+ days ago or never → penalty 0, score divides by 1 (full weight)

Net effect: a freshly-shipped topic is suppressed for about two weeks, then returns to full weight as signals either keep building or decay.

---

## The scoring join

Runs against `ps_analytics`. Produces the top 3 with incumbent advantage applied.

**Note on CTE shape:** DuckDB rejects lateral joins against a CTE in `FROM x, params` form (raises `Non-inner join on correlated columns not supported`). The protocol reads parameters via scalar subqueries instead — `(SELECT half_life_days FROM p)` etc. This was validated against live `signal_tracker` on 2026-04-20.

```sql
WITH p AS (
  SELECT
    3.5::DOUBLE AS half_life_days,
    7::INTEGER AS window_days,
    1.15::DOUBLE AS incumbent_margin,
    2.0::DOUBLE AS min_score,
    2::INTEGER AS min_channel_spread,
    2::INTEGER AS min_unique_authors
),

-- 1. Signals in the rolling window, exponentially decayed to "now"
decayed_signals AS (
  SELECT
    st.topic,
    st.source_channel,
    st.source_author,
    st.signal_strength * POWER(
      0.5,
      DATE_DIFF('hour', st.last_seen, CURRENT_TIMESTAMP)::DOUBLE / 24.0 / (SELECT half_life_days FROM p)
    ) AS decayed_weight,
    st.last_seen
  FROM ps_analytics.signals.signal_tracker st
  WHERE st.is_active = true
    AND st.last_seen >= CURRENT_TIMESTAMP - ((SELECT window_days FROM p)::VARCHAR || ' days')::INTERVAL
),

-- 2. Aggregate per topic across channels
topic_agg AS (
  SELECT
    topic,
    SUM(decayed_weight) AS raw_score,
    COUNT(DISTINCT source_channel) AS channel_spread,
    COUNT(DISTINCT source_author) FILTER (WHERE source_author != 'Richard Williams') AS unique_non_richard_authors,
    COUNT(*) AS signal_count,
    MAX(last_seen) AS most_recent,
    LIST(DISTINCT source_channel) AS channels,
    LIST(DISTINCT source_author) AS authors
  FROM decayed_signals
  GROUP BY topic
),

-- 3. Impact multiplier from topic-to-level mapping (seeded table)
topic_levels AS (
  SELECT topic, level_num, impact_multiplier
  FROM ps_analytics.main.hard_thing_topic_levels
),

-- 4. Last referenceable artifact per topic
richard_artifacts AS (
  SELECT
    topic,
    MAX(artifact_date) AS last_artifact_date,
    DATE_DIFF('day', MAX(artifact_date), CURRENT_DATE) AS days_since_artifact
  FROM ps_analytics.main.hard_thing_artifact_log
  GROUP BY topic
),

-- 5. Compose the final score
scored AS (
  SELECT
    t.topic,
    COALESCE(tl.level_num, 2) AS level_num,
    COALESCE(tl.impact_multiplier, 1.25) AS impact_multiplier,
    t.raw_score,
    t.channel_spread,
    t.unique_non_richard_authors,
    t.signal_count,
    t.most_recent,
    t.channels,
    t.authors,
    COALESCE(ra.days_since_artifact, 999) AS days_since_artifact,
    -- action_recency_penalty: suppresses topics Richard just shipped on.
    -- Inverse scale: days_since = 0 → penalty = 14 (max suppression);
    -- days_since >= 14 → penalty = 0 (no suppression).
    GREATEST(0, 14 - LEAST(14, COALESCE(ra.days_since_artifact, 14))) AS recency_penalty,
    -- score = raw × impact ÷ (1 + recency_penalty)
    (t.raw_score * COALESCE(tl.impact_multiplier, 1.25))
      / (1 + GREATEST(0, 14 - LEAST(14, COALESCE(ra.days_since_artifact, 14))))
      AS score,
    -- Mode classification
    CASE
      WHEN COALESCE(ra.days_since_artifact, 999) > 14 AND t.unique_non_richard_authors >= 2
        THEN 'valuable-and-avoided'
      WHEN ra.days_since_artifact IS NULL AND t.signal_count >= 3
        THEN 'valuable-and-latent'
      ELSE 'other'
    END AS mode
  FROM topic_agg t
  LEFT JOIN topic_levels tl ON tl.topic = t.topic
  LEFT JOIN richard_artifacts ra ON ra.topic = t.topic
  WHERE t.raw_score >= (SELECT min_score FROM p)
    AND t.channel_spread >= (SELECT min_channel_spread FROM p)
    AND t.unique_non_richard_authors >= (SELECT min_unique_authors FROM p)
),

-- 6. Apply incumbent advantage to the displacement candidate
ranked AS (
  SELECT *,
         ROW_NUMBER() OVER (ORDER BY score DESC) AS proposed_rank
  FROM scored
),
with_stickiness AS (
  SELECT
    r.*,
    LAG(score) OVER (ORDER BY score DESC) AS next_higher_score,
    LEAD(score) OVER (ORDER BY score DESC) AS next_lower_score
  FROM ranked r
)

SELECT
  proposed_rank AS rank,
  topic,
  ROUND(score, 3) AS score,
  mode,
  level_num,
  channel_spread,
  unique_non_richard_authors,
  signal_count,
  days_since_artifact,
  most_recent,
  channels,
  authors
FROM with_stickiness
WHERE proposed_rank <= 3
ORDER BY proposed_rank;
```

---

## Incumbent advantage (stickiness) step

The scoring join produces a proposed ranking. Incumbent advantage is applied as a second pass against the previous snapshot. Implemented in the refresh job, not in the SQL above:

```sql
-- Get the previous snapshot
WITH previous AS (
  SELECT rank, topic, score, incumbent_since
  FROM ps_analytics.main.hard_thing_candidates
  WHERE snapshot_at = (SELECT MAX(snapshot_at) FROM ps_analytics.main.hard_thing_candidates)
),
proposed AS (
  -- Result from the scoring join above, aliased as 'proposed'
  SELECT * FROM <scoring_query_result>
),

-- For each incumbent in previous top-3, check if the challenger beats them by the margin
stickiness_applied AS (
  SELECT
    pr.topic AS incumbent_topic,
    pr.rank AS incumbent_rank,
    pr.score AS incumbent_score,
    pp.topic AS challenger_topic,
    pp.score AS challenger_score,
    CASE
      WHEN pp.topic = pr.topic THEN 'hold'  -- same topic retained the slot
      WHEN pp.score > pr.score * 1.15 THEN 'displace'
      ELSE 'defend'  -- challenger doesn't clear the margin, incumbent holds
    END AS action
  FROM previous pr
  FULL OUTER JOIN proposed pp ON pp.rank = pr.rank
)
-- Apply the action: 'defend' keeps incumbent_topic at that rank with refreshed score.
-- 'displace' writes the challenger. 'hold' refreshes the incumbent's incumbent_since.
```

**Incumbent-since logic:**
- Same topic retained rank → `incumbent_since` unchanged.
- Topic newly at rank 1/2/3 → `incumbent_since = CURRENT_TIMESTAMP`.
- Topic falls out → row removed (rank > 3).

---

## Artifact detection

Feeds `ps_analytics.main.hard_thing_artifact_log`. Populated by the refresh job that scans across sources.

```sql
-- Schema
CREATE TABLE IF NOT EXISTS ps_analytics.main.hard_thing_artifact_log (
  topic VARCHAR NOT NULL,
  artifact_type VARCHAR NOT NULL,  -- asana, wiki, email, code, loop
  artifact_ref VARCHAR NOT NULL,   -- task_gid, article_slug, message_id, commit_sha, loop_id
  artifact_date DATE NOT NULL,
  non_richard_interaction_at TIMESTAMP,  -- NULL until someone else touches it
  detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (topic, artifact_type, artifact_ref)
);
```

**Detection rules** (run each on refresh, insert-or-update):

```sql
-- 1. Asana: completed tasks topic-matched to signal topics, with non-Richard story/interaction
INSERT INTO ps_analytics.main.hard_thing_artifact_log (topic, artifact_type, artifact_ref, artifact_date, non_richard_interaction_at)
SELECT
  tl.topic,
  'asana',
  at.task_gid,
  at.completed_at::DATE,
  al.timestamp AS non_richard_interaction_at
FROM ps_analytics.asana.asana_tasks at
JOIN ps_analytics.main.hard_thing_topic_levels tl ON LOWER(at.name) LIKE '%' || REPLACE(tl.topic, '-', ' ') || '%'
LEFT JOIN ps_analytics.asana.asana_audit_log al
  ON al.task_gid = at.task_gid
  AND al.pipeline_agent NOT IN ('richard-manual')
  AND al.timestamp > at.completed_at
WHERE at.completed = true
  AND at.completed_at >= CURRENT_TIMESTAMP - INTERVAL '30 days'
ON CONFLICT (topic, artifact_type, artifact_ref) DO UPDATE SET
  non_richard_interaction_at = COALESCE(EXCLUDED.non_richard_interaction_at, ps_analytics.main.hard_thing_artifact_log.non_richard_interaction_at);

-- 2. Wiki: published articles matched to topic
-- (Requires wiki.publication_registry — add once wiki pipeline is connected)

-- 3. Email: Richard-authored sent messages whose subject/body matches the topic
-- (Requires signals.emails with sender_alias = 'prichwil' AND recipient IS NOT Richard)

-- 4. Code: commits referencing the topic in message or diff path

-- 5. Loop: document last_editor = Richard AND shared_with_count > 0
```

Only rows where `non_richard_interaction_at IS NOT NULL` count toward `days_since_artifact`. That's what "referenceable by another person or agent" operationalizes to.

---

## Topic-to-level seed mapping

Seed table. Hand-curated to start; updatable as new canonical topics appear in the signal-intelligence registry.

```sql
CREATE TABLE IF NOT EXISTS ps_analytics.main.hard_thing_topic_levels (
  topic VARCHAR PRIMARY KEY,
  level_num INTEGER NOT NULL,          -- 1..5
  impact_multiplier DOUBLE NOT NULL,    -- 1.0, 1.25, 1.5, 1.75, 2.0
  rationale VARCHAR,
  last_reviewed DATE DEFAULT CURRENT_DATE
);

-- Seed from canonical-slug registry in signal-intelligence.md
INSERT INTO ps_analytics.main.hard_thing_topic_levels VALUES
  ('polaris-brand-lp',         4, 1.75, 'Brand LP consolidation is an L4 narrative — AEO-adjacent, cross-team visibility, Brandon-driven', CURRENT_DATE),
  ('oci-rollout',              2, 1.25, 'WW testing execution — operational L2 work', CURRENT_DATE),
  ('au-cpa-cvr',               2, 1.25, 'AU market performance — hands-on L2', CURRENT_DATE),
  ('mx-budget-ieccp',          2, 1.25, 'MX market execution — hands-on L2', CURRENT_DATE),
  ('liveramp-enhanced-match',  4, 1.75, 'Audience + identity — L4 strategic territory', CURRENT_DATE),
  ('f90-lifecycle',            4, 1.75, 'Audience strategy — L4', CURRENT_DATE),
  ('ai-search-aeo',            4, 1.75, 'Zero-click future POV — core L4 artifact', CURRENT_DATE),
  ('op1-strategy',             2, 1.25, 'OP1 planning — L2 testing narrative input', CURRENT_DATE),
  ('deep-linking-ref-tags',    3, 1.5,  'Instrumentation / tooling for team', CURRENT_DATE),
  ('pam-budget',               2, 1.25, 'Paid App budget management — L2 execution', CURRENT_DATE)
ON CONFLICT (topic) DO UPDATE SET
  level_num = EXCLUDED.level_num,
  impact_multiplier = EXCLUDED.impact_multiplier,
  rationale = EXCLUDED.rationale,
  last_reviewed = EXCLUDED.last_reviewed;
```

New topics without a mapping get `level_num = 2, impact_multiplier = 1.25` by default and surface to Richard for classification on their first appearance in the top 3.

---

## Refresh cadence

**Continuous, not batched.** Triggers:

| Trigger | Location | What runs |
|---------|----------|-----------|
| Signal-tracker write | Signal-intelligence protocol, end of AM-1 and end of signal reinforcement | Re-run the scoring join, apply stickiness, write snapshot |
| AM-Backend | Morning hook | Full refresh + surface top-3 in daily brief |
| Artifact detected | After any write to `hard_thing_artifact_log` | Re-run scoring for that topic only (incremental) |
| Manual | `refresh_hard_thing_candidates()` stored procedure | Full refresh on demand |

**Throttle:** one full refresh per 15 minutes maximum. Back-to-back signal writes within the window only log and skip.

---

## Null state

If the scoring query returns zero rows after filters, write a null-state snapshot:

```sql
INSERT INTO ps_analytics.main.hard_thing_candidates
  (snapshot_at, rank, topic, score, mode, level_num, channel_spread, unique_non_richard_authors,
   signal_count, days_since_artifact, most_recent, channels, authors, incumbent_since, null_state)
VALUES
  (CURRENT_TIMESTAMP, NULL, NULL, NULL, 'null-state', NULL, NULL, NULL,
   NULL, NULL, NULL, NULL, NULL, NULL, TRUE);
```

Agent reads this as "no hard thing currently — signals flat." Intervention layer stays quiet. Streak logs a neutral day.

---

## Integration points

| Hook/Organ | How it reads the candidates |
|------------|----------------------------|
| AM-Backend | Queries `WHERE snapshot_at = (SELECT MAX(snapshot_at) FROM hard_thing_candidates)`. Surfaces rank 1 as the hard thing. Lists ranks 2-3 as context. |
| aMCC intervention layer | On session start, loads the top-3 before deciding whether to fire an avoidance trigger. |
| rw-trainer | Escalation target when `incumbent_since > 7 days` with no artifact produced. |
| Daily brief | Includes the hard thing with its mode and `days_since_artifact`. |
| `main.l1_streak` | Writes rank-1 topic to `hard_thing_name` and (where available) `hard_thing_task_gid`. Replaces manual entry. Null-state days write `hard_thing_name = 'null-state'`. |
| Ambient surface | Optional: small line item in the session-start agent voice. "Today's hard thing: [topic]. [Mode]. No referenceable artifact in [N] days." |

---

## Common failures to watch for

1. **Topic fragmentation.** Slack uses display names, Hedy uses slugs. If the same topic scores low because it's split across two slugs, the candidate never makes the top 3. Mitigation: the canonical-slug registry in `signal-intelligence.md` must be maintained.
2. **Richard-only echo.** A topic where Richard is the only author shouldn't qualify — that's Richard talking to himself. The `unique_non_richard_authors >= 2` filter catches this.
3. **Level miscoding.** An L3 tool topic coded as L1 will under-rank relative to its strategic weight. Review `hard_thing_topic_levels` quarterly.
4. **Artifact detection too loose.** If a comment on a ticket counts as "referenceable," the completion threshold becomes meaningless. Require `non_richard_interaction_at IS NOT NULL` before counting.
5. **Stickiness infinite loop.** If a topic holds #1 for 30 days without an artifact, the system is enabling avoidance, not overcoming it. The 7-day escalation to rw-trainer is the release valve.
