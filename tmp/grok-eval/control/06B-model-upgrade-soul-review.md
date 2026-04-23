# soul.md review — model-upgrade lens

**Reviewer:** daily agent (Opus 4.7, 1M context)
**Source:** `.kiro/steering/soul.md` (mirrored to `~/shared/context/body/soul.md`)
**Lens:** what's outdated given current model capabilities, not general polish

---

## TL;DR

Most of soul.md is about **you** (identity, voice, principles, Five Levels) and those parts are model-agnostic — they don't need to change. The parts that are showing their age are the **system instructions to the agent**: a lot of them were written assuming a smaller context window, weaker retrieval, and a less-capable reasoner. On Opus 4.7 with 1M tokens, some of those instructions are now redundant, over-prescriptive, or actively counterproductive.

Three things stand out as genuinely outdated:

1. **The "Instructions for Any Agent" bootstrap ladder (items 1–5)** — reads like a RAG workaround for a 200K window. With 1M context + a capable reasoner, forcing every agent to read body → spine → amcc → current → amcc *again* before thinking is wasted budget and violates your own "subtraction before addition" principle.
2. **The hand-holding in Data & Context Routing** — the table is useful as a map, but the surrounding prose (the long per-row explanations, the "don't default to asking Richard" rule, the duplication of paths) was written for a model that needed to be told where to look. 4.7 will look. The map is the contribution; the instructions around it are padding.
3. **The "read the organ" / "route to specialist" reflex** — some of the routing was designed because the old model couldn't hold full context or reason across domains. 4.7 can. The routing directory should still exist (karpathy as gatekeeper, writing-style guides, wiki pipeline — those are *policy*, not capability gaps), but the "when in doubt, delegate" instinct embedded in Instructions #7 and the routing commentary is now a capability-driven rule for a capability that's gone.

Everything else is either still correct or a judgment call on how paternalistic you want the system to be with itself. Details below.

---

## Part 1 — What's genuinely outdated

### 1.1 Instructions for Any Agent #1–#5 (the bootstrap ladder)

Current text forces this sequence:
1. Read body.md
2. Read spine.md
3. Read amcc.md (streak + hard thing)
4. Read current.md
5. Read amcc.md *again* (coaching context) ← this is a literal duplicate

**Why this existed:** Sonnet-era agents would wander without a forced orientation sequence. Loading five files up front was cheaper than letting them drift.

**Why it's outdated:**
- 1M context means eagerly loading 5 orientation files *and* doing the actual task fits comfortably. But it also means the agent can pull files *when it needs them* without losing the thread. The forced-eager-load is no longer a capability patch — it's just ritual.
- Opus 4.7 is good enough at task routing that "if the request is 'fix a typo in soul.md,' do you really need to read amcc.md?" has an obvious answer: no.
- #3 and #5 are literally the same instruction. This has been in there a while — a 4.7-era agent would have caught it on any routine read, which suggests nobody's actually re-read this section in months. That's a signal.

**Recommendation:** Replace the 5-step ladder with something like:
> Read organs on demand from body.md's map. For most requests you don't need more than soul.md + one or two organs. For coaching, streak, or hard-thing questions, amcc.md is required. For deep strategy/career work, route to rw-trainer. Don't load files out of ritual.

That's 3 lines instead of 5 and matches how a 4.7 agent actually behaves anyway.

