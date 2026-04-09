#!/bin/bash
# WBR Pipeline — Single command to run the full weekly callout pipeline
#
# Usage: ./wbr-pipeline.sh <xlsx_path> [--week 2026-W15]
#
# Steps:
#   1. Ingest xlsx (all 10 markets, all KPIs)
#   2. Sync weekly/daily/ie%CCP data to MotherDuck ps.performance
#   3. Score last week's predictions against this week's actuals
#   4. Generate next-week/month/quarter projections (Brand/NB split + ie%CCP)
#   5. Output: callout drafts, data briefs, projection tables, WW summary
#
# After this script completes, trigger the WBR callout skill for writing + review.

set -euo pipefail

XLSX_PATH="${1:?Usage: wbr-pipeline.sh <xlsx_path> [--week 2026-WNN]}"
WEEK_ARG="${3:-}"  # optional --week value

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INGESTER="$SCRIPT_DIR/dashboard-ingester/ingest.py"
PROJECTOR="$SCRIPT_DIR/prediction/project.py"

echo "═══════════════════════════════════════════"
echo "  WBR Pipeline"
echo "═══════════════════════════════════════════"
echo ""

# ── Step 1: Ingest xlsx ──
echo "Step 1: Ingesting $XLSX_PATH..."
python3 "$INGESTER" "$XLSX_PATH" --db none
echo ""

# ── Detect week from ingester output ──
# The ingester prints "Target week: 2026 WNN" — parse it
if [ -z "$WEEK_ARG" ]; then
    DETECTED=$(python3 "$INGESTER" "$XLSX_PATH" --db none 2>&1 | head -1 | grep -oP '20\d{2} W\d+' || true)
    if [ -n "$DETECTED" ]; then
        CURRENT_WEEK=$(echo "$DETECTED" | sed 's/ /-/')
    else
        echo "ERROR: Could not detect week. Pass --week explicitly."
        exit 1
    fi
else
    CURRENT_WEEK="$WEEK_ARG"
fi

WEEK_NUM=$(echo "$CURRENT_WEEK" | grep -oP 'W\d+' | tr -d 'W')
PREV_WEEK_NUM=$((WEEK_NUM - 1))
YEAR=$(echo "$CURRENT_WEEK" | grep -oP '^\d{4}')
PREV_WEEK="${YEAR}-W${PREV_WEEK_NUM}"
WEEK_SLUG=$(echo "$CURRENT_WEEK" | tr '[:upper:]' '[:lower:]')
JSON_PATH="$SCRIPT_DIR/dashboard-ingester/data/${WEEK_SLUG}.json"

echo "Current week: $CURRENT_WEEK"
echo "Previous week: $PREV_WEEK"
echo "JSON path: $JSON_PATH"
echo ""

# ── Step 2: Sync to MotherDuck ──
echo "Step 2: Syncing data to MotherDuck..."
python3 -c "
import sys; sys.path.insert(0, '.')
exec(open('$PROJECTOR').read())
sync_to_motherduck('$JSON_PATH')
"
echo ""

# ── Step 3: Score last week's predictions ──
echo "Step 3: Scoring $PREV_WEEK predictions..."
python3 -c "
import sys; sys.path.insert(0, '.')
exec(open('$PROJECTOR').read())
score_predictions('$PREV_WEEK')
"
echo ""

# ── Step 4: Generate projections ──
echo "Step 4: Generating projections from $CURRENT_WEEK..."
python3 -c "
import sys; sys.path.insert(0, '.')
exec(open('$PROJECTOR').read())
run('$CURRENT_WEEK')
"
echo ""

echo "═══════════════════════════════════════════"
echo "  Pipeline complete."
echo ""
echo "  Outputs:"
echo "    Callout drafts: ~/shared/context/active/callouts/"
echo "    Data briefs:    ~/shared/context/active/callouts/<market>/"
echo "    Projections:    ~/shared/context/active/callouts/projections-${WEEK_SLUG#*-}.md"
echo "    WW Summary:     ~/shared/context/active/callouts/ww-summary-*"
echo "    JSON extract:   $JSON_PATH"
echo ""
echo "  Next: Trigger the WBR callout skill for writing + blind review."
echo "═══════════════════════════════════════════"
