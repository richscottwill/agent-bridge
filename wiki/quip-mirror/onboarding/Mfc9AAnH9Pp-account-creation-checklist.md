---
audience: amazon-internal
creator: Richard Williams
doc_type: document
last_modified: 2026-01-20
mirror_date: 2026-04-10
owner: Richard Williams
quip_folder: Onboarding/Account Best Practice
quip_id: Mfc9AAnH9Pp
source_url: https://quip-amazon.com/Mfc9AAnH9Pp
status: DRAFT
title: Account Creation Checklist
topics:
- onboarding
- best-practices
- account-management
backfill_status: backfilled
---

# Account Creation Checklist - Paid Acquisition
Write about in more detail with step-by-step/links:
* Create within market-level Non-Hyda MCC, and steps for ticket to Emily’s team, and applying PO.
* Because of OCI, we will need to create an associate tag and append to Final URL suffix.
 * Reftag construction (limitations due to char limit and taxonomy for reporting)
  * NA: ref=pd_sl...kwID_MTAdGID
  * EU5: ref=b2b_reg_search...kwID_MTAdGID
  * JP: ref=JP_AB_PSA...kwID_MTAdGID
 * Append "&ps_kw={keyword}" (update when this is solved)
* Adobe (eventually legacy) tracking

## Appendix
### Tracking Template Changes
* URL Construction: https://na.amazon-value-service.com/cl/v1/p/BSQ1ZjkFy2M2q-R5Vhq2HzSs5l2d8ndQPn0KMtF79_ieEA?lp={lpurl}&vscl={gclid}&vsco={gbraid}
 * Portfolio Tag |
* Suffix Construction: hvocijid={random}-{extensionid}&hvexpln=ssrText&ps_kw={keyword}&tag=abpsgglacqus-20
 * OCI pieces | powers Guest AB-shopping searches | Associate Tag
* URL Details:
 * Portfolio tag (long string in URL) available here: [Link][1]
  * Note that each Market has a unique Portfolio tag

### FAQs:
* Can we open a PO in local currency (ie, JPY/MXN)?
 * **Is there any issue with using an MXN purchase order to pay a USD invoice?**
  * If there is an issue with paying for a USD invoice with MXN?
  * The currency setting cannot be changed in Google Ads, so if we need to switch to MXN currency due to PO and invoice currency mismatch, we would need to set up a brand new account, which would lose all valuable historical data.
 * If there is no issue and we can use an MXN purchase order to pay a USD invoice, then the exchange rate used when opening the PO is very important (Google invoices use a dynamic FX rate). If there is any significant change in the exchange rate, that will impact the amount we can utilize in USD.

[1]: https://w.amazon.com/bin/view/AAHydra/OCI/CIT/Dashboards/Prod-EU/PortfolioLevel/
