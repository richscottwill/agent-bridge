---
title: "Proposal: Expand Experiment Scope to Output Quality"
status: archived
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0130 | duck_id: context-experiment-scope-expansion-proposal-adopted-20260403 -->

# Proposal: Expand Experiment Scope to Output Quality

Route to: Karpathy

## Problem

The autoresearch loop currently experiments only on organ files (`~/shared/context/body/*.md`). It measures information retrieval accuracy (can the agent answer questions about the organ's content?). But the system's real purpose is producing high-quality output — emails, callouts, documents, task management decisions. Information accuracy is necessary but not sufficient for output quality.

The style guides, market context files, callout principles, and hook prompts all affect output quality but are never experimented on. Changes to these files are made manually without measurement.

## Proposal

Expand the experiment target set and eval methodology:

### New Target Categories

| Category | Files | Example Experiment |
|----------|-------|-------------------|
| Style guides | `~/.kiro/steering/richard-style-*.md` | REWORD the email drafting checklist → does the next Lena email score higher? |
| Market context | `~/shared/context/active/callouts/*-context.md` | ADD a narrative thread to AU context → does the AU callout draft improve? |
| Callout principles | `~/.kiro/steering/callout-principles.md` | REMOVE a principle → does callout quality degrade? |
| Hook prompts | `~/.kiro/hooks/*.kiro.hook` | REWORD the AM-2 triage prompt → does task prioritization improve? |

### Eval Methodology Change

Current: "Can the agent answer factual questions about the organ?"
Proposed: Add output-quality evals alongside information-retrieval evals.

**Output-quality eval design:**
- Agent A (modified file + full context) produces a work product (email, callout, doc section)
- Agent B (original file + full context) produces the same work product
- Karpathy scores both against the relevant style guide checklist + Amazon writing norms
- delta_ab = quality difference

**Scoring dimensions for output quality:**
1. Voice match (does it sound like Richard?)
2. Structure match (does it follow the doc type's template?)
3. Data integration (are numbers contextualized with "so what"?)
4. Audience calibration (is the register right for the recipient?)
5. Actionability (does it include clear next steps?)

### What Stays the Same

- A/B/C blind eval design
- Bayesian priors per target×technique
- DuckDB logging
- Keep/revert rules (delta_ab ≥ 0)
- Brain/Memory safety floor

### What Changes

- `autoresearch_priors` table needs new organ values for style guides, context files, etc.
- Eval questions become "produce this output" instead of "answer this question"
- Scoring becomes multi-dimensional (voice + structure + data + audience + actionability) averaged into a single score
- Experiments on style guides require the Karpathy agent to also load the relevant style guide as context for the eval agents

## Evidence from Run 18

The writing experiments (experiments 57-58) already demonstrated this approach works:
- Email draft: style guides added +0.15 delta (naming partners, tighter timelines, political awareness)
- Doc outline: style guides added +0.15 delta (methodology section, confidence levels, risk framing)
- Both used the same A/B design as organ experiments

The infrastructure is already there. The proposal is to formalize it and make it part of the regular loop.

## Minimum Viable Implementation

1. Add style guide files to the target selection pool in heart.md
2. Add "output_quality" as an eval_type column in autoresearch_experiments
3. Define the 5 scoring dimensions in heart.md
4. Seed autoresearch_priors with new rows for style guide × technique combos
5. Run 10 output-quality experiments to calibrate the scoring

## Principle Alignment

- Structural over cosmetic: changes the experiment engine, not the format
- Evidence-based: Run 18 writing experiments already validated the approach
- Subtraction before addition: doesn't add a new system — extends the existing one
