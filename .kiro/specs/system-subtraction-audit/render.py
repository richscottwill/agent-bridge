#!/usr/bin/env python3
"""Phase 5 — Render kill-list.md from classified.json."""
import json, hashlib, os
from collections import defaultdict

CL = '/home/prichwil/.kiro/specs/system-subtraction-audit/classified.json'
BR = '/home/prichwil/.kiro/specs/system-subtraction-audit/broken_refs.json'
OUT = '/home/prichwil/.kiro/specs/system-subtraction-audit/kill-list.md'

with open(CL) as f: cl = json.load(f)
with open(BR) as f: br = json.load(f)

# Hash
h = hashlib.sha256(open(CL, 'rb').read()).hexdigest()
cl_hash = f'sha256:{h}'

rows = cl['files']
summary = cl['summary']

# Group by layer then action
by_layer = defaultdict(lambda: defaultdict(list))
for r in rows:
    by_layer[r['layer']][r['action']].append(r)

# Sort rows within action by confidence desc then lines desc
conf_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, None: 3}
for layer in by_layer:
    for act in by_layer[layer]:
        by_layer[layer][act].sort(key=lambda r: (conf_order.get(r.get('confidence')), -r['lines']))

# Total lines per layer
with open('/home/prichwil/.kiro/specs/system-subtraction-audit/inventory.json') as f:
    inv = json.load(f)
inv_by_rel = {e['rel_path']: e for e in inv['files']}
layer_totals = inv['totals']

def fmt_row(r):
    lines = []
    hdr = f"#### {r['row_id']}. `{r['rel_path']}`  [{r['lines']} lines, {r.get('category','')}, {r.get('confidence','')} confidence]"
    lines.append(hdr)
    if r['action'] == 'DELETE':
        lines.append(f"- **Rationale**: {r.get('rationale','')}")
        lines.append(f"- **Active referrers**: {r['evidence']['active_referrers']}")
        if r['evidence']['latent_referrers']:
            lines.append(f"- **Latent referrers**: {r['evidence']['latent_referrers']}")
        if r['evidence']['documentation_referrers']:
            lines.append(f"- **Documentation-only referrers**: {r['evidence']['documentation_referrers']} (do not save from ORPHAN per R2.4)")
        lines.append(f"- **Blast radius**: {r.get('blast_radius','LOW')}")
        if r['evidence'].get('prior_session_notes'):
            lines.append(f"- **Prior context**: {r['evidence']['prior_session_notes'][0][:160]}")
    elif r['action'] == 'UNCLEAR':
        lines.append(f"- **Question**: {r.get('question_for_richard','')}")
        lines.append(f"- **Default if unanswered (30 days)**: {r.get('default_if_unanswered','KEEP')}")
        lines.append(f"- **Active referrers**: {r['evidence']['active_referrers']}")
        if r['evidence'].get('prior_session_notes'):
            lines.append(f"- **Prior context**: {r['evidence']['prior_session_notes'][0][:160]}")
    elif r['action'] == 'KEEP':
        lines.append(f"- **Rationale**: {r.get('rationale','')}")
        if r.get('current_usage'):
            lines.append(f"- **Current usage**: {r['current_usage'][:200]}")
        lines.append(f"- **Active referrers**: {r['evidence']['active_referrers']}  **Blast radius**: {r.get('blast_radius','LOW')}")
    elif r['action'] == 'MERGE':
        lines.append(f"- **Target**: {r.get('merge_target','')}")
        lines.append(f"- **Rationale**: {r.get('rationale','')}")
    elif r['action'] == 'KARPATHY-FLAG':
        lines.append(f"- **Observation**: {r.get('karpathy_observation','')}")
    return '\n'.join(lines) + '\n'

# Build markdown
md = []
md.append('# Kill List — System Subtraction Audit')
md.append('')
md.append(f'**Generated**: 2026-04-21T23:45:13-07:00')
md.append(f'**classified.json hash**: `{cl_hash}`')
md.append(f'**Files reviewed**: {len(rows)} across 4 layers')
md.append('')
md.append('**Karpathy carve-out**: WAIVED for this run per Richard. All files including heart.md, gut.md, hard-thing-selection.md, and experiments/* are classified normally.')
md.append('')
md.append('**Unsearched reference sources** (per R2.10): DuckDB rows, Asana task descriptions, Slack messages, Outlook emails. A file referenced only by these sources will appear orphaned here.')
md.append('')
md.append('## Summary')
md.append('')
md.append('**Per-layer**:')
md.append('')
md.append('| Layer     | Files | Lines | DELETE | MERGE | UNCLEAR | KEEP | KARPATHY |')
md.append('|-----------|-------|-------|--------|-------|---------|------|----------|')
for layer in ['body', 'protocol', 'hook', 'steering']:
    pl = summary['per_layer'].get(layer, {'delete':0,'merge':0,'unclear':0,'keep':0,'karpathy':0})
    # layer_totals uses 'protocols' and 'hooks' plural in the totals key
    totals_key = {'body':'body','protocol':'protocols','hook':'hooks','steering':'steering'}[layer]
    lyr_total = layer_totals.get(totals_key, {})
    md.append(f'| {layer:9s} | {lyr_total.get("files",0):5d} | {lyr_total.get("lines",0):5d} | {pl["delete"]:6d} | {pl["merge"]:5d} | {pl["unclear"]:7d} | {pl["keep"]:4d} | {pl["karpathy"]:8d} |')
