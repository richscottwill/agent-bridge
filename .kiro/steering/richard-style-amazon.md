---
inclusion: manual
---
# Richard Williams — Amazon Writing Norms Layer

Apply this on top of Richard's natural voice when writing for leadership (L7+), OP narratives, MBR/QBR write-ups, cross-org proposals, or any document read outside the immediate team.

## How to Apply (Without Losing Richard's Voice)
- Lead with the "so what" — result or recommendation first, then data support
- Use data to tell a story, not just report metrics. Each section should have a narrative arc.
- Connect to business impact: every key metric ties to registrations, OPS, or customer experience
- Be specific about what was tested and what was learned: "we tested X, learned Y, and are now doing Z"
- Acknowledge trade-offs and risks explicitly, then state the mitigation
- Use "we" for team accomplishments, credit cross-functional partners by name or team
- Avoid jargon that doesn't serve the reader — explain terms for broader audiences
- Tables for comparisons, narrative for interpretation. Always add the "so what" after a table.
- State confidence levels: "HIGH confidence" / "LOW confidence (insufficient volume)"

## Amazon Narrative Standard (from internal templates and Doc Ninja reviews)

These rules are derived from Amazon's Narrative Template, OP1 Template, MBR Template, Flash Template, Working Backwards Guide, and Doc Ninja-reviewed examples (Dog Safety Awareness, Contra-COGS MBR, Data Migration Narrative, Amazon Search OP1). They are non-negotiable for any document that goes to L7+.

### Appendix-heavy structure
The main body carries the narrative argument — results, insights, recommendations, decisions. Supporting material goes in the appendix: data tables, previous test results, program refreshers, team rosters, operational cadence, scope descriptions, and detailed methodology breakdowns. When the main body references supporting data, it cites the appendix section by name (e.g., "see Appendix: OCI Validated Results"). The one exception: a decision table or investment summary that IS the argument belongs in the main body. Everything else is appendix. This keeps the main body tight and readable while preserving all detail for readers who want to drill in. The appendix does not count against word count or Economy scoring.

### Prose over bullets
Amazon documents are narrative-driven. Write in complete paragraphs with connective tissue between ideas. Bullet lists are for short enumerations (3-5 items max) — never as the primary content format. The Narrative Template says: "Use the AMZN Body style for the rest of the text in the document." The body style is prose paragraphs, not bullet lists.

If a section is mostly bullets, rewrite it as prose. The test: if you removed all bullet formatting and the content became unreadable, the writing was relying on formatting instead of ideas.

### Sentence length and readability
Target 18-20 words per sentence average. The Doc Ninja review of the Dog Safety narrative praised "an average of 19.7 words per sentence and a reading ease score of 51.9 (we aim for over 50)." The Data Migration narrative was praised for "a concise average of 18.2 words per sentence."

One idea per sentence. No compound sentences with three clauses joined by commas. If a sentence has more than one verb phrase, split it.

### Purpose statement first
The Narrative Template structure: Purpose → Background → Problem/Opportunity → Recommendation → Next Steps. The purpose statement goes in the first paragraph: "State the purpose of your document. Explain what you need to happen, and why it matters to the business. If you're asking for a decision, state it up front."

### Data embedded in narrative
Instead of standalone tables followed by interpretation, weave numbers into prose: "We launched Tk improvements to Search YTD, yielding an incremental $Tk OPS (US: $Tk, ROW: $Tk)." Tables are for comparisons where the reader needs to scan across multiple dimensions — not for presenting sequential data points that could be a sentence.

### Cut anything duplicative
From the Working Backwards Guide: "Every sentence and quote should add unique value. Cut anything that's duplicative. Ask, 'does the reader really need to know this to understand the core value and capabilities?'"

### Structure by document type
- **Narrative:** Purpose → Background → Problem/Opportunity → Recommendation → Next Steps → FAQs
- **OP1:** Introduction (Mission/Vision) → Background → Previous Year Performance → Goals → Appendix
- **MBR:** Introduction → Goals Status (Green/Yellow/Red) → Wins → Misses → Key Insights → Discussion Topics → Appendix
- **Flash:** Overall Status (R/Y/G) → Path to Green → Project Overview → Updates → Risks → Coming Next → Goals

Confidence calibration:
| Level | Criteria | Example |
|-------|----------|---------|
| HIGH | 4+ weeks data, 1000+ events, consistent trend | "NB CPA decline is sustained — 7 consecutive weeks, HIGH confidence" |
| MEDIUM | 2-3 weeks data OR <500 events OR mixed signals | "Polaris impact unclear — 2 weeks, traffic down but CVR up, MEDIUM confidence" |
| LOW | <2 weeks, <100 events, single data point, or contradictory sources | "IT ad copy lift directional only — LOW confidence (97% fewer clicks than control)" |

## What NOT to Do
- Don't add corporate filler ("synergize," "leverage our learnings going forward")
- Don't remove Richard's parenthetical style — it makes docs more readable
- Don't over-formalize. Richard's OP1 doc is leadership-ready without sounding like a press release.
- Don't add hedging language. Richard's directness is an asset.
- Don't strip first-person accountability. "I could have put more attention towards..." is stronger than "there were delays in planning."

## Analytical Patterns for Leadership Context
- Always contextualize numbers using this pattern: [metric] [value] ([comparison]: [vs what], [interpretation]: [so what]). Example: 'AU NB CPA $118 (+3% WoW, -29% from 6wk ago) — bid strategy working, Polaris migration may cause short-term noise.'
- Compare across dimensions: test vs control, PoP, market vs market, channel vs channel
- Separate platform data from business data (Google Ads vs Hubble/internal)
- Attribute causation carefully: "seems to have allowed" not "caused"
- Include the "so what" — every data point connects to a recommendation
- Honest about limitations: "we'd need a longer timeline" / "volume too low to draw conclusions"
- ie%CCP always contextualized against target
- In testing plans, quantify expected improvement ranges: "5%-15%" not "significant"
