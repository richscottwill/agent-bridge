---
title: "Negative Keyword Ownership Model"
slug: "negative-keyword-ownership-model"
doc-type: "execution"
type: "guide"
audience: "team"
status: "DRAFT"
level: "L2"
category: "operations"
created: "2026-04-17"
updated: "2026-04-17"
owner: "Richard Williams"
tags: ["negative-keywords", "governance", "cross-market", "slack", "amazon-music"]
depends_on: []
summary: "How negative keyword ownership works across markets, the living Slack pin, and process for surfacing cross-market additions."
---

# Negative Keyword Ownership Model

This guide documents how negative keyword lists are owned, maintained, and updated across paid search markets. The gap that prompted this document is cross-market visibility — we add a negative in one market and the same brand conflict sits live in another for weeks. The pinned Slack list closes that gap.

## Why ownership clarity matters

On April 1, a Spyken search surfaced in an unrelated market's CPC report. The cause was straightforward: that market had not received a negative from the market that first identified the conflict. Brandon surfaced the broader pattern on April 2 — each market maintains its own list with three to five variants, and no mechanism exists to propagate a newly-identified conflict globally.

Amazon Music is the canonical example. If a paid search campaign accidentally bids on "Amazon Music" as a broad or phrase match, we pay CPC for traffic that cannot register for AB. Every market should exclude Amazon Music. Today, not all do.

## Ownership model

Each market's paid search lead owns the negative keyword list for that market. Australia has roughly five variants of the core exclusions plus market-specific additions. Mexico has three. The United States and EU5 have their own. Lists are not synchronized; each lead adds negatives based on their own campaign inspection and the regional retail team's requests.

Cross-market coordination relies on a pinned message in the paid acquisition Slack channel. Any team member who identifies a conflict in their market that likely applies elsewhere posts it to the pin. Other market leads are expected to review the pin weekly and apply relevant additions to their own lists.

## When to add to the global pin

Add to the pinned Slack list when the negative applies in multiple markets. Examples include other Amazon business units (Amazon Music, Amazon Prime Video, Amazon Ads), legacy brand names from acquired companies, competitor brand names that consistently appear in match reports, and Google-surfaced autocomplete terms that drive zero conversion. Do not add to the pin when the negative is market-specific — a local Amazon Music competitor in one country, for example.

## Enforcement

The paid acquisition team lead (Brandon) reviews the pin weekly in the Monday team meeting. Each market lead confirms their list is up to date. Gaps get called out directly.

## When a regional retail team asks for a negative

The regional retail team will occasionally request a specific negative to avoid paid search competing with their paid media. Log the request, apply it, and include a line in the monthly cross-market review confirming the addition. Do not pin these requests unless the conflict is likely to apply in other markets.

## Match type considerations

Expansion markets typically run easy and exact match only. Broad match is rare in expansion markets because it compounds attribution ambiguity. When broad match is in use (primarily US and large EU markets), the negative keyword list grows faster and needs more aggressive curation. The pinned Slack list is particularly valuable for broad-match markets.

## Next Steps

1. Confirm the pinned Slack message exists and is current — Brandon to verify by April 22.
2. Add "Amazon Music" and "Spyken" to the pinned list if not present.
3. Review pinned list in next Monday team meeting and enforce per-market confirmation.

## Related

- [Market Expansion Playbook](market-expansion-playbook)
- [Cross Market Playbook](cross-market-playbook)

<!-- AGENT_CONTEXT
machine_summary: "Negative keyword ownership model: per-market leads own their lists, a pinned Slack message captures cross-market additions. Each market has 3-5 variants. Amazon Music is the canonical example of a cross-market negative that gets missed."
key_entities: ["negative keywords", "pinned Slack list", "Amazon Music", "Spyken", "broad match"]
action_verbs: ["add", "exclude", "pin", "propagate"]
update_triggers: ["new brand conflict surfaces", "broad match expanded to new markets", "regional retail negative request"]
-->
