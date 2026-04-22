#!/usr/bin/env python3
"""Phase 2 tasks 2.1-2.5: referrer graph + broken refs.

Scope per R2.8:
  ~/.kiro/**, ~/shared/context/**, ~/shared/wiki/**,
  ~/shared/tools/**, ~/shared/scripts/**, ~/shared/dashboards/**

Match types per R2.2:
  path  — resolvable path from a live file
  latent — resolvable path from a disabled hook or conditional steering
  documentation — resolvable path inside a wiki/spec/README/*-docs/*-guide
  name — bare filename only
"""
import json, subprocess, re, os, sys
from collections import defaultdict

INV = '/home/prichwil/.kiro/specs/system-subtraction-audit/inventory.json'
OUT_REFS = '/home/prichwil/.kiro/specs/system-subtraction-audit/referrers.json'
OUT_BROKEN = '/home/prichwil/.kiro/specs/system-subtraction-audit/broken_refs.json'

# Search roots
SEARCH_ROOTS = [
    '/home/prichwil/.kiro',
    '/home/prichwil/shared/context',
    '/home/prichwil/shared/wiki',
    '/home/prichwil/shared/tools',
    '/home/prichwil/shared/scripts',
    '/home/prichwil/shared/dashboards',
]
SEARCH_ROOTS = [p for p in SEARCH_ROOTS if os.path.isdir(p)]

with open(INV) as f:
    inventory = json.load(f)

files_by_path = {e['path']: e for e in inventory['files']}
files_by_rel = {e['rel_path']: e for e in inventory['files']}
all_files = list(inventory['files'])

# Map each file to its liveness
def is_live(entry):
    if entry['layer'] == 'hook':
        return bool(entry['is_enabled'])
    if entry['layer'] == 'steering':
        return entry['inclusion_mode'] == 'auto'
    # body, protocol: treat as live (they're always potentially loaded)
    return True

# Documentation-file detection: path-based
DOC_PATH_PATTERNS = [
    r'/shared/wiki/',
    r'/\.kiro/specs/',
]
DOC_NAME_PATTERNS = [
    r'README\.md$',
    r'CHANGELOG\.md$',
    r'-docs\.md$',
    r'-guide\.md$',
]

def is_doc_file(path):
    for p in DOC_PATH_PATTERNS:
        if re.search(p, path):
            return True
    for p in DOC_NAME_PATTERNS:
        if re.search(p, path):
            return True
    return False

# Load all candidate referrer files once
# (every text file under the search roots)
print("Scanning corpus...", file=sys.stderr)
corpus = {}  # path -> content
for root in SEARCH_ROOTS:
    for dirpath, dirnames, filenames in os.walk(root):
        # skip .git, node_modules, __pycache__
        dirnames[:] = [d for d in dirnames if d not in ('.git', 'node_modules', '__pycache__', '.venv')]
        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            # skip binaries and large files
            try:
                st = os.stat(fp)
                if st.st_size > 2_000_000:  # 2MB cap
                    continue
                with open(fp, 'rb') as f:
                    b = f.read()
                # quick binary detection
                if b'\x00' in b[:1000]:
                    continue
                corpus[fp] = b.decode('utf-8', errors='replace')
            except Exception:
                continue
print(f"Corpus: {len(corpus)} files", file=sys.stderr)

# Liveness of referring files
referring_liveness = {}  # path -> bool
for fp in corpus:
    if fp in files_by_path:
        referring_liveness[fp] = is_live(files_by_path[fp])
    else:
        # external file — default live
        referring_liveness[fp] = True

# For each inventory target, find referrers
edges = []
by_target = defaultdict(lambda: {
    'active_path_referrers': 0,
    'latent_referrers': 0,
    'documentation_referrers': 0,
    'name_only_referrers': 0,
    'referrers_detail': [],
})
broken_refs_by_referrer = defaultdict(list)

