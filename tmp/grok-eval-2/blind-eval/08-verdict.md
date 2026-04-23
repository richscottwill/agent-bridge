# Blind Verdict — 08 Creative Fatigue

**Scenario:** Richard asks about an MX Brand campaign (MX-Brand-Polaris-Sparkle-01) running since mid-March on same creative. 21-day CTR monotonic decline 4.2% → 2.5%, CVR stable 8.1–8.3%. Fatigue concern?

**Evaluator sees:** ARM-X and ARM-Y only. No knowledge of which is control/treatment.

---

## Q1 — Factual equivalence

**Fatigue diagnosis:** Both arms reach the same conclusion — this is creative fatigue, high confidence. Both invoke the CTR-down / CVR-stable signature as the load-bearing evidence. Both correctly rule out targeting decay, landing-page issues, auction/competitor changes.

**Recommended action:** Both say refresh this week, structured as a variant test rather than a pure swap. Both preserve the incumbent as a control arm. ARM-X says 2–3 variants with incumbent held at 10–20% traffic. ARM-Y says 2–3 alternates at 70/30 split with specific day-7/14 read thresholds (CTR ≥4.0%, CVR within ±0.5pp). Same shape, ARM-Y slightly more prescriptive on thresholds, ARM-X slightly more prescriptive on control traffic %.

**Confidence:** Both land at "high" / ~90%. ARM-X states "~90%" explicitly. ARM-Y says "high confidence" and decomposes sign/magnitude/generalizability per the protocol. Functionally equivalent.

**Equivalent on the core call.** Differences are in framing and supporting moves, not the diagnosis.

---

## Q2 — Quality: Test Analysis Protocol application

Both hit all four checks (incrementality + confidence + next action + creative fatigue signal). Comparing execution:

**Incrementality:**
- ARM-X: "47% more clicks/regs at same impression level" + caveat that $ sizing needs spend pull. Explicitly labels it "not a true counterfactual" — a thoughtful honest hedge.
- ARM-Y: "40% fewer conversions at constant spend" via conversions-per-impression (0.344% → 0.205%). Cleaner single number. Also flags the spend × impression gap.
- Roughly equivalent. ARM-X's 47% and ARM-Y's 40% describe the same gap from different reference points (week-1 baseline vs. end-to-end). Both are directionally right.

**Confidence decomposition:**
- ARM-X: sign / magnitude / generalizability breakdown, each with reasoning. Flags "do not generalize the 5–6 week refresh cadence without frequency data."
- ARM-Y: same three-part decomposition, plus cross-check recommendation (compare to other fresh-creative MX campaigns).
- Tie. Both apply the protocol correctly.

**Next action specificity:**
- ARM-X: (1) pull frequency data, (2) queue 2–3 variants, (3) structure as test with 10–20% control arm, (4) propose standing fatigue tripwire (CTR drop >15% vs 7-day trailing with stable CVR).
- ARM-Y: (1) pull 2–3 creatives (check ABMA), (2) 70/30 split, (3) specific day-7/14 read thresholds (CTR ≥4.0%, CVR ±0.5pp), (4) hints at scanner in daily brief.
- ARM-X is more concrete on the systemic tripwire rule. ARM-Y is more concrete on the go/no-go decision criteria for the refresh test itself. Both actionable.

**Creative fatigue signal:**
- Both explicitly RULE IN. ARM-Y lists four sub-criteria (monotonic 14+ days, CVR stable, linear not cliff, campaign long enough to saturate) with checkboxes — slightly more pedagogical.

