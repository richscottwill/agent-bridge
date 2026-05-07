---
audience: amazon-internal
creator: Richard Williams
doc_type: document
last_modified: 2024-08-28
mirror_date: 2026-04-10
owner: Richard Williams
quip_folder: Onboarding/Data
quip_id: ISQ9AAo3soI
source_url: https://quip-amazon.com/ISQ9AAo3soI
status: DRAFT
title: AB Channel Marketing - SQL Databases & Queries
topics:
- onboarding
- data
- analytics
backfill_status: backfilled
---

# AB Channel Marketing - SQL Databases & Queries
## Data Table Reference
|​|​|​|**Common AB Fields** - These fields are commonly used to join different data sources at AB. If a specific field exists in two tables, it can be used to join the data from those tables (e.g. **m\_ab\_prime\_bps\_signups** and **d\_ab\_business\_accounts** can be joined using **business\_account\_id** since it exists in both tables)|​|​|​|​|
|---|---|---|---|---|---|---|---|
|Category|Table Name|Use Case|AB Account ID (BAID)|Salesforce Lead/Contact ID|MCS Visitor ID (Adobe ECID)|A.com Clickstream ID (Session ID)|Field Reference|
|AB Accounts - EU5|abbd_sandbox_intl.ab_eu_acq_credited_attribution|EU5 account flat table includes business account id, verifcation status, channel attribution credits, etc|business_account_id|N/A|N/A|N/A|[https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd\_sandbox\_intl.ab\_eu\_acq\_credited\_attribution][1]|
|AB Accounts - JP|abbd_sandbox_mktg.jp_acq_channel_attr|JP account flat table includes business account id, verifcation status, etc|business_account_id|N/A|N/A|N/A|[https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd\_sandbox\_mktg.jp\_acq\_channel\_attr][2]|
|AB Accounts|abbd_dtl.d_ab_business_accounts|AB account details including customer ID, verification status, business/revenue tier, etc.|business_account_id|N/A|N/A|N/A|[https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd\_dtl.d\_ab\_business\_accounts][3]|
|Business Prime|abbd_dtl.m_ab_prime_bps_signups|BP subscription details including sign-up channel, ingress, plan type, etc.|business_account_id|N/A|N/A|session_id|[https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd\_dtl.m\_ab\_prime\_bps\_signups][4]|
|Lead Generation|abbd_dtl.m_pardot_bulk_prospect|Salesforce/Pardot prospect information including lead/contact status, email, company, annual revenue, etc.|N/A|**Lead ID - **crm_lead_fid
**Contact ID - **crm_contact_fid|ecid|N/A|[https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd\_dtl.M\_PARDOT\_BULK\_PROSPECT][5]|
|Lead Generation|abbd_dtl.d_ab_prospect_staging_campaign|Salesforce/Pardot prospect staging details including lead/contact status, lead/contact stage, staging campaign, etc.|N/A|**Lead AND Contact ID -** id|N/A|N/A|[https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd\_dtl.d\_ab\_prospect\_staging\_campaign][6]|
|MCS|abbd_dtl.m_ab_adobe_clickstream_logs|Adobe Analytics raw data feed, includes all dimensions and metrics that are captured in AA (for tracking b.a)|N/A|N/A|mcvisid|post_evar47|[https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd\_dtl.m\_ab\_adobe\_clickstream\_logs][7]|
|SSR|abbd_dtl.m_ab_registration_funnel_new|Aggregated data for each step of the self-registration flow|N/A|N/A|N/A|session_id|[https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd\_dtl.m\_ab\_registration\_funnel\_new][8]|
|Traffic/Engagement|abbd_dtl.m_ab_wma_hits|Clickstream details for page hits on a.com and b.a.com, commonly used to track Adoptions/HVAs|N/A|N/A|N/A|session_id|[https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd\_dtl.m\_ab\_wma\_hits][9]|

## Sample Queries
Pulls all self-registered AB accounts (verified positive) and the ref markers tied to their registrations (starting on 1/1/2022)

```
SELECT DISTINCT
baid.business_account_id
, baid.registered_date
, baid.vertical
, sesh.session_id
, ref.landing_ref_marker

FROM ABBD_DTL.D_AB_BUSINESS_ACCOUNTS baid

INNER JOIN
abbd_dtl_ext.apt_ab_registrations sesh on baid.business_account_id = sesh.business_account_id

INNER JOIN
abbd_dtl.m_ab_registration_funnel_new ref on sesh.session_id = ref.session_id

WHERE
    baid.registered_date >= Convert(datetime, '2022-01-01' )
    AND baid.is_active = 1
    AND baid.marketplace_ID = 1
    AND (baid.overall_status = 'VERIFICATION_POSITIVE' OR baid.overall_status = 'WHITELISTED')
    AND ref.business_landing = 1
```

Pulls all lead information for users that submitted the Contact Sales form on the MCS (b.a.xx)

```
drop table if exists test_ecid;
Create temp table test_ecid as(

SELECT
mcvisid

FROM abbd_dtl.m_ab_adobe_clickstream_logs

WHERE post_event_list ilike '%212%'
AND post_evar17 ilike '%contact-us%'
);

SELECT
eid.mcvisid
, lds.marketplace_id
, lds.prospect_id
, lds.crm_contact_fid
, lds.crm_lead_fid
, lds.company
, lds.job_title
, lds.annual_revenue
, lds.source
, lds.grade
, lds.created_at
, lds.updated_at
, lds.contact_us_submit_date
, lds.status_lead
, lds.contact_status
, lds.lead_stage
, lds.contact_stage
, lds.lead_sync_with_crm

FROM abbd_dtl.M_PARDOT_BULK_PROSPECT lds

INNER JOIN test_ecid eid on lds.ecid = eid.mcvisid
```

Pulls the volume of clicks on the MCS to the Business Prime landing page (amazon.xx/businessprime), broken down by outbound ref marker and specific b.a page where click was generated

```
SELECT
post_clickmappage as mcs_page_path,
post_page_event_var1 as exit_link,
post_evar2 as exit_link_reftag,
COUNT(DISTINCT post_visid_high || post_visid_low || visit_num || visit_start_time_gmt) as total_visits

FROM abbd_dtl.m_ab_adobe_clickstream_logs

WHERE
post_page_event_var1 like '%www.amazon.com/businessprime%'
AND post_page_event = '100'

group by 1,2,3
```

[1]: https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd_sandbox_intl.ab_eu_acq_credited_attribution
[2]: https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd_sandbox_mktg.jp_acq_channel_attr
[3]: https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd_dtl.d_ab_business_accounts
[4]: https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd_dtl.m_ab_prime_bps_signups
[5]: https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd_dtl.M_PARDOT_BULK_PROSPECT
[6]: https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd_dtl.d_ab_prospect_staging_campaign
[7]: https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd_dtl.m_ab_adobe_clickstream_logs
[8]: https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd_dtl.m_ab_registration_funnel_new
[9]: https://metadata.galileo.ab.amazon.dev/table/Redshift.abdai.abbd_dtl.m_ab_wma_hits
