---
title: Campaign Link Generator Spec
status: DRAFT
audience: amazon-internal
level: 3
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: reftag convention changes, new markets added, tool built
---

# Campaign Link Generator — Tool Spec

---

## Problem

Every promo cycle (Memorial Day, Prime Day, Back to Biz, etc.) requires updating sitelink URLs across multiple markets with correct reftags, landing page paths, and UTM parameters. This is manual, error-prone, and repetitive.

## Proposed Solution

A simple tool that takes inputs (market, promo name, landing page, campaign type) and outputs correctly formatted URLs with reftags.

## Input

| Field | Example | Required |
|-------|---------|----------|
| Market | AU, MX, US, UK, etc. | Yes |
| Promo name | memorial-day-2026 | Yes |
| Landing page path | /cp/ps-brand | Yes |
| Campaign type | brand, nb, engagement | Yes |
| Custom reftag suffix | (optional override) | No |

## Output

```
Full URL: https://business.amazon.com.au/en/cp/ps-brand?ref=ps_au_nb_memorial-day-2026
Sitelink URL: https://business.amazon.com.au/en/cp/ps-brand?ref=ps_au_sl_memorial-day-2026
```

## Reftag Convention

`ps_[market]_[type]_[promo/campaign]`

| Component | Values |
|-----------|--------|
| ps | Always "ps" (paid search) |
| market | au, mx, us, uk, de, fr, it, es, ca, jp |
| type | brand, nb, sl (sitelink), eng (engagement) |
| promo | kebab-case promo/campaign name |

Consistent reftags are how we track which campaigns drive registrations. A wrong reftag means lost attribution. This tool eliminates the most common source of reftag errors: manual URL construction.

## Implementation Options

1. Python script (simplest — Richard can run locally)
2. Google Sheets formula (team can use without technical setup)
3. Internal web tool (if Level 3 adoption is the goal)

Option 2 (Google Sheets) is the Level 3 play — it's the version teammates will actually use. Build v1 as Python for validation, then convert.

## Next Steps
- [ ] Build v1 as Python script
- [ ] Test with AU sitelink update scenario
- [ ] If useful, convert to Google Sheets for team adoption


## Sources
- Tool proposed in device.md — source: ~/shared/context/body/device.md → Tool Factory → #2 Campaign link generator
- Impact estimate (30-60 min per promo cycle) — source: ~/shared/context/body/device.md → Tool Factory table
- Level 3 goal (team adoption) — source: ~/shared/context/body/brain.md → Five Levels → Level 3

<!-- AGENT_CONTEXT
machine_summary: "Tool spec for a campaign link generator that outputs correctly formatted URLs with reftags for promo cycles. Eliminates manual URL construction errors. Reftag convention: ps_[market]_[type]_[promo]. Build as Python first, then Google Sheets for team adoption (Level 3)."
key_entities: ["reftag", "campaign links", "sitelinks", "promo cycles", "Google Sheets", "Level 3"]
action_verbs: ["generate", "validate", "format", "convert", "adopt"]
update_triggers: ["reftag convention changes", "new markets added", "tool built", "promo cycle"]
-->
