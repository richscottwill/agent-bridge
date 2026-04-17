#!/usr/bin/env python3
"""Process Asana task stories and extract teammate activity signals."""
import json
import sys

def process_stories(task_gid, task_name, raw_file, cutoff, richard_gid):
    try:
        with open(raw_file) as f:
            raw = json.load(f)
        
        text_content = raw['result']['content'][0]['text']
        api_data = json.loads(text_content)
        stories = api_data.get('APIOutput', {}).get('Response', {}).get('data', [])
    except Exception as e:
        print(f"{task_gid}|{task_name}|Parse error: {e}", file=sys.stderr)
        return
    
    for story in stories:
        created_at = story.get('created_at', '')
        if created_at <= cutoff:
            continue
        
        created_by = story.get('created_by', {})
        if not created_by or not created_by.get('gid'):
            continue
        if created_by.get('gid') == richard_gid:
            continue
        
        resource_subtype = story.get('resource_subtype', '')
        text = story.get('text', '')
        author_name = created_by.get('name', 'Unknown')
        author_gid = created_by.get('gid', '')
        
        signal_type = None
        if resource_subtype == 'comment_added' or story.get('type') == 'comment':
            signal_type = 'comment_added'
        elif 'due date' in text.lower() or resource_subtype == 'due_date_changed':
            signal_type = 'due_date_changed'
        elif resource_subtype in ('assigned', 'reassigned') or 'reassigned' in text.lower():
            signal_type = 'reassigned'
        
        if signal_type:
            signal = {
                'task_gid': task_gid,
                'task_name': task_name,
                'signal_type': signal_type,
                'author_name': author_name,
                'author_gid': author_gid,
                'created_at': created_at,
                'text': text[:200],
                'resource_subtype': resource_subtype,
                'story_gid': story.get('gid', '')
            }
            print(json.dumps(signal))

if __name__ == '__main__':
    process_stories(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
