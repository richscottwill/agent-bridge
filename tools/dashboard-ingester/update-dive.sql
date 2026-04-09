SELECT * FROM MD_UPDATE_DIVE_CONTENT(id:='68b308c1-97be-4c72-81ae-517318500de9'::UUID, content:='import { useSQLQuery } from "@motherduck/react-sql-query";
import { useState } from "react";
var N=function(v){return v!=null?Number(v):0;};
var fmt=function(v,t){if(v==null)return"\u2014";if(t==="cost")return"$"+N(v).toLocaleString(undefined,{maximumFractionDigits:0});if(t==="cpa")return"$"+N(v).toFixed(2);return N(v).toLocaleString();};
export default function Dive(){
var _m=useState("AU"),market=_m[0],setMarket=_m[1];
var _t=useState("registrations"),metric=_t[0],setMetric=_t[1];
var _h=useState(null),hover=_h[0],setHover=_h[1];
var waq=useSQLQuery("SELECT week_num,period_key,week_start,value FROM \"ps_analytics\".\"ps\".\"weekly_actuals\" WHERE market=''"+market+"'' AND metric_name=''"+metric+"'' ORDER BY week_num");
var pq=useSQLQuery("SELECT horizon,period_label,period_end,value,ci_low,ci_high,is_actual,reason,prior_prediction,prior_ci_low,prior_ci_high,prior_error_pct,prior_score,prior_made_on FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY horizon,period_label ORDER BY is_actual ASC, CASE WHEN reason LIKE ''%agent_trend%'' THEN 0 WHEN reason LIKE ''pipeline_sync:%'' THEN 1 ELSE 2 END, period_end DESC) as rn FROM \"ps_analytics\".\"ps\".\"projections_standalone\" WHERE market=''"+market+"'' AND metric_name=''"+metric+"'' AND reason NOT LIKE ''%bayesian_backfill%'') WHERE rn=1 ORDER BY period_end");
var nq=useSQLQuery("SELECT section,narrative FROM \"ps_analytics\".\"ps\".\"forecast_narratives\" WHERE market=''"+market+"'' AND channel=''ps''");
var cq=useSQLQuery("SELECT * FROM \"ps_analytics\".\"ps\".\"dive_forecast_calibration\" WHERE market=''"+market+"'' AND channel=''ps''");
var dd=function(q){return Array.isArray(q.data)?q.data:[];};
var waRows=dd(waq),projRows=dd(pq),cal=dd(cq);
var narr={};dd(nq).forEach(function(r){narr[r.section]=r.narrative;});
var moProj=projRows.filter(function(r){return r.horizon==="monthly";});
var qrProj=projRows.filter(function(r){return r.horizon==="quarterly";});
var yeProj=projRows.filter(function(r){return r.horizon==="year_end";});
var wkProj=projRows.filter(function(r){return r.horizon==="weekly";});
var weeklyData={};
waRows.forEach(function(r){weeklyData[r.week_num]={actual:N(r.value),predicted:null,ci_low:null,ci_high:null,prior:null,priorErr:null,priorScore:null};});
wkProj.forEach(function(r){
var wn=parseInt(r.period_label.replace("W",""));
if(!weeklyData[wn])weeklyData[wn]={actual:null,predicted:null,ci_low:null,ci_high:null,prior:null,priorErr:null,priorScore:null};
if(r.is_actual&&r.prior_prediction!=null){weeklyData[wn].predicted=N(r.prior_prediction);weeklyData[wn].ci_low=N(r.prior_ci_low||r.ci_low);weeklyData[wn].ci_high=N(r.prior_ci_high||r.ci_high);weeklyData[wn].priorErr=r.prior_error_pct;weeklyData[wn].priorScore=r.prior_score;}
else if(!r.is_actual){weeklyData[wn].predicted=N(r.value);weeklyData[wn].ci_low=N(r.ci_low);weeklyData[wn].ci_high=N(r.ci_high);}
});
var cumData=[];var runCum=0;
for(var w=1;w<=52;w++){var wd=weeklyData[w];if(wd){var val=wd.actual!=null?wd.actual:(wd.predicted||0);runCum+=val;cumData.push({wk:w,cum:runCum,weekly:val,actual:wd.actual,predicted:wd.predicted,ci_low:wd.ci_low,ci_high:wd.ci_high,isActual:wd.actual!=null});}}
var moByLabel={};moProj.forEach(function(r){moByLabel[r.period_label]=r;});
var qrByLabel={};qrProj.forEach(function(r){qrByLabel[r.period_label]=r;});
var yeRow=yeProj.length>0?yeProj[0]:null;
var ytdRegs=0;waRows.forEach(function(r){ytdRegs+=N(r.value);});
var mLbl=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
var currentMonthIdx=3;var currentMonthLabel=mLbl[currentMonthIdx];
var currentMonthProj=moByLabel[currentMonthLabel];
var currentQ="Q2";var currentQProj=qrByLabel[currentQ];
var gC=function(g){return g==="Excellent"?"#27ae60":g==="Good"?"#2ecc71":g==="Fair"?"#f39c12":g==="Pending"?"#95a5a6":"#e74c3c";};
var eC=function(e){var v=Math.abs(N(e));return v<3?"#27ae60":v<7?"#f39c12":"#e74c3c";};
var isBadCI=function(r){return r&&(N(r.ci_low)===0||N(r.ci_low)<0);};
var cd={background:"#fff",border:"1px solid #ddd",borderRadius:8,padding:16,marginBottom:16};
var sT=function(c){return{fontSize:15,fontWeight:600,marginBottom:10,paddingBottom:6,borderBottom:"2px solid "+c};};
var nS={fontSize:13,color:"#555",lineHeight:1.6,padding:"10px 12px",background:"#fafafa",borderRadius:6,marginTop:12,borderLeft:"3px solid #ddd"};
var th={textAlign:"right",padding:"5px 8px",color:"#888",fontSize:11};
var thL={textAlign:"left",padding:"5px 8px",color:"#888",fontSize:11};
// Chart — taller, with hover, monthly dots, weekly predictions
var cW=950,cH=700,pL=70,pR=20,pT=20,pB=85,plW=cW-pL-pR,plH=cH-pT-pB;
var mx=cumData.length>0?Math.max.apply(null,cumData.map(function(d){return d.cum;}))*1.08:1;
var xS=function(wk){return pL+((wk-1)/51)*plW;};
var yS=function(v){return pT+plH-(N(v)/mx)*plH;};
var actPath="",predPath="",ciPath="";
var lastActX=0,lastActY=0;
cumData.forEach(function(d,i){var x=xS(d.wk),y=yS(d.cum);if(d.isActual){actPath+=(actPath?"L":"M")+x+","+y;lastActX=x;lastActY=y;}else{predPath+=(predPath?"L":"M"+(i>0&&cumData[i-1].isActual?lastActX+","+lastActY+" L":""))+x+","+y;}});
var fcData=cumData.filter(function(d){return!d.isActual;});
if(fcData.length>0){var cumLow=ytdRegs,cumHigh=ytdRegs;var upper="M"+lastActX+","+lastActY,lower="";fcData.forEach(function(d){cumLow+=d.ci_low||d.predicted||0;cumHigh+=d.ci_high||d.predicted||0;upper+=" L"+xS(d.wk)+","+yS(cumHigh);});for(var j=fcData.length-1;j>=0;j--){cumLow=ytdRegs;for(var k=0;k<=j;k++)cumLow+=fcData[k].ci_low||fcData[k].predicted||0;lower+=" L"+xS(fcData[j].wk)+","+yS(cumLow);}ciPath=upper+lower+" L"+lastActX+","+lastActY+" Z";}
// Monthly cumulative dots for chart
var moCumDots=[];var mStart=[1,5,9,14,18,22,27,31,36,40,44,49];var mEnd=[4,8,13,17,22,26,31,35,39,44,48,52];
for(var mi=0;mi<12;mi++){var mCum=0;for(var wi2=1;wi2<=mEnd[mi]&&wi2<=52;wi2++){var wd3=weeklyData[wi2];if(wd3)mCum+=wd3.actual!=null?wd3.actual:(wd3.predicted||0);}if(mCum>0)moCumDots.push({wk:mEnd[mi],cum:mCum,label:mLbl[mi]});}
// Hover points
var hoverPts=[];cumData.forEach(function(d){hoverPts.push({x:xS(d.wk),y:yS(d.cum),label:"W"+d.wk,actual:d.actual,predicted:d.predicted,cum:d.cum,weekly:d.weekly,ci_low:d.ci_low,ci_high:d.ci_high});});
moCumDots.forEach(function(d){hoverPts.push({x:xS(d.wk),y:yS(d.cum),label:d.label,actual:null,predicted:null,cum:d.cum,weekly:null,ci_low:null,ci_high:null});});
// Derive monthly actuals from weekly_actuals (source of truth)
var mEnd2=[4,8,13,17,22,26,31,35,39,44,48,52];var moActuals={};
for(var mi2=0;mi2<12;mi2++){var mSum=0;var hasWeeks=false;for(var wi4=mi2===0?1:mEnd2[mi2-1]+1;wi4<=mEnd2[mi2];wi4++){var wd5=weeklyData[wi4];if(wd5&&wd5.actual!=null){mSum+=wd5.actual;hasWeeks=true;}}if(hasWeeks)moActuals[mLbl[mi2]]=mSum;}
// Derive quarterly actuals
var qActuals={};var qMonths=[["Jan","Feb","Mar"],["Apr","May","Jun"],["Jul","Aug","Sep"],["Oct","Nov","Dec"]];
qLabels.forEach(function(ql,qi){var qSum=0;var complete=true;qMonths[qi].forEach(function(ml){if(moActuals[ml]!=null)qSum+=moActuals[ml];else complete=false;});if(complete&&qSum>0)qActuals[ql]=qSum;});
// Monthly/quarterly/weekly table rows with prior predictions
var monthRows=mLbl.map(function(ml){var proj=moByLabel[ml];var act=moActuals[ml]!=null?moActuals[ml]:null;var pred=null;var ciL=null;var ciH=null;var pErr=null;var pScore=null;
if(proj&&proj.is_actual&&proj.prior_prediction!=null){pred=N(proj.prior_prediction);ciL=N(proj.prior_ci_low||proj.ci_low);ciH=N(proj.prior_ci_high||proj.ci_high);pErr=proj.prior_error_pct;pScore=proj.prior_score;}
else if(proj&&!proj.is_actual){pred=N(proj.value);ciL=N(proj.ci_low);ciH=N(proj.ci_high);}
return{period:ml,actual:act,predicted:pred,ci_low:ciL,ci_high:ciH,prior:null,priorErr:pErr,priorScore:pScore};});
var qLabels=["Q1","Q2","Q3","Q4"];
var qRows=qLabels.map(function(ql){var proj=qrByLabel[ql];var act=qActuals[ql]!=null?qActuals[ql]:null;var pred=null;var ciL=null;var ciH=null;var pErr=null;var pScore=null;
if(proj&&proj.is_actual&&proj.prior_prediction!=null){pred=N(proj.prior_prediction);ciL=N(proj.prior_ci_low||proj.ci_low);ciH=N(proj.prior_ci_high||proj.ci_high);pErr=proj.prior_error_pct;pScore=proj.prior_score;}
else if(proj&&!proj.is_actual){pred=N(proj.value);ciL=N(proj.ci_low);ciH=N(proj.ci_high);}
return{period:ql,actual:act,predicted:pred,ci_low:ciL,ci_high:ciH,prior:null,priorErr:pErr,priorScore:pScore};});
var wkRows=[];for(var wi3=1;wi3<=52;wi3++){var wd4=weeklyData[wi3];if(wd4&&(wd4.actual!=null||wd4.predicted!=null))wkRows.push({period:"W"+wi3,actual:wd4.actual,predicted:wd4.predicted,ci_low:wd4.ci_low,ci_high:wd4.ci_high,prior:wd4.prior,priorErr:wd4.priorErr,priorScore:wd4.priorScore});}
var moHasData=monthRows.some(function(r){return r.actual!=null||r.predicted!=null;});
var qHasData=qRows.some(function(r){return r.actual!=null||r.predicted!=null;});
var filteredCal=cal.filter(function(r){return r.metric_name===metric;});
var TRow=function(props){var r=props.r;var err=r.actual!=null&&r.predicted!=null&&r.actual>0?Math.abs((r.predicted-r.actual)/r.actual*100):null;return(<tr style={{borderBottom:"1px solid #f5f5f5",background:props.bg||"transparent"}}><td style={{padding:"5px 8px",fontWeight:props.wt||400,color:props.co||"#2c3e50",fontSize:12}}>{r.period}</td><td style={{padding:"5px 8px",textAlign:"right",fontWeight:r.actual!=null?600:400}}>{r.actual!=null?fmt(r.actual,metric):"\u2014"}</td><td style={{padding:"5px 8px",textAlign:"right"}}>{r.predicted!=null?fmt(r.predicted,metric):"\u2014"}</td><td style={{padding:"5px 8px",textAlign:"right",color:"#999",fontSize:10}}>{r.ci_low!=null?fmt(r.ci_low,metric)+"\u2013"+fmt(r.ci_high,metric):"\u2014"}</td>{r.prior!=null?<td style={{padding:"5px 8px",textAlign:"right",color:"#7f8c8d"}}>{fmt(r.prior,metric)}</td>:<td style={{padding:"5px 8px",textAlign:"right",color:"#ddd"}}>{"\u2014"}</td>}<td style={{padding:"5px 8px",textAlign:"right",color:err!=null?eC(err):"#ccc",fontWeight:600}}>{err!=null?err.toFixed(1)+"%":"\u2014"}</td>{r.priorScore?<td style={{padding:"5px 8px",textAlign:"right"}}><span style={{background:r.priorScore==="HIT"?"#27ae6022":r.priorScore==="MISS"?"#e74c3c22":"#f39c1222",color:r.priorScore==="HIT"?"#27ae60":r.priorScore==="MISS"?"#e74c3c":"#f39c12",padding:"1px 6px",borderRadius:3,fontSize:10,fontWeight:600}}>{r.priorScore}</span></td>:<td style={{padding:"5px 8px"}}></td>}</tr>);};
return(<div style={{fontFamily:"-apple-system,BlinkMacSystemFont,sans-serif",maxWidth:1100,margin:"0 auto",padding:20}}>
<h1 style={{fontSize:22,marginBottom:4}}>PS Forecast Tracker</h1>
<p style={{fontSize:12,color:"#888",marginBottom:12}}>2026 {metric}</p>
<div style={{display:"flex",gap:8,marginBottom:8,flexWrap:"wrap"}}>{[["AU","AU"],["MX","MX"],["US","US"],["CA","CA"],["JP","JP"],["EU5","EU5"],["WW","WW"]].map(function(x){return <button key={x[0]} onClick={function(){setMarket(x[0]);}} style={{padding:"6px 14px",borderRadius:6,border:market===x[0]?"2px solid #3498db":"1px solid #ddd",background:market===x[0]?"#ebf5fb":"#fff",color:market===x[0]?"#2980b9":"#666",fontWeight:market===x[0]?600:400,cursor:"pointer",fontSize:13}}>{x[1]}</button>;})}</div>
<div style={{display:"flex",gap:8,marginBottom:16,flexWrap:"wrap"}}>{[["registrations","Registrations"],["cost","Cost"],["cpa","CPA"]].map(function(x){return <button key={x[0]} onClick={function(){setMetric(x[0]);}} style={{padding:"6px 12px",borderRadius:6,border:metric===x[0]?"2px solid #555":"1px solid #ddd",background:metric===x[0]?"#f0f0f0":"#fff",color:metric===x[0]?"#333":"#666",fontWeight:metric===x[0]?600:400,cursor:"pointer",fontSize:13}}>{x[1]}</button>;})}</div>
<div style={{display:"flex",gap:16,marginBottom:16,flexWrap:"wrap"}}>
<div style={{background:"#f4f6f7",border:"1px solid #ddd",borderRadius:8,padding:"10px 16px",flex:1,minWidth:120}}><div style={{fontSize:10,color:"#888",textTransform:"uppercase"}}>YTD</div><div style={{fontSize:22,fontWeight:700}}>{fmt(ytdRegs,metric)}</div></div>
{currentMonthProj?<div style={{background:isBadCI(currentMonthProj)?"#fff8f0":"#f4f6f7",border:isBadCI(currentMonthProj)?"1px solid #f0c040":"1px solid #ddd",borderRadius:8,padding:"10px 16px",flex:1,minWidth:120}}><div style={{fontSize:10,color:"#888",textTransform:"uppercase"}}>Month - {currentMonthLabel}</div><div style={{fontSize:22,fontWeight:700}}>{fmt(currentMonthProj.value,metric)}</div><div style={{fontSize:11,color:"#999"}}>{fmt(currentMonthProj.ci_low,metric)}{"\u2013"}{fmt(currentMonthProj.ci_high,metric)}</div>{isBadCI(currentMonthProj)?<div style={{fontSize:9,color:"#e67e22",marginTop:2}}>⚠ wide CI — low confidence</div>:null}</div>:null}
{currentQProj?<div style={{background:isBadCI(currentQProj)?"#fff8f0":"#f4f6f7",border:isBadCI(currentQProj)?"1px solid #f0c040":"1px solid #ddd",borderRadius:8,padding:"10px 16px",flex:1,minWidth:120}}><div style={{fontSize:10,color:"#888",textTransform:"uppercase"}}>Quarter - {currentQ}</div><div style={{fontSize:22,fontWeight:700}}>{fmt(currentQProj.value,metric)}</div><div style={{fontSize:11,color:"#999"}}>{fmt(currentQProj.ci_low,metric)}{"\u2013"}{fmt(currentQProj.ci_high,metric)}</div>{isBadCI(currentQProj)?<div style={{fontSize:9,color:"#e67e22",marginTop:2}}>⚠ wide CI — low confidence</div>:null}</div>:null}
{yeRow?<div style={{background:"#f4f6f7",border:"1px solid #ddd",borderRadius:8,padding:"10px 16px",flex:1,minWidth:120}}><div style={{fontSize:10,color:"#888",textTransform:"uppercase"}}>Year - 2026</div><div style={{fontSize:22,fontWeight:700}}>{fmt(yeRow.value,metric)}</div><div style={{fontSize:11,color:"#999"}}>{fmt(yeRow.ci_low,metric)}{"\u2013"}{fmt(yeRow.ci_high,metric)}</div></div>:null}
</div>
<div style={{...cd,position:"relative"}}>
<div style={{display:"flex",gap:16,fontSize:11,color:"#888",marginBottom:2}}><span><span style={{display:"inline-block",width:16,height:3,background:"#3498db",borderRadius:2,marginRight:4}}/>Actual</span><span><span style={{display:"inline-block",width:16,height:0,borderTop:"2px dashed #1a2744",marginRight:4}}/>Predicted</span><span><span style={{display:"inline-block",width:16,height:10,background:"rgba(234,179,8,0.15)",borderRadius:2,marginRight:4}}/>CI</span></div>
{cumData.length===0?<div style={{textAlign:"center",padding:40,color:"#999"}}>No data</div>:
<svg viewBox={"0 0 "+cW+" "+cH} style={{width:"100%"}} onMouseLeave={function(){setHover(null);}}>
{[0,0.25,0.5,0.75,1].map(function(f){return <g key={f}><line x1={pL} x2={cW-pR} y1={pT+plH*(1-f)} y2={pT+plH*(1-f)} stroke="#f0f0f0"/><text x={pL-6} y={pT+plH*(1-f)+4} textAnchor="end" fontSize={11} fill="#999">{fmt(mx*f,metric)}</text></g>;})}
{["Q1","Q2","Q3","Q4"].map(function(q,i){var x1=xS(i*13+1),x2=xS(Math.min((i+1)*13,52));return <g key={q}><rect x={x1} y={pT} width={x2-x1} height={plH} fill={i%2===0?"rgba(26,39,68,0.03)":"transparent"}/><text x={(x1+x2)/2} y={pT+plH+55} textAnchor="middle" fontSize={12} fill="#bbb">{q}</text></g>;})}
{[1,4,8,12,14,18,22,26,30,35,39,44,48,52].map(function(w2){return <text key={w2} x={xS(w2)} y={pT+plH+16} textAnchor="middle" fontSize={9} fill="#888">W{w2}</text>;})}
{mLbl.map(function(ml,i){var cx=(xS(mStart[i])+xS(mEnd[i]))/2;return <text key={"ml"+i} x={cx} y={pT+plH+35} textAnchor="middle" fontSize={10} fill="#aaa">{ml}</text>;})}
{ciPath?<path d={ciPath} fill="rgba(234,179,8,0.12)"/>:null}
{predPath?<path d={predPath} fill="none" stroke="#1a2744" strokeWidth={2} strokeDasharray="4,3"/>:null}
{actPath?<path d={actPath} fill="none" stroke="#3498db" strokeWidth={2.5}/>:null}
{cumData.filter(function(d){return d.isActual;}).map(function(d,i){return <circle key={"a"+i} cx={xS(d.wk)} cy={yS(d.cum)} r={3} fill="#3498db"/>;})
}
{moCumDots.map(function(d,i){return <g key={"md"+i}><circle cx={xS(d.wk)} cy={yS(d.cum)} r={5} fill="#1a2744" stroke="#fff" strokeWidth={1.5}/><text x={xS(d.wk)} y={yS(d.cum)-10} textAnchor="middle" fontSize={10} fill="#1a2744" opacity={0.7}>{d.label}</text></g>;})}
{hoverPts.map(function(hp,i){return <circle key={"hov"+i} cx={hp.x} cy={hp.y} r={14} fill="transparent" onMouseEnter={function(){setHover(hp);}} style={{cursor:"pointer"}}/>;})
}
{hover?<g><line x1={hover.x} x2={hover.x} y1={pT} y2={pT+plH} stroke="#999" strokeWidth={0.5} strokeDasharray="3,3"/>
<rect x={hover.x>cW/2?hover.x-180:hover.x+8} y={Math.max(hover.y-60,pT)} width={170} height={hover.predicted!=null?58:hover.actual!=null?44:28} rx={4} fill="#fff" stroke="#ddd"/>
<text x={(hover.x>cW/2?hover.x-180:hover.x+8)+8} y={Math.max(hover.y-60,pT)+16} fontSize={11} fill="#333" fontWeight={600}>{hover.label} (cum: {fmt(hover.cum,metric)})</text>
{hover.actual!=null?<text x={(hover.x>cW/2?hover.x-180:hover.x+8)+8} y={Math.max(hover.y-60,pT)+30} fontSize={10} fill="#3498db">Actual: {fmt(hover.actual!=null?hover.actual:hover.weekly,metric)}</text>:null}
{hover.predicted!=null?<text x={(hover.x>cW/2?hover.x-180:hover.x+8)+8} y={Math.max(hover.y-60,pT)+(hover.actual!=null?44:30)} fontSize={10} fill="#1a2744">Pred: {fmt(hover.predicted,metric)} [{fmt(hover.ci_low,metric)}-{fmt(hover.ci_high,metric)}]</text>:null}
</g>:null}
</svg>}
</div>
<div style={{display:"flex",gap:24,marginBottom:16}}>
<div style={{flex:1}}><div style={{fontSize:13,fontWeight:600,color:"#1a2744",marginBottom:6}}>Monthly</div>
<table style={{width:"100%",fontSize:11,borderCollapse:"collapse"}}><thead><tr style={{borderBottom:"1px solid #eee"}}><th style={thL}>Month</th><th style={th}>Actual</th><th style={th}>Pred</th><th style={th}>CI</th><th style={th}>Prior</th><th style={th}>Err</th><th style={th}></th></tr></thead>
<tbody>{moHasData?monthRows.filter(function(r){return r.actual!=null||r.predicted!=null;}).map(function(r,i){return <TRow key={i} r={r} bg={i%2===0?"rgba(26,39,68,0.05)":"transparent"}/>;}):<tr><td colSpan={7} style={{padding:16,textAlign:"center",color:"#999",fontSize:12}}>No predictions yet</td></tr>}</tbody></table></div>
<div style={{flex:1,borderLeft:"2px solid #ddd",paddingLeft:20}}><div style={{fontSize:13,fontWeight:600,color:"#1a2744",marginBottom:6}}>Quarterly + Year-End</div>
<table style={{width:"100%",fontSize:11,borderCollapse:"collapse"}}><thead><tr style={{borderBottom:"1px solid #eee"}}><th style={thL}>Period</th><th style={th}>Actual</th><th style={th}>Pred</th><th style={th}>CI</th><th style={th}>Prior</th><th style={th}>Err</th><th style={th}></th></tr></thead>
<tbody>{qHasData?qRows.filter(function(r){return r.actual!=null||r.predicted!=null;}).map(function(r,i){return <TRow key={i} r={r} wt={600} co="#1a2744" bg={i%2===0?"rgba(26,39,68,0.05)":"transparent"}/>;}):<tr><td colSpan={7} style={{padding:16,textAlign:"center",color:"#999",fontSize:12}}>No predictions yet</td></tr>}{yeRow?<TRow r={{period:"2026 YE",actual:null,predicted:N(yeRow.value),ci_low:N(yeRow.ci_low),ci_high:N(yeRow.ci_high),prior:null,priorErr:null,priorScore:null}} wt={700} co="#1a2744" bg="rgba(26,39,68,0.05)"/>:null}</tbody></table></div></div>
<div style={cd}><div style={sT("#1a2744")}>Weekly (W1-W52)</div>
<div style={{maxHeight:400,overflowY:"auto"}}><table style={{width:"100%",fontSize:11,borderCollapse:"collapse"}}><thead><tr style={{borderBottom:"2px solid #eee",position:"sticky",top:0,background:"#fff"}}><th style={thL}>Week</th><th style={th}>Actual</th><th style={th}>Predicted</th><th style={th}>CI</th><th style={th}>Prior</th><th style={th}>Error</th><th style={th}></th></tr></thead>
<tbody>{wkRows.length>0?wkRows.map(function(r,i){return <TRow key={i} r={r} bg={i%2===0?"rgba(26,39,68,0.05)":"transparent"}/>;}):<tr><td colSpan={7} style={{padding:16,textAlign:"center",color:"#999",fontSize:12}}>No weekly data</td></tr>}</tbody></table></div></div>
<div style={{...cd,background:"#fafbfc"}}><div style={sT("#1a2744")}>Justification</div>
{narr.revisions?<div><div style={{fontSize:12,fontWeight:600,color:"#1a2744",marginBottom:4}}>Revisions</div><div style={nS}>{narr.revisions}</div></div>:null}
{narr.monthly?<div style={{marginTop:10}}><div style={{fontSize:12,fontWeight:600,color:"#1a2744",marginBottom:4}}>Monthly</div><div style={nS}>{narr.monthly}</div></div>:null}
{narr.quarterly?<div style={{marginTop:10}}><div style={{fontSize:12,fontWeight:600,color:"#1a2744",marginBottom:4}}>Quarterly</div><div style={nS}>{narr.quarterly}</div></div>:null}
{narr.year_end?<div style={{marginTop:10}}><div style={{fontSize:12,fontWeight:600,color:"#1a2744",marginBottom:4}}>Year-End</div><div style={nS}>{narr.year_end}</div></div>:null}</div>
<div style={cd}><div style={sT("#1a2744")}>Calibration</div>
{filteredCal.length===0?<div style={{color:"#999",fontSize:13,padding:16,textAlign:"center"}}>No reliable calibration data for {metric}</div>:
<table style={{width:"100%",fontSize:12,borderCollapse:"collapse"}}><thead><tr style={{borderBottom:"1px solid #eee"}}><th style={thL}>Metric</th><th style={th}>Horizon</th><th style={th}>N</th><th style={th}>CI Hit</th><th style={th}>Error</th><th style={th}>Grade</th></tr></thead>
<tbody>{filteredCal.map(function(r,i){return <tr key={i} style={{borderBottom:"1px solid #f5f5f5"}}><td style={{padding:"6px 8px",fontWeight:500}}>{r.metric_name}</td><td style={{padding:"6px 8px"}}>{r.horizon}</td><td style={{padding:"6px 8px",textAlign:"right"}}>{N(r.n_predictions)}</td><td style={{padding:"6px 8px",textAlign:"right"}}>{N(r.ci_hit_rate_pct).toFixed(0)}%</td><td style={{padding:"6px 8px",textAlign:"right"}}>{N(r.mean_abs_error_pct).toFixed(1)}%</td><td style={{padding:"6px 8px",textAlign:"right"}}><span style={{background:gC(r.calibration_grade)+"22",color:gC(r.calibration_grade),padding:"2px 8px",borderRadius:4,fontSize:11,fontWeight:600}}>{r.calibration_grade}</span></td></tr>;})}</tbody></table>}</div>
<div style={{fontSize:10,color:"#bbb",textAlign:"right",marginTop:8}}>ps_analytics.ps live</div>
</div>);}
');