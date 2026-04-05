# Organ Changes Log

## 2026-04-05 — heart.md (consolidated)

**File:** `shared/context/body/heart.md`
**Changes (net result after all edits):**
1. Step 4 refactored: eval agents now invoked via `invokeSubAgent` (same pattern as wiki pipeline). A/B/C blind eval preserved — Agent C (zero context portability) runs on Tier 2 experiments.
2. Fast-fail gate added between Agent A and Agent B: if Agent A scores 50%+ INCORRECT, skip Agent B and mark REVERT with `fast_fail`. Does NOT apply to Brain/Memory.
3. Structured eval output: results written to `~/shared/context/active/experiment-results-latest.json` (overwritten each experiment, keeps eval output out of context window).
4. experiment-log.tsv: one row per experiment appended to `~/shared/context/active/experiment-log.tsv` (human-scannable, git-trackable — analog of Karpathy autoresearch's results.tsv).
5. Logging format updated: fast_fail experiments get logged with `B=- Δ=-` notation.

**What was NOT changed:** Scoring logic (CORRECT/PARTIAL/INCORRECT), decision thresholds (delta_ab ≥ 0), Brain/Memory zero-tolerance rule, Bayesian prior mechanism, 7 techniques, target categories, tiered eval (Tier 1 = A+B, Tier 2 = A+B+C).

**Authorization:** Karpathy-authority changes (loop protocol, eval pipeline). Richard directed implementation.
**Cross-organ impact:** None. New files created (experiment-log.tsv, experiment-results-latest.json) are in active/ directory. karpathy.md and karpathy.json updated to match. All copies verified in sync.

**Note:** Canonical eval questions concept was briefly added then removed in the same session. It was not from Karpathy's autoresearch — it was an agent invention. The frozen eval harness equivalent is the scoring protocol itself, which is already immutable in heart.md. No residual references remain in any file.

## 2026-04-05 — heart.md (heading correction)

**File:** `shared/context/body/heart.md`
**Change:** Step 4 heading updated from "A/B Blind Eval" to "A/B/C Blind Eval"
**Diff:** Single line — `### Step 4: Evaluate — A/B Blind Eval` → `### Step 4: Evaluate — A/B/C Blind Eval`
**Cross-organ impact:** None. This corrects a stale heading — the rest of the system (karpathy.md, portable-body/heart.md, agent-bridge/heart.md, session-log.md, hooks-inventory.md) already uses "A/B/C" terminology. The heading was the only remaining "A/B" reference.
**Authorization:** ⚠️ Edit source unknown. heart.md is gated — only the karpathy agent has authority to modify this file. This edit was detected via fileEdited hook, not from a karpathy-invoked session. If Richard made this edit directly, it's a minor heading fix that aligns with existing terminology. If an unauthorized agent made it, flag for review.
