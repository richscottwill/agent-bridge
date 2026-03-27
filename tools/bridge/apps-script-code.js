// ═══════════════════════════════════════════════════════════
// AGENT BRIDGE — Apps Script Automation Suite
// ═══════════════════════════════════════════════════════════
// Deploy to: agent bridge script (1Y03Qay3ZbP8eGb3oAkvpxkYu-PVixuAwpDheZwUuUknSyMzWXJ8ICz5a)
// After deploying, run setupTriggers() once to create all time-driven triggers.
// Then run setupFormTrigger() to connect the daily check-in form.
//
// FILES TO CREATE IN APPS SCRIPT EDITOR:
//   Config.gs, A1_BusPoller.gs, A2_FormRouter.gs, A3_StalenessChecker.gs,
//   A4_StreakTracker.gs, A5_WeeklyDigest.gs, A7_HeartbeatMonitor.gs, Setup.gs

// ═══ Config.gs ═══
const CONFIG = {
  SPREADSHEET_ID: "1IlM43kzxw8Vlu6aUWXUV1dr7ZIF7O7H2bD5x3kaKIHg",
  DOC_ID: "1koJV8a4Ig9BBDbrtQl-w8L4-2bUrz8lGwxUxEfIgQj8",
  FORM_ID: "12NS7rUXOK7athQgpW2B-mqN0sCMCCNs51DyI9wlceNA",
  RICHARD_EMAIL: "", // Set to receive urgent message notifications
  STALENESS_HOURS: 48,
  HEARTBEAT_HOURS: 24,
};
function getSheet(name){return SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID).getSheetByName(name)}
function now(){return new Date().toISOString().replace(/\.\\d{3}Z$/,"Z")}
function nextMsgId(prefix){return prefix+"-"+String(getSheet("bus").getLastRow()).padStart(3,"0")}
function appendToBus(source,target,type,priority,subject,payload,status,responseTo,expires){
  getSheet("bus").appendRow([nextMsgId(source),now(),source,target||"",type,priority||"normal",subject,JSON.stringify(payload||{}),status||"pending",responseTo||"",expires||""])
}

// ═══ A1_BusPoller.gs — Runs every hour ═══
function pollBus(){
  var bus=getSheet("bus"),data=bus.getDataRange().getValues();
  if(data.length<2)return;
  var h=data[0],si=h.indexOf("status"),pi=h.indexOf("priority"),subi=h.indexOf("subject"),srci=h.indexOf("source");
  var urgent=[],pending=0;
  for(var i=1;i<data.length;i++){
    if(data[i][si]==="pending"){pending++;if(data[i][pi]==="urgent"||data[i][pi]==="high")urgent.push({source:data[i][srci],subject:data[i][subi],priority:data[i][pi]})}
  }
  appendToBus("apps-script","*","heartbeat","low","Bus poll: "+pending+" pending, "+urgent.length+" urgent",{pendingCount:pending,urgentCount:urgent.length},"complete");
  if(urgent.length>0&&CONFIG.RICHARD_EMAIL){
    var body="Agent Bridge: "+urgent.length+" urgent message(s):\n\n";
    urgent.forEach(function(m){body+="  ["+m.priority+"] "+m.source+": "+m.subject+"\n"});
    GmailApp.sendEmail(CONFIG.RICHARD_EMAIL,"Agent Bridge: "+urgent.length+" urgent",body)
  }
}

// ═══ A2_FormRouter.gs — Triggered on form submit ═══
function onFormSubmit(e){
  var responses=e.response.getItemResponses(),payload={},subject="Form submission";
  responses.forEach(function(item){var t=item.getItem().getTitle(),a=item.getResponse();payload[t]=a;if(subject==="Form submission"&&typeof a==="string"&&a.length>0)subject=a.substring(0,80)});
  var msgType="request",priority="normal";
  if(payload["What is the hard thing today?"]||payload["Did you do the hard thing yesterday?"]){
    msgType="context_push";subject="Daily check-in: "+now().substring(0,10);priority="high";
    if(payload["Did you do the hard thing yesterday?"]==="Yes")updateStreak(true);
    else if(payload["Did you do the hard thing yesterday?"]==="No")updateStreak(false);
  }
  appendToBus("form","kiro",msgType,priority,subject,payload,"pending")
}

// ═══ A3_StalenessChecker.gs — Runs daily at 6am ═══
function checkStaleness(){
  var ctx=getSheet("context"),data=ctx.getDataRange().getValues();if(data.length<2)return;
  var h=data[0],ti=h.indexOf("timestamp"),oi=h.indexOf("organ");
  var cutoff=new Date();cutoff.setHours(cutoff.getHours()-CONFIG.STALENESS_HOURS);
  var latest={};
  for(var i=1;i<data.length;i++){var o=data[i][oi],ts=new Date(data[i][ti]);if(!latest[o]||ts>latest[o])latest[o]=ts}
  var stale=[];
  for(var organ in latest){if(latest[organ]<cutoff)stale.push({organ:organ,hoursAgo:Math.round((new Date()-latest[organ])/(1000*60*60))})}
  if(stale.length>0){
    appendToBus("apps-script","kiro","request","normal","Context stale: "+stale.map(function(o){return o.organ+" ("+o.hoursAgo+"h)"}).join(", "),{staleOrgans:stale},"pending")
  }
}

