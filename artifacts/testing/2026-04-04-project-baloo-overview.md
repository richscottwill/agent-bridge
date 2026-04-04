---
title: Project Baloo - Shopping Ads for Amazon Business
status: DRAFT
doc-type: strategy
audience: amazon-internal
level: 2
owner: Richard Williams
created: 2026-04-04
updated: 2026-04-04
update-trigger: early access data available, cost guardrails finalized, full test decision, Google updates
tags: baloo, shopping-ads, google, us, new-channel
---

# Project Baloo - Shopping Ads for Amazon Business

> Overview of Project Baloo (Shopping Ads for AB), early access status, cost implications, and decision framework for full test. Designed for Brandon's awareness and team planning.

---

## What Baloo Is

Project Baloo brings Google Shopping Ads to Amazon Business for the first time. Shopping Ads are the product-image-based ads that appear at the top of Google search results — the visual product cards with price, image, and merchant name. Until now, AB Paid Search has been limited to text ads only. Shopping Ads are a fundamentally different ad format that reaches users at a different point in the purchase journey.

For context: Shopping Ads account for roughly 60-65% of all Google Ads clicks in retail e-commerce. AB has been competing with one hand tied behind its back — text ads only, while competitors (including consumer Amazon) use both text and Shopping. Baloo removes that constraint.

The name "Baloo" is the internal project codename. The underlying Google product is Google Merchant Center + Shopping Campaigns, adapted for AB's B2B catalog.

---

## Why It Matters

### 1. New Channel, Not Just New Format

Shopping Ads reach users that text ads miss. A user searching "office chairs" sees Shopping Ads with product images, prices, and ratings before they see text ads. If AB is not in Shopping results, we are invisible to users who shop visually — and visual shopping behavior is increasing, especially on mobile.

This is not incremental optimization of existing campaigns. It is a new acquisition channel that expands the total addressable audience for AB Paid Search.

### 2. Competitive Parity

Consumer Amazon already runs Shopping Ads. Walmart, Staples, and other B2B competitors run Shopping Ads. AB's absence from Shopping results means we are ceding the most prominent ad placement on Google to competitors. Baloo closes that gap.

### 3. Higher Intent Signal

Shopping Ads show product-level information (image, price, availability) before the click. Users who click a Shopping Ad have already seen the product and price — they are further down the purchase funnel than text ad clickers. This should translate to higher CVR and lower CPA compared to generic NB text ads, though this hypothesis needs validation.

---

## Current Status

| Milestone | Status | Date | Notes |
|-----------|--------|------|-------|
| Early access program | LAUNCHED | 3/30/2026 | 60+ users onboarding through PS flow (Aayushi, Baloo PM) |
| Keywords delivered | COMPLETE | 3/30/2026 | Richard filtered for high-intent product terms, shared via Quip |
| PS flow validation | COMPLETE | 3/18/2026 | ps_kw parameter passthrough confirmed working |
| Cost guardrails | IN PROGRESS | TBD | Vijay 1:1 (3/26) discussed cost planning |
| Product feed setup | PENDING | TBD | Google Merchant Center configuration |
| Full test launch | NOT STARTED | EO Aug 2026 target | Brandon confirmed: "tested against PS US traffic by EO Aug" |

Brandon's message to the team (4/3): "PS team [Stacey, Richard, Adi especially], please look at the experience since this will be tested against PS US traffic by EO Aug." This gives a hard deadline and confirms the test scope is US PS traffic specifically.

Early access launched on 3/30 with a Tampermonkey browser extension. Aayushi (Baloo PM) confirmed 60+ users will onboard through the PS flow. Richard created a separate Quip sheet with filtered keywords (high impressions/clicks/conversions, low CPC, product terms only — removed dropship, business cards, and B2B-adjacent terms like "cheap t shirts bulk").

Key technical detail: the `ps_kw` (paid search keyword) parameter passthrough was initially broken when redirecting to the Baloo subdomain (shop.business.amazon.com). This was identified on 3/17 and resolved by 3/18 — Aayushi confirmed end-to-end flow validation works.

---

## Cost Considerations

Shopping Ads have a different cost structure than text ads. Key differences:

| Factor | Text Ads (Current) | Shopping Ads (Baloo) |
|--------|-------------------|---------------------|
| Bidding unit | Keyword-level CPC | Product-level CPC |
| CPC range | $1-7 (varies by market) | TBD (expected lower per click, higher volume) |
| Conversion path | Click -> LP -> Registration | Click -> Product page -> Registration (longer path) |
| Budget model | Campaign-level daily budget | Campaign-level, but volume can scale quickly |
| Measurement | Registration CPA | Registration CPA + product engagement metrics |

The cost guardrail discussion with Vijay (3/26) focused on three questions:

1. **What is the maximum acceptable CPA for Shopping Ads?** Should it match NB text ad CPA, or is a premium acceptable for the new channel?
2. **How do we prevent budget runaway?** Shopping Ads can scale volume quickly. Daily budget caps and CPA targets need to be set before launch.
3. **How do we attribute Shopping Ad registrations?** The conversion path is different (product page vs. registration LP). Tracking needs to capture the full funnel.