md.append('')
md.append(f'**Aggregate**:')
md.append(f'- DELETE: {summary["delete_count"]} files (~{summary["estimated_lines_removed"]} lines)')
md.append(f'- MERGE: {summary["merge_count"]}')
md.append(f'- UNCLEAR: {summary["unclear_count"]}')
md.append(f'- KEEP: {summary["keep_count"]}')
md.append(f'- KARPATHY-FLAG: {summary["karpathy_count"]}')
md.append(f'- BROKEN REFS: {br["total_broken"]}')
md.append('')
md.append(f'**If all DELETE approved**: ~{summary["estimated_lines_removed"]} lines removed (~{100*summary["estimated_lines_removed"]/max(layer_totals["grand_total_lines"],1):.1f}% of current surface).')
md.append('')
md.append('---')
md.append('')
md.append('## Bulk Approval Block')
md.append('')
md.append('Edit this block to approve, veto, or defer rows. The executor only acts on explicitly APPROVED rows.')
md.append('')
md.append('Syntax:')
md.append('- `APPROVE: B-D1, B-D3, P-D1-P-D5` (IDs or ranges)')
md.append('- `VETO: P-D3` (block specific rows inside an approved range)')
md.append('- `DEFER: U1, U3` (explicitly carry to next cycle, suppresses default-if-unanswered)')
md.append('')
md.append('Absence of veto is NOT approval. Unapproved rows are skipped.')
md.append('')
md.append('```text')
md.append('APPROVE:')
md.append('VETO:')
md.append('DEFER:')
md.append('```')
md.append('')
md.append('---')
md.append('')
md.append('## How to use this file')
md.append('')
md.append('1. Read top-to-bottom. Each row is one file with a recommended action.')
md.append('2. Add row IDs to `APPROVE:` above to approve them for execution.')
md.append('3. Add row IDs to `VETO:` to block specific rows inside an approved range.')
md.append('4. Add UNCLEAR row IDs to `DEFER:` to suppress the default action.')
md.append('5. Rows you don\'t address remain for the next cycle.')
md.append('')
md.append('---')
md.append('')
md.append('## Incomplete classifications')
md.append('')
needs_revisit = [r for r in rows if r.get('needs_revisit')]
if needs_revisit:
    for r in needs_revisit:
        md.append(f'- {r["row_id"]}. {r["rel_path"]} — needs revisit')
else:
    md.append('*(none)*')
md.append('')
md.append('---')
md.append('')
md.append('## Broken references to fix (not audit candidates)')
md.append('')
if br['total_broken']:
    # Cap display to 20 for readability; note full list in broken_refs.json
    md.append(f'Total broken references found: **{br["total_broken"]}**. Full list in `broken_refs.json`. Showing 20 with highest referrer-concentration:')
    md.append('')
    referrer_counts = sorted(br['by_referrer'].items(), key=lambda kv: -len(kv[1]))[:20]
    for referrer, entries in referrer_counts:
        md.append(f'### {referrer} — {len(entries)} broken references')
        for e in entries[:5]:
            md.append(f'- Line {e["line_number"]}: `{e["broken_path"]}` — {e["suggested_action"]}')
        if len(entries) > 5:
            md.append(f'- *... and {len(entries)-5} more in this file*')
        md.append('')
else:
    md.append('*(none)*')
md.append('')
md.append('---')
md.append('')

# Per-layer sections
layer_display = {'body':'Body', 'protocol':'Protocols', 'hook':'Hooks', 'steering':'Steering'}
for layer in ['body', 'protocol', 'hook', 'steering']:
    totals_key = {'body':'body','protocol':'protocols','hook':'hooks','steering':'steering'}[layer]
    lyr_total = layer_totals.get(totals_key, {})
    md.append(f'## {layer_display[layer]} layer ({lyr_total.get("files",0)} files, {lyr_total.get("lines",0)} lines)')
    md.append('')
    for action in ['DELETE', 'MERGE', 'UNCLEAR', 'KEEP', 'KARPATHY-FLAG']:
        bucket = by_layer[layer][action]
        if not bucket:
            continue
        md.append(f'### {action} — {layer_display[layer].lower()} layer ({len(bucket)} rows)')
        md.append('')
        for r in bucket:
            md.append(fmt_row(r))
        md.append('')
    md.append('---')
    md.append('')

# Duplication groups summary
with open('/home/prichwil/.kiro/specs/system-subtraction-audit/duplication_groups.json') as f:
    dups = json.load(f)
md.append('## Duplication groups')
md.append('')
if dups['groups']:
    md.append('| ID | Shape | Members | Total lines | Survivor | Loser lines |')
    md.append('|----|-------|---------|-------------|----------|-------------|')
    for g in dups['groups']:
        if g['shape'] == 'template_plus_instances':
            md.append(f'| {g["group_id"]} | template+instances | {g["template"]} + {len(g["instances"])} instances | {g["aggregate_lines"]} | KEEP ALL | 0 |')
        else:
            mems = ', '.join(os.path.basename(m) for m in g['members'])
            md.append(f'| {g["group_id"]} | {g["shape"]} | {mems} | {g["aggregate_lines"]} | {os.path.basename(g.get("recommended_survivor",""))} | {g.get("loser_lines",0)} |')
else:
    md.append('*(no duplication groups detected)*')
md.append('')

# Write
with open(OUT, 'w') as f:
    f.write('\n'.join(md))

print(f"Wrote {OUT}")
print(f"Lines: {len(md)}")
