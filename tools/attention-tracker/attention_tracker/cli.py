"""CLI entry point for the Attention Tracker.

Provides subcommands for querying attention data, managing the daemon,
and piping insights into the Decision Journal and morning routine.

Entry point: ``attention-tracker = "attention_tracker.cli:main"``
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
from datetime import date, timedelta

from attention_tracker.database import Database
from attention_tracker.models import TrackerConfig
from attention_tracker.rules_loader import load_rules, validate_rules
from attention_tracker.summary import (
    _format_duration_ms,
    generate_daily_summary,
    generate_top_insight,
    store_daily_summary,
)

PID_FILE = os.path.expanduser(
    "~/.local/share/attention-tracker/daemon.pid"
)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _resolve_date(date_str: str) -> str:
    """Convert 'today', 'yesterday', or YYYY-MM-DD to YYYY-MM-DD."""
    if date_str == "today":
        return date.today().isoformat()
    if date_str == "yesterday":
        return (date.today() - timedelta(days=1)).isoformat()
    return date_str


def _open_db_readonly(config: TrackerConfig) -> Database:
    """Open the database (read-only queries go through normal connection)."""
    return Database(config.db_path)


# ------------------------------------------------------------------
# Subcommand handlers
# ------------------------------------------------------------------

def cmd_today(config: TrackerConfig) -> None:
    """Display today's summary."""
    today = date.today().isoformat()
    db = _open_db_readonly(config)
    try:
        summary = generate_daily_summary(db, today)
        active = _format_duration_ms(summary.total_active_ms)
        idle = _format_duration_ms(summary.total_idle_ms)
        top = summary.top_category or "—"
        sessions = summary.focus_session_count
        switches = summary.switch_count

        print(f"Date:            {today}")
        print(f"Active time:     {active}")
        print(f"Idle time:       {idle}")
        print(f"Focus sessions:  {sessions}")
        print(f"Top category:    {top}")
        print(f"Context switches:{switches}")
        if summary.productivity_score_avg > 0:
            print(f"Productivity:    {summary.productivity_score_avg:.1%}")
    finally:
        db.close()


def cmd_yesterday(config: TrackerConfig, oneliner: bool = False) -> None:
    """Display yesterday's summary. --oneliner for morning routine."""
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    db = _open_db_readonly(config)
    try:
        summary = generate_daily_summary(db, yesterday)

        if oneliner:
            active = _format_duration_ms(summary.total_active_ms)
            sessions = summary.focus_session_count
            switches = summary.switch_count
            top = summary.top_category or "misc"
            print(
                f"Yesterday: {active} focused "
                f"({sessions} deep session{'s' if sessions != 1 else ''}), "
                f"{switches} context switch{'es' if switches != 1 else ''}, "
                f"top category {top}"
            )
        else:
            active = _format_duration_ms(summary.total_active_ms)
            idle = _format_duration_ms(summary.total_idle_ms)
            top = summary.top_category or "—"
            sessions = summary.focus_session_count

            print(f"Date:            {yesterday}")
            print(f"Active time:     {active}")
            print(f"Idle time:       {idle}")
            print(f"Focus sessions:  {sessions}")
            print(f"Top category:    {top}")
            print(f"Context switches:{summary.switch_count}")
            if summary.productivity_score_avg > 0:
                print(f"Productivity:    {summary.productivity_score_avg:.1%}")
    finally:
        db.close()


def cmd_journal(config: TrackerConfig) -> None:
    """Generate and output top_daily_insight for Decision Journal."""
    today = date.today().isoformat()
    db = _open_db_readonly(config)
    try:
        # Check if summary already exists
        row = db.connection.execute(
            "SELECT top_daily_insight FROM daily_summaries WHERE date = ?",
            (today,),
        ).fetchone()

        if row and row[0]:
            print(row[0])
            return

        # Generate and store
        summary = generate_daily_summary(db, today)
        summary.top_daily_insight = generate_top_insight(summary)
        store_daily_summary(db, summary)
        print(summary.top_daily_insight)
    finally:
        db.close()


def cmd_sessions(config: TrackerConfig, date_str: str) -> None:
    """List focus sessions for a date."""
    resolved = _resolve_date(date_str)
    db = _open_db_readonly(config)
    try:
        rows = db.connection.execute(
            "SELECT start_time, end_time, total_duration_ms, category "
            "FROM focus_sessions WHERE DATE(start_time) = ? "
            "ORDER BY start_time",
            (resolved,),
        ).fetchall()

        if not rows:
            print(f"No focus sessions for {resolved}")
            return

        print(f"{'Start':<20} {'End':<20} {'Duration':<10} {'Category'}")
        print("-" * 60)
        for start, end, dur_ms, cat in rows:
            start_short = start[:19] if start else "—"
            end_short = end[:19] if end else "ongoing"
            dur = _format_duration_ms(dur_ms) if dur_ms else "—"
            print(f"{start_short:<20} {end_short:<20} {dur:<10} {cat or '—'}")
    finally:
        db.close()


