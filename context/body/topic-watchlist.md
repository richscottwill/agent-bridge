<!-- DOC-0411 | duck_id: organ-topic-watchlist -->



# Topic Watchlist

*Declarative list of topics Richard wants flagged across email, Slack, Loop, Hedy, and Asana — regardless of sender. Used by the Topic Sentry hook (daily) and the Broad Sweep hook (weekly) to catch structural signals the AM Brief's sender-priority filter misses.*

Last updated: 2026-04-28 (revised after state-file keyword mine; removed duplicate single-hard-thing topic)

---




## How this file is used

Three consumers:

1. **Topic Sentry hook (daily).** Scans last 24h of emails + Slack + Loop + Hedy for matches against each topic's keywords. Hits go to `~/shared/context/active/topic-sentry.md` grouped by priority.
2. **Broad Sweep hook (weekly).** Runs the same classifier over a longer window (up to 14 days) and uses hit counts to propose promotions, demotions, and new topics.
3. **Humans.** Read this file directly to see what the system is paying attention to. If a topic isn't here, the system won't flag it proactively — that's by design.




## Schema

Each topic is a markdown section (H3) with these fields:

```



### <topic-slug>
- **Status:** active | monitoring | sunset
- **Priority:** P1 (must surface) | P2 (worth knowing) | P3 (background)
- **Level:** L1 | L2 | L3 | L4 | L5 | operational — which Five Levels layer this advances
- **Keywords:** comma-separated phrases; quoted phrases match exactly, unquoted tokens match case-insensitive substring
- **Senders/distros:** optional — if set, boosts match score when sender matches (counts as a match even without keyword hit)
- **Channels:** all | email | slack | loop | hedy | asana (comma-separated)
- **Why it matters:** one line explaining what you'd do with a hit
- **Review:** YYYY-MM-DD — next time to re-evaluate whether this stays on the list
```

**Rules of thumb:**
- If a keyword list is shorter than 3 entries, it's probably too narrow.
- If a keyword list is longer than 12 entries, consider splitting into sub-topics.
- Review dates matter: topics without a review date become cruft. Default cadence = quarterly (90 days).
- `Level` connects every topic to the Five Levels — if a topic doesn't advance any Level, ask whether it belongs here at all.
- Subtraction before addition — prune sunset topics; don't let this file grow unbounded.

**Anti-pattern:** topic-per-person ("everything Kate mentions"). Sender filtering lives in the AM Brief. Topics here are about *subject matter*.

**Anti-pattern:** duplicating the hard-thing-selection protocol. The system now tracks a few top signals via `signals.signal_tracker` + `main.hard_thing_candidates` — the watchlist is broader-and-slower, not the same mechanism. Topics can *support* current hard thing work (e.g., `ww-testing-methodology` supports the Testing Approach doc) without BEING the hard thing.

---




## Active topics (P1 — must surface)




### mx-registration-funnel
- **Status:** active
- **Priority:** P1
- **Level:** operational (MX is one of two markets Richard owns hands-on)
- **Keywords:** ABMX, "ABMX registration", "registration funnel", RCR, "auto-verification", AVP, "manual verification", "MV%", CSF, RFC, "sole proprietor", "Mexico registration", "ABMX verification", "CSF upload", "MX registration"
- **Senders/distros:** crisjg@amazon.com, mx-abmx-interest@amazon.com, ab-product-mgrs@amazon.com, amazon-business-feature-announcement@amazon.com, lorealea@amazon.com
- **Channels:** email, slack, hedy
- **Why it matters:** MX reg funnel changes shift CPA math and Sparkle volume assumptions directly. The 2026-04-24 Cristobal launch (AVP 38%→73%, MV% -2,280bps) was the miss that created this file.
- **Review:** 2026-07-28




### polaris-brand-lp
- **Status:** active
- **Priority:** P1
- **Level:** L2 (Drive WW Testing — Polaris LP rollout is a cross-market test)
- **Keywords:** Polaris, "Polaris landing page", "brand LP", "Polaris LP", "landing page experiment", "LP revert", "Polaris dial-up", "ps-brand", "cp/ps-brand", MCS-3004, "Polaris Redesign", "Polaris migration", "ref tag audit"
- **Senders/distros:** brandoxy@amazon.com, Dwayne Palmer, Alex VanDerStuyf, staceygu@amazon.com
- **Channels:** email, slack, hedy, asana
- **Why it matters:** Active cross-market dependency. Brandon implicitly committed Richard to a Google Experiment alt-measurement path before 5/5 AU handoff. Italy P0 ref tag regression 4/16 demonstrates rollout process lacks automated ref tag audit — any market rollout is load-bearing.
- **Review:** 2026-05-31




