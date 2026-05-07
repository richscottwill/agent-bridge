---
audience: amazon-internal
creator: Richard Williams
doc_type: document
last_modified: 2025-10-06
mirror_date: 2026-04-10
owner: Richard Williams
quip_folder: Onboarding/Account Best Practice
quip_id: ZfB9AA8dyA6
source_url: https://quip-amazon.com/ZfB9AA8dyA6
status: DRAFT
title: OCI/ROAS bid strategies
topics:
- onboarding
- best-practices
- account-management
backfill_status: backfilled
---

# OCI/ROAS bid strategies
The main objective is to maximize AB registrations using the OCI value as a proxy to guide optimizations. Managing ROAS bid strategy is not passive. (below)

## **Setting and adjusting ROAS targets**
This is our primary lever for controlling performance. The target we set directly tells the algorithm the value we expect back for every dollar spent.
### **Tactic #1: Set a realistic initial baseline to start**
Base starting ROAS target on historical performance data.
**Action**: Observe actual ROAS data, and then set the bid strategy target to 80%-90% of observed ROAS depending on stability/confidence in the campaigns. (80% for lower confidence, and 90% for higher)
**Example**: If baseline data shows 20% ROAS from $1,500 value / $300 spend, then set target at 16% to test the bid strategy. Setting a higher target than this (e.g., 50% target ROAS) will likely constrict volume because the bid strategy will struggle to find conversions at that efficiency.

After the baseline is set, work through the Tactics flow below to manage for efficiency and results.
### **Tactic #2: Update budgets based on ie%CCP **
Each week, you will either be under or over your ie%CCP target for the week/month. The first change to think about is adjusting Nonbrand budgets to meet that threshold based on potential registrations. This allows you to shift the mix of budgets to maximize your registration potential, and at the same time, address your ie%CCP efficiency situation.
**Action**: The simplest approach will be to adjust budgets so that you will be within range of your efficiency target overall, wait a week, then determine whether you need more/less efficient spend.
### **Tactic #3: Change ROAS target with smaller, incremental adjustments**
Large, sudden changes to your ROAS target can push the campaign back into learning period. Sometimes this is justified, but keep in mind that you should treat adjustments as a dial.
#### ** Scenario 1 (Scaling Volume)**
Your campaign is consistently above its 20% ROAS target and is not limited by budget. You want to drive more registrations, even if it means a slightly lower efficiency.
**Action:** Lower the ROAS target to 17% (a ~15% decrease). This tells the bid strategy that it can bid more aggressively to enter more auctions and capture more registration volume. (even at a lower efficiency)
#### **Scenario 2 (Improving efficiency)**
Your campaign is spending its budget but only achieving a 15% ROAS, missing its 20% target.
**Action:** You can raise the ROAS target to 24% (a 20% increase). Both will force the algorithm to be more selective, focusing only on auctions where it predicts a higher probability of converting at your desired efficiency.
## After the above basics are met
### **Tactic #4: Avoid budget constraints**
A campaign that is "Limited by budget" prevents ROAS from working properly.
**Action:** If a campaign hits its ROAS target and is limited by budget, increase the budget. If you cannot increase the budget, you must raise the ROAS target to force the algorithm to be more efficient and stay within the current budget.
####  Scenario: (Constrained budget)
GA campaigns have a 25% ROAS target and a $1,000/day shared budget.
It hits or exceeds the target ROAS consistently, but campaigns within are "Limited by budget."
**Action:** Two options, first would be the opportunity to increase the daily budget at the current ROAS efficiency, and the second would be to raise the ROAS target to force the algorithm to be more efficient.
### **Tactic #5: Consolidate campaigns**
We want to make it easier for our bid strategies to work for our goals. Best Practice says that breaking up our keywords into many small ad groups/campaigns will only make the algorithm less effective. Suggestion is to group campaigns with similar terms and ROAS potential to help things scale.
**Action:** Best practice would be a minimum of 30-50 conversions per campaign per month (even with our ROAS-oriented bid strategies.) If a campaign is not meeting this threshold, consider merging with another, similar one.
Note: Duplication/overlap present among campaigns between portfolios

## Resources/Links
OCI planning document: [OCI Planning - Phased Rollout][1]

[1]: https://quip-amazon.com/UNlJAiiYljjd
