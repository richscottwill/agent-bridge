---
title: "AU Keyword CPA Dashboard — Design"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0365 | duck_id: reporting-au-keyword-cpa-dashboard -->

---
title: AU Keyword CPA Dashboard — Design
status: DRAFT
doc-type: execution
audience: amazon-internal
level: 1
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: weekly AU data pull, Lena feedback, dashboard ingester integration
---

# AU Keyword CPA Dashboard — Design

**STATUS: Design phase. Dashboard not yet built. First data pull pending.**

Due: Next week

---

## Purpose

Lena wants weekly CPA review at the keyword level. This dashboard provides a rolling 4-week view of AU keyword performance, highlighting CPA outliers and trends. Addresses Lena's 3 priorities: (1) keyword CPC/CPA investigation, (2) keyword-to-product mapping, (3) Polaris migration tracking.

## Data Sources

- Google Ads: keyword-level data (impressions, clicks, CPC, conversions, CPA)
- Export: weekly manual pull (no API access)
- Format: Excel/CSV → processed into summary

## Dashboard Structure

### Top 20 Keywords by CPA (highest first)
| Keyword | Match Type | Clicks | Regs | CPA | CPC | WoW Change | Action |
|---------|-----------|--------|------|-----|-----|------------|--------|

### Top 20 Keywords by Volume (most clicks)
| Keyword | Match Type | Clicks | Regs | CPA | CPC | WoW Change |
|---------|-----------|--------|------|-----|-----|------------|

### CPA Trend (4-week rolling)
- Week-over-week CPA by campaign type (Brand, NB)
- Target line: $140 CPA

### Keyword-to-Product Mapping
| Keyword Theme | Product Category | Landing Page | CVR | Notes |
|--------------|-----------------|--------------|-----|-------|

The Top 20 by CPA view is what Lena will look at first. If a keyword has CPA >$200 and meaningful volume, it's a candidate for pause or negative keyword addition.

## Delivery

- Format: Excel or Quip table (Lena's preference)
- Cadence: Weekly, delivered before AU sync
- Owner: Richard (manual until automated)

## Automation Opportunity

This is a candidate for the dashboard ingester tool. If the weekly Excel export follows a consistent format, the ingester could auto-generate this view.

## Next Steps
- [ ] Pull first week's data
- [ ] Build template in Excel/Quip
- [ ] Share with Alexis for feedback
- [ ] Present to Lena at next AU sync


## Sources
- Lena wants weekly CPA review — source: ~/shared/context/active/current.md → AU Paid Search Optimization
- Lena's 3 priorities — source: ~/shared/context/active/current.md → AU CPC Benchmark Response (Brandon sync 3/23)
- AU CPA target $140 — source: ~/shared/context/body/eyes.md → Market Health → AU
- Dashboard ingester tool — source: ~/shared/context/body/device.md → Tool Factory → #1 Dashboard ingester (BUILT)

<!-- AGENT_CONTEXT
machine_summary: "Design spec for a weekly AU keyword-level CPA dashboard. Addresses Lena Zak's request for keyword CPC/CPA investigation. Includes Top 20 by CPA, Top 20 by volume, 4-week CPA trend, and keyword-to-product mapping. Not yet built — design phase only."
key_entities: ["AU", "Lena Zak", "Alexis Eck", "keyword CPA", "CPC", "dashboard ingester", "Google Ads"]
action_verbs: ["pull", "build", "present", "automate", "flag"]
update_triggers: ["first data pull completed", "Lena feedback on format", "dashboard ingester integration", "weekly AU data refresh"]
-->
