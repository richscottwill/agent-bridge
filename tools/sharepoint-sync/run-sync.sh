#!/bin/bash
# run-sync.sh — End-to-end wiki-to-SharePoint sync
#
# Phase 1: Convert eligible wiki articles to .docx (staging dir)
# Phase 2: Generate upload plan for agent to push via SharePoint MCP
#
# Usage:
#   bash run-sync.sh              # live sync + upload plan
#   bash run-sync.sh --dry-run    # phase 1 dry-run only
#   bash run-sync.sh --summary    # phase 1 live + phase 2 summary only

set -euo pipefail

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
DRY_RUN=""
SUMMARY=""

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN="--dry-run" ;;
        --summary) SUMMARY="--summary" ;;
    esac
done

echo "═══════════════════════════════════════════"
echo "  Phase 1: Convert wiki → .docx (staging)"
echo "═══════════════════════════════════════════"
python3 "$SCRIPT_DIR/cli.py" --mode directory $DRY_RUN --output-path "$SCRIPT_DIR/output"

if [ -n "$DRY_RUN" ]; then
    echo ""
    echo "Dry run complete. No files staged."
    exit 0
fi

echo ""
echo "═══════════════════════════════════════════"
echo "  Phase 2: Upload plan → SharePoint"
echo "═══════════════════════════════════════════"
python3 "$SCRIPT_DIR/sp-upload.py" $SUMMARY
