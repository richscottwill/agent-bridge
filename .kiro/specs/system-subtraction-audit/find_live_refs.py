#!/usr/bin/env python3
import json
refs = json.load(open('/home/prichwil/.kiro/specs/system-subtraction-audit/referrers.json'))

DELETE_SET = [
    '/home/prichwil/.kiro/steering/context/context-provider-recommendations.md',
    '/home/prichwil/.kiro/steering/context/kiro-limitations.md',
    '/home/prichwil/.kiro/steering/context/powers-evaluation.md',
    '/home/prichwil/.kiro/steering/context/steering-integrity.md',
    '/home/prichwil/.kiro/steering/agentspaces-core.md',
    '/home/prichwil/.kiro/steering/devspaces-core.md',
    '/home/prichwil/.kiro/hooks/dashboard-server.kiro.hook',
    '/home/prichwil/shared/context/protocols/am-backend.md',
    '/home/prichwil/shared/context/body/body-diagram.md',
]

def category(src):
    if '~/shared/context/body' in src: return 'body'
    if '~/shared/context/protocols' in src: return 'protocols'
    if '~/.kiro/steering' in src: return 'steering'
    if '~/.kiro/hooks' in src: return 'hooks'
    if '~/.kiro/agents' in src: return 'agents'
    if '~/.kiro/specs' in src: return 'specs (doc)'
    if '~/shared/wiki' in src: return 'wiki (doc)'
    if '~/shared/context/active' in src: return 'active (log)'
    if '~/shared/context/experiments' in src: return 'experiments'
    if '~/shared/context/intake' in src: return 'intake'
    if '~/shared/tools' in src: return 'tools'
    if '~/shared/scripts' in src: return 'scripts'
    if '~/shared/dashboards' in src: return 'dashboards (data)'
    return 'other'

LIVE = {'body','protocols','steering','hooks','agents','tools','scripts'}

results = {}
for tgt in DELETE_SET:
    edges = [e for e in refs['edges'] if e['to'] == tgt]
    path_e = [e for e in edges if e['match_type'] == 'path']
    live = [e for e in path_e if category(e['from']) in LIVE]
    results[tgt] = {'total_path': len(path_e), 'live': live}
    print(f'\n=== {tgt.replace("/home/prichwil","~")} ===')
    print(f'  path edges: {len(path_e)}, LIVE: {len(live)}')
    for e in live:
        print(f'    {category(e["from"]):12s} {e["from"]:70s} L{e["line_number"]}')
        print(f'       ctx: {e["context"][:150]}')

# Dump structured for the executor
with open('/home/prichwil/.kiro/specs/system-subtraction-audit/delete_plan.json', 'w') as f:
    json.dump({t: [{'from': e['from'], 'line': e['line_number'], 'context': e['context']}
                   for e in r['live']] for t, r in results.items()}, f, indent=2)
print('\nSaved delete_plan.json')
