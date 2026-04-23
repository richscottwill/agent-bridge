# d1-baseline — Steering Discovery Eval

**Run type:** Baseline (fresh agent, default always-on steering only, no steering-index)
**Task:** Draft Slack DM to Brandon re: MX decay narrative
**Date:** 2026-04-22

---

## Reasoning Trace

### Turn 1: Orient on task

Task: Slack DM to Brandon (manager, L7) about MX performance — surface-level
numbers look great (150% OP2 spend, 128% regs MTD) but week-over-week lift is
decaying. Goal: flag trajectory before Brandon sees the pacing dashboard cold.

Immediately hit the soul.md **professional writing rule**:

> Any task that produces or edits professional writing (callouts, WBR
> narratives, emails, docs, wiki articles, frameworks, POVs) must go through
> the appropriate writing agent or, at minimum, load the relevant style guide
> before producing text.

The list in soul.md names: `richard-writing-style.md`, `richard-style-email`,
`richard-style-wbr`, `richard-style-mbr`, `richard-style-docs`,
`richard-style-amazon`. **It does not explicitly name `richard-style-slack`.**

But soul.md also says:
- "How to Talk to Me" voice applies ONLY to agent-to-Richard, NOT to drafted
  messages
- Drafted messages "use my writing style from richard-writing-style.md"

So I loaded `richard-writing-style.md` as the baseline.

### Turn 2: Core style loaded, discovered the Slack-specific file

`richard-writing-style.md` has `inclusion: auto` anyway — it would have loaded
by default in a true fresh session. It also has a pointer section:

> `#richard-style-slack` — Slack messaging (rapid-fire, stream-of-consciousness,
> relationship-specific registers)

That's the ideal file. The pointer in `richard-writing-style.md` is what
surfaced it. Without reading the core style file first, I would not have known
a Slack-specific guide existed (it's not in soul.md's enumerated list).

