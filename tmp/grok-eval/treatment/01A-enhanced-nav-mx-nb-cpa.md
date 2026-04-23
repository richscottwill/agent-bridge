# MX NB CPA Trajectory — as of W16 (Apr 12–18)

**Short answer:** NB CPA is trending the wrong way. After 5 straight weeks in the $122–$142 band (W11–W15), **W16 spiked to $183** on the back of a NB CVR collapse from 1.32% → 1.13% while NB spend kept climbing. Apr MTD NB CPA is **$153** — the worst monthly NB CPA of the year and materially above the recent 13-week average (~$139).

## Weekly trend (NB only, `ps.v_weekly`)

| Week  | Start  | NB Regs | NB Spend | **NB CPA** | NB CVR |
| ----- | ------ | ------- | -------- | ---------- | ------ |
| W4    | Jan 18 | 117     | $11.5K   | $98        | 1.22%  |
| W5    | Jan 25 | 94      | $13.7K   | $146       | 1.15%  |
| W6    | Feb 1  | 89      | $11.8K   | $133       | 1.22%  |
| W7    | Feb 8  | 88      | $10.4K   | $118       | 1.34%  |
| W8    | Feb 15 | 98      | $13.8K   | $141       | 1.19%  |
| W9    | Feb 22 | 96      | $15.5K   | $161       | 1.13%  |
| W10   | Mar 1  | 98      | $16.2K   | $165       | 1.11%  |
| W11   | Mar 8  | 146     | $17.8K   | **$122**   | 1.56%  |
| W12   | Mar 15 | 121     | $16.0K   | $132       | 1.37%  |
| W13   | Mar 22 | 140     | $18.8K   | $134       | 1.46%  |
| W14   | Mar 29 | 124     | $16.1K   | $130       | 1.33%  |
| W15   | Apr 5  | 142     | $20.2K   | $142       | 1.32%  |
| **W16** | **Apr 12** | **115** | **$21.1K** | **$183** | **1.13%** |

## Monthly view (NB, `ps.v_monthly`)

| Month           | NB Regs | NB Spend | **NB CPA** |
| --------------- | ------- | -------- | ---------- |
| Jan             | 451     | $45.0K   | $100       |
| Feb             | 371     | $51.5K   | $139       |
| Mar             | 562     | $76.4K   | $136       |
| **Apr MTD (18d)** | **324** | **$49.7K** | **$153**   |

## Trajectory read

- **Direction:** Deteriorating. W16 broke out of the Mar–early-Apr band by ~$40+ and is the highest NB CPA since W10.
- **Driver:** It's a CVR problem, not a cost-per-click problem. NB CVR has stair-stepped down from the W11 peak (1.56%) for four straight weeks → 1.13% in W16, back near February lows. NB CPC is basically flat (~$1.9–$2.1).
- **Sunday softness:** Sun Apr 12 (16 regs, $179 CPA) and Sat Apr 18 (10 regs, $224 CPA) were particularly weak and pulled the week down.
- **Spend is not backing off:** NB cost rose again in W16 ($21.1K, highest of the year) even as regs dropped. We're buying the same click volume into a weakening conversion rate.

## Frame vs OP2

- OP2 for Apr is a blended $44 CPA at 791 regs / $35.1K spend. Not a NB-only target — and the callout doc flags OP2 as predating Brand coverage scaling, so the blended number isn't the live planning frame.
- The NB-only comparable is the recent NB CPA band (~$122–$142 in Mar). W16 at **$183 is +30% above that band**. That's the right frame for "is this a real deterioration." It is.

## What's worth checking next

1. **Is the CVR decline concentrated anywhere?** Device, campaign, or query bucket — pull daily NB CVR by campaign to see if it's broad-based or one or two campaigns dragging.
2. **Yun Kang's NB drop note** (`shared/context/intake/drafts/2026-04-22-yun-kang-mx-nb-drop.md` — open in your editor) likely covers the same W16 deterioration. Worth reconciling before it goes to Brandon.
3. **Week-to-date W17:** One day of daily data only (Apr 19+ not yet in `v_daily`). If W17 stays weak, this isn't a single-week blip.

## Source

- `ps.v_weekly`, `ps.v_monthly`, `ps.v_daily` filtered on `market='MX'`
- Data snapshot: `AB SEM WW Dashboard_Y26 W16.xlsx`
- Cross-ref: `shared/wiki/callouts/mx/mx-projections.md` (W16 projection context)
