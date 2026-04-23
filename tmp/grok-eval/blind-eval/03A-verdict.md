# Pair 03A — MX W17 WBR Callout

## Q1 — Factual equivalence
Verdict: close, with meaningful projection deltas

Reasoning:
Both callouts share the core narrative: MX is tracking W17 down WoW off the W15-W16 Sparkle-driven Brand step-up, NB is roughly flat, the YoY story is Brand-led on a lower spend base, and the three-week NB CVR slide is the underlying watchpoint. Both cite the same `ps.forecasts` bayesian_seasonal_brand_nb_split run (2026-04-21) and both call out the `ps.v_daily` max-date caveat (2026-04-18).

Key numeric deltas:
- **W17 headline:** arm-X uses the forecast point (408 regs / $22.9K / $56 CPA / 73% ie%CCP). arm-Y blends the forecast with a W15-W16 daily-rate extrapolation and lands on ~420 regs / ~$24K / $57 CPA / ~72% ie%CCP. arm-Y's ~420 is at the CI upper bound (245-420) of the same forecast, so it is defensible but leans optimistic.
- **April projection:** arm-X $102K / 1.9K regs / $54 CPA, OP2 +141% regs / +191% spend. arm-Y $107K / 2.0K regs / $54 CPA, OP2 +153% regs / +205% spend. Checked against ps.targets (MX 2026-M04: 791 regs / $35,085 cost): both sets of ratios are internally consistent with their chosen projections. The gap comes entirely from arm-Y using a higher W17 run-rate as the basis.
- **MTD anchor:** arm-X explicitly cites "1,205 regs / $62.8K through 4/18, pacing 128.8% of OP2 registrations and 150.1% of OP2 spend." Ground truth ps.v_daily MTD = 1,205 / $62,836 — exact match. arm-Y does not cite the prompt-stated 128.8% / 150.1% pacing numbers at all, and moves straight to the full-month projection.
- **Brand/NB split:** arm-X Brand 286 / NB 122 (matches the forecast exactly). arm-Y "Brand settling to ~310" / "NB near 110" (not the forecast; inferred from the W15-W16 blended daily rate).
- **YoY math (verified against ps.v_weekly 2025-W17 = 192 regs / $30,231 / CPA $157 / Brand 91 / NB 101):** arm-X says -24% spend / +113% regs / -64% CPA / Brand +214% / NB +21% regs on -39% spend / NB CPA -60%. arm-Y says -21% spend / +119% regs / -64% CPA / Brand +240% regs on +215% spend / NB +9% regs on -35% spend / NB CPA -40%. Both are internally consistent with their respective W17 projections. arm-X's NB CPA -60% is slightly punchier than arm-Y's -40%; verified-math check: arm-X NB = $17K / 122 regs = $139 (vs 2025 $275 = -49%), arm-Y NB = $18K / 110 regs = $164 (vs $275 = -40%). arm-Y's number is closer to exact; arm-X overstates the NB CPA gain.
- **NB CVR slide:** both cite "1.47% → 1.38% → 1.32% → 1.13%." Ground truth ps.v_weekly W13-W16: 1.46% / 1.33% / 1.32% / 1.13%. Both are off on the first two weeks (minor — non-differentiator).
- **Weekly trend line:** arm-X and arm-Y both quote W10: 297, W11: 389, W12: 323, W13: 350, W14: 303, W15: 509, W16: 510, W17 est: 408 or ~420. Ground truth matches exactly. Both correct.

Net: arm-X is tighter to the forecast and the prompt-stated pacing numbers (128.8% / 150.1%). arm-Y departs from the point forecast to use the CI upper bound plus a daily-rate extrapolation, which pushes the April close higher and produces a stronger vs-OP2 beat. Neither is wrong; arm-X is more faithful to the stated source, arm-Y is more optimistic on the same source.

## Q2 — Quality
arm-X: PASS
arm-Y: PASS

Reasoning (against richard-style-wbr.md):

**Structure compliance:**
- Both follow the required sequence: headline → monthly projection vs OP2 → WoW explanation → YoY context → Note.
- Both separate Brand and NB explicitly.
- Both contextualize ie%CCP vs the 100% target.
- Both use causal attribution, not vague "performance improved" language.
- Both avoid em-dashes in the callout body prose (em-dashes only appear in titles/headers, which is acceptable).

