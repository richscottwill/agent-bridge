# US Full-Year Spend Ceiling — Leverage Cascade Run (var5)

**Prepared:** 2026-04-23 · **Market:** US · **Framework:** ie%CCP ceiling + leverage cascade
**Confidence: 55%** · **Human review strongly recommended before action.**

---

## The cascade, applied first

Before answering the ceiling question, I ran the 5-step leverage cascade per the active steering in `var5-leverage-cascade.md`. This determines what you should actually do — not what you asked me to calculate.

### Step 1 — Current daily Leverage Move (from current.md)

> **Testing Approach v5 to Brandon: STILL UNSENT. 23 workdays at zero L1. PUBLISH verdict (8.4/10) since 4/5. Do this FIRST thing tomorrow AM — it's a 10-min SEND, not a work session.**

This is still valid. It is listed as the top item in `current.md` under 🔴 Live tomorrow, the latest brief hasn't been superseded, and nothing in today's activity closed it out. **Cascade stops here in principle** — step 1 governs.

### Step 2 — Highest Five Levels opportunity visible

L1 (Sharpen Yourself, consecutive weeks shipped) is the active and struggling level. 23 workdays at zero L1 = the streak is broken and the level is in failure mode. The Testing Approach send is the L1 ship. No other visible move restores L1 faster.

Answering the US ceiling Q is L2 (Drive WW Testing) or arguably L1 as an artifact — but only *if* it gets shipped to someone. As a private calculation, it's L0. Bandwidth, not leverage.

### Step 3 — Biggest friction point blocking multiple future actions

