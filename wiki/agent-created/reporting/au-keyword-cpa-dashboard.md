---
title: "AU Keyword CPA Dashboard"
slug: "au-keyword-cpa-dashboard"
doc-type: reference
type: reference
audience: team
status: REVIEW
level: L2
category: reporting
created: 2026-03-25
updated: 2026-05-01
owner: Richard Williams
tags: ["AU", "CPA", "dashboard", "keyword", "reporting"]
depends_on: ["wbr-callout-guide"]
consumed_by: ["wiki-concierge", "am-auto"]
summary: "Reference spec for the AU keyword-level CPA dashboard: methodology, views, interpretation, and data quality notes."
---
<!-- DOC-0365 | duck_id: reporting-au-keyword-cpa-dashboard -->

# AU Keyword CPA Dashboard

This document is the reference spec for the AU keyword-level CPA dashboard. It serves Lena Zak (AU PS lead) and the broader AU paid search team by defining the dashboard's methodology, structure, interpretation rules, and data quality constraints. After reading it, you should be able to pull the weekly data, populate each view correctly, interpret the output, and know when to escalate.

## Context

Lena requested weekly CPA review at the keyword level to address three priorities: keyword CPC/CPA investigation, keyword-to-product mapping, and Polaris migration tracking. These priorities emerged from the Brandon sync on 2026-03-23 and reflect AU's need for granular cost visibility as the market transitions bid strategies and landing pages simultaneously.

The dashboard provides a rolling 4-week view of AU keyword performance, highlighting CPA outliers and trends. It is one of the core reporting artifacts for the AU market, alongside the WBR callout pipeline (see [WBR Callout Guide](wbr-callout-guide)).

## How the data is sourced and refreshed

The AU keyword CPA dashboard pulls from database registration data, not from Google Ads platform conversions. This is a deliberate choice. Google Ads conversion tracking on the AU account has historical gaps that make platform-reported conversions unreliable for CPA calculation. Database registrations are the source of truth for AU conversions across all PS reporting.

The refresh cadence is weekly, driven by a manual export from Google Ads. The AU account does not have Google Ads API access, which is a known structural limitation. Each week, the operator exports keyword-level data (impressions, clicks, cost, CPC) from Google Ads, then joins it against database registration data to calculate CPA. The export window covers Monday through Sunday of the prior week. The joined dataset is processed into the summary views described below.

