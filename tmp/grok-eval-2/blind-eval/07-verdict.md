---
title: "Blind Verdict — 07 WBR Narrative (MX W16)"
status: FINAL
audience: amazon-internal
created: 2026-04-22
evaluator: blind (no arm labels)
---

# Blind Verdict — 07 WBR Narrative (MX W16)

Ground truth: `shared/wiki/callouts/mx/mx-analysis-2026-w16.md` (W16 analyst brief).

## Q1 — Factual equivalence (MX numbers, WoW/YoY/pacing math)

**ARM-X:**
- W16 regs 510 (+0.2% WoW, +197% YoY) ✓
- Spend +7% WoW, CPA $53 (+7% WoW) ✓
- Brand regs +8% on +16% spend ✓ (brief: +7.6% / +16.0%)
- NB regs -19%, NB spend +5% (brief: +4.6%) ✓ rounded-acceptable
- NB CVR 1.32% → 1.13% (-14%) ✓ (brief: -14.6%)
- YoY: -3% spend / +197% regs ✓; Brand regs +456% ✓; NB regs +14% ✓
- April projection: $105K spend / 2.0K regs / $52 CPA. **Brief says ~$107K / ~2,000 / ~$54.**
  - Spend $105K vs $107K: rounded within $2K — fair.
  - CPA $52: ARM-X is using the MTD-through-W16 CPA, not the projected CPA ($54). Minor but wrong header number.
- vs OP2 pacing: **+199% spend, +154% registrations.** Brief says **+205% spend, +153% regs**.
  - Reg pacing +154 vs +153: acceptable rounding.
  - Spend pacing +199% vs +205%: **off by 6pp** — comes from using $105K not $107K.
- ie%CCP: explicitly flagged "pending (not in W16 source)" — honest gap.

**ARM-Y:**
- W16 regs 510 (+0.2% WoW), +7% spend, $53 CPA (+7%), 70% ie%CCP (vs 100% target) ✓
- April projection: $107K spend, 2.0K regs, $54 CPA ✓ (matches brief exactly)
- vs OP2: +153% regs, +205% spend ✓ (matches brief exactly)
- WoW Brand: +8% regs on +9% clicks (brief says +8.6% clicks — ✓)
- NB regs -19%, NB CVR -15% WoW (brief: -14.6%) ✓ rounded-acceptable
- YoY: -4% spend (brief: -3.5%), +197% regs, Brand +457%, Brand spend +267%, NB regs +14%, NB spend -21% (brief: -20.6%) — all match within rounding.
- W17 spend rec $28K ✓ matches brief.
- W16 NB CPA $183 ✓.

**Winner: ARM-Y** — projection, pacing vs OP2, and ie%CCP match the brief. ARM-X is directionally right but underprints the spend projection ($105K vs $107K) and the OP2 spend pacing (+199% vs +205%), and omits ie%CCP.

**Verdict: ARM-Y wins (PASS for Y, minor REGRESS for X).**

---

## Q2 — Quality vs Richard's WBR style (prose, no em-dashes, ~100–120 words, honest)

Style target (from `richard-style-wbr.md`): ~110 words (±10) for the prose callout, no em-dashes, specific attribution, separate Brand/NB, YoY context, forward-looking "I will" actions, Note: lines for context.

**ARM-X:**
- Em-dash count in file: **6.** Style guide is explicit: "Never use em-dashes in drafted callouts. Scan every draft before finalizing." Direct rule violation.
- Main callout paragraph ~180 words, well over the 110 ±10 target. Self-acknowledges "currently ~140; trim toward 110 if desired" in a reviewer note — honest but un-fixed.
- Three "Note:" lines — matches the style pattern.
- "I am investigating…", "I will flag to Yun and Lorena…" — good first-person forward actions.
- "ie%CCP pending (not in W16 source)" — honest about the gap, but the brief clearly states ie%CCP = 69.8% with source; ARM-X should have pulled it.
- Speculates Sparkle cannibalizes NB intent — **this is not in the brief.** The brief attributes NB softness to query-mix drift / LP / competitor IS, and does not mention Sparkle at all. ARM-X introduces a Sparkle-cannibalization hypothesis on its own initiative. Confident framing ("is likely suppressing NB CPA through upper-funnel absorption") is stronger than the evidence warrants.
- Reviewer comment at bottom is meta-commentary that wouldn't ship.

**ARM-Y:**
- Em-dash count: **2** (one stylistic in header comma, one in W17 watch bullet). Technically violates the rule, but materially closer to compliant.
- Main prose callout is two paragraphs ≈ 135 words. Slightly long but within the spirit of the target and much closer than ARM-X.
- Brand/NB split clearly separated.
- "Pulling the NB SQR with Yun-Kang this week to diagnose the three-week NB CVR slide before leaning NB spend up in W17" — concrete forward action, names a teammate, ties to the brief's recommendation.
- Attribution specific: "+8% Brand regs due to +9% clicks, continuing the Sparkle on-site 'Special Pricing for Business' placement."
- W17 watch / W17 optimization sections are useful decision inputs for Kate.
- Does **not** speculate beyond data. Sticks to what the brief supports.

**Winner: ARM-Y** — closer to word count, ~3x fewer em-dashes, more disciplined about speculation, cleaner forward action.

**Verdict: ARM-Y wins (PASS). ARM-X REGRESS on em-dash rule and word count.**

---

## Q3 — Contradictions vs ps.v_weekly W16 / analyst brief

