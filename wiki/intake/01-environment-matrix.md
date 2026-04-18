# Environment Matrix — Where to Do What with Kiro

**Audience:** Amazon Paid Acquisition teammates and their Kiro agents.
**Purpose:** Decide which Kiro environment to use for a given task in under 10 seconds.
**Status:** READY

## The four environments

| Environment | Where it runs | Primary UI |
|---|---|---|
| **AgentSpaces chat** | Amazon cloud | Browser chat window |
| **DevSpaces (remote IDE)** | Amazon cloud, containerized workspace | Browser-based VS Code ("Kiro code") |
| **kiro-chat-cli** | Your laptop terminal | Terminal chat |
| **Local Kiro IDE** | Your laptop | Native VS Code with Kiro |

## Capability matrix

| Capability | AgentSpaces chat | DevSpaces IDE | kiro-chat-cli | Local IDE |
|---|---|---|---|---|
| Read/write `/workspace` files | No | **Yes** | No | **Yes** (your laptop filesystem) |
| Read/write `~/shared/` (team persistent) | **Yes** | **Yes** | No | No |
| Read/write local laptop files (Downloads, Desktop, etc.) | No | No | **Yes** | **Yes** |
| MCP servers (Slack, Outlook, SharePoint, Asana, Hedy) | **Yes** | **Yes** | **Yes** | **Yes** (with auth) |
| Hooks (file-edit, prompt-submit, agent-stop) | Limited | **Yes** | No | **Yes** |
| Background processes (dashboards, watchers) | No | **Yes** | No | **Yes** |
| Browser / GUI automation | No | No | No | **Yes** (you're on the machine) |
| Persists across sessions (files, state) | **Yes** (via `~/shared/`) | **Yes** | No (ephemeral) | **Yes** |
| Speed (startup) | Fast | Medium (container boot) | Fast | Fast |
| Works offline | No | No | No (needs MCP auth) | Partial (local files only) |

## Decision rules — "I want to..."

**...ask a quick question with no files involved**
→ **AgentSpaces chat.** Fastest, zero setup, MCPs work.

**...pull the latest pacing Excel from OneDrive and summarize it**
→ **AgentSpaces chat** or **DevSpaces IDE**. Both have SharePoint MCP. Use DevSpaces if you want to save the analysis to `~/shared/`.

**...build or edit a dashboard that runs against team data**
→ **DevSpaces IDE**. You need `/workspace` for the source files, `~/shared/` for persistence, hooks for auto-refresh, and background processes for the server. Local IDE works too but you lose team persistence.

**...read a PPTX your vendor just emailed you and is sitting in your Downloads folder**
→ **Local IDE** or **kiro-chat-cli**. Only your laptop sees your Downloads.

**...run a hook that watches for daily Adobe data drops**
→ **DevSpaces IDE**. Hooks persist with the container; your laptop may sleep.

**...browse a team wiki article or search published reports**
→ **DevSpaces IDE** or **AgentSpaces chat**. Both can access `~/shared/wiki/` (DevSpaces natively, AgentSpaces via shared-folder MCP).

**...write a long doc, email draft, or callout**
→ Any. AgentSpaces for pure chat; DevSpaces/local IDE if you want the draft saved to files.

**...orchestrate agents or run the full morning routine**
→ **DevSpaces IDE**. Only environment with hooks + shared folder + MCPs + background processes all at once.

## Team persistence — where files live

| Location | Shared across your own agents? | Shared across team? | Survives container recycle? |
|---|---|---|---|
| `~/shared/` (DevSpaces) | Yes | No (your workspace only) | Yes |
| `/workspace/` (DevSpaces) | Yes | No | Yes |
| Laptop filesystem (local IDE / cli) | No (device-local) | No | N/A |
| OneDrive / SharePoint | Yes (durability layer) | **Yes** (when shared) | Yes |

**Rule:** If a teammate needs to see it, put it in OneDrive or SharePoint. `~/shared/` is yours alone; it doesn't sync across people.

## Getting started — pick one

- **New to Kiro?** Start with **AgentSpaces chat.** Zero setup, try out MCPs, get comfortable.
- **Going to do regular work?** Onboard **DevSpaces IDE.** This is where the team does dashboards, hooks, orchestration.
- **Working offline or with local files?** Install **local Kiro IDE** on your laptop.
- **Want terminal-first chat?** Install **kiro-chat-cli**.

Most teammates will end up using 2 — DevSpaces for "real work" and AgentSpaces chat for quick questions on the go.

## Common traps

- **"My agent can't see the file on my Desktop."** You're on DevSpaces or AgentSpaces — those can't see your laptop. Move to local IDE, upload to OneDrive, or paste the content.
- **"My hooks stopped firing."** DevSpaces container recycled. Check `~/.bashrc` auto-start lines or re-enable the hook.
- **"The agent wrote a file but it's gone next session."** You were on kiro-chat-cli (ephemeral). Use DevSpaces with `~/shared/` for persistence.
- **"Team can't see my shared file."** `~/shared/` is per-person, not per-team. Push to OneDrive or SharePoint.
