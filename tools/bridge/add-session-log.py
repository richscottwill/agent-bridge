#!/usr/bin/env python3
"""
Add session_log sheet to the bridge spreadsheet.
Structured end-of-session checklist that captures behavioral signals.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import Bridge

b = Bridge()
SSID = '1IlM43kzxw8Vlu6aUWXUV1dr7ZIF7O7H2bD5x3kaKIHg'
now = b._now()

# Create sheet
meta = b.sheets.spreadsheets().get(spreadsheetId=SSID).execute()
existing = [s['properties']['title'] for s in meta['sheets']]
if 'session_log' not in existing:
    b.sheets.spreadsheets().batchUpdate(
        spreadsheetId=SSID,
        body={'requests': [{'addSheet': {'properties': {'title': 'session_log'}}}]}
    ).execute()
    print('Created session_log sheet')
else:
    print('session_log already exists')

rows = [
    ['=== SESSION LOG ===', '', ''],
    ['Fill out ONE ROW at the end of every session. This is mandatory — it is how we improve the bridge.', '', ''],
    ['Be honest. If something was confusing, say so. If you skipped a step, say which one and why.', '', ''],
    ['', '', ''],
    [
        'timestamp',
        'agent_id',
        'session_duration_min',
        'read_protocol',
        'read_inbox',
        'read_context',
        'read_playbook',
        'used_playbook_template',
        'which_template',
        'updated_registry',
        'wrote_scratchpad',
        'messages_responded_to',
        'messages_failed',
        'hardest_part',
        'what_was_unclear',
        'what_would_help',
        'skipped_steps',
        'confidence_in_output',
    ],
    # Example row
    [
        '2026-03-30T16:00:00Z',
        'swarm-example',
        '25',
        'yes',
        'yes',
        'yes',
        'yes',
        'yes',
        'Competitive Research',
        'yes',
        'yes',
        '2',
        '0',
        'Understanding what "organ" means in the context tab',
        'The relationship between bus and inbox — are they the same data?',
        'A glossary of terms used across sheets',
        'none',
        'HIGH',
    ],
]

b.sheets.spreadsheets().values().update(
    spreadsheetId=SSID,
    range='session_log!A1',
    valueInputOption='RAW',
    body={'values': rows}
).execute()
print(f'Wrote {len(rows)} rows to session_log')

# --- Add session_log to protocol tab ---
protocol_addition = [
    ['', ''],
    ['=== END-OF-SESSION LOG (MANDATORY) ===', ''],
    ['WHAT', 'Before ending your session, fill out ONE ROW in the session_log tab. This takes 2 minutes. It is not optional.'],
    ['WHY', 'Your feedback improves the bridge for all agents. We use it to fix confusing parts, add missing templates, and simplify the structure. If you skip this, we cannot help you.'],
    ['HOW', 'Go to the session_log tab. Add a new row below the example. Fill in every column. For yes/no columns, write yes or no. For text columns, write 1-2 sentences max. For confidence, write HIGH, MEDIUM, or LOW.'],
    ['COLUMNS EXPLAINED', ''],
    ['timestamp', 'Current UTC time when you finish.'],
    ['agent_id', 'Your agent ID (same as in registry).'],
    ['session_duration_min', 'Roughly how many minutes you spent working. Estimate is fine.'],
    ['read_protocol', 'Did you read the protocol tab this session? yes or no.'],
    ['read_inbox', 'Did you check the inbox tab? yes or no.'],
    ['read_context', 'Did you read the context tab summaries? yes or no.'],
    ['read_playbook', 'Did you check the playbook tab? yes or no.'],
    ['used_playbook_template', 'Did you follow a playbook template for your work? yes or no.'],
    ['which_template', 'If yes, which template name? If no, write none.'],
    ['updated_registry', 'Did you update your last_seen in the registry? yes or no.'],
    ['wrote_scratchpad', 'Did you write notes to the scratchpad? yes or no.'],
    ['messages_responded_to', 'How many bus messages did you respond to? A number.'],
    ['messages_failed', 'How many requests could you NOT complete? A number.'],
    ['hardest_part', 'What was the hardest part of this session? 1-2 sentences.'],
    ['what_was_unclear', 'What was confusing or unclear about the bridge structure? 1-2 sentences. Write none if everything was clear.'],
    ['what_would_help', 'What would make your next session easier? 1-2 sentences. Be specific.'],
    ['skipped_steps', 'Did you skip any protocol steps? If yes, which ones and why? Write none if you followed all steps.'],
    ['confidence_in_output', 'How confident are you in the quality of your work this session? HIGH, MEDIUM, or LOW.'],
]

b.sheets.spreadsheets().values().append(
    spreadsheetId=SSID,
    range='protocol!A:B',
    valueInputOption='RAW',
    insertDataOption='INSERT_ROWS',
    body={'values': protocol_addition}
).execute()
print(f'Added session_log instructions to protocol tab ({len(protocol_addition)} rows)')

# --- Update startup checklist step 7 to mention session_log ---
# Read protocol to find step 7
proto = b._read_sheet('protocol!A:B')
for i, row in enumerate(proto):
    if row and row[0] == 'STEP 7':
        b.sheets.spreadsheets().values().update(
            spreadsheetId=SSID,
            range=f'protocol!B{i+1}',
            valueInputOption='RAW',
            body={'values': [['Before ending your session: (1) Update last_seen in registry. (2) Write notes to scratchpad. (3) Fill out ONE ROW in session_log — this is mandatory.']]}
        ).execute()
        print('Updated STEP 7 in startup checklist to include session_log')
        break

print('\nDone.')
