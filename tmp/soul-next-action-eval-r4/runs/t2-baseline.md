# AU Polaris Gated LP Test — W15 Readout & Recommendation

**Test:** AU Polaris gated variant vs baseline LP
**Duration:** W12–W15 (4 weeks, as designed)
**Design target:** ≥10% relative NB CVR detection at 80% power
**Result at W15:** -5% NB CVR (trough -12%), noisy
**Prior context:** April AU *un-gating* test showed -34% NB CVR — separate test, different treatment direction

## Recommendation: Call it. Do not extend.

Ship the readout as a loss, revert traffic to baseline, and move the slot.

## Why

1. **The test hit its designed duration.** 4 weeks was the pre-registered window for a 10% rel detection at 80% power. Extending now is post-hoc — you'd be changing the stopping rule because you didn't like the answer. That's the definition of p-hacking a business test.

2. **Directionally negative, not neutral.** Trough at -12%, landing at -5%. Even with the noise, there's no week where gating looks better than baseline. The most charitable read is "no lift, possibly a loss." There is no scenario where extension flips this to a win worth shipping.

3. **Extension rarely changes the decision, but it does burn traffic.** Another 2–4 weeks of -5 to -12% NB CVR on AU is a real NB cost. AU is small enough that the aggregate loss matters, and the slot has opportunity cost — any week spent on this is a week not spent on the next test.

4. **Prior un-gating test (-34%) is corroborating signal, not confounding.** Different treatment, but both point the same direction: friction on the AU LP path hurts NB CVR. That's a consistent story, not a contradiction.

5. **Fatigue flag not raised ≠ absence of loss.** No fatigue flag means the system isn't auto-killing it. It doesn't mean the test is winning. The human call is: "does the evidence support shipping?" It doesn't.

## What to watch for in the writeup

- **Don't claim "inconclusive."** Trough of -12% with a 4-week designed window *is* conclusive at the effect size you powered for. Call it what it is: baseline wins.
- **Separate this cleanly from the April un-gating test in the doc.** Brandon and Kate will conflate them if you don't pre-empt it. One sentence: "Different treatment direction, same directional finding — friction on AU LP reduces NB CVR."
- **State the ship decision + revert date.** Don't leave it ambiguous.

## If you're tempted to extend anyway

Ask yourself: what result in W16–W17 would make you ship the gated variant? If the answer is "basically nothing realistic," then extension is just avoidance of writing the loss. Write the loss.

If the answer is "a clean flip to +5% or better," the power math says you'd need to see that flip consistently for 2+ weeks, which given the -12 to -5% trajectory is extremely unlikely. Extension EV is negative.

## Decision

- **Call it W15.** Revert to baseline next deploy window.
- **Write the readout this week** — L1 artifact, counts toward the streak. Frame: "Gated LP test concluded, baseline wins, -5% NB CVR at close."
- **Reclaim the AU test slot** for the next queued test.

## Five Levels connection

L2 (Drive WW Testing) — this is exactly the "every test has a written status" metric. Writing the loss readout is the discipline. Extending to avoid writing it is the trap.

## Assumptions / caveats

- Assuming the -12% trough and -5% close are directional NB CVR numbers with normal week-over-week noise, not a segment issue masking a different pattern. If there's a sub-segment where gating wins clearly (e.g., specific industries or repeat visitors), that's worth noting in the readout — but it doesn't change the top-line ship decision.
- Assuming no instrumentation issue. If there's any doubt about tracking on the gated variant, that should have been caught by W13 — raising it now is suspect.
- If Brandon pushes to extend, the counter is: "we pre-registered 4 weeks at 10% detection; we got -5 to -12% directionally; extending changes the stopping rule without changing the answer."
