# Hooks Cookbook

**Doc:** 11
**Audience:** Paid Acquisition teammates + their Kiro agents
**Status:** FINAL
**Last updated:** 2026-04-17

## Environment Awareness (for your agent)

Hooks are the most environment-dependent feature in Kiro. Be explicit with the user:

| Capability | Remote IDE (DevSpaces) | Local IDE (laptop Kiro) | AgentSpaces (chat) |
|---|---|---|---|
| Define hooks in `.kiro/hooks/` | ✅ | ✅ | ❌ No file editor |
| `fileEdited` / `fileCreated` triggers | ✅ Fires when files change in container | ✅ Fires on laptop file changes | ❌ |
| `promptSubmit` triggers | ✅ Per chat session | ✅ Per chat session | ⚠️ Fires but file/shell effects limited |
| `userTriggered` (manual button) | ✅ | ✅ | ⚠️ No button UI in chat |
| Scheduled-style daily automation reliability | ✅ Container persists, runs when user's not online | ⚠️ Only when laptop is on + Kiro is open | ❌ |
| Shell commands in `runCommand` hooks | ✅ | ✅ | ❌ |

**Tell the user in plain language:**
- **Remote IDE:** *"I can set up automated tasks here that run in the background even when you're not working — like a daily morning briefing or a watcher that processes your Adobe data drop each morning."*
- **Local IDE:** *"I can set up automated tasks, but they only run while Kiro is open on your laptop. If you want something to fire overnight or when your laptop is asleep, open your Remote IDE and I'll set it up there instead."*
- **AgentSpaces:** *"Automated background tasks aren't available in this chat. I can walk you through the automation recipes and show you what they'd do, but to actually install them, open your Remote IDE or Kiro on your laptop."*

---

Hooks are how Kiro runs automation for you — on file events, scheduled-style triggers (via `promptSubmit`), or manual click. This is a cookbook, not a tutorial. Copy what you need, adjust file patterns to your setup, done.

Every hook here is safe: no external writes, no auto-sends, all output goes to your self-DM or a local file.

## How hooks work (30-second version)

Hooks live in `.kiro/hooks/` as JSON files. Each has three parts:

- **`when`** — the trigger (fileEdited, fileCreated, promptSubmit, etc.)
- **`then.type`** — either `askAgent` (send a prompt to yourself) or `runCommand` (shell command)
- **`then.prompt`** or **`then.command`** — what to execute

Create hooks via the Kiro IDE Agent Hooks panel, or write the JSON directly.

## 1. Morning brief (promptSubmit)

Fires on your first chat message of the day, pulls a briefing.

**File:** `.kiro/hooks/morning-brief.kiro.hook`

```json
{
  "name": "Morning Brief",
  "version": "1.0.0",
  "when": {
    "type": "promptSubmit"
  },
  "then": {
    "type": "askAgent",
    "prompt": "If this is my first chat message today (before 10am local time), run a morning brief: (1) scan my unread Slack from the last 14 hours grouped by channel, (2) scan my unread Outlook from the last 14 hours, (3) pull today's calendar with one-line briefs for each meeting, (4) list my overdue Asana tasks. Keep it to one screen. If it's not morning or not the first message, skip silently."
  }
}
```

Guardrail: the prompt itself checks whether it's the first message / morning, so it doesn't fire on every chat.

## 2. Adobe daily raw data watcher (fileCreated)

Fires when a new Adobe raw Excel lands in `Kiro-Drive/raw-data/`, processes it, appends to pacing dashboard.

**File:** `.kiro/hooks/adobe-daily-watch.kiro.hook`

```json
{
  "name": "Adobe Daily Data Watch",
  "version": "1.0.0",
  "when": {
    "type": "fileCreated",
    "patterns": ["**/raw-data/adobe-*.xlsx"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "A new Adobe daily raw file was dropped. Download it from OneDrive, parse the campaign-level regs/clicks/spend/CPA columns, compute day-over-day deltas, append a row to ps-pacing-dashboard.xlsx on the DailySummary sheet (match the schema), and then post a 5-bullet summary of the biggest movers to my self-DM in Slack. Do not send anywhere else."
  }
}
```

Requires: SharePoint MCP + Slack MCP installed, `data-analysis.md` steering loaded.

## 3. Dashboard refresh on Excel edit (fileEdited)

When the WW dashboard Excel is updated, regenerate derivative dashboards.

**File:** `.kiro/hooks/dashboard-refresh.kiro.hook`

