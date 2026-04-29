# AU Paid Search State File — Agent Protocol

## Purpose
Market-specific parameters for the AU Paid Search daily state file. Loaded by the State File Engine (`state-file-engine.md`) during AM-Backend Step 2E and EOD Step 9. This file defines WHAT to analyze; the engine defines HOW to generate and deliver.

## Activation
This protocol is loaded by the state file engine when processing market='AU'. It is NOT invoked directly by hooks.

## AU-Specific Analytical Parameters

### CPA Constraint Model
- No ie%CCP target — CCP data expected July 2026
- Primary constraint: CPA at or below $140 (OP2 target)
- FY26 OP2: $1.8M budget, 12,906 regs, $140 CPA
- FY25 (Jun-Dec): $1.14M spend, 8,763 regs, $158 CPA
- No YoY data available until June 2026

### Key Thresholds
- NB CPC anomaly trigger: >$6.00 or reversal of the 7-week decline streak
- NB CVR baseline (post-bid-strategy): 2.5–3.5%
- Brand CVR normal range: 7.0–8.5%
- Brand CPA stability band: $35–$45
- Monthly projection method: weekday/weekend weighted daily rates, discounted 2-3% for persistent optimism bias

### Data Sources
- Primary: DuckDB `weekly_metrics` WHERE market='AU'
- Daily: DuckDB `daily_metrics` WHERE market='AU'
- Change log: DuckDB `change_log` WHERE market='AU'
- Projections: `~/shared/wiki/callouts/au/au-projections.md`
- Context: `~/shared/wiki/callouts/au/au-context.md`
- Stakeholder context: `~/shared/wiki/meetings/au-paid-search-sync.md`
- Quip tracker: https://quip-amazon.com/ZZR9AAs7OfO
- Quip testing: https://quip-amazon.com/IAJ9AAZJsDL
- Quip launch: https://quip-amazon.com/JMZ9AAput1I

### Stakeholder Context
- Primary: Lena Zak (L7, AU Country Leader) — data-demanding, expects numbers not narratives, has escalated to leadership
- Execution partner: Alexis Eck (L6, Sydney) — collaborative, defers to Lena on strategy
- Manager: Brandon Munday (L7) — approves budget changes, keyword strategy direction
- Previous: Harjeet Heer — stepped back from day-to-day AU

## Output Schema
The agent must produce a JSON object matching the placeholder taxonomy defined in the state file. All keys are required. Static sections (Goals, Tenets) are not in the JSON.

## Quality Gates
Before uploading to SharePoint:
1. Schema validation — all required JSON keys present
2. Math verification — CPA calculations match deterministic recalculation
3. Weasel word scan — zero violations
4. Style replication — static sections unchanged
5. Content replication — historical data matches DuckDB
