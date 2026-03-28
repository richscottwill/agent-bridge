# OCI Performance by Market

Last updated: 2026-03-12
Sources: 2026 MBR/QBR Quip, Global Acq WBR Callouts (W1-W10 2026), OCI Paid Search Instructions Quip

## Summary
OCI (Offline Conversion Import) enables Google Ads to optimize bidding based on actual registration value data sent back from Amazon's systems, replacing Adobe's algorithmic bidding. AB Paid Search was the first non-retail BU to implement OCI at Amazon.

## Rollout Timeline
| Market | Status | Launch Date | Full Impact |
|--------|--------|-------------|-------------|
| US | Live | Jul 2025 (Phase 1) → Sep 2025 (100% NB) | Oct 2025 |
| UK | Live | Aug 2025 (Test) → Sep 2025 (100%) | Oct 2025 |
| DE | Live | Nov 2025 (Test) → Dec 2025 (100%) | Jan 2026 |
| CA | In Progress | Mar 2026 (E2E testing launched 3/4) | Jul 2026 (projected) |
| JP | In Progress | Feb 2026 (E2E testing launched 2/26) | Jul 2026 (projected) |
| FR | In Progress | Feb 2026 (E2E testing launched 2/26) | Jul 2026 (projected) |
| IT | In Progress | Feb 2026 (E2E testing launched 2/26) | Jul 2026 (projected) |
| ES | In Progress | Feb 2026 (E2E testing launched 2/26) | Jul 2026 (projected) |
| AU | Not planned | N/A — not in OCI scope | N/A |
| MX | Not planned | N/A — not in OCI scope | N/A |

## Performance Lift (Rolled-Out Markets)

### US
- Testing period: Jul 1 - Oct 31, 2025 (4 months)
- Lift: +19.1K registrations as of 10/31, +24% reg lift
- Nov 2025: 7,853 additional regs
- Non-Brand CPA improvement: ~50% during test vs control
- Total estimated impact (actual + Nov): 32,047 regs × $520 CCP = **$16.7MM OPS**
- Jan 2026: 39K regs (+30% vs OP2, +86% YoY), driven by OCI-enhanced NB
- Feb 2026: 32.9K regs (+16% vs OP2, +68% YoY)
- Confidence: HIGH (multiple MBR sources confirm)

### UK
- Testing period: Aug 4 - Oct 31, 2025
- Lift: +2.4K registrations as of 10/31, +23% reg lift
- Nov 2025: 1,945 additional regs
- Jan 2026: surpassed OP2 by 41%, driven by OCI + 30% YoY Brand traffic
- Feb 2026: surpassed OP2 by 24% despite -6% spend vs OP2
- Confidence: HIGH

### DE
- Testing period: Oct 1 - Dec 8, 2025 (2.5 months)
- Lift: +749 registrations as of 12/4, +18% lift
- Dec 2025 OCI lift tracking: W49 +20% (95% to expectation), W50 +20% (96%), W51 +16% (74%)
- Jan 2026: surpassed OP2 by 10%
- Feb 2026: missed OP2 by 4% (NB performance -22% vs OP2, higher baseline from strong Y25)
- Confidence: HIGH

## OCI Test vs Control Data (DE, from WBR)

### Week 44 (10/26-11/1) — Early DE testing
| Segment | Cost | Regs | ROAS | CPA |
|---------|------|------|------|-----|
| NB Control | $44,592 | 36 | 3% | $1,239 |
| NB Test | $64,565 | 200 | 13% | $323 |
| NB Diff | +45% | +456% | +333% | -74% |

### Week 45 (11/2-11/8) — Full M4 DE
| Segment | Cost | Regs | ROAS | CPA |
|---------|------|------|------|-----|
| NB Control | $56,790 | 55 | 3% | $1,033 |
| NB Test | $66,182 | 253 | 13% | $262 |
| NB Diff | +17% | +360% | +333% | -75% |

## MCC Structure
- Master MCC: DSAP - Amazon Business Parent MCC (873-788-1095)
- NA MCC: 683-476-0964 (US, CA, MX)
- EU MCC: 549-849-5609 (UK, DE, FR, IT, ES)
- JP MCC: 852-899-4580
- AU: Not created

## Known Issues
- Duplicate hvocijid parameters appearing in landing page URLs across EU3 and existing markets (US, UK, DE). Causing "Duplicate query param found" errors in event processing. JP not affected. Under investigation.

## Gaps Identified → Feed to Experiment 2
- Need competitor response data: did Walmart/others change bidding behavior after our OCI improvements?
- Need AU/MX rationale for exclusion from OCI scope
