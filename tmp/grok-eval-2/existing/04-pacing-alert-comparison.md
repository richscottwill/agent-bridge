# Pacing Alert — Grok Proposal vs Existing Machinery

## Grok's proposal (shared/tmp/grok-eval-2/proposed/04-pacing-alert.md)
- Daily check: MTD spend + regs vs OP2 monthly target per active market.
- Tiered output: 🔴 >20% off, 🟡 10–20% off, 🟢 within 10%.
- Single-line per market. Recommend action on under/overpacing.

## Existing machinery

### 1. `ps.monthly_pacing` (DuckDB view) — the data layer already exists
Columns: market, current_month, mtd_regs, mtd_cost, op2_regs_target, op2_cost_target, pacing_regs_pct, pacing_cost_pct.

Live query result (2026-04-22, 2026-M04):
| market | pacing_regs_pct | pacing_cost_pct |
|---|---|---|
| AU | 38.2 | 36.2 |
| CA | 60.0 | 54.4 |
| DE | 47.8 | 51.4 |
| ES | 61.5 | 72.3 |
| FR | 46.5 | 58.0 |
| IT | 41.8 | 56.3 |
| JP | 58.7 | 52.6 |
| **MX** | **128.8** | **150.1** |
| UK | 68.4 | 53.6 |
| US | 59.5 | 47.9 |

The comparison Grok proposes to "build" is a single `SELECT * FROM ps.monthly_pacing` away. It ships with every ingest.

### 2. Daily brief — already surfaces this in Section 9
From shared/context/intake/daily-brief-latest.md:
> ## 9. PACING — vs OP2 (ps.monthly_pacing)
> - **MX**: 🔴 128.8% regs / **150.1% spend** — OVERSPENT. Forecast decay required BEFORE Brandon 10am send.
> - **AU**: 🟢 38.2% regs / 36.2% spend — on pace for early-month.

Format:
- Already one-line-per-market.
- Already uses 🔴/🟢 emoji tiering.
- Already pulls MTD vs OP2 regs + spend.
- Already drives action: MX overpace cascades into Section 10 action queue ("10:00 PT — MX forecast to Brandon with decay narrative (pacing 150% spend — must explain)").

### 3. `market-constraints-staleness-alert.kiro.hook` — unrelated
This hook flags rows in `ps.market_constraints_manual` not touched in >60 days (governing_constraint, handoff_status, OCI status). It's about metadata staleness, not pacing. No overlap with Grok's proposal.

### 4. `am-backend.kiro.hook` — runs the parallel ingest that populates the brief
v5.2.1, userTriggered. Executes `~/shared/context/protocols/am-backend-parallel.md` which produces the daily brief containing Section 9. So the pacing tiering is running on every backend invocation (morning routine cue).

## Head-to-head

| Grok's feature | Existing coverage | Gap? |
|---|---|---|
| Compute MTD vs OP2 per market | `ps.monthly_pacing` view | None |
| Regs + spend | `pacing_regs_pct`, `pacing_cost_pct` columns | None |
| Daily cadence | am-backend fires on morning routine → Section 9 refreshes | None |
| One-line per market | Section 9 format | None |
| Emoji tiering (🔴🟡🟢) | Daily brief uses 🔴/🟢 | **Partial — 🟡 middle band not used** |
| Explicit threshold bands (10% / 20%) | Not documented in brief; thresholds applied implicitly | **Partial — thresholds implicit, not codified** |
| "Recommend [action]" text | Section 10 action queue derives from Section 9 | None (handled downstream) |

## Verdict

**Existing daily brief pacing section already covers Grok's proposal — with one minor convention gap.**

Every substantive piece of Grok's proposal already ships daily:
- The data layer (`ps.monthly_pacing`) is live and accessible.
- The brief prints one-liners per market with emoji tiers.
- The action queue downstream consumes the pacing signal (MX 150.1% drove today's 10am Brandon send).
- The am-backend hook already fires this on the morning routine cue.

Grok's "add this alert" framing misses that the alert exists. What Grok does catch that's real:

1. **🟡 middle band is unused.** Today's brief has 🔴 MX and 🟢 AU — no 🟡. Once other markets drift into the 90–110% window (which they will), we'll need a tier for it. Codifying "🔴 >20% off, 🟡 10–20% off, 🟢 within 10%" as the convention is a cheap, invariant-preserving tweak to Section 9.
2. **Thresholds are implicit.** The brief assigns 🔴/🟢 by vibe, not by a written rule. Writing the rule into the am-backend protocol (not a new hook, not a new alert) makes the coloring reproducible across sessions and survives a platform migration (portability rule #12).

## Recommendation (framed against the 8 principles)

**Do not adopt Grok's alert as a new hook.** Do the following instead:

1. **Subtraction before addition (#3):** No new hook. No new file. Amend the am-backend protocol's Section 9 spec.
2. **Structural over cosmetic (#2):** Add the threshold rule (🔴 >±20pp from 100, 🟡 ±10–20pp, 🟢 within ±10pp) to the protocol spec so Section 9 renders consistently. This is structural — it codifies behavior, not layout.
3. **Invisible over visible (#5):** Richard doesn't notice a new alert fires; the Section 9 line just gets a 🟡 when warranted.
4. **Protect the habit loop (#4):** Cue (morning brief) and reward (action queue) unchanged. Only the routine inside Section 9 is tightened.
5. **Portability (#12):** Write the thresholds in plain text in the protocol so a cold-start agent computes the same tiers.

**Grok's add-value contribution:** the explicit 10%/20% threshold convention. That's worth adopting into the Section 9 rendering spec. Everything else is already done.

## One-line reply
Existing daily brief Section 9 already delivers Grok's pacing alert using ps.monthly_pacing — adopt only the explicit 10%/20% threshold convention and the 🟡 middle band; don't build a new hook.
