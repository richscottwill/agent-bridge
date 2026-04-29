#!/usr/bin/env python3
"""Populate the 4 intelligence sections in command-center-data.json per am-frontend.md protocol.

Reads existing command-center-data.json, adds/updates:
- commitments: Richard's words first (said_by=richard), then others asked (manager > stakeholder > peer)
- delegate: tasks Richard is doing that someone else could own
- communicate: things Brandon shared that team should know
- differentiate: career-coaching-derived high-leverage actions

Content is hand-curated from today's 4/28 context (Hedy sessions, Slack signals, emails, Loop, Asana).
"""
import json
from pathlib import Path
from datetime import datetime, timezone

DATA = Path.home() / "shared/dashboards/data/command-center-data.json"

commitments = [
    # === Richard said it ===
    {
        "text": "Richard committed to scoping Kiro weekly AU change aggregator before 5/5 handoff",
        "source": "Loop Richard/Brandon 1:1 Notes 4/21",
        "person": "Brandon Munday",
        "days_old": 7,
        "overdue": False,
        "said_by": "richard",
        "quote": "I'll build the aggregator before 5/5 as the oversight mechanism after handoff"
    },
    {
        "text": "Richard committed to adding F90 Legal approval link to Media Tech SIM",
        "source": "Slack dm-brandon 4/27 23:00 UTC",
        "person": "Brandon Munday",
        "days_old": 1,
        "overdue": False,
        "said_by": "richard",
        "quote": "Yeah I can add the link to the approval now"
    },
    {
        "text": "Richard owns alternate measurement design for AU/MX Brand LP test (non-Weblab)",
        "source": "Slack ab-paid-search-abix 4/27 + Asana 1214330104198712 due 5/6",
        "person": "Brandon Munday",
        "days_old": 1,
        "overdue": False,
        "said_by": "richard",
        "quote": "Test design doc lands by 5/6"
    },
    {
        "text": "Richard to create 1-2 Kiro PS use cases for team + offline solution exploration with Adi",
        "source": "Loop Richard/Brandon 1:1 Notes 4/21",
        "person": "Brandon Munday",
        "days_old": 7,
        "overdue": False,
        "said_by": "richard",
        "quote": "I'll create use cases beyond callouts and get with Adi on offline wiki/directory"
    },
    {
        "text": "Richard to draft 3-bullet email overlay update into Outbound Marketing Goals.xlsx post-1:1",
        "source": "New Asana task 1214351597615320 + Brandon email 4/17",
        "person": "Brandon Munday",
        "days_old": 0,
        "overdue": False,
        "said_by": "richard",
        "quote": "I'll drop 3 bullets by EOD 4/28"
    },
    {
        "text": "Richard to Fortune 100 ad copy audit globally + creative site link audit with Lucy's team",
        "source": "Hedy Weekly Paid Acq 4/21 (session hHqCFkFKep3crudfjW70)",
        "person": "Team",
        "days_old": 7,
        "overdue": False,
        "said_by": "richard",
        "quote": "I'll update Fortune 100 copy and do a broad audit of site links"
    },
    {
        "text": "Richard to send updated MX monthly spend forecast to Addy + initiate R&O reallocation with Lorena",
        "source": "Hedy Weekly Paid Acq 4/21",
        "person": "Brandon Munday",
        "days_old": 7,
        "overdue": False,
        "said_by": "richard",
        "quote": "I'll send Lorena the reallocation ask and CC Mexico team"
    },
    # === Others asked - Manager (Brandon) ===
    {
        "text": "Create Intro Guide for VPN Access / BrowserStack",
        "source": "Slack dm-brandon 4/27 + Asana 1214305906350457",
        "person": "Brandon Munday",
        "days_old": 1,
        "overdue": False,
        "said_by": "other",
        "asker_weight": "manager",
        "quote": "hey, do you think you could create a quick Loop doc on what to do with Browserstack access?"
    },
    {
        "text": "Clarify CAT vs MCS email overlay status for Outbound Marketing Goals",
        "source": "Email 4/17 via Asana + new task 1214351597615320",
        "person": "Brandon Munday",
        "days_old": 11,
        "overdue": True,
        "said_by": "other",
        "asker_weight": "manager",
        "quote": "can you clarify the email overlay status? Confused since CAT one is live and MCS one still planned"
    },
    {
        "text": "Measure EM impact subtask (F90 LR Enhanced Match)",
        "source": "Brandon Asana assignment 4/21",
        "person": "Brandon Munday",
        "days_old": 7,
        "overdue": False,
        "said_by": "other",
        "asker_weight": "manager",
        "quote": "Measure EM impact subtask"
    },
    {
        "text": "PO #2D-19910168 approval — needs FAQ added first",
        "source": "Brandon email 4/24",
        "person": "Brandon Munday",
        "days_old": 4,
        "overdue": False,
        "said_by": "other",
        "asker_weight": "manager",
        "quote": "I'm ready to approve this, but don't see an FAQ. Can you get an FAQ in there and I'll approve?"
    },
    {
        "text": "Prep Kiro PS use cases for Kate AB Marketing AI demo May 29",
        "source": "Brandon email 4/22 + Asana 1214330286428120",
        "person": "Brandon Munday",
        "days_old": 6,
        "overdue": False,
        "said_by": "other",
        "asker_weight": "manager",
        "quote": "FYI, get ready b/c you'll be presenting to Kate and her leaders. Plan to setup run-through."
    },
    # === Others asked - Stakeholder ===
    {
        "text": "$535K MX channel-tests reallocation + SPARKLE forecast clarification",
        "source": "Email 4/28 05:01 UTC (1h old)",
        "person": "Lorena Alvarez Larrea",
        "days_old": 0,
        "overdue": False,
        "said_by": "other",
        "asker_weight": "stakeholder",
        "quote": "If we move the $535K into the channel tests item, we could use the budget to launch the discussed ideas, right? Also, is this the forecast without SPARKLE effect?"
    },
    {
        "text": "MX duplicate invoice $56K — status update from Google Ads support",
        "source": "Email 4/27 18:20 UTC — Diana escalated to her manager",
        "person": "Diana De la Fuente",
        "days_old": 1,
        "overdue": False,
        "said_by": "other",
        "asker_weight": "stakeholder",
        "quote": "Escalating to my manager. Asking for latest status from Google."
    },
    {
        "text": "AU LP URL analysis + CPA methodology response",
        "source": "Lena Zak — 17+ days unreplied per state file",
        "person": "Lena Zak",
        "days_old": 17,
        "overdue": True,
        "said_by": "other",
        "asker_weight": "stakeholder",
        "quote": "Response pending since 4/3 draft"
    },
    # === Others asked - Peer ===
    {
        "text": "AB Marketing refmarker mapping audit PoC",
        "source": "Email 4/21 from Kristine Weber (via Brandon)",
        "person": "Kristine Weber",
        "days_old": 7,
        "overdue": False,
        "said_by": "other",
        "asker_weight": "peer",
        "quote": "Need PoC from teams for AB Marketing refmarker mapping audit"
    },
    {
        "text": "Confirm AU PS Weekly Update in shared tracker",
        "source": "Brandon email 26d ago",
        "person": "Brandon Munday",
        "days_old": 26,
        "overdue": True,
        "said_by": "other",
        "asker_weight": "manager",
        "quote": "AU PS Weekly Update"
    }
]

