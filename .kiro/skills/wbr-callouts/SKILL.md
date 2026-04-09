---
name: wbr-callouts
description: "Full WBR callout pipeline for weekly business review. Covers all 10 markets: AU, MX, US, CA, JP, UK, DE, FR, IT, ES. Triggers on WBR, callout, weekly callout, market callout."
---

# WBR Callouts Pipeline

## Instructions

Sequential pipeline — follow each step in order:

1. **Load principles** — Read `callout-principles.md` from this skill's `references/` directory. These principles govern tone, structure, and quality thresholds for all callouts.

2. **Determine ISO week number** — Calculate the current ISO week number. This is used for file naming and callout headers.

3. **Run market-analyst for each market** — Invoke the market-analyst agent for each of the 10 markets (AU, MX, US, CA, JP, UK, DE, FR, IT, ES). The analyst reviews performance data, identifies notable movements, and assigns a confidence score (0-100%) to each potential callout. Every market gets a callout — there is no confidence gate. Even flat/uneventful markets have trends worth noting (streaks, YoY context, ie%CCP movement, NB vs Brand mix shifts).

4. **Run callout-writer for ALL markets** — Write a callout for every market. The writer follows the callout principles and Richard's writing style. EU5 consolidation rule: UK, DE, FR, IT, ES are written as a single combined "EU5" callout (max 150 words total for the group, not per market). Highlight the 1-2 most notable EU5 markets and summarize the rest. Non-EU5 markets (AU, MX, US, CA, JP) each get their own individual callout (max 150 words each).

