---
audience: amazon-internal
creator: Richard Williams
doc_type: document
last_modified: 2026-04-02
mirror_date: 2026-04-10
owner: Richard Williams
quip_folder: .ABIX/AU
quip_id: JMZ9AAput1I
source_url: https://quip-amazon.com/JMZ9AAput1I
status: DRAFT
title: AU PS Launch
topics:
- australia
- abix
- paid-search
backfill_status: backfilled
---

# AU PS Launch

New Budget Allocation based on **$1,276,354****USD (gross budget)**
||A|B|C|D|E|F|G|H|I|
|---|---|---|---|---|---|---|---|---|---|
|1|AB AU  FINAL Budget Y25|Gross USD (Included  fees * taxes) from AU team|Gross AUD (Included fees * taxes) from AU team|Net USD Budget  (Platform Spend)|NET USD Budget in AUD|AMO Fee (USD)|VAT Taxes (USD)|Regs|CPA based on Net USD|
|2|June Actual|$108,693|$175,656|$97,047|$151,034|$1,941|$9,705|1,790|$54|
|3|July Actual|$228,040|$368,531|$203,607|$310,921|$4,072|$20,361|1,574|$129|
|4|August Actual|$247,803|$400,470|$221,253|$357,563|$4,425|$22,125|1,421|$156|
|5|Sept Actual|$225,092|$363,767|$200,975|$324,792|$4,020|$20,098|1,305|$154|
|6|October Actual|$201,581|$325,771|$179,983|$290,867|$3,600|$17,998|1,161|$155|
|7|November Actual|$184,415|$298,030|$164,656|$266,098|$3,293|$16,466|1,055|$156|
|8|December|$80,730|$130,465|$72,080|$116,487|$1,442|$7,208|456|$158|
|9|Total|$1,276,354|$2,062,690|$1,139,602|$1,817,761|$22,792|$113,960|8,763|$158|

July-Sept Brand & NB penetration- Brand 33.3%, NB 66.7%
## **Details**
* **Budget**: **$1.4M gross/$1.3M net \(media\) spend**
 * New Budget (9/8/25)- Total Y25 budget changed to **$1,299,192** (budget reallocated to Paid Media)
 * New Budget (11/13/25)- Gross Budget $1,299,191 USD- $22837USD= **$1,276,354 USD**
  * Need to reduce budget $**[22837.93224][1]******USD
* **PO Owner:** Stella (a week before launch- 5/20/25)
* **Goal**: **4.3K regs at $336 gross CPA/ $300 net CPA **
 * Detailed monthly budget/regs breakout in appendix 1.
* **Platform**: Google under AU non-hydra MCC
 * Google Payment Profile**\- **Same as other AU non-hydra accounts
* **Countries**: AU
* **Launch Date**:** 5/21/25 4am AEST**
* **URL:**[AU PS URLs][2], [Sheet1: MCS content check][3]
 * Yun provided the feedback for the PS URLs in the [Sheet1: MCS content check][3]
 * Next step: Harjeet to address the feedback and update the MCS pages
* **Marketing Review doc[AB\_AU\_MarOffsite\_Marketing\_Review.pdf][4]**
## Tactical Implementation
* **Platform ****Selection**: Google = 100%. Focus exclusively on Google, as it dominates the Australian search engine market with 92% market share, to ensure our funding is fully allocated to Google, following the same approach as Mexico.
* **PS Campaign Structure **
  * We will duplicate the existing Brand and Non-Brand (Product & Vertical) from the UK account with phrase and exact match targeting to start with. The Non-Brand keywords will have a stronger B2B focus to distinguish them from the consumer side. The team will implement the negative lists provided by the AU consumer PS team to avoid competition.
  * Campaign Type - Keyword only
  * Keyword theme- Brand & Non-Brand (Product & Vertical terms), Phrase & Exact Match only
   * AB Paid Search Keyword List- [Sheet1: AB AU KW\_1][5] & [Sheet1: AB AU KW\_2][6]
    * **AB AU team to review**
  * Ad Type -[ Responsive Search Ads][7]**\(AU team to review\)**
  * Ref Tag Structure: Replicating CA/MX PS ref tag structure
   * Structure Template: pd\_sl\_au\_CampaignTheme\_KeywordID at Keyword level
   * pd_sl_ is our paid search tracking code prefix for NA and expansion markets which is required
    * ex: pd_sl_au_brand_KeywordID
