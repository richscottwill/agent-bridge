---
name: wiki-search
description: "Search published wiki articles, synthesize answers, track demand signals. Triggers on search wiki, find doc, do we have a doc on, wiki lookup."
---

# Wiki Search (Concierge)

## Instructions

The wiki-concierge can be invoked directly for search and lookup — it does not require the editor to assign work.

1. **Receive query** — Understand what the user is looking for. Clarify if the request is ambiguous.
2. **Search published articles** — Search the wiki index and published articles for matches. Check titles, tags, and content.
3. **Synthesize answer** — If found, present a summary with a link to the full article. If multiple articles are relevant, rank by relevance.
4. **Track demand signal** — If no article exists, log the query as a demand signal to ~/shared/context/intake/ so the wiki-editor can prioritize future writing.
5. **Suggest creation** — If the topic has high demand (multiple searches, no article), suggest creating one via the /wiki-write skill.

## Notes

- This is the only wiki agent that can be invoked directly without the editor.
- Demand signals help prioritize what to document next.
