# Topic Sentry — 2026-04-29

_Scan window: last 24 hours (2026-04-28 13:30Z → 2026-04-29 13:30Z). Watchlist: 16 active topics. Hits: 18 unique sources across 13 topics._

**Five Levels coverage (by hit count):** L1: 0 · L2: 34 · L3: 3 · L4: 2 · L5: 0 · operational: 12

_First run of topic-sentry.md on disk — no 7-day baseline yet. L1 and L5 are silent today; check again tomorrow before flagging as sustained silence._

_Slack channel_section filter: registry v3.1 excludes only "Channels" section from topic_sentry scans, but `signals.slack_messages` has no `channel_section` column — scan covered all 8 channels with messages in window. Impact: may include a small number of hits that would be excluded under the registry's sweep-only rule for the "Channels" section. Flagged for future schema fix._

---

## P1 — must surface

### mx-registration-funnel (0 hits)
_Why: MX reg funnel changes shift CPA math and Sparkle volume assumptions directly._

_no activity in 24h_

### polaris-brand-lp (7 hits)
_Why: Active cross-market dependency; Brandon implicitly committed Richard to a Google Experiment alt-measurement path before 5/5 AU handoff. Rollout process lacks automated ref tag audit — any market rollout is load-bearing._

- [23:38 email] Alex VanDerStuyf via Asana — Alex mentioned you: ps-brand pages updates WW — Due date: Apr 29. Sprint 05: MCS Design
- [15:47 email] Alex VanDerStuyf via Asana — New comment on: ps-brand XF + Template — Vijeth Shetty re: today's conversation
- [2026-04-28 hedy] Paid Acquisition Team Sync — Polaris surfaced alongside ad copy (UK/IT +11% CTR), OP1 planning, MX Sparkle $1.2M projection
- [2026-04-28 hedy] AU Paid Search Handover and Performance Review — Polaris LP test drove 30% conv rate drop; reverted to legacy (kickoff for Richard→Megan handover)
- [2026-04-28 hedy] OP1 Budgets and Data Sync — 1:1 with Brandon; Polaris pages DDD referenced alongside F90 LiveRamp and ABIX portfolio consolidation
- [loop] 2026 DDD (Deep Dive and Debate) — 4/16 Polaris Brand LP Weblab alignment session recent; 5/4 AI Week with Adi/Richard upcoming
- [loop] Weekly Meeting Doc (WBR Callouts + Agenda) — Polaris Brand LP weblab test (AU/DE/FR feedback to Dwayne pending weblab)

### oci-rollout (9 hits)
_Why: 8/10 markets at 100%. AU + MX remain TBD, blocked on MCC creation — each quarter without AU OCI forgoes 18–24% reg uplift._

- [15:16 email] Adobe Advertising Cloud Search — [EXTERNAL] Campaign Report OCI Tracking Template has completed — OCI Tracking Template → OCI Reporting Feed completed
- [2026-04-28 hedy] Paid Acquisition Team Sync — IECCP ~50% budget guidance discussed alongside OP1/Sparkle
- [2026-04-28 hedy] AU Paid Search Handover and Performance Review — IAPRSTCCP referenced in handover context
- [loop] 2026 Paid Acq MBR / QBR — OCI stats (US +19k reg/+24%, UK +2.4k/+23%, DE +749/+18%)
- [loop] 2026 DDD — 3/19 OCI dial-ups session (EU3, FR, JP, CA) referenced
- [loop] Weekly Meeting Doc — OCI dial-up progression: EU3 4/27 100% switch, CA starting dial-up, FRITES/JP smart bidding
- [loop] Richard/Brandon 1:1 Notes — OCI rollout UK/DE/EU5 on recent agenda

### au-handoff (8 hits)
_Why: Handoff target 5/5. Every late-breaking AU signal is decision-relevant until the doc ships and the new owner takes over._

