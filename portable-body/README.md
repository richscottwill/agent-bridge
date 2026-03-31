# Portable Body — Richard Williams

A personal operating system for AI-augmented work. Text files that let any AI platform understand how Richard thinks, works, and operates — enabling cold-start bootstrap in 2-3 hours instead of weeks.

Repository: https://github.com/richscottwill/portable-body

Last synced: 2026-03-31 (Tuesday ad-hoc sync)

---

## Quick Start (Cold Bootstrap)

1. Read `body/body.md` — the map of the whole system
2. Read `body/soul.md` — Richard's identity, principles, voice
3. Read `body/brain.md` — how Richard decides, Five Levels strategy
4. Ask Richard to populate environment-specific context (manager, org, markets, tools)
5. First morning routine runs within 1-2 hours

Estimated bootstrap time: 2-3 hours (vs weeks from scratch).

---

## Architecture

The system uses a body metaphor. Each organ is a self-contained markdown file.

### Body Organs (13 files)
| Organ | File | Function |
|-------|------|----------|
| Body Map | `body/body.md` | Navigation layer — what each organ does, when to read it |
| Body Diagram | `body/body-diagram.md` | Mermaid visual architecture of the entire system |
| Soul | `body/soul.md` | Identity, values, voice, How I Build principles |
| Brain | `body/brain.md` | Decision log, principles, Five Levels, leverage framework |
| Eyes | `body/eyes.md` | Market metrics, competitors, predicted questions |
| Hands | `body/hands.md` | Action tracker, dependencies, integrations |
| Memory | `body/memory.md` | Compressed context, relationship graph, references |
| Spine | `body/spine.md` | Bootstrap sequence, directory map, key IDs |
| Heart | `body/heart.md` | Autoresearch loop protocol, experiment queue |
| Device | `body/device.md` | Automation, delegation, templates, tool factory |
| Nervous System | `body/nervous-system.md` | Calibration loops, pattern tracking, system health |
| aMCC | `body/amcc.md` | Willpower engine, streak, resistance taxonomy |
| Gut | `body/gut.md` | Compression protocol, word budgets, bloat detection |

### Voice (6 files)
| File | Content |
|------|---------|
| `voice/richard-writing-style.md` | Core voice traits, audience tiers, drafting checklist |
| `voice/richard-style-email.md` | Email patterns (operational, analytical, coordination) |
| `voice/richard-style-slack.md` | Slack messaging (rapid-fire, per-contact registers) |
| `voice/richard-style-docs.md` | Long-form docs (experiments, testing plans, OP1) |
| `voice/richard-style-wbr.md` | WBR weekly callout style |
| `voice/richard-style-mbr.md` | MBR monthly summary style |

### Steering (6 files)
| File | Content |
|------|---------|
| `steering/rw-trainer.md` | Performance coaching framework |
| `steering/rw-task-prioritization.md` | 7-layer task prioritization, calendar block rules |
| `steering/morning-routine-experiments.md` | Experiment engine for morning routine optimization |
| `steering/callout-principles.md` | WBR callout writing principles |
| `steering/long-term-goals.md` | The Five Levels strategic arc |
| `steering/architecture-eval-protocol.md` | Blind evaluation protocol for architecture changes |

### Agents (13 files)
| File | Role |
|------|------|
| `agents/karpathy.md` | Autoresearch engine, loop governor, compression scientist |
| `agents/rw-trainer.md` | Deep performance coach |
| `agents/eyes-chart.md` | Visualization specialist |
| `agents/portable-body-maintainer.md` | This sync system |
| `agents/market-analyst.md` | Parameterized WBR market analyst (all 10 markets) |
| `agents/callout-writer.md` | Parameterized WBR callout writer (all 10 markets) |
| `agents/callout-reviewer.md` | Cross-market callout blind reviewer |
| `agents/wiki-editor.md` | Wiki pipeline orchestrator |
| `agents/wiki-researcher.md` | Wiki research agent |
| `agents/wiki-writer.md` | Wiki writing agent |
| `agents/wiki-critic.md` | Wiki quality gate |
| `agents/wiki-librarian.md` | Wiki publishing agent |
| `agents/wiki-concierge.md` | Wiki search/lookup agent |