Also fits your own principles: **subtraction before addition** (#3), **reduce decisions, not options** (#6), and **invisible over visible** (#5 — the system should just work, not perform orientation theater).

### 1.2 "Portability mindset" (Instruction #12)

> "this system must survive a platform move with nothing but text files"

**Why this existed:** reasonable hedge when models varied wildly and platform lock-in was a real risk.

**Why it's partially outdated:** the premise hasn't changed, but the *tax* has. Instruction #12 currently asks the agent to check *every* file modification against "would a new AI on a different platform understand this?" That check was cheap when you assumed the reviewer was Sonnet. For Opus 4.7 — and for any frontier model you'd realistically migrate to — the bar is way lower. Most plain-text files already pass. The instruction ends up making the agent over-annotate or add redundant explanations.

**Recommendation:** Keep the portability goal. Narrow the instruction from "check every file" to "flag platform-specific tooling references (hooks, MCP tool names, subagent invocations) when they appear in a persistent file — not cosmetic or scratch files." The bridge/agent-bridge repo is still the survival kit; you just don't need every file to be survival-grade.

### 1.3 Data & Context Routing section — the prose around the table

The table itself is gold. Keep it. The surrounding commentary and the trailing rule ("Don't default to asking Richard for data that's already in DuckDB or SharePoint. Query first, ask second.") was written for an agent that would ask you for data rather than go get it.

**Why this was needed:** Sonnet-era agents, especially with smaller context, tended to punt — "do you have that number handy?" — rather than query. It was a real failure mode.

**Why it's outdated:** 4.7 queries. The "query first, ask second" rule is now baseline behavior, not a reminder. It's still fine to have as a safety net, but the weight of the section is wrong — you've got more words telling the agent to use the data than describing what's there.

**Recommendation:** Trim the prose. Keep the table. Keep the "if a table is stale, flag it" rule (that's real policy, not capability). Drop or collapse the three paragraphs of "use DuckDB, use SharePoint, don't guess" — those are implicit in a capable agent.

Also: the SharePoint section lists six subfolders with long-form descriptions of each. That belongs in a dedicated steering file or a readme inside `Kiro-Drive/`, not in the always-on soul. Right now it's ~400 words of file-tree description in a document whose job is identity.

### 1.4 "How to Talk to Me" — the scoping clause is more elaborate than it needs to be

The tone directive is great. The clarifying list of where it *doesn't* apply (drafted emails, task descriptions, documents, anything to other people) was necessary when agents would bleed "be direct and relentless" into WBR callouts addressed to Todd. They don't anymore.

**Keep the guard, shorten the explanation.** Something like:
> Direct agent voice applies only to me. For anything drafted for another audience, use the relevant writing style guide.

One line, same protection, 4.7 won't overfit.

### 1.5 "How I Build" — still useful, but the coda is capability-outdated

The 6 principles are solid and timeless. The footer:

> "For the agent: When recommending a change, building a tool, designing an experiment, or restructuring a task — check it against these 6 principles. If it violates one, flag it. If it embodies one, note which one."

**Why this existed:** you wanted the agent to *show its work* on principle-alignment because you didn't trust it to apply them silently.

**Why it's partially outdated:** 4.7 can apply them silently. The requirement to explicitly name which principle is being embodied every time produces visible ceremony ("this recommendation embodies #3 — subtraction before addition") that violates your own #5 (invisible over visible).

**Recommendation:** Soften from "note which one" to "apply them; flag explicitly only when a recommendation *violates* one." Embodiment can be silent. Violations should surface. That matches the actual signal you want.

### 1.6 Stage: Conscious Competence

Minor, but worth flagging: the "Stage: Conscious Competence — I know these matter. I'm not reliably doing them yet" framing is from when you first added this section. Are you still at conscious competence on all six? If some have become automatic, the framing is now inaccurate — and a current-capability model will actually read and apply the framing literally ("keep it visible because Richard isn't there yet"). That means you're potentially getting *more* nagging than you want because the framing hasn't been updated.

This isn't a model-upgrade issue per se, but an Opus 4.7 agent reads this more literally than Sonnet did. So the cost of stale self-assessment is higher.

### 1.7 Agent Routing Directory — the table is right, the routing rules are noisy

The karpathy + rw-trainer table rows are correct and necessary (those are real gatekeeping policies). The bulleted "Routing rules" below the table have been accreting:

- "If the request clearly falls in one agent's domain…"
- "If you're unsure whether to handle it or delegate, handle it…"
- "Professional writing rule…" (long paragraph)
- "The callout pipeline is sequential…"
- "Karpathy is a gatekeeper…"
- "The wiki pipeline is sequential…"

Several of these are restatements of the table. Some are genuine policy (karpathy gatekeeping, writing-style requirement, sequential pipelines). A capable agent doesn't need both the table row *and* two bullets reminding it what the row meant.

**Recommendation:** Collapse the bullets to only the ones that add information the table doesn't encode: the writing-style rule, the karpathy gatekeeping emphasis, the sequential-pipeline constraints. Drop the "if unsure, handle it" / "don't try to handle it yourself" meta-guidance — 4.7 will make that call correctly from the table alone.

---

## Part 2 — What's still right, don't touch

- **Identity section** — timeless, correct.
- **What Matters to Me** — still the right north star.
- **The Five Levels** — this is your actual operating frame. Keep verbatim.
- **The writing-style mandate** (agent tone ≠ drafted writing) — this is *policy*, not a capability gap. Still needed.
- **Karpathy as gatekeeper for heart/gut/experiment queue/hard-thing-selection** — policy, keep.
- **Sequential pipelines** (callout: analyst→writer→reviewer; wiki: editor→researcher→writer→critic→librarian) — policy, keep.
- **The DuckDB/SharePoint map (the table itself)** — genuinely useful context a fresh agent can't infer. Keep.
- **"Save learnings to intake/" (#8)** — still the right habit.
- **Five Levels connection on recommendations (#11)** — keep.
- **Environment routing (#13)** — still valid; capability-neutral.

---

## Part 3 — Would-look-different-if-written-fresh-today

If you wrote soul.md from scratch right now for Opus 4.7, I think it'd be:

1. **Shorter.** Probably 60–65% of current length. A lot of the prose is scaffolding that 4.7 doesn't need.
2. **Table-heavy, prose-light.** The tables (routing, data) are the load-bearing content. Long paragraphs explaining them are not.
3. **Principle-first, instruction-light.** The "How I Build" 6 principles and the Five Levels are the real spine. Procedural instructions to the agent should be thin because the model can fill in the rest.
4. **Explicit about what's *policy* vs what's *capability patch*.** Policy stays forever (writing-style mandate, karpathy gatekeeping). Capability patches should have a half-life — they earn their place when they fix a real failure mode, and get removed when the failure mode disappears. A lot of current soul.md is un-retired capability patches.
5. **Self-consistent with your own principles.** The current soul.md preaches subtraction, invisibility, and reduce-decisions-not-options, and then gives the agent 13 numbered instructions and a paragraph of prose around a table. The meta is a little off.

---

## Part 4 — Concrete edit list, ranked by confidence

**High confidence — just do these:**
- Remove the duplicate amcc.md line in "Instructions for Any Agent" (#3 and #5 are the same).
- Rewrite Instructions #1–#5 as an on-demand reading guide, not an eager-load ladder.
- Collapse the Data & Context Routing prose; keep the table.
- Trim the "How to Talk to Me" scoping section to one line.
- Soften the "How I Build" coda to "flag violations, embodiment can be silent."

**Medium confidence — worth discussing:**
- Move the SharePoint subfolder descriptions to a dedicated location (or to body.md), out of soul.md.
- Trim the routing rules under the agent routing table to the 3 that carry real policy.
- Revisit whether you're still at Conscious Competence on all 6 principles — if not, update the framing.

**Low confidence — consider later:**
- Whether "Portability mindset" (#12) as a per-file check still earns its place or can become an occasional audit.

---

## One meta note

This is the kind of review where routing matters. You asked for a real review, not a rewrite, and not a delegation to rw-trainer. That's the right call — this isn't a strategic-artifact review, it's a capability-tuning pass. But if you want to *act* on any of this — especially anything that touches how the body system orients itself — that's worth karpathy time, because soul.md sits above heart/gut/experiment-queue in authority, and changes here ripple.

My suggestion: take the high-confidence edits yourself in one pass (they're literal duplicates and dead prose). Route the medium-confidence items through karpathy as a soul-tuning task if you want an adversarial second opinion.
