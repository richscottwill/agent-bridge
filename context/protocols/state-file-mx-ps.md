# MX Paid Search State File — Agent Protocol

## Purpose
Market-specific parameters for the MX Paid Search daily state file. Loaded by the State File Engine (`state-file-engine.md`) during AM-Backend Step 2E and EOD Step 9. This file defines WHAT to analyze; the engine defines HOW to generate and deliver.

## Activation
This protocol is loaded by the state file engine when processing market='MX'. It is NOT invoked directly by hooks.

## MX-Specific Analytical Parameters

### ie%CCP Constraint Model
- Formula: ie%CCP = (Brand_Spend + NB_Spend) / (Brand_Regs × Brand_CCP + NB_Regs × NB_CCP)
- CCP values: Brand = $90, NB = $30 (verify from dashboard — values change)
- Target: ≥100% from Q2 2026 onward
- At 100% ie%CCP: NB_Regs ≤ Brand_Regs × 0.663 (at NB CPA $134)
- At 75% ie%CCP: NB_Regs ≤ Brand_Regs × 0.503 (at NB CPA $115)

### Key Thresholds
- NB CPC anomaly trigger: >$2.00 or >15% above 8-week average
- NB CVR baseline (post-negative-keyword restructuring): 1.3–1.5%
- NB CVR pre-restructuring baseline: 1.1–1.3%
- Brand CPA stability band: $19–$23
- Monthly projection method: weekday/weekend weighted daily rates, not simple linear

### Data Sources
- Primary: DuckDB `weekly_metrics` WHERE market='MX'
- Daily: DuckDB `daily_metrics` WHERE market='MX'
- Change log: DuckDB `change_log` WHERE market='MX'
- Projections: `~/shared/wiki/callouts/mx/mx-projections.md`
- FY26 model: `~/shared/wiki/callouts/mx/mx-fy26-projection.md`
- Stakeholder context: `~/shared/wiki/meetings/mx-paid-search-sync.md`
- Quip tracker: https://quip-amazon.com/K9OYA9mXm7DU

### Stakeholder Context

- Primary: Lorena Alvarez Larrea (L5) — new relationship since 3/17, be thorough
- Support: Yun-Kang Chu (L6) — Adobe/Modern Search
- Manager: Brandon Munday (L7) — approves budget changes
- Previous: Carlos Palmos — transitioned to CPS 3/17, no longer PS stakeholder

## Output Schema
The agent must produce a JSON object matching the placeholder taxonomy in Appendix H of the state file. All keys are required. Static sections (Goals, Tenets) are not in the JSON — they persist in the template.

## Quality Gates
Before uploading to SharePoint:
1. Schema validation — all required JSON keys present
2. Math verification — CPA, ie%CCP match deterministic recalculation
3. Weasel word scan — zero violations
4. Style replication — static sections unchanged
5. Content replication — historical data matches DuckDB

## SharePoint Upload Protocol
Handled by the State File Engine (Layer 3). See `state-file-engine.md` → Layer 3: SharePoint Durability Sync.
The engine uploads both .md and .docx to `Kiro-Drive/state-files/` during AM Phase 5.5 and EOD Phase 5.
