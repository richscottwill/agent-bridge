# Organ Changes Log

## 2026-04-03

**File:** `shared/context/body/gut.md`
**Change:** Removed "or when total body approaches 30,000w safety limit" from the Compression Protocol trigger conditions. Compression now triggers only on Bayesian priors (COMPRESS posterior_mean > 0.7, n > 5), not on total body word count.
**Flags:**
- ⚠️ **Karpathy gate:** gut.md is gated — edit was NOT routed through karpathy agent. May be unauthorized.
- ⚠️ **Cross-organ inconsistency:** `nervous-system.md` line 58 still tracks "Total body words ≤30,000w" as a target metric. If the 30,000w limit is no longer a compression trigger, nervous-system.md should be updated to reflect the new policy (or the metric should be reframed as informational rather than a hard limit).
