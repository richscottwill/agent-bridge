---
title: "Paid App Attribution — Acquisition vs Engagement Debate"
slug: "paid-app-attribution-debate"
doc-type: "strategy"
type: "decision"
audience: "leadership"
status: "DRAFT"
level: "L2"
category: "testing"
created: "2026-04-17"
updated: "2026-04-17"
owner: "Richard Williams"
tags: ["paid-app", "attribution", "budget", "ssr", "engagement", "deep-link", "ref-tag"]
depends_on: []
summary: "If 80% of paid app install traffic is existing customers, the budget belongs with engagement, not SSR. Deep-link test proposal."
---

# Paid App Attribution Debate

Paid search teams pay for app installs from the SSR acquisition budget. The prevailing hypothesis, raised during the April 8 OP1 workshop, is that approximately eighty percent of that install traffic is existing customers re-engaging, not new acquisitions. If true, the budget belongs with Christine's engagement team, not SSR. This document outlines the debate, the test we need to resolve it, and the budget implications.

## Current state

Paid app marketing currently runs through Google and Apple ads, with installs as the primary tracked event. Attribution jumps from install to registration, but we do not cleanly split new customers from existing customers at the install event. The acquisition team's WBR line shows paid app installs, implying acquisition credit, but Peter Ocampo's aggregate data suggests the majority of installs are current customers.

The logic is intuitive: far fewer net-new prospects download a business app than existing customers who already have a workflow need. Paid media amplifies both, and acquisition ad creative catches existing customers as readily as prospects.

## The 80/20 hypothesis

If the split is eighty percent engagement and twenty percent acquisition, three things follow. First, paid search's SSR-funded CPA for paid app is systematically understated because eighty percent of the "conversions" were never acquisitions to begin with. Second, Christine's engagement team gets lifetime-value credit for users they are not paying for. Third, the budget is misallocated. Even accounting for the value of bringing existing customers onto the app (higher OPS, more push reach), the funding source should match the user type.

## Why a deep-link test resolves it

A deep-link paid app campaign with persistent Ref tags would separate acquisition from engagement cleanly. Richard proposed the test: set up a dedicated paid app campaign, add a deep link with a Ref tag (for example `PDSL_something`), route clicks through to Ruby's saving sky page or an equivalent acquisition-focused destination, and measure registrations against installs.

The deep link preserves attribution context through the app, which is the current gap. The Ref tag survives the transition from Google Ads click to in-app page, which means we can pull the IRF data and see whether the user was already signed in as an AB customer or was net-new.

## Budget implications

The 2026 SSR budget reserved roughly $1M for paid app. If eighty percent of that traffic is engagement, $800K is effectively an engagement investment. Christine's team has surplus budget this year; SSR is stingy. The reallocation is politically difficult but analytically justified.

A successful deep-link test unlocks the budget conversation. It also unlocks a secondary optimization: engagement-specific ad creative targeting users who already have the AB app installed, enabled by the LiveRamp MCC-level audience work already in progress.

## Risks

Two risks matter. First, the deep-link test itself may leak traffic attribution if the IRF data cannot distinguish new from existing customers cleanly. Second, any budget reallocation is politically loaded; expect pushback from SSR even if the data is definitive.

## Next Steps

1. Design deep-link test with Andrew and Peter by April 30.
2. Confirm Ref tag persistence through Google Ads click to app registration with tech.
3. Document current paid app budget attribution baseline for the April 30 Flash input.

## Related

- [OP1 2027 Innovation Shortlist](op1-2027-innovation-shortlist)
- [LiveRamp Program](../research/liveramp-program)

<!-- AGENT_CONTEXT
machine_summary: "Paid app install traffic likely 80% existing customers, 20% new acquisition. Deep-link Ref tag test proposed to verify split. If confirmed, $800K of SSR budget belongs with Christine's engagement team."
key_entities: ["paid app", "SSR budget", "Christine's engagement team", "deep link", "Ref tag", "Peter Ocampo"]
action_verbs: ["attribute", "deep-link", "reallocate", "test"]
update_triggers: ["deep-link test results", "budget reallocation decision", "engagement team accepts ownership"]
-->
