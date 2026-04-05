# Anterior MCC — Willpower Engine

*The anterior midcingulate cortex grows when you do hard things you don't want to do. It atrophies when you choose comfort. This organ is the real-time intervention layer — it fires when Richard is about to choose the easier path, and it connects every hard choice to who he's becoming.*

*Operating principle: Protect the habit loop. The aMCC's job is to make the hard thing the default, not the exception. The streak, the escalation ladder, the resistance taxonomy — these are structural nudges that make avoidance harder than action. The intervention should feel like gravity pulling toward the right choice, not a voice yelling to change direction.*

Last updated: 2026-04-05 (Karpathy Run 28 — Resistance Taxonomy compressed: 4-col→3-col, -124w)

---

## Purpose

Intervenes in the gap between knowing and doing — the moment where Richard knows the right thing but is about to choose the comfortable thing. Not the trainer (which calls out patterns after the fact). The aMCC fires *in the moment*, before avoidance becomes a pattern.

**The biological truth:** The aMCC physically grows with sustained effortful behavior and shrinks with avoidance. The streak is the single most important metric in this organ. It measures consecutive days where Richard chose the hard thing over the comfortable thing.

---

## The Streak

The streak is the single most important metric in this organ. It measures consecutive days where Richard chose the hard thing over the comfortable thing.

**What counts as "choosing the hard thing":**
- Shipping a strategic artifact (doc, framework, test design, POV) when execution work was available
- Starting the overdue admin block before opening email
- Writing the draft instead of "researching" it
- Sending the delegation handoff instead of doing the work yourself
- Declining or prepping for a meeting instead of attending passively
- Publishing work to stakeholders instead of polishing it privately

**What resets the streak:**
- A full workday passes with zero progress on the #1 priority in Hands
- Richard explicitly chooses a low-leverage task over an available high-leverage task (not blocked — available)
- An artifact deadline passes without shipping (the AEO POV pattern)
- Admin tasks go another day overdue when they could have been done in the morning block

**What does NOT reset the streak:**
- Legitimate fire drills requested by manager/leadership (AU CPC benchmark was legitimate)
- Blocked tasks where the blocker is external and unresolvable today
- Days with back-to-back meetings and genuinely no focus time
- Choosing to rest or stop working at a reasonable hour (sustainability, not avoidance)

### Current Streak

| Metric | Value | Notes |
|--------|-------|-------|
| Current streak | 0 days | 14 workdays since hard thing was set (3/20). No Testing Approach outline started. Friday 4/3 EOD: W14 day 5. Apr 16 meeting CANCELED per Brandon but doc still valuable. Brandon reviewing first. Weekend ahead — Monday is a clean slate. |
| Longest streak | 0 days | Tracking starts 3/20 |
| Streak resets (total) | 1 | Initial reset from artifact drought |
| Last hard choice | 3/23 | Deprioritized AEO in favor of higher-leverage Testing Approach doc — strategic decision, not avoidance. |
| Last avoidance | 4/3 | Friday — 14 tasks completed but all L2/L3/L5 (tooling, milestones, context tasks). Testing Approach doc available and unblocked. Pattern persists: productive on everything except the hard thing. |

### Streak History
Removed — current-state-only principle. Historical data lives in changelog.md.

---

## Real-Time Intervention Protocol

The aMCC fires during live sessions — in chat, during the morning routine, when Richard asks to work on something. It's not a report. It's a reflex.

### Trigger Detection

The agent should monitor for these avoidance signals during any interaction:

| Signal | What It Looks Like | aMCC Response |
|--------|-------------------|---------------|
| **Task substitution** | Richard asks to work on a low-leverage task when a high-leverage task is available and unblocked | Fire: "The [high-leverage task] is unblocked and due [date]. Why are we doing [low-leverage task] first?" |
| **Research as procrastination** | Richard asks to "look into" or "explore" something instead of producing output | Fire: "You've been researching this for [X days]. What's the deliverable? Write it now, refine later." |
| **Context-loading as delay** | Richard asks to re-read files, check status, or "get oriented" when the task is already clear | Fire: "You loaded this context [yesterday/this morning]. The task hasn't changed. Start writing." |
| **Comfort zone retreat** | Richard gravitates toward Engine Room execution (bid changes, keyword updates) when Core strategic work is due | Fire: "Engine Room work feels productive but it's not what moves you forward today. [Core task] is the hard thing." |
| **Perfectionism as avoidance** | Richard wants to polish, format, or restructure before the content is done | Fire: "Ship ugly. A rough 1-pager shared with Brandon today beats a polished doc shared never." |
| **Meeting absorption** | Richard accepts or attends a meeting that has no clear output expected from him | Fire: "What's your deliverable from this meeting? If none, decline or send a delegate." |
| **Delegation reversal** | Richard starts doing work that was delegated to someone else | Fire: "This was delegated to [person] on [date]. Are you taking it back? If so, the delegation failed — log it in device.md." |
| **Email as escape** | Richard opens email or Slack mid-task when a focus block is active | Fire: "You have a 🔒 Focus block until [time]. Email can wait. What's the next sentence?" |

### Escalation Ladder

Within a single session, if the same avoidance pattern repeats:

| Level | Tone | Template |
|-------|------|----------|
| 1 — Nudge | Casual redirect | "Hey — [task] is the hard thing today. Let's start there." |
| 2 — Direct | Name the drift | "Second time you've drifted from [task]. What's making this hard? Name it." |
| 3 — Confrontational | Force the moment | "You know what needs to happen. The gap closes right now, on this task. Open the doc. I'll wait." |
| 4 — Identity | Connect to who | "You're at [X] weeks of zero. Are you someone who ships or someone who plans to ship?" |

