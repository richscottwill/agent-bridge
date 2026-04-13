#!/usr/bin/env python3
"""
Slack Channel History → DuckDB Bulk Ingester (v2 — Thread-Aware)

Usage:
  python3 slack-ingest.py <channel_id> <channel_name> < history.json
  python3 slack-ingest.py <channel_id> <channel_name> history.json
  python3 slack-ingest.py <channel_id> <channel_name> history.json --sql-only
  python3 slack-ingest.py <channel_id> <channel_name> history.json --threads-sql

Modes:
  (default)     Parse channel history JSON → insert into slack_messages via DuckDB.
  --sql-only    Output INSERT SQL to stdout (for MCP execution when DB is locked).
  --threads-sql Output thread-fetch commands to stdout. The AM-Backend agent reads
                these and calls batch_get_thread_replies for each, then pipes the
                results back through this script with --thread-replies mode.
  --thread-replies <parent_ts>
                Parse thread reply JSON (from batch_get_thread_replies) and insert
                into slack_messages with proper thread_ts linkage.

Thread Architecture:
  - All messages (top-level AND thread replies) live in slack_messages.
  - thread_ts links replies to their parent message (parent's ts = thread_ts).
  - is_thread_reply = TRUE for replies, FALSE for parents.
  - slack_threads is a VIEW computed from slack_messages (not a separate table).
  - Thread detection: any message with reply_count > 0 is a thread parent.
    During ingestion, we output the list of thread parents so the calling agent
    can fetch replies via batch_get_thread_replies MCP tool.

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


def mentions_richard(text: str) -> bool:
    """Check if message @mentions Richard."""
    return RICHARD_ID in text


def process_messages(messages: list, channel_id: str, channel_name: str,
                     force_thread_ts: str = None) -> tuple[list, list]:
    """Convert raw Slack messages into rows for slack_messages table.
    
    Returns:
        (rows, thread_parents) where thread_parents is a list of
        (channel_id, thread_ts, reply_count) for threads needing fetch.
    """
    rows = []
    thread_parents = []
    
    for msg in messages:
        if msg.get("subtype") in ("channel_join", "channel_leave", "channel_topic",
                                    "channel_purpose", "tabbed_canvas_updated"):
            continue

        ts = msg.get("ts")
        if not ts:
            continue

        text = extract_text(msg)
        if not text or len(text.strip()) == 0:
            continue

        author_id = msg.get("user", "")
        up = msg.get("user_profile", {})
        author_alias = up.get("name") or up.get("display_name") or ""
        author_name = up.get("real_name") or ""

        # Thread linkage:
        # - If force_thread_ts is set, we're ingesting thread replies
        #   and the parent ts is force_thread_ts.
        # - Otherwise, use Slack's thread_ts field.
        thread_ts = force_thread_ts or msg.get("thread_ts")
        
        # A message is a reply if its thread_ts differs from its own ts
        # OR if we're forcing thread_ts (thread reply ingestion mode)
        if force_thread_ts:
            is_reply = (ts != force_thread_ts)  # parent message appears in its own thread
        else:
            is_reply = thread_ts is not None and thread_ts != ts
        
        reply_count = msg.get("reply_count", 0)
        reaction_count = sum(r.get("count", 0) for r in msg.get("reactions", []))
        is_richard = author_id == RICHARD_ID
        richard_reacted = has_richard_reaction(msg)
        richard_mentioned = mentions_richard(text)

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
            is_richard,
            is_reply,
            reply_count,
            reaction_count,
            richard_reacted,
            richard_mentioned,
            classify_signal(text),
        ))
        
        # Track thread parents for subsequent thread fetch
        # Any message with replies is a thread parent
        if reply_count > 0 and not force_thread_ts:
            thread_parents.append((channel_id, ts, reply_count))
    
    return rows, thread_parents


def parse_messages(channel_id: str, channel_name: str, data,
                   force_thread_ts: str = None) -> tuple[list, list]:
    """Parse raw Slack API response into insertable rows.
    
    Returns (rows, thread_parents).
    """
    if isinstance(data, list):
        messages = []
        # batch_get_thread_replies format: list of {slackUrl/channelId+threadTs, result: {messages}}
        # batch_get_conversation_history format: list of {channelId, result: {messages}}
        for item in data:
            if isinstance(item, dict):
                result = item.get("result", {})
                msgs = result.get("messages", [])
                if msgs:
                    messages.extend(msgs)
                    break
        if not messages and data:
            first = data[0] if data else {}
            messages = first.get("result", {}).get("messages", [])
    elif isinstance(data, dict):
        messages = data.get("messages", [])
    else:
        return [], []

    return process_messages(messages, channel_id, channel_name, force_thread_ts)


def esc(s) -> str:
    """Escape a value for SQL insertion."""
    if s is None:
        return "NULL"
    return "'" + str(s).replace("'", "''") + "'"


def generate_sql(rows: list) -> str:
    """Generate SQL INSERT statements in batches of 25."""
    if not rows:
        return ""

    output = []
    for i in range(0, len(rows), 25):
        batch = rows[i:i+25]
        values = []
        for r in batch:
            (ts, ch_id, ch_name, thread_ts, author_id, alias, name,
             preview, text, is_r, is_reply, replies, reactions,
             r_reacted, r_mentioned, signal) = r
            
            thread_val = esc(thread_ts) if thread_ts else "NULL"
            signal_val = esc(signal) if signal else "NULL"
            values.append(
                f"({esc(ts)}, {esc(ch_id)}, {esc(ch_name)}, {thread_val}, "
                f"{esc(author_id)}, {esc(alias)}, {esc(name)}, "
                f"{esc(preview[:200])}, {esc(text[:2000])}, "
                f"{'TRUE' if is_r else 'FALSE'}, {'TRUE' if is_reply else 'FALSE'}, "
                f"{replies}, {reactions}, {'TRUE' if r_reacted else 'FALSE'}, "
                f"{'TRUE' if r_mentioned else 'FALSE'}, "
                f"{signal_val}, current_timestamp)"
            )
        sql = ("INSERT OR REPLACE INTO signals.slack_messages "
               "(ts, channel_id, channel_name, thread_ts, author_id, author_alias, author_name, "
               "text_preview, full_text, is_richard, is_thread_reply, reply_count, "
               "reaction_count, richard_reacted, richard_mentioned, signal_type, ingested_at) VALUES\n"
               + ",\n".join(values))
        output.append(sql)

    return ";\n".join(output)


def generate_thread_fetch_commands(thread_parents: list) -> str:
    """Output JSON list of threads to fetch.
    
    The AM-Backend agent reads this and calls batch_get_thread_replies
    for each entry, then pipes results back through --thread-replies mode.
    """
    commands = []
    for channel_id, thread_ts, reply_count in thread_parents:
        commands.append({
            "channelId": channel_id,
            "threadTs": thread_ts,
            "replyCount": reply_count
        })
    return json.dumps(commands, indent=2)


def ingest(channel_id: str, channel_name: str, data, force_thread_ts: str = None):
    """Main ingestion: parse messages and bulk-insert into DuckDB."""
    rows, thread_parents = parse_messages(channel_id, channel_name, data, force_thread_ts)
    if not rows:
        print("No messages to insert", file=sys.stderr)
        return thread_parents

    try:
        con = duckdb.connect(str(DB_PATH))
        con.executemany(
            """INSERT OR REPLACE INTO signals.slack_messages
               (ts, channel_id, channel_name, thread_ts, author_id, author_alias, author_name,
                text_preview, full_text, is_richard, is_thread_reply, reply_count,
                reaction_count, richard_reacted, richard_mentioned, signal_type, ingested_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, current_timestamp)""",
            rows
        )

        # Update slack_people
        author_ids = set()
        for row in rows:
            aid = row[4]
            if aid and aid not in author_ids:
                author_ids.add(aid)
                alias = row[5]
                name = row[6]
                if alias or name:
                    con.execute(
                        """INSERT INTO signals.slack_people (user_id, alias, display_name, total_messages, ingested_at)
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
        mode = "thread replies" if force_thread_ts else "messages"
        print(f"Inserted {len(rows)} {mode} from {channel_name} ({channel_id})", file=sys.stderr)

    except Exception as e:
        if "lock" in str(e).lower():
            print(f"DB locked ({e}). Generating SQL to stdout...", file=sys.stderr)
            print(generate_sql(rows))
            print(f"\n-- {len(rows)} messages from {channel_name} ({channel_id})")
        else:
            raise

    return thread_parents


