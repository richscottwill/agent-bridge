#!/usr/bin/env python3
"""Phase 4 — Classification via decision tree."""
import json, os, re
from collections import defaultdict

INV = '/home/prichwil/.kiro/specs/system-subtraction-audit/inventory.json'
REFS = '/home/prichwil/.kiro/specs/system-subtraction-audit/referrers.json'
DUPS = '/home/prichwil/.kiro/specs/system-subtraction-audit/duplication_groups.json'
PRE = '/home/prichwil/.kiro/specs/system-subtraction-audit/preflight.json'
OUT = '/home/prichwil/.kiro/specs/system-subtraction-audit/classified.json'

with open(INV) as f: inv = json.load(f)
with open(REFS) as f: refs = json.load(f)
with open(DUPS) as f: dups = json.load(f)
with open(PRE) as f: pre = json.load(f)

files = inv['files']
by_rel = {e['rel_path']: e for e in files}

# Flattened by_target key — we stored by abspath by accident earlier; normalize
target_index = {}
for key, val in refs['by_target'].items():
    # key might be absolute path or rel_path; normalize to rel_path via inventory
    if key in by_rel:
        target_index[key] = val
    else:
        # find the inventory entry whose path equals key
        for e in files:
            if e['path'] == key or e['rel_path'] == key:
                target_index[e['rel_path']] = val
                break

# Duplication lookup
dup_membership = {}  # rel_path -> (group, role: 'survivor'|'loser'|'template'|'instance')
for g in dups['groups']:
    if g['shape'] == 'template_plus_instances':
        dup_membership[g['template']] = (g, 'template')
        for inst in g['instances']:
            dup_membership[inst] = (g, 'instance')
    else:
        for m in g['members']:
            if m == g.get('recommended_survivor'):
                dup_membership[m] = (g, 'survivor')
            else:
                dup_membership[m] = (g, 'loser')

# Karpathy-protected: empty this run per user direction
karpathy_set = set(pre.get('karpathy_protected_files', []))

# Build soul.md auto-include set (files referenced via #[[file:...]] from always-auto steering)
auto_include_targets = set()
for e in refs['edges']:
    if e['match_type'] != 'path':
        continue
    from_entry = by_rel.get(e['from'])
    if not from_entry:
        # try absolute form
        for f in files:
            if f['path'] == e['from'].replace('~/', '/home/prichwil/'):
                from_entry = f
                break
    if from_entry and from_entry['layer'] == 'steering' and from_entry['inclusion_mode'] == 'auto':
        auto_include_targets.add(e['to'])

# Classification
classified = []

# Counters for row IDs
row_counter = defaultdict(int)
layer_letter = {'body': 'B', 'protocol': 'P', 'hook': 'H', 'steering': 'S'}
action_letter = {'DELETE': 'D', 'MERGE': 'M', 'UNCLEAR': 'U', 'KEEP': 'K', 'KARPATHY-FLAG': 'X'}

def assign_row_id(layer, action):
    key = (layer_letter.get(layer, 'Z'), action_letter.get(action, '?'))
    row_counter[key] += 1
    return f'{key[0]}-{key[1]}{row_counter[key]}'

def active_refs(rel):
    return target_index.get(rel, {}).get('active_path_referrers', 0)
def latent_refs(rel):
    return target_index.get(rel, {}).get('latent_referrers', 0)
def doc_refs(rel):
    return target_index.get(rel, {}).get('documentation_referrers', 0)
def name_refs(rel):
    return target_index.get(rel, {}).get('name_only_referrers', 0)
def referrer_list(rel):
    return target_index.get(rel, {}).get('referrers_detail', [])

