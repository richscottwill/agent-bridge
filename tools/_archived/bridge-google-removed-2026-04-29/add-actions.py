#!/usr/bin/env python3
"""Check for a Richard actions tab and add items to it."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import Bridge

b = Bridge()
SSID = '1IlM43kzxw8Vlu6aUWXUV1dr7ZIF7O7H2bD5x3kaKIHg'

# List all sheets
meta = b.sheets.spreadsheets().get(spreadsheetId=SSID).execute()
sheets = [s['properties']['title'] for s in meta['sheets']]
print('Existing tabs:', sheets)
