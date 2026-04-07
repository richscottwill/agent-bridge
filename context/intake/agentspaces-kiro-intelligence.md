<!-- DOC-0165 | duck_id: intake-agentspaces-kiro-intelligence -->
# AgentSpaces & Kiro Intelligence — from Slack Scan

Source: `#agentspaces-interest` (C0A1JD8FCUV), `#amazon-builder-genai-power-users` (C08GJKNC3KM)
Scanned: 2026-04-02
Method: Slack search for "agentspaces-interest" — 131 results, page 1 (top 20)

## Key Channels to Monitor
- **agentspaces-interest** (C0A1JD8FCUV): Primary support + feature discussion. Very active. Mostly troubleshooting but has product announcements and power-user tips.
- **amazon-builder-genai-power-users** (C08GJKNC3KM): Cross-org GenAI announcements. AgentSpaces updates posted here.

## Actionable Intelligence

### AgentSpaces Build/Test Fixing (Open Preview, Feb 2026)
- AI-powered build and integration test fixing via AgentSpaces
- One-click "Fix with AgentSpaces" button on build.amazon.com and tod.amazon.com
- ~700 builders used it last week to troubleshoot ~1k failing builds
- Supervised workflow: workspace creation → package checkout → failure investigation → code changes → local validation → CR creation
- builder-mcp integration for additional context

### Known Issues (for Richard's awareness)
- **Spaces stuck in initialization**: Common issue. Requires admin to manually set space to "stopped" state. Self-service troubleshooting doesn't work. Post space ID in channel for fastest resolution.
- **DevSpaces credential chain**: AWS_CONTAINER_CREDENTIALS_FULL_URI takes priority over ADA credentials. Fix: write ADA creds to ~/.aws/credentials. Agent should handle this automatically but currently gives up.
- **MCP config split**: Chat agent and CLI agent use separate config paths (/agentspaces/.aws/amazonq/mcp.json vs .kiro/settings/mcp.json). Known quirk — confusing that they don't share the same MCP config.
- **Certificate issues**: Multiple cert creation from dual browser windows. Fix: mwinit -o --preregister in Kiro CLI Terminal.
- **Mobile access**: Start space on laptop first, then switch to mobile. AEA Browser needs "Allow Cross-Website Tracking" enabled. YubiKey on iOS takes over keyboard — type password first.

### AgentSpaces Features (current as of March 2026)
- Kiro CLI integration (fully transitioned)
- Shared Kiro login across spaces
- AIM package support (custom agents via URL params: mode=CUSTOM&aimPackageName=X&customAgentName=Y)
- Agent swap (context preserved when switching)
- Planning mode toggle
- Persistent terminal (Ctrl+T)
- Stream reconnection (navigate away, come back)
- Deep-linking & space reuse
- Proxy URLs for web apps: https://ds-{spaceId}--{port}.{region}.prod.proxy.devspaces.amazon.dev
- Storage persistent in ~/ directory
- Auto-stop after ~24h inactivity
- L4+ employees have access by default. L1-L3 need manager to add to kiro-subscription-aws-misc or kiro-subscription-sdo-misc

### Relevance to Richard's Work
- **Level 3 (Team Automation)**: The build/test fixing workflow is a model for what Richard could propose for PS workflows. "One-click fix" pattern could apply to campaign anomaly detection.
- **Level 5 (Agentic Orchestration)**: The deep-linking + AIM package pattern enables triggering specialized agents from external tools. Could be used for PS workflow automation.
- **Practical**: The MCP config split and credential chain issues are things Richard should know about for his own AgentSpaces usage.

## Not Worth Ingesting to DuckDB
The channel is 90% support tickets from other teams (stuck spaces, auth issues). Not relevant to PS team context. Better to scan periodically for product announcements and power-user tips.
