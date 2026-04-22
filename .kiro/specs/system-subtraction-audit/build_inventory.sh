#!/bin/bash
# Phase 1 inventory builder — produces inventory.json
# Single-use script; deleted in Phase 7 cleanup.

set -u
OUT="/home/prichwil/.kiro/specs/system-subtraction-audit/inventory.json"

emit_file_entry() {
  local abspath="$1"
  local layer="$2"
  # rel_path — substitute home with ~
  local rel="${abspath/#\/home\/prichwil\//~/}"
  rel="${rel/#~/~}"  # idempotent
  local lines=$(wc -l < "$abspath" 2>/dev/null || echo 0)
  local mtime=$(TZ=America/Los_Angeles stat -c %y "$abspath" 2>/dev/null | sed 's/ /T/;s/\.[0-9]* //;s/ //' | head -c 25)
  local size=$(stat -c %s "$abspath" 2>/dev/null || echo 0)

  # Frontmatter detection (steering)
  local has_fm=false
  local inc_raw="null"
  local inc_mode="null"
  if [[ "$layer" == "steering" ]] && head -1 "$abspath" 2>/dev/null | grep -q "^---$"; then
    has_fm=true
    inc_raw=$(awk '/^---$/{c++; next} c==1 && /^inclusion:/{print $2; exit}' "$abspath" 2>/dev/null | tr -d '"')
    case "$inc_raw" in
      always|auto) inc_mode="auto" ;;
      manual|fileMatch) inc_mode="conditional" ;;
      "") inc_raw="null" ;;
      *) inc_mode="null" ;;  # unknown — needs_revisit
    esac
  elif [[ "$layer" == "steering" ]]; then
    # No frontmatter → auto per R13.1
    inc_mode="auto"
    inc_raw="absent"
  fi

  # Hook enabled state
  local is_enabled="null"
  if [[ "$layer" == "hook" ]]; then
    is_enabled=$(python3 -c "import json,sys;d=json.load(open('$abspath'));print(str(d.get('enabled','null')).lower())" 2>/dev/null || echo "null")
  fi

  # First heading + first paragraph for purpose
  local first_heading=""
  local purpose_line=""
  local purpose_missing="false"

  if [[ "$layer" == "hook" ]]; then
    # JSON — extract description or name
    purpose_line=$(python3 -c "import json;d=json.load(open('$abspath'));print(d.get('description') or d.get('name') or '')" 2>/dev/null)
    first_heading=$(python3 -c "import json;d=json.load(open('$abspath'));print(d.get('name',''))" 2>/dev/null)
  elif [[ "$layer" == "steering" ]] && $has_fm; then
    # Try frontmatter description first
    purpose_line=$(awk '/^---$/{c++; next} c==1 && /^description:/{sub(/^description:[ ]*/,""); gsub(/^"|"$/,""); print; exit}' "$abspath" 2>/dev/null)
    first_heading=$(grep -m1 '^# ' "$abspath" 2>/dev/null | sed 's/^# //' | head -c 200)
    [[ -z "$purpose_line" ]] && purpose_line="$first_heading"
  else
    # body, protocol, or frontmatter-less steering: first H1 + first non-heading paragraph
    first_heading=$(grep -m1 '^# ' "$abspath" 2>/dev/null | sed 's/^# //' | head -c 200)
    purpose_line=$(awk 'BEGIN{hf=0; fc=0} /^---$/{fc++; next} fc==1{next} /^# /{hf=1; next} hf==1 && NF>0 && !/^```/{print; exit}' "$abspath" 2>/dev/null | head -c 400)
    [[ -z "$purpose_line" ]] && purpose_line="$first_heading"
  fi

  # Purpose missing / placeholder check
  if [[ -z "$purpose_line" ]] || echo "$first_heading" | grep -qiE '^(TODO|Placeholder|FIXME)'; then
    purpose_missing="true"
  fi

  # Empty shell check (< 10 non-frontmatter non-blank lines)
  local content_lines
  if $has_fm; then
    content_lines=$(awk 'BEGIN{c=0;skip=1} /^---$/{c++;next} c>=2 && NF>0 && !/^[[:space:]]*$/{n++} END{print n+0}' "$abspath")
  else
    content_lines=$(grep -c '[^[:space:]]' "$abspath" 2>/dev/null || echo 0)
  fi
  local empty_shell="false"
  [[ "$content_lines" -lt 10 ]] && empty_shell="true"

  # Escape strings for JSON
  esc() { python3 -c "import json,sys;print(json.dumps(sys.stdin.read().rstrip()))" <<<"$1"; }

  cat <<EOF
    {
      "path": "$abspath",
      "rel_path": "$rel",
      "layer": "$layer",
      "lines": $lines,
      "content_lines": $content_lines,
      "size_bytes": $size,
      "last_modified": "$mtime",
      "first_heading": $(esc "$first_heading"),
      "purpose_line": $(esc "$purpose_line"),
      "purpose_missing": $purpose_missing,
      "empty_shell": $empty_shell,
      "inclusion_mode": $(if [[ "$inc_mode" == "null" ]]; then echo "null"; else echo "\"$inc_mode\""; fi),
      "inclusion_mode_raw": $(if [[ "$inc_raw" == "null" ]]; then echo "null"; else echo "\"$inc_raw\""; fi),
      "is_enabled": $is_enabled,
      "needs_revisit": $(if [[ "$layer" == "steering" && "$inc_mode" == "null" && "$inc_raw" != "null" && "$inc_raw" != "absent" ]]; then echo "true"; else echo "false"; fi)
    }
EOF
}

# Collect all files
declare -a ENTRIES
FIRST=true
echo '{' > "$OUT"
echo '  "generated_at": "2026-04-21T23:45:13-07:00",' >> "$OUT"
echo '  "pass_mode": "FULL",' >> "$OUT"
echo '  "files": [' >> "$OUT"

FIRST=true
# Body
for f in /home/prichwil/shared/context/body/*.md; do
  [[ ! -f "$f" ]] && continue
  $FIRST || echo "    ," >> "$OUT"
  emit_file_entry "$f" "body" >> "$OUT"
  FIRST=false
done
# Protocols (.md only — .docx excluded)
for f in /home/prichwil/shared/context/protocols/*.md; do
  [[ ! -f "$f" ]] && continue
  $FIRST || echo "    ," >> "$OUT"
  emit_file_entry "$f" "protocol" >> "$OUT"
  FIRST=false
done
# Hooks
for f in /home/prichwil/.kiro/hooks/*.hook; do
  [[ ! -f "$f" ]] && continue
  $FIRST || echo "    ," >> "$OUT"
  emit_file_entry "$f" "hook" >> "$OUT"
  FIRST=false
done
# Steering (top-level .md)
for f in /home/prichwil/.kiro/steering/*.md; do
  [[ ! -f "$f" ]] && continue
  $FIRST || echo "    ," >> "$OUT"
  emit_file_entry "$f" "steering" >> "$OUT"
  FIRST=false
done
# Steering nested
for f in /home/prichwil/.kiro/steering/context/*.md; do
  [[ ! -f "$f" ]] && continue
  $FIRST || echo "    ," >> "$OUT"
  emit_file_entry "$f" "steering" >> "$OUT"
  FIRST=false
done

echo '  ]' >> "$OUT"
echo '}' >> "$OUT"

echo "inventory.json written"