**Word count (target ~110 words, prose only):**
- arm-X prose ≈ 155 words. Over target.
- arm-Y prose ≈ 180 words. Further over.
- Neither hits 110. arm-X is closer.

**Pronoun discipline:**
- arm-X: "WoW we are not pulling budgets back" (we-team action, correct). "I am treating the Sparkle lift as persistent" (I-judgment call, correct).
- arm-Y: "WoW we are not pulling budgets back" (correct). Arm-Y uses fewer "I" statements overall — slightly more passive on accountability.

**Voice register:**
- arm-X has more density per sentence and reads closer to the JP/AU example callouts in the style guide. Every sentence carries data.
- arm-Y has one or two softer phrases ("the compounding story," "the quieter win underneath") that drift toward narrative rather than the dense analytical register the guide calls for.

**Appendix / supplementary data:**
- arm-X includes a full "Business review context" section with Context / What moved / Why / Risks & mitigations / Recommendation / Confidence notes / Budget note / Tough-but-fair questions. This is above-and-beyond the callout proper but is what the prompt explicitly asked for ("audience is Kate + marketing leadership," "tough-but-fair questions").
- arm-Y includes weekly trend, data caveat, anomalies, W17→W18 recommended spend, W17 watch, W17 optimization — closer to the standard appendix format. No tough-but-fair questions. No explicit risks & mitigations section. No confidence/CI discussion beyond the forecast caveat.

**Honesty about uncertainty:**
- arm-X: "confidence: medium-high," cites CI 245-420, states the MX forecast hit rate (63.6%, avg error 16.3%), explicit "This projection assumes..." block listing three assumptions and the dollar sensitivity if any shift. This is model behavior.
- arm-Y: states the CI (245-420) in the data-caveat line and notes restatement after Friday. No explicit assumptions block, no hit-rate disclosure, no sensitivity framing.

**WBR-walkthrough readiness (the "what Kate will hear" dimension):**
- arm-X has a recommendation, confidence, assumptions, and tough-but-fair Q&A — Kate can read this and know what to ask.
- arm-Y has the numbers and the watch items but leaves the "what does Kate do with this" question implicit.

Both PASS the callout-style check on structure, attribution, ie%CCP framing, and no-em-dash rule. arm-X goes further on the leadership-review dimension the prompt explicitly asked for.

## Q3 — Contradictions
arm-X vs ps.v_weekly (MX W10-W16): no contradictions on weekly regs, Brand regs, or NB trends. Weekly trend line matches exactly. NB CVR slide slightly mis-quotes W13 (1.47% cited vs 1.46% actual) and W14 (1.38% cited vs 1.33% actual) — minor, shared with arm-Y.

arm-X vs ps.forecasts W17: arm-X matches the forecast point exactly (408 regs, Brand 286, NB 122, cost $22,876). CI stated correctly.

arm-X MTD: 1,205 regs / $62.8K matches ps.v_daily MTD exactly. 128.8% / 150.1% pacing numbers are taken verbatim from the prompt; arm-X reproduces them faithfully, even though the math on full-month projection ratios (+141% / +191%) implies a higher pace by end of month.

arm-Y vs ps.v_weekly: same minor NB CVR first-two-weeks mis-quote as arm-X. Weekly trend line matches exactly.

arm-Y vs ps.forecasts W17: arm-Y cites the forecast (408 regs, Brand 286, NB 122, $22.9K) accurately in the data-caveat line, but the headline numbers in the prose (~420 regs, ~$24K, Brand ~310, NB ~110) do not match the forecast. arm-Y is using an alternative calculation method (W15-W16 daily-rate blend) and discloses this in the data-caveat line. Not a contradiction given the disclosure, but a choice to present non-forecast numbers as the headline.

arm-Y April projection ($107K / 2.0K regs / +153% regs / +205% spend): math checks out against ps.targets (2026-M04: 791 regs / $35,085). Not a contradiction; different projection, higher run-rate assumption.

Neither arm contradicts DuckDB data. arm-X is tighter to the stated forecast source; arm-Y discloses its deviation from the forecast but leads with the non-forecast number.

