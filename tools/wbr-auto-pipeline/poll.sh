#!/bin/bash
# WBR Auto-Pipeline: Polls OneDrive for new dashboard xlsx, downloads, ingests, runs callouts.
# Usage: bash ~/shared/tools/wbr-auto-pipeline/poll.sh
# Designed to run Monday mornings or on-demand.

set -euo pipefail

CONFIG="$HOME/shared/tools/wbr-auto-pipeline/config.json"
LOG="$HOME/shared/tools/wbr-auto-pipeline/poll.log"
DOWNLOAD_DIR="$HOME/shared/tools/dashboard-ingester/input"
INGESTER="$HOME/shared/tools/dashboard-ingester/ingest.py"
KIRO_CLI="/agentspaces/kiro-cli/kiro-cli"

mkdir -p "$DOWNLOAD_DIR"

echo "$(date -Iseconds) WBR auto-pipeline: checking for new dashboard..." | tee -a "$LOG"

# Step 1: Search OneDrive for latest dashboard file
# We use kiro-cli to call the SharePoint MCP since we can't call it directly from bash
LATEST_FILE=$($KIRO_CLI chat --agent karpathy --no-interactive --trust-all-tools \
  "Search SharePoint for the latest AB SEM WW Dashboard xlsx file. Run this exact command:
   Use the sharepoint_search MCP tool with query '\"AB SEM WW Dashboard\" FileType:xlsx'.
   From the results, find the file with the highest week number (W14 > W13 > W12).
   Output ONLY one line in this exact format: FILENAME|PATH|MODIFIED_DATE
   Example: AB SEM WW Dashboard_Y26 W13.xlsx|/personal/prichwil_amazon_com/Documents/Downloads/AB SEM WW Dashboard_Y26 W13.xlsx|2026-04-03T17:51:42Z
   No other output." 2>/dev/null | grep "^AB SEM" | head -1)

if [ -z "$LATEST_FILE" ]; then
  echo "$(date -Iseconds) No dashboard file found or parse error." | tee -a "$LOG"
  exit 1
fi

FILENAME=$(echo "$LATEST_FILE" | cut -d'|' -f1)
FILEPATH=$(echo "$LATEST_FILE" | cut -d'|' -f2)
MODIFIED=$(echo "$LATEST_FILE" | cut -d'|' -f3)

echo "$(date -Iseconds) Latest: $FILENAME (modified: $MODIFIED)" | tee -a "$LOG"

# Step 2: Check if already processed
LAST_PROCESSED=$(python3 -c "
import json
with open('$CONFIG') as f:
    c = json.load(f)
print(c.get('last_processed_file', '') or '')
" 2>/dev/null)

if [ "$FILENAME" = "$LAST_PROCESSED" ]; then
  echo "$(date -Iseconds) Already processed $FILENAME. Skipping." | tee -a "$LOG"
  exit 0
fi

echo "$(date -Iseconds) New file detected: $FILENAME (last processed: ${LAST_PROCESSED:-none})" | tee -a "$LOG"

# Step 3: Download via SharePoint MCP
echo "$(date -Iseconds) Downloading $FILENAME..." | tee -a "$LOG"
$KIRO_CLI chat --agent karpathy --no-interactive --trust-all-tools \
  "Download this file from SharePoint to local disk. Use the sharepoint_read_file MCP tool with:
   serverRelativeUrl: '$FILEPATH'
   savePath: '$DOWNLOAD_DIR/$FILENAME'
   Output ONLY: DOWNLOADED or FAILED" 2>/dev/null | tee -a "$LOG"

if [ ! -f "$DOWNLOAD_DIR/$FILENAME" ]; then
  echo "$(date -Iseconds) Download failed — file not found at $DOWNLOAD_DIR/$FILENAME" | tee -a "$LOG"
  exit 1
fi

echo "$(date -Iseconds) Downloaded: $DOWNLOAD_DIR/$FILENAME ($(wc -c < "$DOWNLOAD_DIR/$FILENAME") bytes)" | tee -a "$LOG"

# Step 4: Run ingester
echo "$(date -Iseconds) Running dashboard ingester..." | tee -a "$LOG"
python3 "$INGESTER" "$DOWNLOAD_DIR/$FILENAME" 2>&1 | tee -a "$LOG"

# Step 5: Update config
python3 -c "
import json
with open('$CONFIG', 'r') as f:
    c = json.load(f)
c['last_processed_file'] = '$FILENAME'
c['last_processed_date'] = '$(date -Iseconds)'
with open('$CONFIG', 'w') as f:
    json.dump(c, f, indent=2)
print('Config updated.')
" 2>&1 | tee -a "$LOG"

# Step 6: Run callout pipeline
echo "$(date -Iseconds) Launching WBR callout pipeline..." | tee -a "$LOG"
$KIRO_CLI chat --agent karpathy --no-interactive --trust-all-tools \
  "The dashboard has been ingested. Run the WBR callout pipeline now. Invoke the wbr-callouts skill: analyze all 10 markets, write callouts, run blind review. Follow callout-principles.md." 2>&1 | tee -a "$LOG"

echo "$(date -Iseconds) WBR auto-pipeline complete." | tee -a "$LOG"