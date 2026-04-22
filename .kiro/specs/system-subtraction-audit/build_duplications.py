#!/usr/bin/env python3
"""Phase 3 — duplication detection with template+instances protection."""
import json, re, os
from collections import defaultdict
from statistics import median

INV = '/home/prichwil/.kiro/specs/system-subtraction-audit/inventory.json'
REFS = '/home/prichwil/.kiro/specs/system-subtraction-audit/referrers.json'
OUT = '/home/prichwil/.kiro/specs/system-subtraction-audit/duplication_groups.json'

with open(INV) as f:
    inv = json.load(f)
with open(REFS) as f:
    refs = json.load(f)

files = inv['files']
by_path = {e['path']: e for e in files}

# Step 1: stem groups
VARIANT_SUFFIXES = ['-v2', '-new', '-parallel', '-old', '-draft', '-backend', '-frontend']

def stem(name):
    base = name
    if base.endswith('.md') or base.endswith('.hook'):
        base = base.rsplit('.', 1)[0]
    # Try each variant; greedy-strip
    for suf in VARIANT_SUFFIXES:
        if base.endswith(suf):
            base = base[:-len(suf)]
            break
    return base

# Group by (layer, stem)
stem_groups = defaultdict(list)
for f in files:
    basename = os.path.basename(f['path'])
    s = stem(basename)
    # Only consider if stem is nontrivial
    if len(s) < 3:
        continue
    stem_groups[(f['layer'], s)].append(f)

# Prune to groups of 2+
stem_groups = {k: v for k, v in stem_groups.items() if len(v) >= 2}

# Step 2: template + instances detection
# Template: largest member ≥2x median of group lines AND cross-referenced by smaller members via path
groups = []
gid = 0

# Build quick referrer lookup (who references target via path)
# refs['edges'] has from/to/match_type
active_path_edges = [e for e in refs['edges'] if e['match_type'] == 'path']
# For each target rel_path, set of path referrers
refs_of = defaultdict(set)
for e in active_path_edges:
    refs_of[e['to']].add(e['from'])

for (layer, s), members in stem_groups.items():
    if len(members) < 2:
        continue
    lines_list = sorted([m['lines'] for m in members])
    med = median(lines_list)
    members_sorted = sorted(members, key=lambda x: -x['lines'])
    largest = members_sorted[0]
    others = members_sorted[1:]
    gid += 1

    # Template detection
    is_template = False
    if largest['lines'] >= 2 * max(med, 1):
        # Does any smaller member have a path reference TO the largest?
        for m in others:
            # Check if largest's rel_path appears in m's content
            try:
                with open(m['path']) as f:
                    content = f.read()
                if os.path.basename(largest['path']) in content or largest['rel_path'] in content:
                    is_template = True
                    break
            except Exception:
                continue

    if is_template:
        groups.append({
            'group_id': f'tmpl-{gid}',
            'shape': 'template_plus_instances',
            'template': largest['rel_path'],
            'instances': [m['rel_path'] for m in others],
            'stem': s,
            'layer': layer,
            'rationale': f'{os.path.basename(largest["path"])} is {largest["lines"]}L vs others (median {med}); at least one instance path-references template',
            'aggregate_lines': sum(m['lines'] for m in members),
        })
    else:
        # Designate survivor: most recent mtime + most active referrers
        def score(f):
            active = refs['by_target'].get(f['rel_path'], {}).get('active_path_referrers', 0)
            return (active, f['last_modified'])
        members_ranked = sorted(members, key=score, reverse=True)
        survivor = members_ranked[0]
        groups.append({
            'group_id': f'dup-{gid}',
            'shape': 'stem_variant',
            'members': [m['rel_path'] for m in members],
            'stem': s,
            'layer': layer,
            'recommended_survivor': survivor['rel_path'],
            'survivor_rationale': f'most recent + {refs["by_target"].get(survivor["rel_path"],{}).get("active_path_referrers",0)} active referrers',
            'aggregate_lines': sum(m['lines'] for m in members),
            'loser_lines': sum(m['lines'] for m in members if m['rel_path'] != survivor['rel_path']),
        })