The dashboard ingester tool (device.md tool #1, status: BUILT) could eventually automate the export-to-summary pipeline if the weekly Excel export follows a consistent column format. Until API access is granted or the ingester is integrated, the manual pull remains the production path.

## How metrics are defined

**CPA (Cost Per Acquisition):** total Google Ads cost for a keyword divided by the number of database registrations attributed to that keyword in the same period. Formula: CPA = Cost / DB Registrations. This is not the Google Ads "Cost / conv." column, which uses platform conversions.

**CPC (Cost Per Click):** total cost divided by total clicks, pulled directly from Google Ads. Formula: CPC = Cost / Clicks.

**Registration:** a completed registration event recorded in the database and attributed to the keyword via last-click. Only database registrations count. Google Ads "Conversions" column is not used.

**Match type rollup:** keywords are reported at the match type level (exact, phrase, broad). The Top 20 views show each keyword-match type combination as a separate row. A keyword appearing in both exact and broad match appears twice.

**4-week rolling calculation:** each metric is averaged across the most recent four complete weeks. Week-over-week (WoW) change compares the current week's value to the prior week's value, not to the 4-week average.

**AU CPA target:** $140. Historical AU CPA has run $120 to $180 depending on the week and keyword mix. Brand CPA typically runs around $80. Non-brand CPA typically runs $200 or higher.
<!-- TODO: cite AU CPA target $140 source — eyes.md Market Health → AU or current.md -->

## Dashboard structure

The dashboard contains four views, each serving a different analytical need.

### How to read the Top 20 by CPA view

This is the primary action view. It ranks the 20 highest-CPA keywords (with their match type) over the most recent week. Each row shows keyword, match type, clicks, registrations, CPA, CPC, and WoW CPA change.

| Keyword | Match Type | Clicks | Regs | CPA | CPC | WoW Change | Action |
|---------|-----------|--------|------|-----|-----|------------|--------|

The Action column is the decision output. Thresholds for action:

| CPA Range | Volume Context | Recommended Action |
|-----------|---------------|-------------------|
| Above $200 | 50+ clicks/week | Candidate for pause or negative keyword addition |
| $140 to $200 | 50+ clicks/week | Monitor for two weeks, check landing page CVR |
| Below $140 | Any | Performing at or below target, no action needed |
| Above $200 | Under 50 clicks/week | Low volume, CPA is noisy. Flag but do not act on one week |

The key interpretation: high CPA with high volume is the urgent signal. High CPA with low volume is statistical noise until it persists for three or more weeks. Always check whether a CPA spike is driven by a cost increase (CPC up) or a conversion drop (registrations down), because the response differs. A CPC spike points to auction pressure. A registration drop points to landing page or attribution issues.

### How to read the Top 20 by volume view

This view ranks the 20 highest-click keywords. It answers a different question: where is the budget going? A keyword can have acceptable CPA but consume a disproportionate share of spend. This view surfaces those cases.

| Keyword | Match Type | Clicks | Regs | CPA | CPC | WoW Change |
|---------|-----------|--------|------|-----|-----|------------|

Look for keywords where clicks are high but registrations are low relative to the CPA target. A keyword with 500 clicks and 1 registration is a $X,000 CPA problem regardless of what the Top 20 by CPA view shows, because the CPA view caps at 20 rows and may miss high-volume, moderate-CPA keywords that are still inefficient in absolute dollar terms.

### How to read the CPA trend chart

The 4-week rolling CPA trend is split by campaign type: Brand and Non-Brand. A horizontal target line at $140 provides the reference point. Brand CPA should consistently run below target (around $80). Non-Brand CPA will typically run above target ($200+), and the trend direction matters more than the absolute level.

What to watch for: a sustained upward trend in NB CPA over three or more weeks suggests bid strategy or competitive pressure. A sudden Brand CPA spike above $120 is unusual and warrants immediate investigation, as Brand is typically stable. Divergence between Brand and NB trends may indicate budget reallocation or match type bleed.

### How to use the keyword-to-product mapping

This view maps keyword themes to product categories, landing pages, and conversion rates.

| Keyword Theme | Product Category | Landing Page | CVR | Notes |
|--------------|-----------------|--------------|-----|-------|

The Polaris Brand LP migration is currently active and affects this mapping directly. Brand keywords are being rerouted to new Polaris landing pages, which changes the keyword-to-product relationship. During the migration period, CVR fluctuations on Brand keywords are expected and should not trigger immediate action. Flag them for tracking but wait for two full weeks post-migration before drawing conclusions.

## What can go wrong with this data

Three data quality risks are worth naming explicitly.

First, the manual pull introduces human error risk. A missed week, a wrong date range filter, or an incorrect column mapping will silently corrupt the dashboard. The operator should verify row counts and total cost against the Google Ads UI summary before processing. There is no automated validation today.

Second, conversion attribution uses database registrations joined to Google Ads keyword data via last-click. This join depends on consistent UTM tagging and session tracking. If UTM parameters are stripped or modified (common with certain redirect chains), registrations will not attribute to the correct keyword. The result is artificially inflated CPA on affected keywords and unattributed registrations that appear nowhere in the dashboard. When total dashboard registrations diverge from total AU DB registrations by more than 10%, investigate the attribution pipeline before interpreting keyword-level CPA.
<!-- TODO: cite attribution gap threshold — is 10% the right number or should this be calibrated from historical data? -->

Third, the weekly cadence means mid-week surprises are invisible until the following Monday. If a keyword's CPA spikes on Tuesday due to a competitor entering the auction, the dashboard will not surface it until the next weekly pull. For time-sensitive issues, the Google Ads UI remains the real-time monitoring tool, with the caveat that its conversion data is unreliable for AU.

Match type nuances also matter. Broad match keywords can trigger on queries far outside the intended theme. A broad match keyword with high CPA may be serving irrelevant queries rather than performing poorly on its intended traffic. Check the search terms report alongside the CPA dashboard before pausing a broad match keyword.

## Transition context

The AU market is currently transitioning from Richard Williams' direct ownership to Megan Oshry's team. This dashboard is one of the artifacts included in that handoff. Megan's team will own the weekly pull, interpretation, and escalation going forward. For questions about dashboard methodology, contact Richard. For questions about AU keyword actions and escalations, contact Megan's team or Lena Zak directly.

## Delivery

The dashboard is delivered as an Excel or Quip table (per Lena's preference), on a weekly cadence, before the AU sync meeting. The owner of the weekly pull is currently transitioning from Richard to Megan's team.

## Automation path

The dashboard ingester tool (device.md tool #1) is built and ready for integration. If the weekly Excel export follows a consistent column format, the ingester can auto-generate the summary views. The integration path requires: (1) standardizing the export template, (2) configuring the ingester's column mapping, and (3) validating output against one manual pull. Until Google Ads API access is granted for the AU account, the ingester would automate the processing step but not the export step.

## Next steps (historical context)

These steps were defined during the design phase in March 2026. The first data pull and template build should be complete by now. Retained here for provenance.

- Pull first week's data
- Build template in Excel/Quip
- Share with Alexis for feedback
- Present to Lena at next AU sync

## Sources

- Lena wants weekly CPA review: ~/shared/context/active/current.md, AU Paid Search Optimization
- Lena's 3 priorities: ~/shared/context/active/current.md, AU CPC Benchmark Response (Brandon sync 3/23)
- AU CPA target $140: ~/shared/context/body/eyes.md, Market Health, AU
- Dashboard ingester tool: ~/shared/context/body/device.md, Tool Factory, #1 Dashboard ingester (BUILT)
- AU uses DB registrations not Google Ads conversions: ~/shared/context/active/current.md, AU Paid Search Optimization
- AU transition to Megan Oshry's team: ~/shared/context/active/current.md, AU market transition

## Related

- [WBR Callout Guide](wbr-callout-guide)
- [Device: Tool Factory](~/shared/context/body/device.md)
- [Eyes: Market Health](~/shared/context/body/eyes.md)

<!-- AGENT_CONTEXT
machine_summary: "Reference spec for the AU keyword-level CPA dashboard serving Lena Zak. Defines methodology (DB registrations as conversion source, not Google Ads), four dashboard views (Top 20 by CPA, Top 20 by volume, CPA trend, keyword-to-product mapping), interpretation thresholds ($140 target, $200+ action trigger), and data quality risks (manual pull, attribution gaps, weekly cadence). AU market transitioning to Megan Oshry's team."
key_entities: ["AU", "Lena Zak", "Megan Oshry", "Alexis Eck", "keyword CPA", "CPC", "dashboard ingester", "Google Ads", "Polaris", "database registrations"]
action_verbs: ["pull", "build", "interpret", "escalate", "validate", "flag", "pause"]
update_triggers: ["weekly AU data pull", "Lena feedback on format", "dashboard ingester integration", "Polaris migration completion", "AU transition to Megan complete", "Google Ads API access granted"]
-->
