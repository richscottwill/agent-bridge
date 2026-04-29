// ============================================================
// AGENT BRIDGE — Apps Script Automation Layer
// ============================================================
// Persistent automation on Google infrastructure.
// Runs even when Kiro and the swarm are offline.
// ============================================================

var SPREADSHEET_ID = "1IlM43kzxw8Vlu6aUWXUV1dr7ZIF7O7H2bD5x3kaKIHg";
var RICHARD_EMAIL = "prichwil@amazon.com";

// ── BUS POLLER (A1) — runs hourly ──

function pollBus() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var bus = ss.getSheetByName("bus");
  if (!bus) return;

  var data = bus.getDataRange().getValues();
  if (data.length < 2) return;

  var headers = data[0];
  var statusCol = headers.indexOf("status");
  var priorityCol = headers.indexOf("priority");
  var targetCol = headers.indexOf("target");
  var subjectCol = headers.indexOf("subject");
  var sourceCol = headers.indexOf("source");
  var typeCol = headers.indexOf("type");

  var urgent = [];
  var high = [];
  var pendingCount = 0;

  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    if (row[statusCol] !== "pending") continue;
    pendingCount++;

    var target = row[targetCol];
    if (target !== "kiro" && target !== "*") continue;

    if (row[priorityCol] === "urgent") {
      urgent.push({source: row[sourceCol], type: row[typeCol], subject: row[subjectCol]});
    } else if (row[priorityCol] === "high") {
      high.push({source: row[sourceCol], type: row[typeCol], subject: row[subjectCol]});
    }
  }

  if (urgent.length > 0 || high.length > 0) {
    var body = "Agent Bridge Bus Alert\n\n";
    body += "Pending messages for kiro: " + pendingCount + "\n\n";

    if (urgent.length > 0) {
      body += "URGENT:\n";
      for (var j = 0; j < urgent.length; j++) {
        body += "  [" + urgent[j].type + "] " + urgent[j].source + ": " + urgent[j].subject + "\n";
      }
      body += "\n";
    }

    if (high.length > 0) {
      body += "HIGH PRIORITY:\n";
      for (var k = 0; k < high.length; k++) {
        body += "  [" + high[k].type + "] " + high[k].source + ": " + high[k].subject + "\n";
      }
    }

    body += "\nOpen the bridge sheet to review.";

    MailApp.sendEmail({
      to: RICHARD_EMAIL,
      subject: "[Agent Bridge] " + (urgent.length > 0 ? "URGENT" : "High Priority") + " - " + (urgent.length + high.length) + " message(s)",
      body: body
    });

    Logger.log("Emailed: " + urgent.length + " urgent, " + high.length + " high");
  } else {
    Logger.log("No urgent/high messages. " + pendingCount + " pending total.");
  }
}


// ── STALENESS CHECKER (A3) — runs daily at 6am PT ──

function checkStaleness() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var context = ss.getSheetByName("context");
  var bus = ss.getSheetByName("bus");
  if (!context || !bus) return;

  var data = context.getDataRange().getValues();
  if (data.length < 2) {
    writeNudge(bus, "No context snapshots found. Kiro needs to push initial snapshots.");
    return;
  }

  var headers = data[0];
  var tsCol = headers.indexOf("timestamp");
  var organCol = headers.indexOf("organ");

  var now = new Date();
  var staleThreshold = 48 * 60 * 60 * 1000;
  var latestByOrgan = {};

  for (var i = 1; i < data.length; i++) {
    var organ = data[i][organCol];
    var ts = new Date(data[i][tsCol]);
    if (!latestByOrgan[organ] || ts > latestByOrgan[organ]) {
      latestByOrgan[organ] = ts;
    }
  }

  var staleOrgans = [];
  for (var organ in latestByOrgan) {
    var age = now - latestByOrgan[organ];
    if (age > staleThreshold) {
      staleOrgans.push(organ + " (" + Math.round(age / (60 * 60 * 1000)) + "h old)");
    }
  }

  if (staleOrgans.length > 0) {
    writeNudge(bus, "Stale context: " + staleOrgans.join(", ") + ". Push fresh snapshots.");
  } else {
    Logger.log("All context snapshots fresh.");
  }
}


// ── HEARTBEAT MONITOR (A7) — runs every 6 hours ──

function heartbeatMonitor() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var registry = ss.getSheetByName("registry");
  if (!registry) return;

  var data = registry.getDataRange().getValues();
  if (data.length < 2) return;

  var headers = data[0];
  var lastSeenCol = headers.indexOf("last_seen");
  var statusCol = headers.indexOf("status");
  var agentCol = headers.indexOf("agent_id");

  var now = new Date();
  var offlineThreshold = 24 * 60 * 60 * 1000;

  for (var i = 1; i < data.length; i++) {
    var lastSeen = new Date(data[i][lastSeenCol]);
    var age = now - lastSeen;
    if (age > offlineThreshold && data[i][statusCol] === "online") {
      registry.getRange(i + 1, statusCol + 1).setValue("offline");
      Logger.log("Marked " + data[i][agentCol] + " offline (" + Math.round(age / (60 * 60 * 1000)) + "h)");
    }
  }
}


