---
inclusion: manual
---

# Mario-Peter Dichotomy — Agentic Development Ethos

Two passionate, principled voices on how to build with agents. They disagree on spec depth before first run, line-by-line review, and the dark factory. They agree on the things that actually matter — taste, saying no, system design, humans as the bottleneck, training-data mediocrity. The right call depends on context, not on picking a side.

Invoked manually when making architecture / spec / workflow decisions that have "how much rigor before shipping" tradeoffs.

## The Two Voices

**Mario (pi / terminal-bench)**: Cut the slop. Read every line of critical code. Sufficiently detailed spec is a program — blanks get filled with the median of the training set, which is mediocre. Agents don't learn the way humans do, so don't expect memory systems to save you. Slow the [expletive] down.

**Peter Steinberger (OpenClaw)**: The way to the mountain is never a straight line. Waterfall kills exploration. Extensions over forks. Hacker advantage — enterprises can't do what personal tools can. Taste is a smell, not a rubric. Dreaming reconciles memories into durable structure. Run it, iterate, customize. Also: saying no is the most valuable skill right now.

## Where They AGREE (these are the load-bearing principles)

| Principle | Mario's version | Peter's version |
|---|---|---|
| **Taste is the moat** | Humans feel pain, agents don't — humans steer toward good work | Taste is a smell; taste lives in the delightful details |
| **Saying no** | "Learn to say no. Your most valuable capability at the moment." | "Saying no... the wildest idea is just a prompt away, but how all of that fits together is the problem." |
| **System design thinking** | Scope tasks so agents find all the context they need | "System design is still very important. You will eventually swipe yourself into a corner." |
| **Humans as bottleneck** | Humans are failable but they can learn and feel pain | "We're still bottlenecked on thinking and big-picture thinking" |
| **Training data is median** | "90% of code on the internet is our old garbage" | Agents have learned complexity from the internet, and the internet is mostly old garbage |
| **Structural over vigilant** | Defense in depth as anti-pattern | Sandboxing + structure > reviewing every line |

When these principles conflict with something else, these win.

## Where They DISAGREE (read the context before choosing)

| Question | Mario says | Peter says |
|---|---|---|
| How much spec before first run? | Sufficiently detailed — blanks cause slop | First idea is never final — iterate in small steps |
| Dark factory (never reading code)? | "Congratulations, something is broken." | "More and more doable" — with taste + system design |
| Line-by-line review? | For critical code, always | For critical parts, yes — rest is agent work |
| Review fatigue handling? | Review less by scoping tighter | Structure so most of it doesn't need review |
| Audience model | Open-source at scale, nation-state threats | Personal tool or carefully-installed product |

## The Decision Matrix — When to Apply Which

| Situation | Mario ethos | Peter ethos |
|---|---|---|
| Production code, shared systems | YES | — |
| Personal tools you own | — | YES |
| Hard-to-reverse changes | YES | — |
| Exploration, new directions | — | YES |
| Work you'll hand to others | YES | — |
| Work that's yours and only yours | — | YES |
| Critical systems (auth, infra, data) | YES | — |
| Aesthetic / taste-driven work | — | YES |
| One-shot audit or cleanup | YES (rigor before execution) | — |
| Building the next-version-of-your-system | — | YES (iterate into shape) |

Richard's personal body system is mostly Peter-territory with Mario-corners (anything that touches Amazon production, anything shared with the team).

## Applications to Agentic Development

**When designing a new agent or workflow**: start Peter. Ship a scrappy version, see what surfaces, iterate. Spec comes from the pain of the first run, not from imagination.

**When cleaning up an accumulation problem**: start Mario. Once something has sprawled, pure iteration makes it worse. Rigor before execution. This is what the system-subtraction-audit is.

**When deciding between plug-in and monolith**: Peter wins. Extensions over forks. Minimal core + well-defined API + hot-reload. Applies to everything from body organs to writing-style agents.

**When reviewing generated code before shipping**: Mario wins for anything touching production, auth, data, or shared infra. Peter wins for personal tools where the blast radius is your own workflow.

**When deciding how much to document**: if an agent on a different platform needs to execute without access to your hooks/MCP/subagents, Mario — write it all down, explicit, portable. If it's a throwaway or you'll iterate it out of existence, Peter — skip the docs.

**When feeling stuck in spec-tuning loops**: Peter. Four rounds of requirements edits without running v1 is the waterfall trap. Ship the scrappy version. Learn from it. Update the spec from reality, not imagination.

**When an agent is being asked to delete things, change production systems, or make hard-to-reverse calls**: Mario. Explicit approval, dependency-ordered execution, atomic operations, resumable on failure, content preservation. The audit's R9 Execution Safety is the Mario-pattern.

## The Underlying Principle

Rigor is a cost, not a virtue. Pay it where the downside of being wrong is high; skip it where iteration can reveal the right answer faster than reasoning can.

Speed is a cost, not a virtue. Spend it where first-run pain teaches more than planning would; avoid it where mistakes compound silently or irreversibly.

Neither Mario nor Peter is wrong. They're calibrated to different risk profiles, and both failure modes are real: Mario's risk is spec paralysis and over-engineering; Peter's risk is slop and forgotten-about complexity. Match the ethos to the situation, check the agreement list when in doubt, and when both point the same way (which is most of the time), that's probably the right answer.

## For Agents Reading This

When Richard asks you to do something agentic — build a tool, spec a workflow, review a system, cut complexity — pause and ask:
1. Which end of the Mario-Peter axis does this live on?
2. Does the situation actually call for the ethos Richard defaults to, or the other one?
3. What do both agree on? (Taste, saying no, system design, humans-in-loop, training-data mediocrity — if one of these is in play, it trumps the dichotomy.)

Don't reflexively apply Mario-rigor to exploratory work. Don't reflexively apply Peter-speed to production cleanup. Name which ethos fits and why, then proceed.
