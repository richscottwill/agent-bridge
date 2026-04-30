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
from datetime import date
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
    }
    HISTORY.write_text(json.dumps(out, indent=2))
    print(f"wrote {HISTORY} — {len(rows)} rows ({out['earliest']} → {out['latest']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