def sql_only(channel_id: str, channel_name: str, data, force_thread_ts: str = None):
    """Generate SQL to stdout without DB connection."""
    rows, thread_parents = parse_messages(channel_id, channel_name, data, force_thread_ts)
    if not rows:
        print("-- No messages to insert", file=sys.stderr)
        return thread_parents
    print(generate_sql(rows))
    mode = "thread replies" if force_thread_ts else "messages"
    print(f"\n-- {len(rows)} {mode} from {channel_name} ({channel_id})", file=sys.stderr)
    return thread_parents


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: slack-ingest.py <channel_id> <channel_name> [json_file] [options]", file=sys.stderr)
        print("Options:", file=sys.stderr)
        print("  --sql-only              Output SQL to stdout", file=sys.stderr)
        print("  --threads-sql           Output thread fetch commands as JSON", file=sys.stderr)
        print("  --thread-replies <ts>   Ingest thread replies (ts = parent message ts)", file=sys.stderr)
        sys.exit(1)

    ch_id = sys.argv[1]
    ch_name = sys.argv[2]
    force_sql = "--sql-only" in sys.argv
    threads_sql = "--threads-sql" in sys.argv
    
    # Parse --thread-replies <parent_ts>
    force_thread_ts = None
    if "--thread-replies" in sys.argv:
        idx = sys.argv.index("--thread-replies")
        if idx + 1 < len(sys.argv):
            force_thread_ts = sys.argv[idx + 1]
        else:
            print("--thread-replies requires a parent timestamp argument", file=sys.stderr)
            sys.exit(1)

    # Find the json file arg (skip flags and their values)
    json_file = None
    skip_next = False
    for arg in sys.argv[3:]:
        if skip_next:
            skip_next = False
            continue
        if arg == "--thread-replies":
            skip_next = True
            continue
        if not arg.startswith("--"):
            json_file = arg
            break

    if json_file:
        with open(json_file) as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    if threads_sql:
        # Just output the thread parents that need fetching
        _, thread_parents = parse_messages(ch_id, ch_name, data)
        print(generate_thread_fetch_commands(thread_parents))
        print(f"-- {len(thread_parents)} threads to fetch", file=sys.stderr)
    elif force_sql:
        sql_only(ch_id, ch_name, data, force_thread_ts)
    else:
        thread_parents = ingest(ch_id, ch_name, data, force_thread_ts)
        if thread_parents and not force_thread_ts:
            print(f"\n{len(thread_parents)} threads need reply fetching. "
                  f"Run with --threads-sql to get fetch commands.", file=sys.stderr)
