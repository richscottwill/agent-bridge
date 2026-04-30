<!-- DOC-0225 | duck_id: organ-heart -->






# Heart — Autoresearch Loop *Pure experimentation engine. Inspired by [autoresearch](https://github.com/karpathy/autoresearch) — 630 lines, 700 experiments, measurable results. Small, fast, autonomous, compounding. No human input needed. Runs overnight, low token usage, high volume.* Last updated: 2026-04-05 (Karpathy Run 35 — Design Choices compressed 7→7 bullets tighter, Common Failures section added) Created: 2026-03-20 --- ## Architecture & Measurement

Body metaphor. Each organ = self-contained file. Loop experiments autonomously. See `body.md` (organ map), `spine.md` (directory layout).

**Eval agent constraint:** Inline eval prompts must stay under ~3KB for reliable agent behavior. For larger targets, excerpt only the sections being tested. Questions must be specific enough to distinguish from auto-loaded steering context.
  - *Example:* When eval agent constraint:** inline eval prompts must , the expected outcome is verified by checking the result.







### Target Categories

| Category | Files | Eval Type | Example |
|----------|-------|-----------|---------|
| Body organs | `~/shared/context/body/*.md` | information_retrieval | COMPRESS eyes → accuracy holds? |
| Style guides | `~/.kiro/steering/richard-style-*.md` | output_quality | REWORD email checklist → better drafts? |
| Market context | `~/shared/wiki/callouts/*-context.md` | output_quality | ADD narrative to AU → callout improves? |
| Callout principles | `~/.kiro/steering/callout-principles.md` | output_quality | REMOVE principle → quality degrades? |
| Hook prompts | `~/.kiro/hooks/*.kiro.hook` | output_quality | REWORD AM-2 → better prioritization? |

Organs: information-retrieval evals. Style guides/context/hooks: output-quality evals. Same 7 techniques (COMPRESS, ADD, RESTRUCTURE, REMOVE, REWORD, MERGE, SPLIT) and A/B/C blind eval design apply to all.





#### Part 2







### The Metric

**Primary: delta over baseline** — did the experiment make the output better or worse than it was before? Not "is it above an arbitrary floor?" but "is it better than what we had?"







### Experiment Signals

Six signals tracked per experiment as covariates (none inherently good/bad):

| Signal | Measured | Interpretation |
|--------|----------|----------------|
| Accuracy delta (A vs B) | Agent A (modified) vs Agent B (original) on same questions. Delta = A - B. | Primary keep/revert signal. |
| Portability (C) | Agent C (modified, zero context) on same questions. | A-C gap reveals implicit dependencies. |
| Word delta | words_after - words_before. | Covariate, not goal. |
| Latency | Wall-clock seconds. | Track baseline per target×technique. |
| Eval question difficulty | Count + specificity (IDs/dates/formulas vs concepts). | Harder questions = more informative deltas. |
| Context size | Word count of eval prompt. | Larger context may compensate for gaps. |

**No static thresholds for any signal.** All thresholds are learned via Bayesian updating. Each target×technique combination has a Beta distribution prior that updates with every experiment outcome. The posterior mean IS the threshold — targets that consistently revert get naturally tighter, targets that consistently keep get naturally looser.

**Safety floor (non-negotiable):** Brain and Memory experiments require delta_ab ≥ 0 (no degradation allowed, ever). This is the only static rule. Everything else is learned.

---







## Run Protocol — Pure Autoresearch

When invoked (overnight, on-demand, or scheduled), the loop runs N experiments autonomously. No maintenance. No cascade. No suggestions. No human input.







