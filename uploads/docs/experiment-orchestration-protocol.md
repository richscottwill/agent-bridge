<!-- DOC-0232 | duck_id: other-experiment-orchestration-protocol -->
# Experiment Protocol Overhaul — Two Issues

Date: 2026-03-31
For: Karpathy (heart.md overhaul)
Status: Tested orchestration architecture. Spirit of autoresearch not yet addressed. Needs Richard's approval + Karpathy formalization.

## Issue 1: Orchestration (technical — solved)

heart.md Step 4 says Karpathy spawns two blind evaluator subagents. In practice, nested subagent invocation fails (Q13.registerSubAgentExecution error). This means the dual blind eval has never actually run as designed — experiments were self-evaluated or skipped.

### Corrected Architecture

The main loop orchestrates all three agents sequentially. No nesting required.

1. **Main loop invokes Karpathy** → Karpathy selects target, snapshots, applies experiment, generates 5 eval questions + ground truth answers. Returns: modified file, eval questions, ground truth.
2. **Main loop invokes Evaluator A** (Amazon-context) → receives modified file + body.md + soul.md + questions. Just answers the questions. No scoring. Returns: answers only.
3. **Main loop invokes Evaluator B** (Generic/no-context) → receives ONLY modified file + questions. Just answers. No scoring. Returns: answers only.
4. **Main loop invokes Karpathy again** → receives both evaluators' answers + ground truth. Karpathy scores each answer (CORRECT/PARTIAL/INCORRECT, SELF-CONTAINED/NEEDS-MORE-CONTEXT). Makes KEEP/REVERT decision per heart.md thresholds.

### Key Design Principles

- Evaluators are witnesses, not judges. They answer questions. They don't score themselves.
- Karpathy is the judge. It knows ground truth and applies the scoring rubric.
- Neither evaluator knows what was changed, what the correct answers are, or that the other evaluator exists.
- The main loop is the orchestrator — it passes data between agents but doesn't make experiment decisions.

### Tested

2026-03-31: Ran full pipeline on Device compression (2,409w → 1,386w). Both evaluators answered independently. Karpathy scored: A=5/5, B=5/5. KEEP. No gaps. Architecture works.

## Issue 2: Spirit of Autoresearch (philosophical — needs redesign)

The current experiment system violates the core autoresearch principle: random, basic, high-volume, stripped of confidence.

### What autoresearch actually is (Karpathy's original)
- 630 lines of code, 700 experiments
- Small, random, fast
- No hand-crafted hypotheses
- No named experiments with multi-paragraph design docs
- Let the data tell you what works
- Volume over precision — most experiments fail, that's the point

### What we've been doing instead
- 8 experiments in 14 loop runs (~0.6 per run)
- Each experiment is a carefully designed, named, multi-paragraph hypothesis (CE-1 through CE-7)
- Experiments sit in a queue for weeks before running
- Each one feels like a waterfall project, not a random probe
- The queue is a backlog of design docs, not a stream of random trials

### What should change in heart.md

1. **Kill the named experiment queue.** CE-5, CE-6, CE-7 as pre-designed experiments go away. Replace with: Karpathy picks a random organ (weighted by over-budget first, then staleness), picks a random section within that organ, picks a random technique, and applies it. No hypothesis document. No name. Just: organ, section, technique, result.

2. **Volume target.** 5 experiments per batch run, not 1. Most will revert. That's fine. The learning is in the revert pattern, not the individual experiment.

3. **Strip confidence.** Karpathy doesn't predict whether an experiment will work. It tries it and measures. The eval is the only signal. No "expected impact" paragraphs.

4. **Log format is minimal.** Instead of multi-paragraph CE-N entries, log as: `[organ:section] COMPRESS → 2120w→1980w. A=5/5 B=4/5. KEEP.` or `[organ:section] REMOVE → 1297w→1250w. A=3/5 B=4/5. REVERT.` One line per experiment. The changelog accumulates signal over time.

5. **Learning emerges from volume.** After 50+ experiments, patterns emerge: "COMPRESS on Brain always reverts" or "REWORD on Eyes always keeps." That's the autoresearch insight — it comes from data, not from pre-designed hypotheses.

6. **Keep the do-no-harm rules.** Brain/Memory 100% accuracy, identity field protection, snapshot before every edit, revert on failure. The safety net stays. The experiment selection becomes random.

### Requested Change

Rewrite heart.md experiment queue section and run protocol to reflect random, high-volume, minimal-logging autoresearch. Keep the orchestration architecture from Issue 1. Keep the do-no-harm rules. Kill the waterfall.
