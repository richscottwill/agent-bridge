---
audience: amazon-internal
creator: Richard Williams
doc_type: document
last_modified: '2025-11-18'
mirror_date: '2026-04-10'
owner: Richard Williams
quip_folder: Planning/OCI
quip_id: dSZ9AAZBXQy
source_url: https://quip-amazon.com/dSZ9AAZBXQy
status: DRAFT
title: OCI Planning - Phased Rollout
topics:
- OCI
- rollout
- US
- UK
- DE
- phased testing
- ROAS
- bid strategy
- tracking template
backfill_status: backfilled
---

# OCI Planning - Phased Rollout
## Tracking Template Changes
* URL Construction: https://na.amazon-value-service.com/cl/v1/p/BSQ1ZjkFy2M2q-R5Vhq2HzSs5l2d8ndQPn0KMtF79_ieEA?lp={lpurl}&vscl={gclid}&vsco={gbraid}
 * Portfolio Tag |
* Suffix Construction: hvocijid={random}-{extensionid}&hvexpln=ssrText&ps_kw={keyword}&tag=abpsgglacqus-20
 * OCI pieces | powers Guest AB-shopping searches | Associate Tag
 * **ps_kw= THIS IS NOT SUPPORTED BY OCI! DO NOT USE**
* URL Details:
 * Portfolio tag (long string in URL) available here: [Link][1]
  * Note that each Market has a unique Portfolio tag

