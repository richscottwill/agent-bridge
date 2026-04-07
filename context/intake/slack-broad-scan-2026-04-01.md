<!-- DOC-0186 | duck_id: intake-slack-broad-scan-2026-04-01 -->
# Slack Broad Keyword Scan — April 1, 2026

[Slack Backfill: broad keyword scan, Oct 2025–Apr 2026, 2026-04-01]
Source: 8 keyword searches across all channels (not Richard-specific)

## Key Findings

### OCI Timeline (100 results, 5 pages)
- **Jan 2026**: OCI launched US, UK, DE for AB. International Stores Finance (cosmaigm) reached out to validate "OCI launch in Q4'25 exceeded expectations" for SVP doc — Richard clarified AB only launched US/UK/DE, not IT/ES
- **Feb 2026**: Brandon flagged "conclude weblabs before OCI launch" as priority. Duplicate hvocijid parameter errors surfaced in EU3 (arthamm reported)
- **Mar 2026**: FR expanded to 25% OCI application. EU3 data exclusion for AMO bidding. Brandon asked about max time to remove OCI data before perf impact. JP OCI preflight initiated — Brandon asked Adi to validate steps
- **Mar 30**: OCI launch congratulated in ab-paid-search-oci channel (saadavi)
- **New person discovered**: cosmaigm (Matheus Cosmai, International Stores Finance) — reached out about OCI for SVP doc

### Polaris Timeline (100 results, 5 pages)
- **Feb 2026**: Brandon offered Richard leadership on WW Polaris rollout (mpdm with Dwayne). Dwayne confirmed overlay should only go to PS landing pages, separate OP2 initiative for Polaris pages
- **Feb 2026**: Alex VanDerStuyf (afvans) confirmed PS pages were "not in scope" for Polaris 2025, weblab was running
- **Mar 2026**: Vijay (vkumarmp) asked for separate Baloo file for NB landing pages. Brandon requested Polaris Brand page weblab feedback. Yun asked about weblab ticket. Stacey asked about JP Polaris 50/50 split on 4/6-4/7
- **Mar 27**: Stacey proposed 30/70 split as lower-risk alternative to 50/50 weblab for JP

### Baloo Timeline (108 results, 6 pages)
- **Jan 2026**: Brandon pushed back on Shopping Ads acceleration — MarTech prioritizing Associates enablement. Suggested alternate uses of Baloo dev bandwidth (cross-channel enablement)
- **Feb 2026**: Baloo date moved to EO Aug per Kingpin. Brandon asked Vijay about PS ads testing readiness
- **Mar 2026**: Aarushi (aarushij) from Baloo team needed ps_kw parameter passthrough for search page redirect. Channel consolidation: baloo_ps_mcs_integration archived → baloo-search-and-mcs
- **Mar 24**: Baloo Early Access starting 3/30, 60+ users expected through PS flow. Aarushi asked Richard about enabling without impacting metrics
- **Mar 31**: Yoav flagged meta tag noindex requirement as blocker before Baloo launch (not impacting SEO yet since behind VPN)
- **New people discovered**: aarushij (Aarushi Jamwal, Baloo tech), yoavr (Yoav R, SEO), vkumarmp (Vijay Kumar, MCS/Baloo)

### F90 Timeline (100 results, 5 pages — rich project history)
- **Jan 7**: Brandon kicked off F90 audience work — Legal approval pending, audience naming convention needed (obfuscation like trees)
- **Jan 12**: Brandon reported Tech was wrong about Legal conversations. Matt Rich (Legal) said audiences will "raise some eyebrows." Pushing for F90 and F7 top-level auds
- **Jan 26**: Andrew provided ad copy for DG and Search ads. Yun suggested F90 under existing ENG account
- **Feb 19**: Robert Skenes (rskenes) instructed to cut ABMA SIM for F90. Brandon asked Richard to submit SIM
- **Feb 23**: Brandon flagged F90 listed as "subsequent expansion" in Media's plan — pushed to include in primary tech request. Media Legal approval still pending
- **Mar 27**: Brandon finally sent F90 for L8 approval — "3 cheers for our best legal friend, Matt Rich!"
- **Mar 30**: F90 Legal approval received. Brandon assigned Richard to work between Media and Tech for implementation
- **New people discovered**: rskenes (Robert Skenes, Media), arbishar (Abdul Bishar, ABMA/Tech), malloryj (Mallory J, Media)

### Enhanced Match / LiveRamp (4 results — nascent)
- **Mar 30**: Brandon asked Richard to investigate Enhanced Match with Abdul/Adobe — 4 specific questions about data requirements, Google data changes, contracts, and other Amazon org usage
- Still early stage — blocked across Amazon per Clara

### Decision Language Search (0 results in ab-paid-search-global)
- The `in:` modifier combined with decision keywords returned nothing — likely because Slack search doesn't support `in:` for private channels by name. Decision signals were captured through the project-specific searches above.

## DuckDB Impact
- 24 messages inserted to slack_messages with signal_type tags (decision, action-item, status-change, escalation, mention, topic-update)
- Covers 6 channels + 4 DMs across 5 project areas

## Routing
- [target: current.md] — Baloo Early Access 3/30, F90 legal approved, OCI JP preflight
- [target: memory.md] — New contacts: cosmaigm, aarushij, yoavr, rskenes, arbishar, malloryj
- [target: eyes.md] — Baloo noindex blocker, Enhanced Match blocked across Amazon
