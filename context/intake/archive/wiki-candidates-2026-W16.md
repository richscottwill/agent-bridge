# Wiki Candidates Archive — 2026-W16 (2026-04-13 through 2026-04-19)

Archived during wiki-maintenance run on 2026-04-17. One candidate consumed.

## Consumed

```
[2026-04-17T18:16 session-summary] signal: Distributed-contribution pattern — hooks observe one-line signals, central consumer agent dedupes and acts; cheaper and more maintainable than a mega-orchestrator or per-hook judgment. | source: this-session | proposed: distributed-contribution-hook-pattern
```

**Disposition:** Promoted to review-queue.md as candidate proposal. Worth-a-doc signal, but low priority — this is meta-infrastructure, not paid-search content. Marked P3.

## Notes

First-ever consumption pass for this file. Only one entry accumulated over the week. Distributed-contribution pattern is working — hooks aren't spamming noise — but volume is also very low. Kill-condition watch: if by 2026-06-01 only a handful of entries have appeared and <3 articles have been promoted from Richard's review, delete the pattern.

---

## Second pass — appended 2026-04-17 evening run

Four new candidates consumed from wiki-candidates.md on 2026-04-17 19:00 PT. All from session-summary hook, all cluster into one theme: agent operating norms + wiki system architecture.

### Consumed

```
[2026-04-17T18:32 session-summary] signal: Richard directs agents to pick sensible defaults instead of asking about ordering/priority when the choice is low-stakes — reinforces soul.md principle #6 (reduce decisions, not options) as a cross-agent operating norm. | source: this-session | proposed: enrich: agent-architecture

[2026-04-17T18:42 session-summary] signal: When an agent flags a task as needing a "dedicated run" or "more focus," that framing is often caution-as-procrastination — if the data is already in context and the operation is reversible, default to doing it in-session rather than queuing. | source: this-session | proposed: enrich: agent-architecture

[2026-04-17T18:44 session-summary] signal: Wiki system has three disconnected surfaces (human-readable wiki-index.md, auto-crawled dashboard JSON, SharePoint published copies) with no single source of truth — "structural over cosmetic" (soul principle #2) argues for making the crawler authoritative and deriving the rest. | source: this-session | proposed: enrich: agent-architecture

[2026-04-17T18:58 session-summary] signal: Cache-and-derive pattern for cross-surface sync — expensive external calls (SharePoint MCP, Slack search) run once per cycle into a JSON snapshot; builder scripts read from cache and derive multiple outputs from one scan; avoids hammering external systems and keeps builder dependency-free. | source: this-session | proposed: enrich: agent-architecture
```

### Disposition

All 4 deduped into a single proposal: **enrich agent-architecture with a "Agent operating norms" section + a "Wiki system topology" section**. Both sections are meta-infrastructure and appropriate for the agent-architecture doc's audience (agent-facing + personal, not team-facing). Promoted to review-queue.md as one combined candidate.

Grouping rationale: signals #1 and #2 are both operating-norm observations (sensible defaults, caution-as-procrastination). Signals #3 and #4 are both wiki-system-architecture observations (single source of truth, cache-and-derive). Two adjacent sections, not two articles.

### Notes

Queue volume is low but signal quality is high — four related observations in one session, all pointing at the same article. That's exactly the pattern the distributed-contribution hook was designed to surface. Kill-condition watch stays on 2026-06-01; first proof point here that the pattern can produce coherent enrichments, not just noise.