**Additional quality factors:**
- ARM-X provides a **clean alternative-hypothesis elimination table** (6 hypotheses × expected CTR/CVR × fits?). This is the clearest diagnostic logic presentation across either arm.
- ARM-Y provides a **simulated scanner tool output** that frames the answer as if a tool produced it. This is either a nice mental model or a bit of theater depending on how you read it — it's marked "simulated" so it's not dishonest, but the scanner doesn't actually exist. Could mislead a less careful reader.
- ARM-Y adds an explicit **Soul-check** against How-I-Build principles (3, 7, 8) and a **Five Levels tie-in** (L2, L3). This is tailored to Richard's system.
- ARM-Y adds a **"tough but fair questions"** section — anticipating Brandon/Kate pushback. Useful prep.
- ARM-X adds a **systemic follow-up** ("sweep other MX Brand campaigns >4 weeks") that is genuinely the L3 move, though labels it only briefly.

**Call:** ARM-X wins on diagnostic rigor (the hypothesis table is the strongest single artifact across both). ARM-Y wins on decision-ready packaging (soul-check, Five Levels, tough questions, specific go/no-go thresholds). **Net edge to ARM-Y for decision utility; ARM-X has the tightest analytical core.**

---

## Q3 — Contradictions / misreads

**ARM-X:**
- States "47% more clicks … 4.1 / 2.79 − 1 = 47%." Math checks out (1.47).
- Says CTR peak-to-trough is −42% (4.3 → 2.5). Correct (−41.9%).
- Says "monotonic with only two minor noise reversals (day 3, day 15)." Data shows: day 3 = 4.3 (up from 4.1), day 7 = 3.9 (up from 3.8), day 15 = 3.2 (up from 3.1). That's three reversals, not two. Minor miscount, doesn't affect the diagnosis.

**ARM-Y:**
- "conv_per_impression: 0.344% → 0.205% (−40.5%)." CTR × CVR: 4.2% × 8.2% = 0.3444%; 2.5% × 8.2% = 0.205%. Math checks out.
- "consecutive_decline: 7 days (threshold 14+ met across window)." Slightly muddled — what does "7 days" mean if the threshold is 14+? Actual longest monotonic streak in the data is longer than 7 (days 8–14 alone are 7 straight declines, and 15–21 are 6 straight declines). The phrasing is imprecise but the conclusion (decline is sustained) is right.
- "monotone downward with only one up-tick (day 7→8 flat, day 14 +0.1pp)." Actually: day 3 (+0.2), day 7 (+0.1 if you count 3.8→3.9), day 15 (+0.1 if 3.1→3.2). The characterization understates the noise. Still directionally fine.
- States creative_age_days ~38 "live since ~2026-03-15." Consistent with "mid-March" and 21-day window ending ~today.
- The **simulated scanner output** is labeled simulated, but a reader skimming could mistake it for a real tool run. Mild risk.

**Neither misreads the diagnostic logic.** Both handle the CTR-down/CVR-stable inference correctly. Both have minor data-description slips that don't change the call.

**Edge: ARM-X is cleaner on the data specifics; ARM-Y has slightly more scattered imprecisions but labels the scanner output as simulated.**

---

## Q4 — Gaps

Checking against the four signals the rubric calls out:

| Signal | ARM-X | ARM-Y |
|---|---|---|
| CTR-down / CVR-stable signature | ✅ Load-bearing argument, explicit table | ✅ Explicit, four-sub-criteria checklist |
| Alternative-hypothesis ruling | ✅ Full 6-row table with expected CTR/CVR | ✅ Called out inline (seasonality, auction, targeting) but no structured table |
| Refresh-as-test framing | ✅ "Structure as a test, not a swap" — 10–20% control arm | ✅ 70/30 split, day-7/14 read thresholds |
| L2 / L3 tie-in | ⚠️ Mentions "L2 test readout" and "L3 move" in passing without labeling the Five Levels explicitly | ✅ Dedicated "Five Levels tie-in" section, L2 + L3 explicit |

**ARM-X gap:** L2/L3 tie-in is implicit and brief. A reader who doesn't know the Five Levels framework would miss it.

**ARM-Y gap:** No structured alternative-hypothesis table — relies on inline assertions. Less rigorous for a skeptical reader.

**Neither misses the CTR-down/CVR-stable signature** (the most important one). Both frame the refresh as a test.