**ARM-X:**
- Sparkle cannibalization claim ("NB CVR sliding… I am investigating whether Sparkle is cannibalizing NB intent into Brand, which would structurally compress NB CVR"). The brief says NB softness is "query-mix drift, competitor IS, LP issue" and makes no Sparkle-cannibalization claim. Not a direct contradiction but an unsupported hypothesis presented with investigation framing.
- FX claim "0.1818→0.1925 MXN→USD effective 4/1 (+5.9%). Applied to 4/1 forward. Partial driver of the April spend overshoot vs OP2." **The brief does not mention FX.** This is unverifiable from the provided sources. If FX is made up, it's a fabrication in a document headed to Kate.
- April projection $105K: brief says $107K. Close but inconsistent with the brief.
- OP2 pacing +199% spend: brief says +205%. Inconsistent.
- ie%CCP: ARM-X says "pending (not in W16 source)." The brief explicitly says ie%CCP = 69.8% (from `shared/tools/dashboard-ingester/data/2026-w16.json` — noted as primary source because v_weekly.ieccp is NULL). ARM-X didn't check the fallback source the brief documents.

**ARM-Y:**
- No contradictions against the brief on numbers.
- Brand regs +77% above 7-week avg, Brand CVR +30% above avg, total regs +47% above avg — all match the brief's ingester anomaly flags exactly.
- NB CPA $183 +29% WoW matches the brief.
- W17 recommended spend $28K matches the brief.
- 8-week trajectory matches the brief exactly.
- One minor: "-21% NB spend" YoY — brief is -20.6%, rounded-acceptable.

**Verdict: ARM-X contradicts the brief on projection/pacing and introduces unsupported Sparkle-cannibalization and FX claims. ARM-Y clean. ARM-Y wins.**

---

## Q4 — Gaps vs required callouts

Required by Richard: Sparkle → Brand regs, NB CVR slide, pacing vs OP2. Plus FX context (per user's prompt) and tough-but-fair questions.

**ARM-X:**
- Sparkle → Brand regs: ✓ (heavy emphasis, maybe too heavy)
- NB CVR: ✓ (-14%, called out)
- Pacing vs OP2: ✓ but with wrong numbers (+199% spend instead of +205%)
- FX context: ✓ (included; but appears to be a made-up rate not supported by the brief — can't verify)
- Tough-but-fair questions: Raises Sparkle run-length as forecasting risk (good), flags OP2 rebaselining to Yun/Lorena (good). But fails to ask about NB CPC $2.07 (12-week high) or the SURPRISE forecast accuracy — both in the brief.

**ARM-Y:**
- Sparkle → Brand regs: ✓ ("continuing the Sparkle on-site 'Special Pricing for Business' placement that started W15")
- NB CVR: ✓ (-15% WoW, three consecutive weeks, below 1.42% baseline)
- Pacing vs OP2: ✓ numbers match brief (+153% regs, +205% spend)
- FX context: ✗ **Not included.** This is a real gap against the user's prompt.
- Tough-but-fair questions: W17 watch asks three specific questions (NB CVR trajectory vs 1.42% baseline, NB CPA stability after $183 spike, Sparkle sustainability into third week). Also names the diagnostic path (pull NB SQR for query-mix drift / competitor IS / LP issues). Stronger than ARM-X on this dimension.

**Gap summary:** ARM-X includes FX (but possibly fabricated); ARM-Y omits FX entirely. ARM-Y is stronger on the other four. The FX gap in ARM-Y is real and should be flagged. The FX claim in ARM-X is worse because it introduces possible fabrication into a document going to Kate.

**Verdict: Mixed — ARM-X covers FX (weakly), ARM-Y covers everything else better. Net: ARM-Y wins on gaps because unverified FX is worse than missing FX.**

---

## Q5 — Decision utility: which would Richard put in front of Kate?

**ARM-X:**
- Numbers are off in two places Kate will notice: the April spend projection ($105K vs brief's $107K) and OP2 pacing (+199% vs +205%).
- Unverified FX claim + speculative Sparkle-cannibalization hypothesis creates two items Kate could challenge that Richard can't defend with data.
- Appendix tables are strong.
- Main paragraph is ~1.7x too long.
- Six em-dashes against an explicit style rule.
- Reviewer comment at the bottom would need to be stripped before sending.
- **Richard would not send this to Kate without meaningful rework.**

**ARM-Y:**
- Numbers match the brief.
- Forward actions are specific and named (NB SQR with Yun-Kang).
- W17 recommendations are actionable for Kate's review.
- Two em-dashes — still technically rule-breaking but easy to clean in a 30-second pass.
- Missing FX — Richard should add one line before sending.
- **Richard could ship this with minor edits.** That's the test.

**Verdict: ARM-Y wins.**

---

## Overall Winner

**Winner: ARM-Y**
**Margin: Decisive**

Scorecard:
- Q1 Factual equivalence: ARM-Y
- Q2 Style match: ARM-Y
- Q3 Contradictions: ARM-Y (ARM-X REGRESS)
- Q4 Gaps: ARM-Y (with caveat — missing FX)
- Q5 Decision utility: ARM-Y

ARM-Y is shippable with minor edits. ARM-X has two number mismatches with the brief, introduces an unverifiable FX claim and a speculative cannibalization hypothesis, blows the word budget by ~60%, and uses em-dashes 6 times against an explicit style rule. The only dimension where ARM-X does something ARM-Y doesn't is mention FX — and it does that in a way that would fail review.
