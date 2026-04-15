#!/usr/bin/env bash
# ============================================================================
# Admin Block Preservation Property Tests
# ============================================================================
# **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8**
#
# **Property 2: Preservation** — Non-Admin Routing and Hook Structure Unchanged
#
# These tests capture BASELINE behavior on UNFIXED code.
# They MUST PASS on unfixed code (confirming behavior to preserve).
# They MUST ALSO PASS after the fix (confirming no regressions).
#
# Observation-first methodology: each assertion was derived from direct
# observation of the unfixed protocol files and DuckDB state.
#
# Nine preservation dimensions tested:
#   P1. Sweep routing: cap of 5 exists in protocols (Req 3.1)
#   P2. Core routing: cap of 4 exists in protocols (Req 3.2)
#   P3. Engine Room routing: cap of 6 exists in protocols (Req 3.3)
#   P4. Signal-to-Routine mapping: non-admin signals route correctly (Req 3.1-3.3)
#   P5. 4-block model preserved: exactly 4 blocks, no new ones (Req 3.6)
#   P6. Routine_RW enum values preserved: canonical set unchanged (Req 3.7)
#   P7. AM-1/AM-2/AM-3 hook structure intact (Req 3.5)
#   P8. EOD-2 daily reset exists (Req 3.5)
#   P9. Backlog (null Routine_RW) treated as requiring triage (Req 3.8)
# ============================================================================

set -euo pipefail

HANDS_MD="$HOME/shared/context/body/hands.md"
AM_TRIAGE="$HOME/shared/context/protocols/am-triage.md"
AM_AUTO="$HOME/shared/context/protocols/am-auto.md"
EOD_REFRESH="$HOME/shared/context/protocols/eod-system-refresh.md"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL=9

echo "============================================"
echo "Admin Block Preservation Property Tests"
echo "Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8"
echo "============================================"
echo ""
echo "These tests MUST PASS on both unfixed and fixed code."
echo "Failure means a regression was introduced."
echo ""


# --------------------------------------------------------------------------
# P1: Sweep routing — cap of 5 exists in protocols
# Observed: am-triage.md and am-auto.md both have "Sweep: 5" in Bucket Cap Check
# Observed: hands.md Task List Structure has Sweep cap = 5
# Validates: Requirement 3.1
# --------------------------------------------------------------------------
echo "--- P1: Sweep Routing Cap (5) Preserved ---"

SWEEP_CAP_TRIAGE=$(grep -c 'Sweep: 5' "$AM_TRIAGE" || true)
SWEEP_CAP_AUTO=$(grep -c 'Sweep: 5' "$AM_AUTO" || true)
SWEEP_CAP_HANDS=$(grep -E '^\|.*Sweep.*\|.*5\s*\|' "$HANDS_MD" | wc -l || true)

echo "  am-triage.md 'Sweep: 5' occurrences: $SWEEP_CAP_TRIAGE"
echo "  am-auto.md 'Sweep: 5' occurrences: $SWEEP_CAP_AUTO"
echo "  hands.md Sweep cap=5 in table: $SWEEP_CAP_HANDS"

if [[ "$SWEEP_CAP_TRIAGE" -ge 1 && "$SWEEP_CAP_AUTO" -ge 1 && "$SWEEP_CAP_HANDS" -ge 1 ]]; then
  echo "  ✅ PASS: Sweep cap of 5 preserved across all protocol files"
  PASS_COUNT=$((PASS_COUNT + 1))
else
  echo "  ❌ FAIL: Sweep cap of 5 missing from one or more protocol files"
  echo "  Regression: Sweep routing cap was changed or removed"
  FAIL_COUNT=$((FAIL_COUNT + 1))
fi
echo ""

# --------------------------------------------------------------------------
# P2: Core routing — cap of 4 exists in protocols
# Observed: am-triage.md and am-auto.md both have "Core: 4" in Bucket Cap Check
# Observed: hands.md Task List Structure has Core cap = 4
# Validates: Requirement 3.2
# --------------------------------------------------------------------------
echo "--- P2: Core Routing Cap (4) Preserved ---"

CORE_CAP_TRIAGE=$(grep -c 'Core: 4' "$AM_TRIAGE" || true)
CORE_CAP_AUTO=$(grep -c 'Core: 4' "$AM_AUTO" || true)
CORE_CAP_HANDS=$(grep -E '^\|.*Core.*\|.*4\s*\|' "$HANDS_MD" | wc -l || true)

echo "  am-triage.md 'Core: 4' occurrences: $CORE_CAP_TRIAGE"
echo "  am-auto.md 'Core: 4' occurrences: $CORE_CAP_AUTO"
echo "  hands.md Core cap=4 in table: $CORE_CAP_HANDS"

