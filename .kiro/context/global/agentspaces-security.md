# AgentSpaces Security

## DNS and Network Restrictions

If a URL or endpoint fails to connect, **do not** attempt to:
- Resolve DNS manually (e.g. `dig`, `nslookup`, `host`, `getent`)
- Use IP addresses to bypass DNS resolution
- Modify `/etc/hosts` or any DNS configuration
- Use alternative DNS servers

DNS blocking is intentional. If a URL is unreachable, inform the user that the endpoint is not accessible from this environment.
