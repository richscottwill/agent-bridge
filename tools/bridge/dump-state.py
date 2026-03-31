#!/usr/bin/env python3
"""Dump full bridge state: bus messages, context snapshots, registry."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import Bridge

b = Bridge()

rows = b._read_sheet('bus!A:K')
headers = rows[0]
print('=== BUS MESSAGES ===')
for row in rows[1:]:
    while len(row) < len(headers):
        row.append('')
    msg = dict(zip(headers, row))
    status = msg.get('status', '?')
    source = msg.get('source', '?')
    target = msg.get('target', '?')
    mtype = msg.get('type', '?')
    pri = msg.get('priority', '?')
    subj = msg.get('subject', '')[:80]
    resp = msg.get('response_to', '')
    line = f'[{status:8s}] {source:15s} -> {target:10s} | {mtype:14s} | {pri:6s} | {subj}'
    if resp:
        line += f'  (re: {resp})'
    print(line)

print()
print('=== CONTEXT SNAPSHOTS ===')
ctx = b._read_sheet('context!A:F')
if len(ctx) > 1:
    ch = ctx[0]
    for row in ctx[1:]:
        while len(row) < len(ch):
            row.append('')
        snap = dict(zip(ch, row))
        organ = snap.get('organ', '?')
        ts = snap.get('timestamp', '?')
        summary = snap.get('summary', '')[:100]
        print(f'[{organ}] {ts} | {summary}')
else:
    print('(none)')

print()
print('=== REGISTRY ===')
reg = b._read_sheet('registry!A:G')
if len(reg) > 1:
    rh = reg[0]
    for row in reg[1:]:
        while len(row) < len(rh):
            row.append('')
        agent = dict(zip(rh, row))
        aid = agent.get('agent_id', '?')
        plat = agent.get('platform', '?')
        st = agent.get('status', '?')
        ls = agent.get('last_seen', '?')
        print(f'{aid} | {plat} | status: {st} | last_seen: {ls}')
else:
    print('(none)')
