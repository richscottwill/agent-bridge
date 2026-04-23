# AU W16 WBR Callout

**AU: AU drove 242 registrations (+45% WoW), with +7% spend WoW and CPA at $114 (-26% WoW).** April is projected at 38.2% of OP2 registrations and 36.2% of OP2 spend (vs OP2: -63.8% registrations, -63.8% spend). WoW recovery driven by Polaris un-gating being live for most of W16: NB registrations +62% (147 vs 91) on +10% NB spend, dropping NB CPA from $239 to $163. Brand registrations +25% with Brand spend -11%, pulling Brand CPA from $53 to $38. Polaris un-gating was reverted 4/18, so W17 will read the counterfactual. YoY comparison not available for W16 (2025 weekly data missing for this period).

**Note:** W15 was the low-water mark of the April drawdown (167 regs, $155 CPA); W16's rebound is the Polaris-live read, not a structural shift. The April pacing gap vs OP2 reflects the full month drawdown, not just W16.

**Next step:** W17 readout will isolate the Polaris revert impact. I will hold NB bid strategies steady through W17 to keep the counterfactual clean, then decide on a re-test or escalation based on the delta.

---

## Appendix

### Weekly trend (AU, W12→W16)

| Week | Regs | Spend | CPA | Brand Regs | Brand Spend | NB Regs | NB Spend |
|------|-----:|------:|----:|-----------:|------------:|--------:|---------:|
| W12 | 244 | $28.0K | $115 | 119 | $4.4K | 125 | $23.6K |
| W13 | 208 | $24.4K | $117 | 98 | $4.0K | 110 | $20.3K |
| W14 | 171 | $22.1K | $129 | 97 | $4.3K | 74 | $17.8K |
| W15 | 167 | $25.8K | $155 | 76 | $4.0K | 91 | $21.8K |
| W16 | 242 | $27.6K | $114 | 95 | $3.6K | 147 | $24.0K |

### April monthly projection

| Metric | Apr MTD (W14-W16) | OP2 Target | % of OP2 (stated) |
|--------|------------------:|-----------:|------------------:|
| Regs | 493 | 1,071 | 38.2% |
| Spend | $65.6K | $147.6K | 36.2% |
| CPA | $133 | $138 | — |

### Anomalies / context
- Polaris un-gating reverted 4/18 (Friday of W16). Most of W16 ran with Polaris un-gated.
- YoY baseline missing: `ps.v_weekly` has no 2025-W16 row for AU. Flag to re-pull from Y25 Final before publishing externally.
- CPA target check: ieccp is null in v_weekly for recent AU weeks; cannot report ie%CCP vs 100% target this week. Investigating source.
