---
audience: amazon-internal
creator: Richard Williams
doc_type: document
last_modified: 2024-09-04
mirror_date: 2026-04-10
owner: Richard Williams
quip_folder: root
quip_id: FZQ9AARARAN
source_url: https://quip-amazon.com/FZQ9AARARAN
status: DRAFT
title: MBet Process Improvement
topics:
- process
- finance
- po-management
backfill_status: backfilled
---

# MBet Process Improvement
### Next Steps
* Ben to speak with MBet team on:
 * Taking on additional responsibility
 * Confirming timeline for MBet automation rollout (last update Q4)
* York to speak with XCM about AB approval to use PAS
* Brandon to speak to Todd on:
 * Allowing higher-total POs (>$5M) to reduce total PO requirements (will require L10 Finance approval, but will not be sent to Shelley)
 * Alignment to PAS (will need Shelley approval for overall AB budget)
* Outstanding:
 * Identify how we can show 2024 spend accurately vs OP2 (regardless of Y23 PO closures, which do not represent additional funds in Y24)
 * Create more reliable ASP inputs, showing closer-to-accurate spend within the spending month: how do we shift ASP timing to avoid high-spend credits in the following month (ie. setup ASP at beginning of month, update by 26th, is a EOM update still needed?)

### **Pain Points & Solutions:**

Problem - Prolonged MBet Process: The team has historically opened Coupa directly, we are now inputting into MBet with an offshore team translating that into Coupa. This has caused additional work (as we can't manage Coupa directly), introduced lag time (+2 days), and has introduced errors.
Solution:
 * Should be out of MBet beta by now, but this has been pushed out to Q4 based on resource constraints. Ben to ask Nishant for updated timing.
 * Go back to using Coupa directly: This will allow us to simply copy past POs (not available in MBet) & avoid lag and errors due to manual intervention from the offshore MBet team
 * Increase value of time spent in MBet:
  * Roll out new capabilities within MBet, including R&O/MSP integration, ability to Edit PO amounts, ability to view approval chains/progress
  * Remove distribution requirement or create automation to sync into MSP
  * Allow Approvers to see a combined list of related POs with ability to manage in bulk
 * Increase offshore responsibilities: Ben will talk to them to see if they can take on additional responsibility
  * Require offshore team to work from bulksheets for creation of MSP/Coupa entries (PS team solely reviews/approves).
  * Offshore team follows process to ping lagging Approvers (currently done by PS team)
   * _Can provide MBet team list of who needs to be added based on cost-center (SSR/CPS) and PO amount_
   * Coupa reminder after 2 days, Slack/Chime reminder on 3rd day, escalation to PO Owner 5th day
  * Offshore team applies correct chains and manually add approvers missing (ie. Christine Vix always needs to be manually added)
  * If switching to Smartsheet, can offshore team input Coupa link?

Problem - Volume of POs: 1 PO per market, monthly or quarterly per Purpose leads to our team managing **84 POs annually **- easily accounting for** 126 hours of 0-value work**, along with managing stakeholders who open POs in alternate markets (ie. CA, JP, MX). Aside from the volume of POs, each requires long strings of approvals, typically 10 approvers often taking 3+ weeks with constant outreach by the PS team. Considering these budgets were approved and assigned in OP2, this process seems duplicative and unnecessary.
Solution:
 * ​
 * Reduce approver quantity and levels when approved in OP2. (ie. L10 approval not needed for OP2 budgets - approved by L10 earlier in the year)
  * [York] has pushed "pre-approved spend" (PAS). This is requesting Russ-level approval upon OP2 even if it's $100M. Then POs only need a Finance and Business observer (not approver). However, it is up to XCM discretion as to whether this is available for us - we've been trying to get this approval for >1yr. We may have more leverage to be PAS next year (as Stores are being consolidated?). York will begin discussions with XCM to start getting this through & pitching AB as a test case.
 * Will POs >$5M go to Shelley now that Todd is L10? Yes, it should stop at Todd, but will also go to a Finance L10. Brandon to ask Todd if he's aligned to doing this.

Problem - MSP / R&O disparity: The R&O does not match MSP inputs. The team has MSP inputs completed by the 15th, however, The R&O is not picking this up. Has the timing/process changed? There shouldn't be tech issues [York], but this can also be impacted by prior year POs impacting current year totals.
Finance can help
Solution: Align on appropriate timing for MSP inputs &/or alter R&O process to utilize MSP.
---
_Separate conversation from MSP - may need to setup additional meeting_

Problem - PO budget accrual: We open POs with buffer included since PS is a variable channel and costs may fluctuate based on cost vs efficiency. Because of this, we expect unutilized funds associated to every PS PO. However, when closing these POs, the unutilized funds negate actual spend when Finance docs are created. For ex, in August we may plan to spend $1M, and open an Aug PO for $1.2M to ensure funds are available in case efficiencies are hit and increased opportunity to spend is available. If actualized spend is $1M and we soft-close the PO, Finance will reflect spend of $800k ($1M - $.2M) as the total spend.
Solution:
 * ​
 * [York] Switch to SmartSheets process
  * If creating 1PO per budget line, then we won't have to input into R&O
* ​
OLD NOTES
 * If adding approvers through Mbet once approval chain has begun, approvals are cleared and restarted from first approver. This issue does not occur through Coupa.
  * Opp: If approver updates are needed, offshore team to submit via Coupa as to avoid restarting approval chains
