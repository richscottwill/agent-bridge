# Demo Script — Leadership Demo Week of 2026-05-04

**Duration:** 15 minutes
**Audience:** Kate (L8), Brandon (L7), tech leaders at L8+, Zoom + in-person
**Goal:** Show that a marketing manager orchestrates agents that produce the dashboards, docs, and data leaders consume.

---

## Pre-Demo (5 min before)

- Open dashboard at presentation zoom: `http://localhost:8000/`
- Verify these tabs load fresh: Command Center, Agent Activity, System Flow, Contribute
- Close all other browser tabs and windows
- Full screen the dashboard tab
- Zoom the browser to 125% (Cmd/Ctrl +)
- Turn off notifications, Slack, email
- Have offline screenshot folder open in a separate window (for fallback)
- Pre-type the "contribute" signal so demo #4 is faster: *"Lena flagged AU CPC outlier — 3 keywords over $30, need investigation"*

---

## 0:00 — 1:00 · Cold Open

**On screen:** Command Center tab, full dashboard visible.

**Say:**
> "This is my dashboard. Everything on it was produced in the last 24 hours. Some of it by me. Most of it by agents. I want to show you who made what, and why that matters for how a non-technical IC can work."

**Pause.** Let them scan. Don't narrate the layout yet.

**Note:** Small fonts die on Zoom. If dashboard looks cramped, hit Cmd/Ctrl + once more.

---

## 1:00 — 4:00 · Provenance Tour (3 min)

**On screen:** Command Center tab. Scroll to show the three sections.

**Say:**
> "Every section has a provenance bar. It tells you who produced the content below."

**Click sequence:**

1. **Point to "Daily Blocks" provenance bar.** (Should show: 🤖 AM Backend, 🤖 EOD Backend, 👤 Richard)
   > "Daily Blocks comes from the morning and end-of-day agents. I just set the rules for how tasks get bucketed. They do the work."

2. **Point to "Integrity Ledger" provenance.** (Should show: 🤖 Signal Extractor, 🤝 Richard-approved)
   > "The ledger is pulled from every conversation I'm in — Slack, email, meeting transcripts. An agent extracts commitments I made. Nothing appears unless it's from a real source I can trace."

3. **Point to "Actionable Intelligence" provenance.** (Should show: 🤖 Karpathy, 🤖 aMCC)
   > "This is the leverage layer. An agent named Karpathy surfaces what's high-impact. Another one — we call it aMCC — flags when I'm avoiding hard work."

**Key line:** *"Every card tells you its producer. No black boxes."*

**Fallback if provenance bars don't render:** Show the screenshot folder, narrate the same content.

---

## 4:00 — 6:00 · System Flow (2 min)

**On screen:** Click the "System Flow" tab.

**Wait 3 seconds** for the Sankey to render. Let them see the convergence visually before explaining.

**Say:**
> "Here's everything feeding this dashboard. Seven sources on the left — Slack, Asana, Email, meeting transcripts, calendar, Loop docs, the analytics database. Four processing agents in the middle. Five output surfaces on the right."

**Hover one node** (e.g., MotherDuck) to show the tooltip with daily volume.

> "The width of each flow line is a measurable daily volume. About 200 pieces of signal per day go through this system. I don't read most of them. The agents do."

**Land it:** *"This is orchestration. Not automation."*

---

## 6:00 — 9:00 · Live Contribution Loop (3 min)

**On screen:** Click the "Contribute" tab.

**Say:**
> "Here's the piece that matters for scale. Right now, only I can feed this system. But anyone should be able to. Watch what happens when a teammate drops a signal."

**Demo action:**
- Type in "Who are you?": `Lena`
- Select scope: `AU`
- Paste the pre-typed signal: `Lena flagged AU CPC outlier — 3 keywords over $30, need investigation`
- Click **Submit to agents**

**Watch the 4-stage confirmation appear:**
1. Signal accepted
2. Signal Router classified → priority → hands
3. Routed to relevant organ → hands.md + Asana commit
4. Surfaced in Command Center

**Say:**
> "Four stages. Four agents touched this signal. A minute from now it would be on my dashboard and in my Asana. A teammate didn't need to know my file structure, my routing rules, or even what Kiro is. They just dropped a signal."

