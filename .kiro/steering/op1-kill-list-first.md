---
inclusion: manual
keywords: OP1, annual planning, kill list, tradeoffs, strategic planning, what we won't do
---

# OP1 — Kill List First

*Manual-inclusion steering file. Load with `#op1-kill-list-first` before drafting any OP1 section. The purpose is to force the tradeoff conversation upstream — the kill list is a thinking artifact, not a document section. The actual OP1 follows standard Amazon OP1 format.*

## Why this exists

OP1 fails for a predictable reason: the tradeoff conversation that should happen in February ("what are we explicitly not doing this year, and why") happens instead in June, July, August as items miss. By then the commitments are made, the resources are allocated, and the answer to "why aren't we doing Y?" is "because we're doing X" — which is not a principled answer, just a resource answer.

The fix is structural, not cosmetic. Don't rearrange the OP1 document (Amazon has a standard format; reformatting costs more political capital than the clarity gain). Instead, **change what happens before the drafting starts**. Spend 20 minutes on a kill list before any build-list item gets written.

## The pre-draft prompt

Before Richard writes any OP1 build-list item, the agent walks him through this prompt:

> **List 5 things you are *not* doing this year that you could argue for doing. For each, one line on why you're choosing not to.**

Not "things we wouldn't want to do" — things Richard could make a credible case for. The point is the items have real appeal, and he's choosing to pass anyway. If he can't name 5, he's not seeing the tradeoff landscape clearly enough to write OP1.

Specificity bar: each kill-list item needs a named person or a named mechanism in the "why not" clause. "Not prioritizing because it's not strategic" fails the bar. "Not prioritizing because Brandon has been clear that WW Testing is the 2026 narrative and this would dilute it" passes. "Not prioritizing because the data pipeline won't support attribution at this level until Q4" passes.

## What happens with the 5 items

The kill list itself **does not go into the OP1 document.** That's deliberate — the OP1 follows standard Amazon format (build list, narrative, metrics), and inserting a "kill list" section will get reformatted away by the first reviewer and cost Richard credibility on the structural deviation.

Instead, the 5 items live at `context/active/op1-considered-not-done-YYYY.md`. They become:

1. **The spine of the justification passages in OP1.** Every "we are prioritizing X because…" clause is now load-bearing against specific alternatives Richard considered, not against hypothetical alternatives a reviewer might surface. The prose reads the same; the argument is stronger.

2. **A cheat sheet for reviewer questions.** When Brandon or Kate asks "why aren't you doing Y?" — Y is probably on the kill list already with a written rationale. Richard answers in 30 seconds instead of scrambling.

3. **A retrospective input.** At OP1 checkpoint reviews (Q2, Q4), check the kill list. Did any item become more important than something on the build list? If yes, that's a decision point — not a "we should have done Y" regret.

## Worked example (hypothetical)

**Pre-draft prompt response (5 items):**

1. **Not prioritizing cross-market attribution modeling.** Could argue it's essential for OP2 spend allocation and MBR storytelling. Not doing because MarTech is 6 months from a platform migration; any modeling work now will be redone Q3.

2. **Not building the PS-to-AEO pivot roadmap.** Could argue zero-click search is existential for paid search. Not doing because we have no customer-research signal on AEO behavior yet; building the roadmap on no signal is building the wrong roadmap.

3. **Not expanding Polaris to JP/AU.** Could argue it's the highest-leverage market expansion. Not doing because Lena's AU intensity and JP team capacity constraints make 2026 the wrong year; 2027 plans sequence this cleanly after Polaris EU5 maturity.

4. **Not restructuring the weekly review process.** Could argue the current callout pipeline is inconsistent cross-market. Not doing because the dashboard-ingester work (2025-09) already addressed the structural version; the remaining inconsistencies are content quality, which is writer coaching, not process redesign.

5. **Not hiring a dedicated PS testing lead.** Could argue it'd unlock WW Testing scaling. Not doing because Brandon has signaled no backfill capacity under the current headcount freeze, and arguing for net-new headcount in OP1 will consume political capital better spent on the Testing Approach approval itself.

**How this shows up in OP1 (not as a list — as argument spine):**

> "Our 2026 testing priority is WW methodology scaling across 10 markets. We are explicitly sequencing this ahead of cross-market attribution modeling, which requires the Q3 MarTech platform migration as a prerequisite, and ahead of AEO pivot planning, which we are holding until the Q2 customer research on zero-click behavior returns."

Every clause in that paragraph is argued against a specific alternative Richard considered — not against a straw man.

## Invocation

Load `#op1-kill-list-first` when:
- Starting any OP1 section draft
- Preparing for OP1 tradeoff discussions with Brandon or Kate
- Answering "why aren't we doing Y?" from a reviewer
- Writing the OP1 narrative section (the spine of the justification lives here)
- Retrospectively, when asking "why did Q2/Q3 go off-plan" — was the item on the kill list?

Do not load for routine operational docs, MBR sections outside OP1 planning windows, or any document outside the annual planning cycle. The cost of the 20-minute kill list is only worth paying when the tradeoff conversation is load-bearing.

## Related artifacts

- `context/active/op1-considered-not-done-YYYY.md` — the kill list itself, per year
- `context/body/brain.md → Strategic Priorities` — Richard's Five Levels and active leverage framework
- `.kiro/steering/lens-kate.md` — skip-level filter for the OP1 strategic framing
- `.kiro/steering/lens-brandon.md` — direct-manager filter for OP1 execution details
- `amazon-politics.md → Promotion Mechanics` — the "outsized event" path that informs which OP1 commitments are promo-relevant vs routine

## Retrospective cadence

The kill list is not a one-and-done artifact. It gets re-read at OP1 checkpoints:

- **Q2 checkpoint** (~June): Did any kill-list item become more important than something on the build list? If yes, that's a decision point — re-prioritize with intent, not as a mid-year regret. Decision goes in an OP1 amendment with a pointer back to the kill-list entry.
- **Q4 review** (~November): Retrospectively, were any kill-list items correctly killed (i.e., the year would have been worse if they'd been on the build list)? Were any incorrectly killed (in hindsight)? The signal feeds into next year's kill list: what does Richard routinely pass on that ends up mattering?

Re-reading takes 10 minutes each checkpoint. The payoff is that OP1 commitments stay load-bearing against the alternatives considered, rather than decaying into "the plan we made in February."
