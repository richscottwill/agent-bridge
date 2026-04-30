# Polaris Brand LP — QA Feedback Consolidation

**Owner:** Richard Williams (designated by Brandon Munday, 4/29)
**Status:** DRAFT — consolidating all open items before MCS authoring cutoff
**Cutoff for additional feedback:** Fri 5/1 5pm PT

---

## Purpose

Brandon designated Richard single point of contact for all Polaris Brand LP QA coordination (ab-paid-search-global 4/29). This doc is the single canonical feedback file — no more segmented feedback in Asana comments, no more fragmented Slack threads. Feedback goes here, this doc goes to MCS.

---

## Open QA items (by owner)

### Alex VanDerStuyf (Andes) — items 3, 4, 5
- [ ] Item 3: _[fill in from Asana + 4/24 thread]_
- [ ] Item 4: _[fill in]_
- [ ] Item 5: _[fill in]_
- **Status:** Authoring finalizing 4/29

### Vijeth Shetty (Andes) — items 1, 2, 6
- [ ] Item 1: _[fill in]_
- [ ] Item 2: _[fill in]_
- [ ] Item 6: _[fill in]_
- **Status:** Authoring finalizing 4/29

### Yun-Kang Chu — Polaris Br-pages QA (DE/FR weblab path)
- [ ] Subheadlines — _[fill in specific concern]_
- [ ] Ref tag overrides — _[fill in]_
- [ ] Page-load — _[fill in]_
- **Status:** Open, waiting for Richard consolidation per Brandon 4/29

### Andrew Wirtz — copy question
- [ ] _[pull from ab-paid-search-global 4/29 thread "Andrews question on copy"]_
- **Status:** Brandon tagged Richard 4/29 to reply

### AU/MX alt-measurement (Dwayne blocker)
- Context: Dwayne confirmed 4/24 that weblab setup requires control also leading to MCS. AU/MX lead direct to reg start — weblab path blocked.
- **Decision:** AU/MX split to non-weblab measurement path. Richard designing alt-measurement framework (Asana 1214330104198712, due 5/6).
- **Item:** Scope the reftag-based measurement framework for this doc (see §Test Design below).

---

## Timeline (locked 4/30)

| Date | Milestone | Owner |
|---|---|---|
| 4/29 | Weblab authoring finalized | Alex + Vijeth |
| 5/1 5pm PT | **Additional QA feedback cutoff (Richard)** | Richard |
| 5/4 | Weblab setup in test markets (DE, FR) | MCS + Alex |
| 5/6 | AU/MX non-weblab test design v1 shipped | Richard (Asana 1214330104198712) |
| 5/6-5/8 | Dial-up window | MCS + Alex |
| 5/12 | Early signal read (if weblab on) | Richard + Yun |

---

## Communication plan

1. **This doc = canonical.** No Asana comments, no new Slack threads for QA. All QA feedback lands here by 5/1 5pm.
2. **MCS email (send today):** To Alex VanDerStuyf + MCS team. Subject: "Polaris Brand LP — consolidated QA feedback + timeline (AU/MX non-weblab split)". Link to this doc. Timeline locked. Cutoff stated.
3. **ab-paid-search-global post:** 3-line summary with link. Tag Yun, Andrew, Brandon. Reaffirms Richard as single POC.
4. **Recurring Alex sync:** Weekly, 30 min, Alex defers to Richard on PS team priorities. First sync: week of 5/4.

---

## Test Design — AU/MX alt-measurement (placeholder for 5/6 doc)

**Hypothesis:** Polaris Brand LP lifts post-click CVR from LP → reg-start AND improves reg-start → purchase conversion vs current MCS brand LP.

**Control:** Current MCS brand LP (leads direct to reg start)
**Treatment:** Polaris Brand LP (same reg-start hand-off, new LP)

**Measurement (non-weblab):**
- Primary: CVR from LP visit → reg-start, by reftag prefix (PS attribution), pre/post swap, ≥14 days each side
- Secondary: reg-start → purchase CVR, same window
- Tertiary: spend efficiency (NB CPA, Brand CPA)

**Sample size:** TBD — calculate from AU/MX weekly reg baseline. At W17 AU ran 245 regs/week, MX 551 regs/week. 4 weeks each side → ~1000 AU / ~2200 MX regs → MDE ~8-10% relative CVR lift at 80% power.

**Risk table:** _[fill in on 5/6]_

---

## Meta

- **Why this doc:** Brandon 4/29 DM: "create a file with the QA feedback. That way everyone can see their information is included." This doc = execution of that.
- **Why this matters:** Brandon flagged three responsiveness hits on 4/29 within 50 min. Centralized QA is the visible trust-rebuilding mechanism.
- **Where to find it:** `shared/wiki/staging/polaris-brand-lp-qa-feedback-consolidation.md` (pre-publish). Will route through wiki pipeline after cutoff.

---

_Last updated: 2026-04-30 06:10 PT — stub created by kiro-server. Richard fills in by 1pm PT._