# Step 3: heading-overlap groups (skip for files already in a stem group)
already_grouped = set()
for g in groups:
    if g['shape'] == 'template_plus_instances':
        already_grouped.add(g['template'])
        already_grouped.update(g['instances'])
    else:
        already_grouped.update(g['members'])

def extract_headings(path):
    try:
        with open(path) as f:
            content = f.read()
    except Exception:
        return set()
    # First 100 lines
    lines = content.splitlines()[:100]
    heads = set()
    for ln in lines:
        m = re.match(r'^(##?)\s+(.+)', ln)
        if m:
            heads.add(m.group(2).strip())
    return heads

# Only compare within same layer, and only md files
candidates = [f for f in files if f['rel_path'] not in already_grouped and f['path'].endswith('.md')]
heading_map = {f['rel_path']: extract_headings(f['path']) for f in candidates}

overlap_pairs = []
by_layer_cand = defaultdict(list)
for f in candidates:
    by_layer_cand[f['layer']].append(f)

for layer, items in by_layer_cand.items():
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            ha = heading_map[a['rel_path']]
            hb = heading_map[b['rel_path']]
            if len(ha) < 3 or len(hb) < 3:
                continue
            shared = ha & hb
            if len(shared) == 0:
                continue
            ratio = len(shared) / max(len(ha), len(hb))
            if ratio > 0.5:
                overlap_pairs.append((a, b, shared, ratio))

# Merge overlap pairs into groups by transitive closure (union-find light)
parent = {}
def find(x):
    while parent.get(x, x) != x:
        parent[x] = parent.get(parent[x], parent[x])
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb

for a, b, _, _ in overlap_pairs:
    union(a['rel_path'], b['rel_path'])

overlap_clusters = defaultdict(list)
for a, b, _, _ in overlap_pairs:
    root = find(a['rel_path'])
    overlap_clusters[root].append(a['rel_path'])
    overlap_clusters[root].append(b['rel_path'])

for root, members_raw in overlap_clusters.items():
    members_set = sorted(set(members_raw))
    if len(members_set) < 2:
        continue
    member_entries = [next(f for f in files if f['rel_path'] == m) for m in members_set]
    gid += 1
    # Pick survivor: most recent + most referrers
    def score(f):
        active = refs['by_target'].get(f['rel_path'], {}).get('active_path_referrers', 0)
        return (active, f['last_modified'])
    survivor = sorted(member_entries, key=score, reverse=True)[0]
    shared_all = set.intersection(*[heading_map[m] for m in members_set])
    groups.append({
        'group_id': f'ovl-{gid}',
        'shape': 'heading_overlap',
        'members': members_set,
        'layer': member_entries[0]['layer'],
        'shared_headings': sorted(shared_all),
        'recommended_survivor': survivor['rel_path'],
        'aggregate_lines': sum(m['lines'] for m in member_entries),
        'loser_lines': sum(m['lines'] for m in member_entries if m['rel_path'] != survivor['rel_path']),
    })

out = {
    'generated_at': '2026-04-21T23:45:13-07:00',
    'groups': groups,
    'totals': {
        'total_groups': len(groups),
        'template_groups': sum(1 for g in groups if g['shape'] == 'template_plus_instances'),
        'stem_variant_groups': sum(1 for g in groups if g['shape'] == 'stem_variant'),
        'heading_overlap_groups': sum(1 for g in groups if g['shape'] == 'heading_overlap'),
        'potential_lines_removed': sum(g.get('loser_lines', 0) for g in groups),
    }
}
with open(OUT, 'w') as f:
    json.dump(out, f, indent=2)

print(f"Groups: {out['totals']}")
for g in groups:
    if g['shape'] == 'template_plus_instances':
        print(f"  TMPL  {g['group_id']} {g['template']}  + {len(g['instances'])} instances")
    else:
        print(f"  DUP   {g['group_id']} {g['shape']} {len(g['members'])} members, loses {g.get('loser_lines',0)}L")
