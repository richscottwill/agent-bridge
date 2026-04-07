#!/usr/bin/env python3
"""
Slack Channel History → DuckDB Bulk Ingester

Usage:
  python3 slack-ingest.py <channel_id> <channel_name> < history.json
  python3 slack-ingest.py <channel_id> <channel_name> history.json

Reads Slack batch_get_conversation_history JSON output,
extracts message fields, and bulk-inserts into slack_messages table.
Also updates slack_people with any new authors found.

Deduplicates on ts (primary key) — existing messages get replaced.
"""

import sys
import json
import duckdb
from pathlib import Path

DB_PATH = Path("/shared/user/tools/data/ps-analytics.duckdb")
RICHARD_ID = "U040ECP305S"


def extract_text(msg: dict) -> str:
    """Extract plain text from a Slack message, handling blocks."""
    # Use the top-level 'text' field — Slack always provides it
    return msg.get("text", "")


def extract_preview(text: str, max_len: int = 200) -> str:
    """First N chars of text for quick scanning."""
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


def classify_signal(text: str) -> str | None:
    """Basic signal classification from message text."""
    t = text.lower()
    decision_words = ["decided", "going with", "confirmed", "approved", "let's do", "aligned", "final call"]
    action_words = ["can you", "please", "action needed", "todo", "need you to", "help to"]
    status_words = ["update:", "fyi", "completed", "done", "live", "launched", "dialed up"]
    escalation_words = ["blocked", "issue", "error", "failed", "sev2", "urgent"]

    for w in decision_words:
        if w in t:
            return "decision"
    for w in escalation_words:
        if w in t:
            return "escalation"
    for w in action_words:
        if w in t:
            return "action-item"
    for w in status_words:
        if w in t:
            return "status-change"
    return None


def has_richard_reaction(msg: dict) -> bool:
    """Check if Richard reacted to this message."""
    for r in msg.get("reactions", []):
        if RICHARD_ID in r.get("users", []):
            return True
    return False


def process_messages(messages: list, channel_id: str, channel_name: str) -> list:
    """Convert raw Slack messages into rows for slack_messages table."""
    rows = []
    for msg in messages:
        if msg.get("subtype") in ("channel_join", "channel_leave", "channel_topic", "channel_purpose",
                                    "tabbed_canvas_updated"):
            continue

        ts = msg.get("ts")
        if not ts:
            continue

        text = extract_text(msg)
        if not text or len(text.strip()) == 0:
            continue

        author_id = msg.get("user", "")
        # Get display_name from user_profile if available
        up = msg.get("user_profile", {})
        author_alias = up.get("name") or up.get("display_name") or ""
        author_name = up.get("real_name") or ""

        thread_ts = msg.get("thread_ts")
        is_reply = thread_ts is not None and thread_ts != ts
        reply_count = msg.get("reply_count", 0)
        reaction_count = sum(r.get("count", 0) for r in msg.get("reactions", []))

        rows.append((
            ts,
            channel_id,
            channel_name,
            thread_ts if is_reply else None,
            author_id,
            author_alias,
            author_name,
            extract_preview(text),
            text,
            author_id == RICHARD_ID,
            is_reply,
            reply_count,
            reaction_count,
            has_richard_reaction(msg),
            classify_signal(text),
        ))
    return rows


def parse_messages(channel_id: str, channel_name: str, data) -> list:
    """Parse raw Slack API response into insertable rows."""
    if isinstance(data, list):
        messages = []
        for item in data:
            if item.get("channelId") == channel_id:
                messages = item.get("result", {}).get("messages", [])
                break
        if not messages and data:
            messages = data[0].get("result", {}).get("messages", [])
    elif isinstance(data, dict):
        messages = data.get("messages", [])
    else:
        return []

    return process_messages(messages, channel_id, channel_name)


