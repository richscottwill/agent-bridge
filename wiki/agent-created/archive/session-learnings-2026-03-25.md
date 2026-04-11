<!-- DOC-0143 | duck_id: context-session-learnings-2026-03-25 -->
# Session Learnings — 2026-03-25

## Wiki Team Pipeline
- Pipeline works: researcher → writer → critic → revise → publish. Editor orchestrates. Concierge handles search/lookup independently.
- The critic is a **required gate**, not optional. Skipping it produces 6/10 output. With it, 8/10 is the floor.
- 8/10 quality bar produces measurably better output than 7/10. The extra pass catches weasel words, unsupported claims, and structural gaps.
- Weasel word detection should be a standard critic check on every article. ("Significant," "various," "numerous" — replace with specifics or cut.)
- Dual front-matter (wiki metadata + artifact metadata) enables unified publishing across both systems.

## Context & Navigation
- Context catalog (`~/shared/context/wiki/context-catalog.md`) eliminates the "scour through everything" problem. Any agent finds the right source in <10 seconds.
- Artifacts folder (`~/shared/artifacts/`) is the canonical output location. Wiki infrastructure (staging, research, reviews) is process. Don't confuse the two.

## Agent Organization
- Agent subfolders work for .md agents (e.g., `~/.kiro/agents/wiki-team/`) but NOT for .json agents — kiro-cli limitation. JSON agents must stay in the root agents folder.
- Three subfolder structure adopted: `body-system/`, `wbr-callouts/`, `wiki-team/`.

## For Processing
- Route to: Device (wiki team as installed app — DONE), Spine (directory map + build history — DONE), Body (wiki/artifacts rows — DONE)
- Remaining: gut.md word budget table may need update after these additions
