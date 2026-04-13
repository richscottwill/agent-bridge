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
---

# OCI Error Investigation

Investigation into missing JoinID (hvocijid) values in OCI tracking URLs. Issue was resolved by removal of ETAs with static Suffix, finalized 11/20/25. Repulled error log Dec 10-Jan 7 showed 0 errors.

Key findings:
- All error URLs contained "Redacted" after hvocijid
- All error URLs were Android-based
- No Suffix overrides found at keyword, ad, ad group, or campaign levels
- Chrome mobile tests confirmed hvocijid is present in normal flow but removed during reg start
- Resolution: ETA removal resolved the duplicate parameter issue

For the full content, access the source document at: https://quip-amazon.com/PXA9AAUlEXZ
