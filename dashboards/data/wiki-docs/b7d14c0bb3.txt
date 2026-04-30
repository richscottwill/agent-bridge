# MPE Notes — IT (Italy)

**Last fitted**: 2026-04-22 (v2 post-regime-audit)
**Strategy type**: `balanced` (50-65% ie%CCP range)
**Archetype for**: market with two structural shifts in 2026 (tax pause + OCI)

[38;5;10m> [0m## At a glance[0m[0m
[0m[0m
| Parameter | Value | Notes |[0m[0m
|---|---|---|[0m[0m
| Brand CCP | $151.67 | Column U FINAL ALIGNED |[0m[0m
| NB CCP | $92.03 | Column U FINAL ALIGNED |[0m[0m
| ie%CCP range | 50% – 65% | e.g., at 60% ie%CCP the blended CCP ≈ $0.60 × $151.67 + $0.40 × $92.03 = $127.81 |[0m[0m
| Supported target modes | spend / ieccp / regs | "spend" fixes total budget; "ieccp" optimises toward a target blended CCP; "regs" targets a registration volume |[0m[0m
| Brand spend share | 37.6% | High Brand mix relative to EU5 peers — for comparison, typical EU5 Brand share runs 25%–30% |[0m[0m
| Clean weeks | 164 | Represents ~3.15 years of usable data after removing promo, out-of-stock, and launch-distortion weeks |
## Fit quality summary

| Parameter | r² | MAPE | Fallback |
|---|---:|---:|---|
| brand_cpa_elasticity | 0.779 | 15.5% | market_specific |
| brand_cpc_elasticity | 0.820 | 7.5% | market_specific |
| nb_cpa_elasticity | 0.305 | 13.5% | regional_fallback |
| nb_cpc_elasticity | 0.305 | 9.0% | derived_from_cpa |
| brand_seasonality_shape | — | — | market_specific |
| nb_seasonality_shape | — | — | market_specific |
| brand_yoy_growth | 0.133 | — | market_specific |
| nb_yoy_growth | 0.609 | — | market_specific (strong!) |
| brand_spend_share | — | — | market_specific |

## Regime events

| Date | Event | Classification | Effect |
|---|---|---|---|
| 2024-05-15 | Google Bidding loss | **Structural** | -25% reg |
| 2025-06-15 | Brand CPC surge +124% YoY | **Structural** | Progressive degradation of IT Brand profitability |
| 2025-08-07 | CCP recalibration | Structural | IT Brand -13%, IT NB +7% vs static |
| 2026-02-18 | **PAM pause (22% tax)** | **Structural** | Permanent change in viable IT market |
| 2026-03-30 | IT OCI 100% | **Structural** | New baseline (very recent) |

## Known quirks and caveats

### 1. Double structural shift in 2026

IT experienced two structural shifts within 6 weeks: the 22% tax-driven PAM pause on 2026-02-18 (permanent market size reduction) followed by OCI launch on 2026-03-30. The fit captures the post-OCI reality (~4 weeks of data), and pre-regime data has been retained for shape context.

**Owner action**: IT projections in Q2 2026 will show wider CIs than other markets. At first refit (2026-07), expect significant tightening as post-PAM-pause stable data accumulates.

### 2. Progressive Brand CPC degradation through 2025

Per 2025 MBR: IT Brand CPC +124% YoY through 2025, reaching +29% CPA MoM in Oct 2025. Competition and max CPC cap binding. The structural regime flag for this event (2025-06-15) captures the timeline, but the degradation was progressive, not instant — so the fit naturally weights the more recent elevated CPC weeks.

### 3. NB YoY growth shows real signal (r²=0.609)

Unusual — most markets show weak NB YoY fits. IT's stronger NB YoY signal comes from the extreme 2025 spend reductions (-59% YoY NB investment) which create clear YoY comparison landmarks. Not a growth story — it's a story of controlled investment pullback.

### 4. Highest Brand spend share in EU5

IT runs 37.6% Brand vs EU5 peers 27-36%. Brand-heavy mix reflects strong brand term efficiency. This is partially offset by the Brand CPC surge noted above.

## File references

- Parameters: `ps.market_projection_params` WHERE market = 'IT'
- Regime events: `ps.regime_changes` WHERE market = 'IT'

## Regime update from 2025 MBR review (added 2026-04-22)

- **2024-05-15 Google Bidding loss (structural)**: IT lost Google bidding. Compounded through 2025 with the Brand CPC surge below.
- **2025-06-15 IT Brand CPC surge (structural)**: +124% YoY Brand CPC through 2025 with increasing competition. Brand CPA +62% YoY. Separate from the 2026-02-18 PAM pause — this is a persistent degradation of IT Brand economics that the fit absorbs as a new baseline.
- **2025-08-07 CCP recalibration (structural)**: IT Brand -13% ($112→$128 static), IT NB +7% ($75→$70 static). Brand CCP dropped meaningfully — partially offsetting the Brand CPC surge in the ie%CCP math.
- **2026-02-18 PAM pause (22% tax, structural)**: Paid Audience Marketing paused in IT due to 22% tax rate making the channel structurally uneconomic. Permanent change in viable IT market surface area, not a temporary shutdown.
- **2026-03-30 OCI 100% dial-up (structural)**: Very recent. New baseline overlaying all prior regime shifts.
- **NB YoY r²=0.609 unusual strength**: Driven by the -59% YoY NB spend reduction that created clear YoY comparison landmarks. Not an organic growth story — it's the signature of deliberate investment pullback in a market with 22% tax-driven headwinds.

IT has the densest active regime stack of any market (5 active events). The fit is usable but owner conversations about IT should always start from "what regime are we in" before "what does the number say."
