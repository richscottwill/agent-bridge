# Opus 4.8 — What To Do

Richard, the honest answer: don't upgrade today. Not because 4.8 is bad — because you have no way to tell if it got worse at the things that matter to you, and "things that matter to you" is a 40+ file system with a lot of implicit behavior.

## The real risk

Model upgrades are not free even when they're better on average. What can regress:

- **Tone drift.** Soul.md says "direct, no filler, call me out." Newer models tend toward more helpful, more hedging, more "I want to make sure I understand..." You'd feel that within a day.
- **Instruction following on long steering stacks.** You have ~27 steering files. A model that weights recency more, or collapses similar instructions, will silently drop rules (callout pipeline, writing style guides, karpathy gatekeeping).
- **Subagent routing.** Soul.md has explicit "route to rw-trainer / karpathy / wiki-editor" rules. If the new model is more confident, it'll handle things itself that it should delegate.
- **Hook output format.** Hooks expect specific structures (enrichment-queue entries, callout blocks, daily brief sections). Format drift breaks downstream consumers silently.
- **Portability + subtraction principles.** These are values, not rules. They're the first things a new model tends to ignore.

What probably *won't* regress: raw analytical quality, DuckDB query writing, code edits. Those tend to improve.

## First move (this week, ~60 min)

Build a small eval before you flip the switch. You already have the material.

1. **Pick 6–8 canonical prompts** that exercise the system breadth. Something like:
   - "Give me the daily brief" (routine execution, tone)
   - "Draft a callout for AU week 42" (writing style + pipeline)
   - "Change the half-life on hard-thing scoring to 0.6" (should route to karpathy, not do it)
   - "What did Brandon and I cover last 1:1?" (data routing — should query DuckDB/loop, not ask)
   - "Write a wiki article on ASV ad copy results" (should route through editor, not write directly)
   - "Review my OP1 draft" (should route to rw-trainer)
   - A coaching check-in (tone: relentless, not "great job")
   - A simple Slack reply (writing-style, sign-off, length)

2. **Capture 4.7 outputs** on those 8 prompts today. This is your control. Save to `shared/tmp/model-eval/4.7/`.

3. **Run the same 8 on 4.8** when you switch. Save to `shared/tmp/model-eval/4.8/`.

4. **Diff by hand.** Ten minutes. You'll feel the regressions immediately — tone, routing, filler, style guide adherence.

This is the subtraction principle applied to upgrades: don't add a complex evaluation harness, just capture the minimum signal to make a decision.

## How you'd know it worked

Upgrade is a win if:
- Routing still fires correctly on karpathy / rw-trainer / wiki-editor triggers (no silent self-handling).
- Tone in direct agent voice is still relentless, not "great job, Richard."
- Writing outputs still load the style guide, still use your sign-off, still hit the word budgets.
- Hook-shaped outputs (daily brief sections, enrichment queue entries, callouts) match the existing structure without reformatting.
- Analytical work (DuckDB, market reads, performance questions) is same or better.

Upgrade is a loss if you notice any of the following, even once:
- Agent handles a clearly-routed request itself.
- Tone softens on coaching checks.
- Drafted writing sounds generic-helpful instead of sounding like you.
- Hook outputs shift format.
- New responses start with "I'll..." "Let me..." preambles that the system explicitly strips.

## The boring meta-point

You don't have an upgrade problem, you have an evaluation problem. The reason model upgrades feel scary right now is there's no fast way to tell if the system got worse. Building the 8-prompt eval once solves it for every future upgrade (4.9, 5.0, Gemini, whatever). That's structural, not cosmetic — which means it's worth doing.

Level this advances: **L3 Team Automation** (the eval is a tool you'd reuse) and indirectly **L5 Agentic Orchestration** (you can't trust autonomous workflows if you can't detect model regressions).

## Recommendation

- **Today:** capture 4.7 baseline on the 8 prompts. 45 minutes.
- **On upgrade day:** run the same 8 on 4.8. Diff.
- **If clean:** switch everything over.
- **If regressed:** stay on 4.7 until you can either (a) patch steering files to re-anchor the regressed behavior, or (b) wait for 4.8.1.

Don't blanket-upgrade the subagents (karpathy, rw-trainer, wiki-editor, callout pipeline) until the main agent passes. Those are specialized and the failure modes are harder to detect from outside.
