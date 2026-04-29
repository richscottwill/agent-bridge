# MPE Seasonality Research — Per-Market Reference

_Auto-generated from ps.v_weekly Brand registrations history._
_Generated: 2026-04-26_

## Purpose

This document is the reference for understanding each market's seasonal pattern — both what our data says and how it compares to known calendar events.

The MPE Brand trajectory model (see `brand_trajectory.py`) fits a single seasonality curve per market using all available history. This report validates those fits by showing:

1. **What our data says** — lowest/highest weeks from multi-year history
2. **Known seasonal events** — Semana Santa, Ferragosto, Golden Week, etc. — as a sanity check
3. **Anomaly flags** — weeks where the fit looks suspicious (multiplier outside [0.5, 2.0] or high YoY instability)
4. **External benchmark placeholders** — Google Trends, industry reports, WBR/MBR commentary (filled in manually at refresh)

Use this doc when someone asks: _why does the model say W15 is low for MX?_ — answer: because our 3 years of Brand data show W14-W15 at 0.7-0.8× annual mean, AND Semana Santa is a well-known suppression event.

---

## US

**Data coverage**: 172 weeks, 2023-2026
**Annual mean Brand regs/wk**: 2,174

### Notable weeks (from our data)

**Lowest 5 weeks** (seasonal dips):
- W51: **0.73×** annual mean · YoY CV 10%
- W21: **0.85×** annual mean · YoY CV 20%
- W22: **0.89×** annual mean · YoY CV 14%
- W12: **0.90×** annual mean · YoY CV 43%
- W13: **0.90×** annual mean · YoY CV 42%

**Highest 5 weeks** (seasonal peaks):
- W05: **1.19×** annual mean · YoY CV 11%
- W01: **1.18×** annual mean · YoY CV 12%
- W02: **1.14×** annual mean · YoY CV 14%
- W07: **1.10×** annual mean · YoY CV 8%
- W27: **1.10×** annual mean · YoY CV 17%

### Known seasonal events (reference)

- **W01-W02**: Post-holiday slowdown — paid search typically dips 10-15% vs Dec average
- **W13-W15**: Tax deadline spike — business registrations uptick mid-April
- **W27-W32**: Summer soft season — travel + vacation reduces B2B search
- **W48-W52**: Black Friday through year-end — strong paid search lift 20-30%

### External benchmark (to fill in during refresh)

- Google Trends: _compare against `Amazon Business US` search interest over 52w_
- Industry reference: _Search Engine Land B2B search seasonality report_
- Internal: _WBR / MBR seasonality commentary for US market_


---

## CA

**Data coverage**: 172 weeks, 2023-2026
**Annual mean Brand regs/wk**: 356

### Notable weeks (from our data)

**Lowest 5 weeks** (seasonal dips):
- W51: **0.70×** annual mean · YoY CV 22%
- W19: **0.85×** annual mean · YoY CV 4%
- W31: **0.88×** annual mean · YoY CV 4%
- W34: **0.88×** annual mean · YoY CV 16%
- W29: **0.89×** annual mean · YoY CV 3%

**Highest 5 weeks** (seasonal peaks):
- W46: **1.21×** annual mean · YoY CV 13%
- W27: **1.20×** annual mean · YoY CV 16%
- W47: **1.15×** annual mean · YoY CV 19%
- W39: **1.12×** annual mean · YoY CV 6%
- W38: **1.11×** annual mean · YoY CV 10%

### Known seasonal events (reference)

- **W27-W32**: Summer soft season, similar US pattern
- **W48-W52**: Boxing Day + Black Friday echo

### External benchmark (to fill in during refresh)

- Google Trends: _compare against `Amazon Business CA` search interest over 52w_
- Industry reference: _Search Engine Land B2B search seasonality report_
- Internal: _WBR / MBR seasonality commentary for CA market_


---

## UK

**Data coverage**: 172 weeks, 2023-2026
**Annual mean Brand regs/wk**: 464

### Notable weeks (from our data)

**Lowest 5 weeks** (seasonal dips):
- W51: **0.42×** annual mean · YoY CV 0%
- W21: **0.52×** annual mean · YoY CV 75%
- W22: **0.60×** annual mean · YoY CV 66%
- W24: **0.71×** annual mean · YoY CV 47%
- W52: **0.73×** annual mean · YoY CV 16%

**Highest 5 weeks** (seasonal peaks):
- W46: **1.36×** annual mean · YoY CV 9%
- W40: **1.31×** annual mean · YoY CV 1%
- W27: **1.30×** annual mean · YoY CV 27%
- W47: **1.25×** annual mean · YoY CV 12%
- W39: **1.24×** annual mean · YoY CV 8%

### Anomaly flags (investigate before trusting multiplier)

- W21: YoY CV 75% — year-over-year instability
- W22: YoY CV 66% — year-over-year instability
- W23: YoY CV 52% — year-over-year instability
- W51: multiplier 0.42× outside [0.5, 2.0] range

### Known seasonal events (reference)

