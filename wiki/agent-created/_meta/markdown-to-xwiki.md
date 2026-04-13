---
title: "Markdown to XWiki Markup Conversion Rules"
status: REVIEW
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0447 | duck_id: wiki-meta-markdown-to-xwiki -->

# Markdown to XWiki Markup Conversion Rules

Reference for the wiki-librarian when publishing articles to w.amazon.com via XWiki MCP.

## Conversion Table

| Markdown | XWiki 2.1 Syntax | Notes |
|----------|-------------------|-------|
| `# Heading 1` | `= Heading 1 =` | Top-level heading |
| `## Heading 2` | `== Heading 2 ==` | Section heading |
| `### Heading 3` | `=== Heading 3 ===` | Subsection heading |
| `#### Heading 4` | `==== Heading 4 ====` | Sub-subsection |
| `**bold**` | `**bold**` | Same syntax |
| `*italic*` | `//italic//` | Different delimiters |
| `~~strikethrough~~` | `--strikethrough--` | Different delimiters |
| `- list item` | `* list item` | Unordered list |
| `  - nested item` | `** nested item` | Add another `*` per level |
| `1. ordered item` | `1. ordered item` | Same syntax |
| `  1. nested ordered` | `1.1. nested ordered` | Dot notation for nesting |
| `` `inline code` `` | `{{code}}inline code{{/code}}` | Inline code |
| ` ```code block``` ` | `{{code language="..."}}...{{/code}}` | Fenced code block |
| `[text](url)` | `[[text>>url]]` | Links |
| `![alt](url)` | `[[image:url\|\|alt="alt"]]` | Images |
| `> blockquote` | `> blockquote` | Same syntax |
| `---` | `----` | Horizontal rule (4 dashes) |

## Table Conversion

Markdown tables convert directly — XWiki uses the same pipe syntax:

**Markdown:**
```
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

**XWiki:**
```
|= Header 1 |= Header 2
| Cell 1 | Cell 2
```

Note: XWiki uses `|=` for header cells (no separator row needed).

## Frontmatter Handling

Strip YAML frontmatter (`---` blocks) before conversion. Extract these fields for XWiki page metadata:
- `title` → XWiki page title
- `tags` → XWiki category tags
- `doc-type` → Include as XWiki tag
- `audience` → Include as XWiki tag
- `updated` → XWiki page metadata

## AGENT_CONTEXT Block

Strip the `<!-- AGENT_CONTEXT ... -->` HTML comment block before XWiki conversion. This is agent-internal metadata not needed on w.amazon.com.

## Special Characters

Escape these XWiki special characters if they appear in content:
- `~` → `~~` (tilde is the XWiki escape character)
- `{` and `}` → `~{` and `~}` (when not part of macros)

## Conversion Procedure

When converting an article for XWiki publishing:

1. Read the markdown source from `~/shared/wiki/{category}/{filename}.md`
2. Strip YAML frontmatter — extract title, tags for page metadata
3. Strip `<!-- AGENT_CONTEXT -->` block
4. Apply conversion rules line by line:
   a. Convert headings (count `#` → matching `=` pairs)
   b. Convert italic (`*text*` → `//text//`) — careful not to touch `**bold**`
   c. Convert links (`[text](url)` → `[[text>>url]]`)
   d. Convert code blocks (fenced → `{{code}}` macro)
   e. Convert inline code (backticks → `{{code}}` inline)
   f. Convert unordered lists (`-` → `*`, nesting by `*` count)
   g. Convert tables (add `=` to header cells, remove separator row)
   h. Convert horizontal rules (`---` → `----`)
   i. Convert images
5. Validate: no raw markdown syntax remains in output
6. Return the XWiki markup string for publishing

## Example

**Markdown input:**
```markdown
## Testing Methodology

This is **bold** and *italic* text.

- First item
  - Nested item
- Second item

See [the guide](https://example.com) for details.

| Market | Status |
|--------|--------|
| AU     | Active |
| MX     | Active |
```

**XWiki output:**
```
== Testing Methodology ==

This is **bold** and //italic// text.

* First item
** Nested item
* Second item

See [[the guide>>https://example.com]] for details.

|= Market |= Status
| AU | Active
| MX | Active
```
