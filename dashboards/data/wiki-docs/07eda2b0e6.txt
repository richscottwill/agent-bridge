# Team Wiki — Search, Use, Suggest Edits

**Doc:** 10
**Audience:** Paid Acquisition teammates + their Kiro agents
**Status:** FINAL
**Last updated:** 2026-04-17

## Environment Awareness (for your agent)

| Capability | Remote IDE (DevSpaces) | Local IDE (laptop Kiro) | AgentSpaces (chat) |
|---|---|---|---|
| Direct file access to `~/shared/wiki/` | ✅ Native | ❌ Not on laptop | ❌ Not exposed |
| Read wiki via OneDrive (synced copy in `Kiro-Drive/wiki/` if exposed) | ⚠️ Indirect | ⚠️ If selective sync enabled | ⚠️ Via SharePoint MCP |
| Search `wiki_index.json` | ✅ Direct read | ✅ If synced | ✅ via SharePoint MCP read |
| Render wiki-search dashboard | ✅ Local HTTP server | ⚠️ Only if dashboard replicated | ❌ |
| Write edit suggestions to intake folder | ✅ `~/shared/wiki/intake/suggestions/` | ⚠️ Via OneDrive sync | ⚠️ Via SharePoint MCP write to synced intake |
| Merge suggestions to canonical (librarian function) | ✅ Only by designated librarian | ❌ Librarian-only | ❌ |

**Tell the user in plain language:**
- **Remote IDE:** *"I can search the team's shared knowledge base directly, pull up articles, and leave suggested edits for review. Full access here."*
- **Local IDE:** *"I can reach the team's knowledge base if your OneDrive is syncing the files. If you're not sure whether it is, I can check — or you can ask me from your Remote IDE where access is guaranteed."*
- **AgentSpaces:** *"I can search and read the team's knowledge base, and I can leave suggestions by writing to your OneDrive. I can't see changes as quickly as in a regular IDE, but it works for most lookup and contribution tasks."*

---

The Paid Acq team wiki is a collection of markdown articles stored in `~/shared/wiki/` (on DevSpaces) and mirrored to OneDrive. It's the team's knowledge base: market playbooks, test designs, callouts archive, meeting recaps, strategic artifacts, style guides.

An agent that knows how to search the wiki before guessing is dramatically more useful than one that doesn't.

## Structure

```
~/shared/wiki/
├── agent-created/          ← docs written by agents (or humans via agent pipeline)
│   ├── strategy/
│   ├── markets/
│   ├── reporting/
│   ├── operations/
│   ├── testing/
│   ├── research/
│   ├── reviews/
│   └── _meta/
├── callouts/               ← weekly market callouts, organized by market and week
├── meetings/               ← meeting recaps and series files
├── quip-mirror/            ← mirrors of canonical Quip docs (read-only sync)
├── state-files/            ← per-market current state files
└── intake/
    └── suggestions/        ← edit proposals waiting for review (see below)
```

## The index and search dashboard

- **Indexer:** `shared/dashboards/build-wiki-index.py` crawls the local wiki AND reads a SharePoint artifacts snapshot, then produces two outputs from a single scan:
  - `shared/dashboards/data/wiki-search-index.json` — the dashboard data file (full document records, search text, related-docs graph, SharePoint publication status per doc).
  - `shared/wiki/agent-created/_meta/wiki-index.md` — the human- and agent-readable index. **This file is auto-generated — do not hand-edit. Changes will be overwritten on the next build.**
- **SharePoint snapshot:** `shared/dashboards/data/sharepoint-artifacts.json` is a cached list of `Documents/Artifacts/**/*.docx` captured via the SharePoint MCP. The builder reads this to mark each local article as `published` (docx exists on SP), `sharepoint_stale` (local `updated` is newer than the SP `Modified`), or `local-only` (not on SP). Refresh the cache by running the `wiki-maintenance` hook — it calls the SharePoint MCP for each category folder and writes a fresh snapshot before invoking the builder.
- **Dashboard:** `shared/dashboards/wiki-search.html` is the client-side browsing UI. It's reachable at **[http://localhost:8080/wiki-search.html](http://localhost:8080/wiki-search.html)** when the local dashboard server is running (`serve.py` on port 8080 — started automatically in DevSpaces). Filters include Status, Market, Topic, Type, and **SharePoint** (Published / Stale / Local-only). Result cards show a 📤 SP / 📤 stale / 📄 local badge so you can see at a glance which docs are synced.
- **Index refresh:** the `wiki-maintenance` weekly hook (manual, Friday) runs the full pipeline — refresh SharePoint cache, rebuild index, run audit, update roadmap. You can also run `python3 ~/shared/dashboards/build-wiki-index.py` directly whenever you need fresh data — it's fast and idempotent.

## How a teammate's agent searches the wiki

Three access patterns depending on environment:

### Remote IDE (direct access)

```python
import json
with open('/home/prichwil/shared/dashboards/data/wiki-search-index.json') as f:
    index = json.load(f)
# Filter by keyword:
hits = [d for d in index['documents'] if 'Polaris' in d['title'] or 'Polaris' in d.get('search_text', '')]

# Check SharePoint publication status:
published = [d for d in index['documents'] if d.get('published')]
stale_on_sp = [d for d in index['documents'] if d.get('sharepoint_stale')]
```

Or just grep:

```bash
grep -r -l "Polaris" ~/shared/wiki/
```

Agent reads the specific article(s) it needs. Don't bulk-load the whole wiki into context.

### Local IDE (via synced OneDrive)

