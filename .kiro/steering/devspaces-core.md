# DevSpaces Core Rules

## Environment Context

- You are operating within Amazon's DevSpaces containerized development environment
- DevSpaces provides isolated, secure workspaces with pre-configured Amazon development tools
- Your workspace is containerized for consistency and reproducibility across all developers

## Workspace Boundaries

- All file operations must be within the `/workspace` directory
- Respect containerized environment isolation and security boundaries
- Do not attempt to access or modify system files outside your designated workspace

## Pre-configured Tooling

- Brazil build system is available and pre-configured
- CRUX and other Amazon internal development tools are ready to use
- Leverage existing tool configurations rather than attempting manual installations
- Use containerized tools for consistent development experience

## Development Workflow

- Work within the established container boundaries
- Utilize pre-configured Amazon development tools and processes
- Maintain consistency with Amazon's development standards and practices
- Follow containerized development best practices

## Integration

- DevSpaces integrates seamlessly with AgentSpaces (Chat and code modes)
- Coordinate with other Amazon development systems and workflows
- Respect the containerized architecture for security and isolation