**Other gaps common to both:**
- Neither pulled actual data from `ps.v_daily` despite the Data & Context Routing rule saying "Query first, ask second." Both caveat this (ARM-X more explicitly), but it's a live MX campaign — either arm could have run the query. ARM-Y fabricates a tool result, ARM-X says "pull today."
- Neither flags that frequency / reach data lives platform-side and may require a separate request to the search engine platform team or Yun-Kang's access.
- Neither sizes the $ impact. Both caveat, but Richard will need that before any stakeholder conversation.

---

## Q5 — Decision utility

**Richard's next moves:**
1. Tell Yun-Kang: "Refresh Polaris-Sparkle-01 this week, run as variant test, hold incumbent as control."
2. Ask ABMA (or internal team) to pull 2–3 alternate creatives.
3. Document readout when the refresh test reads.
4. Decide whether to build a standing fatigue monitor across markets.

**ARM-X gives him:**
- A crisp hypothesis-elimination table he could paste directly into a Slack to Yun-Kang or into an L2 test readout.
- A clear tripwire rule (>15% CTR decline vs 7-day trailing + stable CVR → refresh) that could become a standing policy.
- The systemic sweep idea (check other MX Brand creatives >4 weeks) is the right L3 question.

**ARM-Y gives him:**
- A go/no-go decision protocol for the refresh test itself (day-7/14 thresholds) — specific enough to hand to Yun-Kang without further instruction.
- "Tough but fair questions" that prep him for the Brandon 1:1 or any skip-level.
- A soul-check and Five Levels framing that connects the tactical move to his strategic priorities.
- A scanner/tool framing that hints at the L3 automation play explicitly.

**Which would Richard actually use?** ARM-Y is more immediately actionable as a communication artifact — the go/no-go thresholds, the tough questions, the soul-check. ARM-X is better as the **analytical backbone** — if Richard had to defend the diagnosis in writing, the hypothesis table is the single best piece of evidence across both arms.

Honest call: **ARM-Y wins narrowly on decision utility.** The 70/30 split with day-7/14 thresholds is ready to ship to Yun-Kang as-is. The tough-questions section is Richard-style Brandon-prep. ARM-X's hypothesis table is stronger analysis but less "ship-ready."

If Richard only reads one: ARM-Y, because it closes the loop on "what do I do Monday morning?" ARM-X is the doc he'd want to attach when someone challenges the diagnosis.

---

## Overall

- **Q1 Equivalence:** Essentially equivalent on diagnosis, action, and confidence.
- **Q2 Quality:** ARM-X has the tightest diagnostic core (hypothesis table). ARM-Y has better decision packaging (soul-check, Five Levels, tough questions, go/no-go thresholds). Net edge **ARM-Y** for protocol application because it more explicitly names each of the four Test Analysis Protocol checks as headers.
- **Q3 Contradictions:** Neither misreads the diagnostic logic. Both have minor imprecisions in characterizing the data (ARM-X miscounts reversals; ARM-Y muddles "consecutive decline"). **ARM-X slightly cleaner on data specifics.**
- **Q4 Gaps:** ARM-X misses explicit L2/L3 framing. ARM-Y misses the structured alternative-hypothesis table. **ARM-Y closer to complete on the rubric's four called-out signals** (L2/L3 tie-in is explicit).
- **Q5 Decision utility:** **ARM-Y wins.** More ship-ready for Yun-Kang / ABMA / Brandon.

**Winner: ARM-Y, narrowly.** Both are high-quality outputs. ARM-Y is better tailored to Richard's system (soul-check, Five Levels) and more decision-ready. ARM-X has the single strongest analytical artifact (the hypothesis-elimination table) and is cleaner on data description. If these were merged — ARM-X's hypothesis table inserted into ARM-Y's framework — that would be the best-in-class output.

**Caveat on the scanner framing in ARM-Y:** The "simulated" scanner output is a stylistic choice that works as a mental model but could be confusing in a real workflow where tools either exist or don't. Marginal concern; labeling it "simulated" mitigates.
