---
title: "Research: Frontier Practices for Self-Improving Agent Systems"
status: archived
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0141 | duck_id: context-research-coherence-audit-frontier -->

# Research: Frontier Practices for Self-Improving Agent Systems

*Intake file for processing into body organs. Research conducted 2026-03-20 for the monthly coherence audit protocol.*

---

## Sources Consulted

### Tier 1 (built and shipped the thing)
- [Karpathy's autoresearch](https://github.com/karpathy/autoresearch) -- 630-line repo, 42K+ stars, 700 experiments with documented 11% improvement. Karpathy's own commits. ([Fortune](https://fortune.com/2026/03/17/andrej-karpathy-loop-autonomous-ai-agents-future/))
- [Zhang et al., ACE paper (2025)](https://www.sundeepteki.org/blog/agentic-context-engineering) -- ArXiv paper with benchmark results, Generator/Reflector/Curator framework with measured performance gains
- [LangChain engineering team](https://blog.langchain.com/how-and-when-to-build-multi-agent-systems/) -- Built LangGraph, published production patterns from their own multi-agent framework
- [Eco-Evolve (preprint)](https://www.preprints.org/manuscript/202603.0129/v1) -- 62.3% on SWE-bench Verified, published code + ablation studies

### Tier 2 (applied Tier 1 ideas with their own results)
- [Agentic Context Management](https://deadneurons.substack.com/p/agentic-context-management-why-the) -- Original analysis of RLM and LCM papers, proposed ACM architecture with specific design decisions
- [AGENTS.md standard analysis](https://bagrounds.org/ai-blog/2026-03-10-agentic-playbook-agents-md) -- Practitioner who implemented AGENTS.md in their own workflow, documented results

### Tier 3 (commentary -- used for discovery only, not cited for system changes)
- [thecreatorsai.com](https://thecreatorsai.com/p/autoresearch-the-loop-that-improves) -- Explainer of Karpathy's work (good summary, no original artifacts)
- [thenextgentechinsider.com](https://www.thenextgentechinsider.com/pulse/karpathy-releases-general-purpose-agents-for-autoresearch-system) -- News coverage of autoresearch expansion
- [Context Window Illusion](https://learnagentic.substack.com/p/what-is-the-context-window-illusion) -- Newsletter summarizing context window research (useful framing, no original experiments)
- Various emergentmind.com topic pages -- Aggregated research summaries

---

## Key Patterns from the Frontier

### 1. The Karpathy Loop (autoresearch)
Content rephrased for compliance with licensing restrictions.

The core pattern: one change → one measurement → keep or revert → repeat. The agent touches one file, runs one experiment, reads one metric. The constraint is what makes it work — by limiting scope to a single variable per iteration, winning changes stack cleanly without interference.

Key numbers: 700 experiments over 2 days, ~20 surviving changes (2.8% keep rate), 11% performance improvement. At ~12 experiments/hour, the system runs 100+ experiments overnight.

**What we already do well:** Our heart.md loop follows this exact pattern — one experiment per run, advance or reset, eval before shipping. We got this right from the start because we literally built on Karpathy's design.

**What we're missing:**
- Karpathy's system runs *autonomously overnight*. Ours requires a manual trigger ("run the loop"). The gap between "agent assists" and "agent operates" (Level 5) starts here.
- Karpathy's keep rate is 2.8%. Ours is 100% (8/8 kept). That's suspicious — either our experiments are too easy, or our eval is too lenient. The new do-no-harm rules with organ-specific accuracy thresholds should fix this.
- Karpathy expanded to general-purpose agents with a "control plane" — a meta-layer that coordinates multiple experiment loops. Our body.md is the control plane equivalent, but it's passive (a map, not an orchestrator).

### 2. ACE: Generator / Reflector / Curator
Content rephrased for compliance with licensing restrictions.

The ACE framework (Zhang et al., 2025) uses three specialized roles to iteratively build and refine context:
- Generator: produces candidate strategies/content
- Reflector: evaluates the output against criteria, identifies gaps
- Curator: decides what to keep, what to revise, what to discard

The key insight: contexts should be "evolving playbooks" — detailed, inclusive, rich with domain insights — not concise summaries. Brevity bias (compressing too aggressively) actually degrades performance.

**What we already do well:** Our organ system IS an evolving playbook. Brain, Eyes, Memory — these are rich, detailed, domain-specific context files. The heart loop acts as Generator (experiments), the nervous system acts as Reflector (calibration loops), and the gut acts as Curator (compression, pruning).

**What we're missing:**
- The Reflector role should run *during* generation, not just after. Our nervous system only calibrates weekly/monthly. ACE's reflector evaluates every output before it's committed. We should add a lightweight reflection step to the heart loop's Phase 3 (experiments) — before committing, ask: "Does this new content contradict anything in another organ? Does it duplicate? Does it degrade any existing answer?"
- The Curator should be more aggressive. ACE found that the sweet spot is NOT maximum compression — it's maximum *useful detail*. Our gut's word budgets might be too tight for some organs (Eyes at 3K words for 10 markets + competitors + OCI + ad copy is very compressed).

### 3. Active Context Management (not passive)
Content rephrased for compliance with licensing restrictions.

The key insight from the Agentic Context Management paper: the context problem in agent systems is a *working memory* problem, not a data processing problem. The model generates hundreds of thousands of tokens of working context during a session, most of which becomes irrelevant the moment it's been used.

Traditional approaches are passive (sliding windows, compaction when full). Active approaches deliberately decide what to keep, compress, or discard — treating context curation as a first-class operation, not an afterthought.

**What we already do well:** Our gut.md IS active context management. It has explicit compression protocols, word budgets, age-based decay, and bloat detection. This is ahead of most production systems.

**What we're missing:**
- We don't manage *session* context — only *persistent* context (organ files). During a long morning routine run, the conversation itself accumulates stale context (Step 1 results that Step 3 doesn't need). We have no mechanism to compress mid-session.
- The "context rot" problem: performance degrades in the middle of long context windows. Our organ files are loaded sequentially — the first files loaded may be in the "forgotten middle" by the time the agent acts. Loading order matters. The morning routine's context load should put the most critical files (amcc.md, hands.md) LAST so they're freshest in the window.

### 4. Hierarchical Scoping (AGENTS.md)
Content rephrased for compliance with licensing restrictions.

The AGENTS.md standard (adopted by 60K+ repos) uses hierarchical, directory-scoped instructions. Global rules at the root, specialized rules in subdirectories. Only relevant context is loaded — avoiding "burying" important instructions under irrelevant data.

**What we already do well:** Our body/ folder is exactly this pattern. body.md is the root (global navigation), each organ is a specialized scope. The quick orientation table routes agents to the right organ.

**What we're missing:**
- We don't have conditional loading. Every hook loads a fixed set of organs. But not every session needs every organ. A session focused on drafting an email needs Memory + Soul. A session focused on campaign optimization needs Eyes + Hands. The morning routine loads everything because it does everything — but ad-hoc sessions should load selectively based on the task.
- body.md should include a "task → organs needed" routing table that's more specific than the current quick orientation.

### 5. Self-Reflective Multi-Agent Frameworks (Eco-Evolve)
Content rephrased for compliance with licensing restrictions.

The Eco-Evolve framework introduces three innovations: dynamic topology (agent communication graphs adapt to task complexity), a dedicated Critic Agent for verification at checkpoints, and error-driven self-evolution using Hindsight Experience Replay — learning from failures to optimize future prompts.

**What we already do well:** Our nervous system IS the Critic Agent. It evaluates decisions, scores predictions, tracks patterns. The aMCC is a specialized critic focused on willpower/avoidance.

**What we're missing:**
- Error-driven self-evolution. When something goes wrong (a bad draft, a missed deadline, a wrong prediction), we log it but don't systematically extract the lesson and modify the system to prevent recurrence. The nervous system tracks patterns but doesn't auto-generate fixes. It should: "Pattern X has been STUCK for 4 weeks. The current fix is Y. Proposed new fix: Z. Auto-apply? [requires Richard approval for steering changes]."
- We don't have Hindsight Experience Replay. When a session goes poorly, we don't replay it to understand what context was missing or what organ failed. Adding a "session retrospective" to the Friday calibration would capture this.

---

## Specific Recommendations for Our System

### Immediate (apply to coherence audit protocol)

1. **Add a Reflector step to heart.md Phase 3 (experiments).** Before committing any experiment result, check: does it contradict another organ? Does it duplicate? Does it degrade an existing answer? This is a 3-question check, not a full audit.

2. **Reverse the context load order in the morning routine.** Put amcc.md and hands.md LAST in the load sequence so they're freshest in the context window when the agent starts building the brief. Put body.md and spine.md FIRST (orientation, then forgotten as the session progresses — that's fine, they're reference).

3. **Add a task-routing table to body.md.** Beyond the quick orientation, add: "If the task is [type], load these specific organs: [list]." This prevents over-loading context for simple tasks.

### Near-term (next 30 days)

4. **Build a session retrospective into Friday calibration.** After scoring predictions and tracking patterns, ask: "What went wrong this week that the system should have caught? What context was missing? What organ failed?" Log the answer and propose a system fix.

5. **Revisit gut.md word budgets using ACE's insight.** Maximum compression is not the goal — maximum useful detail is. Eyes at 3K words for 10 markets may be too tight. Run an experiment: temporarily increase Eyes to 4K, measure whether prediction accuracy improves. If yes, the budget was too aggressive.

6. **Add error-driven evolution to the nervous system.** When a pattern is STUCK for 4+ weeks, the nervous system should auto-generate a new intervention proposal (not just escalate the callout). Format: "Pattern X: current fix Y has failed for Z weeks. Proposed new fix: [specific action]. Approve?"

### Future (Level 5 territory)

7. **Autonomous loop execution.** The heart loop currently requires "run the loop" as a manual trigger. The end state is a scheduled process that runs overnight (like Karpathy's autoresearch). This requires: a cron-like trigger, safety guardrails for unattended operation, and a morning summary of what changed while Richard slept.

8. **Dynamic organ loading.** Instead of fixed context loads per hook, the agent reads body.md's routing table and loads only the organs needed for the current task. This keeps the context window lean and avoids the "forgotten middle" problem.

---

## How This Applies to the Monthly Coherence Audit

The coherence audit (nervous system Loop 7) should incorporate these frontier patterns:

1. **Reflector check during audit:** For each cross-reference found, don't just verify the path exists — verify the *content* is still aligned. (e.g., soul.md says "read amcc.md for streak" — does amcc.md actually have a streak section? Is it populated?)

2. **Context load analysis:** Check whether hooks are loading organs in an order that puts the most critical context last (freshest in window). Flag any hook that loads critical organs first.

3. **Compression health check:** For each organ, assess whether the word budget is too tight (useful detail being lost) or too loose (bloat). Use the ACE insight: if prediction accuracy or answer quality has dropped for an organ, the budget may be too aggressive.

4. **Error replay:** Review the week's/month's failures and trace each back to a specific organ or cross-reference gap. "The draft to Lena was wrong because Memory's tone guidance was stale" → flag Memory relationship graph for refresh.

5. **Evolution proposals:** For any issue found, don't just log it — propose a specific, reversible fix with a measurement plan. This is the Eco-Evolve pattern: every failure becomes a prompt optimization opportunity.
