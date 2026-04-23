# MPE Data Audit — All Markets

**Run at**: 2026-04-22 22:28 PT
**Purpose**: Tell the owner which markets can support a full market-specific fit in MPE v1 and which must use regional fallback. Run by `data_audit.py` before any fit. This is the Phase 0 gate.

## Summary

| Market | Clean Weeks | Spend Variance (B/NB) | Recommendation | Fallback Region |
|--------|-------------|------------------------|----------------|-----------------|
| US | 148 | 0.44 / 0.42 | MARKET-SPECIFIC FIT | NA |
| CA | 168 | 0.33 / 0.52 | MARKET-SPECIFIC FIT | NA |
| UK | 160 | 0.41 / 0.56 | MARKET-SPECIFIC FIT | EU5 |
| DE | 168 | 0.59 / 0.26 | MARKET-SPECIFIC FIT | EU5 |
| FR | 164 | 0.36 / 0.38 | MARKET-SPECIFIC FIT | EU5 |
| IT | 164 | 0.56 / 0.41 | MARKET-SPECIFIC FIT | EU5 |
| ES | 168 | 0.34 / 0.36 | MARKET-SPECIFIC FIT | EU5 |
| JP | 164 | 0.33 / 2.05 | MARKET-SPECIFIC FIT | WW |
| MX | 102 | 0.69 / 0.43 | MARKET-SPECIFIC FIT | WW |
| AU | 29 | 0.29 / 0.36 | regional fallback | WW |

## v1 Spec Alignment Check

The spec designates MX, US, and AU as Fully_Fit_Markets. Compare with audit recommendations:

- MX: ALIGNED — market-specific fit recommended
- US: ALIGNED — market-specific fit recommended
- AU: MISMATCH — spec says Fully_Fit but audit recommends `regional_fallback`. Spec needs updating OR wait for more data.

**Action**: 1 market(s) need spec adjustment or data accumulation before fitting. Update `.kiro/specs/market-projection-engine/requirements.md` and rerun Phase 1.

## Per-Market Detail

### US

- **Recommendation**: `market_specific`
- **Clean weeks**: 148 of 172 total (data range 2023-01-01 to 2026-04-12)
- **Brand spend variance (CV)**: 0.44 (need >= 0.2 for elasticity)
- **NB spend variance (CV)**: 0.42
- **Weeks with no ie%CCP**: 100%
- **Regime changes documented**: 6
- **Fallback region if used**: NA

**Explanation**: US has 148 clean weeks and sufficient spend variance (Brand CV=0.44, NB CV=0.42). Recommend a full market-specific fit.

**Warnings**:
- 6 regime change(s) documented in ps.regime_changes; ~24 weeks excluded from elasticity signal.
- 24 week(s) dropped from clean set due to nulls or zero spend.

### CA

- **Recommendation**: `market_specific`
- **Clean weeks**: 168 of 172 total (data range 2023-01-01 to 2026-04-12)
- **Brand spend variance (CV)**: 0.33 (need >= 0.2 for elasticity)
- **NB spend variance (CV)**: 0.52
- **Weeks with no ie%CCP**: 100%
- **Regime changes documented**: 1
- **Fallback region if used**: NA

**Explanation**: CA has 168 clean weeks and sufficient spend variance (Brand CV=0.33, NB CV=0.52). Recommend a full market-specific fit.

**Warnings**:
- 1 regime change(s) documented in ps.regime_changes; ~4 weeks excluded from elasticity signal.

### UK

- **Recommendation**: `market_specific`
- **Clean weeks**: 160 of 172 total (data range 2023-01-01 to 2026-04-12)
- **Brand spend variance (CV)**: 0.41 (need >= 0.2 for elasticity)
- **NB spend variance (CV)**: 0.56
- **Weeks with no ie%CCP**: 100%
- **Regime changes documented**: 3
- **Fallback region if used**: EU5

**Explanation**: UK has 160 clean weeks and sufficient spend variance (Brand CV=0.41, NB CV=0.56). Recommend a full market-specific fit.

**Warnings**:
- 3 regime change(s) documented in ps.regime_changes; ~12 weeks excluded from elasticity signal.
- 12 week(s) dropped from clean set due to nulls or zero spend.

### DE

- **Recommendation**: `market_specific`
- **Clean weeks**: 168 of 172 total (data range 2023-01-01 to 2026-04-12)
- **Brand spend variance (CV)**: 0.59 (need >= 0.2 for elasticity)
- **NB spend variance (CV)**: 0.26
- **Weeks with no ie%CCP**: 100%
- **Regime changes documented**: 1
- **Fallback region if used**: EU5

**Explanation**: DE has 168 clean weeks and sufficient spend variance (Brand CV=0.59, NB CV=0.26). Recommend a full market-specific fit.

**Warnings**:
- 1 regime change(s) documented in ps.regime_changes; ~4 weeks excluded from elasticity signal.

### FR

