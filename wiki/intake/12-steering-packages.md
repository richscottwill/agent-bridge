# Steering Packages — Pick What Loads Into Your Agent

**Audience:** Paid Acquisition teammates setting up Kiro.
**Purpose:** Give your agent exactly the rules and context you need, without info overload from domains you don't use.
**Status:** READY

## The problem

Steering files auto-load into every agent turn and cost context budget. If everyone got every rule — SharePoint, Slack, Outlook, Asana, Excel conventions, writing guides, hook patterns, wiki rules — agents would run out of room before they started the actual work. Most teammates only need a subset.

## The solution: packages

Kit docs ship as bundles. You activate the ones you care about and skip the rest. Every teammate installs `core`. Everything else is opt-in.

## The packages

### `core` — mandatory for everyone

The bare minimum every PAcq Kiro user needs. About 600 words total.

- **No-external-write rule** — the hard safety rule (from doc 03)
- **Team writing style base** — how we write, sign-offs, tone
- **Wiki search rule** — search `~/shared/wiki/` before guessing, flag stale answers
- **Environment awareness** — which env the agent is in, what it can and can't reach

Install: copy `packages/core/*.md` to `~/.kiro/steering/` with `inclusion: always`.

### `onedrive` — anyone working with Word/Excel/PDFs in OneDrive or SharePoint

- SharePoint MCP protocol (doc 02)
- OneDrive default behavior, team site escalation rules

Install: copy `packages/onedrive/agent-sharepoint-protocol.md` with `inclusion: fileMatch` pattern `*.docx,*.xlsx,*.pdf,*.pptx` or `inclusion: always` if you work with OneDrive daily.

**Skip if:** you only work in code or chat, never touch OneDrive.

### `slack` — anyone triaging Slack with Kiro

- Slack MCP rules (doc 04)
- Read/draft/self-DM pattern
- Channel etiquette

Install: copy `packages/slack/*.md` with `inclusion: manual` (activate with `#slack-rules` when needed) or `always` for heavy Slack users.

**Skip if:** you rarely use Slack, or you only use Slack without Kiro.

### `outlook` — anyone using Kiro for email or calendar

- Outlook MCP rules (doc 05)
- Draft-first email pattern
- Calendar read patterns

Install: copy `packages/outlook/*.md` with `inclusion: always` for daily email triage, or `manual` if occasional.

**Skip if:** you don't connect Outlook to Kiro.

### `asana` — anyone using Asana through Kiro

- Asana task triage patterns (doc 06)
- Bucket conventions (Sweep / Core / Engine Room / Admin / Wiki)
- Bulk-write warnings

Install: copy `packages/asana/*.md` with `inclusion: manual` — activate with `#asana-rules` when doing task work.

**Skip if:** you don't use Asana or prefer the Asana UI directly.

### `writing` — heavy writers (most of the team)

- Team writing style full stack: email, docs, WBR, MBR, Amazon-formal
- Callout pipeline pattern
- Draft defaults for stakeholder communication

Install: copy `packages/writing/*.md` with `inclusion: manual` and activate per-task:
- `#style-email` for emails
- `#style-docs` for long-form docs
- `#style-wbr` for WBR callouts
- `#style-mbr` for MBR prose

**Skip if:** you don't draft prose through Kiro.

### `data` — anyone building dashboards or processing Excel

- Excel-in-SharePoint as source of truth (doc 07)
- Canonical file list (pacing, test tracker, callouts log, reports index)
- Append-to-logs pattern, never overwrite, timestamped saves

Install: copy `packages/data/*.md` with `inclusion: fileMatch` pattern `*.xlsx,*.csv` or `always` for dashboard builders.

**Skip if:** you don't touch the team's Excel data layer.

### `hooks` — anyone building or running automated workflows

- Hook conventions and safety (doc 08 cookbook applies)
- preToolUse / postToolUse gotchas
- Circular dependency warnings

Install: copy `packages/hooks/*.md` with `inclusion: fileMatch` pattern `*.kiro.hook,*.hook.md` or `manual`.

**Skip if:** you're not building hooks.

### `orchestration` — advanced, once you're contributing to shared team artifacts

- Intake folder pattern (doc 11)
- Librarian / promotion flow
- Event log pattern
- How to contribute callouts, reports, data back to the team

Install: copy `packages/orchestration/*.md` with `inclusion: manual` — activate when working on shared deliverables.

**Skip if:** you're still in individual-productivity mode.

## Recommended starter bundles

### Minimal (Kiro-curious, read mostly)

```
core + onedrive
```

### Email-and-Slack triage user

```
core + onedrive + slack + outlook
```

### Full PAcq productivity user

```
core + onedrive + slack + outlook + asana + writing + data
```

### Advanced orchestrator (Richard-level)

```
all packages
```

## How steering files load in Kiro

Every `.md` file in `~/.kiro/steering/` can specify loading behavior in frontmatter:

```markdown
---
inclusion: always
---
```

or

```markdown
---
inclusion: fileMatch
fileMatchPattern: '*.xlsx'
---
```

or

```markdown
---
inclusion: manual
---
```

- **`always`** — loads on every agent turn (costs context budget every time). Use for core rules.
- **`fileMatch`** — loads only when the matching file is in context. Use for domain-specific rules.
- **`manual`** — loads only when you reference it with `#<filename>` in chat. Use for style guides and occasional patterns.

## The install workflow

1. Decide which packages you want (start minimal, add as needed).
2. Download or copy package files from `Kiro-Drive/Artifacts/kiro-paid-acq-team/packages/<name>/` — or ask your agent to read them directly from there.
3. Copy into `~/.kiro/steering/` in your DevSpaces workspace (or wherever your primary Kir