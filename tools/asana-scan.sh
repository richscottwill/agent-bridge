#!/bin/bash
# Asana Activity Scanner - Get stories for tasks and filter for teammate activity
# Cutoff: 2026-04-09T00:00:00Z (7 days before April 16, 2026)
# Richard's GID: 1212732742544167

CUTOFF="2026-04-09T00:00:00Z"
RICHARD_GID="1212732742544167"
MCP_BIN="$HOME/.toolbox/bin/enterprise-asana-mcp"
OUTPUT_DIR="$HOME/shared/tools/asana-scan-output"
mkdir -p "$OUTPUT_DIR"

SIGNALS_FILE="$OUTPUT_DIR/signals.jsonl"
ERRORS_FILE="$OUTPUT_DIR/errors.txt"
> "$SIGNALS_FILE"
> "$ERRORS_FILE"

SCANNED=0
SIGNAL_COUNT=0
ERROR_COUNT=0

# Read task GIDs from file
while IFS='|' read -r TASK_GID TASK_NAME; do
    SCANNED=$((SCANNED + 1))
    
    # Call GetTaskStories
    RESULT=$(echo "{\"jsonrpc\":\"2.0\",\"id\":$SCANNED,\"method\":\"tools/call\",\"params\":{\"name\":\"asana___GetTaskStories\",\"arguments\":{\"task_gid\":\"$TASK_GID\"}}}" | timeout 15 "$MCP_BIN" 2>/dev/null)
    
    if [ $? -ne 0 ] || [ -z "$RESULT" ]; then
        echo "$TASK_GID|$TASK_NAME|API timeout or error" >> "$ERRORS_FILE"
        ERROR_COUNT=$((ERROR_COUNT + 1))
        continue
    fi
    
    if echo "$RESULT" | grep -q '"isError":true'; then
        echo "$TASK_GID|$TASK_NAME|API returned error" >> "$ERRORS_FILE"
        ERROR_COUNT=$((ERROR_COUNT + 1))
        continue
    fi
    
    # Save raw for python processing
    echo "$RESULT" > "$OUTPUT_DIR/raw_${TASK_GID}.json"
    
    # Process with python
    python3 "$HOME/shared/tools/process-stories.py" "$TASK_GID" "$TASK_NAME" "$OUTPUT_DIR/raw_${TASK_GID}.json" "$CUTOFF" "$RICHARD_GID" >> "$SIGNALS_FILE" 2>> "$ERRORS_FILE"
    
done < "$HOME/shared/tools/task-list.txt"

SIGNAL_COUNT=$(wc -l < "$SIGNALS_FILE" | tr -d ' ')
echo "Tasks scanned: $SCANNED"
echo "Signals detected: $SIGNAL_COUNT"
echo "Errors: $ERROR_COUNT"