- **W01**: Return-to-work spike — January is historically UK paid search peak
- **W30-W34**: Summer holidays UK schools out — B2B reduced
- **W48-W52**: Black Friday now strong in UK, ~15-20% lift

### External benchmark (to fill in during refresh)

- Google Trends: _compare against `Amazon Business UK` search interest over 52w_
- Industry reference: _Search Engine Land B2B search seasonality report_
- Internal: _WBR / MBR seasonality commentary for UK market_


---

## DE

**Data coverage**: 172 weeks, 2023-2026
**Annual mean Brand regs/wk**: 611

### Notable weeks (from our data)

**Lowest 5 weeks** (seasonal dips):
- W51: **0.55×** annual mean · YoY CV 23%
- W17: **0.77×** annual mean · YoY CV 28%
- W32: **0.79×** annual mean · YoY CV 21%
- W33: **0.82×** annual mean · YoY CV 29%
- W52: **0.83×** annual mean · YoY CV 16%

**Highest 5 weeks** (seasonal peaks):
- W47: **1.38×** annual mean · YoY CV 37%
- W46: **1.38×** annual mean · YoY CV 24%
- W27: **1.21×** annual mean · YoY CV 32%
- W40: **1.20×** annual mean · YoY CV 23%
- W45: **1.17×** annual mean · YoY CV 21%

### Known seasonal events (reference)

- **W28-W34**: Summer vacation — August especially quiet
- **W48-W52**: Weihnachtsmarkt season — modest Q4 lift

### External benchmark (to fill in during refresh)

- Google Trends: _compare against `Amazon Business DE` search interest over 52w_
- Industry reference: _Search Engine Land B2B search seasonality report_
- Internal: _WBR / MBR seasonality commentary for DE market_


---

## FR

**Data coverage**: 172 weeks, 2023-2026
**Annual mean Brand regs/wk**: 426

### Notable weeks (from our data)

**Lowest 5 weeks** (seasonal dips):
- W51: **0.50×** annual mean · YoY CV 8%
- W32: **0.62×** annual mean · YoY CV 16%
- W33: **0.73×** annual mean · YoY CV 6%
- W31: **0.74×** annual mean · YoY CV 7%
- W52: **0.75×** annual mean · YoY CV 14%

**Highest 5 weeks** (seasonal peaks):
- W47: **1.35×** annual mean · YoY CV 10%
- W46: **1.29×** annual mean · YoY CV 9%
- W10: **1.16×** annual mean · YoY CV 8%
- W40: **1.14×** annual mean · YoY CV 1%
- W44: **1.13×** annual mean · YoY CV 6%

### Anomaly flags (investigate before trusting multiplier)

- W51: multiplier 0.50× outside [0.5, 2.0] range

### Known seasonal events (reference)

- **W31-W34**: August vacances — almost entirely offline
- **W48-W52**: End-of-year moderate uplift

### External benchmark (to fill in during refresh)

- Google Trends: _compare against `Amazon Business FR` search interest over 52w_
- Industry reference: _Search Engine Land B2B search seasonality report_
- Internal: _WBR / MBR seasonality commentary for FR market_


---

## IT

**Data coverage**: 172 weeks, 2023-2026
**Annual mean Brand regs/wk**: 749

### Notable weeks (from our data)

**Lowest 5 weeks** (seasonal dips):
- W32: **0.38×** annual mean · YoY CV 14%
- W51: **0.51×** annual mean · YoY CV 11%
- W33: **0.61×** annual mean · YoY CV 2%
- W31: **0.67×** annual mean · YoY CV 2%
- W52: **0.72×** annual mean · YoY CV 10%

**Highest 5 weeks** (seasonal peaks):
- W46: **1.52×** annual mean · YoY CV 15%
- W47: **1.48×** annual mean · YoY CV 14%
- W40: **1.25×** annual mean · YoY CV 12%
- W05: **1.24×** annual mean · YoY CV 10%
- W48: **1.21×** annual mean · YoY CV 18%

### Anomaly flags (investigate before trusting multiplier)

- W32: multiplier 0.38× outside [0.5, 2.0] range

### Known seasonal events (reference)

- **W32-W34**: Ferragosto (August 15 week) — near-complete shutdown
- **W48-W52**: Holiday season

### External benchmark (to fill in during refresh)

- Google Trends: _compare against `Amazon Business IT` search interest over 52w_
- Industry reference: _Search Engine Land B2B search seasonality report_
- Internal: _WBR / MBR seasonality commentary for IT market_


---

## ES

**Data coverage**: 172 weeks, 2023-2026
**Annual mean Brand regs/wk**: 322

### Notable weeks (from our data)

**Lowest 5 weeks** (seasonal dips):
- W32: **0.51×** annual mean · YoY CV 8%
- W51: **0.62×** annual mean · YoY CV 21%
- W33: **0.65×** annual mean · YoY CV 13%
- W52: **0.66×** annual mean · YoY CV 20%
- W31: **0.70×** annual mean · YoY CV 20%

**Highest 5 weeks** (seasonal peaks):
- W46: **1.51×** annual mean · YoY CV 18%
- W47: **1.48×** annual mean · YoY CV 25%
- W27: **1.25×** annual mean · YoY CV 27%
- W40: **1.22×** annual mean · YoY CV 14%
- W04: **1.21×** annual mean · YoY CV 15%