def cmd_unknowns(config: TrackerConfig) -> None:
    """List uncategorized app names."""
    db = _open_db_readonly(config)
    try:
        rows = db.connection.execute(
            "SELECT DISTINCT app_name FROM activity_events "
            "WHERE category = 'uncategorized' ORDER BY app_name"
        ).fetchall()

        if not rows:
            print("No uncategorized apps found.")
            return

        print("Uncategorized apps:")
        for (name,) in rows:
            print(f"  {name}")
    finally:
        db.close()


def cmd_start() -> None:
    """Start the daemon."""
    # Launch as a subprocess so the CLI returns immediately
    try:
        proc = subprocess.Popen(
            [sys.executable, "-m", "attention_tracker.daemon"],
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # Write PID file
        os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
        with open(PID_FILE, "w") as f:
            f.write(str(proc.pid))
        print(f"Daemon started (PID {proc.pid})")
    except Exception as exc:
        print(f"Failed to start daemon: {exc}", file=sys.stderr)
        sys.exit(1)


def cmd_stop() -> None:
    """Stop the daemon."""
    if not os.path.exists(PID_FILE):
        print("Daemon is not running (no PID file)")
        return

    try:
        with open(PID_FILE) as f:
            pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)
        os.remove(PID_FILE)
        print(f"Daemon stopped (PID {pid})")
    except ProcessLookupError:
        os.remove(PID_FILE)
        print("Daemon was not running (stale PID file removed)")
    except Exception as exc:
        print(f"Failed to stop daemon: {exc}", file=sys.stderr)
        sys.exit(1)


def cmd_status() -> None:
    """Check if daemon is running."""
    if not os.path.exists(PID_FILE):
        print("Daemon is not running")
        return

    try:
        with open(PID_FILE) as f:
            pid = int(f.read().strip())
        # Check if process exists (signal 0 doesn't kill, just checks)
        os.kill(pid, 0)
        print(f"Daemon is running (PID {pid})")
    except ProcessLookupError:
        print("Daemon is not running (stale PID file)")
    except PermissionError:
        print(f"Daemon appears running (PID {pid}, permission denied on check)")


def cmd_rule_validate(config: TrackerConfig) -> None:
    """Validate classification rules."""
    rules_path = os.path.expanduser(config.rules_path)
    try:
        rules = load_rules(rules_path)
    except FileNotFoundError:
        print(f"Rules file not found: {rules_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Error loading rules: {exc}", file=sys.stderr)
        sys.exit(1)

    errors = validate_rules(rules)
    if errors:
        print(f"Found {len(errors)} error(s):")
        for err in errors:
            print(f"  ✗ {err}")
        sys.exit(1)
    else:
        print(f"All {len(rules)} rules are valid.")


# ------------------------------------------------------------------
# Argument parser
# ------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="attention-tracker",
        description="Local attention tracking with Bayesian state inference",
    )
    sub = parser.add_subparsers(dest="command")

    # today
    sub.add_parser("today", help="Display today's summary")

    # yesterday
    p_yesterday = sub.add_parser("yesterday", help="Display yesterday's summary")
    p_yesterday.add_argument(
        "--oneliner", action="store_true",
        help="Single-line output for morning routine",
    )

    # journal
    sub.add_parser("journal", help="Generate daily insight for Decision Journal")

    # sessions
    p_sessions = sub.add_parser("sessions", help="List focus sessions")
    p_sessions.add_argument(
        "--date", default="today",
        help="Date to query: 'today', 'yesterday', or YYYY-MM-DD",
    )

    # unknowns
    sub.add_parser("unknowns", help="List uncategorized app names")

    # start / stop / status
    sub.add_parser("start", help="Start the daemon")
    sub.add_parser("stop", help="Stop the daemon")
    sub.add_parser("status", help="Check daemon status")

    # rule validate
    p_rule = sub.add_parser("rule", help="Rule management")
    rule_sub = p_rule.add_subparsers(dest="rule_command")
    rule_sub.add_parser("validate", help="Validate classification rules")

    return parser


# ------------------------------------------------------------------
# Main entry point
# ------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    config = TrackerConfig()

    try:
        if args.command == "today":
            cmd_today(config)
        elif args.command == "yesterday":
            cmd_yesterday(config, oneliner=args.oneliner)
        elif args.command == "journal":
            cmd_journal(config)
        elif args.command == "sessions":
            cmd_sessions(config, date_str=args.date)
        elif args.command == "unknowns":
            cmd_unknowns(config)
        elif args.command == "start":
            cmd_start()
        elif args.command == "stop":
            cmd_stop()
        elif args.command == "status":
            cmd_status()
        elif args.command == "rule":
            if args.rule_command == "validate":
                cmd_rule_validate(config)
            else:
                parser.parse_args(["rule", "--help"])
        else:
            parser.print_help()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