- [2026-04-29 00:04 slack #dm-brandon] prichwil (Richard): "looks like Alexis is dipping out"
- [2026-04-28 23:06 slack #ab-paid-search-abix] brandoxy (Brandon Munday): "ok @Richard I've got my feedback in the AU Transition doc. Can you look through?"
- [2026-04-28 hedy] AU Paid Search Handover and Performance Review — biweekly AU sync serving as kickoff for formal Richard→Megan handover next week. CPA down to $107 from ~$155 via NB CPC improvements. Brandon leading transition.
- [loop] Richard/Brandon 1:1 Notes — AU performance/transition from Harjeet to Lena on recent agendas

### ww-testing-methodology (2 hits)
_Why: Testing Approach doc is the formalization of PS testing authority. Any Kate/Brandon/Todd mention or team discussion of SyRT/framework is strategic._

- [14:11 email] Asana — You have unread notifications — Testing Document for Kate moved from Prioritized to Complete in ABPS
- [loop] 2026 DDD — 3/12 Testing Doc review session referenced in history

---

## P2 — worth knowing

### sparkle-and-baloo (3 hits)
_Why: Sparkle drives MX Y2026 $824K–$1.1M projection spread. Baloo is the MX follow-on. Both feed the brand-trajectory model directly._

- [2026-04-28 hedy] Paid Acquisition Team Sync — MX Sparkle $1.2M projection called out, Baloo referenced alongside
- [2026-04-28 hedy] OP1 Budgets and Data Sync — Sparkle mentioned alongside MX duplicate invoice status (Diana leading, Pedro in loop)
- [loop] 2026 Paid Acq MBR / QBR — Baloo acceleration detail: US shopping ads paused through 2026, UK-only $14–23MM opportunity

### mx-budget-ieccp (0 hits)
_Why: Y2026 MX at $824K default vs $1.1M Sparkle-confidence — budget + PAM availability questions are load-bearing._

_no activity in 24h — note: Sparkle/MX content surfaced via adjacent topics (sparkle-and-baloo hedy hits reference MX $1.2M projection)_


**Constraint:** All identifiers, thresholds, and rules in this section are load-bearing. Modifications require re-validation.

### ai-search-aeo (2 hits)
_Why: L4 priority — Richard owns the PS POV. Any competitor signal, platform announcement, or internal discussion is raw material._

- [17:08 slack #ab-paid-search-global] jpslater (J Slater): "Quip link for AI Max questions to discuss with Google team" — 1 reply
- [loop] 2026 Paid Acq MBR / QBR — 3P AI integration bright lines (ChatGPT/Claude/Perplexity) on recent agenda

### liveramp-enhanced-match (3 hits)
_Why: Cross-team MarTech dependency affecting attribution quality across all markets._

- [2026-04-28 hedy] OP1 Budgets and Data Sync — LiveRamp Enhanced Match legal review prep on 1:1 agenda
- [loop] Weekly Meeting Doc — F90/LiveRamp audience setup in recent weekly agenda
- [loop] Richard/Brandon 1:1 Notes — F90 LiveRamp enhanced match on recent weeks' focus

### reftag-and-attribution (2 hits)
_Why: AU-specific workaround is fragile; Italy P0 regression + MX Auto overwrite prove this is a recurring failure mode. Attribution breakage invalidates test reads._

- [2026-04-28 hedy] OP1 Budgets and Data Sync — RefTag tagged in meeting topics alongside Adobe, GenBI keyword reporting issues for AU
- [loop] Weekly Meeting Doc — sitelink audit (Fortune 100 copy) referenced; ref tag work implicit in Polaris Brand LP weblab feedback loop

### f90-lifecycle-legal (4 hits)
_Why: Audiences workstream is blocked on Legal SIMs. Feeds directly into the WW Testing Loop._

- [2026-04-28 hedy] Paid Acquisition Team Sync — F90 tagged in meeting topics alongside Jasper AI legal signoff
- [2026-04-28 hedy] OP1 Budgets and Data Sync — F90 tagged; LiveRamp Enhanced Match legal review prep covered
- [loop] Weekly Meeting Doc — F90/LiveRamp audience setup on recent weekly agenda
- [loop] Richard/Brandon 1:1 Notes — F90 LiveRamp enhanced match on recent weeks' focus

### kiro-agentspaces-tooling (3 hits)
_Why: L3 is the next active level. 4/17 AI Tool Demo produced 6 committed adopters — signals help graduate tools from personal to team-standard._

- [19:01 email] Machine Learning University — May 7 Tech Talk: Work Smarter with Kiro IDE — Kiro IDE connects to Amazon internal tools via MCP servers
- [loop] 2026 DDD — 5/4 AI Week with Adi/Richard (Kiro offline install + use cases), 4/17 QuickSuite & Kiro comparison
- [loop] Richard/Brandon 1:1 Notes — Kiro demo syncs with Adi on recent weeks' focus

---

## P3 — background radar

### genbi-adobe-attribution (3 hits)
_Why: Cross-market measurement ground truth. Low volume, high impact when it moves._

- [2026-04-28 hedy] AU Paid Search Handover and Performance Review — manual batch optimization continues; GenBI being adopted in AU
- [2026-04-28 hedy] OP1 Budgets and Data Sync — GenBI keyword reporting issues for AU covered
- [loop] Richard/Brandon 1:1 Notes — MX ie%CCP projections with Carlos/Lorena on recent agenda (adjacent signal)

### competitor-intel (0 hits)
_Why: Market intel for WBR callouts and MBR narratives._

_no activity in 24h_

### ad-copy-and-creative (4 hits)
_Why: Modern Search workstream. UK Phase 1 delivered +86% CTR, +31% regs — strongest evidence base in the program._

- [2026-04-28 20:14 slack #ab-paid-search-global] prichwil (Richard): "@Stacey @J found our US and CA accounts had ads with text '55 of the Fortune 100' or '50 of the Fortune 100' — need to change to correct: Most Fortune 100 Companies Purchase Supplies On Amazon Business / Used By Most of Fortune 100"
- [2026-04-28 18:24 slack #ab-marketing-ai] Recap of AWS agentic AI livestream — Amazon Connect family, OpenAI models on Bedrock, Quick desktop available today
- [15:47 email] Alex VanDerStuyf via Asana — New comment on: ps-brand XF + Template — Vijeth Shetty context
- [2026-04-28 hedy] Paid Acquisition Team Sync — non-brand ad copy testing (11% CTR lift UK/IT), Keyword Insertion tagged in topics

---

## Monitoring

### new-markets (0 hits)
_Why: If WW PSME expands, scope changes. Radar only._

_no activity in 24h_

### org-changes (1 hit)
_Why: Direct-line org changes affect priorities, coaching, and career path._

- [2026-04-29 10:58 email] Cone, David — 2027 OP1 Registrations Inputs [Pending final workback] — +Shan/Masato for EU/JP SMB visibility. Thread referenced Brandon Munday.

---

## Review needed

_No topics have passed their review_date yet. Nearest upcoming: `au-handoff` (2026-05-15, sunset after handoff confirmed stable)._

## Operating notes

- **Signal concentration (today):** au-handoff (8 hits) and oci-rollout (9 hits) lead P1 — consistent with the week's load-bearing stories (5/5 AU handoff + EU3 OCI 100% switch 4/27). polaris-brand-lp (7) is the other cluster.
- **Quiet P1s:** mx-registration-funnel silent 1st day. Expected given Cristobal's launch is 5 days old. Escalate if still silent by end of week.
- **L1 / L5 silent today:** first run, so no sustained-silence signal. Watch tomorrow.
- **Low Slack volume (25 messages in 24h total, 5 topic hits):** consistent with Tuesday being a slower Slack day post-weekend catch-up; not a scanner issue.
- **Hedy coverage concentrated:** 2 meetings (Paid Acq Team Sync + OP1 Budgets 1:1 with Brandon) account for all Hedy hits — each meeting tags many topics via its `topics[]` array, which inflates hit count. Cross-topic dedup is OK here — the signal is "this topic came up" not "a unique event happened".
- **Schema note:** `slack_messages.channel_section` missing vs. protocol spec. Scan fell through to all-channels mode. If noisy Channels-section messages start leaking into P1/P2 topics, revisit the ingester schema.
