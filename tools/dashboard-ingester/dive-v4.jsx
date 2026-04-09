import { useSQLQuery } from "@motherduck/react-sql-query";
import { useState } from "react";
var N=function(v){return v!=null?Number(v):0;};
var fmt=function(v,t){if(v==null)return"\u2014";if(t==="cost")return"$"+Math.round(N(v)).toLocaleString();if(t==="cpa")return"$"+N(v).toFixed(2);return Math.round(N(v)).toLocaleString();};
export default function Dive(){
var _m=useState("AU"),market=_m[0],setMarket=_m[1];
var _t=useState("registrations"),metric=_t[0],setMetric=_t[1];
var _cv=useState("weekly"),chartView=_cv[0],setChartView=_cv[1];
// Single query per horizon — that's it
var wq=useSQLQuery("SELECT period_label,period_order,actual,predicted,ci_low,ci_high FROM \"ps_analytics\".\"ps\".\"forecast_tracker\" WHERE market='"+market+"' AND metric_name='"+metric+"' AND horizon='weekly' ORDER BY period_order");
var mq=useSQLQuery("SELECT period_label,period_order,actual,predicted,ci_low,ci_high FROM \"ps_analytics\".\"ps\".\"forecast_tracker\" WHERE market='"+market+"' AND metric_name='"+metric+"' AND horizon='monthly' ORDER BY period_order");
var qq=useSQLQuery("SELECT period_label,period_order,actual,predicted,ci_low,ci_high FROM \"ps_analytics\".\"ps\".\"forecast_tracker\" WHERE market='"+market+"' AND metric_name='"+metric+"' AND horizon='quarterly' ORDER BY period_order");
var yq=useSQLQuery("SELECT period_label,actual,predicted,ci_low,ci_high FROM \"ps_analytics\".\"ps\".\"forecast_tracker\" WHERE market='"+market+"' AND metric_name='"+metric+"' AND horizon='year_end'");
var nq=useSQLQuery("SELECT section,narrative FROM \"ps_analytics\".\"ps\".\"forecast_narratives\" WHERE market='"+market+"' AND channel='ps'");
var dd=function(q){return q&&Array.isArray(q.data)?q.data:[];};
var weeks=dd(wq),months=dd(mq),quarters=dd(qq),yeArr=dd(yq),narrArr=dd(nq);
var ye=yeArr.length>0?yeArr[0]:null;
var narr={};narrArr.forEach(function(r){narr[r.section]=r.narrative;});
// KPI computations
var ytd=0;weeks.forEach(function(w){if(w.actual!=null)ytd+=N(w.actual);});
var lastActWk=0;weeks.forEach(function(w){if(w.actual!=null)lastActWk=N(w.period_order);});
var curMonth=months.length>3?months[3]:null; // Apr (index 3)
var curQ=quarters.length>1?quarters[1]:null; // Q2 (index 1)
// Styles
var eC=function(e){var v=Math.abs(N(e));return v<5?"#27ae60":v<15?"#f39c12":"#e74c3c";};
var isBadCI=function(r){return r&&(N(r.ci_low)<=0);};
var cd={background:"#fff",border:"1px solid #ddd",borderRadius:8,padding:16,marginBottom:16};
var sT=function(c){return{fontSize:15,fontWeight:600,marginBottom:10,paddingBottom:6,borderBottom:"2px solid "+c};};
var nS={fontSize:13,color:"#555",lineHeight:1.6,padding:"10px 12px",background:"#fafafa",borderRadius:6,marginTop:12,borderLeft:"3px solid #ddd"};
var th={textAlign:"right",padding:"5px 8px",color:"#888",fontSize:11};
var thL={textAlign:"left",padding:"5px 8px",color:"#888",fontSize:11};
// Chart dimensions
var cW=950,cH=400,pL=65,pR=15,pT=15,pB=60,plW=cW-pL-pR,plH=cH-pT-pB;
var mLbl=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
var mStart=[1,5,9,14,18,23,27,32,36,40,45,49];
var mEnd=[4,8,13,17,22,26,31,35,39,44,48,52];
// Build chart function — reused for both weekly standalone and cumulative
function buildWeeklyChart(weeks,metric,chartType){
var xS=function(w){return pL+((w-1)/51)*plW;};
var data=[];
if(chartType==="cumulative"){var runAct=0,runPred=0,runLo=0,runHi=0;
weeks.forEach(function(w){var wo=N(w.period_order);var a=w.actual!=null?N(w.actual):null;var p=N(w.predicted);
if(a!=null)runAct+=a;runPred+=p;runLo+=N(w.ci_low);runHi+=N(w.ci_high);
data.push({wk:wo,actual:a!=null?runAct:null,predicted:runPred,ci_low:runLo,ci_high:runHi});});
}else{weeks.forEach(function(w){data.push({wk:N(w.period_order),actual:w.actual!=null?N(w.actual):null,predicted:N(w.predicted),ci_low:N(w.ci_low),ci_high:N(w.ci_high)});});}
var allVals=data.map(function(d){return Math.max(N(d.actual),N(d.predicted),N(d.ci_high));});
var mx2=Math.max.apply(null,allVals)*1.08||1;
var yS=function(v){return pT+plH-(N(v)/mx2)*plH;};
// Paths
var actPath="",predPath="",ciPath="";var lastAX=0,lastAY=0;
data.forEach(function(d){var x=xS(d.wk),y;if(d.actual!=null){y=yS(d.actual);actPath+=(actPath?"L":"M")+x+","+y;lastAX=x;lastAY=y;}});
// Prediction line — starts from last actual point
var predStarted=false;
data.forEach(function(d){var x=xS(d.wk);if(d.actual==null){if(!predStarted&&lastAX>0){predPath="M"+lastAX+","+lastAY;predStarted=true;}predPath+="L"+x+","+yS(d.predicted);}});
// CI band
var futureData=data.filter(function(d){return d.actual==null;});
if(futureData.length>0){var upper="M"+lastAX+","+lastAY;var lowerPts=[];
futureData.forEach(function(d){upper+=" L"+xS(d.wk)+","+yS(d.ci_high);lowerPts.unshift(xS(d.wk)+","+yS(d.ci_low));});
ciPath=upper+" L"+lowerPts.join(" L")+" L"+lastAX+","+lastAY+" Z";}
return {data:data,mx:mx2,xS:xS,yS:yS,actPath:actPath,predPath:predPath,ciPath:ciPath};
}
// TRow component
var TRow=function(props){var r=props.r;var err=r.actual!=null&&r.predicted!=null&&N(r.actual)>0?Math.abs((N(r.predicted)-N(r.actual))/N(r.actual)*100):null;
return(<tr style={{borderBottom:"1px solid #f5f5f5",background:props.bg||"transparent"}}>
<td style={{padding:"5px 8px",fontWeight:props.wt||400,color:props.co||"#2c3e50",fontSize:12}}>{r.period_label}</td>
<td style={{padding:"5px 8px",textAlign:"right",fontWeight:r.actual!=null?600:400}}>{r.actual!=null?fmt(r.actual,metric):"\u2014"}</td>
<td style={{padding:"5px 8px",textAlign:"right"}}>{r.predicted!=null?fmt(r.predicted,metric):"\u2014"}</td>
<td style={{padding:"5px 8px",textAlign:"right",color:"#999",fontSize:10}}>{r.ci_low!=null?fmt(r.ci_low,metric)+"\u2013"+fmt(r.ci_high,metric):"\u2014"}</td>
<td style={{padding:"5px 8px",textAlign:"right",color:err!=null?eC(err):"#ccc",fontWeight:600}}>{err!=null?err.toFixed(1)+"%":"\u2014"}</td>
</tr>);};
// Render
var chart=weeks.length>0?buildWeeklyChart(weeks,metric,chartView):null;
return(<div style={{fontFamily:"-apple-system,BlinkMacSystemFont,sans-serif",maxWidth:1100,margin:"0 auto",padding:20}}>
<h1 style={{fontSize:22,marginBottom:4}}>PS Forecast Tracker</h1>
<p style={{fontSize:12,color:"#888",marginBottom:12}}>2026 {metric}</p>
<div style={{display:"flex",gap:8,marginBottom:8,flexWrap:"wrap"}}>{[["AU","AU"],["MX","MX"],["US","US"],["CA","CA"],["JP","JP"],["EU5","EU5"],["WW","WW"]].map(function(x){return <button key={x[0]} onClick={function(){setMarket(x[0]);}} style={{padding:"6px 14px",borderRadius:6,border:market===x[0]?"2px solid #3498db":"1px solid #ddd",background:market===x[0]?"#ebf5fb":"#fff",color:market===x[0]?"#2980b9":"#666",fontWeight:market===x[0]?600:400,cursor:"pointer",fontSize:13}}>{x[1]}</button>;})}</div>
<div style={{display:"flex",gap:8,marginBottom:16,flexWrap:"wrap"}}>{[["registrations","Registrations"],["cost","Cost"],["cpa","CPA"]].map(function(x){return <button key={x[0]} onClick={function(){setMetric(x[0]);}} style={{padding:"6px 12px",borderRadius:6,border:metric===x[0]?"2px solid #555":"1px solid #ddd",background:metric===x[0]?"#f0f0f0":"#fff",color:metric===x[0]?"#333":"#666",fontWeight:metric===x[0]?600:400,cursor:"pointer",fontSize:13}}>{x[1]}</button>;})}</div>
{/* KPI Cards */}
<div style={{display:"flex",gap:16,marginBottom:16,flexWrap:"wrap"}}>
<div style={{background:"#f4f6f7",border:"1px solid #ddd",borderRadius:8,padding:"10px 16px",flex:1,minWidth:120}}><div style={{fontSize:10,color:"#888",textTransform:"uppercase"}}>YTD</div><div style={{fontSize:22,fontWeight:700}}>{fmt(ytd,metric)}</div></div>
{curMonth?<div style={{background:isBadCI(curMonth)?"#fff8f0":"#f4f6f7",border:isBadCI(curMonth)?"1px solid #f0c040":"1px solid #ddd",borderRadius:8,padding:"10px 16px",flex:1,minWidth:120}}><div style={{fontSize:10,color:"#888",textTransform:"uppercase"}}>Month - Apr</div><div style={{fontSize:22,fontWeight:700}}>{fmt(curMonth.actual!=null?curMonth.actual:curMonth.predicted,metric)}</div><div style={{fontSize:11,color:"#999"}}>{fmt(curMonth.ci_low,metric)}{"\u2013"}{fmt(curMonth.ci_high,metric)}</div>{isBadCI(curMonth)?<div style={{fontSize:9,color:"#e67e22",marginTop:2}}>⚠ wide CI</div>:null}</div>:null}
{curQ?<div style={{background:isBadCI(curQ)?"#fff8f0":"#f4f6f7",border:isBadCI(curQ)?"1px solid #f0c040":"1px solid #ddd",borderRadius:8,padding:"10px 16px",flex:1,minWidth:120}}><div style={{fontSize:10,color:"#888",textTransform:"uppercase"}}>Quarter - Q2</div><div style={{fontSize:22,fontWeight:700}}>{fmt(curQ.actual!=null?curQ.actual:curQ.predicted,metric)}</div><div style={{fontSize:11,color:"#999"}}>{fmt(curQ.ci_low,metric)}{"\u2013"}{fmt(curQ.ci_high,metric)}</div>{isBadCI(curQ)?<div style={{fontSize:9,color:"#e67e22",marginTop:2}}>⚠ wide CI</div>:null}</div>:null}
{ye?<div style={{background:"#f4f6f7",border:"1px solid #ddd",borderRadius:8,padding:"10px 16px",flex:1,minWidth:120}}><div style={{fontSize:10,color:"#888",textTransform:"uppercase"}}>Year - 2026</div><div style={{fontSize:22,fontWeight:700}}>{fmt(ye.predicted,metric)}</div><div style={{fontSize:11,color:"#999"}}>{fmt(ye.ci_low,metric)}{"\u2013"}{fmt(ye.ci_high,metric)}</div></div>:null}
</div>
{/* Chart */}
<div style={{...cd,position:"relative"}}>
<div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:6}}>
<div style={{display:"flex",gap:16,fontSize:11,color:"#888"}}><span><span style={{display:"inline-block",width:16,height:3,background:"#3498db",borderRadius:2,marginRight:4}}/>Actual</span><span><span style={{display:"inline-block",width:16,height:0,borderTop:"2px dashed #1a2744",marginRight:4}}/>Predicted</span><span><span style={{display:"inline-block",width:16,height:10,background:"rgba(234,179,8,0.15)",borderRadius:2,marginRight:4}}/>CI</span></div>
<div style={{display:"flex",gap:4}}>{[["weekly","Weekly"],["cumulative","Cumulative"]].map(function(v){return <button key={v[0]} onClick={function(){setChartView(v[0]);}} style={{padding:"3px 10px",borderRadius:4,border:chartView===v[0]?"1px solid #3498db":"1px solid #ddd",background:chartView===v[0]?"#ebf5fb":"#fff",color:chartView===v[0]?"#2980b9":"#888",fontSize:11,cursor:"pointer",fontWeight:chartView===v[0]?600:400}}>{v[1]}</button>;})}</div>
</div>
{!chart?<div style={{textAlign:"center",padding:40,color:"#999"}}>Loading...</div>:
<svg viewBox={"0 0 "+cW+" "+cH} style={{width:"100%"}}>
{[0,0.25,0.5,0.75,1].map(function(f){return <g key={f}><line x1={pL} x2={cW-pR} y1={pT+plH*(1-f)} y2={pT+plH*(1-f)} stroke="#f0f0f0"/><text x={pL-4} y={pT+plH*(1-f)+4} textAnchor="end" fontSize={10} fill="#999">{fmt(chart.mx*f,metric)}</text></g>;})}
{["Q1","Q2","Q3","Q4"].map(function(q,i){var x1=chart.xS(i*13+1),x2=chart.xS(Math.min((i+1)*13,52));return <g key={q}><rect x={x1} y={pT} width={x2-x1} height={plH} fill={i%2===0?"rgba(26,39,68,0.03)":"transparent"}/><text x={(x1+x2)/2} y={pT+plH+42} textAnchor="middle" fontSize={11} fill="#bbb">{q}</text></g>;})}
{[1,5,9,14,18,23,27,32,36,40,45,49].map(function(w){return <text key={w} x={chart.xS(w)} y={pT+plH+14} textAnchor="middle" fontSize={8} fill="#888">W{w}</text>;})}
{mLbl.map(function(ml,i){var cx=(chart.xS(mStart[i])+chart.xS(mEnd[i]))/2;return <text key={"ml"+i} x={cx} y={pT+plH+28} textAnchor="middle" fontSize={10} fill="#aaa">{ml}</text>;})}
{chart.ciPath?<path d={chart.ciPath} fill="rgba(234,179,8,0.12)"/>:null}
{chart.predPath?<path d={chart.predPath} fill="none" stroke="#1a2744" strokeWidth={2} strokeDasharray="4,3"/>:null}
{chart.actPath?<path d={chart.actPath} fill="none" stroke="#3498db" strokeWidth={2.5}/>:null}
{chart.data.filter(function(d){return d.actual!=null;}).map(function(d){return <circle key={"a"+d.wk} cx={chart.xS(d.wk)} cy={chart.yS(d.actual)} r={3} fill="#3498db"/>;})}
</svg>}
</div>
{/* Monthly + Quarterly Tables */}
<div style={{display:"flex",gap:24,marginBottom:16}}>
<div style={{flex:1}}><div style={{fontSize:13,fontWeight:600,color:"#1a2744",marginBottom:6}}>Monthly</div>
<table style={{width:"100%",fontSize:11,borderCollapse:"collapse"}}><thead><tr style={{borderBottom:"1px solid #eee"}}><th style={thL}>Month</th><th style={th}>Actual</th><th style={th}>Pred</th><th style={th}>CI</th><th style={th}>Err</th></tr></thead>
<tbody>{months.map(function(r,i){return <TRow key={i} r={r} bg={i%2===0?"rgba(26,39,68,0.05)":"transparent"}/>;})}</tbody></table></div>
<div style={{flex:1,borderLeft:"2px solid #ddd",paddingLeft:20}}><div style={{fontSize:13,fontWeight:600,color:"#1a2744",marginBottom:6}}>Quarterly + Year-End</div>
<table style={{width:"100%",fontSize:11,borderCollapse:"collapse"}}><thead><tr style={{borderBottom:"1px solid #eee"}}><th style={thL}>Period</th><th style={th}>Actual</th><th style={th}>Pred</th><th style={th}>CI</th><th style={th}>Err</th></tr></thead>
<tbody>{quarters.map(function(r,i){return <TRow key={i} r={r} wt={600} co="#1a2744" bg={i%2===0?"rgba(26,39,68,0.05)":"transparent"}/>;})}{ye?<TRow r={{period_label:"2026 YE",actual:null,predicted:N(ye.predicted),ci_low:N(ye.ci_low),ci_high:N(ye.ci_high)}} wt={700} co="#1a2744" bg="rgba(26,39,68,0.05)"/>:null}</tbody></table></div></div>
{/* Weekly Table */}
<div style={cd}><div style={sT("#1a2744")}>Weekly (W1-W52)</div>
<div style={{maxHeight:400,overflowY:"auto"}}><table style={{width:"100%",fontSize:11,borderCollapse:"collapse"}}><thead><tr style={{borderBottom:"2px solid #eee",position:"sticky",top:0,background:"#fff"}}><th style={thL}>Week</th><th style={th}>Actual</th><th style={th}>Predicted</th><th style={th}>CI</th><th style={th}>Error</th></tr></thead>
<tbody>{weeks.map(function(r,i){return <TRow key={i} r={r} bg={i%2===0?"rgba(26,39,68,0.05)":"transparent"}/>;})}</tbody></table></div></div>
{/* Justification */}
<div style={{...cd,background:"#fafbfc"}}><div style={sT("#1a2744")}>Justification</div>
{narr.revisions?<div><div style={{fontSize:12,fontWeight:600,color:"#1a2744",marginBottom:4}}>Revisions</div><div style={nS}>{narr.revisions}</div></div>:null}
{narr.monthly?<div style={{marginTop:10}}><div style={{fontSize:12,fontWeight:600,color:"#1a2744",marginBottom:4}}>Monthly</div><div style={nS}>{narr.monthly}</div></div>:null}
{narr.quarterly?<div style={{marginTop:10}}><div style={{fontSize:12,fontWeight:600,color:"#1a2744",marginBottom:4}}>Quarterly</div><div style={nS}>{narr.quarterly}</div></div>:null}
{narr.year_end?<div style={{marginTop:10}}><div style={{fontSize:12,fontWeight:600,color:"#1a2744",marginBottom:4}}>Year-End</div><div style={nS}>{narr.year_end}</div></div>:null}</div>
<div style={{fontSize:10,color:"#bbb",textAlign:"right",marginTop:8}}>ps.forecast_tracker</div>
</div>);}
