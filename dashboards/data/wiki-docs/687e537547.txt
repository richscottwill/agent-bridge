
---
---

title: "Revisions: competitive-landscape.md"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
<!-- DOC-0466 | duck_id: wiki-review-competitive-landscape-revisions -->
# Revisions: competitive-landscape.md

Reviewer: wiki-critic
Date: 2026-03-25
Verdict: REVISE

---

## Core Issue

This article and the published `competitive-intel-tracker.md` cover 80% of the same content. The staged article is the better doc (strategic framing, decision guide, "so what" blocks), but publishing both creates duplication that will decay at different rates.




**Merge and replace.** Publish this article as the canonical competitive reference. Archive `competitive-intel-tracker.md`. This article is strictly superior — it has everything the tracker has plus strategic interpretation.

## Required Edits

### 1. Add explicit replacement note in frontmatter

Quote to change:
```
depends_on: []
```

Replace with:
```
depends_on: []
replaces: "competitive-intel-tracker"
## Context

Competitive pressure on AB Paid Search has intensified significantly since mid-2024.
```

Replace with:
```
## Context

> This doc replaces the Competitive Intelligence Tracker (previously in `reporting/`). All competitive data now lives here.

Competitive pressure on AB Paid Search has intensified significantly since mid-2024.
```

### 2. Add "Last validated" dates to competitor entries

The EU5 table has no per-entry freshness indicator. A reader can't tell if weareuncapped.com's 24% IS was measured last week or three months ago.

Quote to change:
```
| UK | weareuncapped.com | 24% Brand | +45% Brand Core CPC | Dec 2023 | Most persistent EU competitor |
```

Replace with:
```
| UK | weareuncapped.com | 24% Brand | +45% Brand Core CPC | Dec 2023 | Most persistent EU competitor. IS validated W10 2026. |
```

Apply the same pattern to all EU5 and International rows — add "IS validated W[X] 2026" to the Notes column based on the most recent WBR callout that confirmed the IS figure.

### 3. Add update cadence section

The doc needs an explicit update protocol so it doesn't become the same stale tracker it's replacing.

Add before the Related section:

```
## Update Cadence

- **Weekly:** Check auction insights for IS changes >5% in any market. Update the relevant row.
- **Monthly:** Full competitive review across all markets after MBR data refresh.
- **Ad hoc:** When WBR data shows unexpected CPC/CPA spikes, investigate and update.
- **Quarterly:** Review whether any competitor has exited (>8 weeks absent) and archive their row.
```

### 4. Fix consumed_by to include callout writers

Quote to change:
```
consumed_by: ["wiki-concierge", "abix-analyst", "najp-analyst", "eu5-analyst", "callout-reviewer"]
```

Replace with:
```
consumed_by: ["wiki-concierge", "abix-analyst", "najp-analyst", "eu5-analyst", "abix-callout-writer", "najp-callout-writer", "eu5-callout-writer", "callout-reviewer"]
```

The callout writers need competitive context too, not just the analysts.

---

## Post-Publish Action

After publishing this article, the wiki-librarian should archive `competitive-intel-tracker.md` from `reporting/` and update the wiki-index to point to this article instead.