delegate = [
    {
        "task": "AU Google monthly invoice send (Sat 5/2)",
        "to": "Yun-Kang Chu",
        "reason": "Post-5/5 AU handoff — invoice send is operational work Yun already owns for other markets. Transfer ownership effective 5/2."
    },
    {
        "task": "Change log updates for AU (current CSV-driven process)",
        "to": "Alexis Eck (L6 AU execution partner)",
        "reason": "After 5/5 handoff, Alexis is the hands-on AU operator. Change log is a regular artifact of the work — not a separate task. Alexis should own or explicitly flag to Richard."
    },
    {
        "task": "MX ad copy updates (e.g., Fortune 100 audit execution for MX)",
        "to": "Yun-Kang Chu",
        "reason": "Yun already supports MX invoicing and has account access. Copy update for MX market is L3 tactical work — Yun is the natural owner now that Carlos transitioned out."
    },
    {
        "task": "Brand LP US weblab dial-up coordination (with Alex + Vijeth)",
        "to": "Dwayne Palmer",
        "reason": "DE/FR weblab authoring finalizing 4/29; US is already live. Dwayne consolidated the feedback. Coordination of Alex items 3/4/5 + Vijeth items 1/2/6 is MCS-owned, not PS-owned."
    },
    {
        "task": "IT Polaris ref tag remediation (Italy P0)",
        "to": "Alex VanDerStuyf",
        "reason": "Alex restored legacy Italy template 4/16 and parked Polaris variant. Full remediation + audit methodology for other markets is MCS's continuing work — Richard only needs the audit result for AU."
    },
    {
        "task": "Sitelink audit (US market)",
        "to": "Stacey Gu",
        "reason": "US is Stacey's market. Sitelink audit is tactical execution — Stacey can audit US sitelinks and share back; Richard applies WW learnings to AU/MX/PAM."
    },
    {
        "task": "OCI Japan benchmarking documentation",
        "to": "Adi Thakur + Stacey Gu",
        "reason": "Brandon 4/21 explicitly assigned this pair during Weekly Paid Acq sync. Adi offline → SharePoint. Richard should not be in the critical path."
    }
]

