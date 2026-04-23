# Var2 — Standalone Always-On Steering Index File

**Mechanism:** Create a new always-on steering file `.kiro/steering/steering-index.md` that serves as a pure directory — agents see the index on bootstrap, know what's available by name + trigger, can decide to load.

**File content (to be created at `.kiro/steering/steering-index.md`):**

```markdown
---
inclusion: always
---

# Steering File Index

*Annotated directory of manual-inclusion steering files. Load the named file when the trigger matches your task. Keeping this index always-on solves the discovery problem without loading every file's contents.*

## Writing style files (load before producing professional prose)

| Task | Load |
|---|---|
| Slack DM or channel message | `richard-style-slack.md` |
| Email to colleague or exec | `richard-style-email.md` |
| WBR callout | `richard-style-wbr.md` |
| MBR section or monthly report | `richard-style-mbr.md` |
| Formal doc / PR-FAQ / 6-pager | `richard-style-docs.md` |
| Cross-Amazon communication | `richard-style-amazon.md` |
| Core writing voice reference | `richard-writing-style.md` |

## Analytical / operational files

| Task | Load |
|---|---|
| Projection / forecast / test readout / Excel drop | `performance-marketing-guide.md` |
| High-stakes output (>$50K or leadership-facing) | `high-stakes-guardrails.md` (auto-loads, no manual action) |
| MX forecasting, market data drill-downs | `performance-marketing-guide.md` + `market-constraints.md` (auto) |
| Task prioritization / time-blocking | `rw-task-prioritization.md` (auto) |
| WW testing loop prep | `ww-testing-loop-prep.md` |

## System / protocol files

| Task | Load |
|---|---|
| Evaluating proposed system changes | `blind-test-methodology.md` |
| Running an A/B test harness | `blind-test-harness.md` |
| Architecture-only review (no A/B possible) | `architecture-eval-protocol.md` |
| Enhanced bootstrap navigation | `enhanced-navigation-protocol.md` |
| Asana write operations | `asana-guardrails.md` |
| Slack search / deep context | `slack-deep-context.md` / `slack-knowledge-search.md` |

## Thought-pattern files (optional mental models)

| Task | Load |
|---|---|
| High-agency vs conservative tradeoff reasoning | `mario-peter-dichotomy.md` |
| Channeling specific mentors / styles | `influences.md` |

## Rule
If the task matches a trigger, load the file. If unsure, load the most likely match and proceed — a wrong file takes one readFile call to skip past, a missed file takes multiple turns to recover from.
```

---

**Expected impact:**
- Every agent gets the map on every session (always-on)
- Separation of concerns: soul.md stays focused on identity/principles, steering-index.md is pure routing
- Easy to maintain: adding a new manual file means updating one index, not editing soul.md
- Discoverable by humans too (Richard can grep it)

**Tradeoffs:**
- Adds one always-on file to every session (~60 lines of table content)
- Requires the agent to consult it — a mechanism that might be ignored if agent doesn't read auto-injected steering carefully
- Slight duplication with soul.md's existing Agent Routing section
