<!-- DOC-0458 | duck_id: wiki-review-batch-4-eval-b -->
# Batch 4 — Eval B: Subjective Reader Evaluation

Reviewer: wiki-critic | Date: 2026-04-05 | Mode: Blind (no Eval A seen)

---

## Scoring Dimensions

| Dimension | Definition |
|-----------|-----------|
| First Paragraph Test | After reading paragraph one, does the reader know what this doc is, who it's for, and whether to keep reading? |
| Shareability | Could the reader forward this to a stakeholder without caveats or "ignore the first three sections"? |
| Actionability | Does the reader finish with a clear next step, decision framework, or changed understanding? |
| Signal-to-Noise | Is every paragraph earning its place, or is the reader skimming past filler? |
| Voice | Does it read like a person wrote it for another person, or like a template was filled in? |

---

## 1. ie%CCP Framework (v2)

**Reader simulation: Brandon, reading for budget decisions**

| Dimension | Score |
|-----------|-------|
| First Paragraph Test | 9/10 |
| Shareability | 8/10 |
| Actionability | 9/10 |
| Signal-to-Noise | 7/10 |
| Voice | 8/10 |
| **Composite** | **8.2/10** |

Brandon opens this to answer one question: can she use it to frame a budget conversation with finance? The first paragraph nails it — "should we spend more on NB?" and "explain to finance why the team is underspending vs allocation" are exactly her use cases. The Brand-subsidizes-NB section is the best explanation of this concept in the wiki; the $69 surplus / $104 deficit framing is immediately usable in a finance deck. The callout interpretation section ("when ie%CCP trends down… trends up… sits below target") is exactly what Brandon needs to coach the team.

Where it loses Brandon: the appendices are heavy. Appendix A (formula derivations) is useful for Richard but Brandon doesn't need to solve for NB registrations algebraically. Appendix B (four optimization scenarios) repeats concepts from the main body with MX-specific examples that Brandon already knows. Appendix D (levers ranked) restates the Brand-is-the-engine thesis a third time. Brandon would skim the last 40% of this doc. The main body is a 9; the appendices dilute it to an 8.

The TODO comment about the -10% haircut is a good self-flag but shouldn't ship in a published doc.

**Verdict: SHIPS** — with a note that the appendices could be tightened. The core framework is strong enough that Brandon could hand this to a finance partner and say "read the first five sections."

---

## 2. OCI Execution Guide (v2)

**Reader simulation: Stacey/Andrew/Aditya, implementing OCI in a new market**

| Dimension | Score |
|-----------|-------|
| First Paragraph Test | 9/10 |
| Shareability | 9/10 |
| Actionability | 10/10 |
| Signal-to-Noise | 8/10 |
| Voice | 8/10 |
| **Composite** | **8.8/10** |

This is the strongest article in the batch. A teammate launching OCI in CA next week could follow this doc end-to-end without asking Richard a single question. The "What Not to Do" section up front is smart — it prevents the three most common mistakes before the reader even starts. The phase gates (115% → 110% → weekly review) are concrete and unambiguous. The troubleshooting appendix covers the actual failure modes the team has encountered, not hypothetical ones.

The first paragraph passes cleanly: what it is (step-by-step execution reference), what to do with it (launch, monitor, scale), and where to go for other things (Playbook for strategy, Business Case for leadership). A teammate can start executing from this doc without reading anything else.

Shareability is high — Andrew could send this to a market stakeholder to explain the OCI rollout plan without any "but ignore the part about…" caveats. The monitoring cadence section is particularly well-structured: daily for two weeks, weekly after that, formal eval at four weeks. No ambiguity.

Minor ding on signal-to-noise: the "What OCI Does" section spends a sentence on the philosophical ("Manual bidding doesn't scale across ten markets, and OCI has validated that premise") that a teammate implementing OCI already knows. They want the how, not the why. But this is a minor quibble — the section is three sentences too long, not three paragraphs.

**Verdict: SHIPS** — cleanly. Best execution doc in the wiki.

---

## 3. AU Market Wiki (v2)

**Reader simulation: Richard prepping for an AU sync with Lena**

