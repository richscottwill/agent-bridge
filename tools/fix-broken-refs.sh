#!/bin/bash
# Fix broken path references after wiki migration
# Only touches active system files (body, protocols, agents, hooks, skills, steering, tools, wiki/_meta)
# Skips session-log.md and intake/ (historical references are fine)

SHARED="/home/prichwil/shared"
FIXED=0

fix_refs() {
  local file="$1"
  local changed=false
  
  # Skip session-log and intake docs (historical)
  case "$file" in
    */session-log.md|*/intake/*.md|*/experiments/*.md|*/specs/*) return ;;
  esac

  # shared/wiki/ -> shared/wiki/ (with subdir mapping)
  if /bin/grep -q 'shared/wiki/strategy/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/strategy/|shared/wiki/strategy/|g' "$file"; changed=true
  fi
  if /bin/grep -q 'shared/wiki/testing/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/testing/|shared/wiki/testing/|g' "$file"; changed=true
  fi
  if /bin/grep -q 'shared/wiki/markets/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/markets/|shared/wiki/markets/|g' "$file"; changed=true
  fi
  if /bin/grep -q 'shared/wiki/operations/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/operations/|shared/wiki/operations/|g' "$file"; changed=true
  fi
  if /bin/grep -q 'shared/wiki/operations/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/operations/|shared/wiki/operations/|g' "$file"; changed=true
  fi
  if /bin/grep -q 'shared/wiki/reporting/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/reporting/|shared/wiki/reporting/|g' "$file"; changed=true
  fi
  if /bin/grep -q 'shared/wiki/operations/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/operations/|shared/wiki/operations/|g' "$file"; changed=true
  fi
  if /bin/grep -q 'shared/wiki/strategy/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/strategy/|shared/wiki/strategy/|g' "$file"; changed=true
  fi
  # Generic shared/wiki/ (catch remaining)
  if /bin/grep -q 'shared/wiki/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/|shared/wiki/|g' "$file"; changed=true
  fi

  # shared/wiki/ -> shared/wiki/ (by topic)
  if /bin/grep -q 'shared/wiki/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/|shared/wiki/|g' "$file"; changed=true
  fi
  # shared/wiki/reviews/ -> shared/wiki/reviews/
  if /bin/grep -q 'shared/wiki/reviews/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/reviews/|shared/wiki/reviews/|g' "$file"; changed=true
  fi
  # shared/wiki/archive/ -> shared/wiki/archive/
  if /bin/grep -q 'shared/wiki/archive/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/archive/|shared/wiki/archive/|g' "$file"; changed=true
  fi
  # shared/wiki/research/ -> shared/wiki/research/
  if /bin/grep -q 'shared/wiki/research/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/research/|shared/wiki/research/|g' "$file"; changed=true
  fi
  # Generic shared/wiki/ -> shared/wiki/
  if /bin/grep -q 'shared/wiki/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/|shared/wiki/|g' "$file"; changed=true
  fi

  # shared/wiki/meetings/ -> shared/wiki/meetings/
  if /bin/grep -q 'shared/wiki/meetings/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/meetings/|shared/wiki/meetings/|g' "$file"; changed=true
  fi

  # shared/wiki/callouts/ -> shared/wiki/callouts/
  if /bin/grep -q 'shared/wiki/callouts/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/callouts/|shared/wiki/callouts/|g' "$file"; changed=true
  fi

  # shared/wiki/research/ -> shared/wiki/research/
  if /bin/grep -q 'shared/wiki/research/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/research/|shared/wiki/research/|g' "$file"; changed=true
  fi

  # shared/context/ -> (removed, note in steering)
  # Only fix references that point to specific files
  if /bin/grep -q 'shared/context/body/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/context/body/|shared/context/body/|g' "$file"; changed=true
  fi
  if /bin/grep -q 'shared/.kiro/agents/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/.kiro/agents/|shared/.kiro/agents/|g' "$file"; changed=true
  fi
  if /bin/grep -q 'shared/context/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/context/|shared/context/|g' "$file"; changed=true
  fi

  # ~/shared/context/ -> shared/context/body/ (root-level refs)
  if /bin/grep -q '~/shared/context/' "$file" 2>/dev/null; then
    /bin/sed -i 's|~/shared/context/body/|~/shared/context/body/|g' "$file"
    /bin/sed -i 's|~/shared/context/|~/shared/context/|g' "$file"; changed=true
  fi

  # context/tools/ -> tools/ (but careful not to break context/tools references that mean something else)
  if /bin/grep -q 'shared/tools/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/tools/|shared/tools/|g' "$file"; changed=true
  fi

  # wiki/archive/ -> wiki/archive/
  if /bin/grep -q 'shared/wiki/archive/' "$file" 2>/dev/null; then
    /bin/sed -i 's|shared/wiki/archive/|shared/wiki/archive/|g' "$file"; changed=true
  fi
  if /bin/grep -q 'wiki/archive/' "$file" 2>/dev/null; then
    /bin/sed -i 's|wiki/archive/|wiki/archive/|g' "$file"; changed=true
  fi

  # context/body/changelog.md -> context/body/changelog.md
  if /bin/grep -q 'context/body/changelog.md' "$file" 2>/dev/null; then
    /bin/sed -i 's|context/body/changelog.md|context/body/changelog.md|g' "$file"; changed=true
  fi

  if [ "$changed" = true ]; then
    FIXED=$((FIXED + 1))
    echo "FIXED: $(echo $file | /bin/sed "s|$SHARED/||")"
  fi
}

echo "=== Fixing broken references ==="

# Process all active system files
/usr/bin/find "$SHARED/context/body" "$SHARED/context/active" "$SHARED/context/protocols" -name "*.md" -type f 2>/dev/null | while read f; do fix_refs "$f"; done
/usr/bin/find "$SHARED/.kiro/agents" "$SHARED/.kiro/hooks" "$SHARED/.kiro/skills" "$SHARED/.kiro/steering" -name "*.md" -o -name "*.json" -o -name "*.hook" -o -name "*.sh" 2>/dev/null | while read f; do fix_refs "$f"; done
/usr/bin/find "$SHARED/tools" -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.json" -o -name "*.yaml" 2>/dev/null | while read f; do fix_refs "$f"; done
/usr/bin/find "$SHARED/wiki/_meta" -name "*.md" -type f 2>/dev/null | while read f; do fix_refs "$f"; done

echo ""
echo "Done. Fixed $FIXED files."
