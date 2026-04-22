---
inclusion: manual
---
# Richard Williams — Amazon Writing Norms Layer

Apply this on top of Richard's natural voice when writing for leadership (L7+), OP narratives, MBR/QBR write-ups, cross-org proposals, or any document read outside the immediate team.

## How to Apply (Without Losing Richard's Voice)

- **Lead with the "so what"** — result or recommendation first, then data support. Use data to tell a story, not just report metrics. Each section should have a narrative arc connecting to business impact (registrations, OPS, or customer experience).
- **Be specific about what was tested and what was learned:** "we tested X, learned Y, and are now doing Z." Acknowledge trade-offs and risks explicitly, then state the mitigation. State confidence levels: "HIGH confidence" / "LOW confidence (insufficient volume)."
- **Use "we" for team accomplishments,** credit cross-functional partners by name or team. Example: "We partnered with MarTech to launch OCI in AU" not "I launched OCI in AU."
- **Avoid jargon that doesn't serve the reader** — explain terms for broader audiences. Example: "OCI (Offsite Conversion Improvement, a pixel-based attribution tool)" on first use in cross-org docs.
- **Tables for comparisons, narrative for interpretation.** Always add the "so what" after a table. Example: after a CPA-by-market table, write "MX leads the efficiency gains, suggesting the bid strategy scales best in high-growth markets."

## Amazon Narrative Standard (from internal templates and Doc Ninja reviews)

These rules are derived from Amazon's Narrative Template, OP1 Template, MBR Template, Flash Template, Working Backwards Guide, and Doc Ninja-reviewed examples (Dog Safety Awareness, Contra-COGS MBR, Data Migration Narrative, Amazon Search OP1). They are non-negotiable for any document that goes to L7+.

### Source Templates
Narrative Template, OP1 Template, MBR Template, Flash Template, Working Backwards Guide, Doc Ninja-reviewed examples (Dog Safety Awareness, Contra-COGS MBR, Data Migration Narrative, Amazon Search OP1).

### Document Structure & Writing Discipline
Main body = the argument (results, insights, recommendations, decisions). Appendix = supporting material (data tables, test results, program refreshers, rosters, methodology). Cite appendix by name: "see Appendix: OCI Validated Results." Exception: a decision table that IS the argument stays in the body. Appendix does not count against word count.

Write in complete paragraphs with connective tissue. Bullets only for short enumerations (3-5 items). If a section is mostly bullets, rewrite as prose. Litmus test: remove all bullet formatting. If the content becomes unreadable, the writing relied on formatting, not ideas.

Sentence discipline: target 18-20 words average. One idea per sentence. Split any sentence with more than one verb phrase. Never use em-dashes; replace with commas, periods, colons, or parentheticals.

Purpose statement in paragraph one: what you need to happen and why it matters. If asking for a decision, state it up front. Structure: Purpose → Background → Problem/Opportunity → Recommendation → Next Steps.

**Worked example (before/after):**
Before: "We have been working on several initiatives across AU and MX markets, including OCI rollout, bid strategy optimization, and landing page testing, and we believe these efforts will drive significant improvements in CPA and registration volume going forward."
After: "AU and MX CPA improved 18% QoQ through three coordinated changes: OCI rollout (7/10 markets live), automated bid strategies (NB CPA down 29%), and Polaris LP migration. We recommend scaling the OCI playbook to the remaining three markets by W20."
Why: The "after" leads with the result, attributes causation to specific actions, and ends with a recommendation. The "before" buries the point in a compound sentence with no data.

**Worked example (bullet-to-prose conversion):**
Before: "Key changes this quarter: • Migrated 7/10 markets to Polaris • Reduced NB CPA by 29% • Launched OCI in AU and MX • Paused IT due to low volume"
After: "Three changes drove this quarter's results. We migrated seven of ten markets to Polaris, which reduced NB CPA by 29%. We launched OCI in AU and MX to improve attribution accuracy. We paused IT spend after volume dropped below statistical significance thresholds."
Why: The "before" is a bullet list with no causal links. The "after" connects each action to its outcome and sequences them logically. Each sentence carries one idea.

### Common Failures in Document Structure
1. **Bullet-list documents.** If >50% of a section is bullets, it's not a narrative. Rewrite as prose with connective tissue. Worked example: "We tested three approaches: (1) bid caps, (2) NB shift, (3) OCI efficiency" is a bullet list disguised as a sentence. Rewrite: "We tested bid caps first, then shifted budget to NB, and finally optimized OCI efficiency — each building on the previous result."
2. **Missing purpose statement.** The first paragraph must state what you need to happen and why. If a reader finishes paragraph one without knowing the ask, the doc fails.
3. **Appendix confusion.** Data tables that ARE the argument belong in the main body. Data tables that SUPPORT the argument go in the appendix. The test: would removing this table break the narrative flow? If yes, keep it in the body.

### Data & Document Structure
Weave numbers into prose: "We launched Tk improvements to Search YTD, yielding an incremental $Tk OPS (US: $Tk, ROW: $Tk)." Tables are for multi-dimension comparisons, not sequential data points. Contextualize: [metric] [value] ([comparison]: [vs what], [interpretation]: [so what]). Example: 'AU NB CPA $118 (+3% WoW, -29% from 6wk ago) — bid strategy working, Polaris migration may cause short-term noise.' Compare across dimensions: test vs control, PoP, market vs market, channel vs channel. Separate platform data from business data (Google Ads vs Hubble/internal). Attribute causation carefully: "seems to have allowed" not "caused". Every data point connects to a recommendation. Honest about limitations: "we'd need a longer timeline" / "volume too low to draw conclusions". ie%CCP always contextualized against target. In testing plans, quantify expected improvement ranges: "5%-15%" not "significant".

**Document type structures:**
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

**Worked example:** "AU NB CPA improved from $187 to $168 over the past 3 weeks (MEDIUM confidence, <500 weekly events). We need 2 more weeks of data before recommending this as the new baseline bid strategy." Note: confidence level stated inline, limitation named, and next step tied to the confidence gap.


