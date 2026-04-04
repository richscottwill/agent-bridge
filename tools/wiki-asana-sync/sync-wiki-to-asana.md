# Wiki-to-Asana Sync — Design

## Purpose
Keep wiki article content available in Asana so Richard can read articles from the Asana app (including mobile) without needing file system access.

## Approach: Tiered

### Tier 1: html_notes sync (AVAILABLE NOW)
- Write full article content into each task's html_notes field via Enterprise Asana MCP
- Formatting: bold for headers, lists for bullets, no tables (converted to lists)
- Runs during EOD-2 or on-demand
- Source of truth: ~/shared/artifacts/ (file system)
- Asana is the read-only distribution copy

### Tier 2: File attachment sync (REQUIRES PAT)
- Convert markdown to .docx via python-docx (installed)
- Upload .docx as attachment to each task via Asana REST API
- Requires: Asana Personal Access Token (generate at app.asana.com/0/my-apps)
- Store PAT at: ~/.config/asana/pat.txt (gitignored)
- Full formatting preserved including tables, headers, code blocks

## Tier 1 Implementation

### Markdown to Asana HTML conversion rules:
- `# Header` → `<strong>HEADER</strong>` (all caps for H1)
- `## Header` → `<strong>Header</strong>`
- `### Header` → `<strong>Header</strong>`
- `**bold**` → `<strong>bold</strong>`
- `*italic*` → `<em>italic</em>`
- `- item` → `<ul><li>item</li></ul>`
- `1. item` → `<ol><li>item</li></ol>`
- `[text](url)` → `<a href="url">text</a>`
- `| table |` → converted to `<ul><li>` list format
- `---` (horizontal rule) → removed
- YAML frontmatter → stripped (metadata lives in custom fields)
- AGENT_CONTEXT block → stripped (agent-only, not for human reading)
- Sources section → preserved as a list

### Sync protocol:
1. Read article from ~/shared/artifacts/{category}/{file}.md
2. Strip YAML frontmatter and AGENT_CONTEXT block
3. Convert markdown to Asana HTML
4. Find or create the corresponding task in ABPS AI Content project
5. Write to html_notes via UpdateTask
6. Update Kiro_RW with sync timestamp

### Task matching:
- Match by task name = article title
- If no matching task exists, create one in the Active section
- Custom fields: doc-type, last-synced date, critic score

## Tier 2 Implementation (when PAT available)

### Setup:
1. Richard generates PAT at app.asana.com/0/my-apps
2. Store at ~/.config/asana/pat.txt
3. Script reads PAT and uses Asana REST API directly

### Script: sync-wiki-attachments.py
```python
# Pseudocode — build when PAT is available
import requests
from docx import Document
import os

PAT = open(os.path.expanduser("~/.config/asana/pat.txt")).read().strip()
HEADERS = {"Authorization": f"Bearer {PAT}"}
PROJECT_GID = "1213917352480610"  # ABPS AI Content

def md_to_docx(md_path, docx_path):
    """Convert markdown to docx using python-docx"""
    doc = Document()
    # Parse markdown, add paragraphs/tables/headers
    doc.save(docx_path)

def upload_attachment(task_gid, file_path):
    """Upload file as attachment to Asana task"""
    url = f"https://app.asana.com/api/1.0/tasks/{task_gid}/attachments"
    with open(file_path, "rb") as f:
        resp = requests.post(url, headers=HEADERS, 
                           files={"file": (os.path.basename(file_path), f)})
    return resp.json()

def sync_all():
    """Sync all wiki articles to Asana as .docx attachments"""
    artifacts_dir = os.path.expanduser("~/shared/artifacts")
    for category in os.listdir(artifacts_dir):
        category_path = os.path.join(artifacts_dir, category)
        if not os.path.isdir(category_path):
            continue
        for filename in os.listdir(category_path):
            if not filename.endswith(".md"):
                continue
            md_path = os.path.join(category_path, filename)
            docx_path = f"/tmp/{filename.replace('.md', '.docx')}"
            md_to_docx(md_path, docx_path)
            # Find matching task, upload attachment
```

## Unblock Tier 2:
Richard: generate a PAT at app.asana.com/0/my-apps, save to ~/.config/asana/pat.txt
Then run: python3 shared/tools/wiki-asana-sync/sync-wiki-attachments.py
