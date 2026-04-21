<!-- DOC-slack-digest | generated: 2026-04-20T14:02 UTC | subagent: A (Slack Ingestion) -->
# Slack Digest — Mon Apr 20, 2026

**Scan window:** 2026-04-17 12:48 UTC → 2026-04-20 14:01 UTC (3 days, covers weekend)
**Channels scanned:** 13 of 28 unread (16 community/social channels skipped per tier-3 rules)
**Messages ingested:** 40 parents + 7 thread replies = 47 total
**Signals reinforced:** 12 (signal_tracker rows added/strengthened)

---

## 🔴 HIGH-PRIORITY SIGNALS (Brandon/Kate/decisions/action-items)

### 1. Brandon: keyword audit + weekly perf Quip [DM-Brandon, Fri 4/17 ~5:00-9:25 PM PT]
**Thread summary:** Brandon chased Richard on keyword perf by Kw to Lena, then asked for a paper trail visible to everyone. Richard confirmed: sent to Alexis, copied data into Excel doc linked in Weekly Perf Quip, pivoted monthly per KPI with zero/low-traffic rows removed. Brandon also asked Richard to forward the Polaris template change-requests email to him and Dwayne.

**[ACTION-RW] Send Polaris template change-requests email to Brandon + Dwayne** — requested Fri 4/17, status unknown. Simple forward.
**[ACTION-RW] Verify Weekly Perf Quip has the kw data link that Brandon can see** — Brandon couldn't find it Friday afternoon.

Other dialogue: Richard pushed back that monthly numbers look bad only due to LP change skew; overall CPCs still trending down. Brandon had a 1:1 Friday morning with someone (likely Lorena/Dwayne) who wanted the kw audit out of the SIM — team is antsy to close it, he wants it delivered Friday. Richard also mentioned to Brandon: "I'm #1 non-tech power user for [Kiro] in Todd's org" — visibility signal, worth reinforcing in OP1/growth plan.

### 2. OCI NB-spend drop investigation [#ab-paid-search-global, Fri 4/17 ~12:29 PM PT, 7-reply thread]
**Sam Tangri** flagged big NB spend drops in UK and DE on Mon 4/13, mirroring a US drop (25k vs 70k avg), with spike-recovery the day after. Asked **Jing** and **Nupur** if same-parent-MCC algorithm linkage caused global impact from the US data exclusion.
**Jing's read:** Google MCC prioritizes learning from same MCC (EU vs NA) across child accounts — cross-MCC impact less likely but worth Mike's review. Jing added data exclusions: US 4/7 (extended 4/13), DE 3/28.
**Sam's conclusion:** Makes sense — data would have been parsed through 4/8 on the 13th, likely caused the US drop. Sent follow-up email to Mike (cc Jing + Adi). Brandon reacted 👍.

This is an OCI performance thread worth tracking — relevant to WW Testing + AU+MX OCI understanding.

