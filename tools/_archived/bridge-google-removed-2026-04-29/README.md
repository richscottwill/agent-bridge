# Archived: Google Bridge

**Archived:** 2026-04-29
**Reason:** AmSec (AFSS Iliad) disabled external file sharing in Google Workspace. Richard's Drive share to the `kiro-491503.iam.gserviceaccount.com` service account was the one flagged occurrence originating from Amazon Business - PSME - VAR.

## What this was

Google Sheets/Docs/Drive-based async message bus and context-snapshot channel between Kiro (running server-side in DevSpaces) and Richard's personal agent swarm (running locally with Google account access).

Two jobs it carried:

1. **Google Ads data seam** — local agent pulled Ads data with Richard's Google credentials, wrote into the shared Sheet, Kiro read from the Sheet.
2. **Async message bus + context snapshots** — inter-agent messaging, requests, registry, heartbeats, draft/research/archive/backup folders.

## Why it was removed (not migrated in-place)

The `kiro-491503` GCP project lives outside the amazon.com Google Workspace tenant (personal GCP project). Any Drive share to the service account email registers as external sharing, which is the specific pattern AmSec is shutting off.

Options considered:

- Migrate project to amazon.com tenant → heavy AFSS engagement, uncertain approval
- Get service account tenant-approved → requires TPS review, likely rejected
- Move to approved alternative (Box / S3 / SharePoint) → chosen path

Migration target: **Box** (handles both the file-write pattern for Ads data drops and the message bus pattern, inside Amazon's approved perimeter per InfoSec Secure Data Sharing Best Practices).

## Key facts (preserved for history)

- GCP project: `kiro-491503` (personal)
- Service account: `kiro-sheets-bridge@kiro-491503.iam.gserviceaccount.com`
- Spreadsheet ID: `1IlM43kzxw8Vlu6aUWXUV1dr7ZIF7O7H2bD5x3kaKIHg` (bus, context, registry, log, scratchpad tabs)
- Doc ID: `1koJV8a4Ig9BBDbrtQl-w8L4-2bUrz8lGwxUxEfIgQj8`
- Drive folder root: `1aeRuldkc-OL1gyR7FQ-WrvbpERPsYChZ` (10 subfolders: drafts, research, archive, play, agent-lang, tools, rsw-personal, rsw-work, backup-kiro, backup-swarm)
- Credential file (deleted 2026-04-29): `~/shared/credentials/kiro-491503-6b65ab0501c6.json`

## What was done at sunset

1. Credential JSON deleted from disk (2026-04-29).
2. Drive share from Richard's account to the service account email revoked (action by Richard).
3. GCP service account key revoked in GCP console (action by Richard, separate).
4. Operational references removed from `device.md`, `current.md`, and three spec glossaries (`agentcore-system-integration`, `mcp-integration-optimization`, `mcp-capability-expansion`).

## Do NOT revive without security approval

If AmSec later validates that an Amazon-owned or tenant-approved GCP service account can hold Drive shares, and there's a use case that Box/S3/SharePoint can't cover, revive by:

1. Getting the new service account approved through TPS/AVS.
2. Recreating the credentials under that service account — do NOT reuse the `kiro-491503` project.
3. Updating `device.md` and documenting the approval path.

Until then: this directory stays archived. The sunset drivers — AmSec external-sharing restriction and the personal-tenant GCP service account pattern — remain in effect; any proposal to reintroduce Google Workspace as operational infrastructure should be held against those drivers before acting.
