---
audience: amazon-internal
creator: Richard Williams
doc_type: document
last_modified: 2026-03-26
mirror_date: 2026-04-10
owner: Richard Williams
quip_folder: Onboarding/Data
quip_id: PWB9AAbFqoy
source_url: https://quip-amazon.com/PWB9AAbFqoy
status: DRAFT
title: Adobe FTP files
topics:
- onboarding
- data
- analytics
backfill_status: backfilled
---

# Adobe FTP files
## Adobe Metrics
EFID:
Source: EFID feed files (see below)

EFID RefMarker Reg: New registration metric setup to use OCI (deprecating use of GCLID)
* Source: OCI Files (see below), and EFID Feed
* Combines “registration ef id” and the new “registration_refmarker”
 * Split ensures all regs are captured during transition phase
## Feed Files
**Planned OCI Files:**
* Using the OCI feed files below without EFID
Current Files:
* **OCI Files:** These provide reg flag associated to ref marker on a daily basis
 * amazon_business_registrations_refmarker_US_20250621.txt
 * amazon_business_registrations_refmarker_EU_20250621
* **EFID Files:** These provide reg data associated to EFID on a daily basis
 * amazon_business_registrations_efid_EU_YYYYMMDD
 * amazon_business_registrations_efid_US_YYYYMMDD
* **Ref Reg 2 Files:**
 * EU: amazon_business_registrations_ref_EU__YYYYMMDD_
 * US: amazon_business_registrations_ref_YYYYMMDD.txt
