#!/bin/bash
# Karpathy autoresearch loop — runs batches until Bayesian priors exhaust eligible targets.
# No artificial cap. The priors ARE the stopping mechanism (heart.md Step 6).
# Each batch: Karpathy selects+applies experiments, blind eval via CLI agents.
# Usage: bash ~/shared/tools/karpathy-loop.sh [cooldown_organs] [max_batches]
#   cooldown_organs: comma-separated organs modified this invocation (default: "hands.md")
#   max_batches: safety limit on batch iterations (default: 20, ~200 experiments)
#     This is NOT an experiment cap — it prevents infinite loops if exhaustion detection fails.
#     Set higher if needed. The real stop is prior exhaustion.

COOLDOWN=${1:-"hands.md"}
MAX_BATCHES=${2:-20}
BATCH_SIZE=10
DB_PATH="/home/prichwil/shared/data/duckdb/ps-analytics.duckdb"
LOG="$HOME/shared/context/active/karpathy-loop.log"
KIRO_CLI="/agentspaces/kiro-cli/kiro-cli"
BATCH_RESULT_FILE="/tmp/karpathy-batch-result.txt"
EXHAUSTION_MARKER="/tmp/karpathy-exhausted"

# Clean up from previous runs
rm -f "$EXHAUSTION_MARKER"

