# Re: "I keep re-explaining our test framework to new teammates"

**Date:** 2026-04-22
**For:** Richard
**Steering lens active:** Steinberger Agentic Engineering Upgrades

---

## Short answer

It's structural, not cosmetic. And the fix is subtraction + one missing artifact, not a rewrite.

## What's actually going on

You have two docs, and neither one is built for a new teammate:

- **`testing-approach-kate-v5.md`** — a Kate-audience synthesis. It opens with "In 2025 the team delivered +35,196 regs and $16.7MM OPS" and ends with an OP1 investment table. A new hire reading this learns what the team *accomplished*, not how you *work*. The four-stage methodology is buried in the appendix.
- **`testing-methodology.md`** — closer, but the first line is "The PS team follows a consistent methodology across all workstreams" and the closing section is titled "Why This Matters" — framing language aimed at a reader who already understands the stakes. It's the methodology as pitched to an executive reviewer, not as taught to a new teammate.

So when a new person joins, there's no artifact you can actually point them at. They ask, you explain, they forget the edges, they ask again, you explain again. You're not re-explaining because the docs are wrong — you're re-explaining because the right doc doesn't exist.

**This is a structural gap, not a cosmetic one.** Reformatting either file won't fix it. Adding emojis or a TL;DR won't fix it. The onboarding artifact is missing.

## Diagnosis against your 6 "How I Build" principles

| Principle | Check |
|---|---|
| Routine as liberation | Failing. The "onboard new teammate" routine has no pre-loaded content, so every instance burns willpower. |
| Structural over cosmetic | The fix is structural — create the missing artifact, don't reskin the existing ones. |
| Subtraction before addition | Before writing anything new, ask: can `testing-methodology.md` be *split* so the teaching part extracts cleanly? (Likely yes — see below.) |
| Protect the habit loop | Adding an onboarding doc doesn't disrupt any existing routine. Safe. |
| Invisible over visible | A one-page primer makes re-explaining disappear. You won't notice it working — which is the point. |
| Reduce decisions, not options | You keep both existing docs. You just add the path-of-least-resistance entry point. |

Five of six green. One flags a subtraction opportunity worth checking before building.

## The recommendation

Create **one artifact** — call it `testing-framework-primer.md` or `how-we-test-101.md` — designed for exactly the "new teammate, first week" audience. ~500 words, one page. It should answer:

1. **What's our framework in one sentence?** (Hypothesis → phased rollout → measurement → scale or stop.)
2. **When do I use which measurement method?** (The table already in `testing-methodology.md` — lift it.)
3. **What does a test look like end-to-end?** (One worked example — OCI or in-context reg. Not five.)
4. **Where do I go for more?** (Link to `testing-methodology.md` for depth, `testing-approach-kate-v5.md` for the 2025/2026 strategic context, and the workstream-specific docs.)

That's it. No 2025 results narrative, no OP1 investment pitch, no appendices. Those already exist in the other docs — don't duplicate them.

### The subtraction question first

Before writing the primer, open `testing-methodology.md` and ask: can the teaching content (the four stages + the measurement table + the worked examples) be extracted as-is into a new file, leaving behind only the executive framing? If yes, you're not adding a new doc — you're splitting an existing one that's trying to serve two audiences at once. That's the cleaner move.

My read from skimming it: the four-stage detail is already there, but it's wrapped in "operating system" / "why this matters" framing. A split would leave `testing-methodology.md` as the executive version and extract a clean teaching version. ~1-2 hours of work.

## Steinberger-lens notes

- **Design for agent navigation first** — applies to human agents too. A new teammate is an unprimed agent. They need a registry-first entry point. Right now there isn't one.
- **Iterate toward outcomes, not perfection** — don't over-engineer the primer. Ship a rough version, watch the next new hire use it, fix the parts that confused them. Two iterations gets you to stable.
- **Treat the agent like a capable employee** — the primer should end by telling them *what to do next* (read one workstream doc, shadow one WBR, read one test readout), not hand-hold through every possibility.

## Human review flag

This is a low-stakes structural change (internal doc, not a leadership artifact, no budget impact). No confidence scoring needed. Ship it.

## Suggested next step

One task, one hour: open `testing-methodology.md`, mark which paragraphs are teaching vs. which are framing, and see if a clean split falls out. If yes, split. If no, draft the 500-word primer from scratch using the four-stage table as the spine.

Which level does this advance? **Level 2 (Drive WW Testing).** You own the methodology; making it teachable without you is part of owning it end-to-end. It also quietly advances Level 3 (Team Automation) because a good primer is the first step toward the framework running without you in the room.

---

*Thanks,*
*Richard's agent*