### **Application**
* 6/26: **25% Rollout**
 * Apply OCI TT and Suffix (found in next section) to selected 25% campaigns
  * US [is here][2] | UK [is here][3] <ignore, these were for 10%
   * US can also be found by filtering campaign label contains 'OCI TT Phase 1’
   * campaign list here: [https://docs.google.com/spreadsheets/d/1gN\_CMeUvgxI2NvxZ4DVqBt\_5Ul7pv8zoquJG9oJalxY/edit?gid=1773547684#gid=1773547684][4]
  * Suffix will not include ps_kw (this change is reflected in below OCI TT/Suffix instructions
 * If reverting, TT and Suffix should be deleted from 25% campaigns
* Change Plan: 25% (campaign) > 50% (campaign) > 100% (remove campaign TT/suffix, add account level)
 * 2 day ETA for complete rollout
### US Tracking Template
US OCI

TT:
[https://na.amazon-value-service.com/cl/v1/p/BSQ1ZjkFy2M2q-R5Vhq2HzSs5l2d8ndQPn0KMtF79\_ieEA?lp={lpurl}&vscl={gclid}&vsco={gbraid][5]}

Orig Used:
[https://eu.amazon-value-service.com/cl/v1/p/BSQ1ZjkFy2M2q-R5Vhq2HzSs5l2Y8nxEPn0KMtF79\_ieEA?lp={lpurl}&vscl={gclid}&vsco={gbraid}][6]

Suffix:  hvocijid={random}-{extensionid}&hvexpln=ssrText&tag=abpsgglacqus-20

*to add ps_kw and s_kwcid to Suffix later, once OCI is verified
* &ps_kw={keyword}
To test on ps_kw={keyword} in US for final url suffix:
hvocijid={random}-{extensionid}&hvexpln=ssrText&ps_kw={keyword}&tag=abpsgglacqus-20

US Adobe
TT: [https://pixel.everesttech.net/9012/cq?ev\_sid=3&ev\_ln={keyword}&ev\_lx={targetid}&ev\_crx={creative}&ev\_mt={matchtype}&ev\_n={network}&ev\_ltx={\_evltx}&ev\_pl={placement}&ev\_pos={adposition}&ev\_dvc={device}&ev\_dvm={devicemodel}&ev\_phy={loc\_physical\_ms}&ev\_loc={loc\_interest\_ms}&ev\_cx={campaignid}&ev\_ax={adgroupid}&ev\_efid={gclid}:G:s&url={lpurl][7]}
Suffix:  ef_id={gclid}:G:s&s_kwcid=AL!9012!3!{creative}!{matchtype}!{placement}!{network}!{product_partition_id}!{keyword}!{campaignid}!{adgroupid}&ps_kw={keyword}&tag=abpsgglacqus-20

### UK Tracking Template
UK OCI <The one we’re testing
TT: [https://eu.amazon-value-service.com/cl/v1/p/BSQ1ZjkFy2M2q-R5Vhq2HzSs5l2f8nxEPn0KMtF79\_ieEA?lp={lpurl}&vscl={gclid}&vsco={gbraid][8]}

Suffix:  hvocijid={random}-{extensionid}&hvexpln=ssrText&tag=abpsgglacquk-21

*to add ps_kw and s_kwcid to Suffix later, once OCI is verified
* &ps_kw={keyword}

UK Adobe
TT: [https://pixel.everesttech.net/9012/cq?ev\_sid=3&ev\_ln={keyword}&ev\_lx={targetid}&ev\_crx={creative}&ev\_mt={matchtype}&ev\_n={network}&ev\_ltx={\_evltx}&ev\_pl={placement}&ev\_pos={adposition}&ev\_dvc={device}&ev\_dvm={devicemodel}&ev\_phy={loc\_physical\_ms}&ev\_loc={loc\_interest\_ms}&ev\_cx={campaignid}&ev\_ax={adgroupid}&ev\_efid={gclid}:G:s&url={lpurl][7]}
Suffix:  ef_id={gclid}:G:s&s_kwcid=AL!9012!3!{creative}!{matchtype}!{placement}!{network}!{product_partition_id}!{keyword}!{campaignid}!{adgroupid}&ps_kw={keyword}&tag=abpsgglacquk-21

## Traffic dial up
### US File:
* campaigns count 10% of traffic list in this file, [US 10% traffic campaign list.xlsx][9]
* also can filter campaign label contains ‘OCI TT Phase 1’

### DE Tracking Template
DE: <The one we’re testing - wait on tech confirm correct to use
Final URL suffix:
hvocijid={random}-{extensionid}&hvexpln=ssrText&tag=abpsgglacqde-21

Tracking template:
 * `https://eu.amazon-value-service.com/cl/v1/p/BSQ1ZjkFy2M2q-R5Vhq2HzSs5l2Y8nxEPn0KMtF79\_ieEA?lp={lpurl}&vscl={gclid}&vsco={gbraid}`

## US OCI Planning
***AB PS team internal use, do NOT share w/ AB tech team or Retail team. **

* **\*\*RW/AW & SG **to pull Reg penetration per phase. Pull based on Feb/Mar (US), add per phase flighting (DE/UK)
* **AW** to create spreadsheet feed for tracking: [Untitled][10]
 * To review during DDD May 8
 * Will need to update reg col once Adobe feed has changed.

### Planning Timeline
||A|B|C|D|E|F|G|H|
|---|---|---|---|---|---|---|---|---|
|1|Portfolio  Rollout Timeline|​|​|​|​|​|​|​|
|2|US|​|Data Gathering|Phase 1|Phase 2|Phase 3|Phase 4|Perf Monitor|
|3|Action Items|Duration|7/1/2025|7/28/2025|9/1/2025|9/29/2025|10/20/2025|10/27/2025|
|4|Data gathering Phase|4 weeks|​|​|​|​|​|​|
|5|NB Phase 1: 23% of NB spend to TROAS|2 days|​|​|​|​|​|​|
|6|NB Phase 1 performance monitoring|4 weeks|​|​|​|​|​|​|
|7|NB Phase 2: 26% of NB spend to TROAS (Cum: 49%)|2 days|​|​|​|​|​|​|
|8|NB Phase 2 performance monitoring|4 weeks|​|​|​|​|​|​|
|9|NB Phase 3: 23% of NB spend to TROAS (Cum: 72%)|2 days|​|​|​|​|​|​|
|10|NB Phase 3 performance monitoring|3 weeks|​|​|​|​|​|​|
|11|Brand Phase 1: 50% of Brand plus spend to TROAS|2 days|​|​|​|​|​|​|
|12|Brand Phase 1 performance monitoring|3 weeks|​|​|​|​|​|​|
|13|NB Phase 4: 29% of NB spend to TROAS (Cum: 100%)|2 days|​|​|​|​|​|​|
|14|Brand Phase 2: 50% of Brand plus spend to TROAS (Cum 100%)|2 days|​|​|​|​|​|​|
|15|Account level performance monitoring|2 weeks|​|​|​|​|​|​|

||A|B|C|D|E|F|G|
|---|---|---|---|---|---|---|---|
|1|Non  Brand Bidding Portfolio|spend pene|Note|Phase 1|Phase 2|Phase 3|Phase 4|
|2|US - BAU - [G]|12%|Group B|12%|​|​|​|
|3|US - BAU - C - [G]|12%|Group A|​|​|12%|​|
|4|US - AVT_S & L - [G]|11%|Group B|11%|​|​|​|
|5|US - AVT_S & L - C - [G]|11%|Group A|​|​|11%|​|
|6|US - Non AVT_B- [G]|18%|Group B|​|18%|​|​|
|7|US - Non AVT_B - C - [G]|18%|Group A|​|​|​|18%|
|8|US - AVT_B - [G]|8%|Group B|​|8%|​|​|
|9|US - AVT_B - C - [G]|8%|Group A|​|​|​|8%|
|10|US - AVT_All - [G]|3%|​|​|​|​|3%|
|11|TTL NB|100%|​|​|​|​|​|
|12|Accumulative spend Pene per  phase|​|​|23%|49%|72%|100%|
|13|Number of Wks|​|​|4|4|3|3|
|14|​|​|​|​|​|​|​|
|15|Brand Bidding Portfolio|spend pene|​|Phase 1|Phase 2|Phase 3|Phase 4|
|16|Brand Core BMM|50%|​|​|​|50%|​|
|17|Brand Plus|50%|​|​|​|​|50%|

||A|B|C|D|E|F|G|
|---|---|---|---|---|---|---|---|
|1|Non  Brand Bidding Portfolio|reg pene|Note|Phase 1|Phase 2|Phase 3|Phase 4|
|2|US - BAU - [G]|11%|Group B|11%|​|​|​|
|3|US - BAU - C - [G]|11%|Group A|​|​|11%|​|
|4|US - AVT_S & L - [G]|12%|Group B|12%|​|​|​|
|5|US - AVT_S & L - C - [G]|12%|Group A|​|​|12%|​|
|6|US - Non AVT_B- [G]|15%|Group B|​|15%|​|​|
|7|US - Non AVT_B - C - [G]|15%|Group A|​|​|​|15%|
|8|US - AVT_B - [G]|10%|Group B|​|10%|​|​|
|9|US - AVT_B - C - [G]|10%|Group A|​|​|​|10%|
|10|US - AVT_All - [G]|4%|​|​|​|​|4%|
|11|TTL NB|100%|​|​|​|​|​|
|12|Accumulative reg Pene per  phase|​|​|23%|48%|71%|100%|
|13|Number of Wks|​|​|4|4|3|3|

||A|B|C|D|E|F|
|---|---|---|---|---|---|---|
|1|Non  Brand Bidding Portfolio|Spend Pene|Reg Pene|Weekly Spend Est|Weekly Reg Est|CPA Est|
|2|US - BAU -  [G]|12%|11%|$45,360|286|$159|
|3|US - BAU - C  - [G]|12%|11%|$45,360|286|$159|
|4|US - AVT_S  & L - [G]|11%|12%|$41,580|312|$133|
|5|US - AVT_S  & L - C - [G]|11%|12%|$41,580|312|$133|
|6|US - Non  AVT_B- [G]|18%|15%|$66,150|390|$170|
|7|US - Non  AVT_B - C - [G]|18%|15%|$66,150|390|$170|
|8|US - AVT_B -  [G]|8%|10%|$30,240|260|$116|
|9|US - AVT_B -  C - [G]|8%|10%|$30,240|260|$116|
|10|US - AVT_All  - [G]|3%|4%|$11,340|104|$109|
|11|TTL NB|100%|100%|$378,000|2,600|$145|

### Performance Data Reference
||A|B|C|D|E|F|G|H|I|J|K|
|---|---|---|---|---|---|---|---|---|---|---|---|
|1|NB Portfolio Spend Data|​|​|​|​|​|​|​|​|​|​|
|2|​|Phase 1|Phase 3|Phase 1|Phase 3|Phase 2|Phase 4|Phase 2|Phase 4|Phase 4|​|
|3|​|Group A|Group B|Group A|Group B|Group A|Group B|Group A|Group B|​|​|
|4|Weekly Spend|US - BAU - [G]|US - BAU - C - [G]|US - AVT_S & L - [G]|US - AVT_S & L - C - [G]|US - AVT_PB - [G]|US - AVT_PB - C - [G]|US - Non AVT_PB - [G]|US - Non AVT_PB - C - [G]|US - AVT_All - [G]|TTL NB|
|5|3/2/2025 - 3/8/2025|$36,018|$38,703|$49,242|$49,578|$39,130|$39,192|$51,054|$45,921|$12,210|$361,048|
|6|3/9/2025 - 3/15/2025|$40,295|$40,319|$45,839|$44,755|$31,329|$32,923|$51,298|$49,851|$11,750|$348,359|
|7|3/16/2025 - 3/22/2025|$43,183|$42,092|$45,465|$46,608|$28,449|$25,825|$55,979|$56,904|$11,711|$356,215|
|8|3/23/2025 - 3/29/2025|$41,962|$41,914|$44,921|$48,161|$29,974|$28,438|$57,155|$57,554|$11,476|$361,554|
|9|3/30/2025 - 4/5/2025|$42,996|$42,391|$44,614|$49,396|$30,378|$33,923|$53,983|$55,903|$11,916|$365,501|
|10|4/6/2025 - 4/12/2025|$41,629|$42,552|$40,028|$45,038|$30,918|$30,319|$55,274|$59,785|$10,983|$356,525|
|11|4/13/2025 - 4/19/2025|$42,368|$42,767|$33,268|$46,369|$25,325|$27,799|$62,653|$67,874|$10,575|$358,999|
|12|4/20/2025 - 4/26/2025|$45,327|$44,786|$33,254|$44,786|$27,885|$28,933|$68,996|$71,339|$10,949|$376,255|
|13|​|​|​|​|​|​|​|​|​|​|​|
|14|​|​|​|​|​|​|​|​|​|​|​|
|15|​|​|​|​|​|​|​|​|​|​|​|
|16|​|Group A|Group B|Group A|Group B|Group A|Group B|Group A|Group B|​|​|
|17|Weekly Spend Penetration|US - BAU - [G]|US - BAU - C - [G]|US - AVT_S & L - [G]|US - AVT_S & L - C - [G]|US - AVT_PB - [G]|US - AVT_PB - C - [G]|US - Non AVT_PB - [G]|US - Non AVT_PB - C - [G]|US - AVT_All - [G]|TTL NB|
|18|3/2/2025 - 3/8/2025|10%|11%|14%|14%|11%|11%|14%|13%|3%|100%|
|19|3/9/2025 - 3/15/2025|12%|12%|13%|13%|9%|9%|15%|14%|3%|100%|
|20|3/16/2025 - 3/22/2025|12%|12%|13%|13%|8%|7%|16%|16%|3%|100%|
|21|3/23/2025 - 3/29/2025|12%|12%|12%|13%|8%|8%|16%|16%|3%|100%|
|22|3/30/2025 - 4/5/2025|12%|12%|12%|14%|8%|9%|15%|15%|3%|100%|
|23|4/6/2025 - 4/12/2025|12%|12%|11%|13%|9%|9%|16%|17%|3%|100%|
|24|4/13/2025 - 4/19/2025|12%|12%|9%|13%|7%|8%|17%|19%|3%|100%|
|25|4/20/2025 - 4/26/2025|12%|12%|9%|12%|7%|8%|18%|19%|3%|100%|

||A|B|C|D|E|F|G|H|I|J|K|
|---|---|---|---|---|---|---|---|---|---|---|---|
|1|NB Portfolio EFID Reg Data|​|​|​|​|​|​|​|​|​|​|
|2|​|Phase 1|Phase 3|Phase 1|Phase 3|Phase 2|Phase 4|Phase 2|Phase 4|Phase 4|​|
|3|​|Group A|Group B|Group A|Group B|Group A|Group B|Group A|Group B|​|​|
|4|Weekly Spend|US - BAU - [G]|US - BAU - C - [G]|US - AVT_S & L - [G]|US - AVT_S & L - C - [G]|US - AVT_PB - [G]|US - AVT_PB - C - [G]|US - Non AVT_PB - [G]|US - Non AVT_PB - C - [G]|US - AVT_All - [G]|TTL NB|
|5|3/2/2025 - 3/8/2025|304|324|416|447|344|393|350|322|110|3,010|
|6|3/9/2025 - 3/15/2025|275|285|387|359|274|280|329|342|97|2,628|
|7|3/16/2025 - 3/22/2025|289|256|410|293|249|245|356|353|88|2,539|
|8|3/23/2025 - 3/29/2025|293|283|345|289|255|272|367|337|117|2,558|
|9|3/30/2025 - 4/5/2025|275|257|431|300|248|293|347|327|80|2,558|
|10|4/6/2025 - 4/12/2025|249|272|348|300|269|290|362|301|100|2,491|
|11|4/13/2025 - 4/19/2025|291|266|333|302|214|268|394|314|86|2,468|
|12|4/20/2025 - 4/26/2025|287|327|331|395|251|247|398|410|114|2,760|
|13|​|​|​|​|​|​|​|​|​|​|​|
|14|​|​|​|​|​|​|​|​|​|​|​|
|15|​|​|​|​|​|​|​|​|​|​|​|
|16|​|Group A|Group B|Group A|Group B|Group A|Group B|Group A|Group B|​|​|
|17|Weekly Spend Penetration|US - BAU - [G]|US - BAU - C - [G]|US - AVT_S & L - [G]|US - AVT_S & L - C - [G]|US - AVT_PB - [G]|US - AVT_PB - C - [G]|US - Non AVT_PB - [G]|US - Non AVT_PB - C - [G]|US - AVT_All - [G]|TTL NB|
|18|3/2/2025 - 3/8/2025|10%|11%|14%|15%|11%|13%|12%|11%|4%|100%|
|19|3/9/2025 - 3/15/2025|10%|11%|15%|14%|10%|11%|13%|13%|4%|100%|
|20|3/16/2025 - 3/22/2025|11%|10%|16%|12%|10%|10%|14%|14%|3%|100%|
|21|3/23/2025 - 3/29/2025|11%|11%|13%|11%|10%|11%|14%|13%|5%|100%|
|22|3/30/2025 - 4/5/2025|11%|10%|17%|12%|10%|11%|14%|13%|3%|100%|
|23|4/6/2025 - 4/12/2025|10%|11%|14%|12%|11%|12%|15%|12%|4%|100%|
|24|4/13/2025 - 4/19/2025|12%|11%|13%|12%|9%|11%|16%|13%|3%|100%|
|25|4/20/2025 - 4/26/2025|10%|12%|12%|14%|9%|9%|14%|15%|4%|100%|

||A|B|C|D|E|F|G|H|I|J|K|
|---|---|---|---|---|---|---|---|---|---|---|---|
|1|NB Bidding Portfolio EFID CPA|​|​|​|​|​|​|​|​|​|​|
|2|​|Phase 1|Phase 3|Phase 1|Phase 3|Phase 2|Phase 4|Phase 2|Phase 4|Phase 4|​|
|3|​|Group A|Group B|Group A|Group B|Group A|Group B|Group A|Group B|​|​|
|4|Weekly Spend|US - BAU - [G]|US - BAU - C - [G]|US - AVT_S & L - [G]|US - AVT_S & L - C - [G]|US - AVT_PB - [G]|US - AVT_PB - C - [G]|US - Non AVT_PB - [G]|US - Non AVT_PB - C - [G]|US - AVT_All - [G]|TTL NB|
|5|3/2/2025 - 3/8/2025|$118|$119|$118|$111|$114|$100|$146|$143|$111|$120|
|6|3/9/2025 - 3/15/2025|$147|$141|$118|$125|$114|$118|$156|$146|$121|$133|
|7|3/16/2025 - 3/22/2025|$149|$164|$111|$159|$114|$105|$157|$161|$133|$140|
|8|3/23/2025 - 3/29/2025|$143|$148|$130|$167|$118|$105|$156|$171|$98|$141|
|9|3/30/2025 - 4/5/2025|$156|$165|$104|$165|$122|$116|$156|$171|$149|$143|
|10|4/6/2025 - 4/12/2025|$167|$156|$115|$150|$115|$105|$153|$199|$110|$143|
|11|4/13/2025 - 4/19/2025|$146|$161|$100|$154|$118|$104|$159|$216|$123|$145|
|12|4/20/2025 - 4/26/2025|$158|$137|$100|$113|$111|$117|$173|$174|$96|$136|

### Rollout Notes
* OCI ready by 6/2/25, 4 wks data gathering period before can turn on TROAS
 * 15 convs per week
* US rollout into 4 phases, start 6/30/25 to 9/15/25.
 * Due to 6-8 wks waiting time for A/B testing, and no evenly spend distribution, we use pre vs post to measure performance lift.
 * NB Phase 1 : 23% of NB ttl spend
  * To better measure performance, we will find 2 groups of campaigns with group A as adobe bidding group and group B as OCI bidding group. group A & B will keep use the same budget and had similar behavior for past 8 weeks. it means spend penetration for group A and group B is 22% for each.
  * We will check on pre vs post perf lift on both groups to see if OCI bidding has higher lift to eliminate seasonality factor
  * We expect at least 2 weeks but may go for 3 weeks to measure the perf lift.
 * NB Phase 2: 26% of ttl NB spend on top of phase 1 group of campaigns. Accumulative spend penetration for OCI bidding is 49% (23% from phase 1, 26% from phase 2).
 * NB Phase 3: 23% of ttl NB spend on top of phase 2 group of campaigns. Accumulative spend penetration for OCI bidding is 72% (23% from phase 1, 26% from phase 2, 23% from phase 3).
 * NB Phase 4: 29% of ttl NB spend on top of phase 3 group of campaigns. Accumulative spend penetration for OCI bidding is 100%. This phase for control groups OCI roll out.

*Note for 3 days implementation time - add 1 day buffer due to team member sick, or other reasons
below plan assume 4 wks for G ads to learn, so start roll out on 7/2/2025. it takes 10 wks to roll out and end on 8/27/25
### Roll-out Actions and Considerations
Pre vs Post comp:
* may need to exclude the 1st wk data due to bid adj at the beginning
Negative perf plan:
* currently we have 2 weeks per phase to monitoring performance. if we see a negative impact on perf, we will extend the 2 wks to 4 wks, then to 6 wks period to give more time for G ads bidding to learn.
 * flat or better, can keep rolling out the troas bidding
* If still negative impact after 6 wks without improvement, we would expect modify OCI value would be needed.
### Performance Notes (Factor to consider)
YoY perf notes:
* IE%CCP diff: LY we started opening up 75% ie%ccp in Jul (Wk 27), contributed 5% of ttl (10% of NB) lift on regs vol.
* Adobe learning period: LY adobe bidding started on May, and got 2 months learning when went into Jul
Prime impact

# EU OCI Planning
### UK
#### UK splits
||A|B|C|D|E|F|G|H|I|J|K|
|---|---|---|---|---|---|---|---|---|---|---|---|
|1|Option 1 - Split by portfolio|Last 3 months data|​|​|​|​|​|Option 2- A/B within Portfolio|Last 3 months data|​|​|
|2|UK Group A - Control|Spend|Clicks|Registrations|CPA|​|​|UK Group A|Spend|Registrations|CPA|
|3|EU-UK-Google-GA_Top|$126,303|62765|966|$131|131|​|AMZ1|$22,126|159|$139|
|4|EU-UK-Google-AMZ|$42,723|16735|300|$142|​|​|Brand Plus 1|$35,079|224|$157|
|5|UK_Brand (campaign)|$26,165|4478|133|$197|159|​|GA 1|$131,348|918|$143|
|6|Total A|$195,191|83,978|1,399|$140|​|​|PV1|$19,086|157|$122|
|7|Per day|$2,169|933|16|​|​|​|Total A|$207,639|1458|$142|
|8|​|​|​|​|​|​|​|Per day|$2,307|16|​|
|9|UK Group B - Test|Spend|Clicks|Registrations|CPA|​|​|​|​|​|​|
|10|EU-UK-Google-Generic|$107,932|44776|751|$144|​|​|UK Group B|Spend|Registrations|CPA|
|11|EU-UK-Google-Product-Vertical|$38,796|23689|308|$126|139|​|AMZ2|$20,597|141|$139|
|12|EU-UK-Google-GA|$15,409|6579|58|$266|​|​|Brand Plus 2|$26,164|133|$157|
|13|UK_GA_Brand (campaign)|$35,080|5791|224|$157|179|​|GA2|$118,294|857|$143|
|14|Total B|$197,217|80,835|1,341|$147|​|​|PV2|$19,709|151|$122|
|15|Per day|$2,191|898|15|​|​|​|Total B|$184,764|1282|$144|
|16|​|​|​|​|​|​|​|Per day|$2,053|14|​|
|17|​|​|​|​|​|​|​|​|​|​|​|
|18|Pros:|Cons:|​|​|​|​|​|Pros:|Cons:|​|​|
|19|Simpler implementation|Search terms are different|​|Baseline CVR|Stat sig|Min detectable effect|If MDE 10%|Will require a bit more implementation, but would allow for a more phased approach|Split within each portfolio|​|​|
|20|KPIs line up closely|Either group may react differently to OCI|​|1.67%|95%|11.6%|110K clicks|CPAs line up more closely|​|​|​|

#### UK Timeline
||A|B|C|D|E|F|G|H|I|
|---|---|---|---|---|---|---|---|---|---|
|1|UK|Duration|6/30/2025|8/4/2025|9/1/2025|9/8/2025|9/10/2025|10/8/2025|10/13/2025|
|2|Data gathering  to meeting conv threshold|4 weeks|All|​|​|​|​|​|​|
|3|Assign Group B campaigns to separate OCI portfolios|1 day|​|​|​|​|​|​|​|
|4|4-week test period (1-2 weeks volatility)|4 weeks|​|​|​|​|​|​|​|
|5|5 day holding period (still active)|5 day|​|​|7 days because weekend|​|​|​|​|
|6|Analysis|2 days|​|​|​|​|​|​|​|

### DE
#### DE splits
||A|B|C|D|E|F|G|H|I|J|K|L|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|1|Option 1 - Split by portfolio|​|​|​|​|Option 2 - A/B within Portfolio|​|​|​|​|​|​|
|2|DE Group A|Spend|Registrations|CPA|​|DE Group A - Control|Spend|Clicks|Registrations|CPA|Current AMO bidding Strategy|​|
|3|EU-DE-Google-Generic|$543,728|2602|$209|​|AMZ1|$113,509|41,785|645|$176|CPT|​|
|4|EU-DE-EN-Google-NB|$10,597|17|$623|​|Brand1|$216,418|30,328|740|$292|CPT|​|
|5|DE - GA 2 - Brand|$216,418|740|$292|​|GA1|$113,801|60,737|442|$257|CPT|​|
|6|Total A|$770,743|3359|$229|​|Generic1|$273,354|59,746|1209|$226|CPT|​|
|7|Per day|$8,564|37|​|​|PV1|$47,192|23,645|112|$421|Marginal|​|
|8|​|​|​|​|​|Total A|$717,082|192,596|3036|$236|​|​|
|9|DE Group B|Spend|Registrations|CPA|​|Per day|$7,968|2,140|34|$236|​|​|
|10|EU-DE-Google-AMZ|$230,098|1372|$168|​|​|​|​|​|​|​|​|
|11|EU-DE-Google-GA_Top|$129,810|478|$272|​|DE Group B - Test|Spend|Clicks|Registrations|CPA|Current AMO bidding Strategy|​|
|12|EU-DE-Google-GA|$100,883|367|$275|​|AMZ2|$116,588|50736|727|$160|CPT|​|
|13|EU-DE-Google-Product-Vertical|$82,868|215|$385|​|Brand2|$155,343|17796|614|$253|CPT|​|
|14|DE_Brand|$155,344|614|$253|​|GA2|$116,891|56778|403|$290|CPT|​|
|15|Total B|$699,003|3046|$229|​|Generic2|$270,373|73342|1393|$194|CPT|​|
|16|Per day|$7,767|34|​|​|PV2|$46,272|19129|120|$386|Marginal|​|
|17|​|​|​|​|​|Total B|$705,467|217,781|3257|$217|​|​|
|18|​|​|​|​|​|Per day|$7,839|2,420|36|$217|​|​|
|19|Pros:|Cons:|​|​|​|​|​|​|​|​|​|​|
|20|Simpler implementation|Search terms are different|​|​|​|Pros:|Cons:|​|​|​|​|​|
|21|KPIs line up closely|Either group may react differently to OCI|​|​|​|Will require a bit more implementation|Split within each portfolio|​|Baseline CVR|Stat sig|Min detectable effect|If MDE 10%|
|22|​|​|​|​|​|Would allow for a more phased approach|​|​|1.58%|95%|8%|120K needed|
|23|​|​|​|​|​|​|​|​|​|​|​|​|
|24|​|​|​|​|​|​|Ph 1|ph2|Ph 3|Ph4|Ph5|​|
|25|​|​|​|​|​|UK|1,059|282|433|966|​|​|
|26|​|​|​|​|​|DE|1513|614|2,451|740|1,087|​|
|27|​|​|​|​|​|​|​|​|​|​|​|​|

#### DE Timeline
||A|B|C|D|E|F|G|H|
|---|---|---|---|---|---|---|---|---|
|1|DE|Number of days|10/1/2025|10/22/2025|11/11/2025|11/24/2025|12/1/2025|12/8/2025|
|2|Reftag change, then validate the splits again|​|​|​|​|​|​|​|
|3|Data gathering  to meeting conv threshold|21|All|​|​|​|​|​|
|4|Make changes to Adobe/Google bid strategies|1|​|​|​|​|​|​|
|5|1-2 weeks volatility|14|​|​|​|​|​|​|
|6|3-week test period|21|​|​|​|​|​|​|
|7|5 day holding period (still active)|5|​|​|​|​|​|​|
|8|Control campaigns implementation|2|​|​|​|​|​|​|
|9|Analysis|​|​|​|​|​|​|​|
|10|Transition complete|​|​|​|​|​|​|​|
|11|*Accelerate DE. One A/B test that starts 10/30 and completes 11/19|​|​|​|​|​|​|​|

**Campaign splits**: [EU5\_OCI-Testing\_Split.xlsx][11]
**Optimization of ROAS bid strategy**: [Management of OCI/ROAS][12]
### Timing approach:
Similar to the US, with focus on allowing data to accumulate within reason.
* First 4 weeks of OCI data, allow data to accumulate
* Week 1 of testing: Apply OCI to Group B
* Weeks 2-7: Official testing period, 6 weeks recommended
* Week 8: Convert to OCI if data shows this group as performing at least as well as control group.
### Measurement/Reporting:
* Will record each week’s clicks, registrations from dashboard, and CPA.
* Try to manage spend as consistent between groups
* Success metric will be **Registrations and CVR**.
 * Dashboard registrations are final metric that we care about, but we’re running under the assumption that control/test are comprised of similar volume and that the bid strategy is manipulating volume.
 * Use Bayesian calculator for each week, and should see a consistent weekly trend at least 50% or better. (50% or more likely that the test is better than the control)
 * ABMA support - want to make sure we’re doing analysis from WBR perspective

### Details on Timeline
#### 1) Data gathering to meeting conv threshold
* UK Planned: 6/2 - 6/30
* UK Actual: 6/30 - 7/30
* Actions: Monitor the two groups’ OCI conversions and EF ID. (OCI metric within Google)
 * Ideally they are producing a consistent stream, and not too volatile.
#### 2) Assign Group B campaigns to separate OCI portfolios
* UK Planned: 6/30
* UK Actual: 8/4
* Actions: Go into Adobe, filter for campaigns where “OCI-Test” metric contains “test” and assign to respective segment’s portfolio.
 * OCI-Test metric is is a label applied to show which are the test/control for the test.
 * Use this label to divide each segment into its own portfolio. (**Test campaigns will go into newly built Portfolios**)
 * **The newly built portfolios should be active**, but not optimizing the account. (for easier reporting)
 * **Go into Google, and add all test campaigns into new bid strategies \(create one for each Adobe portfolio\)**
  * Set target ROAS to steer efficiency.
   * Initially set a ROAS target that matches the ROAS for the past month of data (exclude the recent 5 days)
  * Make sure the test campaigns are using the new revenue-based bid strategies, and the control campaigns are set to Manual CPC
#### 3) Pre-test hold period
* UK planned: 6/30 to 7/7
* UK actual: 8/5 to 8/11
* Actions: Make sure to check accounts each day to monitor changes.
 * Initially, we won’t have conversion data (5-day lag), so monitor spend.
 * After 2-3 days, you can start looking over OCI/Adobe registration data.
 * The main action during this period is to make sure the Test group’s bid strategy is not radically changing the cost, and steering it back to a normal level of spend before the test period.
 * What should do in the AMO side?
  * Request AMO to exclude XYZ data?
* Ensure to do AMO and Google Ads bidding switch around the same (do AMO first, so the campaigns won’t get changed while working on the Google Ads part)
#### 4) Test period
* UK planned: 7/7 to 8/4
* UK actual: 8/12 to 9/8
* Actions: Optimize normally, and try to keep spend at a normal level
 * Follow seasonality and efficiency thresholds for the business.
 * Avoid making changes that are too large, or making too many consecutive changes. (Want to let Google to be able to work within stability)
 * Assign OCI campaigns into new AMO portfolios and ensure the portfolios status aren’t "optimized"
 * Create OCI campaigns’ shared budget and bid strategies in Google Ads and assign OCI campaigns into the right shared budget and bid strategies according
#### 5) Post-test hold period
* UK planned: 8/4 to 8/11
* UK actual:
* Actions: Same as test period.
#### 6) Analysis and switch over to OCI pending results
* UK planned: After 8/11
* UK actual:
* Actions: Look at change in registrations for control and for test.
 * Also look at change in CVR; Use a Bayesian calc to calculate prob %.
 * If successful, change Adobe portfolios to active, and apply Google bid strategies to respective campaigns.
 * If not successful, we will need to come up with a hypothesis of why it didn’t, and resolve that with a change. First, think about whether it was the ROAS bid strategy that performed poorly, or the Adobe bid strategy performed significantly better. Ideas:
  * Maybe it took too long to get used to the behavior of the bid strategy, or we over-optimized. Solution is to re-run with those learnings.
  * The bid strategies aren’t working well. Solution might be to think about guardrails to add before re-running. Max bid (for ROAS bid strategy), Target ROAS (for max conversion bid strategy)
* [OCI benchmarking.xlsx][13]
#### ​
### Data
#### Starting ROAS approach (More info here: [Management of OCI/ROAS][12])
||A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|1|Google Ads data - Jul 6th to 26th|​|​|​|​|​|​|​|​|​|​|​|abs. vol|rel vol|​|
|2|Group A|Cost|Conversions|Conv. Value|CPA|ROAS|ROAS target (second phase)|​|Week1 ROAS|Week 2 ROAS|Week 3 ROAS|Mean ROAS|Std.dev.|CV|​|
|3|EU-UK-Google-GA_Top|$28,665|481|$3,970|$60|13.80%|11.80%|​|15.97%|14.11%|10.55%|13.85%|2.75%|19.90%|​|
|4|EU-UK-Google-AMZ|$8,674|162|$962|$54|11.10%|8.90%|​|15.60%|9.78%|8.25%|11.09%|3.88%|35%|​|
|5|UK_Brand (campaign)|$6,824|48|$780|$142|11.40%|9.10%|​|10.81%|9.07%|16.25%|11.42%|3.75%|32.80%|​|
|6|Total A|$44,163|691|$5,711|$64|12.90%|​|​|​|​|​|​|*normal|*Above 20% is high|​|
|7|​|​|​|​|​|​|​|​|​|​|​|​|​|​|​|
|8|​|​|​|​|​|​|​|​|​|​|​|​|abs. vol|rel vol|​|
|9|Group B|Cost|Conversions|Conv. Value|CPA|ROAS|ROAS target|​|Week1 ROAS|Week 2 ROAS|Week 3 ROAS|Mean ROAS|Std.dev.|CV|​|
|10|EU-UK-Google-Generic|$29,131|505|$4,088|$58|14%|11.90%|​|16.63%|10.57%|14.39%|14.03%|3.06%|21.80%|​|
|11|EU-UK-Google-P-V|$15,020|222|$1,732|$68|11.50%|10.40%|​|10.13%|12.52%|13.24%|11.53%|1.63%|14.10%|​|
|12|EU-UK-Google-GA|$3,046|50|$374|$61|12.30%|9.80%|​|15.03%|7.58%|15.11%|12.27%|4.32%|35.20%|​|
|13|UK_GA_Brand (campaign)|$6,047|81|$953|$75|15.80%|12.60%|​|20.95%|13.08%|10.77%|15.75%|5.34%|33.90%|​|
|14|Total B|$53,244|858|$7,147|$62|13.40%|​|​|​|​|​|​|*normal|*Above 20% is high|​|
|15|​|​|​|​|​|​|*Target 80% of baseline for more  volatile|​|​|​|​|​|​|​|​|
|16|​|​|​|​|​|​|90% for more predictable|​|​|​|​|​|​|​|​|

#### Pre-ref changes data
||A|B|C|D|E|F|
|---|---|---|---|---|---|---|
|1|Option 1 - Split by portfolio|4/12 - 4/30|​|​|​|​|
|2|UK Group A - Control|Spend|Clicks|Registrations|CPA|​|
|3|EU-UK-Google-GA_Top|$23,876|12557|110|$217|​|
|4|EU-UK-Google-AMZ|$4,554|1662|23|$198|​|
|5|UK_Brand (campaign)|$2,600|609|2|$1,733|​|
|6|Total A|$31,029|14,828|135|$231|​|
|7|Per day|$1,633|780|7|​|​|
|8|​|​|​|​|​|​|
|9|UK Group B - Test|Spend|Clicks|Registrations|CPA|​|
|10|EU-UK-Google-Generic|$23,655|10622|144|$164|​|
|11|EU-UK-Google-Product-Vertical|$2,009|1456|6|$335|​|
|12|EU-UK-Google-GA|$2,092|972|6|$349|​|
|13|UK_GA_Brand (campaign)|$2,637|681|1|$5,274|​|
|14|Total B|$30,393|13,731|157|$194|​|
|15|Per day|$1,600|723|8|​|​|
|16|​|​|​|​|​|​|
|17|​|​|​|​|​|​|
|18|Pros:|Cons:|​|​|​|​|
|19|Simpler implementation|Search terms are different|​|Baseline CVR|Stat sig|Min detectable effect|
|20|KPIs line up closely|Either group may react differently to OCI|​|0.91%|95%|11.6%|

||A|B|C|D|E|F|
|---|---|---|---|---|---|---|
|1|Option 2 - A/B within Portfolio|​|​|​|​|​|
|2|DE Group A - Control|Spend|Clicks|Registrations|CPA|​|
|3|AMZ1|$34,862|8,187|132|$264|​|
|4|Brand1|$39,263|3,809|118|$333|​|
|5|GA1|$22,328|11,116|30|$744|​|
|6|Generic1|$71,438|15,132|203|$352|​|
|7|PV1|$4,058|2,243|12|$338|​|
|8|Total A|$171,949|40,487|495|$347|​|
|9|Per day|$9,050|2,131|26|​|​|
|10|​|​|​|​|​|​|
|11|DE Group B - Test|Spend|Clicks|Registrations|CPA|​|
|12|AMZ2|$34,565|9917|112|$309|​|
|13|Brand2|$35,808|2857|254|$141|​|
|14|GA2|$31,179|15078|42|$742|​|
|15|Generic2|$67,464|16149|238|$283|​|
|16|PV2|$3,807|1712|10|$381|​|
|17|Total B|$172,823|45,713|656|$263|​|
|18|Per day|$9,096|2,406|35|​|​|

[1]: https://w.amazon.com/bin/view/AAHydra/OCI/CIT/Dashboards/Prod-EU/PortfolioLevel/
[2]: https://quip-amazon.com/UNlJAiiYljjd/OCI-Planning#temp:C:dSZ025e08171a55439fa6404b741
[3]: https://amazon-my.sharepoint.com/:x:/r/personal/prichwil_amazon_com/_layouts/15/Doc.aspx?sourcedoc=%7BA87F4A0E-93F0-443C-91D5-AED481BA74FF%7D&file=TT_UK_Campaign-Phasing.xlsx&action=default&mobileredirect=true
[4]: https://docs.google.com/spreadsheets/d/1gN_CMeUvgxI2NvxZ4DVqBt_5Ul7pv8zoquJG9oJalxY/edit?gid=1773547684#gid=1773547684
[5]: https://na.amazon-value-service.com/cl/v1/p/BSQ1ZjkFy2M2q-R5Vhq2HzSs5l2d8ndQPn0KMtF79_ieEA?lp={lpurl}&vscl={gclid}&vsco={gbraid
[6]: https://eu.amazon-value-service.com/cl/v1/p/BSQ1ZjkFy2M2q-R5Vhq2HzSs5l2Y8nxEPn0KMtF79_ieEA?lp={lpurl}&vscl={gclid}&vsco={gbraid}
[7]: https://pixel.everesttech.net/9012/cq?ev_sid=3&ev_ln={keyword}&ev_lx={targetid}&ev_crx={creative}&ev_mt={matchtype}&ev_n={network}&ev_ltx={_evltx}&ev_pl={placement}&ev_pos={adposition}&ev_dvc={device}&ev_dvm={devicemodel}&ev_phy={loc_physical_ms}&ev_loc={loc_interest_ms}&ev_cx={campaignid}&ev_ax={adgroupid}&ev_efid={gclid}:G:s&url={lpurl
[8]: https://eu.amazon-value-service.com/cl/v1/p/BSQ1ZjkFy2M2q-R5Vhq2HzSs5l2f8nxEPn0KMtF79_ieEA?lp={lpurl}&vscl={gclid}&vsco={gbraid
[9]: https://quip-amazon.com/-/blob/dSZ9AAZBXQy/fM3t_Qxwh3knRyUvTuGcqQ?name=US%2010%25%20traffic%20campaign%20list.xlsx
[10]: https://quip-amazon.com/bigrA7jVSvex
[11]: https://amazon-my.sharepoint.com/:x:/p/prichwil/EbAg4TSrnvFNk-msD4kn02cBWA45Fr-ye5g53KQuuTRupQ?e=c4Snty
[12]: https://quip-amazon.com/UcZuAbj1HloC
[13]: https://amazon-my.sharepoint.com/:x:/r/personal/prichwil_amazon_com/Documents/OCI%20benchmarking.xlsx?d=w5cd8ac1e63f24f7cbdabab3a52cb342a&csf=1&web=1&e=nmEMUf
