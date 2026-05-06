# AgentSpaces Environment

## Space Identity

- **Space config:** `/agentspaces/space.json` — contains space ID, mode (chat/code), agent name, environment (beta/gamma/prod)
- **DevSpace ID:** `/etc/devspace/id` or `$DEVSPACE_ID` env var
- **AgentSpace ID:** `$AGENTSPACE_ID` env var

## Accessing Services Running in the Space

When a user starts a dev server (e.g. on port 3000), it is accessible via the DevSpaces proxy:
```
https://<DEVSPACE_ID>--<PORT>.<REGION>.<ENV>.proxy.devspaces.amazon.dev
```

The proxy base domain is in `/etc/devspace/http-proxy-base-domain`. Example URL:
```
https://ds-abc123--3000.us-west-2.beta.proxy.devspaces.amazon.dev
```

The user can access running services via the **Connect** button on the chat input.

## File Locations

- `/workspace` — working directory, Brazil workspace root (symlink to `~/.workspace`)
- `~/shared` — persists across sessions and is shared between AgentSpaces
- `/agentspaces/` — AgentSpaces runtime (read-only)
