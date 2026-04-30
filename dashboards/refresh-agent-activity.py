#!/usr/bin/env python3
"""refresh-agent-activity.py

Generates shared/dashboards/data/agent-activity-feed.json from LIVE sources:

    - main.autoresearch_experiments  — karpathy's blind-eval loop (primary)
    - main.workflow_executions       — scheduled workflows (hook pipelines)
    - main.hook_executions           — individual hook runs

The viewer (body-system/activity.html) reads this JSON and renders a
24-hour / 7-day / 30-day window. This generator emits the full 30-day
slice so the viewer's window filter has data to work with.

Why local DuckDB not MotherDuck:
    MotherDuck's ps_analytics has been frozen since 2026-04-17 per the
    sync audit flagged in session-log 2026-04-29. The local file at
    ~/shared/data/duckdb/ps-analytics.duckdb is the live copy. MCP agent
    tools hit MotherDuck by default, so using a local connection here
    bypasses the stale path.

Prior state (now replaced):
    data/agent-activity-feed.json was a hand-seeded demo file with
    source='demo-seed' and a frozen snapshot from 2026-04-21. The old
    file's cached stats block (total_24h=47) was a lie — it didn't match
    the activities array (12 rows spanning 2.7h). This generator writes
    stats derived directly from the activities so there's no drift.

Output schema:
    {
      "generated": ISO 8601 with PT offset,
      "source": "refresh-agent-activity.py",
      "stats": {
        "total_24h": int,
        "total_7d": int,
        "total_30d": int,
        "agents_active": int (distinct producers in last 7 days),
        "hooks_fired": int (last 7 days),
        "failures": int (last 7 days)
      },
      "activities": [
        {id, ts,
         producer_type: 'agent' | 'hook' | 'prompt' | 'system',
         producer: actor name (karpathy, hook-name, workflow-name, ...),
         subject: thing acted on (organ, trigger, side-effect target),
         subject_detail: optional finer slice (section name for karpathy),
         action, input_summary, output_summary,
         quality_gate, quality_score, duration_ms, downstream}, ...
      ]
    }

Producer vs subject — IMPORTANT:
    Producer = WHO/WHAT did the thing (karpathy, a specific hook, a workflow).
    Subject  = WHAT the thing was done to (brain.md, asana, duckdb).
    Prior versions conflated these by stuffing the subject (organ) into the
    producer field, which made producer_type filters useless (everything was
    'agent') and inflated agents_active to 310 (really 1 agent × 310 subjects).

Window: last 30 days, newest first. Viewer client-side filters to 1d/7d.

Run:
    python3 shared/dashboards/refresh-agent-activity.py
"""

from __future__ import annotations
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import duckdb
except ImportError:
    print("ERROR: duckdb not installed. Run: pip install duckdb", file=sys.stderr)
    sys.exit(1)

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------

DB_PATH = Path.home() / "shared" / "data" / "duckdb" / "ps-analytics.duckdb"
OUT_PATH = Path(__file__).resolve().parent / "data" / "agent-activity-feed.json"
WINDOW_DAYS = 30  # Generator window. Viewer filters down from this.

# PT offset at runtime. Naive; the DB stores naive UTC-ish TIMESTAMPs so we
# convert below. The viewer re-renders everything in PT via Intl anyway.
PT_OFFSET = "-07:00"  # Pacific Daylight Time; DST-aware would need pytz/zoneinfo.


# -----------------------------------------------------------------------------
# Mappers — translate each source's row shape to the activity feed shape
# -----------------------------------------------------------------------------

def _fmt_ts(ts) -> str:
    """Karpathy timestamps are stored as naive TIMESTAMP (local time).
    Emit as ISO 8601 with PT offset so the viewer's new Date() parses it
    correctly. If we later standardize the DB on UTC, revisit this."""
    if ts is None:
        return ""
    if hasattr(ts, 'isoformat'):
        return ts.isoformat() + PT_OFFSET
    return str(ts)


def _score(row) -> float | None:
    """Blended blind-eval score. score_a/score_b are the two raters.
    Return the lower of the two (conservative) scaled to 0-10."""
    a, b = row.get('score_a'), row.get('score_b')
    scores = [s for s in (a, b) if s is not None]
    if not scores:
        return None
    # DB stores 0-1 floats; viewer expects 0-10
    return round(min(scores) * 10.0, 1)


def _karpathy_gate(decision: str) -> str:
    """Map karpathy decisions to the viewer's quality_gate vocabulary.

    KEEP   → pass              (change survived blind eval and was kept)
    REVERT → observation-only  (experiment ran, evaluator rejected — this
                                is the loop working as designed, NOT a
                                failure, so don't colour it red)
    FAST_FAIL / WIN / anything else → observation-only"""
    if not decision:
        return 'observation-only'
    d = decision.upper()
    if d == 'KEEP':
        return 'pass'
    return 'observation-only'


