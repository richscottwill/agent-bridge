#!/usr/bin/env python3
"""Add Richard action items to the requests tab."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import Bridge

b = Bridge()

now = b._now()

actions = [
    {
        'req_id': 'req-004',
        'timestamp': now,
        'source': 'kiro',
        'type': 'script_update',
        'name': 'Deploy apps-script-code.js (NOT Code.gs)',
        'location': 'agent bridge script (Apps Script editor)',
        'purpose': 'apps-script-code.js is the more complete version — has streak tracker (A4), weekly digest (A5), and form router with streak logic. Code.gs is a simpler subset missing these features. Replace the current script content with apps-script-code.js, then run setupTriggers() once. This is the single most important bridge action — without it, all Google-side automation is dead.',
        'status': 'pending',
        'notes': 'HIGH PRIORITY. Steps: (1) Open Apps Script editor for agent bridge script. (2) Delete existing Code.gs content. (3) Paste full content of ~/shared/tools/bridge/apps-script-code.js. (4) Run setupTriggers(). (5) Run setupFormTrigger(). (6) Verify triggers created in Triggers panel.'
    },
    {
        'req_id': 'req-005',
        'timestamp': now,
        'source': 'kiro',
        'type': 'script_update',
        'name': 'Add error handling wrapper to Apps Script',
        'location': 'agent bridge script (Apps Script editor)',
        'purpose': 'All Apps Script functions have zero try/catch. If a sheet is renamed, a column is missing, or JSON is malformed, triggers silently fail. Add a log sheet and wrap each function. Without this, you will never know when automation breaks.',
        'status': 'pending',
        'notes': 'Do AFTER req-004. Steps: (1) Create a "log" sheet in the spreadsheet (if not exists) with columns: timestamp, function, message, error. (2) In Apps Script, wrap each triggered function: function safePollBus(){ try{ pollBus() }catch(e){ getSheet("log").appendRow([now(),"pollBus","error",e.message]) } }. (3) Update setupTriggers() to use the safe* wrappers instead of the raw functions.'
    },
    {
        'req_id': 'req-006',
        'timestamp': now,
        'source': 'kiro',
        'type': 'config',
        'name': 'Set RICHARD_EMAIL in Apps Script CONFIG',
        'location': 'agent bridge script > Config section',
        'purpose': 'The RICHARD_EMAIL field in apps-script-code.js CONFIG is empty string. Without it, urgent bus message email alerts and file request notifications will not send. Set it to your preferred email.',
        'status': 'pending',
        'notes': 'Do DURING req-004. In the CONFIG object at the top of the script, set RICHARD_EMAIL to your email address.'
    },
    {
        'req_id': 'req-007',
        'timestamp': now,
        'source': 'kiro',
        'type': 'cleanup',
        'name': 'Consolidate Code.gs and apps-script-code.js',
        'location': '~/shared/tools/bridge/',
        'purpose': 'Two conflicting Apps Script files exist locally. After deploying apps-script-code.js (req-004), delete or rename Code.gs to Code.gs.deprecated to prevent future confusion about which version is canonical.',
        'status': 'pending',
        'notes': 'Do AFTER req-004 is confirmed working. Low priority — just housekeeping.'
    },
]

for action in actions:
    row = [
        action['req_id'], action['timestamp'], action['source'],
        action['type'], action['name'], action['location'],
        action['purpose'], action['status'], action['notes']
    ]
    b._append_row('requests', row)
    print(f"Added: {action['req_id']} — {action['name']}")

# Also update req-003 notes to reference req-004 as the superseding action
rows = b._read_sheet('requests!A:I')
for i, row in enumerate(rows):
    if row and row[0] == 'req-003':
        b.sheets.spreadsheets().values().update(
            spreadsheetId='1IlM43kzxw8Vlu6aUWXUV1dr7ZIF7O7H2bD5x3kaKIHg',
            range=f'requests!I{i+1}',
            valueInputOption='RAW',
            body={'values': [['SUPERSEDED by req-004. Deploy apps-script-code.js instead of Code.gs — it has streak tracker, weekly digest, and form router that Code.gs is missing.']]}
        ).execute()
        b.sheets.spreadsheets().values().update(
            spreadsheetId='1IlM43kzxw8Vlu6aUWXUV1dr7ZIF7O7H2bD5x3kaKIHg',
            range=f'requests!H{i+1}',
            valueInputOption='RAW',
            body={'values': [['superseded']]}
        ).execute()
        print(f"Updated req-003 status to superseded (replaced by req-004)")

print("\nDone. 4 actions added to requests tab.")
