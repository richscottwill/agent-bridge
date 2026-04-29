---
inclusion: manual
---


# Richard Williams — Long-Form Document Style Guide

Covers: experiment docs, testing plans, investigation docs, instructional docs, post-mortems, OP1/strategic narratives.



## Universal Rules
- Max 3 bullet points per list before a paragraph break or new header. Lists longer than 3 items lose scannability.
- Every list item must start with a verb or a number. Noun-only items are padding.
- Headers must be questions or imperatives, never bare nouns. 'How to optimize AU NB CPA' not 'AU NB CPA Optimization'. 'When to escalate to Brandon' not 'Escalation Framework'. The header tells the reader what they'll get from the section.



## Strategic Narrative (OP1 / Leadership Docs)
- Each section follows: problem → test → validated result → investment ask. Never present a result without the problem it solved. If the problem isn't clear, the result has no anchor.
- Data lives inside sentences, not beside them: "$16.7MM in OPS" and "+24% registration lift" appear mid-paragraph, not in standalone tables. The narrative carries the data; the data doesn't carry the narrative. Standalone data tables go in appendices.
- Everything connects — no isolated facts. Each initiative links to the next. The word "compound" signals this pattern. If a section doesn't connect to the one before it, restructure.
- Credit cross-functional partners by name or team. Shared wins build political capital. Worked example: "In partnership with Joel Mallory (MarTech) and Yogesh (Data Science), we validated OCI's measurement framework across 7 markets."
- Voice: most polished of all doc types. Longer sentences, more connective tissue between ideas.
- Signature phrases: "validated results," "measurement framework," "cross-functional collaboration," "connective tissue between platform capabilities and business objectives."
- Worked example: Bad: "OCI drove results." Good: "OCI's phased rollout across 7 markets validated a measurement framework that reduced CPA by 18% — a result that compounds as we extend to the remaining 3 markets in 2026."



## Evidence-Based Documents (Experiments & Testing Plans)
- **Experiment structure:** Question → Setup → Results → Recommendation. Worked example: "Does NB bid strategy reduce CPA?" → 6-week test, AU NB campaigns → CPA $168→$117 (-29%) → Adopt as baseline. Every experiment doc follows this exact arc — the question frames the setup, the setup frames the result, the result frames the ask.
- **Testing plan structure:** Goal → Phased plan (with target dates + status) → Supporting case studies → Other initiatives.
- **Data tables always include:** Impressions, Clicks, Cost, Registrations, CTR, CPC, CVR, CPA. Comparisons show absolute numbers AND percentages — never one without the other.
- **Interpretation pattern:** State the finding, then explain why it matters. Worked example: "CPA from platform was $700, which is still high, but half of what the overall test did" — the "but" clause is the interpretation.
- **Confidence calibration:** Signal certainty level explicitly. Use "What we can definitively say is..." for strong evidence, "it would be difficult to conclude that..." for weak evidence. Worked example: "83.4% PPR" and "5.8% chance that experiment would perform better" — Bayesian language when the data supports it.
- **Honesty about failures:** Never spin a negative result. "Bulk page did not perform better than the callback page." / "although regs too low to make strong conclusions." First person sparingly: "I found that," "I could have put more attention towards."
- **Cross-market evidence:** Quantify expectations and cite precedent. Worked example: "I would expect Adobe to allow for a 5%-15% improvement in CPA" backed by "MX market efficiency (case study)."



## Post-Mortem / Retrospective Documents
- Structure: Lessons Learned → Challenges → Accomplishments → Overview → Recommendations. Lead with lessons — the reader gets the learning immediately.
- Most self-critical format. First person: "I could have put more attention towards moving forward on the planning."
- Lessons are actionable, not abstract: "Start simple, then go granular" with specific example. Appendices for supporting data.



## Analytical & Procedural Documents (Investigation + How-To)

**Investigation structure:** Reference links → Data tables → Observations → Hypotheses → Evidence → Actions
**How-To structure:** Objective → Numbered Tactics (sequential) → Scenarios → Resources

Shared principles:
- Start with the anomaly or objective upfront
- Hypotheses/tactics clearly labeled and testable
- Evidence layered: high-level → market-level → query-level
- Cross-references multiple data sources (Adobe, Google Ads, Hubble, Quicksight)
- Scenario-based examples with specific numbers
- Distinguishes "proven" from "not proven or validated"
- Questions embedded for follow-up
- Warnings about what NOT to do

Investigation-specific:
- "Brand Paid Search is consistently saturated with ~97% ad visibility" (starts with anomaly)
- Distinguishes "proven" from "not proven or validated" — never overstates

How-To-specific:
- Imperative mood: "Set a realistic initial baseline" / "Observe actual ROAS data"
- Practical framing: "Managing ROAS bid strategy is not passive."



## Common Failures in Any Document Draft

| Failure | Rule | Fix |
|---------|------|-----|
| Bullets as primary content | Amazon docs are prose-driven; bullets only for 3-5 item enumerations | Rewrite as paragraphs |
| Bare noun headers | Headers must be questions or imperatives, never bare nouns | "How to optimize AU NB CPA" not "AU NB CPA Optimization" |
| Data without interpretation | Every table/data point needs a "so what" sentence | Numbers alone leave the reader guessing |
| Em-dashes in draft | Never use em-dashes in drafted documents | Replace with commas, periods, colons, or parentheticals |



## Knowledge-Sharing Documents

- Organized by scenario/use case rather than by tool
- Casual, peer-to-peer voice. Bullet points heavily.
- Practical examples: "Load files into Cedric and ask questions about the content"
- Honest about limitations: "AI isn't great at math/data analysis yet"
- Future ideas section at the end
