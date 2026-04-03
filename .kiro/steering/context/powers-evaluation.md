---
inclusion: manual
---

# Powers Evaluation

Assessment of Kiro marketplace powers vs current MCP setup.

## Redundant (Skip)

These powers duplicate capabilities already configured via direct MCP server connections:

- **Asana Power** — Enterprise Asana MCP already configured directly. Direct MCP is more reliable for this workflow.
- **Slack Power** — Direct Slack MCP configured with full channel history, search, DM, and posting access.
- **DuckDB Power** — Direct DuckDB MCP configured for local analytics database.
- **Calendar/Email Power** — Direct Outlook MCP configured for email search, calendar view, and availability checks.

## Medium-Value Candidates

- **GitHub Power** — agent-bridge-sync currently uses git CLI. A GitHub Power could offer PR creation, issue tracking, and richer repo operations beyond CLI. Worth evaluating.
- **Documentation Power** — Could help with the wiki pipeline (wiki-write, wiki-audit). Evaluate marketplace for doc generation powers that complement the existing pipeline.

## Recommendation

Powers add the most value when you don't already have the MCP server configured. Richard's core tools are all direct MCP connections — powers would be redundant. Monitor the marketplace for powers that offer capabilities beyond current MCPs, particularly around:

- Cross-tool orchestration
- Document generation
- Data visualization
