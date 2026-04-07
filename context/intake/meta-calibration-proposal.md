<!-- DOC-0178 | duck_id: intake-meta-calibration-proposal -->
# Proposal: Meta-Calibration — Are Our Priors Helping?

Route to: Karpathy

## Problem

The autoresearch loop uses Bayesian priors (autoresearch_priors) to select which experiments to run. The projection system uses calibration notes (au-projections.md) to adjust forecasts. But we've never validated whether these statistical tools are actually improving outcomes vs. introducing bias.

## Three Recurring Calibration Checks

### 1. Prior-Guided vs Random Selection (monthly)

**Design:** Run two batches in the same session.
- Batch A: Select experiments using UCB scores from autoresearch_priors (the current approach)
- Batch B: Select experiments purely randomly (ignore priors, pick organ and technique uniformly at random)
- Compare keep rates. If priors are working, Batch A should have a higher keep rate.

**What it tests:** Are the priors helping us pick better experiments, or are they just reinforcing early biases?

**Blinding:** Batch B agent doesn't see the priors table. It picks randomly from all 112 target×technique combos.

**When to worry:** If Batch B's keep rate is within 5% of Batch A's, the priors aren't adding value — they're just adding complexity. If Batch B's keep rate is HIGHER, the priors are actively hurting (selecting away from productive experiments).

### 2. Projection Calibration Audit (weekly, after actuals arrive)

**Design:** When W14 actuals arrive, compare:
- Agent A's projection (made with projection history + calibration note)
- Agent B's projection (made fresh, no history)
- Actuals

**What it tests:** Did the calibration note ("discount by 2-3%") improve accuracy, or did it overcorrect?

**Tracking:** Add a row to au-projections.md each week:
```
## W13 Projection Audit
- Stored projection (Agent A): ~1,000 regs, $130K, $130 CPA
- Fresh projection (Agent B): ~1,020 regs, $125K, $123 CPA
- Actuals: [fill when known]
- Winner: [A or B]
- Calibration note accuracy: [helped / hurt / neutral]
```

Over 4-6 weeks, this builds a track record. If the stored projection consistently wins, the calibration approach is validated. If fresh consistently wins, the calibration notes are overcorrecting.

### 3. Output Quality Prior Validation (quarterly)

**Design:** The new output-quality priors (style guide × technique combos) are all at Beta(1,1) — uninformed. After 10+ experiments per combo, check:
- Do the priors predict which style guide changes will keep vs revert?
- Is there a pattern the priors missed? (e.g., ADD on style guides always keeps, but the prior hasn't converged because the experiments were too diverse)

**What it tests:** Are the output-quality priors converging to useful signals, or are they noise?

## Implementation

- Check 1: Add to the EOD-2 hook prompt as a monthly task (first business day of month, alongside goal updater)
- Check 2: Add to the weekly callout pipeline — after ingesting new week's data, audit last week's projection
- Check 3: Add to Karpathy's quarterly metabolism report

## Principle Alignment

- Evidence-based: testing our own tools with the same rigor we test the organs
- Structural over cosmetic: changes how we evaluate the evaluation system, not just the format
- Subtraction before addition: if the priors aren't helping, we should simplify to random selection (fewer moving parts)
