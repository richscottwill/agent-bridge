# Kiro Environment Matrix — Where to Do What

**Doc:** 01
**Audience:** Paid Acquisition teammates + their Kiro agents
**Status:** FINAL
**Last updated:** 2026-04-17

## Environment Awareness (for your agent)

This doc is the environment reference itself. Before using any other doc in the kit:

1. Identify which environment you're running in right now (Remote IDE / Local IDE / AgentSpaces Chat / kiro-chat-cli).
2. Tell the user in plain language: "I'm in [environment name]. Here's what I can do here, and here's what I can't."
3. When the user asks you to do something, check the capability matrix below. If the request won't work in the current environment, say so in plain words before attempting it — no jargon, no tool names, just what the user will experience.

---

Kiro runs in four different environments. They look similar on the surface. They behave very differently underneath. Picking the wrong one wastes 20 minutes and makes you think "Kiro is broken" when it's actually just the wrong tool for the job.

This doc answers: **"I want to do X — which environment should I be in?"**

## The four environments

| Environment | What it is | How to access |
|---|---|---|
| **AgentSpaces Chat** | Browser-based chat agent. Pre-configured Amazon devcontainer. No file editor. | chat.agentspaces.aws.dev (or your AgentSpaces entry point) |
| **DevSpaces Remote IDE** | Full VS Code / Kiro IDE in a browser, running in a persistent Amazon container. File editor + terminal + chat. | devspaces.amazon.com |
| **kiro-chat-cli (laptop)** | Terminal-based Kiro running on your local machine. No file editor, chat only. | `kiro chat` in your laptop terminal after install |
| **Local Kiro IDE** | Kiro app installed on your laptop. Full IDE + chat + your local filesystem. | Kiro.app on Mac, Kiro.exe on Windows |

## Capability matrix

| Capability | AgentSpaces Chat | DevSpaces Remote IDE | kiro-chat-cli | Local Kiro IDE |
|---|---|---|---|---|
| **Read/edit laptop files** | ❌ | ❌ | ✅ | ✅ |
| **Read/edit `/workspace/` (containerized)** | ✅ | ✅ | ❌ | ❌ |
| **Access `~/shared/` persistent storage** | ✅ | ✅ | ❌ | ❌ |
| **Terminal commands** | Limited (agent runs shell, no interactive) | ✅ full terminal | ✅ full terminal | ✅ full terminal |
| **Run long processes / servers / hooks** | ❌ (per-session, no daemons) | ✅ | Limited | ✅ |
| **MCPs work** | ✅ most (configured at user level) | ✅ all | ✅ all | ✅ all |
| **Session persists across days** | ❌ (per-chat) | ✅ (container persists) | ❌ (per-session) | ✅ (your laptop) |
| **Speed** | Fast | Medium (cold-start ~30s) | Fastest | Fastest |
| **Can use GUI apps (browser, Excel, PowerPoint)** | ❌ | ❌ | ❌ (no GUI from CLI) | ✅ (you have your laptop) |
| **Good for scheduled automation / hooks** | ❌ | ✅ | ❌ | ⚠️ only when laptop is on |

## Pick-by-task guide

### Quick chat questions, no files involved

**Use:** AgentSpaces Chat or kiro-chat-cli.

Examples: "explain Google Ads value-based bidding," "draft a Slack message to thank Adi," "what's the difference between ROAS and CPA."

Both are fine. AgentSpaces if you're in a browser already, cli if you're already in terminal.

### Reading or editing files in `/workspace/` or `~/shared/`

**Use:** DevSpaces Remote IDE.

This is where the team's shared persistent storage lives. Your morning briefs, state files, wiki, dashboards, shared context files — they all live in `~/shared/` inside the DevSpaces container. AgentSpaces Chat can technically read them, but the IDE is where you get proper file navigation, search, and editing.

### Reading or editing files on your laptop

**Use:** Local Kiro IDE or kiro-chat-cli.

If a vendor sent you a PowerPoint or you've got raw Adobe data on your Downloads folder, the containerized environments can't see it. Either use the laptop IDE directly or drag the file into `~/shared/` via OneDrive sync first.

### Pulling files from SharePoint/OneDrive

**Use:** Any environment with the SharePoint MCP installed.

All four environments can do this. Preference:

- **DevSpaces Remote IDE** if you want to process the file (parse Excel, extract PDF text, diff two docs) — it has Python + Pandas + openpyxl ready to go.
- **Local Kiro IDE** if you want to open the file in Excel/Word after downloading.
- **AgentSpaces Chat** or **cli** for quick "summarize this doc" queries.

### Running daily automation (morning brief, dashboard refresh, Adobe data watcher)

**Use:** DevSpaces Remote IDE.

This is the only environment where hooks run reliably when you're not actively using Kiro. The container stays up, scheduled hooks fire, shared state persists. Don't try to run daily automation from your laptop IDE — it only runs when your laptop is awake and Kiro is open.

### Querying large datasets / running SQL

**Use:** DevSpaces Remote IDE (for now).

The DuckDB/MotherDuck MCP works best here because of token handling and shared state. Once you've got analytical workflows running, you want persistent context.

### Working while offline or on weak wifi

**Use:** Local Kiro IDE or kiro-chat-cli.

Both work locally once installed. DevSpaces and AgentSpaces need a stable connection to the container.

### Sharing context across your own agents

**Use:** DevSpaces Remote IDE + `~/shared/`.

Anything in `~/shared/` is visible to every Kiro session you start (chat, cli, IDE, AgentSpaces). That's the design. Your laptop IDE and the remote IDE do NOT share a filesystem — they're separate worlds. Pick one as your primary, then use OneDrive as the bridge for files you need in both.

## The big gotcha: environment confusion

The #1 source of "Kiro isn't working" reports:

- **Agent says "file not found"** on a file you can clearly see on your laptop → you're in AgentSpaces or DevSpaces, which can't see your laptop.
- **Agent can't find `~/shared/`** → you're in local Kiro or cli on your laptop, which doesn't have our DevSpaces container.
- **Hook didn't fire overnight** → you set it up on your laptop IDE but closed your laptop.

Before troubleshooting, always check: which environment am I in? Your agent can tell you — ask "what environment am I running in and what file access do I have?"

## Recommended working pattern for Paid Acq

Most teammates will end up using two environments in parallel:

1. **DevSpaces Remote IDE** as the primary workspace — morning briefs, state files, dashboards, daily automation, team wiki, anything shared.
2. **Local Kiro IDE** or **AgentSpaces Chat** for laptop-local work — opening files from Outlook, reviewing decks, quick chat questions while in a meeting.

OneDrive via SharePoint MCP is the bridge between them.

## Quick reference card

| I want to... | Use |
|---|---|
| Read a file from my Downloads folder | Local Kiro IDE |
| Read a file from OneDrive | Any env with SharePoint MCP |
| Run morning brief automation | DevSpaces |
| Edit a callout in the team wiki | DevSpaces |
| Parse an Excel the vendor emailed me | Local Kiro IDE, or save to OneDrive + DevSpaces |
| Ask a quick question while in a meeting | AgentSpaces Chat |
| Draft a reply to a Slack message | Any env with Slack MCP |
| Run a dashboard refresh on a schedule | DevSpaces |
| Review a PowerPoint from a vendor | Local Kiro IDE |
| Query the team's shared analytics data | DevSpaces |
