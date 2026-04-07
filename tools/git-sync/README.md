<!-- DOC-0414 | duck_id: tool-README -->
# Git Sync — DevSpaces ↔ Local Machine

Syncs `~/shared/` and `~/.kiro/` between the DevSpaces container and a personal git repo.

## How It Works

- The git repo lives at `/shared/user/` (the real path behind `~/shared/`)
- This EFS volume persists across container restarts
- `.kiro/` lives inside `/shared/user/.kiro/` (symlinked from `~/.kiro`)
- A personal GitHub repo acts as the relay between container and local machine
- `sync.sh` handles commit + push/pull with a single command

## Setup (one-time, both sides)

### In DevSpaces (this container):
```bash
# 1. Add your GitHub repo as remote (MAKE THE REPO PRIVATE)
git -C /shared/user remote add origin https://github.com/YOUR_USER/YOUR_REPO.git

# 2. Store credentials (GitHub PAT with repo scope)
git -C /shared/user config credential.helper store
echo "https://YOUR_USER:YOUR_TOKEN@github.com" > /shared/user/.git-credentials
chmod 600 /shared/user/.git-credentials

# 3. Initial push
~/shared/tools/git-sync/sync.sh push
```

### On your local machine:
```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USER/YOUR_REPO.git rw-system

# 2. Pull updates anytime
cd rw-system && git pull
```

## Usage

```bash
# Push local changes to remote
~/shared/tools/git-sync/sync.sh push

# Pull remote changes to local
~/shared/tools/git-sync/sync.sh pull

# Check status
~/shared/tools/git-sync/sync.sh status
```

## What Gets Synced

- `context/` — body organs, active state, meetings, wiki, intake, archive
- `artifacts/` — published wiki articles (testing, strategy, reporting, etc.)
- `tools/` — bridge, dashboard-ingester, git-sync, sharepoint-sync, progress-charts
- `research/` — ad copy results, competitor intel, test docs, excel analyses
- `reference/` — static reference material
- `.kiro/` — agents, hooks, steering, specs, settings

## What Does NOT Get Synced

- `credentials/` — secrets and auth tokens
- `agentspaces-desktop-launcher/` — local-only launcher
- `audit-reports/` — regenerable
- `.agentspaces/`, `.aim/`, `.smithy-mcp/` — runtime state
- `.kiro/powers/`, `.kiro/mcp-servers-reference.json` — runtime
- `*.tar.gz`, `*.sqlite3`, `*.log` — binaries and logs

## Portability Note

This is just git. No proprietary tooling. Any machine with git can clone the repo and have the full system. A new AI on a different platform would understand this without any special setup.
