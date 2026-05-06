# Code Agent Specific Rules

## Purpose

- Deliver production-ready results with existing Brazil packages
- Focus on building, testing, and deploying real solutions
- Leverage Amazon's development ecosystem effectively
- Ensure code quality and production readiness

## Pre-existing Workspace

The workspace may already exist at `~/.workspace`. If it does, use it directly instead of creating a new one. Also prefer reading and browsing code from this local workspace rather than fetching from remote sources like code.amazon.com.

## Brazil Integration

- Must navigate to specific package directories before building
- Always run `brazil-build release` to verify changes
- Follow Brazil workspace and package structure conventions
- Use `brazil workspace merge` for dependency resolution

## Code Review Process

- Always commit changes before creating CRs
- Check for `.crux_template.md` and use if present
- Verify branch sync status before raising CRs
- Follow conventional commit message format
- When using CRRevisionCreator, invoke the cr-tagging skill for required tags

## Development Standards

- Follow Amazon's coding standards and best practices
- Ensure proper error handling and logging
- Write maintainable, production-quality code
- Include appropriate documentation and comments

## MCP Integration

- Leverage builder-mcp server for internal Amazon resources
- Use internal search capabilities for documentation and examples
- Access Amazon-specific tooling and information through MCP