def map_karpathy_experiment(row: dict) -> dict:
    """One karpathy experiment = one agent action.
    Producer is the karpathy loop itself (the actor). Subject is the target
    organ being experimented on (e.g. "brain", "nervous-system"). Prior
    version stuffed organ into producer, which conflated actor and target —
    the viewer's "agents active" then counted 310 distinct organs as if they
    were 310 distinct agents, which is wrong. Karpathy is ONE agent operating
    on many subjects.
    """
    organ = row.get('organ') or 'unknown'
    section = (row.get('section') or '').strip()
    technique = row.get('technique') or ''
    decision = row.get('decision') or ''
    wd = row.get('word_delta') or 0
    reason = row.get('revert_reason') or ''

    # Coarse action label — strip the section suffix so the By-action view
    # doesn't explode into 1,500+ groups. Section lives on subject_detail
    # for anyone who needs the fine grain (drilldown via the detail pane).
    action_label = f"{technique.lower()} experiment"
    if decision == 'KEEP':
        out = f"KEPT · {wd:+d} words"
    elif decision == 'REVERT':
        out = f"REVERTED{(' · ' + reason) if reason else ''}"
    else:
        out = decision or '—'

    return {
        'id': f"karpathy-{row.get('created_at').isoformat()}-{organ}" if row.get('created_at') else f"karpathy-{organ}",
        'ts': _fmt_ts(row.get('created_at')),
        'producer_type': 'agent',
        'producer': 'karpathy',
        'subject': organ,
        'subject_detail': section if section and section != 'full' else None,
        'action': action_label,
        'input_summary': f"technique={technique}; section={section or 'full'}",
        'output_summary': out,
        'quality_gate': _karpathy_gate(decision),
        'quality_score': _score(row),
        'duration_ms': (row.get('wall_clock_seconds') or 0) * 1000 or None,
        'downstream': 'autoresearch_priors update' if decision == 'KEEP' else None,
    }


def map_workflow_execution(row: dict) -> dict:
    """One workflow_executions row = one pipeline run. Producer is the
    workflow name (the actor that ran). Subject is the trigger source
    (what caused it — a hook, eod, userTriggered, etc.)."""
    name = row.get('workflow_name') or 'workflow'
    trigger = row.get('trigger_source') or 'unknown'
    status = (row.get('status') or 'unknown').lower()
    steps_done = row.get('steps_completed') or 0
    steps_failed = row.get('steps_failed') or 0
    dur = row.get('duration_seconds')

    action_label = f"{name} ran"
    out = f"{steps_done} step{'s' if steps_done != 1 else ''} completed"
    if steps_failed:
        out += f" · {steps_failed} failed"

    return {
        'id': row.get('execution_id') or f"workflow-{row.get('start_time')}",
        'ts': _fmt_ts(row.get('start_time')),
        'producer_type': 'system',
        'producer': name,
        'subject': trigger,
        'subject_detail': None,
        'action': action_label,
        'input_summary': f"trigger={trigger}",
        'output_summary': out,
        'quality_gate': 'pass' if status == 'completed' and not steps_failed else 'block' if status == 'failed' else 'observation-only',
        'quality_score': None,
        'duration_ms': int(dur * 1000) if dur else None,
        'downstream': None,
    }


