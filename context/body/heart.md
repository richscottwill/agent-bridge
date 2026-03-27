# Heart — Autoresearch Loop

*Pure experimentation engine. Inspired by [autoresearch](https://github.com/karpathy/autoresearch) — 630 lines, 700 experiments, measurable results. Small, fast, autonomous, compounding. No human input needed. Runs overnight, low token usage, high volume.*

Last updated: 2026-03-26 (Karpathy — removed CHANGE_WEIGHT gate, added per-organ cooldown)
Created: 2026-03-20

---

## Architecture

The system uses a body metaphor. Each organ is a self-contained file. The loop experiments on these organs autonomously — no maintenance, no cascade, no suggestions. The morning routine handles maintenance. Karpathy handles experimentation.

### The Body (see `body.md` for full map)

| Organ | File | What experiments target |
|-------|------|----------------------|
| 🧠 Brain | `body/brain.md` | Decision log, principles, Five Levels |
| 👁️ Eyes | `body/eyes.md` | Market metrics, competitors, predicted QA |
| ✋ Hands | `body/hands.md` | Action tracker, dependencies |
| 🧠💬 Memory | `body/memory.md` | Compressed context, relationship graph, references |
| 🦴 Spine | `body/spine.md` | Bootstrap sequence, tool access, key IDs |
| 🧬 Nervous System | `body/nervous-system.md` | Calibration loops, pattern tracking, system health |
| 🔥 Anterior MCC | `body/amcc.md` | Willpower engine, streak, resistance taxonomy |
| 🫁 Gut | `body/gut.md` | Compression rules, word budgets, bloat detection |

### Directory Map

| Directory | Role |
|-----------|------|
| `~/shared/context/body/` | Body organs + device |
| `~/shared/context/active/` | Ground truth (current.md, org-chart.md, rw-tracker.md) |
| `~/shared/context/intake/` | Inbox for new material |
| `~/shared/context/tools/` | Utility scripts |
| `~/shared/context/archive/` | Cold storage |
| `~/shared/research/` | Standalone research, data files |
| `~/.kiro/steering/` | Agent behavior config (soul.md, rw-trainer.md) |

---

## The Metric

**Primary: usefulness per token** — does the organ answer the question it's supposed to answer, accurately and self-containedly, without requiring additional tool calls?

Three dimensions, measured on every experiment:

| Dimension | What It Measures | Score |
|-----------|-----------------|-------|
| Accuracy | Pose 3 questions about the organ's content. Are the answers correct from the organ alone? | 0-3 correct |
| Completeness | For each question, did the agent need to read another file to answer? | 0-3 self-contained (higher = better) |
| Token efficiency | Accuracy and completeness per token. If two versions answer equally well, the smaller one wins. But a larger version that's more accurate or complete beats a smaller one that isn't. | Tiebreaker only |

| Organ Category | Accuracy Threshold |
|---------------|-------------------|
| Brain, Memory | 100% (wrong decisions or relationship data = real harm) |
| Eyes, Hands | 95% (minor imprecision acceptable) |
| All others | 90% minimum |

**Secondary:** staleness (<20% stale facts), word count vs budget (budget is a constraint, not an objective).

---

## Run Protocol — Pure Autoresearch

When invoked (overnight, on-demand, or scheduled), the loop runs N experiments autonomously. No maintenance. No cascade. No suggestions. No human input.

### Step 1: Select Target
Karpathy selects:
- A target organ (weighted by: over-budget organs first, then lowest-accuracy, then least-recently-experimented)
- Exclude organs modified by maintenance in the current invocation (per-organ cooldown — if maintenance just rewrote eyes.md, don't experiment on eyes.md this run, but all other organs are fair game)
- An experiment type (COMPRESS, ADD, RESTRUCTURE, REMOVE, REWORD, MERGE, or SPLIT)
- A specific section within that organ

### Step 2: Snapshot
- Record word count of target organ
- Generate 5 eval questions about the target section's content (3 standard + 2 adversarial probing cross-organ boundaries and edge cases)
- Save snapshot for rollback

### Step 3: Apply Experiment
- Apply the selected technique to the selected section
- Experiment types (not limited to compression):
  - **COMPRESS**: resolve completed items, deduplicate, age-decay, structural compression (paragraphs→tables), protocol compression
  - **ADD**: inline a key fact that eliminates a tool call (e.g., a metric the agent always cross-references)
  - **RESTRUCTURE**: reorder so the most-queried data is found faster
  - **REMOVE**: delete content that's accurate but never queried (dead weight)
  - **REWORD**: same info, fewer tokens, less ambiguity
  - **MERGE**: combine sections that always get read together
  - **SPLIT**: separate sections that serve different query patterns

### Step 4: Evaluate — Dual Blind Subagent Review

The compressing agent does NOT evaluate its own work. Evaluation requires two independent blind subagent reviewers — one with full Amazon/system context, one generic (no Amazon context). This is the PR review for every experiment.

**4a. Generate eval questions (5 total):**
- 3 standard eval questions (accuracy + completeness, same as before)
- 2 adversarial questions designed to probe cross-organ boundaries, edge cases, or content that might have been lost in compression

**4b. Spawn two blind evaluators:**
- **Evaluator A (Amazon-context):** Receives the modified organ file + system context (body.md, soul.md). Answers all 5 questions. Scores each as CORRECT/PARTIAL/INCORRECT and SELF-CONTAINED/NEEDS-MORE-CONTEXT.
- **Evaluator B (Generic/no-context):** Receives ONLY the modified organ file. No system context, no body map, no soul.md. Answers all 5 questions with the same scoring.
- Neither evaluator sees the other's answers. Neither knows what was changed.

**4c. Score:**
- Per evaluator: count CORRECT + SELF-CONTAINED answers out of 5
- PARTIAL counts as 0.5 for scoring purposes
- Final score = minimum of the two evaluator scores (the weaker result is the real result)

### Step 5: Keep or Revert

**KEEP if ALL of the following:**
- Both evaluators score ≥4/5 (accuracy: CORRECT or PARTIAL on all 5)
- Both evaluators score ≥4/5 on self-containedness (SELF-CONTAINED on at least 4 of 5)
- No evaluator scores any question as INCORRECT (a single INCORRECT = automatic REVERT for critical organs Brain/Memory; for others, 1 INCORRECT is allowed if overall score ≥4/5)
- Accuracy meets organ-specific thresholds: Brain/Memory 100%, Eyes/Hands 95%, others 90%

**REVERT if ANY of the following:**
- Either evaluator scores <4/5 overall
- Any INCORRECT on a Brain/Memory experiment
- Both evaluators flag the same gap as NEEDS-MORE-CONTEXT (signals a real hole, not evaluator noise)
- Completeness drops vs baseline (agent needs more cross-file reads than before)

**PARTIAL handling:**
- If both evaluators flag the same question as PARTIAL with the same gap → the experiment is KEPT but the gap must be fixed before the experiment is closed. Log the gap, apply a targeted fix (one-liner preferred), re-verify.
- If only one evaluator flags PARTIAL and the other scores CORRECT → acceptable. Modular systems inherently have cross-organ questions. No fix required.
- If 2+ questions score PARTIAL → ITERATE. The compression went too far. Restore content and try a lighter touch.

**Portability signal:**
- If the Amazon-context evaluator passes but the generic evaluator fails → the organ has implicit dependencies on system context. Flag for CE-6 (portability) consideration. The experiment still KEEPs if the Amazon-context score meets thresholds (the organ lives in this system), but the portability gap is logged.

- Log result to changelog.md

### Step 6: Repeat
- Run up to `max_experiments_per_batch` experiments per invocation
- Stop early if: no more over-budget organs, or 3 consecutive reverts (diminishing returns)

---

## Hyperparameters

| Param | Value | Rationale |
|-------|-------|-----------|
| max_experiments_per_batch | 5 | Balance between throughput and token cost |
| total_body_word_ceiling | 24,000 | Hard cap across all organs |
| staleness_threshold | 7 days | Flag organ section if older than this |
| eval_questions_per_exp | 5 (3 standard + 2 adversarial) | Dual blind eval requires broader coverage |
| eval_method | dual_blind_subagent | Two independent evaluators (Amazon-context + generic). Compressing agent never self-evaluates. |
| eval_pass_threshold | ≥4/5 both evaluators | Minimum score to KEEP. PARTIAL = 0.5. |
| accuracy_threshold_critical | 100% | Brain, Memory |
| accuracy_threshold_standard | 95% | Eyes, Hands |
| accuracy_threshold_system | 90% | Spine, Device, NS, aMCC, Gut |
| experiment_word_budget_rule | within organ budget | Experiments can increase word count if accuracy or completeness improves, as long as organ stays within gut.md budget |
| consecutive_revert_stop | 3 | Stop batch if 3 reverts in a row |
| experiment_cooldown_per_organ | same invocation | Don't experiment on an organ that was modified by maintenance in the current invocation. Other organs are fair game. |
| target_selection_weight | over-budget first, then lowest-accuracy | Prioritize organs exceeding budget, then organs with known accuracy gaps |

---

## Experiment Queue

Experiments are generated dynamically by Karpathy during each batch run. The queue below contains pre-designed experiments that take priority over random generation. Completed/adopted experiments are logged in changelog.md — only QUEUED experiments live here.

### CE-5: Device Dead-Weight Removal — QUEUED (next)
- **Hypothesis:** Device (1,829w, 91% of 2,000w budget) contains aspirational content that hasn't been acted on — 5 proposed Background Monitors (none built, no timeline), 7 unbuilt Tool Factory entries, and a reversed delegation (AU → Harjeet) that's just historical. Removing dead-weight proposals and compressing the reversed delegation to a one-liner will improve usefulness per token by surfacing what's actually running vs. what's aspirational.
- **Type:** REMOVE + COMPRESS
- **Target:** Device — Background Monitors section (proposed, not built), Tool Factory table (compress unbuilt entries), reversed delegation (AU → Harjeet)
- **Do-no-harm:** Device accuracy must stay ≥90%. All active/running systems (Morning Routine, Loop, Safety Guards, Karpathy, Hedy) must be fully preserved. Active delegations (MX Invoice, MX Keywords, WBR Coverage, OP1 Contributors) preserved.
- **Eval questions:**
  1. What does the Morning Routine hook do? → One-click daily chain: Asana Sync → Draft Replies → To-Do Refresh + Daily Brief → Calendar Blocks
  2. Who owns MX keyword sourcing delegation? → Lorena Alvarez Larrea (IN PROGRESS)
  3. What tool has been built and is active? → Dashboard ingester (✅ BUILT)
- **Expected impact:** −200-300w (target ≤1,600w, 80% utilization). No accuracy loss — removed content is aspirational, not functional.

### CE-6: Cross-Environment Prompt Portability — QUEUED
- **Hypothesis:** The body is optimized for AgentSpaces (Amazon's Kiro/Claude environment) but Richard also uses non-Amazon AI tools (ChatGPT, other Claude interfaces, potentially Cursor). Organs contain AgentSpaces-specific assumptions (file paths like `~/shared/context/`, hook names, MCP tool references) that make them less useful when loaded into other environments. If we add a portable preamble section to spine.md that maps environment-specific paths/tools to generic equivalents, AND restructure the 3 most-queried organs (Memory, Brain, aMCC) to front-load the highest-value content in the first 500 tokens, the body becomes useful in ANY AI environment — not just this one. This directly increases usefulness-per-token because the same content serves more contexts.
- **Type:** RESTRUCTURE + ADD
- **Target:** Spine (add portable preamble), Memory (front-load relationship graph), Brain (front-load active decisions + Five Levels), aMCC (front-load streak + hard thing)
- **Specific changes to test:**
  1. **Spine portable preamble (~50w):** Add an environment-agnostic header that maps `~/shared/context/` → `[BODY_ROOT]`, lists organs by function (not file path), and provides a 2-line "if you're not in AgentSpaces, here's how to load this" instruction.
  2. **Memory front-loading:** Move the relationship graph and compressed context to the top. When a non-Amazon AI loads Memory with a token limit, it gets the highest-value content first. (Note: meeting briefs have been moved to ~/shared/context/meetings/ — Memory no longer holds them.)
  3. **Brain front-loading:** Move Five Levels summary and active decisions ABOVE the full decision log. Same rationale — most-queried content first.
  4. **aMCC front-loading:** Streak table and current hard thing are already near the top. Verify no restructure needed.
- **Do-no-harm:** All accuracy thresholds must hold. Brain/Memory at 100%. No content removed — only reordered and augmented. All organs must stay within budget. Spine has 276w of headroom (1,224w vs 1,500w budget). Memory has 1,093w headroom. Brain has 437w headroom.
- **Eval questions:**
  1. If I paste Brain into ChatGPT with a 2K token limit, can it answer "What are Richard's Five Levels?" → Must be YES (currently: depends on where truncation hits)
  2. If I paste Memory into a non-AgentSpaces Claude, can it answer "Who is Brandon Munday and what does he care about?" → Must be YES
  3. Can an agent in AgentSpaces still navigate the body using Spine? → Must be YES (no regression)
- **Expected impact:** +50-80w to Spine (within budget). Net zero on Memory and Brain (reorder only). Body becomes functional in ChatGPT, Claude.ai, Cursor, and any future AI environment. Usefulness-per-token increases because the same tokens serve more use cases.
- **Portability test protocol:** After restructure, paste each modified organ into ChatGPT (free tier, ~4K context) and Claude.ai. Ask the eval questions. If answers are correct from the truncated paste, the restructure worked.

### CE-7: Cold-Start Validation — QUEUED
- **Hypothesis:** portable-body/ files claim a new AI can bootstrap from README.md + one organ in 2-3 hours. This has never been tested. If a generic blind evaluator given only portable-body/README.md + portable-body/body/brain.md can answer "What should Richard work on today?" with a useful response, the cold-start path works. If not, the portable body has a bootstrap gap.
- **Type:** EVAL (no modification — pure validation)
- **Target:** portable-body/README.md + portable-body/body/brain.md
- **Do-no-harm:** Read-only test. No organs modified.
- **Eval questions:**
  1. Given only README.md + brain.md, can the evaluator identify Richard's top priority? → Must reference Five Levels / Level 1.
  2. Can the evaluator suggest a concrete next action? → Must be actionable, not generic.
  3. Does the evaluator understand the system architecture well enough to ask for the right next file? → Should request soul.md or current.md, not random files.
- **Expected impact:** Validates or invalidates the bootstrap protocol. If FAIL, feeds directly into CE-6 restructure priorities.

---

## Design Choices

- **Pure autoresearch.** The loop is experimentation only. Maintenance and cascade are handled by the morning routine. No human input needed during loop runs.
- **Current-state-only organs.** Organs hold current state, not history. changelog.md is the audit trail. No append-only logs in organs.
- **Body metaphor.** Organs replace numbered experiment files. Each organ is self-contained.
- **Do no harm.** Organ-specific accuracy thresholds. Brain/Memory = 100%. Rollback is immediate and automatic.
- **Usefulness over size.** Word budgets are constraints (ceilings), not objectives. An organ at 95% of budget that answers everything correctly is fine. An organ at 50% that misses questions needs content added. Experiments optimize for usefulness per token within the budget ceiling.
- **Advance or reset.** Every experiment meets ALL criteria (accuracy + completeness) or gets reverted. No partial advances.
- **Dual blind eval.** The compressing agent never evaluates its own work. Two independent blind subagent reviewers (one Amazon-context, one generic) score 5 questions (3 standard + 2 adversarial). Both must score ≥4/5 to KEEP. Same gap flagged by both evaluators = real hole that must be fixed. Adopted after CE-3/CE-4 post-hoc blind eval exposed that self-grading missed gaps a blind reviewer caught.
- **Random + weighted selection.** Experiments target over-budget organs first, then lowest-accuracy organs, then random selection.
- **Batch execution.** Multiple experiments per invocation, stopping on diminishing returns (3 consecutive reverts).
- **Per-organ cooldown replaces global gate.** The old CHANGE_WEIGHT > 10 gate blocked experiments on 5/6 runs because maintenance always touches 100+ lines. The per-organ cooldown is surgically precise: don't experiment on an organ that maintenance just modified in the same invocation, but all other organs are fair game. The dual blind eval already catches accuracy loss — the cooldown is belt-and-suspenders. Adopted 3/26 after Karpathy assessment showed the gate was effectively dead code.
- **Portability as continuous constraint.** Every organ change must work on a cold platform with only text files. The generic blind evaluator tests this on every experiment. portable-body/ is the test artifact — if the generic evaluator can't answer from a portable-body file, the body isn't portable.

## Governance

All changes to this file, the experiment queue, hyperparameters, and run protocol are governed by the Karpathy agent. No other agent or process modifies heart.md directly. The loop executes. Karpathy governs.
