#!/usr/bin/env python3
"""build-wiki-health-history.py — Append a daily wiki-health snapshot.

Reads the current `data/wiki-search-index.json` (from build-wiki-index.py) and appends one row
to `data/wiki-health-history.json` capturing the key health metrics. Designed to be run daily
after build-wiki-index.py so the WS-M04 fan chart on wiki-search.html has a growing time series.

Shape of each history row:
  {
    "date": "YYYY-MM-DD",
    "total_docs": int,
    "published": int,        # SharePoint-published agent-created articles
    "local_only": int,
    "stale": int,
    "orphans": int,          # WS-M02
    "contradictions": int,   # WS-M09
    "demand_open": int,      # WS-M05 — open demand-log entries
    "by_status": {FINAL: n, REVIEW: n, DRAFT: n, ...}
  }

Idempotent on same day — replaces the last row if its date matches today. Keeps last 365 days.
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).parent
INDEX = HERE / "data" / "wiki-search-index.json"
HISTORY = HERE / "data" / "wiki-health-history.json"
MAX_ROWS = 365


def main() -> int:
    if not INDEX.exists():
        print(f"ERROR: {INDEX} not found — run build-wiki-index.py first", file=sys.stderr)
        return 1

    idx = json.loads(INDEX.read_text())
    today = date.today().isoformat()

    sp = idx.get("sharepoint", {}) or {}
    demand = idx.get("demand_log_entries", []) or []
    demand_open = sum(1 for d in demand if d.get("status") == "open")

    row = {
        "date": today,
        "total_docs": idx.get("total_docs", 0),
        "published": sp.get("published", 0),
        "local_only": sp.get("local_only", 0),
        "stale": sp.get("stale", 0),
        "orphans": idx.get("orphan_count", 0),
        "contradictions": idx.get("contradiction_count", 0),
        "demand_open": demand_open,
        "by_status": idx.get("statuses", {}),
    }

    # Load existing history
    if HISTORY.exists():
        try:
            history = json.loads(HISTORY.read_text())
        except Exception:
            history = {"rows": []}
    else:
        history = {"rows": []}

    rows = history.get("rows", [])
    # Idempotent: replace same-date row if present
    rows = [r for r in rows if r.get("date") != today]
    rows.append(row)
    rows.sort(key=lambda r: r.get("date", ""))
    rows = rows[-MAX_ROWS:]

    out = {
        "generated": today,
        "row_count": len(rows),
        "earliest": rows[0]["date"] if rows else None,
        "latest": rows[-1]["date"] if rows else None,
        "rows": rows,
        # #003 (2026-05-01): weekly rollup for the hero-KPI sparklines on
        # wiki-search.html. Each entry: the last-observed daily row per
        # ISO week. Deterministic + idempotent — same input produces same
        # output regardless of run frequency. When daily rows are thin
        # (< 6 weeks accumulated), the consumer renders what it has
        # instead of showing a placeholder.
        "weekly_rollup": _compute_weekly_rollup(rows),
    }
    HISTORY.write_text(json.dumps(out, indent=2))
    print(f"wrote {HISTORY} — {len(rows)} rows ({out['earliest']} → {out['latest']})")
    return 0


def _compute_weekly_rollup(rows):
    """Aggregate daily rows into last-observed-per-ISO-week entries.

    Output shape:
        [{"week": "2026-W18", "date": "2026-05-03", <all row metrics>}, ...]
    Ordered oldest → newest. Returns empty list when no rows.
    """
    if not rows:
        return []
    by_week = {}
    for r in rows:
        d = r.get("date")
        if not d:
            continue
        try:
            dt = datetime.fromisoformat(d).date()
        except Exception:
            continue
        iso_year, iso_week, _ = dt.isocalendar()
        key = f"{iso_year}-W{iso_week:02d}"
        existing = by_week.get(key)
        if not existing or r.get("date", "") > existing.get("date", ""):
            by_week[key] = dict(r, week=key)
    out = [by_week[k] for k in sorted(by_week.keys())]
    return out


if __name__ == "__main__":
    sys.exit(main())
