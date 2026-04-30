# GenAI Search Traffic — What We Know and What It Means for PS

---

## The Signal

On April 2, 2026, Yoav (ab-outbound-marketing) shared a critical data point: Amazon's WW marketplaces are seeing approximately 1% of total site traffic and OPS coming from GenAI search engines (ChatGPT, Gemini, etc.). In the US, the traffic is "relatively small" because AB lacks Shopping Ads and Free Product listings — the formats that GenAI engines scrape most effectively. But in international marketplaces where these formats exist, the traffic is measurable and growing.

Separately, Yoav revealed that an internal Amazon team called ACE (led by Ed Banty) is actively negotiating with ChatGPT, Anthropic, and Gemini to build a shopping widget powered by an Amazon MCP (Model Context Protocol). This would allow AI search engines to surface Amazon products directly in their responses — a fundamentally different acquisition channel than traditional search ads.

These two signals — measurable GenAI traffic today, and an Amazon team building the infrastructure for more — change the timeline for the AEO (Answer Engine Optimization) conversation from "2028 strategic positioning" to "2026 operational awareness."

---

## What ChatGPT Does Today

ChatGPT scrapes Google Search results to augment its answers. When a user asks "where can I buy office supplies in bulk for my business," ChatGPT may surface Amazon Business in its response — not because Amazon paid for placement, but because Amazon's organic search presence is strong enough to be scraped.

This means AB is already appearing in GenAI search results, but we have no visibility into it. We don't know which queries trigger AB mentions, how often it happens, or whether the traffic converts. The 1% figure from WW marketplaces is the only data point we have, and it's for consumer Amazon, not AB specifically.

For AB Paid Search, the immediate implication is that some of our "organic" traffic may actually be GenAI-referred. If a user sees AB mentioned in a ChatGPT response, then searches "Amazon Business" on Google and clicks our Brand ad, we attribute that to Brand PS — but the intent was created by GenAI. This attribution gap will grow as GenAI search usage increases.

---

## What ACE Is Building

The ACE team's MCP integration would create a direct channel between AI search engines and Amazon's product catalog. Instead of scraping Google results, ChatGPT/Gemini/Anthropic would query Amazon's catalog directly through a structured API (MCP). This means:

1. Product information would be accurate and current (not scraped from cached search results)
2. Amazon could control which products appear and how they're presented
3. The shopping widget could include pricing, availability, and purchase links
4. Attribution would be trackable — Amazon would know when a purchase originated from a GenAI engine

For AB specifically, this could mean business products appearing in GenAI responses to B2B queries. A user asking "what's the best bulk paper supplier for my office" could see AB products with business pricing directly in the AI response.

---

## What This Means for AB Paid Search

### Short-term (Q2-Q3 2026): Monitor and Measure

The immediate action is measurement. We need to know:
- What percentage of AB traffic comes from GenAI referrals today?
- Which queries trigger AB mentions in GenAI responses?
- Does GenAI-referred traffic convert differently than traditional search traffic?

The measurement gap is the biggest risk. If GenAI traffic is growing and we can't see it, we're making optimization decisions based on incomplete data. The Adobe Ad Cloud reporting segment (already in progress for the email overlay) could potentially be extended to identify GenAI referral patterns.

### Medium-term (Q4 2026 - 2027): Content Optimization

If AB content is being scraped by GenAI engines, the quality and structure of our landing pages matters in a new way. Pages optimized for traditional SEO (keyword density, meta tags) may not be optimal for GenAI extraction (clear answers, structured data, FAQ sections). The Polaris LP migration is an opportunity — new pages is designed with both traditional SEO and GenAI extraction in mind.

### Long-term (2027+): Channel Strategy

If the ACE team's MCP integration launches, GenAI becomes a distinct acquisition channel — not a subset of organic or paid search. AB would need to decide: do we participate in the shopping widget? What's the cost model? How does it interact with our existing Google Ads spend?

This is the Level 4 (Zero-Click Future) conversation. The AEO POV should be updated to reflect these concrete signals rather than relying on industry speculation.

---

## What We Don't Know

- AB-specific GenAI traffic volume (the 1% figure is consumer Amazon WW)
- Whether AB pages are being cited in AI Overviews or ChatGPT responses today
- ACE team's timeline for MCP integration launch
- Whether the shopping widget will be available for B2B products or only consumer
- Cost model for the shopping widget (free? CPC? revenue share?)
- How GenAI traffic interacts with our existing OCI bidding signals

---

## Recommended Actions

1. Ask Mike Babich (Google sync) about AI Overview appearance rates on AB's top 50 NB keywords — this is Action #1 from the AEO POV and now has urgency
2. Connect with Ed Banty's ACE team to understand the MCP shopping widget timeline and whether B2B products are in scope
3. Extend the Adobe Ad Cloud reporting segment to identify GenAI referral patterns in AB traffic
4. Update the AEO POV with these concrete signals — the document currently relies on industry speculation; we now have Amazon-internal data

---

## Sources
- GenAI traffic ~1% of WW marketplace traffic/OPS — source: Slack ab-outbound-marketing, yoavr, 4/2/2026
- ACE team (Ed Banty) MCP integration with ChatGPT/Anthropic/Gemini — source: Slack ab-outbound-marketing, yoavr, 4/2/2026
- ChatGPT scrapes Google Search results — source: Slack ab-outbound-marketing, yoavr, 4/2/2026
- AEO POV existing actions — source: ~/shared/artifacts/strategy/2026-03-25-aeo-ai-overviews-pov.md
- Level 4 (Zero-Click Future) — source: ~/shared/context/body/brain.md → Five Levels → Level 4
- Adobe Ad Cloud reporting segment — source: ~/shared/artifacts/testing/2026-03-25-email-overlay-ww-rollout.md

<!-- AGENT_CONTEXT
machine_summary: "GenAI search engines are driving ~1% of Amazon WW marketplace traffic/OPS today. ACE team (Ed Banty) is building MCP integration with ChatGPT/Anthropic/Gemini for a shopping widget. AB has no visibility into GenAI-referred traffic. Short-term: measure. Medium-term: optimize content for GenAI extraction. Long-term: GenAI becomes a distinct acquisition channel. Updates the AEO POV timeline from '2028 strategic' to '2026 operational awareness.' Four recommended actions: Google sync on AI Overview rates, connect with ACE team, extend Adobe reporting, update AEO POV."
key_entities: ["GenAI", "ACE team", "Ed Banty", "ChatGPT", "Anthropic", "Gemini", "MCP", "AI Overviews", "AEO", "shopping widget"]
action_verbs: ["measure", "connect", "extend", "update", "monitor"]
update_triggers: ["ACE team MCP launch date", "GenAI traffic measurement available", "Google AI Overview data for AB keywords", "AEO POV updated"]
-->
