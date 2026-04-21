#!/usr/bin/env python3
"""Merge a dict of enriched Asana tasks (with completion dates) into the
contribution input file at /tmp/contrib-inputs/asana_completed.json.

Run after the orchestrating agent has called GetTaskDetails for each gid and
collected the results. For now, this script holds the enrichment inline as a
one-time backfill — future runs will read from a richer Asana pull.
"""
import json
from pathlib import Path

INPUT = Path("/tmp/contrib-inputs/asana_completed.json")

ENRICHED = {
    "1213917691089036": {"completed_at": "2026-04-20T15:34:12.118Z", "name": "Refmarker mapping audit PoC — AU", "permalink_url": "https://app.asana.com/1/8442528107068/project/1212762061512767/task/1213917691089036", "memberships": [{"project": {"name": "AU"}}]},
    "1214137998433533": {"completed_at": "2026-04-20T15:30:27.802Z", "name": "Italy Polaris ref tag P0 — revert + restore tracking", "permalink_url": "https://app.asana.com/1/8442528107068/project/1205997667578893/task/1214137998433533", "memberships": [{"project": {"name": "ABPS - WW Testing & Projects"}}]},
    "1213925516289208": {"completed_at": "2026-04-17T22:52:04.415Z", "name": "Enhanced Match / LiveRamp — Audience Expansion", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213925516289208", "memberships": []},
    "1213925549433825": {"completed_at": "2026-04-17T22:50:43.035Z", "name": "Email Overlay WW Rollout Plan", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213925549433825", "memberships": []},
    "1213925549385885": {"completed_at": "2026-04-17T22:50:36.845Z", "name": "Paid Search Testing Approach & Year Ahead", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213925549385885", "memberships": []},
    "1213925516128369": {"completed_at": "2026-04-17T22:51:50.779Z", "name": "ie%CCP Planning & Optimization Framework", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213925516128369", "memberships": []},
    "1213925647933633": {"completed_at": "2026-04-17T22:51:05.113Z", "name": "MX Paid Search — Market Wiki", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213925647933633", "memberships": []},
    "1213953288179600": {"completed_at": "2026-04-17T22:51:54.887Z", "name": "Cross-Market Playbook — US → EU5 → RoW", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213953288179600", "memberships": []},
    "1213925733093966": {"completed_at": "2026-04-17T22:51:27.116Z", "name": "Polaris WW Rollout — Status and Decision Log", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213925733093966", "memberships": []},
    "1213953288745383": {"completed_at": "2026-04-17T22:52:02.182Z", "name": "AU Paid Search — Market Wiki", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213953288745383", "memberships": []},
    "1213925515835393": {"completed_at": "2026-04-17T22:51:48.897Z", "name": "OCI Impact Summary — The Business Case", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213925515835393", "memberships": []},
    "1213925648102375": {"completed_at": "2026-04-17T22:51:31.159Z", "name": "AU Keyword CPA Dashboard — Design", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213925648102375", "memberships": []},
    "1213925733287816": {"completed_at": "2026-04-17T22:51:44.740Z", "name": "Landing Page Testing Playbook", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213925733287816", "memberships": []},
    "1213925647211049": {"completed_at": "2026-04-17T22:51:59.511Z", "name": "AEO / AI Overviews POV — Amazon Business Paid Search", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213925647211049", "memberships": []},
    "1213925733042547": {"completed_at": "2026-04-17T22:51:20.269Z", "name": "OCI Execution Guide", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213925733042547", "memberships": []},
    "1214006611366954": {"completed_at": "2026-04-14T04:17:15.568Z", "name": "Reply to Brandon — MX budget line / underspend risk", "permalink_url": "https://app.asana.com/1/8442528107068/task/1214006611366954", "memberships": []},
    "1214068319315340": {"completed_at": "2026-04-15T22:02:31.570Z", "name": "Prep for MX LP optimization call (tomorrow 12 PM CST)", "permalink_url": "https://app.asana.com/1/8442528107068/task/1214068319315340", "memberships": []},
    "1213963678745039": {"completed_at": "2026-04-13T23:24:38.652Z", "name": "Pull AU Polaris LP conversion rate data — share with Brandon + Dwayne", "permalink_url": "https://app.asana.com/1/8442528107068/project/1212762061512767/task/1213963678745039", "memberships": [{"project": {"name": "AU"}}]},
    "1213917772329115": {"completed_at": "2026-04-08T14:18:45.292Z", "name": "Provide Lorena Q2 expected spend for MX PO", "permalink_url": "https://app.asana.com/1/8442528107068/project/1212775592612917/task/1213917772329115", "memberships": [{"project": {"name": "MX"}}]},
    "1214006150150818": {"completed_at": "2026-04-12T00:13:01.552Z", "name": "Reply to Brandon — Polaris LP Brand page ETA", "permalink_url": "https://app.asana.com/1/8442528107068/task/1214006150150818", "memberships": []},
    "1214035135799172": {"completed_at": "2026-04-12T00:12:50.136Z", "name": "Reply to Stacey/York — SSR Cost and Reg inputs for IECCP", "permalink_url": "https://app.asana.com/1/8442528107068/task/1214035135799172", "memberships": []},
    "1213072707685834": {"completed_at": "2026-04-15T23:41:09.255Z", "name": "MX Automotive page", "permalink_url": "https://app.asana.com/1/8442528107068/project/1212775592612917/task/1213072707685834", "memberships": [{"project": {"name": "MX"}}]},
    "1213993242326093": {"completed_at": "2026-04-15T23:40:37.045Z", "name": "AU meetings - Agenda", "permalink_url": "https://app.asana.com/1/8442528107068/project/1212762061512767/task/1213993242326093", "memberships": [{"project": {"name": "AU"}}]},
    "1213546434830000": {"completed_at": "2026-04-08T14:17:11.214Z", "name": "ie%CCP calc - insert MX spend/regs before 9th", "permalink_url": "https://app.asana.com/1/8442528107068/task/1213546434830000", "memberships": []},
}

def main():
    data = json.loads(INPUT.read_text())
    enriched_names = {e["name"] for e in ENRICHED.values()}
    kept = [t for t in data["data"] if t.get("name") not in enriched_names]
    new_list = [
        {"gid": gid, "name": r["name"], "completed_at": r["completed_at"], "permalink_url": r["permalink_url"], "memberships": r["memberships"]}
        for gid, r in ENRICHED.items()
    ] + kept
    INPUT.write_text(json.dumps({"data": new_list}, indent=2))
    print(f"asana_completed.json: {len(new_list)} total ({len(ENRICHED)} enriched with dates, {len(kept)} name-only)")

if __name__ == "__main__":
    main()