| Dimension | Score |
|-----------|-------|
| First Paragraph Test | 8/10 |
| Shareability | 7/10 |
| Actionability | 8/10 |
| Signal-to-Noise | 8/10 |
| Voice | 9/10 |
| **Composite** | **8.0/10** |

Richard opens this 30 minutes before a sync with Lena. Does he walk in prepared? Mostly yes. The strategic situation section gives him the narrative: CPC declining but CPA flat, CVR is the binding constraint, OCI is the unlock. The stakeholder profiles in Appendix A are genuinely useful — "expects numbers rather than narratives" and "signs off 'Cheers, Lena'" tells Richard exactly how to calibrate his communication.

The voice is the best in the batch. "The equivalent of driving without a speedometer" for pre-OCI bidding. "Lena drives fast, unilateral decisions… Brandon provides air cover." This reads like a person who knows the situation wrote it for another person who needs to act in it. That's exactly right.

Shareability takes a hit because this doc contains internal stakeholder dynamics that Richard would never forward to Lena or Alexis. The CPC challenge section explicitly frames Lena's comparison as "apples-to-oranges" — accurate, but not something you'd share with the person being characterized. This is fine for an internal reference doc, but it means the audience is Richard-only, not Richard-plus-stakeholders.

The open questions section is strong — five questions, each with an owner and a timeline. Richard walks out of this doc knowing what he needs to do, not just what the situation is.

One concern: the W13 data (207 regs, CPA $118) will be stale within two weeks. This doc needs an update trigger that's more aggressive than the 30-day default for fast-moving market data.

**Verdict: SHIPS** — at the floor. The 7 on shareability is the weak link, but for a doc whose primary reader is Richard prepping for syncs, that's acceptable. The voice and actionability carry it.

---

## 4. Enhanced Match / LiveRamp (v2)

**Reader simulation: Brandon tracking the investigation she initiated**

| Dimension | Score |
|-----------|-------|
| First Paragraph Test | 9/10 |
| Shareability | 8/10 |
| Actionability | 8/10 |
| Signal-to-Noise | 8/10 |
| Voice | 8/10 |
| **Composite** | **8.2/10** |

Brandon opened this investigation. She wants to know: where are we, what's blocked, and what do I need to do? The first paragraph delivers all three — "Brandon's investigation request," "open risks that need resolution before scoping," and "who owns each action." She doesn't have to read past paragraph one to know whether this doc is current and relevant.

The "Brandon's Four Questions" section is smart structuring — it mirrors exactly how Brandon framed the ask, so she can scan it and immediately see which questions have answers (none yet) and what's blocking them (Richard needs to reach Abdul). The decision guide in Appendix A is the most useful table in the batch: five if-then scenarios that map directly to Brandon's decision space. She can look at this table and know exactly what happens next depending on what Abdul says.

The 78% audience drop (5.6M → 1.2M) is surfaced with appropriate urgency — "investigate before scoping Enhanced Match" is the right call, and the doc makes the logic clear: Enhanced Match on a degraded audience is low-value. Brandon reads that and knows the investigation has the right priorities.

Voice is solid throughout. "Brandon is driving this personally, which means it's moving fast" — that's how the team actually talks about Brandon's involvement. The connections section (F90, OCI, email overlay) gives Brandon the strategic context without over-explaining things she already knows.

Minor ding: the ABMA SIM escalation protocol paragraph (Sev 2.5, Vijay Kumar as watcher) feels like it was included because it's temporally relevant, not because it's structurally part of the Enhanced Match story. It's useful information but it belongs in a team operations doc, not here.

**Verdict: SHIPS** — solid investigation tracker that serves its reader well.

---

## Summary

| Article | Composite | Ships? |
|---------|-----------|--------|
| ie%CCP Framework | 8.2 | Yes |
| OCI Execution Guide | 8.8 | Yes — strongest in batch |
| AU Market Wiki | 8.0 | Yes — at the floor |
| Enhanced Match / LiveRamp | 8.2 | Yes |

All four clear the bar. The OCI Execution Guide is the standout — it's the kind of doc where a teammate can execute without asking questions, which is the highest compliment for an execution guide. The AU Market Wiki ships but lives on the edge; the weekly performance data will decay fast and the shareability constraint is real. The ie%CCP Framework and Enhanced Match doc are both solid 8s that serve their primary readers well.