# Get starting experiment count
START_COUNT=$(python3 -c "
import duckdb
con = duckdb.connect('$DB_PATH', read_only=True)
r = con.execute('SELECT COUNT(*) FROM autoresearch_experiments').fetchone()
print(r[0])
con.close()
" 2>/dev/null)

echo "$(date -Iseconds) Karpathy loop started. Mode: prior-driven (no artificial cap)." | tee -a "$LOG"
echo "$(date -Iseconds) Starting experiments: $START_COUNT. Cooldown: $COOLDOWN. Max batches: $MAX_BATCHES." | tee -a "$LOG"

# Log eligible target stats
python3 -c "
import duckdb
con = duckdb.connect('$DB_PATH', read_only=True)
total = con.execute('SELECT COUNT(*) FROM autoresearch_priors').fetchone()[0]
unexplored = con.execute('SELECT COUNT(*) FROM autoresearch_priors WHERE n_experiments = 0').fetchone()[0]
underexplored = con.execute('SELECT COUNT(*) FROM autoresearch_priors WHERE n_experiments > 0 AND n_experiments < 3').fetchone()[0]
proven_losers = con.execute(\"\"\"SELECT COUNT(*) FROM autoresearch_priors 
  WHERE (alpha / (alpha + beta)) < 0.15 AND n_experiments > 10\"\"\").fetchone()[0]
eligible = total - proven_losers
print(f'Prior state: {total} combos, {unexplored} unexplored, {underexplored} underexplored, {proven_losers} proven losers, {eligible} eligible.')
con.close()
" 2>&1 | tee -a "$LOG"

BATCH_NUM=0
CONSECUTIVE_EMPTY=0

while true; do
  BATCH_NUM=$((BATCH_NUM + 1))

  # Safety: max batch limit (prevents infinite loop, not an experiment cap)
  if [ "$BATCH_NUM" -gt "$MAX_BATCHES" ]; then
    echo "$(date -Iseconds) Safety limit: $MAX_BATCHES batches reached. Stopping." | tee -a "$LOG"
    echo "$(date -Iseconds) This is a safety limit, not a target. Increase max_batches if priors still have eligible targets." | tee -a "$LOG"
    break
  fi

  # Get current count before batch
  PRE_BATCH=$(python3 -c "
import duckdb
con = duckdb.connect('$DB_PATH', read_only=True)
r = con.execute('SELECT COUNT(*) FROM autoresearch_experiments').fetchone()
print(r[0])
con.close()
" 2>/dev/null)

  echo "$(date -Iseconds) Batch $BATCH_NUM/$MAX_BATCHES. Experiments so far: $PRE_BATCH (started at $START_COUNT)." | tee -a "$LOG"

  # Launch Karpathy batch
  echo "$(date -Iseconds) Launching Karpathy for ~$BATCH_SIZE experiments..." | tee -a "$LOG"

  $KIRO_CLI chat --agent karpathy --no-interactive --trust-all-tools \
    "Run ~$BATCH_SIZE autoresearch experiments. Cooldown: $COOLDOWN. All targets fair game per your protocol.

TERMINATION SIGNAL: If you cannot find any eligible target×technique combos (all on cooldown, all proven losers, or all exhausted), write the file /tmp/karpathy-exhausted with a one-line reason and stop. Do NOT invent experiments on ineligible targets just to fill the batch.

IMPORTANT — EVAL PROTOCOL:
For EACH experiment, after applying the change:

0. **STRUCTURAL VALIDITY GATE (mandatory, pre-eval).** Check modified file parses correctly for its type. If fail → auto-REVERT with revert_reason='structural_invalidity', restore from snapshot, log to autoresearch_experiments with eval scores NULL, update priors, skip to next experiment. Do NOT invoke eval agents on structurally invalid files.

   | Extension | Check |
   |---|---|
   | .kiro.hook, .json | python3 -c 'import json; json.loads(open(\"PATH\").read())' |
   | .py | python3 -c 'import ast; ast.parse(open(\"PATH\").read())' |
   | .sh | bash -n PATH |
   | .yml, .yaml | python3 -c 'import yaml; yaml.safe_load(open(\"PATH\"))' |
   | .md, .txt, unknown | no check — proceed to step 1 |

   Added 2026-04-29 after W18 batch broke 13 hook JSONs that scored high on output_quality while being runtime-invalid. Eval agents cannot detect invalid JSON — they read prose.

1. Write the eval-a prompt (modified target + body.md + soul.md + questions) to /tmp/eval-a-exp.txt
2. Write the eval-b prompt (ORIGINAL target + body.md + soul.md + same questions) to /tmp/eval-b-exp.txt  
3. Write the eval-c prompt (modified target ONLY + same questions) to /tmp/eval-c-exp.txt
4. Write ground truth answers to /tmp/eval-ground-truth.txt
5. Run the blind eval by executing these EXACT shell commands (copy-paste, do not paraphrase):

$KIRO_CLI chat --agent eval-a --no-interactive --trust-all-tools \"\$(cat /tmp/eval-a-exp.txt)\" 2>/dev/null | tail -20 > /tmp/eval-a-result.txt
$KIRO_CLI chat --agent eval-b --no-interactive --trust-all-tools \"\$(cat /tmp/eval-b-exp.txt)\" 2>/dev/null | tail -20 > /tmp/eval-b-result.txt
$KIRO_CLI chat --agent eval-c --no-interactive --trust-all-tools \"\$(cat /tmp/eval-c-exp.txt)\" 2>/dev/null | tail -20 > /tmp/eval-c-result.txt

6. Read /tmp/eval-a-result.txt, /tmp/eval-b-result.txt, /tmp/eval-c-result.txt
7. Score against /tmp/eval-ground-truth.txt. Detail-loss = PARTIAL not CORRECT.
8. Compute delta_ab. Keep or revert per heart.md Step 5.
9. Log to DuckDB + experiment-log.tsv.

You MUST run the kiro-cli commands above via shell tool. Do NOT answer eval questions yourself. The eval agents must run as separate processes.

After completing all experiments in this batch, write a summary line to /tmp/karpathy-batch-result.txt:
BATCH_COMPLETE: [N] experiments run, [K] kept, [R] reverted" \
    2>&1 | tee -a "$LOG"

  echo "$(date -Iseconds) Batch $BATCH_NUM complete." | tee -a "$LOG"

  # Check exhaustion signal from Karpathy
  if [ -f "$EXHAUSTION_MARKER" ]; then
    REASON=$(cat "$EXHAUSTION_MARKER" 2>/dev/null)
    echo "$(date -Iseconds) Karpathy signaled exhaustion: $REASON" | tee -a "$LOG"
    break
  fi

  # Check if batch actually produced experiments (DuckDB count delta)
  POST_BATCH=$(python3 -c "
import duckdb
con = duckdb.connect('$DB_PATH', read_only=True)
r = con.execute('SELECT COUNT(*) FROM autoresearch_experiments').fetchone()
print(r[0])
con.close()
" 2>/dev/null)

  BATCH_DELTA=$((POST_BATCH - PRE_BATCH))
  echo "$(date -Iseconds) Batch produced $BATCH_DELTA new experiments ($PRE_BATCH → $POST_BATCH)." | tee -a "$LOG"

  # If batch produced zero experiments, Karpathy may be stuck or exhausted
  if [ "$BATCH_DELTA" -eq 0 ]; then
    CONSECUTIVE_EMPTY=$((CONSECUTIVE_EMPTY + 1))
    echo "$(date -Iseconds) WARNING: Empty batch ($CONSECUTIVE_EMPTY consecutive)." | tee -a "$LOG"
    if [ "$CONSECUTIVE_EMPTY" -ge 2 ]; then
      echo "$(date -Iseconds) Two consecutive empty batches. Likely exhausted or stuck. Stopping." | tee -a "$LOG"
      break
    fi
  else
    CONSECUTIVE_EMPTY=0
  fi

  sleep 2
done

# Final summary
FINAL_COUNT=$(python3 -c "
import duckdb
con = duckdb.connect('$DB_PATH', read_only=True)
total = con.execute('SELECT COUNT(*) FROM autoresearch_experiments').fetchone()[0]
keeps = con.execute(\"SELECT COUNT(*) FROM autoresearch_experiments WHERE decision='KEEP'\").fetchone()[0]
reverts = con.execute(\"SELECT COUNT(*) FROM autoresearch_experiments WHERE decision='REVERT'\").fetchone()[0]
new = total - $START_COUNT
print(f'Session: {new} new experiments. Total: {total}. Keeps: {keeps} ({100*keeps//max(total,1)}%). Reverts: {reverts} ({100*reverts//max(total,1)}%).')
con.close()
" 2>&1)

echo "$(date -Iseconds) $FINAL_COUNT" | tee -a "$LOG"
echo "$(date -Iseconds) Loop complete." | tee -a "$LOG"
