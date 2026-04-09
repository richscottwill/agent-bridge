import { useSQLQuery } from "@motherduck/react-sql-query";
import { useState } from "react";

var N=function(v){return v!=null?Number(v):0;};
var fmt=function(v,t){if(v==null)return"\u2014";if(t==="cost")return"$"+N(v).toLocaleString(undefined,{maximumFractionDigits:0});if(t==="cpa")return"$"+N(v).toFixed(2);return N(v).toLocaleString();};

export default function Dive(){
  var _m=useState("AU"),market=_m[0],setMarket=_m[1];
  var _t=useState("registrations"),metric=_t[0],setMetric=_t[1];
  var _h=useState(null),hover=_h[0],setHover=_h[1];

  // Weekly actuals (standalone values)
  var waq=useSQLQuery("SELECT week_num,period_key,week_start,value FROM \"ps_analytics\".\"ps\".\"weekly_actuals\" WHERE market='"+market+"' AND metric_name='"+metric+"' ORDER BY week_num");
  // Projections (standalone values)
  var pq=useSQLQuery("SELECT horizon,period_label,period_end,value,ci_low,ci_high,is_actual,reason FROM \"ps_analytics\".\"ps\".\"projections_standalone\" WHERE market='"+market+"' AND metric_name='"+metric+"' ORDER BY period_end");
  // Narratives
  var nq=useSQLQuery("SELECT section,narrative FROM \"ps_analytics\".\"ps\".\"forecast_narratives\" WHERE market='"+market+"' AND channel='ps'");
  // Calibration
  var cq=useSQLQuery("SELECT * FROM \"ps_analytics\".\"ps\".\"dive_forecast_calibration\" WHERE market='"+market+"' AND channel='ps'");

  var dd=function(q){return Array.isArray(q.data)?q.data:[];};
  var waRows=dd(waq),projRows=dd(pq),cal=dd(cq);
  var narr={};dd(nq).forEach(function(r){narr[r.section]=r.narrative;});

  var moProj=projRows.filter(function(r){return r.horizon==="monthly";});
  var qrProj=projRows.filter(function(r){return r.horizon==="quarterly";});
  var yeProj=projRows.filter(function(r){return r.horizon==="year_end";});
  var wkProj=projRows.filter(function(r){return r.horizon==="weekly";});

  // Build weekly data: actuals + projections
  var weeklyData={};
  waRows.forEach(function(r){weeklyData[r.week_num]={actual:N(r.value),predicted:null,ci_low:null,ci_high:null};});
  wkProj.forEach(function(r){
    var wn=parseInt(r.period_label.replace("W",""));
    if(!weeklyData[wn])weeklyData[wn]={actual:null,predicted:null,ci_low:null,ci_high:null};
    weeklyData[wn].predicted=N(r.value);weeklyData[wn].ci_low=N(r.ci_low);weeklyData[wn].ci_high=N(r.ci_high);
  });

  // Build cumulative for chart from standalone weekly values
  var cumData=[];var runCum=0;
  for(var w=1;w<=52;w++){
    var wd=weeklyData[w];
    if(wd){
      var val=wd.actual!=null?wd.actual:(wd.predicted||0);
      runCum+=val;
      cumData.push({wk:w,cum:runCum,actual:wd.actual,predicted:wd.predicted,ci_low:wd.ci_low,ci_high:wd.ci_high,isActual:wd.actual!=null});
    }
  }

  // Monthly data (standalone)
  var moByLabel={};moProj.forEach(function(r){moByLabel[r.period_label]=r;});
  var qrByLabel={};qrProj.forEach(function(r){qrByLabel[r.period_label]=r;});
  var yeRow=yeProj.length>0?yeProj[0]:null;

  // KPI cards
  var ytdRegs=0;waRows.forEach(function(r){ytdRegs+=N(r.value);});
  var lastActualWk=waRows.length>0?waRows[waRows.length-1]:null;

  // Find current month forecast
  var mLbl=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  var currentMonthIdx=3; // April (0-indexed)
  var currentMonthLabel=mLbl[currentMonthIdx];
  var currentMonthProj=moByLabel[currentMonthLabel];

  // Find current quarter
  var currentQ="Q2";
  var currentQProj=qrByLabel[currentQ];


  var gC=function(g){return g==="Excellent"?"#27ae60":g==="Good"?"#2ecc71":g==="Fair"?"#f39c12":g==="Pending"?"#95a5a6":"#e74c3c";};
  var bC=function(b){return N(b)<0.005?"#27ae60":N(b)<0.02?"#f39c12":"#e74c3c";};
  var cd={background:"#fff",border:"1px solid #ddd",borderRadius:8,padding:16,marginBottom:16};
  var sT=function(c){return{fontSize:15,fontWeight:600,marginBottom:10,paddingBottom:6,borderBottom:"2px solid "+c};};
  var nS={fontSize:13,color:"#555",lineHeight:1.6,padding:"10px 12px",background:"#fafafa",borderRadius:6,marginTop:12,borderLeft:"3px solid #ddd"};

  // Chart dimensions
  var cW=950,cH=500,pL=70,pR=20,pT=20,pB=60,plW=cW-pL-pR,plH=cH-pT-pB;
  var mx=cumData.length>0?Math.max.apply(null,cumData.map(function(d){return d.cum;}))*1.1:1;
  var xS=function(wk){return pL+((wk-1)/51)*plW;};
  var yS=function(v){return pT+plH-(N(v)/mx)*plH;};

  // Build chart paths
  var actPath="",predPath="",ciPath="";
  var lastActX=0,lastActY=0;
  cumData.forEach(function(d,i){
    var x=xS(d.wk),y=yS(d.cum);
    if(d.isActual){actPath+=(actPath?"L":"M")+x+","+y;lastActX=x;lastActY=y;}
    else{predPath+=(predPath?"L":"M"+(i>0&&cumData[i-1].isActual?lastActX+","+lastActY+" L":""))+x+","+y;}
  });

  // CI band for forecast portion
  var fcData=cumData.filter(function(d){return!d.isActual;});
  if(fcData.length>0){
    var cumLow=ytdRegs,cumHigh=ytdRegs;
    var upper="M"+lastActX+","+lastActY,lower="";
    fcData.forEach(function(d){
      cumLow+=d.ci_low||d.predicted||0;cumHigh+=d.ci_high||d.predicted||0;
      upper+=" L"+xS(d.wk)+","+yS(cumHigh);
    });
    for(var j=fcData.length-1;j>=0;j--){
      cumLow=ytdRegs;for(var k=0;k<=j;k++)cumLow+=fcData[k].ci_low||fcData[k].predicted||0;
      lower+=" L"+xS(fcData[j].wk)+","+yS(cumLow);
    }
    ciPath=upper+lower+" L"+lastActX+","+lastActY+" Z";
  }

  var eC=function(e){var v=Math.abs(N(e));return v<3?"#27ae60":v<7?"#f39c12":"#e74c3c";};
  var th={textAlign:"right",padding:"5px 8px",color:"#888",fontSize:11};
  var thL={textAlign:"left",padding:"5px 8px",color:"#888",fontSize:11};

  var TRow=function(props){
    var r=props.r;
    var err=r.actual!=null&&r.predicted!=null&&r.actual>0?Math.abs((r.predicted-r.actual)/r.actual*100):null;
    return(<tr style={{borderBottom:"1px solid #f5f5f5",background:props.bg||"transparent"}}>
      <td style={{padding:"5px 8px",fontWeight:props.wt||400,color:props.co||"#2c3e50",fontSize:12}}>{r.period}</td>
      <td style={{padding:"5px 8px",textAlign:"right",fontWeight:r.actual!=null?600:400}}>{r.actual!=null?fmt(r.actual,metric):"\u2014"}</td>
      <td style={{padding:"5px 8px",textAlign:"right"}}>{r.predicted!=null?fmt(r.predicted,metric):"\u2014"}</td>
      <td style={{padding:"5px 8px",textAlign:"right",color:"#999",fontSize:11}}>{r.ci_low!=null?fmt(r.ci_low,metric)+"\u2013"+fmt(r.ci_high,metric):"\u2014"}</td>
      <td style={{padding:"5px 8px",textAlign:"right",color:err!=null?eC(err):"#ccc",fontWeight:600}}>{err!=null?err.toFixed(1)+"%":"\u2014"}</td>
    </tr>);
  };

  // Build monthly table rows from standalone projections + actuals
  var monthRows=mLbl.map(function(ml,i){
    var proj=moByLabel[ml];
    var isActual=proj&&proj.is_actual;
    return{
      period:ml,
      actual:isActual?N(proj.value):null,
      predicted:proj&&!isActual?N(proj.value):null,
      ci_low:proj&&!isActual?N(proj.ci_low):null,
      ci_high:proj&&!isActual?N(proj.ci_high):null
    };
  });

  // Build quarterly table rows
  var qLabels=["Q1","Q2","Q3","Q4"];
  var qRows=qLabels.map(function(ql){
    var proj=qrByLabel[ql];
    var isActual=proj&&proj.is_actual;
    return{
      period:ql,
      actual:isActual?N(proj.value):null,
      predicted:proj?N(proj.value):null,
      ci_low:proj?N(proj.ci_low):null,
      ci_high:proj?N(proj.ci_high):null
    };
  });

  // Build weekly table rows
  var wkRows=[];
  for(var wi=1;wi<=52;wi++){
    var wd2=weeklyData[wi];
    wkRows.push({
      period:"W"+wi,
      actual:wd2?wd2.actual:null,
      predicted:wd2?wd2.predicted:null,
      ci_low:wd2?wd2.ci_low:null,
      ci_high:wd2?wd2.ci_high:null
    });
  }


  return(<div style={{fontFamily:"-apple-system,BlinkMacSystemFont,sans-serif",maxWidth:1100,margin:"0 auto",padding:20}}>
    <h1 style={{fontSize:22,marginBottom:4}}>PS Forecast Tracker</h1>
    <p style={{fontSize:12,color:"#888",marginBottom:12}}>2026 {metric} — standalone values (weeks sum to months, months sum to quarters)</p>

    <div style={{display:"flex",gap:8,marginBottom:8,flexWrap:"wrap"}}>
      {[["AU","AU"],["MX","MX"],["US","US"],["CA","CA"],["UK","UK"],["DE","DE"],["FR","FR"],["IT","IT"],["ES","ES"],["JP","JP"],["EU5","EU5"],["WW","WW"]].map(function(x){
        return <button key={x[0]} onClick={function(){setMarket(x[0]);}} style={{padding:"6px 14px",borderRadius:6,border:market===x[0]?"2px solid #3498db":"1px solid #ddd",background:market===x[0]?"#ebf5fb":"#fff",color:market===x[0]?"#2980b9":"#666",fontWeight:market===x[0]?600:400,cursor:"pointer",fontSize:13}}>{x[1]}</button>;
      })}
    </div>

    <div style={{display:"flex",gap:8,marginBottom:16,flexWrap:"wrap"}}>
      {[["registrations","Registrations"],["cost","Cost"],["cpa","CPA"]].map(function(x){
        return <button key={x[0]} onClick={function(){setMetric(x[0]);}} style={{padding:"6px 12px",borderRadius:6,border:metric===x[0]?"2px solid #555":"1px solid #ddd",background:metric===x[0]?"#f0f0f0":"#fff",color:metric===x[0]?"#333":"#666",fontWeight:metric===x[0]?600:400,cursor:"pointer",fontSize:13}}>{x[1]}</button>;
      })}
    </div>

    {/* KPI Cards */}
    <div style={{display:"flex",gap:16,marginBottom:16,flexWrap:"wrap"}}>
      <div style={{background:"#f4f6f7",border:"1px solid #ddd",borderRadius:8,padding:"10px 16px",flex:1,minWidth:120}}>
        <div style={{fontSize:10,color:"#888",textTransform:"uppercase"}}>YTD</div>
        <div style={{fontSize:22,fontWeight:700}}>{fmt(ytdRegs,metric)}</div>
      </div>
      {currentMonthProj?<div style={{background:"#f4f6f7",border:"1px solid #ddd",borderRadius:8,padding:"10px 16px",flex:1,minWidth:120}}>
        <div style={{fontSize:10,color:"#888",textTransform:"uppercase"}}>Month - {currentMonthLabel}</div>
        <div style={{fontSize:22,fontWeight:700}}>{fmt(currentMonthProj.value,metric)}</div>
        <div style={{fontSize:11,color:"#999"}}>{fmt(currentMonthProj.ci_low,metric)}{"\u2013"}{fmt(currentMonthProj.ci_high,metric)}</div>
      </div>:null}
      {currentQProj?<div style={{background:"#f4f6f7",border:"1px solid #ddd",borderRadius:8,padding:"10px 16px",flex:1,minWidth:120}}>
        <div style={{fontSize:10,color:"#888",textTransform:"uppercase"}}>Quarter - {currentQ}</div>
        <div style={{fontSize:22,fontWeight:700}}>{fmt(currentQProj.value,metric)}</div>
        <div style={{fontSize:11,color:"#999"}}>{fmt(currentQProj.ci_low,metric)}{"\u2013"}{fmt(currentQProj.ci_high,metric)}</div>
      </div>:null}
      {yeRow?<div style={{background:"#f4f6f7",border:"1px solid #ddd",borderRadius:8,padding:"10px 16px",flex:1,minWidth:120}}>
        <div style={{fontSize:10,color:"#888",textTransform:"uppercase"}}>Year - 2026</div>
        <div style={{fontSize:22,fontWeight:700}}>{fmt(yeRow.value,metric)}</div>
        <div style={{fontSize:11,color:"#999"}}>{fmt(yeRow.ci_low,metric)}{"\u2013"}{fmt(yeRow.ci_high,metric)}</div>
      </div>:null}
    </div>

    {/* Chart */}
    <div style={{...cd,position:"relative"}}>
      <div style={{display:"flex",gap:16,fontSize:11,color:"#888",marginBottom:2}}>
        <span><span style={{display:"inline-block",width:16,height:3,background:"#3498db",borderRadius:2,marginRight:4}}/>Actual</span>
        <span><span style={{display:"inline-block",width:16,height:0,borderTop:"2px dashed #1a2744",marginRight:4}}/>Predicted</span>
        <span><span style={{display:"inline-block",width:16,height:10,background:"rgba(234,179,8,0.15)",borderRadius:2,marginRight:4}}/>CI</span>
      </div>
      {cumData.length===0?<div style={{textAlign:"center",padding:40,color:"#999"}}>No data</div>:
      <svg viewBox={"0 0 "+cW+" "+cH} style={{width:"100%"}}>
        {[0,0.25,0.5,0.75,1].map(function(f){return <g key={f}><line x1={pL} x2={cW-pR} y1={pT+plH*(1-f)} y2={pT+plH*(1-f)} stroke="#f0f0f0"/><text x={pL-6} y={pT+plH*(1-f)+4} textAnchor="end" fontSize={11} fill="#999">{fmt(mx*f,metric)}</text></g>;})}
        {[1,5,9,13,14,18,22,26,30,35,39,44,48,52].map(function(w){return <text key={w} x={xS(w)} y={pT+plH+16} textAnchor="middle" fontSize={10} fill="#888">W{w}</text>;})}
        {["Q1","Q2","Q3","Q4"].map(function(q,i){var x1=xS(i*13+1),x2=xS(Math.min((i+1)*13,52));return <g key={q}><rect x={x1} y={pT} width={x2-x1} height={plH} fill={i%2===0?"rgba(26,39,68,0.03)":"transparent"}/><text x={(x1+x2)/2} y={pT+plH+32} textAnchor="middle" fontSize={11} fill="#bbb">{q}</text></g>;})}
        {ciPath?<path d={ciPath} fill="rgba(234,179,8,0.12)"/>:null}
        {predPath?<path d={predPath} fill="none" stroke="#1a2744" strokeWidth={2} strokeDasharray="4,3"/>:null}
        {actPath?<path d={actPath} fill="none" stroke="#3498db" strokeWidth={2.5}/>:null}
        {cumData.filter(function(d){return d.isActual;}).map(function(d,i){return <circle key={"a"+i} cx={xS(d.wk)} cy={yS(d.cum)} r={3} fill="#3498db"/>;})
        }
      </svg>}
    </div>

    {/* Monthly + Quarterly tables */}
    <div style={{display:"flex",gap:24,marginBottom:16}}>
      <div style={{flex:1}}>
        <div style={{fontSize:13,fontWeight:600,color:"#1a2744",marginBottom:6}}>Monthly (standalone)</div>
        <table style={{width:"100%",fontSize:11,borderCollapse:"collapse"}}>
          <thead><tr style={{borderBottom:"1px solid #eee"}}><th style={thL}>Month</th><th style={th}>Actual</th><th style={th}>Pred</th><th style={th}>CI</th><th style={th}>Err</th></tr></thead>
          <tbody>{monthRows.map(function(r,i){return <TRow key={i} r={r} bg={Math.floor(i/3)%2===0?"rgba(26,39,68,0.05)":"transparent"}/>;})}</tbody>
        </table>
      </div>
      <div style={{flex:1,borderLeft:"2px solid #ddd",paddingLeft:20}}>
        <div style={{fontSize:13,fontWeight:600,color:"#1a2744",marginBottom:6}}>Quarterly + Year-End (standalone)</div>
        <table style={{width:"100%",fontSize:11,borderCollapse:"collapse"}}>
          <thead><tr style={{borderBottom:"1px solid #eee"}}><th style={thL}>Period</th><th style={th}>Actual</th><th style={th}>Pred</th><th style={th}>CI</th><th style={th}>Err</th></tr></thead>
          <tbody>
            {qRows.map(function(r,i){return <TRow key={i} r={r} wt={600} co="#1a2744" bg={i%2===0?"rgba(26,39,68,0.05)":"transparent"}/>;})
            }
            {yeRow?<TRow r={{period:"2026 YE",actual:null,predicted:N(yeRow.value),ci_low:N(yeRow.ci_low),ci_high:N(yeRow.ci_high)}} wt={700} co="#1a2744" bg="rgba(26,39,68,0.05)"/>:null}
          </tbody>
        </table>
      </div>
    </div>

    {/* Weekly table */}
    <div style={cd}>
      <div style={sT("#1a2744")}>Weekly (W1-W52)</div>
      <div style={{maxHeight:400,overflowY:"auto"}}>
        <table style={{width:"100%",fontSize:11,borderCollapse:"collapse"}}>
          <thead><tr style={{borderBottom:"2px solid #eee",position:"sticky",top:0,background:"#fff"}}><th style={thL}>Week</th><th style={th}>Actual</th><th style={th}>Predicted</th><th style={th}>CI</th><th style={th}>Error</th></tr></thead>
          <tbody>{wkRows.map(function(r,i){
            var hasData=r.actual!=null||r.predicted!=null;
            return <tr key={i} style={{borderBottom:"1px solid #f8f8f8",background:Math.floor(i/13)%2===0?"rgba(26,39,68,0.05)":"transparent"}}>
              <td style={{padding:"4px 8px",fontWeight:500,color:hasData?"#2c3e50":"#ccc"}}>{r.period}</td>
              <td style={{padding:"4px 8px",textAlign:"right",fontWeight:r.actual!=null?600:400}}>{r.actual!=null?fmt(r.actual,metric):"\u2014"}</td>
              <td style={{padding:"4px 8px",textAlign:"right"}}>{r.predicted!=null?fmt(r.predicted,metric):"\u2014"}</td>
              <td style={{padding:"4px 8px",textAlign:"right",color:"#999",fontSize:10}}>{r.ci_low!=null?fmt(r.ci_low,metric)+"\u2013"+fmt(r.ci_high,metric):"\u2014"}</td>
              <td style={{padding:"4px 8px",textAlign:"right",color:r.actual!=null&&r.predicted!=null?eC(Math.abs((r.predicted-r.actual)/r.actual*100)):"#ccc",fontWeight:600}}>{r.actual!=null&&r.predicted!=null&&r.actual>0?(Math.abs((r.predicted-r.actual)/r.actual*100)).toFixed(1)+"%":"\u2014"}</td>
            </tr>;
          })}</tbody>
        </table>
      </div>
    </div>

    {/* Justification */}
    <div style={{...cd,background:"#fafbfc"}}>
      <div style={sT("#1a2744")}>Justification</div>
      {narr.revisions?<div><div style={{fontSize:12,fontWeight:600,color:"#1a2744",marginBottom:4}}>Revisions</div><div style={nS}>{narr.revisions}</div></div>:null}
      {narr.monthly?<div style={{marginTop:10}}><div style={{fontSize:12,fontWeight:600,color:"#1a2744",marginBottom:4}}>Monthly</div><div style={nS}>{narr.monthly}</div></div>:null}
      {narr.quarterly?<div style={{marginTop:10}}><div style={{fontSize:12,fontWeight:600,color:"#1a2744",marginBottom:4}}>Quarterly</div><div style={nS}>{narr.quarterly}</div></div>:null}
      {narr.year_end?<div style={{marginTop:10}}><div style={{fontSize:12,fontWeight:600,color:"#1a2744",marginBottom:4}}>Year-End</div><div style={nS}>{narr.year_end}</div></div>:null}
    </div>

    {/* Calibration */}
    <div style={cd}>
      <div style={sT("#1a2744")}>Calibration</div>
      {cal.length===0?<div style={{color:"#999",fontSize:13,padding:16,textAlign:"center"}}>No calibration data yet</div>:
      <table style={{width:"100%",fontSize:12,borderCollapse:"collapse"}}>
        <thead><tr style={{borderBottom:"1px solid #eee"}}><th style={thL}>Metric</th><th style={th}>Horizon</th><th style={th}>N</th><th style={th}>CI Hit</th><th style={th}>Error</th><th style={th}>Grade</th></tr></thead>
        <tbody>{cal.map(function(r,i){return <tr key={i} style={{borderBottom:"1px solid #f5f5f5"}}>
          <td style={{padding:"6px 8px",fontWeight:500}}>{r.metric_name}</td>
          <td style={{padding:"6px 8px"}}>{r.horizon}</td>
          <td style={{padding:"6px 8px",textAlign:"right"}}>{N(r.n_predictions)}</td>
          <td style={{padding:"6px 8px",textAlign:"right"}}>{N(r.ci_hit_rate_pct).toFixed(0)}%</td>
          <td style={{padding:"6px 8px",textAlign:"right"}}>{N(r.mean_abs_error_pct).toFixed(1)}%</td>
          <td style={{padding:"6px 8px",textAlign:"right"}}><span style={{background:gC(r.calibration_grade)+"22",color:gC(r.calibration_grade),padding:"2px 8px",borderRadius:4,fontSize:11,fontWeight:600}}>{r.calibration_grade}</span></td>
        </tr>;})}</tbody>
      </table>}
    </div>

    <div style={{fontSize:10,color:"#bbb",textAlign:"right",marginTop:8}}>ps_analytics.ps — standalone values, cumulative computed for chart only</div>
  </div>);
}
