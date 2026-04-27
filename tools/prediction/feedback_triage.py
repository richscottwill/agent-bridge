"""
feedback_triage.py — Phase 6.5.4 — review queue for projection feedback.

Scans ps.projection_feedback for unprocessed entries (especially
verdict='missing_context' freetext) and presents them in a CLI triage view.
Richard reviews each, decides: discard / convert-to-qualitative-prior /
convert-to-regime-change / convert-to-parameter-update. The tool records
the decision + sets processed_at.

Usage:
    cd shared/tools
    python3 -m prediction.feedback_triage list            # list all unprocessed
    python3 -m prediction.feedback_triage show <id>       # full detail for one entry
    python3 -m prediction.feedback_triage resolve <id> <disposition> [--note TEXT]
        # disposition ∈ {discard, qualitative_prior, regime_change, param_update}
"""
from __future__ import annotations

import sys


VALID_DISPOSITIONS = {"discard", "qualitative_prior", "regime_change", "param_update"}


def _con():
    import duckdb
    from prediction.config import MOTHERDUCK_TOKEN  # type: ignore
    return duckdb.connect(f"md:ps_analytics?motherduck_token={MOTHERDUCK_TOKEN}")


def list_unprocessed(limit: int = 50) -> None:
    con = _con()
    rows = con.execute("""
        SELECT id, submitted_at, user_id, scope, time_period, verdict,
               magnitude_pct, COALESCE(freetext, ''), scenario_chip
        FROM ps.projection_feedback
        WHERE processed_at IS NULL
        ORDER BY submitted_at DESC
        LIMIT ?
    """, [limit]).fetchall()
    if not rows:
        print("No unprocessed feedback entries.")
        return
    print(f"\n{len(rows)} unprocessed feedback entries (newest first):\n")
    print(f"{'ID':<24} {'WHEN':<20} {'WHO':<10} {'SCOPE':<6} {'PERIOD':<7} {'VERDICT':<18} {'%':<5} {'CHIP':<13} TEXT")
    print("-" * 150)
    for r in rows:
        fid, ts, uid, scope, period, verdict, mag, txt, chip = r
        short_id = fid[:22] if len(fid) > 22 else fid
        short_ts = str(ts)[:19]
        magstr = f"{mag:+.0f}%" if mag is not None else "—"
        print(f"{short_id:<24} {short_ts:<20} {uid:<10} {scope:<6} {period:<7} {verdict:<18} {magstr:<5} {(chip or ''):<13} {txt[:60]}")
    print()


def show_entry(entry_id: str) -> None:
    con = _con()
    row = con.execute("""
        SELECT * FROM ps.projection_feedback WHERE id = ?
    """, [entry_id]).fetchone()
    if not row:
        print(f"No entry {entry_id}")
        return
    cols = [c[0] for c in con.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema='ps' AND table_name='projection_feedback' ORDER BY ordinal_position
    """).fetchall()]
    for k, v in zip(cols, row):
        print(f"  {k:<30} {v}")


def resolve(entry_id: str, disposition: str, note: str | None = None) -> None:
    if disposition not in VALID_DISPOSITIONS:
        print(f"Invalid disposition. Must be one of: {sorted(VALID_DISPOSITIONS)}")
        return
    con = _con()
    resulted_in_prior = disposition == "qualitative_prior"
    con.execute("""
        UPDATE ps.projection_feedback
        SET processed_at = CURRENT_TIMESTAMP,
            resulted_in_qualitative_prior = ?,
            notes = ?
        WHERE id = ?
    """, [resulted_in_prior, note or disposition, entry_id])
    print(f"Resolved {entry_id} → {disposition}" + (f" (note: {note})" if note else ""))
    if disposition == "qualitative_prior":
        print("  → Don't forget to append a scenario to qualitative_priors.yaml.")
    elif disposition == "regime_change":
        print("  → Don't forget to add a row to ps.regime_changes.")
    elif disposition == "param_update":
        print("  → Don't forget to adjust the relevant parameter in ps.market_projection_params.")


def sync_from_queue(queue_json: list[dict]) -> int:
    """Insert rows from a browser-side localStorage queue into ps.projection_feedback.

    Returns number of rows inserted.
    """
    con = _con()
    n = 0
    for rec in queue_json:
        try:
            con.execute("""
                INSERT INTO ps.projection_feedback
                    (id, projection_id, user_id, verdict, magnitude_pct,
                     freetext, scope, time_period, target_mode, target_value,
                     scenario_chip, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (id) DO NOTHING
            """, [
                rec.get("id"),
                rec.get("projection_id"),
                rec.get("user_id"),
                rec.get("verdict"),
                rec.get("magnitude_pct"),
                rec.get("freetext"),
                rec.get("scope"),
                rec.get("time_period"),
                rec.get("target_mode"),
                rec.get("target_value"),
                rec.get("scenario_chip"),
                rec.get("submitted_at"),
            ])
            n += 1
        except Exception as e:
            print(f"  ! skipped {rec.get('id')}: {e}")
    return n


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__)
        return
    cmd = args[0]
    if cmd == "list":
        list_unprocessed()
    elif cmd == "show" and len(args) >= 2:
        show_entry(args[1])
    elif cmd == "resolve" and len(args) >= 3:
        note = None
        if "--note" in args:
            i = args.index("--note")
            if i + 1 < len(args):
                note = args[i + 1]
        resolve(args[1], args[2], note=note)
    else:
        print(f"Unrecognized command. Run with --help.")


if __name__ == "__main__":
    main()
