---
inclusion: manual
---

# Steering File Integrity Rules

## Purpose
Prevents accidental resurrection of deleted steering files and duplication of content across steering files. This document is the authoritative record of intentional deletions and consolidations.

## Deleted Files — DO NOT RECREATE

These files were intentionally deleted. Any agent (including Karpathy) that recreates them is introducing a regression. If you see these files in ~/.kiro/steering/, delete them immediately.

| File | Deleted | Reason | Replacement |
|------|---------|--------|-------------|
| `agentspaces-core.md` | 2026-04-05 | Merged into environment-rules.md (kiro-setup-optimization spec, Req 2) | `environment-rules.md` |
| `devspaces-core.md` | 2026-04-05 | Merged into environment-rules.md (kiro-setup-optimization spec, Req 2) | `environment-rules.md` |
| `product.md` | 2026-04-05 | 100% duplicated by soul.md + body.md. Zero unique content. | `soul.md` (always) + `body.md` (via #[[file:]] ref) |
| `file-creation-rules.md` | 2026-04-05 | Absorbed into environment-rules.md File Operations section | `environment-rules.md` |

## Consolidation History

| Date | Action | Files Affected | Spec/Trigger |
|------|--------|---------------|-------------|
| 2026-04-03 | Merged agentspaces-core + devspaces-core → environment-rules | 3 files | kiro-setup-optimization Req 2 |
| 2026-04-04 | REGRESSION: Karpathy Run 23 resurrected deleted files | agentspaces-core, devspaces-core | Batch commit side effect |
| 2026-04-05 | Re-deleted zombies + deleted product.md + absorbed file-creation-rules | 4 files | Steering duplication audit |
| 2026-04-05 | Demoted tech.md, process-execution.md, amazon-builder-production-safety.md, pilot-steering.md from always → auto | 4 files | Token budget optimization |

## Duplication Rules (for any agent modifying steering files)

1. Before creating a new steering file, check if the content already exists in another file. If >50% overlap, extend the existing file instead.
2. Before restoring a deleted file from git history, check this document's Deleted Files table. If listed, do NOT restore.
3. soul.md is the single source of truth for: identity, Five Levels, agent routing, Instructions for Any Agent. No other always-loaded file should duplicate these.
4. environment-rules.md is the single source of truth for: DevSpaces/AgentSpaces identity, file operation boundaries, workspace rules. No other file should duplicate these.
5. When running batch commits (Karpathy experiments, EOD-2 housekeeping), verify that git staging does not include files from the Deleted Files table.

## Pre-Commit Check

Before any git commit that touches ~/.kiro/steering/:
1. Verify no files from the Deleted Files table are being added
2. Verify no new always-inclusion files duplicate content from soul.md
3. If a new steering file is being created, verify it has proper front matter with an inclusion mode
