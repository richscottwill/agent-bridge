---
name: sharepoint-sync
description: "Sync documents to SharePoint. Triggers on sync to SharePoint, SharePoint sync, upload to SharePoint."
---

# SharePoint Sync

## Instructions

1. **Identify target documents** — Determine which files need to be synced to SharePoint based on the user's request or a predefined sync list.
2. **Verify SharePoint access** — Confirm the target SharePoint site and document library are accessible via the SharePoint MCP server.
3. **Upload files** — Run `scripts/sync.sh` to upload the identified files to the correct SharePoint location.
4. **Verify upload** — Confirm files were uploaded successfully by listing the target library.
5. **Log sync** — Record the sync operation (files synced, timestamps, target location) to ~/shared/context/intake/ for tracking.

## Notes

- Uses the SharePoint MCP server for document library access and file upload.
- Ensure file names and paths comply with SharePoint naming conventions.
