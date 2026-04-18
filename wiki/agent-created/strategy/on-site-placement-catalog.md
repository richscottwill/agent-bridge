---
title: "On-Site Placement Catalog — AB Acquisition"
slug: "on-site-placement-catalog"
doc-type: "reference"
type: "reference"
audience: "team"
status: "DRAFT"
level: "L2"
category: "strategy"
created: "2026-04-17"
updated: "2026-04-17"
owner: "Richard Williams"
tags: ["on-site", "acquisition", "cx", "dpx", "bulk-buy", "mobile"]
depends_on: ["sid-acquisition-funnel-map"]
summary: "Reference catalog of on-site placements on Amazon.com that drive AB registrations, with current state and mobile roadmap."
---

# On-Site Placement Catalog

On-site placements on Amazon.com drive over half of all new Amazon Business registrations. Paid search teams compete against the absence of these placements — we pay when users reach us before the on-site team does. Understanding the catalog is prerequisite to any serious CPC defensibility argument or attribution conversation.

## Why this catalog exists

Sid Sundaresan walked the team through on-site placement mechanics on April 9 during the Austin offsite. The content has been reused in multiple follow-up conversations but exists nowhere as a reference document. This page captures his walkthrough and is intended as the canonical reference PS team members link to rather than re-explain.

## Placement categories

On-site placements fall into two categories: untargeted and targeted. Untargeted placements run always-on to the full consumer traffic base, with no ranking logic. Targeted placements apply prospect definitions and conversion-probability logic to show the right placement to the right user at the right time. Targeted placements use dynamic content and personalization at the CID level.

## Flagship placements

**Sign-in drop-down.** The "Sign up for Amazon Business, it's free" link in the account drop-down on every Amazon.com page. Untargeted. High visibility, high conversion rate because intent is clear when a user opens that menu.

**DPX widget.** The "Save up to 13% with business pricing" widget below the buy box on detail pages. Targeted. The savings percentage is dynamic, calculated from the actual retail-versus-business price delta for that ASIN. A personalized variant adds a calculated figure ("you could have saved $238 last year on AB").

**Bulk-buy trigger.** Triggers on detail page when a user selects quantity above the consumer max for eligible B2B ASINs. The placement recognizes the user is exhibiting bulk-purchase intent and surfaces the business buy-out path. Launched 2023.

**Your Orders module.** On the Your Orders page, a module shows "you could have saved X dollars on these orders." Calculated per user from their actual retail purchase history against AB equivalent prices. Highly personalized.

**AB buy-out tooltip.** On the cart path, a tooltip surfaces AB selection and pricing for targeted prospects. Shows on hover over the AB branding. Launched 2023.

## Mobile is the 2026 priority

Roughly ninety percent of consumer traffic is mobile. Most on-site placements were designed desktop-first and have a degraded mobile experience. Pion, the new on-site PM, owns mobile adaptation as the top 2026 investment. Expect iterative experiments on personalization logic, narrowing targeting criteria, and improving conversion among prospects who already see placements at high frequency.

## Who owns what

Product teams, primarily from Consumer and GoatFeeding, negotiate placements with marketing providing requirements. Once launched, placements generally run without central team intervention. Pion is the new PM replacing prior owners. CPS and Traffic teams run parallel campaign flows on some shared placements.

## Implications for paid search

Paid search wins when users arrive at Amazon.com via Google before they see on-site. We lose when on-site converts them first. Two tactical implications: first, budget discussions should account for the fact that on-site registration volume is not attributable to us even when we influence the user's path. Second, brand keywords where users have already seen an on-site placement may be double-counted in attribution. The Rachel/HEMM multi-touch model, unimplemented, is the resolution path.

## Next Steps

1. Treat this catalog as the reference for any on-site conversation with cross-functional partners.
2. Track Pion's mobile placement roadmap via ComopSight planning cycles.
3. Flag attribution double-counting in the next HEMM implementation discussion.

## Related

- [AB Acquisition Channel Map](sid-acquisition-funnel-map)
- [OP1 2027 Innovation Shortlist](op1-2027-innovation-shortlist)

<!-- AGENT_CONTEXT
machine_summary: "On-site placement catalog for AB acquisition. Five flagship placements: sign-in drop-down, DPX widget, bulk-buy trigger, Your Orders savings module, AB buy-out tooltip. Mobile is 2026 priority. Pion owns roadmap."
key_entities: ["Sid Sundaresan", "Pion", "DPX widget", "bulk buy", "Your Orders", "on-site placements"]
action_verbs: ["place", "target", "convert", "mobilize"]
update_triggers: ["new placement launched", "mobile rollout completes", "HEMM attribution implemented"]
-->
