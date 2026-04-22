# Kill List — System Subtraction Audit

**Generated**: 2026-04-21T23:45:13-07:00
**classified.json hash**: `sha256:eb0dd07a3a6d273cd635cffd6279a5f64bbc776477a2f08feda65321c7017341`
**Files reviewed**: 99 across 4 layers

**Karpathy carve-out**: WAIVED for this run per Richard. All files including heart.md, gut.md, hard-thing-selection.md, and experiments/* are classified normally.

**Unsearched reference sources** (per R2.10): DuckDB rows, Asana task descriptions, Slack messages, Outlook emails. A file referenced only by these sources will appear orphaned here.

## Summary

**Per-layer**:

| Layer     | Files | Lines | DELETE | MERGE | UNCLEAR | KEEP | KARPATHY |
|-----------|-------|-------|--------|-------|---------|------|----------|
| body      |    15 |  3588 |      0 |     0 |       5 |   10 |        0 |
| protocol  |    29 |  6429 |      5 |     0 |       0 |   24 |        0 |
| hook      |    23 |   280 |     12 |     0 |       0 |   11 |        0 |
| steering  |    32 |  3432 |      6 |     0 |       0 |   26 |        0 |

**Aggregate**:
- DELETE: 23 files (~962 lines)
- MERGE: 0
- UNCLEAR: 5
- KEEP: 71
- KARPATHY-FLAG: 0
- BROKEN REFS: 300

**If all DELETE approved**: ~962 lines removed (~7.0% of current surface).

---

## Bulk Approval Block

Edit this block to approve, veto, or defer rows. The executor only acts on explicitly APPROVED rows.

Syntax:
- `APPROVE: B-D1, B-D3, P-D1-P-D5` (IDs or ranges)
- `VETO: P-D3` (block specific rows inside an approved range)
- `DEFER: U1, U3` (explicitly carry to next cycle, suppresses default-if-unanswered)

Absence of veto is NOT approval. Unapproved rows are skipped.

```text
APPROVE:
VETO:
DEFER:
```

---

## How to use this file

1. Read top-to-bottom. Each row is one file with a recommended action.
2. Add row IDs to `APPROVE:` above to approve them for execution.
3. Add row IDs to `VETO:` to block specific rows inside an approved range.
4. Add UNCLEAR row IDs to `DEFER:` to suppress the default action.
5. Rows you don't address remain for the next cycle.

---

## Incomplete classifications

*(none)*

---

## Broken references to fix (not audit candidates)

Total broken references found: **300**. Full list in `broken_refs.json`. Showing 20 with highest referrer-concentration:

### ~/shared/tools/wiki-asana-sync/sync-batch.json — 53 broken references
- Line 7: `~/shared/wiki/reporting/2026-03-25-ai-automation-impact.md` — remove reference OR create target file
- Line 37: `~/shared/wiki/reporting/2026-03-25-au-keyword-cpa-dashboard.md` — remove reference OR create target file
- Line 65: `~/shared/wiki/reporting/2026-03-25-wbr-callout-guide.md` — remove reference OR create target file
- Line 93: `~/shared/wiki/operations/2026-03-25-stakeholder-comms-guide.md` — remove reference OR create target file
- Line 126: `~/shared/wiki/testing/2022-10-yahoo-jp-nb-experiment.md` — remove reference OR create target file
- *... and 48 more in this file*

### ~/shared/tools/sharepoint-sync/.sync-manifest.json — 25 broken references
- Line 102: `/home/prichwil/shared/wiki/agent-created/markets/au-market-overview.md` — remove reference OR create target file
- Line 118: `/home/prichwil/shared/wiki/agent-created/markets/au-paid-search-market-overview.md` — remove reference OR create target file
- Line 142: `/home/prichwil/shared/wiki/agent-created/markets/oci-execution-guide.md` — remove reference OR create target file
- Line 150: `/home/prichwil/shared/wiki/agent-created/markets/oci-implementation-guide.md` — remove reference OR create target file
- Line 158: `/home/prichwil/shared/wiki/agent-created/markets/polaris-rollout-status.md` — remove reference OR create target file
- *... and 20 more in this file*

### ~/shared/wiki/agent-created/_meta/context-catalog.md — 19 broken references
- Line 62: `~/shared/context/active/session-bootstrap.md` — remove reference OR create target file
- Line 65: `~/shared/context/active/portable-layer.md` — remove reference OR create target file
- Line 66: `~/shared/context/active/morning-routine-experiments.md` — remove reference OR create target file
- Line 76: `~/shared/wiki/callouts/callout-principles.md` — remove reference OR create target file
- Line 91: `~/shared/wiki/research/op1-ps-testing-framework-draft.md` — remove reference OR create target file
- *... and 14 more in this file*

### ~/shared/dashboards/data/wiki-docs/1b1f7dc0ba.txt — 19 broken references
- Line 51: `~/shared/context/active/session-bootstrap.md` — remove reference OR create target file
- Line 54: `~/shared/context/active/portable-layer.md` — remove reference OR create target file
- Line 55: `~/shared/context/active/morning-routine-experiments.md` — remove reference OR create target file
- Line 65: `~/shared/wiki/callouts/callout-principles.md` — remove reference OR create target file
- Line 80: `~/shared/wiki/research/op1-ps-testing-framework-draft.md` — remove reference OR create target file
- *... and 14 more in this file*

### ~/.kiro/agents/body-system/agent-bridge-sync.md — 9 broken references
- Line 27: `~/shared/context/active/portable-layer.md` — remove reference OR create target file
- Line 41: `~/.kiro/steering/rw-trainer.md` — remove reference OR create target file
- Line 43: `~/shared/context/active/morning-routine-experiments.md` — remove reference OR create target file
- Line 44: `~/shared/wiki/callouts/callout-principles.md` — remove reference OR create target file
- Line 46: `~/shared/context/active/portable-layer.md` — remove reference OR create target file
- *... and 4 more in this file*

### ~/shared/wiki/agent-created/_meta/audit-2026-04-17-run2.md — 9 broken references
- Line 37: `~/shared/research/competitor-intel.md` — remove reference OR create target file
- Line 39: `~/shared/artifacts/program-details/2026-03-25-body-system-architecture.md` — remove reference OR create target file
- Line 41: `~/shared/artifacts/strategy/2026-03-25-agentic-marketing-landscape.md` — remove reference OR create target file
- Line 43: `~/shared/artifacts/strategy/2026-03-30-ieccp-planning-framework.md` — remove reference OR create target file
- Line 45: `~/shared/artifacts/best-practices/2026-03-25-invoice-po-process-guide.md` — remove reference OR create target file
- *... and 4 more in this file*

### ~/shared/dashboards/data/wiki-docs/ed5451b47b.txt — 9 broken references
- Line 26: `~/shared/research/competitor-intel.md` — remove reference OR create target file
- Line 28: `~/shared/artifacts/program-details/2026-03-25-body-system-architecture.md` — remove reference OR create target file
- Line 30: `~/shared/artifacts/strategy/2026-03-25-agentic-marketing-landscape.md` — remove reference OR create target file
- Line 32: `~/shared/artifacts/strategy/2026-03-30-ieccp-planning-framework.md` — remove reference OR create target file
- Line 34: `~/shared/artifacts/best-practices/2026-03-25-invoice-po-process-guide.md` — remove reference OR create target file
- *... and 4 more in this file*

### ~/.kiro/agents/wiki-team/wiki-librarian.md — 8 broken references
- Line 30: `~/shared/wiki/wiki-structure.md` — remove reference OR create target file
- Line 33: `~/shared/wiki/wiki-structure.md` — remove reference OR create target file
- Line 36: `~/shared/wiki/wiki-index.md` — remove reference OR create target file
- Line 39: `~/shared/wiki/SITEMAP.md` — remove reference OR create target file
- Line 41: `~/shared/wiki/markdown-to-xwiki.md` — remove reference OR create target file
- *... and 3 more in this file*

### ~/shared/dashboards/data/wiki-docs/500b575ae6.txt — 6 broken references
- Line 19: `~/shared/artifacts/testing/2026-03-25-oci-rollout-playbook.md` — remove reference OR create target file
- Line 19: `~/shared/artifacts/strategy/2026-04-04-oci-business-case.md` — remove reference OR create target file
- Line 31: `~/shared/artifacts/testing/2026-03-25-oci-rollout-playbook.md` — remove reference OR create target file
- Line 64: `~/shared/artifacts/testing/2026-03-25-oci-rollout-playbook.md` — remove reference OR create target file
- Line 68: `~/shared/artifacts/testing/2026-03-25-oci-rollout-playbook.md` — remove reference OR create target file
- *... and 1 more in this file*

### ~/.kiro/agents/wiki-team/wiki-concierge.md — 5 broken references
- Line 17: `~/shared/wiki/wiki-index.md` — remove reference OR create target file
- Line 47: `~/shared/wiki/demand-log.md` — remove reference OR create target file
- Line 62: `~/shared/wiki/demand-report.md` — remove reference OR create target file
- Line 90: `~/shared/wiki/wiki-index.md` — remove reference OR create target file
- Line 91: `~/shared/context/active/context-catalog.md` — remove reference OR create target file

### ~/.kiro/specs/slack-deep-context/design.md — 5 broken references
- Line 632: `~/shared/portable-body/voice/richard-style-slack.md` — update path to /home/prichwil/.kiro/steering/richard-style-slack.md (file exists there)
- Line 763: `~/shared/context/wiki/demand-log.md` — remove reference OR create target file
- Line 869: `~/shared/portable-body/voice/richard-style-slack.md` — update path to /home/prichwil/.kiro/steering/richard-style-slack.md (file exists there)
- Line 876: `~/shared/context/wiki/demand-log.md` — remove reference OR create target file
- Line 913: `~/shared/portable-body/voice/richard-style-slack.md` — update path to /home/prichwil/.kiro/steering/richard-style-slack.md (file exists there)

### ~/shared/dashboards/data/wiki-docs/50f97dc5b3.txt — 5 broken references
- Line 25: `~/shared/artifacts/program-details/2026-04-04-oci-execution-guide.md` — remove reference OR create target file
- Line 25: `~/shared/artifacts/strategy/2026-04-04-oci-business-case.md` — remove reference OR create target file
- Line 150: `~/shared/artifacts/program-details/2026-04-04-oci-execution-guide.md` — remove reference OR create target file
- Line 151: `~/shared/artifacts/strategy/2026-04-04-oci-business-case.md` — remove reference OR create target file
- Line 155: `~/shared/artifacts/strategy/2026-03-25-competitive-landscape.md` — remove reference OR create target file

### ~/shared/dashboards/data/wiki-docs/733e12c0f5.txt — 5 broken references
- Line 25: `~/shared/artifacts/program-details/2026-04-04-oci-execution-guide.md` — remove reference OR create target file
- Line 25: `~/shared/artifacts/strategy/2026-04-04-oci-business-case.md` — remove reference OR create target file
- Line 134: `~/shared/artifacts/program-details/2026-04-04-oci-execution-guide.md` — remove reference OR create target file
- Line 135: `~/shared/artifacts/strategy/2026-04-04-oci-business-case.md` — remove reference OR create target file
- Line 139: `~/shared/artifacts/strategy/2026-03-25-competitive-landscape.md` — remove reference OR create target file

### ~/.kiro/hooks/wiki-maintenance.kiro.hook — 3 broken references
- Line 8: `~/shared/context/intake/archive/wiki-candidates-YYYY-WNN.md` — remove reference OR create target file
- Line 8: `~/shared/wiki/agent-created/_meta/health-YYYY-MM-DD.md` — remove reference OR create target file
- Line 8: `~/shared/wiki/agent-created/_meta/audit-YYYY-MM-DD.md` — remove reference OR create target file

### ~/.kiro/agents/wiki-team/wiki-critic.md — 3 broken references
- Line 194: `~/shared/wiki/agent-created/_meta/ready-for-final.md` — remove reference OR create target file
- Line 211: `~/shared/wiki/agent-created/_meta/revision-queue.md` — remove reference OR create target file
- Line 222: `~/shared/wiki/agent-created/_meta/escalations.md` — remove reference OR create target file

### ~/.kiro/steering/slack-deep-context.md — 3 broken references
- Line 269: `~/shared/context/voice/richard-style-slack.md` — update path to /home/prichwil/.kiro/steering/richard-style-slack.md (file exists there)
- Line 281: `~/shared/context/voice/richard-style-slack.md` — update path to /home/prichwil/.kiro/steering/richard-style-slack.md (file exists there)
- Line 696: `~/shared/wiki/demand-log.md` — remove reference OR create target file

### ~/shared/context/active/karpathy-loop-run2.log — 3 broken references
- Line 1025: `~/shared/wiki/meetings/manager/brandon-sync.md` — remove reference OR create target file
- Line 6577: `~/shared/context/body/soul.md` — update path to /home/prichwil/.kiro/steering/soul.md (file exists there)
- Line 24676: `~/.kiro/agents/eval-a.md` — remove reference OR create target file

### ~/shared/dashboards/data/wiki-docs/ff78c23329.txt — 3 broken references
- Line 20: `~/shared/artifacts/program-details/2026-03-25-oci-implementation-guide.md` — remove reference OR create target file
- Line 20: `~/shared/artifacts/communication/2026-03-25-oci-methodology-knowledge-share.md` — remove reference OR create target file
- Line 89: `~/shared/artifacts/program-details/2026-03-25-oci-implementation-guide.md` — remove reference OR create target file

### ~/.kiro/agents/AIPowerUserCapabilities-gpu-coder.json — 2 broken references
- Line 12: `/home/prichwil/.aim/packages/AIPowerUserCapabilities-1.0/eventId-6431234474/context/gpu-coder/AGENTS.md` — remove reference OR create target file
- Line 13: `/home/prichwil/.aim/packages/AIPowerUserCapabilities-1.0/eventId-6431234474/context/gpu-coder/cr-review-loop.md` — remove reference OR create target file

### ~/.kiro/agents/body-system/rw-trainer.md — 2 broken references
- Line 15: `~/.kiro/steering/rw-trainer.md` — remove reference OR create target file
- Line 40: `~/shared/context/intake/annual-review-2026-analysis.md` — remove reference OR create target file


---

## Body layer (15 files, 3588 lines)

### UNCLEAR — body layer (5 rows)

#### B-U1. `/home/prichwil/shared/context/body/amcc.md`  [358 lines, AUTO-INCLUDED-REFERRER, MEDIUM confidence]
- **Question**: /home/prichwil/shared/context/body/amcc.md is referenced from always-auto-loaded steering. Approve coordinated removal via separate spec, or keep?
- **Default if unanswered (30 days)**: KEEP (per R5.6 — coordinated removal needs separate spec)
- **Active referrers**: 124
- **Prior context**: [2026-04-03] Topic: Grok AI swarm agent personas — 8 custom instructions for xAI Grok | Actions: Read body.md, brain.md, amcc.md for grounding; wrote 4 refined 

#### B-U4. `/home/prichwil/shared/context/body/brain.md`  [168 lines, AUTO-INCLUDED-REFERRER, MEDIUM confidence]
- **Question**: /home/prichwil/shared/context/body/brain.md is referenced from always-auto-loaded steering. Approve coordinated removal via separate spec, or keep?
- **Default if unanswered (30 days)**: KEEP (per R5.6 — coordinated removal needs separate spec)
- **Active referrers**: 60
- **Prior context**: [2026-04-03] Topic: Grok AI swarm agent personas — 8 custom instructions for xAI Grok | Actions: Read body.md, brain.md, amcc.md for grounding; wrote 4 refined 

#### B-U5. `/home/prichwil/shared/context/body/spine.md`  [133 lines, AUTO-INCLUDED-REFERRER, MEDIUM confidence]
- **Question**: /home/prichwil/shared/context/body/spine.md is referenced from always-auto-loaded steering. Approve coordinated removal via separate spec, or keep?
- **Default if unanswered (30 days)**: KEEP (per R5.6 — coordinated removal needs separate spec)
- **Active referrers**: 64
- **Prior context**: [2026-04-07] Topic: README updated for new repo structure | Actions: Rewrote shared/README.md to reflect current structure (wiki/, context/, tools/, data/, uplo

#### B-U3. `/home/prichwil/shared/context/body/body.md`  [88 lines, AUTO-INCLUDED-REFERRER, MEDIUM confidence]
- **Question**: /home/prichwil/shared/context/body/body.md is referenced from always-auto-loaded steering. Approve coordinated removal via separate spec, or keep?
- **Default if unanswered (30 days)**: KEEP (per R5.6 — coordinated removal needs separate spec)
- **Active referrers**: 120
- **Prior context**: [2026-04-03] Topic: Grok AI swarm agent personas — 8 custom instructions for xAI Grok | Actions: Read body.md, brain.md, amcc.md for grounding; wrote 4 refined 

#### B-U2. `/home/prichwil/shared/context/body/body-diagram.md`  [181 lines, BODY-LIGHTLY-USED, LOW confidence]
- **Question**: /home/prichwil/shared/context/body/body-diagram.md has 1 active referrers. INFORMATION (keep) or METAPHOR-ONLY (delete)? Name the current workflow OR an L3-L5 future workflow that needs it.
- **Default if unanswered (30 days)**: KEEP
- **Active referrers**: 1
- **Prior context**: [2026-04-20] Topic: Hard-thing redesign PROMOTED to live | Actions: Executed README promotion checklist. Applied amcc-patch (section replacement in body/amcc.md


### KEEP — body layer (10 rows)

#### B-K2. `/home/prichwil/shared/context/body/changelog.md`  [758 lines, INFORMATION, HIGH confidence]
- **Rationale**: 29 active path referrers — workflows depend on this file.
- **Current usage**: Referenced by multiple agents/hooks
- **Active referrers**: 29  **Blast radius**: HIGH

#### B-K7. `/home/prichwil/shared/context/body/heart.md`  [300 lines, INFORMATION, HIGH confidence]
- **Rationale**: 118 active path referrers — workflows depend on this file.
- **Current usage**: Referenced by multiple agents/hooks
- **Active referrers**: 118  **Blast radius**: HIGH

#### B-K10. `/home/prichwil/shared/context/body/roster.md`  [248 lines, INFORMATION, HIGH confidence]
- **Rationale**: 39 active path referrers — workflows depend on this file.
- **Current usage**: Referenced by multiple agents/hooks
- **Active referrers**: 39  **Blast radius**: HIGH

#### B-K8. `/home/prichwil/shared/context/body/memory.md`  [245 lines, INFORMATION, HIGH confidence]
- **Rationale**: 159 active path referrers — workflows depend on this file.
- **Current usage**: Referenced by multiple agents/hooks
- **Active referrers**: 159  **Blast radius**: HIGH

#### B-K3. `/home/prichwil/shared/context/body/device.md`  [240 lines, INFORMATION, HIGH confidence]
- **Rationale**: 93 active path referrers — workflows depend on this file.
- **Current usage**: Referenced by multiple agents/hooks
- **Active referrers**: 93  **Blast radius**: HIGH

#### B-K1. `/home/prichwil/shared/context/body/amazon-politics.md`  [213 lines, INFORMATION, HIGH confidence]
- **Rationale**: 5 active path referrers — workflows depend on this file.
- **Current usage**: Referenced by multiple agents/hooks
- **Active referrers**: 5  **Blast radius**: HIGH

#### B-K5. `/home/prichwil/shared/context/body/gut.md`  [196 lines, INFORMATION, HIGH confidence]
- **Rationale**: 92 active path referrers — workflows depend on this file.
- **Current usage**: Referenced by multiple agents/hooks
- **Active referrers**: 92  **Blast radius**: HIGH

#### B-K9. `/home/prichwil/shared/context/body/nervous-system.md`  [175 lines, INFORMATION, HIGH confidence]
- **Rationale**: 55 active path referrers — workflows depend on this file.
- **Current usage**: Referenced by multiple agents/hooks
- **Active referrers**: 55  **Blast radius**: HIGH

#### B-K6. `/home/prichwil/shared/context/body/hands.md`  [148 lines, INFORMATION, HIGH confidence]
- **Rationale**: 69 active path referrers — workflows depend on this file.
- **Current usage**: Referenced by multiple agents/hooks
- **Active referrers**: 69  **Blast radius**: HIGH

#### B-K4. `/home/prichwil/shared/context/body/eyes.md`  [137 lines, INFORMATION, HIGH confidence]
- **Rationale**: 103 active path referrers — workflows depend on this file.
- **Current usage**: Referenced by multiple agents/hooks
- **Active referrers**: 103  **Blast radius**: HIGH


---

## Protocols layer (29 files, 6429 lines)

### DELETE — protocols layer (5 rows)

#### P-D4. `/home/prichwil/shared/context/protocols/state-file-au-ps.md`  [54 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 4 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW
- **Prior context**: [2026-04-12] Topic: WW Testing + AU state files created; .md cleanup from SharePoint | Actions: Broad search across local filesystem + SharePoint (Kiro-Drive, A

#### P-D2. `/home/prichwil/shared/context/protocols/duckdb-access-policy.md`  [52 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 1 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW
- **Prior context**: [2026-04-16] Topic: EOD phase-skipping structural fixes — all 3 implemented | Actions: (1) Hard gate added to eod-frontend.md: requires all 3 backend JSONs with

#### P-D1. `/home/prichwil/shared/context/protocols/am-backend.md`  [256 lines, DUPLICATE, MEDIUM confidence]
- **Rationale**: Duplicate of /home/prichwil/shared/context/protocols/am-auto.md (group ovl-2, shape=heading_overlap).
- **Active referrers**: 0
- **Documentation-only referrers**: 3 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW
- **Prior context**: [2026-04-06] Topic: AM hook architecture restructure — backend/frontend split | Actions: Created am-backend.md (6 phases: data collection, signal routing, enric

#### P-D3. `/home/prichwil/shared/context/protocols/eod-backend.md`  [220 lines, DUPLICATE, MEDIUM confidence]
- **Rationale**: Duplicate of /home/prichwil/shared/context/protocols/eod-frontend.md (group dup-1, shape=stem_variant).
- **Active referrers**: 1
- **Latent referrers**: 1
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: MEDIUM
- **Prior context**: [2026-04-06] Topic: EOD hook architecture restructure — backend/frontend split | Actions: Created eod-backend.md (7 phases: meeting ingestion, Asana reconciliat

#### P-D5. `/home/prichwil/shared/context/protocols/state-file-mx-ps.md`  [53 lines, DUPLICATE, MEDIUM confidence]
- **Rationale**: Duplicate of /home/prichwil/shared/context/protocols/state-file-au-ps.md (group ovl-3, shape=heading_overlap).
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW
- **Prior context**: [2026-04-12] Topic: MX state file gap audit against original prompt + remediation | Actions: Systematic audit of 20+ requirements from the original architectura


### KEEP — protocols layer (24 rows)

#### P-K2. `/home/prichwil/shared/context/protocols/am-backend-parallel.md`  [608 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 3 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/hooks/am-auto.kiro.hook, ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md
- **Active referrers**: 3  **Blast radius**: HIGH

#### P-K3. `/home/prichwil/shared/context/protocols/am-frontend.md`  [484 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 3 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/hooks/am-triage.kiro.hook, ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md
- **Active referrers**: 3  **Blast radius**: HIGH

#### P-K13. `/home/prichwil/shared/context/protocols/hard-thing-selection.md`  [404 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 11 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/.kiro/specs/system-subtraction-audit/design.md, ~/shared/context/active/karpathy-loop-run2.log
- **Active referrers**: 11  **Blast radius**: HIGH

#### P-K5. `/home/prichwil/shared/context/protocols/asana-duckdb-sync.md`  [403 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 5 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md, ~/shared/context/protocols/eod-backend.md
- **Active referrers**: 5  **Blast radius**: HIGH

#### P-K1. `/home/prichwil/shared/context/protocols/am-auto.md`  [400 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 2 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/.kiro/specs/admin-block-fix/design.md, ~/.kiro/specs/admin-block-fix/tasks.md
- **Active referrers**: 2  **Blast radius**: LOW

#### P-K12. `/home/prichwil/shared/context/protocols/eod-system-refresh.md`  [376 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 2 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md, ~/shared/context/tests/admin-block-preservation-test.sh
- **Active referrers**: 2  **Blast radius**: LOW

#### P-K4. `/home/prichwil/shared/context/protocols/am-triage.md`  [340 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 2 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/.kiro/specs/admin-block-fix/design.md, ~/.kiro/specs/admin-block-fix/tasks.md
- **Active referrers**: 2  **Blast radius**: LOW

#### P-K7. `/home/prichwil/shared/context/protocols/context-enrichment.md`  [313 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 4 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md, ~/shared/context/protocols/eod-backend.md
- **Active referrers**: 4  **Blast radius**: HIGH

#### P-K18. `/home/prichwil/shared/context/protocols/signal-intelligence.md`  [219 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 3 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md, ~/shared/context/protocols/am-backend.md
- **Active referrers**: 3  **Blast radius**: HIGH

#### P-K15. `/home/prichwil/shared/context/protocols/meeting-to-task-pipeline.md`  [211 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 3 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md, ~/shared/context/protocols/eod-backend.md
- **Active referrers**: 3  **Blast radius**: HIGH

#### P-K9. `/home/prichwil/shared/context/protocols/email-calendar-duckdb-sync.md`  [210 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 1 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md
- **Active referrers**: 1  **Blast radius**: LOW

#### P-K21. `/home/prichwil/shared/context/protocols/slack-history-backfill.md`  [210 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 1 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/intake/session-log.md
- **Active referrers**: 1  **Blast radius**: LOW

#### P-K22. `/home/prichwil/shared/context/protocols/state-file-engine.md`  [206 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 3 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/intake/session-log.md, ~/shared/context/protocols/am-backend-parallel.md
- **Active referrers**: 3  **Blast radius**: HIGH

#### P-K19. `/home/prichwil/shared/context/protocols/signal-to-task-pipeline.md`  [204 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 4 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md, ~/shared/context/protocols/am-backend.md
- **Active referrers**: 4  **Blast radius**: HIGH

#### P-K16. `/home/prichwil/shared/context/protocols/seasonality-calendar.md`  [186 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 4 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/agents/wbr-callouts/market-analyst.md, ~/.kiro/agents/wbr-callouts/callout-writer.md, ~/.kiro/skills/wbr-callouts/references/callout-principles.md
- **Active referrers**: 4  **Blast radius**: HIGH

#### P-K10. `/home/prichwil/shared/context/protocols/eod-frontend.md`  [168 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 3 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/hooks/eod.kiro.hook, ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md
- **Active referrers**: 3  **Blast radius**: HIGH

#### P-K17. `/home/prichwil/shared/context/protocols/sharepoint-durability-sync.md`  [167 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 6 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md, ~/shared/context/protocols/eod-frontend.md
- **Active referrers**: 6  **Blast radius**: HIGH

#### P-K23. `/home/prichwil/shared/context/protocols/state-file-ww-testing.md`  [166 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 1 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/.kiro/steering/ww-testing-loop-prep.md, ~/shared/context/intake/session-log.md
- **Active referrers**: 1  **Blast radius**: LOW

#### P-K20. `/home/prichwil/shared/context/protocols/slack-conversation-intelligence.md`  [129 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 3 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md, ~/shared/context/protocols/am-backend.md
- **Active referrers**: 3  **Blast radius**: HIGH

#### P-K24. `/home/prichwil/shared/context/protocols/workflow-observability.md`  [99 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 1 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md
- **Active referrers**: 1  **Blast radius**: LOW

#### P-K8. `/home/prichwil/shared/context/protocols/duckdb-schema-verification.md`  [84 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 3 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md, ~/shared/context/protocols/am-backend.md
- **Active referrers**: 3  **Blast radius**: HIGH

#### P-K6. `/home/prichwil/shared/context/protocols/communication-analytics.md`  [82 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 3 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md, ~/shared/context/protocols/eod-backend.md
- **Active referrers**: 3  **Blast radius**: HIGH

#### P-K11. `/home/prichwil/shared/context/protocols/eod-meeting-sync.md`  [66 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 1 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md
- **Active referrers**: 1  **Blast radius**: LOW

#### P-K14. `/home/prichwil/shared/context/protocols/loop-page-sync.md`  [59 lines, ACTIVE-PROTOCOL, HIGH confidence]
- **Rationale**: 2 active hook/agent references this protocol.
- **Current usage**: ~/.kiro/specs/system-subtraction-audit/inventory.json, ~/shared/context/active/hook-protocol-audit.md, ~/shared/context/protocols/am-backend-parallel.md
- **Active referrers**: 2  **Blast radius**: LOW


---

## Hooks layer (23 files, 280 lines)

### DELETE — hooks layer (12 rows)

#### H-D10. `/home/prichwil/.kiro/hooks/state-file-constraints-sync.kiro.hook`  [16 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 1 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW
- **Prior context**: [2026-04-20] Topic: Phase 2 downstream wiring shipped — callouts, forecast xlsx, state files all consuming ps.market_constraints | Actions: (1) Added "Market co

#### H-D12. `/home/prichwil/.kiro/hooks/wbr-pipeline-trigger.kiro.hook`  [15 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 2 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW
- **Prior context**: [2026-04-13] Topic: Prediction ledger integration into WBR pipeline hooks | Actions: Updated wbr-pipeline-trigger.kiro.hook (v1→v2) with Step 7 to auto-append p

#### H-D5. `/home/prichwil/.kiro/hooks/market-constraints-staleness-alert.kiro.hook`  [13 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 0 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW

#### H-D11. `/home/prichwil/.kiro/hooks/steering-integrity-check.kiro.hook`  [13 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 2 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW
- **Prior context**: [2026-04-05] Topic: Steering file cleanup and duplication prevention | Actions: Deleted 4 redundant files (agentspaces-core, devspaces-core, product, file-creat

#### H-D3. `/home/prichwil/.kiro/hooks/guard-calendar.kiro.hook`  [12 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 3 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW

#### H-D4. `/home/prichwil/.kiro/hooks/guard-email.kiro.hook`  [12 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 3 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW

#### H-D1. `/home/prichwil/.kiro/hooks/dashboard-server.kiro.hook`  [11 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 2 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW
- **Prior context**: [2026-04-15] Topic: Dashboard server auto-restart hook | Actions: Confirmed .bashrc already has auto-start for port 8080 (added previously), but it doesn't help

#### H-D7. `/home/prichwil/.kiro/hooks/ps-audit.kiro.hook`  [9 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 3 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW

#### H-D9. `/home/prichwil/.kiro/hooks/sharepoint-sync.kiro.hook`  [9 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 6 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW
- **Prior context**: [2026-04-07] Topic: MCP reinstall + hook dependency check | Actions: Audited all MCP-related directories (toolbox, aim, mcp-registry). Installed 3 of 4 missing 

#### H-D2. `/home/prichwil/.kiro/hooks/guard-asana.kiro.hook`  [12 lines, ORPHAN, MEDIUM confidence]
- **Rationale**: Zero active referrers; 0 latent, 4 documentation, 1 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 4 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW

#### H-D6. `/home/prichwil/.kiro/hooks/organ-change-detector.kiro.hook`  [12 lines, ORPHAN, MEDIUM confidence]
- **Rationale**: Zero active referrers; 0 latent, 3 documentation, 2 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 3 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW

#### H-D8. `/home/prichwil/.kiro/hooks/session-summary.kiro.hook`  [11 lines, ORPHAN, MEDIUM confidence]
- **Rationale**: Zero active referrers; 0 latent, 3 documentation, 4 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 3 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW


### KEEP — hooks layer (11 rows)

#### H-K8. `/home/prichwil/.kiro/hooks/harmony-forecast-deploy.kiro.hook`  [17 lines, ACTIVE-HOOK, HIGH confidence]
- **Rationale**: Enabled hook, actively firing.
- **Active referrers**: 2  **Blast radius**: LOW

#### H-K2. `/home/prichwil/.kiro/hooks/am-auto.kiro.hook`  [15 lines, INTENTIONALLY-DISABLED, HIGH confidence]
- **Rationale**: Disabled with dated rationale in description.
- **Active referrers**: 12  **Blast radius**: LOW

#### H-K7. `/home/prichwil/.kiro/hooks/forecast-sharepoint-push.kiro.hook`  [15 lines, ACTIVE-HOOK, HIGH confidence]
- **Rationale**: Enabled hook, actively firing.
- **Active referrers**: 1  **Blast radius**: LOW

#### H-K4. `/home/prichwil/.kiro/hooks/audit-asana-writes.kiro.hook`  [14 lines, ACTIVE-HOOK, HIGH confidence]
- **Rationale**: Enabled hook, actively firing.
- **Active referrers**: 56  **Blast radius**: LOW

#### H-K9. `/home/prichwil/.kiro/hooks/open-items-reminder.kiro.hook`  [13 lines, ACTIVE-HOOK, HIGH confidence]
- **Rationale**: Enabled hook, actively firing.
- **Active referrers**: 1  **Blast radius**: LOW

#### H-K3. `/home/prichwil/.kiro/hooks/am-triage.kiro.hook`  [11 lines, ACTIVE-HOOK, HIGH confidence]
- **Rationale**: Enabled hook, actively firing.
- **Active referrers**: 51  **Blast radius**: LOW

#### H-K5. `/home/prichwil/.kiro/hooks/context-preloader.kiro.hook`  [11 lines, ACTIVE-HOOK, HIGH confidence]
- **Rationale**: Enabled hook, actively firing.
- **Active referrers**: 1  **Blast radius**: LOW

#### H-K6. `/home/prichwil/.kiro/hooks/eod.kiro.hook`  [11 lines, ACTIVE-HOOK, HIGH confidence]
- **Rationale**: Enabled hook, actively firing.
- **Active referrers**: 59  **Blast radius**: LOW

#### H-K11. `/home/prichwil/.kiro/hooks/wiki-maintenance.kiro.hook`  [10 lines, ACTIVE-HOOK, HIGH confidence]
- **Rationale**: Enabled hook, actively firing.
- **Active referrers**: 4  **Blast radius**: LOW

#### H-K1. `/home/prichwil/.kiro/hooks/agent-bridge-sync.kiro.hook`  [9 lines, ACTIVE-HOOK, HIGH confidence]
- **Rationale**: Enabled hook, actively firing.
- **Active referrers**: 1  **Blast radius**: LOW

#### H-K10. `/home/prichwil/.kiro/hooks/wbr-callouts.kiro.hook`  [9 lines, ACTIVE-HOOK, HIGH confidence]
- **Rationale**: Enabled hook, actively firing.
- **Active referrers**: 4  **Blast radius**: LOW


---

## Steering layer (32 files, 3432 lines)

### DELETE — steering layer (6 rows)

#### S-D4. `/home/prichwil/.kiro/steering/context/kiro-limitations.md`  [43 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 2 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW

#### S-D6. `/home/prichwil/.kiro/steering/context/steering-integrity.md`  [43 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 3 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW
- **Prior context**: [2026-04-05] Topic: Steering file cleanup and duplication prevention | Actions: Deleted 4 redundant files (agentspaces-core, devspaces-core, product, file-creat

#### S-D5. `/home/prichwil/.kiro/steering/context/powers-evaluation.md`  [29 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 1 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW

#### S-D3. `/home/prichwil/.kiro/steering/context/context-provider-recommendations.md`  [25 lines, ORPHAN, HIGH confidence]
- **Rationale**: Zero active referrers; 0 latent, 2 documentation, 1 name-only.
- **Active referrers**: 0
- **Documentation-only referrers**: 2 (do not save from ORPHAN per R2.4)
- **Blast radius**: LOW

#### S-D2. `/home/prichwil/.kiro/steering/influences.md`  [11 lines, EMPTY-SHELL, HIGH confidence]
- **Rationale**: Empty shell — 6 content lines, no substance to preserve.
- **Active referrers**: 2
- **Documentation-only referrers**: 3 (do not save from ORPHAN per R2.4)
- **Blast radius**: MEDIUM

#### S-D1. `/home/prichwil/.kiro/steering/agentspaces-core.md`  [31 lines, DUPLICATE, MEDIUM confidence]
- **Rationale**: Duplicate of /home/prichwil/.kiro/steering/environment-rules.md (group ovl-4, shape=heading_overlap).
- **Active referrers**: 2
- **Documentation-only referrers**: 4 (do not save from ORPHAN per R2.4)
- **Blast radius**: MEDIUM
- **Prior context**: [2026-04-05] Topic: Asana schema drift handling | Actions: Added tasks 0.10 (schema drift handling) and 0.11 (schema_changes DuckDB table) to MCP spec. Covers: 


### KEEP — steering layer (26 rows)

#### S-K20. `/home/prichwil/.kiro/steering/slack-deep-context.md`  [1142 lines, CONDITIONAL-STEERING-USED, MEDIUM confidence]
- **Rationale**: Conditional steering, 5 active + 0 latent referrers.
- **Active referrers**: 5  **Blast radius**: LOW

#### S-K19. `/home/prichwil/.kiro/steering/rw-task-prioritization.md`  [269 lines, CONDITIONAL-STEERING-USED, MEDIUM confidence]
- **Rationale**: Conditional steering, 4 active + 0 latent referrers.
- **Active referrers**: 4  **Blast radius**: LOW

#### S-K10. `/home/prichwil/.kiro/steering/market-constraints.md`  [268 lines, AUTO-STEERING, MEDIUM confidence]
- **Rationale**: Auto-loaded steering; 10 path refs from elsewhere.
- **Current usage**: Loaded on every chat
- **Active referrers**: 10  **Blast radius**: HIGH

#### S-K3. `/home/prichwil/.kiro/steering/asana-guardrails.md`  [149 lines, CONDITIONAL-STEERING-USED, MEDIUM confidence]
- **Rationale**: Conditional steering, 2 active + 0 latent referrers.
- **Active referrers**: 2  **Blast radius**: LOW

#### S-K23. `/home/prichwil/.kiro/steering/soul.md`  [143 lines, AUTO-STEERING, MEDIUM confidence]
- **Rationale**: Auto-loaded steering; 125 path refs from elsewhere.
- **Current usage**: Loaded on every chat
- **Active referrers**: 125  **Blast radius**: HIGH

#### S-K16. `/home/prichwil/.kiro/steering/richard-style-slack.md`  [126 lines, CONDITIONAL-STEERING-USED, MEDIUM confidence]
- **Rationale**: Conditional steering, 44 active + 0 latent referrers.
- **Active referrers**: 44  **Blast radius**: LOW

#### S-K5. `/home/prichwil/.kiro/steering/document-registry.md`  [95 lines, AUTO-STEERING, MEDIUM confidence]
- **Rationale**: Auto-loaded steering; 4 path refs from elsewhere.
- **Current usage**: Loaded on every chat
- **Active referrers**: 4  **Blast radius**: HIGH

#### S-K9. `/home/prichwil/.kiro/steering/mario-peter-dichotomy.md`  [88 lines, CONDITIONAL-STEERING-USED, MEDIUM confidence]
- **Rationale**: Conditional steering, 1 active + 0 latent referrers.
- **Active referrers**: 1  **Blast radius**: LOW

#### S-K17. `/home/prichwil/.kiro/steering/richard-style-wbr.md`  [88 lines, CONDITIONAL-STEERING-USED, MEDIUM confidence]
- **Rationale**: Conditional steering, 71 active + 0 latent referrers.
- **Active referrers**: 71  **Blast radius**: LOW

#### S-K14. `/home/prichwil/.kiro/steering/richard-style-email.md`  [76 lines, CONDITIONAL-STEERING-USED, MEDIUM confidence]
- **Rationale**: Conditional steering, 67 active + 0 latent referrers.
- **Active referrers**: 67  **Blast radius**: LOW

#### S-K13. `/home/prichwil/.kiro/steering/richard-style-docs.md`  [74 lines, CONDITIONAL-STEERING-USED, MEDIUM confidence]
- **Rationale**: Conditional steering, 24 active + 0 latent referrers.
- **Active referrers**: 24  **Blast radius**: LOW

#### S-K26. `/home/prichwil/.kiro/steering/context/pilot-steering.md`  [72 lines, AUTO-STEERING, MEDIUM confidence]
- **Rationale**: Auto-loaded steering; 0 path refs from elsewhere.
- **Current usage**: Loaded on every chat
- **Active referrers**: 0  **Blast radius**: HIGH

#### S-K6. `/home/prichwil/.kiro/steering/duckdb-schema.md`  [66 lines, AUTO-STEERING, MEDIUM confidence]
- **Rationale**: Auto-loaded steering; 3 path refs from elsewhere.
- **Current usage**: Loaded on every chat
- **Active referrers**: 3  **Blast radius**: HIGH

#### S-K12. `/home/prichwil/.kiro/steering/richard-style-amazon.md`  [65 lines, CONDITIONAL-STEERING-USED, MEDIUM confidence]
- **Rationale**: Conditional steering, 63 active + 0 latent referrers.
- **Active referrers**: 63  **Blast radius**: LOW

#### S-K18. `/home/prichwil/.kiro/steering/richard-writing-style.md`  [65 lines, AUTO-STEERING, MEDIUM confidence]
- **Rationale**: Auto-loaded steering; 17 path refs from elsewhere.
- **Current usage**: Loaded on every chat
- **Active referrers**: 17  **Blast radius**: HIGH

#### S-K21. `/home/prichwil/.kiro/steering/slack-guardrails.md`  [61 lines, AUTO-STEERING, MEDIUM confidence]
- **Rationale**: Auto-loaded steering; 3 path refs from elsewhere.
- **Current usage**: Loaded on every chat
- **Active referrers**: 3  **Blast radius**: HIGH

#### S-K15. `/home/prichwil/.kiro/steering/richard-style-mbr.md`  [60 lines, CONDITIONAL-STEERING-USED, MEDIUM confidence]
- **Rationale**: Conditional steering, 46 active + 0 latent referrers.
- **Active referrers**: 46  **Blast radius**: LOW

#### S-K25. `/home/prichwil/.kiro/steering/ww-testing-loop-prep.md`  [60 lines, CONDITIONAL-STEERING-USED, MEDIUM confidence]
- **Rationale**: Conditional steering, 2 active + 0 latent referrers.
- **Active referrers**: 2  **Blast radius**: LOW

#### S-K22. `/home/prichwil/.kiro/steering/slack-knowledge-search.md`  [51 lines, CONDITIONAL-STEERING-USED, MEDIUM confidence]
- **Rationale**: Conditional steering, 2 active + 0 latent referrers.
- **Active referrers**: 2  **Blast radius**: LOW

#### S-K24. `/home/prichwil/.kiro/steering/tech.md`  [49 lines, AUTO-STEERING, MEDIUM confidence]
- **Rationale**: Auto-loaded steering; 3 path refs from elsewhere.
- **Current usage**: Loaded on every chat
- **Active referrers**: 3  **Blast radius**: HIGH

#### S-K2. `/home/prichwil/.kiro/steering/architecture-eval-protocol.md`  [45 lines, CONDITIONAL-STEERING-USED, MEDIUM confidence]
- **Rationale**: Conditional steering, 2 active + 0 latent referrers.
- **Active referrers**: 2  **Blast radius**: LOW

#### S-K7. `/home/prichwil/.kiro/steering/environment-rules.md`  [40 lines, AUTO-STEERING, MEDIUM confidence]
- **Rationale**: Auto-loaded steering; 5 path refs from elsewhere.
- **Current usage**: Loaded on every chat
- **Active referrers**: 5  **Blast radius**: HIGH

#### S-K4. `/home/prichwil/.kiro/steering/devspaces-core.md`  [33 lines, AUTO-STEERING, MEDIUM confidence]
- **Rationale**: Auto-loaded steering; 2 path refs from elsewhere.
- **Current usage**: Loaded on every chat
- **Active referrers**: 2  **Blast radius**: HIGH

#### S-K11. `/home/prichwil/.kiro/steering/process-execution.md`  [26 lines, AUTO-STEERING, MEDIUM confidence]
- **Rationale**: Auto-loaded steering; 2 path refs from elsewhere.
- **Current usage**: Loaded on every chat
- **Active referrers**: 2  **Blast radius**: HIGH

#### S-K1. `/home/prichwil/.kiro/steering/amazon-builder-production-safety.md`  [23 lines, AUTO-STEERING, MEDIUM confidence]
- **Rationale**: Auto-loaded steering; 2 path refs from elsewhere.
- **Current usage**: Loaded on every chat
- **Active referrers**: 2  **Blast radius**: HIGH

#### S-K8. `/home/prichwil/.kiro/steering/file-creation-rules.md`  [16 lines, AUTO-STEERING, MEDIUM confidence]
- **Rationale**: Auto-loaded steering; 2 path refs from elsewhere.
- **Current usage**: Loaded on every chat
- **Active referrers**: 2  **Blast radius**: HIGH


---

## Duplication groups

| ID | Shape | Members | Total lines | Survivor | Loser lines |
|----|-------|---------|-------------|----------|-------------|
| dup-1 | stem_variant | eod-backend.md, eod-frontend.md | 388 | eod-frontend.md | 220 |
| ovl-2 | heading_overlap | am-auto.md, am-backend.md | 656 | am-auto.md | 256 |
| ovl-3 | heading_overlap | state-file-au-ps.md, state-file-mx-ps.md | 107 | state-file-au-ps.md | 53 |
| ovl-4 | heading_overlap | agentspaces-core.md, environment-rules.md | 71 | environment-rules.md | 31 |
