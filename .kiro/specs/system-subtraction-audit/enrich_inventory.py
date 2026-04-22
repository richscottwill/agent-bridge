#!/usr/bin/env python3
"""Phase 1 tasks 1.4 + 1.5: add auto_generated_candidate and prior_session_notes to inventory.json."""
import json, subprocess, re, os, datetime

INV = '/home/prichwil/.kiro/specs/system-subtraction-audit/inventory.json'
SESSION_LOG = '/home/prichwil/shared/context/intake/session-log.md'

with open(INV) as f:
    d = json.load(f)

# Read session log once
if os.path.exists(SESSION_LOG):
    with open(SESSION_LOG) as f:
        session_log = f.read()
else:
    session_log = ""

# For each file, enrich
for entry in d['files']:
    path = entry['path']
    rel = entry['rel_path']
    basename = os.path.basename(path)

    # Auto-generated candidate: git log --since 30 days, count commits
    try:
        r = subprocess.run(
            ['git', '-C', '/home/prichwil/shared', 'log', '--oneline',
             '--since=30 days ago', '--', path],
            capture_output=True, text=True, timeout=10
        )
        commits_30d = len([ln for ln in r.stdout.splitlines() if ln.strip()])
    except Exception:
        commits_30d = 0
    entry['commits_last_30d'] = commits_30d
    entry['auto_generated_candidate'] = commits_30d >= 5

    # Prior-session notes: grep session-log for basename or rel_path variants
    notes = []
    patterns = [basename, rel, rel.replace('~/', '')]
    for ln in session_log.splitlines():
        if any(p in ln for p in patterns):
            # truncate long lines
            notes.append(ln[:280])
    # Also last 90 days git log subject lines
    try:
        r = subprocess.run(
            ['git', '-C', '/home/prichwil/shared', 'log',
             '--pretty=format:%as: %s', '--since=90 days ago', '--', path],
            capture_output=True, text=True, timeout=10
        )
        git_notes = [ln for ln in r.stdout.splitlines() if ln.strip()][:5]
    except Exception:
        git_notes = []
    entry['prior_session_notes'] = notes[:5]  # cap
    entry['git_notes_90d'] = git_notes

# Totals
by_layer = {}
for e in d['files']:
    by_layer.setdefault(e['layer'], {'files': 0, 'lines': 0})
    by_layer[e['layer']]['files'] += 1
    by_layer[e['layer']]['lines'] += e['lines']
total_lines = sum(l['lines'] for l in by_layer.values())

d['totals'] = {
    'body':      by_layer.get('body', {'files':0,'lines':0}),
    'protocols': by_layer.get('protocol', {'files':0,'lines':0}),
    'hooks':     by_layer.get('hook', {'files':0,'lines':0}),
    'steering':  by_layer.get('steering', {'files':0,'lines':0}),
    'grand_total_lines': total_lines,
    'grand_total_files': len(d['files'])
}

with open(INV, 'w') as f:
    json.dump(d, f, indent=2)

print(f"Enriched {len(d['files'])} entries.")
print(f"Auto-generated candidates: {sum(1 for e in d['files'] if e['auto_generated_candidate'])}")
print(f"Entries with prior-session notes: {sum(1 for e in d['files'] if e['prior_session_notes'])}")
