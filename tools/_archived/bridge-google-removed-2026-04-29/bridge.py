"""
Agent Bridge — Google Sheets/Docs communication layer.

Provides read/write access to the agent-bridge spreadsheet and doc
for inter-agent messaging, context snapshots, and registry management.

Usage:
    from bridge import Bridge
    b = Bridge()
    b.send('swarm', 'request', 'Need Q1 competitive analysis', {'scope': 'AU, MX'})
    messages = b.poll(target='kiro', status='pending')
    b.push_context('brain', 'Level 1 active, streak at 3 weeks', {...})
"""

import json
import os
from datetime import datetime, timezone
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Config
SERVICE_ACCOUNT_PATH = os.environ.get(
    'SERVICE_ACCOUNT_PATH',
    '/home/prichwil/shared/credentials/kiro-491503-6b65ab0501c6.json'
)
SPREADSHEET_ID = '1IlM43kzxw8Vlu6aUWXUV1dr7ZIF7O7H2bD5x3kaKIHg'
DOC_ID = '1koJV8a4Ig9BBDbrtQl-w8L4-2bUrz8lGwxUxEfIgQj8'
DRIVE_FOLDER_ID = '1aeRuldkc-OL1gyR7FQ-WrvbpERPsYChZ'

# Subfolders
FOLDERS = {
    'drafts': '19m7Vke9l0wBRZwJ3ebLxhu-EzkoNeMrO',
    'research': '1pNFnIGiptIG1ak1oqT_S7FWEviusVxHZ',
    'archive': '1xvwTkJkkFz9ivhb85EHkP2BDqTlXIvp_',
    'play': '1-JALSbV8NqQ_SoNKTyQwCz_as1Ku_FlT',
    'agent-lang': '1dl7TPrQv9YPva_LKjuWI6ymFCZE-VDcE',
    'tools': '11pkGCOi9gHXT_ooqxxxFPhOpridXuyV5',
    'rsw-personal': '1lczGdwlLRulXF2C6szjPUN9lL09VaVAL',
    'rsw-work': '1_jszMDKVU-km5a4GoOofZ1VoIN6_Y8_2',
    'backup-kiro': '1Yp6A_y61I_KnFKsrN6SecmI28yOyR9Er',
    'backup-swarm': '1jRTTghm8Af-ZFfg7bbCEd4k8jSK1f-Qz',
}
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
]