def generate_sql(rows: list) -> str:
    """Generate SQL INSERT statements for pasting into DuckDB MCP tool.
    Outputs batches of 25 rows each."""
    if not rows:
        return ""

    output = []
    for i in range(0, len(rows), 25):
        batch = rows[i:i+25]
        values = []
        for r in batch:
            ts, ch_id, ch_name, thread_ts, author_id, alias, name, preview, text, is_r, is_reply, replies, reactions, r_reacted, signal = r
            # Escape single quotes
            def esc(s):
                if s is None:
                    return "NULL"
                return "'" + str(s).replace("'", "''") + "'"

            thread_val = esc(thread_ts) if thread_ts else "NULL"
            signal_val = esc(signal) if signal else "NULL"
            values.append(
                f"({esc(ts)}, {esc(ch_id)}, {esc(ch_name)}, {thread_val}, "
                f"{esc(author_id)}, {esc(alias)}, {esc(name)}, "
                f"{esc(preview[:200])}, {esc(text[:2000])}, "
                f"{'TRUE' if is_r else 'FALSE'}, {'TRUE' if is_reply else 'FALSE'}, "
                f"{replies}, {reactions}, {'TRUE' if r_reacted else 'FALSE'}, "
                f"{signal_val}, current_timestamp)"
            )
        sql = ("INSERT OR REPLACE INTO slack_messages "
               "(ts, channel_id, channel_name, thread_ts, author_id, author_alias, author_name, "
               "text_preview, full_text, is_richard, is_thread_reply, reply_count, "
               "reaction_count, richard_reacted, signal_type, ingested_at) VALUES\n"
               + ",\n".join(values))
        output.append(sql)

    return "\n;\n".join(output)


def ingest(channel_id: str, channel_name: str, data):
    """Main ingestion: parse messages and bulk-insert into DuckDB."""
    rows = parse_messages(channel_id, channel_name, data)
    if not rows:
        print("No messages to insert", file=sys.stderr)
        return

    # Try direct DB connection first
    try:
        con = duckdb.connect(str(DB_PATH))
        con.executemany(
            """INSERT OR REPLACE INTO slack_messages
               (ts, channel_id, channel_name, thread_ts, author_id, author_alias, author_name,
                text_preview, full_text, is_richard, is_thread_reply, reply_count,
                reaction_count, richard_reacted, signal_type, ingested_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, current_timestamp)""",
            rows
        )

        author_ids = set()
        for row in rows:
            aid = row[4]
            if aid and aid not in author_ids:
                author_ids.add(aid)
                alias = row[5]
                name = row[6]
                if alias or name:
                    con.execute(
                        """INSERT INTO slack_people (user_id, alias, display_name, total_messages, ingested_at)
                           VALUES (?, ?, ?, 1, current_timestamp)
                           ON CONFLICT (user_id) DO UPDATE SET
                             alias = COALESCE(EXCLUDED.alias, slack_people.alias),
                             display_name = COALESCE(EXCLUDED.display_name, slack_people.display_name),
                             total_messages = slack_people.total_messages + 1,
                             last_interaction = current_date,
                             ingested_at = current_timestamp""",
                        [aid, alias, name]
                    )

        con.close()
        print(f"Inserted {len(rows)} messages from {channel_name} ({channel_id})")

    except Exception as e:
        if "lock" in str(e).lower():
            # DB is locked by MCP server — output SQL for manual execution
            print(f"DB locked ({e}). Generating SQL to stdout...", file=sys.stderr)
            print(generate_sql(rows))
            print(f"\n-- {len(rows)} messages from {channel_name} ({channel_id})")
        else:
            raise


def sql_only(channel_id: str, channel_name: str, data):
    """Generate SQL to stdout without attempting DB connection.
    Use this when the MCP DuckDB server holds the lock."""
    rows = parse_messages(channel_id, channel_name, data)
    if not rows:
        print("-- No messages to insert", file=sys.stderr)
        return
    print(generate_sql(rows))
    print(f"\n-- {len(rows)} messages from {channel_name} ({channel_id})", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: slack-ingest.py <channel_id> <channel_name> [json_file] [--sql-only]", file=sys.stderr)
        print("  --sql-only: Output SQL to stdout (use when DuckDB MCP server is running)", file=sys.stderr)
        sys.exit(1)

    ch_id = sys.argv[1]
    ch_name = sys.argv[2]
    force_sql = "--sql-only" in sys.argv

    # Find the json file arg (skip flags)
    json_file = None
    for arg in sys.argv[3:]:
        if not arg.startswith("--"):
            json_file = arg
            break

    if json_file:
        with open(json_file) as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    if force_sql:
        sql_only(ch_id, ch_name, data)
    else:
        ingest(ch_id, ch_name, data)
