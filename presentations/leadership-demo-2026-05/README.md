# Leadership Demo — Week of 2026-05-04

**Date:** Week of May 4, 2026 (~12 working days from 2026-04-21)
**Audience:** Kate Rundell (L8), Brandon Munday (L7), tech leaders at L8+
**Format:** Richard's laptop + conference room display + Zoom simulcast
**Duration:** 15 minutes
**Presenter:** Richard Williams (Marketing Manager L5, Paid Search)
**Goal:** Convey depth of what's been built. Inspire a non-technical-leading audience (mixed with technical leaders) that individual contributors can orchestrate meaningful agentic systems.

---

## Audience Implications

- **Tech leaders at L8+** will probe the plumbing. Have answers for: security/PII, auth model, data source of truth, maintenance cost, how agents are prompted, how quality is measured. Don't dodge — lean into substance.
- **Kate (L8 non-technical)** cares about outcomes, team leverage, productization potential, and whether this could scale.
- **Brandon** has seen most of it; his role is credibility witness. Don't re-pitch him. Show him new things.
- **Zoom simulcast** means small fonts on the dashboard will die. Design every visible element for 125%+ zoom.
- **No backup video** → live demo fallbacks must be offline screenshots, captured 24h before. Not recorded video.

## The Story (one sentence)

**"I don't write dashboards anymore. I orchestrate agents that do. And this is what it looks like when humans and agents collaborate on the same surface."**

Richard's job is orchestrator + policy layer — writes specs, sets policy, approves output, defines quality gates. Agents produce the work. The dashboard is the shared surface where humans + agents meet.

---

## 15-Min Demo Flow

### 1. Cold open (1 min)
Open the Kiro dashboard at presentation zoom level. "Everything on this dashboard was produced in the last 24 hours. Some by me. Most by agents. Let me show you who made what, and why that matters."

### 2. Provenance tour (3 min)
Walk through 3 cards with provenance bars visible:
- **WBR callout** → 3 agents (analyst → writer → reviewer) → dashboard
- **Portfolio finding** → EOD backend → Asana enrichment → dashboard
- **Market state file** → AM backend + Hedy transcripts + Slack → SharePoint → dashboard

Key line: "Every card tells you its producer. No black boxes."

### 3. Contribution-flow Sankey chart (2 min)
"Here's every stream feeding this view — 17 Slack channels, 96 Asana tasks, 55 database tables, 11 meeting series, daily." Let the convergence land visually.

### 4. Human contribution loop (3 min)
Click "Contribute" on a state file. Drop a live note. Pre-baked agent picks it up within 30 seconds, renders in dashboard. "Anyone on the team can feed this. Agents route it."

### 5. Agent Activity Feed (3 min)
Open the feed tab. 10 agent actions from the last hour. Click one → full trace (prompt, output, quality gate). "Agents don't just run — they leave an auditable trail."

### 6. Land the message (3 min)
"I'm not a marketing manager who also codes. I'm a marketing manager who orchestrates agents. My job is specs, policy, and quality. The agents produce the work. The dashboard is where we meet. Built in three weeks. Zero budget. Imagine what a team with real resources could do."

---

## Build Priority (12-day sprint)

See `build-tracker.md` for specs.

1. **Provenance bar on dashboard cards** (~2h) — biggest demo impact
2. **Agent Activity Feed tab** (~3h) — makes invisible work visible
3. **Sankey contribution-flow chart** (~2–3h) — the "aha" visual
4. **Contribute affordance + pre-baked loop** (~1.5h) — the interactive moment
5. **Demo script** (~1h) — minute-by-minute, rehearse 3x
6. **One-pager leave-behind** (~1h) — for post-demo reference
7. **Offline screenshot fallbacks** (~30m) — 24h before demo
8. **Risk log + Q&A prep** (~30m) — technical probe answers

**Total: ~11h focused work over 12 days.**

---

## What NOT to Demo

- Morning routine walkthrough (too familiar; "AI reads my Slack" is played out)
- Body system architecture diagrams (too abstract, "look how clever" vibe)
- Karpathy experiments / compression (too meta)
- Wiki pipeline end-to-end (too long for 15 min)
- Code or config files (they want outcomes)
- Eight things in 15 minutes (one thing deeply)

---

## Q&A Prep (for tech leaders)

See `risk-log.md` for narrative risks. Key probes to have tight answers for:

- **"Isn't this what [Kiro/Asana AI/Q Business/Copilot] already does?"** — *Differentiator: orchestration layer, multi-surface, provenance.*
- **"What's the security/PII model?"** — *Safety guards block external email/calendar. Audit log on every write. Read-only Slack. 2 preToolUse hooks enforce.*
- **"What's the maintenance cost?"** — *~1h/week calibration. Karpathy agent handles compression and organ drift autonomously.*
- **"Can my team have this?"** — *Yes. Three things: (1) Kiro env, (2) shared context repo structure, (3) write the specs. No engineering budget needed.*
- **"What about data source of truth?"** — *MotherDuck `ps_analytics` — 55 tables, 8 schemas, keyed by (market, period_type, period_key). Single source. Dashboards and agents both point here.*

---

## Files in This Folder

- `README.md` — this file (vision + context)
- `build-tracker.md` — live build status, specs, acceptance criteria
- `demo-script.md` — minute-by-minute script (drafted ~5/1, rehearsed ~5/2)
- `risk-log.md` — failure modes, mitigations, 24h-before checklist, Q&A bank
- `one-pager.md` — leave-behind for leaders (drafted ~5/2)

---

## Status

- [x] SharePoint folder created via OneDrive
- [x] README + vision set (this file)
- [x] Build tracker with specs
- [ ] Build 1 — Provenance bar
- [ ] Build 2 — Agent Activity Feed
- [ ] Build 3 — Sankey chart
- [ ] Build 4 — Contribute affordance + loop
- [ ] Build 5 — Demo script
- [ ] Build 6 — One-pager
- [ ] Build 7 — Offline screenshots
- [ ] Build 8 — Risk log + Q&A prep expanded
- [ ] Dry run with non-leader audience
- [ ] Demo delivered