**Fallback if it fails:** Screenshot of the 4-stage completion. Narrate the same story from screenshots.

---

## 9:00 — 12:00 · Agent Activity Feed (3 min)

**On screen:** Click the "Agent Activity" tab.

**Say:**
> "Every agent action leaves a trace. This is the last 24 hours — 47 actions, 12 agents active, zero failures."

**Point to the stats row. Scroll down to the feed.**

**Click on an expanded row** — pick the callout-writer entry.

**Say:**
> "Here's one agent invocation. The market analyst pulled weekly metrics and change log entries. The writer drafted a callout. The reviewer scored it 8.6 out of 10 and published. If any step failed a quality gate, it'd be blocked right here."

**Point to the blocked row** (wiki-critic scored 7.9 — below 8.0 gate).

> "This one got blocked. Score was 7.9. Gate is 8.0. It's back in revision. The agent rejected its own output because quality wasn't good enough."

**Key line:** *"Agents don't just produce. They enforce the quality bar I set."*

---

## 12:00 — 15:00 · Close (3 min)

**On screen:** Back to Command Center.

**Say:**
> "So here's what I want to leave you with. I'm a marketing manager. I don't code as my job. What I do is write specs, set policy, and approve output. The agents produce the work. The dashboard is where we meet.
>
> This took three weeks. Zero budget. I used tools that are already available to every Amazon builder.
>
> The interesting question isn't whether this works for one IC. It's what happens if we apply this pattern to a team. If every marketing manager had an orchestration layer like this — if every analyst, every program manager — the ratio of strategic work to tactical work changes. That's the opportunity.
>
> I'm happy to walk through how we'd replicate this pattern for anyone's team. And I'm happy to take questions."

**Pause. Do not fill silence.**

---

## Q&A Preparation

Keep each answer under 60 seconds. See `risk-log.md` for full bank. Top 5 likely questions:

### 1. "Isn't this what Kiro / Q Business / Copilot already does?"
> "Kiro is the development environment I build in. Q Business and Copilot are one-shot assistants. What's different here is the orchestration layer — the agents talk to each other, share context, enforce quality gates, and write to multiple surfaces. No one product gives you that today. The glue is the value."

### 2. "What's the security model?"
> "Every write action goes through a preToolUse hook that either allows it or blocks it. External email sends? Blocked unless recipient is me. Calendar invites with external attendees? Blocked. Every Asana write is audited. Slack is read-only. I can show you the safety guards if you want."

### 3. "Can my team have this?"
> "Yes. Three things. First, Kiro environment — already available. Second, the shared context repo pattern — I can share the structure. Third, the agent specs themselves — I can share those too. The marginal cost of adding a team member to this pattern is roughly one afternoon of setup. I've prepped a one-pager on productization path."

### 4. "What's the maintenance cost?"
> "About an hour a week of calibration. An agent called Karpathy runs experiments on the system itself — compression, output quality, organ drift — and does most of the ongoing tuning. The reason I don't spend more time on it is because I built it to require less of me, not more."

### 5. "How do you know the agents are right?"
> "Two ways. First, quality gates — every agent output is scored, and things below threshold are blocked. Second, calibration — predictions are scored against actuals, and the system learns when it's over- or under-confident. I can show you the calibration view."

### Bridge-back phrases (if Q&A drifts)

- "That's a great question. Let me first close the loop on…"
- "I want to answer that fully. Can we come back to it after I show you one more thing?"
- "The short answer is yes, and the longer version is…"

---

## Hard Rules

- **Do not read slides.** This is a live demo. Eye contact > screen contact.
- **Do not over-explain.** If it landed in 30 seconds, move on.
- **Do not apologize for what's missing.** Show what works.
- **Do not use the word "just."** Ever. ("I just built this" undersells.)
- **If something breaks live, pivot to screenshots immediately.** Do not debug on screen.

---

## Dry-Run Schedule

- **4/28 (Mon) — First rehearsal** with yourself, timed, video yourself
- **4/30 (Wed) — Second rehearsal** with one non-leader (Adi or Dwayne) for feedback
- **5/2 (Fri) — Final rehearsal** with Brandon for substance review
- **5/4+ (demo week) — Lock the dashboard state** 24h before. Screenshot fallbacks captured.
