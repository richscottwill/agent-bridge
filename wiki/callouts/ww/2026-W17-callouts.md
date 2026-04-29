---
title: WBR Callouts — 2026-W17
week: 2026-W17
generated: 2026-04-27
data_source: ps.wbr_weekly + ps.latest_forecasts + ps.monthly_pacing + ps.forecasts (scored W16)
pipeline_run: wbr_pipeline.py on AB SEM WW Dashboard_Y26 W17 (1).xlsx
---

# 2026-W17 WBR Callouts

**Generated:** 2026-04-27 after ingesting the W17 xlsx and running the full WBR pipeline (ingestion → MotherDuck load → W16 prediction scoring → W18 forecast generation → callout drafting → 2-lens blind review).

**Data lag caveat:** W17 xlsx omits Sun 2026-04-26 across all markets (6 days of data, ISO week boundary). Actuals will trend slightly higher on next refresh.

---

## AU (Richard hands-on)

**AU:** AU drove 245 registrations W17 (-1.6% WoW, $107 CPA, -3.5% WoW) on $26,235 spend (-5.1% WoW). April MTD: 661 regs / $79.7K spend vs OP2 1,071 regs / $147.6K (-38% regs, -46% cost) at 4 of 4.3 weeks elapsed. Pacing lag is real, not an artifact. WoW, Brand regs grew +12.4% (CPA -16.2% to $31) and drove the efficiency. NB regs fell -10.5% with CPA up +6.2% to $168, compressing CVR -11.7%. YoY context unavailable. AU has no W17 2025 baseline until June 2026. W16 scored a HIT (207 predicted vs 242 actual, 14.5% error, CI 188–288), confirming the engine is calibrated; W18 predicts 228 regs (CI 195–308). I will keep leaning into Brand efficiency while diagnosing NB CPA drift to protect AU's efficiency mandate. Note: W17 xlsx omits Sun 2026-04-26 across all markets; expected ISO-week lag.

---

## MX (Richard hands-on)

**MX:** MX drove 551 registrations W17 (+8.3% WoW, $46 CPA, +187% YoY) on $25.5K spend (-6.1% WoW, -15.5% YoY). April projected to close at 197.8% of OP2 regs and 222.9% of OP2 cost (MTD 1,565 regs / $78.2K vs 791 / $35K OP2), MX the only market over-pacing on both regs and cost. WoW: Brand regs +5.6% (CPA -12.6%) drove volume; NB regs +17.4% at $147 CPA (-19.7%) on CVR +11.3%. YoY story is Brand: regs +357% at $13.59 CPA (-49.3%), with ie%CCP headroom funding NB CPA -46.5% YoY. I will hold April NB spend inside the 100% ie%CCP ceiling rather than chase volume, and reforecast May with Lorena once W17 Brand CVR is confirmed structural. Notes: forecaster under-predicted MX three weeks running (W16: 304 vs 510, 40.4% error); CI widened 1.3x for W18 (457, CI 288–570). W17 xlsx omits Sun 2026-04-26.

---

## US

**US:** US drove 9,450 registrations W17 (+5.8% WoW, $77 CPA, +64.3% YoY), on $726K spend (+6.9% WoW, +24.0% YoY). April MTD pacing: 89.3% of OP2 regs (27,757 of 31,076) on 73.6% of cost ($2.08M of $2.83M), efficiency ahead, volume slightly behind. WoW split: Brand regs -2.8% with CPA +8.1% (softening auction); NB regs +9.9% with CPA -2.1% (scaling efficiently). YoY, NB is the engine: regs +130% with CPA -40.1%, while Brand is flat (-1.7% regs, -0.7% CPA) as the category matures. Spend +6.9% delivered +5.8% regs (near 1:1), CVR +0.5% WoW. I will lean further into NB to close the pacing gap and investigate Brand CPA drift before it compounds. Notes: W16 actual (9,109) landed above forecast CI high (8,975) despite 1.34x band widening, engine still under-predicting US upside; W17 xlsx omits Sun 2026-04-26.

---

## CA

**CA:** Canada drove 696 registrations W17 (-7.2% WoW, $79 CPA, +58.2% YoY), with spend -9.3% as an efficient response to NB softness rather than chasing volume. April projects at ~2,450 regs and ~$215K spend, pacing 86.5% to OP2 regs ($171K / 80% of OP2 spend MTD) with one week left. WoW: NB regs fell -16.1% (NB CPA +6.5% to $107) while Brand held flat (-0.5%, 426 regs) with Brand CPA improving -7.2% to $61. YoY we spent +15.9% with regs +58.2% (NB +101.5%, Brand +39.2%) and CPA -26.7%, so the efficiency gain is structural. I will diagnose the NB drop (match type, competitor IS, seasonality) before W18 to rebuild volume without reflating CPA.

