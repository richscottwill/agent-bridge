# T4 Blind Verdict — Wednesday 2026-04-22 AM Daily Brief

**Evaluator context:** Four outputs scored against the five criteria below. META criterion (always-on cost) carries extra weight because this procedure fires **daily** — a small bloat compounds to hours/week of Richard's morning.

**Criteria recap:**
1. Clarity of Next Best Action (time-anchored, unambiguous)
2. Decision Quality (ranking given the stakes)
3. Adherence to principles (Subtraction / reduce-decisions / invisible-over-visible)
4. Overall Usefulness (would Richard actually use this?)
5. META — Always-on cost (earns its place daily, or becomes ceremony?)

---

## Summary Table

| Arm | C1 NBA | C2 Decision | C3 Principles | C4 Useful | C5 Always-on | **Total** | Rank |
|-----|--------|-------------|---------------|-----------|--------------|-----------|------|
| ARM-A (var1) | 7 | 7 | 6 | 6 | 4 | **30** | 3 |
| ARM-B (var2) | 9 | 5 | 6 | 7 | 7 | **34** | 2 |
| ARM-C (baseline) | 8 | 8 | 7 | 8 | 6 | **37** | **1** |
| ARM-D (var3) | 8 | 8 | 8 | 8 | 7 | **39** | **1 (tie, preferred)** |

**Verdict: ARM-D wins narrowly over ARM-C.** Both surface the hard-thing correction cleanly and time-anchor the NBA. ARM-D edges ahead on principle alignment (explicit protocol check, fail-loud friction fix, cleaner subtraction) and marginally tighter always-on cost. ARM-C is very close and still the strongest of the first three on pure decision quality (best stack-rank of priorities). ARM-B is usable but makes the wrong call on the hard thing. ARM-A is the longest and the weakest ROI per byte.

---

## ARM-A (var1) — 30/50

**The call:** Hard thing = polaris-brand-lp. NBA = Polaris one-pager before 1:1. Five priorities, heavy NBA-mandate framing.

