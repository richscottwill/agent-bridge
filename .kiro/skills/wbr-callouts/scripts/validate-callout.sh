#!/bin/bash
# validate-callout.sh — Check word count of callout files (max 150 words per callout)
# Usage: validate-callout.sh <callout-file-or-directory>

set -euo pipefail

MAX_WORDS=150
EXIT_CODE=0

validate_file() {
    local file="$1"
    local word_count
    word_count=$(wc -w < "$file")
    
    if [ "$word_count" -gt "$MAX_WORDS" ]; then
        echo "FAIL: $file — $word_count words (max $MAX_WORDS)"
        EXIT_CODE=1
    else
        echo "PASS: $file — $word_count words"
    fi
}

if [ $# -eq 0 ]; then
    echo "Usage: validate-callout.sh <file-or-directory>"
    exit 1
fi

TARGET="$1"

if [ -d "$TARGET" ]; then
    for f in "$TARGET"/*.md; do
        [ -f "$f" ] && validate_file "$f"
    done
elif [ -f "$TARGET" ]; then
    validate_file "$TARGET"
else
    echo "ERROR: $TARGET not found"
    exit 1
fi

exit $EXIT_CODE
