# WBR Callout Principles

## Data Integrity
- Always verify claims against actual data before writing. If CVR is "elevated," check the recent weekly trend to confirm.
- Don't apply last year's seasonality blindly. If this year's baseline is structurally different (e.g., higher CVR from bid strategy maturity), the 2025 pattern may not apply.
- Projections should account for day-of-week patterns, holidays, and whether the current year's performance baseline has shifted from last year. Don't use simple linear projections.
- When projecting, Brand follows seasonality; NB is adjusted to match efficiency thresholds (100% ie%CCP for MX, efficiency-focused for AU).
- Show projected amounts vs OP2 in every callout headline.

## Attribution
- Don't attribute performance to a cause you can't back up with data. If you can't explain a CVR jump, say what happened and leave it. Don't guess "organic demand recovery" if the numbers don't support it.
- Always check whether a WoW change also occurred last year in the same week before calling it seasonal or non-seasonal.
- When actions were taken (negative keywords, bid strategy changes, budget adjustments), reference them as potential contributors, not definitive causes.
- Soften causal language. Say "likely confirming" or "potentially reflecting," not "confirming" or "driven by." The data suggests; it rarely proves.

## Framing
- Frame stabilization, not decline, when performance is settling into a new baseline post-promo or post-change.
- Don't draw excessive attention to negative trends. State the facts, explain the drivers, and move on.
- The WW Dashboard is the PS team's internal data, not the WBR. Callouts are written for the WBR audience (non-PS stakeholders) using PS data.

## Length
- Target: 110 words per market callout, plus or minus 10 words (100-120 word range). This is the prose above the `---` separator.
- The callout should be ~60% the length of the analysis brief's suggested narrative angle. If your draft is longer than 120 words, cut. Every sentence must earn its place.
- Supplementary data below the `---` separator does not count toward the word limit.
- When trimming to hit the word target, cut from wherever the narrative is least interesting that week, not from a fixed section. If the YoY story is the headline (e.g., +90% regs on -35% spend), give it more weight than the WoW paragraph. If the WoW story is the headline, compress YoY. The word budget follows the narrative weight, not the section order.

## Structure
- Headline (standardized across all markets): regs, WoW%, spend WoW%, ie%CCP (MX), CPA. Monthly projection vs OP2. This format is fixed and should not vary market to market.
- WoW paragraph: Lead with what "we" did (or didn't do). Then Brand and NB performance together, Brand first if it drives more volume. Attribute to specific metrics (CVR, CPC, clicks).
- YoY paragraph (if available): Spend and regs YoY. Break out Brand vs NB drivers.
- Note: Internal PS context only. Forward-looking and actionable. What's happening next, not a diagnostic of what might have gone wrong.
- The WoW and YoY paragraphs exist to justify the headline numbers (regs, cost, CPA, ie%CCP). They are evidence, not separate stories. Use whichever lens (WoW, YoY, or both) best explains why the headline looks the way it does. If the YoY context is what makes the headline make sense, give it more space. If the WoW drivers tell the full story, compress YoY to a single sentence. The headline sets the question; the body answers it.
- Supplementary data (trend, anomalies, daily) goes below a `---` separator after the callout prose. This is for internal reference, not the WBR.

### Supplementary section format (below the `---`)
The supplementary section should include three items:
1. **Weekly trend (regs)**: Last 8 weeks of registration totals, formatted as `W5: 239 | W6: 257 | ...`
2. **Flagged anomalies**: Metrics that deviate >20% from recent average, or notable 8-week highs/lows.
3. **W{next} watch**: 2-3 bullet points on what to monitor next week (metric trajectories, competitive dynamics, data normalization).
4. **W{next} optimization**: 2-3 bullet points on actionable opportunities for next week based on seasonality, holidays, events, pending initiatives, or competitive shifts. These should be specific and forward-looking, not generic.

## File Naming
- All files within a country folder must include the country code in the filename (e.g., `au-change-log.md`, not `change-log.md`). Filenames are standardized across countries, so the country code is the disambiguator.

## File Naming
- All files in country folders must be prefixed with the lowercase market code: `{market}-filename.md`.
- Examples: `au-2026-w12.md`, `mx-context.md`, `us-data-brief-2026-w12.md`, `de-projections.md`.
- This applies to callouts, data briefs, analysis briefs, context files, and projections.
- Filenames are standardized across countries; the prefix is what distinguishes them when viewed outside their folder.

## Style
- No em-dashes or arrows.
- No double line breaks between paragraphs (single line break).
- CPAs rounded to whole dollars.
- Percentages rounded to whole numbers.
- Large numbers formatted as "1.1K", "$139K", "$2.7M".
- Don't stack metric modifiers ("W11 WoW NB CVR swing"). State the metric, then the number.
- Don't include registration volume in the WoW/YoY narrative unless it absolutely demands it. The headline carries the total.
- Never write out raw amounts in WoW/YoY narrative (e.g., "from 147 to 122"). Use percentage changes only. The headline carries the totals.
- Always label percentage changes as WoW when they are week-over-week. Don't leave unlabeled percentages that could be ambiguous.
- Avoid "unusually large," "watching whether this holds," or hedging language. Be direct.
- When referencing WoW, just say the current week (e.g., "W11 WoW"), not "W10 to W11."
- Spend applies to both Brand and NB together; don't separate spend callouts by segment unless there's a meaningful divergence.
- Use "we" voice in the WoW/YoY narrative (team perspective). The Note section can use "I" for Richard's personal context.

## Context Awareness
- Brand generally converts more volume than NB in MX. Lead with Brand when both improved.
- AU has no YoY data (launched June 2025).
- MX ie%CCP is the primary budget constraint. Every MX callout should reference it.
- AU is focused on efficiency and bid strategy stabilization, not ie%CCP.
- Promotions affect paid search through halo effect (site-wide promo visibility), not through ad copy changes. The promo sitelink drives some direct traffic, but the bigger impact is users seeing the promo elsewhere and converting at higher rates.
- Holidays cause 15-25% registration dips. Account for them in projections (50% reduction on holiday days).

## Conciseness
- Don't speculate on daily variance causes in the callout. If you can't prove a specific day's weakness was caused by something, don't put it in the WBR prose. Save it for the Note only if it's actionable.
- Simplify holiday references. The WBR audience doesn't need the holiday name. "A holiday on Monday" is enough. State the suppression fact (e.g., "44 regs vs average of 53") and move on.
- Don't quantify estimated holiday impact with false precision ("accounting for roughly 10-15 lost registrations"). Show the suppression, let the reader infer.
- Round projections to clean numbers. $90K not ~$92K. 1.4K not ~1,430. $63 not $64. The WBR wants scannable, round figures.
- Notes should be forward-looking and actionable ("Polaris migration is in progress and should be done this week"), not diagnostic ("Alexis flagged .co.uk URLs on 3/15, Thu/Fri were weak, could be URL disruption").
- If a detail only matters to the PS team and doesn't change the WBR narrative, it belongs below the `---` separator or in the Note, not in the WoW/YoY paragraphs.