// ── FORM RESPONSE ROUTER (A2) ──

function onFormSubmit(e) {
  if (!e || !e.response) return;

  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var bus = ss.getSheetByName("bus");
  if (!bus) return;

  var items = e.response.getItemResponses();
  var payload = {};
  for (var i = 0; i < items.length; i++) {
    payload[items[i].getItem().getTitle()] = items[i].getResponse();
  }

  var msgId = "form-" + Utilities.formatDate(new Date(), "UTC", "yyyyMMddHHmmss");
  var now = Utilities.formatDate(new Date(), "UTC", "yyyy-MM-dd'T'HH:mm:ss'Z'");

  bus.appendRow([
    msgId, now, "google-form", "kiro", "context_push", "normal",
    "Form submission",
    JSON.stringify(payload),
    "pending", "", ""
  ]);

  Logger.log("Form response routed: " + msgId);
}


// ── HELPER ──

function writeNudge(busSheet, message) {
  var msgId = "script-" + Utilities.formatDate(new Date(), "UTC", "yyyyMMddHHmmss");
  var now = Utilities.formatDate(new Date(), "UTC", "yyyy-MM-dd'T'HH:mm:ss'Z'");

  busSheet.appendRow([
    msgId, now, "apps-script", "kiro", "request", "normal",
    message,
    JSON.stringify({source: "apps-script-automation"}),
    "pending", "", ""
  ]);
}


// ── RUN ONCE: Create all triggers ──

function createTriggers() {
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i]);
  }

  ScriptApp.newTrigger("pollBus").timeDriven().everyHours(1).create();
  ScriptApp.newTrigger("checkStaleness").timeDriven().atHour(6).everyDays(1).create();
  ScriptApp.newTrigger("heartbeatMonitor").timeDriven().everyHours(6).create();
  ScriptApp.newTrigger("checkRequests").timeDriven().everyHours(1).create();

  Logger.log("Triggers created: pollBus (1h), checkStaleness (daily 6am), heartbeatMonitor (6h), checkRequests (1h)");
}


// ── REQUEST NOTIFIER — runs hourly with pollBus ──
// Checks the requests tab for new requests (status = "idea" or "pending")
// that haven't been emailed yet. Emails Richard, marks as "notified".

function checkRequests() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var req = ss.getSheetByName("requests");
  if (!req) return;

  var data = req.getDataRange().getValues();
  if (data.length < 2) return;

  var headers = data[0];
  var statusCol = headers.indexOf("status");
  var nameCol = headers.indexOf("name");
  var typeCol = headers.indexOf("type");
  var locationCol = headers.indexOf("location");
  var purposeCol = headers.indexOf("purpose");
  var sourceCol = headers.indexOf("source");

  var newRequests = [];

  for (var i = 1; i < data.length; i++) {
    var status = data[i][statusCol];
    if (status === "idea" || status === "pending") {
      newRequests.push({
        row: i + 1,
        source: data[i][sourceCol],
        type: data[i][typeCol],
        name: data[i][nameCol],
        location: data[i][locationCol],
        purpose: data[i][purposeCol]
      });
    }
  }

  if (newRequests.length > 0) {
    var body = "Agent Bridge — File/Tab Creation Requests\n\n";
    body += newRequests.length + " request(s) need your action:\n\n";

    for (var j = 0; j < newRequests.length; j++) {
      var r = newRequests[j];
      body += (j + 1) + ". [" + r.type + "] " + r.name + "\n";
      body += "   Location: " + r.location + "\n";
      body += "   Purpose: " + r.purpose + "\n";
      body += "   From: " + r.source + "\n\n";
    }

    body += "Action: Create the files/tabs in Google Drive, then update status to 'created' in the requests tab.\n";
    body += "Sheet: agent bridge sheet > requests tab";

    MailApp.sendEmail({
      to: RICHARD_EMAIL,
      subject: "[Agent Bridge] " + newRequests.length + " file request(s) need your action",
      body: body
    });

    // Mark as notified
    for (var k = 0; k < newRequests.length; k++) {
      req.getRange(newRequests[k].row, statusCol + 1).setValue("notified");
    }

    Logger.log("Emailed " + newRequests.length + " file requests.");
  }
}


// ── MANUAL TEST ──

function testAll() {
  pollBus();
  checkStaleness();
  heartbeatMonitor();
  checkRequests();
  Logger.log("All checks complete.");
}
