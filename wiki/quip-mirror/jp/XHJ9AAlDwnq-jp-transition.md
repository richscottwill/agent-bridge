---
audience: amazon-internal
creator: Richard Williams
doc_type: document
last_modified: 2025-04-01
mirror_date: 2026-04-10
owner: Richard Williams
quip_folder: ..JP
quip_id: XHJ9AAlDwnq
source_url: https://quip-amazon.com/XHJ9AAlDwnq
status: DRAFT
title: JP Transition
topics:
- japan
- paid-search
backfill_status: backfilled
---

# JP Transition
## **Important POCs**
||A|B|C|D|
|---|---|---|---|---|
|1|**Name**|**Email**|**Role**|**Tasks**|
|2|Fernando Ramirez|[framirez@amazon.com][1]|Director, SSR|Leads SSR, and WBR calls|
|3|Ken Inouye|[kinouy@amazon.co.jp][2]|Head of JP SSR|Leads the local JP team|
|4|Minami Matsushima|[shimamin@amazon.co.jp][3]|JP Marketing Manager|Acquisition lead, on-site events|
|5|Mao Nagaya|[ngymn@amazon.co.jp][4]|JP Marketing Manager|Telemarketing, Activation, Paid Search support (translations, Percolate, PO creation, etc)|
|6|Google Account management|N/A|N/A|We don't have dedicated local support in the same way EU and NA have it.|
|7|David Iwano|[mandas@amazon.com][5]|Account Manager|Yahoo Account management|
|8|Haruka Taylor|[haruka.taylor@yahooinc.com][6]|Yahoo! JP Creative Strategist|Monthly  catch ups, deep dives|
|9|Sey Fujino|[seyfuji@amazon.co.jp][7]|CPS  contact|He used to lead the local JP team (Ken's current role), so he understands the local market very well.|

## **Important Documents**
**Documents are within Paid Acq Quip, in the JP folder**
* **Previous tests**: [JP Testing][8]
* **Important Market context \(Nonbrand, JP competitors, and previous tests\): [JP Paid Search Competitive Analysis][9]**
* **[JP Holidays][10]**
* WTS: [JP+PS+WTS+07.18.24.docx][11]
## **JP Campaigns: **
#### **1) Campaign structure: **
* Brand\_Exact
 * Core keywords like "amazon business"
* Brand\_Phrase
 * Desktop and Mobile campaign. Split because of the major difference between the two groups.
 * Bid strategy is Portfolio bid strategy, so that all phrase campaigns are together. (conversions assessed together)
* Brand2 campaigns
 * Brand2_Scene contains Invoice campaign, which has seen a recent spike in traffic/interest.
* Nonbrand
 * Pmax and Discovery come with a decent CPA ($40-$100 CPA), although very low reg volume. These campaigns supplement overall regs. (Very sensitive to bid strategy changes. Shifts traffic volume heavily.)
 * We've tested NB keywords multiple times in the past, but they ended up performing at about $1k CPA. (JP testing docs within JP Quip folder)
 * Percolate and Guest experience will be our focus to build our NB campaigns. We've done NB testing in the past (view test documents and competitive analysis doc in JP Quip folder)
  * Percolate: waiting for Mao to confirm ASINs, and Chetan's approval to launch. NB keywords can be confirmed with the JP team. (We had a short list of NB keywords approved with them, but may want another discussion to see if we could expand the keyword list to product keywords as well)
#### **2) Bid strategies:**
* Brand_Exact optimizing towards Impression Share.
* Brand_Phrase campaigns optimizing for conversions.
* Want to keep Brand_Exact maximized as that's where the majority will come from, and work within the other campaings to optimize further.
#### **3) Reporting:**
* Aggregated data: Adobe Advertising Cloud (AMO) for combined data, or to see spend penetration/directional reg penetration.
* In-depth: Within platform is the best way to view across different paid search cuts of data such as by device, audience, search query, etc.
* Registration tracking between platforms or across different keywords should be pulled via Hubble.
#### **4) Tracking:**
* Attribution: First-touch attribution model, but Mauro talked about moving all WW markets to multi-touch.
* JP tracking (Example ref tag): JP_AB_PSA_G_BRP_302379924678
 * (1) Country code
 * (2) Amazon Business
 * (3) Paid Search
 * (4) Google or Yahoo
 * (5) Campaign type (BRP is Brand Plus, other examples are Brand, NB, Discovery, Pmax, etc
 * (6) Keyword ID
#### **5) Events/Localization:**
* From time to time, we support events that the JP team are running. We generally support with sitelinks, callouts, or promo extension depending on the event.
* For localization, I have generally tried to translate by coming up with english copy myself, then using a few translate software to come up with translations, and emailed the best ones to Mao to see if she had any edits she wanted to make, or to come up with text herself using that as a guide.
* You could also work with Mao/Minami during the event planning process to formally request translation via their agency.

## **Qs**:
* Does ref tag Pmax, DA = NB; kronos, prime = brand?; others?
 * Yep the above is correct. Brand will generally contain brand or kronos, and NB will usually not contain those.
* Why does JP got the most Reg in this doc? [JP Paid Search Competitive Analysis][9]
 * If you're referring to the bar charts at the bottom, those show the total number of CPS registrations, and there are probably two things contributing:
  * They might label CPS differently from others in terms of revenue, so they've got a higher volume.
  * Another thing that helps is that we send paid search traffic to the [callback page][12], where users can fill out a form, and maybe CPS customers are identified more often because of this.
* Weekly traffic, regs, cost, CVR? yearly trend?
 * This is something that's based on the time of year, and can be found within Stacey's dashboard. There are a couple periods of time where we saw bigger changes though, and YoY growth might be a bit harder. (hopefully not)
 * **Efficiency starting April 2023**: We saw YoY CPAs drop by 30%-70% from April 2023 to around June 2023 because of the optimizations to consolidate search queries, add negatives, and prioritize budgets more effectively.
 * **Registration volume jump in Sept/Oct**: Regs have been up above 100% YoY since October, which is likely a combination of efficiency within the account, allowing us to capture the increase in interest that we have seen since that time.
* Does JP have any naming convention rule for campaigns? If so, who is the contact?
 * We create the naming conventions in terms of the platform structure and the ref tags, but if you wanted to expand on keyword lists or help with organizing keywords, Mao would likely be your best bet for help on this.
* Verification rate?
 * Verification rate has been around 35%-40%, which is good compared to other regions.
* Does pmax and discovery use ref tag in AMO? didn't see conversion in AMO
 * You can see the conversions if looking at Registration Pending + Complete, but not the Registration Japan V2
* DSA? certain page might work but as a whole AB site
 * We haven't tested DSA, but it was something I was interested in in the past. Might work if you create segments using the site nodes (the more important sites when you look at the navigation bar on the site.)
Notes:
No Google rep
How many KWs for B2B and core brand, and what's the KW penetration?
Prioritize Desktop
Portfolio bidding changed in late Dec
Yahoo are all AVT, not in brand in Google
JP-ENT-BP_Weekly is the report Richard use
Use brand for promo keywords
Separate Phrase_D from portfolio bidding, IS too low
Minami: Acquisition Mao: Activation

Jan 18, 2024
JP_Brand2_Scene is AMZ
We can not bid on 'amazon paper' but we can bid on 'amazon paper bulk' or 'amazon business paper wholesale"
AVT only in Yahoo not Google
Phrase and broad in Yahoo? Scale is smaller in Yahoo so we could use broader match like broad and phrase.
We can't bid on product keywords with ASIN. No list to look up. If need to run non-brand, send to Mao to QA.
Saw large traffic came from invoice terms in Oct that's why we have Invoice campaign.
In AA free search = SEO
Richard worked on ETA>RSA, PMax, Ad copies
Update image extension, ask Brandon if we want to use dynamic image extension to improve CTR and quality score?
Test category for NB from file "JP Data wholesale"
[1]: mailto:framirez@amazon.com
[2]: mailto:kinouy@amazon.co.jp
[3]: mailto:shimamin@amazon.co.jp
[4]: mailto:ngymn@amazon.co.jp
[5]: mailto:mandas@amazon.com
[6]: mailto:haruka.taylor@yahooinc.com
[7]: mailto:seyfuji@amazon.co.jp
[8]: https://quip-amazon.com/sRjNOLnBdTqM
[9]: https://quip-amazon.com/oerFAFI2DXDR
[10]: https://www.timeanddate.com/calendar/?country=26
[11]: https://quip-amazon.com/-/blob/XHJ9AAlDwnq/-FlpUMZJ69Uw4E_m8xkw9w?name=JP%2BPS%2BWTS%2B07.18.24.docx&s=QPHFAKp64x2j
[12]: https://business.amazon.co.jp/ja/campaigns/callback?ref=JP_AB_PSA_G_BR_MT_333073976379