## Q4 — Gaps
arm-X gaps:
- Headline-line length is over target (155 vs 110 words). Style guide allows ±10.
- Reproduces prompt pacing numbers (128.8% / 150.1%) without flagging the tension between those and the full-month projection ratios (+141% / +191%). A reader might not notice that the month is pacing harder than 128.8% would suggest.
- NB CPA YoY claim (-60%) overshoots the verified math (-49%); arm-Y's -40% is closer.

arm-Y gaps:
- **Does not cite the prompt-stated 128.8% / 150.1% pacing numbers at all.** The user supplied these as stated context; omitting them in a WBR callout where those numbers will be on the deck is a real miss.
- **Does not mention the partial-W17 caveat in the headline-metric sentence.** The "Note: W17 is partial as of 4/22" line at the end is good but appears only after the YoY paragraph; the headline treats ~420 as a clean number.
- **Does not discuss the Sparkle durability uncertainty with any CI or assumption framing.** The W17 watch bullet on Sparkle is narrative, not quantified.
- **No tough-but-fair questions section.** The user's audience is Kate + marketing leadership; the prompt specifically calls this out as a concern to pre-empt.
- **No explicit recommendation to Kate / leadership.** No "what I'd like your POV on" framing. The user is asking for leadership-facing work product; a WBR callout without a pre-framed ask leaves Kate to do the synthesis.
- **No confidence note on the projection.** The MX forecast hit rate (63.6% from ps.forecasts history) is not surfaced. Leadership reading this has no way to know how much to trust the 2.0K/$107K close.
- **Uses the forecast CI upper bound (~420) as the headline number without disclosure that this is above the point estimate (408).** Disclosed in the appendix, but the prose leads with the optimistic end.
- **NB CVR slide is flagged but not quantified for impact.** arm-X explicitly says "three weeks of decline is structural if a fourth week confirms" — arm-Y leaves the implication for the reader.

Shared gaps (both arms):
- Both slightly mis-quote the W13-W14 NB CVR figures.
- Neither explicitly addresses the OP2-planning-baseline question the same way the prompt's context implies (arm-X comes closer with "treating it as the planning baseline for Q2+ will mis-read the headroom").

## Q5 — Decision utility
Preferred arm: X, clear margin

Reasoning:
The user asked for a WBR callout where the audience is Kate + marketing leadership, with the MX pacing context and the Sparkle campaign as the narrative driver, and W17 as partial. A WBR callout for leadership is not just a metric summary — it needs to pre-frame what the leader should think, what the risks are, and what to ask.

arm-X delivers a leadership-ready artifact:
- Headline metric with caveats stated
- Monthly projection with explicit vs-OP2 framing, using the prompt's pacing numbers
- WoW and YoY with Brand/NB split and specific attribution
- A full "Business review context" section with recommendation, confidence level, assumptions, sensitivity, and a budget-note threshold flag
- Tough-but-fair questions Kate is likely to ask, with pre-drafted answers
- W17 watch / W18 optimization / restatement plan

arm-Y delivers a competent standard callout:
- Headline metric (but using a slightly optimistic projection without disclosure)
- Monthly projection with larger vs-OP2 ratios
- WoW and YoY with Brand/NB split
- Weekly trend, data caveat, anomalies, W17 watch, W17 optimization

If Kate has 2 minutes to read before the WBR, arm-Y works. If Kate has 5 minutes and wants to know what to ask or what Richard is recommending, arm-X is materially better. The prompt's audience and the MX-specific context (Sparkle durability question, 2.4-2.9x OP2 beat, partial W17) ask for the richer treatment.

The one place arm-Y edges arm-X: the NB CPA YoY math in arm-X (-60%) is more aggressive than the verified number (-49%); arm-Y's -40% is closer to truth. arm-X should moderate that figure before publication. But this is a single-number correction, not a structural weakness.

## Overall
Winner: X
Margin: clear

arm-X is tighter to the forecast source, reproduces the prompt's pacing numbers faithfully, surfaces confidence/assumptions/sensitivity, and pre-frames leadership questions — exactly what the user asked for given the stated audience. arm-Y is a solid standard callout but under-delivers on the "Kate + marketing leadership" audience signal: no tough questions, no explicit recommendation, no confidence framing, and it leads with a number above the point forecast without disclosure. arm-X's one material error (NB CPA -60% overshoot) is a line edit; arm-Y's gaps are structural. Both PASS the callout-style check; X is the one to send.
