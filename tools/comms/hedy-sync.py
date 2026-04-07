#!/usr/bin/env python3
"""
Hedy Session Sync — Pulls new meeting sessions from Hedy API,
analyzes Richard's communication patterns, and outputs a summary
for context file updates.

Usage:
  python3 hedy-sync.py [--since YYYY-MM-DD] [--latest N]  # new sessions only
  python3 hedy-sync.py --resync                            # re-check all for updated speaker labels
  python3 hedy-sync.py --all                               # process everything

Default: pulls sessions newer than the last sync timestamp.
Resync: re-fetches previously processed sessions and checks if speaker labels
        or cleaned transcripts were updated since last pull. Useful when you
        update speaker names in Hedy after the initial recording.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

API_BASE = "https://api.hedy.bot"
API_KEY = os.environ.get("HEDY_API_KEY", "hedy_live_7qBVLetBrufPoWgrge-fYwL2yxvBMsQc")
STATE_FILE = Path(os.path.expanduser("~/shared/tools/.hedy-last-sync"))
PROCESSED_FILE = Path(os.path.expanduser("~/shared/tools/.hedy-processed"))
OUTPUT_DIR = Path(os.path.expanduser("~/shared/context/intake"))


def api_get(path):
    """Make authenticated GET request to Hedy API."""
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"API error {e.code}: {e.read().decode()}", file=sys.stderr)
        return None


def get_last_sync():
    """Read last sync timestamp."""
    if STATE_FILE.exists():
        return STATE_FILE.read_text().strip()
    return None


def save_last_sync(ts):
    """Save current sync timestamp."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(ts)


