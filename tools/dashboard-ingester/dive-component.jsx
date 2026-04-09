import { useSQLQuery } from "@motherduck/react-sql-query";
import { useState } from "react";

var N = function(v) { return v != null ? Number(v) : 0; };
var fmt = function(v, t) {
  if (v == null) return "\u2014";
  if (t === "cost") return "$" + N(v).toLocaleString(undefined, { maximumFractionDigits: 0 });
  if (t === "cpa") return "$" + N(v).toFixed(2);
  return N(v).toLocaleString();
};

export default function Dive() {
  var _m = useState("MX"), market = _m[0], setMarket = _m[1];
  var _t = useState("registrations"), metric = _t[0], setMetric = _t[1];
  var _h = useState(null), hover = _h[0], setHover = _h[1];
  var isCum = metric !== "cpa", cumCol = isCum ? "ytd_cumulative" : "running_avg";

  var aq = useSQLQuery("SELECT week_start, weekly_value, " + cumCol + " as cum_value, period_key FROM \"ps_analytics\".\"ps\".\"cumulative_actuals\" WHERE market='" + market + "' AND channel='ps' AND metric_name='" + metric + "' ORDER BY week_start");
  var pq = useSQLQuery("SELECT horizon, target_end_date, target_label, projected_cumulative, ci_low, ci_high, revision_number, reason FROM \"ps_analytics\".\"ps\".\"cumulative_projections\" WHERE market='" + market + "' AND channel='ps' AND metric_name='" + metric + "' ORDER BY target_end_date, revision_number");
  var nq = useSQLQuery("SELECT section, narrative FROM \"ps_analytics\".\"ps\".\"forecast_narratives\" WHERE market='" + market + "' AND channel='ps'");
  var cq = useSQLQuery("SELECT * FROM \"ps_analytics\".\"ps\".\"dive_forecast_calibration\" WHERE market='" + market + "' AND channel='ps'");

  var dd = function(q) { return Array.isArray(q.data) ? q.data : []; };
  var actRows = dd(aq), projRows = dd(pq), cal = dd(cq);
  var narr = {};
  dd(nq).forEach(function(r) { narr[r.section] = r.narrative; });

  var moProj = projRows.filter(function(r) { return r.horizon === "monthly"; });
  var qrProj = projRows.filter(function(r) { return r.horizon === "quarterly"; });
  var yeProj = projRows.filter(function(r) { return r.horizon === "year_end"; });
  var wkProj = projRows.filter(function(r) { return r.horizon === "weekly"; });

  var lastAct = actRows.length > 0 ? actRows[actRows.length - 1] : null;
  var lastCum = lastAct ? N(lastAct.cum_value) : 0, lastDate = lastAct ? lastAct.week_start : "2026-01-05";

  var gC = function(g) { return g === "Excellent" ? "#27ae60" : g === "Good" ? "#2ecc71" : g === "Fair" ? "#f39c12" : g === "Pending" ? "#95a5a6" : "#e74c3c"; };
  var bC = function(b) { return N(b) < 0.005 ? "#27ae60" : N(b) < 0.02 ? "#f39c12" : "#e74c3c"; };
  var cd = { background: "#fff", border: "1px solid #ddd", borderRadius: 8, padding: 16, marginBottom: 16 };
  var sT = function(c) { return { fontSize: 15, fontWeight: 600, marginBottom: 10, paddingBottom: 6, borderBottom: "2px solid " + c }; };
  var nS = { fontSize: 13, color: "#555", lineHeight: 1.6, padding: "10px 12px", background: "#fafafa", borderRadius: 6, marginTop: 12, borderLeft: "3px solid #ddd" };

  var wkDates = [];
  for (var w = 0; w < 52; w++) { var d2 = new Date(2026, 0, 5 + w * 7); wkDates.push(d2.toISOString().slice(0, 10)); }
  var months = ["2026-01-31","2026-02-28","2026-03-31","2026-04-30","2026-05-31","2026-06-30","2026-07-31","2026-08-31","2026-09-30","2026-10-31","2026-11-30","2026-12-31"];
  var mLbl = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  var mStart = ["2026-01-05","2026-02-02","2026-03-02","2026-03-30","2026-04-27","2026-06-01","2026-06-29","2026-07-27","2026-08-31","2026-09-28","2026-10-26","2026-11-30"];
  var qMonths = { Q1: ["Jan","Feb","Mar"], Q2: ["Apr","May","Jun"], Q3: ["Jul","Aug","Sep"], Q4: ["Oct","Nov","Dec"] };
  var qStart = ["2026-01-05","2026-03-30","2026-06-29","2026-09-28"];
  var qEnd = ["2026-03-31","2026-06-30","2026-09-30","2026-12-31"];

  var allDates = actRows.map(function(r) { return r.week_start; }).slice();
  moProj.forEach(function(r) { if (allDates.indexOf(r.target_end_date) < 0) allDates.push(r.target_end_date); });
  wkDates.forEach(function(d3) { if (allDates.indexOf(d3) < 0) allDates.push(d3); });
  months.forEach(function(m) { if (allDates.indexOf(m) < 0) allDates.push(m); });
  allDates.sort();

  var allVals = actRows.map(function(r) { return N(r.cum_value); });
  moProj.forEach(function(r) { allVals.push(N(r.ci_high) || N(r.projected_cumulative)); });
  var mx = Math.max.apply(null, allVals.concat([1])) * 1.08;

  var cW = 950, cH = 700, pL = 70, pR = 20, pT = 20, pB = 85, plW = cW - pL - pR, plH = cH - pT - pB;
  var xS = function(dt) { var idx = allDates.indexOf(dt); if (idx < 0) { for (var i = 0; i < allDates.length; i++) { if (allDates[i] >= dt) return pL + (i / Math.max(allDates.length - 1, 1)) * plW; } return pL + plW; } return pL + (idx / Math.max(allDates.length - 1, 1)) * plW; };
  var yS = function(v) { return pT + plH - (N(v) / mx) * plH; };
  var actPts = actRows.map(function(r) { return xS(r.week_start) + "," + yS(r.cum_value); });

  var moCi = "", moLine = "";
  if (moProj.length > 0) {
    var s = moProj.slice().sort(function(a, b) { return a.target_end_date < b.target_end_date ? -1 : 1; });
    var sX = xS(lastDate), sY = yS(lastCum);
    var u = "M" + sX + "," + sY, lo = "";
    s.forEach(function(p) { u += " L" + xS(p.target_end_date) + "," + yS(p.ci_high); });
    for (var j = s.length - 1; j >= 0; j--) lo += " L" + xS(s[j].target_end_date) + "," + yS(s[j].ci_low);
    moCi = u + lo + " L" + sX + "," + sY + " Z";
    moLine = "M" + sX + "," + sY;
    s.forEach(function(p) { moLine += " L" + xS(p.target_end_date) + "," + yS(p.projected_cumulative); });
  }

  var axY1 = pT + plH + 4, axY2 = axY1 + 16, axY3 = axY2 + 18, axY4 = axY3 + 18;
  var moByLabel = {}; moProj.forEach(function(r) { moByLabel[r.target_label] = r; });
  var qrByLabel = {}; qrProj.forEach(function(r) { qrByLabel[r.target_label] = r; });
  var wkByLabel = {}; wkProj.forEach(function(r) { wkByLabel[r.target_label] = r; });
  var yeRow = yeProj.length > 0 ? yeProj[0] : null;

  // Build actual cumulative by month from actuals data (no more hardcoded values)
  var actCum = {};
  var monthBuckets = {};
  actRows.forEach(function(r) {
    var ws = r.week_start;
    if (!ws) return;
    // Assign week to month by Thursday (ws + 3 days)
    var dt = new Date(ws);
    dt.setDate(dt.getDate() + 3);
    var mIdx = dt.getMonth();
    var ml = mLbl[mIdx];
    if (!monthBuckets[ml]) monthBuckets[ml] = 0;
    monthBuckets[ml] += N(r.weekly_value);
  });
  // Build cumulative
  var runCum = 0;
  mLbl.forEach(function(ml) {
    if (monthBuckets[ml]) {
      runCum += monthBuckets[ml];
      actCum[ml] = Math.round(runCum);
    }
  });
  // Quarterly actuals
  ["Q1","Q2","Q3","Q4"].forEach(function(ql) {
    var qm = qMonths[ql];
    var lastM = qm[qm.length - 1];
    if (actCum[lastM]) actCum[ql] = actCum[lastM];
  });

  var actByWk = {};
  actRows.forEach(function(r) { actByWk[r.period_key] = N(r.cum_value); });