These questions are not yet answered. Cost guardrails must be finalized before any live spend occurs.

---

## Test Design (Proposed — Pending Cost Guardrail Finalization)

Following the OCI playbook (phased rollout with measurement). These parameters are proposals, not finalized — they require Google sync and cost guardrail agreement before launch.

### Phase 1: Limited Product Set (4 weeks)

| Parameter | Value |
|-----------|-------|
| Market | US only |
| Product scope | Top 50 products by search volume |
| Budget | $5K-10K/week (capped) |
| Bidding | Manual CPC (conservative, learn first) |
| Primary metric | Registrations from Shopping Ad clicks |
| Secondary metrics | CPA, CTR, product page engagement, CVR |
| Guardrail | CPA must not exceed 150% of NB text ad CPA |

The 150% CPA guardrail is deliberately looser than OCI's 110% because Shopping Ads are a new channel with unknown conversion dynamics. The first phase is about learning, not efficiency.

### Phase 2: Expanded Product Set (4 weeks)

If Phase 1 shows positive registration signal:
- Expand to top 200 products
- Increase budget to $15-25K/week
- Tighten CPA guardrail to 120% of NB text ad CPA
- Introduce Smart Bidding (if manual CPC data supports it)

### Phase 3: Full Catalog + OCI Integration

If Phase 2 validates:
- Full product catalog in Shopping
- OCI integration (Shopping Ads optimizing for registrations, not just clicks)
- Budget scaled based on CPA performance
- Plan international rollout (UK/DE first)

---

## Open Questions

| Question | Owner | Status | Impact |
|----------|-------|--------|--------|
| What CPA threshold is acceptable for Shopping Ads? | Richard/Brandon | Open | Determines budget and go/no-go |
| Can OCI work with Shopping Ads? | Richard/Mike Babich | Open | Determines Phase 3 viability |
| How does Shopping Ad attribution work for registrations? | Richard/Vijay | Open | Determines measurement framework |
| Who owns Baloo long-term? | Brandon | Open | Richard is evaluating, but long-term ownership TBD |
| Does Baloo conflict with consumer Amazon Shopping Ads? | Richard | Open | Internal coordination question |

The consumer Amazon conflict question is important. If consumer Amazon already runs Shopping Ads for the same products, AB Shopping Ads could compete with ourselves in the auction. This needs to be investigated before full launch.

---

## What Brandon Needs to Know

1. **No spend is happening yet.** Early access is a preview tool, not a live campaign. No budget impact until cost guardrails are finalized and a test is launched.

2. **This is a new channel, not an optimization.** Shopping Ads expand the team's reach into a format we have never used. The learning curve is real — expect 4-8 weeks before we have meaningful data.

3. **Cost guardrails are the gate.** The test will not launch until CPA thresholds, budget caps, and attribution methodology are agreed upon. Richard and Vijay are working on this.

4. **Long-term ownership is a team decision.** Baloo could sit with Stacey (US lead), Richard (testing methodology), or a new owner. Brandon should weigh in on ownership before the test launches.

5. **International rollout is Phase 3 at earliest.** UK/DE would be first international markets if US validates. No international planning needed yet.

---

## Sources
- Baloo early access launched 3/30 — source: ~/shared/context/body/eyes.md -> What's Coming
- Vijay 1:1 cost planning (3/26) — source: ~/shared/context/body/memory.md -> Vijay Kumar
- Keywords delivered — source: ~/shared/context/body/eyes.md -> What's Coming
- Shopping Ads market share (60-65% of retail clicks) — source: industry knowledge, Google Ads documentation
- OCI test methodology as template — source: ~/shared/context/body/brain.md -> D1: OCI Implementation Approach
- Consumer Amazon Shopping Ads conflict — source: ~/shared/context/active/org-chart.md -> Amazon Retail Central Paid Search
- Tampermonkey extension (50 stakeholders) — source: ~/shared/context/body/memory.md -> Vijay Kumar

<!-- AGENT_CONTEXT
machine_summary: "Overview of Project Baloo — Shopping Ads for Amazon Business. Early access launched 3/30 (preview only, no spend). Shopping Ads are a new channel (not optimization) that reaches users AB text ads miss. Cost guardrails not yet finalized — CPA threshold, budget caps, and attribution methodology are open questions. Proposed 3-phase test: limited products (US, $5-10K/wk) -> expanded catalog -> full catalog + OCI. Consumer Amazon Shopping Ads conflict needs investigation. Long-term ownership TBD."
key_entities: ["Baloo", "Shopping Ads", "Google Merchant Center", "Vijay Kumar", "Mike Babich", "US", "OCI", "Tampermonkey"]
action_verbs: ["evaluate", "test", "guard", "attribute", "scale"]
update_triggers: ["early access data available", "cost guardrails finalized", "full test decision", "Google updates", "consumer Amazon conflict resolved"]
-->