### oci-rollout
- **Status:** active
- **Priority:** P1
- **Level:** L2
- **Keywords:** OCI, "OCI rollout", "OCI MCC", "OCI launch", "OCI bidding", "online conversion integration", "one click", "one-click", "registration-less", "Canada OCI", "AU OCI", "MX OCI", CCP, "ie%CCP", "iECCP", "Smart Bidding", "data exclusion"
- **Senders/distros:** staceygu@amazon.com, arthamm@amazon.com, kpantham@amazon.com
- **Channels:** email, slack, hedy
- **Why it matters:** 8 of 10 markets at 100% OCI. AU and MX remain TBD, blocked on MCC creation — each quarter without AU OCI forgoes 18–24% reg uplift. Data-exclusion incidents distort OCI reads; Sam Tangri + Mike Babich signals are measurement-critical.
- **Review:** 2026-06-30




### au-handoff
- **Status:** active
- **Priority:** P1
- **Level:** operational (5/5 handoff target)
- **Keywords:** "AU handoff", "Australia handoff", "AU transition", "AU owner", "max-clicks", "max clicks", "Anzac Day", "AU Polaris", "AU ref tag", "AU change log", Alexis, Harjeet, DSAP, "AU Google Ads", EOFY, "AU MCC", "AU sync"
- **Senders/distros:** alexieck@amazon.com, Harjeet, lenazak (primary AU stakeholder)
- **Channels:** email, slack, hedy, asana
- **Why it matters:** Handoff target 5/5. Every late-breaking AU signal is decision-relevant until the doc ships and the new owner takes over. Brandon's oversight mechanism requires a weekly change aggregator before 5/5.
- **Review:** 2026-05-15 (sunset after handoff confirmed stable)




### ww-testing-methodology
- **Status:** active
- **Priority:** P1
- **Level:** L2 (Drive WW Testing)
- **Keywords:** "Testing Approach", "testing doc", "testing methodology", "test methodology", "WW Testing", SyRT, incrementality, "hypothesis rollout measurement", "PUBLISH verdict", "test framework", "phased rollout", "kill threshold", "win threshold", "Testing Loop"
- **Senders/distros:** kataxt@amazon.com, brandoxy@amazon.com, theimes@amazon.com
- **Channels:** email, slack, hedy, asana, loop
- **Why it matters:** The Testing Approach document is the formalization of PS testing authority. Any Kate/Brandon/Todd mention of testing methodology, any team discussion of SyRT, any workstream status claim that touches the framework is strategic signal. Replaces the narrower "testing-doc-for-kate" topic — broader framing so the topic survives the v5 ship without needing re-scoping.
- **Review:** 2026-07-28

---




## Active topics (P2 — worth knowing)




### sparkle-and-baloo
- **Status:** active
- **Priority:** P2
- **Level:** operational (MX)
- **Keywords:** Sparkle, "Sparkle regime", "Sparkle decay", "Sparkle half-life", Baloo, "Baloo phase", "Baloo launch", "Baloo MX", "Baloo early access", "Project Baloo"
- **Senders/distros:** Lorena, Brandon
- **Channels:** email, slack, hedy, asana
- **Why it matters:** Sparkle is the regime driving MX Y2026 $824K-$1.1M projection spread. Baloo is the MX follow-on. Both directly affect the brand-trajectory model and regime_fit_state.
- **Review:** 2026-06-30




### ai-search-aeo
- **Status:** active
- **Priority:** P2
- **Level:** L4 (Zero-Click Future)
- **Keywords:** AEO, "answer engine optimization", "AI Overviews", "AI search", "zero click", "zero-click", "ChatGPT search", "Perplexity", "SearchGPT", "Gemini search", "AI Max", "ai-max", "generative search", "LLM-based search"
- **Senders/distros:** —
- **Channels:** email, slack, hedy, loop
- **Why it matters:** L4 priority — Richard owns the PS POV. Any competitor signal, platform announcement, or internal discussion is raw material. AI Max test design is specifically gated here.
- **Review:** 2026-06-30



