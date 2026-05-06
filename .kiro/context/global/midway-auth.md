# Midway Authentication

**For any HTTP request to a Midway-protected endpoint, use `mcscli curl` instead of `curl`:**
```bash
mcscli curl -s "https://example.amazon.com/api/endpoint"
```

`mcscli curl` handles Midway auth automatically via client cert — no cookie file, no `mwinit` session required. It accepts the same flags as `curl`.

**When a service requires a Bearer JWT (OIDC id_token):**
```bash
NONCE=$(uuidgen)
JWT=$(mcscli curl -s "https://midway-auth.amazon.com/SSO?response_type=id_token&client_id=<CLIENT_ID>&redirect_uri=<REDIRECT_URI>&scope=openid&nonce=$NONCE")
```
- The `client_id` is typically the service's UI hostname (e.g. `ui.example.aws.dev`), not the API hostname.
- The `redirect_uri` usually matches `https://<client_id>`.
- If unknown, search the service's source code or documentation for `midway-auth.amazon.com/SSO` or `client_id` to find the correct values.
- JWTs expire in ~5 minutes. Refresh before each batch of requests.

## ~/.midway/cookie does not exist by default

AgentSpaces uses shared Midway authentication via MCS (MidwayClientSuite). The `~/.midway/cookie` file does not exist by default. If a tool or MCP server fails because it depends on `~/.midway/cookie`:

1. **Tell the user** they can click the **⋯ (triple dot) menu** on the chat input box and select **Refresh Midway** to force-create the cookie file inside the space.
2. **Recommend the user contact the MCP/tool maintainer** and ask them to migrate from `~/.midway/cookie` to MCS (`mcscli curl`). The cookie file is being deprecated.
3. **Link to MCS onboarding docs:** [MCS Onboarding](https://w.amazon.com/bin/view/MidwayClientSuite/Onboarding/) — includes an AI agent that can automate the migration.

## Never run mwinit

AgentSpaces uses shared Midway via MCS. Running `mwinit` (including `mwinit -o` or `mwinit --pre-register`) will break authentication. The agent must never attempt to run mwinit itself.