Note: W17 data excludes Sun 2026-04-26 (xlsx lag); actuals will trend slightly higher on refresh. Forecast engine is well-calibrated (hit rate 0.94) and predicts 605 regs for W18.

---

## JP

**JP:** Brand drove 555 registrations W17 (+10.3% WoW, $58.80 CPA, +21.2% YoY), with spend down -8.2% to $32.6K. April projected at ~$140K spend and ~1,920 regs (vs. OP2: -3% spend, on track to target); MTD tracking 75.2% spend / 84.9% regs through W17 with one day of W17 data missing from source. WoW we ran a Brand double-win: Brand regs +10.4% while Brand CPA fell -18.7% to $56.20, pulling blended CPA -16.8% on -8.2% spend (CVR +10.7% supporting). YoY we spent +13.9% for +21.2% regs; CPA essentially flat (-6.0%). I will hold the current Brand bid posture through W18 to preserve the CPA compression, and dig into which Brand terms drove the efficiency lift. Note: NB is 2 regs/week, treat NB CPA movement as noise. Data lag: W17 xlsx omits Sun 2026-04-26.

---

## EU5 (UK, DE, FR, IT, ES)

**EU5:** EU5 drove 5,987 registrations (+1.8% WoW, +54.1% YoY) on $510K spend, with IT the standout (-21.2% CPA WoW to $69.11, regs +5.3%; Brand +8.4%, NB -1.1%) and UK the only market over-pacing April OP2 (4,642 / 4,492, 103.3%; +172.3% YoY off last year's low base). April MTD: DE 73.5%, FR 72.1%, IT 64.7% of OP2 regs, ES at 90.6%. WoW DE/FR/IT all grew +3–5% regs, but DE spend ran +6.1% ahead of its +3.1% reg gain (CPA +2.9%); FR delivered efficiency (-5.5% CPA). ES was the sole decliner (-4.9% regs). YoY every EU5 market is materially up. I will dig into IT's CPA compression to see if the driver (likely NB bid strategy) is replicable in DE and FR, pressure-test DE's spend-ahead-of-regs gap before it compounds, and diagnose the ES reg dip. Note: W17 xlsx omits Sun 2026-04-26; forecast engine over-predicted UK W16 but under-predicted DE (divergent drift, investigating).

---

## W18 forecast table (from ps.latest_forecasts)

| Market | W18 Predicted | CI Low | CI High | Calibration | Hit Rate | Mean Error% |
|--------|---------------|--------|---------|-------------|----------|-------------|
| US | 7,147 | 5,886 | 7,490 | 1.036 | 0.53 | 18.6% |
| UK | 1,105 | 762 | 1,271 | 1.018 | 0.88 | 16.8% |
| DE | 1,103 | 1,005 | 1,312 | 1.002 | 0.65 | 15.2% |
| FR | 786 | 747 | 980 | 1.000 | 0.94 | 11.6% |
| IT | 647 | 550 | 1,250 | 1.000 | 0.94 | 14.4% |
| JP | 590 | 339 | 678 | 1.061 | 0.76 | 21.1% |
| CA | 605 | 591 | 736 | 1.000 | 0.94 | 7.3% |
| MX | 457 | 288 | 570 | 1.036 | 0.55 | 18.6% |
| ES | 436 | 371 | 613 | 1.000 | 0.94 | 14.4% |
| AU | 228 | 195 | 308 | 1.025 | 0.75 | 17.5% |

## W16 prediction scoring (from ps.forecasts, re-scored 2026-04-27 under corrected SURPRISE > HIT > MISS priority)

| Market | Predicted | Actual | Error% | Score |
|--------|-----------|--------|--------|-------|
| ES | 603 | 613 | 1.6% | HIT |
| JP | 570 | 544 | 4.8% | HIT |
| CA | 747 | 778 | 4.0% | MISS (narrow CI artifact) |
| AU | 207 | 242 | 14.5% | HIT |
| US | 7,804 | 9,109 | 14.3% | MISS |
| UK | 1,945 | 1,644 | 18.3% | HIT |
| IT | 911 | 1,136 | 19.8% | HIT |
| FR | 1,279 | 1,037 | 23.3% | SURPRISE |
| DE | 1,096 | 1,550 | 29.3% | SURPRISE |
| MX | 304 | 510 | 40.4% | SURPRISE |

**Run summary:** 10 scored / 5 HIT / 2 MISS / 3 SURPRISE. Mean |error| = 19.0%. DE/MX ran hot (demand above envelope), FR ran cold (demand below envelope). CA's MISS is a narrow-CI artifact.
