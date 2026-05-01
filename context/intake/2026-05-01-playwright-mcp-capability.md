# Capability note: Playwright MCP Bridge on kiro-local

**Date added:** 2026-05-01
**Environment:** kiro-local (Windows Kiro IDE, Richard''s main machine)
**Added by:** kiro-local, in conversation with Richard

## What this unlocks

kiro-local can now drive Richard''s real authenticated Chrome browser via the Microsoft Playwright MCP Bridge extension. This means direct access to any Midway-protected surface without cookie juggling, mwinit scripting, or separate headless sessions.

Verified working against Amazon Quick (QuickSight) Spaces on the day this note was written.

## What''s addressable

Any Midway-protected or authenticated page in Richard''s Chrome profile, including:

- Amazon Quick (QuickSight) — Spaces, dashboards, analyses, datasets
- Internal wikis (w.amazon.com)
- Paragon, SharePoint, Outlook Web, Slack Web
- Google Ads UI (logged in via Amazon SSO)
- Any other internal tool that Richard is already signed into

The extension inherits Richard''s authenticated session from whatever Chrome profile it was installed into. No separate auth flow.

## Architecture

```
Kiro (kiro-local)
  +- MCP client
       +- playwright-mcp server (npx @playwright/mcp@latest --extension)
            +- WebSocket bridge on localhost
                 +- Playwright MCP Bridge Chrome extension
                      +- Attached tab in Richard''s real Chrome
```

Server is spawned on-demand by Kiro via npx. The extension connects to it using `PLAYWRIGHT_MCP_EXTENSION_TOKEN` stored in the MCP config.

## Config location

`~/.kiro/settings/mcp.json` — entry named `playwright-mcp`. Token lives in `env.PLAYWRIGHT_MCP_EXTENSION_TOKEN`. Backup saved at `~/.kiro/settings/mcp.json.bak-<timestamp>` from the original install.

`chrome-devtools-mcp` is disabled in favor of this — they collide on `browser_*` tool names, and Playwright''s accessibility-tree API is cleaner than raw CDP.

## Operating rules

These are behavioral, not enforced by the tooling. kiro-local follows them; when reading this note, honor them.

1. **Always start a browsing session with `browser_tabs action=new`.** Never operate on a tab Richard opened. The agent works only in tabs it opened itself.

2. **One attached tab at a time.** The extension model enforces this — whichever tab the extension is attached to is the only tab addressable. The agent should not try to bulk-navigate across tabs.

3. **If Richard points at a specific tab or URL he has open, treat it as explicit permission** for a one-off interaction with that surface. Revert to rule 1 for the next task.

4. **Watch for extension-disconnect errors.** If a tool call fails with a connection error, the extension has probably disconnected (tab closed, Chrome restarted, token mismatch). Don''t retry blindly — tell Richard so he can reattach.

5. **Don''t run destructive actions without confirmation.** Clicking "Delete", submitting forms that create/modify records, uploading files to production surfaces — all require explicit Richard approval per the safety rules. Browsing and reading is free; writing isn''t.

## Non-interference contract (for Richard)

Richard can keep using his browser normally while the agent works. The only actions that disturb the agent:

- Closing the agent''s attached tab
- Clicking the Playwright MCP Bridge extension icon to detach or reattach elsewhere
- Navigating the agent''s attached tab via the address bar
- Closing Chrome

Visual signal: the extension icon lights up on its attached tab. If it''s lit, that tab is the agent''s — leave it alone.

## Cross-environment routing (for kiro-server)

**kiro-server cannot do this.** The extension lives in Richard''s local Chrome; DevSpaces has no way to reach it. When a task requires:

- Pulling live state from a Midway-protected dashboard
- Scraping a wiki page, SharePoint doc, or Quick analysis
- Driving Google Ads UI or any web-based internal tool
- Verifying what an internal page currently renders

...tell Richard the task needs kiro-local. Don''t silently fall back to fetching the URL server-side (that hits the Midway login wall) or guessing from stale cached data.

Conversely, kiro-local should defer to kiro-server for tasks that require DuckDB (ps-analytics), long-lived shared context access, hook execution, or agent orchestration.

## Five Levels fit

- **Level 2 (Drive WW Testing)** — can pull live test status from Quick dashboards without manual export
- **Level 3 (Team Automation)** — if the agent can reliably read Quick/wiki/Google Ads, it becomes a tool worth building workflows around for teammates
- **Level 5 (Agentic Orchestration)** — bridge-level capability for PS workflows that need live web state

## Known limits

- Chrome profile only (the one where the extension is installed; Richard''s main profile at time of install)
- One attached tab at a time; parallel browsing requires sequential attachment
- Full-page screenshots cause visible scroll on the attached tab
- Token rotates if the extension is reinstalled — config needs updating

## When to consider upgrading

If/when a workflow needs multi-tab parallelism, a dedicated Chrome profile, or headless CI-style automation, revisit. For now, single-session browsing against Richard''s real auth is the right shape.

