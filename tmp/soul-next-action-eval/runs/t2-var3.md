# T2 · Var3 (Friction-Impact Sort) — MX Polaris Gen4 Ad Copy Readout

## Input
MX Polaris Gen4 ad copy test closed W16.
- **Gen4 variant** ("Business Pricing Exclusive"): 612 regs, $24.8K spend, CVR 4.1%, CPA $40
- **Gen3 control**: 548 regs, $24.6K spend, CVR 3.6%, CPA $45
- **Design**: 50/50 split, 4 weeks (W13–W16), powered to detect ≥5% incrementality at 80%
- **Observed lift**: +11.7% regs (612 vs 548), −11.1% CPA ($40 vs $45), +13.9% CVR (4.1% vs 3.6%)
- **Concern**: Yun-Kang flagged creative fatigue in W3

## Quick read
Lift is roughly 2× the minimum detectable effect the test was powered for. Spend is balanced ($24.8K vs $24.6K), so the CPA/CVR gap isn't a spend-skew artifact. Gen4 wins on every surface metric. The fatigue flag is the only reason not to roll immediately — if fatigue is real, the W16 readout overstates the durable lift.

## 2×2 sort of candidate next actions

| Action | Impact | Friction | Quadrant |
|---|---|---|---|
| A. Roll Gen4 to 100% MX Polaris now | High (locks in ~$5 CPA improvement at MX Polaris spend) | Low (flip split in ad platform, ~15 min) | **High Impact / Low Friction** |
| B. Check W-by-W trend for fatigue signal before rolling | High (prevents rolling a decaying variant) | Low (1 DuckDB query on weekly Gen4 vs Gen3 CPA/CVR trend) | **High Impact / Low Friction** |
| C. Write readout doc + socialize to Brandon/Yun-Kang | High (L1 artifact + L2 WW Testing credibility) | Medium (1–2 hr structured writeup) | **High Impact / Medium Friction** |
| D. Design Gen5 refresh now to pre-empt fatigue | Medium (future-dated, depends on B) | High (new creative brief, legal, MCS) | High Impact / High Friction — schedule, don't start |
| E. Replicate test in AU/US before MX rollout | Medium (generalizability evidence) | High (cross-market coordination) | Low–Medium Impact / High Friction — reject for now |
| F. Update WW Testing tracker row | Low (status hygiene) | Low (one line) | Low / Low — do as part of C |

## What the sort says
Two items sit in High Impact / Low Friction: **B (fatigue check)** and **A (roll to 100%)**. B gates A. The Yun-Kang concern isn't dismissable — if Gen4's lift is concentrated in W13–W14 and collapses by W16, rolling to 100% locks in a dying variant and you'll be defending it to Brandon in a month.

The Soul principles agree:
- **Evidence-based decisions grounded in testing** → don't roll on a topline without checking the fatigue claim.
- **Human-in-the-loop on high-stakes** → this moves >$50K/quarter at MX Polaris spend levels. Readout needs explicit confirmation before rollout.
- **Structural over cosmetic** → the fatigue check is a structural input to the decision. Skipping it is cosmetic confidence.

## Next step
**Run the weekly trend check first (Action B), then decide on A.**

Specifically:
1. Query `ps.v_weekly` for MX Polaris, Gen4 vs Gen3, W13–W16 — pull regs, spend, CVR, CPA per week per variant.
2. Test for fatigue: is Gen4's CVR lift vs Gen3 declining week-over-week? Is W16 Gen4 CPA materially worse than W13 Gen4 CPA?
3. If lift holds flat or grows across 4 weeks → fatigue concern is unfounded, roll Gen4 to 100%, write readout.
4. If lift decays W-over-W → hold the 50/50, write readout framing Gen4 as "wins on 4-week average but shows fatigue signal," and queue Gen5 creative refresh (Action D) before full rollout.
5. Either way, readout gets explicit Richard confirmation before socializing (high-stakes guardrail).

**One-line next action:** Query MX Polaris weekly Gen4 vs Gen3 trend W13–W16 to validate or refute Yun-Kang's fatigue flag before rolling to 100%.
