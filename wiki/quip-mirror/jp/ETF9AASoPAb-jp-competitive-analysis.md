---
audience: amazon-internal
creator: Richard Williams
doc_type: document
last_modified: 2025-04-07
mirror_date: 2026-04-10
owner: Richard Williams
quip_folder: ..JP
quip_id: ETF9AASoPAb
source_url: https://quip-amazon.com/ETF9AASoPAb
status: DRAFT
title: JP Paid Search Competitive Analysis
topics:
- japan
- paid-search
backfill_status: backfilled
---

# JP Paid Search Competitive Analysis
### **1. Why is Nonbrand not working in JP? What is the difference with other countries? **
* Cultural**:** According to Google Trends and the survey conducted by the JP Team (Appendix 1 and 2), AB faces issues of low brand awareness within JP. AB has < 85x the search volume as Monotaro and <77x search volume as Askul which is significant compared to the US (3x difference vs. Grainger). Additionally, B2B customers in Japan prefer in-person (or over the phone) interaction before finalizing key business decisions, which can also be supported by receiving 1.8k requests with 31% conversion rate after adding the Contact Us Form on the PS landing page since Wk16. In general, decision makers in JP also skew older (34-54) compared to EU (25-34) and prefer a longer, more traditional decision-making process.
* Value**:** According to Google studies, JP businesses over-index on competitive pricing when purchasing for business. While AB does offer business discounts, pricing is not visible to customers prior to registration. This is in contrast to markets in EU (where nonbrand was able to scale to ~60% of registration volume) such as IT and UK, where feature benefits such as pay by invoice and VAT processing are highly valued.
* Website experience**:** US & EU competitors offer similar website experiences to our JP competitors, but these websites do not always highlight pricing advantages as clearly as our Japanese competitors (missing price strikeout, limited-time discounts, and customer reviews).
* AB Market Performance \(1H-2022: JP vs. NA & EU5\):
 * JP Brand: CTR is healthy (on par with NA), but CVR is 50% lower than EU, and CPA is higher vs. both regions (+66% NA and +170% EU.) This may indicate that the landing experience isn't ideal, as high intent searchers abandoned before registering.
 * JP Nonbrand: CTR is 36%/50% lower than NA/EU, and this shows low/moderate interest. However CVR is the source of abandonment as it is 93% lower than EU and 96% lower than NA; the lowest of any individual country (ES is 2nd with .8% CVR, ~9x JP). This also reflects in CPA, which is 5x higher than NA and 8x higher than EU. Given users are choosing to visit the site prior to abandoning, this might point to on-site experience needing improvement.
 * ![image][1]
