---
name: wbr-callouts
description: "Full WBR callout pipeline for weekly business review. Covers all 10 markets: AU, MX, US, CA, JP, UK, DE, FR, IT, ES. Triggers on WBR, callout, weekly callout, market callout."
---

# WBR Callouts Pipeline

## Instructions

Sequential pipeline — follow each step in order:

1. **Load principles** — Read `callout-principles.md` from this skill's `references/` directory. These principles govern tone, structure, and quality thresholds for all callouts.

2. **Determine ISO week number** — Calculate the current ISO week number. This is used for file naming and callout headers.

3. **Run market-analyst for each market** — Invoke the market-analyst agent for each of the 10 markets (AU, MX, US, CA, JP, UK, DE, FR, IT, ES). The analyst reviews performance data, identifies notable movements, and assigns a confidence score (0-100%) to each potential callout.

4. **Run callout-writer for markets with >66% confidence** — For any market where the analyst assigned >66% confidence, invoke the callout-writer agent to draft the callout. The writer follows the callout principles and Richard's writing style.

5. **Run blind review across all callouts** — Invoke the callout-reviewer agent to perform a blind review of all drafted callouts. The reviewer checks for accuracy, tone, and adherence to callout principles without knowing which market each callout belongs to.

6. **Correct below threshold** — Any callout that scores below the quality threshold in blind review gets sent back to the callout-writer for revision. One revision pass only.

7. **Run validate-callout.sh** — Execute `scripts/validate-callout.sh` to check word count compliance (max 150 words per callout). Fix any violations.

8. **Present AU/MX highlights** — Surface AU and MX callouts first (Richard's hands-on markets), then present the remaining markets grouped by region.

## Notes

- The callout pipeline is sequential: analyst → writer → reviewer. Don't skip steps.
- Load the relevant writing style guide (richard-style-wbr.md) before any writing.
- Callouts additionally require callout-principles.md from references/.
