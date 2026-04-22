# Requirements Document

## Introduction

Richard has never meaningfully used Kiro Skills or Kiro Powers despite having 9 skills and 3 powers installed by default. Meanwhile, the body system already codifies repetitive workflows through four overlapping mechanisms: steering files (auto-loaded instructions), hooks (event-triggered automation), subagents (delegated specialists), and organs (context files). Every new workflow Richard wants to encode has to be placed somewhere — but today the decision is ad-hoc, which leads to duplication, orphaned skills, and tooling Richard does not remember he has.

This spec defines an **adoption system** for skills and powers: a set of requirements the body must meet so that (a) Richard uses the existing skills instead of re-explaining workflows every session, (b) new workflows get routed to the right mechanism (skill vs. power vs. steering vs. hook vs. subagent) on the first try, and (c) anything Richard creates is safe given his sensitive-data environment and survives a platform move.

The scope is explicitly **adoption and governance**, not the creation of any specific new skill or power. This spec produces the decision framework, the inventory of candidates, and the safety rules. Concrete skill/power builds are downstream specs.

**Revision history**: Requirements revised 2026-04-22 after stress-test against on-disk corpus (9 SKILL.md + 4 POWER.md, none carrying the adoption-system metadata) and the completed system-subtraction-audit (archived at `~/shared/wiki/agent-created/archive/system-subtraction-audit-2026-04-22/`). Seven acceptance criteria revised across R4 (portability made advisory not enforcing), R5 (candidate identification replaced by pilot-on-existing-9 framing), and R6 (missed-skill detection replaced by Richard-feedback-driven logging). Full rationale in `design.md` revision-history block.

## Glossary

- **Kiro_Skill**: A markdown file at `~/.kiro/skills/{name}/SKILL.md` with frontmatter (name, description). Activated on demand via the `discloseContext` tool when the agent recognises keyword triggers. Loads specialised instructions into context only when relevant. Currently installed: bridge-sync, charts, coach, cr-tagging, sharepoint-sync, wbr-callouts, wiki-audit, wiki-search, wiki-write.
- **Kiro_Power**: An installable bundle at `~/.kiro/powers/installed/{name}/` containing POWER.md (knowledge base) and optionally mcp.json (MCP server configuration). Activated via the `kiroPowers` tool with action="activate". Powers can be Guided MCP Powers (include MCP servers) or Knowledge Base Powers (documentation only). Currently installed: power-builder, aws-agentcore, flow-gen.
- **Steering_File**: A markdown file at `~/.kiro/steering/{name}.md` that is always-loaded (global) or conditionally loaded. Used for identity, style guides, guardrails. Currently 21 files including soul.md, richard-style-*.md, environment-rules.md.
- **Hook**: A JSON configuration at `~/.kiro/hooks/{name}.kiro.hook` that triggers on IDE events (fileEdited, userTriggered, preToolUse, postToolUse, etc.). Currently 22 hooks including am-auto, eod, guard-email, wbr-callouts.
- **Subagent**: A JSON configuration at `~/.kiro/agents/{name}.json` defining a specialised agent invokable via the `invokeSubAgent` tool. Currently ~14 domain-specific agents (rw-trainer, karpathy, wiki-*, callout-*, etc.).
- **Organ**: A markdown context file in `~/shared/context/body/` that represents persistent state or reference content (body.md, brain.md, heart.md, etc.).
- **Mechanism**: Any of the five encoding targets above (skill, power, steering, hook, subagent, organ) — the set of places a new workflow can live.
- **Sensitive_Data_Class**: One of four data-handling tiers: (1) Public — already published externally; (2) Amazon_Internal — non-confidential internal Amazon information; (3) Amazon_Confidential — business-sensitive Amazon data (performance metrics, forecasts, pre-publication artifacts); (4) Personal_PII — PII of Richard, colleagues, or external parties. Classification drives where a skill/power may live and whether it may be shared via the agent-bridge repo.
- **Cold_Start_Safe**: A file is cold-start safe when a new agent on a different platform can understand and execute it using only the file's contents plus other files already in the agent-bridge repo — no reliance on local MCP servers, hooks, or subagents that may not exist on the new platform.
- **Mechanism_Routing_Decision**: The choice of which mechanism (skill, power, steering, hook, subagent, organ) a given workflow belongs in.
- **Adoption_System**: The body subsystem this spec defines — the inventory, classification, decision framework, and safety rules that together make skills and powers usable.

## Requirements

### Requirement 1: Inventory of existing skills and powers

**User Story:** As Richard, I want a single canonical list of every installed skill and power with what it does and whether I use it, so that I can see at a glance what capabilities I already have before creating anything new.

