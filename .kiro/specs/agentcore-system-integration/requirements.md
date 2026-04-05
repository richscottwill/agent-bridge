# Requirements Document

## Introduction

This document specifies the requirements for integrating AWS Bedrock AgentCore services into Richard's existing productivity system ("The Body"). AgentCore offers five services — Browser, Runtime, Code Interpreter, Memory, and Gateway — each addressing specific limitations in the current DevSpaces-based architecture: container recycling kills persistent processes, no cron/scheduling exists, WorkDocs requires browser auth that CLI agents cannot perform, and context window limits constrain overnight agent runs. The spec evaluates which AgentCore services add real value versus which are redundant with the current system, and proposes an integration roadmap. This is Level 5 (Agentic Orchestration) work — the first step toward PS workflows running without human intervention.

Current blocker: AgentCore requires an internal AWS account (Isengard). The current auth uses external account 729628724606. Browser session creation succeeded but resource provisioning returned 404. All requirements assume this blocker is resolved.

## Glossary

- **AgentCore**: AWS Bedrock AgentCore — a managed service providing Browser, Runtime, Code Interpreter, Memory, and Gateway capabilities for AI agents
- **AgentCore_MCP**: The MCP server (`awslabs.amazon-bedrock-agentcore-mcp-server`) that exposes AgentCore services as tools within Kiro
- **Browser_Service**: AgentCore Browser — cloud-hosted Chrome in Firecracker microVMs for web automation, capable of Midway-authenticated browsing
- **Runtime_Service**: AgentCore Runtime — serverless agent deployment with scheduling, independent of DevSpaces container lifecycle
- **Code_Interpreter_Service**: AgentCore Code Interpreter — sandboxed execution environment for Python, DuckDB queries, and data analysis
- **Memory_Service**: AgentCore Memory — persistent knowledge store across sessions, surviving container recycling
- **Gateway_Service**: AgentCore Gateway — API-to-tool transformation layer that exposes REST APIs as agent-callable tools
- **Body_System**: Richard's 11-organ context management architecture (brain, eyes, hands, memory, spine, heart, device, nervous-system, amcc, gut, body.md)
- **Organ_System**: The file-based context files in `~/shared/context/body/` that constitute the Body_System
- **WBR_Pipeline**: The Monday WBR callout pipeline — polls for new dashboard, ingests data, runs callout generation across 10 markets
- **Karpathy_Loop**: The autoresearch experiment loop that runs overnight, applying and evaluating changes to body organs and style guides
- **Morning_Routine**: The AM-1 → AM-2 → AM-3 sequential hook chain that runs each morning for ingestion, triage, and briefing
- **DevSpaces_Container**: The Amazon DevSpaces containerized environment where the current system runs; subject to recycling
- **Isengard_Account**: An internal Amazon AWS account required for AgentCore resource provisioning
- **WorkDocs_Dashboard**: The AB SEM WW Dashboard xlsx hosted on Amazon WorkDocs, requiring browser-based Midway authentication to download
- **Midway_Auth**: Amazon's internal authentication system requiring browser-based session establishment
- **Agent_Bridge**: The Google Sheets/Docs async message bus for cross-platform context sharing (`~/shared/tools/bridge/bridge.py`)
- **Kiro_CLI**: The CLI agent runner (`/agentspaces/kiro-cli/kiro-cli`) used for non-interactive agent invocations

## Requirements
