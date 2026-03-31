#!/usr/bin/env python3
"""
Bridge Upgrade — Restructure for simpler models.

Changes:
1. Add example rows to bus (status=example)
2. Create 'inbox' sheet with auto-filter formula for pending swarm messages
3. Flatten context tab — add explicit columns, remove JSON dependency
4. Add last_updated timestamp to protocol tab
5. Create 'playbook' sheet — task templates the swarm can copy
6. Create 'scratchpad' sheet — working memory for swarm agents
7. Restructure protocol tab with session startup checklist
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import Bridge

b = Bridge()
SSID = '1IlM43kzxw8Vlu6aUWXUV1dr7ZIF7O7H2bD5x3kaKIHg'

def create_sheet_if_missing(title, index=None):
    meta = b.sheets.spreadsheets().get(spreadsheetId=SSID).execute()
    existing = [s['properties']['title'] for s in meta['sheets']]
    if title not in existing:
        props = {'title': title}
        if index is not None:
            props['index'] = index
        b.sheets.spreadsheets().batchUpdate(
            spreadsheetId=SSID,
            body={'requests': [{'addSheet': {'properties': props}}]}
        ).execute()
        print(f'Created sheet: {title}')
    else:
        print(f'Sheet already exists: {title}')

# ============================================================
# 1. ADD EXAMPLE ROWS TO BUS
# ============================================================
print('\n=== 1. Adding example rows to bus ===')

now = b._now()
example_request = [
    'example-001', '2026-03-30T10:00:00Z', 'kiro', 'swarm', 'request', 'normal',
    'Research AU B2B paid search CPC benchmarks',
    json.dumps({
        'market': 'AU',
        'what_i_need': 'Average CPC for B2B keywords in Australia across Google Ads. Compare to consumer CPC ($0.18-0.50). Include source URLs.',
        'deadline': '2026-04-02',
        'output_format': 'Put findings in the payload of your response. Keep it under 500 words.'
    }),
    'example', '', ''
]
example_response = [
    'example-002', '2026-03-30T14:00:00Z', 'swarm', 'kiro', 'response', 'normal',
    'AU B2B paid search CPC benchmarks — findings',
    json.dumps({
        'market': 'AU',
        'avg_b2b_cpc': '$4-8 AUD',
        'avg_consumer_cpc': '$0.18-0.50 AUD',
        'key_finding': 'B2B keywords in AU run 10-40x higher CPC than consumer due to low search volume and high competition from office supply retailers.',
        'sources': 'WordStream 2025 benchmarks, Google Keyword Planner AU estimates',
        'confidence': 'MEDIUM — benchmarks are cross-industry, not AB-specific'
    }),
    'example', 'example-001', ''
]

# Check if examples already exist
rows = b._read_sheet('bus!A:A')
has_examples = any(r[0].startswith('example-') for r in rows if r)
if not has_examples:
    b._append_row('bus', example_request)
    b._append_row('bus', example_response)
    print('Added 2 example rows to bus')
else:
    print('Example rows already exist, skipping')


# ============================================================
# 2. CREATE INBOX SHEET
# ============================================================
print('\n=== 2. Creating inbox sheet ===')
create_sheet_if_missing('inbox', index=1)

# Write inbox header and instructions
inbox_rows = [
    ['=== SWARM INBOX ===', '', '', '', '', '', ''],
    ['This sheet shows messages waiting for the swarm. Refresh: re-run the inbox updater script or check the bus tab directly.', '', '', '', '', '', ''],
    ['Last refreshed:', now, '', '', '', '', ''],
    ['', '', '', '', '', '', ''],
    ['msg_id', 'timestamp', 'source', 'priority', 'subject', 'what_to_do', 'payload_summary'],
]

# Pull pending messages for swarm
bus_rows = b._read_sheet('bus!A:K')
if len(bus_rows) > 1:
    headers = bus_rows[0]
    for row in bus_rows[1:]:
        while len(row) < len(headers):
            row.append('')
        msg = dict(zip(headers, row))
        if msg.get('status') != 'pending':
            continue
        target = msg.get('target', '')
        if target not in ('swarm', '*'):
            continue
        if msg.get('type') in ('heartbeat',):
            continue

        # Parse payload for summary
        payload_summary = ''
        try:
            p = json.loads(msg.get('payload', '{}'))
            if isinstance(p, dict):
                # Take the most useful fields
                for key in ['what_i_need', 'action', 'message', 'note', 'scope']:
                    if key in p:
                        payload_summary = str(p[key])[:200]
                        break
                if not payload_summary:
                    payload_summary = str(p)[:200]
        except:
            payload_summary = msg.get('payload', '')[:200]

        # Determine what_to_do based on type
        mtype = msg.get('type', '')
        if mtype == 'request':
            what_to_do = 'DO THIS: Read the subject and payload. Do the work. Write a response row in the bus tab.'
        elif mtype == 'context_push':
            what_to_do = 'READ ONLY: This is context from Kiro. Absorb it. No response needed.'
        elif mtype == 'announce':
            what_to_do = 'READ ONLY: Announcement. No response needed.'
        else:
            what_to_do = f'Type: {mtype}. Check protocol tab for instructions.'

        inbox_rows.append([
            msg.get('msg_id', ''),
            msg.get('timestamp', ''),
            msg.get('source', ''),
            msg.get('priority', ''),
            msg.get('subject', ''),
            what_to_do,
            payload_summary
        ])

b.sheets.spreadsheets().values().update(
    spreadsheetId=SSID,
    range='inbox!A1',
    valueInputOption='RAW',
    body={'values': inbox_rows}
).execute()
print(f'Wrote {len(inbox_rows)} rows to inbox (including {len(inbox_rows)-5} pending messages)')


# ============================================================
# 3. FLATTEN CONTEXT TAB
# ============================================================
print('\n=== 3. Flattening context tab ===')

# Read existing context
ctx_rows = b._read_sheet('context!A:F')
ctx_headers = ctx_rows[0] if ctx_rows else []

# Build new flattened context with explicit columns
new_ctx = [
    ['snapshot_id', 'timestamp', 'source', 'organ', 'summary',
     'hard_thing', 'streak', 'overdue_count', 'key_deadline', 'key_people', 'detail_json']
]

for row in ctx_rows[1:]:
    while len(row) < 6:
        row.append('')
    snap = dict(zip(ctx_headers, row))

    # Parse detail JSON to extract flat fields
    hard_thing = ''
    streak = ''
    overdue_count = ''
    key_deadline = ''
    key_people = ''
    detail_json = snap.get('detail', '')

    try:
        d = json.loads(detail_json) if detail_json else {}
        hard_thing = str(d.get('hard_thing', ''))
        streak = str(d.get('streak', ''))
        overdue_count = str(d.get('overdue_count', ''))
        key_deadline = str(d.get('kate_meeting', d.get('key_meeting', '')))
        key_people = str(d.get('new_stakeholder', d.get('key_people', '')))
    except:
        pass

    new_ctx.append([
        snap.get('snapshot_id', ''),
        snap.get('timestamp', ''),
        snap.get('source', ''),
        snap.get('organ', ''),
        snap.get('summary', ''),
        hard_thing,
        streak,
        overdue_count,
        key_deadline,
        key_people,
        detail_json  # keep original JSON as last column for backward compat
    ])

# Clear and rewrite
b.sheets.spreadsheets().values().clear(
    spreadsheetId=SSID,
    range='context!A:K'
).execute()
b.sheets.spreadsheets().values().update(
    spreadsheetId=SSID,
    range='context!A1',
    valueInputOption='RAW',
    body={'values': new_ctx}
).execute()
print(f'Rewrote context tab with {len(new_ctx)-1} snapshots, now with flat columns')


# ============================================================
# 4. UPDATE PROTOCOL TAB WITH TIMESTAMP + STARTUP CHECKLIST
# ============================================================
print('\n=== 4. Updating protocol tab ===')

# Prepend a last_updated row and startup checklist
protocol_rows = b._read_sheet('protocol!A:B')

# Find and update or prepend
new_header_rows = [
    ['LAST UPDATED', now],
    ['', ''],
    ['=== SESSION STARTUP CHECKLIST ===', ''],
    ['STEP 1', 'Read this protocol tab top to bottom. Every time. No exceptions.'],
    ['STEP 2', 'Check the inbox tab — it shows messages waiting for you, pre-filtered and with plain-English instructions.'],
    ['STEP 3', 'Check the context tab — read the summary column for each organ to understand current state. Ignore the detail_json column.'],
    ['STEP 4', 'Check the registry tab — update your last_seen timestamp to show you are online.'],
    ['STEP 5', 'Check the playbook tab — if your task matches a template, follow it exactly.'],
    ['STEP 6', 'Do your work. Write responses to the bus tab following the format in this protocol.'],
    ['STEP 7', 'Before ending your session, update your last_seen in registry and write a summary of what you did to the scratchpad tab.'],
    ['', ''],
]

# Remove old header if it exists (first row might be 'section' header)
if protocol_rows and protocol_rows[0][0] == 'section':
    protocol_rows = protocol_rows[1:]  # skip old header
if protocol_rows and protocol_rows[0][0] == 'LAST UPDATED':
    # Find where the old header section ends
    for i, row in enumerate(protocol_rows):
        if row and row[0] == '=== HOW THIS BRIDGE WORKS ===':
            protocol_rows = protocol_rows[i:]
            break

combined = new_header_rows + protocol_rows

b.sheets.spreadsheets().values().clear(
    spreadsheetId=SSID,
    range='protocol!A:B'
).execute()
b.sheets.spreadsheets().values().update(
    spreadsheetId=SSID,
    range='protocol!A1',
    valueInputOption='RAW',
    body={'values': combined}
).execute()
print(f'Updated protocol tab with timestamp + startup checklist ({len(combined)} rows)')


# ============================================================
# 5. CREATE PLAYBOOK SHEET — Task templates
# ============================================================
print('\n=== 5. Creating playbook sheet ===')
create_sheet_if_missing('playbook')

playbook_rows = [
    ['=== PLAYBOOK — Task Templates ===', '', '', ''],
    ['When you get a request, check if it matches a template below. If yes, follow the template exactly.', '', '', ''],
    ['Last updated:', now, '', ''],
    ['', '', '', ''],
    ['template_name', 'when_to_use', 'steps', 'output_format'],
    [
        'Competitive Research',
        'When asked to research competitors, benchmarks, or market data',
        '1. Search for the specific market + metric requested. 2. Find 2-3 credible sources (industry reports, tool estimates, official docs). 3. Summarize findings in 200-400 words. 4. Include source URLs. 5. Rate your confidence: HIGH (multiple sources agree), MEDIUM (limited data), LOW (extrapolating).',
        'Write a bus response with payload containing: market, finding, sources, confidence, and a plain-text summary under 500 words.'
    ],
    [
        'Draft Document Section',
        'When asked to write or draft a section of a document',
        '1. Read the context tab for current state (especially brain and hands organs). 2. Read any specific instructions in the request payload. 3. Write the section in plain text — no markdown headers, no formatting. 4. Keep it under 800 words unless told otherwise. 5. Include a "suggested edits" note if you think something should change.',
        'Write a bus response with payload containing: section_title, content (plain text), word_count, suggested_edits.'
    ],
    [
        'Data Lookup',
        'When asked to find a specific number, date, or fact',
        '1. Search for the specific data point. 2. Find the most recent and authoritative source. 3. Report the value, the source, and the date of the source. 4. If you cannot find it, say so clearly — do not guess.',
        'Write a bus response with payload containing: query, value, source, source_date, confidence.'
    ],
    [
        'Summarize Content',
        'When asked to summarize a document, article, or thread',
        '1. Read the full content. 2. Write a 3-5 bullet summary of key points. 3. Highlight any action items or decisions. 4. Note anything that seems wrong or contradictory.',
        'Write a bus response with payload containing: source_title, summary_bullets (as a single string with newlines), action_items, flags.'
    ],
    [
        'Monitor / Watch',
        'When asked to monitor something ongoing (competitor, news, metric)',
        '1. Do an initial check now and report findings. 2. Note what you checked and when. 3. Suggest a check-in frequency. 4. Write findings to the bus. 5. On subsequent sessions, check the scratchpad for your last findings and report what changed.',
        'Write a bus response with payload containing: topic, current_status, last_checked, changes_since_last, next_check_suggested.'
    ],
]

b.sheets.spreadsheets().values().update(
    spreadsheetId=SSID,
    range='playbook!A1',
    valueInputOption='RAW',
    body={'values': playbook_rows}
).execute()
print(f'Wrote {len(playbook_rows)} rows to playbook')


# ============================================================
# 6. CREATE SCRATCHPAD SHEET — Working memory
# ============================================================
print('\n=== 6. Creating scratchpad sheet ===')
create_sheet_if_missing('scratchpad')

scratchpad_rows = [
    ['=== SCRATCHPAD — Swarm Working Memory ===', '', '', ''],
    ['Use this sheet to leave notes for your future self. You have no persistent memory — this is it.', '', '', ''],
    ['Write what you did, what you found, what you were working on, and what to do next.', '', '', ''],
    ['Last updated:', now, '', ''],
    ['', '', '', ''],
    ['timestamp', 'agent_id', 'topic', 'notes'],
    [now, 'kiro', 'Bridge setup', 'Protocol sheet, inbox, playbook, scratchpad created. Context tab flattened. Example bus rows added. Swarm should register in registry tab and start checking inbox for pending requests.'],
]

b.sheets.spreadsheets().values().update(
    spreadsheetId=SSID,
    range='scratchpad!A1',
    valueInputOption='RAW',
    body={'values': scratchpad_rows}
).execute()
print(f'Wrote {len(scratchpad_rows)} rows to scratchpad')


# ============================================================
# 7. UPDATE PROTOCOL — Add references to new sheets
# ============================================================
print('\n=== 7. Adding new sheet references to protocol ===')

new_sections = [
    ['', ''],
    ['=== NEW SHEETS (read these too) ===', ''],
    ['inbox', 'Pre-filtered view of messages waiting for you. Check this FIRST — it tells you exactly what to do for each message. Refreshed by Kiro.'],
    ['playbook', 'Task templates. If your request matches a template, follow it step by step. Templates define the output format so you do not have to guess.'],
    ['scratchpad', 'Your working memory. Write notes here at the end of every session: what you did, what you found, what to do next. Read it at the start of every session to remember where you left off.'],
    ['context', 'Kiro pushes knowledge snapshots here. Read the summary column — it is plain text. Ignore the detail_json column unless you need specifics. Key columns: hard_thing, streak, overdue_count, key_deadline.'],
    ['', ''],
    ['=== TIPS FOR SIMPLER MODELS ===', ''],
    ['TIP 1', 'If you are confused, read the inbox tab. It tells you what to do in plain English.'],
    ['TIP 2', 'If you do not know the output format, check the playbook tab for a matching template.'],
    ['TIP 3', 'If you need to remember something for next time, write it to the scratchpad tab.'],
    ['TIP 4', 'Never parse the detail_json column in the context tab. Use the flat columns instead: hard_thing, streak, overdue_count, key_deadline, key_people.'],
    ['TIP 5', 'When writing a response payload, use simple key-value pairs. Example: {"finding": "AU CPC is $6", "source": "Google Ads", "confidence": "HIGH"}. No nested objects.'],
    ['TIP 6', 'If a request is too complex, break it into parts. Respond with what you can do now, and note what remains in the scratchpad.'],
    ['TIP 7', 'Always update your last_seen in the registry tab when you start and end a session. This is how the system knows you are alive.'],
]

b.sheets.spreadsheets().values().append(
    spreadsheetId=SSID,
    range='protocol!A:B',
    valueInputOption='RAW',
    insertDataOption='INSERT_ROWS',
    body={'values': new_sections}
).execute()
print(f'Appended {len(new_sections)} rows to protocol')


print('\n=== DONE ===')
print('New sheets: inbox, playbook, scratchpad')
print('Updated sheets: protocol (timestamp + checklist + new sheet refs + tips), context (flattened), bus (examples)')