#### Acceptance Criteria

1. THE Adoption_System SHALL produce an inventory document listing every installed Kiro_Skill with its name, trigger keywords, one-line purpose, and current usage status (used / unused / unknown).
2. THE Adoption_System SHALL produce an inventory document listing every installed Kiro_Power with its name, type (Guided MCP vs Knowledge Base), one-line purpose, and current usage status.
3. WHEN a new Kiro_Skill or Kiro_Power is installed or uninstalled, THE Adoption_System SHALL update the inventory document within the same session.
4. THE inventory document SHALL be stored at a path that is accessible on both SSH and local environments (either `~/shared/context/` or SharePoint `Kiro-Drive/`).
5. IF an installed skill or power has not been invoked in the prior 30 days, THEN THE Adoption_System SHALL flag it in the inventory as a candidate for removal.

### Requirement 2: Mechanism routing decision framework

**User Story:** As Richard, I want a clear decision framework that tells me whether a new workflow should be a skill, power, steering file, hook, or subagent, so that I stop creating things in the wrong place and ending up with duplication.

#### Acceptance Criteria

1. THE Adoption_System SHALL define a decision framework that maps workflow characteristics (trigger type, frequency, specificity, data sensitivity, sharability) to exactly one primary Mechanism.
2. THE decision framework SHALL be documented in a single markdown file readable on both SSH and local environments.
3. WHEN Richard proposes a new workflow, THE agent SHALL apply the decision framework and state explicitly which Mechanism was selected and why before any file is created.
4. IF a proposed workflow could fit more than one Mechanism, THEN THE agent SHALL list all candidate mechanisms with tradeoffs and request Richard's choice before proceeding.
5. THE decision framework SHALL include at least one worked example for each of the six Mechanisms (skill, power, steering, hook, subagent, organ).
6. WHERE an existing skill, power, steering file, hook, subagent, or organ already covers the proposed workflow, THE agent SHALL surface the existing asset and ask whether to extend it rather than create a new one.

### Requirement 3: Sensitive-data classification for skills and powers

**User Story:** As Richard operating in an Amazon-internal environment, I want every skill and power to declare the data sensitivity tier it handles, so that I never accidentally commit Amazon confidential content to a public repo or share it across a platform boundary.

#### Acceptance Criteria

1. THE Adoption_System SHALL require every Kiro_Skill and Kiro_Power to declare a Sensitive_Data_Class in its metadata (Public, Amazon_Internal, Amazon_Confidential, or Personal_PII).
2. IF a Kiro_Skill or Kiro_Power reads or writes Amazon_Confidential or Personal_PII content, THEN THE Adoption_System SHALL prevent that skill or power from being synced to the agent-bridge GitHub repository.
3. WHEN a Kiro_Skill or Kiro_Power is declared Public or Amazon_Internal, THE Adoption_System SHALL permit inclusion in the agent-bridge repository.
4. THE Adoption_System SHALL define the four Sensitive_Data_Class tiers with concrete examples for each tier in a single reference document.
5. IF a Kiro_Skill or Kiro_Power has no declared Sensitive_Data_Class, THEN THE Adoption_System SHALL treat it as Amazon_Confidential until classified.
6. WHEN a skill or power writes files, THE Adoption_System SHALL require the declared output paths to be consistent with the Sensitive_Data_Class (e.g., Amazon_Confidential output must not go to any path synced to the agent-bridge repo).

### Requirement 4: Cold-start portability for skills and powers

**User Story:** As Richard, I want skills and powers that contain portable workflow knowledge to survive a platform migration, so that moving off Kiro does not erase the codified workflows I rely on.

#### Acceptance Criteria

1. THE Adoption_System SHALL define two portability tiers for skills and powers: Cold_Start_Safe (intent is self-contained in the file text) and Platform_Bound (depends on specific MCP servers, hooks, or subagents that may not exist elsewhere).
2. WHEN a Kiro_Skill or Kiro_Power is created, THE Adoption_System SHALL require the author to declare its portability tier.
3. WHERE a Kiro_Skill or Kiro_Power is declared Cold_Start_Safe, THE file content SHOULD be understandable to a new agent using only the file text plus other Cold_Start_Safe files, with no reliance on specific tool names, hook IDs, or subagent names unique to this environment. This is author intent, not a validator gate.
4. WHERE a Kiro_Skill or Kiro_Power is declared Platform_Bound, THE file MAY explicitly list the specific MCP servers, hooks, or subagents it depends on. Declaration is recommended as cold-start recovery documentation, not required.
5. IF a Kiro_Skill or Kiro_Power is declared Cold_Start_Safe but the portability validator detects Platform_Bound-indicator tokens (MCP tool names, `.kiro.hook` IDs, subagent names, `discloseContext`/`kiroPowers`) in its body, THEN THE Adoption_System SHALL emit an advisory finding listing the tokens. The finding is informational — the validator SHALL NOT reject the asset, auto-downgrade the tier, or modify the file. Richard decides whether to rewrite the body, update the declared tier, or proceed as-is.

