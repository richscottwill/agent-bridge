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
- When a WoW metric swing has multiple plausible causes (e.g., migration vs. seasonality vs. noise) and you can't distinguish between them yet, don't build the narrative around that metric. Acknowledge it, contextualize it against the recent range (e.g., "CVR has been up and down, but within a normal range"), and anchor the narrative to the driver with a clearer directional signal over a longer window (e.g., traffic trend since W9). The ambiguous metric gets a sentence; the clear trend gets the paragraph. Next week's data will clarify — let the story evolve rather than committing prematurely.

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
- Headline (standardized across all markets): regs, WoW%, spend WoW%, ie%CCP (MX), CPA. Monthly projection vs OP2. This format is fixed and should not vary market to market. Use neutral framing for OP2 comparison: "(vs. OP2, +X% spend, +Y% registrations)" — not "ahead of OP2" or "tracking OP2 at." The parenthetical contextualizes; it doesn't editorialize.
- WoW paragraph: Lead with what "we" did (or didn't do). Then Brand and NB performance together, Brand first if it drives more volume. Attribute to specific metrics (CVR, CPC, clicks).
- YoY paragraph (if available): Spend and regs YoY. Break out Brand vs NB drivers.
- Note: Internal PS context only. Forward-looking and actionable. What's happening next, not a diagnostic of what might have gone wrong. The Note should be operational, not analytical — what Richard did, what's pending, what decision is open. Use "I" voice. Example: "I gave Lorena projections for both 100% ie%CCP and 75% ie%CCP and asked for direction, so April spend may change noticeably." Don't speculate conditionally ("if CVR recovers, then CPA gains should follow"). State the fact and the timeline; let next week's data tell the rest.
- The WoW and YoY paragraphs exist to justify the headline numbers (regs, cost, CPA, ie%CCP). They are evidence, not separate stories. Use whichever lens (WoW, YoY, or both) best explains why the headline looks the way it does. If the YoY context is what makes the headline make sense, give it more space. If the WoW drivers tell the full story, compress YoY to a single sentence. The headline sets the question; the body answers it.
- Supplementary data (trend, anomalies, daily) goes below a `---` separator after the callout prose. This is for internal reference, not the WBR.

### Supplementary section format (below the `---`)
The supplementary section should include these items:
1. **Weekly trend (regs)**: Last 8 weeks of registration totals, formatted as `W5: 239 | W6: 257 | ...`
2. **Flagged anomalies**: Metrics that deviate >20% from recent average, or notable 8-week highs/lows.
3. **W{next} recommended spend**: A specific dollar amount for next week's spend, derived from the analyst's projection and the market's spend strategy (see Spend Strategy by Market below). Format: `W{next} recommended spend: $X,XXX (rationale)`.
4. **W{next} watch**: 2-3 bullet points on what to monitor next week (metric trajectories, competitive dynamics, data normalization).
5. **W{next} optimization**: 2-3 bullet points on actionable opportunities for next week based on seasonality, holidays, events, pending initiatives, or competitive shifts. These should be specific and forward-looking, not generic.

### Spend Strategy by Market
Each market has a different spend optimization goal. The analyst produces the recommended spend; the writer includes it in the supplementary section.

- **MX**: Target 100% ie%CCP. Recommended spend is the maximum weekly spend that keeps blended ie%CCP at or below 100%, given the current Brand/NB mix and CCP values. If ie%CCP is already above 100%, recommend reducing NB spend to bring it back. Brand spend follows seasonality; NB is the lever.
- **AU**: Target OP2 registration goals given seasonal expectations, while cutting wasted spend where possible. Recommended spend is the weekly amount needed to stay on track for the month's OP2 registration target, adjusted for seasonality, with a bias toward finding efficiency gains (reducing spend on low-converting segments or keywords without sacrificing registration volume). No ie%CCP constraint, no fixed CPA target.
- **All other markets (US, CA, JP, UK, DE, FR, IT, ES)**: Follow seasonality and OP2 goals. Recommended spend is the weekly amount needed to stay on track for the month's OP2 spend target, adjusted for weekday/weekend mix and known holidays in the remaining days.

## File Naming
- All files within a country folder must include the country code in the filename (e.g., `au-change-log.md`, not `change-log.md`). Filenames are standardized across countries, so the country code is the disambiguator.

## File Naming
- All files in country folders must be prefixed with the lowercase market code: `{market}-filename.md`.
- Examples: `au-2026-w12.md`, `mx-context.md`, `us-data-brief-2026-w12.md`, `de-projections.md`.
- This applies to callouts, data briefs, analysis briefs, context files, and projections.
- Filenames are standardized across countries; the prefix is what distinguishes them when viewed outside their folder.

## Style
- No em-dashes or arrows.
- No coaching or trainer voice in callouts. Callouts are written for a WBR audience, not as internal performance commentary. Phrases like "X is the unlock," "the path forward is Y," or action items directed at specific people (e.g., "Lorena's PO is overdue") do not belong in callout prose or Notes. Keep the tone analytical and market-facing. Task reminders and stakeholder follow-ups belong in the tracker or To-Do, not in callouts.
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
- AU is focused on hitting OP2 registration targets and cutting wasted spend, not ie%CCP.
- Promotions affect paid search through halo effect (site-wide promo visibility), not through ad copy changes. The promo sitelink drives some direct traffic, but the bigger impact is users seeing the promo elsewhere and converting at higher rates.
- Holidays cause 15-25% registration dips. Account for them in projections (50% reduction on holiday days).

## Conciseness
- Don't speculate on daily variance causes in the callout. If you can't prove a specific day's weakness was caused by something, don't put it in the WBR prose. Save it for the Note only if it's actionable.
- Simplify holiday references. The WBR audience doesn't need the holiday name. "A holiday on Monday" is enough. State the suppression fact (e.g., "44 regs vs average of 53") and move on.
- Don't quantify estimated holiday impact with false precision ("accounting for roughly 10-15 lost registrations"). Show the suppression, let the reader infer.
- Round projections to clean numbers. $90K not ~$92K. 1.4K not ~1,430. $63 not $64. The WBR wants scannable, round figures.
- Notes should be forward-looking and actionable ("Polaris migration is in progress and should be done this week"), not diagnostic ("Alexis flagged .co.uk URLs on 3/15, Thu/Fri were weak, could be URL disruption").
- If a detail only matters to the PS team and doesn't change the WBR narrative, it belongs below the `---` separator or in the Note, not in the WoW/YoY paragraphs.

## ie%CCP Metric Reference

ie%CCP (Incremental Efficiency % of Customer Contribution Profit) measures whether paid search spend is justified by the profit each registration generates. It is the ratio of CPA to CCP per account.

### Formula
```
ie%CCP = CPA / CCP_per_Account
```
Where:
```
CCP_per_Account = (Brand_CCP × Brand_Regs + NB_CCP × NB_Regs) / Total_Regs
```

### Interpretation
- ie%CCP < 100%: Efficient. CPA is below the profit each registration generates. Good.
- ie%CCP = 100%: Break-even. Spend equals the profit contribution. Target for MX.
- ie%CCP > 100%: Inefficient. Spending more per registration than the profit it generates.

### CCP Guidance Values (from IECCP tab, rows 75-93)
CCP values are the estimated Customer Contribution Profit per registration, set by finance. They differ by market and segment:
- MX: Brand CCP = $90, NB CCP = $30 (as of W13 2026; was $80/$30 in earlier context files, updated to $90/$30 in the dashboard)
- Other markets have their own Brand/NB CCP values (see IECCP tab rows 75-93)
- CCP values update periodically; always read from the dashboard, not from hardcoded context

### Levels of Calculation
The IECCP tab provides ie%CCP at multiple levels:
1. **Market total** (rows 16-26): Blended ie%CCP = Market CPA / Market CCP_per_Account. This is what goes in the callout headline.
2. **Brand/NB segment** (rows 28-48, "IECCP Segment"): Segment CPA / Segment CCP. Shows whether Brand or NB is the efficiency driver. Brand ie%CCP is typically very low (efficient) because Brand CPA is much lower than Brand CCP. NB ie%CCP is typically high (inefficient) because NB CPA often exceeds NB CCP.
3. **CCP per Account** (rows 96-107): The blended CCP per registration, weighted by Brand/NB mix. This is the denominator in the market-level ie%CCP formula.
4. **WW and EU5 aggregates** (rows 24-25 in IECCP section): Aggregated across markets.

### Why Brand Subsidizes NB
Brand CCP ($90 for MX) is much higher than Brand CPA (~$21), so each Brand registration generates significant profit. NB CCP ($30 for MX) is much lower than NB CPA (~$134), so each NB registration loses money in isolation. The blended ie%CCP works because Brand's surplus covers NB's deficit. This is why the Brand/NB registration mix matters for ie%CCP: more Brand regs = lower blended ie%CCP.

### MX-Specific Rules
- MX ie%CCP target: 100% (break-even). This is the primary budget constraint.
- Every MX callout must include ie%CCP in the headline.
- When ie%CCP approaches or exceeds 100%, NB spend should be reduced.
- April OP2 budget ($35K) is significantly lower than March's run rate (~$96K), so ie%CCP will tighten.

### Ingester Bug (Fixed 2026-03-30)
The dashboard ingester was reading CPA values (rows 2-12) instead of ie%CCP values (rows 16-26) because both sections use the same market labels in column A. The fix: scan for market rows only after the "IECCP" header row (row 15). If ie%CCP values appear as >10 (e.g., 6559%), they are CPA values being misread. Correct ie%CCP values are in the 0.0-1.5 range (0-150%).

## Pipeline Process Rules (from W13 2026 learnings)

### Change Log Staleness Check
- During Phase 1, check the last entry date in each market's change log. If the most recent entry is older than the target week (i.e., no entries within the W{NN} date range), the change log is stale for that week.
- When the change log is stale: do NOT claim "we didn't change budgets" or "we made no campaign changes." Absence of entries means the log hasn't been updated, not that no changes were made. Richard updates these manually from a CSV; they are often a week or more behind.
- Never assume no changes were made. If the log has no entries for the target week, omit the "what we did" framing entirely. Go straight into metric drivers. The Note section can flag: "Change log not updated for W{NN}."
- If the change log IS current (has entries dated within the target week), then you can reference specific actions in the WoW paragraph as potential contributors (with softened causal language per Attribution rules).
- This applies to all markets. AU and MX share a CSV (AB - Change Log - MX_AU.csv). NA/JP and EU5 have separate CSVs. All are manually maintained.

### Dashboard Ingestion
- The WBR callout pipeline MUST include dashboard ingestion as its first step. Don't assume data briefs exist.
- Run: `python3 ~/shared/tools/dashboard-ingester/ingest.py <path_to_xlsx>`
- The ingester generates: per-market data briefs, WW summary, JSON extract, and DuckDB updates.
- If the ingester fails, fix the bug before proceeding. Don't skip to manual analysis.

### Confidence Threshold
- The blind reviewer scores each callout on a Confidence dimension (0-100%): what percentage of the narrative is verifiable from the data brief alone.
- Threshold: 66%. Any market scoring below 66% gets sent back to the writer for revision.
- The fix for low confidence: move external context claims (migrations, competitor names, budget changes, regulatory events) from the WoW/YoY prose to the Note section. The prose should be data-grounded; the Note carries internal PS context.

### Prose vs. Note Separation
- WoW/YoY prose: Only claims verifiable from the data brief. Metric changes, percentage movements, trend observations.
- Note section: Internal PS context. Campaign changes, migrations, competitor dynamics, stakeholder actions, forward-looking plans. This is where the "why" lives when the data brief doesn't carry it.
- This separation ensures the WBR audience (non-PS stakeholders) can read the prose without needing PS-internal context, while the PS team gets the full picture in the Note.

### Reviewer Feedback Loop
- The reviewer performs a BLIND review: it only sees callout drafts + raw data briefs + callout principles. No analysis briefs, no context files, no meeting notes.
- When the reviewer finds data mismatches or confidence issues, it passes feedback back to the responsible writer agent.
- The writer agent receives the feedback + its own context files and either fixes the issue or explains why the reviewer is wrong (with evidence from the change log or context file).
- This creates an adversarial check that prevents the pipeline from rubber-stamping its own work.

### Rounding Methodology
- Always compute WoW% from the underlying numbers, not from rounded display values.
- Round to the nearest whole number. If the calculation gives -14.3%, use -14%, not -13%.
- When the data brief's headline says one number but the underlying math gives another (due to rounding of the display values), use the math. The data brief's headline rounds are for display; the callout should be accurate.

### Projection Sourcing
- The ingester produces a linear projection (simple daily average extrapolation). This is the default.
- Analyst-adjusted projections (accounting for weekday/weekend mix, holidays, fiscal year-end, etc.) may differ from the ingester's estimate.
- If the callout uses an analyst-adjusted projection that differs from the ingester's by more than 10%, it must be labeled in the Note as "analyst-adjusted" with a brief rationale.
