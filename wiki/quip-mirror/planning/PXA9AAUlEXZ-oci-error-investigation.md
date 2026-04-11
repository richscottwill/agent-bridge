---
quip_id: PXA9AAUlEXZ
title: "OCI Error Investigation"
source_url: https://quip-amazon.com/PXA9AAUlEXZ
doc_type: document
creator: Stacey Gu
last_modified: "2025-07-08"
quip_folder: Planning/OCI
topics: [OCI, error investigation, tracking, hvocijid, Android, troubleshooting]
mirror_date: "2026-04-10"
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