### mx-budget-ieccp
- **Status:** active
- **Priority:** P2
- **Level:** operational (MX)
- **Keywords:** "MX budget", "MX ie%CCP", "MX spend", "MX OP2", "PAM budget", "Sparkle budget", "MX forecast", "MX reforecast", "MX pacing", "NA MCC", "MX LP", "automotive LP", "MX Auto", "Lena confusion"
- **Senders/distros:** brandoxy@amazon.com, lorealea@amazon.com, lenazak
- **Channels:** email, slack, hedy, asana
- **Why it matters:** Y2026 MX at $824K default vs $1.1M Sparkle-confidence — budget decisions + PAM availability questions are load-bearing for forecast accuracy.
- **Review:** 2026-06-30




### liveramp-enhanced-match
- **Status:** active
- **Priority:** P2
- **Level:** L2
- **Keywords:** LiveRamp, "enhanced match", "Enhanced Match", "EM integration", "match rate", CDP, "customer data platform", "liveramp-enhanced-match", "identity resolution"
- **Senders/distros:** MarTech team, Data Science
- **Channels:** email, slack, hedy
- **Why it matters:** Cross-team MarTech dependency affecting attribution quality across all markets.
- **Review:** 2026-07-31




### reftag-and-attribution
- **Status:** active
- **Priority:** P2
- **Level:** L2 (measurement integrity underpins all testing)
- **Keywords:** "ref tag", reftag, "ref-tag", "referral tag", "tagging persistence", "reftag bonanza", "attribution break", "ref tag audit", "ref tag overwrite", "MCS attribution", "GenBI attribution", "Adobe attribution", "Adobe Analytics"
- **Senders/distros:** Alex VanDerStuyf, Vijeth, Dwayne Palmer
- **Channels:** email, slack, hedy
- **Why it matters:** AU-specific workaround is fragile; Italy P0 regression + MX Auto overwrite prove this is a recurring failure mode, not a one-off. Attribution breakage invalidates test reads.
- **Review:** 2026-07-31




### f90-lifecycle-legal
- **Status:** active
- **Priority:** P2
- **Level:** L2
- **Keywords:** F90, "F90 Lifecycle", "Audiences workstream", "Legal SIM", "lifecycle targeting", "90-day customer", "F90 activation", engagement channel
- **Senders/distros:** Legal team, MarTech
- **Channels:** email, slack, hedy, asana
- **Why it matters:** Audiences workstream is blocked on Legal SIMs. Any Legal or Audiences signal is unblock-relevant. Feeds directly into the WW Testing Loop.
- **Review:** 2026-07-31




### kiro-agentspaces-tooling
- **Status:** active
- **Priority:** P2
- **Level:** L3 (Team Automation)
- **Keywords:** Kiro, AgentSpaces, "DevSpaces", Brazil, Builder, "AgentCore", MCP, "model context protocol", "Kiro hook", "Kiro skill", "Kiro power", WBR callout automation, "prompt repository", agent adoption
- **Senders/distros:** —
- **Channels:** email, slack, hedy
- **Why it matters:** L3 is the next active level. The 4/17 AI Tool Demo produced 6 committed adopters — signals about Kiro/agent tooling help graduate Richard's tools from personal to team-standard.
- **Review:** 2026-06-30

---




## Active topics (P3 — background radar)




### genbi-adobe-attribution
- **Status:** active
- **Priority:** P3
- **Level:** L2
- **Keywords:** GenBI, "Adobe attribution", "attribution model", "Adobe Analytics", "data science attribution", "NB attribution", "attribution handoff"
- **Senders/distros:** Data Science team
- **Channels:** email, slack, hedy
- **Why it matters:** Cross-market measurement ground truth. Low volume, high impact when it moves.
- **Review:** 2026-07-31




### competitor-intel
- **Status:** active
- **Priority:** P3
- **Level:** L4-adjacent
- **Keywords:** competitor, "Costco Business", Staples, Uline, Officemax, "B2B promotion", "business pricing", "SMB competitor", "Mexican B2B platform", Alibaba
- **Senders/distros:** Customer Research, ABMA
- **Channels:** email, slack, hedy, loop
- **Why it matters:** Market intel for WBR callouts and MBR narratives. Feeds market-specific state files.
- **Review:** 2026-10-31