def load_processed():
    """Load dict of processed sessions: {session_id: {has_speakers: bool, cleaned_at: str}}."""
    if PROCESSED_FILE.exists():
        try:
            return json.loads(PROCESSED_FILE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_processed(processed):
    """Save processed sessions state."""
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED_FILE.write_text(json.dumps(processed, indent=2))


def has_named_speakers(cleaned_transcript):
    """Check if transcript has real speaker names (not 'Speaker 1', 'Speaker 2')."""
    if not cleaned_transcript:
        return False
    for line in cleaned_transcript.split("\n")[:20]:
        line = line.strip()
        if line and ":" in line[:30]:
            speaker = line.split(":")[0].strip()
            if speaker and not speaker.startswith("Speaker ") and len(speaker) < 25:
                return True
    return False


def needs_resync(session_id, detail, processed):
    """Check if a previously processed session should be re-analyzed.
    Returns True if:
    - Session was processed without speaker labels but now has them
    - Session's cleaned_at timestamp is newer than when we last processed it
    """
    if session_id not in processed:
        return True  # Never processed

    prev = processed[session_id]
    ct = detail.get("cleaned_transcript", "") if detail else ""
    cleaned_at = detail.get("cleaned_at", "") if detail else ""

    # Previously had no speakers, now has named speakers
    if not prev.get("has_speakers") and has_named_speakers(ct):
        print(f"    ↻ Re-syncing: speaker labels added since last pull")
        return True

    # Transcript was re-cleaned since we last processed
    if cleaned_at and cleaned_at > prev.get("cleaned_at", ""):
        print(f"    ↻ Re-syncing: transcript updated (cleaned_at changed)")
        return True

    return False


def get_sessions():
    """Fetch all sessions from Hedy."""
    data = api_get("/sessions")
    if data and data.get("success"):
        return data.get("data", [])
    return []


def get_session_detail(session_id):
    """Fetch full session detail including transcript."""
    return api_get(f"/sessions/{session_id}")


def extract_speaker_turns(cleaned_transcript):
    """Extract speaking turns by speaker from cleaned transcript."""
    if not cleaned_transcript:
        return {}
    speakers = {}
    current_speaker = None
    current_text = ""
    for line in cleaned_transcript.split("\n"):
        line = line.strip()
        if not line:
            continue
        if ":" in line[:30]:
            parts = line.split(":", 1)
            if len(parts[0]) < 25:
                if current_speaker and current_text:
                    if current_speaker not in speakers:
                        speakers[current_speaker] = []
                    speakers[current_speaker].append(current_text.strip())
                current_speaker = parts[0].strip()
                current_text = parts[1].strip() + " "
                continue
        current_text += line + " "
    if current_speaker and current_text:
        if current_speaker not in speakers:
            speakers[current_speaker] = []
        speakers[current_speaker].append(current_text.strip())
    return speakers


def analyze_richard(speakers):
    """Analyze Richard's communication patterns in a session."""
    richard_key = None
    for k in speakers:
        if "richard" in k.lower():
            richard_key = k
            break
    if not richard_key:
        return None

    turns = speakers[richard_key]
    total_turns = sum(len(v) for v in speakers.values())
    richard_turns = len(turns)

    # Count filler/hedging
    hedges = 0
    fillers = 0
    for t in turns:
        lower = t.lower()
        hedges += lower.count("i think") + lower.count("i don't know") + lower.count("kind of")
        fillers += lower.count("like, ") + lower.count("you know") + lower.count("sort of")

    # Average turn length
    avg_words = sum(len(t.split()) for t in turns) / max(len(turns), 1)

    # Short turns (< 5 words)
    short_turns = sum(1 for t in turns if len(t.split()) < 5)

    return {
        "richard_turns": richard_turns,
        "total_turns": total_turns,
        "share_pct": round(richard_turns / max(total_turns, 1) * 100, 1),
        "hedges": hedges,
        "fillers": fillers,
        "avg_words_per_turn": round(avg_words, 1),
        "short_turns": short_turns,
        "short_turn_pct": round(short_turns / max(richard_turns, 1) * 100, 1),
        "other_speakers": {k: len(v) for k, v in speakers.items() if k != richard_key}
    }


def format_session_summary(session, detail, analysis):
    """Format a session summary for output."""
    lines = []
    title = session.get("title", "Untitled")
    date = session.get("startTime", "")[:10]
    duration = session.get("duration", 0)
    topic = session.get("topic", {}).get("name", "none")

    lines.append(f"## {title}")
    lines.append(f"Date: {date} | Duration: {duration}min | Topic: {topic}")
    lines.append("")

    if detail:
        recap = detail.get("recap", "")
        if recap:
            lines.append(f"### Recap")
            lines.append(recap[:500])
            lines.append("")

        todos = detail.get("user_todos", [])
        if todos:
            lines.append("### Action Items")
            for t in todos[:5]:
                status = "x" if t.get("completed") else " "
                lines.append(f"- [{status}] {t.get('text', '')} (due: {t.get('dueDate', '?')})")
            lines.append("")

    if analysis:
        lines.append("### Richard's Communication")
        lines.append(f"- Turns: {analysis['richard_turns']}/{analysis['total_turns']} ({analysis['share_pct']}%)")
        lines.append(f"- Avg words/turn: {analysis['avg_words_per_turn']}")
        lines.append(f"- Short turns (<5 words): {analysis['short_turns']} ({analysis['short_turn_pct']}%)")
        lines.append(f"- Hedges ('I think', 'I don't know', 'kind of'): {analysis['hedges']}")
        lines.append(f"- Fillers ('like', 'you know', 'sort of'): {analysis['fillers']}")
        if analysis['other_speakers']:
            others = ", ".join(f"{k}: {v}" for k, v in analysis['other_speakers'].items())
            lines.append(f"- Other speakers: {others}")
        lines.append("")

        # Quick assessment
        if analysis['share_pct'] < 15 and analysis['total_turns'] > 20:
            lines.append("⚠️ LOW VISIBILITY — Richard spoke less than 15% of the time in a multi-person meeting.")
        if analysis['hedges'] > 5:
            lines.append("⚠️ HEDGING — High hedge count. Practice declarative statements.")
        if analysis['short_turn_pct'] > 50:
            lines.append("⚠️ PASSIVE — Over half of Richard's turns were under 5 words.")
        lines.append("")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Sync Hedy meeting data")
    parser.add_argument("--since", help="Only sessions after this date (YYYY-MM-DD)")
    parser.add_argument("--latest", type=int, default=5, help="Number of latest sessions to process")
    parser.add_argument("--all", action="store_true", help="Process all sessions")
    parser.add_argument("--resync", action="store_true", help="Re-check all previously processed sessions for updated speaker labels")
    args = parser.parse_args()

    last_sync = args.since or get_last_sync()
    sessions = get_sessions()
    processed = load_processed()

    if not sessions:
        print("No sessions found.")
        return

    # Build list of sessions to process
    to_process = []

    if args.resync:
        # Re-check ALL sessions for updated transcripts/speaker labels
        print(f"Resync mode: checking {len(sessions)} sessions for updated speaker labels...")
        for session in sessions:
            sid = session["sessionId"]
            detail = get_session_detail(sid)
            if needs_resync(sid, detail, processed):
                to_process.append((session, detail))
            else:
                print(f"  ✓ {session.get('title', 'Untitled')[:50]} — no changes")
        if not to_process:
            print("All sessions up to date. No re-syncing needed.")
            return
    else:
        # Normal mode: new sessions only
        if last_sync and not args.all:
            sessions = [s for s in sessions if s.get("startTime", "") > last_sync]

        if not sessions:
            print(f"No new sessions since {last_sync}.")
            return

        if not args.all:
            sessions = sessions[:args.latest]

        # Pre-fetch details and check for resync opportunities on recent sessions
        for session in sessions:
            detail = get_session_detail(session["sessionId"])
            to_process.append((session, detail))

    print(f"Processing {len(to_process)} session(s)...")

    output_lines = [
        f"# Hedy Session Sync — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"Sessions processed: {len(to_process)}",
        f"Mode: {'resync' if args.resync else 'normal'}",
        ""
    ]

    for session, detail in to_process:
        sid = session["sessionId"]
        print(f"  → {session.get('title', 'Untitled')} ({sid[:8]}...)")

        ct = detail.get("cleaned_transcript", "") if detail else ""
        speakers = extract_speaker_turns(ct)
        analysis = analyze_richard(speakers)

        summary = format_session_summary(session, detail, analysis)
        output_lines.append(summary)
        output_lines.append("---")
        output_lines.append("")

        # Track what we processed
        processed[sid] = {
            "has_speakers": has_named_speakers(ct),
            "cleaned_at": detail.get("cleaned_at", "") if detail else "",
            "last_synced": datetime.now(timezone.utc).isoformat(),
            "had_richard": analysis is not None
        }

    # Save output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts_suffix = datetime.now().strftime('%Y-%m-%d-%H%M')
    outfile = OUTPUT_DIR / f"hedy-sync-{ts_suffix}.md"
    outfile.write_text("\n".join(output_lines))
    print(f"\nOutput saved to {outfile}")

    # Save processed state
    save_processed(processed)

    # Update last sync timestamp (only in normal mode)
    if not args.resync and to_process:
        latest_ts = max(s.get("startTime", "") for s, _ in to_process)
        save_last_sync(latest_ts)
        print(f"Last sync updated to {latest_ts}")


if __name__ == "__main__":
    main()
