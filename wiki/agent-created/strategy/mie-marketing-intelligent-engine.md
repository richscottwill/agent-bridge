---
title: "MIE — Marketing Intelligent Engine"
slug: "mie-marketing-intelligent-engine"
doc-type: "reference"
type: "reference"
audience: "team"
status: "DRAFT"
level: "L3"
category: "strategy"
created: "2026-04-17"
updated: "2026-04-17"
owner: "Richard Williams"
tags: ["mie", "ai", "bid-strategy", "adobe", "genbi", "tech-roadmap"]
depends_on: []
summary: "Tech-built AI tool specifically for paid search with bid and portfolio recommendations, expected 2027. Potential Adobe replacement."
---

# MIE — Marketing Intelligent Engine

MIE is an AI tool in development by the tech team, built specifically for Amazon Business paid search. If it ships as scoped, it will be the single largest change to PS execution in five years. Early documentation positions the PS team to shape requirements rather than inherit a finished product.

## What MIE does

MIE provides bid and portfolio recommendations at the campaign level, informed by AB-specific goals and historical performance. Unlike generic AI tools or GENBI dashboards, MIE understands paid search optimization logic. It can say "change this bid strategy to this setting" rather than "conversion rate dropped on this landing page." It connects the what to the why and the so-what.

Key distinction from existing tools: MIE does not auto-execute. The team reviews recommendations and implements changes manually. This is a deliberate design choice that preserves human judgment on high-consequence changes.

## Why this matters

Three implications stand out. First, MIE reduces Adobe dependency. A large portion of Adobe's current value is reporting and automated bid adjustment. If MIE handles both within an AB-specific context, the Adobe license cost becomes a candidate for reduction, particularly for smaller markets and engagement campaigns where Adobe's registration-focused optimization does not apply.

Second, MIE increases testing velocity. The bottleneck today is not idea generation but implementation speed. MIE can surface dozens of testable hypotheses per week, most of which the team would not have identified manually.

Third, MIE changes the team's time allocation. Less time on data pulls and trend identification, more time on test design, campaign architecture, and stakeholder communication. The skill set that compounds shifts toward strategic judgment.

## Current scope

From the OP1 workshop discussion with Joel, MIE will look at campaign and portfolio-level data, produce recommendations, and show the reasoning. It is paid-search-specific at launch. Expansion to other channels is theoretically possible but unlikely before 2028.

Data inputs include Google Ads performance, Adobe metrics where still in use, and internal AB data through the existing tech pipeline. Output is a recommendation queue the PS team works through on a cadence to be defined.

## Risks and unknowns

The first risk is access timing. Tech has not committed a ship date. Expect 2027 at earliest. The second is recommendation quality — if MIE produces too many low-value recommendations, the team will stop using it regardless of capability. The third is job-security adjacency. The tool is designed to augment, not replace, but team members worry about the framing. Proactive Brandon-level messaging will matter.

## What to watch

Watch three signals. First, whether MIE's data replication latency narrows below the current two-to-three day lag. Real-time anomaly detection requires near-real-time data. Second, whether natural language querying ships in v1 or is deferred. NL querying dramatically lowers the adoption barrier. Third, whether MIE remains paid-search-only or expands to Engagement campaigns — the broader the scope, the larger the Adobe replacement opportunity.

## Next Steps

1. Request Joel's current MIE roadmap and share with the team by April 30.
2. Identify three PS-specific use cases MIE should nail in v1 and document them.
3. Track MIE status in the weekly team sync starting week 17.

## Related

- [Agent Architecture](agent-architecture)
- [Agentic PS Vision](agentic-ps-vision)
- [OP1 2027 Innovation Shortlist](op1-2027-innovation-shortlist)

<!-- AGENT_CONTEXT
machine_summary: "MIE is a tech-built AI tool specifically for paid search. Provides bid and portfolio recommendations at campaign level. Does not auto-execute. Potential Adobe replacement. Expected 2027. Paid-search-specific at launch."
key_entities: ["MIE", "Joel", "Adobe replacement", "GENBI", "bid recommendations"]
action_verbs: ["recommend", "optimize", "review", "implement"]
update_triggers: ["MIE roadmap shared", "tech commits ship date", "Adobe contract renewal"]
-->
