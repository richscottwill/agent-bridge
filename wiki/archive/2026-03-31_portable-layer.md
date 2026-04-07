<!-- DOC-0112 | duck_id: context-2026-03-31_portable-layer -->
# Portable Layer — System Architecture Manifest

What travels with Richard vs what stays with the environment. Updated whenever the system structure changes.

Last updated: 2026-03-24

---

## Portable (Richard owns this regardless of employer)

These files contain the ARCHITECTURE — how the system works, how Richard operates, his principles, his voice. Strip Amazon-specific content before export.

### Core System (the body)
| File | What's Portable | What to Strip |
|------|----------------|---------------|
| body.md | Organ map, operating principles, task routing | — (fully portable) |
| soul.md | Identity, How I Build principles, voice preferences, agent instructions | Employer, team, org chain, market list, Amazon-specific systems |
| brain.md | Decision principles 1-7, Five Levels structure, leverage framework, prediction template | Amazon decision log (D1-D10), OP1 positions, market-specific data |
| amcc.md | Willpower model, streak system, resistance taxonomy, escalation ladder, intervention protocol | Current streak data, current hard thing, Amazon-specific task references |
| gut.md | Compression protocol, word budgets, digestion protocol, bloat detection, excretion rules | Current intake backlog, current word counts |
| heart.md | Loop architecture (maintain → cascade → experiment), experiment protocol | Current experiment queue, Amazon-specific experiment results |
| nervous-system.md | All 9 loop definitions (protocols, scoring methods, graduation criteria) | Current scoring data, Amazon-specific pattern tracking, calibration history |
| device.md | Installed apps architecture, delegation protocol structure, tool factory framework, background monitor concepts | Amazon-specific delegations, To-Do IDs, Outlook IDs, current tool statuses |
| memory.md | Relationship graph structure, meeting prep template structure | All Amazon contacts, all Amazon meeting briefs, all Amazon reference links |
| hands.md | Task list structure (Sweep/Core/Engine Room/Admin/Backlog), recurring task framework | All current tasks, all Amazon-specific IDs and links |
| spine.md | Bootstrap sequence structure, directory map concept | All Amazon IDs, all Amazon tool access details, all Amazon Quip links |
| eyes.md | Market health table structure, competitive landscape framework, OCI tracking framework | All current market data, all Amazon-specific metrics |

### Richard's Voice (fully portable — these ARE Richard)
| File | Content |
|------|---------|
| richard-writing-style.md | Core voice traits, audience tier system, drafting checklist, voice evolution |
| richard-style-email.md | Email drafting patterns (operational, analytical, coordination) |
| richard-style-slack.md | Slack messaging (rapid-fire, stream-of-consciousness, per-contact registers) |
| richard-style-docs.md | Long-form docs (experiments, testing plans, investigations, post-mortems, OP1) |
| richard-style-wbr.md | WBR weekly callout style |
| richard-style-mbr.md | MBR monthly summary style |

### System Steering (portable framework, some Amazon-specific examples)
| File | What's Portable | What to Strip |
|------|----------------|---------------|
| rw-trainer.md | Coaching framework, mediocrity pattern detection, interaction rules, morning routine priorities | Amazon-specific pattern examples, Amazon-specific people/projects |
| rw-task-prioritization.md | 7-layer prioritization, capacity guardrails, backlog rules, task management agency, calendar block rules | — (mostly portable) |
| morning-routine-experiments.md | Experiment engine framework, scoring guide, research priors, hypothesis generation triggers | Current experiment data, run logs |
| portable-layer.md | This manifest + bootstrap protocol | — (fully portable) |

### Amazon-Specific Steering (NOT portable)
| File | Why It Stays |
|------|-------------|
| richard-style-amazon.md | Amazon writing norms layer (leadership principles framing) |
| agentspaces-core.md | Amazon DevSpaces/AgentSpaces rules |
| amazon-builder-production-safety.md | Amazon AWS safety rules |
| devspaces-core.md | Amazon DevSpaces boundaries |
| file-creation-rules.md | Amazon workspace file rules |
| process-execution.md | Amazon process execution template |
| context/pilot-steering.md | Amazon ARCC governance |

## Environment-Specific (rebuilt per context)

| File | Why It Stays |
|------|-------------|
| current.md | Live state of current role |
| org-chart.md | Current employer org |
| rw-tracker.md | Current scorecard and patterns |
| asana-sync-protocol.md | Current tool bridge |
| mcp-tool-reference.md | Current tool API docs |
| callouts/ | Current market data |
| intake/ | Current unprocessed material |
| tools/ | Current utility scripts |
| All hook files | Current tool-specific triggers |

## Export Protocol

**Weekly (Friday calibration):**
1. Bundle all portable files into a single email
2. For each file: include the full content (architecture + current data — the current data provides useful examples for bootstrapping a new environment)
3. Send to richscottwill@gmail.com
4. Subject: "System Snapshot — [date]"
5. Body: brief changelog of what changed this week

**For GitHub:**
1. Repo: https://github.com/richscottwill/portable-body
2. Maintain architecture-only versions (Amazon content stripped)
3. After each loop run that modifies a portable file, commit and push
4. README.md explains the system and how to bootstrap a new environment

## Bootstrap Protocol (for a new environment)

When Richard starts in a new context:
1. Clone the portable layer (from GitHub or from the latest email snapshot)
2. The agent reads body.md first — understands the system architecture
3. The agent reads soul.md — understands Richard's identity and principles
4. The agent asks Richard to populate the environment-specific layer:
   - "Who is your manager? What's the org structure?"
   - "What markets/projects are you working on?"
   - "What tools do you have access to? (email, calendar, task manager, etc.)"
   - "Who are your key contacts and what's the tone with each?"
5. The agent creates the environment-specific files from Richard's answers
6. First morning routine runs within 1-2 hours of setup

Estimated bootstrap time: 2-3 hours (vs weeks to build from scratch).
