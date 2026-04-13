# WW Testing State File — Agent Protocol

## Purpose
Program-specific parameters for the WW Paid Search Testing daily state file. Loaded by the State File Engine (`state-file-engine.md`) during AM-Backend Step 2E and EOD Step 9. This file defines WHAT to analyze; the engine defines HOW to generate and deliver.

## Activation
This protocol is loaded by the state file engine when processing market='WW Testing'. It is NOT invoked directly by hooks.

## WW Testing-Specific Analytical Parameters

### Five Workstreams
1. OCI Bidding — phased rollout across 10 markets. Measurement: seasonality-adjusted CPA baselines.
2. Modern Search (Ad Copy) — evidence-based messaging from SP study. Measurement: test/control splits.
3. Audiences & Lifecycle — Engagement channel + F90 Lifecycle. Measurement: iOPS, ROAS.
4. User Experience — Polaris Brand LP, Baloo, in-context registration. Measurement: Weblab APT, pre/post.
5. Algorithmic Ads — DG CPC, AI Max. Measurement: CPC benchmarks, incrementality.

### Key Thresholds
- OCI uplift expectation: 18–24% reg uplift (validated in US/UK/DE)
- Ad Copy confidence: HIGH requires 30+ days and meaningful volume (>500 conversions)
- Test status coverage target: 100% of active tests with written status
- Methodology: hypothesis → phased rollout → measurement → scale or stop

### OCI Status Tracking
| Market | Status | Notes |
|---|---|---|
| US | 100% | Baseline. +24% uplift, $16.7MM OPS |
| UK | 100% | +23% uplift |
| DE | 100% | +18% uplift |
| FR | 100% | Live, measuring |
| IT | 100% | Live, measuring |
| ES | 100% | Live, measuring |
| JP | 100% | Live, measuring |
| CA | On track | Apr 7 launch |
| AU | Planned | May 2026, no MCC |
| MX | TBD | No MCC |

### Data Sources
- Primary: DuckDB `weekly_metrics` (all markets) for WW aggregate
- Test status: `~/shared/wiki/agent-created/testing/` (all workstream docs)
- OCI status: `~/shared/context/body/eyes.md` → OCI Performance section
- Testing Approach: `~/shared/wiki/agent-created/testing/testing-approach-kate-v5.md`
- Methodology: `~/shared/wiki/agent-created/testing/testing-methodology.md`
- WW callouts: `~/shared/wiki/callouts/ww/`
- Quip OCI Planning: https://quip-amazon.com/dSZ9AAZBXQy
- Quip Ad Copy: https://quip-amazon.com/KCY9AAYqWd2
- Quip Baloo: https://quip-amazon.com/TVY9AAomVYU
- Quip LP Testing: https://quip-amazon.com/BLP9AAhFfua

### Stakeholder Context
- Primary audience: Kate Rundell (L8 Director) — Testing Approach doc is for her
- Manager: Brandon Munday (L7) — must review Testing Approach before Kate sees it
- Team: 7-person team managing 10 markets and 12+ cross-functional partnerships
- Key partners: Google, Adobe, MCS, MarTech, Legal, Data Science, ABMA

## Output Schema
The agent must produce a JSON object matching the placeholder taxonomy defined in the state file. Workstream-level metrics replace market-level metrics. Test status tables replace weekly trend tables.

## Quality Gates
Before uploading to SharePoint:
1. Schema validation — all required JSON keys present
2. Test status accuracy — every test listed must have a verifiable source doc
3. Weasel word scan — zero violations
4. Style replication — static sections unchanged
5. OCI status matches eyes.md source of truth

## SharePoint Upload Protocol
Handled by the State File Engine (Layer 3). See `state-file-engine.md` → Layer 3: SharePoint Durability Sync.