// ═══ A4_StreakTracker.gs — Called by form router ═══
function updateStreak(didHardThing){
  var ctx=getSheet("context"),data=ctx.getDataRange().getValues(),h=data[0];
  var oi=h.indexOf("organ"),di=h.indexOf("detail"),current=0,longest=0;
  for(var i=data.length-1;i>=1;i--){if(data[i][oi]==="amcc"){try{var d=JSON.parse(data[i][di]);current=d.streak||0;longest=d.longest_streak||0}catch(e){}break}}
  if(didHardThing){current++;if(current>longest)longest=current;
    ctx.appendRow(["ctx-amcc-streak-"+now().replace(/[:\-T]/g,"").substring(0,12),now(),"apps-script","amcc","Streak: "+current+" days. Longest: "+longest,JSON.stringify({streak:current,longest_streak:longest,did_hard_thing:true})]);
    if([5,10,21,30].indexOf(current)>=0)appendToBus("apps-script","kiro","announce","high","Streak milestone: "+current+" days!",{streak:current},"pending")
  }else{var prev=current;current=0;
    ctx.appendRow(["ctx-amcc-reset-"+now().replace(/[:\-T]/g,"").substring(0,12),now(),"apps-script","amcc","Streak RESET to 0. Previous: "+prev+". Longest: "+longest,JSON.stringify({streak:0,longest_streak:longest,previous_streak:prev})]);
    if(prev>0)appendToBus("apps-script","kiro","request","high","Streak reset from "+prev+" to 0",{streak:0,previous:prev},"pending")
  }
}

// ═══ A5_WeeklyDigest.gs — Runs Friday 5pm ═══
function generateWeeklyDigest(){
  var bus=getSheet("bus"),ctx=getSheet("context"),reg=getSheet("registry");
  var bd=bus.getDataRange().getValues(),cd=ctx.getDataRange().getValues(),rd=reg.getDataRange().getValues();
  var weekAgo=new Date();weekAgo.setDate(weekAgo.getDate()-7);
  var bh=bd[0],bti=bh.indexOf("timestamp"),bsi=bh.indexOf("status"),wk=0,wp=0,wc=0;
  for(var i=1;i<bd.length;i++){if(new Date(bd[i][bti])>weekAgo){wk++;if(bd[i][bsi]==="pending")wp++;if(bd[i][bsi]==="complete")wc++}}
  var ch=cd[0],coi=ch.indexOf("organ"),csi=ch.indexOf("summary"),latest={};
  for(var i=1;i<cd.length;i++){latest[cd[i][coi]]={summary:cd[i][csi]}}
  var txt="\n\n=== WEEKLY DIGEST "+now().substring(0,10)+" ===\nBus: "+wk+" messages ("+wp+" pending, "+wc+" complete)\nAgents: "+(rd.length-1)+"\n";
  for(var o in latest)txt+="["+o+"] "+latest[o].summary.substring(0,120)+"\n";
  DocumentApp.openById(CONFIG.DOC_ID).getBody().appendParagraph(txt);
  appendToBus("apps-script","*","announce","normal","Weekly digest: "+now().substring(0,10),{messages:wk,pending:wp},"complete")
}

// ═══ A7_HeartbeatMonitor.gs — Runs every 6 hours ═══
function checkHeartbeats(){
  var reg=getSheet("registry"),data=reg.getDataRange().getValues();if(data.length<2)return;
  var h=data[0],ai=h.indexOf("agent_id"),li=h.indexOf("last_seen"),si=h.indexOf("status");
  var cutoff=new Date();cutoff.setHours(cutoff.getHours()-CONFIG.HEARTBEAT_HOURS);
  var offline=[];
  for(var i=1;i<data.length;i++){if(data[i][si]==="online"&&new Date(data[i][li])<cutoff){reg.getRange(i+1,si+1).setValue("offline");offline.push(data[i][ai])}}
  if(offline.length>0)appendToBus("apps-script","*","announce","normal","Agents offline: "+offline.join(", "),{offlineAgents:offline},"pending")
}

// ═══ Setup.gs — Run once to create triggers ═══
function setupTriggers(){
  ScriptApp.getProjectTriggers().forEach(function(t){ScriptApp.deleteTrigger(t)});
  ScriptApp.newTrigger("pollBus").timeBased().everyHours(1).create();
  ScriptApp.newTrigger("checkStaleness").timeBased().atHour(6).everyDays(1).create();
  ScriptApp.newTrigger("generateWeeklyDigest").timeBased().onWeekDay(ScriptApp.WeekDay.FRIDAY).atHour(17).create();
  ScriptApp.newTrigger("checkHeartbeats").timeBased().everyHours(6).create();
  Logger.log("Triggers created: pollBus(1h), staleness(daily 6am), digest(Fri 5pm), heartbeats(6h)")
}
function setupFormTrigger(){
  ScriptApp.newTrigger("onFormSubmit").forForm(FormApp.openById(CONFIG.FORM_ID)).onFormSubmit().create();
  Logger.log("Form trigger created")
}
