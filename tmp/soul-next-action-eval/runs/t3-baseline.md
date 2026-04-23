# AU W16 WBR Callout — DRAFT

**Reporting week:** 2026-04-13 to 2026-04-19 (W16)
**Audience:** Kate + marketing leadership
**Status:** Draft for Richard review before WBR cut

---

## Callout

AU drove 242 registrations (+45% WoW) on $27.6K spend (+7% WoW), CPA $114 (-26% WoW). WoW lift reflects recovery from the Polaris brand LP un-gating test, which was reverted 4/18 after driving -34% NB CVR and -20% brand CVR during W15. NB registrations +62% with NB CVR rebuilding from 2.0% (W15) to 2.9% (W16), NB CPA -32% to $164. Brand registrations +25% on -11% spend, brand CPA $38 (-29%), CVR returned to 7.8% baseline. April projected at ~$108K spend, ~814 registrations at ~$132 CPA (vs. OP2: -27% spend, -24% registrations, -4% CPA). YoY unavailable: v_weekly history does not extend to 2025-W16. **Recommend human review before quoting April projection externally.**

Note: The W16 recovery confirms the test revert decision. CVR trajectory through 4/19 (2.9% NB blended) is holding at pre-test levels; I will monitor W17 to confirm the recovery is stable rather than a rebound spike.

Note: AU April pacing tracks ~46% of OP2 regs and ~44% of OP2 spend through 19 of 30 days (63% linear). The -24% registration gap is structural for the month, not a W17 correction target.

\* Projection method: MTD actuals through 4/19 + 14-day trailing daily average (29.2 regs/day, $3.8K/day) extrapolated over remaining 11 days. Top assumptions: (1) post-revert CVR holds at W16 levels, (2) no further Polaris-driven disruption, (3) spend caps unchanged. If W17 NB CVR reverts toward W15 levels, registration projection drops to ~730 (-32% vs OP2).

---

## Appendix

### Weekly trend (AU, last 6 weeks)

| Week | Regs | Spend | CPA | NB Regs | NB CPA | NB CVR | Brand Regs | Brand CPA | Brand CVR |
|------|------|-------|-----|---------|--------|--------|------------|-----------|-----------|
| W16  | 242  | $27.6K | $114 | 147 | $164 | 2.9% | 95 | $38 | 7.8% |
| W15  | 167  | $25.8K | $155 | 91  | $239 | 2.0% | 76 | $53 | 6.0% |
| W14  | 171  | $22.1K | $129 | 74  | $240 | 1.9% | 97 | $44 | 6.9% |
| W13  | 208  | $24.4K | $117 | 110 | $185 | 2.6% | 98 | $41 | 7.4% |
| W12  | 244  | $28.0K | $115 | 125 | $189 | 2.8% | 119 | $37 | 8.5% |
| W11  | 241  | $31.0K | $129 | 133 | $198 | 2.8% | 108 | $43 | 7.8% |

### April MTD vs OP2 (through 4/19, 19 of 30 days)

| Metric | MTD | OP2 | % of OP2 | Linear pace |
|--------|-----|-----|----------|-------------|
| Registrations | 493 | 1,071 | 46.0% | 63.3% |
| Spend | $65.6K | $147.6K | 44.4% | 63.3% |
| CPA | $133 | $138 | — | — |

### Daily NB/Brand CVR pattern around the Polaris revert

- 4/12 (Sun): NB 2.77%, Brand 9.85% — test still live, slight recovery day
- 4/13 (Mon): NB 3.01%, Brand 7.07% — recovery continuing
- 4/14-4/17: NB 2.79-3.26%, Brand 4.55-8.68% — stable at post-test levels
- 4/18 (revert day): NB 2.48%, Brand 6.45% — holiday-adjusted normal
- Contrast W15 test days: NB 1.66-2.36% (low), Brand 1.55-10.34% (volatile)

### Assumptions & confidence

- **Confidence: Medium (60%).** W16 recovery is directionally clear, but a single week post-revert is not a durable signal. W17 reads the true post-test steady state.
- **Data gaps:** No YoY baseline (v_weekly 2025 history starts 2025-06-10). Cannot confirm whether April pacing gap is structural vs. YoY-comparable.
- **Projection sensitivity:** Registration projection range 730-880 depending on NB CVR trajectory.

---

## What Richard should do next

1. **Before WBR cut**: Send this callout to the WBR callout pipeline hook at `shared/.kiro/hooks/wbr-callouts.kiro.hook` for callout-writer/reviewer review. Per soul.md routing, callouts are not drafted in the default agent voice — this is a first pass, not the publish version.
2. **Today**: Confirm the April projection (-27% spend / -24% regs vs OP2) with Brandon before it lands in Kate's view. This is the number leadership will ask about, and it's the first post-test projection.
3. **W17 data drop**: Validate that NB CVR holds at 2.8-3.0%. If it reverts toward 2.0%, the April projection collapses and the recovery narrative needs rewriting.
4. **Source the YoY baseline**: v_weekly has no 2025-W16. Pull 2025 AU weekly from the WW Dashboard Y25 Final and backfill — every future AU callout needs YoY context per richard-style-wbr.md.
