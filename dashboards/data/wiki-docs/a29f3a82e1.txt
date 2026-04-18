# Blind Test 2 — Evaluator B (Subjective Reader Evaluation)

*Evaluator persona: Simulating Brandon Munday (L7, Richard's manager) and Kate Rundell (L8 Director). Brandon reads 20+ docs a week, values leverage over activity, wants lightweight mechanisms. Kate wants one page, strategic framing, data as evidence not the message. Both can spot mediocre writing in 30 seconds.*

---

## Article 1: OCI Rollout Playbook

**File:** `shared/artifacts/testing/2026-03-25-oci-rollout-playbook.md`

### 1. FIRST PARAGRAPH TEST — 8/10

The opening line works: *"This playbook codifies the OCI rollout methodology that produced +35K registrations and $16.7MM+ OPS across US, UK, and DE."* That's a result, not background. Brandon reads past that. The second sentence — *"A teammate should be able to replicate the rollout in a new market by following this doc. No Richard required."* — is exactly the kind of leverage framing Brandon wants to see. It says: I built something that scales without me. That's an L6 signal, not an L5 signal.

Where it loses a point: the Context section immediately after drops into background mode (*"OCI enables Google Ads to optimize bidding based on actual registration value data..."*). Brandon already knows what OCI is. She'd skim that paragraph.

### 2. SHAREABILITY — 8/10

Brandon could forward this to Kate or a peer with minimal editing. The structure is clean — someone unfamiliar with OCI could follow the phases. The Decision Guide at the bottom is particularly forwardable: *"Stakeholder asks 'does OCI work?' → Show DE W44-W45 test vs control data. Then US $16.7MM OPS figure."* That's the kind of thing Brandon would screenshot and send to Kate.

The one issue: it's long. Kate wouldn't read the whole thing. But the first page and the results table would be enough for her, and that's fine for a playbook.

### 3. ACTIONABILITY — 9/10

This is the strongest dimension. Each phase has explicit exit criteria. The Decision Guide tells you what to do in five specific situations. The Known Issues section has a workaround. A teammate could literally follow this doc and launch OCI in a new market. That's rare — most Amazon docs tell you what happened, not what to do next.

The "What OCI Does (and Doesn't Do)" section is particularly good: *"Doesn't: Fix Brand CPA. Brand traffic converts regardless of bidding algorithm."* That prevents the most common misunderstanding before it happens.

### 4. SIGNAL-TO-NOISE — 7/10

The DE test-vs-control table is pure signal — that's the proof point. The market-specific considerations table is useful. But there's padding: the MCC Structure table appears in both this doc and the Execution Guide. The Sources section at the bottom is agent metadata, not reader value. The Related section is fine but could be tighter.

A busy L8 with 15 minutes would get the value in the first 3 minutes (opening + results table + decision guide). The middle sections (Phase 2-4 details) are reference material, not first-read material. That's acceptable for a playbook — it's designed to be consulted, not read cover-to-cover.

### 5. VOICE — 7/10

Mostly sounds like Richard. The "So what" annotations after data tables are a good Richard touch — he thinks in implications, not just numbers. *"This is the data to show anyone who asks 'does OCI actually work?'"* feels like something Richard would say in a 1:1.

But some sections read like a reference manual rather than a person writing: *"Exit criteria: Data pipeline confirmed working. Conversion counts match within tolerance. No duplicate parameter errors."* That's functional but voiceless. The best parts of this doc have personality; the middle sections lose it.

**Composite: 7.8/10**

---

## Article 2: OCI Execution Guide

**File:** `shared/artifacts/program-details/2026-04-04-oci-execution-guide.md`

### 1. FIRST PARAGRAPH TEST — 7/10

Opens with a cross-reference: *"For the business case, validated results, and strategic rationale, see OCI Rollout Playbook. This doc is the how-to."* That's efficient — it tells you what this doc IS and ISN'T in two sentences. Then the 30-second version delivers the headline numbers.

But Brandon might not read past the cross-reference. If she's already read the Playbook, she might think "I've seen this." The "What NOT to Do" section is the real hook — *"Do not judge OCI by week 1. The algorithm needs 2-4 weeks to learn. CPA will spike. This is normal."* — but it's below the fold. If that section were the opening, this doc would hook harder.

### 2. SHAREABILITY — 6/10

This is where it struggles. Brandon wouldn't forward this to Kate — it's too operational. She'd forward it to Stacey or Andrew, which is the right audience. But even for peers, the doc duplicates content from the Playbook (MCC table, market status table, results numbers). A peer who's read the Playbook would feel like they're re-reading material.

The "What NOT to Do" section is independently forwardable. The Troubleshooting table is independently forwardable. The step-by-step E2E launch is independently forwardable. But the doc as a whole has too much overlap with Article 1 to stand alone cleanly.

### 3. ACTIONABILITY — 9/10

This is the doc's strength and its reason for existing. The prerequisites checklist with actual checkboxes. The step-by-step with specific Google Ads navigation paths (*"Google Ads -> Campaign -> Settings -> Bidding"*). The monitoring cadence (*"Week 1: Daily. Week 2: Daily. Week 3-4: Weekly."*). The gate criteria (*"CPA within 115% of baseline: proceed. CPA between 115-120%: extend. CPA >120% for 7+ days: pause."*).

Someone who has never touched OCI could follow this doc and not break anything. That's the bar for execution documentation, and it clears it.

### 4. SIGNAL-TO-NOISE — 5/10

This is the weakest dimension. Too much duplication with the Playbook. The MCC table appears in both docs. The market status table appears in both docs (with slightly different data — the Execution Guide is more current, which creates a maintenance problem). The "What OCI Is (30-Second Version)" repeats the Playbook's opening.

If you stripped the duplicated content, this doc would be 40% shorter and 100% more useful. The unique value is: What NOT to Do, Prerequisites, Step-by-Step, Troubleshooting, Quick Reference. Everything else is in the Playbook.

Kate would never read this doc. Brandon would skim it. The real audience is the person actually clicking buttons in Google Ads, and for that person, the noise is tolerable but the duplication is confusing.

### 5. VOICE — 6/10

The "What NOT to Do" section has voice: *"Do not panic if CPA spikes in week 1. It normalizes by week 3-4."* That's Richard talking to a teammate. The Troubleshooting table has voice in the "Fix" column: *"Wait. Evaluate at week 3-4. Do not intervene."*

But the step-by-step sections read like a Google Ads help article. *"Switch from Manual CPC to 'Maximize Conversions' or 'Target CPA'."* That's necessary but generic. The per-market notes try to add color but feel like they were assembled from a data source rather than written by someone who manages these markets.

**Composite: 6.6/10**

---

## Article 3: AU Paid Search — Market Wiki

**File:** `shared/artifacts/program-details/2026-04-04-au-market-wiki.md`

### 1. FIRST PARAGRAPH TEST — 6/10

Opens with: *"Australia is the newest market in the AB Paid Search portfolio, launched in June 2025 (W24). Richard owns AU hands-on."* That's background, not a result. Brandon already knows Richard owns AU. She already knows when it launched.

The hook is buried in the second paragraph: *"The market sits at an inflection point... AU does not yet have OCI support (target: May 2026), which means it is running without the conversion signal infrastructure that drives 16-20% registration lifts in other markets."* THAT's the sentence that should open the doc. It tells you the strategic situation in one line.

If I'm Brandon, I'm reading this because I need to prep for a conversation about AU. The first paragraph doesn't help me prep. The second paragraph does.

### 2. SHAREABILITY — 5/10

Brandon would not forward this to Kate. It's a reference doc — useful for Richard and maybe Alexis, but not for upward communication. The stakeholder table with communication style notes (*"Challenged $6 CPC as 'outrageous'"*) is internal intelligence that shouldn't go to Kate. The Open Questions section is good but reads like Richard's personal to-do list, not a shareable status.

If Brandon needed to brief Kate on AU, she'd pull 3-4 sentences from this doc and write her own summary. That's a sign the doc serves Richard's needs but not Brandon's forwarding needs.

### 3. ACTIONABILITY — 4/10

This is a reference doc, not an action doc. The Open Questions section lists questions but doesn't propose answers or next steps. *"How much of the W13 CVR drop is attributable to Polaris migration vs. seasonal softness vs. promo transition?"* — OK, but what's the plan to find out? Who's doing the analysis? By when?

The Active Initiatives section describes what's happening but doesn't say what Richard is doing about each one this week. *"OCI Integration (Target: May 2026) — MCC has not been created."* So... is Richard creating it? Is someone else? What's the next action?

Brandon's feedback would be: "This tells me the state of AU. It doesn't tell me what you're doing about it."

### 4. SIGNAL-TO-NOISE — 6/10

The CPC Challenge section is good signal — it frames the Lena dynamic clearly and provides the counter-argument. The performance table is clean. The campaign structure table is useful.

But the Competitors section — *"No competitors in AU currently."* — is a one-liner that doesn't need its own section. The Recurring Meetings section is filler. The Sources section is agent metadata. The Key Decisions table is useful but could be tighter.

For a market wiki, the signal-to-noise is acceptable. It's a reference doc, and reference docs are allowed to be comprehensive. But it could be 30% shorter without losing value.

### 5. VOICE — 7/10

This sounds more like Richard than the Execution Guide. The CPC Challenge section has personality: *"This is an apples-to-oranges comparison"* and *"B2B search is structurally more expensive than consumer."* The stakeholder notes feel like Richard's actual observations, not generated summaries.

The Overview paragraph is the weakest voice-wise — it reads like a briefing document rather than Richard's perspective. Compare *"The market sits at an inflection point"* (generic) with *"NB CPC has declined 29% over 7 weeks through bid strategy optimization"* (specific, confident). The specific sentences sound like Richard. The framing sentences don't.

**Composite: 5.6/10**

---

## Article 4: Enhanced Match / LiveRamp

**File:** `shared/artifacts/testing/2026-04-04-enhanced-match-liveramp.md`

### 1. FIRST PARAGRAPH TEST — 9/10

*"Brandon initiated an Enhanced Match investigation on 3/30, asking Richard to partner with Abdul Bishar to scope the opportunity. Robert Skenes confirmed on 4/3 that Richard's LiveRamp segment is approved and wants parallel implementation."*

This is exactly how Brandon wants to receive information. It tells her: here's what you asked for, here's what happened since, here's where it stands. No background preamble. No "Enhanced Match is a technology that..." The context comes after the status, not before it.

The second paragraph provides the technical context, but only after the reader knows why they're reading. That's the right order.

### 2. SHAREABILITY — 7/10

Brandon could forward the "Brandon's Four Questions" section to Abdul or Legal without editing. The questions are crisp and numbered. The Current State section provides enough context for someone outside the team to understand the situation.

The concern: the doc includes internal intelligence (*"This is moving fast — Brandon is driving it personally"*) that Brandon might not want forwarded verbatim. And the audience drop investigation (*"5.6M to 1.2M"*) is an open question that Brandon might want resolved before sharing upward.

For peer sharing, this works well. For Kate, Brandon would extract the opportunity framing and the four questions, not forward the whole doc.

### 3. ACTIONABILITY — 8/10

The Next Steps section is explicit: five numbered actions with owners. *"Richard: Reach out to Abdul Bishar with Brandon's 4 questions (URGENT — Brandon is waiting)."* That's clear. The ABMA SIM escalation protocol is actionable — it tells you exactly what severity to use and who to add as a watcher.

The one gap: there's no timeline on the next steps. "URGENT" is relative. When does Brandon need the answers? By end of week? Before a specific meeting? The urgency is stated but not quantified.

### 4. SIGNAL-TO-NOISE — 8/10

This is a lean doc. Almost every section earns its place. The "Connection to Existing Initiatives" section is particularly good — it shows how Enhanced Match connects to F90, OCI, and email overlay without over-explaining any of them. That's the kind of strategic connective tissue Brandon values.

The ABMA SIM Escalation Protocol section is the one piece that feels bolted on — it's relevant but could be a one-liner rather than a full section. And the Sources section is agent metadata that adds no reader value.

### 5. VOICE — 8/10

This sounds like Richard briefing Brandon. *"This is moving fast — Brandon is driving it personally."* *"A concerning signal from Andrew Wirtz..."* *"The EU team wants to launch LiveRamp, but the path is unclear."* These are observations from someone who's tracking the situation, not a generated summary.

The technical explanation of Enhanced Match is clear without being condescending: *"Enhanced Match expands the data signals sent, potentially increasing the match rate beyond the current 30%."* That's the right level of detail for Brandon — enough to understand, not enough to bore.

The weakest voice moment: *"Every percentage point of match rate improvement translates to more precise targeting and less wasted spend."* That's a generic marketing sentence. Richard would say something more specific.

**Composite: 8.0/10**

---

## Article 5: ie%CCP Planning & Optimization Framework

**File:** `shared/artifacts/strategy/2026-03-30-ieccp-planning-framework.md`

### 1. FIRST PARAGRAPH TEST — 5/10

Opens with: *"ie%CCP answers one question: how much are we paying to acquire a customer, relative to what that customer is worth?"* That's a definition, not a result. If Brandon is reading this, she already knows what ie%CCP is. If Kate is reading this, she needs to know why she should care — and "here's a definition" doesn't answer that.

The hook should be something like: "MX Brand is running 2.7x above plan, which creates $X of surplus that could fund Y incremental NB registrations — but only if we move the ie%CCP target from 100% to 75%." That's a decision. The current opening is a tutorial.

The "Why It's Confusing" section is honest and useful — *"ie%CCP trips people up because the relationships run in opposite directions"* — but it reinforces that this is a teaching document, not a decision document. Brandon doesn't need to be taught. She needs to be equipped.

### 2. SHAREABILITY — 4/10

Brandon would not forward this to Kate. It's too long, too tutorial-oriented, and the MX case study is buried at the bottom. Kate would need the MX projection table and the "vs OP2" comparison — that's one page. The other 80% of this doc is framework explanation that Kate doesn't need.

Brandon might forward the Quick Reference section at the very end, which is actually excellent: *"Brand is the engine. Grow it to create surplus. NB is the passenger. Optimize it, then scale it. CCP is the speed limit. Set by finance, not by us."* That's the whole doc in six lines. If the doc opened with that and then provided the MX case study as evidence, it would be far more shareable.

For peers (Stacey, Andrew), this is useful as a reference. But peers would also struggle with the length. The four scenarios section is comprehensive but reads like a textbook chapter.

### 3. ACTIONABILITY — 6/10

The "Applying This to Callouts and Recommendations" section is actionable — it gives you four specific questions and how to answer them. The four scenarios each have ranked levers. The MX case study shows how to apply the framework to a real market.

But the doc doesn't tell you what to DO right now. It tells you how to THINK about ie%CCP. That's valuable — but it's a framework, not a recommendation. Brandon would read this and say: "Great, so what's your recommendation for MX? 75% or 100%? And what do you need from me to make it happen?"

The MX case study gets close to a recommendation but stops short: *"Both scenarios exceed OP2 because Brand is massively outperforming... The question is whether finance funds the NB spend."* That's analysis, not a recommendation. Richard should say: "I recommend Scenario 2 (75%) because [reason], and I need Brandon to [action]."

### 4. SIGNAL-TO-NOISE — 4/10

This is the doc's biggest problem. It's a 2,500+ word framework document where the actual decision-relevant content is the MX case study (maybe 400 words) and the Quick Reference (100 words). The rest is educational.

The formula derivations, the four scenarios, the marginal CPA curve explanation, the lever rankings — all of this is useful knowledge, but it's reference material, not first-read material. A busy L8 with 15 minutes would not get to the MX case study. She'd read the first two sections, decide this is a tutorial, and close it.

The subsidy model explanation is genuinely insightful: *"Brand CPA $21 / CCP $90 = 23% ie%CCP (extremely efficient). NB CPA $134 / CCP $30 = 447% ie%CCP (extremely inefficient)."* That's a powerful framing. But it's buried in a section called "Why It's Confusing" — which is not where Brandon goes looking for insight.

### 5. VOICE — 7/10

The best voice moments are in the plain-English translations: *"We pay 75¢ for every $1 of customer value"* and *"Brand is the engine; NB is the passenger."* Those are Richard's analogies — clear, concrete, memorable.

The scenario descriptions have good voice too: *"Finance gave us less money AND wants us to be more efficient. This is the hardest scenario."* That's how Richard talks in a 1:1 — direct, no hedging.

But the formula sections and the mathematical derivations read like a textbook. *"At a given ie%CCP target T, you can solve for the maximum NB regs the account can support..."* — that's not Richard's voice, that's a finance analyst's voice. Richard would say: "Here's the math if you want it" and put it in an appendix.

**Composite: 5.2/10**

---

## Summary Rankings

| Rank | Article | Composite | Brandon Would... | Kate Would... |
|------|---------|-----------|-----------------|---------------|
| 1 | Enhanced Match / LiveRamp | 8.0 | Read it, act on it, forward the questions section | Not see it (too operational) but would appreciate the strategic connections if briefed |
| 2 | OCI Rollout Playbook | 7.8 | Read it, reference it, forward the Decision Guide | Read the first page and results table, skip the rest |
| 3 | OCI Execution Guide | 6.6 | Skim it, forward to Stacey/Andrew | Never see it, nor should she |
| 4 | AU Market Wiki | 5.6 | Skim for AU prep, wish the Open Questions had next steps | Never see it |
| 5 | ie%CCP Framework | 5.2 | Read the Quick Reference, wish the MX recommendation was on page 1 | Close it after the first section — too tutorial, not enough decision |

---

## Cross-Cutting Observations

**The best writing happens when Richard is briefing Brandon on something Brandon asked for.** The Enhanced Match doc works because it's structured as "here's what you asked, here's what I found, here's what's next." The ie%CCP doc doesn't work as well because it's structured as "let me teach you a concept." Brandon doesn't want to be taught. She wants to be equipped.

**The "So what" instinct is Richard's superpower — when he uses it.** The OCI Playbook's "So what" annotations after data tables are excellent. The ie%CCP doc's subsidy model insight is excellent. But both docs have long stretches where the "so what" disappears and the writing becomes descriptive rather than interpretive.

**Duplication is the biggest structural problem.** The OCI Playbook and OCI Execution Guide share ~30% of their content (MCC tables, market status, results numbers). This creates maintenance burden and reader confusion. The Execution Guide should ruthlessly cross-reference the Playbook instead of duplicating.

**The docs that open with results or decisions score higher than docs that open with definitions or background.** Enhanced Match opens with what happened. The Playbook opens with what it produced. The ie%CCP doc opens with a definition. The AU Wiki opens with background. The pattern is clear: lead with the answer, not the question.

**Kate would read exactly one of these docs (the Playbook, first page only).** That's not a failure — most of these are team-level docs. But if Richard wants Kate-level visibility, he needs a one-page derivative of the ie%CCP framework that says: "MX Brand is outperforming 2.7x. Here's what that means for NB investment. Here's my recommendation. Here's what I need." That doc doesn't exist yet, and it's the one Kate would actually read.