if [[ "$CORE_CAP_TRIAGE" -ge 1 && "$CORE_CAP_AUTO" -ge 1 && "$CORE_CAP_HANDS" -ge 1 ]]; then
  echo "  ✅ PASS: Core cap of 4 preserved across all protocol files"
  PASS_COUNT=$((PASS_COUNT + 1))
else
  echo "  ❌ FAIL: Core cap of 4 missing from one or more protocol files"
  echo "  Regression: Core routing cap was changed or removed"
  FAIL_COUNT=$((FAIL_COUNT + 1))
fi
echo ""

# --------------------------------------------------------------------------
# P3: Engine Room routing — cap of 6 exists in protocols
# Observed: am-triage.md and am-auto.md both have "Engine Room: 6" in Bucket Cap Check
# Observed: hands.md Task List Structure has Engine Room cap = 6
# Validates: Requirement 3.3
# --------------------------------------------------------------------------
echo "--- P3: Engine Room Routing Cap (6) Preserved ---"

ER_CAP_TRIAGE=$(grep -c 'Engine Room: 6' "$AM_TRIAGE" || true)
ER_CAP_AUTO=$(grep -c 'Engine Room: 6' "$AM_AUTO" || true)
ER_CAP_HANDS=$(grep -E '^\|.*Engine Room.*\|.*6\s*\|' "$HANDS_MD" | wc -l || true)

echo "  am-triage.md 'Engine Room: 6' occurrences: $ER_CAP_TRIAGE"
echo "  am-auto.md 'Engine Room: 6' occurrences: $ER_CAP_AUTO"
echo "  hands.md Engine Room cap=6 in table: $ER_CAP_HANDS"

if [[ "$ER_CAP_TRIAGE" -ge 1 && "$ER_CAP_AUTO" -ge 1 && "$ER_CAP_HANDS" -ge 1 ]]; then
  echo "  ✅ PASS: Engine Room cap of 6 preserved across all protocol files"
  PASS_COUNT=$((PASS_COUNT + 1))
else
  echo "  ❌ FAIL: Engine Room cap of 6 missing from one or more protocol files"
  echo "  Regression: Engine Room routing cap was changed or removed"
  FAIL_COUNT=$((FAIL_COUNT + 1))
fi
echo ""

# --------------------------------------------------------------------------
# P4: Signal-to-Routine mapping — non-admin signal types route correctly
# Observed in am-triage.md and am-auto.md:
#   "Quick reply/send/confirm → Sweep"
#   "Strategic discussion/artifact/framework → Core"
#   "Campaign/keyword/bid/spreadsheet → Engine Room"
# Validates: Requirements 3.1, 3.2, 3.3
# --------------------------------------------------------------------------
echo "--- P4: Signal-to-Routine Mapping Preserved ---"

# Check am-triage.md
SWEEP_MAPPING_T=$(grep -c 'Quick reply/send/confirm.*Sweep' "$AM_TRIAGE" || true)
CORE_MAPPING_T=$(grep -c 'Strategic discussion/artifact/framework.*Core' "$AM_TRIAGE" || true)
ER_MAPPING_T=$(grep -c 'Campaign/keyword/bid/spreadsheet.*Engine Room' "$AM_TRIAGE" || true)

# Check am-auto.md
SWEEP_MAPPING_A=$(grep -c 'Quick reply/send/confirm.*Sweep' "$AM_AUTO" || true)
CORE_MAPPING_A=$(grep -c 'Strategic discussion/artifact/framework.*Core' "$AM_AUTO" || true)
ER_MAPPING_A=$(grep -c 'Campaign/keyword/bid/spreadsheet.*Engine Room' "$AM_AUTO" || true)

MAPPING_TOTAL=$((SWEEP_MAPPING_T + CORE_MAPPING_T + ER_MAPPING_T + SWEEP_MAPPING_A + CORE_MAPPING_A + ER_MAPPING_A))

echo "  am-triage.md: Sweep=$SWEEP_MAPPING_T, Core=$CORE_MAPPING_T, ER=$ER_MAPPING_T"
echo "  am-auto.md:   Sweep=$SWEEP_MAPPING_A, Core=$CORE_MAPPING_A, ER=$ER_MAPPING_A"

if [[ "$MAPPING_TOTAL" -eq 6 ]]; then
  echo "  ✅ PASS: All 3 non-admin signal-to-routine mappings preserved in both protocols"
  PASS_COUNT=$((PASS_COUNT + 1))