### ad-copy-and-creative
- **Status:** active
- **Priority:** P3
- **Level:** L2
- **Keywords:** "ad copy", "copy test", "creative test", "copy variant", "headline test", RSA, "responsive search", "AMZ ad copy", "Ad Copy UK", "Ad Copy Phase", "Ad Copy EU4", "Modern Search"
- **Senders/distros:** Andrew Wirtz
- **Channels:** email, slack, hedy
- **Why it matters:** Modern Search workstream. UK Phase 1 delivered +86% CTR, +31% regs — the strongest evidence base in the program. Hits feed L3 scale-what-works queue.
- **Review:** 2026-07-31

---










**Example:** This section demonstrates the pattern in practice — concrete instances ground abstract rules.


### new-markets
- **Status:** monitoring
- **Priority:** P3
- **Level:** operational
- **Keywords:** "new market", "market launch", "BR launch", "IN launch", "new country", "market expansion", "PSME expansion", "Emerging Expansion", "AB EE"
- **Channels:** email, slack, hedy, loop
- **Why it matters:** If WW PSME expands, scope changes. Not imminent — radar only.
- **Review:** 2026-10-31




### org-changes
- **Status:** monitoring
- **Priority:** P3
- **Level:** operational (career)
- **Keywords:** reorg, "organizational change", promotion, "new hire", "Kate Rundell", "Todd Heimes", "Brandon Munday", "new manager", "new director", WW PSME, "org announcement"
- **Channels:** email, slack, hedy
- **Why it matters:** Direct-line org changes affect priorities, coaching, and career path. Low frequency, high relevance.
- **Review:** 2026-10-31

---




## Sunset (do not surface — kept for audit trail)

*None yet. When a topic is retired, move its block here with a `sunset: YYYY-MM-DD` note explaining why, so future scans know not to re-add it reflexively.*

---




## Common Failures

1. **Keyword-only matching without sender boost.** A topic with narrow keywords (e.g., "Polaris LP") misses signals when stakeholders discuss it by project name or ticket ID. Fix: add sender/distro entries so the match fires on WHO even without keyword hit.
2. **Stale review dates.** Topics past their review date accumulate silently. The Sentry keeps scanning them, but nobody evaluates whether they still matter. Fix: Broad Sweep flags overdue reviews in its weekly output.
3. **P1 inflation.** Everything feels urgent → all topics drift to P1 → the priority system collapses. Fix: hard cap of 7 P1 topics. If adding a new P1, demote the weakest existing P1 first.
4. **Duplicating hard-thing-selection.** The watchlist is broad-and-slow radar; the hard-thing pipeline is narrow-and-fast. Don't add topics that are just restatements of the current hard thing — that's what `signals.signal_tracker` handles.
5. **Missing Level tag.** A topic without a Level tag can't be audited for Five Levels balance. Every topic must map to at least one Level or be explicitly tagged `operational`.

**Worked example — P1 demotion:** Current P1 count is 5. New signal: "liveramp-enhanced-match" escalates from P2 (Kate asked about it in skip-level). To add as P1: review existing P1s by last_signal_date. If `au-handoff` hasn't fired in 14d and its review_date passed → demote to P2. Now at 5 P1 again → add liveramp as P1. Log the demotion reason in the topic's `notes` field.



## Operating notes

- **Initial seed (2026-04-28):** P1 topics derived from signal_tracker top-strength topics + MX/AU/WW-Testing state file keyword mining + the ABMX-launch-miss gap. `testing-doc-for-kate` removed — replaced by broader `ww-testing-methodology` that survives v5 ship.
- **Five Levels connection:** every topic carries a `Level` tag. When Richard reviews this file, the `Level` breakdown tells him at a glance whether his radar is skewed — e.g., too many P3 L2 topics vs too few L4 topics means Zero-Click Future isn't getting airtime.
- **Keywords come from state files.** The MX, AU, and WW Testing state files are the richest vocabulary source — when adding a new topic, mine those first before inventing keywords.
- **How to add a topic:** copy any block, change fields, put in the right priority section, set a review date. The Sentry hook re-reads this file every run.
- **How to retire a topic:** move to Sunset with reason. Don't delete — audit trail matters.
- **Current distribution:** 5 P1, 6 P2, 3 P3, 2 monitoring = 16 active topics. Cap: soft 25, hard 40. Beyond that, promote/demote aggressively.
