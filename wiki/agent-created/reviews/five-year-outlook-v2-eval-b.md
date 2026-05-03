---
title: "Eval B Review: Paid Search Five-Year Outlook v2 (Kate Persona)"
status: DRAFT
audience: amazon-internal
owner: "Richard Williams"
created: 2026-05-01
updated: 2026-05-01
---

# Review: Paid Search Five-Year Outlook v2 (Eval B — Kate Rundell Reader Simulation)

Reviewed: 2026-05-01 23:12
Slug: five-year-outlook-v2
Draft version: 2026-04-05 (from frontmatter `updated` date)
Consecutive sub-8: 1

---

## Constraint check

No `.state.json` blackboard file exists for this article. The article predates the blackboard protocol (created 2026-04-05, protocol launched 2026-04-18). Evaluating against default constraints by audience and doc-type.

| Default constraint | Verdict | Rationale |
|--------------------|---------|-----------|
| **Audience: Kate-level exec-readable** | PASS | Prose is direct and data-grounded. Numbers are embedded in narrative sentences, not dumped in standalone tables. Confidence labels are explicit in section headers. The Purpose paragraph opens with the ask (endorsement of four bets within existing budget). No jargon without context. Kate can read the main body (~1,100 words) in under five minutes and reach a decision. |
| **Doc-type: strategy with clear asks + fallbacks** | PASS | The executive summary decision table is the structural backbone — four bets, each with success condition, failure fallback, and read date. The Downside section addresses the speculative horizon. This is a strategy doc that frames a decision and shows what happens if the answer is no. |
| **Citation discipline** | PASS | Every external claim carries a parenthetical source and date. Internal claims reference body system docs by name. Appendix A tiers sources into HIGH/MEDIUM/LOW confidence. No uncited claims found. |

---

## Kate Rundell reading simulation

### What Kate sees in the first 90 seconds

She reads the Purpose paragraph and the executive summary decision table. This is the right structure — the table IS the argument. She knows the ask (endorse four bets), the cost (existing budget), and the risk profile (each bet has a named fallback) before she reaches the body. Good.

### What works

The decision table is the strongest element in the document. Kate can point at it in a review meeting and say "I'm endorsing these four lines." Each row answers three questions: what happens if it works, what happens if it doesn't, and when we'll know. This is exactly the framing a skip-level needs to put her name on something.

The confidence labeling is honest. 2026 is HIGH, 2027 is MEDIUM, 2028+ is LOW. Kate is not being asked to endorse speculation — she's endorsing a 2026 test plan with defined gates. The speculative horizon is clearly fenced in an appendix. This respects her time and her risk tolerance.

The "within existing budget allocation" framing removes the hardest objection. She doesn't need to fight for incremental funding or defend a new line item. The ask is permission, not money.

The downside section is credible. No single bet is existential. The OCI foundation persists regardless. This is the kind of risk framing that lets a director say yes without feeling exposed.

### Where Kate pushes back

**1. The 2026 section is a wall of prose.** Seven distinct topics — OCI deployment status, ad copy test results, Baloo, F90, AI Max, external signals (AI Overviews, Shopping Ads in AI Mode), and agentic tooling — run in a single unbroken section with no subheadings. Kate scans. She reads the first sentence of each paragraph and dives deeper only if the topic is relevant to her decision. Without subheadings, she has to read linearly to find the three paragraphs she cares about (the new bets) buried among operational status updates she'd delegate to her team. This is the single biggest structural problem in the document.

**2. The agentic tooling bet is underweight for the table it sits in.** AI Max has a 14% conversion uplift target. Baloo unlocks a new ad format. F90 targets a 366 bps improvement in 3+ purchase rate. Agentic tooling's success criterion is "one tool adopted by a teammate." Kate would read that row and ask: "Why is this in the same investment table as the other three? What's the business value of one teammate adopting one tool?" The bet lacks a quantified business outcome. It reads like a team capability investment — valid, but it doesn't belong in the same decision frame as revenue-driving bets unless the doc explains why. Right now it looks like a pet project riding the coattails of three real bets.

**3. The Gartner editorial in the 2027 section.** "The teams that survive build for sustainability, not hype" is a platitude. Kate has heard this sentence in fifty strategy decks. It doesn't connect to a specific AB decision or action. She'd either skip it or, worse, it would erode her trust in the analytical rigor of the surrounding paragraphs. The Gartner data points (75% adoption, 40% cancellation) are useful signals — the editorial gloss is not.

**4. Appendix B is file paths.** Kate doesn't navigate `shared/artifacts/testing/2026-04-03-testing-approach-outline.md`. This appendix signals the document was written for an internal tooling audience, not for her. It's a small thing, but it breaks the illusion that this doc was crafted for leadership. Cut it or convert it to document titles with one-line descriptions.

### Would Kate endorse?

**Conditionally yes, with revisions.** The core argument is sound. The decision table is clean. The risk framing is credible. The budget ask is zero. Kate would endorse the four bets — but she'd hand the document back first and say: "Break up the 2026 section so I can scan it. Either give me a business case for the agentic tooling bet or move it to a separate 'team capability' section outside the investment table. Cut the file-path appendix. Then I'll sign."

