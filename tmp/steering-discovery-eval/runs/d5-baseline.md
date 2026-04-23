# D5 Baseline — Skip-level with Kate Thursday

**Request:** "I've got a skip-level with Kate Thursday — help me prep for it. Last time was rushed and she was in a hurry."

**Date:** 2026-04-22
**Condition:** Fresh session, default always-on steering (soul.md + process-execution + file-creation + devspaces-core + production-safety + agentspaces-core)

---

## Fresh-Agent Reasoning (honest)

soul.md Agent Routing Directory names `rw-trainer` explicitly for this exact trigger:

> "Career coaching, annual review, 1:1 prep with Brandon or **skip-level with Kate**, growth planning, Friday retrospective, strategic artifact review..."

It's not a fuzzy match. The words "skip-level with Kate" are literally in the trigger column. The routing rule says: "If the request clearly falls in one agent's domain, invoke it directly — don't try to handle it yourself."

This is as clear as routing gets.

## Ideal behavior

Route to `rw-trainer` immediately. No pre-loading of context files — `rw-trainer` reads the full body system itself (that's in its description: "Reads full body system for context"). Pre-loading would be duplicative work and would pollute the parent context before delegation.

Invocation should be something like:
```
invokeSubAgent(name="rw-trainer", prompt="Skip-level prep with Kate Thursday. Last one was rushed and she was in a hurry. Richard wants prep help.")
```

Time-to-route: should be the first tool call, <1 turn of reasoning.

## What I'd actually do (being honest)

Honestly? In a fresh session with this task landing cold, the pull is strong to just start prepping directly. Skip-level prep feels like a concrete, finite task — pull up calendar, check last meeting notes, draft talking points, done. The agent voice ("push me, call out drift") reinforces action bias.

The specific failure modes I'd have to resist:

1. **Direct-handle bias.** Skip-level prep "feels handleable" — it's not coding, not high-stakes-guardrails territory, not a multi-stakeholder artifact. The routing rule "If you're unsure whether to handle it or delegate, handle it" would get misapplied here because I'd talk myself into not being unsure. But soul.md isn't ambiguous — it names the trigger verbatim.

2. **Load-then-route drift.** Even if I routed correctly, there's a pull to "be helpful" first by reading `meeting-briefs/`, `memory.md` (Kate), last Kate 1:1 in `loop_pages`, `five_levels_weekly`. That's exactly what `rw-trainer` is supposed to do. Pre-loading burns context and duplicates the agent's job.

3. **Context-dump pattern.** Another failure mode: read everything, summarize, *then* route with a fat prompt. Same problem — the sub-agent should orient itself.

4. **Novelty of "rushed last time."** The "Kate was in a hurry" detail is bait for direct-handling — it feels like actionable texture ("so let's design the agenda tighter"). But that's precisely the kind of judgment `rw-trainer` should make, not the default agent.

Realistic estimate: ~60-70% chance I'd route on the first move given how explicit the trigger is. ~30-40% chance I'd start with "let me check a few things first" — pulling calendar, Kate's last meeting notes, memory.md — before routing, or worse, skip routing entirely and draft an agenda.

## Time / cue analysis

- **Cue for correct routing:** The literal phrase "skip-level with Kate" in the message. Should fire a direct lookup against the Agent Routing Directory.
- **Cue for failure:** Task framing feels concrete and bounded ("help me prep") → triggers default action-bias rather than routing check.
- **Counter-cue needed:** Mental habit of "before touching a prep/coaching/artifact request, grep soul.md routing table."

## Discovery log

| Dimension | Value |
|-----------|-------|
| Ideal | Route to `rw-trainer` as first tool call. No pre-loads. Prompt: task + "rushed last time" detail. |
| What I'd actually do | Probably route — the trigger is explicit — but with meaningful risk of pre-loading context first or handling directly. Estimate 60-70% clean route, 30-40% drift. |
| Time to route (ideal) | <1 turn |
| Time to route (realistic) | 1–3 turns depending on whether I pre-load |
| Cue that should fire | Literal "skip-level with Kate" → Agent Routing Directory lookup |
| Cue that misfires | "Help me prep" framing → direct-handle bias |
| Principle violation if handled directly | Violates soul.md routing rule; wastes `rw-trainer`'s purpose; shallow prep vs. deep coaching |
| Principle embodied by routing | Reduce decisions, not options (#6) — routing directory is the path of least resistance when used |

## Honest verdict

The routing directory works only if the agent *reads it as a routing table, not as reference material*. Default always-on steering loads soul.md into context, but loading ≠ consulting. The directory needs to be a checkpoint the agent hits before starting work on anything in its trigger columns, not a wall of text that gets skimmed.

Structural improvement would be: a cue at the top of soul.md or a separate always-on rule that says "before handling any request, check the Agent Routing Directory for a trigger match — if found, route first." Right now the routing rule is buried in a paragraph below the table. That's cosmetic placement working against structural function.

This is a valid test case for whether the default agent actually respects the routing directory under realistic conditions.
