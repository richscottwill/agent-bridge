---
inclusion: manual
---
# Richard Williams — WBR Callout Style Guide

## Structure (per market, per week)
Every WBR callout follows this pattern:

1. Headline metric: "[Market]: [Market] drove [X] registrations ([+/-]% WoW), with [+/-]% spend WoW" — sometimes includes CPA and ie%CCP
2. Monthly projection: "[Month] closed/is projected at $[X] spend and [X] registrations at $[X] CPA. (vs. OP2: [+/-]% spend, [+/-]% registrations)" — include both spend and registrations vs OP2 when registration targets are available. Use "ahead of OP2" for positive, parenthesized format for negative.
3. WoW explanation: What changed and why. Always attributes movement to a specific cause (bid strategy, Brand traffic, CVR shift, seasonal event, budget adjustment)
4. YoY context: "YoY we spent [X]% with [+/-]% registrations." Often breaks out Brand vs NB.
5. Notes: Separate "Note:" lines for context that doesn't fit the main narrative

## Paragraph 1 formula (explicit — blocks REVISE if violated)

The headline paragraph MUST include, in this order:
1. Headline registrations + WoW % (e.g., "MX drove 659 registrations (+22% WoW)")
2. Spend WoW % (e.g., "with -7% spend WoW")
3. CPA + WoW % change (e.g., "CPA improved to $36 (-24% WoW)")
4. **ie%CCP + vs target — required when ie%CCP data is available for the market.** Format: "45% ie%CCP (vs. 70% target)". Missing ie%CCP in paragraph 1 is a REVISE-level failure. Markets without ie%CCP (AU, which has no target) skip this slot.
5. Monthly projection: "[Month] closed/is projected at $[X] spend and [X] registrations at $[X] CPA. (vs. OP2: [+/-]% spend, [+/-]% regs)"

Market-specific ie%CCP targets:
- MX: 70%
- US, CA, UK, DE, FR, IT, ES, JP: 100%
- AU: no target (skip the slot)

## WoW attribution must decompose into clicks × CVR

Don't write "Brand regs +23% WoW on -5% spend" and stop. Decompose: "Brand regs +23% on +14% clicks and +8% CVR" or "Brand regs -5% on +5% clicks and -9% CVR." The point is what drove the movement, not just the movement itself. Apply the same to NB.

## YoY attribution must decompose (when data is informative)

"YoY regs +345% on -11% spend" is the starting point, not the end. Break into the drivers: clicks YoY and CVR YoY, separately for Brand and NB where one side dominates. Example: "YoY increase can be attributed mostly to two things: First, Brand clicks have increased 201% YoY, and second, both Brand and NB are seeing 100%+ CVR YoY for both Brand and NB (+134% and +105% respectively)."

## Concrete past-tense actions, not future intent

"I have increased MX NB budgets to bring ie%CCP closer to the 70% target." → Specific, done, with the right target number.
"I will continue to run MX against the ie%CCP constraint" → Vague, forward-looking, no specific number. Wrong.

## Cross-channel context when it reframes the read

When PS WoW is better or worse than the overall channel mix, state it. Example from Richard's MX W18 edit: "MX market in general decreased, with Unknown dropping 29% from 591 to 417." This reframes +22% PS as bucking the channel trend. Example from AU W18: "Looking at the WoW registrations of other channels, most of the channels decreased between 20%-30%. (with the exception of Email/Direct, the two lowest volume channels)." This reframes -7% PS as outperforming the channel trend. Cross-channel data source: the WW Dashboard xlsx itself (not currently in DuckDB; must pull from the drop).

## Voice Register & Structural Patterns

### Pronoun Rules
- "We" for intentional team actions: "WoW we focused on reducing CPA" / "WoW we pulled budgets back"
- "I" for personal decisions and accountability: "I will continue to test" / "I have adjusted CPA targets" / "This mistake was not caught until mid-month, so I have updated my reporting"

### Required Structural Elements
- Always separates Brand and NB performance
- Causal attribution is always specific, never vague "performance improved"
- Includes forward-looking actions: "I will continue to test with the bid strategies for about a week"
- ie%CCP always contextualized vs. target
- "Note:" lines for holidays, external factors, investigations
- Asterisked (*) deep-dive bullets below the main callout for additional detail

### Tone
- Dense, analytical. Every word carries data.
- Parenthetical data is extremely frequent: "(+13% clicks/+19% registrations)" / "(cost-efficiency)" / "(resolved, increased budgets)"
- Flags unexpected results: "which is unexpected, since last week was a holiday week"

## Common Callout Failures
Watch for these in every callout draft:

### Formatting Rules
- **Word count:** Target 110 words per callout (±10). Only prose paragraphs count — appendix notes (weekly trend, anomalies, daily breakdown) are excluded.
- **Volume changes:** Use percentages, not raw numbers. Write "NB regs fell -33%" not "NB regs fell -33%, 110→74". Absolute values belong in the appendix. Only include raw volumes when the number itself is the point (headline registrations, a CPA dollar amount, a stakeholder threshold).
- **Week references:** Plain text, no parentheses. Write "from W7 to W14" not "from (W7) to (W14)". Parentheses are for percentage changes and dollar amounts.
- **No OP2 in projection tables:** Projection tables show Regs, Spend, CPA, ie%CCP only. No "vs OP2 Spend" column. However, the monthly projection line in the callout prose must always include vs OP2 spend comparison.