for f in files:
    rel = f['rel_path']
    layer = f['layer']
    entry = {
        'rel_path': rel,
        'layer': layer,
        'lines': f['lines'],
        'first_heading': f['first_heading'],
    }

    # Evidence
    ev = {
        'active_referrers': active_refs(rel),
        'latent_referrers': latent_refs(rel),
        'documentation_referrers': doc_refs(rel),
        'name_only_referrers': name_refs(rel),
        'referrer_list': referrer_list(rel)[:10],
        'duplication_group': dup_membership[rel][0]['group_id'] if rel in dup_membership else None,
        'duplication_role': dup_membership[rel][1] if rel in dup_membership else None,
        'is_load_bearing': target_index.get(rel, {}).get('is_load_bearing', False),
        'prior_session_notes': f.get('prior_session_notes', [])[:3],
        'commits_last_30d': f.get('commits_last_30d', 0),
    }
    entry['evidence'] = ev

    # --- DECISION TREE ---

    # Step 1: karpathy — empty this run
    if rel in karpathy_set or f['path'] in karpathy_set:
        entry['action'] = 'KARPATHY-FLAG'
        entry['category'] = None
        entry['confidence'] = None
        entry['karpathy_observation'] = f'{f["lines"]} lines, {ev["active_referrers"]} active refs'
        entry['row_id'] = assign_row_id(layer, entry['action'])
        classified.append(entry)
        continue

    # Step 2: Empty shell
    if f['empty_shell']:
        entry['action'] = 'DELETE'
        entry['category'] = 'EMPTY-SHELL'
        entry['confidence'] = 'HIGH'
        entry['rationale'] = f'Empty shell — {f["content_lines"]} content lines, no substance to preserve.'
        entry['blast_radius'] = 'LOW' if ev['active_referrers'] == 0 else 'MEDIUM'
        entry['row_id'] = assign_row_id(layer, entry['action'])
        classified.append(entry)
        continue

    # Step 3: Template (SCAFFOLDING) or Instance
    if ev['duplication_role'] == 'template':
        entry['action'] = 'KEEP'
        entry['category'] = 'SCAFFOLDING'
        entry['confidence'] = 'HIGH'
        entry['rationale'] = f'Template of duplication group {ev["duplication_group"]} — parameterizable pattern its instances inhabit.'
        entry['current_usage'] = 'Template for state-file / similar pattern'
        entry['blast_radius'] = 'HIGH'
        entry['row_id'] = assign_row_id(layer, entry['action'])
        classified.append(entry)
        continue
    # Instances fall through to per-layer eval

    # Step 4: Duplication loser (stem_variant or heading_overlap, not template group)
    if ev['duplication_role'] == 'loser':
        g = dup_membership[rel][0]
        entry['action'] = 'DELETE'
        entry['category'] = 'DUPLICATE'
        entry['confidence'] = 'MEDIUM'  # MEDIUM because heading_overlap can be noisy
        entry['rationale'] = f'Duplicate of {g.get("recommended_survivor")} (group {g["group_id"]}, shape={g["shape"]}).'
        entry['blast_radius'] = 'LOW' if ev['active_referrers'] == 0 else 'MEDIUM'
        entry['row_id'] = assign_row_id(layer, entry['action'])
        classified.append(entry)
        continue

    # Step 5: Circular orphan — check referrer data
    t = target_index.get(rel, {})
    if t.get('is_orphan') and t.get('circular_cluster_id'):
        entry['action'] = 'DELETE'
        entry['category'] = 'CIRCULAR-ORPHAN'
        entry['confidence'] = 'HIGH'
        entry['rationale'] = f'Member of circular-orphan cluster {t["circular_cluster_id"]}; no external active referrers.'
        entry['blast_radius'] = 'LOW'
        entry['row_id'] = assign_row_id(layer, entry['action'])
        classified.append(entry)
        continue

    # Step 6: Auto-included steering referrer → UNCLEAR
    if rel in auto_include_targets and not (layer == 'steering' and f['inclusion_mode'] == 'auto'):
        entry['action'] = 'UNCLEAR'
        entry['category'] = 'AUTO-INCLUDED-REFERRER'
        entry['confidence'] = 'MEDIUM'
        entry['question_for_richard'] = f'{rel} is referenced from always-auto-loaded steering. Approve coordinated removal via separate spec, or keep?'
        entry['default_if_unanswered'] = 'KEEP (per R5.6 — coordinated removal needs separate spec)'
        entry['blast_radius'] = 'HIGH'
        entry['row_id'] = assign_row_id(layer, entry['action'])
        classified.append(entry)
        continue

    # Step 7: Orphan
    if ev['active_referrers'] == 0 and not (layer == 'steering' and f['inclusion_mode'] == 'auto'):
        entry['action'] = 'DELETE'
        entry['category'] = 'ORPHAN'
        entry['confidence'] = 'HIGH' if (ev['latent_referrers'] == 0 and ev['documentation_referrers'] <= 2) else 'MEDIUM'
        entry['rationale'] = f'Zero active referrers; {ev["latent_referrers"]} latent, {ev["documentation_referrers"]} documentation, {ev["name_only_referrers"]} name-only.'
        entry['blast_radius'] = 'LOW'
        entry['row_id'] = assign_row_id(layer, entry['action'])
        classified.append(entry)
        continue

    # Step 8: Dispatch by layer
    if layer == 'body':
        # B1: workflow dependency test
        # Crude heuristic: if file has 3+ active refs from hooks or agents (non-steering), it's INFORMATION
        active = ev['active_referrers']
        if active >= 3:
            entry['action'] = 'KEEP'
            entry['category'] = 'INFORMATION'
            entry['confidence'] = 'HIGH'
            entry['rationale'] = f'{active} active path referrers — workflows depend on this file.'
            entry['current_usage'] = 'Referenced by multiple agents/hooks'
            entry['blast_radius'] = 'HIGH' if ev['is_load_bearing'] else 'LOW'
            entry['needs_revisit'] = False  # High-usage file, classifier confident
        elif active >= 1:
            # Lightly used — UNCLEAR with question about future workflow
            entry['action'] = 'UNCLEAR'
            entry['category'] = 'BODY-LIGHTLY-USED'
            entry['confidence'] = 'LOW'
            entry['question_for_richard'] = f'{rel} has {active} active referrers. INFORMATION (keep) or METAPHOR-ONLY (delete)? Name the current workflow OR an L3-L5 future workflow that needs it.'
            entry['default_if_unanswered'] = 'KEEP'
            entry['blast_radius'] = 'MEDIUM'
        else:
            # Zero active referrers caught earlier as ORPHAN; shouldn't reach here
            entry['action'] = 'DELETE'
            entry['category'] = 'METAPHOR-ONLY-BODY'
            entry['confidence'] = 'MEDIUM'
            entry['rationale'] = 'Body organ with no active workflow dependency.'
            entry['blast_radius'] = 'LOW'
        entry['row_id'] = assign_row_id(layer, entry['action'])
        classified.append(entry)
        continue

    if layer == 'protocol':
        if ev['active_referrers'] >= 1:
            entry['action'] = 'KEEP'
            entry['category'] = 'ACTIVE-PROTOCOL'
            entry['confidence'] = 'HIGH'
            entry['rationale'] = f'{ev["active_referrers"]} active hook/agent references this protocol.'
            entry['current_usage'] = ', '.join(ev['referrer_list'][:3])
            entry['blast_radius'] = 'HIGH' if ev['is_load_bearing'] else 'LOW'
        else:
            # Shouldn't reach — orphan caught earlier
            entry['action'] = 'DELETE'
            entry['category'] = 'ORPHAN-PROTOCOL'
            entry['confidence'] = 'MEDIUM'
            entry['rationale'] = 'No active referrer, no named future workflow.'
            entry['blast_radius'] = 'LOW'
        entry['row_id'] = assign_row_id(layer, entry['action'])
        classified.append(entry)
        continue

    if layer == 'hook':
        if f['is_enabled'] is False:
            # H1: check description for dated rationale
            desc = f['purpose_line'] or ''
            if re.search(r'DISABLED \d{4}-\d{2}-\d{2}', desc):
                entry['action'] = 'KEEP'
                entry['category'] = 'INTENTIONALLY-DISABLED'
                entry['confidence'] = 'HIGH'
                entry['rationale'] = 'Disabled with dated rationale in description.'
                entry['blast_radius'] = 'LOW'
            else:
                entry['action'] = 'UNCLEAR'
                entry['category'] = 'UNDATED-DISABLED-HOOK'
                entry['confidence'] = 'LOW'
                entry['question_for_richard'] = f'{rel} is disabled without a dated rationale. Delete or document?'
                entry['default_if_unanswered'] = 'DELETE'
                entry['blast_radius'] = 'LOW'
            entry['row_id'] = assign_row_id(layer, entry['action'])
            classified.append(entry)
            continue

        # Enabled hook: keep by default, since it's actively firing
        entry['action'] = 'KEEP'
        entry['category'] = 'ACTIVE-HOOK'
        entry['confidence'] = 'HIGH'
        entry['rationale'] = 'Enabled hook, actively firing.'
        entry['blast_radius'] = 'LOW'
        entry['row_id'] = assign_row_id(layer, entry['action'])
        classified.append(entry)
        continue

    if layer == 'steering':
        if f['inclusion_mode'] == 'auto':
            entry['action'] = 'KEEP'
            entry['category'] = 'AUTO-STEERING'
            entry['confidence'] = 'MEDIUM'
            entry['rationale'] = f'Auto-loaded steering; {ev["active_referrers"]} path refs from elsewhere.'
            entry['current_usage'] = 'Loaded on every chat'
            entry['blast_radius'] = 'HIGH'
        else:  # conditional
            if ev['active_referrers'] > 0 or ev['latent_referrers'] > 0:
                entry['action'] = 'KEEP'
                entry['category'] = 'CONDITIONAL-STEERING-USED'
                entry['confidence'] = 'MEDIUM'
                entry['rationale'] = f'Conditional steering, {ev["active_referrers"]} active + {ev["latent_referrers"]} latent referrers.'
                entry['blast_radius'] = 'LOW'
            else:
                entry['action'] = 'DELETE'
                entry['category'] = 'CONDITIONAL-ORPHAN'
                entry['confidence'] = 'MEDIUM'
                entry['rationale'] = 'Conditional steering with no active or latent invocation.'
                entry['blast_radius'] = 'LOW'
        entry['row_id'] = assign_row_id(layer, entry['action'])
        classified.append(entry)
        continue

    # fallback
    entry['action'] = 'UNCLEAR'
    entry['category'] = 'UNKNOWN-LAYER'
    entry['question_for_richard'] = 'Layer not recognized — classify manually.'
    entry['default_if_unanswered'] = 'KEEP'
    entry['row_id'] = assign_row_id(layer, entry['action'])
    classified.append(entry)

