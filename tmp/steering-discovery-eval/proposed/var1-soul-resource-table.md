# Var1 — Extended Soul Routing Directory with Canonical Resources Table

**Mechanism:** Extend `soul.md`'s Agent Routing Directory section with a second table titled "Canonical Resources by Task Type" that names the manual-inclusion steering file agents should load for each recurring task shape. Keeps everything in one always-on file (soul.md).

**Table content to add to soul.md (immediately after the existing Agent Routing Directory table):**

## Canonical Resources by Task Type

When the task matches a trigger below, load the named manual-inclusion steering file before producing output. Do not guess from first principles — the file is the canonical authority.

| Task shape / trigger | Load this file | Why |
|---|---|---|
| Slack message drafting | `richard-style-slack.md` | Slack tone differs from email; style file has the conventions |
| Email drafting / reply | `richard-style-email.md` | Signature, opener, tone norms |
| WBR callout (weekly business review) | `richard-style-wbr.md` + `richard-style-amazon.md` | WBR-specific narrative shape |
| MBR section (monthly business review) | `richard-style-mbr.md` + `richard-style-amazon.md` | MBR-specific discipline |
| Formal docs / PR-FAQ / 6-pager | `richard-style-docs.md` + `richard-style-amazon.md` | Amazon writing norms |
| Projection / forecast / test readout / Excel drop | `performance-marketing-guide.md` | Task-specific cognitive template for PS analytics |
| High-stakes output (>$50K, leadership-facing) | `high-stakes-guardrails.md` (auto-loads on keywords) | Explicit confidence / top-3 / review flag |
| Blind-testing a proposed system change | `blind-test-methodology.md` | 4-round protocol, failure modes, rubric |
| Proposing a new tool/hook/automation | `device.md` check (principle #8) + `blind-test-harness.md` if testing | Don't build, investigate first |
| Task prioritization / time-blocking | `rw-task-prioritization.md` (auto-loads on Asana context) | Task bucket conventions |
| Asana write operations | `asana-guardrails.md` | Permissioning, deprecated projects, write rules |
| Ad-hoc strategic coaching | route to `rw-trainer` agent | Deep leverage analysis |
| Loop protocol / experiment queue edits | route to `karpathy` agent | Gatekeeper for heart/gut/queue |
| Slack deep research / knowledge search | `slack-deep-context.md` or `slack-knowledge-search.md` | Search protocols |
| Architecture or proposal review (no A/B possible) | `architecture-eval-protocol.md` | Type D reasoning-only protocol |
| WW testing loop prep | `ww-testing-loop-prep.md` | Loop-specific structure |

**Rule:** If the task touches multiple triggers, load all applicable files. These are lightweight (<500 lines each) and the cost of loading is far less than the cost of guessing wrong.

---

**Expected impact:**
- Agents discover the right file on first pass rather than after mid-task correction
- No new always-on file (soul.md already loaded)
- One point of maintenance (soul.md) rather than two
- Structural subtraction: removes agent guessing, not adds

**Tradeoffs:**
- Soul.md grows ~20 lines (still small)
- Every agent session carries the full table even when task is trivial (low cost since it's a table, not content)
