---
inclusion: manual
---

# Dashboard Redesign Naming Convention

*Adopted 2026-04-30 after kiro-local + kiro-server ran two parallel 10-mockup redesigns in the same week and needed to disambiguate commit messages, CSS classes, and bus-thread tags.*

## Rule

When shipping mockup-driven redesigns, prefix the mockup ID with 2 letters identifying the target surface:

| Prefix | Surface | First sprint | Thread |
|---|---|---|---|
| `DR-M##` | dashboards/weekly-review.html (Dashboard Redesign) | 2026-04-30 | `dashboard-mockups-handoff` |
| `WR-M##` | Weekly Review (if split from DR later) | — | (placeholder) |
| `WS-M##` | dashboards/wiki-search.html (Wiki Search) | 2026-04-30 | `wiki-dashboard-redesign` |
| `MPE-M##` | dashboards/projection.html (MPE projection engine) | 2026-04-28 | embedded in mpe-findings.md |

When a new surface gets its own sprint, pick a distinct 2-letter prefix and add a row above. Avoid single-letter prefixes — they collide with existing `M1`, `M2` shorthand used in ad-hoc conversation.

## Where prefixes show up

- **Commit messages** — `feat(wiki-search): WS-M10 graph minimap (force-directed)`. The prefix appears as the first word after the scope parenthesis.
- **CSS classes** — `.ws-m10-*`, `.dr-m03-*`. Scoping prevents style bleed between dashboards rendered on the same page (shared `projection-design-system.css` tokens, different structural classes).
- **HTML section markers** — `<!-- WS-M10 (2026-04-30): ... -->`. Block comment above the section so grep can find every surface a mockup touches.
- **Bus-thread tags** — `tags: [wiki, ws-m10, shipped, graph-minimap]`. Use the lowercase-hyphen form.
- **Inline code comments** — `// WS-M10: force-directed layout, 90 nodes, requestAnimationFrame loop`.

## Why this matters

The first week both agents started shipping mockups in parallel, the commit `73073f1` (wiki-search M01+M02+M07+M11) was initially read as rolling back commit `1530cf2` (weekly-review M7) because both diffs touched `.wr-wbr612-*` CSS classes — the prefix collision caused 8 minutes of false-alarm mode and one bus post of eaten crow (`2026-04-30_dashboard-mockups-handoff/010_kiro-server.md`).

Without the prefix:
- grepping for "M7" returns both sprints' M7 work mixed together
- CSS class namespace collisions aren't obvious from the commit name alone
- bus tags are ambiguous when multiple sprints are active in the same week

With the prefix:
- `DR-M##` and `WS-M##` never collide
- CSS under `.dr-m07-*` is visually distinct from `.ws-m07-*` in the stylesheet
- bus readers can filter by prefix tag to see only one sprint's progress

## Anti-goals

- **Don't create a prefix for every dashboard file.** A dashboard only earns a prefix when it has a sprint's worth of mockups (≥5 numbered items). One-off redesigns stay in regular commit messages without a prefix.
- **Don't nest prefixes.** If a wiki-search sub-feature needs its own numbered sub-sprint, bump the WS range (WS-M101, WS-M102) or start a new prefix — don't write `WS-M10-A`, `WS-M10-B`.
- **Don't retroactively rename.** Old commits and CSS in flight at the time of the first collision (2026-04-30 AM) stay as-is. The rule applies forward.

## Meta — authorities

- **Prefix assignment** — kiro-server + kiro-local can add rows to the table above without routing. Use the agent-bus to announce.
- **Conflict resolution** — if two sprints propose the same prefix, the sprint with the earlier thread-start timestamp wins.
- **Retirement** — a prefix retires when its target surface is decomposed or deprecated. Move the row under a `## Retired` heading and note the commit that closed it out.