**Full Feed File List:**
||A|B|C|D|E|F|G|H|I|
|---|---|---|---|---|---|---|---|---|---|
|1|​|Feed Name|Identifiers in  Feed|What is Parser  Using?|Property 1|Property 2|Property 3|Comments|_Job Links_|
|2|5|amazon_business_registrations_AMO_OPS_US_YYYYMMDD.txt|keyword_id|URL param|keyword_score_new|​|​|​|[https://datacentral.a2z.com/dw-platform/servlet/dwp/template/EtlViewExtractJobs.vm/job\_profile\_id/10235558][1]|
|3|3|amazon_business_registrations_efid_CA_YYYYMMDD.txt|ref_marker;  keyword_id; efid|EFID|registration|​|​|​|​|
|4|12|amazon_business_registrations_efid_EU_YYYYMMDD.txt|ref_marker;  keyword_id; efid|EFID|registration|​|​|​|​|
|5|9|amazon_business_registrations_efid_JP_YYYYMMDD.txt|ref_marker;  keyword_id; efid|EFID|registration|​|​|​|​|
|6|23|amazon_business_registrations_efid_MX_YYYYMMDD.txt|ref_marker;  keyword_id; efid|EFID|registration|​|​|​|​|
|7|1|amazon_business_registrations_efid_US_YYYYMMDD.txt|ref_marker;  keyword_id; efid|EFID|registration|​|​|​|​|
|8|8|amazon_business_registrations_keyword_icp_score_CA_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|keyword_icp_score|registrations|icp_weighted_registrations|​|​|
|9|13|amazon_business_registrations_keyword_icp_score_DE_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|keyword_icp_score|registrations|icp_weighted_registrations|​|​|
|10|21|amazon_business_registrations_keyword_icp_score_ES_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|keyword_icp_score|registrations|icp_weighted_registrations|​|​|
|11|20|amazon_business_registrations_keyword_icp_score_FR_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|keyword_icp_score|registrations|icp_weighted_registrations|​|​|
|12|14|amazon_business_registrations_keyword_icp_score_IN_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|keyword_icp_score|registrations|icp_weighted_registrations|​|​|
|13|18|amazon_business_registrations_keyword_icp_score_IT_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|keyword_icp_score|registrations|icp_weighted_registrations|​|​|
|14|17|amazon_business_registrations_keyword_icp_score_JP_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|keyword_icp_score|registrations|icp_weighted_registrations|​|​|
|15|19|amazon_business_registrations_keyword_icp_score_UK_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|keyword_icp_score|registrations|icp_weighted_registrations|​|​|
|16|4|amazon_business_registrations_keyword_icp_score_US_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|keyword_icp_score|registrations|icp_weighted_registrations|​|​|
|17|2|amazon_business_registrations_keyword_revennue_tier_icp_score_CA_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|micro_registrations|cps_registrations|​|​|​|
|18|10|amazon_business_registrations_keyword_revennue_tier_icp_score_DE_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|micro_registrations|cps_registrations|​|​|​|
|19|27|amazon_business_registrations_keyword_revennue_tier_icp_score_ES_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|micro_registrations|cps_registrations|​|​|​|
|20|26|amazon_business_registrations_keyword_revennue_tier_icp_score_FR_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|micro_registrations|cps_registrations|​|​|​|
|21|24|amazon_business_registrations_keyword_revennue_tier_icp_score_IN_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|micro_registrations|cps_registrations|​|​|​|
|22|28|amazon_business_registrations_keyword_revennue_tier_icp_score_IT_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|micro_registrations|cps_registrations|​|​|​|
|23|11|amazon_business_registrations_keyword_revennue_tier_icp_score_JP_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|micro_registrations|cps_registrations|​|​|​|
|24|25|amazon_business_registrations_keyword_revennue_tier_icp_score_UK_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|micro_registrations|cps_registrations|​|​|​|
|25|22|amazon_business_registrations_keyword_revennue_tier_icp_score_US_YYYYMMDD.txt|ref_marker;  keyword_id|URL param|micro_registrations|cps_registrations|​|​|​|
|26|7|amazon_business_registrations_ref_CA_YYYYMMDD.txt|keyword_id|URL param|REF_Registrations_2|weighted_registration|​|​|[https://datacentral.a2z.com/dw-platform/servlet/dwp/template/EtlViewExtractJobs.vm/job\_profile\_id/7581823][2]|
|27|16|amazon_business_registrations_ref_EU_YYYYMMDD.txt|keyword_id|URL param|REF_Registrations_2|weighted_registration|​|​|​|
|28|6|amazon_business_registrations_ref_YYYYMMDD.txt|keyword_id|URL param|REF_Registrations_2|weighted_registration|​|​|​|
|29|15|amazon_business_registrations_ref_JP_YYYYMMDD.txt|keyword_id|URL param|registration_japan_v2|ICP_weighted_registrations_japan_v2|​|​|​|
|30|​|amazon_business_registrations_refmarker_US_YYYYMMDD.txt|registration_refmarker|registration_refmarker|EFID RefMarker|​|​|OCI File|[https://datacentral.a2z.com/dw-platform/servlet/dwp/template/EtlViewExtractJobs.vm/job\_profile\_id/10235558][1]|
|31|​|amazon_business_registrations_refmarker_EU_YYYYMMDD.txt|registration_refmarker|registration_refmarker|EFID RefMarker|​|​|OCI File|​|
|32|​|amazon_business_registrations_refmarker_EU3_YYYYMMDD.txt|registration_refmarker 2|registration_refmarker|EFID RefMarker Reg 2|​|​|OCI File|​|
|33|​|amazon_business_registrations_refmarker_EU_updated_YYYYMMDD.txt|registration_refmarker 2|registration_refmarker 2|EFID RefMarker Reg 2|​|​|OCI File|​|
|34|12|amazon_business_registrations_refmarker_EU3_updated_YYYYMMDD.txt|registration_refmarker 2|registration_refmarker 2|EFID RefMarker Reg 2|​|​|OCI File|​|
|35|​|amazon_business_registrations_refmarker_JP_updated_YYYYMMDD.txt|registration_refmarker 2|registration_refmarker 2|EFID RefMarker Reg 2|​|​|​|​|
|36|​|amazon_business_registrations_refmarker_JP_YYYYMMDD.txt|registration_refmarker|registration_refmarker|EFID RefMarker|​|​|​|​|
|37|​|amazon_business_registrations_refmarker_CA_YYYYMMDD.txt|registration_refmarker|registration_refmarker|EFID RefMarker|​|​|​|​|
[1]: https://datacentral.a2z.com/dw-platform/servlet/dwp/template/EtlViewExtractJobs.vm/job_profile_id/10235558
[2]: https://datacentral.a2z.com/dw-platform/servlet/dwp/template/EtlViewExtractJobs.vm/job_profile_id/7581823
