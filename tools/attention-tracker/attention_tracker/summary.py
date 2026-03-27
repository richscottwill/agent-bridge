"""Daily Summary aggregation for the Attention Tracker.

Queries activity_events and focus_sessions for a given date, computes
aggregated metrics, and persists the result to daily_summaries.
"""

from __future__ import annotations

import json
from collections import defaultdict

from attention_tracker.database import Database
from attention_tracker.models import DailySummary


def _format_duration_ms(ms: int) -> str:
    """Format milliseconds as human-readable string like '3h12m' or '47m'."""
    total_minutes = ms // 60_000
    hours = total_minutes // 60
    minutes = total_minutes % 60
    if hours > 0 and minutes > 0:
        return f"{hours}h{minutes:02d}m"
    if hours > 0:
        return f"{hours}h"
    return f"{minutes}m"


def generate_top_insight(summary: DailySummary) -> str:
    """Generate a one-liner insight for the Decision Journal.

    Example: "3h12m focused on deep-work, 2 deep sessions, 14 context switches"
    """
    focus_time = _format_duration_ms(summary.total_active_ms)
    top = summary.top_category or "uncategorized"
    sessions = summary.focus_session_count
    switches = summary.switch_count

    return (
        f"{focus_time} focused on {top}, "
        f"{sessions} deep session{'s' if sessions != 1 else ''}, "
        f"{switches} context switch{'es' if switches != 1 else ''}"
    )


def generate_daily_summary(db: Database, date: str) -> DailySummary:
    """Generate a daily summary for the given date (YYYY-MM-DD format).

    Queries activity_events and focus_sessions for the date,
    computes aggregations, and returns a DailySummary.
    """
    conn = db.connection

    # 1. Query all events for the date
    events = conn.execute(
        "SELECT * FROM activity_events WHERE DATE(timestamp) = ?", (date,)
    ).fetchall()
    col_names = [desc[0] for desc in conn.execute(
        "SELECT * FROM activity_events LIMIT 0"
    ).description]
    events = [dict(zip(col_names, row)) for row in events]

    # 2. Query focus sessions for the date
    sessions = conn.execute(
        "SELECT * FROM focus_sessions WHERE DATE(start_time) = ?", (date,)
    ).fetchall()

    # 3. Compute aggregations
    total_active_ms = 0
    total_idle_ms = 0
    category_totals: dict[str, int] = defaultdict(int)
    weighted_score_sum = 0.0
    weighted_duration_sum = 0
    switch_count = 0
    prev_category = None

    for ev in events:
        dur = ev["duration_ms"] or 0
        mode = ev["attention_mode"] or ""
        category = ev["category"] or "uncategorized"
        score = ev["productivity_score"]

        if mode == "IDLE":
            total_idle_ms += dur
        else:
            total_active_ms += dur
            category_totals[category] += dur

        # Productivity score: weighted average excluding NULLs
        if score is not None:
            weighted_score_sum += score * dur
            weighted_duration_sum += dur

        # Count context switches (consecutive category changes)
        if prev_category is not None and category != prev_category:
            switch_count += 1
        prev_category = category

    # Productivity score avg (exclude NULLs from both numerator and denominator)
    productivity_score_avg = (
        weighted_score_sum / weighted_duration_sum
        if weighted_duration_sum > 0
        else 0.0
    )

    # Focus session metrics
    focus_session_count = len(sessions)
    session_col_names = [desc[0] for desc in conn.execute(
        "SELECT * FROM focus_sessions LIMIT 0"
    ).description]
    session_dicts = [dict(zip(session_col_names, row)) for row in sessions]

    total_session_duration = sum(
        (s["total_duration_ms"] or 0) for s in session_dicts
    )
    avg_focus_duration_ms = (
        total_session_duration // focus_session_count
        if focus_session_count > 0
        else 0
    )

    # Top category by active time
    top_category = ""
    if category_totals:
        top_category = max(category_totals, key=category_totals.get)

    category_breakdown = dict(category_totals)

    summary = DailySummary(
        date=date,
        total_active_ms=total_active_ms,
        total_idle_ms=total_idle_ms,
        focus_session_count=focus_session_count,
        avg_focus_duration_ms=avg_focus_duration_ms,
        top_category=top_category,
        category_breakdown=category_breakdown,
        switch_count=switch_count,
        productivity_score_avg=productivity_score_avg,
    )

    # Generate insight
    summary.top_daily_insight = generate_top_insight(summary)

    return summary


def store_daily_summary(db: Database, summary: DailySummary) -> bool:
    """Persist a DailySummary to the daily_summaries table."""
    try:
        db.connection.execute(
            """\
INSERT OR REPLACE INTO daily_summaries (
    date, total_active_ms, total_idle_ms, focus_session_count,
    avg_focus_duration_ms, top_category, category_breakdown,
    switch_count, productivity_score_avg, top_daily_insight
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                summary.date,
                summary.total_active_ms,
                summary.total_idle_ms,
                summary.focus_session_count,
                summary.avg_focus_duration_ms,
                summary.top_category,
                json.dumps(summary.category_breakdown),
                summary.switch_count,
                summary.productivity_score_avg,
                summary.top_daily_insight,
            ),
        )
        db.connection.commit()
        return True
    except Exception:
        return False
