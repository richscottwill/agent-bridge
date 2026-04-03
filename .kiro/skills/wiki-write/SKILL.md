---
name: wiki-write
description: "Write wiki articles using the full pipeline: editor assigns work, researcher gathers context, writer drafts, critic reviews, librarian publishes. Triggers on write wiki, document, wiki article, what should we document."
---

# Wiki Write Pipeline

## Instructions

The wiki pipeline is sequential: editor → researcher → writer → critic → librarian. The editor orchestrates — don't invoke wiki-writer or wiki-researcher directly unless the editor has already assigned the work.

1. **Editor** — Receives the writing request, determines scope, assigns research topics, and defines the article outline.
2. **Researcher** — Gathers context from body organs, shared files, Slack history, and any referenced sources. Compiles research brief for the writer.
3. **Writer** — Drafts the article following Richard's writing style (load richard-style-docs.md). Follows the editor's outline and incorporates the researcher's findings.
4. **Critic** — Reviews the draft for accuracy, completeness, tone, and adherence to wiki standards. Provides specific revision notes.
5. **Librarian** — Publishes the final article, updates any cross-references, and logs the new article in the wiki index.

## Notes

- Always load the relevant writing style guide before drafting.
- The editor is the orchestrator — respect the pipeline sequence.
- Save drafts to ~/shared/context/intake/ for processing before final publish.
