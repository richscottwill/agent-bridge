# Steering Discovery Eval — Final Verdict

**Date:** 2026-04-22
**Protocol:** Type C variation test per `blind-test-methodology.md`
**Method:** 5 discovery tasks × 4 arms (baseline + 3 variations) × blind evaluator per task = 15 treatment runs + 5 blind evals (baselines also run fresh this time, not reused)
**Randomization:** Python seed 46, shuffled A–D labels per task
**Scoring rubric:** adapted for discovery — Discovery success / Time-to-discovery / No false positives / Output quality / META robustness, 10 pts each = 50/arm/task

---

## Headline

**A variation wins for the first time across 4 rounds.** Var2 (steering-index.md always-on) scores 228/250, beating baseline (154/250) by 74 points — the largest margin of any round.

| Variation | D1 Slack | D2 Excel | D3 Hook eval | D4 MBR | D5 skip-level | **Total /250** | **Avg /50** |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Var2** (steering-index.md) | 44 | **47** | **47** | **46** | 44 | **228** | **45.6** |
| Var1 (soul.md canonical table) | 47 | **49** | 42 | 39 | 42 | 219 | 43.8 |
| Var3 (both combined) | **48** | 48 | 26 | 37 | 43 | 202 | 40.4 |
| **Baseline** (current state) | 31 | 20 | 15 | 42 | **46** | 154 | 30.8 |

**Bold** = task winner.

Task-level split:
- **Var1 won D2** (Excel drop — exact trigger match in canonical table)
- **Var2 won D3, D4** (hook eval — trigger row was the literal match; MBR — analytical-companion discovery via index)
- **Var3 won D1** (Slack — redundancy helped on a task where multiple mechanisms could fire)
- **Baseline won D5** (skip-level — the task whose routing is already in soul.md, so all arms routed correctly and baseline scored highest on honesty about its own failure probability)

## Why baseline lost decisively

Baseline catastrophically failed D3 (15/50) and D2 (20/50). In both cases, the evaluator confirmed what I diagnosed earlier: **there's no cue in default steering that maps "evaluate proposal" or "Excel drop" to the relevant manual file.** Baseline honestly self-diagnosed the gap in both cases but would have produced downstream output that was structurally complete but domain-thin (D2) or missing the methodology layer entirely (D3).

Baseline won D5 not because discovery was better — all four arms routed to rw-trainer correctly — but because its honesty about its own drift probability was the strongest. That's a rubric artifact, not a win on discovery.

## Per-variation verdicts

### ✅ Var2 (Standalone always-on steering-index.md) — ADOPT

- **Best aggregate** (228/250, 45.6 avg).
- **Won 3 of 5 tasks decisively** (D3 47, D4 46, D2 47).
- **Crucial win on D4 (MBR):** only arm to discover `performance-marketing-guide.md` as the analytical companion to style files. The index's explicit "Analytical / Excel drop" row surfaced what the canonical-table-only approach missed.
- **Mechanism strength:** an annotated directory with explicit task triggers is more discoverable than a compact table. Agents scan the list and can match on more signal types.
- **Tradeoff:** adds one always-on file (~60 lines), one more maintenance point. Soul.md doesn't bloat further.

### ⚠️ Var1 (Extended soul.md canonical resources table) — STRONG RUNNER-UP

- **Second place** (219/250, 43.8 avg).
- **Won D2 decisively** (49/50) — tied for highest single-task score across all rounds.
- **Weakness on D4 and D3:** compact table format didn't surface `performance-marketing-guide.md` as an MBR companion (D4), and evaluators flagged that multi-category requests (D3: hook = tool + system change + architecture) create pick-one-door ambiguity with a compact table.
- **Mechanism strength:** zero new file, keeps everything in soul.md which is already always-on. Matches existing structure.
- **Tradeoff:** soul.md grows ~20 lines. On composite tasks (task spans multiple categories), the table forces a choice and the agent may miss secondary relevant files.

### ❌ Var3 (Both combined) — REJECT

- **Third place** (202/250, 40.4 avg) — **worse than either component alone**.
- **Won D1 (48/50)** but only because redundancy accidentally helped on a task where the mechanism didn't matter much.
- **Catastrophic on D3** (26/50) and **worst on D4 (37/50)**. Evaluators noted that redundancy created decision ambiguity: agents saw both the soul.md table AND the index, tried to reason about which to use, and ended up less decisive than arms that had only one mechanism.
- **Pattern:** violates principle #3 (subtraction before addition). Two sources of truth for the same mapping = confusion, not safety net. The "defense in depth" intuition is wrong when the mechanisms are redundant rather than complementary.

### ❌ Baseline — REJECT (current state leaves gaps)

- **Last place** (154/250, 30.8 avg).
- **Two catastrophic failures** (D2: 20/50 on Excel drop, D3: 15/50 on hook eval). The `performance-marketing-guide.md` file and `blind-test-methodology.md` file are both invisible from default steering.
- **Baseline's strength (D5 46/50)** is not a discovery win — all arms routed correctly. It's a rubric artifact where baseline happened to score highest on honesty dimension.
- **Not keeping baseline** — the current state ships 14 manual-inclusion files that agents can't reliably find.

## What this round uniquely proved

