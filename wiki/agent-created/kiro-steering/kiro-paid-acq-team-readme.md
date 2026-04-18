# Kiro Paid Acq Team Onboarding Kit

**Owner:** Richard Williams (prichwil)
**Audience:** Amazon Business Paid Acquisition teammates (and their Kiro agents) getting started with Kiro.
**Location:** `Kiro-Drive/Artifacts/kiro-paid-acq-team/` on Richard's OneDrive.

## What's here

This folder holds everything a teammate or their agent needs to onboard to Kiro the way the Paid Acq team uses it. The docs are written for your Kiro agent to read — drop them into your chat and your agent will know what to do. When your agent talks back to you, it'll use plain language (no jargon required).

**Docs are numbered in drop-in order.** Start at 01 and work down. Stop when you hit a doc that isn't relevant to your role yet — you can always come back later.

## If you're not technical, read this first

- **You don't need to be a developer to use this kit.** The docs are written for your Kiro agent, not you. Just drop the relevant file into a chat and ask your agent to help you set things up.
- **Your agent will tell you when something needs you.** If a setting has to be changed or a file needs to be saved, your agent will walk you through it in plain language.
- **You can always say "I don't get it — explain this like I've never seen Kiro before."** Your agent will back up and try again.
- **Nothing in this kit will send a message, email, or post on your behalf without you approving it first.** That's a hard rule across every doc.

## How the kit works

1. **Pick which docs apply to you.** The numbered order below goes from foundation (everyone) to advanced/optional (only some roles). Don't install everything on day 1.
2. **Drop the relevant docs into your agent's context** when working on that topic. For the ones with a "Steering file" section at the end, copy the steering block into your Kiro steering folder so the rule auto-loads.
3. **Every doc is environment-aware.** The top of each doc has an "Environment Awareness" table. Your agent checks it before acting and tells you what works in your current environment (Remote IDE / Local IDE / AgentSpaces) vs what doesn't.

## Environment awareness — the standing rule

Your agent should always know which environment it's running in and proactively tell you:

- What this doc's instructions can do in this environment
- What they can't do (and which environment to switch to)
- Any workarounds

If your agent isn't doing it, paste this into your chat: *"Before acting, tell me which environment you're in and what's possible vs not possible for this request."*

## Hard rule across every doc in this kit

**Agents never send, post, reply, comment, or forward to anyone but the user themselves.** Drafts and `self_dm` are the workaround for external communication. Writing to self (personal OneDrive, self-DM, own calendar blocks, own Asana tasks, own drafts folder) is fine.

See doc 02 for the full rule and the canonical autoApprove lists.

## Drop-in order

**Foundation — everyone**

| # | Doc | Why |
|---|---|---|
| 01 | `01-kiro-environment-matrix.md` | Which environment does what. Your agent needs this first. |
| 02 | `02-kiro-no-external-write-rule.md` | The safety rule + MCP autoApprove lists. Install the steering file before enabling any MCP. |
| 03 | `03-kiro-steering-packages.md` | Picker doc — tells you which steering files to install for your role. |

**Daily productivity MCPs — install as you enable each**

| # | Doc | Why |
|---|---|---|
| 04 | `04-kiro-sharepoint-protocol.md` | OneDrive + SharePoint access. Highest-leverage MCP. |
| 05 | `05-kiro-slack-mcp.md` | Slack triage, drafts, self-DM patterns. |
| 06 | `06-kiro-outlook-mcp.md` | Email triage, calendar, drafts. |

**Core work patterns — everyone writes, so 07 is broadly useful**

| # | Doc | Why |
|---|---|---|
| 07 | `07-kiro-writing-with-kiro.md` | Style guides, callout pipeline, draft defaults. Most paid acq work involves writing. |

**Opt-in — only if relevant to you**

| # | Doc | Why |
|---|---|---|
| 08 | `08-kiro-asana-mcp.md` | Only if you use Asana for task tracking. |
| 09 | `09-kiro-excel-source-of-truth.md` | If you work with the team's Excel data files (pacing, forecast, testing). |
| 10 | `10-kiro-team-wiki.md` | When you're ready to search and contribute to the shared wiki. |

**Advanced — once you're comfortable with the basics**

| # | Doc | Why |
|---|---|---|
| 11 | `11-kiro-hooks-cookbook.md` | Copy-paste hooks for morning briefs, Adobe data watchers, etc. |
| 12 | `12-kiro-team-orchestration.md` | How individual agents contribute to shared team artifacts. Ambitious — don't start here. |

## Recommended first session

A new teammate opening Kiro for the first time should:

1. Read doc 01 in their agent and confirm which environment they're in.
2. Read doc 02 and paste the `no-external-write-rule.md` steering block into their Kiro steering folder.
3. Read doc 03 and pick their Core + MCP packages.
4. Enable SharePoint MCP, paste doc 04 into the chat, test a read.
5. Enable Slack + Outlook MCPs one at a time, docs 05 and 06.
6. Stop. Come back tomorrow to keep going.

That's enough for day 1. The rest unfolds over weeks.

## Questions or issues

Reach out to Richard (prichwil) on Slack.
