# WorkDocs Direct Download Investigation — 2026-04-05

## Goal
Automate downloading the WW Dashboard xlsx from WorkDocs without Richard manually clicking download.

## Document
- WorkDocs URL: https://amazon.awsapps.com/workdocs-amazon/index.html#/document/9924b88a02031acc159c44747e1ced917bc25233e26e8c4f150708649f33d05f
- Document ID: `9924b88a02031acc159c44747e1ced917bc25233e26e8c4f150708649f33d05f`
- Version ID (W13): `1774883850118-c839c542960dbda51918de1f7871521beac56fe459efedf2fed67247d14e79ba`

## API Endpoints Discovered
- Zocalo API: `https://zocalo.us-west-2.amazonaws.com/api/v1/documents/{doc_id}/versions/{version_id}?fields=SOURCE`
- Returns pre-signed S3 URL on `gb-us-west-2-prod-doc-source.s3.us-west-2.amazonaws.com`
- Pre-signed URLs expire in 900 seconds (15 min)

## What We Tried
1. builder-mcp ReadInternalWebsites → WorkDocs viewer URL → "Unsupported resource response mime type: application/pdf"
2. builder-mcp ReadInternalWebsites → Zocalo API URL → "Unrecognized input format"
3. builder-mcp ReadInternalWebsites → WorkDocs API URL → "Unrecognized input format"
4. curl with Midway certs → WorkDocs API → "AccessDenied"
5. curl with Midway certs + cookie → WorkDocs API → "AccessDenied"
6. curl with Midway certs → Zocalo API → "anonymous is not authorized"
7. boto3 WorkDocs client → requires AuthenticationToken (not IAM creds)
8. Amazon Drive endpoint → "Unauthenticated" (wants browser Midway session)

## Root Cause
WorkDocs/Zocalo API requires a user-level authentication token from the WorkDocs OAuth flow, not Midway certs or IAM credentials. DevSpaces can't generate this token — it requires a browser-based auth flow.

## Current Solution
Poll Richard's OneDrive Downloads folder via SharePoint MCP for new `AB SEM WW Dashboard_Y26 W*.xlsx` files. Richard downloads from WorkDocs as usual (one click/week). Watcher detects and runs full pipeline.

## Future Options (if revisited)
- WorkDocs API OAuth token: if Amazon provides a service account or API key for WorkDocs, the Zocalo endpoint would work
- Local browser automation: Tampermonkey/Playwright on Richard's machine to auto-download on schedule
- Ask Stacey/Adi to also save to a shared SharePoint folder (behavioral change for them)
