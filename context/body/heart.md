<!-- DOC-0225 | duck_id: organ-heart -->
# Heart — Autoresearch Loop

*Pure experimentation engine. Inspired by [autoresearch](https://github.com/karpathy/autoresearch) — 630 lines, 700 experiments, measurable results. Small, fast, autonomous, compounding. No human input needed. Runs overnight, low token usage, high volume.*

Last updated: 2026-04-05 (Karpathy Run 35 — Design Choices compressed 7→7 bullets tighter, Common Failures section added)
Created: 2026-03-20

---

## Architecture

The system uses a body metaphor. Each organ is a self-contained file. The loop experiments on these organs autonomously — no maintenance, no cascade, no suggestions. The AM hooks handle morning ingestion and briefing. EOD-2 handles maintenance and cascade. Karpathy handles experimentation within EOD-2.

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

### Target Categories (experiments can target any of these)

| Category | Files | Eval Type | Example Experiment |
|----------|-------|-----------|-------------------|
| Body organs | `~/shared/context/body/*.md` | information_retrieval | COMPRESS eyes competitors section → does accuracy hold? |
| Style guides | `~/.kiro/steering/richard-style-*.md` | output_quality | REWORD the email drafting checklist → does the next Lena email score higher? |
| Market context | `~/shared/wiki/callouts/*-context.md` | output_quality | ADD a narrative thread to AU context → does the AU callout draft improve? |
| Callout principles | `~/.kiro/steering/callout-principles.md` | output_quality | REMOVE a principle → does callout quality degrade? |
| Hook prompts | `~/.kiro/hooks/*.kiro.hook` | output_quality | REWORD the AM-2 triage prompt → does task prioritization improve? |

Organs use information-retrieval evals (can the agent answer factual questions?). Style guides, context files, and hook prompts use output-quality evals (does the agent produce better work products?). The same 7 techniques (COMPRESS, ADD, RESTRUCTURE, REMOVE, REWORD, MERGE, SPLIT) apply to all target categories. The same A/B/C blind eval design applies to both eval types — only the eval questions change.

### Directory Map

| Directory | Role |
|-----------|------|
| `~/shared/context/body/` | Body organs + device |
| `~/shared/context/active/` | Ground truth (current.md, org-chart.md, rw-tracker.md) |
| `~/shared/context/intake/` | Inbox for new material |
| `~/shared/tools/` | Utility scripts |
| `~/shared/wiki/archive/` | Cold storage |
| `~/shared/wiki/research/` | Standalone research, data files |
| `~/.kiro/steering/` | Agent behavior config (soul.md, rw-trainer.md) |

---

## The Metric

**Primary: delta over baseline** — did the experiment make the output better or worse than it was before? Not "is it above an arbitrary floor?" but "is it better than what we had?"

### Experiment Signals

Every experiment produces multiple signals. None are inherently good or bad — more words could mean richer content, higher latency could mean deeper reasoning. We track them all as covariates and use Bayesian updating to learn which signal patterns correlate with output quality over time.

| Signal | What It Captures | How It's Measured | Interpretation |
|--------|-----------------|-------------------|----------------|
| Accuracy delta (A vs B) | Did the change improve or degrade correctness/quality? | Agent A (modified) vs Agent B (original) answer same questions or produce same work product. Delta = A - B. | Primary keep/revert signal. Positive = improvement. |
| Portability (C) | Does the content work without system context? | Agent C (modified, zero context) answers same questions. | Gap between A and C reveals implicit dependencies. |
| Word delta | How did content size change? | words_after - words_before. | Not a goal — a covariate. Compression that loses info reverts. Expansion that adds value keeps. |
| Latency | How long did the experiment take? | Wall-clock seconds from start to decision. | Not a penalty — a signal. High latency may indicate complex reasoning or spinning. Track baseline per target×technique. |
| Eval question difficulty | How hard were the eval questions? | Count + specificity of questions (IDs, dates, formulas vs general concepts). | Harder questions produce more informative deltas. Easy questions mask real degradation. |
| Context size | How much context did the eval agents receive? | Word count of eval prompt (target + body.md + soul.md vs target only). | Larger context may compensate for content gaps. Vary to test robustness. |

**No static thresholds for any signal.** All thresholds are learned via Bayesian updating. Each target×technique combination has a Beta distribution prior that updates with every experiment outcome. The posterior mean IS the threshold — targets that consistently revert get naturally tighter, targets that consistently keep get naturally looser.

**Safety floor (non-negotiable):** Brain and Memory experiments require delta_ab ≥ 0 (no degradation allowed, ever). This is the only static rule. Everything else is learned.

---

## Run Protocol — Pure Autoresearch

When invoked (overnight, on-demand, or scheduled), the loop runs N experiments autonomously. No maintenance. No cascade. No suggestions. No human input.

### Step 1: Select Target
Karpathy selects using a three-stage process: exclude → select target → select technique.

**Pre-filter (exclusions):**
- Targets modified by maintenance in the current invocation (per-target cooldown)
- Target×technique combos with posterior_mean < 0.15 AND n_experiments > 10 (proven losers — stop wasting tokens)

**Stage 1 — Target selection** (priority order):
1. Targets where aggregate body accuracy is declining while word count is increasing (data-driven compression signal — organs only)
2. Targets where COMPRESS prior is strong (posterior_mean > 0.7, n > 5) — known room to shrink
3. Targets with stale sections (>7 days since last update)
4. UCB-weighted random: query `autoresearch_selection_weights` view, sample proportional to UCB score (balances exploitation of known-good combos with exploration of untested ones)

**Stage 2 — Technique selection:**
- Query `autoresearch_priors` for the selected target
- Sample technique proportional to UCB score (posterior_mean + posterior_std)
- High UCB = either proven effective (high mean) or unexplored (high uncertainty) — both worth trying
- **Selection bias check (from Run 26-27 learnings):** Force at least 30% of experiments onto techniques with <3 prior data points on the target. A healthy batch has ≤50% keep rate. Reverts are the learning signal.

**Section selection:** Randomized. Number the sections in the target file, use shuf to pick one. Do not pick "the section that looks compressible" — that's selection bias. The experiment discovers what's compressible; the agent's intuition doesn't.

### Step 2: Snapshot
- Record word count of target organ
- **Generate eval questions BEFORE applying the experiment.** Questions must be written while looking at the original content, not after seeing the result. This prevents unconscious question-easing.
- Question count: 5 minimum for all experiments. Randomize difficulty by including a mix from all three levels:
  - **Easy (1-2):** General concept questions answerable from section headers or topic sentences
  - **Medium (1-2):** Specific facts requiring reading the section (names, dates, percentages)
  - **Hard (1-2):** Precise details that compression is most likely to lose (IDs, formulas, multi-part facts like "CVR from X to Y", cross-references to other sections)
  Use shuf to pick the difficulty mix. The difficulty distribution is itself a signal — track it in the experiment log.
- Standing adversarial questions are ALWAYS included when their organ is the target (see Step 4)
  - No fixed count. Karpathy judges what coverage the experiment needs.
- Save snapshot for rollback

### Step 3: Apply Experiment
- Apply the selected technique to the selected section. **Apply boldly.** The eval is the safety net, not your judgment about whether the change will work. A timid edit that barely changes anything produces delta_ab = 0.0 and teaches nothing. A bold edit that breaks something produces a revert and teaches what's load-bearing. Prefer bold.
- Experiment types (not limited to compression):
  - **COMPRESS**: resolve completed items, deduplicate, age-decay, structural compression (paragraphs→tables), protocol compression
  - **ADD**: inline a key fact that eliminates a tool call. Portable pattern: "Common Failures" sections.
  - **RESTRUCTURE**: reorder so the most-queried data is found faster.
  - **REMOVE**: delete content that's accurate but never queried. See Validated Patterns for cautions.
  - **REWORD**: same info, fewer tokens, less ambiguity.
  - **MERGE**: combine sections that always get read together. See Validated Patterns for cautions.
  - **SPLIT**: separate sections that serve different query patterns.

### Step 4: Evaluate — A/B/C Blind Eval

Karpathy orchestrates the blind eval by invoking eval agents via CLI (`.json` agent configs). Each eval agent runs as an independent CLI agent with its own context — no awareness of the other agents or the experiment. CLI invocation avoids the subagent-can't-invoke-subagent limitation.

**Agent A (treatment + context):** Invoked as CLI agent. Prompt contains: the MODIFIED organ content + body.md + soul.md + eval questions. Instructions: answer each question. No scoring. No awareness of experiment.

**Fast-fail gate (after Agent A, before Agent B):** Karpathy inspects Agent A's answers before invoking Agent B. Score Agent A's answers against ground truth. If 50%+ are INCORRECT, the experiment is obviously broken — skip Agent B, mark as REVERT with reason `fast_fail`, log to DuckDB and experiment-log.tsv, move to next experiment. This saves 1 CLI agent call on clearly bad experiments. Fast-fail does NOT apply to Brain/Memory experiments (always run full eval on critical organs).

**Agent B (control + context):** Invoked as separate CLI agent. Prompt contains: the ORIGINAL organ (pre-experiment snapshot) + body.md + soul.md + same eval questions. Instructions: answer each question. No scoring. Does not know a change was made. Does not know Agent A exists.

**Agent C (treatment + zero context):** Invoked as CLI agent. Prompt contains: ONLY the MODIFIED organ + eval questions. No body.md, no soul.md, no system context. Answers only. Runs on EVERY experiment — portability data is always collected.

**Karpathy (judge):** After all eval agents return, Karpathy scores all answers against ground truth. Writes structured results to `~/shared/context/active/experiment-results-latest.json` (overwritten each experiment — keeps eval output out of main context window):
```json
{
  "experiment_id": "run28_exp3",
  "target": "eyes", "section": "competitors", "technique": "COMPRESS",
  "eval_type": "information_retrieval",
  "score_a": 0.9, "score_b": 0.8, "score_c": null, "delta_ab": 0.1,
  "fast_fail": false, "decision": "KEEP", "wall_clock_seconds": 45,
  "words_before": 2120, "words_after": 1980
}
```
Scoring method depends on eval type:

**Information-retrieval evals** (organs): Score each answer mechanically using fact-counting. For each question:
- Count the distinct facts in the ground truth answer (e.g., "CVR from 0.82% to 2.35% (+187%)" = 3 facts)
- Count how many of those facts appear in the agent's answer
- Score = facts_found / facts_in_ground_truth (e.g., agent says "+187%" = 1/3 = 0.33)
- NOT FOUND = 0.0
This removes judgment from scoring. The ground truth defines what a complete answer looks like; the score measures completeness mechanically.
- delta_ab = score_a - score_b (the real signal: did the change help or hurt?)
- Agent C score = portability baseline

**Output-quality evals** (style guides, context files, hook prompts): Instead of factual questions, the eval prompt is "produce this work product" (e.g., draft an email to Lena, write an AU callout, outline a testing doc). Agent A produces the work product using the modified file + full context. Agent B produces the same work product using the original file + full context. Karpathy scores both against the relevant style guide checklist + Amazon writing norms across 5 dimensions:

| Dimension | What It Measures |
|-----------|-----------------|
| Voice match | Does it sound like Richard? (greeting, register, parenthetical style, sign-off) |
| Structure match | Does it follow the doc type's template? (email structure, callout format, doc outline) |
| Data integration | Are numbers contextualized with "so what"? (not just reported — interpreted) |
| Audience calibration | Is the register right for the recipient? (Tier 1-5 audience matching) |
| Actionability | Does it include clear next steps? (specific asks, dates, owners) |

Each dimension scored 0.0 to 1.0. Final score = average of all 5. delta_ab = score_a - score_b. Same keep/revert rules apply — delta_ab ≥ 0 to KEEP.

For output-quality evals, Karpathy must also load the relevant style guide as context for the eval agents (e.g., richard-style-email.md when testing email drafts, richard-style-wbr.md when testing callout quality).

**Every experiment runs A + B + C.** No tier system. Portability data (Agent C) is collected on every experiment. The cost is ~3 CLI agent calls per experiment — this is the price of real data.

**Eval question generation:**
- Karpathy generates questions scaled to experiment risk (see Step 2). No fixed count.
- Ground truth answers for all questions
- **Standing adversarial questions (must be included when the listed organ is the experiment target):**
  - Memory: "What are Brandon Munday's pronouns?" → Must answer "she/her". (Identity field protection — gut.md §7.)
  - These are mandatory inclusions on top of whatever question count Karpathy selects.

### Step 5: Keep or Revert

The decision is based on delta (did it improve?), not absolute score (is it above a floor?). The goal is output quality, not smaller files. A KEEP that adds 50 words but improves delta_ab by +0.1 is better than a KEEP that removes 100 words with delta_ab = 0.0.

**KEEP if ALL of the following:**
- delta_ab ≥ 0 (the change did not make the organ worse than it was)
- No INCORRECT on a standing adversarial question (identity protection, etc.)
- Wall-clock time is recorded as a signal (not a gate). Track baseline per target×technique — deviations inform future selection.

**REVERT if ANY of the following:**
- delta_ab < 0 (the change made things worse — the only signal that matters)
- Brain/Memory: delta_ab < 0 OR any INCORRECT on any question (zero tolerance)
- Both A and B flag the same question as INCORRECT (signals a pre-existing hole — log it, but still revert the experiment)

**After decision, update DuckDB + experiment-log.tsv:**

Append one row to `~/shared/context/active/experiment-log.tsv` (tab-separated, human-scannable, git-trackable — the "wake up and see what happened" artifact):
```
run_id	target	section	technique	eval_type	words_before	words_after	score_a	score_b	delta_ab	fast_fail	decision	wall_clock_s
run28_exp3	eyes	competitors	COMPRESS	info_retrieval	2120	1980	0.9	0.8	+0.1	false	KEEP	45
```

Then update DuckDB:
```sql
-- Log the experiment
INSERT INTO autoresearch_experiments (run_id, organ, section, technique, eval_type, eval_tier,
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
[target:section] TECHNIQUE (eval_type) → Xw→Yw. A=X B=X C=X Δ=±X. Xs. KEEP/REVERT.
```
Example: `[eyes:competitors] COMPRESS (info_retrieval) → 2120w→1980w. A=0.9 B=0.8 C=0.7 Δ=+0.1. 45s. KEEP.`
Example: `[richard-style-email:checklist] REWORD (output_quality) → 850w→820w. A=0.82 B=0.67 Δ=+0.15. 60s. KEEP.`
Example: `[eyes:competitors] COMPRESS (info_retrieval) → 2120w→2120w. A=0.3 B=- Δ=-. 12s. REVERT (fast_fail).`
Full data logged to DuckDB `autoresearch_experiments` table + `experiment-log.tsv`.

---

## Hyperparameters

| Param | Value |
|-------|-------|
| max_experiments_per_batch | none (Bayesian priors self-terminate) |
| total_body_ceiling | adaptive (plateaus in `autoresearch_organ_health`) |
| organ_budgets | adaptive (baselines in gut.md, learned from priors) |
| staleness_threshold | 7 days |
| eval_questions_per_exp | adaptive: low 2-3, medium 4-6, high 5-8 + standing adversarial |
| eval_method | A/B/C blind (A=modified+context, B=original+context, C=modified+zero context) |
| keep_rule | delta_ab ≥ 0 |
| brain_memory_rule | delta_ab ≥ 0, zero INCORRECT |
| latency_signal | recorded per experiment | Not a gate — a covariate. Track baseline per target×technique. |
| prior_distribution | Beta(α, β), initialized Beta(1,1) |
| target_selection | UCB (posterior_mean + posterior_std) |
| experiment_word_budget_rule | adaptive (gut.md) |
| experiment_cooldown_per_organ | same invocation |
| yield_metric | (abs(word_delta) × max(delta_ab, 0)) / estimated_tokens |

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

- **Pure autoresearch, batch, random.** Experimentation only. Karpathy picks target→section→technique (weighted: over-budget→staleness→random). Volume over precision. Bayesian priors self-terminate proven losers.
- **Current-state organs.** Organs hold current state, not history. changelog.md = audit trail. Each organ self-contained.
- **Do no harm.** Brain/Memory: delta_ab ≥ 0, zero INCORRECT. All others: delta_ab ≥ 0. Rollback immediate.
- **Usefulness over size.** Adaptive budgets (gut.md baselines, learned ceilings). ADD/COMPRESS priors discover natural size. Body ceiling = accuracy plateau in `autoresearch_organ_health`.
- **Dual blind eval.** A=modified+context, B=original+context, C=modified+zero context. Delta A-B is the signal. Karpathy judges. Evaluators unaware of each other.
- **Per-organ cooldown.** No experimenting on organs modified by maintenance this invocation. All others fair game.
- **Output quality + portability.** Style guides, context files, hook prompts are valid targets. A/B/C works for both eval types (Run 18). Every change must work on cold platform — agent-bridge is the test artifact.

### Validated Patterns (from 58 experiments, Runs 19-27)

These patterns emerged from data. They should inform technique selection but not override the Bayesian priors — the priors will converge to the same conclusions over time.

| Pattern | Evidence | Implication |
|---------|----------|-------------|
| REWORD is the dominant technique | ~90% keep rate across both eval types, 15+ experiments | Default to REWORD when uncertain. Concrete examples > abstract rules. |
| REMOVE on unique content always reverts | 7/7 reverted (IDs, URLs, rules, formulas, behavioral constraints) | Pre-check uniqueness before REMOVE. If content exists nowhere else, don't remove it. |
| REMOVE on motivational prose keeps | 2/2 kept (design philosophy, guiding principles) | Rubrics and protocols work without framing prose. Safe to compress. |
| MERGE on distinct registers always reverts | 3/3 reverted (guide/playbook, stakeholder/analytical) | Registers are real semantic boundaries. Don't merge categories that serve different query patterns. |
| SPLIT on structural organization always keeps | 4/4 kept (subsection headers, human/agent split) | Reorganization preserves content. Safe technique. |
| SPLIT labeling content "optional" reverts when it isn't | 1/1 reverted (WBR YoY context) | Check actual usage before labeling anything optional. |
| COMPRESS on explicit handoff steps reverts | 1/1 reverted (wiki-editor pipeline) | Pipeline integrity depends on checkpoint granularity. |
| Common Failures pattern is portable | 4/4 kept across email→wbr→mbr→librarian | Proven structural pattern for any style guide or agent file. |
| Concrete examples > abstract rules | +0.04 to +0.08 delta consistently | When adding a rule, always include a worked example. |
| Empty structural tables are load-bearing | 1/1 reverted (amcc avoidance ratio) | Tables define measurement frameworks even without data. |
| UCB-only selection produces 90%+ keep rate (selection bias) | Runs 19-25: 92% keep rate | Force 30% exploration of untested combos. Healthy batch ≤50% keep rate. Most experiments should revert. |

## DuckDB Integration

All experiment data lives in `~/shared/data/duckdb/ps-analytics.duckdb`. Organs hold protocol (how to experiment). DuckDB holds data (what happened, what works).

### Update Protocol

After every experiment decision:
1. INSERT into `autoresearch_experiments` (full record)
2. UPDATE `autoresearch_priors` (increment α or β)
3. At end of batch: INSERT into `autoresearch_organ_health` (one row per organ with current word counts)

Posterior_mean converges to the true keep rate per target×technique. UCB score = posterior_mean + posterior_std — unexplored combos get tried (high uncertainty), proven winners get prioritized (high mean), proven losers naturally fall off.

**Seeding new targets:** New target category → new rows in `autoresearch_priors` for every target × technique combo, initialized Beta(1,1). `eval_type` column distinguishes `information_retrieval` (organs) from `output_quality` (style guides / context files / hooks). Both flow through the same Bayesian updating.

### Tables

| Table | Purpose |
|-------|---------|
| `autoresearch_experiments` | One row per experiment. Full record: organ, technique, scores, delta, cost, decision. Includes `eval_type` column: `information_retrieval` (organ experiments) or `output_quality` (style guide / context file experiments). |
| `autoresearch_priors` | Bayesian priors per target×technique. Beta(α,β) updated on every KEEP/REVERT. Includes rows for style guide × technique combos, market context × technique combos, etc. — not just organs. |
| `autoresearch_organ_health` | Snapshot per target per run. Word count, utilization, accuracy estimate over time. |

### Views

| View | Purpose |
|------|---------|
| `autoresearch_selection_weights` | UCB scores for target selection. posterior_mean + posterior_std = exploration/exploitation balance. |

## Common Failures in Using This Organ

1. **Skipping Agent B on "obvious" improvements.** Every experiment needs the control. A change that looks good in isolation may score lower than the original. The delta is the signal, not the absolute score.
2. **Scoring PARTIAL as CORRECT.** Detail-loss matters. If Agent A says "+187%" but Agent B says "CVR from 0.82% to 2.35%", A is PARTIAL — the supporting detail was lost. This is how compression damage gets detected.
3. **Running REMOVE without uniqueness pre-check.** 7/7 reverted. If the content exists nowhere else in the body, REMOVE will fail. Always check before attempting.
4. **Treating delta_ab = 0.0 as "nothing happened."** A KEEP at Δ=0.0 with -150 words is a compression win. A KEEP at Δ=0.0 with +50 words is neutral. The word delta is a covariate, not the goal.

## Governance

All changes to this file, the experiment queue, hyperparameters, and run protocol are governed by Karpathy authority (see `~/.kiro/agents/body-system/karpathy.md`). "Karpathy authority" means: the Karpathy CLI agent (`karpathy.json`) running experiment batches, or any agent acting under karpathy.md identity during governance proposals. Karpathy runs as a CLI agent (not a subagent) so it can invoke eval agents A/B/C as independent CLI agents. No agent operating outside Karpathy authority modifies heart.md. The loop executes. Karpathy governs.
