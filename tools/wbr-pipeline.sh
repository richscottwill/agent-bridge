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
#   5. Populate ps.forecast_tracker in MotherDuck (weekly/monthly/quarterly/year-end)
#   6. Update ps-forecast-tracker.xlsx (template-based, _Data sheet only)
#   7. Push xlsx to SharePoint (Kiro-Drive + Dashboards)
#   8. Output: callout drafts, data briefs, projection tables, WW summary
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

# ── Step 2b: Detect regime changes from change_log ──
echo "Step 2b: Scanning for regime changes..."
python3 "$SCRIPT_DIR/prediction/detect_regime_changes.py"
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

# ── Step 5: Populate forecast tracker in MotherDuck ──
echo "Step 5: Populating ps.forecast_tracker in MotherDuck..."
python3 "$SCRIPT_DIR/prediction/populate_forecast_tracker.py"
echo ""

# ── Step 6: Update forecast tracker xlsx (template-based, preserves formatting) ──
echo "Step 6: Updating ps-forecast-tracker.xlsx..."
python3 "$SCRIPT_DIR/../dashboards/update-forecast-tracker.py"
XLSX_OUT="$HOME/shared/dashboards/ps-forecast-tracker.xlsx"
echo ""

# ── Step 7: Push xlsx to SharePoint (Kiro-Drive + Dashboards) ──
echo "Step 7: Pushing forecast tracker to SharePoint..."
python3 -c "
import subprocess, sys
xlsx = '$XLSX_OUT'
# Push to both SharePoint locations
# Uses the SharePoint MCP via a simple Python wrapper
print('  Uploading to Kiro-Drive/...')
print('  Uploading to Dashboards/...')
print('  (SharePoint push requires MCP — flagging for agent to complete)')
" 2>&1 || true
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
echo "    Forecast DB:    ps.forecast_tracker (MotherDuck)"
echo "    Forecast xlsx:  ~/shared/dashboards/ps-forecast-tracker.xlsx"
echo "    SharePoint:     Kiro-Drive/ + Dashboards/ (push pending MCP)"
echo ""
echo "  Next: Trigger the WBR callout skill for writing + blind review."
echo "  Note: SharePoint push requires MCP tools — run agent push after pipeline."
echo ""
echo "  # TODO (deferred 2026-04-13): Add step 8 — regenerate market-constraints.md"
echo "  # from ps.regime_changes + ps.market_status + ps.forecast_tracker."
echo "  # Target: enable after 4/20. See session-log.md open items."
echo "═══════════════════════════════════════════"
