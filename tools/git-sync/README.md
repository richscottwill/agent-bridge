# Git Sync — DevSpaces ↔ Local Machine

Syncs `~/shared/` and `~/.kiro/` between the DevSpaces container and a personal git repo.

## How It Works

- The home directory (`~`) is a git repo tracking only `shared/` and `.kiro/` (everything else is gitignored)
- A personal GitHub repo acts as the relay between container and local machine
- `sync.sh` handles commit + push/pull with a single command

## Setup (one-time, both sides)

### In DevSpaces (this container):
```bash
# 1. Add your GitHub repo as remote
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git

# 2. Store credentials (GitHub PAT)
git config credential.helper store
echo "https://YOUR_USER:YOUR_TOKEN@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials

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

- `shared/` — context, artifacts, tools, research, meetings, wiki
- `.kiro/` — agents, hooks, steering, specs, settings

## What Does NOT Get Synced

- Auth tokens, AWS credentials, SSH keys
- IDE caches, browser data, build artifacts
- `.arcc/`, `.hypothesis/`, `.cache/`, `.local/`

## Portability Note

This is just git. No proprietary tooling. Any machine with git can clone the repo and have the full system. A new AI on a different platform would understand this without any special setup.