She would not decline the bets themselves. She would decline to circulate this document in its current form to her peers or her VP because the 2026 section's density and the agentic bet's weak framing would invite questions she shouldn't have to answer on Richard's behalf.

---

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Usefulness | 8/10 | The decision table enables endorsement. Kate can act on this. The agentic bet's weak business case is the only drag — she'd endorse three of four without hesitation and ask a clarifying question on the fourth. |
| Clarity | 7/10 | The 2026 section's seven-topic wall of prose is the binding problem. A scanning reader loses the new bets among operational status updates. Subheadings would fix this in five minutes. The rest of the document's structure (confidence-labeled year sections, fenced appendices) is strong. |
| Accuracy | 8/10 | Claims are sourced and confidence-tiered. Internal metrics are attributed to named docs with dates. The stale `updated: 2026-04-05` frontmatter is a minor trust issue — if this is v2, the date should reflect the revision. No factual errors found. |
| Dual-audience | 8/10 | AGENT_CONTEXT is well-structured with machine_summary, key_entities, and refresh triggers. Prose serves Kate. Appendix B (file paths) is the one crack — it serves neither audience well. Agents already have `depends_on`; humans don't use file paths. |
| Economy | 7/10 | Appendix B duplicates AGENT_CONTEXT `depends_on` and adds no value for either audience — cut it. The 2027 Gartner editorial ("teams that survive build for sustainability, not hype") is filler. The 2029-2030 appendix section is thin on decision-relevant content — acceptable as scenario painting but borderline. Main body prose is tight. The decision table earns its place. No bullet list abuse, no table abuse, no formatting-as-content violations. |
| **Average** | **7.6/10** | |

---

## Verdict

**REVISE**

Average 7.6/10. Clarity (7) and Economy (7) are below the 8/10 bar. The fixes are structural and achievable in one revision pass.

---

## Required changes

**1. Add subheadings to the 2026 section.**

The current 2026 section runs seven topics in continuous prose. Break it into three subheadings:

> Insert after "Investments are committed, tests are designed, and the team is executing.":
>
> `### Foundation: OCI Deployment and Campaign Consolidation`
>
> Insert before "Project Baloo (early access March 30...":
>
> `### New Bets: Baloo, AI Max, and F90`
>
> Insert before "Two external signals to monitor in 2026":
>
> `### External Signals and Agentic Tooling`

This adds three lines and zero words of prose. Kate can now scan to the section she cares about.

**2. Strengthen the agentic tooling row in the decision table or move it out.**

Current "If it works" cell: "One tool adopted by a teammate, proving scalability"

This is a capability milestone, not a business outcome. Either:

(a) Add a business framing: "One tool adopted by a teammate, reducing WBR prep time from 4 hours to 1 hour (proving scalability of agentic infrastructure)" — or whatever the actual expected efficiency gain is.

(b) Remove the agentic tooling row from the four-bet decision table and add a separate paragraph below the table: "A fourth initiative — agentic team tooling — runs in parallel as a capability investment. Its 2026 gate is one tool adopted by a teammate. Unlike the three bets above, this is infrastructure, not a revenue play. It requires no incremental budget and has no downside if adoption is slower than planned."

Option (b) is the stronger move. It protects the decision table's credibility by keeping it focused on bets with quantified business outcomes.

**3. Cut Appendix B.**

Delete the "Appendix B: Internal Reference Documents" section entirely. The six file paths duplicate information already in AGENT_CONTEXT `depends_on` and in the body's inline citations. Neither Kate nor an agent gains value from this list.

**4. Replace the Gartner editorial with an AB-specific implication.**

Current: "The teams that survive build for sustainability, not hype."

Replace with: "The PS team's text-file-based agentic infrastructure avoids the enterprise platform costs that drive Gartner's projected cancellation wave — no vendor contracts, no per-seat licensing, no sunk-cost pressure to continue if results don't materialize."

This connects the external signal to the specific AB advantage rather than offering a generic truism.

---

## Suggestions (non-blocking)

1. **Update frontmatter `updated` date.** Currently `2026-04-05`. If this is v2, the date should reflect the actual revision date. A stale date on a strategy doc signals the content may also be stale — a small trust erosion for a careful reader.

2. **Consider tightening Appendix C (2029-2030).** The section is honest about its speculative nature, but the content is thin — "the distinction between search, display, and agent-mediated discovery blurs" is directionally true but not specific enough to inform any decision. Kate won't read it. Her team might, but only if the 2028 section gives them a reason to keep going. Not blocking, but the doc would be tighter without it.

3. **The F90 row's "Monthly" read date is an outlier.** The other three bets have quarterly gates. Kate might ask why F90 doesn't have a go/no-go quarter. Consider adding a parenthetical: "Monthly (Q3 2026 decision on scaling criteria)" or similar to match the cadence of the other rows.
