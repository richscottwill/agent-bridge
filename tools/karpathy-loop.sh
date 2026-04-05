#!/bin/bash
# Karpathy autoresearch loop — runs batches until target experiment count reached.
# Each batch: Karpathy selects+applies experiments, THIS SCRIPT runs the blind eval via CLI agents.
# Usage: bash ~/shared/tools/karpathy-loop.sh [total_experiments] [cooldown_organs]

TARGET_TOTAL=${1:-100}
COOLDOWN=${2:-"hands.md"}
BATCH_SIZE=10
DB_PATH="/home/prichwil/shared/data/duckdb/ps-analytics.duckdb"
LOG="$HOME/shared/context/active/karpathy-loop.log"
KIRO_CLI="/agentspaces/kiro-cli/kiro-cli"

echo "$(date -Iseconds) Karpathy loop started. Target: $TARGET_TOTAL experiments." | tee -a "$LOG"

while true; do
  CURRENT=$(python3 -c "
import duckdb
con = duckdb.connect('$DB_PATH', read_only=True)
r = con.execute('SELECT COUNT(*) FROM autoresearch_experiments').fetchone()
print(r[0])
con.close()
" 2>/dev/null)

  if [ -z "$CURRENT" ]; then
    echo "$(date -Iseconds) ERROR: Could not read experiment count" | tee -a "$LOG"
    break
  fi

  REMAINING=$((TARGET_TOTAL - CURRENT))
  echo "$(date -Iseconds) Current: $CURRENT experiments. Remaining: $REMAINING." | tee -a "$LOG"

  if [ "$REMAINING" -le 0 ]; then
    echo "$(date -Iseconds) Target reached ($CURRENT >= $TARGET_TOTAL). Done." | tee -a "$LOG"
    break
  fi

  BATCH=$BATCH_SIZE
  if [ "$REMAINING" -lt "$BATCH" ]; then
    BATCH=$REMAINING
  fi

  echo "$(date -Iseconds) Launching Karpathy for ~$BATCH experiments..." | tee -a "$LOG"

  # Karpathy selects targets, applies experiments, writes eval prompts to /tmp/eval-*.txt,
  # and writes experiment metadata to /tmp/exp-meta.json. It does NOT score — this script does.
  $KIRO_CLI chat --agent karpathy --no-interactive --trust-all-tools \
    "Run ~$BATCH autoresearch experiments. Cooldown: $COOLDOWN. All targets fair game per your protocol.

IMPORTANT — EVAL PROTOCOL:
For EACH experiment, after applying the change:
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

You MUST run the kiro-cli commands above via shell tool. Do NOT answer eval questions yourself. The eval agents must run as separate processes." \
    2>&1 | tee -a "$LOG"

  echo "$(date -Iseconds) Batch complete." | tee -a "$LOG"
  sleep 2
done

echo "$(date -Iseconds) Loop complete." | tee -a "$LOG"
python3 -c "
import duckdb
con = duckdb.connect('$DB_PATH', read_only=True)
total = con.execute('SELECT COUNT(*) FROM autoresearch_experiments').fetchone()[0]
keeps = con.execute(\"SELECT COUNT(*) FROM autoresearch_experiments WHERE decision='KEEP'\").fetchone()[0]
reverts = con.execute(\"SELECT COUNT(*) FROM autoresearch_experiments WHERE decision='REVERT'\").fetchone()[0]
print(f'Total: {total}. Keeps: {keeps} ({100*keeps//max(total,1)}%). Reverts: {reverts} ({100*reverts//max(total,1)}%).')
con.close()
" 2>&1 | tee -a "$LOG"