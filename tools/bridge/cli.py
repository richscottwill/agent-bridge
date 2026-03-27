#!/usr/bin/env python3
"""
Bridge CLI — quick commands for the agent bridge.

Usage:
    python3 cli.py poll                    # Check for pending messages targeting kiro
    python3 cli.py send <target> <subject> # Send a quick message
    python3 cli.py heartbeat              # Send heartbeat + update registry
    python3 cli.py snapshot               # Push fresh context snapshots
    python3 cli.py status                 # Show bridge status summary
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import Bridge


def poll():
    b = Bridge()
    msgs = b.poll(target='kiro', status='pending')
    if not msgs:
        print('No pending messages for kiro.')
        return
    print(f'{len(msgs)} pending message(s):')
    for m in msgs:
        print(f'  [{m["priority"]}] {m["source"]} | {m["type"]} | {m["subject"]}')
        if m.get('payload') and isinstance(m['payload'], dict):
            for k, v in m['payload'].items():
                val = str(v)[:100]
                print(f'    {k}: {val}')
        print()


def send(target, subject, payload_str='{}'):
    b = Bridge()
    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        payload = {'message': payload_str}
    msg_id = b.send(target, 'request', subject, payload)
    print(f'Sent: {msg_id}')


def heartbeat():
    b = Bridge()
    b.heartbeat('Morning routine check-in')
    print('Heartbeat sent. Registry updated.')


def status():
    b = Bridge()
    # Count messages by status
    all_msgs = b._read_sheet('bus!A:K')
    headers = all_msgs[0] if all_msgs else []
    rows = all_msgs[1:] if len(all_msgs) > 1 else []

    status_counts = {}
    for row in rows:
        while len(row) < len(headers):
            row.append('')
        s = row[8] if len(row) > 8 else 'unknown'
        status_counts[s] = status_counts.get(s, 0) + 1

    pending_for_kiro = sum(1 for r in rows if len(r) > 8 and r[8] == 'pending' and len(r) > 3 and r[3] in ('kiro', '*'))

    # Registry
    registry = b._read_sheet('registry!A:G')
    agents = registry[1:] if len(registry) > 1 else []

    # Context snapshots
    context = b._read_sheet('context!A:F')
    snapshots = context[1:] if len(context) > 1 else []

    # Files
    files = b.list_files()

    print('=== BRIDGE STATUS ===')
    print(f'Bus: {len(rows)} messages ({", ".join(f"{v} {k}" for k, v in status_counts.items())})')
    print(f'Pending for kiro: {pending_for_kiro}')
    print(f'Agents registered: {len(agents)}')
    for a in agents:
        print(f'  - {a[0]} ({a[1]}) last seen: {a[4] if len(a) > 4 else "?"}')
    print(f'Context snapshots: {len(snapshots)}')
    print(f'Drive files: {len(files)}')
    for f in files:
        print(f'  - {f["name"]} ({f["mimeType"][:40]})')


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]
    if cmd == 'poll':
        poll()
    elif cmd == 'send':
        if len(sys.argv) < 4:
            print('Usage: cli.py send <target> <subject> [payload_json]')
            return
        payload = sys.argv[4] if len(sys.argv) > 4 else '{}'
        send(sys.argv[2], sys.argv[3], payload)
    elif cmd == 'heartbeat':
        heartbeat()
    elif cmd == 'snapshot':
        print('Use bridge.py directly for full snapshots. This CLI is for quick ops.')
    elif cmd == 'status':
        status()
    else:
        print(f'Unknown command: {cmd}')
        print(__doc__)


if __name__ == '__main__':
    main()
