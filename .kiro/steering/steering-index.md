---
inclusion: always
---

[38;5;10m> [0m# Steering File Index[0m[0m
[0m[0m
*Annotated directory of manual-inclusion steering files. Load the named file when the trigger matches your task. This index is always-on so agents know what's available without loading every file's contents. Adopted 2026-04-22 after blind discovery test (Var2 won 228/250 vs baseline 154/250).*[0m[0m
[0m[0m
**Example:** If a user asks "help me write a PR description," the agent scans this index, matches the trigger phrase "pull request" or "PR description," and loads only the `pr-writing.md` steering file—rather than loading all steering files into context. This keeps token usage low while ensuring the right guidance is applied.
## Writing style files — load before producing professional prose

| Task trigger | Load |
|---|---|
| Slack DM or channel message | `richard-style-slack.md` |
| Email to colleague or exec | `richard-style-email.md` |
| WBR callout (weekly business review) | `richard-style-wbr.md` + `richard-style-amazon.md` |
| MBR section or monthly report | `richard-style-mbr.md` + `richard-style-amazon.md` |
| Formal doc / PR-FAQ / 6-pager | `richard-style-docs.md` + `richard-style-amazon.md` |
| Amazon-wide / up-the-chain communication | `richard-style-amazon.md` |
| Core writing voice reference (auto-inclusion, foundational) | `richard-writing-style.md` |

## Analytical / operational files

| Task trigger | Load |
|---|---|
| Projection / forecast / test readout / Excel drop / market analysis | `performance-marketing-guide.md` |
| High-stakes output (>$50K or leadership-facing) | `high-stakes-guardrails.md` *(auto-loads on keywords)* |
| MX forecasting / AU drill-downs / market-specific analytics | `performance-marketing-guide.md` + `market-constraints.md` *(auto)* |
| Task prioritization / time-blocking / bucket assignment | `rw-task-prioritization.md` *(auto-loads)* |
| WW testing loop prep | `ww-testing-loop-prep.md` |
| OP1 draft or annual planning — tradeoff spine | `op1-kill-list-first.md` |

## Reviewer lens files — load before finalizing a draft that will go to a specific reader

| Task trigger | Load |
|---|---|
| Any draft headed to Brandon (1:1 prep, pre-Kate review, direct-manager email) | `lens-brandon.md` |
| Any draft headed to Kate (Testing Approach, MBR section, skip-level review) | `lens-kate.md` |
| Material landing at VP altitude (QBR talking points, Kate's upward story) | `lens-todd.md` |
| Draft going up the chain — pair lenses | Brandon → Kate → Todd in order |

## System / protocol files

| Task trigger | Load |
|---|---|
| Evaluating proposed system changes (external AI or internal) | `blind-test-methodology.md` |
| Running an A/B test harness | `blind-test-harness.md` |
| Architecture-only review (no A/B possible) | `architecture-eval-protocol.md` |
| Enhanced bootstrap / navigation protocol | `enhanced-navigation-protocol.md` |
| Asana write operations | `asana-guardrails.md` |
| Slack search / deep research / knowledge lookup | `slack-deep-context.md` or `slack-knowledge-search.md` |
| Karpathy experiments on structured files (hooks, JSON, Python) | `karpathy-file-type-awareness.md` |

## Thought-pattern files (optional mental models)

| Task trigger | Load |
|---|---|
| High-agency vs conservative tradeoff reasoning | `mario-peter-dichotomy.md` |
| Channeling specific mentors / styles in writing | `influences.md` |

## Routing to specialist agents (from soul.md Agent Routing Directory)

For reference — these route to sub-agents, not steering files:

| Task trigger | Route to agent |
|---|---|
| Career coaching, skip-level with Kate, 1:1 prep with Brandon, annual review, growth planning, Friday retrospective | `rw-trainer` |
| Loop protocol changes, heart.md/gut.md edits, hard-thing-selection protocol | `karpathy` |
| Wiki article authoring (after editor assignment) | `wiki-writer` |

## Rules

1. **If the task matches a trigger, load the file.** Do not guess from first principles — the file is the canonical authority for that task shape.
2. **If the task touches multiple triggers, load all applicable files.** These are lightweight (<500 lines each) and the cost of loading is far less than the cost of guessing wrong.
3. **"(auto)" means the file is already loaded** via fileMatch or always-inclusion — you don't need to explicitly load it, but knowing it's in context is useful.
4. **When routing to a specialist agent**, do NOT pre-load files that agent will read itself. rw-trainer, karpathy, and wiki-writer read their own context on invocation.
5. **A wrong-file load takes one tool call to skip past. A missed file takes multiple turns to recover from.** Bias toward loading when uncertain.
