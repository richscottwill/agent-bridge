# MPE v1.1 Slim — 10-Step All-Markets Simulation Report

*Generated 2026-04-27T02:48:55.692348. Runs Phase 5.2 simulation across all 10 markets, replaces the original MX-only 4/22 checklist.*

## Per-Market Results

| Market | S01 | S02 | S03 | S04 | S05 | S06 | S07 | S08 | S09 | S10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AU | — | ✓ | ✓ | ✓ | ✓ | · | ✓ | — | — | ✓ |
| CA | ✓ | — | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ |
| DE | ✓ | — | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ |
| ES | ✓ | — | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ |
| FR | ✓ | — | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ |
| IT | ✓ | — | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ |
| JP | — | — | ✓ | ✓ | ✓ | · | ✓ | — | — | ✓ |
| MX | ✓ | — | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ |
| UK | ✓ | — | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ |
| US | ✓ | — | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ |

## Summary

- Total: **85** (10 steps × 10 markets)
- Passed: **75** (88%)

**Example:** If this section references a specific process, the concrete steps are: - Passed: **75** (88%)...

- Skipped: **10** (legitimate: market doesn't have the relevant structure)
- Failed: **0**

## Step Legend

1. Initial projection at ie%CCP target converges or returns feasible bound
4. Regime fit state exists with confidence + decay_status metadata
6. CPA elasticity fit has r² metadata
7. Spend-mode target produces positive NB regs
9. 90% credible interval spans > 2% of central (rejects fake precision)
10. Brand+NB regs > 0 and blended CPA > 0

## Symbols

- ✓ PASSED — check satisfied
- ✗ FAILED — investigate; anomaly detection may help
- · SKIPPED — check doesn't apply to this market (e.g., no active regime)