### **2. What is the difference with our competitors (i.e. MonotaRO, Askul)?**
* Business Approach: MonotaRo and Askul have high market share and brand recognition in JP.
 * MonotaRo (2021 goal: 6.9M customers, $1.63 Bn USD sales): MonotaRo actively spends on TV with the slogan of "creating value for underserved small businesses" and "fight against old, unfair distribution system". They spend a lot on product-level Nonbrand keywords (listed as #1 Acquisition channel) to drive registrations but still keeps up with traditional mediums such as catalogues, faxes, and flyers. They have 3 customer sales support team under their marketing department to service current and new customers.
 * Askul (2021 goal: $3.67Bn USD in sales): Similar to MonotaRo, Askul lists catalogue as a top sales driver (80% of total B2B sales). In their investor update, they discussed the value of partnering closely with agents to drive sales. While they heavily invest in digital marketing, they've attributed their growth on successful partnerships with agents.
 * Overall:
* Website Experience: MonotaRO & Askul - Appendix 3, AB JP - Appendix 4
 * MonotaRO and ASKUL have similar approaches in their marketing purchase path. If searching for office supplies, the Google ad takes you to a page that shows office supply products with prices and item details where you're able to filter to something more specific. The user can also perform a search for and add any other relevant products to the cart. ASKUL prompts for registration when user adds an item to the cart, but MonotaRO allows visibility and modification of the cart, prompting for a registration when beginning the purchase process.
 * Overall: While both competitors require registration, AB is the only site to require registration prior to viewing products.
||A|B|C|D|
|---|---|---|---|---|
|1|​|MonotaRO|ASKUL|Amazon Business|
|2|Product information (Pictures, introductions, pricing...etc)|Yes|Yes|No|
|3|Relevant Product listing and comparison|Yes|Yes|No|
|4|Advanced search capability|Yes,  filters and search bar to refine|Yes,  filters and search bar to refine|No|
|5|Add to/view cart before login/registration|Yes|No,  adding to cart prompts registration|No|
|6|Purchase without Registration|No|No|No|

### **3. What other factors should be considered?**
* Kw Restriction: JP cannot bid on product only keywords, currently restricting solely to keywords with B2B modifiers.
 * JP Modifiers Used:
  * 事業用  For business
業務用  For business
仕入れ  Purchase
まとめ買い  Bulk buying
大量購買  Bulk purchase
卸売  Wholesale
法人向け  For corporate
法人購買  Corporate purchase
セット販売  Set sale
### **4. What solutions have been tested?**
Paid search team conducted 4 NB tests from Oct 2022 to 2024. The tests were not successful because of limited scale and high CPA in JP market. Discovery campaign and PMax campaign continue to run as NB test in 2024.
* [JP NB Experiment][2] (Oct '22 - Jan '23): Tested in Yahoo on Oct 2022 for office, automotive, healthcare, industrial and general NB KWs. Result: Overall CPA at $1,457 with 9 registrations. The test was not successful because NB audiences are limited and the CPA is too high.
* [JP NB Experiment 2][3] (Jan '23 - Apr '23): Tested in Google on Jan 2023 for "purchase", "wholesale", "bulk" and "corporate" related KWs in partnership with JP team to hand-select high intent terms. Result: 8 registrations at a $1,028 CPA. The test was not successful as the CPA is too high and the KWs we can bid on are limited. ([Appendix 6][4])
* Discovery (Apr '23 - Ongoing): 31 registrations at a $410 CPA. The CPA is a lot better compared to the keyword-based tests above but the scale is too small where we can only spend $30 USD per day. The campaign is targeting users who are interested in Amazon Business or JP AB website, B2B terms, competitors' B2B terms, and medium and large companies.
* PMax (Sept '23 - Ongoing): 47 registrations at $453 CPA. Higher volume than Discovery, but CPA is still too high compared to other markets. Audience targeting 1. Users who are interested in 'Amazon Business' keywords 2. Users who browse websites similar to business.amazon.co.jp. For business buyers, the ad group also targets custom customer lists and B2B modifier KWs in addition to the audiences above. The CPA is at $284 in Feb compared to $1,008 in Jan after we added a CPA cap of $300 on 1/22.
Next solution to test:
* Percolate/Guest
 * Percolate Example: Q1, 2024
  * Seen here: https://business.amazon.com/en/find-solutions/simplify-buying/selection/wholesale.
  * ![image.png][5]
 * Guest Account Example: Q4 2024
  * Allow users to fully browse AB store prior to completing registration and verification, just name, verified email, and password required.
  * ![image.png][6]
* Google AVT
* Website Parity to include all categories such as Apparel
### **Appendix**
**Appendix 1**: Google Search Trend Report (Past 12 months)
Search done in Japanese:
![image.png][7]Search trend for JP AB Business Image competitors. (Updated on Feb 8, 2024)
![Capture.PNG][8]**Appendix 2:** March 2022 Brand Survey
![image.png][9]​

**Appendix 3**: MonotaRO and Askul Paid Search Experience

3.1 Google Search Results of Copy Paper:[
コピー 用紙なら - 【モノタロウ】公式通販サイト ][10]is a paid search ad from MonotaRo[
コピー用紙ならアスクル - アスクル法人向け公式サイト][11] is a paid search ad from Askul
![image.png][12]3.2 MonotaRO Paid Search Landing Page (https://www.monotaro.com/s/q-%E3%82%B3%E3%83%94%E3%83%BC%20%E7%94%A8%E7%B4%99/)
![image.png][13]3.3 Askul Paid Search Landing Page (https://www.askul.co.jp/f/copy/copy00/)
![Askul.PNG][14]**Appendix 4**: Amazon Business JP Paid Search Experience

4.1 Google Search results of Amazon Business:
![image.png][15]4.2 AB Paid Search Landing Page (https://business.amazon.co.jp/ja/campaigns/callback)
![image.png][16]​
**Appendix 5**
CPS, All HQ, by market, YTD
![image.png][17]CPS, New HQ, by market, YTD
![image.png][18]CPS, New HQ registrations, by market, YTD
![image.png][19]**Appendix 6**

JP NB 2023 test keywords list:
||A|B|C|D|
|---|---|---|---|---|
|1|Keywords|Translation|Match Type|Query Example|
|2|"まとめ買い"|"bulk buy"|Phrase Match|bulk buy business|
|3|"仕入れ"|"Purchase"|Phrase Match|Resale Purchase|
|4|"卸売"|"Wholesale"|Phrase Match|wholesale business|
|5|"大量購買"|"bulk  buying"|Phrase Match|business bulk buying|
|6|"業務用"|"For  business"|Phrase Match|bulk order for  business|
|7|"法人向け"|"Corporate"|Phrase Match|corporate order|
|8|[せどり 仕入れ  ランキング]|[Sedori purchase  ranking]|Exact Match|Sedori purchase  ranking|
|9|[せどり 仕入れ 先]|[Sedori supplier]|Exact Match|Sedori supplier|
|10|[ネット ショップ 開業  仕入れ]|[Online shop opening  purchase]|Exact Match|Online shop opening  purchase|
|11|[まとめ買い]|[Bulk purchase]|Exact Match|Bulk purchase|
|12|[仕入れ サイト]|[Purchase site]|Exact Match|Purchase site|
|13|[仕入れ]|[Purchase]|Exact Match|Purchase|
|14|[卸売 業]|[Wholesale]|Exact Match|Wholesale|
|15|[卸売]|[Wholesale]|Exact Match|Wholesale|
|16|[業務用]|[For business]|Exact Match|For business|
|17|[物販 仕入れ]|[Product sales  purchase]|Exact Match|Product sales  purchase|

**Appendix 7 **
JP Pmax Lift Experiment: September 2023 to November 2023 (Currently active)
Converted Pmax into a 6 week lift test within Google, and defined the Discovery and Brand keyword campaigns as campaigns that may overlap. Google split Pmax traffic 50/50 and goal was to determine the incremental lift of Pmax; test concluded Week 42. (Asset groups created - 'Brand' asset group, 'medium-large business' asset group, and 'business buyers' asset group.)
**Results**: After 6 week lift test on Google, Treatment group "Pmax + all other brand campaigns" led to 8% more conversions and 20% more cost, compared to the control group, which received no Pmax ads. This translates to $75 CPA on the increase in conversions. (Acceptable for incremental registrations) Google positions the results as, "Adding Pmax ads to your mix of ads will result in +8% incremental conversions overall, with a 12% higher CPA." Actual CPA of Pmax was $375 (database regs) I implemented Pmax, and continued to optimize CPA.

JP Discovery Ads: April 2023 to Current

**Appendix 8**

[AWS JP data][20]
[1]: https://quip-amazon.com/blob/ETF9AASoPAb/DDQBjk62743riUksb5yvfA
[2]: https://quip-amazon.com/m60jAiy6lCMx/202210Yahoo-JP-NBExperiment
[3]: https://quip-amazon.com/ZWyXARUkqszA/202301JP-NBExperiment-Doc
[4]: https://quip-amazon.com/oerFAFI2DXDR/JP-Paid-Search-Competitive-Analysis#temp:C:ETFd5c3164866e7472b89c916071
[5]: https://quip-amazon.com/blob/ETF9AASoPAb/CAz6kOmBcEMqMGWZG3g3GQ
[6]: https://quip-amazon.com/blob/ETF9AASoPAb/Rz0zm_fIEzYvmCAlZCVirg
[7]: https://quip-amazon.com/blob/ETF9AASoPAb/igPccsfeYfLQ2FaUgV2ixg
[8]: https://quip-amazon.com/blob/ETF9AASoPAb/3qWxsUOoEJkE3uKIqGpwsw
[9]: https://quip-amazon.com/blob/ETF9AASoPAb/UAl7qVd-wtPSdjsGkxZyYw
[10]: https://www.google.com/aclk?sa=l&ai=DChcSEwi2gPrlnZ77AhWPiMIKHYzKBHwYABARGgJ0bQ&sig=AOD64_26djNkoB69fjTP467FQaowW8ST6w&q&adurl&ved=2ahUKEwiy1PPlnZ77AhWYqlYBHf81AT0Q0Qx6BAgGEAE&nis=8
[11]: https://www.askul.co.jp/f/copy/copy00/
[12]: https://quip-amazon.com/blob/ETF9AASoPAb/MHxpOLPTMFC5zL_-qzqAnQ
[13]: https://quip-amazon.com/blob/ETF9AASoPAb/oY9xsYDcJGHHkaW1r4djMQ
[14]: https://quip-amazon.com/blob/ETF9AASoPAb/ixTGaI_94boe-iBYNfMdxw
[15]: https://quip-amazon.com/blob/ETF9AASoPAb/TAKlRDSrk3I9KMU4H3lDtA
[16]: https://quip-amazon.com/blob/ETF9AASoPAb/DlR2owjH7iIbco96C1vcEw
[17]: https://quip-amazon.com/blob/ETF9AASoPAb/SwD_hQwTX3QXZ6fM7fWvGA
[18]: https://quip-amazon.com/blob/ETF9AASoPAb/75o32foq1kQUaKmM2sxcqg
[19]: https://quip-amazon.com/blob/ETF9AASoPAb/oXEHQ4zhAvSmLrpep9uG1g
[20]: https://amazon.awsapps.com/workdocs-preview/index.html#/document/dff0d749e567b92b899eee136b03743c397e37f7572dc738dc69e502ed53d432