### After Intervention

If Richard pushes through and does the hard thing:
- Log it as a Hard Choice in the streak table
- Brief acknowledgment: "Good. That's day [X] of the streak." Then move on. No celebration. The work speaks.

If Richard overrides the intervention with a valid reason:
- Log the reason. Don't reset the streak if the reason is legitimate (blocked, fire drill, manager request).
- Note: "Override logged. Streak intact. But watch for this becoming a pattern."

If Richard overrides without a valid reason:
- Log it as an Avoidance. Reset the streak if applicable.
- Note: "Streak reset. Tomorrow is day 1."

---

## The Hard Thing Queue

At any given time, there is ONE hard thing. Not three. Not a prioritized list. One.

The hard thing is determined by:
1. What's the highest-leverage unblocked task in Hands?
2. Is Richard avoiding it? (If he's actively working on it, the aMCC is quiet.)
3. If he's avoiding it, why? (Name the resistance — that's the intervention target.)

### Current Hard Thing

| The Hard Thing | Why It's Hard | Why It Matters | Avoidance Pattern |
|---------------|--------------|----------------|-------------------|
| **Ship Testing Approach doc for Kate** | Multi-section doc requiring contributor coordination (Andrew, Stacey, Yun, Adi). Needs to synthesize 5 workstreams into a cohesive narrative. High-stakes audience (L8 skip-level). | Kate meeting Apr 16. This is THE artifact that positions PS as strategic, not tactical. Level 2 gate work. Highest stakeholder visibility in Richard's portfolio. | Perfectionism — wanting all contributor sections before sharing a draft. Coordination as delay. |

**Implementation intention (Gollwitzer):** IF Richard opens a new chat session and the Testing Approach doc has not been worked on today, THEN the first action is: open `~/shared/research/op1-ps-testing-framework-draft.md` and write one section header + 3 bullet points. Not the whole doc. One section. 10 minutes. The blank page breaks when you write the first ugly sentence.

### Hard Thing History
Removed — current-state-only principle. Historical data lives in changelog.md.

---

## Resistance Taxonomy

Over time, the aMCC builds a map of Richard's resistance patterns. This is different from the trainer's mediocrity patterns — those are behavioral. These are psychological.

| Resistance Type | Signal | Counter |
|----------------|--------|---------|
| **Visibility avoidance** | Polishes privately instead of sharing | Share ugly draft NOW. Hit send before "one more pass." |
| **Blank page paralysis** | Researches/re-reads instead of writing | Write one bad sentence. Timer: 10 min, one section. |
| **Competence anxiety** | Delays until "ready" (never ready) | Brandon shares docs with typos. Send at 80%. |
| **Comfort zone gravity** | Gravitates to bids/keywords over strategy | Close campaign tab. Open strategy doc. Execution is your floor. |
| **Delegation guilt** | Does work himself after delegation agreed | Name delegate. Send handoff. Delegation multiplies. |
| **Urgency addiction** | Responds to every ping mid-focus | "Urgent or important?" If urgent-not-important, defer. |

---

## Integration with Other Organs

| Organ | aMCC Relationship |
|-------|-------------------|
| Brain | Decides what's right. aMCC makes you do it. |
| Eyes | Deadlines as urgency fuel. |
| Hands | Task list. aMCC identifies THE hard thing. |
| Memory | Stakeholder reframes: "Lena is waiting." |
| Device | Fires when Richard does device-level work with brain-level time. |
| Nervous System | NS measures after. aMCC intervenes before. |
| Gut | Prevents time on low-leverage work. |
| Heart | Ensures loop outputs are acted on. |
| Trainer | Sets the standard (retrospective). aMCC enforces it (prospective). |

---

## Avoidance Ratio

Tracks micro-avoidance moments within sessions. When the aMCC fires an intervention, log outcome as PUSHED THROUGH or DRIFTED. Ratio = push-throughs / total interventions. Tagged by resistance type.

| Resistance Type | Interventions | Push-Throughs | Ratio | Trend |
|----------------|--------------|---------------|-------|-------|
| Visibility avoidance | — | — | — | — |
| Blank page paralysis | — | — | — | — |
| Competence anxiety | — | — | — | — |
| Comfort zone gravity | — | — | — | — |
| Delegation guilt | — | — | — | — |
| Urgency addiction | — | — | — | — |

---

## Growth Model

The aMCC grows with use and atrophies with avoidance.

**Grows when:** Streak increases (interventions become less frequent), resistance types get resolved, hard things complete faster, avoidance count per hard thing decreases.

**Atrophies when:** Streak keeps resetting at 0-2, same resistance type persists 4+ weeks, hard things sit 7+ days without progress, Richard dismisses interventions without reason.

| Metric | Current | Target (30d) | Target (90d) |
|--------|---------|--------------|--------------|
| Current streak | 0 | 5+ days | 10+ days |
| Avg days to complete hard thing | — | < 5 days | < 3 days |
| Avoidance count per hard thing | 3+ | < 2 | < 1 |
| Resistance types active | 6 | 4 | 2 |
| Interventions per session | — | < 2 | < 1 |

**End state:** Richard self-selects the hard thing, starts without prompting, ships without delay. The organ becomes quiet — not atrophied, but strong enough that behavior is automatic.

---

## When to Read This File
Every session start (check streak + hard thing). When Richard drifts to comfort zone. When trainer flags a STUCK pattern.