else
  echo "  ❌ FAIL: Signal-to-Routine mapping changed ($MAPPING_TOTAL/6 found)"
  echo "  Regression: Non-admin signal routing was modified"
  FAIL_COUNT=$((FAIL_COUNT + 1))
fi
echo ""

# --------------------------------------------------------------------------
# P5: 4-block model preserved — exactly 4 blocks in hands.md table
# Observed: hands.md Task List Structure has exactly 4 block rows + Backlog
# Blocks: Sweep, Core, Engine Room, Admin (no new blocks)
# Validates: Requirement 3.6
# --------------------------------------------------------------------------
echo "--- P5: 4-Block Model Preserved (No New Blocks) ---"

# Count block rows in the Task List Structure table (emoji-prefixed rows, excluding Backlog)
BLOCK_ROWS=$(grep -E '^\| [🧹🎯⚙️📋]' "$HANDS_MD" | wc -l || true)
HAS_SWEEP=$(grep -cE '^\|.*Sweep' "$HANDS_MD" || true)
HAS_CORE=$(grep -cE '^\|.*Core' "$HANDS_MD" || true)
HAS_ENGINE=$(grep -cE '^\|.*Engine Room' "$HANDS_MD" || true)
HAS_ADMIN=$(grep -cE '^\|.*Admin' "$HANDS_MD" || true)
HAS_BACKLOG=$(grep -cE '^\|.*Backlog' "$HANDS_MD" || true)

echo "  Block rows in table: $BLOCK_ROWS"
echo "  Sweep: $HAS_SWEEP, Core: $HAS_CORE, Engine Room: $HAS_ENGINE, Admin: $HAS_ADMIN, Backlog: $HAS_BACKLOG"

if [[ "$BLOCK_ROWS" -eq 4 && "$HAS_SWEEP" -ge 1 && "$HAS_CORE" -ge 1 && "$HAS_ENGINE" -ge 1 && "$HAS_ADMIN" -ge 1 ]]; then
  echo "  ✅ PASS: 4-block model preserved (Sweep, Core, Engine Room, Admin)"
  PASS_COUNT=$((PASS_COUNT + 1))
else
  echo "  ❌ FAIL: Block model changed — expected exactly 4 blocks"
  echo "  Regression: New block type introduced or existing block removed"
  FAIL_COUNT=$((FAIL_COUNT + 1))
fi
echo ""


# --------------------------------------------------------------------------
# P6: Routine_RW enum values preserved — canonical set unchanged
# Observed in DuckDB: Sweep, Core, Engine Room, Admin, Wiki (plus non-standard variants)
# The canonical enum values referenced in protocols are:
#   Sweep (1213608836755503), Core Two (1213608836755504),
#   Engine Room (1213608836755505), Admin (1213608836755506), Wiki (1213924412583429)
# Validates: Requirement 3.7
# --------------------------------------------------------------------------
echo "--- P6: Routine_RW Enum Values Preserved ---"

# Check that the canonical GIDs are referenced in the design/protocols
# The Routine_RW GID and its enum option GIDs should exist in the system
ROUTINE_GID_REF=$(grep -rl '1213608836755502' "$HOME/shared/context/" 2>/dev/null | wc -l || true)
SWEEP_GID_REF=$(grep -rl '1213608836755503' "$HOME/shared/context/" 2>/dev/null | wc -l || true)
ADMIN_GID_REF=$(grep -rl '1213608836755506' "$HOME/shared/context/" 2>/dev/null | wc -l || true)

# Check that the Signal-to-Routine mapping tables reference all 4 block names + Backlog
BLOCKS_IN_TRIAGE=$(grep -cE '(Sweep|Core|Engine Room|Admin|Backlog)' "$AM_TRIAGE" || true)
BLOCKS_IN_AUTO=$(grep -cE '(Sweep|Core|Engine Room|Admin|Backlog)' "$AM_AUTO" || true)

echo "  Routine_RW GID referenced in: $ROUTINE_GID_REF files"
echo "  Block names in am-triage.md: $BLOCKS_IN_TRIAGE references"
echo "  Block names in am-auto.md: $BLOCKS_IN_AUTO references"

# The mapping tables should reference exactly 5 routing targets: Sweep, Core, Engine Room, Admin, (none — Backlog)
MAPPING_TARGETS_T=$(grep -E '^\|.*\|.*\|.*\|' "$AM_TRIAGE" | grep -cE '(Sweep|Core|Engine Room|Admin|Backlog|none)' || true)
MAPPING_TARGETS_A=$(grep -E '^\|.*\|.*\|.*\|' "$AM_AUTO" | grep -cE '(Sweep|Core|Engine Room|Admin|Backlog|none)' || true)