**Strengths**
- Correctly identifies polaris-brand-lp as rank 1 and makes it NBA.
- Time-ordered top-3 is clean (10:00 MX → pre-1:30 Polaris → pre-WBR Yun).
- Leverage move is sharp: scope the AU aggregator *before* 5/5 handoff to flip the handoff narrative. That's a real insight.
- Good principle tagging (#2 structural, #8 device.md check).

**Weaknesses**
- **Bloat.** NBA Mandate preamble ("Triggers that fired…") is meta-ceremony. Richard doesn't need to know which triggers fired daily — he needs the brief. This is the single clearest violation of invisible-over-visible: the machinery is visible.
- Ends with a redundant "Next Best Action (NBA Mandate)" block repeating priority #1. Belt and suspenders. Choose one.
- Two separate "hard thing" recommendations (Polaris #1, AU aggregator as leverage move) creates competing NBAs — reintroduces a decision Richard has to make. Fails "reduce decisions, not options."
- Longest of the four. Daily × bloat = morning tax.

**Always-on take:** If this runs every day, the NBA Mandate header + trigger audit + closing NBA block is ~15% of the brief's real estate doing zero work for Richard. Ceremony.

---

## ARM-B (var2) — 34/50

**The call:** Hard thing = Testing Doc v5 (overrides the tracker). NBA = send v5 before 10 AM. 2x2 tool invoked to break tie. OOO wall flagged.

**Strengths**
- **Best NBA clarity of the four.** "Send Testing Doc v5 before 10 AM PT today" is unambiguous, time-anchored, and defensible.
- OOO 4/23–4/25 context — no other arm caught this and it's structurally the most important fact on the page. A 3-day OOO changes what "today" means.
- 2x2 is earned — HI/LO vs HI/HI is exactly the right frame for the Testing Doc vs Polaris tradeoff.
- Routes the structural fix to karpathy correctly.

**Weaknesses**
- **Wrong call on the hard thing.** The task brief explicitly says "the hard thing was recently corrected in the ledger: polaris-brand-lp." ARM-B overrides the corrected ledger to reassert Testing Doc. It argues the position in §3 — which is intellectually honest — but the net effect is: Richard asked the system to respect the correction, and it respected it in the data snapshot while ranking priorities against it. Decision quality penalty.
- "5 critic fixes" is referenced but not listed — asking Richard to go find them adds friction instead of removing it.
- Renames AU pacing 🔴 → 🟢 vs ARM-A/C/D that show 🔴. Data inconsistency. Minor but erodes trust in a daily artifact.

**Always-on take:** Length is reasonable, 2x2 is a good tool but won't fire every day (by design — "Optional 2x2" is the right framing). The OOO-wall check should be a permanent structural element of the brief. Earns its place most days.

---

## ARM-C (baseline) — 37/50

**The call:** Hard thing = polaris-brand-lp with ledger-conflict warning at top. Top-3 time-ordered (10:00 MX → pre-1:30 Polaris → pre-WBR Yun). Testing Doc demoted to "recovery of visibility" Core #2.

**Strengths**
- **Best ledger-conflict flagging of any arm.** Opens with the correction, names the stale source (daily-brief-latest.md), and commits to the corrected view. Exactly the "a good brief flags that correction" behavior the eval calls for.
- **Best decision quality.** Testing Doc as "recovery send, not strategic" is a sharper frame than any other arm. It acknowledges the L1 streak wound without promoting it above the tracker's rank-1 signal.
- Leverage move (AU aggregator scope doc) is connected to a real Brandon ask with a forcing function (5/5 handoff), and explicitly principle-checked.
- Friction section is genuinely structural: pre-drafted Brandon sends folder, subtracts Section 10 of the brief itself (**subtraction-before-addition earned**).
- "What to do next" closing block gives a clear ordered sequence.

**Weaknesses**
- Longer than ARM-D. Closing "What to do next" section repeats top-3 with slight variations — mild redundancy.
- 5 open questions × 3-option choices = more decisions than strictly needed; some could be collapsed to binary.
- "Right now (before 08:30 PT): open Polaris channels and start the written POV" — competes slightly with the 10 AM MX send as NBA. Could be sharper.

**Always-on take:** Solid. Each section does work. The redundancy in the closing block would cost Richard ~30 seconds/day; over a year that's ~3 hours. Trimmable.

---

## ARM-D (var3) — 39/50

**The call:** Hard thing = polaris-brand-lp, correction flagged at top. NBA = ship Polaris timeline one-pager today. High-Stakes Clarity Check triggered on MX 150% spend. Protocol alignment check at the end.

**Strengths**
- **Correction handling matches ARM-C's quality and is slightly tighter.**
- **High-stakes guardrail box is the best structural feature across all four arms.** Explicit numeric confidence / top-3 assumptions / human-review flag / IECCP binary — that's soul.md principle #7 operationalized, not just cited.
- "Stop if it's 11am and nothing is out — narrow to the Dwayne reply alone" — best fallback logic of any arm. Anticipates the failure mode.
- Leverage move frames Polaris as a *coordination artifact* (4 people asking in 4 channels → publish once), not a strategy doc. Sharpest L2-vs-L3 distinction of any arm.
- Motherduck_token fix in §3 is genuinely the right structural friction to remove — the tracker correction today only happened *despite* that break. Fixing it is higher-leverage than any other friction fix proposed.
- **Principle check at the end is invisible-over-visible done right** — it's a self-audit that confirms alignment, not a trigger-list advertisement like ARM-A.
- Catches the Asana housekeeping gap (Testing Doc task still 22d overdue because it wasn't marked complete). Small but high signal-to-noise.

**Weaknesses**
- "Karpathy Phase 6: invokeSubAgent nested-call limitation — blind eval blocked" leaks implementation detail Richard doesn't need in an AM brief. Remove.
- Five Levels tie-back + Protocol alignment check = two closing self-audits. One is enough; the other is ceremony.
- Slightly wordier than necessary in Priority #1 ("Minimum viable today… Stop if… Non-negotiable…") — three lines where two would do.

**Always-on take:** The high-stakes guardrail box is the single feature across all four arms most worth keeping permanently. It's conditional (only fires on >$50K triggers), so it doesn't tax low-stakes days. The protocol alignment check trims well — could become invisible after a few weeks of conscious-competence practice. Best daily ROI of the four.

---

## Cross-cutting Observations

**The hard-thing correction test.** The eval specifically called out whether briefs flag the polaris-brand-lp correction. Results:
- **ARM-A:** flags it as a "hard thing pivot detected" trigger. Good.
- **ARM-B:** flags it but then overrides it in priority ranking. Mixed.
- **ARM-C:** flags it best — names the stale source, commits to corrected view.
- **ARM-D:** flags it at the top in a dedicated "Correction" block. Cleanest reader experience.

**The always-on cost test.** If this runs daily:
- ARM-A's "NBA Mandate" scaffolding is pure ceremony and would compound badly.
- ARM-B's "Optional 2x2" is the right pattern (conditional tooling) but would fire rarely.
- ARM-C's structure is trimmable but each section earns its place today.
- ARM-D's high-stakes guardrail is conditional (only fires on qualifying triggers) — the single most defensible always-on feature across the four.

**Time-anchoring.** ARM-B, ARM-C, ARM-D all time-anchor the top-3 queue properly. ARM-A does too but buries it under the NBA-mandate preamble.

**Length.** Rough word counts (priorities-section onward): ARM-A longest, ARM-C second, ARM-D third, ARM-B shortest. Given daily cadence, ARM-B's brevity is a real advantage — tempered by the wrong call on the hard thing.

---

## Recommendation

**Adopt ARM-D as the daily-brief template**, with two trims:
1. Drop the "Karpathy Phase 6" meta-note and the nested-agent line from §4. Leaks implementation detail.
2. Collapse "Five Levels tie-back" + "Protocol alignment check" into one closing block, or rotate them (one per day). Two closing audits is ceremony; one is discipline.

**Borrow from ARM-B:** permanent OOO-wall check as a structural section. If today is the last working day before a block of PTO, that fact belongs at the top of the brief, not in the agent's head.

**Borrow from ARM-C:** the "pre-drafted Brandon sends folder" friction fix. That's the best structural intervention of any brief — it attacks the actual root cause of the 23-workday streak pattern.

**Discard from ARM-A:** the NBA Mandate trigger preamble and the trailing NBA block. Ceremony.

The always-on dimension matters. A brief Richard reads in 90 seconds and acts on beats a brief he reads in 4 minutes and thinks about. ARM-D is closest to 90 seconds with full signal retained.
