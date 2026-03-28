# Sanitization Guide

What to strip before sharing the portable body publicly or with a new employer.

---

## By File Type

### Body Organs
| File | Strip | Keep |
|------|-------|------|
| soul.md | Employer, team, org chain, market list, Amazon-specific systems | Identity, How I Build principles, voice preferences, agent instructions |
| brain.md | Amazon decision log (D1-D10), OP1 positions, market-specific data | Decision principles 1-7, Five Levels structure, leverage framework |
| amcc.md | Current streak data, current hard thing, Amazon-specific task references | Willpower model, streak system, resistance taxonomy, escalation ladder |
| gut.md | Current intake backlog, current word counts | Compression protocol, word budgets, digestion protocol, bloat detection |
| heart.md | Current experiment queue, Amazon-specific experiment results | Loop architecture, experiment protocol, hyperparameters |
| nervous-system.md | Current scoring data, Amazon-specific pattern tracking, calibration history | All 9 loop definitions, scoring methods, graduation criteria |
| device.md | Amazon-specific delegations, To-Do IDs, Outlook IDs, current tool statuses | Installed apps architecture, delegation protocol structure, tool factory framework |
| memory.md | All Amazon contacts, all meeting briefs, all reference links | Relationship graph structure, meeting prep template structure |
| hands.md | All current tasks, all Amazon-specific IDs and links | Task list structure, recurring task framework |
| spine.md | All Amazon IDs, all tool access details, all Quip links | Bootstrap sequence structure, directory map concept |
| eyes.md | All current market data, all Amazon-specific metrics | Market health table structure, competitive landscape framework |
| body.md | Nothing (fully portable) | Organ map, operating principles, task routing |

### Voice Files
All voice files are fully portable — they ARE Richard. No stripping needed.

### Steering Files
| File | Strip | Keep |
|------|-------|------|
| rw-trainer.md | Amazon-specific pattern examples, people/projects | Coaching framework, mediocrity detection, interaction rules |
| rw-task-prioritization.md | Nothing (mostly portable) | 7-layer prioritization, capacity guardrails, backlog rules |
| morning-routine-experiments.md | Current experiment data, run logs | Experiment engine framework, scoring guide, research priors |
| callout-principles.md | Nothing (methodology is portable) | All callout writing principles |
| long-term-goals.md | Nothing (fully portable) | The Five Levels strategic arc |

### Agent Files
Agent definitions contain methodology (portable) and Amazon-specific references (strip). The methodology — how to analyze markets, write callouts, coach performance, run experiments — is the valuable part.

### Research Files
Research files contain Amazon Business data. Strip the specific numbers but keep the methodology and framework structure.

### Hooks
hooks-inventory.md is already plain-text intent descriptions. No stripping needed — the intent is portable even if the implementation is platform-specific.

---

## Process

1. Make a copy of the entire portable-body/ directory
2. For each file, apply the strip/keep rules above
3. Replace Amazon-specific content with placeholder comments: `<!-- ENVIRONMENT-SPECIFIC: populate with your employer's data -->`
4. Keep the structure intact — a new AI should understand what goes where even with placeholders
5. Test: paste body.md + soul.md + brain.md into ChatGPT. Can it answer "What should Richard work on today?" If yes, the sanitized version works.
