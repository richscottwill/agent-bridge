#!/usr/bin/env python3
"""Retry rate-limited Asana tasks from the initial scan."""
import json, subprocess, os, time, sys
from datetime import datetime, timezone

CUTOFF = '2026-04-09T00:00:00.000Z'
RICHARD_GID = '1212732742544167'
MCP_BIN = os.path.expanduser('~/.toolbox/bin/enterprise-asana-mcp')

with open(os.path.expanduser('~/shared/tools/asana-scan-output/scan-results.json')) as f:
    data = json.load(f)

errored = data['errors']
new_signals = []
still_errored = []
new_timestamps = {}
now_ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

print(f'Retrying {len(errored)} tasks...', file=sys.stderr)

for i, e in enumerate(errored):
    task_gid = e['task_gid']
    task_name = e['task_name']
    
    request = json.dumps({
        'jsonrpc': '2.0', 'id': i+1,
        'method': 'tools/call',
        'params': {'name': 'asana___GetTaskStories', 'arguments': {'task_gid': task_gid}}
    })
    cmd = f"echo '{request}' | timeout 30 {MCP_BIN} 2>/dev/null"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=35)
        stdout = result.stdout.strip()
        if not stdout:
            still_errored.append(e)
            time.sleep(0.5)
            continue
        
        raw = json.loads(stdout)
        if 'error' in raw:
            still_errored.append({'task_gid': task_gid, 'task_name': task_name, 'error': str(raw['error'])})
            time.sleep(0.5)
            continue
        
        text_content = raw['result']['content'][0]['text']
        api_data = json.loads(text_content)
        stories = api_data.get('data', api_data.get('APIOutput', {}).get('Response', {}).get('data', []))
        
        latest_ts = None
        for story in stories:
            created_at = story.get('created_at', '')
            if created_at > CUTOFF:
                if latest_ts is None or created_at > latest_ts:
                    latest_ts = created_at
                created_by = story.get('created_by') or {}
                if not created_by.get('gid') or created_by.get('gid') == RICHARD_GID:
                    continue
                resource_subtype = story.get('resource_subtype', '')
                text = story.get('text', '')
                stype = story.get('type', '')
                signal_type = None
                if resource_subtype == 'comment_added' or stype == 'comment':
                    signal_type = 'comment_added'
                elif 'due date' in text.lower() or resource_subtype == 'due_date_changed':
                    signal_type = 'due_date_changed'
                elif resource_subtype in ('assigned', 'reassigned') or 'reassigned' in text.lower():
                    signal_type = 'reassigned'
                if signal_type:
                    new_signals.append({
                        'task_gid': task_gid, 'task_name': task_name,
                        'signal_type': signal_type,
                        'author_name': created_by.get('name', 'Unknown'),
                        'author_gid': created_by.get('gid', ''),
                        'created_at': created_at,
                        'text': text[:200],
                        'resource_subtype': resource_subtype,
                        'story_gid': story.get('gid', '')
                    })
        new_timestamps[task_gid] = latest_ts or now_ts
        
    except Exception as ex:
        still_errored.append({'task_gid': task_gid, 'task_name': task_name, 'error': str(ex)})
    
    time.sleep(0.5)
    if (i+1) % 10 == 0:
        print(f'Retry progress: {i+1}/{len(errored)}', file=sys.stderr)

# Merge results
data['signals'].extend(new_signals)
data['errors'] = still_errored
data['per_task_timestamps'].update(new_timestamps)

with open(os.path.expanduser('~/shared/tools/asana-scan-output/scan-results.json'), 'w') as f:
    json.dump(data, f, indent=2)

print(f'Retry complete. New signals: {len(new_signals)}. Still errored: {len(still_errored)}')
if new_signals:
    for s in new_signals:
        print(f'  {s["signal_type"]}: {s["task_name"]} -- {s["author_name"]}')
