---
inclusion: manual
---
# Richard Williams — Long-Form Document Style Guide

Covers: experiment docs, testing plans, investigation docs, instructional docs, post-mortems, OP1/strategic narratives.

## Universal Rules
- Max 3 bullet points per list before a paragraph break or new header. Lists longer than 3 items lose scannability.
- Every list item must start with a verb or a number. Noun-only items are padding.
- Headers must be questions or imperatives, never bare nouns. 'How to optimize AU NB CPA' not 'AU NB CPA Optimization'. 'When to escalate to Brandon' not 'Escalation Framework'. The header tells the reader what they'll get from the section.

## Experiment Documents
- Structure: Question → Setup → Results → Recommendation. Example: 'Does NB bid strategy reduce CPA?' → 6-week test, AU NB campaigns → CPA $168→$117 (-29%) → Adopt as baseline.
- Tables always include: Impressions, Clicks, Cost, Registrations, CTR, CPC, CVR, CPA
- Comparisons include absolute numbers AND percentages
- Interpretation: States finding, then explains why it matters: "CPA from platform was $700, which is still high, but half of what the overall test did."
- Confidence signals: "What we can definitively say is..." / "it would be difficult to conclude that..."
- Honest about failures: "Bulk page did not perform better than the callback page." No spin.
- Uses first person sparingly: "I found that," "I could have put more attention towards"
- Bayesian language when relevant: "83.4% PPR" / "5.8% chance that experiment would perform better"

## Testing Plans / Strategy Documents
- Structure: Goal → Phased plan (Phase 1, Phase 2...) → Supporting case studies → Other initiatives
- Phases have target completion dates and status updates
- Expectations quantified: "I would expect Adobe to allow for a 5%-15% improvement in CPA"
- Case studies from other markets as evidence: "MX market efficiency (case study)"
- Honest about uncertainty: "although regs too low to make strong conclusions"

## Investigation Documents
- Structure: Reference links → Data tables → Observations → Hypotheses → Evidence → Actions
- Starts with the anomaly: "Brand Paid Search is consistently saturated with ~97% ad visibility"
- Hypotheses clearly labeled and testable: "Clicks are not being correctly attributed." / "Registration process friction."
- Evidence layered: high-level → market-level → query-level
- Cross-references multiple data sources (Adobe, Google Ads, Hubble, Quicksight)
- Distinguishes "proven" from "not proven or validated" — never overstates
- Questions embedded for follow-up: "How do we calculate WBR regs?"

## Instructional / How-To Documents
- Structure: Objective → Numbered Tactics (sequential) → Scenarios → Resources
- Imperative mood: "Set a realistic initial baseline" / "Observe actual ROAS data"
- Scenario-based examples with specific numbers
- Warnings about what NOT to do: "Large, sudden changes can push the campaign back into learning period"
- Practical framing: "Managing ROAS bid strategy is not passive."

## Post-Mortem / Retrospective Documents
- Structure: Lessons Learned → Challenges → Accomplishments → Overview → Recommendations
- Lead with lessons — the reader gets the learning immediately
- Most self-critical format. First person: "I could have put more attention towards moving forward on the planning."
- Lessons are actionable, not abstract: "Start simple, then go granular" with specific example
- Appendices for supporting data, keeping the main narrative clean

## Strategic Narrative (OP1 / Leadership Docs)
- Each section: problem → test → validated result → 2026 investment
- Most polished voice. Longer sentences. More connective tissue.
- Key phrases: "validated results," "measurement framework," "cross-functional collaboration," "connective tissue between platform capabilities and business objectives"
- Data embedded in narrative, not just tabled: "$16.7MM in OPS" / "+24% registration lift"
- Everything connects — nothing presented as isolated. The word "compound" appears repeatedly.
- Credits cross-functional partners by name or team

## Knowledge-Sharing Documents
- Organized by scenario/use case rather than by tool
- Casual, peer-to-peer voice. Bullet points heavily.
- Practical examples: "Load files into Cedric and ask questions about the content"
- Honest about limitations: "AI isn't great at math/data analysis yet"
- Future ideas section at the end