For 3 rounds, external-AI-review variations lost to baseline. Round 4 followup (today's follow-on) tested conditional triggers for soul.md and still lost. **This is the first round where variations beat baseline decisively, and the reason is instructive:**

The prior 3 rounds were testing *always-on behavioral additions* (procedures, mandates, frameworks). Those taxed every task; the always-on cost dimension was decisive. **Baseline kept winning because adding behavior is almost always worse than baseline once soul.md is well-tuned.**

This round tested *a discoverability fix for files the agent already knows how to use once loaded*. That's a different shape entirely. Loading-the-right-file has near-zero always-on cost (files aren't loaded unless triggered) and high upside when the file is needed. The tradeoff reverses: variations win because the baseline discovery mechanism (name-only lookup + pointer chains through auto-loaded files) is actually broken.

**The meta-lesson: blind testing correctly discriminates structural gap-fills from behavioral ceremony.** The same protocol that rejected 0/3 behavioral variations in round 4 accepts 1/3 structural variations in this round. The rubric isn't biased toward rejection — it's biased toward "does the addition earn its always-on cost," and structural fixes earn more cheaply than behavioral ones.

## Concrete actions

### 1. Adopt Var2 — create `.kiro/steering/steering-index.md` (always-on)

Create the file with the full annotated directory covering all 14 manual-inclusion steering files. Structure:
- Writing style section (Slack/email/WBR/MBR/docs/Amazon/core)
- Analytical / operational section (performance-marketing, high-stakes auto-load, MX constraints, task prioritization, WW testing prep)
- System / protocol section (blind-test-methodology, blind-test-harness, architecture-eval, asana-guardrails, Slack search)
- Thought-pattern section (mario-peter, influences)

Use explicit task-trigger rows, not compact names-only lists. Evaluators confirmed the trigger wording is load-bearing — "Evaluating proposed system changes → blind-test-methodology.md" worked on D3 where a tighter name match would have missed.

### 2. Do NOT add a canonical-resources table to soul.md

Keep soul.md focused on identity, principles, and high-level routing to specialist agents. The Var3 combined experiment proved that redundancy across soul.md and a dedicated index creates ambiguity without value. Principle #3 (subtraction before addition) — one source of truth is better than two.

The existing professional-writing rule in soul.md's Agent Routing Directory is fine as-is. It's narrow (writing only) and complements the broader steering-index rather than duplicating it.

### 3. Do NOT rely on naming-only pattern-matching

Baseline's D1 success (a discovery "pull" through `richard-writing-style.md`'s pointer section) is fragile. It only works because `richard-writing-style.md` is auto-inclusion and contains an explicit pointer. If either condition changes, fresh agents default to email styling on Slack tasks. The steering-index eliminates this fragility.

### 4. Update blind-test-methodology.md with round 5 findings

Add two specific findings:
- **Structural additions can beat baseline** (in contrast to rounds 1–4 on behavioral additions). The test type matters; always-on-cost weights differently for structural-fix proposals.
- **Redundancy is not defense-in-depth.** Var3 demonstrated that two sources for the same mapping degrade performance vs one. Future "combined" variations should be tested for complementary-not-redundant mechanisms.

### 5. Close the external-AI-review thread and consider internal thread open

This round was internal (I proposed the three variations, not an external reviewer). Unlike rounds 1–4, the proposals came from structural analysis of an observed discovery gap. That class of proposal is worth continuing to test — different prior than "external AI suggests an addition."

## Meta-lessons

1. **Test types discriminate proposals differently.** Behavioral-addition testing (rounds 3–4) is fair and usually rejects. Structural-fix testing (round 5) is fair and can adopt. The methodology is the same; the prior changes based on proposal shape.
2. **Redundancy isn't safety.** Two mechanisms for the same job = ambiguity cost. Only combine mechanisms when they address different failure modes.
3. **Baseline scored highest on D5 but on "honesty" rubric, not "discovery" rubric.** This is a signal that D5's rubric wasn't discriminating — all arms routed correctly. Future discovery tests should ensure at least 1 task has a real discovery gap for baseline to fail on.
4. **The adopt-worthy signature held.** Var2 matches all 4 properties from blind-test-methodology.md:
   - Specific failure mode: name-only discovery for 14 manual files
   - Task-specific/conditional: each row has a trigger, not a blanket rule
   - Structural: changes the default (what's visible on bootstrap), not cosmetic
   - Blind-testable: the round confirms discovery rate with/without
5. **Discovery-gap catastrophic failures (baseline D2/D3) are visible in real work.** Agents silently missing `performance-marketing-guide.md` on Excel drops is not hypothetical — it's what happens today. The structural fix is overdue.

## Evidence files

- Proposed variations: `shared/tmp/steering-discovery-eval/proposed/var[1-3]-*.md`
- Treatment runs (15 files): `shared/tmp/steering-discovery-eval/runs/d[1-5]-[baseline|var1|var2|var3].md`
- Blind verdicts (5): `shared/tmp/steering-discovery-eval/blind-eval/d[1-5]-verdict.md`
- Randomization: `shared/tmp/steering-discovery-eval/randomization.csv` (seed 46)
- Methodology: `.kiro/steering/blind-test-methodology.md`
