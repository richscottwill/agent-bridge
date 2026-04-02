# Heart — Autoresearch Loop

*Pure experimentation engine. Inspired by [autoresearch](https://github.com/karpathy/autoresearch) — 630 lines, 700 experiments, measurable results. Small, fast, autonomous, compounding. No human input needed. Runs overnight, low token usage, high volume.*

Last updated: 2026-04-02 (Karpathy — removed all static caps and thresholds: adaptive eval depth, no experiment count cap, no static score floors, delta-only keep/revert, Bayesian self-termination)
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

**Primary: delta over baseline** — did the experiment make the organ better or worse than it was before? Not "is it above an arbitrary floor?" but "is it better than what we had?"

Four dimensions, measured on every experiment:

| Dimension | What It Measures | How |
|-----------|-----------------|-----|
| Accuracy delta (A vs B) | Did the change improve or degrade correctness? | Agent A (modified) vs Agent B (original) answer same questions. Delta = A - B. Positive = improvement. |
| Portability (C) | Does the organ work without system context? | Agent C (modified organ, zero context) answers same questions. Baseline check — not compared to A or B. |
| Efficiency | Was the experiment worth the tokens it cost? | yield = (abs(word_delta) × max(delta_ab, 0)) / estimated_tokens. Low yield = deprioritize that organ×technique combo. |
| Latency | Did the experiment spin or stall? | Wall-clock seconds from start to decision. Experiments exceeding 120s are flagged LOW_EFFICIENCY. |

**No static accuracy thresholds.** Thresholds are learned via Bayesian updating (see DuckDB Integration below). Each organ×technique combination has a Beta distribution prior that updates with every experiment outcome. The posterior mean IS the threshold — organs that consistently revert get naturally tighter, organs that consistently keep get naturally looser.

**Safety floor (non-negotiable):** Brain and Memory experiments require delta_ab ≥ 0 (no degradation allowed, ever). This is the only static rule. Everything else is learned.

**Secondary:** staleness (<20% stale facts), word count vs budget (budget is a constraint, not an objective).

---

## Run Protocol — Pure Autoresearch

When invoked (overnight, on-demand, or scheduled), the loop runs N experiments autonomously. No maintenance. No cascade. No suggestions. No human input.

### Step 1: Select Target
Karpathy selects using a two-stage process:

**Stage 1 — Organ selection** (priority order):
1. Over-budget organs (must compress before anything else)
2. Organs with stale sections (>7 days since last update)
3. UCB-weighted random: query `autoresearch_selection_weights` view, sample proportional to UCB score (balances exploitation of known-good combos with exploration of untested ones)

**Stage 2 — Technique selection:**
- Query `autoresearch_priors` for the selected organ
- Sample technique proportional to UCB score (posterior_mean + posterior_std)
- High UCB = either proven effective (high mean) or unexplored (high uncertainty) — both worth trying

**Exclusions:**
- Organs modified by maintenance in the current invocation (per-organ cooldown)
- Organ×technique combos with posterior_mean < 0.15 AND n_experiments > 10 (proven losers — stop wasting tokens)

**Section selection:** Random within the organ.

### Step 2: Snapshot
- Record word count of target organ
- Generate eval questions about the target section's content. Question count scales with experiment risk:
  - Low risk (REWORD, small COMPRESS on non-critical organs): 2-3 questions
  - Medium risk (RESTRUCTURE, REMOVE, larger changes): 4-6 questions
  - High risk (Brain, Memory, any technique): 5-8 questions, include cross-organ boundary probes
  - Standing adversarial questions are ALWAYS included when their organ is the target (see Step 4)
  - No fixed count. Karpathy judges what coverage the experiment needs.
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

### Step 4: Evaluate — A/B/C Blind Eval

Three agents evaluate independently. None knows the others exist. None knows what changed. The main loop orchestrates.

**Agent A (treatment + context):** Receives the MODIFIED organ + body.md + soul.md + eval questions. Answers only. No scoring.

**Agent B (control + context):** Receives the ORIGINAL organ (pre-experiment snapshot) + body.md + soul.md + same eval questions. Answers only. No scoring. Does not know a change was made.

**Agent C (treatment + zero context):** Receives ONLY the MODIFIED organ + eval questions. No body.md, no soul.md, no system context. Answers only. No scoring.

**Karpathy (judge):** Receives all three agents' answers + ground truth. Scores each answer: CORRECT / PARTIAL / INCORRECT. Computes:
- score_a, score_b, score_c (each 0.0 to 1.0, where CORRECT=1, PARTIAL=0.5, INCORRECT=0)
- delta_ab = score_a - score_b (the real signal: did the change help or hurt?)
- Agent C score = portability baseline

**Eval tier determines which agents run:**

| Tier | When | Agents | Cost |
|------|------|--------|------|
| Tier 1 (quick) | Low-risk experiments where the prior suggests high keep rate and the change is small | A + B only (skip C) | ~3 calls |
| Tier 2 (full) | Brain/Memory always. Any experiment where Karpathy judges the risk warrants portability testing. | A + B + C | ~4 calls |

Tier selected BEFORE the experiment runs. If in doubt, Tier 2. Brain and Memory always Tier 2. Tier assignment is a judgment call, not a formula — Karpathy considers organ criticality, technique invasiveness, word delta, and prior history.

**Eval question generation:**
- Karpathy generates questions scaled to experiment risk (see Step 2). No fixed count.
- Ground truth answers for all questions
- **Standing adversarial questions (must be included when the listed organ is the experiment target):**
  - Memory: "What are Brandon Munday's pronouns?" → Must answer "she/her". (Identity field protection — gut.md §7.)
  - These are mandatory inclusions on top of whatever question count Karpathy selects.

### Step 5: Keep or Revert

The decision is based on delta (did it improve?), not absolute score (is it above a floor?).

**KEEP if ALL of the following:**
- delta_ab ≥ 0 (the change did not make the organ worse than it was)
- No INCORRECT on a standing adversarial question (identity protection, etc.)
- Wall-clock time < 120s (if exceeded, flag LOW_EFFICIENCY but still KEEP if other criteria pass)

**REVERT if ANY of the following:**
- delta_ab < 0 (the change made things worse — the only signal that matters)
- Brain/Memory: delta_ab < 0 OR any INCORRECT on any question (zero tolerance)
- Both A and B flag the same question as INCORRECT (signals a pre-existing hole — log it, but still revert the experiment)

**After decision, update DuckDB:**
```sql
-- Log the experiment
INSERT INTO autoresearch_experiments (run_id, organ, section, technique, eval_tier,
  words_before, words_after, word_delta, score_a, score_b, score_c, delta_ab,
  wall_clock_seconds, agent_calls, estimated_tokens, yield_score, decision, revert_reason)
VALUES (...);

-- Update Bayesian prior
UPDATE autoresearch_priors 
SET alpha = alpha + CASE WHEN decision = 'KEEP' THEN 1 ELSE 0 END,
    beta = beta + CASE WHEN decision = 'REVERT' THEN 1 ELSE 0 END,
    n_experiments = n_experiments + 1,
    n_keeps = n_keeps + CASE WHEN decision = 'KEEP' THEN 1 ELSE 0 END,
    n_reverts = n_reverts + CASE WHEN decision = 'REVERT' THEN 1 ELSE 0 END,
    last_updated = CURRENT_TIMESTAMP
WHERE organ = ? AND technique = ?;
```

**Portability signal:**
- If score_a is high but score_c is low → the organ has implicit dependencies on system context. Flag for portability review. The experiment still KEEPs if delta_ab ≥ 0 (the organ lives in this system), but the gap is logged.

- Log one-line result to changelog.md

### Step 6: Repeat
- No cap on experiments. Run until eligible targets are exhausted (all organs on cooldown or excluded by proven-loser filter).
- Most experiments will revert. That's expected. Volume is the point — learning emerges from the revert patterns, not from individual experiment design.
- The Bayesian priors ARE the stopping mechanism. As organ×technique combos accumulate reverts, their UCB scores drop and they stop being selected. The loop self-terminates when nothing worth trying remains.

### Logging Format
One line per experiment in changelog.md:
```
[organ:section] TECHNIQUE → Xw→Yw. A=X B=X C=X Δ=±X. Xs. KEEP/REVERT.
```
Example: `[eyes:competitors] COMPRESS → 2120w→1980w. A=0.9 B=0.8 C=0.7 Δ=+0.1. 45s. KEEP.`
Full data logged to DuckDB `autoresearch_experiments` table.

---

## Hyperparameters

| Param | Value | Rationale |
|-------|-------|-----------|
| max_experiments_per_batch | none | No cap. Loop runs until eligible targets exhausted. Bayesian priors self-terminate by deprioritizing proven losers. |
| total_body_word_ceiling | 24,000 | Hard cap across all organs |
| staleness_threshold | 7 days | Flag organ section if older than this |
| eval_questions_per_exp | adaptive (scales with risk) | Low risk: 2-3. Medium: 4-6. High (Brain/Memory): 5-8. Standing adversarial questions always included. |
| eval_method | A/B/C blind | A=modified+context, B=original+context (control), C=modified+zero context (portability). Karpathy judges. |
| keep_rule | delta_ab ≥ 0 | Change must not degrade. The delta is the only signal. |
| brain_memory_rule | delta_ab ≥ 0, zero INCORRECT | Non-negotiable safety floor for critical organs |
| latency_flag | 120s | Experiments exceeding this are flagged LOW_EFFICIENCY |
| prior_distribution | Beta(α, β), initialized Beta(1,1) | Bayesian updating: KEEP → α+1, REVERT → β+1. Posterior mean = α/(α+β). |
| target_selection | UCB (posterior_mean + posterior_std) | Upper confidence bound balances exploitation (high mean) with exploration (high uncertainty) |
| experiment_word_budget_rule | within organ budget | Experiments can increase word count if accuracy improves, within gut.md budget |
| experiment_cooldown_per_organ | same invocation | Don't experiment on an organ modified by maintenance in the current invocation |
| yield_metric | (abs(word_delta) × max(delta_ab, 0)) / estimated_tokens | Higher = more efficient. Low-yield combos get deprioritized via prior. |

---

## Experiment Queue

No pre-designed experiments. No named hypotheses. No queue.

Experiments are generated randomly at runtime by Karpathy. Each batch run:
1. **Select organ** (weighted: over-budget first → staleness → random)
2. **Select section** (random within organ)
3. **Select technique** (random: COMPRESS, REWORD, REMOVE, RESTRUCTURE, ADD, MERGE, SPLIT)
4. **Apply and eval.** No hypothesis document. No expected impact. The eval is the only signal.

Volume over precision — no caps, most revert, learning emerges from patterns. After 50+ experiments, the data tells you what works (e.g., "COMPRESS on Brain always reverts", "REWORD on Eyes always keeps"). That's autoresearch — it comes from volume, not from pre-designed hypotheses.

Completed experiments are logged in changelog.md as one-line entries. Historical named experiments (CE-1 through CE-5) remain in changelog.md as the audit trail.

---

## Design Choices

- **Pure autoresearch.** The loop is experimentation only. Maintenance and cascade are handled by the morning routine. No human input needed during loop runs.
- **Current-state-only organs.** Organs hold current state, not history. changelog.md is the audit trail. No append-only logs in organs.
- **Body metaphor.** Organs replace numbered experiment files. Each organ is self-contained.
- **Do no harm.** Brain/Memory: zero tolerance for degradation (delta_ab ≥ 0, zero INCORRECT). All other organs: delta_ab ≥ 0. Rollback is immediate and automatic.
- **Usefulness over size.** Word budgets are constraints (ceilings), not objectives. An organ at 95% of budget that answers everything correctly is fine. An organ at 50% that misses questions needs content added. Experiments optimize for usefulness per token within the budget ceiling.
- **Advance or reset.** Every experiment meets ALL criteria (accuracy + completeness) or gets reverted. No partial advances.
- **Dual blind eval.** Three-agent A/B/C design eliminates bias. Agent A evaluates the modified organ with full context. Agent B evaluates the ORIGINAL organ with full context (the control — doesn't know a change was made). Agent C evaluates the modified organ with zero context (portability). The delta between A and B is the real signal — not whether the organ is "above 90%" but whether the change made it better or worse. Karpathy judges all three. None of the evaluators know the others exist.
- **Random + weighted selection.** No pre-designed experiments. No named hypotheses. Karpathy picks organ (weighted: over-budget → staleness → random), section (random), technique (random). Volume over precision — most revert, learning emerges from patterns.
- **Batch execution.** No cap on experiments per invocation. The loop runs until eligible targets are exhausted — the Bayesian priors self-terminate by deprioritizing proven losers, and per-organ cooldown removes recently-touched organs. This is true to autoresearch: volume over caution, let the data tell you when to stop. Token efficiency comes from tiered eval (Tier 1 for low-risk, Tier 2 for high-risk) and Bayesian target selection (stop trying what doesn't work), not from capping volume.
- **Per-organ cooldown replaces global gate.** The old CHANGE_WEIGHT > 10 gate blocked experiments on 5/6 runs because maintenance always touches 100+ lines. The per-organ cooldown is surgically precise: don't experiment on an organ that maintenance just modified in the same invocation, but all other organs are fair game. The dual blind eval already catches accuracy loss — the cooldown is belt-and-suspenders. Adopted 3/26 after Karpathy assessment showed the gate was effectively dead code.
- **Portability as continuous constraint.** Every organ change must work on a cold platform with only text files. The generic blind evaluator tests this on every experiment. The agent-bridge repo is the test artifact — if the generic evaluator can't answer from a portable-body file, the body isn't portable.

## DuckDB Integration

All experiment data lives in `~/shared/data/duckdb/ps-analytics.duckdb`. The loop reads priors before each experiment and writes results after each decision. Organs hold the protocol (how to experiment). DuckDB holds the data (what happened, what works).

### Tables

| Table | Purpose |
|-------|---------|
| `autoresearch_experiments` | One row per experiment. Full record: organ, technique, scores, delta, cost, decision. |
| `autoresearch_priors` | Bayesian priors per organ×technique. Beta(α,β) updated on every KEEP/REVERT. |
| `autoresearch_organ_health` | Snapshot per organ per run. Word count, utilization, accuracy estimate over time. |

### Views

| View | Purpose |
|------|---------|
| `autoresearch_selection_weights` | UCB scores for target selection. posterior_mean + posterior_std = exploration/exploitation balance. |

### Key Queries

```sql
-- What works? (highest keep rate with enough data)
SELECT organ, technique, alpha/(alpha+beta) AS keep_rate, n_experiments 
FROM autoresearch_priors WHERE n_experiments > 5 ORDER BY keep_rate DESC;

-- What doesn't? (proven losers)
SELECT organ, technique, alpha/(alpha+beta) AS keep_rate, n_experiments 
FROM autoresearch_priors WHERE n_experiments > 10 AND alpha/(alpha+beta) < 0.2;

-- Experiment yield ranking (most efficient experiments)
SELECT organ, technique, word_delta, delta_ab, yield_score, decision
FROM autoresearch_experiments ORDER BY yield_score DESC LIMIT 20;

-- Organ health trend
SELECT organ, run_id, word_count, utilization, accuracy_estimate 
FROM autoresearch_organ_health ORDER BY organ, run_id;
```

### Update Protocol

After every experiment decision:
1. INSERT into `autoresearch_experiments` (full record)
2. UPDATE `autoresearch_priors` (increment α or β)
3. At end of batch: INSERT into `autoresearch_organ_health` (one row per organ with current word counts)

The priors table is the learning mechanism. Over time, posterior_mean converges to the true keep rate for each organ×technique combo. The UCB score ensures unexplored combos get tried (high uncertainty → high UCB) while proven winners get prioritized (high mean → high UCB). Proven losers (low mean, low uncertainty) naturally fall off.

## Governance

All changes to this file, the experiment queue, hyperparameters, and run protocol are governed by the Karpathy agent. No other agent or process modifies heart.md directly. The loop executes. Karpathy governs.
