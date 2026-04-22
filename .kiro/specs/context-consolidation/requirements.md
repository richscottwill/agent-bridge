# Requirements Document: Context Consolidation

## Introduction

Create a single `ps-context-index.md` file that serves as a read-only index of all context files agents currently load at startup. Today, each agent definition (market-analyst, callout-writer, callout-reviewer, etc.) independently loads 2–4 context files before starting work — `callout-principles.md`, `callout-writer.md`, `richard-writing-style.md`, multiple style guides, and others spread across `~/shared/context/`. There is no single manifest of what gets loaded, no way to audit context overlap, and no mechanism to detect when an agent loads a stale or renamed file. This spec consolidates the context-loading surface into one index that agents read first, which references (not replaces) the source files.

This is consolidation, not creation. The goal is fewer files loaded per agent startup, not more content in the system. If the consolidated index file ends up larger than any individual source file it references, the design has failed.

**Origin**: `.kiro/specs/dashboard-learnings-roadmap/design.md` — Item #8 (Framework consolidation file). Ranked #8 of 13 roadmap items. Classification: `BUILD-STANDALONE`, effort M (1–3 days), leverage Medium. Sources: marketing-os-starter `marketing-wisdom.md` (single file all agents consult containing 6 Hook Formulas, BOFU Domination, 7 Growth Playbooks), coreyhaines31/marketingskills `product-marketing-context` (foundation file read by all 35+ skills first).

**Five Levels alignment**: L1 (Sharpen Yourself) — faster agent startup means faster artifact output. Reducing context-loading errors and redundant file reads directly supports the L1 key metric (consecutive weeks shipped) by eliminating a class of silent failures where an agent loads the wrong version of a context file or misses one entirely.

**Soul principle**: Subtraction before addition — this is consolidation, not creation. Fewer files loaded per agent invocation, same content available. The index replaces N scattered `#[[file:...]]` references across agent definitions with one canonical lookup. **Risk**: creating a monolith that's hard to maintain. Mitigated by keeping the consolidated file as a read-only index that references source files by path — it contains no content itself, only pointers and brief descriptions.

## Glossary

- **Context file**: Any markdown file in `~/shared/context/` (or its subdirectories) that an agent loads at startup to establish working knowledge — style guides, principles, writing rules, market context, system navigation files
- **Agent definition**: A markdown file that defines an agent's role, capabilities, routing triggers, and context dependencies — e.g., `market-analyst.md`, `callout-writer.md`, `callout-reviewer.md`
- **ps-context-index.md**: The new consolidated index file this spec creates — a read-only manifest listing every context file in the system with its path, purpose, and which agents consume it
- **Context loading**: The process by which an agent reads one or more context files at startup before performing its task. Currently done via `#[[file:...]]` references or explicit instructions in agent definitions.
- **Source file**: An existing context file (e.g., `callout-principles.md`, `richard-writing-style.md`) that contains actual content. The index references these files — it does not duplicate their content.
- **body.md**: The current navigation layer for the whole system — maps context file paths, organ locations, and system navigation. The index complements body.md by focusing specifically on agent context dependencies rather than system-wide navigation.
- **Five Levels**: Richard's sequential strategic priorities — L1 Sharpen Yourself → L2 Drive WW Testing → L3 Team Automation → L4 Zero-Click Future → L5 Agentic Orchestration
- **Soul principles**: The 6 "How I Build" principles in `soul.md` — Routine as liberation, Structural over cosmetic, Subtraction before addition, Protect the habit loop, Invisible over visible, Reduce decisions not options
- **Command Center**: Dashboard home view with Hero, Daily Blocks, Integrity Ledger, Actionable Intelligence

## Scope

### In scope

- Audit of all context files agents currently load at startup (full inventory with paths, sizes, and consumer agents)
- Creation of `ps-context-index.md` — a read-only index that lists every context file with: path, one-line purpose, which agents consume it, and last-verified date
- Update of agent definitions to reference the consolidated index as their first read, replacing scattered individual file references where appropriate
- Size constraint enforcement: the index file must be smaller than every individual source file it references
- Documentation of the audit findings: which files are loaded by multiple agents (overlap), which are loaded by zero agents (orphaned candidates for removal), and which have stale or broken references

### Out of scope

- Merging or combining the content of existing context files — the index references files, it does not absorb them
- Creating new context content — this is consolidation of existing material only
- Changing the content or structure of any source file (e.g., rewriting `callout-principles.md` or `richard-writing-style.md`)
- Automated context-loading infrastructure (e.g., a script that dynamically resolves the index at runtime) — the index is a static markdown file read by agents, not a programmatic dependency resolver
- Removing any context files — the audit may identify removal candidates, but actual removal is a separate decision requiring Richard's review
- Changes to `body.md` or `soul.md` — these are system-level navigation and identity files, not agent context files. The index complements them, it does not replace or modify them.
- Agent behavior changes — agents still do the same work; they just have a clearer map of what to load first

## Requirements

### Requirement 1: Context File Audit

**User Story**: As Richard, I want a complete inventory of every context file agents load at startup, so I can see the full picture of what's being loaded, by whom, and whether any files are redundant or orphaned.

#### Acceptance Criteria