* **Tracking**
 * **AMO & WBR setup ABMA team- Kazuki Yoshida**
  * Yun synced with Kazuki, and will provide PS ref tag and Google Account name by 4/15
  * AU SIM- https://issues.amazon.com/issues/ABMA-8349
  * Communicated the below logic with ABMA for reporting
  * For the ref tag- we will use similar structure like MX but replace MX with AU and the logic should be similar.
   * Brand: ref tag contains **pd\_sl\_au\_brand**
   * Non-Brand: ref tag contains **pd\_sl\_au but doesn't contain Brand**
  * Location in Feature Registry: Amazon Business - Registrations > Offsite - Search (Paid)
  * [MX example- https://issues.amazon.com/ABMA-5891][8]
* **Bidding Strategy**
 * Brand - Target Impression Share to to fully saturate branded traffic (expected to be low due to low awareness)
 * Nonbrand - Will use G ads' Max Clicks to start with. Then we will jusifiy the performance to switch over to AMO bidding and optimize the CPA targets based on the data.
* **Central ****Team Alignment: **For non-brand terms, our strategy is to focus on B2B-related phrase and exact terms. The AB PS team will share the non-brand keyword list with the AU Central PS team 2 weeks before May 20. Additionally, the AB PS team will implement the account-level negative lists from the AU Central team to avoid any potential overlap. Furthermore, the AU AB launch will utilize only keyword campaigns (no shopping campaigns), eliminating any competition concerns with AU Central team's shopping ads efforts.
 * **MX AB PS launch impact**- The impact has been minimal, primarily due to AB PS budget comprising only 2% of total AB retail keyword advertising spend, which significantly reduces potential market disruption. Performance metrics show that MX retail keyword CPC has maintained stability throughout 2024, with no unusual fluctuations or competitive bidding patterns detected. Notably, auction insights data for MX AB PS keywords shows no a.com presence, indicating no cross-border competition, advertising space overlapping issues, or market cannibalization concerns. Given the healthy market dynamics with predictable bidding patterns and clear market segmentation between platforms, the launch appears to have been successfully implemented without disrupting existing advertising operations.
* **Account: **The AB AU account will host under our AU Non-Hydra MCC (127-973-4666) to apply AU payment profile to avoid any disruption regarding of payment
 * Account payment profile -Based on MX and EU5 experiences, the payment profile must match the regional central team's profile due to taxation requirements.
  * AU central team confirmed that the payment profile is 4609-2467-5670
* **Event Promotion: End of Financial Year**
 * Bid on: end of year budget, end of financial year, end of year savings and year end budget keyword during event period
  * [AU Target EOFY keywords][9]
 * Ad Copy Messaging- [AU RSA Ads][10]
 * Ads & sitelink Landing page-https://www.amazon.com.au/business/register/org/landing
 * Time: 5/21/25-6/30/25 AU Time
* **Sitelink:**
||A|B|C|D|
|---|---|---|---|---|
|1|Link Text- Character Limit- 25|Desc 1 - **Character Limit- 35**|Desc 2- **Character Limit- 35**|AU URL|
|2|Exclusive EOFY Savings|This year's savings,|next year's success. Join now.|https://www.amazon.com.au/business/register/org/landing|
|3|Business Prime Free Trial|Fast and free delivery.|Exclusive business only pricing.|https://business.amazon.com.au/en/find-solutions/business-prime|
|4|Register Now|Create a free business account.|The smart way to business savings.|https://business.amazon.com.au/en/register|
|5|Business Solutions|Save time & money.|Tens of millions of items.|https://business.amazon.com.au/en/work-with-us/small-business|
|6|Features & Tools|Multi-user account.|Guide your team's spends.|https://business.amazon.com.au/en/find-solutions|

## Timeline
||A|B|C|D|E|
|---|---|---|---|---|---|
|1|Item|Owner|Status|Date|Note|
|2|Create Google Ads account|Yun|Completed|3/31/2025|​|
|3|Google PO- Need to provide PS team the PO# before the campaigns launch|[][11][Stella \[C\] Foong][11]|Completed|Before 5/16/2025|#HA-17346478|
|4|Provide ABMA ref tag structure/ G ads account name for reporting|Yun|Completed|4/2/2025|​|
|5|Adobe Sync|Yun|Completed|4/15/2025|​|
|6|Yun to review PS MCS pages|Yun|Completed|​|Feedback provided in the   [Sheet1: MCS content check][3]|
|7|Provide AU version URLs|Harjeet|Completed|4/30/2025|Yun provided the feedback for the PS MCS pages in the  [Sheet1: MCS content check][3]. Harjeet to have the pages updated based on the feedback|
|8|Review AU Ads -[Sheet1: AU RSA Ads][12]|Lena/Stella|Completed|4/11/2025|​|
|9|AU team to privide promo message for ads|Lena/Stella|Completed|4/30/2025|​|
|10|AU PS central team to provide negative KW lists|Harsha|Completed|4/30/2025|​|
|11|Implement negative keyword list from AU central|Yun|Completed|5/9/2025|​|
|12|Campaign Build|AB PS Team|Completed|5/12/2025|​|
|13|Soft Launch|AB PS Team|​|5/20/2025|​|
|14|Include AU in PS weekly dashboard|Stacey|​|​|​|

## Appendix
**Appendix 1- Forecast Monthly Budget & Regs -Gross budget= 10% VAT fee on top of the Net Budget \(media spend\)**

**Budget & Actual- All in USD based on $1,459,000 Gross USD - Original Budget**
||A|B|C|D|E|F|G|
|---|---|---|---|---|---|---|---|
|1|AB AU  FINAL Budget Y25|Gross USD (Included  fees * taxes) from AU team|Gross AUD (Included fees * taxes) from AU team|Net USD Budget  (Platform Spend)|NET USD Budget in AUD|AMO Fee (USD)|VAT Taxes (USD)|
|2|June Actual|$108,693|$175,656|$97,047|$151,034|$1,941|$9,705|
|3|July Actual|$228,040|$368,531|$203,607|$310,921|$4,072|$20,361|
|4|August Actual|$247,803|$400,470|$221,253|$357,563|$4,425|$22,125|
|5|September|$232,346|$375,490|$207,452|$335,259|$4,149|$20,745|
|6|October|$232,346|$375,490|$207,452|$335,259|$4,149|$20,745|
|7|November|$217,806|$351,992|$194,470|$314,278|$3,889|$19,447|
|8|December|$191,966|$310,232|$171,398|$276,993|$3,428|$17,140|
|9|Total|$1,459,000|$2,357,861|$1,302,679|$2,081,307|$26,054|$130,268|

**Appendix 2- Paid Search Ads example \(US example\)**
![image.png][13]​
[1]: tel:2283793224
[2]: https://quip-amazon.com/tjd0AJLC6Xjg
[3]: https://quip-amazon.com/nHvRAF25MnQt#temp:C:Vac198fc2a980d04dfca1722a30c
[4]: https://quip-amazon.com/-/blob/JMZ9AAput1I/AmNFuM3rcKKnzNP3Y7Qkiw?name=AB_AU_MarOffsite_Marketing_Review.pdf
[5]: https://quip-amazon.com/VAEmA2u8XY7d#temp:C:UEG9c7c4b792b6d479badaade7d9
[6]: https://quip-amazon.com/Y7EkA19VAtG9#temp:C:AdZce08a9f0bf4d4856a4340788c
[7]: https://quip-amazon.com/OahhAATttFQ1/Untitled#temp:C:RRcb893868b47dd4695901669ef3
[8]: https://issues.amazon.com/ABMA-5891
[9]: https://quip-amazon.com/Acd0AZ0KVzg8/Untitled#temp:C:PUD9a21d73fd46e4b8ba7ce094a0
[10]: https://quip-amazon.com/OahhAATttFQ1/AU-RSA-Ads#temp:C:RRcb893868b47dd4695901669ef3
[11]: https://quip-amazon.com/CWb9EAn2ENP
[12]: https://quip-amazon.com/OahhAATttFQ1#temp:C:RRcb893868b47dd4695901669ef3
[13]: https://quip-amazon.com/blob/JMZ9AAput1I/SE0nnWkjmg--hZtYzdm-NA
