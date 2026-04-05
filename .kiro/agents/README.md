# Agent Directory

## Structure

```
agents/
├── body-system/          # .md definitions (source of truth for agent behavior)
│   ├── karpathy.md       # Autoresearch engine, organ experiments, compression
│   ├── rw-trainer.md     # Deep performance coach
│   ├── eyes-chart.md     # Visualization / dashboard generator
│   └── agent-bridge-sync.md  # Sync to agent-bridge GitHub repo (files + git push)
│
├── wbr-callouts/         # .md definitions (source of truth for agent behavior)
│   ├── market-analyst.md     # Any-market analysis briefs (replaces abix/najp/eu5 analysts)
│   ├── callout-writer.md     # Any-market callout drafts (replaces abix/najp/eu5 writers)
│   └── callout-reviewer.md   # Cross-market quality gate
│
├── wiki-team/            # .md definitions (source of truth for agent behavior)
│   ├── wiki-editor.md        # Editorial director, orchestrates the pipeline
│   ├── wiki-researcher.md    # Gathers source material, produces research briefs
│   ├── wiki-writer.md        # Transforms briefs into dual-audience articles
│   ├── wiki-critic.md        # Quality gate + periodic decay audits
│   ├── wiki-librarian.md     # Publishes, structures, maintains the index
│   └── wiki-concierge.md     # Search, proactive surfacing, demand tracking
│
├── *.json                # CLI-invocable JSON configs (all agents)
│   ├── karpathy.json         # ✅ Tested 2026-04-05
│   ├── rw-trainer.json       # ✅ Tested 2026-04-05
│   ├── eyes-chart.json       # ✅ Tested 2026-04-05
│   ├── agent-bridge-sync.json # ✅ Tested 2026-04-05
│   ├── market-analyst.json   # ✅ Tested 2026-04-05
│   ├── callout-writer.json   # ✅ Tested 2026-04-05
│   ├── callout-reviewer.json # ✅ Tested 2026-04-05
│   ├── wiki-editor.json      # ✅ Tested 2026-03-31
│   ├── wiki-writer.json      # ✅ Tested 2026-03-31
│   ├── wiki-critic.json      # ✅ Tested 2026-03-31
│   ├── wiki-researcher.json  # ✅ Tested 2026-03-31
│   ├── wiki-librarian.json   # ✅ Tested 2026-03-31
│   ├── wiki-concierge.json   # ✅ Tested 2026-03-31
│   ├── AIPowerUserCapabilities-gpu-*.json  # GPU Power User suite (AIM-managed)
│   ├── AmazonBuilderCoreAIAgents-amzn-builder.json (AIM-managed)
│   ├── AtlasAICapabilities-atlas.json (AIM-managed)
│   ├── local-arcc-*.json     # ARCC pilot agents (AIM-managed)
│   ├── agentspaces-chat.json # Platform: Chat agent
│   ├── agentspaces-code.json # Platform: Code agent
│   └── title-generator.json  # Utility: conversation titles
│
└── agent_config.json.example  # Template for new JSON agents
```

## CLI invocation

All custom agents are invocable via:
```bash
echo "your prompt" | kiro-cli chat --agent <name> --no-interactive --trust-all-tools --wrap never
```

The `.md` files in subdirectories remain the source of truth for agent behavior. The `.json` configs at root point to them via `resources` and load their full instructions at runtime.

## Why this layout

- `.md` definitions live in subfolders by team/function — these are the canonical agent specs
- `.json` configs at root make agents discoverable by kiro-cli (which does not recurse into subdirectories)
- Each `.json` references its `.md` via the `resources` field — no duplication of instructions
- AIM-managed agents say "DO NOT EDIT MANUALLY" — don't move or rename them

## Where to put new agents

| Agent type | Location |
|-----------|----------|
| Body system (coaching, experiments, visualization, sync) | `.md` in `body-system/`, `.json` at root |
| WBR callout pipeline (analyst, writer, reviewer) | `.md` in `wbr-callouts/`, `.json` at root |
| Wiki team (editor, researcher, writer, critic, librarian, concierge) | `.md` in `wiki-team/`, `.json` at root |
| AIM-managed (installed via `aim`) | Root (automatic) |
| Platform / utility JSON agents | Root |
| New custom agent | `.md` in appropriate subfolder, `.json` at root |

## Callout pipeline execution order

```
analyst → writer → reviewer
```

Run the region's analyst first, then writer, then callout-reviewer across all markets. See soul.md Agent Routing Directory for the full routing table.

## Wiki pipeline execution order

```
editor (decides topic)
  → researcher (gathers material)
    → writer (drafts article)
      → critic (reviews)
        → editor (publish/revise/kill decision)
          → librarian (publishes, updates index)

concierge (always available — answers questions, tracks demand)
```

The editor orchestrates. The concierge runs independently as the reader-facing search layer. Demand signals from the concierge feed back into the editor's roadmap.

Wiki content lives at `~/shared/context/wiki/` with subdirectories for each pipeline stage: `research/`, `staging/`, `reviews/`, `published/`, `archive/`, `audits/`, `health/`.
