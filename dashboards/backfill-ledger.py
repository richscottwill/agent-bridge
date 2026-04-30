#!/usr/bin/env python3
"""
backfill-ledger.py — One-time backfill of populate-intelligence.py's 17
hand-curated commitments (+ delegate/communicate/differentiate) into the
live DuckDB ledger and am-command-center-intel.json.

Safe to re-run. Deduped by text-hash. No fake completions — all backfilled
commitments land as status=not_started; Richard marks done/remove in the UI.
"""
import hashlib, json, os, sys
from pathlib import Path
from datetime import date, timedelta, datetime, timezone

import duckdb

HOME = Path.home()
INTEL_PATH = HOME / "shared/context/active/am-command-center-intel.json"
PI_PATH = HOME / "shared/dashboards/populate-intelligence.py"


def get_token():
    try:
        cfg = json.loads((HOME / ".kiro/settings/mcp.json").read_text())
        return cfg.get("mcpServers", {}).get("duckdb", {}).get("env", {}).get("motherduck_token")
    except Exception:
        return None


def load_curated():
    """Exec the populate-intelligence.py module to extract its 4 curated lists."""
    src = PI_PATH.read_text()
    # Strip the write-to-disk section so the exec is side-effect-free
    src = src.split("# Load, patch, write")[0]
    ns = {}
    exec(src, ns)
    return {
        "commitments": ns.get("commitments", []),
        "delegate": ns.get("delegate", []),
        "communicate": ns.get("communicate", []),
        "differentiate": ns.get("differentiate", []),
    }


def backfill_commitments(con, commitments):
    """Insert curated commitments into live ledger as not_started. Skip dupes by text-hash."""
    existing = set(r[0] for r in con.execute("SELECT text_hash FROM main.commitment_ledger").fetchall())
    today = date.today()
    added = 0
    skipped = 0
    for c in commitments:
        text = (c.get("text") or "").strip()
        if not text:
            continue
        th = hashlib.md5(text.encode()).hexdigest()
        if th in existing:
            skipped += 1
            continue
        days_old = c.get("days_old", 0) or 0
        first_seen = today - timedelta(days=days_old)
        safe = lambda s: (s or "").replace("'", "''")
        con.execute(f"""
            INSERT INTO main.commitment_ledger
              (text_hash, text, source, person, said_by, status, context, quote, days_old, overdue, first_seen, last_seen)
            VALUES (
              '{th}',
              '{safe(text)}',
              '{safe(c.get("source",""))}',
              '{safe(c.get("person",""))}',
              '{safe(c.get("said_by",""))}',
              'not_started',
              '{safe(c.get("context",""))}',
              '{safe(c.get("quote",""))}',
              {days_old},
              {'TRUE' if c.get("overdue") else 'FALSE'},
              DATE '{first_seen}',
              DATE '{today}'
            )
        """)
        added += 1
    return added, skipped


def merge_intel_json(curated):
    """Merge curated delegate/communicate/differentiate into am-command-center-intel.json.
    Dedup by text field. Keep existing entries; append new ones."""
    existing = {}
    if INTEL_PATH.exists():
        try:
            existing = json.loads(INTEL_PATH.read_text())
        except Exception:
            existing = {}

    stats = {"delegate": [0, 0], "communicate": [0, 0], "differentiate": [0, 0]}

    for section in ("delegate", "communicate", "differentiate"):
        items = existing.get(section, []) or []
        # Dedup key per-section
        if section == "delegate":
            keyfn = lambda it: (it.get("task") or "").strip().lower()
        else:
            keyfn = lambda it: (it.get("text") or it.get("action") or "").strip().lower()
        seen = {keyfn(it) for it in items if keyfn(it)}
        for new in curated.get(section, []):
            k = keyfn(new)
            if k and k in seen:
                stats[section][1] += 1  # skipped
                continue
            items.append(new)
            seen.add(k)
            stats[section][0] += 1  # added
        existing[section] = items

    # Keep commitments list in the intel JSON too, so the generator's am_intel.get("commitments")
    # picks them up on the next run. The DuckDB sync dedups by hash so re-adding is safe.
    existing_texts = {(c.get("text") or "").strip().lower() for c in (existing.get("commitments") or [])}
    c_added = 0
    c_skipped = 0
    commitments_out = list(existing.get("commitments", []))
    for c in curated.get("commitments", []):
        t = (c.get("text") or "").strip().lower()
        if not t or t in existing_texts:
            c_skipped += 1
            continue
        commitments_out.append(c)
        existing_texts.add(t)
        c_added += 1
    existing["commitments"] = commitments_out

    existing["backfilled_at"] = datetime.now(timezone.utc).isoformat()
    INTEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    INTEL_PATH.write_text(json.dumps(existing, indent=2, default=str))
    return stats, (c_added, c_skipped)


def main():
    token = get_token()
    con = duckdb.connect(f"md:ps_analytics?motherduck_token={token}" if token else "md:ps_analytics")

    curated = load_curated()
    print(f"Curated: {len(curated['commitments'])} commitments, "
          f"{len(curated['delegate'])} delegate, "
          f"{len(curated['communicate'])} communicate, "
          f"{len(curated['differentiate'])} differentiate")

    added, skipped = backfill_commitments(con, curated["commitments"])
    print(f"Ledger backfill: +{added} new, {skipped} already present")

    intel_stats, (c_a, c_s) = merge_intel_json(curated)
    print(f"Intel JSON merge:")
    print(f"  commitments: +{c_a} new, {c_s} skipped")
    for sec, (a, s) in intel_stats.items():
        print(f"  {sec}: +{a} new, {s} skipped")

    # Final counts
    row = con.execute("""
        SELECT COUNT(*) AS total,
               COUNT(*) FILTER (WHERE status='not_started') AS active,
               COUNT(*) FILTER (WHERE status='done') AS done,
               COUNT(*) FILTER (WHERE status='dismissed') AS dismissed,
               COUNT(*) FILTER (WHERE status='removed') AS removed
        FROM main.commitment_ledger
    """).fetchone()
    print(f"Ledger now: {row[0]} total ({row[1]} active, {row[2]} done, {row[3]} dismissed, {row[4]} removed)")


if __name__ == "__main__":
    main()
