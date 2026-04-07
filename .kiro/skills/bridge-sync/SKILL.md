---
name: bridge-sync
description: "Sync files to shared/context/ directory, update docs, push to agent-bridge GitHub repo, send snapshot email. Triggers on sync to git, bridge sync, portable body, agent bridge."
---

# Bridge Sync

## Instructions

1. **Identify changed files** — Check which body organs, steering files, and artifacts have been modified since the last sync.
2. **Sync to shared/context/** — Copy updated files to the shared/context/ directory, preserving the directory structure.
3. **Update documentation** — Ensure README and any index files in shared/context/ reflect the current state.
4. **Push to agent-bridge repo** — Run `scripts/sync.sh` to commit and push changes to the agent-bridge GitHub repository.
5. **Send snapshot email** — Optionally send a snapshot summary email with the list of changed files and a brief description of changes.

## Notes

- The agent-bridge repo is the survival kit — it must contain everything needed for a cold start on a new platform.
- Portability mindset: every file synced should be understandable without access to hooks, MCP servers, or subagents.
- Use #git diff before syncing to preview what changed.