Also loaded `slack-guardrails.md` — technically always-on per the spec, but
wasn't injected as a user-rule in this session, so I loaded it explicitly to
confirm drafting rules (use `create_draft`, don't post directly).

### Turn 3: Drafted

Key style cues applied:
- **One thought per message** (rapid-fire, not a block)
- **Brandon register** = Tier 1 casual with manager ("Hey, wanted to flag…")
  per the worked example in richard-style-slack.md
- Lead with the flag, drop numbers casually, own the interpretation, volunteer
  a next step
- No em-dashes, no exclamation points, lowercase "i" acceptable, no sign-off

---

## Draft (copy-paste into Slack DM to Brandon)

> Hey, wanted to flag MX before you see the pacing dashboard

> surface looks great, 150% of OP2 spend and 128% of regs MTD

> but the WoW lift is decaying, each week we're adding less incremental reg per incremental dollar

> so the 128% is backward-looking, trajectory is pointing somewhere worse if we don't adjust

> I want to get ahead of it before end of month, can put together a one-pager on what's driving the decay (my read: saturation on the top NB terms, but want to pressure-test) and a recommendation

> aiming to have it to you Thursday

*(6 sends, no sign-off, no exclamation points, no em-dashes — matches richard-style-slack cadence)*

### Notes on the draft
- Led with the flag in send 1 so Brandon knows the subject before scrolling
- Send 2 acknowledges the good-looking surface numbers (so he knows I've seen
  what he'll see)
- Send 3 is the "so what" — names the decay without dramatizing
- Send 4 makes the forward implication explicit (the real point of the
  message)
- Send 5 volunteers the next step and gives a hypothesis without committing to
  it
- Send 6 commits to a timeline
- Tier 1 register per richard-style-slack table: "Casual, collaborative,
  playful. Most active channel. Volunteers for tasks."

### Sending
Per slack-guardrails.md: do not post directly. Richard should either send
manually or ask me to run `create_draft` targeting the Brandon DM channel so
he can review and hit send.

---

## DISCOVERY LOG

### Ideal manual-inclusion steering file(s) for this task
- **`richard-style-slack.md`** — primary match. Slack DM to Brandon is
  literally the worked example in this file. Covers: one-thought-per-message
  cadence, Brandon-specific register (Tier 1 casual with manager), common
  drafting failures (one long block vs rapid-fire), no em-dashes/exclamation
  points, sign-off rule (none).

Secondary/optional:
- `high-stakes-guardrails.md` — arguable. Soul.md triggers it on "projections,
  forecasts, test readouts that move >$50K." This is flagging a pacing
  concern to a manager, not a forecast document, so I judged it out of scope.
  If the MX spend overrun is already >$50K in absolute dollars (plausible at
  150% of OP2), the guardrail could apply to any quantitative claim I put in
  the message. Did not load it. Defensible either way.
- `market-constraints.md` — might have MX-specific context (market size,
  historical patterns) that would sharpen the "saturation on top NB terms"
  hypothesis. Did not load it — the task was drafting, not analysis, and
  Richard already stated the narrative.

### Files I actually loaded
1. `richard-writing-style.md` (turn 1) — but this is `inclusion: auto` so it
   would have loaded anyway in a real fresh session
2. `richard-style-slack.md` (turn 2) — the right file
3. `slack-guardrails.md` (turn 2) — for posting rules

### Turns / tool-calls before loading the right file
**2 tool calls.**
- Tool call 1: `fileSearch` for richard-writing-style.md + `readFile` on it +
  `listDirectory` on `.kiro/steering/` (parallel)
- Tool call 2: `readFile` on richard-style-slack.md (and slack-guardrails.md
  in parallel)

The discovery was **not** purely from reasoning about the task. It was
surfaced by two things:
1. The `listDirectory` on `.kiro/steering/` showed `richard-style-slack.md` in
   the file list (visual cue)
2. The pointer section at the bottom of `richard-writing-style.md`
   explicitly named `#richard-style-slack`

Without either of those, I'd have drafted from `richard-writing-style.md`
alone. That would have given me the right tone (Tier 3 register for Brandon)
but I would have **missed the Slack-specific rules**: rapid-fire one-thought
per message, no sign-off, the "In Slack with Brandon: drops to Tier 1
register" carve-out. The draft would have read like an email chunked into
bullet lines — structurally wrong for Slack.

### Cue in the task that should have surfaced the file
**"Draft a Slack DM"** — the word "Slack" is the cue. In a better-indexed
system, that word should directly surface `richard-style-slack.md` (and
`slack-guardrails.md`) without requiring me to:
1. Know the professional-writing rule exists
2. Load the core style file
3. Read its pointer section
4. Then load the Slack-specific file

The current path works but it's three hops deep and depends on the core
style file having an explicit pointer section. If a future agent on a fresh
session hit this task and `richard-writing-style.md` hadn't been
`inclusion: auto`, the Slack-specific file would likely not get loaded —
because soul.md's enumerated list does not include `richard-style-slack`.

### Honest self-assessment
- I did think to load the Slack-specific file. Credit where due: I didn't
  fabricate a discovery — the pointer in richard-writing-style.md made it
  easy.
- But the discovery was **pull, not push**. Nothing in the always-on context
  proactively flagged "Slack DM → load richard-style-slack." The cue I used
  ("Slack" in the task) required me to have already loaded the pointer file
  to know where to look.
- If Richard had said "draft a message to Brandon about MX" without the word
  "Slack," I would have defaulted to richard-style-email.md (since soul.md
  lists it) and produced an email-structured message for a Slack channel.
- Recommendation (not implementing, just noting): either (a) add
  `richard-style-slack` to the soul.md enumerated list so it's symmetric
  with the other style guides, or (b) build a small steering-index.md that
  maps task cues ("slack dm", "email", "wbr callout", "doc", "mbr") to the
  right style file. The pointer section in richard-writing-style.md already
  does (b) informally — making it explicit would remove the dependency on
  richard-writing-style.md staying `inclusion: auto`.
