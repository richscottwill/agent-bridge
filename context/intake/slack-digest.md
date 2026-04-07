<!-- DOC-0187 | duck_id: intake-slack-digest -->
# Slack Digest — Monday, April 6, 2026
Scan window: 2026-04-06T00:00:00Z → 2026-04-06T14:30:00Z
Channels scanned: 14 | Signals extracted: 5 | Proactive searches: 3 (1 failed auth)

---

## 🔴 HIGH PRIORITY

### OCI URL Transform — Ref Tag Integrity Issue (ACTIVE THREAD)
- **Channel:** #ab-paid-search-oci (C06R6R19LG0)
- **Author:** Brandon Munday (brandoxy) — 2026-04-06 03:30 UTC (scheduled message)
- **Thread:** Brandon asked Yashasvi Chowta (ychowta) whether OCI transforms URLs. Seeing ref tags in logs like `pd_sl_OCI_97FL_MD_e_APJ288_HFF794_dev_c OCI` but source refs are `ref=pd_sl_ver_art_avt_all_309666204_y131362558227`.
- **Reply:** Yashasvi (08:40 UTC): "No Brandon, We are not doing any URL transformation. In which marketplace is it happening? and in which logs did you find this?"
- **Status:** Thread open — Brandon hasn't replied yet with marketplace/log details.
- **[ACTION-RW]** This directly impacts ref tag tracking integrity across OCI markets. Richard should monitor this thread and be ready to provide marketplace context if Brandon asks. This connects to the RefTag_SEM tracking work.
- **Hot Topic:** Reinforces existing "OCI URL Transform / Ref Tag Integrity" topic (signal_count: 2 → 3).

### PAM Budget — Brandon @mention STILL UNANSWERED (3+ days)
- **Channel:** #ab-paid-search-app (C05KTAAG14J)
- **Status:** No new messages today, but the Brandon @mention about extra PAM budget from 2026-04-03 remains unanswered. Now 3+ days stale.
- **[ACTION-RW]** Respond to Brandon's PAM budget message. This is a direct manager ask that's aging.

---

## 🟡 MEDIUM PRIORITY

### MX Budget / R&O Process Change — No New Activity
- **Channel:** #ab-paid-search-abix (C065KKT53DJ)
- **Status:** No new messages today. Last activity 2026-04-03. Richard acknowledged via +1 reaction. Brandon's action item summary was the last signal.
- **Hot Topic:** Active but cooling. Monitor for follow-up from Yun-Kang or Brandon.

### ABMA SIM Escalation Protocol — No New Activity
- **Channel:** #ab-paid-search-global (C044UG8MCSZ)
- **Status:** No new messages today. Sev 2.5 escalation protocol discussion from 2026-04-03 appears resolved.

### AryaBot Channel — AB Data Queries Active
- **Channel:** #ask-ab-aryabot (C06M7R2SKQW)
- **Messages today:** 4 (all bot interactions — users querying AryaBot for payment methods, onboarding docs, IBA/VCS details, UNSPSC tables)
- **Signal:** AryaBot is actively being used for AB data queries. No direct relevance to PS but shows AB data tooling adoption.

---

## 🟢 FYI / LOW PRIORITY

### Baloo Early Access — No New Activity
- **Channel:** #baloo-interest (C0A9HBB9H2B)
- **Status:** No new messages today. Session invites expected by 4/6 per last signal.

### AgentSpaces Community — General Support Traffic
- **Channel:** #agentspaces-interest (C0A1JD8FCUV)
- **Messages today:** 11 (all community support — MCP loading issues, email write config, AccessDeniedException, opt-in region errors, shared storage questions, custom agent UI config request)
- **Signal:** No direct relevance to Richard. Community is active with onboarding/config issues.

### GenAI Power Users — Skills & MCP Sharing
- **Channel:** #amazon-builder-genai-power-users (C08GJKNC3KM)
- **Messages today:** 4 (oncall report skills sharing, Kiro IDE vs kiro-cli discussion, AI agent for AWS account reading, kiro-cli conversation history compaction question)
- **L5 Signal:** Tanuj Kalra sharing custom skills for oncall reports, MCM, sev2 analysis + custom MCP servers. Pattern: teams building operational automation on kiro-cli. Relevant to Level 3-5 trajectory.

### Marketing Managers All — SlideForge Cross-Post
- **Channel:** #marketing_managers_all (C01NQLC114J)
- **Messages today:** 1 (SlideForge tool announcement cross-posted — AI-powered slide deck generator from URLs/docs, built on Bedrock/CloudFront/Lambda)
- **L5 Signal:** SlideForge is a Level 3 tool example — URL-to-deck automation. Could be useful for PS team presentations.

### Andes Workbench — Data Platform Issues
- **Channel:** #andes-workbench-interest (C096T4SK3EY)
- **Messages today:** 4 (Glue ARN errors, permissions issues — platform support traffic)
- **Signal:** No direct PS relevance.

### Other Channels (LIGHT scan — count only)
| Channel | Today's Messages | Notes |
|---------|-----------------|-------|
| homeowners | 0 today (unreads from weekend) | Personal/lifestyle |
| slack-announcements | Unreads from backlog | General announcements |
| ask-ab-data | 0 today | AB data support |
| ask-an-amazonian | Unreads from backlog | General Q&A |
| remote-advocacy | Unreads from backlog | Remote work |
| rto-advocacy | Unreads from backlog | RTO discussion |
| amazon-q-apps-interest | Unreads from backlog | Q Apps |
| stargate-community | Unreads from backlog | Stargate |
| ab-gen-ai-wins | 0 today | AB GenAI wins |
| bedrock-agentcore-interest | 1 today (image gen question) | AgentCore support |
| genai-power-users-digest | 0 today | Digest channel |

---

## Proactive Search Results

| Query | Results | Notes |
|-------|---------|-------|
| `prichwil after:2026-04-06` | 0 matches | No direct mentions of Richard today |
| `from:@brandoxy after:2026-04-06` | Auth error | Search API returned invalid_auth — retry next cycle |
| `from:@kataxt after:2026-04-06` | 0 matches | No Kate messages today (Sunday) |

---

## Hot Topics Update

| Topic | Status | Last Signal | Channels | Action |
|-------|--------|-------------|----------|--------|
| OCI URL Transform / Ref Tag Integrity | 🔴 Active | 2026-04-06 08:40 UTC | #ab-paid-search-oci | Monitor thread — Brandon needs to reply with marketplace details |
| PAM Budget Availability | 🔴 Stale | 2026-04-03 22:41 UTC | #ab-paid-search-app | [ACTION-RW] Respond to Brandon — 3+ days unanswered |
| MX Budget / R&O Process Change | 🟡 Active | 2026-04-03 21:30 UTC | #ab-paid-search-abix | Acknowledged. Monitor for follow-up |
| ABMA SIM Escalation Protocol | 🟡 Cooling | 2026-04-03 21:36 UTC | #ab-paid-search-global | Appears resolved |
| Baloo Early Access | 🟡 Active | 2026-04-03 17:17 UTC | #baloo-interest | Session invites expected today |

---

## Scan Metadata
- Scan type: AM-1 Slack Ingestion (Subagent A)
- DuckDB writes: Attempted 3 signal inserts
- Proactive search errors: 1 (brandoxy search — invalid_auth)
- Next scan: EOD cycle or next AM-1
