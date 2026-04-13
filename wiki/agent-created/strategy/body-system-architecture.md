---
title: "The Body System — Architecture for Personal AI Operating Systems"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0381 | duck_id: strategy-body-system-architecture -->

---
title: The Body System — Architecture for Personal AI Operating Systems
status: DRAFT
doc-type: strategy
audience: personal
level: 5
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: new organ added, architecture changes, system shared externally
---

# The Body System — Architecture for Personal AI Operating Systems

## What This Is

A framework for building persistent, self-maintaining AI systems that operate as extensions of a single person's work. Built by Richard Williams (March 2026) to solve a specific problem: knowing what to do but not consistently doing it.

The architecture is novel. Most AI assistants are stateless — they start fresh each conversation. The body system is stateful — it maintains context across sessions, experiments on its own processes, and enforces behavioral commitments. It's inspired by Karpathy's autoresearch concept, Duhigg's habit loops, and McKeown's essentialism.

## Core Architecture

### The Body Metaphor
11 organs, each a self-contained markdown file with a specific function:

| Organ | Function | Analogy |
|-------|----------|---------|
| Soul | Identity, values, voice | DNA |
| Brain | Decisions, principles, strategy | Prefrontal cortex |
| Eyes | Market data, metrics, predictions | Sensory input |
| Hands | Tasks, execution, tooling | Motor system |
| Memory | Relationships, compressed context | Hippocampus |
| Spine | Bootstrap, IDs, directory | Skeleton |
| Heart | Loop protocol, experiments | Circulatory system |
| Device | Automation, delegation, tools | Phone/laptop |
| Nervous System | Calibration, patterns, feedback | Feedback loops |
| aMCC | Willpower, streak, resistance | Anterior midcingulate cortex |
| Gut | Compression, budgets, waste removal | Digestive system |

The metaphor isn't decorative — it's functional. Each organ has a word budget, an update trigger, and a decay protocol. The system trends toward compression, not accumulation.

### Key Design Principles
1. Current-state-only: organs hold NOW, not history. Changelog is the audit trail.
2. Word budgets: each organ has a hard ceiling. The gut enforces it.
3. Self-maintaining: the autoresearch loop refreshes organs without human intervention.
4. Portable: the system is plain text files. It survives a platform move.
5. Experimentable: the heart runs structured experiments on the system itself.

### The Autoresearch Loop
Inspired by Karpathy. The system experiments on itself:
1. Maintenance: refresh ground truth from email/calendar/meetings
2. Cascade: update organs with new information
3. Experiment: run one structural change, measure impact, keep or revert
4. Compression: the gut enforces word budgets after each run

### The Habit Loop (Duhigg)
The morning routine IS a habit loop:
- Cue: one-click trigger (invariant)
- Routine: 4-step sequence (shape invariant, contents evolve)
- Reward: populated calendar + clear brief (invariant)

## What Makes It Work
- Persistent context across sessions (organs survive chat deletion)
- Structured compression (information has a half-life, the gut tracks decay)
- Behavioral enforcement (aMCC fires in real-time, not after the fact)
- Dual-blind evaluation (experiments are scored by independent sub-agents)
- Source tracking (every fact has a provenance)

## What Doesn't Work Yet
- No direct access to Slack, Asana, Google Ads, Adobe — workarounds only
- Agent can draft but not send (safety hooks prevent autonomous communication)
- Strategic artifacts still require heavy human input — agent can scaffold but not create
- The system is optimized for one person — team scaling is untested

These limitations are known and accepted. The system is designed to work within them — workarounds (email bridge, morning routine hooks) exist for each gap.

## Potential Applications Beyond PS
- Any knowledge worker with recurring tasks, multiple stakeholders, and information overload
- Sales teams (CRM context + meeting prep + follow-up drafting)
- Program managers (status tracking + stakeholder communication + risk detection)
- Executives (briefing generation + decision logging + pattern detection)

## Sources
- Architecture — source: ~/shared/context/body/body.md (system map)
- Autoresearch loop — source: ~/shared/context/body/heart.md
- Compression protocol — source: ~/shared/context/body/gut.md
- aMCC design — source: ~/shared/context/body/amcc.md
- Habit loop framework — source: ~/shared/context/active/morning-routine-experiments.md → Duhigg section
- Karpathy influence — source: ~/.kiro/steering/soul.md → Influences

<!-- AGENT_CONTEXT
machine_summary: "Architecture doc for the Body System — an 11-organ personal AI operating system built on persistent context, structured compression, and autonomous maintenance loops. Designed for one knowledge worker; potential applications for sales, PM, and executive roles."
key_entities: ["body system", "autoresearch loop", "gut compression", "aMCC", "habit loop", "Karpathy", "Duhigg", "McKeown"]
action_verbs: ["maintain", "compress", "experiment", "bootstrap", "enforce"]
update_triggers: ["new organ added", "architecture changes", "system shared externally", "compression protocol updated"]
-->