# Build two patterns per target:
#   - path pattern: rel_path OR abspath OR #[[file:rel_path]]
#   - name pattern: bare basename outside a path context
for target in all_files:
    rel = target['rel_path']
    ab = target['path']
    basename = os.path.basename(ab)

    # Escape for regex
    rel_re = re.escape(rel)
    ab_re = re.escape(ab)
    # Include form: #[[file:~/shared/... or absolute
    include_re = r'#\[\[file:\s*' + re.escape(rel) + r'\s*\]\]'
    include_re_ab = r'#\[\[file:\s*' + re.escape(ab) + r'\s*\]\]'
    # Relative path with at least one slash (path-style without ~ or /home)
    # e.g. "protocols/foo.md" "body/brain.md"
    path_like_re = None
    # We check for basename preceded by a directory component
    # The 'path' class requires a / or ~ prefix; a bare filename doesn't.
    path_combined = re.compile(
        '(?:' + rel_re + '|' + ab_re + '|' + include_re + '|' + include_re_ab + ')'
    )
    # For protocol-directory relative form (e.g. "protocols/am-backend.md")
    # Build from layer
    layer_dir_map = {
        'body': 'body/',
        'protocol': 'protocols/',
        'hook': 'hooks/',
        'steering': 'steering/',
    }
    layer_prefix = layer_dir_map.get(target['layer'], '')
    if layer_prefix:
        rel_short = layer_prefix + basename
        path_combined = re.compile(
            '(?:' + rel_re + '|' + ab_re + '|' + include_re + '|' + include_re_ab + '|' + re.escape(rel_short) + ')'
        )

    # Name-only pattern: basename that does NOT have a leading path separator / ~ /home
    name_re = re.compile(r'(?<![A-Za-z0-9_./~-])' + re.escape(basename) + r'(?![A-Za-z0-9_./-])')

    for ref_path, content in corpus.items():
        if ref_path == ab:
            continue  # don't count self
        # Path hit first
        found_path = False
        for m in path_combined.finditer(content):
            found_path = True
            # Determine match type
            if is_doc_file(ref_path):
                mt = 'documentation'
            elif not referring_liveness.get(ref_path, True):
                mt = 'latent'
            else:
                mt = 'path'
            # Line number
            line_no = content[:m.start()].count('\n') + 1
            ctx = content.splitlines()[line_no - 1] if line_no - 1 < len(content.splitlines()) else ''
            edges.append({
                'from': ref_path.replace('/home/prichwil/', '~/'),
                'to': rel,
                'match_type': mt,
                'line_number': line_no,
                'context': ctx.strip()[:200],
            })
            if mt == 'path':
                by_target[rel]['active_path_referrers'] += 1
            elif mt == 'latent':
                by_target[rel]['latent_referrers'] += 1
            elif mt == 'documentation':
                by_target[rel]['documentation_referrers'] += 1
            if ref_path.replace('/home/prichwil/', '~/') not in by_target[rel]['referrers_detail']:
                by_target[rel]['referrers_detail'].append(ref_path.replace('/home/prichwil/', '~/'))
        # Only count name-only if no path hit from this referrer
        if not found_path:
            nm = name_re.search(content)
            if nm:
                by_target[rel]['name_only_referrers'] += 1

# Detect broken references: path references in corpus pointing to files not on disk
# Search for #[[file:...]] and ~/shared/... and .kiro/... paths
print("Scanning broken refs...", file=sys.stderr)
path_ref_re = re.compile(r'(?:#\[\[file:\s*)?(~\/[A-Za-z0-9_./-]+\.md|~\/[A-Za-z0-9_./-]+\.hook|/home/prichwil/[A-Za-z0-9_./-]+\.md|/home/prichwil/[A-Za-z0-9_./-]+\.hook)(?:\s*\]\])?')

known_paths = set(e['path'] for e in all_files)
known_paths |= set(e['rel_path'] for e in all_files)

for ref_path, content in corpus.items():
    for m in path_ref_re.finditer(content):
        p = m.group(1)
        # Resolve ~ to /home/prichwil
        resolved = p.replace('~/', '/home/prichwil/', 1) if p.startswith('~/') else p
        if os.path.exists(resolved):
            continue
        # Broken
        line_no = content[:m.start()].count('\n') + 1
        ctx = content.splitlines()[line_no - 1] if line_no - 1 < len(content.splitlines()) else ''
        # Heuristic suggestion
        basename = os.path.basename(resolved)
        alt_matches = [e['rel_path'] for e in all_files if os.path.basename(e['path']) == basename]
        if alt_matches:
            suggested = f"update path to {alt_matches[0]} (file exists there)"
        else:
            suggested = "remove reference OR create target file"
        rel_ref = ref_path.replace('/home/prichwil/', '~/')
        # Skip if the "broken" ref is in our own spec (referencing hypothetical files during design)
        if '.kiro/specs/system-subtraction-audit' in rel_ref:
            continue
        broken_refs_by_referrer[rel_ref].append({
            'broken_path': p,
            'line_number': line_no,
            'context': ctx.strip()[:200],
            'suggested_action': suggested,
        })

