#!/usr/bin/env bash
# deploy-forecast-harmony.sh
# Refreshes forecast-data.json from the latest ps-forecast-tracker.xlsx and
# redeploys the paid-acq-forecast Harmony app to beta.
#
# Called by: shared/.kiro/hooks/harmony-forecast-deploy.kiro.hook
#            (fires on fileEdited shared/dashboards/ps-forecast-tracker.xlsx)
#
# Single responsibility: xlsx-is-fresh → JSON-is-fresh → Harmony-is-fresh.
# Does NOT push to SharePoint — that's forecast-sharepoint-push.hook's job.
#
# Safe to run manually: idempotent, logs to stderr, exits non-zero on failure.

set -euo pipefail

# ── Paths ────────────────────────────────────────────────────────────────
DASHBOARD_DIR="$HOME/shared/dashboards"
XLSX="$DASHBOARD_DIR/ps-forecast-tracker.xlsx"
JSON_SRC="$DASHBOARD_DIR/data/forecast-data.json"
HARMONY_APP_DIR="$HOME/.workspace/forecast-harmony/Harmony-paid-acq-forecast/src/Harmony-paid-acq-forecast"
JSON_DEST="$HARMONY_APP_DIR/src/data/forecast-data.json"
LOG="$HOME/shared/context/active/harmony-forecast-deploy.log"

# ── Logging helper ───────────────────────────────────────────────────────
log() {
  local msg="[$(TZ=America/Los_Angeles date +'%Y-%m-%d %H:%M:%S %Z')] $*"
  echo "$msg" | tee -a "$LOG" >&2
}

log "=== harmony-forecast-deploy start ==="

# ── Preflight ────────────────────────────────────────────────────────────
if [[ ! -f "$XLSX" ]]; then
  log "ERROR: xlsx not found at $XLSX"
  exit 1
fi
if [[ ! -d "$HARMONY_APP_DIR" ]]; then
  log "ERROR: Harmony app dir not found at $HARMONY_APP_DIR"
  exit 1
fi
if ! command -v harmony >/dev/null 2>&1; then
  log "ERROR: harmony CLI not on PATH — ensure toolbox is loaded"
  exit 1
fi

# ── Step 1: Rebuild JSON from xlsx ───────────────────────────────────────
log "Step 1/3: refresh-forecast.py (xlsx → JSON)"
if ! python3 "$DASHBOARD_DIR/refresh-forecast.py" >>"$LOG" 2>&1; then
  log "ERROR: refresh-forecast.py failed — see $LOG"
  exit 1
fi
log "  JSON refreshed: $(stat -c '%y' "$JSON_SRC" | cut -d'.' -f1)"

# ── Step 2: Copy JSON into Harmony app ───────────────────────────────────
log "Step 2/3: copy JSON into Harmony app"
mkdir -p "$(dirname "$JSON_DEST")"
cp "$JSON_SRC" "$JSON_DEST"
log "  Copied: $JSON_DEST ($(stat -c '%s' "$JSON_DEST") bytes)"

# ── Step 3: Deploy to Harmony beta ───────────────────────────────────────
log "Step 3/3: harmony app deploy --stage beta"
# --accept-breaking-changes: auto-accept warnings on subsequent deploys
# printf feeds Y to any lingering interactive prompts (Ground Rules reacceptance, etc.)
if ! ( cd "$HARMONY_APP_DIR" && printf 'Y\nY\nY\n' | harmony app deploy --stage beta --accept-breaking-changes >>"$LOG" 2>&1 ); then
  log "ERROR: harmony app deploy failed — see $LOG"
  exit 1
fi

log "=== harmony-forecast-deploy done: https://paid-acq-forecast.beta.harmony.a2z.com ==="