### Known seasonal events (reference)

- **W32-W34**: Summer holidays southern Spain
- **W48-W52**: Christmas / Three Kings lead-in

### External benchmark (to fill in during refresh)

- Google Trends: _compare against `Amazon Business ES` search interest over 52w_
- Industry reference: _Search Engine Land B2B search seasonality report_
- Internal: _WBR / MBR seasonality commentary for ES market_


---

## JP

**Data coverage**: 172 weeks, 2023-2026
**Annual mean Brand regs/wk**: 565

### Notable weeks (from our data)

**Lowest 5 weeks** (seasonal dips):
- W52: **0.37×** annual mean · YoY CV 37%
- W32: **0.50×** annual mean · YoY CV 21%
- W17: **0.59×** annual mean · YoY CV 14%
- W31: **0.70×** annual mean · YoY CV 16%
- W29: **0.73×** annual mean · YoY CV 18%

**Highest 5 weeks** (seasonal peaks):
- W42: **1.61×** annual mean · YoY CV 43%
- W39: **1.55×** annual mean · YoY CV 38%
- W44: **1.44×** annual mean · YoY CV 43%
- W43: **1.44×** annual mean · YoY CV 37%
- W46: **1.43×** annual mean · YoY CV 8%

### Anomaly flags (investigate before trusting multiplier)

- W35: YoY CV 54% — year-over-year instability
- W52: multiplier 0.37× outside [0.5, 2.0] range

### Known seasonal events (reference)

- **W01-W02**: New Year holiday — January 1-3 extended
- **W18-W21**: Golden Week — early May
- **W32-W34**: Obon (mid-August)

### External benchmark (to fill in during refresh)

- Google Trends: _compare against `Amazon Business JP` search interest over 52w_
- Industry reference: _Search Engine Land B2B search seasonality report_
- Internal: _WBR / MBR seasonality commentary for JP market_


---

## MX

**Data coverage**: 110 weeks, 2024-2026
**Annual mean Brand regs/wk**: 115

### Notable weeks (from our data)

**Lowest 5 weeks** (seasonal dips):
- W30: **0.60×** annual mean · YoY CV 12%
- W37: **0.60×** annual mean · YoY CV 13%
- W16: **0.70×** annual mean · YoY CV 18%
- W33: **0.70×** annual mean · YoY CV 17%
- W36: **0.72×** annual mean · YoY CV 3%

**Highest 5 weeks** (seasonal peaks):
- W15: **1.70×** annual mean · YoY CV 89%
- W07: **1.57×** annual mean · YoY CV 70%
- W14: **1.43×** annual mean · YoY CV 107%
- W10: **1.38×** annual mean · YoY CV 75%
- W42: **1.38×** annual mean · YoY CV 12%

### Anomaly flags (investigate before trusting multiplier)

- W07: YoY CV 70% — year-over-year instability
- W09: YoY CV 58% — year-over-year instability
- W10: YoY CV 75% — year-over-year instability
- W11: YoY CV 85% — year-over-year instability
- W12: YoY CV 77% — year-over-year instability
- W14: YoY CV 107% — year-over-year instability
- W15: YoY CV 89% — year-over-year instability
- W32: YoY CV 76% — year-over-year instability

### Known seasonal events (reference)

- **W14**: Semana Santa (Holy Week) — 30-35% volume suppression
- **W48-W52**: Buen Fin + Navidad — holiday Q4 uplift

### External benchmark (to fill in during refresh)

- Google Trends: _compare against `Amazon Business MX` search interest over 52w_
- Industry reference: _Search Engine Land B2B search seasonality report_
- Internal: _WBR / MBR seasonality commentary for MX market_


---

## AU

**Data coverage**: 45 weeks, 2025-2026
**Annual mean Brand regs/wk**: 130

### Notable weeks (from our data)

**Lowest 5 weeks** (seasonal dips):
- W52: **0.51×** annual mean
- W14: **0.59×** annual mean
- W49: **0.59×** annual mean
- W43: **0.62×** annual mean
- W41: **0.64×** annual mean

**Highest 5 weeks** (seasonal peaks):
- W24: **3.67×** annual mean · YoY CV 43%
- W25: **1.91×** annual mean
- W33: **1.67×** annual mean
- W27: **1.32×** annual mean
- W26: **1.28×** annual mean

### Anomaly flags (investigate before trusting multiplier)

- W24: multiplier 3.67× outside [0.5, 2.0] range

### Known seasonal events (reference)

- **W01-W05**: Southern hemisphere summer — AU schools out through end of January
- **W26-W30**: Mid-year EOFY (End Of Financial Year) ends W26 — business registrations spike
- **W48-W52**: Christmas holidays

### External benchmark (to fill in during refresh)

- Google Trends: _compare against `Amazon Business AU` search interest over 52w_
- Industry reference: _Search Engine Land B2B search seasonality report_
- Internal: _WBR / MBR seasonality commentary for AU market_


---
