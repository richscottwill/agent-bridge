# ie%CCP Learning — 2026-03-30

## What Happened
During the W13 WBR callout pipeline, the dashboard ingester produced ie%CCP values of 6559% for MX (and similarly inflated values for all markets). The blind reviewer flagged this as a major data error.

## Root Cause
The ingester's `_read_ieccp()` method scanned column A from row 1 for market labels. The IECCP tab has multiple sections stacked vertically:
- Rows 1-12: CPA (per market)
- Rows 15-26: ie%CCP (the actual metric)
- Rows 30-48: CCP Segment (Brand/NB)
- Rows 75-93: CCP guidance values
- Rows 96-107: CCP per Account

The method matched "MX" at row 12 (CPA section) instead of row 26 (IECCP section). MX CPA of $65.59 was treated as an ie%CCP ratio, multiplied by 100 = 6559%.

## Fix Applied
Changed `_read_ieccp()` to first find the "IECCP" header row (row 15), then scan for market labels only in the rows immediately following it. This ensures it reads from the correct section.

## ie%CCP Calculation (documented in callout-principles.md)
- Formula: ie%CCP = CPA / CCP_per_Account
- CCP_per_Account = (Brand_CCP × Brand_Regs + NB_CCP × NB_Regs) / Total_Regs
- Target: 100% (break-even). Below 100% = efficient.
- MX CCP guidance: Brand $90, NB $30 (updated from $80 in context file)
- Brand subsidizes NB: Brand CPA (~$21) << Brand CCP ($90), so Brand generates surplus. NB CPA (~$134) >> NB CCP ($30), so NB loses in isolation. Blended ratio works because of Brand's surplus.

## Files Updated
- `shared/tools/dashboard-ingester/ingest.py` — fixed `_read_ieccp()` method
- `shared/context/active/callouts/callout-principles.md` — added ie%CCP reference section + pipeline process rules
- `shared/context/active/callouts/mx/mx-context.md` — corrected CCP guidance from $80 to $90 for Brand

## Process Learnings (also documented in callout-principles.md)
1. Dashboard ingestion must be the first step in the pipeline, not a manual checkpoint
2. Blind reviewer with 66% confidence threshold catches data errors the writers miss
3. Prose vs Note separation: data-grounded claims in prose, internal PS context in Note
4. Analyst-adjusted projections that differ >10% from ingester must be labeled
5. Rounding: compute from underlying numbers, not from rounded display values
