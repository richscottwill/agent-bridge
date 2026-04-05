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

## 2026-04-05 — heart.md (selection bias threshold change)

**File:** `shared/context/body/heart.md`
**Timestamp:** 2026-04-05
**Change:** Selection bias check threshold in Stage 2 (Technique selection) lowered from >85% keep rate to >50%. "Healthy batch" redefined from 50-70% keep rate to ≤50%. Added Karpathy autoresearch citation: "700 experiments, most fail, learning emerges from the pattern of failures." The edit makes the experiment philosophy more aggressive — most experiments should revert, not most should keep.
**Diff:** Single line in Step 1 Stage 2 — `keep rate >85%` → `keep rate >50%`, `50-70% keep rate — not 90%+` → `≤50% keep rate. Most experiments should revert — that's the point.`
**Cross-organ impact:** None detected. gut.md discusses per-organ experiment signals (ADD/COMPRESS posterior means) which operate at a different level than the batch-level selection bias check in heart.md. The two thresholds are independent — gut.md says when to stop adding to a specific organ, heart.md says when the overall experiment selection is too conservative. No conflict.
**Authorization:** ⚠️ heart.md is gated — only the karpathy agent has authority to modify this file. This edit was detected via fileEdited hook, not from a karpathy-invoked session. The change is substantive (halves the keep-rate threshold, fundamentally shifts experiment philosophy toward more aggressive exploration). The Karpathy autoresearch citation suggests this may have been a deliberate karpathy-directed change. If Richard made this edit directly based on karpathy's recommendation, ratify during next Karpathy loop run. If an unauthorized agent made it, flag for karpathy review.

## 2026-04-05 — heart.md

**File:** shared/context/body/heart.md
**Change summary:** Refactored "The Metric" section. Replaced 4-dimension table (Accuracy delta, Portability, Efficiency, Latency) with expanded 6-signal "Experiment Signals" table (Accuracy delta, Portability, Word delta, Latency, Eval question difficulty, Context size). Key conceptual shifts: (1) "organ" → "output" in primary metric description, (2) "organ×technique" → "target×technique" in threshold language, (3) Efficiency yield formula removed — replaced with word delta as a neutral covariate, (4) Latency reframed from penalty (>120s = LOW_EFFICIENCY) to neutral signal, (5) Two new signals added: eval question difficulty and context size, (6) Added "Over time" paragraph describing Bayesian learning across signal combinations. Secondary metrics line removed.
**Karpathy gated:** ⚠️ FLAGGED — heart.md is karpathy-gated. The `Last updated` line still reads "Karpathy Run 26" (not updated to reflect this edit). This edit was NOT made by the karpathy agent — it appears to be a manual/direct edit. Per governance rules, heart.md edits require karpathy authority.
**Cross-organ inconsistencies:**
- `gut.md` references "organ×technique" terminology and Bayesian priors — heart.md now uses "target×technique" in the edited section but retains "organ×technique" elsewhere in the same file (line ~241). Terminology is inconsistent within heart.md itself.
- `portable-body/body/heart.md` and `agent-bridge/body/heart.md` still have the OLD 4-dimension table with the Efficiency yield formula. These copies are now out of sync with the canonical heart.md.
- `changelog.md` references the old Efficiency yield formula and "organ×technique" terminology — historical record, no update needed.
- `karpathy.md` (both copies) references "organ×technique combos" in the Experiment Execution Protocol — terminology mismatch with the new "target×technique" in heart.md.

## 2026-04-05 — heart.md (Step 5 quality-over-size clarification)

**File:** `shared/context/body/heart.md`
**Timestamp:** 2026-04-05
**Change:** Added clarification to Step 5 (Keep or Revert) that output quality is the goal, not smaller files. New sentence: "The goal is output quality, not smaller files. A KEEP that adds 50 words but improves delta_ab by +0.1 is better than a KEEP that removes 100 words with delta_ab = 0.0."
**Diff:** Single line — appended to the existing "The decision is based on delta (did it improve?), not absolute score (is it above a floor?)." sentence.
**Cross-organ impact:** Consistent with gut.md. Gut's adaptive budget philosophy already states "If a larger organ answers more questions correctly, the budget expands" and "budgets are learned, not declared." The heart.md edit makes the same principle explicit at the experiment decision level — quality improvement justifies word count increases. No conflict detected.
**Authorization:** ⚠️ heart.md is gated — only the karpathy agent has authority to modify this file. This edit was detected via fileEdited hook, not from a karpathy-invoked session. The change is philosophically aligned with existing heart.md and gut.md principles (delta-based decisions, adaptive budgets). If Richard made this edit directly to reinforce the quality-over-compression principle, ratify during next Karpathy loop run. If an unauthorized agent made it, flag for karpathy review.

## 2026-04-05 — heart.md (scoring detail-loss rule)

**File:** `shared/context/body/heart.md`
**Timestamp:** 2026-04-05
**Change:** Added "Scoring detail-loss" bullet to the information-retrieval evals section. New rule: if Agent B gives a richer answer than Agent A for the same question (e.g., B includes specific numbers while A gives only a percentage), score A as PARTIAL on that question. This makes compression damage detectable — delta turns negative when detail is lost, even if the headline fact survives.
**Diff:** Single bullet added under `score_a, score_b, score_c` line in the eval scoring block.
**Cross-organ impact:** None detected. Consistent with gut.md's adaptive budget philosophy (quality over compression). Consistent with the Step 5 "quality-over-size" clarification logged earlier today. The new rule operationalizes the same principle at the scoring level — detail loss is now measurable, not just philosophically discouraged.
**Authorization:** ⚠️ heart.md is gated — only the karpathy agent has authority to modify this file. This edit was detected via fileEdited hook, not from a karpathy-invoked session. The change is substantive (adds a new scoring rule that affects how delta_ab is computed). If Richard made this edit directly or based on karpathy's recommendation, ratify during next Karpathy loop run. If an unauthorized agent made it, flag for karpathy review.
