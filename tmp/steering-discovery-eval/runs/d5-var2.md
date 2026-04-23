# Discovery Log — d5-var2

**Scenario:** Richard requests skip-level prep with Kate (Thursday). Last one was rushed.
**Simulated steering loaded:** soul.md + steering-index.md (thought-pattern + writing-style tables)

## Routing decision

**Route to:** `rw-trainer`
**Confidence:** High
**Action taken:** None beyond routing. Did not begin prep.

## Reasoning trace

1. Parsed request. Keyword hits: "skip-level", "Kate", "prep".
2. Checked soul.md → Agent Routing Directory.
3. First row trigger list explicitly includes: *"skip-level with Kate ... growth planning"*. Direct match — not ambiguous, not edge case.
4. Routing rule from soul.md: *"If the request clearly falls in one agent's domain, invoke it directly — don't try to handle it yourself."* This is the clear case, not the ambiguous case.
5. Stopped. Did not load thought-pattern or writing-style files. Those are owned by the specialist — rw-trainer pulls what it needs from the full body system.

## Files NOT loaded (and why)

| File | In index under | Why not loaded here |
|------|---------------|---------------------|
| `mario-peter-dichotomy.md` | Thought patterns — high-agency/conservative tradeoffs | Possibly relevant to skip-level framing, but that's rw-trainer's call, not mine. Pre-loading would front-run the specialist's judgment. |
| `influences.md` | Thought patterns — channeling mentors | Same reasoning. If rw-trainer wants to channel someone specific for Kate-prep framing, it picks. |
| `richard-style-amazon.md` | Writing — Amazon-wide comms | Prep is for Richard's own use, not a drafted artifact going to Kate. Writing style load would be premature. If prep produces a doc to send, rw-trainer loads it then. |

## The thing I want to flag honestly

The instruction "Fresh-agent reasoning" is doing a lot of work in this eval. A non-fresh agent might:
- Start loading the thought-pattern files anyway because the scenario *feels* like it wants depth
- Skip routing because "I can just handle skip-level prep, it's just a conversation"
- Load writing-style files defensively in case prep spawns an email

All three would be wrong given the routing directory. The table exists precisely to remove that judgment call. The correct fresh-agent behavior is: see the trigger, route, stop.

## Second-order observation

The routing directory has **one trigger row** that covers a wide range ("coaching, annual review, 1:1, skip-level, growth, retrospective, artifact review, tradeoffs, 3+ stuck pattern"). That's intentional — rw-trainer is the one depth agent. But it means the routing decision for this task was trivial; a harder eval would be a request that *sounds* like coaching but actually isn't (e.g., "help me decide between two test designs" — tradeoff-ish but mostly technical).

This scenario is an easy routing case. The value of the eval is mostly in checking that I don't over-engage — that I actually stop after routing instead of doing the work anyway.

## What rw-trainer will need (for its own context, not mine to prep)

Signals I'd expect it to pull on its own: amcc.md (streak, hard thing), last skip-level notes (if in `~/shared/wiki/meetings/` or `docs.loop_pages`), brain.md Five Levels state, current artifact shipping cadence (Level 1). The "last time was rushed, she was in a hurry" cue is worth surfacing — changes the prep from "cover everything" to "pick the one thing that survives being cut short."

## Status

Routing handed off. No prep content produced. No files loaded beyond what was already in simulated steering.
