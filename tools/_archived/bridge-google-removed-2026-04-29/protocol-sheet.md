<!-- DOC-0422 | duck_id: tool-protocol-sheet -->
# Protocol Sheet — Paste into "protocol" tab of agent bridge spreadsheet
# Each section below becomes rows in the sheet. Column A = section, Column B = content.
# The swarm agent should read this sheet FIRST before doing anything else.

## HOW THIS BRIDGE WORKS

section,content
OVERVIEW,"This spreadsheet is a message bus between two AI systems: Kiro (Amazon AgentSpace) and the Swarm (Google AI Studio / personal agents). Richard owns both. Neither system can talk to the other directly — this sheet is the only communication channel."
YOUR JOB,"When you open this sheet: (1) Read this protocol tab first. (2) Check the bus tab for messages where target = your agent_id or target = *. (3) If status = pending and the message is for you, do the work. (4) Write your response back to the bus tab. (5) Update the original message status to complete."
NEVER DO,"Never delete rows. Never rename sheets or columns. Never change another agent's messages. Never set status to anything other than: pending, claimed, complete, failed."

## BUS TAB — MESSAGE FORMAT

section,content
BUS COLUMNS,"msg_id | timestamp | source | target | type | priority | subject | payload | status | response_to | expires"
msg_id,"Unique ID. Format: {agent_id}-{number}. Example: kiro-015 or swarm-003. When you write a message, use your agent_id as prefix."
timestamp,"ISO 8601 UTC. Example: 2026-03-30T15:00:00Z"
source,"Who sent this message. Your agent_id when you write."
target,"Who should read this message. Use the agent_id of the recipient. Use * for broadcast (everyone reads it). Use richard for messages only Richard should see."
type,"What kind of message this is. See MESSAGE TYPES below."
priority,"urgent = needs action within 1 hour. high = needs action today. normal = needs action this week. low = informational only."
subject,"One-line summary. Keep under 80 characters. Be specific: 'AU keyword CPA data for Q1' not 'data request'."
payload,"JSON object with details. Keep it flat — no nested objects if you can avoid it. Example: {""market"":""AU"",""metric"":""CPA"",""period"":""Q1 2026"",""value"":""$134""}"
status,"pending = waiting for someone to act. claimed = someone is working on it. complete = done. failed = could not complete (explain in a response message)."
response_to,"If this message is a response to another message, put the original msg_id here. Leave blank for new messages."
expires,"Optional. ISO timestamp after which this message should be ignored. Leave blank if no expiry."

## MESSAGE TYPES — WHAT EACH ONE MEANS AND WHAT TO DO

section,content
type: request,"Someone is asking you to do something. Read the subject and payload. Do the work. Then write a NEW row with type: response, response_to: the original msg_id, and your results in the payload. Then update the original message status to complete."
type: response,"This is an answer to a previous request. Check response_to to find the original. Read the payload for the results. No action needed unless the response asks a follow-up question."
type: context_push,"Informational update about the system state. Read and absorb — use this to stay current on what Kiro knows. No response needed."
type: announce,"Broadcast notification. Read only. No response needed."
type: heartbeat,"Agent health check. Ignore unless you are monitoring which agents are online."

## HOW TO RESPOND TO A REQUEST — STEP BY STEP

section,content
STEP 1,"Find the message in the bus tab. Confirm target matches your agent_id (or is *)."
STEP 2,"Read the subject and payload carefully. The payload JSON contains the details of what's being asked."
STEP 3,"Change the status cell of that row from pending to claimed. This tells other agents you're working on it."
STEP 4,"Do the work. Research, write, analyze — whatever the request asks for."
STEP 5,"Write a NEW row at the bottom of the bus tab with: your agent_id as source, the requester's agent_id as target, type = response, the original msg_id in response_to, your results in the payload JSON, status = complete."
STEP 6,"Go back to the original request row and change its status from claimed to complete."
EXAMPLE REQUEST,"msg_id: kiro-015 | source: kiro | target: swarm | type: request | subject: Need AU Q1 keyword CPA data | payload: {""market"":""AU"",""period"":""Q1""} | status: pending"
EXAMPLE RESPONSE,"msg_id: swarm-001 | source: swarm | target: kiro | type: response | subject: AU Q1 keyword CPA data | payload: {""market"":""AU"",""avg_cpa"":""$134"",""top_keyword"":""business supplies"",""note"":""CPA trending down since OCI launch""} | status: complete | response_to: kiro-015"

## CONTEXT TAB — WHAT KIRO KNOWS

section,content
CONTEXT PURPOSE,"Kiro pushes summaries of its internal knowledge here so the swarm can stay aligned. Each row is a snapshot of one 'organ' (knowledge domain). Read the latest snapshot per organ to understand current state."
CONTEXT COLUMNS,"snapshot_id | timestamp | source | organ | summary | detail"
organ: brain,"Decision principles and strategic priorities. What Richard values, how he decides, the Five Levels (his career growth framework). Read this to understand WHAT MATTERS."
organ: eyes,"Market performance metrics — registrations, CPA, spend, competitors, OCI status for US/UK/DE/FR/IT/ES/CA/JP/AU/MX. Read this before doing any market analysis."
organ: hands,"Active task list — what Richard is working on this week, what's overdue, what's blocked. Read this to understand WHAT'S HAPPENING NOW."
organ: memory,"Relationship graph — who Richard works with, their roles, communication tone, meeting dynamics. Read this before drafting any communication."
organ: amcc,"Willpower tracker — the 'hard thing' Richard is supposed to be doing, his streak of consecutive days doing it, resistance patterns. Read this to understand his current struggle."
organ: device,"Automation and delegation status — what tools exist, what's delegated to whom, what's proposed. Read this to avoid duplicating work."

## REGISTRY TAB — WHO'S ONLINE

section,content
REGISTRY PURPOSE,"Tracks which agents are active. Update your row when you start working. The heartbeat monitor marks agents offline after 24 hours of silence."
REGISTRY COLUMNS,"agent_id | platform | capabilities | tools | last_seen | status | notes"
HOW TO REGISTER,"Add a row with your agent_id, platform (e.g. google-ai-studio), what you can do (capabilities), what tools you have access to (tools), current timestamp, status = online, and any notes."
HEARTBEAT,"Update your last_seen timestamp whenever you do work. If you don't update for 24 hours, the system marks you offline."

## RULES

section,content
RULE 1,"Read this protocol tab every time you start a new session. Don't assume you remember — re-read."
RULE 2,"Never modify rows you didn't create, except to update status on messages targeted at you."
RULE 3,"Always use JSON for the payload column. Keep it flat. No nested objects."
RULE 4,"When responding, always fill in response_to with the original msg_id. This is how messages get linked."
RULE 5,"If you can't complete a request, write a response with status: failed and explain why in the payload."
RULE 6,"Keep subjects short and specific. The subject is what humans scan — make it useful."
RULE 7,"Don't create new sheets or rename existing ones. The structure is fixed."
RULE 8,"If you need Richard to create a file or resource, use the requests tab — don't put it in the bus."
RULE 9,"Write for a reader who has no context. Every response payload should be self-contained — don't reference things only you can see."
RULE 10,"Timestamps are always UTC. Always."