[38;5;10m> [0m### Step 1: Select Target[0m[0m
Karpathy uses a three-stage process: exclude → select target → select technique.[0m[0m
[0m[0m
**Pre-filter:**[0m[0m
- Targets modified by maintenance this invocation[0m[0m
- Target×technique combos with posterior_mean < 0.15 AND n_experiments > 10 (proven losers)[0m[0m
[0m[0m
**Stage 1 — Target selection:**[0m[0m
1. Targets where aggregate body accuracy is declining while word count increases (data-driven compression signal — organs only)[0m[0m
2. Targets with strong COMPRESS prior — known room to shrink[0m[0m
3. Targets with stale sections[0m[0m
4. UCB-weighted random: sample from `autoresearch_selection_weights` proportional to UCB score (balances exploitation with exploration)[0m[0m
[0m[0m
**Stage 2 — Technique selection:**[0m[0m
- Query `autoresearch_priors` for the selected target, sample technique proportional to UCB score (high UCB = proven effective or unexplored)[0m[0m
- **Selection bias check:** Force ≥30% of experiments onto techniques with <3 prior data points on the target. Healthy batch: ≤50% keep rate. Reverts are the learning signal.[0m[0m
[0m[0m
**Section selection:** Randomized via shuf on numbered sections. Do not pick "the section that looks compressible" — that's selection bias. The experiment discovers what's compressible.[0m[0m
[0m[0m
**Worked example:** Pre-filter: hands.md on cooldown, brain×REMOVE at posterior_mean=0.12 (n=12). Stage 1: no declining-accuracy+rising-wordcount organs. Stage 2: no COMPRESS priors >0.7 with n>5. Stage 3: gut.md last updated 9 days ago → selected gut. Technique: REWORD has UCB=0.99, but 30% exploration rule fires — shuf picks MERGE. Section: `echo -e "1\n2\n3\n4" | shuf | head -1` → section 3.[0m[0m
[0m[0m
- Record target organ word count[0m[0m
- **Generate eval questions BEFORE applying the experiment** — written from original content to prevent unconscious question-easing[0m[0m
- Question count: 5 minimum. Randomize difficulty mix using shuf:[0m[0m
 - **Easy (1-2):** General concepts from headers/topic sentences[0m[0m
 - **Medium (1-2):** Specific facts requiring section reading (names, dates, percentages)[0m[0m
 - **Hard (1-2):** Precise details compression most likely loses (IDs, formulas, multi-part facts, cross-references)[0m[0m
 Track difficulty distribution in the experiment log.[0m[0m
- Standing adversarial questions always included when their organ is the target (see Step 4) — count at Karpathy's judgment based on coverage needs[0m[0m
- Save snapshot for rollback
### Step 3: Apply Experiment
- Apply boldly. The eval is the safety net. Timid edits teach nothing; bold edits that break teach what's load-bearing.

**Structural validity gate (mandatory, runs between Step 3 apply and Step 4 eval).** If the target file has a parseable grammar, the modified content MUST parse before any eval agent runs. Added 2026-04-29 after W18 batch invalidated 13 hook JSONs that scored high on output_quality.

| Target extension | Validity check |
|---|---|
| `.kiro.hook`, `.json` | `python3 -c "import json,sys; json.loads(open(sys.argv[1]).read())" <path>` must return 0 |
| `.py` | `python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" <path>` must return 0 |
| `.sh` | `bash -n <path>` must return 0 |
| `.yml`, `.yaml` | `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <path>` must return 0 |
| `.md`, `.txt`, unknown | no structural gate |

**If validity fails:** auto-REVERT with `revert_reason='structural_invalidity'`. Do NOT invoke Agent A / B / C. Log to `autoresearch_experiments` with eval scores NULL. Restore original file from snapshot. Update priors (REVERT → β+1) same as any other revert.

**Why this is a pre-eval gate, not a scoring dimension:** the eval agents cannot detect invalid JSON/Python/bash — they read prose. A broken hook JSON reads as fine prose to the evaluator (the surrounding field names and values are still there) even though it will fail to load at runtime. Structural validity is binary and cheap to check; spending eval tokens on a file that cannot be loaded is pure waste.




### Step 4: Evaluate — A/B/C Blind Eval

Three independent CLI eval agents, each unaware of the others:

- **Agent A (treatment):** MODIFIED organ + body.md + soul.md + eval questions.
- **Agent B (control):** ORIGINAL organ + body.md + soul.md + same questions.
- **Agent C (portability):** MODIFIED organ ONLY + questions. No body.md, no soul.md.

**Fast-fail gate:** After Agent A, if 50%+ INCORRECT → skip B, mark REVERT (`fast_fail`). Does NOT apply to Brain/Memory.

**Scoring — information-retrieval evals (organs):** Mechanical fact-counting per question. Score = facts_found / facts_total. NOT FOUND = 0.0. delta_ab = score_a - score_b.

**Scoring — output-quality evals (style guides, context, hooks):** Agents produce a work product. Scored across 5 dimensions (voice match, structure match, data integration, audience calibration, actionability), each 0.0-1.0. Final = average. delta_ab = score_a - score_b.

Results written to `~/shared/context/active/experiment-results-latest.json`.

**Standing adversarial questions** (mandatory when target organ is listed):
- Memory: "What are Brandon Munday's pronouns?" → Must answer "she/her".







### Step 5: Keep, Revert & Repeat

Decision based on delta (did it improve?), not absolute score. A KEEP that adds 50 words at Δ=+0.1 beats a KEEP that removes 100 words at Δ=0.0.

**KEEP if ALL:** delta_ab ≥ 0, no INCORRECT on standing adversarial questions. Wall-clock time recorded as signal (not gate).

**REVERT if ANY:** delta_ab < 0. Brain/Memory: delta_ab < 0 OR any INCORRECT. Both A and B flag same question INCORRECT → pre-existing hole, log it, still revert.

**After decision:** Append to experiment-log.tsv + INSERT to DuckDB `autoresearch_experiments` + UPDATE `autoresearch_priors` (KEEP → α+1, REVERT → β+1). Log portability signal if score_a high but score_c low. One-liner to changelog.md.

**Repeat:** No cap on experiments. Run until eligible targets are exhausted. Most experiments will revert — learning emerges from revert patterns. Bayesian priors ARE the stopping mechanism: as combos accumulate reverts, UCB scores drop and they stop being selected. The loop self-terminates when nothing worth trying remains.







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







## Experiment Queue & Hyperparameters
**Yield example:** COMPRESS Eyes 150w, Δ=+0.1, ~8K tokens → yield = 0.001875. High yield = bold change + positive delta + low cost.
**Worked example — selection sequence:** Query priors → amcc×ADD has UCB 0.997 (high mean, proven winner). But 30% exploration rule fires → shuf picks hands×MERGE (n=0, untested). Section: shuf picks "Tool Opportunities." Technique: MERGE. Apply boldly, eval catches mistakes. If REVERT → hands×MERGE gets β+1, UCB drops, less likely next time. If KEEP → α+1, UCB stays high.
**Self-termination:** Bayesian priors are the stopping mechanism. As combos accumulate reverts, UCB scores drop and they stop being selected. Proven losers (posterior_mean < 0.15, n > 10) are excluded entirely. The loop self-terminates when nothing worth trying remains — no manual cap needed.
---

Random at runtime. Each batch: select organ (over-budget → stale → UCB random) → section (random) → technique (COMPRESS/REWORD/REMOVE/RESTRUCTURE/ADD/MERGE/SPLIT) → apply and eval. No hypothesis doc. The eval is the only signal.

Volume over precision — most revert, learning emerges from patterns. Logged in changelog.md + DuckDB.

| Param | Value |
|-------|-------|
| keep_rule | delta_ab ≥ 0 |
| brain_memory_rule | delta_ab ≥ 0, zero INCORRECT |
| eval_method | A/B/C blind: A=modified+context, B=original+context, C=modified only |
| eval_questions | 5+ per experiment, mix of easy/medium/hard + standing adversarial |
| prior_distribution | Beta(α, β), init Beta(1,1) |
| target_selection | UCB = posterior_mean + posterior_std |
| cooldown | per-target, same invocation |
| staleness | 7 days |
| yield | (abs(word_delta) × max(delta_ab, 0)) / estimated_tokens |












## Design Choices & Data Layer







### Validated Patterns (from 58 experiments, Runs 19-27)

These patterns emerged from data. They should inform technique selection but not override the Bayesian priors — the priors will converge to the same conclusions over time.

| Pattern | Evidence | Implication |
|---------|----------|-------------|
| REWORD is the dominant technique | ~90% keep rate across both eval types, 15+ experiments | Default to REWORD when uncertain. Concrete examples > abstract rules. |
| REMOVE on unique content always reverts | 7/7 reverted (IDs, URLs, rules, formulas, behavioral constraints) | Pre-check uniqueness before REMOVE. If content exists nowhere else, don't remove it. Worked example: REMOVE on Brain's Foundational Decisions table (run47_exp3) lost decision IDs and dates → delta_ab = -0.362. The table was the only place those IDs lived. |
| REMOVE on motivational prose keeps | 2/2 kept (design philosophy, guiding principles) | Rubrics and protocols work without framing prose. Safe to compress. |
| MERGE on distinct registers always reverts | 3/3 reverted (guide/playbook, stakeholder/analytical) | Registers are real semantic boundaries. Don't merge categories that serve different query patterns. |
| SPLIT on structural organization always keeps | 4/4 kept (subsection headers, human/agent split) | Reorganization preserves content. Safe technique. |
| SPLIT labeling content "optional" reverts when it isn't | 1/1 reverted (WBR YoY context) | Check actual usage before labeling anything optional. |
| COMPRESS on explicit handoff steps reverts | 1/1 reverted (wiki-editor pipeline) | Pipeline integrity depends on checkpoint granularity. |
| Common Failures pattern is portable | 4/4 kept across email→wbr→mbr→librarian | Proven structural pattern for any style guide or agent file. |
| Concrete examples > abstract rules | +0.04 to +0.08 delta consistently | When adding a rule, always include a worked example. |
| Empty structural tables are load-bearing | 1/1 reverted (amcc avoidance ratio) | Tables define measurement frameworks even without data. |
| UCB-only selection produces 90%+ keep rate (selection bias) | Runs 19-25: 92% keep rate | Force 30% exploration of untested combos. Healthy batch ≤50% keep rate. Most experiments should revert. |







### Common Failures

1. **Skipping Agent B on "obvious" improvements.** Every experiment needs the control. The delta is the signal, not the absolute score.
2. **Scoring PARTIAL as CORRECT.** Detail-loss matters. If Agent A says "+187%" but Agent B says "CVR from 0.82% to 2.35%", A is PARTIAL — the supporting detail was lost.
3. **Running REMOVE without uniqueness pre-check.** 7/7 reverted. If the content exists nowhere else in the body, REMOVE will fail.
4. **Treating delta_ab = 0.0 as "nothing happened."** A KEEP at Δ=0.0 with -150 words is a compression win. A KEEP at Δ=0.0 with +50 words is neutral. The word delta is a covariate, not the goal.







### Core Principles - **Pure autoresearch.** Target→section→technique selected by UCB weights. Batch, random, autonomous. Volume over precision — most experiments revert, learning emerges from patterns. Bayesian priors self-terminate losers (posterior_mean < 0.15, n > 10 → excluded). - **Current-state organs.** No history in organs. changelog.md = audit trail. If content grows monotonically, it belongs in changelog, not an organ. - **Do no harm.** Brain/Memory: delta_ab ≥ 0, zero INCORRECT on any question. All others: delta_ab ≥ 0. Immediate rollback on violation. - **Usefulness over size.** Adaptive budgets from gut.md baselines + learned ceilings. ADD/COMPRESS priors discover natural organ size. A KEEP that adds 50 words at Δ=+0.1 beats a KEEP that removes 100 words at Δ=0.0. - **Dual blind eval.** A=modified+context, B=original+context, C=modified+zero context. Delta A-B is the signal. C reveals implicit dependencies. Evaluators unaware of each other. - **Per-organ cooldown.** No experimenting on organs modified by maintenance this invocation. Prevents confounding. - **Output quality + portability.** Style guides, context files, hook prompts are valid targets. Every change must work on a cold platform with no hooks, MCP, or subagents. **Authority:** All changes to this file, experiment queue, hyperparameters, and run protocol are governed by Karpathy authority (`~/.kiro/agents/body-system/karpathy.md`). No agent outside Karpathy authority modifies heart.md. 





### DuckDB Integration

All experiment data lives in `~/shared/data/duckdb/ps-analytics.duckdb`. Organs hold protocol (how to experiment). DuckDB holds data (what happened, what works).

**Update protocol** — after every experiment decision:
1. INSERT into `autoresearch_experiments` (full record)
2. UPDATE `autoresearch_priors` (increment α or β)
3. At end of batch: INSERT into `autoresearch_organ_health` (one row per organ with current word counts)

**How priors work:** Posterior_mean converges to the true keep rate per target×technique. UCB score = posterior_mean + posterior_std — unexplored combos get tried (high uncertainty), proven winners get prioritized (high mean), proven losers naturally fall off.

**Seeding new targets:** New target category → new rows in `autoresearch_priors` for every target × technique combo, initialized Beta(1,1). `eval_type` column distinguishes `information_retrieval` (organs) from `output_quality` (style guides / context files / hooks). Both flow through the same Bayesian updating.

**Schema reference:**

| Table/View | Purpose |
|------------|---------|
| `autoresearch_experiments` | One row per experiment. Full record: organ, technique, scores, delta, cost, decision. Includes `eval_type` column. |
| `autoresearch_priors` | Bayesian priors per target×technique. Beta(α,β) updated on every KEEP/REVERT. |
| `autoresearch_organ_health` | Snapshot per target per run. Word count, utilization, accuracy estimate over time. |
| `autoresearch_selection_weights` (view) | UCB scores for target selection. posterior_mean + posterior_std = exploration/exploitation balance. |







## Active Pipeline Experiments







### PE-1: Prediction Cadence & Lead-Time Structure (2026-W17)

**Status:** PHASE_1_SHIPPED (2026-04-21)
**Phase 1:** `lead_weeks INT NULL` + `prediction_run_id VARCHAR NULL` added to ps.forecasts. `_write_projections` computes both on INSERT. DELETE unchanged. Backward compatible (NULL columns).
**Hypothesis:** Explicit lead-time tagging (Arm C) produces higher CID than weekly-overwrite (Arm A) or multi-run-append (Arm B).

| Arm | Cadence | Write behavior | Lead-time scoring |
|-----|---------|----------------|-------------------|
| A (control) | 1×/wk, DELETE+INSERT | Overwrites unscored | None |
| B | 3×/wk, INSERT only | Accumulates | Implicit (forecast_date spacing) |
| C | 1×/wk, INSERT + `lead_weeks` | Accumulates with tag | Per bucket: 1, 2-3, 4-8, 9-16, 17+ |

**Primary:** CID = scored_predictions_with_distinct_lead_times / (target_weeks × markets). Target ≥ 3.0 after 4 scored weeks.
**Secondary:** first-vs-latest spread, lead-time error decay slope, structural event detection rate.
**Priors:** A=Beta(1,1), B=Beta(2,1), C=Beta(3,1). **Keep:** CID_winner > CID_control, no reliability regression, storage < 10×.
**Eval window:** W18-W22.

**Phase 1 Validation:**
1. `lead_weeks` populated on new rows: `SELECT lead_weeks, COUNT(*) FROM ps.forecasts WHERE forecast_date > '2026-04-21' GROUP BY lead_weeks`
2. `prediction_run_id` unique per batch: `SELECT prediction_run_id, COUNT(*) FROM ps.forecasts GROUP BY prediction_run_id HAVING COUNT(*) > 52`
3. No NULL `lead_weeks` on new rows (old rows stay NULL)
4. DELETE unchanged: scored rows not deleted


