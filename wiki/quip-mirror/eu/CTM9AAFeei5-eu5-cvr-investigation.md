---
audience: amazon-internal
creator: Richard Williams
doc_type: document
last_modified: 2025-02-13
mirror_date: 2026-04-10
owner: Richard Williams
quip_folder: ..EU
quip_id: CTM9AAFeei5
source_url: https://quip-amazon.com/CTM9AAFeei5
status: DRAFT
title: Paid Search EU5 CVR investigation
topics:
- europe
- eu5
- paid-search
backfill_status: backfilled
---

# Paid Search EU5 CVR investigation
### Reference
Adobe Reg Start Report: [https://www5.an.adobe.com/x/5\_18rxck][1]
Registration Funnel Quicksight: [https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/36d03af5-8df3-4844-a8df-f13e6547ed6c/sheets/36d03af5-8df3-4844-a8df-f13e6547ed6c\_34f2cc16-549f-4aa0-912a-049a18a00be3][2]
SIM: https://issues.amazon.com/issues/ABMA-6143[][3][Richard Williams][3]
Resolution: Attribution logic updated after ABMA's impact analysis, with regs coming from Direct/Unknown channels. (UK +5.4%, DE +4.1%, FR +8.4%, IT +4.3%, ES +4.3%)
## **P. 0**
||A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|1|Brand Q1 YoY|Reg Start (Visitors)|Reg|CVR|Imps|Clicks|CPA|CPC|​|Brand Q2 YoY|Reg Start (Visitors)|Reg|CVR|Imps|Clicks|CPA|CPC|
|2|UK|4%|16.1%|-7%|-3%|25%|19.4%|11%|​|UK|18%|-4.3%|22%|-53%|-22%|-14.4%|5%|
|3|DE|3%|-20.1%|-22%|-46%|3%|52.3%|19%|​|DE|61%|12.9%|-6%|-35%|20%|61.8%|53%|
|4|FR|8%|-16.9%|-24%|-47%|10%|97.7%|50%|​|FR|73%|26.9%|6%|-21%|20%|79.9%|90%|
|5|IT|-52%|4.8%|-13%|17%|20%|177.8%|142%|​|IT|-7%|21.0%|-3%|23%|25%|40.4%|36%|
|6|ES|956%|-5.5%|-21%|15%|19%|105.4%|63%|​|ES|2476%|8.0%|-18%|21%|32%|97.8%|62%|
|7|EU|-6%|-4.3%|-17%|-21%|15%|71.9%|43%|​|EU|70%|14.0%|-2%|-16%|17%|42.6%|39%|
|8|​|​|​|​|​|​|​|​|​|​|​|​|​|​|​|​|​|
|9|Brand Q3 YoY|Reg Start (Visitors)|Reg|CVR|Imps|Clicks|CPA|CPC|​|Brand Q4 YoY|Reg Start (Visitors)|Reg|CVR|Imps|Clicks|CPA|CPC|
|10|UK|64%|32.3%|7%|-58%|23%|-3.2%|4%|​|UK|32%|-1.7%|-23%|26%|27%|64.9%|28%|
|11|DE|42%|14.7%|-11%|-9%|29%|79.9%|60%|​|DE|51%|27.1%|-20%|81%|58%|96.7%|58%|
|12|FR|47%|26.3%|-12%|12%|44%|73.7%|52%|​|FR|19%|4.6%|-25%|31%|39%|62.2%|22%|
|13|IT|11%|15.6%|-12%|-20%|31%|6.2%|-6%|​|IT|8%|1.1%|-19%|-1%|25%|-29.9%|-43%|
|14|ES|2065%|29.1%|-18%|-7%|57%|74.3%|44%|​|ES|1184%|4.9%|-25%|46%|40%|32.4%|-1%|
|15|EU|73%|22.5%|-9%|-24%|35%|36.7%|24%|​|EU|53%|6.1%|-22%|29%|35%|41.2%|11%|

||A|B|C|D|E|F|G|H|
|---|---|---|---|---|---|---|---|---|
|1|Brand Dec YoY|Reg Start (Visitors)|Reg|Imps|Clicks|CVR|CPA|CPC|
|2|UK|25%|-12.70%|74%|42%|-39%|126%|39%|
|3|DE|69%|38.60%|153%|89%|-27%|157%|89%|
|4|FR|3%|-11.80%|27%|28%|-31%|104%|40%|
|5|IT|3%|-14.80%|0%|14%|-25%|-10%|-33%|
|6|ES|1719%|-22.20%|17%|12%|-31%|-2%|-32%|
|7|EU|49%|-7%|47%|33%|-30%|90%|34%|

## January 2024 investigation into CVR
Brand Paid Search is consistently saturated with ~97% ad visibility, which gives us strong insight into consumer trends or internal attribution gaps (ie. performance trends are relatively isolated from competition and bid changes).

### **Brand Search query data**: What we see
- **CVR decline Jan 2024 YoY**: This is what prompted us to reach out. Although traffic and Regs are up YoY for Brand Core search terms YoY, we're down in CVR, just like in other Brand terms. (adobe data)
||A|B|C|D|E|F|G|
|---|---|---|---|---|---|---|---|
|1|UK|Brand Core (search terms)|​|​|Brand (not Core)|​|​|
|2|​|Jan 2024|Jan 2023|% change|Jan 2024|Jan 2023|% change|
|3|Impressions|40,193|40,985|-2%|25,941|11,655|123%|
|4|Clicks|25,589|14,473|43%|11,668|11,103|5%|
|5|Cost|$17,420|$15,125|13%|$19,784|$8,440|134%|
|6|Conv (Reg Complete)|439|307|30%|441|551|-20%|
|7|CTR|63.70%|35.30%|80%|45%|95.30%|-53%|
|8|CPC|$0.68|$1.05|-35%|$1.70|$0.76|123%|
|9|CPA|$40|$49|-20%|$45|$15|193%|
|10|CVR|1.70%|2.10%|-19%|3.80%|5%|-24%|

### **Unique visitors > Reg Start > Registration: Further investigation with Adobe Analytics**
* Jan 2024 YoY, Unique Visitors increased 30%, Reg Start visitors increased 23%, and Registrations increased only 8%. A gradual dropoff throughout the customer journey is fine, but CVR from Reg Start to Registration is particularly low. In contrast, the US experienced +30% unique visitors, +14% reg start visitors, and +16% registrations
 * Reg start to Reg complete/pending for Paid Search traffic to their respective LPs:
  * US: +9% CVR
  * UK: -64% CVR
  * DE: -20% CVR
  * FR: +8% CVR
  * IT: -6% CVR
  * ES: -43% CVR (minimal traffic sent to Brand LP last year)
* The exit page of 75% of visitors is the Brand LP. Up from 65% last year. (More people clicking out to another page last year) This shift is likely due to lower CVR and higher bounces.

**LP CTA clicks**: 56% of people entering into UK Brand LP are accepting cookies, and 24% are clicking to "Start Shopping"

**Recreating the KPIs from the WBR New Customer Funnel: **
* Asked Naresh, the owner of the WBR section how to pull the data below, which will help to see more granular reg start data. (Something we currently don't report on internally)
 * Questions to ask:
  * Any parts of the registration that are currently being tested?
  * Any interstititals during the process?
  * When did this lower CVR begin, and what changed in terms of the data? (UK is best example)
* Comments for below:
 * Total unique MCS visitors and reg starts decreased. (-51% and -45% respectively)
 * Brand increased significantly, up to +10x YoY for all volume metrics. Brand is generally about 40-50% of our regs; is there an issue with categorization?
  * Also, Funnel completion rate is about 4x higher for each EU5 market vs. Brand, but should be similar to other markets, where Brand is at least about the same as the total funnel completion rate.
 * Why is PS Brand Registration Rate near 0% for EU Brand, but not for other markets?

|​|US|​|UK|​|DE|​|FR|​|JP|​|CA|​|IT|​|ES|​|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|​|Jan 2023|Jan 2024|Jan 2023|Jan 2024|Jan 2023|Jan 2024|Jan 2023|Jan 2024|Jan 2023|Jan 2024|Jan 2023|Jan 2024|Jan 2023|Jan 2024|Jan 2023|Jan 2024|
|New Paid Search Customer Traffic, Registration, Verification|​|​|​|​|​|​|​|​|​|​|​|​|​|​|​|​|
|Unique Paid Search MCS visitors|820,880|658,453|126,025|61,653|149,694|91,369|109,467|64,255|59,425|78,858|190,157|65,822|108,679|80,260|73,574|64,424|
|Unique Paid Search Brand MCS visitors|165,458|177,699|20,154|25,945|23,745|35,569|21,300|25,357|6|4,386|5,286|4,689|21,312|28,704|1,640|20,023|
|Total Unique Visitors to Registration Start (K)|127,352|114,343|27,506|15,198|30,589|24,543|24,950|16,705|9,188|12,204|34,359|33,286|51,778|50,874|39,894|19,249|
|PS Brand Unique Visitors to Reg Start|35,734|38,691|587|3,172|851|1,492|1,229|2,674|9,143|11,544|21,899|25,504|938|11|5|6|
|Reg Start % from MCS Visitors|-84.49%|-82.63%|-78.17%|-75.35%|-79.57%|-73.14%|-77.21%|-74.00%|-84.54%|-84.52%|-81.93%|-49.43%|-52.36%|-36.61%|-45.78%|-70.12%|
|Reg Start % from PS Brand MCS Visitors|-78.40%|-78.23%|-97.09%|-87.77%|-96.42%|-95.81%|-94.23%|-89.45%|152283.33%|163.20%|314.28%|443.91%|-95.60%|-99.96%|-99.70%|-99.97%|
|Total Started Registrations (Entered Email) (K)|80,422|73,000|15,530|9,534|14,933|14,782|15,005|10,914|4,358|7,005|15,803|17,037|24,879|27,545|19,249|11,538|
|PS Brand Started Regs (Entered Email)|22,766|27,790|88|1,108|14|562|71|214|4,339|6,760|7,450|12,062|59|6|2|1|
|Registration start % from total visitors to Reg Start|63%|64%|56%|63%|49%|60%|60%|65%|47%|57%|46%|51%|48%|54%|48%|60%|
|Reg start % from PS Brand to Reg Start|64%|72%|15%|35%|2%|38%|6%|8%|47%|59%|34%|47%|6%|55%|40%|17%|
|Submitted Registrations (Clicked Submit) (K)|39,372|35,093|6,612|4,159|5,507|5,149|6,334|4,264|2,307|3,371|5,685|4,936|6,724|5,231|3,948|2,920|
|Submitted Regs from PS Brand (clicked submit)|12,173|13,026|10|148|3|78|11|32|2,303|3,303|2,204|2,555|5|0|0|0|
|Funnel Completion Rate (Submitted / Entered Email)|49%|48%|43%|44%|37%|35%|42%|39%|53%|48%|36%|29%|27%|19%|21%|25%|
|PS Brand Funnel Completion Rate (Submitted/Entered Email)|53%|47%|11%|13%|21%|14%|15%|15%|53%|49%|30%|21%|8%|0%|0%|0%|
|Registration Rate (Submitted / Visitors)|4.80%|5.33%|5.25%|6.75%|3.68%|5.64%|5.79%|6.64%|3.88%|4.27%|2.99%|7.50%|6.19%|6.52%|5.37%|4.53%|
|PS Brand Registration Rate|1.48%|1.98%|0.01%|0.24%|0.00%|0.09%|0.01%|0.05%|3.88%|4.19%|1.16%|3.88%|0.00%|0.00%|0.00%|0.00%|
|New Verified Accounts (K)|37,964|32,600|6,317|4,000|5,105|5,200|6,204|4,400|1,517|2,300|4,507|3,600|6,740|5,700|3,973|3,100|
|New Verified Accounts from Reg Start|30%|29%|23%|26%|17%|21%|25%|26%|17%|19%|13%|11%|13%|11%|10%|16%|
|New Verified Accounts from Entered Email|47%|45%|41%|42%|34%|35%|41%|40%|35%|33%|29%|21%|27%|21%|21%|27%|

#### Paid Search Flow Conversion Rates
|**Flow CVRs - **Percentage moving further into flow|US|​|UK|​|DE|​|FR|​|JP|​|CA|​|IT|​|ES|​|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|​|Jan 2023|Jan 2024|Jan 2023|Jan 2024|Jan 2023|Jan 2024|Jan 2023|Jan 2024|Jan 2023|Jan 2024|Jan 2023|Jan 2024|Jan 2023|Jan 2024|Jan 2023|Jan 2024|
|MCS to Reg start|16%|17%|22%|25%|20%|27%|23%|26%|15%|15%|18%|51%|48%|63%|54%|30%|
|MCS to entered email|10%|11%|12%|15%|10%|16%|14%|17%|7%|9%|8%|26%|23%|34%|26%|18%|
|MCS to Submit|5%|5%|5%|7%|4%|6%|6%|7%|4%|4%|3%|7%|6%|7%|5%|5%|
|Reg start to entered email|63%|64%|56%|63%|49%|60%|60%|65%|47%|57%|46%|51%|48%|54%|48%|60%|
|Reg start to Submit|31%|31%|24%|27%|18%|21%|25%|26%|25%|28%|17%|15%|13%|10%|10%|15%|
|Entered email to Submit|49%|48%|43%|44%|37%|35%|42%|39%|53%|48%|36%|29%|27%|19%|21%|25%|
|Submit to Verified|96%|93%|96%|96%|93%|101%|98%|103%|66%|68%|79%|73%|100%|109%|101%|106%|

* UK and DE query-level data that breaks out Brand vs. NB for each market. ( [EU5 CVR investigation][6])
* EU5 Brand queries and AMZ queries shifting.

## March/April 2024 follow-up
### Latest analysis commentary:
* UK: Aside from the incrementality test period (Q2 '23), we continued to drive 25%-51% more clicks YoY. (Although Unique visitors saw a decrease in each quarter) From H1 to H2 of 2023, we went from negative YoY reg starts to +10% reg starts, even with the lower unique visitors, and although we went back to +27% reg start to submit in Q3, we dropped to +1% in Q4. (CVR dropped in Q4 when looking at clicks or within the reg process)
* DE: This market is more simple. Traffic was similar to UK, aside from Q2 (growth), and less volatility compared to UK for traffic. Reg volume went from positive to negative from H1 to H2, click CVR decreased for each quarter, and reg start to reg submit CVR actually went to -10% YoY as well.
### Hypotheses for possible causes:
#### Clicks are not being correctly attributed.
 * Our clicks increased up to 50% YoY in H2, but we saw negative growth in unique visitors. (Makes sense that it wouldn't match up 1:1, but we'd expect traffic to move in the same direction when comparing the Google platform and MCS/Adobe) The New Customer Funnel table shows this decrease in unique visitors from Paid Search.
#### Registration process friction.
 * If someone is starting registration, then they are likely not a current customer. We drove consistently higher YoY reg start volume in H2, but saw a decrease in "start to submit CVR" in YoY for Q4 for both markets. (The table below named 'UK/DE Brand Core (Exact match term [amazon business]' shows YoY to help adjust for seasonality)
#### Direct/Other/Untracked Onsite being misattributed.
 * Direct has seen irregular spikes and shifts in volume when looking at 2024 YoY registrations. (upwards of +500% in UK, and +790% in DE.) Details in "Paid Search compared to Direct" table below.
 * Direct/Other/Untracked Onsite are channels with no ref tag, or no indication that a user was referred from another channel, which could be a result of our preparation for the DMA legislation rather than actual increase of Direct traffic.
 * The section titled March registrations decrease below also details and shows data for marketing vs. non-marketing channels across EU5 markets for 2024 Q1 YoY, QoQ, and Projected performance of April 2024.
#### **UK/DE Paid Search compared to Direct (Hubble data)**
|YoY change - difference|W3|W4|W5|W6|W7|W8|W9|W10|W11|Total|
|---|---|---|---|---|---|---|---|---|---|---|
|UK Paid Search|837|987|1046|1400|1227|1235|1204|1130|1099|10165|
|PS YoY|-431|-473|-459|10|-196|-209|-288|-582|-574|-3203|
|UK Direct|447|918|910|1378|608|1064|2064|1794|1022|10205|
|Direct YoY|266|760|691|1128|314|726|1723|1360|593|7561|
|Total YoY|-165|287|232|1,138|118|517|1,435|778|19|4,358|
|​|​|​|​|​|​|​|​|​|​|​|
|DE Paid Search|1304|1193|1227|1300|1181|1253|1239|1239|1215|11151|
|PS YoY|101|-31|-66|27|20|137|198|-108|-87|191|
|DE Direct|319|553|804|361|1417|627|156|1680|1361|7278|
|Direct YoY|190|405|597|160|1250|488|25|1505|1198|5818|
|Total YoY|291|374|531|187|1,270|625|223|1,397|1,111|6,009|

Above table compares weekly Paid Search registrations to Direct registrations because of the up to 500% YoY growth for UK Direct, and 790% YoY growth for DE Direct.
There doesn't seem to be a correlation between the movements of paid search and direct, but the variation of direct registrations from week to week are irregular for that channel. (Direct is essentially a channel with no ref tag or indication that a user was referred by another channel, which could be a result of DMA rather than increase of Direct traffic.)

## **Q1 and April of 2024 - Marketing vs. non-Marketing channels within EU5**
#### WBR document - March 2024
_A broader hypothesis \(not proven or validated by ABMA\) is that DMA may have further limited our ability to attribute marketing spend. Two points to support this are 1\) The Marketing for EU5 has grown 4.7% YoY, and the Direct channel has grown 189% YoY as well, but other channels that use targeting have decreased \(Targeted Onsite -34%, Email -37%, Paid Search -17%, Paid Offsite -70%, Telemarketing -36%\). 2\) When comparing YoY change data from February to March for Marketing channels, they accelerated in the negative direction, while Direct/Unknown channels were either flat or increased. \(Onsite -79%, Email -60%, Paid Search -91%, Telemarketing -17%, Free Offsite -85%, Marketing EU5 Total -55%\) _

#### EU5 Hubble data - YoY Q1 and April
Below, Q1's regs were -19% YoY vs. +39% for Non-marketing channels. From the sub-category, it looks like this is mainly driven by Direct, Unknown, and Untargeted registrants. (pulled data from _abbd\_sandbox\_mktg.ab\_acq\_channel\_attr\)_
 * **Marketing**: Bounty and Affiliates, Email, Other Paid Offsite, Targeted Onsite, Telemarketing
 * **Non-marketing:**Direct, Free Offsite, Other, Unknown, Untargeted
* Below shows that Marketing channels (even when removing Paid Search, as I've done below), are down -19% overall, down across markets in Q1 and April, while Non-marketing channels are up 39% YoY, and up across markets. This seems to be a trend for each market, as well as a trend for each channel separately within the Marketing/non-Marketing groups.

||A|B|C|D|E|F|G|H|
|---|---|---|---|---|---|---|---|---|
|1|EU5 2024 Q1|Regs|QoQ|YoY|​|April projection|Regs|YoY|
|2|Total|293,908|-7%|4%|​|Total|94,946|5%|
|3|PS|72,627|-3%|-14%|​|PS|23,787|-10%|
|4|Marketing (no PS)|64,491|-27%|-19%|​|Marketing (no PS)|18,605|-27%|
|5|Non-marketing|155,245|6%|39%|​|Non-marketing|52,409|49%|

**Larger points/Actions from [Registration funnel Quicksight][11]:**
* CVR drop for Brand also seen on this Quicksight. (sending more traffic to reg start, seeing less regs)
 * Drop seems to be concentrated on Desktop traffic.
* Other/Free/Direct channel groupings. How are there more registrations vs. total traffic to reg start?
 * Other/Direct/Free Offsite Channel groupings in Quicksight; more reg starts than traffic. (Also separate channel by themselves)
* Direct channel in WBR doc. YoY growth looks normal for EU5, but not for UK/DE.
* Quick logic on how WBRs are pulled, so we can make sure Feature Registry is set up to capture correctly for Brand and NB.
 * How do we calculate WBR regs? Do we filter on both channel groupings and channel detail?
 * Paid Search Brand is within Paid Offsite grouping, and is not capturing all of Brand

## Appendix
#### Dec Only Deep Dive
* **UK**: UK Brand Core had competition from "[weareuncapped.com][12]" from week 12/10 to the end of the month. They had 32% IS, and overlapped with our ads, which increased CPCs by 45% and decreased our IS to 89%. This explains
* **DE**: DE was okay.
* **FR**: Most of the decline was inside of a campaign called GA 2 Generic AMZ. The term that caused this decline was "Amazon pro" (FR portal for resellers to sell Amazon devices.) This was a term that I added as a negative after researching, along with adding terms like "amazon business" which was also going into this campaign.
* **IT**: IT Brand regs decreased 20% YoY and NB increased 12%. One weird thing that caught my eye is that CPC decreased by 53% for Brand, but we actually kept normal IS and +15% clicks. This looks like CVR for IT given it's all Brand.
[1]: https://www5.an.adobe.com/x/5_18rxck
[2]: https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/36d03af5-8df3-4844-a8df-f13e6547ed6c/sheets/36d03af5-8df3-4844-a8df-f13e6547ed6c_34f2cc16-549f-4aa0-912a-049a18a00be3
[3]: https://quip-amazon.com/YAT9EAkZs9f
[4]: https://quip-amazon.com/blob/CTM9AAFeei5/c-ZdGqrn-6fjeEDgCrZgmg
[5]: https://quip-amazon.com/blob/CTM9AAFeei5/D9n1sYLTAk1_KMSj-LjPTA
[6]: https://quip-amazon.com/2z6gA6ye6t4R
[7]: https://quip-amazon.com/blob/CTM9AAFeei5/q6iG7ku8oQ1w5ON0kcDTiw
[8]: https://quip-amazon.com/blob/CTM9AAFeei5/z94NsxwN4chnTUYZmLjxiQ
[9]: https://quip-amazon.com/blob/CTM9AAFeei5/sCfRtrSv5GZtbnvn1WJbTg
[10]: https://quip-amazon.com/blob/CTM9AAFeei5/OGmk2zs3C_lsQ21vRBo56Q
[11]: https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/36d03af5-8df3-4844-a8df-f13e6547ed6c/sheets/36d03af5-8df3-4844-a8df-f13e6547ed6c_34f2cc16-549f-4aa0-912a-049a18a00be3?#
[12]: http://weareuncapped.com/
