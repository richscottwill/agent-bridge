---
title: "IT City-Level Bid Modifiers Test"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0394 | duck_id: testing-2024-12-it-bid-modifiers-test -->

---
title: "IT City-Level Bid Modifiers Test"
status: DRAFT
audience: amazon-internal
level: L5-L7
owner: Richard Williams
created: 2024-12-10
updated: 2026-03-25
update-trigger: "Bid modifier strategy rolled to new markets or IT performance data updated"
tags: [experiment, bid-modifiers, italy, google-ads, NB, location-targeting]
type: reference
summary: "Google Ads experiment in Italy showing +18% registrations and +7% CVR from city-level bid modifiers on NB campaigns, with 83.4% Bayesian PPR."
---

# IT City-Level Bid Modifiers Test

## Documents
- Data: 2024.12.10 - IT Location modifiers
- Google doc: City-level cost/revenue data, and bid modifiers

## Experiment
Question: Will adding city-level bid modifiers to our NB campaigns improve performance?

## Setup
- Account: Italy Google Ads
- Timeline: 11/14 to 12/12
- Targeting: 24 largest cities within IT (Google doc above shows individual cities)
- Method: Google Ads experiment (A/B split)

## Results
When manually adding the modifiers at the city level, with the help of Google, we saw +18% registrations and +7% CVR.

Adding the bid modifiers allowed for location bid adjustments in areas that otherwise would not have been touched by Adobe Ad Cloud. The change allowed for more spend in cities where users sign up for AB, resulting in higher volume of impressions and clicks. Little effect on CPA because bids were pushed up 9%. The volume increase in clicks/registrations alone is valuable, but the CVR increase adds further evidence.

| Metric | City + Modifiers | Italy-Only Targeting | Difference |
| --- | --- | --- | --- |
| Impressions | 32,451 | 26,731 | +21% |
| Clicks | 6,760 | 6,141 | +10% |
| Cost | $37,586 | $31,320 | +20% |
| Registrations | 383 | 324 | +18% |
| CTR | 21% | 23% | -9% |
| CPC | $5.56 | $5.10 | +9% |
| CVR | 5.70% | 5.30% | +7% |
| CPA | $98 | $97 | +2% |

**So what:** City-level bid modifiers are a validated lever for volume growth without CPA degradation. The +18% registration lift at essentially flat CPA ($98 vs $97) means we can drive meaningful incremental volume by directing spend toward high-converting cities. The 83.4% Bayesian PPR exceeds Amazon's 66% Weblab threshold, giving high confidence this is a real effect, not noise.

| Bayesian PPR (probability of positive return) |
| --- |
| 83.40% |

*Amazon uses 66% for Weblab testing when evaluating experiments with Bayesian criteria.

## What Happened After

<!-- TODO: Did IT adopt city-level bid modifiers permanently? Was this approach rolled out to other markets (AU, MX, etc.)? Add outcome context when available. -->

<!-- AGENT_CONTEXT
machine_summary: "Google Ads A/B experiment in Italy (Nov-Dec 2024) testing city-level bid modifiers on NB campaigns. Results: +18% registrations, +7% CVR, +2% CPA (essentially flat). Bayesian PPR of 83.4% exceeds Amazon's 66% threshold. Validates location-level bid optimization as a volume growth lever."
key_entities: ["Italy", "Google Ads", "Adobe Ad Cloud", "NB campaigns", "bid modifiers"]
action_verbs: ["test", "validate", "optimize", "scale"]
depends_on: []
update_triggers: ["Bid modifier strategy adopted permanently in IT", "Strategy rolled to other markets", "Follow-up test with refined city list"]
key_facts: ["+18% registrations with city-level modifiers", "+7% CVR improvement", "83.4% Bayesian PPR (above 66% threshold)", "24 largest Italian cities targeted", "CPA essentially flat: $98 vs $97"]
-->