def map_hook_execution(row: dict) -> dict:
    """One hook_executions row = one hook fire. Producer is the hook name.
    Subject is the primary side-effect target surfaced in the counters
    (asana / slack / duckdb) — falls back to 'scheduled' when nothing fired.
    Schema has no execution_id or phases_failed column."""
    name = row.get('hook_name') or 'hook'
    phases_done = row.get('phases_completed') or 0
    dur = row.get('duration_seconds')
    summary = (row.get('summary') or '').strip()
    start = row.get('start_time')
    hid = f"{name}-{start.isoformat()}" if start else f"{name}-unknown"

    asana_w = row.get('asana_writes') or 0
    slack_m = row.get('slack_messages_sent') or 0
    duck_q = row.get('duckdb_queries') or 0

    # Subject = the dominant side-effect target; makes the By-subject view
    # group hooks by "what they acted on" rather than by name.
    if asana_w >= max(slack_m, duck_q) and asana_w > 0:
        subject = 'asana'
    elif slack_m >= duck_q and slack_m > 0:
        subject = 'slack'
    elif duck_q > 0:
        subject = 'duckdb'
    else:
        subject = 'scheduled'

    out = f"{phases_done} phase{'s' if phases_done != 1 else ''} ok"
    if asana_w or slack_m or duck_q:
        parts = []
        if asana_w: parts.append(f"{asana_w} Asana writes")
        if slack_m: parts.append(f"{slack_m} Slack msgs")
        if duck_q:  parts.append(f"{duck_q} queries")
        out += " · " + ", ".join(parts)
    if summary:
        out += " · " + summary[:80]

    return {
        'id': hid,
        'ts': _fmt_ts(start),
        'producer_type': 'hook',
        'producer': name,
        'subject': subject,
        'subject_detail': None,
        'action': 'hook fired',
        'input_summary': 'scheduled hook',
        'output_summary': out,
        'quality_gate': 'pass' if phases_done > 0 else 'observation-only',
        'quality_score': None,
        'duration_ms': int(dur * 1000) if dur else None,
        'downstream': None,
    }


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found", file=sys.stderr)
        return 1

    con = duckdb.connect(str(DB_PATH), read_only=True)

    # Karpathy experiments — the primary activity stream
    karpathy_rows = con.execute(f"""
        SELECT run_id, organ, section, technique, eval_type, eval_tier,
               words_before, words_after, word_delta,
               score_a, score_b, score_c, delta_ab,
               wall_clock_seconds, agent_calls, estimated_tokens, yield_score,
               decision, revert_reason, fast_fail, created_at
        FROM main.autoresearch_experiments
        WHERE created_at >= CURRENT_TIMESTAMP - INTERVAL '{WINDOW_DAYS} days'
        ORDER BY created_at DESC
    """).fetchall()
    karpathy_cols = [d[0] for d in con.description]
    karpathy_activities = [map_karpathy_experiment(dict(zip(karpathy_cols, r))) for r in karpathy_rows]
    print(f"  karpathy experiments: {len(karpathy_activities)}")

    # Workflow executions
    workflow_activities = []
    try:
        wf_rows = con.execute(f"""
            SELECT execution_id, workflow_name, trigger_source,
                   start_time, end_time, status,
                   steps_completed, steps_failed, duration_seconds
            FROM main.workflow_executions
            WHERE start_time >= CURRENT_TIMESTAMP - INTERVAL '{WINDOW_DAYS} days'
            ORDER BY start_time DESC
        """).fetchall()
        wf_cols = [d[0] for d in con.description]
        workflow_activities = [map_workflow_execution(dict(zip(wf_cols, r))) for r in wf_rows]
    except Exception as e:
        print(f"  workflow_executions skipped: {e}", file=sys.stderr)
    print(f"  workflows: {len(workflow_activities)}")

    # Hook executions
    hook_activities = []
    try:
        hk_rows = con.execute(f"""
            SELECT hook_name, start_time, end_time, duration_seconds,
                   phases_completed, asana_reads, asana_writes,
                   slack_messages_sent, duckdb_queries, summary
            FROM main.hook_executions
            WHERE start_time >= CURRENT_TIMESTAMP - INTERVAL '{WINDOW_DAYS} days'
            ORDER BY start_time DESC
        """).fetchall()
        hk_cols = [d[0] for d in con.description]
        hook_activities = [map_hook_execution(dict(zip(hk_cols, r))) for r in hk_rows]
    except Exception as e:
        print(f"  hook_executions skipped: {e}", file=sys.stderr)
    print(f"  hooks: {len(hook_activities)}")

    # Merge, sort newest-first
    all_activities = karpathy_activities + workflow_activities + hook_activities
    all_activities.sort(key=lambda a: a.get('ts', ''), reverse=True)

    # Compute stats directly from activities so they can't drift.
    now = datetime.now(timezone.utc)
    def _within(hours):
        cutoff = now - timedelta(hours=hours)
        n = 0
        for a in all_activities:
            ts = a.get('ts', '')
            if not ts:
                continue
            try:
                if datetime.fromisoformat(ts.replace('Z', '+00:00')) >= cutoff:
                    n += 1
            except Exception:
                continue
        return n

    acts_7d = [a for a in all_activities if a.get('ts') and _is_within_days(a['ts'], 7)]
    producers_7d = {a.get('producer') for a in acts_7d if a.get('producer')}
    hooks_7d = sum(1 for a in acts_7d if a.get('producer_type') == 'hook')
    failures_7d = sum(1 for a in acts_7d if a.get('quality_gate') == 'block')

    payload = {
        'generated': datetime.now().isoformat(timespec='seconds') + PT_OFFSET,
        'source': 'refresh-agent-activity.py',
        'stats': {
            'total_24h': _within(24),
            'total_7d': len(acts_7d),
            'total_30d': len(all_activities),
            'agents_active': len(producers_7d),
            'hooks_fired': hooks_7d,
            'failures': failures_7d,
        },
        'activities': all_activities,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2, default=str))
    print(f"Wrote {OUT_PATH} — {len(all_activities)} activities, stats: {payload['stats']}")
    return 0


def _is_within_days(ts_str: str, days: int) -> bool:
    """Parse an ISO timestamp and check if it's within the last N days."""
    try:
        ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        cutoff = datetime.now(ts.tzinfo) - timedelta(days=days)
        return ts >= cutoff
    except Exception:
        return False


if __name__ == '__main__':
    sys.exit(main())
