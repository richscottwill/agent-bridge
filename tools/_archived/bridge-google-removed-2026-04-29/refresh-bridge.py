#!/usr/bin/env python3
"""Refresh bridge: push fresh context, clean stale heartbeats, send swarm nudge."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import Bridge

b = Bridge()
SSID = '1IlM43kzxw8Vlu6aUWXUV1dr7ZIF7O7H2bD5x3kaKIHg'

# --- 1. Auto-complete old heartbeat messages ---
rows = b._read_sheet('bus!A:K')
headers = rows[0]
cleaned = 0
for i, row in enumerate(rows[1:], start=2):
    while len(row) < len(headers):
        row.append('')
    msg = dict(zip(headers, row))
    # Complete heartbeats and old announces that are still pending
    if msg.get('status') == 'pending' and msg.get('type') in ('heartbeat', 'announce'):
        b.sheets.spreadsheets().values().update(
            spreadsheetId=SSID,
            range=f'bus!I{i}',
            valueInputOption='RAW',
            body={'values': [['complete']]}
        ).execute()
        cleaned += 1
print(f'Cleaned {cleaned} stale heartbeat/announce messages')

# --- 2. Push fresh context snapshots ---
b.push_context('brain', 
    'Strategic priorities: 5 Levels (L1 struggling - 0 streak, 10 workdays stalled). '
    'Testing Approach doc for Kate Apr 16 is THE hard thing. '
    'Annual Review: Meets High Bar, #1 gap is visibility. '
    'Level 1 gate: 4 consecutive weeks with artifact shipped. Current: 0.',
    {'hard_thing': 'Testing Approach doc', 'kate_meeting': '2026-04-16', 
     'streak': 0, 'days_stalled': 10, 'level': '1 - struggling'})
print('Pushed brain context')

b.push_context('amcc',
    'Streak: 0 days. 10 workdays since hard thing set (3/20). '
    'Hard thing: Testing Approach doc for Kate. '
    'Resistance: blank page paralysis + comfort zone gravity. '
    'W13 was another zero week. Monday 3/30 has 90 min Core window.',
    {'streak': 0, 'days_stalled': 10, 'hard_thing': 'Testing Approach doc',
     'resistance': 'blank page paralysis', 'core_window': '90 min'})
print('Pushed amcc context')

b.push_context('hands',
    'P0: Testing Approach doc (NOT STARTED, Apr 16). '
    'P1: Baloo keyword blurb (due TODAY), Lorena Q2 spend (5d overdue), '
    'Polaris timeline (overdue), AI Max test design (2d overdue). '
    'P2: Flash topics (13d overdue), PAM R&O (20d overdue). '
    '8 overdue items total. 2 meetings today. 4 focus blocks created.',
    {'overdue_count': 8, 'meetings_today': 2, 'focus_blocks': 4,
     'p0': 'Testing Approach doc', 'due_today': ['Baloo blurb', 'Lorena Q2 spend', 'Flash assembly']})
print('Pushed hands context')

b.push_context('eyes',
    'US: 32.9K regs (+16% OP2, +68% YoY), $83 CPA. '
    'AU: 1.1K regs (-1% OP2), ~$140 CPA target, Polaris migration completing. '
    'MX: 1.1K regs (+32% OP2, +37% YoY), Lorena is new PS stakeholder. '
    'Polaris weblab: Vijeth created PS Brand header all markets except US. Dial-up Apr 6-7.',
    {'us_regs': '32.9K', 'au_regs': '1.1K', 'mx_regs': '1.1K',
     'weblab_status': 'header created, scoping in progress', 'weblab_target': 'Apr 6-7'})
print('Pushed eyes context')

b.push_context('memory',
    'Key relationships: Brandon (L7 mgr, she/her, Austin), Kate (L8 skip, Apr 16 meeting), '
    'Lorena (new MX PS stakeholder, needs Q2 spend + keyword data), '
    'Alexis (AU POC, Polaris migration), Vijay Kumar (Baloo tech, early access launching today). '
    'Lorena replies 5 and 11 days overdue. Two drafts ready in Outlook.',
    {'overdue_replies': ['Lorena - Q2 spend', 'Lorena - keyword data'],
     'key_meeting': 'Kate Apr 16', 'new_stakeholder': 'Lorena (MX)'})
print('Pushed memory context')

# --- 3. Send heartbeat ---
b.heartbeat('Monday morning routine complete. Protocol sheet added. Context refreshed.')
print('Heartbeat sent')

# --- 4. Send nudge to swarm ---
b.send('swarm', 'request', 'Read the new protocol tab — it explains how to use this bridge', {
    'action': 'Open the protocol tab (first tab in this spreadsheet). Read it top to bottom. Then register yourself in the registry tab. Then check pending requests.',
    'new_since_last': 'Protocol tab added with full onboarding instructions. Context snapshots refreshed. Stale messages cleaned.',
    'priority_request': 'The Testing Approach doc draft you sent (kiro-006 response) was received. Next: Kiro needs competitive intelligence on B2B paid search benchmarks for AU market. Check pending requests.'
}, priority='high')
print('Swarm nudge sent')

print('\nDone. Bridge refreshed.')