# Orphan + load-bearing flags
for target in all_files:
    rel = target['rel_path']
    t = by_target[rel]
    t['is_orphan'] = (t['active_path_referrers'] == 0
                     and not (target['layer'] == 'steering' and target['inclusion_mode'] == 'auto'))
    t['is_load_bearing'] = t['active_path_referrers'] >= 3

# Circular cluster detection (Tarjan's SCC over active-path edges among inventory files)
graph = defaultdict(set)  # from_rel -> set(to_rel)
inv_rel_set = set(files_by_rel.keys())
for e in edges:
    if e['match_type'] != 'path':
        continue
    if e['to'] not in inv_rel_set:
        continue
    # from must also be in inventory to count as internal edge
    # e['from'] is rel_path form
    from_key = e['from']
    # Convert to matching form
    if from_key in inv_rel_set:
        graph[from_key].add(e['to'])

# Tarjan's SCC
index_counter = [0]
stack = []
lowlinks = {}
index = {}
on_stack = {}
result = []

def strongconnect(node):
    index[node] = index_counter[0]
    lowlinks[node] = index_counter[0]
    index_counter[0] += 1
    stack.append(node)
    on_stack[node] = True
    for successor in graph.get(node, ()):
        if successor not in index:
            strongconnect(successor)
            lowlinks[node] = min(lowlinks[node], lowlinks[successor])
        elif on_stack.get(successor):
            lowlinks[node] = min(lowlinks[node], index[successor])
    if lowlinks[node] == index[node]:
        component = []
        while True:
            successor = stack.pop()
            on_stack[successor] = False
            component.append(successor)
            if successor == node:
                break
        result.append(component)

sys.setrecursionlimit(5000)
for node in list(graph.keys()):
    if node not in index:
        strongconnect(node)

circular_clusters = []
cluster_id = 0
for comp in result:
    if len(comp) < 2:
        continue
    cluster_id += 1
    cid = f'cc-{cluster_id}'
    # External active referrers: any active-path edge TO a member FROM a non-member
    members = set(comp)
    external = 0
    for e in edges:
        if e['match_type'] != 'path':
            continue
        if e['to'] in members and e['from'] not in members:
            external += 1
    circular_clusters.append({
        'cluster_id': cid,
        'members': sorted(comp),
        'external_active_referrers': external,
        'is_cluster_orphan': external == 0
    })
    # Tag each member
    for m in members:
        by_target[m]['circular_cluster_id'] = cid
        if external == 0:
            by_target[m]['is_orphan'] = True

# Write outputs
refs_out = {
    'generated_at': '2026-04-21T23:45:13-07:00',
    'corpus_size': len(corpus),
    'edges': edges,
    'by_target': dict(by_target),
    'circular_clusters': circular_clusters,
}
with open(OUT_REFS, 'w') as f:
    json.dump(refs_out, f, indent=2)

broken_out = {
    'generated_at': '2026-04-21T23:45:13-07:00',
    'total_broken': sum(len(v) for v in broken_refs_by_referrer.values()),
    'by_referrer': dict(broken_refs_by_referrer),
}
with open(OUT_BROKEN, 'w') as f:
    json.dump(broken_out, f, indent=2)

print(f"Edges: {len(edges)}")
print(f"Active path referrers >=1 files: {sum(1 for t in by_target.values() if t['active_path_referrers']>0)}")
print(f"Orphans: {sum(1 for t in by_target.values() if t['is_orphan'])}")
print(f"Load-bearing: {sum(1 for t in by_target.values() if t['is_load_bearing'])}")
print(f"Circular clusters: {len(circular_clusters)}")
print(f"Broken refs: {broken_out['total_broken']}")