- **Recommendation**: `market_specific`
- **Clean weeks**: 164 of 172 total (data range 2023-01-01 to 2026-04-12)
- **Brand spend variance (CV)**: 0.36 (need >= 0.2 for elasticity)
- **NB spend variance (CV)**: 0.38
- **Weeks with no ie%CCP**: 100%
- **Regime changes documented**: 2
- **Fallback region if used**: EU5

**Explanation**: FR has 164 clean weeks and sufficient spend variance (Brand CV=0.36, NB CV=0.38). Recommend a full market-specific fit.

**Warnings**:
- 2 regime change(s) documented in ps.regime_changes; ~8 weeks excluded from elasticity signal.
- 8 week(s) dropped from clean set due to nulls or zero spend.

### IT

- **Recommendation**: `market_specific`
- **Clean weeks**: 164 of 172 total (data range 2023-01-01 to 2026-04-12)
- **Brand spend variance (CV)**: 0.56 (need >= 0.2 for elasticity)
- **NB spend variance (CV)**: 0.41
- **Weeks with no ie%CCP**: 100%
- **Regime changes documented**: 2
- **Fallback region if used**: EU5

**Explanation**: IT has 164 clean weeks and sufficient spend variance (Brand CV=0.56, NB CV=0.41). Recommend a full market-specific fit.

**Warnings**:
- 2 regime change(s) documented in ps.regime_changes; ~8 weeks excluded from elasticity signal.
- 8 week(s) dropped from clean set due to nulls or zero spend.

### ES

- **Recommendation**: `market_specific`
- **Clean weeks**: 168 of 172 total (data range 2023-01-01 to 2026-04-12)
- **Brand spend variance (CV)**: 0.34 (need >= 0.2 for elasticity)
- **NB spend variance (CV)**: 0.36
- **Weeks with no ie%CCP**: 100%
- **Regime changes documented**: 1
- **Fallback region if used**: EU5

**Explanation**: ES has 168 clean weeks and sufficient spend variance (Brand CV=0.34, NB CV=0.36). Recommend a full market-specific fit.

**Warnings**:
- 1 regime change(s) documented in ps.regime_changes; ~4 weeks excluded from elasticity signal.

### JP

- **Recommendation**: `market_specific`
- **Clean weeks**: 164 of 172 total (data range 2023-01-01 to 2026-04-12)
- **Brand spend variance (CV)**: 0.33 (need >= 0.2 for elasticity)
- **NB spend variance (CV)**: 2.05
- **Weeks with no ie%CCP**: 100%
- **Regime changes documented**: 2
- **Fallback region if used**: WW

**Explanation**: JP has 164 clean weeks and sufficient spend variance (Brand CV=0.33, NB CV=2.05). Recommend a full market-specific fit.

**Warnings**:
- 2 regime change(s) documented in ps.regime_changes; ~8 weeks excluded from elasticity signal.
- 8 week(s) dropped from clean set due to nulls or zero spend.

### MX

- **Recommendation**: `market_specific`
- **Clean weeks**: 102 of 110 total (data range 2024-03-13 to 2026-04-12)
- **Brand spend variance (CV)**: 0.69 (need >= 0.2 for elasticity)
- **NB spend variance (CV)**: 0.43
- **Weeks with no ie%CCP**: 100%
- **Regime changes documented**: 2
- **Fallback region if used**: WW

**Explanation**: MX has 102 clean weeks and sufficient spend variance (Brand CV=0.69, NB CV=0.43). Recommend a full market-specific fit.

**Warnings**:
- 2 regime change(s) documented in ps.regime_changes; ~8 weeks excluded from elasticity signal.
- 8 week(s) dropped from clean set due to nulls or zero spend.

### AU

- **Recommendation**: `regional_fallback`
- **Clean weeks**: 29 of 45 total (data range 2025-06-10 to 2026-04-12)
- **Brand spend variance (CV)**: 0.29 (need >= 0.2 for elasticity)
- **NB spend variance (CV)**: 0.36
- **Weeks with no ie%CCP**: 100%
- **Regime changes documented**: 4
- **Fallback region if used**: WW

**Explanation**: AU has 29 clean weeks — below the 80-week threshold for a market-specific fit. Use WW regional fallback. Credible intervals will be wider than fully-fit markets. Revisit after 51 more weeks.

**Warnings**:
- 4 regime change(s) documented in ps.regime_changes; ~16 weeks excluded from elasticity signal.
- 16 week(s) dropped from clean set due to nulls or zero spend.

## What to do with this report

1. Read the Summary table. Markets marked MARKET-SPECIFIC FIT are ready for Phase 1 fitting.
2. Markets marked `regional fallback` will use a regional average curve in v1. Wider credible intervals. Still trustworthy.
3. Markets marked SETUP REQUIRED cannot produce projections until more data accumulates. Re-audit next quarter.
4. Check the v1 Spec Alignment section. If any Fully_Fit_Market came back as fallback-recommended, update the spec before fitting.
5. This report is canonical for the current quarter. Next refit will generate a new one.

