---
audience: amazon-internal
creator: Stacey Gu
doc_type: document
last_modified: '2025-07-08'
mirror_date: '2026-04-10'
owner: Richard Williams
quip_folder: Planning/OCI
quip_id: PXA9AAUlEXZ
source_url: https://quip-amazon.com/PXA9AAUlEXZ
status: DRAFT
title: OCI Error Investigation
topics:
- OCI
- error investigation
- tracking
- hvocijid
- Android
- troubleshooting
backfill_status: backfilled
---

# OCI Error Investigation
## Missing Join ID - Solved
**Resolution Description**: Believe this was solved by the removal of ETAs (with static Suffix) performed finalized 11/20/25. Initial errors were based on data from Nov 20-30. Yashasvi repulled the error log Dec 10-Jan 7, and found 0 errors.

1/6/25
### Issue and Data
**Issue**: JoinID (hvocijid value) is missing from URLs

**Error Refs**:
* pd_sl_brand_core_mt_2938077214_x74244177289
 * Kw: amazon business
 * Clicks: 12,023 Dec | X Nov 20-30
* pd_sl_brand_core_avt_small_mt_2938077214_x127581630151
 * Kw: amazon business
 * Clicks: 3,323 Dec | X Nov 20-30
* pd_sl_brand_plus_mt_464362629057_x110237734797
 * Kw: amazon pallets wholesale
 * Clicks: 4,512 Dec | X Nov 20-30
* pd_sl_brand_core_mt_1802041673_y123887221388
 * Kw: amazon business
 * Clicks: 1,486 Dec | X Nov 20-30
