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

## 2026-04-05 — heart.md (eval invocation pattern change)

**File:** `shared/context/body/heart.md`
**Timestamp:** 2026-04-05
**Change:** Step 4 eval agent invocation refactored from `invokeSubAgent` to CLI-based invocation (`.json` agent configs). Rationale stated in diff: "CLI invocation avoids the subagent-can't-invoke-subagent limitation."
**Diff:** Single line — `Karpathy orchestrates the blind eval by invoking eval agents as subagents (same pattern as wiki pipeline blind reviews). Each eval agent receives its context via invokeSubAgent prompt...` → `Karpathy orchestrates the blind eval by invoking eval agents via CLI (.json agent configs). Each eval agent runs as an independent CLI agent with its own context...`
**Cross-organ impact:** None detected. device.md references karpathy but not the specific invocation mechanism. The Governance section at the bottom of heart.md already states "Karpathy runs as a CLI agent (not a subagent) so it can invoke eval agents A/B/C as independent CLI agents" — this edit makes Step 4 consistent with that existing governance statement. The kiro-setup-optimization design doc references custom subagents as a Phase 2 opportunity for agent routing generally, but does not depend on the eval invocation pattern.
**Authorization:** ⚠️ heart.md is gated — only the karpathy agent has authority to modify this file. This edit was detected via fileEdited hook, not from a karpathy-invoked session. The change is substantive (alters the eval pipeline's invocation mechanism) but makes Step 4 consistent with the Governance section already in heart.md. If Richard made this edit directly to resolve an internal inconsistency, it's a valid correction. If an unauthorized agent made it, flag for karpathy review.

## 2026-04-05 — gut.md

**Change:** Updated Karpathy authority definition in §Governance. Replaced "the executing agent acting under karpathy.md identity (during experiment runs) OR a Karpathy subagent (during governance proposals)" with "the Karpathy CLI agent (`karpathy.json`) running experiment batches, or any agent acting under karpathy.md identity during governance proposals."

**Impact:** Semantic — aligns governance language with CLI-based experiment execution model. No functional change to who owns gut.md.

**Cross-organ conflicts:** None detected. device.md and soul.md references to karpathy remain consistent.

**Gated file flag:** gut.md is Karpathy-gated. Edit source unverified — if manual, ratify during next Karpathy loop run.
