---
name: wiki-audit
description: "Audit published wiki articles for staleness, low usefulness, orphaned pages. Triggers on audit wiki, stale docs, which docs are stale, wiki quality."
---

# Wiki Audit (Critic)

## Instructions

1. **Scan published articles** — Review all published wiki articles for staleness indicators: last modified date, broken links, outdated references, orphaned pages with no inbound links.
2. **Score each article** — Assign a freshness score based on age, relevance, and link health. Flag articles that haven't been updated in 30+ days as potentially stale.
3. **Check usefulness** — Cross-reference articles against demand signals from wiki-search. Articles with zero search hits in the last 30 days may be candidates for archival.
4. **Identify orphans** — Find articles with no inbound links from other articles or body organs. These are likely undiscoverable.
5. **Generate report** — Produce a summary of stale, low-usefulness, and orphaned articles with recommended actions (update, archive, merge, delete).
6. **Log findings** — Save the audit report to ~/shared/context/intake/ for processing.

## Notes

- The critic reviews quality, not content. Content decisions go through the editor.
- Staleness thresholds may vary by article type — operational docs go stale faster than reference docs.