communicate = [
    {
        "text": "Biweekly AU cadence locked with Alexis; 5/5 final handoff; no scheduled AU calls after",
        "context": "Brandon 4/21 Loop 1:1 notes. Needs to be communicated to AU team in today's sync and to Alexis Eck explicitly in 4/29 Brandon review."
    },
    {
        "text": "Andrew Furst is coming in as new Paid App lead; Peter Ocampo will transition off solo ownership once AF is in place",
        "context": "Brandon 4/21 Loop. Affects PAM reporting continuity and Primeday planning. Team should be aware of transition before Peter asks for Primeday plan."
    },
    {
        "text": "OCI official Flash readout 6/3; WBR first input 5/11. EU benchmarks complete, Japan + Canada in progress",
        "context": "Hedy Weekly Paid Acq 4/21 (Andrew). All PS team members should align reporting cadence to these dates."
    },
    {
        "text": "Compliance / Polaris rollout: rolled out to US and Japan ONLY currently. Other markets should NOT apply unless Weblab validation confirmed",
        "context": "Hedy 4/14 Brandon 1:1. Critical for any market teammate considering Polaris rollout — premature application caused AU -34% non-brand / -20% brand CVR drop."
    },
    {
        "text": "MBAT process change: PO submissions via ticketing (Mercy is POC); no QA required; new submission link live",
        "context": "Hedy Weekly Paid Acq 4/21. Team members doing POs need to use new process; no more email-based routing."
    },
    {
        "text": "Fortune 100 ad copy audit in flight; Lucy's content team partnering on site link refresh",
        "context": "Hedy Weekly Paid Acq 4/21. Stacey + Adi need to align on US implementation of updated copy."
    },
    {
        "text": "Kate AB Marketing AI demo May 29 — Richard + Adi presenting Kiro PS use cases to Kate and her leaders",
        "context": "Brandon email 4/22. High-visibility Kate-facing. Team should be aware so they can surface use cases / offer to contribute."
    },
    {
        "text": "F90 Enhanced Match / LiveRamp: ~$255K PS ENG budget confirmed. Legal approval pending TPS. Richard owns FAQ drafting for legal",
        "context": "Hedy + Brandon 4/20 Loop comment. Team should know F90 is still in-flight and to escalate match-rate questions to Richard."
    }
]

differentiate = [
    {
        "action": "Ship the Brand LP AU/MX test design doc by 5/6 as a referenceable artifact Brandon can cite in WBRs/MBRs",
        "why": "Brandon 3/24 coaching: 'proactive sharing of results' + 'earning trust through regimented mechanisms.' Artifact-shipping is what promo criteria calls 'walking on water.' The test design is the next concrete L2 Five Levels artifact."
    },
    {
        "action": "Lead the Kate AB Marketing AI demo with Adi on 5/29 — present 2-3 Kiro PS use cases, not just the callout pipeline",
        "why": "Brandon 4/22 email: 'get ready, you'll be presenting to Kate and her leaders.' L8-facing visibility. Brandon's annual review coaching (3/24) said 'one voice should be you' — this is the opportunity to demonstrate that."
    },
    {
        "action": "Own the $535K MX reallocation conversation end-to-end — draft the Lorena reply, align Brandon pre-send, initiate R&O release, close by 5/15",
        "why": "Brandon 4/21 Loop: 'RW's proposal will assume elevation through EOY.' Stakeholder ownership of budget conversations — not just execution. This is the L5→L7 scope stretch Brandon referenced in 4/6 comp review (10.5% driver)."
    },
    {
        "action": "Publish the Kiro weekly AU change aggregator as the handoff oversight mechanism — teammate-adopted tool = L3 achievement",
        "why": "Brandon 4/21 Loop commitment. Five Levels L3 metric: one tool adopted. If AU team (Alexis specifically) uses this post-handoff, L3 is satisfied. Device.md recurring-friction test: yes, weekly change review is a repeating pattern."
    },
    {
        "action": "Author the market expansion playbook + Year-One one-pager (both Deep Dive artifacts, both 19/12d overdue)",
        "why": "Brandon 4/14 coaching: 'leading the team into global initiatives.' Standing artifacts the team can use are the 'walk on water' evidence. Not urgent in a deadline sense, important in a legitimacy sense."
    },
    {
        "action": "Get in front of the ChatGPT Ads industry signal (Beggs 4/27 first-in-wild sighting) — draft Zero-Click / AEO POV by end of May",
        "why": "Five Levels L4 (Zero-Click Future). Beggs's sighting is an input signal. If Richard owns the POV narrative before AEO becomes a team priority, he sets the frame. L4 key metric: published POV."
    },
    {
        "action": "Close the 5-week-overdue backlog (Lorena 34d, Brandon 22d PAM, Lena 17d AU LP) — not one at a time, but a Friday sweep",
        "why": "Brandon 3/24 coaching feedback: 'regimented mechanisms.' Stale threads are trust leaks. Clearing 3+ high-stakes unreplied threads in one session is the reverse of the avoidance pattern. Habit-loop reward visible in streak."
    }
]

# Load, patch, write
with open(DATA) as f:
    payload = json.load(f)

payload["commitments"] = commitments
payload["delegate"] = delegate
payload["communicate"] = communicate
payload["differentiate"] = differentiate
payload["intelligence_updated"] = datetime.now(timezone.utc).isoformat()

with open(DATA, "w") as f:
    json.dump(payload, f, indent=2)

print(f"✅ Intelligence sections written to {DATA}")
print(f"   commitments: {len(commitments)} items ({sum(1 for c in commitments if c.get('said_by')=='richard')} Richard-said)")
print(f"   delegate: {len(delegate)} items")
print(f"   communicate: {len(communicate)} items")
print(f"   differentiate: {len(differentiate)} items")