### Requirement 5: Pilot on already-installed skills and powers

**User Story:** As Richard, I want to measure activation of the skills and powers I already have installed before building more, so that addition does not outrun subtraction and so the adoption gap is closed on existing assets first.

#### Acceptance Criteria

1. THE Adoption_System SHALL treat the 9 already-installed Kiro_Skills (bridge-sync, charts, coach, cr-tagging, sharepoint-sync, wbr-callouts, wiki-audit, wiki-search, wiki-write) and the 4 already-installed Kiro_Powers (aws-agentcore, flow-gen, hedy, power-builder) as the pilot cohort. The body.md / device.md / hook-inventory / subagent-inventory sources are reference data for future rounds only, not active candidate-generation inputs during the pilot window.
2. FOR each already-installed Kiro_Skill and Kiro_Power, THE Adoption_System SHALL record its current `status` (legacy | current | retired), the activation history from activation-log.jsonl, and — at touch-it-classify-it migration — the declared Sensitive_Data_Class, portability tier, trigger keywords, and owner_agent. Legacy assets are exempt from declaring classification fields until they are next edited.
3. THE Adoption_System SHALL distinguish pilot outcomes per asset as: KEEP (≥3 activations in the 30-day pilot window), PRUNE-CANDIDATE (fewer than 3 activations; surfaces in next Phase E review), or NEW-PROPOSAL (ad-hoc workflows that cleared the Routing Decision Tree's step 0, step 0.5, and step 1 gates without terminating, and therefore qualify for net-new creation).
4. WHERE a proposed new workflow overlaps an already-installed asset by ≥75% keyword/trigger match, THE Adoption_System SHALL NOT recommend creating a new skill or power for it. The Routing Decision Tree's step 1 EXTEND_EXISTING gate terminates the proposal and redirects to editing the existing asset.
5. THE Adoption_System SHALL rank pilot outcomes by activation count from activation-log.jsonl during the 30-day window. A leverage-ranking formula (frequency × reexplanation-cost × artifact-level / creation-cost) is reserved for future rounds where Phase 0 activation baseline has established a real gap that EXTEND_EXISTING cannot close.
6. THE pilot success criterion SHALL be: ≥3 activations per skill during the 30-day window AND at least 5 of the 9 installed skills activated at all. Skills failing the criterion become Phase E pruning candidates rather than replacements-to-build. New skills SHALL NOT be created during the pilot window unless the Routing Decision Tree terminates at CREATE_NEW AND the overlap-check surfaces no viable EXTEND_EXISTING on the installed 9.

### Requirement 6: Adoption habit integration

**User Story:** As Richard, I want the skills I have installed to surface naturally during the work that would benefit from them, so that adoption happens by default rather than requiring me to remember a tool exists.

#### Acceptance Criteria

1. WHEN the agent detects a keyword or workflow in Richard's request that matches an installed Kiro_Skill or the `keywords` field of an installed Kiro_Power, THE agent SHALL activate the asset via `discloseContext` (skill) or `kiroPowers activate` (power) before producing the response.
2. WHEN Richard explicitly identifies an un-activated skill or power that would have helped, THE Adoption_System SHALL log a `{"event": "missed-by-feedback", ...}` entry in the activation log with the named asset, Richard's feedback text (≤200 chars), session id, and timestamp. THE agent SHALL NOT attempt automated pre-send or post-draft detection of missed skills — no platform event exists between response draft and response send, and any convention-based self-check reintroduces the "remember to remember" failure mode skills were designed to eliminate.
3. THE Adoption_System SHALL log every Kiro_Skill and Kiro_Power activation to a durable location (DuckDB table, SharePoint file, or local JSONL) that persists across sessions.
4. THE activation log SHALL record the skill/power name, the triggering request summary, the session context, and the timestamp.
5. WHERE a Kiro_Skill has been installed for more than 14 days and never activated, THE Adoption_System SHALL surface this in a periodic review (e.g., Friday retrospective or EOD summary).

### Requirement 7: Safe creation workflow for new skills and powers

**User Story:** As Richard, I want creating a new skill or power to follow a guarded, reviewable process, so that I do not commit sensitive data or ship a broken skill that pollutes future sessions.

#### Acceptance Criteria

1. WHEN Richard requests creation of a new Kiro_Skill or Kiro_Power, THE agent SHALL apply the Mechanism_Routing_Decision framework (Requirement 2) before creating any files.
2. THE agent SHALL present the proposed skill or power content to Richard for review before writing files to `~/.kiro/skills/` or `~/.kiro/powers/installed/`.
3. THE proposed content review SHALL include the declared Sensitive_Data_Class, portability tier, trigger keywords, and any referenced Platform_Bound assets.
4. IF the proposed Kiro_Skill or Kiro_Power contains Amazon_Confidential content, THEN THE agent SHALL confirm with Richard that the file will be written only to paths not synced to the agent-bridge repo.
5. WHEN a Kiro_Skill or Kiro_Power is created, THE Adoption_System SHALL update the inventory document (Requirement 1) in the same session.
6. THE Adoption_System SHALL provide a validation step that confirms a newly created skill or power can be successfully activated (via discloseContext for skills, kiroPowers activate for powers) before the creation is considered complete.

### Requirement 8: Pruning and deprecation of unused skills and powers

**User Story:** As Richard, I want unused skills and powers to be removed or archived on a regular cadence, so that the skill inventory trends simpler over time rather than accumulating dead weight.

#### Acceptance Criteria

1. THE Adoption_System SHALL provide a pruning review that lists every Kiro_Skill and Kiro_Power flagged as unused for 30 days or more (from Requirement 1.5).
2. WHEN Richard approves a skill or power for removal, THE Adoption_System SHALL remove it from `~/.kiro/skills/` or `~/.kiro/powers/installed/` and update the inventory document.
3. THE Adoption_System SHALL archive removed skill and power files to a dated archive location before deletion so that prior versions are recoverable.
4. IF a skill or power has been activated at least once in the prior 30 days, THEN THE Adoption_System SHALL NOT flag it for pruning.
5. THE pruning review SHALL run on a defined cadence (e.g., monthly) rather than ad-hoc.

### Requirement 9: Round-trip guarantee for the skill and power file format

**User Story:** As Richard, I want the format of my skills and powers to survive being read, edited by an agent, and written back without corruption, so that I can trust automated maintenance of these files.

#### Acceptance Criteria

1. THE Adoption_System SHALL define a canonical file format for Kiro_Skill SKILL.md (frontmatter with name and description, followed by markdown body).
2. THE Adoption_System SHALL define a canonical file format for Kiro_Power POWER.md (frontmatter with name, displayName, description, keywords, author, followed by markdown body).
3. WHEN a Kiro_Skill or Kiro_Power file is parsed and then re-serialized by the Adoption_System, THE resulting file SHALL be semantically equivalent to the original (round-trip property — parse then print then parse yields an equivalent structure).
4. IF a Kiro_Skill or Kiro_Power file does not match the canonical format, THEN THE Adoption_System SHALL return a descriptive error identifying the violation rather than silently rewriting the file.
5. THE Adoption_System SHALL include a validator that reports, for any skill or power file, whether it is format-compliant and whether its declared metadata (Sensitive_Data_Class, portability tier) is present.

### Requirement 10: No duplication with existing mechanisms

**User Story:** As Richard, I want the skills and powers adoption system to actively prevent duplication with the hooks, subagents, steering files, and organs I already have, so that adding skills does not increase total system complexity.

#### Acceptance Criteria

1. BEFORE creating a new Kiro_Skill or Kiro_Power, THE Adoption_System SHALL search the existing hooks, subagents, steering files, and organs for semantic overlap with the proposed workflow.
2. IF semantic overlap is detected with an existing Hook, Subagent, Steering_File, or Organ, THEN THE Adoption_System SHALL present the overlapping asset to Richard and require an explicit decision to (a) extend the existing asset, (b) create the new skill/power anyway with a documented reason, or (c) cancel.
3. WHEN a new Kiro_Skill or Kiro_Power is created, THE Adoption_System SHALL record which existing assets were considered during the overlap check and why the new asset was chosen over extending them.
4. THE Adoption_System SHALL reject creation of a Kiro_Skill or Kiro_Power whose only function is to re-invoke an existing Subagent (the Subagent is the correct mechanism; a skill wrapping it adds no value).
5. THE Adoption_System SHALL permit creation of a Kiro_Skill that orchestrates multiple Subagents or multiple MCP tools in a specific sequence, as this is the skill's legitimate value-add over any single Subagent.
