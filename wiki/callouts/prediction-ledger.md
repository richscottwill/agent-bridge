# Prediction Ledger

Append-only log of weekly predictions. Each entry records what was predicted, when, and from what source week's data. When actuals arrive, score the prediction inline (HIT/MISS/SURPRISE) and record the error.

Format: One block per source week. Weekly predictions target the next week. Monthly predictions target the current month-end. Score column is filled when actuals arrive.

---

## Source: W15 (predicted 2026-04-13)

### W16 Predictions (registrations)

| Market | Predicted | CI Low | CI High | Brand | NB | Actual | Error% | Score |
|--------|-----------|--------|---------|-------|-----|--------|--------|-------|
| US | 8,040 | 7,395 | 8,685 | 2,277 | 5,763 | — | — | — |
| CA | 661 | 599 | 721 | 420 | 241 | — | — | — |
| UK | 1,460 | 1,350 | 1,570 | 454 | 1,006 | — | — | — |
| DE | 986 | 699 | 1,274 | 538 | 448 | — | — | — |
| FR | 1,035 | 922 | 1,148 | 430 | 605 | — | — | — |
| IT | 1,180 | 1,019 | 1,340 | 764 | 416 | — | — | — |
| ES | 580 | 502 | 658 | 317 | 263 | — | — | — |
| JP | 604 | 520 | 684 | 598 | 6 | — | — | — |
| AU | 222 | 150 | 295 | 102 | 120 | — | — | — |
| MX | 370 | 273 | 466 | 244 | 126 | — | — | — |

### April 2026 Month-End Predictions (registrations)

| Market | Predicted | CI Low | CI High | Actual | Error% | Score |
|--------|-----------|--------|---------|--------|--------|-------|
| US | 33,269 | 29,306 | 37,232 | — | — | — |
| CA | 2,690 | 2,319 | 3,061 | — | — | — |
| UK | 5,626 | 4,949 | 6,303 | — | — | — |
| DE | 3,608 | 1,844 | 5,372 | — | — | — |
| FR | 3,865 | 3,169 | 4,564 | — | — | — |
| IT | 4,475 | 3,490 | 5,460 | — | — | — |
| ES | 2,114 | 1,632 | 2,592 | — | — | — |
| JP | 2,390 | 1,886 | 2,879 | — | — | — |
| AU | 886 | 530 | 1,240 | — | — | — |
| MX | 1,565 | 971 | 2,160 | — | — | — |

### Q2 2026 Predictions (registrations)

| Market | Predicted | CI Low | CI High | Actual | Error% | Score |
|--------|-----------|--------|---------|--------|--------|-------|
| US | 115,440 | 94,259 | 136,619 | — | — | — |
| CA | 8,947 | 6,959 | 10,936 | — | — | — |
| UK | 18,143 | 14,522 | 21,763 | — | — | — |
| DE | 10,232 | 2,223 | 19,664 | — | — | — |
| FR | 12,003 | 8,281 | 15,732 | — | — | — |
| IT | 13,633 | 8,371 | 18,891 | — | — | — |
| ES | 6,499 | 3,931 | 9,060 | — | — | — |
| JP | 8,771 | 6,129 | 11,362 | — | — | — |
| AU | 806 | 272 | 2,289 | — | — | — |
| MX | 5,551 | 2,373 | 8,732 | — | — | — |

### Scoring Rules
- HIT: Actual within CI (70% credible interval)
- MISS: Actual outside CI but within 20% of predicted
- SURPRISE: Actual >20% off predicted value
- Error% = |predicted - actual| / actual × 100
