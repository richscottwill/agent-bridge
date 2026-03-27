#!/usr/bin/env bash
# Git Sync — push/pull shared/ and .kiro/ to personal git remote
# Usage: sync.sh [push|pull|status]

set -euo pipefail

REPO_DIR="/shared/user"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")

cd "$REPO_DIR"

case "${1:-status}" in
  push)
    echo "→ Adding tracked files..."
    git add -A
    
    # Check if there's anything to commit
    if git diff --cached --quiet 2>/dev/null; then
      echo "✓ Nothing to push — working tree clean."
      exit 0
    fi
    
    echo "→ Committing..."
    git commit -m "sync: $TIMESTAMP"
    
    echo "→ Pushing to remote..."
    git push -u origin main
    
    echo "✓ Pushed successfully."
    ;;
    
  pull)
    echo "→ Pulling from remote..."
    git pull origin main --rebase
    echo "✓ Pulled successfully."
    ;;
    
  status)
    echo "=== Git Sync Status ==="
    echo ""
    echo "Remote:"
    git remote -v 2>/dev/null || echo "  (no remote configured)"
    echo ""
    echo "Branch:"
    git branch -v 2>/dev/null || echo "  (no commits yet)"
    echo ""
    echo "Changed files:"
    git status --short shared/ .kiro/ 2>/dev/null || echo "  (no changes)"
    ;;
    
  *)
    echo "Usage: sync.sh [push|pull|status]"
    exit 1
    ;;
esac