**Error URLs**:
* https://[www.google.com/asnc/AHb8uPaYqgj0M2Z8frzsMfD8vfCED2KCcwfj8ePzIUXJlttCeyLi/?id=com.amazon.mShop.android.shopping&url=https%3A%2F%2Fbusiness.amazon.com%2Fen%2Fcp%2Flp%3Fref%3Dpd\_sl\_brand\_core\_mt\_2938077214\_x74244177289&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20&referrer=type%3Dcontinue&inline=true&enifd=ABT2UUigsFR5VP62SWynO06ghTYaG-FNoBUsTHmge\_A8ZIMQaiRbKXi3wwMX5kuWtlmr-STOnQ9CNgR7AF3Hx0Ow\_T8oH8HQhIZtCoBA7Qh99DFmqPFu\_spO66DaoGpeua3Vf1wDRgHNGo2RiiPp9KE3vC-B\_Cl35wS74GiRQqAO-aMXLdhbu\_v3sLp\_mK3gxOXneoufqtodyoCx1BAi99SAKqo&gad\_source=1#Intent;scheme=market;package=com.android.vending;end][1];
* https://www.google.com/asnc/AHb8uPYLW_nJt8g4LZ4fLyfkcC1xgpz20UYjgpIpFZbxFR1TLJcV/?id=com.amazon.mShop.android.shopping&url=https%3A%2F%2Fbusiness.amazon.com%2Fen%2Fcp%2Flp%3Fref%3Dpd_sl_brand_core_avt_small_mt_2938077214_x127581630151&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20&referrer=type%3Dcontinue&inline=true&enifd=ABT2UUjWFIUh-Nth14BVS4uNhJ-AsHJW4IAGjRwn15Edi1Tne39ynGwk6N44a4a3QQa_oopzEOd7dFLFDbAIuzuj9bTeSLJciLHGEUtqqIiiJPdwyEe_QJaNHsXNjXgAvStJZYmQlAUaiWIgnKXOGbJcXMtyrNjdAwaOr3WQnYSBBEFcRDNS2Buo9ITG0HOGaZoJNGTNuCJRfnOcuPFOFaqJv4E&gad_source=1#Intent;scheme=market;package=com.android.vending;end;
* https://www.google.com/asnc/AHb8uPa1DogtIfi1EdPEeLykT4yEjeX1i0bCrurYdsOGNDfqLoQV/?id=com.amazon.mShop.android.shopping&url=https%3A%2F%2Fbusiness.amazon.com%2Fen%2Fcp%2Flpa-wholesale%3Fref%3Dpd_sl_brand_plus_mt_464362629057_x110237734797&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20&referrer=type%3Dcontinue&inline=true&enifd=ABT2UUhq6KUG0yIheWHNPHmuDwwoh5ZfLoc_LCPcp_mla3tojJz7Ephu-aSRkusp6Tq_h9EcymLcqJZ97iLV2BdQjIW4cHQKC0lWtvOAEXSuptN_60_zMNU5J8QhDWqWqU_v-i-P8lKtySj2dfMFdV0J2OUuhzz5ifTH07F3rEGkeFeQFHcWvfMQoCvvqf4R60KgxyFr9KD3n5lAJcodxePEyKQ&gad_source=1#Intent;scheme=market;package=com.android.vending;end;
* [https://www.google.com/asnc/AHb8uPYZjuQk9ro\_cDXQFGsC8zL5oMdWf6FZrxllDdE1kv-\_8cY/?id=com.amazon.mShop.android.shopping&url=https%3A%2F%2Fbusiness.amazon.com%2Fen%2Fcp%2Flp%3Fref%3Dpd\_sl\_brand\_core\_mt\_1802041673\_y123887221388&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20&referrer=type%3Dcontinue&inline=true&enifd=ABT2UUhCNR0nm749sxeQoJTIh1HA-Zxxj6uKb3FzVSFIlyCCtFxoYPJLdenFiKUf6usXaKCRC3cHUJ2nR\_bbC50GzC7xCvy3MoZuVIKISiIiZkb-pjRNtemvxDCoAc4\_4q53ILoj8nNYgafGbQAha0fxaA&gad\_source=1#Intent;scheme=market;package=com.android.vending;end][2];
Cleaned URLs
* [https://business.amazon.com/en/cp/lp?ref=pd\_sl\_brand\_core\_mt\_2938077214\_x74244177289&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20][3]
* [https://business.amazon.com/en/cp/lp?ref=pd\_sl\_brand\_core\_avt\_small\_mt\_2938077214\_x127581630151&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20][4]
* [https://business.amazon.com/en/cp/lpa-wholesale?ref=pd\_sl\_brand\_plus\_mt\_464362629057\_x110237734797&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20][5]
* [https://business.amazon.com/en/cp/lp?ref=pd\_sl\_brand\_core\_mt\_1802041673\_y123887221388&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20][6]

### **Troubleshooting Steps**
* Kw: confirmed no Suffix override
* Ad: confirmed no Suffix override
* AdG: confirmed no Suffix override
* Camp: confirmed no Suffix override
Overall Findings:
* All URLs contain “Redacted” after hvocijid. It seems it would only include this if there was a value in hvocijid
* All URLs are Android:

**Chrome Test #1**
* Replicated Mobile within Chrome desktop
* Searched “Amazon business”
* Clicks PS Ad. LP URL:
 * [https://www.google.com/aclk?sa=L&ai=DChsSEwi76POWhPqRAxXkR0cBHdfpMm4YACICCAEQABoCcXU&co=1&ase=2&gclid=EAIaIQobChMIu-jzloT6kQMV5EdHAR3X6TJuEAAYASAAEgItRfD\_BwE&sph&cid=CAASuwHkaCm6-W4dQ1r-7fmIo3AhK4Yt\_91fId89bKDjT11GuVn2uaQj3YlNNTtFjou0tgOpspXyRHFLJ6vi2xJgenH7JiZrAKpF6Mki6yCh84yNI56uDDgyC1KU3lTmTWwjMSqORuy\_ZtbKu6JajtG6E11JWqiDGXbZZzDFB5SPuvXzWEIEETIBZ4u6sccbUIB3bgKs9hKNAFHTK\_4mzn1xS-GUARc\_K1oRV94Y-gdSWqKRxEzJVDAdu0ZRXDnp&cce=2&category=acrcp\_v1\_33&sig=AOD64\_2k-j\_YZzKNfztd04aN0Xkr2HmQmA&q&nis=6&adurl&ved=2ahUKEwikw-2WhPqRAxXPFVkFHXHYHMEQ0Qx6BAgYEAE&ch=1][7]
 * [https://business.amazon.com/en/cp/lp?ref=pd\_sl\_brand\_core\_mt\_2938077214\_x74244177289&hvocijid=14942819914134062752-&hvexpln=ssrText&tag=abpsgglacqus-20][8]
 * Reg Start: [https://www.amazon.com/business/register/org/landing?ref\_=pd\_sl\_brand\_core\_mt\_2938077214\_x74244177289&ecid=25261067811319802861020206118390905276&abreg\_ecid=25261067811319802861020206118390905276&transactid=252610678113198028610202061183909052762026-01-07T19%3A07%3A05.342Z][9]
* Findings: Note - this is an error URL
 * Ref Matches Error Refs: [ref=pd\_sl\_brand\_core\_mt\_2938077214\_x74244177289][8]
 * [hvocijid=14942819914134062752-][8] is present
  * [hvocijid][8] is always removed during reg start (confirmed in test #4)

**Chrome Test #2**
* Replicated Mobile within Chrome desktop
* Created Test URL using error LP: [https://business.amazon.com/en/cp/lpa-wholesale?ref=pd\_sl\_testingref][10]
* URL Following email entry:
 * https://www.amazon.com/ap/register?openid.return_to=https%3A%2F%2Famazon.com%2Fbusiness%2Fregister%2Faccount-setup%2Freturn%3Fabreg_signature%3DOASHCVIINru_vAMRBHU7UBjZsIpAmgygEH4gUuk4In4%253D%26abreg_entryRefTag%3Dpd_sl_testingref%26abreg_hasAcceptedTermsAndConditions%3Dtrue%26abreg_originatingEmailEncrypted%3DAAAAAAAAAAClhl8CmWPqtP05r%252Bc%252F0lDOOgAAAAAAAAAU8nnMphrjh84xo8YlAmBxxGbFUbE7f6GdXCzaSj%252BzyODfYJv4tAZ7SUAleCeZwPkYccd0Igs3VBIh%26abreg_ingressFlow%3DNONE%26abreg_client%3Dpaid_search%26ref_%3Dab_reg_notag_pp-paid_search_rn-paid_search_ab_reg_mbl%26abreg_layoutOverride%3DSTANDALONE&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_ab_reg_web_us&openid.mode=checkid_setup&marketPlaceId=ATVPDKIKX0DER&language=en_US&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=ab_registration_biss_mobile&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&ref_=ab_reg_notag_pp-paid_search_ap-ca-paid_search_ab_reg_mbl&openid.pape.preferred_auth_policies=Singlefactor&email=brandoxy%2BemailTest2%[40amazon.com][11]
 * Decoded: https://www.amazon.com/ap/register?openid.return_to=https://amazon.com/business/register/account-setup/return?abreg_signature=OASHCVIINru_vAMRBHU7UBjZsIpAmgygEH4gUuk4In4%3D&abreg_entryRefTag=pd_sl_testingref&abreg_hasAcceptedTermsAndConditions=true&abreg_originatingEmailEncrypted=AAAAAAAAAAClhl8CmWPqtP05r%2Bc%2F0lDOOgAAAAAAAAAU8nnMphrjh84xo8YlAmBxxGbFUbE7f6GdXCzaSj%2BzyODfYJv4tAZ7SUAleCeZwPkYccd0Igs3VBIh&abreg_ingressFlow=NONE&abreg_client=paid_search&ref_=ab_reg_notag_pp-paid_search_rn-paid_search_ab_reg_mbl&abreg_layoutOverride=STANDALONE&openid.identity=[http://specs.openid.net/auth/2.0/identifier\_select&openid.assoc\_handle=amzn\_ab\_reg\_web\_us&openid.mode=checkid\_setup&marketPlaceId=ATVPDKIKX0DER&language=en\_US&openid.claimed\_id=http://specs.openid.net/auth/2.0/identifier\_select&pageId=ab\_registration\_biss\_mobile&openid.ns=http://specs.openid.net/auth/2.0&ref\_=ab\_reg\_notag\_pp-paid\_search\_ap-ca-paid\_search\_ab\_reg\_mbl&openid.pape.preferred\_auth\_policies=Singlefactor&email=brandoxy+emailTest2@amazon.com][12]
* Findings:
 * Shows in-context email input. However, this is likely not the cause as in-context email input is not applied to “[business.amazon.com/en/cp/lp][8]” which is driving majority of errors
**Chrome Test #3**
* Mobile Chrome (on S20)
* Searched “Amazon business”
* Clicks PS Ad. LP URL:
 * [https://business.amazon.com/en/cp/lp?ref=pd\_sl\_brand\_core\_mt\_avt\_large\_2938077214\_x127700089154&hvocijid=1130826206121244802-&hvexpln=ssrText&tag=abpsgglacqus-20&dplnkId=48daadfe-83d6-421e-aa57-551652f37c64][13]
* Test ended as BM was logged into AB shopping portal (no reg start click available)
* Findings:
 * ref found wasn’t included in error list
 * hvocijid included
**Chrome Test #4**
* Mobile Chrome (on S20), Incognito
* Searched “Amazon business”
* Clicks PS Ad. LP URL:
 * [https://business.amazon.com/en/cp/lp?ref=pd\_sl\_brand\_core\_mt\_2938077214\_x74244177289&hvocijid=4163637588042669218-&hvexpln=ssrText&tag=abpsgglacqus-20][14]
 * Reg Start: [https://www.amazon.com/business/register/org/landing?ref\_=pd\_sl\_brand\_core\_mt\_2938077214\_x74244177289&ecid=24420833761142189331553790988816452585&abreg\_ecid=24420833761142189331553790988816452585&transactid=244208337611421893315537909888164525852026-01-07T19%3A34%3A14.263Z][15]
* Ref Matches Error Refs: [ref=pd\_sl\_brand\_core\_mt\_2938077214\_x74244177289][8]
* [hvocijid=14942819914134062752-][8] is present
 * [hvocijid][8] is always removed during reg start (confirmed in test #1)

[1]: http://www.google.com/asnc/AHb8uPaYqgj0M2Z8frzsMfD8vfCED2KCcwfj8ePzIUXJlttCeyLi/?id=com.amazon.mShop.android.shopping&url=https%3A%2F%2Fbusiness.amazon.com%2Fen%2Fcp%2Flp%3Fref%3Dpd_sl_brand_core_mt_2938077214_x74244177289&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20&referrer=type%3Dcontinue&inline=true&enifd=ABT2UUigsFR5VP62SWynO06ghTYaG-FNoBUsTHmge_A8ZIMQaiRbKXi3wwMX5kuWtlmr-STOnQ9CNgR7AF3Hx0Ow_T8oH8HQhIZtCoBA7Qh99DFmqPFu_spO66DaoGpeua3Vf1wDRgHNGo2RiiPp9KE3vC-B_Cl35wS74GiRQqAO-aMXLdhbu_v3sLp_mK3gxOXneoufqtodyoCx1BAi99SAKqo&gad_source=1#Intent;scheme=market;package=com.android.vending;end
[2]: https://www.google.com/asnc/AHb8uPYZjuQk9ro_cDXQFGsC8zL5oMdWf6FZrxllDdE1kv-_8cY/?id=com.amazon.mShop.android.shopping&url=https%3A%2F%2Fbusiness.amazon.com%2Fen%2Fcp%2Flp%3Fref%3Dpd_sl_brand_core_mt_1802041673_y123887221388&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20&referrer=type%3Dcontinue&inline=true&enifd=ABT2UUhCNR0nm749sxeQoJTIh1HA-Zxxj6uKb3FzVSFIlyCCtFxoYPJLdenFiKUf6usXaKCRC3cHUJ2nR_bbC50GzC7xCvy3MoZuVIKISiIiZkb-pjRNtemvxDCoAc4_4q53ILoj8nNYgafGbQAha0fxaA&gad_source=1#Intent;scheme=market;package=com.android.vending;end
[3]: https://business.amazon.com/en/cp/lp?ref=pd_sl_brand_core_mt_2938077214_x74244177289&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20
[4]: https://business.amazon.com/en/cp/lp?ref=pd_sl_brand_core_avt_small_mt_2938077214_x127581630151&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20
[5]: https://business.amazon.com/en/cp/lpa-wholesale?ref=pd_sl_brand_plus_mt_464362629057_x110237734797&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20
[6]: https://business.amazon.com/en/cp/lp?ref=pd_sl_brand_core_mt_1802041673_y123887221388&hvocijid=REDACTED&hvexpln=ssrText&tag=abpsgglacqus-20
[7]: https://www.google.com/aclk?sa=L&ai=DChsSEwi76POWhPqRAxXkR0cBHdfpMm4YACICCAEQABoCcXU&co=1&ase=2&gclid=EAIaIQobChMIu-jzloT6kQMV5EdHAR3X6TJuEAAYASAAEgItRfD_BwE&sph&cid=CAASuwHkaCm6-W4dQ1r-7fmIo3AhK4Yt_91fId89bKDjT11GuVn2uaQj3YlNNTtFjou0tgOpspXyRHFLJ6vi2xJgenH7JiZrAKpF6Mki6yCh84yNI56uDDgyC1KU3lTmTWwjMSqORuy_ZtbKu6JajtG6E11JWqiDGXbZZzDFB5SPuvXzWEIEETIBZ4u6sccbUIB3bgKs9hKNAFHTK_4mzn1xS-GUARc_K1oRV94Y-gdSWqKRxEzJVDAdu0ZRXDnp&cce=2&category=acrcp_v1_33&sig=AOD64_2k-j_YZzKNfztd04aN0Xkr2HmQmA&q&nis=6&adurl&ved=2ahUKEwikw-2WhPqRAxXPFVkFHXHYHMEQ0Qx6BAgYEAE&ch=1
[8]: https://business.amazon.com/en/cp/lp?ref=pd_sl_brand_core_mt_2938077214_x74244177289&hvocijid=14942819914134062752-&hvexpln=ssrText&tag=abpsgglacqus-20
[9]: https://www.amazon.com/business/register/org/landing?ref_=pd_sl_brand_core_mt_2938077214_x74244177289&ecid=25261067811319802861020206118390905276&abreg_ecid=25261067811319802861020206118390905276&transactid=252610678113198028610202061183909052762026-01-07T19%3A07%3A05.342Z
[10]: https://business.amazon.com/en/cp/lpa-wholesale?ref=pd_sl_testingref
[11]: http://40amazon.com
[12]: http://specs.openid.net/auth/2.0/identifier_select&openid.assoc_handle=amzn_ab_reg_web_us&openid.mode=checkid_setup&marketPlaceId=ATVPDKIKX0DER&language=en_US&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&pageId=ab_registration_biss_mobile&openid.ns=http://specs.openid.net/auth/2.0&ref_=ab_reg_notag_pp-paid_search_ap-ca-paid_search_ab_reg_mbl&openid.pape.preferred_auth_policies=Singlefactor&email=brandoxy+emailTest2@amazon.com
[13]: https://business.amazon.com/en/cp/lp?ref=pd_sl_brand_core_mt_avt_large_2938077214_x127700089154&hvocijid=1130826206121244802-&hvexpln=ssrText&tag=abpsgglacqus-20&dplnkId=48daadfe-83d6-421e-aa57-551652f37c64
[14]: https://business.amazon.com/en/cp/lp?ref=pd_sl_brand_core_mt_2938077214_x74244177289&hvocijid=4163637588042669218-&hvexpln=ssrText&tag=abpsgglacqus-20
[15]: https://www.amazon.com/business/register/org/landing?ref_=pd_sl_brand_core_mt_2938077214_x74244177289&ecid=24420833761142189331553790988816452585&abreg_ecid=24420833761142189331553790988816452585&transactid=244208337611421893315537909888164525852026-01-07T19%3A34%3A14.263Z
