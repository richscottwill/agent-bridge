---
title: "Yahoo JP Nonbrand Experiment — Audience Layering"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0390 | duck_id: testing-2022-10-yahoo-jp-nb-experiment -->

---
title: "Yahoo JP Nonbrand Experiment — Audience Layering"
status: DRAFT
audience: amazon-internal
level: L5-L7
owner: Richard Williams
created: 2022-12-21
updated: 2026-03-25
update-trigger: "Yahoo JP NB strategy revisited or audience targeting approach changes"
tags: [experiment, japan, yahoo, nonbrand, audience-targeting, competitor-subdomain]
type: reference
summary: "Yahoo JP NB test (Oct-Dec 2022) layering audiences on nonbrand. Overall $1,457 CPA, but competitor subdomain audience achieved $700 CPA with 2x better efficiency — the headline finding."
---

# Yahoo JP Nonbrand Experiment — Audience Layering

Question: Will layering audiences on Nonbrand help to reduce CPA of NB traffic?
Account: JP Yahoo! account
Timeline: October 16th to December 21st 2022

## Results

Overall: $1,457 CPA. NB didn't perform well overall, but the competitor subdomain audience was the clear winner — $700 CPA with half the overall test's cost per acquisition.

| Audience | Impressions | Clicks | Cost | USD | Conversions | CTR | CPC | CVR | CPA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Competitor | 330,781 | 8,819 | 1,115,199 | $9,691 | 9 | 2.67% | $1.10 | 0.10% | $1,077 |
| Business | 196,704 | 3,463 | 393,383 | $3,419 | 0 | 1.76% | $0.99 | 0.00% | — |
| Total | 527,485 | 12,282 | 1,508,582 | $13,110 | 9 | 2.33% | $1.07 | 0.07% | $1,457 |

### Performance by Audience

**Headline finding: The competitor subdomain audience delivered $700 CPA — half the overall test CPA — with only 1/3 of the traffic.** This was the most efficient audience segment by a wide margin, and the only audience besides broad Competitor that drove any conversions.

| Audience | Impressions | Clicks | Cost | USD | Conversions | CTR | CPC | CVR | CPA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Competitor | 258,338 | 6,834 | 793,055 | $6,892 | 4 | 2.65% | $1.01 | 0.06% | $1,723 |
| Competitor (Subdomain) | 72,443 | 1,985 | 322,144 | $2,799 | 4 | 2.74% | $1.41 | 0.20% | $700 |
| LBC_20M-10B | 53,508 | 999 | 113,185 | $984 | 0 | 1.87% | $0.98 | 0.00% | — |
| LBC_less-than-20M | 21,742 | 422 | 46,793 | $407 | 0 | 1.94% | $0.96 | 0.00% | — |
| LBC_300-10k | 30,066 | 503 | 57,765 | $502 | 0 | 1.67% | $1.00 | 0.00% | — |
| LBC_1 | 40,825 | 775 | 86,091 | $748 | 0 | 1.90% | $0.97 | 0.00% | — |
| Business Panel_2 | 50,563 | 764 | 89,549 | $778 | 0 | 1.51% | $1.02 | 0.00% | — |

**So what:** The subdomain audience (users who visited specific competitor procurement pages like procurement.monotaro.com and solution.soloel.com) had 2x better CPA than the overall test with only 1/3 of the traffic, yet drove an equal share of conversions (4 of 9). All Business-demographic audiences (LBC and Business Panel) produced zero conversions across $3,419 in spend. The signal is clear: targeting users who have demonstrated procurement intent on competitor sites is far more effective than targeting by company size or job function. This finding directly informed the follow-up Google NB test.

## Key Findings

1. **Competitor subdomain targeting works.** The subdomain audience ($700 CPA) outperformed the broad competitor audience ($1,723 CPA) by 2.5x. Users visiting specific procurement subdomains (Monotaro, Soloel) show stronger purchase intent than general competitor site visitors.

2. **Business demographic audiences produced nothing.** All four LBC segments and the Business Panel audience generated zero conversions across $3,419 in combined spend. Company size and job function targeting on Yahoo did not translate to AB registration intent.

3. **ASIN keywords were non-compliant.** We bid on ASIN keywords and didn't negate them, so this test included keywords we wouldn't be able to bid on going forward. The follow-up test was created to bid on compliant terms only.

4. **Overall NB CPA is too high for sustained investment.** $1,457 CPA is not viable at scale, but the subdomain finding suggests a path to efficient NB if audience targeting is refined.

**Connection to follow-up:** The Google NB experiment ([2023-01 JP NB Google](2023-01-jp-nb-experiment-google.md)) was designed to test compliant keywords on Google with learnings from this Yahoo test. The key change: compliant keyword sets only, no ASIN terms.

---

### Appendix: Audiences

**SET 1: Based on Industry Type**

LBC_1: Users employed at companies with fewer than 100 employees

Business Panel_2: Users in any of the below occupations — Materials/Purchasing, General Affairs, Manufacturing/production mgmt/logistics, Delivery/warehouse/logistics, Medical professionals, Office/assistant/receptionist/secretary, Sales (in store and office), Purchase decision makers

Competitor URL Targeting_3: Users who visited any of the below sites — keiei.co, www.telnavi.jp, www.askul.co.jp, nelog.jp, www.monotaro.com, kakaku.com, www.kaunet.com

**SET 2: Based on Company Size (employees and sales volume)**

LBC_300-10,000 employees: Number of employees between 300-10,000

LBC_less than 20 million: Company Sales less than 20 million dollars (annual)

LBC_20M - 10B: Company Sales between 20 million - 10 billion dollars (annual)

**NEW: Competitor (Subdomain)**

Users who visited any of the below subdomains: procurement.monotaro.com, solution.soloel.com/buyer, www.aperza.com, withkaunet.net, benrinet.com, www.kaunetmonika.com, web.incom.co.jp, kensetsu.ipros.jp, ipros.jp, monoist.itmedia.co.jp, www.indexpro.co.jp, www.fa-mart.co.jp, corporate.nc-net.com

<!-- AGENT_CONTEXT
machine_summary: "Yahoo JP nonbrand experiment (Oct-Dec 2022) testing audience layering on NB campaigns. Overall $1,457 CPA across 9 conversions. Headline finding: competitor subdomain audience achieved $700 CPA (2x better) with 1/3 of traffic. All business-demographic audiences produced zero conversions. ASIN keywords were non-compliant and removed for follow-up test."
key_entities: ["Yahoo Japan", "JP NB", "competitor subdomain", "Monotaro", "Soloel", "LBC audiences"]
action_verbs: ["test", "layer", "target", "compare"]
depends_on: []
update_triggers: ["Yahoo JP NB strategy revisited", "Subdomain audience finding acted on", "Follow-up Google NB results available"]
key_facts: ["$1,457 overall CPA", "$700 subdomain audience CPA (2x better)", "9 total conversions, all from Competitor audiences", "Business demographic audiences: 0 conversions across $3,419 spend", "Subdomain had 1/3 traffic but equal conversion share"]
-->
