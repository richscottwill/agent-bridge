# Pair 01A — MX NB CPA Trajectory

## Q1 — Factual equivalence
Verdict: equivalent (both factually sound, arm-Y very slightly off on one rounding)
Reasoning: Both match `ps.v_weekly` for W16 ($183.37 CPA, 115 regs, $21.1k cost, 1.13% CVR) and for the preceding 12–15 weeks. Both correctly identify the W15→W16 CVR compression as the driver and note flat CPC. Arm-X includes a monthly table that is exact against `ps.v_monthly` (Jan $100, Feb $139, Mar $136, Apr MTD $153). Arm-Y does not surface monthly but instead builds 4-week blocks (W1–W4 $84 → W5–W8 $135 → W9–W12 $142 → W13–W16 $146) — numbers check out. Arm-Y states W16 CVR as "1.12%"; actual is 1.128%, which rounds to 1.13% (arm-X has it right). Minor — not a real factual gap. Arm-Y adds W1–W3 history that arm-X omits, which is useful for framing the Jan baseline.

## Q2 — Quality
arm-X: PASS
arm-Y: PASS
Reasoning: Both are well-structured and readable. Arm-X leads with a crisp TL;DR, separates weekly/monthly/trajectory/OP2/next-steps cleanly, and keeps each section tight. Arm-Y is written more in Richard's voice (first-person, "Yun-Kang hypothesis check", "What I'd say to Brandon/Kate if asked today") and reads like an in-progress working note rather than a neutral analysis — more actionable for Richard personally, less reusable as a shareable artifact. Arm-X is more WBR/Brandon-ready; arm-Y is more 1:1/Yun-Kang-thread-ready.

## Q3 — Contradictions
arm-X: none
arm-Y: none material. W16 CVR rounded to 1.12% instead of 1.13% (actual 1.128%). Not a contradiction of source data, just a rounding choice.

## Q4 — Gaps
arm-X:
- Doesn't name the W15→W16 CVR delta concretely (says "1.32% → 1.13%" in the TL;DR — actually this is there, so this isn't a gap).
- Doesn't check forward-looking W17 partial data — flags it as a next step only.
- Doesn't mention the ABIX/reftag attribution angle or Alex's Italy flag, which is live context in Yun-Kang's draft.
- Cites OP2 as a blended $44 but doesn't explicitly connect the NB-only view to what Richard would commit to verbally.

arm-Y:
- No explicit monthly-level view (Jan/Feb/Mar/Apr MTD). The 4-week blocks proxy for this but aren't calendar-month aligned, which matters for MTD/OP2 storytelling.
- No separate "what to check next" action list; actions are embedded in prose.
- No source citation block (arm-X cites `ps.v_weekly`, `v_monthly`, `v_daily` + dashboard snapshot).
- W17 partial-data caveat missing entirely (arm-X at least flags it).
- Doesn't explicitly name the band (~$122–$142) the way arm-X does, which is the cleanest frame for "is this a real breakout."

## Q5 — Decision utility
Preferred arm: X (for handing to Yun-Kang or using in WBR); Y is stronger as Richard's internal working note
Reasoning: Arm-X is the cleaner artifact — it has the monthly table, the OP2 framing, an explicit "what's worth checking next" list, source citations, and a neutral voice. Richard could copy-paste sections of arm-X into a WBR callout or a reply to Yun-Kang without edits. Arm-Y reads like Richard thinking out loud: strong on diagnosis and on what he'd say verbally, but the 4-week block framing is non-standard for WBR reporting, it lacks the MTD monthly view, and the "What I'd say to Brandon/Kate" closer is great for Richard's prep but would need rewriting before going to anyone else. For Richard's actual stated use case (reply to Yun-Kang, reference in WBR), arm-X wins.

## Overall
Winner: X
Margin: clear (not decisive — arm-Y is better in voice and in naming the hypothesis-check work; arm-X is better in structure, completeness, MTD framing, and re-usability)
