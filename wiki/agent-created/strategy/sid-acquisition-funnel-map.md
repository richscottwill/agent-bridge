---
title: "AB Acquisition Channel Map — Sid Sundaresan Walkthrough"
slug: "sid-acquisition-funnel-map"
doc-type: "reference"
type: "reference"
audience: "team"
status: "DRAFT"
level: "L2"
category: "strategy"
created: "2026-04-17"
updated: "2026-04-17"
owner: "Richard Williams"
tags: ["acquisition", "channels", "on-site", "email", "push", "ai-search", "sundaresan"]
depends_on: []
summary: "Channel-by-channel map of how Amazon Business acquires new customers, grounded in Sid Sundaresan's 4/9 walkthrough."
---

# AB Acquisition Channel Map

This reference captures how Amazon Business currently acquires new customers, synthesized from Sid Sundaresan's 4/9 channel deep-dive in Austin. Use it to orient new PS team members, cross-functional partners, and anyone who needs a shared vocabulary before discussing channel trade-offs, attribution, or OP1 bets.

## Why this matters

AB has roughly five to six million active accounts worldwide against an estimated 36.2 million addressable businesses. Only 6.9 percent of the AB prospect pool has a large deal relationship today. Acquisition remains the primary growth driver while activation, F90, and lifecycle work expand in parallel. The channels below are how we reach that remaining ninety-plus percent.

## Channel structure

Sid splits AB channels into **on-Amazon** and **off-Amazon** first, then paid versus non-paid:

**On-Amazon (no paid bidding).** On-site placements and email sit on Amazon-owned real estate. There is no auction. Placement and send decisions come from tech and product teams, negotiated annually rather than bid in real time. On-site drives over fifty percent of new registrations, making it the largest single channel by volume.

**On-Amazon paid.** Push notifications on the M-Shop app reach unauthenticated consumer prospects but face three constraints: roughly thirty percent deliverability due to consumer messaging priority, only sixteen to twenty percent of the high-intent audience is eligible under consumer guardrails, and conversion is lower because push creative can confuse users into thinking they are buying retail.

**Off-Amazon paid.** Paid Search (Richard's team), paid media (YouTube, LinkedIn, PV Spotlight, Rokt, ADA), digital display, and live channels (telemarketing, SSR field sales) compete in external auctions. Paid Search accounted for the least registration impact from seasonal on-site lifts historically (about ten percent versus twenty to thirty percent for other channels), suggesting it is comparatively insulated from brand awareness pull.

## On-site placement catalog

Sid highlighted five flagship placements: the sign-in drop-down ("sign up for Amazon Business"), the DPX widget ("Save up to 13% with business pricing" — dynamic based on actual price), the bulk-buy trigger on detail pages when quantity exceeds a category max, the Your Orders "you could have saved X" module, and the AB buy-out tooltip on the cart path. Pion, the new on-site PM, owns roadmap expansion for 2026, with mobile adaptation as the top 2026 priority since ninety percent of consumer traffic is mobile.

## Email and the fatigue problem

Email contribution has declined year over year. Sid attributes it to cadence predictability and crowded inboxes rather than content quality. Personalization happens at the CID level via recently-viewed and related-product modules. The engagement team runs post-registration activation separately; acquisition email focuses on sign-up.

## AI search visibility

Free search content built by the CPS team is increasingly surfacing in Google AI Overviews and ChatGPT. Click-through traffic volume is low. Conversion rates from that traffic are significantly higher than typical organic. No paid placement is available on AI results today — AWS confirmed AI Max sponsored inventory cannot yet be attributed to AI slots.

## Attribution gap

The Rachel/Apache/HEMM multi-touch attribution model has not been implemented despite discussion in multiple WBR cycles. Current attribution gives on-site disproportionate credit. Brand awareness investment is not flowing into the WBR model. This is the single largest analytical blind spot in current acquisition measurement.

## Next Steps

1. Treat this map as the baseline reference — link to it rather than re-explaining channel structure.
2. Open the Rachel/HEMM implementation question with Andrew on the next bi-weekly sync.
3. Flag the AI search conversion rate differential in the next Zero-Click POV refresh.

## Related

- [Agentic PS Vision](agentic-ps-vision)
- [AEO AI Overviews POV](aeo-ai-overviews-pov)
- [F90 Program](f90-program)

<!-- AGENT_CONTEXT
machine_summary: "AB acquisition channels split on-Amazon vs off-Amazon, paid vs non-paid. On-site drives 50%+ of new regs. Email declining, push constrained, AI search high conversion but no paid access. HEMM attribution model unimplemented."
key_entities: ["Sid Sundaresan", "on-site placements", "M-Shop push", "AI Overviews", "HEMM attribution", "Pion"]
action_verbs: ["acquire", "attribute", "bid", "personalize"]
update_triggers: ["new on-site placement launched", "HEMM attribution implemented", "paid AI search inventory opens"]
-->
