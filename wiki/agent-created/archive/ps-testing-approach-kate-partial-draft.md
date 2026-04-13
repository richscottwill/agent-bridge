---
title: "Paid Search Testing Approach & Year Ahead"
status: archived
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0140 | duck_id: context-ps-testing-approach-kate-partial-draft -->

---
title: "Paid Search Testing Approach & Year Ahead"
slug: "ps-testing-approach-kate"
type: "playbook"
audience: "org"
status: "draft"
created: "2026-03-25"
updated: "2026-03-25"
owner: "Richard Williams"
tags: ["testing", "strategy", "OP1", "paid-search", "kate-doc"]
depends_on: []
consumed_by: ["wiki-concierge", "rw-trainer"]
summary: "PS testing methodology, 2025 validated results, 2026 investment roadmap, and cross-functional scope for Kate Rundell review."
---

# Paid Search Testing Approach & Year Ahead

This document establishes the Paid Search team's testing methodology and 2026 investment roadmap for Kate Rundell's April 16 review. Every 2026 initiative maps to a validated 2025 result. The team is transforming Paid Search from a keyword-driven acquisition channel into an automated, audience-centric engine that drives incremental growth at scale, grounded in evidence rather than speculation.

Each section below covers one workstream: what we tested, what we learned, and how the validated results directly inform 2026 investment. Each initiative required cross-functional collaboration spanning Legal, Data Science, MarTech, MCS, ABMA, Customer Research, and international market teams, with the PS team serving as the connective tissue between platform capabilities and business objectives.

## How We Test

The PS team follows a consistent methodology across all workstreams: identify a problem, design a controlled test, validate the result, then scale what works.

The methodology has four stages:

1. Hypothesis and baseline. Every test starts with a measurable claim. We establish baselines using prior-quarter data with seasonality adjustments so we can isolate the effect of the change from background noise.

2. Phased rollout. We do not make big-bang changes. OCI launched at the keyword level (E2E testing), scaled to 25% of campaigns, then 50%, then 100%. Each phase has a measurement window and a go/no-go decision. This approach was validated in the US and has become the standard playbook for every subsequent market.

3. Measurement framework. We compare actualized performance against the seasonality-adjusted baseline, not against raw prior-period numbers. For OCI, this means comparing post-OCI CPA against what CPA would have been without OCI, accounting for seasonal registration patterns. For ad copy, we run test/control splits with sufficient volume to reach statistical confidence. For landing pages, we use pre/post causal analysis and Weblab (APT) where available.

4. Scale or stop. If a test validates, we scale it. If it does not, we document the learning and move on. The Gated Guest experiment showed -61% registrations after 4 weeks. We paused it, deep-dived the data, and pivoted to in-context registration, which delivered +13.6K annualized incremental registrations with 100% probability (APT). Failures are data, not setbacks.

This methodology is not unique to Paid Search. It is the same discipline used across Amazon's experimentation culture. What is distinctive is how the PS team applies it across five concurrent workstreams while serving as the connective tissue between platform capabilities (Google, Adobe, MarTech) and business objectives (registrations, OPS, customer lifecycle).

## Workstream 1: Intelligent Bidding (OCI)

Progression: Loss of Google Ads auto-bid strategy and Adobe → OCI success and expansion

To launch OCI bidding, accurate tracking of campaign traffic and conversions was required. The Paid Search team partnered with the MarTech team to implement OCI as the first non-retail business unit at Amazon, requiring significant cross-team collaboration and operational effort. The team worked closely with Legal, the MarTech team, and the Data Science team to enable the rollout. This included defining the OCI value framework, ensuring the appropriate tracking and account structure were set up correctly, and validating the underlying data to support accurate optimization.

To ensure a disciplined rollout, the team established a phased implementation and measurement plan, beginning with E2E keyword-level testing, scaling through 25%, 50%, and 100% campaign-level application, to evaluate performance lift and guide ongoing optimization. As part of this effort, the team also analyzed the relationship between ROAS targets and CPA performance to ensure the appropriate tROAS settings were applied during the transition. The measurement framework, which compares actualized CPA against a baseline built from prior-quarter data with seasonality adjustments, has since become the standard approach for each new market rollout.
