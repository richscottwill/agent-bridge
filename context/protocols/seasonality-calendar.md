# Seasonality Calendar — PS Markets (2026)

Used by the state file engine (Step 2E) and callout pipeline to automatically flag holiday impacts in weekly narratives. When a reporting week overlaps with a holiday period, the agent MUST mention it in the State of Business section and discount the WoW/YoY comparison accordingly.

## How to Use

1. Before generating any weekly narrative, check this calendar for the reporting week
2. If a holiday falls within the week, lead the narrative with the holiday context
3. Discount WoW comparisons: "W14 -33% WoW is holiday-driven (Semana Santa), not structural"
4. Flag YoY comparisons as unreliable if the holiday falls on different weeks across years
5. Note the expected impact level to calibrate the narrative tone

## Impact Levels

- **HIGH (>20% suppression):** Multi-day national holidays, business closures.
- **MEDIUM (5-20% suppression):** Single-day holidays or cultural events.
- **LOW (<5% suppression):** Minor observances.
- **POSITIVE:** Shopping events that boost traffic/registrations.

Impact percentages below are **measured from actual ps.metrics data** (2025-2026), not estimates. Format: `measured_impact% (source: YYYY event)`. Where two years of data exist, the average is shown. The agent uses these as multipliers when projecting holiday weeks.

---

## MX — Mexico