1. WHEN the audit is performed, THEN it SHALL produce a complete list of every context file referenced by any agent definition, hook, or steering file in the system
2. WHEN a context file is listed in the audit, THEN the entry SHALL include: file path, file size (in lines or KB), one-line purpose description, and a list of every agent or process that references it
3. WHEN the audit identifies a context file referenced by 2+ agents, THEN it SHALL flag that file as "shared context" — these are the highest-value entries for the index
4. WHEN the audit identifies a context file referenced by zero agents (orphaned), THEN it SHALL flag it as a removal candidate with the note "verify with Richard before removing"
5. WHEN the audit identifies a broken reference (agent points to a file that doesn't exist or has been renamed), THEN it SHALL flag it as "broken reference — fix required" with the agent name and the broken path

### Requirement 2: Consolidated Index File

**User Story**: As an agent starting up, I want to read one index file first that tells me exactly which context files I need for my task, so I don't load unnecessary files or miss required ones.

#### Acceptance Criteria

1. WHEN `ps-context-index.md` is created, THEN it SHALL list every context file in the system organized by category (e.g., writing style, market context, system navigation, agent-specific)
2. WHEN a context file is listed in the index, THEN the entry SHALL include: file path, one-line purpose, and a tag list of consuming agents (e.g., `[callout-writer, callout-reviewer]`)
3. WHEN the index is created, THEN it SHALL include a per-agent lookup section — for each agent, a list of the context files it should load, in recommended read order
4. WHEN the index is created, THEN it SHALL be a read-only reference document — it contains file paths and descriptions, not duplicated content from the source files
5. WHEN the index is created, THEN its total size SHALL be smaller than every individual source file it references — if the index exceeds this constraint, it must be trimmed (per Subtraction before addition)

### Requirement 3: Agent Definition Updates

**User Story**: As Richard maintaining agent definitions, I want each agent to reference the consolidated index as its starting point, so I have one place to update when context files change instead of editing every agent definition individually.

#### Acceptance Criteria

1. WHEN an agent definition is updated, THEN it SHALL reference `ps-context-index.md` as the first context file to read (e.g., "Read ps-context-index.md first, then load the files listed for this agent")
2. WHEN an agent definition currently lists individual context file references, THEN those references SHALL be replaced with a pointer to the agent's section in the index — not duplicated alongside the index reference
3. WHEN an agent definition is updated, THEN the agent's behavior SHALL NOT change — the same context files are loaded, just discovered via the index instead of hardcoded in the definition
4. WHEN a new agent is added to the system in the future, THEN the index format SHALL be clear enough that the developer knows to add the agent's context dependencies to the index and reference it from the agent definition

### Requirement 4: Size Constraint Enforcement

**User Story**: As Richard living the Subtraction before addition principle, I want a hard constraint that the index file stays small — it's a table of contents, not an encyclopedia.

#### Acceptance Criteria

1. WHEN `ps-context-index.md` is created, THEN its file size in lines SHALL be smaller than the smallest source file it references — the index is always the lightest file in the context system
2. WHEN the index would exceed the size constraint (e.g., because too many files are listed with too-long descriptions), THEN descriptions SHALL be shortened to one line each rather than expanding the index
3. WHEN the index is reviewed, THEN it SHALL contain zero duplicated content from source files — only paths, one-line descriptions, and agent tags
4. WHEN the size constraint is checked, THEN the check SHALL be documented in the design with the specific line counts: index size vs smallest source file size

### Requirement 5: Orphan and Overlap Detection

**User Story**: As Richard, I want the consolidation process to surface context files that are loaded by nobody (orphans) or loaded by everyone (candidates for promotion to the index's "universal" section), so I can make informed decisions about what to keep, remove, or restructure.

#### Acceptance Criteria

1. WHEN the audit identifies files loaded by 3+ agents, THEN those files SHALL be listed in a "Universal Context" section at the top of the index — these are the files every agent should consider loading
2. WHEN the audit identifies files loaded by exactly 1 agent, THEN those files SHALL be listed only in that agent's section — they are agent-specific context, not shared
3. WHEN the audit identifies files loaded by zero agents, THEN those files SHALL be listed in an "Orphaned Files" appendix in the audit output with a recommendation: review for removal or re-link to an agent
4. WHEN the audit identifies two files with substantially overlapping content (e.g., two style guides covering the same writing rules), THEN it SHALL flag the overlap with a note: "potential merge candidate — review with Richard"

## Design Constraints

1. **No new infrastructure**: The index is a static markdown file. No scripts, no runtime resolution, no database entries. Agents read it the same way they read any other context file — as a text document.
2. **Read-only index**: The index is a reference document. It does not replace, merge, or modify any source file. Source files remain the authoritative content; the index is a map to them.
3. **Single-user assumption**: Richard is the sole maintainer. No multi-user editing workflow or conflict resolution needed for the index file.
4. **Backward compatibility**: Agents that don't yet reference the index should continue to work — the index is additive to the agent startup process, not a breaking change. Migration can be incremental.
5. **Portability**: The index must be understandable by a new AI on a different platform without access to Kiro-specific hooks, MCP servers, or subagents. It's a plain-text markdown file with relative paths and human-readable descriptions.
6. **Subtraction check**: This spec consolidates existing references into one file. It does not add new context content, new agent capabilities, or new data stores. The net effect should be fewer file references scattered across agent definitions, not more files in the system. If the implementation adds more complexity than it removes, it has failed.