class Bridge:
    def __init__(self, agent_id='kiro'):
        self.agent_id = agent_id
        self.creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH, scopes=SCOPES)
        self.sheets = build('sheets', 'v4', credentials=self.creds)
        self.drive = build('drive', 'v3', credentials=self.creds)
        self.docs = build('docs', 'v1', credentials=self.creds)
        self._msg_counter = None

    def _now(self):
        return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    def _next_msg_id(self):
        """Generate next sequential message ID."""
        if self._msg_counter is None:
            rows = self._read_sheet('bus!A:A')
            self._msg_counter = len(rows)  # includes header
        self._msg_counter += 1
        return f'{self.agent_id}-{self._msg_counter:03d}'

    def _read_sheet(self, range_str):
        result = self.sheets.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range=range_str
        ).execute()
        return result.get('values', [])

    def _append_row(self, sheet, values):
        self.sheets.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{sheet}!A:Z',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [values]}
        ).execute()

    # ── Message Bus ──

    def send(self, target, msg_type, subject, payload=None, priority='normal',
             response_to='', expires=''):
        """Send a message to the bus."""
        msg_id = self._next_msg_id()
        row = [
            msg_id, self._now(), self.agent_id, target, msg_type,
            priority, subject,
            json.dumps(payload) if payload else '{}',
            'pending', response_to, expires
        ]
        self._append_row('bus', row)
        return msg_id

    def poll(self, target=None, status='pending', msg_type=None):
        """Read messages from the bus, optionally filtered."""
        rows = self._read_sheet('bus!A:K')
        if len(rows) < 2:
            return []
        headers = rows[0]
        messages = []
        for row in rows[1:]:
            # Pad short rows
            while len(row) < len(headers):
                row.append('')
            msg = dict(zip(headers, row))
            if target and msg.get('target') != target:
                continue
            if status and msg.get('status') != status:
                continue
            if msg_type and msg.get('type') != msg_type:
                continue
            # Parse payload JSON
            try:
                msg['payload'] = json.loads(msg.get('payload', '{}'))
            except json.JSONDecodeError:
                pass
            messages.append(msg)
        return messages

    def claim(self, msg_id):
        """Claim a message by setting its status to 'claimed'."""
        return self._update_status(msg_id, 'claimed')

    def complete(self, msg_id):
        """Mark a message as complete."""
        return self._update_status(msg_id, 'complete')

    def respond(self, original_msg_id, payload, subject=''):
        """Respond to a message. Looks up the original to set the correct target."""
        # Find the original message to get its source (who sent it)
        target = ''
        rows = self._read_sheet('bus!A:K')
        if len(rows) >= 2:
            headers = rows[0]
            for row in rows[1:]:
                while len(row) < len(headers):
                    row.append('')
                msg = dict(zip(headers, row))
                if msg.get('msg_id') == original_msg_id:
                    target = msg.get('source', '')
                    break
        return self.send(
            target=target,
            msg_type='response',
            subject=subject or f'Re: {original_msg_id}',
            payload=payload,
            response_to=original_msg_id
        )

    def _update_status(self, msg_id, new_status):
        """Update the status of a message by msg_id."""
        rows = self._read_sheet('bus!A:K')
        for i, row in enumerate(rows):
            if row and row[0] == msg_id:
                # Status is column I (index 8, so column 9)
                self.sheets.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f'bus!I{i+1}',
                    valueInputOption='RAW',
                    body={'values': [[new_status]]}
                ).execute()
                return True
        return False

    # ── Context Snapshots ──

    def push_context(self, organ, summary, detail=None):
        """Push a context snapshot to the context sheet."""
        snapshot_id = f'ctx-{organ}-{self._now().replace(":", "").replace("-", "")[:12]}'
        row = [
            snapshot_id, self._now(), self.agent_id, organ, summary,
            json.dumps(detail) if detail else ''
        ]
        self._append_row('context', row)
        return snapshot_id

    def read_context(self, organ=None):
        """Read context snapshots, optionally filtered by organ."""
        rows = self._read_sheet('context!A:F')
        if len(rows) < 2:
            return []
        headers = rows[0]
        snapshots = []
        for row in rows[1:]:
            while len(row) < len(headers):
                row.append('')
            snap = dict(zip(headers, row))
            if organ and snap.get('organ') != organ:
                continue
            try:
                snap['detail'] = json.loads(snap.get('detail', '{}'))
            except json.JSONDecodeError:
                pass
            snapshots.append(snap)
        return snapshots

    # ── Registry ──

    def register(self, agent_id=None, platform='', capabilities=None, tools=None, notes=''):
        """Register or update an agent in the registry."""
        aid = agent_id or self.agent_id
        row = [
            aid, platform,
            json.dumps(capabilities or []),
            json.dumps(tools or []),
            self._now(), 'online', notes
        ]
        # Check if already registered
        rows = self._read_sheet('registry!A:G')
        for i, existing in enumerate(rows):
            if existing and existing[0] == aid:
                self.sheets.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f'registry!A{i+1}',
                    valueInputOption='RAW',
                    body={'values': [row]}
                ).execute()
                return
        self._append_row('registry', row)

    def heartbeat(self, status_note=''):
        """Send a heartbeat to the bus and update registry last_seen."""
        self.send('*', 'heartbeat', f'{self.agent_id} alive', {'note': status_note})
        # Update last_seen in registry
        rows = self._read_sheet('registry!A:G')
        for i, row in enumerate(rows):
            if row and row[0] == self.agent_id:
                self.sheets.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f'registry!E{i+1}:F{i+1}',
                    valueInputOption='RAW',
                    body={'values': [[self._now(), 'online']]}
                ).execute()
                return

    # ── Google Doc ──

    def append_to_doc(self, text):
        """Append text to the bridge Google Doc."""
        doc = self.docs.documents().get(documentId=DOC_ID).execute()
        end_index = doc['body']['content'][-1]['endIndex']
        self.docs.documents().batchUpdate(
            documentId=DOC_ID,
            body={'requests': [{
                'insertText': {
                    'location': {'index': end_index - 1},
                    'text': f'\n{text}\n'
                }
            }]}
        ).execute()

    # ── File Management ──

    def create_spreadsheet(self, title):
        """Create a new spreadsheet in the bridge folder."""
        file_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': [DRIVE_FOLDER_ID]
        }
        f = self.drive.files().create(
            body=file_metadata,
            fields='id, name',
            supportsAllDrives=True
        ).execute()
        return f

    def create_doc(self, title):
        """Create a new Google Doc in the bridge folder."""
        file_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [DRIVE_FOLDER_ID]
        }
        f = self.drive.files().create(
            body=file_metadata,
            fields='id, name',
            supportsAllDrives=True
        ).execute()
        return f

    def list_files(self):
        """List all files in the bridge folder."""
        results = self.drive.files().list(
            q=f"'{DRIVE_FOLDER_ID}' in parents",
            fields='files(id, name, mimeType, modifiedTime)',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            corpora='allDrives'
        ).execute()
        return results.get('files', [])

    # ── File Requests ──

    def request_file(self, file_type, name, location, purpose):
        """Post a file/tab creation request to the requests sheet and notify via bus."""
        row = [
            f'req-{self._now().replace(":", "").replace("-", "")[:12]}',
            self._now(), self.agent_id, file_type, name, location, purpose,
            'pending', ''
        ]
        self._append_row('requests', row)
        # Also send to bus so it shows up in polling
        self.send('richard', 'request', f'Create {file_type}: {name}', {
            'type': file_type,
            'name': name,
            'location': location,
            'purpose': purpose,
            'action': 'Create this in Google Drive, then update status to "created" in the requests tab.'
        }, priority='normal')
        return row[0]
