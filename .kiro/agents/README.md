# Agent Directory

## Structure

```
agents/
├── body-system/          # Richard's personal operating system agents
│   ├── karpathy.md       # Autoresearch engine, organ experiments, compression
│   ├── rw-trainer.md     # Deep performance coach
│   ├── eyes-chart.md     # Visualization / dashboard generator
│   ├── agent-bridge-sync.md  # Sync to agent-bridge GitHub repo (files + git push)
│   └── loop-governor.md  # (reserved) Loop execution governance
│
├── wbr-callouts/         # WBR callout pipeline (analyst → writer → reviewer)
│   ├── abix-analyst.md       # AU/MX analysis briefs
│   ├── abix-callout-writer.md
│   ├── najp-analyst.md       # US/CA/JP analysis briefs
│   ├── najp-callout-writer.md
│   ├── eu5-analyst.md        # UK/DE/FR/IT/ES analysis briefs
│   ├── eu5-callout-writer.md
│   └── callout-reviewer.md   # Cross-market quality gate
│
├── wiki-team/            # Wiki management pipeline (6 agents)
│   ├── wiki-editor.md        # Editorial director, orchestrates the pipeline
│   ├── wiki-researcher.md    # Gathers source material, produces research briefs
│   ├── wiki-writer.md        # Transforms briefs into dual-audience articles
│   ├── wiki-critic.md        # Quality gate + periodic decay audits
│   ├── wiki-librarian.md     # Publishes, structures, maintains the index
│   └── wiki-concierge.md     # Search, proactive surfacing, demand tracking
│
├── *.json                # AIM-managed + platform agents (flat, DO NOT move)
│   ├── AIPowerUserCapabilities-gpu-*.json  # GPU Power User suite
│   ├── AmazonBuilderCoreAIAgents-amzn-builder.json
│   ├── AtlasAICapabilities-atlas.json
│   ├── local-arcc-*.json     # ARCC pilot agents
│   ├── agentspaces-chat.json # Platform: Chat agent
│   ├── agentspaces-code.json # Platform: Code agent
│   └── title-generator.json  # Utility: conversation titles
│
└── agent_config.json.example  # Template for new JSON agents
```

## Why this layout

- `.md` subagents (invoked by name via Kiro IDE) live in subfolders by team/function
- `.json` agents (discovered by kiro-cli from flat directory) stay at root — kiro-cli does not recurse into subdirectories
- AIM-managed agents say "DO NOT EDIT MANUALLY" — don't move or rename them

## Where to put new agents

| Agent type | Location |
|-----------|----------|
| Body system (coaching, experiments, visualization, sync) | `body-system/` |
| WBR callout pipeline (analyst, writer, reviewer) | `wbr-callouts/` |
| Wiki team (editor, researcher, writer, critic, librarian, concierge) | `wiki-team/` |
| AIM-managed (installed via `aim`) | Root (automatic) |
| Platform / utility JSON agents | Root |
| New custom .md subagent that doesn't fit above | Create a new subfolder with a clear name |

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
