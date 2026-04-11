import { useSQLQuery } from "@motherduck/react-sql-query";
import { useState } from "react";

var N = function(v) { return v != null ? Number(v) : 0; };
var fmt = function(v, t) {
  if (v == null) return "\u2014";
  if (t === "cost") return "$" + N(v).toLocaleString(undefined, { maximumFractionDigits: 0 });
  if (t === "pct") return N(v).toFixed(1) + "%";
  if (t === "regs") return N(v).toLocaleString(undefined, { maximumFractionDigits: 0 });
  return N(v).toLocaleString();
};

var statusColor = function(s) {
  if (s === "on_track") return "#27ae60";
  if (s === "at_risk") return "#f39c12";
  if (s === "behind") return "#e74c3c";
  return "#95a5a6";
};

var pctBarColor = function(pct) {
  if (pct >= 95) return "#27ae60";
  if (pct >= 80) return "#f39c12";
  return "#e74c3c";
};

export default function Pacing() {
  var _m = useState("registrations"), metric = _m[0], setMetric = _m[1];
  var _v = useState("current_month"), view = _v[0], setView = _v[1];

  // Current month pacing — all markets
  var pacingQ = useSQLQuery(
    "SELECT market, market_name, region, currency_code, metric_name, month_key, " +
    "mtd_actual, month_target, pacing_pct, weeks_in, ytd_actual, annual_target, ytd_pacing_pct, status " +
    "FROM \"ps_analytics\".\"ps\".\"dive_pacing\" " +
    "WHERE metric_name='" + metric + "' " +
    "ORDER BY region, market"
  );

  // Weekly trend for sparklines — last 8 weeks per market
  var trendQ = useSQLQuery(
    "SELECT market, period_key, actual_value " +
    "FROM \"ps_analytics\".\"ps\".\"metrics\" " +
    "WHERE metric_name='" + metric + "' AND period_key LIKE '2026-W%' " +
    "ORDER BY market, period_key"
  );

  var dd = function(q) { return q && Array.isArray(q.data) ? q.data : []; };
  var pacingRows = dd(pacingQ);
  var trendRows = dd(trendQ);

  // Group pacing by market — latest month per market
  var byMarket = {};
  pacingRows.forEach(function(r) {
    if (!byMarket[r.market] || r.month_key > byMarket[r.market].month_key) {
      byMarket[r.market] = r;
    }
  });
  var markets = Object.values(byMarket).sort(function(a, b) {
    return N(b.ytd_actual) - N(a.ytd_actual);
  });

  // Build sparkline data per market
  var sparkData = {};
  trendRows.forEach(function(r) {
    if (!sparkData[r.market]) sparkData[r.market] = [];
    sparkData[r.market].push(N(r.actual_value));
  });

  // Mini sparkline SVG
  var Spark = function(props) {
    var data = props.data || [];
    if (data.length < 2) return null;
    var max = Math.max.apply(null, data);
    var min = Math.min.apply(null, data);
    var range = max - min || 1;
    var w = 120, h = 32, pad = 2;
    var points = data.map(function(v, i) {
      var x = pad + (i / (data.length - 1)) * (w - pad * 2);
      var y = h - pad - ((v - min) / range) * (h - pad * 2);
      return x + "," + y;
    }).join(" ");
    var last = data[data.length - 1];
    var prev = data[data.length - 2];
    var color = last >= prev ? "#27ae60" : "#e74c3c";
    return (
      <svg width={w} height={h} style={{ display: "block" }}>
        <polyline points={points} fill="none" stroke={color} strokeWidth="2" />
      </svg>
    );
  };

  // Pacing bar component
  var PacingBar = function(props) {
    var pct = Math.min(N(props.pct), 120);
    var color = pctBarColor(N(props.pct));
    return (
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{ width: 140, height: 16, background: "#2a2a3e", borderRadius: 4, overflow: "hidden", position: "relative" }}>
          <div style={{ width: (pct / 120 * 100) + "%", height: "100%", background: color, borderRadius: 4, transition: "width 0.3s" }} />
          <div style={{ position: "absolute", top: 0, left: "79%", width: 2, height: "100%", background: "#ffffff44" }} />
        </div>
        <span style={{ fontSize: 13, color: color, fontWeight: 600, minWidth: 48 }}>{fmt(props.pct, "pct")}</span>
      </div>
    );
  };

  // Styles
  var card = { background: "#1e1e2e", borderRadius: 10, padding: 16, marginBottom: 12 };
  var headerStyle = { color: "#cdd6f4", fontSize: 22, fontWeight: 700, margin: 0 };
  var subStyle = { color: "#6c7086", fontSize: 13, marginTop: 4 };
  var pillActive = { background: "#89b4fa", color: "#1e1e2e", border: "none", borderRadius: 6, padding: "6px 14px", fontSize: 13, fontWeight: 600, cursor: "pointer" };
  var pillInactive = { background: "#313244", color: "#a6adc8", border: "none", borderRadius: 6, padding: "6px 14px", fontSize: 13, cursor: "pointer" };
  var tableHeader = { color: "#6c7086", fontSize: 11, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, padding: "8px 12px", borderBottom: "1px solid #313244", textAlign: "left" };
  var tableCell = { padding: "10px 12px", borderBottom: "1px solid #1e1e2e", color: "#cdd6f4", fontSize: 14 };

  var metricLabel = metric === "registrations" ? "Registrations" : "Cost";
  var fmtType = metric === "cost" ? "cost" : "regs";

  return (
    <div style={{ fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", background: "#11111b", minHeight: "100vh", padding: 24, color: "#cdd6f4" }}>
      {/* Header */}
      <div style={{ ...card, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={headerStyle}>Market Pacing Dashboard</h1>
          <p style={subStyle}>All 10 markets \u2022 2026 YTD vs OP targets</p>
        </div>
        <div style={{ display: "flex", gap: 6 }}>
          <button style={metric === "registrations" ? pillActive : pillInactive} onClick={function() { setMetric("registrations"); }}>Registrations</button>
          <button style={metric === "cost" ? pillActive : pillInactive} onClick={function() { setMetric("cost"); }}>Cost</button>
        </div>
      </div>

      {/* Summary KPI row */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: 12 }}>
        {(function() {
          var totalYTD = 0, totalTarget = 0, onTrack = 0, atRisk = 0, behind = 0;
          markets.forEach(function(m) {
            totalYTD += N(m.ytd_actual);
            totalTarget += N(m.annual_target);
            if (m.status === "on_track") onTrack++;
            else if (m.status === "at_risk") atRisk++;
            else behind++;
          });
          var wwPct = totalTarget > 0 ? (totalYTD / totalTarget * 100).toFixed(1) : "\u2014";
          return [
            { label: "WW YTD " + metricLabel, value: fmt(totalYTD, fmtType) },
            { label: "WW Annual Target", value: fmt(totalTarget, fmtType) },
            { label: "WW YTD Pacing", value: wwPct + "%" },
            { label: "Status", value: onTrack + " on track \u2022 " + atRisk + " at risk \u2022 " + behind + " behind" }
          ].map(function(kpi, i) {
            return (
              <div key={i} style={card}>
                <div style={{ color: "#6c7086", fontSize: 11, textTransform: "uppercase", letterSpacing: 1, marginBottom: 6 }}>{kpi.label}</div>
                <div style={{ fontSize: 20, fontWeight: 700, color: "#cdd6f4" }}>{kpi.value}</div>
              </div>
            );
          });
        })()}
      </div>

      {/* Market table */}
      <div style={{ ...card, padding: 0, overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#181825" }}>
              <th style={tableHeader}>Market</th>
              <th style={tableHeader}>Region</th>
              <th style={{ ...tableHeader, textAlign: "right" }}>MTD Actual</th>
              <th style={{ ...tableHeader, textAlign: "right" }}>Month Target</th>
              <th style={tableHeader}>MTD Pacing</th>
              <th style={{ ...tableHeader, textAlign: "right" }}>YTD Actual</th>
              <th style={{ ...tableHeader, textAlign: "right" }}>Annual Target</th>
              <th style={tableHeader}>YTD Pacing</th>
              <th style={tableHeader}>Trend</th>
              <th style={tableHeader}>Status</th>
            </tr>
          </thead>
          <tbody>
            {markets.map(function(m, i) {
              var bg = i % 2 === 0 ? "#1e1e2e" : "#181825";
              return (
                <tr key={m.market} style={{ background: bg }}>
                  <td style={{ ...tableCell, fontWeight: 700 }}>{m.market}</td>
                  <td style={{ ...tableCell, color: "#6c7086" }}>{m.region}</td>
                  <td style={{ ...tableCell, textAlign: "right" }}>{fmt(m.mtd_actual, fmtType)}</td>
                  <td style={{ ...tableCell, textAlign: "right", color: "#6c7086" }}>{fmt(m.month_target, fmtType)}</td>
                  <td style={tableCell}><PacingBar pct={m.pacing_pct} /></td>
                  <td style={{ ...tableCell, textAlign: "right" }}>{fmt(m.ytd_actual, fmtType)}</td>
                  <td style={{ ...tableCell, textAlign: "right", color: "#6c7086" }}>{fmt(m.annual_target, fmtType)}</td>
                  <td style={tableCell}><PacingBar pct={m.ytd_pacing_pct} /></td>
                  <td style={tableCell}><Spark data={sparkData[m.market]} /></td>
                  <td style={tableCell}>
                    <span style={{ background: statusColor(m.status) + "22", color: statusColor(m.status), padding: "3px 10px", borderRadius: 4, fontSize: 12, fontWeight: 600 }}>
                      {m.status === "on_track" ? "On Track" : m.status === "at_risk" ? "At Risk" : m.status === "behind" ? "Behind" : "No Target"}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Monthly breakdown — all months for selected metric */}
      <div style={{ ...card, marginTop: 12 }}>
        <h2 style={{ ...headerStyle, fontSize: 16, marginBottom: 12 }}>Monthly Breakdown</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 10 }}>
          {(function() {
            var months = {};
            pacingRows.forEach(function(r) {
              if (!months[r.month_key]) months[r.month_key] = { key: r.month_key, markets: [] };
              months[r.month_key].markets.push(r);
            });
            return Object.values(months).sort(function(a, b) { return a.key < b.key ? -1 : 1; }).map(function(mo) {
              var totalActual = 0, totalTarget = 0;
              mo.markets.forEach(function(m) { totalActual += N(m.mtd_actual); totalTarget += N(m.month_target); });
              var pct = totalTarget > 0 ? (totalActual / totalTarget * 100) : 0;
              var label = mo.key.replace("2026-M", "");
              var monthNames = { "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec" };
              return (
                <div key={mo.key} style={{ background: "#181825", borderRadius: 8, padding: 12 }}>
                  <div style={{ fontSize: 13, color: "#6c7086", marginBottom: 4 }}>{monthNames[label] || label}</div>
                  <div style={{ fontSize: 18, fontWeight: 700 }}>{fmt(totalActual, fmtType)}</div>
                  <div style={{ fontSize: 11, color: "#6c7086" }}>of {fmt(totalTarget, fmtType)}</div>
                  <PacingBar pct={pct} />
                </div>
              );
            });
          })()}
        </div>
      </div>

      <div style={{ color: "#45475a", fontSize: 11, textAlign: "center", marginTop: 16 }}>
        Data from ps_analytics.ps.dive_pacing \u2022 Weekly actuals through latest WBR upload
      </div>
    </div>
  );
}
