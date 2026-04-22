#!/usr/bin/env python3
"""Phase 6 executor — deletes 9 approved files, updates 1 referrer, writes execution.log.

Per R9: append-only line-JSON log, stops on error, atomic per-row.
Resume-safe: checks log for prior row_completed entries before acting.
"""
import json, os, sys, datetime, hashlib, subprocess

SPEC = '/home/prichwil/.kiro/specs/system-subtraction-audit'
LOG = f'{SPEC}/execution.log'
KILL = f'{SPEC}/kill-list.md'
CL = f'{SPEC}/classified.json'

def now():
    return datetime.datetime.now().astimezone().isoformat(timespec='seconds')

def log(event, **kw):
    entry = {'timestamp': now(), 'event': event, **kw}
    with open(LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    print(f'  [{event}] {json.dumps(kw)[:120]}')

def already_completed(row_id):
    if not os.path.exists(LOG):
        return False
    with open(LOG) as f:
        for line in f:
            try:
                e = json.loads(line)
                if e.get('event') == 'row_completed' and e.get('row_id') == row_id:
                    return True
            except json.JSONDecodeError:
                pass
    return False

# Approved rows (from walkthrough)
APPROVED = [
    # (row_id, action, target_path, optional_note)
    ('S-D3', 'DELETE', '/home/prichwil/.kiro/steering/context/context-provider-recommendations.md', None),
    ('S-D4', 'DELETE', '/home/prichwil/.kiro/steering/context/kiro-limitations.md', None),
    ('S-D5', 'DELETE', '/home/prichwil/.kiro/steering/context/powers-evaluation.md', None),
    ('S-D6', 'DELETE', '/home/prichwil/.kiro/steering/context/steering-integrity.md', None),
    ('S-D1', 'DELETE', '/home/prichwil/.kiro/steering/agentspaces-core.md', 'duplicate of environment-rules.md'),
    ('MANUAL-1', 'DELETE', '/home/prichwil/.kiro/steering/devspaces-core.md', 'duplicate of environment-rules.md — audit missed, Richard added'),
    ('H-D1', 'DELETE', '/home/prichwil/.kiro/hooks/dashboard-server.kiro.hook', 'redundant to .bashrc autostart'),
    ('P-D1', 'DELETE', '/home/prichwil/shared/context/protocols/am-backend.md', 'duplicate of am-backend-parallel.md'),
    ('B-U2', 'DELETE', '/home/prichwil/shared/context/body/body-diagram.md', '1 live referrer in changelog.md — will be updated'),
]

# Hashes for integrity check
cl_hash = hashlib.sha256(open(CL, 'rb').read()).hexdigest()

# Emit run_started
log('run_started',
    run_id=f'exec-{datetime.date.today().isoformat()}-01',
    classified_hash=f'sha256:{cl_hash[:16]}...',
    approved_count=len(APPROVED))

# Special case: update changelog.md to note body-diagram deletion (the 1 live referrer)
try:
    changelog_path = '/home/prichwil/shared/context/body/changelog.md'
    if os.path.exists(changelog_path):
        with open(changelog_path) as f:
            content = f.read()
        # Find the line referencing body-diagram.md and prepend a deletion note
        today = datetime.date.today().isoformat()
        deletion_note = f"\n## {today} — body-diagram.md DELETED via system-subtraction-audit\n\nbody/body-diagram.md removed (181 lines, METAPHOR-ONLY per audit). The only live referrer was this changelog; reference preserved below for history.\n"
        # Prepend as the newest entry. Changelog typically starts with "# Changelog" heading; insert after that.
        lines = content.splitlines(True)
        # Find first line after the title
        insert_idx = 1
        for i, ln in enumerate(lines):
            if i > 0 and ln.strip() and not ln.startswith('#'):
                insert_idx = i
                break
            if i > 0 and ln.startswith('## '):
                insert_idx = i
                break
        new_content = ''.join(lines[:insert_idx]) + deletion_note + '\n' + ''.join(lines[insert_idx:])
        with open(changelog_path, 'w') as f:
            f.write(new_content)
        log('referrer_updated',
            row_id='changelog-prep',
            referrer=changelog_path,
            action='prepended deletion note for body-diagram.md')
except Exception as e:
    log('error', stage='changelog_prep', error=str(e))
    print(f'FAILED to update changelog: {e}', file=sys.stderr)
    sys.exit(1)

# Execute deletions
results = {'completed': 0, 'skipped': 0, 'failed': 0}
for row_id, action, target, note in APPROVED:
    if already_completed(row_id):
        log('row_skipped', row_id=row_id, reason='already completed in prior run')
        results['skipped'] += 1
        continue

    if not os.path.exists(target):
        log('row_skipped', row_id=row_id, reason='target does not exist', target=target)
        results['skipped'] += 1
        continue

    log('row_started', row_id=row_id, action=action, target=target, note=note or '')

    try:
        bytes_removed = os.path.getsize(target)
        os.remove(target)
        log('row_completed',
            row_id=row_id,
            action=action,
            target=target,
            bytes_removed=bytes_removed)
        results['completed'] += 1
    except Exception as e:
        log('row_stopped', row_id=row_id, error=str(e))
        results['failed'] += 1
        print(f'STOPPED on {row_id}: {e}', file=sys.stderr)
        break  # Stop on error per R9

# Emit run_completed
log('run_completed', **results)

# git commit
try:
    # Commit from /home/prichwil (home dir, git repo root for shared + .kiro?)
    # Check which repos are involved
    shared_repo = '/home/prichwil/shared'
    kiro_repo = '/home/prichwil/.kiro'
    # Only commit if changes are in a git repo
    for repo in [shared_repo, kiro_repo]:
        r = subprocess.run(['git', '-C', repo, 'status', '--short'],
                         capture_output=True, text=True, timeout=10)
        if r.stdout.strip():
            print(f'\nChanges in {repo}:')
            print(r.stdout)
            # stage + commit
            subprocess.run(['git', '-C', repo, 'add', '-A'], check=False)
            msg = f'audit: system-subtraction-audit — {results["completed"]} files deleted ({datetime.date.today().isoformat()})'
            r2 = subprocess.run(['git', '-C', repo, 'commit', '-m', msg],
                              capture_output=True, text=True, timeout=20)
            print(r2.stdout)
            if r2.returncode != 0:
                print(r2.stderr)
except Exception as e:
    log('git_commit_error', error=str(e))
    print(f'Git commit issue: {e}', file=sys.stderr)

print(f'\nExecution complete: {results}')
