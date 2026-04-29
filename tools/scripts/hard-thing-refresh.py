#!/usr/bin/env python3
"""
hard-thing-refresh.py — compute top 3 hard-thing candidates from signal density.

Executes the scoring join defined in ~/shared/context/protocols/hard-thing-selection.md,
applies incumbent advantage for stickiness, and writes a snapshot to
main.hard_thing_candidates.

Exit codes:
  0  — refresh succeeded (top-3 or null-state written)
  1  — throttled (skip; last snapshot was within throttle window)
  2  — MotherDuck token missing; null-state written; flagged
  3  — hard error

Usage:
  python3 ~/shared/tools/scripts/hard-thing-refresh.py              # default 15-min throttle
  python3 ~/shared/tools/scripts/hard-thing-refresh.py --force      # ignore throttle
  python3 ~/shared/tools/scripts/hard-thing-refresh.py --dry-run    # compute but don't write
  python3 ~/shared/tools/scripts/hard-thing-refresh.py --local      # use local slack tables (degraded; for dev only)

See protocol doc: ~/shared/context/protocols/hard-thing-selection.md
"""

import argparse
import datetime as dt
import os
import sys

import duckdb

LOCAL_DB = "/home/prichwil/shared/data/duckdb/ps-analytics.duckdb"

# DDL for the three tables the refresh procedure reads/writes.
# Idempotent — safe to run on every invocation. Karpathy verdict 2026-04-21:
# script previously assumed these tables existed; first run would hard-error.
ENSURE_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS main.hard_thing_candidates (
  snapshot_at TIMESTAMP NOT NULL,
  rank INTEGER,
  topic VARCHAR,
  score DOUBLE,
  mode VARCHAR,
  level_num INTEGER,
  impact_multiplier DOUBLE,
  channel_spread INTEGER,
  unique_non_richard_authors INTEGER,
  signal_count INTEGER,
  days_since_artifact INTEGER,
  most_recent TIMESTAMP,
  channels VARCHAR[],
  authors VARCHAR[],
  incumbent_since TIMESTAMP,
  challenger_margin DOUBLE,
  null_state BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_hard_thing_candidates_latest
  ON main.hard_thing_candidates (snapshot_at);
CREATE INDEX IF NOT EXISTS idx_hard_thing_candidates_topic
  ON main.hard_thing_candidates (topic);

CREATE TABLE IF NOT EXISTS main.hard_thing_topic_levels (
  topic VARCHAR PRIMARY KEY,
  level_num INTEGER NOT NULL,
  impact_multiplier DOUBLE NOT NULL,
  rationale VARCHAR,
  last_reviewed DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS main.hard_thing_artifact_log (
  topic VARCHAR NOT NULL,
  artifact_type VARCHAR NOT NULL,
  artifact_ref VARCHAR NOT NULL,
  artifact_date DATE NOT NULL,
  non_richard_interaction_at TIMESTAMP,
  detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (topic, artifact_type, artifact_ref)
);
"""

# Seed the topic-to-level mapping per hard-thing-selection.md.
# ON CONFLICT preserves any manual edits to rationale/last_reviewed made since seed.
INSERT INTO main.hard_thing_topic_levels (topic, level_num, impact_multiplier, rationale, last_reviewed) VALUES
  ('polaris-brand-lp',         4, 1.75, 'Brand LP consolidation is an L4 narrative — AEO-adjacent, cross-team visibility, Brandon-driven', CURRENT_DATE),
  ('au-cpa-cvr',               2, 1.25, 'AU market performance — hands-on L2', CURRENT_DATE),
  ('mx-budget-ieccp',          2, 1.25, 'MX market execution — hands-on L2', CURRENT_DATE),
  ('liveramp-enhanced-match',  4, 1.75, 'Audience + identity — L4 strategic territory', CURRENT_DATE),
  ('f90-lifecycle',            4, 1.75, 'Audience strategy — L4', CURRENT_DATE),
  ('ai-search-aeo',            4, 1.75, 'Zero-click future POV — core L4 artifact', CURRENT_DATE),
  ('pam-budget',               2, 1.25, 'Paid App budget management — L2 execution', CURRENT_DATE)
ON CONFLICT (topic) DO UPDATE SET
  impact_multiplier = EXCLUDED.impact_multiplier,
  rationale = EXCLUDED.rationale,
  last_reviewed = EXCLUDED.last_reviewed;
"""

SCORING_SQL = """
WITH decayed_signals AS (
    st.topic,
    st.source_channel,
    st.source_author,
    st.signal_strength * POWER(
      0.5,
      DATE_DIFF('hour', st.last_seen, CURRENT_TIMESTAMP)::DOUBLE / 24.0 / ?
    ) AS decayed_weight,
  FROM signals.signal_tracker st
  WHERE st.is_active = true
),
    topic,
    SUM(decayed_weight) AS raw_score,
    COUNT(DISTINCT source_author) FILTER (WHERE source_author != 'Richard Williams') AS unique_non_richard_authors,
    COUNT(*) AS signal_count,
    MAX(last_seen) AS most_recent,
    LIST(DISTINCT source_channel) AS channels,
),
richard_artifacts AS (
    topic,
    MAX(artifact_date) AS last_artifact_date,
    DATE_DIFF('day', MAX(artifact_date), CURRENT_DATE) AS days_since_artifact
  WHERE non_richard_interaction_at IS NOT NULL
  GROUP BY topic
),
    t.topic,
    COALESCE(tl.level_num, 2) AS level_num,
    COALESCE(tl.impact_multiplier, 1.25) AS impact_multiplier,
    t.raw_score,
    t.most_recent,
    t.authors,
    GREATEST(0, 14 - LEAST(14, COALESCE(ra.days_since_artifact, 14))) AS recency_penalty,
      / (1 + GREATEST(0, 14 - LEAST(14, COALESCE(ra.days_since_artifact, 14))))
      AS score,
      WHEN COALESCE(ra.days_since_artifact, 999) > 14 AND t.unique_non_richard_authors >= 2
        THEN 'valuable-and-avoided'
      WHEN ra.days_since_artifact IS NULL AND t.signal_count >= 3
        THEN 'valuable-and-latent'
    END AS mode
  FROM topic_agg t
  LEFT JOIN main.hard_thing_topic_levels tl ON tl.topic = t.topic
  LEFT JOIN richard_artifacts ra ON ra.topic = t.topic
  WHERE t.raw_score >= ?
    AND t.channel_spread >= ?
    AND t.unique_non_richard_authors >= ?
),
  SELECT *,
         ROW_NUMBER() OVER (ORDER BY score DESC) AS proposed_rank
  FROM scored
)
  proposed_rank AS rank,
  topic,
  level_num,
  impact_multiplier,
  unique_non_richard_authors,
  signal_count,
  most_recent,
  channels,
FROM ranked


# Defaults. Tunable via experiment queue.
DEFAULTS = {
    "half_life_days": 3.5,
    "window_days": 7,
    "incumbent_margin": 1.15,
    "min_score": 2.0,
    "min_channel_spread": 2,
    "min_unique_authors": 2,
    "throttle_minutes": 15,
}


def connect(use_local: bool = False) -> duckdb.DuckDBPyConnection:
    """Connect to MotherDuck if token present, else local shadow DB.

    Ensures the three hard_thing_* tables exist on every connection (idempotent).
    Seeds hard_thing_topic_levels on first run (ON CONFLICT preserves edits).
    """
    if use_local:
        con = duckdb.connect(LOCAL_DB)
    else:
        token = os.environ.get("motherduck_token") or os.environ.get("MOTHERDUCK_TOKEN")
        if not token:
            raise RuntimeError("MotherDuck token missing")
        con = duckdb.connect("md:ps_analytics")
    con.execute(ENSURE_SCHEMA_SQL)
    con.execute(SEED_TOPIC_LEVELS_SQL)
    return con


def throttled(con, window_minutes: int) -> bool:
    """True if last snapshot was within throttle window."""
    last = con.execute(
        "SELECT MAX(snapshot_at) FROM main.hard_thing_candidates"
    ).fetchone()[0]
    if last is None:
        return False
    age_seconds = (dt.datetime.now() - last).total_seconds()
    return age_seconds < window_minutes * 60


def run_scoring(con, params: dict) -> list:
    """Execute the scoring query and return rows (including the #4 contender)."""
    return con.execute(
        SCORING_SQL,
        [
            params["half_life_days"],
            params["window_days"],
            params["min_score"],
            params["min_channel_spread"],
            params["min_unique_authors"],
        ],
    ).fetchall()


def previous_top3(con) -> dict:
    """Map rank -> (topic, score, incumbent_since) from the latest non-null snapshot."""
    rows = con.execute(
        """
        SELECT rank, topic, score, incumbent_since
        FROM main.hard_thing_candidates
        WHERE snapshot_at = (
            SELECT MAX(snapshot_at) FROM main.hard_thing_candidates
            WHERE null_state = FALSE
        )
          AND rank IS NOT NULL
        ORDER BY rank
        """
    ).fetchall()
    return {r[0]: {"topic": r[1], "score": r[2], "incumbent_since": r[3]} for r in rows}


def apply_stickiness(
    proposed: list, previous: dict, margin: float, now: dt.datetime
) -> list:
    """
    Apply incumbent advantage. Returns final top-3 with incumbent_since stamped.

    Rule: at each rank, if previous incumbent at that rank is in the proposed list,
    the challenger must beat the incumbent's previous score by `margin` to displace.
    Otherwise the incumbent holds (refreshed score) and the challenger drops one rank.

    Simple implementation: rank-by-rank. Only #3 -> #4 displacement is subject to the
    margin check in the default case, since #1 and #2 are usually the same topics
    holding their slots. The edge case where a topic is new at rank 1 is rare and
    doesn't need stickiness protection (it's earning its way in with high score).
    """
    # Topic -> proposed row map for convenience
    proposed_by_topic = {r[1]: r for r in proposed}  # r[1] is topic
    prev_topics_at_rank = {
        rank: prev["topic"] for rank, prev in previous.items()
    }

    # Start with top-3 from proposed
    final = []
    for r in proposed[:3]:
        final.append(list(r))

    # Check if there was a previous #3 that got displaced by this round's #4
    prev_rank3 = previous.get(3)
    if prev_rank3 and len(proposed) >= 4:
        prev_rank3_topic = prev_rank3["topic"]
        prev_rank3_score = prev_rank3["score"]
        current_rank3 = proposed[2]  # rank 3 in proposed
        # If proposed #3 is DIFFERENT from previous #3, check if the previous incumbent
        # is still in the proposed list (at rank 4+) and whether challenger beat margin
        if current_rank3[1] != prev_rank3_topic:
            challenger_score = current_rank3[2]
            if challenger_score <= prev_rank3_score * margin:
                # Challenger didn't clear margin — incumbent holds at rank 3
                # Find the incumbent's current score in proposed
                incumbent_row = proposed_by_topic.get(prev_rank3_topic)
                if incumbent_row:
                    # Swap incumbent in at rank 3, demote challenger
                    final[2] = list(incumbent_row)
                    final[2][0] = 3  # rank
                # else: incumbent fell out entirely — just accept the challenger

    # Stamp incumbent_since
    stamped = []
    for r in final:
        rank, topic = r[0], r[1]
        prev_topic_at_rank = prev_topics_at_rank.get(rank)
        if prev_topic_at_rank == topic:
            # Same topic held this rank — preserve incumbent_since
            incumbent_since = previous[rank]["incumbent_since"]
        else:
            # New to this rank — stamp now
            incumbent_since = now
        stamped.append(tuple(r) + (incumbent_since,))
    return stamped


def write_snapshot(con, rows: list, now: dt.datetime) -> None:
    """Write top-3 rows to hard_thing_candidates."""
    if not rows:
        con.execute(
            """
            INSERT INTO main.hard_thing_candidates
              (snapshot_at, rank, topic, score, mode, null_state)
            VALUES (?, NULL, NULL, NULL, 'null-state', TRUE)
            """,
            [now],
        )
        return
    for r in rows:
        # r = (rank, topic, score, mode, level_num, impact_multiplier,
        #      channel_spread, unique_non_richard_authors, signal_count,
        #      days_since_artifact, most_recent, channels, authors, incumbent_since)
        con.execute(
            """
            INSERT INTO main.hard_thing_candidates
              (snapshot_at, rank, topic, score, mode, level_num, impact_multiplier,
               channel_spread, unique_non_richard_authors, signal_count,
               days_since_artifact, most_recent, channels, authors,
               incumbent_since, challenger_margin, null_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, FALSE)
            """,
            [now] + list(r),
        )


def refresh(force: bool = False, dry_run: bool = False, use_local: bool = False) -> int:
    """Main entry point. Returns exit code."""
    # --local can't produce real scoring (signals.signal_tracker is MotherDuck-only).
    # Short-circuit to null-state with explicit reason.
    if use_local:
        fallback = duckdb.connect(LOCAL_DB)
        now = dt.datetime.now()
        if not force and throttled(fallback, DEFAULTS["throttle_minutes"]):
            fallback.close()
            return 1
        if not dry_run:
            fallback.execute(
                """
                INSERT INTO main.hard_thing_candidates
                  (snapshot_at, rank, topic, score, mode, null_state)
                VALUES (?, NULL, NULL, NULL,
                        'null-state-local-mode-no-signals-schema', TRUE)
                """,
                [now],
            )
        fallback.close()
        print(
            f"[{now.isoformat()}] --local mode: signals schema not available locally; "
            "null-state written. Run without --local (MotherDuck) for real scoring.",
            file=sys.stderr,
        )
        return 2

    # Try to connect to MotherDuck
    try:
        con = connect(use_local=False)
    except RuntimeError as e:
        # MotherDuck token missing — write null-state to local fallback
        if "token missing" in str(e):
            fallback = duckdb.connect(LOCAL_DB)
            now = dt.datetime.now()
            fallback.execute(
                """
                INSERT INTO main.hard_thing_candidates
                  (snapshot_at, rank, topic, score, mode, null_state)
                VALUES (?, NULL, NULL, NULL,
                        'null-state-motherduck-token-missing', TRUE)
                """,
                [now],
            )
            fallback.close()
            print(
                f"[{now.isoformat()}] motherduck_token missing — null-state written to local shadow",
                file=sys.stderr,
            )
            return 2
        raise

    try:
        if not force and throttled(con, DEFAULTS["throttle_minutes"]):
            return 1

        proposed = run_scoring(con, DEFAULTS)
        previous = previous_top3(con)
        now = dt.datetime.now()
        final = apply_stickiness(
            proposed, previous, DEFAULTS["incumbent_margin"], now
        )

        if dry_run:
            print(f"[DRY-RUN] {len(final)} rows would be written at {now.isoformat()}")
            for r in final:
                print(f"  rank={r[0]} topic={r[1]} score={r[2]:.3f} mode={r[3]}")
            return 0

        write_snapshot(con, final, now)

        if final:
            print(f"[{now.isoformat()}] top-3 refreshed")
            for r in final:
                print(f"  #{r[0]} {r[1]} (score {r[2]:.3f}, {r[3]})")
        else:
            print(f"[{now.isoformat()}] null-state (no topics cleared filters)")
        return 0
    finally:
        con.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="ignore throttle")
    parser.add_argument("--dry-run", action="store_true", help="compute but don't write")
    parser.add_argument(
        "--local",
        action="store_true",
        help="use local shadow DB (degraded; signals schema missing)",
    )
    args = parser.parse_args()
    return refresh(force=args.force, dry_run=args.dry_run, use_local=args.local)


if __name__ == "__main__":
    sys.exit(main())