| Date | Holiday | Measured Impact | Source | Notes |
|---|---|---|---|---|
| Jan 1 | Año Nuevo (New Year's Day) | -14.8% | Christmas 2025 W52 | MX has lowest Christmas impact of all markets. |
| Feb 2 | Día de la Constitución (observed) | ~-3% | Est. (no clean data) | Monday holiday. Minimal. |
| Mar 16 | Natalicio de Benito Juárez (observed) | -16% WoW | 2026 W12 (W12 vs W11) | Monday holiday. W12 2026: 326 vs 390 = -16.4%. Includes CVR normalization from W11 spike + holiday. Pure holiday effect est. -5 to -8%. |
| Mar 29–Apr 5 | Semana Santa / Easter | -32.6% WoW | 2026 W14 vs W13 | Mexico's largest holiday. Good Friday + Sábado de Gloria near-zero. Strongest Easter impact of any market. |
| May 1 | Día del Trabajo (Labor Day) | ~-5% | Est. from EU Labour Day pattern | Single day. |
| May 25–Jun 7 | Hot Sale (est.) | +10-20% | Est. (no prior data) | Mexico's largest online shopping event. |
| Jul 13-14 | Prime Day (est.) | +10-15% | Est. | Amazon event. |
| Sep 16 | Día de la Independencia | ~-5% | Est. | Single day. |
| Nov 16 | Día de la Revolución (observed) | ~-2% | Est. | Monday holiday. Minimal. |
| Nov 27 | Buen Fin (est. start) | +15-25% | Est. | Mexico's BFCM equivalent. |
| Dec 25 | Navidad | -14.8% | 2025 W52 vs W51 | Lowest Christmas impact — MX B2B less affected than EU/AU. |

## AU — Australia

| Date | Holiday | Measured Impact | Source | Notes |
|---|---|---|---|---|
| Jan 1 | New Year's Day | -39.8% | Christmas 2025 W52 (combined Xmas+NY) | AU has 3rd-highest Christmas impact. |
| Jan 26 | Australia Day | ~-8% | Est. | Monday long weekend. |
| Apr 3-6 | Easter (Good Fri–Easter Mon) | -18.3% WoW | 2026 W14 vs W13 | 4-day weekend. Only 1 year of data (launched Jun 2025). |
| Apr 25 | Anzac Day | ~-3% | Est. (Saturday in 2026) | Reduced impact when on weekend. |
| Jun 30 | EOFY | +10-15% | Est. | B2B purchasing spike. |
| Jul 13-14 | Prime Day (est.) | +10-15% | Est. | Amazon event. |
| Nov 27 | Black Friday | +10-15% | Est. | Growing in AU. |
| Dec 25-26 | Christmas + Boxing Day | -39.8% | 2025 W52 vs W51 | Multi-day shutdown. |

## WW — Worldwide Testing Markets

Covers all 10 PS markets. The WW Testing state file needs to know which markets are affected each week. Organized by market, then aggregated into WW-level impact events.

### US

| Date | Holiday | Measured Impact | Source | Notes |
|---|---|---|---|---|
| Jan 1 | New Year's Day | -11.0% | 2025 W52 vs W51 | Lowest Christmas impact — US B2B recovers fastest. |
| Jan 19 | MLK Day | ~-2% | Est. | Monday. Federal holiday. Minimal B2B impact. |
| Feb 16 | Presidents' Day | ~-2% | Est. | Monday. Federal holiday. |
| May 25 | Memorial Day | -3.9% | 2025 W22 vs W21 | Monday long weekend. Modest impact. |
| Jul 3 | Independence Day (observed) | ~-5% | Est. | Friday. Long weekend. |
| Jul 13-14 | Prime Day (est.) | +15-25% | Est. | Amazon event. Largest positive US event. |
| Sep 7 | Labor Day | ~-4% | Est. (similar to Memorial Day) | Monday long weekend. |
| Nov 26 | Thanksgiving | -4.9% | 2025 W48 vs W47 | Thu-Fri. Lower than expected — US B2B is resilient. |
| Nov 27–30 | BFCM | +20-30% | Est. | Largest positive event. |
| Dec 24–Jan 1 | Christmas/New Year | -11.0% | 2025 W52 vs W51 | US has lowest Christmas suppression of all markets. |

### CA — Canada

| Date | Holiday | Measured Impact | Source | Notes |
|---|---|---|---|---|
| Jan 1 | New Year's Day | -27.0% | 2025 W52 vs W51 | Higher than US — CA B2B shuts down more completely. |
| Apr 3 | Good Friday | -16.7% avg | 2025 (-15.6%) + 2026 (-17.8%) | Single day but strong impact. |
| May 18 | Victoria Day | ~-5% | Est. | Monday long weekend. |
| Jul 1 | Canada Day | ~-5% | Est. | Wednesday in 2026. |
| Jul 13-14 | Prime Day (est.) | +10-15% | Est. | Amazon event. |
| Sep 7 | Labour Day | ~-4% | Est. | Monday long weekend. |
| Oct 12 | Thanksgiving (CA) | ~-5% | Est. | Monday long weekend. |
| Nov 27–30 | BFCM | +15-20% | Est. | Growing in CA. |
| Dec 25-26 | Christmas + Boxing Day | -27.0% | 2025 W52 vs W51 | Multi-day shutdown. |

### UK

| Date | Holiday | Measured Impact | Source | Notes |
|---|---|---|---|---|
| Jan 1 | New Year's Day | -43.3% | 2025 W52 vs W51 | Highest Christmas impact of all markets. |
| Apr 3-6 | Easter (Good Fri–Easter Mon) | -2.7% avg | 2025 (-4.7%) + 2026 (-0.7%) | Surprisingly low — OCI + ad copy gains may offset. |
| May 4 | Early May Bank Holiday | ~-3% | Est. | Monday long weekend. |
| May 25 | Spring Bank Holiday | ~-3% | Est. | Monday long weekend. |
| Jul 13-14 | Prime Day (est.) | +15-20% | Est. | Amazon event. |
| Aug 31 | Summer Bank Holiday | ~-3% | Est. | Monday long weekend. |
| Nov 27–30 | BFCM | +15-25% | Est. | Major in UK. |
| Dec 25-26 | Christmas + Boxing Day | -43.3% | 2025 W52 vs W51 | Highest suppression — UK B2B shuts down completely. |

### DE — Germany

| Date | Holiday | Measured Impact | Source | Notes |
|---|---|---|---|---|
| Jan 1 | Neujahrstag | -35.4% | 2025 W52 vs W51 | Strong Christmas shutdown. |
| Apr 3-6 | Easter (Karfreitag–Ostermontag) | -12.2% | 2025 W16 vs W15 | 2026 data unreliable (W13 data lag recovery distorts W14). |
| May 1 | Tag der Arbeit (Labour Day) | ~-5% | Est. | Single day. |
| May 14 | Christi Himmelfahrt (Ascension) | ~-8% | Est. | Thursday. Many take Friday off → 4-day weekend. |
| May 25 | Pfingstmontag (Whit Monday) | ~-3% | Est. | Monday long weekend. |
| Nov 27–30 | BFCM | +10-15% | Est. | Growing in DE. |
| Dec 24-26 | Weihnachten | -35.4% | 2025 W52 vs W51 | Multi-day shutdown. |

### FR — France

| Date | Holiday | Measured Impact | Source | Notes |
|---|---|---|---|---|
| Jan 1 | Jour de l'An | -38.1% | 2025 W52 vs W51 | Strong Christmas shutdown. |
| Apr 6 | Lundi de Pâques (Easter Monday) | -3.1% avg | 2025 (-5.0%) + 2026 (-1.2%) | Low impact — Easter Monday only. |
| May 1 | Fête du Travail | ~-8% | Est. | Strongest French single-day holiday. |
| May 8 | Victoire 1945 | ~-3% | Est. | Single day. |
| May 14 | Ascension | ~-8% | Est. | Thursday. "Pont" (bridge day). |
| Jul 14 | Fête Nationale | ~-5% | Est. | Tuesday in 2026. |
| Aug 1-31 | Summer holidays | ~-5% per week | Est. | Staggered. Reduced B2B all month. |
| Nov 27–30 | BFCM | +10-15% | Est. | Growing in FR. |
| Dec 25 | Noël | -38.1% | 2025 W52 vs W51 | Multi-day shutdown. |

### IT — Italy

| Date | Holiday | Measured Impact | Source | Notes |
|---|---|---|---|---|
| Jan 1 | Capodanno | -40.1% | 2025 W52 vs W51 | 2nd-highest Christmas impact. |
| Jan 6 | Epifania | ~-5% | Est. | Tuesday in 2026. |
| Apr 6 | Lunedì dell'Angelo (Easter Monday) | -4.0% avg | 2025 (-7.0%) + 2026 (-1.0%) | Low impact — Easter Monday only. |
| May 1 | Festa del Lavoro | ~-5% | Est. | Friday in 2026. Long weekend. |
| Aug 15 | Ferragosto | ~-15% | Est. | Peak summer. Many businesses closed 1-2 weeks. |
| Nov 27–30 | BFCM | +10-15% | Est. | Growing in IT. |
| Dec 25-26 | Natale + Santo Stefano | -40.1% | 2025 W52 vs W51 | Multi-day shutdown. |

### ES — Spain

| Date | Holiday | Measured Impact | Source | Notes |
|---|---|---|---|---|
| Jan 1 | Año Nuevo | -26.9% | 2025 W52 vs W51 | Moderate Christmas impact. |
| Jan 6 | Día de Reyes | ~-5% | Est. | Tuesday in 2026. |
| Apr 2-3 | Jueves/Viernes Santo | -21.4% avg | 2025 (-17.8%) + 2026 (-25.0%) | Strongest Easter impact in EU5. |
| May 1 | Día del Trabajador | ~-5% | Est. | Friday in 2026. Long weekend. |
| Aug 15 | Asunción de la Virgen | ~-8% | Est. | Saturday in 2026. Reduced impact. |
| Nov 27–30 | BFCM | +10-15% | Est. | Growing in ES. |
| Dec 25 | Navidad | -26.9% | 2025 W52 vs W51 | Multi-day shutdown. |

### JP — Japan

| Date | Holiday | Measured Impact | Source | Notes |
|---|---|---|---|---|
| Jan 1-3 | Shōgatsu (New Year) | -64.7% | 2026 W1 vs 2025 W52 | Strongest single-holiday impact in any market. Near-zero for 3+ days. |
| Mar 31 | Fiscal Year End | ~±10% | Est. | Can spike (budget flush) or suppress (year-end freeze). |
| Apr 29–May 5 | Golden Week | -18.6% | 2025 W18 vs W17 | Multi-day. Significant but less than Shōgatsu. |
| Jul 13-14 | Prime Day (est.) | +10-15% | Est. | Amazon event. |
| Aug 13-16 | Obon | ~-10% | Est. | Cultural holiday. Reduced business activity. |
| Sep 21-23 | Silver Week | ~-5% | Est. | Multi-day. Moderate. |
| Nov 27 | Black Friday | ~+5% | Est. | Growing but not major in JP. |
| Dec 25-31 | Year-end | -32.3% | 2025 W52 vs W51 | Business shutdown. |

### WW Aggregate Impact Events

Measured from ps.metrics. WW impact estimated as weighted average (US ~50% of WW regs).

| Date | Event | Measured Market Impacts | Est. WW Impact | Source |
|---|---|---|---|---|
| Jan 1-3 | New Year / Shōgatsu | JP -64.7%, UK -43.3%, IT -40.1%, AU -39.8%, FR -38.1%, DE -35.4%, CA -27.0%, ES -26.9%, MX -14.8%, US -11.0% | -20 to -25% | 2025 W52 + 2026 W1 |
| Mar 29–Apr 6 | Easter / Semana Santa | MX -32.6%, ES -21.4%, AU -18.3%, CA -16.7%, DE -12.2%, US -8.6%, IT -4.0%, FR -3.1%, UK -2.7% | -10 to -15% | 2025+2026 avg |
| Apr 29–May 5 | Golden Week + Labour Day | JP -18.6%, EU5 ~-5% each, MX ~-5% | -5 to -8% | 2025 W18 + est. |
| May 25 | Memorial Day (US) + Spring Bank (UK) | US -3.9%, UK ~-3% | -3 to -4% | 2025 W22 |
| Jul 13-14 | Prime Day | All markets positive | +10 to +15% | Est. |
| Aug 1-31 | Summer (EU) + Obon (JP) | IT ~-15% (Ferragosto), FR/DE/ES ~-5%, JP ~-10% | -3 to -5% per week | Est. |
| Nov 26 | Thanksgiving (US) | US -4.9% | -3 to -4% | 2025 W48 |
| Nov 27–30 | BFCM | All markets positive | +15 to +25% | Est. |
| Dec 24–Jan 1 | Christmas/New Year | UK -43.3%, IT -40.1%, AU -39.8%, FR -38.1%, DE -35.4%, JP -32.3%, CA -27.0%, ES -26.9%, MX -14.8%, US -11.0% | -25 to -35% | 2025 W52 |

---

*This calendar is loaded by the state file engine during Step 2E. The agent checks the reporting week against this calendar before generating any narrative. Holiday context is mandatory — missing a holiday attribution (like the W14 Semana Santa miss) produces incorrect causal analysis.*

*Impact percentages are measured from actual ps.metrics data where available (tagged with source year/week). Entries marked "Est." have no clean historical measurement and will be updated after the first occurrence in 2026. The agent should use measured impacts as multipliers when projecting holiday weeks and discount WoW/YoY comparisons by the measured factor.*

*Update cadence: Annually (January) for dates. After each holiday occurrence, update the measured impact with actual data. Event dates (Prime Day, Hot Sale, BFCM) updated when announced.*

*Data source: `SELECT market, period_key, actual_value FROM ps.metrics WHERE period_type='weekly' AND metric_name='registrations'`*
