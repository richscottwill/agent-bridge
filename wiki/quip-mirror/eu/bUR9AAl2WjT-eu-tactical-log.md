---
audience: amazon-internal
creator: Richard Williams
doc_type: document
last_modified: 2024-12-19
mirror_date: 2026-04-10
owner: Richard Williams
quip_folder: ..EU
quip_id: bUR9AAl2WjT
source_url: https://quip-amazon.com/bUR9AAl2WjT
status: DRAFT
title: EU tactical log
topics:
- europe
- eu5
- paid-search
backfill_status: backfilled
---

# EU tactical log

## Regular bid/budget changes
#### **Brand-plus Learning budget %**
> 5/29 - increased brand-plus learning budgets from 10% to 20%. Next, 6/4 see the effect on predictions as well as CPA.
>
> ​
#### Manage ie%CCP
> 5/29 - decreased max budget multiple from 1.5 to 1.4, and lowered budgets as well. Next, 5/31, see
>
>
> 6/5 - enabled device modifiers in Adobe only for P-V portfolios across EU \(generally smallest/doesn't perform well\)
>
>
> X/X rolled out device, location, audience modifiers across markets
>
>
> X/X rolled out weekly budget to Bing Ads and
>
>
> 8/13 - P-V to most reactive \(DE\)
>
>
>
>
>
> Point to lower CPCs as result of modifiersCase study for bid adjustments:
* EU5 P-V added bid modifiers 6/5 to favor decreasing mobile -50% to 0%, and increasing desktop 0% to 20%. Rolled out to other markets.
Cast study for other budget types:
* ENG: Monthly
* Bing Ads: Weekly (now CPT)
Case study for recency:
* BFCM: increasing budget week prior to BFCM.
#### **CPT**
> 8/6 - CPT for IT GA. Met goal as of 8/21. v5
>
>
> 8/21 - added to other markets' GA campaign.
>
>
> 8/28 - GA bid strategies lowered CPT target to the current target multiplied by the percentage revenue accuracy. \(based on Suzanne's email\)​
Case study for CPT:
* IT GA: Launched 8/6 - 8/21. Improved understanding 8/28.
* GA EU5 from 8/21 (compare GA to others over PoP.)

#### DE-en
> X/X launched \(Sabryna\)
>
>
> 8/28 - took over from Sabryna
>
>
> 8/28 - Added all campaigns to Adobe bidding---
## Structure
#### Consolidation
> X/X - Consolidated Bid strategies
>
>
> X/X - Brand flowing into NB
>
>
> 8/14 - re-added GA/GA2
>
>
> 8/22 - IT GA and GA2 into better performing campaign, and redistributing campaigns to bid strategies \(GA and GA\_Top\). I found it was about 50/50 where there were duplicate terms vs. it being set up correctly.
>
>
> 8/23 - Rolled Covid campaigns into respective P-V or GA campaigns \(active ad groups/keywords\) This is going to reduce redundancy.
>
>
>
>
>
> Next, GA and GA2 across other markets.​
#### Modern Search
> 3/1 - Implemented 13 smallest non-AVT/AMZ/Brand campaigns
>
>
> 3/7 - Implemented 6 medium non-AVT/AMZ/Brand campaigns
>
>
> 5/30 and 6/4 - implemented 4 non-AVT/AMZ/Brand campaigns
>
>
>
>
>
> Next, look over broad performance and effect on Adobe budget size/bidding---
## Tracking/Attribution
#### reftags
> X/X - found that reftags were being overwritten on
> [B.A.com][1]
> because of a setting that allowed reftags to be overwritten
>
>
> 7/17 - EU Sitelink reftags fixed. \(some without refs, and all sitelinks leading to
> [a.com][2]
> weren't formatted as "ref\_="\)
>
>
> X/X - ABMA found reftags disappearing just before registration confirmed for EU regs \(as a result of EU CVR investigation\)
>
>
> X/X - Brand/NB split isn't correct on WBR doc, which will affect ie%CCP​
**Conversion tracking**
> X/X - found Adobe pushing small business month landing page visits conversion signal to Google Ads \(all accounts\), and this overvalued high click campaigns and diluted registration signal for US account. \(initial pushback from Chunsoo\)
>
> ---
## Not Active
#### Pmax
> Did some testing, but paused in May 2024 due to switch away from OCI.
>
> ---

## **Budget Types:**
#### **Target Budget:**
* Daily: What we all use today. It prioritizes objective over spend.
* Weekly: distributes budget across each day (given enough data). This is more balanced and tends to prioritize both budget and objective.
* Monthly: Allow Adobe doesn't account for weekends/weekday, but gets close to your budget. This one tends to focus on spending because it has to project out for the full month.

#### **Target CPT (Cost/Transaction):**
* Similar to Google Ads bid strategies, but we get to control min/max budget.
* Prioritizes averaging for the CPT target across the keywords it has enough data for.
* Can be affected by the coverage/accuracy of the portfolio.

## Case Studies:
#### Case study for bid adjustments:
* EU5 P-V/GA added bid modifiers 6/5 to favor decreasing mobile -50% to 0%, and increasing desktop 0% to 20%.
 * -36% CPC P-V/GA (+45% clicks) vs. -27% NB other (+5% clicks)
 * Rolled out to other portfolios in early July.
* Added Regions to EU5 markets 7/7 to test location bid adj.
#### Cast study for other budget types:
* IT GA: Launched 8/6. Improved understanding 8/21 to 9/21 along with other EU5 markets.
 * PoP 8/06 to 9/21: Cost -65%, Regs -43%, CPA -38%, CPC-13%.
 * Considered successful because we were in a period of high ie%CCP, and were able to lower high-CPA cost.
* GA EU5 from 8/21 (compare GA to others over PoP 8/21 to 9/21.)
 * GA CPA from $340 to $177 (-48%), CVR +96%, but -66% clicks/-34% regs.
 * Others NB from $133 to $148 CPA (-11%), CVR +12%, clicks -1%/regs +10%.
 * I considered this successful because we were in a period of low efficiency and wanted to control GA efficiency (generally least efficient)
#### Case study for recency:
* BFCM: increasing budget week prior to BFCM.

## Tactics to improve:
#### **Bid adjustments** to allow Adobe to spend more or less:
* If overpacing or need better efficiency, rather than changing targets or budget, you can first allow Adobe to decrease bid adjustments for device (or location/audience if granular enough)
* If underpacing or need higher ie%CCP, you can adjust your ranges to favor less restriction. (if Mobile was set to -60% to +0%, then you can shift to -40% to +10%)

#### **Importance of consolidation of ad groups/campaigns:**
Streamline management and improve data aggregation.
* Improve Revenue/Cost Accuracy: Uses historical data to project and evaluate performance.
* Improve Coverage: Whether bid units (keywords/ad groups) have enough historical data to optimize.
* Interdependence: Coverage and accuracy are linked; enough data (coverage) boosts model confidence  (accuracy). Coverage is probably less important if portfolio is skewed towards a few ad groups/keywords.
* Currently experimenting with increasing Learning Budget to enhance coverage.

[1]: http://B.A.com
[2]: http://a.com