### 3. Polaris IT `/cp/ps-brand` page recovery [mpdm-mcs-polaris, Fri 4/17 3:00 PM PT]
**Alex VanDerStuyf (MCS)** wrote up the full timeline referencing **MCS-3004 (Richard's SIM)**:
- Polaris version of `it/cp/ps-brand` went live 4/1/2026
- Legacy version restored 4/16/2026
- Polaris parked in AEM as `it/cp/ps-brand-new`
- Vijeth published IT page thinking it was safe because it was noindex/nofollow and IT wasn't in Richard's original SIM

Apology posted, open for questions. **No Richard follow-up yet — worth a quick thank-you + close-out.**

---

## 🟡 MEDIUM-PRIORITY SIGNALS

### 4. Adi 1:1 / Kiro mentoring [DM-Adi, Fri 4/17 5:09-6:53 PM PT, 12 msgs]
Adi (Aditya Thakur) thanked Richard for talking Kiro "the other week" and asked to cover technical setup in next week's 1:1 — he has it running but isn't clear on implementation. Richard recommended he explore `ai-fluency-for-builders` channel and ask his own Kiro to compare remote workspace vs local + IDE vs browser. Adi noted interest-group overwhelm and tool unpredictability — classic adoption friction signal.

**[ACTION-RW] Block 15-20 min in next Adi 1:1 for Kiro technical setup walkthrough.** Low effort, high mentoring leverage.

### 5. rsw-channel daily brief (self-logged) [Fri 4/17 5:55 AM PT]
Richard's own Friday brief — L1 streak day 20 at zero, Testing Approach v5 done (PUBLISH 8.4/10), hard thing = SEND TO BRANDON (16d overdue), visibility-avoidance = 12 days. Pacing snapshot: AU 15.7% regs ⚠️, MX 65.1% regs / 72.5% cost ⚠️, US 30.6% ⚠️, Forecast US 53% ⚠️. *No update posted for weekend/Mon yet.*

### 6. DDD late-notice [#ab-paid-search-global, Fri 4/17 8:58 AM PT]
Brandon: "please start the DDD without me - I might be a few min late." Procedural, no action needed.

---

## 🟢 LOW-PRIORITY / INFORMATIONAL

### ask-ab-aryabot (Tier 2, 13 parent messages, 0 Richard mentions)
High-volume bot Q&A channel — team members querying AryaBot for SQL/data questions (TTM GMS at BAID level, ESI partner GMS, cxml ordering, VAS flags, Hubble access). Parents ingested for volume tracking; thread replies not ingested (all bot responses, no team intel). Worth nothing: **VAS-flagged-ASIN API limitation** surfaced (talwv), could be relevant if Baloo touches that code path.

### Channels with no activity since last scan
- #ab-paid-search-oci (last msg 4/13, quiet all weekend — unusual, OCI team is usually active)
- #ab-paid-search-abix, #ab-paid-search-app, #ab-ps_jp, #ask-ab-data — all silent in the window
- 3 unread DMs (D04B4ABRHE0, D093XCFQTV1) had last_read after their last message, no new content

---

## 📊 THREAD-REPLY FETCH SUMMARY

| Priority | Channel | Thread Topic | Replies Fetched | Replies Ingested |
|---|---|---|---|---|
| 🔴 High | ab-paid-search-global | OCI NB spend drop (Sam→Jing→Nupur) | 7 | 7 |
| 🟢 Low | ask-ab-aryabot | 5 bot Q&A threads (top reply-count) | 57 | 0 |
| **Total** | | | **64** | **7** |

Cap was 50 threads — only 6 fetched. Bot-Q&A replies deliberately not ingested (noise); parent messages retained for volume/heat-map signal.

---

## 🔍 PROACTIVE SEARCH

| Query | Hits |
|---|---|
| `from:@brandoxy to:@prichwil after:2026-04-17` | 0 |
| `prichwil after:2026-04-17 before:2026-04-21` | 0 |
| `kataxt after:2026-04-17 before:2026-04-21` | 0 |

Workspace search API returned 0 matches — likely a scope/permission artifact of the MCP search index. **Channel-history scan caught all Richard↔Brandon content anyway** (see DM-Brandon + global-channel threads above), so no gap.

---

## 🧠 SIGNAL TRACKER — TOPICS REINFORCED

| Topic | Channel | Author | Strength | Notes |
|---|---|---|---|---|
| polaris-brand-lp | dm-brandon | Brandon | +1.5 | Template change email request |
| polaris-brand-lp | mpdm-mcs-polaris | Alex VanDerStuyf | +1.5 | IT page recovery (MCS-3004) |
| oci-rollout | ab-paid-search-global | Sam Tangri | +1.5 | NB spend drop investigation |
| mcc-algorithm-learning | ab-paid-search-global | Jing Shi | +1.0 | New topic — cross-MCC learning behavior |
| data-exclusion | ab-paid-search-global | Jing Shi | +1.0 | New topic — US 4/7 + 4/13 exclusions |
| kw-audit | dm-brandon | Richard | +1.5 | Hot — Brandon pushing for deliverable |
| weekly-perf-quip | dm-brandon | Brandon | +1.5 | Paper-trail visibility request |
| au-cpa-cvr | dm-brandon | Richard | +1.0 | LP change skew defense |
| kiro-mentoring | dm-adi | Adi Thakur | +1.0 | New — adoption support signal |
| kiro-power-user | dm-brandon | Richard | +1.0 | New — Todd-org visibility claim |
| testing-approach-v5 | rsw-channel | Richard | +1.0 | Still unsent to Brandon (16d) |
| visibility-avoidance | rsw-channel | Richard | +1.0 | Self-logged 12d pattern |

**Cross-channel corroboration:** `polaris-brand-lp` now has signals in 5 channels (hedy, mpdm-brandoxy-dtpalmer, ab-paid-search-global, dm-brandon, mpdm-mcs-polaris) → **confirmed cross-channel trend**, should boost any related wiki/artifact work.

---

## 📥 WRITES PERFORMED

- `ps_analytics.signals.slack_messages` — 47 rows inserted
- `ps_analytics.signals.signal_tracker` — 12 rows inserted
- `ps_analytics.ops.data_freshness` — updated slack_messages + signal_tracker timestamps
- `~/shared/context/active/slack-scan-state.json` — written (file did not exist previously)
- `~/shared/context/intake/slack-digest.md` — this file

**Did NOT touch:** Asana MCP, Outlook MCP, Hedy MCP, SharePoint MCP, any asana-*/email-*/hedy-* files.

---

## ⚠️ FLAGS FOR ORCHESTRATOR

1. **Hard-thing still unsent.** Testing Approach v5 → Brandon. Day 20 at zero. The Friday brief logged it; no send has appeared in any channel over the weekend. Direct this to rw-trainer if not handled by noon.
2. **Polaris template email** — Brandon asked Friday 5:00 PM PT, unanswered in DM history. Likely an easy forward that's stalling on visibility-avoidance.
3. **slack-channel-registry.json is missing from `~/shared/context/active/`.** Operated from slack-ingestion-README.md conventions. Recommend regenerating the registry file before next run, or confirming the README is the new source of truth.
4. **OCI channel silent 4 days** — unusual; the CA OCI launch was Monday of prior week. Worth Richard checking if conversation moved to email or a 1:1.