If the wiki is mirrored to `OneDrive/Kiro-Drive/wiki/`, read via filesystem. Otherwise, use SharePoint MCP (same pattern as AgentSpaces).

### AgentSpaces (via SharePoint MCP)

```
1. sharepoint_search with keyword → returns candidate articles from OneDrive mirror
2. sharepoint_read_file with inline=true → returns markdown
3. Agent parses and answers
```

Slower than direct filesystem, but functional.

## The "search wiki before guessing" rule

Before answering any question that might be covered by the wiki (market context, past test results, team norms, style guides, callout principles, Amazon conventions), your agent should:

1. Formulate a search query.
2. Hit the index (or SharePoint search for AgentSpaces).
3. If a matching article exists, read and cite it in the answer.
4. If no match, say "no wiki article on this yet — here's my best from general context" and tag the topic as a potential new article.

**Install this rule via steering** in your Kiro steering folder as `wiki-contributor.md` (in `.kiro/steering/` inside your workspace, or `~/.kiro/steering/` for user-level) (see bottom of doc).

## How to suggest an edit

Agents never auto-edit the canonical wiki. Edits go through an intake flow:

1. Agent drafts the proposed change as a markdown diff or an edited version of the article.
2. Agent drops the proposal in `~/shared/wiki/intake/suggestions/` with a filename like `<article-slug>-<submitter-alias>-YYYY-MM-DD.md`.
3. Proposal front-matter includes:
   ```yaml
   ---
   target_article: path/to/original.md
   submitted_by: prichwil
   submitted_at: 2026-04-17
   change_type: addition | correction | rewrite | deletion
   rationale: One-line reason for the change
   ---
   ```
4. Submitter pings Richard (or the wiki librarian) to review.
5. Librarian either merges the change, requests revisions, or declines (with reason logged back to the submitter).

**Never push directly to canonical.** Always through intake.

## How to request a new article

If your agent detects a gap (topic keeps coming up in Slack/email/meetings but has no wiki article), it can propose a new one:

1. Drop a "topic brief" in `~/shared/wiki/intake/new-articles/<slug>.md` with:
   - Why this should exist (evidence: mentions count, recency)
   - Proposed category, markets, topics
   - 3–5 questions the article should answer
   - Sources to consult
2. Ping the wiki librarian.
3. Librarian routes through the wiki-writer pipeline (editor → researcher → writer → critic → librarian publishes).

Teammate agents don't run the whole pipeline themselves — they submit the topic brief and let the canonical pipeline handle it. Prevents drift in voice and structure.

## Reading patterns

### "What do we know about [topic]?" ``` 1. Search wiki index for topic keyword 2. Filter by status=FINAL (not reviews/drafts) unless user explicitly wants all 3. If >3 matches, show list with one-line summaries and ask user to pick 4. If 1–2 matches, read and synthesize 5. If 0 matches, say so and suggest submitting a new-article topic brief ``` ### "Summarize market X based on the wiki"

```
1. Filter wiki index by market=X
2. Prioritize: state-files > strategy > playbooks > callouts (latest 3)
3. Read top 5–7 most recent/relevant
4. Synthesize
5. Cite article paths so user can dig deeper
```

### "What's the latest test result on [topic]?"

```
1. Search wiki/testing/ and agent-created/testing/ for topic
2. Sort by date desc
3. Read the top result
4. Answer with test name, hypothesis, outcome, date
```

## Failure modes

- **Wiki index is stale** → run `python3 ~/shared/dashboards/build-wiki-index.py`. Fast (seconds) and regenerates both the JSON and `_meta/wiki-index.md`. Fallback: grep directly.
- **SharePoint cache is stale** → the builder prints `SharePoint cache as of: ...` when it runs. If that's days old, trigger the `wiki-maintenance` hook to refresh it, or ask an agent with SharePoint MCP access to re-list the 7 `Artifacts/<category>/` folders and overwrite `data/sharepoint-artifacts.json`.
- **Search returns nothing for a known article** → index hasn't been rebuilt since the article was added. Ask user to refresh.
- **Someone hand-edited `_meta/wiki-index.md`** → their changes will be overwritten on the next build. The file has an AUTO-GENERATED banner at the top. Edit `build-wiki-index.py`'s `write_wiki_index_md()` function instead.
- **Agent tries to edit canonical directly** → violation of intake rule. Restart with `wiki-contributor.md` steering loaded.
- **Intake folder fills up with unreviewed suggestions** → librarian process isn't running. Flag to Richard.

## Steering file for wiki contributors

Install at your Kiro steering folder as `wiki-contributor.md` (in `.kiro/steering/` inside your workspace, or `~/.kiro/steering/` for user-level):

```markdown
---
inclusion: always
---

# Wiki Contributor Rules

Before answering any question that might be covered by the team wiki, search the wiki first:
1. Remote IDE: search `~/shared/wiki/` or query `shared/dashboards/data/wiki_index.json`.
2. Local IDE: search the OneDrive-synced wiki mirror if available; otherwise use SharePoint MCP.
3. AgentSpaces: use SharePoint MCP search on the wiki mirror.

If a matching article exists, read it and cite the path in your answer.

Never edit the canonical wiki directly. All edits go through intake:
- Edit suggestions → `~/shared/wiki/intake/suggestions/<slug>-<alias>-YYYY-MM-DD.md`
- New article topic briefs → `~/shared/wiki/intake/new-articles/<slug>.md`

Include front-matter with target_article, submitted_by, submitted_at, change_type, rationale.

If no matching article exists and the topic is recurring, propose a new-article topic brief instead of just answering from general context.
```
