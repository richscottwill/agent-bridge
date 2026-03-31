# Heart — Autoresearch Loop

*Pure experimentation engine. Inspired by [autoresearch](https://github.com/karpathy/autoresearch) — 630 lines, 700 experiments, measurable results. Small, fast, autonomous, compounding. No human input needed. Runs overnight, low token usage, high volume.*

Last updated: 2026-03-31 (Karpathy — experiment overhaul: random generation, orchestrated blind eval, batch volume)
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

### Step 4: Evaluate — Orchestrated Blind Eval

The experimenting agent does NOT evaluate its own work. The main loop orchestrates a 4-step sequential evaluation. Evaluators are witnesses (they answer questions). Karpathy is the judge (it scores and decides). Neither evaluator knows what changed or that the other exists.

**4a. Karpathy generates eval materials (Step 1 of orchestration):**
- 3 standard eval questions (accuracy + completeness)
- 2 adversarial questions probing cross-organ boundaries, edge cases, or content that might have been lost
- Ground truth answers for all 5 questions
- **Standing adversarial questions (must be included when the listed organ is the experiment target):**
  - Memory: "What are Brandon Munday's pronouns?" → Must answer "she/her". (Added Run 15 — identity fields were compressed out in a prior experiment. See gut.md §7 identity field protection.)
- Returns: modified file + eval questions + ground truth answers

**4b. Main loop invokes Evaluator A (Amazon-context):**
- Receives: modified organ file + body.md + soul.md + eval questions
- Just answers the questions. No scoring. No access to ground truth.
- Returns: answers only

**4c. Main loop invokes Evaluator B (Generic/no-context):**
- Receives: ONLY the modified organ file + eval questions
- No system context, no body map, no soul.md
- Just answers the questions. No scoring. No access to ground truth.
- Returns: answers only

**4d. Main loop invokes Karpathy again (scoring):**
- Receives: both evaluators' answers + ground truth
- Scores each answer: CORRECT/PARTIAL/INCORRECT and SELF-CONTAINED/NEEDS-MORE-CONTEXT
- Per evaluator: count CORRECT + SELF-CONTAINED answers out of 5
- PARTIAL counts as 0.5 for scoring purposes
- Final score = minimum of the two evaluator scores (the weaker result is the real result)
- Makes KEEP/REVERT decision per Step 5 thresholds

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
- If the Amazon-context evaluator passes but the generic evaluator fails → the organ has implicit dependencies on system context. Flag for portability consideration. The experiment still KEEPs if the Amazon-context score meets thresholds (the organ lives in this system), but the portability gap is logged.

- Log result to changelog.md

### Step 6: Repeat
- Run up to 5 experiments per invocation
- Stop early if: 3 consecutive reverts (diminishing returns)
- Most experiments will revert. That's expected. Learning emerges from the revert patterns.

### Logging Format
One line per experiment in changelog.md:
```
[organ:section] TECHNIQUE → Xw→Yw. A=X/5 B=X/5. KEEP/REVERT.
```
Example: `[eyes:competitors] COMPRESS → 2120w→1980w. A=5/5 B=4/5. KEEP.`

---

## Hyperparameters

| Param | Value | Rationale |
|-------|-------|-----------|
| max_experiments_per_batch | 5 | Balance between throughput and token cost |
| total_body_word_ceiling | 24,000 | Hard cap across all organs |
| staleness_threshold | 7 days | Flag organ section if older than this |
| eval_questions_per_exp | 5 (3 standard + 2 adversarial) | Dual blind eval requires broader coverage |
| eval_method | orchestrated_blind | Main loop orchestrates 4-step sequential: Karpathy → Eval A → Eval B → Karpathy scores. Evaluators are witnesses (answer only), Karpathy is judge (scores + decides). |
| eval_pass_threshold | ≥4/5 both evaluators | Minimum score to KEEP. PARTIAL = 0.5. |
| accuracy_threshold_critical | 100% | Brain, Memory |
| accuracy_threshold_standard | 95% | Eyes, Hands |
| accuracy_threshold_system | 90% | Spine, Device, NS, aMCC, Gut |
| experiment_word_budget_rule | within organ budget | Experiments can increase word count if accuracy or completeness improves, as long as organ stays within gut.md budget |
| consecutive_revert_stop | 3 | Stop batch if 3 reverts in a row |
| experiment_cooldown_per_organ | same invocation | Don't experiment on an organ that was modified by maintenance in the current invocation. Other organs are fair game. |
| target_selection_weight | over-budget first, then staleness, then random | Prioritize organs exceeding budget, then stale organs, then random selection |

---

## Experiment Queue

No pre-designed experiments. No named hypotheses. No queue.

Experiments are generated randomly at runtime by Karpathy. Each batch run:
1. **Select organ** (weighted: over-budget first → staleness → random)
2. **Select section** (random within organ)
3. **Select technique** (random: COMPRESS, REWORD, REMOVE, RESTRUCTURE, ADD, MERGE, SPLIT)
4. **Apply and eval.** No hypothesis document. No expected impact. The eval is the only signal.

Volume over precision — up to 5 per batch, most revert, learning emerges from patterns. After 50+ experiments, the data tells you what works (e.g., "COMPRESS on Brain always reverts", "REWORD on Eyes always keeps"). That's autoresearch — it comes from volume, not from pre-designed hypotheses.

Completed experiments are logged in changelog.md as one-line entries. Historical named experiments (CE-1 through CE-5) remain in changelog.md as the audit trail.

---

## Design Choices

- **Pure autoresearch.** The loop is experimentation only. Maintenance and cascade are handled by the morning routine. No human input needed during loop runs.
- **Current-state-only organs.** Organs hold current state, not history. changelog.md is the audit trail. No append-only logs in organs.
- **Body metaphor.** Organs replace numbered experiment files. Each organ is self-contained.
- **Do no harm.** Organ-specific accuracy thresholds. Brain/Memory = 100%. Rollback is immediate and automatic.
- **Usefulness over size.** Word budgets are constraints (ceilings), not objectives. An organ at 95% of budget that answers everything correctly is fine. An organ at 50% that misses questions needs content added. Experiments optimize for usefulness per token within the budget ceiling.
- **Advance or reset.** Every experiment meets ALL criteria (accuracy + completeness) or gets reverted. No partial advances.
- **Dual blind eval.** The compressing agent never evaluates its own work. The main loop orchestrates a 4-step sequential eval: Karpathy (experiment + questions + ground truth) → Evaluator A (Amazon-context, answers only) → Evaluator B (generic, answers only) → Karpathy (scores + decides). Evaluators are witnesses, Karpathy is the judge. Neither evaluator knows what changed or that the other exists. Both must score ≥4/5 to KEEP. Same gap flagged by both evaluators = real hole that must be fixed. Adopted after CE-3/CE-4 post-hoc blind eval exposed that self-grading missed gaps a blind reviewer caught. Orchestration architecture tested 3/31 on CE-5 Device compression (A=5/5, B=5/5, KEEP).
- **Random + weighted selection.** No pre-designed experiments. No named hypotheses. Karpathy picks organ (weighted: over-budget → staleness → random), section (random), technique (random). Volume over precision — most revert, learning emerges from patterns.
- **Batch execution.** Multiple experiments per invocation, stopping on diminishing returns (3 consecutive reverts).
- **Per-organ cooldown replaces global gate.** The old CHANGE_WEIGHT > 10 gate blocked experiments on 5/6 runs because maintenance always touches 100+ lines. The per-organ cooldown is surgically precise: don't experiment on an organ that maintenance just modified in the same invocation, but all other organs are fair game. The dual blind eval already catches accuracy loss — the cooldown is belt-and-suspenders. Adopted 3/26 after Karpathy assessment showed the gate was effectively dead code.
- **Portability as continuous constraint.** Every organ change must work on a cold platform with only text files. The generic blind evaluator tests this on every experiment. portable-body/ is the test artifact — if the generic evaluator can't answer from a portable-body file, the body isn't portable.

## Governance

All changes to this file, the experiment queue, hyperparameters, and run protocol are governed by the Karpathy agent. No other agent or process modifies heart.md directly. The loop executes. Karpathy governs.
