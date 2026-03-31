---
name: cr-tagging
description: Tag code reviews created via CRRevisionCreator with agent metadata (author, platform, space-id, agent-name, model). Invoke when creating or updating a CR.
---

# CR Tagging

## When to Use

Invoke this skill when creating or updating a code review using the CRRevisionCreator tool.

## Required Tags

Always include in the `tags` parameter:
- `author.agentic`
- `platform.AgentSpaces`

## Conditional Tags

Include when values are non-empty:
- `space-id.{SPACE_ID}` — from `/agentspaces/space.json` field `id`
- `agent-name.{AGENT_NAME}` — from `/agentspaces/space.json` field `agentName`
- `model.{MODEL}` — from `~/.kiro/agents/{agentName}.json` field `model`

## Metadata Collection

1. Check if `/agentspaces/space.json` exists
2. If it exists, extract `id` and `agentName`
3. If `agentName` is found and not "null", look up `~/.kiro/agents/{agentName}.json` for the `model` field
4. Only include tags whose values are non-empty

## Tag Format Rules

- Tags use `name.value` format
- Values must match `[a-zA-Z0-9.-]+` (max 30 chars per tag)
- Replace invalid characters (underscores, colons, spaces) with dashes
- Truncate to 30 characters if exceeded

## Example

```json
{
  "workingDirectory": "/workspace/src/MyPackage",
  "packageNames": ["MyPackage"],
  "tags": ["author.agentic", "platform.AgentSpaces", "space-id.as-abc123xyz", "agent-name.code", "model.claude-sonnet-4"]
}
```