### Hooks (1 file)
| File | Content |
|------|---------|
| `hooks/hooks-inventory.md` | Plain-text descriptions of all 10 automation hooks with portable intent |

### Research (11 files)
| File | Content |
|------|---------|
| `research/ad-copy-results.md` | Ad copy A/B test results |
| `research/competitor-intel.md` | Competitive landscape by market |
| `research/oci-performance.md` | OCI rollout performance data |
| `research/testing-framework-template.md` | OP1 testing framework (5 workstreams) |
| `research/automation-impact/ai-automation-impact.md` | AI automation impact analysis |
| `research/automation-impact/build.py` | Build script for automation impact HTML |
| `research/test-docs/*.md` | 7 historical test documents |

### Tools (9 files)
| File | Content |
|------|---------|
| `tools/ingest.py` | Dashboard data ingester (xlsx → market data briefs) |
| `tools/schema.sql` | DuckDB schema for agent observations, changelog, competitors |
| `tools/query.py` | DuckDB query interface |
| `tools/RECONSTRUCTION.md` | Data layer reconstruction guide |
| `tools/sync.sh` | Git sync script (push shared/ to GitHub) |
| `tools/git-sync-README.md` | Git sync documentation |
| `tools/generate-charts.py` | Progress charts dashboard generator |
| `tools/chart-template.html` | HTML template for chart dashboard |
| `tools/progress-charts-README.md` | Progress charts documentation |

### Specs (22 files across 8 specs)
| Spec | Files | Content |
|------|-------|---------|
| paid-search-daily-audit | requirements, design, tasks | PS audit automation |
| agent-consolidation | requirements, design, tasks | WBR agent consolidation (6→2) |
| agentspaces-desktop-launcher | requirements, design, tasks | Desktop launcher for AgentSpaces |
| attention-tracker | requirements, design, tasks | Attention/focus tracking tool |
| bayesian-prediction-engine | requirements, design, tasks | Bayesian prediction system |
| data-layer-overhaul | requirements, design, tasks | DuckDB data layer migration |
| shared-directory-reorg | requirements | Directory restructuring |
| wiki-sharepoint-sync | requirements, design, tasks | Wiki to SharePoint sync |

### System Files (4 files)
| File | Content |
|------|---------|
| `portable-layer.md` | Architecture manifest — what's portable vs environment-specific |
| `README.md` | This file |
| `CHANGELOG.md` | Version history |
| `SANITIZE.md` | What to strip before sharing publicly |

---

## Total File Count: 87

---

## Key Concepts

- **Doomsday mentality**: If the DevSpace dies tomorrow, this directory has everything needed to rebuild
- **Organs hold current state, not history**: No append-only logs. CHANGELOG.md is the audit trail.
- **Karpathy governs experiments**: The autoresearch loop runs autonomous experiments on organs with orchestrated blind evaluation (4-step: Karpathy → Eval A → Eval B → Karpathy scores)
- **Word budgets are constraints**: Total body budget 23,000w, hard ceiling 24,000w
- **The Five Levels**: Sequential career strategy (Sharpen → Testing → Automation → Zero-Click → Agentic)
- **How I Build principles**: Routine as liberation, Structural over cosmetic, Subtraction before addition, Protect the habit loop, Invisible over visible, Reduce decisions not options
- **Agent consolidation**: WBR callout agents consolidated from 6 per-region to 2 parameterized (market-analyst + callout-writer), reducing duplication while maintaining market-specific behavior via context files

---

## Portability Gaps (flagged for CE-6 experiment)

- File paths reference AgentSpaces-specific locations (`~/shared/context/`, `~/.kiro/steering/`)
- Hook definitions are Kiro JSON format (hooks-inventory.md provides plain-text equivalents)
- Some organs reference MCP tools (Hedy, Outlook) without explaining generic alternatives
- Bootstrap assumes access to email, calendar, and task management APIs
- DuckDB tools (query.py, schema.sql) are infrastructure-specific — the schema is portable but the runtime isn't
- morning-routine-experiments.md source file missing — portable copy may be stale