# Summary
summary = {
    'delete_count': sum(1 for c in classified if c['action'] == 'DELETE'),
    'merge_count': sum(1 for c in classified if c['action'] == 'MERGE'),
    'unclear_count': sum(1 for c in classified if c['action'] == 'UNCLEAR'),
    'keep_count': sum(1 for c in classified if c['action'] == 'KEEP'),
    'karpathy_count': sum(1 for c in classified if c['action'] == 'KARPATHY-FLAG'),
    'broken_ref_count': 0,  # filled from broken_refs.json in render
    'estimated_lines_removed': sum(c['lines'] for c in classified if c['action'] == 'DELETE'),
    'per_layer': defaultdict(lambda: {'delete':0, 'merge':0, 'unclear':0, 'keep':0, 'karpathy':0}),
}
for c in classified:
    k = {'DELETE':'delete','MERGE':'merge','UNCLEAR':'unclear','KEEP':'keep','KARPATHY-FLAG':'karpathy'}[c['action']]
    summary['per_layer'][c['layer']][k] += 1
summary['per_layer'] = dict(summary['per_layer'])

out = {
    'generated_at': '2026-04-21T23:45:13-07:00',
    'files': classified,
    'summary': summary,
}
with open(OUT, 'w') as f:
    json.dump(out, f, indent=2)

# Hash for kill-list header
import hashlib
h = hashlib.sha256(open(OUT, 'rb').read()).hexdigest()
print(f"classified.json hash: sha256:{h[:16]}...")
print(f"Summary: {summary['delete_count']} DELETE, {summary['merge_count']} MERGE, {summary['unclear_count']} UNCLEAR, {summary['keep_count']} KEEP")
print(f"Estimated lines removed if all DELETE approved: {summary['estimated_lines_removed']}")
print(f"Per layer: {summary['per_layer']}")