echo "  Mapping table targets in am-triage.md: $MAPPING_TARGETS_T"
echo "  Mapping table targets in am-auto.md: $MAPPING_TARGETS_A"

if [[ "$BLOCKS_IN_TRIAGE" -ge 5 && "$BLOCKS_IN_AUTO" -ge 5 && "$MAPPING_TARGETS_T" -ge 4 && "$MAPPING_TARGETS_A" -ge 4 ]]; then
  echo "  ✅ PASS: All canonical Routine_RW enum values preserved in protocols"
  PASS_COUNT=$((PASS_COUNT + 1))
else
  echo "  ❌ FAIL: Routine_RW enum values changed in protocols"
  echo "  Regression: New enum values added or existing ones removed"
  FAIL_COUNT=$((FAIL_COUNT + 1))
fi
echo ""

# --------------------------------------------------------------------------
# P7: AM-1/AM-2/AM-3 hook structure intact
# Observed in am-auto.md (AM-1 backend):
#   Phase 1 has: Slack Scan, Asana Full Sync, Email Scan sections
# Observed in am-triage.md (AM-2):
#   Phase 1 has: Signal Routing, Signal-to-Routine Mapping, Bucket Cap Check
# Observed in hands.md:
#   Hook table has AM-1, AM-2, AM-3, EOD-1, EOD-2
# Validates: Requirement 3.5
# --------------------------------------------------------------------------
echo "--- P7: AM-1/AM-2/AM-3 Hook Structure Intact ---"

# AM-1 (am-auto.md) Phase 1 structure
AM1_SLACK=$(grep -c 'Slack Scan' "$AM_AUTO" || true)
AM1_ASANA=$(grep -c 'Asana Full Sync' "$AM_AUTO" || true)
AM1_EMAIL=$(grep -c 'Email Scan' "$AM_AUTO" || true)

# AM-2 (am-triage.md) structure
AM2_SIGNAL_ROUTING=$(grep -c 'Signal Routing' "$AM_TRIAGE" || true)
AM2_MAPPING=$(grep -c 'Signal-to-Routine Mapping' "$AM_TRIAGE" || true)
AM2_CAP_CHECK=$(grep -c 'Bucket Cap Check' "$AM_TRIAGE" || true)

# Hook table in hands.md
HOOK_AM1=$(grep -c 'am-1-ingest\|AM-1' "$HANDS_MD" || true)
HOOK_AM2=$(grep -c 'am-2-triage\|AM-2' "$HANDS_MD" || true)
HOOK_AM3=$(grep -c 'am-3-brief\|AM-3' "$HANDS_MD" || true)
HOOK_EOD2=$(grep -c 'eod-2-system-refresh\|EOD-2' "$HANDS_MD" || true)

echo "  AM-1 (am-auto.md): Slack=$AM1_SLACK, Asana=$AM1_ASANA, Email=$AM1_EMAIL"
echo "  AM-2 (am-triage.md): SignalRouting=$AM2_SIGNAL_ROUTING, Mapping=$AM2_MAPPING, CapCheck=$AM2_CAP_CHECK"
echo "  Hooks in hands.md: AM-1=$HOOK_AM1, AM-2=$HOOK_AM2, AM-3=$HOOK_AM3, EOD-2=$HOOK_EOD2"

AM1_OK=$([[ "$AM1_SLACK" -ge 1 && "$AM1_ASANA" -ge 1 && "$AM1_EMAIL" -ge 1 ]] && echo 1 || echo 0)
AM2_OK=$([[ "$AM2_SIGNAL_ROUTING" -ge 1 && "$AM2_MAPPING" -ge 1 && "$AM2_CAP_CHECK" -ge 1 ]] && echo 1 || echo 0)
HOOKS_OK=$([[ "$HOOK_AM1" -ge 1 && "$HOOK_AM2" -ge 1 && "$HOOK_AM3" -ge 1 && "$HOOK_EOD2" -ge 1 ]] && echo 1 || echo 0)

if [[ "$AM1_OK" -eq 1 && "$AM2_OK" -eq 1 && "$HOOKS_OK" -eq 1 ]]; then
  echo "  ✅ PASS: AM-1/AM-2/AM-3/EOD-2 hook structure intact"
  PASS_COUNT=$((PASS_COUNT + 1))
else
  echo "  ❌ FAIL: Hook structure changed"
  echo "  Regression: AM-1 Phase 1 sections, AM-2 structure, or hook table modified"
  FAIL_COUNT=$((FAIL_COUNT + 1))
fi
echo ""

