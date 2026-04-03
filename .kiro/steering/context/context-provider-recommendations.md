---
inclusion: manual
---

# Context Provider Recommendations

Recommendations for using Kiro context providers to load information into chat more efficiently.

## Providers

- **#url** — Pull Quip docs, wiki pages, SharePoint content into chat. Eliminates manual copy-paste for referenced documents.
  - Example: `#url https://quip-amazon.com/...`

- **#mcp** — Inspect available MCP tools and parameters. Useful when building new hooks or debugging tool calls.
  - Example: `#mcp asana` to see all Asana tools and their parameters.

- **#spec** — Load active spec context. Loads requirements + design + tasks for a named spec.
  - Example: `#spec asana-agent-integration` loads the full spec context.

- **#steering** — Reference steering files during meta-work (system optimization, hook design, etc.).
  - Example: `#steering soul.md`

- **#terminal** — Debug hook execution or script failures by including terminal output in chat context.

- **#git diff** — Preview changes before agent-bridge-sync. Shows what files changed and how.
