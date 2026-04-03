---
inclusion: auto
name: "File Creation Rules"
description: "Where to create files: workspace directory, home directory, shared folder for persistence"
---

# File Creation Rules

## Where to Create Files

Create files in these locations based on purpose:

- **Workspaces** (`/workspace/**`): For active development work, temporary files, and project-specific content
- **Home directory** (`~/**`): For personal configurations and user-specific files
- **Shared folder** (`~/shared/**`): For files that need to persist across sessions or be shared between different AgentSpaces

## Guidelines

- Use workspace for current task files
- Use shared folder for files that should persist beyond the current session
- Use home directory for personal configurations
- Always consider file lifecycle and sharing needs when choosing location