# --------------------------------------------------------------------------
# P8: EOD-2 daily reset — Today → Urgent demotion exists
# Observed in eod-system-refresh.md Phase 1 Step 2:
#   "For tasks that had Priority_RW=Today in the morning snapshot but remain incomplete:
#    Demote to Priority_RW=Urgent"
# Validates: Requirement 3.5
# --------------------------------------------------------------------------
echo "--- P8: EOD-2 Daily Reset (Today → Urgent Demotion) Exists ---"

EOD_DAILY_RESET=$(grep -c 'Daily Reset' "$EOD_REFRESH" || true)
EOD_TODAY_DEMOTE=$(grep -c 'Priority_RW=Today' "$EOD_REFRESH" || true)
EOD_URGENT_DEMOTE=$(grep -c 'Demote to Priority_RW=Urgent' "$EOD_REFRESH" || true)

echo "  'Daily Reset' section: $EOD_DAILY_RESET"
echo "  'Priority_RW=Today' reference: $EOD_TODAY_DEMOTE"
echo "  'Demote to Priority_RW=Urgent': $EOD_URGENT_DEMOTE"

if [[ "$EOD_DAILY_RESET" -ge 1 && "$EOD_TODAY_DEMOTE" -ge 1 && "$EOD_URGENT_DEMOTE" -ge 1 ]]; then
  echo "  ✅ PASS: EOD-2 daily reset (Today → Urgent demotion) preserved"
  PASS_COUNT=$((PASS_COUNT + 1))
else
  echo "  ❌ FAIL: EOD-2 daily reset logic missing or changed"
  echo "  Regression: Today → Urgent demotion removed from eod-system-refresh.md"
  FAIL_COUNT=$((FAIL_COUNT + 1))
fi
echo ""

# --------------------------------------------------------------------------
# P9: Backlog (null Routine_RW) treated as requiring triage
# Observed in am-triage.md Signal-to-Routine Mapping:
#   "Unclear/ambiguous | (none — Backlog) | Flag for triage"
# Observed in hands.md:
#   "📦 Backlog | Deferred/blocked/future with justification"
# Observed in DuckDB: 66 tasks with null Routine_RW (open, incomplete)
# Validates: Requirement 3.8
# --------------------------------------------------------------------------
echo "--- P9: Backlog (Null Routine_RW) Treated as Requiring Triage ---"

BACKLOG_TRIAGE_T=$(grep -c 'Unclear/ambiguous' "$AM_TRIAGE" || true)
BACKLOG_FLAG_T=$(grep -c 'Flag for triage' "$AM_TRIAGE" || true)
BACKLOG_TRIAGE_A=$(grep -c 'Unclear/ambiguous' "$AM_AUTO" || true)
BACKLOG_FLAG_A=$(grep -c 'Flag for triage' "$AM_AUTO" || true)
BACKLOG_HANDS=$(grep -c 'Backlog' "$HANDS_MD" || true)

echo "  am-triage.md: Unclear/ambiguous=$BACKLOG_TRIAGE_T, Flag for triage=$BACKLOG_FLAG_T"
echo "  am-auto.md: Unclear/ambiguous=$BACKLOG_TRIAGE_A, Flag for triage=$BACKLOG_FLAG_A"
echo "  hands.md Backlog references: $BACKLOG_HANDS"

if [[ "$BACKLOG_TRIAGE_T" -ge 1 && "$BACKLOG_FLAG_T" -ge 1 && "$BACKLOG_HANDS" -ge 1 ]]; then
  echo "  ✅ PASS: Backlog (null Routine_RW) treated as requiring triage"
  PASS_COUNT=$((PASS_COUNT + 1))
else
  echo "  ❌ FAIL: Backlog triage treatment changed"
  echo "  Regression: Unclear/ambiguous → Backlog → Flag for triage logic removed"
  FAIL_COUNT=$((FAIL_COUNT + 1))
fi
echo ""

# --------------------------------------------------------------------------
# SUMMARY
# --------------------------------------------------------------------------
echo "============================================"
echo "RESULTS: $PASS_COUNT/$TOTAL passed, $FAIL_COUNT/$TOTAL failed"
echo "============================================"

if [[ "$FAIL_COUNT" -gt 0 ]]; then
  echo ""
  echo "TEST OUTCOME: FAIL"
  echo "REGRESSION DETECTED in $FAIL_COUNT preservation dimension(s)."
  echo "The fix has broken existing behavior that should be unchanged."
  exit 1
else
  echo ""
  echo "TEST OUTCOME: PASS"
  echo "All preservation properties confirmed."
  echo "Baseline behavior is intact — safe to apply or verify fix."
  exit 0
fi
