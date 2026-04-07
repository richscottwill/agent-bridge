#!/usr/bin/env python3
"""
Hedy Meeting Prep — Pushes meeting-specific context into Hedy topic contexts
before meetings, so Hedy's real-time coaching is targeted.

Usage:
  python3 hedy-meeting-prep.py                    # prep all meetings in next 24h
  python3 hedy-meeting-prep.py --topic "AU"       # prep a specific topic
  python3 hedy-meeting-prep.py --dry-run           # show what would be pushed without updating

Reads from: memory.md (relationship graph, meeting briefs), current.md (active projects),
            hands.md (pending actions), eyes.md (metrics), nervous-system.md (communication scores)
Writes to:  Hedy topic contexts via PATCH /topics/{id}
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

API_BASE = "https://api.hedy.bot"
API_KEY = os.environ.get("HEDY_API_KEY", "hedy_live_7qBVLetBrufPoWgrge-fYwL2yxvBMsQc")


def api_get(path):
    req = urllib.request.Request(f"{API_BASE}{path}", headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"API error {e.code}: {e.read().decode()}", file=sys.stderr)
        return None


def api_patch(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(f"{API_BASE}{path}", data=body, method="PATCH", headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"API error {e.code}: {e.read().decode()}", file=sys.stderr)
        return None


def get_topics():
    data = api_get("/topics")
    if data and data.get("success"):
        return {t["name"]: t for t in data.get("data", [])}
    return {}


def read_file_safe(path):
    p = Path(os.path.expanduser(path))
    if p.exists():
        return p.read_text()
    return ""


def build_prep_context(topic_name, topic_data, memory, current, hands):
    """Build meeting-specific prep context from system files."""
    lines = []

    # Get the last session recap for this topic
    overview = topic_data.get("overview", {})
    prep_note = overview.get("prepNote", {}) if overview else {}

    # Build prep based on topic name
    lines.append(f"MEETING PREP for {topic_name} — auto-generated before this session.")
    lines.append("")

    # Extract relevant relationship info from memory
    # Simple keyword matching against the topic name and known attendees
    topic_lower = topic_name.lower()

    # Map topics to key people for targeted prep
    topic_people = {
        "au": ["Alexis Eck", "Lena Zak"],
        "mx": ["Carlos Palmos", "Lorena Alvarez"],
        "brandon sync": ["Brandon Munday"],
        "adi sync": ["Adi", "Aditya"],
        "andrew sync": ["Andrew Wirtz"],
        "yun sync": ["Yun-Kang Chu"],
        "weekly meeting": ["Brandon", "Andrew", "Stacey", "Yun", "Adi", "Peter", "Dwayne"],
        "pam": ["Peter Ocampo", "Andrew Wirtz"],
        "oci": ["Stacey Gu"],
        "activation": ["Fernando", "Nishan", "Mauro", "Yun"],
    }

    people = topic_people.get(topic_lower, [])
    if people:
        lines.append(f"KEY PEOPLE IN THIS MEETING: {', '.join(people)}")
        lines.append("")

    # Extract pending actions relevant to this topic from hands/current
    lines.append("WHAT RICHARD SHOULD BRING UP:")
    action_count = 0
    for keyword in [topic_lower] + [p.lower().split()[0] for p in people]:
        for line in current.split("\n"):
            if keyword in line.lower() and ("- [" in line or "action" in line.lower()):
                lines.append(f"  • {line.strip().lstrip('- [] ')}")
                action_count += 1
                if action_count >= 5:
                    break
        if action_count >= 5:
            break

    if action_count == 0:
        lines.append("  • (No specific pending actions found — review hands.md)")
    lines.append("")

    # Communication coaching reminder based on meeting type
    if topic_lower == "weekly meeting":
        lines.append("COMMUNICATION GOAL: This is Richard's main visibility gap. Prepare 2-3 strategic points and deliver them. Don't let Andrew and Stacey dominate. Aim for at least one strategic contribution.")
    elif topic_lower == "brandon sync":
        lines.append("COMMUNICATION GOAL: Drive the agenda with recommendations, not just status updates. Bring one strategic framing or proposal.")
    elif topic_lower in ["adi sync"]:
        lines.append("COMMUNICATION GOAL: This is where Richard excels — teaching and mentoring. Document any frameworks explained for reuse.")
    elif topic_lower in ["au"]:
        lines.append("COMMUNICATION GOAL: Lena expects data. Have AU metrics loaded. Answer her actual question directly before adding context.")
    elif topic_lower in ["mx"]:
        lines.append("COMMUNICATION GOAL: Richard is strong here. Stay solution-oriented. Look for cross-market insights to share.")
    else:
        lines.append("COMMUNICATION GOAL: Be useful. One strategic contribution. Close with clear commitments.")

    lines.append("")
    lines.append("CLOSE THE MEETING WITH: 'So to confirm — [commitments]. Anything I'm missing?'")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Push meeting prep to Hedy topics")
    parser.add_argument("--topic", help="Prep a specific topic by name")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be pushed")
    parser.add_argument("--all", action="store_true", help="Prep all topics with sessions")
    args = parser.parse_args()

    # Load system context
    memory = read_file_safe("~/shared/context/body/memory.md")
    current = read_file_safe("~/shared/context/active/current.md")
    hands = read_file_safe("~/shared/context/body/hands.md")

    # Get Hedy topics
    topics = get_topics()
    if not topics:
        print("No topics found.")
        return

    # Filter topics to prep
    if args.topic:
        matching = {k: v for k, v in topics.items() if args.topic.lower() in k.lower()}
        if not matching:
            print(f"No topic matching '{args.topic}'. Available: {', '.join(topics.keys())}")
            return
    elif args.all:
        matching = {k: v for k, v in topics.items() if v.get("sessionCount", 0) > 0}
    else:
        # Default: prep topics that have sessions
        matching = {k: v for k, v in topics.items() if v.get("sessionCount", 0) > 0}

    for name, topic in matching.items():
        prep = build_prep_context(name, topic, memory, current, hands)
        existing_ctx = topic.get("topicContext", "") or ""

        # Preserve the base topic context, append prep
        # Split on MEETING PREP marker if it exists from a previous run
        if "MEETING PREP for" in existing_ctx:
            base_ctx = existing_ctx.split("MEETING PREP for")[0].rstrip()
        else:
            base_ctx = existing_ctx

        new_ctx = f"{base_ctx}\n\n{prep}" if base_ctx else prep

        if args.dry_run:
            print(f"\n=== {name} ===")
            print(prep)
            print(f"(Would update topic {topic['id']})")
        else:
            result = api_patch(f"/topics/{topic['id']}", {"topicContext": new_ctx})
            if result and result.get("success"):
                print(f"  ✓ {name}")
            else:
                print(f"  ✗ {name} — update failed")

    if not args.dry_run:
        print(f"\nPrepped {len(matching)} topic(s).")


if __name__ == "__main__":
    main()