5. **Blind review (8/10 gate, two lenses)** — Each callout is scored through two independent lenses, then combined. The bar is 8/10 average across both lenses. Score blind (strip market labels before scoring if possible).

   ### Lens 1: Richard's Voice (scored against richard-style-wbr.md)

   Does this callout read like Richard wrote it? Load `richard-style-wbr.md` as the rubric.

   1. **Attribution** — Is every WoW/YoY movement tied to a specific cause?
      - 10: Every movement has a named driver (CVR, clicks, bid strategy, seasonal, budget change). "Brand regs +19% due to exact match impressions +40%."
      - 7: Most movements attributed, one vague claim
      - 4: Multiple "improved/declined" without cause
      - 1: No causal attribution anywhere

   2. **Structure** — Does it follow the WBR callout pattern? Headline metric → monthly projection → WoW explanation → YoY context → Notes.
      - 10: All sections present in correct order. Headline uses the "[Market]: [Market] drove [X] registrations..." format.
      - 7: Structure present but one section out of order or missing
      - 4: Partial structure, reads like freeform analysis
      - 1: No recognizable callout structure

   3. **Voice fidelity** — Dense, analytical. "We" for team actions, "I" for personal decisions. Parenthetical data. Specific forward-looking actions ("I will continue to test..."). Brand/NB always separated. Asterisked deep-dives. "Note:" lines for external factors.
      - 10: Indistinguishable from Richard's actual callouts in the Pre-WBR Quip doc
      - 7: Right structure but slightly off (too formal, missing "I will" actions, or missing parenthetical data density)
      - 4: Generic analyst voice
      - 1: Wrong register entirely

   4. **Economy** — Every word earns its place. Under 150-word limit. No restating the headline in the body.
      - 10: Tight. No filler. Every sentence carries data or insight.
      - 7: One redundant phrase
      - 4: Significant padding
      - 1: Could be cut by 30%+

   ### Lens 2: Brandon's Read (scored as Brandon Munday reading the callout)

   Brandon reads these callouts as Richard's L7 manager. She's looking for: strategic framing (not just status), clear "so what," proactive next steps, and whether she'd need to ask a follow-up question. She values financial stewardship awareness, dependency mapping, and evidence that Richard owns the narrative rather than just reporting numbers. She does NOT want to read a callout and then have to ask "what are you doing about it?"

   1. **So-what clarity** — Can Brandon read this and immediately understand whether the market needs attention or is on track? Does the callout answer "should I worry about this?" without her having to ask?
      - 10: One read, zero follow-up questions. The narrative tells Brandon exactly what matters and why.
      - 7: Clear but one element requires inference (e.g., CPA rose but no indication whether it's a concern or expected)
      - 4: Data-heavy but no synthesis — Brandon has to do the interpretation herself
      - 1: Just numbers, no narrative

   2. **Proactive ownership** — Does Richard show he's ahead of the problem? "I will investigate," "I have adjusted," "I will continue to test" — not just "performance declined." Brandon's #1 growth area for Richard: visibility and proactive communication. A callout that reports a problem without stating what Richard is doing about it fails this dimension.
      - 10: Every concern has a stated next step or action. Richard is clearly driving, not observing.
      - 7: Most concerns addressed, one left hanging
      - 4: Reports problems without actions — reads like a dashboard, not a manager's update
      - 1: Pure observation, no ownership signal

   3. **Accuracy & completeness** — Do the numbers hold up? Is ie%CCP contextualized vs target? Is YoY included? Are data lag caveats present? Brandon will spot-check numbers against the dashboard — anything wrong erodes trust.
      - 10: Every number verified, all context elements present (YoY, ie%CCP vs target, monthly projection, data lag warnings)
      - 7: One context element missing but numbers are correct
      - 4: A percentage is wrong or a key context element (ie%CCP, YoY) is absent
      - 1: Multiple factual errors

   4. **Strategic signal** — Does the callout connect to something bigger when warranted? Budget implications, competitive dynamics, test results, cross-market patterns. Brandon doesn't want every callout to be a strategy memo — but when spend is up 15% with regs down 12%, she wants to know Richard sees the efficiency concern. When a market is declining 3 weeks straight, she wants to know it's on the radar.
      - 10: Flags strategic implications naturally without over-reaching. Connects to budget, competitive, or cross-market context where relevant.
      - 7: Mentions the implication but doesn't fully connect it
      - 4: Misses an obvious strategic signal (e.g., 3-week decline with no acknowledgment)
      - 1: No strategic awareness — pure tactical reporting

   ### Combined scoring

   Compute the average across all 8 dimensions (4 from each lens). The final score is the arithmetic mean of all 8.

   ### Review output format

   For each callout unit (AU, MX, US, CA, JP, EU5):

   ```
   ## [Market] Review

   ### Lens 1: Richard's Voice
   | Dimension    | Score | Note |
   |-------------|-------|------|
   | Attribution  | X/10  | ...  |
   | Structure    | X/10  | ...  |
   | Voice        | X/10  | ...  |
   | Economy      | X/10  | ...  |
   | *Lens avg*   | *X.X* | |

   ### Lens 2: Brandon's Read
   | Dimension    | Score | Note |
   |-------------|-------|------|
   | So-what      | X/10  | ...  |
   | Ownership    | X/10  | ...  |
   | Accuracy     | X/10  | ...  |
   | Strategic    | X/10  | ...  |
   | *Lens avg*   | *X.X* | |

   **Combined: X.X/10 → PASS / REVISE**
   ```

   ### Decision logic

   - **PASS (combined avg >= 8.0):** Ship it.
   - **REVISE (combined avg < 8.0, first attempt):** Provide specific edit instructions (quote text, provide replacement). Rewrite and re-score. One revision pass.
   - **ESCALATE (combined avg < 8.0 after revision):** Flag for Richard. Don't iterate further.

   Floor rule: no dimension may score below 6, even if the combined average is >= 8. A callout with Ownership=5 and everything else at 9 still gets REVISE.

6. **Cross-callout consistency check** — After scoring all units individually, read all callouts together and check for contradictions:
   - Do WW-level numbers implied across callouts add up? (e.g., if US says spend +15% and EU5 says spend flat, the WW summary shouldn't claim spend declined)
   - Are data lag caveats consistent? (if US/CA/MX all flag data lag, the pattern should be acknowledged, not treated as market-specific)
   - Do cross-market references align? (if CA says "mirrors the US pattern," verify the US callout actually describes that pattern)
   - Are ie%CCP readings internally consistent with the WW dashboard data?
   - Flag any contradictions as `consistency_flags` in the score log. If a contradiction is found, REVISE the affected callout(s) before shipping.

7. **Log scores to DuckDB** — After all reviews (including any revision passes), write every score to `ps.callout_scores`. One row per callout unit per attempt. This is non-negotiable — every pipeline run produces score data.

   ```sql
   INSERT INTO ps.callout_scores (
       iso_week, callout_unit, attempt,
       l1_attribution, l1_structure, l1_voice, l1_economy, l1_avg,
       l2_sowhat, l2_ownership, l2_accuracy, l2_strategic, l2_avg,
       combined_avg, verdict, revision_notes, consistency_flags, word_count
   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
   ```

   Calibration views available:
   - `ps.callout_calibration` — per-market averages across all weeks, weakest dimensions, first-draft vs revision scores
   - `ps.callout_trend` — weekly averages, first-draft pass rate, weakest dimension per week

   Over time, these views reveal: which markets consistently need revision, which dimensions are weakest (rubric calibration signal), whether first-draft quality is improving, and whether the 8/10 bar needs adjustment.

8. **Run validate-callout.sh** — Execute `scripts/validate-callout.sh` to check word count compliance (max 150 words per callout unit — individual market or EU5 block). Fix any violations.

9. **Score last week's predictions** — Before generating new projections, score the previous week's forecasts against this week's actuals. Query `ps.forecasts` for predictions targeting the current week, compare against `ps.performance` actuals, and update `actual_value`, `error_pct`, `scored`, and `score` (HIT if within CI, MISS if outside, SURPRISE if >20% off). This closes the feedback loop.

   ```sql
   -- Example: score W14 predictions now that W14 actuals are in ps.performance
   UPDATE ps.forecasts f SET
       actual_value = p.registrations,
       error_pct = ROUND(ABS(f.predicted_value - p.registrations) / p.registrations * 100, 1),
       scored = true,
       score = CASE
           WHEN p.registrations BETWEEN f.confidence_low AND f.confidence_high THEN 'HIT'
           WHEN ABS(f.predicted_value - p.registrations) / p.registrations > 0.20 THEN 'SURPRISE'
           ELSE 'MISS'
       END
   FROM ps.performance p
   WHERE f.target_period = '2026-W14'
     AND f.metric_name = 'registrations'
     AND p.market = f.market AND p.period_type = 'weekly' AND p.period_key = '2026-W14'
     AND f.scored = false;
   ```

10. **Generate projections** — Run `python3 ~/shared/tools/prediction/project.py --week {current_week}`. This generates next-week, current-month, and current-quarter projections for all 10 markets using Brand/NB split models with ie%CCP constraints. Writes to `ps.forecasts` with revision tracking. Outputs a projection table to append to the callout document (outside word count).

    Market strategies:
    - AU: efficiency (hit registration OP2 at lowest CPA, no ie%CCP)
    - MX: ie%CCP bound (100% target, maximize regs within that envelope)
    - JP: brand-dominant (NB negligible, weight Brand heavily)
    - US/CA/UK/DE/FR/IT/ES: balanced (50-65% ie%CCP normal range)

11. **Sync data to MotherDuck** — After the ingester runs, load the new week's data into `ps.performance` (wide table). The ingester writes local files; this step pushes to MotherDuck. Run:

    ```python
    python3 -c "exec(open('shared/tools/prediction/project.py').read()); ..."
    ```

    Or use the MCP DuckDB server to INSERT directly. The key tables that must be current:
    - `ps.performance` — weekly/daily/monthly actuals (wide format, one row per market×period)
    - `ps.forecasts` — predictions with scoring
    - `ps.forecast_revisions` — drift tracking
    - `ps.callout_scores` — callout quality scores
    - `ps.targets` — OP2 spend targets

12. **Present AU/MX highlights** — Surface AU and MX callouts first (Richard's hands-on markets), then US, CA, JP, then EU5 consolidated. Append the projection tables after the callouts.

## Notes

- The callout pipeline is sequential: analyst → writer → reviewer → consistency → log → validate → score predictions → project → sync → present. Don't skip steps.
- Load the relevant writing style guide (richard-style-wbr.md) before any writing.
- Callouts additionally require callout-principles.md from references/.
- The 8/10 bar matches the wiki pipeline. We ship 8s. We don't ship 7s.
- Two lenses ensure the callout works for both audiences: Richard's voice (the writing) and Brandon's read (the substance). A callout can nail Richard's style but fail Brandon's "so what?" test, or vice versa. Both must pass.
- Score logging is mandatory. Every pipeline run writes to `ps.callout_scores`. This is how the rubric calibrates — if Ownership consistently scores lowest, that's a signal to either improve the writing or recalibrate the dimension anchors.
- The consistency check catches contradictions that per-unit scoring misses. A callout can score 9/10 individually but still contradict another callout's narrative.
- Prediction scoring closes the feedback loop: each week's actuals score last week's forecasts. Over time, `ps.forecast_accuracy` shows which markets/segments the model gets right and where it drifts.
- The projection engine is at `~/shared/tools/prediction/project.py`. It reads from `ps.performance` and writes to `ps.forecasts`.

## End-to-End Weekly Sequence

When Richard drops a new xlsx (e.g., W15):

1. Run ingester: `python3 ~/shared/tools/dashboard-ingester/ingest.py <xlsx_path>`
   → Generates callout drafts, data briefs, JSON extract
2. Load data to MotherDuck: push weekly/daily/monthly/ie%CCP into `ps.performance`
3. Score last week's predictions: update `ps.forecasts` with actuals from the new data
4. Generate new projections: `python3 ~/shared/tools/prediction/project.py --week 2026-W15`
5. Trigger WBR callout skill → runs the full pipeline (steps 1-12 above)

Steps 1-4 should eventually be automated into a single ingestion hook. For now they're manual.