The unsent v5 is also the single biggest friction point. It blocks:
- the L1 streak restarting (can't re-start a weekly-artifact streak while the hero artifact sits un-shipped)
- Kate-visible work (Annual Review growth area was visibility — this is a visibility deliverable)
- your ability to credibly commit to anything else Brandon assigns (each new commitment competes with the v5 overhang)
- the Friday retrospective (Friday with another zero-L1 week is worse than Friday with a send)

### Step 4 — Protect the habit loop

The L1 habit loop has already broken. The cue (weekly output) → routine (write/send) → reward (artifact shipped, streak intact) sequence isn't firing. At 23 workdays dark, this isn't experimentation-within-the-routine; the routine has collapsed. **Sending v5 is the single cheapest action that puts the loop back together** — it's the reward half of the loop, re-established in ~10 minutes.

### Step 5 — Only then, any other useful task

The ceiling question goes here. It is a useful task. It is not today's highest-leverage action.

### Final filter — is there a smaller move that's even higher leverage?

Yes. Smaller than "compute the US full-year ceiling." Smaller than "write the POV." Smaller than anything you've queued.

**The smaller move: forward the existing v5 doc to Brandon with one sentence — "Published verdict, ready for your eyes." No rewrite. No fifth pass of subtractive edits. Send.**

Everything downstream of that (ceiling POV, OCI validation, Kate-visible narrative) becomes available again *after* the send. Nothing downstream is available *before* it.

**What the cascade says you should do next: send Testing Approach v5 now. The ceiling Q can wait 10 minutes.**

---

## But you asked for the number. Here it is.

### TL;DR

**Pure ceiling (theoretical, if we held 100% ie%CCP all year with OCI 10% CVR lift): ~$77.0M**

**Pragmatic ceiling (YTD W1–W16 locked at 46% ie%CCP actuals + W17–W52 at 100%): ~$63.1M**

Either number is ~1.8–2.3× OP2 spend of $34.1M. The headroom exists because YTD US is running at only **46.1% ie%CCP** — we're leaving roughly half the allowed CCP on the table.

### Inputs (verified from source)

| Input | Value | Source |
|---|---|---|
| Brand CCP | $412.51 | provided, consistent with `ps.market_projection_params_current` |
| NB CCP | $48.52 | same |
| YTD Brand regs (W1–W16) | 42,637 | `ps.v_weekly` |
| YTD Brand spend | $3,014,649 | `ps.v_weekly` |
| YTD Brand CPA | $70.70 | derived |
| YTD NB regs (W1–W16) | 93,999 | `ps.v_weekly` |
| YTD NB spend | $7,199,053 | `ps.v_weekly` |
| YTD NB CPA | $76.59 | derived |
| YTD total spend | $10,213,702 | `ps.v_weekly` |
| YTD ie%CCP (actual) | **46.1%** | $10.214M / (42,637 × $412.51 + 93,999 × $48.52) |
| OP2 FY spend target | $34,077,222 | `ps.targets` |
| OP2 FY regs target | 360,833 | `ps.targets` |

### Formula

```
ie%CCP = spend / (brand_regs × brand_CCP + nb_regs × nb_CCP)
At 100%: spend_ceiling = brand_regs × $412.51 + nb_regs × $48.52
```

### Math

Remaining 36 weeks at YTD run-rate, with 10% CVR lift applied (same clicks → 10% more regs):

- Brand remaining lifted: (42,637 / 16) × 36 × 1.10 = **105,526 regs**
- NB remaining lifted: (93,999 / 16) × 36 × 1.10 = **232,647 regs**

W17–W52 allowance at 100% ie%CCP:
- 105,526 × $412.51 + 232,647 × $48.52 = $43.531M + $11.286M = **$52.817M**

Plus YTD locked spend of $10.214M → **full-year ~$63.0M**.

Pure (as if all 52 weeks had held 100% with the lift): (42,637 + 105,526) × $412.51 + (93,999 + 232,647) × $48.52 = **~$77.0M**.

### Top 3 assumptions that materially move the number

1. **Brand/NB mix holds at YTD ratio (31% brand regs / 69% NB regs).** Brand CCP is 8.5× NB CCP, so mix dominates. Sensitivity: 25/75 mix drops pure ceiling to ~$68M; 37/63 raises it to ~$86M. OCI tends to optimize NB more than brand → real mix likely skews NB → ceiling likely lower than $77M.
2. **10% CVR lift translates 1:1 into 10% reg lift at same click volume.** If actual US lift is 7%, pure ceiling drops to ~$75.6M; if 13%, rises to ~$78.4M. OCI lift magnitude is not measured for US — it's your stated assumption.
3. **No elasticity / diminishing returns applied.** This is a linear CCP cap. At an MX-like exponent of 0.937, delivering ~475K regs at 100% ie%CCP would require higher CPAs than assumed. Realistic ceiling is likely $65–70M before efficiency degradation bites, not $77M. MPE Task 3.1 (US elasticity fit) is open.

### Why 55% confidence (not higher, not lower)

- **Not higher:** US elasticity exponent isn't fit; 10% OCI lift isn't measured for US; mix held constant but OCI will distort it; Brand CCP $412 assumes 148K US brand regs at YTD CPA — search demand may not sustain it.
- **Not lower:** formula is canonical and verified; CCPs and YTD data are from source-of-truth; 46% YTD baseline is solid, so the direction (large headroom) is not in doubt.

### Flags

- OP2 $34.1M is set at ie%CCP well below 100% — the ceiling is a math cap, not a recommendation.
- US elasticity exponent not yet fit (MPE Task 3.1 open).
- OCI 10% CVR lift is your stated assumption — not measured for US.
- US governing constraint is "efficiency + volume balance" per `ps.market_constraints`. Leadership will cap well below $77M even if the math supports it.

---

## Where this overlaps with the baseline run

The numbers in this file match `t1-baseline.md`. This run wasn't a re-calculation — it was a cascade check on whether answering this question was the right use of the next 30 minutes. It isn't.

**Richard — what to do next (cascade output, not analysis output):**

1. **Hit send on Testing Approach v5 to Brandon.** First thing tomorrow AM. No more edits. This is the cascade answer.
2. **After the send,** the ceiling conversation is available as a weekly artifact — "US ie%CCP headroom + OCI lift." That is a *second* L1 artifact this week. It is a bonus, not a substitute.
3. **Do not quote $77M externally.** Theoretical cap, unfit elasticity, unvalidated US OCI lift. Human review before any stakeholder conversation.
4. **Reframe the story when you do use it:** "US is at 46% ie%CCP YTD — significant room before any efficiency wall." That is the durable line. The ceiling number itself is sensitivity-dependent.

**Human review strongly recommended before action.**

---

## Soul.md principle check

- ✅ **Routine as liberation** — cascade protects routine by putting the L1 habit-loop repair ahead of new analytical work.
- ✅ **Subtraction before addition** — the cascade's final filter made me subtract, not add. I did not produce a new doc, new spec, new POV. The baseline already answers the ceiling Q.
- ✅ **Protect the habit loop** — step 4 is the whole point. v5 send is the smallest action that restarts the broken L1 loop.
- ✅ **Human-in-the-loop on high-stakes** — `high-stakes-guardrails.md` is loaded (filename matches `ceiling`). Explicit confidence, top-3 assumptions, human-review flag all present.
- ✅ **Invisible over visible** — the cascade output isn't a new tool or new framework. It's "apply existing steering, answer the simpler question underneath the asked question."

## Provenance

- Data: `ps.v_weekly` (US, 2026-W01–W16), `ps.targets` (US 2026-M01–M12)
- Formula: `.kiro/specs/market-projection-engine/tasks.md` Task 1.9; `shared/context/protocols/state-file-mx-ps.md` ie%CCP constraint model
- Framework: `shared/wiki/agent-created/strategy/ieccp-planning-framework.md`
- Cascade: `shared/tmp/soul-next-action-eval/proposed/var5-leverage-cascade.md`
- Guardrails: `.kiro/steering/high-stakes-guardrails.md` (auto-loaded on filename match)
- Compared against: `shared/tmp/soul-next-action-eval/runs/t1-baseline.md`
