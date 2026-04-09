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

## Voice
- Dense, analytical. Every word carries data.
- "We" for intentional team actions: "WoW we focused on reducing CPA" / "WoW we pulled budgets back"
- "I" for personal decisions and accountability: "I will continue to test" / "I have adjusted CPA targets" / "This mistake was not caught until mid-month, so I have updated my reporting"
- Parenthetical data is extremely frequent: "(+13% clicks/+19% registrations)" / "(cost-efficiency)" / "(resolved, increased budgets)"

## Key Patterns
- Always separates Brand and NB performance
- Causal attribution is always specific — never vague "performance improved"
- Flags unexpected results: "which is unexpected, since last week was a holiday week"
- Includes forward-looking actions: "I will continue to test with the bid strategies for about a week"
- Asterisked (*) deep-dive bullets below the main callout for additional detail
- "Note:" lines for holidays, external factors, investigations
- ie%CCP always contextualized vs. target

## Examples (actual, by market)

### Established Markets (high volume, OCI live)
These markets have mature data — callouts emphasize optimization, competitive response, and YoY trends.

#### JP Example
JP Week 40: "JP: 1,180 registrations (+40% WoW, +183% YoY) and $20 CPA (-19% WoW, -35% YoY) Registrations continued to increase after the holiday in Week 38. Last week I worked a lot to make the phrase match campaigns more efficient by adding negatives, pausing redundant keywords, refining ad text, and adjusting budgets/bids, but this increase seems to be more because of our core terms being eligible for more traffic."

### Emerging/Hands-On Markets (lower volume, more narrative)
These markets need more causal explanation — callouts emphasize what changed and why.

#### MX Example
MX Week 10: "MX drove 300 registrations (+13% WoW), with +4% spend WoW, and 97% ie%CCP. March is projected to end at $84K spend and 1.2K registrations. (vs. OP2: +68% spend, +45% registrations) WoW we minimized changes to NB spend (+5%), and overall registrations increased +13%. The increase in registrations can be attributed to Brand campaigns (+13% clicks/+19% registrations)"

#### AU Example
AU Week 7: "WoW we didn't change budgets, but saw an improvement on both Brand and NB. On the Brand side, the 41% increase in registrations was due to our exact match Brand terms increasing in impressions by 40%... On the NB side, the bid strategies seem to be managing the campaigns more efficiently; increasing registrations by 15%, while reducing spend by 10%."

## Common Callout Failures
Watch for these in every callout draft:

### Formatting Rules
- **Word count:** Target 110 words per callout (±10). Only prose paragraphs count — appendix notes (weekly trend, anomalies, daily breakdown) are excluded.
- **Volume changes:** Use percentages, not raw numbers. Write "NB regs fell -33%" not "NB regs fell -33%, 110→74". Absolute values belong in the appendix. Only include raw volumes when the number itself is the point (headline registrations, a CPA dollar amount, a stakeholder threshold).
- **Week references:** Plain text, no parentheses. Write "from W7 to W14" not "from (W7) to (W14)". Parentheses are for percentage changes and dollar amounts.
- **No OP2 in projection tables:** Projection tables show Regs, Spend, CPA, ie%CCP only. No "vs OP2 Spend" column. However, the monthly projection line in the callout prose must always include vs OP2 spend comparison.

The source of truth for all callout writing rules is the callout-writer agent definition at `shared/.kiro/agents/wbr-callouts/callout-writer.md`. Callouts are generated via the WBR callout pipeline hook at `shared/.kiro/hooks/wbr-callouts.kiro.hook`. Do not invoke the callout-writer or callout-reviewer agents directly — use the hook.

### Attribution Failures
1. **Vague attribution.** Wrong: "performance improved." Right: "Brand registrations increased +19% due to exact match impressions +40%." Every movement needs a specific cause — bid strategy, CVR shift, seasonal event, budget change.

### Context Failures
2. **Missing YoY context.** Always include YoY comparison when available. WoW alone doesn't show whether the trend is structural or seasonal. Format: "YoY we spent [X]% with [+/-]% registrations."

3. **ie%CCP without target comparison.** Never report ie%CCP in isolation. Always contextualize vs. target: "97% ie%CCP (vs. 100% target)" or "brought ie%CCP below the 100% target, averaging 97%."

4. **Em-dashes in callout draft.** Never use em-dashes (—) in drafted callouts. Replace with commas, periods, colons, or parentheticals. Scan every draft before finalizing.

## Data Source Quick Reference

| Metric | Source | Update Cadence |
|--------|--------|---------------|
| Regs, CPA, Spend, CVR | WW Dashboard xlsx → DuckDB weekly_metrics | Weekly (Richard drops xlsx) |
| ie%CCP | WW Dashboard → DuckDB weekly_metrics | Weekly |
| OCI status | DuckDB oci_status table | On change |
| Competitor IS | Google Ads Auction Insights → DuckDB competitors | Weekly |
| YoY baselines | WW Dashboard Y25 Final | Annual |
