#!/bin/bash
# WBR Dashboard Watcher — polls OneDrive every 30 mins for new dashboard xlsx.
# When found: checks context freshness, ingests change log, ingests dashboard,
# runs projection accuracy check, runs callout pipeline, Slacks Richard.
# Usage: bash ~/shared/tools/wbr-auto-pipeline/wbr-watcher.sh
# Stop: kill the process or Ctrl+C

POLL_INTERVAL=1800  # 30 minutes in seconds
CONFIG="$HOME/shared/tools/wbr-auto-pipeline/config.json"
LOG="$HOME/shared/tools/wbr-auto-pipeline/watcher.log"
KIRO_CLI="/agentspaces/kiro-cli/kiro-cli"
CHANGE_LOG_SHEET="1YUpRrtiBSpbWkwz_8hYcushXnXBt1WuoNR36UnGqAkU"

echo "$(date -Iseconds) WBR watcher started. Polling every ${POLL_INTERVAL}s (Mondays only, 6am-6pm PT)." | tee -a "$LOG"

while true; do
  # Only poll on Mondays between 6am-6pm PT (UTC-7 = 13:00-01:00 UTC)
  DAY_OF_WEEK=$(date -u +%u)  # 1=Monday
  HOUR_UTC=$(date -u +%H)
  
  IS_MONDAY_WINDOW=false
  if [ "$DAY_OF_WEEK" = "1" ] && [ "$HOUR_UTC" -ge 13 ]; then
    IS_MONDAY_WINDOW=true
  elif [ "$DAY_OF_WEEK" = "2" ] && [ "$HOUR_UTC" -lt 1 ]; then
    IS_MONDAY_WINDOW=true
  fi

  if [ "$IS_MONDAY_WINDOW" = "false" ]; then
    sleep 3600
    continue
  fi

  echo "$(date -Iseconds) Polling for new dashboard..." | tee -a "$LOG"

  LAST_PROCESSED=$(python3 -c "
import json, os
cfg = '$CONFIG'
if os.path.exists(cfg):
    with open(cfg) as f:
        c = json.load(f)
    print(c.get('last_processed_file', ''))
else:
    print('')
" 2>/dev/null)

  # Full pipeline in one kiro-cli call
  $KIRO_CLI chat --no-interactive --trust-all-tools \
    "WBR auto-pipeline. Execute these steps in order. Stop on critical failure, continue on non-critical.

=== STEP 1: CHECK FOR NEW DASHBOARD ===
Use sharepoint_search with query '\"AB SEM WW Dashboard\" FileType:xlsx' rowLimit 3.
Find the file with the highest week number (W14 > W13 etc). Note its Name and Path.
Last processed: '${LAST_PROCESSED:-none}'.
If the latest file name matches last processed, say 'NO_NEW_FILE' and STOP — no further steps.

=== STEP 2: MARKET CONTEXT FRESHNESS CHECK ===
Check modification dates of all 10 market context files:
  ~/shared/context/active/callouts/{au,mx,us,ca,jp,uk,de,fr,it,es}/*-context.md
For each, check if last modified > 14 days ago. Flag stale ones.
This is non-critical — log stale markets but continue.

=== STEP 3: CHANGE LOG INGESTION ===
Download the change log from Google Sheets (ID: $CHANGE_LOG_SHEET).
The sheet has 4 tabs. Export each as CSV using these URLs:
  Tab 1 (MX/AU): https://docs.google.com/spreadsheets/d/$CHANGE_LOG_SHEET/export?format=csv&gid=1407602397
  Tab 2 (EU5): https://docs.google.com/spreadsheets/d/$CHANGE_LOG_SHEET/export?format=csv&gid=238419350
  Tab 3 (NA/JP): https://docs.google.com/spreadsheets/d/$CHANGE_LOG_SHEET/export?format=csv&gid=1176759484
  Tab 4 (Partnership): https://docs.google.com/spreadsheets/d/$CHANGE_LOG_SHEET/export?format=csv&gid=1994107761
Save each CSV to ~/shared/tools/dashboard-ingester/input/change-log-{mx_au,eu5,na_jp,partnership}.csv
Ingest all to DuckDB change_log table via:
  python3 -c \"import duckdb; con=duckdb.connect('/home/prichwil/shared/data/duckdb/ps-analytics.duckdb'); con.execute(\\\"INSERT INTO change_log SELECT * FROM read_csv_auto('[csv_path]')\\\"); con.close()\"
Non-critical — if this fails, log and continue.

=== STEP 4: PROJECTION ACCURACY CHECK ===
For each market with a projections file (~/shared/context/active/callouts/*/[market]-projections.md):
  Read last week's projected regs and spend.
  Compare against this week's actuals from the new dashboard data briefs.
  Compute accuracy: actual/projected for regs and spend.
  Append one line to each projections file: 'W[N-1] accuracy: regs [X]% of projected, spend [X]% of projected.'
Non-critical — if projections files don't have last week's numbers, skip.

=== STEP 5: DOWNLOAD NEW DASHBOARD ===
Use sharepoint_read_file with the serverRelativeUrl from Step 1.
Save to: ~/shared/tools/dashboard-ingester/input/[filename]
Confirm file exists on disk. CRITICAL — stop if download fails.

=== STEP 6: INGEST DASHBOARD ===
Run: python3 ~/shared/tools/dashboard-ingester/ingest.py ~/shared/tools/dashboard-ingester/input/[filename]
CRITICAL — stop if ingestion fails.

=== STEP 7: UPDATE CONFIG ===
python3 -c \"import json; c=json.load(open('$CONFIG')); c['last_processed_file']='[filename]'; c['last_processed_date']='$(date -Iseconds)'; json.dump(c,open('$CONFIG','w'),indent=2)\"

=== STEP 8: RUN CALLOUT PIPELINE ===
Run the WBR callout pipeline: $KIRO_CLI chat --agent karpathy --no-interactive --trust-all-tools 'Run the wbr-callouts skill for all 10 markets. Dashboard already ingested. Follow callout-principles.md.'

=== STEP 9: SLACK NOTIFICATION ===
After callouts complete, DM Richard on Slack with a summary. Use self_dm with login 'prichwil':
  '📊 W[NN] WBR Callouts Ready
  Dashboard: [filename] ingested
  Markets: 10 callouts drafted
  Stale context: [list or none]
  Projection accuracy: [summary or first run]
  Change log: [ingested/failed/skipped]
  Review: ~/shared/context/active/callouts/[market]/[market]-2026-w[NN].md'

Report final status: PIPELINE_COMPLETE, NO_NEW_FILE, or ERROR:[step]:[reason]" \
    2>&1 | tail -10 | tee -a "$LOG"

  echo "$(date -Iseconds) Poll complete. Next check in ${POLL_INTERVAL}s." | tee -a "$LOG"
  sleep $POLL_INTERVAL
done