```json
{
  "name": "Dashboard Refresh on WW Update",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["**/Kiro-Drive/D*AB SEM WW Dashboard*.xlsx"]
  },
  "then": {
    "type": "runCommand",
    "command": "python3 ~/shared/dashboards/refresh-all.py"
  }
}
```

Adjust the command to your dashboard refresh script.

## 4. Callout linter (fileEdited)

When you save a callout markdown file, lint it against team principles.

**File:** `.kiro/hooks/callout-linter.kiro.hook`

```json
{
  "name": "Callout Linter",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["**/callouts/**/*.md"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Check this callout against ~/shared/wiki/agent-created/callout-principles.md (or the equivalent principles doc). Flag: missing so-what, weak data, unclear ask, wrong register. Don't rewrite — just flag. Post findings inline."
  }
}
```

Requires: `callout-principles.md` exists. If you don't have one yet, skip this hook.

## 5. Weekly retrospective (userTriggered)

A button you click Friday afternoon to run your weekly retro.

**File:** `.kiro/hooks/weekly-retro.kiro.hook`

```json
{
  "name": "Weekly Retrospective",
  "version": "1.0.0",
  "when": {
    "type": "userTriggered"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Run my weekly retro. Pull: (1) Asana tasks I completed this week grouped by project, (2) meetings I had with one-line notes on each, (3) Slack messages I sent grouped by topic, (4) emails I replied to (subject + recipient). Then suggest: what was high-leverage this week, what was low-leverage, what should I drop or delegate next week. Save the output to ~/shared/retrospectives/YYYY-WW.md."
  }
}
```

Fires when you click the hook in the IDE panel. No auto-trigger.

## 6. Wiki suggestion intake (fileCreated)

When you drop a markdown file in `~/shared/wiki/intake/suggestions/`, auto-tag it and notify self.

**File:** `.kiro/hooks/wiki-suggestion-intake.kiro.hook`

```json
{
  "name": "Wiki Suggestion Intake",
  "version": "1.0.0",
  "when": {
    "type": "fileCreated",
    "patterns": ["**/shared/wiki/intake/suggestions/*.md"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "A new wiki suggestion was dropped. Read it, tag it with the target article path, submitter alias, and date in a front-matter block if missing, then post a one-line summary to my self-DM so I remember to review it."
  }
}
```

## 7. Hook output to self-DM only (pattern)

Any hook that summarizes state should end with "post to my self-DM" — never to channels, never to shared docs without review. Example baseline:

```
...your analysis prompt...
...end with: "Post the summary to my Slack self-DM. Do not post to any channel. Do not send email."
```

## Anti-patterns (don't do these)

- **Don't chain writes to canonical files in a hook.** A fileCreated hook firing on an Adobe drop should only append to one log — not update five files. Keep hooks single-responsibility.
- **Don't use hooks to auto-send external communication.** The hard rule applies. If a hook drafts an email or Slack message, it stops at draft.
- **Don't build hooks that run on every promptSubmit.** Every single chat message will fire them. Use guardrail logic (check time, check conditions) in the prompt, or use `fileEdited` / `userTriggered`.
- **Don't forget to test with a manual trigger first.** Hooks that misfire eat context budget fast.

## Debugging hooks

- Hook didn't fire? Check the patterns. `**/foo.md` matches any depth. `foo.md` matches only root.
- Hook fires too often? Narrow the pattern, or move to `userTriggered`.
- Hook output not appearing? The agent answered in its own session, which may not surface unless you check the hook log in Kiro.
- Hook runs command that fails? Add `> /tmp/hook.log 2>&1` to the command for debugging.

## Where hooks store state

Hooks themselves are stateless. If you need state between runs (e.g., "did I already process today's Adobe drop?"), write a marker file:

```bash
marker="$HOME/shared/.state/adobe-processed-$(date +%F)"
if [ -f "$marker" ]; then exit 0; fi
# ... do work ...
touch "$marker"
```

## Starter loadout

New teammate, just enabled Slack + Outlook + SharePoint MCPs, wants minimal automation:

1. `morning-brief.kiro.hook` — the daily habit starter
2. `weekly-retro.kiro.hook` — manual trigger, runs Friday

Add adobe-daily-watch and dashboard-refresh when you actually have those data flows running. Add callout-linter when you're actively writing callouts.

## Rules for writing your own hooks

- **Single responsibility.** One trigger, one kind of output.
- **Safe by default.** Output to self-DM or local file, never channel or external recipient.
- **Guardrails in the prompt.** "If condition X, skip silently."
- **Version it.** Bump the `"version"` field when you change behavior so you know what's running.
- **Test with `userTriggered` first,** then switch to auto-trigger once it works.