The source of truth for all callout writing rules is the callout-writer agent definition at `shared/.kiro/agents/wbr-callouts/callout-writer.md`. Callouts are generated via the WBR callout pipeline hook at `shared/.kiro/hooks/wbr-callouts.kiro.hook`. Do not invoke the callout-writer or callout-reviewer agents directly — use the hook.

### Content Errors
1. **Vague attribution.** Wrong: "performance improved." Right: "Brand registrations increased +19% due to exact match impressions +40%." Every movement needs a specific cause: bid strategy, CVR shift, seasonal event, or budget change. If the cause is unknown, say "under investigation" rather than omitting.
2. **Missing YoY context.** Always include YoY comparison when available. WoW alone doesn't show whether the trend is structural or seasonal. Format: "YoY we spent [X]% with [+/-]% registrations." If YoY data is unavailable, state why (new market, new campaign type).
3. **ie%CCP without target comparison.** Never report ie%CCP in isolation. Always contextualize vs. target: "97% ie%CCP (vs. 100% target)" or "brought ie%CCP below the 100% target, averaging 97%."
4. **Em-dashes in callout draft.** Never use em-dashes in drafted callouts. Replace with commas, periods, colons, or parentheticals. Scan every draft before finalizing.
5. **Editorial narrator voice.** Wrong: "Both segments accelerated." / "First week since W14 where X and Y moved together." / "A choice, not a miss." / "Consistent with a post-Anzac softening rather than a structural shift." These editorialize instead of describing. Write like a PS manager reporting data, not an analyst framing a narrative. Right: "Both segments increased WoW." / "Brand regs +23% on +14% clicks and +8% CVR." State the move, attribute the cause, stop.
6. **Future intent dressed as action.** Wrong: "I will continue to run MX against the ie%CCP constraint" (vague, forward, no target number). Right: "I have increased MX NB budgets to bring ie%CCP closer to the 70% target" (past tense, specific, measurable). Future-intent sentences belong in the appendix "W19 optimization" section, not in the prose paragraphs.

### Worked Failure Example
Draft: "MX drove 300 registrations — performance improved — with 97% ie%CCP." Three failures: (1) em-dash used twice, (2) vague attribution ("performance improved"), (3) ie%CCP without target. Fix: "MX drove 300 registrations (+13% WoW), with Brand clicks +13% driving the increase, and 97% ie%CCP (vs. 100% target)."

## Examples (actual, by market)

### Emerging Markets (lower volume, more narrative)

**MX W10:** "MX drove 300 registrations (+13% WoW), +4% spend WoW, 97% ie%CCP. March projected: $84K spend, 1.2K regs (vs. OP2: +68% spend, +45% regs). Minimized NB spend changes (+5%); registration increase attributed to Brand campaigns (+13% clicks/+19% regs)."

**AU W7:** "WoW we didn't change budgets, but saw improvement on both Brand and NB. Brand: 41% increase in registrations due to exact match terms increasing impressions by 40%. NB: bid strategies managing campaigns more efficiently — registrations +15%, spend -10%."

**AU Failure-Correction:** Draft: "AU drove 850 registrations — NB improved — with CPA at $132 and 94% ie%CCP." Failures: (1) em-dash, (2) vague NB attribution, (3) ie%CCP without target, (4) missing YoY. Fix: "AU drove 850 registrations (+8% WoW), NB bid strategies reducing CPA 12% while holding volume. CPA $132 (vs. $140 target), 94% ie%CCP (vs. 100% target). YoY: -5% spend, +12% registrations."

### Established Markets (high volume, OCI live)

**JP W40:** "JP: 1,180 registrations (+40% WoW, +183% YoY) and $20 CPA (-19% WoW, -35% YoY). Registrations continued to increase after W38 holiday. Optimization work (negatives, pausing redundant keywords, refining ad text, adjusting budgets/bids) wasn't the primary driver — increase attributed to core terms being eligible for more traffic."

**Why JP works:** Leads with headline metric, includes WoW and YoY, attributes cause (core terms traffic), honestly notes optimization wasn't the primary driver.

## Data Source Quick Reference

### Metric Sources

| Metric | Source | Update Cadence |
|--------|--------|---------------|
| Regs, CPA, Spend, CVR | WW Dashboard xlsx → DuckDB weekly_metrics | Weekly (Richard drops xlsx) |
| ie%CCP | WW Dashboard → DuckDB weekly_metrics | Weekly |
| OCI status | DuckDB oci_status table | On change |
| Competitor IS | Google Ads Auction Insights → DuckDB competitors | Weekly |
| YoY baselines | WW Dashboard Y25 Final | Annual |

### Query Examples

**Worked data-source example:** Writing AU W10 callout → query `ps.v_weekly WHERE market='AU' AND period_key='2026-W10'` for regs/spend/CPA. Check `ps.v_weekly WHERE market='AU' AND period_key='2025-W10'` for YoY. Pull ie%CCP from same table. If competitor IS needed, query DuckDB competitors table for AU Brand auction insights.

### Common Data Pitfalls

**Common data-source failure:** Using stale YoY baselines from memory instead of querying the Y25 Final table. If the YoY comparison doesn't match the WW Dashboard, the baseline is wrong — re-pull from the Annual source before publishing.
