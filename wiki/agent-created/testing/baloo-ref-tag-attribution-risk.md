---
title: "Baloo Ref Tag Attribution Risk"
slug: "baloo-ref-tag-attribution-risk"
doc-type: "execution"
type: "postmortem"
audience: "team"
status: "DRAFT"
level: "L2"
category: "testing"
created: "2026-04-17"
updated: "2026-04-17"
owner: "Richard Williams"
tags: ["baloo", "attribution", "ref-tag", "paid-search", "tracking", "sharetbz"]
depends_on: ["project-baloo-overview"]
summary: "Ref tags are overwritten during Baloo's registration flow, breaking attribution for any paid campaign that lands on shop.business.amazon.com."
---

# Baloo Ref Tag Attribution Risk

This document captures a production-blocking attribution issue identified during the April 14 Baloo Phase 1 demo. Any paid search campaign that sends traffic to `shop.business.amazon.com` currently loses its Ref tag during the registration flow, which destroys attribution and distorts cost-per-acquisition reporting.

## What we found

During the Baloo Phase 1 walkthrough with Vijay Kumar and the Baloo tech team, Richard tested whether Ref tags persisted from the landing page through authentication. Paid search campaigns carry Ref tags in the URL query string (for example `?ref_=pd_sl_somepath`) that identify the driving placement. These tags should survive the click-through to registration so ABMA can attribute the resulting registration back to the correct campaign.

Testing revealed that Ref tags within the URL query string are being overwritten as users navigate from the Baloo landing page through the authentication flow. The original tag present on arrival is replaced by downstream internal tags before the registration event is captured.

## Why this matters Every paid media dollar spent driving traffic to Baloo is currently unattributable once the user reaches registration. This affects three measurement layers simultaneously: The **WBR attribution model** will show Baloo registrations without the paid search source, making Baloo look more organic than it is. The **campaign-level CPA reporting** that feeds weekly callouts will be wrong on both sides — paid search CPA will be inflated because successful conversions are not credited back, and Baloo's organic CPA will be artificially depressed. The **OP1 2027 planning assumptions** about Baloo's role as a paid search landing page are built on attribution that does not yet work. If Baloo launches publicly with this issue unresolved, every paid acquisition dollar we route through it looks like waste in the reporting even when it converts. ## Scope of impact

The issue affects any campaign using Ref tags — which is every active paid search campaign. It is most acute for campaigns where users click around away from the initial landing page before registering, because those navigation events are where the overwriting appears to happen. Campaigns that drive direct, single-click registrations on the first Baloo page may be less affected.

## Next Steps

1. **Vijay Kumar to review the ticket** — Richard submitted screenshots and a repro case. Owner confirmation requested by April 18.
2. **Baloo SIM must be updated with this risk** — currently overdue on Richard's action list. Update by April 18.
3. **Marketing team to use relative URLs only** — absolute URLs in campaign creative exacerbate the URL flip problem that correlates with the Ref tag loss.
4. **Test repro case once fix ships** — validate that paid search attribution survives the full Baloo-to-registration flow before Baloo goes public.

## Workarounds

None currently. Any paid search spend routed to Baloo should be tagged as "attribution-unreliable" in internal reporting until the fix ships. Consider holding paid search Baloo investment to a minimum test budget until resolution.

## Related

- [Project Baloo Overview](project-baloo-overview)
- [Sid Acquisition Funnel Map](sid-acquisition-funnel-map)

<!-- AGENT_CONTEXT
machine_summary: "Paid search Ref tags are overwritten during Baloo's registration flow, breaking attribution. Identified by Richard 4/14. Ticket submitted to Vijay Kumar. Ongoing risk to paid acquisition attribution for any Baloo-routed campaign."
key_entities: ["Baloo", "Ref tag", "Vijay Kumar", "shop.business.amazon.com", "ABMA attribution", "URL flip"]
action_verbs: ["track", "attribute", "repro", "fix"]
update_triggers: ["ticket resolved", "Baloo goes public", "attribution model updated"]
-->
