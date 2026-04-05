# Eval B: Workstream 3 — Audiences and Lifecycle (v3)

Reviewer: wiki-critic (blind, no knowledge of Eval A)
Reader persona: Kate reviewing workstream detail behind Testing Approach doc. 10 minutes.
Date: 2026-04-05

## Scores

| Dimension | Score | Assessment |
|-----------|-------|------------|
| First Paragraph | 9/10 | Opens with the number ($765K iOPS), names the reader (Kate), states the purpose (Testing Approach evidence base), and makes a clear promise of what you'll know after reading. Does everything a first paragraph should do. |
| Shareability | 8/10 | Kate could hand this to a VP and it stands alone. Question headers make it scannable. Names and teams attributed throughout. The cross-functional partners section is a prose wall — the one place where a reader looking for "who owns what" has to parse sentences instead of scanning. |
| Actionability | 6/10 | The doc explains what happened and what's planned, but the F90 section reads as a status update rather than a decision document. Risks are stated but not framed as choices. Kate finishes knowing the story but not what she needs to do about it. The "What did we learn" section states a mindset rather than a transferable action. |
| Signal-to-Noise | 6/10 | Three appendices repeat body content. Appendix A restates the 13% → 30% match rate. Appendix B restates $765K and Prime Day numbers verbatim. The cross-functional partners section re-attributes people already named inline. "What did we learn" is one paragraph that could be a sentence in the build section. Roughly 25% of the doc is redundant. |
| Voice | 8/10 | "This was not a Google feature or a platform toggle" — that's a person making a point. Question headers give conversational rhythm. "Platform limitations are problems, not constraints" lands. Minor mechanical transitions ("The problem was that," "The result:") don't break the flow. Reads like someone who knows the work wrote it. |

## Composite

**7.4 / 10**

## Does it ship?

No. Two dimensions below 7 (Actionability 6, Signal-to-Noise 6) and composite below 8.

The bones are strong — the narrative arc works, the voice is right, the first paragraph is nearly perfect. But the doc is carrying ~25% redundant weight in the appendices and cross-functional section, and the F90 section informs without enabling action. Those are fixable problems.

## What would get it to 8

1. **Kill Appendices A and B.** The match rate table and Prime Day numbers are already in the body with full context. Repeating them in an appendix adds tokens, not value. Keep Appendix C only if the Guest auto-expiration cross-reference (Workstream 4 link) is preserved — fold that single sentence into the F90 section and cut the appendix.

2. **Reframe the F90 section around the decision.** Currently reads: "the team is navigating Legal SIMs to launch F90." Should read: what needs to be true for F90 to launch, what's the decision point, and what does Kate need to know or do. The Legal SIM timeline is a dependency — frame it as "if X by April, then Y; if not, then Z."

3. **Fold "What did we learn" into the build section.** The insight ("platform limitations are problems, not constraints") is good but doesn't need its own H2. Add it as a closing sentence to the audience infrastructure section.

4. **Convert the cross-functional partners section to a compact list or table.** Every partner is already named in context in the body. This section's value is as a quick-reference lookup — prose format defeats that purpose. A 6-row table (Partner | Role | Status) would serve both audiences better and cut word count.

5. **Minor:** "The result:" in the Phase 2 paragraph is a mechanical transition. Let the sentence carry itself — "Match rate jumped from 13% to 30%" doesn't need a label.
